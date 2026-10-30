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

(vazio: o chat começa aqui)

## Decisões

## Pedidos
