import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

EMBEDDING_MODEL = "text-embedding-3-small"
LLM_MODEL = "gpt-4o-mini"

# VECTOR_STORE_PATH = "vector_store/faiss_index.bin"
# METADATA_PATH = "vector_store/metadata.pkl"
# DATA_PATH = "data/raw"

VECTOR_DB_PATH = "vector_store"
DATA_PATH = "data"