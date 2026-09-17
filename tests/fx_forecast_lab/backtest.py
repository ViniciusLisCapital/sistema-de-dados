"""Walk-forward engine and the statistics that decide whether a win is real.

Design, and the reasons each choice is not the obvious one:

- **Direct, not iterated.** One model per horizon, regressing the cumulative
  h-month log return on the state at the origin. The iterated alternative — a
  one-month model fed its own output h times — needs a projected path for every
  regressor, and projecting the regressors is precisely the part that
  `models/ridge_vs_random_walk.md` measured as unforecastable (CDS is *harder*
  to predict from its own past than the exchange rate is). Direct forecasting
  sidesteps that entirely: the regression learns the h-month mapping itself.

- **Overlapping origins, and every test corrected for it.** Monthly origins with
  an h-month horizon overlap by construction, so the errors are serially
  correlated by design and a naive t-test on them is badly oversized. Every
  variance here is Bartlett-HAC with bandwidth h-1, and the bootstrap resamples
  blocks of length h rather than single observations.

- **Clark-West, not Diebold-Mariano, for the headline.** The driftless random
  walk is *nested* inside every regression here (all slopes and the intercept at
  zero). Under nesting DM is undersized and its null is non-standard; CW
  corrects for the estimation noise the larger model pays. Both are reported,
  because the gap between them is itself diagnostic — when DM says "no" and CW
  says "yes", the model is paying more in parameter noise than it earns in
  signal, which is an argument for shrinkage rather than for the model.

- **Aligned origins across models.** Two specs with different natural starts
  score on different folds, and comparing their U ratios then compares samples
  rather than models. ``run_horserace`` intersects the origin sets before
  scoring anything.
"""

from __future__ import annotations

import numpy as np
import pandas as pd
from scipy import stats


# --------------------------------------------------------------------------
# variance / tests
# --------------------------------------------------------------------------

def hac_se(x: np.ndarray, bandwidth: int) -> float:
    """Newey-West / Bartlett standard error of the mean of x."""
    x = np.asarray(x, dtype=float)
    n = len(x)
    xc = x - x.mean()
    gamma0 = float(xc @ xc) / n
    s = gamma0
    for lag in range(1, max(bandwidth, 0) + 1):
        if lag >= n:
            break
        w = 1.0 - lag / (bandwidth + 1.0)
        cov = float(xc[lag:] @ xc[:-lag]) / n
        s += 2.0 * w * cov
    s = max(s, 1e-18)
    return float(np.sqrt(s / n))


def clark_west(y: np.ndarray, f_bench: np.ndarray, f_model: np.ndarray, h: int):
    """One-sided CW test that the larger model improves on the nested benchmark."""
    f = (y - f_bench) ** 2 - ((y - f_model) ** 2 - (f_bench - f_model) ** 2)
    se = hac_se(f, max(h - 1, 0))
    t = float(f.mean() / se)
    return t, float(1 - stats.norm.cdf(t))


def diebold_mariano(y: np.ndarray, f_bench: np.ndarray, f_model: np.ndarray, h: int):
    """DM with the Harvey-Leybourne-Newbold small-sample correction, two-sided."""
    d = (y - f_bench) ** 2 - (y - f_model) ** 2
    n = len(d)
    se = hac_se(d, max(h - 1, 0))
    t = float(d.mean() / se)
    corr = np.sqrt(max((n + 1 - 2 * h + h * (h - 1) / n) / n, 1e-9))
    t_adj = t * corr
    return float(t_adj), float(2 * (1 - stats.t.cdf(abs(t_adj), df=n - 1)))


def block_bootstrap_u(y, f_bench, f_model, h: int, draws: int = 4000, seed: int = 7):
    """Percentile CI for Theil's U from a moving-block bootstrap, block = h."""
    rng = np.random.default_rng(seed)
    e_b = (y - f_bench) ** 2
    e_m = (y - f_model) ** 2
    n = len(y)
    L = max(h, 1)
    if n <= L:
        return (np.nan, np.nan)
    starts_pool = n - L + 1
    nblocks = int(np.ceil(n / L))
    out = np.empty(draws)
    for d in range(draws):
        starts = rng.integers(0, starts_pool, nblocks)
        idx = np.concatenate([np.arange(s, s + L) for s in starts])[:n]
        denom = e_b[idx].mean()
        out[d] = np.sqrt(e_m[idx].mean() / denom) if denom > 0 else np.nan
    return tuple(np.nanpercentile(out, [2.5, 97.5]))


# --------------------------------------------------------------------------
# engine
# --------------------------------------------------------------------------

def make_origins(X: pd.DataFrame, y: pd.Series, cols: list[str],
                 min_train: int, h: int) -> pd.DatetimeIndex:
    """Origins with a complete feature row, a realized target, and at least
    ``min_train`` training rows whose own targets were already realized at the
    origin. Computed once and shared by every model in a comparison, so a U
    ratio never compares two different samples."""
    avail = X[cols].dropna().index.intersection(y.dropna().index).sort_values()
    usable = []
    for t0 in avail:
        past = avail[avail < t0]
        past = past[past + pd.DateOffset(months=h) <= t0]
        if len(past) >= min_train:
            usable.append(t0)
    return pd.DatetimeIndex(usable)


def walk_forward(X: pd.DataFrame, y: pd.Series, cols: list[str], model,
                 origins: pd.DatetimeIndex, window: int | None = 120,
                 min_train: int = 60) -> pd.Series:
    """Refit at every origin, predict that origin's h-month return.

    ``window=None`` is an expanding window. A training row is admitted only if
    its own target is already realized at the origin — that is the ``t + h <=
    origin`` filter below, and it is the single easiest leak to ship: without
    it, the fold at origin T trains on h months of returns that had not
    happened yet at T.
    """
    Xs = X[cols]
    avail = Xs.dropna().index.intersection(y.dropna().index).sort_values()
    h_off = _horizon_of(y)
    preds = {}
    for t0 in origins:
        train_idx = avail[avail < t0]
        # y[t] is only knowable at t + h; keep only rows already realized.
        train_idx = train_idx[train_idx + pd.DateOffset(months=h_off) <= t0]
        if window is not None:
            train_idx = train_idx[-window:]
        if len(train_idx) < min_train:
            continue
        Xtr = Xs.loc[train_idx].to_numpy(dtype=float)
        ytr = y.loc[train_idx].to_numpy(dtype=float)
        xnow = Xs.loc[t0].to_numpy(dtype=float)
        if not np.isfinite(xnow).all() or not np.isfinite(Xtr).all():
            continue
        preds[t0] = model.fit_predict(Xtr, ytr, xnow)
    return pd.Series(preds, name=getattr(model, "name", "model")).sort_index()


def _horizon_of(y: pd.Series) -> int:
    try:
        return int(str(y.name).split("_")[-1])
    except Exception:
        return 1


def score(y: pd.Series, pred: pd.Series, bench: pd.Series, h: int,
          bootstrap: bool = True) -> dict:
    idx = y.dropna().index.intersection(pred.dropna().index).intersection(bench.dropna().index)
    yv = y.loc[idx].to_numpy(float)
    pv = pred.loc[idx].to_numpy(float)
    bv = bench.loc[idx].to_numpy(float)
    e_m, e_b = yv - pv, yv - bv
    rmse_m = float(np.sqrt(np.mean(e_m ** 2)))
    rmse_b = float(np.sqrt(np.mean(e_b ** 2)))
    u = rmse_m / rmse_b if rmse_b > 0 else np.nan
    cw_t, cw_p = clark_west(yv, bv, pv, h)
    dm_t, dm_p = diebold_mariano(yv, bv, pv, h)
    ci = block_bootstrap_u(yv, bv, pv, h) if bootstrap else (np.nan, np.nan)
    # A model that always predicts zero has no direction to be right about;
    # scoring sign(0) against sign(y) would report it as 0% and read as a
    # finding rather than as the benchmark's definition.
    moved = (yv != 0) & (pv != 0)
    hit = float(np.mean(np.sign(pv[moved]) == np.sign(yv[moved]))) if moved.any() else np.nan
    return dict(
        n=len(idx),
        first=str(idx.min().date()) if len(idx) else None,
        last=str(idx.max().date()) if len(idx) else None,
        rmse=rmse_m, rmse_bench=rmse_b, theil_u=u,
        r2_oos=float(1 - np.mean(e_m ** 2) / np.mean(e_b ** 2)) if rmse_b > 0 else np.nan,
        mae=float(np.mean(np.abs(e_m))), mae_bench=float(np.mean(np.abs(e_b))),
        bias=float(np.mean(e_m)), bias_bench=float(np.mean(e_b)),
        cw_t=cw_t, cw_p=cw_p, dm_t=dm_t, dm_p=dm_p,
        u_ci_lo=ci[0], u_ci_hi=ci[1],
        hit_rate=hit,
        closer_than_bench=float(np.mean(np.abs(e_m) < np.abs(e_b))),
    )
