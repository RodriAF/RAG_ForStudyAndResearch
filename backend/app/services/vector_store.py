import chromadb
from chromadb.config import Settings
from typing import List, Dict
import uuid
import os

class VectorStore:
    """
    Handles interactions with the ChromaDB vector database,
    including collection management, document storage, and similarity search.
    """
    def __init__(self, persist_directory: str = "./data/chroma_db"):
        # Asegurar que el directorio existe
        os.makedirs(persist_directory, exist_ok=True)
        
        # Configuración CORRECTA para persistencia
        self.client = chromadb.PersistentClient(
            path=persist_directory
        )

    def create_collection(self, name: str):
        """Creates or retrieves an existing collection"""
        return self.client.get_or_create_collection(name=name)
    
    def add_documents(self, collection_name: str, chunks: List[str], 
                      embeddings: List, metadata: List[Dict] = None):
        """Adds documents (text chunks) to the specified collection"""
        collection = self.create_collection(collection_name)
        
        # Generate unique IDs for each chunk
        ids = [str(uuid.uuid4()) for _ in chunks]
        
        if metadata is None:
            metadata = [{"chunk_index": i} for i in range(len(chunks))]
        
        collection.add(
            embeddings=embeddings,
            documents=chunks,
            metadatas=metadata,
            ids=ids
        )
        
        return len(chunks)
    
    def search(self, collection_name: str, query_embedding: List[float], 
               n_results: int = 5):
        """Searches for the most similar chunks based on vector similarity"""
        try:
            collection = self.client.get_collection(name=collection_name)
            
            results = collection.query(
                query_embeddings=[query_embedding],
                n_results=n_results
            )
            
            return results
        except ValueError:
            return {'documents': [[]], 'metadatas': [[]], 'distances': [[]]}
    
    def delete_collection(self, collection_name: str):
        """Deletes a collection from the database"""
        try:
            self.client.delete_collection(name=collection_name)
            return True
        except:
            return False
    
    def list_collections(self):
        """Lists all collections"""
        return self.client.list_collections()