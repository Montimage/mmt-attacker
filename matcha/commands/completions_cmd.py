"""``matcha completions`` command -- print shell completion activation scripts."""

from __future__ import annotations

import click

_SHELLS = {
    "bash": 'eval "$(_MATCHA_COMPLETE=bash_source matcha)"',
    "zsh": 'eval "$(_MATCHA_COMPLETE=zsh_source matcha)"',
    "fish": "_MATCHA_COMPLETE=fish_source matcha | source",
}


@click.command("completions")
@click.argument("shell", type=click.Choice(sorted(_SHELLS), case_sensitive=False))
def completions_cmd(shell: str) -> None:
    """Print shell completion activation command.

    Supported shells: bash, zsh, fish.

    Add the printed command to your shell profile to enable tab-completion
    for matcha.
    """
    click.echo(_SHELLS[shell])
