import os
import uuid

from app.graphs.runner import GraphRunner
from app.github.clone import (
    clone_repository,
    checkout_branch,
)
from app.github.repository import get_pr_context
from app.github.utils import extract_owner_repo
from app.github.markdown_format import format_summary_comment
from app.github.comments import post_pr_comment
from app.rag.ingest import ingest_repository
from app.database.history import save_review
import re
from fastapi import HTTPException


class ReviewService:

    def __init__(self):
        self.graph = GraphRunner()

    def review_repository(
    self,
    repo_path: str,
    owner: str = "",
    repo_name: str = "",
    pr_number: int | None = None,
    changed_files: list | None = None,
    source: str = "manual"
):

        review_id = str(uuid.uuid4())
        print("\n========================================")
        print("Building Repository RAG...")
        print("========================================")

        ingest_repository(repo_path)

        print("Repository RAG Ready!\n")

        state = self.graph.run(
    repo_path=repo_path,
    review_id=review_id,
    owner=owner,
    repo_name=repo_name,
    pr_number=pr_number,
    changed_files=changed_files,
    source=source,
)

        return {
            "success": True,
            "review_id": review_id,
            "status": "WAITING_FOR_REVIEW",
            "total_findings": len(state["findings"]),
            "score": state["score"],
            "grade": state["grade"],
            "risk": state["risk"],
            "summary": state["summary"],
            "report_path": None,
        }

    def review_decision(
    self,
    review_id: str,
    approved: bool,
    feedback: str = "",
    action: str = "approve",
):

        state = self.graph.resume(
            review_id=review_id,
            approved=approved,
            feedback=feedback,
            action=action,
        )

        if "__interrupt__" in state:
            return {
                "success": True,
                "review_id": review_id,
                "status": "WAITING_FOR_REVIEW",
                "total_findings": len(state["findings"]),
                "score": state["score"],
                "grade": state["grade"],
                "risk": state["risk"],
                "summary": state["summary"],
                "report_path": None,
            }
        print(f"[Decision] pr_number in state: {state.get('pr_number')}")
        print(f"[Decision] owner: {state.get('owner')} repo: {state.get('repo_name')}")

        if state.get("pr_number"):
            try:
                comment = format_summary_comment(state)
                post_pr_comment(
                    owner=state["owner"],
                    repo_name=state["repo_name"],
                    pr_number=state["pr_number"],
                    body=comment,
                )
                print(f"[Decision] ✅ Comment posted on PR #{state['pr_number']}")
            except Exception as exc:
                print(f"[Decision] ❌ Failed to post PR comment: {exc}")
        else:
            print("[Decision] No pr_number in state — skipping comment")

        # Persist review to history DB for dashboard
        try:
            save_review(state)
        except Exception as exc:  # noqa: BLE001
            print(f"[ReviewService] Failed to save review history: {exc}")

        return {
            "success": True,
            "review_id": review_id,
            "status": "COMPLETED",
            "total_findings": len(state["findings"]),
            "score": state["score"],
            "grade": state["grade"],
            "risk": state["risk"],
            "summary": state["summary"],
            "report_path": state["report_path"],
        }
    def review_github_repository(self, repo_url: str):
        if not re.match(r'^https?://github\.com/[\w.-]+/[\w.-]+(?:\.git)?$', repo_url):
            raise HTTPException(status_code=400, detail="Invalid GitHub repository URL")

        owner, repo_name = extract_owner_repo(repo_url)

        clone_path = os.path.join(
            "temp",
            f"{repo_name}_{uuid.uuid4().hex[:8]}",
        )

        repo = clone_repository(
            repo_url,
            clone_path,
        )

        repo.close()

        return self.review_repository(
            repo_path=clone_path,
            owner=owner,
            repo_name=repo_name,
            source="manual"
        )

    def review_pull_request(
        self,
        repo_url: str,
        pr_number: int,
        source: str = "manual"
    ):
        if not re.match(r'^https?://github\.com/[\w.-]+/[\w.-]+(?:\.git)?$', repo_url):
            raise HTTPException(status_code=400, detail="Invalid GitHub repository URL")

        owner, repo_name = extract_owner_repo(repo_url)

        pr = get_pr_context(
            owner,
            repo_name,
            pr_number,
        )

        clone_path = os.path.join(
            "temp",
            f"{repo_name}_{uuid.uuid4().hex[:8]}",
        )

        repo = clone_repository(
            repo_url,
            clone_path,
        )

        checkout_branch(
            repo,
            pr["head_branch"],
        )

        repo.close()

        return self.review_repository(
    repo_path=clone_path,
    owner=owner,
    repo_name=repo_name,
    pr_number=pr_number,
    changed_files=pr["changed_files"],
    source=source,
)