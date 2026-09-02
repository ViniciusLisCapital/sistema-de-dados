// Testa a 4a tabela da aba Impulso do Panorama de Credito -- FLUXO FINANCEIRO e IMPULSO
// DE CREDITO no conceito do BCB -- executando o script REAL do HTML gerado contra um DOM
// stub e um Plotly stub.
//
// Roda com:
//     node tests/test_credit_fluxo_js.js
//
// Precisa de "reports/brasil/Credit.html" gerado:
//     uv run python -c "from analytics.brasil.credit.generate_report import run; run()"
//
// Por que este teste existe, alem do que ja cobre test_credit_ciclos_js.js:
//
//   (a) Esta tabela tem um seletor que troca a UNIDADE, nao so a serie. Fluxo e um nivel
//       em % do PIB; impulso e uma variacao em p.p. do PIB. Se o titulo do eixo, o hover
//       ou o cabecalho ficarem presos numa das duas, o grafico afirma a unidade errada em
//       metade dos estados -- e nenhuma excecao e lancada. As secoes 5 e 6 afirmam que os
//       tres mudam juntos.
//   (b) O impulso e DERIVADO no Python (Fluxo(t) - Fluxo(t-12)). A secao 3 refaz a conta
//       aqui, a partir da propria serie de fluxo do payload, e exige igualdade -- um erro
//       de deslocamento produziria uma serie plausivel, so que defasada.
//   (c) A arvore e uma decomposicao exata na fonte, e a fabrica so empilha certo se ela
//       for. A secao 2 afirma a aditividade no payload e a secao 7 no que chega ao
//       Plotly (topo da pilha == linha do total).
//   (d) O escopo e TRES series (Total/PJ/PF), 2 niveis -- o conjunto que as duas fontes
//       publicam. A secao 8 fixa isso: uma serie a mais significa que a quebra
//       Livre/Direcionado do boxe voltou, e foi ela que quebrou a aditividade da arvore
//       na primeira versao (pai e filho em vintages diferentes). Se voltar, tem de ser
//       de propósito e com a regra de emenda refeita, nao por acidente.
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
let asserts = 0;
function ok(cond, nome, detalhe) {
  asserts++;
  if (cond) { console.log('  ok    ' + nome); }
  else { falhas++; console.log('  FALHA ' + nome + (detalhe ? '  -- ' + detalhe : '')); }
}
function secao(t) { console.log('\n' + t); }

// -- DOM stub (mesmo de tests/test_credit_ciclos_js.js) ------------------------
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

function linhasDaTabela(tbody) {
  return tbody.children.map((tr) => {
    let cb = null, label = '';
    const valores = [];
    tr.children.forEach((td) => {
      td.children.forEach((c) => { if (c.tag === 'input') cb = c; });
      if (td.classList.contains('col-label')) {
        // So os nos de TEXTO: a celula carrega span.tree-toggle, span.row-n e, desde
        // 2026-08-28, button.info-btn ("i"). Filtrar por tag seria uma lista de
        // excecoes que envelhece -- ver .claude/rules/lis-dashboards.md.
        label = td.children.filter((c) => c.tag === '#text').map((c) => c.textContent).join('')
                || td.textContent;
      }
      if (td.classList.contains('col-value')) valores.push(td.textContent);
    });
    return { tr, cb, label: String(label).trim(), valores };
  });
}

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

// Pills: o relatorio as procura por document.querySelectorAll('#<grupo> .pill'). Sem
// isto, wirePills() nao acha nada e NENHUM seletor da aba fica clicavel -- o teste
// passaria a exercitar so o estado default, que e justamente o que ele nao precisa
// testar. As pills sao lidas do HTML gerado, com data-freq/data-variant reais.
const PILLS = {};
(CRU.match(/<div class="pill-group" id="[^"]+">[\s\S]*?<\/div>/g) || []).forEach((blk) => {
  const id = /id="([^"]+)"/.exec(blk)[1];
  const botoes = [];
  const re = /<button([^>]*)>([\s\S]*?)<\/button>/g;
  let m;
  while ((m = re.exec(blk)) !== null) {
    const attrs = m[1] || '';
    const el = new El('button');
    const cls = /class="([^"]*)"/.exec(attrs);
    el.className = cls ? cls[1] : '';
    const f = /data-freq="([^"]*)"/.exec(attrs);
    const v = /data-variant="([^"]*)"/.exec(attrs);
    if (f) el.dataset.freq = f[1];
    if (v) el.dataset.variant = v[1];
    el.textContent = m[2].replace(/<[^>]*>/g, '').trim();
    botoes.push(el);
  }
  PILLS[id] = botoes;
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
    createTextNode(t) { const n = new El('#text'); n.textContent = t; return n; },
    querySelector: () => null,
    querySelectorAll(sel) {
      if (sel === '.tab-btn') return tabBtns;
      if (sel === '.tab-panel') return tabPanels;
      const m = /^#([\w-]+) \.pill$/.exec(String(sel));
      if (m && PILLS[m[1]]) return PILLS[m[1]];
      return [];
    },
    addEventListener() {},
    body: new El('body'),
    documentElement: { clientWidth: 1400, clientHeight: 900 },
    _els: els, _tabPanels: tabPanels,
  };
}

function makePlotly(documento, chamadas) {
  function thenable(v) { return { then(f) { f(v); return thenable(v); }, catch() { return thenable(v); } }; }
  return {
    react(divId, traces, layout) {
      chamadas.push({ tipo: 'react', divId, traces, layout });
      const el = documento.getElementById(divId);
      el.data = traces;
      el._fullLayout = JSON.parse(JSON.stringify(layout || {}));
      el._fullLayout.xaxis = el._fullLayout.xaxis || {};
      if (!el._fullLayout.xaxis.type) el._fullLayout.xaxis.type = 'date';
      return thenable(el);
    },
    newPlot(divId, traces, layout) { return this.react(divId, traces, layout); },
    relayout(divId, upd) { chamadas.push({ tipo: 'relayout', divId, upd }); return thenable(documento.getElementById(divId)); },
  };
}

// -- Execucao ------------------------------------------------------------------
const doc = makeDom();
const chamadas = [];
global.document = doc;
global.window = { scrollX: 0, scrollY: 0 };
global.Option = function (label, value) { const o = new El('option'); o.textContent = label; o.value = value; return o; };
global.Plotly = makePlotly(doc, chamadas);

const EXPORTS = ['D', 'IMP_FLUXO_TAB', 'IMP_RECURSO_TAB', 'RENDERERS'];
let R;
try {
  new Function(SRC + ';global.__R = {' + EXPORTS.join(',') + '};')();
  R = global.__R;
} catch (e) {
  console.error('o script do relatorio lancou excecao ao carregar: ' + e.stack);
  process.exit(1);
}

const DIV = 'chart-imp-fluxo';
const F = R.D.fluxo || {};
const S = F.series || {};
const CHAVES = ['fluxo_total', 'fluxo_pj', 'fluxo_pf'];
// Tolerancias: sao o arredondamento do payload, nao folga de modelo.
// TOL      -- fluxo. `_load_flat` arredonda em 4 casas (+-0,5e-4 por valor); comparar
//             pai contra 2 filhos envolve 3 valores -> 1,5e-4.
// TOL_IMP  -- impulso. Cada ponto ja e a diferenca de DOIS fluxos arredondados
//             (+-1e-4) e e arredondado de novo (+-0,5e-4) -> 1,5e-4 por valor, 4,5e-4
//             nos 3 da comparacao. Medido: o pior caso real e 2,0e-4.
const TOL = 2e-4;
const TOL_IMP = 5e-4;

function mapa(chave, variante, freq) {
  const s = ((S[chave] || {})[variante] || {})[freq] || { dates: [], values: [] };
  const m = {};
  for (let i = 0; i < s.dates.length; i++) m[s.dates[i]] = s.values[i];
  return m;
}
function ultimoReact() { return chamadas.filter((x) => x.tipo === 'react' && x.divId === DIV).pop(); }
function clicar(grupo, pred) {
  const b = (PILLS[grupo] || []).find(pred);
  if (!b) { falhas++; asserts++; console.log('  FALHA pill nao encontrada em #' + grupo); return null; }
  b.fire('click');
  return b;
}
function fmt(v) {
  if (v == null || isNaN(v)) return '—';
  const r = Math.round(v * 100) / 100;
  if (r === 0) return '0,00';
  return (r > 0 ? '+' : '') + r.toFixed(2).replace('.', ',');
}
function colunas(headId) {
  const cab = doc.getElementById(headId).children[0];
  return (cab ? cab.children : []).filter((th) => th.classList.contains('col-value'))
    .map((th) => th.textContent);
}
function ultimasComValor(s, n) {
  return s.dates.filter((d, i) => s.values[i] != null).slice(-n);
}

// ==============================================================================
secao('1. Payload -- forma e cobertura');

ok(!!F.tree && F.tree.length === 1, 'D.fluxo.tree tem uma raiz');
ok(F.anchor === 'fluxo_total', 'ancora e fluxo_total', String(F.anchor));
ok(CHAVES.every((k) => !!S[k]), '3 series presentes', CHAVES.filter((k) => !S[k]).join(','));
ok(Object.keys(S).length === 3, 'e SO essas 3 -- nada de boxe voltou',
   Object.keys(S).join(','));
ok(CHAVES.every((k) => S[k].fluxo && S[k].impulso), 'toda serie tem as 2 variantes');
ok(CHAVES.every((k) => S[k].fluxo.m12 && S[k].fluxo.anual), 'toda variante tem as 2 frequencias');
ok(S.fluxo_total.fluxo.m12.dates.length >= 130, 'fluxo_total cobre boxe + edicao corrente',
   String(S.fluxo_total.fluxo.m12.dates.length));
ok(S.fluxo_total.fluxo.m12.dates[0] === '2015-01-01',
   'serie comeca em 2015-01 -- o alcance do boxe de mar/2025',
   S.fluxo_total.fluxo.m12.dates[0]);

// ==============================================================================
secao('2. Aditividade no payload -- a arvore e decomposicao, nao aproximacao');

['fluxo', 'impulso'].forEach((v) => {
  ['m12', 'anual'].forEach((fq) => {
    const t = mapa('fluxo_total', v, fq), pj = mapa('fluxo_pj', v, fq), pf = mapa('fluxo_pf', v, fq);
    let pior = 0, n = 0;
    Object.keys(t).forEach((d) => {
      if (t[d] == null || pj[d] == null || pf[d] == null) return;
      n++; pior = Math.max(pior, Math.abs(pj[d] + pf[d] - t[d]));
    });
    const lim = v === 'impulso' ? TOL_IMP : TOL;
    ok(n >= 5 && pior <= lim, 'PJ + PF = Total (' + v + '/' + fq + ', ' + n + ' pontos)',
       'pior ' + pior.toFixed(6));
  });
});


// ==============================================================================
secao('3. Impulso = Fluxo(t) - Fluxo(t-12), refeito aqui a partir do fluxo');

function menos12(d) {
  const y = +d.slice(0, 4), m = +d.slice(5, 7);
  const t = y * 12 + (m - 1) - 12;
  return String(Math.floor(t / 12)).padStart(4, '0') + '-'
       + String((t % 12) + 1).padStart(2, '0') + d.slice(7);
}
CHAVES.forEach((k) => {
  const fl = mapa(k, 'fluxo', 'm12'), im = mapa(k, 'impulso', 'm12');
  let pior = 0, n = 0, nulosOk = true;
  Object.keys(fl).forEach((d) => {
    const esperado = (fl[d] == null || fl[menos12(d)] == null) ? null : fl[d] - fl[menos12(d)];
    if (esperado === null) { if (im[d] != null) nulosOk = false; return; }
    if (im[d] == null) { nulosOk = false; return; }
    n++; pior = Math.max(pior, Math.abs(im[d] - esperado));
  });
  ok(n > 40 && pior <= TOL && nulosOk,
     k + ': impulso reproduz a diferenca de 12m (' + n + ' pontos)',
     'pior ' + pior.toFixed(6) + (nulosOk ? '' : ', nulos divergem'));
});

const primeiroImp = ultimasComValor(S.fluxo_total.impulso.m12, 1e9)[0];
ok(primeiroImp === '2016-01-01', 'primeiro impulso e 12 meses depois do inicio do fluxo', primeiroImp);

// ==============================================================================
secao('4. Tabela renderizada -- o default e o FLUXO');

R.RENDERERS.impulso();

const corpo = doc.getElementById('imp-fluxo-table-body');
let linhas = linhasDaTabela(corpo);
ok(linhas.length === 3, 'abre com 3 linhas (Total, PJ, PF)', String(linhas.length));
ok(linhas.map((l) => l.label).join('|') === 'Total|Pessoa Jurídica|Pessoa Física',
   'rotulos na ordem da arvore', linhas.map((l) => l.label).join('|'));
ok(colunas('imp-fluxo-table-head').length === 12, 'cabecalho com 12 colunas de mes',
   String(colunas('imp-fluxo-table-head').length));

const mFl = mapa('fluxo_total', 'fluxo', 'm12');
const ultFl = ultimasComValor(S.fluxo_total.fluxo.m12, 12);
ok(linhas[0].valores.join('|') === ultFl.map((d) => fmt(mFl[d])).join('|'),
   'celulas do Total batem com o payload (fluxo)', linhas[0].valores.join('|'));

// ==============================================================================
secao('5. Seletor de medida -- troca serie, unidade do eixo e unidade do hover');

const antes = ultimoReact();
ok(!!antes, 'grafico plotado no default');
ok(antes.layout.yaxis && antes.layout.yaxis.title.text === '% do PIB',
   'eixo Y do fluxo e "% do PIB"', JSON.stringify(antes.layout.yaxis && antes.layout.yaxis.title));
ok(antes.traces.every((t) => /% do PIB<extra>/.test(t.hovertemplate)),
   'hover do fluxo diz "% do PIB"');
ok(antes.traces.every((t) => !/p\.p\. do PIB/.test(t.hovertemplate)),
   'hover do fluxo NAO diz "p.p. do PIB"');

clicar('imp-fluxo-medida-group', (b) => b.dataset.variant === 'impulso');

const depois = ultimoReact();
ok(depois !== antes, 'clicar na pill re-renderiza');
ok(depois.layout.yaxis.title.text === 'p.p. do PIB', 'eixo Y do impulso e "p.p. do PIB"',
   depois.layout.yaxis.title.text);
ok(depois.traces.every((t) => /p\.p\. do PIB<extra>/.test(t.hovertemplate)),
   'hover do impulso diz "p.p. do PIB"');

linhas = linhasDaTabela(corpo);
const mIm = mapa('fluxo_total', 'impulso', 'm12');
const ultIm = ultimasComValor(S.fluxo_total.impulso.m12, 12);
ok(linhas[0].valores.join('|') === ultIm.map((d) => fmt(mIm[d])).join('|'),
   'celulas do Total batem com o payload (impulso)', linhas[0].valores.join('|'));
ok(linhas[0].valores.join('|') !== ultFl.map((d) => fmt(mFl[d])).join('|'),
   'a tabela realmente mudou de numero ao trocar a medida');

// ==============================================================================
secao('6. Cabecalho do grafico -- muda junto e imprime a janela plotada');

function head() {
  return {
    titulo: doc.getElementById('imp-fluxo-h-titulo').textContent,
    sub: doc.getElementById('imp-fluxo-h-sub').textContent,
    fonte: doc.getElementById('imp-fluxo-h-fonte').textContent,
  };
}
const hImp = head();
ok(/Impulso de Crédito/.test(hImp.titulo), 'titulo nomeia a medida corrente', hImp.titulo);
ok(/p\.p\. do PIB/.test(hImp.sub), 'subtitulo traz a unidade corrente', hImp.sub);
ok(/Fonte: BCB, anexo estatístico do RPM/.test(hImp.fonte), 'linha de fonte presente', hImp.fonte);
// `fmtMonthShort` imprime "Abr/26", com ano de 2 digitos -- exigir 4 aqui seria testar
// uma formatacao que o relatorio nao usa em lugar nenhum.
ok(/\w{3}\/\d{2} a \w{3}\/\d{2}/.test(hImp.fonte), 'linha de fonte traz a janela', hImp.fonte);
ok(/^Mensal/.test(hImp.sub), 'subtitulo diz a frequencia corrente', hImp.sub);

clicar('imp-fluxo-medida-group', (b) => b.dataset.variant === 'fluxo');
const hFlx = head();
ok(/Fluxo Financeiro/.test(hFlx.titulo) && /% do PIB/.test(hFlx.sub) && !/p\.p\./.test(hFlx.sub),
   'cabecalho volta para o fluxo', hFlx.titulo + ' / ' + hFlx.sub);

clicar('imp-fluxo-freq-group', (b) => b.dataset.freq === 'anual');
ok(/^Anual \(dezembro\)/.test(head().sub), 'subtitulo acompanha a frequencia', head().sub);
const cabAnual = colunas('imp-fluxo-table-head');
ok(cabAnual.length > 0 && cabAnual.every((t) => /^\d{4}$/.test(t)), 'cabecalho anual mostra anos',
   cabAnual.join(','));
clicar('imp-fluxo-freq-group', (b) => b.dataset.freq === 'm12');

// ==============================================================================
secao('7. Grafico -- barras empilhadas + linha, e o topo da pilha fecha com a linha');

const g = ultimoReact();
ok(g.layout.barmode === 'relative', 'barmode e relative, nunca stack', g.layout.barmode);
ok(Array.isArray(g.layout.shapes), 'layout leva as faixas de ciclo do Copom');
const barras = g.traces.filter((t) => t.type === 'bar');
const linha = g.traces.filter((t) => t.type === 'scatter');
ok(barras.length === 2 && linha.length === 1, 'default = 2 barras (PJ, PF) + 1 linha (Total)',
   barras.length + ' barras, ' + linha.length + ' linhas');

(function () {
  const soma = {};
  barras.forEach((t) => t.x.forEach((d, i) => {
    if (t.y[i] == null) return;
    soma[d] = (soma[d] || 0) + t.y[i];
  }));
  let pior = 0, n = 0;
  linha[0].x.forEach((d, i) => {
    if (linha[0].y[i] == null || soma[d] === undefined) return;
    n++; pior = Math.max(pior, Math.abs(soma[d] - linha[0].y[i]));
  });
  ok(n >= 90 && pior <= TOL, 'topo da pilha == linha do total (' + n + ' pontos)',
     'pior ' + pior.toFixed(6));
})();

// Selecao nao exaustiva deixa folga entre a pilha e a linha, de proposito -- e a leitura
// honesta de "o que falta para fechar o total". Desmarcar PF tem de produzir isso, e nao
// uma pilha que continua encostando na linha por acaso.
linhas = linhasDaTabela(corpo);
const trPF = linhas.find((l) => l.label === 'Pessoa Física');
ok(!!trPF, 'linha de PF presente para desmarcar');
if (trPF) {
  trPF.cb.checked = false;
  trPF.cb.fire('change');
  const g3 = ultimoReact();
  const b3 = g3.traces.filter((t) => t.type === 'bar');
  const l3 = g3.traces.filter((t) => t.type === 'scatter')[0];
  ok(b3.length === 1 && b3[0].name === 'Pessoa Jurídica', 'sobra so a barra de PJ',
     b3.map((t) => t.name).join(','));
  let folga = 0;
  b3[0].x.forEach((d, i) => {
    const j = l3.x.indexOf(d);
    if (j < 0 || b3[0].y[i] == null || l3.y[j] == null) return;
    folga = Math.max(folga, Math.abs(l3.y[j] - b3[0].y[i]));
  });
  ok(folga > TOL, 'a folga ate a linha do total aparece (selecao nao exaustiva)',
     'maior folga ' + folga.toFixed(3));
  trPF.cb.checked = true;
  trPF.cb.fire('change');
}

// ==============================================================================
secao('8. Escopo -- Total/PJ/PF, o conjunto que as duas fontes publicam');

const fimDe = (k) => ultimasComValor(S[k].fluxo.m12, 1)[0];
const iniDe = (k) => S[k].fluxo.m12.dates[0];
const fimTotal = fimDe('fluxo_total');
ok(CHAVES.every((k) => fimDe(k) === fimTotal), 'as 3 series terminam juntas', fimTotal);
ok(CHAVES.every((k) => iniDe(k) === '2015-01-01'), 'as 3 comecam juntas em 2015-01',
   CHAVES.map(iniDe).join(','));
// A emenda so e invisivel se as duas fontes estiverem na mesma unidade e sem correcao de
// nivel: um degrau muito acima do passo tipico da serie seria sinal de que alguem emendou
// R$ com % do PIB, que e o modo de falhar que o padrao de titulo existe para impedir.
(function () {
  const m = mapa('fluxo_total', 'fluxo', 'm12');
  const ds = S.fluxo_total.fluxo.m12.dates;
  const passos = [];
  for (let i = 1; i < ds.length; i++) {
    if (m[ds[i]] != null && m[ds[i - 1]] != null) passos.push(Math.abs(m[ds[i]] - m[ds[i - 1]]));
  }
  passos.sort((a, b) => a - b);
  const p99 = passos[Math.floor(passos.length * 0.99)];
  ok(passos.length > 100 && p99 < 1.5,
     'nenhum passo mensal absurdo -- as duas fontes estao na mesma unidade',
     'p99 = ' + p99.toFixed(3) + ', maior = ' + passos[passos.length - 1].toFixed(3));
})();
ok(!Object.keys(S).some((k) => /_livre|_direcionado/.test(k)),
   'a quebra Livre/Direcionado do boxe continua fora', Object.keys(S).join(','));
ok(F.tree[0].children.length === 2 && F.tree[0].children.every((c) => !c.children),
   'arvore tem 2 niveis: Total > PJ/PF',
   JSON.stringify(F.tree[0].children.map((c) => c.label)));

// ==============================================================================
secao('9. Regressao -- as 3 tabelas de Biggs et al. seguem inteiras');

['chart-imp-recurso', 'chart-imp-porte', 'chart-imp-ativ'].forEach((d) => {
  const c = chamadas.filter((x) => x.tipo === 'react' && x.divId === d).pop();
  ok(!!c && c.traces.length > 0, d + ' continua sendo plotado');
  ok(!!c && c.layout.barmode === 'relative', d + ' mantem barmode relative');
  ok(!!c && c.traces.every((t) => /p\.p\. do PIB<extra>/.test(t.hovertemplate)),
     d + ' mantem o hover em p.p. do PIB');
});
const recTab = linhasDaTabela(doc.getElementById('imp-recurso-table-body'));
ok(recTab.length >= 3 && recTab[0].label === 'Total Geral',
   'tabela (a) continua abrindo em Total Geral', recTab.map((l) => l.label).join('|'));

// -- Resultado -----------------------------------------------------------------
console.log('\n' + asserts + ' assercoes -- '
            + (falhas === 0 ? 'TODOS OS TESTES PASSARAM' : falhas + ' FALHA(S)'));
process.exit(falhas === 0 ? 0 : 1);
