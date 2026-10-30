# Chat A — Desenho do ciclo e do moderador

**Objetivo.** Redesenhar o ciclo com o usuário: um report 1 mais enxuto, uma **conversa com moderador no lugar das rodadas**, e o papel do moderador bem definido. É a frente que mais precisa do usuário: o trabalho é conversa e decisão, e o texto vem depois.

**Ler primeiro:**
- `README.md` desta pasta (as regras dos chats).
- `SISTEMA_AGENTES.md`: III.III.i (formato do report), **III.III.ii (fluxo, registro e o teste do moderador e da ata)**, IV.ii (principal e subordinado; a regra de quem não tem papel numa exógena), IV.iii (número de rodadas), IV.vi (consolidação P1, P2, PF*), IV.vii (escrivão).
- O ciclo 2026-10-27, em `obsidian/ciclos/2026-10-27/`:
    - `log.md`: o fluxo real e o custo de cada etapa;
    - `ata_r2.md`: o teste do moderador, com as mensagens literais;
    - `cobrancas.md` e `relatorio.md`;
    - um par de reports para sentir o peso, por exemplo `cambio_r1.md` e `cambio_r2.md`.
- Os templates `obsidian/ciclos/_modelo_report.md` e `_modelo_log.md`, e `obsidian/escrivao/manual_do_escrivao.md`.


## O que precisa do usuário, em ordem

Cada item fecha numa janela de escolha, com a opção recomendada primeiro, depois de uma conversa curta quando o item pedir.

1. **O ciclo de ponta a ponta.** Partir do desenho de hoje (rodada 1 → P1 → rodada 2 → P2 → report final → PF* → relatório) e do teste do moderador. A decidir: as etapas, o que cada agente lê em cada uma, o que fica fixo no ciclo e onde entram o agente web e as consolidações.
2. **O report 1 enxuto** (ideia do usuário, 2026-10-27). A rodada 1 parte do ciclo anterior, faz as análises iniciais (o que mudou, como a tese se desenrolou desde então, o placar) e termina nos pedidos ao agente web e aos outros agentes. A decidir:
    - o que sai do report de hoje e o que fica;
    - o que faz o agente que não tem ciclo anterior (os dois novos, no ciclo 2);
    - se o P1 continua existindo e com que caminhos.
3. **A conversa com moderador no lugar da rodada 2.** A decidir:
    - a pauta, as voltas e quem fala com quem;
    - o limite de voltas e como a conversa termina;
    - o que cada agente escreve depois (caminhos, report final) e se ainda há P2.
4. **O papel do moderador.** Já decidido: não decide o mérito (é do principal da exógena ou do dono da variável), não muda número, e tudo fica na ata, literal. A decidir:
    - quem é: um agente próprio (Opus) ou a sessão que conduz o ciclo, como no teste;
    - quem monta a pauta, e se o usuário a vê antes;
    - os poderes: chamar um agente que não está na divergência, pedir notícia ao agente web no meio da conversa, exigir resposta a uma pergunta, encerrar um item, escalar ao usuário;
    - o critério de "resolvido";
    - a relação com o principal e os subordinados das exógenas e com o escrivão;
    - o que ele lê e como é avaliado.
5. **Os pontos da leitura do ciclo 2026-10-27** (notas do usuário, saídas do PLANO):
    - a. o escrivão precisa sintetizar bem: a leitura dos reports está pesada;
    - b. a parte "o que derrubaria a tese?" precisa ficar melhor;
    - c. como o agente sem papel numa exógena calibra o upside e o downside dela (a regra do base está no SISTEMA IV.ii);
    - d. como o ciclo incorpora o ciclo passado (provavelmente resolvido no item 2);
    - f. o câmbio sempre testa o cenário com o juro da curva e com o da Focus, e pede o tempero à PM;
    - a ordem de escrita (ideia de 2026-10-22: o segundo agente lê o report do primeiro), provavelmente absorvida pela conversa.
6. **A medição do ruído** (rodar a mesma etapa duas vezes no ciclo 2): sim ou não.
7. **O custo.** No ciclo 2026-10-27, com sete agentes, foram ~8–9M (o `log.md` tem o custo de cada agente). Com nove agentes e conversa, que teto?

**Restrição técnica para o desenho:** um subagente não dispara outro. A conversa é orquestrada pela sessão que conduz o ciclo: ela retoma cada agente com o contexto (`SendMessage` para o agente da etapa anterior) e entrega a mensagem do moderador. Se o moderador for um agente, ele devolve a próxima mensagem e o destinatário, e a sessão entrega. Cada retomada custa: no report final de 2026-10-27 foram ~90–110k por agente.


## Passos

- **A1.** A conversa e as decisões dos itens 1–7, registradas abaixo em "Decisões".
- **A2.** Escrever, com a aprovação do usuário:
    - o template do report 1 e o do report final (`_modelo_report.md`);
    - o template da ata e o do log;
    - a definição do moderador (`.claude/agents/moderador.md`), se ele for um agente;
    - o que mudar no manual e na definição do escrivão.
- **A3.** Entregar ao chat E, em "Pedidos", a lista do que muda nas definições dos sete agentes, na consolidação e no agente web, e ao chat C o que muda no que é consolidado e quando.

**Escreve:** este arquivo, os templates do ciclo, `.claude/agents/moderador.md`, o manual e a definição do escrivão. **Não escreve:** as definições dos analistas, a consolidação e o motor (chat E), o SISTEMA (principal).

**Pronto quando:** as decisões estão no SISTEMA (pelo principal), os templates e o moderador estão aprovados pelo usuário, e E e C têm a lista do que mudar.


## Estado

(vazio: o chat começa aqui)

## Decisões

## Pedidos
