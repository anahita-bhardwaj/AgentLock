
from typer.testing import CliRunner

from agentlock.cli import app


runner = CliRunner()


def test_check_allows_permitted_action():
    result = runner.invoke(app, ["check", "read_file"])

    assert result.exit_code == 0
    assert "read_file: allow" in result.stdout


def test_check_denies_forbidden_action():
    result = runner.invoke(app, ["check", "write_file"])

    assert result.exit_code == 1
    assert "write_file: deny" in result.stdout


def test_check_reports_approval_required_action():
    result = runner.invoke(app, ["check", "network_access"])

    assert result.exit_code == 0
    assert "network_access: ask" in result.stdout


def test_check_denies_unknown_action():
    result = runner.invoke(app, ["check", "unknown_action"])

    assert result.exit_code == 1
    assert "unknown_action: deny" in result.stdout



def test_run_blocks_denied_action():
    result = runner.invoke(
        app,
        ["run", "write_file", "--", "cmd", "/c", "echo", "should-not-run"],
    )

    assert result.exit_code == 1
    assert "write_file: deny" in result.stdout
    assert "should-not-run" not in result.stdout


def test_run_blocks_action_requiring_approval():
    result = runner.invoke(
        app,
        ["run", "network_access", "--", "cmd", "/c", "echo", "should-not-run"],
    )

    assert result.exit_code == 1
    assert "network_access: ask" in result.stdout
    assert "approval is not implemented" in result.stderr
    assert "should-not-run" not in result.stdout


def test_run_executes_allowed_action():
    result = runner.invoke(
        app,
        ["run", "read_file", "--", "cmd", "/c", "echo", "hello"],
    )

    assert result.exit_code == 0
    assert "read_file: allow" in result.stdout
    assert "hello" in result.stdout
