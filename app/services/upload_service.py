import os
import uuid
import numpy as np

from app.utils.file_parser import extract_text
from app.utils.chunking import chunk_text
from app.services.embeddings import get_embedding
from app.services.vector_store import load_index, save_index, create_index
from app.core.tenant_manager import get_index_path


def process_upload(file_path, tenant_id):

    text = extract_text(file_path)

    chunks = chunk_text(text)

    embeddings = []
    metadata = []

    for chunk in chunks:

        embedding = get_embedding(chunk)

        embeddings.append(embedding)

        metadata.append({
            "tenant_id": tenant_id,
            "chunk_id": str(uuid.uuid4()),
            "text": chunk,
            "source": os.path.basename(file_path)
        })

    embeddings = np.array(embeddings).astype("float32")

    #  Check if tenant index exists
    if os.path.exists(get_index_path(tenant_id)):

        index, existing_metadata = load_index(tenant_id)

        index.add(embeddings)

        existing_metadata.extend(metadata)

        save_index(index, existing_metadata, tenant_id)

    else:

        # 🔹 Create new index for first document
        index = create_index(embeddings)

        save_index(index, metadata, tenant_id)