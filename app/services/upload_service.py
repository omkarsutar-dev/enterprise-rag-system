import os
import uuid
import numpy as np

from app.utils.file_parser import extract_text
from app.services.chunking_service import chunk_text   # ✅ UPDATED
from app.services.embeddings import get_embedding
from app.services.vector_store import load_index, save_index, create_index
from app.core.tenant_manager import get_index_path

# ✅ NEW
from app.services.bm25_service import build_bm25_index


def process_upload(file_path, tenant_id, department):

    text = extract_text(file_path)

    # ✅ Improved chunking
    raw_chunks = chunk_text(text)

    embeddings = []
    metadata = []

    for chunk in raw_chunks:

        embedding = get_embedding(chunk)

        embeddings.append(embedding)

        metadata.append({
            "tenant_id": tenant_id,
            "chunk_id": str(uuid.uuid4()),
            "text": chunk,
            "source": os.path.basename(file_path),
            "department": department
        })

    embeddings = np.array(embeddings).astype("float32")

    # -------------------------------
    # ✅ FAISS (existing logic)
    # -------------------------------
    if os.path.exists(get_index_path(tenant_id)):

        index, existing_metadata = load_index(tenant_id)

        index.add(embeddings)

        existing_metadata.extend(metadata)

        save_index(index, existing_metadata, tenant_id)

        # 🔥 IMPORTANT: rebuild BM25 with full corpus
        all_chunks = [m["text"] for m in existing_metadata]

    else:

        index = create_index(embeddings)

        save_index(index, metadata, tenant_id)

        all_chunks = [m["text"] for m in metadata]

    # -------------------------------
    # ✅ BM25 Index (NEW)
    # -------------------------------
    bm25_chunks = [{"text": c} for c in all_chunks]

    build_bm25_index(bm25_chunks, tenant_id)