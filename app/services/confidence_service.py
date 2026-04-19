def calculate_confidence(chunks):

    if not chunks:
        return 0

    scores = [c.get("score", 0) for c in chunks]

    return sum(scores) / len(scores)


def is_confident(confidence, threshold=0.6):

    return confidence >= threshold