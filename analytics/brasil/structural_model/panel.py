"""Painel trimestral de insumos do modelo estrutural.

A curva de Phillips e estimada DESAGREGADA nos quatro cortes do BC, em inflacao
do TRIMESTRE -- nao acumulada em doze meses e nao anualizada:

    (IS) IS(t) = is1*IS(t-1) + (1-is1)*E(t-1)/4 + is2*H(t)                    + saz
    (IA) IA(t) = ia1*IA(t-1) + (1-ia1)*E(t-1)/4 + ia2*IAGR(t) + ia3*F(t)
                                                + ia4*H(t)                    + saz
    (II) II(t) = ii1*II(t-1) + ii1b*MM4(II) + (1-ii1-ii1b)*E(t-1)/4
                             + ii2*IMET(t) + ii3*IMET(t-1) + ii4*F(t-1) + ii5*H(t) + saz
    (IM) IM(t) = im1*IM(t-1) + im2*I(t-1) + (1-im1-im2)*E(t-1)/4              + saz

    (IS) tambem carrega a media movel de 4 trimestres de si mesma -- ver o CLAUDE.md.

    pi_q         I     inflacao do trimestre, IPCA cheio, %
    pi_is_q      IS    idem, servicos            pi_ia_q  IA   alimentacao
    pi_ii_q      II    bens industriais          pi_im_q  IM   monitorados
    wq_*               peso de cada corte no trimestre (media dos tres meses)
    pi_e         E     Focus IPCA 12 meses a frente, suavizada, % ao ano
    hiato        H     hiato do produto do BCB, % do produto potencial (nivel)
    de           F     variacao do cambio no trimestre, 100*dlog, %
    pi_agr_usd   IAGR  IC-Br agropecuaria em USD (SGS 29041), variacao do trimestre
    pi_met_usd   IMET  IC-Br metal em USD (SGS 29040), variacao do trimestre
    pi_star_usd        IC-Br geral em USD (SGS 29042) -- contexto da aba de dados
    meta_12m     Meta  meta do CMN no horizonte de 12 meses, % ao ano -- eq. (E)
    ipca_12m     I12   IPCA acumulado em 12 meses publicado (SGS 13522), % ao ano

    (H) H(t) = h1*H(t-1) + h2*g_rr(t-1) + d08 + d20 + eps

    rr_2a        taxa real de mercado de 2 anos (NTN-B 24M), % ao ano
    rr_10a       taxa real de mercado de 10 anos (NTN-B 120M), % ao ano
    g_rr         inclinacao real 2a-10a = rr_2a - rr_10a, p.p. -- o aperto monetario
    g_rr_fim     a mesma inclinacao pelo FECHAMENTO do trimestre, coluna paralela

    (E) E(t) = e1*E(t-1) + e2*I12(t) + (1-e1-e2)*Meta(t) + eps

    (R) R(t) = r1*R(t-1) + (1-r1)*(RR*(t) + Meta(t)) + r2*dI(t) + d08 + d20 + eps

    selic        R     Selic, media do trimestre, % ao ano (curva POLICY, fonte BIS)
    selic_fim          a mesma Selic pelo FECHAMENTO do trimestre, coluna paralela
    pi_e_2a            Focus IPCA a 2 anos, % ao ano -- reconstruida da curva anual
    meta_24m           meta do CMN no horizonte de 24 meses, % ao ano
    pi_bcb             projecao de IPCA do proprio Copom no horizonte relevante, % ao ano

    RR* NAO e coluna do painel: e a media movel de `rr_10a`, e a JANELA e escolha de
    estimacao. Ela vive em `equations/taylor.py`, onde a tabela de janelas e comparada.

## Por que o aperto monetario e uma INCLINACAO, e nao um juro contra um neutro

A forma usual poria `r(t) - RR*(t)`, com `RR*` uma taxa real de equilibrio. Medido, isso
nao sobrevive: com `RR*` constante (4,5%) ou com a neutra que o BC declara no RPM (5,0%),
o coeficiente da IS sai em -0,016 e -0,017, com t de -0,6, porque o juro real ex-ante cai
de 12,2% em 2001T4 a -0,9% em 2020T4 e volta a 8,5% -- uma tendencia que o hiato nao tem.
O que decide a estimativa e o que REMOVE essa tendencia, nao o nivel escolhido.

A inclinacao resolve isso sem precisar de `RR*` nenhum: e a diferenca entre dois precos
observados no mesmo pregao, mean-reverting por construcao, sem filtro, sem pesquisa e sem
look-ahead. A ponta de 2 anos carrega o ciclo de politica e a de 10 anos carrega a taxa
estrutural mais o premio; a diferenca e o aperto.

**O que a inclinacao NAO e: o premio de maturidade.** 10a - 2a da +0,37 p.p. (desvio 1,04),
contra +0,89/+1,11 (desvio 0,61/0,65) medidos contra a Focus de 3 e 4 anos -- porque a ponta
de 2 anos tem o premio dela e e ciclica. Para LER o premio, o gabarito e a Focus; para medir
aperto, e a inclinacao. Sao dois trabalhos e dois numeros.

    A equacao (E) vive em taxa ANUAL, e nao na unidade do trimestre: o que ela explica
    e a expectativa de doze meses, e o alvo dela e a meta, que tambem e anual. E por
    isso que `pi_e` entra inteiro aqui e dividido por 4 na curva de Phillips.

## Por que trimestral, e nao acumulada em 12 meses

Um acumulado de doze meses lido a cada tres tem janelas sobrepostas: duas leituras
seguidas compartilham nove meses de dado. O residuo e MA(3) por construcao e a inercia
sai mecanicamente alta -- medido, `i1` caiu de 0,73 para 0,32 ao trocar a metrica, e o
Ljung-Box do residuo deixou de rejeitar (p 0,0008 -> 0,12). Ver o CLAUDE.md da pasta.

## E por que a unidade NATIVA do trimestre, sem anualizar

Anualizar e `(1+pi)^4`, que **nao comuta com a media ponderada**: somar os quatro grupos
e depois anualizar nao da o mesmo que anualizar cada um e somar. Medido, a identidade do
IPCA fecha com RMSE de 0,0253 p.p. na unidade nativa e 0,2326 anualizada -- nove vezes
pior. Como a tese da pagina e que a soma ponderada dos quatro reproduz o cheio, a unidade
nativa e a unica que nao estraga o que se quer mostrar.

A expectativa e anual e entra dividida por 4, que e como o BC poe a expectativa de doze
meses na unidade do trimestre na eq. (1) do modelo agregado dele. Hiato, cambio e IC-Br
ja sao trimestrais e nao mudam.

## O que NAO e reescrito aqui

`q`, `serie`, `para_q` e `focus_ipca_12m` sao importados de
`analytics.brasil.monetary_policy.modelo_painel`, nao copiados. Sao funcoes ja
validadas contra numero publicado pelo BC, e duas copias divergem no primeiro
ajuste que so uma delas receber.

## Tres convencoes de trimestralizacao, e cada uma e uma decisao

1. **Inflacao do trimestre ENCADEADA**, nao somada: (1+m1)(1+m2)(1+m3)-1. Somar os tres
   meses erra o cruzado da composicao, pouco em inflacao baixa e muito em 2002 ou 2021.

2. **Focus pela MEDIA dos boletins do trimestre**, que e o que `focus_ipca_12m()`
   ja faz e o que o modelo agregado do BC consome. Le-se "a expectativa que
   vigorou durante o trimestre", nao "a do ultimo boletim".

3. **Cambio e IC-Br pela MEDIA do trimestre, depois diferenciados.** E a convencao
   do BC e e a certa para repasse a precos: o que o importador enfrentou foi a
   taxa media do trimestre, nao o fechamento do ultimo dia util. As colunas
   `de_fim` e `pi_star_usd_fim` trazem a variante ponta-a-ponta ao lado, porque a
   equacao (F) -- um retorno financeiro -- vai querer a outra convencao, e a
   divergencia entre as duas tem de ser visivel em vez de silenciosa.

O peso de cada corte e a **media dos tres meses** do trimestre, nao o do ultimo mes: a
inflacao do trimestre e produzida ao longo dele, com o peso que vigorou em cada mes.

O trimestre incompleto da ponta e descartado por `para_q(completos=True)`: sem
isso o trimestre corrente entra calculado com um ou dois meses.

Uso:
    uv run python analytics/brasil/structural_model/panel.py
"""
from __future__ import annotations

import warnings
from pathlib import Path

import numpy as np
import pandas as pd

from analytics.brasil.monetary_policy.modelo_painel import (
    focus_anual,
    focus_ipca_12m,
    para_q,
    q,
    serie,
)

warnings.filterwarnings("ignore")

_HERE = Path(__file__).parent
DATA = _HERE / "data"
INICIO = pd.Period("2001Q4", "Q")   # folga antes do inicio do hiato do BC (2003Q4)

# Os quatro cortes analiticos do BC. `grupo`/`subgrupo` de `inflc_dim` sao a
# classificacao POR SUBITEM que o BC mantem -- Monitorados de um lado, e os livres
# repartidos em Alimentos, Bens Industriais e Servicos. Nao e a arvore do IBGE
# (grupo/subgrupo/item), que e outra coisa e vive nas colunas `ibge_*`.
CORTES = {
    "is": ("servicos",     "Livres",      "Servi"),
    "ia": ("alimentacao",  "Livres",      "Aliment"),
    "ii": ("industriais",  "Livres",      "Bens"),
    "im": ("administrado", "Monitorados", None),
}

# rotulo legivel ao lado do tecnico, para a pagina nao imprimir nome de coluna
COLS = {
    "pi_q":        ("Inflacao do trimestre, IPCA cheio", "%"),
    "pi_is_q":     ("Inflacao do trimestre, servicos", "%"),
    "pi_ia_q":     ("Inflacao do trimestre, alimentacao", "%"),
    "pi_ii_q":     ("Inflacao do trimestre, bens industriais", "%"),
    "pi_im_q":     ("Inflacao do trimestre, monitorados", "%"),
    "pi_e":        ("Expectativa de IPCA para 12 meses a frente", "% ao ano"),
    "hiato":       ("Hiato do produto", "% do produto potencial"),
    "de":          ("Variacao do cambio no trimestre", "%"),
    "pi_agr_usd":  ("Variacao do IC-Br agropecuaria em dolar", "%"),
    "pi_met_usd":  ("Variacao do IC-Br metal em dolar", "%"),
    "pi_star_usd": ("Variacao do IC-Br geral em dolar", "%"),
    "meta_12m":    ("Meta de inflacao no horizonte de 12 meses", "% ao ano"),
    "ipca_12m":    ("IPCA acumulado em 12 meses, publicado", "% ao ano"),
    "rr_2a":       ("Taxa real de mercado de 2 anos", "% ao ano"),
    "rr_10a":      ("Taxa real de mercado de 10 anos", "% ao ano"),
    "g_rr":        ("Inclinacao real 2 anos menos 10 anos", "p.p."),
    "selic":       ("Selic, media do trimestre", "% ao ano"),
    "pi_e_2a":     ("Expectativa de IPCA para 2 anos a frente", "% ao ano"),
    "meta_24m":    ("Meta de inflacao no horizonte de 24 meses", "% ao ano"),
    "pi_bcb":      ("Projecao de IPCA do Copom no horizonte relevante", "% ao ano"),
}

# Peso da meta do ANO SEGUINTE na mistura de 12 meses, por trimestre.
#
# A Focus "IPCA 12 meses a frente suavizada" e uma interpolacao entre a expectativa
# do ano corrente e a do seguinte: uma pesquisa no mes m enxerga (12-m) meses do ano
# Y e m meses de Y+1, entao o peso de Y+1 e m/12. Um trimestre e a media dos seus
# tres meses, que da 2/12, 5/12, 8/12 e 11/12.
#
# Casar a meta com a MESMA convencao nao e preciosismo: `pi_e - meta` e o desvio que
# a equacao (E) explica, e usar a meta do ano-calendario contra uma expectativa de
# doze meses a frente injeta um degrau de janeiro em toda transicao de meta. Em
# 2003T4, com a meta indo de 8,5% para 5,5%, o degrau vale 2,75 p.p. -- maior que
# quase tudo o que a equacao tem para explicar.
META_W_Q = {1: 2.0 / 12, 2: 5.0 / 12, 3: 8.0 / 12, 4: 11.0 / 12}

# corte -> coluna de inflacao trimestral e coluna de peso
SUB_COL = {k: "pi_%s_q" % k for k in CORTES}
PESO_COL = {k: "wq_%s" % k for k in CORTES}


def _mensal(nome: str) -> pd.Series:
    """Variacao % mensal de um agregado do IPCA, com indice de data."""
    s = serie("macro_brasil", "inflc_agregados", nome).dropna()
    s.index = pd.to_datetime(s.index)
    return s


def _infl_q(s: pd.Series) -> pd.Series:
    """% mensal -> inflacao do TRIMESTRE em %, encadeando os tres meses.

    Encadeia, nao soma: (1+m1)(1+m2)(1+m3)-1. So trimestres com os tres meses.
    """
    per = pd.PeriodIndex(s.index, freq="Q")
    n = s.groupby(per).size()
    fat = (1.0 + s / 100.0).groupby(per).prod()
    return (fat[n >= 3] - 1.0) * 100.0


def ipca_12m_publicado() -> pd.Series:
    """IPCA acumulado em 12 meses publicado (SGS 13522), no ultimo mes do trimestre.

    Dois papeis, e nenhum e o de regressor da curva de Phillips: e o GABARITO da
    leitura de 12 meses da pagina, e e o termo de inflacao da equacao (E), onde a
    especificacao pede a serie publicada (SGS 13522).

    Encadear quatro trimestres da nossa `pi_q` tem de reproduzi-lo, e reproduz -- erro
    medio 0,0025 p.p., maximo 0,0052. Somar os quatro em vez de encadear erra 0,149
    (max 0,861), sessenta vezes mais, e e por isso que o gabarito existe.
    """
    s = serie("macro_brasil", "inflc_agregados", "ipca_12m").dropna()
    s.index = pd.to_datetime(s.index)
    per = pd.PeriodIndex(s.index, freq="Q")
    n = s.groupby(per).size()
    ult = s.groupby(per).last()
    # os TRES meses, e nao a regra de meia-mediana do `para_q`: com dois meses o
    # trimestre da ponta entra carregando a leitura de agosto com rotulo de T3, que
    # e o mesmo defeito que a coluna `completo` existe para impedir do outro lado.
    return ult[n >= 3]


def _meta_anual() -> pd.Series:
    """Meta de inflacao por ANO, do CMN (SGS 13521), indexada pelo ano."""
    a = serie("macro_brasil", "inflc_meta", "meta_inflacao").dropna().astype(float)
    a.index = pd.to_datetime(a.index)
    return pd.Series(a.values, index=a.index.year).sort_index()


def metas(idx: pd.PeriodIndex) -> tuple[pd.Series, int]:
    """(meta no horizonte de 12 meses, ultimo ano que o CMN publicou).

    O horizonte de 12 meses de um trimestre do ano Y alcanca Y+1, entao a ponta da
    serie precisa de uma meta que o CMN ainda pode nao ter anunciado. Desde 2025 o
    regime e de meta CONTINUA em 3,0%, o que torna a extensao pelo ultimo valor uma
    leitura do regime e nao um chute -- mas ela e uma premissa, e por isso o ultimo
    ano efetivamente publicado volta junto para a pagina poder dize-lo.
    """
    a = _meta_anual()
    ult = int(a.index.max())

    def _m(ano: int) -> float:
        return float(a.loc[min(ano, ult)])

    m12 = pd.Series([(1.0 - META_W_Q[p.quarter]) * _m(p.year)
                     + META_W_Q[p.quarter] * _m(p.year + 1) for p in idx], index=idx)
    return m12, ult


def _hiato() -> pd.Series:
    """Hiato do produto publicado pelo BCB -- ja trimestral, nao agregar.

    `pm_hiato_produto` guarda a edicao CORRENTE do anexo do RPM: o BCB reescreve o
    passado a cada edicao, e esta tabela e sempre a ultima leitura. A serie em
    tempo real (o que ele publicou na epoca) e `pm_hiato_produto_vintages`, e entra
    como coluna de robustez quando a equacao (H) for estimada.
    """
    d = q("macro_brasil", "SELECT date, value FROM pm_hiato_produto "
                          "WHERE variavel='central' ORDER BY date")
    d["date"] = pd.to_datetime(d["date"])
    s = d.set_index("date")["value"].astype(float).sort_index()
    return s.groupby(pd.PeriodIndex(s.index, freq="Q")).last()


# Vertices da curva real da B3 que a inclinacao usa. 24M e 120M sao os dois que a
# grade `VERTICES` de `connectors/b3_curvas.py` sustenta em todos os 5.121 pregoes.
NTNB_VERT = {"rr_2a": "24M", "rr_10a": "120M"}


_NTNB: pd.DataFrame | None = None


def _ntnb_bruta() -> pd.DataFrame:
    """A curva real diaria, um pregao por linha. Consultada uma vez por processo."""
    global _NTNB
    if _NTNB is None:
        d = q("macro_brasil",
              "SELECT date, tenor, value FROM br_interest_rate "
              "WHERE curve='NTNBJS' AND tenor IN ('24M','120M') ORDER BY date")
        d["date"] = pd.to_datetime(d["date"])
        piv = d.pivot_table(index="date", columns="tenor", values="value", aggfunc="last")
        faltando = [v for v in NTNB_VERT.values() if v not in piv.columns]
        if faltando:
            raise ValueError("br_interest_rate sem os vertices %s da curva NTNBJS" % faltando)
        _NTNB = piv
    return _NTNB


def ntnb_real(como: str = "media") -> pd.DataFrame:
    """Taxa real de mercado de 2 e 10 anos (NTN-B), trimestral.

    Fonte: `br_interest_rate`, curva NTNBJS, que vem do arquivo de pregao da B3 -- a
    mesma tabela dos tres relatorios de juros. Os dois vertices tem 5.121 pregoes cada,
    2006-01-02 -> hoje, sem buraco.

    ## A convencao e a MEDIA do trimestre, e a de fechamento anda ao lado

    Mesmo argumento do cambio nesta pasta: o que age sobre a demanda e a taxa que vigorou
    ao longo do trimestre, nao a do ultimo pregao. As duas concordam na media (diferenca
    de -0,011 p.p. na inclinacao) e divergem ate 0,99 p.p. num trimestre isolado, o que e
    grande contra um desvio de 1,04 -- por isso `g_rr_fim` existe, para a divergencia ser
    visivel em vez de silenciosa.

    A escolha NAO foi feita pelo ajuste: na equacao (H) a media da h2 = -0,164 (t -2,62) e
    o fechamento -0,177 (t -2,65). A regressao nao distingue as duas, entao quem decide e
    a convencao, e ela fica declarada aqui.
    """
    piv = _ntnb_bruta()
    return pd.DataFrame({col: para_q(piv[v].dropna(), como=como)
                         for col, v in NTNB_VERT.items()})


# ── os insumos da regra de juros, equacao (R) ────────────────────────────────
def selic_bc(como: str = "media") -> pd.Series:
    """A Selic trimestral, da curva POLICY de `br_interest_rate`.

    A curva POLICY e onde este repositorio centralizou "a taxa que o banco central
    define", nas tres bases de juros; a fonte dela e o BIS e nao a SGS 432, decisao
    medida e registrada em `domain/db/brasil/b3/br_interest_rate.py` (as duas
    concordam em 10.027 dos 10.029 dias comuns).

    A convencao e a MEDIA do trimestre, como o plano pede, e pelo mesmo motivo das
    outras colunas de nivel: o que age sobre a economia e a taxa que vigorou ao longo
    do trimestre. `selic_fim` anda ao lado para a divergencia ser visivel -- ela e
    -0,026 p.p. na media e chega a 3,59 p.p. num trimestre isolado (2002T4, o Copom
    subindo 3 p.p. em dezembro), contra um desvio de 4,82 p.p. na propria Selic.

    A ressalva do trecho 1994-1999, em que o instrumento eram a TBC e a TBAN e nao a
    meta Selic, nao alcanca este painel: ele comeca em 2001T4.
    """
    d = q("macro_brasil", "SELECT date, value FROM br_interest_rate "
                          "WHERE curve='POLICY' AND tenor='1d' ORDER BY date")
    d["date"] = pd.to_datetime(d["date"])
    return para_q(d.set_index("date")["value"].astype(float), como=como)


# Horizonte, em anos, em que a curva anual do Focus reproduz a "IPCA 24 meses a
# frente". Nao e 2,0: a janela de 24 meses acumula os meses 12 a 24, entao o CENTRO
# dela esta a 18 meses -- e os pontos anuais do Focus, sendo inflacao acumulada no
# ano, ja estao datados no meio do ano (`h = ref + 0,5 - ano`, em `focus_anual`).
H_FOCUS_2A = 1.5


def focus_ipca_2a() -> pd.Series:
    """Expectativa Focus de IPCA a 2 anos, trimestral, desde 2001T4.

    ## Por que reconstruida, e nao lida direto

    A serie rolante publicada existe (`expc_focus`, horizonte '24m'), mas so desde
    **2021-03-31** -- cinco anos, contra os vinte e cinco que a regra de juros precisa.
    A pesquisa ANUAL do Focus, essa sim, vai a 2000 e projeta ate 2030, e interpolar a
    curva dela no horizonte certo devolve a mesma coisa: contra os 1.370 boletins em
    que as duas coexistem, o erro medio e **0,071 p.p.**, o maximo 0,681, a correlacao
    0,931 e o vies -0,027. Interpolar em h=1,0 erra 0,365 e em h=2,0 erra 0,246, entao
    o horizonte nao foi ajustado ao dado: ele sai da definicao da janela e o dado
    confirma.

    E a mesma maquinaria que `focus_selic_12m_diario()` usa para a Selic -- importada,
    nao copiada, porque duas leituras da mesma curva divergiriam.
    """
    fa = focus_anual()
    fa = fa[fa["indicador"] == "IPCA"]
    out = {}
    for data, g in fa.groupby("date"):
        g = g[g["h"] > 0].sort_values("h")
        if len(g) >= 2 and g["h"].max() >= H_FOCUS_2A:
            out[data] = float(np.interp(H_FOCUS_2A, g["h"].values, g["mediana"].values))
    return para_q(pd.Series(out).sort_index())


def metas_24m(idx: pd.PeriodIndex) -> pd.Series:
    """A meta no horizonte de 24 meses -- a de `metas()`, um ano adiante.

    A janela de 24 meses de um trimestre do ano Y cobre (12-m) meses de Y+1 e m de
    Y+2, os MESMOS pesos de `META_W_Q` deslocados um ano. Ela existe para casar com
    `pi_e_2a`: comparar uma expectativa de dois anos contra a meta de doze meses
    injetaria o mesmo degrau de janeiro que `META_W_Q` foi escrito para evitar.
    """
    a = _meta_anual()
    ult = int(a.index.max())

    def _m(ano: int) -> float:
        return float(a.loc[min(ano, ult)])

    return pd.Series([(1.0 - META_W_Q[p.quarter]) * _m(p.year + 1)
                      + META_W_Q[p.quarter] * _m(p.year + 2) for p in idx], index=idx)


def copom_relevante() -> pd.Series:
    """Projecao de IPCA do proprio Copom no horizonte relevante, por trimestre.

    E a alternativa de `dI` que o plano pede ao lado da Focus: em vez do desvio que o
    MERCADO projeta, o desvio que o proprio comite projetava quando decidiu. Cenario de
    `juros_esperado` -- o que condiciona na trajetoria de juros da Focus, e nao em juros
    constantes -- porque e esse o cenario que o Copom trata como referencia desde 2017.

    O horizonte relevante e **6 trimestres a frente** em toda a amostra util, o que o
    poe entre a Focus de 12 meses e a de 2 anos. A tabela `pm_copom_projecoes` marca
    qual linha e ela (`horizonte_relevante=1`), entao nao ha escolha de horizonte aqui.

    Cobertura: um vintage por trimestre, sem buraco, de 2008T1 ate hoje. Os cinco
    trimestres sem linha (os T3 de 2003 a 2007) sao anteriores a qualquer amostra que a
    regra de juros alcanca, porque o juro real de 10 anos so comeca em 2006.
    """
    d = q("macro_brasil", "SELECT vintage, value FROM pm_copom_projecoes "
                          "WHERE indice='ipca' AND horizonte_relevante=1 "
                          "AND cenario='juros_esperado' ORDER BY vintage")
    d["vintage"] = pd.to_datetime(d["vintage"])
    s = d.set_index("vintage")["value"].astype(float)
    return s.groupby(pd.PeriodIndex(s.index, freq="Q")).last()


def _var_log(s: pd.Series) -> pd.Series:
    """100 * diferenca do log -- a variacao do trimestre em pontos percentuais."""
    return np.log(s).diff() * 100.0


def _ultimo_cheio_mensal(s: pd.Series) -> pd.Period:
    """Ultimo trimestre com os TRES meses presentes."""
    n = s.groupby(pd.PeriodIndex(s.index, freq="Q")).size()
    return n[n >= 3].index.max()


def _ultimo_cheio_diario(s: pd.Series) -> pd.Period:
    """Ultimo trimestre cujo ultimo dia de calendario ja passou na serie."""
    ult = pd.PeriodIndex(s.index, freq="Q").max()
    return ult if s.index.max() >= ult.end_time.normalize() else ult - 1


def _pesos_mensais() -> pd.DataFrame:
    """Peso de cada corte no IPCA, por mes, direto do que o IBGE publica.

    Os pesos NAO sao os da POF nem uma media da amostra: o IBGE atualiza o peso de
    cada subitem todo mes pela inflacao relativa dele, e reancora quando a POF
    muda. `inflc_decomposicao` guarda esse peso efetivo, subitem a subitem, desde
    1999-08 -- entao aqui basta somar por corte, sem encadear nada a mao.

    Medido: a soma ponderada dos quatro subindices PUBLICADOS com estes pesos
    reproduz o IPCA cheio mensal com erro medio de 0,0077 p.p. (max 0,107) em 325
    meses. Com peso fixo na media da amostra o erro dobra (0,0189 / 0,153).
    """
    d = q("macro_brasil",
          "SELECT c.date, m.grupo, m.subgrupo, c.pesos "
          "FROM inflc_decomposicao c JOIN inflc_dim m USING (subitem_codigo) "
          "WHERE c.indice='IPCA'")
    d["date"] = pd.to_datetime(d["date"])
    gr = d["grupo"].fillna("")
    sg = d["subgrupo"].fillna("")

    corte = pd.Series("??", index=d.index)
    for k, (_, grupo, pref) in CORTES.items():
        if pref is None:
            m = gr.str.startswith(grupo)
        else:
            m = gr.str.startswith(grupo) & sg.str.startswith(pref)
        corte = corte.mask(m, k)
    faltando = int((corte == "??").sum())
    if faltando:
        raise ValueError("%d linhas de inflc_dim sem corte do BC" % faltando)

    d["corte"] = corte
    w = d.groupby(["date", "corte"])["pesos"].sum().unstack()[list(CORTES)]
    # renormaliza: a fonte fecha em 1,0000 mas o arredondamento por subitem
    # deixa ate 1,0010 em alguns meses
    return w.div(w.sum(axis=1), axis=0)


def _subindices() -> tuple[pd.DataFrame, pd.DataFrame, pd.Period]:
    """(inflacao trimestral por corte, peso por corte, ultimo trimestre cheio comum).

    O peso e a MEDIA dos tres meses do trimestre. Medido contra o IPCA cheio do
    trimestre, reconstruindo-o a partir dos quatro: erro medio 0,0167 p.p. e maximo
    0,138 em 91 trimestres, R2 0,9990. E o piso do erro de reconstrucao -- 2,7% do
    RMSE da soma dos ajustados (0,613), entao nao domina, mas fica declarado.
    """
    mensal = {k: _mensal("ipca_" + nome) for k, (nome, _, _) in CORTES.items()}
    A = pd.DataFrame({k: _infl_q(s) for k, s in mensal.items()})

    w = _pesos_mensais()
    W = pd.DataFrame({k: para_q(w[k], como="mean") for k in CORTES})
    W = W.div(W.sum(axis=1), axis=0)

    fim = min(min(_ultimo_cheio_mensal(s) for s in mensal.values()),
              _ultimo_cheio_mensal(w[list(CORTES)[0]]))
    return A, W, fim


def construir() -> pd.DataFrame:
    """Monta o painel trimestral. Uma coluna por variavel das quatro equacoes."""
    ipca = _mensal("ipca")
    ptax = serie("macro_brasil", "cmb_ptax", "ptax_venda")
    icbr = serie("macro_brasil", "comm_icbr_usd", "icbr_usd")
    agr = serie("macro_brasil", "comm_icbr_usd", "icbr_agropecuaria_usd")
    met = serie("macro_brasil", "comm_icbr_usd", "icbr_metal_usd")
    hiato = _hiato()
    rr = ntnb_real("media")
    rr_fim = ntnb_real("last")
    sel = selic_bc("media")
    A, W, fim_sub = _subindices()

    df = pd.DataFrame({
        "pi_q":            _infl_q(ipca),
        "pi_e":            focus_ipca_12m(),
        "hiato":           hiato,
        "de":              _var_log(para_q(ptax)),
        "pi_star_usd":     _var_log(para_q(icbr)),
        "pi_agr_usd":      _var_log(para_q(agr)),
        "pi_met_usd":      _var_log(para_q(met)),
        "de_fim":          _var_log(para_q(ptax, como="last")),
        "pi_star_usd_fim": _var_log(para_q(icbr, como="last")),
        "ipca_12m":        ipca_12m_publicado(),
        "rr_2a":           rr["rr_2a"],
        "rr_10a":          rr["rr_10a"],
        "g_rr":            rr["rr_2a"] - rr["rr_10a"],
        "g_rr_fim":        rr_fim["rr_2a"] - rr_fim["rr_10a"],
        "selic":           sel,
        "selic_fim":       selic_bc("last"),
        "pi_e_2a":         focus_ipca_2a(),
        "pi_bcb":          copom_relevante(),
        **{SUB_COL[k]: A[k] for k in CORTES},
        **{PESO_COL[k]: W[k] for k in CORTES},
    })
    df = df[df.index >= INICIO].sort_index()
    df["meta_12m"], _ = metas(df.index)
    df["meta_24m"] = metas_24m(df.index)
    # a ponta so existe onde ALGUMA coluna tem dado -- um trimestre inteiramente
    # vazio no fim e so o calendario andando, nao observacao
    df = df.loc[: df.dropna(how="all").index.max()]

    # `completo` e o que impede o trimestre da ponta de ser lido como fechado.
    # Um trimestre rotulado "2026T3" carregando o IPCA de agosto e a media de
    # 2,5 meses de PTAX nao e um fechamento de trimestre, e nada no numero avisa:
    # a estimacao filtra por esta coluna e a pagina marca a barra.
    # a curva da B3 entra pela regra diaria: com a media do trimestre, um trimestre
    # sem o ultimo pregao carrega uma media parcial, que e o mesmo defeito do PTAX
    ntnb_bruta = _ntnb_bruta()["120M"].dropna()
    sel_bruta = q("macro_brasil", "SELECT date, value FROM br_interest_rate "
                                  "WHERE curve='POLICY' AND tenor='1d' ORDER BY date")
    sel_bruta = sel_bruta.set_index(pd.to_datetime(sel_bruta["date"]))["value"]
    fim_cheio = min(_ultimo_cheio_mensal(ipca), _ultimo_cheio_mensal(icbr),
                    _ultimo_cheio_mensal(agr), _ultimo_cheio_mensal(met),
                    _ultimo_cheio_diario(ptax), _ultimo_cheio_diario(ntnb_bruta),
                    _ultimo_cheio_diario(sel_bruta),
                    hiato.dropna().index.max(), fim_sub)
    df["completo"] = df.index <= fim_cheio
    return df


def salvar(verbose: bool = True) -> pd.DataFrame:
    df = construir()
    DATA.mkdir(parents=True, exist_ok=True)
    df.to_csv(DATA / "panel.csv")
    if verbose:
        print("painel: %s -> %s, %d trimestres" % (df.index[0], df.index[-1], len(df)))
        print()
        print("coluna            primeiro    ultimo      n   ultimo valor")
        for c in df.columns:
            s = df[c].dropna()
            if not len(s):
                print("%-16s  (vazia)" % c)
                continue
            print("%-16s  %-10s  %-10s  %3d  %8.3f"
                  % (c, s.index[0], s.index[-1], len(s), s.iloc[-1]))
    return df


def carregar() -> pd.DataFrame:
    """Le o painel gravado, com o indice de volta como PeriodIndex trimestral."""
    df = pd.read_csv(DATA / "panel.csv", index_col=0)
    df.index = pd.PeriodIndex(df.index, freq="Q")
    return df


if __name__ == "__main__":
    salvar()
