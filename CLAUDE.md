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
    ibge/            — Scripts por pesquisa IBGE (pim, gdp, pmc, pms, pnad)
    bcb/             — Scripts por tema BCB (ibc_br, inflacao, caged, credito, expectativas,
                       indicadores_familias, reservas, balanco_pagamentos, fluxo_cambial, termos_de_troca)
  db/international/  — ETL dados cross-country: fetch → insert em macro_international
    bis/             — reer (REER Brasil/MX/CL/CO via BIS API)
    cftc/            — cot_fx (posicionamento especulativo BRL/MXN)
  db/analytics/      — Séries derivadas: fetch + calcular → insert em macro_analytics
    fred/            — diferenciais_juros (Selic × Fed Funds, real ex-post)
analytics/           — Projetos que consomem o banco MySQL
  oraculo/           — Termômetro macro (brasil e us)
  painel_setores/    — Painel de setores
  cambio/            — Panorama Cambial HTML  [ver CAMBIO.md]
    generate_report.py  — Lê macro_brasil/macro_international/macro_analytics, injeta JSON no template, salva HTML
    report.html         — Template fixo (HTML + CSS + Plotly.js CDN)
jobs/                — Entry points
  update_db.py          — Atualiza todas as tabelas de macro_brasil
  update_international.py — Atualiza macro_international (reer, cot_fx)
  update_analytics.py   — Atualiza macro_analytics (diferenciais_juros)
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

### Tabelas ativas

| Tabela | Fonte | Período disponível | Script |
|---|---|---|---|
| `pim` | IBGE 8888 | 2002 → hoje | `ibge/pim.py` |
| `gdp` | IBGE 1620/1621 | 2016 → hoje | `ibge/gdp.py` |
| `pmc` | IBGE 8880/8881/8883 | 2023 → hoje | `ibge/pmc.py` |
| `pms` | IBGE 8688 | 2023 → hoje | `ibge/pms.py` |
| `pnad` | IBGE 6318/6320/6323/6387/6388/6389/6391/6392 | 2024 → hoje | `ibge/pnad.py` |
| `ibc_br` | BCB SGS (12 séries) | 2003 → hoje | `bcb/ibc_br.py` |
| `inflacao` | BCB SGS (28 séries IPCA + núcleos) | 1980 → hoje | `bcb/inflacao.py` |
| `caged` | BCB SGS (14 séries) | 1992 → hoje | `bcb/caged.py` |
| `credito` | BCB SGS (17 séries crédito amplo) | 2013 → hoje | `bcb/credito.py` |
| `expectativas` | BCB Focus (IPCA 12m/24m, IGP-M, Selic) | 2001 → hoje | `bcb/expectativas.py` |
| `indicadores_familias` | BCB SGS (3 séries — endividamento/renda famílias) | 2005 → hoje | `bcb/indicadores_familias.py` |

### Schema das tabelas

Todas as tabelas usam **chave primária composta natural** (sem `id` sintético):

```sql
-- Séries com ajuste sazonal
PRIMARY KEY (date, name, seasonal_adjs)   -- pim, gdp, pmc, pms

-- Séries sem ajuste sazonal  
PRIMARY KEY (date, name)                  -- inflacao, caged, credito, ibc_br, indicadores_familias
PRIMARY KEY (date, name, region)          -- pnad

-- Expectativas Focus
PRIMARY KEY (date, indicador, horizonte)  -- expectativas
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

insert_data_into_database("macro_brasil", "pim", df)
```

Faz `SHOW COLUMNS FROM table`, reordena o df, e executa `INSERT ... ON DUPLICATE KEY UPDATE` em batches de 1000 linhas.

**Bug corrigido:** `.where(pd.notna(df), None)` não convertia NaN em float64 para None — `executemany` enviava `float('nan')` como string `'nan'` ao MySQL. Fix: `df.astype(object).where(...)`.

---

## Padrão dos scripts de domínio

Cada script expõe apenas `run()` — sem execução ao importar.

```python
# Carga histórica (primeira vez)
pim.run(periodos="all")
ibc_br.run(start="all")

# Atualização rotineira (padrão)
pim.run()              # últimos N anos (default do script)
inflacao.run()         # últimos N meses

# Range específico
gdp.run(periodos=(2015, 2024))
caged.run(start="01/01/2020", end="31/12/2024")
```

Scripts IBGE usam `periodos=` (formatos do connector IBGE).  
Scripts BCB SGS usam `start=`/`end=` (formato `"DD/MM/YYYY"`) ou `start="all"`.  
`expectativas.run()` usa `start=` ISO (`"YYYY-MM-DD"`) ou `n_dias=` para janela retroativa.

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
- Todas as funções de scoring renomeadas para snake_case (ex: `Inflacao` → `inflacao`, `IBC_BR` → `ibc_br`)
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
uv run python jobs/update_db.py          # atualiza macro_brasil (inclui reservas, BOP, fluxo, termos)
uv run python jobs/update_international.py  # atualiza macro_international (reer, cot_fx)
uv run python jobs/update_analytics.py   # atualiza macro_analytics (diferenciais_juros)
uv run python -c "from analytics.cambio.generate_report import run; run()"
# Saída: reports/cambio_latest.html
```

### Arquitetura do relatório

Template fixo `report.html` com marcador `/*REPORT_DATA*/`. `generate_report.py` lê tabelas de três schemas, serializa como JSON e substitui o marcador. Sem Jinja2 — só `str.replace()`.

| Seção | Schema | Tabela |
|---|---|---|
| Diferenciais de Juros | `macro_analytics` | `diferenciais_juros` |
| REER | `macro_international` | `reer` |
| Posicionamento CFTC | `macro_international` | `cot_fx` |
| Fluxos e Fundamentos | `macro_brasil` | `reservas`, `termos_de_troca`, `fluxo_cambial`, `balanco_pagamentos` |

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

### Média prioridade
- **`domain/db/brasil/ibge/subcomponents.py`**: WIP — subcomponentes IPCA (IBGE 7060). Adaptar para connector v3, definir schema, implementar `run()`.
- **`analytics/oraculo/us/term_us.py` — revisão de qualidade**: snake_case, `_load_data()` centralizado, bugs de robustez.
- **US — expandir dados**: `connectors/not_in_production/bls.py`, schema `macro_us`, `domain/db/us/inflation/`.
- **macro_analytics/international — itens menores**: confirmar descrições SGS 22099/22100, sub-itens CEP/CBE fluxo cambial, diferenciais ex-ante. Ver `CAMBIO.md`.

### Baixa prioridade
- `quarantine/` — scripts legados (curva de juros, decomposição IPCA). Limpar quando conveniente.
- `brasil/thermometer.py` lê de `MySQLDataRequester('br_finance', 'brazil_real_yield_curve')` — verificar se schema ainda existe.
