# Sistema de Dados — Contexto para o Claude

## Regras gerais

- **The text should remain in the language it already is, NO TRANSLATION.** When generating `.md` files from English-language PDFs, write in English. When generating from Portuguese-language sources, write in Portuguese.

## Sobre o Projeto

Sistema de dados da LIS Capital para coleta, processamento e visualização de variáveis macroeconômicas (Brasil, EUA). Alimenta dashboards Power BI e materiais de análise macro.

📄 **Racional estratégico e origem do projeto** (por que o vault `obsidian/` e a direção de agentes especialistas por área macro existem, fases de investimento planejadas): [`team_materials/structure_materials/macro-project-context.md`](team_materials/structure_materials/macro-project-context.md).

---

## Arquitetura atual

```
connectors/          — Clientes de APIs/fontes externas: IBGE, BCB (SGS + Focus/Olinda, agenda ICS,
                       tabelas especiais xlsx, anexo estatístico do RPM, comunicados do Copom),
                       FRED, BIS, BLS, BEA (tabelas NIPA da Secao 2, xlsx aberto — sem chave),
                       CFTC, IPEA,
                       Comex Stat/MDIC (API ao vivo + CSV em massa), Tesouro (RTN via CKAN + Séries
                       Temporais + EFGG), PDET/MTE (FTP do Novo CAGED), Yahoo Finance, MySQL
                       ↳ assinatura, gotchas e limites de cada um: connectors/CLAUDE.md
domain/
  db/                — ETL: fetch → transform → insert. Uma pasta por schema e, dentro dela, uma por
                       FONTE: brasil/{ibge,bcb,tesouro,mdic,mte,ipea,investing},
                       international/{bis,cftc,fred,noaa,yfinance}, us/{inflation} (CPI do BLS + PCE
                       do BEA). Um script por
                       tabela, todos com a mesma interface run()
    registry.py      — tabela → script, derivado da convenção `_TABLE` (73 tabelas; valida em vez de
                       envelhecer em silêncio). É o que faz o --group/--tables/--continuous do
                       update_db.py e o botão do relatório de calendário funcionarem
                       ↳ tabelas ativas, fonte, range, chave primária e gotchas: domain/db/CLAUDE.md
  release_calendar/  — Config estática de QUANDO cada dado é divulgado (calendar_2026.yaml, uma
                       entrada por evento de divulgação) + sync.py (o dado chegou quando devia?) +
                       update_calendar.py (puxa as datas do BCB dos feeds ICS). Não é ETL, nada
                       escreve no MySQL
                       ↳ domain/release_calendar/CLAUDE.md · virada de ano: ROLLOVER.md
analytics/           — Projetos que consomem o banco. Layout país > área desde 2026-08: módulo que lê
                       o schema de um país só vive em brasil/ ou us/; infra de apresentação e
                       cross-country fica na raiz
  report_structure/  — Scaffolding de build-time compartilhado: theme.css, y_autofit.js,
                       tree_helpers.py, builder.py (`render_report()`, que injeta /*REPORT_DATA*/)
  release_calendar/  — Relatório HTML do calendário + serve.py, o modo servido em que o botão
                       "Atualizar" roda o ETL do grupo (abrir_calendario.bat é o atalho de dois
                       cliques). Na raiz porque monitora o sistema inteiro, não uma área
  oraculo/           — Termômetro macro: notas 1–10 por variável (Brasil e EUA) → Power BI
  brasil/            — 9 áreas: exchange_rate, inflation, economic_activity, fiscal_policy, credit,
                       labor_market, monetary_policy (réplica do modelo agregado do BC +
                       relatório de cenários, 2026-08-21), expectations (Focus, 2026-08-24),
                       painel_setores. Cada área = generate_report.py + report.html (+ um módulo por
                       aba) e o seu próprio CLAUDE.md, que é onde vivem abas, fontes e pendências
  us/                — inflation (CPI-U do BLS + PCE do BEA), mesmo padrão; UI em inglês
                       ↳ padrões compartilhados e a regra de corte país/raiz: analytics/CLAUDE.md
jobs/                — Entry points. update_db.py: passe completo de macro_brasil (50 scripts) ou
                       recorte — --continuous (as 7 séries diárias, ~45s: é o que faz sentido agendar
                       todo dia), --group <slug> (o que o botão do calendário chama), --tables a,b,
                       --list. Mais update_international.py (3 scripts), update_us.py (4 passos e a
                       ORDEM importa — ver docstring) e update_oraculo.py
reports/             — Outputs gerados, não versionados, autocontidos e enviáveis. Espelha o país >
                       área de analytics/ (reports/brasil/, reports/us/) — sem isso o Inflation.html
                       do Brasil colidiria com o dos EUA; release_calendar.html fica na raiz pelo
                       mesmo motivo que analytics/release_calendar/. Nomes em Title Case com espaço
                       desde 2026-08 (o sufixo "_latest" foi abandonado), e os defaults de run() de
                       cada generate_report.py já apontam para lá
utils/               — Funções auxiliares compartilhadas
tests/               — Testes pontuais (pytest + harness .js), cada um nascido de um bug específico —
                       não é suíte de cobertura
```


---

## Banco de dados: macro_brasil / macro_international / macro_us

📄 **Organização de schemas, convenção de nomes, tabelas ativas, padrões de chave primária:** [`domain/db/CLAUDE.md`](domain/db/CLAUDE.md) — carrega sob demanda quando o Claude lê arquivos dentro de `domain/db/`.

---

## Connectors

📄 **Documentação completa (API IBGE v3, SGS/Focus do BCB, FRED, MySQL insert/update):** [`connectors/CLAUDE.md`](connectors/CLAUDE.md) — carrega sob demanda quando o Claude lê arquivos dentro de `connectors/`.

---

## analytics/

📄 **Visão geral do diretório, padrões compartilhados entre os relatórios (`/*REPORT_DATA*/`, `data/` vs `referencia/`), e itens de organização pendentes:** [`analytics/CLAUDE.md`](analytics/CLAUDE.md) — carrega sob demanda quando o Claude lê arquivos dentro de `analytics/`.

---

## analytics/oraculo/ — Termômetro Macro

Calcula "notas" (scores 1–10) para variáveis macroeconômicas de Brasil e EUA, alimentando dashboards Power BI.

📄 **Componentes, fluxo de execução, padrão de `scores.py`:** [`analytics/oraculo/CLAUDE.md`](analytics/oraculo/CLAUDE.md) — carrega sob demanda quando o Claude lê arquivos dentro de `analytics/oraculo/`.

---

## analytics/brasil/exchange_rate/ — Panorama Cambial

Relatório HTML interativo de fundamentos cambiais. Arquivo único autocontido — abre em qualquer browser, enviável por email/Dropbox. Desde 2026-08 inclui as 3 abas de modelo que antes eram um segundo arquivo (`reports/ppp_dashboard.html`, template próprio + entry point próprio, ambos retirados na fusão).

📄 **Como gerar, arquitetura do relatório, mapeamento seção→schema→tabela, gotchas atuais, pendências:** [`analytics/brasil/exchange_rate/CLAUDE.md`](analytics/brasil/exchange_rate/CLAUDE.md) — carrega sob demanda quando o Claude lê arquivos dentro de `analytics/brasil/exchange_rate/`.

---

## analytics/brasil/inflation/ — Panorama de Inflação

Relatório HTML de decomposição do IPCA/IPCA-15. Decomposição por subitem vive em `macro_brasil` (`inflc_decomposicao` + `inflc_dim`); agregados BCB/SGS vêm de um CSV separado (`ipca_bcb_series.csv`, via `fetch_bcb.py`).

📄 **Como gerar, arquitetura, mapa de dados, gotchas atuais, pendências:** [`analytics/brasil/inflation/CLAUDE.md`](analytics/brasil/inflation/CLAUDE.md) — carrega sob demanda quando o Claude lê arquivos dentro de `analytics/brasil/inflation/`.

---

## analytics/brasil/monetary_policy/ — Modelo agregado do BC, cenários e Curva de Phillips

A réplica do modelo pequeno do BCB foi **removida em 2026-08** (junto com as tabelas
`pm_hiato_seed`/`pm_parametros`), e um modelo novo será construído sobre a extração automatizada do
anexo do RPM (`pm_hiato_produto`/`_vintages`). Ficaram o `phillips_excel.py` (Curva de Phillips
estimada → planilha de auditoria célula a célula) e o material de referência.

**O modelo agregado do BC foi replicado de ponta a ponta** (2026-08-21), do boxe do RI de
jun/2024: `modelo_painel.py` (painel trimestral, dois recortes de janela de HP) +
`modelo_agregado.py` (espaço de estados, estimação, decomposições, simulador de cenários) →
`generate_report.py` → `reports/brasil/Monetary Policy.html`, com as abas **Cenários**,
**Decomposição**, **Taxa Neutra** e **Hiato** prontas (Projeções do Copom segue stub). Desde
2026-08-24 a aba default é **Modelo BC — Agregado**, a única do projeto em que o modelo roda **no
navegador**: o simulador está portado para JS, e a seção de inputs segue a estrutura da aba Ridge
do FX Report (uma caixa por trimestre sempre visível, atalhos que preenchem as caixas, gráfico por
input, cenários com plotar/carregar/editar). Cada input é endógeno, premissa ou estimativa do
modelo, e os cenários ficam no `localStorage`. A Selic pode ser resposta ali, pela
eq. (3) — extensão nossa, o `simular()` do Python só a aceita como caminho dado.

Validação: **17 dos 22** parâmetros dentro do intervalo de credibilidade de 90% que o próprio BC
publica, hiato latente com correlação **0,990** contra o `pm_hiato_produto`, e — o teste mais direto
de implementação — **o mesmo motor rodado com as modas publicadas reproduz o IRF do BC com erro
absoluto médio de 0,030 p.p., picando no mesmo trimestre**. O que sobra de diferença no IRF com os
nossos parâmetros é estimativa, não código.

**A equação (5) de expectativas está resolvida no simulador** (2026-08-21): o modelo é linear, então
o ponto fixo é um sistema afim `(I−G)π^e = g`, resolvido de uma vez em vez de iterado (resíduo 1e-14).
Isso reconcilia a nota antiga de que "Fair-Taylor divergiu por instabilidade" — o motor de então
aproximava a Selic esperada pela corrente, o mesmo bug que inflava o IRF 4-5x, e era ele que inflava
o laço; com `i^e` lido do caminho de juros o raio espectral cai para 0,68. Mas a fronteira é real:
passa de 1 em φ₂ ≈ 0,32, e acima disso a condição terminal passa a determinar a resposta. Os φ vêm
de estimador próprio (`estimar_eq5`, mínimos quadrados não lineares, R² 0,898); no filtro π^e segue
como dado observado da Focus. **A única premissa que sobrou no cenário são os preços administrados.**
306 asserções em `tests/test_monetary_policy_js.js` e 19 em `tests/test_eq5_expectativas.py` — as
seções 19-25 do primeiro rodam o motor JS nas **mesmas 12 configurações** que o Python pré-simulou e
exigem que batam série a série (discrepância máxima 5e-5, o piso do arredondamento do payload).

**Comunicados do Copom → `pm_copom_projecoes`** (2026-08): o texto das 233 reuniões que a API do BCB
devolve (48ª/2000-06 → 280ª) está versionado em
`repository/monetary_policy/raw_md/central_bank_comunication/`, e as projeções de inflação do próprio
Copom — IPCA/livres/administrados por período, com o ponto do horizonte relevante marcado — viraram
tabela em `macro_brasil`. É a contrapartida oficial do `expc_focus*`: o que o BC projeta, não o que o
mercado espera. Levantamento da fonte por era, e a armadilha do nome do cenário que trocou de
significado em 2022, em [`domain/db/brasil/bcb/copom_comunicados.md`](domain/db/brasil/bcb/copom_comunicados.md).

📄 **O que foi removido e por quê, a lacuna da curva forward que não deve ser repetida no modelo novo,
conteúdo de `referencia/`/`models/`, pendências:**
[`analytics/brasil/monetary_policy/CLAUDE.md`](analytics/brasil/monetary_policy/CLAUDE.md) — carrega sob
demanda quando o Claude lê arquivos dentro de `analytics/brasil/monetary_policy/`.

---

## analytics/brasil/expectations/ — Panorama de Expectativas (Focus)

Relatório de **escopo fechado** (2026-08-24): lê `expc_focus`, `expc_focus_copom` e
`expc_focus_periodo` e **nada mais** — sem meta de inflação, sem realizado, sem projeção do Copom, por
decisão explícita do usuário. 8 abas: Boletim (mediana de hoje × 1/4/12/52 semanas), Revisão (fixa o
período previsto e varre as datas de pesquisa, com eixo alternativo em "meses até o período"), Curva
do Copom (curva por reunião + horizonte ao longo do tempo + mapa de calor), Horizonte Móvel, Trajetória
(a curva à frente inteira numa semana), Dispersão, Bases (0 × 1) e Apêndice.

O que resolve o problema de tamanho: **grade semanal global** (1.425 semanas) e séries comprimidas
como `{i0, m[], s[], n[]}` — 1,28 M de linhas viram um payload de 5,6 MB. Duas regras de redução
diferentes de propósito (JOIN com o `MAX(date)` da semana na `expc_focus_periodo`, para a tabela do
Boletim ser transversal a uma mesma data de pesquisa; último ponto por série nas outras duas). Dois
testes: `tests/test_expectations_js.js` (framework + os 8 renderizadores contra o payload real) e
`tests/test_expectations_data.py` (o **arquivo gerado** contra o MySQL, valor a valor — a compressão
desloca séries no tempo sem lançar exceção nenhuma).

📄 **Abas, grade/compressão, gotchas da fonte e pendências:**
[`analytics/brasil/expectations/CLAUDE.md`](analytics/brasil/expectations/CLAUDE.md) — carrega sob
demanda quando o Claude lê arquivos dentro de `analytics/brasil/expectations/`.

---

## Extração de PDFs para bibliography

Ao converter PDFs em `.md` para alimentar o agente de análise, use a seguinte lógica de roteamento:

| Tipo de PDF | Abordagem | Custo |
|---|---|---|
| Born digital, coluna única (ex: cartas Verde) | Script `utils/extract_pdf.py` (pdfplumber) | Zero tokens |
| Artigos acadêmicos 2 colunas, relatórios de research | Ler com Claude diretamente na sessão (Read tool) | Zero tokens extras (já na sessão) |
| PDFs novos complexos num pipeline automatizado | API Claude Haiku via `anthropic` SDK | ~$0.02/artigo |
| PDFs escaneados (sem camada de texto) | Nenhuma das opções acima funciona — usar OCR externo | Variável |

**Regras:**
- Para as cartas da Verde (81 PDFs, coluna única, born digital): sempre usar o script.
- Para papers acadêmicos e relatórios de research na `repository/`: ler na sessão e gerar `.md` estruturado diretamente.
- A estrutura `.md` (headers, seções) só importa para legibilidade humana no Obsidian. Para o agente, texto limpo é suficiente.
- Nunca usar `pypdf` para PDFs de 2 colunas — a ordem de leitura fica errada.
- `pdfplumber` e `pymupdf` produzem Unicode correto (ç, ã, é) — o display `?` no terminal Windows é apenas artefato de codepage, não corrupção.

---

## repository/ — curated knowledge base (bibliography + conceptual maps)

Since 2026-07, organized by topic area (exchange rate, monetary policy, trader, and future ones: economic activity, fiscal policy, inflation, labor market), each with a literature → data → conceptual map pipeline. Named `agent_bibliography/` before — old name still turns up in git history/older docs, treat as a synonym. Doesn't use or reconcile with `obsidian/`'s own concept/synthesis pages — deliberately parallel systems, per explicit user instruction. Does interact with `repository/ingestion/` (2026-08) — that's the PDF ingestion pipeline itself, living inside this tree: drop a PDF in `repository/ingestion/land_space/<topic>/`, run `repository/ingestion/scripts/run.py`, and it populates `raw_pdf/`/`raw_md/`/`clean_md/` in one command.

📄 **Folder structure, methodology, per-topic status, and pending items:** [`repository/CLAUDE.md`](repository/CLAUDE.md) — loads on demand when Claude reads files inside `repository/` (unlike this root file, which loads in full every session).

**Three branches of exchange-rate material (2026-07):**
1. **Curation** (`repository/exchange_rate/` + `repository/agent_mapping/*`) — literature → conceptual map pipeline. Not team-facing, it's the base that feeds the agent. Full detail in `repository/CLAUDE.md`.
2. **Consolidated** (`team_materials/agent_materials/exchange_rate/`) — condensed, presentable synthesis for team discussion (bibliography, conceptual map, data inventory, EN/PT introduction, two interactive HTML explorers).
3. **Analytical** (`analytics/brasil/exchange_rate/`) — applied/analytical branch, same pattern as `analytics/brasil/inflation/` (code + HTML report + `referencia/`). See its own section above.

---

## obsidian/ — Vault de conhecimento macro

Vault Obsidian cross-linked por área macro (`exchange_rate`, `monetary_policy`, `inflation`, `fiscal_policy`, `labor_market`, `economic_activity`), voltado para leitura/navegação por humanos e agentes — não é um arquivo de material bruto. Cada tópico segue um modelo de três camadas: `concepts/` (notas atômicas de teoria, densamente linkadas), `sources/` (material completo por fonte, só com boilerplate/disclaimers removidos — equivalente ao `clean_md` do `repository/`, nova em 2026-08 e ainda vazia), `synthesis/` (notas condensadas por fonte, já populadas para várias áreas). Deliberadamente paralelo ao `repository/`'s `agent_mapping/`, por instrução explícita do usuário — mas as duas árvores passaram a compartilhar a camada de extração bruta em 2026-08 (ver histórico abaixo).

📄 **Definição de cada camada, status por tópico, histórico da reorganização de 2026-08, pendências:** [`obsidian/CLAUDE.md`](obsidian/CLAUDE.md) — carrega sob demanda quando o Claude lê arquivos dentro de `obsidian/`.

---

## Gerenciamento de pacotes: uv + pyproject.toml

📄 **Documentação completa:** [`AMBIENTE.md`](AMBIENTE.md) — racional do `uv`, papel de cada arquivo (`pyproject.toml`, `uv.lock`, `.venv`), setup em máquina nova, como atualizar versões, manutenção e troubleshooting. Resumo abaixo.

```powershell
# Adicionar pacote
uv add nome-do-pacote

# Configurar em nova máquina
uv sync
uv pip install -e .   # instala o projeto em modo editável (necessário uma vez)
cp .env.example .env
# Editar .env com credenciais
```

**Nunca** usar `pip install` direto — o `pyproject.toml` não será atualizado.

### Instalação editável (`uv pip install -e .`)

Cria um `.pth` no venv que aponta para a raiz do projeto, resolvendo todos os imports (`connectors`, `domain`, `analytics`, `utils`) independentemente de onde o script é executado. Deve ser rodado **uma vez** em cada máquina após `uv sync`. Sem isso, `python jobs\update_oraculo.py` falha com `ModuleNotFoundError: No module named 'analytics'`.

Todos os pacotes Python do projeto (`connectors/`, `domain/`, `analytics/`, `utils/`) precisam ter `__init__.py` para serem encontrados pelo `setuptools.packages.find`.

---

## Pendências (próximas sessões)

Cada relatório em reconstrução tem seu próprio "Pending" atualizado no `CLAUDE.md` da pasta — histórico
rodada-a-rodada de como cada um chegou ao estado atual vive só no git log, não aqui.

### Alta prioridade
- **`analytics/brasil/exchange_rate/`**: ver "Pending" em [`analytics/brasil/exchange_rate/CLAUDE.md`](analytics/brasil/exchange_rate/CLAUDE.md).
- **`analytics/brasil/inflation/`**: ver "Pending" em [`analytics/brasil/inflation/CLAUDE.md`](analytics/brasil/inflation/CLAUDE.md).
- **`analytics/brasil/economic_activity/`**: 6 abas (PIB, Produção Industrial, Comércio, Serviços, IBC-Br,
  Apêndice), framework interativo comum às 5 abas de dados (multiselect, toggle Y/Y↔acumulado, momentum
  scatter/heatmap); só a aba PIB tem decomposição de crescimento (as outras 4 não têm tabela de
  peso nominal/taxa oficial). Ver "Pending" em
  [`analytics/brasil/economic_activity/CLAUDE.md`](analytics/brasil/economic_activity/CLAUDE.md) — falta principalmente
  confirmar visualmente num browser real (sandbox sem browser disponível).
- **`analytics/brasil/fiscal_policy/`**: 5 abas (Receitas e Despesas GFSM+RTN — aba padrão, com seletor de Esfera
  União/Estados/Municípios/Geral —, Dívida Líquida/DLSP — 9 tabelas, uma por fator condicionante, nova em
  2026-08 —, Investimento — GND × função e GND × natureza, nova em 2026-08 —, Impulso Fiscal/IEG,
  Apêndice). Das 3 abas antigas apagadas a pedido do usuário, Dívida
  Pública foi superada pela nova aba Dívida Líquida (fonte melhor); Visão Geral e Resultado Fiscal seguem
  sem reconstrução. Ver "Pending" em [`analytics/brasil/fiscal_policy/CLAUDE.md`](analytics/brasil/fiscal_policy/CLAUDE.md)
  (inclui o double-count de transferências intergovernamentais no total Governo Geral, re-estimação dos
  multiplicadores do IEG, e o bloqueio do MEFA).
- **`analytics/brasil/credit/`**: substituiu `analytics/credit_stress/` (removida junto com a tabela
  `insolv_falencia_rj` e `connectors/datajud.py` a pedido do usuário — histórico só em git log). Hoje
  tem Saldo (+ 2ª tabela para Crédito Ampliado), Concessão (ambas via a fábrica JS `makeHierTab()`,
  toggle Nominal/Real/% PIB), Taxa & Spread e Inadimplência (formato bespoke, com overlay de Selic), +
  Impulso (3 tabelas via `makeImpulseTab()`) e PTC (`cred_ptc`, nova em 2026-08 — árvore
  Oferta/Demanda × 4 segmentos, pill Observada|Esperada, sem linha de total, régua da escala
  −2..+2 no topo, mais uma 2ª tabela+gráfico de **surpresa**: o desvio
  `observada(t) − esperada(t−1)` em **média móvel de 4 trimestres** na tabela e nas linhas grossas
  do gráfico, com o trimestre cru na linha fina; faixa "em linha" = |MA| ≤ σ₀ da própria MA (RQM em torno de zero, não sd em torno da
  média — a troca foi um bug corrigido em 2026-08) — um
  critério de 1/N foi tentado antes e retirado, ver o CLAUDE.md da pasta), + Apêndice.
  Ver "Pending" em [`analytics/brasil/credit/CLAUDE.md`](analytics/brasil/credit/CLAUDE.md) (confirmação em
  browser real, `cred_credito_controle_capital.saldo`/`provisoes` ainda não charteados).
- **`analytics/brasil/expectations/`**: construído e testado em 2026-08-24; falta **confirmação
  visual num browser real** — em especial o mapa de calor da aba Copom (único gráfico não-linha) e o
  eixo invertido da aba Revisão. Ver "Pending" em
  [`analytics/brasil/expectations/CLAUDE.md`](analytics/brasil/expectations/CLAUDE.md).

### Média prioridade
- **Expectativas Focus — consumo nos relatórios**: **o relatório dedicado existe desde 2026-08-24**
  (`analytics/brasil/expectations/` → `reports/brasil/Expectations.html`, 8 abas sobre as 3 tabelas e
  nada mais — inclusive o gráfico de convergência, que só a `expc_focus_periodo.data_referencia`
  permite). O que segue pendente é o consumo **dentro das outras áreas**, onde a expectativa entra
  cruzada com meta/realizado/modelo — coisa que o relatório de escopo "só Focus" deliberadamente não
  faz. Por ordem de retorno: (a) `expc_focus_copom` no modelo de política monetária — é a curva
  forward cuja ausência produziu o IRF 4-5x maior que o do BCB na réplica removida (o motor
  aproximava a Selic futura pela taxa corrente); o `MODEL_REPLICATION_PLAN.md` registra que
  `i^e_{t,t+4|t}` precisa da média ponderada 0,5/1/1/1/0,5 dos 4 trimestres à frente; (b) aba de
  expectativas em `analytics/brasil/inflation/` — o que o Panorama de Expectativas não pode mostrar:
  as medianas anuais **contra `inflc_meta`**; (c) diferenciais ex-ante em
  `analytics/brasil/exchange_rate/`, pendência já aberta em 3 `CLAUDE.md`; (d) consenso vs. realizado
  em `economic_activity/`, `fiscal_policy/` e `labor_market/`.
- **Focus Top5 não carregado**: os 6 endpoints Top5 têm a mesma forma de chave das 3 tabelas mais a
  dimensão `tipo_calculo`, que já existe na chave com valor `'geral'` — então é backfill de dados,
  não migração. Só vale se a leitura "consenso vs. Top5" interessar. `base_calculo=1` na
  `expc_focus_periodo` está na mesma situação.
- **Mercado de trabalho — pendências pós-Novo CAGED** (o conector do FTP e as 3 tabelas de corte
  ficaram prontos em 2026-08, ver `domain/db/brasil/mte/` e `analytics/brasil/labor_market/fontes_dados.md`;
  a rotulagem estoque-vs-saldo de `mt_caged.py` e a integração das 3 tabelas ao relatório foram
  resolvidas em 2026-08, ver a aba "Emprego Formal"):
  (a) cortes do microdado ainda não modelados: município, ocupação (CBO), sexo/idade/instrução/raça
  — todos disponíveis no mesmo microdado já baixado, adicionar é só uma tabela irmã nova com o
  mesmo padrão (`categoria`/`metrica`), sem migração;
  (b) `mt_pnad_trimestral`: nível UF/N3 deixado de fora deliberadamente, sem previsão.
- **US — expandir dados**: mapeamento de fontes das 8 áreas macro pronto em [`us_project/`](us_project/)
  (levantado ao vivo contra as APIs, 377 séries FRED conferidas uma a uma). Prontos: `connectors/bls.py`
  (2026-08, substitui o stub morto de `not_in_production/`; chave da API instalada no `.env`, limites
  medidos ao vivo — 50 séries / 20 anos por requisição) e a hierarquia do CPI em
  [`us_project/inflation_hierarchy.md`](us_project/inflation_hierarchy.md) (as **duas** árvores: a de
  despesa, 355 itens × 10 níveis na versão carregada, e a do news release, 37 linhas × 5 níveis — food/energy/core goods/
  core services, extraída da Tabela 1 do release, onde o BLS declara a hierarquia na própria marcação
  HTML; validada com 111/111 índices publicados batendo com a API).
  **O ramo de inflação está construído** (2026-08): schema `macro_us` com 5 tabelas
  (`inflc_cpi` 341 mil linhas 1913→hoje, `inflc_cpi_dim` as 2 árvores, `inflc_cpi_pesos` 2020-2025,
  mais `inflc_pce` 608 mil linhas 1959→hoje e `inflc_pce_dim`),
  ETL em `domain/db/us/inflation/` + `jobs/update_us.py`, e o relatório em `analytics/us/inflation/`.
  Validado contra a Tabela 1 publicada: os 111 índices conferem exatos e o headline/core/energy/food
  y/y batem na arredondamento do BLS. Cada aba de árvore tem toggle **Series | Table 1** — a segunda
  troca as 12 colunas de mês pelas 9 do news release, com a importância relativa *reconstruída* da
  planilha de dezembro (as 37 publicadas batem em 0,0008), então não há tabela de pesos mensais a
  carregar.
  **O PCE entrou em 2026-08-20** como 3ª aba do mesmo relatório, e sem a chave do BEA que estava
  registrada aqui como pendência: o BEA publica as tabelas 2.4.4U (índice de preço) e 2.4.5U (despesa
  nominal) num xlsx aberto de 12 MB, mensais desde 1959, e as duas casam **linha a linha** — 368 linhas
  de árvore em 9 níveis + 34 agregados de addenda. É fonte melhor que a do CPI em três pontos medidos:
  os **níveis 1-4 particionam o índice exatamente** (contra 0-2 da árvore de divulgação do CPI), o peso
  é **mensal** em vez de snapshot de dezembro, e a contribuição reconstrói o headline com 0,0009 p.p. de
  erro médio contra 0,0124 do CPI. O detalhe que não se adivinha: **19 linhas entram subtraindo** no
  total e só 4 dizem `Less:` no rótulo — a subárvore inteira herda o sinal, e somar um nível sem isso dá
  116% do PCE.
  **Falta**: as outras 7 áreas macro (só `bls.py` e `bea.py` existem), os pesos pré-2020 do CPI (existem
  desde 1947 no site do BLS, em 2 formatos antigos sem parser — é lacuna de parser, não de dado),
  CPI-W/C-CPI-U (schema e loader suportam, não carregados) e, do lado do PCE, as tabelas **reais** nas
  mesmas 402 linhas (2.4.3U índices de quantidade e 2.4.6U dólares encadeados — seriam um `medida` novo
  na mesma árvore, mas são atividade, não inflação: pelo critério de prefixo temático virariam `atv_`).
  Ver "Pending" em [`analytics/us/inflation/CLAUDE.md`](analytics/us/inflation/CLAUDE.md).
- **`repository/` — curation pending items** (conceptual maps, bibliography gaps, trader scope): ver "Pending" em [`repository/CLAUDE.md`](repository/CLAUDE.md).
- **Jobs de rotina incompletos** (a checagem de freshness em `domain/release_calendar/sync.py` confirmou
  em 2026-08-17 que isto causa atraso real, não só teórico: `comm_icbr`/`comm_icbr_usd` estavam um mês
  atrás e avançaram ao rodar o script à mão). O `--continuous` do `update_db.py` (2026-08) fechou
  metade do buraco: `cmb_ptax`, `cmb_dollar_index`, `cmb_dollar_index_em`, `cmb_fx_latam`,
  `cmb_equity_us`, `comm_brent` e `cmb_policy_rates` já rodam por ele (via `registry.py`, mesmo as 6
  de `macro_international`), então basta agendar `update_db.py --continuous` diariamente. O que segue
  **sem nenhum job**, só à mão ou via `--tables`: `comm_icbr`/`comm_icbr_usd`/`inflc_meta` e
  `inflc_decomposicao_item` (este alimenta os núcleos MA/MS/DP do IPCA-15) em
  `domain/db/brasil/`, `clima_oni`/`cmb_real_rates` em `domain/db/international/`, e
  `cmb_risco_pais` (que por natureza não automatiza — CSV exportado à mão).
  `update_international.py` continua com 3 scripts só.
- **Órfãos de verdade são só duas tabelas** — `comm_brent` e `clima_oni`, ambas insumo da réplica do
  modelo do BCB removida em 2026-08: decidir se voltam a alimentar o modelo novo ou se são dropadas.
  A lista antiga de "órfãos" desta seção estava errada, conferida script a script em 2026-08-19:
  `comm_icbr` (ppp_equilibrium + ridge_deviation_model + phillips_excel), `comm_icbr_usd` e
  `inflc_meta` (ppp_equilibrium + phillips_excel), `atv_pib_usd` (generate_report do câmbio +
  ppp_equilibrium), `cmb_dollar_index`/`cmb_dollar_index_em`/`cmb_policy_rates`/`cmb_equity_us`
  (ppp_equilibrium) e `cmb_real_rates` (real_rates_comparison.py) todas têm consumidor vivo — o que
  a remoção da réplica quebrou foi menos do que se registrou na época.
- **`team_materials/agent_materials/exchange_rate/` — notas desatualizadas**: `data_inventory.md` ainda diz que o `conceptual_map.md` "não foi construído" (já foi); `introduction_pt.md` não lista o `conceptual_map.md` entre os documentos da pasta.
- **Kinea PDF órfão**: `team_materials/agent_materials/exchange_rate/kinea_fx_mental_models.pdf` existe mas não há `.md` de origem em lugar nenhum, e `bibliography.md` ainda marca Kinea como "pendente" — investigar se é um artefato de teste esquecido ou uma síntese real nunca finalizada (fonte bruta: `repository/mental_model/kinea_insights/`).
- **`analytics/brasil/monetary_policy/`**: a equação (5) e a escala do regressor de clima foram
  resolvidas em 2026-08-21 (o ONI entra em **décimos de grau**, não em graus — α₅ e α₆ saíram do teto
  da priori e caíram dentro do IC publicado; e a eq. (5) virou um sistema afim resolvido de uma vez
  no simulador). O que restou, em ordem: o **bloco de preços administrados** (boxe do RI de set/2017),
  que é a única premissa que ainda fecha o IPCA no cenário e o que separa o nosso IRF completo da
  primeira linha do Graf 4B — os alvos de validação já estão levantados (10% de depreciação → +1,65
  p.p. nos administrados, +0,72 nos livres, +0,96 no IPCA); a **aba Projeções do Copom**; e levar a
  eq. (5) **para dentro do filtro**, que é a única via para testar se o α₁ᴵ se corrige (exige π^e como
  estado e uma convenção, não publicada, para o que o modelo espera dos exógenos em cada trimestre da
  amostra). Ver "Pending" em
  [`analytics/brasil/monetary_policy/CLAUDE.md`](analytics/brasil/monetary_policy/CLAUDE.md).
- **Taxa neutra: a premissa que domina os cenários.** Com dado até 2026T2 a especificação do boxe
  põe r* em ~7,9% (tendência HP do juro real Focus + passeio aleatório), contra ~4,8% da mediana que
  o BC publicou para 2024T2. Isso faz a Selic de 15% parecer pouco restritiva e uma Selic de 10%
  parecer expansionista. Não é bug, é a definição — mas decidir se ela é aceitável vem antes de usar
  os cenários para decisão.

### Baixa prioridade
- (nenhuma pendência no momento)
