import numpy as np
from app.services.embeddings import get_embedding
from app.services.vector_store import load_index
from app.services.bm25_service import bm25_search


def apply_filters(metadata, filters):

    if not filters:
        return metadata  # ✅ skip filtering completely

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
    print(f"Metadata chunks{len(metadata)}")

    # ✅ Apply filters BEFORE retrieval
    if filters:
        metadata = apply_filters(metadata, filters)
    
    print(f"Filters : {filters}")

    if not metadata:
        return []

    for i in metadata :
        print(f"Filterted chunks{metadata}")


    query_embedding = get_embedding(query)

    D, I = index.search(np.array([query_embedding]), top_k)

    semantic_results = []
    for idx in I[0]:
        if idx < len(metadata):
            doc = metadata[idx]
            doc["semantic_score"] = float(D[0][list(I[0]).index(idx)])
            semantic_results.append(doc)


    bm25_results = bm25_search(query, metadata, tenant_id, top_k=top_k)

    combined = semantic_results + bm25_results

    # Deduplicate (keep best version)
    unique = {}
    for doc in combined:
        key = doc["text"]

        if key not in unique:
            unique[key] = doc
        else:
            # keep higher score version
            existing = unique[key]

            new_score = doc.get("bm25_score", 0) + doc.get("semantic_score", 0)
            old_score = existing.get("bm25_score", 0) + existing.get("semantic_score", 0)

            if new_score > old_score:
                unique[key] = doc

    results = list(unique.values())

    return results[:top_k]