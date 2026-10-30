# Chat D — Conhecimento: camada 1 de literatura e de modelos mentais

**Objetivo.** Os nove agentes chegam ao ciclo 2 com a camada 1 completa:
- modelos mentais dos cinco agentes de 2026-10-22 (inflação, atividade, fiscal, externo, expectativas), que ainda não têm gestora;
- literatura e modelos mentais dos dois novos (mercado de trabalho e crédito), a partir dos mapas do chat B.

É o único chat que roda `/ingest`, `/vault`, `/mental` e `owner.py`, porque dois deles ao mesmo tempo se atropelam no tracker e nas páginas de conceito.

**Ler primeiro:**
- `README.md` desta pasta.
- `SISTEMA_AGENTES.md`:
    - I.III.xvi–xvii (camadas e dono da literatura);
    - II.I (iv a vii: ingestão, vault, modelos mentais);
    - **II.IV** (como a camada 1 dos cinco foi feita em 2026-10-29: uma fonte por canal, as decisões e as lições do limpador).
- `repository/CLAUDE.md`, `repository/mental_model/MENTAL_MODELS.md` e `repository/mental_model/mental_models.yaml`.
- As definições `.claude/agents/ingestion.md`, `vault.md` (a regra nova da seção BRL / application), `mental-model.md` e `mental-model-reviewer.md`.
- O tracker: as abas "Qual - <área>" (colunas Dono, Camada, Fila) e "Mental Models".


## O que precisa do usuário

1. **As gestoras dos cinco**, numa janela: uma por área, com a proposta e quantas cartas de cada gestora falam da área. Cartas no repositório: Verde (200), Kapitalo (83), Kinea (60), Kinea Insights (64), Goldman Sachs (~80), SPX (7). Já existem documentos de câmbio (Verde, Kapitalo, Kinea, Goldman) e de PM (Verde).
2. **A camada 1 dos dois novos**, com o julgamento delegado, como em 2026-10-29 ("siga o seu julgamento"; pergunte só o que tiver muita dúvida e nenhuma jurisprudência).
3. **As gestoras dos dois novos**, numa janela.


## Passos

- **D1.** Gestoras dos cinco → `/mental <gestora> <área>` em série, cada rodada com o revisor → Camada 1 na aba Mental Models → `tracker.py`. Começa já.
- **D2.** Quando o chat B avisar, pelo principal, que os mapas estão aprovados, a literatura dos dois novos, pelo mesmo processo de 2026-10-29:
    1. uma fonte por canal da Parte 2;
    2. um subagente Sonnet propõe e baixa, só cópias abertas;
    3. `/ingest` e `/vault` (no máximo 5 por rodada);
    4. Dono e Camada no tracker;
    5. a lista da camada 1 na Parte 5 de cada mapa;
    6. `vault.py check`, `concept` e `map`.

  A pasta de crédito nasce agora (`repository/credit/raw_pdf/`); a de mercado de trabalho já existe e a aba dela tem 25 candidatas. Depois, a gestora e o `/mental` dos dois.
- **D3.** Conferir o retrato: `conhecimento.itens` sem item faltando para os nove (o registro do crédito no `OWNERS`/`AREA` é do chat E).
- **D4 (opcional, no fim).** As pendências pequenas da base, listadas no PLANO ("Anotado para depois").

**Escreve:** este arquivo, `repository/` (raw_pdf, raw_md, settings, LOG), `obsidian/<área>/{clean_md,synthesis,mental_models}`, `obsidian/concepts/`, a Parte 5 dos mapas e o `data_tracker.xlsx` (menos a aba Exógenas, que é do usuário). **Não escreve:** as Partes 1–4 dos mapas (chat B), o código do retrato e do tracker (chat E e o principal).

**Pronto quando:** os nove têm camada 1 de literatura e de modelo mental marcada no tracker, as checagens passam e o retrato monta sem item faltando.


## Estado

- **2026-10-30 — leitura feita, nada escrito.** Parado a pedido do principal até ele liberar. D2 não começa antes dos mapas de B aprovados.
- **Levantamento (só leitura).** Contagem léxica por parágrafo, nas cartas já extraídas: cartas com 3 ou mais parágrafos sobre a área no Brasil, desde 2020 (externo sem o filtro de Brasil). Goldman Sachs (sem texto, e só câmbio) e SPX (7 PDFs, sem texto) ficam fora.

  | área | Verde (80) | Kapitalo (80) | Kinea Carta (62) | Kinea Insights (67) |
  |---|---|---|---|---|
  | inflação | 8 | 3 | 9 | 2 |
  | atividade | 2 | 1 | 5 | 6 |
  | fiscal | 4 | 1 | **22** | 4 |
  | externo | 45 | **54** | 61 | 45 |
  | expectativas | 2 (77 parágrafos) | 0 (23) | 0 (7) | 0 (3) |

  As cartas da Kinea são longas (~2.200 palavras, contra ~800 da Verde e ~900 da Kapitalo), então a contagem por carta a favorece; por isso a proposta olha também o total de parágrafos.
- **Plano do D1** (a confirmar com o usuário numa janela, recomendação primeiro):
    - inflação → Verde; expectativas → Verde; externo → Kapitalo (fundo global: dólar, juros dos desenvolvidos, commodities em quase toda carta); fiscal → Kinea; atividade → Kinea (Carta + Insights).
    - Janela de camada 1, como a da Verde de PM (24 cartas): as ~24 cartas mais recentes. Verde e Kapitalo de 2024-09 a 2026-08 (24 cartas cada); Kinea de 2025-09 a 2026-09 (26 cartas, Carta + Insights). Alternativa na janela: um episódio por área (ex.: fiscal desde o arcabouço, 2023), mais caro.
    - Execução: `/mental <gestora> <área>` em série, um documento de cada vez, escritor e revisor Opus, ~3 rodadas por documento (Kinea ~4, pelas cartas longas); ~17 rodadas no total. Depois de cada primeira rodada, a estrutura do documento novo vai ao usuário antes da segunda (regra do `mental-model.md`).
- **Arquivos que o D1 toca:**
    - `repository/mental_model/mental_models.yaml`: os códigos de área `external` e `expectations` (hoje faltam, e o `mental.py` recusa a área) e a janela dos cinco documentos;
    - `obsidian/{inflation,expectations,external,fiscal_policy,economic_activity}/mental_models/` (cinco documentos novos);
    - `repository/mental_model/ledger/` (pelo `mental.py`);
    - `data_tracker.xlsx`, aba Mental Models (pelo `mental.py done`; Camada = 1 nos cinco);
    - `repository/mental_model/MENTAL_MODELS.md` (tabela de estado).
- **Custo estimado do D1:** ~1–2M por documento (estimativa do PLANO, não medida), ~5–10M nos cinco. O levantamento acima custou só a leitura desta sessão.
- **2026-10-30 — D1 liberado e preparado.** `mental_models.yaml` ganhou os códigos `external`/`expectations` e as cinco janelas; o `mental.py --list` reconhece os cinco documentos (24 cartas pendentes em cada um dos da Verde e da Kapitalo, 26 em cada um da Kinea). A tabela de áreas do `mental-model.md` ganhou externo e expectativas.
- **2026-10-30 — Verde × inflação, rodada 1 (10 cartas, set/2024 a jun/2025): não registrada, à espera do usuário.** O documento novo existe (`obsidian/inflation/mental_models/verde_inflation_mental_models.md`, ~3.500 palavras, 3 grupos e 9 entradas) e o `check` passa. Os três revisores barraram 4, depois 5, depois 2 frases. Todas tinham o mesmo defeito: um nexo causal, um motivo ou uma generalização que a carta não diz. As duas rodadas de correção que o processo permite acabaram, e os dois achados que sobram foram ao principal como janela.
    - Custo medido: escritor 166k + 180k + 210k = ~555k; revisores 147k + 156k + 150k = ~452k; **~1,0M na rodada**, sem a sessão que conduz.
    - Projeção: com ~3 rodadas por documento, ~2,5–3M por documento e ~12–15M nos cinco, acima dos 5–10M estimados. Rodadas seguintes podem sair mais baratas (menos frases novas por rodada), mas também passam a reempacotar.
- **2026-10-30 — terceira correção feita (as duas frases), mas o quarto revisor barrou outras duas** que já estavam no texto e que três revisores tinham deixado passar: 1.4 ("e com ela o trade eleitoral", quando a carta antecipa só a *discussão*) e a introdução do grupo 3 ("nos EUA e no Brasil", quando nenhuma carta liga a posição no Brasil a uma visão de inflação, o que o próprio 3.2 diz). A rodada continua não registrada; isto e a proposta de pente fino foram ao principal.
    - Custo medido da rodada 1 até aqui: escritor 166k + 180k + 210k + 212k = ~768k (a terceira correção, de duas frases, custou 212k em 23 s, porque a retomada carrega todo o contexto); revisores 147k + 156k + 150k + 151k = ~604k; **~1,37M**.
    - Os quatro revisores barraram 4, 5, 2 e 2 frases, nunca a mesma duas vezes: cada leitura inteira acha outras, então o processo não converge por repetição.
- **2026-10-30 — pente fino implementado** (subagente Sonnet, 197k):
    - em `mental.py`: `findings`, `packet --delta`, a base de revisão no `done` e o campo `evidence` exigido nas rodadas novas;
    - as duas definições de agente, o SKILL do `/mental` e o `MENTAL_MODELS.md`;
    - `tests/test_mental.py`: 15 testes, que pegam 11 mutantes (rodar com `uv run --with pytest python -m pytest tests/test_mental.py`, porque o pytest não está no venv).
- **2026-10-30 — Verde × inflação, rodada 1 REGISTRADA** (10 cartas, set/2024 a jun/2025; 14 pendentes). A correção pelo processo novo custou 111k no escritor enxuto e 117k na revisão delta (só os blocos 1.4 e 3, nenhum achado), **228k contra ~100k estimados**, e contra ~360k da correção à moda antiga (retomada + revisor inteiro). Custo total da rodada 1: **~1,6M** (escritor 768k, quatro revisores inteiros 604k, a correção nova 228k), mais 197k da implementação.
    - Por que a correção saiu acima da estimativa: todo subagente carrega `.claude/rules/lis-dashboards.md` (180 KB, ~45–50 mil tokens, sem `paths:` no cabeçalho, então carrega em qualquer sessão), mais o `CLAUDE.md` da raiz (19 KB). É um piso fixo em cada subagente do sistema, inclusive nos agentes do ciclo. Proposta ao principal em Pedidos.
- **2026-10-30 — Verde × inflação, rodada 2 REGISTRADA** (10 cartas, jul/2025 a abr/2026; 20 lidas, 4 pendentes). Primeira rodada inteira no processo novo, com **~569k**: escritor 185k, revisor inteiro 168k (3 achados), escritor enxuto 109k, revisão delta 107k (nenhum achado). Ficou dentro dos 0,45–0,65M estimados para o processo novo e é cerca de um terço da rodada 1.
    - Entradas novas: 2.4 (Fed sob pressão política) e 2.5 (choque de energia de 2026). O escritor anotou que nenhuma das 10 cartas discute a inflação brasileira em si, e que 2.1 e 2.5 são dois choques estagflacionários mantidos separados.
    - Defeito pequeno do `mental.py`, anotado e não consertado: o `check` conta a divisória `---` que fecha um grupo como texto da última entrada, então uma entrada nova no fim do grupo obriga a deixar uma divisória a mais depois da 2.3. É cosmético; o conserto muda o corte de blocos (e os hashes da base de revisão), então fica para fora de rodada aberta e com o aval do usuário.
- **2026-10-30 — Verde × inflação FECHADO** (24 de 24 cartas; ~8.200 palavras, 12 entradas em 3 grupos).
    - Rodada 3 (4 cartas, mai a ago/2026): **~593k**. Escritor 172k, revisor inteiro 170k (2 achados), escritor enxuto 119k, revisão delta 132k (nenhum achado). Entrada nova 2.6 (dívida dos desenvolvidos: mais inflação ou repressão financeira); a posição em inflação implícita nos EUA acaba em mai/2026, sem razão declarada.
    - **Custo do documento: ~2,76M** (rodada 1 ~1,6M, rodada 2 ~0,57M, rodada 3 ~0,59M), mais 197k do pente fino.
    - Camada = 1 marcada na aba Mental Models para os cinco documentos (sobrevive à reconstrução do `tracker.py`); tabela de estado do `MENTAL_MODELS.md` atualizada.
    - **O filtro `paths:` no `lis-dashboards.md` não mostrou ganho nos subagentes:** a correção enxuta custou 119k depois do filtro, contra 109–111k antes, e a revisão delta 132k, contra 107–117k antes. As do rodada 3 fizeram mais trabalho (mais blocos e afirmações, uma aplicação nova). A hipótese de que o arquivo pesava em todo subagente não se confirma; o piso de ~110k vem de outro lugar (definição do agente, `CLAUDE.md`, leituras).
    - **Projeção dos quatro restantes,** a ~0,58M por rodada: Verde × expectativas ~1,8M (3 rodadas), Kapitalo × externo ~1,8M, Kinea × fiscal e Kinea × atividade ~2,3M cada (cartas longas, ~4 rodadas). São ~8,2M, e os cinco ficam em **~11M**, um pouco acima dos 5–10M.
    - **Pontos de texto que não barraram e ficam para o usuário** (nenhum se corrige pelo fluxo normal, que só reescreve a entrada que as cartas novas tocam):
        - em 1.2 falta a aplicação de jun/2026 (a carta que nomeia o "acelerador fiscal e parafiscal"), e o texto põe em mai/2026 a palavra dessa carta;
        - em 2.5, o petróleo caro "por bastante tempo" (mar/2026) convive sem reconciliação com o Brent de volta aos preços de antes da guerra (jun/2026);
        - o título novo de 1.3 ("Os dados de inflação movem os juros") se apoia numa linha só;
        - a introdução do grupo 1 não menciona o parafiscal, a do grupo 2 virou uma frase longa demais, e a 3.1 tem 23 marcadores e lê como diário de posições;
        - 2.1 e 2.5 são dois choques estagflacionários mantidos separados;
        - sobra uma divisória `---` (o defeito do `check` anotado acima).
- **2026-10-30 — Verde × expectativas, rodada 1: escritor feito (175k), parado antes do revisor.** As 3 entradas do documento novo repetem 3 do documento de inflação:
    - 1.1 Fiscal desancorado, igual à 1.2 de inflação;
    - 1.2 inflação implícita longa no Brasil, igual à 3.2;
    - 2.1 inflação implícita americana, igual à 3.1.

  O escritor anotou que a Verde nunca fala de Focus, pesquisas, dispersão ou revisão de expectativas. A pergunta foi ao principal antes de gastar o revisor (~170k mais a correção).
- **2026-10-30 — Verde × expectativas DESCARTADO** (decisão do usuário). Rodada abortada pelo `mental.py abort`, sem registro; o documento novo apagado (nunca foi versionado); ledger sem mudança. **O agente de expectativas fica sem modelo mental próprio na camada 1** e chega ao da Verde em inflação pelos conceitos (ancoragem de expectativas, inflação implícita). O código `expectations` continua no `mental_models.yaml` e na tabela do `mental-model.md`, com nota; a janela do documento ficou comentada. Perda: 175k. Projeção dos cinco: **~9,4M**.
- **2026-10-30 — Kapitalo × externo, rodada 1 (10 cartas, set/2024 a jun/2025): não registrada, à espera do usuário.** O documento novo tem 13 entradas em 5 grupos e 192 afirmações, todas com a frase da carta.
    - Custo: escritor 270k, revisor inteiro 189k (5 achados), escritor enxuto 130k, revisão delta 4 blocos 152k; **~0,74M** até aqui.
    - A revisão delta achou 3 pontos novos nos blocos corrigidos:
        - 2.4: comércio e investimento postos como efeito da incerteza;
        - 2.4: "política americana" onde a carta fala de acontecimentos que incluem a Alemanha e a China;
        - 4.2: "não reflete" onde a carta diz "não refletia completamente".
    - Pelo P4, a correção única da rodada já foi usada, e a escolha foi ao principal.
    - Decidido por mim (técnico): o Canadá fica na 5.2 e a 1.3 fica como entrada própria (as duas podem crescer nas próximas rodadas, e o número de entrada é permanente).
- **2026-10-30 — Kapitalo × externo, rodada 1: segunda correção feita** (escritor enxuto 112k, revisão delta 147k). As 3 frases passaram, mas sobrou 1 ponto no bloco 1.2: o parágrafo de abertura diz que o conjunto "deveria encerrar o sincronismo dos ciclos" sem o "entre os desenvolvidos" da carta. A aplicação de jan/2025, na mesma entrada, já diz certo.
    - Esse bloco só foi relido por **erro meu de condução**: não rodei o `done` depois da primeira revisão delta, a base de comparação não andou, e a segunda revisão releu 1.2 e 2.1, que não tinham mudado. Corrigido no procedimento: o `done` roda depois de toda revisão.
    - Custo da rodada até aqui: **~1,0M** (270 + 189 + 130 + 152 + 112 + 147k).
    - A segunda correção falhou, então, pela regra do usuário, a escolha foi ao principal.
- **2026-10-30 — Kapitalo × externo, rodada 1 REGISTRADA** (10 de 24 cartas; 14 pendentes), com o aceite do usuário no 1.2 anotado no log. Custo: **~1,0M**.
- **2026-10-30 — Kapitalo × externo, rodada 2** (10 cartas, jul/2025 a abr/2026): passou na revisão delta, sem achado. O `done` espera a ingestão do mercado de trabalho terminar (os dois escrevem o tracker).
    - Custo: escritor 297k, revisor inteiro 243k (5 achados), escritor enxuto 124k, revisão delta 149k; **~0,81M**.
    - Entradas novas: 1.4 ciclo global estendido, 1.5 choque de oferta e o dilema do BC, 1.6 institucionalidade do Fed, 2.5 a política americana empurra carteiras para fora dos EUA, 4.4 ouro, 4.5 prata, 5.3 Argentina. A posição vendida em petróleo virou comprada em mar/2026.
    - Notas do escritor, sem mexer: 4.2 escreve spreads de petróleo em "$/bushel" (conferir na carta de jan/2025); sobram divisórias `---` (o defeito do `check`); as introduções dos grupos 1, 4 e 5 não citam as entradas novas.
- **2026-10-30 — D2 do mercado de trabalho:**
    - Borges (2022) movido de atividade para mercado de trabalho (`owner.py`: 4 arquivos, 8 links); `vault.py check` passa; a Parte 5 do mapa de atividade anota o dono novo.
    - As 7 fontes novas baixadas, só cópias abertas, por um subagente Sonnet (161k): IPEA 2025 sobre participação (2.2, substitui o boxe do BC, que não existe), Ball, Leigh & Loungani 2013 (2.3), Ulyssea 2018 (2.4), boxe do BC set/2021 sobre efeito composição (2.5), Greenstone, Mas & Nguyen 2014 (2.6, substitui Chodorow-Reich, sem cópia aberta acessível), Galí 2010 (2.7), Engbom & Moser 2021 (2.9).
    - `/ingest labor_market` rodando.
- **2026-10-30 — gestão Galípolo no vault:** plano enviado ao principal. Ponto central: os comunicados do vault são espelhados byte a byte do raw_md a cada ETL, então as tags ficam numa página-índice fora do clean_md (`obsidian/monetary_policy/central_bank/gestao_galipolo.md`), e as páginas de conceito ganham a linha de volta. Pedido ao E: o retrato tem de levar a página-índice. Custo ~0,5–0,7M. Pergunta ao usuário: só a gestão Galípolo ou o histórico inteiro.
- **Próximo passo:** quando a ingestão terminar, o `done` do Kapitalo e depois `/vault labor_market` (duas levas); Kapitalo × externo rodada 3; a gestão Galípolo quando o usuário responder.

## Decisões

- 2026-10-30 (usuário, pelo principal): modelo mental de camada 1 dos cinco = a gestora mais forte em cada área, com as ~24 cartas mais recentes. Verde para inflação e expectativas (de 2024-09 a 2026-08), Kapitalo para externo (de 2024-09 a 2026-08), Kinea para fiscal e atividade (de 2025-09 a 2026-09, Carta + Insights). Um `/mental` por vez, com o custo real de cada rodada no Estado.
- 2026-10-30 (usuário, pelo principal), Verde × inflação, rodada 1: uma terceira correção, só das duas frases barradas, com o texto que o revisor propôs; um revisor novo confere, e a rodada é registrada.
- 2026-10-30 (usuário, pelo principal): a estrutura do modelo mental de inflação da Verde fica com os 3 grupos (Brasil; mundo; posicionamento em inflação), inclusive a 1.2 e as entradas de posição 3.1 e 3.2.
- 2026-10-30 (usuário, pelo principal): os cinco documentos mantêm as ~24 cartas, mas antes da rodada 2 o chat D propõe um pente fino do processo do `/mental` (ex.: o revisor da correção lê só os blocos corrigidos), com o ganho estimado. A proposta vai ao principal antes de mexer em `mental.py`, `.claude/agents/mental-model*.md` ou no `/mental`: esses arquivos ficam com o chat D, mas a mudança de processo é decisão do usuário.
- 2026-10-30 (usuário, pelo principal): pente fino do `/mental` adotado, os quatro pontos:
    - P1, a correção é feita por um escritor novo e enxuto, não pela retomada do escritor;
    - P2, a revisão depois de uma correção vê só os blocos que mudaram;
    - P3, cada afirmação nova traz a frase literal da carta que a sustenta, e o `check` a confere;
    - P4, no máximo uma correção por rodada, e o que sobrar vai ao usuário.

  Feito por um subagente Sonnet com teste, sem commit.
- 2026-10-30 (usuário, pelo principal), Verde × inflação, rodada 1: as duas frases do quarto revisor (1.4 e introdução do grupo 3) são corrigidas pelo processo novo, como primeiro teste, e a rodada é registrada. O custo medido dessa correção volta ao principal antes da rodada 2.
- 2026-10-30 (usuário, pelo principal): o modelo mental de expectativas da Verde é descartado, porque as entradas repetiam as do de inflação. O agente de expectativas fica sem modelo mental próprio na camada 1 e chega ao da Verde em inflação pelos conceitos. O código `expectations` fica, com nota.
- 2026-10-30 (usuário, pelo principal): "corrigir sempre, sem perguntar". Quando a revisão da correção achar imprecisões pequenas, faz-se uma segunda correção com o texto do revisor, conferem-se só esses trechos e registra-se a rodada (~250k). O usuário só é chamado se essa segunda correção também falhar. Vale já para as 3 frases do Kapitalo × externo.
- 2026-10-30 (principal, escopo técnico): a entrada do gás natural americano (4.3) fica no documento do Kapitalo × externo.
- 2026-10-30 (usuário, pelo principal): "aceitar e virar regra".
    - A frase do 1.2 do Kapitalo × externo (sem "entre diversos países desenvolvidos") é aceita, e a rodada 1 é registrada.
    - Regra daqui em diante: se sobrar uma imprecisão depois da segunda correção e a frase exata da carta já estiver na mesma entrada, o chat D aceita sozinho, e o histórico do documento registra "aceite por regra do usuário de 2026-10-30". Se a frase não estiver na entrada, a escolha vai ao principal.
    - Escrita no `MENTAL_MODELS.md`. O SKILL do `/mental` não foi editado: a trava de modo automático bloqueou duas vezes a edição como automodificação, inclusive depois da liberação do usuário pelo principal, e a trava não abre pedido de aprovação. Até o usuário fazer a edição ou liberá-la, a regra vale pelo `MENTAL_MODELS.md` e por esta lista.
- 2026-10-30 (usuário, pelo principal): o agente de mercado de trabalho fica **sem modelo mental próprio** na camada 1 ("nenhuma por ora"). Ele chega aos modelos mentais de atividade e de inflação pelos conceitos, como o de expectativas.
- 2026-10-30 (usuário, pelo principal): o plano do D2 do mercado de trabalho está liberado, com o julgamento das fontes delegado ao chat D. Uma fonte por canal:
    - Borges (2022) passa ao mercado de trabalho pelo `owner.py`;
    - sete fontes novas, só de cópias abertas;
    - 2.8 fica sem fonte própria (é da inflação);
    - custo ~0,9–1,2M.
- 2026-10-30 (usuário, pelo principal): atas e comunicados do Copom entram no vault como estão, sem `/mental`; os RPMs serão o material processado do modelo mental da gestão, depois. Escopo: **só a gestão Galípolo** (reuniões 268–281, 28 documentos). O plano foi liberado:
    - página-índice `obsidian/monetary_policy/central_bank/gestao_galipolo.md`, fora do clean_md (o ETL espelha os comunicados byte a byte);
    - vocabulário fechado de tags, cada tema ligado a uma página de conceito existente;
    - linha de volta nas páginas de conceito;
    - script determinístico para número, datas, decisão (do banco, `pm_copom_reuniao`) e links;
    - subagente só para escolher os temas, com uma frase do documento por tema;
    - checagem nova e ajuste no `vault.py`, por um subagente Sonnet com teste;
    - custo ~0,5–0,7M.

  O pedido ao E (a página-índice no retrato da PM) foi repassado pelo principal; o chat D avisa o E quando a página existir.

## Pedidos

- **Ao principal (2026-10-30):** a tabela "The area" de `.claude/agents/mental-model.md` não tem linhas para `external` e `expectations`. Não é arquivo da frente D. Proposta de texto: *external — the global environment as it reaches Brazil: Fed and US rates, the global dollar, risk appetite, commodities, the peers' policy cycle*; *expectations — inflation expectations and their anchoring: Focus, the curve's implied inflation, dispersion and revisions*. Quem escreve? Se ninguém, o D1 passa a descrição da área no prompt do escritor. **Resolvido (2026-10-30):** o principal passou a tabela ao chat D, que acrescenta as duas linhas quando o D1 for liberado.
- **Ao principal (2026-10-30), afeta todas as frentes:** `.claude/rules/lis-dashboards.md` tem 180 KB (~45–50 mil tokens) e não tem `paths:` no cabeçalho, então carrega em toda sessão e em todo subagente, inclusive nos que nada têm a ver com dashboard (modelo mental, vault, agentes do ciclo). Proposta: pôr no cabeçalho um `paths:` restrito aos relatórios (ex.: `analytics/**/report.html`, `analytics/**/generate_report.py`, `analytics/report_structure/**`, `tests/test_*_js.js`). Não é arquivo da frente D, e a decisão é do usuário.
