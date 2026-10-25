
import subprocess


def execute(args: list[str]) -> subprocess.CompletedProcess[str]:
    """Execute a program with arguments without invoking a shell."""
    if not args or not all(isinstance(arg, str) for arg in args):
        raise ValueError("args must be a non-empty list of strings.")

    if not args[0].strip():
        raise ValueError("The executable name cannot be empty.")

    return subprocess.run(
        args,
        shell=False,
        capture_output=True,
        text=True,
        check=False,
    )
