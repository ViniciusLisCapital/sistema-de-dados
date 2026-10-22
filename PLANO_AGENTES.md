**Sobre este arquivo:** o plano de construção do sistema de agentes-analistas, com fases, estimativas e quem faz cada coisa. As decisões ficam no [`SISTEMA_AGENTES.md`](SISTEMA_AGENTES.md) e os princípios no [`PRINCIPIOS_AGENTES.md`](PRINCIPIOS_AGENTES.md); aqui fica a ordem do trabalho. Ao fim de cada fase, o chat principal marca o status na tabela abaixo.

O primeiro plano (aprovado em 2026-10-21) ia até um ciclo conjunto só de câmbio + PM. As Fases 0–6 dele foram feitas. Em 2026-10-22 o usuário mudou o rumo, e as Fases 7–9 daquele plano foram substituídas pelas Fases 7–10 abaixo.

**Objetivo final, desde 2026-10-22:** os sete agentes do primeiro batch rodando juntos um ciclo completo, até o relatório do escrivão:

- os que já existem: câmbio e política monetária (PM);
- os cinco novos: inflação, atividade, fiscal, externo e expectativas.

Fica fora deste plano tudo o que não leva a isso (lista em "Anotado para depois"). Por ora, não se mexe em outras coisas.


# Status

| Fase | O quê | Status |
|---|---|---|
| 0 | Registrar o framework e arrumar | feito (2026-10-21) |
| 1 | Camada 1 e fila do câmbio | feito (2026-10-21): donos, camada 1 e fila no tracker; as 6 fontes da camada 1 com síntese que passa no check; conceito fx_intervention criado; Kalemli-Ozcan 2019 entrou na camada 1 (canal 2.3) |
| 2 | Mapa conceitual, camada 1 e fila de PM | feito (2026-10-21): mapa com as Partes 1–4 aprovadas (perguntas Q1–Q4, refeitas após o teste solo; horizonte; worst/best; saídas e entradas espelhadas no câmbio); camada 1 de PM (10 fontes, uma por canal, todas com síntese) e fila aprovadas e marcadas no tracker |
| 3 | Infraestrutura | feito (2026-10-21): 3A (F de PM, acea399, 6698688), 3B (Selic de fechamento derivada da média de dois trimestres, 5fdab47; a revisar no fim), 3C, 3D e 3E |
| 4 | Re-teste do câmbio só com o núcleo | feito (2026-10-21, dados de 15/10): report completo com pouca literatura aberta; Kapitalo promovida para a camada 1; síntese do Cortapasso refeita pelo `/vault` (f44c8a0); o câmbio declara a lacuna do Copom em vez de escrever de memória (SISTEMA II.II.iv) |
| 5 | Material da camada 1 de PM | feito (2026-10-21): modelo mental da Verde, 24 cartas em 3 rodadas (14d91ac); as 10 fontes da camada 1 já tinham síntese |
| 6 | Agente de PM e teste solo | feito (2026-10-21): definição (`.claude/agents/politica-monetaria-analyst.md`); dois testes solo em `obsidian/ciclos/2026-10-15/` (fba897b, 414eda4). Da revisão do usuário: passo máximo de 25 p.b. afirmado de memória (virou o princípio I.II.ix); foco vai × deveria × mercado (Q1–Q4); central do modelo em todos os trimestres; seção 6, "Sobre o modelo", em todo report. Promovidos Segura-Ubiergo e Adrian-Crump-Moench. Seta no diagrama (9f6383e) |
| 7 | Desenho do ciclo conjunto (decisões) | feito (2026-10-22): SISTEMA IV.ii, IV.vi, IV.vii e III.III.vii; a tutela das exógenas virou a aba "Exógenas" do tracker, **que o usuário preenche**; caudas upside/downside para todos; relatório por tema com apêndice por área (manual §13) |
| 8 | Os cinco agentes novos, na forma mínima | quase feito (2026-10-22): os cinco mapas aprovados (o fiscal reescrito nas duas discussões, com foco no impacto na demanda), listas V.III–V.VII, módulos de dados e definições (1a7ef6a, b23ea25, cd52f2f, 04d3102, 0e311f4), os sete em `AGENTES` (50a40b0), ajuste de câmbio e PM (d0a14d1, 2026-10-22; linhas S5–S10 do câmbio e S7–S13 da PM aprovadas pelo usuário; repasse tirado e renumerado, 318dfb0). **Falta a Parte 4 (entradas) dos cinco mapas novos** |
| 9 | Engrenagem do ciclo conjunto | quase feito (2026-10-22): E1 (71bbb16, 78c79f6), E2 consolidação (4f9f186), E3 escrivão (94a1672), E4 grupos do IPCA e upside/downside (faab307), templates (9b262ce), tutela preenchida (cf8a7c6, efe85f7). Falta a unificação das `variante` e o teste dos sete |
| 10 | O primeiro ciclo conjunto, sem literatura | — |

## Para a próxima sessão (handover de 2026-10-22)

Esta sessão parou aqui por custo (o chat ficou longo). Ler este bloco, a tabela acima, a seção (III) e o `SISTEMA_AGENTES.md` III.III.i, III.III.vii, IV.ii, IV.vi e IV.vii.

**Modelo dos subagentes** (decisão do usuário, 2026-10-22): Sonnet para engenharia com teste; Opus para mapas, definições, rodadas do ciclo e escrivão.

**Próximos passos, nesta ordem:**
1. **Ajuste de câmbio e PM** (feito 2026-10-22, d0a14d1 e 318dfb0; sobra a Parte 4 dos cinco mapas novos, abaixo). O que se pedia:
    - V.I e V.II do SISTEMA: os grupos TWA viram "Endógeno de <agente> (consulta)" conforme as fronteiras de III.III.vii (inflação, atividade com hiato e mercado de trabalho, fiscal com o CDS, externo, expectativas com Focus e QPC); o CDS sai de "Exógeno". O `motor.conferir` tem de seguir passando.
    - Os dois mapas: a linha do repasse (E3 do câmbio, S3 da PM) vai para a inflação; na PM, 2.3 (ancoragem) vai para expectativas, 2.4 (hiato) para atividade, a leitura do prêmio fiscal (2.5, 2.6) para o fiscal, o caminho do Fed (2.8, item 6 do horizonte) para o externo; as seções 3.2/4.2 "not defined yet" viram linhas; worst/best → upside/downside; tutela pela aba.
    - As duas definições (`cambio-analyst.md` 110–112, `politica-monetaria-analyst.md` 133–134 ainda dizem worst/best e Pbc − Pwc): upside/downside, JSON de caminhos, tutela, divergência, multiplicador do dono da equação, sem literatura.
    - `cambio.py`: CLP e COP do `cmb_fx_latam` (BIS) chegam com um dia de defasagem (correlação com o dólar EM 0,02 no mesmo dia, 0,55 alinhado); o externo já alinha, câmbio e PM não.
    - **A Parte 4 (entradas) dos sete mapas**, espelho das Partes 3: hoje é placeholder nos cinco novos.
2. **Unificação das `variante`** (subagente, Sonnet): os recortes de `expc_focus_periodo` declarados por inflação (componentes), atividade (PIB, desocupação) e fiscal (fiscal) passam a vir de expectativas, onde fizer sentido; `tests/test_dados_agentes.py` cobrindo os sete (`conferir` e `conferir_consultas` já passam nos sete).
3. **Fase 10:** a conversa sobre o recorte e a tempestividade, com o que os subagentes acharam: Focus parada em 09/10; CDS em 14/10 (carga manual); `cred_fluxo_financeiro` em abr/26; `mt_pnad` fora do job de rotina; posição de swap do BC em 01/08; EFGG e PIB trimestral no 2T26; `inflc_meta` só até 2026; inflação implícita de 1 ano em 6,66% contra Focus 4,48% (vértice curto da NTN-B, causa não confirmada); IPCA 24m suavizado com 17 respondentes. Depois: o usuário atualiza a base, escolhemos a data, `dados <agente> --ciclo D --sem-literatura` para os sete, conferir F e retratos, rodadas (a definição do fiscal espera `tutela=...` nos argumentos).

**Placar do hiato** (decidido 2026-10-22, depois do handover): o primeiro RPM depois do PIB do IBGE do trimestre, a edição do fechamento do trimestre seguinte. Mapa, definição e F da atividade já mudaram.

**Fora do plano, anotado:** o diagrama (`analytics/agent_system/report.html:322`) ainda diz "os cenários worst de cada agente".

O A e o F(A) de câmbio e PM do ciclo 2026-10-22 já foram montados, antes da mudança de rumo. A data do ciclo conjunto será escolhida na Fase 10, depois da conversa sobre o recorte dos dados.

**A revisar quando o plano terminar** (pedidos do usuário, 2026-10-21):
- a Selic de fechamento derivada da média de dois trimestres (reestimar a regra no fechamento?);
- um pente fino no processo dos modelos mentais (as regras gravadas no `mental-model.md` e no revisor nesse dia);
- a estrutura do modelo mental da Verde de PM (juros dos desenvolvidos no bloco 3, 2.3 × 3.2, 2.6 de uma carta só, 1.1 × a 1.2 do câmbio).

**Para o próximo plano** (decisão do usuário, 2026-10-21): refazer a construção da taxa neutra do Modelo Estrutural, a âncora `rr_10a` + meta da regra de juros, incluindo uma suavização da taxa de 10 anos (ver as propostas do 2º teste de PM em `SISTEMA_AGENTES.md` III.III.vi, 1 e 3). Até lá, a tabela da tese de PM fica como está: faixa em volta da central do modelo, mesmo com a massa do agente na cauda.


# (I) O framework: começar pequeno, testar, ampliar

Ingerir e sintetizar toda a literatura de câmbio e de PM antes de ter o agente foi um erro estratégico (avaliação do usuário, 2026-10-21). Ainda não se sabe quanto o agente de fato busca na literatura nem como a usa, e isso só aparece rodando. Daqui em diante, o sistema fica de pé com o mínimo e cresce conforme recebe mais conteúdo; se errarmos, erramos pequeno e corrigimos em escala menor. Registrado como princípio em `PRINCIPIOS_AGENTES.md` (I.VI).

- **Camadas do material** (literatura, modelos mentais, documentos do Copom):
    - **Camada 1, o núcleo:** o mínimo que cobre cada pergunta central e cada canal do esqueleto causal do mapa, com uma fonte por canal (~8–12 por agente). Uma gestora nos modelos mentais. Do Copom: comunicados, atas e RPMs publicados desde o início do mandato do Galípolo (2025-01-01), sempre anteriores à data do ciclo.
    - **Camada 2:** profundidade, alternativas, evidência brasileira adicional, as outras gestoras.
    - **Camada 3:** o resto, inclusive o histórico.
- **Agente novo:** ingere e sintetiza só a camada 1. As camadas 2 e 3 ficam listadas no tracker e não são ingeridas.
- **O agente enxerga só a camada 1**, por um **retrato do conhecimento por ciclo**: uma cópia em `obsidian/ciclos/<data>/conhecimento/<agente>/`, fixa no ciclo como o F(A).
- **Promoção, por dois caminhos:**
    - **Fila de prioridade por agente, o caminho normal.** A cada ciclo aprovado sobe o próximo lote (3 a 5 itens), e o ciclo seguinte testa esse lote.
    - **Demanda do ciclo, que fura a fila.** O que um ciclo mostra que faltou vai para o topo. O sinal vem do log ou da revisão do usuário.
    - Até existir o agente administrador, o usuário aprova cada lote.
- **O log de cada ciclo lista os arquivos de conhecimento que o agente abriu.**

**Neste plano o primeiro ciclo conjunto roda sem literatura** (decisão de 2026-10-22): cada agente lê só o mapa conceitual dele, e a PM lê também os documentos do Copom. A camada 1 dos agentes novos fica para depois.


# (II) Contexto da mudança (2026-10-22)

Com só dois agentes, cada um escrevia exógenas que não lhe competem. O caso mais claro foi a NTN-B de 10 anos, que decidiu a central da Selic sem ter dono. A decisão: criar de uma vez os agentes que o Modelo Estrutural precisa, sem teste solo, e o primeiro teste já é o ciclo conjunto. A forma de cada agente novo é a mínima; expectativas ganha agente próprio.


# (III) Fases

## Fase 7 — Desenho · decisões, chat principal, com o usuário
1. **Tutela de cada exógena do modelo.** Decidido (2026-10-22): fica na aba "Exógenas" do `data_tracker.xlsx`, com níveis de 1 a 5 por agente, e quem preenche é o usuário. A coluna "Proposta" traz a sugestão:
    - **externo:** `ffr`, `infl_us`, `dxy_em`, `sp500`, `icbr_usd`, `icbr_agr_usd`, `icbr_met_usd`;
    - **fiscal:** `fiscal` (o CDS);
    - **câmbio:** `vol`;
    - **PM:** `meta_12m`;
    - **fiscal ou PM:** `rr_10a`.
2. **Endógenas do modelo:**
    - hiato → atividade;
    - IPCA → inflação;
    - expectativas → expectativas;
    - Selic → PM;
    - câmbio → câmbio.
3. **A tese de fiscal e externo, que não têm variável no modelo.** Proposta: a central é o caminho base do próprio agente, e a distribuição em volta dela também é dele.
4. **Consolidação.**
    - O P é uma rodada do modelo com o caminho base de cada exógena, vindo do dono, sem multiplicadores.
    - Da rodada 2 em diante, a central de quem tem variável no modelo vem do P.
    - O PF* é a central conjunta mais a distribuição de cada agente.
    - Os caminhos base saem num JSON padrão, com as chaves do `modelo.CONVENCAO`.
5. **Estrutura do relatório do escrivão** (§13 do manual).

## Fase 8 — Os cinco agentes novos, na forma mínima · subagentes em paralelo; uma janela de aprovação por agente
1. **Rascunho do mapa conceitual**, Partes 1 a 4. Externo e expectativas ganham pasta no vault.
2. **Aprovação, numa janela por agente:**
    - perguntas centrais;
    - variável, horizonte e worst/best;
    - lista de dados (V.III–V.VII do SISTEMA, a partir das tabelas que hoje são TWA nas listas V.I e V.II);
    - saídas e entradas.
3. **Módulo de dados** `analytics/agent_system/dados/<agente>.py`, mais a linha no `AGENTES`.
4. **Definição** `.claude/agents/<agente>-analyst.md`, derivada das duas que já existem.
5. **Ajuste de câmbio e PM:** o que hoje é TWA dessas áreas vira "endógeno de outro agente", e a premissa passa a vir do report do dono. Os mapas recebem as saídas e entradas novas.

## Fase 9 — Engrenagem · subagentes, em paralelo com a 8
Só o que o ciclo conjunto precisa:
- **`dados/`:**
    - helper genérico `_de(modulo, nome, ...)` para um agente reaproveitar a tabela de outro;
    - checagem de conflito de consulta entre todos os pares de agentes;
    - o erro do retrato do conhecimento não pode deixar o F gravado pela metade.
- **`conhecimento.py`:**
    - `expectativas` e `externo` reconhecidos;
    - flag `--sem-literatura`, que mantém o mapa e os documentos do Copom.
- **Tracker:** `expectativas` como dono válido.
- **`analytics/agent_system/consolidacao.py`:**
    - lê os JSON de caminhos e a tabela declarativa exógena → dono (ver "Sem amarrar");
    - usa o caminho do dono de cada exógena e registra quem divergiu;
    - roda `modelo.rodar`;
    - escreve P1, P2 e PF*.
- **Templates:** `_modelo_report.md` sem exemplos só de câmbio, mais a regra para quem não tem exógena; `_modelo_log.md` com divergências entre vários agentes.
- **Agente escrivão** (`.claude/agents/escrivao.md`).
- **Testes:**
    - `tests/test_dados_agentes.py`;
    - `tests/test_conhecimento.py`;
    - um teste novo da consolidação.

## Fase 10 — O ciclo conjunto · chat principal + sete subagentes por rodada
1. **Antes de rodar:**
    - conversa sobre o recorte do A e a tempestividade de cada dado;
    - o usuário atualiza a base;
    - escolhemos juntos a data do ciclo.
2. **Montagem:**
    - `dados <agente> --ciclo <data> --sem-literatura` para os sete;
    - conferir, de cada agente, o F, o retrato e a definição.
3. **Rodada 1:** os sete agentes. O chat principal lê os reports e traz os problemas antes do P1.
4. **P1 → rodada 2 → P2 → report final → PF*.** O usuário revisa cada P.
5. **Escrivão:** o relatório conjunto, a checagem dos números contra a fonte e o log.


# (IV) Quem faz o quê

**O chat principal coordena e fala com o usuário.** Todas as decisões passam por ele, na janela de escolha. Ele também edita sozinho os arquivos que todo mundo lê: `SISTEMA_AGENTES.md`, este arquivo, os `CLAUDE.md`, a linha `AGENTES` de `dados/__main__.py` e os templates do ciclo.

**O resto vai para subagentes, disparados daqui, que devolvem o resultado para cá.** Nenhuma tarefa deste plano precisa de chat separado: nenhuma usa `/loop` nem comando que só o usuário pode digitar. Se o usuário quiser acompanhar alguma tarefa de perto, ela vira chat separado e o principal escreve o pedido pronto para colar.

| Tarefa | Quem | Começa quando | Escreve em |
|---|---|---|---|
| Fase 7, decisões de desenho | principal | já | SISTEMA, este arquivo |
| **E1.** Base da engrenagem: helper `_de`, checagem de conflito entre todos os pares, `conhecimento.py` (`expectativas`, `externo`, `--sem-literatura`), `expectativas` no tracker, testes | subagente | já | `dados/motor.py`, `dados/politica_monetaria.py`, `conhecimento.py`, `tracker.py`, `tests/` |
| **M1–M5.** Rascunho do mapa de cada agente novo: Partes 1–4 e a proposta de lista de dados | 5 subagentes em paralelo, um por agente | já | só o mapa daquela área (sem commit) |
| Aprovação de cada agente | principal + usuário | o rascunho dele chegar | janela de escolha; SISTEMA V.III–V.VII |
| **M1–M5, continuação.** Módulo de dados e definição do agente, depois da aprovação | o mesmo subagente do rascunho, retomado com o contexto dele | aprovação do agente e E1 pronto | `dados/<agente>.py`, `.claude/agents/<agente>-analyst.md` |
| Ajuste de câmbio e PM (endógeno de outro agente, saídas e entradas novas) | subagente | os cinco aprovados | os dois mapas, as duas definições, `cambio.py`, `politica_monetaria.py` |
| **E2.** `consolidacao.py`, a tabela de donos e o teste | subagente | Fase 7, item 4 decidido | `analytics/agent_system/consolidacao.py`, `tests/` |
| **E3.** Agente escrivão | subagente | Fase 7, item 5 decidido | `.claude/agents/escrivao.md` |
| Fase 10, cada rodada | 7 subagentes em paralelo, um por agente | montagem conferida | os reports do ciclo |
| P1, P2, PF*, log | principal (roda o `consolidacao.py`) | os sete reports da rodada | pasta do ciclo |
| Relatório | subagente escrivão | o PF* | `relatorio.md` |

**Regras para o paralelo:**
- cada subagente commita só os próprios caminhos (`git add` explícito, nunca `-a`);
- dois subagentes não escrevem no mesmo arquivo ao mesmo tempo. Por isso o E1 vem antes da continuação de M1–M5, que usa o `_de`; e o ajuste de câmbio e PM vem depois dos cinco;
- um subagente não pode disparar outro, então as rodadas do ciclo são disparadas pelo principal;
- `obsidian/concepts/` é escrito só pelo `/vault`.


# (V) Sem amarrar (pedido do usuário, 2026-10-22)

Quem influencia o modelo, e por qual variável, vai mudar. Um exemplo: o modelo de PIB, quando existir, vai receber a demanda do governo do agente fiscal. Por isso o vínculo entre agente e variável do modelo fica em **dado declarativo**, não em código. A consolidação lê a aba "Exógenas" do `data_tracker.xlsx` (2026-10-22, antecipada a pedido do usuário): uma exógena por linha, os agentes nas colunas, tutela de 1 a 5. Mudar a tutela é editar uma célula. A tese de cada agente também não fica presa a ter variável no modelo. O objetivo é construir simples e ir fazendo o fine tuning.


# (VI) Anotado para depois (fora deste plano)

- **Estudo de cada exógena** para definir a tutela com mais cuidado (a aba "Exógenas" já existe, preenchida pelo usuário). Mais de um agente pode acompanhar a mesma exógena, com prioridades diferentes.
- **Ordem de escrita dos reports** (ideia do usuário, 2026-10-22): numa rodada, o segundo agente já lê o report do primeiro, e assim por diante, para haver mais interação entre eles. Na Rodada 1 do primeiro ciclo conjunto os sete rodam independentes, sem ler os reports dos outros. Há que decidir a ordem e o que cada um pode ler.
- **Corte do F por data de divulgação** (achado da Rodada 1 de inflação, 2026-10-22): o F corta as tabelas pela data de referência, então o ciclo de 2026-10-02 trouxe o IPCA de set/26 (divulgado em 9/10) e a PMS de ago/26. O Modelo Estrutural parte do 3T26 com o IPCA 12m de set (4,58%, contra 4,30% do QPC), e a central do 4T26 leva 0,28 p.p. dessa diferença. Decidido pelo usuário (2026-10-22): seguir o primeiro ciclo com o F como está, declarando o vazamento nos reports e no log, por ser um teste do sistema; corrigir antes do próximo ciclo (atraso de divulgação por tabela, ou o calendário).
- **A tutela é peso, não exclusividade** (correção do usuário, 2026-10-22): os níveis da aba "Exógenas" dão o peso da opinião de cada agente, e todos com nível escrevem o caminho. Falta decidir o peso de cada nível e mudar `consolidacao.py`, a nota da aba e as definições (hoje: vale o melhor nível, empate em média, e caminho fora do nível vira divergência). Fazer antes do P1.
- Variáveis próprias da área para fiscal e externo, além do caminho das exógenas.
- O modelo de PIB do agente de atividade, com a demanda do governo vindo do fiscal.
- Um modelo do hiato que regride só a parte consolidada do hiato do BC (até dois ou três anos atrás, a de menor revisão esperada) contra PIB, desemprego, indústria e outros, e usa os coeficientes para a frente (ideia do usuário, 2026-10-22).
- A camada 1 de literatura dos agentes novos (~5 fontes cada), o ciclo com literatura e a medição do ruído (a rodada 1 duas vezes).
- O agente de busca na internet (a discutir).
- Os demais agentes (crédito, mercado de trabalho, trader, administrador), as promoções de câmbio e PM, o estoque de sínteses pendentes e o diagrama.
- **Mover os arquivos para a pasta do dono**, de uma vez, quando a camada 1 dos agentes novos entrar. Um script move os arquivos e reescreve os wikilinks; o `vault.py check` confere.
- Duas páginas de conceito apontadas pelo `/vault`: `exchange_rate_pass_through` traz uma conta do próprio autor; `monetary_policy_shocks` ainda diz que não há fonte brasileira.


# (VII) Registro e custo

**Registro, ao executar:** `SISTEMA_AGENTES.md` I.II.i reescrito; I.III.xii (agente de expectativas); IV.ii e IV.vi decididos; V.III–V.VII.

| Fase | Tokens (aproximados) |
|---|---|
| 8 | ~150 M |
| 9 | ~60 M |
| 10 | ~150 M |
| Total | ~360 M, em ~1 semana |

O gargalo são as cinco janelas de aprovação da Fase 8. Os valores reais ficam no `/usage-credits`.


# (VIII) Verificação

- **Montagem:** `uv run python -m analytics.agent_system.dados <agente> --ciclo <data> --sem-literatura` roda para os sete, e o `motor.conferir` bate com a lista de cada um.
- **Testes:**
    - `tests/test_dados_agentes.py`;
    - `tests/test_conhecimento.py`;
    - `tests/test_modelo_agentes.py`;
    - o teste da consolidação.
- **Mapas:** `vault.py map <área>` passa nos sete.
- **Consolidação:** `consolidacao.py` reproduz o `modelo.rodar` com os caminhos juntados e levanta quando há dono em conflito.
- **Relatório:** os números conferidos contra a fonte; o log com o que cada agente abriu e o que faltou.
