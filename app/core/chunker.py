from typing import List, Dict, Any

def chunk_pages_data(
    pages_data: List[Dict[str, Any]], 
    chunk_size: int = 500, 
    chunk_overlap: int = 50
) -> List[Dict[str, Any]]:
    """
    Splits text across pages into overlapping chunks while preserving page metadata.
    """
    chunks = []
    stride = chunk_size - chunk_overlap
    
    for item in pages_data:
        text = item["text"]
        page = item["page"]
        
        # Sliding window over the page text
        for i in range(0, len(text), stride):
            chunk = text[i:i + chunk_size].strip()
            # 20 characters se chhote useless fragments ko skip karo
            if len(chunk) > 20:
                chunks.append({
                    "text": chunk,
                    "page": page
                })
                
    return chunks