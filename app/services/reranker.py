from sentence_transformers import CrossEncoder

# Load model once (global)
cross_encoder = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")


def rerank(query, chunks, top_k=5, threshold=0.3):

    if not chunks:
        return []

    pairs = [(query, c["text"]) for c in chunks]
    scores = cross_encoder.predict(pairs)

    for i, chunk in enumerate(chunks):
        chunk["score"] = float(scores[i])

    ranked = sorted(chunks, key=lambda x: x["score"], reverse=True)

    # Filter
    filtered = [c for c in ranked if c["score"] >= threshold]
    

    # 🔥 IMPORTANT FALLBACK
    if not filtered:
        return ranked[:top_k]   # don't return empty

    return filtered[:top_k]