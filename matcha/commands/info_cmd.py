"""``matcha info <attack>`` command -- display detailed information about an attack."""

from __future__ import annotations

import json
import sys
from typing import Any, Dict, List, Optional

import click

from matcha.commands.list_cmd import CATEGORIES

# ---------------------------------------------------------------------------
# Attack detail registry
# ---------------------------------------------------------------------------
# Each entry maps an attack name to its detailed metadata: description,
# category, constructor parameters (with type and default), and a usage
# example.  Entries are keyed by the attack name used in the CLI.

_ATTACK_DETAILS: Dict[str, Dict[str, Any]] = {
    # --- Network-layer ---
    "arp-spoof": {
        "description": "Perform ARP spoofing attack to associate the attacker's MAC "
                       "address with the IP of a target host.",
        "category": "Network-layer",
        "parameters": [
            {"name": "target_ip", "type": "str", "default": None, "required": True,
             "help": "IP address of the target host"},
            {"name": "gateway_ip", "type": "str", "default": None, "required": True,
             "help": "IP address of the network gateway"},
            {"name": "interval", "type": "float", "default": 1.0, "required": False,
             "help": "Seconds between spoofed ARP packets"},
        ],
        "example": "matcha run arp-spoof --target-ip 192.168.1.10 --gateway-ip 192.168.1.1",
    },
    "bgp-hijacking": {
        "description": "Simulate BGP hijacking by advertising false BGP route "
                       "announcements to divert traffic.",
        "category": "Network-layer",
        "parameters": [
            {"name": "target_prefix", "type": "str", "default": None, "required": True,
             "help": "Target IP prefix to hijack (CIDR notation)"},
            {"name": "as_number", "type": "int", "default": None, "required": True,
             "help": "Autonomous System number to spoof"},
        ],
        "example": "matcha run bgp-hijacking --target-prefix 10.0.0.0/24 --as-number 65001",
    },
    "dhcp-starvation": {
        "description": "Exhaust the DHCP server's address pool by sending a flood of "
                       "DHCP discover requests with randomized MAC addresses.",
        "category": "Network-layer",
        "parameters": [
            {"name": "interface", "type": "str", "default": None, "required": True,
             "help": "Network interface to use"},
            {"name": "count", "type": "int", "default": 1000, "required": False,
             "help": "Number of DHCP discover packets to send"},
        ],
        "example": "matcha run dhcp-starvation --interface eth0 --count 500",
    },
    "dns-amplification": {
        "description": "Perform DNS amplification attack by sending small queries with "
                       "a spoofed source IP to open DNS resolvers.",
        "category": "Network-layer",
        "parameters": [
            {"name": "target_ip", "type": "str", "default": None, "required": True,
             "help": "IP address of the victim to flood"},
            {"name": "dns_server", "type": "str", "default": "8.8.8.8", "required": False,
             "help": "Open DNS resolver to use for amplification"},
            {"name": "count", "type": "int", "default": 1000, "required": False,
             "help": "Number of DNS queries to send"},
        ],
        "example": "matcha run dns-amplification --target-ip 192.168.1.10 --dns-server 8.8.8.8",
    },
    "icmp-flood": {
        "description": "Perform ICMP flood attack (Ping Flood) by sending a large "
                       "volume of ICMP Echo Request packets to the target.",
        "category": "Network-layer",
        "parameters": [
            {"name": "target_ip", "type": "str", "default": None, "required": True,
             "help": "IP address of the target host"},
            {"name": "count", "type": "int", "default": 1000, "required": False,
             "help": "Number of ICMP packets to send"},
            {"name": "size", "type": "int", "default": 64, "required": False,
             "help": "Payload size in bytes"},
        ],
        "example": "matcha run icmp-flood --target-ip 192.168.1.10 --count 5000",
    },
    "mac-flooding": {
        "description": "Perform MAC flooding attack to overflow the switch's CAM table "
                       "by sending frames with random source MAC addresses.",
        "category": "Network-layer",
        "parameters": [
            {"name": "interface", "type": "str", "default": None, "required": True,
             "help": "Network interface to use"},
            {"name": "count", "type": "int", "default": 10000, "required": False,
             "help": "Number of frames to send"},
        ],
        "example": "matcha run mac-flooding --interface eth0 --count 5000",
    },
    "mitm": {
        "description": "Perform Man-in-the-Middle attack using ARP spoofing to "
                       "intercept traffic between two hosts.",
        "category": "Network-layer",
        "parameters": [
            {"name": "target_ip", "type": "str", "default": None, "required": True,
             "help": "IP address of the target host"},
            {"name": "gateway_ip", "type": "str", "default": None, "required": True,
             "help": "IP address of the network gateway"},
            {"name": "forward", "type": "bool", "default": True, "required": False,
             "help": "Enable IP forwarding to relay intercepted traffic"},
        ],
        "example": "matcha run mitm --target-ip 192.168.1.10 --gateway-ip 192.168.1.1",
    },
    "ntp-amplification": {
        "description": "Perform NTP amplification attack by sending monlist requests "
                       "to NTP servers with a spoofed source IP.",
        "category": "Network-layer",
        "parameters": [
            {"name": "target_ip", "type": "str", "default": None, "required": True,
             "help": "IP address of the victim to flood"},
            {"name": "ntp_server", "type": "str", "default": None, "required": True,
             "help": "NTP server to use for amplification"},
            {"name": "count", "type": "int", "default": 1000, "required": False,
             "help": "Number of NTP requests to send"},
        ],
        "example": "matcha run ntp-amplification --target-ip 192.168.1.10 --ntp-server 10.0.0.1",
    },
    "ping-of-death": {
        "description": "Perform Ping of Death attack by sending oversized ICMP packets "
                       "that exceed the maximum allowed size.",
        "category": "Network-layer",
        "parameters": [
            {"name": "target_ip", "type": "str", "default": None, "required": True,
             "help": "IP address of the target host"},
            {"name": "count", "type": "int", "default": 100, "required": False,
             "help": "Number of oversized packets to send"},
        ],
        "example": "matcha run ping-of-death --target-ip 192.168.1.10 --count 50",
    },
    "smurf-attack": {
        "description": "Perform Smurf amplification attack by sending ICMP Echo Requests "
                       "to a broadcast address with a spoofed source IP.",
        "category": "Network-layer",
        "parameters": [
            {"name": "target_ip", "type": "str", "default": None, "required": True,
             "help": "IP address of the victim"},
            {"name": "broadcast_ip", "type": "str", "default": None, "required": True,
             "help": "Broadcast address to send ICMP requests to"},
            {"name": "count", "type": "int", "default": 1000, "required": False,
             "help": "Number of ICMP packets to send"},
        ],
        "example": "matcha run smurf-attack --target-ip 192.168.1.10 --broadcast-ip 192.168.1.255",
    },
    "syn-flood": {
        "description": "Perform SYN flood attack by sending a large number of TCP SYN "
                       "packets to exhaust the target's connection resources.",
        "category": "Network-layer",
        "parameters": [
            {"name": "target_ip", "type": "str", "default": None, "required": True,
             "help": "IP address of the target host"},
            {"name": "target_port", "type": "int", "default": 80, "required": False,
             "help": "Target TCP port"},
            {"name": "count", "type": "int", "default": 1000, "required": False,
             "help": "Number of SYN packets to send"},
        ],
        "example": "matcha run syn-flood --target-ip 192.168.1.10 --target-port 80",
    },
    "udp-flood": {
        "description": "Perform UDP flood attack by sending a large volume of UDP "
                       "packets to random ports on the target.",
        "category": "Network-layer",
        "parameters": [
            {"name": "target_ip", "type": "str", "default": None, "required": True,
             "help": "IP address of the target host"},
            {"name": "target_port", "type": "int", "default": 53, "required": False,
             "help": "Target UDP port"},
            {"name": "count", "type": "int", "default": 1000, "required": False,
             "help": "Number of UDP packets to send"},
        ],
        "example": "matcha run udp-flood --target-ip 192.168.1.10 --target-port 53",
    },
    # --- Application-layer ---
    "credential-harvester": {
        "description": "Perform credential harvesting attack by cloning a target login "
                       "page and capturing submitted credentials.",
        "category": "Application-layer",
        "parameters": [
            {"name": "target_url", "type": "str", "default": None, "required": True,
             "help": "URL of the login page to clone"},
            {"name": "listen_port", "type": "int", "default": 8080, "required": False,
             "help": "Port to serve the cloned page on"},
        ],
        "example": "matcha run credential-harvester --target-url https://example.com/login",
    },
    "directory-traversal": {
        "description": "Perform directory traversal attack to access files outside "
                       "the web root directory.",
        "category": "Application-layer",
        "parameters": [
            {"name": "target_url", "type": "str", "default": None, "required": True,
             "help": "Base URL of the target web application"},
            {"name": "depth", "type": "int", "default": 5, "required": False,
             "help": "Maximum traversal depth to attempt"},
        ],
        "example": "matcha run directory-traversal --target-url http://example.com/page?file=test",
    },
    "ftp-brute-force": {
        "description": "Perform FTP brute force attack by trying common username and "
                       "password combinations against the target FTP server.",
        "category": "Application-layer",
        "parameters": [
            {"name": "target_ip", "type": "str", "default": None, "required": True,
             "help": "IP address of the FTP server"},
            {"name": "username", "type": "str", "default": "admin", "required": False,
             "help": "Username to brute force"},
            {"name": "wordlist", "type": "str", "default": None, "required": True,
             "help": "Path to the password wordlist file"},
        ],
        "example": "matcha run ftp-brute-force --target-ip 192.168.1.10 --wordlist passwords.txt",
    },
    "http-dos": {
        "description": "Perform HTTP DoS attack by sending malformed or resource-intensive "
                       "HTTP requests to the target server.",
        "category": "Application-layer",
        "parameters": [
            {"name": "target_url", "type": "str", "default": None, "required": True,
             "help": "URL of the target web server"},
            {"name": "threads", "type": "int", "default": 10, "required": False,
             "help": "Number of concurrent threads"},
        ],
        "example": "matcha run http-dos --target-url http://example.com --threads 20",
    },
    "http-flood": {
        "description": "Perform HTTP flood attack by sending a high volume of HTTP "
                       "requests to overwhelm the target web server.",
        "category": "Application-layer",
        "parameters": [
            {"name": "target_url", "type": "str", "default": None, "required": True,
             "help": "URL of the target web server"},
            {"name": "count", "type": "int", "default": 10000, "required": False,
             "help": "Number of HTTP requests to send"},
            {"name": "threads", "type": "int", "default": 10, "required": False,
             "help": "Number of concurrent threads"},
        ],
        "example": "matcha run http-flood --target-url http://example.com --count 5000",
    },
    "rdp-brute-force": {
        "description": "Perform RDP brute force attack by trying common credentials "
                       "against the target Remote Desktop Protocol server.",
        "category": "Application-layer",
        "parameters": [
            {"name": "target_ip", "type": "str", "default": None, "required": True,
             "help": "IP address of the RDP server"},
            {"name": "username", "type": "str", "default": "administrator", "required": False,
             "help": "Username to brute force"},
            {"name": "wordlist", "type": "str", "default": None, "required": True,
             "help": "Path to the password wordlist file"},
        ],
        "example": "matcha run rdp-brute-force --target-ip 192.168.1.10 --wordlist passwords.txt",
    },
    "slowloris": {
        "description": "Perform Slowloris attack by opening many connections to the "
                       "target and sending partial HTTP requests to keep them open.",
        "category": "Application-layer",
        "parameters": [
            {"name": "target_ip", "type": "str", "default": None, "required": True,
             "help": "IP address of the target web server"},
            {"name": "target_port", "type": "int", "default": 80, "required": False,
             "help": "Target HTTP port"},
            {"name": "sockets", "type": "int", "default": 200, "required": False,
             "help": "Number of sockets to open"},
        ],
        "example": "matcha run slowloris --target-ip 192.168.1.10 --sockets 500",
    },
    "sql-injection": {
        "description": "Perform SQL injection attack by injecting malicious SQL "
                       "statements through vulnerable input fields.",
        "category": "Application-layer",
        "parameters": [
            {"name": "target_url", "type": "str", "default": None, "required": True,
             "help": "URL of the vulnerable web page"},
            {"name": "parameter", "type": "str", "default": None, "required": True,
             "help": "Vulnerable query parameter name"},
        ],
        "example": "matcha run sql-injection --target-url http://example.com/search --parameter q",
    },
    "ssh-brute-force": {
        "description": "Perform SSH brute force attack by trying common credentials "
                       "against the target SSH server.",
        "category": "Application-layer",
        "parameters": [
            {"name": "target_ip", "type": "str", "default": None, "required": True,
             "help": "IP address of the SSH server"},
            {"name": "username", "type": "str", "default": "root", "required": False,
             "help": "Username to brute force"},
            {"name": "wordlist", "type": "str", "default": None, "required": True,
             "help": "Path to the password wordlist file"},
        ],
        "example": "matcha run ssh-brute-force --target-ip 192.168.1.10 --wordlist passwords.txt",
    },
    "ssl-strip": {
        "description": "Perform SSL Strip attack by downgrading HTTPS connections to "
                       "HTTP to intercept encrypted traffic.",
        "category": "Application-layer",
        "parameters": [
            {"name": "target_ip", "type": "str", "default": None, "required": True,
             "help": "IP address of the target host"},
            {"name": "gateway_ip", "type": "str", "default": None, "required": True,
             "help": "IP address of the network gateway"},
            {"name": "listen_port", "type": "int", "default": 10000, "required": False,
             "help": "Port for the SSL stripping proxy"},
        ],
        "example": "matcha run ssl-strip --target-ip 192.168.1.10 --gateway-ip 192.168.1.1",
    },
    "vlan-hopping": {
        "description": "Perform VLAN hopping attack to gain access to traffic on "
                       "other VLANs by exploiting switch misconfigurations.",
        "category": "Application-layer",
        "parameters": [
            {"name": "interface", "type": "str", "default": None, "required": True,
             "help": "Network interface to use"},
            {"name": "target_vlan", "type": "int", "default": None, "required": True,
             "help": "VLAN ID to hop to"},
        ],
        "example": "matcha run vlan-hopping --interface eth0 --target-vlan 100",
    },
    "xss": {
        "description": "Perform XSS vulnerability testing by injecting JavaScript "
                       "payloads into vulnerable web page inputs.",
        "category": "Application-layer",
        "parameters": [
            {"name": "target_url", "type": "str", "default": None, "required": True,
             "help": "URL of the target web page"},
            {"name": "parameter", "type": "str", "default": None, "required": True,
             "help": "Vulnerable query parameter name"},
        ],
        "example": "matcha run xss --target-url http://example.com/search --parameter q",
    },
    "xxe": {
        "description": "Perform XML External Entity attack by injecting malicious XML "
                       "entities to read local files or trigger SSRF.",
        "category": "Application-layer",
        "parameters": [
            {"name": "target_url", "type": "str", "default": None, "required": True,
             "help": "URL of the XML-accepting endpoint"},
            {"name": "payload_file", "type": "str", "default": None, "required": False,
             "help": "Path to a custom XXE payload file"},
        ],
        "example": "matcha run xxe --target-url http://example.com/api/xml",
    },
    # --- Replay ---
    "pcap-replay": {
        "description": "Replay captured network traffic from PCAP files to reproduce "
                       "previously observed network conditions or attacks.",
        "category": "Replay",
        "parameters": [
            {"name": "pcap_file", "type": "str", "default": None, "required": True,
             "help": "Path to the PCAP file to replay"},
            {"name": "interface", "type": "str", "default": None, "required": True,
             "help": "Network interface to replay traffic on"},
            {"name": "speed", "type": "float", "default": 1.0, "required": False,
             "help": "Replay speed multiplier (1.0 = original speed)"},
        ],
        "example": "matcha run pcap-replay --pcap-file capture.pcap --interface eth0",
    },
}


def get_attack_names() -> List[str]:
    """Return a sorted list of all known attack names."""
    return sorted(_ATTACK_DETAILS.keys())


def lookup_attack(name: str) -> Optional[Dict[str, Any]]:
    """Return detail dict for *name*, or ``None`` if not found."""
    return _ATTACK_DETAILS.get(name)


# ---------------------------------------------------------------------------
# Text formatter
# ---------------------------------------------------------------------------

def _format_text(name: str, detail: Dict[str, Any]) -> str:
    """Return a human-readable info page for an attack."""
    lines: list[str] = []
    lines.append(f"Attack:      {name}")
    lines.append(f"Category:    {detail['category']}")
    lines.append(f"Description: {detail['description']}")
    lines.append("")
    lines.append("Parameters:")
    for param in detail["parameters"]:
        req = "required" if param["required"] else "optional"
        default_part = ""
        if not param["required"] and param["default"] is not None:
            default_part = f", default: {param['default']}"
        lines.append(
            f"  --{param['name'].replace('_', '-'):20s} "
            f"({param['type']}, {req}{default_part})"
        )
        lines.append(f"    {' ' * 20} {param['help']}")
    lines.append("")
    lines.append(f"Example:")
    lines.append(f"  {detail['example']}")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# JSON formatter
# ---------------------------------------------------------------------------

def _format_json(name: str, detail: Dict[str, Any]) -> str:
    """Return the attack detail as a JSON string."""
    payload: Dict[str, Any] = {
        "name": name,
        "category": detail["category"],
        "description": detail["description"],
        "parameters": detail["parameters"],
        "example": detail["example"],
    }
    return json.dumps(payload, indent=2)


# ---------------------------------------------------------------------------
# Click command
# ---------------------------------------------------------------------------

@click.command("info")
@click.argument("attack")
@click.pass_context
def info_cmd(ctx: click.Context, attack: str) -> None:
    """Show detailed information about a specific attack."""
    detail = lookup_attack(attack)
    if detail is None:
        known = ", ".join(get_attack_names()[:5]) + ", ..."
        click.echo(f"Error: unknown attack {attack!r}. Known attacks: {known}", err=True)
        ctx.exit(2)
        return

    fmt = ctx.obj.get("output", "text")
    if fmt == "json":
        sys.stdout.write(_format_json(attack, detail))
        sys.stdout.write("\n")
    else:
        sys.stdout.write(_format_text(attack, detail))
        sys.stdout.write("\n")
