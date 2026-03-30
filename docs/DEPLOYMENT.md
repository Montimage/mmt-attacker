# Deployment

## CLI Tool

### Install from Source

```bash
git clone https://github.com/Montimage/mmt-attacker.git
cd mmt-attacker
pip install .
```

### Install in Development Mode

```bash
pip install -e .
```

### Verify Installation

```bash
matcha --help
matcha list
```

## Web Demo (Frontend)

### Local Development

```bash
cd frontend
npm install
npm run dev
```

### Production Build

```bash
cd frontend
npm run build
```

Build output goes to `frontend/dist/`.

### Netlify Deployment

The frontend is configured for Netlify deployment via `frontend/netlify.toml`:

```bash
# Deploy preview
cd frontend
npm run build
# Upload dist/ to Netlify
```

Netlify configuration handles SPA routing automatically.

## Environment Requirements

### CLI

- Python 3.8+
- Root/sudo privileges for raw socket operations
- Network interface access for packet-level attacks

### Frontend

- Node.js 18+
- npm

## Docker (Planned)

Docker containerization is on the roadmap. See [GitHub Issues](https://github.com/Montimage/mmt-attacker/issues) for progress.
