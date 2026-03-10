import faiss
import pickle
import numpy as np

from app.core.tenant_manager import get_index_path, get_metadata_path


def create_index(embeddings):
    dim = len(embeddings[0])
    index = faiss.IndexFlatL2(dim)
    index.add(np.array(embeddings))
    return index


def save_index(index, metadata, tenant_id):
    faiss.write_index(index, get_index_path(tenant_id))
    with open(get_metadata_path(tenant_id), "wb") as f:
        pickle.dump(metadata, f)


def load_index(tenant_id):
    index = faiss.read_index(get_index_path(tenant_id))
    with open(get_metadata_path(tenant_id), "rb") as f:
        metadata = pickle.load(f)
    return index, metadata