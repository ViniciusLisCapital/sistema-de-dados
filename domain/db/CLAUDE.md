# domain/db/ — Context for Claude

ETL scripts that populate `macro_brasil` (`brasil/`), `macro_international` (`international/`) and `macro_us` (`us/`) on the MySQL server at `192.168.15.200` (credentials in `.env`, never hardcoded). See [`.claude/rules/domain-scripts.md`](../../.claude/rules/domain-scripts.md) for the shared `run()`-only script pattern.

One subfolder per **source**, not per theme: `brasil/` has `ibge/`, `bcb/`, `tesouro/`, `mdic/`, `mte/`, `ipea/` (só `cmb_termos_troca` — séries que o SGS não tem) and `investing/` (só `cmb_risco_pais` — CSV exportado à mão, o único script aqui sem connector); `international/` has `bis/`, `cftc/`, `fred/`, `noaa/`, `yfinance/`; `us/` has `inflation/`. A table's schema follows the rule below, not the folder it's loaded from — `cmb_termos_troca` comes from IPEA and still lives in `macro_brasil`.

## `registry.py` — tabela → script

`domain/db/registry.py` answers "I want to refresh only these tables, which scripts do I run?" — used by
`jobs/update_db.py --group/--tables/--continuous` and by the update button in
[`analytics/release_calendar/`](../../analytics/release_calendar/CLAUDE.md).

**Derived from the naming convention, not maintained by hand.** Every script here declares
`_TABLE = "<name>"` (or `TABLE`) inside a file of exactly that name — 71 of 71 comply, and
`validar()` raises if a new one doesn't, so the map complains instead of silently going stale. The scan
reads files with a regex rather than importing, since importing 71 modules would pull in
pandas/mysql/requests just to build a dict; the import happens only in `carregar()`, for the module
about to run.

```powershell
uv run python -m domain.db.registry     # lista o mapa e valida a convencao
```

One override: the three Novo CAGED cut tables (`mt_caged_setor`/`_uf`/`_salario`) map to the
**orchestrator** `mt_caged_novo`, not to their own modules — those have working `run()`s, but running
them separately would download the same ~50MB/month from the FTP three times.
`scripts_para_tabelas()` therefore collapses those three tables into one script, and returns any
unmappable table in a separate `sem_script` list rather than skipping it silently.

## Schema criterion: domain/geography, not raw-vs-computed

A table's schema depends only on which countries' data it needs — never on whether it's raw or derived.

```
macro_brasil        — anything Brazil-specific (BCB, IBGE), raw or computed
macro_international — anything needing data from 2+ countries to exist or make sense
macro_us            — US-only data that isn't just an input to an international series
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
pm_     — monetary policy: BCB's own model estimates, published projections, and the policy
          decision itself — not observed series (pm_hiato_produto + pm_hiato_produto_vintages
          + pm_copom_projecoes + pm_copom_reuniao)
```

`macro_international`:
```
cmb_    — FX: cmb_reer, cmb_cot_fx, cmb_dollar_index, cmb_dollar_index_em, cmb_policy_rates,
           cmb_real_rates
(none)  — diferenciais_juros: the one table in this schema with no prefix,
           by explicit user instruction — not "cmb_diferenciais_juros"
```

`macro_us`:
```
inflc_  — CPI (levels, the two item trees, relative importance) and PCE (price index +
          nominal spending, the BEA tree). Same prefix on purpose: both are consumer
          price indices, and the theme prefix classifies what the data IS, not which
          agency publishes it
```

`diferenciais_juros` is deliberately unprefixed despite being FX/rate-themed — don't add `cmb_` to it in a future cleanup without reconfirming. A table only gets a prefix if the theme helps group it visually among others in the same schema.

Renaming a table never touches its columns/data — only `RENAME TABLE` plus updating the script/file name and every consumer to match.

## Active tables (`macro_brasil`)

| Table | Source | Available range | Script |
|---|---|---|---|
| `atv_pim` | IBGE 8888 (seções e atividades CNAE — indústria geral/extrativas/transformação + 24 divisões CNAE da transformação, ver docstring do script) | 2002 → today | `brasil/ibge/atv_pim.py` |
| `atv_pim_uso` | IBGE 8887 (grandes categorias econômicas / categoria de uso — bens de capital/intermediários/consumo e subcategorias, perspectiva complementar a `atv_pim`, ver `analytics/brasil/economic_activity/CLAUDE.md`) | 2002 → today | `brasil/ibge/atv_pim_uso.py` |
| `atv_pib` | IBGE 1620/1621 | 2016 → today | `brasil/ibge/atv_pib.py` |
| `atv_pib_valores_correntes` | IBGE 1846 (mesmas categorias de `atv_pib` + `variacao_estoque`, único category exclusivo desta tabela — em R$ milhões a preços correntes, não índice de volume nem preços de um ano fixo; NSA apenas, sem par SA. Insumo para o peso anual usado na decomposição/contribuição de crescimento — método "alternativo ad hoc" da Nota Técnica do BCB nº 46, ver `analytics/brasil/economic_activity/CLAUDE.md`) | 1996 → today | `brasil/ibge/atv_pib_valores_correntes.py` |
| `atv_pib_taxas` | IBGE 5932 (4 taxas oficiais por categoria: `yoy`, `acum_4t`, `acum_ano`, `qoq` — ver docstring do script) | 1996 → today | `brasil/ibge/atv_pib_taxas.py` |
| `atv_renda_poupanca` | IBGE 2072 (Contas econômicas trimestrais — 12 linhas encadeadas, sem classificação própria: PIB → itens líquidos com o exterior → Renda Nacional Bruta → Renda Nacional Disponível Bruta → (−) consumo → Poupança Bruta → itens de capital → Capacidade/Necessidade Líquida de Financiamento. Cascata linear de subtotais, não uma árvore que ramifica. R$ milhões correntes, NSA apenas — sem par SA neste agregado) | 2000-I → today | `brasil/ibge/atv_renda_poupanca.py` |
| `atv_pmc` | IBGE 8880/8881/8883 | 2023 → today | `brasil/ibge/atv_pmc.py` |
| `atv_pms` | IBGE 8688 | 2023 → today | `brasil/ibge/atv_pms.py` |
| `atv_ibcbr` | BCB SGS (12 series) | 2003 → today | `brasil/bcb/atv_ibcbr.py` |
| `atv_pib_mensal` | BCB SGS 4380/4382 (2 séries — PIB mensal e PIB acumulado 12m, R$ milhões correntes). O `pib_acum_12m` é **o mesmo denominador que o próprio BCB usa** para publicar `cred_credito_resumo.pct_pib_*` (confirmado ao vivo: saldo / pib_acum_12m × 100 reproduz `pct_pib_total_total` exatamente, 55,76% em 2026-06) — por isso é ele que sustenta todo `% PIB` calculado na camada de consumo (`credit/transforms.py::compute_pct_pib`, `fiscal_policy/`). Distinto de `atv_pib_usd` (SGS 4385, em dólar, para o toggle % PIB do Balanço de Pagamentos) — séries e propósitos separados | ver script (`run(n_meses=36)` por default) | `brasil/bcb/atv_pib_mensal.py` |
| `mt_pnad` | IBGE 6318/6320/6323/6379/6380/6381/6387/6388/6389/6390/6391/6392/6393/5944/6438/6439/6440/6441/6785/6807/8501/8513/3919 (ocupação, força de trabalho, subutilização, informalidade, rendimento, massa salarial, taxas/níveis agregados — ver docstring do script) | 2012-03 → today (confirmado ao vivo contra o banco, 2026-08; corrigido de "2024" que estava desatualizado) | `brasil/ibge/mt_pnad.py` |
| `mt_pnad_trimestral` | IBGE 24 agregados (4093-6406, pesquisa DD — cortes por sexo, grupo de idade, nível de instrução, cor/raça, posição na ocupação, atividade e grupamento ocupacional que a mensal não tem; ver docstring do script para a lista completa e o que ficou fora nesta rodada) | 2012-01 → today, só nível Brasil (N1) — nível UF/N3, suportado pela API para quase todos esses agregados, ficou fora deliberadamente nesta rodada (multiplicaria o volume por ~27x) | `brasil/ibge/mt_pnad_trimestral.py` |
| `mt_caged` | BCB SGS (14 series) — **ESTOQUE** de vínculos formais celetistas, total e por setor (taxonomia própria do BCB, distinta das 22 seções CNAE do microdado). Não é saldo/fluxo: a diferença mensal desta série é que reproduz o saldo (confirmado ao vivo, 2026-08: bate exatamente com `mt_caged_setor`). Rotulagem corrigida em 2026-08, tem `COMMENT` nativo | 1992 → today | `brasil/bcb/mt_caged.py` |
| `mt_caged_setor` | MTE/PDET, microdado do Novo CAGED via FTP (saldo/admissões/desligamentos por seção CNAE 2.0 — 22 seções) | 2020-01 → today | `brasil/mte/mt_caged_setor.py` (rodar via `mt_caged_novo.py`) |
| `mt_caged_uf` | Idem, por UF (27 + "NI") | 2020-01 → today | `brasil/mte/mt_caged_uf.py` (idem) |
| `mt_caged_salario` | Idem, por faixa de salário em múltiplos do salário mínimo vigente (10 bandas + `nao_identificado`) | 2020-01 → today | `brasil/mte/mt_caged_salario.py` (idem) |
| `cred_credito_amplo` | BCB SGS (17 series) | 2013 → today | `brasil/bcb/cred_credito_amplo.py` |
| `cred_credito_resumo` | BCB SGS (84 series = 72 [8 metrics × 3 recurso [total/livre/direcionado] × 3 segmento [pj/pf/total] — saldo, concessão, concessão SA, taxa de juros, spread, ICC, inadimplência, % PIB] + 12 [taxa de juros/spread × recurso [não rotativo/livre não rotativo] × segmento] from Tabela 14's "crédito não rotativo" cut; codes sourced from BCB's "Tabelas de Estatísticas Monetárias e de Crédito" Tabelas 3-5 and 14, Tabela 2 confirmed fully redundant with 3-5 and not replicated, Tabela 14's "taxa de captação" columns have no SGS code at all (confirmed live, not an extraction bug) — see script docstring) | pct_pib_total_total 1995-07, saldo_total_total 1988-06, most others 2007-03 or 2011-03, ICC-suffixed 2013-01, não-rotativo 2011-03 → today | `brasil/bcb/cred_credito_resumo.py` |
| `cred_credito_familias` | BCB SGS (5 series — household debt/income, incl./excl. mortgage debt) | 2005 → today | `brasil/bcb/cred_credito_familias.py` |
| `cred_inadimplencia_pj` | BCB SGS (5 series — Selic + corporate credit-stress proxies: inadimplência, atraso, taxa de juros, concessão; PTCC removida em 2026-08, ver `cred_ptc`) | Selic 1986-08, demais 2011-03 → today | `brasil/bcb/cred_inadimplencia_pj.py` |
| `cred_modalidade_livre_pj` | BCB SGS (saldo/concessão/taxa média/inadimplência por modalidade específica de crédito — capital de giro, cartão, cheque especial, ACC, arrendamento etc. — Pessoa Jurídica, recursos livres; ver `analytics/brasil/credit/fontes_dados.md`, Tabelas 6/10/15/19) | 1994-07 (saldo) / 2011-03 (demais) → today | `brasil/bcb/cred_modalidade_livre_pj.py` |
| `cred_modalidade_livre_pf` | Idem, Pessoa Física (consignado por origem, cartão, cheque especial, veículos etc.; Tabelas 7/11/16/20) | 1994-07 (saldo) / 2011-03 (demais) → today | `brasil/bcb/cred_modalidade_livre_pf.py` |
| `cred_modalidade_direcionado_pj` | Idem, recursos direcionados, Pessoa Jurídica (BNDES, rural, imobiliário; Tabelas 8/12/17/21) | 2007-03 → today | `brasil/bcb/cred_modalidade_direcionado_pj.py` |
| `cred_modalidade_direcionado_pf` | Idem, recursos direcionados, Pessoa Física (imobiliário, rural, BNDES, microcrédito; Tabelas 9/13/18/22) | 2007-03 → today | `brasil/bcb/cred_modalidade_direcionado_pf.py` |
| `cred_credito_porte` | BCB SGS (10 series — saldo/inadimplência/saldo de maior risco a PJ por porte de empresa, MPMe/Grande; Tabela 23) | 2012-01 → today | `brasil/bcb/cred_credito_porte.py` |
| `cred_credito_atividade_economica` | BCB SGS (38 series — saldo por atividade econômica, agropecuária + ~17 subsetores industriais + ~15 de serviços; Tabela 24) | 2012-01 → today | `brasil/bcb/cred_credito_atividade_economica.py` |
| `cred_credito_tipo_cliente` | BCB SGS (7 series — saldo por tipo de cliente, setor privado PJ/PF × setor público federal/estadual-municipal; Tabela 25) | 2012-01 → today | `brasil/bcb/cred_credito_tipo_cliente.py` |
| `cred_credito_controle_capital` | BCB SGS (9 series — saldo/inadimplência/provisões por controle de capital da instituição, públicas/privadas nacionais/estrangeiras; Tabela 26) | 1988-06 → today | `brasil/bcb/cred_credito_controle_capital.py` |
| `cred_ptc` | BCB SGS (16 series — Pesquisa Trimestral de Condições de Crédito: 4 segmentos [grandes empresas/MPME/PF consumo/PF habitacional] × oferta/demanda × observada/esperada; índice de difusão, equivalente ao Senior Loan Officer Opinion Survey do Fed. Substitui os códigos 21397/21399/21401/21403 usados antes em `cred_inadimplencia_pj`/`painel_setores.py`, que ficaram congelados desde 2022-10 — o BCB não descontinuou a pesquisa, só trocou de código; corrigido em 2026-08) | 2011-04 → today (trimestral) | `brasil/bcb/cred_ptc.py` |
| `inflc_agregados` | BCB SGS (33 series — IPCA/IPCA-15 + cores) | 1980 → today | `brasil/bcb/inflc_agregados.py` |
| `inflc_decomposicao` | IBGE, one aggregate per weighting-structure vintage — see `analytics/brasil/inflation/CLAUDE.md` (subitem: monthly var/weights/contribution) | IPCA 1999-08 / IPCA-15 2000-05 → today | `brasil/ibge/inflc_decomposicao.py` |
| `inflc_decomposicao_item` | Same as above, one hierarchy level coarser (item, 4-digit, not subitem/7-digit) — feeds MA/MS/DP núcleos only, see `analytics/brasil/inflation/CLAUDE.md` | IPCA 1999-08 / IPCA-15 2000-05 → today | `brasil/ibge/inflc_decomposicao_item.py` |
| `inflc_dim` | Subitem → **two independent classification axes**. BCB analytical: Group/Subgroup/Item + tradable/non-tradable (`comercializavel`, added 2026-08) + core-inflation flags, all from BCB's official NT-57 vector. IBGE expenditure: `ibge_grupo`/`ibge_subgrupo`/`ibge_item` (added 2026-08) — the parentage is the 7-digit code's own 1/2/4-digit prefix, only the names come from SIDRA. Neither derives from the other (see `analytics/brasil/inflation/CLAUDE.md`) | — (no date) | `brasil/ibge/inflc_dim.py` |
| `expc_focus` | BCB Focus/Olinda, **horizonte móvel** — IPCA + 5 componentes (Livres/Administrados/Serviços/Bens industrializados/Alimentação no domicílio) a 12m e 24m, mais IGP-M a 12m. Cada série em 4 variantes: `suavizada` S/N × `base_calculo` 0/1 — ver docstring do script | IPCA/IGP-M 12m 2001-11 (não suavizado) / 2001-12 (suavizado); IPCA 24m 2021-03; componentes 2021-09 → today | `brasil/bcb/expc_focus.py` |
| `expc_focus_copom` | BCB Focus/Olinda, **Selic esperada por reunião do Copom** — ~16 reuniões à frente por data de pesquisa, ou seja a curva de política monetária implícita no consenso. `base_calculo` 0 e 1. Substituiu as 5.458 linhas de `indicador='Selic'`/`horizonte='eop'` que a `expc_focus` colapsava (uma por data, sem coluna `reuniao`; a sobrevivente era a reunião mais distante, de painel mais fino) — apagadas em 2026-08, nenhum consumidor as lia | 2004-11 → today | `brasil/bcb/expc_focus_copom.py` |
| `expc_focus_periodo` | BCB Focus/Olinda, **período de referência fixo** (o Boletim Focus propriamente dito) — 3 periodicidades × 26 indicadores vivos: IPCA e componentes, IGP-M, Câmbio, Selic, Taxa de desocupação, PIB total/setores/componentes de demanda, Resultado primário/nominal, Dívida bruta/líquida, Conta corrente, Balança comercial (3 detalhes), IED. **Duas datas independentes** (`date` = quando perguntaram, `data_referencia` = sobre qual período), o que é o que permite a história da revisão. Só `base_calculo` 0. Unidades heterogêneas, ver coluna `unidade` | anual 1999-04, mensal 2000-01, trimestral 2001-11 → today (indicadores da reformulação de 2021-09 começam ali) | `brasil/bcb/expc_focus_periodo.py` |
| `atv_pib_usd` | BCB SGS 4385 (monthly GDP in USD) | — → today | `brasil/bcb/atv_pib_usd.py` |
| `comm_icbr` | BCB SGS 27574-27577 (IC-Br + 3 sub-indices) | 1998-02 → today | `brasil/bcb/comm_icbr.py` |
| `comm_icbr_usd` | BCB SGS 29042 (1 série — IC-Br em **USD**). O `comm_icbr` (27574 etc.) é denominado em **reais**, o que o torna endógeno ao próprio USD/BRL e portanto inadequado como regressor num modelo que explica o USD/BRL — adequado, sim, para a curva de Phillips, onde o repasse cambial é parte do que se quer capturar. Esta é a versão USD-neutra: melhorou o MSE out-of-sample do `ridge_deviation_model` em ~4,6% isoladamente (2026-07-31) | 1998-01 → today (`start="all"`) | `brasil/bcb/comm_icbr_usd.py` |
| `inflc_meta` | BCB SGS 13521 (CMN inflation target) | 1999 → today | `brasil/bcb/inflc_meta.py` |
| `cmb_risco_pais` | investing.com (manual CSV export, Brazil 5Y CDS USD) | 2007-12 → today (gap: 2015-12-02→2015-12-31, real gap in source exports) | `brasil/investing/cmb_risco_pais.py` |
| `fisc_divida` | BCB SGS (6 series — DBGG bruta + DLSP líquida, total e por nível de governo, % PIB) | 2001-12 → today | `brasil/bcb/fisc_divida.py` |
| `fisc_nfsp` | BCB SGS (16 series — NFSP primário/nominal/juros, % PIB acum. 12m [10, incl. 5 por esfera] + fluxo mensal bruto R$ mi não acumulado [6, total + 5 por esfera, 2026-08 — alimenta o ajuste sazonal STL do impulso fiscal em `analytics/brasil/fiscal_policy/`]) | 1991-12 → today (varia por série) | `brasil/bcb/fisc_nfsp.py` |
| `fisc_dlsp_fatores` | BCB, tabela especial `Facdetp.xlsx` (**não existe no SGS** — ver `connectors/bcb_tabelas_especiais.py`): fatores condicionantes da DLSP, detalhamento por item. 95 itens × 9 fatores = 855 séries (1 estoque + 8 fluxos: primário, juros, ajuste met. interno/externo, paridade, caixa-competência, reconhecimento de dívidas, privatizações), R$ milhões. Identidade `estoque[t]−estoque[t−1] = Σ 8 fluxos[t]` validada célula a célula. **Sinal "necessidade de financiamento" — fluxo positivo aumenta a dívida, logo `primario` positivo = déficit, oposto de `fisc_nfsp`** | 2001-12 → today (mensal) | `brasil/bcb/fisc_dlsp_fatores.py` |
| `pm_hiato_produto` | BCB, anexo estatístico do RPM (**não existe no SGS** — ver `connectors/bcb_rpm.py`): hiato do produto, edição corrente. `central` (Cenário de referência) + `minimo`/`p25`/`p75`/`maximo` (dispersão entre modelos). % do produto potencial, nível — não anualizar. Recarregada com truncate a cada edição, `vintage` registra de qual | 2003-IV → trimestre de referência da edição (trimestral) | `brasil/bcb/pm_hiato_produto.py` |
| `pm_copom_projecoes` | BCB, **texto de duas publicações**, distinguidas pela coluna `documento` (nada disso existe no SGS nem no Focus): o **comunicado** de decisão (`connectors/bcb_copom.py`), que publica 2 ou 3 períodos escolhidos, e o **Relatório de Política Monetária** (`connectors/bcb_rpm.py`; chamado Relatório de Inflação até 2024-12), que sai 7 a 28 dias depois da mesma reunião e publica o **caminho trimestral contíguo inteiro**. É o que o BC projeta, não o que o mercado espera (`expc_focus*`), e por isso a única forma de medir o gap projeção-oficial-vs-meta. `horizonte_relevante` marca o ponto do horizonte que o Comitê persegue, com `regime` dizendo qual dos quatro conceitos vale ali (`hr_aproximado` = os 6 trimestres calculados por nós nas eras em que o HR de 6 trimestres não existia — só possível porque o relatório publica o caminho contíguo); `cenario` classifica pelo **condicionamento** (`juros_esperado`/`juros_constante`/`juros_decrescente`), não pelo rótulo publicado, porque "cenário de referência" significava o oposto até ~2020 — o rótulo original fica em `cenario_publicado` e a informação de fato usada em `input_juros` (`focus`/`di_swaps`/`constante`). Texto versionado em `repository/monetary_policy/raw_md/{central_bank_comunication,relatorio_politica_monetaria}/` | 2.363 linhas: comunicado reuniões 206 (2017-04-12) → 280, 396 linhas; relatório 108 das 109 edições (1999-09 → 2026-06), 1.967 linhas. Comunicados 48-205 baixados mas **fora da carga** (ver `copom_comunicados.md`); RI de 1999-06 não publica tabela numérica | `brasil/bcb/pm_copom_projecoes.py` |
| `pm_copom_reuniao` | BCB **SGS 432** (meta Selic, diária de dia corrido) cruzada com o calendário de reuniões de `connectors/bcb_copom.calendario_reunioes()`. Uma linha por reunião: o nível herdado, o decidido, e o **passo em pontos-base** — a variação daquela reunião, não o acumulado do ciclo. Contrapartida de `pm_copom_projecoes`: as duas juntas permitem ler a reação (projeção no horizonte relevante × passo de juros). O passo é o nível 5 dias corridos depois da decisão menos o vigente no dia, e cinco dias não é folga arbitrária: das 152 mudanças da série, 147 entram 1 dia depois da reunião, 4 em 2 (feriado na quinta) e 1 em 5 (20/04/2011), enquanto os **8 movimentos por viés** — até 2003 o presidente do BCB podia mover a meta entre reuniões — estão todos a 7 dias ou mais; a janela separa decisão de viés exatamente, e `alterada_fora_da_reuniao` marca as 4 reuniões cujo nível de entrada não é o que a anterior deixou. A decisão em prosa do comunicado entra como **conferência independente**, não como fonte: 63 reuniões comparadas, zero divergência | 247 reuniões, 34ª (1999-04-14) → 280ª. As reuniões 21ª-33ª ficam fora — a meta Selic não existia, o instrumento eram a TBC e a TBAN | `brasil/bcb/pm_copom_reuniao.py` |
| `pm_hiato_produto_vintages` | Mesma fonte, **todas** as edições: o que cada RI/RPM publicou para cada trimestre. É a dimensão que nenhuma outra tabela do banco tem — o que o BCB *achava* na época, não só o que acha hoje. **Quebra metodológica entre as edições 2024-06 e 2024-09** (um modelo + banda ±2 d.p. → dispersão entre modelos); só `central` é comparável entre os dois regimes | edições 2021-09 → hoje (a 1ª com anexo estatístico); trimestres 2003-II → hoje | `brasil/bcb/pm_hiato_produto_vintages.py` |
| `fisc_rtn` | Tesouro Nacional, RTN (164 séries — receita/despesa/resultado do Governo Central por rubrica orçamentária, R$ milhões) — ver `analytics/brasil/fiscal_policy/CLAUDE.md` | 1997-01 → today | `brasil/tesouro/fisc_rtn.py` |
| `fisc_investimento` | Tesouro Nacional, API de Séries Temporais, **Tema 13** (78 séries — investimento do Governo Federal por GND, R$ milhões, mensal). Dois cortes independentes do mesmo agregado: `funcao` (GND × função orçamentária, 60 séries, subtema 13.1) e `natureza` (GND × natureza da despesa, 18, subtema 13.2), que compartilham os 4 nós de cima (`total`/`gnd4`/`gnd5`/`ajuste_ordem_bancaria`) e divergem abaixo. Só os GNDs de capital — 4 Investimentos (cria ativo novo) e 5 Inversões Financeiras (só troca titularidade). Identidades `total = gnd4+gnd5+ajuste` e `pai = Σ filhos` validadas com desvio exato 0,0 | 2008-01 → today. **A metadata da API diz 1997-01 e mente**: 1997-2006 vem 0,0 em todas as 78 séries (zero = sem dado), e 2007 só tem o total do corte `funcao`, sem decomposição e contradizendo o total do corte `natureza` — `_START` corta em 2008-01 | `brasil/tesouro/fisc_investimento.py` |
| `fisc_efgg` | Tesouro Nacional, EFGG — Estatísticas Fiscais do Governo Geral (108 séries GFSM 2014 por natureza econômica, não rubrica — 16 códigos de despesa [remuneração de empregados, transferências, investimento líquido etc.] + 11 códigos de receita [impostos por tipo, contribuições sociais, transferências/doações, outras receitas, adicionados 2026-08] — por esfera Central/Estados/Municípios + `geral` = soma das três, R$ milhões, trimestral) — fonte da IEG, ver `analytics/brasil/fiscal_policy/reference/rtn_vs_efgg.md` | 2010-I → today (Central sozinho vai até 2006-01, mas `geral` fica limitado pelo início de Estados/Municípios) | `brasil/tesouro/fisc_efgg.py` |

`cmb_*` FX tables in `macro_brasil` (reserves, BOP, flow, terms of trade, contracted FX, Comex breakdowns) plus `macro_international`'s `cmb_reer`/`cmb_cot_fx`/`diferenciais_juros` are documented in [`analytics/brasil/exchange_rate/CLAUDE.md`](../../analytics/brasil/exchange_rate/CLAUDE.md) instead, since that's where they're actually consumed.

`inflc_agregados` has native MySQL documentation: `COMMENT` on the table and on the `name` column (lists every series with its SGS code) — see `SHOW CREATE TABLE inflc_agregados` or the Workbench table editor. The three `expc_focus*` tables also carry table- and column-level `COMMENT`.

📄 **Focus/Olinda — inventário de cobertura por endpoint × indicador, as 4 reformulações da pesquisa que cortam séries no meio, e volumes:** [`brasil/bcb/focus_inventario.md`](brasil/bcb/focus_inventario.md). Medido ao vivo; redescobrir custa ~100 chamadas à API e nada disso está na documentação do serviço.

📄 **Comunicados do Copom — os 5 regimes de comunicação (o que dá para extrair de cada era), a armadilha do nome do cenário que trocou de significado, os 3 conceitos de horizonte relevante, e o que a Ata acrescenta:** [`brasil/bcb/copom_comunicados.md`](brasil/bcb/copom_comunicados.md). Também medido ao vivo, varrendo as 233 reuniões que a API devolve.

📄 **Relatório de Política Monetária — os 3 formatos de tabela por era, as 5 armadilhas silenciosas do PDF (a coluna central que muda de lugar, o separador ano/trimestre, o layout de 2 colunas, a fonte de subconjunto sem cmap, o rótulo que troca de significado), a grade 2×2 de cenários de 2016-2020 e como cada edição se liga à reunião que a condiciona:** [`brasil/bcb/relatorio_politica_monetaria.md`](brasil/bcb/relatorio_politica_monetaria.md). Levantado baixando e lendo as 109 edições.

`expc_focus_pre202608` é o snapshot das 19.204 linhas da `expc_focus` antes da reescrita de 2026-08 — não é tabela de produção, nenhum script escreve ou lê dela. Já serviu: a variante `suavizada='S' AND base_calculo=0` da tabela nova reproduz as 13.746 linhas não-Selic dela **valor a valor, zero divergência** (verificado). Pode ser derrubada quando não fizer mais falta; as 5.458 linhas de Selic que ela ainda guarda são as colapsadas, sem valor analítico.

## Active tables (`macro_international`)

`cmb_reer`, `cmb_cot_fx` and `diferenciais_juros` are documented in
[`analytics/brasil/exchange_rate/CLAUDE.md`](../../analytics/brasil/exchange_rate/CLAUDE.md), where they're
consumed. The rest:

| Table | Source | Available range | Script |
|---|---|---|---|
| `cmb_policy_rates` | BIS WS_CBPOL — policy rate, **diária** (o mensal do BIS é só o fechamento da própria diária, então só a diária é guardada). BR/MX/CL/CO/PE/AR | BR truncado em **1994-07** (Plano Real, decisão explícita do usuário — o BIS cobre desde 1986-06, mas ~790.799% a.a. em 1990 não é comparável); **AR parou de ser atualizada pelo BIS em meados de 2025** — gap no fim da série é esperado, não é falha do script | `international/bis/cmb_policy_rates.py` |
| `cmb_real_rates` | BIS WS_CBPOL + WS_LONG_CPI — taxa real ex-post (policy rate − CPI YoY), mensal, BR/MX/CL/CO/PE (sem AR). **Recalcula o Brasil pela fonte/método do BIS** para comparabilidade cross-country homogênea — não substitui o `real_br_ex_post` de `diferenciais_juros`, que usa Selic meta + IPCA oficiais | Cada país começa no início da **própria** série de policy rate do BIS (o fator limitante; o CPI do BIS é bem mais longo): BR 1994-07, CO 1995-04, CL 1997-02, MX 1998-11, PE 2003-09 | `international/bis/cmb_real_rates.py` |
| `cmb_dollar_index` | Yahoo Finance `DX-Y.NYB` (ICE US Dollar Index, DXY), diário. Preferido ao FRED `DTWEXBGS`, que só cobre a partir de 2006 | 1971-01-04 → today | `international/yfinance/cmb_dollar_index.py` |
| `cmb_dollar_index_em` | FRED `DTWEXEMEGS` — dólar contra moedas de emergentes, diário | 2006-01-02 → today | `international/fred/cmb_dollar_index_em.py` |
| `cmb_fx_latam` | Yahoo Finance `MXN=X`/`CLP=X`/`COP=X`/`PEN=X` — moeda local por USD, mesma convenção do PTAX (maior = moeda local mais fraca), diário. Sem AR (mesma exclusão de `cmb_policy_rates`). Insumo de volatilidade do métrico `relative_carry_vol` em `ppp_equilibrium.py` — o papel que `cmb_ptax` cumpre do lado brasileiro | ver script | `international/yfinance/cmb_fx_latam.py` |
| `cmb_equity_us` | Yahoo Finance `^GSPC` (S&P 500, fechamento diário) — canal "competição por capital" do modelo cambial. Preferido ao FRED `SP500`, que é janela rolante de ~10 anos. Testado antes de ser ingerido: `delta_sp500` melhorou o MSE out-of-sample do `ridge_deviation_model` em ~4%, coeficiente positivo e estável nas 163 janelas; VIX e o real de 10a dos EUA foram testados junto e **não** melhoraram — não ingeridos | 1990 → today | `international/yfinance/cmb_equity_us.py` |
| `comm_brent` | FRED `DCOILBRENTEU` (Brent, USD/barril, diário) — era o cenário de choque de commodities da réplica do modelo do BCB, isolado do IC-Br Energia (que embute câmbio). **Sem consumidor** desde a remoção da réplica em 2026-08 | ver script | `international/fred/comm_brent.py` |
| `clima_oni` | NOAA CPC, texto estático (`oni.ascii.txt`, sem connector dedicado) — Oceanic Niño Index. Só as 4 estações móveis alinhadas ao calendário trimestral (JFM/AMJ/JAS/OND) das 12 que a NOAA publica, para casar com Q1-Q4 sem ambiguidade. Era insumo climático da Curva de Phillips da réplica; **sem consumidor** desde 2026-08 | ver script | `international/noaa/clima_oni.py` |

**Quem roda o quê**: `jobs/update_international.py` só cobre `cmb_reer`, `cmb_cot_fx` e
`diferenciais_juros`. As séries **diárias** desta lista (`cmb_dollar_index`,
`cmb_dollar_index_em`, `cmb_fx_latam`, `cmb_equity_us`, `comm_brent`, `cmb_policy_rates`) são
alcançadas pelo `jobs/update_db.py --continuous` — que resolve tabela→script pelo `registry.py` e
por isso não se limita a `macro_brasil`, apesar do nome do job. Sem job nenhum: `cmb_real_rates`
e `clima_oni`.

## Active tables (`macro_us`)

Built 2026-08, the first US branch. Full method, validation and gotchas:
[`us_project/inflation_hierarchy.md`](../../us_project/inflation_hierarchy.md) and each script's docstring.

| Table | Source | Available range | Script |
|---|---|---|---|
| `inflc_cpi` | BLS API v2 — CPI-U index **levels** by item, SA and NSA (340,907 rows). Variations are computed at read time, never stored | 1913-01 → today (NSA); 1947-01 → today (SA) | `us/inflation/inflc_cpi.py` |
| `inflc_cpi_dim` | `cu.item` flat file + the annual relative-importance table + the news-release HTML — **both** of the CPI's trees, keyed apart by `arvore`: `despesa` (355 items × 10 levels, the statistical structure) and `divulgacao` (37 rows × 5 levels, Table 1 of the release) | — (no date) | `us/inflation/inflc_cpi_dim.py` |
| `inflc_cpi_pesos` | `relative-importance/<year>.xlsx` — December snapshots, CPI-U and CPI-W, both sections of Table 1 (3,864 rows) | 2020-12 → 2025-12 (annual). BLS publishes back to **1947** in two older formats with no parser yet — parsing gap, not data gap | `us/inflation/inflc_cpi_pesos.py` |
| `inflc_pce` | BEA **API** (dataset `NIUnderlyingDetail`, needs `BEA_API_KEY`) since 2026-08-26 — tables 2.4.4U (chained price index, 2017=100) and 2.4.5U (nominal spending, US$ mn SAAR) for the same 402 lines, monthly, **SA only** (the BEA publishes no NSA monthly counterpart). The API is the better contract for values (typed JSON instead of a spreadsheet parser) and only sends the requested window, so the routine 3-year run costs ~6 MB against the xlsx's fixed 12 MB. `fonte="xlsx"` remains as a fallback and gives identical numbers (608,442 observations cross-checked, 0 differing). Each load re-runs that cross-check for free whenever the xlsx is already cached — see `connectors/CLAUDE.md`. 608,442 rows. `medida` in the key, not two columns: the 2 `ZZZZZZ` "net" lines have spending and no price index | 1959-01 → today | `us/inflation/inflc_pce.py` |
| `inflc_pce_dim` | **The one table in the project that is its own source of truth.** The hierarchy exists only in the xlsx — the BEA API publishes none at all (checked across every dataset in the service; 10 fields, none a parent/level/indent) — but it does not change month to month, so it is written once and thereafter **re-read from here** and re-proved against the API: same line set (number, label, and code on the index table), additivity closing in nominal over the stored parentage, levels 1–4 summing to 100%. Passing all three, only the coverage columns are rewritten. Failing any, the 12 MB xlsx is downloaded and the tree rebuilt — the file is a *repair* path, not a monthly dependency. `run(fonte="xlsx")` forces the rebuild; the API-only route was verified to produce a byte-identical table. The published **indentation** of those same two tables — 402 lines = 368 in the tree (9 levels) + 34 addenda aggregates. Keyed by BEA **line number**, because 13 series codes appear on two lines each | — (no date) | `us/inflation/inflc_pce_dim.py` |

Three things about this trio that don't generalise from the Brazil tables:

- **Weights are a separate table, not columns on the monthly rows** (unlike `inflc_decomposicao`, which
  carries `var_mensal`/`pesos`/`contribuicao` together). The BLS publishes one weight per item per
  *year*; writing it onto every month would either duplicate it twelvefold or imply a monthly weight
  that was never published. Contribution therefore becomes an explicit join decision — carry December's
  snapshot forward through the following year — made in the report, not baked into the schema.
- **`ajuste` is in the key, not a column.** Coverage is uneven: 273 items have NSA, 234 have SA. A
  `value_sa` column would be NULL for ~40 items and would imply the pair exists.
- **The expenditure tree has two layers, and `tem_peso` separates them.** 272 items come from the
  relative-importance spreadsheet and have a published weight; 83 come from `cu.item`, below the depth
  the spreadsheet publishes, and have an index but **no** weight (gasoline by grade, roasted vs. instant
  coffee, new cars vs. new trucks, smartphones). Contribution exists only for `tem_peso=1`, and the
  weight-additivity proof runs on the spreadsheet layer alone — the graft only ever adds leaves.
- **Only December weights are loaded, and the monthly ones don't need to be.** The news release prints a
  relative importance dated one month behind the reference month; it is recoverable from the December
  snapshot by multiplying by the item's own NSA index ratio over the headline's, which reproduces all 37
  printed figures to 0.0008. `analytics/us/inflation/report.html` does that in its Table 1 view rather than
  loading the release's column, so there is no monthly weight table to maintain.
- **`inflc_cpi_pesos` is keyed by name + indent level, not item_code**, because the spreadsheet doesn't
  publish a code. `item_code` is a resolved, nullable column (91% match); the unmatched rows are the
  "Unsampled …" residuals, kept on purpose because they carry weight and are real children in the
  tree's arithmetic.

`inflc_cpi_dim`'s coverage columns (`sa_begin`/`nsa_begin`/`nsa_end`) are **measured** from
`inflc_cpi`, not read from API metadata — which is why `jobs/update_us.py` runs the dim script twice,
before and after loading the levels. All five tables carry table- and column-level `COMMENT`.

The PCE pair inverts three of those CPI decisions, each time because the source is better:

- **The weight is not a separate table**, it is the `nominal` measure of `inflc_pce`. The BEA publishes
  each line's spending every month, on the same grid as the price index, so there is no annual snapshot
  to carry forward — the weight is `nominal / nominal[line 1]` and is computed at read time, like the
  variations. Measured payoff: contribution rebuilds the published headline to 0.0009 p.p. (M/M), against
  0.0124 for the CPI's December-snapshot join.
- **One dim pass, not two.** `inflc_pce_dim` measures `idx_begin`/`nom_end` from the source and does not
  depend on `inflc_pce` being loaded. It still runs *first* in the job, because it is what validates the
  structure.
- **The routine run touches no file at all** (2026-08-26). Both PCE steps go through the API; the xlsx is
  fetched only when the structural check says the tree moved. Two details that cost a debugging round
  each, both worth knowing before touching this: the API **returns a record only where there is data**,
  so on a short window the 2 `ZZZZZZ` lines (no price index, ever) and the discontinued ones (157/158,
  ended 2001-12) are legitimately absent — absence only means removal if the stored `idx_end`/`nom_end`
  says the line should still be publishing. And the BEA **SeriesCode encodes the measure**: line 1 is
  `DPCERG` in 2.4.4U and `DPCERC` in 2.4.5U. `inflc_pce_dim.code` therefore holds the *index* code, which
  is also why `_validar_casamento` compares line/label/indentation between the two sheets and never the
  code.
- **The tree is proved, and the tolerance comes from the source, not from taste.** Every parent must equal
  the sum of its children × each child's sign, in nominal, across all 810 months. The BEA rounds each line
  to whole millions, so k children against a rounded parent can differ by up to `0.5*(k+1)` by rounding
  alone; the test is that the residual fit inside that. It does, using at most 80% of the allowance (worst
  case US$ 3 mn against a US$ 20 tn total). Plus: levels 1–4 each sum to 100% of PCE and the 245 leaves to
  100.0000%. Any of these failing raises instead of writing.
- **`sinal` and `sinal_acumulado` are two different questions.** Four lines start with `Less:` and enter
  their parent negatively; **nineteen** enter the PCE negatively, because the whole subtree under a `Less:`
  inherits the sign without saying so in its label. Summing a level with only the first column gives 116%
  of PCE. Note also that a negative *value* is not the same thing: `Employee reimbursement` has negative
  spending of its own with an ordinary `+1` sign.

`domain/db/us/_gravar.py` wraps the shared insert helper with a **verified** write. It exists because
`connectors.mysql.insert_data_into_database` catches `mysql.connector.Error`, *prints* it and returns
normally — so a caller that then prints "N rows written" lies. That happened on the first
`inflc_cpi_pesos` load (a NOT NULL `weights_year` vs. BLS's biennial baskets for 2020/2021): the INSERT
died with 1048 and the script announced success into an empty table. `gravar()` re-checks in the
database and raises. Not applied to the `macro_brasil` scripts, which still have the silent-failure
behaviour — migrating that check into the shared helper is the real fix, still open.

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

-- Investimento do Governo Federal (dois cortes INDEPENDENTES do mesmo agregado,
-- nao cruzados: cada um e a decomposicao inteira por aquele criterio -- mesma
-- logica das 3 tabelas de mt_caged_*, mas numa tabela so porque vem do mesmo
-- tema/fonte e compartilham os 4 nos de cima)
PRIMARY KEY (date, corte, item)           -- fisc_investimento (corte = funcao | natureza;
                                          --  item = slug hierarquico separado por "__",
                                          --  raizes total/gnd4/gnd5/ajuste_ordem_bancaria)

-- Fatores condicionantes da DLSP (item x fator; o fator NAO e derivavel do item
-- nem vice-versa -- cada aba da planilha do BCB traz a taxonomia inteira de
-- itens, ver a docstring do script)
PRIMARY KEY (date, fator, item)           -- fisc_dlsp_fatores (fator = estoque | primario | juros
                                          --  | ajuste_met_interno | ajuste_met_externo | ajuste_paridade
                                          --  | ajuste_caixa_competencia | reconhecimento_dividas
                                          --  | privatizacoes; item = slug hierarquico separado por "__",
                                          --  3 arvores independentes: total/interna/externa)

-- Hiato do produto: a tabela corrente e uma serie normal; a de vintages carrega
-- a EDICAO na chave, porque o mesmo trimestre tem um valor por edicao publicada
PRIMARY KEY (date, variavel)              -- pm_hiato_produto (variavel = central | minimo | p25
                                          --  | p75 | maximo; `vintage` fica fora da PK, e so
                                          --  procedencia -- a tabela guarda uma edicao por vez)
PRIMARY KEY (vintage, date, variavel)     -- pm_hiato_produto_vintages (vintage = 1o dia do mes de
                                          --  publicacao, mar/jun/set/dez; variavel inclui tambem
                                          --  banda_sup/banda_inf nas edicoes ate 2024-06)

-- Projecoes do Copom: a REUNIAO entra na chave em vez da data dela, porque o
-- numero da reuniao e a identidade natural da publicacao (e o que a API indexa, e
-- o que o comunicado usa para se referir a si mesmo); `vintage` = a data dela fica
-- fora, como procedencia -- e para as linhas de relatorio `vintage` e a data de
-- PUBLICACAO da edicao, dias depois da reuniao, entao os dois documentos da mesma
-- reuniao tem vintages diferentes. `date` aqui e o periodo PROJETADO, nao o da
-- publicacao -- as duas dimensoes de tempo que uma projecao tem, mesma logica do par
-- pm_hiato_produto_vintages, so com os papeis nomeados diferente. `documento` esta na
-- chave porque comunicado e relatorio projetam o MESMO periodo com numeros proprios.
PRIMARY KEY (nro_reuniao, documento, indice, cenario, date)
                                          -- pm_copom_projecoes (documento = comunicado |
                                          --  relatorio; indice = ipca | ipca_livres |
                                          --  ipca_administrados; cenario = juros_esperado |
                                          --  juros_constante | juros_decrescente, pelo
                                          --  CONDICIONAMENTO e nao pelo rotulo publicado --
                                          --  ver o COMMENT da coluna;
                                          --  date = 1o mes do trimestre projetado, com o ano civil
                                          --  acumulado normalizado para o 4o trimestre daquele ano)

-- Decisao de Selic: a reuniao E a linha, entao a PK e ela sozinha. `date` aqui e a data
-- da DECISAO (dia 2 da reuniao), nao um periodo projetado -- diferente do papel que
-- `date` tem na pm_copom_projecoes, e a razao de as duas nao serem uma tabela so.
PRIMARY KEY (nro_reuniao)                 -- pm_copom_reuniao (decisao = elevacao | manutencao |
                                          --  reducao, derivada do sinal de variacao_bps)

-- Credit by modality/cut x metric (each cell's underlying SGS code differs by
-- BOTH dimensions, not derivable from one alone — see cred_modalidade_*'s own
-- docstrings for which BCB workbook tabelas feed which metrica)
PRIMARY KEY (date, modalidade, metrica)   -- cred_modalidade_livre_pj, cred_modalidade_livre_pf, cred_modalidade_direcionado_pj, cred_modalidade_direcionado_pf (metrica = saldo | concessao | taxa_media | inadimplencia)
PRIMARY KEY (date, porte, metrica)        -- cred_credito_porte (porte = mpme | grande | total; metrica = saldo | inadimplencia | saldo_maior_risco | saldo_maior_risco_res4966)
PRIMARY KEY (date, controle, metrica)     -- cred_credito_controle_capital (controle = publicas | privadas_nacionais | estrangeiras; metrica = saldo | inadimplencia | provisoes)

-- Focus expectations
-- Focus expectations: TRES tabelas, uma por forma de chave que a API realmente tem
-- (mesmo racional dos cortes independentes de mt_caged_*). Todas carregam as
-- dimensoes `base_calculo` (0 = janela de 30 dias, 1 = janela de 4 dias uteis;
-- NAO sao duas pesquisas, e a mesma com dois prazos de validade de submissao) e
-- `tipo_calculo` ('geral' hoje -- os endpoints Top5 tem chave identica mais essa
-- dimensao, entao carregar Top5 depois e backfill de dados, nao migracao).
-- A base 1 NAO cobre o historico todo, e isso vem da fonte: comeca em 2014-01 nos
-- endpoints de inflacao e em 2021-03 no de Selic. `expc_focus_periodo` carrega so a
-- base 0 por decisao de escopo (dobraria 1,28 M de linhas por uma leitura secundaria).
-- Tamanhos medidos apos a carga historica (2026-08): expc_focus 88.596 linhas,
-- expc_focus_copom 87.734, expc_focus_periodo 1.279.700.
PRIMARY KEY (date, indicador, horizonte, suavizada, base_calculo, tipo_calculo)
                                          -- expc_focus (horizonte = 12m | 24m,
                                          --  movel a partir da propria data da pesquisa)
PRIMARY KEY (date, reuniao, base_calculo, tipo_calculo)
                                          -- expc_focus_copom (reuniao = "R<n>/<ano>";
                                          --  a ordem cronologica NAO e alfabetica nem
                                          --  derivavel da data da pesquisa sem o
                                          --  calendario do Copom)
PRIMARY KEY (date, periodicidade, indicador, detalhe, data_referencia, base_calculo, tipo_calculo)
                                          -- expc_focus_periodo (periodicidade = mensal |
                                          --  trimestral | anual; data_referencia no
                                          --  formato do BCB, "MM/YYYY" | "Q/YYYY" |
                                          --  "YYYY", com `ref_date` derivada ao lado
                                          --  para graficar; `detalhe` = '' em tudo
                                          --  menos Balanca comercial, porque coluna de
                                          --  PK nao aceita NULL). Indice secundario
                                          --  idx_revisao (indicador, data_referencia,
                                          --  date) para a consulta OPOSTA a do PK:
                                          --  fixar o periodo previsto e varrer as datas
                                          --  de pesquisa = historia da revisao

-- Multiple named rates per category, no seasonal_adjs column (each rate is inherently
-- NSA or SA by its own definition, not a dimension of the table)
PRIMARY KEY (date, name, indicador)       -- atv_pib_taxas (indicador = yoy | acum_4t | acum_ano | qoq)

-- IPCA by subitem
PRIMARY KEY (date, indice, subitem_codigo) -- inflc_decomposicao (indice = IPCA | IPCA15; codigo = 7-digit IBGE code, not "code + name" text — see analytics/brasil/inflation/CLAUDE.md)
PRIMARY KEY (subitem_codigo)               -- inflc_dim (dimension table, no date)

-- IPCA by item (one level coarser than subitem — 4-digit, not 7-digit)
PRIMARY KEY (date, indice, item_codigo)    -- inflc_decomposicao_item

-- Cross-country, one value per country
PRIMARY KEY (date, country_code)          -- cmb_policy_rates
PRIMARY KEY (date, country_code, reer_type) -- cmb_reer
PRIMARY KEY (date, country_code, name)    -- cmb_real_rates (name = policy_rate | cpi_yoy | real_rate_ex_post)
```

```sql
-- macro_us: CPI dos EUA
-- `ajuste` na chave porque a cobertura SA/NSA e desigual (ver acima); sem coluna
-- `arvore` porque o NIVEL do indice de um item e o mesmo nas duas arvores -- so o
-- lugar dele na hierarquia muda, e isso vive na dim.
PRIMARY KEY (date, indice, item_code, ajuste)   -- inflc_cpi (indice = CPI-U | CPI-W | C-CPI-U;
                                                --  ajuste = SA | NSA; value = NIVEL, nao variacao)
PRIMARY KEY (arvore, item_code)                 -- inflc_cpi_dim (arvore = despesa | divulgacao;
                                                --  o mesmo item_code aparece nas duas com nivel e
                                                --  pai DIFERENTES -- Apparel e grupo de nivel 1 numa
                                                --  e componente de core goods no nivel 3 na outra)
-- PCE: `linha` e a chave porque a POSICAO na arvore e a identidade -- 13 codigos do
-- BEA aparecem em duas linhas cada (a mesma serie entra 2x na arvore, com pais
-- diferentes), e ZZZZZZ nao e codigo, e o marcador de "nao publico serie".
-- `medida` na chave pelo mesmo motivo que `ajuste` na do CPI: cobertura desigual --
-- as 2 linhas de net tem nominal e nao tem indice de preco.
PRIMARY KEY (date, linha, medida)               -- inflc_pce (medida = indice | nominal;
                                                --  value = NIVEL/US$ mi, nao variacao;
                                                --  so SA -- nao ha NSA mensal na fonte)
PRIMARY KEY (linha)                             -- inflc_pce_dim (bloco = principal | addenda;
                                                --  parent_linha NULL na raiz E em todo o
                                                --  bloco addenda, que nao e arvore)

PRIMARY KEY (reference_period, indice, secao, indent_level, item_name)
                                                -- inflc_cpi_pesos (secao = expenditure |
                                                --  special_aggregate, duas arvores EMPILHADAS no
                                                --  mesmo arquivo: expenditure soma 100,
                                                --  special_aggregate soma ~664 porque sao recortes
                                                --  que se sobrepoem -- nunca agregar por cima das
                                                --  duas. item_name na chave porque a planilha nao
                                                --  publica item_code)
```

`ON DUPLICATE KEY UPDATE` on insert makes it an idempotent upsert.
