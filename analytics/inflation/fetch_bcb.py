"""
Fetch IPCA aggregate series from BCB/SGS and save as CSV.

Covers: headline, componentes (Livres/Administrado/Servicos/Industriais/Alimentacao/
Comercializaveis/Nao Comercializaveis), grupos IBGE, e nucleos do BCB.

Para cada série usada nos gráficos de 3M SAAR, gera uma versão dessazonalizada via
STL (Seasonal-Trend decomposition using Loess), salva com sufixo _sa.

Uso:
    uv run python analytics/inflation/fetch_bcb.py
    uv run python -c "from analytics.inflation.fetch_bcb import run; run()"
"""
from pathlib import Path

import pandas as pd

from connectors.bcb import BCB

# Séries para as quais gerar SA via STL (usadas nos charts de 3M SAAR).
# Todos os núcleos estão aqui (inclusive EX01/EX02, antes de fora) para que o
# dropdown "Núcleo Selecionado" do relatório sempre tenha SAAR disponível,
# qualquer que seja o núcleo escolhido.
_SAAR_SERIES = {
    "IPCA", "IPCA_administrado", "IPCA_livres", "IPCA_industriais",
    "IPCA_alimentacao", "IPCA_servicos",
    "IPCA_comercializaveis", "IPCA_nao_comercializaveis",
    "IPCA_nucleo_medias_aparadas", "IPCA_nucleo_medias_aparadas_sem_suavizacao",
    "IPCA_nucleo_EX0", "IPCA_nucleo_EX01", "IPCA_nucleo_EX02", "IPCA_nucleo_EX03",
    "IPCA_nucleo_EX03_servicos", "IPCA_nucleo_EX03_industriais",
    "IPCA_nucleo_P55", "IPCA_nucleo_EXFE", "IPCA_nucleo_DP",
}

_DATA = Path(__file__).parent / "data"

_SERIES = {
    # Headline
    "IPCA":                                433,
    "IPCA15":                             7478,
    "IPCA_12m":                          13522,
    "IPCA_indice_difusao":               21379,
    # Componentes por tipo de bem/servico
    "IPCA_administrado":                  4449,
    "IPCA_livres":                       11428,
    "IPCA_industriais":                  27863,
    "IPCA_alimentacao":                  27864,
    "IPCA_servicos":                     10844,
    "IPCA_bens_nao_duraveis":            10841,
    "IPCA_bens_semi_duraveis":           10842,
    "IPCA_bens_duraveis":                10843,
    "IPCA_comercializaveis":              4447,
    "IPCA_nao_comercializaveis":          4448,
    # Grupos por finalidade (IPCA)
    "IPCA_grupo_alimentacao_bebidas":     1635,
    "IPCA_grupo_habitacao":               1636,
    "IPCA_grupo_artigos_residencia":      1637,
    "IPCA_grupo_vestuario":               1638,
    "IPCA_grupo_transporte":              1639,
    "IPCA_grupo_comunicacao":             1640,
    "IPCA_grupo_saude_cuidados_pessoais": 1641,
    "IPCA_grupo_despesas_pessoais":       1642,
    "IPCA_grupo_educacao":                1643,
    # Nucleos de inflacao (BCB)
    "IPCA_nucleo_medias_aparadas":                 4466,
    "IPCA_nucleo_medias_aparadas_sem_suavizacao": 11426,
    "IPCA_nucleo_EX0":                            11427,
    "IPCA_nucleo_EX01":                            16121,
    "IPCA_nucleo_DP":                              16122,
    "IPCA_nucleo_EX02":                            27838,
    "IPCA_nucleo_EX03":                            27839,
    "IPCA_nucleo_P55":                             28750,
    "IPCA_nucleo_EXFE":                            28751,
    "IPCA_nucleo_EX03_servicos":                   29683,
    "IPCA_nucleo_EX03_industriais":                29684,
}


def _seasonal_cutoff(dts: "pd.Series") -> str:
    """Return the in-sample cutoff December for seasonal factor estimation.

    Factors are recalculated only when January of a new year arrives —
    that is when the previous December is considered complete and added
    to the in-sample period. December itself is always out-of-sample
    until the following January is observed.

    Examples:
        data through 2026-05 → cutoff 2025-12
        data through 2026-12 → cutoff 2025-12  (Dec still OOS)
        data through 2027-01 → cutoff 2026-12  (Jan triggers recalc)
    """
    last_year = int(dts.max()[:4])
    return f"{last_year - 1}-12"


def _apply_stl_ma3(df: pd.DataFrame) -> pd.DataFrame:
    """Seasonally adjust each SAAR series via STL, then take MA(3), store as _ma3_sa.

    Seasonal factors are estimated on data up to the last complete December
    (auto-detected). The 12 monthly factors are then applied to the full
    series — including months beyond the cutoff — preventing STL end-effects
    from flattening recent SAAR readings.

    STL is fit on the raw monthly series, not on a pre-smoothed MA(3) of it —
    averaging first would blend several calendar months' seasonal patterns
    into one number before STL ever sees it. Seasonally adjust first, then
    average, matching standard practice (BLS/X-13, Dallas Fed annualizing
    convention).

    Deliberately still STL, not the BLS/Census X-13ARIMA-SEATS itself — see
    "Trocar STL por X-13ARIMA-SEATS" in INFLATION.md pendências for why
    (external binary, no pip package, breaks uv-based reproducibility).
    """
    import numpy as np
    from statsmodels.tsa.seasonal import STL

    sa_frames = []
    for name, grp in df.groupby("name"):
        if name not in _SAAR_SERIES:
            continue
        grp = grp.sort_values("dt").reset_index(drop=True)
        vals = grp["value"].astype(float)
        if vals.count() < 24:
            continue

        dts = grp["dt"]
        cutoff = _seasonal_cutoff(dts)
        in_mask = (dts <= cutoff).values
        month_num = pd.to_datetime(dts + "-01").dt.month.values  # 1-12

        # Step 1: fit STL only on the in-sample raw monthly series
        vals_in = vals[in_mask].interpolate(method="linear").ffill().bfill()
        if len(vals_in) < 24:
            continue

        try:
            fit = STL(vals_in.values, period=12, robust=True).fit()
        except Exception as e:
            print(f"  STL failed for {name}: {e}")
            continue

        # Step 2: average seasonal component by calendar month (frozen factors)
        months_in = month_num[in_mask]
        sf = {}
        for m in range(1, 13):
            idx = months_in == m
            if idx.any():
                sf[m] = float(fit.seasonal[idx].mean())

        # Step 3: apply frozen factors to the full raw series
        seasonal = pd.Series(
            [sf.get(m, 0.0) for m in month_num],
            index=vals.index,
        )
        monthly_sa = vals - seasonal

        # Step 4: MA(3) of the already seasonally-adjusted monthly series
        ma3_sa = monthly_sa.rolling(3).mean()

        sa_grp = grp.copy()
        sa_grp["name"] = name + "_ma3_sa"
        sa_grp["value"] = ma3_sa.values
        sa_frames.append(sa_grp)

    return pd.concat(sa_frames, ignore_index=True) if sa_frames else pd.DataFrame(columns=df.columns)


def run(start: str = "01/01/2000") -> pd.DataFrame:
    bcb = BCB()
    print(f"Fetching {len(_SERIES)} IPCA series from BCB/SGS (start={start})...")
    # get_sgs already returns long format: date (Timestamp), name (str), value (float)
    df = bcb.get_sgs(_SERIES, start=start)

    df = df.rename(columns={"date": "dt"})
    df["dt"] = pd.to_datetime(df["dt"]).dt.strftime("%Y-%m")
    df = df.dropna(subset=["value"]).sort_values(["name", "dt"]).reset_index(drop=True)

    print(f"  Applying STL + MA(3) to {len(_SAAR_SERIES)} series...")
    sa_df = _apply_stl_ma3(df)
    if not sa_df.empty:
        df = pd.concat([df, sa_df]).sort_values(["name", "dt"]).reset_index(drop=True)
        print(f"  {len(sa_df)} MA3-SA observations added ({len(sa_df) // len(_SAAR_SERIES)} months/series)")

    _DATA.mkdir(exist_ok=True)
    out = _DATA / "ipca_bcb_series.csv"
    df.to_csv(out, index=False, encoding="utf-8-sig")
    print(f"  {len(df)} total records -> {out}")
    return df


if __name__ == "__main__":
    run()
