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
    assert "--target-ip" in result.output
    assert "--target-port" in result.output


def test_syn_flood_missing_required_args():
    """``matcha syn-flood`` without required args exits with code 2."""
    runner = CliRunner()
    result = runner.invoke(cli, ["syn-flood"])
    assert result.exit_code == 2


# ---------------------------------------------------------------------------
# Network-layer attack command smoke tests
# ---------------------------------------------------------------------------

NETWORK_ATTACKS = [
    "arp-spoof",
    "bgp-hijacking",
    "dhcp-starvation",
    "dns-amplification",
    "icmp-flood",
    "mac-flooding",
    "mitm",
    "ntp-amplification",
    "ping-of-death",
    "smurf-attack",
    "syn-flood",
    "udp-flood",
]


def test_all_network_attacks_registered_as_subcommands():
    """Every network-layer attack must appear as a CLI subcommand."""
    runner = CliRunner()
    result = runner.invoke(cli, ["--help"])
    assert result.exit_code == 0
    for name in NETWORK_ATTACKS:
        assert name in result.output, f"{name} not found in CLI help output"


def test_network_attack_help_exits_zero():
    """``matcha <attack> --help`` exits 0 for every network-layer attack."""
    runner = CliRunner()
    for name in NETWORK_ATTACKS:
        result = runner.invoke(cli, [name, "--help"])
        assert result.exit_code == 0, f"{name} --help exited with {result.exit_code}"


def test_network_attacks_missing_required_args():
    """Network attacks with required args should exit 2 when called bare."""
    runner = CliRunner()
    for name in NETWORK_ATTACKS:
        result = runner.invoke(cli, [name])
        assert result.exit_code == 2, (
            f"{name} should exit 2 without required args, got {result.exit_code}"
        )


# ---------------------------------------------------------------------------
# Application-layer attack command smoke tests
# ---------------------------------------------------------------------------

APPLICATION_ATTACKS = [
    "credential-harvester",
    "directory-traversal",
    "ftp-brute-force",
    "http-dos",
    "http-flood",
    "rdp-brute-force",
    "slowloris",
    "sql-injection",
    "ssh-brute-force",
    "ssl-strip",
    "vlan-hopping",
    "xss",
    "xxe",
]


def test_all_application_attacks_registered_as_subcommands():
    """Every application-layer attack must appear as a CLI subcommand."""
    runner = CliRunner()
    result = runner.invoke(cli, ["--help"])
    assert result.exit_code == 0
    for name in APPLICATION_ATTACKS:
        assert name in result.output, f"{name} not found in CLI help output"


def test_application_attack_help_exits_zero():
    """``matcha <attack> --help`` exits 0 for every application-layer attack."""
    runner = CliRunner()
    for name in APPLICATION_ATTACKS:
        result = runner.invoke(cli, [name, "--help"])
        assert result.exit_code == 0, f"{name} --help exited with {result.exit_code}"


def test_application_attacks_missing_required_args():
    """Application attacks with required args should exit 2 when called bare."""
    runner = CliRunner()
    for name in APPLICATION_ATTACKS:
        result = runner.invoke(cli, [name])
        assert result.exit_code == 2, (
            f"{name} should exit 2 without required args, got {result.exit_code}"
        )
