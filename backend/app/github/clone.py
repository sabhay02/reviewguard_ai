from git import Repo
import os
import shutil


def clone_repository(repo_url: str, clone_path: str):

    if os.path.exists(clone_path):
        shutil.rmtree(clone_path)

    repo = Repo.clone_from(repo_url, clone_path)
    repo.close()

    return repo

def checkout_branch(repo: Repo, branch_name: str):

    repo.git.checkout(branch_name)

    print(f"Checked out to {branch_name}")

