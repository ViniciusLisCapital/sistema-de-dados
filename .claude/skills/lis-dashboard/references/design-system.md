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
15. [Cores para séries múltiplas — e como garantir que não se confundem](#cores-series)
16. [Botão de informação + card de definição](#info-card)
17. [Cabeçalho do gráfico](#cabecalho)
18. [Unidade no eixo Y](#unidades)

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
.chart-subtitle { font-size: 12px; color: var(--ice2); line-height: 1.4; margin-top: 3px; }
.chart-src { font-family: var(--mono); font-size: 10px; color: var(--muted); margin-top: 5px; }
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

O título, o subtítulo e a linha de fonte são **obrigatórios** e o subtítulo é
**preenchido por JS a cada render**, nunca escrito fixo no HTML — ver
[Cabeçalho do gráfico](#cabecalho). As pills de range ficam **abaixo** do gráfico.

```html
<div class="chart-container">
  <div class="chart-hdr">
    <div class="chart-hdr-left">
      <div class="chart-title" id="chartTitle">TÍTULO DO GRÁFICO</div>
      <!-- preenchidos por describeChart(), não escritos à mão -->
      <div class="chart-subtitle" id="chartSub"></div>
      <div class="chart-src" id="chartSrc"></div>
    </div>
    <div class="chart-hdr-right">
      <!-- filtros e/ou dl-toggle aqui -->
      <div class="dl-toggle" id="dlToggle" onclick="toggleLabels()">
        <span class="toggle-icon"></span> Dados no gráfico
      </div>
    </div>
  </div>
  <div class="chart-wrap"><div id="mainChart" style="width:100%"></div></div>
  <div class="range-pills" id="rangePills"></div>
</div>
```

### Footer <a name="footer"></a>
```html
<div class="ftr">Lis Capital · ATIVO · FUNDO · PERÍODO</div>
```

---

## JavaScript Patterns <a name="chartjs-setup"></a>

Padrão único de charting do projeto desde 2026-07-28 (histórico completo da mudança em `.claude/rules/lis-dashboards.md`, repo principal): **Plotly**, não Chart.js. Todo relatório analítico do projeto (`analytics/brasil/exchange_rate/report.html`, `analytics/brasil/inflation/report.html`) já usava Plotly desde o início; esta skill migrou para o mesmo padrão no mesmo dia em que `ppp_dashboard.html` (originalmente Chart.js; então em `analytics/brasil/exchange_rate/referencia/`, movido para o `reports/` de topo em 2026-08 por ser um deliverable gerado por código, não material de referência) foi convertido, a pedido direto do usuário ("I want all graphs to be this way ... set this in skill too"). Os padrões abaixo são os MESMOS já usados nesses relatórios — não uma variação nova.

### CDNs obrigatórios (no <head>)
```html
<link href="https://fonts.googleapis.com/css2?family=Barlow:wght@300;400;500;600;700&family=Barlow+Condensed:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<script src="https://cdn.plot.ly/plotly-2.35.2.min.js" charset="utf-8"></script>
```

Nada além disso — sem Chart.js, sem chartjs-plugin-datalabels, sem hammer.js/chartjs-plugin-zoom. Cada `<div id="...">` vazio (não `<canvas>`) recebe seu gráfico via `Plotly.newPlot`/`Plotly.react`.

## JS — Zoom/Pan Interativo <a name="zoom-pan"></a>

**Obrigatório em todo dashboard** — nenhum gráfico fica estático. Interação livre nos dois eixos, mesmo padrão usado em `analytics/brasil/exchange_rate/report.html`/`analytics/brasil/inflation/report.html` (histórico completo, incluindo as versões descartadas antes de chegar neste padrão, em `.claude/rules/lis-dashboards.md`):

- **Arrastar (drag)** → pan nos dois eixos diretamente (Plotly `dragmode:'pan'` nativo)
- **Scroll / pinch** → zoom nos dois eixos, ancorado no cursor (`scrollZoom:true`)
- **Double-click** → reseta para o range completo (comportamento nativo do Plotly, não precisa de handler)
- **Sem gesto de box-zoom** (o `dragmode:'pan'` do Plotly já substitui o `'zoom'` padrão da lib, que faria rubber-band box-zoom)
- **Botões de range rápido** (1a/3a/5a/10a/Tudo) — **botões HTML normais + `Plotly.relayout()` direto, NÃO o `xaxis.rangeselector` nativo do Plotly.** Ver caixa de atenção abaixo antes de implementar isso de outra forma.

> [!WARNING]
> **Não use `layout.xaxis.rangeselector` para os botões de range rápido.** Duas tentativas anteriores nesse próprio padrão quebraram em produção (`analytics/brasil/economic_activity/report.html`, 2026-08, histórico completo em `.claude/rules/lis-dashboards.md`):
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
// containerEl: elemento vazio (ex. <div class="range-pills"></div>) posicionado ABAIXO do gráfico,
// dentro do mesmo card (pedido explícito do usuário, 2026-08-27: "coloque o seletor de range de data
// na parte debaixo do grafico; aplique em todos os graficos"). Acima também funciona, mas a régua de
// tempo pertence ao pé do gráfico, junto do eixo X que ela controla.
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
.range-pills { display: flex; gap: 6px; flex-wrap: wrap; justify-content: center; padding: 8px 0 2px; }
.range-pill {
  font-family: var(--mono, 'JetBrains Mono'); font-size: 11px; font-weight: 500; letter-spacing: 0.03em;
  padding: 4px 13px; border: 1px solid rgba(31,40,83,0.15); border-radius: 20px;
  background: rgba(31,40,83,0.03); color: #7A88A8; cursor: pointer; transition: all .15s;
}
.range-pill:hover { color: #1F2853; border-color: rgba(31,40,83,0.3); }
```

**Por que ainda precisa de um helper de autofit em Y, mesmo com `dragmode:'pan'`+Y livre:** os botões de range rápido (1a/3a/...) mudam `xaxis.range` diretamente, sem nenhum gesto de usuário em Y — então Y fica mostrando o range antigo (às vezes uma janela nova e estreita espremida no range antigo inteiro). `_bindYAutofit` cobre exatamente esse caso: só recalcula Y quando `xaxis.range` mudou **sem** `yaxis`/`yaxis2` também terem mudado no mesmo evento (ou seja, clique num botão de range rápido ou um double-click reset — nunca um drag/scroll direto, que já move os dois eixos juntos e não deve ser contrariado). Isso continua funcionando idêntico com os novos botões HTML: `Plotly.relayout()` dispara o mesmo evento `plotly_relayout` que os botões nativos disparavam. Versão genérica (funciona com eixo category ou date, single ou dual y-axis, barras simples ou empilhadas — mesma função usada nos três relatórios analíticos e nas abas de modelo do `analytics/brasil/exchange_rate/report.html`, ex-`ppp_dashboard.html`, fundido nele em 2026-08):

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

## Cores para séries múltiplas <a name="cores-series"></a>

**Duas séries do mesmo gráfico têm que ser distinguíveis, e isso é uma medida, não uma
impressão.** Pedido explícito do usuário (2026-09-01), depois de reportar que "a cor de
consumo das famílias e de exportações está muito próximo" em
`analytics/brasil/economic_activity/report.html`: *"coloque esse cuidado da skill
/lis-dashboard para sempre garantir que as cores não serão confundidas"*.

O que a auditoria daquele relatório achou é o motivo de isto virar regra: o par reportado
estava a **ΔE2000 = 13,0**, mas na mesma vista havia **três pares com a cor idêntica** —
as óticas da oferta e da demanda tinham sido coloridas em separado, como se nunca fossem
plotadas juntas, e o multiselect deixa. Nada disso lança exceção: o gráfico renderiza
perfeitamente.

### A regra

**ΔE2000 ≥ 20 entre quaisquer duas séries que possam aparecer no mesmo gráfico.**

O 20 é calibrado, não inventado: é onde fecham as duas paletas publicadas que são
referência em legibilidade — **Okabe-Ito** (8 cores, mínimo 21,7) e **Tol bright** (7
cores, mínimo 20,5). A paleta antiga desta skill fechava em 13,0.

### A paleta

Qualquer par tem ΔE2000 ≥ 20,8. `PALETTE[0]` (navy da marca) fica **reservado para a linha
de total/agregado** — a série de referência do gráfico —, e as 4 primeiras são cores da
marca. As últimas são mais claras e só entram quando há muita série marcada ao mesmo tempo.

```js
const PALETTE = [
  '#1F2853', // navy (marca) -- reservado para o total
  '#EA523A', // laranja (marca)
  '#418791', // verde-petróleo (marca)
  '#BB9B1D', // dourado (marca)
  '#8E44AD', // roxo
  '#1565C0', // azul
  '#5D6B1F', // oliva
  '#AD1457', // magenta escuro
  '#795548', // marrom
  '#7CB342', // verde claro
  '#F06292', // rosa
  '#64B5F6', // azul pastel
  '#9E9E9E', // cinza
  '#B39DDB', // lilás
];
```

Cores que **saíram** por não passarem no limiar, e que estavam na paleta antiga: `#02739B`
(azul claro — 13,0 do verde-petróleo, o par que o usuário viu), `#FBC852` (amarelo — 13,9
do dourado) e `#BFBFBF` (cinza claro — 9,3 do cinza da paleta). Usar qualquer uma delas
junto do seu par é o defeito, não a cor em si.

Isto vale para **séries dentro de um gráfico**, não para cromo de interface: o `--purple`
(`#02739B`) segue sendo a cor de botões, badges e do botão `i` — ali ele nunca compete com
`#418791` pela atenção do leitor no mesmo eixo.

### Acima de 13 séries, mude de canal

13 matizes separáveis é o teto prático — 30 não existem, e nenhuma paleta publicada passa
de 8–9. Passando disso, a cor **volta ao início da paleta e o tracejado muda**
(`line.dash`, sintaxe do Plotly: string, não array de pixels como no Chart.js). É o segundo
canal que mantém as séries distinguíveis quando o primeiro se esgota — não empilhe mais
matizes.

### A cor sai da POSIÇÃO, não de um literal por série

Escrever a cor em cada categoria é o que produz colisão: duas listas coloridas em momentos
diferentes não sabem uma da outra. Atribua por posição, com as séries **marcadas por
padrão na frente da fila** — assim a vista inicial, que é a que quase todo mundo vê, nunca
repete cor.

```js
const SERIES_DASH = ['solid', 'dash', 'dot'];
// `fixos` prende uma série a uma cor (o agregado de referência do gráfico, p.ex.).
function assignSeriesColors(cats, defaults, fixos) {
  fixos = fixos || {};
  const ordem = [];
  (defaults || []).forEach((b) => cats.forEach((c) => {
    if (c.base === b && ordem.indexOf(c) < 0) ordem.push(c);
  }));
  cats.forEach((c) => { if (ordem.indexOf(c) < 0) ordem.push(c); });
  const n = PALETTE.length - 1;   // PALETTE[0] fica de fora: é a cor do total
  let k = 0;
  ordem.forEach((c) => {
    if (fixos[c.base]) { c.color = fixos[c.base]; c.dash = 'solid'; return; }
    c.color = PALETTE[1 + (k % n)];
    c.dash = SERIES_DASH[Math.min(SERIES_DASH.length - 1, Math.floor(k / n))];
    k++;
  });
  return cats;
}
// no trace: line: { color: s.color, width: 2, dash: s.dash || 'solid' }
```

Trocar a cor de uma série específica passa a ser **mudar a ordem dela na lista**, não
editar um literal — e a garantia vale para a lista inteira, não para o par que alguém
lembrou de olhar.

### Verifique, não confie no olho

ΔE2000 em ~50 linhas de JS, para rodar no harness de teste do dashboard. Asserção mínima:
para **cada gráfico**, nenhum par de traces com o mesmo `dash` pode ficar abaixo de 20.

```js
function _lin(c) { c /= 255; return c <= 0.04045 ? c / 12.92 : Math.pow((c + 0.055) / 1.055, 2.4); }
function _lab(hex) {
  const h = hex.replace('#', '');
  const r = _lin(parseInt(h.slice(0, 2), 16)), g = _lin(parseInt(h.slice(2, 4), 16)), b = _lin(parseInt(h.slice(4, 6), 16));
  const x = (r * 0.4124564 + g * 0.3575761 + b * 0.1804375) / 0.95047;
  const y = (r * 0.2126729 + g * 0.7151522 + b * 0.0721750);
  const z = (r * 0.0193339 + g * 0.1191920 + b * 0.9503041) / 1.08883;
  const f = (t) => (t > 216 / 24389 ? Math.cbrt(t) : (841 / 108) * t + 4 / 29);
  const fx = f(x), fy = f(y), fz = f(z);
  return [116 * fy - 16, 500 * (fx - fy), 200 * (fy - fz)];
}
function deltaE(hex1, hex2) {                       // CIEDE2000
  const A = _lab(hex1), B = _lab(hex2);
  const C1 = Math.hypot(A[1], A[2]), C2 = Math.hypot(B[1], B[2]), Cb = (C1 + C2) / 2;
  const G = 0.5 * (1 - Math.sqrt(Math.pow(Cb, 7) / (Math.pow(Cb, 7) + Math.pow(25, 7))));
  const a1p = (1 + G) * A[1], a2p = (1 + G) * B[1];
  const C1p = Math.hypot(a1p, A[2]), C2p = Math.hypot(a2p, B[2]);
  const h1p = (Math.atan2(A[2], a1p) * 180 / Math.PI + 360) % 360;
  const h2p = (Math.atan2(B[2], a2p) * 180 / Math.PI + 360) % 360;
  const dLp = B[0] - A[0], dCp = C2p - C1p;
  let dhp = 0;
  if (C1p * C2p !== 0) { dhp = h2p - h1p; if (dhp > 180) dhp -= 360; else if (dhp < -180) dhp += 360; }
  const dHp = 2 * Math.sqrt(C1p * C2p) * Math.sin(dhp * Math.PI / 360);
  const Lbp = (A[0] + B[0]) / 2, Cbp = (C1p + C2p) / 2;
  let hbp;
  if (C1p * C2p === 0) hbp = h1p + h2p;
  else if (Math.abs(h1p - h2p) <= 180) hbp = (h1p + h2p) / 2;
  else hbp = (h1p + h2p + (h1p + h2p < 360 ? 360 : -360)) / 2;
  const rad = (d) => d * Math.PI / 180;
  const T = 1 - 0.17 * Math.cos(rad(hbp - 30)) + 0.24 * Math.cos(rad(2 * hbp))
            + 0.32 * Math.cos(rad(3 * hbp + 6)) - 0.20 * Math.cos(rad(4 * hbp - 63));
  const dTheta = 30 * Math.exp(-Math.pow((hbp - 275) / 25, 2));
  const Rc = 2 * Math.sqrt(Math.pow(Cbp, 7) / (Math.pow(Cbp, 7) + Math.pow(25, 7)));
  const Sl = 1 + (0.015 * Math.pow(Lbp - 50, 2)) / Math.sqrt(20 + Math.pow(Lbp - 50, 2));
  const Sc = 1 + 0.045 * Cbp, Sh = 1 + 0.015 * Cbp * T;
  const Rt = -Math.sin(rad(2 * dTheta)) * Rc;
  return Math.sqrt(Math.pow(dLp / Sl, 2) + Math.pow(dCp / Sc, 2) + Math.pow(dHp / Sh, 2)
                   + Rt * (dCp / Sc) * (dHp / Sh));
}
```

E **exercite o segundo canal de propósito**: nenhuma vista padrão chega a 13 séries, então
um teste que só olhe a vista inicial passa mesmo com o `dash` removido das linhas
(verificado num mutante que fazia exatamente isso). Marque tudo e asserte que aparece mais
de um tracejado.

### Daltonismo: o que dá para prometer, e o que não dá

Medido nesta paleta: sob **deuteranopia/protanopia** o par **dourado × laranja da marca**
cai para ΔE 5,4, e nenhuma escolha das outras cores conserta isso — as duas são âncoras de
marca. Um gráfico que precise ser legível para daltônicos não pode usar as duas juntas; a
saída é tracejado diferente ou trocar uma delas.

Isso **não** é um defeito exclusivo desta paleta: na mesma medida a própria Okabe-Ito cai
para 9,1 e a Tol bright para 1,2. Segurança para daltônicos é uma garantia mais fraca do
que o senso comum sugere — trate como um número a reportar, não como uma porta a fechar.

### Eixos independentes

Eixos independentes (série secundária num eixo à direita): trace da série secundária ganha `yaxis: 'y2'`, e o layout ganha `yaxis2: { overlaying: 'y', side: 'right', gridcolor: 'rgba(31,40,83,0.06)', tickfont: {...} }` — `_bindYAutofit` já é dual-axis-aware (agrupa por `t.yaxis || 'y'`), não precisa de tratamento especial.

---

## Botão de informação + card de definição <a name="info-card"></a>

Pedido do usuário (2026-08-27): *"algumas linhas poderiam ter um nome mais simples com um card
descritivo quando passa o mouse por cima ... um botão que você clica e consegue ver a definição e
explicações, assim não precisa escrever tudo na linha e deixar a tabela deformada"*.

O rótulo visível é o **nome curto**; o nome oficial da fonte e a explicação ficam num card que abre no
hover e fixa no clique. Vale para qualquer rótulo que precise ser curto na tela mas ambíguo fora dela:
linha de tabela, botão de toggle de série, label de stat card, título de gráfico.

```
┌─────────────────────────────────────────────┐
│ Taxa Combinada — Horas                      │  ← nome curto (o que aparece)
│ Taxa combinada de desocupação e de          │  ← nome oficial da fonte
│ subocupação por insuficiência de horas...   │
│                                             │
│ Soma desocupados e subocupados por          │  ← a explicação
│ insuficiência de horas, sobre a força...    │
│ ───────────────────────────────────────     │
│ Unidade: (desocupados + subocupados) /      │  ← reaproveita a unidade do eixo
│ força de trabalho, %                        │
└─────────────────────────────────────────────┘
```

**Quatro decisões que evitam refazer isto:**

1. **Um único card no `<body>`, reposicionado a cada abertura** — não um popover por item. Numa
   página com dezenas de rótulos, um nó por item é DOM que quase nunca é visto.
2. **Só ganha botão quem precisa.** Rótulo que já se explica não leva `i`; o ícone tem que ser raro
   para significar alguma coisa. Guarde a informação num mapa `chave → {full, desc}` e deixe o botão
   nascer da presença da entrada, em vez de decidir item a item no markup.
3. **Não repita o rótulo dentro do card.** Anexe `full` só quando ele **difere** do que já está na
   tela — senão o card abre para dizer o que o usuário acabou de ler.
4. **A última linha reaproveita a mesma string de unidade que vai para o título do eixo Y** (ver
   [Unidade no eixo Y](#unidades)), para as duas não divergirem com o tempo.

Hover abre, clique **fixa** (o texto precisa poder ser lido com calma e selecionado), clique fora ou
Esc fecha. O card se prende à direita da janela e vira para cima quando não cabe embaixo — necessário
porque tabelas e barras de toggle rolam na horizontal e o botão pode estar na borda.

```css
.info-btn {
  display: inline-flex; align-items: center; justify-content: center;
  width: 14px; height: 14px; margin-left: 6px; padding: 0; flex: 0 0 auto;
  font-family: var(--mono); font-size: 9px; font-weight: 600; line-height: 1;
  color: var(--muted); background: transparent;
  border: 1px solid var(--line); border-radius: 50%; cursor: pointer;
  vertical-align: middle; transition: all .15s;
}
.info-btn:hover, .info-btn.pinned { color: #fff; background: var(--purple); border-color: var(--purple); }
.info-pop {
  position: absolute; z-index: 300; display: none; max-width: 380px;
  background: var(--bg2); border: 1px solid var(--line); border-radius: 10px;
  box-shadow: 0 6px 24px rgba(31,40,83,0.16); padding: 12px 14px;
}
.info-pop.show { display: block; }
.info-pop h4 { font-family: var(--cond); font-size: 13.5px; font-weight: 600; color: var(--ice); line-height: 1.3; }
.info-pop .info-full { font-size: 12px; color: var(--ice2); line-height: 1.45; margin-top: 5px; }
.info-pop .info-desc { font-size: 12px; color: var(--muted); line-height: 1.5; margin-top: 8px; }
.info-pop .info-unit {
  font-family: var(--mono); font-size: 10px; color: var(--muted);
  margin-top: 9px; padding-top: 8px; border-top: 1px solid var(--line);
}
```

```js
// Mapa de informação: só o que precisa de card entra aqui.
// chave -> { full: nome oficial da fonte, desc: explicação, unit: unidade }
const INFO = {
  ibov:  { full: 'Índice Bovespa (pontos de fechamento)', desc: 'Carteira teórica...', unit: 'pontos' },
  // ...
};

let _pop = null, _pinned = null;
function _ensurePop() {
  if (_pop) return _pop;
  _pop = document.createElement('div');
  _pop.className = 'info-pop';
  document.body.appendChild(_pop);
  _pop.addEventListener('mouseleave', () => { if (!_pinned) hideInfo(); });
  document.addEventListener('click', (e) => {
    if (_pinned && !_pop.contains(e.target) && e.target !== _pinned) hideInfo();
  });
  document.addEventListener('keydown', (e) => { if (e.key === 'Escape') hideInfo(); });
  return _pop;
}
function hideInfo() {
  if (!_pop) return;
  _pop.classList.remove('show');
  if (_pinned) { _pinned.classList.remove('pinned'); _pinned = null; }
}
function showInfo(btn, label, info) {
  const pop = _ensurePop();
  let html = '<h4>' + label + '</h4>';
  // `full` só entra quando acrescenta algo ao rótulo já visível.
  if (info.full && info.full !== label) html += '<div class="info-full">' + info.full + '</div>';
  if (info.desc) html += '<div class="info-desc">' + info.desc + '</div>';
  if (info.unit) html += '<div class="info-unit">Unidade: ' + info.unit + '</div>';
  pop.innerHTML = html;
  pop.classList.add('show');

  const r = btn.getBoundingClientRect();
  const w = pop.offsetWidth || 380, h = pop.offsetHeight || 120;
  let left = r.left + window.scrollX;
  const maxLeft = window.scrollX + document.documentElement.clientWidth - w - 12;
  if (left > maxLeft) left = Math.max(window.scrollX + 12, maxLeft);
  let top = r.bottom + window.scrollY + 6;
  if (r.bottom + h + 18 > document.documentElement.clientHeight) top = r.top + window.scrollY - h - 6;
  pop.style.left = left + 'px';
  pop.style.top = top + 'px';
}
// Pendura o botão em qualquer elemento que mostre um rótulo curto.
// Não faz nada se a chave não estiver no INFO -- é assim que o ícone fica raro.
function attachInfo(hostEl, key, label) {
  const info = INFO[key];
  if (!info || (!info.full && !info.desc)) return;
  const b = document.createElement('button');
  b.type = 'button';
  b.className = 'info-btn';
  b.textContent = 'i';
  b.setAttribute('aria-label', 'Definição de ' + label);
  b.addEventListener('mouseenter', () => { if (!_pinned) showInfo(b, label, info); });
  b.addEventListener('mouseleave', () => {
    if (_pinned) return;
    // Deixa o ponteiro atravessar o vão até o card antes de fechar.
    setTimeout(() => { if (!_pinned && !_pop.matches(':hover')) hideInfo(); }, 120);
  });
  b.addEventListener('click', (e) => {
    e.stopPropagation();
    if (_pinned === b) { hideInfo(); return; }
    hideInfo();
    _pinned = b; b.classList.add('pinned');
    showInfo(b, label, info);
  });
  hostEl.appendChild(b);
}
```

Cuidado ao ler o rótulo de volta do DOM depois disso: `textContent` do elemento passa a incluir o "i"
do botão. Se algum código compara rótulos (teste, filtro, busca), leia só os nós de texto —
`[...el.childNodes].filter(n => n.nodeType === 3).map(n => n.textContent).join('')`.

**Quinta decisão, quando a página tem mais de uma tabela: a chave do mapa precisa de NAMESPACE.**
Descoberta em `analytics/brasil/fiscal_policy` (2026-08-28), onde a mesma chave `receita_total`
aparece em duas árvores da mesma aba significando coisas diferentes — uma classifica as
transferências constitucionais como despesa, a outra as deduz da receita. Um mapa de chave nua faz
uma tabela explicar a outra, e **nada lança**: o cartão abre, com o texto errado. Guarde
`namespace:chave` e faça cada tabela declarar o seu. Duas extensões que valem junto:

- **Aceite uma LISTA de namespaces, tentada em ordem.** Quando uma segunda tabela reusa a mesma
  árvore mudando o significado de poucos nós (lá: as rubricas viram *contribuição ao impulso*, com
  sinal), o específico ganha entrada própria e o resto cai no compartilhado — em vez de duplicar
  dezenas de textos que envelheceriam separados.
- **Se a chave não bater, tente o sufixo depois do último `__`.** É o que faz uma definição servir a
  todas as variantes de um mesmo item (`geral__folha`, `central__folha`, …). Lá, 99 entradas cobrem
  184 linhas por causa disso.

**Teste a órfã, não só o card.** Um erro de digitação numa chave produz um botão que deixa de nascer:
sem erro, sem lacuna visível. Resolva toda chave do mapa contra as árvores reais e exija zero órfãs —
foi o que pegou dois `full` que só repetiam o rótulo e uma chave inexistente naquele port.

Implementação de referência: `analytics/brasil/labor_market/report.html`, 52 rótulos com card em 17
tabelas; a variante com namespace está em `analytics/brasil/fiscal_policy/report.html`, 99 entradas
cobrindo 184 linhas em 10 tabelas.

---

## Cabeçalho do gráfico — ele tem que se explicar sozinho <a name="cabecalho"></a>

Pedido do usuário (2026-08-27): *"se eu enviar o gráfico para alguém, a pessoa não fará a mínima ideia
do que se passa, terá que ler os eixos"*. Um gráfico daqui costuma sair da página como print e circular
sozinho, então ele precisa dizer **o quê, em que métrica, em que unidade, de que fonte e de quando até
quando** — três linhas no topo do card, acima do plot:

```
Taxa de Desocupação — Brasil
Mensal (trimestre móvel) · desocupados / força de trabalho, %
Fonte: IBGE, PNAD Contínua · mar/2012 a jul/2026
```

**Regra dura: só o título e a fonte são texto fixo. O subtítulo e o período são recalculados a cada
render.** Um subtítulo escrito no HTML começa certo e passa a mentir no instante em que alguém mexe num
seletor — e é justamente o print tirado depois desse clique que vai circular. Pelo mesmo motivo o
período sai da extensão real das séries plotadas, não de uma constante: numa visão de variação anual o
gráfico legitimamente começa um ano depois.

O subtítulo carrega, nesta ordem: as séries marcadas (quando dizem algo além do título), o estado dos
**seletores** (frequência, janela, métrica) e a unidade — a mesma string do título do eixo Y, ver
[Unidade no eixo Y](#unidades).

**A poda é a parte que dá trabalho.** O mesmo fato chega por três caminhos — o rótulo da opção do
seletor, o nome da série e o título do eixo — e imprimir os três lado a lado vira ruído ("Taxa de
Desocupação · Mensal · Taxa · desocupados / força de trabalho, %"). Duas regras resolvem: **não repita
o rótulo de um seletor cujo conteúdo já está no título do eixo** (o "Nível"/"Taxa" da visão de nível,
cuja informação é a unidade; ou uma janela que o próprio eixo nomeia), e **descarte o nome da série
quando ele é o próprio título do gráfico**. Na prática, filtre cada pedaço contra o título do eixo
antes de juntar tudo.

```js
// Extensão real das séries plotadas -- nunca a constante do dataset inteiro,
// nem o range atual do eixo (que traz o padding do Plotly).
function dataExtent(series) {
  let lo = null, hi = null;
  (series || []).forEach((s) => (s.dates || []).forEach((d, i) => {
    if (s.values[i] == null || isNaN(s.values[i])) return;
    if (lo === null || d < lo) lo = d;
    if (hi === null || d > hi) hi = d;
  }));
  return lo === null ? null : [lo, hi];
}
const MESES = ['jan','fev','mar','abr','mai','jun','jul','ago','set','out','nov','dez'];
const fmtMesAno = (iso) => MESES[parseInt(iso.slice(5, 7), 10) - 1] + '/' + iso.slice(0, 4);

// o = { title, subEl, srcEl, series, bits, unit, source, fmtDate }
//   series : as séries EFETIVAMENTE plotadas ({name, dates, values})
//   bits   : estado dos seletores já como rótulos ('Mensal', 'Acum. 12m', ...)
//   unit   : o mesmo texto do título do eixo Y
function describeChart(o) {
  let bits = [];
  const nomes = (o.series || []).map((s) => s.name);
  // Nome da série só entra se disser algo além do título.
  if (nomes.length && !(nomes.length === 1 && o.title.indexOf(nomes[0]) === 0)) bits.push(nomes.join(', '));
  (o.bits || []).forEach((b) => { if (b) bits.push(b); });
  // Nada que a unidade já diga.
  const lowU = (o.unit || '').toLowerCase();
  bits = bits.filter((b) => lowU.indexOf(b.toLowerCase()) < 0);
  if (o.unit) bits.push(o.unit);

  const ext = dataExtent(o.series);
  const f = o.fmtDate || fmtMesAno;
  const periodo = ext ? f(ext[0]) + ' a ' + f(ext[1]) : '';
  o.subEl.textContent = bits.join(' · ');
  o.srcEl.textContent = (o.source || '') + (periodo ? (o.source ? ' · ' : '') + periodo : '');
}
// Chamar de dentro da MESMA função que redesenha o gráfico, com as séries que
// ela acabou de plotar -- não num init que roda uma vez só.
```

Aplicado nos 17 gráficos de `analytics/brasil/labor_market/report.html`, que é a implementação de
referência (lá o subtítulo sai de uma árvore hierárquica de linhas marcadas; aqui, das séries ligadas
nos toggles — a regra de poda é a mesma).

---

## Unidade no eixo Y — o que a série mede, não só em que unidade <a name="unidades"></a>

Convenção do usuário (2026-08-27): **todo gráfico diz no eixo Y o que está medindo**, e o rótulo é
uma definição curta, não o nome da unidade. "A taxa de desocupação mede o quê? O percentual de
desempregados vis-à-vis a força de trabalho" — então o eixo diz `desocupados / força de trabalho, %`,
não `%` nem `Taxa (%)`. Uma linha, do tamanho de um rótulo de eixo: **não é para escrever um livro no
gráfico.**

```js
// Ruim: não informa nada que o título do card já não diga
yaxis: { title: { text: '%' } }
// Bom: numerador / denominador, unidade
yaxis: { title: { text: 'desocupados / força de trabalho, %' } }
```

Exemplos do padrão (do relatório de mercado de trabalho, onde os denominadores foram conferidos
contra os próprios níveis da fonte antes de virarem rótulo):

| Série | Eixo Y |
|---|---|
| Taxa de desocupação | `desocupados / força de trabalho, %` |
| Taxa de participação | `força de trabalho / população 14+, %` |
| Nível da ocupação | `ocupados / população 14+, %` |
| Rendimento médio | `rendimento médio mensal, R$ por pessoa` |
| Massa de rendimento | `massa de rendimento mensal, R$ milhões` |
| Saldo do CAGED | `saldo (admissões − desligamentos) — pessoas no mês` |

**A unidade acompanha a métrica selecionada.** Se o gráfico tem um seletor Nível/Variação, o eixo
**não pode** continuar dizendo a unidade do nível na visão de variação — foi exatamente o bug
reportado ("mesmo sendo uma variação % Y/Y, ainda aparece como nível de mil pessoas"). Na visão de
variação o eixo passa a ser `p.p. contra o mesmo período do ano anterior` (séries que já são razão) ou
`% contra o mesmo período do ano anterior` (níveis e valores em R$).

Duas consequências práticas:

- **A unidade não vive no rótulo da série.** `"Pessoas Ocupadas (mil pessoas)"` mente na visão de
  variação, porque o rótulo aparece na legenda em qualquer métrica. Guarde a unidade num campo
  próprio do dado (ex.: `unit` curto para a tabela, `def` para o eixo) e monte o rótulo do eixo a
  partir da métrica selecionada + das séries plotadas.
- **Numa tabela/gráfico de unidades mistas** (uma taxa em % e um nível em mil pessoas marcados
  juntos), o eixo não pode escolher uma das duas: diga `unidades mistas — ver a unidade de cada linha`
  e mostre a unidade curta ao lado do rótulo de cada linha da tabela. Numa tabela toda na mesma
  unidade, **não** repita a unidade linha a linha — o eixo já disse, e a repetição só polui.

---

## Texto explicativo: justificado e na largura do bloco <a name="prosa"></a>

Convenção do projeto desde 2026-09-01, a pedido do usuário, a partir de um print: **todo
texto explicativo e todo texto de apêndice sai justificado e ocupa a largura do bloco que o
contém.** Nada de `max-width` em `ch` na prosa.

```css
/* Liste aqui as classes de PROSA do dashboard — legenda de gráfico, corpo de apêndice,
   nota de metodologia, lead de seção. Não `.kpi-sub`, não célula de tabela, não linha de
   metadado em mono. */
.chart-caption,
.appendix-body,
.note-metodologia,
.lead {
  text-align: justify;
  text-justify: inter-word;
  -webkit-hyphens: auto;
  hyphens: auto;
}
```

Três coisas que fazem a regra funcionar, e cada uma é o motivo de um erro possível:

- **`hyphens: auto` é obrigatório junto do `justify`, não é enfeite.** Sem hifenização o
  texto abre rios de espaço branco entre as palavras da linha — pior em português, que tem
  palavras longas e poucas monossílabas para o navegador usar de folga.
- **A hifenização depende do `lang` no `<html>`.** Sem ele o browser não sabe que dicionário
  usar e não hifeniza nada: a regra *parece* aplicada e produz justamente os rios que ela
  existia para evitar. `<html lang="pt-BR">` (ou `en` num dashboard em inglês).
- **Tirar o `max-width` em `ch` resolve duas coisas de uma vez.** Cobre o vazio à direita do
  parágrafo *e*, ocupando mais linha, deixa o bloco **mais baixo** — o que num card cheio de
  nota é a diferença entre caber e não caber na tela. Medido no relatório do calendário: uma
  nota de 526 caracteres caiu de 7 para 3 linhas, e o card encurtou ~160 px.

**O que fica de fora, e por quê:**

| não justifique | motivo |
|---|---|
| célula de tabela (`td` com `max-width` em ch) | container estreito é exatamente onde os rios aparecem |
| popover de definição (`.info-pop`, ~320 px) | mesmo motivo |
| linha de metadado em mono (`rodou em … · ~90s · em dia`) | é lista de campos separada por `·`, não prosa |
| rodapé/legenda centralizada | `text-align: center` é decisão de layout; justificar exigiria tirá-la |
| rótulo curto (`.kpi-sub`, `.stat-sub`) | uma linha não tem o que justificar |

A ressalva a levar ao usuário quando o container é muito largo: num bloco de 1.300 px a
12 px a linha passa de 200 caracteres, bem acima da faixa confortável de leitura (45–90).
Foi decisão explícita do usuário cobrir a largura; se ele reclamar do contrário, o
corretivo é um `max-width` generoso (~120ch), não voltar aos 78ch.

Aplicado em: `analytics/release_calendar/` (origem) e nos 9 relatórios de `analytics/brasil/`
e `analytics/us/`.

## O texto explicativo é para quem nunca viu o dashboard <a name="audiencia"></a>

Pedido direto do usuário (2026-09-01), sobre um print de um card cheio de nota: *"você está
transferindo nossa conversa daqui para o dash, e eu não quero isso. Lá deve ser a explicação do
que está acontecendo ali, para alguém que nunca viu o dashboard e não sabe da nossa conversa."*

O sintoma é fácil de reconhecer depois de nomeado: a prosa tinha virado transcrição da sessão
em que o dashboard foi construído.

| o que estava escrito | por que não serve |
|---|---|
| "Desde 2026-08-31 o Regerar refaz…" | a data é do dia em que **nós** mudamos o código; o leitor não estava lá |
| "as abas leem artefatos que o `generate_report` NÃO calcula" | nomes do repositório — função, arquivo, tabela |
| "Segundos não medidos" | anotação de pendência nossa, não informação sobre o dado |
| "cada trimestre" (a granularidade) | é o nome do mecanismo, não a consequência dele |
| "O Regerar refaz antes de gerar · nada atrasado" | descreve a ordem interna de duas funções, não o que o leitor vê |

A regra que substitui: **cada bloco de prosa responde "o que é isto que estou vendo, e o que
isso muda para mim?"**, no vocabulário do domínio (dado, cálculo, relatório, banco), não no do
repositório. Quatro trocas cobrem quase todos os casos:

- **Nome de mecanismo → consequência.** `cada trimestre` → *fica velho quando abre um trimestre
  novo*. Quem lê precisa saber de quanto em quanto tempo aquilo desatualiza, não em que unidade
  duas datas são comparadas.
- **Identificador → nome que se lê.** `expc_focus_periodo já tinha 31/08` → *a pesquisa Focus já
  tinha dado de 31/08*. Guarde o nome legível **ao lado** do técnico na própria estrutura de
  dados (um campo `nome` no mapa de fontes), para os dois não divergirem depois.
- **Data de decisão → nada.** "Desde 2026-08-31" pertence ao `CLAUDE.md` e ao git log; no
  dashboard ela só levanta a pergunta "e antes disso?".
- **Ordem interna → efeito visível.** Em vez de *"o Regerar refaz antes de gerar"*, diga o que
  pode dar errado e como se corrige: *"se um destes foi calculado com dado mais antigo do que o
  banco já tem, o número dentro do relatório fica velho mesmo que o arquivo seja novo — é isso
  que o botão Regerar corrige"*.

O que **fica**: decisões, medições e o "por que" continuam sendo escritos — no `CLAUDE.md` da
pasta e nos comentários do código, que é onde a próxima sessão procura. Nada disso é apagado; é
movido.

**Vale testar**, porque a prosa é o único conteúdo do dashboard que nenhuma asserção olhava.
Extraia os blocos de prosa do HTML renderizado e proíba uma lista de termos — e rode contra o
payload **real**, para cobrir o que está escrito na configuração e não só o que o template monta:

```js
const PROSA = (cards.match(/<div class="(?:dash-note|proc-note|proc-hint)">([\s\S]*?)<\/div>/g) || [])
  .map((b) => b.replace(/<[^>]*>/g, ''));
const JARGAO = ['generate_report', 'manifest.yaml', 'granularidade', 'mtime', 'ETL',
                'run(', 'Desde 2026', 'não medidos'];
// nenhum termo em nenhum bloco; e cada bloco com texto de verdade (> 60 caracteres)
```

Aplicado em `analytics/release_calendar/report.html` + as 10 notas de
`domain/dashboards/manifest.yaml`, e na faixa de frescor de
`analytics/brasil/monetary_policy/report.html`. Fechado por `tests/test_release_calendar_js.js`
(o guarda acima, verificado contra um mutante que reinjeta a frase antiga) e por
`tests/test_monetary_policy_js.js`, que exercita a faixa laranja sinteticamente — ela não
aparece no payload de um relatório recém-gerado, que é justamente o caso que o leitor precisa
entender.

## Checklist antes de entregar

- [ ] CDN: só Plotly (`https://cdn.plot.ly/plotly-2.35.2.min.js`) — sem Chart.js/chartjs-plugin-datalabels/hammer.js/chartjs-plugin-zoom
- [ ] Todo gráfico com série temporal em `mkLayout()` (`dragmode:'pan'`, `scrollZoom:true` no config, sem `fixedrange`, sem `xaxis.rangeselector`) + botões de range rápido via `renderQuickRangeButtons()` (HTML + `Plotly.relayout()`, NÃO `xaxis.rangeselector` nativo) + `_bindYAutofit(divId)` chamado logo após `Plotly.newPlot`/`react`
- [ ] Texto explicativo e de apêndice **justificado** (`text-align: justify` + `hyphens: auto`), sem `max-width` em `ch`, e o `<html>` com `lang` — sem o `lang` não há hifenização e o justificado abre rios. Não justifique célula de tabela, `.info-pop` nem legenda centralizada. Ver [Texto explicativo](#prosa)
- [ ] Texto explicativo escrito para quem **nunca viu o dashboard**: sem nome de arquivo/função do repositório, sem data de decisão nossa ("desde 2026-…"), sem o nome do mecanismo no lugar da consequência. Ver [Para quem nunca viu o dashboard](#audiencia)
- [ ] Rótulo longo vira nome curto + botão `i` com card de definição (nunca um rótulo que deforma a coluna/legenda). Ver [Botão de informação](#info-card)
- [ ] Todo gráfico com cabeçalho de 3 linhas — título, subtítulo e fonte+período — e o subtítulo/período **recalculados a cada render**, nunca fixos no HTML. Ver [Cabeçalho do gráfico](#cabecalho)
- [ ] Subtítulo reflete o estado dos seletores e não repete o que o título do eixo já diz
- [ ] Botões de range **abaixo** do gráfico, dentro do mesmo card
- [ ] Eixo Y diz o que a série mede (`desocupados / força de trabalho, %`), não só a unidade — e MUDA com a métrica selecionada (na visão de variação, `p.p./% contra o mesmo período do ano anterior`, nunca a unidade do nível). Unidade fora do rótulo da série. Ver [Unidade no eixo Y](#unidades)
- [ ] Gráficos que não são série temporal (ranking horizontal, heatmap categórico) ficam com a interação padrão do Plotly — não force `_bindYAutofit` neles
- [ ] Cada gráfico é um `<div id="...">` vazio, nunca `<canvas>`
- [ ] Botão "Dados no gráfico" presente e funcional (`Plotly.restyle(..., {mode: 'lines+text'|'lines'}, [idx])`)
- [ ] Labels truncados com vírgula (não arredondados) — via `text`/`customdata`, nunca no tick do eixo Y
- [ ] Step adequado ao número de pontos
- [ ] Stats cards com último/máxima/mínima
- [ ] Marcadores coloridos por variação (verde/vermelho) via `marker.color` (array por ponto)
- [ ] Cores de séries pela `PALETTE` via `assignSeriesColors()` (nunca um `color:` literal por série), com ΔE2000 ≥ 20 entre quaisquer duas séries do mesmo gráfico — conferido com `deltaE()`, não a olho. Ver [Cores para séries múltiplas](#cores-series)
- [ ] Tooltip via `customdata`+`hovertemplate`, mostrando todas as métricas disponíveis, formatado em BR
- [ ] Formato BR: vírgula decimal, R$ para preços, k para milhares
- [ ] Footer com contexto
