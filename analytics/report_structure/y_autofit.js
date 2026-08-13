// ── Y-axis autofit to visible X range, on pan/zoom/reset ──────────────────────
// Generic across every chart shape in this report: category or date x-axis
// (Plotly reports xaxis.range as fractional array indices for category axes,
// real values for date ones — handled via `isCat`), single or dual y-axis
// (grouped by each trace's own `yaxis` id), and plain vs. stacked bars
// (barmode 'stack'/'relative' sums same-axis bar traces per x-bucket by sign
// before taking min/max, and always anchors that axis at 0, since a stacked
// bar's baseline is always the zero line — pure line/scatter axes autofit
// tightly to whatever's actually visible, no forced zero, matching
// TradingView's own price-axis behavior). Y is user-pannable/zoomable
// directly too (no fixedrange, dragmode:'pan' moves both axes per the
// user's actual drag/scroll) — this function only fires when X changed
// WITHOUT Y also changing in the same relayout event, i.e. exactly the
// rangeselector preset buttons (3a/5a/10a/Tudo etc.), which only ever touch
// xaxis. A direct diagonal drag or an xy scroll-zoom changes both axes in
// one event and is deliberately left alone here, since overriding it would
// fight the user's own gesture. Skips 'heatmap' traces entirely (a chart div
// that mixes a heatmap trace with value-axis traces would otherwise have the
// heatmap's z-values pollute the min/max scan — no report currently binds
// _bindYAutofit to a heatmap-only div at all, so this is a defensive no-op
// for those, not exercised behavior). Verified in isolation against
// synthetic data (scratchpad/test_yautofit.js) since this environment has no
// browser to test the real Plotly wiring in.
function _toComparableX(v) {
  return (typeof v === 'string' && /^\d{4}-\d{2}(-\d{2})?/.test(v)) ? Date.parse(v) : v;
}
function _bindYAutofit(divId) {
  var el = document.getElementById(divId);
  // Idempotent per div: a report that re-renders the same div via Plotly.react on every filter/
  // control change (e.g. economic_activity's PIB tab checkbox dropdowns) calls this again on every
  // re-render. Without the guard, el.on() adds one more listener each time -- after N re-renders,
  // N redundant relayout listeners all fire (and each schedule their own Plotly.relayout) on every
  // single rangeselector click or preserved-range redraw. The listener itself is stateless (reads
  // el.data/_fullLayout live at event time), so binding it once per div's lifetime is correct.
  if (!el || el._yAutofitBound) return;
  el._yAutofitBound = true;
  var lock = false;
  el.on('plotly_relayout', function(ev) {
    if (lock) return;
    var xChanged = Object.keys(ev).some(function(k) { return k.indexOf('xaxis.range') === 0 || k.indexOf('xaxis.autorange') === 0; });
    var yChanged = Object.keys(ev).some(function(k) { return /^yaxis\d*\.(range|autorange)/.test(k); });
    if (!xChanged || yChanged) return;
    // _fullLayout first, not layout: it's Plotly's fully-resolved internal
    // state, guaranteed to have xaxis.type auto-detected (category vs date)
    // -- el.layout is the raw object passed to newPlot/react and may never
    // have had .type set at all when it wasn't specified explicitly. Caught
    // by a runtime harness test against real category-axis data (see
    // CLAUDE.md's Gotchas), not assumed.
    var layout = el._fullLayout || el.layout;
    if (!layout || !layout.xaxis || !layout.xaxis.range) return;
    var isCat = layout.xaxis.type === 'category';
    var stackedAxes = {};
    if (layout.barmode === 'stack' || layout.barmode === 'relative') {
      (el.data || []).forEach(function(t) { if (t.type === 'bar') stackedAxes[t.yaxis || 'y'] = true; });
    }
    var xr = layout.xaxis.range;
    var lo = isCat ? Math.round(xr[0]) : _toComparableX(xr[0]);
    var hi = isCat ? Math.round(xr[1]) : _toComparableX(xr[1]);
    var axes = {};
    (el.data || []).forEach(function(t) {
      if (!t.x || !t.y || t.type === 'heatmap') return;
      var axisId = t.yaxis || 'y';
      if (!axes[axisId]) axes[axisId] = { mn: Infinity, mx: -Infinity, byX: {} };
      var a = axes[axisId];
      var stackable = stackedAxes[axisId] && t.type === 'bar';
      for (var i = 0; i < t.x.length; i++) {
        var inRange = isCat ? (i >= lo && i <= hi) : (_toComparableX(t.x[i]) >= lo && _toComparableX(t.x[i]) <= hi);
        if (!inRange) continue;
        var v = t.y[i];
        if (v == null || isNaN(v)) continue;
        if (stackable) {
          var key = isCat ? i : t.x[i];
          if (!a.byX[key]) a.byX[key] = { pos: 0, neg: 0 };
          if (v >= 0) a.byX[key].pos += v; else a.byX[key].neg += v;
        } else {
          if (v < a.mn) a.mn = v;
          if (v > a.mx) a.mx = v;
        }
      }
    });
    var upd = {}, any = false;
    Object.keys(axes).forEach(function(axisId) {
      var a = axes[axisId], mn = a.mn, mx = a.mx;
      Object.keys(a.byX).forEach(function(k) {
        var b = a.byX[k];
        if (b.pos > mx) mx = b.pos;
        if (b.neg < mn) mn = b.neg;
      });
      if (Object.keys(a.byX).length) { mn = Math.min(mn, 0); mx = Math.max(mx, 0); }
      if (mn === Infinity || mx === -Infinity) return;
      var pad = Math.max((mx - mn) * 0.1, 0.5);
      var key = axisId === 'y' ? 'yaxis' : axisId.replace('y', 'yaxis');
      upd[key + '.range'] = [mn - pad, mx + pad];
      upd[key + '.autorange'] = false;
      any = true;
    });
    if (any) {
      lock = true;
      Plotly.relayout(divId, upd).then(function() { lock = false; }).catch(function() { lock = false; });
    }
  });
}
