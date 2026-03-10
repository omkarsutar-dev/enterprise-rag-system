# Enterprise Multi-Tenant RAG System

A **production-oriented Retrieval Augmented Generation (RAG) platform** designed to answer questions from enterprise documents with **high accuracy, low latency, and tenant-level data isolation**.

This project demonstrates how modern AI systems combine **vector search, hybrid retrieval, and LLMs** to build scalable enterprise knowledge assistants.

---

## 🚀 Key Features

* **Multi-Tenant Architecture** – isolated vector indexes per organization
* **Hybrid Retrieval** – semantic search (embeddings) + keyword search
* **Vector Database** – FAISS for high-performance similarity search
* **Chunking Pipeline** – optimized document segmentation with overlap
* **LLM Response Generation** – contextual answers grounded in retrieved documents
* **FastAPI Backend** – scalable API layer for AI services

---

## 🏗 System Architecture

User Query
↓
Hybrid Retrieval (Semantic + Keyword Search)
↓
Top Relevant Chunks
↓
LLM Context Generation
↓
Final Answer

---

## 📂 Project Structure

```
enterprise-rag/

app/
 ├── api/                # API routes
 ├── services/           # Retrieval, embeddings, LLM services
 ├── models/             # Request/response schemas
 ├── core/               # Tenant management
 └── utils/              # Chunking utilities

data/                    # Tenant documents
vector_store/            # FAISS indexes
scripts/                 # Index building scripts
```

---

## ⚙️ Tech Stack

* Python
* FastAPI
* FAISS
* OpenAI Embeddings
* Scikit-Learn
* NumPy

---

## ▶️ Running the Project

Install dependencies:

```
pip install -r requirements.txt
```

Add your API key in `.env`:

```
OPENAI_API_KEY=your_key
```

Build document index:

```
python scripts/build_index.py
```

Run the API server:

```
uvicorn app.main:app --reload
```

Open API docs:

```
http://localhost:8000/docs
```

---

## 🎯 Use Cases

* Enterprise knowledge assistants
* Internal documentation search
* Policy / HR Q&A systems
* AI copilots for organizations

---

## 🔮 Future Improvements

* Reranking models for better retrieval precision
* Metadata filtering
* Streaming responses
* Cloud deployment on AWS
* Monitoring and evaluation pipelines

---

## 👨‍💻 Author

**Omkar Sutar**
Python Developer | Generative AI Engineer

Focused on building **Scalable AI systems and production-ready LLM applications**.
