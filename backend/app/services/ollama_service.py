import requests
from typing import List
from langdetect import detect, DetectorFactory
from langdetect.lang_detect_exception import LangDetectException

# Para resultados consistentes
DetectorFactory.seed = 0

class OllamaService:
    def __init__(self, base_url: str = "http://localhost:11434", model: str = "llama3.2"):
        self.base_url = base_url
        self.model = model
    
    def _detect_language(self, text: str) -> str:
        """Detect lang using langdetect"""
        try:
            lang = detect(text)
            # Mapear códigos a idiomas
            if lang == 'es':
                return 'spanish'
            elif lang == 'en':
                return 'english'
            else:
                # Por defecto inglés si no es español
                return 'english'
        except LangDetectException:
            return 'english'  # Default a inglés si hay error
    
    def generate_answer(self, question: str, context_chunks: List[str]) -> str:
        """Generates respones based on the context using Ollama"""

        language = self._detect_language(question)
        print(language)
        
        context = "\n\n".join([f"Fragment {i+1}:\n{chunk}" 
                               for i, chunk in enumerate(context_chunks)])
        
        if language == 'spanish':
            prompt = f"""Eres un asistente experto en analizar documentos. 
            Responde la pregunta basándote ÚNICAMENTE en el contexto proporcionado.
            IMPORTANTE: Debes responder SIEMPRE EN ESPAÑOL.
            Si la información no está en el contexto, di "No tengo suficiente información en el documento para responder esa pregunta."

            Contexto del documento:
            {context}

            Pregunta: {question}

            Responde de forma clara, concisa y directa basándote solo en el contexto anterior.

            Respuesta:"""
        else:
            prompt = f"""You are an expert document analysis assistant. 
            Answer the question based SOLELY on the provided context.
            If the information is not in the context, say "I don't have enough information in the document to answer that question."

            Document context:
            {context}

            Question: {question}

            Answer clearly, concisely and directly based only on the previous context.

            Answer:"""
        try:
            response = requests.post(
                f"{self.base_url}/api/generate",
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "stream": False,
                    "options": {
                        "temperature": 0.3,
                        "num_predict": 512,  # máximo tokens de respuesta
                    }
                },
                timeout=60  # timeout de 60 segundos
            )
            
            if response.status_code == 200:
                result = response.json()
                return result["response"]
            else:
                return f"Error generating response: {response.status_code}"
                
        except requests.exceptions.ConnectionError:
            return "Error: No conection to Ollama. ¿Is it running? Command: ollama serve"
        except Exception as e:
            return f"Unexpected error: {str(e)}"
    
    def check_connection(self) -> bool:
        """Verifies if Ollama is running"""
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            return response.status_code == 200
        except:
            return False