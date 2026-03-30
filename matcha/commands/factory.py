"""Command factory -- auto-generate Click commands from registry entries.

Given an :class:`~matcha.registry.AttackEntry` the factory produces a fully
configured :class:`click.Command` with options derived from the entry's
parameter definitions, input validation, dynamic class loading, and output
formatting.
"""

from __future__ import annotations

import importlib
import logging
import os
import sys
from typing import Any, Dict

import click

from matcha.output import format_output
from matcha.registry import AttackEntry, ParamDef

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Type mapping -- registry type strings to Python / Click types
# ---------------------------------------------------------------------------

_CLICK_TYPES: Dict[str, click.ParamType] = {
    "str": click.STRING,
    "int": click.INT,
    "float": click.FLOAT,
}


# ---------------------------------------------------------------------------
# Validation helpers
# ---------------------------------------------------------------------------


def validate_params(
    entry: AttackEntry,
    values: Dict[str, Any],
) -> list[str]:
    """Validate *values* against *entry*.params and return a list of errors.

    Checks:
    * Required parameters are present and not ``None``.
    * ``int`` / ``float`` values are the correct type (Click normally
      handles this, but we double-check for safety).
    """
    errors: list[str] = []
    for pdef in entry.params:
        val = values.get(pdef.name)
        if pdef.required and val is None:
            cli_flag = f"--{pdef.name.replace('_', '-')}"
            errors.append(f"Missing required option: {cli_flag}")
        elif val is not None and pdef.type in ("int", "float"):
            expected = int if pdef.type == "int" else float
            if not isinstance(val, expected):
                errors.append(
                    f"Option --{pdef.name.replace('_', '-')}: "
                    f"expected {pdef.type}, got {type(val).__name__}"
                )
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
    _project_root = os.path.dirname(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    )
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

    kwargs: Dict[str, Any] = {
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
        values: Dict[str, Any] = {}
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
        format_output(result, fmt=fmt)

    cmd = click.Command(
        name=entry.name,
        callback=callback,
        params=params,
        help=entry.description,
    )
    # Store the entry on the command so tests can inspect it.
    cmd.matcha_entry = entry  # type: ignore[attr-defined]
    return cmd
