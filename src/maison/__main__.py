"""Command-line interface."""
import click


@click.command()
@click.version_option()
def main() -> None:
    """Maison."""


if __name__ == "__main__":
    main(prog_name="maison")  # pragma: no cover
