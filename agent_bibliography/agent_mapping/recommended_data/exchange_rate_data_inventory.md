# Exchange Rate Data Inventory

**Purpose:** inventory of the data categories relevant to exchange rate (BRL) analysis, mapping each analytical category to what already exists in the database (`macro_brasil` / `macro_international` / `macro_analytics`) and to what's still missing. Meant to inform the exchange rate analysis agent (see `CAMBIO.md`, "Fase 3 — Agente de análise") about which series are available to support each type of argument.

**Not cross-linked yet** to `exchange_rate_conceptual_map.md` (theory/bibliography) — that's left for a later step, by the user's decision. For now this file documents only the data side.

Technical details on schema, SGS codes and observation counts live in `CAMBIO.md` and `RESERVAS.md` — this file organizes the same information by analytical category instead of by table.

---

## 1. Spot price — ⚠️ GAP

There is currently no spot exchange rate series (PTAX or otherwise) stored in `macro_brasil`, `macro_international` or `macro_analytics`. The entire FX pipeline covers *determinants* of the exchange rate (flow, positioning, rates, reserves) but not the dependent variable (USD/BRL) itself.

**Impact:** the analysis agent cannot today directly correlate fundamentals with the level or change of the exchange rate — it needs that to be supplied externally or read from another source on each analysis.

**Possible source:** BCB SGS 1 (PTAX sell, daily, since 1984) or 10813 (PTAX sell, closing). No script built yet.

---

## 2. Interest rate differential (carry)

| What we have | Table | Series | Coverage |
|---|---|---|---|
| Selic (raw) | `macro_analytics.diferenciais_juros` | `selic` | ~36m rolling (script's default window) |
| Fed Funds (raw) | `macro_analytics.diferenciais_juros` | `fed_funds` | same |
| Nominal ex-post differential | `macro_analytics.diferenciais_juros` | `diferencial_nominal` | same |
| Real ex-post differential (Selic − IPCA vs. Fed Funds − CPI) | `macro_analytics.diferenciais_juros` | `real_br_ex_post`, `real_us_ex_post`, `diferencial_real` | same |

Script: `domain/db/analytics/fred/diferenciais_juros.py`.

**Gaps:**
- History limited to ~36 months by default (Selic available since 1996 on SGS, Fed Funds since 1954 on FRED — full historical load still pending, see `CAMBIO.md` §1a).
- **Ex-ante** differentials (based on expectations, not realized inflation) not implemented yet — detailed plan in `CAMBIO.md` §1b/§2, uses `macro_brasil.expectativas` (Focus) on the BR side and FRED (`FF{m}` futures/OIS, `MICH`/`T5YIE`) on the US side.
- Cupom cambial (DDI/FRC curve) and B3 futures (DOL/WDO) — deferred, requires Bloomberg access (`blpapi`/`xbbg`).

---

## 3. Terms of trade / commodity prices

| What we have | Table | Series | Note |
|---|---|---|---|
| Terms of trade index (series A) | `macro_brasil.termos_de_troca` | `termos_de_troca_a` (SGS 22099) | exact description (FOB vs. CIF? basket?) unconfirmed |
| Terms of trade index (series B) | `macro_brasil.termos_de_troca` | `termos_de_troca_b` (SGS 22100) | same |

Script: `domain/db/brasil/bcb/termos_de_troca.py`.

**Gaps:**
- Exact descriptions of both series still pending confirmation with BCB SGS.
- No individual commodity prices (iron ore, soybeans, oil) — only the BCB's aggregate index. If the agent needs to decompose terms of trade by commodity, there's no data for that today.

---

## 4. Balance of payments

| What we have | Table | Series | Coverage |
|---|---|---|---|
| Current account, trade balance+services, goods exports | `macro_brasil.balanco_pagamentos` | `conta_corrente`, `balanca_comercial_servicos`, `exportacao_bens` | 2001 → today |
| Financial account, FDI (net and inflows), outward FDI | `macro_brasil.balanco_pagamentos` | `conta_financeira`, `investimento_direto_liquido`, `idp_ingressos`, `ide_saidas` | 2001 → today |
| Portfolio investment (total, equities, fixed income) | `macro_brasil.balanco_pagamentos` | `investimento_carteira`, `carteira_acoes`, `carteira_renda_fixa` | 2001 → today |

Script: `domain/db/brasil/bcb/balanco_pagamentos.py`. BPM6 methodology.

**Gaps:** none identified at this time — coverage considered complete for the current FX report's purposes.

---

## 5. FX flow (registered vs. contracted)

Two distinct tables measuring different channels — **not substitutes for one another**:

### 5a. Registered FX flow (BCB Nota Cambial)

| What we have | Table | Series |
|---|---|---|
| Total balance/inflow/outflow | `macro_brasil.fluxo_cambial` | `total_saldo`, `total_entrada`, `total_saida` |
| Commercial sector (inflow/outflow) | `macro_brasil.fluxo_cambial` | `comercial_entrada`, `comercial_saida` |
| Financial sector (balance) | `macro_brasil.fluxo_cambial` | `financeiro_saldo` |

Script: `domain/db/brasil/bcb/fluxo_cambial.py`. Coverage: 2003 → today.

**Gaps:** CEP/CBE sub-items of the financial flow (finer granularity, published in the weekly Nota Cambial) — candidate SGS codes (24372–24376) unconfirmed. Commercial balance (24366) timed out during research — can be derived as `comercial_entrada − comercial_saida` if needed.

### 5b. Contracted FX (bank-client movement)

| What we have | Table | Series |
|---|---|---|
| Daily — total balance, exports (total/ACC/PA/other), imports, commercial balance, financial purchases/sales/balance | `macro_brasil.cambio_contratado` | `cc_saldo_total`, `cc_export_*`, `cc_import_total`, `cc_saldo_comercial`, `cc_fin_compras`, `cc_fin_vendas`, `cc_fin_saldo` | since Sep/2008 |
| Monthly — detailed financial breakdown (services, income, domestic/foreign capital) | `macro_brasil.cambio_contratado` | `cc_fin_saldo_det`, `cc_fin_servicos`, `cc_fin_rendas`, `cc_fin_cap_bras`, `cc_fin_cap_ext` | since 1982 (monthly) / 2011 (detailed) |

Script: `domain/db/brasil/bcb/cambio_contratado.py`. ~46k observations.

**Conceptual difference:** `cambio_contratado` measures bank-client settlements (BCB Tables 13/14); `fluxo_cambial` (24xxx codes) is a broader measure covering all registered channels — the two should not be summed or treated as equivalent.

---

## 6. International reserves and BCB intervention

| What we have | Table | Series (main) | Frequency |
|---|---|---|---|
| Total reserves and by component (FX securities, deposits, IMF, SDR, gold, other assets) | `macro_brasil.reservas` | `reserves_total_monthly`, `reserves_fx_*`, `reserves_imf_position`, `reserves_sdrs`, `reserves_gold_*`, `reserves_other_*` | monthly |
| Reserves — total and liquidity concept | `macro_brasil.reservas` | `reserves_total_daily`, `reserves_liquidity_daily` | daily |
| Banks' net FX spot position | `macro_brasil.reservas` | `bank_fx_spot_position` (SGS 21195) | monthly |
| BCB FX swap — net position | `macro_brasil.reservas` | `bcb_swap_cambial_position` (SGS 29533) | monthly |
| Stock of repo lines/loans/repurchase agreements in FX | `macro_brasil.reservas` | `bcb_fx_stock_repos_loans` (SGS 29534) | monthly |
| BCB interventions (spot, forwards, FX loans/repos, repo lines) — only days with actual intervention | `macro_brasil.reservas` | `bcb_intervention_spot`, `bcb_intervention_forwards`, `bcb_intervention_fx_loans_repos`, `bcb_intervention_repo_lines` | daily (sparse) |

Script: `domain/db/brasil/bcb/reservas.py`. ~19k observations total. Full detail in `RESERVAS.md`.

**Coverage considered robust** — includes both the stock (reserves, bank position, swap) and the intervention flow (BCB's net buying/selling in spot and forwards), which lets the agent distinguish "how much the BCB has" from "what the BCB is doing right now."

**Gaps:** none identified — the historical "gross reserves" pending item (SGS 13127, timeout) mentioned in earlier versions of `CAMBIO.md` has been superseded by using the liquidity concept plus detailed components.

---

## 7. Real effective exchange rate (REER)

| What we have | Table | Coverage |
|---|---|---|
| Real (broad) and nominal (broad) REER — Brazil, Mexico, Chile, Colombia | `macro_international.reer` | 1994 → today (BIS, full history) |

Script: `domain/db/international/bis/reer.py`. Source: BIS Statistics API.

**Gaps:**
- Only 4 LatAm countries (BR/MX/CL/CO) — no coverage of other relevant EM peers for comparison (e.g., Turkey, South Africa, India) or developed-market peers.
- `real_narrow` was excluded from scope (broad basket only).

---

## 8. Speculative positioning (FX futures)

| What we have | Table | Series | Coverage |
|---|---|---|---|
| Open interest, net/long/short positioning of "leveraged money" and non-reportables | `macro_international.cot_fx` | `open_interest`, `lev_long`, `lev_short`, `lev_net`, `nonrept_long`, `nonrept_short` | BRL and MXN, weekly (Tuesdays), 2010 → today |

Script: `domain/db/international/cftc/cot_fx.py`. Source: CFTC Traders in Financial Futures.

**Gaps:**
- CLP and COP have no CME futures — they don't appear in the TFF report, and there's no equivalent alternative data today.
- History not available before 2010 (CFTC returns 404 for 2006–2009).
- No options-based positioning data (skew, risk reversal) — see the corresponding gap in the bibliography (`exchange_rate_bibliography_gaps.md`, section 4, FX options and volatility).

---

## 9. Inflation differential and market expectations

| What we have | Table | Note |
|---|---|---|
| IPCA (28 series, incl. cores) | `macro_brasil.inflacao` | 1980 → today |
| Focus expectations — IPCA 12m/24m, IGP-M, Selic | `macro_brasil.expectativas` | 2001 → today |
| US CPI (via FRED, consumed inside the differentials calculation) | `macro_analytics.diferenciais_juros` (`cpi_12m_us`) | ~36m rolling |

Scripts: `domain/db/brasil/bcb/inflacao.py`, `domain/db/brasil/bcb/expectativas.py`.

**Use for FX analysis:** `expectativas` is already ready to feed the pending ex-ante differentials (item 2 above) — Focus Selic EOP 12m and Focus IPCA 12m are already available; only the script combining them with the US side is missing.

---

## 10. Domestic activity backdrop (context, not FX-specific)

General `macro_brasil` series that help contextualize the domestic cycle (relevant for carry/country risk, but not "FX data" per se): `ibc_br` (monthly GDP proxy), `gdp`, `pim` (industrial production), `pmc`/`pms` (retail/services), `pnad` (labor market), `caged`, `credito`, `indicadores_familias`. Full table in `CLAUDE.md`.

On the US side, activity/inflation data today only exists ad hoc inside `analytics/oraculo/us/term_us.py` (via FRED) — there's no persistent `macro_us` schema equivalent to `macro_brasil` (already logged as a pending item in `CLAUDE.md`, "Média prioridade — US expandir dados").

---

## Gap summary (suggested priority)

| Priority | Gap | Category |
|---|---|---|
| High | Spot exchange rate (PTAX) series not stored | §1 |
| High | Ex-ante interest rate differentials (Focus × Fed Funds futures/OIS) | §2 |
| Medium | Full history of `diferenciais_juros` (today ~36m, should go back to 1995/1954) | §2 |
| Medium | CEP/CBE granularity of the financial FX flow | §5a |
| Medium | Confirmation of SGS 22099/22100 descriptions (terms of trade) | §3 |
| Low | Cupom cambial + B3 futures (requires Bloomberg access) | §2 |
| Low | REER/COT for EM peers beyond BR/MX/CL/CO | §7, §8 |
| Low | Options-based positioning data (skew, risk reversal) | §8 |
| Low | Persistent `macro_us` schema (today only ad hoc FRED in the oráculo) | §10 |

---

## How to update this inventory

When creating a new table in `macro_brasil`/`macro_international`/`macro_analytics` that's relevant to FX analysis, add a row to the corresponding section (or create a new section, if it's an analytical category not yet covered) and remove/update the corresponding gap in the summary table above.
