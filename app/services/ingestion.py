import os
from app.config import DATA_PATH
from app.utils.chunking import chunk_text

def load_documents():
    documents = []

    for filename in os.listdir(DATA_PATH):
        if filename.endswith(".txt"):
            with open(os.path.join(DATA_PATH, filename), "r", encoding="utf-8") as f:
                text = f.read()
                chunks = chunk_text(text)
                for chunk in chunks:
                    documents.append({
                        "text": chunk,
                        "source": filename
                    })

    return documents