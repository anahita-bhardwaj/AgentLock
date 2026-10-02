import subprocess


def execute(command: str) -> subprocess.CompletedProcess[str]:
    """Execute a command and return the completed process."""
    return subprocess.run(
        command,
        shell=True,
        capture_output=True,
        text=True,
    )