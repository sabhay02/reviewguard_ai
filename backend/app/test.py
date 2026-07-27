import time

from app.graphs.workflow import review_graph
from app.utils.timer import execution_times
from app.database.history import initialize_db, save_review

# --------------------------------------------------
# Initialize Database
# --------------------------------------------------
initialize_db()

graph = review_graph

state = {
    # Repository
    "repo_path": "temp/reviewguard-demo_fb494407",

    # Shared state
    "findings": [],

    # Supervisor
    "enabled_agents": [],
    "project_type": "",

    # Statistics
    "stats": {},

    # Risk
    "score": 0,
    "grade": "",
    "risk": "",

    # Executive Summary
    "summary": "",

    # Human Review
    "human_approved": False,
    "reviewer_feedback": "",

    # Report
    "report_path": "",
}

config = {
    "configurable": {
        "thread_id": "review-001"
    }
}

print("\nStarting ReviewGuard AI...\n")

workflow_start = time.perf_counter()

# Keep track of the latest state
latest_state = state.copy()

for event in graph.stream(state, config=config):
    node = next(iter(event))
    print(f"✔ Completed: {node}")

    latest_state.update(event[node])


workflow_end = time.perf_counter()

print("\nReview Finished!\n")

# --------------------------------------------------
# Save Review History
# --------------------------------------------------
save_review(latest_state)

print("Review saved to database.\n")

# --------------------------------------------------
# Execution Metrics
# --------------------------------------------------
print("=" * 60)
print("EXECUTION METRICS")
print("=" * 60)

for node, elapsed in sorted(
    execution_times.items(),
    key=lambda x: x[1],
    reverse=True,
):
    print(f"{node:<20} {elapsed:.3f} s")

print("-" * 60)
print(f"{'Actual Workflow Time':<20} {(workflow_end - workflow_start):.3f} s")
print("=" * 60)