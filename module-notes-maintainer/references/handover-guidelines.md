# Handover Guidelines

Use this file to decide whether to create or update a module handover note.

## Create or Update Handover When

A module has durable state that is expensive to reconstruct from code and short runbooks alone.

Typical triggers:
- architecture, layering, or protocol changes were made
- board-specific validation produced reusable results
- there are active known limitations or caveats
- the next owner needs a clear continuation path
- multiple rounds of work have converged into a current state worth preserving

A good mental test:
- if a new owner would ask “what is the current state, what already works, what is still risky, and where do I continue?”, the module likely needs handover

## Do Not Create or Expand Handover For

- minor typo or formatting edits
- a single command run with no durable consequence
- speculative analysis with no confirmed outcome
- temporary debugging branches that were discarded
- information already fully captured by a short runbook or by source comments

## Keep Handover Iterative

Treat handover as a maintained current-state note, not an append-only diary.

Update in place:
- collapse stale branches
- replace superseded conclusions
- remove obsolete next steps
- keep only the current validated state and the current unresolved edges

## Prefer This Content Shape

1. Goal or scope
2. Current code entrypoints
3. Verified results worth reusing
4. Active limitations
5. Next-step guidance
6. Important caveats or anti-patterns

## Avoid These Failure Modes

- copying chat summaries verbatim
- logging every conversation turn
- mixing long history into operational runbooks
- treating a one-time board observation as a universal rule without labeling it as a sample or current-board reference
