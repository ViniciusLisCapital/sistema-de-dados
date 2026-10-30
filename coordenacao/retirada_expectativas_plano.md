# Retirada do agente de expectativas — plano integrado (cenário 2 da B3 + itens comuns)

Leitura feita: SISTEMA III.III.vii–x e V.I–V.IX; B_novos_agentes.md (Plano da B3); mapas de expectativas e PM (e as linhas espelho dos outros sete); dados/*.py, motor, __main__, consolidacao, modelo (SAIDAS/CONVENCAO); definições de PM e expectativas; web, moderador, escrivão, skill ciclo; os seis testes (rodados).

## Estado de partida
- 5 de 6 testes verdes. **test_dados_credito tem 3 FALHAS pré-existentes** (l.106: "nenhum outro agente declara" itera `dados_main.AGENTES`, que já inclui o próprio crédito). Conserta no passo 4.
- Expectativas não é principal nem subordinado de nenhuma exógena (aba Exógenas, coluna vazia): nada de tutela a mover.
- `modelo.py` não muda: `focus_12m` continua saída do modelo; só o dono em `consolidacao.ENDOGENA_DONO` muda.

## Decisões técnicas (tomadas, só listadas)
1. **Posse pela lista, declaração física onde está** (regra do B): Focus Selic/IPCA/câmbio/Copom ficam declaradas em `cambio.py`; QPC em `politica_monetaria.py`; Focus de desocupação em `atividade.py`, **sem `variante`** (MT lê por `de(atividade, ...)`, arquivo `expc_focus_periodo__desocupacao.csv.gz`). É isso que mata a exceção `DIVIDIDAS`. Mover para `mercado_trabalho.py` criaria import circular.
2. `expectativas.py` vira `dados/focus.py` (`git mv`, preserva histórico): só funções de F (focus_movel, focus_periodo_inflacao, inflacao_implicita, desancoragem, juro_real_esperado, focus_contra_copom), sem TABELAS/SECAO. PM importa de lá; `focus_pib` some (a atividade já tem o seu).
3. PM ganha como endógenas `expc_focus (inflação)` e `expc_focus_periodo (inflação)` (as de expectativas, com dispersão e base de 4 dias) e deixa de listar o `expc_focus` simples e `expc_focus_periodo (IPCA)` (duplicatas). O `expc_focus` simples passa a ser declarado em `inflacao.py` (único consumidor); `juro_real` e `selic_curva_focus` da PM passam a ler o recorte inflação. Combinadas de PM: + desancoragem, + coerência Selic×IPCA da pesquisa (sem repetir o neutro do QPC, que `juro_real` já imprime), + Copom×QPC×Focus no horizonte relevante, + implícita com Δ e percentis.
4. Focus PIB: declaração idêntica passa para `atividade.py` (mesmo arquivo `expc_focus_periodo__pib.csv.gz`). Focus fiscal: dono natural é o fiscal → endógena dele, sai a `variante="fiscal"`. Crédito: `de(cambio, ..., "Selic")`.
5. **V.VII não some do SISTEMA**: fica o cabeçalho "## (V.VII) Agente de expectativas" com uma linha "retirado em 2026-10-30, III.III.x", sem itens. `externo.SECAO` termina em "## (V.VII)"; renumerar V.VIII/V.IX mexeria em SECAO de MT e crédito e em dezenas de referências.
6. Grupos de V.II renumerados (sai "iii. expectativas", entra "Endógeno de mercado de trabalho"): `pm.SECAO[1]` ("### ix. Fora da lista") muda junto, no mesmo passo.
7. PM vira dona da equação (E): multiplicadores `E.e1`/`E.e2` passam à PM (regra III.III.vii do dono da equação).
8. Mapa de expectativas fica como registro (cabeçalho "retirado"); `obsidian/expectations/` esvazia com o `owner.py --move` do D. `conhecimento.AREA` e `tracker.OWNERS` só perdem `expectativas` **depois** do move do D.
9. `.claude/agents/expectativas-analyst.md`: `git rm` (histórico guarda), só depois de `consolidacao.AGENTES` mudar.
10. Coluna "Expectativas" da aba Exógenas: fica (vazia, inofensiva; `ler_tutela` só exige as colunas de AGENTES). Remover é do usuário, que preenche a aba.

## Decidido pelo usuário (via coordenador)
- PM tem DUAS teses completas: Selic de fechamento e Focus IPCA 12m (média do trimestre), cada uma com central do modelo, faixa, caudas e placar. ENDOGENA_DONO["focus_12m"] = "politica_monetaria"; JSON da PM com `selic_fim` e `focus_12m` em `tese`; template já aceita várias variáveis (coluna "Variável").

## Plano em ordem de execução (nenhum arquivo em dois executores)
0. **Janela de decisões** (coordenador, ~0,05M) — as 3 abaixo.
1. **SISTEMA (coordenador, ~0,15M)**: V.I–V.IX reagrupados (ver lista no relatório), V.VII como registro, I.III.xii, IV.ii ("expectativas → expectativas" → PM), III.III.i (Q da PM renumeradas), fora-da-lista. Inclui os comuns da B3 (TWA crédito → consulta; mt_* → consulta ao MT).
2. **Sonnet, dados+registro+testes (~0,45M), imediatamente após 1**: módulos, __main__/consolidacao AGENTES, ENDOGENA_DONO, rótulo da PTC (comum B3), comentários "TWA/provisório", 4 testes, analytics/agent_system/CLAUDE.md. Gera F de PM/atividade/MT/crédito/fiscal em pasta temporária.
3. **Opus, mapa de PM (~0,35M)**: absorve expectativas + linhas B3 da PM. Fixa os rótulos novos.
4. **Opus ×2 em paralelo, outros mapas (~0,3M cada)**: A = câmbio, inflação, externo, fiscal; B = atividade, MT, crédito. Espelham o mapa da PM já pronto + linhas B3.
5. **Opus, definição da PM (~0,3M)**, depois de 2 e 3.
6. **Opus ×2 em paralelo (~0,25M cada)**: 6a = definições de câmbio, inflação, atividade, fiscal, externo, MT, crédito; 6b = web, moderador, escrivão, mental-model, skill ciclo, `git rm` expectativas-analyst.md.
7. **D move a literatura** (fora deste plano; depois de 3–4, porque o `owner.py` reescreve wikilinks nos mapas).
8. **Sonnet (~0,1M)**: AREA/OWNERS/test_conhecimento l.231; `generate_report.AGENTES_DET` + `report.html` ('x') + regerar o diagrama.
9. **Verificação (~0,1M)**: seis testes, `vault.py map` nos oito mapas, F real de PM.

Total ≈ 2,5M (≈0,6M disso é B3 que existiria nos dois cenários).

## Decisões do usuário (30/10, todas tomadas)
- A PM tem duas teses completas: a Selic e a Focus IPCA 12m, cada uma com central, faixa, caudas e placar. O JSON da PM leva `selic_fim` e `focus_12m` em `tese`.
- A ancoragem vira pergunta própria da PM (Q4), e o cenário passa a Q5.
- A Focus por componente do IPCA vai para a inflação. A PM fica com o IPCA cheio. A E24 não existe.

## O que o mapa da PM absorve (numeração proposta pelo subagente)

**Parte 1, perguntas centrais:**
- Q1–Q3 ficam. A Q2 remete à Q4. A Q3 absorve a Q3 de expectativas: a Focus (Selic por reunião e por ano), o QPC, a implícita contra a Focus e contra a projeção do Copom, e o teste de coerência da pesquisa.
- **Q4 nova:** "As expectativas de inflação estão ancoradas na meta, e o que as move?". Junta as Q1 e Q2 de expectativas: a distância à meta por horizonte, a posição no histórico (F ou G), nível contra ruído, os motores e o IPCA cheio.
- **Q5** é a antiga Q4: o cenário da Selic **e** da Focus 12m.

**Parte 1, horizonte.** Entram:
- a variável `focus_12m`: média do trimestre, exceção ao fechamento;
- a central do modelo;
- o placar;
- upside e downside como posição, com a desancoragem para baixo dita no texto;
- as leituras fixas que não são tese: os anos longos contra a meta e a implícita;
- o tempero `E.e1` e `E.e2`, que passa a ser da PM.

**Parte 2, canais.** Os números 2.1–2.10 ficam, porque crédito e MT os citam.
- **2.1:** o desvio é variável da própria PM.
- **2.2:** + o 2.4 de expectativas (choques visíveis movem primeiro os horizontes curtos e administrados e alimentos).
- **2.3 reescrito, endógeno:** + o 2.2 (meta, Copom, credibilidade) e o 2.7 de expectativas (curto contra longo à mesma distância). Sai a referência à S9.
- **2.4:** o QPC do hiato vira dado próprio; o trabalho vem do MT.
- **2.5:** + metade do 2.8 (o juro real esperado pela pesquisa contra o neutro do QPC).
- **2.6:** + o 2.3 de expectativas (a dúvida fiscal chega primeiro aos longos; contagem dupla).
- **2.7:** a Focus de câmbio vira consulta ao câmbio.
- **2.9:** + a outra metade do 2.8 (a Selic esperada pela pesquisa contra a curva; cortes esperados com a expectativa acima da meta como sinal de credibilidade).
- **2.10:** a regra de dados do crédito (B3).
- **2.11 nova:** formação das expectativas, a equação (E), que é o 2.1 de expectativas.
- **2.12 nova:** a pesquisa (dispersão, respostas frescas, respondentes), só o IPCA cheio; os componentes vão para a inflação, o PIB para a atividade.
- **2.13 nova:** pesquisa contra mercado, a implícita (o 2.6 de expectativas).
- A tabela de leitura de documento do Copom e "Where the agent reads the data" são atualizadas.

**Parte 3, saídas:**
- **S8:** + o que entra e sai da janela de 12 meses (o XS5).
- **S9:** aposentada.
- **S10:** só o hiato.
- **S12:** + a notícia fiscal nos horizontes longos (o XS8).
- **S14 nova, à inflação:** surpresas contra a Focus mensal (o XS6).
- **S15 nova, ao MT:** espelha ME-PM1.
- **S16 e S17 novas, ao crédito:** espelham CE-PM1 e CE-PM2.

**Parte 4, entradas.** E17–E20 ficam aposentadas. As novas:

| Linha | Origem | O que pede |
|---|---|---|
| E22 | câmbio S10 | Focus de IPCA e Selic |
| E23 | inflação IN-S9 | caminho da expectativa 12m e ancoragem |
| E25 | atividade S-PM4 (nova) | QPC: PIB, hiato, potencial |
| E26 | fiscal FS-PM5 (nova) | expectativas longas e implícita em torno de notícia fiscal; percepção fiscal do QPC |
| E27 | externo XS8 | bloco externo do QPC |
| E28 | MT MT-PM1 | leitura do Copom sobre o trabalho |
| E29 | MT MT-PM2 (nova) | NAIRU e hiato do QPC |
| E30 | crédito CR-PM1 | Selic e curva, mais a Focus de Selic e IPCA por ano |
| E31 | crédito CR-PM2 | leitura do Copom e do BC sobre o crédito |

**Nos outros mapas:**
- **câmbio:** a Focus de câmbio é dado próprio; S10 passa para a PM; E15 sai.
- **inflação:** o 2.3 passa para a PM; IN-S9 passa para a PM; IN-S10 (componentes) fica com a própria inflação; IN-E9 sai; IN-E10 espelha a S14.
- **atividade:** a Focus de PIB é dado próprio; S-EXP1 e S-EXP2 viram S-PM4 mais as S-MT; E5 sai.
- **fiscal:** a 3.6 sai; a Focus fiscal é dado próprio; entra FS-PM5; FE-EP1 sai.
- **externo:** XS8 passa para a PM; XE12 sai.
- **MT:** a Focus de desocupação é dado próprio (T5, 2.1); MT-EP1 vira MT-PM2.
- **crédito:** CR-EP1 entra na CR-PM1.
- Mais as linhas comuns da B3 de `B_novos_agentes.md`.

## Riscos de ordem
- Os passos 1 e 2 rodam juntos: entre eles, `test_dados_agentes`, `test_dados_credito` e `test_dados_mercado_trabalho` ficam vermelhos.
- `focus.py` e `test_dados_credito` vão no mesmo passo, porque o teste importa `expectativas`.
- O `git rm` de `expectativas-analyst.md` só acontece depois de `consolidacao.AGENTES` mudar.
- `DIVIDIDAS` sai junto com a remoção da variante. Fazer antes de extrair o A do ciclo 2, porque os nomes dos arquivos de desocupação e fiscal mudam.
- `pm.SECAO[1]` muda no mesmo passo em que o SISTEMA renumera os grupos de V.II. `externo.SECAO` termina em "## (V.VII)", então o cabeçalho fica.
- `test_conhecimento` l.231, `AREA` e `OWNERS` só mudam depois do `owner.py`.
- O `owner.py` reescreve wikilinks nos mapas, então roda depois dos passos 3 e 4. Os passos 4 e 6 dependem dos rótulos fixados no 3.
- O `test_dados_credito` tem uma falha que já existia (l.106) e precisa ser consertada no passo 2.
