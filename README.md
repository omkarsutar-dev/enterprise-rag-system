# Enterprise Adaptive RAG System

An enterprise-grade Adaptive Retrieval-Augmented Generation (RAG) system built using FastAPI, FAISS, BM25, OCR, Hybrid Search, Reranking, Confidence Scoring, Feedback Learning, and Streamlit UI.

---

# 🚀 Features

## ✅ Multi-Tenant RAG
- Separate vector indexes per tenant
- Tenant-specific retrieval pipeline

---

## ✅ OCR-Based Document Processing
Supports:
- PDF
- Scanned PDFs
- TXT documents

Uses OCR + intelligent parsing to extract structured content.

---

## ✅ Advanced Chunking
- Semantic chunking
- Section-aware chunking
- Heading-based parsing

---

## ✅ Hybrid Search
Combines:
- Semantic Search (FAISS)
- Keyword Search (BM25)

for better retrieval quality.

---

## ✅ Score-based Reranking
Uses:
- Adaptive weighted reranking to rerank retrieved chunks.

---

## ✅ Confidence + No-Hallucination System
- Confidence scoring
- Rejects weak-context answers
- Prevents hallucinated responses

---

## ✅ Query Expansion
Improves retrieval using:
- Synonym expansion
- LLM-assisted query expansion

---

## ✅ Feedback Learning System
Adaptive retrieval:
- Positive feedback boosts chunks
- Negative feedback reduces ranking

---

## ✅ Streaming Responses
Supports token streaming for chat-like UX.

---

## ✅ Streamlit Demo UI
Interactive frontend for:
- Document upload
- Chat interface
- Streaming answers
- Confidence visualization
- Source inspection

---

# 🏗️ Architecture

User Query
→ Query Expansion
→ BM25 + FAISS Retrieval
→ Cross-Encoder Reranking
→ Confidence Filtering
→ LLM Response Generation
→ Feedback Learning Loop

---

# 📁 Project Structure

```
enterprise-rag-system/
│
├── app/
│   ├── api/
│   ├── core/
│   ├── services/
│   ├── utils/
│   ├── evaluation/
│   ├── models/
│
├── streamlit_app/
│   ├── app.py
│   ├── api_client.py
│   ├── components/
│   │   ├── sidebar.py
│   │   ├── uploader.py
│   │   ├── chat.py
│
├── uploads/
├── vector_store/
├── requirements.txt
```

---

# ⚙️ Tech Stack

## Backend
- FastAPI
- Python

## Retrieval
- FAISS
- BM25
- SentenceTransformers

## LLM
- OpenAI GPT

## OCR
- pdfplumber
- pytesseract

## Frontend
- Streamlit

---

# 🔥 Installation

## 1. Clone Repository

```bash
git clone https://github.com/omkarsutar-dev/enterprise-rag-system.git
cd enterprise-rag-system
```

---

## 2. Create Virtual Environment

```bash
python -m venv venv
venv\Scripts\activate       # Windows
source venv/bin/activate    # Linux/Mac
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```
---

# 🔑 Environment Variables

Create `.env`
```bash
OPENAI_API_KEY=your_openai_key
```
---

# 🚀 Run Backend

```bash
uvicorn app.main:app --reload
```
Backend:
```bash
http://127.0.0.1:8000
```

Swagger Docs:
```bash
http://127.0.0.1:8000/docs
```
---

# 🚀 Run Streamlit UI

```bash
streamlit run streamlit_app/app.py
```

UI:
```bash
http://localhost:8501
```

---

# 📤 Upload Documents

Supported:
- TXT
- PDF
- Scanned PDFs

Metadata:
- tenant_id
- department

---

# 💬 Query Example

{
  "query": "How many sick leaves are allowed?",
  "tenant_id": "company_a",
  "department": "HR",
  "source": "",
  "session_id": "session_1"
}

---

# 📊 Evaluation Metrics

System supports:
- Precision
- Recall
- Exact Match
- Latency

---

# 🔥 Key Engineering Highlights

- Adaptive Retrieval
- OCR + Structured Parsing
- Hybrid Retrieval Architecture
- Feedback Learning
- Confidence-Based Hallucination Prevention
- Streaming AI Responses

---

# 🚀 Future Improvements

- LangChain migration
- LangGraph workflows
- Kubernetes deployment
- Observability dashboard
- Role-based access control
- Async indexing pipeline

---

## 👨‍💻 Author

**Omkar Sutar**
GenAI Engineer

---

## ⭐ If you like this project

Give it a ⭐ on GitHub — it helps a lot!