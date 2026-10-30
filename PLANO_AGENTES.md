**Sobre este arquivo:** o plano de construção do sistema de agentes-analistas: frentes, ordem, quem faz o quê. As decisões ficam no [`SISTEMA_AGENTES.md`](SISTEMA_AGENTES.md) e os princípios no [`PRINCIPIOS_AGENTES.md`](PRINCIPIOS_AGENTES.md); aqui fica a ordem do trabalho. O chat principal marca o status na tabela abaixo.

Desde 2026-10-30 o trabalho corre em **vários chats, coordenados por um principal**. Cada chat tem um brief em [`coordenacao/`](coordenacao/README.md), com o escopo, o que ler, o que pode escrever e o que precisa do usuário. O detalhe de cada frente está lá; aqui fica a visão de conjunto.


# Plano 2 (desde 2026-10-30)

**Objetivo:** o ciclo 2, com **nove agentes**, até o relatório do escrivão:

- os sete de hoje, com a camada 1 de literatura e de modelos mentais;
- dois novos, **mercado de trabalho e crédito**, já criados com a camada 1 de literatura e de modelos mentais;
- um **ciclo redesenhado**: report 1 mais enxuto e uma **conversa com moderador** no lugar das rodadas, com o papel do moderador bem definido;
- o **Modelo Estrutural revisto** a partir do feedback dos próprios agentes, porque hoje ele complica o trabalho deles.

O ciclo 2026-10-27 (o primeiro conjunto, sem literatura) é a base de tudo: os reports, a ata da moderação, o log e o relatório dele são o material de partida das frentes A e C.


## Status

As frentes estão na ordem do que mais precisa do usuário para o que menos.

| Frente | O quê | Chat | Quanto precisa do usuário | Status |
|---|---|---|---|---|
| A | Desenho do ciclo e do moderador | A | **muito**: conversas de desenho e decisões em janela, do formato do ciclo ao papel do moderador | **feito** (2026-10-30: A1–A3; decisões em SISTEMA III.III.viii) |
| B | Agentes de mercado de trabalho e crédito | B | **muito**: dois mapas conceituais aprovados parte a parte, fronteiras com atividade, PM e fiscal, lista de dados | fronteiras e perguntas decididas (SISTEMA III.III.ix); mapas em rascunho; a tese espera C |
| C | Modelo Estrutural, a partir do feedback dos agentes | C | **médio**: ler o feedback consolidado, escolher o que mudar, aprovar o resultado da reestimação | C1 feito (feedback dos sete, testes de âncora e hiato, PDF); decisões adiadas pelo usuário para antes do ciclo 2 |
| D | Conhecimento: camada 1 de literatura e de modelos mentais | D | **pouco**: a escolha das gestoras (uma janela) e a camada 1 dos dois novos, com o julgamento delegado como em 2026-10-29 | D1 em curso: Verde-inflação feito (~2,8M); expectativas descartado; Kapitalo-externo e Kinea-fiscal/atividade a seguir |
| E | Engenharia do ciclo | E | **pouco**: a regra do corte do F por divulgação | E1 feito (ciclo 10-27 fechado; sem regra de corte, decisão do usuário); E2 parte A em curso |
| F | O ciclo 2 | F | **no fim**: a data, a base atualizada, a revisão da conversa, dos P e do relatório | espera A–E |
| P | Coordenação | principal | o ponto de contato: abre as ondas, integra as decisões | em curso |


## Ondas

**Onda 1 — começa já, em paralelo:**
- A1. A conversa de desenho do ciclo, a partir do ciclo 2026-10-27.
- B1. Rascunho dos mapas de mercado de trabalho e de crédito, e as janelas de aprovação.
- C1. O feedback dos agentes sobre o modelo: juntar a seção 6 de todos os reports de 2026-10-27 e perguntar a cada um dos sete onde o modelo complicou o trabalho.
- D1. As gestoras da camada 1 dos cinco agentes novos e o `/mental` de cada área.
- E1. Fechar o ciclo 2026-10-27 (cobrança C6 e conferência do relatório contra o banco) e o corte do F por data de divulgação.

**Onda 2 — cada item começa quando a entrada dele chega:**
- A2. Os templates do ciclo novo (report 1, ata, log) e a definição do moderador. Entrada: as decisões de A1.
- B2. Os módulos de dados e as definições dos dois agentes novos, e o ajuste dos sete (mapas e listas de dados: crédito e mercado de trabalho deixam de ser TWA). Entrada: os mapas aprovados.
- C2. As mudanças escolhidas no modelo, reestimadas, com o `modelo.py` e os testes. Entrada: a escolha do usuário em C1.
- D2. A camada 1 de literatura e a gestora dos dois agentes novos. Entrada: os mapas de B1.
- E2. O ciclo novo nas definições dos sete e na consolidação, e o registro dos dois novos no motor, no retrato e no tracker. Entrada: A2, B2 e C2.

**Onda 3:**
- E3. Montagem de ensaio dos nove, com literatura (dados e retrato), e os testes.
- F. O ciclo 2.

O modelo muda antes do ciclo 2 e fica fixo nele, como o F(A).


## Dependências que cruzam chats

- **B e C:** se crédito e mercado de trabalho ganham variável no Modelo Estrutural (ideia do usuário: crédito na curva IS; o desemprego no hiato), a decisão é de C e a tese dos dois agentes depende dela. Até lá, os dois seguem a regra do fiscal e do externo: a tese é o caminho base das exógenas que tutelam.
- **A e C:** a conversa moderada substitui a rodada 2, e o P1, o P2 e o PF* saem da consolidação. Se A mudar o que é consolidado e quando, C e E precisam saber antes de mexer no `modelo.py` e na `consolidacao.py`.
- **B e D:** a camada 1 dos dois novos é uma fonte por canal da Parte 2 do mapa, então D2 espera os mapas aprovados.
- **A, B, C → E:** E é quem escreve as definições dos sete e o motor. Ninguém mais mexe nesses arquivos (`coordenacao/README.md`, tabela de donos).


## Custo

Medido no ciclo 2026-10-27, com sete agentes: rodada 1 ~2,0M, rodada 2 ~2,4M, report final ~0,7M, agente web ~2,5M, escrivão ~0,6M, ~8–9M no total, mais a sessão que conduziu. Medido em 2026-10-29: a camada 1 de literatura dos cinco agentes novos custou ~3,6M.

| Frente | Estimativa (a partir desses precedentes) |
|---|---|
| A | 2–5M (conversa e templates) |
| B | 5–10M (dois mapas, dados, definições, ajuste dos sete) |
| C | 1M de feedback; 5–15M de implementação, conforme o que for escolhido |
| D | ~2M de literatura dos dois novos; ~1–2M por documento de modelo mental (sete documentos) |
| E | 3–8M |
| F | 12–20M (nove agentes, literatura, conversa moderada) |
| Total | ~40–70M |

As estimativas não são medidas. O valor real fica no `/usage-credits`; cada chat anota o custo de cada passo no próprio arquivo de coordenação.


## Verificação

- **Montagem:** `uv run python -m analytics.agent_system.dados <agente> --ciclo <data>` roda para os nove, e o `motor.conferir` bate com a lista de cada um.
- **Retrato:** `conhecimento.itens` sem item faltando para os nove; o retrato monta com literatura.
- **Testes:** `tests/test_dados_agentes.py`, `tests/test_conhecimento.py`, `tests/test_modelo_agentes.py`, `tests/test_consolidacao.py`, `tests/test_tracker.py`, `tests/test_vault.py`, `tests/test_ingestion.py`.
- **Mapas:** `vault.py map <área>` passa nos nove.
- **Modelo:** a reestimação reproduz o painel do `Structural Model.html` e o `modelo.rodar` bate com ele.
- **Relatório:** os números conferidos contra a fonte (III.III.iii); o log com o que cada agente abriu.


# Plano 1 (2026-10-21 a 2026-10-28): feito

O objetivo era o primeiro ciclo conjunto dos sete agentes, até o relatório do escrivão, e foi cumprido no ciclo 2026-10-27. O detalhe das fases está no git (este arquivo antes de 2026-10-30).

| Fase | O quê | Status |
|---|---|---|
| 0 | Registrar o framework e arrumar | feito (2026-10-21) |
| 1 | Camada 1 e fila do câmbio | feito (2026-10-21) |
| 2 | Mapa conceitual, camada 1 e fila de PM | feito (2026-10-21) |
| 3 | Infraestrutura (F de PM, Selic de fechamento, retrato, flag sem literatura) | feito (2026-10-21) |
| 4 | Re-teste do câmbio só com o núcleo | feito (2026-10-21) |
| 5 | Material da camada 1 de PM (modelo mental da Verde) | feito (2026-10-21) |
| 6 | Agente de PM e teste solo | feito (2026-10-21) |
| 7 | Desenho do ciclo conjunto | feito (2026-10-22) |
| 8 | Os cinco agentes novos, na forma mínima | feito (2026-10-22; a Parte 4 dos mapas novos depois, 63cfc6a) |
| 9 | Engrenagem do ciclo conjunto (dados, consolidação, escrivão, templates) | feito (2026-10-22; principal/subordinado em 2026-10-27, 7d5b687) |
| 10 | O primeiro ciclo conjunto, sem literatura | feito (ciclo 2026-10-27, rodadas 1 e 2, moderação em teste, RF, PF*, relatório; fecha em E1) |
| — | Camada 1 de literatura dos cinco novos e arquivos na pasta do dono | feito (2026-10-29, SISTEMA II.IV) |


# O framework: começar pequeno, testar, ampliar

Ingerir e sintetizar toda a literatura de câmbio e de PM antes de ter o agente foi um erro estratégico (avaliação do usuário, 2026-10-21). Ainda não se sabe quanto o agente de fato busca na literatura nem como a usa, e isso só aparece rodando. O sistema fica de pé com o mínimo e cresce conforme recebe mais conteúdo; se errarmos, erramos pequeno. Registrado como princípio em `PRINCIPIOS_AGENTES.md` (I.VI).

- **Camadas do material** (literatura, modelos mentais, documentos do Copom):
    - **Camada 1, o núcleo:** uma fonte por canal do esqueleto causal do mapa. Uma gestora nos modelos mentais. Do Copom: comunicados, atas e RPMs publicados desde o início do mandato do Galípolo (2025-01-01), sempre anteriores à data do ciclo.
    - **Camada 2:** profundidade, alternativas, evidência brasileira adicional, as outras gestoras.
    - **Camada 3:** o resto, inclusive o histórico.
- **Agente novo:** ingere e sintetiza só a camada 1.
- **O agente enxerga só a camada 1**, por um retrato do conhecimento por ciclo, fixo no ciclo como o F(A).
- **Promoção:** pela fila de prioridade de cada agente, um lote de 3 a 5 por ciclo aprovado, ou pela demanda do ciclo, que fura a fila. Até existir o agente administrador, o usuário aprova cada lote.
- **O log de cada ciclo lista os arquivos de conhecimento que o agente abriu.**


# Sem amarrar (pedido do usuário, 2026-10-22)

Quem influencia o modelo, e por qual variável, vai mudar. Por isso o vínculo entre agente e variável do modelo fica em **dado declarativo**, não em código: a consolidação lê a aba "Exógenas" do `data_tracker.xlsx`, uma exógena por linha, com o principal e os subordinados de cada uma. Mudar a tutela é editar uma célula. A tese de cada agente também não fica presa a ter variável no modelo. O objetivo é construir simples e ir fazendo o fine tuning.


# Anotado para depois (fora deste plano)

Os itens que o Plano 2 absorveu saíram daqui: o report 1 enxuto, a ordem de escrita, como o ciclo incorpora o anterior e as notas a–d e f da leitura de 2026-10-27 estão na frente A; as notas e, g e h, a taxa neutra e a Selic de fechamento, na frente C; o corte do F por divulgação, na frente E; os agentes de crédito e de mercado de trabalho, na frente B; as gestoras dos cinco, na frente D.

- **Estudo de cada exógena** para definir a tutela com mais cuidado. Mais de um agente pode acompanhar a mesma exógena, com prioridades diferentes.
- Variáveis próprias da área para fiscal e externo, além do caminho das exógenas (candidato da frente C, se o feedback pedir).
- O modelo de PIB do agente de atividade, com a demanda do governo vindo do fiscal (candidato da frente C).
- Um modelo do hiato que regride só a parte consolidada do hiato do BC (até dois ou três anos atrás, a de menor revisão esperada) contra PIB, desemprego, indústria e outros, e usa os coeficientes para a frente (ideia do usuário, 2026-10-22; candidato da frente C).
- Os demais agentes (trader, administrador), as promoções de câmbio e PM e o estoque de sínteses pendentes.
- **Conhecimento produzido por nós e notas de divulgação** (usuário, 2026-10-29, retomar com calma): SISTEMA II.I.viii e ix.
- O diagrama (`analytics/agent_system/report.html:322`) ainda diz "os cenários worst de cada agente".
- **A revisar** (pedidos do usuário, 2026-10-21): um pente fino no processo dos modelos mentais (as regras do `mental-model.md` e do revisor); a estrutura do modelo mental da Verde de PM (juros dos desenvolvidos no bloco 3, 2.3 × 3.2, 2.6 de uma carta só, 1.1 × a 1.2 do câmbio).
- **Pendências pequenas da base de conhecimento** (2026-10-29): a síntese do Goldfajn (2000) com conta do autor da síntese; `exchange_rate_pass_through` sem "When it applies" e `mundell_fleming_policy_mix` fora do modelo de página; o catálogo de working papers do BCB no fim de dois clean_md de expectativas; as 14 sínteses antigas do câmbio que não passam no `vault.py check`.
