# F(A) — cambio — ciclo 2026-10-27

Gerado em 2026-10-27 13:03. Dados do banco até 2026-10-27, fixos durante o ciclo. Ciclo anterior: 2026-10-22.

Os dados brutos (A) estão em `A/`, um arquivo por tabela; as funções G leem de lá e o código delas fica em `G/`. Nada aqui é opinião: é a mesma conta em todo ciclo.

Como ler:
- **Δ% 1m/3m/12m**: variação contra o último valor de 1, 3 e 12 meses antes da última data da série; numa série trimestral, **1t/4t**: contra 1 e 4 trimestres antes.
- **Δ**: diferença na unidade da série (p.p. quando a série é %, p.b. quando é p.b.).
- **Pctl**: posição do último valor no histórico, de 0 (o menor já visto) a 100 (o maior). "10a" = últimos 10 anos.
- **Soma 3m/12m**: soma dos últimos 3 e 12 meses completos; o mês em curso aparece à parte e não entra nas somas.
- **Acum.**: variação composta.
- **Desde o ciclo ant.**: contra o valor em 2026-10-22.

## i. Endógeno (leitura completa)

### cmb_ptax

Último dado 2026-10-26 (1 dia antes do corte) · A: `A/cmb_ptax.csv.gz`

| Série | Unidade | Data | Último | Δ% 1m | Δ% 3m | Δ% 12m | Δ% desde o ciclo ant. | Pctl 10a | Pctl hist. | Pctl Δ12m hist. | Mín–máx 10a |
|---|---|---|---|---|---|---|---|---|---|---|---|
| PTAX venda | R$/US$ | 2026-10-26 | 5.5007 | +5.8 | +8.6 | +2.2 | +9.2 | 84 | 95 | 44 | 3.0510 a 6.2086 |

| Série | Unidade | Data | Média 1m | Média 3m | Média 12m | Pctl média 1m 10a |
|---|---|---|---|---|---|---|
| Volume interbancário D+1 | US$ mi/dia | 2026-10-23 | 326 | 290 | 368 | 67 |
| Volume interbancário D+2 | US$ mi/dia | 2026-10-23 | 985 | 1014 | 1508 | 19 |

### cmb_cambio_contratado

Último dado 2026-10-16 (11 dias antes do corte) · A: `A/cmb_cambio_contratado.csv.gz`

| Série | Unidade | Último mês | Soma 3m | Soma 12m | Soma 12m, um ano antes | Mês em curso | Soma desde o ciclo ant. | Pctl soma 12m hist. |
|---|---|---|---|---|---|---|---|---|
| Saldo total (comercial + financeiro) | US$ bi | -5.20 (2026-09) | -7.17 | -4.01 | -42.67 | 5.15 (até 16/10) | 0.00 | 40 |
| Comercial, saldo | US$ bi | 2.13 (2026-09) | 11.76 | 58.26 | 46.33 | 1.02 (até 16/10) | 0.00 | 93 |
| Comercial, exportação | US$ bi | 26.34 (2026-09) | 81.09 | 309.00 | 286.53 | 12.51 (até 16/10) | 0.00 | 100 |
| Comercial, importação | US$ bi | 24.21 (2026-09) | 69.34 | 250.74 | 240.20 | 11.49 (até 16/10) | 0.00 | 100 |
| Financeiro, saldo | US$ bi | -7.33 (2026-09) | -18.92 | -62.27 | -89.00 | 4.13 (até 16/10) | 0.00 | 18 |
| Financeiro, compras | US$ bi | 63.35 (2026-09) | 160.51 | 686.26 | 581.45 | 44.42 (até 16/10) | 0.00 | 100 |
| Financeiro, vendas | US$ bi | 70.68 (2026-09) | 179.43 | 748.53 | 670.44 | 40.29 (até 16/10) | 0.00 | 100 |
| Financeiro: serviços (mensal) | US$ bi | -2.61 (2026-09) | -8.05 | -28.30 | -30.37 |  |  | 68 |
| Financeiro: rendas (mensal) | US$ bi | -4.60 (2026-09) | -12.31 | -66.03 | -55.76 |  |  | 6 |
| Financeiro: capitais brasileiros (mensal) | US$ bi | -5.04 (2026-09) | -11.38 | -49.62 | -40.59 |  |  | 3 |
| Financeiro: capitais estrangeiros (mensal) | US$ bi | 4.92 (2026-09) | 12.82 | 81.68 | 37.72 |  |  | 66 |

### cmb_balanco_pagmt

Último dado 2026-09-01 (56 dias antes do corte) · A: `A/cmb_balanco_pagmt.csv.gz`

| Série | Unidade | Último mês | Soma 3m | Soma 12m | Soma 12m, um ano antes | 12m % PIB | Pctl soma 12m hist. |
|---|---|---|---|---|---|---|---|
| Transações correntes | US$ bi | -5.10 (2026-09) | -20.16 | -59.99 | -78.43 | -2.33 | 26 |
| Exportação de bens | US$ bi | 34.58 (2026-09) | 101.14 | 376.63 | 342.29 |  | 100 |
| Importação de bens | US$ bi | 27.72 (2026-09) | 82.64 | 302.30 | 288.64 |  | 100 |
| Serviços, saldo | US$ bi | -5.24 (2026-09) | -15.98 | -56.25 | -54.11 |  | 3 |
| Renda primária, saldo | US$ bi | -7.20 (2026-09) | -24.07 | -84.23 | -82.70 |  | 0 |
| Conta financeira (concessões − captações líquidas) | US$ bi | -7.20 (2026-09) | -24.89 | -65.83 | -80.42 |  | 24 |
| Investimento direto no país (passivos) | US$ bi | 11.29 (2026-09) | 25.66 | 88.27 | 85.01 | 3.43 | 93 |
| Carteira, passivos | US$ bi | -1.70 (2026-09) | -4.86 | 16.36 | 8.68 | 0.64 | 61 |
| Carteira: ações, passivos | US$ bi | -2.11 (2026-09) | -5.98 | -5.34 | -6.36 |  | 10 |
| Carteira: títulos no mercado doméstico, passivos | US$ bi | -0.38 (2026-09) | 0.19 | 11.78 | 16.55 |  | 72 |
| Outros investimentos, passivos | US$ bi | 3.26 (2026-09) | 13.75 | 35.37 | 15.70 |  | 92 |
| Ativos de reserva | US$ bi | -3.62 (2026-09) | -0.42 | 11.93 | -22.95 |  | 67 |
| Erros e omissões | US$ bi | -2.15 (2026-09) | -4.89 | -5.71 | -1.78 |  | 3 |

### cmb_comex_fator_agregado

Último dado 2026-09-01 (56 dias antes do corte) · A: `A/cmb_comex_fator_agregado.csv.gz`

| Série | Unidade | Último mês | Soma 3m | Soma 12m | Soma 12m, um ano antes | Pctl soma 12m hist. |
|---|---|---|---|---|---|---|
| Básicos, exportação | US$ bi | 20.54 (2026-09) | 59.86 | 224.73 | 194.52 | 100 |
| Básicos, importação | US$ bi | 1.95 (2026-09) | 5.87 | 21.53 | 21.67 | 64 |
| Semimanufaturados, exportação | US$ bi | 4.09 (2026-09) | 12.96 | 48.18 | 45.36 | 100 |
| Semimanufaturados, importação | US$ bi | 1.22 (2026-09) | 3.62 | 13.35 | 11.94 | 96 |
| Manufaturados, exportação | US$ bi | 9.76 (2026-09) | 27.86 | 101.93 | 99.95 | 100 |
| Manufaturados, importação | US$ bi | 23.49 (2026-09) | 70.11 | 255.82 | 244.45 | 100 |
| Demais, exportação | US$ bi | 0.02 (2026-09) | 0.06 | 0.20 | 0.11 | 25 |
| Demais, importação | US$ bi | 0.02 (2026-09) | 0.06 | 0.17 | 0.10 | 100 |

### cmb_comex_pais

Último dado 2026-09-01 (56 dias antes do corte) · A: `A/cmb_comex_pais.csv.gz`

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

Último dado 2026-09-01 (56 dias antes do corte) · A: `A/cmb_comex_produto.csv.gz`

| Série | Unidade | Último mês | Soma 3m | Soma 12m | Soma 12m, um ano antes | Pctl soma 12m hist. |
|---|---|---|---|---|---|---|
| Mundo, exportação | US$ bi | 34.42 (2026-09) | 100.73 | 375.04 | 339.93 | 100 |
| Mundo, importação | US$ bi | 26.68 (2026-09) | 79.66 | 290.87 | 278.16 | 100 |
| Petróleo, exportação | US$ bi | 6.50 (2026-09) | 15.72 | 54.10 | 43.87 | 100 |
| Petróleo, importação | US$ bi | 0.63 (2026-09) | 1.93 | 6.71 | 7.12 | 49 |
| Soja, exportação | US$ bi | 3.47 (2026-09) | 13.76 | 49.10 | 41.33 | 97 |
| Soja, importação | US$ bi | 0.05 (2026-09) | 0.12 | 0.40 | 0.26 | 97 |
| Minério de ferro, exportação | US$ bi | 2.02 (2026-09) | 6.77 | 28.53 | 27.33 | 72 |
| Minério de ferro, importação | US$ bi | 0.01 (2026-09) | 0.01 | 0.02 | 0.00 | 84 |
| Carnes, exportação | US$ bi | 2.51 (2026-09) | 7.76 | 33.26 | 28.04 | 99 |
| Carnes, importação | US$ bi | 0.03 (2026-09) | 0.09 | 0.35 | 0.37 | 75 |
| Café, exportação | US$ bi | 1.30 (2026-09) | 3.22 | 13.78 | 14.05 | 97 |
| Café, importação | US$ bi | 0.01 (2026-09) | 0.03 | 0.11 | 0.11 | 93 |

### cmb_reservas_bc

Último dado 2026-10-26 (1 dia antes do corte) · A: `A/cmb_reservas_bc.csv.gz`

| Série | Unidade | Data | Último | Δ 1m | Δ 3m | Δ 12m | Δ desde o ciclo ant. | Pctl 10a | Pctl hist. | Mín–máx 10a |
|---|---|---|---|---|---|---|---|---|---|---|
| Reservas internacionais | US$ bi | 2026-10-26 | 364.9 | -0.0 | -4.0 | +5.7 | -0.1 | 57 | 74 | 323.5 a 390.5 |
| Reservas, conceito liquidez | US$ bi | 2026-10-26 | 368.9 | +1.0 | -2.0 | -1.6 | -0.1 | 56 | 53 | 327.4 a 401.6 |
| Swap cambial do BC, posição (− = vendido) | US$ bi | 2026-08-01 | -91.6 | +1.3 | +3.2 | +9.8 | sem dado novo | 46 | 34 | -102.7 a -17.8 |
| Posição à vista dos bancos | US$ bi | 2026-09-01 | -26.2 | -4.1 | -4.8 | +2.0 | sem dado novo | 24 | 9 | -42.4 a 4.6 |

| Série | Unidade | Último mês | Soma 3m | Soma 12m | Soma 12m, um ano antes | Mês em curso | Soma desde o ciclo ant. | Pctl soma 12m hist. |
|---|---|---|---|---|---|---|---|---|
| Intervenção à vista (+ compra, − venda) | US$ bi | -2.00 (2026-09) | -3.00 | -8.00 | -22.57 | 0.00 (até 26/10) | 0.00 | 14 |
| Leilões de linha (+ compra, − venda) | US$ bi | -2.00 (2026-09) | 0.05 | 7.25 | -11.25 | 0.00 (até 26/10) | 0.00 | 92 |

### cmb_cot_fx

Último dado 2026-10-20 (7 dias antes do corte) · A: `A/cmb_cot_fx.csv.gz`

| Série | Unidade | Data | Último | Δ 1m | Δ 3m | Δ 12m | Δ desde o ciclo ant. | Pctl 10a | Pctl hist. | Mín–máx 10a |
|---|---|---|---|---|---|---|---|---|---|---|
| BRL: fundos alavancados, líquido | contratos | 2026-10-20 | 18677 | +2572 | +17002 | +17286 | sem dado novo | 96 | 97 | -40335 a 32847 |
| BRL: asset managers, líquido | contratos | 2026-10-20 | 51268 | -6208 | -2287 | -3084 | sem dado novo | 85 | 90 | -57523 a 78334 |
| BRL: dealers, líquido | contratos | 2026-10-20 | -65413 | -16787 | -6376 | -19865 | sem dado novo | 4 | 3 | -83394 a 59543 |
| BRL: outros reportáveis, líquido | contratos | 2026-10-20 | -8998 | +19875 | -8790 | +3748 | sem dado novo | 9 | 12 | -48451 a 12141 |
| BRL: não reportáveis, líquido | contratos | 2026-10-20 | 4466 | +548 | +451 | +1915 | sem dado novo | 98 | 98 | -5527 a 14033 |
| BRL: posições em aberto | contratos | 2026-10-20 | 135679 | +19792 | +29620 | +37219 | sem dado novo | 98 | 99 | 10333 a 152424 |
| MXN: fundos alavancados, líquido | contratos | 2026-10-20 | 63814 | -26194 | +10015 | +37820 | sem dado novo | 90 | 87 | -79304 a 114016 |
| MXN: asset managers, líquido | contratos | 2026-10-20 | -24064 | -77410 | -54926 | -83997 | sem dado novo | 0 | 0 | -24064 a 176493 |
| MXN: dealers, líquido | contratos | 2026-10-20 | 15252 | +109018 | +77071 | +107673 | sem dado novo | 96 | 92 | -234567 a 39715 |
| MXN: outros reportáveis, líquido | contratos | 2026-10-20 | -55805 | -2302 | -28178 | -59306 | sem dado novo | 16 | 10 | -111774 a 6128 |
| MXN: não reportáveis, líquido | contratos | 2026-10-20 | 803 | -3112 | -3982 | -2190 | sem dado novo | 19 | 31 | -10152 a 13919 |
| MXN: posições em aberto | contratos | 2026-10-20 | 278165 | -41334 | +78815 | +99920 | sem dado novo | 92 | 95 | 94469 a 376712 |

### cmb_reer

Último dado 2026-09-01 (56 dias antes do corte) · A: `A/cmb_reer.csv.gz`

| Série | Unidade | Data | Último | Δ% 1m | Δ% 3m | Δ% 12m | Δ% desde o ciclo ant. | Pctl 10a | Pctl hist. | Pctl Δ12m hist. | Mín–máx 10a |
|---|---|---|---|---|---|---|---|---|---|---|---|
| BR, real efetivo | índice 2020=100 | 2026-09-01 | 117.18 | +0.6 | -0.9 | +4.5 | sem dado novo | 53 | 36 | 60 | 90.32 a 151.33 |
| BR, nominal efetivo | índice 2020=100 | 2026-09-01 | 113.48 | +0.3 | -0.4 | +3.8 | sem dado novo | 52 | 19 | 67 | 88.28 a 146.37 |
| MX, real efetivo | índice 2020=100 | 2026-09-01 | 140.31 | -1.2 | -0.0 | +6.9 | sem dado novo | 92 | 76 | 69 | 88.88 a 144.59 |
| MX, nominal efetivo | índice 2020=100 | 2026-09-01 | 127.52 | -1.1 | +0.2 | +6.5 | sem dado novo | 89 | 31 | 84 | 89.71 a 134.70 |
| CL, real efetivo | índice 2020=100 | 2026-09-01 | 98.94 | -3.2 | -5.0 | +0.1 | sem dado novo | 15 | 7 | 53 | 92.25 a 117.27 |
| CL, nominal efetivo | índice 2020=100 | 2026-09-01 | 91.73 | -3.1 | -5.1 | -0.5 | sem dado novo | 3 | 1 | 53 | 87.75 a 117.49 |
| CO, real efetivo | índice 2020=100 | 2026-09-01 | 144.72 | -1.6 | +9.7 | +24.8 | sem dado novo | 99 | 98 | 97 | 83.28 a 147.02 |
| CO, nominal efetivo | índice 2020=100 | 2026-09-01 | 121.37 | -1.5 | +9.7 | +21.3 | sem dado novo | 99 | 40 | 97 | 79.19 a 123.18 |

### cmb_termos_troca

Último dado 2026-08-01 (87 dias antes do corte) · A: `A/cmb_termos_troca.csv.gz`

| Série | Unidade | Data | Último | Δ% 1m | Δ% 3m | Δ% 12m | Δ% desde o ciclo ant. | Pctl 10a | Pctl hist. | Pctl Δ12m hist. | Mín–máx 10a |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Termos de troca (Funcex) | índice | 2026-08-01 | 108.44 | -1.5 | -3.0 | +2.5 | sem dado novo | 60 | 84 | 63 | 93.15 a 122.43 |

### cmb_fx_latam

Último dado 2026-10-20 (7 dias antes do corte) · A: `A/cmb_fx_latam.csv.gz`

**Atenção:** O peso chileno e o colombiano datados em um dia são a taxa oficial formada no dia útil anterior: para comparar com o real ou com o dólar no mesmo dia, leia a taxa do dia útil seguinte. A tabela abaixo está como a fonte publica.

| Série | Unidade | Data | Último | Δ% 1m | Δ% 3m | Δ% 12m | Δ% desde o ciclo ant. | Pctl 10a | Pctl hist. | Pctl Δ12m hist. | Mín–máx 10a |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Peso mexicano | MXN/US$ | 2026-10-20 | 18.5215 | +7.8 | +5.9 | +0.7 | sem dado novo | 29 | 72 | 45 | 16.3125 a 25.1039 |
| Peso chileno | CLP/US$ | 2026-10-20 | 981.86 | +2.8 | +5.1 | +2.2 | sem dado novo | 98 | 99 | 57 | 588.28 a 1042.97 |
| Peso colombiano | COP/US$ | 2026-10-16 | 3170.46 | +2.3 | -2.0 | -18.8 | sem dado novo | 24 | 71 | 3 | 2705.34 a 5061.21 |
| Sol peruano | PEN/US$ | 2026-10-19 | 3.4405 | +2.5 | +1.0 | +1.4 | sem dado novo | 44 | 63 | 71 | 3.2070 a 4.1340 |

### diferenciais_juros

Último dado 2026-10-01 (26 dias antes do corte) · A: `A/diferenciais_juros.csv.gz`

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
| última | 2026-09-16 | -41 |
| próxima 1 | 2026-11-04 | 8 |
| próxima 2 | 2026-12-09 | 43 |
| próxima 3 | 2027-01-27 | 92 |
| próxima 4 | 2027-03-17 | 141 |

### pm_copom_reuniao

Último dado 2026-09-16 (41 dias antes do corte) · A: `A/pm_copom_reuniao.csv.gz`

| Reunião | Decisão | Selic decidida (% a.a.) | Passo (p.b.) |
|---|---|---|---|
| 281 | 2026-09-16 | 13.75 | -25 |
| 280 | 2026-08-05 | 14.00 | -25 |
| 279 | 2026-06-17 | 14.25 | -25 |
| 278 | 2026-04-29 | 14.50 | -25 |
| 277 | 2026-03-18 | 14.75 | -25 |
| 276 | 2026-01-28 | 15.00 | +0 |

### pm_copom_projecoes

Último dado 2026-09-24 (33 dias antes do corte) · A: `A/pm_copom_projecoes.csv.gz`

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

Último dado 2026-10-26 (1 dia antes do corte) · A: `A/br_di_grade.csv.gz`

Pregão de 2026-10-26. DI × pré, base 252, nos prazos redondos.

| Prazo | Taxa (% a.a.) | Δ 1m (p.b.) | Δ 3m (p.b.) | Δ 12m (p.b.) | Δ ciclo ant. (p.b.) |
|---|---|---|---|---|---|
| 1 mês | 13.62 | -4 | -41 | -128 | +6 |
| 3 meses | 13.77 | +22 | -18 | -111 | +31 |
| 6 meses | 14.15 | +60 | +16 | -60 | +83 |
| 1 ano | 14.70 | +109 | +59 | +64 | +170 |
| 2 anos | 15.19 | +140 | +84 | +201 | +250 |
| 3 anos | 15.30 | +141 | +75 | +227 | +263 |
| 5 anos | 15.29 | +133 | +63 | +199 | +258 |
| 10 anos | 15.12 | +116 | +42 | +164 | +235 |

Selic precificada na curva em cada reunião (meta vigente 13.75%). É preço, com prêmio de prazo, não previsão. Reuniões só até onde vai o calendário oficial (2027-12-08).

| Reunião | Selic na curva (% a.a.) | Passo implícito (p.b.) | 1 mês antes (2026-09-25) | Δ 1 mês (p.b.) |
|---|---|---|---|---|
| 2026-11-04 | 13.73 | -2 | 13.61 | +12 |
| 2026-12-09 | 14.02 | +29 | 13.58 | +44 |
| 2027-01-27 | 14.45 | +44 | 13.63 | +82 |
| 2027-03-17 | 14.84 | +39 | 13.69 | +115 |
| 2027-04-28 | 15.13 | +30 | 13.73 | +140 |
| 2027-06-16 | 15.31 | +18 | 13.77 | +154 |
| 2027-08-04 | 15.43 | +12 | 13.80 | +163 |
| 2027-09-22 | 15.54 | +11 | 13.85 | +169 |
| 2027-10-27 | 15.65 | +11 | 13.92 | +173 |
| 2027-12-08 | 15.78 | +13 | 14.02 | +176 |

### inflc_meta

Último dado 2026-01-01 (299 dias antes do corte) · A: `A/inflc_meta.csv.gz`

| Ano | Meta (%) |
|---|---|
| 2024 | 3.00 |
| 2025 | 3.00 |
| 2026 | 3.00 |

## iii. Endógeno de expectativas (leitura enxuta)

### expc_focus_periodo (câmbio)

Último dado 2026-10-23 (4 dias antes do corte) · A: `A/expc_focus_periodo__cambio.csv.gz`

Unidade: R$/US$. Mediana da pesquisa (janela de 30 dias).

| Ano | Mediana (2026-10-23) | 4 sem. antes (2026-09-25) | 13 sem. antes (2026-07-24) | Δ 4 sem. | Ciclo ant. (2026-10-22) | Respondentes |
|---|---|---|---|---|---|---|
| 2026 | 5.05 | 5.20 | 5.20 | -0.15 | 5.10 | 112 |
| 2027 | 5.15 | 5.28 | 5.29 | -0.13 | 5.20 | 111 |
| 2028 | 5.20 | 5.30 | 5.30 | -0.10 | 5.22 | 87 |
| 2029 | 5.28 | 5.35 | 5.37 | -0.07 | 5.29 | 82 |

### expc_focus_copom

Último dado 2026-10-23 (4 dias antes do corte) · A: `A/expc_focus_copom.csv.gz`

Selic vigente na data da pesquisa: 13.75% (decidida em 2026-09-16). Mediana da pesquisa (janela de 30 dias), % a.a.

| Reunião | Data | Mediana (2026-10-23) | 4 sem. antes (2026-09-25) | Δ 4 sem. (p.p.) | Mín–máx | Ciclo ant. (2026-10-22) |
|---|---|---|---|---|---|---|
| R7/2026 | 2026-11-04 | 13.50 | 13.50 | +0.00 | 13.25 a 14.00 | 13.50 |
| R8/2026 | 2026-12-09 | 13.25 | 13.50 | -0.25 | 13.00 a 14.00 | 13.25 |
| R1/2027 | 2027-01-27 | 13.00 | 13.50 | -0.50 | 12.50 a 14.00 | 13.00 |
| R2/2027 | 2027-03-17 | 12.75 | 13.25 | -0.50 | 12.00 a 14.00 | 12.75 |
| R3/2027 | 2027-04-28 | 12.50 | 13.00 | -0.50 | 11.50 a 14.00 | 12.50 |
| R4/2027 | 2027-06-16 | 12.25 | 13.00 | -0.75 | 10.75 a 14.00 | 12.25 |
| R5/2027 | 2027-08-04 | 12.00 | 12.50 | -0.50 | 10.25 a 14.00 | 12.00 |
| R6/2027 | 2027-09-22 | 12.00 | 12.50 | -0.50 | 9.75 a 14.00 | 12.00 |

### expc_focus_periodo (Selic)

Último dado 2026-10-23 (4 dias antes do corte) · A: `A/expc_focus_periodo__selic.csv.gz`

Unidade: %. Mediana da pesquisa (janela de 30 dias).

| Ano | Mediana (2026-10-23) | 4 sem. antes (2026-09-25) | 13 sem. antes (2026-07-24) | Δ 4 sem. | Ciclo ant. (2026-10-22) | Respondentes |
|---|---|---|---|---|---|---|
| 2026 | 13.25 | 13.50 | 14.00 | -0.25 | 13.25 | 137 |
| 2027 | 11.75 | 12.00 | 12.00 | -0.25 | 12.00 | 136 |
| 2028 | 10.00 | 10.50 | 10.50 | -0.50 | 10.25 | 115 |
| 2029 | 10.00 | 10.00 | 10.00 | +0.00 | 10.00 | 110 |

### expc_focus_periodo (IPCA)

Último dado 2026-10-23 (4 dias antes do corte) · A: `A/expc_focus_periodo__ipca.csv.gz`

Unidade: %. Mediana da pesquisa (janela de 30 dias).

| Ano | Mediana (2026-10-23) | 4 sem. antes (2026-09-25) | 13 sem. antes (2026-07-24) | Δ 4 sem. | Ciclo ant. (2026-10-22) | Respondentes |
|---|---|---|---|---|---|---|
| 2026 | 5.19 | 4.99 | 5.12 | +0.20 | 5.21 | 142 |
| 2027 | 4.34 | 4.31 | 4.22 | +0.03 | 4.30 | 142 |
| 2028 | 3.75 | 3.80 | 3.80 | -0.05 | 3.70 | 124 |
| 2029 | 3.50 | 3.50 | 3.50 | -0.00 | 3.50 | 116 |

## iv. Endógeno de externo (leitura enxuta)

### cmb_dollar_index

Último dado 2026-10-27 (no corte) · A: `A/cmb_dollar_index.csv.gz`

| Série | Unidade | Data | Último | Δ% 1m | Δ% 3m | Δ% 12m | Δ% desde o ciclo ant. |
|---|---|---|---|---|---|---|---|
| DXY | índice | 2026-10-27 | 102.21 | +1.2 | +0.7 | +3.5 | +0.6 |

### cmb_dollar_index_em

Último dado 2026-10-23 (4 dias antes do corte) · A: `A/cmb_dollar_index_em.csv.gz`

| Série | Unidade | Data | Último | Δ% 1m | Δ% 3m | Δ% 12m | Δ% desde o ciclo ant. |
|---|---|---|---|---|---|---|---|
| Dólar contra emergentes (FRED) | índice | 2026-10-23 | 130.21 | +1.6 | +0.6 | -1.2 | -0.1 |

### cmb_equity_us

Último dado 2026-10-27 (no corte) · A: `A/cmb_equity_us.csv.gz`

| Série | Unidade | Data | Último | Δ% 1m | Δ% 3m | Δ% 12m | Δ% desde o ciclo ant. |
|---|---|---|---|---|---|---|---|
| S&P 500 | pontos | 2026-10-27 | 7717 | -0.3 | +4.1 | +12.2 | +0.7 |

### us_interest_rate

Último dado 2026-10-27 (no corte) · A: `A/us_interest_rate.csv.gz`

| Série | Unidade | Data | Último | Δ 1m | Δ 3m | Δ 12m | Δ desde o ciclo ant. |
|---|---|---|---|---|---|---|---|
| Fed Funds, meta (ponto médio) | % a.a. | 2026-10-27 | 3.88 | +0.00 | +0.25 | -0.25 | +0.00 |
| Treasury 2 anos | % a.a. | 2026-10-23 | 4.69 | -0.16 | +0.32 | +1.21 | +0.04 |
| Treasury 10 anos | % a.a. | 2026-10-23 | 5.00 | -0.11 | +0.29 | +0.99 | +0.04 |

### cmb_real_rates

Último dado 2026-08-01 (87 dias antes do corte) · A: `A/cmb_real_rates.csv.gz`

| Série | Unidade | Data | Último | Δ 1m | Δ 3m | Δ 12m | Δ desde o ciclo ant. |
|---|---|---|---|---|---|---|---|
| BR, juro real ex-post | % a.a. | 2026-08-01 | 9.78 | -0.03 | +0.00 | -0.09 | sem dado novo |
| MX, juro real ex-post | % a.a. | 2026-08-01 | 3.24 | -0.14 | +0.68 | -0.94 | sem dado novo |
| CL, juro real ex-post | % a.a. | 2026-08-01 | 0.37 | -0.61 | -0.20 | -0.35 | sem dado novo |
| CO, juro real ex-post | % a.a. | 2026-08-01 | 5.76 | -0.22 | +0.35 | +1.60 | sem dado novo |
| PE, juro real ex-post | % a.a. | 2026-08-01 | -0.19 | -0.37 | -0.53 | -3.58 | sem dado novo |

### comm_brent

Último dado 2026-10-20 (7 dias antes do corte) · A: `A/comm_brent.csv.gz`

| Série | Unidade | Data | Último | Δ% 1m | Δ% 3m | Δ% 12m | Δ% desde o ciclo ant. |
|---|---|---|---|---|---|---|---|
| Brent | US$/barril | 2026-10-20 | 115.22 | -3.7 | +32.5 | +89.8 | sem dado novo |

### comm_icbr_usd

Último dado 2026-09-01 (56 dias antes do corte) · A: `A/comm_icbr_usd.csv.gz`

| Série | Unidade | Data | Último | Δ% 1m | Δ% 3m | Δ% 12m | Δ% desde o ciclo ant. |
|---|---|---|---|---|---|---|---|
| IC-Br em dólar | índice | 2026-09-01 | 205.70 | +1.7 | +4.1 | +12.8 | sem dado novo |
| IC-Br agropecuária | índice | 2026-09-01 | 201.80 | +0.3 | +3.3 | +0.7 | sem dado novo |
| IC-Br metal | índice | 2026-09-01 | 335.06 | -0.6 | +0.7 | +42.2 | sem dado novo |
| IC-Br energia | índice | 2026-09-01 | 96.00 | +10.6 | +11.2 | +29.2 | sem dado novo |

## v. Endógeno de inflação (leitura enxuta)

### inflc_agregados

Último dado 2026-10-01 (26 dias antes do corte) · A: `A/inflc_agregados.csv.gz`

| Série | Mês | Último mês | Acum. 3m | Acum. 12m | Acum. 12m, 3 meses antes |
|---|---|---|---|---|---|
| IPCA | 2026-09 | 0.82 | 0.57 | 4.58 | 4.64 |
| Livres | 2026-09 | 0.55 | 0.55 | 4.68 | 4.31 |
| Administrados | 2026-09 | 1.59 | 0.59 | 4.14 | 5.52 |
| Comercializáveis | 2026-09 | 0.20 | 0.41 | 2.65 | 2.15 |
| Não comercializáveis | 2026-09 | 0.80 | 0.67 | 6.22 | 5.92 |
| Serviços | 2026-09 | 0.61 | 1.18 | 5.97 | 5.90 |
| Industriais | 2026-09 | 0.17 | 0.50 | 3.07 | 2.76 |

## vi. Endógeno de fiscal (leitura enxuta)

### fisc_nfsp

Último dado 2026-08-01 (87 dias antes do corte) · A: `A/fisc_nfsp.csv.gz`

| Série | Unidade | Data | Último | Δ 1m | Δ 3m | Δ 12m | Δ desde o ciclo ant. |
|---|---|---|---|---|---|---|---|
| Resultado primário, 12m (+ = superávit) | % do PIB | 2026-08-01 | -0.62 | +0.05 | +0.52 | -0.43 | sem dado novo |
| Resultado nominal, 12m | % do PIB | 2026-08-01 | -9.48 | -0.13 | +0.13 | -1.69 | sem dado novo |
| Juros nominais, 12m | % do PIB | 2026-08-01 | 8.86 | +0.18 | +0.38 | +1.25 | sem dado novo |

### fisc_divida

Último dado 2026-08-01 (87 dias antes do corte) · A: `A/fisc_divida.csv.gz`

| Série | Unidade | Data | Último | Δ 1m | Δ 3m | Δ 12m | Δ desde o ciclo ant. |
|---|---|---|---|---|---|---|---|
| Dívida bruta do governo geral | % do PIB | 2026-08-01 | 82.9 | +0.3 | +1.8 | +5.6 | sem dado novo |
| Dívida líquida do setor público | % do PIB | 2026-08-01 | 69.3 | +0.2 | +1.4 | +5.2 | sem dado novo |

### cmb_risco_pais

Último dado 2026-10-26 (1 dia antes do corte) · A: `A/cmb_risco_pais.csv.gz`

| Série | Unidade | Data | Último | Δ 1m | Δ 3m | Δ 12m | Δ desde o ciclo ant. |
|---|---|---|---|---|---|---|---|
| CDS 5 anos Brasil | p.b. | 2026-10-26 | 137 | +13 | +13 | -4 | +19 |

## vii. Endógeno de atividade (leitura enxuta)

### atv_pib_usd

Último dado 2026-09-01 (56 dias antes do corte) · A: `A/atv_pib_usd.csv.gz`

| Série | Unidade | Último mês | Soma 3m | Soma 12m | Soma 12m, um ano antes |
|---|---|---|---|---|---|
| PIB mensal em dólar | US$ bi | 220.79 (2026-09) | 670.57 | 2573.70 | 2197.80 |

## Leituras combinadas

### O real e os pares

Moeda local por dólar: Δ% positivo = a moeda se desvalorizou. Volatilidade realizada em % ao ano. O peso chileno e o colombiano entram com a taxa oficial do dia útil seguinte, que é a formada no dia anterior: a coluna Data é o dia da formação, como no real. Juro de política dos pares pelo BIS (mensal, com defasagem: data ao lado); o do Brasil é a Selic vigente. Carry = juro de política menos a meta do Fed na mesma data.

| Moeda | Data | Δ% 1m | Δ% 3m | Δ% 12m | Δ% desde o ciclo ant. | Vol. 21d | Vol. 63d | Pctl vol. 63d 10a | Juro de política | Carry vs Fed (p.p.) | Carry / vol. 63d |
|---|---|---|---|---|---|---|---|---|---|---|---|
| BRL | 2026-10-26 | +5.8 | +8.6 | +2.2 | +9.2 | 35.7 | 21.4 | 96 | 13.75 (2026-09-16) | 10.12 | 0.47 |
| MXN | 2026-10-20 | +7.8 | +5.9 | +0.7 | +0.0 | 10.9 | 7.8 | 15 | 6.50 (2026-08-01) | 2.88 | 0.37 |
| CLP | 2026-10-19 | +2.4 | +5.1 | +2.2 | +0.0 | 10.4 | 9.6 | 36 | 4.50 (2026-08-01) | 0.88 | 0.09 |
| COP | 2026-10-15 | +2.3 | -2.0 | -18.8 | +0.0 | 15.8 | 14.8 | 85 | 12.00 (2026-08-01) | 8.38 | 0.57 |
| PEN | 2026-10-19 | +2.5 | +1.0 | +1.4 | +0.0 | 6.6 | 4.6 | 40 | 4.25 (2026-08-01) | 0.62 | 0.14 |
