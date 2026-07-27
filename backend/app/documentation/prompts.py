DOCUMENTATION_PROMPT = """
You are a senior software documentation reviewer.

Analyze the following documentation issue.

Tool:
{tool}

Rule:
{rule}

Severity:
{severity}

Issue:
{message}

IMPORTANT:
Return your response as valid JSON only.
Do not include markdown, explanations, or code fences.

The JSON must have exactly this format:

{{
  "title": "...",
  "summary": "...",
  "impact": "...",
  "recommendation": "...",
  "secure_code": "...",
  "status": "Open"
}}
"""