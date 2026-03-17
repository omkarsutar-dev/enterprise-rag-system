import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer

from app.services.embeddings import get_embedding
from app.services.vector_store import load_index

vectorizer = None
tfidf_matrix = None


def initialize_keyword_search(metadata):

    global vectorizer, tfidf_matrix

    texts = [doc["text"] for doc in metadata]

    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(texts)


def apply_filters(metadata, filters):

    filtered = []

    for doc in metadata:

        match = True

        if filters.get("department") and doc.get("department") != filters["department"]:
            match = False

        if filters.get("source") and doc.get("source") != filters["source"]:
            match = False

        if match:
            filtered.append(doc)

    return filtered


def hybrid_search(query, tenant_id, filters=None, top_k=20):

    index, metadata = load_index(tenant_id)

    # ✅ Apply filters BEFORE retrieval
    if filters:
        metadata = apply_filters(metadata, filters)

    if not metadata:
        return []

    # Reinitialize keyword search
    initialize_keyword_search(metadata)

    # Semantic search
    query_embedding = get_embedding(query)
    D, I = index.search(np.array([query_embedding]), top_k)

    semantic_results = [
        metadata[i] for i in I[0] if i < len(metadata)
    ]

    # Keyword search
    query_vec = vectorizer.transform([query])
    scores = (tfidf_matrix @ query_vec.T).toarray().flatten()

    keyword_indices = scores.argsort()[-top_k:][::-1]
    keyword_results = [metadata[i] for i in keyword_indices]

    # Combine
    combined = semantic_results + keyword_results

    # Remove duplicates
    unique = {item["text"]: item for item in combined}

    return list(unique.values())[:top_k]