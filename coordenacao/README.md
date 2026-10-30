# Coordenação do Plano 2 — vários chats, um principal

Desde 2026-10-30 o sistema de agentes é construído em vários chats ao mesmo tempo, coordenados por um chat principal. O plano é o [`PLANO_AGENTES.md`](../PLANO_AGENTES.md); aqui fica como os chats trabalham juntos sem se atropelar. Um arquivo por chat, escrito só por ele.

| Chat | Arquivo | Frente |
|---|---|---|
| principal | `P_principal.md` | coordena, integra as decisões, abre as ondas |
| A | `A_ciclo.md` | desenho do ciclo e do moderador |
| B | `B_novos_agentes.md` | agentes de mercado de trabalho e crédito |
| C | `C_modelo.md` | Modelo Estrutural, a partir do feedback dos agentes |
| D | `D_conhecimento.md` | camada 1 de literatura e de modelos mentais |
| E | `E_engenharia.md` | engenharia do ciclo |
| F | `F_ciclo2.md` | o ciclo 2 (abre na onda 3) |


## Como começar um chat

O usuário abre um chat novo e cola: *"Você é o chat X do Plano 2 do sistema de agentes. Leia `coordenacao/README.md` e `coordenacao/X_<nome>.md`, e comece pelo que o seu arquivo diz."* O arquivo do chat é o brief inteiro: escopo, o que ler, o que pode escrever, o que precisa do usuário e quando está pronto.


## Regras

1. **Cada chat escreve só o próprio arquivo de coordenação e os caminhos da sua frente** (tabela de donos abaixo). Um arquivo que não está na tabela da frente não se edita: pede-se ao principal.
2. **As decisões do usuário vão primeiro para a seção "Decisões" do arquivo do chat**, em lista simples, com data. O principal as leva ao `SISTEMA_AGENTES.md`, que só ele escreve. Assim o SISTEMA tem um escritor só.
3. **Pedido a outro chat** vai na seção "Pedidos" do próprio arquivo, com o destinatário. O principal repassa. Pode-se também avisar a outra sessão por `SendMessage` (as sessões locais aparecem no `ListAgents`), mas o arquivo é o registro.
4. **A seção "Estado" é atualizada ao fim de cada passo**: o que foi feito, os commits, o custo do passo e o próximo passo. É por ela que o principal sabe onde cada chat está.
5. **Decisão do usuário passa por uma janela de escolha** (AskUserQuestion), com a opção recomendada primeiro; nunca como lista de perguntas em texto.
6. **Commit só quando o usuário pedir**, e só dos próprios caminhos (`git add` explícito, nunca `-a`). Há outros chats, inclusive fora deste plano, mexendo na mesma pasta.
7. **Custo:** cada passo com subagente diz quanto custou (a notificação do subagente traz os tokens).
8. **Subagentes:** Sonnet para engenharia com teste e para buscar e baixar literatura; Opus para mapas, definições, rodadas do ciclo, moderador, escrivão, `/vault` e `/mental`.
9. **Dois `run.py` (ingestão) ou dois `/vault` nunca ao mesmo tempo**: os dois escrevem o tracker e as páginas de conceito. Por isso só o chat D roda `/ingest`, `/vault`, `/mental` e `owner.py`.


## Donos dos arquivos

Um escritor por arquivo. Quando duas frentes precisam do mesmo arquivo, uma escreve e a outra pede.

| Caminho | Dono | Observação |
|---|---|---|
| `SISTEMA_AGENTES.md`, `PLANO_AGENTES.md`, `PRINCIPIOS_AGENTES.md`, `CLAUDE.md` da raiz, `analytics/agent_system/CLAUDE.md` | P | os outros escrevem as decisões no próprio arquivo |
| `obsidian/ciclos/_modelo_report.md`, `_modelo_log.md`, o template da ata, `.claude/agents/moderador.md` (novo), `obsidian/escrivao/manual_do_escrivao.md`, `.claude/agents/escrivao.md` | A | o desenho do ciclo vira texto aqui |
| `.claude/agents/<os sete>-analyst.md`, `.claude/agents/web.md`, `analytics/agent_system/consolidacao.py`, `dados/motor.py`, `dados/__main__.py`, `conhecimento.py`, o código do tracker (`repository/ingestion/scripts/tracker.py`, `owner.py`), `tests/test_consolidacao.py`, `tests/test_dados_agentes.py`, `tests/test_conhecimento.py`, `tests/test_tracker.py` | E | aplica as decisões de A, B e C nesses arquivos |
| `obsidian/labor_market/`, `obsidian/credit/` (mapa conceitual), `.claude/agents/mercado-trabalho-analyst.md`, `.claude/agents/credito-analyst.md`, `dados/mercado_trabalho.py`, `dados/credito.py`, os mapas dos sete (só as linhas de saída e entrada com os dois novos), `dados/<os sete>.py` (só o reagrupamento do que era TWA) | B | os mapas e os módulos dos sete, numa janela que o principal libera |
| `analytics/brasil/structural_model/`, `analytics/agent_system/modelo.py`, `tests/test_modelo_agentes.py`, `tests/test_antecipa_modelo.py` | C | |
| `repository/` (raw_pdf, raw_md, settings, LOG), `obsidian/<área>/{clean_md,synthesis,mental_models}`, `obsidian/concepts/`, a Parte 5 dos mapas, `data_tracker.xlsx` (menos a aba Exógenas) | D | a aba Exógenas é do usuário |
| `obsidian/ciclos/2026-10-27/` | E | só o fechamento (C6, conferência) |
| `obsidian/ciclos/<data do ciclo 2>/` | F | |


## Sincronização

O principal lê os arquivos dos chats no início de cada sessão dele e quando o usuário pede. Nas passagens de onda ele confere as entradas (ex.: os mapas de B aprovados antes de D2 e B2), libera as janelas de escrita compartilhada (ex.: B nos mapas dos sete) e atualiza a tabela de status do PLANO.
