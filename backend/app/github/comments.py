from app.github.client import github_client


def post_pr_comment(
    owner: str,
    repo_name: str,
    pr_number: int,
    body: str,
):
    repository = github_client.get_repo(f"{owner}/{repo_name}")

    pr = repository.get_pull(pr_number)

    pr.create_issue_comment(body)