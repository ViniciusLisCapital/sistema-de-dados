# Fiscal Impulse Metrics — Reference

Documents every metric built into `reports/brasil/fiscal_impulse_audit.xlsx` (not yet part of
`report.html`/`generate_report.py` — this is an audit workbook, built directly from BCB "tabelas
especiais" downloads, not from the MySQL tables `fisc_divida`/`fisc_nfsp`/`fisc_rtn` that feed the
main Panorama Fiscal report). Formulas, rationale, and literature references, in the order the
metrics were built.

## Motivation

The standard fiscal-impulse concept (IMF/OECD: the change in the cyclically-adjusted primary balance)
only sees what passes through the budget. It says nothing about *how* a deficit is financed — by
selling bonds to the private sector (draining existing savings) vs. by the Central Bank absorbing
them (creating new money) — and it says nothing about quasi-fiscal channels that inject money into
the economy without ever appearing as budget spending (subsidized directed credit being the largest
one in Brazil). This workbook builds toward a "whole story" version: how much net stimulus the
consolidated public sector is injecting into the real economy, through *any* channel, not just the
primary balance.

## Data sources

| File / series | Provider | What it gives | Frequency |
|---|---|---|---|
| `Dlspp.xlsx` | BCB, "tabelas especiais" (manual download, no API) | DLSP composition by government level and instrument — gross debt, cash (Conta Única, depósitos à vista), PIB acumulado 12m | Monthly, 2001-12→ |
| `Dbggindexp.xlsx` | BCB, "tabelas especiais" (manual download, no API) | DBGG (Governo Geral = Federal+Estados+Municípios only) stock and official net-issuance flow, by indexador | Monthly, 2006-12→ |
| SGS 4189 | BCB SGS (REST API) | Meta Selic (% a.a.) | Daily/monthly |
| SGS 256 | BCB SGS (REST API) | TJLP (% a.a.) | Monthly (superseded by TLP for new contracts since 2018, see Metric 5) |
| SGS 20593 | BCB SGS (REST API) | Saldo da carteira de crédito com recursos direcionados — Total (PF+PJ) | Monthly, 2007-03→ |
| SGS 20756 | BCB SGS (REST API) | Taxa média de juros das operações de crédito com recursos direcionados — Total | Monthly, 2011-03→ |

## Building blocks: debt and cash by government level

Reconstructed from `Dlspp.xlsx`'s per-level detail (Federal, Estados, Municípios, Estatais):

- **`Debt_Federal` / `Debt_Estados` / `Debt_Municipios` / `Debt_SOEs`** — sum of pure-liability rows
  per level (excludes every credit-side row: Conta Única, FAT, Previdência, Renegociações, Créditos a
  Inst. Financ. Oficiais, Aplicações em fundos, Outros créditos).

- **`Cash_Federal`** = Conta Única + Depósitos à vista. **`Cash_Estados`** = Depósitos à vista.

  **`Cash_Municipios`** = Depósitos à vista e aplicações. **`Cash_SOEs`** = Depósitos à vista (soma
  federais+estaduais+municipais).

**Verified**: liability rows + credit rows per level reconcile *exactly* (0.0 difference) to DLSP's
own published net total for that level — see `Reconciliacao` sheet, `_check_*` columns.

**Known bug, fixed**: an earlier version double-counted "Dívida Mobiliária na carteira do Bacen" (row
49) on top of "Dívida mobiliária em mercado" (row 30, which already includes it), inflating
`Debt_Federal` by ~26% vs. the official DBGG. Row 49 was moved to a separate `Memo_IntraSetor` bucket,
excluded from `Debt_Federal`.

**Known open gap, not fixed**: `Debt_Federal + Debt_Estados + Debt_Municipios` still diverges from the
official `DBGG_GovGeral_publicado` by a time-varying amount (mean −3.7%, range −14.7% to +20.5%,
2006–2026). Likely a market-value-vs-book-value or instrument-classification difference between
`Dlspp.xlsx`'s composition and DBGG's own methodology. Treat any *by-level* debt breakdown as
approximate, not official — this is why Metric 2 below is flagged as the least reliable of the three
Impulso variants.

## Metric 1 — `Impulso_por_nivel`

```
Impulso_por_nivel(t) = [Debt_Total(t) − Debt_Total(t−1)] − [Cash_Total(t) − Cash_Total(t−1)]
```

where `Debt_Total = Debt_Federal + Debt_Estados + Debt_Municipios + Debt_SOEs` and `Cash_Total`
likewise sums all four levels. The only one of the three original variants decomposable by government
level. **Not reliable as a headline number** — inherits the reconciliation gap above, and is a clear
outlier vs. Metrics 2 and 3 when cross-checked (12m-accumulated: +R$1,247.9bi vs. −R$26.2bi and
−R$5.0bi respectively, same period). Kept in the workbook for the by-level composition view only.

## Metric 2 — `Impulso_limpo_DBGG`

```
Impulso_limpo_DBGG(t) = EmissaoLiquida_DBGG_publicado(t) + [Debt_SOEs(t) − Debt_SOEs(t−1)]
                         − [Cash_Total(t) − Cash_Total(t−1)]
```

Uses BCB's own official, already interest-stripped net-issuance flow for Federal+Estados+Municípios
(`Dbggindexp.xlsx`, aba "Emissões líquidas por indexador"), adding SOEs' debt change (not covered by
DBGG) and subtracting the same consolidated cash change as Metric 1. Cleaner than Metric 1 on the
Federal+Estados+Municípios side (no reconstruction, no reconciliation gap), but not decomposable by
level within that block — only Federal+Estados+Municípios as one number vs. SOEs separately.

## Metric 3 — `Impulso_BC_menos_Cash`

```
Impulso_BC_menos_Cash(t) = [BC_holdings_Federal(t) − BC_holdings_Federal(t−1)]
                            − [Cash_Total(t) − Cash_Total(t−1)]
```

where `BC_holdings_Federal` is `Dlspp.xlsx` row 49, "Dívida Mobiliária na carteira do Bacen" — the
same row excluded from `Debt_Federal` above (this is where it's actually used).

**Derivation**: from a three-agent accounting identity (Government / Central Bank / Real Economy)
worked out by the user directly (`reports/brasil/raciocinio_impulso.xlsx`):

```
C(t) = C(t-1) + ΔGD(t) + ΔBC(t) + [T(t) - G(t)]      -- Government's cash balance
ΔRE(t) = [G(t) - T(t)] - ΔGD(t)                       -- Real Economy, from the same system
  =>  ΔRE(t) = ΔBC(t) - ΔC(t)                          -- substituting, GD cancels out
```

`ΔRE` (change in the real economy's holdings) is the actual quantity of interest — what this workbook
calls the fiscal impulse. The algebra shows it needs no debt-issuance term at all (`GD` cancels), just
the change in BC's bond holdings minus the change in government cash — the simplest of the three
formulas, and the only one that needs no debt-by-level reconstruction whatsoever.

**Theoretical grounding**: this is a specific case of the classic bond-financed-vs.-money-financed
deficit decomposition in monetary theory — Sargent, T.J. & Wallace, N. (1981), *"Some Unpleasant
Monetarist Arithmetic,"* Federal Reserve Bank of Minneapolis Quarterly Review. It also matches BCB's
own consolidation logic in the DLSP methodology manual: intra-public-sector debt (government owing
the Central Bank) is netted out at the consolidated level because it isn't a claim held by an "outside"
creditor.

**Caveat — what `BC_holdings_Federal` actually measures in Brazil**: this line is dominated by
*operações compromissadas* (repo operations), BCB's day-to-day tool for hitting the Selic target —
cyclical, reversible monetary-policy plumbing, not necessarily a deliberate decision to monetize the
deficit. The share of row 49 that is repo collateral vs. genuine outright/permanent holdings has not
been checked. Related literature: Hawkins, J., *"Central Bank Balance Sheets and Fiscal Operations,"*
BIS Papers No. 20d; BIS Papers No. 122, *"The Monetary-Fiscal Policy Nexus in the Wake of the
Pandemic"* (2021, EME-focused, discusses Brazil).

**Caveat — noise**: `ΔCash_Total` is a raw month-to-month stock difference, not flow-decomposed, so
individual months are noisy (12m-accumulated is the number to read, not the monthly figure).

## Metric 4 — `Subsidio_Implicito_Direcionado`

```
Subsidio_Implicito_Direcionado(t) = [Selic_meta(t) - Taxa_media_direcionado(t)] / 100 / 12
                                      × Estoque_credito_direcionado(t)
```

The quasi-fiscal piece: the implicit cost to the public sector of directing credit (BNDES/Caixa/BB,
historically at TJLP, now TLP) below what it would cost at the policy rate. Available from 2011-03
(limited by the rate-series history; the stock series itself goes back to 2007-03).

**Literature — general framework**: Mackenzie, G.A. & Stella, P. (1996), *"Quasi-Fiscal Operations of
Public Financial Institutions,"* IMF Occasional Paper No. 142 — defines the implicit subsidy as
`(market rate − subsidized rate) × subsidized loan stock`, the formula used here. Blejer, M.I. &
Cheasty, A. (eds., 1991), *"How to Measure the Fiscal Deficit,"* IMF, ch. 11 "Amalgamating Central
Bank and Fiscal Deficits" — argues quasi-fiscal subsidies should be added to the primary deficit for a
true public-sector deficit figure. IMF WP/23/114 (2023), *"Quasi-Fiscal Implications of Central Bank
Crisis Interventions"* — a modern framework for isolating a quasi-fiscal residual from a central
bank's balance sheet.

**Literature — Brazil-specific**: SEAE/Ministério da Fazenda estimated the implicit BNDES subsidy
(TJLP-priced, FAT/Tesouro-funded) at ~R$429bn over 2007–2016 (~R$43bn/yr), against an explicit
equalização-de-taxas budget line of ~R$9.5bn/yr — used below as the validation benchmark. BCB Working
Paper 490, *"Impactos do Direcionamento de Crédito sobre a Economia,"* covers the TJLP/TLP subsidy
mechanics directly. IPEA/Feijó (2014), *"Um Estudo Quantitativo dos Subsídios Implícitos nas Operações
de Crédito do PRONAF"* — same market-rate-minus-subsidized-rate methodology, applied to a specific
credit line.

**Why Selic, not the "taxa média — crédito livre" series, as the market-rate benchmark**: tested
empirically before adopting this formula. SGS 20717 (taxa média, crédito livre, Total) reads ~49.8%
a.a. (2026-06) — dominated by unsecured retail products (cheque especial, cartão rotativo), not
comparable in risk/duration to long-term directed credit. Multiplying that spread by the R$3.19tn
direcionado stock would imply a subsidy in the trillions of reais — implausible on its face, discarded
after the check. Selic (SGS 4189) is used instead, matching this project's existing convention for
that series (see `domain/db/brasil/bcb/cred_inadimplencia_pj.py`'s docstring for the 4390→4189
annualization fix this project already made elsewhere).

**Why the realized average rate (SGS 20756), not TJLP or TLP directly**: TJLP was replaced by TLP for
new contracts starting 2018-01-02 (Lei 13.483/2017), but contracts signed before 2018 keep earning
TJLP until they mature, and TLP itself only fully converged to the market NTN-B rate in 2023 (a
legally-fixed "redutor" schedule: 57% in 2018, rising to 100% in 2023). There is no public data on the
TJLP-legacy vs. TLP-new mix within the aggregate stock, so no single contractual rate can be applied
to the whole stock without bias. SGS 20756 (the actual realized average rate paid across the whole
book) sidesteps this — it already reflects whatever blend of legacy and current contracts exists in
any given month, with no reconstruction needed. TLP itself is not published as a BCB SGS series at all
(confirmed by searching `dadosabertos.bcb.gov.br` directly — only unrelated balance-of-payments
"longo prazo" series match that search term); it would otherwise require scraping BNDES's own
published historical table.

**Validation**: 2016 average = R$48.6bn/yr, against the SEAE benchmark of R$42.9bn/yr for the same
decade — close. Last-12-months average (~2025–2026) = R$89.6bn/yr ≈ 0.78% of GDP, against IPEA's Carta
de Conjuntura estimate of ~0.97% of GDP (2024, "subsídios financeiros" + "subsídios creditícios"
combined) — same order of magnitude.

## Metric 5 — `Impulso_Total`

```
Impulso_Total(t) = Impulso_BC_menos_Cash(t) + Subsidio_Implicito_Direcionado(t)
```

The "whole story" metric: monetary-financing channel plus quasi-fiscal directed-credit channel.
Available from 2011-03 onward (limited by Metric 4's rate-series history).

## Not yet included

- **Tax expenditures** ("gastos tributários", Receita Federal's annual DGT) — annual only, no API,
  too slow-moving for a monthly impulse metric.
- **Contingent liabilities / guarantees** (Tesouro's Anexo de Riscos Fiscais, federal; Siconfi
  RGF/RREO/DCA, subnational — the latter *does* have a REST API,
  `apidatalake.tesouro.gov.br/docs/siconfi/`) — conceptually a risk overlay, not a flow, so not
  additive to `Impulso_Total` even if added; would sit alongside it.
- **Explicit equalização de taxas** (Tesouro Transparente's "Boletim de Subsídios," CKAN dataset) —
  the direct budget-line cost, useful as a lower-bound cross-check against Metric 4's implicit-subsidy
  estimate, not yet pulled in.

## Standard fiscal impulse, for contrast

The IMF/OECD definition — `Impulso = −Δ(cyclically-adjusted primary balance, % potential GDP)` — is
not built here and is a different concept: it measures discretionary policy tightening/loosening
relative to the economic cycle, and by construction excludes everything quasi-fiscal or off-budget.
Reference: IMF Technical Notes and Manuals, *"Computing Cyclically Adjusted Balances and Automatic
Stabilizers"* (2009); the output-gap-dependence critique goes back to Blanchard, O. (1990), *"Suggestions
for a New Set of Fiscal Indicators,"* OECD Working Paper No. 79.
