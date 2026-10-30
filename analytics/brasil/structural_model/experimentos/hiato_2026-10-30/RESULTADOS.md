# Teste A do hiato · 2026-10-30

Decisão do usuário em `coordenacao/C_modelo.md` (Decisões, item 3a). Script: `hiato_a.py`.

Insumos (os do BC, boxe "Medidas de hiato do produto no Brasil", RPM jun/2024):
- NUCI da FGV, dessazonalizada por X-13;
- desocupação a.s. retropolada pelo BC;
- PIB e estoque do CAGED pelo filtro de Hamilton, que olha só para trás.

O corte de cada edição é respeitado; os valores de cada insumo são os de hoje, porque não há vintages deles.

## 1. Revisão do hiato por idade (trimestres já consolidados hoje)

|final − publicado| médio: 1,48 no trimestre da edição, 0,81 com 3 trimestres de idade, 0,51 com 8, 0,37 com 12.

Nessa amostra a revisão foi sempre para cima: o BC subestimou o hiato em 2021–2023, e a troca de
metodologia de 2024 também revisou a série. Nas edições desde 2024-09 a revisão já fica abaixo de
0,1 a partir de 9 trimestres.

## 2. Regressão no trecho consolidado da edição de 2026-09 (idade ≥ 12; 2004T3–2023T3, 77 tri)

S1: R² 0,865 · NUCI +0,191 (t 4,2) · desocupação −0,323 (t −3,7) · PIB +0,060 (t 1,1) · CAGED −0,025 (t −0,7).

- Quem explica são a NUCI e a desocupação. Dadas as duas, PIB e CAGED não acrescentam nada.
- **Instável:** de 2004–2014 para 2015–2023 a NUCI vai de 0,51 a 0,26 e a desocupação de −0,63 a −0,35.

## 3. Pseudo tempo real (9 edições avaliáveis, 2021-09 a 2023-09)

Ganho contra a primeira publicação do BC = 1 − erro da regressão / erro do BC.

| idade | ganho, treino na própria edição | ganho, treino na edição de hoje truncada |
|---|---|---|
| 0 | 39–44% | 49–50% |
| 1 | 26–32% | 30–32% |
| 2 | 14–17% | 18–21% |
| 6+ | negativo | negativo |

- **Sinal de 2022T4 a 2024T1, idades 0 a 2:** o BC acertou 0 de 12; a regressão, 8 ou 9 de 12.
- **Ressalva:** a avaliação é um episódio só, em que o BC errou sempre para baixo.

## 4. Hoje

| | 2025T4 | 2026T1 | 2026T2 | 2026T3 |
|---|---|---|---|---|
| publicado (2026-09) | +0,74 | +0,60 | +0,51 | +0,41 |
| regressão S1 (S0 no 3T) | +1,21 | +1,57 | +1,53 | +1,45 |
| só NUCI | −0,13 | +0,28 | +0,40 | — |

A desocupação de hoje (5,4%) está abaixo de qualquer trimestre do treino (mínimo 6,67%), então a
regressão extrapola. Contra 2023T3, a desocupação responde por +0,80 p.p. do hiato estimado e a NUCI
por +0,53. O p.p. de diferença para o BC é a pergunta da NAIRU: a regressão supõe uma NAIRU constante
de 2004 a 2023.

O CAGED pelo filtro de Hamilton dá −3,7 no 3T26, que tem só julho; vale conferir antes de usar.
