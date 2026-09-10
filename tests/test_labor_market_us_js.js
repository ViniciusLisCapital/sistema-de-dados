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
function eq(a, b, nome) {
  ok(a === b, nome, 'esperado ' + JSON.stringify(b) + ', veio ' + JSON.stringify(a));
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
                 'dataExtent', 'assignSeriesColors', 'VALORES', '_RANGE_MEM', 'fmtNum',
                 'fmtQuarter', 'fmtQuarterShort',
                 // as 7 camadas de metrica (piloto na aba de emprego da CES)
                 '_dif', '_pctv', '_aplicarCamadas', 'camadasDe', 'unitCamadas',
                 'CAMADA_COMPARA', 'CAMADA_SUAVIZA', 'larguraPills', 'PILL_MAX_PX'];
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
// Um grupo de opcoes pode estar em pills ou num <select>, decidido pela largura --
// entao o helper que escolhe uma opcao tem de servir os dois, ou cada asserção passa a
// depender do formato em vez do comportamento.
function grupoSel(pref, grupo) {
  return doc.getElementById('pg-' + pref + '-' + grupo).children
    .find((c) => c.tag === 'select') || null;
}
function opcoesDoGrupo(pref, grupo) {
  const s = grupoSel(pref, grupo);
  if (s) return s.children.map((o) => o.textContent);
  return pills(pref, grupo).map(pillLabel);
}
function escolherNoGrupo(pref, grupo, label) {
  const s = grupoSel(pref, grupo);
  if (s) {
    const op = s.children.find((o) => o.textContent === label);
    if (!op) throw new Error('opcao inexistente em ' + pref + '/' + grupo + ': ' + label);
    s.value = op.value; s.fire('change'); return;
  }
  clicar(pillDe(pref, grupo, label));
}
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
const ABAS_ESPERADAS = ['Payroll', 'Household', 'JOLTS', 'Productivity',
                        'Derived', 'Appendix'];
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
  escolherNoGrupo(c, 'medida', 'Job openings');
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
  escolherNoGrupo(c, 'medida', 'Hires');
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
  escolherNoGrupo(c, 'medida', 'Job openings');
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
  escolherNoGrupo(c, 'medida', 'Job openings');
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
  escolherNoGrupo(c, 'medida', 'Job openings');
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
  escolherNoGrupo(c, 'medida', 'Hires');
  const pa = pillDe(c, 'transform', '12M total');
  ok(pa && pa.classList.contains('disabled') && /share/i.test(pa.title),
     c + ': com Hires (fluxo) + participacao, "12M total" segue desligada e diz por que',
     pa ? (pa.classList.contains('disabled') ? pa.title : 'LIGADA') : 'ausente');
  const antesT = tab.state.transform;
  clicar(pa);
  ok(tab.state.transform === antesT, c + ': clicar nela nao muda o estado');
  escolherNoGrupo(c, 'medida', 'Job openings');

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
  escolherNoGrupo('industria', 'medida', 'Job openings');
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
  escolherNoGrupo('tamanho', 'medida', 'Job openings');
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
  escolherNoGrupo(c, 'medida', 'Job openings');
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
  escolherNoGrupo(c, 'medida', 'Job openings');
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
  // A produtividade entrou em 2026-09-03, com DOIS namespaces proprios: `emprego` e
  // `horas_semana` existem na CES e aqui medindo coisas diferentes (a CES conta empregos
  // em folha; esta pesquisa conta pessoas, incluindo conta propria), entao um mapa de
  // chave nua faria um cartao explicar o outro sem erro nenhum.
  R.achatar(D.prod.setores).forEach((n) => { validas['setor:' + n.key] = true; });
  Object.keys(D.prod.medidas).forEach((m) => { validas['medida_prod:' + m] = true; });
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
  R.achatar(D.prod.setores).forEach((n) => { labels['setor:' + n.key] = n.label; });
  Object.keys(D.prod.medidas).forEach((m) => {
    labels['medida_prod:' + m] = D.prod.medidas[m].label;
  });
  const repetidos = Object.keys(D.info).filter((k) => D.info[k].full && D.info[k].full === labels[k]);
  ok(!repetidos.length, 'nenhum `full` repete o rotulo visivel', repetidos.join(', '));

  // A unidade do cartao vem da MESMA funcao que titula o eixo Y -- se ficar fixa,
  // passa a mentir no primeiro clique.
  const tab = R.TABS.industria;
  escolherNoGrupo('industria', 'medida', 'Quits');
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
  escolherNoGrupo(c, 'medida', 'Quits');
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
  // GABARITO: o release de AGOSTO/2026 (divulgado 04/09/2026), tabela B-1 e Summary
  // table B. Estas literais sao a ponta da serie, entao elas ENVELHECEM a cada
  // divulgacao -- por duas razoes, e a segunda nao e obvia: (a) a ponta anda, e (b) o
  // Employment Situation REVISA os dois meses anteriores, entao nem fixar o mes
  // salvaria as literais. Julho saiu a 158.858 no proprio release de julho e esta
  // reimpresso a 158.913 no de agosto. Ao atualizar, copie do release publicado --
  // nunca do nosso proprio banco, que e justamente o que se quer conferir.
  const lit = {'00000000': 159075, '05000000': 135752, '06000000': 21606,
               '08000000': 114146, '90000000': 23323, '20000000': 8359,
               '30000000': 12638, '10000000': 609};
  Object.keys(lit).forEach((cat) => {
    ok(val(cat, 'emprego', 'sa') === lit[cat],
       'B-1 ' + cat + ': ' + lit[cat] + ' mil empregos em ago/2026', val(cat, 'emprego', 'sa') + '');
  });
  ok(Math.abs(val('05000000', 'ganho_hora', 'sa') - 37.75) < 0.005,
     'Summary table B: ganho medio/hora do setor privado = US$ 37,75',
     val('05000000', 'ganho_hora', 'sa') + '');
  ok(Math.abs(val('05000000', 'horas_semana', 'sa') - 34.4) < 0.05,
     'Summary table B: horas semanais medias = 34,4', val('05000000', 'horas_semana', 'sa') + '');
  ok(Math.abs(val('05000000', 'ganho_semana', 'sa') - 1298.60) < 0.02,
     'Summary table B: ganho medio/semana = US$ 1.298,60',
     val('05000000', 'ganho_semana', 'sa') + '');
  // As identidades do topo, no dado que o relatorio mostra.
  ok(val('05000000', 'emprego', 'sa') + val('90000000', 'emprego', 'sa')
     === val('00000000', 'emprego', 'sa'),
     'privado + governo = total nonfarm, exato');
  ok(val('06000000', 'emprego', 'sa') + val('08000000', 'emprego', 'sa')
     === val('05000000', 'emprego', 'sa'),
     'bens + servico privado = total privado, exato');

  // A aditividade por medida agora e afirmada na secao 13c, sobre a barra de camadas.
})();

// ── 13b. As 7 camadas de metrica (piloto: Payroll employment — CES) ─────────
// Cada asserção aqui existe por um modo de falha que NAO lanca excecao:
//   - uma camada que o dado nao oferece renderizando controle (a pill solitaria)
//   - a composicao "media de 3 meses da variacao mensal" continuar inalcancavel
//   - `Change` e `%` virarem a mesma opcao (dois numeros com a mesma cara)
//   - o eixo Y continuar dizendo a unidade do nivel numa vista de variacao
//   - o motivo de uma opcao cinza sumir da tela (title de <option> nao aparece)
secao('13b. As 7 camadas de metrica — piloto na aba de emprego da CES');
{
  const LB = 'lb-ces-emprego';
  const camadaDe = (rot) => doc.getElementById(LB).children.find(
    (w) => w.children.some((c) => c.tag === 'label' && c.textContent === rot));
  const selDe = (rot) => {
    const w = camadaDe(rot);
    return w ? w.children.find((c) => c.tag === 'select') : null;
  };
  const opcoesDe = (rot) => { const s = selDe(rot); return s ? s.children : []; };
  const rotulosDe = (rot) => opcoesDe(rot).map((o) => o.textContent);
  const escolher = (rot, v) => { const s = selDe(rot); s.value = v; s.fire('change'); };
  const why = () => doc.getElementById('lw-ces-emprego').children
    .map((d) => d.children.map((c) => c.textContent).join('')).join(' | ');

  const tab = R.TABS.ces_emprego;
  const st = tab.state;
  const raiz = tab.raiz;
  const filho = (raiz.children || [])[0];

  // ---- (a) quais camadas EXISTEM
  const labels = doc.getElementById(LB).children.map(
    (w) => (w.children.find((c) => c.tag === 'label') || {}).textContent);
  eq(labels.join(' · '),
     'Adjustment · Denominator · Comparison · Smoothing · Chart',
     'as 5 camadas que este dado oferece, na ordem do pipeline');
  ok(labels.indexOf('Measure') < 0,
     'Measure NAO renderiza: a familia de emprego tem uma medida so');
  ok(labels.indexOf('Window') < 0,
     'Window NAO renderiza: emprego e ESTOQUE, e estoque nao acumula');
  ok(labels.indexOf('Basis') < 0,
     'Basis NAO renderiza: emprego nao e valor monetario');
  // Antes da migracao esta opcao existia e ficava PERMANENTEMENTE cinza nesta aba.
  ok(!rotulosDe('Comparison').concat(rotulosDe('Smoothing'))
      .some((r) => /12-month total/.test(r)),
     'e "12M total" nao aparece em nenhuma camada, em vez de ficar cinza para sempre');

  // ---- (b) a serie crua, para as contas abaixo
  escolher('Comparison', 'valor');
  escolher('Smoothing', 'none');
  const nivel = tab.serie(filho).slice();
  const n = nivel.length;
  ok(nivel.some((v) => v != null), 'a serie de nivel tem dado');

  // ---- (c) a composicao que era inalcancavel: media de 3 meses da variacao mensal
  escolher('Comparison', 'dPer');
  const dif = tab.serie(filho).slice();
  escolher('Smoothing', 'ma3');
  const difMa3 = tab.serie(filho).slice();
  const esperadoDif = R._dif(nivel, 1);
  const esperadoMa3 = R._janela(esperadoDif, 3, true);
  let piorD = 0, piorM = 0, nD = 0, nM = 0;
  for (let i = 0; i < n; i++) {
    if (esperadoDif[i] != null && dif[i] != null) { piorD = Math.max(piorD, Math.abs(dif[i] - esperadoDif[i])); nD++; }
    if (esperadoMa3[i] != null && difMa3[i] != null) { piorM = Math.max(piorM, Math.abs(difMa3[i] - esperadoMa3[i])); nM++; }
  }
  ok(nD > 300 && piorD < 1e-9, 'Change M/M e a diferenca do nivel (' + nD + ' meses)');
  ok(nM > 300 && piorM < 1e-9,
     'e "3-month average" + "Change M/M" da a MEDIA DE 3 MESES DA VARIACAO ('
     + nM + ' meses) — a leitura de payroll que antes nao era pedivel');
  // A media de 3 nao pode ser igual a variacao crua, senao a camada 6 nao fez nada.
  let difere = 0;
  for (let i = 0; i < n; i++) if (dif[i] != null && difMa3[i] != null && Math.abs(dif[i] - difMa3[i]) > 1e-9) difere++;
  ok(difere > 300, 'e a suavizacao muda o numero em ' + difere + ' meses (nao e no-op)');

  // ---- (d) `Change` e `%` sao opcoes DISTINTAS
  escolher('Smoothing', 'none');
  escolher('Comparison', 'pPer');
  const pct = tab.serie(filho).slice();
  let checados = 0, pior = 0;
  for (let i = 1; i < n; i++) {
    if (nivel[i - 1] == null || nivel[i - 1] === 0 || pct[i] == null) continue;
    pior = Math.max(pior, Math.abs(pct[i] - (dif[i] / nivel[i - 1]) * 100));
    checados++;
  }
  ok(checados > 300 && pior < 1e-9,
     '% M/M = Change M/M / nivel anterior (' + checados + ' meses): duas grandezas, nao uma');
  // A ordem de grandeza e a razao de a distincao importar: +89 mil contra +0,06%.
  const iUlt = (() => { for (let i = n - 1; i >= 0; i--) if (dif[i] != null && pct[i] != null) return i; })();
  ok(Math.abs(dif[iUlt]) > 20 * Math.abs(pct[iUlt]),
     'e as duas leituras do MESMO mes diferem em ordem de grandeza ('
     + dif[iUlt].toFixed(1) + ' contra ' + pct[iUlt].toFixed(3) + ')');

  // ---- (e) Δ Y/Y em mil empregos: antes da migracao, inalcancavel
  escolher('Comparison', 'dYoY');
  const dyoy = tab.serie(filho).slice();
  const espYoY = R._dif(nivel, 12);
  let piorY = 0, nY = 0;
  for (let i = 0; i < n; i++) {
    if (espYoY[i] != null && dyoy[i] != null) { piorY = Math.max(piorY, Math.abs(dyoy[i] - espYoY[i])); nY++; }
  }
  ok(nY > 300 && piorY < 1e-9,
     'Change Y/Y e a diferenca contra 12 meses atras, em mil empregos (' + nY + ')');
  ok(/thousands of jobs/.test(tab.yTitle()) && !/%/.test(tab.yTitle()),
     'e o eixo diz "thousands of jobs", nao %: ' + tab.yTitle());

  // ---- (f) a camada 5 perde as opcoes de % quando o denominador e participacao
  escolher('Comparison', 'pPer');
  eq(st.compara, 'pPer', 'com o denominador em Level, % M/M vale');
  escolher('Denominator', 'share');
  eq(st.compara, 'valor',
     'trocar para participacao CAI DE VOLTA para Value em vez de deixar o estado invalido na tela');
  const cinzas = opcoesDe('Comparison').filter((o) => o.disabled).map((o) => o.textContent);
  eq(cinzas.length, 2, 'as duas opcoes de % ficam cinza, e nao desaparecem');
  ok(/percentage points/.test(why()),
     'e o motivo aparece na tela, abaixo da barra: ' + why().slice(0, 90));

  // ---- (g) o par que NAO comuta: denominador x suavizacao
  escolher('Comparison', 'valor');
  escolher('Smoothing', 'ma3');
  const shareMa3 = tab.serie(filho).slice();
  escolher('Smoothing', 'none');
  const share = tab.serie(filho).slice();
  const espShareMa3 = R._janela(share, 3, true);
  // O certo: media da RAZAO. O errado plausivel: razao das medias.
  escolher('Denominator', 'nivel');
  escolher('Smoothing', 'ma3');
  const numMa3 = tab.serie(filho).slice();
  const denMa3 = tab.serie(raiz).slice();
  const razaoDasMedias = numMa3.map((a, i) => (a == null || denMa3[i] == null || denMa3[i] === 0) ? null : (a / denMa3[i]) * 100);
  let piorS = 0, nS = 0, divergem = 0;
  for (let i = 0; i < n; i++) {
    if (espShareMa3[i] != null && shareMa3[i] != null) { piorS = Math.max(piorS, Math.abs(shareMa3[i] - espShareMa3[i])); nS++; }
    if (espShareMa3[i] != null && razaoDasMedias[i] != null
        && Math.abs(espShareMa3[i] - razaoDasMedias[i]) > 1e-9) divergem++;
  }
  ok(nS > 300 && piorS < 1e-9,
     'com participacao, a suavizacao e a MEDIA DA RAZAO (' + nS + ' meses)');
  ok(divergem > 100,
     'e ela difere da razao das medias em ' + divergem + ' meses — este par NAO comuta, '
     + 'e e nele que a ordem do pipeline pode ser afirmada');
  // O par que comuta, afirmado para ninguem escrever a asserção de ordem nele:
  const difDeMa3 = R._dif(R._janela(nivel, 3, true), 1);
  const ma3DeDif = R._janela(R._dif(nivel, 1), 3, true);
  let iguais = 0;
  for (let i = 0; i < n; i++) {
    if (difDeMa3[i] != null && ma3DeDif[i] != null && Math.abs(difDeMa3[i] - ma3DeDif[i]) < 1e-9) iguais++;
  }
  ok(iguais > 300,
     'diferenca e media movel COMUTAM (' + iguais + ' meses iguais): um teste de ordem '
     + 'escrito nesse par passa nas duas ordens e nao segura nada');

  // ---- (h) barras empilhadas: a tabela de aditividade depende so da camada 5
  escolher('Denominator', 'nivel');
  escolher('Smoothing', 'none');
  const barras = (cmp) => { escolher('Comparison', cmp); return tab.barrasOk(); };
  ok(barras('valor'), 'barras: nivel soma entre irmas');
  ok(barras('dPer'), 'barras: a DIFERENCA soma (herda a aditividade da base)');
  ok(barras('dYoY'), 'barras: a diferenca Y/Y tambem');
  ok(!barras('pPer'), 'barras OFF em % M/M: variacao percentual nao soma');
  ok(!barras('pYoY'), 'barras OFF em % Y/Y');
  const opChart = opcoesDe('Chart').find((o) => /Stacked/.test(o.textContent));
  ok(opChart && opChart.disabled, 'e a opcao fica cinza, nao desaparece');
  ok(/inherit it from the level/.test(why()),
     'com o motivo dizendo que a diferenca soma e esta na mesma lista: ' + why().slice(-95));
  escolher('Comparison', 'valor');
  escolher('Smoothing', 'ma3');
  ok(tab.barrasOk(), 'e a suavizacao nao mexe na aditividade: media de coisas que somam soma');

  // ---- (i) o eixo Y e o CAMINHO INTEIRO
  escolher('Smoothing', 'none');
  escolher('Comparison', 'valor');
  eq(tab.yTitle(), 'employees on payrolls, thousands', 'eixo: nivel');
  escolher('Smoothing', 'ma3');
  eq(tab.yTitle(), 'employees on payrolls, thousands, 3-month average',
     'eixo: a suavizacao ACRESCENTA e nao troca a unidade');
  escolher('Comparison', 'dPer');
  eq(tab.yTitle(), 'change vs. the previous month, thousands of jobs, 3-month average',
     'eixo: a comparacao TROCA a unidade, e a suavizacao continua acrescentando');
  escolher('Comparison', 'valor');
  escolher('Smoothing', 'none');
  escolher('Denominator', 'share');
  eq(tab.yTitle(), 'share of Total nonfarm employment, %',
     'eixo: o denominador NOMEIA a raiz da propria arvore');
  escolher('Comparison', 'dPer');
  eq(tab.yTitle(), 'p.p. change vs. the previous month',
     'eixo: diferenca de uma participacao sai em p.p., nunca em %');

  // ---- (j) o subtitulo do grafico segue as camadas
  const sub = () => doc.getElementById('cs-ces-emprego').textContent;
  ok(/% of Total nonfarm/.test(sub()) && /Change M\/M/.test(sub()),
     'o subtitulo carrega o estado das camadas que sairam do default: ' + sub().slice(0, 110));
  escolher('Denominator', 'nivel');
  escolher('Comparison', 'valor');
  ok(!/Change M\/M/.test(sub()) && !/% of/.test(sub()),
     'e nao repete as que estao no default');

  // ---- (k) o cartao de definicao da medida sobreviveu a saida da barra
  const ct = doc.getElementById('ct-ces-emprego');
  ok(ct.children.some((c) => c.className === 'info-btn'),
     'com Measure fora da barra, o cartao de definicao passou para o titulo do grafico');
  tab.redraw();
  eq(ct.children.filter((c) => c.className === 'info-btn').length, 1,
     'e o botao nao duplica a cada render (describeChart reescreve o titulo)');
}

// ── 13c. As camadas na aba de horas e ganhos — 10 medidas, 3 naturezas ──────
// Esta aba exercita o que a de emprego nao tinha: um seletor de MEDIDA de verdade
// (que fica em pills, porque medida nao e camada e uma <option> nao hospeda cartao),
// uma camada de BASE, e a disponibilidade das camadas 4 e 7 mudando por medida.
// Os modos de falha que nao lancam excecao:
//   - a variacao de um numero em DOLARES sair rotulada "p.p." (era o estado anterior)
//   - a opcao Real renderizar com o payload sem as series dela (grafico vazio)
//   - "% do total" aparecer numa media ponderada, que nao tem total
secao('13c. As camadas na aba de horas e ganhos da CES');
{
  const LB = 'lb-ces-horas';
  const camadaDe = (rot) => doc.getElementById(LB).children.find(
    (w) => w.children.some((c) => c.tag === 'label' && c.textContent === rot));
  const selDe = (rot) => {
    const w = camadaDe(rot);
    return w ? w.children.find((c) => c.tag === 'select') : null;
  };
  const opcoesDe = (rot) => { const s = selDe(rot); return s ? s.children : []; };
  const escolher = (rot, v) => { const s = selDe(rot); s.value = v; s.fire('change'); };
  const labels = () => doc.getElementById(LB).children.map(
    (w) => (w.children.find((c) => c.tag === 'label') || {}).textContent);
  const why = () => doc.getElementById('lw-ces-horas').children
    .map((d) => d.children.map((c) => c.textContent).join('')).join(' | ');
  const medida = (rot) => escolherNoGrupo('ces-horas', 'medida', rot);

  const tab = R.TABS.ces_horas;
  const st = tab.state;
  const filho = (tab.raiz.children || [])[0];

  // ---- (a) a medida fica FORA da barra de camadas, e num <select> por largura
  const gm = doc.getElementById('pg-ces-horas-medida');
  const sm = gm.children.find((c) => c.tag === 'select');
  ok(!!sm, 'as 10 medidas nao cabem numa linha de pills: o controle e um <select>');
  eq(sm.children.length, 10, 'com as 10 medidas (2 das 12 viraram opcao de base)');
  eq(gm.children.filter((c) => c.className === 'info-btn').length, 1,
     'e UM cartao de definicao, do item selecionado — uma <option> nao hospedaria');
  ok(!labels().some((l) => l === 'Measure'),
     'a medida nao aparece como camada: "entidade x medida" e upstream do pipeline');

  // ---- (b) a camada de BASE existe so onde a fonte publica as duas
  medida('Hourly earnings');
  ok(labels().indexOf('Basis') === 0,
     'Basis e a primeira camada em ganho por hora: ' + labels().join(' · '));
  eq(opcoesDe('Basis').map((o) => o.textContent).join(' | '),
     'Nominal US$ | Constant 1982-84 US$',
     'com as duas bases que o BLS publica');
  medida('Weekly hours');
  ok(labels().indexOf('Basis') < 0,
     'e desaparece em horas semanais, que nao tem contrapartida real');

  // ---- (c) a opcao Real tem DADO: mover uma serie para dentro da base tirou 376
  //          series do payload na primeira execucao, sem erro nenhum
  medida('Hourly earnings');
  escolher('Basis', 'nominal');
  const nomHora = tab.serie(filho).slice();
  escolher('Basis', 'real');
  const realHora = tab.serie(filho).slice();
  ok(realHora && realHora.some((v) => v != null),
     'a base Real plota dado de verdade, e nao um grafico vazio');
  let difBase = 0;
  for (let i = 0; i < nomHora.length; i++) {
    if (nomHora[i] != null && realHora[i] != null && Math.abs(nomHora[i] - realHora[i]) > 1e-9) difBase++;
  }
  // A serie real do BLS e mais curta que a nominal -- dai o piso ser 200 e nao 300.
  ok(difBase > 200, 'e e outra serie: difere da nominal em ' + difBase + ' meses');
  eq(tab.yTitle(), 'average hourly earnings, constant 1982-84 US$',
     'o eixo diz a base, e o titulo do card segue sendo a medida');
  escolher('Basis', 'nominal');

  // ---- (d) O BUG QUE A MIGRACAO ACHOU: dolar nao e p.p.
  // Antes de 2026-09-04, `razao` vinha de `!aditivo`, entao ganho medio por hora --
  // que nao soma entre industrias mas esta em US$ -- tinha a variacao calculada como
  // diferenca e rotulada "p.p. change". As duas coisas estavam erradas.
  escolher('Comparison', 'dPer');
  eq(tab.yTitle(), 'change vs. the previous month, US$ per hour',
     'a diferenca de um ganho em dolares sai em US$ por hora, nunca em p.p.');
  ok(!/p\.p\./.test(tab.yTitle()), 'e o eixo nao diz p.p. em lugar nenhum');
  escolher('Comparison', 'pYoY');
  const pctAno = tab.serie(filho).slice();
  eq(tab.yTitle(), '% change vs. the same month a year earlier',
     'e o "+% a/a" da manchete passou a existir nesta aba');
  escolher('Comparison', 'valor');
  const nivel = tab.serie(filho).slice();
  let conf = 0, pior = 0;
  for (let i = 12; i < nivel.length; i++) {
    if (nivel[i] == null || nivel[i - 12] == null || nivel[i - 12] === 0 || pctAno[i] == null) continue;
    pior = Math.max(pior, Math.abs(pctAno[i] - (nivel[i] / nivel[i - 12] - 1) * 100));
    conf++;
  }
  // A serie de ganho medio de TODOS os empregados comeca em 2006 (a de operarios vai a
  // 1964, e outra serie), entao 230 e o tamanho certo da amostra aqui, nao 300.
  ok(conf > 200 && pior < 1e-9,
     '% Y/Y e variacao percentual mesmo (' + conf + ' meses, erro max '
     + pior.toExponential(1) + '), nao diferenca');
  // A ordem de grandeza: um ganho por hora perto de 30 dolares.
  const iU = (() => { for (let i = nivel.length - 1; i >= 0; i--) if (pctAno[i] != null) return i; })();
  ok(nivel[iU] > 10 && Math.abs(pctAno[iU]) < 10,
     'nivel ~US$' + nivel[iU].toFixed(2) + '/h e variacao ' + pctAno[iU].toFixed(2)
     + '% — a diferenca rotulada p.p. confundia estas duas');

  // As tres naturezas, e a unidade da diferenca em cada uma.
  escolher('Comparison', 'dPer');
  const unidadeDif = {};
  [['Weekly hours', 'hours per employee'],
   ['Aggregate weekly hours', 'thousands of hours'],
   ['Aggregate weekly payrolls', 'thousands of US$'],
   ['Index of aggregate hours', 'index points']].forEach((par) => {
    medida(par[0]);
    unidadeDif[par[0]] = tab.yTitle();
    eq(tab.yTitle(), 'change vs. the previous month, ' + par[1],
       par[0] + ': a diferenca vem em ' + par[1]);
  });
  ok(!Object.keys(unidadeDif).some((k) => /p\.p\./.test(unidadeDif[k])),
     'nenhuma das quatro sai em p.p.: a CES nao tem medida que seja porcentagem');

  // ---- (e) a camada 4 e a 7 mudam por MEDIDA, nao por camada
  medida('Hourly earnings');
  escolher('Comparison', 'valor');
  let denOff = opcoesDe('Denominator').filter((o) => o.disabled);
  eq(denOff.length, 1, 'media ponderada: "% do total" fica cinza');
  ok(/average per worker/.test(why()),
     'com o motivo na tela: ' + why().slice(0, 80));
  ok(!tab.barrasOk(), '...e barras empilhadas saem junto');
  medida('Aggregate weekly hours');
  eq(opcoesDe('Denominator').filter((o) => o.disabled).length, 0,
     'horas agregadas: "% do total" volta, porque as industrias somam');
  eq(opcoesDe('Denominator')[1].textContent, '% of Total private',
     'e o denominador nomeia a raiz DESTA aba, que nao e a da aba de emprego');
  ok(tab.barrasOk(), '...e as barras voltam');
  medida('Index of aggregate hours');
  ok(!tab.barrasOk(), 'indice 2007=100 nao empilha');
  ok(/index/i.test(why()), 'e o motivo diz que a mesma grandeza em milhares esta na lista');

  // ---- (f) nada na CES acumula: a camada de janela nao renderiza em nenhuma medida
  const semJanela = [];
  opcoesDoGrupo('ces-horas', 'medida').forEach((rot) => {
    medida(rot);
    if (labels().indexOf('Window') < 0) semJanela.push(rot);
  });
  eq(semJanela.length, 10,
     'as 10 medidas dispensam a camada de janela: doze meses de folha semanal nao dao um ano');

  medida('Weekly hours');
  escolher('Comparison', 'valor');
  escolher('Smoothing', 'none');
}

// ── 13d. Pills ou <select>: o controle cabe numa linha ou nao e pill ────────
// Pedido do usuario a partir de um print em que as 10 medidas da CES quebravam para
// uma segunda linha. O modo de falha nao lanca excecao nenhuma: o grupo simplesmente
// embrulha, e quem acrescentou a 7a opcao meses depois nao ve nada de errado.
secao('13d. A forma do controle segue a largura, nao o papel da opcao');
{
  const PREFS = ['industria', 'tamanho', 'regiao', 'ces-emprego', 'ces-horas',
                 'cps-status', 'cps-taxa_grupo', 'cps-composicao', 'cps-alternativa', 'prod'];
  const GRUPOS = ['medida', 'tipo', 'ajuste', 'transform', 'kind', 'eixo'];
  let vistos = 0, comoSelect = [], estouram = [];
  PREFS.forEach((pf) => GRUPOS.forEach((g) => {
    const el = doc.getElementById('pg-' + pf + '-' + g);
    if (!el || !el.children.length) return;
    vistos++;
    const sel = el.children.find((c) => c.tag === 'select');
    if (sel) { comoSelect.push(pf + '/' + g + ' (' + sel.children.length + ')'); return; }
    const items = pills(pf, g).map((b) => ({
      label: pillLabel(b),
      infoKey: b.children.some((c) => c.className === 'info-btn') ? 1 : 0,
    }));
    const w = R.larguraPills(items);
    if (w > R.PILL_MAX_PX) estouram.push(pf + '/' + g + ' ' + Math.round(w) + 'px');
  }));
  // O piso caiu de 30 para 12 quando as 4 abas da CPS migraram para a barra de
  // camadas: 16 grupos de pill viraram 4 barras de <select> (o `Cut` da composicao e o
  // unico pill que sobrou ali, porque corte e seletor de serie e nao camada).
  ok(vistos > 12, vistos + ' grupos de controle renderizados, todos varridos');
  eq(estouram.length, 0,
     'nenhum grupo em pills estoura a linha: ' + (estouram.join(', ') || 'nenhum'));
  // Os dois que estouravam no print, e continuam sendo os unicos que precisam de select.
  eq(comoSelect.sort().join(' · '), 'ces-horas/medida (10) · prod/medida (19)',
     'os dois grupos largos viraram <select>, e so eles');
  // E o formato NAO e escolhido a mao: sai da largura estimada.
  const seis = pills('industria', 'medida').map((b) => ({label: pillLabel(b), infoKey: 1}));
  eq(seis.length, 6, 'as 6 medidas do JOLTS seguem em pills');
  ok(R.larguraPills(seis) < R.PILL_MAX_PX,
     '...porque cabem: ' + Math.round(R.larguraPills(seis)) + 'px de ' + R.PILL_MAX_PX);
  // O mutante que importa: acrescentar opcoes ao mesmo grupo tem de virar select sozinho.
  const dobrado = seis.concat(seis).concat(seis);
  ok(R.larguraPills(dobrado) > R.PILL_MAX_PX,
     'e o mesmo grupo com 18 viraria select sem ninguem decidir nada ('
     + Math.round(R.larguraPills(dobrado)) + 'px)');
  // O cartao de definicao sobrevive a troca de formato, um por controle.
  ['ces-horas', 'prod'].forEach((pf) => {
    const el = doc.getElementById('pg-' + pf + '-medida');
    eq(el.children.filter((c) => c.className === 'info-btn').length, 1,
       pf + ': um cartao, do item selecionado');
  });
}

// ── 13e. A raiz da arvore segue o ESCOPO da medida ──────────────────────────
// Reportado pelo usuario: "Overtime hours", "Hourly earnings ex-overtime" e "Aggregate
// overtime hours" apareciam VAZIAS. A CES coleta overtime so na industria de
// transformacao, entao as tres cobrem 21 das 94 linhas -- e nenhuma das marcadas por
// default (Total private, Goods-producing, Private services) esta entre elas.
// Dois blanks silenciosos, nao um: o grafico sem linha nenhuma, e um "% do total" que
// dividia por uma serie de overtime de Total private que NAO EXISTE.
secao('13e. A raiz da arvore segue o escopo da medida (o caso do overtime)');
{
  const tab = R.TABS.ces_horas;
  const MD_OT = ['Overtime hours', 'Hourly earnings ex-overtime', 'Aggregate overtime hours'];
  const raizPayload = R.D.ces.abas.horas.tree[0];
  const medida = (rot) => escolherNoGrupo('ces-horas', 'medida', rot);
  const sub = () => doc.getElementById('cs-ces-horas').textContent;

  // ---- (a) o fato que produzia o vazio, afirmado para nao voltar em silencio
  eq(!!R.D.ces.series[[raizPayload.key, 'overtime_semana', 'sa'].join('|')], false,
     'Total private NAO tem serie de overtime — era por isso que o grafico saia vazio');
  ok(!!R.D.ces.series[['31000000', 'overtime_semana', 'sa'].join('|')]
     || R.achatar(R.D.ces.abas.horas.tree).some(
          (n) => /^Manufacturing$/.test(n.label)
                 && !!R.D.ces.series[[n.key, 'overtime_semana', 'sa'].join('|')]),
     '...e Manufacturing tem');

  // ---- (b) as 3 medidas de overtime: raiz Manufacturing, 21 linhas
  MD_OT.forEach((md) => {
    medida(md);
    const vis = R.achatar(tab.arvoreAtual());
    eq(vis.length, 21, md + ': a arvore visivel cai para as 21 linhas cobertas');
    eq(tab.raizAtual().label, 'Manufacturing', md + ': ...com raiz Manufacturing');
    // O conjunto coberto e uma subarvore COMPLETA -- e o que autoriza filtrar por
    // cobertura em vez de listar sobras. Medido: nenhum filho sem dado sob pai com dado.
    const semDado = vis.filter(
      (n) => !R.D.ces.series[[n.key, tab.state.medida, tab.state.ajuste].join('|')]);
    eq(semDado.length, 0, md + ': ...e toda linha visivel tem dado');
    // A selecao caiu de volta para linhas que existem, em vez de plotar nada.
    const marcadas = vis.filter((n) => tab.state.checked[n.key]);
    ok(marcadas.length >= 1, md + ': ...alguma linha visivel fica marcada');
    const comDado = marcadas.filter((n) => {
      const s = tab.serie(n);
      return s && s.some((v) => v != null);
    });
    eq(comDado.length, marcadas.length,
       md + ': ...e TODA marcada plota dado (' + comDado.length + ')');
    ok(/published only within Manufacturing/.test(sub()),
       md + ': ...e o cabecalho diz o escopo, senao a tabela curta le como dado faltando');
  });

  // ---- (c) o denominador da participacao e a raiz COBERTA
  medida('Aggregate overtime hours');
  tab.state.tipo = 'share';
  tab.redraw();
  eq(tab.yTitle(), 'share of Manufacturing aggregate overtime, %',
     '"% do total" nomeia Manufacturing, nao Total private — que nao tem o dado');
  const alvo = R.achatar(tab.arvoreAtual()).find((n) => tab.state.checked[n.key]);
  const sh = tab.serie(alvo);
  ok(sh && sh.some((v) => v != null),
     '...e a participacao tem valor, em vez de dividir por uma serie inexistente');
  // A raiz lê exatamente 100: o invariante que prova que o denominador e ela mesma.
  tab.state.checked[tab.raizAtual().key] = true;
  tab.redraw();
  const raizSerie = tab.serie(tab.raizAtual());
  const ult = (() => {
    for (let i = raizSerie.length - 1; i >= 0; i--) if (raizSerie[i] != null) return raizSerie[i];
  })();
  ok(Math.abs(ult - 100) < 1e-9, 'e a raiz da arvore lê exatamente 100, nao 100 x algo');
  tab.state.tipo = 'nivel';
  tab.redraw();

  // ---- (d) as outras 7 medidas nao mudaram de raiz
  const semEscopo = [];
  opcoesDoGrupo('ces-horas', 'medida').forEach((rot) => {
    if (MD_OT.indexOf(rot) >= 0) return;
    medida(rot);
    if (R.achatar(tab.arvoreAtual()).length === 94
        && tab.raizAtual().key === raizPayload.key) semEscopo.push(rot);
  });
  eq(semEscopo.length, 7,
     'as outras 7 medidas seguem com as 94 linhas e raiz Total private');
  medida('Weekly hours');
}

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
  // Summary table A de AGOSTO/2026 (divulgado 04/09/2026). Mesma advertencia da
  // secao 13: e a ponta da serie, entao envelhece a cada divulgacao.
  const lit = {ocupados: 162746, desocupados: 7031, forca_trabalho: 169777,
               fora_forca: 105638, taxa_desemprego: 4.1, participacao: 61.6,
               razao_emprego_pop: 59.1, u6: 7.7};
  Object.keys(lit).forEach((k) => {
    ok(Math.abs(val(k, 'sa') - lit[k]) < 0.051,
       'Summary table A ' + k + ' = ' + lit[k], val(k, 'sa') + '');
  });
  ok(val('populacao', 'nsa') === 275415,
     'a populacao vem so sem ajuste sazonal, e bate: 275.415',
     val('populacao', 'nsa') + '');
  ok(val('populacao', 'sa') === null,
     '...e nao existe versao ajustada dela (o BLS nao publica)');
  // Aditividade do bloco de status.
  // NAO e exato, e a nota de pe da propria Summary table A diz por que: "detail ...
  // will not necessarily add to totals because of the independent seasonal adjustment
  // of the various series". Em ago/2026 ela fecha exata (162.746 + 7.031 = 169.777),
  // mas em jul/2026 dava 162.177 + 6.916 = 169.093 contra 169.094 publicados -- e por
  // isso a tolerancia de 1 mil fica, mesmo num mes em que o residuo e zero. Mesmo
  // efeito que faz a arvore da CES ser validada no dado bruto.
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

// ── 14b. As 7 camadas nos quatro blocos da CPS ──────────────────────────────
// A CPS e a primeira aba em que a NATUREZA e propriedade da LINHA e nao de uma medida:
// o mesmo bloco mistura pessoas (mil), taxas (%) e duracao (semanas). Tres defeitos
// desta aba foram MEDIDOS no arquivo anterior a migracao, e nenhum lancava excecao:
//
//   (a) "% do total" no bloco de status, na vista ajustada (que e a default), plotava
//       ZERO series -- a populacao e a unica linha que o BLS nunca dessazonaliza,
//       entao a divisao era por uma serie inexistente. Tabela e grafico em branco.
//   (b) O rotulo do eixo dizia "p.p. change" no Y/Y do corte por motivo enquanto a
//       conta feita era percentual (Job losers −5,86% no ultimo mes). Nos blocos nao
//       aditivos o eixo saia por BLOCO e o valor por LINHA, e nada reconciliava.
//   (c) `naoSoma` era lido como "e porcentagem", entao a variacao de uma duracao em
//       SEMANAS saia rotulada em p.p. -- a mesma confusao entre `aditivo` e `razao`
//       que a aba de horas da CES tinha, por outro caminho.
secao('14b. As 7 camadas nos quatro blocos da CPS');
{
  const BL = ['cps-status', 'cps-taxa_grupo', 'cps-composicao', 'cps-alternativa'];
  const camadasDe = (pref) => doc.getElementById('lb-' + pref).children.map((w) => {
    const lab = w.children.find((c) => c.tag === 'label');
    const sel = w.children.find((c) => c.tag === 'select');
    return {label: lab ? lab.textContent : '?', sel: sel,
            opts: sel ? sel.children : []};
  });
  const camada = (pref, rot) => camadasDe(pref).find((c) => c.label === rot);
  const setC = (pref, rot, key) => {
    const c = camada(pref, rot);
    c.sel.value = key; c.sel.fire('change');
  };
  const optDe = (pref, rot, key) => camada(pref, rot).opts.find((o) => o.value === key);
  const why = (pref) => doc.getElementById('lw-' + pref).children
    .map((d) => d.children.map((c) => c.textContent).join('')).join(' || ');
  const sub = (pref) => doc.getElementById('cs-' + pref).textContent;
  const ultimo = (v) => { for (let i = v.length - 1; i >= 0; i--) if (v[i] != null) return v[i]; return null; };
  const iUltimo = (v) => { for (let i = v.length - 1; i >= 0; i--) if (v[i] != null) return i; return -1; };

  // ---- (a) as quatro abas estao na barra de camadas, e os pills antigos sumiram
  BL.forEach((p) => {
    ok(!!doc.getElementById('lb-' + p), p + ': tem barra de camadas');
    // Afirmado sobre a MARCACAO, e nao com getElementById: o stub cria elemento sob
    // demanda (e um browser devolveria null), entao um id que sobrou no HTML passaria
    // batido dos dois lados.
    ['tipo', 'ajuste', 'transform', 'kind'].forEach((g) => {
      ok(CRU.indexOf('pg-' + p + '-' + g) < 0,
         p + ': o pill group "' + g + '" saiu do HTML');
    });
  });
  // O `Cut` fica em pills: corte e seletor de SERIE (que linhas existem), nao camada de
  // metrica -- e e o que preserva a possibilidade de cartao por opcao.
  ok(!!doc.getElementById('pg-cps-composicao-eixo'),
     'o Cut da composicao continua em pills: corte e upstream do pipeline');
  eq(camadasDe('cps-status').map((c) => c.label).join(' · '),
     'Adjustment · Denominator · Comparison · Smoothing · Chart',
     'as camadas que renderizam sao 5: base e janela nao existem nesta pesquisa');

  // ---- (b) a camada 6 tem a media de 6 meses, e ela e uma media de 6 meses
  BL.forEach((p) => {
    eq(camada(p, 'Smoothing').opts.map((o) => o.textContent).join('/'),
       'None/3-month average/6-month average/12-month average',
       p + ': a camada de suavizacao tem as quatro janelas');
  });
  {
    const t = R.TABS.cps_status;
    const no = R.achatar(t.arvoreAtual()).find((n) => n.label === 'Employed');
    setC('cps-status', 'Smoothing', 'none');
    const nivel = t.serie(no).slice();
    setC('cps-status', 'Smoothing', 'ma6');
    const ma6 = t.serie(no).slice();
    const esperado = R._janela(nivel, 6, true);
    let dif = 0, comValor = 0;
    for (let i = 0; i < ma6.length; i++) {
      if (ma6[i] == null && esperado[i] == null) continue;
      if (ma6[i] == null || esperado[i] == null || Math.abs(ma6[i] - esperado[i]) > 1e-9) dif++;
      if (ma6[i] != null) comValor++;
    }
    eq(dif, 0, 'a media de 6 meses e a media dos 6 meses (' + comValor + ' pontos)');
    // Janela incompleta mostra NADA -- a convencao do design system, e o que faz o
    // buraco de out/2025 apagar seis pontos em vez de virar uma media de cinco meses.
    const iOut = D.cps.dates.indexOf('2025-10-01');
    let apagados = 0;
    for (let k = 0; k < 6; k++) if (ma6[iOut + k] == null) apagados++;
    eq(apagados, 6, 'e o mes nao coletado apaga as 6 janelas que o contem, nao vira media de 5');
    ok(ma6[iOut + 6] != null, '...e a setima volta a ter valor');
    setC('cps-status', 'Smoothing', 'none');
    ok(/6-month average/.test(R.unitCamadas(
         {yNivel: 'x', razao: false}, {tipo: 'nivel', compara: 'valor',
          janela: 'nativa', suaviza: 'ma6'})),
       'e o eixo Y diz a janela: o caminho inteiro, na ordem do pipeline');
  }

  // ---- (c) DEFEITO (a): a participacao exige um denominador que EXISTA
  {
    const t = R.TABS.cps_status;
    setC('cps-status', 'Adjustment', 'sa');
    ok(!!optDe('cps-status', 'Denominator', 'share').disabled,
       'na vista ajustada "% do total" fica cinza: a populacao nao tem serie ajustada');
    ok(/never adjusts/.test(why('cps-status')),
       '...com o motivo na tela: ' + why('cps-status').slice(0, 90));
    t.state.tipo = 'share'; t.redraw();
    eq(t.state.tipo, 'nivel',
       '...e o estado cai de volta para Level em vez de plotar zero series');
    // Sem ajuste sazonal a participacao funciona, e a raiz le exatamente 100.
    setC('cps-status', 'Adjustment', 'nsa');
    ok(!optDe('cps-status', 'Denominator', 'share').disabled,
       'sem ajuste sazonal ela volta');
    setC('cps-status', 'Denominator', 'share');
    eq(t.yTitle(), 'share of civilian population, %',
       'e o eixo NOMEIA o denominador');
    const raiz = t.specs().find((s) => s.name === 'Civilian population');
    ok(raiz && Math.abs(ultimo(raiz.values) - 100) < 1e-9,
       'a raiz da arvore le exatamente 100 — a prova de que o denominador e ela');
    // A FONTE JA PUBLICA ESTA RAZAO, e por isso ela e o gabarito: forca de trabalho
    // sobre populacao E a taxa de participacao. Tolerancia 0,1 p.p. porque o BLS
    // publica o nivel ao milhar e a taxa a 1 decimal (medido: pior 0,069 em 943 meses).
    const fo = t.specs().find((s) => s.name === 'Labor force');
    const iU = iUltimo(fo.values);
    const pub = D.cps.series['participacao|nsa'];
    const alvo = pub.v[iU - pub.i0];
    ok(Math.abs(fo.values[iU] - alvo) < 0.1,
       'forca/populacao reproduz a taxa de participacao publicada ('
       + fo.values[iU].toFixed(3) + ' vs ' + alvo + ')');
    // Marcar uma taxa mata a participacao: uma taxa nao e parte da populacao.
    t.state.tipo = 'share'; t.redraw();
    t.state.checked['taxa_desemprego'] = true;
    t.redraw();
    eq(t.state.tipo, 'nivel',
       'marcar uma taxa derruba a participacao — ela nao e parte do total');
    ok(/Unemployment rate/.test(why('cps-status')),
       '...e o motivo NOMEIA a linha culpada, em vez de dizer "invalido"');
  }

  // ---- (d) DEFEITO (b): o rotulo e a conta dizem a MESMA coisa, nos dois sentidos
  {
    const t = R.TABS.cps_status;
    const nos = R.achatar(t.arvoreAtual());
    const marcar = (labels) => {
      Object.keys(t.state.checked).forEach((k) => { t.state.checked[k] = false; });
      labels.forEach((L) => {
        const n = nos.find((x) => x.label === L);
        t.state.checked[n.key] = true;
      });
      t.redraw();
    };
    const serieDe = (L) => t.specs().find((s) => s.name === L).values;

    // So niveis: "% Y/Y" existe, diz "% change" E calcula variacao percentual.
    marcar(['Employed', 'Unemployed']);
    ok(!optDe('cps-status', 'Comparison', 'pYoY').disabled,
       'com so niveis marcados, "% Y/Y" esta disponivel');
    setC('cps-status', 'Comparison', 'valor');
    const nivel = serieDe('Unemployed').slice();
    setC('cps-status', 'Comparison', 'pYoY');
    const pct = serieDe('Unemployed').slice();
    ok(/^% change vs\. the same month/.test(t.yTitle()),
       'o eixo diz "% change": ' + t.yTitle());
    let conf = 0, pior = 0;
    for (let i = 12; i < nivel.length; i++) {
      if (nivel[i] == null || nivel[i - 12] == null || nivel[i - 12] === 0 || pct[i] == null) continue;
      pior = Math.max(pior, Math.abs(pct[i] - (nivel[i] / nivel[i - 12] - 1) * 100));
      conf++;
    }
    ok(conf > 600 && pior < 1e-9,
       '...e a conta E percentual em ' + conf + ' meses (antes o eixo dizia p.p. aqui)');

    // So taxas: "% Y/Y" fica cinza, e "Change" sai em p.p. E calcula diferenca.
    marcar(['Unemployment rate', 'Participation rate']);
    ok(!!optDe('cps-status', 'Comparison', 'pYoY').disabled,
       'com so taxas marcadas, "% Y/Y" fica cinza');
    setC('cps-status', 'Comparison', 'valor');
    const tx = serieDe('Unemployment rate').slice();
    setC('cps-status', 'Comparison', 'dYoY');
    const dtx = serieDe('Unemployment rate').slice();
    eq(t.yTitle(), 'p.p. change vs. the same month a year earlier',
       '...e o eixo passa a dizer p.p.');
    let conf2 = 0, pior2 = 0;
    for (let i = 12; i < tx.length; i++) {
      if (tx[i] == null || tx[i - 12] == null || dtx[i] == null) continue;
      pior2 = Math.max(pior2, Math.abs(dtx[i] - (tx[i] - tx[i - 12])));
      conf2++;
    }
    ok(conf2 > 600 && pior2 < 1e-9,
       '...e a conta E diferenca em ' + conf2 + ' meses');

    // Mistura: o eixo e UM SO, entao a variacao percentual cai e a diferenca diz
    // "unidades mistas" em vez de escolher a unidade de metade das linhas.
    marcar(['Employed', 'Unemployment rate']);
    ok(!!optDe('cps-status', 'Comparison', 'pPer').disabled
       && !!optDe('cps-status', 'Comparison', 'pYoY').disabled,
       'com nivel E taxa marcados as duas variacoes percentuais caem');
    ok(/percent change of a percentage/.test(why('cps-status')),
       '...com o motivo certo dos tres possiveis: ' + why('cps-status').slice(0, 80));
    setC('cps-status', 'Comparison', 'dPer');
    eq(t.yTitle(), 'change vs. the previous month, mixed units — see each row in the table',
       'e a diferenca, que e honesta nas duas unidades, diz que sao mistas');
    // Um clique numa opcao cinza nao pode mudar o estado.
    const antes = t.state.compara;
    const op = optDe('cps-status', 'Comparison', 'pYoY');
    camada('cps-status', 'Comparison').sel.value = op.value;
    camada('cps-status', 'Comparison').sel.fire('change');
    ok(t.state.compara === antes || t.state.compara === 'valor',
       'e escolher a opcao cinza nao deixa o estado num percentual de porcentagem',
       t.state.compara);
    // O aviso do mes nao coletado entra so na vista de variacao -- ali ele apaga DOIS
    // pontos em vez de um, e um aviso que aparece sempre nao e lido.
    setC('cps-status', 'Comparison', 'dPer');
    ok(/October 2025 was not collected/.test(sub('cps-status')),
       'o cabecalho avisa do mes nao coletado quando a leitura e variacao');
    setC('cps-status', 'Comparison', 'valor');
    ok(!/October 2025 was not collected/.test(sub('cps-status')),
       '...e nao avisa na vista de nivel, onde o buraco e um mes so');

    // E o caminho REAL de marcar tem de refazer a barra. Mexer em `state.checked` e
    // chamar redraw() contorna justamente o listener em questao: sem ele a barra fica
    // com as opcoes da selecao ANTERIOR -- a variacao percentual segue clicavel depois
    // de marcar uma taxa, e o estado fica valido no objeto e invalido na tela.
    marcar(['Employed']);
    setC('cps-status', 'Comparison', 'pYoY');
    eq(t.state.compara, 'pYoY', 'com so um nivel marcado, "% Y/Y" pega');
    const nos2 = R.flattenHierRows(t.arvoreAtual(), t.state.expanded, 0).map((r) => r.node);
    const tb = doc.getElementById('tb-cps-status');
    const iTaxa = nos2.findIndex((n) => n.label === 'Unemployment rate');
    ok(iTaxa >= 0 && tb.children.length === nos2.length,
       'a tabela tem uma linha por no, e a taxa esta na posicao ' + iTaxa);
    const cx = tb.children[iTaxa].children[0].children[0];
    cx.checked = true; cx.fire('change');
    ok(!!optDe('cps-status', 'Comparison', 'pYoY').disabled,
       'marcar a taxa PELA CAIXA derruba "% Y/Y" na hora');
    eq(t.state.compara, 'valor', '...e o estado cai de volta junto');

    marcar(['Civilian population', 'Labor force', 'Employed', 'Unemployed']);
    setC('cps-status', 'Adjustment', 'sa');
  }

  // ---- (e) o eixo de um bloco 100% taxa NOMEIA a base
  {
    const t = R.TABS.cps_taxa_grupo;
    eq(t.yTitle(), "unemployed as a share of that group's labor force, %",
       'o eixo de um bloco de taxas diz o que a porcentagem mede, nao "%"');
    ok(!!optDe('cps-taxa_grupo', 'Comparison', 'pYoY').disabled,
       'taxa_grupo: variacao percentual de porcentagem fica cinza');
    ok(!!optDe('cps-taxa_grupo', 'Chart', 'bars').disabled,
       '...e barras empilhadas tambem: cada taxa divide pela propria forca de trabalho');
    eq(R.TABS.cps_alternativa.yTitle(),
       'underutilized as a share of the relevant labor force, %',
       'e o de U-1..U-6 diz a base DELE — U-4/U-5/U-6 mudam o denominador');
  }

  // ---- (f) DEFEITO (c): semanas nao e porcentagem
  {
    const t = R.TABS.cps_composicao;
    clicar(pillDe('cps-composicao', 'eixo', 'By duration'));
    const nos = R.achatar(t.arvoreAtual());
    const dm = nos.find((n) => n.label === 'Average duration');
    Object.keys(t.state.checked).forEach((k) => { t.state.checked[k] = false; });
    t.state.checked[dm.key] = true;
    t.redraw();
    eq(t.yTitle(), 'weeks', 'duracao media e medida em SEMANAS');
    ok(!optDe('cps-composicao', 'Comparison', 'pYoY').disabled,
       'e por isso a variacao percentual dela e legitima — nao fica cinza');
    setC('cps-composicao', 'Comparison', 'valor');
    const niv = t.specs()[0].values.slice();
    setC('cps-composicao', 'Comparison', 'pYoY');
    const pc = t.specs()[0].values.slice();
    const iU = iUltimo(pc);
    ok(Math.abs(pc[iU] - (niv[iU] / niv[iU - 12] - 1) * 100) < 1e-9,
       'a conta e percentual: ' + pc[iU].toFixed(2) + '% (antes saia rotulada p.p.)');
    eq(t.yTitle(), '% change vs. the same month a year earlier',
       '...e o eixo concorda');
    // Mas ela NAO SOMA com contagens de pessoas: continua linha na vista de barras.
    setC('cps-composicao', 'Comparison', 'valor');
    nos.forEach((n) => { t.state.checked[n.key] = true; });
    t.redraw();
    setC('cps-composicao', 'Chart', 'bars');
    const sp = t.specs();
    const linhas = sp.filter((s) => s.comoLinha).map((s) => s.name).sort().join(', ');
    eq(linhas, 'Average duration, Median duration',
       'na vista de barras as duas duracoes ficam LINHA: nao empilham com pessoas');
    setC('cps-composicao', 'Chart', 'lines');
  }

  // ---- (g) a camada 4 do corte existe onde as partes SOMAM, e foi medido
  {
    const t = R.TABS.cps_composicao;
    clicar(pillDe('cps-composicao', 'eixo', 'By reason'));
    const nos = R.achatar(t.arvoreAtual());
    eq(nos.length, 4, 'o corte por motivo tem 4 linhas');
    Object.keys(t.state.checked).forEach((k) => { t.state.checked[k] = false; });
    nos.forEach((n) => { t.state.checked[n.key] = true; });
    t.redraw();
    // O DENOMINADOR NAO E A RAIZ DA ARVORE VISIVEL: e `desocupados`, uma linha de outro
    // bloco. Nomear a raiz do corte daria "share of job losers".
    setC('cps-composicao', 'Denominator', 'share');
    eq(t.yTitle(), 'share of unemployed, %',
       'o total do corte e o nivel de desocupados, que nem esta nesta tabela');
    setC('cps-composicao', 'Adjustment', 'nsa');
    let sp = t.specs(), iU = iUltimo(sp[0].values);
    let soma = sp.reduce((a, s) => a + (s.values[iU] || 0), 0);
    ok(Math.abs(soma - 100) < 0.15,
       'no dado BRUTO os 4 motivos somam ' + soma.toFixed(3) + '% dos desocupados');
    // No ajustado NAO fecham, e o motivo e o mesmo da arvore da CES: o BLS
    // dessazonaliza cada serie sozinho. Medido: pior 2,24% em 391 meses.
    setC('cps-composicao', 'Adjustment', 'sa');
    sp = t.specs(); iU = iUltimo(sp[0].values);
    const somaSa = sp.reduce((a, s) => a + (s.values[iU] || 0), 0);
    ok(Math.abs(somaSa - 100) > 0.001 && Math.abs(somaSa - 100) < 3.2,
       '...e no ajustado somam ' + somaSa.toFixed(3) + '% — perto, e nao uma identidade');
    ok(/adjusts each series on its own/.test(doc.getElementById('note-cps-composicao').innerHTML),
       'e a nota do bloco diz isso ao leitor, porque a barra empilhada AFIRMA que somam');
    setC('cps-composicao', 'Denominator', 'nivel');
  }

  // ---- (h) o corte que nao soma nao oferece nem barras nem participacao
  {
    const t = R.TABS.cps_composicao;
    clicar(pillDe('cps-composicao', 'eixo', 'Part-time status'));
    ok(!!optDe('cps-composicao', 'Denominator', 'share').disabled,
       'no corte por tempo parcial "% do total" fica cinza');
    ok(!!optDe('cps-composicao', 'Chart', 'bars').disabled,
       '...e as barras tambem');
    ok(/four ways and publishes these two/.test(why('cps-composicao')),
       '...com o motivo medido: as 2 linhas indentadas sao 2 das 4 razoes publicadas');
    // A selecao cai de volta para o escopo do corte: as 6 marcadas por default sao de
    // motivo e duracao, entao sem o fallback este corte abriria com grafico VAZIO.
    ok(t.specs().length >= 1,
       'e o corte abre com alguma linha plotada, nao com um grafico vazio',
       t.specs().length + ' series');
    // Mas desmarcar tudo a mao NAO remarca: a condicao e "nada no escopo COM algo
    // marcado fora dele", nao "nada marcado".
    Object.keys(t.state.checked).forEach((k) => { t.state.checked[k] = false; });
    t.redraw();
    eq(t.specs().length, 0,
       'desmarcar tudo a mao deixa o grafico vazio, em vez de remarcar tres sozinho');
    clicar(pillDe('cps-composicao', 'eixo', 'By reason'));
    eq(t.specs().length, 0,
       '...e o fallback nao dispara em corte nenhum enquanto nada estiver marcado');
    R.achatar(t.arvoreAtual()).forEach(function(n) { t.state.checked[n.key] = true; });
    t.redraw();
    ok(t.specs().length === 4, 'remarcar a mao volta a plotar as 4 do corte');
  }
}

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

// ── 16. produtividade (prod2 / MSPC) ────────────────────────────────────────
secao('16. Produtividade e custos por setor maior');
(function () {
  const P = D.prod;
  const tab = R.TABS.prod;
  ok(!!tab, 'a aba de produtividade foi construida');

  // -- 16a. a grade e TRIMESTRAL, e a compressao nao pode desalinhar --------
  const passo = (ms(P.dates[1]) - ms(P.dates[0])) / MS_DIA;
  ok(passo > 85 && passo < 95,
     'a grade avanca de trimestre em trimestre (' + P.dates[0] + ' -> ' + P.dates[1] + ')',
     'passo de ' + passo + ' dias');
  const foraDoTri = P.dates.filter((d) => ['01', '04', '07', '10'].indexOf(d.slice(5, 7)) < 0);
  ok(!foraDoTri.length, 'toda data da grade e um inicio de trimestre',
     foraDoTri.slice(0, 3).join(', '));
  // O rotulo da coluna e o do hover saem da MESMA leitura do mes de inicio. O `%q` do
  // Plotly nao e verificavel sem browser -- nao esta no bundle 2.35.2 --, entao o hover
  // e montado em JS, e e isto que confere as duas pontas.
  ok(R.fmtQuarterShort('2026-04-01') === 'Q2/26'
     && R.fmtQuarter('2026-04-01') === '2026 Q2'
     && R.fmtQuarter('2026-10-01') === '2026 Q4'
     && R.fmtQuarter('2026-01-01') === '2026 Q1',
     'o trimestre sai do mes de inicio (01->Q1, 04->Q2, 10->Q4)',
     R.fmtQuarterShort('2026-04-01') + ' / ' + R.fmtQuarter('2026-10-01'));
  const th = [...doc.getElementById('th-prod').children[0].children]
    .map((x) => x.textContent).filter((t) => /^Q[1-4]\//.test(t));
  ok(th.length === 12, 'a tabela mostra 12 trimestres (3 anos, como as tabelas do release)',
     th.length + ' colunas: ' + th.join(' '));
  const rp = ultimaReact('chart-prod');
  ok(rp && rp.traces[0].customdata
     && rp.traces[0].customdata[0] === R.fmtQuarter(rp.traces[0].x[0]),
     'o hover carrega o rotulo de trimestre em customdata, nao um %q do Plotly',
     rp && JSON.stringify((rp.traces[0].customdata || []).slice(0, 2)));

  // -- 16b. a leitura ESCOLHE UMA SERIE, nao calcula ------------------------
  const chaveDe = (medida, dur) => ['nonfarm_business', medida, dur].join('|');
  ok(P.duracoes.map((d) => d.key).join(',') === 'tri_anual,ano_a_ano,indice',
     'as tres duracoes publicadas estao no payload, com a trimestral anualizada primeiro',
     P.duracoes.map((d) => d.key).join(','));
  P.duracoes.forEach((d) => {
    ok(!!P.series[chaveDe('produtividade', d.key)],
       'produtividade/nonfarm existe como serie propria na leitura ' + d.key);
  });
  const idx = P.series[chaveDe('produtividade', 'indice')];
  const pub = P.series[chaveDe('produtividade', 'tri_anual')];
  ok(Math.abs(idx.v[idx.v.length - 1] - 120.017) < 0.0005,
     'indice de produtividade do nonfarm em 2026 Q2 = 120,017 -- o release imprime 120,0',
     idx.v[idx.v.length - 1]);
  // As duas precisoes que a fonte usa, e o payload preserva as duas: o indice vem com
  // TRES decimais (a precisao com que o BLS calcula) e as variacoes com uma (a que ele
  // imprime). Guardar o indice arredondado a 1 casa faria a reconta errar 1,35 p.p. no
  // maximo -- medido -- e nada na tela mudaria de aparencia.
  const nDec = (v) => { const t = String(v); return t.indexOf('.') < 0 ? 0 : t.split('.')[1].length; };
  ok(idx.v.filter((v) => v != null && nDec(v) === 3).length > idx.v.length * 0.8,
     'o indice chega com 3 decimais (a precisao de calculo do BLS), nao com 1',
     idx.v.slice(-4).join(' '));
  ok(pub.v.every((v) => v == null || nDec(v) <= 1),
     'e as variacoes chegam com 1 decimal, como o BLS as publica',
     pub.v.slice(-4).join(' '));
  ok(Math.abs(pub.v[pub.v.length - 1] - 1.4) < 0.001,
     'variacao trimestral anualizada em 2026 Q2 = 1,4 (a manchete do release)',
     pub.v[pub.v.length - 1]);
  // A prova de que recomputar ERRA: a reconta a partir do indice de 1 decimal difere do
  // publicado. Se um dia a fabrica voltar a calcular esta leitura, isto pega.
  const n = idx.v.length;
  const recont = (Math.pow(idx.v[n - 1] / idx.v[n - 2], 4) - 1) * 100;
  ok(Math.abs(recont - pub.v[pub.v.length - 1]) <= 0.0501,
     'a reconta a partir do indice de 3 decimais CONCORDA com a taxa publicada dentro '
     + 'de meio digito (' + recont.toFixed(3) + ' contra ' + pub.v[pub.v.length - 1]
     + ') -- a pill le a serie porque o numero publicado e o citavel, nao porque a '
     + 'reconta erre', recont.toFixed(4));
  // Trocar a leitura tem de trocar a SERIE plotada, nao transformar a mesma.
  clicar(pillDe('prod', 'transform', 'Index 2017=100'));
  const plotIdx = ultimaReact('chart-prod').traces
    .find((t) => t.name === 'Nonfarm business');
  ok(plotIdx && Math.abs(plotIdx.y[plotIdx.y.length - 1] - 120.017) < 0.0005,
     'clicar em Index plota o indice publicado, nao uma variacao acumulada',
     plotIdx && plotIdx.y[plotIdx.y.length - 1]);
  clicar(pillDe('prod', 'transform', 'Q/Q annualized'));
  const plotTri = ultimaReact('chart-prod').traces
    .find((t) => t.name === 'Nonfarm business');
  ok(plotTri && Math.abs(plotTri.y[plotTri.y.length - 1] - 1.4) < 0.001,
     'e voltar para Q/Q plota 1,4 -- a mesma celula que o release imprime',
     plotTri && plotTri.y[plotTri.y.length - 1]);

  // -- 16c. nada e aditivo: os tres controles de aditividade estao fora -----
  ok(tab.tiposDisponiveis().length === 1 && tab.tiposDisponiveis()[0].key === 'nivel',
     'nao existe "% do total": nao ha total, os setores se contem',
     JSON.stringify(tab.tiposDisponiveis()));
  ok(!tab.barrasOk(), 'barras empilhadas desligadas em toda combinacao');
  const bar = pillDe('prod', 'kind', 'Stacked bars');
  ok(bar && bar.classList.contains('disabled'),
     'a pill de barras fica na tela, desabilitada');
  ok(bar && /overlap|do not add/i.test(bar.title || ''),
     'e o motivo exibido fala de sobreposicao/nao-aditividade, nao de "variacao percentual"',
     bar && bar.title);
  // Clicar nela nao pode mudar o estado.
  const kindAntes = tab.state.kind;
  clicar(bar);
  ok(tab.state.kind === kindAntes, 'e o clique nela nao muda o estado', tab.state.kind);
  // A razao numerica: dois indices de base 100 somam ~200.
  const mf = P.series[['manufacturing', 'produtividade', 'indice'].join('|')];
  const du = P.series[['manufacturing_durable', 'produtividade', 'indice'].join('|')];
  const nd = P.series[['manufacturing_nondurable', 'produtividade', 'indice'].join('|')];
  const razao = (du.v[du.v.length - 1] + nd.v[nd.v.length - 1]) / mf.v[mf.v.length - 1];
  ok(razao > 1.9 && razao < 2.15,
     'durable + nondurable da ' + razao.toFixed(2) + 'x manufacturing (indices nunca somam)',
     razao);

  // -- 16d. so existe dessazonalizado, e a pill diz isso -------------------
  const nsa = pills('prod', 'ajuste')
    .find((b) => /NSA|not adj/i.test(pillLabel(b)));
  ok(nsa && nsa.classList.contains('disabled'),
     'a pill NSA fica desabilitada (a pesquisa so sai ajustada)');
  ok(nsa && /adjusted only|no unadjusted/i.test(nsa.title || ''),
     'com o motivo no title', nsa && nsa.title);

  // -- 16e. a grade setor x medida e esburacada, e o buraco e dito ---------
  const soNfc = Object.keys(P.medidas).filter((m) => P.medidas[m].so_nfc);
  ok(soNfc.length === 4,
     'quatro medidas existem so nas corporacoes nao financeiras (a Tabela 6)',
     soNfc.join(', '));
  soNfc.forEach((m) => {
    ok(P.combos.indexOf('nonfarm_business|' + m) < 0
       && P.combos.indexOf('nonfinancial_corp|' + m) >= 0,
       m + ': publicada na nao financeira e nao no nonfarm business');
  });
  ok(P.combos.length === 79,
     '79 pares setor x medida de 114 possiveis -- a grade e esburacada por construcao',
     P.combos.length);
  ok(P.conceito.nonfarm_business === 'valor_adicionado'
     && P.conceito.manufacturing === 'setorial',
     'o conceito de produto difere entre business e transformacao (valor adicionado x setorial)',
     JSON.stringify(P.conceito));
  // Com os dois conceitos marcados (o default), o subtitulo tem de avisar -- o release
  // da esse aviso em prosa, e aqui ele sai do dado.
  const sub = doc.getElementById('cs-prod').textContent;
  ok(/two output concepts/i.test(sub),
     'o subtitulo avisa quando os dois conceitos de produto estao no mesmo grafico',
     sub.slice(0, 170));
  // Trocando para uma medida que so a nao financeira publica, o subtitulo diz de quem
  // falta -- um setor marcado sem dado sairia como linha vazia, sem sintoma nenhum.
  escolherNoGrupo('prod', 'medida', 'Unit profits');
  const sub2 = doc.getElementById('cs-prod').textContent;
  ok(/not published for/i.test(sub2),
     'e diz quais setores marcados nao publicam a medida escolhida',
     sub2.slice(0, 200));
  ok(/nonfinancial corporations only/i.test(doc.getElementById('hint-prod').innerHTML),
     'e a dica abaixo da tabela nomeia quem publica',
     doc.getElementById('hint-prod').innerHTML.slice(0, 200));
  escolherNoGrupo('prod', 'medida', 'Labor productivity');

  // -- 16f. o titulo do eixo troca com a duracao --------------------------
  clicar(pillDe('prod', 'transform', 'Index 2017=100'));
  const yIdx = tab.yTitle();
  clicar(pillDe('prod', 'transform', 'Q/Q annualized'));
  const yTri = tab.yTitle();
  clicar(pillDe('prod', 'transform', 'Y/Y'));
  const yYoy = tab.yTitle();
  ok(/index 2017=100/.test(yIdx) && !/%/.test(yIdx),
     'no indice o eixo nomeia a base e nao diz por cento', yIdx);
  ok(/% change/.test(yTri) && /annual rate/.test(yTri),
     'na trimestral o eixo diz que a taxa e anualizada', yTri);
  ok(/% change/.test(yYoy) && /a year earlier/.test(yYoy) && !/annual rate/.test(yYoy),
     'na anual o eixo diz "a year earlier" e NAO "annual rate" -- sao leituras diferentes',
     yYoy);
  clicar(pillDe('prod', 'transform', 'Q/Q annualized'));

  // -- 16g. a regua e a primeira pintura (as faces do bug de range) -------
  const iProd = CRU.indexOf('id="p-prod"');
  const painelProd = CRU.slice(iProd, CRU.indexOf('id="p-derived"'));
  ok(!/rangeselector:/.test(painelProd),
     'nenhum xaxis.rangeselector nativo no painel de produtividade');
  ok(painelProd.indexOf('id="rb-prod"') > painelProd.indexOf('id="chart-prod"'),
     'a regua de range vem DEPOIS do grafico na marcacao');
  const rel = relayoutsDe('chart-prod').filter((c) => c.upd && c.upd['xaxis.range']);
  ok(rel.length >= 1, 'a primeira pintura aplica uma janela de data calculada');
  const janela = rel[0].upd['xaxis.range'];
  const fimDado = ms(P.dates[P.dates.length - 1]);
  ok(Math.abs(ms(janela[1].slice(0, 10)) - fimDado) < 50 * MS_DIA,
     'e a borda direita fica a menos de meio trimestre do ultimo ponto (nao autorange)',
     janela.join(' .. '));
  ok(!ultimaReact('chart-prod').layout.xaxis
     || !ultimaReact('chart-prod').layout.xaxis.autorange,
     'e o layout nao pede autorange');

  // -- 16h. os ciclos: os graficos 3 e 4 do release, reproduzidos ---------
  const C = P.ciclos;
  ok(!!R.TABS.prod_ciclos, 'o card de ciclos foi construido');
  const PUB = {
    nonfarm_business: {'atual:produtividade': 2.1, 'atual:produto_real': 2.5,
                       'atual:horas_trabalhadas': 0.4,
                       'anterior:produtividade': 1.5, 'longo:produtividade': 2.1},
    manufacturing: {'atual:produtividade': 0.5, 'atual:produto_real': 0.2,
                    'atual:horas_trabalhadas': -0.3,
                    'anterior:produtividade': 0.1, 'longo:produtividade': 2.1},
  };
  Object.keys(PUB).forEach((setor) => {
    Object.keys(PUB[setor]).forEach((chave) => {
      const v = C.porSetor[setor].taxas[chave];
      ok(v != null && Math.abs(Math.round(v * 10) / 10 - PUB[setor][chave]) < 0.051,
         setor + '/' + chave + ' = ' + PUB[setor][chave] + '% (texto do release)', v);
    });
  });
  ok(C.porSetor.nonfarm_business.inicio === '1947Q1'
     && C.porSetor.manufacturing.inicio === '1987Q1',
     'a janela longa parte do inicio da serie de cada setor (1947Q1 e 1987Q1)',
     C.porSetor.nonfarm_business.inicio + ' / ' + C.porSetor.manufacturing.inicio);
  // A taxa de PONTA A PONTA nao e a media das trimestrais.
  const serieTri = P.series[['nonfarm_business', 'produtividade', 'tri_anual'].join('|')];
  const desde2019 = serieTri.v.slice(-26).filter((x) => x != null);
  const media = desde2019.reduce((a, b) => a + b, 0) / desde2019.length;
  ok(Math.abs(media - C.porSetor.nonfarm_business.taxas['atual:produtividade']) > 0.03,
     'a media das taxas trimestrais (' + media.toFixed(2) + ') difere da taxa entre as '
     + 'pontas (' + C.porSetor.nonfarm_business.taxas['atual:produtividade']
     + ') -- o release usa a segunda', media.toFixed(3));
  const ciclo = ultimaReact('chart-prod-ciclo');
  ok(ciclo && ciclo.layout.xaxis && ciclo.layout.xaxis.type === 'category',
     'o grafico de ciclos tem X categorico (as tres janelas)',
     ciclo && JSON.stringify(ciclo.layout.xaxis));
  ok(doc.getElementById('rb-prod-ciclo').style.display === 'none',
     'e a regua de tempo sai da tela nele (o X nao e tempo)',
     doc.getElementById('rb-prod-ciclo').style.display);
  ok(ciclo.layout.barmode === 'group',
     'as barras sao agrupadas e nao empilhadas: tres medidas independentes, nao partes',
     ciclo.layout.barmode);
  ok(ciclo.traces.length === 3 && ciclo.traces.every((t) => t.x.length === 3),
     'tres medidas x tres janelas', ciclo.traces.length);
  ok(/1947 Q1/.test(ciclo.traces[0].x[2]),
     'o rotulo da janela longa imprime o inicio da serie daquele setor',
     ciclo.traces[0].x.join(' | '));
  // Trocar de setor troca o rotulo da janela longa -- e a prova de que o inicio nao e
  // uma constante.
  clicar(pillDe('prod-ciclo', 'setor', 'Manufacturing'));
  const ciclo2 = ultimaReact('chart-prod-ciclo');
  ok(/1987 Q1/.test(ciclo2.traces[0].x[2]),
     'na transformacao a janela longa comeca em 1987 Q1, nao em 1947',
     ciclo2.traces[0].x[2]);
  ok(Math.abs(ciclo2.traces[0].y[0] - 0.5) < 0.001,
     'e a barra do ciclo atual marca 0,5% (o numero do grafico 4)',
     ciclo2.traces[0].y[0]);
  clicar(pillDe('prod-ciclo', 'setor', 'Nonfarm business'));

  // -- 16i. a prosa da aba e escrita para o leitor, nao para nos ----------
  // A nota entra por innerHTML e o stub de elemento nao deriva textContent dela --
  // ler o texto sem as tags e o unico jeito de afirmar sobre a prosa.
  const notas = ['note-prod', 'note-prod-ciclo']
    .map((id) => doc.getElementById(id).innerHTML.replace(/<[^>]*>/g, ''))
    .join(' ');
  const proibidos = ['calcTransform', 'makeGenericTab', 'payload', 'mt_produtividade',
                     'periodicidade', 'series_id', 'prod_tab', 'duracao'];
  const achados = proibidos.filter((t) => notas.indexOf(t) >= 0);
  ok(!achados.length, 'as notas da aba nao usam vocabulario de construcao',
     achados.join(', '));
  ok(notas.length > 900, 'e nao estao vazias de conteudo', notas.length);
})();

// ── resumo ──────────────────────────────────────────────────────────────────
console.log('\n' + '='.repeat(66));
console.log((asserts - falhas) + '/' + asserts + ' assercoes ok'
            + (falhas ? ', ' + falhas + ' FALHAS' : ''));
process.exit(falhas ? 1 : 0);
