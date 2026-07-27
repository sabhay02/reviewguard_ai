from app.models.finding import Finding


def normalize_message(message: str) -> str:
    """
    Normalize messages from different tools.
    """

    msg = message.lower()

    if "unused import" in msg or "imported but unused" in msg:
        return "unused-import"

    if "docstring" in msg:
        return "missing-docstring"

    if "final newline" in msg:
        return "missing-final-newline"

    return msg.strip()


def deduplicate(findings: list[Finding]) -> list[Finding]:

    unique = []
    seen = set()

    for finding in findings:

        key = (
            finding.file,
            finding.line,
            normalize_message(finding.message),
        )

        if key not in seen:
            seen.add(key)
            unique.append(finding)

    return unique