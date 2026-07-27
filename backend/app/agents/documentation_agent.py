from app.agents.base_agent import BaseAgent

from app.documentation.scanner import DocumentationScanner
from app.documentation.parser import parse_documentation
from app.documentation.explainer import DocumentationExplainer


class DocumentationAgent(BaseAgent):

    def __init__(self):
        super().__init__("Documentation Agent")
        self.explainer = DocumentationExplainer()

    def analyze(
        self,
        repo_path: str,
        changed_files: list | None = None,
    ):
        scanner = DocumentationScanner()

        raw_output = scanner.scan(
            repo_path,
            changed_files,
        )

        findings = parse_documentation(raw_output)

        enhanced = []

        for finding in findings:
            finding.agent = "Documentation"
            explained = self.explainer.explain(finding)
            enhanced.append(explained)

        return enhanced