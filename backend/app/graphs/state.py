from typing import Annotated
from typing_extensions import TypedDict
from operator import add

from app.models.finding import Finding


class ReviewState(TypedDict):
    
    repo_path: str
    review_id: str

    findings: Annotated[list[Finding], add]

    stats: dict

    score: int
    grade: str
    risk: str

    summary: str

    human_approved: bool
    reviewer_feedback: str
    action: str

    enabled_agents: list[str]
    project_type: str

    report_path: str
    owner: str
    repo_name: str
    pr_number: int | None
    changed_files: list[dict]
    source: str