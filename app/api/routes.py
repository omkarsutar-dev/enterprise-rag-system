from fastapi import APIRouter, UploadFile, File, Form, BackgroundTasks
import os
from fastapi.responses import StreamingResponse
from app.services.query_expansion import expand_query
from app.models.schemas import QueryRequest, QueryResponse, FeedbackRequest
from app.services.upload_service import process_upload
from app.services.retriever import hybrid_search
from app.services.reranker import rerank
from app.services.llm_service import generate_answer, generate_streaming_answer
from app.evaluation.evaluator import evaluate_system
from app.services.feedback_service import save_feedback
from app.services.cache_service import (
    generate_cache_key,
    get_cached_response,
    set_cached_response
)
from app.services.memory_service import (
    get_chat_history,
    append_message
)
from app.services.confidence_service import (
    calculate_confidence,
    is_confident
)

router = APIRouter()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


# -------------------------------
# 🔹 Utility: Dynamic Threshold
# -------------------------------
def dynamic_threshold(query: str):
    if len(query.split()) < 4:
        return 0.4
    return 0.3


# -------------------------------
# 🔹 Feedback API
# -------------------------------
@router.post("/feedback")
def submit_feedback(request: FeedbackRequest):
    save_feedback(request.dict())
    return {"message": "Feedback saved successfully"}


# -------------------------------
# 🔹 Upload API
# -------------------------------
@router.post("/upload")
async def upload_document(
        background_tasks: BackgroundTasks,
        tenant_id: str = Form(...),
        department: str = Form(...),
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


# -------------------------------
# 🔹 Query API
# -------------------------------
@router.post("/query", response_model=QueryResponse)
def query(request: QueryRequest):

    filters = {}

    if request.department and request.department.lower() not in ["", "string", "all", "none"]:
        filters["department"] = request.department

    if request.source and request.source.lower() not in ["", "string", "all", "none"]:
        filters["source"] = request.source

    cache_key = generate_cache_key(
        request.tenant_id,
        request.query,
        filters
    ) + f":session={request.session_id}"

    # ✅ Cache check
    cached = get_cached_response(cache_key)
    # cached = None
    if cached:
        print("It's Cached reponse.")
        return cached

    # ✅ Chat history
    history = get_chat_history(request.session_id)

    # Query expansion
    expanded_query = expand_query(request.query)

    # ✅ Retrieval
    chunks = hybrid_search(
        expanded_query,
        request.tenant_id,
        filters=filters,
        top_k=20
    )

    print(f"Chunks BEFORE rerank: {len(chunks)}")

    # ✅ Rerank
    reranked = rerank(request.query, chunks, top_k=3)
    print(f"Chunks after rerank: {len(reranked)}")
    if reranked : 
        for chunk in reranked:
            print(chunk)

    # ❌ No chunks found
    if not reranked:
        response = {
            "answer": "No relevant information found.",
            "confidence": 0.0,
            "source": []
        }
        set_cached_response(cache_key, response)
        return response

    # ✅ Confidence
    confidence = calculate_confidence(reranked)
    threshold = dynamic_threshold(request.query)

    print(f"Query: {request.query}")
    print(f"Confidence: {confidence}, Threshold: {threshold}")
    print(f"Chunks: {len(reranked)}")

    # ❌ Low confidence
    if not is_confident(confidence, threshold):
        response = {
            "answer": "I don’t have enough information to answer this question.",
            "confidence": confidence,
            "source": []
        }
        set_cached_response(cache_key, response)
        return response

    # ✅ Generate answer
    answer = generate_answer(request.query, reranked, history)

    response = {
        "answer": answer,
        "confidence": confidence,
        "source": reranked
    }

    # ✅ Save memory
    append_message(request.session_id, "user", request.query)
    append_message(request.session_id, "assistant", answer)

    # ✅ Cache full response
    set_cached_response(cache_key, response)

    return response


# -------------------------------
# 🔹 Streaming Query API
# -------------------------------
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

    cached = get_cached_response(cache_key)

    def stream_generator():

        # ✅ Cache hit
        if cached:
            yield cached["answer"]
            return

        history = get_chat_history(request.session_id)

        chunks = hybrid_search(
            request.query,
            request.tenant_id,
            filters=filters,
            top_k=20
        )

        reranked = rerank(request.query, chunks, top_k=3)

        if not reranked:
            yield "No relevant information found."
            return

        confidence = calculate_confidence(reranked)
        threshold = dynamic_threshold(request.query)

        yield f"[CONFIDENCE:{round(confidence, 2)}]\n"

        if not is_confident(confidence, threshold):
            yield "I don’t have enough information to answer this question."
            return

        full_answer = ""

        for token in generate_streaming_answer(
            request.query,
            reranked,
            history
        ):
            full_answer += token
            yield token

        # ✅ Save memory
        append_message(request.session_id, "user", request.query)
        append_message(request.session_id, "assistant", full_answer)

        # ✅ Cache
        set_cached_response(cache_key, {
            "answer": full_answer,
            "confidence": confidence,
            "source": reranked
        })

    return StreamingResponse(stream_generator(), media_type="text/plain")


# -------------------------------
# 🔹 Evaluation API
# -------------------------------
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