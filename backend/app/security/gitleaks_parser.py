import json

from app.models.finding import Finding
from app.security.severity import SeverityMapper


def parse_gitleaks(data: str) -> list[Finding]:
    """
    Parse Gitleaks JSON output into Finding objects.
    """

    try:
        results = json.loads(data)
    except json.JSONDecodeError:
        return []

    findings = []

    for result in results:

        findings.append(
            Finding(
                tool="Gitleaks",
                rule=result.get("RuleID", "Unknown"),
                severity=SeverityMapper.normalize(
                    "Gitleaks",
                    result.get("Severity", "HIGH"),
                ),
                confidence="HIGH",
                file=result.get("File", ""),
                line=result.get(
                    "StartLine",
                    result.get("Line", 0),
                ),
                message=result.get(
                    "Description",
                    f"Hardcoded secret detected ({result.get('RuleID', 'Unknown')})",
                ),
            )
        )

    return findings