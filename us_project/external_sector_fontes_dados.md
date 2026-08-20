# US external sector — source mapping (Census / BEA / Fed Board / Treasury TIC / BIS)

Surveyed live on 2026-08-17 against each source's API, not just its documentation — same method as
[`analytics/brasil/labor_market/fontes_dados.md`](../analytics/brasil/labor_market/fontes_dados.md). Cross-cutting
access status: [`README.md`](README.md). Brazil counterpart:
[`analytics/brasil/exchange_rate/CLAUDE.md`](../analytics/brasil/exchange_rate/CLAUDE.md).

**Why this branch is not called `exchange_rate`.** The Brazil report exists to explain BRL: carry,
REER, reserves, BOP, contracted FX flow, CFTC positioning — the currency is the dependent variable.
For the US the dollar is the numéraire, so the interesting objects are the external accounts
themselves: the trade balance, the current account, the net international investment position, and who
holds Treasuries. The dollar indices are inputs here rather than the subject.

**Partly in the database already** — this is the one branch with real existing coverage, all of it in
`macro_international` because it was built for the Brazil side.

## Coverage table

| Data | Primary source | On FRED | Agency direct | Format | In DB | Comment |
|---|---|---|---|---|---|---|
| Nominal dollar indices | **Fed Board** (H.10) | ✅ `DTWEXBGS` (broad), `DTWEXAFEGS` (advanced), `DTWEXEMEGS` (emerging), all daily 2006-01→ | ✅ DDP | FRED | ⚠️ `cmb_dollar_index_em` (`DTWEXEMEGS`) already ingested; `cmb_dollar_index` holds DXY from Yahoo (**1971-01→**, far longer) | The Fed's indices only start **2006-01** — that is why the Brazil pipeline chose Yahoo's ICE DXY instead. Documented in the root `CLAUDE.md` |
| Real effective exchange rate | **BIS** | ✅ `RBUSBIS` (broad, 1994-01→), `RNUSBIS` (narrow, **1964-01→**) | ✅ BIS API (`connectors/bis.py` already works) | FRED / SDMX | ⚠️ `cmb_reer` covers BR/MX/CL/CO, not US | Adding US to the existing `cmb_reer` table is a one-line change to the country list |
| Bilateral spot rates | **Fed Board** (H.10/G.5) | ✅ `DEXJPUS`, `DEXCHUS`, `DEXBZUS`, `DEXUSUK`, `DEXCAUS`, `DEXMXUS`, `DEXKOUS` (daily), `EXUSEU` (monthly) | ✅ | FRED | ⚠️ `cmb_fx_latam` covers MX/CL/CO/PE from Yahoo | Note the **direction flips**: `DEXUSUK` and `EXUSEU` are USD *per* foreign unit; the rest are foreign units per USD |
| Trade in goods and services, monthly | **Census/BEA** (FT-900) | ✅ `BOPGSTB` (total balance), `BOPGTB` (goods balance), `BOPGEXP`/`BOPGIMP`, `BOPSEXP`/`BOPSIMP`, `BOPTEXP`/`BOPTIMP` — all 1992-01→ | 🔑 Census key needed | FRED | ❌ | Live at 2026-06: total balance **−$73.3bn**, goods **−$102.1bn**, services **+$28.8bn**. FRED has the aggregates; **product and country detail needs the Census key** |
| Trade by partner country | **Census** | ✅ only the big four: `IMPCH`/`EXPCH` (China, 1985-01→), `IMPMX`/`EXPMX` (Mexico) | 🔑 Census | FRED | ❌ | The analogue of `cmb_comex_pais`, which has the full partner list for Brazil. FRED carries a handful of countries; the rest needs the API |
| Trade by product / HS code | **Census** | ❌ | 🔑 Census (`timeseries/intltrade/imports/hs`) | — | ❌ | The analogue of `cmb_comex_produto`/`cmb_comex_fator_agregado`. **No FRED path at all** |
| Current account | **BEA** (ITA) | ✅ `IEABC` (1999-01→), `IEABCSN` (services balance), `IEAXGS`/`IEAMGS`, `NETFI` (NIPA basis, **1947-01→**) | 🔑 BEA key needed | FRED | ❌ | Live at 2026-Q1: current account **−$226.8bn**. The analogue of `cmb_balanco_pagmt`. **Full BOP detail (income, transfers, financial account) needs the BEA key** |
| Net international investment position | **BEA** | ✅ `IIPUSNETIQ` (2006-01→) | 🔑 BEA | FRED | ❌ | Live at 2026-Q1: **−$21.27tn**. No Brazil counterpart in the current pipeline |
| International reserves | **IMF** (via FRED) | ✅ `TRESEGUSM052N` (ex-gold, 1950-12→) | not probed | FRED | ⚠️ `cmb_reservas_bc` is Brazil's | Live at 2026-06: **$240.2bn** — two orders of magnitude below Brazil's relative position, which is the point of the series for a reserve-currency issuer |
| **Foreign holdings of Treasuries, by country** | **Treasury** (TIC) | ⚠️ only the aggregate (`FDHBFIN`, and it **lags a quarter**) | ✅ **`mfhhis01.csv` confirmed** | csv | ❌ | Major Foreign Holders table — Japan, China, UK etc. **Only reachable from TIC.** The closest US analogue of the Brazil report's foreign-investor-flow section |
| **Cross-border securities flows** | **Treasury** (TIC) | ❌ | ✅ **`slt1d_globl.csv` confirmed** (1.37 MB) | csv | ❌ | Long-term securities held by foreign residents, by instrument. Awkward CSV layout — see Gotchas |
| Speculative FX positioning | **CFTC** | ❌ | ✅ `connectors/cftc.py` already works | — | ⚠️ `cmb_cot_fx` covers BRL/MXN | Adding the dollar-index and major-currency contracts is a change to the existing script's contract list, not a new connector |
| Terms of trade | derived / BLS | ✅ `IR`/`IQ` (import/export price indices — see the inflation branch) | ✅ | FRED | ❌ | `IQ ÷ IR` is the standard construction. Brazil has `cmb_termos_troca` published directly by the BCB; the US has no published equivalent |
| Merchandise trade, OECD basis | **OECD** (via FRED) | ✅ `XTEXVA01USM667S` (1955-01→) | not probed | FRED | ❌ | Long history but only to 2026-04 — laggier than the Census-based series |

🔑 = the direct path needs an API key we do not have yet (free registration; see README).

## Verified series inventory

30 external-sector candidates checked, **30 exist — a clean sweep**, the only branch of the eight
with no failures at all. By release: U.S. International Trade in Goods and Services (11 series — a
12th, the headline balance `BOPGSTB`, is counted under activity), H.10 Foreign Exchange Rates (10),
U.S. International Transactions (3), BIS Effective Exchange Rate Indices (2), plus the IIP, IMF
reserves, G.5 and OECD series. Note that what FRED *has* here is thin relative
to what the sources publish — the missing material (trade by product, BOP detail, TIC by country) is
absent from FRED entirely rather than present under a different id.

Latest data as probed: FX rates to **2026-08-07**, monthly trade to **2026-06**, quarterly ITA/IIP to
**2026-Q1**, BIS REER to **2026-06**.

## Gotchas found live

- **The Fed's dollar indices only start 2006-01.** All three (`DTWEXBGS`, `DTWEXAFEGS`,
  `DTWEXEMEGS`) begin there — the pre-2006 broad index was a different series that was discontinued.
  This is already known on the Brazil side (root `CLAUDE.md` records choosing Yahoo's ICE DXY,
  1971-01→, over FRED's `DTWEXBGS` for exactly this reason) and `macro_international.cmb_dollar_index`
  already holds 14,114 daily observations back to 1971-01-04. **Reuse it rather than re-solving this.**
- **Bilateral rate direction is inconsistent within the same FRED release.** `DEXUSUK` (1.3498) and
  `EXUSEU` (1.1423) are dollars per foreign unit; `DEXJPUS` (157.54), `DEXCHUS` (6.7474),
  `DEXBZUS` (5.0882), `DEXCAUS`, `DEXMXUS`, `DEXKOUS` are foreign units per dollar. The id prefix
  `DEXUS…` vs. `DEX…US` encodes it, which is easy to miss. An index built by averaging them without
  inverting the first two is wrong and still plausible-looking.
- **TIC CSVs are report layouts, not data files.** `mfhhis01.csv` opens with three lines of title and
  units (`,,MAJOR FOREIGN HOLDERS OF TREASURY SECURITIES,,,,,,,,,,,`) before any header, and
  `slt1d_globl.csv` has quoted fragments split mid-word across columns
  (`"TABLE 1D:  U.","S. Long-Term Se","curities Held b"…`) — an artefact of a fixed-width export.
  Both need bespoke parsing, closer to the BCB `Facdetp.xlsx` work than to reading an API. Budget for
  it.
- **`FDHBFIN` (aggregate foreign holdings, on FRED) lags TIC by a quarter** — it ended 2025-10 when
  probed, against 2026-01 for its sibling holder series. If the holder-composition chart needs the
  current quarter, TIC is the source, not FRED.
- **Two definitions of the current account are both on FRED and they differ.** `IEABC` is the BEA's
  ITA measure (−$226.8bn in 2026-Q1, quarterly level) and `NETFI` is the NIPA-consistent "balance on
  current account, NIPAs" (−$994.5bn SAAR). Different basis, different units, same name in
  conversation. Pick one per chart and label it.
- **`XTEXVA01USM667S` (OECD merchandise exports) is stale relative to the Census series** — 2026-04
  vs. 2026-06. Long history, laggy tail; the usual trade-off with OECD redistribution.

## Open items

- **Get the Census key** — trade by product and by partner country is the whole substance of the
  Brazil report's Comex tabs and there is no FRED path to it.
- **Get the BEA key** — the current account beyond the headline (primary/secondary income, the
  financial account, direct vs. portfolio investment) is ITA table detail.
- **Three cheap extensions to existing Brazil infrastructure**, all confirmed feasible: add `US` to
  `cmb_reer`'s country list (`connectors/bis.py` already works), add the dollar-index contract to
  `cmb_cot_fx` (`connectors/cftc.py` already works), and reuse `cmb_dollar_index` rather than
  ingesting `DTWEXBGS`.
- **Decide the schema boundary.** `cmb_dollar_index` and `cmb_equity_us` sit in `macro_international`
  today even though both are single-country US series — by the repo's own rule
  ([`domain/db/CLAUDE.md`](../domain/db/CLAUDE.md): "anything needing 2+ countries") they arguably
  belong in `macro_us`. Worth settling before adding more, or the boundary stops meaning anything.
- **Not inventoried this round**: the full TIC table set, BEA ITA tables, Census trade by district
  and by end-use category, and the IMF's own reserve-composition (COFER) data.
