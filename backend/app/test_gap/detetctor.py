import ast
from pathlib import Path

from app.utils.filter import get_source_files
from app.test_gap.multi_lang_detector import MultiLangTestGapDetector


class TestGapDetector:

    def __init__(self):
        self.multi_lang_detector = MultiLangTestGapDetector()

    def _extract_functions(self, file_path: Path) -> list[str]:
        """
        Extract all top-level function names from a Python file.
        """

        try:
            source = file_path.read_text(encoding="utf-8")
            tree = ast.parse(source)

            functions = []

            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    functions.append(node.name)

            return functions

        except Exception:
            return []

    def detect(
        self,
        repo_path: str,
        changed_files: list | None = None,
    ) -> list[dict]:

        repo = Path(repo_path)

        findings = []

        tests_dir = repo / "tests"

        paths = get_source_files(
            repo_path,
            changed_files,
        )

        print("TestGap scanning:", paths)

        for path in paths:

            py_file = Path(path)

            # Only analyze Python source files
            if py_file.suffix != ".py":
                continue

            # Ignore virtual environments
            if ".venv" in py_file.parts:
                continue

            # Ignore cache folders
            if "__pycache__" in py_file.parts:
                continue

            # Ignore test files themselves
            if "tests" in py_file.parts:
                continue

            expected_test = tests_dir / f"test_{py_file.stem}.py"

            if not expected_test.exists():

                findings.append(
                    {
                        "file": str(py_file.relative_to(repo)),
                        "test_file": str(expected_test.relative_to(repo)),
                        "reason": "Missing test file",
                        "functions": self._extract_functions(py_file),
                    }
                )

        # Detect test gaps for non-Python files
        multi_lang_findings = self.multi_lang_detector.detect(repo_path, changed_files)
        findings.extend(multi_lang_findings)

        return findings