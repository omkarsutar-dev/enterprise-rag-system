# def calculate_confidence(chunks):

#     if not chunks:
#         return 0.0
    
#     confidence = sum(c["final_score"] for c in chunks[:3]) / 3

#     return confidence

def calculate_confidence(chunks):

    if not chunks:
        return 0.0

    avg_score = sum(c.get("final_score", 0) for c in chunks) / len(chunks)

    return avg_score

def is_confident(confidence, threshold=0.3):   # 🔥 reduce threshold
    return confidence >= threshold