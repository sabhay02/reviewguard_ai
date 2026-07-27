def extract_pr_info(payload):

    owner = payload["repository"]["owner"]["login"]
    repo_name = payload["repository"]["name"]

    return {
        "repository": repo_name,
        "owner": owner,
        "pr_number": payload["pull_request"]["number"],
        "title": payload["pull_request"]["title"],
        "base_branch": payload["pull_request"]["base"]["ref"],
        "head_branch": payload["pull_request"]["head"]["ref"],
        "author": payload["sender"]["login"],
        "repo_url": f"https://github.com/{owner}/{repo_name}",
    }