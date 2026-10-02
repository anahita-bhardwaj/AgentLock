import typer

from agentlock.executor import execute

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
def run(command: str):
    """Run a command inside AgentLock."""
    result = execute(command)

    if result.stdout:
        typer.echo(result.stdout, nl=False)

    if result.stderr:
        typer.echo(result.stderr, err=True, nl=False)

    raise typer.Exit(code=result.returncode)


if __name__ == "__main__":
    app()