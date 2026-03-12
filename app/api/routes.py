from fastapi import APIRouter
from app.models.schemas import QueryRequest, QueryResponse
from app.services.retriever import hybrid_search
from app.services.reranker import rerank
from app.services.llm_service import generate_answer
from fastapi import APIRouter, UploadFile, File, Form
import os
from app.services.upload_service import process_upload

router = APIRouter()


# Query section
@router.post("/query", response_model=QueryResponse)
def query(request: QueryRequest):

    # Step 1: Retrieve candidate chunks
    chunks = hybrid_search(request.query, request.tenant_id, top_k=20)

    # Step 2: Rerank chunks
    reranked_chunks = rerank(request.query, chunks, top_k=5)

    # Step 3: Send best chunks to LLM
    answer = generate_answer(request.query, reranked_chunks)

    return {"answer": answer}


# Upload section
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/upload")
async def upload_document(
        tenant_id: str = Form(...),
        file: UploadFile = File(...)
):

    file_path = os.path.join(UPLOAD_DIR, file.filename)

    with open(file_path, "wb") as f:
        f.write(await file.read())

    process_upload(file_path, tenant_id)

    return {"message": "Document uploaded and indexed successfully"}