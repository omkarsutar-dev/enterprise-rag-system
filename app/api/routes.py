from fastapi import APIRouter
from app.models.schemas import QueryRequest, QueryResponse
from app.services.retriever import hybrid_search
from app.services.llm_service import generate_answer

router = APIRouter()

@router.post("/query", response_model=QueryResponse)
def query_rag(request: QueryRequest):
    results = hybrid_search(request.query)
    answer = generate_answer(request.query, results)
    return QueryResponse(answer=answer)