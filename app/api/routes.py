from fastapi import APIRouter, UploadFile, File, Form, BackgroundTasks
import os
from fastapi.responses import StreamingResponse
from app.models.schemas import QueryRequest, QueryResponse
from app.services.upload_service import process_upload
from app.services.retriever import hybrid_search
from app.services.reranker import rerank
from app.services.llm_service import generate_answer
from app.services.llm_service import generate_streaming_answer
from app.evaluation.evaluator import evaluate_system



from app.services.cache_service import (
    generate_cache_key,
    get_cached_response,
    set_cached_response
)
from app.services.memory_service import (
    get_chat_history,
    append_message
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

    # ✅ Cache key includes session
    cache_key = generate_cache_key(
        request.tenant_id,
        request.query,
        filters
    ) + f":session={request.session_id}"

    cached = get_cached_response(cache_key)

    if cached:
        return {"answer": cached}

    # ✅ Get chat history
    history = get_chat_history(request.session_id)

    # ✅ Retrieval
    chunks = hybrid_search(
        request.query,
        request.tenant_id,
        filters=filters,
        top_k=20
    )

    # ✅ Rerank
    reranked = rerank(request.query, chunks, top_k=5)

    # ✅ LLM with memory
    answer = generate_answer(request.query, reranked, history)

    # ✅ Save conversation
    append_message(request.session_id, "user", request.query)
    append_message(request.session_id, "assistant", answer)

    # ✅ Cache
    set_cached_response(cache_key, answer)

    return {"answer": answer}


@router.post("/query-stream")
def query_stream(request: QueryRequest):

    filters = {
        "department": request.department,
        "source": request.source
    }

    cache_key = generate_cache_key(
        request.tenant_id,
        request.query,
        filters
    ) + f":session={request.session_id}"

    # ✅ Check cache first
    cached = get_cached_response(cache_key)

    def stream_generator():

        # 🔥 CASE 1: Cache hit
        if cached:
            yield cached
            return

        # 🔥 CASE 2: Cache miss
        history = get_chat_history(request.session_id)

        chunks = hybrid_search(
            request.query,
            request.tenant_id,
            filters=filters,
            top_k=20
        )

        reranked = rerank(request.query, chunks, top_k=5)

        full_answer = ""

        for token in generate_streaming_answer(
            request.query,
            reranked,
            history
        ):
            full_answer += token
            yield token

        # Save memory
        append_message(request.session_id, "user", request.query)
        append_message(request.session_id, "assistant", full_answer)

        # Save cache
        set_cached_response(cache_key, full_answer)

    return StreamingResponse(stream_generator(), media_type="text/plain")



@router.get("/evaluate")
def evaluate(tenant_id: str):

    results = evaluate_system(tenant_id)

    avg_precision = sum(r["precision"] for r in results) / len(results)
    avg_recall = sum(r["recall"] for r in results) / len(results)
    avg_em = sum(r["exact_match"] for r in results) / len(results)
    avg_latency = sum(r["latency"] for r in results) / len(results)

    return {
        "avg_precision": avg_precision,
        "avg_recall": avg_recall,
        "avg_exact_match": avg_em,
        "avg_latency": avg_latency,
        "details": results
    }