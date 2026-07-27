from collections import Counter
from app.models.finding import Finding


def generate_quality_stats(findings: list[Finding]):
    """
    Generate statistics for quality findings.
    """

    severity = Counter()
    rules = Counter()
    files = Counter()
    tools = Counter()

    for finding in findings:
        severity[finding.severity] += 1
        rules[finding.rule] += 1
        files[finding.file] += 1
        tools[finding.tool] += 1

    return {
        "total": len(findings),
        "severity": dict(severity),
        "rules": dict(rules),
        "files": dict(files),
        "tools": dict(tools),
    }