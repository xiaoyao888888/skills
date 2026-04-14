# Repository Pattern

Use the current repository layout as the default pattern.

## Current Layering

1. `AGENTS.md`
- Keep stable repo-wide rules only.
- Point readers to `module_notes/` for module details.

2. `module_notes/README.md`
- Route readers to `common/`, `bluetooth/`, `orb_slam3/`, and future modules.

3. `module_notes/common/`
- Store shared board access rules such as ADB endpoint, cleanup conventions, and basic checks.

4. `module_notes/bluetooth/`
- Split into build/deploy, runtime test, driver notes, and handover.
- Keep low-level protocol conclusions in a driver notes file, not in `AGENTS.md`.
- Keep current state and continuation guidance in `04_handover.md`, not in runbooks.

5. `module_notes/orb_slam3/`
- Split into build/run, IMU checks, and historical handover entrypoints.
- Keep the long history in `external/ORB_SLAM3/docs/handover/` and link to it instead of copying it.

## Compression Pattern

When condensing a session into notes:
- keep commands that were actually used
- keep the shortest explanation that makes the command reusable
- keep success criteria near the command
- keep caveats only when they change operator behavior
- delete repeated context that can be recovered from an index file
- move durable current-state context into handover only when the handover threshold is met

## Good Update Pattern

When adding a new module:
1. Add the module to `module_notes/README.md`.
2. Create `module_notes/<module>/README.md`.
3. Create only the first topic files that are justified by current work.
4. Add a handover file only if the module has durable current state that another owner would need.
5. Link to existing module-owned history docs if they already exist.
6. Leave `AGENTS.md` unchanged unless the new information is genuinely repo-wide and stable.
