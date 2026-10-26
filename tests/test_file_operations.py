
from pathlib import Path

import pytest

from agentlock.file_operations import read_file


def test_read_file_inside_workspace(tmp_path: Path):
    test_file = tmp_path / "hello.txt"
    test_file.write_text("Hello, AgentLock!", encoding="utf-8")

    result = read_file("hello.txt", tmp_path)

    assert result == "Hello, AgentLock!"


def test_read_file_rejects_path_outside_workspace(tmp_path: Path):
    workspace = tmp_path / "workspace"
    workspace.mkdir()

    outside_file = tmp_path / "outside.txt"
    outside_file.write_text("This should not be read.", encoding="utf-8")

    with pytest.raises(ValueError, match="inside the workspace"):
        read_file("../outside.txt", workspace)


def test_read_file_rejects_missing_file(tmp_path: Path):
    with pytest.raises(ValueError, match="regular file"):
        read_file("missing.txt", tmp_path)


def test_read_file_rejects_directory(tmp_path: Path):
    directory = tmp_path / "folder"
    directory.mkdir()

    with pytest.raises(ValueError, match="regular file"):
        read_file("folder", tmp_path)
