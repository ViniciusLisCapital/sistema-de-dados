"""
BIS Statistics API v1 client — Effective Exchange Rates (WS_EER).

API: https://data.bis.org/api/v1/data/WS_EER/{key}/all?format=csv
No authentication required.

Key structure (WS_EER): FREQ.ADJUSTMENT.REF_AREA.BASKET
  FREQ:       M  (monthly)
  ADJUSTMENT: R (real) | N (nominal)
  REF_AREA:   ISO2 country code, e.g. BR, MX, CL, CO
  BASKET:     B (broad) | N (narrow)

Multiple values in one dimension use '+', e.g. "R+N" or "BR+MX".
"""

import io
import logging
from typing import List, Tuple

import pandas as pd
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

logger = logging.getLogger(__name__)

_BASE = "https://stats.bis.org/api/v1/data/WS_EER"

_TYPE_LABEL = {
    ("R", "B"): "real_broad",
    ("R", "N"): "real_narrow",
    ("N", "B"): "nominal_broad",
    ("N", "N"): "nominal_narrow",
}


def _build_session() -> requests.Session:
    s = requests.Session()
    s.headers["User-Agent"] = "lis-capital-bis-connector/1.0"
    retry = Retry(
        total=4,
        backoff_factor=1.0,
        status_forcelist=(429, 500, 502, 503, 504),
        allowed_methods=frozenset(["GET"]),
        respect_retry_after_header=True,
    )
    s.mount("https://", HTTPAdapter(max_retries=retry))
    return s


class BIS:
    def __init__(self) -> None:
        self._session = _build_session()

    def get_eer(
        self,
        countries: List[str],
        types: List[Tuple[str, str]],
        start: str | None = None,
    ) -> pd.DataFrame:
        """
        Fetch Effective Exchange Rates from BIS.

        Args:
            countries: ISO2 country codes, e.g. ["BR", "MX", "CL", "CO"]
            types:     (adjustment, basket) pairs, e.g. [("R","B"), ("R","N"), ("N","B")]
            start:     "YYYY-MM" to filter from that date, or None for full history

        Returns:
            Tidy DataFrame with columns:
                date         Timestamp (month-start)
                country_code str
                reer_type    str  (real_broad | real_narrow | nominal_broad | ...)
                value        float64
        """
        eer_types = "+".join(sorted({t[0] for t in types}))
        baskets = "+".join(sorted({t[1] for t in types}))
        country_str = "+".join(countries)

        # BIS WS_EER key order: FREQ.EER_TYPE.EER_BASKET.REF_AREA
        key = f"M.{eer_types}.{baskets}.{country_str}"
        url = f"{_BASE}/{key}/all"

        params: dict = {"format": "csv"}
        if start:
            params["startPeriod"] = start

        logger.debug("BIS EER GET %s  params=%s", url, params)
        resp = self._session.get(url, params=params, timeout=60.0)
        resp.raise_for_status()

        return self._parse(resp.text, types)

    def _parse(self, text: str, types: List[Tuple[str, str]]) -> pd.DataFrame:
        # BIS CSV may have comment/annotation lines starting with '#'
        clean_lines = [ln for ln in text.splitlines() if not ln.startswith("#")]
        raw = pd.read_csv(io.StringIO("\n".join(clean_lines)), low_memory=False)

        # Normalize column names to UPPER so we're not case-sensitive
        raw.columns = [c.strip().upper() for c in raw.columns]

        # Required columns — BIS WS_EER SDMX-CSV column names
        for col in ("REF_AREA", "EER_TYPE", "EER_BASKET", "TIME_PERIOD", "OBS_VALUE"):
            if col not in raw.columns:
                raise ValueError(
                    f"BIS CSV missing column '{col}'. "
                    f"Available columns: {list(raw.columns)}"
                )

        # Keep only requested (eer_type, basket) pairs
        type_set = {(a, b) for a, b in types}
        mask = [
            (str(et).strip(), str(bk).strip()) in type_set
            for et, bk in zip(raw["EER_TYPE"], raw["EER_BASKET"])
        ]
        df = raw[mask].copy()

        df["value"] = pd.to_numeric(df["OBS_VALUE"], errors="coerce")
        # TIME_PERIOD format: "YYYY-MM" → Timestamp month-start
        df["date"] = pd.to_datetime(df["TIME_PERIOD"].str.strip(), format="%Y-%m")
        df["country_code"] = df["REF_AREA"].str.strip()
        df["reer_type"] = [
            _TYPE_LABEL.get(
                (str(et).strip(), str(bk).strip()),
                f"{str(et).strip().lower()}_{str(bk).strip().lower()}",
            )
            for et, bk in zip(df["EER_TYPE"], df["EER_BASKET"])
        ]

        result = (
            df[["date", "country_code", "reer_type", "value"]]
            .dropna(subset=["value"])
            .reset_index(drop=True)
        )

        logger.debug(
            "BIS EER parsed %d rows, %d country-type combos",
            len(result),
            result.groupby(["country_code", "reer_type"]).ngroups,
        )
        return result
