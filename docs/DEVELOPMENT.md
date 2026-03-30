# Development Guide

## Prerequisites

- Python 3.8+
- pip
- Node.js 18+ (for frontend work)
- Root/sudo privileges (for raw socket attacks)

## Setup

### Backend (CLI)

```bash
# Clone the repository
git clone https://github.com/Montimage/mmt-attacker.git
cd mmt-attacker

# Install in development mode with dev dependencies
pip install -e ".[dev]"

# Install pre-commit hooks
pip install pre-commit
pre-commit install

# Verify installation
matcha --help
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

The dev server starts at `http://localhost:3000`.

## Running Tests

```bash
# All unit tests
pytest

# E2E tests only
pytest -m e2e

# Verbose output
pytest -v

# Specific test file
pytest tests/test_cli.py
```

## Linting and Formatting

Ruff is configured in `pyproject.toml`:

```bash
# Check for lint errors
ruff check .

# Auto-fix lint errors
ruff check --fix .

# Check formatting
ruff format --check .

# Auto-format
ruff format .
```

## Project Structure

```
mmt-attacker/
├── matcha/              # CLI package (installed as `matcha` command)
│   ├── cli.py          # Click entry point
│   ├── registry.py     # Attack registry + CLI option definitions
│   ├── output.py       # Output formatting
│   └── commands/       # Non-attack CLI commands
├── src/attacks/         # Attack implementations
│   ├── base.py         # AttackBase abstract class
│   └── *.py            # Individual attack modules
├── frontend/            # React web demo
├── scripts/             # Standalone attack scripts
├── tests/               # Test suite
├── docs/                # Documentation
└── pyproject.toml       # Package configuration
```

## Adding a New Attack

1. Create `src/attacks/your_attack.py`:

```python
from .base import AttackBase
from argparse import ArgumentParser
import logging

logger = logging.getLogger(__name__)

class YourAttack(AttackBase):
    name = "your-attack"
    description = "Description of the attack"

    def add_arguments(self, parser: ArgumentParser) -> None:
        parser.add_argument('--target', required=True, help='Target IP')

    def validate(self, args) -> bool:
        if not self.validator.validate_ip(args.target):
            logger.error(f"Invalid target: {args.target}")
            return False
        return True

    def run(self, args) -> None:
        logger.info(f"Starting {self.name} against {args.target}")
        # Attack implementation
```

2. Register in `src/attacks/__init__.py`
3. Add CLI wiring in `matcha/registry.py`
4. Add tests in `tests/`
5. Document in `docs/PLAYBOOK.md`

## Debugging

```bash
# Run matcha with verbose output
matcha --help

# Run a specific attack with debug logging
python -m matcha <attack-name> [options]
```

## Common Issues

- **Permission denied**: Raw socket attacks require root/sudo
- **Module not found**: Ensure `pip install -e .` was run from the project root
- **Scapy errors**: Some attacks require specific network interfaces to be available
