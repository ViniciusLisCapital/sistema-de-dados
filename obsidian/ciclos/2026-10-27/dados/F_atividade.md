# F(A) — atividade — ciclo 2026-10-27

Gerado em 2026-10-27 13:05. Dados do banco até 2026-10-27, fixos durante o ciclo. Ciclo anterior: 2026-10-02.

Os dados brutos (A) estão em `A/`, um arquivo por tabela; as funções G leem de lá e o código delas fica em `G/`. Nada aqui é opinião: é a mesma conta em todo ciclo.

Como ler:
- **Δ% 1m/3m/12m**: variação contra o último valor de 1, 3 e 12 meses antes da última data da série; numa série trimestral, **1t/4t**: contra 1 e 4 trimestres antes.
- **Δ**: diferença na unidade da série (p.p. quando a série é %, p.b. quando é p.b.).
- **Pctl**: posição do último valor no histórico, de 0 (o menor já visto) a 100 (o maior). "10a" = últimos 10 anos.
- **Soma 3m/12m**: soma dos últimos 3 e 12 meses completos; o mês em curso aparece à parte e não entra nas somas.
- **Acum.**: variação composta.
- **Desde o ciclo ant.**: contra o valor em 2026-10-02.

## i. Endógeno (leitura completa)

### atv_pib

Último dado 2026-04-01 (209 dias antes do corte) · A: `A/atv_pib.csv.gz`

| Série | Unidade | Data | Último | Δ% 1t | Δ% 4t | Δ% desde o ciclo ant. | Pctl 10a | Pctl hist. | Pctl Δ12m hist. | Mín–máx 10a |
|---|---|---|---|---|---|---|---|---|---|---|
| PIB | índice, dessaz. | 2026-04-01 | 198.24 | +0.5 | +1.9 | sem dado novo | 100 | 100 | 47 | 153.16 a 198.24 |
| Consumo das famílias | índice, dessaz. | 2026-04-01 | 208.27 | -0.4 | +0.4 | sem dado novo | 98 | 99 | 52 | 162.77 a 209.20 |
| Consumo do governo | índice, dessaz. | 2026-04-01 | 167.44 | +0.4 | +3.1 | sem dado novo | 100 | 100 | 50 | 136.33 a 167.44 |
| FBCF | índice, dessaz. | 2026-04-01 | 183.60 | +1.2 | +1.4 | sem dado novo | 98 | 90 | 62 | 130.82 a 184.45 |
| Exportação | índice, dessaz. | 2026-04-01 | 402.36 | -0.8 | +4.2 | sem dado novo | 95 | 98 | 43 | 280.55 a 414.07 |
| Importação | índice, dessaz. | 2026-04-01 | 328.82 | +1.8 | +5.4 | sem dado novo | 100 | 100 | 73 | 200.92 a 328.82 |
| Agropecuária | índice, dessaz. | 2026-04-01 | 307.40 | +2.8 | +6.4 | sem dado novo | 100 | 100 | 53 | 192.83 a 307.40 |
| Indústria | índice, dessaz. | 2026-04-01 | 146.95 | +0.1 | +1.2 | sem dado novo | 100 | 93 | 62 | 114.49 a 146.95 |
| Serviços | índice, dessaz. | 2026-04-01 | 206.74 | +0.2 | +1.5 | sem dado novo | 100 | 100 | 42 | 160.99 a 206.74 |

### atv_pib_taxas

Último dado 2026-04-01 (209 dias antes do corte) · A: `A/atv_pib_taxas.csv.gz`

**Contra o trimestre anterior, dessazonalizada (%)**

| Componente | 2T25 | 3T25 | 4T25 | 1T26 | 2T26 | Pctl hist. do último |
|---|---|---|---|---|---|---|
| PIB | 0.4 | 0.1 | 0.2 | 1.1 | 0.5 | 45 |
| Agropecuária | -3.2 | 0.5 | 0.7 | 2.3 | 2.8 | 76 |
| Indústria | 0.7 | 0.6 | -0.7 | 1.2 | 0.1 | 41 |
|   Transformação | -0.4 | 0.2 | -0.7 | 0.1 | -0.4 | 38 |
|   Extrativa | 4.4 | 2.4 | 1.7 | 3.9 | 3.4 | 83 |
|   Construção | -0.2 | 0.9 | -2.3 | 2.8 | -0.4 | 40 |
| Serviços | 0.8 | 0.3 | 0.6 | 0.4 | 0.2 | 25 |
| Consumo das famílias | 0.8 | -0.1 | 0.1 | 0.8 | -0.4 | 19 |
| Consumo do governo | 0.0 | 1.3 | 1.0 | 0.4 | 0.4 | 51 |
| FBCF | -1.9 | 0.7 | -3.8 | 3.4 | 1.2 | 55 |
| Exportação | 1.8 | 3.3 | 3.8 | -2.1 | -0.8 | 34 |
| Importação | -2.5 | 0.5 | -1.1 | 4.2 | 1.8 | 52 |

**Contra o mesmo trimestre do ano anterior (%)**

| Componente | 2T25 | 3T25 | 4T25 | 1T26 | 2T26 | Pctl hist. do último |
|---|---|---|---|---|---|---|
| PIB | 2.4 | 1.8 | 1.8 | 1.8 | 2.0 | 44 |
| Agropecuária | 11.5 | 10.1 | 12.1 | 0.7 | 6.8 | 72 |
| Indústria | 1.1 | 1.7 | 0.6 | 1.6 | 1.5 | 52 |
|   Transformação | -0.2 | -0.6 | -2.0 | -0.9 | -0.9 | 40 |
|   Extrativa | 8.8 | 11.9 | 12.0 | 13.1 | 12.0 | 90 |
|   Construção | 0.2 | 2.0 | -2.9 | 1.3 | 1.0 | 42 |
| Serviços | 1.9 | 1.3 | 2.0 | 2.1 | 1.5 | 29 |
| Consumo das famílias | 1.8 | 0.4 | 1.0 | 1.7 | 0.5 | 25 |
| Consumo do governo | 0.9 | 1.8 | 3.6 | 2.8 | 3.1 | 72 |
| FBCF | 4.1 | 2.3 | -3.1 | -1.4 | 1.4 | 41 |
| Exportação | 2.1 | 7.2 | 14.2 | 7.4 | 3.8 | 45 |
| Importação | 3.9 | 2.2 | -0.3 | 1.2 | 5.5 | 51 |

PIB acumulado em quatro trimestres até 2T26: 1.9%. Taxas oficiais do IBGE (impostos sem taxa contra o trimestre anterior).

### atv_pib_valores_correntes

Último dado 2026-04-01 (209 dias antes do corte) · A: `A/atv_pib_valores_correntes.csv.gz`

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

Último dado 2026-09-01 (56 dias antes do corte) · A: `A/atv_pib_mensal.csv.gz`

| Série | Unidade | Data | Último | Δ% 1m | Δ% 3m | Δ% 12m | Δ% desde o ciclo ant. | Pctl 10a | Pctl hist. | Pctl Δ12m hist. | Mín–máx 10a |
|---|---|---|---|---|---|---|---|---|---|---|---|
| PIB nominal, 12 meses | R$ bi | 2026-09-01 | 13402 | +0.5 | +1.6 | +7.0 | sem dado novo | 100 | 100 | 21 | 6187 a 13402 |

### atv_ibcbr

Último dado 2026-08-01 (87 dias antes do corte) · A: `A/atv_ibcbr.csv.gz`

| Série | Unidade | Data | Último | Δ% 1m | Δ% 3m | Δ% 12m | Δ% desde o ciclo ant. | Pctl 10a | Pctl hist. | Pctl Δ12m hist. | Mín–máx 10a |
|---|---|---|---|---|---|---|---|---|---|---|---|
| IBC-Br | índice, dessaz. | 2026-08-01 | 110.41 | +0.3 | -0.8 | +1.4 | sem dado novo | 97 | 99 | 40 | 82.96 a 111.25 |
| IBC-Br ex-agropecuária | índice, dessaz. | 2026-08-01 | 109.07 | +0.3 | -1.0 | +1.1 | sem dado novo | 97 | 99 | 35 | 82.71 a 110.13 |
| Agropecuária | índice, dessaz. | 2026-08-01 | 129.83 | -1.8 | -1.0 | +6.6 | sem dado novo | 91 | 96 | 69 | 87.40 a 133.07 |
| Indústria | índice, dessaz. | 2026-08-01 | 105.87 | +0.9 | -1.4 | +0.5 | sem dado novo | 96 | 65 | 46 | 80.11 a 107.41 |
| Serviços | índice, dessaz. | 2026-08-01 | 110.40 | +0.2 | -0.4 | +1.4 | sem dado novo | 98 | 99 | 35 | 84.70 a 110.81 |

### atv_pim

Último dado 2026-08-01 (87 dias antes do corte) · A: `A/atv_pim.csv.gz`

| Série | Unidade | Data | Último | Δ% 1m | Δ% 3m | Δ% 12m | Δ% desde o ciclo ant. | Pctl 10a | Pctl hist. | Pctl Δ12m hist. | Mín–máx 10a |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Indústria geral | índice, dessaz. | 2026-08-01 | 103.25 | -0.6 | -2.1 | -1.4 | sem dado novo | 69 | 47 | 29 | 75.36 a 106.57 |
| Transformação | índice, dessaz. | 2026-08-01 | 101.01 | -0.7 | -2.2 | -1.9 | sem dado novo | 58 | 38 | 28 | 71.78 a 106.17 |
| Extrativa | índice, dessaz. | 2026-08-01 | 116.56 | -0.7 | -2.0 | +1.7 | sem dado novo | 81 | 84 | 44 | 92.68 a 122.28 |

### atv_pim_uso

Último dado 2026-08-01 (87 dias antes do corte) · A: `A/atv_pim_uso.csv.gz`

| Série | Unidade | Data | Último | Δ% 1m | Δ% 3m | Δ% 12m | Δ% desde o ciclo ant. | Pctl 10a | Pctl hist. | Pctl Δ12m hist. | Mín–máx 10a |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Bens de capital | índice, dessaz. | 2026-08-01 | 90.38 | -0.6 | -0.8 | -3.9 | sem dado novo | 47 | 45 | 32 | 46.51 a 103.95 |
| Bens intermediários | índice, dessaz. | 2026-08-01 | 105.62 | -0.2 | -1.5 | -0.3 | sem dado novo | 93 | 57 | 39 | 81.99 a 108.14 |
| Bens de consumo duráveis | índice, dessaz. | 2026-08-01 | 119.03 | -1.0 | -0.8 | +3.2 | sem dado novo | 71 | 49 | 51 | 21.35 a 135.09 |
| Bens de consumo semi e não duráveis | índice, dessaz. | 2026-08-01 | 98.09 | -1.7 | -4.8 | -5.0 | sem dado novo | 7 | 14 | 12 | 83.49 a 110.06 |

### atv_pmc

Último dado 2026-08-01 (87 dias antes do corte) · A: `A/atv_pmc.csv.gz`

| Série | Unidade | Data | Último | Δ% 1m | Δ% 3m | Δ% 12m | Δ% desde o ciclo ant. | Pctl 10a | Pctl hist. | Pctl Δ12m hist. | Mín–máx 10a |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Varejo restrito | índice, dessaz. | 2026-08-01 | 108.69 | +0.1 | -0.4 | +1.0 | sem dado novo | 94 | 98 | 32 | 79.08 a 110.14 |
| Varejo ampliado | índice, dessaz. | 2026-08-01 | 106.63 | -0.2 | -0.9 | +0.6 | sem dado novo | 88 | 94 | 27 | 70.66 a 108.87 |
| Super e hipermercados | índice, dessaz. | 2026-08-01 | 112.49 | -0.1 | +0.8 | +1.6 | sem dado novo | 97 | 99 | 38 | 86.03 a 113.37 |
| Móveis e eletrodomésticos | índice, dessaz. | 2026-08-01 | 102.97 | -4.2 | -8.7 | -8.4 | sem dado novo | 51 | 66 | 13 | 66.18 a 136.28 |
| Veículos, motos e peças | índice, dessaz. | 2026-08-01 | 119.73 | -1.0 | -2.1 | +2.0 | sem dado novo | 88 | 89 | 47 | 45.43 a 131.05 |

### atv_pms

Último dado 2026-08-01 (87 dias antes do corte) · A: `A/atv_pms.csv.gz`

| Série | Unidade | Data | Último | Δ% 1m | Δ% 3m | Δ% 12m | Δ% desde o ciclo ant. | Pctl 10a | Pctl hist. | Pctl Δ12m hist. | Mín–máx 10a |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Serviços, total | índice, dessaz. | 2026-08-01 | 110.51 | -0.1 | +0.1 | +0.6 | sem dado novo | 95 | 97 | 36 | 73.71 a 110.81 |
| Prestados às famílias | índice, dessaz. | 2026-08-01 | 115.63 | +2.1 | +1.5 | +4.2 | sem dado novo | 100 | 84 | 77 | 40.77 a 115.63 |
| Informação e comunicação | índice, dessaz. | 2026-08-01 | 122.02 | -0.0 | -0.5 | +4.8 | sem dado novo | 97 | 98 | 62 | 83.48 a 125.53 |
| Profissionais e administrativos | índice, dessaz. | 2026-08-01 | 118.91 | -0.2 | -0.9 | +1.5 | sem dado novo | 98 | 95 | 55 | 79.77 a 120.04 |
| Transportes e correio | índice, dessaz. | 2026-08-01 | 100.98 | -0.2 | +0.2 | -3.1 | sem dado novo | 77 | 85 | 27 | 65.15 a 106.71 |

### atv_renda_poupanca

Último dado 2026-04-01 (209 dias antes do corte) · A: `A/atv_renda_poupanca.csv.gz`

Contas nacionais trimestrais, preços correntes.

| Conta | % do PIB, 4 tri até 2T26 | Um ano antes | Δ (p.p.) |
|---|---|---|---|
| Poupança bruta | 14.4 | 14.4 | -0.0 |
| Formação bruta de capital | 16.7 | 17.8 | -1.1 |
| Capacidade (+) ou necessidade (−) de financiamento | -2.3 | -3.4 | +1.1 |
| Rendas de propriedade líquidas com o exterior (− = envio) | -3.1 | -3.4 | +0.2 |

### pm_hiato_produto

Último dado 2026-09-01 (56 dias antes do corte) · A: `A/pm_hiato_produto.csv.gz`

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

Último dado 2026-09-01 (56 dias antes do corte) · A: `A/pm_hiato_produto_vintages.csv.gz`

21 edições, desde 2021-09. Central, % do potencial. O placar do hiato de um trimestre é a central do primeiro RPM depois do PIB do IBGE daquele trimestre (a edição do fechamento do trimestre seguinte); a quebra metodológica entre 2024-06 e 2024-09 deixa só a central comparável.

| Trimestre | Placar: 1º RPM após o PIB | Edição 2025-12 | Edição 2026-03 | Edição 2026-06 | Edição 2026-09 | Revisão na última (p.p.) |
|---|---|---|---|---|---|---|
| 3T26 | ainda não saiu | — | — | — | 0.41 | — |
| 2T26 | 0.51 (2026-09) | — | — | 0.36 | 0.51 | +0.15 |
| 1T26 | 0.49 (2026-06) | — | 0.13 | 0.49 | 0.60 | +0.11 |
| 4T25 | 0.39 (2026-03) | 0.17 | 0.39 | 0.60 | 0.74 | +0.14 |
| 3T25 | 0.54 (2025-12) | 0.54 | 0.70 | 0.82 | 0.95 | +0.13 |
| 2T25 | 0.67 (2025-09) | 0.89 | 1.01 | 1.07 | 1.17 | +0.10 |
| 1T25 | 0.86 (2025-06) | 1.15 | 1.26 | 1.32 | 1.40 | +0.08 |
| 4T24 | 0.85 (2025-03) | 1.25 | 1.34 | 1.39 | 1.47 | +0.08 |

### mt_pnad

Último dado 2026-08-01 (87 dias antes do corte) · A: `A/mt_pnad.csv.gz`

| Série | Unidade | Data | Último | Δ 1m | Δ 3m | Δ 12m | Δ desde o ciclo ant. | Pctl 10a | Pctl hist. | Mín–máx 10a |
|---|---|---|---|---|---|---|---|---|---|---|
| Taxa de desocupação | % | 2026-08-01 | 5.3 | +0.0 | -0.3 | -0.3 | sem dado novo | 3 | 2 | 5.1 a 14.9 |
| Taxa de participação | % | 2026-08-01 | 62.2 | +0.0 | +0.2 | -0.1 | sem dado novo | 47 | 33 | 56.5 a 63.6 |
| Nível de ocupação | % da PIA | 2026-08-01 | 58.9 | +0.0 | +0.3 | +0.1 | sem dado novo | 99 | 99 | 48.4 a 59.0 |
| Subutilização composta | % | 2026-08-01 | 13.1 | +0.1 | -0.2 | -1.0 | sem dado novo | 2 | 2 | 12.9 a 30.7 |
| Informalidade | % dos ocupados | 2026-08-01 | 37.5 | +0.0 | +0.2 | -0.5 | sem dado novo | 9 | 9 | 36.6 a 41.1 |

| Série | Unidade | Data | Último | Δ% 1m | Δ% 3m | Δ% 12m | Δ% desde o ciclo ant. | Pctl 10a | Pctl hist. | Pctl Δ12m hist. | Mín–máx 10a |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Ocupados | mil pessoas | 2026-08-01 | 103477 | +0.1 | +0.8 | +1.0 | sem dado novo | 100 | 100 | 39 | 81129 a 103477 |
| Rendimento habitual real | R$ | 2026-08-01 | 3777 | +0.5 | +0.7 | +3.7 | sem dado novo | 98 | 98 | 74 | 3061 a 3804 |
| Massa de rendimento habitual real | R$ bi | 2026-08-01 | 385.6 | +0.6 | +1.4 | +4.8 | sem dado novo | 100 | 100 | 67 | 280.2 a 385.6 |

### mt_desocupacao_retro

Último dado 2026-09-01 (56 dias antes do corte) · A: `A/mt_desocupacao_retro.csv.gz`

| Série | Unidade | Data | Último | Δ 1m | Δ 3m | Δ 12m | Δ desde o ciclo ant. | Pctl 10a | Pctl hist. | Mín–máx 10a |
|---|---|---|---|---|---|---|---|---|---|---|
| Desocupação dessazonalizada, retropolada pelo BC | % | 2026-07-01 | 5.41 | -0.02 | -0.01 | -0.32 | sem dado novo | 2 | 1 | 5.38 a 15.35 |

### mt_caged

Último dado 2026-08-01 (87 dias antes do corte) · A: `A/mt_caged.csv.gz`

| Série | Unidade | Data | Último | Δ% 1m | Δ% 3m | Δ% 12m | Δ% desde o ciclo ant. | Pctl 10a | Pctl hist. | Pctl Δ12m hist. | Mín–máx 10a |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Estoque de emprego formal | mil empregos | 2026-08-01 | 48245 | +0.3 | +0.7 | +1.9 | sem dado novo | 100 | 100 | 42 | 36697 a 48245 |
| Serviços | mil empregos | 2026-08-01 | 23587 | +0.5 | +0.9 | +2.9 | sem dado novo | 100 | 100 | 45 | 17451 a 23587 |
| Comércio | mil empregos | 2026-08-01 | 10490 | +0.2 | +0.3 | +0.9 | sem dado novo | 99 | 100 | 23 | 8137 a 10537 |
| Indústria de transformação | mil empregos | 2026-08-01 | 8292 | +0.2 | +0.5 | +0.2 | sem dado novo | 98 | 100 | 37 | 6666 a 8316 |
| Construção | mil empregos | 2026-08-01 | 3151 | +0.7 | +1.5 | +3.0 | sem dado novo | 100 | 99 | 53 | 1988 a 3151 |

### mt_caged_setor

Último dado 2026-08-01 (87 dias antes do corte) · A: `A/mt_caged_setor.csv.gz`

| Série | Unidade | Último mês | Soma 3m | Soma 12m | Soma 12m, um ano antes | Pctl soma 12m hist. |
|---|---|---|---|---|---|---|
| Saldo: comércio | mil empregos | 16.6 (2026-08) | 31.3 | 97.7 | 322.2 | 6 |
| Saldo: indústria de transformação | mil empregos | 15.2 (2026-08) | 37.2 | 15.9 | 210.3 | 1 |
| Saldo: construção | mil empregos | 20.8 (2026-08) | 46.0 | 91.6 | 88.7 | 12 |
| Saldo: agropecuária | mil empregos | 1.5 (2026-08) | 37.9 | -10.7 | 35.2 | 6 |
| Saldo: alojamento e alimentação | mil empregos | 11.7 (2026-08) | 16.7 | 65.7 | 79.0 | 12 |
| Saldo: informação e comunicação | mil empregos | 0.6 (2026-08) | 1.0 | 9.7 | 24.9 | 1 |
| Saldo: serviços administrativos | mil empregos | 16.4 (2026-08) | 45.0 | 193.0 | 210.8 | 14 |
| Saldo: saúde | mil empregos | 19.1 (2026-08) | 43.6 | 130.9 | 131.4 | 51 |
| Saldo: educação | mil empregos | 25.4 (2026-08) | 10.7 | 16.9 | 47.6 | 22 |

## ii. Endógeno de política monetária (leitura enxuta)

### br_interest_rate

Último dado 2026-10-26 (1 dia antes do corte) · A: `A/br_interest_rate.csv.gz`

| Série | Unidade | Data | Último | Δ 1m | Δ 3m | Δ 12m | Δ desde o ciclo ant. |
|---|---|---|---|---|---|---|---|
| Selic, meta | % a.a. | 2026-10-20 | 13.75 | +0.00 | -0.50 | -1.25 | +0.00 |
| NTN-B 2 anos (juro real) | % a.a. | 2026-10-26 | 7.96 | +0.57 | -0.53 | -0.66 | +0.60 |
| NTN-B 10 anos (juro real) | % a.a. | 2026-10-26 | 8.05 | +0.49 | -0.02 | +0.56 | +0.55 |

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

### inflc_meta

Último dado 2026-01-01 (299 dias antes do corte) · A: `A/inflc_meta.csv.gz`

| Ano | Meta (%) |
|---|---|
| 2024 | 3.00 |
| 2025 | 3.00 |
| 2026 | 3.00 |

## iii. Endógeno de câmbio (leitura enxuta)

### cmb_ptax

Último dado 2026-10-26 (1 dia antes do corte) · A: `A/cmb_ptax.csv.gz`

| Série | Unidade | Data | Último | Δ% 1m | Δ% 3m | Δ% 12m | Δ% desde o ciclo ant. |
|---|---|---|---|---|---|---|---|
| PTAX venda | R$/US$ | 2026-10-26 | 5.5007 | +5.8 | +8.6 | +2.2 | +5.3 |

### cmb_termos_troca

Último dado 2026-08-01 (87 dias antes do corte) · A: `A/cmb_termos_troca.csv.gz`

| Série | Unidade | Data | Último | Δ% 1m | Δ% 3m | Δ% 12m | Δ% desde o ciclo ant. |
|---|---|---|---|---|---|---|---|
| Termos de troca (Funcex) | índice | 2026-08-01 | 108.44 | -1.5 | -3.0 | +2.5 | sem dado novo |

### cmb_comex_produto

Último dado 2026-09-01 (56 dias antes do corte) · A: `A/cmb_comex_produto.csv.gz`

| Série | Unidade | Último mês | Soma 3m | Soma 12m | Soma 12m, um ano antes |
|---|---|---|---|---|---|
| Mundo, exportação | US$ bi | 34.42 (2026-09) | 100.73 | 375.04 | 339.93 |
| Petróleo, exportação | US$ bi | 6.50 (2026-09) | 15.72 | 54.10 | 43.87 |
| Soja, exportação | US$ bi | 3.47 (2026-09) | 13.76 | 49.10 | 41.33 |
| Minério de ferro, exportação | US$ bi | 2.02 (2026-09) | 6.77 | 28.53 | 27.33 |
| Carnes, exportação | US$ bi | 2.51 (2026-09) | 7.76 | 33.26 | 28.04 |
| Café, exportação | US$ bi | 1.30 (2026-09) | 3.22 | 13.78 | 14.05 |

### cmb_comex_pais

Último dado 2026-09-01 (56 dias antes do corte) · A: `A/cmb_comex_pais.csv.gz`

| Série | Unidade | Último mês | Soma 3m | Soma 12m | Soma 12m, um ano antes |
|---|---|---|---|---|---|
| Mundo, exportação | US$ bi | 34.42 (2026-09) | 100.73 | 375.04 | 339.93 |
| Mundo, importação | US$ bi | 26.68 (2026-09) | 79.66 | 290.87 | 278.16 |
| China, exportação | US$ bi | 7.89 (2026-09) | 26.62 | 109.03 | 93.53 |
| EUA, exportação | US$ bi | 3.52 (2026-09) | 10.14 | 35.77 | 40.36 |
| Argentina, exportação | US$ bi | 1.36 (2026-09) | 4.24 | 15.48 | 18.33 |

## iv. Endógeno de inflação (leitura enxuta)

### inflc_agregados

Último dado 2026-10-01 (26 dias antes do corte) · A: `A/inflc_agregados.csv.gz`

| Série | Mês | Último mês | Acum. 3m | Acum. 12m | Acum. 12m, 3 meses antes |
|---|---|---|---|---|---|
| IPCA | 2026-09 | 0.82 | 0.57 | 4.58 | 4.64 |
| Livres | 2026-09 | 0.55 | 0.55 | 4.68 | 4.31 |
| Serviços | 2026-09 | 0.61 | 1.18 | 5.97 | 5.90 |
| Alimentação | 2026-09 | 0.96 | -0.80 | 4.19 | 3.01 |
| Administrados | 2026-09 | 1.59 | 0.59 | 4.14 | 5.52 |

### comm_icbr

Último dado 2026-09-01 (56 dias antes do corte) · A: `A/comm_icbr.csv.gz`

| Série | Unidade | Data | Último | Δ% 1m | Δ% 3m | Δ% 12m | Δ% desde o ciclo ant. |
|---|---|---|---|---|---|---|---|
| IC-Br | índice, em R$ | 2026-09-01 | 462.94 | +1.5 | +4.5 | +8.1 | sem dado novo |
| IC-Br agropecuária | índice, em R$ | 2026-09-01 | 454.03 | +0.1 | +3.8 | -3.5 | sem dado novo |
| IC-Br metal | índice, em R$ | 2026-09-01 | 754.19 | -0.8 | +1.1 | +36.3 | sem dado novo |
| IC-Br energia | índice, em R$ | 2026-09-01 | 216.23 | +10.4 | +11.7 | +23.8 | sem dado novo |

## v. Endógeno de fiscal (leitura enxuta)

### fisc_efgg

Último dado 2026-04-01 (209 dias antes do corte) · A: `A/fisc_efgg.csv.gz`

Governo geral (GFSM) = soma de União, estados e municípios, SEM consolidar as transferências entre esferas: receita e despesa ficam acima das do governo geral consolidado; leia a variação, não o nível. Soma de quatro trimestres sobre o PIB nominal dos mesmos quatro.

| Conta | % do PIB, 4 tri até 2T26 | Um ano antes | Δ (p.p.) |
|---|---|---|---|
| Receita total | 51.8 | 50.3 | +1.5 |
| Despesa total | 60.2 | 56.4 | +3.7 |
| Juros | 11.4 | 9.6 | +1.8 |
| Benefícios previdenciários e assistenciais | 16.0 | 15.6 | +0.4 |
| Remuneração de empregados | 11.2 | 10.9 | +0.3 |
| Investimento líquido | 0.5 | 0.4 | +0.0 |

### fisc_rtn

Último dado 2026-08-01 (87 dias antes do corte) · A: `A/fisc_rtn.csv.gz`

| Série | Unidade | Último mês | Soma 3m | Soma 12m | Soma 12m, um ano antes |
|---|---|---|---|---|---|
| Primário do governo central (+ = superávit) | R$ bi | -13.6 (2026-08) | -50.7 | -70.7 | -30.4 |
| Receita líquida | R$ bi | 187.9 (2026-08) | 609.6 | 2488.4 | 2290.2 |
| Despesa total | R$ bi | 201.5 (2026-08) | 660.3 | 2559.1 | 2320.6 |

### fisc_nfsp

Último dado 2026-08-01 (87 dias antes do corte) · A: `A/fisc_nfsp.csv.gz`

| Série | Unidade | Data | Último | Δ 1m | Δ 3m | Δ 12m | Δ desde o ciclo ant. |
|---|---|---|---|---|---|---|---|
| Resultado primário, 12m (+ = superávit) | % do PIB | 2026-08-01 | -0.62 | +0.05 | +0.52 | -0.43 | sem dado novo |
| Resultado nominal, 12m | % do PIB | 2026-08-01 | -9.48 | -0.13 | +0.13 | -1.69 | sem dado novo |

### cmb_risco_pais

Último dado 2026-10-26 (1 dia antes do corte) · A: `A/cmb_risco_pais.csv.gz`

| Série | Unidade | Data | Último | Δ 1m | Δ 3m | Δ 12m | Δ desde o ciclo ant. |
|---|---|---|---|---|---|---|---|
| CDS 5 anos Brasil | p.b. | 2026-10-26 | 137 | +13 | +13 | -4 | +6 |

## vi. Endógeno de externo (leitura enxuta)

### comm_icbr_usd

Último dado 2026-09-01 (56 dias antes do corte) · A: `A/comm_icbr_usd.csv.gz`

| Série | Unidade | Data | Último | Δ% 1m | Δ% 3m | Δ% 12m | Δ% desde o ciclo ant. |
|---|---|---|---|---|---|---|---|
| IC-Br em dólar | índice | 2026-09-01 | 205.70 | +1.7 | +4.1 | +12.8 | sem dado novo |
| IC-Br agropecuária | índice | 2026-09-01 | 201.80 | +0.3 | +3.3 | +0.7 | sem dado novo |
| IC-Br metal | índice | 2026-09-01 | 335.06 | -0.6 | +0.7 | +42.2 | sem dado novo |
| IC-Br energia | índice | 2026-09-01 | 96.00 | +10.6 | +11.2 | +29.2 | sem dado novo |

## vii. Endógeno de expectativas (leitura enxuta)

### expc_focus_periodo (PIB)

Último dado 2026-10-23 (4 dias antes do corte) · A: `A/expc_focus_periodo__pib.csv.gz`

Pesquisa de 2026-10-23; 4 semanas antes: 2026-09-25. Mediana.

**PIB Total, trimestral** (unidade: %)

| Trimestre | Mediana | 4 sem. antes | Δ 4 sem. | Respondentes |
|---|---|---|---|---|
| 3T26 | 1.70 | 1.81 | -0.11 | 103 |
| 4T26 | 1.67 | 1.79 | -0.12 | 103 |
| 1T27 | 1.30 | 1.42 | -0.12 | 97 |
| 2T27 | 1.25 | 1.40 | -0.15 | 97 |
| 3T27 | 1.30 | 1.40 | -0.10 | 97 |
| 4T27 | 1.49 | 1.50 | -0.01 | 97 |
| 1T28 | 1.80 | 1.80 | +0.00 | 75 |
| 2T28 | 1.75 | 1.77 | -0.02 | 73 |

**Anual** (variação no ano para o PIB e os componentes; taxa no fim do ano para a desocupação)

| Indicador | 2026 | Δ 4 sem. 2026 | 2027 | Δ 4 sem. 2027 | 2028 | Δ 4 sem. 2028 |
|---|---|---|---|---|---|---|
| PIB Total | 1.80 | -0.06 | 1.31 | -0.10 | 1.81 | -0.01 |
| PIB Agropecuária | 2.50 | +0.10 | 1.00 | +0.00 | 2.51 | +0.01 |
| PIB Indústria | 1.44 | -0.16 | 1.00 | -0.20 | 1.66 | -0.04 |
| PIB Serviços | 1.70 | -0.10 | 1.50 | +0.00 | 1.80 | +0.00 |
| PIB Despesa de consumo das famílias | 1.30 | -0.15 | 1.20 | -0.21 | 1.80 | +0.00 |
| PIB Despesa de consumo da administração pública | 2.20 | +0.05 | 1.14 | -0.15 | 1.32 | +0.00 |
| PIB Formação Bruta de Capital Fixo | 0.90 | +0.00 | 1.06 | +0.00 | 1.75 | +0.00 |
| PIB Exportação de bens e serviços | 4.20 | -0.05 | 3.00 | +0.00 | 3.00 | +0.00 |
| PIB Importação de bens e serviços | 3.10 | +0.10 | 1.96 | +0.16 | 2.20 | +0.20 |

### expc_focus_periodo (desocupação)

Último dado 2026-10-23 (4 dias antes do corte) · A: `A/expc_focus_periodo__desocupacao__atividade.csv.gz`

Pesquisa de 2026-10-23; 4 semanas antes: 2026-09-25. Mediana.

**Taxa de desocupação, trimestral** (unidade: %)

| Trimestre | Mediana | 4 sem. antes | Δ 4 sem. | Respondentes |
|---|---|---|---|---|
| 3T26 | 5.30 | 5.31 | -0.01 | 69 |
| 4T26 | 5.20 | 5.30 | -0.10 | 69 |
| 1T27 | 6.10 | 6.10 | +0.00 | 65 |
| 2T27 | 5.80 | 5.80 | +0.00 | 65 |
| 3T27 | 5.77 | 5.80 | -0.03 | 64 |
| 4T27 | 5.73 | 5.80 | -0.07 | 63 |

**Anual** (variação no ano para o PIB e os componentes; taxa no fim do ano para a desocupação)

| Indicador | 2026 | Δ 4 sem. 2026 | 2027 | Δ 4 sem. 2027 | 2028 | Δ 4 sem. 2028 |
|---|---|---|---|---|---|---|
| Taxa de desocupação | 5.20 | -0.10 | 5.73 | -0.07 | 6.27 | -0.13 |

### expc_qpc

Último dado 2026-09-23 (34 dias antes do corte) · A: `A/expc_qpc.csv.gz`

QPC da reunião 281 (publicado em 2026-09-23).

Medianas do mercado. "Última vez perguntado": o QPC anterior mais recente com a mesma pergunta e a mesma referência.

| Variável | Referência | Mediana | p25 a p75 | Última vez perguntado |
|---|---|---|---|---|
| Hiato do produto (% do potencial) | 2026T2 | 0.50 | 0.30 a 1.00 | — |
| Hiato do produto (% do potencial) | 2026T4 | 0.20 | 0.00 a 0.50 | 0.21 (R279) |
| Hiato do produto (% do potencial) | 2027T4 | -0.20 | -0.41 a 0.07 | 0.00 (R279) |
| PIB, contra o trimestre anterior, dessaz. (%) | 2026T3 | 0.20 | 0.10 a 0.30 | 0.30 (R280) |
| PIB, contra o trimestre anterior, dessaz. (%) | 2026T4 | 0.20 | 0.10 a 0.30 | — |
| PIB, contra o mesmo trimestre do ano anterior (%) | 2026T3 | 1.82 | 1.70 a 2.00 | 2.00 (R280) |
| PIB, contra o mesmo trimestre do ano anterior (%) | 2026T4 | 1.80 | 1.60 a 1.90 | — |

Balanço de riscos do PIB, fatia das respostas:

| Ano | Respostas |
|---|---|
| 2026 | risco de alta 4%; risco de baixa 34%; riscos equilibrados 63% |
| 2027 | risco de alta 1%; risco de baixa 73%; riscos equilibrados 26% |

Perguntadas só em algumas reuniões; vale a mais recente:

| Variável estrutural | Horizonte | Mediana | QPC | Na pergunta anterior |
|---|---|---|---|---|
| Crescimento do PIB potencial (%) | 2a | 2.00 | R279 (2026-06-24) | 2.00 (R275) |
| Crescimento do PIB potencial (%) | 5a | 2.00 | R279 (2026-06-24) | 2.00 (R275) |
| Crescimento do PIB potencial (%) | curto prazo | 2.00 | R279 (2026-06-24) | 2.00 (R275) |
| Taxa de desemprego neutra, NAIRU (%) | 2a | 7.40 | R279 (2026-06-24) | 7.50 (R275) |
| Taxa de desemprego neutra, NAIRU (%) | 5a | 7.45 | R279 (2026-06-24) | 7.50 (R275) |
| Taxa de desemprego neutra, NAIRU (%) | curto prazo | 7.30 | R279 (2026-06-24) | 7.50 (R275) |
| Juro real neutro (% a.a.) | 2a | 6.00 | R279 (2026-06-24) | 5.50 (R275) |
| Juro real neutro (% a.a.) | 5a | 5.50 | R279 (2026-06-24) | 5.00 (R275) |
| Juro real neutro (% a.a.) | curto prazo | 6.40 | R279 (2026-06-24) | 6.00 (R275) |

## viii. TWA — crédito (leitura enxuta)

### cred_credito_resumo

Último dado 2026-08-01 (87 dias antes do corte) · A: `A/cred_credito_resumo.csv.gz`

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

Último dado 2026-06-01 (148 dias antes do corte) · A: `A/cred_fluxo_financeiro.csv.gz`

| Série | Unidade | Data | Último | Δ 1m | Δ 3m | Δ 12m | Δ desde o ciclo ant. |
|---|---|---|---|---|---|---|---|
| Fluxo financeiro, total | % do PIB, 12m | 2026-04-01 | -2.8 | -0.2 | -0.7 | -2.1 | sem dado novo |
| Fluxo financeiro, PF | % do PIB, 12m | 2026-04-01 | -1.8 | -0.1 | -0.4 | -1.4 | sem dado novo |
| Fluxo financeiro, PJ | % do PIB, 12m | 2026-04-01 | -1.0 | -0.1 | -0.3 | -0.7 | sem dado novo |

### cred_ptc

Último dado 2026-04-01 (209 dias antes do corte) · A: `A/cred_ptc.csv.gz`

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

Último dado 2026-07-01 (118 dias antes do corte) · A: `A/cred_credito_familias.csv.gz`

| Série | Unidade | Data | Último | Δ 1m | Δ 3m | Δ 12m | Δ desde o ciclo ant. |
|---|---|---|---|---|---|---|---|
| Endividamento das famílias | % da renda 12m | 2026-07-01 | 49.86 | +0.21 | -0.02 | +1.08 | sem dado novo |
| Endividamento sem imobiliário | % da renda 12m | 2026-07-01 | 30.81 | +0.04 | -0.38 | +0.29 | sem dado novo |
| Comprometimento de renda com o serviço da dívida | % da renda | 2026-07-01 | 28.72 | +0.06 | +0.34 | +1.40 | sem dado novo |
| Comprometimento de renda com juros | % da renda | 2026-07-01 | 10.83 | +0.05 | +0.17 | +0.88 | sem dado novo |

### cred_credito_amplo

Último dado 2026-08-01 (87 dias antes do corte) · A: `A/cred_credito_amplo.csv.gz`

| Série | Unidade | Data | Último | Δ% 1m | Δ% 3m | Δ% 12m | Δ% desde o ciclo ant. |
|---|---|---|---|---|---|---|---|
| Empresas: empréstimos do SFN | R$ bi | 2026-08-01 | 2352 | +0.0 | +0.7 | +7.0 | sem dado novo |
| Empresas: títulos de dívida | R$ bi | 2026-08-01 | 1527 | +0.6 | +2.4 | +16.0 | sem dado novo |
| Empresas: dívida externa | R$ bi | 2026-08-01 | 73 | +1.8 | +3.5 | -9.6 | sem dado novo |
| Famílias: empréstimos do SFN | R$ bi | 2026-08-01 | 4670 | +0.8 | +1.6 | +10.5 | sem dado novo |
| Governo: títulos públicos | R$ bi | 2026-08-01 | 8098 | -0.1 | +3.2 | +13.9 | sem dado novo |

### cred_modalidade_livre_pf

Último dado 2026-08-01 (87 dias antes do corte) · A: `A/cred_modalidade_livre_pf.csv.gz`

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

Último dado 2026-08-01 (87 dias antes do corte) · A: `A/cred_modalidade_livre_pj.csv.gz`

| Série | Unidade | Data | Último | Δ 1m | Δ 3m | Δ 12m | Δ desde o ciclo ant. |
|---|---|---|---|---|---|---|---|
| Capital de giro: taxa | % a.a. | 2026-08-01 | 22.89 | -1.60 | -0.21 | -3.23 | sem dado novo |
| Desconto de duplicatas: taxa | % a.a. | 2026-08-01 | 18.60 | -0.65 | -1.02 | -1.64 | sem dado novo |
| Conta garantida: taxa | % a.a. | 2026-08-01 | 56.15 | -1.23 | -7.20 | -2.86 | sem dado novo |
| Capital de giro: inadimplência | % da carteira | 2026-08-01 | 5.98 | +0.19 | +0.45 | +0.78 | sem dado novo |

| Série | Unidade | Último mês | Soma 3m | Soma 12m | Soma 12m, um ano antes |
|---|---|---|---|---|---|
| Capital de giro: concessões | R$ bi | 53.95 (2026-08) | 153.19 | 534.92 | 335.29 |

### cred_modalidade_direcionado_pj

Último dado 2026-08-01 (87 dias antes do corte) · A: `A/cred_modalidade_direcionado_pj.csv.gz`

| Série | Unidade | Data | Último | Δ% 1m | Δ% 3m | Δ% 12m | Δ% desde o ciclo ant. |
|---|---|---|---|---|---|---|---|
| BNDES: saldo | R$ bi | 2026-08-01 | 497 | +0.4 | +2.0 | +10.3 | sem dado novo |
| Rural: saldo | R$ bi | 2026-08-01 | 127 | -0.4 | +1.1 | +30.6 | sem dado novo |

| Série | Unidade | Data | Último | Δ 1m | Δ 3m | Δ 12m | Δ desde o ciclo ant. |
|---|---|---|---|---|---|---|---|
| BNDES: taxa | % a.a. | 2026-08-01 | 11.73 | -1.51 | -4.45 | -2.16 | sem dado novo |

## Leituras combinadas

### O trimestre pelos indicadores mensais

Índices dessazonalizados. "Carrego": quanto o trimestre cresce sobre o anterior se os meses que faltam repetirem o último. O trimestre de cada linha é o do último mês publicado daquele indicador, e eles não andam juntos.

| Indicador | Último mês | Trimestre | Média do tri contra o anterior (%) | Carrego: último mês contra o tri anterior (%) | 2T26 contra 1T26 (%) | Situação |
|---|---|---|---|---|---|---|
| IBC-Br | 2026-08 | 3T26 (2 de 3 meses) | -0.6 | -0.4 | +0.3 | parcial |
| IBC-Br ex-agropecuária | 2026-08 | 3T26 (2 de 3 meses) | -0.7 | -0.6 | +0.4 | parcial |
| Indústria geral | 2026-08 | 3T26 (2 de 3 meses) | -1.6 | -1.9 | +0.3 | parcial |
| Bens de capital | 2026-08 | 3T26 (2 de 3 meses) | -0.2 | -0.6 | +0.2 | parcial |
| Bens de consumo duráveis | 2026-08 | 3T26 (2 de 3 meses) | +2.0 | +1.5 | -0.1 | parcial |
| Varejo restrito | 2026-08 | 3T26 (2 de 3 meses) | -0.5 | -0.4 | -0.3 | parcial |
| Varejo ampliado | 2026-08 | 3T26 (2 de 3 meses) | -0.5 | -0.6 | -1.0 | parcial |
| Serviços | 2026-08 | 3T26 (2 de 3 meses) | -0.0 | -0.1 | +0.4 | parcial |

Emprego formal (CAGED, estoque sem ajuste sazonal), até 2026-08: saldo de 359 mil em 3 meses e 888 mil em 12 meses.

### O hiato do BC e o potencial implícito nele

Hiato da edição de 2026-09-01; PIB interanual oficial do IBGE. Potencial implícito = PIB interanual − (hiato − hiato de 4 trimestres antes).

| Trimestre | PIB interanual (%) | Hiato (%) | Hiato 4 tri antes (%) | Potencial implícito (%) |
|---|---|---|---|---|
| 2T26 | 2.0 | 0.51 | 1.17 | 2.66 |
| 1T26 | 1.8 | 0.60 | 1.40 | 2.60 |
| 4T25 | 1.8 | 0.74 | 1.47 | 2.53 |
| 3T25 | 1.8 | 0.95 | 1.34 | 2.19 |
| 2T25 | 2.4 | 1.17 | 1.10 | 2.33 |
| 1T25 | 3.1 | 1.40 | 0.83 | 2.53 |
| 4T24 | 3.6 | 1.47 | 0.56 | 2.69 |
| 3T24 | 4.1 | 1.34 | 0.43 | 3.19 |

**Potencial da linha companheira** (média dos últimos 4 trimestres): 2.50% ao ano. PIB interanual de um trimestre projetado = este potencial + hiato do modelo no trimestre − hiato quatro trimestres antes (observado ou do modelo). A conta é mecânica, não tempero.
O hiato já tem 3T26 (nowcast do BC) e o PIB oficial ainda não: na tradução, 3T26 dá 1.96% de PIB interanual implícito no hiato do BC.

Desocupação dessazonalizada do BC em 2026-07: 5.41%. NAIRU do QPC da reunião 279, mediana: 2a 7.40% (desocupação -1.99 p.p. contra ela); 5a 7.45% (desocupação -2.04 p.p. contra ela); curto prazo 7.30% (desocupação -1.89 p.p. contra ela). Abaixo da NAIRU = mercado de trabalho apertado.
