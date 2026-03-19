from fastapi import APIRouter, UploadFile, File, Form, BackgroundTasks
import os

from app.models.schemas import QueryRequest, QueryResponse
from app.services.upload_service import process_upload
from app.services.retriever import hybrid_search
from app.services.reranker import rerank
from app.services.llm_service import generate_answer
from app.services.cache_service import (
    generate_cache_key,
    get_cached_response,
    set_cached_response
)


router = APIRouter()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


# ✅ Upload API (with dynamic metadata)
@router.post("/upload")
async def upload_document(
        background_tasks: BackgroundTasks,
        tenant_id: str = Form(...),
        department: str = Form(...),   # dynamic
        file: UploadFile = File(...)
):

    file_path = os.path.join(UPLOAD_DIR, file.filename)

    with open(file_path, "wb") as f:
        f.write(await file.read())

    background_tasks.add_task(
        process_upload,
        file_path,
        tenant_id,
        department
    )

    return {
        "message": "Document uploaded. Indexing started in background."
    }


# ✅ Query API (with filters)
@router.post("/query", response_model=QueryResponse)
def query(request: QueryRequest):

    filters = {
        "department": request.department,
        "source": request.source
    }

    # ✅ Step 1: Generate cache key
    cache_key = generate_cache_key(
        request.tenant_id,
        request.query,
        filters
    )

    # ✅ Step 2: Check cache
    cached = get_cached_response(cache_key)

    if cached:
        return {"answer": cached}

    # ✅ Step 3: Retrieve
    chunks = hybrid_search(
        request.query,
        request.tenant_id,
        filters=filters,
        top_k=20
    )

    # ✅ Step 4: Rerank
    reranked = rerank(request.query, chunks, top_k=5)

    # ✅ Step 5: LLM
    answer = generate_answer(request.query, reranked)

    # ✅ Step 6: Store in cache
    set_cached_response(cache_key, answer)

    return {"answer": answer}