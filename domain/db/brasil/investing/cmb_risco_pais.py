"""
Risco-pais (CDS Brasil 5 anos, USD).

Preenche a lacuna "Country risk / sovereign spread (EMBI or CDS)" identificada
em analytics/exchange_rate/models/DATA_REQUIREMENTS.md como um dos dois gaps
de dados do fiscal_credibility_model (o outro e' o resultado fiscal em si).
CDS Brasil 5Y costuma ser uma serie paga (Bloomberg/Refinitiv); os 4 CSVs em
raw/ foram exportados manualmente do investing.com pelo usuario (2026-07-23).

Diferente dos demais scripts em domain/db/: nao ha conector de API — o
investing.com nao expõe uma API publica gratuita para series historicas.
run() le os CSVs ja presentes em raw/ em vez de buscar de uma fonte externa.
Para atualizar no futuro, exportar um novo CSV do investing.com cobrindo o
periodo faltante e adicionar em raw/ antes de rodar run() de novo — os nomes
dos arquivos nao importam, so o conteudo (todos os CSVs em raw/ sao lidos e
combinados).

Formato do CSV (export padrao investing.com, "Visão Geral"):
  Data (DD.MM.YYYY), Último, Abertura, Máxima, Mínima, Var%
Só "Último" (fechamento diário, em bps) é armazenado — Abertura/Máxima/Mínima/
Var% não têm uso identificado neste projeto (nenhuma tabela existente guarda
OHLC) e foram deixados de fora para não carregar colunas sem consumidor.

Gap real confirmado nos dados-fonte: 2015-12-02 -> 2015-12-31 (31 dias) não
aparece em nenhum dos 4 exports — não é um bug desta ingestão, os arquivos
brutos em raw/ genuinamente pulam esse mês.

Banco: macro_brasil.cmb_risco_pais — PRIMARY KEY (date, name)
"""

import logging
from pathlib import Path

import pandas as pd

from connectors.mysql import insert_data_into_database

logger = logging.getLogger(__name__)

_DATABASE = "macro_brasil"
_TABLE    = "cmb_risco_pais"
_NOME     = "cds_5y_usd"
_RAW_DIR  = Path(__file__).resolve().parent / "raw"


def _load_raw(raw_dir: Path) -> pd.DataFrame:
    frames = []
    for csv_path in sorted(raw_dir.glob("*.csv")):
        df = pd.read_csv(csv_path, encoding="utf-8-sig")
        frames.append(df[["Data", "Último"]])
    combined = pd.concat(frames, ignore_index=True)

    combined["date"] = pd.to_datetime(combined["Data"], format="%d.%m.%Y")
    combined["value"] = (
        combined["Último"].astype(str).str.replace(".", "", regex=False).str.replace(",", ".", regex=False).astype(float)
    )
    combined = combined.drop_duplicates(subset="date").sort_values("date")
    combined["name"] = _NOME
    return combined[["date", "name", "value"]]


def run(raw_dir: str | None = None) -> None:
    """Atualiza macro_brasil.cmb_risco_pais a partir dos CSVs em raw/.

    Args:
        raw_dir: pasta com os CSVs brutos do investing.com. Default: raw/
                 ao lado deste script.
    """
    df = _load_raw(Path(raw_dir) if raw_dir else _RAW_DIR)
    logger.info("cmb_risco_pais: %d linhas, %s -> %s", len(df), df["date"].min().date(), df["date"].max().date())
    insert_data_into_database(_DATABASE, _TABLE, df)
