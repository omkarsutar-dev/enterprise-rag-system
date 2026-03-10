import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from app.services.embeddings import get_embedding
from app.services.vector_store import load_index

index, metadata = load_index()

vectorizer = None
tfidf_matrix = None

def initialize_keyword_search():
    global vectorizer, tfidf_matrix
    texts = [doc["text"] for doc in metadata]
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(texts)

initialize_keyword_search()

def hybrid_search(query, top_k=5):
    # Semantic search
    query_embedding = get_embedding(query)
    D, I = index.search(np.array([query_embedding]), top_k)

    semantic_results = [metadata[i] for i in I[0]]

    # Keyword search
    query_vec = vectorizer.transform([query])
    scores = (tfidf_matrix @ query_vec.T).toarray().flatten()
    keyword_indices = scores.argsort()[-top_k:][::-1]
    keyword_results = [metadata[i] for i in keyword_indices]

    # Merge results
    combined = semantic_results + keyword_results

    # Remove duplicates
    unique = {item["text"]: item for item in combined}

    return list(unique.values())[:top_k]