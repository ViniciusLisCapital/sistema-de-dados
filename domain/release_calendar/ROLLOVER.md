# Release calendar — year rollover runbook

How to carry `calendar_2026.yaml` (or whatever the current file is) into the next year. Written for
whoever — human or agent — picks this up next, because the reasoning behind the default path is not
obvious from the code and one plausible-looking shortcut quietly damages the file.

**Read this first, in one line:** the sources do *not* publish a full year at a time, so this is a
recurring chore spread over months, not a single end-of-year action. Default to extending the window
on the existing file; only build a per-year file if you specifically want the archive.

---

## 0. Measure the horizon before planning anything

The single most important step, and the one that was previously gotten wrong: **do not assume how far
the feeds reach.** An earlier version of these docs claimed BCB's ICS feeds ran "~18 months forward".
Measured on 2026-08-17 that was false — most stopped at 31/12 of the running year.

```powershell
uv run python -m domain.release_calendar.update_calendar --horizonte
```

That flag exists *because* of that error — it prints each feed's first/last event, the months of reach,
and a summary line counting how many feeds stop at the end of the current year. Run it, don't assume.

Baseline output from 2026-08-17, for comparison — if a future run looks wildly different, trust the run:

```
  bcb_ibcbr                     85 ev   2020-01-16 -> 2027-02-18   (+6m)
  bcb_icbr                      26 ev   2025-01-08 -> 2027-02-03   (+6m)
  bcb_focus                    363 ev   2020-01-06 -> 2026-12-28   (+4m)
  bcb_copom                    128 ev   2020-02-04 -> 2027-12-08   (+16m)
  bcb_copom_ata                 56 ev   2020-02-11 -> 2026-12-15   (+4m)
  bcb_rpm                       28 ev   2020-03-26 -> 2026-12-17   (+4m)
  bcb_ptc                       18 ev   2024-11-21 -> 2026-12-03   (+4m)
  bcb_credit_note               81 ev   2020-01-29 -> 2026-12-28   (+4m)
  bcb_external_sector_note      81 ev   2020-01-27 -> 2026-12-18   (+4m)
  bcb_fiscal_statistics         83 ev   2020-01-31 -> 2026-12-30   (+4m)

7/10 feeds param em 2026 ou antes: bcb_focus, bcb_copom_ata, bcb_rpm, bcb_ptc, ...
maior horizonte: 2027-12-08
```

`bcb_copom` is the outlier at +16m because Copom's meeting calendar is published years ahead by norm.
The other nine are short, and seven of them stop dead at 31/12 of the running year.

IBGE's API behaves the same way — as of 2026-08-17 it had 1–2 releases per product for 2027 and
nothing at all for IPCA-15. Conclusion: BCB and IBGE both publish next year's agenda late in the
preceding year, so expect to repeat step 2 every month or two through H1 before the next year is fully
populated. Groups still short of a full year keep `confirmed: false` estimates in the meantime.

---

## 1. Pick a path

**Default — extend the window on the existing file.** No new file, no code change, nothing to
repoint. `--until` is already a CLI flag; the `_em_escopo` guard in `update_calendar.py` was written
specifically so out-of-window entries survive a `--write`, which is what makes a multi-year file safe.

**Only if you want a genuine per-year archive** (or need the report scoped to a single year) go to
step 5. It costs a hand-edit, two code edits, and some cosmetic damage to the YAML — see the trap
in step 5.

---

## 2. Extend and apply (the default path)

```powershell
uv run python -m domain.release_calendar.update_calendar --until 2027-12-31           # ve o drift
uv run python -m domain.release_calendar.update_calendar --until 2027-12-31 --write   # aplica
uv run python -c "from analytics.release_calendar.generate_report import run; run()"
```

Dry-run first, always — the YAML is hand-curated and the script only swaps dates. What the
2026-08-17 dry-run produced, as a sanity reference: 12 new 2027 releases across exactly 3 groups
(`bcb_ibcbr` 2, `bcb_icbr` 2, `bcb_copom` 8), every other group `sem mudanca`.

Expect and do not be alarmed by 8 warnings of the form:

```
! 2027-01-27: entrada nova sem reference_period derivavel — preencher a mao
```

That's Copom working as designed — the meeting number (`281ª reunião`) isn't in the ICS feed and has
no `ref:` rule, so it must be typed in by hand after the write. Everything else derives its
`reference_period` from the group's `ref:` block.

---

## 3. Fill in what the feeds can't give

- **Copom meeting numbers** — hand-fill each new entry's `reference_period`. Continue the sequence
  from the last existing entry; BCB's `/api/servico/sitebcb/copom/atas` could in principle supply
  these but is not wired up (see the parent CLAUDE.md's Pending).
- **Recheck `reference_period` sanity across the year boundary.** `_ref_period` handles the wrap
  (January with `lag: 1` → previous December, Q1 with `lag: 1` → previous Q4) — asserted at the year
  boundary when it was written, but in-session only, with no checked-in test (see Reference below). A
  January release covering the prior year is exactly the case worth eyeballing once in the diff.

---

## 4. Re-research the 15 manual groups

These have no ICS feed and stay manual. `update_calendar.py` names them at the end of every run so
they don't silently look covered. Ordered by how easy they are:

| groups | source | notes |
|---|---|---|
| the 8 `ibge_*` | `servicodados.ibge.gov.br/api/v3/calendario/?de=&ate=&qtd=` | **A real JSON API — automate this first.** Product IDs and gotchas are in the parent CLAUDE.md's "Non-BCB sources". Returns the reference period explicitly, so no lag rule to infer. |
| `cftc_cot` | [CFTC release schedule](https://www.cftc.gov/MarketReports/CommitmentsofTraders/ReleaseSchedule/index.htm) | Static HTML table, ~19 weekly dates. Publishes a full year at a time. |
| `fomc` | [Fed FOMC calendars](https://www.federalreserve.gov/monetarypolicy/fomccalendars.htm) | Static HTML, published years ahead. |
| `mdic_comex_stat` | [MDIC cronograma](https://balanca.economia.gov.br/balanca/cronograma/pg_cronograma.html) | Static HTML. |
| `mte_caged_novo`, `bcb_caged_sgs_mirror` | [PDET calendar](https://www.gov.br/trabalho-e-emprego/pt-br/acesso-a-informacao/acoes-e-programas/programas-projetos-acoes-obras-e-atividades/estatisticas-trabalho/o-pdet/calendario-de-divulgacao-do-novo-caged) | The two share one source. `bcb_caged_sgs_mirror` is the **only** `confirmed: false` group in the file — its dates are pattern estimates, not published. |
| `tesouro_rtn`, `tesouro_efgg` | per-semester PDF | **The `source_url` will 404.** It embeds the semester (`.../2026_2sem.pdf`), so a new one must be located each half-year. Both groups share the same PDF. |

All six non-BCB source pages were probed on 2026-08-17: every one HTTP 200, none an SPA, so all are
scrapeable — unlike BCB's own calendar page. Update each group's `source_url` when it changes.

---

## 5. Per-year file instead (optional)

```powershell
Copy-Item domain/release_calendar/calendar_2026.yaml domain/release_calendar/calendar_2027.yaml
# hand-edit calendar_2027.yaml: reset every group's `entries:` to [], update the header comment year
uv run python -m domain.release_calendar.update_calendar --yaml domain/release_calendar/calendar_2027.yaml --from 2027-01-01 --write
```

Then two code edits, both hardcoded to the year and both easy to miss:

- `analytics/release_calendar/generate_report.py:24` — `_YAML_PATH` names the file.
- `analytics/release_calendar/report.html:116` — the period label reads `Ago–Dez 2026` as literal
  text. It will silently lie about the wrong year if not updated. Better: compute it from the data.

**The trap: emptying `entries:` destroys the blank lines between groups.** Measured on a scratch copy
— 25 blank lines became 15, exactly one lost per emptied group; comments (27) and all 25 groups
survived intact. The separator rides on `entries.ca.end` (ruamel's sequence footer) and the dumper
won't emit a footer for an empty flow-style `[]`, so it's gone the instant the emptied file is saved
and a later process cannot restore it. **Keeping the `entries:` key rather than deleting it does not
avoid this** — an intuitive assumption that testing disproved. The damage is purely cosmetic, but it
is one more reason the rolling-window path in step 2 is the default.

---

## 6. Verify, then update the docs

```powershell
uv run python -m domain.release_calendar.update_calendar --until 2027-12-31   # re-run: expect "nenhuma mudanca"
uv run python -m domain.release_calendar.update_calendar --coverage           # tabelas do banco sem grupo
```

The refresh must be **idempotent** — a second dry-run right after a `--write` should report
`nenhuma mudanca; o arquivo ja esta em dia`. If it reports drift, something in `_merge`/`_diff` is
mismatching and the write is not stable; do not leave it there.

Then:

- Regenerate the report and **open it in a real browser.** No browser exists in the usual sandbox, so
  no generated version of this report has ever been visually confirmed. Check the month filter pills
  handle two years (they're computed from the data, but have only ever been exercised on one year),
  and that the stat cards agree with the filtered table.
- Update the YAML header comment: the researched-on date and the covered period.
- Update `analytics/release_calendar/report.html:171`, which states the manual-research date.
- Correct any horizon claim you find that step 0 disproved, rather than leaving it in place — the
  "~18 months" error survived in three files (`connectors/bcb_agenda.py`,
  `connectors/CLAUDE.md`, this folder's `CLAUDE.md`) precisely because nobody re-measured.

---

## Reference

- Schema, per-group notes, the `ics:` block, BCB endpoint archaeology, coverage audit:
  [`CLAUDE.md`](CLAUDE.md) in this folder.
- HTTP/ICS layer and its gotchas: [`connectors/bcb_agenda.py`](../../connectors/bcb_agenda.py).
- Report generation: [`analytics/release_calendar/CLAUDE.md`](../../analytics/release_calendar/CLAUDE.md).
- There is **no automated test** for `update_calendar.py`. Its behavior was verified by byte-diffing
  `--write` on scratch copies, idempotency checks, synthetic drift injection, and unit-style asserts
  on `_merge`/`_diff`/`_ref_period`/`_pair_days` including year boundaries — all in-session, none
  checked in. Re-verify the same way after touching it.
