from dataclasses import dataclass


@dataclass
class PRContext:
    owner: str
    repository: str
    pr_number: int

    base_branch: str
    head_branch: str

    clone_path: str

    changed_files: list[str]

    patch: str