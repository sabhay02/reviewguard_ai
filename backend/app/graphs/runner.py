from app.graphs.workflow import review_graph
from langgraph.types import Command


class GraphRunner:

    def run(
    self,
    repo_path: str,
    review_id: str,
    owner: str = "",
    repo_name: str = "",
    pr_number: int | None = None,
    changed_files: list | None = None,
    source: str = "manual",
):

        initial_state = {
    "repo_path": repo_path,
    "review_id": review_id,
    "owner": owner,
    "repo_name": repo_name,
    "pr_number": pr_number,

    "findings": [],
    "score": None,
    "grade": "",
    "summary": "",
    "report_path": "",
    "changed_files": changed_files or [],
    "source": source,
}
        print("Changed files:", initial_state["changed_files"]) 
        config = {
            "configurable": {
                "thread_id": review_id
            }
        }

        return review_graph.invoke(
            initial_state,
            config=config,
        )

    def resume(
        self,
        review_id: str,
        approved: bool,
        feedback: str = "",
        action: str = "approve",
    ):

        config = {
            "configurable": {
                "thread_id": review_id
            }
        }

        return review_graph.invoke(
            Command(
                resume={
                    "approved": approved,
                    "feedback": feedback,
                    "action": action,
                }
            ),
            config=config,
        )