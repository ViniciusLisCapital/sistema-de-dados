"""
CFTC Commitments of Traders — Traders in Financial Futures (TFF) client.

Downloads annual ZIP files and parses disaggregated positioning data for
currency futures. FX contracts (BRL, MXN, etc.) are in the TFF report,
not the commodity disaggregated report.

Source: https://www.cftc.gov/files/dea/history/fut_fin_txt_{YYYY}.zip
No authentication required.

Columns extracted per contract:
  open_interest  — Open_Interest_All
  lev_long       — Lev_Money_Positions_Long_All  (Leveraged Funds = speculative)
  lev_short      — Lev_Money_Positions_Short_All
  lev_net        — lev_long - lev_short
  nonrept_long   — NonRept_Positions_Long_All
  nonrept_short  — NonRept_Positions_Short_All
"""

import io
import logging
import zipfile
from datetime import datetime
from typing import Dict, List, Optional

import pandas as pd
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

logger = logging.getLogger(__name__)

_BASE_URL = "https://www.cftc.gov/files/dea/history/fut_fin_txt_{year}.zip"

# Map CFTC contract name fragment → ISO currency code
_CONTRACT_MAP: Dict[str, str] = {
    "BRAZILIAN REAL":  "BRL",
    "MEXICAN PESO":    "MXN",
    "CHILEAN PESO":    "CLP",
    "COLOMBIAN PESO":  "COP",
}

# Date column changed name between 2012 and 2013:
#   2010-2012: Report_Date_as_MM_DD_YYYY  (format "%m/%d/%Y")
#   2013+:     Report_Date_as_YYYY-MM-DD  (format "%Y-%m-%d")
_DATE_COL_NEW = "Report_Date_as_YYYY-MM-DD"
_DATE_COL_OLD = "Report_Date_as_MM_DD_YYYY"

_VALUE_COLS = [
    "Open_Interest_All",
    "Lev_Money_Positions_Long_All",
    "Lev_Money_Positions_Short_All",
    "NonRept_Positions_Long_All",
    "NonRept_Positions_Short_All",
]

# Keep _DATE_COL for backwards compat (used in _parse signature reference)
_DATE_COL = _DATE_COL_NEW


def _build_session() -> requests.Session:
    s = requests.Session()
    s.headers["User-Agent"] = "lis-capital-cftc-connector/1.0"
    retry = Retry(
        total=4,
        backoff_factor=1.5,
        status_forcelist=(429, 500, 502, 503, 504),
        allowed_methods=frozenset(["GET"]),
        respect_retry_after_header=True,
    )
    s.mount("https://", HTTPAdapter(max_retries=retry))
    return s


def _col_to_name(col: str) -> str:
    """Map raw CSV column to tidy series name."""
    return {
        "Open_Interest_All":              "open_interest",
        "Lev_Money_Positions_Long_All":   "lev_long",
        "Lev_Money_Positions_Short_All":  "lev_short",
        "NonRept_Positions_Long_All":     "nonrept_long",
        "NonRept_Positions_Short_All":    "nonrept_short",
    }[col]


class CFTC:
    def __init__(self) -> None:
        self._session = _build_session()
        # In-memory ZIP cache: {year: bytes}
        self._zip_cache: Dict[int, bytes] = {}

    def get_cot_fx(
        self,
        contract_names: Optional[List[str]] = None,
        years: Optional[List[int]] = None,
    ) -> pd.DataFrame:
        """
        Fetch TFF COT positioning data for FX futures.

        Args:
            contract_names: CFTC contract name prefixes to include, e.g.
                            ["BRAZILIAN REAL", "MEXICAN PESO"].
                            Defaults to all currencies in _CONTRACT_MAP.
            years:          Calendar years to fetch. Defaults to current year
                            and the two prior years.

        Returns:
            Tidy DataFrame with columns:
                date      Timestamp (Tuesday = report week)
                currency  str  (BRL | MXN | CLP | COP)
                name      str  (open_interest | lev_long | lev_short | lev_net |
                                nonrept_long | nonrept_short)
                value     float64
        """
        if contract_names is None:
            contract_names = list(_CONTRACT_MAP.keys())
        if years is None:
            current = datetime.now().year
            years = [current - 2, current - 1, current]

        frames: List[pd.DataFrame] = []
        for year in years:
            df_year = self._fetch_year(year, contract_names)
            if df_year is not None and not df_year.empty:
                frames.append(df_year)

        if not frames:
            raise RuntimeError(
                f"No CFTC TFF data found for years={years}, "
                f"contracts={contract_names}"
            )

        combined = pd.concat(frames, ignore_index=True)
        # Deduplicate — overlapping years can produce duplicate rows
        combined = combined.drop_duplicates(subset=["date", "currency", "name"])
        return combined.reset_index(drop=True)

    def _fetch_year(
        self, year: int, contract_names: List[str]
    ) -> Optional[pd.DataFrame]:
        url = _BASE_URL.format(year=year)
        if year not in self._zip_cache:
            logger.debug("CFTC TFF downloading year=%d  %s", year, url)
            try:
                resp = self._session.get(url, timeout=120.0)
                resp.raise_for_status()
                self._zip_cache[year] = resp.content
                logger.debug("CFTC year=%d  %.1f MB", year, len(resp.content) / 1e6)
            except requests.HTTPError as e:
                if e.response is not None and e.response.status_code == 404:
                    logger.warning("CFTC TFF year=%d not available (404)", year)
                    return None
                raise

        raw_csv = self._unzip(self._zip_cache[year], year)
        return self._parse(raw_csv, contract_names)

    def _unzip(self, content: bytes, year: int) -> str:
        with zipfile.ZipFile(io.BytesIO(content)) as zf:
            names = zf.namelist()
            if not names:
                raise ValueError(f"Empty ZIP for CFTC year {year}")
            # Pick the text/csv file (ignore any embedded directories)
            txt_files = [n for n in names if n.lower().endswith((".txt", ".csv"))]
            target = txt_files[0] if txt_files else names[0]
            return zf.read(target).decode("utf-8", errors="replace")

    def _parse(self, csv_text: str, contract_names: List[str]) -> pd.DataFrame:
        # Detect which date column is present in this file's header.
        # Note: Report_Date_as_MM_DD_YYYY (2010-2012) also stores values as YYYY-MM-DD,
        # so we infer the format from data rather than from the column name.
        header = csv_text.split("\n")[0]
        date_col = _DATE_COL_NEW if _DATE_COL_NEW in header else _DATE_COL_OLD

        usecols = ["Market_and_Exchange_Names", date_col] + _VALUE_COLS

        df = pd.read_csv(
            io.StringIO(csv_text),
            usecols=usecols,
            dtype={"Market_and_Exchange_Names": str, date_col: str},
            low_memory=False,
        )

        # Filter to requested contracts
        upper_names = {n.upper() for n in contract_names}
        mask = df["Market_and_Exchange_Names"].str.upper().apply(
            lambda s: any(s.startswith(u) for u in upper_names)
        )
        df = df[mask].copy()

        if df.empty:
            found = df["Market_and_Exchange_Names"].unique()[:5].tolist()
            logger.warning(
                "No matching contracts for %s. "
                "Sample contract names in file: %s",
                contract_names,
                found,
            )
            return df

        # Map contract name → ISO currency code
        def _to_iso(name: str) -> str:
            upper = name.upper()
            for fragment, iso in _CONTRACT_MAP.items():
                if upper.startswith(fragment):
                    return iso
            return "UNKNOWN"

        df["currency"] = df["Market_and_Exchange_Names"].apply(_to_iso)
        df["date"] = pd.to_datetime(df[date_col])

        # Coerce numeric columns
        for col in _VALUE_COLS:
            df[col] = pd.to_numeric(df[col], errors="coerce")

        # Unpivot raw columns → tidy
        id_vars = ["date", "currency"]
        tidy = df[id_vars + _VALUE_COLS].copy().melt(
            id_vars=id_vars, var_name="_col", value_name="value"
        )
        tidy["name"] = tidy["_col"].map(_col_to_name)
        tidy = tidy.drop(columns="_col").dropna(subset=["value"])

        # Add derived net position for leveraged funds
        wide = df[["date", "currency"] + _VALUE_COLS].copy()
        net = wide[["date", "currency"]].copy()
        net["name"] = "lev_net"
        net["value"] = (
            wide["Lev_Money_Positions_Long_All"]
            - wide["Lev_Money_Positions_Short_All"]
        )
        net = net.dropna(subset=["value"])

        result = pd.concat([tidy, net], ignore_index=True)
        result["date"] = pd.to_datetime(result["date"])
        return result[["date", "currency", "name", "value"]].reset_index(drop=True)
