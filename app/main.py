from fastapi import FastAPI
from app.api.routes import router

app = FastAPI(title="Enterprise RAG")

app.include_router(router)