# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.2.1] - 2026-03-31

### Bug Fixes

- Resolve `ModuleNotFoundError` for `utils` module when running `matcha list` after pip install — moved `logger.py` into the `matcha` package and updated the import in `matcha/cli.py`

**Full Changelog**: https://github.com/montimage/mmt-attacker/compare/v0.2.0...v0.2.1

## [0.2.0] - 2026-03-31

### Features

- Rich terminal output with coloured logs and attack verdict panels ([188515e](https://github.com/montimage/mmt-attacker/commit/188515e)) ([#49](https://github.com/montimage/mmt-attacker/pull/49))
- Modernise website UI with cybersecurity-themed design ([9698e0d](https://github.com/montimage/mmt-attacker/commit/9698e0d))
- Add Docs page and navigation link to frontend ([28566ee](https://github.com/montimage/mmt-attacker/commit/28566ee))
- Rebuild landing page with light-only theme ([6392c78](https://github.com/montimage/mmt-attacker/commit/6392c78))
- Update CLI commands from `python src/cli.py` to `matcha` ([cb00515](https://github.com/montimage/mmt-attacker/commit/cb00515))
- Add target container and docker-compose for two-container demo ([b8596b9](https://github.com/montimage/mmt-attacker/commit/b8596b9)) ([#44](https://github.com/montimage/mmt-attacker/pull/44))
- Add CLI-only Docker container ([6370f66](https://github.com/montimage/mmt-attacker/commit/6370f66)) ([#43](https://github.com/montimage/mmt-attacker/pull/43))

### Bug Fixes

- Resolve playbook test failures found during end-to-end run ([372fe50](https://github.com/montimage/mmt-attacker/commit/372fe50))
- Rewrite simulation engine to match real matcha CLI output ([aaa65aa](https://github.com/montimage/mmt-attacker/commit/aaa65aa))
- Align all website CLI commands with `matcha --help` ([8a7c018](https://github.com/montimage/mmt-attacker/commit/8a7c018))
- Correct invalid Tailwind class and sticky offset after header resize ([85e09ab](https://github.com/montimage/mmt-attacker/commit/85e09ab))
- Rename `generatePythonCommand` to `generateCommand` ([4fc71b7](https://github.com/montimage/mmt-attacker/commit/4fc71b7)) ([#48](https://github.com/montimage/mmt-attacker/pull/48))
- Resolve 15 attack failures found during end-to-end playbook run ([b5762cf](https://github.com/montimage/mmt-attacker/commit/b5762cf)) ([#46](https://github.com/montimage/mmt-attacker/pull/46))

### Documentation

- Rewrite playbook and deployment docs for two-container Docker workflow ([b89bdf8](https://github.com/montimage/mmt-attacker/commit/b89bdf8)) ([#45](https://github.com/montimage/mmt-attacker/pull/45))

### Other Changes

- Update playbook runner results from end-to-end run ([2679243](https://github.com/montimage/mmt-attacker/commit/2679243))
- Add playbook runner results and credential harvester templates ([348f9ba](https://github.com/montimage/mmt-attacker/commit/348f9ba))
- Remove automated PyPI publishing — publish manually with twine ([aef1390](https://github.com/montimage/mmt-attacker/commit/aef1390))

**Full Changelog**: https://github.com/montimage/mmt-attacker/compare/v0.1.0...v0.2.0

## [0.1.0] - 2026-03-30

### Features

- Add PyPI publish workflow and update install to prefer PyPI ([7d25d43](https://github.com/montimage/mmt-attacker/commit/7d25d43))
- Add one-line install script for Linux and macOS ([15f776e](https://github.com/montimage/mmt-attacker/commit/15f776e))
- Add shell completions command for bash/zsh/fish ([ee7c579](https://github.com/montimage/mmt-attacker/commit/ee7c579)) ([#37](https://github.com/montimage/mmt-attacker/pull/37))
- Add `__main__.py` for `python -m matcha` invocation ([5a99195](https://github.com/montimage/mmt-attacker/commit/5a99195)) ([#36](https://github.com/montimage/mmt-attacker/pull/36))
- Add semantic input validation for all attack parameters ([3df13db](https://github.com/montimage/mmt-attacker/commit/3df13db)) ([#34](https://github.com/montimage/mmt-attacker/pull/34))
- Wire pcap-replay command via command factory ([5f71b35](https://github.com/montimage/mmt-attacker/commit/5f71b35)) ([#33](https://github.com/montimage/mmt-attacker/pull/33))
- Wire all 13 application-layer attacks via command factory ([1c39ea1](https://github.com/montimage/mmt-attacker/commit/1c39ea1)) ([#32](https://github.com/montimage/mmt-attacker/pull/32))
- Wire all 12 network-layer attacks via command factory ([d01a091](https://github.com/montimage/mmt-attacker/commit/d01a091)) ([#31](https://github.com/montimage/mmt-attacker/pull/31))
- Add command factory for auto-generating click commands ([f25b062](https://github.com/montimage/mmt-attacker/commit/f25b062)) ([#30](https://github.com/montimage/mmt-attacker/pull/30))
- Add centralized attack registry with script class mappings ([2acf9f1](https://github.com/montimage/mmt-attacker/commit/2acf9f1)) ([#29](https://github.com/montimage/mmt-attacker/pull/29))
- Implement `matcha syn-flood` attack command ([9e29872](https://github.com/montimage/mmt-attacker/commit/9e29872)) ([#26](https://github.com/montimage/mmt-attacker/pull/26))
- Implement `matcha info` command ([d31b530](https://github.com/montimage/mmt-attacker/commit/d31b530)) ([#25](https://github.com/montimage/mmt-attacker/pull/25))
- Implement `matcha list` command ([72ae1ce](https://github.com/montimage/mmt-attacker/commit/72ae1ce)) ([#24](https://github.com/montimage/mmt-attacker/pull/24))
- Add text and JSON output formatter ([30884ad](https://github.com/montimage/mmt-attacker/commit/30884ad)) ([#23](https://github.com/montimage/mmt-attacker/pull/23))
- Add global CLI options: `--verbose`, `--output`, `--no-color` ([c9c856b](https://github.com/montimage/mmt-attacker/commit/c9c856b)) ([#22](https://github.com/montimage/mmt-attacker/pull/22))

### Bug Fixes

- Move dependencies from `project.urls` to `project` section in `pyproject.toml` ([2040422](https://github.com/montimage/mmt-attacker/commit/2040422))
- Address review feedback for CLI skeleton ([156ef18](https://github.com/montimage/mmt-attacker/commit/156ef18))
- Pin click version and add no-args test ([ec1e5d3](https://github.com/montimage/mmt-attacker/commit/ec1e5d3))
- Address review feedback for pyproject.toml ([04237dc](https://github.com/montimage/mmt-attacker/commit/04237dc))

### Documentation

- Reframe README around educational purpose, remove fixed attack counts ([a3dbd9a](https://github.com/montimage/mmt-attacker/commit/a3dbd9a))
- Add OSS community files, GitHub templates, and project documentation ([b1ea9f9](https://github.com/montimage/mmt-attacker/commit/b1ea9f9)) ([#42](https://github.com/montimage/mmt-attacker/pull/42))
- Transform README into landing page format ([35e4155](https://github.com/montimage/mmt-attacker/commit/35e4155)) ([#40](https://github.com/montimage/mmt-attacker/pull/40))
- Update README with matcha CLI usage ([99c9583](https://github.com/montimage/mmt-attacker/commit/99c9583)) ([#39](https://github.com/montimage/mmt-attacker/pull/39))

### Other Changes

- Add pre-commit hooks, GitHub Actions CI, and e2e tests ([c148c16](https://github.com/montimage/mmt-attacker/commit/c148c16)) ([#41](https://github.com/montimage/mmt-attacker/pull/41))
- Add comprehensive test suite for all 26 commands ([c021c80](https://github.com/montimage/mmt-attacker/commit/c021c80)) ([#35](https://github.com/montimage/mmt-attacker/pull/35))
- Add basic CLI smoke tests with CliRunner ([c0f1874](https://github.com/montimage/mmt-attacker/commit/c0f1874)) ([#28](https://github.com/montimage/mmt-attacker/pull/28))
- Add `pyproject.toml` with matcha CLI entry point ([4013918](https://github.com/montimage/mmt-attacker/commit/4013918)) ([#21](https://github.com/montimage/mmt-attacker/pull/21))

**Full Changelog**: https://github.com/montimage/mmt-attacker/commits/v0.1.0
