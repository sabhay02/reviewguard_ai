from app.github.client import github_client


def get_repository(owner, repo):
    return github_client.get_repo(f"{owner}/{repo}")

repo = get_repository(
    "sabhay02",
    "reviewguard-demo"
)

def get_pull_request(owner, repo, pr_number):

    repository = github_client.get_repo(
        f"{owner}/{repo}"
    )

    return repository.get_pull(pr_number)

pr = get_pull_request(
    "sabhay02",
    "reviewguard-demo",
    1
)

print(pr.title)
print(pr.user.login)
print(pr.base.ref)
print(pr.head.ref)

print(repo.full_name)