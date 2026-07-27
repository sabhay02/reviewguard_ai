from app.rag.loader import DocumentLoader

loader = DocumentLoader()

docs = loader.load_all("temp/reviewguard-demo_1f8f7c87")

print(f"Loaded {len(docs)} documents")

for doc in docs:
    print(doc.metadata)