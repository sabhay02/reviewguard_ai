"""
ReviewGuard AI — Approve a pending webhook review.

Usage:
    uv run python approve_review.py
"""
import httpx

BASE = "http://127.0.0.1:8000"
HEADERS = {"X-API-Key": "dev-secret-key"}

# 1. Fetch pending reviews
print("Fetching pending reviews...\n")
r = httpx.get(f"{BASE}/dashboard/pending", headers=HEADERS)
pending = r.json()

if not pending:
    print("No pending reviews found!")
    raise SystemExit(0)

for i, rev in enumerate(pending):
    print(f"  [{i}] Review ID : {rev['review_id']}")
    print(f"      Repo     : {rev.get('owner')}/{rev.get('repo_name')}")
    print(f"      PR #     : {rev.get('pr_number')}")
    print(f"      Score    : {rev.get('score')}  Grade: {rev.get('grade')}  Risk: {rev.get('risk')}")
    print(f"      Findings : {rev.get('findings')}")
    print()

# 2. Approve the first one (or pick by index)
choice = input(f"Approve which review? [0-{len(pending)-1}] (default 0): ").strip()
idx = int(choice) if choice else 0
review_id = pending[idx]["review_id"]

print(f"\nApproving review {review_id} ...")
r = httpx.post(
    f"{BASE}/review/{review_id}/decision",
    headers=HEADERS,
    json={"approved": True, "feedback": "", "action": "approve"},
)
print(f"Status: {r.status_code}")
print(r.json())
