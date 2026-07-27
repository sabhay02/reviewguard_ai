from copy import deepcopy
import json

from app.llm.groq import LLMClient
from app.llm.prompts import SECURITY_REVIEW_PROMPT
from app.models.finding import Finding


class SecurityExplainer:

    def __init__(self):
        self.llm = LLMClient()

    def explain(self, finding: Finding) -> Finding:

        prompt = SECURITY_REVIEW_PROMPT.format(
            tool=finding.tool,
            rule=finding.rule,
            severity=finding.severity,
            file=finding.file,
            line=finding.line,
            message=finding.message,
        )

        response = self.llm.generate(prompt,json_mode=True)

        enhanced = deepcopy(finding)

        try:
            cleaned = response.strip()

            if cleaned.startswith("```json"):
                cleaned = cleaned[7:]

            if cleaned.startswith("```"):
                cleaned = cleaned[3:]

            if cleaned.endswith("```"):
                cleaned = cleaned[:-3]

            cleaned = cleaned.strip()

            review = json.loads(cleaned)
           

            enhanced.review.title = review.get("title")
            enhanced.review.summary = review.get("summary")
            enhanced.review.impact = review.get("impact")
            enhanced.review.recommendation = review.get("recommendation")
            enhanced.review.secure_code = review.get("secure_code")
            enhanced.review.status = review.get("status")

        except Exception:
            # Fallback if the LLM doesn't return valid JSON
            enhanced.review.summary = response

        return enhanced