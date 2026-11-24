import os
from openai import OpenAI
from typing import List, Dict, Any
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def build_prompt(query: str, retrieved_chunks: List[Dict[str, Any]]) -> str:
    context_blocks = []
    for chunk in retrieved_chunks:
        context_blocks.append(f"[Page {chunk['page']}]\n{chunk['text']}")
    
    context_text = "\n\n---\n\n".join(context_blocks)
    
    prompt = f"""You are a precise document assistant. Answer the user question strictly using only the provided context below.
If the answer cannot be found in the context, explicitly say: "Information not found in the document."
Always cite the specific page numbers where the information was extracted.

Context:
{context_text}

Question: {query}

Answer:"""
    return prompt

def generate_answer(query: str, retrieved_chunks: List[Dict[str, Any]]) -> Dict[str, Any]:
    if not retrieved_chunks:
        return {
            "answer": "No relevant context found in the document.",
            "sources": []
        }
    
    prompt = build_prompt(query, retrieved_chunks)
    
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a factual document QA assistant."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.0
    )
    
    answer_text = response.choices[0].message.content
    pages = sorted(list({chunk["page"] for chunk in retrieved_chunks}))
    
    return {
        "answer": answer_text,
        "sources": [f"Page {p}" for p in pages]
    }