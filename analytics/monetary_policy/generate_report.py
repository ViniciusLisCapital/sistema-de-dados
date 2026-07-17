"""
Gerador do relatorio HTML de cenarios do modelo agregado do BCB.

Roda o motor de simulacao (model.py) para um cenario-base (Selic endogena via
regra de Taylor) e um cenario de choque (Selic +1pp por 4 trimestres, mesmo
experimento do proprio box do BCB — ver referencia/MODEL_REPLICATION_PLAN.md),
injeta os resultados no template report.html.

Uso:
    uv run python analytics/monetary_policy/generate_report.py
    uv run python -c "from analytics.monetary_policy.generate_report import run; run()"
"""

import json
from datetime import datetime
from pathlib import Path

import pandas as pd

from analytics.monetary_policy.model import load_history, load_parameters, load_seed, simulate

_HERE = Path(__file__).parent
_TEMPLATE = _HERE / "report.html"

_DECOMP_LABELS = {
    "decomp_inercia_propria": "Inercia (livres)",
    "decomp_inercia_ipca":    "Inercia (IPCA)",
    "decomp_expectativas":    "Expectativas (Focus)",
    "decomp_commodities":     "Commodities",
    "decomp_cambio":          "Cambio",
    "decomp_hiato":           "Hiato do produto",
    "decomp_clima":           "Clima",
}


def _quarter_labels(last_hist_date: pd.Timestamp, n: int) -> list[str]:
    future = pd.date_range(last_hist_date + pd.DateOffset(months=3), periods=n, freq="QS")
    return [f"{d.year}T{d.quarter}" for d in future]


def _df_to_cols(df: pd.DataFrame) -> dict:
    return {col: [round(float(v), 4) for v in df[col]] for col in df.columns if col != "quarter"}


def run(output: str = "reports/bcb_model.html", n_quarters: int = 8) -> None:
    print("Carregando parametros, seed e historico...")
    coef = load_parameters()
    seed = load_seed()
    hist = load_history()

    baseline = simulate(n_quarters=n_quarters)
    base_selic = dict(zip(baseline["quarter"] - 1, baseline["selic"]))
    shock_selic = {q: base_selic[q] + 1.0 for q in range(min(4, n_quarters))}
    shocked = simulate(n_quarters=n_quarters, scenario={"selic_override": shock_selic})

    labels = _quarter_labels(hist.index.max(), n_quarters)

    data = {
        "generated_at": datetime.now().strftime("%d/%m/%Y %H:%M"),
        "quarters": labels,
        "kpi": {
            "selic_atual":       round(float(hist["selic"].iloc[-1]), 2),
            "fed_funds_atual":   round(float(hist["fed_funds"].iloc[-1]), 2),
            "meta_inflacao":     round(float(hist["meta_inflacao"].iloc[-1]), 2),
            "focus_ipca_12m":    round(float(hist["focus_ipca_12m"].iloc[-1]), 2),
            "pi_livres_ultimo_trim": round(float(hist["pi_livres"].iloc[-1]), 2),
            "hiato_seed":        {"value": round(seed["output_gap"][0], 2), "as_of": seed["output_gap"][1].strftime("%Y-%m")},
            "taxa_neutra_seed":  {"value": round(seed["neutral_rate"][0], 2), "as_of": seed["neutral_rate"][1].strftime("%Y-%m")},
        },
        "baseline": _df_to_cols(baseline),
        "shock":    _df_to_cols(shocked),
        "decomp_labels": _DECOMP_LABELS,
    }
    print(f"  {n_quarters} trimestres simulados ({labels[0]} -> {labels[-1]})")

    template = _TEMPLATE.read_text(encoding="utf-8")
    payload = json.dumps(data, ensure_ascii=False, default=str)
    html = template.replace("/*REPORT_DATA*/", f"const REPORT_DATA = {payload};")

    out = Path(output)
    out.parent.mkdir(exist_ok=True)
    out.write_text(html, encoding="utf-8")
    print(f"Relatorio salvo: {out.resolve()}")


if __name__ == "__main__":
    run()
