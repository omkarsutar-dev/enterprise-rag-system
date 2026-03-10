import os
import uuid

from app.config import DATA_PATH
from app.utils.chunking import chunk_text


def load_documents(tenant_id):

    tenant_path = os.path.join(DATA_PATH, tenant_id)

    documents = []

    for filename in os.listdir(tenant_path):

        if filename.endswith(".txt"):

            with open(os.path.join(tenant_path, filename), "r", encoding="utf-8") as f:

                text = f.read()
                chunks = chunk_text(text)
                document_id = str(uuid.uuid4())

                for i, chunk in enumerate(chunks):
                    documents.append({
                        "tenant_id": tenant_id,
                        "document_id": document_id,
                        "chunk_id": f"{document_id}_{i}",
                        "text": chunk,
                        "source": filename
                    })

    return documents