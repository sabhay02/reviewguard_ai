from langgraph.graph import StateGraph, START, END

from app.graphs.state import ReviewState
from app.graphs.supervisor_node import supervisor_node
from app.graphs.human_review import human_review_node
from app.graphs.reflection_node import reflection_node
from app.graphs.remediation_node import remediation_node
from app.graphs.check import checkpointer



from app.graphs.nodes import (
    security_node,
    quality_node,
    testgap_node,
    documentation_node,
    statistics_node,
    risk_node,
    summary_node,
    report_node,
)

builder = StateGraph(ReviewState)


def review_decision(state: ReviewState):
    if state.get("action") == "auto_fix":
        return "remediation"
    if state["human_approved"]:
        return "report"
    return "reflection"





# --------------------
# Nodes
# --------------------

builder.add_node("supervisor", supervisor_node)

builder.add_node("security", security_node)
builder.add_node("quality", quality_node)
builder.add_node("testgap", testgap_node)
builder.add_node("documentation", documentation_node)

builder.add_node("statistics", statistics_node)
builder.add_node("risk", risk_node)
builder.add_node("summary", summary_node)

builder.add_node("human_review", human_review_node)
builder.add_node("reflection", reflection_node)
builder.add_node("remediation", remediation_node)

builder.add_node("report", report_node)

# --------------------
# Flow
# --------------------

builder.add_edge(START, "supervisor")

# Parallel execution
builder.add_edge("supervisor", "security")
builder.add_edge("supervisor", "quality")
builder.add_edge("supervisor", "testgap")
builder.add_edge("supervisor", "documentation")

# Merge
builder.add_edge("security", "statistics")
builder.add_edge("quality", "statistics")
builder.add_edge("testgap", "statistics")
builder.add_edge("documentation", "statistics")

builder.add_edge("statistics", "risk")
builder.add_edge("risk", "summary")

builder.add_edge("summary", "human_review")

builder.add_conditional_edges(
    "human_review",
    review_decision,
    {
        "report": "report",
        "reflection": "reflection",
        "remediation": "remediation",
    },
)

builder.add_edge("reflection", "human_review")
builder.add_edge("remediation", "human_review")

builder.add_edge("report", END)


review_graph = builder.compile(
    checkpointer=checkpointer
)
