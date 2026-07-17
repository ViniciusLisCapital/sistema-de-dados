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
| `cmb_balanco_pagmt` | `macro_brasil` | BCB SGS (52 séries) | 1995 → hoje | `domain/db/brasil/bcb/cmb_balanco_pagmt.py` |
| `cmb_fluxo_cambial` | `macro_brasil` | BCB SGS (6 séries) | 2003 → hoje | `domain/db/brasil/bcb/cmb_fluxo_cambial.py` |
| `cmb_termos_troca` | `macro_brasil` | IPEADATA/Funcex (`FUNCEX12_TTR12`) | 1978 → hoje | `domain/db/brasil/ipea/cmb_termos_troca.py` |
| `atv_pib_usd` | `macro_brasil` | BCB SGS 4385 (PIB mensal em USD, Depec) | 1995 → hoje | `domain/db/brasil/bcb/atv_pib_usd.py` |
| `cmb_comex_pais` | `macro_brasil` | Comex Stat/MDIC (China/EUA/Argentina/Alemanha/mundo × export/import) | 1997 → hoje | `domain/db/brasil/mdic/cmb_comex_pais.py` |
| `cmb_comex_fator_agregado` | `macro_brasil` | Comex Stat/MDIC (Básicos/Semi/Manufaturados/Demais × export/import) | 1997 → hoje | `domain/db/brasil/mdic/cmb_comex_fator_agregado.py` |
| `cmb_comex_produto` | `macro_brasil` | Comex Stat/MDIC (Soja/Petróleo/Minério de Ferro/Carnes/Café/mundo × export/import) | 1997 → hoje | `domain/db/brasil/mdic/cmb_comex_produto.py` |
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

**`cmb_balanco_pagmt`** — reestruturada em 2026-07 a partir de `analytics/exchange_rate/referencia/balance_payments_breakdown.xlsx` (mapeamento oficial de códigos SGS fornecido pelo usuário). 52 séries brutas (41 + 7 da quebra de Balança de Bens + 4 da quebra de Carteira — Ativos, todas 2026-07-14), 1995 → hoje:
- Conta corrente: `conta_corrente`, `balanca_comercial_servicos`, `exportacao_bens`, `importacao_bens`, `servicos`, `viagens`, `transportes`, `aluguel_equipamentos`, `renda_primaria`, `remuneracao_empregados`, `lucros_remetidos`, `lucros_reinvestidos`, `juros_intercompanhia`, `lucros_dividendos_carteira`, `juros_carteira_externo`, `juros_carteira_domestico`, `juros_outros_investimentos`, `renda_reservas`, `renda_secundaria`, `conta_capital`
- Conta financeira: `conta_financeira`, `idp_exterior`, `ide_saidas`, `investimento_direto_liquido`, `idp_ingressos`, `portfolio_ativos`, `portfolio_passivos`, `acoes_passivos`, `fundos_passivos`, `titulos_dom`, `titulos_externo_cp`, `titulos_externo_lp` (+ `_ingressos`/`_saidas`), `outros_inv_ativos`, `outros_inv_passivos`, `emprestimos_cp_passivos`, `emprestimos_lp_passivos` (+ `_ingressos`/`_saidas`), `derivativos`, `ativos_reserva`, `erros_omissoes`
- **Agregados derivados** (calculados em `generate_report.py`, não armazenados): `demais_servicos`, `juros`, `lucros_dividendos`, `investimentos_ativos`, `investimentos_passivos`, `acoes_totais`, `emprestimos_titulos_lp_externo`, `emprestimos_titulos_cp_externo`, `demais_passivos` — todas as fórmulas cross-checadas contra o quadro condensado oficial do BCB ("Financiamento Externo") em 5 meses (Jan-Mai/2026), batendo dentro da tolerância de arredondamento da API (<0.11). Ver docstring de `cmb_balanco_pagmt.py` para as fórmulas completas.
- **Pendência conhecida:** a quebra "Ativos de bancos" vs "Demais ativos" (lado ativo do balanço) e a quebra público/privado/direto/demais dos empréstimos de LP externo (Ingressos e Amortizações) — 10 das 40 linhas do "quadro que o usuário quer" — não têm código SGS correspondente nem em `analytics/exchange_rate/referencia/balance_payments_breakdown.xlsx` nem em qualquer fonte que já temos. Precisa de códigos adicionais (possivelmente de uma tabela BCB diferente) antes de resolver.

**Bug corrigido (2026-07, achado ao processar `analytics/exchange_rate/referencia/balance_payments_breakdown.xlsx`):** 6 das 10 séries originais desta tabela usavam códigos SGS **errados** — apontavam para sub-itens sem relação com o nome da série (ex: `conta_corrente` usava SGS 22707, que é "Balança comercial (bens)", não "Transações correntes" — sinal e magnitude completamente diferentes). Séries afetadas: `conta_corrente`, `balanca_comercial_servicos`, `conta_financeira`, `investimento_carteira`, `carteira_acoes`, `carteira_renda_fixa`. As 3 últimas foram descontinuadas (substituídas por `portfolio_ativos`/`portfolio_passivos`/`acoes_passivos`/`fundos_passivos`/`titulos_dom`, mais precisas); as linhas históricas sob os nomes antigos foram deletadas do banco (1131 linhas) com confirmação do usuário, já que nunca representaram o conceito que o nome sugeria. Isso também significa que os 3 charts da aba BOP construídos horas antes desta correção mostravam dados errados — foram reconstruídos (ver "Estrutura em abas" abaixo).

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
| `connectors/comexstat.py` (2026-07-14) | Comex Stat/MDIC API ao vivo (`api-comexstat.mdic.gov.br`) — só updates marginais | Nenhuma |
| `connectors/comexstat_bulk.py` (2026-07-14) | Comex Stat/MDIC download em massa (`balanca.economia.gov.br`) — carga histórica (país + Fator Agregado) | Nenhuma |

**`connectors/ipeadata.py`** — criado para termos de troca (Funcex não está no BCB SGS). Nota técnica: o filtro `$filter=contains(...)` retorna 400 nesta API — usar `substringof('valor', CAMPO)` (sintaxe OData v3) para buscar séries por nome/código.

**`connectors/comexstat.py`** — criado para a quebra da Balança de Bens por país parceiro (ver "Comex Stat/MDIC — pesquisa e decisões" abaixo). Dois gotchas confirmados empiricamente, ambos tratados dentro do connector para que nada silenciosamente errado chegue ao banco:
- **Bug de período multi-ano:** `period.from`/`period.to` da API NÃO é uma janela contínua quando os anos são diferentes — ela aplica o intervalo de MESES em TODO ano do intervalo (ex: `from=1997-01, to=2026-06` não retorna 1997-01→2026-06 contínuo; retorna jan-jun de CADA ano entre 1997 e 2026 — confirmado, 180 linhas = 30 anos × 6 meses, não os ~354 meses esperados). Um range que cruza anos com mês(from) > mês(to) retorna lista vazia, sem erro. `get_trade()` corrige isso fazendo 1 chamada por ano internamente (sempre dentro do mesmo ano civil) e concatenando. Checado contra o OpenAPI da própria API (`/docs/doc.yaml`) — os únicos exemplos documentados usam range dentro de um único ano; a doc não confirma nem descarta comportamento multi-ano, então esse achado é 100% empírico (curl direto), não uma leitura de doc.
- **Rate limit mais severo do que parecia inicialmente:** ~5 chamadas rápidas em sequência bastam para um 429 ("tente novamente em 10 segundos" — mensagem genérica e enganosa). Um throttle proativo (2s entre chamadas) + backoff reativo (11s→60s, 10 tentativas) reduziu a frequência de 429 mas **não foi suficiente** — um backfill de ~300 chamadas em sequência esgotou uma cota que continuou bloqueando por mais de 65s mesmo SEM nenhuma chamada adicional nesse intervalo (confirmado com testes `curl` isolados depois da falha) — indício de uma janela de limite mais longa (minutos, possivelmente mais) do que um burst-limiter comum. Resultado prático: **a API ao vivo não é confiável para o backfill histórico completo** — ver pivô para download em massa abaixo. Fica reservada só para updates marginais (`run()`, janela padrão de 36 meses — poucas dezenas de chamadas).

**`connectors/comexstat_bulk.py`** — criado depois que o backfill via API ao vivo falhou 2x por rate limit (ver acima). Baixa os arquivos anuais estáticos do Comex Stat (`balanca.economia.gov.br/balanca/bd/comexstat-bd/ncm/{EXP,IMP}_{ano}.csv`, NCM-level, `;`-separado) — sem rate limit, porque são downloads de arquivo estático, não chamadas a uma API com cota. É a alternativa que a própria documentação da API recomenda para "consultas muito grandes". Um gotcha de TLS encontrado e corrigido: `balanca.economia.gov.br` envia só o certificado-folha, sem a cadeia intermediária (confirmado via `openssl s_client -showcerts`: 1 certificado, contra 3 em `api-comexstat.mdic.gov.br`) — `requests`/certifi rejeita com `CERTIFICATE_VERIFY_FAILED` porque não faz *AIA fetching* (completar a cadeia buscando o emissor via a extensão Authority Information Access do certificado); `curl`/Windows Schannel fazem isso automaticamente, por isso os testes manuais via `curl` funcionavam sem configuração extra enquanto o `requests` do Python falhava. Corrigido adicionando a dependência `truststore` (`uv add truststore`) e um `HTTPAdapter` customizado que usa verificação nativa do SO em vez do bundle do certifi — mesmo comportamento do Schannel.

**Validação cruzada:** os totais agregados do CSV em massa batem exatamente com os da API ao vivo testada antes da falha — China exportação 2025: `99940244710` (bulk) vs `99940244710` (API); Estados Unidos: `37682246914` em ambas. Confirma que as duas fontes são consistentes entre si — o problema era só a confiabilidade operacional da API para volumes grandes, não os dados.

---

## Relatório HTML — analytics/exchange_rate/

Construído em junho 2026. Arquivo único autocontido (`reports/fx_report.html`, renomeado de `cambio_latest.html` em 2026-07) gerado por `analytics/exchange_rate/generate_report.py` a partir do template `analytics/exchange_rate/report.html`.

### Como atualizar

```powershell
# Atualizar dados (opcional — só se quiser dados mais frescos)
uv run python jobs/update_db.py            # macro_brasil (inclui cmb_reservas_bc, cmb_cambio_contratado, cmb_ptax, cmb_balanco_pagmt, cmb_fluxo_cambial, cmb_termos_troca)
uv run python jobs/update_international.py # macro_international (cmb_reer, cmb_cot_fx, diferenciais_juros)

# Gerar relatório
uv run python -c "from analytics.exchange_rate.generate_report import run; run()"
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
| a | `chart-bop-bens` | mercadorias em geral + ouro não monetário + merchanting (barras) + balança de bens = exportação−importação (linha, total) | barras empilhadas + linha |
| a | `chart-bop-bens-pais` | saldo China/EUA/Argentina/Alemanha + demais países (barras) + total Comex Stat (linha) — fonte diferente do resto da aba (não BPM6, não segue o toggle % PIB) | barras empilhadas + linha |
| a | `chart-bop-bens-fator-agregado` | saldo Básicos/Semimanufaturados/Manufaturados/Demais (barras) + total Comex Stat (linha) — mesma fonte/ressalvas do chart por país; 4 categorias já somam 100% (sem residual) | barras empilhadas + linha |
| a | `chart-bop-bens-produto` | saldo Soja/Petróleo Bruto/Minério de Ferro/Carnes/Café + demais produtos (barras) + total Comex Stat (linha) — mesma fonte/ressalvas do chart por país; NÃO cobre 100% do total (como o chart por país, não o de Fator Agregado) | barras empilhadas + linha |
| a | `chart-bop-servicos` | viagens + transportes + aluguel de equipamentos + demais serviços (barras) + serviços (linha, total) | barras empilhadas + linha |
| a | `chart-bop-renda` | remuneração de empregados + juros + lucros e dividendos (barras) + renda primária (linha, total) | barras empilhadas + linha |
| a | `chart-bop-financial` | investimentos ativos/passivos + derivativos + ativos de reserva (barras) + conta_financeira (linha, total) | barras empilhadas + linha |
| a | `chart-bop-ativos-externos` | IDP no exterior + ações/fundos — ativos + títulos de dívida LP/CP — ativos + outros invest. — ativos (barras) + investimentos ativos (linha, total) | barras empilhadas + linha |
| a | `chart-bop-financiamento` | IDP no país + ações totais + títulos mercado doméstico + empréstimos/títulos LP/CP externo + demais passivos (barras) + investimentos passivos (linha, total) | barras empilhadas + linha |
| heatmap | `chart-heatmap-current` | árvore de 3 níveis, Conta Corrente (ver seção própria abaixo) | heatmap, z-score trimestral |
| heatmap | `chart-heatmap-financial` | árvore de 2 níveis, Conta Financeira | heatmap, z-score trimestral |
| heatmap | `chart-heatmap-capital` | Conta Capital + Erros e Omissões (flat, sem drilldown) | heatmap, z-score trimestral |
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

**Agregação por período (aba BOP, 2026-07):** os 5 charts da aba Balanço de Pagamentos têm um seletor compartilhado (`#bop-period-selector`) — Mensal / Trimestral / Anual (barras empilhadas, `barmode: 'relative'`) ou 12m Acumulado (linha, soma móvel de 12 meses). Motivação: essas séries são composições (partes que somam a um total, validado em `cmb_balanco_pagmt.py`) — barra empilhada comunica "isso construiu aquilo" melhor que linhas sobrepostas; a soma móvel de 12m suaviza a sazonalidade mensal do BOP para leitura de tendência. Trimestral/anual agregam por soma calendário-fixa (`QS`/`YS`, equivalente a `pandas.resample`); se qualquer mês do bucket for `null`, o bucket inteiro vira `null` (evita subestimar silenciosamente). `chart-bop-financial` ganhou linha de total em 2026-07-14 (antes não tinha — ver "Convenção de sinal — Conta Financeira" abaixo para o porquê).

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

Ao processar `analytics/exchange_rate/referencia/balance_payments_breakdown.xlsx` (2026-07), 30 das 40 linhas do quadro condensado que o usuário quer foram resolvidas e cross-checadas (ver `cmb_balanco_pagmt.py`). Restam sem código SGS identificado:
- **Ativos de bancos** vs **Demais ativos** (quebra por setor do lado ativo do balanço) — só encontramos quebra setorial (Banco Central/Bancos/Governo/Demais setores) para o lado ativo em "Moeda e depósitos" (SGS 22982 para bancos); não bate exatamente com o valor do quadro condensado, então não é só essa série.
- **Títulos públicos / Títulos privados / Empréstimos diretos / Demais empréstimos** — quebra por tipo de credor dentro de "Empréstimos e títulos de LP negociados no mercado externo", tanto para Ingressos quanto para Amortizações (8 linhas) — não existe em `analytics/exchange_rate/referencia/balance_payments_breakdown.xlsx` nem no detalhamento BPM6 padrão (códigos 22701–23060).

**Próximos passos (definido com o usuário em 2026-07):** duas linhas de ataque possíveis, ainda em aberto:
1. **Usar a informação do jeito que o BCB fornece** — ao invés de forçar a quebra exata do quadro "Financiamento Externo" (bancos/demais setores, público/privado/direto), aceitar a granularidade que o BPM6 detalhado (`analytics/exchange_rate/referencia/balance_payments_breakdown.xlsx`, aba 1) já oferece nativamente para essas 10 linhas, mesmo que não bata 1:1 com "o quadro que eu quero".
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

#### 7. Balança de Bens — quebra adicional ✓ (feito, 2026-07-14 — quebra por categoria BCB e por país parceiro; quebra por produto/NCM segue em aberto)

`cmb_balanco_pagmt` ganhou 7 novas séries (SGS 22710–22713, 22716–22718), backfilled desde 1995: `mercadorias_gerais` (+`_export`/`_import`), `merchanting`, `ouro_nao_monetario` (+`_export`/`_import`). É a quebra oficial que o próprio BCB já publica dentro do detalhamento BPM6 (mesma planilha `balance_payments_breakdown.xlsx`, aba "BreakDown the bcb provides", já em uso para o resto da tabela — não foi preciso um connector novo). Confirmado aditivo: `mercadorias_gerais + merchanting + ouro_nao_monetario = exportacao_bens − importacao_bens` bate exatamente (testado contra a API, Jan-Mai/2026). `merchanting` é pequeno em módulo (~USD 5–20 mi/mês) e tem convenção de sinal atípica no detalhamento bruto — só o líquido (22713) foi ingerido, sem export/import próprios.

Novo chart `chart-bop-bens` ("Balança de Bens — Detalhe", espelhando "Serviços — Detalhe") na aba BOP, e o nó "Balança de Bens" do Mapa de Calor (Conta Corrente) ganhou 2 níveis de profundidade (Mercadorias em Geral / Ouro Não Monetário — cada um com Exportação/Importação — e Merchanting como folha), substituindo os antigos filhos flat "Exportação de Bens"/"Importação de Bens".

**Quebra por país parceiro ✓ (feito, 2026-07-14):** usuário pediu para pesquisar alternativas — Comex Stat/MDIC confirmado como a fonte oficial de comércio exterior por país/produto (ver pesquisa detalhada abaixo, "Comex Stat/MDIC"). Novo connector `connectors/comexstat.py` (API ao vivo) + `connectors/comexstat_bulk.py` (download em massa) + script `domain/db/brasil/mdic/cmb_comex_pais.py` (`backfill()` via bulk, `run()` via API) + tabela `cmb_comex_pais` (`macro_brasil`), **354 linhas cada série, 1997-01 → 2026-06, sem gaps**. Novo chart `chart-bop-bens-pais` ("Balança de Bens — por País Parceiro") logo abaixo de `chart-bop-bens` na aba BOP: China, Estados Unidos, Argentina, Alemanha (os 4 maiores parceiros por comércio total em 2025) + "Demais Países" (residual). Aditividade confirmada via Node harness (mensal: soma dos 5 = 9.7577 = total; anual: soma dos 5 = 42.3575 = total). **Importante:** Comex Stat usa metodologia de comércio geral (SISCOMEX), não BPM6 — o BCB aplica ajustes documentados para chegar de uma para a outra (bens para transformação, mudança de propriedade sem cruzar fronteira etc.) — por isso o total desta quebra não fecha exatamente com `chart-bop-bens`/`mercadorias_gerais`; é um recorte complementar por parceiro, com seu próprio total interno (`saldo_mundo`), não uma reconciliação linha a linha. Ver seção própria abaixo para detalhes técnicos (gotcha de período da API, rate limit persistente que forçou o pivô para download em massa, gotcha de TLS, escolha dos parceiros).

**Quebra por Fator Agregado ✓ (feito, 2026-07-14 — pedido do usuário: "can we get the balance of payments by product?"):** confirmado antes que essa classificação **não está disponível via a API do Comex Stat**, só via join local contra `NCM.csv`/`NCM_FAT_AGREG.csv` do download em massa. Validado o join primeiro (2025 export: total bate exatamente com o já obtido pela API, `nao_classificado` residual de só 0.04% do total) antes de construir o pipeline completo. Novo connector `connectors/comexstat_bulk.py::get_year_by_fator_agregado()` + script `domain/db/brasil/mdic/cmb_comex_fator_agregado.py` + tabela `cmb_comex_fator_agregado` (`macro_brasil`) — 4 séries agregadas dos 6 códigos oficiais (Básicos, Semimanufaturados, Manufaturados, "Demais" = Transações Especiais + Consumo de Bordo + Reexportação + resíduo não classificado). **Diferente da quebra por país**, aqui as 4 categorias já somam 100% do total (toda transação cai em exatamente 1 categoria) — não precisa de série "mundo" + residual, só a soma direta. Só existe fonte bulk (sem API ao vivo equivalente) — `run()` é um wrapper fino sobre `backfill()` com janela curta (últimos 2 anos, sem risco de rate limit já que é download de arquivo estático). Backfill completo: **354 linhas em basicos/semimanufaturados/manufaturados × export/import; "demais" tem gaps genuínos** (324 linhas export, só 51 import — meses sem nenhuma transação nessas categorias raras, não falha do pipeline) — corrigido com `fillna(0)` em `generate_report.py` antes de calcular saldo/total (ausência de linha = zero real, análogo ao `lucros_reinvestidos` de `cmb_balanco_pagmt`). Novo chart `chart-bop-bens-fator-agregado` ("Balança de Bens — por Categoria de Produto"). Aditividade confirmada via Node harness — e os totais batem EXATAMENTE com os do chart por país para o mesmo período (mensal e anual), confirmando consistência entre as duas quebras da mesma fonte. Sinais batem com o perfil conhecido do comércio brasileiro: Básicos/Semimanufaturados superavitários, Manufaturados deficitário.

**Quebra por produto específico ✓ (feito, 2026-07-14 — usuário apontou: "We don't have the by product information?"):** a quebra por Fator Agregado acima responde "que TIPO de produto" (categorias amplas), não "QUAL produto" — usuário queria os produtos específicos citados originalmente (soja, petróleo). Investigação rápida por capítulo do Sistema Harmonizado (SH2) nos exports de 2025 confirmou os 5 maiores: Petróleo/Combustíveis (cap. 27, US$56.0 Bi), Soja/oleaginosas (cap. 12, US$44.7 Bi), Minérios (cap. 26, US$34.9 Bi), Carnes (cap. 02, US$30.0 Bi), Café/especiarias (cap. 09, US$15.6 Bi) — usuário escolheu via pergunta o conjunto "Top 5" (Petróleo, Soja, Minério de Ferro, Carnes, Café).

**Precisão do código SH escolhida por produto** (verificado numericamente antes de implementar — ver tabela abaixo): para 4 dos 5 produtos, uma única posição SH4 (4 dígitos) domina o capítulo inteiro, então usar o capítulo (SH2) inflaria o número com produtos correlatos mas diferentes — usado SH4 nesses casos. "Carnes" é a exceção: o capítulo 02 se divide genuinamente entre bovina/suína/aves sem uma posição dominante, então manteve o capítulo inteiro (SH2).

| Produto | Código usado | % do capítulo (2025 export) | O que ficaria de fora com o capítulo inteiro |
|---|---|---|---|
| Soja | SH4 `1201` | 97.5% do cap. 12 | Outras sementes oleaginosas (girassol, colza etc.) |
| Petróleo Bruto | SH4 `2709` | 79.6% do cap. 27 | Combustíveis refinados (SH4 `2710`, US$10.3 Bi) — categoria distinta |
| Minério de Ferro | SH4 `2601` | 83.1% do cap. 26 | Minério de cobre e outros (SH4 `2603` etc.) |
| Café | SH4 `0901` | 95.4% do cap. 09 | Chá, mate, especiarias |
| Carnes | SH2 `02` (capítulo inteiro) | 100% (é o próprio capítulo) | — bovina (SH4 `0202`=US$14.4 Bi)/aves (`0207`=US$8.8 Bi)/suína (`0203`=US$3.4 Bi) somadas de propósito |

**Implementação:** `connectors/comexstat_bulk.py` ganhou `get_ncm_sh6()` (correlação NCM→SH6, cacheada) + `get_year_by_produto()` (agrega por prefixo de código SH, aceita SH2 ou SH4 no mesmo dict) + script `domain/db/brasil/mdic/cmb_comex_produto.py` (mesmo padrão de `cmb_comex_pais.py`: série "mundo" + residual "Demais Produtos", já que 5 produtos específicos não cobrem 100% do total) + tabela `cmb_comex_produto`. Séries de import de commodities que o Brasil majoritariamente exporta têm gaps genuínos (`minerio_ferro_import` só 283/354 meses, `soja_import` 339/354, `petroleo_export` 321/354 — ausência real, não falha) — mesmo tratamento `fillna(0)` de `_load_comex_fator_agregado()`.

**Bug de robustez encontrado durante o backfill:** o primeiro `backfill(1997)` falhou no meio (`ChunkedEncodingError`/`IncompleteRead` — conexão caiu depois de já ter recebido `200 OK` e começado a transferir o corpo de ~50MB) — o `Retry` do `urllib3` montado no adapter NÃO cobre esse caso (só retries de conexão/status HTTP, não de leitura de corpo interrompida no meio). Corrigido com `_get_csv_bytes()`, um retry manual (3 tentativas, backoff simples) em volta da leitura de `.content` — aplicado retroativamente também às 2 outras funções de fetch (`get_year`, `get_year_by_fator_agregado`) para a mesma robustez, mesmo que não tivessem falhado ainda.

**Verificação:** Node harness confirmou aditividade (mensal: soma dos 6 = 9.7577 = total; anual: soma dos 6 = 42.3575 = total) — **os totais batem EXATAMENTE com os das outras 2 quebras Comex Stat** (por país e por Fator Agregado) para os mesmos períodos, uma terceira confirmação cruzada de consistência entre as 3 tabelas. Sinais econômicos fazem sentido: os 5 produtos nomeados são todos superavitários (Soja +28.9 Bi, Petróleo +24.6 Bi, Minério +13.4 Bi, Carnes +16.5 Bi, Café +5.9 Bi no acumulado 2026 parcial) e "Demais Produtos" é bem negativo (-47.1 Bi) — absorve o déficit de manufaturados já visto na quebra por Fator Agregado.

#### 8. Métricas em % do PIB ✓ (feito, 2026-07-14)

Botão "USD Bi / % do PIB" adicionado no topo da aba BOP, ao lado do seletor de período — aplica-se aos 7 gráficos de composição. Usa nova tabela `atv_pib_usd` (BCB SGS 4385, PIB mensal em USD — não é `atv_pib`, que é trimestral em R$ via IBGE). Ver seção própria abaixo ("Botão 'USD Bi / % do PIB'...") para a convenção de agregação por período e a verificação numérica.

#### 9. Melhorias no Mapa de Calor (registrado 2026-07)

- ~~Altura fixa do card desproporcional quando poucas linhas visíveis~~ ✓ resolvido 2026-07-14 — ver "Ajustes de UX" abaixo (altura agora dinâmica por painel).
- Espaço para outras melhorias a definir (ex: exportar/imprimir o estado expandido, indicador visual de "quantas colunas iniciais estão em branco" por falta de baseline de 3 anos, etc.) — usuário não especificou detalhes ainda.

### Ajustes de UX e correção de dados (2026-07-14)

Pedidos do usuário após revisão do relatório já em uso — cinco itens:

1. **USD mi → USD Bi:** todas as séries em USD (BOP, posicionamento BCB — reservas/ouro/swap/intervenções —, fluxo cambial) convertidas para bilhões na camada de dados (`generate_report.py`, `/1000` logo após o pivot), não só no rótulo — z-score do heatmap é invariante a escala, mas o valor bruto exibido em cada célula/hover muda de fato. PTAX, REER, diferenciais de juros e COT não usam USD nominal e não foram tocados.

2. **"Lucros e Dividendos" 2000–2010 — verificado, era um gap real da fonte BCB, não um bug do pipeline.** `lucros_reinvestidos` (SGS 22815) não tem dado publicado pelo BCB entre 1999-01 e 2009-12 (confirmado direto na API: HTTP 404 "Value(s) not found" para essa janela — a série volta a existir a partir de 2010-01, provavelmente por causa da transição de metodologia BPM5→BPM6). Como `lucros_dividendos = lucros_remetidos + lucros_reinvestidos + lucros_dividendos_carteira`, a soma propagava `NaN` pela década inteira mesmo com as outras duas parcelas presentes — o componente sumia do gráfico de composição nesses anos. Fix: `fillna(0)` em `lucros_reinvestidos` antes da soma (ver docstring de `cmb_balanco_pagmt.py`); a Renda Primária (linha de total) nunca foi afetada, pois vem direto do agregado oficial do BCB, não da soma dos componentes.

3. **Trimestres rotulados pelo mês final (mar/jun/set/dez), não inicial (jan/abr/jul/out).** `bucketStartDate()` em `report.html` usava o primeiro mês do trimestre como data de rótulo; ajustado para o último mês — convenção mais comum de leitura de trimestre fiscal. Só afeta o rótulo do eixo X — a soma trimestral em si (quais meses entram em cada bucket) não mudou.

4. **Notas explicativas em todos os gráficos:** cada seção agora tem um `.note` com 1–2 frases sobre o que a série representa (ex: o que é REER, o que é Financiamento Externo, o que significa net comprado no COT) — antes só ~3 seções tinham nota, e eram técnicas (sobre a fonte/cálculo), não explicativas sobre o conceito.

5. **Mapa de Calor dividido em 3 painéis** (Conta Corrente / Conta Financeira / Conta de Capital + Erros e Omissões), cada um com seu próprio estado de expansão e altura de card dinâmica (`chromePx + linhas_visíveis * rowPx`, 220–820px) — resolve a pendência conhecida de linhas desproporcionalmente altas quando poucas estão visíveis. Erros e Omissões foi agrupado com Conta Capital (não é uma das 3 contas nomeadas do BP, mas também não justifica um painel próprio de 1 linha). Página alargada (`main`, 1440px → 1800px).
   - **Valor escrito em cada célula, mas só sob zoom suficiente:** primeira tentativa (`texttemplate: '%{text}'` sempre ativo) ficou ilegível com o histórico completo (~126 colunas trimestrais) — texto de células vizinhas se sobrepõe e vira ruído. Corrigido com `applyHeatmapTextVisibility()`: liga o texto (via `Plotly.restyle`) só quando o range visível no eixo X tem ≤32 colunas (~8 anos — cabe sem sobrepor numa área de plotagem de ~1450px), escutando `plotly_relayout` (dispara tanto em zoom manual quanto nos botões "1a/3a/5a/10a/Tudo"). Com o histórico completo visível, só a cor fica ativa (valor exato continua no hover). Números arredondados para 1 casa decimal (era 2 — ajuste pedido pelo usuário).

6. **Hoverformat nos gráficos em USD Bi:** o item 1 converteu os valores para Bi, mas não arredondava o hover (Plotly mostra float cheio por padrão, ex. "1.7888") — `yaxis.hoverformat: '.1f'` adicionado em todos os charts de BOP/BCB Positioning/Fluxo Cambial (PTAX ficou de fora — cotação precisa de mais casas decimais).

### Convenção de sinal — Conta Financeira (2026-07-14, pedido do usuário)

**Objetivo:** o usuário quer ler a Conta Financeira como "contraparte" da Conta Corrente, com uma única regra em todo o relatório: **negativo = saída de USD do Brasil, positivo = entrada de USD** — a mesma leitura que Conta Corrente já tem (déficit/negativo = saída).

**Descoberta ao verificar dado real (Ativos, maio/2026 = -745):** o BPM6 publicado pelo BCB usa convenções opostas para Ativos e Passivos — positivo em Ativos = aumento de ativo no exterior = SAÍDA de USD; positivo em Passivos = aumento de passivo externo = ENTRADA de USD (confirmado numericamente: `investimento_direto_liquido`, a maior componente de Passivos, é consistentemente positivo todo mês — IDE líquido positivo é a norma no Brasil). Isso significa que **só o lado Ativos precisa ser invertido** para bater com a regra desejada — Passivos já publica na convenção certa e não deveria ser tocado.

**Correção de rumo nesta sessão:** a primeira tentativa inverteu Passivos (raciocínio: "Ativos e Passivos parecem andar juntos no mesmo gráfico, uniformizar os dois para 'positivo = saída' em ambos") — isso resolvia a inconsistência *entre* Ativos e Passivos, mas na direção errada para o objetivo real (comparar com Conta Corrente). Corrigido depois de o usuário testar o valor de maio/2026 passo a passo comigo e apontar a contradição. Lição: verificar a direção do sinal contra um exemplo numérico real e contra o objetivo final (aqui, "contraparte da Conta Corrente"), não só contra consistência interna entre duas séries.

**Implementação final** (`generate_report.py::_load_bop()`), tudo aplicado só na camada do relatório, ANTES de qualquer fórmula rodar (fórmulas são combinações lineares, então invertem corretamente sem precisar reescrever nada):
- Invertido: `idp_exterior`, `portfolio_ativos`, `outros_inv_ativos` (→ `investimentos_ativos`), `derivativos`, `ativos_reserva`, `conta_financeira` (total oficial).
- NÃO invertido: `investimento_direto_liquido`, `portfolio_passivos`, `acoes_passivos`, `fundos_passivos`, `titulos_dom`, `titulos_externo_cp`, `titulos_externo_lp`, `emprestimos_cp_passivos`, `emprestimos_lp_passivos`, `outros_inv_passivos` (→ `investimentos_passivos` e tudo que dele deriva) — já publica na convenção desejada.
- `Ativos de Reserva` também invertido, por decisão explícita do usuário: quando o BC aumenta reservas (positivo na fonte), esse USD é absorvido pelo BC em vez de ficar disponível — mesma direção de "saída" que Ativos.
- `conta_financeira` (total oficial, SGS 22863) precisou ser invertido também para a identidade continuar fechando: originalmente `conta_financeira = investimentos_ativos − investimentos_passivos + derivativos + ativos_reserva` (Passivos entra subtraído — convenção "Concessões líquidas(+)/Captações líquidas(-)"); invertendo ativos/derivativos/reserva e mantendo passivos como está, só fecha invertendo `conta_financeira` também. Confirmado numericamente para maio/2026 (soma dos 4 componentes = 3.7157, `conta_financeira` invertido = 3.7159 — bate dentro do arredondamento).
- **Bônus:** com a identidade voltando a fechar como soma direta, `chart-bop-financial` ("Conta Financeira — Ativos vs Passivos") ganhou linha de total pela primeira vez — antes não tinha, porque a soma dos 4 componentes não batia com o total.
- **Bug encontrado de graça nesse processo:** `outros_inv_ativos` era referenciado pelo nó "Outros Investimentos — Ativos" do Mapa de Calor mas nunca tinha sido incluído na lista de passthrough de `_load_bop()` — a linha vinha em branco desde sempre. Corrigido junto (adicionado à lista).
- `Investimentos — Passivos` e "Financiamento Externo — Passivos" (`chart-bop-financiamento`) permanecem exatamente na convenção original do BCB, sem alteração.

**Verificação:** script Node.js executou o JS extraído do HTML gerado contra um stub mínimo de `document`/`Plotly` (mesma técnica já usada para `rollingZScore()` — ver "Verificação" na seção do Mapa de Calor original) — confirmado sem erros de runtime, valores em USD Bi na faixa esperada (ex: reservas ~USD 371 Bi em 2026-05, bate com o número real de reservas do Brasil), e rótulos trimestrais terminando em `-03-01`/`-06-01`/`-09-01`/`-12-01`.

**Breakdown "Ativos" adicionado (2026-07-14, pedido do usuário: "it's missing the breakdown of the asset part"):** `chart-bop-financiamento` ("Financiamento Externo — Passivos") já detalhava o lado Passivos, mas não havia equivalente para Ativos — adicionado `chart-bop-ativos-externos` ("Investimentos no Exterior — Ativos"), inicialmente com 3 linhas (IDP no exterior + carteira — ativos, lump + outros investimentos — ativos).

**Refinamento (mesma sessão, pedido do usuário):** usuário pediu para usar a granularidade da aba oficial "BreakDown the bcb provides" (`balance_payments_breakdown.xlsx`), separando investimento direto de investimento em carteira, e — dada a opção — escolheu abrir Carteira em Ações+Fundos e Títulos de Dívida CP/LP separados, no mesmo nível de detalhe já usado no lado Passivos (`chart-bop-financiamento`). 4 novas séries adicionadas a `cmb_balanco_pagmt` (SGS 22909/22912/22918/22921 — ver docstring de `cmb_balanco_pagmt.py`), backfilled `start='01/01/1995'` (377 linhas cada, sem gaps). `chart-bop-ativos-externos` agora tem 5 linhas: IDP no Exterior, Ações e Fundos — Ativos, Títulos de Dívida — Ativos (LP), Títulos de Dívida — Ativos (CP), Outros Investimentos — Ativos. Aditividade confirmada numericamente (Node harness, maio/2026: soma dos 5 componentes = 0.7452, `investimentos_ativos` = 0.7451). As 4 novas séries entram em `_INVERTED_COLS` em `_load_bop()` — herdam a mesma inversão de sinal de `portfolio_ativos` (do qual são subitens), pela mesma lógica documentada acima.

### Botão "USD Bi / % do PIB" na aba Balanço de Pagamentos (2026-07-14, pedido do usuário)

Usuário encontrou a série SGS 4385 ("GDP monthly in dollar") no buscador de séries do BCB e pediu um botão no topo da aba para alternar entre valor absoluto (USD Bi) e % do PIB.

**Nova tabela `atv_pib_usd`** (`domain/db/brasil/bcb/atv_pib_usd.py`) — série única, SGS 4385, PIB mensal do Brasil em USD (BCB/Depec). Prefixo `atv_` porque é dado de atividade por natureza (independente de quem consome — ver critério de classificação do projeto), não `cmb_`, mesmo sendo usada só pelo relatório cambial por ora. Tabela nova (schema idêntico às demais: `date`, `name`, `value`, `PRIMARY KEY (date, name)`), sem relação com `atv_pib` (PIB trimestral IBGE em R$, tabela e propósito diferentes). Backfilled `start='01/01/1995'` (378 linhas, 1995-01 a 2026-06 — um mês à frente de `cmb_balanco_pagmt`, sem problema porque o reindex em `_load_bop()` alinha pelo índice do BOP). Adicionada a `jobs/update_db.py`.

**Alinhamento em `generate_report.py::_load_bop()`:** `atv_pib_usd` é lida e reindexada ao índice de datas de `cmb_balanco_pagmt` (`gdp_wide["pib_usd"].reindex(wide.index)`), convertida para USD Bi (`/1000`), e exposta como `REPORT_DATA.bop.gdp_usd_bi` — mesmo array de datas que todas as outras séries da aba.

**Escopo do toggle (decisão via pergunta ao usuário):** aplica-se aos 7 gráficos de composição da aba (`chart-bop-current`, `-bens`, `-servicos`, `-renda`, `-financial`, `-ativos-externos`, `-financiamento`) — não ao Mapa de Calor (que já usa uma normalização própria via z-score).

**Convenção de agregação por período:** `renderComposition()` ganhou parâmetros opcionais `gdpValues`/`mode`. Quando `mode === 'pct'`, o PIB é agregado pela MESMA regra do período ativo (`aggregateSum` para mensal/trimestral/anual, `rollingSum12` para 12m acumulado) antes da divisão — ou seja, o bucket anual divide a soma de 12 meses de fluxo pela soma de 12 meses de PIB, não pelo PIB de um mês isolado. É a convenção usual de "déficit em conta corrente como % do PIB" (razão entre duas somas na mesma janela, não razão instantânea mês-a-mês). Como as fórmulas de agregação (`aggregateSum`/`rollingSum12`) já eram lineares e reaproveitadas, converter para % só exigiu dividir depois de agregar — não antes.

**Verificação:** Node harness re-executando `renderBopCharts('annual', 'pct')` contra o script extraído do HTML gerado — bucket 2025 de Conta Corrente: soma = -66.72 USD Bi, PIB somado = 2280.89 USD Bi, razão = -2.925% (compatível com o histórico real de déficit em conta corrente do Brasil, ~1-3% do PIB) — 2023 (-1.23%) e 2024 (-2.99%) também na faixa esperada.

### Comex Stat/MDIC — pesquisa e decisões (2026-07-14, pedido do usuário: "search for a better decomposition of the Balance of goods")

Usuário pediu para pesquisar alternativas à quebra da Balança de Bens (que já tinha Mercadorias em Geral/Ouro/Merchanting, mas nada por produto ou país — pendência registrada no item 7 acima desde a sessão anterior). Pesquisa (agente dedicado + verificação direta via `curl` contra a API ao vivo) confirmou o Comex Stat/MDIC como a fonte oficial.

**O que existe na fonte:**
- API pública sem autenticação (`https://api-comexstat.mdic.gov.br`), cobertura 1997-01 → hoje, atualizada ~3 dias após o fechamento do mês (mais rápido que a Balança de Pagamentos do BCB). Valores em USD FOB.
- Quebras disponíveis via API: país, bloco econômico (blocos se sobrepõem entre si — Ásia inclui ASEAN, Europa inclui UE, América do Sul inclui Mercosul — não formam uma partição própria para um gráfico empilhado), NCM (8 dígitos), Sistema Harmonizado em 4 níveis, CGCE, CUCI/SITC, ISIC.
- **A quebra clássica brasileira "Fator Agregado" (Básicos/Semimanufaturados/Manufaturados) NÃO está disponível via API** — confirmado checando `/general/filters` diretamente — só existe no arquivo de correlação `NCM.csv` do download em massa (`balanca.economia.gov.br`), teria que ser feito join local por código NCM.
- Metodologia "comércio geral" (registro aduaneiro/SISCOMEX), **não BPM6** — o BCB aplica ajustes documentados (bens para transformação que cruzam fronteira sem mudança de propriedade, bens que mudam de propriedade sem cruzar fronteira, etc.) para chegar da base Comex Stat/SECEX até `mercadorias_gerais`. Os dois não devem ser somados/comparados linha a linha.
- Rate limit agressivo (confirmado: ~5 chamadas rápidas → 429) — a própria documentação da API recomenda os arquivos de download em massa para consultas grandes/históricas em vez da API.

**Decisão (via pergunta ao usuário):** começar pela quebra mais simples — país/bloco parceiro — deixando a quebra por produto (Fator Agregado, via download em massa + join) para uma fase 2. Fase 2 feita na mesma sessão, logo em seguida (usuário: "can we get the balance of payments by product?") — ver item "Quebra por Fator Agregado" acima.

**Pivô de arquitetura no meio da implementação (mesma sessão):** a primeira tentativa de backfill histórico (1997→2026, ~300 chamadas via `connectors/comexstat.py`) falhou duas vezes por rate limit — na segunda vez, mesmo esperando 65+ segundos SEM nenhuma chamada adicional, a API continuou retornando 429. Isso indicou uma cota de duração mais longa do que um burst-limiter comum, não contornável com backoff dentro de uma única execução. Usuário perguntou diretamente "did you see the documentation?" — resposta honesta: não, a conclusão veio de teste empírico direto (`curl`), não de leitura prévia da doc; checando depois o OpenAPI (`/docs/doc.yaml`), os exemplos ali só cobrem ranges de um único ano, então a doc não confirma nem contradiz o achado — ela simplesmente não fala sobre isso. Usuário então perguntou "Can we use the csv to get the historical and the marginal update by the API?" — confirmado que sim, essa é exatamente a divisão de responsabilidade que a própria documentação do Comex Stat recomenda para "consultas muito grandes".

**Implementação final:**
- `connectors/comexstat.py` — API ao vivo, usada só para updates marginais (`run()`, default 36 meses). Ver tabela de connectors acima para os 2 gotchas confirmados e corrigidos (bug de período multi-ano, rate limit).
- `connectors/comexstat_bulk.py` (novo, criado depois do pivô) — download em massa (`balanca.economia.gov.br`), sem rate limit, usado para a carga histórica completa. Gotcha de TLS encontrado e corrigido via `truststore` — ver tabela de connectors acima.
- `domain/db/brasil/mdic/cmb_comex_pais.py` (novo, pasta `mdic/` nova ao lado de `bcb/`/`ibge/`/`ipea/`) → tabela `cmb_comex_pais`. Duas funções: `backfill(start_year=1997)` (bulk, insere incrementalmente por ano×flow — uma falha no meio não descarta o que já foi buscado, ao contrário da primeira versão que só inseria uma vez no final) e `run(n_meses=36)` (API ao vivo, update rotineiro — a única chamada em `jobs/update_db.py`). Parceiros escolhidos: os 4 maiores por comércio total (export+import) em 2025 — China (US$170.8 Bi), Estados Unidos (US$82.8 Bi), Argentina (US$31.0 Bi), Alemanha (US$20.9 Bi), juntos ~70% do comércio de bens do Brasil — mais o total mundial (`mundo_export`/`mundo_import`, sem filtro de país), que permite calcular "Demais Países" como residual na camada de consumo sem precisar buscar os ~200 parceiros individualmente. Backfill completo executado com sucesso via `backfill(1997)`: **354 linhas por série, 1997-01 → 2026-06, sem gaps**, ~60 downloads (30 anos × 2 fluxos), sem nenhum 429.
- `generate_report.py::_load_comex_pais()` — calcula saldo (export−import) por parceiro e `saldo_demais = saldo_mundo − soma dos 4 parceiros`; expõe `REPORT_DATA.comex_pais` (dict próprio, separado de `REPORT_DATA.bop` — fonte/índice de datas diferentes). Valores já vêm em USD (não USD MM, diferente de `cmb_balanco_pagmt`) — convertidos para USD Bi via `/1e9`.
- Novo chart `chart-bop-bens-pais` ("Balança de Bens — por País Parceiro"), logo abaixo de `chart-bop-bens` na aba BOP. Segue o seletor de período (Mensal/Trimestral/Anual/12m) mas **não** o toggle "% do PIB" (fonte/metodologia diferentes das demais séries da aba — nota explícita no HTML).

**Verificação:** valores agregados do bulk CSV batem exatamente com a API ao vivo testada antes da falha (China export 2025: `99940244710` nas duas fontes; EUA: `37682246914` nas duas). Node harness confirmou aditividade do chart: mensal (jun/2026) soma dos 5 componentes = 9.7577, total = 9.7577; anual (2026 parcial) soma = 42.3575, total = 42.3575.

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
| `cmb_balanco_pagmt` | `macro_brasil` | 1995 → hoje | ✓ (reestruturada 2026-07, 52 séries) |
| `atv_pib_usd` | `macro_brasil` | 1995 → hoje | ✓ (nova 2026-07-14, PIB mensal USD para normalização % PIB) |
| `cmb_fluxo_cambial` | `macro_brasil` | 2003 → hoje | ✓ |
| `cmb_reservas_bc` | `macro_brasil` | 1971 → hoje | ✓ 22 séries (doc anterior estava desatualizado) |
| `cmb_cambio_contratado` | `macro_brasil` | 1982 → hoje | ✓ |
| `cmb_ptax` | `macro_brasil` | 1984 → hoje | ✓ (feito 2026-07; chart-ptax no relatório) |
| `cmb_termos_troca` | `macro_brasil` | 1978 → hoje | ✓ (feito 2026-07, fonte corrigida para Funcex/IPEADATA) |

- Adicionar no `generate_report.py` um campo `data_range` no JSON por seção (para exibir no tooltip do chart header: "2006 – jun/2026")

---

### Fase 3 — Agente de análise ✓ (feito, 2026-07, arquitetura diferente da originalmente planejada)

**Implementado como:** um subagente Claude Code (`.claude/agents/cambio-analyst.md`) que roda `analytics/exchange_rate/agent_data.py` (`get_fx_snapshot()` — snapshot data-only: último valor + deltas 1m/3m/12m por série, reaproveitando os loaders de `generate_report.py`) e conecta os movimentos de dados a conceitos já curados em `obsidian/exchange_rate/concepts/` (UIP, carry trade, REER/PPP, BOP, crises cambiais etc.). Resposta conversacional por padrão; gera relatório markdown em `reports/cambio_analysis_<data>.md` quando solicitado — não escreve nem regenera `reports/cambio_latest.html`.

**Por que a arquitetura mudou em relação ao plano original abaixo (histórico):** o plano original previa uma pasta `bibliography/` de PDFs novos + chamada direta à API Anthropic (`analyze.py`) injetando narrativa estática no HTML. Optou-se por reaproveitar o conhecimento conceitual já existente em `obsidian/exchange_rate/` (evita duplicar uma segunda base de textos) e por um subagente Claude Code interativo/on-demand (evita builds de narrativa estática que ficam desatualizadas assim que os dados mudam). `agent_bibliography/` continua deliberadamente fora do escopo deste agente — sistema paralelo, sem reconciliação (ver `CLAUDE.md`).

**Pendências conhecidas:**
- ~~Sem série de câmbio à vista (PTAX) no banco~~ ✓ resolvido 2026-07: `macro_brasil.cmb_ptax` (PTAX + volume interbancário), e `analytics/exchange_rate/agent_data.py` atualizado para incluir o grupo `ptax` no snapshot.
- **Sem allowlist de permissões Bash em `.claude/settings.json`** — cada chamada do agente ao script (`uv run python ...`) pede confirmação até isso ser configurado separadamente (skill `fewer-permission-prompts`/`update-config`).
- **Casamento de conceitos do obsidian é um julgamento do LLM, não uma busca estruturada** — `concepts/*.md` não tem índice de tags parseável, só uma linha `**Tags:**` em texto livre e nomes de arquivo.

<details>
<summary>Plano original (histórico, superseded)</summary>

**Objetivo:** ao rodar o relatório, um agente lê os dados atuais + uma biblioteca de textos selecionados e gera uma narrativa analítica estruturada, incorporada ao HTML ou exportada como documento separado.

#### Arquitetura proposta

```
analytics/exchange_rate/
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

O diretório `analytics/exchange_rate/bibliography/` deve conter textos relevantes para análise do BRL. Exemplos de conteúdo útil:
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
