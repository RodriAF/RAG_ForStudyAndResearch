from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import shutil
from pathlib import Path
from typing import List

from app.config import get_settings
from app.services.pdf_processor import PDFProcessor
from app.services.embeddings import EmbeddingService
from app.services.vector_store import VectorStore
from app.services.ollama_service import OllamaService

app = FastAPI(title="PDF RAG API - Local with Ollama")

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

settings = get_settings()

# Initialize services
pdf_processor = PDFProcessor()
embedding_service = EmbeddingService(settings.embedding_model)
vector_store = VectorStore(settings.chroma_db_path)
llm_service = OllamaService(
    base_url=settings.ollama_base_url,
    model=settings.ollama_model
)

# Create required directories
Path(settings.upload_dir).mkdir(parents=True, exist_ok=True)
Path(settings.chroma_db_path).mkdir(parents=True, exist_ok=True)

class QueryRequest(BaseModel):
    question: str
    collection_name: str
    n_results: int = 5

class QueryResponse(BaseModel):
    answer: str
    sources: List[str]

@app.get("/")
async def root():
    """Test endpoint"""
    ollama_status = "✅ Connected" if llm_service.check_connection() else "❌ Not connected"
    return {
        "message": "PDF RAG API - Local with Ollama",
        "ollama_status": ollama_status,
        "model": settings.ollama_model
    }

@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    """Uploads a PDF, processes it, and stores it in the vector DB"""
    
    if not file.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="File must be a PDF")
    
    # Save file
    file_path = Path(settings.upload_dir) / file.filename
    with file_path.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    try:
        # 1. Extract text
        text = pdf_processor.extract_text(str(file_path))
        
        if not text.strip():
            raise HTTPException(status_code=400, detail="The PDF does not contain extractable text")
        
        # 2. Split into chunks
        chunks = pdf_processor.chunk_text(
            text, 
            chunk_size=settings.chunk_size,
            chunk_overlap=settings.chunk_overlap
        )
        
        # 3. Create embeddings (this might take a while the first time)
        embeddings = embedding_service.create_embeddings(chunks)
        
        # 4. Save to vector store
        collection_name = file.filename.replace('.pdf', '').replace(' ', '_').lower()
        
        metadata = [
            {"chunk_index": i, "source": file.filename} 
            for i in range(len(chunks))
        ]
        
        num_chunks = vector_store.add_documents(
            collection_name=collection_name,
            chunks=chunks,
            embeddings=embeddings.tolist(),
            metadata=metadata
        )
        
        return {
            "message": "PDF processed successfully",
            "collection_name": collection_name,
            "num_chunks": num_chunks,
            "filename": file.filename
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing PDF: {str(e)}")

@app.post("/query", response_model=QueryResponse)
async def query_document(request: QueryRequest):
    """Asks a question about a processed document"""
    
    # Verify connection with Ollama
    if not llm_service.check_connection():
        raise HTTPException(
            status_code=503, 
            detail="Ollama is not running. Run: ollama serve"
        )
    
    try:
        # 1. Create embedding for the question
        question_embedding = embedding_service.create_embedding(request.question)
        
        # 2. Search for similar chunks
        results = vector_store.search(
            collection_name=request.collection_name,
            query_embedding=question_embedding.tolist(),
            n_results=request.n_results
        )
        
        if not results['documents'][0]:
            raise HTTPException(status_code=404, detail="No relevant information found")
        
        context_chunks = results['documents'][0]
        
        # 3. Generate answer with Ollama (local)
        answer = llm_service.generate_answer(
            question=request.question,
            context_chunks=context_chunks
        )
        
        return QueryResponse(
            answer=answer,
            sources=context_chunks
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing question: {str(e)}")

@app.get("/collections")
async def list_collections():
    """Lists all available collections"""
    collections = vector_store.client.list_collections()
    return {"collections": [col.name for col in collections]}

@app.delete("/collection/{name}")
async def delete_collection(name: str):
    """Deletes a collection"""
    success = vector_store.delete_collection(name)
    if success:
        return {"message": f"Collection {name} deleted"}
    raise HTTPException(status_code=404, detail="Collection not found")

@app.get("/health")
async def health_check():
    """Verifies the status of all services"""
    return {
        "api": "✅ OK",
        "ollama": "✅ Connected" if llm_service.check_connection() else "❌ Not connected",
        "model": settings.ollama_model,
        "embeddings": settings.embedding_model,
        "vector_db": "ChromaDB"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)