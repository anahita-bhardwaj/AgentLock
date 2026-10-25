import pytest

from agentlock.executor import execute


def test_execute_success():
    result = execute(["cmd", "/c", "echo", "hello"])

    assert result.returncode == 0
    assert "hello" in result.stdout


def test_execute_failure():
    with pytest.raises(FileNotFoundError):
        execute(["this-agentlock-command-should-not-exist-12345"])
