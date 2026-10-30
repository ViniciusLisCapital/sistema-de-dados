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

- 2026-10-30, abertura (só leitura, à espera do ok do principal). Lidos: README, este brief, `P_principal.md`, SISTEMA III.III e IV.
  - **Plano do A1.** Terminar a leitura (`log.md` nas partes de fluxo e custo, `ata_r2.md`, `cobrancas.md`, o começo do `relatorio.md`, `cambio_r1/r2`, os dois templates, o manual do escrivão, e o feedback dos sete ao modelo em `structural_model/feedback_agentes/2026-10-30/` só no que toca o ciclo). Depois, os itens 1–7 do brief em ordem, cada um com uma proposta curta em prosa e uma janela de escolha, recomendada primeiro. Itens que dependem um do outro (1 → 2 → 3 → 4) vão em sequência; 5–7 podem ir juntos no fim. Cada janela espera o ok do principal antes de ir ao usuário.
  - **Arquivos que o A1 toca:** só este (`Estado`, `Decisões`, `Pedidos`). Nada nos templates, no escrivão ou no moderador até o A2.
  - **Custo estimado do A1:** sem subagente. Só o contexto desta sessão, ~0,4–0,6M (a leitura do ciclo é ~0,3M; a conversa, o resto). O A2 deve sair também sem subagente (~0,2–0,3M). Se o usuário quiser um teste do moderador novo antes do ciclo 2, ele custaria uma rodada de conversa, ~1–1,5M, e seria decidido no item 7.
- 2026-10-30, leitura feita (ata_r2, custos do log, cobranças, templates, notas a–h do PLANO antigo, feedback dos sete no que toca o ciclo). Rascunho do item 1 pronto e mostrado ao usuário em texto, sem janela. Aviso o principal por SendMessage; as janelas esperam o ok dele.
  - Números que o desenho usa (log): r1 ~1,97M (sete, 248–345k cada); r2 ~2,48M; moderação ~63k de réplicas mais o moderador (não medido); RF ~0,67M retomando (86–110k cada); web ~0,5M em duas demandas; escrivão 534k + 94k.
  - Achado que pesa no item 1: a única mudança de caminho no RF (`rr_10a` do 4T26, 7,72 → 7,75, fiscal) gerou as cobranças C1 e C2. Argumento para congelar os caminhos no fim da conversa.

- 2026-10-30, **A1 fechado.** Todas as decisões dos itens 1–7 estão abaixo, com as respostas do usuário vindas pelo principal. Custo: só o contexto desta sessão, sem subagente. Próximo: A2, liberado nos arquivos de A, sem commit; cada texto vai ao principal com um resumo do que mudou.
- 2026-10-30, **A2 escrito, à espera da aprovação do usuário** (via principal). Sem commit, sem subagente.
  - `obsidian/ciclos/_modelo_report.md`: reescrito como template do R1, com três etapas (R1, R1 final e atualização) e sete seções.
  - `obsidian/ciclos/_modelo_ata.md`: novo.
  - `obsidian/ciclos/_modelo_log.md`: reescrito no fluxo novo.
  - `.claude/agents/moderador.md`: novo, Opus.
  - `obsidian/escrivao/manual_do_escrivao.md` e `.claude/agents/escrivao.md`: ajustados ao R1 e à ata, com a regra "dizer uma vez".
  - Escolha de A em aberto para o usuário: um argumento "Mantido" entra como o R1 o escreve, sem buscar o texto no relatório anterior.
  - Próximo: A3, a lista para E e para C, depois da aprovação.
- 2026-10-30, **A2 e A3 fechados; frente A fechada** (principal). Disponível para reabrir. **A2 fechado**: o usuário aprovou os cinco textos (via principal). Um ajuste depois da aprovação, para seguir a decisão 1.1 ao pé da letra ("o moderador consolida as demandas web e despacha o web agente"): o moderador ganhou o modo `d1`. Nele, junta os pedidos dos R1 numa demanda D1 e agrupa as perguntas entre agentes por destinatário. A ata ganhou a seção "D1 e perguntas entre agentes", e o log, a linha correspondente. A3 escrito em Pedidos.

## Decisões

- **2026-10-30, item 1.1 — o fluxo do ciclo** (desenho do próprio usuário, no lugar das opções; resposta literal, via principal):
  > "Como eu quero organizar o ciclo:
  > 1.) Os agentes começam lendo o ultimo relatório final (RFt-1) (e outras informações do ciclo, caso necessário);
  > 2.) Os agentes fazem um relatório R1, com anotações das principais mudanças em relação ao RFt-1, quais dados saíram e como eles confirmam ou mostram um cenário diferente do RFt-1. Somado a isso, agente faz as primeiras demanda para o agente web.
  > 3.) Quando todos os agentes terminarem o R1 e o D1 (D1 demanda de web search), o moderador consolida as demandas web e despacha o web agente.
  > 4.) Com o retorno do web agent, os agentes recebem as respostas e finalizam o R1.
  > 5.) O moderador começar o processo de convergência, conversando com todos os agentes e afunilando as premissas e provocando discussões para afinamento dos cenários. Durante essa discussão, caso os agentes demandem mais informações web, ela é consolidada ao final, a discussão para e o agente web é despachado novamente.
  > 6.) Quando os agentes encontrarem todos os pontos de convergência nas premissas e cenários, os R1 são enviados para o escrivão consolidar no relatório final.
  > 7.) Lembrando, o papel do escrivão é garantir a organização ótima em boa linguagem do material.
  > No final, eu quero impor uma estrutura para o relatório final (acredito que isso está no plano)."
  - Em resumo: R1 (mudanças contra o RFt-1) + D1 (demanda web) → web, despachado pelo moderador → R1 finalizado → convergência conduzida pelo moderador, com novas demandas web consolidadas e despachadas em pausas → os R1 vão ao escrivão. Sem rodada 2 e sem report final por agente.
  - Em aberto, mandado ao principal como decisões (não preenchido por A): onde o Modelo Estrutural roda; o que é o RFt-1; se o R1 é atualizado depois da convergência; caminhos congelados; a estrutura do relatório.
- **2026-10-30, item 1.2 — caminhos congelados depois da conversa:** "Veja a resposta da questão anterior". Reaberta como 1.6 (caminhos congelados quando a convergência fecha), no fluxo novo.
- **2026-10-30, item 1.3 — onde o Modelo Estrutural roda** (literal): "Acho bom deixar o inicio e final como padrão, mas os agentes podem rodar os modelos em qualquer momento da discussão, as vezes para provar um ponto ou testar o impacto de uma premissa."
  - Consequência: duas rodadas padrão da consolidação, uma com os caminhos do R1 final (a mesa comum da conversa) e outra quando a convergência fecha (a central do relatório). Durante a conversa o agente roda o modelo como ferramenta de argumento, por um G, e isso não muda a central, que sai só da rodada do fim.
- **2026-10-30, item 1.4 — o que é o RFt-1:** "Relatório + próprio R1 (Recommended)". O agente começa lendo o relatório do escrivão do ciclo anterior (o cenário conjunto) e o próprio R1 do ciclo anterior (o detalhe da área: temperos, caminhos das caudas, "Sobre o modelo").
- **2026-10-30, item 1.5 — o R1 depois da convergência:** "Atualização curta (Recommended)". Cada agente é retomado com o contexto e atualiza o R1 no que a conversa mudou (tese, caminhos, probabilidades), com uma linha por mudança. O escrivão lê os R1 atualizados, com a ata só como referência.
- **2026-10-30, item 1.6 — caminhos depois da convergência:** "Não, vale o combinado (Recommended)". O que fechou na conversa vale até o relatório, e o modelo final roda com isso; a atualização curta do R1 (1.5) não muda premissa, e a mudança fica para o próximo ciclo.
- **2026-10-30, item 2.1 — o que o R1 contém** (literal): "Atualização completa. Não entendi a duvida com o Escrivão. O Escrivão recebe os reports individuais dos agentes no no final de todo o ciclo para formatar e organizar tudo num unico relatório." O R1 é uma atualização completa: (1) o que mudou e o placar; (2) a tese com todos os trimestres, antes → agora; (3) a argumentação só onde mudou, o mantido em uma linha por item; (4) caminhos (JSON) e temperos em tabela, ficha só para o novo ou mudado; (5) pedidos (D1 e aos outros agentes); (6) "Sobre o modelo". O escrivão formata e organiza os R1 finais num relatório só; não há questão aberta sobre ele.
- **2026-10-30, item 2.2 — os dois agentes novos:** "Completo (Recommended)". No ciclo 2, mercado de trabalho e crédito escrevem um R1 completo, no formato de hoje, com o relatório anterior como contexto; do ciclo seguinte em diante, R1 de atualização.
- **2026-10-30, item 2.3 — perguntas entre agentes:** "perguntas no R1 final (Recommended)". Cada agente recebe, junto com as respostas da web, as perguntas que os outros lhe fizeram no R1, e responde no R1 final. A conversa fica para o que continuar divergente.
- **2026-10-30, item 3.1 — o que o moderador leva à conversa** (literal): "EU concordo com a sua recomendação, só quero deixar bem claro. O moderador é um provocador, ele questiona premissas, stress ainda mais cenários, tenta levar as coisas ao limite, procurando mapear todos os riscos. Ele pode inclusive, questionar o principal de um exógena e recomendar que a opnião do subordinado tem mais fundamentação. Ele é a central da lógica e da razão. A ideia é depois alimentá-lo com bastante eventos históricos de todas as variaveis para que ele possa ter mais capacidade imaginativa para pensar cenários não discutidos pelos agentes das areas."
  - Pauta: divergências, cenários que não batem entre si e os stresses que o próprio moderador propõe.
  - Muda a regra do teste ("o moderador não opina sobre o mérito"): agora ele questiona premissas e pode recomendar o lado com mais fundamento, inclusive o do subordinado contra o principal. A palavra final continua com o dono da premissa (SISTEMA IV.ii); o moderador recomenda, não decide.
- **2026-10-30, item 3.2 — como a mensagem circula** (literal): "Sigo sua recomendação. Contudo, tudo deve ser pesado em termos de premissas e conclusão, e o moderador tambem é responsável por garantir que argumentos "porque sim" passem." (Leitura do principal, confirmada pelo contexto: garantir que argumentos "porque sim" **não** passem.)
  - Um a um, pelo moderador. Cada argumento é lido como premissas → conclusão, e o moderador devolve o que não tem premissa sustentada.
- **2026-10-30, item 3.3 — quem entra em cada assunto** (literal): "Nesse caso, outras areas podem ser chamadas como testemunha, mas se elas não possuem expertise na exogena, a opinião dele não deveria ser requerida. Vou usar o seu exemplo. No caso de entender o juros está restritivo ou não (suponha que Fiscal e PM discordem quanto a isso), o agente da atividade pode ser chamado, e ele poderia dizer "Olha, os dados de atividade estão sentido o impacto do juros, o PIB está crescendo, mas são coisas acíclicas, pois as coisas sensíveis ao juros está sofrendo bem". Ou seja, ele pode fortalecer ou enfraquer evidencias num argumento."
  - Os lados e o dono; o moderador chama outra área como **testemunha**, que traz evidência da própria área para fortalecer ou enfraquecer um argumento e não dá opinião sobre a exógena.
- **2026-10-30, item 3.4 — como um assunto termina** (literal): "Por hora, o dono decide em até 2 voltas. Quero deixar registrado que em algum momento no futuro, o moderador será o economista chefe que continuará com as funções de moderador, mas decidirá divergencia tambem. Deixe registrado por enquanto."
  - O dono da premissa dá a palavra final em até duas voltas por assunto; sem acordo, "divergência registrada", com o fato que a decidiria. Nenhum limite total de voltas foi fixado.
  - Futuro: o moderador vira economista-chefe, que modera e também decide divergências (em Pedidos, para o plano).
- **2026-10-30, item 4.1 — quem é o moderador:** "Agente próprio, Opus (Recommended)". Agente com definição própria (`.claude/agents/moderador.md`, A2); a sessão que conduz o ciclo só entrega as mensagens.
- **2026-10-30, item 4.2 — a pauta antes da conversa:** "No ciclo 2 sim, depois não (Recommended)". No ciclo 2 o usuário vê a pauta e pode acrescentar ou cortar assuntos; depois, só na ata.
- **2026-10-30, itens 4.3 e 4.4 — o moderador roda o modelo; o que só o usuário resolve** (literal): "Roda; Por enquanto, pode levar para a ata. Isso conversa com o que falei na decisão A". O moderador roda o modelo para estressar cenários (o número é provocação, não premissa); o que só o usuário resolve vai para a seção "Para o usuário" da ata, sem parar a conversa, até existir o economista-chefe (3.4).
- **2026-10-30, leitura do moderador (padrão proposto por A, sem objeção do usuário):** os R1 finais de todos, o P da abertura, o relatório e a ata do ciclo anterior, e os mapas conceituais por trecho. É avaliado pela ata literal.
- **2026-10-30, itens 5–7** (o usuário escolheu todas as recomendadas):
  - 5.a, leitura pesada — "Dizer uma vez": regra nova do escrivão, o mesmo fato é dito uma vez, no lugar em que pesa mais, e as outras seções só o citam; releitura depois do ciclo 2.
  - 5.b, o que derrubaria a tese — "Formato fixo + teste": 2 ou 3 itens por tese, cada um com o que observar, direção, até quando e o que muda (qual cauda, quanto de probabilidade); o moderador testa cada um na conversa.
  - 5.c, caudas de exógena sem papel — "Usa as caudas do dono": o agente usa os caminhos de upside e downside do principal, que passam a ir no arquivo de caminhos (pedido ao E).
  - 5.d, como o ciclo incorpora o anterior: resolvida por 1.4 e 2.1. A ordem de escrita foi substituída pela conversa.
  - 5.f, câmbio e juro — "Fixo no R1 do câmbio": o câmbio roda o cenário com a Selic do modelo, a da curva e a da Focus; se a diferença for grande, pergunta à PM pelo caminho da 2.3.
  - 6, ruído — "Câmbio e PM, 2x": o R1 do câmbio e o da PM rodados duas vezes no ciclo 2 (~0,6M).
  - 7, teto — "10M": a sessão que conduz o ciclo 2 para e pergunta ao usuário ao chegar a 10M.
- **2026-10-30, o "Mantido" no relatório:** "Não, usa a linha do R1". Um argumento que o R1 marca "Mantido" entra no relatório como o R1 o escreve, em uma frase; o escrivão não o busca no relatório anterior.
- **2026-10-30, A2 aprovado pelo usuário:** os templates do R1, da ata e do log, `moderador.md`, o manual e `escrivao.md`.
- Consequência prática (não decisão): no ciclo 2, o "próprio R1 anterior" dos sete é o RF de 2026-10-27.
- **2026-10-30, item 1.7 — a estrutura do relatório:** "Manter sem teto". Fica a estrutura de SISTEMA IV.vii (2026-10-22; manual do escrivão, seção 13), sem limite de tamanho. A nota a (leitura pesada) continua em aberto no item 5, pelo lado da síntese do escrivão, não por teto.

## Pedidos

- **2026-10-30 → principal, para o plano (trabalho futuro, fora do ciclo 2):** uma base de eventos históricos de todas as variáveis para o moderador, que lhe dê capacidade imaginativa para pensar cenários que os agentes das áreas não discutiram (usuário, item 3.1). Candidato a "Anotado para depois" do PLANO; quem constrói fica a definir (provavelmente D, como conhecimento do moderador).
- **2026-10-30 → principal, para o "Anotado para depois" do PLANO:** o moderador vira **economista-chefe**: continua moderando e passa a decidir divergências e o que hoje vai para "Para o usuário" na ata (usuário, itens 3.4 e 4.4). Até lá, decide o dono da premissa.
- **2026-10-30 → E (decisão 5.c):** o arquivo de caminhos (`caminhos/<agente>_<etapa>.json`, contrato na docstring de `consolidacao.py`) passa a levar, além do caminho base, os caminhos de **upside** e **downside** de cada exógena de que o agente é principal. A consolidação continua usando só o base; as caudas são lidas pelos agentes sem papel naquela exógena. Incluído no A3 → E, item 2.

- **Nota para a lista do A3 (incluída no A3 → E, item 3):** a 1.3 não pede engenharia nova a E. Os agentes já rodam `modelo.rodar(sim, caminhos=..., mult=...)` por G (definição do câmbio, l. 251; o fiscal fez isso na moderação de 2026-10-27). O que muda é texto: a definição de cada analista, no modo conversa, diz que pode rodar o modelo para provar um ponto, que o G entra no log e que o resultado não é a central. Vai na lista do A3 para E.

### A3 → E: o ciclo novo nas definições, na consolidação e no web (2026-10-30)

Entrada do E2. Os textos de referência, aprovados pelo usuário, são `obsidian/ciclos/_modelo_report.md` (R1), `_modelo_ata.md`, `_modelo_log.md` e `.claude/agents/moderador.md`. As decisões estão em "Decisões", acima.

**1. O fluxo que a sessão conduz** (decisão 1.1 e seguintes). Hoje ele não está escrito em lugar nenhum como procedimento. Pede-se a E que o escreva onde ficar o procedimento do ciclo (o principal diz onde):
   1. R1 dos nove, em paralelo, a partir do relatório e do próprio R1 do ciclo anterior. No ciclo 2, o "R1 anterior" dos sete é o `<agente>_rf.md` de 2026-10-27, e mercado de trabalho e crédito escrevem R1 completo.
   2. Ruído (só no ciclo 2): câmbio e PM rodam o R1 uma segunda vez, com agentes novos e as mesmas entradas, em `<agente>_r1b.md` e `caminhos/<agente>_r1b.json`. Fora do fluxo: ninguém lê, a consolidação ignora, e a comparação vai para o log.
   3. Moderador, modo `d1`: devolve a demanda D1 e as perguntas entre agentes por destinatário.
   4. Agente web, modo demanda, com a D1 (`noticias/demanda_d1.md`).
   5. R1 final: cada agente é retomado (SendMessage) com as notícias dele e as perguntas que lhe fizeram.
   6. P1: consolidação com os `caminhos/<agente>_r1.json` do R1 final.
   7. Moderador, `pauta`. No ciclo 2, a sessão mostra a pauta ao usuário e devolve a resposta literal.
   8. Voltas. A sessão entrega cada bloco `PARA: <agente>` ao agente retomado, junta as respostas literais e retoma o moderador com elas. Num `PAUSA WEB · Dn`, roda o web com a demanda e retoma o moderador com o arquivo. Num `ENCERRADA`, segue.
   9. PF\*: consolidação com os caminhos fechados.
   10. Atualização: cada agente é retomado com o PF\* e o encerramento da ata. Não muda caminho, e registra a etapa "conversa" na seção 7, mesmo quando nada mudou.
   11. A consolidação roda de novo, para o `PF.json` levar as teses atualizadas. Com os caminhos congelados, a central tem de sair igual à do passo 9: vale um assert.
   12. Escrivão, como hoje (com cobranças e retomada).
   - Teto de 10M (decisão 7): a sessão soma o custo por etapa no log e para quando chegar ao teto.

**2. Arquivo de caminhos e consolidação** (`consolidacao.py`, `tests/test_consolidacao.py`):
   - nome `caminhos/<agente>_r1.json`, um por agente, atualizado no R1 final e durante a conversa (quando o principal muda); depois do encerramento, não muda mais;
   - contrato: além do caminho **base**, os caminhos de **upside** e **downside** de cada exógena de que o agente é principal (decisão 5.c). O P usa só o base; o validador aceita e confere as caudas;
   - não há mais P2: a consolidação roda no P1 (abertura) e no PF\* (fechamento, mais a nova rodada depois da atualização, passo 11);
   - a consolidação ignora `*_r1b.json`.

**3. As definições dos analistas** (os sete; os dois novos são de B, com o mesmo texto):
   - modos: `r1` (atualização ou completo), `r1-final` (notícias e perguntas recebidas), `conversa` (responde ao moderador) e `atualizacao` (depois do PF\*). Saem as rodadas 1, 2 e o report final;
   - o que lê no `r1`: o relatório e o próprio R1 do ciclo anterior (decisão 1.4), mais o que lê hoje;
   - o template é o `_modelo_report.md` novo: tabelas inteiras, texto só onde mudou, "Mantido: …, porque …", "O que derrubaria a tese" no formato fixo (decisão 5.b), a seção 7;
   - exógena sem papel: usa os três caminhos do principal e não escreve caminho próprio (decisão 5.c);
   - no modo `conversa`:
     - responde no formato das regras da ata, com premissa → conclusão;
     - pode rodar o modelo por G para provar um ponto; o G entra no log e o resultado não é a central (decisão 1.3);
     - se é dono da premissa e muda, atualiza o JSON e o R1;
     - como testemunha, traz evidência da própria área e não opina sobre a premissa em discussão (decisão 3.3);
     - pedido de notícia vem como "Pedido ao web:";
   - no modo `atualizacao`: não muda caminho (decisão 1.6); a central é a do PF\*;
   - câmbio, fixo no R1: roda o cenário com a Selic do modelo, a da curva e a da Focus; se a diferença for grande, pergunta à PM pela seção 5 (decisão 5.f).

**4. O agente web** (`web.md`):
   - a demanda passa a chegar consolidada pelo moderador (D1) e em pausas da conversa (D2, D3…);
   - arquivos `noticias/demanda_d<n>.md`;
   - o modo pauta continua desligado.

**5. Fica com A, já feito:** `moderador.md`, `escrivao.md`, o manual e os templates.

### A3 → C: o que muda no que é consolidado e quando (2026-10-30)

- O modelo é usado em quatro momentos:
  - P1, com os caminhos do R1 final;
  - as rodadas livres dos agentes e do moderador durante a conversa, sempre por G, sem mudar a central;
  - o PF\*, com os caminhos fechados;
  - a nova rodada depois da atualização, com a mesma central.
- Não há mais P2. O modelo fica fixo no ciclo 2, como o F(A) (PLANO).
- O moderador também roda `modelo.carregar/listar/rodar` para testes de estresse; nada novo na interface.
- A coluna "Antes" da tese do R1 sai do R1 anterior, não do modelo, então C não precisa guardar vintages da central.
- Uma consequência do feedback dos sete que passa pela conversa: assuntos de "agente contra modelo" (ex.: a (E) abaixo da pesquisa, a Selic do modelo baixa para a PM) não entram na pauta como divergência entre agentes. Ficam no tempero e na seção 6 do R1 e chegam a C pelo caminho de hoje (III.III.vi).

- 2026-10-30 (principal): as decisões de A estão no SISTEMA, em III.III.viii. O procedimento do ciclo vai para uma skill nova, `.claude/skills/ciclo/SKILL.md` (`/ciclo`), de dono E; o item 1 do A3 → E vai para lá.
