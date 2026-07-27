from app.models.finding import Finding


def parse_documentation(results):

    findings = []

    for item in results:

        findings.append(
            Finding(
                tool="Documentation Scanner",
                rule=item["rule"],
                severity=item["severity"],
                file=item["file"],
                line=item["line"],
                message=item["message"],
            )
        )

    return findings