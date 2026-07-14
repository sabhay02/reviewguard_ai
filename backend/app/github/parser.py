def extract_pr_info(payload):

    return {
        "repository": payload["repository"]["name"],
        "owner": payload["repository"]["owner"]["login"],
        "pr_number": payload["pull_request"]["number"],
        "title": payload["pull_request"]["title"],
        "base_branch": payload["pull_request"]["base"]["ref"],
        "head_branch": payload["pull_request"]["head"]["ref"],
        "author": payload["sender"]["login"]
    }