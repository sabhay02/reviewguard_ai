from pathlib import Path
from langchain_chroma import Chroma

from app.rag.embeddings import embeddings

BASE_DIR = Path(__file__).resolve().parents[2]
PERSIST_DIR = BASE_DIR / "chroma_db"


def get_knowledge_db():

    return Chroma(
        collection_name="quality_knowledge",
        embedding_function=embeddings,
        persist_directory=str(PERSIST_DIR),
    )


def get_repository_db():

    return Chroma(
        collection_name="repository_docs",
        embedding_function=embeddings,
        persist_directory=str(PERSIST_DIR),
    )