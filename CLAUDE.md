# Sistema de Dados — Contexto para o Claude

## Regras gerais

- **The text should remain in the language it already is, NO TRANSLATION.** When generating `.md` files from English-language PDFs, write in English. When generating from Portuguese-language sources, write in Portuguese.

## Sobre o Projeto

Sistema de dados da LIS Capital para coleta, processamento e visualização de variáveis macroeconômicas (Brasil, EUA). Alimenta dashboards Power BI e materiais de análise macro.

📄 **Racional estratégico e origem do projeto** (por que o vault `obsidian/` e a direção de agentes especialistas por área macro existem, fases de investimento planejadas): [`team_materials/structure_materials/macro-project-context.md`](team_materials/structure_materials/macro-project-context.md).

---

## Arquitetura atual

```
connectors/          — Clientes de APIs externas (IBGE, BCB, FRED, BIS, CFTC, MySQL,
                       Comex Stat/MDIC — comexstat.py live API + comexstat_bulk.py CSV histórico)
domain/
  db/brasil/         — ETL Brasil: fetch → transform → insert em macro_brasil
    ibge/            — Scripts por pesquisa IBGE (atv_pim, atv_pib, atv_pmc,
                       atv_pms, mt_pnad, inflc_decomposicao, inflc_dim)
    bcb/             — Scripts por tema BCB (atv_ibcbr, inflc_agregados, mt_caged,
                       cred_credito_amplo, expc_focus, cred_credito_familias, cmb_reservas_bc,
                       cmb_balanco_pagmt, cmb_fluxo_cambial, cmb_termos_troca, cmb_cambio_contratado,
                       atv_pib_usd, comm_icbr, inflc_meta — os 3 últimos alimentam o modelo BCB em
                       analytics/monetary_policy/, ver seção própria abaixo)
    mdic/            — Comex Stat: cmb_comex_pais (saldo por parceiro), cmb_comex_fator_agregado
                       (básicos/semi/manufaturados), cmb_comex_produto (soja, petróleo, minério,
                       carnes, café) — todos com run() (janela recente, API) e backfill() (1997→hoje, bulk CSV)
  db/international/  — ETL dados cross-country: fetch → insert em macro_international
    bis/             — cmb_reer (REER Brasil/MX/CL/CO via BIS API)
    cftc/            — cmb_cot_fx (posicionamento especulativo BRL/MXN)
    fred/            — diferenciais_juros (Selic × Fed Funds, real ex-post — precisa de BR+US),
                       comm_brent (Brent diário, FRED DCOILBRENTEU — insumo de choque de commodities do
                       modelo BCB; ainda não integrado a jobs/update_international.py)
    noaa/            — clima_oni (Oceanic Niño Index, texto NOAA CPC — insumo climático da Curva de
                       Phillips do modelo BCB; ainda não integrado a jobs/update_international.py)
analytics/           — Projetos que consomem o banco MySQL
  oraculo/           — Termômetro macro (brasil e us)
  painel_setores/    — Painel de setores
  exchange_rate/     — Panorama Cambial HTML  [ver analytics/exchange_rate/CLAUDE.md]
    generate_report.py  — Lê macro_brasil/macro_international, injeta JSON no template, salva HTML
    report.html         — Template fixo (HTML + CSS + Plotly.js CDN)
    referencia/          — Material de contexto (mapeamento SGS, peças analíticas sobre forecasting
                           cambial) — ver analytics/exchange_rate/CLAUDE.md
    models/              — Modelos estatísticos testando teoria cambial contra o banco — ver
                           analytics/exchange_rate/CLAUDE.md
  inflation/         — Panorama de Inflação HTML  [ver analytics/inflation/CLAUDE.md]
    fetch_bcb.py         — Agregados BCB/SGS (IPCA headline/componentes/núcleos) → data/ipca_bcb_series.csv (+ STL _ma3_sa)
    generate_report.py   — Lê Excel (subitens) + CSV (agregados), injeta JSON no template, salva HTML
    report.html           — Template fixo (HTML + CSS + Plotly.js CDN)
    data/                 — Excel (decomposição por subitem, fora do MySQL) + CSV (agregados BCB)
  monetary_policy/   — Replicação do modelo pequeno do BCB (Selic/Phillips/Taylor)  [ver seção própria abaixo]
    model.py             — Motor de simulação (5 equações, recursão a partir do estado inicial lido do MySQL)
    generate_report.py   — Mesmo padrão /*REPORT_DATA*/ de exchange_rate/inflation
    report.html           — Template fixo, abas "Cenários" e "Sobre o Modelo"
    referencia/           — PDFs do modelo original do BCB + MODEL_REPLICATION_PLAN.md (histórico da réplica)
jobs/                — Entry points
  update_db.py          — Atualiza todas as tabelas de macro_brasil (inclui mdic/ e atv_pib_usd; NÃO inclui
                          ainda comm_icbr/inflc_meta — rodar manualmente por enquanto)
  update_international.py — Atualiza macro_international (cmb_reer, cmb_cot_fx, diferenciais_juros; NÃO
                          inclui ainda comm_brent/clima_oni — rodar manualmente por enquanto)
  update_oraculo.py     — Atualiza o oráculo
reports/             — Outputs gerados (não versionados)
  fx_report.html — Relatório cambial mais recente (autocontido, enviável; renomeado de cambio_latest.html em 2026-07)
  bcb_model.html — Relatório do modelo BCB replicado (renomeado de monetary_policy_latest.html)
utils/               — Funções auxiliares compartilhadas
quarantine/          — Scripts e materiais legados/experimentais (não fazem parte do ETL)
```


---

## Banco de dados: macro_brasil / macro_international

📄 **Organização de schemas, convenção de nomes, tabelas ativas, padrões de chave primária:** [`domain/db/CLAUDE.md`](domain/db/CLAUDE.md) — carrega sob demanda quando o Claude lê arquivos dentro de `domain/db/`.

---

## Connectors

📄 **Documentação completa (API IBGE v3, SGS/Focus do BCB, FRED, MySQL insert/update):** [`connectors/CLAUDE.md`](connectors/CLAUDE.md) — carrega sob demanda quando o Claude lê arquivos dentro de `connectors/`.

---

## analytics/oraculo/ — Termômetro Macro

Calcula "notas" (scores 1–10) para variáveis macroeconômicas de Brasil e EUA, alimentando dashboards Power BI.

📄 **Componentes, fluxo de execução, padrão de `scores.py`:** [`analytics/oraculo/CLAUDE.md`](analytics/oraculo/CLAUDE.md) — carrega sob demanda quando o Claude lê arquivos dentro de `analytics/oraculo/`.

---

## analytics/exchange_rate/ — Panorama Cambial

Relatório HTML interativo de fundamentos cambiais. Arquivo único autocontido — abre em qualquer browser, enviável por email/Dropbox.

📄 **Como gerar, arquitetura do relatório, mapeamento seção→schema→tabela, gotchas atuais, pendências:** [`analytics/exchange_rate/CLAUDE.md`](analytics/exchange_rate/CLAUDE.md) — carrega sob demanda quando o Claude lê arquivos dentro de `analytics/exchange_rate/`.

---

## analytics/inflation/ — Panorama de Inflação

Relatório HTML de decomposição do IPCA/IPCA-15. Decomposição por subitem vive em `macro_brasil` (`inflc_decomposicao` + `inflc_dim`); agregados BCB/SGS vêm de um CSV separado (`ipca_bcb_series.csv`, via `fetch_bcb.py`).

📄 **Como gerar, arquitetura, mapa de dados, gotchas atuais, pendências:** [`analytics/inflation/CLAUDE.md`](analytics/inflation/CLAUDE.md) — carrega sob demanda quando o Claude lê arquivos dentro de `analytics/inflation/`.

---

## analytics/monetary_policy/ — Replicação do Modelo Pequeno do BCB

Motor de simulação que replica o modelo agregado pequeno do BCB (Curva de Phillips para livres, curva IS, regra de Taylor, UIP, termos climático/commodities) como recursão para frente a partir de um estado inicial lido do MySQL, mais o mesmo relatório HTML autocontido (`/*REPORT_DATA*/`) usado por `analytics/exchange_rate/` e `analytics/inflation/`.

📄 **Histórico completo da réplica, decisões de escopo e validação:** [`analytics/monetary_policy/referencia/MODEL_REPLICATION_PLAN.md`](analytics/monetary_policy/referencia/MODEL_REPLICATION_PLAN.md)

### Como gerar

```powershell
uv run python -c "from analytics.monetary_policy.generate_report import run; run()"
# Saída: reports/bcb_model.html
```

**Pontos-chave:**
- `model.py` implementa as 5 equações do modelo original como `load_history()` / `simulate(n_quarters, scenario)` / `decompose_last_quarter()`, lendo parâmetros/seed/histórico do MySQL.
- **Lacuna de calibração conhecida:** o choque de IRF replicado (Selic +1pp por 4 trimestres) bate em sinal/timing com o resultado publicado pelo BCB, mas a magnitude fica **~4-5x maior** (pico ~-1.5pp no trimestre 9 vs. -0.33pp esperado no trimestre 6). Causa raiz: o motor aproxima a trajetória futura esperada da Selic pela taxa atual/simulada (sem curva forward), então não desconta a antecipação de reversão do choque — consequência direta de pular a equação 5 (expectativas de inflação model-consistent), decisão de escopo deliberada. Esse aviso aparece no próprio relatório, não só na documentação. **Tratar as magnitudes como direcionalmente úteis, não precisas**, até essa lacuna ser revisitada.
- Alimentado por três séries BCB SGS novas (`atv_pib_usd`, `comm_icbr`, `inflc_meta` — ver tabela em "Banco de dados: macro_brasil" acima) mais duas séries internacionais ainda não integradas aos jobs de rotina: `comm_brent` (Brent diário, FRED) e `clima_oni` (Oceanic Niño Index, NOAA).
- `report.html` tem duas abas: **Cenários** (baseline + choque de Selic) e **Sobre o Modelo** (introdução para leigos: diagrama de fluxo, um card por equação, glossário, tabela de fontes de dados).
- `referencia/` guarda os PDFs do modelo original do BCB (`atualizacao_modelos.pdf`, `modelo_agregado.pdf`, `modelo_desagregado.pdf`) que fundamentam a réplica — mesma convenção `data/` vs. `referencia/` usada em `analytics/inflation/`.

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

Since 2026-07, organized by topic area (exchange rate, monetary policy, trader, and future ones: economic activity, fiscal policy, inflation, labor market), each with a literature → data → conceptual map pipeline. Named `agent_bibliography/` before — old name still turns up in git history/older docs, treat as a synonym. Doesn't use or reconcile with `obsidian/`, nor interact with the `ingestion/` pipeline — deliberately parallel systems, per explicit user instruction.

📄 **Folder structure, methodology, per-topic status, and pending items:** [`repository/CLAUDE.md`](repository/CLAUDE.md) — loads on demand when Claude reads files inside `repository/` (unlike this root file, which loads in full every session).

**Three branches of exchange-rate material (2026-07):**
1. **Curation** (`repository/exchange_rate/` + `repository/agent_mapping/*`) — literature → conceptual map pipeline. Not team-facing, it's the base that feeds the agent. Full detail in `repository/CLAUDE.md`.
2. **Consolidated** (`team_materials/agent_materials/exchange_rate/`) — condensed, presentable synthesis for team discussion (bibliography, conceptual map, data inventory, EN/PT introduction, two interactive HTML explorers).
3. **Analytical** (`analytics/exchange_rate/`) — applied/analytical branch, same pattern as `analytics/monetary_policy/` and `analytics/inflation/` (code + HTML report + `referencia/`). See its own section above.

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

### Alta prioridade
- **`analytics/exchange_rate/`**: ver "Pending" em [`analytics/exchange_rate/CLAUDE.md`](analytics/exchange_rate/CLAUDE.md).
- **`analytics/inflation/`**: ver "Pending" em [`analytics/inflation/CLAUDE.md`](analytics/inflation/CLAUDE.md).

### Média prioridade
- **US — expandir dados**: `connectors/not_in_production/bls.py`, schema `macro_us`, `domain/db/us/inflation/`.
- **`repository/` — curation pending items** (conceptual maps, bibliography gaps, trader scope): see "Pending" section in [`repository/CLAUDE.md`](repository/CLAUDE.md).
- **Jobs de rotina incompletos**: `comm_icbr.py`/`inflc_meta.py` (novos, `domain/db/brasil/bcb/`) não estão em `jobs/update_db.py`; `comm_brent.py`/`clima_oni.py` (novos, `domain/db/international/`) não estão em `jobs/update_international.py`. Todos os quatro já alimentam `analytics/monetary_policy/model.py` mas precisam ser rodados manualmente até serem integrados.
- **`team_materials/agent_materials/exchange_rate/` — notas desatualizadas**: `data_inventory.md` ainda diz que o `conceptual_map.md` "não foi construído" (já foi); `introduction_pt.md` não lista o `conceptual_map.md` entre os documentos da pasta. Nenhum dos dois foi corrigido ainda.
- **Kinea PDF órfão**: `team_materials/agent_materials/exchange_rate/kinea_fx_mental_models.pdf` existe mas não há `.md` de origem em lugar nenhum, e `bibliography.md` ainda marca Kinea como "pendente" — investigar se é um artefato de teste esquecido ou uma síntese real nunca finalizada (fonte bruta: `repository/mental_model/kinea_insights/`).

### Baixa prioridade
- `quarantine/` — scripts legados (curva de juros, decomposição IPCA). Limpar quando conveniente.
