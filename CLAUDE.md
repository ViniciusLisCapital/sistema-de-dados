# Sistema de Dados — Contexto para o Claude

## Regras gerais

- **The text should remain in the language it already is, NO TRANSLATION.** When generating `.md` files from English-language PDFs, write in English. When generating from Portuguese-language sources, write in Portuguese.
- **Este arquivo é um índice, e é o único que carrega em toda sessão.** Ele guarda o mapa e o que vale para o repositório inteiro; nada mais. Detalhe de área vive no `CLAUDE.md` da pasta, que carrega sob demanda quando o Claude lê um arquivo de lá; histórico rodada-a-rodada vive no git log. **Ao documentar algo novo, escreva na pasta** — uma linha aqui só se a informação for transversal.

## Sobre o Projeto

Sistema de dados da LIS Capital para coleta, processamento e visualização de variáveis
macroeconômicas (Brasil, EUA). Alimenta dashboards Power BI e materiais de análise macro.

📄 **Racional estratégico e origem do projeto** (por que o vault `obsidian/` e a direção de agentes
especialistas por área macro existem, fases de investimento planejadas):
[`team_materials/structure_materials/macro-project-context.md`](team_materials/structure_materials/macro-project-context.md).

---

## Onde está cada coisa

```
connectors/          — Clientes de APIs/fontes externas (22 módulos): IBGE, BCB (SGS + Focus/Olinda,
                       agenda ICS, tabelas especiais, anexo do RPM, comunicados do Copom), FRED, BIS,
                       BLS, BEA, agendas de divulgação BLS/BEA, CFTC, IPEA, B3, Comex Stat/MDIC,
                       Tesouro (RTN/Séries Temporais/EFGG), PDET/MTE, Yahoo Finance, MySQL
                       ↳ assinatura, gotchas e limites de cada um: connectors/CLAUDE.md
domain/
  db/                — ETL: fetch → transform → insert. Uma pasta por schema e, dentro, uma por FONTE:
                       brasil/{ibge,bcb,b3,tesouro,mdic,mte,ipea,bloomberg,investing},
                       international/{bis,cftc,fred,noaa,yfinance}, us/{inflation,labor_market,rates}.
                       Um script por tabela, todos com a mesma interface run()
    registry.py      — tabela → script, derivado da convenção `_TABLE` (86 tabelas; valida em vez de
                       envelhecer em silêncio). É o que faz --group/--tables/--continuous funcionarem
                       ↳ tabelas ativas, fonte, range, chave primária e gotchas: domain/db/CLAUDE.md
  dashboards/        — O lado do CONSUMO: manifest.yaml declara de que cada dashboard depende, e
                       status.py resolve o estado ao vivo de cada dependência
                       ↳ domain/dashboards/CLAUDE.md
  release_calendar/  — Config estática de QUANDO cada dado é divulgado + sync.py (o dado chegou quando
                       devia?) + update_calendar.py / update_us_calendar.py. Nada escreve no MySQL
                       ↳ domain/release_calendar/CLAUDE.md · virada de ano: ROLLOVER.md
analytics/           — Projetos que consomem o banco. Layout país > área desde 2026-08: módulo que lê
                       o schema de um país só vive em brasil/ ou us/; infra de apresentação e
                       cross-country fica na raiz
  report_structure/  — Scaffolding de build-time compartilhado: theme.css, y_autofit.js,
                       tree_helpers.py, builder.py (`render_report()`, que injeta /*REPORT_DATA*/)
  mds/               — Decisões metodológicas transversais, uma por arquivo: metric_layers.md (o que
                       ESTE repo decidiu por camada — a taxonomia mora na skill lis-dashboard) e
                       seasonal_adjustment.md (STL × X-13, quem usa qual). Só texto, nada executa
  release_calendar/  — Relatório HTML do calendário + serve.py, o modo servido em que os botões rodam
                       o ETL e regeram dashboards. Na raiz porque monitora o sistema inteiro
  oraculo/           — Termômetro macro: notas 1–10 por variável (Brasil e EUA) → Power BI
  brasil/ · us/      — Um diretório por área, cada um = generate_report.py + report.html (+ um módulo
                       por aba) + o seu próprio CLAUDE.md. Ver a tabela de relatórios abaixo.
                       A área que teve levantamento de fontes guarda o `fontes_dados.md` dela aqui
                       (3 no brasil/, 8 no us/ — o us/ tem as 8 porque foi levantado de uma vez,
                       antes de construir; 6 dessas pastas ainda são só o levantamento)
                       ↳ padrões compartilhados e a regra de corte país/raiz: analytics/CLAUDE.md
                       ↳ acesso por fonte, chaves de API e as 377 séries FRED conferidas: analytics/us/CLAUDE.md
Linear_algebra/      — Fora do sistema de dados: ferramenta de ESTUDO da geometria da regressão
                       (`regression_geometry.html`, autocontida, não lê o banco e não está no
                       manifesto). Mínimos quadrados como projeção ortogonal, em ℝ² e ℝ³, com os
                       vetores editáveis ↳ Linear_algebra/CLAUDE.md
jobs/                — Entry points: update_db.py (macro_brasil), update_us.py, update_international.py,
                       update_oraculo.py e atualizar_diario.py (o que a tarefa agendada chama).
                       Os dois .bat de dois cliques moraram na raiz ate 2026-09-10 e vivem aqui:
                       abrir_calendario.bat e atualizar_diario.bat (ambos sobem um nivel e rodam
                       da raiz; a tarefa agendada nao passa por eles)
                       ↳ recortes, a tarefa agendada e as armadilhas dela: jobs/CLAUDE.md
reports/             — Outputs gerados, não versionados, autocontidos e enviáveis. Espelha o país >
                       área de analytics/ (reports/brasil/, reports/us/) — sem isso o Inflation.html
                       do Brasil colidiria com o dos EUA. Nomes em Title Case com espaço
repository/          — Base de conhecimento curada: fontes brutas por área, os mapas derivados delas
                       (bibliografia, inventário de dados, mapa conceitual) em agent_mapping/, e o
                       pipeline de ingestão de PDFs (`repository/ingestion/`) ↳ repository/CLAUDE.md
obsidian/            — Vault de conhecimento macro por área, para leitura humana. Deliberadamente
                       paralelo ao repository/, por instrução explícita do usuário ↳ obsidian/CLAUDE.md
team_materials/      — Só o que é MOSTRADO: PDFs, painéis HTML interativos, vídeos, diagramas e as
                       introduções narrativas. Lista, inventário e mapa vivem no repository/, qualquer
                       que seja a voz em que foram escritos — foi por essa regra que as 3 .md de base
                       de câmbio saíram daqui em 2026-09-10. Material DE área aninha por área
                       (<área>/agent_materials/); o que é do projeto inteiro fica em
                       structure_materials/, no primeiro nível ↳ team_materials/CLAUDE.md
utils/               — Funções auxiliares compartilhadas, mais o caminho curto entre uma tabela do
                       MySQL e um gráfico durante a construção de um modelo (`explore.py` +
                       `analise_template.py`, célula `#%%` no VS Code — não é relatório)
                       ↳ utils/CLAUDE.md
tests/               — Testes pontuais (pytest + harness .js), cada um nascido de um bug específico —
                       não é suíte de cobertura
```

---

## As quatro camadas declarativas

Todas declarativas, cada uma respondendo uma pergunta, e é a combinação delas que faz o sistema ter
**dois botões e só dois** — *atualizar os dados na base* e *regerar o dashboard*.

| pergunta | onde | como |
|---|---|---|
| QUANDO cada dado sai | `domain/release_calendar/calendar_2026.yaml` | 30 grupos de divulgação |
| QUEM ESCREVE cada tabela | `domain/db/registry.py` | derivado da convenção `_TABLE`, 86 tabelas |
| QUEM LÊ cada tabela | `domain/dashboards/manifest.yaml` | 12 dashboards, 138 dependências |
| QUEM RECALCULA cada ARTEFATO | `manifest.yaml`, bloco `procedures:` | 1 dashboard, 3 passos |

A quarta existe porque **um artefato calculado tem duas datas e só uma era observável**: quando foi
escrito (mtime) e com que conjunto de informação. Dos 12 dashboards só um tem passo a declarar — os
outros onze leem o banco e calculam durante a geração, então a resposta honesta para eles é não ter
bloco nenhum.

**E quanto menos passos, melhor: um passo é dívida, não recurso.** A inflação teve um até
2026-09-11 e o que ele fazia era buscar no SGS uma cópia de `inflc_agregados`, tabela que o
`update_db.py` já mantinha em dia. Um insumo que só o Regerar alcança é um insumo que o Atualizar
não alcança, e o veredito que decide se aquele passo roda é mais uma coisa que pode estar errada —
naquele caso estava, e o relatório publicou núcleo e difusão de um mês atrás com a tela verde. Antes
de declarar um passo novo, a pergunta é se aquilo não deveria ser uma tabela: se a resposta for sim,
o passo certo é não existir. Os três que restam são estimação de modelo, que é cálculo de verdade e
não tem tabela que o substitua.

O relatório de calendário tem duas abas que dividem o trabalho como a atualização acontece de
verdade: **Divulgações** atualiza o dado que saiu, **Status dashboard** reconstrói o relatório que o
consome. As duas não se encadeiam — são duas ações. Na linha de comando, sim: terminado o ETL,
`update_db.py` regera os dashboards que leem as tabelas que acabou de escrever, e só os que ficaram
para trás.

↳ mecanismo, os 5 tipos de dependência, o stamp, `procedures`, os botões de lote e o custo medido de
cada geração: [`domain/dashboards/CLAUDE.md`](domain/dashboards/CLAUDE.md) e
[`analytics/release_calendar/CLAUDE.md`](analytics/release_calendar/CLAUDE.md).

**O que nenhum botão resolve** são duas coisas, as duas decisão humana e não lacuna de encanamento:
as 3 planilhas de atribuição cambial, extraídas à mão de PDFs; e os 2 arquivos do modelo Ridge, que
dependem de uma decisão de reestimar.

---

## Os relatórios

Um diretório por área, todos no mesmo padrão (`generate_report.py` + `report.html` + um módulo por
aba). **Abas, fontes, decisões e pendências vivem no `CLAUDE.md` da pasta** — é lá que se lê antes
de mexer, e é lá que se escreve depois.

| área | saída | pasta |
|---|---|---|
| Câmbio | `reports/brasil/FX Report.html` | [`analytics/brasil/exchange_rate/`](analytics/brasil/exchange_rate/CLAUDE.md) |
| Câmbio — leitura narrativa | `reports/brasil/FX Outlook.pdf` | mesma pasta. É o **único relatório em PDF, e não em HTML**: lê os mesmos dados do dashboard, separa mudança marginal de nível estrutural e termina em três cenários com probabilidade |
| Inflação | `reports/brasil/Inflation.html` | [`analytics/brasil/inflation/`](analytics/brasil/inflation/CLAUDE.md) |
| Atividade | `reports/brasil/Economic Activity.html` | [`analytics/brasil/economic_activity/`](analytics/brasil/economic_activity/CLAUDE.md) |
| Fiscal | `reports/brasil/Fiscal Policy.html` | [`analytics/brasil/fiscal_policy/`](analytics/brasil/fiscal_policy/CLAUDE.md) |
| Crédito | `reports/brasil/Credit.html` | [`analytics/brasil/credit/`](analytics/brasil/credit/CLAUDE.md) |
| Mercado de trabalho | `reports/brasil/Labor Market.html` | [`analytics/brasil/labor_market/`](analytics/brasil/labor_market/CLAUDE.md) |
| Política monetária | `reports/brasil/Monetary Policy.html` | [`analytics/brasil/monetary_policy/`](analytics/brasil/monetary_policy/CLAUDE.md) |
| Expectativas (Focus) | `reports/brasil/Expectations.html` | [`analytics/brasil/expectations/`](analytics/brasil/expectations/CLAUDE.md) |
| Modelo estrutural | `reports/brasil/Structural Model.html` | [`analytics/brasil/structural_model/`](analytics/brasil/structural_model/CLAUDE.md) — versão simplificada do modelo do BC, estimada equação por equação, com o câmbio do FX Report como equação cambial. Hoje sete abas: os insumos trimestrais; a curva de Phillips aberta em serviços, alimentação, bens industriais e monitorados — em inflação do trimestre, com um seletor que lê os mesmos números acumulados em 12 meses; a equação de expectativas, que mede a força da âncora da meta, a meia-vida de um desvio e quanto de uma inflação permanente a expectativa incorpora; a curva IS, em que o aperto monetário é a inclinação da curva de juro real da NTN-B (2 anos menos 10) em vez de um juro contra uma taxa de equilíbrio; a regra de juros, com a âncora `RR* + Meta` desenhada ao lado da Selic; o câmbio trimestral, estimado por Ridge sobre o mesmo modelo que serve o FX Report, sem reescrevê-lo; e o simulador, que roda a conta solta — uma equação por vez, hoje só a de juros, com os pesos vindo de uma estimação bayesiana e a faixa saindo do posterior |
| Inflação US | `reports/us/Inflation.html` | [`analytics/us/inflation/`](analytics/us/inflation/CLAUDE.md) |
| Mercado de trabalho US | `reports/us/Labor Market.html` | [`analytics/us/labor_market/`](analytics/us/labor_market/CLAUDE.md) |
| Calendário | `reports/release_calendar.html` | [`analytics/release_calendar/`](analytics/release_calendar/CLAUDE.md) |
| Termômetro macro | `analytics/oraculo/base/Central_base.csv` → Power BI | [`analytics/oraculo/`](analytics/oraculo/CLAUDE.md) |

**Nunca edite o HTML gerado em `reports/`** — edite o `report.html` da pasta de origem e regere.

As convenções de gráfico, cor, unidade de eixo, cabeçalho, cartão de definição e camadas de métrica
são compartilhadas por todos e estão em dois lugares: a skill `lis-dashboard` (o que fazer num
relatório novo) e [`.claude/rules/lis-dashboards.md`](.claude/rules/lis-dashboards.md) (o histórico
das armadilhas já pisadas, com o número medido de cada uma).

---

## Extração de PDFs para bibliography

| Tipo de PDF | Abordagem | Custo |
|---|---|---|
| Born digital, coluna única (ex: cartas Verde) | Script `utils/extract_pdf.py` (pdfplumber) | Zero tokens |
| Artigos acadêmicos 2 colunas, relatórios de research | Ler com Claude na sessão (Read tool) | Zero tokens extras |
| PDFs novos complexos num pipeline automatizado | API Claude Haiku via `anthropic` SDK | ~$0.02/artigo |
| PDFs escaneados (sem camada de texto) | Nenhuma das acima funciona — OCR externo | Variável |

- Para papers e relatórios de research na `repository/`: ler na sessão e gerar `.md` estruturado.
- A estrutura `.md` (headers, seções) só importa para legibilidade humana no Obsidian; para o agente,
  texto limpo basta.
- **Nunca usar `pypdf` para PDFs de 2 colunas** — a ordem de leitura fica errada.
- `pdfplumber` e `pymupdf` produzem Unicode correto (ç, ã, é) — o `?` no terminal Windows é artefato
  de codepage, não corrupção.

---

## Ambiente: uv + pyproject.toml

```powershell
uv add nome-do-pacote     # adicionar pacote
uv sync                   # configurar em máquina nova
uv pip install -e .       # UMA vez por máquina, depois do sync
cp .env.example .env      # e editar com as credenciais
```

**Nunca** usar `pip install` direto — o `pyproject.toml` não será atualizado.

A instalação editável cria um `.pth` no venv apontando para a raiz, o que resolve os imports
(`connectors`, `domain`, `analytics`, `utils`) independentemente de onde o script roda. Sem ela,
`python jobs/update_oraculo.py` falha com `ModuleNotFoundError: No module named 'analytics'`. Todo
pacote do projeto precisa de `__init__.py` para o `setuptools.packages.find` encontrá-lo.

📄 Racional, papel de cada arquivo, atualização de versões e troubleshooting: [`AMBIENTE.md`](AMBIENTE.md).

---

## Pendências

📄 [`PENDENCIAS.md`](PENDENCIAS.md) — só o que é **transversal** (cobertura de dados, jobs sem
agendamento, tabelas órfãs), mais o índice de onde fica o "Pending" de cada área. Pendência de um
relatório específico é atualizada no `CLAUDE.md` da pasta dele, não aqui.
