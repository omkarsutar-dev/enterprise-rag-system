def normalize_scores(docs, score_key):

    scores = [doc.get(score_key, 0) for doc in docs]

    if not scores:
        return docs

    min_s = min(scores)
    max_s = max(scores)

    if max_s == min_s:
        for doc in docs:
            doc[f"{score_key}_norm"] = 0.5
        return docs

    for doc in docs:
        doc[f"{score_key}_norm"] = (
            (doc.get(score_key, 0) - min_s) / (max_s - min_s)
        )

    return docs


def combine_scores(docs, alpha=0.6, beta=0.4):

    for doc in docs:
        semantic = doc.get("semantic_score_norm", 0)
        bm25 = doc.get("bm25_score_norm", 0)

        doc["final_score"] = alpha * semantic + beta * bm25

    return docs