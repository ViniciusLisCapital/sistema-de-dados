# Log — ciclo 2026-10-07

Escrito pela sessão que conduz o ciclo. Os reports de cada rodada e as consolidações (P1, P2) ficam vivos durante o ciclo; quando ele acaba, ficam o report final (RF) de cada agente e este log, que guarda o processo: o que cada um leu, o que mudou entre as rodadas e por quê.

Primeiro ciclo do sistema, em teste solo: só o agente de câmbio roda, na rodada 1. O agente de política monetária ainda não existe. A rodada 1 rodou duas vezes: a v1 (07/10), no formato antigo (`cambio_r1_v1.md`), e a v2 (15/10), refeita do zero no formato novo do report (`cambio_r1.md`), sobre o mesmo F(A).

## Informação nova desde o ciclo anterior

Primeiro ciclo: não há ciclo anterior. F(A) gerado em 2026-10-07 14:01, com dados até 2026-10-07 (`dados/F_cambio.md`).

| # | Informação (dado, divulgação, evento) | Data | Fonte · tabela |
|---|---|---|---|

## Rodadas

Rodada 1 → P1 → rodada 2 → P2 → report final → PF*. Dentro de uma rodada todos os agentes escrevem, sem ordem entre eles.

### Rodada 1 · câmbio · v1 (07/10, formato antigo)

- **Leu:**
  - Dados: `dados/F_cambio.md`.
  - Mapa conceitual: Partes 1–4 e o início da Parte 5.
  - Regras e modelos: `_modelo_report.md`, `manual_do_escrivao.md` (inteiro), `SISTEMA_AGENTES.md` (I.III, III, IV) e `PRINCIPIOS_AGENTES.md`.
  - Modelos mentais: `verde_fx_mental_models.md` (§1.9, §2.4, §5.3–5.5, §6.2, §6.3, §7.1–7.3) e `kapitalo_fx_mental_models.md` (§7.1 e os trechos sobre eleição).
  - Conceitos e sínteses: `concepts/exchange_rate_pass_through.md` e `synthesis/Cortapasso 2023`. A extração do Cortapasso está incompleta e não tem coeficiente citável.
  - Nenhum report de outro agente e nenhum P.
- **Escreveu:** report 1, hoje `cambio_r1_v1.md`.
- **Mudanças:** — (rodada 1).
- **Contas fora de G:** o report usa contas que nenhum G registra:
  - alta de 1,5% da PTAX em 14/09;
  - forward de 1 ano entre R$ 5,36 e R$ 5,40;
  - DI de 1 ano 8,89 p.p. acima da meta do Fed;
  - US$ 4,0 bi das intervenções contra a queda das reservas.

  A PTAX nos dias de intervenção (5,12 a 5,18) é leitura direta da base e não precisa de G. Desde 2026-10-07 a regra é: todo tratamento passa por G.

### Rodada 1 · câmbio · v2 (15/10, formato novo)

- **Leu:**
  - Dados: `dados/F_cambio.md`; o A, pelos G.
  - Mapa conceitual: Partes 1–4.
  - Regras e modelos: a definição do agente e `_modelo_report.md` (versões de 15/10), `manual_do_escrivao.md` (§1.2–1.3, §6–9), `PRINCIPIOS_AGENTES.md` e `SISTEMA_AGENTES.md` (I.II, IV.i, IV.iv, IV.vi–ix, V.I).
  - Modelos mentais: `verde_fx_mental_models.md` (§1.9–1.11, §2.4, §3.1–3.3, §5.3–5.5, §7.1–7.2) e `kapitalo_fx_mental_models.md` (§1.5, §3.2, §4.3–4.5, §6.8).
  - Conceitos: `exchange_rate_pass_through.md` e `carry_trade.md`.
  - Política monetária (vault): comunicado e ata da 281ª e RPM de set/2026, nos trechos sobre câmbio e petróleo.
  - Abriu este log sem usá-lo. Não leu a v1.
- **Escreveu:** report 1 (`cambio_r1.md`).
- **Mudanças:** — (rodada 1, refeita do zero).

## Funções G

Conta que o F(A) não faz. O código fica em `dados/G/`, lê os arquivos de `dados/A/` e nunca escreve no banco; o report e o relatório não citam o G, o rastro fica aqui. No fim do ciclo cada G fica como registro ou é promovido ao F.

| Agente · rodada | Arquivo | O que calcula | Resultado usado | Destino (registro · promover ao F) |
|---|---|---|---|---|
| câmbio · 1 v1 | `G/cambio_trajetoria_recente_v1.py` | Caminho diário e semanal desde jun/2026 de PTAX, pares, DXY, dólar contra emergentes, DI de 1 e 5 anos, CDS, Brent e Treasuries; intervenções diárias; reservas; fluxo contratado diário; COT do BRL | Salto de 02/10 → 05/10: PTAX −4,55%, DI 5a −135 p.b., DI 1a −70 p.b., DXY +0,24%, Treasury 10a +3 p.b. Janela 28/08 → 29/09: PTAX +0,4%, média dos pares +3,6%, DXY +1,7%. Datas das intervenções. Saídas financeiras de 01–02/09 (−US$ 6,2 bi) | a decidir |
| câmbio · 1 v1 | `G/cambio_faixas_e_analogos_v1.py` | Quantis da variação da PTAX em 39, 148 e 278 dias úteis; análogos dos 1º turnos de 2002–2022 com o DXY; fluxo financeiro contratado médio por mês em 2016–2025 | Faixas: 39 du de −3,3% a +3,5%; 148 du de 4,65 a 5,44. Análogos até o fim de novembro: 2014 +6,2%, 2018 +2,8%, 2022 +1,8%. Fluxo financeiro médio: dezembro −US$ 15,19 bi, novembro −US$ 2,34 bi | a decidir |
| câmbio · 1 v2 | `G/cambio_trajetoria.py` | Painel diário desde 20/06 (PTAX, DI 1a/2a/5a, Treasuries, DXY, dólar contra emergentes, pares, CDS); PTAX nos fechamentos de mês e trimestre; maiores variações diárias | PTAX 5,1809 (30/09), 5,2238 (02/10), 5,1766 (30/06), 5,5024 (31/12/25); −4,07% desde 30/09; −9,68% no ano; +1,52% em 14/09; −4,66% em 05/10 | a decidir |
| câmbio · 1 v2 | `G/cambio_global_idio.py` | Variação do real, dos pares e dos índices de dólar por janela; beta diário do real (jul/24–jun/26) e componente próprio | Beta 1,37 ao dólar contra emergentes (R² 0,33); setembro: global +2,68, próprio −2,70; 02/10–06/10: próprio −4,94; 3 meses: global +0,31, próprio −4,39 (log %) | a decidir |
| câmbio · 1 v2 | `G/cambio_forward_faixas.py` | Forward por paridade coberta (DI de 06/10, juro americano entre Fed Funds e Treasury 2a); distribuição histórica da variação da PTAX por prazo (out/16–out/26) | Forward 5,0676 · 5,1657 · 5,2638 · 5,3600 · 5,4455 · 5,5338 (4T26 a 1T28); massas das faixas candidatas | a decidir |
| câmbio · 1 v2 | `G/cambio_canais.py` | DI e Treasuries em 05/10 e desde 04/09; diferencial de juros por trimestre com a Selic da curva; carry/vol; diferencial de inflação; sazonalidade de dezembro; central contra spot, forward, Focus e condicionante | DI −70/−110/−135/−134 p.b. em 05/10; diferencial 9,38 a 8,32 p.p.; carry/vol 0,81; dezembro −US$ 12,56 bi contra +0,10; central 1,9% abaixo de R$ 5,15 | a decidir |

## Divergências abertas

Nenhuma com outro agente, porque este é um teste solo. Na v2, quatro premissas aguardam política monetária: a Selic igual à curva de 06/10 (S1), a leitura de credibilidade na cauda worst de 2027 (S2), a leitura do Copom sobre a apreciação de outubro (S3) e a função de reação na cauda worst do 4T26 (S4).

| Tema | Posição de <agente A> | Posição de <agente B> | Por que não se resolveu |
|---|---|---|---|

## Relatório

—
