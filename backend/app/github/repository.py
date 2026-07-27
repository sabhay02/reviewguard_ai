from app.github.client import github_client


def get_repository(owner: str, repo: str):
    """
    Returns a GitHub repository object.
    """
    return github_client.get_repo(f"{owner}/{repo}")


def get_pull_request(owner: str, repo: str, pr_number: int):
    """
    Returns a pull request object.
    """
    repository = get_repository(owner, repo)

    return repository.get_pull(pr_number)

def get_changed_files(owner: str, repo: str, pr_number: int):
    repository = github_client.get_repo(f"{owner}/{repo}")

    pr = repository.get_pull(pr_number)

    files = []

    for file in pr.get_files():
        files.append({
            "filename": file.filename,
            "status": file.status,
            "additions": file.additions,
            "deletions": file.deletions,
            "changes": file.changes,
        })

    return files

def get_pr_context(owner: str, repo: str, pr_number: int):
    pr = get_pull_request(owner, repo, pr_number)

    return {
        "title": pr.title,
        "author": pr.user.login,
        "base_branch": pr.base.ref,
        "head_branch": pr.head.ref,
        "state": pr.state,
        "url": pr.html_url,
         "changed_files": get_changed_files(owner, repo, pr_number),
        "commits": pr.commits,
    }