"""Tests for the ``matcha list`` command."""

import json

from click.testing import CliRunner

from matcha.cli import cli
from matcha.commands.list_cmd import (
    APPLICATION_LAYER,
    CATEGORIES,
    NETWORK_LAYER,
    REPLAY,
    _format_json,
    _format_text,
    _total_attacks,
)


# ---------------------------------------------------------------------------
# Catalog integrity
# ---------------------------------------------------------------------------

def test_total_attack_count():
    """The catalog must contain exactly 26 attacks."""
    assert _total_attacks() == 26


def test_network_layer_count():
    """Network-layer category should have 12 attacks."""
    assert len(NETWORK_LAYER) == 12


def test_application_layer_count():
    """Application-layer category should have 13 attacks."""
    assert len(APPLICATION_LAYER) == 13


def test_replay_count():
    """Replay category should have 1 attack."""
    assert len(REPLAY) == 1


def test_no_duplicate_names():
    """Attack names must be unique across all categories."""
    all_names = [
        atk["name"] for cat in CATEGORIES for atk in cat["attacks"]
    ]
    assert len(all_names) == len(set(all_names))


# ---------------------------------------------------------------------------
# Text output
# ---------------------------------------------------------------------------

def test_format_text_contains_categories():
    """Text output should include each category header."""
    text = _format_text()
    assert "Network-layer" in text
    assert "Application-layer" in text
    assert "Replay" in text


def test_format_text_contains_total():
    """Text output should show the total attack count."""
    text = _format_text()
    assert "Total: 26 attacks" in text


def test_format_text_contains_all_attacks():
    """Every attack name must appear in the text output."""
    text = _format_text()
    for cat in CATEGORIES:
        for atk in cat["attacks"]:
            assert atk["name"] in text


# ---------------------------------------------------------------------------
# JSON output
# ---------------------------------------------------------------------------

def test_format_json_valid():
    """JSON output must be valid JSON."""
    raw = _format_json()
    payload = json.loads(raw)
    assert isinstance(payload, list)


def test_format_json_count():
    """JSON output should have exactly 26 entries."""
    payload = json.loads(_format_json())
    assert len(payload) == 26


def test_format_json_entry_keys():
    """Each JSON entry must have name, category, and description."""
    payload = json.loads(_format_json())
    for entry in payload:
        assert "name" in entry
        assert "category" in entry
        assert "description" in entry


def test_format_json_categories():
    """JSON entries should only belong to known categories."""
    allowed = {"Network-layer", "Application-layer", "Replay"}
    payload = json.loads(_format_json())
    for entry in payload:
        assert entry["category"] in allowed


# ---------------------------------------------------------------------------
# CLI integration via Click CliRunner
# ---------------------------------------------------------------------------

def test_cli_list_text():
    """``matcha list`` should print categorized text output."""
    runner = CliRunner()
    result = runner.invoke(cli, ["list"])
    assert result.exit_code == 0
    assert "Network-layer" in result.output
    assert "Application-layer" in result.output
    assert "Replay" in result.output
    assert "Total: 26 attacks" in result.output


def test_cli_list_json():
    """``matcha -o json list`` should print valid JSON array."""
    runner = CliRunner()
    result = runner.invoke(cli, ["-o", "json", "list"])
    assert result.exit_code == 0
    payload = json.loads(result.output)
    assert isinstance(payload, list)
    assert len(payload) == 26


def test_cli_list_json_long_flag():
    """``matcha --output json list`` should also work."""
    runner = CliRunner()
    result = runner.invoke(cli, ["--output", "json", "list"])
    assert result.exit_code == 0
    payload = json.loads(result.output)
    assert len(payload) == 26


def test_cli_list_help():
    """``matcha list --help`` should show help text."""
    runner = CliRunner()
    result = runner.invoke(cli, ["list", "--help"])
    assert result.exit_code == 0
    assert "List all available attacks" in result.output


def test_cli_help_shows_list():
    """``matcha --help`` should mention the list subcommand."""
    runner = CliRunner()
    result = runner.invoke(cli, ["--help"])
    assert result.exit_code == 0
    assert "list" in result.output
