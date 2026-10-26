
from pathlib import Path


def read_file(path: str, workspace: Path) -> str:
    """Read a file contained within the designated workspace."""
    workspace = workspace.resolve()
    requested_path = Path(path)

    if not requested_path.is_absolute():
        requested_path = workspace / requested_path

    resolved_path = requested_path.resolve()

    try:
        resolved_path.relative_to(workspace)
    except ValueError as exc:
        raise ValueError("File path must remain inside the workspace.") from exc

    if not resolved_path.is_file():
        raise ValueError("Requested path is not a regular file.")

    return resolved_path.read_text(encoding="utf-8")
