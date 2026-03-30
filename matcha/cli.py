"""matcha CLI entry point."""

import logging
import os
import sys

import click

from matcha import __version__


@click.group(invoke_without_command=True)
@click.version_option(version=__version__, prog_name="matcha")
@click.option("-v", "--verbose", is_flag=True, default=False, help="Enable debug logging.")
@click.option(
    "-o",
    "--output",
    type=click.Choice(["text", "json"], case_sensitive=False),
    default="text",
    help="Output format (default: text).",
)
@click.option(
    "--no-color",
    is_flag=True,
    default=False,
    help="Disable colored output.",
)
@click.pass_context
def cli(ctx, verbose, output, no_color):
    """matcha - MMT Attack Toolkit CLI."""
    ctx.ensure_object(dict)
    ctx.obj["verbose"] = verbose
    ctx.obj["output"] = output

    # Honour --no-color flag and NO_COLOR env var (see https://no-color.org/)
    if no_color or os.environ.get("NO_COLOR", "") != "":
        ctx.color = False
    ctx.obj["no_color"] = no_color or os.environ.get("NO_COLOR", "") != ""

    # Configure logging: messages go to stderr so stdout stays clean for
    # structured output.
    log_level = logging.DEBUG if verbose else logging.WARNING
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)
    if not root_logger.handlers:
        handler = logging.StreamHandler(sys.stderr)
        handler.setFormatter(logging.Formatter("%(levelname)s: %(message)s"))
        root_logger.addHandler(handler)

    if ctx.invoked_subcommand is None:
        click.echo(ctx.get_help())


if __name__ == "__main__":
    cli()
