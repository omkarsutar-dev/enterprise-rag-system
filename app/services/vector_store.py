import faiss
import numpy as np
import pickle
import os
from app.config import VECTOR_STORE_PATH, METADATA_PATH

def create_faiss_index(embeddings):
    dimension = len(embeddings[0])
    index = faiss.IndexFlatL2(dimension)
    index.add(np.array(embeddings))
    return index

def save_index(index, metadata):
    faiss.write_index(index, VECTOR_STORE_PATH)
    with open(METADATA_PATH, "wb") as f:
        pickle.dump(metadata, f)

def load_index():
    if not os.path.exists(VECTOR_STORE_PATH):
        return None, None

    index = faiss.read_index(VECTOR_STORE_PATH)
    with open(METADATA_PATH, "rb") as f:
        metadata = pickle.load(f)

    return index, metadata