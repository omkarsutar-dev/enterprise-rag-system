from sentence_transformers import CrossEncoder

# Load reranker model
model = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")


def rerank(query, documents, top_k=5):

    pairs = []

    for doc in documents:
        pairs.append((query, doc["text"]))

    scores = model.predict(pairs)

    scored_docs = list(zip(documents, scores))

    scored_docs.sort(key=lambda x: x[1], reverse=True)

    reranked = [doc for doc, score in scored_docs]

    return reranked[:top_k]