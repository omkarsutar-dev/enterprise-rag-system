from rank_bm25 import BM25Okapi
import pickle
import os

bm25_store = {}
tokenized_corpus_store = {}


def tokenize(text):
    return text.lower().split()


def build_bm25_index(chunks, tenant_id):

    corpus = [chunk["text"] for chunk in chunks]
    tokenized_corpus = [tokenize(doc) for doc in corpus]

    bm25 = BM25Okapi(tokenized_corpus)

    bm25_store[tenant_id] = bm25
    tokenized_corpus_store[tenant_id] = tokenized_corpus

    # Persist
    with open(f"bm25_{tenant_id}.pkl", "wb") as f:
        pickle.dump((bm25, tokenized_corpus), f)


def load_bm25_index(tenant_id):

    if tenant_id in bm25_store:
        return bm25_store[tenant_id]

    path = f"bm25_{tenant_id}.pkl"

    if os.path.exists(path):
        with open(path, "rb") as f:
            bm25, tokenized_corpus = pickle.load(f)

            bm25_store[tenant_id] = bm25
            tokenized_corpus_store[tenant_id] = tokenized_corpus

            return bm25

    return None


def bm25_search(query, chunks, tenant_id, top_k=10):

    bm25 = load_bm25_index(tenant_id)
    if not bm25:
        return []

    tokenized_query = tokenize(query)

    scores = bm25.get_scores(tokenized_query)

    results = []
    for i, score in enumerate(scores):
        chunk = chunks[i]
        chunk["bm25_score"] = float(score)
        results.append(chunk)

    results = sorted(results, key=lambda x: x["bm25_score"], reverse=True)

    return results[:top_k]