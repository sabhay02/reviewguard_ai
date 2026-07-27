from app.agents.base_agent import BaseAgent

from app.test_gap.detetctor import TestGapDetector
from app.test_gap.explainer import TestGapExplainer
from app.test_gap.parser import TestGapParser


class TestGapAgent(BaseAgent):

    def __init__(self):
        super().__init__("TestGap Agent")
        self.detector = TestGapDetector()
        self.explainer = TestGapExplainer()
        self.parser = TestGapParser()

    def analyze(self, repo_path: str,changed_files: list | None = None,):

        findings = []

        detected = self.detector.detect(repo_path,changed_files)

        for finding in detected:

            review = self.explainer.explain(finding)

            findings.append(
                self.parser.parse(finding, review)
            )

        return findings