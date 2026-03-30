# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2025

### Added

- `matcha` CLI with 26 attack commands (network, application, replay)
- Attack registry with auto-discovery of attack modules
- `AttackBase` abstract class for pluggable attack architecture
- Input validation for IP addresses, ports, and network interfaces
- Structured logging for all attack events
- Shell completions for bash, zsh, and fish
- `matcha list` command to display all available attacks
- `matcha info <attack>` command for attack details
- PCAP replay with speed control and interface selection
- React-based web demo with Mermaid flow diagrams
- Pre-commit hooks with Ruff linting and formatting
- GitHub Actions CI pipeline
- Comprehensive test suite (unit + e2e)
