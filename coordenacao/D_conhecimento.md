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

(vazio: o chat começa aqui)

## Decisões

## Pedidos
