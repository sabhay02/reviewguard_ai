from git import Repo
import os
import shutil


def clone_repository(repo_url: str, clone_path: str):

    if os.path.exists(clone_path):
        try:
            repo = Repo(clone_path)
            repo.git.fetch("--all")
            return repo
        except Exception:
            shutil.rmtree(clone_path, ignore_errors=True)

    return Repo.clone_from(repo_url, clone_path)


def checkout_branch(repo: Repo, branch_name: str):

    repo.git.fetch()

    repo.git.checkout(branch_name)