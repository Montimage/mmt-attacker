"""Command factory -- auto-generate Click commands from registry entries.

Given an :class:`~matcha.registry.AttackEntry` the factory produces a fully
configured :class:`click.Command` with options derived from the entry's
parameter definitions, input validation, dynamic class loading, and output
formatting.
"""

from __future__ import annotations

import importlib
import ipaddress
import logging
import os
import sys
from typing import Any
from urllib.parse import urlparse

import click

from matcha.output import format_output
from matcha.registry import AttackEntry, ParamDef

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Type mapping -- registry type strings to Python / Click types
# ---------------------------------------------------------------------------

_CLICK_TYPES: dict[str, click.ParamType] = {
    "str": click.STRING,
    "int": click.INT,
    "float": click.FLOAT,
}


# ---------------------------------------------------------------------------
# Validation helpers
# ---------------------------------------------------------------------------


def _validate_ip(value: str) -> str | None:
    """Return an error string if *value* is not a valid IP address."""
    try:
        ipaddress.ip_address(value)
    except ValueError:
        return f"Invalid IP address: {value}"
    return None


def _validate_port(value: int) -> str | None:
    """Return an error string if *value* is outside the valid port range."""
    if not (0 <= value <= 65535):
        return f"Invalid port number: {value} (must be 0-65535)"
    return None


def _validate_url(value: str) -> str | None:
    """Return an error string if *value* is not a valid HTTP(S) URL."""
    parsed = urlparse(value)
    if parsed.scheme not in ("http", "https"):
        return f"Invalid URL scheme: {parsed.scheme!r} (expected http or https)"
    if not parsed.netloc:
        return f"Invalid URL (missing hostname): {value}"
    return None


def _validate_file_path(value: str) -> str | None:
    """Return an error string if *value* does not point to a readable file."""
    if not os.path.exists(value):
        return f"File not found: {value}"
    if not os.access(value, os.R_OK):
        return f"File not readable: {value}"
    return None


def _validate_network(value: str) -> str | None:
    """Return an error string if *value* is not valid CIDR notation."""
    try:
        ipaddress.ip_network(value, strict=False)
    except ValueError:
        return f"Invalid network (CIDR notation expected): {value}"
    return None


# Maps parameter name patterns to their semantic validator.
# Checked in order — first match wins.
_PARAM_VALIDATORS = [
    # Exact name matches first
    ("target_prefix", _validate_network),
    # Suffix-based patterns
    ("_ip", _validate_ip),
    ("_port", _validate_port),
    ("_url", _validate_url),
    ("_file", _validate_file_path),
    ("wordlist", _validate_file_path),
]

# Params matched by exact name (not suffix)
_EXACT_NAME_VALIDATORS: dict[str, Any] = {
    "target_prefix": _validate_network,
    "wordlist": _validate_file_path,
    "passwords": _validate_file_path,
}


def _get_semantic_validator(name: str):
    """Return the semantic validation function for a param *name*, or None."""
    if name in _EXACT_NAME_VALIDATORS:
        return _EXACT_NAME_VALIDATORS[name]
    for suffix, validator in _PARAM_VALIDATORS:
        if name.endswith(suffix):
            return validator
    return None


def validate_params(
    entry: AttackEntry,
    values: dict[str, Any],
) -> list[str]:
    """Validate *values* against *entry*.params and return a list of errors.

    Checks:
    * Required parameters are present and not ``None``.
    * ``int`` / ``float`` values are the correct type (Click normally
      handles this, but we double-check for safety).
    * Semantic validation: IP addresses, ports, URLs, file paths, and
      network prefixes are validated based on parameter name patterns.
    """
    errors: list[str] = []
    for pdef in entry.params:
        val = values.get(pdef.name)
        cli_flag = f"--{pdef.name.replace('_', '-')}"

        # Required check
        if pdef.required and val is None:
            errors.append(f"Missing required option: {cli_flag}")
            continue

        # Skip further checks if value is absent (optional + not provided)
        if val is None:
            continue

        # Basic type check
        if pdef.type in ("int", "float"):
            expected = int if pdef.type == "int" else float
            if not isinstance(val, expected):
                errors.append(f"Option {cli_flag}: expected {pdef.type}, got {type(val).__name__}")
                continue

        # Semantic validation
        validator = _get_semantic_validator(pdef.name)
        if validator is not None:
            err = validator(val)
            if err is not None:
                errors.append(f"Option {cli_flag}: {err}")

    return errors


# ---------------------------------------------------------------------------
# Dynamic class loader
# ---------------------------------------------------------------------------


def load_attack_class(entry: AttackEntry) -> type:
    """Import and return the attack class described by *entry*.

    The ``scripts/`` directory lives at the project root and is not a proper
    Python package.  We add the project root to ``sys.path`` when needed so
    the import resolves.
    """
    _project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    if _project_root not in sys.path:
        sys.path.insert(0, _project_root)

    module = importlib.import_module(entry.module_path)
    return getattr(module, entry.class_name)


# ---------------------------------------------------------------------------
# Factory
# ---------------------------------------------------------------------------


def _make_option(pdef: ParamDef) -> click.Option:
    """Create a :class:`click.Option` from a single :class:`ParamDef`."""
    option_name = f"--{pdef.name.replace('_', '-')}"
    param_decls = [option_name]

    kwargs: dict[str, Any] = {
        "help": pdef.help,
    }

    if pdef.type == "bool":
        # Boolean params become --flag / --no-flag pairs.
        on_flag = option_name
        off_flag = f"--no-{pdef.name.replace('_', '-')}"
        param_decls = [on_flag + "/" + off_flag]
        kwargs["default"] = pdef.default if pdef.default is not None else False
        kwargs["show_default"] = True
    else:
        kwargs["type"] = _CLICK_TYPES.get(pdef.type, click.STRING)
        kwargs["required"] = pdef.required
        if not pdef.required:
            kwargs["default"] = pdef.default
            kwargs["show_default"] = True

    return click.Option(param_decls, **kwargs)


def make_command(entry: AttackEntry) -> click.Command:
    """Return a :class:`click.Command` for the given registry *entry*.

    The generated command:

    1. Creates Click options from *entry.params*.
    2. Validates user-supplied values.
    3. Dynamically loads the script class from *entry.module_path*.
    4. Instantiates the class with validated arguments.
    5. Calls ``.execute()`` and pipes the result through
       :func:`~matcha.output.format_output`.
    """

    # Build Click options from the parameter definitions.
    params = [_make_option(p) for p in entry.params]

    def callback(**kwargs: Any) -> None:
        ctx = click.get_current_context()

        # Map CLI option names (with hyphens) back to Python names
        # (with underscores). Click does this automatically for the
        # callback kwargs, so `kwargs` keys already use underscores.
        values: dict[str, Any] = {}
        for pdef in entry.params:
            values[pdef.name] = kwargs.get(pdef.name)

        # Validate -------------------------------------------------------
        errors = validate_params(entry, values)
        if errors:
            for err in errors:
                click.echo(f"Error: {err}", err=True)
            ctx.exit(2)
            return

        # Load & execute -------------------------------------------------
        attack_cls = load_attack_class(entry)

        logger.debug("Instantiating %s with %s", entry.class_name, values)
        attack = attack_cls(**values)
        result = attack.execute()

        # Format output --------------------------------------------------
        fmt = ctx.obj.get("output", "text") if ctx.obj else "text"
        format_output(result, fmt=fmt, entry=entry)

    cmd = click.Command(
        name=entry.name,
        callback=callback,
        params=params,
        help=entry.description,
    )
    # Store the entry on the command so tests can inspect it.
    cmd.matcha_entry = entry  # type: ignore[attr-defined]
    return cmd
