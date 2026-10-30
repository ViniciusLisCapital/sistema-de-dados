# Chat C — Modelo Estrutural, a partir do feedback dos agentes

**Objetivo.** Rever o Modelo Estrutural, que hoje complica o trabalho dos agentes. Primeiro o feedback dos próprios agentes, consolidado; depois o usuário escolhe o que mudar; por fim a mudança, reestimada, entra no `modelo.py` antes do ciclo 2 e fica fixa nele.

**Ler primeiro:**
- `README.md` desta pasta.
- `analytics/brasil/structural_model/CLAUDE.md` e os `pendencias_*_eq.md` da mesma pasta.
- `analytics/agent_system/modelo.py`, com a `CONVENCAO`, e `analytics/agent_system/CLAUDE.md`.
- `SISTEMA_AGENTES.md`:
    - I.III.xv (o modelo é o filtro de saída da análise, não ferramenta);
    - **III.III.vi** (a seção 6 "Sobre o modelo" de todo report, e as quatro propostas do segundo teste de PM, ainda a decidir);
    - IV.vi (consolidação) e IV.ix (as duas etapas: caminhos das exógenas e tempero).
- O ciclo 2026-10-27:
    - a seção 6 dos reports de rodada 1, rodada 2 e report final dos sete (`*_r1.md`, `*_r2.md`, `*_rf.md`);
    - `log.md` (as divergências com o modelo; por exemplo, expectativas contra a central da (E));
    - `P1.md`, `P2.md` e `PF.md`.

**Já pedido pelo usuário** (entra no quadro junto com o feedback):
- e. capturar o efeito não linear e o efeito sazonal no câmbio: o câmbio achou o resíduo da (F) positivo no 4º trimestre em 8 de 9 anos desde 2017;
- g. testar um modelo de juros com a taxa de câmbio embutida;
- h. uma métrica de crédito na curva IS (ligado ao agente de crédito do chat B);
- refazer a taxa neutra: a âncora `rr_10a` + meta da regra de juros, com uma suavização da taxa de 10 anos (propostas 1 e 3 de III.III.vi);
- a Selic de fechamento pela média de dois trimestres: reestimar a regra no fechamento?
- candidatos, se o feedback pedir: variáveis próprias para fiscal e externo, o modelo de PIB com a demanda do governo e o modelo do hiato (PLANO, "Anotado para depois").


## Passos

- **C1a. Juntar** a seção 6 dos 21 reports e os achados do log num quadro, com uma linha por proposta: o que é, quem pediu, a evidência no ciclo, o teste que decidiria, o custo e o impacto nos agentes.
- **C1b. Perguntar aos agentes.** Cada um dos sete (o subagente `<agente>-analyst`, Opus, em modo ad hoc) recebe o próprio report final de 2026-10-27 e um questionário curto:
    - onde o modelo complicou o trabalho;
    - em que equação;
    - o que mudaria;
    - que teste decidiria;
    - o que acontece com a tese se mudar.

  Só leitura dos arquivos do ciclo, sem dado novo. As respostas ficam em `analytics/brasil/structural_model/feedback_agentes/2026-10-30/<agente>.md`. Custo estimado: ~1M.
- **C1c. O usuário escolhe**, numa ou mais janelas, o que mudar e o que testar. Uma proposta por janela quando ela tiver alternativas.
- **C2. Implementar:** estimar, comparar com o modelo de hoje (erro fora da amostra), regerar o `Structural Model.html`, atualizar o `modelo.py` e a `CONVENCAO`, e rodar `tests/test_modelo_agentes.py`.
- **C3. Entregar:** a lista de impacto ao chat E (definições, templates, consolidação) e ao chat B, se crédito ou mercado de trabalho ganharem variável.

**Atenção:** `analytics/brasil/structural_model/` também é mexido por chats fora deste plano. Confira o `git status` antes de começar e não reverta o que não é seu.

**Escreve:** este arquivo, `analytics/brasil/structural_model/`, `analytics/agent_system/modelo.py` e os testes do modelo. **Não escreve:** a consolidação e as definições (chat E), os mapas (chat B), o SISTEMA (principal).

**Pronto quando:** as mudanças escolhidas estão implementadas e reestimadas, os testes passam, o painel foi regerado, o `modelo.py` devolve o que as definições esperam e E e B têm a lista de impacto. O feedback dos nove sobre o modelo novo vem na seção 6 do ciclo 2.


## Estado

- 2026-10-30 · **C1 em curso.** `git status` de `analytics/brasil/structural_model/`, `analytics/agent_system/` e dos testes do modelo: limpo (nada de outro chat pendente).
    - **Lido:** README, este brief, SISTEMA I.III.xv, III.III.i/vi, IV.ii/vi/ix, a seção 6 dos 21 reports (extraída para o scratchpad), a pauta e o encerramento da `ata_r2.md`, as divergências abertas do `log.md`, o PF, o PLANO e os títulos dos cinco `pendencias_*_eq.md`.
    - **C1b lançado antes do pedido de pausa do principal:** os sete `<agente>-analyst` (Opus, modo ad hoc) rodam em paralelo, em segundo plano. Modo ad hoc não escreve arquivo e o prompt proíbe G, banco e dado novo: só leem o RF, r1/r2, as entradas deles no log, a ata e o PF. Questionário: as cinco perguntas do brief mais a reação de cada um à lista de 19 propostas já na mesa (a–s). Custo estimado: ~1M, como no brief.
    - **Próximo, quando o principal liberar:**
        - gravar as sete respostas, literais, em `analytics/brasil/structural_model/feedback_agentes/2026-10-30/<agente>.md` (pasta nova);
        - C1a: o quadro, uma linha por proposta (o que é, quem pediu, evidência no ciclo, teste, custo, impacto), em `analytics/brasil/structural_model/feedback_agentes/2026-10-30/quadro.md`, cruzando com o que os `pendencias_*_eq.md` já mediram (vários itens já foram testados ou descartados lá: Brent em (II), clima em (IA), (IM) no livre, câmbio em (E), prêmio de maturidade em (H), separar prêmio na (R));
        - C1c: as janelas de escolha do usuário.
    - **Arquivos que C1 toca:** só esta pasta nova `feedback_agentes/` e este arquivo. Nenhum código, nenhum painel, nenhum commit.
- 2026-10-30 · **C1b feito.** As sete respostas estão gravadas, literais, em `analytics/brasil/structural_model/feedback_agentes/2026-10-30/<agente>.md`, com a liberação do principal. Sem commit.
    - **Custo real:** 1,06M. Por agente: câmbio 165k, externo 159k, PM 155k, inflação 153k, fiscal 145k, expectativas 143k, atividade 140k.
    - **Próximo:** o quadro C1a e as janelas C1c, que esperam a liberação do principal.
    - **Pedido do B (crédito na IS, desemprego no hiato):**
        - Crédito na IS: só a atividade toca nisso. A proposta 1 dela é um termo de demanda fora do juro na (H): impulso fiscal, impulso de crédito ou fluxo financeiro, e intercepto só se nenhum fechar. O fiscal e a inflação apoiam a mesma proposta pelo lado fiscal.
        - Desemprego no hiato: nenhum dos sete pediu.
        - Os dois vão como linha própria no quadro. Ainda não tenho posição.
        - Aviso que pesa no teste: segundo o B, `cred_fluxo_financeiro` está parado em 2026-04.
- 2026-10-30 · **C1a feito**, liberado pelo principal, sem subagente e sem commit: `analytics/brasil/structural_model/feedback_agentes/2026-10-30/quadro.md`.
    - O quadro tem 21 propostas. Cada uma foi cruzada com o que os `pendencias_*_eq.md` já mediram, e há uma recomendação por linha.
    - **Posição para o B** (depende da decisão 3): o crédito entra como candidato no teste do termo de demanda da (H); o desemprego fica fora do ciclo 2.
    - **C1c em curso:** por pedido do usuário, as decisões vão ao principal, não em janela daqui. Primeiro lote enviado: o item 1 (partida), o 2 (âncora) e o 3 (a IS, com a posição do B).
- 2026-10-30 · **Decisões 1–3 gravadas** (ver Decisões). Antes de rodar, o plano dos dois testes liberados (a âncora e o teste A do hiato) foi ao principal. Só inventário de dados até aqui: nenhum código, nenhum painel, nenhum commit.
    - **Inventário:**
        - **Vintages do hiato:** 21 edições em `pm_hiato_produto_vintages`, de 2021-09 a 2026-09. A revisão média contra a edição mais recente cai de 1,09 p.p. no trimestre da edição para 0,37 com 12 trimestres de idade, contando todas as edições. Contando só as edições desde 2024-09, cai a 0,04 com 12 trimestres, mas essa leitura tem viés para baixo: as edições recentes são as mais próximas da última.
        - **Insumos do hiato do BC:** PIB, taxa de desocupação ou de ocupação da PNAD, estoque do CAGED e NUCI da FGV (boxe do RPM de jun/2024 e eqs. 6–9 do modelo agregado). A suíte de modelos usa ainda o estoque de capital e o núcleo Ex-0, e o número publicado incorpora julgamento do Copom.
        - **NUCI:** não está no banco. Existe em cache da IPEADATA (`modelo_agregado/data/modelo_nuci_fgv.csv`, até 2026-07) e no SGS 24352.
        - **Vintages do PIB:** não estão no banco.
        - **QPC:** o juro neutro tem 10 leituras semestrais, de 2021-08 a 2026-06. Não sustenta uma estimação desde 2006.
    - **Próximo:** esperar o principal liberar o plano, e as duas perguntas dele: o QPC como gabarito com a Focus de 5 anos como série histórica, e o prêmio na (H).
- 2026-10-30 · **Os dois testes rodaram**, com liberação do principal. Código e números em `analytics/brasil/structural_model/experimentos/{ancora,hiato}_2026-10-30/` (`RESULTADOS.md` em cada pasta). Nenhuma equação, painel ou `modelo.py` mudou. Sem commit.
    - **Âncora:**
        - A MM4 passa o critério na leitura do simulador: Selic −23/−6/−2%, hiato +2/+5/−6% em h1/h4/h8. Na leitura condicional ao caminho realizado da NTN-B, falha (Selic h8 +8%, hiato h8 +11%).
        - A MM8 falha por pouco: hiato h4 +5,7%.
        - As variantes com o desvio na (H) falham, e o desvio sai com sinal oposto ao de custo de capital (t 0,3 e 0,5).
        - Em nenhuma variante o salto da NTN-B aperta o hiato: a Selic acompanha a âncora. A média móvel só atrasa a passagem: na MM4 entra 0,25 no trimestre e o resto em 4.
    - **Hiato A:**
        - (a) R² 0,865, mas só NUCI e desocupação contam. Os coeficientes caem à metade entre 2004–14 e 2015–23, então o critério de estabilidade falha.
        - (b) Nas idades 0–2 o ganho médio fica entre 26% e 33%, na fronteira dos 30%. De 6 trimestres em diante a regressão é pior que o BC.
        - (c) Sinal de 2022T4–2024T1: o BC acertou 0 de 12, a regressão 8 ou 9 de 12.
        - Hoje a regressão dá ~+1,5 contra +0,4–0,6 publicado. A diferença é a desocupação de 5,4%, abaixo do mínimo do treino (6,67%), ou seja, a pergunta da NAIRU.
    - **Custo real:** ~300k, estimado pelo tamanho da sessão (não há medidor). Abaixo dos ~600k liberados, porque o subagente da Focus saiu.
    - **Próximo:** as decisões do usuário, via principal.
- 2026-10-30 · **PDF dos testes entregue**, a pedido do usuário: `analytics/brasil/structural_model/experimentos/Testes do Modelo Estrutural - ancora e hiato.pdf`, 9 páginas, 7 gráficos.
    - **Gerador:** `experimentos/relatorio_testes_2026-10-30/gerar_pdf.py`, no padrão do FX Outlook. Todos os números saem das funções dos dois testes na geração (~2 min).
    - **Correção de número:** a redução de erro nos três trimestres mais recentes é de **28% a 35%** quando o erro é medido sobre os casos juntos, e não 26–33%, que era a média dos ganhos por idade.
    - **Custo:** ~120k. Nos testes e no PDF, ~420k ao todo.
    - **Decisões A, B e C abertas** até o usuário ler.
- 2026-10-30 · **Decisões adiadas pelo usuário, retomam antes do ciclo 2.** Âncora, hiato e neutro pedem análise cuidadosa, e o usuário decide quando afinarmos o modelo para o ciclo 2 (repassado pelo principal).
    - Nada novo roda. O PDF e os dois experimentos ficam como estão.
    - O lote seguinte do quadro também espera: a faixa com o erro das equações, a sazonalidade do câmbio, a vol implícita e a âncora das expectativas.
    - Também esperam o D1 (condicionar o primeiro trimestre), a implementação C2 e as listas de impacto C3.
    - **C fica disponível**, sem trabalho em curso.
- 2026-10-30 · **Lote de decisões preparado**, a pedido do usuário via principal, sem rodar nada: `analytics/brasil/structural_model/feedback_agentes/2026-10-30/decisoes_pendentes.md`.
    - Cada decisão tem a pergunta em palavras simples, o impacto de cada opção (na Selic, na inflação, no câmbio, nos agentes e no custo), a recomendação em uma linha e um exemplo real.
    - Lote 1 (A, B, C): os dois testes do PDF.
    - Lote 2 (itens 4–7 do quadro): a faixa, a sazonalidade do câmbio, a vol da B3 e a âncora da expectativa.
    - O que está marcado como "conta" sai das elasticidades já medidas, sem rodar o modelo.
    - Lote 3, a pedido do usuário: item 10, o S&P na equação do câmbio.
        - O principal foi avisado de que a alta do S&P enfraquece o real pela equação (coeficiente +1,90), e não o aprecia, como dizia o ponto de partida vindo do E.
        - O principal respondeu que o erro foi dele, ao resumir. A definição do externo já diz o certo, então não há nada a avisar ao E.

## Decisões

Respostas literais do usuário, repassadas pelo principal em 2026-10-30. Numeração do quadro (`feedback_agentes/2026-10-30/quadro.md`).

- 2026-10-30 · **1. Ponto de partida:** "Condicionar (Recommended)". Entra depois dos testes da âncora e do hiato, por ordem do principal.
- 2026-10-30 · **2. Âncora da (R) e da (H):** "Faça o teste com o QPC e com o de 10 suavizado em 4 e 8 trimestres". Liberado; o plano vai ao principal antes de rodar.
- 2026-10-30 · **3. A (H):** o usuário reabriu o desenho. Em vez do termo de demanda, primeiro o hiato:
    - a. Regredir o hiato publicado pelo BC, no trecho em que as revisões já são pequenas (ele estima uns 3 anos atrás), contra PIB, CAGED, taxa de desemprego e NUCI (e o que mais o BC usar). Com isso, o hiato dos trimestres recentes passa a sair dos dados já observados, como estimativa do hiato final.
    - b. Se o teste A der certo, estimar os próprios regressores (PIB, desemprego, NUCI, CAGED).
    - "Faça o teste A, e depois retorne com os resultados." Liberado; o plano vai ao principal antes de rodar.
    - O termo de demanda fora do juro (impulso fiscal, crédito, rp_hat, intercepto) fica parado até o resultado do hiato.
- 2026-10-30 · **2, detalhe:**
    - Pergunta 1: "Tirar o QPC".
    - Pergunta 2: "Sim, variante extra (Recommended)".
    - Como o principal fechou o teste:
        - sem série de neutro, o prêmio é o desvio do 10 anos cru contra a própria média móvel;
        - variantes: (0) hoje; (1) MM4; (2) MM8; (1b/2b) a MM como âncora e o desvio como regressor na (H);
        - a âncora sem subagente;
        - os dois testes liberados, com os critérios propostos;
        - ~600k no total, código só em `experimentos/`, sem commit.
- 2026-10-30 · **Resultado dos testes (decisões A, B e C), respostas literais:**
    - A (âncora): "Cara eu quero um relatório simples em pdf apresentando o resultado dos testes. Coloque grafico tabelas e com boa explicação."
    - B (hiato): "Ver resposta anterior"
    - C (neutro): "Mostrar os resultados no relatório e apresente tambem a alternativa"
    - Ordem do principal:
        - um PDF no padrão do FX Outlook, com os dois testes e, como próximos passos, o neutro pela Focus com o prêmio na IS e a NAIRU que anda no tempo, cada um com o que testaria e o custo;
        - nada roda das alternativas;
        - o PDF fica em `experimentos/`, sem commit;
        - **as três decisões ficam abertas até o usuário ler.**

## Pedidos
