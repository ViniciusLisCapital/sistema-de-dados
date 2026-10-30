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


## Próximas ações (2026-10-30)

1. O usuário abre os chats A, B, C, D e E (onda 1), cada um com a frase de `README.md`.
2. Avisar o chat C de que `analytics/brasil/structural_model/` e o chat E de que `domain/release_calendar/` também são mexidos por outros chats, fora do plano (`git status` de 2026-10-30).
3. Integrar ao SISTEMA, quando chegarem, as primeiras decisões de A (o ciclo) e de B (as fronteiras).


## Estado

- 2026-10-30: Plano 2 escrito (`PLANO_AGENTES.md`) e esta pasta criada pelo chat anterior, que terminou com o handover. Todo o trabalho anterior está commitado (último commit do usuário: 9e31b46).
- 2026-10-30 12:17: principal novo aberto (handover lido). Nenhum chat de frente começou: Estado de A–E vazio, F fechado. PLANO, `coordenacao/` e a linha do CLAUDE.md da raiz ainda sem commit.

## Pedidos repassados

- 2026-10-30 → C: `analytics/brasil/structural_model/` também é mexido por chats fora do plano; olhar `git status` antes de editar e não commitar o que não é seu.
- 2026-10-30 → E: idem para `domain/release_calendar/` (M em calendar_2026.yaml e sync.py) e `jobs/atualizar_diario.py`.
