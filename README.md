# Practical Codex Skills

This repository is a small, shareable collection of custom Codex skills built from real engineering workflows. Each skill is meant to be dropped into `~/.codex/skills` and used directly, with references and helper scripts included only where they materially improve repeatability.

## Featured Skills

| Skill | What it solves | Notable details |
| --- | --- | --- |
| `git-repo-publish-sanitize` | Initialize a repo, publish it to GitHub, remove leaked secrets from history, and delete/recreate remotes when cleanup must reach GitHub. | Includes a bundled Linux `x86_64` `gh` fallback, in-place sanitization guidance, and concrete notes on sandbox, auth, and scope pitfalls. |
| `module-notes-maintainer` | Turn chat history, logs, diffs, and verified repo state into durable notes without mixing repo rules, runbooks, handover notes, and temporary debugging residue. | Useful when a codebase is growing and operational knowledge keeps getting lost in chat. |
| `rk-gerrit` | Work against Rockchip internal Gerrit for login checks, connectivity tests, change lookup, review signal triage, and blocker analysis. | Keeps the key path local-only and documents the exact review and submit signals to inspect. |

## Install

If you already have Codex and the built-in `skill-installer`, install the Git skill from this repo with:

```bash
python3 ~/.codex/skills/.system/skill-installer/scripts/install-skill-from-github.py \
  --repo xiaoyao888888/skills \
  --path git-repo-publish-sanitize
```

Install all public custom skills from this repository with:

```bash
python3 ~/.codex/skills/.system/skill-installer/scripts/install-skill-from-github.py \
  --repo xiaoyao888888/skills \
  --path git-repo-publish-sanitize module-notes-maintainer rk-gerrit
```

After installation, restart Codex so the new skills are discovered.

## Example Prompts

```text
Use $git-repo-publish-sanitize to initialize this directory, audit secrets, and publish a clean GitHub repository.

Use $module-notes-maintainer to summarize verified progress on this module and move the durable facts into the right notes.

Use $rk-gerrit to inspect this Gerrit change and tell me exactly what is still blocking submission.
```

## Why This Repo Exists

- These skills are based on workflows that are easy to get mostly right and expensive to get slightly wrong.
- Each skill is intentionally narrow: one operational problem, one set of references, one place to start.
- The repository is meant to be understandable by other engineers browsing it for the first time, not just by the original author.

## Contributor Notes

- Read the target skill's `SKILL.md` first; the skills are designed to be self-contained.
- Keep repo-wide engineering and collaboration rules in [AGENTS.md](./AGENTS.md).
- Treat local-only secrets as local-only: document them clearly and keep them out of Git history.
