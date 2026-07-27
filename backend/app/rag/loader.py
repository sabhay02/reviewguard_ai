from pathlib import Path
from langchain_community.document_loaders import TextLoader

DOC_FILES = {
    "readme.md",
    "README.md",
    "CONTRIBUTING.md",
    "ARCHITECTURE.md",
    "architecture.md",
    "STYLE.md",
    "style.md",
    "coding_guidelines.md",
    "CODE_OF_CONDUCT.md",
}

SUPPORTED_EXTENSIONS = {
    ".md",
    ".txt",
}


class DocumentLoader:

    def __init__(self, knowledge_path="knowledge"):
        self.knowledge_path = Path(knowledge_path)
        print("Knowledge path:", self.knowledge_path.resolve())
        print("Exists:", self.knowledge_path.exists())

    def load_repository_docs(self, repo_path: str):
        docs = []

        repo = Path(repo_path)

        if not repo.exists():
            return docs

        for file in repo.rglob("*"):

            if (
                file.name in DOC_FILES
                or "docs" in file.parts
            ) and file.suffix.lower() in SUPPORTED_EXTENSIONS:

                try:
                    loader = TextLoader(str(file), encoding="utf-8")
                    loaded = loader.load()

                    for doc in loaded:
                        doc.metadata["source"] = str(file)
                        doc.metadata["type"] = "repository"

                    docs.extend(loaded)

                except Exception as e:
                    print(f"Failed to load {file}: {e}")

        return docs

    def load_knowledge_docs(self):
        docs = []

        if not self.knowledge_path.exists():
            return docs

        for file in self.knowledge_path.rglob("*.md"):

            try:
                loader = TextLoader(str(file), encoding="utf-8")
                loaded = loader.load()

                for doc in loaded:
                    doc.metadata["source"] = str(file)
                    doc.metadata["type"] = "knowledge"

                docs.extend(loaded)

            except Exception as e:
                print(f"Failed to load {file}: {e}")

        return docs

    def load_all(self, repo_path: str):

        repo_docs = self.load_repository_docs(repo_path)
        knowledge_docs = self.load_knowledge_docs()

        return repo_docs + knowledge_docs