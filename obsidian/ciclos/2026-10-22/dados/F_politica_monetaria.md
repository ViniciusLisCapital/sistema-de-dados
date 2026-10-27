# F(A) — politica_monetaria — ciclo 2026-10-22

Gerado em 2026-10-22 09:14. Dados do banco até 2026-10-22, fixos durante o ciclo. Ciclo anterior: 2026-10-15.

Os dados brutos (A) estão em `A/`, um arquivo por tabela; as funções G leem de lá e o código delas fica em `G/`. Nada aqui é opinião: é a mesma conta em todo ciclo.

Como ler:
- **Δ% 1m/3m/12m**: variação contra o último valor de 1, 3 e 12 meses antes da última data da série; numa série trimestral, **1t/4t**: contra 1 e 4 trimestres antes.
- **Δ**: diferença na unidade da série (p.p. quando a série é %, p.b. quando é p.b.).
- **Pctl**: posição do último valor no histórico, de 0 (o menor já visto) a 100 (o maior). "10a" = últimos 10 anos.
- **Soma 3m/12m**: soma dos últimos 3 e 12 meses completos; o mês em curso aparece à parte e não entra nas somas.
- **Acum.**: variação composta.
- **Desde o ciclo ant.**: contra o valor em 2026-10-15.

## i. Endógeno (leitura completa)

### pm_copom_calendario

Último dado 2027-12-08 (data no futuro) · A: `A/pm_copom_calendario.csv.gz`

O calendário oficial vai até 2027-12-08.

| Reunião | Decisão | Dias a partir do corte |
|---|---|---|
| última | 2026-09-16 | -36 |
| próxima 1 | 2026-11-04 | 13 |
| próxima 2 | 2026-12-09 | 48 |
| próxima 3 | 2027-01-27 | 97 |
| próxima 4 | 2027-03-17 | 146 |
| próxima 5 | 2027-04-28 | 188 |
| próxima 6 | 2027-06-16 | 237 |
| próxima 7 | 2027-08-04 | 286 |
| próxima 8 | 2027-09-22 | 335 |
| próxima 9 | 2027-10-27 | 370 |
| próxima 10 | 2027-12-08 | 412 |

### pm_copom_reuniao

Último dado 2026-09-16 (36 dias antes do corte) · A: `A/pm_copom_reuniao.csv.gz`

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

### pm_copom_projecoes

Último dado 2026-09-24 (28 dias antes do corte) · A: `A/pm_copom_projecoes.csv.gz`

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

### pm_hiato_produto

Último dado 2026-09-01 (51 dias antes do corte) · A: `A/pm_hiato_produto.csv.gz`

Edição de 2026-09-01 do RPM. % do produto potencial; positivo = economia acima do potencial. A dispersão é a que o BC publica para o conjunto de estimativas.

| Trimestre | Central | p25 a p75 | Mín–máx |
|---|---|---|---|
| 3T26 | 0.41 | 0.00 a 0.89 | -0.33 a 1.81 |
| 2T26 | 0.51 | 0.35 a 1.43 | -0.01 a 2.04 |
| 1T26 | 0.60 | 0.30 a 1.38 | 0.00 a 1.50 |
| 4T25 | 0.74 | 0.22 a 1.02 | -0.26 a 1.22 |
| 3T25 | 0.95 | 0.40 a 1.40 | -0.12 a 1.65 |
| 2T25 | 1.17 | 0.58 a 1.85 | 0.26 a 2.24 |
| 1T25 | 1.40 | 0.75 a 1.60 | 0.34 a 2.03 |
| 4T24 | 1.47 | 0.29 a 1.44 | 0.03 a 1.71 |

Pctl hist. da central no último trimestre: 57 (92 trimestres, desde 4T03).

### pm_hiato_produto_vintages

Último dado 2026-09-01 (51 dias antes do corte) · A: `A/pm_hiato_produto_vintages.csv.gz`

21 edições na tabela, desde 2021-09-01. Central, % do potencial.

| Trimestre | Edição 2025-12-01 | Edição 2026-03-01 | Edição 2026-06-01 | Edição 2026-09-01 | Revisão na última (p.p.) |
|---|---|---|---|---|---|
| 3T26 | — | — | — | 0.41 | — |
| 2T26 | — | — | 0.36 | 0.51 | +0.15 |
| 1T26 | — | 0.13 | 0.49 | 0.60 | +0.11 |
| 4T25 | 0.17 | 0.39 | 0.60 | 0.74 | +0.14 |
| 3T25 | 0.54 | 0.70 | 0.82 | 0.95 | +0.13 |
| 2T25 | 0.89 | 1.01 | 1.07 | 1.17 | +0.10 |

### br_interest_rate

Último dado 2026-10-20 (2 dias antes do corte) · A: `A/br_interest_rate.csv.gz`

| Série | Unidade | Data | Último | Δ 1m | Δ 3m | Δ 12m | Δ desde o ciclo ant. | Pctl 10a | Pctl hist. | Mín–máx 10a |
|---|---|---|---|---|---|---|---|---|---|---|
| Selic, meta | % a.a. | 2026-10-13 | 13.75 | -0.25 | -0.50 | -1.25 | sem dado novo | 84 | 56 | 2.00 a 15.00 |
| DI × pré 3 meses | % a.a. | 2026-10-20 | 13.46 | -0.11 | -0.48 | -1.43 | -0.04 | 72 | 74 | 1.87 a 14.94 |
| DI × pré 6 meses | % a.a. | 2026-10-20 | 13.28 | -0.26 | -0.66 | -1.51 | -0.08 | 71 | 73 | 1.87 a 14.96 |
| DI × pré 1 ano | % a.a. | 2026-10-20 | 12.91 | -0.69 | -1.15 | -1.30 | -0.13 | 71 | 71 | 2.19 a 15.42 |
| DI × pré 2 anos | % a.a. | 2026-10-20 | 12.59 | -1.20 | -1.69 | -0.80 | -0.07 | 75 | 70 | 3.23 a 15.95 |
| DI × pré 5 anos | % a.a. | 2026-10-20 | 12.66 | -1.42 | -1.92 | -0.83 | -0.06 | 76 | 70 | 5.42 a 15.60 |
| DI × pré 10 anos | % a.a. | 2026-10-20 | 12.75 | -1.41 | -1.86 | -0.92 | -0.04 | 75 | 70 | 6.66 a 15.04 |
| NTN-B 1 ano (juro real) | % a.a. | 2026-10-20 | 5.92 | -0.29 | -2.30 | -3.91 | +0.12 | 57 | 53 | -2.33 a 10.32 |
| NTN-B 2 anos (juro real) | % a.a. | 2026-10-20 | 6.83 | -0.51 | -1.72 | -1.89 | +0.02 | 79 | 74 | -0.21 a 8.92 |
| NTN-B 5 anos (juro real) | % a.a. | 2026-10-20 | 6.78 | -0.80 | -1.51 | -1.28 | -0.04 | 80 | 72 | 1.58 a 8.77 |
| NTN-B 10 anos (juro real) | % a.a. | 2026-10-20 | 6.88 | -0.72 | -1.12 | -0.84 | +0.01 | 81 | 74 | 2.61 a 8.20 |

### br_di_grade

Último dado 2026-10-20 (2 dias antes do corte) · A: `A/br_di_grade.csv.gz`

Pregão de 2026-10-20. DI × pré, base 252, nos prazos redondos.

| Prazo | Taxa (% a.a.) | Δ 1m (p.b.) | Δ 3m (p.b.) | Δ 12m (p.b.) | Δ ciclo ant. (p.b.) |
|---|---|---|---|---|---|
| 1 mês | 13.56 | -10 | -50 | -134 | -3 |
| 3 meses | 13.45 | -11 | -49 | -144 | -4 |
| 6 meses | 13.27 | -27 | -67 | -152 | -8 |
| 1 ano | 12.90 | -70 | -116 | -130 | -12 |
| 2 anos | 12.58 | -121 | -170 | -80 | -8 |
| 3 anos | 12.60 | -136 | -190 | -65 | -6 |
| 5 anos | 12.67 | -141 | -191 | -83 | -6 |
| 10 anos | 12.75 | -141 | -186 | -92 | -4 |

Selic precificada na curva em cada reunião (meta vigente 13.75%). É preço, com prêmio de prazo, não previsão. Reuniões só até onde vai o calendário oficial (2027-12-08).

| Reunião | Selic na curva (% a.a.) | Passo implícito (p.b.) | 1 mês antes (2026-09-18) | Δ 1 mês (p.b.) |
|---|---|---|---|---|
| 2026-11-04 | 13.59 | -16 | 13.61 | -2 |
| 2026-12-09 | 13.45 | -14 | 13.58 | -13 |
| 2027-01-27 | 13.27 | -18 | 13.63 | -36 |
| 2027-03-17 | 13.07 | -19 | 13.68 | -60 |
| 2027-04-28 | 12.87 | -20 | 13.73 | -85 |
| 2027-06-16 | 12.66 | -21 | 13.76 | -110 |
| 2027-08-04 | 12.48 | -18 | 13.79 | -131 |
| 2027-09-22 | 12.37 | -11 | 13.84 | -147 |
| 2027-10-27 | 12.33 | -5 | 13.92 | -159 |
| 2027-12-08 | 12.35 | +2 | 14.03 | -169 |

### inflc_meta

Último dado 2026-01-01 (294 dias antes do corte) · A: `A/inflc_meta.csv.gz`

| Ano | Meta (%) |
|---|---|
| 2024 | 3.00 |
| 2025 | 3.00 |
| 2026 | 3.00 |

## ii. Endógeno de câmbio (leitura enxuta)

### cmb_ptax

Último dado 2026-10-20 (2 dias antes do corte) · A: `A/cmb_ptax.csv.gz`

| Série | Unidade | Data | Último | Δ% 1m | Δ% 3m | Δ% 12m | Δ% desde o ciclo ant. |
|---|---|---|---|---|---|---|---|
| PTAX venda | R$/US$ | 2026-10-20 | 5.0140 | -2.8 | -1.5 | -6.8 | -0.8 |

### cmb_fx_latam

Último dado 2026-10-13 (9 dias antes do corte) · A: `A/cmb_fx_latam.csv.gz`

| Série | Unidade | Data | Último | Δ% 1m | Δ% 3m | Δ% 12m | Δ% desde o ciclo ant. |
|---|---|---|---|---|---|---|---|
| Peso mexicano | MXN/US$ | 2026-10-13 | 18.3345 | +8.0 | +4.8 | -0.9 | sem dado novo |
| Peso chileno | CLP/US$ | 2026-10-13 | 978.61 | +4.4 | +5.8 | +2.5 | sem dado novo |
| Peso colombiano | COP/US$ | 2026-10-09 | 3218.75 | +3.3 | -3.6 | -17.0 | sem dado novo |
| Sol peruano | PEN/US$ | 2026-10-09 | 3.4535 | +2.8 | +1.5 | +0.5 | sem dado novo |

### cmb_reer

Último dado 2026-08-01 (82 dias antes do corte) · A: `A/cmb_reer.csv.gz`

| Série | Unidade | Data | Último | Δ% 1m | Δ% 3m | Δ% 12m | Δ% desde o ciclo ant. |
|---|---|---|---|---|---|---|---|
| BR, real efetivo | índice 2020=100 | 2026-08-01 | 116.46 | -2.0 | -3.4 | +5.5 | sem dado novo |
| BR, nominal efetivo | índice 2020=100 | 2026-08-01 | 113.18 | -1.4 | -2.7 | +4.9 | sem dado novo |
| MX, real efetivo | índice 2020=100 | 2026-08-01 | 141.98 | +1.6 | +1.1 | +9.2 | sem dado novo |
| CL, real efetivo | índice 2020=100 | 2026-08-01 | 102.21 | +0.9 | -2.0 | +3.7 | sem dado novo |
| CO, real efetivo | índice 2020=100 | 2026-08-01 | 147.03 | +3.7 | +19.4 | +30.3 | sem dado novo |

### cmb_reservas_bc

Último dado 2026-10-20 (2 dias antes do corte) · A: `A/cmb_reservas_bc.csv.gz`

| Série | Unidade | Data | Último | Δ 1m | Δ 3m | Δ 12m | Δ desde o ciclo ant. |
|---|---|---|---|---|---|---|---|
| Reservas internacionais | US$ bi | 2026-10-20 | 364.6 | -3.1 | -4.8 | +4.2 | +0.3 |
| Swap cambial do BC, posição (− = vendido) | US$ bi | 2026-08-01 | -91.6 | +1.3 | +3.2 | +9.8 | sem dado novo |

| Série | Unidade | Último mês | Soma 3m | Soma 12m | Soma 12m, um ano antes | Mês em curso | Soma desde o ciclo ant. |
|---|---|---|---|---|---|---|---|
| Intervenção à vista (+ compra, − venda) | US$ bi | -2.00 (2026-09) | -3.00 | -8.00 | -22.57 | 0.00 (até 20/10) | 0.00 |
| Leilões de linha (+ compra, − venda) | US$ bi | -2.00 (2026-09) | 0.05 | 7.25 | -11.25 | 0.00 (até 20/10) | 0.00 |

### cmb_cambio_contratado

Último dado 2026-10-09 (13 dias antes do corte) · A: `A/cmb_cambio_contratado.csv.gz`

| Série | Unidade | Último mês | Soma 3m | Soma 12m | Soma 12m, um ano antes | Mês em curso | Soma desde o ciclo ant. |
|---|---|---|---|---|---|---|---|
| Saldo total (comercial + financeiro) | US$ bi | -5.09 (2026-09) | -7.06 | -3.90 | -42.67 | 3.21 (até 09/10) | 0.00 |
| Comercial, saldo | US$ bi | 2.28 (2026-09) | 11.91 | 58.41 | 46.33 | -0.87 (até 09/10) | 0.00 |
| Financeiro, saldo | US$ bi | -7.37 (2026-09) | -18.96 | -62.31 | -89.00 | 4.09 (até 09/10) | 0.00 |

### cmb_balanco_pagmt

Último dado 2026-08-01 (82 dias antes do corte) · A: `A/cmb_balanco_pagmt.csv.gz`

| Série | Unidade | Último mês | Soma 3m | Soma 12m | Soma 12m, um ano antes | 12m % PIB |
|---|---|---|---|---|---|---|
| Transações correntes | US$ bi | -5.05 (2026-08) | -18.06 | -63.04 | -76.92 | — |
| Investimento direto no país (passivos) | US$ bi | 7.40 (2026-08) | 23.51 | 86.56 | 79.28 | — |
| Carteira, passivos | US$ bi | -5.32 (2026-08) | -4.22 | 24.42 | 5.76 | — |

### cmb_cot_fx

Último dado 2026-10-06 (16 dias antes do corte) · A: `A/cmb_cot_fx.csv.gz`

| Série | Unidade | Data | Último | Δ 1m | Δ 3m | Δ 12m | Δ desde o ciclo ant. |
|---|---|---|---|---|---|---|---|
| BRL: fundos alavancados, líquido | contratos | 2026-10-06 | 27396 | +11350 | +19670 | +5047 | sem dado novo |
| BRL: asset managers, líquido | contratos | 2026-10-06 | 56610 | +7876 | +10534 | -667 | sem dado novo |
| BRL: posições em aberto | contratos | 2026-10-06 | 134541 | +7268 | +19551 | -5869 | sem dado novo |

### cmb_termos_troca

Último dado 2026-07-01 (113 dias antes do corte) · A: `A/cmb_termos_troca.csv.gz`

| Série | Unidade | Data | Último | Δ% 1m | Δ% 3m | Δ% 12m | Δ% desde o ciclo ant. |
|---|---|---|---|---|---|---|---|
| Termos de troca (Funcex) | índice | 2026-07-01 | 111.35 | -1.8 | -2.7 | +1.5 | sem dado novo |

### cmb_comex_fator_agregado

Último dado 2026-08-01 (82 dias antes do corte) · A: `A/cmb_comex_fator_agregado.csv.gz`

| Série | Unidade | Último mês | Soma 3m | Soma 12m | Soma 12m, um ano antes |
|---|---|---|---|---|---|
| Básicos, exportação | US$ bi | 19.75 (2026-08) | 61.85 | 222.48 | 192.15 |
| Manufaturados, exportação | US$ bi | 9.18 (2026-08) | 27.32 | 101.29 | 99.83 |

### cmb_comex_pais

Último dado 2026-09-01 (51 dias antes do corte) · A: `A/cmb_comex_pais.csv.gz`

| Série | Unidade | Último mês | Soma 3m | Soma 12m | Soma 12m, um ano antes |
|---|---|---|---|---|---|
| Mundo, exportação | US$ bi | 34.42 (2026-09) | 100.73 | 375.04 | 339.93 |
| Mundo, importação | US$ bi | 26.68 (2026-09) | 79.66 | 290.87 | 278.16 |
| China, exportação | US$ bi | 7.89 (2026-09) | 26.62 | 109.03 | 93.53 |

### cmb_comex_produto

Último dado 2026-08-01 (82 dias antes do corte) · A: `A/cmb_comex_produto.csv.gz`

| Série | Unidade | Último mês | Soma 3m | Soma 12m | Soma 12m, um ano antes |
|---|---|---|---|---|---|
| Petróleo, exportação | US$ bi | 4.83 (2026-08) | 15.29 | 51.62 | 43.22 |
| Soja, exportação | US$ bi | 4.41 (2026-08) | 16.55 | 48.73 | 40.81 |
| Minério de ferro, exportação | US$ bi | 2.35 (2026-08) | 7.60 | 29.13 | 27.24 |

### diferenciais_juros

Último dado 2026-10-01 (21 dias antes do corte) · A: `A/diferenciais_juros.csv.gz`

| Série | Unidade | Data | Último | Δ 1m | Δ 3m | Δ 12m | Δ desde o ciclo ant. |
|---|---|---|---|---|---|---|---|
| Selic | % a.a. | 2026-10-01 | 13.75 | +0.00 | -0.50 | -1.25 | sem dado novo |
| Fed Funds | % a.a. | 2026-09-01 | 3.75 | +0.12 | +0.12 | -0.47 | sem dado novo |
| Diferencial nominal (Selic − Fed Funds) | p.p. | 2026-09-01 | 10.00 | -0.37 | -0.62 | -0.78 | sem dado novo |
| Diferencial real ex-post | p.p. | 2026-09-01 | 9.14 | -0.37 | -0.31 | +0.50 | sem dado novo |

## iii. TWA — expectativas (leitura enxuta)

### expc_focus_copom

Último dado 2026-10-09 (13 dias antes do corte) · A: `A/expc_focus_copom.csv.gz`

Selic vigente na data da pesquisa: 13.75% (decidida em 2026-09-16). Mediana da pesquisa (janela de 30 dias), % a.a.

| Reunião | Data | Mediana (2026-10-09) | 4 sem. antes (2026-09-11) | Δ 4 sem. (p.p.) | Mín–máx | Ciclo ant. (2026-10-09) |
|---|---|---|---|---|---|---|
| R7/2026 | 2026-11-04 | 13.50 | 13.75 | -0.25 | 13.50 a 14.00 | 13.50 |
| R8/2026 | 2026-12-09 | 13.25 | 13.75 | -0.50 | 13.00 a 14.00 | 13.25 |
| R1/2027 | 2027-01-27 | 13.25 | 13.50 | -0.25 | 12.50 a 14.00 | 13.25 |
| R2/2027 | 2027-03-17 | 13.00 | 13.50 | -0.50 | 12.00 a 14.00 | 13.00 |
| R3/2027 | 2027-04-28 | 12.75 | 13.25 | -0.50 | 11.25 a 14.00 | 12.75 |
| R4/2027 | 2027-06-16 | 12.62 | 13.00 | -0.38 | 10.50 a 14.00 | 12.62 |
| R5/2027 | 2027-08-04 | 12.50 | 12.62 | -0.12 | 9.75 a 14.00 | 12.50 |
| R6/2027 | 2027-09-22 | 12.25 | 12.50 | -0.25 | 9.75 a 14.00 | 12.25 |

### expc_focus_periodo (Selic)

Último dado 2026-10-09 (13 dias antes do corte) · A: `A/expc_focus_periodo__selic.csv.gz`

Unidade: %. Mediana da pesquisa (janela de 30 dias).

| Ano | Mediana (2026-10-09) | 4 sem. antes (2026-09-11) | 13 sem. antes (2026-07-10) | Δ 4 sem. | Ciclo ant. (2026-10-09) | Respondentes |
|---|---|---|---|---|---|---|
| 2026 | 13.25 | 13.75 | 14.00 | -0.50 | 13.25 | 139 |
| 2027 | 12.00 | 12.00 | 12.00 | +0.00 | 12.00 | 138 |
| 2028 | 10.50 | 10.50 | 10.50 | +0.00 | 10.50 | 117 |
| 2029 | 10.00 | 10.00 | 10.00 | +0.00 | 10.00 | 110 |

### expc_qpc

Último dado 2026-09-23 (29 dias antes do corte) · A: `A/expc_qpc.csv.gz`

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

### expc_focus

Último dado 2026-10-09 (13 dias antes do corte) · A: `A/expc_focus.csv.gz`

| Série | Unidade | Data | Último | Δ 1m | Δ 3m | Δ 12m | Δ desde o ciclo ant. |
|---|---|---|---|---|---|---|---|
| IPCA 12 meses à frente (suavizada) | % | 2026-10-09 | 4.48 | -0.15 | +0.38 | +0.32 | sem dado novo |
| IPCA 24 meses à frente | % | 2026-10-09 | 3.91 | -0.03 | -0.04 | -0.13 | sem dado novo |
| IPCA serviços 12 meses à frente (suavizada) | % | 2026-10-09 | 5.14 | +0.03 | -0.10 | -0.24 | sem dado novo |
| IPCA livres 12 meses à frente (suavizada) | % | 2026-10-09 | 4.69 | +0.02 | +0.15 | +0.10 | sem dado novo |
| IPCA administrados 12 meses à frente (suavizada) | % | 2026-10-09 | 3.90 | -0.78 | +0.38 | +1.10 | sem dado novo |

### expc_focus_periodo (IPCA)

Último dado 2026-10-09 (13 dias antes do corte) · A: `A/expc_focus_periodo__ipca.csv.gz`

Unidade: %. Mediana da pesquisa (janela de 30 dias).

| Ano | Mediana (2026-10-09) | 4 sem. antes (2026-09-11) | 13 sem. antes (2026-07-10) | Δ 4 sem. | Ciclo ant. (2026-10-09) | Respondentes |
|---|---|---|---|---|---|---|
| 2026 | 5.22 | 4.90 | 5.16 | +0.32 | 5.22 | 144 |
| 2027 | 4.30 | 4.30 | 4.20 | +0.00 | 4.30 | 144 |
| 2028 | 3.79 | 3.80 | 3.70 | -0.01 | 3.79 | 121 |
| 2029 | 3.50 | 3.50 | 3.50 | -0.00 | 3.50 | 113 |

### expc_focus_periodo (câmbio)

Último dado 2026-10-09 (13 dias antes do corte) · A: `A/expc_focus_periodo__cambio.csv.gz`

Unidade: R$/US$. Mediana da pesquisa (janela de 30 dias).

| Ano | Mediana (2026-10-09) | 4 sem. antes (2026-09-11) | 13 sem. antes (2026-07-10) | Δ 4 sem. | Ciclo ant. (2026-10-09) | Respondentes |
|---|---|---|---|---|---|---|
| 2026 | 5.15 | 5.20 | 5.20 | -0.05 | 5.15 | 111 |
| 2027 | 5.26 | 5.28 | 5.28 | -0.02 | 5.26 | 111 |
| 2028 | 5.30 | 5.30 | 5.33 | +0.00 | 5.30 | 85 |
| 2029 | 5.30 | 5.36 | 5.40 | -0.06 | 5.30 | 79 |

## iv. TWA — inflação (leitura enxuta)

### inflc_agregados

Último dado 2026-09-01 (51 dias antes do corte) · A: `A/inflc_agregados.csv.gz`

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

| Série | Unidade | Data | Último | Δ 1m | Δ 3m | Δ 12m | Δ desde o ciclo ant. |
|---|---|---|---|---|---|---|---|
| Índice de difusão | % dos subitens | 2026-09-01 | 54.9 | +0.5 | +1.3 | +2.7 | sem dado novo |

### inflc_decomposicao

Último dado 2026-09-01 (51 dias antes do corte) · A: `A/inflc_decomposicao.csv.gz`

IPCA. Recortes refeitos dos subitens com a classificação do BC (`inflc_dim`); variação ponderada pelos pesos do mês. Sem ajuste sazonal.

| Recorte do BC | Mês | Último mês (%) | Acum. 3m | Acum. 12m | Acum. 12m, 3 meses antes | Contribuição no mês (p.p.) |
|---|---|---|---|---|---|---|
| Alimentação | 2026-09 | 0.96 | -0.79 | 4.21 | 3.03 | 0.15 |
| Bens industriais | 2026-09 | 0.17 | 0.51 | 3.06 | 2.74 | 0.04 |
| Serviços | 2026-09 | 0.61 | 1.18 | 5.97 | 5.90 | 0.22 |
| Monitorados | 2026-09 | 1.59 | 0.58 | 4.13 | 5.52 | 0.41 |
| Serviços subjacentes | 2026-09 | 0.36 | 1.17 | 5.32 | 5.00 | 0.08 |
| Industriais subjacentes | 2026-09 | 0.13 | 0.24 | 3.70 | 4.14 | 0.02 |

Maiores contribuições para cima em 2026-09:

| Subitem | Var. no mês (%) | Peso (%) | Contribuição (p.p.) |
|---|---|---|---|
| Energia elétrica residencial | 7.98 | 3.98 | 0.318 |
| Tomate | 37.76 | 0.22 | 0.083 |
| Passagem aérea | 9.66 | 0.71 | 0.069 |
| Gasolina | 1.21 | 5.13 | 0.062 |
| Batata-inglesa | 24.07 | 0.18 | 0.044 |

Maiores contribuições para baixo:

| Subitem | Var. no mês (%) | Peso (%) | Contribuição (p.p.) |
|---|---|---|---|
| Cinema, teatro e concertos | -3.20 | 0.50 | -0.016 |
| Perfume | -1.19 | 1.15 | -0.014 |
| Automóvel novo | -0.35 | 2.95 | -0.010 |
| Frango em pedaços | -1.41 | 0.61 | -0.009 |
| Manga | -9.62 | 0.09 | -0.008 |

### inflc_decomposicao_item

Último dado 2026-09-01 (51 dias antes do corte) · A: `A/inflc_decomposicao_item.csv.gz`

IPCA de 2026-09: os oito itens de maior contribuição, em valor absoluto.

| Item | Var. no mês (%) | Acum. 12m (%) | Peso (%) | Contribuição (p.p.) |
|---|---|---|---|---|
| Energia elétrica residencial | 7.98 | 2.76 | 3.98 | 0.318 |
| Tubérculos, raízes e legumes | 18.92 | 48.29 | 0.74 | 0.140 |
| Combustíveis (veículos) | 1.41 | 4.96 | 6.05 | 0.085 |
| Transporte público | 2.50 | 12.19 | 3.14 | 0.078 |
| Alimentação fora do domicílio | 0.48 | 5.79 | 6.13 | 0.029 |
| Comunicação | 0.64 | 2.78 | 4.51 | 0.029 |
| Serviços pessoais | 0.40 | 6.09 | 6.39 | 0.026 |
| Aluguel e taxas | 0.26 | 4.97 | 7.80 | 0.020 |

### inflc_dim

Tabela sem data (classificação), 614 linhas · A: `A/inflc_dim.csv.gz`

Peso no IPCA de 2026-09. A tabela guarda subitens que já saíram da cesta; só os do mês têm peso.

| Grupo do BC | Classe | Subitens | No IPCA do mês | Peso (%) |
|---|---|---|---|---|
| Alimentos | Alimentos in natura | 56 | 39 | 2.4 |
| Alimentos | Alimentos industrializados | 120 | 71 | 7.5 |
| Alimentos | Alimentos semi-elaborados | 80 | 49 | 5.5 |
| Alimentos | — | 5 | 0 | 0.0 |
| Bens Industriais | Duráveis | 48 | 25 | 9.0 |
| Bens Industriais | Não Duráveis | 64 | 45 | 7.6 |
| Bens Industriais | Semi-duráveis | 89 | 43 | 5.9 |
| Monitorados | Monitorados | 44 | 37 | 26.0 |
| Serviços | Serviços Ex Subjacentes | 31 | 24 | 14.6 |
| Serviços | Serviços Subjacente | 77 | 44 | 21.6 |

## v. TWA — atividade (leitura enxuta)

### atv_pib

Último dado 2026-04-01 (204 dias antes do corte) · A: `A/atv_pib.csv.gz`

| Série | Unidade | Data | Último | Δ% 1t | Δ% 4t | Δ% desde o ciclo ant. |
|---|---|---|---|---|---|---|
| PIB | índice, dessaz. | 2026-04-01 | 198.24 | +0.5 | +1.9 | sem dado novo |
| Consumo das famílias | índice, dessaz. | 2026-04-01 | 208.27 | -0.4 | +0.4 | sem dado novo |
| Consumo do governo | índice, dessaz. | 2026-04-01 | 167.44 | +0.4 | +3.1 | sem dado novo |
| FBCF | índice, dessaz. | 2026-04-01 | 183.60 | +1.2 | +1.4 | sem dado novo |
| Exportação | índice, dessaz. | 2026-04-01 | 402.36 | -0.8 | +4.2 | sem dado novo |
| Importação | índice, dessaz. | 2026-04-01 | 328.82 | +1.8 | +5.4 | sem dado novo |
| Agropecuária | índice, dessaz. | 2026-04-01 | 307.40 | +2.8 | +6.4 | sem dado novo |
| Indústria | índice, dessaz. | 2026-04-01 | 146.95 | +0.1 | +1.2 | sem dado novo |
| Serviços | índice, dessaz. | 2026-04-01 | 206.74 | +0.2 | +1.5 | sem dado novo |

### atv_pib_taxas

Último dado 2026-04-01 (204 dias antes do corte) · A: `A/atv_pib_taxas.csv.gz`

| Série | Unidade | Data | Último | Δ 1t | Δ 4t | Δ desde o ciclo ant. |
|---|---|---|---|---|---|---|
| PIB, contra o trimestre anterior (dessaz.) | % | 2026-04-01 | 0.5 | -0.6 | +0.1 | sem dado novo |
| PIB, contra o mesmo trimestre do ano anterior | % | 2026-04-01 | 2.0 | +0.2 | -0.4 | sem dado novo |
| PIB, acumulado em 4 trimestres | % | 2026-04-01 | 1.9 | -0.1 | -1.4 | sem dado novo |
| Consumo das famílias, contra o trimestre anterior | % | 2026-04-01 | -0.4 | -1.2 | -1.2 | sem dado novo |
| FBCF, contra o trimestre anterior | % | 2026-04-01 | 1.2 | -2.2 | +3.1 | sem dado novo |
| Serviços, contra o trimestre anterior | % | 2026-04-01 | 0.2 | -0.2 | -0.6 | sem dado novo |
| Indústria, contra o trimestre anterior | % | 2026-04-01 | 0.1 | -1.1 | -0.6 | sem dado novo |

### atv_pib_valores_correntes

Último dado 2026-04-01 (204 dias antes do corte) · A: `A/atv_pib_valores_correntes.csv.gz`

Preços correntes. PIB de 4 trimestres: R$ 13.19 tri.

| Componente | % do PIB, 4 tri até 2T26 | Um ano antes |
|---|---|---|
| Consumo das famílias | 63.1 | 63.7 |
| Consumo do governo | 19.6 | 18.7 |
| Formação bruta de capital fixo | 16.5 | 17.2 |
| Variação de estoques | 0.2 | 0.7 |
| Exportação | 17.2 | 18.2 |
| Importação | 16.6 | 18.4 |

### atv_pib_mensal

Último dado 2026-08-01 (82 dias antes do corte) · A: `A/atv_pib_mensal.csv.gz`

| Série | Unidade | Data | Último | Δ% 1m | Δ% 3m | Δ% 12m | Δ% desde o ciclo ant. |
|---|---|---|---|---|---|---|---|
| PIB nominal, 12 meses | R$ bi | 2026-08-01 | 13342 | +0.6 | +1.8 | +7.2 | sem dado novo |

### atv_ibcbr

Último dado 2026-07-01 (113 dias antes do corte) · A: `A/atv_ibcbr.csv.gz`

| Série | Unidade | Data | Último | Δ% 1m | Δ% 3m | Δ% 12m | Δ% desde o ciclo ant. |
|---|---|---|---|---|---|---|---|
| IBC-Br | índice, dessaz. | 2026-07-01 | 109.92 | -0.2 | -0.9 | +1.3 | sem dado novo |
| IBC-Br ex-agropecuária | índice, dessaz. | 2026-07-01 | 108.72 | -0.1 | -1.0 | +1.1 | sem dado novo |
| Agropecuária | índice, dessaz. | 2026-07-01 | 130.01 | -1.2 | -1.1 | +4.3 | sem dado novo |
| Indústria | índice, dessaz. | 2026-07-01 | 105.00 | -0.4 | -1.5 | +0.4 | sem dado novo |
| Serviços | índice, dessaz. | 2026-07-01 | 110.12 | -0.0 | -0.4 | +1.4 | sem dado novo |

### atv_pim

Último dado 2026-08-01 (82 dias antes do corte) · A: `A/atv_pim.csv.gz`

| Série | Unidade | Data | Último | Δ% 1m | Δ% 3m | Δ% 12m | Δ% desde o ciclo ant. |
|---|---|---|---|---|---|---|---|
| Indústria geral | índice, dessaz. | 2026-08-01 | 103.25 | -0.6 | -2.1 | -1.4 | sem dado novo |
| Transformação | índice, dessaz. | 2026-08-01 | 101.01 | -0.7 | -2.2 | -1.9 | sem dado novo |
| Extrativa | índice, dessaz. | 2026-08-01 | 116.56 | -0.7 | -2.0 | +1.7 | sem dado novo |

### atv_pim_uso

Último dado 2026-08-01 (82 dias antes do corte) · A: `A/atv_pim_uso.csv.gz`

| Série | Unidade | Data | Último | Δ% 1m | Δ% 3m | Δ% 12m | Δ% desde o ciclo ant. |
|---|---|---|---|---|---|---|---|
| Bens de capital | índice, dessaz. | 2026-08-01 | 90.38 | -0.6 | -0.8 | -3.9 | sem dado novo |
| Bens intermediários | índice, dessaz. | 2026-08-01 | 105.62 | -0.2 | -1.5 | -0.3 | sem dado novo |
| Bens de consumo duráveis | índice, dessaz. | 2026-08-01 | 119.03 | -1.0 | -0.8 | +3.2 | sem dado novo |
| Bens de consumo semi e não duráveis | índice, dessaz. | 2026-08-01 | 98.09 | -1.7 | -4.8 | -5.0 | sem dado novo |

### atv_pmc

Último dado 2026-08-01 (82 dias antes do corte) · A: `A/atv_pmc.csv.gz`

| Série | Unidade | Data | Último | Δ% 1m | Δ% 3m | Δ% 12m | Δ% desde o ciclo ant. |
|---|---|---|---|---|---|---|---|
| Varejo restrito | índice, dessaz. | 2026-08-01 | 108.69 | +0.1 | -0.4 | +1.0 | sem dado novo |
| Varejo ampliado | índice, dessaz. | 2026-08-01 | 106.63 | -0.2 | -0.9 | +0.6 | sem dado novo |
| Super e hipermercados | índice, dessaz. | 2026-08-01 | 112.49 | -0.1 | +0.8 | +1.6 | sem dado novo |
| Móveis e eletrodomésticos | índice, dessaz. | 2026-08-01 | 102.97 | -4.2 | -8.7 | -8.4 | sem dado novo |
| Veículos, motos e peças | índice, dessaz. | 2026-08-01 | 119.73 | -1.0 | -2.1 | +2.0 | sem dado novo |

### atv_pms

Último dado 2026-08-01 (82 dias antes do corte) · A: `A/atv_pms.csv.gz`

| Série | Unidade | Data | Último | Δ% 1m | Δ% 3m | Δ% 12m | Δ% desde o ciclo ant. |
|---|---|---|---|---|---|---|---|
| Serviços, total | índice, dessaz. | 2026-08-01 | 110.51 | -0.1 | +0.1 | +0.6 | sem dado novo |
| Prestados às famílias | índice, dessaz. | 2026-08-01 | 115.63 | +2.1 | +1.5 | +4.2 | sem dado novo |
| Informação e comunicação | índice, dessaz. | 2026-08-01 | 122.02 | -0.0 | -0.5 | +4.8 | sem dado novo |
| Profissionais e administrativos | índice, dessaz. | 2026-08-01 | 118.91 | -0.2 | -0.9 | +1.5 | sem dado novo |
| Transportes e correio | índice, dessaz. | 2026-08-01 | 100.98 | -0.2 | +0.2 | -3.1 | sem dado novo |

### atv_renda_poupanca

Último dado 2026-04-01 (204 dias antes do corte) · A: `A/atv_renda_poupanca.csv.gz`

Contas nacionais trimestrais, preços correntes.

| Conta | % do PIB, 4 tri até 2T26 | Um ano antes | Δ (p.p.) |
|---|---|---|---|
| Poupança bruta | 14.4 | 14.4 | -0.0 |
| Formação bruta de capital | 16.7 | 17.8 | -1.1 |
| Capacidade (+) ou necessidade (−) de financiamento | -2.3 | -3.4 | +1.1 |
| Rendas de propriedade líquidas com o exterior (− = envio) | -3.1 | -3.4 | +0.2 |

## vi. TWA — mercado de trabalho (leitura enxuta)

### mt_pnad

Último dado 2026-08-01 (82 dias antes do corte) · A: `A/mt_pnad.csv.gz`

| Série | Unidade | Data | Último | Δ 1m | Δ 3m | Δ 12m | Δ desde o ciclo ant. |
|---|---|---|---|---|---|---|---|
| Taxa de desocupação | % | 2026-08-01 | 5.3 | +0.0 | -0.3 | -0.3 | sem dado novo |
| Taxa de participação | % | 2026-08-01 | 62.2 | +0.0 | +0.2 | -0.1 | sem dado novo |
| Nível de ocupação | % da PIA | 2026-08-01 | 58.9 | +0.0 | +0.3 | +0.1 | sem dado novo |
| Subutilização composta | % | 2026-08-01 | 13.1 | +0.1 | -0.2 | -1.0 | sem dado novo |
| Informalidade | % dos ocupados | 2026-08-01 | 37.5 | +0.0 | +0.2 | -0.5 | sem dado novo |

| Série | Unidade | Data | Último | Δ% 1m | Δ% 3m | Δ% 12m | Δ% desde o ciclo ant. |
|---|---|---|---|---|---|---|---|
| Ocupados | mil pessoas | 2026-08-01 | 103477 | +0.1 | +0.8 | +1.0 | sem dado novo |
| Rendimento habitual real | R$ | 2026-08-01 | 3777 | +0.5 | +0.7 | +3.7 | sem dado novo |
| Massa de rendimento habitual real | R$ bi | 2026-08-01 | 385.6 | +0.6 | +1.4 | +4.8 | sem dado novo |

### mt_desocupacao_retro

Último dado 2026-09-01 (51 dias antes do corte) · A: `A/mt_desocupacao_retro.csv.gz`

| Série | Unidade | Data | Último | Δ 1m | Δ 3m | Δ 12m | Δ desde o ciclo ant. |
|---|---|---|---|---|---|---|---|
| Desocupação dessazonalizada, retropolada pelo BC | % | 2026-07-01 | 5.41 | -0.02 | -0.01 | -0.32 | sem dado novo |

### mt_caged

Último dado 2026-08-01 (82 dias antes do corte) · A: `A/mt_caged.csv.gz`

| Série | Unidade | Data | Último | Δ% 1m | Δ% 3m | Δ% 12m | Δ% desde o ciclo ant. |
|---|---|---|---|---|---|---|---|
| Estoque de emprego formal | mil empregos | 2026-08-01 | 48245 | +0.3 | +0.7 | +1.9 | sem dado novo |
| Serviços | mil empregos | 2026-08-01 | 23587 | +0.5 | +0.9 | +2.9 | sem dado novo |
| Comércio | mil empregos | 2026-08-01 | 10490 | +0.2 | +0.3 | +0.9 | sem dado novo |
| Indústria de transformação | mil empregos | 2026-08-01 | 8292 | +0.2 | +0.5 | +0.2 | sem dado novo |
| Construção | mil empregos | 2026-08-01 | 3151 | +0.7 | +1.5 | +3.0 | sem dado novo |

### mt_caged_setor

Último dado 2026-08-01 (82 dias antes do corte) · A: `A/mt_caged_setor.csv.gz`

| Série | Unidade | Último mês | Soma 3m | Soma 12m | Soma 12m, um ano antes |
|---|---|---|---|---|---|
| Saldo: comércio | mil empregos | 16.6 (2026-08) | 31.3 | 97.7 | 322.2 |
| Saldo: indústria de transformação | mil empregos | 15.2 (2026-08) | 37.2 | 15.9 | 210.3 |
| Saldo: construção | mil empregos | 20.8 (2026-08) | 46.0 | 91.6 | 88.7 |
| Saldo: agropecuária | mil empregos | 1.5 (2026-08) | 37.9 | -10.7 | 35.2 |
| Saldo: alojamento e alimentação | mil empregos | 11.7 (2026-08) | 16.7 | 65.7 | 79.0 |
| Saldo: informação e comunicação | mil empregos | 0.6 (2026-08) | 1.0 | 9.7 | 24.9 |
| Saldo: serviços administrativos | mil empregos | 16.4 (2026-08) | 45.0 | 193.0 | 210.8 |
| Saldo: saúde | mil empregos | 19.1 (2026-08) | 43.6 | 130.9 | 131.4 |
| Saldo: educação | mil empregos | 25.4 (2026-08) | 10.7 | 16.9 | 47.6 |

## vii. TWA — crédito (leitura enxuta)

### cred_credito_resumo

Último dado 2026-08-01 (82 dias antes do corte) · A: `A/cred_credito_resumo.csv.gz`

| Série | Unidade | Data | Último | Δ% 1m | Δ% 3m | Δ% 12m | Δ% desde o ciclo ant. |
|---|---|---|---|---|---|---|---|
| Saldo total | R$ bi | 2026-08-01 | 7398 | +0.5 | +1.3 | +9.2 | sem dado novo |
| Saldo livre PF | R$ bi | 2026-08-01 | 2572 | +0.8 | +1.1 | +10.5 | sem dado novo |
| Saldo livre PJ | R$ bi | 2026-08-01 | 1575 | -0.7 | -1.1 | +0.5 | sem dado novo |

| Série | Unidade | Último mês | Soma 3m | Soma 12m | Soma 12m, um ano antes |
|---|---|---|---|---|---|
| Concessões livres PF | R$ bi | 346.6 (2026-08) | 1039.0 | 4074.7 | 3685.6 |
| Concessões livres PJ | R$ bi | 301.3 (2026-08) | 927.7 | 3487.1 | 3126.1 |

| Série | Unidade | Data | Último | Δ 1m | Δ 3m | Δ 12m | Δ desde o ciclo ant. |
|---|---|---|---|---|---|---|---|
| Taxa de juros, livre PF | % a.a. | 2026-08-01 | 61.74 | +1.44 | -0.45 | +2.95 | sem dado novo |
| Taxa de juros, livre PJ | % a.a. | 2026-08-01 | 24.19 | -0.96 | -0.74 | -0.74 | sem dado novo |
| Spread, livre | p.p. | 2026-08-01 | 34.73 | +0.86 | -0.53 | +2.29 | sem dado novo |
| Custo do crédito (ICC) | % a.a. | 2026-08-01 | 24.19 | +0.13 | -0.05 | +0.80 | sem dado novo |
| Inadimplência, livre PF | % da carteira | 2026-08-01 | 8.01 | +0.23 | +0.45 | +1.04 | sem dado novo |
| Inadimplência, livre PJ | % da carteira | 2026-08-01 | 4.33 | +0.12 | +0.22 | +0.55 | sem dado novo |

### cred_fluxo_financeiro

Último dado 2026-06-01 (143 dias antes do corte) · A: `A/cred_fluxo_financeiro.csv.gz`

| Série | Unidade | Data | Último | Δ 1m | Δ 3m | Δ 12m | Δ desde o ciclo ant. |
|---|---|---|---|---|---|---|---|
| Fluxo financeiro, total | % do PIB, 12m | 2026-04-01 | -2.8 | -0.2 | -0.7 | -2.1 | sem dado novo |
| Fluxo financeiro, PF | % do PIB, 12m | 2026-04-01 | -1.8 | -0.1 | -0.4 | -1.4 | sem dado novo |
| Fluxo financeiro, PJ | % do PIB, 12m | 2026-04-01 | -1.0 | -0.1 | -0.3 | -0.7 | sem dado novo |

### cred_ptc

Último dado 2026-04-01 (204 dias antes do corte) · A: `A/cred_ptc.csv.gz`

| Série | Unidade | Data | Último | Δ 1t | Δ 4t | Δ desde o ciclo ant. |
|---|---|---|---|---|---|---|
| PF consumo: oferta, observada | índice, −1 a 1 | 2026-04-01 | -0.23 | +0.06 | -0.16 | sem dado novo |
| PF consumo: demanda, observada | índice, −1 a 1 | 2026-04-01 | 0.19 | +0.01 | +0.19 | sem dado novo |
| PF habitação: oferta, observada | índice, −1 a 1 | 2026-04-01 | 0.00 | -0.29 | +0.43 | sem dado novo |
| PF habitação: demanda, observada | índice, −1 a 1 | 2026-04-01 | 0.43 | +0.29 | +0.86 | sem dado novo |
| Grandes empresas: oferta, observada | índice, −1 a 1 | 2026-04-01 | -0.24 | +0.08 | +0.03 | sem dado novo |
| Grandes empresas: demanda, observada | índice, −1 a 1 | 2026-04-01 | 0.14 | +0.19 | +0.00 | sem dado novo |
| Micro, pequenas e médias: oferta, observada | índice, −1 a 1 | 2026-04-01 | -0.19 | +0.17 | -0.01 | sem dado novo |
| Micro, pequenas e médias: demanda, observada | índice, −1 a 1 | 2026-04-01 | 0.19 | +0.23 | +0.23 | sem dado novo |

### cred_credito_familias

Último dado 2026-07-01 (113 dias antes do corte) · A: `A/cred_credito_familias.csv.gz`

| Série | Unidade | Data | Último | Δ 1m | Δ 3m | Δ 12m | Δ desde o ciclo ant. |
|---|---|---|---|---|---|---|---|
| Endividamento das famílias | % da renda 12m | 2026-07-01 | 49.86 | +0.21 | -0.02 | +1.08 | sem dado novo |
| Endividamento sem imobiliário | % da renda 12m | 2026-07-01 | 30.81 | +0.04 | -0.38 | +0.29 | sem dado novo |
| Comprometimento de renda com o serviço da dívida | % da renda | 2026-07-01 | 28.72 | +0.06 | +0.34 | +1.40 | sem dado novo |
| Comprometimento de renda com juros | % da renda | 2026-07-01 | 10.83 | +0.05 | +0.17 | +0.88 | sem dado novo |

### cred_credito_amplo

Último dado 2026-08-01 (82 dias antes do corte) · A: `A/cred_credito_amplo.csv.gz`

| Série | Unidade | Data | Último | Δ% 1m | Δ% 3m | Δ% 12m | Δ% desde o ciclo ant. |
|---|---|---|---|---|---|---|---|
| Empresas: empréstimos do SFN | R$ bi | 2026-08-01 | 2352 | +0.0 | +0.7 | +7.0 | sem dado novo |
| Empresas: títulos de dívida | R$ bi | 2026-08-01 | 1527 | +0.6 | +2.4 | +16.0 | sem dado novo |
| Empresas: dívida externa | R$ bi | 2026-08-01 | 73 | +1.8 | +3.5 | -9.6 | sem dado novo |
| Famílias: empréstimos do SFN | R$ bi | 2026-08-01 | 4670 | +0.8 | +1.6 | +10.5 | sem dado novo |
| Governo: títulos públicos | R$ bi | 2026-08-01 | 8098 | -0.1 | +3.2 | +13.9 | sem dado novo |

### cred_modalidade_livre_pf

Último dado 2026-08-01 (82 dias antes do corte) · A: `A/cred_modalidade_livre_pf.csv.gz`

| Série | Unidade | Data | Último | Δ 1m | Δ 3m | Δ 12m | Δ desde o ciclo ant. |
|---|---|---|---|---|---|---|---|
| Consignado: taxa | % a.a. | 2026-08-01 | 29.00 | +0.57 | +1.09 | +2.33 | sem dado novo |
| Pessoal não consignado: taxa | % a.a. | 2026-08-01 | 110.22 | -0.75 | -5.82 | +6.25 | sem dado novo |
| Veículos: taxa | % a.a. | 2026-08-01 | 26.42 | -0.10 | +0.11 | -0.92 | sem dado novo |
| Cartão rotativo: taxa | % a.a. | 2026-08-01 | 444.89 | +8.74 | +3.83 | -8.75 | sem dado novo |
| Pessoal não consignado: inadimplência | % da carteira | 2026-08-01 | 10.95 | +0.30 | +0.51 | +1.82 | sem dado novo |
| Veículos: inadimplência | % da carteira | 2026-08-01 | 6.57 | -0.06 | +0.10 | +1.07 | sem dado novo |

| Série | Unidade | Último mês | Soma 3m | Soma 12m | Soma 12m, um ano antes |
|---|---|---|---|---|---|
| Pessoal não consignado: concessões | R$ bi | 23.04 (2026-08) | 66.52 | 264.47 | 252.80 |
| Veículos: concessões | R$ bi | 22.55 (2026-08) | 66.38 | 253.94 | 212.40 |

### cred_modalidade_livre_pj

Último dado 2026-08-01 (82 dias antes do corte) · A: `A/cred_modalidade_livre_pj.csv.gz`

| Série | Unidade | Data | Último | Δ 1m | Δ 3m | Δ 12m | Δ desde o ciclo ant. |
|---|---|---|---|---|---|---|---|
| Capital de giro: taxa | % a.a. | 2026-08-01 | 22.89 | -1.60 | -0.21 | -3.23 | sem dado novo |
| Desconto de duplicatas: taxa | % a.a. | 2026-08-01 | 18.60 | -0.65 | -1.02 | -1.64 | sem dado novo |
| Conta garantida: taxa | % a.a. | 2026-08-01 | 56.15 | -1.23 | -7.20 | -2.86 | sem dado novo |
| Capital de giro: inadimplência | % da carteira | 2026-08-01 | 5.98 | +0.19 | +0.45 | +0.78 | sem dado novo |

| Série | Unidade | Último mês | Soma 3m | Soma 12m | Soma 12m, um ano antes |
|---|---|---|---|---|---|
| Capital de giro: concessões | R$ bi | 53.95 (2026-08) | 153.19 | 534.92 | 335.29 |

### cred_modalidade_direcionado_pf

Último dado 2026-08-01 (82 dias antes do corte) · A: `A/cred_modalidade_direcionado_pf.csv.gz`

| Série | Unidade | Data | Último | Δ% 1m | Δ% 3m | Δ% 12m | Δ% desde o ciclo ant. |
|---|---|---|---|---|---|---|---|
| Imobiliário: saldo | R$ bi | 2026-08-01 | 1431 | +1.1 | +3.8 | +13.8 | sem dado novo |
| Rural: saldo | R$ bi | 2026-08-01 | 558 | -0.1 | -2.1 | +2.9 | sem dado novo |

| Série | Unidade | Data | Último | Δ 1m | Δ 3m | Δ 12m | Δ desde o ciclo ant. |
|---|---|---|---|---|---|---|---|
| Imobiliário: taxa | % a.a. | 2026-08-01 | 11.28 | -0.02 | +0.05 | +0.79 | sem dado novo |

### cred_modalidade_direcionado_pj

Último dado 2026-08-01 (82 dias antes do corte) · A: `A/cred_modalidade_direcionado_pj.csv.gz`

| Série | Unidade | Data | Último | Δ% 1m | Δ% 3m | Δ% 12m | Δ% desde o ciclo ant. |
|---|---|---|---|---|---|---|---|
| BNDES: saldo | R$ bi | 2026-08-01 | 497 | +0.4 | +2.0 | +10.3 | sem dado novo |
| Rural: saldo | R$ bi | 2026-08-01 | 127 | -0.4 | +1.1 | +30.6 | sem dado novo |

| Série | Unidade | Data | Último | Δ 1m | Δ 3m | Δ 12m | Δ desde o ciclo ant. |
|---|---|---|---|---|---|---|---|
| BNDES: taxa | % a.a. | 2026-08-01 | 11.73 | -1.51 | -4.45 | -2.16 | sem dado novo |

### cred_credito_controle_capital

Último dado 2026-08-01 (82 dias antes do corte) · A: `A/cred_credito_controle_capital.csv.gz`

| Série | Unidade | Data | Último | Δ% 1m | Δ% 3m | Δ% 12m | Δ% desde o ciclo ant. |
|---|---|---|---|---|---|---|---|
| Saldo: bancos públicos | R$ bi | 2026-08-01 | 3085 | +0.4 | +1.5 | +8.2 | sem dado novo |
| Saldo: privados nacionais | R$ bi | 2026-08-01 | 3321 | +0.6 | +1.2 | +10.0 | sem dado novo |
| Saldo: estrangeiros | R$ bi | 2026-08-01 | 992 | +0.4 | +0.8 | +9.5 | sem dado novo |

| Série | Unidade | Data | Último | Δ 1m | Δ 3m | Δ 12m | Δ desde o ciclo ant. |
|---|---|---|---|---|---|---|---|
| Inadimplência: bancos públicos | % da carteira | 2026-08-01 | 4.67 | +0.21 | +0.33 | +1.10 | sem dado novo |
| Inadimplência: privados nacionais | % da carteira | 2026-08-01 | 5.46 | +0.09 | +0.33 | +0.77 | sem dado novo |
| Inadimplência: estrangeiros | % da carteira | 2026-08-01 | 4.79 | +0.24 | +0.08 | +0.94 | sem dado novo |

### cred_inadimplencia_pj

Último dado 2026-09-01 (51 dias antes do corte) · A: `A/cred_inadimplencia_pj.csv.gz`

| Série | Unidade | Data | Último | Δ 1m | Δ 3m | Δ 12m | Δ desde o ciclo ant. |
|---|---|---|---|---|---|---|---|
| Inadimplência PJ (acima de 90 dias) | % da carteira | 2026-08-01 | 3.35 | +0.03 | +0.10 | +0.50 | sem dado novo |
| Atraso PJ de 15 a 90 dias | % da carteira | 2026-08-01 | 2.18 | -0.12 | +0.02 | +0.36 | sem dado novo |
| Taxa de juros PJ | % a.a. | 2026-08-01 | 19.75 | -1.06 | -1.49 | -1.75 | sem dado novo |

| Série | Unidade | Último mês | Soma 3m | Soma 12m | Soma 12m, um ano antes |
|---|---|---|---|---|---|
| Concessões PJ | R$ bi | 335.0 (2026-08) | 1027.2 | 3859.1 | 3447.0 |

## viii. TWA — fiscal (leitura enxuta)

### fisc_nfsp

Último dado 2026-08-01 (82 dias antes do corte) · A: `A/fisc_nfsp.csv.gz`

| Série | Unidade | Data | Último | Δ 1m | Δ 3m | Δ 12m | Δ desde o ciclo ant. |
|---|---|---|---|---|---|---|---|
| Resultado primário, 12m (+ = superávit) | % do PIB | 2026-08-01 | -0.62 | +0.05 | +0.52 | -0.43 | sem dado novo |
| Primário do governo federal e BC, 12m | % do PIB | 2026-08-01 | -0.53 | +0.02 | +0.51 | -0.30 | sem dado novo |
| Resultado nominal, 12m | % do PIB | 2026-08-01 | -9.48 | -0.13 | +0.13 | -1.69 | sem dado novo |
| Juros nominais, 12m | % do PIB | 2026-08-01 | 8.86 | +0.18 | +0.38 | +1.25 | sem dado novo |

### fisc_divida

Último dado 2026-08-01 (82 dias antes do corte) · A: `A/fisc_divida.csv.gz`

| Série | Unidade | Data | Último | Δ 1m | Δ 3m | Δ 12m | Δ desde o ciclo ant. |
|---|---|---|---|---|---|---|---|
| Dívida bruta do governo geral | % do PIB | 2026-08-01 | 82.9 | +0.3 | +1.8 | +5.5 | sem dado novo |
| Dívida líquida do setor público | % do PIB | 2026-08-01 | 69.3 | +0.1 | +1.4 | +5.2 | sem dado novo |

### fisc_dlsp_fatores

Último dado 2026-08-01 (82 dias antes do corte) · A: `A/fisc_dlsp_fatores.csv.gz`

Setor público consolidado, até 2026-08. Fluxo que AUMENTA a dívida é positivo. Estoque da dívida líquida: R$ 9.24 tri.

| Fator | Último mês (R$ bi) | 12m (R$ bi) | 12m % do PIB | 12m, um ano antes (R$ bi) |
|---|---|---|---|---|
| Resultado primário (+ = déficit) | 10.0 | 82.1 | 0.62 | 23.1 |
| Juros nominais | 105.9 | 1182.2 | 8.86 | 946.5 |
| Ajuste cambial da dívida externa | -26.7 | 60.5 | 0.45 | 42.8 |
| Ajuste da dívida interna indexada | -0.6 | 1.2 | 0.01 | 1.4 |
| Ajuste de paridade da cesta de moedas | -12.9 | -27.8 | -0.21 | -52.7 |
| Reconhecimento de dívidas | 3.0 | 8.2 | 0.06 | 15.4 |
| Privatizações | -0.5 | -17.2 | -0.13 | -0.6 |
| Ajuste caixa-competência | -2.4 | -17.3 | -0.13 | -32.9 |

### fisc_rtn

Último dado 2026-08-01 (82 dias antes do corte) · A: `A/fisc_rtn.csv.gz`

| Série | Unidade | Último mês | Soma 3m | Soma 12m | Soma 12m, um ano antes |
|---|---|---|---|---|---|
| Primário do governo central (+ = superávit) | R$ bi | -13.6 (2026-08) | -50.7 | -70.7 | -30.4 |
| Receita líquida | R$ bi | 187.9 (2026-08) | 609.6 | 2488.4 | 2290.2 |
| Despesa total | R$ bi | 201.5 (2026-08) | 660.3 | 2559.1 | 2320.6 |

### fisc_efgg

Último dado 2026-04-01 (204 dias antes do corte) · A: `A/fisc_efgg.csv.gz`

Governo geral (GFSM) = soma de União, estados e municípios, SEM consolidar as transferências entre esferas: receita e despesa ficam acima das do governo geral consolidado; leia a variação, não o nível. Soma de quatro trimestres sobre o PIB nominal dos mesmos quatro.

| Conta | % do PIB, 4 tri até 2T26 | Um ano antes | Δ (p.p.) |
|---|---|---|---|
| Receita total | 51.8 | 50.3 | +1.5 |
| Despesa total | 60.2 | 56.4 | +3.7 |
| Juros | 11.4 | 9.6 | +1.8 |
| Benefícios previdenciários e assistenciais | 16.0 | 15.6 | +0.4 |
| Remuneração de empregados | 11.2 | 10.9 | +0.3 |
| Investimento líquido | 0.5 | 0.4 | +0.0 |

## ix. TWA — externo (leitura enxuta)

### us_interest_rate

Último dado 2026-10-21 (1 dia antes do corte) · A: `A/us_interest_rate__curva.csv.gz`

| Série | Unidade | Data | Último | Δ 1m | Δ 3m | Δ 12m | Δ desde o ciclo ant. |
|---|---|---|---|---|---|---|---|
| Fed Funds, meta (ponto médio) | % a.a. | 2026-10-21 | 3.88 | +0.00 | +0.25 | -0.25 | +0.00 |
| Treasury 3 meses | % a.a. | 2026-10-19 | 4.27 | +0.13 | +0.42 | +0.27 | -0.01 |
| Treasury 2 anos | % a.a. | 2026-10-19 | 4.77 | +0.01 | +0.59 | +1.31 | +0.00 |
| Treasury 5 anos | % a.a. | 2026-10-19 | 4.94 | +0.08 | +0.66 | +1.35 | +0.03 |
| Treasury 10 anos | % a.a. | 2026-10-19 | 5.15 | +0.14 | +0.60 | +1.13 | +0.05 |
| Treasury 30 anos | % a.a. | 2026-10-19 | 5.48 | +0.14 | +0.42 | +0.88 | +0.05 |

### inter_interest_rate

Último dado 2026-10-13 (9 dias antes do corte) · A: `A/inter_interest_rate.csv.gz`

| Série | Unidade | Data | Último | Δ 1m | Δ 3m | Δ 12m | Δ desde o ciclo ant. |
|---|---|---|---|---|---|---|---|
| México, juro de política | % a.a. | 2026-10-13 | 6.50 | +0.00 | +0.00 | -1.00 | sem dado novo |
| Chile, juro de política | % a.a. | 2026-10-13 | 4.50 | +0.00 | +0.00 | -0.25 | sem dado novo |
| Colômbia, juro de política | % a.a. | 2026-10-09 | 12.25 | +0.25 | +0.25 | +3.00 | sem dado novo |
| Peru, juro de política | % a.a. | 2026-10-12 | 4.25 | +0.00 | +0.00 | +0.00 | sem dado novo |

### cmb_real_rates

Último dado 2026-08-01 (82 dias antes do corte) · A: `A/cmb_real_rates.csv.gz`

| Série | Unidade | Data | Último | Δ 1m | Δ 3m | Δ 12m | Δ desde o ciclo ant. |
|---|---|---|---|---|---|---|---|
| BR, juro real ex-post | % a.a. | 2026-08-01 | 9.78 | -0.03 | +0.00 | -0.09 | sem dado novo |
| MX, juro real ex-post | % a.a. | 2026-08-01 | 3.24 | -0.14 | +0.68 | -0.94 | sem dado novo |
| CL, juro real ex-post | % a.a. | 2026-08-01 | 0.37 | -0.61 | -0.20 | -0.35 | sem dado novo |
| CO, juro real ex-post | % a.a. | 2026-08-01 | 5.76 | -0.22 | +0.35 | +1.60 | sem dado novo |
| PE, juro real ex-post | % a.a. | 2026-08-01 | -0.19 | -0.37 | -0.53 | -3.58 | sem dado novo |

### cmb_dollar_index

Último dado 2026-10-21 (1 dia antes do corte) · A: `A/cmb_dollar_index.csv.gz`

| Série | Unidade | Data | Último | Δ% 1m | Δ% 3m | Δ% 12m | Δ% desde o ciclo ant. |
|---|---|---|---|---|---|---|---|
| DXY | índice | 2026-10-21 | 101.78 | +1.3 | +0.6 | +2.9 | -0.2 |

### cmb_dollar_index_em

Último dado 2026-10-16 (6 dias antes do corte) · A: `A/cmb_dollar_index_em.csv.gz`

| Série | Unidade | Data | Último | Δ% 1m | Δ% 3m | Δ% 12m | Δ% desde o ciclo ant. |
|---|---|---|---|---|---|---|---|
| Dólar contra emergentes (FRED) | índice | 2026-10-16 | 129.98 | +2.2 | +0.7 | -1.2 | +0.0 |

### comm_brent

Último dado 2026-10-14 (8 dias antes do corte) · A: `A/comm_brent.csv.gz`

| Série | Unidade | Data | Último | Δ% 1m | Δ% 3m | Δ% 12m | Δ% desde o ciclo ant. |
|---|---|---|---|---|---|---|---|
| Brent | US$/barril | 2026-10-14 | 126.55 | +4.4 | +51.2 | +100.9 | sem dado novo |

### comm_icbr

Último dado 2026-09-01 (51 dias antes do corte) · A: `A/comm_icbr.csv.gz`

| Série | Unidade | Data | Último | Δ% 1m | Δ% 3m | Δ% 12m | Δ% desde o ciclo ant. |
|---|---|---|---|---|---|---|---|
| IC-Br | índice, em R$ | 2026-09-01 | 462.94 | +1.5 | +4.5 | +8.1 | sem dado novo |
| IC-Br agropecuária | índice, em R$ | 2026-09-01 | 454.03 | +0.1 | +3.8 | -3.5 | sem dado novo |
| IC-Br metal | índice, em R$ | 2026-09-01 | 754.19 | -0.8 | +1.1 | +36.3 | sem dado novo |
| IC-Br energia | índice, em R$ | 2026-09-01 | 216.23 | +10.4 | +11.7 | +23.8 | sem dado novo |

### comm_icbr_usd

Último dado 2026-09-01 (51 dias antes do corte) · A: `A/comm_icbr_usd.csv.gz`

| Série | Unidade | Data | Último | Δ% 1m | Δ% 3m | Δ% 12m | Δ% desde o ciclo ant. |
|---|---|---|---|---|---|---|---|
| IC-Br em dólar | índice | 2026-09-01 | 205.70 | +1.7 | +4.1 | +12.8 | sem dado novo |
| IC-Br agropecuária | índice | 2026-09-01 | 201.80 | +0.3 | +3.3 | +0.7 | sem dado novo |
| IC-Br metal | índice | 2026-09-01 | 335.06 | -0.6 | +0.7 | +42.2 | sem dado novo |
| IC-Br energia | índice | 2026-09-01 | 96.00 | +10.6 | +11.2 | +29.2 | sem dado novo |

## x. Exógeno (leitura enxuta)

### cmb_risco_pais

Último dado 2026-10-14 (8 dias antes do corte) · A: `A/cmb_risco_pais.csv.gz`

| Série | Unidade | Data | Último | Δ 1m | Δ 3m | Δ 12m | Δ desde o ciclo ant. |
|---|---|---|---|---|---|---|---|
| CDS 5 anos Brasil | p.b. | 2026-10-14 | 112 | +0 | -11 | -40 | sem dado novo |

## Leituras combinadas

### A Selic por reunião: curva DI e Focus

Selic vigente 13.75% (decidida em 2026-09-16). Curva do pregão de 2026-10-20; Focus de 2026-10-09. A curva é preço, com prêmio de prazo; a Focus é a mediana da pesquisa. A diferença mistura prêmio e discordância.

| Reunião | Rótulo Focus | Focus (mediana) | Curva DI | Curva − Focus (p.b.) |
|---|---|---|---|---|
| 2026-11-04 | R7/2026 | 13.50 | 13.59 | +9 |
| 2026-12-09 | R8/2026 | 13.25 | 13.45 | +20 |
| 2027-01-27 | R1/2027 | 13.25 | 13.27 | +2 |
| 2027-03-17 | R2/2027 | 13.00 | 13.07 | +7 |
| 2027-04-28 | R3/2027 | 12.75 | 12.87 | +12 |
| 2027-06-16 | R4/2027 | 12.62 | 12.66 | +4 |
| 2027-08-04 | R5/2027 | 12.50 | 12.48 | -2 |
| 2027-09-22 | R6/2027 | 12.25 | 12.37 | +12 |
| 2027-10-27 | R7/2027 | 12.00 | 12.33 | +33 |
| 2027-12-08 | R8/2027 | 12.00 | 12.35 | +35 |

### Juro real e inflação implícita

Focus IPCA 12 meses (suavizada) de 2026-10-09. Real = (1 + nominal)/(1 + inflação) − 1; nos títulos, o real é a própria NTN-B e a inflação implícita sai do DI contra ela no mesmo prazo (com prêmio de risco de inflação dentro).

| Medida | Data | Nominal (%) | Inflação (%) | Real (%) |
|---|---|---|---|---|
| Selic vigente | 2026-09-16 | 13.75 | 4.48 (Focus 12m) | 8.88 |
| DI e NTN-B, 1 ano | 2026-10-20 | 12.91 | 6.60 (implícita) | 5.92 |
| DI e NTN-B, 2 anos | 2026-10-20 | 12.59 | 5.39 (implícita) | 6.83 |
| DI e NTN-B, 5 anos | 2026-10-20 | 12.66 | 5.51 (implícita) | 6.78 |
| DI e NTN-B, 10 anos | 2026-10-20 | 12.75 | 5.50 (implícita) | 6.88 |

Juro real neutro no QPC da reunião 279 (2026-06-24), mediana, e a Selic real acima dele: 2a 6.00% (+2.88 p.p.); 5a 5.50% (+3.38 p.p.); curto prazo 6.40% (+2.48 p.p.).
