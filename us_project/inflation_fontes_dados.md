# US inflation — source mapping (BLS / BEA / regional Feds / NY Fed)

Surveyed live on 2026-08-17 against each source's API, not just its documentation — same method as
[`analytics/labor_market/fontes_dados.md`](../analytics/labor_market/fontes_dados.md). Cross-cutting
access status and outstanding API keys: [`README.md`](README.md). Brazil counterpart:
[`analytics/inflation/CLAUDE.md`](../analytics/inflation/CLAUDE.md).

**Two headline indices, not one.** Brazil has the IPCA and everything anchors to it. The US has
**CPI** (BLS, the public/contractual index, released ~mid-month) and **PCE** (BEA, the Fed's actual
target, released ~end of month, different weights and scope). They differ persistently, not just
noisily — different weighting source (household survey vs. business surveys), different treatment of
health care and housing. Any US inflation report has to carry both and explain the wedge; a single
"inflation" line is a design error here.

**Nothing is in the database yet.** `macro_international.diferenciais_juros` holds `cpi_12m_us` as an
input to the BR-US real-rate differential — that is the only US inflation series persisted anywhere.
Five series are read ad hoc by `analytics/oraculo/us/term_us.py`, marked `(oráculo)`.

## Coverage table

| Data | Primary source | On FRED | Agency direct | Format | In DB | Comment |
|---|---|---|---|---|---|---|
| CPI headline and core | **BLS** | ✅ `CPIAUCSL` (SA, 1947-01→), `CPIAUCNS` (NSA, **1913-01→**), `CPILFESL` | ✅ API + `cu` flat file | FRED / JSON | ⚠️ `cpi_12m_us` only, in `macro_international` | |
| CPI major groups | **BLS** | ✅ `CPIUFDSL` (food), `CPIENGSL` (energy), `CPIHOSSL` (housing), `CPIMEDSL`/`CUSR0000SAM2` (medical), `CUSR0000SAH1` (shelter) | ✅ | FRED | ❌ | |
| CPI analytical cuts | **BLS** | ✅ `CUSR0000SASLE` (services less energy), `CUSR0000SACL1E` (core goods), `CUSR0000SETA01`/`02` (new/used vehicles), `CUSR0000SEHA` (rent), `CUSR0000SEHC` (OER) | ✅ | FRED | ❌ | Core services ex-shelter — the current policy focus — is **not a published series**; it has to be built from components, which needs the weights |
| **CPI weights and the full item tree** | **BLS** | ⚠️ FRED has indices, **not weights** | ✅ `cu` flat file (1.34 MB catalog) | flat file | ❌ | **This is the gap that matters.** The Brazil report's whole architecture (`inflc_decomposicao`, `inflc_dim`, contribution = variation × weight) needs relative importance per item. FRED does not carry it; the BLS flat files and the news-release tables do |
| PCE price index, headline and core | **BEA** | ✅ `PCEPI`, `PCEPILFE` (both 1959-01→), `BPCERO1Q156NBEA`, `BPCCRO1Q156NBEA` (quarterly YoY) | 🔑 BEA key needed | FRED | ❌ (oráculo uses both) | **The Fed's target index.** The monthly percent-change series I guessed (`DPCERG3M086SBEA`, `DPCCRG3M086SBEA`) do **not** exist — compute from the index |
| Trimmed-mean and median cores | **Dallas Fed**, **Cleveland Fed** | ✅ `PCETRIM12M159SFRBDAL`, `PCETRIM1M158SFRBDAL`, `MEDCPIM158SFRBCLE`, `TRMMEANCPIM158SFRBCLE`, `MEDCPIM094SFRBCLE` | ✅ | FRED | ❌ | The analogue of the BCB's núcleos. All live to 2026-06/07 |
| Sticky vs. flexible price CPI | **Atlanta Fed** | ✅ `STICKCPIM159SFRBATL`, `CORESTICKM159SFRBATL`, `FLEXCPIM159SFRBATL`, `CORESTICKM158SFRBATL` | ✅ xlsx confirmed | FRED / xlsx | ❌ (oráculo uses sticky + flexible) | Already in the oráculo. The `…159…` ids are YoY rates, `…158…` are indices — easy to mix up |
| PPI | **BLS** | ✅ `PPIACO` (**1913-01→**), `PPIFIS` (final demand, 2009-11→), `PPIFES` (core final demand), `PPIFID` (NSA), `WPSFD49207`, `WPSFD4131`, `WPSFD41312`, `WPUFD49207`, `PPIIDC` | ✅ `wp` flat file | FRED | ❌ (oráculo uses `PPIACO`) | The modern "final demand" family only starts **2009-11**; the long history is in the old "finished goods" family (`WPSFD49207`, 1947-04→). Not the same concept |
| Import and export prices | **BLS** | ✅ `IR` (imports, 1982-09→), `IQ` (exports, 1983-09→) | ✅ | FRED | ❌ | NSA only. `IREXFOODFEEDS` does not exist |
| Market-implied inflation expectations | **Fed Board/Treasury** | ✅ `T5YIE`, `T10YIE`, `T5YIFR` (all daily, 2003-01→) | ✅ Treasury TIPS curve csv | FRED | ❌ | The 5y5y forward is the standard anchoring read |
| Survey inflation expectations — households | **U. Michigan** | ⚠️ `MICH` — **2 months stale** (last obs 2026-06 on 2026-08-17) | ⚠️ direct path unresolved | FRED | ❌ (oráculo uses `MICH`) | See Gotchas |
| Survey inflation expectations — NY Fed SCE | **NY Fed** | ❌ not on FRED | ✅ xlsx confirmed (1.23 MB) | xlsx | ❌ | 1y/3y/5y median expectations plus dispersion. **Only reachable from the NY Fed directly** — and it is the better household series (rotating panel, quantitative) |
| Model-based expectations | **Cleveland Fed** | ✅ `EXPINF1YR`, `EXPINF10YR` (1982-01→, live to 2026-08) | ✅ | FRED | ❌ | Term structure of expected inflation; more current than Michigan |
| **Cleveland Fed inflation nowcast** | Cleveland Fed | ❌ zero search results | not probed | — | ❌ | The current-month CPI/PCE nowcast is not on FRED |
| GDP deflator | **BEA** | ✅ `GDPDEF`, `GDPCTPI` | 🔑 BEA | FRED | ❌ | |
| Energy and commodity inputs | **EIA** | ✅ `DCOILWTICO`, `DCOILBRENTEU`, `DHHNGSP`, `GASREGW` | ❌ EIA needs a key | FRED | ⚠️ `comm_brent` (from FRED) already in `macro_international` | FRED redistributes the four headline energy prices; anything deeper needs the EIA key |
| **Multivariate Core Trend** | NY Fed | ❌ not on FRED | ⚠️ url unresolved | — | ❌ | The NY Fed's own trend-inflation model. Its download path 404'd on both urls tried |

🔑 = the direct path needs an API key we do not have yet. ✅ under "On FRED" means verified live.

## Verified series inventory

49 inflation candidates checked, **45 exist**. All 4 failures are my own guessed ids:
`DPCERG3M086SBEA` and `DPCCRG3M086SBEA` (the real BEA percent-change series have different ids —
compute from the index instead), `WPUFD49104`, `IREXFOODFEEDS`. No genuine series gap, but see the
weights problem below, which is a gap in the *kind* of data FRED carries rather than in its coverage.

By release: Consumer Price Index (14 series — a 15th, owners' equivalent rent, is counted under
housing), Producer Price Index (6), Sticky Price CPI (4), Current Median CPI (3), Interest Rate
Spreads (3 breakevens), Personal Income and Outlays (2, the PCE indices), Trimmed Mean PCE (2),
Inflation Expectations (2, Cleveland's model-based series), Import and Export Price Indexes (2), Spot
Prices (2), Surveys of Consumers (1), plus the two GDP deflators.

Latest data as probed: CPI/PPI/sticky/median through **2026-07**, PCE and trimmed-mean PCE through
**2026-06**, breakevens through **2026-08-14**, Cleveland expectations through **2026-08**.

## Gotchas found live

- **The weights problem is the architectural decision for this branch.** The Brazil inflation report
  is built on subitem-level variation *and* relative importance, which lets it compute contributions
  and rebuild any aggregate (`inflc_decomposicao` + `inflc_dim`). FRED gives us the CPI indices but
  **not** the relative-importance vector, so "contribution of shelter to July CPI" is not derivable
  from FRED alone. Getting it means the BLS flat files or the news-release tables. **Decide this
  before designing the report**, because it determines whether the US report can have a
  decomposition/waterfall tab at all or is limited to index and YoY charts.
- **PPI has two incompatible families and both look like "PPI".** The modern *final demand* series
  (`PPIFIS`, `PPIFES`, `PPIFID`) start **2009-11**/2010-04. The long history is the legacy *finished
  goods* family (`WPSFD49207`, 1947-04→; `PPIACO`, 1913-01→). Splicing them makes a chart that reads
  as one series and is two. The oráculo currently uses `PPIACO` (all commodities), which is the
  longest but also the least like a core measure.
- **`…159…` vs `…158…` suffixes on the Atlanta/Cleveland Fed series.** `STICKCPIM159SFRBATL` is a
  1-year percent change; `CORESTICKM158SFRBATL` is an index. Both are "Sticky Price CPI". The oráculo
  uses the `159` (rate) variants, correctly — but a new consumer picking ids by name will get this
  wrong, and there is no unit hint in the id.
- **Michigan inflation expectations on FRED lag ~2 months** (`MICH` ended 2026-06 when probed on
  2026-08-17), and the University of Michigan's own file path could not be resolved. If a current
  household expectation reading matters, the **NY Fed SCE xlsx** is the better answer: it downloaded
  cleanly (1.23 MB, verified xlsx by magic bytes) and is a quantitative rotating panel rather than
  Michigan's qualitative-anchored question.
- **CPI vs. PCE is not a rounding difference.** Different weights, different scope (PCE covers
  employer-paid health care, CPI does not), different formula treatment. Both must be present and the
  wedge stated, the same way the Brazil fiscal report has to state GFSM-vs-RTN rather than reconcile
  them.
- **`CPIAUCNS` reaches 1913 and `CPIAUCSL` only 1947.** The seasonal adjustment, not the data, is
  what starts in 1947 — worth knowing before promising a "century of US inflation" chart with an SA
  series.

## Open items

- **Resolve the CPI weights source** (BLS flat files vs. news-release tables) — the one decision this
  branch is blocked on for anything beyond index/YoY charts.
- **Get the BEA key** for PCE at NIPA table granularity (component price indices, contributions).
- **Ingest the NY Fed SCE** — no FRED path exists and it is the best household expectation series.
- **Not inventoried this round**: CPI-W and C-CPI-U, regional/metro CPI, the full PPI industry tree,
  PCE component price indices, the Cleveland nowcast, the NY Fed MCT (url unresolved), and the Dallas
  Fed's own trimmed-mean components.
