# Pipeline Cambial — Status e Pendências

Schemas MySQL: `macro_brasil` · `macro_international` (servidor 192.168.15.200) — ver [`DB_SCHEMAS.md`](DB_SCHEMAS.md) para a organização geral  
Entry points: `jobs/update_db.py` · `jobs/update_international.py`  
Construído em: junho 2026 · Reestruturado: junho 2026, julho 2026 (macro_analytics descontinuado; tabelas renomeadas com prefixo de tema `cambio_`, depois abreviadas para `cmb_` nos dois schemas — exceto `diferenciais_juros`, que ficou sem prefixo por escolha explícita — ver `DB_SCHEMAS.md`)

---

## O que foi feito

### Fase 1 — BCB + FRED (connectors existentes)

| Tabela | Schema | Fonte | Período | Script |
|---|---|---|---|---|
| `cmb_reservas_bc` | `macro_brasil` | BCB SGS (22 séries) | 1971 → hoje | `domain/db/brasil/bcb/cmb_reservas_bc.py` |
| `cmb_cambio_contratado` | `macro_brasil` | BCB SGS (15 séries) | 1982 → hoje | `domain/db/brasil/bcb/cmb_cambio_contratado.py` |
| `cmb_ptax` | `macro_brasil` | BCB SGS 1, 20205, 20359 | 1984 → hoje | `domain/db/brasil/bcb/cmb_ptax.py` |
| `cmb_balanco_pagmt` | `macro_brasil` | BCB SGS (41 séries) | 1995 → hoje | `domain/db/brasil/bcb/cmb_balanco_pagmt.py` |
| `cmb_fluxo_cambial` | `macro_brasil` | BCB SGS (6 séries) | 2003 → hoje | `domain/db/brasil/bcb/cmb_fluxo_cambial.py` |
| `cmb_termos_troca` | `macro_brasil` | IPEADATA/Funcex (`FUNCEX12_TTR12`) | 1978 → hoje | `domain/db/brasil/ipea/cmb_termos_troca.py` |
| `diferenciais_juros` | `macro_international` | BCB SGS + FRED | 1995 → hoje | `domain/db/international/fred/diferenciais_juros.py` |

**`cmb_reservas_bc`** — schema `(date, sgs_code, name, value)`, PK `(date, sgs_code)`, `name` coluna regular. 22 séries, mistura mensal/diária. (Correção 2026-07: esta tabela era documentada aqui com apenas 1 série — a implementação real já estava muito mais completa; doc estava desatualizado, não o dado. Consolidado de `RESERVAS.md`, que foi descontinuado — conteúdo integralmente incorporado abaixo.)

*Reservas internacionais — mensais:*

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

> Excluído do escopo: 3545 (mesma série em periodicidade anual — redundante com 3546). Excluído: 3557 (Notes and coins — descontinuado pelo BCB set/2008).

*Posição cambial líquida BCB — mensais (Tabela 12 BCB):*

| SGS | Nome | Descrição | Unidade | Início |
|---|---|---|---|---|
| 21195 | `bank_fx_spot_position` | Posição de câmbio dos bancos no mercado à vista (net) | US$ MM | 1994 |
| 29533 | `bcb_swap_cambial_position` | Swap cambial BCB — posição líquida; **negativo = BCB vendeu swap ao mercado** (posição vendida em USD) | US$ MM | 2008 |
| 29534 | `bcb_fx_stock_repos_loans` | Estoque de linhas com recompra, empréstimos e compromissadas em ME | US$ MM | 2008 |
| 29535 | `bcb_fx_other_assets_liabilities` | Outros ativos/passivos no balanço do BCB em ME | US$ MM | 2008 |

*Reservas internacionais — diárias:*

| SGS | Nome | Descrição | Início |
|---|---|---|---|
| 13621 | `reserves_total_daily` | International reserves - Total - daily | 1998 |
| 13982 | `reserves_liquidity_daily` | International reserves - Liquidity concept - daily | 2008 |

*Intervenções BCB — diárias (líquidas, zeros filtrados — armazena só dias com intervenção efetiva; positivo = BCB comprando USD, negativo = vendendo):*

| SGS | Nome | Descrição | Nº obs (2026-07) |
|---|---|---|---|
| 17843 | `bcb_intervention_spot` | Spot net interventions – settled | 1.692 |
| 24425 | `bcb_intervention_forwards` | Forwards net interventions – settled | 11 |
| 24427 | `bcb_intervention_fx_loans_repos` | FX loans and FX repos – settled | 316 |
| 24448 | `bcb_intervention_repo_lines` | Repo lines of credit – settled | 278 |

*Contagens aproximadas (levantamento original, 2026-07):* `3546` ~665 obs (1971–hoje) · `3547`–`3556` ~305 cada (2001–hoje) · `7323` ~292 (2002–hoje) · `21195` ~388 (1994–hoje) · `29533`–`29535` ~221 cada (2008–hoje) · `13621` ~6.986 (1998–hoje) · `13982` ~4.644 (2008–hoje) · intervenções ~2.300 total (1999–hoje) — total ~19.000 linhas na tabela.

**`cmb_cambio_contratado`** — schema `(date, sgs_code, name, value)`, PK `(date, sgs_code)` (não documentada aqui até 2026-07, apesar de já implementada — maior histórico de qualquer tabela cambial; consolidado de `RESERVAS.md`):

*Tabela 13 BCB — Movimento de câmbio contratado (diário, desde set/2008):*

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

*Tabela 14 BCB — Financeiro detalhado (mensal):*

| SGS | Nome | Descrição | Início |
|---|---|---|---|
| 11050 | `cc_fin_saldo_det` | Saldo financeiro detalhado | 1982 |
| 29561 | `cc_fin_servicos` | Serviços | 2011 |
| 29562 | `cc_fin_rendas` | Rendas primária e secundária | 2011 |
| 29563 | `cc_fin_cap_bras` | Capitais brasileiros | 2011 |
| 29564 | `cc_fin_cap_ext` | Capitais estrangeiros | 2011 |

*Contagens aproximadas:* diárias (13961–13970) ~44.610 obs (set/2008–hoje); mensais (11050, 29561–29564) ~1.272 obs (1982–hoje); total ~45.882 linhas.

> **`cmb_cambio_contratado` ≠ `cmb_fluxo_cambial`:** o contratado mede liquidações banco-cliente (Tabelas 13/14 BCB, séries `13xxx`/`29561`–`29564`); o fluxo cambial registrado (`cmb_fluxo_cambial`, códigos `24xxx`) é uma medida mais ampla que cobre todos os canais — não são a mesma coisa nem substitutos um do outro.

**`cmb_ptax`** (nova, 2026-07) — preenche a lacuna "sem série de câmbio à vista" identificada em `agent_bibliography/agent_mapping/recommended_data/exchange_rate_data_inventory.md`:
- `ptax_venda` (SGS 1) — Taxa de câmbio livre, dólar americano (venda), diário; desde 28/11/1984
- `fx_interbank_vol_t1` (SGS 20359) — Volume interbancário de câmbio USD, liquidação T+1; desde 04/07/1994
- `fx_interbank_vol_t2` (SGS 20205) — Volume interbancário de câmbio USD, liquidação T+2; desde 04/07/1994
- Série diária: carga histórica usa chunking anual (API BCB rejeita janelas > 10 anos para séries diárias — erro 406 confirmado).

**`cmb_balanco_pagmt`** — reestruturada em 2026-07 a partir de `balance_payments_breakdown.xlsx` (mapeamento oficial de códigos SGS fornecido pelo usuário, arquivo na raiz do repo). 41 séries brutas, 1995 → hoje:
- Conta corrente: `conta_corrente`, `balanca_comercial_servicos`, `exportacao_bens`, `importacao_bens`, `servicos`, `viagens`, `transportes`, `aluguel_equipamentos`, `renda_primaria`, `remuneracao_empregados`, `lucros_remetidos`, `lucros_reinvestidos`, `juros_intercompanhia`, `lucros_dividendos_carteira`, `juros_carteira_externo`, `juros_carteira_domestico`, `juros_outros_investimentos`, `renda_reservas`, `renda_secundaria`, `conta_capital`
- Conta financeira: `conta_financeira`, `idp_exterior`, `ide_saidas`, `investimento_direto_liquido`, `idp_ingressos`, `portfolio_ativos`, `portfolio_passivos`, `acoes_passivos`, `fundos_passivos`, `titulos_dom`, `titulos_externo_cp`, `titulos_externo_lp` (+ `_ingressos`/`_saidas`), `outros_inv_ativos`, `outros_inv_passivos`, `emprestimos_cp_passivos`, `emprestimos_lp_passivos` (+ `_ingressos`/`_saidas`), `derivativos`, `ativos_reserva`, `erros_omissoes`
- **Agregados derivados** (calculados em `generate_report.py`, não armazenados): `demais_servicos`, `juros`, `lucros_dividendos`, `investimentos_ativos`, `investimentos_passivos`, `acoes_totais`, `emprestimos_titulos_lp_externo`, `emprestimos_titulos_cp_externo`, `demais_passivos` — todas as fórmulas cross-checadas contra o quadro condensado oficial do BCB ("Financiamento Externo") em 5 meses (Jan-Mai/2026), batendo dentro da tolerância de arredondamento da API (<0.11). Ver docstring de `cmb_balanco_pagmt.py` para as fórmulas completas.
- **Pendência conhecida:** a quebra "Ativos de bancos" vs "Demais ativos" (lado ativo do balanço) e a quebra público/privado/direto/demais dos empréstimos de LP externo (Ingressos e Amortizações) — 10 das 40 linhas do "quadro que o usuário quer" — não têm código SGS correspondente nem em `balance_payments_breakdown.xlsx` nem em qualquer fonte que já temos. Precisa de códigos adicionais (possivelmente de uma tabela BCB diferente) antes de resolver.

**Bug corrigido (2026-07, achado ao processar `balance_payments_breakdown.xlsx`):** 6 das 10 séries originais desta tabela usavam códigos SGS **errados** — apontavam para sub-itens sem relação com o nome da série (ex: `conta_corrente` usava SGS 22707, que é "Balança comercial (bens)", não "Transações correntes" — sinal e magnitude completamente diferentes). Séries afetadas: `conta_corrente`, `balanca_comercial_servicos`, `conta_financeira`, `investimento_carteira`, `carteira_acoes`, `carteira_renda_fixa`. As 3 últimas foram descontinuadas (substituídas por `portfolio_ativos`/`portfolio_passivos`/`acoes_passivos`/`fundos_passivos`/`titulos_dom`, mais precisas); as linhas históricas sob os nomes antigos foram deletadas do banco (1131 linhas) com confirmação do usuário, já que nunca representaram o conceito que o nome sugeria. Isso também significa que os 3 charts da aba BOP construídos horas antes desta correção mostravam dados errados — foram reconstruídos (ver "Estrutura em abas" abaixo).

**`cmb_fluxo_cambial`** — séries armazenadas:
- Total: `total_saldo`, `total_entrada`, `total_saida`
- Comercial: `comercial_entrada`, `comercial_saida`
- Financeiro: `financeiro_saldo`

**`cmb_termos_troca`** — série armazenada:
- `termos_de_troca_funcex` — índice termos de troca (PX/PM, média 2018=100), fonte Funcex via IPEADATA; mensal, 1978 → hoje
- **Correção 2026-07:** as séries antigas (`termos_de_troca_a`/`b`, BCB SGS 22099/22100) foram removidas — confirmado que esses códigos SGS **não são termos de troca cambiais**, e sim séries de Contas Nacionais (PIB). O BCB SGS não publica termos de troca; a fonte correta é a Funcex, disponibilizada via API IPEADATA (`connectors/ipeadata.py`, série `FUNCEX12_TTR12`).

**`diferenciais_juros`** — séries armazenadas (frequência mensal, month-start):
- Brutas: `selic`, `fed_funds`, `ipca_12m`, `cpi_12m_us`
- Diferenciais ex-post: `diferencial_nominal`, `real_br_ex_post`, `real_us_ex_post`, `diferencial_real`
- **Histórico expandido 2026-07** (era janela de 36 meses): `selic`/`ipca_12m`/`fed_funds`/`cpi_12m_us` agora desde 1995; `selic` de fato começa em 1999-03 (início do regime de meta Selic do Copom, SGS 432 não tem dado anterior). Fetch de `selic` (SGS 432, série diária) usa chunking de 8 anos para evitar o erro 406 da API BCB (janela máxima de 10 anos para séries diárias).

### Fase 2 — BIS + CFTC (novos connectors)

| Tabela | Schema | Fonte | Período | Script |
|---|---|---|---|---|
| `cmb_reer` | `macro_international` | BIS API (stats.bis.org) | 1994 → hoje | `domain/db/international/bis/cmb_reer.py` |
| `cmb_cot_fx` | `macro_international` | CFTC TFF ZIPs | 2010 → hoje | `domain/db/international/cftc/cmb_cot_fx.py` |

**`cmb_reer`** — países × tipos (388 obs cada, ~1994–hoje):
- Brasil (BR), México (MX), Chile (CL), Colômbia (CO)
- Tipos: `real_broad`, `nominal_broad`
- BIS API key order: `FREQ.EER_TYPE.EER_BASKET.REF_AREA` (ex: `M.R.B.BR`)
- `real_narrow` foi excluído do escopo

**`cmb_cot_fx`** — BRL e MXN; semanal (terças):
- `open_interest`, `lev_long`, `lev_short`, `lev_net`, `nonrept_long`, `nonrept_short`
- Fonte: CFTC Traders in Financial Futures (`fut_fin_txt_{YYYY}.zip`)
- CLP e COP **não têm** futuros CME no relatório TFF

### Connectors criados

| Arquivo | API | Auth |
|---|---|---|
| `connectors/bis.py` | BIS Statistics API v1 (`stats.bis.org/api/v1`) | Nenhuma |
| `connectors/cftc.py` | CFTC TFF ZIPs anuais | Nenhuma |
| `connectors/ipeadata.py` (2026-07) | IPEADATA OData v4 (`ipeadata.gov.br/api/odata4`) | Nenhuma |

**`connectors/ipeadata.py`** — criado para termos de troca (Funcex não está no BCB SGS). Nota técnica: o filtro `$filter=contains(...)` retorna 400 nesta API — usar `substringof('valor', CAMPO)` (sintaxe OData v3) para buscar séries por nome/código.

---

## Relatório HTML — analytics/cambio/

Construído em junho 2026. Arquivo único autocontido (`reports/fx_report.html`, renomeado de `cambio_latest.html` em 2026-07) gerado por `analytics/cambio/generate_report.py` a partir do template `analytics/cambio/report.html`.

### Como atualizar

```powershell
# Atualizar dados (opcional — só se quiser dados mais frescos)
uv run python jobs/update_db.py            # macro_brasil (inclui cmb_reservas_bc, cmb_cambio_contratado, cmb_ptax, cmb_balanco_pagmt, cmb_fluxo_cambial, cmb_termos_troca)
uv run python jobs/update_international.py # macro_international (cmb_reer, cmb_cot_fx, diferenciais_juros)

# Gerar relatório
uv run python -c "from analytics.cambio.generate_report import run; run()"
# Saída: reports/fx_report.html  (~50 KB, abre em qualquer browser)
```

### Mecanismo de injeção

O template contém o marcador `/*REPORT_DATA*/` num bloco `<script>`. `generate_report.py` lê tabelas de `macro_brasil` e `macro_international`, serializa como JSON e substitui o marcador via `str.replace()`. Sem Jinja2.

### Estrutura em abas (2026-07, reestruturação)

O relatório era uma página única com âncoras de navegação (scroll), sem separação de assunto. Reestruturado para abas reais (JS troca `display:none`/`flex` por `.tab-panel`, sem reload), agrupando por *o que a informação responde* em vez de por fonte de dado:

| Aba | ID | Pergunta que responde |
|---|---|---|
| a) Balanço de Pagamentos | `tab-bop` | De onde vêm/para onde vão os dólares na conta corrente e financeira? |
| Mapa de Calor — BP | `tab-heatmap` | Quais componentes do BP estão anormalmente fortes/fracos agora vs. os últimos 3 anos? (2026-07, ver seção própria abaixo) |
| b) Posicionamento do BCB | `tab-bcb` | O que o Banco Central está fazendo (reservas, swap, ouro, intervenção)? |
| c) Fluxo Cambial | `tab-flow` | Qual o fluxo de câmbio contratado no mercado (Nota Cambial + volume interbancário)? |
| d) Cotação | `tab-quotation` | Qual o nível do câmbio à vista? |
| e) Valuation | `tab-valuation` | O câmbio está caro ou barato (juros reais, REER, termos de troca, posicionamento especulativo)? |

**Detalhe técnico do tab switching:** `Plotly.newPlot()` dentro de um painel `display:none` renderiza com largura zero. `activateTab()` chama `Plotly.Plots.resize()` em todo chart do painel recém-ativado (guardado por `div._fullLayout`, que só existe se o chart já foi de fato desenhado — evita erro em charts que retornaram cedo por falta de dado).

**Bug corrigido nesta reestruturação:** `_load_reservas()` (agora `_load_bcb_positioning()`) referenciava a coluna `reservas_liquidez_usd`, que nunca existiu em `cmb_reservas_bc` (nomes reais em inglês: `reserves_liquidity_daily`, `reserves_total_monthly` etc. — ver docstring de `cmb_reservas_bc.py`). `chart-reservas` estava silenciosamente vazio desde a criação do relatório.

**Detalhe técnico do loader `_load_bcb_positioning()`:** `cmb_reservas_bc` mistura frequências (mensal para reservas/swap/ouro, diária para `reserves_liquidity_daily`/intervenções) numa única tabela. Pivotar tudo junto criaria um índice de datas comum onde as séries mensais ficariam cercadas de `null` e a linha "quebraria" no gráfico (Plotly não conecta através de gaps por padrão). Corrigido pivotando cada subgrupo (`reserves`, `gold`, `swap`, `interventions`) separadamente, cada um com seu próprio eixo `dates` — por isso `REPORT_DATA.bcb_positioning` é aninhado, diferente dos outros grupos.

### Charts ativos

| Aba | ID | Dados | Tipo |
|---|---|---|---|
| a | `chart-bop-current` | balança comercial+serviços + renda primária + renda secundária (barras) + conta_corrente (linha, total) | barras empilhadas + linha |
| a | `chart-bop-servicos` | viagens + transportes + aluguel de equipamentos + demais serviços (barras) + serviços (linha, total) | barras empilhadas + linha |
| a | `chart-bop-renda` | remuneração de empregados + juros + lucros e dividendos (barras) + renda primária (linha, total) | barras empilhadas + linha |
| a | `chart-bop-financial` | investimentos ativos/passivos + derivativos + ativos de reserva | barras (sem linha de total — ver nota) |
| a | `chart-bop-financiamento` | IDP no país + ações totais + títulos mercado doméstico + empréstimos/títulos LP/CP externo + demais passivos (barras) + investimentos passivos (linha, total) | barras empilhadas + linha |
| heatmap | `chart-heatmap` | árvore de 3 níveis do BP (ver seção própria abaixo) | heatmap, z-score trimestral |
| b | `chart-bcb-reserves` | reserves_liquidity_daily (diária) + reserves_total_monthly (mensal, connectgaps) | 2 linhas |
| b | `chart-bcb-swap` | bcb_swap_cambial_position vs bank_fx_spot_position | 2 linhas |
| b | `chart-bcb-gold` | reserves_gold_usd | linha + fill |
| b | `chart-bcb-intervention` | 4 séries de intervenção BCB (spot/forwards/fx loans-repos/repo lines) | barras |
| c | `chart-fluxo` | total/comercial/financeiro_saldo | 3 linhas |
| c | `chart-fluxo-breakdown` | total/comercial entrada (+) e saída (−, espelhada) | barras |
| c | `chart-interbank-vol` | fx_interbank_vol_t1/t2 | barras empilhadas |
| d | `chart-ptax` | ptax_venda | 1 linha |
| e | `chart-nominal-rates` | Selic + Fed Funds | linha |
| e | `chart-diferencial-nominal` | diferencial_nominal | linha + fill |
| e | `chart-taxas-reais` | real_br/us ex-post + diferencial | 3 linhas |
| e | `chart-reer` | BR/MX/CL/CO real_broad | 4 linhas + linha base 100 |
| e | `chart-termos` | termos_de_troca_funcex | 1 linha |
| e | `chart-cot-brl` | lev_net (barras) + open_interest | bar + linha eixo duplo |

**Agregação por período (aba BOP, 2026-07):** os 5 charts da aba Balanço de Pagamentos têm um seletor compartilhado (`#bop-period-selector`) — Mensal / Trimestral / Anual (barras empilhadas, `barmode: 'relative'`) ou 12m Acumulado (linha, soma móvel de 12 meses). Motivação: essas séries são composições (partes que somam a um total, validado em `cmb_balanco_pagmt.py`) — barra empilhada comunica "isso construiu aquilo" melhor que linhas sobrepostas; a soma móvel de 12m suaviza a sazonalidade mensal do BOP para leitura de tendência. Trimestral/anual agregam por soma calendário-fixa (`QS`/`YS`, equivalente a `pandas.resample`); se qualquer mês do bucket for `null`, o bucket inteiro vira `null` (evita subestimar silenciosamente). `chart-bop-financial` não tem linha de total porque `conta_financeira = investimentos_ativos − investimentos_passivos + derivativos + ativos_reserva` (passivos entra com sinal invertido na identidade — empilhar os 4 componentes com sinal natural não soma ao total).

**Nota:** volume interbancário (T+1/T+2) saiu do `chart-ptax` (antes combinado) e virou seu próprio chart em Fluxo Cambial (`chart-interbank-vol`) — a aba Cotação agora mostra só o nível do câmbio, sem misturar volume.

### Mapa de Calor — Balanço de Pagamentos (2026-07)

Aba nova (`tab-heatmap`), pedida pelo usuário para visualizar todo o BP num único heatmap com drill-down, ao invés de vários line charts separados.

**Decisões de design (definidas com o usuário antes de implementar):**
- **Interação:** drill-down hierárquico — linhas organizadas em árvore de 3 níveis (`BOP_TREE` em `report.html`, espelhando exatamente a hierarquia de `cmb_balanco_pagmt.py`: Conta Corrente → Balança Comercial+Serviços/Renda Primária/Renda Secundária → sub-detalhe; Conta Financeira → Ativos/Passivos/Derivativos/Reserva → Financiamento Externo). Clicar numa linha com filho (`▸`/`▾`) expande/recolhe via `plotly_click` (`evt.points[0].y` mapeado de volta ao nó da árvore por um dicionário `labelToNode` reconstruído a cada render). Botões "Expandir Tudo"/"Recolher Tudo" para conveniência.
- **Cor = z-score, não sinal bruto:** cada célula é colorida pelo z-score da própria série contra sua média/desvio-padrão móvel de 3 anos (12 trimestres, `rollingZScore()`), não pelo sinal do valor bruto. Azul = acima do normal da própria série (mais inflow ou menos outflow que o usual — "melhora"), vermelho = abaixo do normal ("piora"). Isso funciona igual para séries que são estruturalmente positivas (ex: Investimentos-Passivos) e estruturalmente negativas (ex: Renda Primária, tipicamente outflow — um mês com outflow menor que o usual aparece azul mesmo com valor bruto negativo). Colorscale customizada `[[0,'#B91C1C'],[0.5,'#F5F5F5'],[1,'#1D4ED8']]` com `zmin:-3, zmax:3` (branco = z=0, exatamente no centro da escala).
- **Colunas:** trimestral, histórico completo desde 1995 (reaproveita `aggregateSum()` já usado na aba BOP). Z-score precisa de janela de 12 trimestres cheia — as primeiras ~3 anos de cada série ficam em branco (sem baseline ainda).

**Verificação:** `rollingZScore()` e `flattenVisibleRows()`/toggle de expand-collapse foram extraídos e rodados via Node.js contra os dados reais do relatório, comparados a `pandas` (`.rolling(12).mean()/.std()`) — bateram exatamente (mesmos 6 últimos trimestres testados).

**Pendência conhecida:** altura do card é fixa (`.chart-card-tall`, 820px) dimensionada para a árvore totalmente expandida (~31 linhas); com poucas linhas visíveis (colapsado), as linhas ficam desproporcionalmente altas — não implementado redimensionamento dinâmico por enquanto.

**Pendência conhecida (aba d):** só há cotação BRL/USD hoje. O pedido do usuário foi explicitamente "mais moedas pares" (MXN, CLP, COP etc.) — nenhuma série de câmbio à vista para esses pares está no banco ainda; nota visível no próprio relatório (`sec-quotation-ptax`).

---

## Pendências

### Alta prioridade

#### 0. Balanço de Pagamentos — 10 linhas do quadro "Financiamento Externo" sem código SGS

Ao processar `balance_payments_breakdown.xlsx` (2026-07), 30 das 40 linhas do quadro condensado que o usuário quer foram resolvidas e cross-checadas (ver `cmb_balanco_pagmt.py`). Restam sem código SGS identificado:
- **Ativos de bancos** vs **Demais ativos** (quebra por setor do lado ativo do balanço) — só encontramos quebra setorial (Banco Central/Bancos/Governo/Demais setores) para o lado ativo em "Moeda e depósitos" (SGS 22982 para bancos); não bate exatamente com o valor do quadro condensado, então não é só essa série.
- **Títulos públicos / Títulos privados / Empréstimos diretos / Demais empréstimos** — quebra por tipo de credor dentro de "Empréstimos e títulos de LP negociados no mercado externo", tanto para Ingressos quanto para Amortizações (8 linhas) — não existe em `balance_payments_breakdown.xlsx` nem no detalhamento BPM6 padrão (códigos 22701–23060).

**Próximos passos (definido com o usuário em 2026-07):** duas linhas de ataque possíveis, ainda em aberto:
1. **Usar a informação do jeito que o BCB fornece** — ao invés de forçar a quebra exata do quadro "Financiamento Externo" (bancos/demais setores, público/privado/direto), aceitar a granularidade que o BPM6 detalhado (`balance_payments_breakdown.xlsx`, aba 1) já oferece nativamente para essas 10 linhas, mesmo que não bata 1:1 com "o quadro que eu quero".
2. **Tentar por tentativa e erro** — buscar no buscador de séries do BCB SGS (https://www3.bcb.gov.br/sgspub/localizarseries/localizarSeries.do) por candidatos a código fora do range 22701–23060 (o quadro condensado "Financiamento Externo" das notas do setor externo do BCB provavelmente tem sua própria faixa de códigos, sem correspondência 1:1 com o detalhamento BPM6).

Nenhuma das duas foi executada ainda — ficou registrado como pendência para retomar quando o usuário tiver tempo/prioridade.

#### 1. Reservas internacionais — série "brutas" em aberto

O código SGS 13127 (supostamente `reservas_brutas_usd`) retorna timeout consistente — pode ser código errado ou série descontinuada. O BCB publica vários conceitos de reservas (liquidez, caixa, brutas) com fontes e metodologias distintas.

**Próximos passos:**
- Acessar o buscador de séries do BCB SGS: https://www3.bcb.gov.br/sgspub/localizarseries/localizarSeries.do
- Buscar por "reservas internacionais" e mapear os códigos disponíveis
- Avaliar se o conceito "brutas" é necessário para o dashboard ou se "liquidez" (3546) já é suficiente
- Verificar também a posição de swaps cambiais do BCB (não disponível no SGS — necessita scraper da URL `https://www4.bcb.gov.br/pom/demab/cronogramacambiais/vencdata.asp`)

#### 2. Diferenciais de juros ex-ante (nominal e real)

A `diferenciais_juros` hoje contém apenas ex-post (inflação realizada). Os ex-ante usam expectativas de mercado:

**Diferencial nominal ex-ante:**
- Brasil: mediana Focus Selic EOP 12m à frente (já em `macro_brasil.expc_focus`)
- EUA: taxa implícita nos Fed Funds futuros (FRED: `FF{mês}` futures ou OIS) — **pendente de implementação**

**Diferencial real ex-ante:**
- Brasil: Selic EOP Focus 12m − IPCA 12m Focus (ambos já em `expc_focus`)
- EUA: taxa implícita − CPI 12m expectativa (FRED: Michigan Survey `MICH` ou 5yr breakeven `T5YIE`)

**Implementação sugerida:** criar novas séries em `diferenciais_juros` com sufixo `_ex_ante` sem alterar as séries ex-post já existentes.

#### 6. Aba Cotação — cotações de moedas pares (2026-07, pedido explícito do usuário)

Hoje `chart-ptax` mostra só BRL/USD. Pedido: adicionar spot de moedas pares EM (candidatas óbvias: MXN, CLP, COP — mesmo conjunto já usado em `cmb_reer`/`cmb_cot_fx`) para comparação lado a lado. Nenhuma dessas séries está no banco — precisa de connector novo (FRED tem `DEXMXUS`, `DEXCHUS`... confirmar códigos exatos; BIS/BCB não publicam spot de moedas de terceiros). Depende de "não pegar mais dado ainda" (instrução do usuário nesta sessão) — avaliar quando ele autorizar nova coleta.

### Média prioridade

#### 3. Fluxo cambial — granularidade adicional

A BCB publica sub-itens do fluxo financeiro (CEP/CBE) na Nota Cambial semanal que podem ter códigos SGS — ainda não confirmados. Séries candidatas (24372–24376) retornaram dados na pesquisa inicial mas com descrições não confirmadas. Ver Nota Cambial BCB para mapeamento.

#### 4. Cupom cambial + futuros B3 — Bloomberg (Fase 3)

Deferred: requer `blpapi`/`xbbg` na máquina de Bloomberg.
- `cupom_cambial`: curva DDI/FRC, schema `PRIMARY KEY (date, name, maturity)`
- `b3_fx_futures`: DOL/WDO preço, volume, OI

#### 5. `cmb_ptax` — incorporada ao relatório HTML ✓ (feito, 2026-07)

`chart-ptax` (linha PTAX venda) adicionado na aba Cotação. `agent_data.py` (cambio-analyst) também atualizado para incluir o grupo `ptax` no snapshot — a nota antiga "nenhuma série de câmbio à vista disponível" estava desatualizada e foi removida. **Atualização (mesmo dia, reestruturação em abas):** o volume interbancário (T+1/T+2), que tinha sido colocado no mesmo chart em eixo secundário, foi separado para seu próprio chart (`chart-interbank-vol`) na aba Fluxo Cambial — a aba Cotação mostra só o nível do câmbio. `_load_ptax()` ainda expõe `vol_t1`/`vol_t2`/`vol_total` (soma) para os dois consumidores.

#### 7. Balança de Bens — quebra adicional (registrado 2026-07)

Hoje `cmb_balanco_pagmt` só tem `exportacao_bens`/`importacao_bens` em total (sem quebra por produto, país/parceiro comercial, ou fator agregado). O usuário quer mais detalhe aqui — eixo de quebra ainda não definido. Precisa decidir com o usuário: quebra por categoria de produto (commodities vs manufaturados?), por país/bloco parceiro, ou ambos — e se os dados vêm do BCB SGS (buscar códigos) ou de outra fonte mais adequada para comércio exterior (ex: Comex Stat/MDIC, que é a fonte oficial de dados de comércio exterior desagregados por NCM e país, mas não é BCB SGS — pode exigir um connector novo).

#### 8. Métricas em % do PIB (registrado 2026-07)

Adicionar as séries do Balanço de Pagamentos como % do PIB (ex: conta corrente/PIB, IDP líquido/PIB), para comparabilidade histórica entre períodos de câmbio/preço diferentes — hoje todo o BOP está em USD milhões nominais, o que dificulta comparar magnitude entre 1995 e 2026. Precisa: (a) confirmar se já temos uma série de PIB adequada no banco (`atv_pib`, IBGE 1620/1621 — verificar se é só em BRL ou também disponível/conversível para USD, e se a frequência trimestral bate com o BOP) e (b) decidir onde expor isso no relatório — provavelmente como um toggle adicional na aba BOP (ao lado do seletor de período) ou uma aba/seção própria.

#### 9. Melhorias no Mapa de Calor (registrado 2026-07)

Itens abertos, ainda sem prioridade definida:
- **Altura fixa do card** (`.chart-card-tall`, 820px) foi dimensionada para a árvore totalmente expandida (~31 linhas) — com poucas linhas visíveis (estado recolhido, default), as linhas ficam desproporcionalmente altas. Deliberadamente deixado assim por ora ("por enquanto, deixa assim" — instrução do usuário). Redimensionamento dinâmico por número de linhas visíveis é a solução óbvia quando isso virar prioridade.
- Espaço para outras melhorias a definir (ex: exportar/imprimir o estado expandido, indicador visual de "quantas colunas iniciais estão em branco" por falta de baseline de 3 anos, etc.) — usuário não especificou detalhes ainda.

---

## Notas técnicas

### BCB — Reservas e Câmbio Contratado (consolidado de `RESERVAS.md`)
- Séries diárias em `cmb_reservas_bc` e `cmb_cambio_contratado` usam chunking anual para evitar o erro 406 da API BCB (mesma limitação de janela de 10 anos para séries diárias documentada em `diferenciais_juros`/`cmb_ptax`).
- `reserves_gold_volume` (SGS 3553) está em **troy oz (thousand)**, não USD — não somar/plotar junto com as demais séries de reservas (todas em US$ MM) sem converter.
- `bcb_swap_cambial_position` (SGS 29533) negativo = BCB vendeu swap ao mercado (posição vendida em USD via swap tradicional).

### BIS API
- Base correta: `https://stats.bis.org/api/v1/` (não `data.bis.org`)
- Key structure WS_EER: `FREQ.EER_TYPE.EER_BASKET.REF_AREA`
- Colunas CSV retornadas: `FREQ, EER_TYPE, EER_BASKET, REF_AREA, TIME_PERIOD, OBS_VALUE, ...`

### CFTC TFF
- URL: `https://www.cftc.gov/files/dea/history/fut_fin_txt_{YYYY}.zip`
- ZIP contém: `FinFutYY.txt` (87 colunas)
- Coluna de data: `Report_Date_as_YYYY-MM-DD` (2013+) ou `Report_Date_as_MM_DD_YYYY` (2010–2012 — o nome é enganoso, os valores também são `YYYY-MM-DD`). O connector auto-detecta.
- Histórico disponível: 2010 → hoje (2006–2009 retornam 404 no CFTC).
- FX contracts no arquivo: BRL e MXN. CLP/COP não têm futuros CME no TFF.

### Selic + alinhamento de frequência
- BCB SGS 432 (Selic) usa datas de reunião do COPOM, não datas de calendário
- Em `diferenciais_juros.py`: `bcb_wide.resample("MS").last()` alinha para month-start antes de concatenar com dados FRED mensais

---

## Roadmap do Relatório

### Fase 1 — Qualidade e detalhe dos dados

**Objetivo:** o relatório deve mostrar o quadro cambial completo, sem lacunas de série nem dados truncados.

#### 1a. Histórico `diferenciais_juros` ✓ (feito, 2026-07)

Carga histórica expandida para 1995 → hoje (rodar `diferenciais_juros.run(start="all")`). Confirmado: BCB SGS 432 (Selic, série diária) retorna 406 para janelas > 10 anos (mensagem da API: "o sistema aceita uma janela de consulta de, no máximo, 10 anos em séries de periodicidade diária"). Fix: `_fetch_bcb_chunked()` encadeia em janelas de 8 anos. `selic` de fato só existe a partir de 1999-03 (início do regime de meta Selic do Copom) — não é um bug, é o início real da série.

#### 1b. Diferenciais ex-ante

Criar séries `_ex_ante` em `diferenciais_juros` sem remover as ex-post existentes:

| Nome da série | Fonte | Observação |
|---|---|---|
| `selic_ex_ante` | Focus Selic EOP 12m (`macro_brasil.expc_focus`) | JOIN por data |
| `ipca_ex_ante` | Focus IPCA 12m (`macro_brasil.expc_focus`) | JOIN por data |
| `real_br_ex_ante` | `selic_ex_ante − ipca_ex_ante` | calculado no script |
| `ff_ex_ante` | FRED: `FF{M}` futures ou OIS 1y | novo fetch |
| `cpi_ex_ante` | FRED: `MICH` (Michigan Survey) ou `T5YIE` breakeven | novo fetch |
| `real_us_ex_ante` | `ff_ex_ante − cpi_ex_ante` | calculado no script |
| `diferencial_nominal_ex_ante` | `selic_ex_ante − ff_ex_ante` | calculado no script |
| `diferencial_real_ex_ante` | `real_br_ex_ante − real_us_ex_ante` | calculado no script |

Adicionar dois charts novos no relatório: "Diferencial Nominal ex-ante" e "Taxas Reais ex-ante".

#### 1c. CFTC histórico ✓ (feito)

`connectors/cftc.py` agora suporta 2010 → hoje (auto-detecção de coluna de data entre formatos pré/pós-2013). 2006–2009 retornam 404 no servidor do CFTC — não há histórico disponível antes de 2010.

#### 1d. Pendências menores de ETL

- ~~Confirmar SGS 22099/22100 (termos de troca) — descrições exatas~~ ✓ resolvido 2026-07: não são termos de troca (são Contas Nacionais/PIB); fonte correta é Funcex via IPEADATA — ver `cmb_termos_troca` acima
- Mapear sub-itens CEP/CBE do fluxo financeiro (candidatos 24372–24376)
- Reservas brutas: investigar código SGS correto (13127 retorna timeout)

---

### Fase 2 — Histórico ampliado no relatório

**Objetivo:** todos os charts mostrem o máximo de história disponível na base.

- Garantir que todos os scripts de domínio foram rodados com `start="all"` ao menos uma vez
- Verificar cobertura real de cada tabela:

| Tabela | Schema | Cobertura esperada | Status |
|---|---|---|---|
| `diferenciais_juros` | `macro_international` | 1995 → hoje | ✓ (feito 2026-07; `selic` real desde 1999-03) |
| `cmb_reer` | `macro_international` | 1994 → hoje | ✓ BIS full history |
| `cmb_cot_fx` | `macro_international` | 2010 → hoje | ✓ (2006–2009 indisponíveis no CFTC) |
| `cmb_balanco_pagmt` | `macro_brasil` | 1995 → hoje | ✓ (reestruturada 2026-07, 41 séries) |
| `cmb_fluxo_cambial` | `macro_brasil` | 2003 → hoje | ✓ |
| `cmb_reservas_bc` | `macro_brasil` | 1971 → hoje | ✓ 22 séries (doc anterior estava desatualizado) |
| `cmb_cambio_contratado` | `macro_brasil` | 1982 → hoje | ✓ |
| `cmb_ptax` | `macro_brasil` | 1984 → hoje | ✓ (feito 2026-07; chart-ptax no relatório) |
| `cmb_termos_troca` | `macro_brasil` | 1978 → hoje | ✓ (feito 2026-07, fonte corrigida para Funcex/IPEADATA) |

- Adicionar no `generate_report.py` um campo `data_range` no JSON por seção (para exibir no tooltip do chart header: "2006 – jun/2026")

---

### Fase 3 — Agente de análise ✓ (feito, 2026-07, arquitetura diferente da originalmente planejada)

**Implementado como:** um subagente Claude Code (`.claude/agents/cambio-analyst.md`) que roda `analytics/cambio/agent_data.py` (`get_fx_snapshot()` — snapshot data-only: último valor + deltas 1m/3m/12m por série, reaproveitando os loaders de `generate_report.py`) e conecta os movimentos de dados a conceitos já curados em `obsidian/exchange_rate/concepts/` (UIP, carry trade, REER/PPP, BOP, crises cambiais etc.). Resposta conversacional por padrão; gera relatório markdown em `reports/cambio_analysis_<data>.md` quando solicitado — não escreve nem regenera `reports/cambio_latest.html`.

**Por que a arquitetura mudou em relação ao plano original abaixo (histórico):** o plano original previa uma pasta `bibliography/` de PDFs novos + chamada direta à API Anthropic (`analyze.py`) injetando narrativa estática no HTML. Optou-se por reaproveitar o conhecimento conceitual já existente em `obsidian/exchange_rate/` (evita duplicar uma segunda base de textos) e por um subagente Claude Code interativo/on-demand (evita builds de narrativa estática que ficam desatualizadas assim que os dados mudam). `agent_bibliography/` continua deliberadamente fora do escopo deste agente — sistema paralelo, sem reconciliação (ver `CLAUDE.md`).

**Pendências conhecidas:**
- ~~Sem série de câmbio à vista (PTAX) no banco~~ ✓ resolvido 2026-07: `macro_brasil.cmb_ptax` (PTAX + volume interbancário), e `analytics/cambio/agent_data.py` atualizado para incluir o grupo `ptax` no snapshot.
- **Sem allowlist de permissões Bash em `.claude/settings.json`** — cada chamada do agente ao script (`uv run python ...`) pede confirmação até isso ser configurado separadamente (skill `fewer-permission-prompts`/`update-config`).
- **Casamento de conceitos do obsidian é um julgamento do LLM, não uma busca estruturada** — `concepts/*.md` não tem índice de tags parseável, só uma linha `**Tags:**` em texto livre e nomes de arquivo.

<details>
<summary>Plano original (histórico, superseded)</summary>

**Objetivo:** ao rodar o relatório, um agente lê os dados atuais + uma biblioteca de textos selecionados e gera uma narrativa analítica estruturada, incorporada ao HTML ou exportada como documento separado.

#### Arquitetura proposta

```
analytics/cambio/
  generate_report.py    — existente (dados → HTML)
  analyze.py            — novo: dados + bibliography → narrativa
  bibliography/         — novo: PDFs ou .txt de papers/relatórios de referência
    README.md           — lista dos textos e por que foram incluídos
```

#### `analyze.py` — fluxo

1. `_load_context()` — lê `bibliography/` (PDFs via pypdf ou txt direto), constrói string de contexto
2. `_load_snapshot()` — lê tabelas `macro_brasil`/`macro_international` e formata como texto tabular (últimas N observações por série)
3. `_build_prompt(context, snapshot)` — monta prompt estruturado: contexto bibliográfico + dados atuais + instruções de análise
4. `_call_claude(prompt)` → `anthropic.Anthropic().messages.create(model="claude-opus-4-8", ...)` → texto de análise
5. `run(output_html, inject=True)` — chama `generate_report.run()` e injeta o texto no HTML como seção "Análise"

#### Dependências novas

```powershell
uv add anthropic          # API Claude
uv add pypdf              # leitura de PDFs da bibliography (opcional)
```

#### Estrutura da bibliografia

O diretório `analytics/cambio/bibliography/` deve conter textos relevantes para análise do BRL. Exemplos de conteúdo útil:
- Framework de análise cambial (determinantes do BRL: carry, risco, termos de troca, fluxo)
- Research sobre posicionamento especulativo e reversão de câmbio
- Estudos BCB/FMI sobre equilíbrio do câmbio real no Brasil
- Notas internas de análise macro da LIS Capital

Cada texto deve ter um cabeçalho indicando fonte, data e relevância. O agente usa esse contexto para calibrar a interpretação dos dados, não para reproduzir o texto.

#### Output esperado

Seção "Análise Macro — BRL" no relatório com:
- Diagnóstico atual (ex: "REER apreciado X% acima da média histórica")
- Fatores dominantes (carry vs. fundamentos vs. posicionamento)
- Riscos e pontos de atenção
- Referências explícitas às séries que embasam cada conclusão

</details>
