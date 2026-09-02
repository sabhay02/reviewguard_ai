import os
import re
from pathlib import Path

from app.utils.filter import get_source_files


# Map of file extensions to their test file conventions
TEST_CONVENTIONS = {
    # JavaScript / TypeScript
    ".js": {
        "test_patterns": ["test_{stem}.js", "{stem}.test.js", "{stem}.spec.js"],
        "test_dirs": ["tests", "test", "__tests__"],
        "func_pattern": re.compile(
            r'(?:^|\n)(?:export\s+)?(?:async\s+)?function\s+(\w+)|'
            r'(?:^|\n)(?:export\s+)?(?:const|let|var)\s+(\w+)\s*=\s*(?:async\s+)?\(',
            re.MULTILINE,
        ),
    },
    ".jsx": {
        "test_patterns": ["test_{stem}.jsx", "{stem}.test.jsx", "{stem}.spec.jsx", "{stem}.test.js"],
        "test_dirs": ["tests", "test", "__tests__"],
        "func_pattern": re.compile(
            r'(?:^|\n)(?:export\s+)?(?:async\s+)?function\s+(\w+)|'
            r'(?:^|\n)(?:export\s+)?(?:const|let|var)\s+(\w+)\s*=\s*(?:async\s+)?\(',
            re.MULTILINE,
        ),
    },
    ".ts": {
        "test_patterns": ["test_{stem}.ts", "{stem}.test.ts", "{stem}.spec.ts"],
        "test_dirs": ["tests", "test", "__tests__"],
        "func_pattern": re.compile(
            r'(?:^|\n)(?:export\s+)?(?:async\s+)?function\s+(\w+)|'
            r'(?:^|\n)(?:export\s+)?(?:const|let|var)\s+(\w+)\s*=\s*(?:async\s+)?\(',
            re.MULTILINE,
        ),
    },
    ".tsx": {
        "test_patterns": ["test_{stem}.tsx", "{stem}.test.tsx", "{stem}.spec.tsx", "{stem}.test.ts"],
        "test_dirs": ["tests", "test", "__tests__"],
        "func_pattern": re.compile(
            r'(?:^|\n)(?:export\s+)?(?:async\s+)?function\s+(\w+)|'
            r'(?:^|\n)(?:export\s+)?(?:const|let|var)\s+(\w+)\s*=\s*(?:async\s+)?\(',
            re.MULTILINE,
        ),
    },
    # Java
    ".java": {
        "test_patterns": ["{stem}Test.java", "Test{stem}.java"],
        "test_dirs": ["test", "tests", "src/test"],
        "func_pattern": re.compile(
            r'(?:public|private|protected)\s+(?:static\s+)?(?:\w+\s+)+(\w+)\s*\(',
            re.MULTILINE,
        ),
    },
    # Go
    ".go": {
        "test_patterns": ["{stem}_test.go"],
        "test_dirs": ["."],  # Go tests live alongside source
        "func_pattern": re.compile(
            r'^func\s+(?:\(\w+\s+\*?\w+\)\s+)?(\w+)\s*\(',
            re.MULTILINE,
        ),
    },
    # C / C++
    ".c": {
        "test_patterns": ["test_{stem}.c", "{stem}_test.c"],
        "test_dirs": ["tests", "test"],
        "func_pattern": re.compile(
            r'^(?:\w+\s+)+(\w+)\s*\([^)]*\)\s*\{',
            re.MULTILINE,
        ),
    },
    ".cpp": {
        "test_patterns": ["test_{stem}.cpp", "{stem}_test.cpp"],
        "test_dirs": ["tests", "test"],
        "func_pattern": re.compile(
            r'^(?:\w+\s+)+(\w+)\s*\([^)]*\)\s*\{',
            re.MULTILINE,
        ),
    },
    # C#
    ".cs": {
        "test_patterns": ["{stem}Tests.cs", "Test{stem}.cs"],
        "test_dirs": ["Tests", "tests", "test"],
        "func_pattern": re.compile(
            r'(?:public|private|protected)\s+(?:static\s+)?(?:\w+\s+)+(\w+)\s*\(',
            re.MULTILINE,
        ),
    },
    # Rust
    ".rs": {
        "test_patterns": ["{stem}_test.rs", "test_{stem}.rs"],
        "test_dirs": ["tests", "test"],
        "func_pattern": re.compile(
            r'^(?:pub\s+)?(?:async\s+)?fn\s+(\w+)',
            re.MULTILINE,
        ),
    },
}


class MultiLangTestGapDetector:
    """Detects missing test files for non-Python source files."""

    def _extract_functions(self, file_path: str, ext: str) -> list[str]:
        """Extract function names from a non-Python source file using regex."""

        config = TEST_CONVENTIONS.get(ext)
        if not config:
            return []

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                source = f.read()
        except Exception:
            return []

        functions = []
        for match in config["func_pattern"].finditer(source):
            # Get the first non-None group (handles alternation patterns)
            name = next((g for g in match.groups() if g is not None), None)
            if name:
                functions.append(name)

        return functions

    def detect(
        self,
        repo_path: str,
        changed_files: list | None = None,
    ) -> list[dict]:

        repo = Path(repo_path)
        findings = []

        paths = get_source_files(repo_path, changed_files)

        for path in paths:
            file_path = Path(path)

            # Skip Python files (handled by existing detector)
            if file_path.suffix == ".py":
                continue

            ext = file_path.suffix.lower()
            config = TEST_CONVENTIONS.get(ext)
            if not config:
                continue

            # Skip files inside test directories
            if any(part in ["tests", "test", "__tests__"] for part in file_path.parts):
                continue

            # Skip node_modules
            if "node_modules" in file_path.parts:
                continue

            stem = file_path.stem

            # Check if a corresponding test file exists
            test_found = False
            for test_dir_name in config["test_dirs"]:
                test_dir = repo / test_dir_name
                for test_pattern in config["test_patterns"]:
                    test_file = test_dir / test_pattern.format(stem=stem)
                    if test_file.exists():
                        test_found = True
                        break

                    # Also check same directory as source (common in Go, JS)
                    same_dir_test = file_path.parent / test_pattern.format(stem=stem)
                    if same_dir_test.exists():
                        test_found = True
                        break

                if test_found:
                    break

            if not test_found:
                try:
                    relative = str(file_path.relative_to(repo))
                except ValueError:
                    relative = str(file_path)

                functions = self._extract_functions(str(file_path), ext)

                findings.append({
                    "file": relative,
                    "test_file": f"tests/test_{stem}{ext}",
                    "reason": "Missing test file",
                    "functions": functions,
                })

        return findings
