from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import shutil
from pathlib import Path
from typing import List
import json
import os

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

# Metadata file to track collections
COLLECTIONS_META_FILE = Path(settings.chroma_db_path) / "collections_meta.json"

def load_collections_metadata():
    """Loads metadata of existing collections"""
    if COLLECTIONS_META_FILE.exists():
        try:
            with open(COLLECTIONS_META_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return {}
    return {}

def save_collections_metadata(metadata):
    """Saves metadata of collections"""
    try:
        with open(COLLECTIONS_META_FILE, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2, ensure_ascii=False)
    except Exception as e:
        print(f"Error saving metadata: {e}")

# Load metadata at startup
collections_metadata = load_collections_metadata()

class QueryRequest(BaseModel):
    question: str
    collection_name: str
    n_results: int = 5

class QueryResponse(BaseModel):
    answer: str
    sources: List[str]

@app.on_event("startup")
async def startup_event():
    """Verifies the status when starting the service"""
    print("\n" + "="*50)
    print("PDF RAG API - Starting...")
    print("="*50)
    
    # Check directories
    print(f"\n📁 Upload directory: {settings.upload_dir}")
    print(f"📁 ChromaDB directory: {settings.chroma_db_path}")
    
    # Load metadata
    global collections_metadata
    collections_metadata = load_collections_metadata()
    print(f"📚 Collections found in metadata: {len(collections_metadata)}")
    
    # Sync with actual ChromaDB collections
    try:
        chroma_collections = vector_store.list_collections()
        chroma_names = [col.name for col in chroma_collections]
        print(f"💾 Collections in ChromaDB: {len(chroma_names)}")
        
        # Clean metadata for collections that no longer exist
        to_delete = []
        for name in collections_metadata:
            if name not in chroma_names:
                to_delete.append(name)
        
        for name in to_delete:
            print(f"  🧹 Removing stale metadata for: {name}")
            del collections_metadata[name]
        
        if to_delete:
            save_collections_metadata(collections_metadata)
    except Exception as e:
        print(f"⚠️  Warning: Could not sync collections: {e}")
    
    # Check Ollama connection
    if llm_service.check_connection():
        print("✅ Ollama connected successfully")
        print(f"   Model: {settings.ollama_model}")
    else:
        print("⚠️  Warning: Ollama is not running")
        print("   Run: ollama serve")
    
    print("\n" + "="*50)
    print("🚀 Server ready at http://localhost:8000")
    print("📚 API documentation at http://localhost:8000/docs")
    print("="*50 + "\n")

@app.get("/")
async def root():
    """Test endpoint"""
    ollama_status = "✅ Connected" if llm_service.check_connection() else "❌ Not connected"
    
    # Get list of collections
    collections = list(collections_metadata.keys())
    
    return {
        "message": "PDF RAG API - Local with Ollama",
        "ollama_status": ollama_status,
        "model": settings.ollama_model,
        "collections_available": len(collections),
        "collections": collections[:10]  # Show first 10
    }

@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    """Uploads a PDF, processes it, and stores it in the vector DB"""
    
    if not file.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="File must be a PDF")
    
    # Generate collection name from filename
    base_name = file.filename.replace('.pdf', '').replace(' ', '_').lower()
    collection_name = base_name
    
    # If collection exists, add a number suffix
    counter = 1
    while collection_name in collections_metadata:
        collection_name = f"{base_name}_{counter}"
        counter += 1
    
    # Save file
    file_path = Path(settings.upload_dir) / file.filename
    with file_path.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    try:
        print(f"\n📄 Processing PDF: {file.filename}")
        print(f"   Collection name: {collection_name}")
        
        # 1. Extract text
        text = pdf_processor.extract_text(str(file_path))
        
        if not text.strip():
            # Clean up if no text
            file_path.unlink()
            raise HTTPException(status_code=400, detail="The PDF does not contain extractable text")
        
        print(f"   📝 Text extracted: {len(text)} characters")
        
        # 2. Split into chunks
        chunks = pdf_processor.chunk_text(
            text, 
            chunk_size=settings.chunk_size,
            chunk_overlap=settings.chunk_overlap
        )
        
        print(f"   ✂️  Text split into {len(chunks)} chunks")
        
        # 3. Create embeddings (this might take a while the first time)
        print(f"   🔄 Creating embeddings... (this may take a moment)")
        embeddings = embedding_service.create_embeddings(chunks)
        print(f"   ✅ Embeddings created: {len(embeddings)} vectors")
        
        # 4. Save to vector store
        metadata = [
            {"chunk_index": i, "source": file.filename, "collection": collection_name} 
            for i in range(len(chunks))
        ]
        
        num_chunks = vector_store.add_documents(
            collection_name=collection_name,
            chunks=chunks,
            embeddings=embeddings.tolist(),
            metadata=metadata
        )
        
        # 5. Save collection metadata
        collections_metadata[collection_name] = {
            "filename": file.filename,
            "num_chunks": num_chunks,
            "upload_date": str(file_path.stat().st_mtime),
            "file_size": file_path.stat().st_size,
            "original_name": file.filename
        }
        save_collections_metadata(collections_metadata)
        
        print(f"   💾 Saved to ChromaDB: {num_chunks} chunks")
        print(f"✅ PDF processed successfully!\n")
        
        return {
            "message": "PDF processed successfully",
            "collection_name": collection_name,
            "num_chunks": num_chunks,
            "filename": file.filename,
            "text_length": len(text)
        }
    
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        # Clean up in case of error
        if file_path.exists():
            file_path.unlink()
        print(f"❌ Error processing PDF: {str(e)}")
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
    
    # Verify collection exists
    if request.collection_name not in collections_metadata:
        raise HTTPException(
            status_code=404, 
            detail=f"Collection '{request.collection_name}' not found. Available: {list(collections_metadata.keys())}"
        )
    
    try:
        print(f"\n❓ Question: {request.question}")
        print(f"   Collection: {request.collection_name}")
        
        # 1. Create embedding for the question
        question_embedding = embedding_service.create_embedding(request.question)
        
        # 2. Search for similar chunks
        results = vector_store.search(
            collection_name=request.collection_name,
            query_embedding=question_embedding.tolist(),
            n_results=request.n_results
        )
        
        if not results['documents'][0]:
            raise HTTPException(status_code=404, detail="No relevant information found in the document")
        
        context_chunks = results['documents'][0]
        print(f"   📚 Found {len(context_chunks)} relevant chunks")
        
        # 3. Generate answer with Ollama (local)
        print(f"   🤔 Generating answer with Ollama...")
        answer = llm_service.generate_answer(
            question=request.question,
            context_chunks=context_chunks
        )
        
        print(f"   ✅ Answer generated\n")
        
        return QueryResponse(
            answer=answer,
            sources=context_chunks
        )
    
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Error processing question: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error processing question: {str(e)}")

@app.get("/collections")
async def list_collections():
    """Lists all available collections with metadata"""
    collections_list = []
    
    for col_name, metadata in collections_metadata.items():
        collections_list.append({
            "name": col_name,
            "filename": metadata.get("filename", "Unknown"),
            "num_chunks": metadata.get("num_chunks", 0),
            "upload_date": metadata.get("upload_date", "Unknown"),
            "file_size": metadata.get("file_size", 0),
            "file_size_mb": round(metadata.get("file_size", 0) / (1024 * 1024), 2) if metadata.get("file_size") else 0
        })
    
    # Sort by upload date (newest first)
    collections_list.sort(key=lambda x: x.get("upload_date", ""), reverse=True)
    
    return {
        "total": len(collections_list),
        "collections": collections_list
    }

@app.get("/collections/{name}")
async def get_collection_info(name: str):
    """Gets detailed information about a specific collection"""
    if name not in collections_metadata:
        raise HTTPException(status_code=404, detail="Collection not found")
    
    metadata = collections_metadata[name]
    
    # Try to get sample chunks from ChromaDB
    sample_chunks = []
    try:
        collection = vector_store.client.get_collection(name=name)
        # Get first 3 chunks as samples
        results = collection.get(limit=3)
        if results and results['documents']:
            sample_chunks = [
                {
                    "chunk": doc[:200] + "..." if len(doc) > 200 else doc,
                    "metadata": results['metadatas'][i] if results['metadatas'] else {}
                }
                for i, doc in enumerate(results['documents'])
            ]
    except:
        pass
    
    return {
        "name": name,
        "metadata": metadata,
        "sample_chunks": sample_chunks
    }

@app.delete("/collection/{name}")
async def delete_collection(name: str):
    """Deletes a collection and its associated PDF file"""
    
    # Verify collection exists
    if name not in collections_metadata:
        raise HTTPException(status_code=404, detail="Collection not found")
    
    try:
        # Get filename before deletion
        filename = collections_metadata[name].get("filename", f"{name}.pdf")
        file_path = Path(settings.upload_dir) / filename
        
        # Delete from ChromaDB
        success = vector_store.delete_collection(name)
        
        if success:
            # Delete PDF file if it exists
            if file_path.exists():
                file_path.unlink()
                print(f"🗑️  Deleted PDF file: {filename}")
            
            # Remove from metadata
            del collections_metadata[name]
            save_collections_metadata(collections_metadata)
            
            print(f"🗑️  Deleted collection: {name}")
            
            return {
                "message": f"Collection '{name}' deleted successfully",
                "deleted_files": {
                    "collection": name,
                    "pdf": filename if file_path.exists() else None
                }
            }
        else:
            raise HTTPException(status_code=500, detail="Error deleting collection from database")
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting collection: {str(e)}")

@app.delete("/collections")
async def delete_all_collections(confirm: bool = False):
    """Deletes ALL collections and PDF files (requires confirmation)"""
    
    if not confirm:
        raise HTTPException(
            status_code=400, 
            detail="This will delete ALL collections and PDF files. Add ?confirm=true to proceed."
        )
    
    deleted = []
    errors = []
    
    for name in list(collections_metadata.keys()):
        try:
            # Get filename
            filename = collections_metadata[name].get("filename", f"{name}.pdf")
            file_path = Path(settings.upload_dir) / filename
            
            # Delete from ChromaDB
            if vector_store.delete_collection(name):
                # Delete PDF if exists
                if file_path.exists():
                    file_path.unlink()
                
                deleted.append({
                    "collection": name,
                    "pdf": filename if file_path.exists() else None
                })
            else:
                errors.append(name)
        except Exception as e:
            errors.append(f"{name}: {str(e)}")
    
    # Clear metadata
    collections_metadata.clear()
    save_collections_metadata(collections_metadata)
    
    return {
        "message": f"Deleted {len(deleted)} collections",
        "deleted": deleted,
        "errors": errors if errors else None
    }

@app.post("/sync")
async def sync_collections():
    """Synchronizes ChromaDB collections with metadata"""
    try:
        # Get actual collections from ChromaDB
        chroma_collections = vector_store.list_collections()
        chroma_names = [col.name for col in chroma_collections]
        
        # Get collections from metadata
        metadata_names = list(collections_metadata.keys())
        
        # Find collections in ChromaDB but not in metadata
        new_collections = []
        for name in chroma_names:
            if name not in metadata_names:
                # Try to recover metadata from ChromaDB
                try:
                    collection = vector_store.client.get_collection(name=name)
                    # Get a sample to extract source info
                    sample = collection.get(limit=1)
                    source = "unknown.pdf"
                    if sample and sample['metadatas'] and sample['metadatas'][0]:
                        source = sample['metadatas'][0].get('source', 'unknown.pdf')
                    
                    collections_metadata[name] = {
                        "filename": source,
                        "num_chunks": collection.count(),
                        "upload_date": str(Path(settings.upload_dir / source).stat().st_mtime) if (settings.upload_dir / source).exists() else "unknown",
                        "file_size": (settings.upload_dir / source).stat().st_size if (settings.upload_dir / source).exists() else 0,
                        "original_name": source
                    }
                    new_collections.append(name)
                except:
                    pass
        
        # Find collections in metadata but not in ChromaDB
        stale_metadata = []
        for name in metadata_names:
            if name not in chroma_names:
                stale_metadata.append(name)
                del collections_metadata[name]
        
        # Save updated metadata
        if new_collections or stale_metadata:
            save_collections_metadata(collections_metadata)
        
        return {
            "message": "Collections synchronized",
            "chroma_collections": chroma_names,
            "metadata_collections": list(collections_metadata.keys()),
            "new_collections_found": new_collections,
            "stale_metadata_removed": stale_metadata
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error syncing: {str(e)}")

@app.get("/health")
async def health_check():
    """Verifies the status of all services"""
    
    # Check directories
    upload_dir_exists = Path(settings.upload_dir).exists()
    chroma_dir_exists = Path(settings.chroma_db_path).exists()
    
    # Check Ollama
    ollama_status = llm_service.check_connection()
    
    # Check ChromaDB
    try:
        chroma_collections = vector_store.list_collections()
        chroma_status = f"✅ OK ({len(chroma_collections)} collections)"
    except:
        chroma_status = "❌ Error"
    
    # Check disk space
    upload_dir_size = 0
    if upload_dir_exists:
        for f in Path(settings.upload_dir).glob('*'):
            if f.is_file():
                upload_dir_size += f.stat().st_size
    
    return {
        "api": {
            "status": "✅ OK",
            "version": "1.0.0"
        },
        "services": {
            "ollama": {
                "status": "✅ Connected" if ollama_status else "❌ Not connected",
                "model": settings.ollama_model
            },
            "embeddings": {
                "status": "✅ OK",
                "model": settings.embedding_model
            },
            "vector_db": {
                "status": chroma_status,
                "path": settings.chroma_db_path,
                "exists": chroma_dir_exists
            }
        },
        "storage": {
            "upload_dir": {
                "path": settings.upload_dir,
                "exists": upload_dir_exists,
                "files": len(list(Path(settings.upload_dir).glob('*.pdf'))),
                "size_mb": round(upload_dir_size / (1024 * 1024), 2)
            },
            "collections": len(collections_metadata)
        }
    }

@app.get("/debug/collections")
async def debug_collections():
    """Debug endpoint to see raw collection data"""
    try:
        # Get ChromaDB collections directly
        chroma_collections = vector_store.list_collections()
        chroma_data = []
        
        for col in chroma_collections:
            try:
                count = col.count()
                chroma_data.append({
                    "name": col.name,
                    "count": count,
                    "metadata": col.metadata
                })
            except:
                chroma_data.append({
                    "name": col.name,
                    "error": "Could not get details"
                })
        
        return {
            "chroma_collections": chroma_data,
            "metadata_collections": collections_metadata,
            "upload_dir": {
                "path": str(settings.upload_dir),
                "files": [f.name for f in Path(settings.upload_dir).glob('*.pdf')]
            }
        }
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app", 
        host="0.0.0.0", 
        port=8000,
        reload=True,  # Enable auto-reload during development
        log_level="info"
    )