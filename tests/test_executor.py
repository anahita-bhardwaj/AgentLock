from agentlock.executor import execute


def test_execute_success():
    result = execute("echo hello")

    assert result.returncode == 0
    assert "hello" in result.stdout


def test_execute_failure():
    result = execute("this-command-does-not-exist")

    assert result.returncode != 0
    assert result.stderr