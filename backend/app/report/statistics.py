from collections import Counter
from pathlib import Path

from app.models.finding import Finding


class RepositoryStatistics:

    def generate(self, findings: list[Finding]) -> dict:

        files = {Path(f.file).name for f in findings}
        rules = {f.rule for f in findings}
        scanners = {f.tool for f in findings}

        severity_count = Counter()
        scanner_count = Counter()

        for finding in findings:
            severity_count[finding.severity.upper()] += 1
            scanner_count[finding.tool] += 1

        return {
            "total_findings": len(findings),
            "affected_files": len(files),
            "unique_rules": len(rules),
            "scanners": len(scanners),

            "scanner_names": sorted(scanners),
            "file_names": sorted(files),

            "critical": severity_count["CRITICAL"],
            "high": severity_count["HIGH"],
            "medium": severity_count["MEDIUM"],
            "low": severity_count["LOW"],

            # NEW
            "findings_per_scanner": dict(scanner_count),
        }