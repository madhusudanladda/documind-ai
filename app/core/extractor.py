import fitz  # PyMuPDF
from typing import List, Dict, Any

def extract_text_from_pdf(pdf_path: str) -> List[Dict[str, Any]]:
    """
    Extracts text from each page of a PDF with metadata.
    Returns: List of dicts [{"page": 1, "text": "..."}]
    """
    doc = fitz.open(pdf_path)
    extracted_pages = []
    
    for page_num in range(len(doc)):
        page = doc[page_num]
        text = page.get_text("text").strip()
        if text:
            extracted_pages.append({
                "page": page_num + 1,
                "text": text
            })
            
    doc.close()
    return extracted_pages