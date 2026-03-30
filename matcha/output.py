"""Output formatter for attack results.

Formats ``Dict[str, Any]`` payloads returned by attack ``execute()``
methods as either human-readable rich text or raw JSON.

Terminal output uses ANSI colours when stdout is a TTY.
File output (piped) is always plain text.
"""

from __future__ import annotations

import json
import os
import re
import sys
import textwrap
from collections.abc import Sequence
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from matcha.registry import AttackEntry

# ---------------------------------------------------------------------------
# ANSI palette  (electric cyan / amber / slate)
# ---------------------------------------------------------------------------

_R     = "\033[0m"
_BOLD  = "\033[1m"
_DIM   = "\033[2m"

_CYAN  = "\033[38;5;51m"
_TEAL  = "\033[38;5;37m"
_AMBER = "\033[38;5;214m"
_GREEN = "\033[38;5;82m"
_RED   = "\033[38;5;196m"
_GREY  = "\033[38;5;240m"
_WHITE = "\033[38;5;252m"
_LBLUE = "\033[38;5;117m"

# Detect colour support (can be overridden at runtime via the module attribute)
_COLOR: bool = sys.stdout.isatty() and os.environ.get("NO_COLOR", "") == ""

# Strip ANSI escapes for visible-width calculation
_ANSI_RE = re.compile(r"\033\[[0-9;]*m")


def _c(code: str, text: str) -> str:
    """Wrap *text* with *code* only when colour is active."""
    return f"{code}{text}{_R}" if _COLOR else text


def _vis(s: str) -> int:
    """Return the visible (printable) character width of *s*."""
    return len(_ANSI_RE.sub("", s))


# ---------------------------------------------------------------------------
# Box layout constants
# ---------------------------------------------------------------------------

_W       = 70   # inner content width (between the two ║ borders)
_LABEL_W = 24   # label column width
_SEP     = 2    # gap between label and value columns
_VALUE_W = _W - _LABEL_W - _SEP - 4  # usable value width (2 left + 2 right margin)


# ---------------------------------------------------------------------------
# Box-drawing primitives
# ---------------------------------------------------------------------------


def _box_top(title: str = "") -> str:
    if title:
        vis_title = _vis(title)
        right_fill = _W - vis_title - 4  # "╔══ " + " " + "═…╗"
        bar = (
            _c(_GREY, "╔══ ")
            + _c(_CYAN + _BOLD, title)
            + _c(_GREY, " " + "═" * max(right_fill, 0) + "╗")
        )
    else:
        bar = _c(_GREY, "╔" + "═" * _W + "╗")
    return bar


def _box_bot() -> str:
    return _c(_GREY, "╚" + "═" * _W + "╝")


def _box_sep() -> str:
    return _c(_GREY, "╠" + "═" * _W + "╣")


def _box_blank() -> str:
    return _c(_GREY, "║") + " " * _W + _c(_GREY, "║")


def _box_divider(label: str) -> str:
    """A section divider: ╠══ LABEL ═…═╣"""
    vis = _vis(label)
    right = _W - vis - 4
    return (
        _c(_GREY, "╠══ ")
        + _c(_AMBER + _BOLD, label)
        + _c(_GREY, " " + "═" * max(right, 0) + "╣")
    )


def _box_row(label: str, value: str) -> str:
    """One data row with fixed-width columns and exact right border."""
    vis_label = _vis(label)
    vis_value = _vis(str(value))
    label_pad = max(_LABEL_W - vis_label, 0)
    used = 2 + vis_label + label_pad + _SEP + vis_value
    right_pad = max(_W - used, 0)
    inner = "  " + label + " " * label_pad + " " * _SEP + str(value) + " " * right_pad
    return _c(_GREY, "║") + inner + _c(_GREY, "║")


def _box_text(text: str, indent: int = 2) -> str:
    """A full-width text row (no label column)."""
    vis = _vis(text)
    pad = max(_W - indent - vis, 0)
    return _c(_GREY, "║") + " " * indent + text + " " * pad + _c(_GREY, "║")


def _box_wrapped(text: str, indent: int = 2, colour: str = "") -> list[str]:
    """Wrap plain *text* to fit inside the box, returning coloured rows."""
    avail = _W - indent
    lines = textwrap.wrap(text, width=avail) or [""]
    rows: list[str] = []
    for line in lines:
        coloured = _c(colour, line) if colour else line
        pad = max(_W - indent - len(line), 0)
        rows.append(_c(_GREY, "║") + " " * indent + coloured + " " * pad + _c(_GREY, "║"))
    return rows


# ---------------------------------------------------------------------------
# Value renderers
# ---------------------------------------------------------------------------

_BYTES_THRESHOLDS = [(1 << 30, "GB"), (1 << 20, "MB"), (1 << 10, "KB"), (1, "B")]


def _human_bytes(n: int | float) -> str:
    for threshold, unit in _BYTES_THRESHOLDS:
        if n >= threshold:
            return f"{n / threshold:.2f} {unit}"
    return f"{n} B"


def _render_value(key: str, value: Any) -> str:
    """Apply semantic formatting to a single value."""
    if isinstance(value, float):
        if "efficiency" in key or "percent" in key:
            if value >= 90:
                colour = _GREEN + _BOLD
            elif value >= 60:
                colour = _AMBER + _BOLD
            else:
                colour = _RED + _BOLD
            return _c(colour, f"{value:.2f}%")
        return f"{value:.4f}".rstrip("0").rstrip(".")

    if isinstance(value, int) and "byte" in key.lower():
        return _human_bytes(value)

    if isinstance(value, bool):
        return _c(_GREEN, "yes") if value else _c(_RED, "no")

    if isinstance(value, list):
        return _c(_LBLUE, ", ".join(str(v) for v in value))

    return str(value)


# ---------------------------------------------------------------------------
# Table renderer
# ---------------------------------------------------------------------------


def _is_table(value: Sequence[Any]) -> bool:
    if not value or not isinstance(value, (list, tuple)):
        return False
    if not all(isinstance(row, dict) for row in value):
        return False
    keys = set(value[0].keys())
    return all(set(row.keys()) == keys for row in value)


def _format_table_rows(rows: list[dict[str, Any]]) -> list[str]:
    if not rows:
        return []
    headers = list(rows[0].keys())
    col_w = {h: max(len(h), *(len(str(r.get(h, ""))) for r in rows)) for h in headers}
    sep_line = "  ".join("─" * col_w[h] for h in headers)
    hdr_line = "  ".join(_c(_TEAL + _BOLD, h.upper().ljust(col_w[h])) for h in headers)
    lines = [hdr_line, _c(_GREY, sep_line)]
    for row in rows:
        lines.append("  ".join(_c(_WHITE, str(row.get(h, "")).ljust(col_w[h])) for h in headers))
    return lines


# ---------------------------------------------------------------------------
# Result interpretation  (works across all 26 inconsistent return shapes)
# ---------------------------------------------------------------------------


def _interpret_result(data: dict[str, Any], entry: AttackEntry | None) -> dict[str, Any]:
    """Derive a normalised verdict from a raw result dict.

    Returns a dict with keys:
        succeeded  bool
        reason     str   — why it failed (empty string on success)
        narrative  str   — plain-English description of what happened
    """
    # --- Determine success -----------------------------------------------
    # Priority: explicit "success" / "error" / "simulated" fields, then
    # heuristics based on packet/request counts.

    explicit_success = data.get("success")
    error_msg        = data.get("error", "")
    simulated        = data.get("simulated", False)

    if error_msg:
        succeeded = False
        reason = str(error_msg)
    elif explicit_success is not None:
        succeeded = bool(explicit_success)
        reason    = "" if succeeded else "Attack reported failure (no detail provided)"
    elif simulated:
        # Scripts that only simulate (BGP hijacking, SSL strip) always "succeed"
        succeeded = True
        reason    = ""
    else:
        # Heuristic: if any meaningful work metric > 0, consider it a success
        work_keys = (
            "packets_sent", "requests_sent", "frames_sent", "fragments_sent",
            "attempts", "vulnerabilities_found", "successful_attacks",
            "credentials_captured", "poison_packets_sent", "requests_sent",
        )
        work_done = any(int(data.get(k, 0) or 0) > 0 for k in work_keys)

        # exit_code = 0 for subprocess-based attacks (slowloris)
        if "exit_code" in data:
            succeeded = data["exit_code"] == 0
            reason    = "" if succeeded else f"Process exited with code {data['exit_code']}"
        elif work_done:
            succeeded = True
            reason    = ""
        else:
            succeeded = False
            reason    = "No work was performed — check permissions and target reachability"

    # Brute-force attacks: distinguish "ran fine" from "credential found"
    brute_found_key = data.get("successful_password") or data.get("password")
    if "attempts" in data and "passwords_loaded" in data:
        # SSH / FTP brute force
        if brute_found_key:
            reason = ""   # found a password = attack goal achieved
        elif succeeded and not brute_found_key:
            # Ran fine but no credential cracked
            reason = "No valid credential found in the provided wordlist"

    # --- Build narrative -------------------------------------------------
    packets  = data.get("packets_sent", data.get("requests_sent", data.get("frames_sent")))
    duration = data.get("duration_seconds", data.get("duration"))
    target   = data.get("target_ip", data.get("target_url", data.get("target", "")))

    parts: list[str] = []

    if simulated:
        parts.append("This attack was simulated — no real network traffic was generated.")
    elif packets is not None and duration is not None:
        rate = packets / duration if duration > 0 else 0
        parts.append(
            f"Sent {packets:,} packet{'s' if packets != 1 else ''} to {target} "
            f"over {duration:.2f}s ({rate:.1f} pkt/s)."
        )
    elif packets is not None:
        parts.append(f"Sent {packets:,} packet{'s' if packets != 1 else ''} to {target}.")

    # Brute-force specifics
    attempts = data.get("attempts")
    if attempts is not None:
        pwd = data.get("successful_password") or data.get("password")
        if pwd:
            parts.append(f"Tried {attempts:,} credential(s) — valid password found: '{pwd}'.")
        else:
            parts.append(f"Tried {attempts:,} credential(s) — no valid password found.")

    # Vulnerability scan specifics
    vulns = data.get("vulnerabilities_found", data.get("successful_attacks"))
    if vulns is not None and attempts is None:
        tested = data.get("payloads_tested", data.get("attempts", "?"))
        parts.append(
            f"Tested {tested} payload(s) — {vulns} vulnerability/vulnerabilities confirmed."
        )

    # Credentials captured
    creds = data.get("credentials_captured")
    if creds is not None:
        out_file = data.get("output_file", "")
        file_note = f" Saved to: {out_file}" if out_file else ""
        parts.append(f"{creds} credential set(s) captured.{file_note}")

    if not parts:
        parts.append("Attack execution completed.")

    narrative = " ".join(parts)

    return {"succeeded": succeeded, "reason": reason, "narrative": narrative}


# ---------------------------------------------------------------------------
# Verdict panel
# ---------------------------------------------------------------------------


def _verdict_panel(data: dict[str, Any], entry: AttackEntry | None) -> list[str]:
    """Return box lines for the STATUS / DESCRIPTION / HOW IT HAPPENED panel."""
    verdict = _interpret_result(data, entry)
    lines: list[str] = []

    lines.append(_box_divider("RESULT"))
    lines.append(_box_blank())

    # Status badge
    if verdict["succeeded"]:
        badge = _c(_GREEN + _BOLD, "✔  SUCCESS")
    else:
        badge = _c(_RED + _BOLD, "✘  FAILED")
    lines.append(_box_text(badge, indent=2))

    # Failure reason
    if not verdict["succeeded"] and verdict["reason"]:
        lines.append(_box_blank())
        lines.append(_box_text(_c(_RED, "Reason:"), indent=2))
        lines.extend(_box_wrapped(verdict["reason"], indent=4, colour=_WHITE + _DIM))

    lines.append(_box_blank())

    # What happened
    lines.append(_box_divider("WHAT HAPPENED"))
    lines.append(_box_blank())
    lines.extend(_box_wrapped(verdict["narrative"], indent=2, colour=_WHITE))
    lines.append(_box_blank())

    # Attack description
    if entry and entry.description:
        lines.append(_box_divider("ABOUT THIS ATTACK"))
        lines.append(_box_blank())
        lines.extend(_box_wrapped(entry.description + ".", indent=2, colour=_DIM + _WHITE))
        cat_label = _c(_TEAL, "Category")
        cat_value = _c(_GREY, entry.category)
        lines.append(_box_blank())
        lines.append(_box_row(cat_label, cat_value))
        lines.append(_box_blank())

    return lines


# ---------------------------------------------------------------------------
# Main text formatter
# ---------------------------------------------------------------------------


def _format_text(data: dict[str, Any], entry: AttackEntry | None = None) -> str:
    lines: list[str] = []

    # Title: attack name + target
    attack_name = (entry.name if entry else data.get("attack", data.get("name", ""))).upper()
    target      = data.get("target_ip", data.get("target_url", ""))
    title_parts = [p for p in [attack_name, str(target).upper()] if p]
    title = "  ·  ".join(title_parts) if title_parts else "RESULTS"

    lines.append("")
    lines.append(_box_top(title))
    lines.append(_box_blank())

    # Skip internal/meta keys already handled in the verdict panel
    _SKIP = {"success", "error", "simulated", "name", "attack"}

    for key, value in data.items():
        if key in _SKIP:
            continue
        # Skip None values — they add no information
        if value is None:
            continue
        label = _c(_TEAL, key.replace("_", " ").title())

        if isinstance(value, (list, tuple)) and _is_table(value):
            lines.append(_box_row(label, ""))
            for trow in _format_table_rows(list(value)):
                vis = _vis(trow)
                pad = max(_W - 4 - vis, 0)
                lines.append(_c(_GREY, "║") + "    " + trow + " " * pad + _c(_GREY, "║"))
        elif isinstance(value, dict):
            lines.append(_box_row(label, ""))
            for sub_key, sub_value in value.items():
                sub_label = _c(_TEAL, ("  " + sub_key.replace("_", " ").title()))
                lines.append(_box_row(sub_label, _render_value(sub_key, sub_value)))
        else:
            lines.append(_box_row(label, _render_value(key, value)))

    lines.append(_box_blank())

    # Verdict panel
    lines.extend(_verdict_panel(data, entry))

    lines.append(_box_bot())
    lines.append("")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# List formatter (used by `matcha list`)
# ---------------------------------------------------------------------------


def format_attack_list(categories: list[dict[str, Any]]) -> str:
    total = sum(len(c.get("attacks", [])) for c in categories)
    lines: list[str] = []

    _NAME_W = 28
    _DESC_W = _W - _NAME_W - 4  # 2 left + 2 right margin

    lines.append("")
    lines.append(_box_top("MATCHA — ATTACK CATALOGUE"))
    lines.append(_box_blank())

    for cat in categories:
        cat_name = cat["category"]
        attacks  = cat.get("attacks", [])
        lines.append(_box_divider(f"{cat_name}  ({len(attacks)})"))
        for atk in attacks:
            name_col = _c(_CYAN, atk["name"].ljust(_NAME_W))
            desc = atk["description"]
            if len(desc) > _DESC_W:
                desc = desc[:_DESC_W - 1] + "…"
            desc_col = _c(_DIM + _WHITE, desc.ljust(_DESC_W))
            lines.append(_c(_GREY, "║") + "  " + name_col + desc_col + "  " + _c(_GREY, "║"))
        lines.append(_box_blank())

    footer = _c(_GREY, f"  {total} attacks total")
    vis = _vis(footer)
    pad = max(_W - vis, 0)
    lines.append(_c(_GREY, "║") + footer + " " * pad + _c(_GREY, "║"))
    lines.append(_box_blank())
    lines.append(_box_bot())
    lines.append("")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Info formatter (used by `matcha info`)
# ---------------------------------------------------------------------------


def format_attack_info(name: str, detail: dict[str, Any]) -> str:
    lines: list[str] = []

    lines.append("")
    lines.append(_box_top(name.upper()))
    lines.append(_box_blank())
    lines.append(_box_row(_c(_TEAL, "Category"), _c(_WHITE, detail["category"])))
    lines.append(_box_blank())

    desc_wrapped = textwrap.wrap(detail["description"], width=_VALUE_W + _LABEL_W)
    for i, dl in enumerate(desc_wrapped):
        label = _c(_TEAL, "Description") if i == 0 else ""
        lines.append(_box_row(label, _c(_WHITE, dl)))

    lines.append(_box_blank())
    lines.append(_box_divider("PARAMETERS"))

    for param in detail.get("parameters", []):
        req_tag = _c(_RED, "required") if param["required"] else _c(_GREY, "optional")
        flag    = _c(_CYAN, f"--{param['name'].replace('_', '-')}")
        type_s  = _c(_DIM + _WHITE, param["type"])
        lines.append(_box_row(flag, f"{type_s}  {req_tag}"))
        if param.get("default") is not None and not param["required"]:
            lines.append(_box_row("", _c(_DIM + _WHITE, f"default: {param['default']}")))
        lines.append(_box_row("", _c(_DIM + _WHITE, param["help"])))
        lines.append(_box_blank())

    lines.append(_box_divider("EXAMPLE"))
    lines.append(_box_blank())
    lines.append(_box_text(_c(_GREEN, detail["example"])))
    lines.append(_box_blank())
    lines.append(_box_bot())
    lines.append("")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Public entry point
# ---------------------------------------------------------------------------


def format_output(
    data: dict[str, Any],
    fmt: str = "text",
    entry: AttackEntry | None = None,
) -> None:
    """Print *data* to stdout in the requested format.

    Parameters
    ----------
    data:
        Dictionary of results returned by an attack's ``execute()`` method.
    fmt:
        ``"text"`` for rich human-readable output or ``"json"`` for raw JSON.
    entry:
        Optional :class:`~matcha.registry.AttackEntry` used to populate the
        description and narrative panels (text mode only).

    Raises
    ------
    ValueError
        If *fmt* is not ``"text"`` or ``"json"``.
    """
    if fmt == "json":
        json.dump(data, sys.stdout, indent=2, default=str)
        sys.stdout.write("\n")
    elif fmt == "text":
        sys.stdout.write(_format_text(data, entry=entry))
    else:
        raise ValueError(f"Unsupported output format: {fmt!r}")
