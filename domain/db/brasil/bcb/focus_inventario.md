# Focus / Expectativas de Mercado — inventário de cobertura

Medido ao vivo contra a API Olinda em **2026-08-17** (`https://olinda.bcb.gov.br/olinda/servico/Expectativas/versao/v1/odata`).
Existe porque redescobrir isso custa ~100 chamadas à API, e porque nenhuma das quatro
descontinuações abaixo é visível na documentação do serviço — só medindo `MIN(Data)`/`MAX(Data)`
por indicador. Consumido por `expc_focus.py`, `expc_focus_copom.py` e `expc_focus_periodo.py`,
que carregam **só o que ainda é publicado**.

A API expõe 13 recursos: 6 de consenso geral, 6 espelhos Top5 (as 5 instituições mais assertivas)
e `DatasReferencia` (metadado, sem série). Três formas de chave, daí as três tabelas — ver
[`../../CLAUDE.md`](../../CLAUDE.md).

## As quatro reformulações da pesquisa

Séries com início/fim descontínuos. Ler antes de graficar qualquer coisa, ou um gráfico "de
1999 até hoje" aparece cortado no meio sem explicação:

| data | o que mudou |
|---|---|
| 2018-07-05 | Top5 IGP-DI encerrado |
| **2021-02-17** | a família antiga de índices de preços encerrada no mesmo dia em **todos** os endpoints: IGP-DI, INPC, IPA-DI, IPA-M, IPC-Fipe, IPCA-15 |
| **2021-09-13 → 09-14** | troca em um dia. Sai "Produção industrial"; saem PIB Agropecuária/Indústria/Serviços do endpoint **trimestral** (as versões **anuais** seguem vivas — assimetria real, não erro). Entram os 5 componentes do IPCA, Taxa de desocupação, os 5 componentes de demanda do PIB, e Câmbio/IPCA trimestrais |
| 2026-01-29 | Top5 IGP-M e Top5 IPCA Administrados encerrados |

Fora disso, `base_calculo=1` (janela de 4 dias úteis) também não cobre o histórico todo: começa
em **2014-01-02** nos endpoints de inflação e em **2021-03-31** no de Selic, contra 2001-11 e
2004-11 da base 0. Não é falha de carga.

## Volume (linhas em 2025, filtro de carga aplicado)

| endpoint | linhas em 2025 |
|---|---|
| `ExpectativaMercadoMensais` | 52.920 |
| `ExpectativasMercadoAnuais` | 40.307 |
| `ExpectativasMercadoTrimestrais` | 17.640 |
| `ExpectativasMercadoSelic` | 4.032 |
| `ExpectativasMercadoInflacao12Meses` | 1.764 |
| `ExpectativasMercadoInflacao24Meses` | 1.512 |
| Top5 (6 endpoints somados) | ~91.700 |

~250 dias de pesquisa por ano, ~440 linhas por dia nos três endpoints de período de referência.

## Cobertura por endpoint × indicador

### `ExpectativaMercadoMensais` → `expc_focus_periodo`

| indicador | primeira | ultima | |
|---|---|---|---|
| Câmbio | 2001-11-06 | 2026-08-14 |  |
| IGP-M | 2001-01-04 | 2026-08-14 |  |
| IPCA | 2000-01-03 | 2026-08-14 |  |
| IPCA Administrados | 2021-09-15 | 2026-08-14 |  |
| IPCA Alimentação no domicílio | 2021-09-14 | 2026-08-14 |  |
| IPCA Bens industrializados | 2021-09-14 | 2026-08-14 |  |
| IPCA Livres | 2021-09-14 | 2026-08-14 |  |
| IPCA Serviços | 2021-09-14 | 2026-08-14 |  |
| Taxa de desocupação | 2021-09-14 | 2026-08-14 |  |
| IGP-DI | 2001-04-10 | 2021-02-17 | **encerrado** |
| INPC | 2000-01-03 | 2021-02-17 | **encerrado** |
| IPA-DI | 2001-11-06 | 2021-02-17 | **encerrado** |
| IPA-M | 2001-11-06 | 2021-02-17 | **encerrado** |
| IPC-Fipe | 2000-01-03 | 2021-02-17 | **encerrado** |
| IPCA-15 | 2001-11-06 | 2021-02-17 | **encerrado** |
| Produção industrial | 2001-11-06 | 2021-09-13 | **encerrado** |

### `ExpectativasMercadoTrimestrais` → `expc_focus_periodo`

| indicador | primeira | ultima | |
|---|---|---|---|
| Câmbio | 2021-09-14 | 2026-08-14 |  |
| IPCA | 2021-09-14 | 2026-08-14 |  |
| IPCA Administrados | 2021-09-15 | 2026-08-14 |  |
| IPCA Alimentação no domicílio | 2021-09-14 | 2026-08-14 |  |
| IPCA Bens industrializados | 2021-09-14 | 2026-08-14 |  |
| IPCA Livres | 2021-09-14 | 2026-08-14 |  |
| IPCA Serviços | 2021-09-14 | 2026-08-14 |  |
| PIB Total | 2001-11-06 | 2026-08-14 |  |
| Taxa de desocupação | 2021-09-14 | 2026-08-14 |  |
| PIB Agropecuária | 2001-11-06 | 2021-09-13 | **encerrado** |
| PIB Indústria | 2001-11-06 | 2021-09-13 | **encerrado** |
| PIB Serviços | 2001-11-06 | 2021-09-13 | **encerrado** |

### `ExpectativasMercadoAnuais` → `expc_focus_periodo`

| indicador | primeira | ultima | |
|---|---|---|---|
| Balança comercial | 2000-01-03 | 2026-08-14 |  |
| Conta corrente | 2000-01-03 | 2026-08-14 |  |
| Câmbio | 2000-01-03 | 2026-08-14 |  |
| Dívida bruta do governo geral | 2018-01-22 | 2026-08-14 |  |
| Dívida líquida do setor público | 2000-01-03 | 2026-08-14 |  |
| IGP-M | 1999-04-30 | 2026-08-14 |  |
| IPCA | 2000-01-03 | 2026-08-14 |  |
| IPCA Administrados | 2003-05-27 | 2026-08-14 |  |
| IPCA Alimentação no domicílio | 2021-09-14 | 2026-08-14 |  |
| IPCA Bens industrializados | 2021-09-14 | 2026-08-14 |  |
| IPCA Livres | 2021-09-14 | 2026-08-14 |  |
| IPCA Serviços | 2021-09-14 | 2026-08-14 |  |
| Investimento direto no país | 2000-01-03 | 2026-08-14 |  |
| PIB Agropecuária | 2001-01-02 | 2026-08-14 |  |
| PIB Despesa de consumo da administração pública | 2021-09-14 | 2026-08-14 |  |
| PIB Despesa de consumo das famílias | 2021-09-14 | 2026-08-14 |  |
| PIB Exportação de bens e serviços | 2021-09-17 | 2026-08-14 |  |
| PIB Formação Bruta de Capital Fixo | 2021-09-14 | 2026-08-14 |  |
| PIB Importação de bens e serviços | 2021-09-17 | 2026-08-14 |  |
| PIB Indústria | 2001-01-02 | 2026-08-14 |  |
| PIB Serviços | 2001-01-02 | 2026-08-14 |  |
| PIB Total | 1999-07-01 | 2026-08-14 |  |
| Resultado nominal | 2001-11-06 | 2026-08-14 |  |
| Resultado primário | 2000-01-03 | 2026-08-14 |  |
| Selic | 2000-01-03 | 2026-08-14 |  |
| Taxa de desocupação | 2021-09-14 | 2026-08-14 |  |
| IGP-DI | 1999-04-30 | 2021-02-17 | **encerrado** |
| INPC | 2000-01-03 | 2021-02-17 | **encerrado** |
| IPA-DI | 1999-05-18 | 2021-02-17 | **encerrado** |
| IPA-M | 2001-01-02 | 2021-02-17 | **encerrado** |
| IPC-Fipe | 2000-01-03 | 2021-02-17 | **encerrado** |
| IPCA-15 | 2001-05-17 | 2021-02-17 | **encerrado** |
| Produção industrial | 2001-11-06 | 2021-09-13 | **encerrado** |

### `ExpectativasMercadoInflacao12Meses` → `expc_focus`

| indicador | primeira | ultima | |
|---|---|---|---|
| IGP-M | 2001-11-07 | 2026-08-14 |  |
| IPCA | 2001-11-07 | 2026-08-14 |  |
| IPCA Administrados | 2021-09-17 | 2026-08-14 |  |
| IPCA Alimentação no domicílio | 2021-09-14 | 2026-08-14 |  |
| IPCA Bens industrializados | 2021-09-14 | 2026-08-14 |  |
| IPCA Livres | 2021-09-14 | 2026-08-14 |  |
| IPCA Serviços | 2021-09-14 | 2026-08-14 |  |
| IGP-DI | 2001-11-07 | 2021-02-17 | **encerrado** |
| INPC | 2001-11-07 | 2021-02-17 | **encerrado** |
| IPA-DI | 2001-11-07 | 2021-02-17 | **encerrado** |
| IPA-M | 2001-11-07 | 2021-02-17 | **encerrado** |
| IPC-Fipe | 2001-11-07 | 2021-02-17 | **encerrado** |
| IPCA-15 | 2001-11-07 | 2021-02-17 | **encerrado** |

### `ExpectativasMercadoInflacao24Meses` → `expc_focus`

| indicador | primeira | ultima | |
|---|---|---|---|
| IPCA | 2021-03-31 | 2026-08-14 |  |
| IPCA Administrados | 2021-09-17 | 2026-08-14 |  |
| IPCA Alimentação no domicílio | 2021-09-14 | 2026-08-14 |  |
| IPCA Bens industrializados | 2021-09-14 | 2026-08-14 |  |
| IPCA Livres | 2021-09-14 | 2026-08-14 |  |
| IPCA Serviços | 2021-09-14 | 2026-08-14 |  |

### `ExpectativasMercadoSelic` — (sem indicadores enumerados: campo Indicador em minuscula)

### `ExpectativasMercadoTop5Mensais` → **nao carregado**

| indicador | primeira | ultima | |
|---|---|---|---|
| Câmbio | 2001-11-06 | 2026-08-14 |  |
| IPCA | 2001-11-06 | 2026-08-14 |  |
| Taxa de desocupação | 2022-05-11 | 2026-08-14 |  |
| IGP-DI | 2001-11-06 | 2018-07-05 | **encerrado** |
| IGP-M | 2001-11-16 | 2026-01-29 | **encerrado** |

### `ExpectativaMercadoTop5Trimestral` → **nao carregado**

| indicador | primeira | ultima | |
|---|---|---|---|
| Câmbio | 2021-09-14 | 2026-08-14 |  |
| IPCA | 2021-09-14 | 2026-08-14 |  |
| PIB Total | 2023-03-31 | 2026-08-14 |  |
| Taxa de desocupação | 2022-05-11 | 2026-08-14 |  |

### `ExpectativasMercadoTop5Anuais` → **nao carregado**

| indicador | primeira | ultima | |
|---|---|---|---|
| Câmbio | 2001-11-06 | 2026-08-14 |  |
| IPCA | 2001-11-06 | 2026-08-14 |  |
| PIB Total | 2023-03-31 | 2026-08-14 |  |
| Selic | 2001-11-06 | 2026-08-14 |  |
| Taxa de desocupação | 2022-05-11 | 2026-08-14 |  |
| IGP-DI | 2001-11-06 | 2018-07-05 | **encerrado** |
| IGP-M | 2001-11-16 | 2026-01-29 | **encerrado** |
| IPCA Administrados | 2022-04-08 | 2026-01-29 | **encerrado** |

### `ExpectativasMercadoTop5Inflacao12Meses` → **nao carregado**

| indicador | primeira | ultima | |
|---|---|---|---|
| IPCA | 2001-11-06 | 2026-08-14 |  |
| IGP-DI | 2001-11-06 | 2018-07-05 | **encerrado** |
| IGP-M | 2001-11-16 | 2026-01-29 | **encerrado** |
| IPCA Administrados | 2022-04-08 | 2026-01-29 | **encerrado** |

### `ExpectativasMercadoTop5Inflacao24Meses` → **nao carregado**

| indicador | primeira | ultima | |
|---|---|---|---|
| IPCA | 2021-03-31 | 2026-08-14 |  |
| IPCA Administrados | 2022-04-08 | 2026-01-29 | **encerrado** |

### `ExpectativasMercadoTop5Selic` — (sem indicadores enumerados: campo Indicador em minuscula)

## Notas de leitura

- **`ExpectativasMercadoTop5Selic`** não aparece com indicadores acima porque é o único recurso
  cujos campos vêm em minúscula (`indicador`, `mediana`, `reuniao`, mais `coeficienteVariacao`,
  que nenhum outro tem). Um filtro OData `Indicador eq ...` nele devolve 400.
- **`tipoCalculo`** (dimensão exclusiva dos Top5) vale `C`/`M`/`L` nos endpoints mensal/
  trimestral/anual e `CURTO_PRAZO`/`MEDIO_PRAZO`/`LONGO_PRAZO` nos de inflação — mesma ideia,
  codificação diferente por endpoint.
- **`IndicadorDetalhe`** existe só em `ExpectativasMercadoAnuais`, e só "Balança comercial" o
  usa (Exportações / Importações / Saldo). Todo o resto vem nulo.
- **Horizonte cotado à frente**, na última data de pesquisa: 25 meses (mensal), 8 trimestres
  (trimestral), 5 anos (anual), 16 reuniões (Selic).
- **Quantas reuniões o Focus cota à frente cresceu**: 1 em 2004, ~9 entre 2007-2009, ~12 de
  2010 a 2020, 16 desde 2021. Propriedade da fonte, não da carga.
