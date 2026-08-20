# domain/release_calendar/ — Context for Claude

Static config tracking when Brazilian macro data actually gets published, so a future report/dashboard can show "next release" instead of only historical values. Lives under `domain/` (parallel to `db/`) because it's about data provenance/timing, not an analytics deliverable — but it isn't ETL: nothing here writes to MySQL, it's read-only reference data.

## Files

- `calendar_2026.yaml` — one entry per official release **event** (not per series). BCB in particular bundles dozens of series into a single monthly "nota" (e.g. the credit statistics note covers all 12 `cred_*` tables at once) — grouping by event instead of by series avoids listing the same date a dozen times.
- `update_calendar.py` — refreshes the BCB dates from the ICS feeds, audits DB coverage, enumerates BCB's calendar lists. Uses `connectors/bcb_agenda.py` for the HTTP/ICS layer (the usual split: connector = external API client, `domain/` = orchestration).
- `sync.py` — confronts the calendar against the database: did the data actually arrive when the calendar said it would? See its own section below.
- `ROLLOVER.md` — step-by-step runbook for carrying the calendar into the next year. Self-contained on purpose: the year boundary comes up once a year, by which point nobody remembers the traps.
- No `loader.py` — `sync.py` reads the YAML directly with `yaml.safe_load` (read-only; only `update_calendar.py` needs ruamel). A separate loader was never needed.

## update_calendar.py

```powershell
uv run python -m domain.release_calendar.update_calendar              # relatório de drift, não grava
uv run python -m domain.release_calendar.update_calendar --write      # aplica no YAML
uv run python -m domain.release_calendar.update_calendar --coverage   # tabelas do banco sem grupo
uv run python -m domain.release_calendar.update_calendar --listas     # as 29 listas do BCB
uv run python -m domain.release_calendar.update_calendar --horizonte  # até onde cada feed chega
```

Covers only the 10 groups that carry an `ics:` block (all BCB). The other 15 have no equivalent feed and stay manual — the report names them each run so that stays visible rather than looking like full coverage.

**Dry-run is the default on purpose**: the YAML is hand-curated (long per-group notes, reliability caveats) and is the source of truth for metadata. The script only swaps dates; anything surprising in the diff deserves a human look first.

Behaviors worth knowing before trusting a `--write`:
- **Comments survive.** Round-trip via `ruamel.yaml`, verified byte-identical on a no-change load+dump (needs `indent(mapping=2, sequence=4, offset=2)` to match this file's style; plain PyYAML would erase every comment).
- **Matching is date-first, `reference_period` second.** A same-period-different-date pair is reported as `REVISAO DE DATA` rather than an add+remove, which is what keeps a hand-written `note` attached. Matching by period first breaks every group whose period isn't derivable from the feed (Copom uses `281ª reunião`).
- **Nothing outside the fetched window is touched.** Entries before `--from` (default today) or after `--until` (default Dec 31 of the year in the filename) are preserved untouched and excluded from the diff. Without that guard a 2027 date sitting in the 2026 file would be deleted for "not being in the feed".
- **Notes follow a revised date**, recovered via `reference_period`, and the run warns when that happens — the note may have been written about the old date.
- `reference_period` values must stay clean (`"2026-08"`, not `"2026-08 (inferred)"`); they're the match key, so an appended annotation breaks it. Caveats belong in the group `note`.

## sync.py — freshness do banco contra o calendário

Answers what `jobs/update_db.py` can't: the script ran without raising, but did the data
arrive? A `46/46 OK` log line coexists happily with a source that silently returned last
week's data.

```powershell
uv run python -m domain.release_calendar.sync            # relatório completo, exit 1 se houver atraso
uv run python -m domain.release_calendar.sync --quiet    # omite as listas OK / SEM DIVULGACAO
uv run python -m domain.release_calendar.sync --grace 1  # tolera divulgações das últimas 24h
uv run python -m domain.release_calendar.sync --as-of 2026-09-15   # simula outra data
```

**Stateless by construction** — `esperado` = reference period of the most recent release
that already happened; `observado` = `MAX(date)` of the table; late iff `observado < esperado`.
No "when did we last run" marker, so a missed day causes no drift and a recovered gap
self-heals. Two facts make it possible with zero per-table config: the YAML already says
which *period* each release delivers, and **68 of the 69 tables share an identical
`date DATE` column** in the same convention (month start for monthly, quarter start for
quarterly). The 1 without it (`inflc_dim`) is a dimension table, not a published series.
(`pm_parametros` / `pm_hiato_seed` were the other two exceptions until 2026-08-18, when
the BCB-model replication that owned them was removed.)

Five verdicts: `OK`, `ATRASADO`, `SEM EXPECTATIVA` (covered by a group, but no past release
with a datable period — the report says which of the three causes), `SEM CALENDARIO`,
`SEM DIVULGACAO`.

Three consumers read the computation instead of reimplementing it: `status_por_grupo()` (one verdict per
calendar group — worst verdict among its tables — which drives the update button in
[`analytics/release_calendar/`](../../analytics/release_calendar/CLAUDE.md)), `grupos_atrasados()`
(`{grupo: [tabelas]}`, for a future `--due` mode), and `continuas()` (the daily set, for
`jobs/update_db.py --continuous`).

### Three YAML blocks it reads (all top-level, additive)

- **`no_release:`** — tables with no release event on purpose, **split by reason** because the two
  halves have different consumers: `continuous:` (daily market series — PTAX, DXY, Brent, BIS policy
  rates) is what `jobs/update_db.py --continuous` runs every day without consulting the calendar;
  `not_a_series:` (dimension table, model parameters) runs neither daily nor by calendar. Criterion for
  `continuous:` is that `run()` fetches from the source by itself — which is why `cmb_risco_pais` is
  *not* there despite being a market series: its `run()` reads CSVs exported by hand from
  investing.com, so a daily job would fetch nothing. **Declared, never inferred from "has no group"** —
  otherwise a real coverage gap becomes indistinguishable from a deliberate exclusion, which is exactly
  the confusion the `--coverage` triage below had to resolve by hand. (`sem_divulgacao()` also still
  accepts the old flat-list form, so a `calendar_2027.yaml` copied before this change won't break.)
- **`max_age_days:`** — staleness tolerance for **daily content**, the check that was missing. A daily
  table has no reference period to compare against; the right question is "how old is the last point
  relative to *today*?" Expectation = `today − N`, and the **strictest** of this and any calendar
  expectation wins.

  **This was not hypothetical.** Found 2026-08-19: BCB released FX flow, the check said everything was
  OK, and `cmb_cambio_contratado` was sitting at 2026-07-24 while SGS already had 08-14 (3 weeks), with
  `cmb_reservas_bc` at 08-03 against SGS 08-18 (2 weeks). Both are *daily* series filed under the
  *monthly* external-sector note, whose expectation (reference 2026-06) anything recent satisfies. A
  frequency audit — comparing each table's measured date spacing against its group's cadence — found
  exactly 5 such tables, and running their ETL confirmed a third victim, `cmb_dollar_index_em`
  (08-07 → 08-14). Third occurrence of this bug class after `expc_focus`, hence a general rule rather
  than another per-table override.

  It also closed a silent hole: before this, every `no_release.continuous` table was `SEM DIVULGACAO`
  and therefore checked by **nothing** — if the daily job stopped, no one would notice. `SEM DIVULGACAO`
  went from 8 tables to 1.

  **The tolerances are measured, not guessed.** Right after a `--continuous` that finished 9/9 OK,
  `today − MAX(date)` per table isolates the *source's* own publication lag; tolerance = that lag + ~4
  days for weekend/holiday. The first guess understated three of the nine (`cmb_dollar_index_em` needs
  9 not 6 — FRED publishes it weekly; `cmb_policy_rates` 12 not 8 — BIS republishes in batches;
  `cmb_cambio_contratado` 9 not 8). Re-measure the same way if false lateness shows up; don't tighten
  to 1–2 days, that fires every Monday.

  `--continuous` runs the **union** of this block and `no_release.continuous`, which is what pulls
  `cmb_reservas_bc`/`cmb_cambio_contratado` into the daily pass (keeping them current) without removing
  them from the calendar (keeping them checked).
- **`expectation_overrides:`** — per-table corrections where a group's `tables:` link means
  "this release is *relevant* to this table" rather than "this release *delivers* this
  table's period". `tables:` stays as-is on purpose (it's the relevance list the HTML report
  shows); the override only corrects the expectation. Three modes: `expect: none`,
  `lag_months: N` (shifts the expectation, doesn't disable it), `release_minus_days: N`
  (anchors on the release *date* instead of a reference period).

**All four current overrides were diagnosed empirically, not assumed** (2026-08-17): each
table's ETL was executed and `MAX(date)` checked for movement. `cred_credito_familias`
(one month behind the credit note — income data), `cmb_termos_troca` (IPEA/Funcex, own
calendar, filed under BCB's external-sector note by topic affinity) and `inflc_meta`
(annual CMN target, not a quarterly RPM series) did **not** move → the mapping was
over-claiming. In the same test `comm_icbr`/`comm_icbr_usd` **did** move → those were real
staleness, caused by the documented gap that neither is in `jobs/update_db.py`.

The fourth override, `expc_focus`, fixes a blind spot the check itself had: `bcb_focus`'s
weekly entries carry no `reference_period` at all, so the table fell through to `bcb_rpm`'s
*quarterly* expectation and a two-week-stale Focus reported `OK`. Verified by running the
ETL: `2026-07-31 → 2026-08-14`. Anchoring on the release date (BCB publishes Monday with
expectations collected through the prior Friday, and the table's `date` is the collection
date — hence 3 days) closes it. **Any other group whose feed carries no reference period
has the same weakness** — Copom/Copom-Ata are the remaining ones, both harmless since no
table depends on them advancing.

### Past entries are load-bearing now

The check reads the *most recent past* release, so a file holding only future dates makes it
inert. This was real: at first run 45 of 66 tables reported `SEM EXPECTATIVA`. Fixed by
backfilling the 10 BCB groups with `--from 2026-05-01 --write` (the ICS feeds carry history
back to 2020 — measured, see `--horizonte`). Consequence to know: **`update_calendar.py`'s
default `--from today` never adds past entries**, it only preserves them, so the file
accretes history going forward on its own. The 15 non-BCB groups still hold future dates
only, which is why ~20 tables remain `SEM EXPECTATIVA` — closing that is the same IBGE-API
work already listed in Pending.

## Rolling over to the next year

📄 **Full runbook: [`ROLLOVER.md`](ROLLOVER.md)** — read it before touching the year boundary. Short version:

- **Don't create a new file.** `--until 2027-12-31 --write` extends the existing one; the `_em_escopo` guard makes a multi-year file safe. A per-year file needs two hardcoded-year code edits and quietly costs the blank lines between groups.
- **It's not a once-a-year chore.** Measured 2026-08-17 via `--horizonte`: 7 of the 10 BCB feeds stop at 31/12 of the running year, `bcb_copom` reaches +16 months, IBC-Br/IC-Br +6. IBGE's API is the same. So the next year fills in over several months — re-run periodically through H1.
- **Measure, never assume, the horizon** — that's what `--horizonte` is for. The claim "~18 months forward" sat wrong in three files for months because nobody re-checked.

## `ics:` block (machine-readable refresh config)

Additive per-group schema, read only by `update_calendar.py`:

```yaml
    ics:
      lista: "Sondagens - PTC PEF"   # exact name, from BCBAgenda.listas()
      summary_contains: "PTC"        # optional: feed mixes releases, filter by title
      ref: {unit: month, lag: 1}     # optional: how to derive reference_period
      pair_days: true                # optional: Copom's 2-day meeting -> date_start + date
```

`ref.unit` is `month` or `quarter`; `lag` is how many periods back the release covers (`{unit: quarter, lag: 0}` for the RPM, which covers the quarter it's published in). Omit `ref` when the period isn't derivable — Copom's meeting number and Focus (no period at all).

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

## BCB access notes (2026-08-14) — read this before trying to re-scrape BCB

Three findings from a second research round, all verified live. They matter well beyond this file.

**1. `www.bcb.gov.br` is an Angular SPA — every HTML path returns the same empty 2871-byte shell.** `/acessoinformacao/calendariobc`, `/acessoinformacao/calendariobc_ics`, `/en/about/rssen`, `/estatisticas/notas_calendario` all return `<app-root></app-root>` and nothing else to a plain fetch. There is no `.ics` file at the `_ics` URL — it's an Angular *route*, not a download. Don't waste time re-fetching these.

**2. BCB's REST API works, but only with browser-like headers.** Requests to `https://www.bcb.gov.br/api/servico/sitebcb/<service>` get a 400 from BCB's edge WAF unless you send `Accept`, `Referer: https://www.bcb.gov.br/` and a real browser `User-Agent`. With those headers the same URLs return clean JSON. Endpoints confirmed working:

| Endpoint | Returns |
|---|---|
| `/api/servico/sitebcb/copom/atas?quantidade=N` | Past Copom meetings: `nroReuniao`, `dataReferencia` (= meeting day 2), `dataPublicacao` (= Ata) |
| `/api/servico/sitebcb/copom/comunicados?quantidade=N` | Same shape, for Comunicados |
| `/api/servico/sitebcb/rpm/proximos-relatorios?inicioAgenda=YYYY-MM-DD` | **Forward** RPM calendar — the one genuinely forward-looking BCB endpoint found |
| `https://dadosabertos.bcb.gov.br/api/3/action/*` | CKAN open-data catalog (no special headers needed) — how the above were discovered |

OpenAPI specs live at `https://www.bcb.gov.br/conteudo/dadosabertos/BCBDeinf/{copom,rpm_prop,ri_prop}.yaml`. Their full documented path list is small: Copom exposes only `/atas`, `/atas_detalhes`, `/comunicados`, `/comunicados_detalhes` — no forward Copom-calendar endpoint at this path (see point 4 below for the one that does exist).

**4. THE ONE THAT ACTUALLY WORKS — `/api/exportarics/sitebcb/agendaics?lista=<Nome Exato>` returns a real, forward-looking `.ics` file.** No special headers needed (unlike point 2's REST API), and it is *not* the same thing as the dead `_ics` SPA route in point 1. This is now the primary source for every BCB group in `calendar_2026.yaml` and supersedes both the "no forward Copom endpoint" claim above and the derived-rule workaround below. **How far forward each feed runs is short and mostly capped at the current calendar year** — see "Rolling over to the next year" below for the measured per-list horizons and what that implies for building a 2027 file.

Note the asymmetry that makes this confusing: the human-facing pages `/acessoinformacao/calendariobc` and `.../calendariobc_ics` are **both dead server-side** — their content API (`/api/pagina/sitebcb/calendariobc[_ics]`) returns a SharePoint `File Not Found` stub — yet the ICS export API behind them serves fine. A browser still renders the page because Angular builds the list-picker from the *service* endpoints below, not from page content. So "the page works in my browser but not for you" and "the page is broken" are both true at once.

**Enumerating the `lista` values (don't guess them, and don't ask the user to read them off the page).** Two service endpoints, both plain GETs needing only a browser `User-Agent`:

| Endpoint | Returns |
|---|---|
| `/api/servico/sitebcb/calendario/categorias?lista=CategoriasCalendario` | The 14 category names (Copom, Estatísticas, Sondagens do BC, …) |
| `/api/servico/sitebcb/calendario/catassociado?lista=CalendariosAssociacaoCategorias` | **All 29 calendar lists** — `lista` (the exact string to pass to `agendaics`), its categories, `linkPadrao`, `eEvento` |

Discovered by scraping the SPA: fetch the page shell, pull the `chunk-*.js` bundle names out of `main-*.js`, grep them for `agendario`/`calendario` components, then read `calendario-card.component-*.js` — it hardcodes `identificador="calendario"` plus the `categorias`/`catassociado`/`selecionacatassociado` paths and the two SharePoint list names above. (`selecionacatassociado` additionally needs `&categoria=<name>`; it 500s without it. `catassociado` with no category returns everything, which is what you want.)

The 29 lists, as of 2026-08-17 — **project-relevant ones in bold**: **Reuniões do Copom**, **Atas e Comunicados do Copom**, **Focus**, **Estatísticas fiscais**, **Estatísticas do setor externo**, **Estatísticas monetárias e de crédito**, **Índice de atividade econômica (IBC-Br)**, **Índice de Commodities – Brasil (IC-Br)**, **Sondagens - PTC PEF**, **Relatório de Política Monetária**; then the unused rest — Reuniões do CMN e COMOC, Indeco, Estatísticas do Valores a Receber, Eventos, Events, Capitais Internacionais, Boletim Regional, Reuniões do Comef, Reuniões do Coremec, Reuniões do GRC, Ranking de Reclamações, Estatísticas macroeconômicas (quarterly EBI / Títulos de Dívida / Matriz do Patrimônio Financeiro), Estatísticas macroeconômicas mensais (only "Estatísticas de Pagamento por Atividade Econômica"), Estatísticas do mercado aberto, Índice de Atividade Econômica Regional (IBCR), Relatório de Investimento Direto, Sondagens do BC, Relatório de Estabilidade Financeira, Atas e Comunicados do Comef.

**Parse the raw ICS yourself — do not let a summarizing fetch do it.** A scratch parser (`BEGIN:VEVENT` → `DTSTART`/`SUMMARY`, honoring RFC 5545 line-folding on continuation lines) is ~40 lines. This matters concretely: a summarized read of the IBC-Br feed reported 2026-08-16, but the raw feed says **2026-08-17** — a wrong date that briefly landed in the YAML before the raw parse caught it. Summaries also silently elide with "continues monthly through…", which hides exactly the holiday shifts you need (see `bcb_focus`: three 2026 releases move to Tuesday).

**3. BCB's statistics release calendar is genuinely broken server-side, not merely unreachable.** `GET /api/pagina/sitebcb/notas_calendario` returns the page's real SharePoint payload, and that payload is a `File Not Found` redirect stub. The two `Lists/...aspx` calendar pages return a true HTTP 502. So *nobody* can read BCB's forward statistics calendar right now — this is not a scraping limitation to engineer around, and re-checking later is the only fix.

**Superseded fallback (kept in case the ICS feed ever dies).** Before point 4 was found, the release *rule* for the three monthly notes was measured from BCB's own archive: each note's real publication timestamp read from the `Last-Modified` header of its archived PDF, giving 7 real 2026 dates per note → fiscal = 2nd-to-last business day (7/7 exact), credit = 3rd-to-last (6/7), external sector = no clean rule. Worth knowing the accuracy this achieves: checked against the now-confirmed ICS dates, the credit rule was **systematically one day early on all five** forward dates, and the external-sector window missed December badly (real 12-18 vs. a guessed 12-23/29). Treat derived rules as ±1 day at best, and re-derive from the ICS rather than the PDFs whenever possible.

PDF URL patterns, for re-measuring later (note the inconsistent `de_`/`do_`):
```
/content/estatisticas/hist_estatisticasfiscais/<YYYYMM>_Texto_de_estatisticas_fiscais.pdf
/content/estatisticas/hist_estatisticasmonetariascredito/<YYYYMM>_Texto_de_estatisticas_monetarias_e_de_credito.pdf
/content/estatisticas/hist_estatisticassetorexterno/<YYYYMM>_Texto_de_estatisticas_do_setor_externo.pdf
```
`<YYYYMM>` is the **publication** month; the note covers month M-1.

## Non-BCB sources — where they're recorded, and how automatable (probed 2026-08-17)

Every group's origin is in its own `source_url` in the YAML; the 15 non-BCB groups share just 6 distinct pages. All six answered HTTP 200 as plain static content — **none is an SPA**, so all are scrapeable, unlike BCB's site.

| Source | Groups | Format | Automatable? |
|---|---|---|---|
| `servicodados.ibge.gov.br/api/v3/calendario` | the 8 `ibge_*` | **JSON API** | **Yes — best case of all, see below** |
| `federalreserve.gov/monetarypolicy/fomccalendars.htm` | `fomc` | static HTML, 164KB | Likely (parse the table) |
| `cftc.gov/.../ReleaseSchedule/index.htm` | `cftc_cot` | static HTML, 48KB | Likely |
| `balanca.economia.gov.br/balanca/cronograma/` | `mdic_comex_stat` | static HTML, 1.4MB | Likely |
| `cdn.tesouro.gov.br/.../2026_2sem.pdf` | `tesouro_rtn`, `tesouro_efgg` | **PDF** (semester calendar) | Harder — `pdfplumber` is already a dep; URL changes each semester |
| `gov.br/trabalho-e-emprego/.../calendario-de-divulgacao-do-novo-caged` | `mte_caged_novo`, `bcb_caged_sgs_mirror` | static HTML (gov.br) | Likely |

**IBGE's calendar API is better than BCB's ICS feeds** and is the obvious next automation target (8 of the 15 manual groups):

- `GET /api/v3/calendario/?de=YYYY-MM-DD&ate=YYYY-MM-DD&qtd=100` — real server-side date filtering (63 releases across 22 products in Aug–Dec 2026, one page). Paginated envelope (`count`/`totalPages`/`items`).
- It returns the **reference period explicitly** (`ano_/mes_referencia_inicio` + `_fim`), so unlike the BCB groups there's no `ics.ref` lag rule to infer. Caveat: a quarter is expressed as its first and last month (`2026-04`…`2026-06` = Q2), so a consumer must fold that into a `YYYY-QN` label itself.
- Send `Accept-Encoding` handling / use `requests` — responses are gzipped and raw `urllib` chokes on them intermittently.
- Product IDs, mapped and verified: `ibge_pim`→**9294** (`PIM-PF Brasil#pimpf1`; 9296 is the *Regional* variant, which no table here uses), `ibge_pmc`→**9227**, `ibge_pms`→**9229**, `ibge_pib_trimestral`→**9300**, `ibge_pnad_mensal`→**9171**, `ibge_pnad_trimestral`→**9173**, `ibge_ipca`→**9256**, `ibge_ipca15`→**9260**. Titles carry internal slugs (`Divulgação mensal#pnadc1`), so match on `produto_id`, never on the name.
- **Cross-validation: all 29 forward IBGE dates in the YAML match this API exactly, 0 divergences** — the original hand research was right, and these dates are effectively double-sourced now.

## Known gaps — not in this file yet

- **BCB's WEEKLY FX-flow release is not modelled** (found 2026-08-19). BCB publishes the *fluxo
  cambial* weekly (the "Nota Cambial", Wednesdays), and that release appears on **none** of BCB's 29
  calendar lists — verified live: the only relevant list, `Estatísticas do setor externo`, returns
  monthly events only (2026-07-28, 2026-08-27) for Jul–Sep 2026. So the calendar, which is built from
  those feeds for every BCB group, has no way to know the weekly note exists. Consequences, all three
  distinct:
  1. There is no calendar row for the weekly release, and can't be until someone enters the dates by
     hand or scrapes the note's own page. `update_calendar.py` cannot help — there is no feed.
  2. `cmb_fluxo_cambial` holds the **monthly** SGS aggregation (24352/24370/24371/…), not the weekly
     detail. Checked live: SGS's own latest for those series is 2026-07-01, exactly what the DB has —
     that table is *not* stale, it simply isn't the weekly product.
  3. The weekly detail (CEP/CBE sub-items) is **not ingested at all**. The script's own docstring
     already flagged this: the SGS codes for that granularity "não foram identificados com certeza na
     fase de pesquisa". Still open.
- **International — still missing.** `cmb_reer` / `cmb_policy_rates` / `cmb_real_rates` (**BIS** — cadence not verified, do not assume the "3rd week of the month" figure that circulated in an earlier draft; it was an unchecked assumption, never confirmed) and `clima_oni` (**NOAA CPC** — monthly, but the "2nd Thursday" rule is likewise unverified). Both were left OUT of the YAML rather than guessed. `cmb_cot_fx` (CFTC) and `diferenciais_juros`' Fed side (FOMC) **are now in** — both read off the issuing body's own published calendar.
- **Daily market series need no calendar entries**: `cmb_dollar_index`, `cmb_dollar_index_em`, `cmb_fx_latam`, `comm_brent` are continuous market/daily data with no discrete release event. Deliberately not modelled as dated entries.
- **LatAm CPI dates** (INEGI/INE/DANE/INEI — feed `cmb_real_rates`) not researched.
- **`atv_pib_usd`, `comm_icbr`, `inflc_meta`, `cmb_risco_pais`** — BCB SGS series (or manual CSV, for the last one) with no dedicated release-calendar research done yet. `comm_icbr` (IC-Br) is known to share a BCB calendar page with IBC-Br/IBCR, so it likely rides along with `bcb_ibcbr`.
- **All BCB groups are `confirmed: true` as of 2026-08-17**, sourced from the ICS feeds in point 4. That closed every BCB gap previously listed here: `bcb_ibcbr`, `bcb_copom`, `bcb_copom_ata`, `bcb_ptc`, `bcb_fiscal_statistics`, `bcb_external_sector_note`, `bcb_credit_note` (the last BCB note to be found — its list is `Estatísticas monetárias e de crédito`), plus `bcb_focus` upgraded from a bare weekday rule to 19 itemized dates, and a brand-new `bcb_icbr` group. `bcb_rpm` is now double-sourced (RPM API + ICS agreeing exactly).
- **`comm_icbr` is now covered** by the new `bcb_icbr` group — and this **corrects an assumption previously recorded here**: IC-Br does *not* ride along with `bcb_ibcbr`. It has its own calendar list, releases Wednesdays at 14:30 (vs. IBC-Br's 09:00), and its dates never coincide with IBC-Br's. Its `reference_period` mapping is still inferred from the one-month-lag pattern, not stated by the feed.
- **`inflc_meta` / `atv_pib_usd` / `cmb_risco_pais`** — still no dedicated release-calendar research. `inflc_meta` rides with CMN decisions (`Reuniões do CMN e COMOC` list exists, not yet pulled).
- **The remaining `confirmed: false` entries are only `bcb_caged_sgs_mirror`** — derived from MTE's calendar rather than a BCB source, so the ICS feed doesn't help it.

### Coverage audit: what the 16 uncovered tables actually are

`--coverage` reports 53/69 tables covered (re-measured 2026-08-18, after `pm_hiato_produto`/`pm_hiato_produto_vintages` were added and `pm_hiato_seed`/`pm_parametros` dropped). Triaged 2026-08-17 so future runs don't re-litigate the same list:

- **Deliberate, no release event exists** — continuous daily market data: `cmb_dollar_index`, `cmb_dollar_index_em`, `cmb_fx_latam`, `cmb_equity_us`, `cmb_ptax`, `comm_brent`. Plus `inflc_dim` (dimension table). `pm_hiato_seed` / `pm_parametros` were here too until 2026-08-18, when they were dropped with the BCB-model replication.
- **`expc_focus_pre202608`** — surfaced by the 2026-08-18 re-measure, not in the 2026-08-17 triage. Frozen snapshot of the pre-rewrite Focus table; if it's dead weight it should be dropped rather than covered, but that hasn't been confirmed.
- **Genuine gaps, need research**: `atv_pib_usd`, `cmb_risco_pais`, `clima_oni` (NOAA CPC), the BIS trio `cmb_reer` / `cmb_policy_rates` / `cmb_real_rates`, and `fisc_investimento` (Tesouro's Séries Temporais API, Tema 13 — a different release from RTN/EFGG, would need its own group).
- **`atv_pib_mensal`** — BCB SGS 4380/4382. Likely rides with the monetary/credit note (it's the same 12-month-accumulated GDP denominator BCB uses for `cred_credito_resumo.pct_pib_*`), but that's an inference, not verified — left uncovered rather than asserted.
- **Two were found miscategorized by this audit and fixed**: `fisc_dlsp_fatores` now sits under `bcb_fiscal_statistics` (it comes from the Facdetp.xlsx tabela especial, overwritten at each monthly fiscal release), and `comm_icbr_usd` under `bcb_icbr` (SGS 29042, same release as `comm_icbr`).
- The 502-dead BCB calendar pages no longer matter for date sourcing — point 4's ICS feeds replaced every derived-rule date. No need to keep re-checking them.

## Pending

- ~~Build the actual calendar view/report~~ — **done**, it's [`analytics/release_calendar/`](../../analytics/release_calendar/CLAUDE.md) (HTML report reading this YAML). Regenerate it after every `--write`: `uv run python -c "from analytics.release_calendar.generate_report import run; run()"`. Nothing chains the two automatically.
- **Annual refresh**: the BCB half is now `update_calendar.py` (done — this replaced the "promote the scratch parser" item). To start 2027, copy the YAML to `calendar_2027.yaml`, empty the `entries` of the BCB groups, and run `--write --from 2027-01-01`; the feeds already carry 2027. Only the non-BCB groups (IBGE, Tesouro, MTE, MDIC, CFTC, FOMC) still need per-institution research.
- **Extend `update_calendar.py` to IBGE** — the 8 `ibge_*` groups via `servicodados.ibge.gov.br/api/v3/calendario` (see the table above: product IDs already mapped and validated). Would need a `connectors/ibge_agenda.py` sibling to `bcb_agenda.py`, and an `api:`-style block alongside `ics:` in the YAML — or a small `source:` discriminator, since the existing `ics:` key is BCB-shaped. That single addition takes automated coverage from 10/25 groups to 18/25.
- Copom/Ata `reference_period` (`281ª reunião`) can't come from the feed — new meetings get flagged for manual fill. BCB's `copom/atas` API does return `nroReuniao`, so the script could derive it; not wired up.
- `Reuniões do CMN e COMOC` list not yet pulled — the likely calendar source for `inflc_meta` (CMN sets the inflation target).
- `update_calendar.py` has no automated test. The logic was verified by a throwaway assert script (merge/diff/ref-period/day-pairing, including year boundaries) plus a byte-diff of `--write` on a copy; nothing is checked in. **`sync.py` does have one** — [`tests/test_sync_calendar.py`](../../tests/test_sync_calendar.py), 31 asserts over the pure expectation logic (no DB), same runnable-script style as `tests/test_ibge2.py` since the project has no pytest. It caught two real bugs while being written: a malformed `reference_period` (`"2026-13"`) crashing the whole run instead of degrading to "not datable", and `date.__format__` treating a format spec as a `strftime` pattern (`f"{some_date:12s}"` prints `"12s"`).
- **Wire `sync.py` into the routine**: it's on-demand only. Natural next steps, in order — a `--due` mode on `jobs/update_db.py` consuming `grupos_atrasados()` (needs the `SEM CALENDARIO` list closed first, or gating would skip those tables forever), an update button on the HTML report (see [`analytics/release_calendar/CLAUDE.md`](../../analytics/release_calendar/CLAUDE.md)), and a daily scheduled run for the alert.
- **`SEM EXPECTATIVA` for the 15 non-BCB groups** — they hold future dates only. Same fix as the IBGE-API item above; for Tesouro/MTE/MDIC/CFTC/FOMC it means entering recent past dates by hand.
