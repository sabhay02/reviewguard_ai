from app.models.finding import Finding


class TestGapParser:

    def parse(self, finding: dict, review):

        return Finding(
            agent="Test Gap",
            tool="Test Gap Detector",
            rule="Missing Unit Test",

            severity="MEDIUM",
            confidence="HIGH",

            file=finding["file"],
            line=1,

            message=finding["reason"],

            review=review,
        )