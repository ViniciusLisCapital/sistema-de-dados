// Testa as FAIXAS DE CICLO DE POLITICA MONETARIA ao fundo dos 3 graficos da aba Impulso
// do Panorama de Credito, executando o script REAL do HTML gerado contra um DOM stub e
// um Plotly stub.
//
// Roda com:
//     node tests/test_credit_ciclos_js.js
//
// Precisa de "reports/brasil/Credit.html" gerado:
//     uv run python -c "from analytics.brasil.credit.generate_report import run; run()"
//
// A classificacao em si -- quais datas sao alta/manutencao/queda -- e testada em Python,
// em tests/test_credit_ciclos.py. Aqui se testa a outra metade, que e o que chega no
// Plotly, e sao modos de falhar diferentes: se `shapes` nao entrar no layout as faixas
// simplesmente nao aparecem, sem excecao nenhuma -- o Plotly aceita `shapes: undefined`
// calado, exatamente como aceitou x/y undefined no bug de 2026-08 do relatorio fiscal.
//
// Tres invariantes que so este lado consegue afirmar:
//   (a) as 3 chamadas de Plotly.react levam `shapes`, e continuam levando depois de um
//       re-render -- um layout remontado sem elas apaga o fundo em silencio;
//   (b) as cores do grafico (JS) e as da legenda (CSS) sao as MESMAS strings; elas moram
//       em dois lugares por necessidade, e nada alem deste teste as mantem juntas;
//   (c) nenhuma faixa passa da janela plotada -- `shapes` com xref:'x' entram no
//       autorange do Plotly, entao uma faixa solta antes do dado abre o grafico com um
//       vazio a esquerda, que e a mesma familia de bug ja documentada em
//       .claude/rules/lis-dashboards.md ("a vista que ninguem clica: o primeiro paint").
//
// O que ele NAO substitui: confirmacao visual num browser real.

const fs = require('fs');
const path = require('path');

const HTML = path.join(__dirname, '..', 'reports', 'brasil', 'Credit.html');
if (!fs.existsSync(HTML)) {
  console.error('reports/brasil/Credit.html nao existe -- gere o relatorio primeiro:');
  console.error('  uv run python -c "from analytics.brasil.credit.generate_report import run; run()"');
  process.exit(1);
}
const CRU = fs.readFileSync(HTML, 'utf8');
const blocos = CRU.match(/<script>([\s\S]*?)<\/script>/g) || [];
if (!blocos.length) { console.error('nenhum <script> encontrado no HTML'); process.exit(1); }
const SRC = blocos[blocos.length - 1].replace(/^<script>/, '').replace(/<\/script>$/, '');

let falhas = 0;
function ok(cond, nome, detalhe) {
  if (cond) { console.log('  ok    ' + nome); }
  else { falhas++; console.log('  FALHA ' + nome + (detalhe ? '  -- ' + detalhe : '')); }
}

// ── DOM stub ──────────────────────────────────────────────────────────────────
function El(tag) {
  this.tag = tag || 'div';
  this.children = []; this.style = {}; this.dataset = {};
  this._className = ''; this.textContent = ''; this.value = '';
  this._html = ''; this._listeners = {}; this._plotly = {};
  this.parentNode = null;
  const self = this;
  this.classList = {
    _set: {},
    add(c) { self.classList._set[c] = true; self._syncClass(); },
    remove(c) { delete self.classList._set[c]; self._syncClass(); },
    contains(c) { return !!self.classList._set[c]; },
    toggle(c, force) {
      const on = force === undefined ? !self.classList._set[c] : !!force;
      if (on) self.classList._set[c] = true; else delete self.classList._set[c];
      self._syncClass();
      return on;
    },
  };
}
El.prototype._syncClass = function () { this._className = Object.keys(this.classList._set).join(' '); };
Object.defineProperty(El.prototype, 'className', {
  get() { return this._className; },
  set(v) {
    this._className = v;
    this.classList._set = {};
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
El.prototype.setAttribute = function (k, v) { (this._attrs = this._attrs || {})[k] = v; };
El.prototype.addEventListener = function (k, f) { (this._listeners[k] = this._listeners[k] || []).push(f); };
El.prototype.fire = function (k, ev) { (this._listeners[k] || []).forEach((f) => f(ev)); };
El.prototype.on = function (k, f) { (this._plotly[k] = this._plotly[k] || []).push(f); };
El.prototype.closest = function () { return this._closest || null; };
El.prototype.contains = function () { return false; };
El.prototype.matches = function () { return false; };
El.prototype.getBoundingClientRect = function () {
  return { left: 10, right: 24, top: 40, bottom: 54, width: 14, height: 14 };
};
// Busca por classe na subarvore -- _ensureQuickRange escreve a barra de pills por
// innerHTML e logo em seguida procura o '.pill-group' que acabou de escrever.
El.prototype.querySelector = function (sel) {
  if (typeof sel === 'string' && sel.charAt(0) === '.') {
    const cls = sel.slice(1);
    const pilha = (this.children || []).slice();
    while (pilha.length) {
      const n = pilha.shift();
      if (n.classList && n.classList.contains(cls)) return n;
      pilha.push.apply(pilha, n.children || []);
    }
  }
  return null;
};
El.prototype.querySelectorAll = function () { return []; };
// Parse minimo de uma tag com class por nivel -- o suficiente para o
// '<div class="pill-group"></div>' de _ensureQuickRange virar um filho de verdade.
Object.defineProperty(El.prototype, 'innerHTML', {
  get() { return this._html; },
  set(v) {
    this._html = v;
    this.children = [];
    const re = /<(\w+)[^>]*class="([^"]*)"[^>]*>/g;
    let m;
    while ((m = re.exec(String(v))) !== null) {
      const filho = new El(m[1]);
      filho.className = m[2];
      this.appendChild(filho);
    }
  },
});

// Toda linha da tabela vira <tr> com <input type=checkbox> e <td class="col-label">; o
// harness precisa recuperar (label, checkbox) para poder MARCAR uma linha como o usuario
// faria, que e a unica forma de exercitar renderChart() com um corte diferente do default.
function linhasDaTabela(tbody) {
  return tbody.children.map((tr) => {
    let cb = null, label = '';
    tr.children.forEach((td) => {
      td.children.forEach((c) => { if (c.tag === 'input') cb = c; });
      if (td.classList.contains('col-label')) {
        // So os nos de TEXTO: a celula carrega span.tree-toggle, span.row-n e, desde
        // 2026-08-28, button.info-btn ("i"). Filtrar por tag seria uma lista de
        // excecoes que envelhece -- ver .claude/rules/lis-dashboards.md.
        label = td.children.filter((c) => c.tag === '#text').map((c) => c.textContent).join('')
                || td.textContent;
      }
    });
    return { tr, cb, label: String(label).trim() };
  });
}

// Os <select> do relatorio sao lidos como sel.options[i].value/.disabled pelas fabricas
// (findOption/applyMetricAvailability). Um stub que devolvesse um <div> vazio quebraria
// no carregamento -- e, pior, um stub com opcoes INVENTADAS testaria um relatorio que nao
// existe. Entao as opcoes vem do HTML gerado, com o `selected` definindo o valor inicial.
const SELECTS = {};
(CRU.match(/<select[^>]*id="([^"]+)"[^>]*>([\s\S]*?)<\/select>/g) || []).forEach((blk) => {
  const id = /id="([^"]+)"/.exec(blk)[1];
  const opts = [];
  const re = /<option([^>]*)>/g;
  let m;
  while ((m = re.exec(blk)) !== null) {
    const attrs = m[1] || '';
    const v = /value="([^"]*)"/.exec(attrs);
    opts.push({ value: v ? v[1] : '', disabled: false, selected: /\sselected/.test(attrs) });
  }
  SELECTS[id] = opts;
});

// Os pills (Nivel/Y-Y/..., Nominal/Real/% PIB, Mensal/Anual) sao lidos por
// document.querySelectorAll('#<grupo> .pill'), e makeHierTab tira de la o valor INICIAL
// do seletor -- `state.metric` so e definido pelo pill que ja vem com class="active".
// Um stub que devolvesse [] deixaria state.metric em null, as series sairiam vazias e o
// grafico seria testado sem nenhum dado. Como nos SELECTS, os pills vem do HTML gerado,
// nao inventados aqui.
const PILLS = {};
(CRU.match(/<div class="pill-group" id="([^"]+)">([\s\S]*?)<\/div>/g) || []).forEach((blk) => {
  const id = /id="([^"]+)"/.exec(blk)[1];
  const btns = [];
  const re = /<button([^>]*)>/g;
  let m;
  while ((m = re.exec(blk)) !== null) {
    const attrs = m[1] || '';
    const b = new El('button');
    b.className = (/class="([^"]*)"/.exec(attrs) || [null, ''])[1];
    const ds = /data-([a-zA-Z]+)="([^"]*)"/g;
    let d;
    while ((d = ds.exec(attrs)) !== null) b.dataset[d[1]] = d[2];
    btns.push(b);
  }
  PILLS[id] = btns;
});

const ABAS = ['saldo', 'concessao', 'impulso', 'taxa', 'inadimplencia', 'ptc', 'apendice'];
function makeDom() {
  const els = {};
  const tabBtns = ABAS.map((t) => { const b = new El('button'); b.dataset.tab = t; return b; });
  const tabPanels = ABAS.map((t) => { const p = new El('div'); p.id = 'tab-' + t; return p; });
  return {
    getElementById(id) {
      if (!els[id]) {
        const opts = SELECTS[id];
        const el = new El(opts ? 'select' : 'div');
        el.id = id;
        if (opts) {
          el.options = opts.map((o) => ({ value: o.value, disabled: o.disabled }));
          const sel = opts.find((o) => o.selected) || opts[0];
          el.value = sel ? sel.value : '';
        }
        if (/^chart-/.test(id)) {
          const card = new El('div'); card.classList.add('chart-card');
          const pai = new El('div');
          pai.appendChild(card); card.appendChild(el);
          el._closest = card;
        }
        els[id] = el;
      }
      return els[id];
    },
    createElement: (t) => new El(t),
    // O rotulo de uma folha entra por createTextNode -- sem isto a tabela
    // renderizaria linhas sem nome e linhasDaTabela() nao teria o que ler.
    createTextNode(t) { const n = new El('#text'); n.textContent = t; return n; },
    querySelector: () => null,
    querySelectorAll(sel) {
      if (sel === '.tab-btn') return tabBtns;
      if (sel === '.tab-panel') return tabPanels;
      const m = /^#([\w-]+)\s+\.pill$/.exec(sel || '');
      if (m && PILLS[m[1]]) return PILLS[m[1]];
      return [];
    },
    addEventListener() {},
    body: new El('body'),
    documentElement: { clientWidth: 1400, clientHeight: 900 },
    _els: els, _tabPanels: tabPanels,
  };
}

function makePlotly(doc, chamadas) {
  function thenable(v) { return { then(f) { f(v); return thenable(v); }, catch() { return thenable(v); } }; }
  return {
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
    relayout(divId, upd) { chamadas.push({ tipo: 'relayout', divId, upd }); return thenable(doc.getElementById(divId)); },
  };
}

// -- Execucao ------------------------------------------------------------------
const doc = makeDom();
const chamadas = [];
global.document = doc;
global.window = { scrollX: 0, scrollY: 0 };
global.Option = function (label, value) { const o = new El('option'); o.textContent = label; o.value = value; return o; };
global.Plotly = makePlotly(doc, chamadas);

const EXPORTS = ['D', 'CICLO_CORES', 'IMP_RECURSO_TAB', 'SALDO_TAB', 'RENDERERS'];
let R;
try {
  new Function(SRC + ';global.__R = {' + EXPORTS.join(',') + '};')();
  R = global.__R;
} catch (e) {
  console.error('o script do relatorio lancou excecao ao carregar: ' + e.stack);
  process.exit(1);
}

const TIPOS = ['alta', 'manutencao', 'queda'];
const ciclos = R.D.ciclos || [];
// Quem DEVE receber faixa, e quem deve continuar sem. A segunda metade e a que garante
// que o opt-in por chamada existe de verdade: `renderLineChart` e a mesma funcao nos
// dois grupos, e ligar as faixas por default pintaria Concessao, Taxa e Inadimplencia
// junto sem ninguem notar.
const COM_FAIXA = ['chart-saldo', 'chart-amplo',
                   'chart-imp-recurso', 'chart-imp-porte', 'chart-imp-ativ', 'chart-imp-fluxo'];
const SEM_FAIXA = ['chart-concessao', 'chart-taxa', 'chart-inad'];

function ultimoReact(div) {
  return chamadas.filter((x) => x.tipo === 'react' && x.divId === div).pop();
}
function shapesDe(div) {
  const c = ultimoReact(div);
  return (c && c.layout && c.layout.shapes) || [];
}

// O recorte esperado por grafico. Todos os graficos dividem UMA lista de ciclos, mas
// comecam em anos diferentes (saldo e recurso em 2000, porte e atividade em 2012) -- e
// uma shape com xref:'x' entra no autorange do Plotly, entao emitir a faixa de 2000 no
// grafico de porte puxaria o eixo 12 anos para tras. Este e o mesmo calculo que
// _ciclosShapes faz, refeito de forma independente: se as duas versoes discordarem, uma
// das duas esta errada.
function esperadas(traces) {
  const xs = [];
  (traces || []).forEach((t) => (t.x || []).forEach((v) => xs.push(v)));
  xs.sort();
  const lo = xs[0];
  const hi = new Date(Date.parse(xs[xs.length - 1] + 'T00:00:00Z') + 15 * 864e5).toISOString().slice(0, 10);
  return ciclos.filter((c) => c.ate > lo && c.de < hi)
               .map((c) => ({ de: c.de < lo ? lo : c.de, ate: c.ate > hi ? hi : c.ate, tipo: c.tipo }));
}

console.log('');
console.log('1. Payload das faixas (D.ciclos -- topo, nao dentro de uma aba)');
ok(ciclos.length > 20, 'ha faixas de ciclo no payload', ciclos.length + ' faixas');
ok(ciclos.every((c) => TIPOS.indexOf(c.tipo) >= 0), 'todo tipo esta no conjunto conhecido',
   JSON.stringify(ciclos.map((c) => c.tipo).filter((t) => TIPOS.indexOf(t) < 0)));
ok(ciclos.every((c) => c.de < c.ate), 'nenhuma faixa tem largura zero ou negativa');
const buracos = ciclos.slice(0, -1).filter((c, i) => c.ate !== ciclos[i + 1].de);
ok(buracos.length === 0, 'as faixas sao contiguas -- sem buraco e sem sobreposicao',
   JSON.stringify(buracos.slice(0, 2)));
ok(ciclos.every((c, i) => i === 0 || c.tipo !== ciclos[i - 1].tipo),
   'nenhuma faixa vizinha repete o tipo (a fusao de decisoes iguais rodou)');

console.log('');
console.log('2. As faixas chegam no Plotly como shapes');
chamadas.length = 0;
R.RENDERERS.saldo();
R.RENDERERS.impulso();
R.RENDERERS.concessao();
R.RENDERERS.taxa();
R.RENDERERS.inadimplencia();
COM_FAIXA.forEach((div) => {
  const c = ultimoReact(div);
  ok(!!c, div + ': Plotly.react foi chamado');
  const sh = shapesDe(div);
  const esp = esperadas(c && c.traces);
  ok(sh.length === esp.length, div + ': uma shape por faixa DENTRO da janela do grafico',
     sh.length + ' shapes para ' + esp.length + ' esperadas (payload tem ' + ciclos.length + ')');
  ok(sh.length > 0 && sh.every((s) => s.layer === 'below'),
     div + ': toda faixa fica ATRAS das series');
  ok(sh.length > 0 && sh.every((s) => s.yref === 'paper' && s.y0 === 0 && s.y1 === 1),
     div + ': toda faixa cobre a altura inteira (yref paper, 0..1)');
  ok(sh.length > 0 && sh.every((s) => s.xref === 'x' && s.type === 'rect' && s.line && s.line.width === 0),
     div + ': retangulo ancorado no eixo X, sem borda');
  ok(sh.every((s, i) => !!esp[i] && s.x0 === esp[i].de && s.x1 === esp[i].ate),
     div + ': as coordenadas batem com o recorte calculado a parte',
     JSON.stringify({ shape: sh[0], esperado: esp[0] }));
  ok(sh.every((s, i) => !!esp[i] && s.fillcolor === R.CICLO_CORES[esp[i].tipo]),
     div + ': a cor de cada faixa e a do seu tipo');
});

console.log('');
console.log('3. O opt-in por chamada -- quem NAO deve ter faixa nao tem');
SEM_FAIXA.forEach((div) => {
  const c = ultimoReact(div);
  ok(!!c, div + ': Plotly.react foi chamado (o grafico existe)');
  ok(shapesDe(div).length === 0, div + ': sem faixa de ciclo (nao pediu)',
     shapesDe(div).length + ' shapes');
});
// Concessao usa a MESMA makeHierTab()/renderLineChart() que Saldo -- se o flag nao
// existisse, os dois teriam faixa e a asserção acima seria a unica a acusar.
ok(shapesDe('chart-saldo').length > 0 && shapesDe('chart-concessao').length === 0,
   'Saldo e Concessao saem da mesma fabrica e so Saldo tem faixa (o opt-in funciona)');

console.log('');
console.log('4. O recorte por grafico morde de verdade');
const nSaldo = shapesDe('chart-saldo').length;
const nPorte = shapesDe('chart-imp-porte').length;
ok(nPorte < nSaldo, 'porte (serie desde 2012) recebe MENOS faixas que saldo (desde 2000)',
   nPorte + ' vs ' + nSaldo);
ok(nPorte > 0 && shapesDe('chart-imp-porte')[0].x0 >= '2012-01-01',
   'e a 1a faixa de porte nao vem de antes de 2012, quando a serie comeca',
   nPorte ? shapesDe('chart-imp-porte')[0].x0 : 'sem shapes');

console.log('');
console.log('5. As 3 cores existem e sao sutis');
TIPOS.forEach((t) => {
  const cor = R.CICLO_CORES[t];
  const m = /^rgba\(\s*\d+,\s*\d+,\s*\d+,\s*([0-9.]+)\s*\)$/.exec(cor || '');
  ok(!!m, t + ': a cor e um rgba valido', cor);
  ok(!!m && parseFloat(m[1]) > 0 && parseFloat(m[1]) <= 0.2,
     t + ': alfa entre 0 e 0,2 -- faixa e pano de fundo, nao destaque', cor);
});
ok(new Set(TIPOS.map((t) => R.CICLO_CORES[t])).size === 3, 'as 3 cores sao distintas entre si');

console.log('');
console.log('6. Legenda: o CSS repete a cor exata do grafico');
const SWATCH = { alta: 'sw-alta', manutencao: 'sw-manut', queda: 'sw-queda' };
TIPOS.forEach((t) => {
  const re = new RegExp('\\.ciclo-legend i\\.' + SWATCH[t] + '\\s*\\{[^}]*background:\\s*([^;]+);');
  const m = re.exec(CRU);
  ok(!!m, t + ': o quadradinho .' + SWATCH[t] + ' existe no CSS');
  ok(!!m && m[1].trim() === R.CICLO_CORES[t],
     t + ': a cor do CSS e identica a do grafico',
     m ? m[1].trim() + '  vs  ' + R.CICLO_CORES[t] : null);
});
// Nao se conta legenda: afirma-se que TODO grafico com faixa tem uma logo acima dele,
// dentro do mesmo .chart-card. Contar quebraria a cada grafico novo que alguem some.
COM_FAIXA.forEach((div) => {
  const i = CRU.indexOf('id="' + div + '"');
  const antes = i < 0 ? '' : CRU.slice(Math.max(0, i - 900), i);
  const card = antes.lastIndexOf('class="chart-card"');
  ok(card >= 0 && antes.indexOf('class="ciclo-legend"', card) >= 0,
     div + ': tem legenda de ciclo dentro do proprio cartao');
});
// A legenda e um <p> de proposito: `.chart-card > div` carimba 560px de altura em todo
// div filho direto do cartao, entao um <div> viraria uma tarja gigante em branco.
ok(!/<div class="ciclo-legend"/.test(CRU), 'nenhuma legenda e <div> (herdaria os 560px)');

console.log('');
console.log('7. Nenhuma faixa escapa da janela plotada');
COM_FAIXA.forEach((div) => {
  const c = ultimoReact(div);
  const xs = [];
  (c.traces || []).forEach((t) => (t.x || []).forEach((v) => xs.push(v)));
  xs.sort();
  const lo = xs[0], hi = xs[xs.length - 1];
  const sh = shapesDe(div);
  ok(sh.every((s) => s.x0 >= lo), div + ': nenhuma faixa comeca antes do 1o ponto plotado',
     'primeiro ponto ' + lo + ', primeira faixa ' + (sh[0] || {}).x0);
  // A folga na ponta direita e meia barra mensal, por construcao.
  const limite = new Date(Date.parse(hi + 'T00:00:00Z') + 16 * 864e5).toISOString().slice(0, 10);
  ok(sh.every((s) => s.x1 <= limite), div + ': nenhuma faixa passa meia barra do ultimo ponto',
     'ultimo ponto ' + hi + ', ultima faixa ' + (sh[sh.length - 1] || {}).x1);
});

console.log('');
console.log('8. O re-render nao perde as faixas');
const REDRAW = [['chart-imp-recurso', R.IMP_RECURSO_TAB], ['chart-saldo', R.SALDO_TAB]];
// Os dois `antes` tem de ser lidos ANTES de limpar `chamadas` -- limpar dentro do laco
// deixaria o segundo lendo 0 e comparando com 0 logo depois, o que passaria sempre.
const antes = REDRAW.map(([div]) => shapesDe(div).length);
chamadas.length = 0;
REDRAW.forEach(([, tab]) => tab.init());
REDRAW.forEach(([div], i) => {
  ok(antes[i] > 0 && shapesDe(div).length === antes[i],
     div + ': apos re-render o layout continua levando as faixas',
     shapesDe(div).length + ' vs ' + antes[i]);
});

console.log('');
console.log(falhas === 0 ? 'TUDO OK (' + ciclos.length + ' faixas no payload)' : falhas + ' FALHA(S)');
process.exit(falhas ? 1 : 0);
