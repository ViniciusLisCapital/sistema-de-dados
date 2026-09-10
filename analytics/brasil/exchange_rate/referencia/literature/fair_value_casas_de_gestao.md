# Nível justo do USDBRL — o que as casas de gestão dizem (levantamento 2026-09-08)

Levantamento do que gestoras brasileiras publicaram sobre **valor justo / câmbio de
equilíbrio** do USDBRL, cruzando o corpus interno de cartas
(`repository/mental_model/`, via `fx_attribution_data/`) com declarações públicas
na imprensa. Não é uma projeção nossa — é um inventário de quem afirma o quê, com
que método, e contra que spot.

## O achado que organiza tudo

**Uma única gestora brasileira publica um número: a Verde.** Todas as outras falam
em direção, em prêmio de risco ou em posição — nunca em nível. Isso não é falta de
modelo (a Kapitalo diz explicitamente que roda "projeções de câmbio de equilíbrio"),
é decisão de não publicar o nível.

## Âncoras de spot (PTAX venda, `macro_brasil.cmb_ptax`)

| data | PTAX | o que é |
|---|---|---|
| 2025-01-02 | 6,2086 | máxima histórica |
| 2024-12-31 | 6,1923 | fecho de 2024 |
| 2025-12-31 | 5,5024 | fecho de 2025 |
| 2026-01-02 | 5,4372 | máxima de 2026 |
| 2026-05-11 | 4,8973 | mínima de 2026 |
| 2026-09-04 | 5,1253 | último dado na base |

## Gestoras

### Verde Asset — R$ 4,40, e é o único número
Luis Stuhlberger, LAIC/UBS, **27/01/2026** (PTAX do dia: **5,2392**):

> "A gente tem impressão, pelos nossos modelos, que o *fair value* dele hoje é
> R$ 4,40." · "O câmbio hoje, na nossa opinião, está ainda extremamente fora do lugar."

**Canais do modelo** (Brazil Journal): dólar contra uma cesta de moedas emergentes
mais o DXY; diferencial Selic − Fed Funds; índice de commodities; CDS do Brasil.

**Duas ressalvas que importam:**

1. **Os dois números do desalinhamento não fecham e nenhuma fonte reconcilia.**
   R$ 4,40 contra 5,2392 é ~16%; ele fala em "**25% fora do lugar**" (Brazil Journal)
   / "26%" (Forbes), equiparando a situação ao fim de 2024, com o dólar acima de R$ 6.
   O mais provável é que os 25% sejam o resíduo do modelo na série de desvio e os 16%
   a razão simples spot/fair value — mas isso é inferência nossa, ninguém afirma.
2. **Valor justo não é posição.** A carta de **maio/2026** zerou a alocação em real
   ("Zeramos as alocações em Real"), pela volta do excepcionalismo americano, e as
   cartas de junho, julho e agosto seguem sem posição na moeda. A âncora de valuation
   convive com risco zero na moeda há quatro meses.

Atribuição do gap, nas palavras dele: "fiscal descontrolado e a expansão fiscal";
o câmbio aprecia quando a disciplina fiscal melhora (cita o teto de gastos do Temer).
E o fluxo estrangeiro "ignora solenemente a questão eleitoral".

### Legacy Capital — o dólar é que está caro
Pedro Jobim, **26/02/2026** (PTAX **5,1382**). O otimismo com o real é o ponto central
da tese do ano: com o **dólar historicamente caro numa janela de 50 anos**, o real é
destino natural do fluxo estrangeiro; a taxa "pode chegar a R$ 5 e até romper esse
patamar num horizonte" relativamente curto. Fundos vendidos em dólar contra uma cesta
que inclui o real.

Construção diferente da Verde: é uma avaliação **do dólar**, não do real — não produz
um nível bilateral, produz uma direção.

### Kapitalo — tem o modelo, não publica o nível, e lê ao contrário
- **jun/2024**: "Nossas projeções de conta corrente pioraram… subindo levemente nossas
  projeções de **câmbio de equilíbrio**." O modelo existe e é puxado pela conta corrente.
- **set/2025**: "o **câmbio apreciado** e o baixo nível de reservas são fragilidades";
  uma eleição legislativa razoável traria "câmbio mais depreciado e reservas mais elevadas".
- **dez/2025**: "os **prêmios de risco (câmbio**, inflação implícita, spreads de crédito,
  equity risk premium) **são muito baixos** e subestimam sobremaneira os riscos de
  continuidade da atual política econômica."

É a leitura **oposta** à da Verde sobre o mesmo objeto: para a Verde o real está barato
demais para os fundamentos; para a Kapitalo está caro demais para o risco de política.

### Kinea — tático, sem nível, e virou no meio do ano
- **nov/2021**: "Não só temos uma moeda barata, mas logo passaremos a ter um dos maiores
  carregos do mercado global." (barateza invocada, nunca precificada)
- **jan/2026**: "viés na ponta comprada em real, sustentada pelo elevado diferencial de
  juros… e pelo carrego ainda bastante atrativo."
- **abr/2026**: comprado em BRL contra moedas europeias, vendido em peso mexicano como
  proteção.
- **jun/2026**: virou — "Preferimos o dólar a moedas vulneráveis… cautela com Brasil."
- **ago/2026**: "exposição neutra ao país durante o período eleitoral".

### Outras — posição, não valuation
Itaú Asset (Bruno Serra) abriu 2026 vendida em USDBRL pelo carry e virou comprada em
dólar no meio do ano, por Fed mais duro e preocupação fiscal. SulAmérica, Vinland, Genoa
e Vista compunham o consenso de dólar fraco na largada de 2026 — Vista com a ressalva de
João Landau ("com esse nível de endividamento e com juros reais estruturalmente mais
altos, o país perde graus de liberdade"). Ibiuna comprou dólar contra real como hedge no
início de 2026 mantendo posições compradas em moedas da China e da América Latina.
**Armor Capital** (Alfredo Menezes, 16/04/2026) é a exceção que quase dá um número: a
força do real se apoia em dois pilares — petróleo a ~US$ 90 (≈US$ 20 bi de superávit
comercial extra) e um dos maiores juros reais do mundo — e não deve durar; vê o dólar
voltando à faixa de R$ 4,90 como piso.

## Sell side — é quem publica nível, e serve de triangulação

| casa | número | data | racional |
|---|---|---|---|
| Morgan Stanley | preços "justos"; R$ 4,50 **só** com consolidação fiscal | 18/05/2026 (spot 5,0093) | prêmio de risco fiscal excedente ≈ zero; país negocia em linha com o rating |
| Goldman Sachs | 4,90 / 5,00 / 5,00 (3/6/12m) | 28/04/2026 (spot ~4,98) | revisado de 5,20/5,30/5,30 |
| Goldman Sachs | 5,20 / 5,10 (3/6m) | 18/08/2026 (spot 5,2043) | revisão de volta, "o mercado passou a atribuir maior peso à incerteza política" |
| Itaú BBA | 5,30 fim de 2026 | 18/08/2026 | aperto adicional nos EUA + prêmios domésticos elevados |
| BTG · XP · BofA · BNP | 4,90 · 5,00 · 4,95 · 4,90 | 1S2026 | todas revisadas para baixo no rali |
| Focus (BCB) | 5,20 fim de 2026 | 08/2026 | mediana de mercado |
| Citi | saiu do real, trocou pelo rand | 18/08/2026 | risco eleitoral, não valuation |
| IIF (Robin Brooks) | R$ 4,50 | 28/06/2021 (spot 4,90) | boom de exportação de commodities + conta corrente perto de +2% do PIB |

O **BTG** publicou em 20/06/2026 uma decomposição do USDBRL (Elastic Net + filtro de
Kalman) separando fator global e componente idiossincrático: *"Em 2025, o real foi
global. Em 2026, está sendo exclusivamente Brasil."*

## A dispersão, e de onde ela vem

Os números publicados vão de **R$ 4,00–4,50** (construções de conta corrente / PPP
ajustada) a **R$ 6,70** (PPP relativa ingênua, IPCA contra CPI desde 2003). Não é
desacordo sobre o Brasil — é escolha de construção. A PPP relativa depende do **mês-base**
por definição, e é exatamente por isso que o `ppp_equilibrium.py` deste projeto não a
trata como valor justo isolado, e sim como o termo de **offset** do modelo Ridge.

## O que isso diz sobre o nosso próprio modelo

**O conjunto de canais que a Verde publica é quase o nosso.**

| Verde (publicado) | nosso Ridge (spec de 2026-09-01) |
|---|---|
| dólar contra cesta EM + DXY | `dxy_em` |
| diferencial Selic − Fed Funds | `carry_vol` |
| índice de commodities | `icbr_usd` |
| CDS do Brasil | `fiscal` |
| — | `sp500` |
| — | AR(1) + PPP com β fixo em 1 |

Duas diferenças carregam peso. Usamos o carry **por unidade de volatilidade realizada**
em vez do diferencial cru — medido, o cru não é estável em sinal entre janelas de 72
meses. E carregamos a PPP explicitamente como offset em vez de deixá-la no intercepto:
é justamente esse termo que transforma um "desvio" em um **nível** de valor justo, que
é o que a Verde publica e nós hoje não publicamos.

## Fontes

- Brazil Journal, 27/01/2026 — *Valor justo do dólar é R$ 4,40, diz Stuhlberger*
- CNN Brasil / Forbes Brasil / Seu Dinheiro, 27/01/2026 — mesma fala, LAIC/UBS
- Seu Dinheiro, 26/02/2026 — Legacy, *Touros e Ursos* #260
- Seu Dinheiro, 16/04/2026 — Armor Capital
- Seu Dinheiro, 10/06/2026 — Verde zera a posição em real
- InfoMoney, 17/01, 20/01, 28/04, 18/05, 18/08/2026 — consenso de multimercados,
  revisões de projeção, prêmio eleitoral
- Bora Investir/B3, 05/08/2026 — compilação de projeções para o fim de 2026
- dunderdog (Christian Lupinacci), 20/06/2026 — modelo do BTG
- Cartas: `repository/mental_model/{verde_asset,kinea,kapitalo}/`

## Pendências

- **Nenhuma casa foi lida em fonte primária para as declarações de imprensa** — as falas
  de Stuhlberger, Jobim e Menezes vêm de reportagem, não de carta. Se alguma virar base
  de decisão, vale procurar o material original.
- **SPX Capital** tem 7 PDFs em `repository/mental_model/spx_capital/raw_pdf/` sem
  extração; Rogério Xavier fala publicamente de câmbio e não entrou neste levantamento
  por falta de declaração de nível.
- **Não publicamos nosso próprio nível.** O Ridge entrega desvio; com o offset de PPP já
  dentro do modelo desde 2026-09-01, produzir um número comparável ao R$ 4,40 da Verde é
  uma soma, não um modelo novo.
