"""matcha CLI entry point."""

import click

from matcha import __version__


@click.group()
@click.version_option(version=__version__, prog_name="matcha")
def cli():
    """matcha - MMT Attack Toolkit CLI."""


if __name__ == "__main__":
    cli()
