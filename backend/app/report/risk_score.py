from app.models.finding import Finding


class RiskScorer:

    WEIGHTS = {
        "CRITICAL": 40,
        "HIGH": 20,
        "MEDIUM": 10,
        "LOW": 5,
    }

    def calculate(self, findings: list[Finding]):

        counts = {"CRITICAL": 0, "HIGH": 0, "MEDIUM": 0, "LOW": 0}

        for finding in findings:
            severity = finding.severity.upper()
            if severity in counts:
                counts[severity] += 1

        score = 100.0
        score *= (0.50 ** counts["CRITICAL"])
        score *= (0.80 ** counts["HIGH"])
        score *= (0.90 ** counts["MEDIUM"])
        score *= (0.98 ** counts["LOW"])

        score = int(score)

        if score >= 90:
            grade = "A"
            risk = "LOW"

        elif score >= 75:
            grade = "B"
            risk = "MEDIUM"

        elif score >= 60:
            grade = "C"
            risk = "HIGH"

        elif score >= 40:
            grade = "D"
            risk = "HIGH"

        else:
            grade = "F"
            risk = "SEVERE"

        return {
            "score": score,
            "grade": grade,
            "risk": risk,
        }