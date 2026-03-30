"""Tests for the ``matcha syn-flood`` command."""

from __future__ import annotations

import json
from unittest.mock import MagicMock, patch

from click.testing import CliRunner

from matcha.cli import cli
from matcha.commands.syn_flood_cmd import parse_ports, validate_target_ip


# ---------------------------------------------------------------------------
# Unit tests -- parse_ports
# ---------------------------------------------------------------------------


def test_parse_ports_single():
    assert parse_ports("80") == [80]


def test_parse_ports_multiple():
    assert parse_ports("80,443,8080") == [80, 443, 8080]


def test_parse_ports_range():
    assert parse_ports("8000-8003") == [8000, 8001, 8002, 8003]


def test_parse_ports_mixed():
    result = parse_ports("80,443,8000-8002")
    assert result == [80, 443, 8000, 8001, 8002]


def test_parse_ports_dedup():
    result = parse_ports("80,80,80")
    assert result == [80]


def test_parse_ports_invalid_skipped():
    result = parse_ports("abc,80")
    assert result == [80]


def test_parse_ports_out_of_range():
    result = parse_ports("0,80,99999")
    assert result == [80]


def test_parse_ports_empty():
    assert parse_ports("") == []


def test_parse_ports_range_too_large():
    """Ranges larger than 1000 should be clamped."""
    result = parse_ports("1-2000")
    assert len(result) == 1001  # 1..1001


def test_parse_ports_whitespace():
    assert parse_ports(" 80 , 443 ") == [80, 443]


# ---------------------------------------------------------------------------
# Unit tests -- validate_target_ip
# ---------------------------------------------------------------------------


def test_validate_ip_valid_v4():
    assert validate_target_ip("192.168.1.1") is True


def test_validate_ip_valid_loopback():
    assert validate_target_ip("127.0.0.1") is True


def test_validate_ip_valid_v6():
    assert validate_target_ip("::1") is True


def test_validate_ip_invalid():
    assert validate_target_ip("not-an-ip") is False


def test_validate_ip_empty():
    assert validate_target_ip("") is False


# ---------------------------------------------------------------------------
# CLI -- help & registration
# ---------------------------------------------------------------------------


def test_cli_syn_flood_help():
    """``matcha syn-flood --help`` should show all options."""
    runner = CliRunner()
    result = runner.invoke(cli, ["syn-flood", "--help"])
    assert result.exit_code == 0
    for flag in ["--target", "--ports", "--count", "--rate", "--spoof-ip"]:
        assert flag in result.output


def test_cli_help_shows_syn_flood():
    """``matcha --help`` should mention the syn-flood subcommand."""
    runner = CliRunner()
    result = runner.invoke(cli, ["--help"])
    assert result.exit_code == 0
    assert "syn-flood" in result.output


# ---------------------------------------------------------------------------
# CLI -- validation errors
# ---------------------------------------------------------------------------


def test_cli_syn_flood_missing_target():
    """Missing --target should fail."""
    runner = CliRunner()
    result = runner.invoke(cli, ["syn-flood", "--ports", "80"])
    assert result.exit_code != 0


def test_cli_syn_flood_missing_ports():
    """Missing --ports should fail."""
    runner = CliRunner()
    result = runner.invoke(cli, ["syn-flood", "--target", "127.0.0.1"])
    assert result.exit_code != 0


def test_cli_syn_flood_invalid_target():
    """Invalid target IP should exit with code 2."""
    runner = CliRunner()
    result = runner.invoke(cli, ["syn-flood", "--target", "not-an-ip", "--ports", "80"])
    assert result.exit_code == 2


def test_cli_syn_flood_invalid_ports():
    """All-invalid ports should exit with code 2."""
    runner = CliRunner()
    result = runner.invoke(cli, ["syn-flood", "--target", "127.0.0.1", "--ports", "abc"])
    assert result.exit_code == 2


# ---------------------------------------------------------------------------
# CLI -- successful execution (mocked attack)
# ---------------------------------------------------------------------------

_FAKE_STATS = {
    "target_ip": "127.0.0.1",
    "ports": [80],
    "packets_sent": 10,
    "duration_seconds": 0.5,
    "configured_rate": 100,
    "actual_rate": 20.0,
    "rate_efficiency": 20.0,
    "estimated_traffic_bytes": 600,
}


def _mock_load_class():
    """Return a mock SYNFloodAttack class whose instances return _FAKE_STATS."""
    mock_cls = MagicMock()
    mock_instance = MagicMock()
    mock_instance.execute.return_value = _FAKE_STATS.copy()
    mock_cls.return_value = mock_instance
    return mock_cls


def test_cli_syn_flood_text():
    """``matcha syn-flood --target ... --ports ...`` prints text output."""
    mock_cls = _mock_load_class()

    with patch(
        "matcha.commands.syn_flood_cmd._load_syn_flood_class", return_value=mock_cls
    ):
        runner = CliRunner()
        result = runner.invoke(
            cli, ["syn-flood", "--target", "127.0.0.1", "--ports", "80"]
        )
    assert result.exit_code == 0
    assert "packets_sent" in result.output


def test_cli_syn_flood_json():
    """``matcha -o json syn-flood ...`` outputs valid JSON stats."""
    mock_cls = _mock_load_class()

    with patch(
        "matcha.commands.syn_flood_cmd._load_syn_flood_class", return_value=mock_cls
    ):
        runner = CliRunner()
        result = runner.invoke(
            cli,
            ["-o", "json", "syn-flood", "--target", "127.0.0.1", "--ports", "80"],
        )
    assert result.exit_code == 0
    payload = json.loads(result.output)
    assert payload["target_ip"] == "127.0.0.1"
    assert payload["packets_sent"] == 10


def test_cli_syn_flood_custom_count():
    """--count is forwarded to SYNFloodAttack."""
    mock_cls = _mock_load_class()

    with patch(
        "matcha.commands.syn_flood_cmd._load_syn_flood_class", return_value=mock_cls
    ):
        runner = CliRunner()
        result = runner.invoke(
            cli,
            ["syn-flood", "--target", "127.0.0.1", "--ports", "80", "--count", "50"],
        )
    assert result.exit_code == 0
    _, kwargs = mock_cls.call_args
    assert kwargs["packet_count"] == 50


def test_cli_syn_flood_custom_rate():
    """--rate is forwarded to SYNFloodAttack."""
    mock_cls = _mock_load_class()

    with patch(
        "matcha.commands.syn_flood_cmd._load_syn_flood_class", return_value=mock_cls
    ):
        runner = CliRunner()
        result = runner.invoke(
            cli,
            ["syn-flood", "--target", "127.0.0.1", "--ports", "80", "--rate", "200"],
        )
    assert result.exit_code == 0
    _, kwargs = mock_cls.call_args
    assert kwargs["rate"] == 200


def test_cli_syn_flood_no_spoof():
    """--no-spoof-ip is forwarded to SYNFloodAttack."""
    mock_cls = _mock_load_class()

    with patch(
        "matcha.commands.syn_flood_cmd._load_syn_flood_class", return_value=mock_cls
    ):
        runner = CliRunner()
        result = runner.invoke(
            cli,
            [
                "syn-flood",
                "--target", "127.0.0.1",
                "--ports", "80",
                "--no-spoof-ip",
            ],
        )
    assert result.exit_code == 0
    _, kwargs = mock_cls.call_args
    assert kwargs["spoof_ip"] is False


def test_cli_syn_flood_multiple_ports():
    """Multiple ports are parsed and forwarded."""
    mock_cls = _mock_load_class()

    with patch(
        "matcha.commands.syn_flood_cmd._load_syn_flood_class", return_value=mock_cls
    ):
        runner = CliRunner()
        result = runner.invoke(
            cli,
            ["syn-flood", "--target", "127.0.0.1", "--ports", "80,443,8080"],
        )
    assert result.exit_code == 0
    _, kwargs = mock_cls.call_args
    assert kwargs["ports"] == [80, 443, 8080]


def test_cli_syn_flood_verbose():
    """--verbose flag propagates to SYNFloodAttack."""
    mock_cls = _mock_load_class()

    with patch(
        "matcha.commands.syn_flood_cmd._load_syn_flood_class", return_value=mock_cls
    ):
        runner = CliRunner()
        result = runner.invoke(
            cli,
            ["-v", "syn-flood", "--target", "127.0.0.1", "--ports", "80"],
        )
    assert result.exit_code == 0
    _, kwargs = mock_cls.call_args
    assert kwargs["verbose"] is True
