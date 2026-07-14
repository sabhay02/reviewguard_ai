from app.github.clone import clone_repository, checkout_branch
from app.github.diff import get_diff_summary


def prepare_repository(
    repo_url: str,
    clone_path: str,
    base_branch: str,
    head_branch: str,
):

    repo = clone_repository(
        repo_url,
        clone_path
    )

    checkout_branch(
        repo,
        head_branch
    )

    summary = get_diff_summary(
        repo,
        base_branch,
        head_branch
    )

    return repo, summary