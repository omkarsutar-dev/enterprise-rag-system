from fastapi import APIRouter
from app.models.schemas import QueryRequest, QueryResponse
from app.services.retriever import hybrid_search
from app.services.llm_service import generate_answer

router = APIRouter()

@router.post("/query", response_model=QueryResponse)
def query(request: QueryRequest):
    chunks = hybrid_search(request.query, request.tenant_id)
    answer = generate_answer(request.query, chunks)
    return {"answer": answer}