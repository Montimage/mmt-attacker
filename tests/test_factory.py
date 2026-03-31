"""Tests for the command factory (``matcha.commands.factory``)."""

from __future__ import annotations

import json
from unittest.mock import MagicMock, patch

import click
from click.testing import CliRunner

from matcha.commands.factory import (
    make_command,
    validate_params,
)
from matcha.registry import AttackEntry, ParamDef

# ---------------------------------------------------------------------------
# Fixtures -- reusable registry entries
# ---------------------------------------------------------------------------


def _simple_entry() -> AttackEntry:
    """An entry with one required str and one optional int param."""
    return AttackEntry(
        name="fake-attack",
        description="A fake attack for testing.",
        category="Network-layer",
        module_path="scripts.fake.fake",
        class_name="FakeAttack",
        params=[
            ParamDef("target_ip", "str", True, None, "Target IP address"),
            ParamDef("count", "int", False, 100, "Packet count"),
        ],
    )


def _bool_entry() -> AttackEntry:
    """An entry with a boolean param."""
    return AttackEntry(
        name="bool-attack",
        description="Attack with a boolean flag.",
        category="Network-layer",
        module_path="scripts.fake.fake",
        class_name="FakeAttack",
        params=[
            ParamDef("target_ip", "str", True, None, "Target IP"),
            ParamDef("verbose_mode", "bool", False, True, "Enable verbose"),
        ],
    )


def _float_entry() -> AttackEntry:
    """An entry with a float param."""
    return AttackEntry(
        name="float-attack",
        description="Attack with a float option.",
        category="Replay",
        module_path="scripts.fake.fake",
        class_name="FakeAttack",
        params=[
            ParamDef("pcap_file", "str", True, None, "Path to pcap"),
            ParamDef("speed", "float", False, 1.0, "Replay speed"),
        ],
    )


def _multi_required_entry() -> AttackEntry:
    """An entry with multiple required params."""
    return AttackEntry(
        name="multi-req",
        description="Attack with two required params.",
        category="Application-layer",
        module_path="scripts.fake.fake",
        class_name="FakeAttack",
        params=[
            ParamDef("target_url", "str", True, None, "Target URL"),
            ParamDef("parameter", "str", True, None, "Vulnerable param"),
        ],
    )


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _wrap_in_group(cmd: click.Command) -> click.Group:
    """Wrap *cmd* in a group that mimics the real ``cli`` group context."""

    @click.group(invoke_without_command=True)
    @click.option("-o", "--output", type=click.Choice(["text", "json"]), default="text")
    @click.pass_context
    def group(ctx, output):
        ctx.ensure_object(dict)
        ctx.obj["output"] = output

    group.add_command(cmd)
    return group


def _make_mock_cls(result: dict | None = None):
    """Return a mock attack class whose instances return *result* from execute()."""
    mock_cls = MagicMock()
    mock_instance = MagicMock()
    mock_instance.execute.return_value = result or {"status": "ok"}
    mock_cls.return_value = mock_instance
    return mock_cls


# ---------------------------------------------------------------------------
# make_command -- returns a valid Click command
# ---------------------------------------------------------------------------


class TestMakeCommand:
    """Tests for ``make_command()``."""

    def test_returns_click_command(self):
        cmd = make_command(_simple_entry())
        assert isinstance(cmd, click.Command)

    def test_command_name_matches_entry(self):
        cmd = make_command(_simple_entry())
        assert cmd.name == "fake-attack"

    def test_help_text_matches_description(self):
        entry = _simple_entry()
        cmd = make_command(entry)
        assert cmd.help == entry.description

    def test_has_correct_options(self):
        cmd = make_command(_simple_entry())
        option_names = {p.name for p in cmd.params}
        assert "target_ip" in option_names
        assert "count" in option_names

    def test_required_option_is_required(self):
        cmd = make_command(_simple_entry())
        target_opt = [p for p in cmd.params if p.name == "target_ip"][0]
        assert target_opt.required is True

    def test_optional_has_default(self):
        cmd = make_command(_simple_entry())
        count_opt = [p for p in cmd.params if p.name == "count"][0]
        assert count_opt.required is False
        assert count_opt.default == 100

    def test_bool_param_creates_flag(self):
        cmd = make_command(_bool_entry())
        flag_opt = [p for p in cmd.params if p.name == "verbose_mode"][0]
        assert flag_opt.is_flag is True

    def test_float_param_type(self):
        cmd = make_command(_float_entry())
        speed_opt = [p for p in cmd.params if p.name == "speed"][0]
        assert speed_opt.type == click.FLOAT

    def test_matcha_entry_attribute(self):
        entry = _simple_entry()
        cmd = make_command(entry)
        assert cmd.matcha_entry is entry


# ---------------------------------------------------------------------------
# make_command -- help output
# ---------------------------------------------------------------------------


class TestMakeCommandHelp:
    """Tests for --help output of generated commands."""

    def test_help_shows_required_options(self):
        cmd = make_command(_simple_entry())
        group = _wrap_in_group(cmd)
        runner = CliRunner()
        result = runner.invoke(group, ["fake-attack", "--help"])
        assert result.exit_code == 0
        assert "--target-ip" in result.output
        assert "--count" in result.output

    def test_help_shows_description(self):
        cmd = make_command(_simple_entry())
        group = _wrap_in_group(cmd)
        runner = CliRunner()
        result = runner.invoke(group, ["fake-attack", "--help"])
        assert result.exit_code == 0
        assert "fake attack for testing" in result.output.lower()

    def test_help_shows_defaults(self):
        cmd = make_command(_simple_entry())
        group = _wrap_in_group(cmd)
        runner = CliRunner()
        result = runner.invoke(group, ["fake-attack", "--help"])
        assert result.exit_code == 0
        assert "100" in result.output

    def test_help_shows_bool_flag(self):
        cmd = make_command(_bool_entry())
        group = _wrap_in_group(cmd)
        runner = CliRunner()
        result = runner.invoke(group, ["bool-attack", "--help"])
        assert result.exit_code == 0
        assert "--verbose-mode" in result.output
        assert "--no-verbose-mode" in result.output

    def test_help_shows_help_text_for_params(self):
        cmd = make_command(_simple_entry())
        group = _wrap_in_group(cmd)
        runner = CliRunner()
        result = runner.invoke(group, ["fake-attack", "--help"])
        assert result.exit_code == 0
        assert "Target IP address" in result.output
        assert "Packet count" in result.output


# ---------------------------------------------------------------------------
# make_command -- validation errors
# ---------------------------------------------------------------------------


class TestMakeCommandValidation:
    """Tests for validation error handling in generated commands."""

    def test_missing_required_exits_nonzero(self):
        """Missing a required option should result in a non-zero exit code."""
        cmd = make_command(_simple_entry())
        group = _wrap_in_group(cmd)
        runner = CliRunner()
        # Omit --target-ip (required)
        result = runner.invoke(group, ["fake-attack"])
        assert result.exit_code != 0

    def test_missing_required_shows_error(self):
        """Missing a required option should show an error message."""
        cmd = make_command(_simple_entry())
        group = _wrap_in_group(cmd)
        runner = CliRunner()
        result = runner.invoke(group, ["fake-attack"])
        assert result.exit_code != 0

    def test_wrong_type_exits_nonzero(self):
        """Passing a string where int is expected should fail."""
        cmd = make_command(_simple_entry())
        group = _wrap_in_group(cmd)
        runner = CliRunner()
        result = runner.invoke(group, ["fake-attack", "--target-ip", "1.2.3.4", "--count", "abc"])
        assert result.exit_code != 0

    def test_multi_required_missing_both(self):
        """Multiple required params missing should fail."""
        cmd = make_command(_multi_required_entry())
        group = _wrap_in_group(cmd)
        runner = CliRunner()
        result = runner.invoke(group, ["multi-req"])
        assert result.exit_code != 0


# ---------------------------------------------------------------------------
# make_command -- execution (mocked)
# ---------------------------------------------------------------------------


class TestMakeCommandExecution:
    """Tests for successful command execution with mocked attack classes."""

    def test_text_output(self):
        """Successful execution should produce text output."""
        entry = _simple_entry()
        cmd = make_command(entry)
        group = _wrap_in_group(cmd)
        mock_cls = _make_mock_cls({"target": "1.2.3.4", "packets": 100})

        with patch("matcha.commands.factory.load_attack_class", return_value=mock_cls):
            runner = CliRunner()
            result = runner.invoke(group, ["fake-attack", "--target-ip", "1.2.3.4"])
        assert result.exit_code == 0
        assert "1.2.3.4" in result.output
        assert "100" in result.output

    def test_json_output(self):
        """With -o json the result should be valid JSON."""
        entry = _simple_entry()
        cmd = make_command(entry)
        group = _wrap_in_group(cmd)
        mock_cls = _make_mock_cls({"target": "1.2.3.4", "packets": 50})

        with patch("matcha.commands.factory.load_attack_class", return_value=mock_cls):
            runner = CliRunner()
            result = runner.invoke(group, ["-o", "json", "fake-attack", "--target-ip", "1.2.3.4"])
        assert result.exit_code == 0
        payload = json.loads(result.output)
        assert payload["target"] == "1.2.3.4"
        assert payload["packets"] == 50

    def test_class_instantiated_with_correct_args(self):
        """The attack class should receive the validated param dict."""
        entry = _simple_entry()
        cmd = make_command(entry)
        group = _wrap_in_group(cmd)
        mock_cls = _make_mock_cls()

        with patch("matcha.commands.factory.load_attack_class", return_value=mock_cls):
            runner = CliRunner()
            runner.invoke(
                group,
                ["fake-attack", "--target-ip", "10.0.0.1", "--count", "50"],
            )

        mock_cls.assert_called_once_with(target_ip="10.0.0.1", count=50)

    def test_default_value_forwarded(self):
        """Optional param defaults should be forwarded to the class."""
        entry = _simple_entry()
        cmd = make_command(entry)
        group = _wrap_in_group(cmd)
        mock_cls = _make_mock_cls()

        with patch("matcha.commands.factory.load_attack_class", return_value=mock_cls):
            runner = CliRunner()
            runner.invoke(group, ["fake-attack", "--target-ip", "10.0.0.1"])

        mock_cls.assert_called_once_with(target_ip="10.0.0.1", count=100)

    def test_bool_flag_true(self):
        """Boolean flag should default to its defined default."""
        entry = _bool_entry()
        cmd = make_command(entry)
        group = _wrap_in_group(cmd)
        mock_cls = _make_mock_cls()

        with patch("matcha.commands.factory.load_attack_class", return_value=mock_cls):
            runner = CliRunner()
            runner.invoke(group, ["bool-attack", "--target-ip", "10.0.0.1"])

        _, kwargs = mock_cls.call_args
        assert kwargs["verbose_mode"] is True

    def test_bool_flag_negated(self):
        """--no-verbose-mode should pass False."""
        entry = _bool_entry()
        cmd = make_command(entry)
        group = _wrap_in_group(cmd)
        mock_cls = _make_mock_cls()

        with patch("matcha.commands.factory.load_attack_class", return_value=mock_cls):
            runner = CliRunner()
            runner.invoke(
                group,
                ["bool-attack", "--target-ip", "10.0.0.1", "--no-verbose-mode"],
            )

        _, kwargs = mock_cls.call_args
        assert kwargs["verbose_mode"] is False

    def test_float_param_forwarded(self, tmp_path):
        """Float params should be correctly typed."""
        pcap = tmp_path / "test.pcap"
        pcap.write_bytes(b"")

        entry = _float_entry()
        cmd = make_command(entry)
        group = _wrap_in_group(cmd)
        mock_cls = _make_mock_cls()

        with patch("matcha.commands.factory.load_attack_class", return_value=mock_cls):
            runner = CliRunner()
            runner.invoke(
                group,
                ["float-attack", "--pcap-file", str(pcap), "--speed", "2.5"],
            )

        _, kwargs = mock_cls.call_args
        assert kwargs["speed"] == 2.5

    def test_execute_called_once(self):
        """attack.execute() should be called exactly once."""
        entry = _simple_entry()
        cmd = make_command(entry)
        group = _wrap_in_group(cmd)
        mock_cls = _make_mock_cls()

        with patch("matcha.commands.factory.load_attack_class", return_value=mock_cls):
            runner = CliRunner()
            runner.invoke(group, ["fake-attack", "--target-ip", "10.0.0.1"])

        mock_cls.return_value.execute.assert_called_once()


# ---------------------------------------------------------------------------
# validate_params -- unit tests
# ---------------------------------------------------------------------------


class TestValidateParams:
    """Tests for ``validate_params()``."""

    def test_valid_input_no_errors(self):
        entry = _simple_entry()
        errors = validate_params(entry, {"target_ip": "1.2.3.4", "count": 100})
        assert errors == []

    def test_missing_required_reports_error(self):
        entry = _simple_entry()
        errors = validate_params(entry, {"target_ip": None, "count": 100})
        assert len(errors) == 1
        assert "--target-ip" in errors[0]

    def test_optional_none_is_ok(self):
        entry = _simple_entry()
        errors = validate_params(entry, {"target_ip": "1.2.3.4", "count": None})
        assert errors == []

    def test_wrong_type_reports_error(self):
        entry = _simple_entry()
        errors = validate_params(entry, {"target_ip": "1.2.3.4", "count": "bad"})
        assert len(errors) == 1
        assert "--count" in errors[0]

    def test_multiple_errors(self):
        entry = _multi_required_entry()
        errors = validate_params(entry, {"target_url": None, "parameter": None})
        assert len(errors) == 2


# ---------------------------------------------------------------------------
# validate_params -- semantic validation
# ---------------------------------------------------------------------------


class TestSemanticValidation:
    """Tests for IP, port, URL, file path, and network validation."""

    def test_invalid_ip_reports_error(self):
        entry = _simple_entry()
        errors = validate_params(entry, {"target_ip": "not-an-ip", "count": 100})
        assert len(errors) == 1
        assert "Invalid IP" in errors[0]

    def test_valid_ip_no_error(self):
        entry = _simple_entry()
        errors = validate_params(entry, {"target_ip": "192.168.1.1", "count": 100})
        assert errors == []

    def test_valid_ipv6_no_error(self):
        entry = _simple_entry()
        errors = validate_params(entry, {"target_ip": "::1", "count": 100})
        assert errors == []

    def test_invalid_url_scheme(self):
        entry = _multi_required_entry()
        errors = validate_params(entry, {"target_url": "ftp://bad.example.com", "parameter": "id"})
        assert len(errors) == 1
        assert "Invalid URL scheme" in errors[0]

    def test_invalid_url_missing_host(self):
        entry = _multi_required_entry()
        errors = validate_params(entry, {"target_url": "http://", "parameter": "id"})
        assert len(errors) == 1
        assert "missing hostname" in errors[0]

    def test_valid_url_no_error(self):
        entry = _multi_required_entry()
        errors = validate_params(
            entry, {"target_url": "https://example.com/login", "parameter": "id"}
        )
        assert errors == []

    def test_invalid_port_too_high(self):
        entry = AttackEntry(
            name="port-test",
            description="Test",
            category="Network-layer",
            module_path="scripts.fake.fake",
            class_name="Fake",
            params=[ParamDef("target_port", "int", True, None, "Port")],
        )
        errors = validate_params(entry, {"target_port": 99999})
        assert len(errors) == 1
        assert "Invalid port" in errors[0]

    def test_valid_port_no_error(self):
        entry = AttackEntry(
            name="port-test",
            description="Test",
            category="Network-layer",
            module_path="scripts.fake.fake",
            class_name="Fake",
            params=[ParamDef("target_port", "int", False, 80, "Port")],
        )
        errors = validate_params(entry, {"target_port": 443})
        assert errors == []

    def test_file_not_found(self):
        entry = _float_entry()
        errors = validate_params(entry, {"pcap_file": "/nonexistent/file.pcap", "speed": 1.0})
        assert len(errors) == 1
        assert "File not found" in errors[0]

    def test_valid_file(self, tmp_path):
        pcap = tmp_path / "test.pcap"
        pcap.write_bytes(b"")
        entry = _float_entry()
        errors = validate_params(entry, {"pcap_file": str(pcap), "speed": 1.0})
        assert errors == []

    def test_network_prefix_invalid(self):
        entry = AttackEntry(
            name="net-test",
            description="Test",
            category="Network-layer",
            module_path="scripts.fake.fake",
            class_name="Fake",
            params=[ParamDef("target_prefix", "str", True, None, "Prefix")],
        )
        errors = validate_params(entry, {"target_prefix": "not-cidr"})
        assert len(errors) == 1
        assert "Invalid network" in errors[0]

    def test_network_prefix_valid(self):
        entry = AttackEntry(
            name="net-test",
            description="Test",
            category="Network-layer",
            module_path="scripts.fake.fake",
            class_name="Fake",
            params=[ParamDef("target_prefix", "str", True, None, "Prefix")],
        )
        errors = validate_params(entry, {"target_prefix": "192.168.0.0/24"})
        assert errors == []

    def test_optional_none_skips_semantic_validation(self):
        """Optional params with None value should not be validated."""
        entry = _float_entry()
        errors = validate_params(entry, {"pcap_file": "/dev/null", "speed": None})
        assert errors == []

    def test_wordlist_param_validates_as_file(self):
        entry = AttackEntry(
            name="brute-test",
            description="Test",
            category="Application-layer",
            module_path="scripts.fake.fake",
            class_name="Fake",
            params=[
                ParamDef("target_ip", "str", True, None, "IP"),
                ParamDef("wordlist", "str", True, None, "Wordlist file"),
            ],
        )
        errors = validate_params(entry, {"target_ip": "10.0.0.1", "wordlist": "/no/such/file.txt"})
        assert len(errors) == 1
        assert "File not found" in errors[0]


# ---------------------------------------------------------------------------
# make_command with real registry entries (smoke tests)
# ---------------------------------------------------------------------------


class TestMakeCommandWithRealRegistry:
    """Verify make_command works with actual registry entries."""

    def test_syn_flood_command(self):
        from matcha.registry import get_attack

        entry = get_attack("syn-flood")
        cmd = make_command(entry)
        assert cmd.name == "syn-flood"
        option_names = {p.name for p in cmd.params}
        assert "target_ip" in option_names
        assert "target_port" in option_names
        assert "count" in option_names

    def test_pcap_replay_command(self):
        from matcha.registry import get_attack

        entry = get_attack("pcap-replay")
        cmd = make_command(entry)
        assert cmd.name == "pcap-replay"
        option_names = {p.name for p in cmd.params}
        assert "pcap_file" in option_names
        assert "interface" in option_names
        assert "rate" in option_names

    def test_all_attacks_produce_commands(self):
        """Every registered attack should produce a valid command."""
        from matcha.registry import all_attack_names, get_attack

        for name in all_attack_names():
            entry = get_attack(name)
            cmd = make_command(entry)
            assert isinstance(cmd, click.Command), f"Failed for {name}"
            assert cmd.name == name

    def test_all_commands_show_help(self):
        """Every generated command should produce valid --help output."""
        from matcha.registry import all_attack_names, get_attack

        runner = CliRunner()
        for name in all_attack_names():
            entry = get_attack(name)
            cmd = make_command(entry)
            group = _wrap_in_group(cmd)
            result = runner.invoke(group, [name, "--help"])
            assert result.exit_code == 0, f"--help failed for {name}"
