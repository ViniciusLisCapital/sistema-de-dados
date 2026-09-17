"""Painel trimestral de insumos do modelo estrutural.

Esta primeira versao cobre so as variaveis da equacao (I), a curva de Phillips:

    I(t) = i1*I(t-1) + (1-i1)*E(t-1) + i2*H(t) + i3*F(t-1) + i4*I*(t) + d08 + d20 + e

    ipca_12m     I    IPCA cheio acumulado em 12 meses, % -- SGS 13522
    pi_e         E    Focus IPCA 12 meses a frente, suavizada, %
    hiato        H    hiato do produto do BCB, % do produto potencial (nivel)
    de           F    variacao do cambio no trimestre, 100*dlog(PTAX), %
    pi_star_usd  I*   variacao do IC-Br em USD no trimestre, 100*dlog, %

As demais colunas (juro real, neutra, meta, Selic, dI) entram quando as equacoes
(E), (H), (R) e (F) forem escritas. Ver o CLAUDE.md desta pasta.

## O que NAO e reescrito aqui

`q`, `serie`, `para_q` e `focus_ipca_12m` sao importados de
`analytics.brasil.monetary_policy.modelo_painel`, nao copiados. Sao funcoes ja
validadas contra numero publicado pelo BC, e duas copias divergem no primeiro
ajuste que so uma delas receber.

## Tres convencoes de trimestralizacao, e cada uma e uma decisao

1. **IPCA 12m pelo ULTIMO mes do trimestre.** E um acumulado de 12 meses, entao a
   media dos tres meses do trimestre seria a media de tres janelas sobrepostas --
   um numero que nao corresponde a acumulado nenhum.

2. **Focus pela MEDIA dos boletins do trimestre**, que e o que `focus_ipca_12m()`
   ja faz e o que o modelo agregado do BC consome. Le-se "a expectativa que
   vigorou durante o trimestre", nao "a do ultimo boletim".

3. **Cambio e IC-Br pela MEDIA do trimestre, depois diferenciados.** E a convencao
   do BC e e a certa para repasse a precos: o que o importador enfrentou foi a
   taxa media do trimestre, nao o fechamento do ultimo dia util. As colunas
   `de_fim` e `pi_star_usd_fim` trazem a variante ponta-a-ponta ao lado, porque a
   equacao (F) -- um retorno financeiro -- vai querer a outra convencao, e a
   divergencia entre as duas tem de ser visivel em vez de silenciosa.

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
    focus_ipca_12m,
    para_q,
    q,
    serie,
)

warnings.filterwarnings("ignore")

_HERE = Path(__file__).parent
DATA = _HERE / "data"
INICIO = pd.Period("2001Q4", "Q")   # folga antes do inicio do hiato do BC (2003Q4)

# rotulo legivel ao lado do tecnico, para a pagina nao imprimir nome de coluna
COLS = {
    "ipca_12m":    ("IPCA acumulado em 12 meses", "%"),
    "pi_e":        ("Expectativa de IPCA para 12 meses a frente", "%"),
    "hiato":       ("Hiato do produto", "% do produto potencial"),
    "de":          ("Variacao do cambio no trimestre", "%"),
    "pi_star_usd": ("Variacao do IC-Br em dolar no trimestre", "%"),
}


def _ipca_12m() -> pd.Series:
    """IPCA acumulado em 12 meses (SGS 13522), no ultimo mes de cada trimestre."""
    return para_q(serie("macro_brasil", "inflc_agregados", "ipca_12m"), como="last")


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


def construir() -> pd.DataFrame:
    """Monta o painel trimestral. Uma coluna por variavel da equacao (I)."""
    ipca = serie("macro_brasil", "inflc_agregados", "ipca_12m")
    ptax = serie("macro_brasil", "cmb_ptax", "ptax_venda")
    icbr = serie("macro_brasil", "comm_icbr_usd", "icbr_usd")
    hiato = _hiato()

    df = pd.DataFrame({
        "ipca_12m":        para_q(ipca, como="last"),
        "pi_e":            focus_ipca_12m(),
        "hiato":           hiato,
        "de":              _var_log(para_q(ptax)),
        "pi_star_usd":     _var_log(para_q(icbr)),
        "de_fim":          _var_log(para_q(ptax, como="last")),
        "pi_star_usd_fim": _var_log(para_q(icbr, como="last")),
    })
    df = df[df.index >= INICIO].sort_index()
    # a ponta so existe onde ALGUMA coluna tem dado -- um trimestre inteiramente
    # vazio no fim e so o calendario andando, nao observacao
    df = df.loc[: df.dropna(how="all").index.max()]

    # `completo` e o que impede o trimestre da ponta de ser lido como fechado.
    # Um trimestre rotulado "2026T3" carregando o IPCA de agosto e a media de
    # 2,5 meses de PTAX nao e um fechamento de trimestre, e nada no numero avisa:
    # a estimacao filtra por esta coluna e a pagina marca a barra.
    fim_cheio = min(_ultimo_cheio_mensal(ipca), _ultimo_cheio_mensal(icbr),
                    _ultimo_cheio_diario(ptax), hiato.dropna().index.max())
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
