import json
import os

from app.llm.groq import LLMClient
from app.models.finding import Finding, AIReview


LLM_QUALITY_PROMPT = """
You are an expert Senior Software Engineer performing a code quality review.

Analyze the following source file for code quality issues. Look for:
1. Naming convention violations (variables, functions, classes)
2. Code complexity (deeply nested logic, overly long functions)
3. Code smells (duplicate code, magic numbers, dead code)
4. Anti-patterns specific to the language
5. Missing error handling
6. Performance issues

Source File: {filename}
Language: {language}

```
{code}
```

Return a JSON array of findings. Each finding must have this structure:
{{
    "rule": "Short rule name (e.g. 'Magic Number', 'Deep Nesting')",
    "severity": "LOW" or "MEDIUM" or "HIGH",
    "line": <approximate line number as integer>,
    "message": "Clear explanation of the quality issue"
}}

If there are no quality issues, return an empty array: []
Return ONLY the JSON array, no other text.
"""

LANGUAGE_MAP = {
    ".js": "JavaScript",
    ".ts": "TypeScript",
    ".jsx": "React JSX",
    ".tsx": "React TSX",
    ".java": "Java",
    ".go": "Go",
    ".rs": "Rust",
    ".c": "C",
    ".cpp": "C++",
    ".cs": "C#",
}


class LLMQualityReviewer:

    def __init__(self):
        self.llm = LLMClient()

    def analyze(self, file_path: str, repo_path: str) -> list[Finding]:
        """Analyze a non-Python source file for quality issues using the LLM."""

        ext = os.path.splitext(file_path)[1].lower()
        language = LANGUAGE_MAP.get(ext, "Unknown")

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                code = f.read()
        except Exception:
            return []

        # Skip very large files to avoid token limits
        if len(code) > 15000:
            code = code[:15000] + "\n... [File Truncated] ..."

        relative_path = os.path.relpath(file_path, repo_path)

        prompt = LLM_QUALITY_PROMPT.format(
            filename=relative_path,
            language=language,
            code=code,
        )

        response = self.llm.generate(prompt)
        response = response.strip()

        # Clean markdown fences
        if response.startswith("```json"):
            response = response[7:]
        if response.startswith("```"):
            response = response[3:]
        if response.endswith("```"):
            response = response[:-3]
        response = response.strip()

        findings = []

        try:
            items = json.loads(response)
            if not isinstance(items, list):
                return []

            for item in items:
                findings.append(
                    Finding(
                        tool="LLM Quality Reviewer",
                        rule=item.get("rule", "Quality Issue"),
                        severity=item.get("severity", "LOW"),
                        file=relative_path,
                        line=item.get("line", 1),
                        message=item.get("message", ""),
                    )
                )
        except Exception as e:
            print(f"LLM Quality Review parse error: {e}")

        return findings
