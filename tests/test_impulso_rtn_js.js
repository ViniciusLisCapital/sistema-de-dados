// Testa a secao "Impulso via Resultado Primario -- RTN (acima da linha)" da aba Impulso
// Fiscal, executando o script REAL do HTML gerado contra um DOM stub e um Plotly stub.
//
// Roda com:
//     node tests/test_impulso_rtn_js.js
//
// Precisa de "reports/brasil/Fiscal Policy.html" gerado:
//     uv run python -c "from analytics.brasil.fiscal_policy.generate_report import run; run()"
//
// Por que um harness e nao um teste em Python sobre o payload: o bug que este relatorio ja
// teve em producao (ver impulsoRPEsfera() no report.html) foi um ACESSOR devolvendo a lista
// crua em vez de {dates, values}. O payload estava perfeito, a reconciliacao em Python
// passava, e as 5 barras do grafico saiam vazias -- o Plotly aceita x/y undefined sem
// lancar nada. So um teste que olha os TRACES pega isso, e e por isso que as asserções
// abaixo afirmam sobre o que chega no Plotly, nao sobre D.
//
// O que ele NAO substitui: confirmacao visual num browser real.

const fs = require('fs');
const path = require('path');

const HTML = path.join(__dirname, '..', 'reports', 'brasil', 'Fiscal Policy.html');
if (!fs.existsSync(HTML)) {
  console.error('reports/brasil/Fiscal Policy.html nao existe -- gere o relatorio primeiro:');
  console.error('  uv run python -c "from analytics.brasil.fiscal_policy.generate_report import run; run()"');
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
El.prototype.addEventListener = function (k, f) { (this._listeners[k] = this._listeners[k] || []).push(f); };
El.prototype.fire = function (k, ev) { (this._listeners[k] || []).forEach((f) => f(ev)); };
El.prototype.on = function (k, f) { (this._plotly[k] = this._plotly[k] || []).push(f); };
El.prototype.closest = function () { return this._closest || null; };
El.prototype.contains = function () { return false; };
El.prototype.matches = function () { return false; };   // inclui ':hover' do cartão de definição
El.prototype.getBoundingClientRect = function () {
  return { left: 10, right: 24, top: 40, bottom: 54, width: 14, height: 14 };
};
El.prototype.setAttribute = function (k, v) { (this._attrs = this._attrs || {})[k] = v; };
El.prototype.getAttribute = function (k) { return (this._attrs || {})[k]; };
// Resolve seletor de CLASSE (o unico que o relatorio usa em elemento: '.range-bar',
// '.range-btn'). Um stub que devolvesse sempre null faria _ensureRangeBar criar uma
// regua nova a cada redesenho -- e o teste passaria medindo a ultima, escondendo
// justamente o vazamento de DOM que ele deveria pegar.
El.prototype.querySelector = function (sel) {
  if (!sel || sel[0] !== '.') return null;
  const cls = sel.slice(1);
  for (let i = 0; i < this.children.length; i++) {
    const c = this.children[i];
    if (c.classList && c.classList.contains(cls)) return c;
    const d = c.querySelector(sel);
    if (d) return d;
  }
  return null;
};
El.prototype.querySelectorAll = function (sel) {
  if (!sel || sel[0] !== '.') return [];
  const cls = sel.slice(1), out = [];
  (function walk(n) {
    n.children.forEach((c) => { if (c.classList && c.classList.contains(cls)) out.push(c); walk(c); });
  })(this);
  return out;
};
Object.defineProperty(El.prototype, 'innerHTML', {
  get() { return this._html; },
  set(v) {
    this._html = v; this.children = [];
    // Um <select> populado por innerHTML precisa passar a ter options/value, senao
    // o codigo que le sel.value trabalha com '' e produz series vazias sem erro --
    // foi assim que a secao Balanco por Entidade ficou fora do harness ate 2026-08-28.
    if (this.tag === 'select') {
      const opts = [];
      const re = /<option([^>]*)>/g;
      let m;
      while ((m = re.exec(String(v))) !== null) {
        const a = m[1] || '';
        const val = /value="([^"]*)"/.exec(a);
        opts.push({ value: val ? val[1] : '', disabled: false, selected: /\sselected/.test(a) });
      }
      if (opts.length) {
        this.options = opts.map((o) => ({ value: o.value, disabled: o.disabled }));
        const sel = opts.find((o) => o.selected) || opts[0];
        this.value = sel ? sel.value : '';
      }
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
        // Só os nós de TEXTO: depois que o botão "i" entrou na célula, filtrar por tag
        // ('span' da seta, 'button' do info) vira uma lista de exceções que envelhece,
        // e o textContent cru passa a trazer o "i" junto com o rótulo. É o gotcha que o
        // próprio padrão documenta.
        label = td.children.filter((c) => c.tag === '#text').map((c) => c.textContent).join('')
                || td.textContent;
      }
    });
    let info = null;
    tr.children.forEach((td) => td.children.forEach((c) => {
      if (c.tag === 'button' && c.className === 'info-btn') info = c;
    }));
    return { tr, cb, info, label: String(label).trim() };
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

const ABAS = ['gfsm', 'dlsp', 'investimento', 'impulso', 'apendice'];
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

// ── Execucao ──────────────────────────────────────────────────────────────────
const doc = makeDom();
const chamadas = [];
global.document = doc;
global.window = { scrollX: 0, scrollY: 0 };
global.Option = function (label, value) { const o = new El('option'); o.textContent = label; o.value = value; return o; };
global.Plotly = makePlotly(doc, chamadas);

const EXPORTS = ['D', 'IMPULSO_RTN_TAB', 'IMPULSO_RP_TAB', 'impulsoRTNTotal', 'impulsoRTNSerie',
                 'impulsoRPTotal', 'iegTotal', 'renderImpulsoCombinado', 'RENDERERS',
                 'NODE_INFO', 'infoOf', 'attachInfo', 'GFSM_TAB', 'RTN_TAB',
                 'IEG_HIER_TAB', 'CREDITO_OFICIAL_TAB', 'renderDlspTab', 'renderInvestimentoTab'];
let R;
try {
  new Function(SRC + ';global.__R = {' + EXPORTS.join(',') + '};')();
  R = global.__R;
} catch (e) {
  console.error('o script do relatorio lancou excecao ao carregar: ' + e.stack);
  process.exit(1);
}

const G = R.D.impulso_rtn || {};
const N = (G.dates || []).length;

console.log('\n1. Payload');
ok(!!R, 'script executa sem excecao');
ok(N > 300, 'impulso_rtn tem historia mensal longa', N + ' meses');
ok(Object.keys(G.series || {}).length === 34, 'as 34 rubricas da arvore estao no payload',
   Object.keys(G.series || {}).length);
ok((G.impulso || []).length === N && (G.impulso_quarter || []).length === N,
   'as duas variantes do total tem o comprimento do grid');
// Ids duplicados: o stub guarda um elemento por id, o browser devolve o PRIMEIRO --
// uma colisao faria a tabela ser escrita por cima de outro elemento sem erro nenhum.
const ids = (CRU.match(/ id="[^"]+"/g) || []).map((s) => s.trim());
const vistos = {}, dups = [];
ids.forEach((i) => { if (vistos[i]) dups.push(i); vistos[i] = true; });
ok(dups.length === 0, 'nenhum id duplicado no HTML gerado', dups.join(', '));
// A regra de CSS que da largura aos divs de grafico: fora dela o div colapsa para ~0 e o
// grafico nao aparece (gotcha ja documentado, ja aconteceu duas vezes neste relatorio).
ok(/#chart-impulso-rtn[,\s]/.test(CRU), 'chart-impulso-rtn esta na regra de dimensao do CSS');
ok(!!SELECTS['impulso-rtn-accum-select'] && SELECTS['impulso-rtn-accum-select'].length === 2,
   'o seletor de Nivel da secao existe no HTML com as 2 opcoes',
   JSON.stringify(SELECTS['impulso-rtn-accum-select'] || null));

console.log('\n2. Acessores devolvem {dates, values} -- a classe de bug de 2026-08');
const tot = R.impulsoRTNTotal('acum12m');
ok(Array.isArray(tot.dates) && Array.isArray(tot.values) && tot.dates.length === N,
   'impulsoRTNTotal devolve {dates, values} preenchidos');
['receita_liquida', 'despesa_total', 'pessoal_encargos_sociais', 'discricionarias_saude'].forEach((k) => {
  const s = R.impulsoRTNSerie(k, 'acum12m');
  ok(Array.isArray(s.dates) && s.dates.length === N && s.values.length === N,
     'impulsoRTNSerie("' + k + '") devolve {dates, values} alinhados ao grid');
});
ok(R.impulsoRTNSerie('nao_existe', 'acum12m').dates.length === 0,
   'serie inexistente devolve vazio em vez de undefined');

console.log('\n3. init() desenha barras E linha (nao um grafico vazio)');
R.IMPULSO_RTN_TAB.init();
const desenhos = chamadas.filter((c) => c.tipo === 'react' && c.divId === 'chart-impulso-rtn');
ok(desenhos.length >= 1, 'chart-impulso-rtn recebeu um react');
const traces = desenhos[desenhos.length - 1].traces || [];
ok(traces.length === 3, 'default: 2 barras (receita, despesa) + 1 linha de total', traces.length);
const barras = traces.filter((t) => t.type === 'bar');
const linha = traces.filter((t) => t.type !== 'bar')[0];
ok(barras.length === 2, 'duas barras', barras.length);
ok(!!linha, 'linha de total presente');
barras.forEach((b, i) => {
  const naoNulos = (b.y || []).filter((v) => v != null).length;
  ok((b.x || []).length === N && naoNulos > 300,
     'barra ' + i + ' ("' + b.name + '") tem x e y de verdade', naoNulos + ' pontos');
});
ok((linha.y || []).filter((v) => v != null).length > 300, 'a linha tem pontos');

console.log('\n4. As barras somam a linha (a afirmacao que a secao faz na caption)');
let pior = 0, comparados = 0;
for (let i = 0; i < N; i++) {
  const a = barras[0].y[i], b = barras[1].y[i], t = linha.y[i];
  if (a == null || b == null || t == null) continue;
  comparados++;
  pior = Math.max(pior, Math.abs(a + b - t));
}
ok(comparados > 300, 'ha meses suficientes com as tres series', comparados);
// 0,001 p.p. = o arredondamento de 4 casas do payload, nao uma tolerancia escolhida.
ok(pior < 0.001, 'receita + despesa == total em todo mes', 'residuo max ' + pior.toFixed(6) + ' p.p.');
ok(G.residuo_max_pp != null && G.residuo_max_pp < 0.001,
   'o payload carrega o residuo medido, e ele bate', String(G.residuo_max_pp));

console.log('\n5. Sinal por ramo -- o que impede a tabela de mentir');
// A convencao e "positivo = expansionista", entao os sinais NAO sao uniformes: receita
// entra com -1, despesa com +1, e transferencias (dentro de receita, subtraindo) volta a
// +1. Se alguem "simplificar" isso para um sinal so, esta secao pega.
function ultimo(k, v) {
  const s = R.impulsoRTNSerie(k, v || 'acum12m');
  for (let i = s.values.length - 1; i >= 0; i--) if (s.values[i] != null) return s.values[i];
  return null;
}
ok(ultimo('despesa_total') != null && ultimo('receita_liquida') != null,
   'os dois ramos tem valor no fim da amostra');
// Checagem estrutural, nao de conjuntura: a soma dos filhos reproduz o pai em cada ramo,
// o que so acontece se cada filho carregar o sinal do seu ramo.
function somaFilhos(pai) {
  const no = (function achar(nodes) {
    for (const n of nodes) {
      if (n.seriesKey === pai) return n;
      if (n.children) { const r = achar(n.children); if (r) return r; }
    }
    return null;
  })(G.tree || []);
  if (!no || !no.children) return null;
  const idx = G.dates.indexOf('2026-06-01');
  let soma = 0;
  for (const c of no.children) {
    const v = R.impulsoRTNSerie(c.seriesKey, 'acum12m').values[idx];
    if (v == null) return null;
    soma += v;
  }
  return { soma, pai: R.impulsoRTNSerie(pai, 'acum12m').values[idx] };
}
[['receita_liquida', 'receita (Total − Transferências, sinais opostos)'],
 ['despesa_total', 'despesa (4 rubricas, mesmo sinal)']].forEach(([k, rot]) => {
  const r = somaFilhos(k);
  ok(r && Math.abs(r.soma - r.pai) < 0.002,
     'filhos somam o pai em ' + rot, r ? (r.soma.toFixed(4) + ' vs ' + r.pai.toFixed(4)) : 'sem dado');
});
// Controle NEGATIVO: se transferencias herdasse o sinal do ramo (-1) em vez da excecao
// (+1), a reconciliacao acima ainda passaria em algum mes por acaso? Nao -- e este teste
// afirma isso, para que "filhos somam o pai" nao seja um assert que passa com qualquer
// sinal. Sem ele, trocar +1 por -1 em _SIGN_EXCECOES quebraria o relatorio em silencio.
(function () {
  const idx = G.dates.indexOf('2026-06-01');
  const rt = R.impulsoRTNSerie('receita_total', 'acum12m').values[idx];
  const tr = R.impulsoRTNSerie('transferencias_reparticao_receita', 'acum12m').values[idx];
  const rl = R.impulsoRTNSerie('receita_liquida', 'acum12m').values[idx];
  ok(idx > 0 && rt != null && tr != null && rl != null, 'junho/2026 tem os 3 valores do ramo receita');
  ok(Math.abs(rt + tr - rl) < 0.002, 'com o sinal certo, Total + Transferencias = Liquida',
     rt + ' + ' + tr + ' vs ' + rl);
  ok(Math.abs(rt - tr - rl) > 0.01, 'com o sinal uniforme (errado), a conta NAO fecha',
     'diferenca ' + Math.abs(rt - tr - rl).toFixed(4) + ' p.p.');
})();

console.log('\n6. O seletor Nivel troca de variante de verdade');
const sel = doc.getElementById('impulso-rtn-accum-select');
const antes = JSON.stringify(barras.map((b) => b.y.slice(-6)));
sel.value = 'quarter';
sel.fire('change');
const depois = chamadas.filter((c) => c.tipo === 'react' && c.divId === 'chart-impulso-rtn').pop();
const barras2 = (depois.traces || []).filter((t) => t.type === 'bar');
ok(barras2.length === 2, 'Trimestre continua desenhando as 2 barras');
ok(JSON.stringify(barras2.map((b) => b.y.slice(-6))) !== antes,
   'Trimestre produz valores diferentes de Acum. 12m');
ok((barras2[0].y || []).filter((v) => v != null).length > 300,
   'a variante Trimestre tambem tem pontos', (barras2[0].y || []).filter((v) => v != null).length);
sel.value = 'acum12m'; sel.fire('change');

console.log('\n7. A tabela lista a arvore e o checkbox muda o grafico');
const linhasTab = linhasDaTabela(doc.getElementById('impulso-rtn-table-body'));
ok(linhasTab.length === 2, 'com tudo fechado, a tabela mostra os 2 ramos de topo', linhasTab.length);
ok(linhasTab.every((l) => l.cb), 'toda linha tem checkbox');
ok(linhasTab.filter((l) => l.cb.checked).length === 2, 'os 2 ramos vem marcados por default');
const nBarrasAntes = chamadas.filter((c) => c.tipo === 'react' && c.divId === 'chart-impulso-rtn').pop()
  .traces.filter((t) => t.type === 'bar').length;
linhasTab[0].cb.checked = false;
linhasTab[0].cb.fire('change');
const nBarrasDepois = chamadas.filter((c) => c.tipo === 'react' && c.divId === 'chart-impulso-rtn').pop()
  .traces.filter((t) => t.type === 'bar').length;
ok(nBarrasDepois === nBarrasAntes - 1, 'desmarcar uma linha remove a barra dela',
   nBarrasAntes + ' -> ' + nBarrasDepois);

console.log('\n8. Coexistencia -- a secao do BCB continua inteira');
R.IMPULSO_RP_TAB.init();
const rp = chamadas.filter((c) => c.tipo === 'react' && c.divId === 'chart-impulso-rp-esfera').pop();
ok(!!rp, 'chart-impulso-rp-esfera ainda e desenhado');
ok((rp.traces || []).filter((t) => t.type === 'bar').length === 5,
   'as 5 esferas do NFSP continuam la', (rp.traces || []).filter((t) => t.type === 'bar').length);
// As duas metricas medem escopos diferentes -- se algum dia sairem IDENTICAS, alguem ligou
// as duas secoes na mesma fonte por engano.
const tRTN = R.impulsoRTNTotal('acum12m'), tRP = R.impulsoRPTotal('acum12m');
const mapaRP = {};
tRP.dates.forEach((d, i) => { mapaRP[d] = tRP.values[i]; });
let diferentes = 0, comuns = 0;
tRTN.dates.forEach((d, i) => {
  if (mapaRP[d] == null || tRTN.values[i] == null) return;
  comuns++;
  if (Math.abs(mapaRP[d] - tRTN.values[i]) > 0.01) diferentes++;
});
ok(comuns > 200, 'as duas series se sobrepoem no tempo', comuns + ' meses');
ok(diferentes > comuns * 0.5,
   'RTN (Gov. Central) e NFSP (consolidado) sao series distintas, nao a mesma duplicada',
   diferentes + '/' + comuns + ' meses diferem');

console.log('\n9. Visao Combinada -- a 4a metrica entrou sem desalojar as outras');
R.renderImpulsoCombinado();
const comb = chamadas.filter((c) => c.tipo === 'react' && c.divId === 'chart-impulso-combinado').pop();
ok(!!comb, 'chart-impulso-combinado foi desenhado');
const linhas = (comb.traces || []);
ok(linhas.length === 4, 'quatro linhas no grafico combinado', linhas.length);
const nomes = linhas.map((t) => t.name);
ok(nomes.filter((n) => /Res\. Prim/.test(n)).length === 2,
   'as duas apuracoes do resultado primario estao nomeadas distintamente', JSON.stringify(nomes));
// O rotulo generico "Impulso via Resultado Primario" deixou de servir com duas linhas: um
// leitor nao teria como saber qual apuracao esta olhando.
ok(!nomes.includes('Impulso via Resultado Primário'),
   'o rotulo ambiguo antigo nao sobreviveu', JSON.stringify(nomes));
const rtnLinha = linhas.find((t) => /RTN/.test(t.name));
const pbLinha = linhas.find((t) => /BCB/.test(t.name));
ok(!!rtnLinha && !!pbLinha, 'as duas linhas do par existem');
ok((rtnLinha.y || []).filter((v) => v != null).length > 300,
   'a linha do RTN tem pontos de verdade (nao um trace vazio)',
   (rtnLinha.y || []).filter((v) => v != null).length);
// Codificacao visual: as duas sao um par (mesma familia de cor, a de cima tracejada). Se
// alguem trocar por uma cor de matiz diferente, elas passam a ler como metricas
// independentes -- que e o oposto do que sao.
ok(rtnLinha.line.dash === 'dash', 'a linha do RTN e tracejada', String(rtnLinha.line.dash));
ok(pbLinha.line.dash === undefined, 'a do BCB continua solida');
ok(rtnLinha.line.color !== pbLinha.line.color, 'cores distintas entre as duas');
ok(linhas.indexOf(rtnLinha) === linhas.indexOf(pbLinha) + 1,
   'a do RTN vem logo depois da do BCB na legenda');
// A serie do RTN alcanca um mes que a do BCB ainda nao tem -- e o unico ganho de prazo
// que a metrica oferece, e o grafico so o entrega se as duas nao forem truncadas ao grid
// comum. Um bug de alinhamento apagaria isso sem erro nenhum.
function ultimaData(t) {
  for (let i = t.y.length - 1; i >= 0; i--) if (t.y[i] != null) return t.x[i];
  return null;
}
const fimRTN = ultimaData(rtnLinha), fimPB = ultimaData(pbLinha);
ok(fimRTN != null && fimPB != null, 'as duas terminam em alguma data');
ok(String(fimRTN) >= String(fimPB), 'a do RTN nao termina antes da do BCB', fimRTN + ' vs ' + fimPB);

// O toggle Comparacao tem de mover a linha nova junto com as outras. A do credito NAO --
// ela nao tem variante trimestral, e isso ja era regra antes desta secao existir.
const selComb = doc.getElementById('impulso-combinado-view-select');
const antesRTN = JSON.stringify(rtnLinha.y.slice(-8));
const antesCred = JSON.stringify(linhas.find((t) => /Crédito/.test(t.name)).y.slice(-8));
selComb.value = 'quarter';
R.renderImpulsoCombinado();
const comb2 = chamadas.filter((c) => c.tipo === 'react' && c.divId === 'chart-impulso-combinado').pop();
const rtn2 = comb2.traces.find((t) => /RTN/.test(t.name));
const cred2 = comb2.traces.find((t) => /Crédito/.test(t.name));
ok(comb2.traces.length === 4, 'Trimestre continua com as 4 linhas', comb2.traces.length);
ok(JSON.stringify(rtn2.y.slice(-8)) !== antesRTN, 'Trimestre muda a linha do RTN');
ok(JSON.stringify(cred2.y.slice(-8)) === antesCred,
   'e continua sem mexer na do credito (que nao tem variante trimestral)');
selComb.value = 'acum';
R.renderImpulsoCombinado();

// As duas apuracoes tem de CONCORDAR no acumulado -- e o argumento da secao. Se algum dia
// discordarem muito, ou uma delas foi ligada na fonte errada, ou ha noticia de verdade.
(function () {
  const c = chamadas.filter((x) => x.tipo === 'react' && x.divId === 'chart-impulso-combinado').pop();
  const a = c.traces.find((t) => /RTN/.test(t.name));
  const b = c.traces.find((t) => /BCB/.test(t.name));
  const mapa = {};
  b.x.forEach((d, i) => { mapa[d] = b.y[i]; });
  let n = 0, soma = 0, pior = 0;
  a.x.forEach((d, i) => {
    if (mapa[d] == null || a.y[i] == null) return;
    n++; const g = Math.abs(mapa[d] - a.y[i]); soma += g; pior = Math.max(pior, g);
  });
  ok(n > 200, 'as duas se sobrepoem em muitos meses', n);
  // 0,6 p.p. de gap medio seria escopo virando outra historia; medido hoje: ~0,26.
  ok(soma / n < 0.6, 'gap medio entre as apuracoes fica na faixa de escopo',
     (soma / n).toFixed(3) + ' p.p. (max ' + pior.toFixed(2) + ')');
})();

// Le o HTML do cartao aberto. O cartao e criado sob demanda dentro do script do
// relatorio, entao o harness o encontra pelo <body> em vez de por id.
function _popHtml() {
  const pop = doc.body.children.find((c) => c.className && String(c.className).indexOf('info-pop') >= 0);
  return pop ? pop.innerHTML : null;
}

console.log('\n10. Cartoes de definicao (padrao lis-dashboard)');
// Todas as tabelas precisam ter sido montadas para os botoes existirem.
R.RENDERERS.gfsm(); R.RENDERERS.investimento(); R.RENDERERS.dlsp(); R.IEG_HIER_TAB.init();

// (a) O mapa nao pode ter chave orfa. Um erro de digitacao numa chave produz um cartao
// que nunca abre -- sem erro, sem lacuna visivel, so um botao que deixou de nascer. Esta
// e a asserção que justifica o harness existir para esta feature.
const NS_DE = {                     // namespace -> as arvores em que ele e usado
  gfsm:    [R.D.gfsm && R.D.gfsm.tree],
  rtn:     [R.D.rtn && R.D.rtn.tree],
  imprtn:  [R.D.impulso_rtn && R.D.impulso_rtn.tree],
  inv:     Object.keys((R.D.investimento || {}).cortes || {}).map((c) => R.D.investimento.cortes[c].tree),
  ieg:     [R.D.ieg && R.D.ieg.tree],
  imprp:   [R.D.fiscal_impulse_nfsp && R.D.fiscal_impulse_nfsp.tree],
  imprp2:  [],
  credof:  [R.D.credito_oficial && R.D.credito_oficial.tree],
  dlsp:    [R.D.dlsp && R.D.dlsp.tree, R.D.dlsp && R.D.dlsp.balanco_tree],
};
function chavesDe(trees) {
  const out = new Set();
  (trees || []).forEach(function walkT(t) {
    (t || []).forEach((n) => { out.add(n.key); if (n.children) walkT(n.children); });
  });
  // A busca cai para o sufixo depois do ultimo "__" -- entao uma entrada por sufixo e
  // legitima e tem de contar como alcancavel.
  Array.from(out).forEach((k) => { if (String(k).indexOf('__') >= 0) out.add(String(k).split('__').pop()); });
  return out;
}
const alcancaveis = {};
Object.keys(NS_DE).forEach((ns) => { alcancaveis[ns] = chavesDe(NS_DE[ns]); });
const orfas = Object.keys(R.NODE_INFO).filter((full) => {
  const i = full.indexOf(':');
  const ns = full.slice(0, i), k = full.slice(i + 1);
  return !alcancaveis[ns] || !alcancaveis[ns].has(k);
});
ok(Object.keys(R.NODE_INFO).length > 60, 'o mapa tem conteudo', Object.keys(R.NODE_INFO).length + ' entradas');
ok(orfas.length === 0, 'nenhuma chave do NODE_INFO aponta para linha inexistente', orfas.join(', '));

// (b) Isolamento por namespace -- o motivo de o mapa nao ser de chave nua.
ok(R.infoOf('gfsm', 'receita_total') !== R.infoOf('rtn', 'receita_total'),
   'gfsm:receita_total e rtn:receita_total sao cartoes distintos');
ok(/GFSM/.test(R.infoOf('gfsm', 'receita_total').full), 'o da GFSM cita o codigo GFSM');
ok(/RTN/.test(R.infoOf('rtn', 'receita_total').full), 'o do RTN cita o codigo RTN');
// A lista ['imprtn','rtn'] resolve o especifico primeiro e cai no compartilhado depois.
ok(/impulso/i.test(R.infoOf(['imprtn', 'rtn'], 'receita_liquida').full),
   'na tabela de impulso, receita_liquida usa a definicao de CONTRIBUICAO');
ok(R.infoOf(['imprtn', 'rtn'], 'cofins') === R.infoOf('rtn', 'cofins'),
   'e as rubricas sem entrada propria caem na definicao compartilhada do RTN');
// Sufixo: uma definicao de categoria serve as 4 esferas do IEG.
ok(R.infoOf('ieg', 'geral__folha') === R.infoOf('ieg', 'central__folha'),
   'a busca por sufixo faz uma definicao servir as 4 esferas do IEG');
ok(R.infoOf('rtn', 'nao_existe_mesmo') === null, 'chave sem entrada devolve null');

// (c) `full` nunca repete o rotulo -- regra 3 do padrao (o cartao nao abre para dizer o
// que o leitor acabou de ler). Checa contra os rotulos reais das arvores.
const rotulos = {};
Object.keys(NS_DE).forEach((ns) => {
  rotulos[ns] = {};
  (NS_DE[ns] || []).forEach(function walkT(t) {
    (t || []).forEach((n) => { rotulos[ns][n.key] = n.label; if (n.children) walkT(n.children); });
  });
});
const repetidos = Object.keys(R.NODE_INFO).filter((full) => {
  const i = full.indexOf(':');
  const ns = full.slice(0, i), k = full.slice(i + 1);
  const info = R.NODE_INFO[full];
  return info.full && rotulos[ns] && rotulos[ns][k] === info.full;
});
ok(repetidos.length === 0, 'nenhum `full` apenas repete o rotulo da linha', repetidos.join(', '));
// E toda entrada tem de dizer alguma coisa -- uma entrada vazia so produz um botao morto.
const vazias = Object.keys(R.NODE_INFO).filter((k) => !R.NODE_INFO[k].full && !R.NODE_INFO[k].desc);
ok(vazias.length === 0, 'nenhuma entrada vazia', vazias.join(', '));

// (d) O botao nasce da presenca no mapa, nao de markup linha a linha.
R.IMPULSO_RTN_TAB.init();
const linhasRTN = linhasDaTabela(doc.getElementById('impulso-rtn-table-body'));
ok(linhasRTN.length === 2 && linhasRTN.every((l) => l.info),
   'os 2 ramos do impulso RTN tem botao de info');
ok(linhasRTN[0].label === 'Receita Líquida (Total − Transferências)',
   'o rotulo lido da celula NAO traz o "i" do botao junto', JSON.stringify(linhasRTN[0].label));
// Uma linha sem entrada no mapa nao pode ganhar botao.
const linhasIEG = linhasDaTabela(doc.getElementById('ieg-hier-table-body'));
ok(linhasIEG.length > 0 && linhasIEG.every((l) => l.info),
   'as 4 esferas do IEG tem cartao');
(function () {
  const b = doc.getElementById('impulso-rtn-accum-select');
  // Expande a receita para chegar nas folhas: os 9 tributos, dos quais alguns NAO tem
  // cartao (Imposto de Importacao tem `full`; "Outras Administradas" tambem; mas as
  // 9 funcoes discricionarias em sua maioria nao tem).
  R.IMPULSO_RTN_TAB.init();
})();

// (e) A unidade do cartao vem do eixo, nao de uma string fixa -- o erro que o
// exchange_rate documentou. Se alguem congelar a unidade, o cartao passa a mentir no
// primeiro clique no seletor.
(function () {
  const sel = doc.getElementById('impulso-rtn-accum-select');
  const btn = linhasRTN[0].info;
  sel.value = 'acum12m'; sel.fire('change');
  const l1 = linhasDaTabela(doc.getElementById('impulso-rtn-table-body'))[0];
  l1.info.fire('mouseenter');
  const u1 = (_popHtml() || '').match(/Unidade: ([^<]*)/);
  sel.value = 'quarter'; sel.fire('change');
  const l2 = linhasDaTabela(doc.getElementById('impulso-rtn-table-body'))[0];
  l2.info.fire('mouseenter');
  const u2 = (_popHtml() || '').match(/Unidade: ([^<]*)/);
  ok(!!u1 && !!u2, 'o cartao imprime a linha de unidade', JSON.stringify([u1 && u1[1], u2 && u2[1]]));
  ok(u1 && u2 && u1[1] !== u2[1],
     'e ela ACOMPANHA o seletor de Nivel', (u1 && u1[1]) + ' -> ' + (u2 && u2[1]));
  sel.value = 'acum12m'; sel.fire('change');
})();

// (f) Um cartao so no documento, reposicionado -- nao um por linha.
const pops = doc.body.children.filter((c) => c.classList && c.classList.contains('info-pop'));
ok(pops.length === 1, 'existe exatamente um .info-pop no <body>', pops.length);
// E o conteudo nao repete o titulo dentro do corpo.
(function () {
  const html = _popHtml() || '';
  const h4 = /<h4>([^<]*)<\/h4>/.exec(html);
  const full = /class="info-full">([^<]*)</.exec(html);
  ok(!!h4, 'o cartao tem titulo');
  ok(!full || full[1] !== h4[1], 'o corpo nao repete o titulo');
})();

console.log('\n11. Regua de periodo -- a janela, nao a definicao do botao');
// O defeito que motivou esta secao (2026-08-28, print do usuario): faixa vazia nas
// duas pontas do grafico. Causa: xaxis.rangeselector nativo + autorange. As
// asserções abaixo afirmam sobre o [from, to] que sai, porque foi exatamente
// asserção-sobre-a-definicao-do-botao que deixou a versao anterior passar.
ok(!/rangeselector\s*:/.test(CRU),
   'nenhum xaxis.rangeselector nativo sobrou no HTML gerado');

const MS_DIA = 86400000;
function reguaDe(divId) {
  const card = doc.getElementById(divId)._closest;
  const wrap = card && card.parentNode;
  return wrap ? wrap.querySelector('.range-bar') : null;
}
function reguasDe(divId) {
  const card = doc.getElementById(divId)._closest;
  const wrap = card && card.parentNode;
  return wrap ? wrap.querySelectorAll('.range-bar') : [];
}
// Ultimo xaxis.range aplicado ao div -- e o que o usuario ve.
function janelaDe(divId) {
  for (let i = chamadas.length - 1; i >= 0; i--) {
    const c = chamadas[i];
    if (c.tipo === 'relayout' && c.divId === divId && c.upd && c.upd['xaxis.range']) return c.upd['xaxis.range'];
  }
  return null;
}
// Extremos com dado nos traces realmente plotados (o que o eixo deveria respeitar).
function extentDe(divId) {
  const el = doc.getElementById(divId);
  let lo = null, hi = null;
  (el.data || []).forEach((t) => {
    if (!t.x || !t.y) return;
    for (let i = 0; i < t.x.length; i++) {
      const v = t.y[i];
      if (v === null || v === undefined || (typeof v === 'number' && isNaN(v))) continue;
      if (lo === null || t.x[i] < lo) lo = t.x[i];
      if (hi === null || t.x[i] > hi) hi = t.x[i];
    }
  });
  return [lo, hi];
}


// Todos os graficos das 4 abas de dados, desenhados de verdade.
R.RENDERERS.gfsm(); R.RENDERERS.investimento(); R.RENDERERS.dlsp(); R.RENDERERS.impulso();
const DIVS = ['chart-gfsm', 'chart-rtn', 'chart-inv-funcao', 'chart-inv-natureza',
              'chart-dlsp-balanco', 'chart-impulso-combinado', 'chart-ieg-hier',
              'chart-impulso-rp-esfera', 'chart-impulso-rtn', 'chart-credito-oficial'];

const semRegua = DIVS.filter((d) => !reguaDe(d));
ok(semRegua.length === 0, 'todos os ' + DIVS.length + ' graficos ganharam regua', semRegua.join(', '));
const duplicadas = DIVS.filter((d) => reguasDe(d).length !== 1);
ok(duplicadas.length === 0, 'e exatamente UMA por grafico, mesmo apos redesenhos', duplicadas.join(', '));
const rotulosErrados = DIVS.filter((d) => {
  const b = reguaDe(d);
  return !b || b.children.map((c) => c.textContent).join('|') !== '1a|3a|5a|10a|Tudo';
});
ok(rotulosErrados.length === 0, 'com os 5 botoes na ordem 1a/3a/5a/10a/Tudo', rotulosErrados.join(', '));

// (a) A VISTA INICIAL e um range calculado, nao autorange -- e cabe no dado.
// Folga aceita: um passo da serie de cada lado (meio passo de padding e o passo
// inteiro por seguranca de arredondamento). Um autorange percentual num historico
// de 15+ anos estoura isso por ordens de grandeza -- era ~9 meses no print.
const foraDoDado = [];
DIVS.forEach((d) => {
  const w = janelaDe(d), ex = extentDe(d);
  if (!w || !ex[0]) { foraDoDado.push(d + ' (sem janela)'); return; }
  const el = doc.getElementById(d);
  // passo da serie: menor distancia entre dois x consecutivos com dado
  const xs = [];
  (el.data || []).forEach((t) => { if (t.x) t.x.forEach((v) => { if (xs.indexOf(v) < 0) xs.push(v); }); });
  xs.sort();
  const passo = xs.length > 1 ? Date.parse(xs[xs.length - 1]) - Date.parse(xs[xs.length - 2]) : 31 * MS_DIA;
  const folgaEsq = Date.parse(ex[0]) - Date.parse(w[0]);
  const folgaDir = Date.parse(w[1]) - Date.parse(ex[1]);
  if (folgaEsq < 0 || folgaDir < 0 || folgaEsq > passo || folgaDir > passo) {
    foraDoDado.push(d + ' esq=' + Math.round(folgaEsq / MS_DIA) + 'd dir=' + Math.round(folgaDir / MS_DIA) + 'd (passo=' + Math.round(passo / MS_DIA) + 'd)');
  }
});
ok(foraDoDado.length === 0,
   'a vista inicial abre colada no dado (folga <= 1 passo nas duas pontas)', foraDoDado.join(' | '));
(function () {
  const b = reguaDe(DIVS[0]);
  const ativos = b ? b.children.filter((c) => c.classList.contains('active')).map((c) => c.textContent) : [];
  ok(ativos.join(',') === 'Tudo', 'e o pill "Tudo" nasce marcado', ativos.join(','));
})();

// (b) A janela do grafico combinado NAO e a grade do payload: o IEG termina antes do
// RTN, e um x com y nulo continua empurrando o autorange. E o caso que produziu 26
// anos de faixa vazia no relatorio de cambio.
(function () {
  const el = doc.getElementById('chart-impulso-combinado');
  const grade = [];
  (el.data || []).forEach((t) => (t.x || []).forEach((v) => { if (grade.indexOf(v) < 0) grade.push(v); }));
  grade.sort();
  const ex = extentDe('chart-impulso-combinado');
  const w = janelaDe('chart-impulso-combinado');
  ok(grade[0] < ex[0] || grade[grade.length - 1] > ex[1],
     'no combinado a grade do payload e MAIOR que o trecho com dado',
     grade[0] + '..' + grade[grade.length - 1] + ' vs ' + ex[0] + '..' + ex[1]);
  ok(Date.parse(w[1]) < Date.parse(grade[grade.length - 1]) + 31 * MS_DIA,
     'e a janela segue o trecho com dado, nao a grade');
})();

// (c) "10a" ancora no ULTIMO DADO, nao no range do eixo. Este e o bug original:
// stepmode:'backward' lia ax.range[1] ja inflado pelo padding, e a janela saia
// deslocada para a frente com a direita vazia.
(function () {
  const div = 'chart-impulso-rtn';
  const b = reguaDe(div);
  const tudo = janelaDe(div);
  b.children.find((c) => c.textContent === '10a').fire('click');
  const dez = janelaDe(div);
  ok(dez[1] === tudo[1], '"10a" termina no mesmo ponto que "Tudo"', dez[1] + ' vs ' + tudo[1]);
  const anos = (Date.parse(dez[1]) - Date.parse(dez[0])) / (365.2425 * MS_DIA);
  ok(anos > 9.9 && anos < 10.2, 'e a janela tem 10 anos de largura', anos.toFixed(3) + ' anos');
  const ativos = b.children.filter((c) => c.classList.contains('active')).map((c) => c.textContent);
  ok(ativos.join(',') === '10a', 'e so o pill clicado fica marcado', ativos.join(','));
  // A faixa escolhida sobrevive a um redesenho -- senao marcar uma linha na tabela
  // jogaria o usuario de volta para o historico inteiro.
  R.IMPULSO_RTN_TAB.init();
  const depois = janelaDe(div);
  ok(depois[0] === dez[0] && depois[1] === dez[1],
     'e sobrevive ao redesenho da tabela', JSON.stringify(depois));
  reguaDe(div).children.find((c) => c.textContent === 'Tudo').fire('click');
})();


// (d) A invariante que vale para TODOS os botoes de TODOS os graficos: nenhum
// inventa historia antes do primeiro dado, e TODOS terminam no mesmo ponto -- o
// ultimo dado. Era exatamente o "to" que o componente nativo errava, e a faixa
// vazia que o usuario viu estava do lado direito.
(function () {
  const ruins = [];
  DIVS.forEach((d) => {
    const b = reguaDe(d);
    if (!b || !b.children.length) { ruins.push(d + ' (sem regua)'); return; }
    const tudoBtn = b.children.find((c) => c.textContent === 'Tudo');
    tudoBtn.fire('click');
    const tudo = janelaDe(d);
    b.children.forEach((btn) => {
      btn.fire('click');
      const w = janelaDe(d);
      if (w[1] !== tudo[1]) ruins.push(d + '/' + btn.textContent + ' termina em ' + w[1] + ' != ' + tudo[1]);
      if (Date.parse(w[0]) < Date.parse(tudo[0])) ruins.push(d + '/' + btn.textContent + ' comeca antes do dado');
      if (Date.parse(w[0]) >= Date.parse(w[1])) ruins.push(d + '/' + btn.textContent + ' janela vazia');
    });
    tudoBtn.fire('click');
  });
  ok(ruins.length === 0,
     'todo botao termina no ultimo dado e nenhum comeca antes do primeiro',
     ruins.slice(0, 4).join(' | '));
})();

// (e) E a regra de clamp: numa serie mais curta que a faixa pedida, o botao cai para
// o inicio do dado em vez de abrir anos vazios a esquerda.
(function () {
  const div = 'chart-impulso-rtn';
  const b = reguaDe(div);
  b.children.find((c) => c.textContent === 'Tudo').fire('click');
  const tudo = janelaDe(div);
  b.children.find((c) => c.textContent === '1a').fire('click');
  const um = janelaDe(div);
  ok(Date.parse(um[0]) > Date.parse(tudo[0]),
     '"1a" corta de verdade numa serie de ~30 anos', um[0]);
  b.children.find((c) => c.textContent === 'Tudo').fire('click');
})();

console.log('\n' + '='.repeat(62));
if (falhas) { console.log(falhas + ' FALHA(S)'); process.exit(1); }
console.log('todos os asserts passaram');
