import json

from app.models.finding import Finding
from app.security.severity import SeverityMapper


def parse_semgrep(data: str) -> list[Finding]:
    """
    Parse Semgrep JSON output into Finding objects.
    """

    try:
        data = json.loads(data)
    except json.JSONDecodeError:
        return []

    findings = []

    for result in data.get("results", []):

        extra = result.get("extra", {})

        findings.append(
            Finding(
                tool="Semgrep",
                rule=result.get("check_id", "Unknown"),
                severity=SeverityMapper.normalize(
                    "Semgrep",
                    extra.get("severity", "LOW"),
                ),
                confidence=None,
                file=result.get("path"),
                line=result.get("start", {}).get("line", 0),
                message=extra.get("message", ""),
            )
        )

    return findings