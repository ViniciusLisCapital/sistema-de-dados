# Sistema de Dados — LIS Capital

Coleta, processa e pontua variáveis macroeconômicas (Brasil e EUA) para alimentar
dashboards Power BI e materiais de análise macro.

O fluxo é simples: **APIs externas → ETL → banco MySQL `macro_brasil` → notas (oráculo) → CSVs/Power BI.**

> 📚 **Documentação relacionada**
> - [`AMBIENTE.md`](AMBIENTE.md) — setup do ambiente, `uv`, dependências, troubleshooting. **Comece por aqui numa máquina nova.**
> - [`CLAUDE.md`](CLAUDE.md) — contexto detalhado: schema das tabelas, detalhes técnicos dos connectors, decisões de arquitetura e pendências.

---

## Início rápido

```powershell
# 1. Configurar o ambiente (uma vez por máquina) — detalhes em AMBIENTE.md
uv sync
uv pip install -e .
cp .env.example .env          # preencher com as credenciais reais

# 2. Atualizar o banco de dados (11 tabelas de macro_brasil)
uv run python jobs/update_db.py

# 3. Recalcular as notas do oráculo (lê o banco → CSVs)
uv run python jobs/update_oraculo.py
```

> ⚠️ **A ordem importa:** `update_oraculo` lê do banco que `update_db` alimenta.
> Rode `update_db` primeiro.

---

## Como os dados fluem

```
  connectors/            domain/db/brasil/             MySQL                  analytics/oraculo/
┌─────────────┐   run() ┌──────────────────┐  insert ┌──────────────┐  read ┌─────────────────────┐
│ IBGE  BCB   │ ──────► │ 11 scripts ETL:  │ ──────► │ macro_brasil │ ────► │ scores.py (Brasil)  │
│ FRED  MySQL │         │ fetch→transform  │         │ (11 tabelas) │       │ term_us.py (EUA)    │
└─────────────┘         └──────────────────┘         └──────────────┘       └─────────┬───────────┘
                                                                                       │ notas 1–10
                                                                                       ▼
                                                                          base/Central_base.csv → Power BI
```

**Exemplo concreto (IPCA):** `connectors/bcb.py` busca as séries SGS →
`domain/db/brasil/bcb/inflacao.py` (`run()`) grava na tabela `macro_brasil.inflacao` →
`analytics/oraculo/brasil/scores.py` lê a tabela e calcula a nota.

---

## Estrutura do projeto

| Diretório | Papel | Estado |
|---|---|---|
| **`connectors/`** | Clientes de API/banco: `ibge.py` (classe `IBGE`), `bcb.py` (`BCB`), `fred.py`, `mysql.py`. | ✅ Vivo, canônico |
| `connectors/not_in_production/` | Staging de connectors (`bls.py` é usado pelo ETL EUA; `fred.py` aqui é duplicata obsoleta). | ⚠️ Parcial |
| **`domain/db/brasil/`** | **ETL de produção.** 11 scripts em `ibge/` e `bcb/`, cada um expõe `run()` (busca → transforma → grava em `macro_brasil`). | ✅ Vivo, canônico |
| `domain/db/us/` | ETL EUA (`inflation/cpi.py`, `shelter.py`). | 🚧 Em construção |
| `domain/oraculo/` | Cópia antiga de `analytics/oraculo/`. Não é importada por nada. | ❌ Obsoleto |
| **`analytics/oraculo/`** | **Cálculo das notas** (scores) de Brasil e EUA → CSVs. Consumido por `jobs/update_oraculo.py`. | ✅ Vivo, canônico |
| `analytics/painel_setores/` | Painel de setores (script + dashboard). | 🚧 Quebrado no import |
| **`utils/`** | Helpers compartilhados: `transforms.py` (conversões de séries) e `thermometer.py` (scoring sigmóide 1–10). | ✅ Vivo |
| **`jobs/`** | **Entry points:** `update_db.py` e `update_oraculo.py`. | ✅ Vivo |
| `quarantine/` | Scripts e materiais legados/experimentais: `finance_modelo_curva_juros/` (curva de juros, pbix), `inflation_decomposition/` (decomposição IPCA, pbix), `reservoirs.py`. | ❌ Fora do ETL |
| `tests/` | Um arquivo de demonstração (`test_ibge2.py`), sem asserts. | 🚧 Sem cobertura real |

---

## Tabelas do banco `macro_brasil`

Schema e período de cada tabela em [`CLAUDE.md`](CLAUDE.md): `atv_pim`,
`atv_pib`, `atv_pmc`, `atv_pms`, `mt_pnad` (IBGE) ·
`atv_ibcbr`, `inflc_agregados`, `mt_caged`, `cred_credito_amplo`,
`expc_focus`, `cred_credito_familias` (BCB). Nomes prefixados por tema desde
2026-07, abreviados numa segunda rodada — ver [`DB_SCHEMAS.md`](DB_SCHEMAS.md).

---

## Dashboards Power BI

Os `.pbix` consomem os CSVs do oráculo e bases de análise.

| Dashboard | Localização |
|---|---|
| `PAINEL DE SETORES.pbix` | `analytics/painel_setores/docs/` |
| `Curva de Juros.pbix`, `Curva_de_Juros_old.pbix`, `Decomposition.pbix` | `quarantine/finance_modelo_curva_juros/` |
| `br_ipca_decomposition.pbix`, `br_ipca15_decomposition.pbix`, `Projeto_CriseHídrica.pbix` | `quarantine/inflation_decomposition/` |

---

## Navegação: o que é vivo vs. legado

Para evitar a confusão de versões duplicadas, este é o estado real do código:

- **O sistema que roda hoje** é pequeno: os **2 entry points** em `jobs/`, os **11 scripts ETL**
  em `domain/db/brasil/`, e o `analytics/oraculo/`. Se está mexendo no fluxo de dados, é aqui.
- **`quarantine/`** — scripts e materiais legados (curva de juros, decomposição IPCA). Os `.py`
  **não rodam** (importam pacotes inexistentes). Os `.pbix` ainda são consultados. Não use como
  referência do ETL — o equivalente vivo está em `domain/db/brasil/`.
- **Duplicatas obsoletas** (não importadas por nada): `domain/oraculo/` e
  `connectors/not_in_production/fred.py`. O canônico é `analytics/oraculo/` e `connectors/fred.py`.
- **Em construção:** o ramo EUA (`domain/db/us/`, sem tabela `macro_us` ainda) e
  `analytics/painel_setores/`.

> Pendências e plano de limpeza estão em [`CLAUDE.md`](CLAUDE.md).
