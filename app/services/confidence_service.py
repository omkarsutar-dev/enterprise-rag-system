def calculate_confidence(chunks):

    if not chunks:
        return 0.0
    
    confidence = sum(c["final_score"] for c in chunks[:3]) / 3

    return confidence


def is_confident(confidence, threshold=0.3):   # 🔥 reduce threshold
    return confidence >= threshold