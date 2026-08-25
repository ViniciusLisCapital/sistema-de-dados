"""
Monta o dataset da aba "PTC" do Panorama de Credito.

Fonte: Pesquisa Trimestral de Condicoes de Credito (PTC) do BCB, tabela
macro_brasil.cred_ptc -- 16 series = 4 segmentos x 2 direcoes (oferta/demanda) x 2
horizontes (observada = ultimos 3 meses, esperada = proximos 3 meses), trimestral desde
2011-04. E o equivalente brasileiro ao Senior Loan Officer Opinion Survey do Fed / Bank
Lending Survey do BCE: os proprios bancos respondem se afrouxaram ou apertaram a
concessao e se viram mais ou menos procura.

Metodologia oficial (nao inferida): Annibal, C. A. & Koyama, S. M. (2011), "Pesquisa
Trimestral de Condicoes de Credito no Brasil", BCB Trabalhos para Discussao 245
(https://www.bcb.gov.br/pec/wps/port/TD245.pdf) — o desenho da pesquisa, a escala e a
formula dos indicadores; mais a nota "Introducao" de qualquer relatorio trimestral da
PTC (ex. https://www.bcb.gov.br/content/publicacoes/ptc/202406/RelatorioPTC-Junho2024.pdf).
ATENCAO: a nota de rodape desses relatorios cita "Trabalhos para Discussao 254" — e
erro de digitacao do proprio BCB; o TD 254 e um paper de regulacao macroprudencial de
outros autores. O da PTC e o 245.

## Como o numero e construido

Cada respondente escolhe UM de cinco niveis, convertidos para inteiros de -2 a +2, e o
indicador publicado e a MEDIA ARITMETICA SIMPLES dessas respostas no segmento:

    I(segmento, trimestre) = (1/N) * SOMA_b resposta_b,   resposta_b em {-2,-1,0,+1,+2}

com N = numero de instituicoes que responderam aquela questao naquele trimestre. Nas
palavras do relatorio trimestral: "as avaliacoes sao convertidas em valores entre -2 e 2
e sao apresentadas as medias NAO PONDERADAS das respostas".

Nao e um "saldo liquido" de respostas (% que apertou menos % que afrouxou), que e a
forma como muitos surveys de credito — inclusive o SLOOS do Fed — publicam seus
numeros. Uma versao anterior desta docstring dizia isso e estava errada: aqui os niveis
tem peso 1 e 2, entao intensidade e direcao entram no mesmo numero.

A ausencia de ponderacao por participacao de mercado e escolha deliberada, nao lacuna:
o TD 245 registra que essa e a pratica internacional dominante "pelo fato de que as
pesquisas ja seriam naturalmente direcionadas as maiores instituicoes financeiras de
cada regiao" — o painel da PTC cobria 92,4% a 99,7% do credito de cada segmento na
primeira rodada.

## A escala, e o que cada faixa significa

    +2  consideravelmente mais flexivel     |  demanda consideravelmente mais forte
    +1  moderadamente mais flexivel         |  demanda moderadamente mais forte
     0  basicamente inalterado              |  demanda no mesmo nivel
    -1  moderadamente mais restritivo       |  demanda moderadamente mais fraca
    -2  consideravelmente mais restritivo   |  demanda consideravelmente mais fraca

Logo o indice vai de -2 a +2 (e NAO de -1 a +1, como diz o COMMENT da tabela no MySQL —
19 dos 976 pontos passam de 1 em modulo justamente porque o teto e 2). Como e uma media
de niveis rotulados, a magnitude tem leitura direta: |I| ~ 1 significa "o respondente
medio marcou 'moderadamente'", |I| ~ 2, "'consideravelmente'". Um -0,32 nao e "32% dos
bancos apertaram" — e "o banco medio ficou a um terco do caminho entre 'inalterado' e
'moderadamente mais restritivo'", ou seja, aperto brando. Nos proprios relatorios do BCB
a escala aparece como gradiente de cor, de vermelho pleno em -2 a verde pleno em +2.

Zero e o ponto em que as respostas se cancelam, nao "condicoes neutras": um segmento
pode marcar 0 com metade do painel apertando e metade afrouxando.

Cuidado com o sinal ao ler o TD 245: no questionario de demanda as alternativas sao
listadas de "substancialmente mais forte" (1) para "substancialmente mais fraca" (5),
ordem INVERSA da conversao numerica publicada. Na serie divulgada, e nesta tabela,
positivo = demanda maior. Confirmado ao vivo (ver a validacao adiante).

## O painel e pequeno, e isso limita a granularidade

Sendo media simples de N respostas, o indice so pode assumir multiplos de 1/N: uma
unica instituicao mudando de nivel move o indice em 1/N. Recuperando o N implicito da
propria base (menor N que explica os 4 indicadores de um segmento num trimestre, dado o
arredondamento de 2 decimais), o N modal por segmento bate com os participantes que o
BCB publica na rodada de junho/2024:

    grandes empresas   N modal 22   (BCB jun/2024: 22)
    MPME               N modal 28   (BCB jun/2024: 28)
    PF consumo         N modal 17   (BCB jun/2024: 17)
    PF habitacional    N modal  7   (BCB jun/2024:  7; TD 245, 2011: 8)

Implicacao de leitura: em PF Habitacional o passo minimo do indice e ~0,14 (1/7) e nos
primeiros anos ~0,13 (1/8) — a serie so consegue se mover em degraus grossos, e uma
variacao de 0,14 ali e UM banco mudando de opiniao, nao mudanca de regime. E o oposto
de MPME, com ~28 respondentes e passo ~0,04. Nao comparar amplitude entre segmentos sem
isso em conta.

## O que o numero nao e

Nao e inadimplencia, nao e probabilidade de default e nao e volume: e percepcao
declarada, uma leitura qualitativa que antecede o dado quantitativo das outras abas. O
proprio BCB adverte que os resultados "representam unicamente a visao das instituicoes
financeiras pesquisadas", nao a do Banco Central.

Convencao de sinal confirmada ao vivo contra episodios conhecidos (2026-08):
  - Recessao 2015-2016: oferta observada em -1,08 (grandes empresas, 2015-T3 e 2016-T1)
    e -1,12 (MPME, 2016-T1), com demanda tambem negativa -- aperto de credito
    generalizado com retracao de procura, exatamente o quadro do periodo. Note que -1,08
    quer dizer "o banco medio apertou um pouco MAIS que 'moderadamente'".
  - COVID, 2020-T2: oferta negativa em todos os 4 segmentos (-0,77 grandes, -0,53 MPME)
    ao mesmo tempo que a demanda PJ DISPARA (+0,91 grandes, +0,63 MPME) e a demanda de
    PF consumo colapsa (-0,90). E a assinatura classica do "dash for cash" corporativo
    -- empresas sacando linhas ja contratadas -- contra o recuo do consumo das familias.

## Por que nao existe linha de total

O BCB nao publica no SGS (nem nos relatorios) nenhum agregado "todos os segmentos" da
PTC — so os 16 codigos por segmento. E somar/mediar os 4 segmentos aqui nao reproduz a
conta do BCB: a media simples do BCB e sobre INSTITUICOES DENTRO de um segmento, com o
painel e o questionario daquele segmento. Uma media entre segmentos misturaria paineis
de tamanhos diferentes (7 a 28 respondentes) e universos de credito de tamanhos muito
diferentes, produzindo um objeto que nao e o indice de nada. Decisao explicita do
usuario (2026-08): NAO sintetizar total.

Os dois nos de topo ("Oferta" e "Demanda") sao, por isso, nos CABECALHO -- seriesKey com
sufixo "_header" que deliberadamente nao existe em `series`, sem checkbox e sem coluna de
valor, so expansor. Mesmo padrao de "Por Porte de Empresa" em inadimplencia_tab.py.

## Horizonte como variante, nao como no da arvore

`series[seriesKey]` = {"observada": {...}, "esperada": {...}, "desvio": {...}} -- a pill
Observada|Esperada troca qual das duas primeiras variantes a tabela le, sem mexer na
arvore; a terceira nao entra na pill, e a tabela/grafico de surpresa (adiante) le so ela. Mesma forma de
payload que impulso_tab.py usa para Mensal|Anual. Decisao explicita do usuario
(2026-08): horizonte e um seletor, nao um terceiro nivel de arvore -- mantem a tabela
em 8 linhas de dado em vez de 16 e deixa a comparacao entre segmentos, que e a leitura
principal, na mesma tela.

Aferido ao vivo: a expectativa dos bancos acerta a DIRECAO com frequencia alta --
esperada(t-1) tem o mesmo sinal de observada(t) em 47 dos 52 trimestres comparaveis de
ge_oferta. Ou seja, as duas variantes contam quase a mesma historia deslocada de um
trimestre; o valor de alternar esta em ver antecipacao de virada, nao divergencia.

## Surpresa: observado contra o que os bancos esperavam um trimestre antes

Como a pesquisa pergunta as duas coisas na mesma rodada -- o que aconteceu nos ultimos 3
meses E o que se espera para os proximos 3 --, a serie `esperada` de um trimestre e uma
previsao verificavel pelo `observada` do trimestre seguinte. O desvio e:

    desvio(t) = observada(t) - esperada(t-1)

Isto e, o realizado do trimestre t contra a expectativa que os proprios bancos
declararam em t-1 exatamente sobre t. Positivo = veio ACIMA do esperado (aprovacao mais
frouxa, ou procura mais forte, do que o painel previa); negativo = veio ABAIXO.

Tres armadilhas nessa conta:

1. O alinhamento e defasado de um trimestre, nao contemporaneo. Comparar observada(t)
   com esperada(t) e comparar o realizado com uma previsao sobre o trimestre SEGUINTE --
   nao e surpresa nenhuma, e a diferenca entre dois periodos diferentes. Aqui o `t-1` e
   calculado por aritmetica de calendario (mes -3, com jan -> out do ano anterior), nao
   por deslocamento de indice, para nao inventar par se um dia faltar um trimestre.
2. O primeiro trimestre da amostra (2011-T2) nao tem desvio -- nao existe expectativa
   anterior a ele. A serie de desvio tem, por construcao, um ponto menos que as outras.
3. As duas medias sao sobre paineis de trimestres diferentes, e nem o N e o mesmo: o
   respondente de t-1 nao e necessariamente o de t. Logo a diferenca NAO cai numa grade
   de 1/N -- ver adiante.

## A faixa "em linha" e o sigma da propria serie, e nao 1/N (correcao 2026-08)

A primeira versao desta aba marcava "em linha" como |desvio| <= 1/N do segmento, com o
argumento de que um desvio desse tamanho "cabe em uma instituicao tendo mudado de
opiniao". O argumento nao se sustenta, e o usuario apontou o furo:

- 1/N e a RESOLUCAO do indice num trimestre com N fixo, nao um piso de relevancia. Um
  desvio de 1/N e apenas COMPATIVEL com um respondente ter se movido; ele tambem sai de
  cinco subindo um nivel e quatro descendo, que e muita mudanca de opiniao, nao pouca.
  O que 1/N da corretamente e um LIMITE INFERIOR na outra direcao: |desvio| * N
  arredondado para cima e o minimo de respondentes que tem de ter mudado de nivel (o
  +0,26 de grandes empresas em 2026-T2 exige >= 6 dos 22). Isso vale, e por isso virou
  informacao de hover no grafico, em vez de faixa.
- A grade de 1/N so existe se N for igual nos dois trimestres, e nao e. Teste direto na
  base: se N fosse sempre 7 em PF Habitacional, 100% dos desvios cairiam em multiplos de
  1/7; caem 52%-58%. (Em grandes empresas 90% "passam", mas ali o teste nao tem poder --
  com N=22 o passo 0,045 e proximo do arredondamento de 0,01 publicado, entao quase
  qualquer valor passa.) Onde o teste tem poder, ele refuta a grade.
- Nao existe modelo amostral aqui para chamar nada de "ruido": o painel e um censo de si
  mesmo, e um desvio pequeno e uma resposta de verdade que por acaso deu pequena.

O que ficou: faixa de +-sigma_0 calculada sobre a HISTORIA DE DESVIOS DAQUELA PROPRIA
serie (`_desvio_rms`), centrada em zero. Responde "esta surpresa e grande para o padrao
desta serie?", que e uma pergunta com resposta nos dados, e nao afirma nada sobre quantos
bancos se moveram. Centrada em zero, e nao na media dos desvios, de proposito: zero e o
ponto de nenhuma surpresa, que e o que a faixa tem de referenciar -- centrar na media
responderia "em linha com o vies habitual", outra pergunta.

E porque a faixa e centrada em zero, a LARGURA tambem e medida em torno de zero: sigma_0 e
o RQM, sqrt(media(v^2)), nao o desvio-padrao em torno da media da serie. Ate 2026-08 era o
desvio-padrao, e isso era um bug -- os dois centros nao combinavam e serie enviesada
acusava quase tudo (ver _desvio_rms para o caso de pfc_demanda e os numeros do antes/depois).

Descritivo sobre os 60 desvios que existem, nao inferencia sobre uma populacao maior. Fica
entre 0,14 (mpme_oferta) e 0,37 (pfh_demanda) -- 2,6x de amplitude, que e a razao de a
faixa continuar sendo POR SERIE e nunca uma faixa comum. Uma escala robusta em torno de
zero (mediana de |v| / 0,6745) fica a menos de 0,04 disso, ou seja 2015-16 e 2020 nao
estao inflando a conta.

Achado lateral, registrado sem exagerar a forca: a media dos desvios e negativa em tres
das quatro series de demanda (-0,06 a -0,09) e ~0 nas de oferta, isto e, os bancos tendem
a prever demanda um pouco mais forte do que a que reportam depois. Com 60 trimestres
autocorrelacionados isto NAO esta sendo chamado de significante.

## Media movel de 4 trimestres (`desvio_ma4`), a leitura principal desde 2026-08

A pedido do usuario, a tabela e a linha grossa do grafico mostram a MEDIA MOVEL DE 4
TRIMESTRES do desvio, nao o desvio trimestral cru -- a pergunta passa a ser "os bancos
vem erradando para o mesmo lado ao longo de um ano?" em vez de "erraram neste trimestre?".
Media APARADA A DIREITA (trailing): o ponto de t e a media de t-3..t, entao cada ponto e
"o ultimo ano fechado naquele trimestre" e nada olha para o futuro. Perde os 3 primeiros
pontos: 57 contra 60.

So agrega janelas de 4 trimestres CONSECUTIVOS de calendario, checadas com
_trimestre_anterior() -- se um dia faltar um trimestre na base, a janela e descartada em
vez de mediar pontos que estao a mais de um ano de distancia entre si.

Duas consequencias que precisam estar registradas:

1. O sigma_0 da MA NAO e o do desvio trimestral -- e cerca de metade dele (razoes
   medidas de 0,38 a 0,69, media 0,51). Logo a faixa "em linha" da MA e a propria
   (`desvio_ma4.rms`), nunca a do trimestral: usar a trimestral deixaria a MA dentro da
   faixa quase sempre, e nada pareceria surpresa. Como a tabela passou a mostrar a MA, a
   faixa do grafico tambem e a da MA, para tabela e grafico nao discordarem sobre o que e
   "em linha". A faixa da MA vai de 0,06 (pfc_oferta) a 0,20 (pfh_demanda), 3,4x.
2. A razao ~0,50 e exatamente o que se esperaria se os desvios fossem INDEPENDENTES entre
   trimestres (sd da media de k valores iid = sd/raiz(k) = sd/2 para k=4). E os AR(1)
   medidos ficam entre -0,23 e +0,21, ou seja quase nenhuma persistencia. Consequencia
   honesta: a MA aqui esta sobretudo MEDIANDO RUIDO INDEPENDENTE, nao revelando um ciclo
   lento -- ela suaviza, mas nao se deve ler tendencia forte onde a persistencia e ~0. O
   que a MA mostra bem e vies acumulado: a MA de ge_demanda saiu de +0,07 para -0,14 nos
   4 ultimos trimestres, um ano de demanda de grandes empresas vindo abaixo do previsto,
   que nenhum trimestre isolado deixa ver.

Janelas VIZINHAS COMPARTILHAM 3 dos 4 trimestres, entao os pontos da MA sao fortemente
correlacionados por construcao -- nao ler duas celulas vizinhas da tabela como duas
observacoes independentes.

Aferido ao vivo (2026-08): em ge_oferta a expectativa acerta a direcao em 47 dos 52
trimestres comparaveis -- o desvio e pequeno na maior parte do tempo, e e justamente por
isso que os poucos trimestres em que ele estoura merecem atencao (2020-T2, 2016).
"""
from analytics.report_structure import tree_helpers as th

_direct = th.direct

HORIZONTES = ("observada", "esperada")

# Limites teoricos da escala de resposta (-2 a +2), e o ponto onde o respondente medio
# marcou "moderadamente" (+-1). O relatorio desenha guias nesses niveis para dar
# significado a magnitude -- ver a docstring, secao "A escala".
ESCALA = {"min": -2, "max": 2, "moderado": 1}

# 4 segmentos da pesquisa, na ordem em que o BCB os publica (PJ do maior para o menor,
# depois PF por finalidade). Prefixos batem com os nomes de serie de cred_ptc.
# `n_respondentes`: painel da rodada de junho/2024 do BCB, que e tambem o N modal
# recuperado da propria serie (ver docstring) -- entra no relatorio para o leitor saber
# o passo minimo do indice em cada segmento (1/N).
_SEGMENTOS = [
    ("ge",   "Grandes Empresas", 22),
    ("mpme", "MPME (Micro, Pequenas e Médias)", 28),
    ("pfc",  "Pessoa Física — Consumo", 17),
    ("pfh",  "Pessoa Física — Habitacional", 7),
]

# Oferta e Demanda no topo (decisao explicita do usuario, 2026-08 -- e como o SLOOS do
# Fed se le: condicao de oferta contra condicao de demanda, cada uma comparada entre
# segmentos). Ambos sao nos-cabecalho, sem serie propria -- ver docstring do modulo.
_DIRECOES = [
    ("oferta",  "Oferta — Flexibilidade de Aprovação"),
    ("demanda", "Demanda — Procura por Crédito"),
]


def _segmento_node(seg: str, seg_label: str, n: int, direcao: str) -> dict:
    node = _direct(f"{seg}_{direcao}", seg_label)
    node["n"] = n
    return node


PTC_TREE = [
    _direct(
        f"{direcao}__header",
        label,
        [_segmento_node(seg, seg_label, n, direcao) for seg, seg_label, n in _SEGMENTOS],
    )
    for direcao, label in _DIRECOES
]

# Serie de referencia das datas do cabecalho de colunas. Qualquer uma serve -- as 16
# tem exatamente as mesmas 60 datas (confirmado ao vivo, nenhum buraco em nenhuma) --
# mas fixar uma torna a tabela imune a uma eventual divergencia futura.
ANCHOR = "ge_oferta"


def _trimestre_anterior(date_str: str) -> str:
    """Data do trimestre imediatamente anterior, por calendario (as series sao datadas em
    jan/abr/jul/out). Aritmetica de mes -3 em vez de indice-1 para que um eventual buraco
    na serie produza desvio ausente, nao um par errado."""
    y, m, d = (int(x) for x in date_str.split("-"))
    return f"{y - 1:04d}-10-{d:02d}" if m == 1 else f"{y:04d}-{m - 3:02d}-{d:02d}"


def _desvio_rms(values: list) -> float | None:
    """Dispersao dos desvios da propria serie medida EM TORNO DE ZERO: raiz do quadrado
    medio, sqrt(media(v^2)). Nao e o desvio-padrao (que mede em torno da MEDIA da serie).

    A distincao nao e cosmetica, e foi um bug ate 2026-08: a faixa "em linha" e centrada
    em zero, porque zero e o ponto de nenhuma surpresa. Medir a dispersao em torno da
    media e desenhar a faixa em torno de zero mistura dois centros, e numa serie com vies
    a faixa passa a acusar quase tudo -- pfc_demanda tinha media -0,09 contra sd 0,09,
    isto e o vies inteiro cabia dentro de um sigma, e 8 das 12 celulas visiveis saiam da
    faixa so por a serie ser ela mesma. O RQM absorve isso por construcao:
    RQM^2 = media^2 + variancia, logo uma serie enviesada ganha faixa mais larga, e
    sobra pintado o trimestre que e de fato atipico.

    Efeito medido na troca (MA 4T, 57 pontos): cobertura da faixa passou de 49%-68% entre
    as 8 series para 61%-70%, agrupada em torno dos ~68% que "1 sigma" sugere; celulas
    pintadas nas 12 colunas visiveis cairam de 31 para 23 de 96 (contadas na precisao
    exibida; 36 -> 27 na precisao cheia). O que era sinal ficou:
    pfh_oferta segue com 9 de 12 fora, porque ali a surpresa positiva e real (media dos
    ultimos 12 = +0,11 contra faixa 0,10), nao artefato do centro errado.

    Descritivo sobre os 60 desvios que existem, nao inferencia -- ver a secao "A faixa" na
    docstring do modulo, inclusive por que este numero substituiu 1/N."""
    if len(values) < 2:
        return None
    return round((sum(v * v for v in values) / len(values)) ** 0.5, 4)


def _ma4(serie: dict) -> dict:
    """Media movel de 4 trimestres, aparada a direita: valor de t = media de t-3..t. So
    agrega janela de 4 trimestres CONSECUTIVOS (checado por _trimestre_anterior), para
    nunca mediar pontos separados por um buraco. Perde os 3 primeiros pontos. `rms` e o
    RQM da propria MA (em torno de zero, ver _desvio_rms), que e ~metade do trimestral --
    ver a secao "Media movel" na docstring do modulo, inclusive por que isso importa para
    a faixa."""
    dates, values = serie.get("dates", []), serie.get("values", [])
    out_d, out_v = [], []
    for i in range(3, len(dates)):
        janela = dates[i - 3:i + 1]
        if any(janela[j] != _trimestre_anterior(janela[j + 1]) for j in range(3)):
            continue                      # buraco na serie: nao inventa janela
        out_d.append(dates[i])
        out_v.append(round(sum(values[i - 3:i + 1]) / 4, 4))
    return {"dates": out_d, "values": out_v, "rms": _desvio_rms(out_v)}


def _desvio(observada: dict, esperada: dict) -> dict:
    """desvio(t) = observada(t) - esperada(t-1): o realizado do trimestre contra o que os
    proprios bancos declararam um trimestre antes SOBRE esse trimestre. Ver a secao
    "Surpresa" da docstring do modulo -- em particular por que a defasagem de um
    trimestre e obrigatoria e por que o primeiro ponto da amostra nao tem desvio."""
    esp = dict(zip(esperada.get("dates", []), esperada.get("values", [])))
    dates, values = [], []
    for dt, obs in zip(observada.get("dates", []), observada.get("values", [])):
        prev = esp.get(_trimestre_anterior(dt))
        if obs is None or prev is None:
            continue
        dates.append(dt)
        # entradas tem 2 casas (conferido na base); 2 casas mantem a diferenca exata
        values.append(round(obs - prev, 2))
    # `rms` viaja junto com a serie porque e propriedade dela: e a faixa "em linha" do
    # relatorio, e o browser so le, nunca calcula (mesma convencao de transforms.py).
    return {"dates": dates, "values": values, "rms": _desvio_rms(values)}


def series_keys() -> list:
    """Os 16 nomes de serie de cred_ptc que a arvore consome (`<seg>_<direcao>_<horizonte>`)."""
    return [
        f"{seg}_{direcao}_{horizonte}"
        for seg, _, _ in _SEGMENTOS
        for direcao, _ in _DIRECOES
        for horizonte in HORIZONTES
    ]


def build(raw: dict) -> dict:
    """`raw`: {name: {"dates", "values"}} vindo direto de cred_ptc, com os 16 nomes de
    series_keys(). Sem transformacao nenhuma -- media de niveis rotulados nao se
    deflaciona, nao se dessazonaliza (a pergunta ja e "comparado ao trimestre anterior")
    e nao se expressa como % do PIB. Reagrupa apenas por horizonte, para a pill do
    relatorio, e acrescenta as duas series derivadas da aba: `desvio` = observada(t) -
    esperada(t-1), a surpresa da rodada (subtracao entre dois pontos ja publicados, nao
    modelo -- ver "Surpresa" na docstring do modulo), e `desvio_ma4`, a media movel de 4
    trimestres dela (ver "Media movel").
    """
    series = {}
    for seg, _, _ in _SEGMENTOS:
        for direcao, _ in _DIRECOES:
            key = f"{seg}_{direcao}"
            variants = {}
            for horizonte in HORIZONTES:
                s = raw.get(f"{key}_{horizonte}")
                variants[horizonte] = s if s else {"dates": [], "values": []}
            # 3a e 4a variantes, derivadas das duas acima: a surpresa da rodada e a
            # media movel de 4 trimestres dela, que e a leitura principal da aba.
            variants["desvio"] = _desvio(variants["observada"], variants["esperada"])
            variants["desvio_ma4"] = _ma4(variants["desvio"])
            series[key] = variants

    anchor = series.get(ANCHOR, {}).get("observada", {"dates": []})
    ref_date = anchor["dates"][-1] if anchor["dates"] else None

    return {
        "tree": PTC_TREE,
        "anchor": ANCHOR,
        "escala": ESCALA,
        "series": series,
        "ref_date": ref_date,
    }
