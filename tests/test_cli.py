"""Smoke tests for the matcha CLI."""

import logging

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
    assert result.exit_code == 0
    assert "matcha" in result.output.lower()


def test_help_shows_global_options():
    """--help output must list all global options."""
    runner = CliRunner()
    result = runner.invoke(cli, ["--help"])
    assert result.exit_code == 0
    for flag in ["--verbose", "--output", "--no-color", "--version", "--help"]:
        assert flag in result.output


def test_verbose_sets_debug_logging():
    """-v flag should set root logger to DEBUG."""
    runner = CliRunner()
    result = runner.invoke(cli, ["-v"])
    assert result.exit_code == 0
    root_level = logging.getLogger().level
    assert root_level == logging.DEBUG


def test_output_default_is_text():
    """Default output format should be text."""
    obj = {}
    runner = CliRunner()
    result = runner.invoke(cli, [], obj=obj)
    assert result.exit_code == 0
    assert obj.get("output") == "text"


def test_output_json():
    """--output json should be accepted."""
    runner = CliRunner()
    result = runner.invoke(cli, ["--output", "json"])
    assert result.exit_code == 0


def test_output_invalid_choice():
    """Invalid --output value should fail."""
    runner = CliRunner()
    result = runner.invoke(cli, ["--output", "xml"])
    assert result.exit_code != 0


def test_no_color_flag():
    """--no-color flag should be accepted and respected."""
    obj = {}
    runner = CliRunner()
    result = runner.invoke(cli, ["--no-color"], obj=obj)
    assert result.exit_code == 0
    assert obj.get("no_color") is True


def test_no_color_env_var():
    """NO_COLOR env var should disable color."""
    obj = {}
    runner = CliRunner(env={"NO_COLOR": "1"})
    result = runner.invoke(cli, [], obj=obj)
    assert result.exit_code == 0
    assert obj.get("no_color") is True


# ---------------------------------------------------------------------------
# Subcommand smoke tests
# ---------------------------------------------------------------------------


def test_list_exits_zero_and_contains_attacks():
    """``matcha list`` exits 0 and output contains attack names."""
    runner = CliRunner()
    result = runner.invoke(cli, ["list"])
    assert result.exit_code == 0
    # Must contain at least a few well-known attack names
    assert "syn-flood" in result.output
    assert "arp-spoof" in result.output
    assert "slowloris" in result.output


def test_syn_flood_help_exits_zero_and_shows_options():
    """``matcha syn-flood --help`` exits 0 and shows required options."""
    runner = CliRunner()
    result = runner.invoke(cli, ["syn-flood", "--help"])
    assert result.exit_code == 0
    assert "--target" in result.output
    assert "--ports" in result.output


def test_syn_flood_missing_required_args():
    """``matcha syn-flood`` without required args exits with code 2."""
    runner = CliRunner()
    result = runner.invoke(cli, ["syn-flood"])
    assert result.exit_code == 2
