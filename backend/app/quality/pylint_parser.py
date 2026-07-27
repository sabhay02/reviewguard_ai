import json

from app.models.finding import Finding, AIReview
from app.utils.path_utils import normalize_path

def parse_pylint(raw_output: str):
    """
    Parse Pylint JSON output into Finding objects.
    """

    findings = []

    try:
        data = json.loads(raw_output)
    except json.JSONDecodeError:
        return findings

    for issue in data:

        finding = Finding(
            agent="Quality",
            tool="Pylint",
            rule=issue.get("message-id", "UNKNOWN"),
            severity=map_severity(issue.get("type", "convention")),
            confidence="HIGH",
            file=normalize_path(issue.get("path", "")),
            line=issue.get("line", 0),
            message=issue.get("message", ""),
            review=AIReview(),
        )

        findings.append(finding)

    return findings


def map_severity(issue_type: str):
    """
    Convert Pylint categories to project severity.
    """

    mapping = {
        "fatal": "HIGH",
        "error": "MEDIUM",
        "warning": "LOW",
        "refactor": "LOW",
        "convention": "LOW",
        "info": "LOW",
    }

    return mapping.get(issue_type.lower(), "LOW")