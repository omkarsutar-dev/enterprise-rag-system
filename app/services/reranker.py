from sentence_transformers import CrossEncoder

# Load model once (global)
cross_encoder = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")


def rerank(query, chunks, top_k=3):

    if not chunks:
        return []

    # Create pairs (query, chunk_text)
    pairs = [(query, c["text"]) for c in chunks]

    # Get scores
    scores = cross_encoder.predict(pairs)

    # Attach scores
    for i, chunk in enumerate(chunks):
        chunk["score"] = float(scores[i])

    # Sort by score (descending)
    ranked = sorted(chunks, key=lambda x: x["score"], reverse=True)

    return ranked[:top_k]