# Lis Capital — Design System Reference

Referência completa de CSS, componentes HTML e padrões de código para dashboards.

## Table of Contents

1. [CSS Base Completo](#css-base)
2. [HTML — Header](#header)
3. [HTML — Stats Cards](#stats-cards)
4. [HTML — Chart Container](#chart-container)
5. [HTML — Botão Dados no Gráfico](#dl-toggle)
6. [HTML — Filtros de Período](#filtros)
7. [HTML — Toggle de Séries](#toggle-series)
8. [HTML — Footer](#footer)
9. [JS — Plotly Setup](#chartjs-setup)
10. [JS — Zoom/Pan Interativo](#zoom-pan)
11. [JS — Datalabels (toggle de texto)](#datalabels)
12. [JS — Formatação BR](#formatacao)
13. [JS — Cores por variação](#cores)
14. [JS — Stats dinâmicos](#stats-dinamicos)
15. [Exemplo completo — Dashboard single-metric](#exemplo-single)
16. [Exemplo completo — Dashboard multi-metric](#exemplo-multi)

---

## CSS Base Completo <a name="css-base"></a>

```css
:root {
  --bg: #F4F5F7;
  --bg2: #FFFFFF;
  --navy: #1F2853;
  --ice: #1F2853;
  --ice2: #3A4F72;
  --gold: #BB9B1D;
  --muted: #7A88A8;
  --green: #418791;
  --red: #EA523A;
  --purple: #02739B;
  --line: rgba(31,40,83,0.1);
  --sans: 'Barlow', sans-serif;
  --cond: 'Barlow Condensed', sans-serif;
  --mono: 'JetBrains Mono', monospace;
}

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

body {
  font-family: var(--sans);
  background: var(--bg);
  color: var(--navy);
  font-size: 14px;
  line-height: 1.5;
  min-height: 100vh;
}

.page { margin: 0 auto; padding: 24px 32px; }

/* Header */
.hdr {
  background: var(--bg2);
  border: 1px solid var(--line);
  border-radius: 12px;
  padding: 16px 24px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 20px;
}
.hdr-logo { font-family: Georgia, serif; font-size: 22px; letter-spacing: 0.06em; color: var(--navy); }
.hdr-logo span { color: var(--gold); }
.hdr-center { font-family: var(--cond); font-size: 13px; font-weight: 600; letter-spacing: 0.2em; text-transform: uppercase; color: var(--ice2); }
.hdr-right { display: flex; align-items: center; gap: 12px; }
.hdr-date { font-family: var(--mono); font-size: 11px; color: var(--muted); }
.hdr-badge { font-family: var(--mono); font-size: 10px; padding: 4px 12px; border-radius: 100px; background: rgba(2,115,155,0.08); border: 1px solid rgba(2,115,155,0.25); color: var(--purple); }

/* Stats Cards */
.stats-row { display: grid; grid-template-columns: repeat(3, 1fr); gap: 12px; margin-bottom: 20px; }
.stat-card { background: var(--bg2); border: 1px solid var(--line); border-radius: 10px; padding: 14px 16px; }
.stat-label { font-family: var(--mono); font-size: 9px; letter-spacing: 0.12em; text-transform: uppercase; color: var(--muted); margin-bottom: 4px; }
.stat-val { font-family: var(--cond); font-size: 26px; font-weight: 600; color: var(--ice); line-height: 1; }
.stat-sub { font-size: 10px; color: var(--muted); margin-top: 3px; }
.up { color: var(--green) !important; }
.dn { color: var(--red) !important; }

/* Chart Container */
.chart-container { background: var(--bg2); border: 1px solid var(--line); border-radius: 12px; padding: 20px 24px; }
.chart-hdr { display: flex; align-items: center; justify-content: space-between; margin-bottom: 16px; flex-wrap: wrap; gap: 10px; }
.chart-hdr-left { display: flex; flex-direction: column; gap: 2px; }
.chart-title { font-family: var(--cond); font-size: 18px; font-weight: 700; letter-spacing: 0.08em; text-transform: uppercase; color: var(--ice); }
.chart-subtitle { font-family: var(--mono); font-size: 10px; color: var(--muted); }
.chart-hdr-right { display: flex; align-items: center; gap: 10px; flex-wrap: wrap; }
.chart-wrap { position: relative; height: 480px; }

/* Botão Dados no Gráfico */
.dl-toggle {
  font-family: var(--mono); font-size: 10px; letter-spacing: 0.06em;
  padding: 6px 16px; border-radius: 8px; cursor: pointer;
  border: 2px solid rgba(2,115,155,0.4); background: rgba(2,115,155,0.06);
  color: var(--purple); transition: all 0.2s; user-select: none;
  display: flex; align-items: center; gap: 7px;
}
.dl-toggle:hover { border-color: rgba(2,115,155,0.7); background: rgba(2,115,155,0.1); }
.dl-toggle.on { background: rgba(2,115,155,0.18); border-color: rgba(2,115,155,0.7); color: #025E82; font-weight: 600; }
.dl-toggle .toggle-icon {
  width: 14px; height: 14px; border-radius: 4px;
  border: 2px solid currentColor;
  display: flex; align-items: center; justify-content: center;
  font-size: 9px; line-height: 1;
}
.dl-toggle.on .toggle-icon { background: var(--purple); color: #fff; }

/* Filtros de Período */
.month-bar { display: flex; gap: 6px; flex-wrap: wrap; }
.month-btn {
  font-family: var(--mono); font-size: 10px; letter-spacing: 0.08em;
  padding: 5px 14px; border-radius: 6px; cursor: pointer;
  border: 1px solid rgba(31,40,83,0.12); background: rgba(31,40,83,0.03);
  color: var(--muted); transition: all 0.15s;
}
.month-btn:hover { color: var(--ice); border-color: rgba(31,40,83,0.3); }
.month-btn.active { background: rgba(187,155,29,0.15); border-color: rgba(187,155,29,0.5); color: var(--gold); }

/* Toggle de Séries (multi-variável) */
.controls {
  background: var(--bg2); border: 1px solid var(--line); border-radius: 12px;
  padding: 16px 24px; margin-bottom: 20px;
  display: flex; align-items: center; gap: 20px; flex-wrap: wrap;
}
.ctrl-label { font-family: var(--mono); font-size: 9px; letter-spacing: 0.12em; text-transform: uppercase; color: var(--muted); }
.toggle-group { display: flex; gap: 8px; }
.toggle-btn {
  font-family: var(--mono); font-size: 11px; letter-spacing: 0.06em;
  padding: 8px 18px; border-radius: 8px; cursor: pointer;
  border: 2px solid; transition: all 0.2s; user-select: none;
  display: flex; align-items: center; gap: 8px;
}
.toggle-btn .indicator { width: 10px; height: 10px; border-radius: 3px; transition: all 0.2s; }
.toggle-btn.off { opacity: 0.3; }
.sep { width: 1px; height: 32px; background: var(--line); }

/* Cores padrão para séries */
.t-primary { color: var(--navy); border-color: rgba(31,40,83,0.5); background: rgba(31,40,83,0.06); }
.t-primary .indicator { background: var(--navy); }
.t-secondary { color: var(--purple); border-color: rgba(2,115,155,0.5); background: rgba(2,115,155,0.06); }
.t-secondary .indicator { background: var(--purple); }
.t-tertiary { color: var(--gold); border-color: rgba(187,155,29,0.5); background: rgba(187,155,29,0.06); }
.t-tertiary .indicator { background: var(--gold); }

/* Axis Legend */
.axis-legend { display: flex; gap: 20px; justify-content: center; margin-top: 10px; }
.axis-item { display: flex; align-items: center; gap: 6px; font-family: var(--mono); font-size: 10px; color: var(--muted); }
.axis-dot { width: 12px; height: 3px; border-radius: 2px; }

/* Footer */
.ftr { text-align: center; font-family: var(--mono); font-size: 10px; color: var(--muted); padding: 12px 0; }
```

---

## HTML Components <a name="header"></a>

### Header
```html
<div class="hdr">
  <div class="hdr-logo">LIS <span>CAPITAL</span></div>
  <div class="hdr-center">TÍTULO — SUBTÍTULO</div>
  <div class="hdr-right">
    <div class="hdr-badge">BADGE TEXT</div>
    <div class="hdr-date">DD/MM/YYYY</div>
  </div>
</div>
```

### Stats Cards <a name="stats-cards"></a>
```html
<div class="stats-row" id="statsRow">
  <div class="stat-card">
    <div class="stat-label">LABEL</div>
    <div class="stat-val">VALUE</div>
    <div class="stat-sub">DD/MM</div>
  </div>
  <div class="stat-card">
    <div class="stat-label">MÁXIMA</div>
    <div class="stat-val up">VALUE</div>
    <div class="stat-sub">DD/MM</div>
  </div>
  <div class="stat-card">
    <div class="stat-label">MÍNIMA</div>
    <div class="stat-val dn">VALUE</div>
    <div class="stat-sub">DD/MM</div>
  </div>
</div>
```

### Chart Container <a name="chart-container"></a>
```html
<div class="chart-container">
  <div class="chart-hdr">
    <div class="chart-hdr-left">
      <div class="chart-title">TÍTULO DO GRÁFICO</div>
      <div class="chart-subtitle">Descrição · contexto</div>
    </div>
    <div class="chart-hdr-right">
      <!-- filtros e/ou dl-toggle aqui -->
      <div class="dl-toggle" id="dlToggle" onclick="toggleLabels()">
        <span class="toggle-icon"></span> Dados no gráfico
      </div>
    </div>
  </div>
  <div class="chart-wrap"><div id="mainChart" style="width:100%"></div></div>
</div>
```

### Footer <a name="footer"></a>
```html
<div class="ftr">Lis Capital · ATIVO · FUNDO · PERÍODO</div>
```

---

## JavaScript Patterns <a name="chartjs-setup"></a>

Padrão único de charting do projeto desde 2026-07-28 (histórico completo da mudança em `.claude/rules/lis-dashboards.md`, repo principal): **Plotly**, não Chart.js. Todo relatório analítico do projeto (`analytics/exchange_rate/report.html`, `analytics/inflation/report.html`, `analytics/monetary_policy/report.html`) já usava Plotly desde o início; esta skill migrou para o mesmo padrão no mesmo dia em que `ppp_dashboard.html` (originalmente Chart.js; então em `analytics/exchange_rate/referencia/`, movido para o `reports/` de topo em 2026-08 por ser um deliverable gerado por código, não material de referência) foi convertido, a pedido direto do usuário ("I want all graphs to be this way ... set this in skill too"). Os padrões abaixo são os MESMOS já usados nesses relatórios — não uma variação nova.

### CDNs obrigatórios (no <head>)
```html
<link href="https://fonts.googleapis.com/css2?family=Barlow:wght@300;400;500;600;700&family=Barlow+Condensed:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<script src="https://cdn.plot.ly/plotly-2.35.2.min.js" charset="utf-8"></script>
```

Nada além disso — sem Chart.js, sem chartjs-plugin-datalabels, sem hammer.js/chartjs-plugin-zoom. Cada `<div id="...">` vazio (não `<canvas>`) recebe seu gráfico via `Plotly.newPlot`/`Plotly.react`.

## JS — Zoom/Pan Interativo <a name="zoom-pan"></a>

**Obrigatório em todo dashboard** — nenhum gráfico fica estático. Interação livre nos dois eixos, mesmo padrão usado em `analytics/exchange_rate/report.html`/`analytics/inflation/report.html`/`analytics/monetary_policy/report.html` (histórico completo, incluindo as versões descartadas antes de chegar neste padrão, em `.claude/rules/lis-dashboards.md`):

- **Arrastar (drag)** → pan nos dois eixos diretamente (Plotly `dragmode:'pan'` nativo)
- **Scroll / pinch** → zoom nos dois eixos, ancorado no cursor (`scrollZoom:true`)
- **Double-click** → reseta para o range completo (comportamento nativo do Plotly, não precisa de handler)
- **Sem gesto de box-zoom** (o `dragmode:'pan'` do Plotly já substitui o `'zoom'` padrão da lib, que faria rubber-band box-zoom)
- **Botões de range rápido** (1a/3a/5a/10a/Tudo) — **botões HTML normais + `Plotly.relayout()` direto, NÃO o `xaxis.rangeselector` nativo do Plotly.** Ver caixa de atenção abaixo antes de implementar isso de outra forma.

> [!WARNING]
> **Não use `layout.xaxis.rangeselector` para os botões de range rápido.** Duas tentativas anteriores nesse próprio padrão quebraram em produção (`analytics/economic_activity/report.html`, 2026-08, histórico completo em `.claude/rules/lis-dashboards.md`):
> 1. `rangeselector.buttons[]` com `step`/`stepmode`/`count` (a forma "correta"/documentada) ainda assim ancora o `to` no range **atual** do eixo — que, se estiver com autorange ligado, é o range com o padding automático do próprio Plotly (uma % do span total, grande em termos absolutos quando o histórico é longo). Resultado: clicar em "3a" abre uma janela com meses/anos vazios depois do último ponto real.
> 2. Uma correção errada assumiu que `rangeselector.buttons[]` aceitava `{method:'relayout', args:[...]}` como os botões de `layout.updatemenus` — **não aceita**. Esse campo não existe na spec do rangeselector (só `step`/`stepmode`/`count`/`label`/`name`/`visible`). O Plotly ignora o campo silenciosamente e o clique produz um resultado sem sentido (gráfico em branco, eixo X reduzido a poucas semanas perto da data de renderização).
>
> A causa raiz dos dois problemas é a mesma: depender do comportamento interno do componente `rangeselector` em vez de calcular o range você mesmo. Botões HTML normais que chamam `Plotly.relayout(divId, {'xaxis.range': [from, to]})` diretamente evitam ambos de uma vez — você mesmo calcula `[from, to]` a partir dos dados reais, sem depender de nenhum estado interno do Plotly.

```javascript
// Config do Plotly (passar como 3º argumento de Plotly.newPlot/react)
const PLOTLY_CONFIG = {
  responsive: true,
  displayModeBar: 'hover',       // toolbar só aparece no hover, não compete com os botões de range
  displaylogo: false,
  modeBarButtonsToRemove: ['lasso2d', 'select2d', 'autoScale2d'],
  scrollZoom: true,              // scroll/pinch zoom in place, estilo TradingView
};

// Calcula [from, to] a partir dos dados REAIS do gráfico (não do range atual do eixo, que pode
// estar com padding do Plotly) -- `dates` = array ordenado de strings 'YYYY-MM-DD', ex. o próprio
// eixo X de uma das séries do gráfico.
function quickRangeOptions(dates) {
  if (!dates.length) return [];
  const hiISO = dates[dates.length - 1], loISO = dates[0];
  const hiMs = Date.parse(hiISO);
  function backISO(years) {
    const d = new Date(hiMs);
    d.setUTCFullYear(d.getUTCFullYear() - years);
    return d.toISOString().slice(0, 10);
  }
  return [
    { label: '1a',  from: backISO(1),  to: hiISO },
    { label: '3a',  from: backISO(3),  to: hiISO },
    { label: '5a',  from: backISO(5),  to: hiISO },
    { label: '10a', from: backISO(10), to: hiISO },
    { label: 'Tudo', from: loISO,      to: hiISO },
  ];
}
// containerEl: elemento vazio (ex. <div class="range-pills"></div>) posicionado acima do gráfico.
// Chamar de novo a cada re-render do gráfico (troca de filtro/série) -- é barato e mantém `dates`
// (portanto o "to" de cada botão) sempre correto mesmo que o range de dados mude.
function renderQuickRangeButtons(containerEl, divId, dates) {
  containerEl.innerHTML = '';
  quickRangeOptions(dates).forEach((opt) => {
    const btn = document.createElement('button');
    btn.type = 'button';
    btn.className = 'range-pill';
    btn.textContent = opt.label;
    btn.addEventListener('click', () => Plotly.relayout(divId, { 'xaxis.range': [opt.from, opt.to] }));
    containerEl.appendChild(btn);
  });
}

function mkLayout(extra) {
  const base = {
    dragmode: 'pan',              // nunca 'zoom' (rubber-band box) -- ver acima
    hovermode: 'x unified',
    hoverlabel: { bgcolor: '#1F2853', bordercolor: '#1F2853', font: { family: 'Barlow', size: 12, color: '#fff' } },
    showlegend: false,
    xaxis: {
      type: 'date',               // ou 'category' se o eixo X não for uma série temporal real
      showgrid: false, showline: true, linecolor: 'rgba(31,40,83,0.1)',
      tickfont: { family: 'JetBrains Mono', size: 10, color: '#7A88A8' },
      rangeslider: { visible: false },
      // NÃO setar `fixedrange` -- Y também precisa ficar pannable/zoomable livremente.
      // NÃO setar `rangeselector` -- ver caixa de atenção acima; os botões vivem fora do Plotly.
    },
    yaxis: {
      gridcolor: 'rgba(31,40,83,0.06)',
      tickfont: { family: 'JetBrains Mono', size: 10, color: '#7A88A8' },
    },
    paper_bgcolor: 'rgba(0,0,0,0)', plot_bgcolor: 'rgba(0,0,0,0)',
    font: { family: 'Barlow, sans-serif', color: '#1F2853', size: 12 },
  };
  if (!extra) return base;
  Object.keys(extra).forEach((k) => {
    if (k === 'xaxis' || k === 'yaxis') base[k] = Object.assign({}, base[k], extra[k]);
    else base[k] = extra[k];
  });
  return base;
}
```

CSS mínimo para `.range-pill` (mesma linguagem visual dos outros controles pill do design system):

```css
.range-pill {
  font-family: var(--mono, 'JetBrains Mono'); font-size: 11px; font-weight: 500; letter-spacing: 0.03em;
  padding: 4px 13px; border: 1px solid rgba(31,40,83,0.15); border-radius: 20px;
  background: rgba(31,40,83,0.03); color: #7A88A8; cursor: pointer; transition: all .15s;
}
.range-pill:hover { color: #1F2853; border-color: rgba(31,40,83,0.3); }
```

**Por que ainda precisa de um helper de autofit em Y, mesmo com `dragmode:'pan'`+Y livre:** os botões de range rápido (1a/3a/...) mudam `xaxis.range` diretamente, sem nenhum gesto de usuário em Y — então Y fica mostrando o range antigo (às vezes uma janela nova e estreita espremida no range antigo inteiro). `_bindYAutofit` cobre exatamente esse caso: só recalcula Y quando `xaxis.range` mudou **sem** `yaxis`/`yaxis2` também terem mudado no mesmo evento (ou seja, clique num botão de range rápido ou um double-click reset — nunca um drag/scroll direto, que já move os dois eixos juntos e não deve ser contrariado). Isso continua funcionando idêntico com os novos botões HTML: `Plotly.relayout()` dispara o mesmo evento `plotly_relayout` que os botões nativos disparavam. Versão genérica (funciona com eixo category ou date, single ou dual y-axis, barras simples ou empilhadas — mesma função usada nos três relatórios analíticos e em `ppp_dashboard.html`):

```javascript
function _toComparableX(v) {
  return (typeof v === 'string' && /^\d{4}-\d{2}(-\d{2})?/.test(v)) ? Date.parse(v) : v;
}
function _bindYAutofit(divId) {
  const el = document.getElementById(divId);
  if (!el || el._yAutofitBound) return;
  el._yAutofitBound = true;
  let lock = false;
  el.on('plotly_relayout', function (ev) {
    if (lock) return;
    const xChanged = Object.keys(ev).some((k) => k.indexOf('xaxis.range') === 0 || k.indexOf('xaxis.autorange') === 0);
    const yChanged = Object.keys(ev).some((k) => /^yaxis\d*\.(range|autorange)/.test(k));
    if (!xChanged || yChanged) return;
    // _fullLayout primeiro, não layout: só ali o Plotly resolve o xaxis.type
    // (category vs date) detectado automaticamente.
    const layout = el._fullLayout || el.layout;
    if (!layout || !layout.xaxis || !layout.xaxis.range) return;
    const isCat = layout.xaxis.type === 'category';
    const stackedAxes = {};
    if (layout.barmode === 'stack' || layout.barmode === 'relative') {
      (el.data || []).forEach((t) => { if (t.type === 'bar') stackedAxes[t.yaxis || 'y'] = true; });
    }
    const xr = layout.xaxis.range;
    const lo = isCat ? Math.round(xr[0]) : _toComparableX(xr[0]);
    const hi = isCat ? Math.round(xr[1]) : _toComparableX(xr[1]);
    const axes = {};
    (el.data || []).forEach((t) => {
      if (!t.x || !t.y || t.visible === 'legendonly') return;
      const axisId = t.yaxis || 'y';
      if (!axes[axisId]) axes[axisId] = { mn: Infinity, mx: -Infinity, byX: {} };
      const a = axes[axisId];
      const stackable = stackedAxes[axisId] && t.type === 'bar';
      for (let i = 0; i < t.x.length; i++) {
        const inRange = isCat ? (i >= lo && i <= hi) : (_toComparableX(t.x[i]) >= lo && _toComparableX(t.x[i]) <= hi);
        if (!inRange) continue;
        const v = t.y[i];
        if (v == null || isNaN(v)) continue;
        if (stackable) {
          const key = isCat ? i : t.x[i];
          if (!a.byX[key]) a.byX[key] = { pos: 0, neg: 0 };
          if (v >= 0) a.byX[key].pos += v; else a.byX[key].neg += v;
        } else {
          if (v < a.mn) a.mn = v;
          if (v > a.mx) a.mx = v;
        }
      }
    });
    const upd = {}; let any = false;
    Object.keys(axes).forEach((axisId) => {
      const a = axes[axisId]; let mn = a.mn, mx = a.mx;
      Object.keys(a.byX).forEach((k) => {
        const b = a.byX[k];
        if (b.pos > mx) mx = b.pos;
        if (b.neg < mn) mn = b.neg;
      });
      if (Object.keys(a.byX).length) { mn = Math.min(mn, 0); mx = Math.max(mx, 0); }
      if (mn === Infinity || mx === -Infinity) return;
      const pad = Math.max((mx - mn) * 0.1, 0.5);
      const key = axisId === 'y' ? 'yaxis' : axisId.replace('y', 'yaxis');
      upd[key + '.range'] = [mn - pad, mx + pad];
      upd[key + '.autorange'] = false;
      any = true;
    });
    if (any) {
      lock = true;
      Plotly.relayout(divId, upd).then(() => { lock = false; }).catch(() => { lock = false; });
    }
  });
}
// depois de CADA Plotly.newPlot/react: _bindYAutofit('mainChart');
```

Só pule `_bindYAutofit` (deixe o Plotly com a interação padrão dele) em gráficos que não são série temporal no eixo X — ex. um ranking horizontal (x=valor, y=categoria) ou um heatmap com eixo Y fixo por categoria, mesma exceção já documentada nos relatórios analíticos.

Dica de descoberta, uma linha só, perto do topo da página (não repetir por gráfico):
```html
<div class="chart-hint">Todo gráfico: scroll/pinch para zoom (2 eixos) · arraste para mover (2 eixos) · double-click para resetar</div>
```
```css
.chart-hint {
  font-family: var(--mono); font-size: 10px; color: var(--muted);
  padding: 6px 2px 14px; letter-spacing: 0.02em;
}
```

### Formatação BR <a name="formatacao"></a>
```javascript
// Truncar (não arredondar!) para 1 casa decimal com vírgula
function fmtLabel(v) {
  return (Math.floor(v * 10) / 10).toFixed(1).replace('.', ',') + '%';
}

// Para preços
function fmtPrice(v) {
  return 'R$ ' + (Math.floor(v * 10) / 10).toFixed(1).replace('.', ',');
}

// Para quantidades
function fmtQty(v) {
  return (v / 1000).toFixed(1).replace('.', ',') + 'k';
}
```

Nota: o eixo Y do Plotly não aceita um formatter arbitrário em JS (só strings de formato d3, que não fazem vírgula decimal BR) — não tente forçar isso no eixo. Os valores formatados em BR (`fmtLabel`/`fmtPrice`/`fmtQty`) entram via `customdata` + `hovertemplate` (tooltip) e via `text` (labels sobre o gráfico, ver abaixo), nunca via tick do eixo.

### Datalabels (toggle de texto sobre o gráfico) <a name="datalabels"></a>

Chart.js tinha um plugin dedicado (`chartjs-plugin-datalabels`); no Plotly o equivalente é nativo — `mode` inclui `'text'`, com `text`/`textposition`/`textfont` por trace, e o toggle liga/desliga trocando `mode` via `Plotly.restyle` (sem re-renderizar o gráfico inteiro):

```javascript
// Step baseado no total de pontos -- igual ao Chart.js
const step = data.length > 60 ? 5 : data.length > 30 ? 3 : 1;

// Ao montar a trace:
{
  type: 'scatter',
  mode: showLabels ? 'lines+text' : 'lines',   // começa 'lines' (labels ocultos)
  x: dates, y: values,
  text: values.map((v, i) => (i % step === 0 ? fmtLabel(v) : '')),
  textposition: 'top center',
  textfont: { family: 'JetBrains Mono', size: 9, color: '#1F2853' },
  // ... cor/fill/hovertemplate, ver "Dataset padrão" abaixo
}
```

### Toggle labels function
```javascript
let showLabels = false;

function toggleLabels() {
  showLabels = !showLabels;
  document.getElementById('dlToggle').classList.toggle('on', showLabels);
  Plotly.restyle('mainChart', { mode: showLabels ? 'lines+text' : 'lines' }, [0]); // [0] = índice da trace principal
}
```

### Cores por variação <a name="cores"></a>
```javascript
// Marcadores coloridos: verde se subiu, vermelho se caiu -- array de cores
// por ponto, igual ao pointBackgroundColor do Chart.js mas via marker.color
const pointColors = data.map((d, i) =>
  i === 0 ? 'rgba(31,40,83,0.6)'
  : d.value >= data[i-1].value ? 'rgba(65,135,145,0.7)'
  : 'rgba(234,82,58,0.7)'
);
// na trace: mode: 'lines+markers', marker: { color: pointColors, size: 3 }
```

### Dataset padrão (single line) <a name="dataset-padrao"></a>
```javascript
{
  type: 'scatter',
  mode: 'lines+markers',           // markers sempre visíveis (pointRadius:3 do Chart.js)
  x: dates, y: values,
  line: { color: '#1F2853', width: 2, shape: 'spline', smoothing: 0.25 },
  marker: { color: pointColors, size: 3 },
  fill: 'tozeroy', fillcolor: 'rgba(31,40,83,0.06)',
  customdata: values.map(fmtLabel),          // valor já formatado em BR, para o tooltip
  hovertemplate: 'NOME_DA_SÉRIE: %{customdata}<extra></extra>',
}
```

### Layout padrão (chamar via `Plotly.newPlot(divId, traces, mkLayout(extra), PLOTLY_CONFIG)`)
`mkLayout()` (seção Zoom/Pan acima) já cobre `dragmode`, `hovermode`, `rangeselector`, cores de eixo/fonte. Para overrides específicos do gráfico (título de eixo Y, `barmode` para stacked bar, etc.), passe um objeto `extra`:

```javascript
Plotly.newPlot('mainChart', traces, mkLayout({
  yaxis: { ticksuffix: '%' },   // sufixo simples no eixo -- não um formatter BR completo, ver nota acima
}), PLOTLY_CONFIG);
_bindYAutofit('mainChart');
```

### Stats dinâmicos <a name="stats-dinamicos"></a>
```javascript
function buildStats(data, valueKey, label, suffix) {
  const last = data[data.length - 1];
  const min = data.reduce((a, b) => b[valueKey] < a[valueKey] ? b : a);
  const max = data.reduce((a, b) => b[valueKey] > a[valueKey] ? b : a);
  document.getElementById('statsRow').innerHTML = `
    <div class="stat-card">
      <div class="stat-label">${label} Último</div>
      <div class="stat-val">${last[valueKey].toFixed(2)}${suffix}</div>
      <div class="stat-sub">${formatDate(last.d)}</div>
    </div>
    <div class="stat-card">
      <div class="stat-label">Máxima</div>
      <div class="stat-val up">${max[valueKey].toFixed(2)}${suffix}</div>
      <div class="stat-sub">${formatDate(max.d)}</div>
    </div>
    <div class="stat-card">
      <div class="stat-label">Mínima</div>
      <div class="stat-val dn">${min[valueKey].toFixed(2)}${suffix}</div>
      <div class="stat-sub">${formatDate(min.d)}</div>
    </div>`;
}
```

---

## Cores para séries múltiplas

Coluna "Dash" usa a sintaxe do Plotly (`line.dash`: string, não array de pixels como no Chart.js):

| Série      | Linha      | Fill                    | Dash     |
|------------|------------|-------------------------|----------|
| Primária   | #1F2853    | rgba(31,40,83,0.08)     | solid    |
| Secundária | #02739B    | rgba(2,115,155,0.08)    | dash     |
| Terciária  | #BB9B1D    | rgba(187,155,29,0.12)   | dot      |
| Quaternária| #EA523A    | rgba(234,82,58,0.08)    | longdash |
| Quinquenária| #418791   | rgba(65,135,145,0.08)   | dashdot  |

Eixos independentes (série secundária num eixo à direita): trace da série secundária ganha `yaxis: 'y2'`, e o layout ganha `yaxis2: { overlaying: 'y', side: 'right', gridcolor: 'rgba(31,40,83,0.06)', tickfont: {...} }` — `_bindYAutofit` já é dual-axis-aware (agrupa por `t.yaxis || 'y'`), não precisa de tratamento especial.

---

## Checklist antes de entregar

- [ ] CDN: só Plotly (`https://cdn.plot.ly/plotly-2.35.2.min.js`) — sem Chart.js/chartjs-plugin-datalabels/hammer.js/chartjs-plugin-zoom
- [ ] Todo gráfico com série temporal em `mkLayout()` (`dragmode:'pan'`, `scrollZoom:true` no config, sem `fixedrange`, sem `xaxis.rangeselector`) + botões de range rápido via `renderQuickRangeButtons()` (HTML + `Plotly.relayout()`, NÃO `xaxis.rangeselector` nativo) + `_bindYAutofit(divId)` chamado logo após `Plotly.newPlot`/`react`
- [ ] Gráficos que não são série temporal (ranking horizontal, heatmap categórico) ficam com a interação padrão do Plotly — não force `_bindYAutofit` neles
- [ ] Cada gráfico é um `<div id="...">` vazio, nunca `<canvas>`
- [ ] Botão "Dados no gráfico" presente e funcional (`Plotly.restyle(..., {mode: 'lines+text'|'lines'}, [idx])`)
- [ ] Labels truncados com vírgula (não arredondados) — via `text`/`customdata`, nunca no tick do eixo Y
- [ ] Step adequado ao número de pontos
- [ ] Stats cards com último/máxima/mínima
- [ ] Marcadores coloridos por variação (verde/vermelho) via `marker.color` (array por ponto)
- [ ] Tooltip via `customdata`+`hovertemplate`, mostrando todas as métricas disponíveis, formatado em BR
- [ ] Formato BR: vírgula decimal, R$ para preços, k para milhares
- [ ] Footer com contexto
