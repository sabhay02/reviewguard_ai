class SeverityMapper:

    SEMGREP = {
        "INFO": "LOW",
        "WARNING": "MEDIUM",
        "ERROR": "HIGH",
    }

    GITLEAKS = {
        "LOW": "LOW",
        "MEDIUM": "MEDIUM",
        "HIGH": "HIGH",
        "CRITICAL": "CRITICAL",
    }

    @staticmethod
    def normalize(tool: str, severity: str) -> str:

        severity = severity.upper()

        if tool == "Semgrep":
            return SeverityMapper.SEMGREP.get(severity, "LOW")

        if tool == "Gitleaks":
            return SeverityMapper.GITLEAKS.get(severity, "HIGH")

        return severity