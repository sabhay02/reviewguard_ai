import ast
import os

from app.utils.filter import get_source_files


class DocumentationScanner:

    def scan(
        self,
        repo_path: str,
        changed_files: list | None = None,
    ):

        findings = []

        # -----------------------------
        # Check README
        # -----------------------------
        readme = os.path.join(repo_path, "README.md")

        if not os.path.exists(readme):

            findings.append(
                {
                    "rule": "Missing README",
                    "severity": "MEDIUM",
                    "file": "README.md",
                    "line": 1,
                    "message": "Repository does not contain a README.md file.",
                }
            )

        else:

            with open(readme, "r", encoding="utf-8") as f:
                content = f.read().strip()

            if len(content) < 100:

                findings.append(
                    {
                        "rule": "Weak README",
                        "severity": "LOW",
                        "file": "README.md",
                        "line": 1,
                        "message": "README exists but contains very little documentation.",
                    }
                )

        # -----------------------------
        # Scan only changed Python files
        # -----------------------------
        paths = get_source_files(repo_path, changed_files)

        print("Documentation scanning:", paths)

        for path in paths:

            if not path.endswith(".py"):
                continue

            findings.extend(
                self.scan_python_file(path, repo_path)
            )

        return findings

    def scan_python_file(self, file_path, repo_path):

        findings = []

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                source = f.read()

            tree = ast.parse(source)

        except Exception:
            return findings

        relative_path = os.path.relpath(file_path, repo_path)

        # Module docstring
        if not ast.get_docstring(tree):
            findings.append(
                {
                    "rule": "Missing Module Docstring",
                    "severity": "LOW",
                    "file": relative_path,
                    "line": 1,
                    "message": "Module does not contain a top-level docstring.",
                }
            )

        # Class docstrings
        for node in ast.walk(tree):

            if isinstance(node, ast.ClassDef):

                if not ast.get_docstring(node):

                    findings.append(
                        {
                            "rule": "Missing Class Docstring",
                            "severity": "LOW",
                            "file": relative_path,
                            "line": node.lineno,
                            "message": f"Class '{node.name}' does not contain a docstring.",
                        }
                    )

        # Function docstrings
        for node in ast.walk(tree):

            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):

                if not ast.get_docstring(node):

                    findings.append(
                        {
                            "rule": "Missing Function Docstring",
                            "severity": "LOW",
                            "file": relative_path,
                            "line": node.lineno,
                            "message": f"Function '{node.name}' does not contain a docstring.",
                        }
                    )

        return findings