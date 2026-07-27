from pathlib import Path


# ── Severity helpers ──────────────────────────────────────────────────────────

SEVERITY_ICON = {
    "CRITICAL": "🔴",
    "HIGH":     "🟠",
    "MEDIUM":   "🟡",
    "LOW":      "🟢",
}

GRADE_BADGE = {
    "A": "brightgreen",
    "B": "green",
    "C": "yellow",
    "D": "orange",
    "F": "red",
}

RISK_BADGE = {
    "LOW":      "brightgreen",
    "MEDIUM":   "yellow",
    "HIGH":     "orange",
    "CRITICAL": "red",
}


def _score_bar(score: int) -> str:
    """Unicode progress bar for the score (0–100)."""
    filled = round(score / 5)      # out of 20 blocks
    empty  = 20 - filled
    return "█" * filled + "░" * empty


def _severity_mini_bar(count: int, total: int) -> str:
    if total == 0:
        return "░" * 10
    filled = round((count / total) * 10)
    return "█" * filled + "░" * (10 - filled)


def _top_findings_table(findings: list, limit: int = 8) -> str:
    """Return a markdown table of the top N findings sorted by severity."""
    order = {"CRITICAL": 0, "HIGH": 1, "MEDIUM": 2, "LOW": 3}
    sorted_f = sorted(
        findings,
        key=lambda f: order.get(f.severity.upper(), 4),
    )[:limit]

    if not sorted_f:
        return "_No findings._"

    lines = [
        "| Severity | Agent | Rule | File | Line |",
        "|----------|-------|------|------|-----:|",
    ]
    for f in sorted_f:
        icon = SEVERITY_ICON.get(f.severity.upper(), "⚪")
        fname = Path(f.file).name
        title = (f.review.title or f.rule) if f.review else f.rule
        lines.append(
            f"| {icon} {f.severity.upper()} | {f.agent} | {title} | `{fname}` | {f.line} |"
        )
    return "\n".join(lines)


def _agent_breakdown(findings: list) -> str:
    """One-line count per agent."""
    agents = {}
    for f in findings:
        agents[f.agent] = agents.get(f.agent, 0) + 1

    agent_icons = {
        "Security":      "🔐",
        "Quality":       "📐",
        "TestGap":       "🧪",
        "Documentation": "📄",
    }

    rows = []
    for agent, count in sorted(agents.items(), key=lambda x: -x[1]):
        icon = agent_icons.get(agent, "🤖")
        rows.append(f"| {icon} {agent} | **{count}** |")

    if not rows:
        return "| Agent | Findings |\n|-------|----------|\n| — | 0 |"

    return "| Agent | Findings |\n|-------|----------:|\n" + "\n".join(rows)


def _scanner_list(stats: dict) -> str:
    scanners = stats.get("findings_per_scanner", {})
    if not scanners:
        return "_None_"
    return ", ".join(
        f"`{s}` ({c})" for s, c in sorted(scanners.items(), key=lambda x: -x[1])
    )


def _affected_files_list(stats: dict) -> str:
    files = stats.get("file_names", [])
    if not files:
        return "_No files affected._"
    return "\n".join(f"- `{f}`" for f in files[:10]) + (
        f"\n- _…and {len(files) - 10} more_" if len(files) > 10 else ""
    )


# ── Main formatter ────────────────────────────────────────────────────────────

def format_summary_comment(state: dict) -> str:
    """
    Build a rich, structured GitHub PR comment from the final review state.
    Uses GitHub-flavoured Markdown: tables, collapsible sections, badges.
    """
    score    = state.get("score", 0) or 0
    grade    = state.get("grade", "?")
    risk     = state.get("risk", "UNKNOWN")
    summary  = state.get("summary", "No summary generated.")
    findings = state.get("findings", [])
    stats    = state.get("stats", {})
    feedback = state.get("reviewer_feedback", "")

    total    = stats.get("total_findings", len(findings))
    critical = stats.get("critical", sum(1 for f in findings if f.severity.upper() == "CRITICAL"))
    high     = stats.get("high",     sum(1 for f in findings if f.severity.upper() == "HIGH"))
    medium   = stats.get("medium",   sum(1 for f in findings if f.severity.upper() == "MEDIUM"))
    low      = stats.get("low",      sum(1 for f in findings if f.severity.upper() == "LOW"))

    grade_color = GRADE_BADGE.get(grade, "lightgrey")
    risk_color  = RISK_BADGE.get(risk.upper(), "lightgrey")

    score_bar = _score_bar(score)

    # ── Build the comment ─────────────────────────────────────────────────────
    lines = []

    # Header
    lines += [
        "## 🤖 ReviewGuard AI — Automated Code Review",
        "",
        "> Powered by a multi-agent pipeline: **Security · Quality · Test Gap · Documentation**",
        "",
        "---",
        "",
    ]

    # Score dashboard (badge-style using shields.io)
    lines += [
        "### 📊 Overall Score",
        "",
        f"![Score](https://img.shields.io/badge/Score-{score}%2F100-{grade_color}?style=for-the-badge) "
        f"![Grade](https://img.shields.io/badge/Grade-{grade}-{grade_color}?style=for-the-badge) "
        f"![Risk](https://img.shields.io/badge/Risk-{risk}-{risk_color}?style=for-the-badge)",
        "",
        f"`{score_bar}` **{score}/100**",
        "",
        "---",
        "",
    ]

    # Severity summary
    lines += [
        "### 🚨 Findings Summary",
        "",
        "| Severity | Count | Distribution |",
        "|----------|------:|--------------|",
        f"| 🔴 Critical | **{critical}** | `{_severity_mini_bar(critical, total)}` |",
        f"| 🟠 High     | **{high}**     | `{_severity_mini_bar(high, total)}` |",
        f"| 🟡 Medium   | **{medium}**   | `{_severity_mini_bar(medium, total)}` |",
        f"| 🟢 Low      | **{low}**      | `{_severity_mini_bar(low, total)}` |",
        f"| **Total**   | **{total}**    | |",
        "",
        "---",
        "",
    ]

    # Agent breakdown
    lines += [
        "### 🤖 Agent Breakdown",
        "",
        _agent_breakdown(findings),
        "",
        "---",
        "",
    ]

    # Executive summary
    lines += [
        "### 📝 AI Executive Summary",
        "",
        summary,
        "",
    ]

    # Reviewer feedback (only if rejection happened before final approval)
    if feedback:
        lines += [
            "",
            "> **👤 Reviewer Note:** " + feedback,
            "",
        ]

    lines += ["---", ""]

    # Top findings table
    lines += [
        "### 🔥 Top Issues",
        "",
        _top_findings_table(findings),
        "",
        "---",
        "",
    ]

    # Collapsible: all findings per agent
    security_findings = [f for f in findings if f.agent == "Security"]
    quality_findings  = [f for f in findings if f.agent == "Quality"]
    testgap_findings  = [f for f in findings if f.agent == "TestGap"]
    doc_findings      = [f for f in findings if f.agent == "Documentation"]

    def _collapsible_agent(icon, title, agent_findings):
        if not agent_findings:
            return []
        rows = ["| Severity | Rule | File | Line |",
                "|----------|------|------|-----:|"]
        for f in agent_findings:
            icon_s = SEVERITY_ICON.get(f.severity.upper(), "⚪")
            fname  = Path(f.file).name
            title_ = (f.review.title or f.rule) if f.review else f.rule
            rows.append(f"| {icon_s} {f.severity.upper()} | {title_} | `{fname}` | {f.line} |")
        table = "\n".join(rows)
        return [
            f"<details>",
            f"<summary>{icon} <strong>{title}</strong> — {len(agent_findings)} finding(s)</summary>",
            "",
            table,
            "",
            "</details>",
            "",
        ]

    lines += ["### 📋 All Findings (by agent)", ""]
    lines += _collapsible_agent("🔐", "Security", security_findings)
    lines += _collapsible_agent("📐", "Quality",  quality_findings)
    lines += _collapsible_agent("🧪", "Test Gap", testgap_findings)
    lines += _collapsible_agent("📄", "Documentation", doc_findings)
    lines += ["---", ""]

    # Scanner coverage
    lines += [
        "### 🛠️ Scanner Coverage",
        "",
        _scanner_list(stats),
        "",
        "---",
        "",
    ]

    # Affected files (collapsible)
    file_list = _affected_files_list(stats)
    lines += [
        "<details>",
        f"<summary>📂 <strong>Affected Files</strong> — {stats.get('affected_files', '?')} file(s)</summary>",
        "",
        file_list,
        "",
        "</details>",
        "",
        "---",
        "",
    ]

    # Footer
    lines += [
        "<sub>",
        "🔒 **ReviewGuard AI** · Multi-Agent DevSecOps Platform · "
        "Powered by LangGraph, Groq, Bandit, Semgrep, Gitleaks, Ruff & Pylint",
        "</sub>",
        "",
    ]

    return "\n".join(lines)