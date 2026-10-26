import typer

from agentlock.executor import execute
from agentlock.policy import Decision
from agentlock.policy_loader import load_policy
from pathlib import Path
from agentlock.file_operations import read_file

app = typer.Typer()



def require_allowed_action(action: str) -> None:
    """Exit unless the policy explicitly allows the action."""
    policy_path = (
        Path(__file__).resolve().parent.parent
        / "policies"
        / "default.yaml"
    )
    policy = load_policy(str(policy_path))
    decision = policy.evaluate(action)

    typer.echo(f"{action}: {decision.value}")

    if decision != Decision.ALLOW:
        if decision == Decision.ASK:
            typer.echo(
                "Execution blocked: this action requires approval, "
                "but approval is not implemented yet.",
                err=True,
            )
        else:
            typer.echo("Execution blocked by policy.", err=True)

        raise typer.Exit(code=1)



@app.callback()
def main():
    """AgentLock - a security sandbox for AI agents."""
    pass


@app.command()
def version():
    """Show the AgentLock version."""
    typer.echo("AgentLock v0.1.0")




@app.command()
def run(
    action: str,
    command: list[str] = typer.Argument(
        ...,
        help="Program and its arguments",
    ),
):
    """Check policy, then run a command if allowed."""
    require_allowed_action(action)
    result = execute(command)

    if result.stdout:
        typer.echo(result.stdout, nl=False)

    if result.stderr:
        typer.echo(result.stderr, err=True, nl=False)

    raise typer.Exit(code=result.returncode)



@app.command()
def check(action: str):
    """Check the policy decision for an action."""
    policy = load_policy("policies/default.yaml")
    decision = policy.evaluate(action)

    typer.echo(f"{action}: {decision.value}")

    if decision == Decision.DENY:
        raise typer.Exit(code=1)


@app.command("read-file")
def read_file_command(path: str):
    """Read a file within the AgentLock workspace if policy allows."""
    require_allowed_action("read_file")

    workspace = Path.cwd()
    try:
        content = read_file(path, workspace)
    except (ValueError, OSError, UnicodeError) as exc:
        typer.echo(f"File read failed: {exc}", err=True)
        raise typer.Exit(code=1) from exc

    typer.echo(content, nl=False)


if __name__ == "__main__":
    app()