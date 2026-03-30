"""Output formatter for attack results.

Formats ``Dict[str, Any]`` payloads returned by attack ``execute()``
methods as either human-readable text or raw JSON.
"""

from __future__ import annotations

import json
import sys
from typing import Any, Dict, List, Sequence


def _is_table(value: Sequence[Any]) -> bool:
    """Return True when *value* looks like a list of dicts with uniform keys."""
    if not value or not isinstance(value, (list, tuple)):
        return False
    if not all(isinstance(row, dict) for row in value):
        return False
    keys = set(value[0].keys())
    return all(set(row.keys()) == keys for row in value)


def _format_table(rows: List[Dict[str, Any]]) -> str:
    """Return a simple ASCII table for a list of dicts."""
    if not rows:
        return ""
    headers = list(rows[0].keys())
    col_widths = {h: len(str(h)) for h in headers}
    for row in rows:
        for h in headers:
            col_widths[h] = max(col_widths[h], len(str(row.get(h, ""))))

    header_line = "  ".join(str(h).ljust(col_widths[h]) for h in headers)
    separator = "  ".join("-" * col_widths[h] for h in headers)
    lines = [header_line, separator]
    for row in rows:
        lines.append("  ".join(str(row.get(h, "")).ljust(col_widths[h]) for h in headers))
    return "\n".join(lines)


def _format_text(data: Dict[str, Any]) -> str:
    """Return a human-readable text representation of *data*."""
    lines: list[str] = []
    for key, value in data.items():
        if isinstance(value, (list, tuple)) and _is_table(value):
            lines.append(f"{key}:")
            lines.append(_format_table(list(value)))
        elif isinstance(value, dict):
            lines.append(f"{key}:")
            for sub_key, sub_value in value.items():
                lines.append(f"  {sub_key}: {sub_value}")
        else:
            lines.append(f"{key}: {value}")
    return "\n".join(lines)


def format_output(data: Dict[str, Any], fmt: str = "text") -> None:
    """Print *data* to stdout in the requested format.

    Parameters
    ----------
    data:
        Dictionary of results returned by an attack's ``execute()`` method.
    fmt:
        ``"text"`` for a human-readable summary or ``"json"`` for raw JSON.

    Raises
    ------
    ValueError
        If *fmt* is not ``"text"`` or ``"json"``.
    """
    if fmt == "json":
        json.dump(data, sys.stdout, indent=2, default=str)
        sys.stdout.write("\n")
    elif fmt == "text":
        sys.stdout.write(_format_text(data))
        sys.stdout.write("\n")
    else:
        raise ValueError(f"Unsupported output format: {fmt!r}")
