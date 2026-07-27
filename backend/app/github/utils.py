from urllib.parse import urlparse


def extract_owner_repo(repo_url: str):
    """
    Extract owner and repository name from a GitHub URL.

    Example:
    https://github.com/sabhay02/reviewguard-demo

    Returns:
    ("sabhay02", "reviewguard-demo")
    """

    parsed = urlparse(repo_url)

    parts = parsed.path.strip("/").split("/")

    if len(parts) < 2:
        raise ValueError("Invalid GitHub repository URL.")

    owner = parts[0]
    repo = parts[1].replace(".git", "")

    return owner, repo