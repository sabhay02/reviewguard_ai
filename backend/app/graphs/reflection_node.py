from app.graphs.state import ReviewState
from app.llm.groq import LLMClient
from app.utils.timer import measure

llm = LLMClient()


@measure("Reflection")
def reflection_node(state: ReviewState):
    prompt = f"""
You are a senior software reviewer.

The reviewer rejected the generated report.

Executive Summary:
{state["summary"]}

Reviewer Feedback:
{state["reviewer_feedback"]}

Rewrite the executive summary by incorporating the reviewer's feedback.

Return only the improved summary.
"""
    print(">>> ENTERED REFLECTION NODE <<<")
    print("Approved:", state["human_approved"])
    print("Feedback:", state["reviewer_feedback"])

    improved_summary = llm.generate(prompt)

    return {
        "summary": improved_summary.strip(),
    }