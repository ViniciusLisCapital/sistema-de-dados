"""The candidate forecasters, behind one interface.

Every model implements ``fit_predict(Xtr, ytr, xnow) -> float``, receives only
the training window the backtest hands it, and returns the predicted cumulative
h-month log return in pp. A model never sees a date, so it cannot accidentally
condition on one; and it never sees the scored point, so there is no path by
which a leak can enter here rather than in `features.py`.

Standardisation lives inside each model, fitted on ``Xtr`` alone. Doing it once
over the full sample — the obvious convenience — leaks the future's mean and
variance into every fold, which inflates out-of-sample scores by a margin that
is small enough to look like a real win.

The line-up is chosen so that a loss is as informative as a win:

- ``RandomWalk`` predicts zero. This is the Meese-Rogoff benchmark and the
  thing every other row has to beat.
- ``HistoricalMean`` is the drifted random walk — it gets the sample's own
  depreciation trend for free. Against a currency that lost ~80% of its value
  over the sample, that is the harder benchmark, not the softer one.
- The regressions (``OLS``, ``Ridge``) are the direct test of "is there
  information in the state variables".
- ``Shrunk`` wraps any model and pulls its forecast toward the random walk by a
  fixed factor. This is the Campbell-Thompson move, and it is here because a
  regression with 20 regressors and 150 observations is nearly guaranteed to
  beat the benchmark in-sample and lose out of sample; shrinkage is what usually
  decides whether the loss becomes a win.
- ``Combination`` averages univariate forecasts instead of fitting them jointly.
  In the return-predictability literature this beats the joint regression
  reliably, because the joint fit spends its degrees of freedom on collinearity.
  The shipped FX model's own drop-one analysis measured 71% of its fit as shared
  between channels, so that failure mode is present in this data too.
"""

from __future__ import annotations

import numpy as np


def _standardize(Xtr, xnow):
    mu = Xtr.mean(axis=0)
    sd = Xtr.std(axis=0, ddof=0)
    sd = np.where(sd < 1e-12, 1.0, sd)
    return (Xtr - mu) / sd, (xnow - mu) / sd


def _ridge_solve(Xz, yc, lam):
    k = Xz.shape[1]
    A = Xz.T @ Xz + lam * np.eye(k)
    return np.linalg.solve(A, Xz.T @ yc)


class Forecaster:
    name = "base"

    def fit_predict(self, Xtr: np.ndarray, ytr: np.ndarray, xnow: np.ndarray) -> float:
        raise NotImplementedError


class RandomWalk(Forecaster):
    """No drift. The level stays where it is, so the h-month return is zero."""
    name = "rw"

    def fit_predict(self, Xtr, ytr, xnow):
        return 0.0


class HistoricalMean(Forecaster):
    """Random walk with drift, drift estimated on the training window only."""
    name = "rw_drift"

    def fit_predict(self, Xtr, ytr, xnow):
        return float(np.mean(ytr))


class OLS(Forecaster):
    name = "ols"

    def fit_predict(self, Xtr, ytr, xnow):
        Xz, xz = _standardize(Xtr, xnow)
        ybar = ytr.mean()
        beta, *_ = np.linalg.lstsq(Xz, ytr - ybar, rcond=None)
        return float(ybar + xz @ beta)


class Ridge(Forecaster):
    """Ridge with lambda re-selected on each training window by an inner,
    expanding-window walk-forward — never by cross-validation that shuffles
    time, and never on a point that will be scored.

    The inner split reuses the same logic as the outer one on purpose: a lambda
    picked by k-fold CV on overlapping h-month returns is picked on folds whose
    training and validation halves share observations, which is how a penalty
    that is far too small ends up looking optimal.
    """
    name = "ridge"

    def __init__(self, lambdas=None, min_inner: int = 36, name: str | None = None):
        self.lambdas = np.logspace(-2, 3, 16) if lambdas is None else np.asarray(lambdas)
        self.min_inner = min_inner
        if name:
            self.name = name
        self.last_lambda = np.nan

    def _pick_lambda(self, Xz, yc):
        n = len(yc)
        if n <= self.min_inner + 6:
            return float(np.median(self.lambdas))
        err = np.zeros(len(self.lambdas))
        cnt = 0
        for t in range(self.min_inner, n):
            Xi, yi = Xz[:t], yc[:t]
            G = Xi.T @ Xi
            b = Xi.T @ yi
            k = Xz.shape[1]
            for j, lam in enumerate(self.lambdas):
                try:
                    beta = np.linalg.solve(G + lam * np.eye(k), b)
                except np.linalg.LinAlgError:
                    beta = np.zeros(k)
                err[j] += (yc[t] - Xz[t] @ beta) ** 2
            cnt += 1
        return float(self.lambdas[int(np.argmin(err))]) if cnt else float(np.median(self.lambdas))

    def fit_predict(self, Xtr, ytr, xnow):
        Xz, xz = _standardize(Xtr, xnow)
        ybar = ytr.mean()
        yc = ytr - ybar
        lam = self._pick_lambda(Xz, yc)
        self.last_lambda = lam
        beta = _ridge_solve(Xz, yc, lam)
        return float(ybar + xz @ beta)


class Shrunk(Forecaster):
    """``w * inner + (1 - w) * benchmark``. With ``toward='rw'`` the benchmark
    is zero, with ``'mean'`` it is the training mean."""

    def __init__(self, inner: Forecaster, w: float = 0.5, toward: str = "rw"):
        self.inner, self.w, self.toward = inner, w, toward
        self.name = f"{inner.name}_shrunk{int(w * 100)}"

    def fit_predict(self, Xtr, ytr, xnow):
        base = 0.0 if self.toward == "rw" else float(np.mean(ytr))
        return self.w * self.inner.fit_predict(Xtr, ytr, xnow) + (1 - self.w) * base


class Combination(Forecaster):
    """Mean of the univariate OLS forecasts, one per column.

    Each column gets its own ``y = a + b*x`` on the training window; the
    forecast is the simple average of the k predictions. No weights are
    estimated, which is the whole point — estimated combination weights
    reintroduce exactly the parameter noise this is meant to avoid.
    """
    name = "combo"

    def __init__(self, trim: bool = False, name: str | None = None):
        self.trim = trim
        if name:
            self.name = name

    def fit_predict(self, Xtr, ytr, xnow):
        preds = []
        ybar = ytr.mean()
        for j in range(Xtr.shape[1]):
            x = Xtr[:, j]
            sd = x.std(ddof=0)
            if sd < 1e-12:
                preds.append(ybar)
                continue
            xc = (x - x.mean()) / sd
            b = float(xc @ (ytr - ybar) / (xc @ xc))
            preds.append(ybar + b * (xnow[j] - x.mean()) / sd)
        preds = np.asarray(preds)
        if self.trim and len(preds) >= 5:
            lo, hi = np.percentile(preds, [10, 90])
            keep = preds[(preds >= lo) & (preds <= hi)]
            if len(keep):
                preds = keep
        return float(np.mean(preds))


class CampbellThompson(Forecaster):
    """Wraps a model with the two sign restrictions from Campbell-Thompson
    (2008): clip the forecast's implied move so it never contradicts the
    sample's own drift direction, and fall back to the training mean whenever
    the model would predict an appreciation larger than anything in the window.

    Included because it is the cheapest known fix for regression forecasts that
    are directionally right and wildly over-scaled — which is the specific way a
    small-sample FX regression usually loses to a random walk.
    """

    def __init__(self, inner: Forecaster):
        self.inner = inner
        self.name = f"{inner.name}_ct"

    def fit_predict(self, Xtr, ytr, xnow):
        p = self.inner.fit_predict(Xtr, ytr, xnow)
        lo, hi = np.percentile(ytr, [5, 95])
        return float(np.clip(p, lo, hi))
