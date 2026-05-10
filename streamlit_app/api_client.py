import requests

BASE_URL = "http://127.0.0.1:8000"


def upload_document(file, tenant_id, department):

    files = {
        "file": file
    }

    data = {
        "tenant_id": tenant_id,
        "department": department
    }

    response = requests.post(
        f"{BASE_URL}/upload",
        files=files,
        data=data
    )

    return response.json()


def query_rag(payload):

    response = requests.post(
        f"{BASE_URL}/query",
        json=payload,
        stream=True
    )

    return response