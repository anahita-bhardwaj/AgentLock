
from pathlib import Path


def write_file(path: str, content: str, workspace: Path) -> None:
    """Write text to a file contained within the designated workspace."""
    workspace = workspace.resolve()
    requested_path = Path(path)

    if not requested_path.is_absolute():
        requested_path = workspace / requested_path

    resolved_path = requested_path.resolve()

    try:
        resolved_path.relative_to(workspace)
    except ValueError as exc:
        raise ValueError("File path must remain inside the workspace.") from exc

    if resolved_path.exists() and not resolved_path.is_file():
        raise ValueError("Requested path is not a regular file.")

    resolved_path.write_text(content, encoding="utf-8")
