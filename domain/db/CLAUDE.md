# domain/db/ — Context for Claude

ETL scripts that populate `macro_brasil` (`brasil/`) and `macro_international` (`international/`) on the MySQL server at `192.168.15.200` (credentials in `.env`, never hardcoded). See [`.claude/rules/domain-scripts.md`](../../.claude/rules/domain-scripts.md) for the shared `run()`-only script pattern.

## Schema criterion: domain/geography, not raw-vs-computed

A table's schema depends only on which countries' data it needs — never on whether it's raw or derived.

```
macro_brasil        — anything Brazil-specific (BCB, IBGE), raw or computed
macro_international — anything needing data from 2+ countries to exist or make sense
macro_us             — future: US-only data that isn't just an input to an international series
```

E.g. `inflc_decomposicao.contribuicao` (= `var_mensal × pesos`, computed) stays in `macro_brasil` because both inputs are Brazilian. `diferenciais_juros` stores raw `selic`/`fed_funds` alongside the computed differentials in `macro_international`, because it needs both countries to exist at all.

Signal raw vs. computed at the table/column level instead, via MySQL's native `COMMENT` (see `inflc_agregados`, `SHOW CREATE TABLE`) and/or a "Raw series" / "Derived series" docstring section (see `international/fred/diferenciais_juros.py`, `brasil/ibge/inflc_decomposicao.py`).

**A `macro_analytics`-style schema-per-computation-stage was tried and discontinued in 2026-07** — it never grew past one table (`diferenciais_juros`), which already qualified for `macro_international` under the rule above. Only reconsider a dedicated cross-domain schema if 2-3+ tables genuinely belong to no single domain (e.g. if `oraculo`'s CSV-based scores, which already mix BR+US in one file, ever migrate to MySQL) — don't recreate one preemptively for a single table.

## Naming convention: theme prefix, not schema/stage

Table names are prefixed by macro theme, independent of schema or computation stage — the prefix classifies what the data *is*.

`macro_brasil`:
```
atv_    — real activity (GDP, industrial production, retail, services, IBC-Br)
mt_     — labor market (PNAD, CAGED) — kept its unabbreviated prefix
cred_   — credit and household/corporate financial conditions
cmb_    — FX and its determinants (reserves, BOP, flow, terms of trade, contracted FX)
inflc_  — IPCA/IPCA-15 (aggregates, subitem decomposition, dimension table)
expc_   — market expectations (Focus)
fisc_   — fiscal (public debt, NFSP, RTN revenue/expenditure)
```

`macro_international`:
```
cmb_    — FX: cmb_reer, cmb_cot_fx, cmb_dollar_index, cmb_dollar_index_em, cmb_policy_rates,
           cmb_real_rates
(none)  — diferenciais_juros: the one table in this schema with no prefix,
           by explicit user instruction — not "cmb_diferenciais_juros"
```

`diferenciais_juros` is deliberately unprefixed despite being FX/rate-themed — don't add `cmb_` to it in a future cleanup without reconfirming. A table only gets a prefix if the theme helps group it visually among others in the same schema.

Renaming a table never touches its columns/data — only `RENAME TABLE` plus updating the script/file name and every consumer to match.

## Active tables (`macro_brasil`)

| Table | Source | Available range | Script |
|---|---|---|---|
| `atv_pim` | IBGE 8888 (seções e atividades CNAE — indústria geral/extrativas/transformação + 24 divisões CNAE da transformação, ver docstring do script) | 2002 → today | `brasil/ibge/atv_pim.py` |
| `atv_pim_uso` | IBGE 8887 (grandes categorias econômicas / categoria de uso — bens de capital/intermediários/consumo e subcategorias, perspectiva complementar a `atv_pim`, ver `analytics/economic_activity/CLAUDE.md`) | 2002 → today | `brasil/ibge/atv_pim_uso.py` |
| `atv_pib` | IBGE 1620/1621 | 2016 → today | `brasil/ibge/atv_pib.py` |
| `atv_pib_valores_correntes` | IBGE 1846 (mesmas categorias de `atv_pib` + `variacao_estoque`, único category exclusivo desta tabela — em R$ milhões a preços correntes, não índice de volume nem preços de um ano fixo; NSA apenas, sem par SA. Insumo para o peso anual usado na decomposição/contribuição de crescimento — método "alternativo ad hoc" da Nota Técnica do BCB nº 46, ver `analytics/economic_activity/CLAUDE.md`) | 1996 → today | `brasil/ibge/atv_pib_valores_correntes.py` |
| `atv_pib_taxas` | IBGE 5932 (4 taxas oficiais por categoria: `yoy`, `acum_4t`, `acum_ano`, `qoq` — ver docstring do script) | 1996 → today | `brasil/ibge/atv_pib_taxas.py` |
| `atv_pmc` | IBGE 8880/8881/8883 | 2023 → today | `brasil/ibge/atv_pmc.py` |
| `atv_pms` | IBGE 8688 | 2023 → today | `brasil/ibge/atv_pms.py` |
| `atv_ibcbr` | BCB SGS (12 series) | 2003 → today | `brasil/bcb/atv_ibcbr.py` |
| `mt_pnad` | IBGE 6318/6320/6323/6379/6380/6381/6387/6388/6389/6390/6391/6392/6393/5944/6438/6439/6440/6441/6785/6807/8501/8513/3919 (ocupação, força de trabalho, subutilização, informalidade, rendimento, massa salarial, taxas/níveis agregados — ver docstring do script) | 2012-03 → today (confirmado ao vivo contra o banco, 2026-08; corrigido de "2024" que estava desatualizado) | `brasil/ibge/mt_pnad.py` |
| `mt_pnad_trimestral` | IBGE 24 agregados (4093-6406, pesquisa DD — cortes por sexo, grupo de idade, nível de instrução, cor/raça, posição na ocupação, atividade e grupamento ocupacional que a mensal não tem; ver docstring do script para a lista completa e o que ficou fora nesta rodada) | 2012-01 → today, só nível Brasil (N1) — nível UF/N3, suportado pela API para quase todos esses agregados, ficou fora deliberadamente nesta rodada (multiplicaria o volume por ~27x) | `brasil/ibge/mt_pnad_trimestral.py` |
| `mt_caged` | BCB SGS (14 series) | 1992 → today | `brasil/bcb/mt_caged.py` |
| `mt_caged_setor` | MTE/PDET, microdado do Novo CAGED via FTP (saldo/admissões/desligamentos por seção CNAE 2.0 — 22 seções) | 2020-01 → today | `brasil/mte/mt_caged_setor.py` (rodar via `mt_caged_novo.py`) |
| `mt_caged_uf` | Idem, por UF (27 + "NI") | 2020-01 → today | `brasil/mte/mt_caged_uf.py` (idem) |
| `mt_caged_salario` | Idem, por faixa de salário em múltiplos do salário mínimo vigente (10 bandas + `nao_identificado`) | 2020-01 → today | `brasil/mte/mt_caged_salario.py` (idem) |
| `cred_credito_amplo` | BCB SGS (17 series) | 2013 → today | `brasil/bcb/cred_credito_amplo.py` |
| `cred_credito_resumo` | BCB SGS (84 series = 72 [8 metrics × 3 recurso [total/livre/direcionado] × 3 segmento [pj/pf/total] — saldo, concessão, concessão SA, taxa de juros, spread, ICC, inadimplência, % PIB] + 12 [taxa de juros/spread × recurso [não rotativo/livre não rotativo] × segmento] from Tabela 14's "crédito não rotativo" cut; codes sourced from BCB's "Tabelas de Estatísticas Monetárias e de Crédito" Tabelas 3-5 and 14, Tabela 2 confirmed fully redundant with 3-5 and not replicated, Tabela 14's "taxa de captação" columns have no SGS code at all (confirmed live, not an extraction bug) — see script docstring) | pct_pib_total_total 1995-07, saldo_total_total 1988-06, most others 2007-03 or 2011-03, ICC-suffixed 2013-01, não-rotativo 2011-03 → today | `brasil/bcb/cred_credito_resumo.py` |
| `cred_credito_familias` | BCB SGS (5 series — household debt/income, incl./excl. mortgage debt) | 2005 → today | `brasil/bcb/cred_credito_familias.py` |
| `cred_inadimplencia_pj` | BCB SGS (5 series — Selic + corporate credit-stress proxies: inadimplência, atraso, taxa de juros, concessão; PTCC removida em 2026-08, ver `cred_ptc`) | Selic 1986-08, demais 2011-03 → today | `brasil/bcb/cred_inadimplencia_pj.py` |
| `cred_modalidade_livre_pj` | BCB SGS (saldo/concessão/taxa média/inadimplência por modalidade específica de crédito — capital de giro, cartão, cheque especial, ACC, arrendamento etc. — Pessoa Jurídica, recursos livres; ver `analytics/credit/fontes_dados.md`, Tabelas 6/10/15/19) | 1994-07 (saldo) / 2011-03 (demais) → today | `brasil/bcb/cred_modalidade_livre_pj.py` |
| `cred_modalidade_livre_pf` | Idem, Pessoa Física (consignado por origem, cartão, cheque especial, veículos etc.; Tabelas 7/11/16/20) | 1994-07 (saldo) / 2011-03 (demais) → today | `brasil/bcb/cred_modalidade_livre_pf.py` |
| `cred_modalidade_direcionado_pj` | Idem, recursos direcionados, Pessoa Jurídica (BNDES, rural, imobiliário; Tabelas 8/12/17/21) | 2007-03 → today | `brasil/bcb/cred_modalidade_direcionado_pj.py` |
| `cred_modalidade_direcionado_pf` | Idem, recursos direcionados, Pessoa Física (imobiliário, rural, BNDES, microcrédito; Tabelas 9/13/18/22) | 2007-03 → today | `brasil/bcb/cred_modalidade_direcionado_pf.py` |
| `cred_credito_porte` | BCB SGS (10 series — saldo/inadimplência/saldo de maior risco a PJ por porte de empresa, MPMe/Grande; Tabela 23) | 2012-01 → today | `brasil/bcb/cred_credito_porte.py` |
| `cred_credito_atividade_economica` | BCB SGS (38 series — saldo por atividade econômica, agropecuária + ~17 subsetores industriais + ~15 de serviços; Tabela 24) | 2012-01 → today | `brasil/bcb/cred_credito_atividade_economica.py` |
| `cred_credito_tipo_cliente` | BCB SGS (7 series — saldo por tipo de cliente, setor privado PJ/PF × setor público federal/estadual-municipal; Tabela 25) | 2012-01 → today | `brasil/bcb/cred_credito_tipo_cliente.py` |
| `cred_credito_controle_capital` | BCB SGS (9 series — saldo/inadimplência/provisões por controle de capital da instituição, públicas/privadas nacionais/estrangeiras; Tabela 26) | 1988-06 → today | `brasil/bcb/cred_credito_controle_capital.py` |
| `cred_ptc` | BCB SGS (16 series — Pesquisa Trimestral de Condições de Crédito: 4 segmentos [grandes empresas/MPME/PF consumo/PF habitacional] × oferta/demanda × observada/esperada; índice de difusão, equivalente ao Senior Loan Officer Opinion Survey do Fed. Substitui os códigos 21397/21399/21401/21403 usados antes em `cred_inadimplencia_pj`/`painel_setores.py`, que ficaram congelados desde 2022-10 — o BCB não descontinuou a pesquisa, só trocou de código; corrigido em 2026-08) | 2011-04 → today (trimestral) | `brasil/bcb/cred_ptc.py` |
| `inflc_agregados` | BCB SGS (33 series — IPCA/IPCA-15 + cores) | 1980 → today | `brasil/bcb/inflc_agregados.py` |
| `inflc_decomposicao` | IBGE, one aggregate per weighting-structure vintage — see `analytics/inflation/CLAUDE.md` (subitem: monthly var/weights/contribution) | IPCA 1999-08 / IPCA-15 2000-05 → today | `brasil/ibge/inflc_decomposicao.py` |
| `inflc_decomposicao_item` | Same as above, one hierarchy level coarser (item, 4-digit, not subitem/7-digit) — feeds MA/MS/DP núcleos only, see `analytics/inflation/CLAUDE.md` | IPCA 1999-08 / IPCA-15 2000-05 → today | `brasil/ibge/inflc_decomposicao_item.py` |
| `inflc_dim` | Subitem → Group/Subgroup/Item + tradable/non-tradable (`comercializavel`, added 2026-08) + core-inflation flag, all from BCB's official NT-57 vector (see `analytics/inflation/CLAUDE.md`) | — (no date) | `brasil/ibge/inflc_dim.py` |
| `expc_focus` | BCB Focus (IPCA 12m/24m, IGP-M, Selic) | 2001 → today | `brasil/bcb/expc_focus.py` |
| `atv_pib_usd` | BCB SGS 4385 (monthly GDP in USD) | — → today | `brasil/bcb/atv_pib_usd.py` |
| `comm_icbr` | BCB SGS 27574-27577 (IC-Br + 3 sub-indices) | 1998-02 → today | `brasil/bcb/comm_icbr.py` |
| `inflc_meta` | BCB SGS 13521 (CMN inflation target) | 1999 → today | `brasil/bcb/inflc_meta.py` |
| `cmb_risco_pais` | investing.com (manual CSV export, Brazil 5Y CDS USD) | 2007-12 → today (gap: 2015-12-02→2015-12-31, real gap in source exports) | `brasil/investing/cmb_risco_pais.py` |
| `fisc_divida` | BCB SGS (6 series — DBGG bruta + DLSP líquida, total e por nível de governo, % PIB) | 2001-12 → today | `brasil/bcb/fisc_divida.py` |
| `fisc_nfsp` | BCB SGS (16 series — NFSP primário/nominal/juros, % PIB acum. 12m [10, incl. 5 por esfera] + fluxo mensal bruto R$ mi não acumulado [6, total + 5 por esfera, 2026-08 — alimenta o ajuste sazonal STL do impulso fiscal em `analytics/fiscal_policy/`]) | 1991-12 → today (varia por série) | `brasil/bcb/fisc_nfsp.py` |
| `fisc_rtn` | Tesouro Nacional, RTN (164 séries — receita/despesa/resultado do Governo Central por rubrica orçamentária, R$ milhões) — ver `analytics/fiscal_policy/CLAUDE.md` | 1997-01 → today | `brasil/tesouro/fisc_rtn.py` |
| `fisc_efgg` | Tesouro Nacional, EFGG — Estatísticas Fiscais do Governo Geral (108 séries GFSM 2014 por natureza econômica, não rubrica — 16 códigos de despesa [remuneração de empregados, transferências, investimento líquido etc.] + 11 códigos de receita [impostos por tipo, contribuições sociais, transferências/doações, outras receitas, adicionados 2026-08] — por esfera Central/Estados/Municípios + `geral` = soma das três, R$ milhões, trimestral) — fonte da IEG, ver `analytics/fiscal_policy/reference/rtn_vs_efgg.md` | 2010-I → today (Central sozinho vai até 2006-01, mas `geral` fica limitado pelo início de Estados/Municípios) | `brasil/tesouro/fisc_efgg.py` |

`cmb_*` FX tables in `macro_brasil` (reserves, BOP, flow, terms of trade, contracted FX, Comex breakdowns) plus `macro_international`'s `cmb_reer`/`cmb_cot_fx`/`diferenciais_juros` are documented in [`analytics/exchange_rate/CLAUDE.md`](../../analytics/exchange_rate/CLAUDE.md) instead, since that's where they're actually consumed.

`inflc_agregados` has native MySQL documentation: `COMMENT` on the table and on the `name` column (lists every series with its SGS code) — see `SHOW CREATE TABLE inflc_agregados` or the Workbench table editor.

## Primary key patterns

All tables use a natural composite key (no synthetic `id`):

```sql
-- Seasonally adjusted series
PRIMARY KEY (date, name, seasonal_adjs)   -- atv_pim, atv_pim_uso, atv_pib, atv_pmc, atv_pms

-- Not seasonally adjusted
PRIMARY KEY (date, name)                  -- inflc_agregados, mt_caged, cred_credito_amplo, atv_ibcbr, cred_credito_familias, atv_pib_valores_correntes, fisc_divida, fisc_nfsp, fisc_rtn, fisc_efgg, cred_inadimplencia_pj, cred_credito_resumo, cred_credito_atividade_economica, cred_credito_tipo_cliente
PRIMARY KEY (date, name, region)          -- mt_pnad

-- Novo CAGED por corte x metrica (uma tabela por corte, cortes independentes e
-- nao cruzados entre si -- decisao explicita do usuario, 2026-08: cada tabela e
-- um total nacional por aquele corte, nao uma grade setor x UF x salario)
PRIMARY KEY (date, categoria, metrica)    -- mt_caged_setor, mt_caged_uf, mt_caged_salario
                                          -- (metrica = saldo | admissoes | desligamentos;
                                          --  date = competencia de MOVIMENTACAO, nao de declaracao)

-- Credit by modality/cut x metric (each cell's underlying SGS code differs by
-- BOTH dimensions, not derivable from one alone — see cred_modalidade_*'s own
-- docstrings for which BCB workbook tabelas feed which metrica)
PRIMARY KEY (date, modalidade, metrica)   -- cred_modalidade_livre_pj, cred_modalidade_livre_pf, cred_modalidade_direcionado_pj, cred_modalidade_direcionado_pf (metrica = saldo | concessao | taxa_media | inadimplencia)
PRIMARY KEY (date, porte, metrica)        -- cred_credito_porte (porte = mpme | grande | total; metrica = saldo | inadimplencia | saldo_maior_risco | saldo_maior_risco_res4966)
PRIMARY KEY (date, controle, metrica)     -- cred_credito_controle_capital (controle = publicas | privadas_nacionais | estrangeiras; metrica = saldo | inadimplencia | provisoes)

-- Focus expectations
PRIMARY KEY (date, indicador, horizonte)  -- expc_focus

-- Multiple named rates per category, no seasonal_adjs column (each rate is inherently
-- NSA or SA by its own definition, not a dimension of the table)
PRIMARY KEY (date, name, indicador)       -- atv_pib_taxas (indicador = yoy | acum_4t | acum_ano | qoq)

-- IPCA by subitem
PRIMARY KEY (date, indice, subitem_codigo) -- inflc_decomposicao (indice = IPCA | IPCA15; codigo = 7-digit IBGE code, not "code + name" text — see analytics/inflation/CLAUDE.md)
PRIMARY KEY (subitem_codigo)               -- inflc_dim (dimension table, no date)

-- IPCA by item (one level coarser than subitem — 4-digit, not 7-digit)
PRIMARY KEY (date, indice, item_codigo)    -- inflc_decomposicao_item

-- Cross-country, one value per country
PRIMARY KEY (date, country_code)          -- cmb_policy_rates
PRIMARY KEY (date, country_code, reer_type) -- cmb_reer
PRIMARY KEY (date, country_code, name)    -- cmb_real_rates (name = policy_rate | cpi_yoy | real_rate_ex_post)
```

`ON DUPLICATE KEY UPDATE` on insert makes it an idempotent upsert.
