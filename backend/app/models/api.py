from pydantic import BaseModel

class GithubReviewRequest(BaseModel):
    repo_url: str

class ReviewRequest(BaseModel):
    repo_path: str

class PullRequestReviewRequest(BaseModel):
    repo_url: str
    pr_number: int

class ReviewResponse(BaseModel):
    success: bool
    review_id: str
    status: str

    total_findings: int

    score: int
    grade: str
    risk: str

    summary: str

    report_path: str | None = None

class ReviewDecisionRequest(BaseModel):
    approved: bool
    feedback: str = ""
    action: str = "approve"