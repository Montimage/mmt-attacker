"""Comprehensive test suite for all 26 attack commands.

Covers:
- ``--help`` smoke test for every command (exits 0, shows expected options)
- Validation tests (invalid IP, invalid port, missing required args)
- ``matcha list`` output includes all attack names
- ``matcha info <name>`` for each attack
- JSON output mode tests

See: https://github.com/Montimage/mmt-attacker/issues/17
"""

from __future__ import annotations

import json
from unittest.mock import MagicMock, patch

import pytest
from click.testing import CliRunner

from matcha.cli import cli
from matcha.registry import all_attack_names, get_attack

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

ALL_ATTACKS = all_attack_names()

runner = CliRunner()


def _mock_load_class(result: dict | None = None):
    """Return a mock attack class whose execute() returns *result*."""
    mock_cls = MagicMock()
    mock_instance = MagicMock()
    mock_instance.execute.return_value = result or {"status": "ok"}
    mock_cls.return_value = mock_instance
    return mock_cls


def _cli_flag(param_name: str) -> str:
    """Convert a Python param name to its CLI flag form."""
    return f"--{param_name.replace('_', '-')}"


def _valid_args_for(name: str, tmp_path=None) -> list[str]:
    """Build a list of valid CLI arguments for the given attack.

    Uses safe dummy values that pass semantic validation.  For file
    params, creates a temporary file via *tmp_path* (pytest fixture).
    """
    entry = get_attack(name)
    args: list[str] = []
    for p in entry.params:
        flag = _cli_flag(p.name)
        if p.type == "bool":
            continue  # booleans are flags with defaults

        if p.name.endswith("_ip") or p.name == "dns_server" or p.name == "ntp_server":
            args.extend([flag, "10.0.0.1"])
        elif p.name.endswith("_port") or p.name == "listen_port":
            args.extend([flag, "8080"])
        elif p.name.endswith("_url"):
            args.extend([flag, "http://example.com"])
        elif p.name.endswith("_file") or p.name in ("passwords", "payload_file", "wordlist"):
            if tmp_path is not None:
                f = tmp_path / f"{p.name}.txt"
                f.write_text("dummy")
                args.extend([flag, str(f)])
            else:
                args.extend([flag, "/dev/null"])
        elif p.name == "target_prefix":
            args.extend([flag, "192.168.0.0/24"])
        elif p.name == "target_vlan" or p.name == "as_number":
            args.extend([flag, "100"])
        elif p.type == "int":
            args.extend([flag, "10"])
        elif p.type == "float":
            args.extend([flag, "1.0"])
        else:
            args.extend([flag, "test-value"])
    return args


# ---------------------------------------------------------------------------
# 1. --help smoke test for every command
# ---------------------------------------------------------------------------


class TestHelpSmokeAllCommands:
    """``matcha <attack> --help`` exits 0 and shows expected options."""

    @pytest.mark.parametrize("name", ALL_ATTACKS, ids=ALL_ATTACKS)
    def test_help_exits_zero(self, name: str):
        result = runner.invoke(cli, [name, "--help"])
        assert result.exit_code == 0, f"{name} --help exited {result.exit_code}: {result.output}"

    @pytest.mark.parametrize("name", ALL_ATTACKS, ids=ALL_ATTACKS)
    def test_help_shows_all_options(self, name: str):
        """--help output must mention every parameter defined in the registry."""
        entry = get_attack(name)
        result = runner.invoke(cli, [name, "--help"])
        assert result.exit_code == 0
        for p in entry.params:
            flag = _cli_flag(p.name)
            if p.type == "bool":
                # bool params show as --flag/--no-flag
                assert (
                    flag in result.output or f"--no-{p.name.replace('_', '-')}" in result.output
                ), f"{name}: {flag} not found in help output"
            else:
                assert flag in result.output, f"{name}: {flag} not found in help output"

    @pytest.mark.parametrize("name", ALL_ATTACKS, ids=ALL_ATTACKS)
    def test_help_shows_description(self, name: str):
        """--help output should contain at least part of the description."""
        entry = get_attack(name)
        result = runner.invoke(cli, [name, "--help"])
        assert result.exit_code == 0
        # Check first 40 chars of description appear (Click may wrap)
        snippet = entry.description[:40].lower()
        assert snippet in result.output.lower(), f"{name}: description not in help output"


# ---------------------------------------------------------------------------
# 2. Missing required args — every command exits 2
# ---------------------------------------------------------------------------


_ALL_OPTIONAL_ATTACKS = [
    n for n in ALL_ATTACKS if not any(p.required for p in get_attack(n).params)
]
_ATTACKS_WITH_REQUIRED = [n for n in ALL_ATTACKS if n not in _ALL_OPTIONAL_ATTACKS]


class TestMissingRequiredArgs:
    """Invoking a command without required args must exit with code 2."""

    @pytest.mark.parametrize("name", _ATTACKS_WITH_REQUIRED, ids=_ATTACKS_WITH_REQUIRED)
    def test_missing_required_exits_2(self, name: str):
        result = runner.invoke(cli, [name])
        assert result.exit_code == 2, f"{name} without args exited {result.exit_code}, expected 2"


# ---------------------------------------------------------------------------
# 3. IP validation — commands with *_ip params
# ---------------------------------------------------------------------------


_IP_ATTACKS = [n for n in ALL_ATTACKS if any(p.name.endswith("_ip") for p in get_attack(n).params)]

_INVALID_IPS = [
    "not-an-ip",
    "999.999.999.999",
    "abc.def.ghi.jkl",
    "",
]


class TestIPValidation:
    """Commands with IP params must reject invalid IPs."""

    @pytest.mark.parametrize("name", _IP_ATTACKS, ids=_IP_ATTACKS)
    @pytest.mark.parametrize(
        "bad_ip", _INVALID_IPS, ids=["text", "out-of-range", "alpha", "empty"]
    )
    def test_invalid_ip_rejected(self, name: str, bad_ip: str, tmp_path):
        entry = get_attack(name)
        # Find the first *_ip param and inject the bad value
        ip_param = next(p for p in entry.params if p.name.endswith("_ip"))
        args = _valid_args_for(name, tmp_path)
        flag = _cli_flag(ip_param.name)
        # Replace the valid IP with the bad one
        idx = args.index(flag)
        args[idx + 1] = bad_ip

        with patch("matcha.commands.factory.load_attack_class", return_value=_mock_load_class()):
            result = runner.invoke(cli, [name] + args)
        assert result.exit_code != 0, f"{name} accepted invalid IP {bad_ip!r}"


# ---------------------------------------------------------------------------
# 4. Port validation — commands with *_port or listen_port params
# ---------------------------------------------------------------------------


_PORT_ATTACKS = [
    n
    for n in ALL_ATTACKS
    if any(p.name.endswith("_port") or p.name == "listen_port" for p in get_attack(n).params)
]


class TestPortValidation:
    """Commands with port params must reject out-of-range ports."""

    @pytest.mark.parametrize("name", _PORT_ATTACKS, ids=_PORT_ATTACKS)
    def test_port_too_high(self, name: str, tmp_path):
        entry = get_attack(name)
        port_param = next(
            p for p in entry.params if p.name.endswith("_port") or p.name == "listen_port"
        )
        args = _valid_args_for(name, tmp_path)
        flag = _cli_flag(port_param.name)
        idx = args.index(flag)
        args[idx + 1] = "99999"

        with patch("matcha.commands.factory.load_attack_class", return_value=_mock_load_class()):
            result = runner.invoke(cli, [name] + args)
        assert result.exit_code != 0, f"{name} accepted port 99999"

    @pytest.mark.parametrize("name", _PORT_ATTACKS, ids=_PORT_ATTACKS)
    def test_port_negative(self, name: str, tmp_path):
        entry = get_attack(name)
        port_param = next(
            p for p in entry.params if p.name.endswith("_port") or p.name == "listen_port"
        )
        args = _valid_args_for(name, tmp_path)
        flag = _cli_flag(port_param.name)
        idx = args.index(flag)
        args[idx + 1] = "-1"

        with patch("matcha.commands.factory.load_attack_class", return_value=_mock_load_class()):
            result = runner.invoke(cli, [name] + args)
        assert result.exit_code != 0, f"{name} accepted port -1"


# ---------------------------------------------------------------------------
# 5. URL validation — commands with *_url params
# ---------------------------------------------------------------------------


_URL_ATTACKS = [
    n for n in ALL_ATTACKS if any(p.name.endswith("_url") for p in get_attack(n).params)
]


class TestURLValidation:
    """Commands with URL params must reject invalid URLs."""

    @pytest.mark.parametrize("name", _URL_ATTACKS, ids=_URL_ATTACKS)
    def test_invalid_scheme_rejected(self, name: str, tmp_path):
        entry = get_attack(name)
        url_param = next(p for p in entry.params if p.name.endswith("_url"))
        args = _valid_args_for(name, tmp_path)
        flag = _cli_flag(url_param.name)
        idx = args.index(flag)
        args[idx + 1] = "ftp://bad.example.com"

        with patch("matcha.commands.factory.load_attack_class", return_value=_mock_load_class()):
            result = runner.invoke(cli, [name] + args)
        assert result.exit_code != 0, f"{name} accepted ftp:// URL"

    @pytest.mark.parametrize("name", _URL_ATTACKS, ids=_URL_ATTACKS)
    def test_missing_host_rejected(self, name: str, tmp_path):
        entry = get_attack(name)
        url_param = next(p for p in entry.params if p.name.endswith("_url"))
        args = _valid_args_for(name, tmp_path)
        flag = _cli_flag(url_param.name)
        idx = args.index(flag)
        args[idx + 1] = "http://"

        with patch("matcha.commands.factory.load_attack_class", return_value=_mock_load_class()):
            result = runner.invoke(cli, [name] + args)
        assert result.exit_code != 0, f"{name} accepted URL with no host"


# ---------------------------------------------------------------------------
# 6. File validation — commands with *_file or wordlist params
# ---------------------------------------------------------------------------


_FILE_ATTACKS = [
    n
    for n in ALL_ATTACKS
    if any(p.name.endswith("_file") or p.name == "wordlist" for p in get_attack(n).params)
]


class TestFileValidation:
    """Commands with file params must reject non-existent files."""

    @pytest.mark.parametrize("name", _FILE_ATTACKS, ids=_FILE_ATTACKS)
    def test_nonexistent_file_rejected(self, name: str, tmp_path):
        entry = get_attack(name)
        file_param = next(
            p for p in entry.params if p.name.endswith("_file") or p.name == "wordlist"
        )
        args = _valid_args_for(name, tmp_path)
        flag = _cli_flag(file_param.name)
        idx = args.index(flag)
        args[idx + 1] = "/nonexistent/path/to/file.txt"

        with patch("matcha.commands.factory.load_attack_class", return_value=_mock_load_class()):
            result = runner.invoke(cli, [name] + args)
        assert result.exit_code != 0, f"{name} accepted non-existent file"


# ---------------------------------------------------------------------------
# 7. Network (CIDR) validation — bgp-hijacking
# ---------------------------------------------------------------------------


class TestNetworkValidation:
    """bgp-hijacking target_prefix must reject invalid CIDR."""

    def test_invalid_cidr_rejected(self):
        result = runner.invoke(
            cli,
            [
                "bgp-hijacking",
                "--target-prefix",
                "not-cidr",
                "--as-number",
                "100",
            ],
        )
        assert result.exit_code != 0

    def test_valid_cidr_accepted(self):
        mock_cls = _mock_load_class()
        with patch("matcha.commands.factory.load_attack_class", return_value=mock_cls):
            result = runner.invoke(
                cli,
                [
                    "bgp-hijacking",
                    "--target-prefix",
                    "10.0.0.0/8",
                    "--as-number",
                    "100",
                ],
            )
        assert result.exit_code == 0


# ---------------------------------------------------------------------------
# 8. matcha list — includes all attack names
# ---------------------------------------------------------------------------


class TestListIncludesAllAttacks:
    """``matcha list`` must include every registered attack name."""

    def test_list_text_contains_all_names(self):
        result = runner.invoke(cli, ["list"])
        assert result.exit_code == 0
        for name in ALL_ATTACKS:
            assert name in result.output, f"{name} not found in 'matcha list' output"

    def test_list_json_contains_all_names(self):
        result = runner.invoke(cli, ["-o", "json", "list"])
        assert result.exit_code == 0
        payload = json.loads(result.output)
        listed_names = {e["name"] for e in payload}
        for name in ALL_ATTACKS:
            assert name in listed_names, f"{name} not found in JSON list output"

    def test_list_json_has_26_entries(self):
        result = runner.invoke(cli, ["-o", "json", "list"])
        assert result.exit_code == 0
        payload = json.loads(result.output)
        assert len(payload) == 26

    def test_list_text_shows_correct_total(self):
        result = runner.invoke(cli, ["list"])
        assert result.exit_code == 0
        assert "26 attacks" in result.output


# ---------------------------------------------------------------------------
# 9. matcha info <name> — for every attack
# ---------------------------------------------------------------------------


class TestInfoAllAttacks:
    """``matcha info <name>`` must work for every registered attack."""

    @pytest.mark.parametrize("name", ALL_ATTACKS, ids=ALL_ATTACKS)
    def test_info_exits_zero(self, name: str):
        result = runner.invoke(cli, ["info", name])
        assert result.exit_code == 0, (
            f"matcha info {name} exited {result.exit_code}: {result.output}"
        )

    @pytest.mark.parametrize("name", ALL_ATTACKS, ids=ALL_ATTACKS)
    def test_info_shows_attack_name(self, name: str):
        result = runner.invoke(cli, ["info", name])
        assert result.exit_code == 0
        assert name in result.output

    @pytest.mark.parametrize("name", ALL_ATTACKS, ids=ALL_ATTACKS)
    def test_info_shows_category(self, name: str):
        entry = get_attack(name)
        result = runner.invoke(cli, ["info", name])
        assert result.exit_code == 0
        assert entry.category in result.output

    @pytest.mark.parametrize("name", ALL_ATTACKS, ids=ALL_ATTACKS)
    def test_info_shows_parameters_section(self, name: str):
        result = runner.invoke(cli, ["info", name])
        assert result.exit_code == 0
        assert "Parameters:" in result.output or "parameters" in result.output.lower()

    @pytest.mark.parametrize("name", ALL_ATTACKS, ids=ALL_ATTACKS)
    def test_info_json_valid(self, name: str):
        result = runner.invoke(cli, ["-o", "json", "info", name])
        assert result.exit_code == 0
        payload = json.loads(result.output)
        assert payload["name"] == name
        assert "category" in payload
        assert "parameters" in payload

    def test_info_unknown_attack_fails(self):
        result = runner.invoke(cli, ["info", "nonexistent-attack"])
        assert result.exit_code != 0


# ---------------------------------------------------------------------------
# 10. JSON output mode — commands produce valid JSON with mocked execution
# ---------------------------------------------------------------------------


class TestJSONOutputMode:
    """All commands should produce valid JSON output with -o json."""

    @pytest.mark.parametrize("name", ALL_ATTACKS, ids=ALL_ATTACKS)
    def test_json_output_valid(self, name: str, tmp_path):
        mock_result = {"attack": name, "status": "completed", "packets": 42}
        mock_cls = _mock_load_class(mock_result)
        args = _valid_args_for(name, tmp_path)

        with patch("matcha.commands.factory.load_attack_class", return_value=mock_cls):
            result = runner.invoke(cli, ["-o", "json", name] + args)
        assert result.exit_code == 0, (
            f"{name} JSON mode exited {result.exit_code}: {result.output}"
        )
        payload = json.loads(result.output)
        assert payload["attack"] == name
        assert payload["status"] == "completed"

    @pytest.mark.parametrize("name", ALL_ATTACKS, ids=ALL_ATTACKS)
    def test_text_output_valid(self, name: str, tmp_path):
        mock_result = {"attack": name, "status": "completed"}
        mock_cls = _mock_load_class(mock_result)
        args = _valid_args_for(name, tmp_path)

        with patch("matcha.commands.factory.load_attack_class", return_value=mock_cls):
            result = runner.invoke(cli, [name] + args)
        assert result.exit_code == 0, (
            f"{name} text mode exited {result.exit_code}: {result.output}"
        )
        assert "completed" in result.output


# ---------------------------------------------------------------------------
# 11. Mocked execution — every command invokes attack class correctly
# ---------------------------------------------------------------------------


class TestMockedExecution:
    """Every command loads and executes the attack class with correct params."""

    @pytest.mark.parametrize("name", ALL_ATTACKS, ids=ALL_ATTACKS)
    def test_execute_called(self, name: str, tmp_path):
        mock_cls = _mock_load_class()
        args = _valid_args_for(name, tmp_path)

        with patch("matcha.commands.factory.load_attack_class", return_value=mock_cls):
            result = runner.invoke(cli, [name] + args)
        assert result.exit_code == 0, f"{name} failed: {result.output}"
        mock_cls.return_value.execute.assert_called_once()

    @pytest.mark.parametrize("name", ALL_ATTACKS, ids=ALL_ATTACKS)
    def test_class_receives_required_params(self, name: str, tmp_path):
        entry = get_attack(name)
        mock_cls = _mock_load_class()
        args = _valid_args_for(name, tmp_path)

        with patch("matcha.commands.factory.load_attack_class", return_value=mock_cls):
            runner.invoke(cli, [name] + args)

        _, kwargs = mock_cls.call_args
        for p in entry.params:
            if p.required:
                assert p.name in kwargs, f"{name}: required param {p.name} not passed to class"
                assert kwargs[p.name] is not None, f"{name}: required param {p.name} is None"
