# F(A) — fiscal — ciclo 2026-10-27

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

### fisc_rtn

Último dado 2026-08-01 (87 dias antes do corte) · A: `A/fisc_rtn.csv.gz`

Governo central, acima da linha, R$ correntes, 12 meses até 2026-08. Crescimento real: soma dos 12 meses deflacionada mês a mês pelo IPCA contra a dos 12 meses anteriores (IPCA até 2026-09-01; mês sem IPCA deixa a célula em branco). % do PIB sobre o PIB nominal de 12 meses. Precatórios e créditos extraordinários movem os totais sem mudar a postura: leia os grupos.

| Grupo | 12m (R$ bi) | 12m % do PIB | 12m um ano antes (R$ bi) | Cresc. real 12m (%) |
|---|---|---|---|---|
| Receita líquida | 2488.4 | 18.65 | 2290.2 | +4.0 |
| Despesa total | 2559.1 | 19.18 | 2320.6 | +5.6 |
| Benefícios previdenciários | 1086.8 | 8.15 | 1003.5 | +3.7 |
| Pessoal e encargos | 428.6 | 3.21 | 390.2 | +5.2 |
| BPC/LOAS | 134.9 | 1.01 | 123.1 | +5.0 |
| Abono e seguro-desemprego | 94.1 | 0.71 | 85.7 | +5.1 |
| Obrigatórias com controle de fluxo (inclui Bolsa Família) | 377.0 | 2.83 | 367.7 | -1.9 |
|   dessas, Bolsa Família | 153.8 | 1.15 | 163.8 | -10.2 |
| Subsídios, subvenções e Proagro | 23.1 | 0.17 | 22.4 | -0.8 |
| Sentenças judiciais e precatórios | 42.3 | 0.32 | 41.0 | +0.3 |
| Discricionárias do Executivo | 245.2 | 1.84 | 174.6 | +34.6 |
| Resultado primário do governo central (+ = superávit) | -70.7 | -0.53 | -30.4 | — |

Último trimestre fechado contra o mesmo trimestre do ano anterior:

| Grupo | 2T26 (R$ bi) | Mesmo trimestre do ano anterior (R$ bi) | Cresc. real (%) |
|---|---|---|---|
| Receita líquida | 628.9 | 561.4 | +7.1 |
| Despesa total | 704.6 | 627.7 | +7.3 |
| Benefícios previdenciários | 328.8 | 304.6 | +3.2 |
| Discricionárias do Executivo | 67.2 | 41.7 | +54.0 |

### fisc_efgg

Último dado 2026-04-01 (209 dias antes do corte) · A: `A/fisc_efgg.csv.gz`

Governo geral (GFSM) = SOMA de União, estados e municípios, sem consolidar as transferências entre esferas: o nível fica acima do governo geral consolidado; leia a variação. Soma de 4 trimestres sobre o PIB nominal dos mesmos 4; real = deflacionado pela média trimestral do IPCA. A Δ da despesa exceto juros em % do PIB é a medida de impulso pela despesa (+ = expansionista).

| Conta | % do PIB, 4 tri até 2T26 | Um ano antes | Δ (p.p. do PIB) | Cresc. real 4 tri (%) |
|---|---|---|---|---|
| Despesa exceto juros | 48.8 | 46.8 | +1.9 | +6.7 |
| Despesa total | 60.2 | 56.4 | +3.7 | +9.3 |
| Juros | 11.4 | 9.6 | +1.8 | +21.6 |
| Benefícios previdenciários e assistenciais | 16.0 | 15.6 | +0.4 | +5.4 |
| Remuneração de empregados | 11.2 | 10.9 | +0.3 | +5.7 |
| Uso de bens e serviços | 5.9 | 5.7 | +0.3 | +7.2 |
| Subsídios | 0.4 | 0.3 | +0.1 | +23.9 |
| Investimento líquido | 0.5 | 0.4 | +0.0 | +8.7 |
| Receita total | 51.8 | 50.3 | +1.5 | +5.5 |

### fisc_investimento

Último dado 2026-08-01 (87 dias antes do corte) · A: `A/fisc_investimento.csv.gz`

Governo federal, pago, 12 meses até 2026-08. GND 4 cria ativo novo (é demanda); GND 5 só troca a titularidade de um ativo (não é demanda).

| Item | 12m (R$ bi) | 12m % do PIB | 12m um ano antes (R$ bi) | Cresc. real 12m (%) |
|---|---|---|---|---|
| Total (GND 4 + 5) | 100.8 | 0.76 | 82.9 | +16.3 |
| GND 4, investimentos | 78.6 | 0.59 | 60.1 | +25.5 |
|   obras e instalações | 12.0 | 0.09 | 10.9 | +5.3 |
|   equipamentos | 13.2 | 0.10 | 11.6 | +8.5 |
|   transferências a estados | 7.6 | 0.06 | 5.0 | +45.3 |
|   transferências a municípios | 29.0 | 0.22 | 16.3 | +70.4 |
| GND 5, inversões financeiras | 22.1 | 0.17 | 22.9 | -7.8 |

### fisc_nfsp

Último dado 2026-08-01 (87 dias antes do corte) · A: `A/fisc_nfsp.csv.gz`

| Série | Unidade | Data | Último | Δ 1m | Δ 3m | Δ 12m | Δ desde o ciclo ant. | Pctl 10a | Pctl hist. | Mín–máx 10a |
|---|---|---|---|---|---|---|---|---|---|---|
| Primário, setor público consolidado, 12m (+ = superávit) | % do PIB | 2026-08-01 | -0.62 | +0.05 | +0.52 | -0.43 | sem dado novo | 69 | 35 | -9.24 a 2.40 |
| Primário, governo federal e BC, 12m | % do PIB | 2026-08-01 | -0.53 | +0.02 | +0.51 | -0.30 | sem dado novo | 72 | 24 | -9.79 a 1.15 |
| Primário, estados e municípios, 12m | % do PIB | 2026-08-01 | -0.04 | +0.03 | -0.01 | -0.16 | sem dado novo | 2 | 12 | -0.07 a 1.37 |
| Primário, estatais, 12m | % do PIB | 2026-08-01 | -0.04 | +0.02 | +0.03 | +0.03 | sem dado novo | 25 | 24 | -0.08 a 0.20 |
| Juros nominais, 12m | % do PIB | 2026-08-01 | 8.86 | +0.18 | +0.38 | +1.25 | sem dado novo | 100 | 98 | 3.40 a 8.86 |
| Resultado nominal, 12m | % do PIB | 2026-08-01 | -9.48 | -0.13 | +0.13 | -1.69 | sem dado novo | 15 | 9 | -13.48 a -3.06 |

### fisc_dlsp_fatores

Último dado 2026-08-01 (87 dias antes do corte) · A: `A/fisc_dlsp_fatores.csv.gz`

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

O canal parafiscal, até 2026-08. No estoque da dívida líquida um crédito do governo é ATIVO e aparece negativo: mais negativo = mais crédito concedido.

|  | Último (R$ bi) | Um ano antes (R$ bi) | Δ 12m (R$ bi) | % do PIB | % do PIB, um ano antes |
|---|---|---|---|---|---|
| Créditos do Tesouro a instituições financeiras oficiais (estoque) | -232.9 | -106.7 | -126.2 | -1.75 | -0.86 |

### fisc_divida

Último dado 2026-08-01 (87 dias antes do corte) · A: `A/fisc_divida.csv.gz`

| Série | Unidade | Data | Último | Δ 1m | Δ 3m | Δ 12m | Δ desde o ciclo ant. | Pctl 10a | Pctl hist. | Mín–máx 10a |
|---|---|---|---|---|---|---|---|---|---|---|
| Dívida bruta do governo geral | % do PIB | 2026-08-01 | 82.9 | +0.3 | +1.8 | +5.6 | sem dado novo | 93 | 96 | 69.3 a 87.7 |
| Dívida líquida do setor público | % do PIB | 2026-08-01 | 69.3 | +0.2 | +1.4 | +5.2 | sem dado novo | 100 | 100 | 42.8 a 69.3 |
| DLSP, governo federal | % do PIB | 2026-08-01 | 61.5 | +0.4 | +1.2 | +4.0 | sem dado novo | 100 | 100 | 32.4 a 61.5 |
| DLSP, Banco Central | % do PIB | 2026-08-01 | -0.7 | -0.2 | +0.2 | +1.2 | sem dado novo | 87 | 73 | -10.0 a 0.6 |
| DLSP, estados e municípios | % do PIB | 2026-08-01 | 8.1 | -0.0 | +0.0 | +0.0 | sem dado novo | 14 | 6 | 8.0 a 13.1 |
| DLSP, estatais | % do PIB | 2026-08-01 | 0.3 | -0.0 | -0.1 | -0.0 | sem dado novo | 11 | 4 | 0.3 a 0.9 |

### cmb_risco_pais

Último dado 2026-10-26 (1 dia antes do corte) · A: `A/cmb_risco_pais.csv.gz`

**Atenção:** carga manual (export da Bloomberg), com um trecho provisório de outra fonte; confira a data do último dado no cabeçalho antes de usar.

| Série | Unidade | Data | Último | Δ 1m | Δ 3m | Δ 12m | Δ desde o ciclo ant. | Pctl 10a | Pctl hist. | Mín–máx 10a |
|---|---|---|---|---|---|---|---|---|---|---|
| CDS 5 anos Brasil | p.b. | 2026-10-26 | 137 | +13 | +13 | -4 | +6 | 17 | 27 | 92 a 383 |


Fechamento de cada trimestre (último pregão), a convenção da exógena `fiscal` do Modelo Estrutural; o trimestre em curso aparece com o último dado.

| Trimestre | Último pregão | CDS (p.b.) |
|---|---|---|
| 4T24 | 2024-12-31 | 216 |
| 1T25 | 2025-03-31 | 187 |
| 2T25 | 2025-06-30 | 149 |
| 3T25 | 2025-09-30 | 136 |
| 4T25 | 2025-12-31 | 138 |
| 1T26 | 2026-03-31 | 140 |
| 2T26 | 2026-06-30 | 125 |
| 3T26 | 2026-09-30 | 131 |
| 4T26 | 2026-10-26 | 137 |

## ii. Endógeno de atividade (leitura enxuta)

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

### atv_pib

Último dado 2026-04-01 (209 dias antes do corte) · A: `A/atv_pib.csv.gz`

| Série | Unidade | Data | Último | Δ% 1t | Δ% 4t | Δ% desde o ciclo ant. |
|---|---|---|---|---|---|---|
| PIB | índice, dessaz. | 2026-04-01 | 198.24 | +0.5 | +1.9 | sem dado novo |
| Consumo do governo | índice, dessaz. | 2026-04-01 | 167.44 | +0.4 | +3.1 | sem dado novo |
| FBCF | índice, dessaz. | 2026-04-01 | 183.60 | +1.2 | +1.4 | sem dado novo |
| Consumo das famílias | índice, dessaz. | 2026-04-01 | 208.27 | -0.4 | +0.4 | sem dado novo |

### atv_pib_taxas

Último dado 2026-04-01 (209 dias antes do corte) · A: `A/atv_pib_taxas.csv.gz`

| Série | Unidade | Data | Último | Δ 1t | Δ 4t | Δ desde o ciclo ant. |
|---|---|---|---|---|---|---|
| PIB, contra o trimestre anterior (dessaz.) | % | 2026-04-01 | 0.5 | -0.6 | +0.1 | sem dado novo |
| PIB, contra o mesmo trimestre do ano anterior | % | 2026-04-01 | 2.0 | +0.2 | -0.4 | sem dado novo |
| PIB, acumulado em 4 trimestres | % | 2026-04-01 | 1.9 | -0.1 | -1.4 | sem dado novo |
| Consumo do governo, contra o trimestre anterior | % | 2026-04-01 | 0.4 | +0.0 | +0.4 | sem dado novo |
| Consumo do governo, contra o mesmo trimestre | % | 2026-04-01 | 3.1 | +0.3 | +2.2 | sem dado novo |
| Consumo do governo, acumulado em 4 trimestres | % | 2026-04-01 | 2.8 | +0.5 | +1.5 | sem dado novo |
| FBCF, contra o mesmo trimestre | % | 2026-04-01 | 1.4 | +2.8 | -2.7 | sem dado novo |

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

| Série | Unidade | Data | Último | Δ% 1m | Δ% 3m | Δ% 12m | Δ% desde o ciclo ant. |
|---|---|---|---|---|---|---|---|
| PIB nominal, 12 meses | R$ bi | 2026-09-01 | 13402 | +0.5 | +1.6 | +7.0 | sem dado novo |

## iii. Endógeno de inflação (leitura enxuta)

### inflc_agregados

Último dado 2026-10-01 (26 dias antes do corte) · A: `A/inflc_agregados.csv.gz`

| Série | Mês | Último mês | Acum. 3m | Acum. 12m | Acum. 12m, 3 meses antes |
|---|---|---|---|---|---|
| IPCA | 2026-09 | 0.82 | 0.57 | 4.58 | 4.64 |
| Administrados | 2026-09 | 1.59 | 0.59 | 4.14 | 5.52 |
| Livres | 2026-09 | 0.55 | 0.55 | 4.68 | 4.31 |

## iv. Endógeno de política monetária (leitura enxuta)

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
| 275 | 2025-12-10 | 15.00 | +0 |
| 274 | 2025-11-05 | 15.00 | +0 |

Ciclo em curso: corte desde 2026-03-18, 5 reuniões, -125 p.b. acumulados (Selic de 15.00% para 13.75%).

### br_interest_rate

Último dado 2026-10-26 (1 dia antes do corte) · A: `A/br_interest_rate.csv.gz`

| Série | Unidade | Data | Último | Δ 1m | Δ 3m | Δ 12m | Δ desde o ciclo ant. |
|---|---|---|---|---|---|---|---|
| Selic, meta | % a.a. | 2026-10-20 | 13.75 | +0.00 | -0.50 | -1.25 | +0.00 |
| DI × pré 1 ano | % a.a. | 2026-10-26 | 14.69 | +1.09 | +0.59 | +0.62 | +1.20 |
| DI × pré 5 anos | % a.a. | 2026-10-26 | 15.28 | +1.33 | +0.63 | +2.00 | +1.25 |
| DI × pré 10 anos | % a.a. | 2026-10-26 | 15.13 | +1.16 | +0.42 | +1.64 | +0.97 |
| NTN-B 2 anos (juro real) | % a.a. | 2026-10-26 | 7.96 | +0.57 | -0.53 | -0.66 | +0.60 |
| NTN-B 5 anos (juro real) | % a.a. | 2026-10-26 | 7.94 | +0.29 | -0.36 | +0.07 | +0.38 |
| NTN-B 10 anos (juro real) | % a.a. | 2026-10-26 | 8.05 | +0.49 | -0.02 | +0.56 | +0.55 |

## v. Endógeno de câmbio (leitura enxuta)

### cmb_ptax

Último dado 2026-10-26 (1 dia antes do corte) · A: `A/cmb_ptax.csv.gz`

| Série | Unidade | Data | Último | Δ% 1m | Δ% 3m | Δ% 12m | Δ% desde o ciclo ant. |
|---|---|---|---|---|---|---|---|
| PTAX venda | R$/US$ | 2026-10-26 | 5.5007 | +5.8 | +8.6 | +2.2 | +5.3 |

### cmb_reservas_bc

Último dado 2026-10-26 (1 dia antes do corte) · A: `A/cmb_reservas_bc.csv.gz`

| Série | Unidade | Data | Último | Δ 1m | Δ 3m | Δ 12m | Δ desde o ciclo ant. |
|---|---|---|---|---|---|---|---|
| Reservas internacionais | US$ bi | 2026-10-26 | 364.9 | -0.0 | -4.0 | +5.7 | +2.1 |
| Swap cambial do BC, posição (− = vendido) | US$ bi | 2026-08-01 | -91.6 | +1.3 | +3.2 | +9.8 | sem dado novo |

### cmb_fx_latam

Último dado 2026-10-20 (7 dias antes do corte) · A: `A/cmb_fx_latam.csv.gz`

**Atenção:** O peso chileno e o colombiano datados em um dia são a taxa oficial formada no dia útil anterior: para comparar com o real ou com o dólar no mesmo dia, leia a taxa do dia útil seguinte. A tabela abaixo está como a fonte publica.

| Série | Unidade | Data | Último | Δ% 1m | Δ% 3m | Δ% 12m | Δ% desde o ciclo ant. |
|---|---|---|---|---|---|---|---|
| Peso mexicano | MXN/US$ | 2026-10-20 | 18.5215 | +7.8 | +5.9 | +0.7 | +1.0 |
| Peso chileno | CLP/US$ | 2026-10-20 | 981.86 | +2.8 | +5.1 | +2.2 | -0.2 |
| Peso colombiano | COP/US$ | 2026-10-16 | 3170.46 | +2.3 | -2.0 | -18.8 | -4.1 |
| Sol peruano | PEN/US$ | 2026-10-19 | 3.4405 | +2.5 | +1.0 | +1.4 | +0.0 |

## vi. Endógeno de expectativas (leitura enxuta)

### expc_focus_periodo (fiscal)

Último dado 2026-10-23 (4 dias antes do corte) · A: `A/expc_focus_periodo__fiscal__fiscal.csv.gz`

Focus, mediana por ano de referência, para cada indicador fiscal.

**Resultado primário**

Unidade: % do PIB. Mediana da pesquisa (janela de 30 dias).

| Ano | Mediana (2026-10-23) | 4 sem. antes (2026-09-25) | 13 sem. antes (2026-07-24) | Δ 4 sem. | Ciclo ant. (2026-10-02) | Respondentes |
|---|---|---|---|---|---|---|
| 2026 | -0.48 | -0.41 | -0.50 | -0.07 | -0.41 | 58 |
| 2027 | -0.30 | -0.40 | -0.40 | +0.10 | -0.40 | 57 |
| 2028 | 0.00 | -0.30 | -0.25 | +0.30 | -0.27 | 53 |
| 2029 | 0.10 | -0.15 | -0.16 | +0.25 | -0.16 | 49 |

**Resultado nominal**

Unidade: % do PIB. Mediana da pesquisa (janela de 30 dias).

| Ano | Mediana (2026-10-23) | 4 sem. antes (2026-09-25) | 13 sem. antes (2026-07-24) | Δ 4 sem. | Ciclo ant. (2026-10-02) | Respondentes |
|---|---|---|---|---|---|---|
| 2026 | -8.93 | -8.90 | -8.70 | -0.03 | -8.88 | 53 |
| 2027 | -8.50 | -8.50 | -8.20 | +0.00 | -8.50 | 52 |
| 2028 | -7.90 | -7.91 | -7.70 | +0.01 | -7.91 | 47 |
| 2029 | -7.40 | -7.50 | -7.20 | +0.10 | -7.50 | 43 |

**Dívida líquida do setor público**

Unidade: % do PIB. Mediana da pesquisa (janela de 30 dias).

| Ano | Mediana (2026-10-23) | 4 sem. antes (2026-09-25) | 13 sem. antes (2026-07-24) | Δ 4 sem. | Ciclo ant. (2026-10-02) | Respondentes |
|---|---|---|---|---|---|---|
| 2026 | 70.10 | 70.00 | 69.80 | +0.10 | 70.00 | 54 |
| 2027 | 74.00 | 73.80 | 73.40 | +0.20 | 73.75 | 53 |
| 2028 | 76.60 | 76.44 | 76.40 | +0.16 | 76.46 | 49 |
| 2029 | 79.13 | 79.07 | 79.00 | +0.05 | 79.05 | 47 |

**Dívida bruta do governo geral**

Unidade: % do PIB. Mediana da pesquisa (janela de 30 dias).

| Ano | Mediana (2026-10-23) | 4 sem. antes (2026-09-25) | 13 sem. antes (2026-07-24) | Δ 4 sem. | Ciclo ant. (2026-10-02) | Respondentes |
|---|---|---|---|---|---|---|
| 2026 | 83.50 | 83.40 | 83.30 | +0.10 | 83.40 | 58 |
| 2027 | 87.20 | 87.31 | 87.10 | -0.11 | 87.30 | 57 |
| 2028 | 90.10 | 90.42 | 90.00 | -0.31 | 90.40 | 53 |
| 2029 | 92.65 | 92.90 | 92.27 | -0.25 | 92.88 | 50 |

**PIB Despesa de consumo da administração pública**

Unidade: %. Mediana da pesquisa (janela de 30 dias).

| Ano | Mediana (2026-10-23) | 4 sem. antes (2026-09-25) | 13 sem. antes (2026-07-24) | Δ 4 sem. | Ciclo ant. (2026-10-02) | Respondentes |
|---|---|---|---|---|---|---|
| 2026 | 2.20 | 2.15 | 2.10 | +0.05 | 2.20 | 46 |
| 2027 | 1.14 | 1.29 | 1.20 | -0.15 | 1.21 | 46 |
| 2028 | 1.32 | 1.32 | 1.30 | +0.00 | 1.32 | 39 |
| 2029 | 1.50 | 1.50 | 1.50 | +0.00 | 1.50 | 35 |

### expc_focus_periodo (IPCA)

Último dado 2026-10-23 (4 dias antes do corte) · A: `A/expc_focus_periodo__ipca.csv.gz`

IPCA, % no ano. Os anos distantes são a expectativa longa: subir com notícia fiscal é sinal de dominância (mapa 2.12).

| Ano | Mediana (2026-10-23) | 13 sem. antes (2026-07-24) | Δ 13 sem. |
|---|---|---|---|
| 2026 | 5.19 | 5.12 | +0.07 |
| 2027 | 4.34 | 4.22 | +0.12 |
| 2028 | 3.75 | 3.80 | -0.05 |
| 2029 | 3.50 | 3.50 | +0.00 |
| 2030 | 3.50 | 3.50 | +0.00 |

### expc_qpc

Último dado 2026-09-23 (34 dias antes do corte) · A: `A/expc_qpc.csv.gz`

Fração das respostas sobre a situação fiscal DESDE O COPOM ANTERIOR (difusão, não nível).

| Reunião | Publicação | Piorou (%) | Sem mudança (%) | Melhorou (%) | Respostas |
|---|---|---|---|---|---|
| 281 | 2026-09-23 | 17 | 81 | 2 | 106 |
| 280 | 2026-08-12 | 29 | 71 | 1 | 112 |
| 279 | 2026-06-24 | 50 | 48 | 2 | 115 |
| 278 | 2026-05-06 | 22 | 60 | 18 | 115 |
| 277 | 2026-03-25 | 6 | 86 | 8 | 111 |
| 276 | 2026-02-04 | 14 | 80 | 5 | 111 |

## vii. Endógeno de externo (leitura enxuta)

### us_interest_rate

Último dado 2026-10-27 (no corte) · A: `A/us_interest_rate.csv.gz`

| Série | Unidade | Data | Último | Δ 1m | Δ 3m | Δ 12m | Δ desde o ciclo ant. |
|---|---|---|---|---|---|---|---|
| Fed Funds, meta (ponto médio) | % a.a. | 2026-10-27 | 3.88 | +0.00 | +0.25 | -0.25 | +0.00 |
| Treasury 2 anos | % a.a. | 2026-10-23 | 4.69 | -0.16 | +0.32 | +1.21 | -0.14 |
| Treasury 10 anos | % a.a. | 2026-10-23 | 5.00 | -0.11 | +0.29 | +0.99 | -0.28 |

### cmb_equity_us

Último dado 2026-10-27 (no corte) · A: `A/cmb_equity_us.csv.gz`

| Série | Unidade | Data | Último | Δ% 1m | Δ% 3m | Δ% 12m | Δ% desde o ciclo ant. |
|---|---|---|---|---|---|---|---|
| S&P 500 | pontos | 2026-10-27 | 7717 | -0.3 | +4.1 | +12.2 | -0.1 |

### cmb_dollar_index_em

Último dado 2026-10-23 (4 dias antes do corte) · A: `A/cmb_dollar_index_em.csv.gz`

| Série | Unidade | Data | Último | Δ% 1m | Δ% 3m | Δ% 12m | Δ% desde o ciclo ant. |
|---|---|---|---|---|---|---|---|
| Dólar contra emergentes (FRED) | índice | 2026-10-23 | 130.21 | +1.6 | +0.6 | -1.2 | +0.4 |

### comm_brent

Último dado 2026-10-20 (7 dias antes do corte) · A: `A/comm_brent.csv.gz`

| Série | Unidade | Data | Último | Δ% 1m | Δ% 3m | Δ% 12m | Δ% desde o ciclo ant. |
|---|---|---|---|---|---|---|---|
| Brent | US$/barril | 2026-10-20 | 115.22 | -3.7 | +32.5 | +89.8 | -15.0 |

## viii. TWA — crédito (leitura enxuta)

### cred_credito_controle_capital

Último dado 2026-08-01 (87 dias antes do corte) · A: `A/cred_credito_controle_capital.csv.gz`

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

### cred_modalidade_direcionado_pj

Último dado 2026-08-01 (87 dias antes do corte) · A: `A/cred_modalidade_direcionado_pj.csv.gz`

| Série | Unidade | Data | Último | Δ% 1m | Δ% 3m | Δ% 12m | Δ% desde o ciclo ant. |
|---|---|---|---|---|---|---|---|
| BNDES: saldo | R$ bi | 2026-08-01 | 497 | +0.4 | +2.0 | +10.3 | sem dado novo |
| Rural: saldo | R$ bi | 2026-08-01 | 127 | -0.4 | +1.1 | +30.6 | sem dado novo |

| Série | Unidade | Data | Último | Δ 1m | Δ 3m | Δ 12m | Δ desde o ciclo ant. |
|---|---|---|---|---|---|---|---|
| BNDES: taxa | % a.a. | 2026-08-01 | 11.73 | -1.51 | -4.45 | -2.16 | sem dado novo |

### cred_modalidade_direcionado_pf

Último dado 2026-08-01 (87 dias antes do corte) · A: `A/cred_modalidade_direcionado_pf.csv.gz`

| Série | Unidade | Data | Último | Δ% 1m | Δ% 3m | Δ% 12m | Δ% desde o ciclo ant. |
|---|---|---|---|---|---|---|---|
| Imobiliário: saldo | R$ bi | 2026-08-01 | 1431 | +1.1 | +3.8 | +13.8 | sem dado novo |
| Rural: saldo | R$ bi | 2026-08-01 | 558 | -0.1 | -2.1 | +2.9 | sem dado novo |

| Série | Unidade | Data | Último | Δ 1m | Δ 3m | Δ 12m | Δ desde o ciclo ant. |
|---|---|---|---|---|---|---|---|
| Imobiliário: taxa | % a.a. | 2026-08-01 | 11.28 | -0.02 | +0.05 | +0.79 | sem dado novo |

### cred_credito_resumo

Último dado 2026-08-01 (87 dias antes do corte) · A: `A/cred_credito_resumo.csv.gz`

| Série | Unidade | Data | Último | Δ% 1m | Δ% 3m | Δ% 12m | Δ% desde o ciclo ant. |
|---|---|---|---|---|---|---|---|
| Saldo total | R$ bi | 2026-08-01 | 7398 | +0.5 | +1.3 | +9.2 | sem dado novo |
| Saldo direcionado | R$ bi | 2026-08-01 | 3250 | +0.8 | +2.5 | +12.9 | sem dado novo |

| Série | Unidade | Data | Último | Δ 1m | Δ 3m | Δ 12m | Δ desde o ciclo ant. |
|---|---|---|---|---|---|---|---|
| Saldo direcionado | % do PIB | 2026-08-01 | 24.4 | +0.0 | +0.2 | +1.2 | sem dado novo |
| Taxa de juros, direcionado | % a.a. | 2026-08-01 | 11.73 | -0.36 | -0.58 | +0.03 | sem dado novo |
| Taxa de juros, livre PJ | % a.a. | 2026-08-01 | 24.19 | -0.96 | -0.74 | -0.74 | sem dado novo |

| Série | Unidade | Último mês | Soma 3m | Soma 12m | Soma 12m, um ano antes |
|---|---|---|---|---|---|
| Concessões direcionadas | R$ bi | 81.3 (2026-08) | 241.2 | 891.5 | 827.3 |

## Leituras combinadas

### O impulso fiscal em quatro medidas

Em p.p. do PIB, + = expansionista. Primário: impulso = −(variação do primário em % do PIB), sem correção pelo ciclo nem por receitas e despesas extraordinárias. EFGG: variação da despesa exceto juros em % do PIB (soma não consolidada das três esferas). Parafiscal: variação do crédito do Tesouro às instituições oficiais em % do PIB (sinal trocado: + = mais crédito). Hiato do BC (edição de 2026-09-01): 0.41% em 3T26, para ler o impulso contra o ciclo.

| Medida | Até | Último (% do PIB) | Antes | Impulso (p.p.) |
|---|---|---|---|---|
| Setor público consolidado, primário 12m (NFSP), variação em 3 meses | 2026-08 | -0.62 | -1.14 | -0.52 |
| Setor público consolidado, primário 12m (NFSP), variação em 12 meses | 2026-08 | -0.62 | -0.19 | +0.43 |
| Governo central, primário 12m (RTN), variação em 3 meses | 2026-08 | -0.53 | -1.06 | -0.53 |
| Governo central, primário 12m (RTN), variação em 12 meses | 2026-08 | -0.53 | -0.24 | +0.29 |
| Governo geral (EFGG), despesa exceto juros 4 tri, variação em 1 ano | 2T26 | 48.78 | 46.83 | +1.95 |
| Parafiscal: créditos do Tesouro a inst. financeiras oficiais (estoque), variação em 1 ano | 2026-08 | 1.75 | 0.86 | +0.89 |

### O preço do risco na convenção do modelo

NTN-B de 10 anos na média dos pregões do trimestre (é a `rr_10a` do Modelo Estrutural) e CDS no último pregão do trimestre (a `fiscal`); o trimestre em curso vai até o último dado. Inflação implícita = (1 + DI)/(1 + NTN-B) − 1, com prêmio de risco de inflação dentro.

| Trimestre | NTN-B 10a, média (`rr_10a`, %) | DI 10a, média (%) | Inflação implícita 10a, média (%) | CDS 5a, fechamento (p.b.) | Pregões |
|---|---|---|---|---|---|
| 2T25 | 7.40 | 13.96 | 6.11 | 149 | 61 |
| 3T25 | 7.46 | 13.64 | 5.75 | 136 | 66 |
| 4T25 | 7.49 | 13.51 | 5.60 | 138 | 62 |
| 1T26 | 7.54 | 13.60 | 5.63 | 140 | 61 |
| 2T26 | 7.67 | 14.00 | 5.88 | 125 | 61 |
| 3T26 | 7.84 | 14.41 | 6.09 | 131 | 65 |
| 4T26 | 6.99 | 13.03 | 5.64 | 137 | 17 |
