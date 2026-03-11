from fastapi import APIRouter
from app.models.schemas import QueryRequest, QueryResponse
from app.services.retriever import hybrid_search
from app.services.reranker import rerank
from app.services.llm_service import generate_answer

router = APIRouter()


@router.post("/query", response_model=QueryResponse)
def query(request: QueryRequest):

    # Step 1: Retrieve candidate chunks
    chunks = hybrid_search(request.query, request.tenant_id, top_k=20)

    # Step 2: Rerank chunks
    reranked_chunks = rerank(request.query, chunks, top_k=5)

    # Step 3: Send best chunks to LLM
    answer = generate_answer(request.query, reranked_chunks)

    return {"answer": answer}