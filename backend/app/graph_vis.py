import uuid
from pprint import pprint

from app.graphs.runner import GraphRunner


def main():
    runner = GraphRunner()

    review_id = str(uuid.uuid4())

    print(f"Review ID : {review_id}")

    result = runner.run(
        repo_path="temp/reviewguard-demo_fb494407",   # Change to your repo
        review_id=review_id,
    )

    print("\nReturned from graph:\n")
    pprint(result)


if __name__ == "__main__":
    main()