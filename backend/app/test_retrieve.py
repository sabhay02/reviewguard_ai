from app.rag.retrieve import QualityRetriever

retriever = QualityRetriever()

results = retriever.retrieve(
    "Missing docstring"
)

for r in results:
    print("=" * 50)
    print("Source :", r["source"])
    print("Type   :", r["type"])
    print("Content:")
    print(r["content"][:200])