
def validate_command(args: list[str]) -> None:
    """Reject malformed command argument lists before execution."""
    if not isinstance(args, list) or not args:
        raise ValueError("Command must be a non-empty list of strings.")

    if not all(isinstance(arg, str) for arg in args):
        raise ValueError("Every command argument must be a string.")

    if not args[0].strip():
        raise ValueError("The executable name cannot be empty.")
