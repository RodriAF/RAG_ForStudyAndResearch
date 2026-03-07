from sentence_transformers import SentenceTransformer
from typing import List
import numpy as np

class EmbeddingService:
    """
    Handles the generation of vector embeddings for text using the 
    sentence-transformers library.
    """
    def __init__(self, model_name: str = "sentence-transformers/all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model_name)
    
    def create_embeddings(self, texts: List[str]) -> np.ndarray:
        """Creates embeddings for a list of texts"""
        return self.model.encode(texts, show_progress_bar=True)
    
    def create_embedding(self, text: str) -> np.ndarray:
        """Creates an embedding for a single text"""
        return self.model.encode([text])[0]