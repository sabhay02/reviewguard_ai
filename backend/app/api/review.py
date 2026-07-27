from fastapi import APIRouter

from app.models.api import (
    ReviewRequest,
    ReviewResponse,
    GithubReviewRequest,
    PullRequestReviewRequest
)
from app.services.review_service import ReviewService

router = APIRouter(
    prefix="/review",
    tags=["Review"]
)

service = ReviewService()

from app.models.api import ReviewDecisionRequest


@router.post("/{review_id}/decision", response_model=ReviewResponse)
def review_decision(
    review_id: str,
    request: ReviewDecisionRequest,
):
    result = service.review_decision(
        review_id=review_id,
        approved=request.approved,
        feedback=request.feedback,
        action=request.action,
    )

    return ReviewResponse(**result)

@router.post("/", response_model=ReviewResponse)
def review_repository(request: ReviewRequest):

    result = service.review_repository(request.repo_path)

    return ReviewResponse(**result)

@router.post(
    "/github",
    response_model=ReviewResponse
)
def review_github_repository(
    request: GithubReviewRequest,
):

    return service.review_github_repository(
        request.repo_url
    )

@router.post(
    "/pr",
    response_model=ReviewResponse,
)
def review_pull_request(
    request: PullRequestReviewRequest,
):
    return service.review_pull_request(
        request.repo_url,
        request.pr_number,
    )