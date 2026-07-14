from git import Repo
from typing import List, Dict


def get_changed_files(
    repo: Repo,
    base_branch: str,
    head_branch: str,
) -> List[str]:
    """
    Returns all files changed between two branches.

    Example:
    [
        "app.py",
        "auth/login.py"
    ]
    """

    changed_files = repo.git.diff(
        f"{base_branch}..{head_branch}",
        "--name-only"
    )

    return changed_files.splitlines()


def get_diff_patch(
    repo: Repo,
    base_branch: str,
    head_branch: str,
) -> str:
    """
    Returns the complete git patch between two branches.
    """

    return repo.git.diff(
        f"{base_branch}..{head_branch}"
    )


def get_changed_python_files(
    repo: Repo,
    base_branch: str,
    head_branch: str,
) -> List[str]:
    """
    Returns only Python files.
    """

    files = get_changed_files(
        repo,
        base_branch,
        head_branch
    )

    return [
        file
        for file in files
        if file.endswith(".py")
    ]


def get_changed_javascript_files(
    repo: Repo,
    base_branch: str,
    head_branch: str,
) -> List[str]:
    """
    Returns JS/TS files.
    """

    files = get_changed_files(
        repo,
        base_branch,
        head_branch
    )

    extensions = (
        ".js",
        ".jsx",
        ".ts",
        ".tsx"
    )

    return [
        file
        for file in files
        if file.endswith(extensions)
    ]


def get_file_patch(
    repo: Repo,
    base_branch: str,
    head_branch: str,
    file_path: str,
) -> str:
    """
    Returns patch of a single file.
    """

    return repo.git.diff(
        f"{base_branch}..{head_branch}",
        "--",
        file_path,
    )


def get_diff_summary(
    repo: Repo,
    base_branch: str,
    head_branch: str,
) -> Dict:
    """
    Returns everything required by AI agents.
    """

    changed_files = get_changed_files(
        repo,
        base_branch,
        head_branch
    )

    patch = get_diff_patch(
        repo,
        base_branch,
        head_branch
    )

    return {
        "changed_files": changed_files,
        "patch": patch,
        "total_files": len(changed_files)
    }