import subprocess

def run_semgrep(paths: list[str]):

    if not paths:
        return "[]"

    command = [
        "semgrep",
        "scan",
        "--config",
        "auto",
        "--json",
        "--",
        *paths,
    ]

    print("Running:", command)

    result = subprocess.run(
        command,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace"
    )

    print("Return Code:", result.returncode)
    print("STDOUT:\n", result.stdout)
    print("STDERR:\n", result.stderr)

    if result.returncode not in (0, 1):
        raise RuntimeError(result.stderr)

    return result.stdout