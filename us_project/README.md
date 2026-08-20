# US pipeline — source mapping (initial discussion)

Pre-build survey of what US macro data exists, who publishes it, how we can reach it, and what
we already have. Same purpose and shape as the Brazil-side source maps
([`analytics/brasil/labor_market/fontes_dados.md`](../analytics/brasil/labor_market/fontes_dados.md),
[`analytics/brasil/fiscal_policy/fontes_dados.md`](../analytics/brasil/fiscal_policy/fontes_dados.md)) — one
file per macro branch, each with a coverage table, a live-verified series inventory, gotchas and
open items. This folder is for the scoping conversation that comes first — but it is no longer
purely a scoping folder: the **inflation branch has started building**. Done as of 2026-08-18:
[`connectors/bls.py`](../connectors/bls.py) (working, API key installed, limits measured live) and
the CPI item hierarchy in [`inflation_hierarchy.md`](inflation_hierarchy.md) +
[`cpi_item_hierarchy.tsv`](cpi_item_hierarchy.tsv) /
[`cpi_newsrelease_table1.tsv`](cpi_newsrelease_table1.tsv). Still not built for **any** branch:
the `macro_us` schema, the ETL scripts, the reports.

**Where the built code goes.** `analytics/` was reorganised country-first in 2026-08 (see
[`analytics/CLAUDE.md`](../analytics/CLAUDE.md)), so a US report lands in `analytics/us/<area>/` —
`analytics/us/inflation/` for the first one — and its ETL in `domain/db/us/<area>/`, mirroring
`domain/db/brasil/`. The "Brazil counterpart" column below is therefore the *precedent to copy*,
not the destination: `analytics/brasil/inflation/` is the model for `analytics/us/inflation/`.

**Method — everything below was probed live against each source on 2026-08-17**, not read off
documentation. 377 candidate FRED series were checked one by one against `/fred/series` (existence,
frequency, units, SA flag, real observation window, publishing release); 25 of them do not exist,
and the rest are inventoried in the branch files. Every non-FRED source was hit directly and the
response body inspected — file magic bytes checked, so a 200-with-an-HTML-error-page is not
recorded as a success. Claims I could **not** verify are labelled as such inline.

The raw probe output is kept alongside these notes as
[`fred_inventory.tsv`](fred_inventory.tsv) — 377 rows, one per candidate series, with branch, id,
status, title, frequency, units, SA flag, observation window, last-updated date, publishing release
and last value. Every FRED claim in the branch files is auditable against it, and it is the seed list
for whatever gets ingested. **Four rows are marked `MISSING` but do exist** (`CES0500000017`, `M2V`,
`HDTGPDUSQ163N`, `BOGZ1FL194090005Q`) — transient API errors during the threaded run, caught and
corrected on an individual re-check; the branch files use the corrected counts.

## Branch files

| File | Brazil counterpart | Scope |
|---|---|---|
| [`activity_fontes_dados.md`](activity_fontes_dados.md) | `analytics/brasil/economic_activity/` | GDP/NIPA, industrial production, retail, orders, inventories, income, sentiment, nowcasts |
| [`labor_market_fontes_dados.md`](labor_market_fontes_dados.md) | `analytics/brasil/labor_market/` | CPS, CES, JOLTS, claims, ECI, productivity, wage trackers |
| [`inflation_fontes_dados.md`](inflation_fontes_dados.md) | `analytics/brasil/inflation/` | CPI, PCE, PPI, import/export prices, cores/trimmed means, expectations |
| ↳ [`inflation_hierarchy.md`](inflation_hierarchy.md) | — | **How the inflation data nests** (2026-08-18): the CPI's **two** trees — the 294-item / 9-level expenditure structure and the 37-row news-release structure (food / energy / core goods / core services) — both with weights and series ids and both validated against the weight identities; why every other US price measure is flat or nests differently; proposed `macro_us` tables |
| ↳ [`cpi_item_hierarchy.tsv`](cpi_item_hierarchy.tsv) · [`cpi_newsrelease_table1.tsv`](cpi_newsrelease_table1.tsv) | — | Machine-readable form of those two trees — level, parent, CPI-U/CPI-W weights, SA and NSA series ids, coverage window. Seed for `inflc_cpi_dim` |
| [`monetary_policy_fontes_dados.md`](monetary_policy_fontes_dados.md) | `analytics/brasil/monetary_policy/` | Fed target/effective rates, yield curve, balance sheet, money, financial conditions, SEP |
| [`fiscal_policy_fontes_dados.md`](fiscal_policy_fontes_dados.md) | `analytics/brasil/fiscal_policy/` | MTS receipts/outlays, debt stock and holders, NIPA government accounts, CBO |
| [`credit_fontes_dados.md`](credit_fontes_dados.md) | `analytics/brasil/credit/` | H.8 bank credit, SLOOS, G.19 consumer credit, delinquencies, Z.1 debt, FDIC |
| [`external_sector_fontes_dados.md`](external_sector_fontes_dados.md) | `analytics/brasil/exchange_rate/` | Dollar indices, trade, current account, IIP, TIC, reserves |
| [`housing_fontes_dados.md`](housing_fontes_dados.md) | *(none)* | Starts/permits/sales, prices, mortgage rates, vacancy, residential construction |

**Why housing is its own branch and not a section of activity**: it has its own release cycle, its
own primary agencies (Census+HUD, NAR, FHFA, S&P/Cotality, Freddie Mac — five, none of which
publish anything else on this list), and it is the branch where US licensing restrictions bite
hardest (see the FRED windowing gotcha below). Brazil has no equivalent because there is no
comparable monthly housing statistics complex. The other seven map 1:1 onto existing Brazil
branches, so the reports can reuse the same tab/table patterns.

**`external_sector` rather than `exchange_rate`**: the Brazil report is built around what drives
BRL. For the US, the dollar is one input among many and the interesting object is the external
accounts themselves (trade, current account, net international investment position, foreign
holdings of Treasuries). Same tables, different centre of gravity — hence the different name.

## Access status — what each source demands (all live-tested 2026-08-17)

| Source | Auth | Status | Note |
|---|---|---|---|
| **FRED** | API key — **we have one** (`FRED_API_KEY` in `.env`) | ✅ working | The broadest distributor by far. 352 of 377 candidate series confirmed present |
| **BLS API v2** | key optional | ✅ works **unregistered** | Confirmed live: a 1-series request with no `registrationKey` returned data. Unregistered caps: 25 series / 10 years / 25 queries per day; registered: 50 / 20 / 500 |
| BLS API v1 | none | ⚠️ partial | CPI and CES returned data; **JOLTS did not** — `"Series does not exist for Series JTSJOL"`. v1 is not a full substitute for v2 |
| **BLS flat files** (`download.bls.gov/pub/time.series/`) | none, but **needs an identifying User-Agent** | ✅ working | 403 Access Denied with a normal browser UA; 200 with `LISCapital-macro-pipeline/1.0 (fabian@liscapital.com.br)`. This is the only path to the *full* series catalogs — `cu` (CPI, 1.34 MB), `ce` (CES, 3.94 MB), `jt` (JOLTS), `ln` (CPS, 15.3 MB), `wp` (PPI), `ci` (ECI), `pr` (productivity) |
| **BEA API** | UserID required | ❌ **blocked** | Empty and invalid keys both return `APIErrorCode 1`. Free registration at `apps.bea.gov/API/signup` — **needs the user to request one** |
| **Census API** | key required | ❌ **blocked** | Every `api.census.gov/data/timeseries/eits/*` call returns an HTML page titled `Missing Key`. The discovery catalog (`eits.json`) works without one. Free key at `api.census.gov/data/key_signup.html` — **needs the user to request one** |
| **Treasury Fiscal Data** | none | ✅ working | MTS tables 1/4/5, Debt to the Penny, MSPD, average interest rates, Daily Treasury Statement — all returned live JSON |
| **Treasury yield curves** | none | ✅ working | Par yields (14 tenors) and TIPS real yields (5 tenors), one CSV per calendar year |
| **Fed Board DDP** | none, but **needs a series hash** | ✅ working, with a trap | H.15 and H.8 both returned real CSV. `Output.aspx` **without** a `series=` hash returns HTTP 200 with a **zero-byte body** — a silent failure, not an error. Hashes are scrapable from `Choose.aspx?rel=<REL>` (5+ found on the H.8 page) |
| Fed Z.1 (Financial Accounts) | none | ✅ working | `z1_csv_files.zip`, 8.08 MB |
| **NY Fed markets API** | none | ✅ working | JSON reference rates: SOFR, EFFR, OBFR, SOFR averages/index |
| NY Fed research xlsx | none | ✅ working | SCE inflation expectations (1.23 MB xlsx), ACM term premium (10.1 MB xls), GSCPI, Household Debt & Credit report |
| **Atlanta Fed** xlsx | none | ✅ working, with a trap | Only under `/-/media/Project/Atlanta/FRBA/Documents/…`. The shorter `/-/media/documents/…` path returns **HTTP 200 with a 48,302-byte HTML soft-404** — check content, never status. GDPNow (10.9 MB), Wage Growth Tracker, Sticky-Price CPI |
| **Philly Fed** | none | ✅ working | ADS index xlsx, coincident indexes xls, MBOS history csv/xls. Real paths must be scraped off the landing page — hand-guessed ones 404 |
| FHFA House Price Index | none | ✅ working | `hpi_master.csv`, 17.0 MB, all flavours/levels in one file |
| FDIC BankFind API | none | ✅ working | 4,352 institutions returned for `REPDTE:20260331` |
| Treasury TIC | none | ✅ working | Major foreign holders and long-term securities CSVs |
| OFR Financial Stress Index | none | ✅ working | Daily CSV back to 2000 |
| **EIA v2** | key required | ❌ blocked | `API_KEY_MISSING`. Only matters if we want energy detail beyond FRED's WTI/Brent/Henry Hub/gasoline |
| **CBO** | — | ❌ blocked | 403 bot-protection on the xlsx. FRED already carries CBO's `GDPPOT` and `NROU` (to 2036), which may be all we need |
| **UMich Surveys of Consumers** | — | ⚠️ unresolved | Could not find a working direct file path (`fetchdoc.php` returns "Sorry, I can't find the file"). FRED redistributes `UMCSENT`/`MICH` but **~2 months stale** (last obs 2026-06 as of 2026-08-17) |
| **ISM** (manufacturing/services PMI) | licensed | ❌ **not obtainable** | Zero FRED search results for "ISM Manufacturing PMI" / "ISM Purchasing Managers Index" / "ISM Services"; the legacy ids `NAPM`, `NAPMPI`, `NAPMNOI`, `NMFBAI` all return `"The series does not exist"`. `ismworld.org` serves a captcha. Would need a paid ISM licence |
| **Conference Board** (LEI, consumer confidence) | licensed | ❌ **not obtainable** | Zero FRED results; `CONCCONF` does not exist |
| **NAHB** (housing market index) | licensed | ❌ not obtainable | Zero FRED results |
| **Zillow** (ZORI/ZHVI) | — | ❌ not on FRED | `ZORI` does not exist. Zillow's own research download page not tested |

**Practical read**: FRED alone covers most of what a first version of each report needs, and we
already have that key. The two free registrations worth requesting are **BEA** (the only way to get
NIPA/ITA at full table granularity rather than FRED's curated selection) and **Census** (retail,
housing, orders and trade at product/geography detail). Neither blocks a first build. ISM and the
Conference Board are genuinely unavailable at any effort short of a licence — plan the activity
branch so it does not depend on them.

## What we already have

No `macro_us` schema exists — confirmed live against the MySQL server: the schemas are
`macro_brasil` (55 tables) and `macro_international` (11 tables), plus non-macro ones. `macro_us`
is reserved in [`domain/db/CLAUDE.md`](../domain/db/CLAUDE.md) as a future schema and is still empty
of even a definition.

US data that exists today lives in `macro_international`, always because some Brazil-facing series
needed it (verified live):

| Table | US content | Range | Rows |
|---|---|---|---|
| `diferenciais_juros` | `fed_funds`, `cpi_12m_us`, `real_us_ex_post` (alongside the BR side and the differentials) | 1995-01 → 2026-08 | 2,825 |
| `cmb_dollar_index` | `dxy` (Yahoo Finance ICE index) | 1971-01 → 2026-08 | 14,114 |
| `cmb_dollar_index_em` | FRED `DTWEXEMEGS` | — | — |
| `cmb_equity_us` | `sp500` — **not documented in any `CLAUDE.md`**, found by inspecting the live schema | 1990-01 → 2026-08 | 9,214 |
| `comm_brent` | `brent_usd` (FRED `DCOILBRENTEU`) | 1990-01 → 2026-07 | 9,258 |
| `clima_oni` | Oceanic Niño Index (NOAA) | 1950-01 → 2026-04 | 306 |

Outside the database, `analytics/oraculo/us/term_us.py` already pulls **23 FRED series** ad hoc for
the macro thermometer (unemployment, JOLTS/unemployed ratio, payrolls, hourly earnings, PCE and
core PCE, sticky/flexible CPI, PPI, Michigan expectations, retail sales, industrial production, GDP
YoY and QoQ, NFCI, ANFCI, and six housing series). It writes a CSV, never MySQL. That script is the
de facto current US pipeline and the natural first consumer of a `macro_us` schema — see its own
pending item in [`analytics/oraculo/CLAUDE.md`](../analytics/oraculo/CLAUDE.md).

`connectors/fred.py` exists and works (`FredUniFrame`/`FredMultFrame`, key from `.env`), in the old
CamelCase style rather than the class-based pattern of `connectors/ibge.py`/`bcb.py`.
**`connectors/bls.py` was written on 2026-08-18** and is the first US connector built to the current
conventions (class-based, key from `.env`, `date`/`value` output). It replaces the dead stub that used
to live in `not_in_production/` — that file's hardcoded key was invalid (`"The key:8c7fe923… provided
by the User is invalid"`), it pointed at a spreadsheet on the old Dropbox layout, and its date parser
crashed on the BLS's `M13` annual-average rows; it has been removed (recoverable from git). The new
connector covers three access paths — API by series id, the raw `download.bls.gov` flat files for
backfill and dimensions, and the CPI relative-importance xlsx for weights — and serves every BLS
survey (CPI, PPI, CES, CPS, JOLTS, import/export prices) through the same call. Full behaviour and
gotchas in [`connectors/CLAUDE.md`](../connectors/CLAUDE.md).

## Naming and schema proposal (for discussion, nothing decided)

Following the repo rule that the prefix classifies *what the data is*, independent of schema
(see [`domain/db/CLAUDE.md`](../domain/db/CLAUDE.md)):

```
macro_us
  atv_*    activity            (reuses macro_brasil's prefix)
  mt_*     labor market        (reuses)
  inflc_*  inflation           (reuses)
  fisc_*   fiscal              (reuses)
  cred_*   credit              (reuses)
  cmb_*    external sector/FX  (reuses)
  expc_*   expectations        (reuses — SEP, SPF, SCE, breakevens)
  ???_*    monetary policy: rates/balance sheet/money have no Brazil prefix to reuse
  ???_*    housing: no Brazil counterpart at all
```

**Two open naming decisions.** Brazil never needed a rates/policy prefix (Selic lives inside
`cred_inadimplencia_pj`, `diferenciais_juros`, `expc_focus`) and never needed a housing one. The US
needs both. Candidates: `mon_` or `jur_` for policy/rates, `hous_` or `imob_` for housing. Since
this branch of the project is English-first, my recommendation is **`mon_`** and **`hous_`** — but
it breaks the Portuguese-abbreviation pattern of the existing prefixes, so it is the user's call.

**One open scope decision**: whether daily market data (yield curve by tenor, spreads, dollar
indices, VIX) belongs in `macro_us` or stays in `macro_international` next to `cmb_dollar_index`
and `cmb_equity_us`. The schema rule says "anything needing 2+ countries" goes international —
by that rule the US yield curve is `macro_us`, and `cmb_equity_us`/`cmb_dollar_index` arguably
sit in the wrong schema today.

## Open items for the discussion

- **Request the free BEA and Census API keys** — the only two hard blockers found, and both take
  minutes. Nothing else on this list needs credentials we lack.
- **Decide the ISM/Conference Board workaround** before designing the activity branch. Options:
  live without survey diffusion indices; substitute the regional Fed surveys (Philly MBOS is free
  and confirmed working, Empire/Dallas/Richmond not tested); or buy a licence.
- **Decide branch depth per report** — the Brazil reports grew tab by tab over months. Worth
  deciding up front which of the eight branches get a full HTML report and which are only
  ingestion for the oráculo.
- ~~Fix or retire `connectors/not_in_production/bls.py`~~ — **done 2026-08-18**: rewritten as
  `connectors/bls.py`, old stub removed. Still open: whether `connectors/fred.py` gets rewritten into
  the class-based connector pattern before the US ETL is built on top of it, and whether to register
  a free `BLS_API_KEY` (raises the caps from 25 series / 10 years / 25 queries per day to
  50 / 20 / 500 and enables `catalog`/`calculations`).
- **Rolling-window licensing on FRED is a real design constraint, not a footnote** — corporate
  spreads start 2023-08, S&P 500 and Dow start 2016-08, NAR existing home sales has **13 monthly
  observations**. Any report tab built on those needs either a different source or an explicit
  short-history design. Full detail in the branch files.
- **US release calendar** — the Brazil side has `domain/release_calendar/` fed by the BCB's ICS
  feeds. The US equivalents (BLS schedule, BEA schedule, Census economic-indicator calendar, FOMC
  calendar) were **not probed in this round**; whether they are machine-readable is unverified.
