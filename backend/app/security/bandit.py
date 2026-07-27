import subprocess


def run_bandit(paths: list[str]):

    findings = []

    for path in paths:

        command = [
            "bandit",
            "-r",
            "-f",
            "json",
            "--",
            path
        ]

        print("Running:", command)

        result = subprocess.run(
            command,
            capture_output=True,
            text=True
        )

        print("Return Code:", result.returncode)
        print("STDOUT:\n", result.stdout)
        print("STDERR:\n", result.stderr)

        if result.returncode not in (0, 1):
            raise RuntimeError(result.stderr)

        findings.append(result.stdout)

    return findings