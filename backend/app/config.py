from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    # Ollama settings (local)
    ollama_base_url: str = "http://localhost:11434"
    ollama_model: str = "llama3.2"  # or "mistral", "llama3.1", etc.
    
    # Embeddings settings (local)
    embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2"
    
    # PDF processing configuration
    chunk_size: int = 1000
    chunk_overlap: int = 200
    
    # Storage paths
    chroma_db_path: str = "./data/chroma_db"
    upload_dir: str = "./data/uploads"
    
    class Config:
        env_file = ".env"

@lru_cache()
def get_settings():
    """Returns a cached instance of the application settings"""
    return Settings()