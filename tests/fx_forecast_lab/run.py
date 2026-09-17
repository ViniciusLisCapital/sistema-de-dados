"""Entry point: the unconditional horse race.

    uv run python -m tests.fx_forecast_lab.run
    uv run python -m tests.fx_forecast_lab.run --horizons 1,3 --specs fundamentals
    uv run python -m tests.fx_forecast_lab.run --window 0        # expanding

Every model in a given (spec, horizon) cell is scored on the **same** forecast
origins, and the benchmark is always the driftless random walk. Theil U below 1
means the model beat it; the Clark-West p-value is what says whether the gap
survives the overlap in the folds.
"""

from __future__ import annotations

import argparse
import json
import os

import numpy as np
import pandas as pd

from tests.fx_forecast_lab import backtest as bt
from tests.fx_forecast_lab import models as M
from tests.fx_forecast_lab.data import load_panel
from tests.fx_forecast_lab.features import FEATURE_SETS, build_features, target

RESULTS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "results")

DEFAULT_HORIZONS = [1, 3, 6, 12]
DEFAULT_SPECS = ["fundamentals", "technical", "fund_tech", "wide_2001",
                 "wide_2008", "shipped_lagged"]


def model_lineup():
    return [
        M.RandomWalk(),
        M.HistoricalMean(),
        M.OLS(),
        M.Ridge(),
        M.Shrunk(M.Ridge(), w=0.5),
        M.Shrunk(M.Ridge(), w=0.25),
        M.Combination(),
        M.Combination(trim=True, name="combo_trim"),
        M.Shrunk(M.Combination(), w=0.5),
        M.CampbellThompson(M.Ridge()),
    ]


def run_cell(X, y, cols, h, window, min_train, bootstrap=True):
    origins = bt.make_origins(X, y, cols, min_train=min_train, h=h)
    if len(origins) < 24:
        return None, origins
    preds = {}
    for m in model_lineup():
        preds[m.name] = bt.walk_forward(X, y, cols, m, origins,
                                        window=window, min_train=min_train)
    # Score every model on the origins every model produced, not on its own.
    common = None
    for s in preds.values():
        idx = s.dropna().index
        common = idx if common is None else common.intersection(idx)
    bench = preds["rw"].reindex(common)
    rows = []
    for name, s in preds.items():
        sc = bt.score(y, s.reindex(common), bench, h, bootstrap=bootstrap)
        sc["model"] = name
        rows.append(sc)
    return pd.DataFrame(rows).set_index("model"), common


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--horizons", default=",".join(str(h) for h in DEFAULT_HORIZONS))
    ap.add_argument("--specs", default=",".join(DEFAULT_SPECS))
    ap.add_argument("--window", type=int, default=120,
                    help="rolling training window in months; 0 = expanding")
    ap.add_argument("--min-train", type=int, default=60)
    ap.add_argument("--no-bootstrap", action="store_true")
    ap.add_argument("--tag", default="main")
    args = ap.parse_args()

    horizons = [int(x) for x in args.horizons.split(",") if x.strip()]
    specs = [s.strip() for s in args.specs.split(",") if s.strip()]
    window = None if args.window == 0 else args.window

    panel = load_panel()
    X = build_features(panel)

    os.makedirs(RESULTS_DIR, exist_ok=True)
    all_rows = []
    for spec in specs:
        cols = [c for c in FEATURE_SETS[spec] if c in X.columns]
        print(f"\n{'=' * 78}\nSPEC {spec}  ({len(cols)} features)  "
              f"window={'expanding' if window is None else str(window) + 'm'}\n{'=' * 78}")
        for h in horizons:
            y = target(panel, h)
            tab, origins = run_cell(X, y, cols, h, window, args.min_train,
                                    bootstrap=not args.no_bootstrap)
            if tab is None:
                print(f"\n  h={h}: not enough origins ({len(origins)}) — skipped")
                continue
            n = int(tab["n"].iloc[0])
            print(f"\n  h={h}m   {n} origins   {tab['first'].iloc[0]} -> {tab['last'].iloc[0]}")
            print(f"  {'model':<18}{'RMSE':>8}{'U':>8}{'R2oos':>8}"
                  f"{'CW p':>8}{'DM p':>8}{'U 95% CI':>18}{'hit':>7}{'bias':>8}")
            for name, r in tab.iterrows():
                ci = (f"[{r['u_ci_lo']:.2f}, {r['u_ci_hi']:.2f}]"
                      if np.isfinite(r["u_ci_lo"]) else "-")
                print(f"  {name:<18}{r['rmse']:>8.3f}{r['theil_u']:>8.3f}"
                      f"{r['r2_oos']:>8.3f}{r['cw_p']:>8.3f}{r['dm_p']:>8.3f}"
                      f"{ci:>18}{(r['hit_rate'] if np.isfinite(r['hit_rate']) else float('nan')):>7.1%}{r['bias']:>8.2f}")
            t = tab.reset_index()
            t.insert(0, "spec", spec)
            t.insert(1, "h", h)
            all_rows.append(t)

    if all_rows:
        out = pd.concat(all_rows, ignore_index=True)
        csv = os.path.join(RESULTS_DIR, f"horserace_{args.tag}.csv")
        out.to_csv(csv, index=False)
        meta = dict(window=args.window, min_train=args.min_train,
                    horizons=horizons, specs=specs,
                    built_at=pd.Timestamp.now().isoformat(timespec="seconds"))
        with open(os.path.join(RESULTS_DIR, f"horserace_{args.tag}.json"), "w") as fh:
            json.dump(meta, fh, indent=2)
        print(f"\nwrote {csv}")

        best = (out[out.model != "rw"]
                .sort_values("theil_u")
                .groupby("h").head(3)[["h", "spec", "model", "theil_u", "cw_p", "n"]])
        print("\nbest three per horizon, by Theil U:")
        print(best.sort_values(["h", "theil_u"]).to_string(index=False))


if __name__ == "__main__":
    main()
