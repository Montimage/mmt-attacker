"""Centralized attack registry -- single source of truth for all attack metadata.

Maps CLI attack names to script module paths, class names, categories,
constructor parameter definitions, and one-line descriptions.  Used by
``matcha list``, ``matcha info``, and the command factory.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

# ---------------------------------------------------------------------------
# Data classes
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class ParamDef:
    """Definition of a single constructor / CLI parameter."""

    name: str
    type: str
    required: bool
    default: Any = None
    help: str = ""


@dataclass(frozen=True)
class AttackEntry:
    """Metadata for a single registered attack."""

    name: str
    description: str
    category: str
    module_path: str
    class_name: str
    params: list[ParamDef] = field(default_factory=list)


# ---------------------------------------------------------------------------
# Category constants
# ---------------------------------------------------------------------------

CATEGORY_NETWORK = "Network-layer"
CATEGORY_APPLICATION = "Application-layer"
CATEGORY_REPLAY = "Replay"

_CATEGORIES = (CATEGORY_NETWORK, CATEGORY_APPLICATION, CATEGORY_REPLAY)


# ---------------------------------------------------------------------------
# Internal registry storage
# ---------------------------------------------------------------------------

_REGISTRY: dict[str, AttackEntry] = {}


def _register(entry: AttackEntry) -> None:
    """Add *entry* to the global registry (used at module load time)."""
    if entry.name in _REGISTRY:
        raise ValueError(f"Duplicate attack name: {entry.name!r}")
    _REGISTRY[entry.name] = entry


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


def get_attack(name: str) -> AttackEntry:
    """Return the registry entry for *name*.

    Raises
    ------
    KeyError
        If *name* is not a registered attack.
    """
    try:
        return _REGISTRY[name]
    except KeyError:
        raise KeyError(f"Unknown attack: {name!r}") from None


def list_attacks() -> dict[str, list[AttackEntry]]:
    """Return all registered attacks grouped by category.

    Returns a dict keyed by category name whose values are lists of
    :class:`AttackEntry` sorted alphabetically by attack name.
    """
    grouped: dict[str, list[AttackEntry]] = {cat: [] for cat in _CATEGORIES}
    for entry in _REGISTRY.values():
        grouped.setdefault(entry.category, []).append(entry)
    for entries in grouped.values():
        entries.sort(key=lambda e: e.name)
    return grouped


def all_attack_names() -> list[str]:
    """Return a sorted list of every registered attack name."""
    return sorted(_REGISTRY.keys())


# ---------------------------------------------------------------------------
# Attack registrations  (26 attacks)
# ---------------------------------------------------------------------------

# --- Network-layer (12) ---

_register(
    AttackEntry(
        name="arp-spoof",
        description="Perform ARP spoofing attack to associate the attacker's MAC address with the IP of a target host",
        category=CATEGORY_NETWORK,
        module_path="scripts.arp_spoofing.arp_spoof",
        class_name="ARPSpoofingAttack",
        params=[
            ParamDef("target_ip", "str", True, None, "IP address of the target host"),
            ParamDef("gateway_ip", "str", True, None, "IP address of the network gateway"),
            ParamDef("interval", "float", False, 1.0, "Seconds between spoofed ARP packets"),
        ],
    )
)

_register(
    AttackEntry(
        name="bgp-hijacking",
        description="Simulate BGP hijacking by advertising false BGP route announcements to divert traffic",
        category=CATEGORY_NETWORK,
        module_path="scripts.bgp_hijacking.bgp_hijacking",
        class_name="BGPHijackingAttack",
        params=[
            ParamDef(
                "target_prefix", "str", True, None, "Target IP prefix to hijack (CIDR notation)"
            ),
            ParamDef("as_number", "int", True, None, "Autonomous System number to spoof"),
        ],
    )
)

_register(
    AttackEntry(
        name="dhcp-starvation",
        description="Exhaust the DHCP server's address pool by flooding DHCP discover requests with randomized MACs",
        category=CATEGORY_NETWORK,
        module_path="scripts.dhcp_starvation.dhcp_starvation",
        class_name="DHCPStarvationAttack",
        params=[
            ParamDef("interface", "str", True, None, "Network interface to use"),
            ParamDef("count", "int", False, 1000, "Number of DHCP discover packets to send"),
        ],
    )
)

_register(
    AttackEntry(
        name="dns-amplification",
        description="Perform DNS amplification attack by sending small queries with a spoofed source IP to open resolvers",
        category=CATEGORY_NETWORK,
        module_path="scripts.dns_amplification.dns_amplification",
        class_name="DNSAmplificationAttack",
        params=[
            ParamDef("target_ip", "str", True, None, "IP address of the victim to flood"),
            ParamDef(
                "dns_server", "str", False, "8.8.8.8", "Open DNS resolver to use for amplification"
            ),
            ParamDef("count", "int", False, 1000, "Number of DNS queries to send"),
        ],
    )
)

_register(
    AttackEntry(
        name="icmp-flood",
        description="Perform ICMP flood attack (Ping Flood) by sending a large volume of ICMP Echo Request packets",
        category=CATEGORY_NETWORK,
        module_path="scripts.icmp_flood.icmp_flood",
        class_name="ICMPFloodAttack",
        params=[
            ParamDef("target_ip", "str", True, None, "IP address of the target host"),
            ParamDef("count", "int", False, 1000, "Number of ICMP packets to send"),
            ParamDef("size", "int", False, 64, "Payload size in bytes"),
        ],
    )
)

_register(
    AttackEntry(
        name="mac-flooding",
        description="Perform MAC flooding attack to overflow the switch's CAM table with random source MACs",
        category=CATEGORY_NETWORK,
        module_path="scripts.mac_flooding.mac_flooding",
        class_name="MACFloodingAttack",
        params=[
            ParamDef("interface", "str", True, None, "Network interface to use"),
            ParamDef("count", "int", False, 10000, "Number of frames to send"),
        ],
    )
)

_register(
    AttackEntry(
        name="mitm",
        description="Perform Man-in-the-Middle attack using ARP spoofing to intercept traffic between two hosts",
        category=CATEGORY_NETWORK,
        module_path="scripts.mitm.mitm",
        class_name="MITMAttack",
        params=[
            ParamDef("target_ip", "str", True, None, "IP address of the target host"),
            ParamDef("gateway_ip", "str", True, None, "IP address of the network gateway"),
            ParamDef(
                "forward", "bool", False, True, "Enable IP forwarding to relay intercepted traffic"
            ),
        ],
    )
)

_register(
    AttackEntry(
        name="ntp-amplification",
        description="Perform NTP amplification attack by sending monlist requests with a spoofed source IP",
        category=CATEGORY_NETWORK,
        module_path="scripts.ntp_amplification.ntp_amplification",
        class_name="NTPAmplificationAttack",
        params=[
            ParamDef("target_ip", "str", True, None, "IP address of the victim to flood"),
            ParamDef("ntp_server", "str", True, None, "NTP server to use for amplification"),
            ParamDef("count", "int", False, 1000, "Number of NTP requests to send"),
        ],
    )
)

_register(
    AttackEntry(
        name="ping-of-death",
        description="Perform Ping of Death attack by sending oversized ICMP packets that exceed the maximum allowed size",
        category=CATEGORY_NETWORK,
        module_path="scripts.ping_of_death.ping_of_death",
        class_name="PingOfDeathAttack",
        params=[
            ParamDef("target_ip", "str", True, None, "IP address of the target host"),
            ParamDef("count", "int", False, 100, "Number of oversized packets to send"),
        ],
    )
)

_register(
    AttackEntry(
        name="smurf-attack",
        description="Perform Smurf amplification attack by sending ICMP Echo Requests to a broadcast address with a spoofed source IP",
        category=CATEGORY_NETWORK,
        module_path="scripts.smurf_attack.smurf_attack",
        class_name="SmurfAttack",
        params=[
            ParamDef("target_ip", "str", True, None, "IP address of the victim"),
            ParamDef(
                "broadcast_ip", "str", True, None, "Broadcast address to send ICMP requests to"
            ),
            ParamDef("count", "int", False, 1000, "Number of ICMP packets to send"),
        ],
    )
)

_register(
    AttackEntry(
        name="syn-flood",
        description="Perform SYN flood attack by sending a large number of TCP SYN packets to exhaust the target's connection resources",
        category=CATEGORY_NETWORK,
        module_path="scripts.syn_flood.syn_flood",
        class_name="SYNFloodAttack",
        params=[
            ParamDef("target_ip", "str", True, None, "IP address of the target host"),
            ParamDef("target_port", "int", False, 80, "Target TCP port"),
            ParamDef("count", "int", False, 1000, "Number of SYN packets to send"),
        ],
    )
)

_register(
    AttackEntry(
        name="udp-flood",
        description="Perform UDP flood attack by sending a large volume of UDP packets to random ports on the target",
        category=CATEGORY_NETWORK,
        module_path="scripts.udp_flood.udp_flood",
        class_name="UDPFloodAttack",
        params=[
            ParamDef("target_ip", "str", True, None, "IP address of the target host"),
            ParamDef("target_port", "int", False, 53, "Target UDP port"),
            ParamDef("count", "int", False, 1000, "Number of UDP packets to send"),
        ],
    )
)

# --- Application-layer (13) ---

_register(
    AttackEntry(
        name="credential-harvester",
        description="Perform credential harvesting attack by cloning a target login page and capturing submitted credentials",
        category=CATEGORY_APPLICATION,
        module_path="scripts.credential_harvester.credential_harvester",
        class_name="CredentialHarvester",
        params=[
            ParamDef("target_url", "str", True, None, "URL of the login page to clone"),
            ParamDef("listen_port", "int", False, 8080, "Port to serve the cloned page on"),
        ],
    )
)

_register(
    AttackEntry(
        name="directory-traversal",
        description="Perform directory traversal attack to access files outside the web root directory",
        category=CATEGORY_APPLICATION,
        module_path="scripts.directory_traversal.directory_traversal",
        class_name="DirectoryTraversalAttack",
        params=[
            ParamDef("target_url", "str", True, None, "Base URL of the target web application"),
            ParamDef("depth", "int", False, 5, "Maximum traversal depth to attempt"),
        ],
    )
)

_register(
    AttackEntry(
        name="ftp-brute-force",
        description="Perform FTP brute force attack by trying common username and password combinations",
        category=CATEGORY_APPLICATION,
        module_path="scripts.ftp_brute_force.ftp_brute_force",
        class_name="FTPBruteForceAttack",
        params=[
            ParamDef("target_ip", "str", True, None, "IP address of the FTP server"),
            ParamDef("username", "str", False, "admin", "Username to brute force"),
            ParamDef("wordlist", "str", True, None, "Path to the password wordlist file"),
        ],
    )
)

_register(
    AttackEntry(
        name="http-dos",
        description="Perform HTTP DoS attack by sending malformed or resource-intensive HTTP requests",
        category=CATEGORY_APPLICATION,
        module_path="scripts.http_dos.http_dos",
        class_name="HTTPDoSAttack",
        params=[
            ParamDef("target_url", "str", True, None, "URL of the target web server"),
            ParamDef("threads", "int", False, 10, "Number of concurrent threads"),
        ],
    )
)

_register(
    AttackEntry(
        name="http-flood",
        description="Perform HTTP flood attack by sending a high volume of HTTP requests to overwhelm the target",
        category=CATEGORY_APPLICATION,
        module_path="scripts.http_flood.http_flood",
        class_name="HTTPFloodAttack",
        params=[
            ParamDef("target_url", "str", True, None, "URL of the target web server"),
            ParamDef("count", "int", False, 10000, "Number of HTTP requests to send"),
            ParamDef("threads", "int", False, 10, "Number of concurrent threads"),
        ],
    )
)

_register(
    AttackEntry(
        name="rdp-brute-force",
        description="Perform RDP brute force attack by trying common credentials against the target RDP server",
        category=CATEGORY_APPLICATION,
        module_path="scripts.rdp_brute_force.rdp_brute_force",
        class_name="RDPBruteForceAttack",
        params=[
            ParamDef("target_ip", "str", True, None, "IP address of the RDP server"),
            ParamDef("username", "str", False, "administrator", "Username to brute force"),
            ParamDef("wordlist", "str", True, None, "Path to the password wordlist file"),
        ],
    )
)

_register(
    AttackEntry(
        name="slowloris",
        description="Perform Slowloris attack by opening many connections and sending partial HTTP requests to keep them open",
        category=CATEGORY_APPLICATION,
        module_path="scripts.slowloris.slowloris",
        class_name="SlowlorisAttack",
        params=[
            ParamDef("target_ip", "str", True, None, "IP address of the target web server"),
            ParamDef("target_port", "int", False, 80, "Target HTTP port"),
            ParamDef("sockets", "int", False, 200, "Number of sockets to open"),
        ],
    )
)

_register(
    AttackEntry(
        name="sql-injection",
        description="Perform SQL injection attack by injecting malicious SQL statements through vulnerable input fields",
        category=CATEGORY_APPLICATION,
        module_path="scripts.sql_injection.sql_injection",
        class_name="SQLInjectionAttack",
        params=[
            ParamDef("target_url", "str", True, None, "URL of the vulnerable web page"),
            ParamDef("parameter", "str", True, None, "Vulnerable query parameter name"),
        ],
    )
)

_register(
    AttackEntry(
        name="ssh-brute-force",
        description="Perform SSH brute force attack by trying common credentials against the target SSH server",
        category=CATEGORY_APPLICATION,
        module_path="scripts.ssh_brute_force.ssh_brute_force",
        class_name="SSHBruteForceAttack",
        params=[
            ParamDef("target_ip", "str", True, None, "IP address of the SSH server"),
            ParamDef("username", "str", False, "root", "Username to brute force"),
            ParamDef("wordlist", "str", True, None, "Path to the password wordlist file"),
        ],
    )
)

_register(
    AttackEntry(
        name="ssl-strip",
        description="Perform SSL Strip attack by downgrading HTTPS connections to HTTP to intercept encrypted traffic",
        category=CATEGORY_APPLICATION,
        module_path="scripts.ssl_strip.ssl_strip",
        class_name="SSLStripAttack",
        params=[
            ParamDef("target_ip", "str", True, None, "IP address of the target host"),
            ParamDef("gateway_ip", "str", True, None, "IP address of the network gateway"),
            ParamDef("listen_port", "int", False, 10000, "Port for the SSL stripping proxy"),
        ],
    )
)

_register(
    AttackEntry(
        name="vlan-hopping",
        description="Perform VLAN hopping attack to gain access to traffic on other VLANs by exploiting switch misconfigurations",
        category=CATEGORY_APPLICATION,
        module_path="scripts.vlan_hopping.vlan_hopping",
        class_name="VLANHoppingAttack",
        params=[
            ParamDef("interface", "str", True, None, "Network interface to use"),
            ParamDef("target_vlan", "int", True, None, "VLAN ID to hop to"),
        ],
    )
)

_register(
    AttackEntry(
        name="xss",
        description="Perform XSS vulnerability testing by injecting JavaScript payloads into vulnerable web page inputs",
        category=CATEGORY_APPLICATION,
        module_path="scripts.xss.xss",
        class_name="XSSAttack",
        params=[
            ParamDef("target_url", "str", True, None, "URL of the target web page"),
            ParamDef("parameter", "str", True, None, "Vulnerable query parameter name"),
        ],
    )
)

_register(
    AttackEntry(
        name="xxe",
        description="Perform XML External Entity attack by injecting malicious XML entities to read local files or trigger SSRF",
        category=CATEGORY_APPLICATION,
        module_path="scripts.xxe.xxe",
        class_name="XXEAttack",
        params=[
            ParamDef("target_url", "str", True, None, "URL of the XML-accepting endpoint"),
            ParamDef("payload_file", "str", False, None, "Path to a custom XXE payload file"),
        ],
    )
)

# --- Replay (1) ---

_register(
    AttackEntry(
        name="pcap-replay",
        description="Replay captured network traffic from PCAP files to reproduce previously observed network conditions",
        category=CATEGORY_REPLAY,
        module_path="scripts.pcap_replay.pcap_replay",
        class_name="PCAPReplayAttack",
        params=[
            ParamDef("pcap_file", "str", True, None, "Path to the PCAP file to replay"),
            ParamDef("interface", "str", True, None, "Network interface to replay traffic on"),
            ParamDef(
                "speed", "float", False, 1.0, "Replay speed multiplier (1.0 = original speed)"
            ),
        ],
    )
)
