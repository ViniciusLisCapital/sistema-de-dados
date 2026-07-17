"""
Oceanic Nino Index (ONI) — proxy de anomalia climatica (El Nino/La Nina)
usado na curva de Phillips do modelo agregado de pequeno porte do BCB — ver
analytics/monetary_policy/referencia/MODEL_REPLICATION_PLAN.md.

Fonte: NOAA CPC, texto simples (nao precisa de connector dedicado — um unico
endpoint estatico, sem autenticacao):
  https://www.cpc.ncep.noaa.gov/data/indices/oni.ascii.txt
Colunas: SEAS (estacao movel de 3 meses), YR, TOTAL (SST), ANOM (ONI).

So as 4 estacoes alinhadas ao calendario trimestral (JFM/AMJ/JAS/OND) sao
mantidas — o arquivo da NOAA tem 12 estacoes moveis por ano (DJF, JFM, FMA,
...), mas o modelo do BCB opera em frequencia trimestral; usar so as 4
estacoes que coincidem exatamente com Q1-Q4 do calendario evita ambiguidade
de "qual mes representa a estacao".

Colocado em macro_international (nao macro_brasil) por ser uma serie global
(temperatura do Oceano Pacifico), nao especifica do Brasil — mesma logica
aplicada ao Brent (comm_brent).

Banco: macro_international.clima_oni — PRIMARY KEY (date, name)
"""

import pandas as pd
import requests

from connectors.mysql import insert_data_into_database

_DATABASE = "macro_international"
_TABLE    = "clima_oni"

_URL = "https://www.cpc.ncep.noaa.gov/data/indices/oni.ascii.txt"

_QUARTER_SEASONS = {
    "JFM": 1,
    "AMJ": 4,
    "JAS": 7,
    "OND": 10,
}


def _fetch() -> pd.DataFrame:
    resp = requests.get(_URL, timeout=30)
    resp.raise_for_status()
    lines = resp.text.strip().splitlines()
    rows = [line.split() for line in lines[1:]]
    df = pd.DataFrame(rows, columns=["seas", "yr", "total", "anom"])
    df = df[df["seas"].isin(_QUARTER_SEASONS)]
    df["date"] = df.apply(
        lambda r: pd.Timestamp(year=int(r["yr"]), month=_QUARTER_SEASONS[r["seas"]], day=1),
        axis=1,
    )
    df["value"] = df["anom"].astype(float)
    df["name"] = "oni"
    return df[["date", "name", "value"]]


def run() -> None:
    """Atualiza macro_international.clima_oni (serie completa - fonte NOAA nao pagina)."""
    df = _fetch()
    insert_data_into_database(_DATABASE, _TABLE, df)
