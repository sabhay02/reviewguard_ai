from langchain_text_splitters import RecursiveCharacterTextSplitter

from app.rag.loader import DocumentLoader
from app.rag.vectorstore import (
    get_knowledge_db,
    get_repository_db,
)


def ingest_knowledge():

    loader = DocumentLoader()

    knowledge_docs = loader.load_knowledge_docs()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100,
    )

    knowledge_chunks = splitter.split_documents(
        knowledge_docs
    )

    knowledge_db = get_knowledge_db()

    existing = knowledge_db.get()

    if existing["ids"]:
        knowledge_db.delete(ids=existing["ids"])

    if knowledge_chunks:
        knowledge_db.add_documents(knowledge_chunks)


def ingest_repository(repo_path: str):

    loader = DocumentLoader()

    repository_docs = loader.load_repository_docs(
        repo_path
    )

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100,
    )

    repository_chunks = splitter.split_documents(
        repository_docs
    )
    repository_db = get_repository_db()

    # Remove all existing documents instead of resetting the collection
    existing = repository_db.get()

    if existing["ids"]:
        repository_db.delete(ids=existing["ids"])

    if repository_chunks:
        repository_db.add_documents(repository_chunks)

    print(f"Repository chunks indexed: {len(repository_chunks)}")