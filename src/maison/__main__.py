"""Command-line interface."""

import typer


app: typer.Typer = typer.Typer()


@app.command(name="maison")
def main() -> None:
    """Maison."""


if __name__ == "__main__":
    app()  # pragma: no cover
