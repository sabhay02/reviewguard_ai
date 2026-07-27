import json

from app.documentation.prompts import DOCUMENTATION_PROMPT
from app.llm.groq import LLMClient
from app.models.finding import AIReview


class DocumentationExplainer:

    def __init__(self):
        self.llm = LLMClient()

    def explain(self, finding):

        prompt = DOCUMENTATION_PROMPT.format(
             tool=finding.tool,
             rule=finding.rule,
             severity=finding.severity,
             message=finding.message,
)

        response = self.llm.generate(
            prompt,
            json_mode=True,
        )

        response = response.strip()

        if response.startswith("```json"):
            response = response.replace("```json", "", 1)

        if response.startswith("```"):
            response = response.replace("```", "", 1)

        if response.endswith("```"):
            response = response[:-3]

        response = response.strip()

        try:
            review = json.loads(response)

        except Exception:

            review = {
                "title": "Documentation Issue",
                "summary": response,
                "impact": "",
                "recommendation": "",
                "secure_code": "",
                "status": "Open",
            }

        finding.review = AIReview(**review)

        return finding