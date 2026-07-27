from app.agents.security_agent import SecurityAgent
from app.agents.quality_agent import QualityAgent
from app.agents.testgap_agent import TestGapAgent
class Supervisor:

    def __init__(self):

        self.agents = [
            SecurityAgent(),
            QualityAgent(),
            TestGapAgent(),
        ]

    def review_repository(self, repo_path: str):

        findings = []

        for agent in self.agents:

            print(f"\nRunning {agent.name}...")

            findings.extend(
                agent.analyze(repo_path,)
            )

        return findings