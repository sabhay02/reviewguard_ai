import subprocess

def run_gitleaks(repo_path: str) -> str:
    """
    Run Gitleaks against the repository.
    Returns JSON output.
    """

    command = [
        "gitleaks",
        "dir",
        ".",
        "--report-format",
        "json",
        "--report-path",
        "-",
    ]

    print("Running:", command)

    try:
        result = subprocess.run(
            command,
            cwd=repo_path,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
        )

        print("Return Code:", result.returncode)
        print("STDOUT:")
        print(result.stdout)
        print("STDERR:")
        print(result.stderr)

        if result.returncode not in (0, 1):
            raise RuntimeError(result.stderr)

        return result.stdout

    except FileNotFoundError:
        print("Gitleaks is not installed.")
        return "[]"

    except Exception as e:
        print(e)
        return "[]"