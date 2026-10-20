---
name: mental
description: Grow a manager's mental-model document for one area from the letters it has not read yet. Runs the mental-model agent (reads the letters, repacks the entries they add to, writes the claims), then the independent mental-model-reviewer (judges every claim against the old text, the new text and the letters), then records the run with mental.py done. Run as /mental <manager> <area> [letter ...] [--n N]; with no arguments, lists every document and what is pending.
argument-hint: "<manager> <area> [letter ...] [--n N]"
disable-model-invocation: true
---

Build mental models. Arguments: $ARGUMENTS

You conduct the run; you do not write the document. Two agents do the work, one after the other,
and the run is recorded only when the second one's verdicts let it through. The writer and the
reviewer are separate agents on purpose: a writer grading its own rewrite is the weakness this
design exists to remove. Commands: `uv run python repository/ingestion/scripts/mental.py`.

1. **No manager and area** → run `mental.py --list`, show it, stop.

2. **Writer.** Launch the `mental-model` agent in the foreground (`run_in_background: false`) with
   the prompt `$ARGUMENTS`. It runs `begin`, reads the document and the letters, repacks, writes the
   claims and gets `check` to pass. It does not run `done`. If it stops without a passing check (a
   corpus with no text, a run it had to abort), report that to the user and stop.

3. **Reviewer.** Launch a **new** `mental-model-reviewer` agent in the foreground with the prompt
   `<manager> <area>`. Never pass it the writer's report or your own reading: it must judge the texts
   cold. It writes the verdicts file.

4. **Record.** `mental.py done <manager> <area>`.
   - It passes → the letters enter the ledger and the review table is appended to
     `repository/mental_model/ledger/<document>.log.md`. Go to 6.
   - It is blocked → step 5.

5. **Findings.** Send the blocking lines, verbatim, to the **same** writer agent (SendMessage to the
   agent from step 2) and wait for it. Then launch a **new** reviewer (step 3) and run `done` again.
   At most two rounds. If it is still blocked, stop and give the user the open findings, each with
   the old text and the new text it concerns, and the two ways out:
   - the user accepts a verdict → `mental.py done <manager> <area> --accept <block>:<id> ...`
     (only with the user's explicit word; the acceptance is written to the log);
   - the user gives up on the run → `mental.py abort <manager> <area>` and `git checkout` of the
     document restores it.
   Never edit the document, the claims or the review yourself to get past a finding.

6. **Report to the user**: the writer's table (letters, entries repacked and created, reversals),
   the reviewer's summary line, anything accepted, and where the review log is. Keep it short; the
   git diff of the document and the log are where the user reads the detail.
