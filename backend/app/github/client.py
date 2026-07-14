from github import Github
from app.utils.configs import settings


github_client = Github(settings.github_token)