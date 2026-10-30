# Chat B — Agentes de mercado de trabalho e crédito

**Objetivo.** Criar os agentes `mercado_trabalho` e `credito` para que rodem no ciclo 2 junto com os sete. Cada um precisa de mapa conceitual aprovado, lista de dados, módulo de dados e definição, e os sete precisam ser ajustados. A camada 1 de literatura e de modelos mentais deles é feita pelo chat D, a partir dos mapas aprovados aqui.

**Ler primeiro:**
- `README.md` desta pasta.
- `PRINCIPIOS_AGENTES.md` inteiro: os princípios de todo agente, aplicados sem perguntar.
- `SISTEMA_AGENTES.md`:
    - I.II.ii e I.III.vi (o mapa conceitual é o contrato da área: perguntas, esqueleto causal, saídas, entradas, conceitos);
    - I.III.ix–xii (endógeno, exógeno, TWA, endógeno de outro agente);
    - **III.III.vii** (as fronteiras do primeiro batch; a atividade absorveu o mercado de trabalho "provisoriamente, até existir o agente dele");
    - V.IV.i (as tabelas `mt_*` hoje na atividade), V.II.vi, V.IV.viii e V.V.viii (crédito, TWA na PM, na atividade e no fiscal).
- Um agente novo do primeiro batch como molde, por exemplo o fiscal: o mapa `obsidian/fiscal_policy/fiscal_policy_conceptual_map.md`, o módulo `analytics/agent_system/dados/fiscal.py` e a definição `.claude/agents/fiscal-analyst.md`.
- O que o banco tem: `analytics/brasil/credit/CLAUDE.md`, `analytics/brasil/labor_market/CLAUDE.md` e `domain/db/CLAUDE.md` (tabelas `cred_*` e `mt_*`).
- O tracker: a aba "Qual - Labor Market" tem 25 candidatas; não há aba de crédito.


## O que precisa do usuário, em ordem

O processo é o da Fase 8 do Plano 1: um subagente Opus rascunha o mapa (Partes 1–4) e a lista de dados, e cada parte é aprovada numa janela, um agente de cada vez.

1. **As fronteiras.**
    - Mercado de trabalho: o que sai da atividade (`mt_pnad`, `mt_desocupacao_retro`, `mt_caged`, `mt_caged_setor`) e o que fica (o hiato fica com a atividade).
    - Crédito: o que é dele e não da PM (o canal de crédito), do fiscal (o crédito parafiscal e o BNDES, canal 2.5 do fiscal) ou da atividade (o impulso de crédito).
2. **As perguntas centrais** de cada um.
3. **A variável, o horizonte e o upside/downside.** Hoje nenhum dos dois tem variável no Modelo Estrutural. A decidir com o chat C (frente do modelo): se o crédito entra na curva IS e se o desemprego entra no hiato. Até lá vale a regra do fiscal e do externo: a tese é o caminho base das exógenas que tutelam, e a distribuição em volta é deles.
4. **A lista de dados.** As lacunas de tempestividade já conhecidas: `cred_fluxo_financeiro` parado em abr/26 e `mt_pnad` fora do job de rotina (achados da Fase 10; confirmar se continuam).
5. **As saídas e as entradas**, espelhadas nos mapas dos sete.
6. **A tutela de exógenas**, se houver alguma para os dois. Quem preenche a aba "Exógenas" é o usuário.


## Passos

- **B1.** Os dois mapas, Partes 1–4, aprovados parte a parte, mais a lista de dados (para o SISTEMA, pelo principal, como V.VIII e V.IX). Ao fim, avisar o chat D, pelo principal, que os mapas estão prontos (D2 começa daí).
- **B2.** Os módulos `dados/mercado_trabalho.py` e `dados/credito.py`, com teste (Sonnet), e as definições `.claude/agents/mercado-trabalho-analyst.md` e `credito-analyst.md` (Opus), derivadas das que existem.
- **B3.** O ajuste dos sete, numa janela que o principal libera:
    - as linhas de saída e entrada com os dois novos nos mapas dos sete;
    - o que era TWA vira "endógeno de <agente> (consulta)" nos módulos de dados dos sete;
    - a lista do que muda nas definições dos sete vai para o chat E.
- **B4.** Pedir ao chat E o registro dos dois novos: a linha em `AGENTES`, a pasta `credit` no `OWNERS` do tracker e no `AREA` do retrato, a checagem de consulta entre todos os pares, e as colunas na aba Exógenas.

**Escreve:** este arquivo, `obsidian/labor_market/` e `obsidian/credit/` (os mapas), as duas definições novas, os dois módulos novos e os testes deles; na janela B3, as linhas dos mapas dos sete e o reagrupamento nos módulos dos sete. **Não escreve:** as definições dos sete, o motor, o `__main__` e o retrato (chat E), a Parte 5 dos mapas e a literatura (chat D), o modelo (chat C).

**Pronto quando:** os dois mapas passam no `vault.py map`, `dados <agente> --ciclo <data>` roda para os dois e o `motor.conferir` bate, as definições estão aprovadas e os sete foram ajustados.


## Estado

(vazio: o chat começa aqui)

## Decisões

## Pedidos
