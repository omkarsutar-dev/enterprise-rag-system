from sentence_transformers import CrossEncoder
cross_encoder = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")


def rerank(query, chunks, top_k=5, threshold=0.2):

    if not chunks:
        return []

    # Assume scores already exist (final_score)

    ranked = sorted(chunks, key=lambda x: x.get("final_score", 0), reverse=True)

    # Filter
    filtered = [c for c in ranked if c.get("final_score", 0) >= threshold]

    # 🔥 CRITICAL: fallback
    if not filtered:
        return ranked[:top_k]

    return filtered[:top_k]