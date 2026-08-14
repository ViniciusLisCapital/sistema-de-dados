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
                       Comex Stat/MDIC — comexstat.py live API + comexstat_bulk.py CSV histórico,
                       Tesouro Nacional — tesouro.py, RTN via CKAN,
                       PDET/MTE — pdet_ftp.py, microdados do Novo CAGED via FTP, encoding
                       Latin-1 nos nomes de arquivo, ver connectors/CLAUDE.md)
domain/
  db/brasil/         — ETL Brasil: fetch → transform → insert em macro_brasil
    ibge/            — Scripts por pesquisa IBGE (atv_pim, atv_pim_uso — categoria de uso, perspectiva
                       complementar ao atv_pim por seção/atividade —, atv_pib, atv_pmc,
                       atv_pms, mt_pnad, inflc_decomposicao, inflc_decomposicao_item,
                       inflc_dim)
    bcb/             — Scripts por tema BCB (atv_ibcbr, inflc_agregados, mt_caged,
                       cred_credito_amplo, cred_credito_resumo — resumo por recurso [livre/
                       direcionado/total] x segmento [pj/pf/total], 84 séries (72 + 12 do corte
                       "crédito não rotativo" da Tabela 14), códigos SGS extraídos da planilha
                       mensal do BCB "Tabelas de Estatísticas Monetárias e de Crédito"
                       (Tabelas 3-5, 14) —, cred_modalidade_livre_pj/livre_pf/direcionado_pj/
                       direcionado_pf — saldo/concessão/taxa média/inadimplência por modalidade
                       específica de crédito (Tabelas 6-13, 15-22) —, cred_credito_porte/
                       atividade_economica/tipo_cliente/controle_capital — cortes estruturais
                       (Tabelas 23-26) —, expc_focus, cred_credito_familias,
                       cmb_reservas_bc, cmb_balanco_pagmt, cmb_fluxo_cambial, cmb_termos_troca,
                       cmb_cambio_contratado, atv_pib_usd, comm_icbr, inflc_meta — os 3 últimos
                       alimentam o modelo BCB em analytics/monetary_policy/, ver seção própria
                       abaixo — fisc_divida, fisc_nfsp, cred_inadimplencia_pj — Selic + proxies
                       de estresse de crédito PJ, alimenta analytics/credit/, ver seção própria
                       abaixo —, cred_ptc — Pesquisa Trimestral de Condições de Crédito, 16 séries,
                       percepção dos bancos sobre oferta/demanda de crédito por segmento, equivalente
                       ao Senior Loan Officer Opinion Survey do Fed)
    tesouro/         — fisc_rtn (RTN, Resultado do Tesouro Nacional — receita/despesa/resultado do
                       Governo Central por rubrica orçamentária), fisc_efgg (EFGG, Estatísticas
                       Fiscais do Governo Geral — classificação econômica GFSM 2014, por esfera
                       Central/Estados/Municípios + geral, fonte da IEG) — alimentam
                       analytics/fiscal_policy/, ver seção própria abaixo
    mdic/            — Comex Stat: cmb_comex_pais (saldo por parceiro), cmb_comex_fator_agregado
                       (básicos/semi/manufaturados), cmb_comex_produto (soja, petróleo, minério,
                       carnes, café) — todos com run() (janela recente, API) e backfill() (1997→hoje, bulk CSV)
    mte/             — Novo CAGED via microdado do FTP do PDET (2020-01→hoje): saldo/admissões/
                       desligamentos em 3 cortes independentes — mt_caged_setor (seção CNAE),
                       mt_caged_uf, mt_caged_salario (faixas em múltiplos de SM). Rodar via
                       mt_caged_novo.py, o orquestrador que baixa cada release UMA vez e alimenta
                       as 3 tabelas no mesmo passe (~50MB/mês; ~4GB para start="all"). Lógica
                       MOV+FOR-EXC por competência de movimentação em _caged_core.py — leitura
                       obrigatória antes de mexer, a revisão retroativa é sutil.
  db/international/  — ETL dados cross-country: fetch → insert em macro_international
    bis/             — cmb_reer (REER Brasil/MX/CL/CO via BIS API), cmb_policy_rates (taxa de juros de
                       politica monetaria, BIS WS_CBPOL, diária, BR/MX/CL/CO/PE/AR — AR parou de ser
                       atualizada pelo BIS em 2025-07; ainda não integrado a jobs/update_international.py),
                       cmb_real_rates (taxa real ex-post = policy rate − CPI YoY, BIS WS_CBPOL + WS_LONG_CPI,
                       mensal, BR/MX/CL/CO/PE — cada país começa no início da própria série de policy rate
                       do BIS, o fator limitante; BR truncado em 1994-07 como cmb_policy_rates; recalcula BR
                       com fonte BIS para comparabilidade cross-country, não substitui o real_br_ex_post de
                       diferenciais_juros — ainda não integrado a jobs/update_international.py)
    cftc/            — cmb_cot_fx (posicionamento especulativo BRL/MXN)
    fred/            — diferenciais_juros (Selic × Fed Funds, real ex-post — precisa de BR+US),
                       comm_brent (Brent diário, FRED DCOILBRENTEU — insumo de choque de commodities do
                       modelo BCB; ainda não integrado a jobs/update_international.py), cmb_dollar_index_em
                       (Índice do dólar x moedas EM, FRED DTWEXEMEGS, diário desde 2006-01-02 — ainda não
                       integrado a jobs/update_international.py)
    noaa/            — clima_oni (Oceanic Niño Index, texto NOAA CPC — insumo climático da Curva de
                       Phillips do modelo BCB; ainda não integrado a jobs/update_international.py)
    yfinance/        — cmb_dollar_index (DXY, Yahoo Finance DX-Y.NYB — ICE US Dollar Index, diário desde
                       1971-01-04; preferido ao FRED DTWEXBGS, que só cobre a partir de 2006 — ainda não
                       integrado a jobs/update_international.py), cmb_fx_latam (câmbio diário MX/CL/CO/PE
                       vs. USD, Yahoo Finance MXN=X/CLP=X/COP=X/PEN=X — insumo de volatilidade cambial para
                       o métrico carry/vol de analytics/exchange_rate/models/ppp_equilibrium.py; ainda não
                       integrado a jobs/update_international.py)
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
    models/               — Material legado de curva de juros (ex-quarantine/, 2026-08), ainda não integrado
                           ao motor principal — ver "Pendências" abaixo
  economic_activity/ — Panorama de Atividade Econômica HTML (PIB/PIM/PMC/PMS/IBC-Br)  [ver
                       analytics/economic_activity/CLAUDE.md]
    generate_report.py   — Lê atv_pib/atv_pib_valores_correntes/atv_pib_taxas/atv_pim/atv_pmc/atv_pms/
                           atv_ibcbr de macro_brasil, injeta JSON no template, salva HTML — sem
                           CSV/Excel local, tudo já está no MySQL
    report.html           — Template fixo (HTML + CSS + Plotly.js CDN), 6 abas
  fiscal_policy/     — Panorama Fiscal HTML (dívida pública, NFSP, RTN)  [ver
                       analytics/fiscal_policy/CLAUDE.md]
    generate_report.py   — Lê fisc_divida/fisc_nfsp/fisc_rtn de macro_brasil, injeta JSON no
                           template, salva HTML — sem CSV/Excel local, tudo já está no MySQL
    report.html           — Template fixo (HTML + CSS + Plotly.js CDN), 4 abas
  credit/            — Panorama de Crédito HTML (novo, substitui credit_stress/ — 2026-08)  [ver
                       analytics/credit/CLAUDE.md]
    generate_report.py   — Lê cred_credito_amplo/cred_credito_resumo/cred_credito_familias/
                           cred_inadimplencia_pj de macro_brasil, injeta JSON no template, salva HTML
                           — sem CSV/Excel local no pipeline de atualização (a planilha do BCB em
                           analytics/credit/ foi usada só para mapear códigos SGS, não é lida em
                           runtime)
    report.html           — Template fixo (HTML + CSS + Plotly.js CDN); em reconstrucao aba por aba
                           desde 2026-08 (usuario apagou as 4 abas de dados do v1, so Apendice
                           sobreviveu) — hoje tem Saldo (com 2a tabela para Credito Ampliado, mais
                           grupos por porte/atividade economica/tipo cliente) + Concessao (ambas
                           tabela-hierarquica-grafico via a fabrica JS makeHierTab(), reusada entre as
                           duas, com toggle Nominal/Real/% PIB) + Concessao + Taxa & Spread (formato
                           bespoke, sem makeHierTab, com overlay de Selic) + Inadimplencia (mesmo
                           formato bespoke de Taxa & Spread, reune inadimplencia de todos os cortes que
                           a publicam, mais Saldo de Maior Risco em 2 grupos por metodologia -- Res.
                           2.682 vs. Res. 4.966, quebra confirmada ao vivo, nunca emendadas) + Apendice,
                           ver analytics/credit/CLAUDE.md
  report_structure/  — Scaffolding compartilhado de build-time para os relatórios acima (theme CSS,
                       _bindYAutofit, harness de substituição /*REPORT_DATA*/) — ver analytics/CLAUDE.md
                       e analytics/report_structure/CLAUDE.md. Piloto: inflation/ (2026-08, migração completa);
                       exchange_rate/ parcialmente migrado (JS/harness, falta o CSS — precisa do reskin 2026-07
                       antes); monetary_policy/ ainda não migrado; economic_activity/ (2026-08) já nasceu
                       construído sobre os dois marcadores, sem precisar de migração.
jobs/                — Entry points
  update_db.py          — Atualiza todas as tabelas de macro_brasil (inclui mdic/, atv_pib_usd e o
                          Novo CAGED via mte/mt_caged_novo — este último baixa ~50MB do FTP e leva
                          minutos, não segundos, por isso fica no fim da lista; NÃO inclui ainda
                          comm_icbr/inflc_meta — rodar manualmente por enquanto)
  update_international.py — Atualiza macro_international (cmb_reer, cmb_cot_fx, diferenciais_juros; NÃO
                          inclui ainda comm_brent/clima_oni — rodar manualmente por enquanto)
  update_oraculo.py     — Atualiza o oráculo
reports/             — Outputs gerados (não versionados)
  fx_report.html — Relatório cambial mais recente (autocontido, enviável; renomeado de cambio_latest.html em 2026-07)
  bcb_model.html — Relatório do modelo BCB replicado (renomeado de monetary_policy_latest.html)
utils/               — Funções auxiliares compartilhadas
```


---

## Banco de dados: macro_brasil / macro_international

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

Since 2026-07, organized by topic area (exchange rate, monetary policy, trader, and future ones: economic activity, fiscal policy, inflation, labor market), each with a literature → data → conceptual map pipeline. Named `agent_bibliography/` before — old name still turns up in git history/older docs, treat as a synonym. Doesn't use or reconcile with `obsidian/`'s own concept/synthesis pages — deliberately parallel systems, per explicit user instruction. Does interact with `repository/ingestion/` (2026-08) — that's the PDF ingestion pipeline itself, living inside this tree: drop a PDF in `repository/ingestion/land_space/<topic>/`, run `repository/ingestion/scripts/run.py`, and it populates `raw_pdf/`/`raw_md/`/`clean_md/` in one command.

📄 **Folder structure, methodology, per-topic status, and pending items:** [`repository/CLAUDE.md`](repository/CLAUDE.md) — loads on demand when Claude reads files inside `repository/` (unlike this root file, which loads in full every session).

**Three branches of exchange-rate material (2026-07):**
1. **Curation** (`repository/exchange_rate/` + `repository/agent_mapping/*`) — literature → conceptual map pipeline. Not team-facing, it's the base that feeds the agent. Full detail in `repository/CLAUDE.md`.
2. **Consolidated** (`team_materials/agent_materials/exchange_rate/`) — condensed, presentable synthesis for team discussion (bibliography, conceptual map, data inventory, EN/PT introduction, two interactive HTML explorers).
3. **Analytical** (`analytics/exchange_rate/`) — applied/analytical branch, same pattern as `analytics/monetary_policy/` and `analytics/inflation/` (code + HTML report + `referencia/`). See its own section above.

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
- **`analytics/exchange_rate/`**: ver "Pending" em [`analytics/exchange_rate/CLAUDE.md`](analytics/exchange_rate/CLAUDE.md).
- **`analytics/inflation/`**: ver "Pending" em [`analytics/inflation/CLAUDE.md`](analytics/inflation/CLAUDE.md).
- **`analytics/economic_activity/`**: 6 abas (PIB, Produção Industrial, Comércio, Serviços, IBC-Br,
  Apêndice), framework interativo comum às 5 abas de dados (multiselect, toggle Y/Y↔acumulado, momentum
  scatter/heatmap); só a aba PIB tem decomposição de crescimento (as outras 4 não têm tabela de
  peso nominal/taxa oficial). Ver "Pending" em
  [`analytics/economic_activity/CLAUDE.md`](analytics/economic_activity/CLAUDE.md) — falta principalmente
  confirmar visualmente num browser real (sandbox sem browser disponível).
- **`analytics/fiscal_policy/`**: 3 abas (Receitas e Despesas GFSM — aba padrão, com seletor de Esfera
  União/Estados/Municípios/Geral —, Impulso Fiscal/IEG, Apêndice). As 3 abas antigas (Visão Geral/Dívida
  Pública/Resultado Fiscal) foram apagadas a pedido do usuário para reconstrução tab-a-tab, ainda não
  retomada. Ver "Pending" em [`analytics/fiscal_policy/CLAUDE.md`](analytics/fiscal_policy/CLAUDE.md)
  (inclui o double-count de transferências intergovernamentais no total Governo Geral, re-estimação dos
  multiplicadores do IEG, e o bloqueio do MEFA).
- **`analytics/credit/`**: substituiu `analytics/credit_stress/` (removida junto com a tabela
  `insolv_falencia_rj` e `connectors/datajud.py` a pedido do usuário — histórico só em git log). Hoje
  tem Saldo (+ 2ª tabela para Crédito Ampliado), Concessão (ambas via a fábrica JS `makeHierTab()`,
  toggle Nominal/Real/% PIB), Taxa & Spread e Inadimplência (formato bespoke, com overlay de Selic), +
  Apêndice. Ver "Pending" em [`analytics/credit/CLAUDE.md`](analytics/credit/CLAUDE.md) (confirmação em
  browser real, `cred_credito_controle_capital.saldo`/`provisoes` ainda não charteados, `cred_ptc` ainda
  não charteada em nenhuma aba).

### Média prioridade
- **Mercado de trabalho — pendências pós-Novo CAGED** (o conector do FTP e as 3 tabelas de corte
  ficaram prontos em 2026-08, ver `domain/db/brasil/mte/` e `analytics/labor_market/fontes_dados.md`):
  (a) `domain/db/brasil/bcb/mt_caged.py` continua rotulando **estoque** como "saldo" — corrigir a
  rotulagem (pendência antiga, agora mais visível porque o saldo real existe em tabela própria);
  (b) cortes do microdado ainda não modelados: município, ocupação (CBO), sexo/idade/instrução/raça
  — todos disponíveis no mesmo microdado já baixado, adicionar é só uma tabela irmã nova com o
  mesmo padrão (`categoria`/`metrica`), sem migração;
  (c) `mt_pnad_trimestral`: nível UF/N3 deixado de fora deliberadamente, sem previsão;
  (d) nenhum relatório/dashboard consome as 3 tabelas novas ainda — não existe
  `analytics/labor_market/` como projeto de relatório, só o `fontes_dados.md`.
- **US — expandir dados**: `connectors/not_in_production/bls.py`, schema `macro_us`, `domain/db/us/inflation/`.
- **`repository/` — curation pending items** (conceptual maps, bibliography gaps, trader scope): ver "Pending" em [`repository/CLAUDE.md`](repository/CLAUDE.md).
- **Jobs de rotina incompletos**: `comm_icbr.py`/`inflc_meta.py` (`domain/db/brasil/bcb/`) não estão em `jobs/update_db.py`; `comm_brent.py`/`clima_oni.py`/`cmb_dollar_index.py`/`cmb_dollar_index_em.py`/`cmb_policy_rates.py`/`cmb_fx_latam.py`/`cmb_real_rates.py` (`domain/db/international/`) não estão em `jobs/update_international.py`. Os quatro primeiros já alimentam `analytics/monetary_policy/model.py`; `cmb_dollar_index`/`cmb_dollar_index_em`/`cmb_policy_rates`/`cmb_real_rates` ainda não são consumidos por nenhum relatório/modelo. `inflc_decomposicao_item.py` (`domain/db/brasil/ibge/`) também não está em `jobs/update_db.py` — alimenta os núcleos MA/MS/DP do IPCA-15. Todos precisam ser rodados manualmente até serem integrados.
- **`team_materials/agent_materials/exchange_rate/` — notas desatualizadas**: `data_inventory.md` ainda diz que o `conceptual_map.md` "não foi construído" (já foi); `introduction_pt.md` não lista o `conceptual_map.md` entre os documentos da pasta.
- **Kinea PDF órfão**: `team_materials/agent_materials/exchange_rate/kinea_fx_mental_models.pdf` existe mas não há `.md` de origem em lugar nenhum, e `bibliography.md` ainda marca Kinea como "pendente" — investigar se é um artefato de teste esquecido ou uma síntese real nunca finalizada (fonte bruta: `repository/mental_model/kinea_insights/`).
- **`analytics/monetary_policy/models/curva_juros/`**: material legado de curva de juros (`yield_curve.py`, `yield_curve_model.py`, planilhas DI/títulos/governo), movido de `quarantine/` em 2026-08. Ainda não integrado ao motor principal (`model.py`) — revisitar quando essa frente for retomada.

### Baixa prioridade
- (nenhuma pendência no momento)
