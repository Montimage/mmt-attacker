# Architecture

## Overview

MMT-Attacker is a modular network attack simulation toolkit with two main components: a Python CLI (`matcha`) and a React web demo frontend.

## System Architecture

```
┌─────────────────────────────────────────────────────┐
│                    User Interface                    │
├──────────────────────┬──────────────────────────────┤
│    CLI (matcha)      │     Web Demo (React)          │
│    Python + Click    │     Vite + Tailwind           │
├──────────────────────┴──────────────────────────────┤
│                  Attack Registry                     │
│            matcha/registry.py                        │
├─────────────────────────────────────────────────────┤
│                Attack Modules (26)                   │
│              src/attacks/*.py                        │
│         Each extends AttackBase                      │
├─────────────────────────────────────────────────────┤
│              Core Libraries                          │
│   Scapy · Paramiko · Requests · Cryptography         │
└─────────────────────────────────────────────────────┘
```

## Components

### CLI Layer (`matcha/`)

- **`cli.py`** — Click-based entry point, registers all commands from the registry
- **`registry.py`** — Maps attack names to their implementations, defines CLI options per attack
- **`output.py`** — Standardized output formatting (tables, colors, status messages)
- **`commands/`** — Non-attack CLI commands (list, info, completions, factory)

### Attack Layer (`src/attacks/`)

- **`base.py`** — `AttackBase` abstract class defining the interface: `add_arguments()`, `validate()`, `run()`
- **26 attack modules** — Each inherits from `AttackBase` and implements a specific attack type
- Attacks are organized by layer: network (12), application (13), replay (1)

### Frontend (`frontend/`)

- React 19 + Vite 7 single-page application
- Tailwind CSS for styling
- Mermaid diagrams for attack flow visualization
- Educational interface — demonstrates attack concepts without executing real attacks

### Scripts (`scripts/`)

- Standalone attack scripts (pre-CLI implementations)
- Organized by attack type in subdirectories

## Data Flow

1. User invokes `matcha <attack-name> [options]`
2. CLI looks up the attack in the registry
3. Registry maps to the corresponding `AttackBase` subclass
4. Attack validates inputs (IP, port, interface checks)
5. Attack executes with structured logging
6. Results are formatted via the output module

## Key Design Decisions

- **Plugin architecture**: New attacks require only a class + one-line registration
- **Validation first**: All inputs are validated before attack execution begins
- **Structured logging**: Every attack logs events for post-analysis
- **Separation of concerns**: CLI wiring is separate from attack logic
