# Enterprise Multi-Tenant RAG Platform

A production-style **Retrieval Augmented Generation (RAG) system** that enables organizations to query internal documents using LLMs with **hybrid retrieval, reranking, and dynamic document ingestion**.

This project demonstrates how modern AI systems combine **vector search, keyword search, and cross-encoder reranking** to build scalable enterprise knowledge assistants.

---

## 🚀 Key Features

* **Multi-Tenant Architecture** – isolated knowledge base for each organization
* **Hybrid Retrieval** – semantic search + keyword search
* **Cross-Encoder Reranking** – improves document relevance
* **Dynamic Document Upload** – upload PDFs/TXT via API
* **Automatic Indexing Pipeline** – chunking → embeddings → vector index update
* **Vector Search** – FAISS for high-performance similarity search
* **FastAPI Backend** – scalable AI service layer

---

## 🧠 System Pipeline

User Upload Document
↓
Text Extraction (PDF/TXT)
↓
Chunking with Overlap
↓
Embedding Generation
↓
FAISS Vector Index Update

User Query
↓
Hybrid Retrieval (Semantic + Keyword)
↓
Reranking Model
↓
Top Context Chunks
↓
LLM Answer Generation

---

## 📂 Project Structure

```
enterprise-rag/

app/
 ├── api/            # FastAPI routes
 ├── core/           # Tenant management
 ├── models/         # API schemas
 ├── services/       # Retrieval, reranking, ingestion, LLM
 └── utils/          # Chunking and file parsing

uploads/             # Uploaded documents
data/                # Tenant data
vector_store/        # FAISS vector indexes
scripts/             # Index build scripts
```

---

## ⚙️ Tech Stack

* Python
* FastAPI
* FAISS (Vector Database)
* OpenAI Embeddings
* Sentence Transformers (Reranker)
* Scikit-Learn (Keyword Search)
* PyPDF (Document Parsing)

---

## ▶️ Running the Project

Install dependencies

```
pip install -r requirements.txt
```

Add OpenAI API key

```
OPENAI_API_KEY=your_api_key
```

Run the API server

```
uvicorn app.main:app --reload
```

Open API documentation

```
http://localhost:8000/docs
```

---

## 🎯 Use Cases

* Enterprise knowledge assistants
* Internal documentation search
* HR policy Q&A systems
* AI copilots for organizations

---

## 🔮 Next Improvements

* Asynchronous document indexing
* Query caching
* Metadata filtering
* Evaluation metrics
* Cloud deployment

---

## 👨‍💻 Author

Omkar Sutar
Python Developer →  Generative AI Engineer
