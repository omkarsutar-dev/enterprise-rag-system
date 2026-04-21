import requests

BASE_URL = "http://localhost:8000"  # change if deployed


def query_api(payload):
    url = f"{BASE_URL}/query?stream=true"

    response = requests.post(url, json=payload, stream=True)

    for chunk in response.iter_content(chunk_size=1024):
        if chunk:
            yield chunk.decode("utf-8")