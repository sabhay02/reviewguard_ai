import os
import re

from app.utils.filter import get_source_files


# Regex patterns for detecting functions/classes in various languages
# Each entry: (file_extensions, doc_comment_pattern, definition_pattern)
LANGUAGE_PATTERNS = {
    "javascript": {
        "extensions": {".js", ".jsx"},
        "doc_pattern": re.compile(r'/\*\*[\s\S]*?\*/\s*$', re.MULTILINE),
        "func_pattern": re.compile(
            r'^(?:export\s+)?(?:async\s+)?function\s+(\w+)',
            re.MULTILINE,
        ),
        "class_pattern": re.compile(
            r'^(?:export\s+)?class\s+(\w+)',
            re.MULTILINE,
        ),
        "arrow_pattern": re.compile(
            r'^(?:export\s+)?(?:const|let|var)\s+(\w+)\s*=\s*(?:async\s+)?\(',
            re.MULTILINE,
        ),
    },
    "typescript": {
        "extensions": {".ts", ".tsx"},
        "doc_pattern": re.compile(r'/\*\*[\s\S]*?\*/\s*$', re.MULTILINE),
        "func_pattern": re.compile(
            r'^(?:export\s+)?(?:async\s+)?function\s+(\w+)',
            re.MULTILINE,
        ),
        "class_pattern": re.compile(
            r'^(?:export\s+)?class\s+(\w+)',
            re.MULTILINE,
        ),
        "arrow_pattern": re.compile(
            r'^(?:export\s+)?(?:const|let|var)\s+(\w+)\s*=\s*(?:async\s+)?\(',
            re.MULTILINE,
        ),
    },
    "java": {
        "extensions": {".java"},
        "doc_pattern": re.compile(r'/\*\*[\s\S]*?\*/\s*$', re.MULTILINE),
        "func_pattern": re.compile(
            r'(?:public|private|protected)\s+(?:static\s+)?(?:\w+\s+)+(\w+)\s*\(',
            re.MULTILINE,
        ),
        "class_pattern": re.compile(
            r'(?:public|private|protected)?\s*class\s+(\w+)',
            re.MULTILINE,
        ),
        "arrow_pattern": None,
    },
    "go": {
        "extensions": {".go"},
        "doc_pattern": re.compile(r'//\s+\w+.*\n$', re.MULTILINE),
        "func_pattern": re.compile(
            r'^func\s+(?:\(\w+\s+\*?\w+\)\s+)?(\w+)\s*\(',
            re.MULTILINE,
        ),
        "class_pattern": re.compile(
            r'^type\s+(\w+)\s+struct',
            re.MULTILINE,
        ),
        "arrow_pattern": None,
    },
    "c_cpp": {
        "extensions": {".c", ".cpp", ".cs"},
        "doc_pattern": re.compile(r'/\*\*[\s\S]*?\*/\s*$', re.MULTILINE),
        "func_pattern": re.compile(
            r'^(?:\w+\s+)+(\w+)\s*\([^)]*\)\s*\{',
            re.MULTILINE,
        ),
        "class_pattern": re.compile(
            r'^class\s+(\w+)',
            re.MULTILINE,
        ),
        "arrow_pattern": None,
    },
    "rust": {
        "extensions": {".rs"},
        "doc_pattern": re.compile(r'///.*\n$', re.MULTILINE),
        "func_pattern": re.compile(
            r'^(?:pub\s+)?(?:async\s+)?fn\s+(\w+)',
            re.MULTILINE,
        ),
        "class_pattern": re.compile(
            r'^(?:pub\s+)?struct\s+(\w+)',
            re.MULTILINE,
        ),
        "arrow_pattern": None,
    },
}


def _get_lang_config(file_path: str):
    """Return the language config for a given file extension."""
    ext = os.path.splitext(file_path)[1].lower()
    for lang, config in LANGUAGE_PATTERNS.items():
        if ext in config["extensions"]:
            return config
    return None


class MultiLangDocScanner:
    """Scans non-Python source files for missing documentation comments."""

    def scan(self, repo_path: str, changed_files: list | None = None) -> list[dict]:

        findings = []
        paths = get_source_files(repo_path, changed_files)

        for path in paths:
            # Skip Python files (handled by the existing AST scanner)
            if path.endswith(".py"):
                continue

            # If path is a directory, walk it
            if os.path.isdir(path):
                for root, _, files in os.walk(path):
                    for fname in files:
                        full = os.path.join(root, fname)
                        if not full.endswith(".py"):
                            findings.extend(
                                self._scan_file(full, repo_path)
                            )
            else:
                findings.extend(self._scan_file(path, repo_path))

        return findings

    def _scan_file(self, file_path: str, repo_path: str) -> list[dict]:
        """Scan a single non-Python file for missing doc comments."""

        config = _get_lang_config(file_path)
        if config is None:
            return []

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
                lines = content.split("\n")
        except Exception:
            return []

        relative_path = os.path.relpath(file_path, repo_path)
        findings = []

        # Find all function definitions
        for pattern_key in ["func_pattern", "class_pattern", "arrow_pattern"]:
            pattern = config.get(pattern_key)
            if pattern is None:
                continue

            for match in pattern.finditer(content):
                name = match.group(1)
                # Find the line number
                line_num = content[:match.start()].count("\n") + 1

                # Check if there's a doc comment in the 3 lines preceding
                has_doc = False
                start_check = max(0, line_num - 4)
                preceding_text = "\n".join(lines[start_check:line_num - 1])

                if config["doc_pattern"].search(preceding_text):
                    has_doc = True

                if not has_doc:
                    kind = "Function" if "func" in pattern_key or "arrow" in pattern_key else "Class/Struct"
                    findings.append({
                        "rule": f"Missing {kind} Documentation",
                        "severity": "LOW",
                        "file": relative_path,
                        "line": line_num,
                        "message": f"{kind} '{name}' does not have a documentation comment.",
                    })

        return findings
