from app.rag.vectorstore import (
    get_knowledge_db,
    get_repository_db,
)


class QualityRetriever:

    def retrieve(self, query: str):

        repository_db = get_repository_db()
        knowledge_db = get_knowledge_db()
        print("Retriever collection:", repository_db._collection.name)
        print("Retriever count:", repository_db._collection.count())

        repo_docs = repository_db.similarity_search(
            query=query,
            k=2,
        )

        knowledge_docs = knowledge_db.similarity_search(
            query=query,
            k=2,
        )

        docs = repo_docs + knowledge_docs

        context = []

        for doc in docs:
            context.append(
                {
                    "source": doc.metadata.get("source", ""),
                    "type": doc.metadata.get("type", ""),
                    "content": doc.page_content,
                }
            )

        return context