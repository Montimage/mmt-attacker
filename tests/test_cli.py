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


def test_no_args():
    """Invoking bare matcha with no arguments should display group help."""
    runner = CliRunner()
    result = runner.invoke(cli, [])
    assert result.exit_code == 0 or result.exit_code == 2
    assert "usage" in result.output.lower() or "matcha" in result.output.lower()
