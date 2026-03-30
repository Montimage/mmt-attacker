"""``matcha syn-flood`` command -- execute a SYN flood attack simulation."""

from __future__ import annotations

import ipaddress
import logging
import os
import sys
from typing import List

import click

from matcha.output import format_output

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def parse_ports(port_string: str) -> List[int]:
    """Parse a comma-separated port list (ranges supported).

    Examples:
        ``"80"`` -> ``[80]``
        ``"80,443"`` -> ``[80, 443]``
        ``"8000-8002"`` -> ``[8000, 8001, 8002]``

    Returns an empty list when no valid ports are found.
    """
    ports: list[int] = []
    for part in port_string.split(","):
        part = part.strip()
        if "-" in part:
            try:
                start_s, end_s = part.split("-", 1)
                start, end = int(start_s), int(end_s)
                if end - start > 1000:
                    end = start + 1000
                ports.extend(range(start, end + 1))
            except ValueError:
                continue
        else:
            try:
                ports.append(int(part))
            except ValueError:
                continue

    # Filter valid & deduplicate while preserving order.
    seen: set[int] = set()
    valid: list[int] = []
    for p in ports:
        if 0 < p < 65536 and p not in seen:
            valid.append(p)
            seen.add(p)
    return valid


def validate_target_ip(ip: str) -> bool:
    """Return *True* when *ip* is a valid IPv4/IPv6 address."""
    try:
        ipaddress.ip_address(ip)
        return True
    except ValueError:
        return False


def _load_syn_flood_class():
    """Import and return ``SYNFloodAttack`` from the scripts package.

    The ``scripts/`` directory lives at the project root and is not a proper
    Python package (no ``__init__.py``).  We add the project root to
    ``sys.path`` when needed so the import resolves.
    """
    _project_root = os.path.dirname(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    )
    if _project_root not in sys.path:
        sys.path.insert(0, _project_root)

    from scripts.syn_flood.syn_flood import SYNFloodAttack  # type: ignore[import]

    return SYNFloodAttack


# ---------------------------------------------------------------------------
# Click command
# ---------------------------------------------------------------------------


@click.command("syn-flood")
@click.option(
    "--target",
    required=True,
    help="Target IP address.",
)
@click.option(
    "--ports",
    required=True,
    help="Comma-separated port list (ranges allowed, e.g. 80,443,8000-8080).",
)
@click.option(
    "--count",
    default=1000,
    type=int,
    show_default=True,
    help="Number of SYN packets to send.",
)
@click.option(
    "--rate",
    default=100,
    type=int,
    show_default=True,
    help="Packets per second.",
)
@click.option(
    "--spoof-ip/--no-spoof-ip",
    default=True,
    show_default=True,
    help="Use random source IPs.",
)
@click.pass_context
def syn_flood_cmd(
    ctx: click.Context,
    target: str,
    ports: str,
    count: int,
    rate: int,
    spoof_ip: bool,
) -> None:
    """Execute a SYN flood attack simulation against a target."""
    # ---- Validate target IP ------------------------------------------------
    if not validate_target_ip(target):
        click.echo(f"Error: invalid target IP address: {target!r}", err=True)
        ctx.exit(2)
        return

    # ---- Parse & validate ports -------------------------------------------
    port_list = parse_ports(ports)
    if not port_list:
        click.echo(f"Error: no valid ports in {ports!r}", err=True)
        ctx.exit(2)
        return

    # ---- Load attack class & execute --------------------------------------
    SYNFloodAttack = _load_syn_flood_class()

    verbose = ctx.obj.get("verbose", False)

    attack = SYNFloodAttack(
        target_ip=target,
        ports=port_list,
        packet_count=count,
        rate=rate,
        spoof_ip=spoof_ip,
        verbose=verbose,
    )

    result = attack.execute()

    # ---- Format output -----------------------------------------------------
    fmt = ctx.obj.get("output", "text")
    format_output(result, fmt=fmt)
