# Pipeline Câmbio — Dados de Posição e Fluxo BCB

---

## Tabela `macro_brasil.cmb_reservas_bc`

Script: `domain/db/brasil/bcb/cmb_reservas_bc.py`  
Chave primária: `(date, sgs_code INT)` — `name` é coluna regular

### Reservas internacionais — mensais

| SGS | Nome | Descrição BCB | Unidade | Início |
|---|---|---|---|---|
| 3546 | `reserves_total_monthly` | International reserves - Total - monthly | US$ MM | 1970 |
| 3547 | `reserves_fx_total` | Foreign currency reserves (convertible) - Total | US$ MM | 2000 |
| 3548 | `reserves_fx_securities` | Foreign currency reserves - Securities | US$ MM | 2000 |
| 3549 | `reserves_fx_currency_deposits` | Foreign currency reserves - Currency and deposits | US$ MM | 2000 |
| 3550 | `reserves_imf_position` | IMF reserve position | US$ MM | 2000 |
| 3551 | `reserves_sdrs` | Special Drawing Rights (SDRs) | US$ MM | 2000 |
| 3552 | `reserves_gold_usd` | Gold (including gold deposits) | US$ MM | 2000 |
| 3553 | `reserves_gold_volume` | Gold - volume | troy oz (thousand) | 2000 |
| 3554 | `reserves_other_total` | Other reserve assets - Total | US$ MM | 2000 |
| 3555 | `reserves_other_derivatives` | Other reserve assets - Financial derivatives | US$ MM | 2000 |
| 3556 | `reserves_other_loans` | Other reserve assets - Loans to nonbank nonresidents | US$ MM | 2000 |
| 7323 | `reserves_other_reverse_repo` | Other reserve assets - Reverse Repo | US$ MM | 2002 |

> **Excluído:** 3545 (anual). **Excluído:** 3557 (Notes and coins — descontinuado set/2008).

### Posição cambial líquida BCB — mensais (Tabela 12 BCB)

| SGS | Nome | Descrição | Unidade | Início |
|---|---|---|---|---|
| 21195 | `bank_fx_spot_position` | Posição de câmbio dos bancos no mercado à vista (net) | US$ MM | 1994 |
| 29533 | `bcb_swap_cambial_position` | Swap cambial BCB — posição líquida; negativo = BCB vendeu swap ao mercado | US$ MM | 2008 |
| 29534 | `bcb_fx_stock_repos_loans` | Estoque de linhas com recompra, empréstimos e compromissadas em ME | US$ MM | 2008 |
| 29535 | `bcb_fx_other_assets_liabilities` | Outros ativos/passivos no balanço do BCB | US$ MM | 2008 |

### Reservas internacionais — diárias

| SGS | Nome | Descrição | Início |
|---|---|---|---|
| 13621 | `reserves_total_daily` | International reserves - Total - daily | 1998 |
| 13982 | `reserves_liquidity_daily` | International reserves - Liquidity concept - daily | 2008 |

### Intervenções BCB — diárias

| SGS | Nome | Descrição | Obs |
|---|---|---|---|
| 17843 | `bcb_intervention_spot` | Spot net interventions – settled | 1.697 |
| 24425 | `bcb_intervention_forwards` | Forwards net interventions – settled | 11 |
| 24427 | `bcb_intervention_fx_loans_repos` | FX loans and FX repos – settled | 316 |
| 24448 | `bcb_intervention_repo_lines` | Repo lines of credit – settled | 278 |

> Zeros filtrados — armazenam apenas dias com intervenção efetiva.  
> Positivo = BCB comprando USD, negativo = vendendo.

### Contagens

| SGS | Obs | Período |
|---|---|---|
| 3546 | 665 | 1971 – 2026-05 |
| 3547–3556 | ~305 cada | 2001 – 2026-05 |
| 7323 | 292 | 2002 – 2026-05 |
| 21195 | 388 | 1994 – 2026-05 |
| 29533 | 221 | 2008 – 2026-05 |
| 29534/29535 | 221 cada | 2008 – 2026-05 |
| 13621 | 6.986 | 1998 – 2026-06 |
| 13982 | 4.644 | 2008 – 2026-06 |
| 17843/24425/24427/24448 | 2.302 total | 1999 – 2026-06 |
| **Total** | **~19.000** | |

---

## Tabela `macro_brasil.cmb_cambio_contratado`

Script: `domain/db/brasil/bcb/cmb_cambio_contratado.py`  
Chave primária: `(date, sgs_code INT)`

### Tabela 13 — Movimento de câmbio contratado (DIÁRIO, desde set/2008)

| SGS | Nome | Descrição |
|---|---|---|
| 13961 | `cc_saldo_total` | Saldo total c = (a+b) |
| 13962 | `cc_export_total` | Exportação de bens - Total |
| 13963 | `cc_export_acc` | Exportação - Adiantamento de Contrato de Câmbio (ACC) |
| 13964 | `cc_export_pa` | Exportação - Pagamento Antecipado (PA) |
| 13965 | `cc_export_outros` | Exportação - Demais |
| 13966 | `cc_import_total` | Importação de bens |
| 13967 | `cc_saldo_comercial` | Saldo comercial (a) |
| 13968 | `cc_fin_compras` | Financeiro - Compras (total) |
| 13969 | `cc_fin_vendas` | Financeiro - Vendas (total) |
| 13970 | `cc_fin_saldo` | Financeiro - Saldo (b) |

### Tabela 14 — Financeiro detalhado (MENSAL)

| SGS | Nome | Descrição | Início |
|---|---|---|---|
| 11050 | `cc_fin_saldo_det` | Saldo financeiro detalhado | 1982 |
| 29561 | `cc_fin_servicos` | Serviços | 2011 |
| 29562 | `cc_fin_rendas` | Rendas primária e secundária | 2011 |
| 29563 | `cc_fin_cap_bras` | Capitais brasileiros | 2011 |
| 29564 | `cc_fin_cap_ext` | Capitais estrangeiros | 2011 |

### Contagens

| Grupo | Obs | Período |
|---|---|---|
| Diárias (13961–13970) | 44.610 | set/2008 – jun/2026 |
| Mensais (11050, 29561–29564) | 1.272 | 1982 – 2026-05 |
| **Total** | **~45.882** | |

---

## Notas técnicas

- Séries diárias em ambas as tabelas usam chunking anual para evitar erro 406 da API BCB.
- `cmb_cambio_contratado` ≠ `cmb_fluxo_cambial`: o contratado mede liquidações banco-cliente (Tabelas 13/14 BCB); o fluxo registrado (24xxx) é uma medida mais ampla de todos os canais.
- 3553 (`reserves_gold_volume`) em troy oz (thousand), não USD.
- 29533 negativo = BCB tem posição vendida em USD via swap (swap tradicional ao mercado).

---

## Pendências

- [ ] Confirmar SGS 22099/22100 (termos de troca) — descrições exatas
