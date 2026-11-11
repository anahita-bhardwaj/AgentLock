
from pathlib import Path

import pytest

from agentlock.file_writer import write_file


def test_write_file_inside_workspace(tmp_path: Path):
    write_file("hello.txt", "Hello, AgentLock!", tmp_path)

    result = tmp_path / "hello.txt"
    assert result.read_text(encoding="utf-8") == "Hello, AgentLock!"


def test_write_file_rejects_path_outside_workspace(tmp_path: Path):
    workspace = tmp_path / "workspace"
    workspace.mkdir()

    with pytest.raises(ValueError, match="inside the workspace"):
        write_file("../outside.txt", "Should not be written", workspace)

    assert not (tmp_path / "outside.txt").exists()


def test_write_file_rejects_directory(tmp_path: Path):
    directory = tmp_path / "folder"
    directory.mkdir()

    with pytest.raises(ValueError, match="regular file"):
        write_file("folder", "Should not be written", tmp_path)


def test_write_file_overwrites_existing_file(tmp_path: Path):
    test_file = tmp_path / "hello.txt"
    test_file.write_text("Original content", encoding="utf-8")

    write_file("hello.txt", "Updated content", tmp_path)

    assert test_file.read_text(encoding="utf-8") == "Updated content"


def test_write_file_rejects_relative_path_traversal(tmp_path):
    workspace = tmp_path / "workspace"
    workspace.mkdir()

    outside_file = tmp_path / "outside.txt"

    with pytest.raises(ValueError, match="inside the workspace"):
        write_file("../outside.txt", "malicious content", workspace)

    assert not outside_file.exists()

def test_write_file_rejects_symlink_outside_workspace(tmp_path):
    workspace = tmp_path / "workspace"
    workspace.mkdir()

    outside_file = tmp_path / "outside.txt"
    outside_file.write_text("original content", encoding="utf-8")

    link = workspace / "link.txt"

    try:
        link.symlink_to(outside_file)
    except (OSError, NotImplementedError):
        pytest.skip("Symlinks are not supported on this system.")

    with pytest.raises(ValueError, match="Symbolic links are not allowed"):
        write_file("link.txt", "malicious content", workspace)

    assert outside_file.read_text(encoding="utf-8") == "original content"


def test_write_file_rejects_symlinked_parent_directory(tmp_path):
    workspace = tmp_path / "workspace"
    workspace.mkdir()

    outside_dir = tmp_path / "outside"
    outside_dir.mkdir()

    outside_file = outside_dir / "secret.txt"
    outside_file.write_text("original content", encoding="utf-8")

    link = workspace / "linked_dir"

    try:
        link.symlink_to(outside_dir, target_is_directory=True)
    except (OSError, NotImplementedError):
        pytest.skip("Symlinks are not supported on this system.")

    with pytest.raises(ValueError, match="Symbolic links are not allowed"):
        write_file(
            "linked_dir/secret.txt",
            "malicious content",
            workspace,
        )

    assert outside_file.read_text(encoding="utf-8") == "original content"


def test_write_file_rejects_absolute_path_outside_workspace(tmp_path):
    workspace = tmp_path / "workspace"
    workspace.mkdir()

    outside_file = tmp_path / "outside.txt"

    with pytest.raises(ValueError, match="inside the workspace"):
        write_file(
            str(outside_file),
            "malicious content",
            workspace,
        )

    assert not outside_file.exists()
