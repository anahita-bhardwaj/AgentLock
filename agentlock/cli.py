import typer

from agentlock.executor import execute
from agentlock.policy import Decision
from agentlock.policy_loader import load_policy

app = typer.Typer()


@app.callback()
def main():
    """AgentLock - a security sandbox for AI agents."""
    pass


@app.command()
def version():
    """Show the AgentLock version."""
    typer.echo("AgentLock v0.1.0")



@app.command()
def run(command: list[str] = typer.Argument(..., help="Program and its arguments")):
    """Run a command inside AgentLock."""
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

if __name__ == "__main__":
    app()