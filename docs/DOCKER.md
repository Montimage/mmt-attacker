# Running matcha via Docker

The `matcha` CLI is available as a Docker image that includes **only the CLI module** — no Node.js, no web frontend. It is the fastest way to run matcha in a sandboxed environment without touching your host Python installation.

## Prerequisites

- [Docker](https://docs.docker.com/get-docker/) installed and running
- Root / sudo access on the host (required to pass network capabilities to the container)

---

## Option A — Pull from GitHub Container Registry (recommended)

```bash
docker pull ghcr.io/montimage/mmt-attacker:latest
```

Tag the image locally for convenience:

```bash
docker tag ghcr.io/montimage/mmt-attacker:latest matcha
```

## Option B — Build from source

```bash
git clone https://github.com/Montimage/mmt-attacker.git
cd mmt-attacker
docker build -t matcha .
```

---

## Starting the container

### Verify the image works

```bash
docker run --rm matcha --help
```

```
Usage: matcha [OPTIONS] COMMAND [ARGS]...

  MMT Attack Toolkit — 26 network attacks for authorized security testing.
  ...
```

### List all available attacks

```bash
docker run --rm matcha list
```

### Get details on a specific attack

```bash
docker run --rm matcha info syn-flood
```

---

## Running attacks

Most attacks use raw sockets and require two Linux capabilities:

| Capability | Purpose |
|---|---|
| `NET_ADMIN` | Modify network interfaces, ARP tables, routes |
| `NET_RAW`   | Send/receive raw packets (required by scapy) |

Use `--network host` so the container shares the host's network stack (necessary for attacks that target local-network hosts).

### General template

```bash
docker run --rm \
  --cap-add NET_ADMIN \
  --cap-add NET_RAW \
  --network host \
  matcha <attack-name> [OPTIONS]
```

### Example — SYN Flood

```bash
docker run --rm \
  --cap-add NET_ADMIN \
  --cap-add NET_RAW \
  --network host \
  matcha syn-flood \
    --target-ip 192.168.1.100 \
    --target-port 80 \
    --count 500
```

### Example — ARP Spoofing

```bash
docker run --rm \
  --cap-add NET_ADMIN \
  --cap-add NET_RAW \
  --network host \
  matcha arp-spoof \
    --target-ip 192.168.1.100 \
    --gateway-ip 192.168.1.1
```

### Example — HTTP DoS

```bash
docker run --rm \
  --cap-add NET_ADMIN \
  --cap-add NET_RAW \
  --network host \
  matcha http-dos \
    --target-url http://192.168.1.100 \
    --threads 10
```

### Example — PCAP Replay (with a local capture file)

Mount the directory containing the `.pcap` file into the container:

```bash
docker run --rm \
  --cap-add NET_ADMIN \
  --cap-add NET_RAW \
  --network host \
  -v /path/to/pcaps:/pcaps \
  matcha pcap-replay \
    --pcap-file /pcaps/capture.pcap \
    --interface eth0 \
    --speed 1.0
```

---

## Interactive shell

To explore the container or debug an issue, override the entrypoint:

```bash
docker run --rm -it \
  --cap-add NET_ADMIN \
  --cap-add NET_RAW \
  --network host \
  --entrypoint bash \
  matcha
```

Inside the shell:

```bash
matcha list
matcha --version
```

---

## JSON output

All attacks support `--output json` for machine-readable results:

```bash
docker run --rm \
  --cap-add NET_ADMIN \
  --cap-add NET_RAW \
  --network host \
  matcha --output json list
```

---

## Security notes

- The container runs as a **non-root user** (`matcha`) by default.
- `NET_ADMIN` and `NET_RAW` capabilities are **not** granted automatically — you must pass `--cap-add` explicitly.
- Use only in **controlled, isolated lab environments** with explicit authorization. See [PLAYBOOK.md](PLAYBOOK.md) for ethical guidelines.
- Avoid using `--privileged`; the two capabilities above are sufficient for all attacks.

---

## Troubleshooting

| Symptom | Fix |
|---|---|
| `Operation not permitted` | Add `--cap-add NET_ADMIN --cap-add NET_RAW` |
| `Network unreachable` | Add `--network host` |
| `pcap file not found` | Mount the directory with `-v /local/path:/container/path` |
| `matcha: command not found` inside container | Run `docker run --rm matcha --help` to verify image is built correctly |
