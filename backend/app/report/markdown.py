from datetime import datetime
from pathlib import Path
from collections import Counter
from app.models.finding import Finding

SEVERITY_ICON = {
    "LOW": "🟢",
    "MEDIUM": "🟡",
    "HIGH": "🟠",
    "CRITICAL": "🔴",
}


class MarkdownReportGenerator:

    def finding_card(self, finding: Finding) -> list[str]:

        report = []

        severity = finding.severity.upper()
        icon = SEVERITY_ICON.get(severity, "⚪")

        filename = Path(finding.file).name

        report.append("---")
        report.append("")

        report.append("<details>")
        report.append(f"<summary><strong>{icon} {finding.review.title}</strong></summary>")
        report.append("")

        report.append("| Property | Value |")
        report.append("|----------|-------|")
        report.append(f"| Agent | {finding.agent} |")
        report.append(f"| Tool | {finding.tool} |")
        report.append(f"| Rule | {finding.rule} |")
        report.append(f"| Severity | {icon} {severity} |")
        report.append(f"| File | `{filename}` |")
        report.append(f"| Line | {finding.line} |")
        report.append(f"| Status | {finding.review.status} |")

        report.append("")
        report.append("### 📝 Summary")
        report.append("")
        report.append(finding.review.summary)

        report.append("")
        report.append("### ⚠️ Impact")
        report.append("")
        report.append(finding.review.impact)

        report.append("")
        report.append("### ✅ Recommendation")
        report.append("")
        report.append(finding.review.recommendation)

        report.append("")

        if finding.review.secure_code:

            title = (
                "Suggested Test Code"
                if finding.agent == "Test Gap"
                else "Suggested Fix"
            )

            report.append(f"### 💡 {title}")
            report.append("")
            report.append("```python")
            report.append(finding.review.secure_code)
            report.append("```")
            report.append("")

        report.append("</details>")
        report.append("")

        return report
        
    def add_findings_section(
    self,
    report,
    findings,
    title,
):

        report.append(f"# {title}")
        report.append("")

        if not findings:
            report.append("✅ No findings.")
            report.append("")
            return

        for finding in findings:
            report.extend(
                self.finding_card(finding)
            )

    def executive_dashboard(
    self,
    score: dict,
    executive_summary: str,
) -> list[str]:

        report = []

        report.append("# 🔒 ReviewGuard AI Report")
        report.append("")
        report.append("> AI-Powered Multi-Agent DevSecOps Code Review")
        report.append("")
        report.append(
            f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        )

        report.append("")
        report.append("---")
        report.append("")

        report.append("## 📊 Executive Dashboard")
        report.append("")

        report.append("| Metric | Status |")
        report.append("|--------|--------|")
        report.append(f"| Repository Score | **{score['score']}/100** |")
        report.append(f"| Risk Grade | **{score['grade']}** |")
        report.append(f"| Overall Risk | **{score['risk']}** |")
        report.append("| Human Review | ⏳ Pending |")

        report.append("")
        report.append("---")
        report.append("")

        report.append("## 🤖 AI Assessment")
        report.append("")
        report.append(executive_summary)

        report.append("")
        report.append("---")
        report.append("")

        return report

    def statistics_section(
    self,
    stats: dict,
    score: dict,
    security_findings: list,
    quality_findings: list,
    documentation_findings: list,
    test_gap_findings: list,
) -> list[str]:

        report = []

        report.append("## 📈 Repository Statistics")
        report.append("")

        report.append("| Metric | Value |")
        report.append("|--------|------:|")

        report.append(f"| Total Findings | {stats['total_findings']} |")
        report.append(f"| Security Findings | {len(security_findings)} |")
        report.append(f"| Quality Findings | {len(quality_findings)} |")
        report.append(f"| Documentation Findings | {len(documentation_findings)} |")
        report.append(f"| Test Gap Findings | {len(test_gap_findings)} |")

        report.append(f"| Affected Files | {stats['affected_files']} |")
        report.append(f"| Unique Rules | {stats['unique_rules']} |")
        report.append(f"| Security Scanners | {stats['scanners']} |")

        report.append(f"| Repository Score | {score['score']}/100 |")
        report.append(f"| Risk Grade | {score['grade']} |")
        report.append(f"| Overall Risk | {score['risk']} |")

        report.append("")
        report.append("---")
        report.append("")

        return report

    def severity_section(
    self,
    stats: dict,
) -> list[str]:

        report = []

        report.append("## 🚨 Severity Dashboard")
        report.append("")

        report.append("| Severity | Count |")
        report.append("|----------|------:|")
        report.append(f"| 🔴 Critical | {stats['critical']} |")
        report.append(f"| 🟠 High | {stats['high']} |")
        report.append(f"| 🟡 Medium | {stats['medium']} |")
        report.append(f"| 🟢 Low | {stats['low']} |")

        report.append("")

        total = max(stats["total_findings"], 1)

        def bar(count):
            filled = round((count / total) * 20)
            return "█" * filled + "░" * (20 - filled)

        report.append("### Visual Distribution")
        report.append("")
        report.append(
            f"🔴 Critical : `{bar(stats['critical'])}` ({stats['critical']})"
        )
        report.append(
            f"🟠 High     : `{bar(stats['high'])}` ({stats['high']})"
        )
        report.append(
            f"🟡 Medium   : `{bar(stats['medium'])}` ({stats['medium']})"
        )
        report.append(
            f"🟢 Low      : `{bar(stats['low'])}` ({stats['low']})"
        )

        report.append("")
        report.append("---")
        report.append("")

        return report

    def scanner_section(
    self,
    stats: dict,
) -> list[str]:

        report = []

        report.append("## 🛠 Scanner Coverage")
        report.append("")

        report.append("| Scanner | Findings |")
        report.append("|---------|---------:|")

        scanners = stats.get("findings_per_scanner", {})

        if not scanners:
            report.append("| None | 0 |")
        else:
            for scanner, count in sorted(
                scanners.items(),
                key=lambda x: x[1],
                reverse=True,
            ):
                report.append(f"| {scanner} | {count} |")

        report.append("")
        report.append("---")
        report.append("")

        return report

    def affected_files_section(
    self,
    findings: list[Finding],
) -> list[str]:

        report = []

        report.append("## 📂 Affected Files")
        report.append("")

        if not findings:
            report.append("✅ No affected files.")
            report.append("")
            report.append("---")
            report.append("")
            return report

        counter = Counter()

        for finding in findings:
            filename = Path(finding.file).name
            counter[filename] += 1

        report.append("| File | Findings |")
        report.append("|------|---------:|")

        for filename, count in sorted(
            counter.items(),
            key=lambda x: x[1],
            reverse=True,
        ):
            report.append(f"| `{filename}` | {count} |")

        report.append("")
        report.append(f"**Total Files Affected:** {len(counter)}")

        report.append("")
        report.append("---")
        report.append("")

        return report


    def action_plan_section(
    self,
    findings: list[Finding],
) -> list[str]:

        report = []

        report.append("## 🎯 AI Action Plan")
        report.append("")

        if not findings:
            report.append("✅ Repository is healthy. No actions required.")
            report.append("")
            report.append("---")
            report.append("")
            return report

        priority = {
            "CRITICAL": [],
            "HIGH": [],
            "MEDIUM": [],
            "LOW": [],
        }

        for finding in findings:
            sev = finding.severity.upper()
            priority.setdefault(sev, []).append(finding)

        sections = [
            ("🔴 Immediate Priority", "CRITICAL"),
            ("🟠 High Priority", "HIGH"),
            ("🟡 Medium Priority", "MEDIUM"),
            ("🟢 Low Priority", "LOW"),
        ]

        for title, level in sections:

            if not priority[level]:
                continue

            report.append(f"### {title}")
            report.append("")

            for idx, finding in enumerate(priority[level], start=1):

                filename = Path(finding.file).name

                report.append(
                    f"{idx}. **{finding.review.title}** (`{filename}:{finding.line}`)"
                )

            report.append("")

        report.append("---")
        report.append("")

        return report

    def top_issues_section(
    self,
    findings: list[Finding],
) -> list[str]:

        report = []

        report.append("## 🔥 Top Issues")
        report.append("")

        if not findings:
            report.append("✅ No critical issues found.")
            report.append("")
            report.append("---")
            report.append("")
            return report

        severity_order = {
            "CRITICAL": 0,
            "HIGH": 1,
            "MEDIUM": 2,
            "LOW": 3,
        }

        sorted_findings = sorted(
            findings,
            key=lambda f: severity_order.get(
                f.severity.upper(),
                4,
            ),
        )
        report.append("| Priority | Agent | Issue | File |")
        report.append("|----------|-------|-------|------|")

        for finding in sorted_findings[:10]:

            severity = finding.severity.upper()

            icon = SEVERITY_ICON.get(
                severity,
                "⚪",
            )

            filename = Path(finding.file).name

            report.append(
                f"| {icon} {severity} | "
                f"{finding.agent} | "
                f"{finding.review.title} | "
                f"`{filename}` |"
            )
        report.append("")
        report.append("---")
        report.append("")

        return report

    def footer_section(
    self,
    stats: dict,
) -> list[str]:

        report = []

        report.append("---")
        report.append("")

        report.append("## 📌 Scan Metadata")
        report.append("")

        report.append("| Property | Value |")
        report.append("|----------|-------|")
        report.append(
            f"| Generated At | {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} |"
        )
        report.append("| Generated By | ReviewGuard AI |")
        report.append("| Report Version | v1.0 |")
        report.append("| Review Type | Multi-Agent AI Review |")
        report.append(f"| Total Findings | {stats['total_findings']} |")
        report.append(f"| Security Scanners | {stats['scanners']} |")

        scanners = ", ".join(stats["findings_per_scanner"].keys())

        report.append(f"| Tools Used | {scanners} |")

        report.append("")
        report.append(
            "> Generated automatically by **ReviewGuard AI**."
        )
        report.append(
            "> Multi-Agent DevSecOps Platform powered by LangGraph, Hybrid RAG, Ruff, Pylint, Bandit, Semgrep and Gitleaks."
        )

        report.append("")

        return report
        
    def generate(
        self,
        findings: list[Finding],
        score: dict,
        stats: dict,
        executive_summary: str,
    ) -> str:

        report = []
        security_findings = [
            f for f in findings
            if getattr(f, "agent", "") == "Security"
        ]

        quality_findings = [
            f for f in findings
            if getattr(f, "agent", "") == "Quality"
        ]
        test_gap_findings = [
    f for f in findings
    if f.agent == "Test Gap"
]
        documentation_findings = [
    f for f in findings
    if getattr(f, "agent", "") == "Documentation"
]
        

        report.extend(
    self.executive_dashboard(
        score,
        executive_summary,
    )
)

        # =====================================================
        # Repository Statistics
        # =====================================================

        report.extend(
    self.statistics_section(
        stats,
        score,
        security_findings,
        quality_findings,
        documentation_findings,
        test_gap_findings,
    )
)
        # =====================================================
        # Severity Dashboard
        # =====================================================

        report.extend(
    self.severity_section(stats)
)

        # =====================================================
        # Scanner Coverage
        # =====================================================

        report.extend(
    self.scanner_section(stats)
)
        
        # =====================================================
        # Affected Files
        # =====================================================

        report.extend(
    self.affected_files_section(findings)
)

        report.extend(
    self.top_issues_section(findings)
)
        
        report.extend(
    self.action_plan_section(findings)
)

        report.extend(
    self.footer_section(stats)
)


        for i, item in enumerate(report):
            if item is None:
                print(f"None found at index {i}")

        return "\n".join(str(item) for item in report)

    

    def save(self, markdown: str, output_path: str):

        output = Path(output_path)

        output.parent.mkdir(parents=True, exist_ok=True)

        output.write_text(markdown, encoding="utf-8")