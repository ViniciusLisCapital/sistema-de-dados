---
name: handover
description: >
  Generates a session handover document — session goal, instructions/guidelines the
  user gave, conventions and decisions established, work completed, open items, and
  which files to read first — so a fresh session can pick up with full context. Use
  when the user asks to "hand over", "wrap up", "write a handover", "summarize this
  session for next time", or before ending a session that has unfinished work someone
  (the same user, a teammate, or a future Claude session) will need to continue.
---

# Handover

Writes `HANDOVER.md` at the repo root, overwriting whatever was there before. This is
a working note for continuing a task, not documentation — it is untracked
(`.gitignore`d) and disposable. Do not confuse this with the auto-memory system: memory
holds durable facts that should survive indefinitely across many future sessions;
`HANDOVER.md` holds this-task-in-progress context that stops being useful once the
task is done, and gets overwritten by the next handover.

## Step 1 — Scope

By default, cover the entire current conversation. If the user passes an argument
(e.g. `/handover fx-attribution`) or the conversation clearly contains multiple
unrelated threads, scope the handover to just the thread they named — say so at the
top of the document rather than silently narrowing.

## Step 2 — Reconstruct, don't invent

Read back over the conversation (and check `git status`/`git diff` for concrete
evidence of what actually changed on disk — a claim of "I edited X" is worth
double-checking against reality before it goes in the handover) and pull out, in this
order:

1. **Goal.** What the user was actually trying to accomplish — the real objective, not
   just the literal last message. If the goal shifted mid-session, note the shift.
2. **Instructions and constraints given.** Anything the user explicitly told Claude to
   do or not do during this session — a rule, a preference, a correction, a scope
   boundary. Quote or closely paraphrase; don't generalize into something vaguer than
   what was actually said.
3. **Conventions and decisions established.** Naming choices, structural choices,
   format choices, anything decided along the way that the next session needs to
   follow rather than re-decide from scratch.
4. **Work completed.** Concrete: files created/edited/deleted, what changed in each,
   commands run that changed state (DB writes, installs, commits). Cite paths.
5. **Current state.** Where things actually stand right now — what works, what's
   half-done, what's untested.
6. **Open items / next steps.** What's left, in priority order if there's an obvious
   one. Include unresolved questions the user hasn't answered yet.
7. **Files to read first.** The short list of paths a new session should open before
   doing anything else to get oriented — not every file touched, just the ones that
   actually orient someone.
8. **Gotchas.** Anything that surprised you, a dead end already tried and ruled out
   (so it isn't retried), or a fragile bit of state (e.g. "DB migration applied but not
   committed").

Skip any section that's genuinely empty for this session — don't pad with "N/A".

## Step 3 — Don't duplicate what already persists elsewhere

- If something belongs in the auto-memory system (a durable fact about the user, a
  standing preference, project context that will matter beyond this task), name it in
  a short closing note ("→ also save to memory: ...") rather than relying on the
  handover file alone — `HANDOVER.md` gets overwritten by the next handover and won't
  carry it forward.
- If something belongs in `CLAUDE.md` (an architecture decision, a new pending item
  for the "Pendências" section), say so the same way rather than only writing it into
  the handover.
- The handover itself should stay focused on the ephemeral, task-specific context that
  neither of those systems is meant to hold.

## Step 4 — Write

Write `HANDOVER.md` at the repo root (create it if missing, overwrite if present).
Lead with a one-line timestamp and scope note using the date from the current session
context (never compute it — this environment can't call `Date.now()`/`new Date()`
reliably for this purpose, so use the date already given in context). Structure the
rest under the headers from Step 2. Keep it dense and concrete — file paths, not
"various files"; the actual constraint the user stated, not a softened summary of it.

## Step 5 — Confirm

Tell the user the handover was written, in one or two sentences, and flag anything
from Step 3 that still needs a manual save to memory or `CLAUDE.md` — don't save those
automatically without the user's sign-off, since they land somewhere durable.
