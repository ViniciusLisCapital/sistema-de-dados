# F(A) — cambio — ciclo 2026-10-15

Gerado em 2026-10-15 16:26. Dados do banco até 2026-10-15, fixos durante o ciclo. Ciclo anterior: 2026-10-07.

Os dados brutos (A) estão em `A/`, um arquivo por tabela; as funções G leem de lá e o código delas fica em `G/`. Nada aqui é opinião: é a mesma conta em todo ciclo.

Como ler:
- **Δ% 1m/3m/12m**: variação contra o último valor de 1, 3 e 12 meses antes da última data da série.
- **Δ**: diferença na unidade da série (p.p. quando a série é %, p.b. quando é p.b.).
- **Pctl**: posição do último valor no histórico, de 0 (o menor já visto) a 100 (o maior). "10a" = últimos 10 anos.
- **Soma 3m/12m**: soma dos últimos 3 e 12 meses completos; o mês em curso aparece à parte e não entra nas somas.
- **Acum.**: variação composta.
- **Desde o ciclo ant.**: contra o valor em 2026-10-07.

## i. Endógeno (leitura completa)

### cmb_ptax

Último dado 2026-10-14 (1 dia antes do corte) · A: `A/cmb_ptax.csv.gz`

| Série | Unidade | Data | Último | Δ% 1m | Δ% 3m | Δ% 12m | Δ% desde o ciclo ant. | Pctl 10a | Pctl hist. | Pctl Δ12m hist. | Mín–máx 10a |
|---|---|---|---|---|---|---|---|---|---|---|---|
| PTAX venda | R$/US$ | 2026-10-14 | 5.0441 | -2.4 | -0.6 | -8.3 | +1.0 | 48 | 84 | 26 | 3.0510 a 6.2086 |

| Série | Unidade | Data | Média 1m | Média 3m | Média 12m | Pctl média 1m 10a |
|---|---|---|---|---|---|---|
| Volume interbancário D+1 | US$ mi/dia | 2026-10-14 | 356 | 279 | 377 | 68 |
| Volume interbancário D+2 | US$ mi/dia | 2026-10-14 | 1233 | 1021 | 1550 | 44 |

### cmb_cambio_contratado

Último dado 2026-10-09 (6 dias antes do corte) · A: `A/cmb_cambio_contratado.csv.gz`

| Série | Unidade | Último mês | Soma 3m | Soma 12m | Soma 12m, um ano antes | Mês em curso | Soma desde o ciclo ant. | Pctl soma 12m hist. |
|---|---|---|---|---|---|---|---|---|
| Saldo total (comercial + financeiro) | US$ bi | -5.09 (2026-09) | -7.06 | -3.90 | -42.67 | 3.21 (até 09/10) | 1.22 | 41 |
| Comercial, saldo | US$ bi | 2.28 (2026-09) | 11.91 | 58.41 | 46.33 | -0.87 (até 09/10) | -0.32 | 93 |
| Comercial, exportação | US$ bi | 26.31 (2026-09) | 81.07 | 308.97 | 286.53 | 6.84 (até 09/10) | 1.61 | 100 |
| Comercial, importação | US$ bi | 24.03 (2026-09) | 69.16 | 250.57 | 240.20 | 7.71 (até 09/10) | 1.93 | 100 |
| Financeiro, saldo | US$ bi | -7.37 (2026-09) | -18.96 | -62.31 | -89.00 | 4.09 (até 09/10) | 1.54 | 18 |
| Financeiro, compras | US$ bi | 63.24 (2026-09) | 160.40 | 686.15 | 581.45 | 30.19 (até 09/10) | 8.76 | 100 |
| Financeiro, vendas | US$ bi | 70.62 (2026-09) | 179.36 | 748.46 | 670.44 | 26.10 (até 09/10) | 7.22 | 100 |
| Financeiro: serviços (mensal) | US$ bi | -2.72 (2026-08) | -7.78 | -28.22 | -31.83 |  |  | 69 |
| Financeiro: rendas (mensal) | US$ bi | -3.31 (2026-08) | -11.34 | -67.00 | -54.64 |  |  | 5 |
| Financeiro: capitais brasileiros (mensal) | US$ bi | -2.03 (2026-08) | -7.89 | -47.69 | -39.63 |  |  | 3 |
| Financeiro: capitais estrangeiros (mensal) | US$ bi | -1.03 (2026-08) | 9.61 | 87.32 | 33.20 |  |  | 72 |

### cmb_balanco_pagmt

Último dado 2026-08-01 (75 dias antes do corte) · A: `A/cmb_balanco_pagmt.csv.gz`

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

Último dado 2026-08-01 (75 dias antes do corte) · A: `A/cmb_comex_fator_agregado.csv.gz`

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

Último dado 2026-09-01 (44 dias antes do corte) · A: `A/cmb_comex_pais.csv.gz`

| Série | Unidade | Último mês | Soma 3m | Soma 12m | Soma 12m, um ano antes | Pctl soma 12m hist. |
|---|---|---|---|---|---|---|
| Mundo, exportação | US$ bi | 34.42 (2026-09) | 100.73 | 375.04 | 339.93 | 100 |
| Mundo, importação | US$ bi | 26.68 (2026-09) | 79.66 | 290.87 | 278.16 | 100 |
| China, exportação | US$ bi | 7.89 (2026-09) | 26.62 | 109.03 | 93.53 | 99 |
| China, importação | US$ bi | 7.06 (2026-09) | 20.09 | 76.19 | 70.69 | 100 |
| EUA, exportação | US$ bi | 3.52 (2026-09) | 10.14 | 35.77 | 40.36 | 87 |
| EUA, importação | US$ bi | 4.43 (2026-09) | 12.81 | 42.71 | 44.18 | 92 |
| Argentina, exportação | US$ bi | 1.36 (2026-09) | 4.24 | 15.48 | 18.33 | 67 |
| Argentina, importação | US$ bi | 1.31 (2026-09) | 3.56 | 13.36 | 13.40 | 79 |
| Alemanha, exportação | US$ bi | 0.62 (2026-09) | 1.70 | 7.24 | 6.25 | 86 |
| Alemanha, importação | US$ bi | 1.20 (2026-09) | 4.03 | 14.84 | 14.10 | 94 |

### cmb_comex_produto

Último dado 2026-08-01 (75 dias antes do corte) · A: `A/cmb_comex_produto.csv.gz`

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

Último dado 2026-10-14 (1 dia antes do corte) · A: `A/cmb_reservas_bc.csv.gz`

| Série | Unidade | Data | Último | Δ 1m | Δ 3m | Δ 12m | Δ desde o ciclo ant. | Pctl 10a | Pctl hist. | Mín–máx 10a |
|---|---|---|---|---|---|---|---|---|---|---|
| Reservas internacionais | US$ bi | 2026-10-14 | 362.6 | -6.5 | -7.1 | +4.0 | +0.1 | 54 | 71 | 323.5 a 390.5 |
| Reservas, conceito liquidez | US$ bi | 2026-10-14 | 366.6 | -4.5 | -5.1 | -3.3 | +0.1 | 50 | 49 | 327.4 a 401.6 |
| Swap cambial do BC, posição (− = vendido) | US$ bi | 2026-08-01 | -91.6 | +1.3 | +3.2 | +9.8 | sem dado novo | 46 | 34 | -102.7 a -17.8 |
| Posição à vista dos bancos | US$ bi | 2026-08-01 | -22.1 | -2.7 | +4.8 | +5.8 | sem dado novo | 40 | 15 | -42.4 a 4.6 |

| Série | Unidade | Último mês | Soma 3m | Soma 12m | Soma 12m, um ano antes | Mês em curso | Soma desde o ciclo ant. | Pctl soma 12m hist. |
|---|---|---|---|---|---|---|---|---|
| Intervenção à vista (+ compra, − venda) | US$ bi | -2.00 (2026-09) | -3.00 | -8.00 | -22.57 | 0.00 (até 14/10) | 0.00 | 14 |
| Leilões de linha (+ compra, − venda) | US$ bi | -2.00 (2026-09) | 0.05 | 7.25 | -11.25 | 0.00 (até 14/10) | 0.00 | 92 |

### cmb_cot_fx

Último dado 2026-10-06 (9 dias antes do corte) · A: `A/cmb_cot_fx.csv.gz`

| Série | Unidade | Data | Último | Δ 1m | Δ 3m | Δ 12m | Δ desde o ciclo ant. | Pctl 10a | Pctl hist. | Mín–máx 10a |
|---|---|---|---|---|---|---|---|---|---|---|
| BRL: fundos alavancados, líquido | contratos | 2026-10-06 | 27396 | +11350 | +19670 | +5047 | sem dado novo | 99 | 100 | -40335 a 32847 |
| BRL: asset managers, líquido | contratos | 2026-10-06 | 56610 | +7876 | +10534 | -667 | sem dado novo | 89 | 93 | -57523 a 78334 |
| BRL: dealers, líquido | contratos | 2026-10-06 | -63683 | -19843 | -2895 | -18916 | sem dado novo | 4 | 3 | -83394 a 59543 |
| BRL: outros reportáveis, líquido | contratos | 2026-10-06 | -24795 | +3050 | -28022 | +13302 | sem dado novo | 4 | 3 | -48451 a 12141 |
| BRL: não reportáveis, líquido | contratos | 2026-10-06 | 4472 | -2433 | +713 | +1234 | sem dado novo | 98 | 99 | -5527 a 14033 |
| BRL: posições em aberto | contratos | 2026-10-06 | 134541 | +7268 | +19551 | -5869 | sem dado novo | 98 | 99 | 10333 a 152424 |
| MXN: fundos alavancados, líquido | contratos | 2026-10-06 | 74927 | +565 | +19613 | +31553 | sem dado novo | 95 | 92 | -79304 a 114016 |
| MXN: asset managers, líquido | contratos | 2026-10-06 | -20599 | -88676 | -53098 | -77677 | sem dado novo | 0 | 0 | -20599 a 176493 |
| MXN: dealers, líquido | contratos | 2026-10-06 | 1221 | +125912 | +66311 | +106100 | sem dado novo | 93 | 82 | -234567 a 48410 |
| MXN: outros reportáveis, líquido | contratos | 2026-10-06 | -57549 | -35331 | -31193 | -57491 | sem dado novo | 14 | 9 | -111774 a 6128 |
| MXN: não reportáveis, líquido | contratos | 2026-10-06 | 2000 | -2470 | -1633 | -2485 | sem dado novo | 27 | 38 | -10152 a 13919 |
| MXN: posições em aberto | contratos | 2026-10-06 | 290507 | -22681 | +95101 | +107286 | sem dado novo | 94 | 96 | 94469 a 376712 |

### cmb_reer

Último dado 2026-08-01 (75 dias antes do corte) · A: `A/cmb_reer.csv.gz`

| Série | Unidade | Data | Último | Δ% 1m | Δ% 3m | Δ% 12m | Δ% desde o ciclo ant. | Pctl 10a | Pctl hist. | Pctl Δ12m hist. | Mín–máx 10a |
|---|---|---|---|---|---|---|---|---|---|---|---|
| BR, real efetivo | índice 2020=100 | 2026-08-01 | 116.46 | -2.0 | -3.4 | +5.5 | sem dado novo | 50 | 35 | 63 | 90.32 a 151.33 |
| BR, nominal efetivo | índice 2020=100 | 2026-08-01 | 113.18 | -1.4 | -2.7 | +4.9 | sem dado novo | 51 | 19 | 70 | 88.28 a 146.37 |
| MX, real efetivo | índice 2020=100 | 2026-08-01 | 141.98 | +1.6 | +1.1 | +9.2 | sem dado novo | 98 | 81 | 80 | 88.88 a 144.59 |
| MX, nominal efetivo | índice 2020=100 | 2026-08-01 | 128.99 | +1.7 | +1.4 | +8.7 | sem dado novo | 92 | 31 | 90 | 89.71 a 134.70 |
| CL, real efetivo | índice 2020=100 | 2026-08-01 | 102.21 | +0.9 | -2.0 | +3.7 | sem dado novo | 40 | 16 | 70 | 92.25 a 117.27 |
| CL, nominal efetivo | índice 2020=100 | 2026-08-01 | 94.68 | +0.6 | -2.1 | +2.9 | sem dado novo | 16 | 5 | 66 | 87.75 a 117.49 |
| CO, real efetivo | índice 2020=100 | 2026-08-01 | 147.03 | +3.7 | +19.4 | +30.3 | sem dado novo | 100 | 99 | 100 | 83.28 a 147.03 |
| CO, nominal efetivo | índice 2020=100 | 2026-08-01 | 123.18 | +3.6 | +18.8 | +26.4 | sem dado novo | 100 | 41 | 100 | 79.19 a 123.18 |

### cmb_termos_troca

Último dado 2026-07-01 (106 dias antes do corte) · A: `A/cmb_termos_troca.csv.gz`

| Série | Unidade | Data | Último | Δ% 1m | Δ% 3m | Δ% 12m | Δ% desde o ciclo ant. | Pctl 10a | Pctl hist. | Pctl Δ12m hist. | Mín–máx 10a |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Termos de troca (Funcex) | índice | 2026-07-01 | 111.35 | -1.8 | -2.7 | +1.5 | sem dado novo | 75 | 90 | 58 | 93.15 a 122.43 |

### cmb_fx_latam

Último dado 2026-10-13 (2 dias antes do corte) · A: `A/cmb_fx_latam.csv.gz`

| Série | Unidade | Data | Último | Δ% 1m | Δ% 3m | Δ% 12m | Δ% desde o ciclo ant. | Pctl 10a | Pctl hist. | Pctl Δ12m hist. | Mín–máx 10a |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Peso mexicano | MXN/US$ | 2026-10-13 | 18.3345 | +8.0 | +4.8 | -0.9 | +1.3 | 26 | 71 | 41 | 16.3125 a 25.1039 |
| Peso chileno | CLP/US$ | 2026-10-13 | 978.61 | +4.4 | +5.8 | +2.5 | +1.1 | 97 | 99 | 56 | 588.28 a 1042.97 |
| Peso colombiano | COP/US$ | 2026-10-09 | 3218.75 | +3.3 | -3.6 | -17.0 | +0.1 | 27 | 72 | 4 | 2705.34 a 5061.21 |
| Sol peruano | PEN/US$ | 2026-10-09 | 3.4535 | +2.8 | +1.5 | +0.5 | +0.1 | 45 | 64 | 72 | 3.2070 a 4.1340 |

### diferenciais_juros

Último dado 2026-10-01 (14 dias antes do corte) · A: `A/diferenciais_juros.csv.gz`

| Série | Unidade | Data | Último | Δ 1m | Δ 3m | Δ 12m | Δ desde o ciclo ant. | Pctl 10a | Pctl hist. | Mín–máx 10a |
|---|---|---|---|---|---|---|---|---|---|---|
| Selic | % a.a. | 2026-10-01 | 13.75 | +0.00 | -0.50 | -1.25 | sem dado novo | 83 | 62 | 2.00 a 15.00 |
| Fed Funds | % a.a. | 2026-09-01 | 3.75 | +0.12 | +0.12 | -0.47 | sem dado novo | 69 | 62 | 0.05 a 5.33 |
| Diferencial nominal (Selic − Fed Funds) | p.p. | 2026-09-01 | 10.00 | -0.37 | -0.62 | -0.78 | sem dado novo | 72 | 46 | 1.90 a 13.85 |
| IPCA 12m | % | 2026-09-01 | 4.58 | +0.36 | -0.06 | -0.59 | sem dado novo | 56 | 30 | 1.88 a 12.13 |
| CPI EUA 12m | % | 2026-09-01 | 3.72 | +0.36 | +0.25 | +0.69 | sem dado novo | 76 | 86 | 0.20 a 8.98 |
| Juro real ex-post Brasil | % a.a. | 2026-09-01 | 9.17 | -0.61 | -0.44 | -0.66 | sem dado novo | 83 | 67 | -4.74 a 11.19 |
| Juro real ex-post EUA | % a.a. | 2026-09-01 | 0.03 | -0.24 | -0.13 | -1.16 | sem dado novo | 59 | 51 | -8.37 a 2.72 |
| Diferencial real ex-post | p.p. | 2026-09-01 | 9.14 | -0.37 | -0.31 | +0.50 | sem dado novo | 81 | 72 | -1.61 a 12.21 |

## ii. Endógeno de política monetária (leitura enxuta)

### pm_copom_calendario

Último dado 2027-12-08 (data no futuro) · A: `A/pm_copom_calendario.csv.gz`

O calendário oficial vai até 2027-12-08.

| Reunião | Decisão | Dias a partir do corte |
|---|---|---|
| última | 2026-09-16 | -29 |
| próxima 1 | 2026-11-04 | 20 |
| próxima 2 | 2026-12-09 | 55 |
| próxima 3 | 2027-01-27 | 104 |
| próxima 4 | 2027-03-17 | 153 |

### pm_copom_reuniao

Último dado 2026-09-16 (29 dias antes do corte) · A: `A/pm_copom_reuniao.csv.gz`

| Reunião | Decisão | Selic decidida (% a.a.) | Passo (p.b.) |
|---|---|---|---|
| 281 | 2026-09-16 | 13.75 | -25 |
| 280 | 2026-08-05 | 14.00 | -25 |
| 279 | 2026-06-17 | 14.25 | -25 |
| 278 | 2026-04-29 | 14.50 | -25 |
| 277 | 2026-03-18 | 14.75 | -25 |
| 276 | 2026-01-28 | 15.00 | +0 |

### pm_copom_projecoes

Último dado 2026-09-24 (21 dias antes do corte) · A: `A/pm_copom_projecoes.csv.gz`

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

Último dado 2026-10-14 (1 dia antes do corte) · A: `A/br_di_grade.csv.gz`

Pregão de 2026-10-14. DI × pré, base 252, nos prazos redondos.

| Prazo | Taxa (% a.a.) | Δ 1m (p.b.) | Δ 3m (p.b.) | Δ 12m (p.b.) | Δ ciclo ant. (p.b.) |
|---|---|---|---|---|---|
| 1 mês | 13.59 | -11 | -50 | -131 | -2 |
| 3 meses | 13.44 | -17 | -51 | -145 | +3 |
| 6 meses | 13.24 | -32 | -67 | -155 | +5 |
| 1 ano | 12.85 | -76 | -105 | -137 | +11 |
| 2 anos | 12.46 | -134 | -149 | -101 | +3 |
| 3 anos | 12.46 | -154 | -168 | -89 | -4 |
| 5 anos | 12.55 | -161 | -171 | -106 | -12 |
| 10 anos | 12.63 | -166 | -165 | -113 | -16 |

Selic precificada na curva em cada reunião (meta vigente 13.75%). É preço, com prêmio de prazo, não previsão. Reuniões só até onde vai o calendário oficial (2027-12-08).

| Reunião | Selic na curva (% a.a.) | Passo implícito (p.b.) | 1 mês antes (2026-09-14) | Δ 1 mês (p.b.) |
|---|---|---|---|---|
| 2026-11-04 | 13.57 | -18 | 13.63 | -6 |
| 2026-12-09 | 13.38 | -19 | 13.59 | -21 |
| 2027-01-27 | 13.18 | -20 | 13.62 | -43 |
| 2027-03-17 | 12.99 | -19 | 13.67 | -68 |
| 2027-04-28 | 12.79 | -20 | 13.72 | -93 |
| 2027-06-16 | 12.58 | -21 | 13.76 | -118 |
| 2027-08-04 | 12.39 | -19 | 13.80 | -141 |
| 2027-09-22 | 12.25 | -14 | 13.85 | -160 |
| 2027-10-27 | 12.16 | -9 | 13.94 | -178 |
| 2027-12-08 | 12.13 | -3 | 14.07 | -194 |

### inflc_meta

Último dado 2026-01-01 (287 dias antes do corte) · A: `A/inflc_meta.csv.gz`

| Ano | Meta (%) |
|---|---|
| 2024 | 3.00 |
| 2025 | 3.00 |
| 2026 | 3.00 |

## iii. TWA — expectativas (leitura enxuta)

### expc_focus_periodo (câmbio)

Último dado 2026-10-09 (6 dias antes do corte) · A: `A/expc_focus_periodo__cambio.csv.gz`

Unidade: R$/US$. Mediana da pesquisa (janela de 30 dias).

| Ano | Mediana (2026-10-09) | 4 sem. antes (2026-09-11) | 13 sem. antes (2026-07-10) | Δ 4 sem. | Ciclo ant. (2026-10-07) | Respondentes |
|---|---|---|---|---|---|---|
| 2026 | 5.15 | 5.20 | 5.20 | -0.05 | 5.20 | 111 |
| 2027 | 5.26 | 5.28 | 5.28 | -0.02 | 5.28 | 111 |
| 2028 | 5.30 | 5.30 | 5.33 | +0.00 | 5.30 | 85 |
| 2029 | 5.30 | 5.36 | 5.40 | -0.06 | 5.33 | 79 |

### expc_focus_copom

Último dado 2026-10-09 (6 dias antes do corte) · A: `A/expc_focus_copom.csv.gz`

Selic vigente na data da pesquisa: 13.75% (decidida em 2026-09-16). Mediana da pesquisa (janela de 30 dias), % a.a.

| Reunião | Data | Mediana (2026-10-09) | 4 sem. antes (2026-09-11) | Δ 4 sem. (p.p.) | Mín–máx | Ciclo ant. (2026-10-07) |
|---|---|---|---|---|---|---|
| R7/2026 | 2026-11-04 | 13.50 | 13.75 | -0.25 | 13.50 a 14.00 | 13.50 |
| R8/2026 | 2026-12-09 | 13.25 | 13.75 | -0.50 | 13.00 a 14.00 | 13.50 |
| R1/2027 | 2027-01-27 | 13.25 | 13.50 | -0.25 | 12.50 a 14.00 | 13.25 |
| R2/2027 | 2027-03-17 | 13.00 | 13.50 | -0.50 | 12.00 a 14.00 | 13.25 |
| R3/2027 | 2027-04-28 | 12.75 | 13.25 | -0.50 | 11.25 a 14.00 | 13.00 |
| R4/2027 | 2027-06-16 | 12.62 | 13.00 | -0.38 | 10.50 a 14.00 | 12.75 |
| R5/2027 | 2027-08-04 | 12.50 | 12.62 | -0.12 | 9.75 a 14.00 | 12.50 |
| R6/2027 | 2027-09-22 | 12.25 | 12.50 | -0.25 | 9.75 a 14.00 | 12.50 |

### expc_focus_periodo (Selic)

Último dado 2026-10-09 (6 dias antes do corte) · A: `A/expc_focus_periodo__selic.csv.gz`

Unidade: %. Mediana da pesquisa (janela de 30 dias).

| Ano | Mediana (2026-10-09) | 4 sem. antes (2026-09-11) | 13 sem. antes (2026-07-10) | Δ 4 sem. | Ciclo ant. (2026-10-07) | Respondentes |
|---|---|---|---|---|---|---|
| 2026 | 13.25 | 13.75 | 14.00 | -0.50 | 13.50 | 139 |
| 2027 | 12.00 | 12.00 | 12.00 | +0.00 | 12.00 | 138 |
| 2028 | 10.50 | 10.50 | 10.50 | +0.00 | 10.50 | 117 |
| 2029 | 10.00 | 10.00 | 10.00 | +0.00 | 10.00 | 110 |

### expc_focus_periodo (IPCA)

Último dado 2026-10-09 (6 dias antes do corte) · A: `A/expc_focus_periodo__ipca.csv.gz`

Unidade: %. Mediana da pesquisa (janela de 30 dias).

| Ano | Mediana (2026-10-09) | 4 sem. antes (2026-09-11) | 13 sem. antes (2026-07-10) | Δ 4 sem. | Ciclo ant. (2026-10-07) | Respondentes |
|---|---|---|---|---|---|---|
| 2026 | 5.22 | 4.90 | 5.16 | +0.32 | 5.02 | 144 |
| 2027 | 4.30 | 4.30 | 4.20 | +0.00 | 4.31 | 144 |
| 2028 | 3.79 | 3.80 | 3.70 | -0.01 | 3.80 | 121 |
| 2029 | 3.50 | 3.50 | 3.50 | -0.00 | 3.50 | 113 |

## iv. TWA — externo (leitura enxuta)

### cmb_dollar_index

Último dado 2026-10-15 (no corte) · A: `A/cmb_dollar_index.csv.gz`

| Série | Unidade | Data | Último | Δ% 1m | Δ% 3m | Δ% 12m | Δ% desde o ciclo ant. |
|---|---|---|---|---|---|---|---|
| DXY | índice | 2026-10-15 | 102.06 | +2.4 | +1.6 | +3.3 | -0.2 |

### cmb_dollar_index_em

Último dado 2026-10-09 (6 dias antes do corte) · A: `A/cmb_dollar_index_em.csv.gz`

| Série | Unidade | Data | Último | Δ% 1m | Δ% 3m | Δ% 12m | Δ% desde o ciclo ant. |
|---|---|---|---|---|---|---|---|
| Dólar contra emergentes (FRED) | índice | 2026-10-09 | 129.77 | +2.9 | +0.2 | -1.4 | +0.6 |

### cmb_equity_us

Último dado 2026-10-15 (no corte) · A: `A/cmb_equity_us.csv.gz`

| Série | Unidade | Data | Último | Δ% 1m | Δ% 3m | Δ% 12m | Δ% desde o ciclo ant. |
|---|---|---|---|---|---|---|---|
| S&P 500 | pontos | 2026-10-15 | 7721 | +1.8 | +2.0 | +15.7 | -1.0 |

### us_interest_rate

Último dado 2026-10-15 (no corte) · A: `A/us_interest_rate.csv.gz`

| Série | Unidade | Data | Último | Δ 1m | Δ 3m | Δ 12m | Δ desde o ciclo ant. |
|---|---|---|---|---|---|---|---|
| Fed Funds, meta (ponto médio) | % a.a. | 2026-10-15 | 3.88 | +0.25 | +0.25 | -0.25 | +0.00 |
| Treasury 2 anos | % a.a. | 2026-10-13 | 4.79 | +0.16 | +0.53 | +1.27 | +0.02 |
| Treasury 10 anos | % a.a. | 2026-10-13 | 5.21 | +0.25 | +0.59 | +1.16 | -0.07 |

### cmb_real_rates

Último dado 2026-08-01 (75 dias antes do corte) · A: `A/cmb_real_rates.csv.gz`

| Série | Unidade | Data | Último | Δ 1m | Δ 3m | Δ 12m | Δ desde o ciclo ant. |
|---|---|---|---|---|---|---|---|
| BR, juro real ex-post | % a.a. | 2026-08-01 | 9.78 | -0.03 | +0.00 | -0.09 | sem dado novo |
| MX, juro real ex-post | % a.a. | 2026-08-01 | 3.24 | -0.14 | +0.68 | -0.94 | sem dado novo |
| CL, juro real ex-post | % a.a. | 2026-08-01 | 0.37 | -0.61 | -0.20 | -0.35 | sem dado novo |
| CO, juro real ex-post | % a.a. | 2026-08-01 | 5.76 | -0.22 | +0.35 | +1.60 | sem dado novo |
| PE, juro real ex-post | % a.a. | 2026-08-01 | -0.19 | -0.37 | -0.53 | -3.58 | sem dado novo |

### comm_brent

Último dado 2026-10-06 (9 dias antes do corte) · A: `A/comm_brent.csv.gz`

| Série | Unidade | Data | Último | Δ% 1m | Δ% 3m | Δ% 12m | Δ% desde o ciclo ant. |
|---|---|---|---|---|---|---|---|
| Brent | US$/barril | 2026-10-06 | 125.44 | +22.7 | +80.3 | +87.0 | sem dado novo |

### comm_icbr_usd

Último dado 2026-09-01 (44 dias antes do corte) · A: `A/comm_icbr_usd.csv.gz`

| Série | Unidade | Data | Último | Δ% 1m | Δ% 3m | Δ% 12m | Δ% desde o ciclo ant. |
|---|---|---|---|---|---|---|---|
| IC-Br em dólar | índice | 2026-09-01 | 205.70 | +1.7 | +4.1 | +12.8 | sem dado novo |
| IC-Br agropecuária | índice | 2026-09-01 | 201.80 | +0.3 | +3.3 | +0.7 | sem dado novo |
| IC-Br metal | índice | 2026-09-01 | 335.06 | -0.6 | +0.7 | +42.2 | sem dado novo |
| IC-Br energia | índice | 2026-09-01 | 96.00 | +10.6 | +11.2 | +29.2 | sem dado novo |

## v. TWA — doméstico (leitura enxuta)

### inflc_agregados

Último dado 2026-09-01 (44 dias antes do corte) · A: `A/inflc_agregados.csv.gz`

| Série | Mês | Último mês | Acum. 3m | Acum. 12m | Acum. 12m, 3 meses antes |
|---|---|---|---|---|---|
| IPCA | 2026-09 | 0.82 | 0.57 | 4.58 | 4.64 |
| Livres | 2026-09 | 0.55 | 0.55 | 4.68 | 4.31 |
| Administrados | 2026-09 | 1.59 | 0.59 | 4.14 | 5.52 |
| Comercializáveis | 2026-09 | 0.20 | 0.41 | 2.65 | 2.15 |
| Não comercializáveis | 2026-09 | 0.80 | 0.67 | 6.22 | 5.92 |
| Serviços | 2026-09 | 0.61 | 1.18 | 5.97 | 5.90 |
| Industriais | 2026-09 | 0.17 | 0.50 | 3.07 | 2.76 |

### fisc_nfsp

Último dado 2026-08-01 (75 dias antes do corte) · A: `A/fisc_nfsp.csv.gz`

| Série | Unidade | Data | Último | Δ 1m | Δ 3m | Δ 12m | Δ desde o ciclo ant. |
|---|---|---|---|---|---|---|---|
| Resultado primário, 12m (+ = superávit) | % do PIB | 2026-08-01 | -0.62 | +0.05 | +0.52 | -0.43 | sem dado novo |
| Resultado nominal, 12m | % do PIB | 2026-08-01 | -9.48 | -0.13 | +0.13 | -1.69 | sem dado novo |
| Juros nominais, 12m | % do PIB | 2026-08-01 | 8.86 | +0.18 | +0.38 | +1.25 | sem dado novo |

### fisc_divida

Último dado 2026-08-01 (75 dias antes do corte) · A: `A/fisc_divida.csv.gz`

| Série | Unidade | Data | Último | Δ 1m | Δ 3m | Δ 12m | Δ desde o ciclo ant. |
|---|---|---|---|---|---|---|---|
| Dívida bruta do governo geral | % do PIB | 2026-08-01 | 82.9 | +0.3 | +1.8 | +5.5 | sem dado novo |
| Dívida líquida do setor público | % do PIB | 2026-08-01 | 69.3 | +0.1 | +1.4 | +5.2 | sem dado novo |

### atv_pib_usd

Último dado 2026-08-01 (75 dias antes do corte) · A: `A/atv_pib_usd.csv.gz`

| Série | Unidade | Último mês | Soma 3m | Soma 12m | Soma 12m, um ano antes |
|---|---|---|---|---|---|
| PIB mensal em dólar | US$ bi | 223.05 (2026-08) | 671.31 | 2553.86 | 2176.49 |

## vi. Exógeno (leitura enxuta)

### cmb_risco_pais

Último dado 2026-10-14 (1 dia antes do corte) · A: `A/cmb_risco_pais.csv.gz`

| Série | Unidade | Data | Último | Δ 1m | Δ 3m | Δ 12m | Δ desde o ciclo ant. |
|---|---|---|---|---|---|---|---|
| CDS 5 anos Brasil | p.b. | 2026-10-14 | 112 | +0 | -11 | -40 | +3 |

## Leituras combinadas

### O real e os pares

Moeda local por dólar: Δ% positivo = a moeda se desvalorizou. Volatilidade realizada em % ao ano. Juro de política dos pares pelo BIS (mensal, com defasagem: data ao lado); o do Brasil é a Selic vigente. Carry = juro de política menos a meta do Fed na mesma data.

| Moeda | Data | Δ% 1m | Δ% 3m | Δ% 12m | Δ% desde o ciclo ant. | Vol. 21d | Vol. 63d | Pctl vol. 63d 10a | Juro de política | Carry vs Fed (p.p.) | Carry / vol. 63d |
|---|---|---|---|---|---|---|---|---|---|---|---|
| BRL | 2026-10-14 | -2.4 | -0.6 | -8.3 | +1.0 | 18.0 | 12.2 | 54 | 13.75 (2026-09-16) | 10.12 | 0.83 |
| MXN | 2026-10-13 | +8.0 | +4.8 | -0.9 | +1.3 | 10.3 | 7.5 | 13 | 6.50 (2026-08-01) | 2.88 | 0.38 |
| CLP | 2026-10-13 | +4.4 | +5.8 | +2.5 | +1.1 | 12.1 | 9.7 | 38 | 4.50 (2026-08-01) | 0.88 | 0.09 |
| COP | 2026-10-09 | +3.3 | -3.6 | -17.0 | +0.1 | 16.1 | 14.8 | 86 | 12.00 (2026-08-01) | 8.38 | 0.56 |
| PEN | 2026-10-09 | +2.8 | +1.5 | +0.5 | +0.1 | 6.4 | 4.5 | 38 | 4.25 (2026-08-01) | 0.62 | 0.14 |
