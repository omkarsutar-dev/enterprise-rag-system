def is_relevant(retrieved_text, relevant_docs):

    retrieved_text = retrieved_text.lower()

    for rel in relevant_docs:
        if rel.lower() in retrieved_text:
            return True

    return False


def precision_at_k(retrieved, relevant, k=3):

    retrieved_k = retrieved[:k]

    hits = sum(1 for doc in retrieved_k if is_relevant(doc, relevant))

    return hits / len(retrieved_k) if retrieved_k else 0


def recall_at_k(retrieved, relevant, k=3):

    retrieved_k = retrieved[:k]

    hits = sum(1 for doc in retrieved_k if is_relevant(doc, relevant))

    return hits / len(relevant) if relevant else 0

def exact_match(predicted, expected):

    return int(
        predicted.strip().lower() == expected.strip().lower()
    )