# F(A) — cambio — ciclo 2026-10-07

Gerado em 2026-10-07 14:01. Dados do banco até 2026-10-07, fixos durante o ciclo. Sem ciclo anterior.

Os dados brutos (A) estão em `A/`, um arquivo por tabela; as funções G leem de lá e o código delas fica em `G/`. Nada aqui é opinião: é a mesma conta em todo ciclo.

Como ler:
- **Δ% 1m/3m/12m**: variação contra o último valor de 1, 3 e 12 meses antes da última data da série.
- **Δ**: diferença na unidade da série (p.p. quando a série é %, p.b. quando é p.b.).
- **Pctl**: posição do último valor no histórico, de 0 (o menor já visto) a 100 (o maior). "10a" = últimos 10 anos.
- **Soma 3m/12m**: soma dos últimos 3 e 12 meses completos; o mês em curso aparece à parte e não entra nas somas.
- **Acum.**: variação composta.

## i. Endógeno (leitura completa)

### cmb_ptax

Último dado 2026-10-06 (1 dia antes do corte) · A: `A/cmb_ptax.csv.gz`

| Série | Unidade | Data | Último | Δ% 1m | Δ% 3m | Δ% 12m | Pctl 10a | Pctl hist. | Pctl Δ12m hist. | Mín–máx 10a |
|---|---|---|---|---|---|---|---|---|---|---|
| PTAX venda | R$/US$ | 2026-10-06 | 4.9698 | -3.0 | -3.8 | -6.6 | 43 | 82 | 23 | 3.0510 a 6.2086 |

| Série | Unidade | Data | Média 1m | Média 3m | Média 12m | Pctl média 1m 10a |
|---|---|---|---|---|---|---|
| Volume interbancário D+1 | US$ mi/dia | 2026-10-06 | 331 | 266 | 381 | 68 |
| Volume interbancário D+2 | US$ mi/dia | 2026-10-06 | 1240 | 980 | 1567 | 45 |

### cmb_cambio_contratado

Último dado 2026-09-25 (12 dias antes do corte) · A: `A/cmb_cambio_contratado.csv.gz`

| Série | Unidade | Último mês | Soma 3m | Soma 12m | Soma 12m, um ano antes | Mês em curso | Pctl soma 12m hist. |
|---|---|---|---|---|---|---|---|
| Saldo total (comercial + financeiro) | US$ bi | -3.90 (2026-08) | 1.92 | 1.00 | -46.46 | -4.02 (até 25/09) | 53 |
| Comercial, saldo | US$ bi | 5.18 (2026-08) | 19.33 | 56.58 | 46.44 | 0.60 (até 25/09) | 91 |
| Comercial, exportação | US$ bi | 26.87 (2026-08) | 86.06 | 305.54 | 285.89 | 21.10 (até 25/09) | 100 |
| Comercial, importação | US$ bi | 21.69 (2026-08) | 66.73 | 248.96 | 239.45 | 20.50 (até 25/09) | 100 |
| Financeiro, saldo | US$ bi | -9.09 (2026-08) | -17.41 | -55.58 | -92.90 | -4.62 (até 25/09) | 24 |
| Financeiro, compras | US$ bi | 48.38 (2026-08) | 160.80 | 679.45 | 574.46 | 53.97 (até 25/09) | 100 |
| Financeiro, vendas | US$ bi | 57.47 (2026-08) | 178.21 | 735.04 | 667.36 | 58.59 (até 25/09) | 100 |
| Financeiro: serviços (mensal) | US$ bi | -2.72 (2026-08) | -7.78 | -28.22 | -31.83 |  | 69 |
| Financeiro: rendas (mensal) | US$ bi | -3.31 (2026-08) | -11.34 | -67.00 | -54.64 |  | 5 |
| Financeiro: capitais brasileiros (mensal) | US$ bi | -2.03 (2026-08) | -7.89 | -47.69 | -39.63 |  | 3 |
| Financeiro: capitais estrangeiros (mensal) | US$ bi | -1.03 (2026-08) | 9.61 | 87.32 | 33.20 |  | 72 |

### cmb_balanco_pagmt

Último dado 2026-08-01 (67 dias antes do corte) · A: `A/cmb_balanco_pagmt.csv.gz`

| Série | Unidade | Último mês | Soma 3m | Soma 12m | Soma 12m, um ano antes | 12m % PIB | Pctl soma 12m hist. |
|---|---|---|---|---|---|---|---|
| Transações correntes | US$ bi | -5.05 (2026-08) | -18.06 | -63.04 | -76.92 | -2.47 | 24 |
| Exportação de bens | US$ bi | 33.28 (2026-08) | 102.76 | 373.31 | 340.32 |  | 100 |
| Importação de bens | US$ bi | 26.66 (2026-08) | 82.42 | 302.72 | 284.61 |  | 100 |
| Serviços, saldo | US$ bi | -5.25 (2026-08) | -15.97 | -55.77 | -54.81 |  | 5 |
| Renda primária, saldo | US$ bi | -6.95 (2026-08) | -23.73 | -83.92 | -82.49 |  | 0 |
| Conta financeira (concessões − captações líquidas) | US$ bi | -6.05 (2026-08) | -20.32 | -65.84 | -79.26 |  | 24 |
| Investimento direto no país (passivos) | US$ bi | 7.40 (2026-08) | 23.51 | 86.56 | 79.28 | 3.39 | 91 |
| Carteira, passivos | US$ bi | -5.32 (2026-08) | -4.22 | 24.42 | 5.76 | 0.96 | 75 |
| Carteira: ações, passivos | US$ bi | -5.56 (2026-08) | -6.66 | -4.22 | -7.06 |  | 13 |
| Carteira: títulos no mercado doméstico, passivos | US$ bi | 1.30 (2026-08) | 2.17 | 17.17 | 15.93 |  | 80 |
| Outros investimentos, passivos | US$ bi | 1.61 (2026-08) | 9.55 | 29.44 | 15.88 |  | 85 |
| Ativos de reserva | US$ bi | 0.43 (2026-08) | 4.42 | 19.37 | -27.44 |  | 80 |
| Erros e omissões | US$ bi | -1.05 (2026-08) | -2.32 | -2.57 | -2.17 |  | 18 |

### cmb_comex_fator_agregado

Último dado 2026-08-01 (67 dias antes do corte) · A: `A/cmb_comex_fator_agregado.csv.gz`

| Série | Unidade | Último mês | Soma 3m | Soma 12m | Soma 12m, um ano antes | Pctl soma 12m hist. |
|---|---|---|---|---|---|---|
| Básicos, exportação | US$ bi | 19.75 (2026-08) | 61.85 | 222.48 | 192.15 | 100 |
| Básicos, importação | US$ bi | 1.84 (2026-08) | 5.89 | 21.23 | 21.96 | 63 |
| Semimanufaturados, exportação | US$ bi | 4.21 (2026-08) | 13.14 | 47.76 | 45.83 | 100 |
| Semimanufaturados, importação | US$ bi | 1.08 (2026-08) | 3.74 | 13.12 | 11.97 | 95 |
| Manufaturados, exportação | US$ bi | 9.18 (2026-08) | 27.32 | 101.29 | 99.83 | 100 |
| Manufaturados, importação | US$ bi | 22.82 (2026-08) | 69.74 | 256.98 | 240.17 | 100 |
| Demais, exportação | US$ bi | 0.02 (2026-08) | 0.06 | 0.20 | 0.10 | 24 |
| Demais, importação | US$ bi | 0.02 (2026-08) | 0.05 | 0.17 | 0.10 | 100 |

### cmb_comex_pais

Último dado 2026-08-01 (67 dias antes do corte) · A: `A/cmb_comex_pais.csv.gz`

| Série | Unidade | Último mês | Soma 3m | Soma 12m | Soma 12m, um ano antes | Pctl soma 12m hist. |
|---|---|---|---|---|---|---|
| Mundo, exportação | US$ bi | 33.16 (2026-08) | 102.37 | 371.73 | 337.92 | 100 |
| Mundo, importação | US$ bi | 25.76 (2026-08) | 79.42 | 291.50 | 274.21 | 100 |
| China, exportação | US$ bi | 8.34 (2026-08) | 31.03 | 109.97 | 92.42 | 99 |
| China, importação | US$ bi | 6.61 (2026-08) | 20.82 | 75.40 | 70.19 | 100 |
| EUA, exportação | US$ bi | 3.19 (2026-08) | 10.20 | 35.08 | 40.93 | 86 |
| EUA, importação | US$ bi | 4.01 (2026-08) | 11.79 | 42.57 | 43.65 | 91 |
| Argentina, exportação | US$ bi | 1.48 (2026-08) | 4.21 | 15.94 | 17.97 | 70 |
| Argentina, importação | US$ bi | 1.10 (2026-08) | 3.53 | 13.29 | 13.43 | 78 |
| Alemanha, exportação | US$ bi | 0.59 (2026-08) | 1.67 | 7.15 | 6.30 | 85 |
| Alemanha, importação | US$ bi | 1.41 (2026-08) | 4.27 | 14.97 | 14.01 | 95 |

### cmb_comex_produto

Último dado 2026-08-01 (67 dias antes do corte) · A: `A/cmb_comex_produto.csv.gz`

| Série | Unidade | Último mês | Soma 3m | Soma 12m | Soma 12m, um ano antes | Pctl soma 12m hist. |
|---|---|---|---|---|---|---|
| Mundo, exportação | US$ bi | 33.16 (2026-08) | 102.37 | 371.73 | 337.92 | 100 |
| Mundo, importação | US$ bi | 25.76 (2026-08) | 79.42 | 291.50 | 274.21 | 100 |
| Petróleo, exportação | US$ bi | 4.83 (2026-08) | 15.29 | 51.62 | 43.22 | 100 |
| Petróleo, importação | US$ bi | 0.55 (2026-08) | 2.05 | 6.59 | 7.31 | 48 |
| Soja, exportação | US$ bi | 4.41 (2026-08) | 16.55 | 48.73 | 40.81 | 97 |
| Soja, importação | US$ bi | 0.04 (2026-08) | 0.09 | 0.39 | 0.23 | 96 |
| Minério de ferro, exportação | US$ bi | 2.35 (2026-08) | 7.60 | 29.13 | 27.24 | 75 |
| Minério de ferro, importação | US$ bi | 0.01 (2026-08) | 0.01 | 0.01 | 0.00 | 82 |
| Carnes, exportação | US$ bi | 2.51 (2026-08) | 8.40 | 33.76 | 27.40 | 100 |
| Carnes, importação | US$ bi | 0.03 (2026-08) | 0.09 | 0.35 | 0.37 | 73 |
| Café, exportação | US$ bi | 1.10 (2026-08) | 2.86 | 13.67 | 13.92 | 96 |
| Café, importação | US$ bi | 0.01 (2026-08) | 0.03 | 0.11 | 0.11 | 92 |

### cmb_reservas_bc

Último dado 2026-10-06 (1 dia antes do corte) · A: `A/cmb_reservas_bc.csv.gz`

| Série | Unidade | Data | Último | Δ 1m | Δ 3m | Δ 12m | Pctl 10a | Pctl hist. | Mín–máx 10a |
|---|---|---|---|---|---|---|---|---|---|
| Reservas internacionais | US$ bi | 2026-10-06 | 363.2 | -9.7 | -7.3 | +5.8 | 55 | 72 | 323.5 a 390.5 |
| Reservas, conceito liquidez | US$ bi | 2026-10-06 | 367.2 | -7.7 | -5.3 | -1.5 | 51 | 50 | 327.4 a 401.6 |
| Swap cambial do BC, posição (− = vendido) | US$ bi | 2026-08-01 | -91.6 | +1.3 | +3.2 | +9.8 | 46 | 34 | -102.7 a -17.8 |
| Posição à vista dos bancos | US$ bi | 2026-08-01 | -22.1 | -2.7 | +4.8 | +5.8 | 40 | 15 | -42.4 a 4.6 |

| Série | Unidade | Último mês | Soma 3m | Soma 12m | Soma 12m, um ano antes | Mês em curso | Pctl soma 12m hist. |
|---|---|---|---|---|---|---|---|
| Intervenção à vista (+ compra, − venda) | US$ bi | -2.00 (2026-09) | -3.00 | -8.00 | -22.57 | 0.00 (até 06/10) | 14 |
| Leilões de linha (+ compra, − venda) | US$ bi | -1.00 (2026-09) | 1.05 | 8.25 | -11.25 | 0.00 (até 06/10) | 94 |

### cmb_cot_fx

Último dado 2026-09-22 (15 dias antes do corte) · A: `A/cmb_cot_fx.csv.gz`

| Série | Unidade | Data | Último | Δ 1m | Δ 3m | Δ 12m | Pctl 10a | Pctl hist. | Mín–máx 10a |
|---|---|---|---|---|---|---|---|---|---|
| BRL: fundos alavancados, líquido | contratos | 2026-09-22 | 14917 | +949 | +9496 | -1914 | 91 | 92 | -40335 a 32847 |
| BRL: asset managers, líquido | contratos | 2026-09-22 | 59481 | +8052 | +3504 | -13514 | 93 | 95 | -57523 a 78334 |
| BRL: dealers, líquido | contratos | 2026-09-22 | -52093 | +1622 | +14756 | +6731 | 10 | 7 | -83394 a 59543 |
| BRL: outros reportáveis, líquido | contratos | 2026-09-22 | -26780 | -11294 | -28721 | +7752 | 3 | 2 | -48451 a 12141 |
| BRL: não reportáveis, líquido | contratos | 2026-09-22 | 4475 | +671 | +965 | +945 | 98 | 99 | -5527 a 14033 |
| BRL: posições em aberto | contratos | 2026-09-22 | 117063 | +3655 | +10575 | -3151 | 94 | 96 | 10333 a 152424 |
| MXN: fundos alavancados, líquido | contratos | 2026-09-22 | 79188 | +13858 | +29914 | +43362 | 97 | 93 | -96547 a 114016 |
| MXN: asset managers, líquido | contratos | 2026-09-22 | 45506 | -16646 | +1537 | +5268 | 22 | 44 | -18603 a 176493 |
| MXN: dealers, líquido | contratos | 2026-09-22 | -74696 | +34294 | -78 | +8266 | 56 | 42 | -234567 a 48410 |
| MXN: outros reportáveis, líquido | contratos | 2026-09-22 | -54451 | -30826 | -30325 | -56601 | 15 | 10 | -111774 a 6128 |
| MXN: não reportáveis, líquido | contratos | 2026-09-22 | 4453 | -680 | -1048 | -295 | 69 | 69 | -10152 a 13919 |
| MXN: posições em aberto | contratos | 2026-09-22 | 266061 | -18530 | -10889 | +83943 | 89 | 93 | 94469 a 376712 |

### cmb_reer

Último dado 2026-08-01 (67 dias antes do corte) · A: `A/cmb_reer.csv.gz`

| Série | Unidade | Data | Último | Δ% 1m | Δ% 3m | Δ% 12m | Pctl 10a | Pctl hist. | Pctl Δ12m hist. | Mín–máx 10a |
|---|---|---|---|---|---|---|---|---|---|---|
| BR, real efetivo | índice 2020=100 | 2026-08-01 | 116.46 | -2.0 | -3.4 | +5.5 | 50 | 35 | 63 | 90.32 a 151.33 |
| BR, nominal efetivo | índice 2020=100 | 2026-08-01 | 113.18 | -1.4 | -2.7 | +4.9 | 51 | 19 | 70 | 88.28 a 146.37 |
| MX, real efetivo | índice 2020=100 | 2026-08-01 | 141.98 | +1.6 | +1.1 | +9.2 | 98 | 81 | 80 | 88.88 a 144.59 |
| MX, nominal efetivo | índice 2020=100 | 2026-08-01 | 128.99 | +1.7 | +1.4 | +8.7 | 92 | 31 | 90 | 89.71 a 134.70 |
| CL, real efetivo | índice 2020=100 | 2026-08-01 | 102.21 | +0.9 | -2.0 | +3.7 | 40 | 16 | 70 | 92.25 a 117.27 |
| CL, nominal efetivo | índice 2020=100 | 2026-08-01 | 94.68 | +0.6 | -2.1 | +2.9 | 16 | 5 | 66 | 87.75 a 117.49 |
| CO, real efetivo | índice 2020=100 | 2026-08-01 | 147.03 | +3.7 | +19.4 | +30.3 | 100 | 99 | 100 | 83.28 a 147.03 |
| CO, nominal efetivo | índice 2020=100 | 2026-08-01 | 123.18 | +3.6 | +18.8 | +26.4 | 100 | 41 | 100 | 79.19 a 123.18 |

### cmb_termos_troca

Último dado 2026-07-01 (98 dias antes do corte) · A: `A/cmb_termos_troca.csv.gz`

| Série | Unidade | Data | Último | Δ% 1m | Δ% 3m | Δ% 12m | Pctl 10a | Pctl hist. | Pctl Δ12m hist. | Mín–máx 10a |
|---|---|---|---|---|---|---|---|---|---|---|
| Termos de troca (Funcex) | índice | 2026-07-01 | 111.35 | -1.8 | -2.7 | +1.5 | 75 | 90 | 58 | 93.15 a 122.43 |

### cmb_fx_latam

Último dado 2026-09-29 (8 dias antes do corte) · A: `A/cmb_fx_latam.csv.gz`

| Série | Unidade | Data | Último | Δ% 1m | Δ% 3m | Δ% 12m | Pctl 10a | Pctl hist. | Pctl Δ12m hist. | Mín–máx 10a |
|---|---|---|---|---|---|---|---|---|---|---|
| Peso mexicano | MXN/US$ | 2026-09-29 | 17.8971 | +5.6 | +2.4 | -2.4 | 19 | 68 | 35 | 16.3125 a 25.1039 |
| Peso chileno | CLP/US$ | 2026-09-29 | 969.70 | +4.8 | +5.8 | +1.1 | 95 | 98 | 50 | 588.28 a 1042.97 |
| Peso colombiano | COP/US$ | 2026-09-23 | 3208.66 | +4.8 | -5.8 | -16.7 | 27 | 72 | 3 | 2705.34 a 5061.21 |
| Sol peruano | PEN/US$ | 2026-09-25 | 3.4205 | +2.3 | +0.3 | -2.4 | 43 | 60 | 46 | 3.2070 a 4.1340 |

### diferenciais_juros

Último dado 2026-09-01 (36 dias antes do corte) · A: `A/diferenciais_juros.csv.gz`

| Série | Unidade | Data | Último | Δ 1m | Δ 3m | Δ 12m | Pctl 10a | Pctl hist. | Mín–máx 10a |
|---|---|---|---|---|---|---|---|---|---|
| Selic | % a.a. | 2026-09-01 | 13.75 | -0.25 | -0.50 | -1.25 | 83 | 62 | 2.00 a 15.00 |
| Fed Funds | % a.a. | 2026-08-01 | 3.63 | +0.00 | +0.00 | -0.70 | 65 | 61 | 0.05 a 5.33 |
| Diferencial nominal (Selic − Fed Funds) | p.p. | 2026-08-01 | 10.37 | -0.25 | -0.50 | -0.30 | 74 | 48 | 1.90 a 13.85 |
| IPCA 12m | % | 2026-08-01 | 4.22 | -0.22 | -0.50 | -0.91 | 37 | 21 | 1.88 a 12.13 |
| CPI EUA 12m | % | 2026-08-01 | 3.35 | +0.05 | -0.81 | +0.41 | 72 | 80 | 0.20 a 8.98 |
| Juro real ex-post Brasil | % a.a. | 2026-08-01 | 9.78 | -0.03 | +0.00 | -0.09 | 90 | 74 | -4.74 a 11.19 |
| Juro real ex-post EUA | % a.a. | 2026-08-01 | 0.28 | -0.05 | +0.81 | -1.11 | 63 | 57 | -8.37 a 2.72 |
| Diferencial real ex-post | p.p. | 2026-08-01 | 9.50 | +0.02 | -0.81 | +1.02 | 87 | 74 | -1.61 a 12.21 |

## ii. Endógeno de política monetária (leitura enxuta)

### pm_copom_calendario

Último dado 2027-12-08 (data no futuro) · A: `A/pm_copom_calendario.csv.gz`

O calendário oficial vai até 2027-12-08.

| Reunião | Decisão | Dias a partir do corte |
|---|---|---|
| última | 2026-09-16 | -21 |
| próxima 1 | 2026-11-04 | 28 |
| próxima 2 | 2026-12-09 | 63 |
| próxima 3 | 2027-01-27 | 112 |
| próxima 4 | 2027-03-17 | 161 |

### pm_copom_reuniao

Último dado 2026-09-16 (21 dias antes do corte) · A: `A/pm_copom_reuniao.csv.gz`

| Reunião | Decisão | Selic decidida (% a.a.) | Passo (p.b.) |
|---|---|---|---|
| 281 | 2026-09-16 | 13.75 | -25 |
| 280 | 2026-08-05 | 14.00 | -25 |
| 279 | 2026-06-17 | 14.25 | -25 |
| 278 | 2026-04-29 | 14.50 | -25 |
| 277 | 2026-03-18 | 14.75 | -25 |
| 276 | 2026-01-28 | 15.00 | +0 |

### pm_copom_projecoes

Último dado 2026-09-24 (13 dias antes do corte) · A: `A/pm_copom_projecoes.csv.gz`

Reunião 281 (de 2026-09-24), Relatório de Política Monetária. Valor = IPCA acumulado em quatro trimestres.

| Período | IPCA 4 trimestres (%) |  |
|---|---|---|
| 3T26 | 4.4 |  |
| 4T26 | 5.2 |  |
| 1T27 | 4.9 |  |
| 2T27 | 4.5 |  |
| 3T27 | 4.5 |  |
| 4T27 | 3.9 |  |
| 1T28 | 3.2 | horizonte relevante |
| 2T28 | 3.1 |  |
| 3T28 | 3.1 |  |
| 4T28 | 3.1 |  |
| 1T29 | 3.1 |  |

Na reunião anterior (280), o horizonte relevante (1T28) estava em 3.2%.

### br_di_grade

Último dado 2026-10-06 (1 dia antes do corte) · A: `A/br_di_grade.csv.gz`

Pregão de 2026-10-06. DI × pré, base 252, nos prazos redondos.

| Prazo | Taxa (% a.a.) | Δ 1m (p.b.) | Δ 3m (p.b.) | Δ 12m (p.b.) |
|---|---|---|---|---|
| 1 mês | 13.62 | -13 | -52 | -128 |
| 3 meses | 13.41 | -21 | -61 | -149 |
| 6 meses | 13.17 | -35 | -82 | -166 |
| 1 ano | 12.77 | -78 | -128 | -156 |
| 2 anos | 12.46 | -132 | -165 | -112 |
| 3 anos | 12.51 | -148 | -175 | -87 |
| 5 anos | 12.63 | -152 | -170 | -91 |
| 10 anos | 12.74 | -149 | -155 | -89 |

Selic precificada na curva em cada reunião (meta vigente 13.75%). É preço, com prêmio de prazo, não previsão. Reuniões só até onde vai o calendário oficial (2027-12-08).

| Reunião | Selic na curva (% a.a.) | Passo implícito (p.b.) | 1 mês antes (2026-09-04) | Δ 1 mês (p.b.) |
|---|---|---|---|---|
| 2026-11-04 | 13.50 | -25 | 13.59 | -9 |
| 2026-12-09 | 13.26 | -24 | 13.51 | -25 |
| 2027-01-27 | 13.04 | -22 | 13.53 | -48 |
| 2027-03-17 | 12.83 | -21 | 13.57 | -74 |
| 2027-04-28 | 12.62 | -21 | 13.63 | -100 |
| 2027-06-16 | 12.42 | -20 | 13.69 | -126 |
| 2027-08-04 | 12.27 | -16 | 13.75 | -148 |
| 2027-09-22 | 12.18 | -9 | 13.84 | -166 |
| 2027-10-27 | 12.16 | -2 | 13.95 | -179 |
| 2027-12-08 | 12.20 | +4 | 14.10 | -189 |

### inflc_meta

Último dado 2026-01-01 (279 dias antes do corte) · A: `A/inflc_meta.csv.gz`

| Ano | Meta (%) |
|---|---|
| 2024 | 3.00 |
| 2025 | 3.00 |
| 2026 | 3.00 |

## iii. TWA — expectativas (leitura enxuta)

### expc_focus_periodo (câmbio)

Último dado 2026-09-25 (12 dias antes do corte) · A: `A/expc_focus_periodo__cambio.csv.gz`

Unidade: R$/US$. Mediana da pesquisa (janela de 30 dias).

| Ano | Mediana (2026-09-25) | 4 sem. antes (2026-08-28) | 13 sem. antes (2026-06-26) | Δ 4 sem. | Respondentes |
|---|---|---|---|---|---|
| 2026 | 5.20 | 5.20 | 5.20 | +0.00 | 110 |
| 2027 | 5.28 | 5.30 | 5.28 | -0.02 | 110 |
| 2028 | 5.30 | 5.30 | 5.35 | +0.00 | 84 |
| 2029 | 5.35 | 5.36 | 5.40 | -0.01 | 79 |

### expc_focus_copom

Último dado 2026-09-25 (12 dias antes do corte) · A: `A/expc_focus_copom.csv.gz`

Selic vigente na data da pesquisa: 13.75% (decidida em 2026-09-16). Mediana da pesquisa (janela de 30 dias), % a.a.

| Reunião | Data | Mediana (2026-09-25) | 4 sem. antes (2026-08-28) | Δ 4 sem. (p.p.) | Mín–máx |
|---|---|---|---|---|---|
| R7/2026 | 2026-11-04 | 13.50 | 13.75 | -0.25 | 13.50 a 14.00 |
| R8/2026 | 2026-12-09 | 13.50 | 13.75 | -0.25 | 13.00 a 14.00 |
| R1/2027 | 2027-01-27 | 13.50 | 13.75 | -0.25 | 12.50 a 14.00 |
| R2/2027 | 2027-03-17 | 13.25 | 13.50 | -0.25 | 12.00 a 14.00 |
| R3/2027 | 2027-04-28 | 13.00 | 13.25 | -0.25 | 11.50 a 14.00 |
| R4/2027 | 2027-06-16 | 13.00 | 13.00 | +0.00 | 11.00 a 14.00 |
| R5/2027 | 2027-08-04 | 12.50 | 12.75 | -0.25 | 10.25 a 14.00 |
| R6/2027 | 2027-09-22 | 12.50 | 12.50 | +0.00 | 9.75 a 14.00 |

### expc_focus_periodo (Selic)

Último dado 2026-09-25 (12 dias antes do corte) · A: `A/expc_focus_periodo__selic.csv.gz`

Unidade: %. Mediana da pesquisa (janela de 30 dias).

| Ano | Mediana (2026-09-25) | 4 sem. antes (2026-08-28) | 13 sem. antes (2026-06-26) | Δ 4 sem. | Respondentes |
|---|---|---|---|---|---|
| 2026 | 13.50 | 13.75 | 14.00 | -0.25 | 138 |
| 2027 | 12.00 | 12.00 | 12.00 | +0.00 | 137 |
| 2028 | 10.50 | 10.50 | 10.50 | +0.00 | 114 |
| 2029 | 10.00 | 10.00 | 10.00 | +0.00 | 107 |

### expc_focus_periodo (IPCA)

Último dado 2026-09-25 (12 dias antes do corte) · A: `A/expc_focus_periodo__ipca.csv.gz`

Unidade: %. Mediana da pesquisa (janela de 30 dias).

| Ano | Mediana (2026-09-25) | 4 sem. antes (2026-08-28) | 13 sem. antes (2026-06-26) | Δ 4 sem. | Respondentes |
|---|---|---|---|---|---|
| 2026 | 4.99 | 5.01 | 5.33 | -0.01 | 144 |
| 2027 | 4.31 | 4.28 | 4.17 | +0.03 | 144 |
| 2028 | 3.80 | 3.80 | 3.70 | +0.00 | 117 |
| 2029 | 3.50 | 3.50 | 3.50 | +0.00 | 110 |

## iv. TWA — externo (leitura enxuta)

### cmb_dollar_index

Último dado 2026-10-07 (no corte) · A: `A/cmb_dollar_index.csv.gz`

| Série | Unidade | Data | Último | Δ% 1m | Δ% 3m | Δ% 12m |
|---|---|---|---|---|---|---|
| DXY | índice | 2026-10-07 | 102.31 | +3.2 | +1.2 | +3.8 |

### cmb_dollar_index_em

Último dado 2026-10-02 (5 dias antes do corte) · A: `A/cmb_dollar_index_em.csv.gz`

| Série | Unidade | Data | Último | Δ% 1m | Δ% 3m | Δ% 12m |
|---|---|---|---|---|---|---|
| Dólar contra emergentes (FRED) | índice | 2026-10-02 | 129.71 | +2.4 | +0.2 | -1.5 |

### cmb_equity_us

Último dado 2026-10-07 (no corte) · A: `A/cmb_equity_us.csv.gz`

| Série | Unidade | Data | Último | Δ% 1m | Δ% 3m | Δ% 12m |
|---|---|---|---|---|---|---|
| S&P 500 | pontos | 2026-10-07 | 7769 | +0.7 | +3.5 | +15.7 |

### us_interest_rate

Último dado 2026-10-07 (no corte) · A: `A/us_interest_rate.csv.gz`

| Série | Unidade | Data | Último | Δ 1m | Δ 3m | Δ 12m |
|---|---|---|---|---|---|---|
| Fed Funds, meta (ponto médio) | % a.a. | 2026-10-07 | 3.88 | +0.25 | +0.25 | -0.25 |
| Treasury 2 anos | % a.a. | 2026-10-05 | 4.84 | +0.47 | +0.70 | +1.26 |
| Treasury 10 anos | % a.a. | 2026-10-05 | 5.31 | +0.53 | +0.82 | +1.18 |

### cmb_real_rates

Último dado 2026-06-01 (128 dias antes do corte) · A: `A/cmb_real_rates.csv.gz`

| Série | Unidade | Data | Último | Δ 1m | Δ 3m | Δ 12m |
|---|---|---|---|---|---|---|
| BR, juro real ex-post | % a.a. | 2026-06-01 | 9.61 | -0.17 | -1.00 | -0.04 |
| MX, juro real ex-post | % a.a. | 2026-06-01 | 3.13 | +0.57 | +0.97 | -0.55 |
| CL, juro real ex-post | % a.a. | 2026-06-01 | 0.16 | -0.41 | -1.50 | -0.72 |
| CO, juro real ex-post | % a.a. | 2026-06-01 | 5.11 | -0.30 | +0.42 | +0.68 |
| PE, juro real ex-post | % a.a. | 2026-06-01 | 0.24 | -0.10 | -0.20 | -2.57 |

### comm_brent

Último dado 2026-09-29 (8 dias antes do corte) · A: `A/comm_brent.csv.gz`

| Série | Unidade | Data | Último | Δ% 1m | Δ% 3m | Δ% 12m |
|---|---|---|---|---|---|---|
| Brent | US$/barril | 2026-09-29 | 113.96 | +27.0 | +59.2 | +65.2 |

### comm_icbr_usd

Último dado 2026-08-01 (67 dias antes do corte) · A: `A/comm_icbr_usd.csv.gz`

| Série | Unidade | Data | Último | Δ% 1m | Δ% 3m | Δ% 12m |
|---|---|---|---|---|---|---|
| IC-Br em dólar | índice | 2026-08-01 | 202.35 | +2.8 | -2.6 | +12.6 |
| IC-Br agropecuária | índice | 2026-08-01 | 201.19 | +1.3 | +0.2 | +1.0 |
| IC-Br metal | índice | 2026-08-01 | 337.08 | +5.9 | -3.9 | +49.2 |
| IC-Br energia | índice | 2026-08-01 | 86.80 | +3.3 | -11.7 | +18.4 |

## v. TWA — doméstico (leitura enxuta)

### inflc_agregados

Último dado 2026-09-01 (36 dias antes do corte) · A: `A/inflc_agregados.csv.gz`

| Série | Mês | Último mês | Acum. 3m | Acum. 12m | Acum. 12m, 3 meses antes |
|---|---|---|---|---|---|
| IPCA | 2026-08 | -0.32 | -0.09 | 4.22 | 4.72 |
| Livres | 2026-08 | 0.01 | 0.11 | 4.11 | 4.31 |
| Administrados | 2026-08 | -1.25 | -0.70 | 4.42 | 5.85 |
| Comercializáveis | 2026-08 | 0.38 | -0.00 | 2.52 | 2.29 |
| Não comercializáveis | 2026-08 | -0.24 | 0.21 | 5.30 | 5.82 |
| Serviços | 2026-08 | 0.03 | 0.90 | 5.46 | 5.97 |
| Industriais | 2026-08 | 0.43 | 0.44 | 2.95 | 2.69 |

### fisc_nfsp

Último dado 2026-08-01 (67 dias antes do corte) · A: `A/fisc_nfsp.csv.gz`

| Série | Unidade | Data | Último | Δ 1m | Δ 3m | Δ 12m |
|---|---|---|---|---|---|---|
| Resultado primário, 12m (+ = superávit) | % do PIB | 2026-08-01 | -0.62 | +0.05 | +0.52 | -0.43 |
| Resultado nominal, 12m | % do PIB | 2026-08-01 | -9.48 | -0.13 | +0.13 | -1.69 |
| Juros nominais, 12m | % do PIB | 2026-08-01 | 8.86 | +0.18 | +0.38 | +1.25 |

### fisc_divida

Último dado 2026-08-01 (67 dias antes do corte) · A: `A/fisc_divida.csv.gz`

| Série | Unidade | Data | Último | Δ 1m | Δ 3m | Δ 12m |
|---|---|---|---|---|---|---|
| Dívida bruta do governo geral | % do PIB | 2026-08-01 | 82.9 | +0.3 | +1.8 | +5.5 |
| Dívida líquida do setor público | % do PIB | 2026-08-01 | 69.3 | +0.1 | +1.4 | +5.2 |

### atv_pib_usd

Último dado 2026-08-01 (67 dias antes do corte) · A: `A/atv_pib_usd.csv.gz`

| Série | Unidade | Último mês | Soma 3m | Soma 12m | Soma 12m, um ano antes |
|---|---|---|---|---|---|
| PIB mensal em dólar | US$ bi | 223.05 (2026-08) | 671.31 | 2553.86 | 2176.49 |

## vi. Exógeno (leitura enxuta)

### cmb_risco_pais

Último dado 2026-09-08 (29 dias antes do corte) · A: `A/cmb_risco_pais.csv.gz`

| Série | Unidade | Data | Último | Δ 1m | Δ 3m | Δ 12m |
|---|---|---|---|---|---|---|
| CDS 5 anos Brasil | p.b. | 2026-09-08 | 112 | -10 | -12 | -24 |

## Leituras combinadas

### O real e os pares

Moeda local por dólar: Δ% positivo = a moeda se desvalorizou. Volatilidade realizada em % ao ano. Juro de política dos pares pelo BIS (mensal, com defasagem: data ao lado); o do Brasil é a Selic vigente. Carry = juro de política menos a meta do Fed na mesma data.

| Moeda | Data | Δ% 1m | Δ% 3m | Δ% 12m | Vol. 21d | Vol. 63d | Pctl vol. 63d 10a | Juro de política | Carry vs Fed (p.p.) | Carry / vol. 63d |
|---|---|---|---|---|---|---|---|---|---|---|
| BRL | 2026-10-06 | -3.0 | -3.8 | -6.6 | 18.6 | 12.2 | 53 | 13.75 (2026-09-16) | 10.12 | 0.83 |
| MXN | 2026-09-29 | +5.6 | +2.4 | -2.4 | 6.4 | 5.8 | 1 | 6.50 (2026-06-01) | 2.88 | 0.49 |
| CLP | 2026-09-29 | +4.8 | +5.8 | +1.1 | 10.5 | 9.3 | 32 | 4.50 (2026-06-01) | 0.88 | 0.09 |
| COP | 2026-09-23 | +4.8 | -5.8 | -16.7 | 13.4 | 13.6 | 77 | 11.25 (2026-06-01) | 7.62 | 0.56 |
| PEN | 2026-09-25 | +2.3 | +0.3 | -2.4 | 5.6 | 4.4 | 36 | 4.25 (2026-06-01) | 0.62 | 0.14 |
