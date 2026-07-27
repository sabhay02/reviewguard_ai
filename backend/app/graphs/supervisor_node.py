from pathlib import Path

from app.graphs.state import ReviewState
from app.utils.timer import measure


@measure("Supervisor")
def supervisor_node(state: ReviewState):
    repo = Path(state["repo_path"])

    enabled_agents = []

    # Detect Python project
    has_python = any(repo.rglob("*.py"))

    # Detect JS/Node project
    has_package_json = (repo / "package.json").exists()

    # Detect tests
    has_tests = (
        any(repo.rglob("test_*.py"))
        or any(repo.rglob("*_test.py"))
        or any(repo.rglob("tests"))
    )

    project_type = "unknown"

    if has_python:
        project_type = "python"

        enabled_agents.extend([
            "security",
            "quality",
            "documentation",
        ])

        if not has_tests:
            enabled_agents.append("testgap")

    elif has_package_json:
        project_type = "javascript"

        enabled_agents.extend([
            "security",
            "quality",
            "documentation",
        ])

        if not has_tests:
            enabled_agents.append("testgap")

    else:
        # Fallback for unknown projects
        enabled_agents.extend([
            "security",
            "quality",
            "documentation",
        ])

    print("\n========== SUPERVISOR ==========")
    print("Project Type :", project_type)
    print("Enabled Agents :", enabled_agents)
    print("================================\n")

    return {
        "enabled_agents": enabled_agents,
        "project_type": project_type,
    }