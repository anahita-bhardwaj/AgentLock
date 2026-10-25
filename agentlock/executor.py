
import subprocess

from agentlock.validator import validate_command


def execute(args: list[str]) -> subprocess.CompletedProcess[str]:
    """Validate and execute a program without invoking a shell."""
    validate_command(args)

    return subprocess.run(
        args,
        shell=False,
        capture_output=True,
        text=True,
        check=False,
    )
