"""Tests for the ``matcha info`` command."""

import json

from click.testing import CliRunner

from matcha.cli import cli
from matcha.commands.info_cmd import (
    _ATTACK_DETAILS,
    _format_json,
    _format_text,
    get_attack_names,
    lookup_attack,
)
from matcha.commands.list_cmd import CATEGORIES


# ---------------------------------------------------------------------------
# Registry integrity
# ---------------------------------------------------------------------------

def test_all_catalog_attacks_have_details():
    """Every attack in the list catalog must have a detail entry."""
    for cat in CATEGORIES:
        for atk in cat["attacks"]:
            detail = lookup_attack(atk["name"])
            assert detail is not None, f"Missing detail for {atk['name']}"


def test_detail_count_matches_catalog():
    """The detail registry must cover exactly the same attacks as the catalog."""
    catalog_names = {atk["name"] for cat in CATEGORIES for atk in cat["attacks"]}
    detail_names = set(_ATTACK_DETAILS.keys())
    assert detail_names == catalog_names


def test_categories_match_catalog():
    """The category in each detail entry must match the catalog grouping."""
    catalog_map = {}
    for cat in CATEGORIES:
        for atk in cat["attacks"]:
            catalog_map[atk["name"]] = cat["category"]
    for name, detail in _ATTACK_DETAILS.items():
        assert detail["category"] == catalog_map[name], (
            f"{name} category mismatch: {detail['category']} != {catalog_map[name]}"
        )


def test_get_attack_names_sorted():
    """get_attack_names() must return a sorted list."""
    names = get_attack_names()
    assert names == sorted(names)


def test_lookup_known_attack():
    """lookup_attack should return a dict for a known attack."""
    detail = lookup_attack("syn-flood")
    assert detail is not None
    assert "description" in detail
    assert "category" in detail
    assert "parameters" in detail
    assert "example" in detail


def test_lookup_unknown_attack():
    """lookup_attack should return None for an unknown attack."""
    assert lookup_attack("nonexistent-attack") is None


def test_detail_entries_have_required_keys():
    """Every detail entry must include description, category, parameters, example."""
    for name, detail in _ATTACK_DETAILS.items():
        for key in ("description", "category", "parameters", "example"):
            assert key in detail, f"{name} is missing key {key!r}"


def test_parameter_entries_have_required_keys():
    """Each parameter in every detail entry must include the expected keys."""
    for name, detail in _ATTACK_DETAILS.items():
        for param in detail["parameters"]:
            for key in ("name", "type", "default", "required", "help"):
                assert key in param, (
                    f"{name} parameter {param.get('name', '?')} missing key {key!r}"
                )


# ---------------------------------------------------------------------------
# Text output
# ---------------------------------------------------------------------------

def test_format_text_contains_name():
    """Text output should include the attack name."""
    text = _format_text("syn-flood", _ATTACK_DETAILS["syn-flood"])
    assert "syn-flood" in text


def test_format_text_contains_category():
    """Text output should include the category."""
    text = _format_text("syn-flood", _ATTACK_DETAILS["syn-flood"])
    assert "Network-layer" in text


def test_format_text_contains_description():
    """Text output should include the description."""
    text = _format_text("syn-flood", _ATTACK_DETAILS["syn-flood"])
    assert "SYN flood" in text


def test_format_text_contains_parameters_section():
    """Text output should have a Parameters: header."""
    text = _format_text("syn-flood", _ATTACK_DETAILS["syn-flood"])
    assert "Parameters:" in text


def test_format_text_contains_example():
    """Text output should include the example."""
    text = _format_text("syn-flood", _ATTACK_DETAILS["syn-flood"])
    assert "Example:" in text
    assert "matcha run syn-flood" in text


def test_format_text_shows_required_and_optional():
    """Text output should label parameters as required or optional."""
    text = _format_text("syn-flood", _ATTACK_DETAILS["syn-flood"])
    assert "required" in text
    assert "optional" in text


# ---------------------------------------------------------------------------
# JSON output
# ---------------------------------------------------------------------------

def test_format_json_valid():
    """JSON output must be valid JSON."""
    raw = _format_json("syn-flood", _ATTACK_DETAILS["syn-flood"])
    payload = json.loads(raw)
    assert isinstance(payload, dict)


def test_format_json_contains_expected_keys():
    """JSON output must include name, category, description, parameters, example."""
    payload = json.loads(_format_json("syn-flood", _ATTACK_DETAILS["syn-flood"]))
    for key in ("name", "category", "description", "parameters", "example"):
        assert key in payload


def test_format_json_name_matches():
    """JSON output name field must match the requested attack."""
    payload = json.loads(_format_json("syn-flood", _ATTACK_DETAILS["syn-flood"]))
    assert payload["name"] == "syn-flood"


def test_format_json_parameters_is_list():
    """JSON output parameters field must be a list."""
    payload = json.loads(_format_json("syn-flood", _ATTACK_DETAILS["syn-flood"]))
    assert isinstance(payload["parameters"], list)
    assert len(payload["parameters"]) > 0


# ---------------------------------------------------------------------------
# CLI integration via Click CliRunner
# ---------------------------------------------------------------------------

def test_cli_info_syn_flood_text():
    """``matcha info syn-flood`` should print detailed info in text mode."""
    runner = CliRunner()
    result = runner.invoke(cli, ["info", "syn-flood"])
    assert result.exit_code == 0
    assert "syn-flood" in result.output
    assert "Network-layer" in result.output
    assert "Parameters:" in result.output
    assert "Example:" in result.output


def test_cli_info_syn_flood_json():
    """``matcha -o json info syn-flood`` should output valid JSON."""
    runner = CliRunner()
    result = runner.invoke(cli, ["-o", "json", "info", "syn-flood"])
    assert result.exit_code == 0
    payload = json.loads(result.output)
    assert payload["name"] == "syn-flood"
    assert payload["category"] == "Network-layer"
    assert "parameters" in payload


def test_cli_info_json_long_flag():
    """``matcha --output json info syn-flood`` should also work."""
    runner = CliRunner()
    result = runner.invoke(cli, ["--output", "json", "info", "syn-flood"])
    assert result.exit_code == 0
    payload = json.loads(result.output)
    assert payload["name"] == "syn-flood"


def test_cli_info_unknown_attack():
    """``matcha info unknown-attack`` should fail with exit code 2."""
    runner = CliRunner()
    result = runner.invoke(cli, ["info", "unknown-attack"])
    assert result.exit_code == 2


def test_cli_info_unknown_attack_error_message():
    """Error message for unknown attack should mention 'unknown attack'."""
    runner = CliRunner()
    result = runner.invoke(cli, ["info", "unknown-attack"])
    assert "unknown attack" in result.output.lower() or "unknown attack" in (result.output + getattr(result, 'stderr', '')).lower()


def test_cli_info_pcap_replay():
    """``matcha info pcap-replay`` should show replay category."""
    runner = CliRunner()
    result = runner.invoke(cli, ["info", "pcap-replay"])
    assert result.exit_code == 0
    assert "Replay" in result.output


def test_cli_info_application_layer_attack():
    """``matcha info slowloris`` should show application-layer info."""
    runner = CliRunner()
    result = runner.invoke(cli, ["info", "slowloris"])
    assert result.exit_code == 0
    assert "Application-layer" in result.output
    assert "slowloris" in result.output.lower()


def test_cli_info_help():
    """``matcha info --help`` should show help text."""
    runner = CliRunner()
    result = runner.invoke(cli, ["info", "--help"])
    assert result.exit_code == 0
    assert "Show detailed information" in result.output


def test_cli_help_shows_info():
    """``matcha --help`` should mention the info subcommand."""
    runner = CliRunner()
    result = runner.invoke(cli, ["--help"])
    assert result.exit_code == 0
    assert "info" in result.output
