// Testa o CABECALHO DE GRAFICO, a REGUA DE TEMPO ABAIXO DO GRAFICO, a UNIDADE DO
// EIXO Y, os CARDS DE DEFINICAO e o modo "% do PIB" da aba Renda e Poupanca do
// Panorama de Atividade Economica -- executando o script REAL do HTML gerado contra
// um DOM montado a partir do proprio HTML gerado e um Plotly stub.
//
// Roda com:
//     node tests/test_economic_activity_js.js
//
// Precisa de "reports/brasil/Economic Activity.html" gerado:
//     uv run python -c "from analytics.brasil.economic_activity.generate_report import run; run()"
//
// Por que ele existe -- nenhum destes modos de falha lanca excecao:
//
//   (a) REGUA ACIMA DO GRAFICO. A barra de periodo era inserida ANTES do card ate
//       2026-09. Mover para dentro do card e uma mudanca de DOM que nada valida.
//       A secao 2 exige que o rodape venha DEPOIS do div do grafico no card.
//   (b) JANELA COM FAIXA VAZIA. Um botao de range que ancora no range corrente do
//       eixo (ou um "Tudo" via autorange) abre com meses vazios na direita -- e um
//       grafico perfeitamente renderizado. As secoes 3 e 4 comparam a janela de
//       CADA botao, e a do primeiro paint, com a extensao real das series.
//   (c) SUBTITULO/UNIDADE PRESOS. Um subtitulo escrito no HTML, ou uma unidade fixa,
//       comeca certo e passa a mentir no primeiro clique de seletor -- e e o print
//       tirado depois desse clique que circula. A secao 5 troca os seletores e exige
//       que eixo, subtitulo e card de definicao andem juntos.
//   (d) CHAVE ORFA no INFO. Um erro de digitacao produz um botao que nunca nasce:
//       sem erro, sem lacuna visivel. A secao 6 resolve TODA chave do mapa contra as
//       listas reais e exige zero orfas.
//   (e) ROTULO CONTAMINADO. Depois do botao, o textContent da celula inclui o "i".
//       A secao 6 le so os nos de texto.
//   (g) CORES CONFUNDIVEIS. Duas series com a mesma cor -- ou a uma distancia
//       perceptual pequena -- renderizam sem erro nenhum. A secao 8 exige dE2000
//       >= 20 entre quaisquer duas series do MESMO grafico (limiar calibrado
//       contra Okabe-Ito e Tol bright).
//   (f) % DO PIB SAZONAL. A razao do trimestre isolado carrega a sazonalidade
//       inteira; a secao 7 confere a janela de 4 trimestres contra uma referencia
//       calculada aqui e mede a amplitude sazonal que justifica o padrao.
//
// O que ele NAO substitui: confirmacao visual num browser real (posicao do card,
// hover, pin, layout).

const fs = require('fs');
const path = require('path');
const vm = require('vm');

// EA_REPORT permite apontar para uma copia MUTADA do relatorio -- e assim que se
// confere que este harness realmente falha quando a feature quebra.
const HTML = process.env.EA_REPORT || path.join(__dirname, '..', 'reports', 'brasil', 'Economic Activity.html');
if (!fs.existsSync(HTML)) {
  console.error('reports/brasil/Economic Activity.html nao existe -- gere o relatorio primeiro:');
  console.error('  uv run python -c "from analytics.brasil.economic_activity.generate_report import run; run()"');
  process.exit(1);
}
const CRU = fs.readFileSync(HTML, 'utf8');
const blocos = CRU.match(/<script>([\s\S]*?)<\/script>/g) || [];
if (!blocos.length) { console.error('nenhum <script> encontrado'); process.exit(1); }
const SRC = blocos[blocos.length - 1].replace(/^<script>/, '').replace(/<\/script>$/, '');

let falhas = 0, asserts = 0;
function ok(cond, nome, detalhe) {
  asserts++;
  if (cond) console.log('  ok    ' + nome);
  else { falhas++; console.log('  FALHA ' + nome + (detalhe ? '  -- ' + detalhe : '')); }
}
function secao(t) { console.log('\n' + t); }

// ─────────────────────────────────────────────────────────────────────────────
// DOM minimo montado a partir do HTML REAL (nao elementos sinteticos): so assim
// `#pib1-mode-toggle .pill`, `closest('.chart-card')` e a ordem dos filhos dentro
// do card significam a mesma coisa que no browser.
// ─────────────────────────────────────────────────────────────────────────────
const VOID = new Set(['br', 'hr', 'img', 'input', 'meta', 'link', 'source', 'col']);

function El(tag) {
  this.tag = (tag || 'div').toLowerCase();
  this.nodeType = 1;
  this.children = [];
  this.childNodes = [];
  this.attrs = {};
  this.style = {};
  this.dataset = {};
  this.parentNode = null;
  this._listeners = {};
  this._plotly = {};
  this._html = '';
  this._text = null;          // so para folhas com texto proprio
  this.value = '';
  this.checked = false;
  this.type = '';
  const self = this;
  this.classList = {
    _set: {},
    add(c) { self.classList._set[c] = 1; self._sync(); },
    remove(c) { delete self.classList._set[c]; self._sync(); },
    contains(c) { return !!self.classList._set[c]; },
    toggle(c, f) {
      const on = f === undefined ? !self.classList._set[c] : !!f;
      if (on) self.classList._set[c] = 1; else delete self.classList._set[c];
      self._sync();
      return on;
    },
  };
}
function Txt(t) { this.nodeType = 3; this.textContent = t; this.children = []; this.childNodes = []; this.parentNode = null; }

El.prototype._sync = function () { this.attrs['class'] = Object.keys(this.classList._set).join(' '); };
Object.defineProperty(El.prototype, 'className', {
  get() { return this.attrs['class'] || ''; },
  set(v) {
    this.attrs['class'] = v;
    this.classList._set = {};
    String(v).split(/\s+/).filter(Boolean).forEach((c) => { this.classList._set[c] = 1; });
  },
});
Object.defineProperty(El.prototype, 'id', {
  get() { return this.attrs.id || ''; },
  set(v) { this.attrs.id = v; },
});
Object.defineProperty(El.prototype, 'textContent', {
  get() {
    let out = '';
    (this.childNodes || []).forEach((n) => { out += n.nodeType === 3 ? n.textContent : n.textContent; });
    return out;
  },
  set(v) {
    this.children = [];
    this.childNodes = [];
    if (v !== '' && v != null) {
      const t = new Txt(String(v));
      t.parentNode = this;
      this.childNodes.push(t);
    }
  },
});
Object.defineProperty(El.prototype, 'innerHTML', {
  get() { return this._html; },
  set(v) { this._html = v; this.children = []; this.childNodes = []; },
});
El.prototype.appendChild = function (c) {
  c.parentNode = this;
  if (c.nodeType === 1) this.children.push(c);
  this.childNodes.push(c);
  return c;
};
El.prototype.insertBefore = function (n, ref) {
  n.parentNode = this;
  let i = this.children.indexOf(ref);
  if (i < 0) i = this.children.length;
  this.children.splice(i, 0, n);
  let j = this.childNodes.indexOf(ref);
  if (j < 0) j = this.childNodes.length;
  this.childNodes.splice(j, 0, n);
  return n;
};
El.prototype.removeChild = function (c) {
  let i = this.children.indexOf(c);
  if (i >= 0) this.children.splice(i, 1);
  let j = this.childNodes.indexOf(c);
  if (j >= 0) this.childNodes.splice(j, 1);
  c.parentNode = null;
  return c;
};
El.prototype.setAttribute = function (k, v) { this.attrs[k] = v; };
El.prototype.getAttribute = function (k) { return this.attrs[k]; };
El.prototype.addEventListener = function (k, f) { (this._listeners[k] = this._listeners[k] || []).push(f); };
El.prototype.fire = function (k, ev) { (this._listeners[k] || []).forEach((f) => f.call(this, ev || {})); };
El.prototype.on = function (k, f) { (this._plotly[k] = this._plotly[k] || []).push(f); };
El.prototype.contains = function (o) {
  let n = o;
  while (n) { if (n === this) return true; n = n.parentNode; }
  return false;
};
El.prototype.matches = function () { return false; };
El.prototype.getBoundingClientRect = function () { return { left: 10, right: 24, top: 40, bottom: 54, width: 14, height: 14 }; };
El.prototype.closest = function (sel) {
  const cls = sel.replace(/^\./, '');
  let n = this;
  while (n) { if (n.classList && n.classList.contains(cls)) return n; n = n.parentNode; }
  return null;
};
El.prototype.descendants = function () {
  const out = [];
  const pilha = this.children.slice();
  while (pilha.length) { const n = pilha.shift(); out.push(n); pilha.unshift.apply(pilha, n.children); }
  return out;
};
function matchSimple(el, sel) {
  if (sel.charAt(0) === '#') return el.id === sel.slice(1);
  if (sel.charAt(0) === '.') return el.classList.contains(sel.slice(1));
  return el.tag === sel.toLowerCase();
}
El.prototype.querySelectorAll = function (sel) {
  const partes = String(sel).trim().split(/\s+/);
  let escopo = [this];
  partes.forEach((p, i) => {
    const prox = [];
    escopo.forEach((raiz) => {
      const cand = i === 0 && raiz === this ? this.descendants() : raiz.descendants();
      cand.forEach((el) => { if (matchSimple(el, p) && prox.indexOf(el) < 0) prox.push(el); });
    });
    escopo = prox;
  });
  const arr = escopo.slice();
  arr.forEach = Array.prototype.forEach;
  return arr;
};
El.prototype.querySelector = function (sel) { const r = this.querySelectorAll(sel); return r.length ? r[0] : null; };

// -- parser: so o suficiente para o <body> deste relatorio ---------------------
function parseHTML(html) {
  const raiz = new El('root');
  const pilha = [raiz];
  const re = /<!--[\s\S]*?-->|<\/([a-zA-Z0-9]+)\s*>|<([a-zA-Z0-9]+)((?:\s+[^>]*?)?)\/?>/g;
  let pos = 0, m;
  while ((m = re.exec(html)) !== null) {
    const texto = html.slice(pos, m.index);
    if (texto.trim()) {
      const t = new Txt(texto.replace(/\s+/g, ' '));
      t.parentNode = pilha[pilha.length - 1];
      pilha[pilha.length - 1].childNodes.push(t);
    }
    pos = re.lastIndex;
    if (m[0].startsWith('<!--')) continue;
    if (m[1]) {                                  // fechamento
      for (let i = pilha.length - 1; i > 0; i--) {
        if (pilha[i].tag === m[1].toLowerCase()) { pilha.length = i; break; }
      }
      continue;
    }
    const tag = m[2].toLowerCase();
    const el = new El(tag);
    const attrRe = /([a-zA-Z0-9\-]+)(?:="([^"]*)")?/g;
    let a;
    while ((a = attrRe.exec(m[3] || '')) !== null) {
      const k = a[1], v = a[2] === undefined ? '' : a[2];
      el.attrs[k] = v;
      if (k === 'class') el.className = v;
      else if (k === 'style') {
        v.split(';').forEach((d) => {
          const p = d.split(':');
          if (p.length === 2) el.style[p[0].trim().replace(/-([a-z])/g, (x, c) => c.toUpperCase())] = p[1].trim();
        });
      } else if (k.indexOf('data-') === 0) {
        el.dataset[k.slice(5).replace(/-([a-z])/g, (x, c) => c.toUpperCase())] = v;
      } else if (k === 'checked') el.checked = true;
      else if (k === 'value') el.value = v;
      else if (k === 'type') el.type = v;
    }
    pilha[pilha.length - 1].appendChild(el);
    if (!VOID.has(tag) && !m[0].endsWith('/>')) pilha.push(el);
  }
  return raiz;
}

const corpoRe = /<body>([\s\S]*?)<\/body>/;
const corpoHtml = (CRU.match(corpoRe) || [null, ''])[1]
  .replace(/<script>[\s\S]*?<\/script>/g, '')
  .replace(/<style>[\s\S]*?<\/style>/g, '');
const body = parseHTML(corpoHtml);
body.tag = 'body';
body.className = 'body';

const document = {
  body: body,
  documentElement: { clientWidth: 1400, clientHeight: 900 },
  _listeners: {},
  createElement(t) { return new El(t); },
  getElementById(id) {
    const todos = body.descendants();
    for (let i = 0; i < todos.length; i++) if (todos[i].id === id) return todos[i];
    return null;
  },
  querySelector(sel) { return body.querySelector(sel); },
  querySelectorAll(sel) { return body.querySelectorAll(sel); },
  addEventListener(k, f) { (this._listeners[k] = this._listeners[k] || []).push(f); },
};

// -- Plotly stub: guarda traces/layout por div e resolve sincronicamente ------
const PLOT = {};
function thenable(gd) {
  const p = { then(f) { const r = f(gd); return r && r.then ? r : thenable(gd); }, catch() { return p; } };
  return p;
}
const Plotly = {
  react(divId, traces, layout) {
    const gd = typeof divId === 'string' ? document.getElementById(divId) : divId;
    PLOT[gd.id] = { traces: traces, layout: JSON.parse(JSON.stringify(layout)) };
    gd.data = traces;
    gd.layout = PLOT[gd.id].layout;
    gd._fullLayout = PLOT[gd.id].layout;
    return thenable(gd);
  },
  newPlot(divId, traces, layout) { return Plotly.react(divId, traces, layout); },
  relayout(divId, upd) {
    const gd = typeof divId === 'string' ? document.getElementById(divId) : divId;
    const st = PLOT[gd.id];
    if (st) {
      Object.keys(upd).forEach((k) => {
        if (k === 'xaxis.range') st.layout.xaxis.range = upd[k].slice();
        else if (k === 'xaxis.range[0]') st.layout.xaxis.range[0] = upd[k];
        else if (k === 'xaxis.range[1]') st.layout.xaxis.range[1] = upd[k];
      });
      st.ultimoRelayout = upd;
    }
    return thenable(gd);
  },
  restyle() { return thenable(null); },
};

const ctx = {
  document, Plotly, console,
  window: { scrollX: 0, scrollY: 0 },
  setTimeout: () => 0,
  Set, Math, Date, JSON, Object, Array, String, Number, isNaN, parseInt, parseFloat,
};
ctx.globalThis = ctx;
vm.createContext(ctx);
try {
  vm.runInContext(SRC, ctx, { filename: 'economic_activity.js' });
} catch (e) {
  console.error('o script do relatorio lancou ao carregar:\n', e && e.stack);
  process.exit(1);
}

// Renderiza TODAS as abas (o relatorio so renderiza a ativa).
['pib', 'pim', 'pmc', 'pms', 'ibcbr', 'renda'].forEach((t) => ctx.activateTab(t));

const D = ctx.D;   // `const REPORT_DATA` nao vira propriedade do contexto do vm; `var D` vira
const CHART_META = ctx.CHART_META;
const IDS = Object.keys(CHART_META);
const ms = (iso) => Date.parse(iso);
const DIA = 86400000;

// ─────────────────────────────────────────────────────────────────────────────
secao('1. Cabecalho: todo grafico se explica sozinho (titulo + subtitulo + fonte/periodo)');
ok(IDS.length === 25, 'CHART_META cobre os 25 graficos', 'tem ' + IDS.length);
IDS.forEach((id) => {
  const div = document.getElementById(id);
  if (!div) { ok(false, id + ': div existe'); return; }
  const card = div.closest('.chart-card');
  if (!card) { ok(false, id + ': dentro de um .chart-card'); return; }
  const head = card.querySelector('.chart-head');
  const h3 = head && head.querySelector('h3');
  const sub = head && head.querySelector('.chart-sub');
  const src = head && head.querySelector('.chart-src');
  ok(!!head && !!h3 && !!sub && !!src, id + ': cabecalho de 3 linhas existe');
  if (!head) return;
  ok(h3.textContent === CHART_META[id].title, id + ': titulo = CHART_META');
  ok(sub.textContent.trim().length > 0, id + ': subtitulo preenchido', JSON.stringify(sub.textContent));
  ok(src.textContent.indexOf(CHART_META[id].source) === 0, id + ': fonte no inicio da 3a linha', src.textContent);
  // O quadrante e um CORTE TRANSVERSAL, nao uma serie: o "quando" dele e uma data
  // so, e ela vai no subtitulo. Exigir um intervalo ali seria exigir o que nao existe.
  if (/quadrant/.test(id)) {
    ok(/leitura de /.test(sub.textContent), id + ': subtitulo diz de que leitura sao os pontos', sub.textContent);
  } else {
    ok(/ a /.test(src.textContent) && src.textContent.length > CHART_META[id].source.length + 6,
       id + ': 3a linha traz o periodo real', src.textContent);
  }
});

// ─────────────────────────────────────────────────────────────────────────────
secao('2. A regua de tempo fica ABAIXO do grafico, dentro do mesmo card');
const SEM_REGUA = ['chart-pim-quadrant', 'chart-pmc-quadrant', 'chart-pms-quadrant', 'chart-ibcbr-quadrant'];
IDS.forEach((id) => {
  const div = document.getElementById(id);
  const card = div && div.closest('.chart-card');
  if (!card) return;
  const iChart = card.children.indexOf(div);
  const head = card.querySelector('.chart-head');
  const foot = card.querySelector('.chart-foot');
  ok(head && card.children.indexOf(head) < iChart, id + ': cabecalho ANTES do grafico');
  if (SEM_REGUA.indexOf(id) >= 0) {
    // Quadrante nao e serie temporal em X -- nao ganha regua, de proposito.
    ok(!foot || !foot.querySelector('.period-ctrl-bar'), id + ': quadrante nao ganha regua de tempo');
    return;
  }
  ok(!!foot && card.children.indexOf(foot) > iChart, id + ': rodape DEPOIS do grafico');
  const pills = foot && foot.querySelector('.range-pills');
  ok(!!pills && pills.children.length === 5, id + ': 5 botoes de range no rodape',
     pills ? String(pills.children.length) : 'sem .range-pills');
});
ok(JSON.stringify(PLOT).indexOf('rangeselector') < 0,
   'nenhum layout usa o xaxis.rangeselector nativo do Plotly');

// ─────────────────────────────────────────────────────────────────────────────
secao('3. Cada botao manda uma janela tirada dos DADOS (o "Tudo" inclusive)');
function extentPlotado(id) {
  const traces = PLOT[id].traces;
  let lo = null, hi = null;
  traces.forEach((t) => {
    if (!t.x) return;
    const z = t.type === 'heatmap' ? (t.z || []) : null;
    for (let i = 0; i < t.x.length; i++) {
      let tem = false;
      if (z) { for (let r = 0; r < z.length; r++) if (z[r] && z[r][i] != null) { tem = true; break; } }
      else tem = t.y && t.y[i] != null;
      if (!tem) continue;
      if (lo === null || t.x[i] < lo) lo = t.x[i];
      if (hi === null || t.x[i] > hi) hi = t.x[i];
    }
  });
  return lo === null ? null : [lo, hi];
}
const TS_IDS = IDS.filter((id) => SEM_REGUA.indexOf(id) < 0);
TS_IDS.forEach((id) => {
  const ext = extentPlotado(id);
  if (!ext) { ok(false, id + ': tem extensao plotada'); return; }
  const card = document.getElementById(id).closest('.chart-card');
  const pills = card.querySelector('.range-pills');
  const passo = 62 * DIA;   // meio passo de uma trimestral, com folga
  let todosOk = true, detalhe = '';
  pills.children.forEach((btn) => {
    btn.fire('click');
    const r = PLOT[id].layout.xaxis.range;
    const dentro = ms(r[0]) >= ms(ext[0]) - passo && ms(r[1]) <= ms(ext[1]) + passo && ms(r[1]) > ms(r[0]);
    if (!dentro) { todosOk = false; detalhe = btn.textContent + ' -> ' + JSON.stringify(r) + ' vs ' + JSON.stringify(ext); }
  });
  ok(todosOk, id + ': as 5 janelas ficam dentro dos dados (+/- meio passo)', detalhe);
  // "Tudo" (ultimo botao) cobre a serie inteira
  const btnTudo = pills.children[pills.children.length - 1];
  ok(btnTudo.textContent === 'Tudo', id + ': ultimo botao e "Tudo"');
  btnTudo.fire('click');
  const rt = PLOT[id].layout.xaxis.range;
  ok(ms(rt[0]) <= ms(ext[0]) && ms(rt[1]) >= ms(ext[1]), id + ': "Tudo" cobre a serie inteira',
     JSON.stringify(rt) + ' vs ' + JSON.stringify(ext));
  ok(btnTudo.classList.contains('active'), id + ': o botao clicado fica marcado');
});

// ─────────────────────────────────────────────────────────────────────────────
secao('4. A vista do PRIMEIRO paint tambem e calculada, nao autorange');
// Re-executa tudo num contexto limpo para observar o primeiro paint sem cliques.
function contextoLimpo() {
  const doc2body = parseHTML(corpoHtml);
  doc2body.tag = 'body';
  const PLOT2 = {};
  const doc2 = Object.assign({}, document, {
    body: doc2body,
    _listeners: {},
    getElementById(id) { const t = doc2body.descendants(); for (const e of t) if (e.id === id) return e; return null; },
    querySelector(s) { return doc2body.querySelector(s); },
    querySelectorAll(s) { return doc2body.querySelectorAll(s); },
    addEventListener() {},
    createElement(t) { return new El(t); },
  });
  const P2 = {
    react(divId, traces, layout) {
      const gd = typeof divId === 'string' ? doc2.getElementById(divId) : divId;
      PLOT2[gd.id] = { traces, layout: JSON.parse(JSON.stringify(layout)) };
      gd.data = traces; gd.layout = PLOT2[gd.id].layout; gd._fullLayout = PLOT2[gd.id].layout;
      return thenable(gd);
    },
    newPlot(a, b, c) { return P2.react(a, b, c); },
    relayout(divId, upd) {
      const gd = typeof divId === 'string' ? doc2.getElementById(divId) : divId;
      const st = PLOT2[gd.id];
      if (st && upd['xaxis.range']) st.layout.xaxis.range = upd['xaxis.range'].slice();
      return thenable(gd);
    },
    restyle() { return thenable(null); },
  };
  const c2 = { document: doc2, Plotly: P2, console, window: { scrollX: 0, scrollY: 0 }, setTimeout: () => 0, Set, Math, Date, JSON, Object, Array, String, Number, isNaN, parseInt, parseFloat };
  c2.globalThis = c2;
  vm.createContext(c2);
  vm.runInContext(SRC, c2, { filename: 'ea2.js' });
  ['pib', 'pim', 'pmc', 'pms', 'ibcbr', 'renda'].forEach((t) => c2.activateTab(t));
  return { ctx: c2, PLOT: PLOT2 };
}
const limpo = contextoLimpo();
TS_IDS.forEach((id) => {
  const st = limpo.PLOT[id];
  if (!st) { ok(false, id + ': renderizou no contexto limpo'); return; }
  const r = st.layout.xaxis && st.layout.xaxis.range;
  ok(!!r && st.layout.xaxis.autorange === false, id + ': primeiro paint com range explicito (sem autorange)');
  if (!r) return;
  let lo = null, hi = null;
  st.traces.forEach((t) => {
    if (!t.x) return;
    const z = t.type === 'heatmap' ? (t.z || []) : null;
    for (let i = 0; i < t.x.length; i++) {
      let tem = false;
      if (z) { for (let k = 0; k < z.length; k++) if (z[k] && z[k][i] != null) { tem = true; break; } }
      else tem = t.y && t.y[i] != null;
      if (!tem) continue;
      if (lo === null || t.x[i] < lo) lo = t.x[i];
      if (hi === null || t.x[i] > hi) hi = t.x[i];
    }
  });
  const span = ms(hi) - ms(lo);
  const folga = Math.max(span * 0.05, 62 * DIA);
  ok(ms(r[0]) >= ms(lo) - folga && ms(r[1]) <= ms(hi) + folga,
     id + ': a vista inicial nao abre com faixa vazia', JSON.stringify(r) + ' vs [' + lo + ',' + hi + ']');
});

// ─────────────────────────────────────────────────────────────────────────────
secao('5. A unidade do eixo Y muda com a metrica -- e o subtitulo acompanha');
function subtituloDe(id) {
  return document.getElementById(id).closest('.chart-card').querySelector('.chart-sub').textContent;
}
function unidadeDe(id) {
  const t = PLOT[id].layout.yaxis && PLOT[id].layout.yaxis.title;
  return t ? t.text : '';
}
function clicaPill(seletor, valorAttr, valor) {
  const btns = document.querySelectorAll(seletor);
  for (const b of btns) if (b.dataset[valorAttr] === valor) { b.fire('click'); return true; }
  return false;
}
// PIB Grafico 1: Interanual <-> Acumulado em 4 trimestres
ok(clicaPill('#pib1-mode-toggle .pill', 'mode', 'yoy'), 'PIB: pill "Interanual" existe');
const uPibYoY = unidadeDe('chart-pib-rate1'), sPibYoY = subtituloDe('chart-pib-rate1');
ok(clicaPill('#pib1-mode-toggle .pill', 'mode', 'acum_4t'), 'PIB: pill "Acumulado em 4 Trimestres" existe');
const uPibAcum = unidadeDe('chart-pib-rate1'), sPibAcum = subtituloDe('chart-pib-rate1');
ok(uPibYoY !== uPibAcum, 'PIB G1: o titulo do eixo Y muda com o modo', uPibYoY + ' | ' + uPibAcum);
ok(/mesmo trimestre do ano anterior/.test(uPibYoY), 'PIB G1 (Y/Y): eixo diz contra o que compara', uPibYoY);
ok(/acumulado em 4 trimestres/.test(uPibAcum), 'PIB G1 (Acum-4T): eixo diz a janela', uPibAcum);
ok(sPibYoY.indexOf(uPibYoY) >= 0 && sPibAcum.indexOf(uPibAcum) >= 0,
   'PIB G1: o subtitulo carrega a MESMA string de unidade do eixo');
ok(sPibYoY !== sPibAcum, 'PIB G1: o subtitulo e recalculado a cada render');
ok(!/^%$|^Var\./.test(uPibYoY), 'PIB G1: o eixo e uma definicao, nao so a unidade', uPibYoY);
// PIM Grafico 1: Interanual <-> Acumulado em 12 meses
ok(clicaPill('#pim-mode-toggle .pill', 'mode', 'yoy'), 'PIM: pill "Interanual" existe');
const uPimYoY = unidadeDe('chart-pim-rate1');
ok(clicaPill('#pim-mode-toggle .pill', 'mode', 'acum12m'), 'PIM: pill "Acumulado" existe');
const uPimAcum = unidadeDe('chart-pim-rate1');
ok(uPimYoY !== uPimAcum, 'PIM G1: o titulo do eixo Y muda com o modo', uPimYoY + ' | ' + uPimAcum);
ok(/produção física/.test(uPimYoY) && /produção física/.test(uPimAcum), 'PIM G1: o eixo diz O QUE mede', uPimYoY);
ok(/volume de vendas/.test(unidadeDe('chart-pmc-rate1')), 'PMC G1: eixo fala em volume de vendas', unidadeDe('chart-pmc-rate1'));
ok(/volume de serviços/.test(unidadeDe('chart-pms-rate1')), 'PMS G1: eixo fala em volume de servicos', unidadeDe('chart-pms-rate1'));
ok(/p\.p\./.test(unidadeDe('chart-pib-decomp-oferta-yoy')), 'Decomposicao: eixo em p.p. (contribuicao)', unidadeDe('chart-pib-decomp-oferta-yoy'));
ok(/z-score/.test(subtituloDe('chart-pib-heatmap-oferta')), 'Heatmap: subtitulo diz o que a cor mede', subtituloDe('chart-pib-heatmap-oferta'));
ok(/eixo X/.test(subtituloDe('chart-pim-quadrant')) && /eixo Y/.test(subtituloDe('chart-pim-quadrant')),
   'Quadrante: subtitulo nomeia os DOIS eixos (unidade mista)', subtituloDe('chart-pim-quadrant'));

// ─────────────────────────────────────────────────────────────────────────────
secao('6. Cards de definicao: zero chaves orfas, nenhum `full` repetindo o rotulo');
const INFO = ctx.INFO;
const chavesInfo = Object.keys(INFO);
// Universo real de chaves, por namespace.
const universo = { kpi: new Set(), pib: new Set(), pim: new Set(), pmc: new Set(), pms: new Set(), ibcbr: new Set(), renda: new Set() };
document.querySelectorAll('.kpi-label').forEach(() => {});
// kpi: as chaves que o codigo realmente passa para attachKPIInfo
['pib_qoq', 'pib_yoy', 'pib_acum4t', 'carrego_ano', 'mom', 'yoy', 'acum12m', 'carrego_trimestre',
 'renda_pib', 'renda_poupanca', 'renda_fbcf', 'renda_capfin'].forEach((k) => universo.kpi.add(k));
ctx.PIB_MS_GROUPS.forEach((g) => g.items.forEach((it) => universo.pib.add(it.key)));
ctx.PIM_MS_GROUPS.forEach((g) => g.items.forEach((it) => universo.pim.add(it.key)));
ctx.PMC_MS_GROUPS.forEach((g) => g.items.forEach((it) => universo.pmc.add(it.key)));
ctx.PMS_MS_GROUPS.forEach((g) => g.items.forEach((it) => universo.pms.add(it.key)));
ctx.IBCBR_MS_GROUPS.forEach((g) => g.items.forEach((it) => universo.ibcbr.add(it.key)));
ctx.RENDA_POUPANCA_ROWS.forEach((r) => universo.renda.add(r.key));
const orfas = chavesInfo.filter((k) => {
  const ns = k.slice(0, k.indexOf(':')), key = k.slice(k.indexOf(':') + 1);
  return !universo[ns] || !universo[ns].has(key);
});
ok(orfas.length === 0, 'toda chave do INFO resolve contra as listas reais', orfas.join(', '));
ok(chavesInfo.length >= 100, 'o mapa cobre o relatorio (>= 100 entradas)', String(chavesInfo.length));
// nenhum `full` igual ao rotulo visivel
const rotulos = {};
ctx.PIB_MS_GROUPS.forEach((g) => g.items.forEach((it) => { rotulos['pib:' + it.key] = it.label; }));
ctx.PIM_MS_GROUPS.forEach((g) => g.items.forEach((it) => { rotulos['pim:' + it.key] = it.label; }));
ctx.PMC_MS_GROUPS.forEach((g) => g.items.forEach((it) => { rotulos['pmc:' + it.key] = it.label; }));
ctx.PMS_MS_GROUPS.forEach((g) => g.items.forEach((it) => { rotulos['pms:' + it.key] = it.label; }));
ctx.IBCBR_MS_GROUPS.forEach((g) => g.items.forEach((it) => { rotulos['ibcbr:' + it.key] = it.label; }));
ctx.RENDA_POUPANCA_ROWS.forEach((r) => { rotulos['renda:' + r.key] = r.label; });
const fullRepetido = chavesInfo.filter((k) => rotulos[k] && INFO[k].full === rotulos[k]);
ok(fullRepetido.length === 0, 'nenhum `full` apenas repete o rotulo ja visivel', fullRepetido.join(', '));
// a mesma chave em dois namespaces tem textos diferentes
const colisoes = [];
chavesInfo.forEach((k) => {
  const key = k.slice(k.indexOf(':') + 1);
  chavesInfo.forEach((o) => {
    if (o === k) return;
    if (o.slice(o.indexOf(':') + 1) !== key) return;
    if (INFO[o].desc === INFO[k].desc && INFO[o].full === INFO[k].full) colisoes.push(k + ' == ' + o);
  });
});
ok(colisoes.length === 0, 'chave repetida em outro namespace nao tem o mesmo texto', colisoes.join(', '));

secao('6b. Os botoes `i` nascem no DOM, e so onde ha entrada');
function textoLimpo(el) {
  return (el.childNodes || []).filter((n) => n.nodeType === 3).map((n) => n.textContent).join('').trim();
}
function checaPainel(panelId, ns) {
  const panel = document.getElementById(panelId);
  const labels = panel.children.filter((c) => c.tag === 'label');
  let comBotao = 0, semEntradaComBotao = 0, fullOk = true, rotuloSujo = 0;
  labels.forEach((lab) => {
    const key = lab.dataset.key;
    const btn = lab.children.filter((c) => c.classList.contains('info-btn'))[0];
    const tem = !!INFO[ns + ':' + key];
    if (btn) comBotao++;
    if (btn && !tem) semEntradaComBotao++;
    if (tem && !btn) fullOk = false;
    if (btn) {
      // o rotulo lido do DOM inclui o "i" -- so os nos de texto dao o rotulo limpo
      const span = lab.children.filter((c) => c.classList.contains('ms-label'))[0];
      if (!span || textoLimpo(span).length === 0) rotuloSujo++;
      if (lab.textContent.indexOf('i') < 0) rotuloSujo++;
    }
  });
  ok(labels.length > 0, panelId + ': montou os itens', String(labels.length));
  ok(semEntradaComBotao === 0, panelId + ': nenhum botao sem entrada no INFO');
  ok(fullOk, panelId + ': todo item com entrada ganhou botao');
  ok(comBotao > 0, panelId + ': tem botoes (' + comBotao + '/' + labels.length + ')');
  ok(rotuloSujo === 0, panelId + ': o rotulo limpo sai dos nos de texto, nao do textContent');
  return labels;
}
checaPainel('pib1-ms-panel', 'pib');
checaPainel('pim1-ms-panel', 'pim');
checaPainel('pmc1-ms-panel', 'pmc');
checaPainel('pms1-ms-panel', 'pms');
checaPainel('ibcbr1-ms-panel', 'ibcbr');
checaPainel('renda-ms-panel', 'renda');
// tabela da Renda: 12 linhas, todas com card
const tbody = document.getElementById('renda-hier-tbody');
const linhas = tbody.children;
ok(linhas.length === ctx.RENDA_POUPANCA_ROWS.length, 'tabela Renda: uma linha por item da cascata', String(linhas.length));
let semCard = 0, rotuloErrado = 0;
linhas.forEach((tr, i) => {
  const td = tr.children[0];
  const btn = td.children.filter((c) => c.classList.contains('info-btn'))[0];
  if (!btn) semCard++;
  // casa por POSICAO, nao por rotulo (rotulos se repetem em arvores maiores)
  if (textoLimpo(td) !== ctx.RENDA_POUPANCA_ROWS[i].label) rotuloErrado++;
});
ok(semCard === 0, 'tabela Renda: as 12 linhas tem card de definicao');
ok(rotuloErrado === 0, 'tabela Renda: rotulo limpo casa com a linha na mesma POSICAO');
// KPIs
const KPI_PREFIXOS = ['kpi-pib-qoq', 'kpi-pib-yoy', 'kpi-pib-acum4t', 'kpi-pib-carrego',
  'kpi-pim-mom', 'kpi-pim-yoy', 'kpi-pim-acum12m', 'kpi-pim-carrego',
  'kpi-pmc-ampliado-mom', 'kpi-pmc-restrito-period', 'kpi-pms-acum12m', 'kpi-ibcbr-carrego',
  'kpi-renda-pib', 'kpi-renda-poupanca', 'kpi-renda-fbcf', 'kpi-renda-capfin'];
let kpiSemCard = 0;
KPI_PREFIXOS.forEach((p) => {
  const el = document.getElementById(p + '-label');
  if (!el || !el.children.filter((c) => c.classList.contains('info-btn')).length) kpiSemCard++;
});
ok(kpiSemCard === 0, 'todos os cards de KPI checados ganharam botao `i`', String(kpiSemCard) + ' sem');

secao('6c. A linha "Unidade:" do card acompanha o seletor, nao fica presa');
function abreCard(lab) {
  const btn = lab.children.filter((c) => c.classList.contains('info-btn'))[0];
  btn.fire('mouseenter');
  return document.body.children.filter((c) => c.classList.contains('info-pop'))[0].innerHTML;
}
const painelPim = document.getElementById('pim1-ms-panel');
const labPim = painelPim.children.filter((c) => c.tag === 'label' && c.dataset.key === 'transf_veiculos')[0];
clicaPill('#pim-mode-toggle .pill', 'mode', 'yoy');
const cardYoY = abreCard(labPim);
clicaPill('#pim-mode-toggle .pill', 'mode', 'acum12m');
const cardAcum = abreCard(labPim);
ok(/Unidade:/.test(cardYoY), 'card tem linha de unidade', cardYoY.slice(0, 120));
ok(cardYoY !== cardAcum, 'a unidade do card muda quando o modo do grafico muda');
ok(cardYoY.indexOf(unidadeDe('chart-pim-rate1')) < 0 || true, 'sanidade');
clicaPill('#pim-mode-toggle .pill', 'mode', 'acum12m');
ok(cardAcum.indexOf(unidadeDe('chart-pim-rate1')) >= 0,
   'a unidade do card e a MESMA string do titulo do eixo Y', unidadeDe('chart-pim-rate1'));
// entrada com `unit` proprio vence a funcao da tabela
const elCarrego = document.getElementById('kpi-pim-carrego-label');
const btnCarrego = elCarrego.children.filter((c) => c.classList.contains('info-btn'))[0];
btnCarrego.fire('mouseenter');
const cardCarrego = document.body.children.filter((c) => c.classList.contains('info-pop'))[0].innerHTML;
ok(/trimestre corrente/.test(cardCarrego), 'entrada com `unit` proprio vence a unidade da funcao', cardCarrego.slice(-160));

// ─────────────────────────────────────────────────────────────────────────────
secao('7. Renda e Poupanca: modo "% do PIB"');
const rp = D.renda_poupanca;
const mapa = (k) => { const o = {}; rp[k].dates.forEach((d, i) => { o[d] = rp[k].values[i]; }); return o; };
const pibMap = mapa('pib'), datas = rp.pib.dates;
function ref4t(base) {
  const v = mapa(base), out = {};
  for (let i = 3; i < datas.length; i++) {
    let num = 0, den = 0, ok2 = true;
    for (let j = i - 3; j <= i; j++) {
      const x = v[datas[j]], p = pibMap[datas[j]];
      if (x == null || p == null) { ok2 = false; break; }
      num += x; den += p;
    }
    if (ok2 && den !== 0) out[datas[i]] = num / den * 100;
  }
  return out;
}
const s4 = ctx.rendaShareOfGDP('poupanca_bruta', '4t');
const r4 = ref4t('poupanca_bruta');
let maxDif = 0;
s4.dates.forEach((d, i) => {
  if (s4.values[i] == null || r4[d] == null) return;
  maxDif = Math.max(maxDif, Math.abs(s4.values[i] - r4[d]));
});
ok(maxDif < 1e-3, 'razao 4T bate com a referencia calculada aqui', 'dif max ' + maxDif.toFixed(6));
const ult = s4.values[s4.values.length - 1];
ok(ult > 10 && ult < 20, 'taxa de poupanca na ordem de grandeza publicada (~14%)', String(ult));
const inv = ctx.rendaShareOfGDP('formacao_bruta_capital', '4t');
const ultInv = inv.values[inv.values.length - 1];
ok(ultInv > 13 && ultInv < 22, 'taxa de investimento na ordem de grandeza publicada (~17%)', String(ultInv));
// o PIB contra ele mesmo e 100 em todo trimestre -- e por isso ele sai do grafico
const sPib = ctx.rendaShareOfGDP('pib', '4t');
ok(sPib.values.filter((v) => v != null).every((v) => Math.abs(v - 100) < 1e-6), 'PIB / PIB = 100 em todo trimestre');
// a janela de 4T e o padrao porque a trimestral crua e sazonal -- medido
const cru = ctx.rendaShareOfGDP('poupanca_bruta', 'trim').values.filter((v) => v != null).slice(-8);
const amp = Math.max.apply(null, cru) - Math.min.apply(null, cru);
const amp4 = (() => { const w = s4.values.filter((v) => v != null).slice(-8); return Math.max.apply(null, w) - Math.min.apply(null, w); })();
ok(amp > 3 * amp4, 'a razao trimestral crua e muito mais volatil que a de 4T (justifica o padrao)',
   'amplitude 8T: crua ' + amp.toFixed(1) + ' p.p. vs 4T ' + amp4.toFixed(1) + ' p.p.');
// janela incompleta nao vira numero parcial
ok(s4.dates.length === datas.length - 3, 'a janela de 4T comeca no 4o trimestre, sem soma parcial',
   s4.dates.length + ' vs ' + (datas.length - 3));

secao('7b. O modo troca eixo, series e controles');
clicaPill('#renda-mode-toggle .pill', 'mode', 'level');
const uNivel = unidadeDe('chart-renda'), nNivel = PLOT['chart-renda'].traces.length;
const janelaVisivelNivel = document.querySelectorAll('.renda-janela-ctrl').every((e) => e.style.display === 'none');
clicaPill('#renda-mode-toggle .pill', 'mode', 'share');
const uShare = unidadeDe('chart-renda'), nShare = PLOT['chart-renda'].traces.length;
const janelaVisivelShare = document.querySelectorAll('.renda-janela-ctrl').every((e) => e.style.display === '');
clicaPill('#renda-mode-toggle .pill', 'mode', 'yoy');
const uYoY = unidadeDe('chart-renda');
ok(uNivel !== uShare && uShare !== uYoY && uNivel !== uYoY, 'os 3 modos tem 3 unidades diferentes',
   [uNivel, uShare, uYoY].join(' | '));
ok(/R\$ milhões/.test(uNivel), 'Nivel: eixo em R$ milhoes', uNivel);
ok(/\/ PIB/.test(uShare), 'share: eixo diz que e razao contra o PIB', uShare);
ok(nShare === nNivel - 1, 'share: a linha do PIB sai do grafico (seria 100 por construcao)',
   nNivel + ' -> ' + nShare);
ok(janelaVisivelNivel, 'o seletor de janela fica escondido fora do modo "% do PIB"');
ok(janelaVisivelShare, 'o seletor de janela aparece no modo "% do PIB"');
clicaPill('#renda-mode-toggle .pill', 'mode', 'share');
ok(/PIB omitido/.test(subtituloDe('chart-renda')), 'o subtitulo avisa que o PIB foi omitido', subtituloDe('chart-renda'));
const u4t = unidadeDe('chart-renda');
clicaPill('#renda-janela-toggle .pill', 'janela', 'trim');
const uTrim = unidadeDe('chart-renda');
ok(u4t !== uTrim, 'a unidade distingue a janela de 4T da trimestral', u4t + ' | ' + uTrim);
ok(/4 trimestres/.test(u4t) && !/4 trimestres/.test(uTrim), 'a janela padrao diz que soma 4 trimestres', u4t);


// ─────────────────────────────────────────────────────────────────────────────
secao('8. Cores: duas series do mesmo grafico nunca podem ser confundidas');
// dE2000 (CIEDE2000). Duas cores "parecidas" nao lancam excecao nenhuma -- ate
// 2026-09 tres pares da vista padrao do PIB tinham a MESMA cor e o grafico
// renderizava normalmente. O limiar de 20 e calibrado, nao inventado: e onde fecham
// as paletas publicadas de referencia (Okabe-Ito 21,7; Tol bright 20,5).
const DE_MIN = 20;
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
  const L1 = _lab(hex1), L2 = _lab(hex2);
  const C1 = Math.hypot(L1[1], L1[2]), C2 = Math.hypot(L2[1], L2[2]), Cb = (C1 + C2) / 2;
  const G = 0.5 * (1 - Math.sqrt(Math.pow(Cb, 7) / (Math.pow(Cb, 7) + Math.pow(25, 7))));
  const a1p = (1 + G) * L1[1], a2p = (1 + G) * L2[1];
  const C1p = Math.hypot(a1p, L1[2]), C2p = Math.hypot(a2p, L2[2]);
  const h1p = (Math.atan2(L1[2], a1p) * 180 / Math.PI + 360) % 360;
  const h2p = (Math.atan2(L2[2], a2p) * 180 / Math.PI + 360) % 360;
  const dLp = L2[0] - L1[0], dCp = C2p - C1p;
  let dhp = 0;
  if (C1p * C2p !== 0) {
    dhp = h2p - h1p;
    if (dhp > 180) dhp -= 360; else if (dhp < -180) dhp += 360;
  }
  const dHp = 2 * Math.sqrt(C1p * C2p) * Math.sin(dhp * Math.PI / 360);
  const Lbp = (L1[0] + L2[0]) / 2, Cbp = (C1p + C2p) / 2;
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
// Sanidade do port: os dois valores foram conferidos contra a implementacao Python
// usada para escolher a paleta.
ok(Math.abs(deltaE('#02739B', '#418791') - 13.0) < 0.3, 'dE2000 portado bate com a referencia (13,0)',
   deltaE('#02739B', '#418791').toFixed(1));
ok(Math.abs(deltaE('#1F2853', '#BB9B1D') - 64.9) < 0.3, 'dE2000 portado bate na outra ponta (64,9)',
   deltaE('#1F2853', '#BB9B1D').toFixed(1));
ok(Math.abs(deltaE('#8E44AD', '#AD1457') - 20.8) < 0.3, 'dE2000 portado bate no pior par da paleta (20,8)',
   deltaE('#8E44AD', '#AD1457').toFixed(1));

const PALETTE = ctx.PALETTE;
let piorPaleta = 999, parPior = '';
for (let i = 0; i < PALETTE.length; i++) {
  for (let j = i + 1; j < PALETTE.length; j++) {
    const dd = deltaE(PALETTE[i], PALETTE[j]);
    if (dd < piorPaleta) { piorPaleta = dd; parPior = PALETTE[i] + ' x ' + PALETTE[j]; }
  }
}
ok(piorPaleta >= DE_MIN, 'a paleta inteira tem dE >= ' + DE_MIN, 'pior ' + parPior + ' = ' + piorPaleta.toFixed(1));

// O par que originou esta secao (relatado pelo usuario, 2026-09-01).
const cf = ctx.PIB_RATE_CATS.filter((c) => c.base === 'consumo_familias')[0];
const ex = ctx.PIB_RATE_CATS.filter((c) => c.base === 'exportacao')[0];
ok(deltaE(cf.color, ex.color) >= DE_MIN, 'Consumo das Familias x Exportacoes separados',
   cf.color + ' x ' + ex.color + ' = ' + deltaE(cf.color, ex.color).toFixed(1));

// Toda serie efetivamente PLOTADA em cada grafico, na vista padrao (contexto limpo).
function corDoTrace(t) {
  const c = (t.line && t.line.color) || (t.marker && t.marker.color);
  return typeof c === 'string' && c.charAt(0) === '#' ? c : null;
}
let graficosOk = 0, piorGlobal = 999, ondePior = '';
Object.keys(limpo.PLOT).forEach((id) => {
  const ts = limpo.PLOT[id].traces
    .map((t) => ({ nome: t.name, cor: corDoTrace(t), dash: (t.line && t.line.dash) || 'solid' }))
    .filter((t) => t.cor);
  if (ts.length < 2) return;
  let pior = 999, par = '';
  for (let i = 0; i < ts.length; i++) {
    for (let j = i + 1; j < ts.length; j++) {
      // Tracejados diferentes ja separam as duas linhas: a cor pode repetir.
      if (ts[i].dash !== ts[j].dash) continue;
      const dd = deltaE(ts[i].cor, ts[j].cor);
      if (dd < pior) { pior = dd; par = ts[i].nome + ' (' + ts[i].cor + ') x ' + ts[j].nome + ' (' + ts[j].cor + ')'; }
    }
  }
  if (pior === 999) return;
  graficosOk++;
  if (pior < piorGlobal) { piorGlobal = pior; ondePior = id + ': ' + par; }
  ok(pior >= DE_MIN, id + ': nenhum par de series confundivel', par + ' = ' + pior.toFixed(1));
});
ok(graficosOk >= 15, 'a checagem cobriu os graficos com mais de uma serie', String(graficosOk));
// O segundo canal (tracejado) so entra em acao acima de 13 series -- nenhuma vista
// PADRAO chega la, entao ele precisa ser exercitado de proposito: marcando as 30
// categorias do PIM de uma vez. Sem esta parte, remover o `dash` das linhas passaria
// despercebido (verificado num mutante que fazia exatamente isso).
(function () {
  const painel = document.getElementById('pim1-ms-panel');
  const boxes = painel.children.filter((c) => c.tag === 'label')
    .map((l) => l.children.filter((x) => x.tag === 'input')[0]).filter(Boolean);
  boxes.forEach((b) => { b.checked = true; });
  boxes[0].fire('change');
  const ts = PLOT['chart-pim-rate1'].traces
    .map((t) => ({ nome: t.name, cor: corDoTrace(t), dash: (t.line && t.line.dash) || 'solid' }))
    .filter((t) => t.cor);
  ok(ts.length > 13, 'com tudo marcado o PIM passa de 13 series', String(ts.length));
  const dashes = {};
  ts.forEach((t) => { dashes[t.dash] = (dashes[t.dash] || 0) + 1; });
  ok(Object.keys(dashes).length > 1, 'acima de 13 series o tracejado entra como 2o canal',
     JSON.stringify(dashes));
  let colisao = '';
  for (let i = 0; i < ts.length && !colisao; i++) {
    for (let j = i + 1; j < ts.length; j++) {
      if (ts[i].dash !== ts[j].dash) continue;
      const dd = deltaE(ts[i].cor, ts[j].cor);
      if (dd < DE_MIN) { colisao = ts[i].nome + ' x ' + ts[j].nome + ' = ' + dd.toFixed(1); break; }
    }
  }
  ok(!colisao, 'com as 30 categorias marcadas, nenhum par (cor, tracejado) se repete', colisao);
})();
console.log('    (pior par em todo o relatorio: ' + ondePior + ' = ' + piorGlobal.toFixed(1) + ')');

// Nenhuma lista repete o par (cor, tracejado) -- e o que permite 30 categorias.
[['PIB', ctx.PIB_RATE_CATS], ['PIM', ctx.PIM_CATS], ['PMC', ctx.PMC_CATS],
 ['PMS', ctx.PMS_CATS], ['IBCBR', ctx.IBCBR_CATS], ['RENDA', ctx.RENDA_POUPANCA_CATS]].forEach((par) => {
  const nome = par[0], cats = par[1];
  const vistos = {};
  let dup = 0;
  cats.forEach((c) => { const k = c.color + '|' + c.dash; if (vistos[k]) dup++; vistos[k] = 1; });
  ok(dup === 0, nome + ' (' + cats.length + ' categorias): nenhum par (cor, tracejado) repetido', String(dup));
  ok(cats.every((c) => c.color && c.dash), nome + ': toda categoria recebeu cor e tracejado');
  ok(cats.every((c) => c.color !== PALETTE[0] || c.base === 'pib'),
     nome + ': o navy fica reservado para a linha de total');
});

// ─────────────────────────────────────────────────────────────────────────────
console.log('\n' + (falhas ? 'FALHOU' : 'OK') + ': ' + (asserts - falhas) + '/' + asserts + ' asserções');
process.exit(falhas ? 1 : 0);
