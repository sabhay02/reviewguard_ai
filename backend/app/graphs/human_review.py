from langgraph.types import interrupt

from app.graphs.state import ReviewState
from app.utils.timer import measure


@measure("Human Review")
def human_review_node(state: ReviewState):
    print("\n>>> ENTERED HUMAN REVIEW <<<")
    print("Current approved:", state.get("human_approved"))
    print("Current feedback:", state.get("reviewer_feedback"))

    decision = interrupt(
        {
            "summary": state["summary"],
            "score": state["score"],
            "grade": state["grade"],
            "risk": state["risk"],
            "findings": len(state["findings"]),
        }
    )

    print(">>> RESUMED HUMAN REVIEW <<<")
    print(decision)

    return {
        "human_approved": decision["approved"],
        "reviewer_feedback": decision.get("feedback", ""),
        "action": decision.get("action", "approve"),
    }