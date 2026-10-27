# F(A) — externo — ciclo 2026-10-02

Gerado em 2026-10-22 16:21. Dados do banco até 2026-10-02, fixos durante o ciclo. Sem ciclo anterior.

Os dados brutos (A) estão em `A/`, um arquivo por tabela; as funções G leem de lá e o código delas fica em `G/`. Nada aqui é opinião: é a mesma conta em todo ciclo.

Como ler:
- **Δ% 1m/3m/12m**: variação contra o último valor de 1, 3 e 12 meses antes da última data da série; numa série trimestral, **1t/4t**: contra 1 e 4 trimestres antes.
- **Δ**: diferença na unidade da série (p.p. quando a série é %, p.b. quando é p.b.).
- **Pctl**: posição do último valor no histórico, de 0 (o menor já visto) a 100 (o maior). "10a" = últimos 10 anos.
- **Soma 3m/12m**: soma dos últimos 3 e 12 meses completos; o mês em curso aparece à parte e não entra nas somas.
- **Acum.**: variação composta.

## i. Endógeno (leitura completa)

### us_interest_rate

Último dado 2026-10-02 (no corte) · A: `A/us_interest_rate__curva_completa.csv.gz`

| Série | Unidade | Data | Último | Δ 1m | Δ 3m | Δ 12m | Pctl 10a | Pctl hist. | Mín–máx 10a |
|---|---|---|---|---|---|---|---|---|---|
| Fed Funds, meta (ponto médio) | % a.a. | 2026-10-02 | 3.88 | +0.25 | +0.25 | -0.25 | 71 | 51 | 0.12 a 5.38 |
| Treasury 1 mês | % a.a. | 2026-10-02 | 4.04 | +0.21 | +0.34 | -0.19 | 71 | 82 | 0.00 a 6.02 |
| Treasury 3 meses | % a.a. | 2026-10-02 | 4.19 | +0.27 | +0.37 | +0.17 | 71 | 52 | 0.00 a 5.63 |
| Treasury 6 meses | % a.a. | 2026-10-02 | 4.27 | +0.27 | +0.29 | +0.46 | 74 | 52 | 0.02 a 5.61 |
| Treasury 1 ano | % a.a. | 2026-10-02 | 4.46 | +0.30 | +0.50 | +0.84 | 82 | 45 | 0.04 a 5.49 |
| Treasury 2 anos | % a.a. | 2026-10-02 | 4.83 | +0.44 | +0.69 | +1.28 | 95 | 53 | 0.09 a 5.19 |
| Treasury 3 anos | % a.a. | 2026-10-02 | 4.96 | +0.51 | +0.80 | +1.40 | 100 | 50 | 0.10 a 5.03 |
| Treasury 5 anos | % a.a. | 2026-10-02 | 5.06 | +0.52 | +0.83 | +1.39 | 100 | 49 | 0.19 a 5.09 |
| Treasury 7 anos | % a.a. | 2026-10-02 | 5.17 | +0.51 | +0.82 | +1.31 | 100 | 46 | 0.36 a 5.19 |
| Treasury 10 anos | % a.a. | 2026-10-02 | 5.28 | +0.49 | +0.79 | +1.18 | 100 | 49 | 0.52 a 5.29 |
| Treasury 20 anos | % a.a. | 2026-10-02 | 5.67 | +0.40 | +0.68 | +1.01 | 100 | 56 | 0.87 a 5.68 |
| Treasury 30 anos | % a.a. | 2026-10-02 | 5.63 | +0.36 | +0.65 | +0.94 | 100 | 52 | 0.99 a 5.64 |

### diferenciais_juros (EUA)

Último dado 2026-09-01 (31 dias antes do corte) · A: `A/diferenciais_juros__eua.csv.gz`

| Série | Unidade | Data | Último | Δ 1m | Δ 3m | Δ 12m | Pctl 10a | Pctl hist. | Mín–máx 10a |
|---|---|---|---|---|---|---|---|---|---|
| Fed Funds efetivo, média do mês (o `ffr` do modelo) | % a.a. | 2026-09-01 | 3.75 | +0.12 | +0.12 | -0.47 | 69 | 62 | 0.05 a 5.33 |
| CPI EUA 12 meses | % | 2026-09-01 | 3.72 | +0.36 | +0.25 | +0.69 | 76 | 86 | 0.20 a 8.98 |
| Juro real ex-post EUA (Fed Funds − CPI 12m) | % a.a. | 2026-09-01 | 0.03 | -0.24 | -0.13 | -1.16 | 59 | 51 | -8.37 a 2.72 |

### inflc_cpi

Último dado 2026-09-01 (31 dias antes do corte) · A: `A/inflc_cpi.csv.gz`

**Atenção:** Outubro de 2025 não existe (o BLS não coletou durante a paralisação do governo americano); a variação de um mês que atravesse ele é calculada por G.

| Série | Unidade | Data | Último | Δ% 1m | Δ% 3m | Δ% 12m | Pctl 10a | Pctl hist. | Pctl Δ12m hist. | Mín–máx 10a |
|---|---|---|---|---|---|---|---|---|---|---|
| CPI cheio | índice, com ajuste sazonal | 2026-09-01 | 336.298 | +0.6 | +1.1 | +3.7 | 100 | 100 | 71 | 241.176 a 336.298 |
| Núcleo (sem alimentos e energia) | índice, com ajuste sazonal | 2026-09-01 | 338.896 | +0.3 | +0.8 | +2.6 | 100 | 100 | 50 | 248.842 a 338.896 |
| Bens sem alimentos e energia | índice, com ajuste sazonal | 2026-09-01 | 168.361 | +0.3 | +0.6 | +0.7 | 100 | 100 | 40 | 142.586 a 168.361 |
| Serviços sem energia | índice, com ajuste sazonal | 2026-09-01 | 448.723 | +0.4 | +0.9 | +3.2 | 100 | 100 | 41 | 312.348 a 448.723 |
| Habitação (shelter) | índice, com ajuste sazonal | 2026-09-01 | 431.908 | +0.4 | +0.8 | +3.2 | 100 | 100 | 55 | 290.369 a 431.908 |
| Alimentos | índice, com ajuste sazonal | 2026-09-01 | 350.477 | +0.0 | +0.2 | +2.5 | 100 | 100 | 48 | 247.725 a 350.477 |
| Energia | índice, com ajuste sazonal | 2026-09-01 | 337.834 | +5.2 | +5.8 | +20.4 | 99 | 100 | 93 | 180.040 a 338.639 |

### inflc_pce

Último dado 2026-08-01 (62 dias antes do corte) · A: `A/inflc_pce.csv.gz`

| Série | Unidade | Data | Último | Δ% 1m | Δ% 3m | Δ% 12m | Pctl 10a | Pctl hist. | Pctl Δ12m hist. | Mín–máx 10a |
|---|---|---|---|---|---|---|---|---|---|---|
| PCE cheio | índice 2017=100 | 2026-08-01 | 131.579 | +0.3 | +0.3 | +3.4 | 100 | 100 | 64 | 98.479 a 131.579 |
| PCE núcleo (sem alimentos e energia) | índice 2017=100 | 2026-08-01 | 130.455 | +0.2 | +0.5 | +3.0 | 100 | 100 | 58 | 98.703 a 130.455 |

### expc_inflacao

Último dado 2026-10-01 (1 dia antes do corte) · A: `A/expc_inflacao.csv.gz`

| Série | Unidade | Data | Último | Δ 1m | Δ 3m | Δ 12m | Pctl 10a | Pctl hist. | Mín–máx 10a |
|---|---|---|---|---|---|---|---|---|---|
| Inflação esperada, 1 ano | % a.a. | 2026-10-01 | 2.98 | +0.32 | +0.59 | +0.25 | 89 | 62 | -0.22 a 4.23 |
| Inflação esperada, 2 anos | % a.a. | 2026-10-01 | 2.87 | +0.23 | +0.44 | +0.37 | 97 | 61 | 0.42 a 3.18 |
| Inflação esperada, 5 anos | % a.a. | 2026-10-01 | 2.77 | +0.17 | +0.34 | +0.45 | 100 | 58 | 0.86 a 2.77 |
| Inflação esperada, 10 anos | % a.a. | 2026-10-01 | 2.73 | +0.14 | +0.29 | +0.43 | 100 | 57 | 1.16 a 2.73 |
| Inflação esperada, 30 anos | % a.a. | 2026-10-01 | 2.70 | +0.08 | +0.17 | +0.27 | 100 | 54 | 1.78 a 2.70 |

### mt_ces

Último dado 2026-09-01 (31 dias antes do corte) · A: `A/mt_ces.csv.gz`

**Atenção:** O mês mais recente é preliminar e o BLS o revisa nos dois meses seguintes.

| Série | Unidade | Data | Último | Δ 1m | Δ 3m | Δ 12m | Pctl 10a | Pctl hist. | Mín–máx 10a |
|---|---|---|---|---|---|---|---|---|---|
| Payroll, emprego total (Δ 1m = criação de vagas no mês) | mil | 2026-09-01 | 159044 | +29 | +152 | +496 | 100 | 100 | 130426 a 159044 |
| Payroll, emprego privado | mil | 2026-09-01 | 135717 | +46 | +163 | +712 | 100 | 100 | 108517 a 135717 |

| Série | Unidade | Data | Último | Δ% 1m | Δ% 3m | Δ% 12m | Pctl 10a | Pctl hist. | Pctl Δ12m hist. | Mín–máx 10a |
|---|---|---|---|---|---|---|---|---|---|---|
| Salário médio por hora, privado | US$ | 2026-09-01 | 37.81 | +0.1 | +0.6 | +3.0 | 100 | 100 | 51 | 25.77 a 37.81 |

### mt_cps

Último dado 2026-09-01 (31 dias antes do corte) · A: `A/mt_cps.csv.gz`

| Série | Unidade | Data | Último | Δ 1m | Δ 3m | Δ 12m | Pctl 10a | Pctl hist. | Mín–máx 10a |
|---|---|---|---|---|---|---|---|---|---|
| Taxa de desemprego (U-3) | % | 2026-09-01 | 4.20 | +0.10 | +0.00 | -0.20 | 63 | 23 | 3.40 a 14.80 |
| Desemprego amplo (U-6) | % | 2026-09-01 | 7.60 | -0.10 | -0.30 | -0.50 | 44 | 21 | 6.60 a 22.90 |
| Taxa de participação | % | 2026-09-01 | 61.80 | +0.20 | +0.30 | -0.70 | 21 | 40 | 60.10 a 63.30 |
| Emprego / população | % | 2026-09-01 | 59.20 | +0.10 | +0.20 | -0.50 | 22 | 53 | 51.20 a 61.10 |

### mt_jolts

Último dado 2026-08-01 (62 dias antes do corte) · A: `A/mt_jolts.csv.gz`

| Série | Unidade | Data | Último | Δ 1m | Δ 3m | Δ 12m | Pctl 10a | Pctl hist. | Mín–máx 10a |
|---|---|---|---|---|---|---|---|---|---|
| Vagas em aberto, taxa | % do emprego + vagas | 2026-08-01 | 4.30 | -0.10 | -0.20 | +0.10 | 32 | 73 | 3.40 a 7.50 |
| Contratações, taxa | % do emprego | 2026-08-01 | 3.30 | +0.10 | +0.00 | +0.10 | 16 | 23 | 3.10 a 6.10 |
| Pedidos de demissão, taxa | % do emprego | 2026-08-01 | 1.90 | +0.00 | -0.10 | -0.10 | 10 | 40 | 1.50 a 3.00 |
| Demissões, taxa | % do emprego | 2026-08-01 | 1.00 | -0.10 | -0.10 | -0.20 | 31 | 12 | 0.90 a 8.60 |
| Desempregados por vaga | razão | 2026-08-01 | 1.00 | +0.10 | +0.00 | -0.10 | 72 | 28 | 0.50 a 5.00 |

### cmb_dollar_index

Último dado 2026-10-02 (no corte) · A: `A/cmb_dollar_index.csv.gz`

| Série | Unidade | Data | Último | Δ% 1m | Δ% 3m | Δ% 12m | Pctl 10a | Pctl hist. | Pctl Δ12m hist. | Mín–máx 10a |
|---|---|---|---|---|---|---|---|---|---|---|
| DXY | índice | 2026-10-02 | 101.93 | +2.4 | +1.1 | +4.2 | 73 | 71 | 60 | 88.59 a 114.11 |

### cmb_dollar_index_em

Último dado 2026-10-02 (no corte) · A: `A/cmb_dollar_index_em.csv.gz`

| Série | Unidade | Data | Último | Δ% 1m | Δ% 3m | Δ% 12m | Pctl 10a | Pctl hist. | Pctl Δ12m hist. | Mín–máx 10a |
|---|---|---|---|---|---|---|---|---|---|---|
| Dólar contra emergentes (FRED) | índice | 2026-10-02 | 129.71 | +2.4 | +0.2 | -1.5 | 74 | 88 | 33 | 113.15 a 139.99 |

### cmb_equity_us

Último dado 2026-10-02 (no corte) · A: `A/cmb_equity_us.csv.gz`

| Série | Unidade | Data | Último | Δ% 1m | Δ% 3m | Δ% 12m | Pctl 10a | Pctl hist. | Pctl Δ12m hist. | Mín–máx 10a |
|---|---|---|---|---|---|---|---|---|---|---|
| S&P 500 | pontos | 2026-10-02 | 7723 | +0.7 | +3.2 | +15.0 | 99 | 100 | 53 | 2085 a 7799 |

### comm_icbr_usd

Último dado 2026-09-01 (31 dias antes do corte) · A: `A/comm_icbr_usd.csv.gz`

| Série | Unidade | Data | Último | Δ% 1m | Δ% 3m | Δ% 12m | Pctl 10a | Pctl hist. | Pctl Δ12m hist. | Mín–máx 10a |
|---|---|---|---|---|---|---|---|---|---|---|
| IC-Br em dólar | índice | 2026-09-01 | 205.70 | +1.7 | +4.1 | +12.8 | 99 | 100 | 72 | 86.43 a 207.70 |
| IC-Br agropecuária | índice | 2026-09-01 | 201.80 | +0.3 | +3.3 | +0.7 | 98 | 99 | 46 | 97.42 a 203.94 |
| IC-Br metal | índice | 2026-09-01 | 335.06 | -0.6 | +0.7 | +42.2 | 98 | 99 | 92 | 115.63 a 350.89 |
| IC-Br energia | índice | 2026-09-01 | 96.00 | +10.6 | +11.2 | +29.2 | 89 | 92 | 79 | 32.32 a 147.30 |

### comm_brent

Último dado 2026-10-02 (no corte) · A: `A/comm_brent.csv.gz`

| Série | Unidade | Data | Último | Δ% 1m | Δ% 3m | Δ% 12m | Pctl 10a | Pctl hist. | Pctl Δ12m hist. | Mín–máx 10a |
|---|---|---|---|---|---|---|---|---|---|---|
| Brent | US$/barril | 2026-10-02 | 135.51 | +38.9 | +97.7 | +107.1 | 100 | 100 | 98 | 9.12 a 138.21 |

### inter_interest_rate

Último dado 2026-10-02 (no corte) · A: `A/inter_interest_rate.csv.gz`

| Série | Unidade | Data | Último | Δ 1m | Δ 3m | Δ 12m | Pctl 10a | Pctl hist. | Mín–máx 10a |
|---|---|---|---|---|---|---|---|---|---|
| México, juro de política | % a.a. | 2026-10-02 | 6.50 | +0.00 | +0.00 | -1.00 | 32 | 46 | 4.00 a 11.25 |
| Chile, juro de política | % a.a. | 2026-10-02 | 4.50 | +0.00 | +0.00 | -0.25 | 61 | 52 | 0.50 a 11.25 |
| Colômbia, juro de política | % a.a. | 2026-10-02 | 12.25 | +0.25 | +0.25 | +3.00 | 88 | 81 | 1.75 a 13.25 |
| Peru, juro de política | % a.a. | 2026-10-02 | 4.25 | +0.00 | +0.00 | +0.00 | 66 | 72 | 0.25 a 7.75 |

### cmb_real_rates

Último dado 2026-08-01 (62 dias antes do corte) · A: `A/cmb_real_rates.csv.gz`

| Série | Unidade | Data | Último | Δ 1m | Δ 3m | Δ 12m | Pctl 10a | Pctl hist. | Mín–máx 10a |
|---|---|---|---|---|---|---|---|---|---|
| BR, juro de política | % a.a. | 2026-08-01 | 14.00 | -0.25 | -0.50 | -1.00 | 84 | 54 | 2.00 a 15.00 |
| BR, inflação 12m | % | 2026-08-01 | 4.22 | -0.22 | -0.50 | -0.91 | 37 | 21 | 1.88 a 12.13 |
| BR, juro real ex-post | % a.a. | 2026-08-01 | 9.78 | -0.03 | +0.00 | -0.09 | 90 | 67 | -4.74 a 11.19 |
| MX, juro de política | % a.a. | 2026-08-01 | 6.50 | +0.00 | +0.00 | -1.25 | 32 | 43 | 4.00 a 11.25 |
| MX, inflação 12m | % | 2026-08-01 | 3.26 | +0.14 | -0.68 | -0.31 | 12 | 13 | 2.15 a 8.70 |
| MX, juro real ex-post | % a.a. | 2026-08-01 | 3.24 | -0.14 | +0.68 | -0.94 | 55 | 64 | -2.37 a 6.99 |
| CL, juro de política | % a.a. | 2026-08-01 | 4.50 | +0.00 | +0.00 | -0.25 | 61 | 52 | 0.50 a 11.25 |
| CL, inflação 12m | % | 2026-08-01 | 4.13 | +0.61 | +0.20 | +0.10 | 62 | 65 | 1.45 a 14.08 |
| CL, juro real ex-post | % a.a. | 2026-08-01 | 0.37 | -0.61 | -0.20 | -0.35 | 55 | 43 | -4.33 a 4.94 |
| CO, juro de política | % a.a. | 2026-08-01 | 12.00 | +0.00 | +0.75 | +2.75 | 87 | 81 | 1.75 a 13.25 |
| CO, inflação 12m | % | 2026-08-01 | 6.24 | +0.22 | +0.40 | +1.15 | 72 | 59 | 1.49 a 13.34 |
| CO, juro real ex-post | % a.a. | 2026-08-01 | 5.76 | -0.22 | +0.35 | +1.60 | 99 | 85 | -4.53 a 5.97 |
| PE, juro de política | % a.a. | 2026-08-01 | 4.25 | +0.00 | +0.00 | -0.25 | 66 | 72 | 0.25 a 7.75 |
| PE, inflação 12m | % | 2026-08-01 | 4.44 | +0.37 | +0.53 | +3.33 | 79 | 83 | 0.36 a 8.81 |
| PE, juro real ex-post | % a.a. | 2026-08-01 | -0.19 | -0.37 | -0.53 | -3.58 | 32 | 24 | -4.45 a 3.75 |

## ii. Endógeno de câmbio (leitura enxuta)

### cmb_fx_latam

Último dado 2026-10-02 (no corte) · A: `A/cmb_fx_latam.csv.gz`

**Atenção:** O peso chileno e o colombiano datados em um dia são a taxa oficial formada no dia útil anterior: para comparar com o real ou com o dólar no mesmo dia, leia a taxa do dia útil seguinte. A tabela abaixo está como a fonte publica.

| Série | Unidade | Data | Último | Δ% 1m | Δ% 3m | Δ% 12m |
|---|---|---|---|---|---|---|
| Peso mexicano | MXN/US$ | 2026-10-02 | 18.3346 | +7.8 | +4.4 | -0.2 |
| Peso chileno | CLP/US$ | 2026-10-02 | 983.84 | +5.0 | +6.1 | +2.6 |
| Peso colombiano | COP/US$ | 2026-10-02 | 3307.73 | +3.9 | -2.8 | -15.0 |
| Sol peruano | PEN/US$ | 2026-10-02 | 3.4395 | +2.5 | +1.0 | -1.2 |

### cmb_cot_fx

Último dado 2026-09-29 (3 dias antes do corte) · A: `A/cmb_cot_fx.csv.gz`

| Série | Unidade | Data | Último | Δ 1m | Δ 3m | Δ 12m |
|---|---|---|---|---|---|---|
| BRL: fundos alavancados, líquido | contratos | 2026-09-29 | 9553 | -5160 | +1676 | -7581 |
| BRL: asset managers, líquido | contratos | 2026-09-29 | 67015 | +18136 | +15178 | -1313 |
| BRL: posições em aberto | contratos | 2026-09-29 | 146704 | +15151 | +42420 | +12386 |
| MXN: fundos alavancados, líquido | contratos | 2026-09-29 | 80587 | +11683 | +24056 | +45095 |
| MXN: asset managers, líquido | contratos | 2026-09-29 | 16251 | -52339 | -18718 | -29747 |
| MXN: posições em aberto | contratos | 2026-09-29 | 274821 | -11608 | +76233 | +98814 |

### cmb_termos_troca

Último dado 2026-07-01 (93 dias antes do corte) · A: `A/cmb_termos_troca.csv.gz`

| Série | Unidade | Data | Último | Δ% 1m | Δ% 3m | Δ% 12m |
|---|---|---|---|---|---|---|
| Termos de troca (Funcex) | índice | 2026-07-01 | 111.35 | -1.8 | -2.7 | +1.5 |

### cmb_comex_pais

Último dado 2026-09-01 (31 dias antes do corte) · A: `A/cmb_comex_pais.csv.gz`

| Série | Unidade | Último mês | Soma 3m | Soma 12m | Soma 12m, um ano antes |
|---|---|---|---|---|---|
| Mundo, exportação | US$ bi | 34.42 (2026-09) | 100.73 | 375.04 | 339.93 |
| China, exportação | US$ bi | 7.89 (2026-09) | 26.62 | 109.03 | 93.53 |
| EUA, exportação | US$ bi | 3.52 (2026-09) | 10.14 | 35.77 | 40.36 |

## iii. Endógeno de fiscal (leitura enxuta)

### cmb_risco_pais

Último dado 2026-10-02 (no corte) · A: `A/cmb_risco_pais.csv.gz`

| Série | Unidade | Data | Último | Δ 1m | Δ 3m | Δ 12m |
|---|---|---|---|---|---|---|
| CDS 5 anos Brasil | p.b. | 2026-10-02 | 131 | +10 | +6 | -5 |

## iv. Endógeno de expectativas (leitura enxuta)

### expc_qpc

Último dado 2026-09-23 (9 dias antes do corte) · A: `A/expc_qpc.csv.gz`

Fração das respostas do Questionário Pré-Copom sobre o ambiente externo; as outras perguntas do QPC são do agente de expectativas.

| Pergunta | Resposta | R280 (2026-08-12) | R281 (2026-09-23) |
|---|---|---|---|
| ambiente externo | mais favoravel | 2% | 1% |
| ambiente externo | menos favoravel | 62% | 67% |
| ambiente externo | sem mudancas relevantes | 36% | 32% |

## Leituras combinadas

### As sete exógenas na convenção do modelo

O valor de cada trimestre como o Modelo Estrutural o lê (`modelo.CONVENCAO`): é nesta convenção que o caminho é escrito e que o placar é medido. `ffr` = Fed Funds efetivo, média do último mês do trimestre; `infl_us` = 100·Δlog do CPI cheio (SA) do último mês do trimestre anterior ao último deste, em % no trimestre (sem anualizar); `dxy_em` e `sp500` = fechamento; `icbr_usd` = o índice do último mês; `icbr_agr_usd` e `icbr_met_usd` = média dos três meses. O trimestre em curso sai parcial, marcado.

| Trimestre | ffr | infl_us | dxy_em | sp500 | icbr_usd | icbr_agr_usd | icbr_met_usd |
|---|---|---|---|---|---|---|---|
| 2T25 | 4.33 | 0.51 | 131.29 | 6204.95 | 178.44 | 196.62 | 212.78 |
| 3T25 | 4.22 | 0.87 | 131.34 | 6688.46 | 182.31 | 198.10 | 228.74 |
| 4T25 | 3.72 | 0.55 | 130.34 | 6845.50 | 180.87 | 190.19 | 263.60 |
| 1T26 | 3.64 | 1.30 | 131.02 | 6528.52 | 194.92 | 188.96 | 328.79 |
| 2T26 | 3.63 | 0.69 | 129.46 | 7499.36 | 197.60 | 197.67 | 339.45 |
| 3T26 | 3.75 | 1.12 | 129.38 | 7651.54 | 205.70 | 200.53 | 330.14 |
| 4T26 (em curso) | — | — | 129.71 (até 02/10) | 7722.72 (até 02/10) | — | — | — |

### Política dos EUA: a curva contra a meta

Em 2026-10-02, meta do Fed (ponto médio) 3.88% e Fed Funds efetivo de 3.75% (09/2026, média do mês). Um vértice curto abaixo da meta é corte precificado no prazo dele, somado a um prêmio; não há futuros de Fed Funds no banco.

| Vértice | Taxa | Menos a meta (p.p.) |
|---|---|---|
| Treasury 1 mês | 4.04 | +0.17 |
| Treasury 3 meses | 4.19 | +0.32 |
| Treasury 6 meses | 4.27 | +0.39 |
| Treasury 1 ano | 4.46 | +0.58 |
| Treasury 2 anos | 4.83 | +0.96 |

| Inclinação | Hoje (p.p.) | 3 meses antes (p.p.) |
|---|---|---|
| 10 anos − 3 meses | +1.09 | +0.67 |
| 10 anos − 2 anos | +0.45 | +0.35 |
| 30 anos − 10 anos | +0.35 | +0.49 |

Juro real ex-ante de 10 anos aproximado: Treasury 10 anos 5.28% menos a inflação esperada de 10 anos do Cleveland Fed 2.73% (10/2026) = 2.55%.

Inflação americana recente, % ao ano (o CPI não tem outubro de 2025; uma janela que o atravessa compara com o mês disponível anterior):

| Medida | Mês | 3m anualizado | 6m anualizado | 12m |
|---|---|---|---|---|
| CPI cheio | 2026-09 | 4.56 | 3.67 | 3.72 |
| CPI núcleo | 2026-09 | 3.41 | 2.85 | 2.57 |
| CPI serviços sem energia | 2026-09 | 3.76 | 3.56 | 3.16 |
| PCE cheio | 2026-08 | 1.03 | 3.57 | 3.42 |
| PCE núcleo | 2026-08 | 2.05 | 2.74 | 3.01 |

### Risco e dólar: o que anda junto agora

Correlação dos retornos diários (log) com o dólar contra emergentes, até 2026-10-02. Moedas latinas em moeda local por dólar: correlação positiva = a moeda se desvaloriza quando o dólar EM sobe. Chile e Colômbia entram com a taxa oficial do dia útil seguinte, que é a formada no dia do retorno do dólar EM. Na (F) o S&P e o dólar EM entram juntos (mapa, 2.5).

| Contra o dólar EM | Correlação 3m | Correlação 12m | Correlação 10a |
|---|---|---|---|
| S&P 500 | -0.45 | -0.49 | -0.35 |
| DXY | +0.60 | +0.56 | +0.46 |
| México | +0.45 | +0.64 | +0.63 |
| Chile | +0.72 | +0.78 | +0.54 |
| Colômbia | +0.58 | +0.33 | +0.55 |
| Peru | +0.62 | +0.50 | +0.43 |

### Commodities: os grupos mês a mês

IC-Br em dólar (média do mês, publicado pelo BC com cerca de um mês de defasagem) e a variação contra o mês anterior. O Brent diário vai até 2026-10-02, além do último IC-Br: é ele que mostra o mês ainda não publicado na energia.

| Mês | IC-Br | Agro | Metal | Energia | Brent, média do mês |
|---|---|---|---|---|---|
| 2026-04 | 201.2 (+3.2%) | 196.9 (+4.0%) | 334.6 (+2.4%) | 94.5 (+0.4%) | 117.3 |
| 2026-05 | 207.7 (+3.2%) | 200.8 (+2.0%) | 350.9 (+4.9%) | 98.3 (+4.1%) | 107.1 |
| 2026-06 | 197.6 (-4.9%) | 195.3 (-2.8%) | 332.9 (-5.1%) | 86.3 (-12.2%) | 85.4 |
| 2026-07 | 196.8 (-0.4%) | 198.6 (+1.7%) | 318.3 (-4.4%) | 84.0 (-2.7%) | 83.8 |
| 2026-08 | 202.3 (+2.8%) | 201.2 (+1.3%) | 337.1 (+5.9%) | 86.8 (+3.3%) | 91.1 |
| 2026-09 | 205.7 (+1.7%) | 201.8 (+0.3%) | 335.1 (-0.6%) | 96.0 (+10.6%) | 114.2 |
