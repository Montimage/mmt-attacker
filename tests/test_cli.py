"""Smoke tests for the matcha CLI."""

from click.testing import CliRunner

from matcha import __version__
from matcha.cli import cli


def test_version():
    runner = CliRunner()
    result = runner.invoke(cli, ["--version"])
    assert result.exit_code == 0
    assert __version__ in result.output


def test_help():
    runner = CliRunner()
    result = runner.invoke(cli, ["--help"])
    assert result.exit_code == 0
    assert "matcha" in result.output.lower()
