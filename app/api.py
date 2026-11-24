import os
import shutil
from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel
from typing import List

from app.core.extractor import extract_text_from_pdf
from app.core.chunker import chunk_pages_data
from app.core.vector_store import create_faiss_index, query_vector_store
from app.services.rag_service import generate_answer

app = FastAPI(title="DocuMind AI Backend")

# In-memory document storage (single-session state)
DOCUMENT_STATE = {
    "index": None,
    "chunks": []
}

class QueryRequest(BaseModel):
    question: str
    top_k: int = 3

class QueryResponse(BaseModel):
    answer: str
    sources: List[str]

@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")
    
    temp_dir = "temp_uploads"
    os.makedirs(temp_dir, exist_ok=True)
    temp_file_path = os.path.join(temp_dir, file.filename)
    
    with open(temp_file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        
    try:
        pages_data = extract_text_from_pdf(temp_file_path)
        if not pages_data:
            raise HTTPException(status_code=400, detail="No readable text found in PDF.")
            
        chunks = chunk_pages_data(pages_data)
        index, stored_chunks = create_faiss_index(chunks)
        
        DOCUMENT_STATE["index"] = index
        DOCUMENT_STATE["chunks"] = stored_chunks
        
        return {
            "message": "File processed successfully.",
            "pages_extracted": len(pages_data),
            "chunks_created": len(chunks)
        }
    finally:
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)

@app.post("/ask", response_model=QueryResponse)
async def ask_question(request: QueryRequest):
    if DOCUMENT_STATE["index"] is None or not DOCUMENT_STATE["chunks"]:
        raise HTTPException(status_code=400, detail="Please upload a PDF document first.")
    
    retrieved_chunks = query_vector_store(
        query=request.question,
        index=DOCUMENT_STATE["index"],
        chunks=DOCUMENT_STATE["chunks"],
        top_k=request.top_k
    )
    
    result = generate_answer(request.question, retrieved_chunks)
    return result