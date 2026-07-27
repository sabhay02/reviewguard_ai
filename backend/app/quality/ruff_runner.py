import subprocess

def run_ruff(paths: list[str]):

    if not paths:
        return "[]"

    command = [
        "ruff",
        "check",
        "--output-format",
        "json",
        "--",
        *paths
    ]

    print("Running:", command)

    result = subprocess.run(
        command,
        capture_output=True,
        text=True
    )
    
    print("Return Code:", result.returncode)
    print("STDOUT:")
    print(result.stdout)
    print("STDERR:")
    print(result.stderr)

    if result.returncode not in (0, 1):
        return "[]"

    return result.stdout or "[]"