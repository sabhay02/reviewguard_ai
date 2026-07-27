from app.llm.groq import LLMClient
from app.llm.prompts import EXECUTIVE_SUMMARY_PROMPT
from app.models.finding import Finding


class ExecutiveSummaryGenerator:

    def __init__(self):
        self.llm = LLMClient()

    def generate(
        self,
        findings: list[Finding],
        score: dict,
    ) -> str:

        critical = sum(f.severity.upper() == "CRITICAL" for f in findings)
        high = sum(f.severity.upper() == "HIGH" for f in findings)
        medium = sum(f.severity.upper() == "MEDIUM" for f in findings)
        low = sum(f.severity.upper() == "LOW" for f in findings)

        issues = "\n".join(
            f"- {finding.rule}: {finding.message}"
            for finding in findings
        )

        prompt = EXECUTIVE_SUMMARY_PROMPT.format(
            total=len(findings),
            critical=critical,
            high=high,
            medium=medium,
            low=low,
            score=score["score"],
            risk=score["risk"],
            issues=issues,
        )

        return self.llm.generate(prompt)