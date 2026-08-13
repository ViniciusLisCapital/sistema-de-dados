# Fiscal — mapeamento de fontes (BCB / Tesouro Nacional / IPEA / outros)

Levantamento feito em 2026-08-12, ao vivo contra as APIs/portais de cada fonte (não
apenas documentação) — mesmo método do
[`analytics/labor_market/fontes_dados.md`](../labor_market/fontes_dados.md). Objetivo:
mapear, por dado fiscal, quem é a fonte primária, quem redistribui, e o que já está no
banco (`fisc_*`, ver [`domain/db/CLAUDE.md`](../../domain/db/CLAUDE.md)) vs. o que existe
mas ainda não foi puxado — contexto adicional (gotchas, pendências já documentadas) em
[`analytics/fiscal_policy/CLAUDE.md`](CLAUDE.md).

**Segunda correção (mesmo dia, terceira passada)**: a segunda versão desta tabela (que já
tinha corrigido a primeira usando a API de Séries Temporais do Tesouro) ainda comparava o
Tesouro contra um mapeamento incompleto do lado do BCB — só as duas planilhas
(`Dlspp.xlsx`, `Dbggindexp.xlsx`) já conhecidas de uma investigação anterior
(`reference/fiscal_impulse_metrics.md`). A pedido do usuário, esta passada mapeou
sistematicamente `bcb.gov.br/estatisticas/tabelasespeciais` (também uma SPA Angular sem
conteúdo renderizado no servidor — confirmado tentando fetch direto, JS bundle e Wayback
Machine desde 2019, todos vazios) e **confirmou ao vivo, baixando e inspecionando cada
arquivo com `openpyxl`** (não só nome/URL) que existem 6 planilhas fiscais nesse catálogo,
todas em `https://www.bcb.gov.br/content/estatisticas/Documents/Tabelas_especiais/`, sem
API, sem autenticação — ver tabela consolidada abaixo, que substitui as duas tabelas
anteriores desta seção (cobertura + mapa de Temas do Tesouro), cruzando as duas fontes
lado a lado.

## Tabela consolidada — BCB (Tabelas Especiais) × Tesouro (Séries Temporais) × outras fontes

Cobre todo dado fiscal identificado neste projeto, de onde vem, como se conecta, e —
onde as duas fontes se sobrepõem — qual tem mais detalhe. "Formato de conexão" distingue
3 tipos usados neste projeto: **API SGS/REST** (BCB, JSON, parâmetro de série), **API
Séries Temporais** (Tesouro, JSON, `connectors/tesouro_series_temporais.py`, não
documentada no CKAN) e **xlsx estático** (download direto de URL fixa, sem parâmetros —
BCB Tabelas Especiais e Tesouro RTN/EFGG legado).

| Dado | Fonte | Formato de conexão | Na base/ETL | Comentário |
|---|---|---|---|---|
| Dívida bruta/líquida agregada, % PIB, por nível de governo (DBGG/DLSP) | **BCB** (SGS) | API SGS | ✅ `fisc_divida` | Conceito "de cima" — sem equivalente Tesouro (DPF do Tesouro é só os títulos que ele emite, um subconjunto; DBGG/DLSP são conceitos mais amplos do BCB, incluem dívida contratual, intra-governo etc.). |
| Resultado fiscal agregado — NFSP (primário/nominal/juros), % PIB, por nível de governo | **BCB** (SGS) | API SGS | ✅ `fisc_nfsp` | Idem — agregado publicado, sem equivalente Tesouro. |
| **NFSP detalhado** — mesma base do item acima, mas por Governo Federal / Bacen / INSS / Empresas Estatais Federais / Estaduais / Municipais separadamente (não agregado) | **BCB**, planilha `Nfspp.xlsx` | xlsx estático | ❌ | **Mais granular que `fisc_nfsp`** — confirmado abrindo o arquivo: `fisc_nfsp` hoje só tem 4 cortes (consolidado/federal+BC/estados-municípios/estatais); esta planilha separa INSS do Governo Federal e Empresas Estatais por esfera (federais/estaduais/municipais), 10 abas (mensal/anual/12m × R$/% × corrente/constante). Nenhum equivalente no Tesouro. |
| Composição da DBGG por indexador (prefixado/câmbio/índices de preços), + Primário e Juros por indexador | **BCB**, planilha `Dbggindexp.xlsx` | xlsx estático | ❌ | Escopo = Governo Geral (Federal+Estados+Municípios). 4 abas: `Divida%`/`DividaR$`/`PrimarioR$`/`JurosR$` — as duas últimas (resultado primário e juros **por indexador**) não têm equivalente no Tesouro. **Parcialmente redundante** com a linha abaixo para a parte de estoque por indexador. |
| Composição da DPF por indexador/título (prefixado/Selic/IPCA/câmbio/taxa flutuante; por título LFT/LTN/NTN-B/C/D/F/TDA) | **Tesouro**, Tema 18 "Dívida Pública Federal", subtema Estoque (`18.02.01`) | API Séries Temporais | ❌ | Escopo = só DPF (títulos do Tesouro, um pouco mais estreito que Governo Geral). **Redundante em conceito** com `Dbggindexp.xlsx` acima para "por indexador", mas via API pronta (JSON, sem parsear xlsx) — caminho operacionalmente preferível mesmo cobrindo uma fatia um pouco menor. |
| Composição da dívida por detentor (bancos, fundos, previdência, não residentes, governo, seguradoras) | **Tesouro**, Tema 18, mesmo subtema (`18.02.02 Detentores`) | API Séries Temporais | ❌ | **Só existe no Tesouro** — inspecionado `Dbggindexp.xlsx` a fundo, não tem corte por detentor, só por indexador. Sem redundância. |
| Fatores condicionantes da evolução da DBGG/DLSP (resultado primário, juros, ajustes patrimoniais/metodológicos, privatização, impacto das operações compromissadas do BC) | **BCB**, planilha `Evldp.xlsx` | xlsx estático | ❌ | **Só existe no BCB** — ~20 abas (Tabela 1 a 11, com subdivisões A/B), decompõe o que explica a variação do estoque de dívida período a período. Sem equivalente no Tesouro. É a peça que faltava para reconciliar "por que a dívida mudou" além do estoque puro — relevante para `reference/fiscal_impulse_metrics.md`. |
| Taxa de juros implícita da DLSP e DBGG (mensal e acum. 12m) | **BCB**, planilha `Tximplnp.xlsx` | xlsx estático | ❌ | **Só existe no BCB** — custo efetivo médio do estoque de dívida (DLSP e DBGG separadamente). Parcialmente relacionado ao "Custo Médio" do Tesouro (Tema 18, subtema 4) mas conceitos diferentes: esse é sobre DPF (só títulos), este é sobre DLSP/DBGG (conceito mais amplo do BCB) — não é a mesma série, não conferido se convergem numericamente. |
| Dívida líquida/bruta do governo geral, metodologia pré-2008 (histórica) | **BCB**, planilha `Divggp.xlsx` | xlsx estático | ❌ | Só ponte histórica — `fisc_divida`'s DBGG já começa em 2006-12 na metodologia atual (ver Gotchas em `CLAUDE.md`); esta planilha cobre a metodologia anterior, útil só se algum dia se quiser estender a série para trás com descontinuidade assinalada. Baixa prioridade. |
| Relacionamento Tesouro Nacional × Banco Central (emissão/resgate de títulos, remuneração de disponibilidades, resultado do relacionamento) | **Tesouro**, Tema 14 | API Séries Temporais | ❌ | **Só existe no Tesouro** nesse recorte exato (fluxo mensal Tesouro↔BC) — relacionado, mas não idêntico, ao "impacto das operações compromissadas do BC" dentro de `Evldp.xlsx` acima (esse é fator condicionante do estoque de dívida; o do Tesouro é receita/despesa de caixa do relacionamento). Candidato a simplificar `reference/fiscal_impulse_metrics.md`'s Metric 3, que hoje depende de baixar `Dlspp.xlsx` manualmente. |
| Receita/despesa do Governo Central por rubrica orçamentária (RTN, mensal, caixa) | **Tesouro**, Tema 10 | API Séries Temporais | ✅ `fisc_rtn` | Sem equivalente no BCB. |
| RTN detalhado por Poder e Órgão (Legislativo/Judiciário/Executivo/MPU/DPU) | **Tesouro**, Tema 12 | API Séries Temporais | ❌ | Corte que `fisc_rtn` não tem — sem equivalente BCB. |
| Comparativo RTN × RREO (reconciliação de metodologias) | **Tesouro**, Tema 19 | API Séries Temporais | ❌ | Sem equivalente BCB. |
| Despesa por natureza econômica GFSM 2014, todos os entes (EFGG) | **Tesouro**, Tema 15 (ou conector `tesouro_efgg.py`, sheets `1.3`/`2.3`) | API Séries Temporais **ou** xlsx estático (dois caminhos) | ✅ `fisc_efgg` (via xlsx) | Sem equivalente BCB. |
| Receita por natureza econômica GFSM 2014, todos os entes (EFGG) | **Tesouro**, Tema 15 (ou `tesouro_efgg.py`, sheets `1.2`/`2.2`) | API Séries Temporais **ou** xlsx estático (dois caminhos) | ✅ `fisc_efgg` (via xlsx, 2026-08) | Ingerida via o caminho xlsx (mesmo connector da despesa) — 11 códigos por esfera, ver "Impulso de receitas" em `CLAUDE.md`. Sem equivalente BCB. |
| Investimento do Governo Federal (por GND/Função e por Natureza da Despesa) | **Tesouro**, Tema 13 | API Séries Temporais | ❌ | Sem equivalente BCB. |
| Responsabilidade Fiscal/LRF (pessoal, dívida consolidada líquida, garantias, operações de crédito, receita corrente líquida) | **Tesouro**, Tema 17 | API Séries Temporais | ❌ | Sem equivalente BCB — indicadores de limite legal, não de estoque/fluxo puro. |
| Restos a Pagar (Processados/Não Processados × 6 categorias de despesa) | **Tesouro**, Tema 16 (subtema `16.3`) | API Séries Temporais | ❌ | Sem equivalente BCB. Corrige um bloqueio herdado de uma investigação anterior sobre o MEFA (Portal da Transparência/CKAN não tinham isso) — a API de Séries Temporais tem, com granularidade menor (anual, por categoria, não por órgão). |
| Custeio Administrativo do Governo Central (por Grupo/Item e por Função) | **Tesouro**, Tema 20 | API Séries Temporais | ❌ | Sem equivalente BCB. |
| Gastos tributários / renúncias fiscais | **RFB** | Só PDF/portal (Demonstrativo de Gastos Tributários) | ❌ | Fonte mais direta para "impulso de receitas" (mede renúncia por corte de imposto/subsídio diretamente) — ver Pending em `CLAUDE.md`. Nem BCB nem Tesouro têm isso. |
| Execução orçamentária federal granular (por ação/programa/órgão) | **SIOP/MGI** | Webservice SOAP credenciado (ou arquivos estáticos RDF/CSV) | ❌ | Tema 16 do Tesouro (Despesa/Receita Orçamentária, não checado a fundo) pode cobrir parte disso sem precisar de credencial — não confirmado. |
| Precatórios (estoque e pagamento, por tipo/órgão) | **Tesouro** (painel "Riscos Fiscais com Demandas Judiciais e Precatórios", Tesouro Transparente — não confirmado se está também na API de Séries Temporais) | Painel/portal (não API confirmada) | ❌ | Fonte SIAFI, mensal, desde 2015. Nenhum dos 11 Temas da API tem "precatório" no nome — pode estar embutido em alguma folha do Tema 12/16, não checado. |
| Dados subnacionais — estados/municípios (RREO/RGF) | **Tesouro/STN (SICONFI)** | API REST (`apidatalake.tesouro.gov.br`) | ❌ | Fora de escopo por decisão explícita do usuário (ver Gotchas em `CLAUDE.md`) — não é falta de fonte. |

## Mapa de referência — Temas do Tesouro (Séries Temporais)

`fisc_rtn` usa só o Tema 10, de 11 temas totais (`get_temas()` confirmado ao vivo). Mapa
completo dos subtemas por trás de cada linha da tabela acima:

| Tema | Nome | Subtemas |
|---|---|---|
| 10 | Resultado Fiscal do Governo Central — Valores Mensais | 9 (Receitas, Transferências, Despesas, Result. Primário, Ajustes, Discrepância, Result. Abaixo da Linha, Juros, Result. Nominal) |
| 11 | Resultado Fiscal do Governo Central — Valores Acumulados no Ano | não explorado — provável redundância com o Tema 10 (mesma coisa, acumulado no ano), não conferido |
| 12 | Transferências e Despesas Primárias — Critério "Valor Pago" | Detalhamento RTN; Detalhamento por Poder e Órgão |
| 13 | Investimento do Governo Federal | Por GND e Função; Por Natureza da Despesa |
| 14 | Relacionamento Tesouro Nacional x Banco Central | 1 subtema, 9 séries mensais |
| 15 | Estatísticas de Finanças Públicas — Padrões Internacionais | 5 esferas (Central Orçamentário/Consolidado, Estadual, Municipal, Geral), trimestral, GFSM |
| 16 | Execução Orçamentária — União | Despesa Orçamentária; Receita Orçamentária; Restos a Pagar |
| 17 | Responsabilidade Fiscal — União | Despesa com Pessoal; Dívida Consolidada Líquida; Garantias e Contra-Garantias; Operações de Crédito; Receita Corrente Líquida |
| 18 | Dívida Pública Federal | Operações Mercado Primário (112 séries); Estoque (60 — indexador/detentor/título); Vencimentos (135); Custo Médio (59); Tesouro Direto (47); Mercado Secundário (6) |
| 19 | Comparativo RTN x RREO | não explorado |
| 20 | Custeio Administrativo do Governo Central — Mensal | Por Grupo e Item; Por Função Orçamentária |

Cada série tem `dataInicialSerie`/`dataFinalSerie` (epoch ms) e `fontePrimaria` própria no
retorno de `get_arvore()` — não extraído nesta rodada para todos os temas (só confirmada a
existência/estrutura), então datas de início/fim e possíveis defasagens ainda precisam ser
checadas tema a tema antes de qualquer ingestão. Idem para os subtemas de Vencimentos/Custo
Médio/Tesouro Direto/Mercado Secundário do Tema 18 e para Despesa/Receita Orçamentária do
Tema 16 — confirmada só a existência/estrutura de alto nível, não inspecionados item a item.

## Mapa de referência — Tabelas Especiais do BCB (fiscal)

Página `bcb.gov.br/estatisticas/tabelasespeciais` é uma SPA Angular sem conteúdo
renderizado no servidor (confirmado: fetch direto, JS bundle, Wayback Machine desde 2019 —
todos retornam só o shell vazio). Os arquivos em si, porém, vivem em URL estática e
previsível — `https://www.bcb.gov.br/content/estatisticas/Documents/Tabelas_especiais/
<Nome>.xlsx`, sem autenticação — confirmado baixando e abrindo cada um com `openpyxl`:

| Arquivo | Conteúdo confirmado | Abas |
|---|---|---|
| `Dlspp.xlsx` | DLSP por nível de governo (Federal/BC/Estados/Municípios/Estatais por esfera) + decomposição em ajustes (metodológico interno/externo, patrimonial, privatização) — mesma planilha-base de `reference/fiscal_impulse_metrics.md` | R$ milhões, % PIB |
| `Dbggindexp.xlsx` | DBGG por indexador + Primário e Juros por indexador | Divida%, DividaR$, PrimarioR$, JurosR$ |
| `Nfspp.xlsx` | NFSP detalhado (Nível Federal/Regional → Governo Federal/Bacen/INSS/Empresas Estatais por esfera) | 10 abas (mensal/anual/12m × R$/% × corrente/constante) |
| `Divggp.xlsx` | DBGG/DLSP, metodologia pré-2008 (legado) | R$ milhões, % PIB |
| `Evldp.xlsx` | Fatores condicionantes da evolução da dívida (~20 tabelas) | Tabela 1-11 + subdivisões A/B |
| `Tximplnp.xlsx` | Taxa de juros implícita da DLSP e DBGG | DLSP/DBGG × mensal/12m |

Confirmado como inexistentes no mesmo diretório (tentativa direta, HTTP 404): `Dlsp.xlsx`,
`Dbgg.xlsx`, `Nfsp.xlsx`, `Divliq.xlsx`, `Tximpl.xlsx`, `Cronograma.xlsx`, `Dpmfi.xlsx`,
`Detentores.xlsx` — os nomes reais usam o sufixo "p" (Dlsp**p**, Dbggindex**p**, Nfsp**p**,
Divgg**p**) que não é óbvio a priori. Categorias do próprio Manual de Estatísticas Fiscais
do BCB (maio/2019) para cronograma de vencimentos e outras tabelas não-fiscais (ex.
Balanço de Pagamentos: `BalPagA.xlsx`, `BalPagT.xlsx`, `BalPagM.xlsx`) existem no mesmo
diretório mas fora do escopo fiscal desta tabela.

## Leitura geral

- **BCB e Tesouro raramente publicam exatamente o mesmo dado — quando parecem
  redundantes, o BCB tende a ter escopo mais amplo (Governo Geral/setor público) e o
  Tesouro tende a ter o caminho de acesso mais simples (API JSON pronta vs. xlsx
  estático).** O único par genuinamente sobreposto é "dívida por indexador":
  `Dbggindexp.xlsx` (BCB, Governo Geral) vs. Tema 18 do Tesouro (só DPF, um subconjunto)
  — mas o caminho do Tesouro é uma API, o do BCB é xlsx manual. Fora esse par, cada fonte
  tem material que a outra não tem — ver a tabela consolidada acima para o detalhe linha
  a linha.
- **O que só o BCB tem**: fatores condicionantes da evolução da dívida (`Evldp.xlsx` —
  reconcilia por que o estoque mudou período a período: primário, juros, ajustes,
  privatização, operações compromissadas do BC), taxa de juros implícita da DLSP/DBGG
  (`Tximplnp.xlsx`), e um NFSP muito mais granular (`Nfspp.xlsx` — separa INSS do Governo
  Federal e quebra Empresas Estatais por esfera, algo que a série SGS já usada em
  `fisc_nfsp` não tem). Nenhum desses tem qualquer equivalente nos 11 Temas do Tesouro.
- **O que só o Tesouro tem**: RTN (já usado), EFGG despesa (já usado) e receita (não
  ingerida), relacionamento Tesouro×BC (Tema 14 — candidato a simplificar o cálculo
  manual de `reference/fiscal_impulse_metrics.md`), restos a pagar, investimento federal,
  responsabilidade fiscal/LRF, custeio administrativo, RTN por Poder/Órgão, comparativo
  RTN×RREO, e — só no caso da dívida — o corte por **detentor** (bancos/fundos/
  previdência/não-residentes), que não existe em nenhuma planilha do BCB inspecionada.
- **Nenhuma das duas fontes tem API "de verdade" descoberta por busca convencional** —
  ambas exigiram engenharia reversa (Tesouro: rastrear chamadas de rede da SPA; BCB:
  confirmar o padrão de URL estática por tentativa direta, já que a página também é uma
  SPA sem conteúdo server-rendered, inclusive em snapshots do Wayback Machine desde
  2019). Qualquer levantamento futuro de dados do Tesouro ou do BCB deveria testar esses
  dois caminhos primeiro, antes de qualquer busca web/CKAN.
- **RFB e SIOP continuam sem caminho aberto confirmado** — gastos tributários (RFB) só em
  PDF; SIOP só tem webservice credenciado como caminho "oficial", mas o Tema 16 do
  Tesouro (Despesa/Receita Orçamentária, não checado a fundo) pode cobrir parte disso sem
  precisar de credencial.
- **IPEA e Precatórios** ficam como nesta rodada: IPEA não trouxe cobertura nova
  confirmada (evidência só circunstancial de que redistribui séries do BCB, e agora
  irrelevante frente ao que BCB/Tesouro já cobrem diretamente); Precatórios segue como
  painel do Tesouro Transparente (mensal, SIAFI, desde 2015), sem confirmação de estar
  também na API de Séries Temporais.
