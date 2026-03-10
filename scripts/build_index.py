from app.services.ingestion import load_documents
from app.services.embeddings import get_embedding
from app.services.vector_store import create_index, save_index

# tenant_id = "company_a"
tenant_id = input("Enter Tenant ID : ")

documents = load_documents(tenant_id)

embeddings = []
metadata = []

for doc in documents:

    embedding = get_embedding(doc["text"])
    embeddings.append(embedding)
    metadata.append(doc)

index = create_index(embeddings)

save_index(index, metadata, tenant_id)

print("Index built successfully")