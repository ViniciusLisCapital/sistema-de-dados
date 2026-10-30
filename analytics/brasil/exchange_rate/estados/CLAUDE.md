# estados/ — estados do mercado de câmbio USD/BRL (Q0–Q4)

Pesquisa: classificar cada pregão num quadrante definido por dois eixos, se a **data** do evento é
conhecida e se o **resultado** é conhecido. Q0 é sem estado; Q1, data conhecida e resultado incerto; Q2,
surpresa; Q3, calendário de fluxo; Q4, processo com direção. Definições, regra de prioridade e casos de
fronteira em [`protocolo_rotulagem.md`](protocolo_rotulagem.md).

## Status

**Fase 1 (rótulos) e fase 2 (primeira estimação) entregues em 2026-10-29.** O usuário mandou estimar com
os rótulos como estão. Os erros do modelo servem para apontar rótulos a revisar (aba
`trechos_suspeitos`). A revisão dos rótulos é o próximo passo.

| arquivo | o que é |
|---|---|
| `rotulos_episodios.csv` / `.xlsx` | 193 trechos rotulados por notícia, com URLs. O `.xlsx` é a cópia de revisão; a fonte de verdade é o `.csv` |
| `rotular.py` | valida o CSV e gera o rótulo diário. Rodar: `uv run python analytics/brasil/exchange_rate/estados/rotular.py` |
| `rotulos_diarios.csv` | um rótulo por pregão da PTAX, de 2006-01-02 a 2026-10-28 |
| `modelo_markov.py` | fase 2: métricas, logit, HMM, validação, ablação. Rodar: `uv run python analytics/brasil/exchange_rate/estados/modelo_markov.py`, cerca de 15 min por causa da grade |
| `prob_estados_diaria.csv` | por pregão: rótulo e probabilidades. As colunas `filt_*` e `suav_*` são do modelo final, dentro da amostra; as `oos_*` são fora da amostra |
| `resultado_fase2.xlsx` | para o usuário: probabilidades, transição e duração, projeção, ablação, grade, separação par a par, confusão, sobreposição, régua antiga, piores dias, trechos suspeitos e coeficientes |
| `classificacao_regra_antiga.csv` | a classificação antiga por regra sobre métricas, copiada do scratchpad. Serve só para comparar |

Para mudar um rótulo, edite o `.csv` (não o `.xlsx`), rode o `rotular.py` e depois o `modelo_markov.py`.

**Regra que não se quebra:** os rótulos saem de notícias. Revisar um trecho porque o modelo errou nele é
legítimo. O que não vale é redesenhar as datas olhando vol, cupom, CDS ou juros: confirme pelas notícias.

## Decisões do usuário sobre os rótulos (2026-10-29)

O detalhe e os ids afetados por cada uma estão no protocolo, em "Casos de fronteira".

1. Tendências de fluxo, carry e dólar global continuam Q4 (A23, B01, C40, D01, D23, D30, D12, D32).
2. Surpresa em reunião com data marcada e sem aposta dividida é Q1 `evento`.
3. Rating esperado sem data não é Q2: é o desfecho do Q4 em curso (A12, B32 e B36 saíram).
4. Q2 dura no máximo ~10 pregões, e o resto vira Q4 com a direção do choque (linhas `…p`). Q2 de 11 a 12
   pregões ficaram como estavam.
5. O `antes` de eleição pode ir até 6 meses se houver evidência de câmbio reagindo às pesquisas (2014 desde
   17/03; 2018 desde 19/07).
6. O impeachment (C03) termina em 12/05/2016. O tapering foi partido em B15a e B15b.
7. A marca de Q3 em `sobreposicao` cobre novembro e dezembro.
8. Swap do BC e IOF só são Q2 se foram surpresa (A26 e B02 saíram).

## Fase 2 — como foi feita (2026-10-29)

- **Classes:** Q0, Q1, Q2, Q4u e Q4d. As fases do Q1 não são classe. O Q3 é a dummy de novembro–dezembro.
- **Métricas:** todas causais. O z-score é calculado contra os 252 e os 1.260 pregões **anteriores**, e o
  nível absoluto entra ao lado. Os blocos:
  - (a) câmbio (retornos de 1, 5, 21 e 63 dias divididos pela vol de 3M, distância das médias), vol
    implícita (nível, z, termo, vol menos realizada, movimento do evento), prêmio onshore (cupom limpo 3M
    menos o juro em dólar de 3M, ou o T-bill antes de 21/02/2008, como desvio da mediana dessazonalizado),
    dólar contra emergentes e Q3: 22 métricas;
  - (b) = (a) + CDS: 27 métricas;
  - (c) = (b) + DI de 1 ano, inclinação de 1 a 5 anos e NTN-B de 10 anos: 36 métricas.
- **Emissão:** logit multinomial L2 com pesos balanceados, de modo que p(x|y) ∝ p_bal(y|x). No filtro ela é
  elevada a τ, porque as métricas usam janelas sobrepostas e, sem têmpera, o filtro conta a mesma evidência
  muitas vezes (com τ = 1 o log-loss fica em 2–3).
- **Transição:** contada nos rótulos, mais 0,1 de pseudo-contagem. A regra proíbe a transição que nunca
  ocorre, mas todas as 20 ocorrem nos rótulos, então nenhuma ficou proibida.
- **Validação:** cada um dos 21 anos sai da amostra por vez. A purga tira do treino todo trecho que toca o
  ano de teste.
- **Escolha de C e τ:** pelo log-loss **balanceado** (média por classe). O log-loss comum premia nunca
  prever Q1 nem Q2. Resultado: C = 0,001, no limite da grade, o que é sinal de pouco sinal, e τ = 0,1.

## Fase 2 — resultados (fora da amostra)

- **Os estados se separam mal.** O logit sozinho tem log-loss balanceado de 1,52, contra 1,61 da
  probabilidade uniforme. O acerto balanceado é 0,32 a 0,40, contra 0,20 do acaso.
  - Separam bem (AUC par a par do logit): Q4u × Q4d (0,97), Q2 × Q4d (0,95), Q0 × Q2 (0,84) e Q0 × Q4
    (0,80–0,82).
  - Não separam: Q0 × Q1 (0,59), Q2 × Q4u (0,62), Q1 × Q2 (0,64) e Q1 × Q4u (0,68). O Q1 é quase
    invisível em todas as fases, inclusive no `evento`.
- **A camada de Markov não ganha do logit fora da amostra.** O log-loss balanceado da filtrada é 1,63 e o
  da suavizada 1,68, contra 1,52 do logit. Ela só ajuda o acerto balanceado da suavizada (0,40).
- **CDS e juros não ajudam.**
  - O CDS empata. No log-loss balanceado agregado, (b) contra (a) dá +0,001 no logit e −0,005 na
    filtrada. Ano a ano, melhora em 9 a 10 dos 21 anos.
  - Os juros pioram. (c) contra (b) dá +0,027 no logit e +0,044 na filtrada, e melhora em 9 a 10 dos 21
    anos.
- **Na sobreposição o modelo vê o fundo.** Dentro de um Q4, os Q1 e Q2 que venceram pela regra de
  prioridade saem como o Q4: 2016, 2015 e 2008. Os Q4 fiscais lentos de 2021 (C41) e de 2024 (D13) saem
  como Q0, com acerto de 0% e 8%.
- **Régua antiga:** acerto de 0,46 e acerto balanceado de 0,26, contra 0,51 e 0,40 do modelo suavizado.
  Ela erra mais justamente nas janelas de sobreposição.
- **Duração típica** (pregões), 1/(1 − p_ficar): Q0 38,5, Q1 14,9, Q2 7,6, Q4u 21,9 e Q4d 35,3.

## Ressalvas e próximos passos

- **Ressalvas dos dados:**
  - O CDS de 2026-09-09 a 2026-10-26 veio provisoriamente do investing.com. O CDS e o T-bill de 27 e
    28/10 repetem o último valor.
  - O cupom antes de 2012 é estruturalmente mais alto, por causa do IOF e da regulação.
  - O 1M da vol é ruidoso perto do vencimento; o 3M dilui eventos com data.
- **A escolha de C e τ pela mesma validação** que mede o resultado otimiza um pouco o número. São dois
  hiperparâmetros contra 21 dobras: o viés é pequeno, mas existe.
- **Próximos passos:**
  - Revisar os rótulos apontados em `trechos_suspeitos`.
  - Testar o modelo em camadas, com fundo (Q0/Q4u/Q4d) e evento (Q1/Q2) separados. Com um rótulo só, a
    regra de prioridade apaga o fundo, que é o que as métricas veem.
