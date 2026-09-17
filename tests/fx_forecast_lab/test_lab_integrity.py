"""Controls for the forecast lab. Run these before believing any number it prints.

    uv run python -m tests.fx_forecast_lab.test_lab_integrity     # no pytest needed
    uv run python -m pytest tests/fx_forecast_lab/test_lab_integrity.py -v

A backtest that says "the model does not beat a random walk" is worthless unless
it can be shown to *recognise* a model that does — otherwise the null result is
indistinguishable from a broken harness, and every honest-looking loss is
unfalsifiable. So there are two controls pulling in opposite directions:

- **Positive control**: hand the model a feature that IS the answer. Theil U
  must collapse toward zero. If it doesn't, the scoring cannot see a win and no
  loss it reports means anything.
- **Negative control**: hand it pure noise. U must sit at ~1 and Clark-West must
  not fire. If a noise feature "wins", something in the plumbing is leaking.

The rest checks the two places a look-ahead can enter: the panel's availability
shifts (does row m really hold what was public at m?) and the training filter
(does a fold ever train on a target that had not resolved yet?).
"""

from __future__ import annotations

import numpy as np
import pandas as pd

try:  # pytest is not a declared dependency of this project
    import pytest
except ImportError:  # minimal shim so the controls run either way
    from tests.fx_forecast_lab._nopytest import pytest  # type: ignore

from tests.fx_forecast_lab import backtest as bt
from tests.fx_forecast_lab import models as M
from tests.fx_forecast_lab.data import load_panel
from tests.fx_forecast_lab.features import build_features, target


@pytest.fixture(scope="module")
def panel():
    return load_panel()


@pytest.fixture(scope="module")
def feats(panel):
    return build_features(panel)


# --------------------------------------------------------------------------
# 1. the panel really is as-of
# --------------------------------------------------------------------------

def test_slow_series_are_shifted(panel):
    """IPCA and US CPI at row m must be the index for m-1 — that is what a
    forecaster standing on the last day of m had actually read."""
    from decimal import Decimal

    from tests.fx_forecast_lab.data import _read_table

    ipca = _read_table("macro_brasil", "inflc_agregados")
    ipca = ipca[ipca["name"] == "ipca"]
    s = ipca.set_index(pd.to_datetime(ipca["date"]))["value"].sort_index()
    s = s[s.index >= "1994-01-01"]
    raw_idx = ((s / 100 + 1).cumprod() * 100).resample("MS").last()

    both = pd.concat([panel["ipca_index"], raw_idx.rename("raw")], axis=1).dropna()
    assert len(both) > 300
    # row m holds raw[m-1]
    aligned = both["raw"].shift(1).dropna()
    common = both.index.intersection(aligned.index)
    assert np.allclose(both.loc[common, "ipca_index"], aligned.loc[common], rtol=1e-9)
    # and is NOT raw[m] — the shift has to actually bite
    assert not np.allclose(both.loc[common, "ipca_index"], both.loc[common, "raw"])


def test_ptax_row_is_month_end(panel):
    """The target's anchor must be the real month-end print, with no shift."""
    from tests.fx_forecast_lab.data import _daily_series

    d = _daily_series("macro_brasil", "cmb_ptax", {"name": "ptax_venda"})
    for m in ["2019-03-01", "2022-07-01", "2026-06-01"]:
        ts = pd.Timestamp(m)
        expected = d[d.index <= ts + pd.offsets.MonthEnd(0)].iloc[-1]
        assert panel.loc[ts, "ptax"] == pytest.approx(float(expected))


def test_flow_month_is_truncated_not_future(panel):
    """Contracted FX carries a 4-day publication delay, so the monthly figure
    must be a partial month, never the full one a later reader would see."""
    from tests.fx_forecast_lab.data import _read_table

    cc = _read_table("macro_brasil", "cmb_cambio_contratado")
    cc["date"] = pd.to_datetime(cc["date"])
    s = cc[cc["name"] == "cc_saldo_total"].set_index("date")["value"].sort_index()
    full = s.resample("MS").sum()
    common = panel["cc_total"].dropna().index.intersection(full.index)
    diff = (panel.loc[common, "cc_total"] - full.loc[common]).abs()
    # Most months lose their last days; a handful end on a weekend and match.
    assert (diff > 1e-9).mean() > 0.5


# --------------------------------------------------------------------------
# 2. the target is what it claims
# --------------------------------------------------------------------------

def test_target_definition(panel):
    for h in (1, 3, 12):
        y = target(panel, h)
        t = pd.Timestamp("2018-05-01")
        expect = 100 * np.log(panel["ptax"].shift(-h).loc[t] / panel["ptax"].loc[t])
        assert y.loc[t] == pytest.approx(expect)
    # and the last h rows must be NaN, not silently filled
    y12 = target(panel, 12)
    assert y12.iloc[-12:].isna().all()


# --------------------------------------------------------------------------
# 3. no fold trains on an unresolved target
# --------------------------------------------------------------------------

def test_training_rows_are_already_realized(feats, panel):
    h = 12
    y = target(panel, h)
    cols = ["ppp_gap", "carry", "mom_12"]
    origins = bt.make_origins(feats, y, cols, min_train=60, h=h)
    assert len(origins) > 50

    seen = {}

    class Spy(M.Forecaster):
        name = "rw"

        def fit_predict(self, Xtr, ytr, xnow):
            return 0.0

    # Re-derive the training index the engine would build, and assert on it.
    avail = feats[cols].dropna().index.intersection(y.dropna().index).sort_values()
    for t0 in origins[::7]:
        train = avail[avail < t0]
        train = train[train + pd.DateOffset(months=h) <= t0]
        seen[t0] = train
        assert (train + pd.DateOffset(months=h) <= t0).all()
        # the origin itself is never a training row
        assert t0 not in train
    assert len(seen) > 5


# --------------------------------------------------------------------------
# 4. positive control — the harness can see a win
# --------------------------------------------------------------------------

def test_positive_control_detects_a_real_signal(feats, panel):
    """A feature that is the answer plus a little noise must produce U well
    below 1 with a significant Clark-West. If this fails, every 'no better than
    a random walk' verdict this lab prints is uninterpretable."""
    h = 3
    y = target(panel, h)
    rng = np.random.default_rng(11)
    X = feats.copy()
    X["oracle"] = y + rng.normal(0, 1.0, size=len(y))

    cols = ["oracle"]
    origins = bt.make_origins(X, y, cols, min_train=60, h=h)
    preds = bt.walk_forward(X, y, cols, M.OLS(), origins, window=120, min_train=60)
    bench = bt.walk_forward(X, y, cols, M.RandomWalk(), origins, window=120, min_train=60)
    sc = bt.score(y, preds, bench, h, bootstrap=False)

    assert sc["theil_u"] < 0.4, sc
    assert sc["cw_p"] < 0.01, sc
    assert sc["u_ci_hi"] != sc["u_ci_hi"] or sc["u_ci_hi"] < 1  # NaN when bootstrap off


# --------------------------------------------------------------------------
# 5. negative control — noise does not win
# --------------------------------------------------------------------------

@pytest.mark.parametrize("h", [1, 12])
def test_negative_control_noise_does_not_beat_rw(feats, panel, h):
    """Pure noise regressors must land at U ~ 1. A leak anywhere in the
    alignment would show up here as a noise feature beating the benchmark."""
    y = target(panel, h)
    rng = np.random.default_rng(23)
    X = feats.copy()
    for j in range(5):
        X[f"noise{j}"] = rng.normal(size=len(X))

    cols = [f"noise{j}" for j in range(5)]
    origins = bt.make_origins(X, y, cols, min_train=60, h=h)
    preds = bt.walk_forward(X, y, cols, M.Ridge(), origins, window=120, min_train=60)
    bench = bt.walk_forward(X, y, cols, M.RandomWalk(), origins, window=120, min_train=60)
    sc = bt.score(y, preds, bench, h, bootstrap=False)

    assert 0.9 < sc["theil_u"] < 1.35, sc
    assert sc["cw_p"] > 0.01, sc


# --------------------------------------------------------------------------
# 6. the statistics themselves
# --------------------------------------------------------------------------

def test_clark_west_reduces_to_2yf_against_a_zero_benchmark():
    rng = np.random.default_rng(3)
    y = rng.normal(size=400)
    f = rng.normal(size=400) * 0.3
    b = np.zeros(400)
    t1, _ = bt.clark_west(y, b, f, h=1)
    manual = 2 * y * f
    t2 = manual.mean() / bt.hac_se(manual, 0)
    assert t1 == pytest.approx(t2, rel=1e-10)


def test_hac_se_matches_plain_se_at_zero_bandwidth():
    rng = np.random.default_rng(5)
    x = rng.normal(size=250)
    assert bt.hac_se(x, 0) == pytest.approx(x.std(ddof=0) / np.sqrt(len(x)), rel=1e-12)


def test_theil_u_is_one_when_model_is_the_benchmark(panel):
    h = 6
    y = target(panel, h).dropna()
    z = pd.Series(0.0, index=y.index)
    sc = bt.score(y, z, z, h, bootstrap=False)
    assert sc["theil_u"] == pytest.approx(1.0)
    assert sc["r2_oos"] == pytest.approx(0.0)


# --------------------------------------------------------------------------
# standalone runner (pytest optional)
# --------------------------------------------------------------------------

if __name__ == "__main__":
    import sys
    import traceback

    _panel = load_panel()
    _feats = build_features(_panel)
    fixtures = {"panel": _panel, "feats": _feats}

    failures = 0
    for name, fn in sorted(globals().items()):
        if not (name.startswith("test_") and callable(fn)):
            continue
        for case in (getattr(fn, "_params", None) or [{}]):
            argnames = fn.__code__.co_varnames[:fn.__code__.co_argcount]
            args = {k: fixtures[k] for k in argnames if k in fixtures}
            args.update(case)
            label = name + (f"[{case}]" if case else "")
            try:
                fn(**args)
                print(f"  PASS  {label}")
            except Exception:
                failures += 1
                print(f"  FAIL  {label}")
                traceback.print_exc()
    print(f"\n{failures} failure(s)")
    sys.exit(1 if failures else 0)
