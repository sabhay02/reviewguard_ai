from app.models.finding import Finding


def deduplicate_findings(findings: list[Finding]) -> list[Finding]:
    seen = set()
    unique = []

    for f in findings:
        key = (
            f.agent,
            f.tool,
            f.rule,
            f.file,
            f.line,
        )

        if key not in seen:
            seen.add(key)
            unique.append(f)

    return unique