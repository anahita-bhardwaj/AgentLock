import pytest

from agentlock.executor import execute


def test_execute_success():
    result = execute(["cmd", "/c", "echo", "hello"])

    assert result.returncode == 0
    assert "hello" in result.stdout


def test_execute_failure():
    with pytest.raises(FileNotFoundError):
        execute(["this-agentlock-command-should-not-exist-12345"])


def test_execute_rejects_empty_arguments():
    with pytest.raises(ValueError, match="non-empty list"):
        execute([])


def test_execute_rejects_non_string_argument():
    with pytest.raises(ValueError, match="Every command argument"):
        execute(["cmd", 123])


def test_execute_rejects_blank_executable():
    with pytest.raises(ValueError, match="executable name"):
        execute(["   ", "hello"])
