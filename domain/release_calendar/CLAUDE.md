# domain/release_calendar/ — Context for Claude

Static config tracking when Brazilian macro data actually gets published, so a future report/dashboard can show "next release" instead of only historical values. Lives under `domain/` (parallel to `db/`) because it's about data provenance/timing, not an analytics deliverable — but it isn't ETL: nothing here writes to MySQL, it's read-only reference data.

## Files

- `calendar_2026.yaml` — one entry per official release **event** (not per series). BCB in particular bundles dozens of series into a single monthly "nota" (e.g. the credit statistics note covers all 12 `cred_*` tables at once) — grouping by event instead of by series avoids listing the same date a dozen times.
- No `loader.py` yet — added when an actual consumer (a report) needs one. Until then it's just data + docs.

## Schema

```yaml
groups:
  - group: <english_slug>            # stable key, used as a lookup id
    institution: <IBGE|BCB|Tesouro Nacional|MTE/PDET|MDIC>
    name: "<official Portuguese release name>"
    tables: [<macro_brasil/macro_international table names this release feeds>]
    cadence: monthly|quarterly|weekly
    source_url: <calendar page or a representative PDF>
    entries:
      - {date: "YYYY-MM-DD", reference_period: "YYYY-MM"|"YYYY-QN", confirmed: true|false}
```

- `confirmed: true` — date read directly off an official published calendar or PDF.
- `confirmed: false` — the official forward calendar was unreachable (JS-rendered SPA, HTTP error) when this was built (2026-08-13); the date (or `date`/`date_end` window) is an estimate from the historical day-of-month pattern instead. Re-check `source_url` closer to the date before trusting it.
- `reference_period` is the period the release *covers*, not the month it's published in — these are offset by one month (or more) for almost every group here. Match on this field, not on `date`, when asking "when does July data come out."

## Research method (2026-08-13)

Built by dispatching one web-research agent per institution (IBGE; BCB credit note; BCB external-sector/fiscal/Focus/IBC-Br; Tesouro Nacional; MTE+MDIC), each asked to find the official calendar and report exact Aug–Dec 2026 dates or explicitly say "not found" rather than guess. Two of BCB's three calendar pages couldn't be fetched at all (one is a JS-rendered SPA, one returned a genuine HTTP 502) — those groups fall back to historical-pattern estimates, flagged `confirmed: false` above. Everything else came from a live official source, cross-checked where possible against a second independent page.

## Known gaps — not in this file yet

- **International-sourced series** (`cmb_reer`, `cmb_cot_fx`, `cmb_dollar_index`, `cmb_dollar_index_em`, `cmb_policy_rates`, `cmb_real_rates`, `diferenciais_juros`) — BIS/CFTC/FRED/yfinance releases, out of scope for this first pass (research focused on Brazilian institutions only).
- **`cred_ptc`** (Pesquisa Trimestral de Condições de Crédito) — quarterly, not researched; not confirmed whether it's bundled into `bcb_credit_note` or released separately.
- **`atv_pib_usd`, `comm_icbr`, `inflc_meta`, `cmb_risco_pais`** — BCB SGS series (or manual CSV, for the last one) with no dedicated release-calendar research done yet.
- The two "502/JS-rendered" BCB pages (`bcb_credit_note`, `bcb_external_sector_note`, `bcb_fiscal_statistics`) should be retried directly in a browser once the site is reachable, to replace the pattern-based estimates with confirmed dates.

## Pending

- Build the actual calendar view/report that consumes this file — not started.
- Annual refresh: BCB usually publishes its own forward calendar a few weeks into the new semester; re-run the same per-institution research next time (Jan/Jul) rather than hand-extrapolating another year of patterns.
