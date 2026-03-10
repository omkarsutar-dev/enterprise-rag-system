import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer

from app.services.embeddings import get_embedding
from app.services.vector_store import load_index

vectorizers = {}
tfidf_matrices = {}
indexes = {}
metadatas = {}


def initialize_tenant(tenant_id):
    index, metadata = load_index(tenant_id)
    texts = [doc["text"] for doc in metadata]
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(texts)

    indexes[tenant_id] = index
    metadatas[tenant_id] = metadata
    vectorizers[tenant_id] = vectorizer
    tfidf_matrices[tenant_id] = tfidf_matrix


def hybrid_search(query, tenant_id, top_k=5):

    if tenant_id not in indexes:
        initialize_tenant(tenant_id)

    index = indexes[tenant_id]
    metadata = metadatas[tenant_id]
    vectorizer = vectorizers[tenant_id]
    tfidf_matrix = tfidf_matrices[tenant_id]

    query_embedding = get_embedding(query)

    D, I = index.search(np.array([query_embedding]), top_k)

    semantic_results = [metadata[i] for i in I[0]]

    query_vec = vectorizer.transform([query])

    scores = (tfidf_matrix @ query_vec.T).toarray().flatten()

    keyword_indices = scores.argsort()[-top_k:][::-1]

    keyword_results = [metadata[i] for i in keyword_indices]

    combined = semantic_results + keyword_results

    unique = {item["text"]: item for item in combined}

    return list(unique.values())[:top_k]