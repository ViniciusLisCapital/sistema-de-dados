"""Markdown tables from a horse-race CSV.

    uv run python -m tests.fx_forecast_lab.tables
    uv run python -m tests.fx_forecast_lab.tables --tag expanding --spec wide_2001

Exists so that any number quoted about this lab is printed from
``results/horserace_<tag>.csv`` rather than retyped from a console scroll. Two
views, because they answer different questions:

- the **Theil U grid** (one table per horizon, models x specs) answers "did
  anything beat the random walk";
- the **full statistics** table answers "and does the gap survive a test",
  which needs RMSE, R2-OOS, both tests, the bootstrap CI and the two
  benchmark-relative diagnostics side by side.

The grid must be read down a column, never across a row: each spec has its own
natural start (dxy_em 2006, contracted FX 2008), so two specs at the same
horizon are two different samples. The engine aligns origins *within* a cell,
never across specs.
"""

from __future__ import annotations

import argparse
import os

import numpy as np
import pandas as pd

RESULTS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "results")

MODEL_ORDER = ["rw", "rw_drift", "ols", "ridge", "ridge_ct", "ridge_shrunk50",
               "ridge_shrunk25", "combo", "combo_trim", "combo_shrunk50"]

MODEL_LABEL = {
    "rw": "RW (benchmark)",
    "rw_drift": "RW + drift",
    "ols": "OLS",
    "ridge": "Ridge",
    "ridge_ct": "Ridge + Campbell-Thompson",
    "ridge_shrunk50": "Ridge, 50% toward RW",
    "ridge_shrunk25": "Ridge, 25% toward RW",
    "combo": "Combination (univariate mean)",
    "combo_trim": "Combination, trimmed",
    "combo_shrunk50": "Combination, 50% toward RW",
}


def _order(df: pd.DataFrame) -> pd.DataFrame:
    cat = pd.CategoricalDtype(MODEL_ORDER, ordered=True)
    return df.assign(model=df["model"].astype(cat)).sort_values("model")


def u_grid(d: pd.DataFrame) -> str:
    out = []
    specs = [s for s in ["technical", "fundamentals", "fund_tech", "wide_2001",
                         "wide_2008", "shipped_lagged"] if s in set(d["spec"])]
    for h in sorted(d["h"].unique()):
        sub = d[d.h == h]
        piv = sub.pivot_table(index="model", columns="spec", values="theil_u")
        piv = piv.reindex(index=[m for m in MODEL_ORDER if m in piv.index], columns=specs)
        ns = sub.groupby("spec")["n"].first().reindex(specs)
        out.append(f"\n**h = {h} mes(es)** — origins por spec: "
                   + ", ".join(f"{s} {int(n)}" for s, n in ns.items()))
        out.append("")
        out.append("| modelo | " + " | ".join(specs) + " |")
        out.append("|---|" + "---|" * len(specs))
        for m in piv.index:
            cells = []
            for s in specs:
                v = piv.loc[m, s]
                if not np.isfinite(v):
                    cells.append("—")
                elif m == "rw":
                    cells.append("1.000")
                else:
                    cells.append(f"**{v:.3f}**" if v < 1 else f"{v:.3f}")
            out.append(f"| {MODEL_LABEL.get(m, m)} | " + " | ".join(cells) + " |")
        out.append("")
    return "\n".join(out)


def full_stats(d: pd.DataFrame, spec: str) -> str:
    out = []
    sub = _order(d[d.spec == spec])
    for h in sorted(sub["h"].unique()):
        s = sub[sub.h == h]
        n = int(s["n"].iloc[0])
        out.append(f"\n**{spec} · h = {h}** — {n} origins, "
                   f"{s['first'].iloc[0]} a {s['last'].iloc[0]}  "
                   f"(RMSE do RW: {s['rmse_bench'].iloc[0]:.3f} pp)")
        out.append("")
        out.append("| modelo | RMSE | Theil U | R²-OOS | CW p | DM p | IC 95% de U | "
                   "acerto de sinal | mais perto que RW | viés |")
        out.append("|---|---|---|---|---|---|---|---|---|---|")
        for _, r in s.iterrows():
            if r["model"] == "rw":
                out.append(f"| {MODEL_LABEL.get(r['model'], r['model'])} | "
                           f"{r['rmse']:.3f} | 1.000 | 0.000 | — | — | — | — | — | "
                           f"{r['bias']:+.2f} |")
                continue
            ci = (f"[{r['u_ci_lo']:.2f}, {r['u_ci_hi']:.2f}]"
                  if np.isfinite(r["u_ci_lo"]) else "—")
            u = f"**{r['theil_u']:.3f}**" if r["theil_u"] < 1 else f"{r['theil_u']:.3f}"
            out.append(
                f"| {MODEL_LABEL.get(r['model'], r['model'])} | {r['rmse']:.3f} | {u} | "
                f"{r['r2_oos']:+.3f} | {r['cw_p']:.3f} | {r['dm_p']:.3f} | {ci} | "
                f"{r['hit_rate']:.1%} | {r['closer_than_bench']:.1%} | {r['bias']:+.2f} |")
        out.append("")
    return "\n".join(out)


def summary(d: pd.DataFrame) -> str:
    m = d[d.model != "rw"]
    n_cells = len(m)
    beat = m[m.theil_u < 1]
    sig = m[m.cw_p < 0.05]
    both = m[(m.theil_u < 1) & (m.cw_p < 0.05)]
    both_ci = both[both.u_ci_hi < 1]
    lines = [
        f"- células modelo×spec×horizonte: **{n_cells}**",
        f"- com Theil U < 1: **{len(beat)}** ({len(beat) / n_cells:.1%})",
        f"- com Clark-West p < 0.05: **{len(sig)}** "
        f"(esperado sob o nulo: ~{0.05 * n_cells:.0f})",
        f"- com U < 1 **e** CW p < 0.05: **{len(both)}**",
        f"- ... e com o IC 95% de U inteiramente abaixo de 1: **{len(both_ci)}**",
        f"- melhor U do painel: **{m.theil_u.min():.3f}** "
        f"({m.loc[m.theil_u.idxmin(), 'spec']}, h={int(m.loc[m.theil_u.idxmin(), 'h'])}, "
        f"{m.loc[m.theil_u.idxmin(), 'model']})",
    ]
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tag", default="main")
    ap.add_argument("--spec", default="wide_2001",
                    help="spec for the full-statistics table")
    ap.add_argument("--which", default="all", choices=["all", "grid", "full", "summary"])
    args = ap.parse_args()

    d = pd.read_csv(os.path.join(RESULTS_DIR, f"horserace_{args.tag}.csv"))
    if args.which in ("all", "summary"):
        print("### Resumo\n")
        print(summary(d))
    if args.which in ("all", "grid"):
        print("\n### Theil U — todos os modelos, todas as specs\n")
        print(u_grid(d))
    if args.which in ("all", "full"):
        print(f"\n### Estatísticas completas — spec `{args.spec}`\n")
        print(full_stats(d, args.spec))


if __name__ == "__main__":
    main()
