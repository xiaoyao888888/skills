---
name: module-notes-maintainer
description: Organize repo operational notes and progress documentation for multi-module work. Use when Codex needs to turn verified chat history, commands, logs, diffs, or current repo state into concise notes; decide whether content belongs in AGENTS.md, module_notes/common/, module_notes/<module>/, or a module-owned history directory; decide whether a module needs a maintained handover/current-status note; add or refactor progressive indexes; or remove redundancy while keeping notes evidence-backed and easy to traverse.
---

# Module Notes Maintainer

Keep repository notes layered, concise, and evidence-backed. Record stable repo rules once, route module details through `module_notes/`, and keep handover notes focused on durable current state rather than chat residue.

## Use This Prompt Shape

Use a narrow prompt when invoking this skill. Prefer a request shaped like this:

`Use $module-notes-maintainer to summarize verified work on <module>, place each fact in the right note layer, decide whether handover needs an update, update indexes, and remove redundancy without losing commands, validation signals, or known caveats.`

Add only the missing specifics:
- target module or directory
- source material to summarize
- whether the task is create, refine, deduplicate, or hand over
- whether long-form history already has a separate home

## Follow This Workflow

1. Extract only verified facts.
- Keep commands, paths, logs, and conclusions only if they were actually run, observed, or confirmed from files.
- Drop speculation, temporary debugging ideas, and stale alternatives.

2. Classify each fact by scope and lifespan.
- Put repo-wide stable collaboration rules in `AGENTS.md`.
- Put cross-module board access or shared environment rules in `module_notes/common/`.
- Put module-specific build, deploy, test, and driver notes in `module_notes/<module>/`.
- Put long-form progress, handover history, or narrative status in a module-owned history directory when one exists.

3. Decide whether handover is required.
- Create or update a module handover note when the module has accumulated durable state that another person would otherwise need to reconstruct.
- Typical triggers are: architecture or protocol changes, board-verified results, non-obvious environment constraints, active known limitations, or a clear next-step chain for continued work.
- Do not create or expand handover for trivial edits, one-off Q and A, speculative exploration, or temporary debugging noise with no durable outcome.
- When a handover note already exists, update it in place. Keep it current, remove stale items, and avoid chronological append-only growth.

4. Preserve progressive disclosure.
- Keep `AGENTS.md` as a stable cache-friendly entrypoint.
- Keep `module_notes/README.md` as the module router.
- Keep each module `README.md` as the topic router.
- Keep detailed procedures in numbered topic files such as `01_build.md` and `02_runtime_test.md`.
- Keep module handover as a separate topic such as `04_handover.md` only when the threshold in `references/handover-guidelines.md` is met.

5. Write the smallest useful note.
- Prefer short headings, direct bullets, and runnable commands.
- Keep expected success signals and current caveats close to the commands they qualify.
- Remove duplicate explanations that already exist at a higher layer.
- Record the current known state, not every past branch of investigation.

6. Update indexes whenever structure changes.
- Add a new module entry to `module_notes/README.md` when creating `module_notes/<module>/`.
- Keep module `README.md` limited to scope, prerequisite entrypoints, and topic list.
- Add a module handover entry to the module `README.md` when one is created.
- Link to existing module-owned history docs instead of copying them.

7. Verify the result before finishing.
- Ensure `AGENTS.md` does not contain module runbooks.
- Ensure module notes do not restate repo-wide rules except as brief references.
- Ensure each new topic file has a clear single purpose.
- Ensure naming stays predictable: `README.md` for indexes, `01_xxx.md` for topics.
- Ensure handover, if present, contains only durable current state, not chat transcript residue.

## Apply These Content Rules

- Record commands in the form most likely to be rerun successfully.
- Keep board addresses, device paths, module names, and binary names exact.
- Keep examples short and representative.
- Prefer “how to verify” over broad prose.
- Prefer “known limitation” over unproven fixes.
- Keep history and current runbooks separated when both are needed.
- Keep handover iterative: rewrite for clarity, collapse stale branches, and keep only what materially helps the next owner continue work.

## Read These References When Needed

- Read `references/placement-model.md` when deciding where a note should live.
- Read `references/handover-guidelines.md` when deciding whether handover is warranted and what it should contain.
- Read `references/repo-pattern.md` when following the layout already used in this repository.
