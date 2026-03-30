"""matcha CLI entry point."""

import logging
import os
import sys

import click

from matcha import __version__
from matcha.commands.info_cmd import info_cmd
from matcha.commands.list_cmd import list_cmd
from matcha.commands.syn_flood_cmd import syn_flood_cmd


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
    color_disabled = no_color or os.environ.get("NO_COLOR", "") != ""
    if color_disabled:
        ctx.color = False
    ctx.obj["no_color"] = color_disabled

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


cli.add_command(info_cmd)
cli.add_command(list_cmd)
cli.add_command(syn_flood_cmd)


if __name__ == "__main__":
    cli()
