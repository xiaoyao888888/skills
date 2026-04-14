# Codex Skills

This repository collects reusable Codex skills and related references, scripts, and assets. It currently contains two custom skills plus several bundled system skills under `.system/`.

See [AGENTS.md](./AGENTS.md) for the repository-wide engineering and collaboration rules that should apply before editing or extending any skill here.

## Layout

- `.system/`: bundled system skills for image generation, OpenAI docs lookups, plugin creation, skill creation, and skill installation.
- `module-notes-maintainer/`: guidance for organizing durable repo and module notes without mixing stable rules, runbooks, and handover state.
- `rk-gerrit/`: a self-contained skill for querying and diagnosing Rockchip internal Gerrit changes.

## Included Skills

- `module-notes-maintainer`
  - Purpose: keep repo notes layered, concise, evidence-backed, and placed in the right note layer.
  - Key references: `references/placement-model.md`, `references/handover-guidelines.md`, `references/repo-pattern.md`.

- `rk-gerrit`
  - Purpose: inspect Rockchip Gerrit state on `10.10.10.29:29418`, including connectivity, approvals, comments, and submit readiness.
  - Key files: `config/gerrit_config.json`, `scripts/gerrit_client.py`, `scripts/search_changes.py`.
  - Local-only secret: place the real private key at `config/robot_verifier`; that path is gitignored and must not be committed.

- `.system/imagegen`
  - Purpose: create or transform bitmap assets such as mockups, textures, illustrations, and transparent-background cutouts.

- `.system/openai-docs`
  - Purpose: answer OpenAI product and API questions using official documentation and bundled references.

- `.system/plugin-creator`
  - Purpose: scaffold Codex plugins, including `.codex-plugin/plugin.json` and optional support files.

- `.system/skill-creator`
  - Purpose: create or update skills with the right structure, metadata, and helper scripts.

- `.system/skill-installer`
  - Purpose: install curated skills into `$CODEX_HOME/skills` from curated sources or GitHub repositories.

## Using This Repo

- Read the target skill's `SKILL.md` first; each skill is designed to be self-contained.
- Use the local `references/`, `scripts/`, and `assets/` folders instead of re-deriving instructions when they already exist.
- Keep repo-wide rules in [AGENTS.md](./AGENTS.md); keep skill-specific behavior inside each skill directory.

## Notes

- `rk-gerrit` is intended for intranet access and may require rerunning commands outside the sandbox when networking is restricted.
- `AGENTS.md` also records the proxy fallback currently used for network-related problems.
