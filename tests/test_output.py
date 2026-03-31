"""Tests for the matcha output formatter."""

import json

import pytest

from matcha.output import format_output


def test_format_text_key_value(capsys):
    """Text mode renders all keys and values."""
    data = {"attack": "syn_flood", "packets_sent": 100, "status": "ok"}
    format_output(data, fmt="text")
    captured = capsys.readouterr()
    out = captured.out
    # "attack" key is used as title (uppercased); value appears there
    assert "SYN_FLOOD" in out
    assert "100" in out
    assert "ok" in out
    # Nothing should leak to stderr
    assert captured.err == ""


def test_format_json_valid(capsys):
    """JSON mode prints valid JSON to stdout."""
    data = {"attack": "syn_flood", "packets_sent": 100}
    format_output(data, fmt="json")
    captured = capsys.readouterr()
    parsed = json.loads(captured.out)
    assert parsed == data
    assert captured.err == ""


def test_format_json_ends_with_newline(capsys):
    """JSON output should end with a trailing newline."""
    format_output({"a": 1}, fmt="json")
    captured = capsys.readouterr()
    assert captured.out.endswith("\n")


def test_format_text_with_table(capsys):
    """Text mode renders a list of dicts as a table."""
    data = {
        "results": [
            {"host": "10.0.0.1", "port": 80, "state": "open"},
            {"host": "10.0.0.2", "port": 443, "state": "closed"},
        ]
    }
    format_output(data, fmt="text")
    captured = capsys.readouterr()
    assert "host" in captured.out.lower()
    assert "10.0.0.1" in captured.out
    assert "10.0.0.2" in captured.out
    # Separator line should be present
    assert "─" in captured.out


def test_format_text_with_nested_dict(capsys):
    """Text mode renders nested dicts with their values visible."""
    data = {"config": {"target": "10.0.0.1", "timeout": 30}}
    format_output(data, fmt="text")
    captured = capsys.readouterr()
    assert "config" in captured.out.lower()
    assert "10.0.0.1" in captured.out
    assert "30" in captured.out


def test_format_text_default(capsys):
    """Default format is text."""
    data = {"key": "value"}
    format_output(data)
    captured = capsys.readouterr()
    assert "key" in captured.out.lower()
    assert "value" in captured.out


def test_format_invalid_raises():
    """Invalid format should raise ValueError."""
    with pytest.raises(ValueError, match="Unsupported output format"):
        format_output({"a": 1}, fmt="xml")


def test_format_json_non_serializable(capsys):
    """JSON mode should handle non-serializable types via default=str."""
    data = {"timestamp": object()}
    format_output(data, fmt="json")
    captured = capsys.readouterr()
    parsed = json.loads(captured.out)
    assert "timestamp" in parsed


def test_no_logging_in_stdout(capsys):
    """Neither text nor json mode should emit logging output to stdout."""
    import logging

    logger = logging.getLogger("matcha.output")
    logger.warning("should go to stderr not stdout")
    data = {"clean": True}
    format_output(data, fmt="text")
    captured = capsys.readouterr()
    assert "should go to stderr" not in captured.out


def test_format_text_empty_dict(capsys):
    """Text mode handles an empty dict gracefully — outputs at least a newline."""
    format_output({}, fmt="text")
    captured = capsys.readouterr()
    assert "\n" in captured.out


def test_format_json_empty_dict(capsys):
    """JSON mode handles an empty dict."""
    format_output({}, fmt="json")
    captured = capsys.readouterr()
    assert json.loads(captured.out) == {}
