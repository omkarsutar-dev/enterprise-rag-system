from sentence_transformers import CrossEncoder
import numpy as np

model = CrossEncoder(
    "cross-encoder/ms-marco-MiniLM-L-6-v2"
)


def normalize(scores):

    min_score = min(scores)
    max_score = max(scores)

    if max_score == min_score:
        return [1.0] * len(scores)

    return [
        (s - min_score) / (max_score - min_score)
        for s in scores
    ]


def rerank(query, chunks, top_k=5, threshold=0.3):

    if not chunks:
        return []

    # Query-doc pairs
    pairs = [
        (query, chunk["text"])
        for chunk in chunks
    ]

    # Raw logits
    raw_scores = model.predict(pairs)

    # ✅ Normalize rerank scores
    normalized_scores = normalize(raw_scores)

    # Attach scores
    for chunk, rerank_score in zip(chunks, normalized_scores):

        chunk["rerank_score"] = float(rerank_score)

        # ✅ Balanced scoring
        chunk["combined_score"] = (
            0.4 * chunk.get("final_score", 0)
            +
            0.6 * chunk["rerank_score"]
        )

    # Sort
    ranked = sorted(
        chunks,
        key=lambda x: x["combined_score"],
        reverse=True
    )

    # Threshold
    filtered = [
        c for c in ranked
        if c["combined_score"] >= threshold
    ]

    # Fallback
    if not filtered:
        return ranked[:top_k]

    return filtered[:top_k]