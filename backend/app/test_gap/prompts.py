TEST_GAP_PROMPT = """
You are an expert Python Test Engineer.

A Python source file has no corresponding unit tests.

File:
{file}

Functions:
{functions}

Your job is to:

1. Explain why missing tests are a problem.
2. Describe the possible impact.
3. Recommend adding pytest tests.
4. Generate starter pytest test cases for ALL functions.

Return ONLY valid JSON.

Rules:
- Do NOT use markdown.
- Do NOT wrap the response in ```json.
- "secure_code" MUST be a STRING.
- Escape all newline characters using \n.
- Do NOT use triple quotes.
- Do NOT return nested objects.

Example:

{{
    "title": "Missing Unit Tests",
    "summary": "...",
    "impact": "...",
    "recommendation": "...",
    "secure_code": "import pytest\n\ndef test_add():\n    assert add(2,3)==5",
    "status": "Open"
}}
"""