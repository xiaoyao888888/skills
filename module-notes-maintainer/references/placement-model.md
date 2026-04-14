# Placement Model

Use this file to decide where new information belongs.

## AGENTS.md

Put only repo-wide, stable rules here.

Keep:
- collaboration rules
- stable board access constraints shared across modules
- repo-wide editing or testing constraints
- the pointer to `module_notes/`

Do not keep:
- module build commands
- module runtime validation steps
- long troubleshooting sequences
- per-module status or history

## module_notes/README.md

Use this file as the only top-level module router.

Keep:
- one-line purpose of the note system
- reading order
- module entry list
- naming conventions

Do not keep:
- detailed procedures
- repo-wide rules already in `AGENTS.md`

## module_notes/common/

Use this directory for cross-module board access and shared runtime constraints.

Keep:
- ADB endpoints
- shared cleanup commands
- environment checks reused across modules

Do not keep:
- module-specific build or deploy flows
- module-specific current status or handover content

## module_notes/<module>/README.md

Use this file as a module router.

Keep:
- scope
- prerequisite entrypoints
- topic list

Do not keep:
- detailed commands that belong in topic files
- repeated repository philosophy
- handover details beyond a pointer to the handover file

## module_notes/<module>/0x_*.md

Use numbered topic files for concrete runbooks.

Keep:
- build commands
- deployment steps
- runtime validation
- expected good signals
- known caveats backed by evidence

Do not keep:
- long historical narratives if a history directory exists
- duplicate commands that already live in another topic file

## module_notes/<module>/0x_handover.md

Use a module handover file only when the module has durable current state that materially helps the next owner continue.

Keep:
- current goal or scope
- key code entrypoints
- verified validation results worth reusing
- active known limitations
- concrete next-step guidance
- important “do not rely on” caveats

Do not keep:
- raw chat chronology
- every past branch that was explored
- one-off trivial edits
- speculative ideas without evidence

## Module-Owned History Directories

Use a module-owned history directory for long-form progress, handover history, and chronology.

Keep:
- milestone summaries
- investigation history
- references for deeper background

Do not copy this material into operational runbooks. Link to it from the module README or from the top-level module index instead.
