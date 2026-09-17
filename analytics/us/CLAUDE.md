# analytics/us/ — the US branch

Country-level notes for the US side: what each macro area's sources are, how we reach them, and
what is already loaded. **Each area keeps its own `fontes_dados.md` in its own folder**, the same
way `analytics/brasil/` does — this file holds only what is common to all eight, plus the raw
probe output they were all written from.

## Where things stand (2026-09-10)

| built | area | tables in `macro_us` | report |
|---|---|---|---|
| ✅ | [inflation](inflation/) | `inflc_cpi`, `inflc_cpi_dim`, `inflc_cpi_pesos`, `inflc_pce`, `inflc_pce_dim` | `reports/us/Inflation.html` |
| ✅ | [labor market](labor_market/) | `mt_ces`, `mt_ces_dim`, `mt_cps`, `mt_jolts`, `mt_jolts_dim`, `mt_produtividade` | `reports/us/Labor Market.html` |
| partial | [monetary policy](monetary_policy/) | `us_interest_rate` — Treasury curve (11 tenors) + the Fed target, loaded 2026-09-03 | — |
| — | [activity](economic_activity/) · [credit](credit/) · [external sector](external_sector/) · [fiscal](fiscal_policy/) · [housing](housing/) | — | — |

The ETL for the built areas is in `domain/db/us/<area>/`, mirroring `domain/db/brasil/`; the schema
layout and every table's detail is in [`domain/db/CLAUDE.md`](../../domain/db/CLAUDE.md).

**This folder was `us_project/` at the repo root until 2026-09-10.** It held a single scoping round
that surveyed all eight areas at once, on 2026-08-17/18, before anything was built — which is why
the US has eight `fontes_dados.md` and Brazil only three (Brazil grew area by area and wrote the
survey only where the source was tangled enough to need one). The practical consequence for anyone
reading: **these notes were written before the build, so a claim in one can be older than the
code.** The two built areas' files were updated as they were built; the other six are still as
surveyed, and the database column in them still reads empty because it was.

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

## What each area covers

| Area | Brazil counterpart | Scope |
|---|---|---|
| [economic_activity](economic_activity/fontes_dados.md) | `analytics/brasil/economic_activity/` | GDP/NIPA, industrial production, retail, orders, inventories, income, sentiment, nowcasts |
| [labor_market](labor_market/fontes_dados.md) | `analytics/brasil/labor_market/` | CPS, CES, JOLTS, claims, ECI, productivity, wage trackers |
| [inflation](inflation/fontes_dados.md) | `analytics/brasil/inflation/` | CPI, PCE, PPI, import/export prices, cores/trimmed means, expectations |
| ↳ [`inflation_hierarchy.md`](inflation/inflation_hierarchy.md) | — | **How the inflation data nests** (2026-08-18): the CPI's **two** trees — the 294-item / 9-level expenditure structure and the 37-row news-release structure (food / energy / core goods / core services) — both with weights and series ids and both validated against the weight identities; why every other US price measure is flat or nests differently; proposed `macro_us` tables |
| ↳ [`cpi_item_hierarchy.tsv`](inflation/cpi_item_hierarchy.tsv) · [`cpi_newsrelease_table1.tsv`](inflation/cpi_newsrelease_table1.tsv) | — | Machine-readable form of those two trees — level, parent, CPI-U/CPI-W weights, SA and NSA series ids, coverage window. Seed for `inflc_cpi_dim` |
| [monetary_policy](monetary_policy/fontes_dados.md) | `analytics/brasil/monetary_policy/` | Fed target/effective rates, yield curve, balance sheet, money, financial conditions, SEP |
| [fiscal_policy](fiscal_policy/fontes_dados.md) | `analytics/brasil/fiscal_policy/` | MTS receipts/outlays, debt stock and holders, NIPA government accounts, CBO |
| [credit](credit/fontes_dados.md) | `analytics/brasil/credit/` | H.8 bank credit, SLOOS, G.19 consumer credit, delinquencies, Z.1 debt, FDIC |
| [external_sector](external_sector/fontes_dados.md) | `analytics/brasil/exchange_rate/` | Dollar indices, trade, current account, IIP, TIC, reserves |
| [housing](housing/fontes_dados.md) | *(none)* | Starts/permits/sales, prices, mortgage rates, vacancy, residential construction |

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
| **BEA API** | UserID required | ✅ working **since 2026-08-26** | The key arrived and is in the `.env` (`BEA_API_KEY`); `connectors/bea.py` uses it. Was blocked at survey time — empty and invalid keys both return `APIErrorCode 1` |
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

`macro_us` exists and holds **12 tables** (5 inflation, 6 labor market, 1 rates) — see the table at
the top of this file for which, and [`domain/db/CLAUDE.md`](../../domain/db/CLAUDE.md) for each
one's range, key and gotchas. It was still an empty reservation when this survey was written.

US data **outside** `macro_us` lives in `macro_international`, always because some Brazil-facing
series needed it first (verified live 2026-08-17):

| Table | US content | Range | Rows |
|---|---|---|---|
| `diferenciais_juros` | `fed_funds`, `cpi_12m_us`, `real_us_ex_post` (alongside the BR side and the differentials) | 1995-01 → 2026-08 | 2,825 |
| `cmb_dollar_index` | `dxy` (Yahoo Finance ICE index) | 1971-01 → 2026-08 | 14,114 |
| `cmb_dollar_index_em` | FRED `DTWEXEMEGS` | — | — |
| `cmb_equity_us` | `sp500` — **not documented in any `CLAUDE.md`**, found by inspecting the live schema | 1990-01 → 2026-08 | 9,214 |
| `comm_brent` | `brent_usd` (FRED `DCOILBRENTEU`) | 1990-01 → 2026-07 | 9,258 |
| `clima_oni` | Oceanic Niño Index (NOAA) | 1950-01 → 2026-04 | 306 |

Outside the database, `analytics/oraculo/us/term_us.py` still pulls **23 FRED series** ad hoc for
the macro thermometer and writes a CSV, never MySQL — it was the de facto US pipeline before
`macro_us` existed and is the natural first consumer of it now. See its pending item in
[`analytics/oraculo/CLAUDE.md`](../oraculo/CLAUDE.md).

**Connectors.** `connectors/bls.py` (2026-08-18) was the first US connector on the current
class-based conventions, and covers three access paths — API by series id, the raw
`download.bls.gov` flat files for backfill and dimensions, and the CPI relative-importance xlsx for
weights — serving every BLS survey (CPI, PPI, CES, CPS, JOLTS, import/export prices) through the
same call. `connectors/bea.py` followed once the key arrived (2026-08-26). `connectors/us_agenda.py`
covers the BLS and BEA **release schedules**, feeding `domain/release_calendar/update_us_calendar.py`
— the calendar item this survey left unverified. `connectors/fred.py` works but is still in the old
CamelCase-function style (`FredUniFrame`/`FredMultFrame`) rather than the class-based pattern of
`ibge.py`/`bcb.py`. Full behaviour and gotchas for all of them in
[`connectors/CLAUDE.md`](../../connectors/CLAUDE.md).

## Naming — what the survey proposed and what was actually decided

The prefix classifies *what the data is*, independent of schema (see
[`domain/db/CLAUDE.md`](../../domain/db/CLAUDE.md)). Seven of the eight areas simply reuse
`macro_brasil`'s prefixes — `atv_`, `mt_`, `inflc_`, `fisc_`, `cred_`, `cmb_`, `expc_` — and the
built tables follow that (`inflc_cpi`, `mt_jolts`, …).

Two prefixes had no Brazil precedent to reuse, and this file used to recommend inventing `mon_` for
rates/policy and `hous_` for housing. **The rates half was decided differently on 2026-09-03**: the
US yield curve landed as `us_interest_rate`, with a **country** prefix, because the same table
exists for three regions and the three names would collide in `domain/db/registry.py`
(`br_interest_rate`, `us_interest_rate`, `inter_interest_rate`). Housing has nothing built, so
`hous_` is still only a proposal.

**The daily-market-data scope question resolved itself the same way**: the US curve went to
`macro_us`, per the rule that `macro_international` is for what needs 2+ countries. By that rule
`cmb_equity_us` and `cmb_dollar_index` arguably sit in the wrong schema today — unchanged, and
still worth deciding.

## Open items

- **The Census API key** is the only free registration still missing (`api.census.gov/data/key_signup.html`).
  It buys retail, housing, orders and trade at product/geography detail. **BEA and BLS are done** —
  both keys are in the `.env` and both connectors are built.
- **Decide the ISM/Conference Board workaround** before designing the activity branch. Options:
  live without survey diffusion indices; substitute the regional Fed surveys (Philly MBOS is free
  and confirmed working, Empire/Dallas/Richmond not tested); or buy a licence.
- **Decide branch depth per area** — worth deciding up front which of the remaining six get a full
  HTML report and which are only ingestion for the oráculo. The two built so far both went the full
  report route.
- **`connectors/fred.py` is still in the old CamelCase-function style.** Whether it gets rewritten
  into the class-based connector pattern is still open; the US ETL was built on top of it as-is.
- **Rolling-window licensing on FRED is a real design constraint, not a footnote** — corporate
  spreads start 2023-08, S&P 500 and Dow start 2016-08, NAR existing home sales has **13 monthly
  observations**. Any report tab built on those needs either a different source or an explicit
  short-history design. Full detail in the area files.
- ~~US release calendar~~ — **done**: `connectors/us_agenda.py` reads the BLS and BEA schedules
  (dates *and* times), and `domain/release_calendar/update_us_calendar.py` writes them into the
  calendar. The Census economic-indicator and FOMC calendars were still not probed.
