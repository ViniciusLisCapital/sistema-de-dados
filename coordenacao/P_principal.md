# Chat principal — Coordenação do Plano 2

**Papel.** O ponto de contato do usuário com o plano inteiro. Não faz o trabalho das frentes:
- abre as ondas;
- lê o arquivo de cada chat;
- leva as decisões ao `SISTEMA_AGENTES.md`, do qual é o único escritor;
- repassa os pedidos entre chats;
- libera as janelas de escrita compartilhada;
- mantém a tabela de status do `PLANO_AGENTES.md`.

Fica enxuto de propósito: se o contexto dele crescer, o principal novo começa por este arquivo.

**Ler primeiro:** `PLANO_AGENTES.md` (Plano 2), `README.md` desta pasta e o arquivo de cada chat (seções Estado, Decisões e Pedidos).


## Rotina

1. No começo de cada sessão, e quando o usuário pedir: ler Estado, Decisões e Pedidos de A–F.
2. **Decisões:** levar ao SISTEMA, na seção certa e em lista simples; marcar no arquivo do chat "integrada em <seção>".
3. **Pedidos:** repassar ao chat destinatário (avisar o usuário, ou `SendMessage` para a sessão local, `ListAgents`) e registrar abaixo.
4. **Passagem de onda:** conferir as entradas e liberar. São três:
    - os mapas de B aprovados → D2 e B2;
    - as decisões de A, as mudanças de C e o registro de B → E2;
    - tudo pronto → F.
5. **Janelas de escrita compartilhada:** por exemplo B nos mapas e nos módulos de dados dos sete (B3), enquanto ninguém mais mexe neles.
6. **Status:** atualizar a tabela do PLANO a cada passagem.


## Próximas ações

- **31/10: começar por [`ROTEIRO_2026-10-31.md`](ROTEIRO_2026-10-31.md).** Sem chats de frente: o principal conduz com subagentes.

### Próximas ações de 30/10 (superadas)

1. O usuário abre os chats A, B, C, D e E (onda 1), cada um com a frase de `README.md`.
2. Avisar o chat C de que `analytics/brasil/structural_model/` e o chat E de que `domain/release_calendar/` também são mexidos por outros chats, fora do plano (`git status` de 2026-10-30).
3. Integrar ao SISTEMA, quando chegarem, as primeiras decisões de A (o ciclo) e de B (as fronteiras).


## Estado

- 2026-10-30: Plano 2 escrito (`PLANO_AGENTES.md`) e esta pasta criada pelo chat anterior, que terminou com o handover. Todo o trabalho anterior está commitado (último commit do usuário: 9e31b46).
- 2026-10-30 12:17: principal novo aberto (handover lido). Nenhum chat de frente começou: Estado de A–E vazio, F fechado. PLANO, `coordenacao/` e a linha do CLAUDE.md da raiz ainda sem commit.

## Pedidos repassados

- 2026-10-30 → C: `analytics/brasil/structural_model/` também é mexido por chats fora do plano; olhar `git status` antes de editar e não commitar o que não é seu.
- 2026-10-30 → E: idem para `domain/release_calendar/` (M em calendar_2026.yaml e sync.py) e `jobs/atualizar_diario.py`.
- 2026-10-30, B → C: crédito na IS e desemprego no hiato do modelo revisto? (B precisa antes da janela 3, a variável da tese). Repassado por SendMessage.

## Canal (2026-10-30, pedido do usuário)

As decisões do usuário passam todas pelo principal: os chats mandam a pergunta por SendMessage, o principal pergunta numa janela e devolve a resposta literal. Os chats não abrem janela direto.

Até agora, à tarde: A gravou 1.1–1.7, 2.1–2.3, 3.1–3.3 (o ciclo desenhado pelo usuário, moderador provocador); B gravou as fronteiras (as 4 recomendadas) e as perguntas centrais (MT 5, crédito 6), e a janela 3 espera o C; C fez os testes da âncora e do hiato e o PDF, com decisões abertas até o usuário ler; D liberado com pente fino P1–P4 e na rodada 2 da Verde em inflação (a rodada 1 custou ~1,6M); E fechou a C6, a conferência e as 3 correções, tirou o CDS do passe diário, e a restauração do CDS espera aprovação direta do usuário na sessão E. O principal pôs `paths:` em `.claude/rules/lis-dashboards.md` (aprovado pelo usuário).

Mais tarde no mesmo dia:
- A fechou (A1–A3); decisões no SISTEMA III.III.viii; o procedimento vira a skill `/ciclo` (dono E).
- E2, parte de A, liberado (~1,1–1,4M), com o diagrama junto.
- CDS restaurado pelo principal com autorização do usuário: 6.423 linhas, até 26/10, 137,43; o ciclo 10-27 fecha.
- O usuário adiou as decisões do Modelo Estrutural (âncora, hiato, neutro; PDF em `structural_model/experimentos/`) para antes do ciclo 2: "antes de rodarmos o ciclo 2, afinamos o modelo estrutural". C parado.
- B liberado para os mapas, com a variável da tese provisória até o modelo.
- D: expectativas da Verde descartado; segue Kapitalo em externo.

## Pedidos pendentes de entrega (2026-10-30) — superada: os chats não voltam; tudo isto está no roteiro de 31/10

O usuário decidiu **retirar o agente de expectativas** (SISTEMA III.III.x). Redistribuição: à PM a Focus de IPCA e de Selic, a ancoragem, a inflação implícita, o QPC e a variável de tese (Focus IPCA 12m, endógena da equação de expectativas); à atividade a Focus de PIB; ao MT a de desocupação; ao câmbio a de câmbio. Ciclo 2 com oito agentes.

- **→ B:** a B3 abre no cenário 2 (a lista está em `B_novos_agentes.md`, "Plano da B3"), com a janela dos mapas e módulos dos sete exclusiva até o principal fechar. O escopo cresce: (a) o mapa da PM absorve o que o de expectativas tinha de próprio; (b) `dados/expectativas.py` sai e as declarações vão aos novos donos; (c) os espelhos que apontavam para expectativas. **Antes de escrever:** plano no formato novo, com custo e as decisões do usuário (provável: a PM com duas teses, Selic e Focus IPCA 12m, ou a tese de expectativas só como central do modelo). Separar o que é do E e as linhas do SISTEMA (do principal).
- **→ E:** depois do plano do B: tirar expectativas do registro (dados, consolidação, lista de agentes, web.md, contagens); a tese de expectativas passa à PM na consolidação; a definição da PM ganha o que vier do mapa; `expectativas-analyst.md` sai (propor apagar ou arquivar); a coluna Expectativas da aba Exógenas, se tutela algo (a aba é do usuário). Plano e custo antes. Registrar o crédito (pedido do B) segue normal. Retirar a exceção da Focus de desocupação quando o MT passar a ser dono dela (a linha da V.VII guardada pelo principal deixa de ser necessária no cenário 2).
- **→ D:** a camada 1 de literatura de expectativas vai aos novos donos (quase toda à PM) pelo `owner.py`; plano do que acontece com `obsidian/expectations/` e com a Parte 5 dos mapas que recebem, com custo, **depois** de o B fechar o mapa da PM. Seguem em curso: Kapitalo-externo, D2 do MT, as atas e comunicados da gestão Galípolo (liberados), e a regra do aceite no roteiro do `/mental` (o usuário aprova na aba do D).
- **→ C:** só aviso: a equação de expectativas do modelo fica igual e passa a ter a PM como dona; os itens sobre a âncora da expectativa ficam com a PM como interlocutora.

## Pausa de 2026-10-30 (pedido do usuário: nada sem liberação)

- A: a primeira aba "Chats A" era só a geradora das frases. O chat A real é a sessão `sistema-de-dados-11`: parado, plano A1 sem subagente, ~0,4–0,6M de contexto, itens 1–7 em janelas depois do ok.
- B: parado. Plano B1 = 3 janelas (fronteiras, perguntas centrais, tese) e depois 2 subagentes Opus para os mapas, ~2–3M.
- C: o C1b (feedback dos sete, Opus ad hoc, ~1M) já estava rodando; liberado terminar e gravar as respostas brutas em `structural_model/feedback_agentes/2026-10-30/`. O quadro C1a espera.
  C1b terminou: 1,06M, sete respostas gravadas, sem commit. Só a atividade pediu crédito na IS; ninguém pediu desemprego no hiato.
- D: parado. Plano D1 = Verde (inflação, expectativas), Kapitalo (externo), Kinea (fiscal, atividade), ~24 cartas cada, ~17 /mental, ~5–10M. Pedido: a tabela de áreas de `.claude/agents/mental-model.md` sem external/expectations (arquivo sem dono na tabela).
- Alerta de E: `cmb_risco_pais` recarregada às 11:14 por chat fora do plano, voltou a 2026-09-08; backup até 26/10 em `domain/db/brasil/bloomberg/backup/cmb_risco_pais_20261030_111451.csv`. Levado ao usuário.
- E: a C6 fechou antes da pausa (~105k, uma frase em fiscal_rf.md §4). A conferência (~0,6–1M) espera.
