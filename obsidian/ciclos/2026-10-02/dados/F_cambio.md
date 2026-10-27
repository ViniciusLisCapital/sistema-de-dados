# F(A) — cambio — ciclo 2026-10-02

Gerado em 2026-10-22 16:18. Dados do banco até 2026-10-02, fixos durante o ciclo. Sem ciclo anterior.

Os dados brutos (A) estão em `A/`, um arquivo por tabela; as funções G leem de lá e o código delas fica em `G/`. Nada aqui é opinião: é a mesma conta em todo ciclo.

Como ler:
- **Δ% 1m/3m/12m**: variação contra o último valor de 1, 3 e 12 meses antes da última data da série; numa série trimestral, **1t/4t**: contra 1 e 4 trimestres antes.
- **Δ**: diferença na unidade da série (p.p. quando a série é %, p.b. quando é p.b.).
- **Pctl**: posição do último valor no histórico, de 0 (o menor já visto) a 100 (o maior). "10a" = últimos 10 anos.
- **Soma 3m/12m**: soma dos últimos 3 e 12 meses completos; o mês em curso aparece à parte e não entra nas somas.
- **Acum.**: variação composta.

## i. Endógeno (leitura completa)

### cmb_ptax

Último dado 2026-10-02 (no corte) · A: `A/cmb_ptax.csv.gz`

| Série | Unidade | Data | Último | Δ% 1m | Δ% 3m | Δ% 12m | Pctl 10a | Pctl hist. | Pctl Δ12m hist. | Mín–máx 10a |
|---|---|---|---|---|---|---|---|---|---|---|
| PTAX venda | R$/US$ | 2026-10-02 | 5.2238 | +1.9 | +0.6 | -2.3 | 64 | 89 | 33 | 3.0510 a 6.2086 |

| Série | Unidade | Data | Média 1m | Média 3m | Média 12m | Pctl média 1m 10a |
|---|---|---|---|---|---|---|
| Volume interbancário D+1 | US$ mi/dia | 2026-10-02 | 327 | 266 | 381 | 68 |
| Volume interbancário D+2 | US$ mi/dia | 2026-10-02 | 1228 | 975 | 1573 | 44 |

### cmb_cambio_contratado

Último dado 2026-10-02 (no corte) · A: `A/cmb_cambio_contratado.csv.gz`

| Série | Unidade | Último mês | Soma 3m | Soma 12m | Soma 12m, um ano antes | Mês em curso | Pctl soma 12m hist. |
|---|---|---|---|---|---|---|---|
| Saldo total (comercial + financeiro) | US$ bi | -5.20 (2026-09) | -7.17 | -4.01 | -42.67 | 0.80 (até 02/10) | 40 |
| Comercial, saldo | US$ bi | 2.13 (2026-09) | 11.76 | 58.26 | 46.33 | 0.84 (até 02/10) | 93 |
| Comercial, exportação | US$ bi | 26.34 (2026-09) | 81.09 | 309.00 | 286.53 | 2.59 (até 02/10) | 100 |
| Comercial, importação | US$ bi | 24.21 (2026-09) | 69.34 | 250.74 | 240.20 | 1.76 (até 02/10) | 100 |
| Financeiro, saldo | US$ bi | -7.33 (2026-09) | -18.92 | -62.27 | -89.00 | -0.04 (até 02/10) | 18 |
| Financeiro, compras | US$ bi | 63.35 (2026-09) | 160.51 | 686.26 | 581.45 | 6.21 (até 02/10) | 100 |
| Financeiro, vendas | US$ bi | 70.68 (2026-09) | 179.43 | 748.53 | 670.44 | 6.25 (até 02/10) | 100 |
| Financeiro: serviços (mensal) | US$ bi | -2.61 (2026-09) | -8.05 | -28.30 | -30.37 |  | 68 |
| Financeiro: rendas (mensal) | US$ bi | -4.60 (2026-09) | -12.31 | -66.03 | -55.76 |  | 6 |
| Financeiro: capitais brasileiros (mensal) | US$ bi | -5.04 (2026-09) | -11.38 | -49.62 | -40.59 |  | 3 |
| Financeiro: capitais estrangeiros (mensal) | US$ bi | 4.92 (2026-09) | 12.82 | 81.68 | 37.72 |  | 66 |

### cmb_balanco_pagmt

Último dado 2026-08-01 (62 dias antes do corte) · A: `A/cmb_balanco_pagmt.csv.gz`

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

Último dado 2026-08-01 (62 dias antes do corte) · A: `A/cmb_comex_fator_agregado.csv.gz`

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

Último dado 2026-09-01 (31 dias antes do corte) · A: `A/cmb_comex_pais.csv.gz`

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

Último dado 2026-08-01 (62 dias antes do corte) · A: `A/cmb_comex_produto.csv.gz`

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

Último dado 2026-10-02 (no corte) · A: `A/cmb_reservas_bc.csv.gz`

| Série | Unidade | Data | Último | Δ 1m | Δ 3m | Δ 12m | Pctl 10a | Pctl hist. | Mín–máx 10a |
|---|---|---|---|---|---|---|---|---|---|
| Reservas internacionais | US$ bi | 2026-10-02 | 362.8 | -9.1 | -7.6 | +5.8 | 55 | 71 | 323.5 a 390.5 |
| Reservas, conceito liquidez | US$ bi | 2026-10-02 | 366.8 | -7.1 | -5.6 | -1.5 | 50 | 49 | 327.4 a 401.6 |
| Swap cambial do BC, posição (− = vendido) | US$ bi | 2026-08-01 | -91.6 | +1.3 | +3.2 | +9.8 | 46 | 34 | -102.7 a -17.8 |
| Posição à vista dos bancos | US$ bi | 2026-09-01 | -26.2 | -4.1 | -4.8 | +2.0 | 24 | 9 | -42.4 a 4.6 |

| Série | Unidade | Último mês | Soma 3m | Soma 12m | Soma 12m, um ano antes | Mês em curso | Pctl soma 12m hist. |
|---|---|---|---|---|---|---|---|
| Intervenção à vista (+ compra, − venda) | US$ bi | -2.00 (2026-09) | -3.00 | -8.00 | -22.57 | 0.00 (até 02/10) | 14 |
| Leilões de linha (+ compra, − venda) | US$ bi | -2.00 (2026-09) | 0.05 | 7.25 | -11.25 | 0.00 (até 02/10) | 92 |

### cmb_cot_fx

Último dado 2026-09-29 (3 dias antes do corte) · A: `A/cmb_cot_fx.csv.gz`

| Série | Unidade | Data | Último | Δ 1m | Δ 3m | Δ 12m | Pctl 10a | Pctl hist. | Mín–máx 10a |
|---|---|---|---|---|---|---|---|---|---|
| BRL: fundos alavancados, líquido | contratos | 2026-09-29 | 9553 | -5160 | +1676 | -7581 | 77 | 78 | -40335 a 32847 |
| BRL: asset managers, líquido | contratos | 2026-09-29 | 67015 | +18136 | +15178 | -1313 | 96 | 97 | -57523 a 78334 |
| BRL: dealers, líquido | contratos | 2026-09-29 | -59755 | -13987 | +6357 | -4302 | 7 | 5 | -83394 a 59543 |
| BRL: outros reportáveis, líquido | contratos | 2026-09-29 | -20549 | +2111 | -23601 | +12657 | 5 | 3 | -48451 a 12141 |
| BRL: não reportáveis, líquido | contratos | 2026-09-29 | 3736 | -1100 | +390 | +539 | 92 | 95 | -5527 a 14033 |
| BRL: posições em aberto | contratos | 2026-09-29 | 146704 | +15151 | +42420 | +12386 | 99 | 100 | 10333 a 152424 |
| MXN: fundos alavancados, líquido | contratos | 2026-09-29 | 80587 | +11683 | +24056 | +45095 | 97 | 93 | -96547 a 114016 |
| MXN: asset managers, líquido | contratos | 2026-09-29 | 16251 | -52339 | -18718 | -29747 | 5 | 16 | -18603 a 176493 |
| MXN: dealers, líquido | contratos | 2026-09-29 | -42428 | +77649 | +26508 | +45934 | 79 | 60 | -234567 a 48410 |
| MXN: outros reportáveis, líquido | contratos | 2026-09-29 | -56605 | -33171 | -30599 | -58571 | 15 | 9 | -111774 a 6128 |
| MXN: não reportáveis, líquido | contratos | 2026-09-29 | 2195 | -3822 | -1247 | -2711 | 29 | 39 | -10152 a 13919 |
| MXN: posições em aberto | contratos | 2026-09-29 | 274821 | -11608 | +76233 | +98814 | 91 | 94 | 94469 a 376712 |

### cmb_reer

Último dado 2026-09-01 (31 dias antes do corte) · A: `A/cmb_reer.csv.gz`

| Série | Unidade | Data | Último | Δ% 1m | Δ% 3m | Δ% 12m | Pctl 10a | Pctl hist. | Pctl Δ12m hist. | Mín–máx 10a |
|---|---|---|---|---|---|---|---|---|---|---|
| BR, real efetivo | índice 2020=100 | 2026-09-01 | 117.18 | +0.6 | -0.9 | +4.5 | 53 | 36 | 60 | 90.32 a 151.33 |
| BR, nominal efetivo | índice 2020=100 | 2026-09-01 | 113.48 | +0.3 | -0.4 | +3.8 | 52 | 19 | 67 | 88.28 a 146.37 |
| MX, real efetivo | índice 2020=100 | 2026-09-01 | 140.31 | -1.2 | -0.0 | +6.9 | 92 | 76 | 69 | 88.88 a 144.59 |
| MX, nominal efetivo | índice 2020=100 | 2026-09-01 | 127.52 | -1.1 | +0.2 | +6.5 | 89 | 31 | 84 | 89.71 a 134.70 |
| CL, real efetivo | índice 2020=100 | 2026-09-01 | 98.94 | -3.2 | -5.0 | +0.1 | 15 | 7 | 53 | 92.25 a 117.27 |
| CL, nominal efetivo | índice 2020=100 | 2026-09-01 | 91.73 | -3.1 | -5.1 | -0.5 | 3 | 1 | 53 | 87.75 a 117.49 |
| CO, real efetivo | índice 2020=100 | 2026-09-01 | 144.72 | -1.6 | +9.7 | +24.8 | 99 | 98 | 97 | 83.28 a 147.02 |
| CO, nominal efetivo | índice 2020=100 | 2026-09-01 | 121.37 | -1.5 | +9.7 | +21.3 | 99 | 40 | 97 | 79.19 a 123.18 |

### cmb_termos_troca

Último dado 2026-07-01 (93 dias antes do corte) · A: `A/cmb_termos_troca.csv.gz`

| Série | Unidade | Data | Último | Δ% 1m | Δ% 3m | Δ% 12m | Pctl 10a | Pctl hist. | Pctl Δ12m hist. | Mín–máx 10a |
|---|---|---|---|---|---|---|---|---|---|---|
| Termos de troca (Funcex) | índice | 2026-07-01 | 111.35 | -1.8 | -2.7 | +1.5 | 75 | 90 | 58 | 93.15 a 122.43 |

### cmb_fx_latam

Último dado 2026-10-02 (no corte) · A: `A/cmb_fx_latam.csv.gz`

**Atenção:** O peso chileno e o colombiano datados em um dia são a taxa oficial formada no dia útil anterior: para comparar com o real ou com o dólar no mesmo dia, leia a taxa do dia útil seguinte. A tabela abaixo está como a fonte publica.

| Série | Unidade | Data | Último | Δ% 1m | Δ% 3m | Δ% 12m | Pctl 10a | Pctl hist. | Pctl Δ12m hist. | Mín–máx 10a |
|---|---|---|---|---|---|---|---|---|---|---|
| Peso mexicano | MXN/US$ | 2026-10-02 | 18.3346 | +7.8 | +4.4 | -0.2 | 25 | 71 | 41 | 16.3125 a 25.1039 |
| Peso chileno | CLP/US$ | 2026-10-02 | 983.84 | +5.0 | +6.1 | +2.6 | 98 | 99 | 58 | 588.28 a 1042.97 |
| Peso colombiano | COP/US$ | 2026-10-02 | 3307.73 | +3.9 | -2.8 | -15.0 | 31 | 74 | 7 | 2705.34 a 5061.21 |
| Sol peruano | PEN/US$ | 2026-10-02 | 3.4395 | +2.5 | +1.0 | -1.2 | 44 | 62 | 71 | 3.2070 a 4.1340 |

### diferenciais_juros

Último dado 2026-10-01 (1 dia antes do corte) · A: `A/diferenciais_juros.csv.gz`

| Série | Unidade | Data | Último | Δ 1m | Δ 3m | Δ 12m | Pctl 10a | Pctl hist. | Mín–máx 10a |
|---|---|---|---|---|---|---|---|---|---|
| Selic | % a.a. | 2026-10-01 | 13.75 | +0.00 | -0.50 | -1.25 | 83 | 62 | 2.00 a 15.00 |
| Fed Funds | % a.a. | 2026-09-01 | 3.75 | +0.12 | +0.12 | -0.47 | 69 | 62 | 0.05 a 5.33 |
| Diferencial nominal (Selic − Fed Funds) | p.p. | 2026-09-01 | 10.00 | -0.37 | -0.62 | -0.78 | 72 | 46 | 1.90 a 13.85 |
| IPCA 12m | % | 2026-09-01 | 4.58 | +0.36 | -0.06 | -0.59 | 56 | 30 | 1.88 a 12.13 |
| CPI EUA 12m | % | 2026-09-01 | 3.72 | +0.36 | +0.25 | +0.69 | 76 | 86 | 0.20 a 8.98 |
| Juro real ex-post Brasil | % a.a. | 2026-09-01 | 9.17 | -0.61 | -0.44 | -0.66 | 83 | 67 | -4.74 a 11.19 |
| Juro real ex-post EUA | % a.a. | 2026-09-01 | 0.03 | -0.24 | -0.13 | -1.16 | 59 | 51 | -8.37 a 2.72 |
| Diferencial real ex-post | p.p. | 2026-09-01 | 9.14 | -0.37 | -0.31 | +0.50 | 81 | 72 | -1.61 a 12.21 |

## ii. Endógeno de política monetária (leitura enxuta)

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

### pm_copom_projecoes

Último dado 2026-09-24 (8 dias antes do corte) · A: `A/pm_copom_projecoes.csv.gz`

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

Último dado 2026-10-02 (no corte) · A: `A/br_di_grade.csv.gz`

Pregão de 2026-10-02. DI × pré, base 252, nos prazos redondos.

| Prazo | Taxa (% a.a.) | Δ 1m (p.b.) | Δ 3m (p.b.) | Δ 12m (p.b.) |
|---|---|---|---|---|
| 1 mês | 13.65 | -12 | -50 | -125 |
| 3 meses | 13.53 | -10 | -50 | -137 |
| 6 meses | 13.50 | -4 | -55 | -133 |
| 1 ano | 13.50 | -11 | -70 | -85 |
| 2 anos | 13.69 | -19 | -64 | +12 |
| 3 anos | 13.89 | -23 | -58 | +51 |
| 5 anos | 14.04 | -24 | -47 | +50 |
| 10 anos | 14.16 | -21 | -30 | +54 |

Selic precificada na curva em cada reunião (meta vigente 13.75%). É preço, com prêmio de prazo, não previsão. Reuniões só até onde vai o calendário oficial (2027-12-08).

| Reunião | Selic na curva (% a.a.) | Passo implícito (p.b.) | 1 mês antes (2026-09-02) | Δ 1 mês (p.b.) |
|---|---|---|---|---|
| 2026-11-04 | 13.60 | -15 | 13.58 | +2 |
| 2026-12-09 | 13.54 | -6 | 13.53 | +1 |
| 2027-01-27 | 13.55 | +1 | 13.58 | -3 |
| 2027-03-17 | 13.57 | +1 | 13.66 | -9 |
| 2027-04-28 | 13.57 | +1 | 13.73 | -16 |
| 2027-06-16 | 13.58 | +1 | 13.80 | -22 |
| 2027-08-04 | 13.61 | +3 | 13.87 | -27 |
| 2027-09-22 | 13.68 | +7 | 13.97 | -29 |
| 2027-10-27 | 13.79 | +11 | 14.09 | -30 |
| 2027-12-08 | 13.95 | +16 | 14.24 | -30 |

### inflc_meta

Último dado 2026-01-01 (274 dias antes do corte) · A: `A/inflc_meta.csv.gz`

| Ano | Meta (%) |
|---|---|
| 2024 | 3.00 |
| 2025 | 3.00 |
| 2026 | 3.00 |

## iii. Endógeno de expectativas (leitura enxuta)

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

### expc_focus_periodo (Selic)

Último dado 2026-10-02 (no corte) · A: `A/expc_focus_periodo__selic.csv.gz`

Unidade: %. Mediana da pesquisa (janela de 30 dias).

| Ano | Mediana (2026-10-02) | 4 sem. antes (2026-09-04) | 13 sem. antes (2026-07-03) | Δ 4 sem. | Respondentes |
|---|---|---|---|---|---|
| 2026 | 13.50 | 13.75 | 14.00 | -0.25 | 139 |
| 2027 | 12.00 | 12.00 | 12.00 | +0.00 | 138 |
| 2028 | 10.50 | 10.50 | 10.50 | +0.00 | 115 |
| 2029 | 10.00 | 10.00 | 10.00 | +0.00 | 108 |

### expc_focus_periodo (IPCA)

Último dado 2026-10-02 (no corte) · A: `A/expc_focus_periodo__ipca.csv.gz`

Unidade: %. Mediana da pesquisa (janela de 30 dias).

| Ano | Mediana (2026-10-02) | 4 sem. antes (2026-09-04) | 13 sem. antes (2026-07-03) | Δ 4 sem. | Respondentes |
|---|---|---|---|---|---|
| 2026 | 5.01 | 5.00 | 5.30 | +0.01 | 144 |
| 2027 | 4.30 | 4.29 | 4.18 | +0.01 | 144 |
| 2028 | 3.80 | 3.80 | 3.70 | +0.00 | 118 |
| 2029 | 3.51 | 3.50 | 3.50 | +0.01 | 110 |

## iv. Endógeno de externo (leitura enxuta)

### cmb_dollar_index

Último dado 2026-10-02 (no corte) · A: `A/cmb_dollar_index.csv.gz`

| Série | Unidade | Data | Último | Δ% 1m | Δ% 3m | Δ% 12m |
|---|---|---|---|---|---|---|
| DXY | índice | 2026-10-02 | 101.93 | +2.4 | +1.1 | +4.2 |

### cmb_dollar_index_em

Último dado 2026-10-02 (no corte) · A: `A/cmb_dollar_index_em.csv.gz`

| Série | Unidade | Data | Último | Δ% 1m | Δ% 3m | Δ% 12m |
|---|---|---|---|---|---|---|
| Dólar contra emergentes (FRED) | índice | 2026-10-02 | 129.71 | +2.4 | +0.2 | -1.5 |

### cmb_equity_us

Último dado 2026-10-02 (no corte) · A: `A/cmb_equity_us.csv.gz`

| Série | Unidade | Data | Último | Δ% 1m | Δ% 3m | Δ% 12m |
|---|---|---|---|---|---|---|
| S&P 500 | pontos | 2026-10-02 | 7723 | +0.7 | +3.2 | +15.0 |

### us_interest_rate

Último dado 2026-10-02 (no corte) · A: `A/us_interest_rate.csv.gz`

| Série | Unidade | Data | Último | Δ 1m | Δ 3m | Δ 12m |
|---|---|---|---|---|---|---|
| Fed Funds, meta (ponto médio) | % a.a. | 2026-10-02 | 3.88 | +0.25 | +0.25 | -0.25 |
| Treasury 2 anos | % a.a. | 2026-10-02 | 4.83 | +0.44 | +0.69 | +1.28 |
| Treasury 10 anos | % a.a. | 2026-10-02 | 5.28 | +0.49 | +0.79 | +1.18 |

### cmb_real_rates

Último dado 2026-08-01 (62 dias antes do corte) · A: `A/cmb_real_rates.csv.gz`

| Série | Unidade | Data | Último | Δ 1m | Δ 3m | Δ 12m |
|---|---|---|---|---|---|---|
| BR, juro real ex-post | % a.a. | 2026-08-01 | 9.78 | -0.03 | +0.00 | -0.09 |
| MX, juro real ex-post | % a.a. | 2026-08-01 | 3.24 | -0.14 | +0.68 | -0.94 |
| CL, juro real ex-post | % a.a. | 2026-08-01 | 0.37 | -0.61 | -0.20 | -0.35 |
| CO, juro real ex-post | % a.a. | 2026-08-01 | 5.76 | -0.22 | +0.35 | +1.60 |
| PE, juro real ex-post | % a.a. | 2026-08-01 | -0.19 | -0.37 | -0.53 | -3.58 |

### comm_brent

Último dado 2026-10-02 (no corte) · A: `A/comm_brent.csv.gz`

| Série | Unidade | Data | Último | Δ% 1m | Δ% 3m | Δ% 12m |
|---|---|---|---|---|---|---|
| Brent | US$/barril | 2026-10-02 | 135.51 | +38.9 | +97.7 | +107.1 |

### comm_icbr_usd

Último dado 2026-09-01 (31 dias antes do corte) · A: `A/comm_icbr_usd.csv.gz`

| Série | Unidade | Data | Último | Δ% 1m | Δ% 3m | Δ% 12m |
|---|---|---|---|---|---|---|
| IC-Br em dólar | índice | 2026-09-01 | 205.70 | +1.7 | +4.1 | +12.8 |
| IC-Br agropecuária | índice | 2026-09-01 | 201.80 | +0.3 | +3.3 | +0.7 |
| IC-Br metal | índice | 2026-09-01 | 335.06 | -0.6 | +0.7 | +42.2 |
| IC-Br energia | índice | 2026-09-01 | 96.00 | +10.6 | +11.2 | +29.2 |

## v. Endógeno de inflação (leitura enxuta)

### inflc_agregados

Último dado 2026-09-01 (31 dias antes do corte) · A: `A/inflc_agregados.csv.gz`

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

Último dado 2026-08-01 (62 dias antes do corte) · A: `A/fisc_nfsp.csv.gz`

| Série | Unidade | Data | Último | Δ 1m | Δ 3m | Δ 12m |
|---|---|---|---|---|---|---|
| Resultado primário, 12m (+ = superávit) | % do PIB | 2026-08-01 | -0.62 | +0.05 | +0.52 | -0.43 |
| Resultado nominal, 12m | % do PIB | 2026-08-01 | -9.48 | -0.13 | +0.13 | -1.69 |
| Juros nominais, 12m | % do PIB | 2026-08-01 | 8.86 | +0.18 | +0.38 | +1.25 |

### fisc_divida

Último dado 2026-08-01 (62 dias antes do corte) · A: `A/fisc_divida.csv.gz`

| Série | Unidade | Data | Último | Δ 1m | Δ 3m | Δ 12m |
|---|---|---|---|---|---|---|
| Dívida bruta do governo geral | % do PIB | 2026-08-01 | 82.9 | +0.3 | +1.8 | +5.6 |
| Dívida líquida do setor público | % do PIB | 2026-08-01 | 69.3 | +0.2 | +1.4 | +5.2 |

### cmb_risco_pais

Último dado 2026-10-02 (no corte) · A: `A/cmb_risco_pais.csv.gz`

| Série | Unidade | Data | Último | Δ 1m | Δ 3m | Δ 12m |
|---|---|---|---|---|---|---|
| CDS 5 anos Brasil | p.b. | 2026-10-02 | 131 | +10 | +6 | -5 |

## vii. Endógeno de atividade (leitura enxuta)

### atv_pib_usd

Último dado 2026-09-01 (31 dias antes do corte) · A: `A/atv_pib_usd.csv.gz`

| Série | Unidade | Último mês | Soma 3m | Soma 12m | Soma 12m, um ano antes |
|---|---|---|---|---|---|
| PIB mensal em dólar | US$ bi | 220.79 (2026-09) | 670.57 | 2573.70 | 2197.80 |

## Leituras combinadas

### O real e os pares

Moeda local por dólar: Δ% positivo = a moeda se desvalorizou. Volatilidade realizada em % ao ano. O peso chileno e o colombiano entram com a taxa oficial do dia útil seguinte, que é a formada no dia anterior: a coluna Data é o dia da formação, como no real. Juro de política dos pares pelo BIS (mensal, com defasagem: data ao lado); o do Brasil é a Selic vigente. Carry = juro de política menos a meta do Fed na mesma data.

| Moeda | Data | Δ% 1m | Δ% 3m | Δ% 12m | Vol. 21d | Vol. 63d | Pctl vol. 63d 10a | Juro de política | Carry vs Fed (p.p.) | Carry / vol. 63d |
|---|---|---|---|---|---|---|---|---|---|---|
| BRL | 2026-10-02 | +1.9 | +0.6 | -2.3 | 9.2 | 7.8 | 4 | 13.75 (2026-09-16) | 10.12 | 1.29 |
| MXN | 2026-10-02 | +7.8 | +4.4 | -0.2 | 7.3 | 6.4 | 5 | 6.50 (2026-08-01) | 2.88 | 0.45 |
| CLP | 2026-10-01 | +5.0 | +6.1 | +2.6 | 10.9 | 9.4 | 34 | 4.50 (2026-08-01) | 0.88 | 0.09 |
| COP | 2026-10-01 | +3.9 | -2.8 | -15.0 | 13.7 | 14.6 | 84 | 12.00 (2026-08-01) | 8.38 | 0.57 |
| PEN | 2026-10-02 | +2.5 | +1.0 | -1.2 | 6.2 | 4.5 | 38 | 4.25 (2026-08-01) | 0.62 | 0.14 |
