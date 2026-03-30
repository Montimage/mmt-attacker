# Deployment

## Docker (Recommended)

### Two-container lab (attacker + target)

The fastest way to get started. Both containers share an isolated bridge
network — no host configuration needed.

```bash
git clone https://github.com/Montimage/mmt-attacker.git
cd mmt-attacker
docker compose up --build -d
docker compose ps
```

Run an attack:

```bash
docker compose exec attacker matcha syn-flood --target-ip target --target-port 80 --count 200
```

Tear down:

```bash
docker compose down
```

See [DEMO.md](DEMO.md) for the full two-container guide including all example
attacks and target observation commands.

### CLI-only container (no target)

Pull the pre-built image and run against your own lab target:

```bash
docker pull ghcr.io/montimage/mmt-attacker:latest

docker run --rm \
  --cap-add NET_ADMIN \
  --cap-add NET_RAW \
  ghcr.io/montimage/mmt-attacker:latest \
  --help
```

Run an attack:

```bash
docker run --rm \
  --cap-add NET_ADMIN \
  --cap-add NET_RAW \
  --network host \
  ghcr.io/montimage/mmt-attacker:latest \
  http-dos --target-url http://<target-ip> --threads 5
```

See [DOCKER.md](DOCKER.md) for the full CLI-only Docker guide (PCAP replay
with volume mounts, shell completions, JSON output, etc.).

---

## CLI Tool

### Install from PyPI

```bash
pip install mmt-attacker
```

### Install from source

```bash
git clone https://github.com/Montimage/mmt-attacker.git
cd mmt-attacker
pip install .
```

### Install in development mode

```bash
pip install -e .
```

### Verify installation

```bash
matcha --help
matcha list
```

---

## Web Demo (Frontend)

### Local development

```bash
cd frontend
npm install
npm run dev
```

Opens at `http://localhost:3000`.

### Production build

```bash
cd frontend
npm run build
```

Build output goes to `frontend/dist/`.

### Netlify deployment

The frontend is configured for Netlify via `frontend/netlify.toml`:

```bash
cd frontend
npm run build
# Upload dist/ to Netlify
```

Netlify configuration handles SPA routing automatically.

---

## Environment Requirements

### CLI

- Python 3.8+
- Root/sudo privileges for raw socket operations
- Network interface access for packet-level attacks

### Docker

- Docker Engine 20.10+
- Docker Compose v2

### Frontend

- Node.js 18+
- npm
