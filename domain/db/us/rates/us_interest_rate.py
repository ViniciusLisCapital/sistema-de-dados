"""
ETL da estrutura a termo de juros dos EUA -> macro_us.us_interest_rate.

Fonte: FRED, via `connectors/fred.py`. Duas curvas, e a segunda existe por
decisao explicita do usuario (2026-09-03): *"na tabela de interest rate coloque
tambem a policy_rate descrita como tal. Assim centralizamos os dados de juros
na mesma tabela, independente se ele e o dado da curva, ou dado definido pelo
BC"*.

    US_TREASURY   11 vertices de 1M a 30Y, "constant maturity" do Treasury
    POLICY        a meta do Fed, um ponto, no vertice de 1 dia util

Historia: ate 2026-09-03 esta tabela vinha do projeto CentralManagement com
**2 vertices** (DGS2 e DGS10) e nenhum consumidor neste repositorio. A curva
inteira sempre esteve disponivel no mesmo endpoint, de graca.

## O que "policy rate" significa aqui, e por que nao e a Fed funds efetiva

O usuario pediu o dado *definido pelo BC*, o que exclui a `DFF` (Fed funds
**efetiva**, que e onde o mercado negociou, nao o que o Fed decidiu). A meta e
publicada em duas eras e a emenda e limpa, sem um dia de sobreposicao:

    DFEDTAR              1982-09-27 -> 2008-12-15   meta unica
    (DFEDTARL+DFEDTARU)/2  2008-12-16 -> hoje       ponto medio da BANDA

Desde dez/2008 o Fed anuncia um **intervalo** de 25 bps, nao um numero. O ponto
medio e a convencao usual para reduzi-lo a uma serie (e o que permite comparar
com a Selic meta de `macro_brasil`), mas e uma reducao nossa e nao um numero
publicado -- se algum dia a banda em si importar, ela sai dos dois codigos
acima sem retrabalho.

## Duas coisas que diferem das curvas brasileiras

**A POLICY tem calendario proprio, e mais denso que a curva.** Os `DGS*` sao de
dia util com falha em feriado; a meta vigora todo dia, inclusive fim de semana,
e e assim que o FRED a publica. Nao truncamos para o calendario da curva --
seria descartar informacao. Consequencia pratica para quem consulta: um
`SELECT ... WHERE date = <sabado>` devolve so a POLICY, e um JOIN de curva com
policy tem de ser por data com `LEFT JOIN` do lado da curva.

**Nao ha guarda de qualidade como o de `br_interest_rate`.** Lá o valor era
*construido* por nos (interpolacao sobre uma grade), e o defeito historico
nasceu exatamente disso. Aqui cada vertice e uma serie publicada, lida e
gravada sem transformacao -- nao ha o que a interpolacao possa inventar. O que
resta e checagem de sanidade de faixa, feita na carga.

Banco: macro_us.us_interest_rate -- PRIMARY KEY (date, curve, tenor)
"""

from __future__ import annotations

import logging

import pandas as pd

from connectors.fred import _fred
from connectors.mysql import insert_data_into_database

logger = logging.getLogger(__name__)

_DATABASE = "macro_us"
_TABLE = "us_interest_rate"

# Vertice -> serie do FRED. "Constant maturity" e a taxa que o Treasury
# interpola da propria curva de leilao, publicada ja no vertice redondo -- por
# isso aqui nao interpolamos nada, ao contrario do lado brasileiro.
#
# Os rotulos sao os do PROPRIO Treasury ("1 Mo", "2 Yr", "30 Yr"), em anos a
# partir de 1Y -- nao em meses como no `br_interest_rate`. E o que o COMMENT da
# coluna manda ("como a fonte nomeia o vertice") e o que a tabela ja usava nos
# 2 vertices herdados, o que faz a carga nova ATUALIZAR aquelas linhas em vez de
# deixa-las orfas sob outro rotulo. Quem cruza os dois paises cruza por
# `tenor_years`, que existe exatamente para isso -- o texto de `tenor` e da
# fonte e nao e chave de juncao entre schemas.
_TREASURY = {
    "1M":  ("DGS1MO", 1 / 12),
    "3M":  ("DGS3MO", 3 / 12),
    "6M":  ("DGS6MO", 6 / 12),
    "1Y":  ("DGS1", 1.0),
    "2Y":  ("DGS2", 2.0),
    "3Y":  ("DGS3", 3.0),
    "5Y":  ("DGS5", 5.0),
    "7Y":  ("DGS7", 7.0),
    "10Y": ("DGS10", 10.0),
    "20Y": ("DGS20", 20.0),
    "30Y": ("DGS30", 30.0),
}

# Meta do Fed: uma serie ate 2008-12-15, banda depois. Ver o docstring.
_FED_META_UNICA = "DFEDTAR"
_FED_BANDA = ("DFEDTARL", "DFEDTARU")

# 1 dia util em anos, a mesma convencao de 252 dias do resto do projeto. Zero
# seria errado: a coluna existe para interpolar e ordenar, e um vertice em zero
# quebra qualquer interpolacao que o use como ancora curta.
_TENOR_1D = round(1 / 252, 6)

# Faixa de sanidade. O Treasury de 30 anos chegou a ~15% em 1981 e os vertices
# curtos a zero em 2009-2015 e 2020-2021 -- entao o piso e 0 e nao negativo:
# nenhum vertice desta curva jamais fechou negativo (medido; ao contrario da
# NTN-B brasileira, que e taxa real).
_PISO, _TETO = 0.0, 25.0

_INICIO_ROTINA_DIAS = 30


def _serie(fred, code: str) -> pd.Series:
    s = fred.get_series(code).dropna()
    s.index = pd.to_datetime(s.index)
    return s.astype(float)


def _meta_do_fed(fred) -> pd.Series:
    """Meta do Fed numa serie continua: a meta unica ate 2008-12-15, o ponto
    medio da banda depois. A emenda e verificada, nao presumida -- se as duas
    eras passarem a se sobrepor, o `assert` avisa em vez de a media silenciosa
    de dois regimes entrar no banco."""
    unica = _serie(fred, _FED_META_UNICA)
    baixa = _serie(fred, _FED_BANDA[0])
    alta = _serie(fred, _FED_BANDA[1])
    banda = ((baixa + alta) / 2).dropna()
    sobreposicao = unica.index.intersection(banda.index)
    if len(sobreposicao):
        raise ValueError(
            f"{_FED_META_UNICA} e a banda se sobrepoem em {len(sobreposicao)} dias "
            f"(de {sobreposicao.min().date()} a {sobreposicao.max().date()}) -- "
            "a emenda deixou de ser limpa, reveja qual serie vale em cada era"
        )
    return pd.concat([unica, banda]).sort_index()


def coletar(full: bool = False, dias: int = _INICIO_ROTINA_DIAS) -> pd.DataFrame:
    """Monta o DataFrame pronto para a tabela. Separado de run() para o teste
    poder exercitar a coleta sem tocar no banco."""
    fred = _fred()
    corte = None if full else pd.Timestamp.today().normalize() - pd.Timedelta(days=dias)

    linhas = []
    for tenor, (code, anos) in _TREASURY.items():
        s = _serie(fred, code)
        if corte is not None:
            s = s[s.index >= corte]
        for data, valor in s.items():
            linhas.append((data.date(), "US_TREASURY", tenor, round(anos, 6),
                           round(float(valor), 8)))
        logger.info("  US_TREASURY %-5s %-7s %5d obs", tenor, code, len(s))

    meta = _meta_do_fed(fred)
    if corte is not None:
        meta = meta[meta.index >= corte]
    for data, valor in meta.items():
        linhas.append((data.date(), "POLICY", "1d", _TENOR_1D, round(float(valor), 8)))
    logger.info("  POLICY      1d    meta Fed %5d obs", len(meta))

    df = pd.DataFrame(linhas, columns=["date", "curve", "tenor", "tenor_years", "value"])

    fora = df[(df.value < _PISO) | (df.value > _TETO)]
    if len(fora):
        raise ValueError(
            f"{len(fora)} valores fora de [{_PISO}, {_TETO}]:\n"
            f"{fora.head(10).to_string(index=False)}"
        )
    if df.duplicated(["date", "curve", "tenor"]).any():
        raise ValueError("chave (date, curve, tenor) duplicada na coleta")
    return df


def run(full: bool = False, dias: int = _INICIO_ROTINA_DIAS) -> None:
    """Atualiza macro_us.us_interest_rate.

    Args:
        full: True carrega o historico inteiro de cada serie (o 1Y, o 3Y, o 5Y,
              o 10Y e o 20Y comecam em 1962-01-02; o 1M so em 2001-07). Sao
              ~160 mil linhas.
        dias: janela retroativa do passe de rotina, em dias corridos. 30 cobre
              qualquer feriado e absorve revisao da fonte; o upsert torna
              reescrever dia ja gravado inofensivo.
    """
    df = coletar(full=full, dias=dias)
    if df.empty:
        logger.warning("us_interest_rate: nada a inserir")
        return
    logger.info("us_interest_rate: %d linhas, %s -> %s",
                len(df), df["date"].min(), df["date"].max())
    for curva, g in df.groupby("curve"):
        logger.info("  %-11s %6d linhas, %2d vertices, %s -> %s",
                    curva, len(g), g["tenor"].nunique(),
                    g["date"].min(), g["date"].max())
    insert_data_into_database(_DATABASE, _TABLE, df)
