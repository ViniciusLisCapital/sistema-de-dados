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
19 dos 960 pontos passam de 1 em modulo justamente porque o teto e 2). Como e uma media
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

`series[seriesKey]` = {"observada": {...}, "esperada": {...}} -- a pill Observada|
Esperada troca qual variante ja carregada e lida, sem mexer na arvore. Mesma forma de
payload que impulso_tab.py usa para Mensal|Anual. Decisao explicita do usuario
(2026-08): horizonte e um seletor, nao um terceiro nivel de arvore -- mantem a tabela
em 8 linhas de dado em vez de 16 e deixa a comparacao entre segmentos, que e a leitura
principal, na mesma tela.

Aferido ao vivo: a expectativa dos bancos acerta a DIRECAO com frequencia alta --
esperada(t-1) tem o mesmo sinal de observada(t) em 47 dos 52 trimestres comparaveis de
ge_oferta. Ou seja, as duas variantes contam quase a mesma historia deslocada de um
trimestre; o valor de alternar esta em ver antecipacao de virada, nao divergencia.
"""
from analytics.credit import tree_helpers as th

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
    relatorio.
    """
    series = {}
    for seg, _, _ in _SEGMENTOS:
        for direcao, _ in _DIRECOES:
            key = f"{seg}_{direcao}"
            variants = {}
            for horizonte in HORIZONTES:
                s = raw.get(f"{key}_{horizonte}")
                variants[horizonte] = s if s else {"dates": [], "values": []}
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
