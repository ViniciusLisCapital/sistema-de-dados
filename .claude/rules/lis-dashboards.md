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

Applied verbatim to `analytics/brasil/exchange_rate/report.html`, `analytics/brasil/inflation/report.html`, and `analytics/brasil/monetary_policy/report.html` — historically by hand copy-paste, since each report is self-contained with no shared JS module at *runtime*. **Since 2026-08**, `analytics/brasil/inflation/report.html` and `analytics/brasil/exchange_rate/report.html` no longer carry their own inline copy: both have a `/*Y_AUTOFIT_JS*/` marker, filled in at generation time from `analytics/report_structure/y_autofit.js` (see [`analytics/report_structure/CLAUDE.md`](../../analytics/report_structure/CLAUDE.md)) — the *shipped* HTML still ends up with this function embedded verbatim, only the source-of-truth for edits moved. That shared file's guard clause was widened to `!t.x || !t.y || t.type === 'heatmap'` to match `exchange_rate`'s version, which then needed it for its BOP heatmap panels. **Those panels are gone since 2026-08-27** (the user asked for the whole Mapa de Calor tab to be removed), so the guard is now a defensive no-op in both reports — kept, not reverted, since the reasoning behind it is the reusable part. `monetary_policy/report.html` carried its own hand-copied inline version and was never migrated; the file was **deleted in 2026-08** along with the BCB-model replication it belonged to, so only the two reports above remain in scope here. Excluded on purpose: any chart that isn't a time series along X — `analytics/brasil/inflation/report.html`'s `chart-waterfall` (vertical category-ranking bars, x=category/y=value — flipped from horizontal to vertical 2026-08 at direct user request) and `chart-scatter-momentum` (both axes are plain % values, no category or time axis at all) keep Plotly's own default interaction instead. `analytics/brasil/exchange_rate/report.html`'s BOP z-score heatmap panels (`renderHeatmapPanel`, x=date but y=fixed category rows, not a value axis) used to be the third case here; that tab was removed in 2026-08-27.

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

### The "All" button is the same trap wearing a third face (2026-08-26)

Found in `analytics/us/inflation/report.html`, which had been on the HTML-buttons pattern from the
start and was therefore *not* in the list above — its five range buttons all computed `[from, to]`
from real data, exactly as prescribed. All except the last: **"All" called
`Plotly.relayout(div, {'xaxis.autorange': true})`**, which reads as the obvious way to say "show
everything" and is not.

`autorange` does not return the data's own extent. It returns the extent **plus Plotly's automatic
padding**, a percentage of the total span — the same padding that made point 1 above open a window
with empty months after the last real bar. On a chart whose x-axis starts in 1913, a few percent of
113 years is a visibly empty band of years hanging off the right edge, which on a monthly series
reads as missing data rather than as margin.

So the rule is not "don't use `stepmode`" — it is **the button must send a range you computed from
the traces' own values, every button, including the one that means everything**. `All` now sends
`[dates[0], dates[dates.length - 1]]` like the rest. `_bindYAutofit` is unaffected: it fires on
`xaxis.range*` and `xaxis.autorange*` alike, so it was doing its job in both versions — which is
precisely why the padding never surfaced as a Y-axis symptom and went unnoticed.

Worth checking wherever a "Tudo"/"All"/"Max" button exists, including
`.claude/skills/lis-dashboard/references/design-system.md`'s own `quickRangeOptions()` — that one is
already correct (it returns `{from: loISO, to: hiISO}` from the real array), so this is a note about
hand-written implementations drifting from it, not a defect in the reference.

### The buttons go BELOW the chart (2026-08-27)

Direct user request while reviewing `analytics/brasil/labor_market/report.html`: "coloque o seletor de
range de data na parte debaixo do grafico; aplique em todos os graficos". The time ruler belongs at the
foot of the chart, next to the X axis it controls — and the native `xaxis.rangeselector` can only draw
it *above*, which is one more reason the HTML-button pattern above is the standard rather than a
workaround.

`analytics/brasil/labor_market/report.html` is the first report migrated: its 17 charts (12 PNAD + 5
CAGED) dropped `xaxis.rangeselector` entirely for a `.range-bar` div rendered inside the same
`.chart-card`, after the chart div, by `renderRangeBar(barId, divId, specsFn, activeIdx)`. Every button
including "Tudo" sends a `[from, to]` computed from the plotted traces' own values (`_dataExtent()`),
per the two notes above. `_bindYAutofit` is unaffected — it reacts to the `plotly_relayout` this
produces exactly as it did to the native buttons'. Promoted into the skill's `design-system.md`
(`renderQuickRangeButtons()`'s comment, a `.range-pills` container placed after the chart in the Chart
Container markup, its CSS, and the delivery checklist). `exchange_rate/report.html`'s six
**data** tabs migrated 2026-08-27 (see the next section — the latent bug surfaced for real there);
`inflation/report.html` and `exchange_rate`'s three **model** tabs still keep the native selector
above the chart.

### The latent bug is not latent: measured, in production (2026-08-27)

The user reported charts in `reports/brasil/FX Report.html` opening with a wide empty band on the
right after clicking "10a". This is exactly point 1 of the section above, now with numbers.

The BOP series runs 1995-01 → 2026-07 — **31.5 years**. Plotly's autorange padding is a fraction of
that span, so on first paint `xaxis.range[1]` sits well past the last month: in the screenshot the
user sent, the axis of a chart whose data stops at 2026-07 runs past 2028. A `stepmode:'backward'`
button reads that inflated value as its `to` anchor, so the ten-year window it opens is shifted
forward by the same amount and its right ~2 years are blank. (The screenshot is the measurement here
— there is no browser in this environment to instrument Plotly's padding directly.) The effect scales
with total history, which is why it is invisible on a chart with a short one and glaring on this
report — "acontece em vários gráficos" was the user's own description, and it was in fact every chart
on the tab, since they all shared `mkLayout()`.

Two things worth carrying forward from the fix:

- **The right edge needs padding derived from the data, not zero and not Plotly's.** Bars and heatmap
  cells are centered on their x value, so a window ending exactly at the last point cuts the last bar
  in half. `_ensureRangeBar()` pads by **half the distance between the last two points of the plotted
  series** — 15 days on a monthly series, ~45 on a quarterly one. Same idea as autorange's padding,
  except it comes from the series' own spacing instead of a percentage of the span.
- **The date strings are timezone-naive, and `Date.parse` is not.** `"YYYY-MM-DD HH:mm:ss"` is
  Plotly's canonical form and Plotly reads it as UTC, but JavaScript's `Date.parse` reads
  *date-with-time and no offset* as **local time** (only the bare `"YYYY-MM-DD"` form is UTC). Mixing
  the two in a test produces a phantom offset of exactly the machine's timezone — three hours here,
  which looked like a real overshoot until it was traced. Compare both sides with the same rule.

Covered by `tests/test_fx_report_js.js` (94 assertions), which asserts on the `[from, to]` each button
produces and on the window a real click applies — not on the button definition, which is what let the
earlier rounds ship.

### Fourth face: the view nobody clicks for — the first paint (2026-08-27)

The three faces above are all about *buttons*. The window a chart opens with is not produced by any
button, so every fix so far left it on Plotly's `autorange` — and `autorange` is the very thing all
three faces were about. Reported by the user against `reports/brasil/FX Report.html`: a chart whose
data starts in **2008-09** opened with its axis starting in **1982**, 26.6 years of empty space, the
line squeezed into the right third of the plot.

The mechanism is a hair different from the earlier faces and that difference is the lesson.
`autorange` does not range over the *values*; it ranges over the **x array**, and a point whose `y` is
`null` still has an `x`. So a series that is null for its first 320 months still pushes the axis back
320 months. This matters wherever several series of different vintages share one date grid — here, one
tab's payload carries both a 1982-start series (BCB Tabela 14) and a 2008-start one (Tabela 13), so
plotting only the second one drags in the first one's history as blank space.

Two rules come out of it, and they generalize past this report:

- **A chart's initial window is a range you compute, exactly like a button's.** Not `autorange`, not
  omission. The fix was one line in the shared post-plot hook: with no range remembered, apply the
  same `[from, to]` the "All" button would send, and mark that pill active — which is honest, since
  that *is* the view.
- **Derive the extent from what the chart actually holds, not from what the caller passes.** Every
  call site here passed its own `dates` array, and each one was the payload's full grid, not the
  plotted series. Reading `gd.data` inside the hook instead means a chart added next year cannot
  forget. Watch the trace shape when you do: in a **heatmap** the `y` is the row *labels*, not values,
  so a "does column i have data?" test must look at `z` before `y` or it reports the first N columns
  as populated, N = number of categories.

Covered by `tests/test_fx_report_js.js` §2b, which snapshots the window each chart applies on first
paint — before the test itself clicks anything — and requires it to sit within half a step of the
plotted data at both ends, for all 21 charts. Verified to fail on the pre-fix file.

## A hierarchical table that holds a STOCK needs a different aggregator (2026-08-27)

The tree-table factory in `analytics/brasil/exchange_rate/report.html` was written for flows, so its
period selector runs everything through a **sum**. Point it at a stock — reserves, a position, a debt
balance — and "Quarterly" silently returns three months added together. On Brazil's reserves that is
~1,100 USD Bi, which is wrong by 3× and still looks like a plausible reserves chart to anyone who
doesn't read the axis. No exception, no gap, no visual tell.

Two rules, both of which generalize to any dashboard that lets the user re-bucket a series:

- **The aggregator is a property of the data, not of the control.** A period `<select>` labelled
  Monthly/Quarterly/Annual means "sum" for a flow and "value at the end of the period" for a stock,
  and the same widget cannot mean both. Carry it as a flag on the series/tab (`stat: 'last'` here)
  and let the incomplete-bucket rule apply to both — a year labelled "2026" carrying July's balance
  reads as a year-end and isn't one. Take the value at the bucket's **last position, assigned
  unconditionally**, not the last non-null: if the closing month has no data, the honest answer is
  blank, not the previous month wearing the closing month's date. And drop the "12m trailing" option
  entirely — accumulating a stock produces no quantity at all.
- **A "% of GDP" toggle changes denominator with it.** The flow convention is numerator and
  denominator summed over the *same* window. A stock has no "quarter's GDP" to match: divide it by
  one month's GDP and you get ~1,700%, and the number changes scale every time the user touches the
  aggregation selector. Build the ratio on the monthly grid against **trailing-12m** GDP and aggregate
  the ratio afterwards. The assertion worth writing is not the magnitude — it's that the value does
  **not** move when the period selector does.

Related, from the same round and equally reusable: **check whether the ETL drops zeros before
deciding what a missing row means.** `domain/db/brasil/bcb/cmb_reservas_bc.py` deliberately discards
zero rows from the BCB's four intervention series, so an absent day inside the publication window is
a real zero, not missing data — propagating null would have opened a six-year hole in 2013-2018 that
reads as "no data" where the truth is "did not intervene". It also means the series' own `max(date)`
is **not** the publication window: 2023 has no spot-intervention row at all, and ending the series
there would hide months of zeros that are themselves the finding. Take the window from a neighbouring
series in the same table that isn't zero-filtered.

## "It isn't a hierarchy" is not a reason to skip the table (2026-08-27)

Direct user request, on a chart that had been left as a bare chart precisely because its four series
don't nest: *"mesmo que não tenha hierarquia, você pode colocar uma tabela, pois isso ajuda, assim
como as tags de explicação."*

They're right, and the reason generalizes: **most of what a tree-table gives you has nothing to do
with the tree.** Month-by-month cells next to the chart, a checkbox that picks what gets plotted, a
colour swatch tying row to legend, a definition card per row, the chart header, the range ruler —
none of that needs a parent-child relation. Only three things do: the indent, the expand caret, and
the "a checked row with checked descendants becomes a line" rule.

So run the flat case through the same factory with a one-level tree, and **turn off the three
controls that don't apply** instead of dropping the table. Two of those are cosmetic; the third is
not. With no parent, nothing ever becomes a line by the total-over-stack rule, so a factory that
defaults to stacked bars will happily stack series that **do not sum to anything** — here, three
central-bank exposures the source publishes no total for plus one belonging to a different entity.
That isn't a visualization preference, it's a fabricated aggregate. Give the factory an explicit
`defaultKind: 'lines'` for flat tables and don't render the type selector at all.

## Long row labels: short name + a definition card (2026-08-27)

Same review again: "algumas linhas poderiam ter um nome mais simples com um card descritivo quando
passa o mouse por cima ... um botão que você clica e consegue ver a definição e explicações, assim não
precisa escrever tudo na linha e deixar a tabela deformada."

The pattern, as built in `analytics/brasil/labor_market/report.html`: a row's label is the **short**
name; the source's official variable name (`full`) and a short explanation (`desc`) are separate
fields on the node, and a row that has either gets a 14 px `i` button after the label. Hover opens the
card, click pins it (so the text can be read and selected), click-away or Esc closes.

Four things that make it worth copying rather than re-deriving:

- **One `.info-pop` in the document**, repositioned on each open — not one popover per row. 52 rows
  have cards across 17 tables; a node per row would be DOM that is almost never seen.
- **`full` is attached only when it differs from the displayed label**, so the card never opens just to
  repeat the row back at the reader.
- **The card's last line reuses the same `def` field the Y axis uses**, so the unit shown in the card
  and the unit on the axis cannot drift apart.
- **The short label is what the chart legend gets too.** That was half the motivation — a name like
  "Taxa Combinada (Desocupação + Subocupação por Insuficiência de Horas)" wrecks the legend as badly as
  it wrecks the table column.

Positioning has to survive the table's own horizontal scroll: the card clamps to the viewport on the
right and flips above the button when it would fall off the bottom.

**Promoted into the skill** at user request (2026-08-27):
`.claude/skills/lis-dashboard/references/design-system.md` gained a "Botão de informação + card de
definição" section with `attachInfo()`/`showInfo()` and the CSS, plus rules in `SKILL.md` and the
delivery checklist. The skill's version hangs the button on whatever shows a short label — a series
toggle, a stat-card label, a chart title — since those dashboards have no hierarchical row table; the
four decisions above are what carried over.

**Second report, and two things the port changed (2026-08-27)**: `analytics/brasil/exchange_rate/report.html`,
all 7 hierarchical tables (BOP, 3 Comex cuts, 3 Fluxo Cambial sections). Both changes are worth
carrying into any third port.

- **The content lives outside the tree**, in a `NODE_INFO` map keyed by node key, not as fields on
  each node literal. In `labor_market` the rows are a flat-ish spec list and inline fields read fine;
  a four-level BOP tree with three paragraphs inside every literal stops being readable *as a
  hierarchy*, which is the one thing that source has to show at a glance. Generated nodes (the Comex
  cuts, built by a factory) still take `info` inline, since their keys are prefixed per cut.
- **The unit line is a function, not a string.** `labor_market`'s unit is fixed per row, so reusing
  the row's own `def` was enough. Here the same row is USD bilhões or % do PIB, monthly or annual,
  depending on two `<select>`s — so the card calls the tab's `unitLine()`, which builds the same
  (unit, window) pair the Y axis and the chart header show. A fixed string would start lying on the
  first click. A `unitNoun` option covers the table that isn't a flow at all: the interbank tab is
  *volume negociado*, and calling it flow would suggest direction where there is none.

The two rules from the original hold and are now tested (`tests/test_fx_report_js.js` §12): a row with
neither `full` nor `desc` gets no button, and `full` is attached only when it differs from the label.

**Third report, and the one rule the first two were missing (2026-08-27)**:
`analytics/brasil/expectations/report.html`, all 28 rows of the Boletim table plus the chart title. It
follows `exchange_rate`'s two changes (content in a `NODE_INFO`-style map outside the tree; the unit
line is a function, here a `{ano}` template resolved against the year pill so the card and the Y axis
can't drift). What it adds: **the card's provenance line is derived from the payload, not written in
the prose.** "Na pesquisa desde mar/2003" comes from the smallest `i0` among that indicator's
reference periods — a date typed into the `desc` would keep reading 2003 forever, and this one is
recomputed every generation. Same instinct as "recalculate the subtitle on every render": anything in
a card that a future load could contradict should be read from the data, not from the string.

Also worth copying: the card is only as trustworthy as what it asserts. Two lines of these
definitions were **measured against the database before being written** — that the survey's annual
unemployment rate is end-of-period and not the year's average (0,2 p.p. vs 1,1 p.p. against the
realized PNAD), and that the trade-balance median is not the difference of the export and import
medians (3,4 US$ bi apart across 8.310 survey dates). Both read as obvious either way; only one of
each pair is true.

## Every chart carries its own header (2026-08-27)

"Se eu enviar o gráfico para alguém, a pessoa não fará a mínima ideia do que se passa, terá que ler os
eixos." A chart that can be screenshotted and sent has to explain itself: what it is, in what metric
and frequency, in what unit, from what source, over what period.

Three lines at the top of the chart card, **inside** it, above the plot — not the card's own section
heading, which a screenshot of the chart region won't include:

```
Taxa de Desocupação — Brasil
Mensal (trimestre móvel) · desocupados / força de trabalho, %
Fonte: IBGE, PNAD Contínua · mar/2012 a jul/2026
```

Rebuild it on every render, never as static markup: the moment a selector moves, a fixed caption is
lying. Only the title and the source are declared per chart; the rest is derived from what is actually
plotted — the checked series, the selected controls, the Y-axis unit, and the real extent of the data
(which is why the year-over-year view honestly starts a year later than the level view).

The trap worth knowing before writing one: **the same fact arrives by three routes** — the control's
option label, the series name and the axis title — and printing all three reads as noise ("Taxa de
Desocupação · Mensal · Taxa · desocupados / força de trabalho, %"). Two rules cut it down: skip an
option's label when the unit line already implies it (the level/"Taxa" option) or when the label is
already inside the axis title, and drop the series name when it is just the chart title again. Filter
each candidate fragment against the axis title before joining.

Applied to all 17 charts of `analytics/brasil/labor_market/report.html`, and **promoted into the
skill** at user request (2026-08-27, "coloque esse padrão de descrição no skill /lis-dashboard para ser
aplicado em todos os gráficos e do seletor também"):
`.claude/skills/lis-dashboard/references/design-system.md` gained a "Cabeçalho do gráfico" section with
`describeChart()`/`dataExtent()`, its Chart Container markup now wires the three lines to ids (subtitle
and source left empty in the HTML, since JS fills them), and both `SKILL.md` and the delivery checklist
carry the rule. The skill's dashboards drive the subtitle off their series toggles instead of a row
tree, but the pruning rules are identical.

## Chart axis titles say what the series measures (2026-08-27)

Same review, same report: "coloque as unidades no grafico. Por exemplo, a taxa de desocupação mede o
que? O percentual de desempregados vis a vis a força de trabalho — coloque algo como
(desocupados/força de trabalho, %) — use isso para todos os graficos ... Veja não é para escrever um
livro no grafico."

So a Y-axis title is a **short definition**, not a unit name: `desocupados / força de trabalho, %`,
never `%` or `Taxa (%)`. One line, axis-label length.

The load-bearing half is the second complaint from the same message: "nos graficos de ocupação e
desocupação, por exemplo, mesmo sendo uma variação % Y/Y, ainda aparece como nivel de 'mil pessoas'".
That was **the unit living inside the series label** (`"Pessoas Ocupadas (mil pessoas)"`) — a label
shows in the legend under every metric, so it lies as soon as the chart isn't showing levels. The fix
is structural, not a string edit:

- The unit is a **field on the data**, not text in the label — `unit` (short, for a table cell) and
  `def` (the definition, for the axis) in `pnad_tab.py`.
- The axis title is **derived from the selected metric plus the plotted series**: levels use the
  series' own `def`; a year-over-year view becomes `p.p. contra o mesmo período do ano anterior` (for
  series that are already ratios) or `% contra o mesmo período do ano anterior` (levels and R$).
- **Mixed units in one chart** (a rate and a level checked together) can't pick one: the axis says
  `unidades mistas — ver a unidade de cada linha na tabela`, and the table shows the short unit next to
  each row's label — but *only* when the table actually has more than one unit, since repeating "%" on
  every row of an all-percent table informs nothing the axis hasn't already said.

Two implementation notes, in case this is ported: the mechanism is `ymode` on the metric option (PNAD,
where the unit varies per row) vs. literal `ypart` strings concatenated across controls (CAGED, where
it's uniform per control and the axis should name the metric too — `admissões — pessoas, acum. 12
meses`). And the numerators/denominators that go in those strings were **reconstructed from the
source's own level series and checked** rather than copied from documentation — which is how two of them
turned out to be wrong on the first pass (see the report's `pnad_tab.py` docstring). Promoted into
`design-system.md` as "Unidade no eixo Y".
