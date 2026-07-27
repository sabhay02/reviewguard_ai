from app.models.finding import Finding


def calculate_quality_score(findings: list[Finding]) -> int:
    """
    Calculate quality score out of 100.
    """

    score = 100

    penalties = {
        "HIGH": 15,
        "MEDIUM": 8,
        "LOW": 2,
    }

    for finding in findings:
        score -= penalties.get(finding.severity, 2)

    return max(score, 0)