from abc import ABC, abstractmethod


class BaseAgent(ABC):
    """
    Base class for every ReviewGuard AI agent.
    """

    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    def analyze(
    self,
    repo_path: str,

):
        """
        Analyze a repository and return findings.
        """
        pass