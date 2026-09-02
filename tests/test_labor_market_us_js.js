// Testa o JS REAL de reports/us/Labor Market.html contra um DOM stub e um Plotly stub.
//
// Roda com:
//     node tests/test_labor_market_us_js.js
//
// Precisa do relatorio gerado:
//     uv run python -c "from analytics.us.labor_market.generate_report import run; run()"
//
// Cada secao existe por um modo de falha que NAO lanca excecao. Os cinco que mais
// custaram em outros relatorios deste projeto, e que aqui sao afirmados de frente:
//
//   (a) A JANELA DO EIXO X. Seis versoes do mesmo defeito estao documentadas em
//       .claude/rules/lis-dashboards.md, e todas as seis passam por "o range veio do
//       estado do Plotly em vez dos dados". As secoes 3 e 4 afirmam sobre a janela que
//       cada botao PRODUZ e sobre a que a primeira pintura aplica, nao sobre a
//       definicao dos botoes -- foi asserir sobre a definicao que deixou dois desses
//       defeitos irem para producao.
//   (b) AGREGAR UM ESTOQUE COMO FLUXO. Vagas e posicao no ultimo dia util; somar 12
//       meses dela da ~12x e continua parecendo um grafico de vagas. A secao 5 exige
//       que a pill esteja desligada e que o estado nao consiga chegar la.
//   (c) EMPILHAR O QUE NAO SOMA. Taxa e razao contra o emprego da propria categoria;
//       empilhar irmas inventa um total. Secao 6.
//   (d) COR REPETIDA. dE2000 < 20 entre duas series do mesmo grafico. Numa auditoria
//       real isso apareceu como TRES pares de cor identica na vista default. Secao 8,
//       que tambem marca as 28 linhas para exercitar o tracejado -- nenhuma vista
//       default chega a 13 series, entao um teste que so olhe a inicial passa mesmo
//       com o `dash` removido.
//   (e) CARTAO COM O TEXTO ERRADO. '00' e categoria em dois cortes com significados
//       diferentes. Secao 9.
//
// O que ele NAO substitui: confirmacao visual num browser real.

const fs = require('fs');
const path = require('path');

const HTML = path.join(__dirname, '..', 'reports', 'us', 'Labor Market.html');
if (!fs.existsSync(HTML)) {
  console.error('reports/us/Labor Market.html nao existe -- gere o relatorio primeiro:');
  console.error('  uv run python -c "from analytics.us.labor_market.generate_report import run; run()"');
  process.exit(1);
}
const CRU = fs.readFileSync(HTML, 'utf8');
const blocos = CRU.match(/<script>([\s\S]*?)<\/script>/g) || [];
if (!blocos.length) { console.error('nenhum <script> no HTML'); process.exit(1); }
const SRC = blocos[blocos.length - 1].replace(/^<script>/, '').replace(/<\/script>$/, '');

let falhas = 0, asserts = 0;
function ok(cond, nome, detalhe) {
  asserts++;
  if (cond) console.log('  ok    ' + nome);
  else { falhas++; console.log('  FALHA ' + nome + (detalhe ? '  -- ' + detalhe : '')); }
}
function secao(t) { console.log('\n' + t); }

// ── DOM stub ────────────────────────────────────────────────────────────────
function El(tag) {
  this.tag = tag || 'div';
  this.children = []; this.style = {}; this.dataset = {};
  this._className = ''; this.textContent = ''; this.value = '';
  this._html = ''; this._listeners = {}; this._plotly = {};
  this.parentNode = null; this.title = '';
  const self = this;
  this.classList = {
    _set: {},
    add(c) { self.classList._set[c] = true; self._sync(); },
    remove(c) { delete self.classList._set[c]; self._sync(); },
    contains(c) { return !!self.classList._set[c]; },
    toggle(c, force) {
      const on = force === undefined ? !self.classList._set[c] : !!force;
      if (on) self.classList._set[c] = true; else delete self.classList._set[c];
      self._sync(); return on;
    },
  };
}
El.prototype._sync = function () { this._className = Object.keys(this.classList._set).join(' '); };
Object.defineProperty(El.prototype, 'className', {
  get() { return this._className; },
  set(v) {
    this._className = v; this.classList._set = {};
    String(v).split(/\s+/).filter(Boolean).forEach((c) => { this.classList._set[c] = true; });
  },
});
El.prototype.appendChild = function (c) { c.parentNode = this; this.children.push(c); return c; };
El.prototype.insertBefore = function (n, r) {
  n.parentNode = this;
  const i = this.children.indexOf(r);
  this.children.splice(i < 0 ? this.children.length : i, 0, n);
  return n;
};
El.prototype.removeChild = function (c) {
  const i = this.children.indexOf(c);
  if (i >= 0) this.children.splice(i, 1);
  c.parentNode = null; return c;
};
El.prototype.remove = function () { if (this.parentNode) this.parentNode.removeChild(this); };
El.prototype.setAttribute = function (k, v) { (this._attrs = this._attrs || {})[k] = v; };
El.prototype.addEventListener = function (k, f) { (this._listeners[k] = this._listeners[k] || []).push(f); };
El.prototype.fire = function (k, ev) { (this._listeners[k] || []).forEach((f) => f(ev || {})); };
El.prototype.on = function (k, f) { (this._plotly[k] = this._plotly[k] || []).push(f); };
El.prototype.contains = function () { return false; };
El.prototype.matches = function () { return false; };
El.prototype.getBoundingClientRect = function () {
  return { left: 10, right: 24, top: 40, bottom: 54, width: 14, height: 14 };
};
// Selector minimo: '.cls', 'tag', 'tag.cls'. Suficiente para o que o relatorio usa
// ('button.rb', '.dl-toggle', '.chart') e explicito o bastante para quebrar em vez de
// devolver vazio caladamente se alguem escrever um seletor mais complexo.
function _casa(el, sel) {
  const m = /^([a-z]*)(?:\.([\w-]+))?$/.exec(sel);
  if (!m) throw new Error('seletor nao suportado pelo stub: ' + sel);
  if (m[1] && el.tag !== m[1]) return false;
  if (m[2] && !el.classList.contains(m[2])) return false;
  return true;
}
El.prototype.querySelectorAll = function (sel) {
  const out = [], pilha = (this.children || []).slice();
  while (pilha.length) {
    const n = pilha.shift();
    if (n.tag !== '#text' && _casa(n, sel)) out.push(n);
    pilha.push.apply(pilha, n.children || []);
  }
  return out;
};
El.prototype.querySelector = function (sel) { return this.querySelectorAll(sel)[0] || null; };
Object.defineProperty(El.prototype, 'innerHTML', {
  get() { return this._html; },
  set(v) {
    this._html = v; this.children = [];
    const re = /<(\w+)[^>]*class="([^"]*)"[^>]*>/g;
    let m;
    while ((m = re.exec(String(v))) !== null) {
      const f = new El(m[1]); f.className = m[2]; this.appendChild(f);
    }
  },
});
Object.defineProperty(El.prototype, 'offsetWidth', { get() { return 390; } });
Object.defineProperty(El.prototype, 'offsetHeight', { get() { return 130; } });

// Rotulo LIMPO: so os nos de TEXTO. Filtrar por tag vira lista de excecoes que
// envelhece -- ver a nota em .claude/rules/lis-dashboards.md.
function rotuloLimpo(el) {
  return el.children.filter((c) => c.tag === '#text').map((c) => c.textContent).join('').trim();
}

// Os 4 botoes de aba, com o data-panel lido do HTML gerado.
const TAB_BTNS = [];
(CRU.match(/<button data-panel="([^"]+)"[^>]*>([^<]*)<\/button>/g) || []).forEach((blk) => {
  const b = new El('button');
  b.dataset.panel = /data-panel="([^"]+)"/.exec(blk)[1];
  b.textContent = />([^<]*)<\/button>/.exec(blk)[1];
  TAB_BTNS.push(b);
});
const PANEL_IDS = TAB_BTNS.map((b) => b.dataset.panel);

const els = {};
const PANELS = {};
const doc = {
  getElementById(id) {
    if (!els[id]) { const el = new El('div'); el.id = id; els[id] = el; }
    return els[id];
  },
  createElement: (t) => new El(t),
  createTextNode(t) { const n = new El('#text'); n.textContent = t; return n; },
  querySelector: () => null,
  querySelectorAll(sel) {
    if (sel === 'nav.tabs button') return TAB_BTNS;
    if (sel === '.panel') return PANEL_IDS.map((id) => { if (!PANELS[id]) { PANELS[id] = new El('section'); PANELS[id].id = id; } return PANELS[id]; });
    return [];
  },
  addEventListener() {},
  body: new El('body'),
  documentElement: { clientWidth: 1400, clientHeight: 900 },
};
// Os painéis precisam existir com o mesmo objeto que getElementById devolve, senao
// wireTabs() acha um painel e o teste inspeciona outro.
PANEL_IDS.forEach((id) => { PANELS[id] = doc.getElementById(id); });

const chamadas = [];
function thenable(v) { return { then(f) { f(v); return thenable(v); }, catch() { return thenable(v); } }; }
const plotlyStub = {
  react(divId, traces, layout) {
    chamadas.push({ tipo: 'react', divId, traces, layout });
    const el = doc.getElementById(divId);
    el.data = traces;
    el._fullLayout = JSON.parse(JSON.stringify(layout || {}));
    el._fullLayout.xaxis = el._fullLayout.xaxis || {};
    if (!el._fullLayout.xaxis.type) el._fullLayout.xaxis.type = 'date';
    return thenable(el);
  },
  newPlot(divId, traces, layout) { return this.react(divId, traces, layout); },
  relayout(divId, upd) {
    chamadas.push({ tipo: 'relayout', divId, upd });
    const el = doc.getElementById(divId);
    if (upd && upd['xaxis.range'] && el._fullLayout) el._fullLayout.xaxis.range = upd['xaxis.range'];
    (el._plotly['plotly_relayout'] || []).forEach((f) => f(upd));
    return thenable(el);
  },
  Plots: { resize() {} },
};

global.document = doc;
global.window = { scrollX: 0, scrollY: 0 };
global.Plotly = plotlyStub;

const EXPORTS = ['D', 'TABS', 'PALETTE', 'TRANSFORMS', 'achatar', 'flattenHierRows',
                 '_janela', '_yoy', '_mm', 'serieTransformada', '_extentPlotado', '_rangeOptions',
                 'dataExtent', 'assignSeriesColors', 'VALORES', '_RANGE_MEM', 'fmtNum'];
let R;
try {
  new Function(SRC + ';global.__R = {' + EXPORTS.join(',') + '};')();
  R = global.__R;
} catch (e) {
  console.error('erro ao executar o script do relatorio:', e.message);
  console.error(e.stack);
  process.exit(1);
}
const D = R.D;
const CORTES = ['industria', 'tamanho', 'regiao'];

// ── CIEDE2000 (copia da referencia do design system) ────────────────────────
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
function deltaE(hex1, hex2) {
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

// ── helpers de leitura ──────────────────────────────────────────────────────
function ultimaReact(divId) {
  for (let i = chamadas.length - 1; i >= 0; i--) {
    if (chamadas[i].tipo === 'react' && chamadas[i].divId === divId) return chamadas[i];
  }
  return null;
}
function relayoutsDe(divId) {
  return chamadas.filter((c) => c.tipo === 'relayout' && c.divId === divId);
}
function pills(corte, grupo) {
  return doc.getElementById('pg-' + corte + '-' + grupo).children;
}
function pillLabel(b) {
  const s = b.children.find((c) => c.tag === 'span');
  return s ? s.textContent : '';
}
function pillDe(corte, grupo, label) {
  return pills(corte, grupo).find((b) => pillLabel(b) === label);
}
function clicar(b) { b.fire('click'); }
const MS_DIA = 86400000;
function ms(iso) { return Date.parse(iso + 'T00:00:00Z'); }

// ── 1. boot ─────────────────────────────────────────────────────────────────
secao('1. Boot');
ok(!!R.TABS && CORTES.every((c) => R.TABS[c]), 'os 3 cortes foram construidos');
// A faixa de KPI saiu a pedido do usuario (2026-09-01). Isto e afirmado para o CSS e a
// funcao nao voltarem como codigo morto num merge futuro.
ok(!/renderKpis|class="kpi/.test(CRU), 'nenhum vestigio da faixa de KPI no HTML gerado');
CORTES.forEach((c) => {
  ok(!!ultimaReact('chart-' + c), c + ': o grafico foi plotado no boot',
     'sem react para chart-' + c);
});
ok(D.dates.length > 300 && D.meta.nSeries > 900,
   'payload: ' + D.meta.nSeries + ' series x ' + D.dates.length + ' meses');
ok(D.dates[D.dates.length - 1] === D.meta.ultimoMes,
   'a grade termina no mes de referencia declarado (' + D.meta.ultimoMes + ')');

// Os tres cortes ficam numa aba SO (pedido do usuario, 2026-09-01) -- antes eram tres
// abas. Isto e afirmado sobre a marcacao porque de dentro do JS os elementos sao
// buscados por id: um card que escape do painel some da pagina sem erro nenhum, e um
// card que perca um grupo de pill continua renderizando.
const ABAS_ESPERADAS = ['Payroll', 'Household', 'JOLTS', 'Derived', 'Appendix'];
ok(TAB_BTNS.length === ABAS_ESPERADAS.length
   && TAB_BTNS.every((b, i) => b.textContent === ABAS_ESPERADAS[i]),
   ABAS_ESPERADAS.length + ' abas, na ordem: ' + ABAS_ESPERADAS.join(' | '),
   TAB_BTNS.map((b) => b.textContent).join(' | '));
ok(TAB_BTNS[0] && TAB_BTNS[0].dataset.panel === 'p-payroll',
   'a aba default e o payroll (a manchete do release)',
   TAB_BTNS[0] ? TAB_BTNS[0].dataset.panel : 'nenhuma');
ok((CRU.match(/class="panel active"/g) || []).length === 1,
   'exatamente um painel nasce ativo');
const _iJolts = CRU.indexOf('id="p-jolts"');
const _painelJolts = CRU.slice(_iJolts, CRU.indexOf('</section>', _iJolts));
ok(_iJolts > 0 && CORTES.every((c) => _painelJolts.indexOf('id="chart-' + c + '"') > 0),
   'os 3 graficos estao dentro do MESMO <section class="panel">',
   CORTES.filter((c) => _painelJolts.indexOf('id="chart-' + c + '"') < 0).join(', ') + ' fora');
ok((_painelJolts.match(/<div class="card">/g) || []).length === 3,
   '3 cards dentro da aba JOLTS, um por corte',
   (_painelJolts.match(/<div class="card">/g) || []).length + ' cards');
const _PILLS = ['medida', 'tipo', 'ajuste', 'transform', 'kind'];
CORTES.forEach((c) => {
  const falta = _PILLS.filter((g) => _painelJolts.indexOf('id="pg-' + c + '-' + g + '"') < 0);
  ok(falta.length === 0, c + ': mantem os 5 grupos de pill', 'faltam ' + falta.join(', '));
});

// ── 2. a regua fica ABAIXO do grafico ───────────────────────────────────────
// Isto e afirmado sobre o HTML e nao sobre o DOM stub: os elementos sao buscados por
// id, entao a ordem entre eles nao e observavel de dentro do JS. A regra
// ("coloque o seletor de range na parte debaixo do grafico", 2026-08-27) e sobre a
// marcacao, e e nela que ela tem de ser conferida.
secao('2. A regua de tempo fica ABAIXO do grafico');
CORTES.forEach((c) => {
  const frame = new RegExp('<div class="chart-frame">([\\s\\S]*?)</div>\\s*</div>\\s*</section>', 'g');
  const trecho = CRU.slice(CRU.indexOf('id="ct-' + c + '"'));
  const iChart = trecho.indexOf('id="chart-' + c + '"');
  const iBar = trecho.indexOf('id="rb-' + c + '"');
  ok(iChart > 0 && iBar > iChart,
     c + ': <div class="range-bar"> vem depois de <div class="chart">',
     'chart em ' + iChart + ', bar em ' + iBar);
});
ok(!/rangeselector\s*:/.test(SRC),
   'nenhum `rangeselector:` nativo do Plotly no script');
ok(!/autorange\s*:\s*true/.test(SRC),
   'nenhum `autorange: true` — toda janela e calculada dos dados');

// ── 3. a janela que cada botao PRODUZ ───────────────────────────────────────
secao('3. A janela que cada botao de range produz');
CORTES.forEach((c) => {
  const divId = 'chart-' + c;
  const ext = R._extentPlotado(divId);
  ok(!!ext, c + ': extent derivado de gd.data');
  if (!ext) return;
  const passoMax = 32 * MS_DIA;                 // mensal: meia-passada <= ~16 dias
  const botoes = doc.getElementById('rb-' + c).querySelectorAll('button.rb');
  ok(botoes.length >= 3, c + ': ' + botoes.length + ' botoes de range');
  botoes.forEach((b) => {
    const antes = relayoutsDe(divId).length;
    clicar(b);
    const rl = relayoutsDe(divId).slice(antes);
    const comX = rl.filter((x) => x.upd && x.upd['xaxis.range']);
    const nova = comX.length ? comX[comX.length - 1].upd['xaxis.range'] : null;
    if (!nova) { ok(false, c + '/' + b.textContent + ': clique nao produziu xaxis.range'); return; }
    // O clique move so X; `_bindYAutofit` tem de reagir e refitar Y no MESMO clique --
    // sem isso a janela nova aparece espremida no range de Y da janela anterior.
    const comY = rl.filter((x) => x.upd && Object.keys(x.upd).some((k) => /^yaxis/.test(k)));
    ok(comY.length >= 1, c + '/' + b.textContent + ': _bindYAutofit refitou Y no mesmo clique',
       'nenhum relayout de yaxis');
    const fimOk = ms(nova[1]) >= ms(ext.hi) && ms(nova[1]) - ms(ext.hi) <= passoMax / 2 + MS_DIA;
    const iniOk = ms(nova[0]) >= ms(ext.lo) - MS_DIA;
    ok(fimOk && iniOk,
       c + '/' + b.textContent + ': [' + nova[0] + ', ' + nova[1] + '] dentro de meia passada dos dados',
       'dados ' + ext.lo + '..' + ext.hi);
    if (b.textContent === 'All') {
      ok(nova[0] === ext.lo, c + '/All: comeca no primeiro ponto real, nao no autorange');
    }
  });
  // O botao clicado fica marcado, e so ele.
  const ativos = doc.getElementById('rb-' + c).querySelectorAll('button.rb').filter((b) => b.classList.contains('active'));
  ok(ativos.length === 1, c + ': exatamente 1 botao ativo', ativos.length + '');
});

// ── 4. a primeira pintura ───────────────────────────────────────────────────
// A vista inicial e produzida por nenhum botao, e por isso ficou no `autorange` em
// varios relatorios deste projeto -- que e exatamente o que os botoes existem para
// evitar. Aqui ela e conferida num contexto NOVO, antes de qualquer clique.
secao('4. A vista inicial e uma janela calculada, nao autorange');
(function () {
  const els2 = {}, panels2 = {};
  const doc2 = {
    getElementById(id) { if (!els2[id]) { const e = new El('div'); e.id = id; els2[id] = e; } return els2[id]; },
    createElement: (t) => new El(t),
    createTextNode(t) { const n = new El('#text'); n.textContent = t; return n; },
    querySelector: () => null,
    querySelectorAll(sel) {
      if (sel === 'nav.tabs button') return [];
      if (sel === '.panel') return [];
      return [];
    },
    addEventListener() {},
    body: new El('body'),
    documentElement: { clientWidth: 1400, clientHeight: 900 },
  };
  const chamadas2 = [];
  const plot2 = {
    react(divId, traces, layout) {
      chamadas2.push({ tipo: 'react', divId, traces, layout });
      const el = doc2.getElementById(divId);
      el.data = traces; el._fullLayout = { xaxis: { type: 'date' } };
      return thenable(el);
    },
    newPlot(a, b, c) { return this.react(a, b, c); },
    relayout(divId, upd) { chamadas2.push({ tipo: 'relayout', divId, upd }); return thenable(doc2.getElementById(divId)); },
    Plots: { resize() {} },
  };
  const antesDoc = global.document, antesPlot = global.Plotly;
  global.document = doc2; global.Plotly = plot2;
  try {
    new Function(SRC + ';global.__R2 = {D: D, TABS: TABS, _extentPlotado: _extentPlotado};')();
  } finally {
    global.document = antesDoc; global.Plotly = antesPlot;
  }
  CORTES.forEach((c) => {
    const divId = 'chart-' + c;
    const rl = chamadas2.filter((x) => x.tipo === 'relayout' && x.divId === divId
                                       && x.upd && x.upd['xaxis.range']);
    ok(rl.length >= 1, c + ': a primeira pintura aplica um xaxis.range explicito');
    if (!rl.length) return;
    const janela = rl[rl.length - 1].upd['xaxis.range'];
    const trace = chamadas2.filter((x) => x.tipo === 'react' && x.divId === divId).pop();
    let lo = null, hi = null;
    trace.traces.forEach((t) => t.x.forEach((x, i) => {
      if (t.y[i] == null || isNaN(t.y[i])) return;
      if (lo === null || x < lo) lo = x;
      if (hi === null || x > hi) hi = x;
    }));
    ok(janela[0] === lo && ms(janela[1]) >= ms(hi),
       c + ': a vista inicial e "All" sobre o extent plotado (' + lo + ' .. ' + hi + ')',
       'aplicou ' + JSON.stringify(janela));
    ok(!chamadas2.some((x) => x.tipo === 'relayout' && x.divId === divId
                              && x.upd && x.upd['xaxis.autorange']),
       c + ': nenhum relayout de autorange');
  });
})();

// ── 5. estoque x fluxo: o acumulado de 12 meses ─────────────────────────────
secao('5. Estoque x fluxo — a pill de acumulado 12M');
CORTES.forEach((c) => {
  const tab = R.TABS[c];
  // Vagas (estoque): a pill existe, esta desligada e explica por que.
  clicar(pillDe(c, 'medida', 'Job openings'));
  clicar(pillDe(c, 'tipo', 'Level'));
  let p = pillDe(c, 'transform', '12M total');
  ok(p && p.classList.contains('disabled'),
     c + ': com Job openings + Level, "12M total" esta desligada');
  ok(p && /stock/i.test(p.title), c + ': ...e o title explica que vagas e estoque',
     p ? p.title : '');
  // O clique nao pode mudar o estado.
  const antes = tab.state.transform;
  clicar(p);
  ok(tab.state.transform === antes, c + ': clicar na pill desligada nao muda o estado');

  // Fluxo (contratacoes): a mesma pill liga.
  clicar(pillDe(c, 'medida', 'Hires'));
  p = pillDe(c, 'transform', '12M total');
  ok(p && !p.classList.contains('disabled'),
     c + ': com Hires + Level, "12M total" esta ligada');
  clicar(p);
  ok(tab.state.transform === 'sum12', c + ': e selecionavel');
  ok(/12 months to the date/.test(tab.yTitle()),
     c + ': o eixo Y passa a dizer "during the 12 months to the date"', tab.yTitle());

  // Taxa: a pill volta a desligar, E o estado cai de volta para o mensal em vez de
  // ficar num acumulado de razoes.
  clicar(pillDe(c, 'tipo', 'Rate'));
  ok(tab.state.transform === 'm',
     c + ': trocar para Rate com 12M total selecionado cai de volta para Monthly',
     tab.state.transform);
  p = pillDe(c, 'transform', '12M total');
  ok(p && p.classList.contains('disabled') && /ratio/i.test(p.title),
     c + ': ...e a pill fica desligada, explicando que razoes nao somam', p ? p.title : '');
  // Nunca ha um estado (medida x tipo) em que sum12 esteja ativo sem ser fluxo+nivel.
  clicar(pillDe(c, 'medida', 'Job openings'));
  clicar(pillDe(c, 'tipo', 'Level'));
});
// E a contraprova numerica de por que isso importa: somar 12 meses de vagas da ~12x.
(function () {
  const chave = ['industria', '000000', 'JO', 'nivel', 'sa'].join('|');
  const mensal = R.serieTransformada(chave, 'm', false);
  const somada = R._janela(D.series[chave], 12, false);
  const i = mensal.length - 1;
  const razao = somada[i] / mensal[i];
  ok(razao > 10 && razao < 14,
     'somar 12 meses de vagas daria ' + razao.toFixed(1) + 'x o nivel — e por isso que a pill nao existe',
     'razao ' + razao);
})();

// ── 6. empilhar o que nao soma ──────────────────────────────────────────────
secao('6. Barras empilhadas');
CORTES.forEach((c) => {
  const tab = R.TABS[c];
  clicar(pillDe(c, 'medida', 'Job openings'));
  clicar(pillDe(c, 'tipo', 'Level'));
  clicar(pillDe(c, 'transform', 'Monthly'));
  let b = pillDe(c, 'kind', 'Stacked bars');
  ok(b && !b.classList.contains('disabled'), c + ': Level + Monthly permite barras');
  clicar(b);
  ok(tab.state.kind === 'bars', c + ': barras selecionadas');
  let react = ultimaReact('chart-' + c);
  ok(react.layout.barmode === 'relative',
     c + ": barmode 'relative' (contribuicoes negativas ficam abaixo do zero, nao dentro da pilha)",
     react.layout.barmode);
  // A raiz esta marcada E tem descendente marcado -> tem de virar LINHA.
  const raizLabel = D.cortes[c].tree[0].label;
  const traceRaiz = react.traces.find((t) => t.name === raizLabel);
  ok(traceRaiz && traceRaiz.type === 'scatter',
     c + ': a raiz (' + raizLabel + ') vira LINHA, nao uma barra sobre as proprias partes',
     traceRaiz ? traceRaiz.type : 'ausente');
  const barras = react.traces.filter((t) => t.type === 'bar');
  ok(barras.length >= 2, c + ': ' + barras.length + ' filhos empilhados como barra');

  // Taxa: desliga, e o estado volta para linhas.
  clicar(pillDe(c, 'tipo', 'Rate'));
  b = pillDe(c, 'kind', 'Stacked bars');
  ok(b && b.classList.contains('disabled'), c + ': Rate desliga as barras');
  ok(tab.state.kind === 'lines', c + ': ...e o estado cai de volta para Lines', tab.state.kind);
  ok(/employment/.test(b.title), c + ': ...com o motivo no title', b.title);

  // Y/Y de nivel: tambem desliga (variacao percentual nao soma entre irmas).
  clicar(pillDe(c, 'tipo', 'Level'));
  clicar(pillDe(c, 'kind', 'Stacked bars'));
  clicar(pillDe(c, 'transform', 'Y/Y'));
  ok(tab.state.kind === 'lines', c + ': Y/Y tambem cai de volta para Lines', tab.state.kind);
  clicar(pillDe(c, 'transform', 'Monthly'));
  clicar(pillDe(c, 'kind', 'Lines'));
});

// ── 6b. % do total ──────────────────────────────────────────────────────────
// O tipo "% of total" nao existe em mt_jolts: e o nivel dividido pelo nivel da RAIZ da
// PROPRIA arvore. O erro que isto existe para pegar e um denominador compartilhado --
// usar Total nonfarm nas classes de tamanho nao levanta excecao nenhuma, so faz as seis
// somarem 88,86% em vez de 100%.
secao('6b. % do total — o denominador e a raiz da propria arvore');
CORTES.forEach((c) => {
  const tab = R.TABS[c];
  const raiz = D.cortes[c].tree[0];
  const i = D.dates.length - 1;
  clicar(pillDe(c, 'medida', 'Job openings'));
  clicar(pillDe(c, 'ajuste', 'Seasonally adjusted'));
  clicar(pillDe(c, 'transform', 'Monthly'));

  const pShare = pillDe(c, 'tipo', '% of total');
  ok(pShare && !pShare.classList.contains('disabled'),
     c + ': a pill "% of total" existe e esta ligada');
  clicar(pShare);
  ok(tab.state.tipo === 'share', c + ': selecionada', tab.state.tipo);

  const vRaiz = tab.serie(raiz.key) || [];
  ok(vRaiz[i] != null && Math.abs(vRaiz[i] - 100) < 1e-9,
     c + ': a raiz (' + raiz.label + ') le 100.00 — so le se o denominador for ela mesma',
     vRaiz[i] + '');

  const filhos = raiz.children || [];
  const soma = filhos.reduce((a, n) => a + (tab.serie(n.key) || [])[i], 0);
  ok(Math.abs(soma - 100) < 0.2,
     c + ': os ' + filhos.length + ' filhos de nivel 1 somam ' + soma.toFixed(2) + '%');

  ok(tab.yTitle().indexOf(raiz.label) >= 0,
     c + ': o eixo Y nomeia o denominador (' + raiz.label + ')', tab.yTitle());

  // O acumulado tem de ficar desligado por ser PARTICIPACAO, e para provar isso a
  // medida precisa ser um FLUXO: com Job openings a pill ja estaria desligada pela
  // regra do estoque, e um bug na regra da participacao passaria em silencio (foi o
  // que um mutante mostrou).
  clicar(pillDe(c, 'medida', 'Hires'));
  const pa = pillDe(c, 'transform', '12M total');
  ok(pa && pa.classList.contains('disabled') && /share/i.test(pa.title),
     c + ': com Hires (fluxo) + participacao, "12M total" segue desligada e diz por que',
     pa ? (pa.classList.contains('disabled') ? pa.title : 'LIGADA') : 'ausente');
  const antesT = tab.state.transform;
  clicar(pa);
  ok(tab.state.transform === antesT, c + ': clicar nela nao muda o estado');
  clicar(pillDe(c, 'medida', 'Job openings'));

  // Barras LIGADAS: e o que separa participacao de taxa. Irmas dividem pelo MESMO
  // denominador, entao empilhar nao inventa total nenhum.
  const pb = pillDe(c, 'kind', 'Stacked bars');
  ok(pb && !pb.classList.contains('disabled'),
     c + ': barras LIGADAS para participacao', pb ? pb.title : 'ausente');
  clicar(pb);
  ok(tab.state.kind === 'bars', c + ': ...e selecionaveis', tab.state.kind);
  const react = ultimaReact('chart-' + c);
  const traceRaiz = react.traces.find((t) => t.name === raiz.label);
  ok(traceRaiz && traceRaiz.type === 'scatter',
     c + ': a raiz continua sendo LINHA sobre a pilha de 100%',
     traceRaiz ? traceRaiz.type : 'ausente');
  clicar(pillDe(c, 'kind', 'Lines'));

  clicar(pillDe(c, 'transform', 'Y/Y'));
  ok(/p\.p\./.test(tab.yTitle()),
     c + ': Y/Y da participacao sai em p.p., nao em %', tab.yTitle());
  clicar(pillDe(c, 'transform', 'Monthly'));
  clicar(pillDe(c, 'tipo', 'Level'));
});

// O exemplo do usuario, conferido contra os niveis do payload em vez de contra um
// literal: mining and logging como fracao das vagas de Total nonfarm.
(function () {
  const tab = R.TABS.industria;
  const i = D.dates.length - 1;
  clicar(pillDe('industria', 'medida', 'Job openings'));
  clicar(pillDe('industria', 'tipo', '% of total'));
  const num = D.series[['industria', '110099', 'JO', 'nivel', 'sa'].join('|')];
  const den = D.series[['industria', '000000', 'JO', 'nivel', 'sa'].join('|')];
  const esperado = 100 * num[i] / den[i];
  const obtido = (tab.serie('110099') || [])[i];
  ok(Math.abs(obtido - esperado) < 1e-9,
     'mining and logging: ' + obtido.toFixed(2) + '% das vagas ('
     + num[i] + ' de ' + den[i] + ')', obtido + ' vs ' + esperado);
  ok(obtido > 0.2 && obtido < 0.6,
     '...e na ordem de grandeza publicada (~0,3%)', obtido + '');
  // A media movel sai da PARTICIPACAO, nao dos niveis: a media de razoes nao e a razao
  // das medias, e trocar as duas passaria em silencio no mes corrente.
  clicar(pillDe('industria', 'transform', '3M avg'));
  const ma = (tab.serie('110099') || [])[i];
  const daShare = (100 * num[i] / den[i] + 100 * num[i - 1] / den[i - 1]
                   + 100 * num[i - 2] / den[i - 2]) / 3;
  const dosNiveis = 100 * ((num[i] + num[i - 1] + num[i - 2]) / 3)
                    / ((den[i] + den[i - 1] + den[i - 2]) / 3);
  ok(Math.abs(ma - daShare) < 1e-9, 'MM3 e a media das participacoes',
     ma + ' vs ' + daShare + ' (razao das medias daria ' + dosNiveis + ')');
  clicar(pillDe('industria', 'transform', 'Monthly'));
  clicar(pillDe('industria', 'tipo', 'Level'));
})();

// E a contraprova de que o denominador NAO e compartilhado entre os cortes.
(function () {
  const tab = R.TABS.tamanho;
  const i = D.dates.length - 1;
  clicar(pillDe('tamanho', 'medida', 'Job openings'));
  clicar(pillDe('tamanho', 'tipo', '% of total'));
  const raizT = D.cortes.tamanho.tree[0];
  const totPrivado = D.series[['tamanho', raizT.key, 'JO', 'nivel', 'sa'].join('|')][i];
  const totNonfarm = D.series[['industria', '000000', 'JO', 'nivel', 'sa'].join('|')][i];
  ok(totPrivado < totNonfarm,
     'a raiz do corte de tamanho (' + totPrivado + ') e menor que Total nonfarm ('
     + totNonfarm + ')');
  const soma = (raizT.children || []).reduce((a, n) => a + (tab.serie(n.key) || [])[i], 0);
  const somaErrada = 100 * totPrivado / totNonfarm;
  ok(Math.abs(soma - 100) < 0.05 && Math.abs(soma - somaErrada) > 5,
     'as classes de tamanho somam ' + soma.toFixed(2) + '% e nao ' + somaErrada.toFixed(2)
     + '% — o denominador e Total private', soma + '');
  clicar(pillDe('tamanho', 'tipo', 'Level'));
})();

// ── 6c. diferenca M/M ──────────────────────────────────────────────────────
// M/M e uma DIFERENCA nos tres tipos. O erro que estas asserções existem para pegar e
// ela sair como variacao PERCENTUAL no nivel: +89 mil vagas lido como +89% e um numero
// plausivel num grafico e um absurdo na leitura.
secao('6c. A diferenca M/M');
(function () {
  const chave = ['industria', '000000', 'JO', 'nivel', 'sa'].join('|');
  const bruta = D.series[chave];
  const mm = R.serieTransformada(chave, 'mm', false);
  const i = bruta.length - 1;
  ok(mm[0] === null, 'M/M: o primeiro mes e nulo (nao ha mes anterior)', mm[0] + '');
  ok(mm[1] === bruta[1] - bruta[0], 'M/M: o segundo mes ja tem a diferenca');
  // O literal da manchete do release de julho/2026.
  ok(mm[i] === 89, 'total nonfarm openings: M/M = +89 mil em jul/2026 (7.271 - 7.182)',
     mm[i] + '');
  ok(Math.abs(mm[i]) > 10,
     '...e e uma diferenca em mil, nao uma variacao % (que seria ' +
     (100 * (bruta[i] / bruta[i - 1] - 1)).toFixed(2) + ')');
  // As outras cinco medidas, contra o proprio release.
  const esperado = {HI: -278, TS: -265, QU: -157, LD: -119, OS: 10};
  Object.keys(esperado).forEach((med) => {
    const k = ['industria', '000000', med, 'nivel', 'sa'].join('|');
    const v = R.serieTransformada(k, 'mm', false);
    ok(v[i] === esperado[med],
       med + ': M/M = ' + (esperado[med] > 0 ? '+' : '') + esperado[med] + ' mil em jul/2026',
       v[i] + '');
  });
  // Aditividade: a diferenca das partes soma a diferenca do total. E o que autoriza a
  // barra empilhada em M/M.
  const filhos = D.cortes.industria.tree[0].children.map((n) =>
    R.serieTransformada(['industria', n.key, 'JO', 'nivel', 'sa'].join('|'), 'mm', false));
  const soma = filhos.reduce((a, v) => a + v[i], 0);
  ok(Math.abs(soma - mm[i]) <= 1.5,
     'as partes somam a diferenca do total (' + soma + ' vs ' + mm[i] + ', tolerancia de arredondamento)');
})();
CORTES.forEach((c) => {
  const tab = R.TABS[c];
  const raiz = D.cortes[c].tree[0];
  clicar(pillDe(c, 'medida', 'Job openings'));
  clicar(pillDe(c, 'ajuste', 'Seasonally adjusted'));

  // Nivel: mil, e o eixo NAO pode dizer "%".
  clicar(pillDe(c, 'tipo', 'Level'));
  const pmm = pillDe(c, 'transform', 'M/M');
  ok(pmm && !pmm.classList.contains('disabled'), c + ': a pill "M/M" existe e esta ligada');
  clicar(pmm);
  ok(tab.state.transform === 'mm', c + ': selecionada', tab.state.transform);
  let yt = tab.yTitle();
  ok(/thousands/.test(yt) && !/%/.test(yt),
     c + ': no nivel o eixo diz mil e NAO diz %', yt);
  ok(/previous month/.test(yt), c + ': ...e diz contra que mes', yt);

  // Barras seguem valendo: a diferenca de coisas que somam soma.
  let pb = pillDe(c, 'kind', 'Stacked bars');
  ok(pb && !pb.classList.contains('disabled'),
     c + ': M/M no nivel permite barras empilhadas', pb ? pb.title : 'ausente');

  // Taxa e participacao: p.p.
  clicar(pillDe(c, 'tipo', 'Rate'));
  ok(tab.state.transform === 'mm', c + ': M/M sobrevive a troca para Rate', tab.state.transform);
  yt = tab.yTitle();
  ok(/p\.p\./.test(yt) && /previous month/.test(yt),
     c + ': na taxa o eixo sai em p.p.', yt);
  pb = pillDe(c, 'kind', 'Stacked bars');
  ok(pb && pb.classList.contains('disabled'),
     c + ': ...e as barras seguem desligadas na taxa (o denominador e por categoria)');

  clicar(pillDe(c, 'tipo', '% of total'));
  yt = tab.yTitle();
  ok(/p\.p\./.test(yt) && /previous month/.test(yt),
     c + ': na participacao tambem sai em p.p.', yt);
  // O M/M da participacao e a diferenca das participacoes, nao a participacao da
  // diferenca -- e a mesma armadilha da MM3, por outro caminho.
  const i = D.dates.length - 1;
  const num = D.series[[c, raiz.children[0].key, 'JO', 'nivel', 'sa'].join('|')];
  const den = D.series[[c, raiz.key, 'JO', 'nivel', 'sa'].join('|')];
  const daShare = 100 * num[i] / den[i] - 100 * num[i - 1] / den[i - 1];
  const obtido = (tab.serie(raiz.children[0].key) || [])[i];
  ok(Math.abs(obtido - daShare) < 1e-9,
     c + ': M/M da participacao e a diferenca das participacoes', obtido + ' vs ' + daShare);
  pb = pillDe(c, 'kind', 'Stacked bars');
  ok(pb && !pb.classList.contains('disabled'),
     c + ': ...e as barras VALEM na participacao (irmas dividem pelo mesmo total)');

  clicar(pillDe(c, 'tipo', 'Level'));
  clicar(pillDe(c, 'transform', 'Monthly'));
  clicar(pillDe(c, 'kind', 'Lines'));
});

// ── 7. transformacoes ───────────────────────────────────────────────────────
secao('7. As transformacoes de leitura');
(function () {
  const chave = ['industria', '000000', 'HI', 'nivel', 'sa'].join('|');
  const bruta = D.series[chave];
  const ma3 = R.serieTransformada(chave, 'ma3', false);
  const ma12 = R.serieTransformada(chave, 'ma12', false);
  const sum12 = R.serieTransformada(chave, 'sum12', false);
  // Janela incompleta mostra NADA -- convencao de analytics/metric_layers.md.
  ok(ma3.slice(0, 2).every((v) => v === null) && ma3[2] !== null,
     'MM3: os 2 primeiros meses sao nulos, o 3o ja tem valor');
  ok(ma12.slice(0, 11).every((v) => v === null) && ma12[11] !== null,
     'MM12: os 11 primeiros sao nulos, o 12o ja tem valor');
  const i = bruta.length - 1;
  ok(Math.abs(ma3[i] - (bruta[i] + bruta[i - 1] + bruta[i - 2]) / 3) < 1e-9,
     'MM3 e a media dos 3 ultimos, exata');
  ok(Math.abs(sum12[i] - ma12[i] * 12) < 1e-6,
     'acumulado 12M = MM12 x 12, exato');

  // Y/Y: % para nivel, p.p. para taxa. Sao coisas diferentes, e o erro de tratar as
  // duas como % passa desapercebido porque as duas saem "por volta de 0".
  const yoyNivel = R.serieTransformada(chave, 'yoy', false);
  ok(Math.abs(yoyNivel[i] - (bruta[i] / bruta[i - 12] - 1) * 100) < 1e-9,
     'Y/Y de nivel e variacao percentual');
  const chaveTaxa = ['industria', '000000', 'HI', 'taxa', 'sa'].join('|');
  const brutaTaxa = D.series[chaveTaxa];
  const yoyTaxa = R.serieTransformada(chaveTaxa, 'yoy', true);
  ok(Math.abs(yoyTaxa[i] - (brutaTaxa[i] - brutaTaxa[i - 12])) < 1e-9,
     'Y/Y de taxa e diferenca em p.p., nao variacao percentual');
  ok(yoyNivel.slice(0, 12).every((v) => v === null),
     'Y/Y: os 12 primeiros meses sao nulos');
})();

// ── 8. cores ────────────────────────────────────────────────────────────────
secao('8. Cores das series');
ok(R.PALETTE.length === 14, 'paleta de 14 cores', R.PALETTE.length + '');
(function () {
  let piorPar = null, pior = Infinity;
  for (let i = 0; i < R.PALETTE.length; i++) {
    for (let j = i + 1; j < R.PALETTE.length; j++) {
      const d = deltaE(R.PALETTE[i], R.PALETTE[j]);
      if (d < pior) { pior = d; piorPar = R.PALETTE[i] + ' x ' + R.PALETTE[j]; }
    }
  }
  ok(pior >= 20, 'o pior par da paleta fecha em dE2000 ' + pior.toFixed(1) + ' (>= 20)', piorPar);
})();
CORTES.forEach((c) => {
  const tab = R.TABS[c];
  clicar(pillDe(c, 'medida', 'Job openings'));
  clicar(pillDe(c, 'tipo', 'Level'));
  clicar(pillDe(c, 'kind', 'Lines'));
  const react = ultimaReact('chart-' + c);
  // Por GRAFICO: nenhum par de traces com o mesmo tracejado abaixo de 20.
  const cores = react.traces.map((t) => ({
    cor: (t.line && t.line.color) || (t.marker && t.marker.color),
    dash: (t.line && t.line.dash) || 'solid',
    nome: t.name,
  }));
  let pior = Infinity, piorPar = null;
  for (let i = 0; i < cores.length; i++) {
    for (let j = i + 1; j < cores.length; j++) {
      if (cores[i].dash !== cores[j].dash) continue;
      const d = deltaE(cores[i].cor, cores[j].cor);
      if (d < pior) { pior = d; piorPar = cores[i].nome + ' x ' + cores[j].nome; }
    }
  }
  ok(cores.length < 2 || pior >= 20,
     c + ': vista default, ' + cores.length + ' series, pior par dE2000 '
     + (pior === Infinity ? 'n/a' : pior.toFixed(1)), piorPar);
  ok(cores[0].cor === R.PALETTE[0],
     c + ': a raiz usa PALETTE[0] (navy da marca), reservado ao agregado', cores[0].cor);
});
// Marca TODAS as linhas: nenhuma vista default chega a 13 series, entao um teste que
// so olhe a inicial passa mesmo com o `dash` removido (verificado num mutante em
// outro relatorio deste projeto).
(function () {
  const tab = R.TABS.industria;
  R.achatar(D.cortes.industria.tree).forEach((n) => { tab.state.checked[n.key] = true; });
  Object.keys(tab.state.checked).forEach((k) => { tab.state.expanded[k] = true; });
  tab.redraw();
  const react = ultimaReact('chart-industria');
  ok(react.traces.length === 28, 'industria com tudo marcado: 28 series', react.traces.length + '');
  const dashes = {};
  react.traces.forEach((t) => { dashes[(t.line && t.line.dash) || 'solid'] = true; });
  ok(Object.keys(dashes).length > 1,
     'acima de 13 series o segundo canal entra: ' + Object.keys(dashes).join(', '));
  let pior = Infinity, piorPar = null;
  const cs = react.traces.map((t) => ({ cor: t.line.color, dash: t.line.dash || 'solid', nome: t.name }));
  for (let i = 0; i < cs.length; i++) {
    for (let j = i + 1; j < cs.length; j++) {
      if (cs[i].dash !== cs[j].dash) continue;
      const d = deltaE(cs[i].cor, cs[j].cor);
      if (d < pior) { pior = d; piorPar = cs[i].nome + ' x ' + cs[j].nome; }
    }
  }
  ok(pior >= 20, '28 series: pior par de mesmo tracejado dE2000 ' + pior.toFixed(1), piorPar);
  // Volta ao default para as secoes seguintes.
  R.achatar(D.cortes.industria.tree).forEach((n) => { delete tab.state.checked[n.key]; });
  const raiz = D.cortes.industria.tree[0];
  tab.state.checked[raiz.key] = true;
  (raiz.children || []).forEach((n) => { tab.state.checked[n.key] = true; });
  tab.redraw();
})();

// ── 9. cartoes de definicao ─────────────────────────────────────────────────
secao('9. Cartoes de definicao');
(function () {
  // Toda chave do INFO resolve contra uma linha/pill real. Uma chave errada produz um
  // botao que nunca nasce: sem erro, sem lacuna visivel.
  const validas = {};
  D.ordemMedidas.forEach((m) => { validas['medida:' + m] = true; });
  CORTES.forEach((c) => R.achatar(D.cortes[c].tree).forEach((n) => { validas[c + ':' + n.key] = true; }));
  // A CES e a CPS entraram em 2026-09-01: o resolvedor tem de conhecer as tres fontes,
  // senao 900 chaves legitimas passam por orfas e a assercao deixa de valer para todas.
  Object.keys(D.ces.medidas).forEach((m) => { validas['medida_ces:' + m] = true; });
  Object.keys(D.ces.abas).forEach((a) => {
    R.achatar(D.ces.abas[a].tree).forEach((n) => { validas['ces:' + n.key] = true; });
  });
  D.cps.blocos.forEach((b) => b.linhas.forEach((l) => { validas['cps:' + l.key] = true; }));
  const orfas = Object.keys(D.info).filter((k) => !validas[k]);
  ok(!orfas.length, 'zero chaves orfas (' + Object.keys(D.info).length + ' entradas)', orfas.join(', '));

  // A tabela renderizada: casa linha com no por POSICAO, nunca por rotulo -- "Total
  // private" e "Total US" aparecem em mais de um corte.
  CORTES.forEach((c) => {
    const tab = R.TABS[c];
    R.achatar(D.cortes[c].tree).forEach((n) => { tab.state.expanded[n.key] = true; });
    tab.redraw();
    const tbody = doc.getElementById('tb-' + c);
    const nos = R.flattenHierRows(D.cortes[c].tree, tab.state.expanded, 0).map((r) => r.node);
    ok(tbody.children.length === nos.length,
       c + ': ' + tbody.children.length + ' linhas renderizadas == ' + nos.length + ' nos da arvore');
    let comBotao = 0, semEntrada = 0;
    tbody.children.forEach((tr, i) => {
      const tdl = tr.children.find((td) => td.classList.contains('col-label'));
      const btn = tdl.children.find((x) => x.classList && x.classList.contains('info-btn'));
      const temEntrada = !!D.info[c + ':' + nos[i].key];
      if (btn) comBotao++;
      if (!temEntrada) semEntrada++;
      if (!!btn !== temEntrada) {
        ok(false, c + '/' + nos[i].key + ': botao ' + (btn ? 'presente' : 'ausente')
                  + ' mas entrada ' + (temEntrada ? 'presente' : 'ausente'));
      }
      // O rotulo limpo nao pode incluir o "i" do botao.
      const limpo = rotuloLimpo(tdl);
      if (limpo !== nos[i].label) {
        ok(false, c + '/' + nos[i].key + ': rotulo lido "' + limpo + '" != "' + nos[i].label + '"');
      }
    });
    ok(comBotao === nos.length - semEntrada,
       c + ': ' + comBotao + ' linhas com botao `i`, ' + semEntrada + ' sem entrada no mapa');
  });

  // O namespace nao e enfeite: tamanho:00 e regiao:00 sao a MESMA categoria com
  // significados diferentes, e um mapa de chave nua faria um explicar o outro.
  ok(D.info['tamanho:00'] && D.info['regiao:00']
     && D.info['tamanho:00'].desc !== D.info['regiao:00'].desc,
     'tamanho:00 e regiao:00 tem textos diferentes');
  ok(/private/i.test(D.info['tamanho:00'].desc),
     '  e o de tamanho avisa que a raiz e so o setor privado');

  // `full` so entra quando difere do rotulo visivel.
  const labels = {};
  D.ordemMedidas.forEach((m) => { labels['medida:' + m] = D.medidas[m].label; });
  CORTES.forEach((c) => R.achatar(D.cortes[c].tree).forEach((n) => { labels[c + ':' + n.key] = n.label; }));
  Object.keys(D.ces.medidas).forEach((m) => { labels['medida_ces:' + m] = D.ces.medidas[m].label; });
  Object.keys(D.ces.abas).forEach((a) => {
    R.achatar(D.ces.abas[a].tree).forEach((n) => { labels['ces:' + n.key] = n.label; });
  });
  D.cps.blocos.forEach((b) => b.linhas.forEach((l) => { labels['cps:' + l.key] = l.label; }));
  const repetidos = Object.keys(D.info).filter((k) => D.info[k].full && D.info[k].full === labels[k]);
  ok(!repetidos.length, 'nenhum `full` repete o rotulo visivel', repetidos.join(', '));

  // A unidade do cartao vem da MESMA funcao que titula o eixo Y -- se ficar fixa,
  // passa a mentir no primeiro clique.
  const tab = R.TABS.industria;
  clicar(pillDe('industria', 'medida', 'Quits'));
  clicar(pillDe('industria', 'tipo', 'Rate'));
  const unidadeTaxa = tab.yTitle();
  clicar(pillDe('industria', 'tipo', 'Level'));
  const unidadeNivel = tab.yTitle();
  ok(unidadeTaxa !== unidadeNivel && /employment/.test(unidadeTaxa) && /thousands/.test(unidadeNivel),
     'a unidade acompanha o seletor: "' + unidadeTaxa + '" x "' + unidadeNivel + '"');
})();

// ── 10. cabecalho do grafico ────────────────────────────────────────────────
secao('10. Cabecalho do grafico');
CORTES.forEach((c) => {
  clicar(pillDe(c, 'medida', 'Quits'));
  clicar(pillDe(c, 'tipo', 'Rate'));
  clicar(pillDe(c, 'ajuste', 'Not adjusted'));
  clicar(pillDe(c, 'transform', 'Monthly'));
  const t = doc.getElementById('ct-' + c).textContent;
  const s = doc.getElementById('cs-' + c).textContent;
  const src = doc.getElementById('cr-' + c).textContent;
  ok(/^Quits/.test(t), c + ': o titulo acompanha a medida ("' + t + '")');
  ok(/Not adjusted/.test(s), c + ': o subtitulo diz o ajuste selecionado', s);
  ok(/quits \/ employment, %/.test(s), c + ': ...e a unidade, igual a do eixo Y', s);
  ok(/^Source: BLS/.test(src) && /to /.test(src), c + ': a linha de fonte tem fonte e periodo', src);
  // O periodo sai da extensao REAL do plotado: na visao Y/Y o grafico comeca um ano
  // depois, e tem de dizer isso.
  const mensal = /· (\w+ \d{4}) to/.exec(src)[1];
  clicar(pillDe(c, 'transform', 'Y/Y'));
  const yoy = /· (\w+ \d{4}) to/.exec(doc.getElementById('cr-' + c).textContent)[1];
  ok(mensal !== yoy && Date.parse(yoy) > Date.parse(mensal),
     c + ': na visao Y/Y o periodo comeca depois (' + mensal + ' -> ' + yoy + ')');
  clicar(pillDe(c, 'transform', 'Monthly'));
  clicar(pillDe(c, 'ajuste', 'Seasonally adjusted'));
});
// Acima de 3 series o subtitulo conta em vez de listar (a legenda embaixo do plot ja
// esta no print).
(function () {
  const s = doc.getElementById('cs-industria').textContent;
  ok(/\d+ series \(see legend\)/.test(s) || /,/.test(s),
     'subtitulo de industria com 12 series marcadas: "' + s + '"');
})();

// ── 11. o payload contra o release ──────────────────────────────────────────
secao('11. O payload reproduz o release de julho/2026');
(function () {
  const i = D.dates.length - 1;
  // Tabela A (JO/HI/TS) e Tabelas 4/5/6 (QU/LD/OS) do release de julho/2026, coluna
  // "July 2026p", total nonfarm, SA.
  const esperado = {
    JO: [7271, 4.4], HI: [5054, 3.2], TS: [5072, 3.2],
    QU: [3056, 1.9], LD: [1666, 1.0], OS: [350, 0.2],
  };
  Object.keys(esperado).forEach((m) => {
    const niv = D.series[['industria', '000000', m, 'nivel', 'sa'].join('|')][i];
    const tax = D.series[['industria', '000000', m, 'taxa', 'sa'].join('|')][i];
    ok(niv === esperado[m][0] && Math.abs(tax - esperado[m][1]) < 1e-9,
       m + ': ' + niv + 'k / ' + tax + '% (release: ' + esperado[m][0] + 'k / ' + esperado[m][1] + '%)');
  });
  // A raiz do corte de tamanho e Total private, 810 mil menor.
  const jo_i = D.series[['industria', '000000', 'JO', 'nivel', 'sa'].join('|')][i];
  const jo_t = D.series[['tamanho', '00', 'JO', 'nivel', 'sa'].join('|')][i];
  ok(jo_i - jo_t === 810, 'a raiz de tamanho e 810k menor que a de industria (governo)',
     jo_i + ' - ' + jo_t);
  // Aditividade no que o navegador de fato recebeu.
  const filhos = (D.cortes.industria.tree[0].children || []).map((n) => n.key);
  const soma = filhos.reduce((acc, k) =>
    acc + D.series[['industria', k, 'JO', 'nivel', 'sa'].join('|')][i], 0);
  ok(Math.abs(soma - jo_i) <= 1.5,
     'os filhos da raiz somam a raiz no payload (' + soma + ' x ' + jo_i + ')');
})();

// ── 12. formatacao ──────────────────────────────────────────────────────────
secao('12. Formatacao americana');
ok(R.fmtNum(7271, 0) === '7,271', 'virgula de milhar, ponto decimal: 7271 -> ' + R.fmtNum(7271, 0));
ok(R.fmtNum(4.4, 1) === '4.4', '4.4 -> ' + R.fmtNum(4.4, 1));
ok(R.fmtNum(null, 1) === '—', 'nulo -> travessao');
ok(R.fmtNum(-177, 0) === '−177', 'negativo com sinal tipografico: ' + R.fmtNum(-177, 0));

// ── 13. a CES (payroll) ────────────────────────────────────────────────────
secao('13. A CES — payroll, horas e ganhos');
(function () {
  ok(!!R.TABS.ces_emprego && !!R.TABS.ces_horas, 'as 2 abas da CES foram construidas');
  const emp = D.ces.abas.emprego, hor = D.ces.abas.horas;
  // As raizes sao DIFERENTES, e e isso que justifica duas abas: a CES nao publica
  // horas nem ganhos de governo.
  ok(emp.raiz === '00000000' && hor.raiz === '05000000',
     'emprego enraiza em Total nonfarm e horas/ganhos em Total private',
     emp.raiz + ' / ' + hor.raiz);
  const i = D.ces.dates.length - 1;
  function val(cat, med, adj) {
    const s = D.ces.series[[cat, med, adj].join('|')];
    if (!s) return null;
    const k = i - s.i0;
    return (k >= 0 && k < s.v.length) ? s.v[k] : null;
  }
  // Contra o release de julho/2026 (tabela B-1 e Summary table B).
  const lit = {'00000000': 158858, '05000000': 135588, '06000000': 21561,
               '08000000': 114027, '90000000': 23270, '20000000': 8343,
               '30000000': 12611, '10000000': 607};
  Object.keys(lit).forEach((cat) => {
    ok(val(cat, 'emprego', 'sa') === lit[cat],
       'B-1 ' + cat + ': ' + lit[cat] + ' mil empregos em jul/2026', val(cat, 'emprego', 'sa') + '');
  });
  ok(Math.abs(val('05000000', 'ganho_hora', 'sa') - 37.62) < 0.005,
     'Summary table B: ganho medio/hora do setor privado = US$ 37,62',
     val('05000000', 'ganho_hora', 'sa') + '');
  ok(Math.abs(val('05000000', 'horas_semana', 'sa') - 34.3) < 0.05,
     'Summary table B: horas semanais medias = 34,3', val('05000000', 'horas_semana', 'sa') + '');
  ok(Math.abs(val('05000000', 'ganho_semana', 'sa') - 1290.37) < 0.02,
     'Summary table B: ganho medio/semana = US$ 1.290,37',
     val('05000000', 'ganho_semana', 'sa') + '');
  // As identidades do topo, no dado que o relatorio mostra.
  ok(val('05000000', 'emprego', 'sa') + val('90000000', 'emprego', 'sa')
     === val('00000000', 'emprego', 'sa'),
     'privado + governo = total nonfarm, exato');
  ok(val('06000000', 'emprego', 'sa') + val('08000000', 'emprego', 'sa')
     === val('05000000', 'emprego', 'sa'),
     'bens + servico privado = total privado, exato');

  // Uma MEDIA por trabalhador nao soma entre industrias: barras e "% do total" saem.
  const t = R.TABS.ces_horas;
  clicar(pillDe('ces-horas', 'medida', 'Hourly earnings'));
  ok(t.tiposDisponiveis().length === 1,
     'ganho medio/hora nao oferece "% do total"',
     t.tiposDisponiveis().map((x) => x.key).join(','));
  ok(!t.barrasOk(), '...e nao oferece barras empilhadas');
  let pb = pillDe('ces-horas', 'kind', 'Stacked bars');
  ok(pb && pb.classList.contains('disabled') && /average per worker|weighted/i.test(pb.title),
     '...com o motivo no title', pb ? pb.title : 'ausente');
  // O agregado em milhares de horas soma: barras e participacao voltam.
  clicar(pillDe('ces-horas', 'medida', 'Aggregate weekly hours'));
  ok(t.tiposDisponiveis().length === 2, 'horas agregadas oferecem "% do total"');
  ok(t.barrasOk(), '...e barras empilhadas');
  // Indice nao soma, e o motivo diz o que fazer.
  clicar(pillDe('ces-horas', 'medida', 'Index of aggregate hours'));
  pb = pillDe('ces-horas', 'kind', 'Stacked bars');
  ok(pb && pb.classList.contains('disabled') && /index/i.test(pb.title),
     'o indice 2007=100 nao empilha, e o title explica', pb ? pb.title : 'ausente');
  // Nada na CES acumula em 12 meses.
  const pa = pillDe('ces-horas', 'transform', '12M total');
  ok(pa && pa.classList.contains('disabled') && /stock|weekly/i.test(pa.title),
     '"12M total" desligada em toda a CES, com o motivo', pa ? pa.title : 'ausente');
  clicar(pillDe('ces-horas', 'medida', 'Weekly hours'));
})();

// ── 14. a CPS (domiciliar) ─────────────────────────────────────────────────
secao('14. A CPS — pesquisa domiciliar');
(function () {
  ['status', 'taxa_grupo', 'composicao', 'alternativa'].forEach((b) => {
    ok(!!R.TABS['cps_' + b], 'bloco ' + b + ' construido');
  });
  const i = D.cps.dates.length - 1;
  function val(cat, adj) {
    const s = D.cps.series[[cat, adj].join('|')];
    if (!s) return null;
    const k = i - s.i0;
    return (k >= 0 && k < s.v.length) ? s.v[k] : null;
  }
  // Summary table A de julho/2026.
  const lit = {ocupados: 162177, desocupados: 6916, forca_trabalho: 169094,
               fora_forca: 106189, taxa_desemprego: 4.1, participacao: 61.4,
               razao_emprego_pop: 58.9, u6: 7.9};
  Object.keys(lit).forEach((k) => {
    ok(Math.abs(val(k, 'sa') - lit[k]) < 0.051,
       'Summary table A ' + k + ' = ' + lit[k], val(k, 'sa') + '');
  });
  ok(val('populacao', 'nsa') === 275282,
     'a populacao vem so sem ajuste sazonal, e bate: 275.282',
     val('populacao', 'nsa') + '');
  ok(val('populacao', 'sa') === null,
     '...e nao existe versao ajustada dela (o BLS nao publica)');
  // Aditividade do bloco de status.
  // NAO e exato, e a nota de pe da propria Summary table A diz por que: "detail ...
  // will not necessarily add to totals because of the independent seasonal adjustment
  // of the various series". Em jul/2026 sao 162.177 + 6.916 = 169.093 contra 169.094
  // publicados. Mesmo efeito que faz a arvore da CES ser validada no dado bruto.
  const somaFT = val('ocupados', 'sa') + val('desocupados', 'sa');
  ok(Math.abs(somaFT - val('forca_trabalho', 'sa')) <= 1,
     'ocupados + desocupados = forca de trabalho a menos de 1 mil (o ajuste sazonal e '
     + 'independente por serie)', somaFT + ' vs ' + val('forca_trabalho', 'sa'));
  ok(Math.abs(val('ocupados', 'nsa') + val('desocupados', 'nsa')
              - val('forca_trabalho', 'nsa')) <= 1,
     '...e no dado bruto tambem fecha');
  // O buraco de outubro/2025 esta PRESERVADO e no lugar certo.
  const s = D.cps.series['ocupados|sa'];
  const iOut = D.cps.dates.indexOf('2025-10-01');
  ok(iOut > 0 && s.v[iOut - s.i0] === null,
     'outubro/2025 e um null NO LUGAR, nao um mes removido',
     'valor em ' + iOut + ': ' + s.v[iOut - s.i0]);
  ok(s.v[iOut - s.i0 - 1] === 163656 && s.v[iOut - s.i0 + 1] === 163760,
     '...e os vizinhos sao setembro (163.656) e novembro (163.760)');
  // Blocos nao aditivos nao oferecem barras nem participacao.
  ['taxa_grupo', 'alternativa'].forEach((b) => {
    const t = R.TABS['cps_' + b];
    ok(!t.barrasOk(), b + ': sem barras empilhadas (cada linha tem sua propria base)');
    ok(t.tiposDisponiveis().length === 1, b + ': sem "% do total"');
  });
  ok(R.TABS.cps_status.barrasOk(), 'status: com barras (o bloco e aditivo)');
  // A composicao filtra por eixo: os dois cortes nunca aparecem juntos.
  const tc = R.TABS.cps_composicao;
  const antes = tc.specs().length;
  clicar(pillDe('cps-composicao', 'eixo', 'By duration'));
  ok(tc.state.eixo === 'duracao', 'o pill de corte troca o eixo', tc.state.eixo);
  const nomes = tc.specs().map((x) => x.name).join('|');
  ok(!/Job losers|Reentrants/.test(nomes),
     'com o corte por duracao, nenhuma linha de motivo e plotada', nomes);
  clicar(pillDe('cps-composicao', 'eixo', 'By reason'));
})();

// ── 15. as derivadas ───────────────────────────────────────────────────────
secao('15. As metricas derivadas');
(function () {
  const DV = D.derivadas;
  ok(!!R.TABS.derivadas, 'a aba de derivadas foi construida');
  ok(DV.vuAferido.n > 300 && DV.vuAferido.erroMax <= 0.05,
     'vagas/desempregado conferida contra o BLS em ' + DV.vuAferido.n
     + ' meses, erro max ' + DV.vuAferido.erroMax + ' (o BLS publica com 1 decimal)');
  // A razao e vagas POR desempregado, nao o contrario: hoje ela esta perto de 1, mas
  // em 2009 era 0,15 -- e o reciproco seria 6,5. Uma inversao passaria batida hoje.
  const vu = DV.vu, g = DV.grade;
  const iJul09 = g.indexOf('2009-07-01');
  const v09 = vu.v[g.indexOf(vu.i0) === -1 ? -1 : (iJul09 - g.indexOf(vu.i0))];
  ok(v09 !== undefined && v09 !== null && v09 > 0.10 && v09 < 0.20,
     'jul/2009: 0,15 vaga por desempregado (o reciproco, 6,5, seria a serie do BLS)',
     v09 + '');
  const ult = vu.v[vu.v.length - 1];
  ok(ult > 0.8 && ult < 1.4, 'no fim da serie a razao esta perto de 1', ult + '');
  // A curva de Beveridge nao tem regua de tempo: o X dela nao e tempo.
  ok(/rb-dv-bev/.test(CRU), 'o card da Beveridge tem o div da regua na marcacao');
  const relBev = relayoutsDe('chart-dv-bev').filter(
    (c) => c.upd && c.upd['xaxis.range']);
  ok(!relBev.length,
     'mas nenhuma janela de data e aplicada nele (o X sao taxas, nao meses)',
     relBev.length + ' relayouts de xaxis.range');
  // Os outros tres SAO series temporais e recebem a janela.
  ['dv-vu', 'dv-liq', 'dv-div'].forEach((d) => {
    const r = relayoutsDe('chart-' + d).filter((c) => c.upd && c.upd['xaxis.range']);
    ok(r.length >= 1, d + ': a primeira pintura aplica uma janela de data');
  });
  // O pill de periodo da Beveridge muda o numero de pontos plotados.
  const antes = (ultimaReact('chart-dv-bev').traces[0].x || []).length;
  clicar(pillDe('dv-bev', 'opt', '2020 on'));
  const depois = (ultimaReact('chart-dv-bev').traces[0].x || []).length;
  ok(depois > 0 && depois < antes,
     'o pill de periodo recorta a nuvem (' + antes + ' -> ' + depois + ' pontos)');
  clicar(pillDe('dv-bev', 'opt', 'All'));
})();

// ── resumo ──────────────────────────────────────────────────────────────────
console.log('\n' + '='.repeat(66));
console.log((asserts - falhas) + '/' + asserts + ' assercoes ok'
            + (falhas ? ', ' + falhas + ' FALHAS' : ''));
process.exit(falhas ? 1 : 0);
