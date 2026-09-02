from app.agents.base_agent import BaseAgent
from app.quality.ruff_runner import run_ruff
from app.quality.parser import parse_ruff
from app.quality.explain import QualityExplainer
from app.quality.pylint_runner import run_pylint
from app.quality.pylint_parser import parse_pylint
from app.quality.deduplicate import deduplicate
from app.quality.llm_reviewer import LLMQualityReviewer
from app.utils.filter import get_source_files
from app.rag.retrieve import QualityRetriever
import os


class QualityAgent(BaseAgent):

    def __init__(self):
        super().__init__("Quality Agent")
        self.explainer = QualityExplainer()
        self.retriever = QualityRetriever()
        self.llm_reviewer = LLMQualityReviewer()

    def should_use_rag(self, finding):

        text = f"{finding.rule} {finding.message}".lower()

        keywords = [
            "docstring",
            "documentation",
            "complexity",
            "type hint",
            "naming",
            "design",
            "too many",
            "long function",
            "too many branches",
            "too many arguments",
            "too many locals",
            "duplicate code",
        ]

        return any(keyword in text for keyword in keywords)

    def analyze(self, repo_path: str, changed_files: list | None = None):

        findings = []
        paths = get_source_files(
            repo_path,
            changed_files,
        )
        print("Quality scanning:", paths)

        # Only run Python tools on Python files or directories
        py_paths = [p for p in paths if p.endswith(".py") or os.path.isdir(p)]

        if py_paths:
            # Ruff
            ruff_output = run_ruff(py_paths)
            findings.extend(parse_ruff(ruff_output))

            # Pylint
            pylint_output = run_pylint(py_paths)
            findings.extend(parse_pylint(pylint_output))

        # LLM-based quality review for non-Python files
        non_py_files = []
        for p in paths:
            if os.path.isdir(p):
                for root, _, files in os.walk(p):
                    for fname in files:
                        full = os.path.join(root, fname)
                        if not full.endswith(".py"):
                            ext = os.path.splitext(full)[1].lower()
                            if ext in {".js", ".ts", ".jsx", ".tsx", ".java", ".go", ".rs", ".c", ".cpp", ".cs"}:
                                non_py_files.append(full)
            elif not p.endswith(".py"):
                non_py_files.append(p)

        for file_path in non_py_files:
            findings.extend(self.llm_reviewer.analyze(file_path, repo_path))

        findings = deduplicate(findings)

        enhanced = []

        for finding in findings:

            finding.agent = "Quality"

            query = f"""
        Tool: {finding.tool}
        Rule: {finding.rule}
        Message: {finding.message}
        """

            if self.should_use_rag(finding):
                context = self.retriever.retrieve(query)
            else:
                context = []

            explained = self.explainer.explain(
                finding,
                context,
            )

            enhanced.append(explained)

        return enhanced