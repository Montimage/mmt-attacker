"""End-to-end tests for the matcha CLI.

These tests invoke the installed ``matcha`` binary via subprocess to verify
the full install-and-run path works on Linux and macOS.
"""

import json
import subprocess
import sys

import pytest

pytestmark = pytest.mark.e2e

TIMEOUT = 30


def run_matcha(*args: str) -> subprocess.CompletedProcess:
    """Run ``matcha`` as a subprocess and return the result."""
    return subprocess.run(
        [sys.executable, "-m", "matcha", *args],
        capture_output=True,
        text=True,
        timeout=TIMEOUT,
    )


# ---------------------------------------------------------------------------
# Installation & entry point
# ---------------------------------------------------------------------------


class TestInstallation:
    def test_module_entry_point(self):
        """``python -m matcha`` exits 0."""
        result = run_matcha()
        assert result.returncode == 0

    def test_version_output(self):
        """``matcha --version`` prints a version string."""
        result = run_matcha("--version")
        assert result.returncode == 0
        assert "version" in result.stdout.lower() or "." in result.stdout

    def test_help_output(self):
        """``matcha --help`` shows usage and global options."""
        result = run_matcha("--help")
        assert result.returncode == 0
        assert "--verbose" in result.stdout
        assert "--output" in result.stdout
        assert "--no-color" in result.stdout


# ---------------------------------------------------------------------------
# List command
# ---------------------------------------------------------------------------


class TestListCommand:
    def test_list_text(self):
        """``matcha list`` shows all attack categories in text mode."""
        result = run_matcha("list")
        assert result.returncode == 0
        assert "Network-layer" in result.stdout
        assert "Application-layer" in result.stdout
        assert "Replay" in result.stdout

    def test_list_json(self):
        """``matcha -o json list`` returns a valid JSON array."""
        result = run_matcha("-o", "json", "list")
        assert result.returncode == 0
        data = json.loads(result.stdout)
        assert isinstance(data, list)
        assert len(data) == 26
        names = {entry["name"] for entry in data}
        assert "syn-flood" in names
        assert "http-dos" in names
        assert "pcap-replay" in names

    def test_list_attack_count(self):
        """``matcha list`` reports 26 total attacks."""
        result = run_matcha("list")
        assert result.returncode == 0
        assert "26" in result.stdout


# ---------------------------------------------------------------------------
# Info command
# ---------------------------------------------------------------------------


class TestInfoCommand:
    def test_info_known_attack(self):
        """``matcha info syn-flood`` shows attack details."""
        result = run_matcha("info", "syn-flood")
        assert result.returncode == 0
        assert "syn-flood" in result.stdout.lower()

    def test_info_json(self):
        """``matcha -o json info syn-flood`` returns valid JSON."""
        result = run_matcha("-o", "json", "info", "syn-flood")
        assert result.returncode == 0
        data = json.loads(result.stdout)
        assert data["name"] == "syn-flood"

    def test_info_unknown_attack(self):
        """``matcha info nonexistent`` fails with exit code 2."""
        result = run_matcha("info", "nonexistent")
        assert result.returncode == 2


# ---------------------------------------------------------------------------
# Completions command
# ---------------------------------------------------------------------------


class TestCompletions:
    @pytest.mark.parametrize("shell", ["bash", "zsh", "fish"])
    def test_completions_prints_activation(self, shell):
        """``matcha completions <shell>`` prints an activation command."""
        result = run_matcha("completions", shell)
        assert result.returncode == 0
        assert "_MATCHA_COMPLETE" in result.stdout

    def test_completions_invalid_shell(self):
        """``matcha completions powershell`` fails."""
        result = run_matcha("completions", "powershell")
        assert result.returncode == 2


# ---------------------------------------------------------------------------
# Attack commands (help & validation only -- no actual network I/O)
# ---------------------------------------------------------------------------


ALL_ATTACKS = [
    "arp-spoof",
    "bgp-hijacking",
    "credential-harvester",
    "dhcp-starvation",
    "directory-traversal",
    "dns-amplification",
    "ftp-brute-force",
    "http-dos",
    "http-flood",
    "icmp-flood",
    "mac-flooding",
    "mitm",
    "ntp-amplification",
    "pcap-replay",
    "ping-of-death",
    "rdp-brute-force",
    "slowloris",
    "smurf-attack",
    "sql-injection",
    "ssh-brute-force",
    "ssl-strip",
    "syn-flood",
    "udp-flood",
    "vlan-hopping",
    "xss",
    "xxe",
]

# Attacks that have at least one required parameter — running without args
# must exit 2 (validation error).  Attacks with all-optional params are
# excluded because they execute immediately and exit 0.
ATTACKS_WITH_REQUIRED_PARAMS = [
    a for a in ALL_ATTACKS if a not in ("credential-harvester", "ssl-strip", "bgp-hijacking")
]


class TestAttackCommands:
    @pytest.mark.parametrize("attack", ALL_ATTACKS)
    def test_help_exits_zero(self, attack):
        """``matcha <attack> --help`` exits 0 for every registered attack."""
        result = run_matcha(attack, "--help")
        assert result.returncode == 0, f"{attack} --help failed: {result.stderr}"

    @pytest.mark.parametrize("attack", ATTACKS_WITH_REQUIRED_PARAMS)
    def test_missing_args_exits_two(self, attack):
        """``matcha <attack>`` without required args exits 2."""
        result = run_matcha(attack)
        assert result.returncode == 2, (
            f"{attack} without args should exit 2, got {result.returncode}"
        )


# ---------------------------------------------------------------------------
# Global flags
# ---------------------------------------------------------------------------


class TestGlobalFlags:
    def test_verbose_flag(self):
        """``matcha -v list`` works with verbose."""
        result = run_matcha("-v", "list")
        assert result.returncode == 0

    def test_no_color_flag(self):
        """``matcha --no-color list`` works without color."""
        result = run_matcha("--no-color", "list")
        assert result.returncode == 0

    def test_json_output_flag(self):
        """``matcha -o json list`` returns valid JSON."""
        result = run_matcha("-o", "json", "list")
        assert result.returncode == 0
        data = json.loads(result.stdout)
        assert isinstance(data, list)

    def test_invalid_output_format(self):
        """``matcha -o xml`` fails."""
        result = run_matcha("-o", "xml")
        assert result.returncode != 0
