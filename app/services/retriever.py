import numpy as np

from app.services.embeddings import get_embedding
from app.services.vector_store import load_index
from app.services.bm25_service import bm25_search

# ✅ NEW
from app.services.scoring_service import normalize_scores, combine_scores


def apply_filters(metadata, filters):

    if not filters:
        return metadata

    filtered = []

    for doc in metadata:

        match = True

        if "department" in filters:
            if doc.get("department") != filters["department"]:
                match = False

        if "source" in filters:
            if doc.get("source") != filters["source"]:
                match = False

        if match:
            filtered.append(doc)

    return filtered


def hybrid_search(query, tenant_id, filters=None, top_k=20):

    index, metadata = load_index(tenant_id)

    if filters:
        metadata = apply_filters(metadata, filters)

    if not metadata:
        return []

    # -------------------------------
    # ✅ Semantic Search
    # -------------------------------
    query_embedding = get_embedding(query)

    D, I = index.search(np.array([query_embedding]), top_k)

    semantic_results = []
    for i, idx in enumerate(I[0]):
        if idx < len(metadata):
            doc = metadata[idx]
            doc["semantic_score"] = float(D[0][i])
            semantic_results.append(doc)

    # -------------------------------
    # ✅ BM25 Search
    # -------------------------------
    bm25_results = bm25_search(query, metadata, tenant_id, top_k=top_k)

    # -------------------------------
    # ✅ Merge (union)
    # -------------------------------
    combined = {}

    for doc in semantic_results + bm25_results:
        key = doc["text"]

        if key not in combined:
            combined[key] = doc
        else:
            # merge scores
            combined[key]["semantic_score"] = max(
                combined[key].get("semantic_score", 0),
                doc.get("semantic_score", 0)
            )
            combined[key]["bm25_score"] = max(
                combined[key].get("bm25_score", 0),
                doc.get("bm25_score", 0)
            )

    results = list(combined.values())

    # -------------------------------
    # ✅ Normalize scores
    # -------------------------------
    results = normalize_scores(results, "semantic_score")
    results = normalize_scores(results, "bm25_score")

    # -------------------------------
    # ✅ Weighted scoring
    # -------------------------------
    results = combine_scores(results, alpha=0.6, beta=0.4)

    # -------------------------------
    # ✅ Sort by final score
    # -------------------------------
    results = sorted(results, key=lambda x: x["final_score"], reverse=True)

    return results[:top_k]