from app.services.ingestion import load_documents
from app.services.embeddings import get_embedding
from app.services.vector_store import create_faiss_index, save_index
from app.services.retriever import initialize_keyword_search

documents = load_documents()

embeddings = []
metadata = []

for doc in documents:
    embedding = get_embedding(doc["text"])
    embeddings.append(embedding)
    metadata.append(doc)

index = create_faiss_index(embeddings)
save_index(index, metadata)

initialize_keyword_search(documents)

print("Index built successfully.")