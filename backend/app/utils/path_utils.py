from pathlib import Path


def normalize_path(path: str) -> str:
    """
    Keep only the last two path components.

    Example:
    temp/reviewguard-demo/calculator.py
    """

    if not path:
        return ""

    parts = Path(path).parts

    if len(parts) >= 2:
        return "/".join(parts[-2:])

    return Path(path).name