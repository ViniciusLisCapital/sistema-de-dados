# Panorama de Inflação — Estrutura de Dados e Pendências

Relatório HTML: `reports/inflation_latest.html` (gerado por `analytics/inflation/generate_report.py`)
Migrado para MySQL em 2026-07: decomposição por subitem agora vive em `macro_brasil`.
`inflacao` renomeada para `ipca_agregados` (mesma data), séries padronizadas para minúsculo;
depois renomeada de novo para `inflation_agregados` (prefixo de tema — ver `DB_SCHEMAS.md`),
e mais uma vez para `inflc_agregados` (prefixo abreviado, 2026-07-09).
`ipca_decomposicao`/`ipca_dimensao` seguiram a mesma cadeia até `inflc_decomposicao`/`inflc_dim`.

---

## Mapa de dados atual

### MySQL — `macro_brasil`

| Tabela | Papel | Script | Atualização |
|---|---|---|---|
| `inflc_decomposicao` | IPCA/IPCA-15 por subitem: var_mensal, pesos, contribuicao (57.288 linhas, 2020 → hoje) | `domain/db/brasil/ibge/inflc_decomposicao.py` | `jobs/update_db.py` (rotina) |
| `inflc_dim` | Subitem → Grupo/Subgrupo/Item/Subjacente + 7 flags oficiais de núcleo (377 linhas, sem dimensão de tempo) | `domain/db/brasil/ibge/inflc_dim.py` | `jobs/update_db.py` (idempotente — reflete os xlsx a cada run) |
| `inflc_agregados` | Agregados BCB/SGS (headline, componentes, núcleos), 33 séries — renomeada de `inflacao`, depois de `ipca_agregados` | `domain/db/brasil/bcb/inflc_agregados.py` | `jobs/update_db.py` |

`inflc_decomposicao` busca direto da API do IBGE (agregados 7060 IPCA / 7062 IPCA-15,
classificação 315 "Geral, grupo, subgrupo, item e subitem", nível 4 = subitem/folha).
IDs de subitem são resolvidos dinamicamente via `listar_classificacoes()` — não há lista
hardcoded, então altas/baixas de subitens no IBGE são acompanhadas automaticamente.
**Não armazena variação 12 meses** — removida em 2026-07 por decisão de calcular
acumulados/YoY a partir de `var_mensal` na camada de consumo em vez de manter uma
segunda fonte de verdade no banco (a API do IBGE oferece essa variável direto, mas
teria que ser combinada com a mesma pegadinha de IDs abaixo).

**Pegadinha resolvida:** IPCA e IPCA-15 usam **IDs de variável diferentes** dentro do
mesmo esquema de classificação — 7060 usa 63 (var_mensal) / 66 (pesos); 7062 usa
355 / 357. Pedir o ID errado para o agregado errado não dá 404 — a API do IBGE
responde HTTP 500 (bug deles), o que inicialmente pareceu um problema de payload
grande demais em vez de um ID de variável inválido.

`inflc_dim` **não tem fonte via API** — combina duas fontes de naturezas distintas:
- `grupo`/`subgrupo`/`item`/`subjacente`: classificação própria (BCB/LIS), mantida
  manualmente em `analytics/inflation/data/tabela_dimensao_ipca.xlsx`
  (sheet `dimensao_bcb_2020`) — não faz parte da árvore do IBGE. Editar o xlsx e
  rodar `inflc_dim.run()` para propagar mudanças.
- `nucleo_ex0`/`nucleo_ex01`/`nucleo_ex02`/`nucleo_ex03`/`nucleo_ex03_servicos`/
  `nucleo_ex03_industriais`/`nucleo_exfe` (2026-07, adicionadas nesta rodada):
  derivadas de `analytics/inflation/data/Vetores_NT_57.xlsx` (sheet
  `jan20-presente`), arquivo de apoio **oficial** da Nota Técnica do Banco Central
  do Brasil nº 57 (dez/2025) — não uma aproximação nossa. Cada subitem recebe 1
  se ele próprio ou algum ancestral (item/subgrupo/grupo/índice geral) tiver o
  flag ligado no vetor de agregação oficial daquele núcleo (`_rollup_nucleo_flags()`
  em `inflc_dim.py` implementa essa propagação). Cross-checado contra o texto da
  NT-57 (lista literal de exclusões do EX-01) com 100% de acerto nos 377 subitens.

**Achado ao cruzar as duas fontes (e resolvido, 2026-07):** `subjacente`
(manual) divergia de `nucleo_ex03_servicos`/`nucleo_ex03_industriais`
(oficial) em ~19 dos 377 subitens — a maioria bens industriais que
`tabela_dimensao_ipca.xlsx` nunca marcou como "Bens Industriais Subjacente"
(madeira e taco, sabão líquido, papel toalha, bermuda/short, mochila, óculos
de grau, livros didáticos, entre outros), mais 1 caso inverso ("Conselho de
classe", marcado como "Serviços Subjacente" na planilha manual mas fora do
EX-03 Serviços no vetor oficial). Por instrução explícita do usuário ("You
should follow the official dimension"), `inflc_dim.py` agora **deriva**
`subjacente` = Serviços/Bens Industriais Subjacente diretamente de
`nucleo_ex03_servicos`/`nucleo_ex03_industriais` (`_apply_official_subjacente()`),
não mais do xlsx manual — as duas fontes são idênticas por construção agora.
"Alimentos Subjacente" continua vindo do xlsx manual sem alteração: a NT-57
não publica uma coluna equivalente para o núcleo de alimentação do EX2 (só
Serviços/Industriais têm série oficial própria, EX3 Serviços/Industriais),
então não há fonte oficial para reconciliar essa parte. Confirmado sem
sobreposição entre os 34 subitens "Alimentos Subjacente" e os flags oficiais
de serviços/industriais antes de aplicar a regra.

`inflc_agregados` (33 séries, ex-`inflacao`, ex-`ipca_agregados`; +2 nesta
rodada — `ipca_comercializaveis`/SGS4447 e `ipca_nao_comercializaveis`/SGS4448)
tem documentação nativa no MySQL: `COMMENT` na tabela (visão geral) e na
coluna `name` (lista as 33 séries com seus códigos SGS, ex.:
`ipca_nucleo_p55=SGS28750`) — visível via `SHOW CREATE TABLE inflc_agregados`
ou no editor de tabelas do Workbench, sem precisar ler o código Python.
Consumidores que ainda referenciam o nome/série antigo
(`analytics/oraculo/brasil/scores.py`) foram atualizados; ele re-mapeia
`ipca` → `IPCA` internamente logo após o load para não precisar tocar no resto do
arquivo.

### `analytics/inflation/data/` vs. `analytics/inflation/referencia/` (2026-07)

Convenção adotada nesta rodada (a mesma vale para os outros relatórios em
`analytics/`, ex. `cambio/`, `oraculo/`): `data/` é só para arquivos que
algum script efetivamente lê ou escreve; material de contexto/proveniência
que nenhum script toca vai para `referencia/`.

**`analytics/inflation/data/` (operacional):**

| Arquivo | Situação |
|---|---|
| `tabela_dimensao_ipca.xlsx` | **Em uso** — fonte de `grupo`/`subgrupo`/`item` + "Alimentos Subjacente" (sem equivalente oficial); lido por `inflc_dim.py` |
| `Vetores_NT_57.xlsx` | **Em uso** — fonte oficial de `subjacente` (Serviços/Industriais) + todos os `nucleo_*`; lido por `inflc_dim.py` |
| `ipca_bcb_series.csv` | **Em uso** — agregados BCB/SGS + STL `_ma3_sa`, gerado por `fetch_bcb.py`, lido por `generate_report.py` |

**`analytics/inflation/referencia/` (contexto/proveniência, nenhum script lê):**

| Arquivo | Situação |
|---|---|
| `Nucleos_inflacao.pdf` | Nota Técnica BCB nº 57 (dez/2025) — fonte da metodologia consolidada e do glossário de núcleos |
| `Series_NT_57.xlsx` | Arquivo de apoio da NT-57 (comparação séries novas/anteriores) — não lido por código |
| `inflacao_servico.pdf` | Boxe RI jun/2024, "Inflação de serviços reponderada por fatores de produção" — insumo da pendência de novas métricas de serviços |
| `dim_inflation_ipca15.xlsx` | Formato pré-MySQL, substituído por `inflc_decomposicao` — mantido como registro histórico |

`variacao_peso_contribuicao_ipca.xlsx`/`variacao_peso_contribuicao_ipca15.xlsx`
(mesma categoria de `dim_inflation_ipca15.xlsx` acima) foram apagados em
2026-07 — registro histórico sem valor prático, substituídos por
`inflc_decomposicao` há tempo.

**Pendência registrada para discutir na próxima sessão:** avaliar se algum
desses arquivos de `referencia/` deveria ser carregado no MySQL em vez de
ficar como Excel solto — em especial `Vetores_NT_57.xlsx` (que hoje só tem a
aba `jan20-presente` lida; as demais abas, por período de estrutura do IPCA
desde 1991, ainda não viraram dado de banco — ver pendência de expandir
`inflc_decomposicao`/`inflc_dim` acima) e `Series_NT_57.xlsx` (série
comparativa nova/anterior da própria NT-57 — pode ter valor como
cross-check histórico se carregada). Nada decidido ainda; só um apontador
para a conversa.

### `generate_report.py`

`_load_decomposicao()` lê `inflc_decomposicao` + `inflc_dim` via
`MySQLDataRequester`, faz o join em Python (`merge` por `subitem`) e formata para o
mesmo contrato de dados que o template `report.html` já consumia (`records`,
`records_ipca15`, `min_date`, `max_date`).

`_load_bcb()` (agregados BCB/SGS) não mudou — continua lendo do CSV gerado por
`fetch_bcb.py`, que ainda usa nomes de série em maiúsculo (`IPCA_nucleo_P55`) e é
independente de `macro_brasil.inflc_agregados` — ver pendência abaixo.

### Mudanças no relatório (2026-07, rodada de rebranding + correções)

- **Renomeado** de `analytics/ipca/` → `analytics/inflation/`, saída →
  `reports/inflation_latest.html`, título → "Panorama de Inflação".
- **Aba Snapshot removida** (decisão do usuário) — junto com `groupVarMensal()`,
  `prevMonth()` e todo o código de `renderSnapshot*`/`_snapLayout`. O relatório
  agora tem 2 abas: Decomposição e Núcleos & Difusão.
- **KPI "12 Meses" corrigido**: janela tinha off-by-one (13 meses em vez de 12,
  via `monthsBack`) e ignorava o período selecionado (sempre usava
  `currentMaxDate()` em vez de `endDate`). Agora usa 3 níveis de precisão —
  série oficial BCB `IPCA_12m`/SGS 13522 (IPCA) → encadeamento da série mensal
  oficial do BCB (`computeYoY`, cobre IPCA-15 também) → reconstrução a partir do
  subitem (`computeIpca`, só como último recurso). "IPCA Acumulado" reusa o
  mesmo valor quando o período selecionado é exatamente os últimos 12 meses,
  para as duas métricas nunca discordarem sobre a mesma janela.
- **3M SAAR**: ordem STL↔MA(3) corrigida (`fetch_bcb.py:_apply_stl_ma3`) — STL
  agora roda na série mensal bruta, MA(3) depois, alinhado à convenção
  BLS/X-13. Ver seção "3M SAAR" mais abaixo.
- **Difusão**: chart antigo "Índice de Difusão IPCA" removido; substituído por
  "Difusão por Categoria" (drilldown Grupo/Subgrupo/Item, MM3/MM6).
- **Glossário de núcleos**: painel colapsável na aba Núcleos & Difusão com
  definição de cada núcleo (EX-0/EX-01/EX-02/EX-03/EX-FE/P55/Médias
  Aparadas/Dupla Ponderação).
- **"Núcleo Selecionado"**: dropdown com os 11 núcleos disponíveis, mostra 3M
  SAAR + 12M a/a do núcleo escolhido num único gráfico.
- **"Núcleos — 3M SAAR" e "Núcleos de Inflação — Variação 12M"**: ambos os
  gráficos ganharam um dropdown de checkboxes (`NUCLEO_ALL`, 13 opções — IPCA
  + os 11 núcleos + a média sintética abaixo) para escolher livremente quais
  linhas exibir, em vez do conjunto fixo anterior. Adicionada também a série
  sintética **"Média 5 Núcleos (BCB)"** — média simples de EX-0, EX-03,
  Médias Aparadas (com suavização), Dupla Ponderação e P55, o conjunto que o
  próprio BC costuma resumir em uma média única (NÃO inclui EX-01/EX-02/EX-FE
  — ver `NUCLEO5_BCB` em `report.html` e o Estudo Especial 102 do BC).
- **Fonte oficial adotada: Nota Técnica do Banco Central do Brasil nº 57**
  (dez/2025, "Núcleos de inflação e outras séries analíticas derivadas do
  IPCA: metodologia consolidada"; PDF + 2 xlsx de apoio em
  `analytics/inflation/data/Nucleos_inflacao.pdf`/`Vetores_NT_57.xlsx`/
  `Series_NT_57.xlsx`). Confirma os códigos SGS já em uso
  (`inflc_agregados.py`/`fetch_bcb.py`), inclusive as 3 séries adicionadas
  nesta rodada (11426=MA, 29683=EX-03 Serviços, 29684=EX-03 Industriais —
  validação independente do fix de citação de série feito anteriormente).
  Também confirmou que nosso "medias_aparadas" (série 4466) = MS **com**
  suavização e "medias_aparadas_sem_suavizacao" (série 11426) = MA **sem**
  suavização — nomenclatura já estava correta. Glossário de núcleos
  reescrito com as definições textuais exatas da nota (EX-0/EX-01/EX-02/
  EX-03/EX-FE/DP detalhados; MA e MS agora com entradas separadas, antes
  confladas em uma única "Médias Aparadas").
- **Difusão por Categoria — nível "Núcleo"** (`NUCLEO_DIFUSAO_CATS` em
  `report.html`, 7 categorias: EX-0/EX-01/EX-02/EX-03/EX-03 Serviços/EX-03
  Industriais/EX-FE), agora usando os flags oficiais `nucleo_*` de
  `inflc_dim` (ver acima) em vez de uma aproximação por `grupo`/`subgrupo`
  ou do campo `subjacente`. `Vetores_NT_57.xlsx` — arquivo de apoio da NT-57
  que o usuário adicionou numa rodada seguinte — trouxe o vetor de
  agregação oficial (0/1 por componente do IPCA, todos os níveis
  hierárquicos) de cada núcleo por exclusão, o que tornou EX-01 e EX-FE
  finalmente viáveis para difusão (antes descartados por falta de dados
  granulares o suficiente). Cross-checado com 100% de acerto contra a
  lista literal de exclusões do EX-01 na NT-57. Ainda não cobre P55/Médias
  Aparadas/DP — exclusões estatísticas, sem conjunto fixo de itens.
- **`subjacente` agora segue a dimensão oficial** (2026-07, mesmo dia,
  rodada seguinte): por instrução explícita do usuário, `inflc_dim.py`
  passou a derivar Serviços/Bens Industriais Subjacente a partir de
  `nucleo_ex03_servicos`/`nucleo_ex03_industriais` em vez do xlsx manual —
  ver acima e a pendência de reconciliação, agora resolvida para essas duas
  categorias (Alimentos Subjacente permanece manual, sem equivalente oficial).
- **Comercializáveis / Não Comercializáveis** (SGS 4447/4448, confirmadas na
  Tabela 11 da NT-57): adicionadas a `fetch_bcb.py`/`inflc_agregados.py`
  (31→33 séries) e aos dois gráficos "Componentes" (3M SAAR e Variação 12M).
- **Glossário — bug de overflow corrigido**: rótulos longos ("Médias
  Aparadas (sem suavização) — MA") ficavam com `white-space: nowrap` numa
  coluna fixa de 130px, transbordando visualmente por cima do texto da
  definição ao lado. Corrigido permitindo quebra de linha e alargando a
  coluna para 190px.
- **Nova aba "Mapa de Calor"**: heatmap de 3M SAAR (Grupos: IPCA/Livres/
  Monitorados/Alimentação/Serviços/Industriais/Comercializáveis/Não
  Comercializáveis; Núcleos: os 11 núcleos + Média 5 Núcleos), últimos 12
  meses. Metodologia (pesquisada e confirmada com o usuário antes de
  implementar): z-score de cada série contra sua **própria** média/desvio-
  padrão móvel de 60 meses (5 anos) — mesma abordagem do heatmap de
  inflação do FRED Blog (St. Louis Fed, "Is inflation running hot or
  cold?"). Normalizar por série (não por um limiar comum) torna núcleos com
  volatilidade muito diferente comparáveis na mesma escala de cor
  azul(frio)→branco→vermelho(quente). Não achamos um equivalente publicado
  pelo BCB para replicar — o FRED é a referência mais sólida encontrada.
- **`data/` vs. `referencia/`**: separação adotada para organizar material
  técnico — `data/` só para arquivos que algum script lê/escreve,
  `referencia/` para PDFs/notas de proveniência que ninguém no código toca.
  Movidos para `analytics/inflation/referencia/`: `Nucleos_inflacao.pdf`,
  `Series_NT_57.xlsx`, `dim_inflation_ipca15.xlsx`,
  `variacao_peso_contribuicao_ipca(15).xlsx`, e `inflacao_servico.pdf`
  (que estava solto na raiz do projeto). Ver seção de dados acima.
  `variacao_peso_contribuicao_ipca(15).xlsx` foram apagados em seguida —
  registro histórico sem valor prático.
- **Bug corrigido: "Evolução Mensal" mostrando contribuição positiva como
  negativa** (`renderTimeSeries()`): usava `barmode:'stack'`, que empilha as
  barras estritamente na ordem dos traces, independente do sinal — se uma
  categoria (ex.: Bens Industriais) tem contribuição negativa num mês, a
  próxima categoria empilhada (ex.: Serviços) nasce daquela base negativa e
  pode aparecer abaixo de zero mesmo com valor próprio positivo (bug
  reportado pelo usuário via screenshot). Corrigido para `barmode:'relative'`
  — empilha positivos a partir de zero para cima e negativos a partir de
  zero para baixo, independentemente uns dos outros; já era o padrão correto
  usado no gráfico equivalente do IPCA-15 (`renderCompContrib15()`).

---

## Pendências

### Alta prioridade
- **Mapa de Calor de variação mensal por Grupo/Subgrupo/Item/Subitem**
  (pedido do usuário, não iniciado): hoje a aba "Mapa de Calor" só cobre um
  conjunto fixo de linhas (Grupos BCB + Núcleos, 3M SAAR). Falta uma segunda
  visão — ou um modo alternativo na mesma aba — mostrando **variação mensal
  (var_mensal)**, não SAAR, com o **nível selecionável** (Grupo/Subgrupo/
  Item/Subitem, os mesmos 4 níveis de `LEVELS`/`currentLevel()` usados no
  drilldown da Decomposição) e todas as categorias daquele nível como linhas
  do heatmap — ao contrário da "Difusão por Categoria", que já tem Nível +
  Categoria (uma categoria de cada vez); aqui a ideia é ver **todas** as
  categorias do nível escolhido lado a lado. Pontos em aberto para a próxima
  sessão: (1) reaproveitar `rollingZScore`/`zColor` (mesma regra já
  confirmada com o usuário) ou usar outra régua já que var_mensal de
  subitem é mais ruidoso que 3M SAAR de núcleo; (2) nível Subitem pode
  gerar 300+ linhas — precisa de paginação, scroll, ou um teto com "ver
  todos" (mesmo padrão do ranking da aba Decomposição); (3) fonte de dados
  são os `records`/`records_ipca15` já carregados (mesmo pipeline da
  Difusão por Categoria), não os agregados BCB — funciona igual para
  IPCA/IPCA-15 sem branching.
- **Núcleos não existem para o IPCA-15 — precisam ser reconstruídos por
  agregação própria**: todo o trabalho de núcleos desta rodada (glossário,
  dropdowns, "Média 5 Núcleos", Mapa de Calor, difusão por núcleo) usa séries
  BCB/SGS que **só existem para o IPCA cheio**. O BCB não publica núcleos
  para o IPCA-15 — `inflc_agregados`/`fetch_bcb.py` só têm o headline IPCA-15
  (série 7478); não há EX-0/EX-01/.../P55/MA/MS/DP equivalentes. Por isso
  `renderNucleosTab()` já esconde essas seções para IPCA-15 hoje (mostra só
  "Decomposição Mensal por Componente" no lugar). Para ter núcleos de
  IPCA-15, teríamos que **calcular nós mesmos**, via agregação simples (o
  mesmo método da NT-57, Subseção 2.1.2: variação ponderada dos componentes
  que pertencem ao núcleo) em cima de `inflc_decomposicao` (que já tem os
  dados de var_mensal/pesos por subitem do IPCA-15) e `inflc_dim` (cujos
  flags `nucleo_ex0/ex01/ex02/ex03/ex03_servicos/ex03_industriais/exfe` já
  são compartilhados entre IPCA e IPCA-15 — "todo subitem do IPCA-15 também
  existe no IPCA", ver docstring de `inflc_dim.py`). Viável para os núcleos
  por exclusão (EX-0/EX-01/EX-02/EX-03/EX-FE) com renormalização de peso
  dentro da cesta do IPCA-15; MA/MS/DP/P55 exigiriam replicar toda a
  metodologia estatística (aparação, dupla ponderação, percentil) sobre os
  subitens do IPCA-15 — bem mais trabalho. Não iniciado.
- **Expandir `inflc_decomposicao`/`inflc_dim` para períodos anteriores a 2020**:
  hoje a decomposição por subitem só cobre a estrutura vigente (jan/20-presente,
  POF 2017-2018). `Vetores_NT_57.xlsx` (`analytics/inflation/data/`) na
  verdade tem uma aba por período de estrutura do IPCA desde jan/91
  (`jan91-jul99`, `ago99-dez05`, `jan06-jun06`, `jul06-dez11`, `jan12-dez19`,
  além de `jan20-presente`, já em uso) — ou seja, agora temos a classificação/
  vetor de agregação oficial necessária para estender a decomposição e os
  flags de núcleo históricamente, se algum dia for necessário (ex.: séries de
  contribuição por subitem mais longas que 2020). Não faz parte do escopo
  atual do `inflc_decomposicao.py` (que busca direto da API do IBGE, que só
  cobre a estrutura vigente) — exigiria decidir se vale a pena reconstruir
  histórico via IBGE (dados existem, mas a API atual não expõe estruturas
  antigas do mesmo jeito) ou aceitar que só o vetor oficial (sem os dados de
  variação/peso do IBGE em si) está disponível para os períodos anteriores.
- **Decomposição por subitem dentro de um núcleo** (não só do IPCA cheio):
  hoje `inflc_decomposicao` calcula contribuição de cada subitem para o IPCA
  geral; falta uma visão equivalente *dentro* da cesta reduzida de um núcleo
  (ex.: quais subitens mais contribuíram para o EX-03 este mês, com pesos
  renormalizados dentro da cesta do núcleo, não do IPCA cheio). Os flags
  `nucleo_*` em `inflc_dim` (2026-07) já dão a filtragem de membership
  necessária — falta a lógica de renormalização de peso + contribuição
  específica do núcleo.
- **Agregados também a partir da perspectiva do IBGE** (hoje só vêm do BCB):
  `inflc_agregados` inteiro vem de séries BCB/SGS; o usuário quer também
  agregados construídos diretamente a partir da API do IBGE (agregados
  7060/7062, mesmos dados-fonte de `inflc_decomposicao`), permitindo
  decompor esses agregados por subitem do mesmo jeito que já se faz para o
  IPCA cheio — um cross-check independente do BCB e uma decomposição que o
  BCB não publica para seus próprios agregados/núcleos.
- **Novas métricas de inflação de serviços** — `analytics/inflation/referencia/inflacao_servico.pdf`
  (movido da raiz do projeto em 2026-07): boxe do BC (RI jun/2024, "Inflação de serviços reponderada
  por fatores de produção") propõe reponderar subitens de serviços por
  intensidade de uso de trabalho/capital/insumos, estimada a partir das
  Tabelas de Recursos e Usos (TRU) das Contas Nacionais por atividade
  econômica — mais abrangente que a medida de "serviços intensivos em mão de
  obra" de 2013 (que cobre só 6% do IPCA vs. 35% do total de serviços).
  Implementar exigiria: (1) obter os pesos de fator (trabalho/capital/
  insumos) por atividade das TRU/IBGE, (2) mapear atividades → subitens de
  serviços do IPCA, (3) construir as séries reponderadas. Não iniciado.
- ~~Reconciliar `subjacente` (manual) com os flags `nucleo_*` (oficiais)~~ —
  **resolvido em 2026-07** (rodada seguinte): `inflc_dim.py` agora deriva
  Serviços/Bens Industriais Subjacente diretamente de
  `nucleo_ex03_servicos`/`nucleo_ex03_industriais`, por instrução explícita
  do usuário. Ver "Mudanças no relatório" acima.
- **Consolidar agregados BCB/SGS**: `fetch_bcb.py` ainda duplica ~33 das 34 séries já
  em `macro_brasil.inflc_agregados`, com nomes de série em maiúsculo (inconsistente
  com o padrão minúsculo adotado na tabela em 2026-07). Poderia ler de
  `inflc_agregados` e calcular `_ma3_sa`/`ipca_12m` em cima do dado do banco,
  eliminando o CSV e padronizando os nomes — não feito nesta rodada. (Os dois
  scripts vêm sendo mantidos em sincronia manualmente em 2026-07 a cada nova
  série adicionada — `medias_aparadas_sem_suavizacao`/SGS11426,
  `ex03_servicos`/SGS29683, `ex03_industriais`/SGS29684,
  `comercializaveis`/SGS4447, `nao_comercializaveis`/SGS4448 — reforçando por
  que consolidar isso seria valioso.)

### Média prioridade
- **Trocar STL por X-13ARIMA-SEATS no 3M SAAR** (`fetch_bcb.py:_apply_stl_ma3`):
  em 2026-07 a ordem das etapas foi corrigida (STL agora roda na série mensal
  bruta, depois MA(3) — não o inverso — alinhado à convenção BLS/Census de
  dessazonalizar antes de suavizar/anualizar). O motor de decomposição em si
  continua sendo STL (genérico, via `statsmodels`), não o X-13ARIMA-SEATS que
  o BLS/Census efetivamente usa para publicar o CPI oficial. X-13 tem
  tratamento nativo de efeitos de calendário (feriados móveis como Carnaval,
  dias úteis por mês) e estende a série via ARIMA antes de decompor — em vez
  do workaround manual de "congelar fatores do último dezembro completo" que
  usamos hoje para evitar o efeito de borda do STL. `statsmodels.tsa.x13`
  (wrapper `x13_arima_analysis`) já está disponível no venv (statsmodels
  0.14.6) — a mudança de código seria pequena. O bloqueio real é
  operacional: X-13 não é um pacote pip, é um executável separado do Census
  Bureau que precisa ser baixado e instalado manualmente em **cada máquina**
  que rodar `fetch_bcb.py` (`_find_x12()` confirma que não está presente
  nesta máquina hoje) — quebra o modelo de reprodutibilidade via `uv sync`
  que o projeto depende. Decisão do usuário: manter STL por ora, revisitar
  quando a fidelidade ao método oficial do BLS valer o custo operacional.
- **Tamanho do relatório**: `reports/inflation_latest.html` está em ~14 MB — os 57k
  registros de decomposição embutidos como JSON inline são o grosso disso. Se o
  tamanho for um problema para envio por email, considerar paginar por data no
  frontend ou comprimir o payload antes de decidir qualquer mudança de schema.
- **View de contribuição 12m por subitem**: adiada — `var_12m` foi removida de
  `inflc_decomposicao` por decisão do usuário (calcular em outra camada). Se
  necessária no futuro, calcular a partir de `var_mensal` (encadeamento de 12 meses)
  em `generate_report.py` ou num script de analytics, sem reintroduzir a coluna no
  banco.
- **`ipca_bcb_series.csv` fica desatualizado silenciosamente**: `fetch_bcb.py` não
  roda automaticamente (não está em `jobs/update_db.py`, é chamado manualmente) —
  isso já causou dados desatualizados por um mês inteiro sem nenhum erro visível.
  O ideal seria incluir `fetch_bcb.py` no `jobs/update_db.py` ou equivalente para
  eliminar esse gap de vez.
- Confirmar se `variacao_peso_contribuicao_ipca*.xlsx` e `dim_inflation_ipca15.xlsx`
  (não lidos mais) podem ser apagados ou se algum uso externo (Power BI) ainda
  depende deles.

### Baixa prioridade
- Encoding: nenhum problema real encontrado nesta migração — o que parecia mojibake
  em vários pontos (nomes de subitem, docstrings da API IBGE) sempre foi artefato de
  exibição no console do Windows, não corrupção de dado. Os bytes UTF-8 no HTML
  gerado e no banco estão corretos.
