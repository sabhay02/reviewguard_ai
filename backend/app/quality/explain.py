import json

from app.llm.groq import LLMClient
from app.models.finding import AIReview
from app.quality.prompts import QUALITY_PROMPT


class QualityExplainer:

    def __init__(self):
        self.llm = LLMClient()

    def explain(self, finding, context):

        context_text = ""

        if context:
            for item in context:
                context_text += f"""
Source: {item['source']}

{item['content']}

----------------------------------------
"""
        else:
            context_text = "No relevant coding standards were retrieved."

        prompt = QUALITY_PROMPT.format(
            tool=finding.tool,
            rule=finding.rule,
            message=finding.message,
            context=context_text,
        )

        response = self.llm.generate(prompt, json_mode=True)
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
                "title": "Quality Issue",
                "summary": response,
                "impact": "",
                "recommendation": "",
                "secure_code": "",
                "status": "Open",
            }

        finding.review = AIReview(**review)

        return finding