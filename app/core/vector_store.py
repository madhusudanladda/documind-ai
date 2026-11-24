import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from typing import List, Dict, Any, Tuple

# Lightweight, fast aur high-accuracy model
embedder = SentenceTransformer("all-MiniLM-L6-v2")

def create_faiss_index(chunks: List[Dict[str, Any]]) -> Tuple[faiss.Index, List[Dict[str, Any]]]:
    """
    Creates normalized FAISS IndexFlatIP (Cosine Similarity) from chunks.
    """
    texts = [item["text"] for item in chunks]
    
    # Generate embeddings and normalize for cosine similarity
    embeddings = embedder.encode(texts, convert_to_numpy=True, normalize_embeddings=True)
    
    dim = embeddings.shape[1]
    index = faiss.IndexFlatIP(dim)
    index.add(embeddings.astype(np.float32))
    
    return index, chunks

def query_vector_store(
    query: str, 
    index: faiss.Index, 
    chunks: List[Dict[str, Any]], 
    top_k: int = 3
) -> List[Dict[str, Any]]:
    """
    Searches the most relevant chunks for a user question.
    """
    query_vector = embedder.encode([query], convert_to_numpy=True, normalize_embeddings=True)
    distances, indices = index.search(query_vector.astype(np.float32), top_k)
    
    results = []
    for idx in indices[0]:
        if idx != -1 and idx < len(chunks):
            results.append(chunks[idx])
            
    return results