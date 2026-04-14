---
name: rk-gerrit
description: Work with Rockchip internal Gerrit on 10.10.10.29 for login checks, SSH key permission fixes, connectivity testing, querying a change number or full Change-Id, reading patch set metadata, files, approvals, comments, CI signals, and deciding what action is still required. Use when the user asks how to log into Gerrit, whether the default robot_verifier account works, how to inspect a specific change, or what unresolved review items remain.
---

# RK Gerrit

Use this skill for Rockchip internal Gerrit operations on `10.10.10.29:29418`.

## Self-contained layout

This skill does not depend on `rk-skills`.

Files in this skill:

- Config: `/home/xy/.codex/skills/rk-gerrit/config/gerrit_config.json`
- Local private key path (gitignored, not committed): `/home/xy/.codex/skills/rk-gerrit/config/robot_verifier`
- Query script: `/home/xy/.codex/skills/rk-gerrit/scripts/search_changes.py`
- Client module: `/home/xy/.codex/skills/rk-gerrit/scripts/gerrit_client.py`
- Connectivity test entry: `/home/xy/.codex/skills/rk-gerrit/scripts/gerrit_client.py`

## Defaults

Default config template:

- Server: `10.10.10.29`
- Port: `29418`
- Username: `robot_verifier`
- Key file: `robot_verifier`

## Safety rules

- Never print the private key contents.
- Treat any terminal output that already revealed the private key as a security incident and recommend key rotation.
- Do not copy a leaked real private key into this skill.
- Put the real private key into `config/robot_verifier` manually, then set it to `600`.
- If SSH fails because the key permissions are too open, fix permissions before retrying.
- If sandbox networking blocks SSH, rerun the Gerrit command outside the sandbox.

## Setup and preflight

1. Confirm config:

```bash
cat /home/xy/.codex/skills/rk-gerrit/config/gerrit_config.json
```

2. Ensure key permission is strict:

```bash
chmod 600 /home/xy/.codex/skills/rk-gerrit/config/robot_verifier
ls -l /home/xy/.codex/skills/rk-gerrit/config/robot_verifier
```

3. Test connectivity:

```bash
python3 /home/xy/.codex/skills/rk-gerrit/scripts/gerrit_client.py
```

## Common failure diagnosis (generic)

- `socket: Operation not permitted`
  - Cause: sandbox/network restriction.
  - Action: rerun the same Gerrit command outside sandbox.

- `Permission denied (publickey)`
  - Cause: wrong key, wrong key permissions, or account not authorized.
  - Action: verify key file path, `chmod 600`, and account access.

- timeout/refused/unreachable
  - Cause: intranet unreachable, host/port mismatch, or temporary network issue.
  - Action: verify server `10.10.10.29`, port `29418`, and network route.

- change is `NEW` but no clear blocker
  - Cause: status alone is not enough.
  - Action: inspect `submit-records`, current patch set comments, and approvals.

## Core operations

### 1) Search by keyword/project/branch

```bash
python3 /home/xy/.codex/skills/rk-gerrit/scripts/search_changes.py "bluetooth" -p rk/kernel -b develop-6.1 -n 20
```

JSON mode:

```bash
python3 /home/xy/.codex/skills/rk-gerrit/scripts/search_changes.py "bluetooth" -p rk/kernel -b develop-6.1 -n 20 --json
```

### 2) Query a specific change (metadata)

```bash
python3 /home/xy/.codex/skills/rk-gerrit/scripts/search_changes.py --id Ixxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

### 3) Query change files

```bash
python3 /home/xy/.codex/skills/rk-gerrit/scripts/search_changes.py --id Ixxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx --files
```

### 4) Query review signals (generic review/submit analysis)

```bash
python3 /home/xy/.codex/skills/rk-gerrit/scripts/search_changes.py \
  --id Ixxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx \
  --comments --approvals --submit-records --patch-sets
```

JSON mode for tooling:

```bash
python3 /home/xy/.codex/skills/rk-gerrit/scripts/search_changes.py \
  --id Ixxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx \
  --comments --approvals --submit-records --patch-sets --json
```

### 5) Include timeline or commit message when needed

```bash
python3 /home/xy/.codex/skills/rk-gerrit/scripts/search_changes.py --id Ixxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx --timeline
python3 /home/xy/.codex/skills/rk-gerrit/scripts/search_changes.py --id Ixxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx --commit-message
```

## Interpretation rules

Prioritize signals in this order:

1. `submitRecords`
   - `NOT_READY` + label `NEED` means hard blocker.
2. current patch set (`currentPatchSet`)
   - `kind: NO_CODE_CHANGE` means latest upload did not change code.
3. current patch set line comments
   - these are direct action items for author.
4. current patch set approvals
   - e.g. `Verified+1` means CI passed for that patch set.
5. older patch set warnings/comments
   - only relevant if still unresolved on latest patch set.

Do not infer blocker from `status: NEW` alone.

## Reporting template

When summarizing a change, use this structure:

1. Basic metadata
   - change number, subject, project/branch, owner, status, current patch set, URL
2. Current signals
   - submit-record labels, current patch set approvals, patch set kind
3. Action items
   - unresolved line comments on current patch set
4. Conclusion
   - exact blocker now
   - concrete next action (author/reviewer)

Use direct conclusions such as:

- `network reachable issue: sandbox blocked SSH; rerun outside sandbox`
- `auth issue: key permissions too open; set key to 600`
- `change is NEW, blockers are Code-Review NEED and Verified NEED from submitRecords`
- `latest patch set is NO_CODE_CHANGE; unresolved review comments still need a code patch set`
