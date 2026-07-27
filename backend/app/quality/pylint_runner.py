import subprocess


def run_pylint(paths: list[str]):

    if not paths:
        return "[]"

    command = [
        "pylint",
        "--recursive=y",
        "--output-format=json",
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

    # Pylint returns non-zero if issues are found.
    # We still want the JSON output.
    if result.stdout.strip():
        return result.stdout

    return "[]"