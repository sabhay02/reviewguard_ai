from app.security.bandit import run_bandit
from app.security.semgrep import run_semgrep
from app.security.parse_sem import parse_semgrep
from app.security.parser import parse_bandit
from app.llm.explainer import SecurityExplainer
from app.security.gitleaks_parser import parse_gitleaks
from app.security.gitleaks_runner import run_gitleaks
from app.agents.base_agent import BaseAgent
from app.utils.filter import get_source_files
import os 
class SecurityAgent(BaseAgent):

    def __init__(self):
         super().__init__("Security Agent")
         self.explainer = SecurityExplainer()

    def analyze(self, repo_path: str,changed_files: list | None = None):
        paths = get_source_files(
    repo_path,
    changed_files,
)
        print("Security scanning:", paths)
        findings = []

        # Bandit
        # Bandit (Python only or directories)
        py_paths = [p for p in paths if p.endswith(".py") or os.path.isdir(p)]
        if py_paths:
            for output in run_bandit(py_paths):
                 findings.extend(
                    parse_bandit(output)
            )

        # Semgrep
        findings.extend(
            parse_semgrep(
                run_semgrep(paths)
            )
        )

        # Gitleaks
        findings.extend(
            parse_gitleaks(
                run_gitleaks(repo_path)
            )
        )

        enhanced = []

        for finding in findings:
            finding.agent = "Security"
            enhanced.append(
                self.explainer.explain(finding)
            )

        return enhanced