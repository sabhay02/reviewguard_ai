import json

from app.models.finding import Finding


def parse_bandit(data: str) -> list[Finding]:
    """
    Parse Bandit JSON output into Finding objects.
    """

    try:
        data = json.loads(data)
    except json.JSONDecodeError:
        return []

    findings = []

    for result in data.get("results", []):

        findings.append(
            Finding(
                tool="Bandit",
                rule=result.get("test_id", "Unknown"),
                severity=result.get("issue_severity", "UNKNOWN"),
                confidence=result.get("issue_confidence"),
                file=result.get("filename"),
                line=result.get("line_number", 0),
                message=result.get("issue_text", ""),
            )
        )

    return findings