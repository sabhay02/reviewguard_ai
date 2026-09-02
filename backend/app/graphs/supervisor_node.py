from pathlib import Path

from app.graphs.state import ReviewState
from app.utils.timer import measure


@measure("Supervisor")
def supervisor_node(state: ReviewState):
    repo = Path(state["repo_path"])

    # All 4 agents are now multi-language, so always enable all of them
    enabled_agents = ["security", "quality", "documentation", "testgap"]

    # Detect project type for reporting purposes
    has_python = any(repo.rglob("*.py"))
    has_js = any(repo.rglob("*.js")) or any(repo.rglob("*.ts"))
    has_package_json = (repo / "package.json").exists()
    has_java = any(repo.rglob("*.java"))
    has_go = any(repo.rglob("*.go"))
    has_rust = any(repo.rglob("*.rs"))

    # Determine project type label
    detected = []
    if has_python:
        detected.append("python")
    if has_js or has_package_json:
        detected.append("javascript")
    if has_java:
        detected.append("java")
    if has_go:
        detected.append("go")
    if has_rust:
        detected.append("rust")

    project_type = "+".join(detected) if detected else "unknown"

    print("\n========== SUPERVISOR ==========")
    print("Project Type :", project_type)
    print("Enabled Agents :", enabled_agents)
    print("================================\n")

    return {
        "enabled_agents": enabled_agents,
        "project_type": project_type,
    }