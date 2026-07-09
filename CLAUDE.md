# Sistema de Dados — Contexto para o Claude

## Regras gerais

- **The text should remain in the language it already is, NO TRANSLATION.** When generating `.md` files from English-language PDFs, write in English. When generating from Portuguese-language sources, write in Portuguese.

## Sobre o Projeto

Sistema de dados da LIS Capital para coleta, processamento e visualização de variáveis macroeconômicas (Brasil, EUA). Alimenta dashboards Power BI e materiais de análise macro.

---

## Arquitetura atual

```
connectors/          — Clientes de APIs externas (IBGE, BCB, FRED, BIS, CFTC, MySQL)
domain/
  db/brasil/         — ETL Brasil: fetch → transform → insert em macro_brasil
    ibge/            — Scripts por pesquisa IBGE (atv_pim, atv_pib, atv_pmc,
                       atv_pms, mt_pnad, inflc_decomposicao, inflc_dim)
    bcb/             — Scripts por tema BCB (atv_ibcbr, inflc_agregados, mt_caged,
                       cred_credito_amplo, expc_focus, cred_credito_familias, cmb_reservas_bc,
                       cmb_balanco_pagmt, cmb_fluxo_cambial, cmb_termos_troca, cmb_cambio_contratado)
  db/international/  — ETL dados cross-country: fetch → insert em macro_international
    bis/             — cmb_reer (REER Brasil/MX/CL/CO via BIS API)
    cftc/            — cmb_cot_fx (posicionamento especulativo BRL/MXN)
    fred/            — diferenciais_juros (Selic × Fed Funds, real ex-post — precisa de BR+US)
analytics/           — Projetos que consomem o banco MySQL
  oraculo/           — Termômetro macro (brasil e us)
  painel_setores/    — Painel de setores
  cambio/            — Panorama Cambial HTML  [ver CAMBIO.md]
    generate_report.py  — Lê macro_brasil/macro_international, injeta JSON no template, salva HTML
    report.html         — Template fixo (HTML + CSS + Plotly.js CDN)
  inflation/         — Panorama de Inflação HTML  [ver INFLATION.md]
    fetch_bcb.py         — Agregados BCB/SGS (IPCA headline/componentes/núcleos) → data/ipca_bcb_series.csv (+ STL _ma3_sa)
    generate_report.py   — Lê Excel (subitens) + CSV (agregados), injeta JSON no template, salva HTML
    report.html           — Template fixo (HTML + CSS + Plotly.js CDN)
    data/                 — Excel (decomposição por subitem, fora do MySQL) + CSV (agregados BCB)
jobs/                — Entry points
  update_db.py          — Atualiza todas as tabelas de macro_brasil
  update_international.py — Atualiza macro_international (cmb_reer, cmb_cot_fx, diferenciais_juros)
  update_oraculo.py     — Atualiza o oráculo
reports/             — Outputs gerados (não versionados)
  cambio_latest.html — Relatório cambial mais recente (autocontido, enviável)
utils/               — Funções auxiliares compartilhadas
quarantine/          — Scripts e materiais legados/experimentais (não fazem parte do ETL)
```


---

## Banco de dados: macro_brasil

**Servidor:** 192.168.15.200 (rede local da empresa)  
**Credenciais:** `.env` (nunca hardcoded)

📄 **Como os schemas são organizados (por domínio/geografia, não por estágio bruto/calculado) e por que `macro_analytics` foi descontinuado:** [`DB_SCHEMAS.md`](DB_SCHEMAS.md)

Nomes de tabela são prefixados por tema macro (`atv_` = atividade, `mt_` =
mercado de trabalho, `cred_` = crédito, `cmb_` = câmbio, `inflc_` = inflação,
`expc_` = expectativas) para facilitar organização visual dentro de cada
schema — ver [`DB_SCHEMAS.md`](DB_SCHEMAS.md) para o critério completo.
Renomeação feita em 2026-07, em duas rodadas: primeiro para prefixos por
extenso (`pim`→`atividade_pim`), depois abreviados por instrução explícita do
usuário (`atividade_pim`→`atv_pim`, `atividade_gdp`→`atv_pib`, etc.) — mapeamento
completo em [`DB_SCHEMAS.md`](DB_SCHEMAS.md). `mt_pnad`/`mt_caged` ficaram de
fora da segunda rodada (mantidos com o prefixo por extenso).

### Tabelas ativas

| Tabela | Fonte | Período disponível | Script |
|---|---|---|---|
| `atv_pim` | IBGE 8888 | 2002 → hoje | `ibge/atv_pim.py` |
| `atv_pib` | IBGE 1620/1621 | 2016 → hoje | `ibge/atv_pib.py` |
| `atv_pmc` | IBGE 8880/8881/8883 | 2023 → hoje | `ibge/atv_pmc.py` |
| `atv_pms` | IBGE 8688 | 2023 → hoje | `ibge/atv_pms.py` |
| `atv_ibcbr` | BCB SGS (12 séries) | 2003 → hoje | `bcb/atv_ibcbr.py` |
| `mt_pnad` | IBGE 6318/6320/6323/6387/6388/6389/6391/6392 | 2024 → hoje | `ibge/mt_pnad.py` |
| `mt_caged` | BCB SGS (14 séries) | 1992 → hoje | `bcb/mt_caged.py` |
| `cred_credito_amplo` | BCB SGS (17 séries crédito amplo) | 2013 → hoje | `bcb/cred_credito_amplo.py` |
| `cred_credito_familias` | BCB SGS (3 séries — endividamento/renda famílias) | 2005 → hoje | `bcb/cred_credito_familias.py` |
| `inflc_agregados` | BCB SGS (33 séries IPCA/IPCA-15 + núcleos) | 1980 → hoje | `bcb/inflc_agregados.py` |
| `inflc_decomposicao` | IBGE 7060/7062 (subitem: var_mensal/pesos/contribuicao) | 2020 → hoje | `ibge/inflc_decomposicao.py` |
| `inflc_dim` | Subitem → Grupo/Subgrupo/Item (manual) + Subjacente/núcleos (híbrido, ver INFLATION.md) | — (sem data) | `ibge/inflc_dim.py` |
| `expc_focus` | BCB Focus (IPCA 12m/24m, IGP-M, Selic) | 2001 → hoje | `bcb/expc_focus.py` |

`inflc_agregados` (renomeada de `inflacao` em 2026-07, depois de
`ipca_agregados`, depois de `inflation_agregados`, todas em 2026-07 até chegar
no prefixo abreviado atual; séries agora em minúsculo, ex: `ipca_nucleo_p55`)
tem documentação nativa no MySQL: `COMMENT` na tabela e na coluna `name` (lista
cada série com seu código SGS) — visível via `SHOW CREATE TABLE inflc_agregados`
ou no editor de tabelas do Workbench.

### Schema das tabelas

Todas as tabelas usam **chave primária composta natural** (sem `id` sintético):

```sql
-- Séries com ajuste sazonal
PRIMARY KEY (date, name, seasonal_adjs)   -- atv_pim, atv_pib, atv_pmc, atv_pms

-- Séries sem ajuste sazonal  
PRIMARY KEY (date, name)                  -- inflc_agregados, mt_caged, cred_credito_amplo, atv_ibcbr, cred_credito_familias
PRIMARY KEY (date, name, region)          -- mt_pnad

-- Expectativas Focus
PRIMARY KEY (date, indicador, horizonte)  -- expc_focus

-- IPCA por subitem
PRIMARY KEY (date, indice, subitem)       -- inflc_decomposicao (indice = IPCA | IPCA15)
PRIMARY KEY (subitem)                     -- inflc_dim (tabela de dimensao, sem data)
```

`ON DUPLICATE KEY UPDATE` no insert garante upsert idempotente.

---

## Connectors

### `connectors/ibge.py` — API de Agregados IBGE v3

Cliente paramétrico baseado em `view=flat`. Substituiu o antigo `ibge_get(url, start, end, freq)`.

```python
from connectors.ibge import IBGE

ibge = IBGE()
df = ibge.get(
    agregado=8888,
    variaveis=12606,
    classificacoes={544: "all"},
    localidades={"N1": "all"},
    periodos="last:24",    # ou "202401-202412", "all", (2024, 2024)
)
# date: Timestamp, value: float64, sentinels -> NaN
```

**Detalhes técnicos da API IBGE v3:**
- `periodos`: aceita `YYYYMM-YYYYMM`, `last:N`, `-N`, `all`. A tupla `(ano_ini, ano_fim)` usa metadados para inferir o sufixo correto.
- `view=flat`: primeiro item do array é sempre o cabeçalho — `_parse_flat` pula automaticamente.
- Frequência inferida do cabeçalho `D2N` (`"Mês"`, `"Trimestre"`, `"Trimestre Móvel"`, `"Semestre"`, `"Ano"`).
- `"trimestral móvel"` (PNAD) é mapeado para formato `YYYYMM` igual ao mensal.
- Retry: 6 tentativas, backoff 1s, respeita `Retry-After`.
- `ibge_old.py` foi removido (código morto).

### `connectors/bcb.py` — APIs SGS e Focus do BCB

```python
from connectors.bcb import BCB

bcb = BCB()

# SGS: últimos N meses
df = bcb.get_sgs_ultimos({"ibcbr_nsa": 24363, "ibcbr_sa": 24364}, n=36)

# SGS: por período ou histórico completo
df = bcb.get_sgs(series, start="01/01/2020")
df = bcb.get_sgs(series, start="all")   # série histórica completa desde o início

# Focus/Olinda
df = bcb.get_focus(
    endpoint="ExpectativasMercadoInflacao12Meses",
    indicador="IPCA",
    campos=["Data", "Media", "Mediana", "DesvioPadrao"],
    start="2020-01-01",
    filtros_extras="Suavizada eq 'S' and baseCalculo eq 0",
)
# colunas em snake_case, date como Timestamp
```

**Detalhes técnicos:**
- SGS: `/ultimos/{n}` tem limite ~24 — `get_sgs_ultimos` usa `/dados?dataInicial=...` calculando a data.
- SGS `start="all"` mapeia para `"01/01/1970"` internamente; a API retorna desde o início real da série.
- Focus: URL deve ter `$` literal — `requests(params={})` percent-encoda para `%24` e a API rejeita. URL é construída manualmente.
- `$count` não suportado pelo endpoint Focus do BCB — paginação por `$skip` até `len(page) < page_size`.
- `ExpectativasMercadoSelic` não tem campo `Suavizada` — filtro diferente de inflação.
- Paralelismo: `ThreadPoolExecutor` para múltiplas séries SGS simultâneas.

### `connectors/fred.py` — API FRED (Federal Reserve)

```python
from connectors.fred import FredUniFrame, FredMultFrame

# Série única
df = FredUniFrame("PCE", "PCEPI", "2010-01-01", "2024-12-31")
# colunas: Date, <NameSerie>

# Múltiplas séries (wide ou unpivoted)
df = FredMultFrame({"PCE": "PCEPI", "CPI": "CPIAUCSL"}, "2010-01-01", "2024-12-31")
df_long = FredMultFrame({...}, start, end, Pivot=True)
```

**Detalhes:**
- API key via `FRED_API_KEY` no `.env` — nunca hardcoded.
- `US_IndexNormalize`: expande dados trimestrais para mensais via merge com CPI e `ffill(limit=2)`.
- Arquivo em `connectors/fred.py` (movido de `connectors/not_in_production/` em 2026-05).

### `connectors/mysql.py` — Insert/Update no banco

```python
from connectors.mysql import insert_data_into_database

insert_data_into_database("macro_brasil", "atv_pim", df)
```

Faz `SHOW COLUMNS FROM table`, reordena o df, e executa `INSERT ... ON DUPLICATE KEY UPDATE` em batches de 1000 linhas.

**Bug corrigido:** `.where(pd.notna(df), None)` não convertia NaN em float64 para None — `executemany` enviava `float('nan')` como string `'nan'` ao MySQL. Fix: `df.astype(object).where(...)`.

---

## Padrão dos scripts de domínio

Cada script expõe apenas `run()` — sem execução ao importar.

```python
# Carga histórica (primeira vez)
atv_pim.run(periodos="all")
atv_ibcbr.run(start="all")

# Atualização rotineira (padrão)
atv_pim.run()             # últimos N anos (default do script)
inflc_agregados.run()     # últimos N meses

# Range específico
atv_pib.run(periodos=(2015, 2024))
mt_caged.run(start="01/01/2020", end="31/12/2024")
```

Scripts IBGE usam `periodos=` (formatos do connector IBGE).  
Scripts BCB SGS usam `start=`/`end=` (formato `"DD/MM/YYYY"`) ou `start="all"`.  
`expc_focus.run()` usa `start=` ISO (`"YYYY-MM-DD"`) ou `n_dias=` para janela retroativa.

---

## analytics/oraculo/ — Termômetro Macro

Calcula "notas" (scores 1–10) para variáveis macroeconômicas de Brasil e EUA, alimentando dashboards Power BI.

### Componentes

| Módulo | Função | Output |
|---|---|---|
| `brasil/scores.py` | Notas macro Brasil (inflação, trabalho, crédito, atividade) | `brasil/base/Brasil_base.csv` |
| `us/term_us.py` | Notas macro EUA (labor, inflation, activity, financial, housing) | `us/base/US_BASE.csv` |
| `brasil/thermometer.py` | Múltiplos financeiros BRL (P/E, P/B, EV/EBITDA) | `brasil/base/Brasil_notas_preco.csv` |
| `us/thermometer.py` | Múltiplos financeiros US | `us/base/` |
| `jobs/update_oraculo.py` | Entry point: importa os módulos acima e combina em Central_base.csv | `base/Central_base.csv` |

### Fluxo de execução (reestruturado 2026-05)

```
jobs/update_oraculo.py
  scores.run()   → _load_data() lê macro_brasil → grava Brasil_base.csv → retorna DataFrame
  term_us.run()  → lê FRED/BCB → grava US_BASE.csv → retorna DataFrame
  pd.concat([db_brl, db_us]) → base/Central_base.csv
```

A lógica de scoring está em `utils/thermometer.py` (`Score`, `Score_SMC`, `Score_SA`, `Score_Diff`) e usa sigmóide normalizada para transformar qualquer série em nota 1–10.

### Padrão de `scores.py` (Brasil)

`_load_data()` centraliza todos os reads do banco e popula variáveis de módulo `_data_*`. `run()` chama `_load_data()` uma vez e concatena os frames de scoring. Colunas são renomeadas em `_load_data()` para manter os corpos das funções de scoring inalterados.

Todas as séries consumidas por `_load_data()` vêm de `macro_brasil` via `MySQLDataRequester` — sem dependência direta de connectors externos (BCB, FRED etc.).

**Refatoração 2026-05:**
- Todas as funções de scoring renomeadas para snake_case (ex: `Inflacao` → `inflacao`, `IBC_BR` → `ibc_br`) — nomes de função, não as tabelas (que levam o prefixo de tema desde a renomeação de 2026-07)
- `_finalize(*frames)` elimina boilerplate: `pd.concat([unpivot(f.tail(_N)) for f in frames]).dropna()`
- `serv_divida_renda()`: usa `comp_renda_servico_total` diretamente do banco (antes reconstruía via juros + amortização)
- `saldo_credito_empresas()`: `deflator.reindex(df.index)` antes da divisão para alinhar índices corretamente
- `ibc_br()`: label corrigido (`'IBC_BR - [MA(Var(Yt, 12))]'` — parêntese faltando antes)

---

## analytics/cambio/ — Panorama Cambial

Relatório HTML interativo de fundamentos cambiais. Arquivo único autocontido — abre em qualquer browser, enviável por email/Dropbox.

📄 **Status, pendências e roadmap completos:** [`CAMBIO.md`](CAMBIO.md)

### Como gerar

```powershell
uv run python jobs/update_db.py          # atualiza macro_brasil (inclui cmb_reservas_bc, cmb_balanco_pagmt, cmb_fluxo_cambial, cmb_termos_troca)
uv run python jobs/update_international.py  # atualiza macro_international (cmb_reer, cmb_cot_fx, diferenciais_juros)
uv run python -c "from analytics.cambio.generate_report import run; run()"
# Saída: reports/cambio_latest.html
```

### Arquitetura do relatório

Template fixo `report.html` com marcador `/*REPORT_DATA*/`. `generate_report.py` lê tabelas de dois schemas, serializa como JSON e substitui o marcador. Sem Jinja2 — só `str.replace()`.

| Seção | Schema | Tabela |
|---|---|---|
| Diferenciais de Juros | `macro_international` | `diferenciais_juros` |
| REER | `macro_international` | `cmb_reer` |
| Posicionamento CFTC | `macro_international` | `cmb_cot_fx` |
| Fluxos e Fundamentos | `macro_brasil` | `cmb_reservas_bc`, `cmb_termos_troca`, `cmb_fluxo_cambial`, `cmb_balanco_pagmt` |

---

## analytics/inflation/ — Panorama de Inflação

Relatório HTML de decomposição do IPCA/IPCA-15 (renomeado de `analytics/ipca/` em 2026-07, rebranding para refletir que o relatório cobre inflação de forma geral, não só o índice IPCA). Desde 2026-07, a decomposição por subitem vive em `macro_brasil` (`inflc_decomposicao` + `inflc_dim`); os agregados BCB/SGS ainda vêm de um CSV separado (`ipca_bcb_series.csv`, via `fetch_bcb.py`).

📄 **Mapa de dados completo:** [`INFLATION.md`](INFLATION.md)

**Pontos-chave:**
- Decomposição por subitem agora é buscada diretamente da API do IBGE (agregados 7060/7062, classificação 315, nível 4 = subitem) por `domain/db/brasil/ibge/inflc_decomposicao.py`, direto para `macro_brasil.inflc_decomposicao`. Os antigos scripts em `quarantine/inflation_decomposition/` (que geravam os xlsx) não são mais usados pelo relatório. Não armazena variação 12 meses (removida em 2026-07 — calcular a partir de `var_mensal` na camada de consumo, não no banco).
- `macro_brasil.inflc_dim` combina duas fontes (2026-07): `grupo`/`subgrupo`/`item` seguem sendo sincronizados a partir de `analytics/inflation/data/tabela_dimensao_ipca.xlsx` (mantido manualmente). `subjacente` (Serviços/Bens Industriais) e os 7 flags `nucleo_ex0/ex01/ex02/ex03/ex03_servicos/ex03_industriais/exfe` são derivados de `analytics/inflation/data/Vetores_NT_57.xlsx` — vetor de agregação **oficial** do BC (Nota Técnica BCB nº 57, dez/2025), com precedência sobre a planilha manual. "Alimentos Subjacente" continua vindo do xlsx manual (sem equivalente oficial). Ver `INFLATION.md` para o detalhe completo.
- IPCA e IPCA-15 usam **IDs de variável diferentes** no mesmo esquema de classificação (63/66 vs 355/357) — ver docstring de `inflc_decomposicao.py`.
- Agregados BCB/SGS (`ipca_bcb_series.csv`, via `fetch_bcb.py`) ainda duplicam ~33 das 34 séries já em `macro_brasil.inflc_agregados` (`fetch_bcb.py` tem uma a mais, `IPCA_12m`, usada no cross-check do KPI "12 Meses") — pipeline separado por ora, sem migração planejada. Note que os nomes de série em `fetch_bcb.py` continuam em maiúsculo (`IPCA_nucleo_P55`) — só as séries em `macro_brasil.inflc_agregados` foram padronizadas para minúsculo.

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
- Para papers acadêmicos e relatórios de research na `agent_bibliography/`: ler na sessão e gerar `.md` estruturado diretamente.
- A estrutura `.md` (headers, seções) só importa para legibilidade humana no Obsidian. Para o agente, texto limpo é suficiente.
- Nunca usar `pypdf` para PDFs de 2 colunas — a ordem de leitura fica errada.
- `pdfplumber` e `pymupdf` produzem Unicode correto (ç, ã, é) — o display `?` no terminal Windows é apenas artefato de codepage, não corrupção.

---

## agent_bibliography/ — estrutura geral e Conceptual Maps

Desde 2026-07, `agent_bibliography/` organiza-se por área temática (exchange rate, monetary policy, e futuras), cada uma com um pipeline literatura → dados. O processo reutilizável está documentado em [`agent_bibliography/BIBLIOGRAPHY_METHODOLOGY.md`](agent_bibliography/BIBLIOGRAPHY_METHODOLOGY.md) — misturar fontes internacionais + Brasil, extrair só os capítulos relevantes de livros, pontuar cada fonte 1-5 em "quão fundacional" (independente da idade) ao lado do ano, organizar em clusters temáticos `#tag`.

Layout de pastas:
```
agent_bibliography/
  BIBLIOGRAPHY_METHODOLOGY.md          — processo reutilizável (não é output de nenhum tópico)
  exchange_rate_policy/                — PDFs brutos adquiridos (28 fontes)
  monetary_policy/                     — PDFs brutos (ainda vazio — candidatos em agent_mapping/recommended_bibliography/)
  agent_mapping/
    conceptual_maps/                   — <topic>_conceptual_map.md, um por área
    recommended_bibliography/          — <topic>_bibliography_candidates.md (pré-aquisição) + <topic>_bibliography_gaps.md (pós-mapa)
    recommended_data/                  — <topic>_data_inventory.md, um por área
```

### Exchange rate (área completa)

`agent_bibliography/agent_mapping/conceptual_maps/exchange_rate_conceptual_map.md` é um mapa de conhecimento single-file, estilo Obsidian (`[[wikilinks]]` para conceitos, `#tags` para clusters temáticos), construído diretamente a partir dos 18 PDFs originais em `agent_bibliography/exchange_rate_policy/` (hoje 28) — **não** a partir de `.md` extraídos (esses foram deletados de propósito; os PDFs são a fonte de verdade). Cobre 9 clusters temáticos (`#market_microstructure`, `#exchange_rate_determination`, `#currency_regimes`, `#balance_of_payments`, `#policy_transmission`, `#applied_valuation_tools`, `#pass_through_and_inflation`, `#capital_controls`, `#currency_crisis_dynamics`).

**Não usa e não reconcilia com** o vault `obsidian/exchange_rate/` (páginas de conceito pré-existentes) — são dois sistemas paralelos por instrução explícita do usuário. Também não interage com o pipeline `ingestion/`.

`agent_bibliography/agent_mapping/recommended_bibliography/exchange_rate_bibliography_gaps.md` lista fontes candidatas para fechar as lacunas identificadas na seção "Coverage notes" do mapa (crisis models de 1ª/2ª/3ª geração, capital controls como ferramenta de política, teoria de OCA, opções de FX/volatilidade, econometria de falha de UIP (Fama 1984), profundidade em EM não-Brasil, economia política do câmbio) — nenhuma dessas fontes foi adquirida/processada ainda.

`agent_bibliography/agent_mapping/recommended_data/exchange_rate_data_inventory.md` mapeia categorias analíticas (preço à vista, carry, termos de troca, BOP, fluxo cambial, reservas, REER, posicionamento, diferencial de inflação) ao que já existe no banco vs. lacunas — maior gap identificado: nenhuma série de câmbio à vista (PTAX) está armazenada hoje.

**Para incrementar a base (próxima sessão ou quando novas fontes chegarem):**
1. Adicionar o(s) PDF(s) em `agent_bibliography/exchange_rate_policy/`, usando a convenção de nome já estabelecida: `topic_description (Author, Year).pdf` (os nomes sugeridos já estão no arquivo de gaps).
2. Processar **um de cada vez** (não paralelizar com agents em background — fluxo de trabalho preferido pelo usuário: extrair texto completo → ler → identificar conceitos novos vs. reforço de existentes → editar o mapa).
3. Extrair texto via `pdfplumber` em Bash (o `Read` tool não renderiza PDF nesta máquina — falta `poppler`/`pdftoppm`); redirecionar para arquivo no scratchpad com `sys.stdout.reconfigure(encoding='utf-8')` para evitar `UnicodeEncodeError` em símbolos não-ASCII no console do Windows.
4. Atualizar o mapa: nova linha na tabela `## Sources processed`, bullets de conceito no(s) `#theme_cluster` correspondente(s) com cross-links `[[conceito]]` para conceitos já existentes quando houver conexão genuína, e remover/marcar a linha correspondente em `exchange_rate_bibliography_gaps.md`.

### Monetary policy (em andamento)

`agent_bibliography/agent_mapping/recommended_bibliography/monetary_policy_bibliography_candidates.md` tem 29 candidatos de literatura em 7 clusters (`#policy_rules_and_credibility`, `#new_keynesian_transmission`, `#inflation_targeting_regimes`, `#transmission_channels_financial_frictions`, `#unconventional_policy_zlb`, `#global_spillovers_em_autonomy`, `#brazil_monetary_policy`) mais uma seção §8 separada para materiais primários do COPOM (Comunicado, Ata, Relatório de Política Monetária) — nenhuma fonte adquirida ainda; escopo/mecanismo de ingestão do §8 ficaram deliberadamente em aberto.

`agent_bibliography/agent_mapping/recommended_data/monetary_policy_data_inventory.md` usa uma estrutura de duas camadas — dados próprios (Selic/decisões COPOM, diferenciais, r*) vs. dados consumidos de outros agentes ainda não construídos (inflação, atividade, fiscal, câmbio) — reflexo da arquitetura multi-agente que a LIS está planejando (um agente por área macro).
5. Manter textos em inglês para fontes em inglês e português para fontes em português (regra geral do projeto) — o mapa em si é escrito em inglês, mas termos técnicos em PT (ex: "posição de câmbio", "repasse cambial") são preservados entre parênteses quando a fonte é em português.

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

### Alta prioridade — Relatório Cambial
Ver pendências e roadmap detalhados em [`CAMBIO.md`](CAMBIO.md).

### Alta prioridade — Relatório de Inflação
Ver mapa de dados e pendências detalhados em [`INFLATION.md`](INFLATION.md). Resumo: decomposição por subitem migrada para `macro_brasil.inflc_decomposicao`/`inflc_dim` (2026-07) e já no `jobs/update_db.py`; tabela `inflacao` renomeada em sequência para `ipca_agregados` → `inflation_agregados` → `inflc_agregados` (prefixo de tema, depois abreviado) com séries em minúsculo; falta migrar os agregados BCB/SGS do relatório (`ipca_bcb_series.csv`) para ler de `macro_brasil.inflc_agregados` em vez de duplicar o fetch (e, se migrado, também padronizar os nomes de série para minúsculo lá).

### Média prioridade
- **`analytics/oraculo/us/term_us.py` — revisão de qualidade**: snake_case, `_load_data()` centralizado, bugs de robustez. Se os scores do oráculo migrarem para MySQL no futuro, ver `DB_SCHEMAS.md` — esse é o cenário citado lá como justificativa legítima para um schema de analytics dedicado.
- **US — expandir dados**: `connectors/not_in_production/bls.py`, schema `macro_us`, `domain/db/us/inflation/`.
- **macro_international — itens menores**: confirmar descrições SGS 22099/22100, sub-itens CEP/CBE fluxo cambial, diferenciais ex-ante. Ver `CAMBIO.md`.
- **`agent_bibliography/agent_mapping/conceptual_maps/exchange_rate_conceptual_map.md` — incrementar com fontes de `agent_mapping/recommended_bibliography/exchange_rate_bibliography_gaps.md`**: mapa base (18 fontes, hoje 28) está completo; próximo passo é adquirir e processar fontes para as lacunas listadas (crisis models, capital controls, OCA, FX options, Fama 1984, EM não-Brasil, economia política). Ver seção acima.
- **Monetary policy — iniciar aquisição**: `agent_bibliography/agent_mapping/recommended_bibliography/monetary_policy_bibliography_candidates.md` tem 29 candidatos prontos, nenhum adquirido; ordem sugerida no próprio arquivo. Decisões em aberto no §8 (materiais COPOM): janela de retenção e mecanismo de ingestão (fetcher automatizado planejado, mirroring `domain/db/brasil/bcb/*.py`).

### Baixa prioridade
- `quarantine/` — scripts legados (curva de juros, decomposição IPCA). Limpar quando conveniente.
- `brasil/thermometer.py` lê de `MySQLDataRequester('br_finance', 'brazil_real_yield_curve')` — verificar se schema ainda existe.
