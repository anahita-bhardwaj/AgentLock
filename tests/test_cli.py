
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


def test_read_file_command_reads_file_in_workspace(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    test_file = tmp_path / "hello.txt"
    test_file.write_text("Hello from AgentLock!", encoding="utf-8")

    result = runner.invoke(app, ["read-file", "hello.txt"])

    assert result.exit_code == 0
    assert "read_file: allow" in result.stdout
    assert "Hello from AgentLock!" in result.stdout


def test_read_file_command_blocks_path_outside_workspace(
    tmp_path, monkeypatch
):
    workspace = tmp_path / "workspace"
    workspace.mkdir()

    outside_file = tmp_path / "outside.txt"
    outside_file.write_text("Secret outside content", encoding="utf-8")

    monkeypatch.chdir(workspace)

    result = runner.invoke(app, ["read-file", "../outside.txt"])

    assert result.exit_code == 1
    assert "read_file: allow" in result.stdout
    assert "must remain inside the workspace" in result.stderr
    assert "Secret outside content" not in result.stdout
