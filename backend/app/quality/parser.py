import json

from app.models.finding import Finding, AIReview

from app.utils.path_utils import normalize_path

def parse_ruff(raw_output: str):
    """
    Parse Ruff JSON output into Finding objects.
    """

    findings = []

    try:
        data = json.loads(raw_output)
    except json.JSONDecodeError:
        return findings

    for issue in data:

        finding = Finding(
            tool="Ruff",
            rule=issue.get("code", "UNKNOWN"),
            severity=map_severity(issue.get("severity", "warning")),
            confidence="HIGH",
            file=normalize_path(issue.get("filename", "")),
            line=issue.get("location", {}).get("row", 0),
            message=issue.get("message", ""),
            review=AIReview(),
        )

        findings.append(finding)

    return findings


def map_severity(severity: str) -> str:
    """
    Ruff only reports 'error' or 'warning'.
    Convert them to our project's severity scale.
    """

    mapping = {
        "error": "LOW",
        "warning": "LOW",
    }

    return mapping.get(severity.lower(), "LOW")