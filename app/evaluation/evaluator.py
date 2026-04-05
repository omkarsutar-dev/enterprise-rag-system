import json
import time

from app.services.retriever import hybrid_search
from app.services.reranker import rerank
from app.services.llm_service import generate_answer

from app.evaluation.metrics import (
    precision_at_k,
    recall_at_k,
    exact_match
)


def evaluate_system(tenant_id):

    with open("app/evaluation/dataset.json") as f:
        dataset = json.load(f)

    results = []

    for item in dataset:

        query = item["query"]
        expected = item["expected_answer"]
        relevant = item["relevant_docs"]

        start_time = time.time()
        filters = item.get("metadata", {})

        chunks = hybrid_search(
            query,
            tenant_id,
            filters=filters,
            top_k=5
        )
        
        # chunks = hybrid_search(query, tenant_id, top_k=5)

        # Rerank
        reranked = rerank(query, chunks, top_k=3)

        # Retrieval
        retrieved_texts = [c["text"] for c in reranked]

        # LLM
        answer = generate_answer(query, reranked, history=[])

        latency = time.time() - start_time

        # Metrics
        precision = precision_at_k(retrieved_texts, relevant)
        recall = recall_at_k(retrieved_texts, relevant)
        em = exact_match(answer, expected)

        results.append({
            "query": query,
            "precision": precision,
            "recall": recall,
            "exact_match": em,
            "latency": latency
        })

    return results