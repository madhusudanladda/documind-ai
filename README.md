# DocuMind AI – AI-Powered Document Intelligence

DocuMind AI is a Retrieval-Augmented Generation (RAG) application that allows users to upload PDF documents and ask questions in natural language. It retrieves relevant information and generates answers with page-level citations.

Built using Python and FAISS without heavy frameworks like LangChain.

## 🚀 Features

- PDF text extraction with page numbers using PyMuPDF.
- Sliding-window text chunking with overlap.
- Local embeddings using Sentence Transformers.
- FAISS-based vector similarity search.
- Context-grounded answers using OpenAI API.
- Page-level source citations.
- FastAPI backend and Streamlit frontend.

## 🏗️ Architecture

```text
PDF Upload
    ↓
Text Extraction (PyMuPDF)
    ↓
Text Chunking
    ↓
Embeddings (Sentence Transformers)
    ↓
FAISS Vector Index
    ↓
Question & Similarity Search
    ↓
OpenAI API
    ↓
Answer + Page Citations
```

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| Python | Core Development |
| PyMuPDF | PDF Extraction |
| Sentence Transformers | Text Embeddings |
| FAISS | Vector Search |
| OpenAI API (gpt-4o-mini) | Answer Generation |
| FastAPI | Backend API |
| Streamlit | User Interface |

## 📁 Project Structure

```text
documind-ai/
├── app/
│   ├── api.py
│   ├── core/
│   │   ├── extractor.py
│   │   ├── chunker.py
│   │   └── vector_store.py
│   └── services/
│       └── rag_service.py
├── ui/
│   └── streamlit_app.py
├── requirements.txt
└── README.md
```

## ⚙️ Installation

**1. Clone the repository**

```bash
git clone https://github.com/YOUR_USERNAME/documind-ai.git
cd documind-ai
```

**2. Create virtual environment**

```bash
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**3. Install dependencies**

```bash
pip install -r requirements.txt
```

**4. Configure API Key**

Create a `.env` file:

```env
OPENAI_API_KEY=your_api_key_here
```

## ▶️ Run the Application

**Backend:**

```bash
uvicorn app.api:app --reload --port 8000
```

**Frontend (new terminal):**

```bash
streamlit run ui/streamlit_app.py
```

## 🔌 API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| POST | `/upload` | Upload and process PDF documents |
| POST | `/ask` | Ask questions and receive grounded answers |

---

*DocuMind AI – Intelligent Document Search and Question Answering.*
