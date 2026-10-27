# F(A) — expectativas — ciclo 2026-10-02

Gerado em 2026-10-22 16:23. Dados do banco até 2026-10-02, fixos durante o ciclo. Sem ciclo anterior.

Os dados brutos (A) estão em `A/`, um arquivo por tabela; as funções G leem de lá e o código delas fica em `G/`. Nada aqui é opinião: é a mesma conta em todo ciclo.

Como ler:
- **Δ% 1m/3m/12m**: variação contra o último valor de 1, 3 e 12 meses antes da última data da série; numa série trimestral, **1t/4t**: contra 1 e 4 trimestres antes.
- **Δ**: diferença na unidade da série (p.p. quando a série é %, p.b. quando é p.b.).
- **Pctl**: posição do último valor no histórico, de 0 (o menor já visto) a 100 (o maior). "10a" = últimos 10 anos.
- **Soma 3m/12m**: soma dos últimos 3 e 12 meses completos; o mês em curso aparece à parte e não entra nas somas.
- **Acum.**: variação composta.

## i. Endógeno (leitura completa)

### expc_focus (inflação)

Último dado 2026-10-02 (no corte) · A: `A/expc_focus__inflacao.csv.gz`

**A variável da tese**: Focus IPCA 12 meses à frente, suavizada, base de 30 dias, mediana, **média das pesquisas do trimestre** (a `pi_e` do Modelo Estrutural). É o que o placar compara.

| Trimestre | Média do trimestre (% a.a.) | Pesquisas |  |
|---|---|---|---|
| 4T26 | 4.59 | 2 | em curso, menos da metade das pesquisas |
| 3T26 | 4.37 | 65 |  |
| 2T26 | 4.05 | 61 |  |
| 1T26 | 4.00 | 61 |  |
| 4T25 | 4.09 | 64 |  |
| 3T25 | 4.44 | 66 |  |
| 2T25 | 4.88 | 61 |  |

IPCA e componentes, mediana da pesquisa suavizada, base de 30 dias, % nos próximos 12 ou 24 meses. Pesquisa mais recente: 2026-10-02. Comparações: 4 sem. = 2026-09-04, 13 sem. = 2026-07-03. O histórico dos componentes é curto (a pesquisa os acrescentou depois): o percentil vale para a janela da coluna Desde.

| Indicador | Horizonte | Mediana (2026-10-02) | Δ 4 sem. | Δ 13 sem. | Desvio-padrão | Pctl hist. | Desde |
|---|---|---|---|---|---|---|---|
| IPCA | 12m | 4.59 | -0.01 | +0.49 | 0.48 | 43 | 2001-12-12 |
| IPCA | 24m | 3.93 | -0.01 | -0.00 | 0.42 | 69 | 2021-03-31 |
| Livres | 12m | 4.77 | +0.12 | +0.20 | 0.67 | 63 | 2021-09-14 |
| Livres | 24m | 3.96 | -0.04 | -0.11 | 0.52 | 70 | 2021-09-14 |
| Administrados | 12m | 4.13 | -0.30 | +0.66 | 0.76 | 45 | 2021-09-17 |
| Administrados | 24m | 3.63 | -0.01 | +0.00 | 0.63 | 8 | 2021-09-17 |
| Serviços | 12m | 5.15 | +0.02 | -0.10 | 0.61 | 35 | 2021-09-14 |
| Serviços | 24m | 4.78 | -0.03 | -0.01 | 0.70 | 71 | 2021-09-14 |
| Bens industrializados | 12m | 2.68 | -0.03 | -0.21 | 0.58 | 33 | 2021-09-14 |
| Bens industrializados | 24m | 2.76 | +0.01 | +0.06 | 0.65 | 46 | 2021-09-14 |
| Alimentação no domicílio | 12m | 6.95 | +0.63 | +1.93 | 1.84 | 99 | 2021-09-14 |
| Alimentação no domicílio | 24m | 4.30 | -0.19 | -0.20 | 1.62 | 74 | 2021-09-14 |

IPCA, dispersão e respostas frescas. A base de 4 dias úteis só conta quem respondeu nos últimos dias: quando ela se afasta da de 30 dias, há revisão em curso que a mediana ainda não mostra. Média acima da mediana = cauda de respondentes acima.

| Horizonte | Mediana, 30 dias | Mediana, 4 dias úteis | 4 dias − 30 dias (p.p.) | Média − mediana | Desvio-padrão | Pctl desvio hist. | Mín–máx | Respondentes (30 d / 4 d) |
|---|---|---|---|---|---|---|---|---|
| 12m | 4.59 | 4.65 | +0.06 | -0.01 | 0.48 | 76 | 3.10 a 6.08 | 132 / 35 |
| 24m | 3.93 | 3.90 | -0.03 | +0.00 | 0.42 | 35 | 2.90 a 5.11 | 89 / 25 |

### expc_focus_periodo (inflação)

Último dado 2026-10-02 (no corte) · A: `A/expc_focus_periodo__inflacao.csv.gz`

**Por ano-calendário**, mediana de 2026-10-02 e, entre parênteses, a variação em 4 semanas (desde 2026-09-04), em p.p. A meta de anos ainda não fixados é a última publicada.

| Indicador | 2026 | 2027 | 2028 | 2029 | 2030 |
|---|---|---|---|---|---|
| IPCA | 5.01 (+0.01) | 4.30 (+0.01) | 3.80 (+0.00) | 3.51 (+0.01) | 3.50 (+0.00) |
| Livres | 5.14 (-0.00) | 4.49 (+0.05) | 3.90 (+0.00) | 3.56 (-0.01) | 3.55 (+0.01) |
| Administrados | 4.61 (-0.10) | 3.84 (+0.05) | 3.62 (+0.01) | 3.50 (+0.00) | 3.50 (+0.00) |
| Serviços | 5.47 (-0.11) | 5.07 (+0.01) | 4.50 (+0.00) | 4.00 (+0.00) | 4.00 (+0.00) |
| Bens industrializados | 3.50 (-0.05) | 2.73 (+0.02) | 2.80 (+0.01) | 2.98 (+0.02) | 3.00 (+0.00) |
| Alimentação no domicílio | 6.88 (+0.63) | 5.66 (+0.08) | 4.00 (+0.00) | 4.00 (+0.00) | 4.00 (+0.00) |
| Meta do CMN | 3.00 | 3.00 | 3.00 | 3.00 | 3.00 |

IPCA por ano: dispersão das respostas.

| Ano | Mediana | Média | Desvio-padrão | Mín–máx | Respondentes |
|---|---|---|---|---|---|
| 2026 | 5.01 | 5.00 | 0.22 | 4.34 a 5.90 | 144 |
| 2027 | 4.30 | 4.33 | 0.42 | 3.17 a 6.00 | 144 |
| 2028 | 3.80 | 3.83 | 0.45 | 3.00 a 6.00 | 118 |
| 2029 | 3.51 | 3.68 | 0.48 | 3.00 a 6.00 | 110 |
| 2030 | 3.50 | 3.66 | 0.50 | 3.00 a 6.00 | 105 |

IPCA nos próximos 6 períodos, por trimestre (variação no período, %).

| Referência | Mediana (%) | Δ 4 sem. | Desvio-padrão |
|---|---|---|---|
| 3/2026 | 0.35 | -0.04 | 0.12 |
| 4/2026 | 1.24 | +0.04 | 0.17 |
| 1/2027 | 1.55 | +0.03 | 0.27 |
| 2/2027 | 0.97 | +0.02 | 0.16 |
| 3/2027 | 0.65 | -0.01 | 0.20 |
| 4/2027 | 1.06 | -0.03 | 0.20 |

IPCA nos próximos 6 períodos, por mês (variação no período, %).

| Referência | Mediana (%) | Δ 4 sem. | Desvio-padrão |
|---|---|---|---|
| 09/2026 | 0.60 | +0.07 | 0.12 |
| 10/2026 | 0.32 | -0.01 | 0.08 |
| 11/2026 | 0.35 | +0.03 | 0.09 |
| 12/2026 | 0.56 | +0.03 | 0.09 |
| 01/2027 | 0.45 | +0.01 | 0.14 |
| 02/2027 | 0.66 | +0.02 | 0.13 |

### expc_focus_periodo (PIB)

Último dado 2026-10-02 (no corte) · A: `A/expc_focus_periodo__pib.csv.gz`

Crescimento real esperado no ano, %, mediana de 2026-10-02; variações em p.p. contra 2026-09-04 (4 sem.) e 2026-07-03 (13 sem.). Setores e componentes da demanda entraram na pesquisa em set/2021.

| Componente | 2026 | Δ 4 sem. 2026 | Δ 13 sem. 2026 | 2027 | Δ 4 sem. 2027 | Δ 13 sem. 2027 | 2028 | Δ 4 sem. 2028 | Δ 13 sem. 2028 |
|---|---|---|---|---|---|---|---|---|---|
| PIB | 1.85 | -0.08 | -0.13 | 1.40 | -0.10 | -0.29 | 1.81 | -0.15 | -0.19 |
| Agropecuária | 2.40 | +0.90 | +0.70 | 1.00 | -0.90 | -1.30 | 2.50 | +0.00 | -0.03 |
| Indústria | 1.57 | -0.23 | -0.21 | 1.10 | -0.10 | -0.40 | 1.70 | +0.00 | +0.00 |
| Serviços | 1.80 | -0.20 | -0.18 | 1.50 | +0.00 | -0.20 | 1.80 | -0.10 | -0.20 |
| Consumo das famílias | 1.40 | -0.50 | -0.60 | 1.40 | -0.10 | -0.22 | 1.80 | +0.00 | -0.18 |
| Consumo do governo | 2.20 | +0.10 | +0.10 | 1.21 | -0.02 | +0.01 | 1.32 | +0.02 | -0.03 |
| Investimento (FBCF) | 0.90 | +0.00 | -0.10 | 1.08 | -0.07 | -0.42 | 1.75 | +0.05 | -0.19 |
| Exportação | 4.27 | -0.13 | +0.07 | 3.00 | +0.00 | +0.00 | 3.00 | +0.00 | +0.00 |
| Importação | 3.00 | +0.08 | +0.20 | 1.85 | +0.05 | -0.15 | 2.00 | +0.00 | +0.00 |

PIB por trimestre (unidade da pesquisa: %).

| Trimestre | Mediana (%) | Δ 4 sem. |
|---|---|---|
| 3/2026 | 1.80 | -0.17 |
| 4/2026 | 1.77 | -0.13 |
| 1/2027 | 1.40 | -0.20 |
| 2/2027 | 1.40 | -0.10 |
| 3/2027 | 1.40 | -0.10 |
| 4/2027 | 1.50 | +0.00 |

### expc_focus_periodo (Selic)

Último dado 2026-10-02 (no corte) · A: `A/expc_focus_periodo__selic.csv.gz`

Unidade: %. Mediana da pesquisa (janela de 30 dias).

| Ano | Mediana (2026-10-02) | 4 sem. antes (2026-09-04) | 13 sem. antes (2026-07-03) | Δ 4 sem. | Respondentes |
|---|---|---|---|---|---|
| 2026 | 13.50 | 13.75 | 14.00 | -0.25 | 139 |
| 2027 | 12.00 | 12.00 | 12.00 | +0.00 | 138 |
| 2028 | 10.50 | 10.50 | 10.50 | +0.00 | 115 |
| 2029 | 10.00 | 10.00 | 10.00 | +0.00 | 108 |

Dispersão das respostas, mesma pesquisa:

| Ano | Desvio-padrão | Mín–máx |
|---|---|---|
| 2026 | 0.22 | 13.00 a 14.00 |
| 2027 | 0.73 | 9.75 a 14.00 |
| 2028 | 0.88 | 8.00 a 13.50 |
| 2029 | 0.94 | 8.00 a 13.50 |

### expc_focus_periodo (câmbio)

Último dado 2026-10-02 (no corte) · A: `A/expc_focus_periodo__cambio.csv.gz`

Unidade: R$/US$. Mediana da pesquisa (janela de 30 dias).

| Ano | Mediana (2026-10-02) | 4 sem. antes (2026-09-04) | 13 sem. antes (2026-07-03) | Δ 4 sem. | Respondentes |
|---|---|---|---|---|---|
| 2026 | 5.20 | 5.20 | 5.20 | +0.00 | 110 |
| 2027 | 5.28 | 5.30 | 5.28 | -0.02 | 110 |
| 2028 | 5.30 | 5.30 | 5.35 | +0.00 | 85 |
| 2029 | 5.33 | 5.35 | 5.40 | -0.02 | 79 |

### expc_focus_copom

Último dado 2026-10-02 (no corte) · A: `A/expc_focus_copom.csv.gz`

Selic vigente na data da pesquisa: 13.75% (decidida em 2026-09-16). Mediana da pesquisa (janela de 30 dias), % a.a.

| Reunião | Data | Mediana (2026-10-02) | 4 sem. antes (2026-09-04) | Δ 4 sem. (p.p.) | Mín–máx |
|---|---|---|---|---|---|
| R7/2026 | 2026-11-04 | 13.50 | 13.75 | -0.25 | 13.50 a 14.00 |
| R8/2026 | 2026-12-09 | 13.50 | 13.75 | -0.25 | 13.00 a 14.00 |
| R1/2027 | 2027-01-27 | 13.50 | 13.75 | -0.25 | 12.50 a 14.00 |
| R2/2027 | 2027-03-17 | 13.25 | 13.50 | -0.25 | 12.00 a 14.00 |
| R3/2027 | 2027-04-28 | 13.00 | 13.25 | -0.25 | 11.50 a 14.00 |
| R4/2027 | 2027-06-16 | 12.75 | 13.00 | -0.25 | 11.00 a 14.00 |
| R5/2027 | 2027-08-04 | 12.50 | 12.75 | -0.25 | 10.25 a 14.00 |
| R6/2027 | 2027-09-22 | 12.50 | 12.50 | +0.00 | 9.75 a 14.00 |

### expc_qpc

Último dado 2026-09-23 (9 dias antes do corte) · A: `A/expc_qpc.csv.gz`

QPC da reunião 281 (publicado em 2026-09-23); o anterior é o da reunião 280.

Passo da Selic, em p.b.: a resposta mais frequente (fatia das respostas) e a média.

| Reunião | Fará | Deveria |
|---|---|---|
| R281 | -25 p.b. (97%); média -24 | -25 p.b. (68%); média -17 |
| R282 | +0 p.b. (53%); média -12 | +0 p.b. (61%); média -9 |
| R283 | +0 p.b. (66%); média -9 | +0 p.b. (69%); média -8 |

Medianas. "Última vez perguntado": o QPC anterior mais recente com a mesma pergunta e a mesma referência.

| Variável | Referência | Mediana | p25 a p75 | Última vez perguntado |
|---|---|---|---|---|
| IPCA no horizonte relevante, 4 trimestres (%) | 2028T1 | 4.00 | 3.77 a 4.20 | — |
| Hiato do produto (% do potencial) | 2026T2 | 0.50 | 0.30 a 1.00 | — |
| Hiato do produto (% do potencial) | 2026T4 | 0.20 | 0.00 a 0.50 | 0.21 (R279) |
| Hiato do produto (% do potencial) | 2027T4 | -0.20 | -0.41 a 0.07 | 0.00 (R279) |
| PIB, trimestre contra o anterior, dessaz. (%) | 2026T3 | 0.20 | 0.10 a 0.30 | 0.30 (R280) |
| PIB, trimestre contra o anterior, dessaz. (%) | 2026T4 | 0.20 | 0.10 a 0.30 | — |
| IPCA no mês (%) | 2026-09 | 0.56 | 0.50 a 0.60 | 0.51 (R280) |
| IPCA no mês (%) | 2026-10 | 0.34 | 0.30 a 0.39 | 0.34 (R280) |
| IPCA no mês (%) | 2026-11 | 0.32 | 0.28 a 0.37 | — |
| IPCA no mês (%) | 2026-12 | 0.55 | 0.50 a 0.60 | — |
| Média dos núcleos no mês (%) | 2026-09 | 0.29 | 0.27 a 0.33 | 0.30 (R280) |
| Média dos núcleos no mês (%) | 2026-10 | 0.35 | 0.31 a 0.39 | 0.35 (R280) |
| Média dos núcleos no mês (%) | 2026-11 | 0.26 | 0.23 a 0.32 | — |
| Média dos núcleos no mês (%) | 2026-12 | 0.48 | 0.42 a 0.52 | — |
| Serviços subjacentes no mês (%) | 2026-09 | 0.30 | 0.25 a 0.35 | 0.34 (R280) |
| Serviços subjacentes no mês (%) | 2026-10 | 0.40 | 0.36 a 0.46 | 0.39 (R280) |
| Serviços subjacentes no mês (%) | 2026-11 | 0.39 | 0.33 a 0.44 | — |
| Serviços subjacentes no mês (%) | 2026-12 | 0.54 | 0.45 a 0.57 | — |

Balanço de riscos e avaliação do cenário, fatia das respostas:

| Pergunta | Respostas |
|---|---|
| vies ipca 2026 | risco de alta 33%; risco de baixa 6%; riscos equilibrados 60% |
| vies ipca 2027 | risco de alta 60%; risco de baixa 5%; riscos equilibrados 35% |
| vies pib 2026 | risco de alta 4%; risco de baixa 34%; riscos equilibrados 63% |
| vies pib 2027 | risco de alta 1%; risco de baixa 73%; riscos equilibrados 26% |
| ambiente externo | mais favoravel 1%; menos favoravel 67%; sem mudancas relevantes 32% |
| situacao fiscal | melhorou 2%; piorou 17%; sem mudancas relevantes 81% |

Perguntadas só em algumas reuniões; vale a mais recente:

| Variável estrutural | Horizonte | Mediana | QPC | Na pergunta anterior |
|---|---|---|---|---|
| Juro real neutro (% a.a.) | 2a | 6.00 | R279 (2026-06-24) | 5.50 (R275) |
| Juro real neutro (% a.a.) | 5a | 5.50 | R279 (2026-06-24) | 5.00 (R275) |
| Juro real neutro (% a.a.) | curto prazo | 6.40 | R279 (2026-06-24) | 6.00 (R275) |
| Crescimento do PIB potencial (%) | 2a | 2.00 | R279 (2026-06-24) | 2.00 (R275) |
| Crescimento do PIB potencial (%) | 5a | 2.00 | R279 (2026-06-24) | 2.00 (R275) |
| Crescimento do PIB potencial (%) | curto prazo | 2.00 | R279 (2026-06-24) | 2.00 (R275) |
| Taxa de desemprego neutra (%) | 2a | 7.40 | R279 (2026-06-24) | 7.50 (R275) |
| Taxa de desemprego neutra (%) | 5a | 7.45 | R279 (2026-06-24) | 7.50 (R275) |
| Taxa de desemprego neutra (%) | curto prazo | 7.30 | R279 (2026-06-24) | 7.50 (R275) |

## ii. Endógeno de política monetária (leitura enxuta)

### inflc_meta

Último dado 2026-01-01 (274 dias antes do corte) · A: `A/inflc_meta.csv.gz`

| Ano | Meta (%) |
|---|---|
| 2024 | 3.00 |
| 2025 | 3.00 |
| 2026 | 3.00 |

### pm_copom_projecoes

Último dado 2026-09-24 (8 dias antes do corte) · A: `A/pm_copom_projecoes.csv.gz`

Reunião 281 (de 2026-09-24), Relatório de Política Monetária, cenário de referência (juros da Focus). Valor = acumulado em quatro trimestres. Meta vigente: 3.00%.

| Período | IPCA (%) | Livres (%) | Administrados (%) |  |
|---|---|---|---|---|
| 3T26 | 4.4 | 4.6 | 3.9 |  |
| 4T26 | 5.2 | 5.2 | 5.3 |  |
| 1T27 | 4.9 | 5.0 | 4.5 |  |
| 2T27 | 4.5 | 4.6 | 4.0 |  |
| 3T27 | 4.5 | 4.5 | 4.3 |  |
| 4T27 | 3.9 | 4.1 | 3.5 |  |
| 1T28 | 3.2 | 3.2 | 3.2 | horizonte relevante |
| 2T28 | 3.1 | 3.0 | 3.4 |  |
| 3T28 | 3.1 | 3.0 | 3.5 |  |
| 4T28 | 3.1 | 3.0 | 3.4 |  |
| 1T29 | 3.1 | 3.1 | 3.2 |  |

O horizonte relevante nas últimas reuniões (cenário de referência):

| Reunião | Documento | Data | Horizonte relevante | IPCA projetado (%) | Passo decidido (p.b.) |
|---|---|---|---|---|---|
| 281 | relatorio | 2026-09-24 | 1T28 | 3.2 | -25 |
| 280 | comunicado | 2026-08-05 | 1T28 | 3.2 | -25 |
| 279 | relatorio | 2026-06-25 | 4T27 | 3.7 | -25 |
| 278 | comunicado | 2026-04-29 | 4T27 | 3.5 | -25 |
| 277 | relatorio | 2026-03-26 | 3T27 | 3.3 | -25 |
| 276 | comunicado | 2026-01-28 | 3T27 | 3.2 | +0 |
| 275 | relatorio | 2025-12-18 | 2T27 | 3.2 | +0 |
| 274 | comunicado | 2025-11-05 | 2T27 | 3.3 | +0 |

### pm_copom_reuniao

Último dado 2026-09-16 (16 dias antes do corte) · A: `A/pm_copom_reuniao.csv.gz`

| Reunião | Decisão | Selic decidida (% a.a.) | Passo (p.b.) |
|---|---|---|---|
| 281 | 2026-09-16 | 13.75 | -25 |
| 280 | 2026-08-05 | 14.00 | -25 |
| 279 | 2026-06-17 | 14.25 | -25 |
| 278 | 2026-04-29 | 14.50 | -25 |
| 277 | 2026-03-18 | 14.75 | -25 |
| 276 | 2026-01-28 | 15.00 | +0 |
| 275 | 2025-12-10 | 15.00 | +0 |
| 274 | 2025-11-05 | 15.00 | +0 |

Ciclo em curso: corte desde 2026-03-18, 5 reuniões, -125 p.b. acumulados (Selic de 15.00% para 13.75%).

### pm_copom_calendario

Último dado 2027-12-08 (data no futuro) · A: `A/pm_copom_calendario.csv.gz`

O calendário oficial vai até 2027-12-08.

| Reunião | Decisão | Dias a partir do corte |
|---|---|---|
| última | 2026-09-16 | -16 |
| próxima 1 | 2026-11-04 | 33 |
| próxima 2 | 2026-12-09 | 68 |
| próxima 3 | 2027-01-27 | 117 |
| próxima 4 | 2027-03-17 | 166 |

### br_interest_rate

Último dado 2026-10-02 (no corte) · A: `A/br_interest_rate.csv.gz`

Inflação implícita = (1 + DI × pré)/(1 + NTN-B) − 1, no mesmo vértice (razão, não diferença). É preço: carrega prêmio de risco de inflação e efeitos de liquidez. Meta de referência: 3.00% (a do ano 2028 ou a última publicada). Histórico desde 2006. Δ em p.p.

| Vértice | Data | DI × pré (%) | NTN-B (%) | Implícita (%) | Implícita − meta (p.p.) | Δ 1m | Δ 3m | Δ 12m | Pctl hist. | Pctl 10a |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 ano | 2026-10-02 | 13.50 | 6.14 | 6.94 | +3.94 | +0.65 | +1.88 | +2.78 | 91 | 92 |
| 2 anos | 2026-10-02 | 13.69 | 7.36 | 5.89 | +2.89 | +0.30 | +0.87 | +1.43 | 78 | 87 |
| 5 anos | 2026-10-02 | 14.04 | 7.56 | 6.02 | +3.02 | +0.21 | +0.52 | +0.88 | 86 | 87 |
| 10 anos | 2026-10-02 | 14.15 | 7.51 | 6.18 | +3.18 | +0.02 | +0.40 | +0.62 | 86 | 86 |

## iii. Endógeno de inflação (leitura enxuta)

### inflc_agregados

Último dado 2026-09-01 (31 dias antes do corte) · A: `A/inflc_agregados.csv.gz`

| Série | Mês | Último mês | Acum. 3m | Acum. 12m | Acum. 12m, 3 meses antes |
|---|---|---|---|---|---|
| IPCA | 2026-09 | 0.82 | 0.57 | 4.58 | 4.64 |
| IPCA-15 | 2026-09 | 0.70 | 0.36 | 4.47 | 4.80 |
| Livres | 2026-09 | 0.55 | 0.55 | 4.68 | 4.31 |
| Administrados | 2026-09 | 1.59 | 0.59 | 4.14 | 5.52 |
| Alimentação | 2026-09 | 0.96 | -0.80 | 4.19 | 3.01 |
| Serviços | 2026-09 | 0.61 | 1.18 | 5.97 | 5.90 |
| Industriais | 2026-09 | 0.17 | 0.50 | 3.07 | 2.76 |
| Núcleo EX0 | 2026-09 | 0.44 | 0.92 | 4.85 | 4.67 |
| Núcleo EX3 | 2026-09 | 0.26 | 0.78 | 4.65 | 4.64 |
| Núcleo médias aparadas com suavização | 2026-09 | 0.31 | 0.89 | 4.43 | 4.33 |
| Núcleo P55 | 2026-09 | 0.42 | 0.97 | 4.68 | 4.54 |
| Núcleo dupla ponderação | 2026-09 | 0.37 | 0.68 | 4.06 | 4.01 |
| Núcleo EXFE | 2026-09 | 0.35 | 0.87 | 4.71 | 4.70 |

| Série | Unidade | Data | Último | Δ 1m | Δ 3m | Δ 12m |
|---|---|---|---|---|---|---|
| Índice de difusão | % dos subitens | 2026-09-01 | 54.9 | +0.5 | +1.3 | +2.7 |

## iv. Endógeno de câmbio (leitura enxuta)

### cmb_ptax

Último dado 2026-10-02 (no corte) · A: `A/cmb_ptax.csv.gz`

| Série | Unidade | Data | Último | Δ% 1m | Δ% 3m | Δ% 12m |
|---|---|---|---|---|---|---|
| PTAX venda | R$/US$ | 2026-10-02 | 5.2238 | +1.9 | +0.6 | -2.3 |

## v. Endógeno de fiscal (leitura enxuta)

### cmb_risco_pais

Último dado 2026-10-02 (no corte) · A: `A/cmb_risco_pais.csv.gz`

| Série | Unidade | Data | Último | Δ 1m | Δ 3m | Δ 12m |
|---|---|---|---|---|---|---|
| CDS 5 anos Brasil | p.b. | 2026-10-02 | 131 | +10 | +6 | -5 |

## Leituras combinadas

### Desancoragem: distância da meta por horizonte, e onde ela está no histórico

Mediana da Focus menos a meta do mesmo horizonte, em p.p. A 12 meses, a meta do ano e a do seguinte pesadas pelos meses da janela; por ano-calendário, a meta daquele ano (a última publicada para anos ainda não fixados). Ano corrente e t+1 carregam choques já visíveis; a ancoragem se julga em t+2 e t+3. Pctl = posição da distância de hoje entre todas as pesquisas da série (hist.) e dos últimos 10 anos. Ano-calendário desde 2000; 12 meses desde 2001.

| Horizonte | Data | Expectativa − meta (p.p.) | Δ 3m | Δ 12m | Pctl hist. | Pctl 10a | Maior da série | Desde |
|---|---|---|---|---|---|---|---|---|
| 12 meses à frente (a variável da tese) | 2026-10-02 | +1.59 | +0.47 | +0.37 | 81 | 79 | +8.35 (2002-12-19) | 2001-12-12 |
| ano corrente | 2026-10-02 | +2.01 | -0.31 | +0.21 | 74 | 71 | +9.06 (2002-12-31) | 2000-01-03 |
| ano seguinte (t+1) | 2026-10-02 | +1.30 | +0.13 | +0.02 | 84 | 86 | +7.00 (2002-12-13) | 2000-01-13 |
| t+2 | 2026-10-02 | +0.80 | +0.10 | -0.10 | 85 | 89 | +2.50 (2002-12-31) | 2000-08-07 |
| t+3 | 2026-10-02 | +0.51 | +0.01 | -0.19 | 86 | 88 | +1.50 (2002-12-09) | 2000-08-07 |

### A pesquisa contra ela mesma: Selic e IPCA esperados

Focus de 2026-10-02, medianas por ano. Juro real = (1 + Selic do fim do ano)/(1 + IPCA do ano) − 1: uma aproximação do juro real que a pesquisa espera, não uma taxa ex-ante de mercado. Se a pesquisa espera inflação acima da meta e, ao mesmo tempo, juro real caindo, é sinal de dúvida sobre a reação do Copom (mapa 2.8).

| Ano | Selic no fim do ano (%) | IPCA do ano (%) | Meta (%) | IPCA − meta (p.p.) | Juro real implícito na pesquisa (%) |
|---|---|---|---|---|---|
| 2026 | 13.50 | 5.01 | 3.00 | +2.01 | 8.08 |
| 2027 | 12.00 | 4.30 | 3.00 | +1.30 | 7.38 |
| 2028 | 10.50 | 3.80 | 3.00 | +0.80 | 6.45 |
| 2029 | 10.00 | 3.51 | 3.00 | +0.51 | 6.27 |
| 2030 | 10.00 | 3.50 | 3.00 | +0.50 | 6.28 |

Juro real neutro no QPC da reunião 279, mediana: 2a 6.00%; 5a 5.50%; curto prazo 6.40%.

### O Copom, o QPC e a Focus no horizonte relevante

Horizonte relevante do Copom: 1T28. A projeção do Copom é condicional aos caminhos que ele usa (Selic da Focus, câmbio, petróleo): não é a previsão dele.

| Fonte | IPCA 4 trimestres no horizonte relevante (%) |
|---|---|
| Copom, reunião 281 (RPM, 2026-09-24) | 3.2 |
| QPC da reunião 281, mediana (referência 2028T1) | 4.00 |
| Focus, 12 meses à frente (2026-10-02) | 4.59 (outro horizonte: os próximos 12 meses) |
