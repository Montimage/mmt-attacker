---
name: playbook-runner
description: End-to-end playbook execution skill for mmt-attacker. Checks and installs dependencies, spins up the two-container Docker lab, runs every attack scenario from PLAYBOOK.md one by one, auto-fixes errors (rebuild + re-test), summarizes results, and opens a PR if any code was modified. Trigger when the user says "run the playbook", "test all attacks", "execute playbook scenarios", "run end-to-end tests", "validate docker lab", or wants a full integration test of the mmt-attacker toolkit.
metadata:
  version: 2.0.0
---

# Playbook Runner

Runs the full mmt-attacker playbook end-to-end inside the two-container Docker lab. The main agent acts as a clean orchestrator: it coordinates three specialized subagents (builder, attacker, fixer) and never does the heavy lifting directly. Each phase produces a structured status report.

## Architecture

```
Main Agent (orchestrator)
├── Builder subagent  — Docker lab lifecycle (startup, rebuild, teardown)
├── Attacker subagent — Executes one scenario, returns pass/fail
└── Fixer subagent    — Diagnoses failures, patches source code
```

The main agent reads no source files, runs no Docker commands, and makes no code changes. It spawns subagents, collects their JSON results, and coordinates the next step.

Subagent prompt files live in `agents/`:
- `agents/builder.md` — full builder prompt
- `agents/attacker.md` — full attacker prompt
- `agents/fixer.md` — full fixer prompt

## Environment Check

If the Agent tool is available, use subagents as described throughout this skill.

If the Agent tool is NOT available (e.g., Claude.ai), execute each phase inline in the main conversation instead — read files directly, run Docker commands yourself, make fixes in-line. The workflow logic is identical; only the isolation changes.

---

## Repo Sync Before Edits (mandatory)

Before making any changes to files:

```bash
branch="$(git rev-parse --abbrev-ref HEAD)"
git fetch origin
git pull --rebase origin "$branch"
```

If the working tree is dirty: stash, sync, then pop (`git stash && git pull --rebase origin "$branch" && git stash pop`).

If `origin` is missing or rebase conflicts appear, stop and ask the user before continuing.

---

## Phase 0 — Dependency Check

Before touching Docker, verify the local environment. Run these directly in the main agent (they are quick):

```bash
docker --version
docker compose version
git --version
gh --version
```

| Missing | Hint |
|---------|------|
| `docker` | "Install Docker Desktop from https://docs.docker.com/get-docker/" |
| `docker compose` | "Upgrade Docker Desktop or install the compose plugin" |
| `gh` | "Install with `brew install gh` or from https://cli.github.com/" |

Stop if `docker` or `docker compose` are missing. Warn but continue if `gh` is missing (PR creation will fall back to printing the diff).

---

## Phase 1 — Lab Startup (Builder subagent)

Spawn the builder subagent to bring up the lab. Read `agents/builder.md` for the full prompt.

Pass to the builder:
```json
{ "repo_root": "<absolute path to repo>", "action": "startup" }
```

The builder returns `builder_result.json`. Extract and keep:
- `target_ip`
- `gateway_ip`
- `broadcast_ip`
- `target_reachable`

If `success: false`, print the builder's `error` field and abort — the lab is broken.

### Step Completion Report

```
◆ Lab Startup (phase 1 of 5)
··································································
  docker compose up:       √ pass | × fail
  attacker running:        √ pass | × fail
  target running:          √ pass | × fail
  target reachable:        √ pass | × fail
  TARGET_IP resolved:      √ pass — <value> | × fail
  ____________________________
  Result:             PASS | FAIL
```

---

## Phase 2 — Playbook Parsing

Parse `docs/PLAYBOOK.md` directly in the main agent. This is lightweight (one file read) and produces the scenario list that drives all subsequent phases.

**Extraction algorithm:**

1. Split on H3 headings (`### `). Each heading is a scenario name.
2. Within each section, find fenced bash blocks (` ```bash ... ``` `).
3. Extract every line matching `docker compose exec attacker matcha` — these are runnable commands.
4. If a section has setup commands before the main attack (e.g., creating a wordlist), record them as `pre_commands`.
5. For each scenario record:
   - `name`: from the H3 heading (lowercased, spaces → hyphens)
   - `section`: top-level H2 section it falls under
   - `command`: the extracted `docker compose exec attacker matcha ...` line
   - `pre_commands`: list of setup commands (may be empty)
   - `is_simulation`: true if the section text mentions "simulation", "no real", "educational simulation", or the note says the target service isn't present
   - `timeout_s`: 60 for brute-force attacks (SSH, FTP, RDP), 30 for everything else

Print the parsed list before executing:

```
Parsed 26 scenarios from docs/PLAYBOOK.md:
  1.  syn-flood            [network]      30s
  2.  icmp-flood           [network]      30s
  ...
  26. pcap-replay          [replay]       30s  (skipped if no .pcap available)
```

---

## Phase 3 — Scenario Execution Loop

For each scenario in parsed order, run the **attacker → fixer → builder (rebuild) → attacker (retest)** cycle as needed.

### 3a: Run the attacker subagent

Read `agents/attacker.md` for the full prompt. Pass:

```json
{
  "repo_root": "<repo_root>",
  "scenario": { <scenario object from Phase 2> },
  "target_ip": "<from builder>",
  "gateway_ip": "<from builder>",
  "broadcast_ip": "<from builder>"
}
```

Announce before spawning: `▶ Running scenario N/M: <name>`

The attacker returns a result with `status: PASS | FAIL | SKIP`.

### 3b: On PASS or SKIP — record and continue

Append to the running results log and move to the next scenario.

### 3c: On FAIL — enter the fix cycle (up to 3 attempts)

**Attempt loop:**

1. Spawn the **fixer subagent** (read `agents/fixer.md`). Pass the scenario name, attempt number, and the full failure result from the attacker.

2. If fixer returns `files_changed: []`: mark the scenario `BLOCKED` and move on.

3. If fixer returns `requires_target_restart: true`: spawn the builder subagent with `action: "rebuild"` (which will also restart the target). Wait for builder success.

4. If fixer returns `requires_rebuild: true` (the common case): spawn the **builder subagent** with `action: "rebuild"`. Wait for builder success before retesting.

5. Spawn the **attacker subagent** again for the same scenario.

6. If PASS: record as `FIXED (N attempts)` and continue.

7. If still FAIL and attempts < 3: loop back to step 1 with attempt incremented.

8. After 3 failed attempts: mark `BLOCKED`, record all attempted fixes.

### Fix cycle report (after each attempt)

```
◆ Fix Cycle — <scenario.name> (attempt N of 3)
··································································
  diagnosis:          <one-line from fixer>
  files changed:      <file:lines — description>
  rebuild:            √ pass | × fail
  re-test result:     √ PASS | × FAIL
  ____________________________
  Result:             FIXED | STILL FAILING | BLOCKED
```

### Per-scenario status (after final outcome)

```
◆ <scenario.name> (scenario N of M)
··································································
  exit code:          √ 0 | × <N>
  no traceback:       √ pass | × fail
  structured output:  √ pass | × fail
  elapsed:            <N>s
  ____________________________
  Result:             PASS | FAIL | SKIP | BLOCKED
```

---

## Phase 4 — Summary

After all scenarios, produce the summary. The main agent aggregates the results it collected from attacker/fixer responses — no additional subagents needed.

```
╔══════════════════════════════════════════════════════════════════╗
║              PLAYBOOK EXECUTION SUMMARY                          ║
╠══════════════════════════════════════════════════════════════════╣
║  Total scenarios:    26                                          ║
║  PASS:               22   ✓                                      ║
║  FAIL (fixed):        2   ↺                                      ║
║  BLOCKED:             1   ✗                                      ║
║  SKIP (simulation):   1   ○                                      ║
╚══════════════════════════════════════════════════════════════════╝

Scenario Results:
  ✓ syn-flood           0.8s
  ✓ icmp-flood          0.6s
  ...
  ↺ http-dos            fixed (2 attempts) — was missing --timeout default
  ✗ vlan-hopping        BLOCKED — bridge network does not support 802.1Q
  ○ bgp-hijacking       SKIP (simulation)
```

Also list every source file modified during fix cycles, with a one-line description.

---

## Phase 5 — PR Creation

If **any source files were modified** during fix cycles:

1. Check the diff (run directly in main agent):
   ```bash
   git diff --stat
   git status --short
   ```

2. Stage and commit:
   ```bash
   git add <specific modified files — never git add -A>
   git commit -m "$(cat <<'EOF'
   fix: resolve playbook test failures found during end-to-end run

   Auto-fixed by playbook-runner skill. See summary for details.
   EOF
   )"
   ```

3. Push and open PR:
   ```bash
   git push origin HEAD
   gh pr create \
     --title "fix: resolve playbook test failures" \
     --body "$(cat <<'EOF'
   ## Summary
   - Auto-fixed failures found during end-to-end playbook execution
   - All scenarios re-tested after fixes

   ## Test Results
   <paste summary table here>

   ## Changes
   <list of modified files with descriptions>

   ## Test plan
   - [ ] `docker compose up --build -d` succeeds
   - [ ] All fixed scenarios pass when re-run manually
   - [ ] No regressions in previously passing scenarios
   EOF
   )"
   ```

4. Return the PR URL to the user.

If `gh` is not available, print the full diff and manual instructions.

If **no files were modified**, skip PR creation: "All tests passed with no code changes required."

---

## Lab Teardown

After Phase 5, tear down the lab (unless the user asked to keep it running). Spawn the builder subagent with `action: "teardown"`.

---

## Important Notes

- **Never use `git add -A` or `git add .`** — always stage specific files.
- **Never skip git hooks** (`--no-verify`) — fix the underlying issue if a hook fails.
- **Never amend published commits** — create new commits.
- **Keep fixes minimal** — the fixer agent is instructed to be surgical; don't second-guess it by adding extra changes.
- **Respect lab isolation** — all attacks go through `docker compose exec attacker`. Never run attacks against external IPs.
- **Workspace directory**: subagents write intermediate JSON to `<repo_root>/.playbook-runner/`. You can read these files if you need to inspect a result more carefully, but normally just use the return value from the Agent tool call.
