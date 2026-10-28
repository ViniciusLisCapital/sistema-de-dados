"""
Volatilidade implicita ATM do dolar (USD/BRL) -> macro_brasil.cmb_vol_implicita.

Fonte: premio de referencia das opcoes de dolar comercial da B3
(`connectors/b3_premio.py`, arquivo RE do pregao). A B3 nao publica a vol num
arquivo aberto; publica o premio que sai da superficie dela, e a vol e
recuperada aqui invertendo Black. Substitui -- quando o modelo for trocado de
fonte -- o CSV da Bloomberg (`USDBRLV3M`) que viaja em
`analytics/brasil/structural_model/data/`, a pendencia F4.

## A conta, por pregao e vencimento

1. **Forward e desconto pela paridade**, sem curva externa: C - P = D*F - D*K
   e uma reta em K, entao uma regressao nos strikes com call e put da D e F.
   Primeiro em todos os strikes, depois so nos a +-20% do F da primeira
   passada (strike muito fundo tem premio arredondado).
2. **Vol no forward**: inverte Black na opcao fora do dinheiro dos dois strikes
   que cercam F (put abaixo, call acima) e interpola linear no strike. Vencimento
   cujo F cai fora dos strikes publicados nao da vol -- nada e extrapolado.
3. **Prazo fixo**: interpolacao linear da VARIANCIA TOTAL (vol^2 x dias) entre
   os dois vencimentos que cercam o prazo, em dias corridos. Prazo fora do
   intervalo dos vencimentos nao sai -- por isso nao ha 1 semana (o vencimento
   mais curto raramente esta a menos de 7 dias).

A B3 vence opcao de dolar no 1o dia util do mes, entao o 3M e quase sempre
interpolado. **Isso dilui evento discreto**: medido em 29/07-04/08/2026, quando
os 3 meses passaram a cobrir as duas voltas da eleicao, o 3M daqui ficou ~1,7
p.p. abaixo do Bloomberg (13,3-13,7 contra 15,0-15,2), enquanto em datas sem
evento no prazo bate na casa decimal (2010-03-31: 14,28 x 14,30; 2015-03-31:
21,07 x 21,06; 2026-06-30: 12,08 x 12,19). A hipotese -- nao confirmada -- e a
interpolacao espalhar o salto de variancia do evento, ou a superficie teorica da
B3 precifica-lo menos que o mercado.

Ressalva da fonte, do manual de apreçamento: o premio e TEORICO, e sem insumo a
B3 pode repetir a vol da sessao anterior.

Banco: macro_brasil.cmb_vol_implicita -- PRIMARY KEY (date, prazo)
"""

from __future__ import annotations

import logging
import os

import mysql.connector
import numpy as np
import pandas as pd
from scipy.optimize import brentq
from scipy.stats import norm

from connectors import b3_premio
from connectors.mysql import insert_data_into_database

logger = logging.getLogger(__name__)

_DATABASE = "macro_brasil"
_TABLE = "cmb_vol_implicita"
_INICIO = "2006-01-02"
_DIAS_ROTINA = 10

# Prazo -> dias corridos. Os da Bloomberg (USDBRLV1M..V1Y), sem a semana.
PRAZOS = {"1M": 30, "2M": 61, "3M": 91, "6M": 182, "9M": 273, "1Y": 365}

# Guardas -- folga larga, o objetivo e pegar unidade/layout errado, nao julgar
# o mercado. Vol ATM do real: ~8% nos dias mais calmos, ~40% em out/2008.
_VOL_MIN, _VOL_MAX = 2.0, 120.0
_D_MIN = 0.2               # fator de desconto: 10 anos a 15% a.a. ainda da 0,25

_DDL = """
CREATE TABLE IF NOT EXISTS cmb_vol_implicita (
    date   DATE        NOT NULL COMMENT 'Pregao',
    prazo  VARCHAR(4)  NOT NULL COMMENT '1M | 2M | 3M | 6M | 9M | 1Y (30, 61, 91, 182, 273, 365 dias corridos)',
    value  DOUBLE      NOT NULL COMMENT 'Volatilidade implicita ATM-forward, % a.a.',
    PRIMARY KEY (date, prazo)
) COMMENT='Volatilidade implicita ATM-forward do USD/BRL por prazo fixo, % a.a. RECUPERADA do premio de referencia das opcoes de dolar comercial da B3 (arquivo RE do pregao), invertendo Black sobre o futuro: forward e desconto pela paridade put-call, vol no forward por interpolacao entre os strikes que o cercam, prazo fixo por interpolacao linear da variancia total entre os vencimentos que o cercam -- nada extrapolado. Vencimentos mensais: o prazo fixo e quase sempre interpolado e dilui evento discreto (eleicao). Ver domain/db/brasil/b3/cmb_vol_implicita.py.'
"""


def _conectar():
    return mysql.connector.connect(
        host=os.environ.get("MYSQL_HOST", "localhost"),
        user=os.environ.get("MYSQL_USER", "root"),
        password=os.environ.get("MYSQL_PASSWORD", ""),
        database=_DATABASE,
    )


def _garantir_tabela() -> None:
    cnx = _conectar()
    try:
        cur = cnx.cursor()
        cur.execute(_DDL)
        cnx.commit()
    finally:
        cnx.close()


def _black(F, K, T, D, s, call: bool) -> float:
    sq = s * np.sqrt(T)
    d1 = (np.log(F / K) + sq * sq / 2) / sq
    d2 = d1 - sq
    if call:
        return D * (F * norm.cdf(d1) - K * norm.cdf(d2))
    return D * (K * norm.cdf(-d2) - F * norm.cdf(-d1))


def _iv(premio, F, K, T, D, call: bool) -> float:
    intr = max(0.0, D * ((F - K) if call else (K - F)))
    if premio <= intr + 1e-9:
        return np.nan
    try:
        return brentq(lambda s: _black(F, K, T, D, s, call) - premio, 1e-4, 5.0)
    except ValueError:
        return np.nan


def _paridade(c: pd.Series, p: pd.Series) -> tuple[float, float] | None:
    k = c.index.intersection(p.index)
    if len(k) < 3:
        return None
    ks = np.array(k, dtype=float)
    y = (c[k] - p[k]).values
    a, b = np.linalg.lstsq(np.c_[np.ones(len(ks)), ks], y, rcond=None)[0]
    D = -b
    if D <= 0:
        return None
    F = a / D
    perto = np.abs(ks / F - 1) <= 0.20
    if perto.sum() >= 3:
        a, b = np.linalg.lstsq(np.c_[np.ones(perto.sum()), ks[perto]], y[perto], rcond=None)[0]
        D = -b
        if D <= 0:
            return None
        F = a / D
    return F, D


def vol_por_vencimento(P: pd.DataFrame, data) -> pd.DataFrame:
    """(vencimento, dias, F, D, vol) de um pregao. Vol em fracao, nao %."""
    data = pd.Timestamp(data)
    out = []
    for venc, g in P.groupby("vencimento"):
        dias = (pd.Timestamp(venc) - data).days
        if dias < 1:
            continue
        T = dias / 365
        c = g[g.tipo == "C"].set_index("strike").premio
        p = g[g.tipo == "V"].set_index("strike").premio
        fd = _paridade(c, p)
        if fd is None:
            continue
        F, D = fd
        if not (_D_MIN <= D <= 1.0001):
            continue
        k = sorted(c.index.intersection(p.index))
        abaixo = [x for x in k if x <= F]
        acima = [x for x in k if x >= F]
        if not abaixo or not acima:
            continue
        k1, k2 = abaixo[-1], acima[0]
        v1 = _iv(p[k1], F, k1, T, D, call=False)
        v2 = _iv(c[k2], F, k2, T, D, call=True)
        if np.isnan(v1) or np.isnan(v2):
            continue
        vol = v1 if k2 == k1 else v1 + (v2 - v1) * (F - k1) / (k2 - k1)
        out.append((pd.Timestamp(venc), dias, F, D, vol))
    return pd.DataFrame(out, columns=["vencimento", "dias", "F", "D", "vol"])


def nos_prazos(V: pd.DataFrame) -> dict[str, float]:
    """Vol (em %) em cada prazo fixo cercado por dois vencimentos."""
    if len(V) < 2:
        return {}
    V = V.sort_values("dias")
    dias, var = V.dias.values.astype(float), (V.vol.values ** 2) * V.dias.values
    res = {}
    for prazo, n in PRAZOS.items():
        if n < dias[0] or n > dias[-1]:
            continue
        res[prazo] = round(100 * np.sqrt(np.interp(n, dias, var) / n), 6)
    return res


def coletar(full: bool = False, dias: int = _DIAS_ROTINA) -> pd.DataFrame:
    fim = pd.Timestamp.today().normalize()
    datas = list(pd.bdate_range(_INICIO, fim) if full else pd.bdate_range(end=fim, periods=dias))
    b3_premio.baixar_muitos(datas)
    linhas, sem = [], []
    for d in datas:
        P = b3_premio.premios(d)
        if P is None:
            sem.append(d.date())
            continue
        for prazo, v in nos_prazos(vol_por_vencimento(P, d)).items():
            linhas.append((d.date(), prazo, v))
    if sem:
        logger.info("cmb_vol_implicita: %d pregoes sem arquivo RE (%s%s)", len(sem),
                    sem[:5], " ..." if len(sem) > 5 else "")
    df = pd.DataFrame(linhas, columns=["date", "prazo", "value"])
    fora = df[(df.value < _VOL_MIN) | (df.value > _VOL_MAX)]
    if len(fora):
        raise ValueError(f"cmb_vol_implicita: {len(fora)} vols fora de [{_VOL_MIN}, "
                         f"{_VOL_MAX}]:\n{fora.head().to_string()}")
    return df


def run(full: bool = False, dias: int = _DIAS_ROTINA) -> None:
    """Atualiza macro_brasil.cmb_vol_implicita.

    Args:
        full: True recarrega de 2006-01-02 (~5.200 pregoes; num cache vazio,
              horas -- a B3 aceita 2 conexoes).
        dias: dias uteis para tras no passe de rotina.
    """
    _garantir_tabela()
    df = coletar(full=full, dias=dias)
    if df.empty:
        logger.warning("cmb_vol_implicita: nada a inserir")
        return
    logger.info("cmb_vol_implicita: %d linhas, %s -> %s", len(df), df.date.min(), df.date.max())
    insert_data_into_database(_DATABASE, _TABLE, df)
