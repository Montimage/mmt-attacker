"""``matcha list`` command -- display all available attacks grouped by category."""

from __future__ import annotations

import json
import sys
from typing import Any

import click

# ---------------------------------------------------------------------------
# Attack catalog
# ---------------------------------------------------------------------------
# Each entry is (name, one-line description).
# Grouped into the three categories defined by the project spec.

NETWORK_LAYER: list[dict[str, str]] = [
    {"name": "arp-spoof", "description": "Perform ARP spoofing attack"},
    {"name": "bgp-hijacking", "description": "Perform BGP hijacking simulation"},
    {"name": "dhcp-starvation", "description": "Perform DHCP starvation attack"},
    {"name": "dns-amplification", "description": "Perform DNS amplification attack"},
    {"name": "icmp-flood", "description": "Perform ICMP flood attack (Ping Flood)"},
    {"name": "mac-flooding", "description": "Perform MAC flooding attack"},
    {"name": "mitm", "description": "Perform Man-in-the-Middle attack using ARP spoofing"},
    {"name": "ntp-amplification", "description": "Perform NTP amplification attack"},
    {"name": "ping-of-death", "description": "Perform Ping of Death attack"},
    {"name": "smurf-attack", "description": "Perform Smurf amplification attack"},
    {"name": "syn-flood", "description": "Perform SYN flood attack"},
    {"name": "udp-flood", "description": "Perform UDP flood attack"},
]

APPLICATION_LAYER: list[dict[str, str]] = [
    {"name": "credential-harvester", "description": "Perform credential harvesting attack"},
    {"name": "directory-traversal", "description": "Perform directory traversal attack"},
    {"name": "ftp-brute-force", "description": "Perform FTP brute force attack"},
    {"name": "http-dos", "description": "Perform HTTP DoS attack"},
    {"name": "http-flood", "description": "Perform HTTP flood attack"},
    {"name": "rdp-brute-force", "description": "Perform RDP brute force attack"},
    {"name": "slowloris", "description": "Perform Slowloris attack"},
    {"name": "sql-injection", "description": "Perform SQL injection attack"},
    {"name": "ssh-brute-force", "description": "Perform SSH brute force attack"},
    {"name": "ssl-strip", "description": "Perform SSL Strip attack"},
    {"name": "vlan-hopping", "description": "Perform VLAN hopping attack"},
    {"name": "xss", "description": "Perform XSS vulnerability testing"},
    {"name": "xxe", "description": "Perform XXE attack"},
]

REPLAY: list[dict[str, str]] = [
    {"name": "pcap-replay", "description": "Replay captured network traffic from PCAP files"},
]

CATEGORIES: list[dict[str, Any]] = [
    {"category": "Network-layer", "attacks": NETWORK_LAYER},
    {"category": "Application-layer", "attacks": APPLICATION_LAYER},
    {"category": "Replay", "attacks": REPLAY},
]


def _total_attacks() -> int:
    return sum(len(c["attacks"]) for c in CATEGORIES)


# ---------------------------------------------------------------------------
# Text formatter
# ---------------------------------------------------------------------------


def _format_text() -> str:
    """Return a human-readable categorized attack list."""
    lines: list[str] = []
    for cat in CATEGORIES:
        header = f"{cat['category']} ({len(cat['attacks'])} attacks)"
        lines.append(header)
        lines.append("-" * len(header))
        for atk in cat["attacks"]:
            lines.append(f"  {atk['name']:25s} {atk['description']}")
        lines.append("")
    lines.append(f"Total: {_total_attacks()} attacks")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# JSON formatter
# ---------------------------------------------------------------------------


def _format_json() -> str:
    """Return the attack catalog as a JSON string."""
    payload: list[dict[str, Any]] = []
    for cat in CATEGORIES:
        for atk in cat["attacks"]:
            payload.append(
                {
                    "name": atk["name"],
                    "category": cat["category"],
                    "description": atk["description"],
                }
            )
    return json.dumps(payload, indent=2)


# ---------------------------------------------------------------------------
# Click command
# ---------------------------------------------------------------------------


@click.command("list")
@click.pass_context
def list_cmd(ctx: click.Context) -> None:
    """List all available attacks grouped by category."""
    fmt = ctx.obj.get("output", "text")
    if fmt == "json":
        sys.stdout.write(_format_json())
        sys.stdout.write("\n")
    else:
        sys.stdout.write(_format_text())
        sys.stdout.write("\n")
