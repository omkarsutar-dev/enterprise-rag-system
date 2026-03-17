from fastapi import APIRouter, UploadFile, File, Form, BackgroundTasks
import os

from app.models.schemas import QueryRequest, QueryResponse
from app.services.upload_service import process_upload
from app.services.retriever import hybrid_search
from app.services.reranker import rerank
from app.services.llm_service import generate_answer

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

    chunks = hybrid_search(
        request.query,
        request.tenant_id,
        filters=filters,
        top_k=20
    )

    reranked = rerank(request.query, chunks, top_k=5)

    answer = generate_answer(request.query, reranked)

    return {"answer": answer}