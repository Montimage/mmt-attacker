# Contributing to MMT-Attacker

Thank you for your interest in contributing to MMT-Attacker! This guide will help you get started.

## How to Contribute

### Reporting Bugs

1. Check [existing issues](https://github.com/Montimage/mmt-attacker/issues) to avoid duplicates
2. Use the [bug report template](.github/ISSUE_TEMPLATE/bug_report.md)
3. Include steps to reproduce, expected vs actual behavior, and your environment

### Suggesting Features

1. Check [existing issues](https://github.com/Montimage/mmt-attacker/issues) for similar requests
2. Use the [feature request template](.github/ISSUE_TEMPLATE/feature_request.md)
3. Describe your use case and why the feature would be valuable

### Submitting Code

1. Fork the repository
2. Create a feature branch from `main` (`feat/description` or `fix/description`)
3. Make your changes
4. Write or update tests as needed
5. Ensure all checks pass
6. Submit a pull request

## Development Setup

### Prerequisites

- Python 3.8+
- Node.js 18+ (for frontend development)

### Backend (CLI)

```bash
git clone https://github.com/Montimage/mmt-attacker.git
cd mmt-attacker
pip install -e ".[dev]"
```

### Frontend (Web Demo)

```bash
cd frontend
npm install
npm run dev
```

### Running Tests

```bash
# Unit tests
pytest

# E2E tests
pytest -m e2e

# Linting
ruff check .
ruff format --check .
```

### Pre-commit Hooks

Pre-commit hooks are configured for code quality. Install them with:

```bash
pip install pre-commit
pre-commit install
```

## Branching Strategy

- `main` — stable, production-ready code
- `feat/NN-description` — new features (NN = issue number)
- `fix/NN-description` — bug fixes
- `docs/NN-description` — documentation changes
- `ci/description` — CI/CD improvements

## Commit Conventions

We follow [Conventional Commits](https://www.conventionalcommits.org/):

```
<type>(<scope>): <description>

[optional body]
```

**Types:** `feat`, `fix`, `docs`, `test`, `ci`, `refactor`, `chore`

**Examples:**
```
feat(cli): add DNS amplification attack command
fix(attacks): correct SYN flood packet construction
docs: update installation instructions
test: add unit tests for ARP spoof module
```

## Pull Request Process

1. Fill out the PR template completely
2. Link to any related issues
3. Ensure CI passes (linting, tests)
4. Request review from a maintainer
5. Address review feedback promptly

### PR Guidelines

- Keep PRs focused — one feature or fix per PR
- Include tests for new functionality
- Update documentation if behavior changes
- Maintain backward compatibility unless discussed

## Coding Standards

### Python

- Follow [PEP 8](https://peps.python.org/pep-0008/) style
- Use [Ruff](https://docs.astral.sh/ruff/) for linting and formatting (configured in `pyproject.toml`)
- Line length: 99 characters
- Type hints are encouraged

### Adding a New Attack

1. Create a module in `src/attacks/` inheriting from `AttackBase`
2. Implement `add_arguments()`, `validate()`, and `run()`
3. Register in `src/attacks/__init__.py`
4. Add CLI wiring in `matcha/registry.py`
5. Add tests in `tests/`
6. Document in `docs/PLAYBOOK.md`

### Frontend (React)

- Use functional components with hooks
- Follow existing Tailwind CSS patterns
- Keep components focused and reusable

## Code of Conduct

This project follows the [Contributor Covenant Code of Conduct](CODE_OF_CONDUCT.md). By participating, you agree to uphold this code.

## Questions?

- Open a [discussion](https://github.com/Montimage/mmt-attacker/issues) on GitHub
- Email [developer@montimage.eu](mailto:developer@montimage.eu)

Thank you for helping make MMT-Attacker better!
