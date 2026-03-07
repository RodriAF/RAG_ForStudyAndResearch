import fitz  # PyMuPDF
from typing import List
from pathlib import Path

class PDFProcessor:
    @staticmethod
    def extract_text(pdf_path: str) -> str:
        """Extracts all text from a PDF file"""
        doc = fitz.open(pdf_path)
        text = ""
        
        for page_num in range(len(doc)):
            page = doc[page_num]
            text += page.get_text()
        
        doc.close()
        return text
    
    @staticmethod
    def chunk_text(text: str, chunk_size: int = 1000, chunk_overlap: int = 200) -> List[str]:
        """Splits the text into chunks with overlap"""
        chunks = []
        start = 0
        text_length = len(text)
        
        while start < text_length:
            end = start + chunk_size
            
            # Attempt to split at a natural boundary (period, newline)
            if end < text_length:
                # Look for the last period or newline within the chunk
                chunk = text[start:end]
                last_period = chunk.rfind('.')
                last_newline = chunk.rfind('\n')
                
                cut_point = max(last_period, last_newline)
                if cut_point > chunk_size * 0.7:  # If it is in the last 30%
                    end = start + cut_point + 1
            
            chunks.append(text[start:end].strip())
            start = end - chunk_overlap  
        
        return chunks