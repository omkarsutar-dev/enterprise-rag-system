import os
from app.config import VECTOR_DB_PATH

def get_index_path(tenant_id):
    return os.path.join(VECTOR_DB_PATH, f"{tenant_id}_index.bin")

def get_metadata_path(tenant_id):
    return os.path.join(VECTOR_DB_PATH, f"{tenant_id}_metadata.pkl")