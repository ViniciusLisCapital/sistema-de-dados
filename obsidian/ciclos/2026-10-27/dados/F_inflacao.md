# F(A) — inflacao — ciclo 2026-10-27

Gerado em 2026-10-27 13:08. Dados do banco até 2026-10-27, fixos durante o ciclo. Ciclo anterior: 2026-10-02.

Os dados brutos (A) estão em `A/`, um arquivo por tabela; as funções G leem de lá e o código delas fica em `G/`. Nada aqui é opinião: é a mesma conta em todo ciclo.

Como ler:
- **Δ% 1m/3m/12m**: variação contra o último valor de 1, 3 e 12 meses antes da última data da série; numa série trimestral, **1t/4t**: contra 1 e 4 trimestres antes.
- **Δ**: diferença na unidade da série (p.p. quando a série é %, p.b. quando é p.b.).
- **Pctl**: posição do último valor no histórico, de 0 (o menor já visto) a 100 (o maior). "10a" = últimos 10 anos.
- **Soma 3m/12m**: soma dos últimos 3 e 12 meses completos; o mês em curso aparece à parte e não entra nas somas.
- **Acum.**: variação composta.
- **Desde o ciclo ant.**: contra o valor em 2026-10-02.

## i. Endógeno (leitura completa)

### inflc_agregados

Último dado 2026-10-01 (26 dias antes do corte) · A: `A/inflc_agregados.csv.gz`

Variação mensal (%), sem ajuste sazonal. Acumulados compostos. Posição no histórico desde 2000. Grupos e núcleos na classificação do BC.

| Série | Mês | Último mês | Acum. 3m | Acum. 12m | Acum. 12m, 3 meses antes | Pctl acum. 12m hist. |
|---|---|---|---|---|---|---|
| IPCA | 2026-09 | 0.82 | 0.57 | 4.58 | 4.64 | 31 |
| IPCA-15 | 2026-10 | 0.32 | 0.62 | 4.62 | 4.52 | 33 |
| Serviços | 2026-09 | 0.61 | 1.18 | 5.97 | 5.90 | 42 |
| Alimentação | 2026-09 | 0.96 | -0.80 | 4.19 | 3.01 | 32 |
| Bens industriais | 2026-09 | 0.17 | 0.50 | 3.07 | 2.76 | 37 |
| Monitorados | 2026-09 | 1.59 | 0.59 | 4.14 | 5.52 | 32 |
| Livres | 2026-09 | 0.55 | 0.55 | 4.68 | 4.31 | 35 |
| Comercializáveis | 2026-09 | 0.20 | 0.41 | 2.65 | 2.15 | 22 |
| Não comercializáveis | 2026-09 | 0.80 | 0.67 | 6.22 | 5.92 | 53 |
| Núcleo EX0 | 2026-09 | 0.44 | 0.92 | 4.85 | 4.67 | 38 |
| Núcleo EX3 | 2026-09 | 0.26 | 0.78 | 4.65 | 4.64 | 35 |
| Núcleo EX3, serviços | 2026-09 | 0.36 | 1.18 | 5.34 | 5.00 | 37 |
| Núcleo EX3, industriais | 2026-09 | 0.13 | 0.23 | 3.70 | 4.15 | 34 |
| Núcleo EXFE | 2026-09 | 0.35 | 0.87 | 4.71 | 4.70 | 32 |
| Núcleo médias aparadas com suavização | 2026-09 | 0.31 | 0.89 | 4.43 | 4.33 | 26 |
| Núcleo médias aparadas sem suavização | 2026-09 | 0.33 | 0.65 | 3.81 | 3.62 | 31 |
| Núcleo P55 | 2026-09 | 0.42 | 0.97 | 4.68 | 4.54 | 37 |
| Núcleo dupla ponderação | 2026-09 | 0.37 | 0.68 | 4.06 | 4.01 | 22 |

| Série | Unidade | Data | Último | Δ 1m | Δ 3m | Δ 12m | Δ desde o ciclo ant. | Pctl 10a | Pctl hist. | Mín–máx 10a |
|---|---|---|---|---|---|---|---|---|---|---|
| Índice de difusão | % dos subitens com alta | 2026-09-01 | 54.9 | +0.5 | +1.3 | +2.7 | sem dado novo | 31 | 18 | 41.8 a 78.2 |
| IPCA acumulado em 12 meses (publicado) | % | 2026-09-01 | 4.58 | +0.36 | -0.06 | -0.59 | sem dado novo | 56 | 30 | 1.88 a 12.13 |

### inflc_indice_geral

Último dado 2026-10-01 (26 dias antes do corte) · A: `A/inflc_indice_geral.csv.gz`

IPCA, últimos seis meses (IBGE/SIDRA):

| Mês | Número-índice | No mês (%) | No ano (%) | 12 meses (%) |
|---|---|---|---|---|
| 2026-09 | 7695.82 | 0.82 | 3.95 | 4.58 |
| 2026-08 | 7633.23 | -0.32 | 3.11 | 4.22 |
| 2026-07 | 7657.73 | 0.07 | 3.44 | 4.44 |
| 2026-06 | 7652.37 | 0.16 | 3.36 | 4.64 |
| 2026-05 | 7640.15 | 0.58 | 3.20 | 4.72 |
| 2026-04 | 7596.09 | 0.67 | 2.60 | 4.39 |

IPCA-15, últimos seis meses (IBGE/SIDRA):

| Mês | Número-índice | No mês (%) | No ano (%) | 12 meses (%) |
|---|---|---|---|---|
| 2026-10 | 7567.08 | 0.32 | 4.15 | 4.62 |
| 2026-09 | 7542.94 | 0.70 | 3.82 | 4.47 |
| 2026-08 | 7490.51 | -0.40 | 3.09 | 4.24 |
| 2026-07 | 7520.59 | 0.06 | 3.51 | 4.52 |
| 2026-06 | 7516.08 | 0.41 | 3.45 | 4.80 |
| 2026-05 | 7485.39 | 0.62 | 3.02 | 4.64 |

IPCA acumulado em 12 meses no fechamento dos últimos oito trimestres (a variável da tese e do placar):

| Trimestre | Mês de fechamento | IPCA 12 meses (%) |
|---|---|---|
| 3T26 | 2026-09 | 4.58 |
| 2T26 | 2026-06 | 4.64 |
| 1T26 | 2026-03 | 4.14 |
| 4T25 | 2025-12 | 4.26 |
| 3T25 | 2025-09 | 5.17 |
| 2T25 | 2025-06 | 5.35 |
| 1T25 | 2025-03 | 5.48 |
| 4T24 | 2024-12 | 4.83 |

### inflc_decomposicao

Último dado 2026-10-01 (26 dias antes do corte) · A: `A/inflc_decomposicao.csv.gz`

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

Último dado 2026-10-01 (26 dias antes do corte) · A: `A/inflc_decomposicao_item.csv.gz`

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

### comm_icbr

Último dado 2026-09-01 (56 dias antes do corte) · A: `A/comm_icbr.csv.gz`

| Série | Unidade | Data | Último | Δ% 1m | Δ% 3m | Δ% 12m | Δ% desde o ciclo ant. | Pctl 10a | Pctl hist. | Pctl Δ12m hist. | Mín–máx 10a |
|---|---|---|---|---|---|---|---|---|---|---|---|
| IC-Br | índice, em R$ | 2026-09-01 | 462.94 | +1.5 | +4.5 | +8.1 | sem dado novo | 98 | 99 | 51 | 154.23 a 482.57 |
| IC-Br agropecuária | índice, em R$ | 2026-09-01 | 454.03 | +0.1 | +3.8 | -3.5 | sem dado novo | 89 | 96 | 23 | 160.08 a 537.72 |
| IC-Br metal | índice, em R$ | 2026-09-01 | 754.19 | -0.8 | +1.1 | +36.3 | sem dado novo | 98 | 99 | 83 | 182.41 a 772.65 |
| IC-Br energia | índice, em R$ | 2026-09-01 | 216.23 | +10.4 | +11.7 | +23.8 | sem dado novo | 89 | 96 | 72 | 73.58 a 330.55 |

## ii. Endógeno de câmbio (leitura enxuta)

### cmb_ptax

Último dado 2026-10-26 (1 dia antes do corte) · A: `A/cmb_ptax.csv.gz`

| Série | Unidade | Data | Último | Δ% 1m | Δ% 3m | Δ% 12m | Δ% desde o ciclo ant. |
|---|---|---|---|---|---|---|---|
| PTAX venda | R$/US$ | 2026-10-26 | 5.5007 | +5.8 | +8.6 | +2.2 | +5.3 |

## iii. Endógeno de política monetária (leitura enxuta)

### inflc_meta

Último dado 2026-01-01 (299 dias antes do corte) · A: `A/inflc_meta.csv.gz`

| Ano | Meta (%) |
|---|---|
| 2024 | 3.00 |
| 2025 | 3.00 |
| 2026 | 3.00 |

### pm_copom_projecoes

Último dado 2026-09-24 (33 dias antes do corte) · A: `A/pm_copom_projecoes.csv.gz`

Reunião 281 (de 2026-09-24), Relatório de Política Monetária, cenário de referência (juros da Focus). Valor = acumulado em quatro trimestres. Os condicionantes (petróleo, bandeira, câmbio) estão no texto do Copom e chegam pela IN-S4.

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

O horizonte relevante nas últimas reuniões:

| Reunião | Documento | Data | Horizonte relevante | IPCA projetado (%) |
|---|---|---|---|---|
| 281 | relatorio | 2026-09-24 | 1T28 | 3.2 |
| 280 | comunicado | 2026-08-05 | 1T28 | 3.2 |
| 279 | relatorio | 2026-06-25 | 4T27 | 3.7 |
| 278 | comunicado | 2026-04-29 | 4T27 | 3.5 |

## iv. Endógeno de atividade (leitura enxuta)

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

### atv_pms

Último dado 2026-08-01 (87 dias antes do corte) · A: `A/atv_pms.csv.gz`

| Série | Unidade | Data | Último | Δ% 1m | Δ% 3m | Δ% 12m | Δ% desde o ciclo ant. |
|---|---|---|---|---|---|---|---|
| Serviços, total | índice, dessaz. | 2026-08-01 | 110.51 | -0.1 | +0.1 | +0.6 | sem dado novo |
| Prestados às famílias | índice, dessaz. | 2026-08-01 | 115.63 | +2.1 | +1.5 | +4.2 | sem dado novo |
| Informação e comunicação | índice, dessaz. | 2026-08-01 | 122.02 | -0.0 | -0.5 | +4.8 | sem dado novo |
| Profissionais e administrativos | índice, dessaz. | 2026-08-01 | 118.91 | -0.2 | -0.9 | +1.5 | sem dado novo |
| Transportes e correio | índice, dessaz. | 2026-08-01 | 100.98 | -0.2 | +0.2 | -3.1 | sem dado novo |

### mt_pnad

Último dado 2026-08-01 (87 dias antes do corte) · A: `A/mt_pnad.csv.gz`

| Série | Unidade | Data | Último | Δ 1m | Δ 3m | Δ 12m | Δ desde o ciclo ant. |
|---|---|---|---|---|---|---|---|
| Taxa de desocupação | % | 2026-08-01 | 5.3 | +0.0 | -0.3 | -0.3 | sem dado novo |
| Informalidade | % dos ocupados | 2026-08-01 | 37.5 | +0.0 | +0.2 | -0.5 | sem dado novo |

| Série | Unidade | Data | Último | Δ% 1m | Δ% 3m | Δ% 12m | Δ% desde o ciclo ant. |
|---|---|---|---|---|---|---|---|
| Rendimento habitual real | R$ | 2026-08-01 | 3777 | +0.5 | +0.7 | +3.7 | sem dado novo |
| Massa de rendimento habitual real | R$ bi | 2026-08-01 | 385.6 | +0.6 | +1.4 | +4.8 | sem dado novo |
| Ocupados | mil pessoas | 2026-08-01 | 103477 | +0.1 | +0.8 | +1.0 | sem dado novo |

### mt_desocupacao_retro

Último dado 2026-09-01 (56 dias antes do corte) · A: `A/mt_desocupacao_retro.csv.gz`

| Série | Unidade | Data | Último | Δ 1m | Δ 3m | Δ 12m | Δ desde o ciclo ant. |
|---|---|---|---|---|---|---|---|
| Desocupação dessazonalizada, retropolada pelo BC | % | 2026-07-01 | 5.41 | -0.02 | -0.01 | -0.32 | sem dado novo |

### mt_caged

Último dado 2026-08-01 (87 dias antes do corte) · A: `A/mt_caged.csv.gz`

| Série | Unidade | Data | Último | Δ% 1m | Δ% 3m | Δ% 12m | Δ% desde o ciclo ant. |
|---|---|---|---|---|---|---|---|
| Estoque de emprego formal | mil empregos | 2026-08-01 | 48245 | +0.3 | +0.7 | +1.9 | sem dado novo |
| Serviços | mil empregos | 2026-08-01 | 23587 | +0.5 | +0.9 | +2.9 | sem dado novo |

## v. Endógeno de expectativas (leitura enxuta)

### expc_focus

Último dado 2026-10-23 (4 dias antes do corte) · A: `A/expc_focus.csv.gz`

| Série | Unidade | Data | Último | Δ 1m | Δ 3m | Δ 12m | Δ desde o ciclo ant. |
|---|---|---|---|---|---|---|---|
| IPCA 12 meses à frente (suavizada) | % | 2026-10-23 | 4.53 | -0.07 | +0.35 | +0.41 | -0.06 |
| IPCA 24 meses à frente | % | 2026-10-23 | 3.87 | -0.04 | -0.06 | -0.13 | -0.08 |
| IPCA livres 12 meses à frente (suavizada) | % | 2026-10-23 | 4.80 | +0.07 | +0.30 | +0.39 | +0.03 |
| IPCA administrados 12 meses à frente (suavizada) | % | 2026-10-23 | 4.10 | -0.30 | +0.63 | +1.08 | -0.03 |
| IPCA serviços 12 meses à frente (suavizada) | % | 2026-10-23 | 5.20 | +0.05 | +0.04 | -0.12 | +0.05 |
| IPCA bens industrializados 12 meses à frente (suavizada) | % | 2026-10-23 | 2.60 | -0.08 | -0.16 | -0.09 | -0.08 |
| IPCA alimentação no domicílio 12 meses à frente (suavizada) | % | 2026-10-23 | 6.77 | -0.16 | +1.47 | +1.65 | -0.18 |
| IGP-M 12 meses à frente (suavizada) | % | 2026-10-23 | 4.28 | -0.45 | -0.19 | -0.33 | -0.36 |

### expc_focus_periodo (IPCA)

Último dado 2026-10-23 (4 dias antes do corte) · A: `A/expc_focus_periodo__ipca.csv.gz`

Unidade: %. Mediana da pesquisa (janela de 30 dias).

| Ano | Mediana (2026-10-23) | 4 sem. antes (2026-09-25) | 13 sem. antes (2026-07-24) | Δ 4 sem. | Ciclo ant. (2026-10-02) | Respondentes |
|---|---|---|---|---|---|---|
| 2026 | 5.19 | 4.99 | 5.12 | +0.20 | 5.01 | 142 |
| 2027 | 4.34 | 4.31 | 4.22 | +0.03 | 4.30 | 142 |
| 2028 | 3.75 | 3.80 | 3.80 | -0.05 | 3.80 | 124 |
| 2029 | 3.50 | 3.50 | 3.50 | -0.00 | 3.51 | 116 |

### expc_focus_periodo (componentes)

Último dado 2026-10-23 (4 dias antes do corte) · A: `A/expc_focus_periodo__componentes__inflacao.csv.gz`

**IGP-M**

Unidade: %. Mediana da pesquisa (janela de 30 dias).

| Ano | Mediana (2026-10-23) | 4 sem. antes (2026-09-25) | 13 sem. antes (2026-07-24) | Δ 4 sem. | Ciclo ant. (2026-10-02) | Respondentes |
|---|---|---|---|---|---|---|
| 2026 | 5.61 | 4.76 | 5.42 | +0.85 | 5.27 | 63 |
| 2027 | 4.01 | 4.11 | 4.16 | -0.10 | 4.11 | 61 |
| 2028 | 3.92 | 3.92 | 3.96 | +0.00 | 3.94 | 56 |
| 2029 | 3.80 | 3.81 | 3.90 | -0.01 | 3.80 | 53 |

**IPCA Administrados**

Unidade: %. Mediana da pesquisa (janela de 30 dias).

| Ano | Mediana (2026-10-23) | 4 sem. antes (2026-09-25) | 13 sem. antes (2026-07-24) | Δ 4 sem. | Ciclo ant. (2026-10-02) | Respondentes |
|---|---|---|---|---|---|---|
| 2026 | 4.80 | 4.62 | 5.00 | +0.17 | 4.61 | 98 |
| 2027 | 3.99 | 3.82 | 3.90 | +0.17 | 3.84 | 97 |
| 2028 | 3.63 | 3.62 | 3.50 | +0.01 | 3.62 | 71 |
| 2029 | 3.50 | 3.50 | 3.50 | +0.00 | 3.50 | 67 |

**IPCA Alimentação no domicílio**

Unidade: %. Mediana da pesquisa (janela de 30 dias).

| Ano | Mediana (2026-10-23) | 4 sem. antes (2026-09-25) | 13 sem. antes (2026-07-24) | Δ 4 sem. | Ciclo ant. (2026-10-02) | Respondentes |
|---|---|---|---|---|---|---|
| 2026 | 7.38 | 6.85 | 6.58 | +0.53 | 6.88 | 93 |
| 2027 | 5.76 | 5.66 | 5.39 | +0.10 | 5.66 | 92 |
| 2028 | 4.00 | 4.00 | 4.00 | +0.00 | 4.00 | 65 |
| 2029 | 4.00 | 4.00 | 3.82 | +0.00 | 4.00 | 61 |

**IPCA Bens industrializados**

Unidade: %. Mediana da pesquisa (janela de 30 dias).

| Ano | Mediana (2026-10-23) | 4 sem. antes (2026-09-25) | 13 sem. antes (2026-07-24) | Δ 4 sem. | Ciclo ant. (2026-10-02) | Respondentes |
|---|---|---|---|---|---|---|
| 2026 | 3.44 | 3.50 | 3.60 | -0.06 | 3.50 | 92 |
| 2027 | 2.71 | 2.73 | 2.70 | -0.02 | 2.73 | 91 |
| 2028 | 2.80 | 2.80 | 2.70 | +0.00 | 2.80 | 64 |
| 2029 | 2.98 | 2.98 | 2.80 | +0.00 | 2.98 | 60 |

**IPCA Livres**

Unidade: %. Mediana da pesquisa (janela de 30 dias).

| Ano | Mediana (2026-10-23) | 4 sem. antes (2026-09-25) | 13 sem. antes (2026-07-24) | Δ 4 sem. | Ciclo ant. (2026-10-02) | Respondentes |
|---|---|---|---|---|---|---|
| 2026 | 5.31 | 5.11 | 5.23 | +0.20 | 5.14 | 94 |
| 2027 | 4.52 | 4.48 | 4.41 | +0.04 | 4.49 | 92 |
| 2028 | 3.90 | 3.90 | 3.90 | +0.00 | 3.90 | 66 |
| 2029 | 3.66 | 3.56 | 3.54 | +0.10 | 3.56 | 62 |

**IPCA Serviços**

Unidade: %. Mediana da pesquisa (janela de 30 dias).

| Ano | Mediana (2026-10-23) | 4 sem. antes (2026-09-25) | 13 sem. antes (2026-07-24) | Δ 4 sem. | Ciclo ant. (2026-10-02) | Respondentes |
|---|---|---|---|---|---|---|
| 2026 | 5.62 | 5.45 | 5.66 | +0.17 | 5.47 | 92 |
| 2027 | 5.16 | 5.07 | 5.10 | +0.08 | 5.07 | 91 |
| 2028 | 4.65 | 4.50 | 4.50 | +0.15 | 4.50 | 65 |
| 2029 | 4.10 | 4.00 | 4.00 | +0.10 | 4.00 | 61 |

### expc_qpc

Último dado 2026-09-23 (34 dias antes do corte) · A: `A/expc_qpc.csv.gz`

QPC da reunião 281 (publicado em 2026-09-23). Medianas.

| Variável | Referência | Mediana | p25 a p75 | Última vez perguntado |
|---|---|---|---|---|
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
| IPCA no horizonte relevante, 4 trimestres (%) | 2028T1 | 4.00 | 3.77 a 4.20 | — |

Probabilidade de o IPCA no horizonte relevante desviar da meta, mediana das respostas: abaixo 0,5 p.p. 15%; acima 0,5 p.p. 25%; entre 0,5 p.p. 60%.

Balanço de riscos do IPCA, fatia das respostas: 2026: risco de alta 33%, risco de baixa 6%, riscos equilibrados 60% · 2027: risco de alta 60%, risco de baixa 5%, riscos equilibrados 35%.

## vi. Endógeno de externo (leitura enxuta)

### comm_icbr_usd

Último dado 2026-09-01 (56 dias antes do corte) · A: `A/comm_icbr_usd.csv.gz`

| Série | Unidade | Data | Último | Δ% 1m | Δ% 3m | Δ% 12m | Δ% desde o ciclo ant. |
|---|---|---|---|---|---|---|---|
| IC-Br em dólar | índice | 2026-09-01 | 205.70 | +1.7 | +4.1 | +12.8 | sem dado novo |
| IC-Br agropecuária | índice | 2026-09-01 | 201.80 | +0.3 | +3.3 | +0.7 | sem dado novo |
| IC-Br metal | índice | 2026-09-01 | 335.06 | -0.6 | +0.7 | +42.2 | sem dado novo |
| IC-Br energia | índice | 2026-09-01 | 96.00 | +10.6 | +11.2 | +29.2 | sem dado novo |

### comm_brent

Último dado 2026-10-20 (7 dias antes do corte) · A: `A/comm_brent.csv.gz`

| Série | Unidade | Data | Último | Δ% 1m | Δ% 3m | Δ% 12m | Δ% desde o ciclo ant. |
|---|---|---|---|---|---|---|---|
| Brent | US$/barril | 2026-10-20 | 115.22 | -3.7 | +32.5 | +89.8 | -15.0 |

## Leituras combinadas

### O IPCA e os quatro grupos por trimestre

Variação composta dos meses do trimestre (%, sem ajuste sazonal), como a curva de Phillips do Modelo Estrutural a lê. Os quatro grupos são os do modelo (classificação do BC). O trimestre em curso aparece com os meses que já saíram.

| Trimestre | IPCA | Serviços | Alimentação | Bens industriais | Monitorados |
|---|---|---|---|---|---|
| 3T24 | 0.80 | 1.14 | -1.68 | 0.67 | 1.98 |
| 4T24 | 1.48 | 1.85 | 4.26 | 1.08 | -0.34 |
| 1T25 | 2.04 | 2.24 | 3.20 | 1.24 | 1.77 |
| 2T25 | 0.93 | 0.78 | 0.42 | 0.72 | 1.66 |
| 3T25 | 0.63 | 1.11 | -1.92 | 0.20 | 1.93 |
| 4T25 | 0.60 | 1.74 | -0.22 | 0.22 | -0.17 |
| 1T26 | 1.92 | 2.15 | 2.28 | 1.27 | 1.93 |
| 2T26 | 1.42 | 0.77 | 2.91 | 1.05 | 1.74 |
| 3T26 | 0.57 | 1.18 | -0.80 | 0.50 | 0.59 |

Acumulado em 12 meses no fechamento de cada trimestre (%), a variável da tese:

| Trimestre | IPCA | Serviços | Alimentação | Bens industriais | Monitorados |
|---|---|---|---|---|---|
| 3T24 | 4.42 | 4.80 | 6.27 | 1.52 | 5.47 |
| 4T24 | 4.83 | 4.74 | 8.22 | 2.87 | 4.66 |
| 1T25 | 5.48 | 5.84 | 7.85 | 3.67 | 5.12 |
| 2T25 | 5.35 | 6.14 | 6.23 | 3.76 | 5.16 |
| 3T25 | 5.17 | 6.11 | 5.97 | 3.28 | 5.10 |
| 4T25 | 4.26 | 6.00 | 1.42 | 2.39 | 5.28 |
| 1T26 | 4.14 | 5.91 | 0.51 | 2.42 | 5.44 |
| 2T26 | 4.64 | 5.90 | 3.01 | 2.76 | 5.52 |
| 3T26 | 4.58 | 5.97 | 4.19 | 3.07 | 4.14 |

### O último mês contra o mesmo mês dos dez anos anteriores

Sem ajuste sazonal: a comparação com o mesmo mês é o padrão sazonal medido. "Anos abaixo do atual" conta em quantos dos dez anos anteriores aquele mês foi menor.

| Série | Mês | Último (%) | Mesmo mês, média 10a | Mín–máx 10a | Anos abaixo do atual | Último − média |
|---|---|---|---|---|---|---|
| IPCA | 2026-09 | 0.82 | 0.34 | -0.29 a 1.16 | 9 de 10 | +0.48 |
| Serviços | 2026-09 | 0.61 | 0.33 | 0.05 a 0.63 | 9 de 10 | +0.28 |
| Alimentação | 2026-09 | 0.96 | 0.03 | -1.02 a 2.89 | 8 de 10 | +0.93 |
| Bens industriais | 2026-09 | 0.17 | 0.23 | -0.20 a 1.04 | 6 de 10 | -0.06 |
| Monitorados | 2026-09 | 1.59 | 0.65 | -1.21 a 1.93 | 8 de 10 | +0.94 |
| Núcleo EX3 | 2026-09 | 0.26 | 0.28 | 0.06 a 0.70 | 5 de 10 | -0.02 |
| Núcleo médias aparadas | 2026-09 | 0.31 | 0.31 | 0.13 a 0.63 | 6 de 10 | +0.00 |

A mesma comparação para os três meses até o último:

| Série | 3 meses até | Acum. 3m (%) | Mesma janela, média 10a | Mín–máx 10a | Anos abaixo do atual |
|---|---|---|---|---|---|
| IPCA | 2026-09 | 0.57 | 0.76 | -1.32 a 3.02 | 2 de 10 |
| Serviços | 2026-09 | 1.18 | 0.98 | -0.40 a 1.70 | 7 de 10 |
| Alimentação | 2026-09 | -0.80 | -0.29 | -3.36 a 4.22 | 6 de 10 |
| Bens industriais | 2026-09 | 0.50 | 0.68 | 0.04 a 2.77 | 6 de 10 |
| Monitorados | 2026-09 | 0.59 | 1.25 | -7.92 a 4.63 | 2 de 10 |
| Núcleo EX3 | 2026-09 | 0.78 | 0.91 | 0.31 a 2.43 | 7 de 10 |
| Núcleo médias aparadas | 2026-09 | 0.89 | 1.02 | 0.43 a 1.90 | 5 de 10 |

### Os preços monitorados, item a item

IPCA de 2026-09. Subitens monitorados pela classificação do BC, somados no item do IBGE; variação ponderada pelos pesos de cada mês. Peso dos monitorados no mês: 26.0%. Nenhum destes canais está no Modelo Estrutural, salvo pela inércia e pela indexação ao IPCA (mapa, 2.7).

| Item | Peso (%) | No mês (%) | Acum. 3m (%) | Acum. 12m (%) | Contribuição no mês (p.p.) | Soma das contribuições 12m (p.p.) |
|---|---|---|---|---|---|---|
| Combustíveis (veículos) | 5.45 | 1.22 | -0.71 | 5.95 | 0.066 | 0.32 |
| Plano de saúde | 4.17 | 0.42 | 1.27 | 5.69 | 0.018 | 0.23 |
| Energia elétrica residencial | 3.98 | 7.98 | 2.82 | 2.76 | 0.318 | 0.11 |
| Produtos farmacêuticos | 3.49 | 0.02 | 0.30 | 4.04 | 0.001 | 0.14 |
| Veículo próprio | 2.76 | -0.01 | -0.02 | -0.06 | -0.000 | -0.00 |
| Transporte público | 2.01 | 0.03 | 0.22 | 4.91 | 0.001 | 0.10 |
| Aluguel e taxas | 1.90 | 0.13 | 0.64 | 6.32 | 0.002 | 0.12 |
| Combustíveis (domésticos) | 1.39 | 0.51 | -0.40 | 3.54 | 0.007 | 0.05 |
| Recreação | 0.48 | 0.00 | 0.00 | 0.00 | 0.000 | 0.00 |
| Comunicação | 0.27 | 0.00 | 0.00 | 1.12 | 0.000 | 0.00 |
| Serviços pessoais | 0.07 | 0.29 | 0.87 | 4.65 | 0.000 | 0.00 |
