# US activity — source mapping (BEA / Census / Fed Board / regional Feds)

Surveyed live on 2026-08-17 against each source's API, not just its documentation — same method as
[`analytics/brasil/labor_market/fontes_dados.md`](../analytics/brasil/labor_market/fontes_dados.md). Access status
for every source, and the two API keys we still need, are in [`README.md`](README.md); this file
covers only what the activity branch needs. Brazil counterpart:
[`analytics/brasil/economic_activity/CLAUDE.md`](../analytics/brasil/economic_activity/CLAUDE.md).

**Nothing in this branch is in the database.** Every row below is `❌` on "In DB/ETL" except where
noted; the seven series already used ad hoc by `analytics/oraculo/us/term_us.py` are flagged
`(oráculo)` — they are read straight from FRED into a CSV, never persisted.

## Coverage table

| Data | Primary source | On FRED | Agency direct | Format | In DB | Comment |
|---|---|---|---|---|---|---|
| Real GDP, level and growth (SAAR, YoY) | **BEA** (NIPA T1.1.x) | ✅ `GDPC1`, `GDP`, `A191RL1Q225SBEA`, `A191RO1Q156NBEA` | 🔑 BEA API key needed | FRED / BEA JSON | ❌ (oráculo uses the two growth series) | FRED carries the headline aggregates; the **full 20+ line NIPA decomposition by category needs the BEA key**. This is the one place where the Brazil report's growth-contribution table has no FRED shortcut |
| GDP expenditure components (real) | **BEA** | ✅ `PCECC96`, `GPDIC1`, `PNFI`, `PRFIC1`, `GCEC1`, `CBIC1`, `FINSLC1`, `EXPGSC1`, `IMPGSC1` | 🔑 BEA | FRED | ❌ | Enough for a top-level decomposition. Contribution-to-growth series (BEA's own `DPCERY2Q224SBEA` family) not inventoried this round |
| Potential GDP / output gap | **CBO** | ✅ `GDPPOT` (1949-01 → **2036-10**, projections included) | ❌ CBO site 403s | FRED | ❌ | FRED is the *only* working path — CBO's own xlsx is bot-blocked. Note the series extends 10 years into the future; a naive "last observation" read gets a 2036 forecast |
| Industrial production and capacity utilisation | **Fed Board** (G.17) | ✅ `INDPRO` (1919-01→), `IPMAN`, `IPBUSEQ`, `IPCONGD`, `IPMINE`, `TCU`, `MCUMFN` | ✅ DDP (needs series hash) | FRED / DDP CSV | ❌ (oráculo uses `INDPRO`) | The direct analogue of `atv_pim`. FRED's selection is thin on the ~300 industry-level indices the G.17 actually publishes — those need the DDP |
| Retail sales | **Census** (MARTS/MRTS) | ✅ `RSAFS`, `RSXFS`, `RRSFS` (real), `MRTSSM44000USS` | 🔑 Census key needed | FRED / Census API | ❌ (oráculo uses `RSAFS`) | Direct analogue of `atv_pmc`. **Sales by retail subsector (the interesting cut) needs the Census key** |
| Manufacturers' orders, shipments, inventories | **Census** (M3) | ✅ `DGORDER`, `NEWORDER` (core capital goods), `AMTMNO`, `AMTMTI`, `AMTMUO` | 🔑 Census | FRED | ❌ | `NEWORDER` (nondefense capital goods ex-aircraft) is the standard capex proxy |
| Business inventories and I/S ratio | **Census** (MTIS) | ✅ `BUSINV`, `ISRATIO`, `TOTBUSSMSA` | 🔑 Census | FRED | ❌ | |
| Construction spending | **Census** | ✅ `TTLCONS`, `PRRESCONS`, `TLRESCONS` | 🔑 Census | FRED | ❌ | Residential detail also appears in [`housing_fontes_dados.md`](housing_fontes_dados.md) |
| Personal income, saving rate, real spending | **BEA** | ✅ `PI`, `DSPIC96`, `PSAVERT`, `W875RX1`, `A229RX0`, `PCEC96`, `PCEDG`, `PCEND`, `PCES` | 🔑 BEA | FRED | ❌ | `W875RX1` (real income ex-transfers) is one of the NBER recession-dating series |
| Motor vehicle sales | **BEA** (supplemental) | ✅ `TOTALSA`, `ALTSALES`, `DAUTOSAAR` | 🔑 BEA | FRED | ❌ | Monthly, SAAR, back to 1976 |
| Consumer sentiment | **U. Michigan** | ⚠️ `UMCSENT` — **2 months stale** (last obs 2026-06 on 2026-08-17) | ⚠️ direct path unresolved | FRED | ❌ | See Gotchas. `CSCICP03USM665S` (OECD's composite) **died 2024-01**; use `USACSCICP02STSAM` instead (live to 2026-06) |
| **Consumer confidence (Conference Board)** | Conference Board | ❌ **absent** | ❌ licensed | — | ❌ | `CONCCONF` does not exist; zero FRED search results. Not obtainable without a licence |
| **ISM manufacturing / services PMI** | ISM | ❌ **absent** | ❌ licensed | — | ❌ | `NAPM`, `NAPMPI`, `NAPMNOI`, `NMFBAI` all return `"The series does not exist"`; searches for "ISM Manufacturing PMI"/"ISM Services" return **zero results**; `ismworld.org` serves a captcha. **The single biggest hole in this branch** — see Gotchas |
| Regional Fed manufacturing surveys | **Philly Fed** (MBOS) and peers | — | ✅ MBOS csv/xls confirmed | csv | ❌ | The free substitute for ISM. Only Philly was tested; Empire (NY), Dallas, Richmond, KC not probed |
| Coincident / national activity indices | **Chicago Fed**, **Philly Fed** | ✅ `CFNAI`, `CFNAIDIFF`, `USPHCI` | ✅ | FRED | ❌ | `USSLIND` (leading index) **stopped 2020-02** — dead, don't use |
| ADS business conditions index | **Philly Fed** | ❌ `ADSI` does not exist | ✅ xlsx confirmed | xlsx | ❌ | Daily-frequency real activity index; only reachable from the Philly Fed directly |
| GDP nowcast | **Atlanta Fed** (GDPNow) | ✅ `GDPNOW` (2011-07 → 2026-07) | ✅ xlsx confirmed (10.9 MB) | FRED / xlsx | ❌ | FRED has the headline; the xlsx has the subcomponent tracking |
| Weekly activity index | **NY Fed** | ✅ `WEI` (weekly, to 2026-08-08) | ✅ | FRED | ❌ | Highest-frequency broad activity read available free |
| Trade balance and current account | **Census/BEA** | ✅ `BOPGSTB`, `IEABC`, `NETFI` | 🔑 both | FRED | ❌ | Detail lives in [`external_sector_fontes_dados.md`](external_sector_fontes_dados.md) |

🔑 = the direct path needs an API key we do not have yet (free registration; see README).

## Verified series inventory

66 activity candidates checked, **60 exist**. All 6 failures are genuine absences, not wrong ids:
`NAPM`, `NAPMPI`, `NAPMNOI`, `NMFBAI` (ISM), `CONCCONF` (Conference Board), `ADSI` (Philly ADS).

Frequency mix as measured: mostly quarterly (BEA NIPA) and monthly, plus 1 weekly (`WEI`) and the
two CBO projection series. Longest history: `INDPRO` and `IPMINE` at **1919-01**.

Publishing releases behind this branch's 60 series: Gross Domestic Product/NIPA (15), Personal Income
and Outlays (9), G.17 Industrial Production and Capacity Utilization (7), M3 Manufacturers'
Shipments/Inventories/Orders (5), Manufacturing and Trade Inventories and Sales (3), Supplemental
Estimates Motor Vehicles (3), Advance Monthly Retail Sales (2), Surveys of Consumers (2), OECD Main
Economic Indicators (2), plus the single-series nowcast/index releases (GDPNow, WEI, CFNAI, coincident
and leading indexes, construction spending, trade, CBO).

## Gotchas found live

- **ISM is unavailable, and this is structural.** FRED removed the ISM series years ago over
  licensing and there is no free redistributor. Every US activity dashboard convention leans on
  ISM manufacturing and services PMI as the headline forward-looking indicator, so **the activity
  branch has to be designed around its absence** rather than patched later. The free substitutes
  are the regional Fed manufacturing surveys (Philly MBOS confirmed reachable; a composite of
  several regional surveys is the usual proxy) and `CFNAI`, which is a coincident diffusion index
  rather than a survey.
- **`GDPPOT` and `NROU` contain forecasts to 2036-10.** They are CBO projections, not history.
  Reading "the last observation" gives a 2036 value. Any output-gap calculation must slice to the
  last *actual* GDP date, and any chart must mark where history ends.
- **`USSLIND` (Leading Index for the United States) ends 2020-02** and `CSCICP03USM665S` (OECD
  composite consumer confidence) **ends 2024-01**. Both look alive in a series list and are dead in
  the data. `NETEXC96` (real net exports) is flagged DISCONTINUED and ends **2017-04** — use
  `EXPGSC1 − IMPGSC1` instead. This is the same "check the data, not the metadata" rule the Brazil
  fiscal survey learned from the Tesouro's `dataInicialSerie`.
- **Michigan sentiment on FRED is ~2 months behind the real release.** `UMCSENT` and `MICH` both
  ended 2026-06 when probed on 2026-08-17, while the survey itself publishes twice a month. The
  University of Michigan's own download path could not be resolved (`fetchdoc.php?docid=…` returns
  "Sorry, I can't find the file" for every id tried, and the data-archive page exposes no file
  links). If sentiment needs to be current, this needs solving separately.
- **Atlanta Fed URLs must use the long `/-/media/Project/Atlanta/FRBA/Documents/…` form.** The
  shorter `/-/media/documents/…` path returns **HTTP 200 with a 48,302-byte HTML page** — a
  soft-404. Three different Atlanta Fed files returned byte-identical lengths on the wrong path,
  which is what gave it away. Always check content, never status code.
- **`RSAFS` is the *advance* estimate and `MRTSSM44000USS` is the revised one** — they are different
  series with different last dates (2026-07 vs. 2026-06 when probed). Mixing them in one chart
  splices a first estimate onto revised history.
- **SAAR vs. SA is not cosmetic here.** FRED reports 20 of these series as `SAAR` (annualised) and
  the rest as plain `SA`. `TTLCONS` is SAAR while `BUSINV` is SA, both monthly, both in dollars —
  a level comparison between them is off by a factor of 12 unless normalised.

## Open items

- **Get the BEA API key.** Everything the Brazil PIB tab does (growth decomposition, contribution
  by category, current-price weights) needs NIPA at table granularity, which FRED's curated
  selection does not provide.
- **Get the Census API key** for retail by subsector, orders detail, and construction by category.
- **Decide the ISM substitute** and whether the regional Fed surveys are worth ingesting as a set
  (only Philly tested — the other four need probing).
- **Not inventoried this round**: BEA's contribution-to-growth series family, the G.17's
  industry-level indices, GDP by industry, and the state-level coincident indices.
