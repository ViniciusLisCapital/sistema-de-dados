# US labor market — source mapping (BLS / DOL / ADP / regional Feds)

Surveyed live on 2026-08-17 against each source's API, not just its documentation — same method as
[`analytics/brasil/labor_market/fontes_dados.md`](../analytics/brasil/labor_market/fontes_dados.md), which is also
the Brazil counterpart of this branch. Cross-cutting access status and the outstanding API keys are
in [`README.md`](README.md).

This is the branch where the US is **best** served relative to Brazil: one agency (BLS) owns almost
everything, its API works without a key, and its flat-file archive exposes the complete series
catalog — no scraping, no xlsx parsing, no FTP microdata like the Novo CAGED. **Nothing is in the
database yet**; three series are read ad hoc by `analytics/oraculo/us/term_us.py`, marked `(oráculo)`.

## The three-source structure

Brazil splits labor between a household survey (PNAD, IBGE) and an administrative register (CAGED,
MTE) that **cannot share a chart** — different universes, different units. The US has the same split
and it needs the same discipline:

- **CPS** (Current Population Survey, BLS) — household survey. Unemployment rate, participation,
  employment-population ratio, duration, demographics. The PNAD analogue.
- **CES** (Current Employment Statistics, BLS) — establishment survey. Payrolls, hours, earnings by
  industry. Closest to CAGED in spirit but it is a *survey of firms*, not a register, and it reports
  a **level** (158.9M nonfarm employees) whose monthly difference is the "payrolls" headline.
- **JOLTS** (Job Openings and Labor Turnover Survey, BLS) — flows: openings, hires, quits, layoffs.
  Genuinely a third universe, in people/month; the direct CAGED-flow analogue.

CPS and CES disagree on employment by millions of people every month by construction (household vs.
establishment concept). Same non-comparability note the Brazil report carries in its Apêndice.

## Coverage table

| Data | Primary source | On FRED | Agency direct | Format | In DB | Comment |
|---|---|---|---|---|---|---|
| Unemployment rate (headline, U-6) | **BLS/CPS** | ✅ `UNRATE` (1948-01→), `U6RATE` (1994-01→), `UNRATENSA` | ✅ BLS API + `ln` flat file | FRED / JSON | ❌ (oráculo) | `LNU04000000` does **not** exist on FRED — the NSA rate is `UNRATENSA` |
| Participation and employment-population ratio | **BLS/CPS** | ✅ `CIVPART`, `EMRATIO`, `LNS11300060` (prime-age 25-54), `LNS12300060` | ✅ | FRED | ❌ | Prime-age participation is the standard slack read |
| Unemployment by demographics | **BLS/CPS** | ✅ `LNS14000003` (White), `LNS14000006` (Black), `LNS14000009` (Hispanic), `LNS14032183` (Asian), `LNS14027662` (BA+) | ✅ | FRED | ❌ | The direct analogue of `mt_pnad_trimestral`'s cuts. FRED carries a handful; the **full demographic cross-tabs need the `ln` flat file** (15.3 MB catalog) |
| Duration and composition of unemployment | **BLS/CPS** | ✅ `UEMPMED`, `UEMPLT5`, `UEMP27OV`, `LNS13023621` (job losers), `LNS12032194` (part-time economic reasons), `LNS15000000` (not in labor force) | ✅ | FRED | ❌ | |
| Nonfarm payrolls, total and by sector | **BLS/CES** | ✅ `PAYEMS` (1939-01→), `USPRIV`, `MANEMP`, `USCONS`, `USGOVT`, `CES9091000001` (federal), `USTPU`, `USFIRE`, `USEHS`, `USLAH` | ✅ BLS API + `ce` flat file (3.94 MB) | FRED | ❌ (oráculo uses `PAYEMS`) | 10 sectors verified; CES publishes hundreds of industry levels — the flat file is the path to the full tree |
| Hours and earnings | **BLS/CES** | ✅ `AWHAETP`, `AWHMAN`, `CES0500000003` (AHE all employees), `AHETPI` (production workers, **1964-01→**), `AWHI`, `AWHAE`, `CES0500000017` | ✅ | FRED | ❌ (oráculo uses `CES0500000003`) | `CES0500000003` only starts **2006-03**; `AHETPI` is the long series. `CES0500000002`/`CES0500000008` do **not** exist on FRED (my initial guesses) |
| Weekly initial and continuing claims | **DOL/ETA** | ✅ `ICSA`, `IC4WSA`, `CCSA`, `ICNSA` — all live to 2026-08 | not probed | FRED | ❌ | Highest-frequency labor read; weekly, back to 1967 |
| Job openings, hires, quits, layoffs | **BLS/JOLTS** | ✅ `JTSJOL`, `JTSHIR`, `JTSQUR`, `JTSLDR`, `JTSTSR`, `JTSJOR`, `JTSQUL`, `JTSLDL` | ✅ bulk file `jt.data.1.AllItems` (the route actually used) | TSV / BLS v2 | ✅ **`macro_us.mt_jolts` + `mt_jolts_dim`, 2026-09-01** — 913 series, 3 cuts, 2000-12 → today; report in `analytics/us/labor_market/` | **BLS API v1 does not serve JOLTS** — confirmed live: `"Series does not exist for Series JTSJOL"`. Rate levels and rate ratios are separate series (`JTSJOL` = level in thousands, `JTSJOR` = rate) |
| Employment Cost Index | **BLS/ECI** | ✅ `ECIALLCIV`, `ECIWAG` (both 2001-01→, quarterly) | ✅ `ci` flat file | FRED | ❌ | The cleanest compensation measure (fixed occupation weights). `CIU1010000000000A` does not exist on FRED |
| Productivity and unit labor costs | **BLS** | ✅ `OPHNFB`, `ULCNFB`, `HOANBS` (all 1947-01→, quarterly) | ✅ `pr` flat file | FRED | ❌ | |
| Wage growth tracker (median, matched workers) | **Atlanta Fed** | ✅ `FRBATLWGT3MMAUMHWGO` and ~6 siblings (unweighted/weighted × 3m/12m MA, plus distribution cuts) | ✅ xlsx confirmed | FRED / xlsx | ❌ | Controls for composition, unlike AHE. **The 12-month unweighted id is not `FRBATLWGT12MMAUMHWGO`** (does not exist) — the weighted one is `FRBATLWGT12MMAWMHWGO` |
| Private payrolls, independent estimate | **ADP** | ✅ `ADPMNUSNERSA` (monthly), `ADPWNUSNERSA` (**weekly**, 2010-01→) | not probed | FRED | ❌ | Free on FRED despite being a private product. The weekly series is unusual and useful |
| Sahm rule recession indicator | **Fed/derived** | ✅ `SAHMREALTIME` (1959-12→), `SAHMCURRENT` (1949-03→) | — | FRED | ❌ | Two variants: real-time (uses vintage data) vs. current (revised). Don't mix |
| Natural rate of unemployment | **CBO** | ✅ `NROU` (to **2036-10**) | ❌ CBO 403s | FRED | ❌ | Projections included — same forecast-in-the-series trap as `GDPPOT` |
| **State/metro detail** | BLS (LAUS) | partially | ✅ | — | ❌ | Not inventoried this round. The `ln`/`sm` flat files carry it |

## Verified series inventory

59 labor candidates checked, **54 exist**. All 5 failures are my own guessed ids rather than real
gaps — every concept has a series, just under a different name: `LNU04000000` (→ `UNRATENSA`),
`CES0500000002` and `CES0500000008` (→ `AHETPI`), `CIU1010000000000A` (→ `ECIALLCIV`),
`FRBATLWGT12MMAUMHWGO` (→ `FRBATLWGT3MMAUMHWGO` or `FRBATLWGT12MMAWMHWGO`). This branch has **no
genuine coverage gap on FRED** — the only US branch of the eight where that is true.

Measured windows: 28 series from the Employment Situation release (CPS+CES), 8 JOLTS, 4 weekly
claims, 3 Productivity and Costs, 2 ECI, 2 ADP, 2 Sahm. Longest: `PAYEMS`, `MANEMP`, `USCONS`,
`AWHMAN` at **1939-01**. Latest data as probed: monthly series through **2026-07**, JOLTS through
**2026-06** (one month more lag, as expected), claims through **2026-08-08**.

## Gotchas found live

- **BLS API v1 cannot replace v2.** v1 needs no key and returned CPI and CES fine, but JOLTS came
  back `"Series does not exist"`. If we want a key-free path, it has to be v1 *plus* something else
  for JOLTS — or just use unregistered v2, which **does** work (confirmed: a no-key v2 request
  returned CPI data) at 25 series / 10 years / 25 queries per day.
- **The BLS key hardcoded in the old `not_in_production/bls.py` was dead** — live response:
  `"The key:8c7fe923715143688e37c1c2b069a38d provided by the User is invalid"`. Resolved 2026-08-18:
  that stub is gone, replaced by [`connectors/bls.py`](../connectors/bls.py), which reads
  `BLS_API_KEY` from `.env` and works unregistered when it is absent. Registering a free key is still
  worth doing (caps go to 50 series / 20 years / 500 queries per day). Note that this branch's series
  come through the same connector as the inflation branch — `ce` (CES), `ln` (CPS) and `jt` (JOLTS)
  answer the same call as `cu`, confirmed live in one request covering five surveys.
- **`download.bls.gov` returns 403 to a browser User-Agent and 200 to an identifying one.** BLS
  policy requires the UA to identify the requester; `LISCapital-macro-pipeline/1.0
  (fabian@liscapital.com.br)` worked on all seven catalogs tried. This is the only path to the
  complete series lists — worth building into the connector from the start, because guessing BLS
  series ids is exactly how six of my candidates failed above.
- **JOLTS level vs. rate are different series and both are named "Total Nonfarm".** `JTSJOL` is
  7,359 (thousands of openings) and `JTSJOR` is 4.4 (percent). `JTSQUL`/`JTSQUR` and
  `JTSLDL`/`JTSLDR` pair the same way. Plotting a level and a rate on one axis is the same failure
  mode the Brazil CAGED tab avoids by keeping stock and flow apart.
- **`CES0500000003` (average hourly earnings, all employees) starts 2006-03**, not 1964. The long
  series is `AHETPI` (production and nonsupervisory workers only, 1964-01→) — a different universe,
  not an extension. `analytics/oraculo/us/term_us.py` currently uses `CES0500000003` from
  `InicialDate`, so its earnings score silently has no pre-2006 history.
- **`NROU` carries CBO projections to 2036-10.** Same trap as `GDPPOT` in the activity branch: a
  "current natural rate" read off the last observation returns a forecast a decade out.
- **CPS and CES will not reconcile, ever** — household vs. establishment concept, different
  treatment of multiple jobholders, agriculture and the self-employed. Design the report so no chart
  invites the comparison, the way the Brazil report separates the PNAD tabs from Emprego Formal.

## Open items

- **Decide the BLS access strategy**: unregistered v2 (works, tight caps), a fresh registered key
  (free, 20× the caps), or flat files (no caps at all, but bulk text parsing). Probably flat files
  for backfill plus the API for the monthly increment — the same shape as the Novo CAGED pipeline.
- **Not inventoried this round**: full CPS demographic cross-tabs, CES industry tree below the 10
  sectors, state/metro (LAUS), union membership, job flows (BED), and the Atlanta Fed tracker's
  distribution cuts.
- **No derived metric proposed** — same scope discipline as the Brazil round: visualise first, then
  decide about Okun, Beveridge curve, Sahm decomposition or a wage-Phillips fit.

## JOLTS is loaded (2026-09-01) — what the live work added to the notes above

The inventory above was built from FRED. The branch was actually loaded from the **bulk file**
instead, and the reason is a measurement: the 913 useful series are 19 API requests per 20-year
window against **one** 34 MB request that brings the whole history in 1.6 s and spends no quota.
The API stayed in the pipeline as an independent vintage check — ten headline series over two
years, any disagreement raises rather than writing a stale month.

Six things the FRED inventory could not have told us, all measured against the source:

- **`JTSJOL` and its siblings are one cell of a cube JOLTS does not publish.** Each axis exists
  only at the total of the others: industry (28 codes, 4 additive levels) at the national total,
  establishment size (6 classes) **at Total private only**, region (4) at Total nonfarm only. The
  size-class root is therefore 810 thousand openings smaller than the industry root — the release
  says so in a table footnote, and a tree that ignored it would fail to close by ~11%.
- **State estimates are dead.** All 51 series (plus DC) stop at **2025-M12**; the catalogue still
  lists them. Excluded from the load on purpose.
- **One measure is a stock and five are flows.** Job openings is the position on the last business
  day; hires and the four separation types are counts over the whole month. Summing 12 months of
  openings gives 12.0× the level and still looks like a plausible openings chart.
- **The rate denominators differ between measures, and it is checkable.** Implied employment from
  `hires level / (hires rate/100)` reproduces the openings rate as `openings/(employment+openings)`
  to 0.038 p.p. mean absolute error over 8,624 cells, against 0.150 p.p. for `openings/employment`.
  So "openings rate minus hires rate" is not a quantity — the two do not share a base.
- **The one data gap is not in JOLTS.** Openings, hires and separations are complete over the whole
  history. The only blank in the files is the *unemployed per opening* ratio in **October 2025**
  (the appropriations lapse) — its denominator is the household survey, which stopped; JOLTS
  collection did not. Same missing month as `inflc_cpi`.
- **API v1 vs v2 is moot now.** The bulk file needs no key at all; only the vintage check touches
  v2. The v1 finding above still stands and is still the reason not to plan around v1.

**Release timing**, from the live BLS schedule page and cross-checked against FRED release 192
(the two agree exactly on the 8 dates of 2026 both cover): monthly, **10:00 ET** (not 08:30 like
the CPI), and with **one extra month of lag** — the 2026-09-01 release delivers July, while the
CPI release of 2026-09-11 delivers August. In the calendar as group `bls_jolts`.

## CES and CPS are loaded too (2026-09-01, same day) — and so are the derived metrics

`mt_ces` (3.3 M rows over 12,000 series, 1939→) + `mt_ces_dim` (the 839-industry tree) and
`mt_cps` (43 headline concepts, 1948→). Vacancies-per-unemployed, net hiring, the Beveridge
curve and the CES×CPS divergence now live in their own tab, which is what the JOLTS round was
waiting for. What the live work added to the notes above:

- **The CES has no `AllItems` file.** It is 30 files partitioned by supersector × measure family
  (78 MB for the employment ones alone). The choice rule is now explicit for this branch: the
  flat file when series count in the hundreds, the API when they count in dozens — which is why
  the CPS comes through the API (43 concepts, 8 requests against a 500/day quota) and the CES
  through the files.
- **The CES `series_id` is 13 chars and the adjustment is the PREFIX** (`CES` adjusted, `CEU`
  raw), like `CUSR`/`CUUR` and `JTS`/`JTU`. There is no separate field.
- **The CPS SA/NSA pair is not a prefix swap**: the 2-digit field changes with it
  (`LNS11`→`LNU01`, `LNS13`→`LNU03`). Derived ids must be verified against the catalogue.
- **`CES0500000002`/`CES0500000008` missing from FRED** (note above) stopped mattering: both come
  from the CES flat files, and `mt_ces` loads all 13 measures straight from the source.
- **Three CPS series read right and mean something else**, found by checking each concept against
  the printed release: the noneconomic part-time line is the *at work 1-34 hours* series (22,770
  against 22,345), "15 to 26 weeks" is not the one named "15 weeks & over" (1,157 against 2,929),
  and marginally attached has an adjusted version which is the one the summary table prints.
- **The CES tree cannot be derived from the indentation, and additivity only holds in the raw
  data** — the hard part of this branch is documented in
  `domain/db/us/labor_market/mt_ces_dim.py`.
- **The Employment Situation is in the calendar as group `bls_empsit`**, first Friday, 08:30 ET,
  one month ahead of JOLTS for the same reference month.

Still open: weekly claims (would be the first non-monthly grid in this area), ECI, productivity,
the CES production/non-supervisory tables (B-6 to B-9, whose earnings series starts 1964 against
2006 for all employees) and the full CPS demographic cross-tabs.
