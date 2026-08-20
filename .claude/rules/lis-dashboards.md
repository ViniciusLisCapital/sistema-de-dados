# LIS Dashboards — Chart Interactivity

All self-contained HTML dashboards/reports in this project should give every chart free pan/zoom on both axes, not leave them as static images. This applies **dashboard-wide regardless of charting library** — both the Chart.js dashboards and the Plotly-based reports implement the same interaction model, each via its own library-appropriate mechanism (sections below).

## The interaction model (updated 2026-07, twice in one day)

- **Plain click-drag** on the chart body → **pans**, both axes, following the drag direction
- **Scroll wheel / trackpad pinch** → **zooms**, both axes, anchored at the cursor
- **Double-click** → resets both axes back to the full data range
- There is **no click-drag box-zoom gesture**

History, since this has flip-flopped twice — read this before changing it again:
1. **First version**: plain drag = box-zoom, shift+drag = pan (both axes). Reasonable, but an inversion of TradingView's actual gestures.
2. **Second version**, at explicit user request to match real TradingView: plain drag = pan (X only), scroll = zoom (X only), Y auto-fit to visible data via a hand-rolled function, no box-zoom.
3. **Current (third) version**, at explicit user follow-up ("apply this to the Y axis too" — they wanted full manual control over the price scale, same as most charting tools' free-pan/free-zoom default, not a Y axis locked to auto-fit): drag and scroll now move **both** axes directly, no lock on Y. This is simpler than version 2 for Chart.js (native `mode:'xy'` handles it all, no auxiliary function needed) but Plotly's reports keep a *narrowed* version of the auto-fit function — see below for why.

## Chart.js setup (4.x)

1. CDN script tags, in this order (after Chart.js, and after chartjs-plugin-datalabels if that's also used):

```html
<script src="https://cdnjs.cloudflare.com/ajax/libs/hammer.js/2.0.8/hammer.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/chartjs-plugin-zoom/2.2.0/chartjs-plugin-zoom.min.js"></script>
```

Hammer.js is technically optional (chartjs-plugin-zoom checks `if (Hammer)` before enabling touch/pinch), but include it anyway so trackpad/touch users get pinch-zoom too.

2. Register the plugin once, but **do NOT** set `Chart.defaults.plugins.zoom` — confirmed by direct Playwright A/B testing (2026-07-28, see `analytics/brasil/exchange_rate/CLAUDE.md`'s `ppp_dashboard_template.html` entry for the full investigation) that doing so silently breaks x-axis wheel-zoom/pan on every chart on the page: y still moves, x never does, REGARDLESS of whether each chart also sets its own `options.plugins.zoom` correctly on top of the default (Chart.defaults-only, and Chart.defaults + identical per-chart config together, are both broken the same way — `chart.options.plugins.zoom` on a live chart correctly SHOWS the right merged values when inspected in either case, the config just doesn't work). The only combination confirmed to actually work: never touch `Chart.defaults.plugins.zoom`, and set the full options object on **every chart's own** `options.plugins.zoom` at construction time instead, via one shared helper function so it isn't hand-copied per chart:

```js
Chart.register(ChartDataLabels, ChartZoom);  // ChartZoom is chartjs-plugin-zoom's UMD global name
// Do NOT also assign Chart.defaults.plugins.zoom here -- see above.
function zoomPluginOpts() {
  return {
    pan: { enabled: true, mode: 'xy' },
    zoom: {
      wheel: { enabled: true },
      pinch: { enabled: true },
      drag: { enabled: false },
      mode: 'xy',
    },
    limits: { x: { min: 'original', max: 'original' }, y: { min: 'original', max: 'original' } },
  };
}
// then, in every `new Chart(...)` call's options:
//   plugins: { ..., zoom: zoomPluginOpts() }
```

`zoomPluginOpts()` returns a fresh object per call (not a shared reference) — call it again for each chart rather than reusing one object across multiple charts. `mode:'xy'` on both `pan` and `zoom` is what makes drag/scroll move Y as well as X — Chart.js's own native handling covers this completely, no auxiliary "autofit" function needed on this side (unlike Plotly, below): a diagonal drag or a scroll-zoom already moves whichever axes the gesture implies, correctly, on its own.

A tempting-looking shortcut — a custom Chart.js plugin's `beforeInit(chart)` hook mutating `chart.options.plugins.zoom` after construction, to avoid touching every call site — was tried and **crashed** with "Maximum call stack size exceeded": Chart.js's `options` object is Proxy-based and isn't safe to write into after the fact this way. Don't retry that; call `zoomPluginOpts()` directly in each chart's own construction options instead.

**The x-axis also needs to not be a category scale.** Every line/bar chart built the normal way here (`data: { labels: [...], datasets: [{ data: [...] }] }`, no explicit `scales.x.type`) gets an *implicit* category x-axis from Chart.js — and chartjs-plugin-zoom does not reliably zoom/pan a category-type axis (matches long-standing upstream issues #360/#655/#90: category-axis wheel-zoom "barely works" or not at all; confirmed here too, empirically, both for the implicit case and for an explicit `type:'category'`). The fix: give the x-axis `type:'linear'` with explicit `min:0, max:labels.length-1`, and re-express each dataset's data as `{x: index, y: value}` pairs instead of a bare value array — a plain array is silently NOT plotted at all once the scale stops being category-type. A `ticks.callback` maps the numeric index back to its label string so the axis reads the same as before:

```js
function toXY(values) {
  return values.map((v, i) => ({ x: i, y: (v === undefined ? null : v) }));
}
function xAxis(labels, extra) {
  return Object.assign({ type: 'linear', min: 0, max: labels.length - 1 }, extra || {}, {
    ticks: Object.assign({}, (extra && extra.ticks) || {}, {
      callback: (v) => labels[Math.round(v)] != null ? labels[Math.round(v)] : '',
    }),
  });
}
// then: data: { labels, datasets: [{ data: toXY(values), ... }] }, scales: { x: xAxis(labels, { ...your grid/tick styling... }) }
```

This applies equally to stacked bar charts (an initial round of testing wrongly concluded bar charts couldn't zoom on x at all even with this fix — that testing still had the `Chart.defaults.plugins.zoom` bug present at the same time; once that was actually fixed, bar charts zoom/pan on x exactly like line charts, no separate limitation).

3. Add a global double-click-to-reset handler once (not per chart) — `Chart.getChart(canvas)` recovers the chart instance from any canvas element, so one delegated listener covers every chart on the page:

```js
document.addEventListener('dblclick', function (e) {
  if (e.target && e.target.tagName === 'CANVAS') {
    const chart = Chart.getChart(e.target);
    if (chart && typeof chart.resetZoom === 'function') chart.resetZoom();
  }
});
```

4. Add a one-line, dashboard-wide hint near the top of the page (not repeated per-chart) so the interaction is discoverable, e.g.:
"Every chart: scroll/pinch to zoom (both axes) · drag to pan (both axes) · double-click to reset"

### Why a shared helper function, not hand-copied config

Each of these dashboards' charts is its own `new Chart(...)` call spread across many tabs — often 15-30+ per dashboard, and growing every time a tab is added. Since the options must live on each chart's own `options.plugins.zoom` (see above — `Chart.defaults` doesn't work), the maintainable way to do that without copy-pasting a config block into every one of 15-30+ call sites is a single shared `zoomPluginOpts()` function (and `toXY()`/`xAxis()` for the x-axis fix) that every chart calls — a new chart, or a new tab added in a future session, just needs to call these same three helpers rather than needing its own hand-rolled config.

Applied to: `analytics/brasil/exchange_rate/models/ppp_dashboard_template.html` (the template) → regenerated into `reports/ppp_dashboard.html` (the output). **Both are gone since 2026-08** — that template's three tabs were fused into `analytics/brasil/exchange_rate/report.html`, so the charts described here now live in `reports/brasil/FX Report.html`, regenerated by `analytics.brasil.exchange_rate.generate_report.run()` — edit `analytics/brasil/exchange_rate/report.html`, never the generated output. The Chart.js configuration this section documents was already dead before the merge (nothing called `new Chart(` anymore) and the merge dropped the CDN tags with it — read the Chart.js half below as history that applies to the `lis-dashboard` skill's own recipe, not to this report. Verified with a real Playwright harness (not just `node --check`) across all 21 time-series charts in all 6 tabs: real wheel-zoom and click-drag-pan events fired against the actual generated file, confirming the visible x/y range actually changes — see `analytics/brasil/exchange_rate/CLAUDE.md` for the full before/after investigation. The `lis-dashboard` skill's own Chart.js zoom recipe (`.claude/skills/lis-dashboard/references/design-system.md`) has the same `Chart.defaults.plugins.zoom`-based pattern and is presumed to have the same bug, though not directly retested here — treat it as needing the same fix before trusting it.

## Plotly setup

Plotly ships its own zoom/pan/reset toolbar out of the box, but its *defaults* don't match this model (default `dragmode` is `'zoom'` — click-drag rubber-bands a box-zoom instead of panning). Two pieces, added to every report's shared layout factory (`mkLayout()` / `_nucLayout()` / `baseLayout()` depending on the file) so every chart gets them automatically:

1. **`scrollZoom: true`** in the chart config (not layout) — makes scroll/pinch zoom in place instead of scrolling the page. With no `fixedrange` set on any axis, this zooms both X and Y together, anchored at the cursor — matching Chart.js's `mode:'xy'` above.
2. **`dragmode: 'pan'`** in the layout, and **no `fixedrange`** on any axis (`yaxis`, `yaxis2` for dual-axis charts) — makes plain click-drag pan freely along both axes per the actual drag direction, instead of box-zooming.

That's it for direct user gestures — Plotly's own pan/scroll-zoom handling covers both axes correctly on its own, same as Chart.js's native `mode:'xy'`.

**Why `_bindYAutofit` still exists here and not on the Chart.js side**: these Plotly reports also have **quick-range preset buttons** ("3a"/"5a"/"10a"/"Tudo" etc.) that jump the visible X window directly, bypassing drag/scroll entirely — clicking one changes `xaxis.range` alone, with no accompanying user gesture on Y at all, so Y is left showing whatever range was visible before the click (often squeezing a newly-narrow window into a sliver of the old full-history range). `_bindYAutofit(divId)` — bound once per chart div, right after its `Plotly.react`/`Plotly.newPlot` call — patches exactly that gap: it listens for `plotly_relayout` events, and **only** recomputes Y when `xaxis.range` changed **without** `yaxis`/`yaxis2` also changing in that same event (i.e. a preset-button click or a double-click reset, never a direct drag or an xy scroll-zoom, which always change both axes together and must be left alone or they'd fight the user's own gesture). This reasoning holds regardless of *how* those preset buttons are implemented — native `xaxis.rangeselector` or plain HTML buttons calling `Plotly.relayout()` (see "Quick-range buttons" dated entry below for why the latter is now the standard) — both fire the same `plotly_relayout` event shape this function listens for. Generic across category x-axis (Plotly reports `xaxis.range` as fractional array indices there) vs. date x-axis (real values, compared via `Date.parse`), single/dual y-axis (grouped by each trace's own `yaxis` id), and plain vs. stacked (`barmode: 'stack'`/`'relative'`) bar traces — stacked axes always get 0 folded into their fitted range (a stacked bar's baseline is the zero line), plain line/bar axes autofit tightly with no forced zero:

```js
function _toComparableX(v) {
  return (typeof v === 'string' && /^\d{4}-\d{2}(-\d{2})?/.test(v)) ? Date.parse(v) : v;
}
function _bindYAutofit(divId) {
  var el = document.getElementById(divId);
  if (!el) return;
  var lock = false;
  el.on('plotly_relayout', function(ev) {
    if (lock) return;
    var xChanged = Object.keys(ev).some(function(k) { return k.indexOf('xaxis.range') === 0 || k.indexOf('xaxis.autorange') === 0; });
    var yChanged = Object.keys(ev).some(function(k) { return /^yaxis\d*\.(range|autorange)/.test(k); });
    if (!xChanged || yChanged) return;
    // _fullLayout first, not layout: it's Plotly's fully-resolved internal
    // state, guaranteed to have xaxis.type auto-detected (category vs date)
    // -- el.layout is the raw object passed to newPlot/react and may never
    // have had .type set at all when it wasn't specified explicitly.
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
```

Applied verbatim to `analytics/brasil/exchange_rate/report.html`, `analytics/brasil/inflation/report.html`, and `analytics/brasil/monetary_policy/report.html` — historically by hand copy-paste, since each report is self-contained with no shared JS module at *runtime*. **Since 2026-08**, `analytics/brasil/inflation/report.html` and `analytics/brasil/exchange_rate/report.html` no longer carry their own inline copy: both have a `/*Y_AUTOFIT_JS*/` marker, filled in at generation time from `analytics/report_structure/y_autofit.js` (see [`analytics/report_structure/CLAUDE.md`](../../analytics/report_structure/CLAUDE.md)) — the *shipped* HTML still ends up with this function embedded verbatim, only the source-of-truth for edits moved. That shared file's guard clause was widened to `!t.x || !t.y || t.type === 'heatmap'` to match `exchange_rate`'s version (needed for its BOP heatmap panels; a no-op for `inflation`, which never binds `_bindYAutofit` to a heatmap trace). `monetary_policy/report.html` carried its own hand-copied inline version and was never migrated; the file was **deleted in 2026-08** along with the BCB-model replication it belonged to, so only the two reports above remain in scope here. Excluded on purpose: any chart that isn't a time series along X — `analytics/brasil/inflation/report.html`'s `chart-waterfall` (vertical category-ranking bars, x=category/y=value — flipped from horizontal to vertical 2026-08 at direct user request) and `chart-scatter-momentum` (both axes are plain % values, no category or time axis at all) and `analytics/brasil/exchange_rate/report.html`'s BOP z-score heatmap panels (`renderHeatmapPanel`, x=date but y=fixed category rows, not a value axis) keep Plotly's own default interaction instead.

## Verification approach (no browser available in this environment)

`_bindYAutofit`'s core min/max-over-visible-range logic was unit-tested against synthetic/mock objects (category vs. date axes, single vs. dual y-axis, plain vs. stacked bars) before being embedded in any report, then re-verified by actually executing each Plotly report's real generated `<script>` against a stubbed `document`/`Plotly` and firing synthetic `plotly_relayout` events against the *real* embedded data — both the "X-only changed → autofit fires" case and the "X and Y changed together → autofit stays out of the way" case, across all three reports including the dual-axis (`chart-timeseries`, `chart-cot-brl`) and category-axis (`monetary_policy`) charts. This caught one real bug before it shipped: `el.layout || el._fullLayout` has the precedence backwards for reading the auto-detected `xaxis.type` — Plotly only resolves that onto `_fullLayout`, never back onto the raw `layout` object — fixed to `el._fullLayout || el.layout` everywhere. The Chart.js side has no auxiliary function left to test (native `mode:'xy'` handles everything) — its zoom/pan config was checked for syntax validity only. **Actual browser rendering of any of this has still not been visually confirmed** — do that before fully trusting the feel of the interaction.

## Related conventions

Brand colors/typography are a separate concern from this rule — see the `project-lis-brand-colors` memory and each dashboard's own `:root` CSS variables.

## Promoted to the `lis-dashboard` skill

User visually confirmed the interaction in a real browser and it's correct. The Chart.js half of this setup (CDN tags, `Chart.defaults.plugins.zoom` config, double-click handler, discoverability hint) was originally baked into `.claude/skills/lis-dashboard/references/design-system.md` (§10, "JS — Zoom/Pan Interativo") and `.claude/skills/lis-dashboard/SKILL.md`'s Chart.js rules + output-structure lists, so every *new* dashboard the skill generated got this by default. The Plotly `_bindYAutofit` half stayed here only at the time, since that skill was Chart.js-only.

**Superseded 2026-07-28, same day, later that day**: the skill itself moved off Chart.js entirely, onto Plotly — direct user request after converting `analytics/brasil/exchange_rate/referencia/ppp_dashboard.html`'s Chart.js charts to Plotly one at a time and liking the result better ("I want all graphs to be this way ... set this in skill too"). `.claude/skills/lis-dashboard/references/design-system.md` and `SKILL.md` were rewritten so every future dashboard the skill generates uses the exact same Plotly convention already established here (`dragmode:'pan'`, `scrollZoom:true`, `rangeselector`, the generic `_bindYAutofit`) — the design-system.md's own JS section is now the canonical copy-paste source for new skill-built dashboards, not a Chart.js-specific variant of it. This section's "Chart.js half"/"Plotly half stays here only" framing is accordingly obsolete: there is now one Plotly convention shared by the three analytics reports, `ppp_dashboard.html` (since 2026-08 three tabs of `reports/brasil/FX Report.html`, not its own file), and the skill — not two parallel conventions split by codebase. Kept here as history, not corrected in place, since the point of this file is documenting how the interaction model evolved.

## Quick-range buttons: native `xaxis.rangeselector` replaced by plain HTML + `Plotly.relayout()` (2026-08)

The "3a"/"5a"/"10a"/"Tudo" quick-range buttons above were, at the time the previous section was
written, Plotly's own native `layout.xaxis.rangeselector.buttons[]` component. That component broke
in production twice while building `analytics/brasil/economic_activity/report.html`'s PIB tab (full
before/after detail in that report's own `analytics/brasil/economic_activity/CLAUDE.md`, "Chart interaction
and KPI fixes"/"Sixth round" sections):

1. Even used correctly (`step`/`stepmode`/`count`, the documented fields), a `stepmode:'backward'`
   button computes its `to` anchor from the axis's *current* range — which, on a fresh view with
   `autorange` still on, is Plotly's own auto-padded full-data range, not the true last data point.
   On a chart with a long history, that padding is small as a percentage but large in absolute
   terms, so a "3a" click opened a window with a wall of empty months/years past the last real bar.
2. An attempted fix wrongly assumed `rangeselector.buttons[]` accepted an `updatemenus`-style
   `{method:'relayout', args:[...]}` button definition to bake in an exact `[from,to]` range. It does
   not — that field doesn't exist in the rangeselector button spec (only `step`/`stepmode`/`count`/
   `label`/`name`/`visible`/`templateitemname`) — Plotly silently ignores it, and the resulting click
   produced a blank chart with the x-axis collapsed to a few weeks near the render date.

Both failures trace to the same root cause: relying on `xaxis.rangeselector`'s internal behavior
instead of computing the range yourself. **Current standard**: plain HTML `<button>` elements (styled
as pills) whose click handler calls `Plotly.relayout(divId, {'xaxis.range': [from, to]})` directly,
with `[from, to]` computed from the chart's own real trace data (never from the axis's current
range). This is a real, documented, top-level Plotly API call, not an internal component's
undocumented click-dispatch — there is no more Plotly-internal behavior this pattern depends on and
cannot verify with a jsdom-without-real-Plotly harness (which is exactly what let both failures above
ship undetected — every test up to that point asserted on the button *definition object*, never on
what real Plotly does when that definition is clicked). User confirmed the resulting buttons "much
better" in a real browser and asked for this to become the standard.

Promoted into `.claude/skills/lis-dashboard/references/design-system.md` (`quickRangeOptions()`/
`renderQuickRangeButtons()`, replacing the old `RANGE_SELECTOR` const) and `SKILL.md` — every
*future* dashboard the skill generates uses this pattern from the start, same promotion mechanism as
the Chart.js→Plotly switch above. `_bindYAutofit`'s own rationale is unaffected (see the amended note
above) — it reacts to the `plotly_relayout` event either implementation produces. Not retrofitted
into `analytics/brasil/exchange_rate/report.html` or `analytics/brasil/inflation/report.html` — both
still carry the native `xaxis.rangeselector` from before this fix and have not been reported as
broken, but should be treated as carrying the same latent bug until migrated (point 1 above
applies to native step/stepmode/count buttons generally, regardless of whether point 2's invalid
method/args form was ever added to them). A third report used to be in this list,
`analytics/brasil/monetary_policy/report.html`, deleted in 2026-08.
