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
9. [JS — Chart.js Setup](#chartjs-setup)
10. [JS — Datalabels](#datalabels)
11. [JS — Formatação BR](#formatacao)
12. [JS — Cores por variação](#cores)
13. [JS — Stats dinâmicos](#stats-dinamicos)
14. [Exemplo completo — Dashboard single-metric](#exemplo-single)
15. [Exemplo completo — Dashboard multi-metric](#exemplo-multi)

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
  <div class="chart-wrap"><canvas id="mainChart"></canvas></div>
</div>
```

### Footer <a name="footer"></a>
```html
<div class="ftr">Lis Capital · ATIVO · FUNDO · PERÍODO</div>
```

---

## JavaScript Patterns <a name="chartjs-setup"></a>

### Setup obrigatório
```javascript
// SEMPRE no início do script
Chart.register(ChartDataLabels);
```

### CDNs obrigatórios (no <head>)
```html
<link href="https://fonts.googleapis.com/css2?family=Barlow:wght@300;400;500;600;700&family=Barlow+Condensed:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.1/chart.umd.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/chartjs-plugin-datalabels/2.2.0/chartjs-plugin-datalabels.min.js"></script>
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

### Datalabels config <a name="datalabels"></a>
```javascript
// Step baseado no total de pontos
const step = data.length > 60 ? 5 : data.length > 30 ? 3 : 1;

datalabels: {
  display: false, // começa desligado!
  align: 'top',
  anchor: 'end',
  offset: 4,
  color: '#1F2853',
  font: { family: 'JetBrains Mono', size: 9, weight: 500 },
  formatter: (v, ctx) => ctx.dataIndex % step === 0 ? fmtLabel(v) : '',
  backgroundColor: 'rgba(255,255,255,0.85)',
  borderRadius: 3,
  padding: { top: 2, bottom: 2, left: 4, right: 4 }
}
```

### Toggle labels function
```javascript
let showLabels = false;

function toggleLabels() {
  showLabels = !showLabels;
  document.getElementById('dlToggle').classList.toggle('on', showLabels);
  chart.options.plugins.datalabels.display = showLabels;
  chart.update();
}
```

### Cores por variação <a name="cores"></a>
```javascript
// Pontos coloridos: verde se subiu, vermelho se caiu
const pointColors = data.map((d, i) =>
  i === 0 ? 'rgba(31,40,83,0.6)'
  : d.value >= data[i-1].value ? 'rgba(65,135,145,0.7)'
  : 'rgba(234,82,58,0.7)'
);
```

### Dataset padrão (single line)
```javascript
{
  data: values,
  borderColor: '#1F2853',
  backgroundColor: 'rgba(31,40,83,0.06)',
  fill: true,
  pointBackgroundColor: pointColors,
  pointRadius: 3,      // 4 se poucos pontos
  pointHoverRadius: 6,  // 7 se poucos pontos
  borderWidth: 2,
  tension: 0.25
}
```

### Chart options padrão
```javascript
{
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: { display: false },
    datalabels: { /* config acima */ },
    tooltip: {
      backgroundColor: '#1F2853',
      titleFont: { family: 'JetBrains Mono', size: 11 },
      bodyFont: { family: 'Barlow', size: 12 },
      padding: 12,
      cornerRadius: 8,
      callbacks: { /* custom por dashboard */ }
    }
  },
  scales: {
    x: {
      grid: { color: 'rgba(31,40,83,0.04)' },
      ticks: { color: '#7A88A8', font: { family: 'JetBrains Mono', size: 9 }, maxTicksLimit: 20, maxRotation: 45 }
    },
    y: {
      grid: { color: 'rgba(31,40,83,0.06)' },
      ticks: { color: '#7A88A8', font: { family: 'JetBrains Mono', size: 10 }, callback: v => v.toFixed(0) + '%' }
    }
  },
  interaction: { mode: 'index', intersect: false }
}
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

| Série      | Linha      | Fill                    | Dash   |
|------------|------------|-------------------------|--------|
| Primária   | #1F2853    | rgba(31,40,83,0.08)     | solid  |
| Secundária | #02739B    | rgba(2,115,155,0.08)    | [6,3]  |
| Terciária  | #BB9B1D    | rgba(187,155,29,0.12)   | [2,2]  |
| Quaternária| #EA523A    | rgba(234,82,58,0.08)    | [8,4]  |
| Quinquenária| #418791   | rgba(65,135,145,0.08)   | [4,2]  |

---

## Checklist antes de entregar

- [ ] `Chart.register(ChartDataLabels)` no início
- [ ] Botão "Dados no gráfico" presente e funcional
- [ ] Labels truncados com vírgula (não arredondados)
- [ ] Step adequado ao número de pontos
- [ ] Stats cards com último/máxima/mínima
- [ ] Pontos coloridos por variação (verde/vermelho)
- [ ] `responsive:true, maintainAspectRatio:false`
- [ ] Tooltip mostrando todas as métricas disponíveis
- [ ] Formato BR: vírgula decimal, R$ para preços, k para milhares
- [ ] Footer com contexto
