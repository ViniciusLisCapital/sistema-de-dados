# Teste da âncora da (R) e da (H) · 2026-10-30

Decisão do usuário em `coordenacao/C_modelo.md` (Decisões, item 2): sem QPC; a âncora `rr_10a + meta`
contra a mesma com o juro de 10 anos em média móvel de 4 e 8 trimestres, e como variante extra a
média como âncora e o desvio do cru contra ela como regressor da (H). Script: `ancora.py`.

Amostra comum 2008T2–2026T3, 74 trimestres. Fora da amostra: estimação recursiva desde 2016T1, 43 origens.

## Pesos

| | t1 | t2 | t3 (LP) | h2 (t) | h3 desvio (t) |
|---|---|---|---|---|---|
| (0) cru, hoje | 1,392 | −0,550 | 1,80 | −0,075 (−2,1) | — |
| (1) MM4 | 1,507 | −0,655 | 1,68 | −0,073 (−2,1) | — |
| (2) MM8 | 1,558 | −0,701 | 1,76 | −0,065 (−2,0) | — |
| (1b) MM4 + desvio | 1,507 | −0,655 | 1,68 | −0,075 (−2,1) | **+0,064 (0,3)** |
| (2b) MM8 + desvio | 1,558 | −0,701 | 1,76 | −0,076 (−2,1) | **+0,078 (0,5)** |
| BC | 1,41–1,54 | −0,63 a −0,52 | 1,47–2,64 | | |

O desvio entra com o sinal **oposto** ao de custo de capital, e não é significativo.

## Fora da amostra, RMSE contra a variante (0)

Duas leituras, e elas discordam:
- **condicional:** cada equação recebe a NTN-B, a Focus e a Selic que de fato aconteceram;
- **como o simulador roda:** NTN-B, Focus e meta ficam paradas na origem; a Selic sai da (R) e o hiato lê essa Selic.

| | Selic h1/h4/h8, condicional | Selic h1/h4/h8, simulador | hiato h1/h4/h8, condicional | hiato h1/h4/h8, simulador |
|---|---|---|---|---|
| (1) MM4 | −23% / +4% / +8% | **−23% / −6% / −2%** | +2% / +5% / +11% | **+2% / +5% / −6%** |
| (2) MM8 | −21% / +14% / +24% | −22% / −5% / −2% | +2% / +6% / +13% | +2% / +6% / −7% |
| (1b), (2b) | iguais a (1), (2) | iguais | +5% / +12% / +17% | +5% / +12–14% / +2% |

A vantagem do 10 anos cru na leitura condicional existe só conhecendo a NTN-B realizada, que o
mercado forma olhando a própria Selic (a correlação de +0,80 da pendência R2). Projetando, ela não
está disponível.

## 1 p.p. permanente na NTN-B de 10 anos (diferença contra o base, trimestres 1/2/4/8/12)

| | Selic | hiato |
|---|---|---|
| (0) | +1,00 em todos | 0 |
| (1) MM4 | +0,25 / +0,50 / +1,00 / +1,00 / +1,00 | 0 |
| (2) MM8 | +0,12 / +0,25 / +0,50 / +1,00 / +1,00 | 0 |
| (1b) | como (1) | +0,05 / +0,08 / +0,05 / +0,03 (sobe) |
| (2b) | como (2) | +0,07 / +0,15 / +0,17 / +0,10 (sobe) |

Em toda variante a Selic acompanha a âncora, então o aperto não muda e o hiato não se mexe. A média
móvel só atrasa a passagem. Fazer o salto da NTN-B apertar o hiato exige um neutro separado do
prêmio, que saiu do teste junto com o QPC.

Hoje (2026T3): âncora 10,84 (cru), 10,63 (MM4), 10,49 (MM8); aperto 3,22 / 3,42 / 3,57.
