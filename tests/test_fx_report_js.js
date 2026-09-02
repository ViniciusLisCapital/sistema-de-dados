/*
 * Executa o JavaScript REAL das abas de dados de reports/brasil/FX Report.html
 * contra um document/Plotly stubados, e confere COMPORTAMENTO -- nao a forma dos
 * objetos de configuracao.
 *
 * Nasceu da rodada de 2026-08-27, que fez quatro coisas na aba Balanco de
 * Pagamentos: trocou os seletores de aba por seletores por grafico, deu escolha
 * de barras empilhadas ou linhas, fundiu os 6 graficos de composicao numa arvore
 * unica com tabela hierarquica, e corrigiu a regua de periodo.
 *
 * O teste da regua e o mais importante e o motivo direto deste arquivo existir:
 * o botao "10a" abria uma janela terminando ~2 anos DEPOIS do ultimo dado porque
 * o xaxis.rangeselector nativo do Plotly ancora o fim da janela no range atual do
 * eixo -- que, com autorange, ja vem com o padding automatico do Plotly embutido.
 * Nenhum teste pegava isso porque todos afirmavam sobre a DEFINICAO do botao e
 * nunca sobre a janela que ele produz (mesma licao registrada em
 * .claude/rules/lis-dashboards.md). Aqui as assercoes sao sobre o [from, to].
 *
 * Sem browser neste ambiente: renderizacao visual continua nao verificada.
 *
 * Uso:  node tests/test_fx_report_js.js
 */

const fs = require('fs');
const path = require('path');

const HTML = path.join(__dirname, '..', 'reports', 'brasil', 'FX Report.html');

let falhas = 0, oks = 0;
function ok(cond, msg, extra) {
  if (cond) { oks++; console.log('  ok      ' + msg); }
  else { falhas++; console.log('  FALHOU  ' + msg + (extra !== undefined ? '  -> ' + extra : '')); }
}
function near(a, b, tol, msg) {
  const d = Math.abs(a - b);
  ok(d <= tol, msg, `esperado ~${b}, veio ${a} (diff ${d})`);
}
// A regua emite "YYYY-MM-DD HH:mm:ss" sem fuso, que e a forma canonica de data do
// Plotly e que ele le como ingenua/UTC. Date.parse, ao contrario, le "data + hora
// sem offset" como HORA LOCAL (so a forma "YYYY-MM-DD" pura e UTC) -- ler os dois
// lados com a mesma regua evitaria um falso negativo de 3h (o fuso desta maquina).
function parseNaive(s) {
  return Date.parse(String(s).replace(' ', 'T') + (/[Z+]/.test(s) ? '' : 'Z'));
}

// ── DOM stub ──────────────────────────────────────────────────────────────────
const registry = {};
const byClass = {};

function makeEl(tag) {
  // className e classList tem de ser DUAS VISTAS DO MESMO conjunto. Eram campos
  // separados numa versao anterior deste stub, e o resultado foi um falso negativo
  // caro: o relatorio cria a regua com `div.className = 'chart-with-range'`, o
  // teste perguntava por classList.contains(...) e recebia false, entao a regua
  // parecia nunca ter sido inserida quando na verdade estava toda certa.
  const _classes = new Set();
  const e = {
    tagName: (tag || '').toUpperCase(),
    children: [], parentNode: null, textContent: '', style: {}, dataset: {},
    type: '', checked: false, value: '',
    // Estado interno que o Plotly pendura no div do grafico: _bindYAutofit le
    // gd._fullLayout.xaxis para saber se o eixo X e categoria ou data. Sem range
    // definido ele sai cedo, que e o estado de "recem-plotado".
    _fullLayout: { xaxis: {} },
    _listeners: {},
    classList: {
      _s: _classes,
      add(c) { _classes.add(c); }, remove(c) { _classes.delete(c); },
      contains(c) { return _classes.has(c); },
      toggle(c, on) { if (on === undefined) { _classes.has(c) ? _classes.delete(c) : _classes.add(c); } else { on ? _classes.add(c) : _classes.delete(c); } },
    },
    appendChild(c) {
      // Reparentar tem de DESLIGAR do pai anterior, como no DOM real: sem isso o
      // card embrulhado pela regua continuaria listado tambem na secao original.
      if (c.parentNode && c.parentNode !== this) {
        const j = c.parentNode.children.indexOf(c);
        if (j >= 0) c.parentNode.children.splice(j, 1);
      }
      this.children.push(c); c.parentNode = this; return c;
    },
    insertBefore(nw, ref) {
      const i = this.children.indexOf(ref);
      this.children.splice(i < 0 ? this.children.length : i, 0, nw);
      nw.parentNode = this;
      return nw;
    },
    addEventListener(ev, fn) { (this._listeners[ev] = this._listeners[ev] || []).push(fn); },
    // O botao de definicao usa setAttribute (aria-label), e showInfo mede o botao
    // e o proprio cartao para se posicionar. Numeros fixos: o que o teste afirma e
    // o CONTEUDO do cartao, nao onde ele cai na tela -- posicao so e verificavel
    // num browser de verdade.
    attributes: {},
    setAttribute(k, v) { this.attributes[k] = String(v); },
    getAttribute(k) { return Object.prototype.hasOwnProperty.call(this.attributes, k) ? this.attributes[k] : null; },
    getBoundingClientRect() { return { left: 10, top: 20, right: 24, bottom: 34, width: 14, height: 14 }; },
    // ':hover' nunca e verdade sem ponteiro; qualquer outro seletor cai no
    // classList, que e o que o resto do stub ja usa.
    matches(sel) { return sel === ':hover' ? false : this.classList.contains(String(sel).replace('.', '')); },
    contains(node) {
      if (node === this) return true;
      return this.children.some(c => c.contains && c.contains(node));
    },
    on(ev, fn) { (this._listeners[ev] = this._listeners[ev] || []).push(fn); },
    fire(ev, arg) { (this._listeners[ev] || []).forEach(f => f.call(this, arg || {})); },
    click() { this.fire('click'); },
    change() { this.fire('change'); },
    // O codigo sobe do div do grafico ate o .chart-card para embrulhar o card e a
    // regua num mesmo item de layout -- sem closest o embrulho nao acontece.
    closest(sel) {
      const want = sel.replace('.', '');
      let n = this;
      while (n) { if (n.classList.contains(want)) return n; n = n.parentNode; }
      return null;
    },
    querySelector(sel) { return (this.querySelectorAll(sel) || [])[0] || null; },
    querySelectorAll(sel) {
      const want = sel.replace('.', '');
      const out = [];
      (function walk(node) {
        node.children.forEach(c => { if (c.classList.contains(want)) out.push(c); walk(c); });
      })(this);
      return out;
    },
  };
  // innerHTML como acessor: o relatorio limpa thead/tbody/regua com `= ''` antes
  // de cada render. Como campo simples, `children` nunca esvaziaria e as
  // assercoes leriam a renderizacao ANTERIOR.
  Object.defineProperty(e, 'className', {
    get() { return [..._classes].join(' '); },
    set(v) { _classes.clear(); String(v).split(/\s+/).filter(Boolean).forEach(c => _classes.add(c)); },
  });
  let _html = '';
  Object.defineProperty(e, 'innerHTML', {
    get() { return _html; },
    set(v) { _html = v; if (v === '') e.children.length = 0; },
  });
  let _id = '';
  Object.defineProperty(e, 'id', {
    get() { return _id; },
    set(v) { _id = v; if (v) registry[v] = e; },
  });
  return e;
}

function el(id) {
  if (!registry[id]) { const e = makeEl('div'); e.id = id; }
  return registry[id];
}

// Os ids sao lidos do PROPRIO html gerado, nao listados aqui: renomear um id no
// template tem de quebrar o teste em vez de virar um stub vazio que passa.
const htmlBruto = fs.readFileSync(HTML, 'utf8');
const idsNoHtml = [...htmlBruto.matchAll(/\bid="([\w-]+)"/g)].map(m => m[1]);
idsNoHtml.forEach(id => el(id));

// Cada div de grafico mora dentro de um .chart-card, que mora dentro de uma
// <section>. A regua e inserida pelo codigo entre os dois, entao a hierarquia
// precisa existir de verdade no stub.
const chartDivIds = [...htmlBruto.matchAll(/<div class="chart-card"[^>]*><div id="([\w-]+)"><\/div><\/div>/g)].map(m => m[1]);
const cardOf = {};
chartDivIds.forEach(divId => {
  const section = makeEl('div');
  const card = makeEl('div'); card.classList.add('chart-card');
  section.appendChild(card);
  card.appendChild(el(divId));
  cardOf[divId] = card;
});
const tabButtons = [...htmlBruto.matchAll(/<button class="tab-btn" data-tab="([\w-]+)">/g)].map(m => {
  const b = makeEl('button'); b.dataset.tab = m[1]; return b;
});
const tabPanels = [...htmlBruto.matchAll(/<div class="tab-panel[^"]*" id="([\w-]+)">/g)].map(m => el(m[1]));
tabPanels.forEach(p => { p.querySelectorAll = () => []; });

const reactCalls = [], relayoutCalls = [], newPlotCalls = [];

global.document = {
  getElementById: (id) => registry[id] || null,
  createElement: (t) => makeEl(t),
  createTextNode: (txt) => ({ nodeType: 3, textContent: txt, children: [], classList: { contains: () => false } }),
  addEventListener: () => {},
  querySelectorAll: (sel) => {
    if (sel === '.tab-panel') return tabPanels;
    if (sel === '.tab-btn') return tabButtons;
    return [];
  },
};
// O .then() de react/newPlot e onde o relatorio instala a regua de periodo. Uma
// Promise real so resolveria depois que este arquivo terminasse de rodar, entao o
// stub devolve um thenable SINCRONO -- do contrario o teste leria um DOM em que a
// regua ainda nao existe e o falso negativo pareceria bug do produto.
function thenableSync(val) {
  return { then(fn) { return thenableSync(fn ? fn(val) : val); }, catch() { return this; } };
}
// O Plotly pendura traces/layout no proprio div (gd.data / gd.layout), e o
// relatorio le isso -- _bindYAutofit varre gd.data para refazer o Y e _ensureRangeBar
// le el.data para achar o extent. Guardar no stub e o que torna esses caminhos
// exercitaveis em vez de apenas nao-lancarem.
function plotStub(div, traces, layout) {
  const e = el(div);
  e.data = traces;
  e.layout = layout;
  e._fullLayout = Object.assign({}, layout, { xaxis: Object.assign({}, (layout || {}).xaxis) });
  return e;
}
global.Plotly = {
  react: (div, traces, layout, config) => { reactCalls.push({ div, traces, layout, config }); return thenableSync(plotStub(div, traces, layout)); },
  newPlot: (div, traces, layout, config) => { newPlotCalls.push({ div, traces, layout, config }); return thenableSync(plotStub(div, traces, layout)); },
  relayout: (div, upd) => { relayoutCalls.push({ div, upd }); return thenableSync(); },
  restyle: () => thenableSync(),
  Plots: { resize: () => {} },
};
global.window = global;
// O cartao de definicao vive no <body> (um so, reposicionado) e se posiciona
// lendo scroll e viewport -- sem estes o showInfo lanca antes de montar o HTML.
global.document.body = makeEl('body');
global.document.documentElement = Object.assign(makeEl('html'), { clientWidth: 1440, clientHeight: 900 });
global.scrollX = 0;
global.scrollY = 0;

// ── roda o script real das abas de dados ──────────────────────────────────────
const scripts = [...htmlBruto.matchAll(/<script(?![^>]*\bsrc=)[^>]*>([\s\S]*?)<\/script>/g)].map(m => m[1]);
ok(scripts.length >= 1, 'ha script inline no relatorio', scripts.length);
const code = scripts[0];   // primeiro bloco = abas de dados (o segundo e o das abas de modelo)
console.log(`script das abas de dados: ${code.length.toLocaleString()} chars`);

// `function` e `var` do eval vazam para o escopo do modulo (e por isso
// _rangeOptions / BOP_TREE_* ficam visiveis aqui direto), mas REPORT_DATA o
// builder injeta como `const`, que fica preso ao escopo do proprio eval -- dai
// a exportacao explicita no fim do codigo avaliado.
let erro = null;
try {
  eval(code + ';\nglobal.__RD = REPORT_DATA;');
} catch (e) { erro = e; }
ok(erro === null, 'o script das abas de dados roda sem excecao', erro && (erro.message + '\n' + erro.stack));
if (erro) { console.log(`\n${oks} ok, ${falhas} falhou`); process.exit(1); }

// Janela X aplicada na PRIMEIRA pintura de cada grafico, e os traces daquela
// pintura -- capturados aqui, antes de qualquer clique do proprio teste, porque as
// secoes seguintes trocam seletores e marcam caixas.
const janelaInicial = {};
relayoutCalls.forEach(r => {
  if (r.upd && r.upd['xaxis.range'] && !(r.div in janelaInicial)) janelaInicial[r.div] = r.upd['xaxis.range'];
});
const tracesIniciais = {};
newPlotCalls.concat(reactCalls).forEach(c => { if (!(c.div in tracesIniciais)) tracesIniciais[c.div] = c.traces || []; });

const REPORT_DATA = global.__RD;
const D = REPORT_DATA.bop;

console.log('\n=== 1. o payload chegou ======================================');
ok(D && D.dates && D.dates.length > 300, 'bop tem historico mensal longo', D && D.dates && D.dates.length);
ok(REPORT_DATA.comex_pais && REPORT_DATA.comex_pais.dates.length > 300, 'comex_pais tem historico');
ok(Array.isArray(REPORT_DATA.comex_pais.export_china), 'comex_pais agora traz export_china (detalhe novo)');
ok(Array.isArray(REPORT_DATA.comex_pais.import_china), 'comex_pais agora traz import_china');
ok(Array.isArray(REPORT_DATA.comex_fator_agregado.export_basicos), 'comex_fator_agregado traz export_basicos');
ok(Array.isArray(REPORT_DATA.comex_produto.import_soja), 'comex_produto traz import_soja');

console.log('\n=== 2. a regua de periodo: o bug do "10a" ====================');
// Este e o teste de regressao. Com o rangeselector nativo, "10a" terminava a
// janela no range ATUAL do eixo (dado + padding do Plotly); aqui tem de terminar
// no ULTIMO DADO (mais, no maximo, meio passo da propria serie).
const dts = D.dates;
const ultimoMs = Date.parse(dts[dts.length - 1]);
const primeiroMs = Date.parse(dts[0]);
const meioPasso = (ultimoMs - Date.parse(dts[dts.length - 2])) / 2;
const opts = _rangeOptions(dts);
ok(opts.length === 5, 'a regua tem 5 faixas', opts.map(o => o.label).join('/'));

const dez = opts.find(o => o.label === '10a');
const tudo = opts.find(o => o.label === 'Tudo');
const fimDez = parseNaive(dez.to);
const excedente = (fimDez - ultimoMs) / 86400000;
console.log(`          ultimo dado ${dts[dts.length - 1]} | fim da janela 10a ${dez.to}`);
console.log(`          excedente: ${excedente.toFixed(1)} dias (o bug antigo dava ~800+)`);
ok(fimDez <= ultimoMs + meioPasso + 1000, '"10a" termina no ultimo dado (+ meio passo, nao mais)', dez.to);
ok(excedente < 20, 'o excedente a direita e de dias, nao de anos', excedente.toFixed(1) + ' dias');

// "10a" tem de comecar 10 anos antes do ULTIMO DADO -- nao 10 anos antes de um
// fim inflado, que era o que empurrava a janela inteira para frente.
const inicioDez = parseNaive(dez.from);
const esperado = new Date(ultimoMs); esperado.setUTCFullYear(esperado.getUTCFullYear() - 10);
near(inicioDez, esperado.getTime(), 86400000, '"10a" comeca exatamente 10 anos antes do ultimo dado');

// "Tudo" tambem calcula das series, nao chama xaxis.autorange -- autorange
// devolve o span MAIS o padding, o mesmo defeito com outra roupa (ver a nota de
// 2026-08-26 em .claude/rules/lis-dashboards.md).
ok(Math.abs(parseNaive(tudo.from) - primeiroMs) <= meioPasso + 1000, '"Tudo" comeca no primeiro dado', tudo.from);
ok(Math.abs(parseNaive(tudo.to) - ultimoMs) <= meioPasso + 1000, '"Tudo" termina no ultimo dado', tudo.to);
ok(JSON.stringify(opts).indexOf('autorange') < 0, 'nenhuma faixa usa xaxis.autorange');
ok(JSON.stringify(opts).indexOf('stepmode') < 0, 'nenhuma faixa usa stepmode');

// E o clique tem de MEXER no grafico, nao so existir.
const barra = cardOf['chart-bop-tree'].parentNode.querySelector('.range-bar');
ok(!!barra, 'a regua foi inserida no DOM ao lado do grafico');
ok(barra.parentNode.classList.contains('chart-with-range'), 'card e regua ficam no mesmo embrulho');
ok(barra.parentNode.children.indexOf(cardOf['chart-bop-tree']) < barra.parentNode.children.indexOf(barra),
   'a regua fica ABAIXO do grafico (convencao de 2026-08-27)');
const antes = relayoutCalls.length;
barra.children.find(b => b.textContent === '10a').click();
ok(relayoutCalls.length === antes + 1, 'clicar em "10a" chama Plotly.relayout', relayoutCalls.length - antes);
const ultRelayout = relayoutCalls[relayoutCalls.length - 1];
ok(ultRelayout.div === 'chart-bop-tree' && !!ultRelayout.upd['xaxis.range'],
   'o relayout mexe no xaxis.range do proprio grafico');
ok(parseNaive(ultRelayout.upd['xaxis.range'][1]) <= ultimoMs + meioPasso + 1000,
   'a janela aplicada no clique termina no ultimo dado');

console.log('\n=== 2b. a VISTA INICIAL tambem nao abre com faixa vazia ======');
// Terceira encarnacao do mesmo defeito, agora na primeira pintura. O relatorio
// deixava a vista inicial no autorange do Plotly, que devolve o extremo do ARRAY x
// mais um padding percentual do span -- e um ponto com y nulo continua contando
// para esse extremo. Em chart-cc-tree isso valia 26,6 ANOS de faixa vazia: a aba
// Fluxo Cambial tem um payload so, cuja grade vai a 1982-02 por causa do saldo da
// Tabela 14, enquanto as series da Tabela 13 comecam em 2008-09. A regra agora e a
// mesma dos botoes: a janela vem sempre do dado, inclusive a que significa "tudo".
{
  function extentTraces(traces) {
    let lo = Infinity, hi = -Infinity, passo = 0;
    (traces || []).forEach(t => {
      if (!t.x) return;
      for (let i = 0; i < t.x.length; i++) {
        if (!t.y || t.y[i] === null || t.y[i] === undefined) continue;
        const x = parseNaive(t.x[i]);
        if (isNaN(x)) continue;
        if (x < lo) lo = x;
        if (x > hi) hi = x;
      }
      if (t.x.length > 1) {
        passo = Math.max(passo, Math.abs(parseNaive(t.x[t.x.length - 1]) - parseNaive(t.x[t.x.length - 2])));
      }
    });
    return lo === Infinity ? null : { lo, hi, passo };
  }

  const semJanela = [], comBanda = [];
  Object.keys(tracesIniciais).forEach(div => {
    const e = extentTraces(tracesIniciais[div]);
    if (!e) return;
    const j = janelaInicial[div];
    if (!j) { semJanela.push(div); return; }
    // Tolerancia = meio passo da propria serie (barras e celulas sao centradas no
    // seu x, entao a janela precisa desse tanto para nao cortar a ultima ao meio)
    // + 1 dia de folga de arredondamento.
    const tol = e.passo / 2 + 86400000;
    const esq = e.lo - parseNaive(j[0]), dir = parseNaive(j[1]) - e.hi;
    if (esq > tol || dir > tol) {
      comBanda.push(`${div}: ${(esq / 2629800000).toFixed(1)}m esq / ${(dir / 2629800000).toFixed(1)}m dir`);
    }
  });
  ok(semJanela.length === 0,
     'todo grafico APLICA uma janela X calculada (nenhum fica no autorange do Plotly)',
     semJanela.join(', '));
  ok(comBanda.length === 0,
     'nenhum grafico abre com faixa vazia dos dois lados (tolerancia: meio passo da serie)',
     comBanda.join(' | '));
}
// Regressao nominal do caso que motivou a rodada: a grade do payload e MUITO maior
// que a serie plotada, e a janela tem de seguir a serie, nao a grade.
{
  const grade = REPORT_DATA.cambio_contratado.dates;
  ok(grade[0] < '1990', 'a grade de cambio_contratado de fato comeca nos anos 1980', grade[0]);
  const primeiroT13 = grade[REPORT_DATA.cambio_contratado.cc_saldo_total.findIndex(v => v != null)];
  ok(primeiroT13 > '2008', 'e as series da Tabela 13 so comecam em 2008', primeiroT13);
  const j = janelaInicial['chart-cc-tree'];
  ok(!!j && String(j[0]) >= '2008', 'chart-cc-tree abre em 2008, nao na ponta da grade',
     j && String(j[0]).slice(0, 10));
}

console.log('\n=== 3. todos os graficos das abas de dados ganharam regua ====');
const semRegua = Object.keys(cardOf).filter(divId => {
  const w = cardOf[divId].parentNode;
  return !(w && w.classList.contains('chart-with-range') && w.querySelector('.range-bar'));
});
ok(semRegua.length === 0, 'nenhum grafico ficou sem regua de periodo', semRegua.join(', '));
// Piso de fumaca: confirma que o harness achou os graficos de verdade, e nao que
// a contagem esta num numero exato -- este relatorio ganha e perde grafico por
// pedido do usuario (6 abas de dados no inicio, 4 desde 2026-09-01). Quem afirma
// composicao exata e a secao 15, e so para a aba que acabou de mudar.
ok(Object.keys(cardOf).length >= 14, 'o harness achou os graficos das abas de dados', Object.keys(cardOf).length);

console.log('\n=== 4. seletor por grafico, nao por aba ======================');
['bop', 'comex-pais', 'comex-fator', 'comex-produto'].forEach(pfx => {
  ok(!!registry['sel-' + pfx + '-period'], `${pfx}: tem seletor de agregacao proprio`);
  ok(!!registry['sel-' + pfx + '-kind'], `${pfx}: tem seletor de tipo de grafico proprio`);
});
ok(!!registry['sel-bop-mode'], 'so o BP tem seletor de unidade (USD Bi / % do PIB)');
ok(!registry['sel-comex-pais-mode'], 'os recortes do Comex nao tem "% do PIB" (fonte diferente)');
ok(htmlBruto.indexOf('bop-period-selector') < 0, 'o seletor unico de aba saiu do HTML');
ok(htmlBruto.indexOf('bop-mode-selector') < 0, 'o seletor unico de unidade saiu do HTML');

console.log('\n=== 5. "Balanca de Bens - Detalhe" foi removida ==============');
ok(htmlBruto.indexOf('sec-bop-bens"') < 0, 'a secao sumiu do HTML');
ok(htmlBruto.indexOf('chart-bop-bens"') < 0, 'o grafico sumiu do HTML');
ok(htmlBruto.indexOf('Balança de Bens — Detalhe') < 0, 'o titulo sumiu do HTML');
// mas o ramo continua na arvore -- sem ele a Conta Corrente nao fecha
const chaves = [];
(function walk(ns) { ns.forEach(n => { chaves.push(n.key); if (n.children) walk(n.children); }); })(BOP_TREE_FULL);
ok(chaves.indexOf('balanca_bens') >= 0, 'o ramo "Balanca de Bens" continua na arvore (aditividade)');

console.log('\n=== 6. a arvore unica cobre o que os 6 graficos mostravam ====');
[['conta_corrente', 'Conta Corrente'], ['servicos', 'Servicos'], ['renda_primaria', 'Renda Primaria'],
 ['conta_financeira', 'Conta Financeira'], ['investimentos_ativos', 'Investimentos - Ativos'],
 ['acoes_fundos_ativos', 'Acoes e Fundos (ex-grafico Ativos Externos)'],
 ['titulos_ativos_lp', 'Titulos LP (ex-grafico Ativos Externos)'],
 ['investimento_direto_liquido', 'IDP (ex-grafico Financiamento Externo)'],
 // O ex-grafico "Financiamento Externo" agrupava por PRAZO atravessando categorias
 // funcionais ("Empr./Tit. LP Externo" = titulo de carteira + emprestimo de outros
 // investimentos). A reorganizacao de 2026-08-27 desfez esse agrupamento, mas nao
 // perdeu nenhum item: cada metade virou linha propria sob a sua categoria.
 ['titulos_externo_lp', 'Titulos Externo LP (metade do ex-"Empr./Tit. LP")'],
 ['emprestimos_lp_passivos', 'Emprestimos LP (a outra metade)'],
 ['titulos_externo_cp', 'Titulos Externo CP (metade do ex-"Empr./Tit. CP")'],
 ['emprestimos_cp_passivos', 'Emprestimos CP (a outra metade)'],
 ['acoes_totais', 'Acoes e Fundos - Passivos (ex-"Acoes Totais")'],
 ['titulos_dom', 'Titulos Mercado Domestico'],
 ['demais_outros_passivos', 'Demais (residuo de Outros Investimentos - Passivos)'],
 ['conta_capital', 'Conta Capital'], ['erros_omissoes', 'Erros e Omissoes'],
].forEach(([k, nome]) => ok(chaves.indexOf(k) >= 0, `a arvore tem ${nome}`));
ok(new Set(chaves).size === chaves.length, 'nenhuma chave repetida na arvore do BP',
   chaves.length - new Set(chaves).size);

console.log('\n=== 7. a tabela renderizou e os filhos somam o pai ===========');
const corpo = registry['bop-tree-body'];
ok(corpo.children.length > 0, 'a tabela do BP tem linhas', corpo.children.length);
const cab = registry['bop-tree-head'];
ok(cab.children[0].children.length === 14, 'cabecalho = check + rotulo + 12 colunas de periodo',
   cab.children[0].children.length);

// Aditividade lida da PROPRIA tabela: some as celulas dos filhos e compare com a
// celula do pai, em cada uma das 12 colunas. E o invariante que uma arvore errada
// quebra sem lancar excecao nenhuma.
function celulas(node, periodo, modo) {
  const sel = registry['sel-bop-period']; sel.value = periodo; sel.change();
  const selM = registry['sel-bop-mode']; selM.value = modo; selM.change();
  return null;
}
// Busca por CHAVE, nao por rotulo: desde a reorganizacao de 2026-08-27 os dois
// lados da Conta Financeira usam as mesmas categorias, entao "Investimento em
// Carteira" e "Acoes e Fundos" existem duas vezes na arvore com rotulo identico.
function valoresDaLinha(chave) {
  const linha = corpo.children.find(tr => tr.dataset.key === chave);
  if (!linha) return null;
  return linha.children.slice(2).map(td => {
    const t = td.textContent;
    return t === '—' ? null : parseFloat(t.replace('%', '').replace(',', '.'));
  });
}
// Aditividade lida da PROPRIA tabela renderizada: soma as celulas dos filhos e
// compara com a celula do pai, coluna a coluna. E o invariante que uma arvore
// remontada errada quebra sem lancar excecao nenhuma -- o unico jeito de saber que
// a reorganizacao nao inventou um pai que nao e a soma dos seus filhos.
// A tolerancia e o arredondamento de EXIBICAO (1 casa em USD Bi, 2 em % PIB),
// multiplicado pelo numero de parcelas.
function checaSoma(msg, paiKey, filhosKeys, modo) {
  const pai = valoresDaLinha(paiKey);
  const filhos = filhosKeys.map(valoresDaLinha);
  if (!pai || filhos.some(f => !f)) { ok(false, msg, 'linha nao encontrada na tabela'); return; }
  let pior = 0, n = 0;
  for (let i = 0; i < 12; i++) {
    if (pai[i] == null || filhos.some(f => f[i] == null)) continue;
    pior = Math.max(pior, Math.abs(pai[i] - filhos.reduce((a, f) => a + f[i], 0)));
    n++;
  }
  const passo = (modo === 'pct' ? 0.005 : 0.05);
  const tol = passo * (filhosKeys.length + 1) + 1e-9;
  // Nem toda coluna precisa ter valor: desde 2026-08-27 o trimestre/ano EM CURSO
  // sai em branco (regra de periodo incompleto, ver analytics/metric_layers.md), e
  // por isso a agregacao trimestral/anual entrega 11 colunas cheias, nao 12.
  ok(n >= 10 && pior <= tol, msg, `n=${n} pior=${pior.toFixed(3)} tol=${tol.toFixed(3)}`);
}

['monthly', 'quarterly', 'annual', 'ttm'].forEach(periodo => {
  ['abs', 'pct'].forEach(modo => {
    celulas(null, periodo, modo);
    registry['btn-bop-expand'].click();     // todas as linhas visiveis
    checaSoma(`${periodo}/${modo}: Conta Corrente = soma dos 3 filhos nas 12 colunas`,
              'conta_corrente', ['balanca_bens_servicos', 'renda_primaria', 'renda_secundaria'], modo);
  });
});

// A arvore inteira, ramo a ramo, em USD Bi mensal. Cada linha destas e um pai que
// tem de fechar com os seus filhos depois da reorganizacao.
registry['sel-bop-period'].value = 'monthly'; registry['sel-bop-period'].change();
registry['sel-bop-mode'].value = 'abs'; registry['sel-bop-mode'].change();
registry['btn-bop-expand'].click();

checaSoma('Bens e Servicos = Balanca de Bens + Servicos',
          'balanca_bens_servicos', ['balanca_bens', 'servicos'], 'abs');
checaSoma('Balanca de Bens = Mercadorias + Ouro + Merchanting',
          'balanca_bens', ['mercadorias_gerais', 'ouro_nao_monetario', 'merchanting'], 'abs');
checaSoma('Mercadorias em Geral = Exportacao + Importacao(negada)',
          'mercadorias_gerais', ['mercadorias_gerais_export', 'mercadorias_gerais_import'], 'abs');
checaSoma('Servicos = Viagens + Transportes + Aluguel + Demais',
          'servicos', ['viagens', 'transportes', 'aluguel_equipamentos', 'demais_servicos'], 'abs');
checaSoma('Renda Primaria = Remuneracao + Juros + Lucros/Dividendos',
          'renda_primaria', ['remuneracao_empregados', 'juros', 'lucros_dividendos'], 'abs');
checaSoma('Conta Financeira = Ativos + Passivos + Derivativos + Reserva',
          'conta_financeira', ['investimentos_ativos', 'investimentos_passivos', 'derivativos', 'ativos_reserva'], 'abs');
checaSoma('Ativos = Direto + Carteira + Outros',
          'investimentos_ativos', ['idp_exterior', 'portfolio_ativos', 'outros_inv_ativos'], 'abs');
checaSoma('Carteira-Ativos = Acoes/Fundos + Titulos LP + Titulos CP',
          'portfolio_ativos', ['acoes_fundos_ativos', 'titulos_ativos_lp', 'titulos_ativos_cp'], 'abs');

console.log('\n=== 7b. o lado Passivos agora espelha o lado Ativos ==========');
// Este bloco e a razao de a reorganizacao existir: antes, Passivos era uma mistura
// de criterios (funcional + instrumento + prazo, com "Empr./Tit. LP Externo"
// somando titulo de carteira com emprestimo de outros investimentos, ou seja,
// atravessando duas categorias funcionais). Agora os dois lados sao as mesmas 3
// categorias do BPM6, e cada uma tem de fechar com os seus filhos.
checaSoma('Passivos = Direto + Carteira + Outros (mesmas 3 categorias dos Ativos)',
          'investimentos_passivos', ['investimento_direto_liquido', 'portfolio_passivos', 'outros_inv_passivos'], 'abs');
checaSoma('Carteira-Passivos = Acoes/Fundos + Tit. Domestico + Tit. Externo LP + CP',
          'portfolio_passivos', ['acoes_totais', 'titulos_dom', 'titulos_externo_lp', 'titulos_externo_cp'], 'abs');
checaSoma('Outros-Passivos = Emprestimos LP + Emprestimos CP + Demais',
          'outros_inv_passivos', ['emprestimos_lp_passivos', 'emprestimos_cp_passivos', 'demais_outros_passivos'], 'abs');

// Simetria estrutural, nao so aritmetica: os dois lados tem de ter o MESMO conjunto
// de categorias filhas, senao voltaram a divergir de criterio.
function filhosDe(chave) {
  let achado = null;
  (function walk(ns) { ns.forEach(n => { if (n.key === chave) achado = n; if (n.children) walk(n.children); }); })(BOP_TREE_FULL);
  return achado && achado.children ? achado.children.map(c => c.label) : null;
}
ok(JSON.stringify(filhosDe('investimentos_ativos').slice(1)) ===
   JSON.stringify(filhosDe('investimentos_passivos').slice(1)),
   'Ativos e Passivos abrem nas mesmas categorias (Carteira, Outros Investimentos)',
   filhosDe('investimentos_ativos') + ' vs ' + filhosDe('investimentos_passivos'));

console.log('\n=== 7c. a identidade do BP e a ordem das contas ==============');
// Conta Corrente + Conta Capital + Conta Financeira + Erros e Omissoes = 0, com a
// convencao de sinal deste relatorio. E o que justifica as 4 contas serem os nos de
// topo, e o que a ordem antiga (Capital DEPOIS de Financeira) escondia.
{
  const contas = ['conta_corrente', 'conta_capital', 'conta_financeira', 'erros_omissoes'];
  const vals = contas.map(valoresDaLinha);
  let pior = 0, n = 0;
  for (let i = 0; i < 12; i++) {
    if (vals.some(v => v[i] == null)) continue;
    pior = Math.max(pior, Math.abs(vals.reduce((a, v) => a + v[i], 0)));
    n++;
  }
  ok(n === 12 && pior <= 0.25, 'as 4 contas somam zero nas 12 colunas (identidade do BP)',
     `n=${n} pior=${pior.toFixed(3)}`);
}
ok(JSON.stringify(BOP_TREE_FULL.map(n => n.key)) ===
   JSON.stringify(['conta_corrente', 'conta_capital', 'conta_financeira', 'erros_omissoes']),
   'as contas estao na ordem do BPM6, com Erros e Omissoes por ultimo',
   BOP_TREE_FULL.map(n => n.key).join(' > '));

console.log('\n=== 7d. alinhamento das linhas ===============================');
// O que fazia a arvore PARECER baguncada mesmo com a hierarquia certa: folha sem o
// espacador do "▸" comecava 16px a esquerda de um grupo do mesmo nivel, e o
// quadradinho de cor so existia na linha marcada, entao marcar a caixa empurrava o
// rotulo. As duas colunas invisiveis tem de existir em TODA linha.
{
  const semToggle = corpo.children.filter(tr =>
    !tr.children[1].children.some(c => c.classList && c.classList.contains('tree-toggle')));
  ok(semToggle.length === 0, 'toda linha tem o espacador do toggle (folha inclusive)', semToggle.length);
  const semSwatch = corpo.children.filter(tr =>
    !tr.children[1].children.some(c => c.classList && c.classList.contains('swatch-dot')));
  ok(semSwatch.length === 0, 'toda linha reserva o espaco do quadradinho de cor', semSwatch.length);
  // e a ordem dentro da celula e sempre toggle -> swatch -> texto
  const ordemOk = corpo.children.every(tr => {
    const f = tr.children[1].children;
    return f[0].classList.contains('tree-toggle') && f[1].classList.contains('swatch-dot');
  });
  ok(ordemOk, 'a celula do rotulo tem sempre a mesma ordem: toggle, cor, texto');
  // marcar/desmarcar nao pode mexer no numero de elementos antes do texto
  const antesN = corpo.children[0].children[1].children.length;
  const cb0 = corpo.children[0].children[0].children[0];
  const estado = cb0.checked;
  cb0.checked = !estado; cb0.fire('change');
  const linha0 = corpo.children.find(tr => tr.dataset.key === 'conta_corrente');
  ok(linha0.children[1].children.length === antesN,
     'marcar a caixa nao desloca o rotulo (mesma contagem de elementos)',
     `${antesN} -> ${linha0.children[1].children.length}`);
  cb0.checked = estado; cb0.fire('change');
}

console.log('\n=== 7e. a tabela fica ACIMA do grafico =======================');
[['bop-tree', 'chart-bop-tree'], ['comex-pais', 'chart-comex-pais'],
 ['comex-fator', 'chart-comex-fator'], ['comex-produto', 'chart-comex-produto']].forEach(([tid, cid]) => {
  const iTab = htmlBruto.indexOf('id="' + tid + '-table"');
  const iCht = htmlBruto.indexOf('id="' + cid + '"');
  ok(iTab > 0 && iCht > 0 && iTab < iCht, `${tid}: a tabela vem antes do grafico no HTML`,
     `tabela@${iTab} grafico@${iCht}`);
});

console.log('\n=== 7f. nomes de legenda desambiguados =======================');
// "Exportacao" existe sob Mercadorias e sob Ouro; "Acoes e Fundos" existe dos dois
// lados da Conta Financeira. Na tabela o recuo resolve; na legenda nao ha recuo.
{
  const nomes = buildDisplayNames(BOP_TREE_FULL);
  const vals = Object.keys(nomes).map(k => nomes[k]);
  ok(new Set(vals).size === vals.length, 'nenhum nome de legenda se repete na arvore do BP',
     vals.length - new Set(vals).size);
  ok(nomes['conta_corrente'] === 'Conta Corrente', 'no unico mantem o rotulo curto', nomes['conta_corrente']);
  ok(nomes['mercadorias_gerais_export'].indexOf('Mercadorias em Geral') === 0,
     'no repetido recebe o pai', nomes['mercadorias_gerais_export']);
  ok(nomes['acoes_fundos_ativos'] !== nomes['acoes_totais'],
     'os dois "Acoes e Fundos" ficam distinguiveis',
     nomes['acoes_fundos_ativos'] + ' vs ' + nomes['acoes_totais']);
}

console.log('\n=== 7g. CSS: a colisao de nome de classe nao pode voltar =====');
// Assercoes sobre o TEXTO do CSS, nao sobre o DOM -- nao ha browser aqui para
// resolver cascata. Existem por um bug real: a metade de modelo do relatorio (o
// ex-dashboard PPP, fundido em 2026-08) traz um bloco `table.data-table` que ficou
// SEM o escopo .ppp-scope que todo o resto daquela metade tem. Enquanto so ela
// usava esse nome de classe, ninguem notou. Quando a aba BP ganhou tabelas com o
// mesmo nome, `table.data-table td { text-align: right }` capturou as celulas de
// rotulo: o recuo por padding-left continuava sendo aplicado, mas com o texto
// encostado na direita ele nao desenhava nada e a arvore virava uma lista chapada.
{
  const css = htmlBruto.slice(htmlBruto.indexOf('<style>'), htmlBruto.indexOf('</style>'));
  // Os comentarios saem ANTES da varredura: a explicacao do bug, escrita no proprio
  // CSS, cita a regra defeituosa literalmente e faria o teste acusar a si mesmo.
  const cssSemComentarios = css.replace(/\/\*[\s\S]*?\*\//g, '');
  const semEscopo = cssSemComentarios.split('\n')
    .map(l => l.trim())
    .filter(l => l.indexOf('table.data-table') >= 0 && l.indexOf('.ppp-scope') < 0);
  ok(semEscopo.length === 0,
     'nenhuma regra `table.data-table` fora de .ppp-scope (era o que alinhava os rotulos a direita)',
     semEscopo.join(' | '));
  ok(/\.data-table td\.col-label\s*{[^}]*text-align:\s*left/.test(css),
     'a celula de rotulo declara text-align:left explicitamente (defesa contra a proxima colisao)');
  ok(/\.data-table tbody tr\.is-group\s*>\s*td\s*{[^}]*background/.test(css),
     'linha pai tem fundo cinza');
  ok(/\.data-table tbody tr\.is-account\s*>\s*td\s*{[^}]*background/.test(css),
     'conta do BP tem o seu proprio tom de cinza');
  // o hover precisa vir DEPOIS dos fundos, ou sumiria justamente nas linhas pai
  ok(css.indexOf('tr:hover > td') > css.indexOf('tr.is-account > td'),
     'a regra de hover vem depois das de fundo (mesma especificidade, quem vem depois ganha)');
  // Os 600px ficam no div do GRAFICO, nao no card: o card ganhou cabecalho, e uma
  // altura fixa nele faria o cabecalho comer parte da area de plotagem.
  ok(/\.chart-card\s*>\s*div\s*{[^}]*height:\s*600px/.test(css), 'os graficos tem 600px de altura');
  ok(!/\.chart-card\s*{[^}]*height:\s*\d/.test(cssSemComentarios),
     'o card em si nao tem altura fixa (senao o cabecalho sairia de dentro do grafico)');
}

console.log('\n=== 7g2. periodo incompleto sai em branco ====================');
// Regra escrita em analytics/metric_layers.md: janela incompleta mostra nada -- nem
// soma parcial, nem estimativa sinalizada. aggregateSum() nao a seguia: com a serie
// terminando em jul/2026 ela entregava um "T3/26" de um mes so e um "2026" de sete,
// somados e impressos ao lado de trimestres e anos completos. A conta corrente de
// 2026 saia -36,0 contra -66,7 de 2025, o que se le como melhora de 46% e e so o ano
// pela metade. Passava despercebido enquanto era a ultima barra de um grafico;
// virou uma coluna rotulada "2026" quando a aba ganhou tabela.
{
  const ultimoMes = parseInt(D.dates[D.dates.length - 1].slice(5, 7), 10);
  const mesesNoAnoCorrente = ultimoMes;
  ok(mesesNoAnoCorrente < 12, 'o payload de fato termina no meio de um ano (senao o teste nao testa nada)',
     `${mesesNoAnoCorrente} meses`);

  const anual = aggregateSum(D.dates, D.conta_corrente, 'annual');
  ok(anual.values[anual.values.length - 1] === null,
     'o ano em curso sai null na agregacao anual', anual.values[anual.values.length - 1]);
  ok(anual.values[anual.values.length - 2] !== null,
     'o ultimo ano COMPLETO continua com valor', anual.values[anual.values.length - 2]);

  const trim = aggregateSum(D.dates, D.conta_corrente, 'quarterly');
  const nQ = trim.values.length;
  const mesesNoUltimoTri = ((ultimoMes - 1) % 3) + 1;
  ok(mesesNoUltimoTri === 3 ? trim.values[nQ - 1] !== null : trim.values[nQ - 1] === null,
     'o trimestre em curso sai null a menos que esteja fechado',
     `${mesesNoUltimoTri} mes(es) no ultimo trimestre -> ${trim.values[nQ - 1]}`);

  // e a tabela tem de refletir isso, nao so a funcao
  registry['sel-bop-period'].value = 'annual'; registry['sel-bop-period'].change();
  registry['sel-bop-mode'].value = 'abs'; registry['sel-bop-mode'].change();
  const linha = valoresDaLinha('conta_corrente');
  ok(linha[11] === null, 'a ultima coluna da tabela anual mostra "—"', linha[11]);
  ok(linha[10] !== null, 'a penultima (ano fechado) mostra valor', linha[10]);

  // O cabecalho e a regua tem de anunciar o periodo REALMENTE plotado -- se ainda
  // dissessem "a dez/2026" o leitor procuraria um dado que a regra acabou de vetar.
  ok(cabecalho('chart-bop-tree').indexOf('/' + D.dates[D.dates.length - 1].slice(0, 4) + ' a ') < 0 ||
     cabecalho('chart-bop-tree').indexOf('dez/') < 0,
     'o cabecalho nao anuncia um bucket que saiu em branco', cabecalho('chart-bop-tree'));
  registry['sel-bop-period'].value = 'monthly'; registry['sel-bop-period'].change();
}

console.log('\n=== 7h. cabecalho de cada grafico ============================');
// Bloco de tres linhas acima da area de plotagem: o que e, o que mede/em que
// unidade, e a fonte + o periodo coberto. Existe para o grafico se explicar sozinho
// quando circula como print, longe do <h2> da secao e das notas.
function cabecalho(divId) {
  const card = cardOf[divId];
  const h = card && card.querySelector('.chart-head');
  return h ? h.innerHTML : null;
}
{
  const semCabecalho = Object.keys(cardOf).filter(d => !cabecalho(d));
  ok(semCabecalho.length === 0, 'todos os graficos das abas de dados tem cabecalho',
     semCabecalho.join(', '));

  const semTitulo = Object.keys(cardOf).filter(d => (cabecalho(d) || '').indexOf('<h3>') < 0);
  ok(semTitulo.length === 0, 'todo cabecalho tem titulo', semTitulo.join(', '));

  const semFonte = Object.keys(cardOf).filter(d => (cabecalho(d) || '').indexOf('Fonte:') < 0);
  ok(semFonte.length === 0, 'todo cabecalho declara a fonte', semFonte.join(', '));

  // O periodo tem de vir das datas PLOTADAS, nao de um intervalo escrito a mao que
  // envelheceria a cada divulgacao. Confere o texto contra o payload.
  const rePeriodo = /(jan|fev|mar|abr|mai|jun|jul|ago|set|out|nov|dez)\/\d{4} a (jan|fev|mar|abr|mai|jun|jul|ago|set|out|nov|dez)\/\d{4}/;
  const semPeriodo = Object.keys(cardOf).filter(d => !rePeriodo.test(cabecalho(d) || ''));
  ok(semPeriodo.length === 0, 'todo cabecalho declara o periodo coberto', semPeriodo.join(', '));

  const MESES = ['jan','fev','mar','abr','mai','jun','jul','ago','set','out','nov','dez'];
  function esperado(dates) {
    const f = dt => MESES[parseInt(dt.slice(5, 7), 10) - 1] + '/' + dt.slice(0, 4);
    return f(dates[0]) + ' a ' + f(dates[dates.length - 1]);
  }
  ok(cabecalho('chart-ptax').indexOf(esperado(REPORT_DATA.ptax.dates)) > 0,
     'o periodo do PTAX bate com as datas do payload', esperado(REPORT_DATA.ptax.dates));
  ok(cabecalho('chart-bop-tree').indexOf(esperado(D.dates)) > 0,
     'o periodo do BP bate com as datas do payload', esperado(D.dates));

  // Nenhum grafico pode ter ficado com o title do Plotly: seria titulo em dobro.
  const comTitlePlotly = newPlotCalls.concat(reactCalls).filter(c => c.layout && c.layout.title);
  ok(comTitlePlotly.length === 0, 'nenhum grafico ainda desenha title pelo Plotly',
     comTitlePlotly.map(c => c.div).join(', '));

  // O cabecalho da arvore e dinamico: acompanha o seletor de unidade.
  registry['sel-bop-mode'].value = 'abs'; registry['sel-bop-mode'].change();
  const cabAbs = cabecalho('chart-bop-tree');
  registry['sel-bop-mode'].value = 'pct'; registry['sel-bop-mode'].change();
  const cabPct = cabecalho('chart-bop-tree');
  ok(cabAbs.indexOf('USD bilhões') > 0 && cabPct.indexOf('% do PIB') > 0,
     'o cabecalho da arvore acompanha o seletor de unidade');
  registry['sel-bop-mode'].value = 'abs'; registry['sel-bop-mode'].change();

  // ...e o de tipo de grafico, e a lista de linhas marcadas.
  registry['sel-bop-kind'].value = 'lines'; registry['sel-bop-kind'].change();
  ok(cabecalho('chart-bop-tree').indexOf('linhas') > 0, 'o cabecalho diz o tipo de grafico');
  registry['sel-bop-kind'].value = 'bars'; registry['sel-bop-kind'].change();
  ok(cabecalho('chart-bop-tree').indexOf('barras empilhadas') > 0, 'e volta ao trocar de novo');
  ok(cabecalho('chart-bop-tree').indexOf('Conta Corrente') > 0,
     'o cabecalho lista as linhas marcadas');
}

console.log('\n=== 8. barras empilhadas vs linhas ===========================');
function ultimoReact(divId) {
  for (let i = reactCalls.length - 1; i >= 0; i--) if (reactCalls[i].div === divId) return reactCalls[i];
  return null;
}
registry['sel-bop-kind'].value = 'bars'; registry['sel-bop-kind'].change();
let r = ultimoReact('chart-bop-tree');
let barras = r.traces.filter(t => t.type === 'bar');
let linhas = r.traces.filter(t => t.type === 'scatter');
ok(r.traces.length === 4, 'o padrao plota 4 series (o total + 3 componentes)', r.traces.length);
ok(barras.length === 3 && linhas.length === 1,
   'em "Barras empilhadas": o pai marcado vira LINHA, os 3 filhos viram barras',
   `${barras.length} barras / ${linhas.length} linhas`);
ok(linhas[0].name === 'Conta Corrente', 'a linha e o total, nao um componente', linhas[0].name);
ok(r.layout.barmode === 'relative', "barmode 'relative' (as parcelas trocam de sinal)", r.layout.barmode);
ok(r.traces.indexOf(linhas[0]) === r.traces.length - 1, 'a linha do total vai por ULTIMO, para ficar por cima');

registry['sel-bop-kind'].value = 'lines'; registry['sel-bop-kind'].change();
r = ultimoReact('chart-bop-tree');
ok(r.traces.every(t => t.type === 'scatter'), 'em "Linhas" nenhuma serie fica como barra',
   r.traces.map(t => t.type).join('/'));
ok(r.traces.length === 4, 'e o mesmo conjunto de series', r.traces.length);

// A regra so vale para nos ANINHADOS: dois irmaos marcados continuam barras.
registry['sel-bop-kind'].value = 'bars'; registry['sel-bop-kind'].change();
{
  // desmarca o pai (Conta Corrente) -> os 3 filhos viram barras e nada vira linha
  const linhaPai = corpo.children.find(tr => tr.dataset.key === 'conta_corrente');
  const cb = linhaPai.children[0].children[0];
  cb.checked = false; cb.fire('change');
  r = ultimoReact('chart-bop-tree');
  ok(r.traces.length === 3 && r.traces.every(t => t.type === 'bar'),
     'sem o pai marcado, os 3 irmaos ficam todos como barra',
     r.traces.map(t => t.type).join('/'));
  cb.checked = true; cb.fire('change');
}

console.log('\n=== 9. o toggle "% do PIB" muda de fato o eixo e os numeros ==');
registry['sel-bop-mode'].value = 'abs'; registry['sel-bop-mode'].change();
const rAbs = ultimoReact('chart-bop-tree');
registry['sel-bop-mode'].value = 'pct'; registry['sel-bop-mode'].change();
const rPct = ultimoReact('chart-bop-tree');
ok(rAbs.layout.yaxis.ticksuffix === '' && rPct.layout.yaxis.ticksuffix === '%',
   'o sufixo do eixo Y acompanha a unidade');
// A unidade e dita pelo CABECALHO HTML, nao mais pelo title do Plotly -- desde
// 2026-08-27 o titulo saiu do grafico e virou um bloco de tres linhas acima dele.
ok(cabecalho('chart-bop-tree').indexOf('% do PIB') > 0,
   'o cabecalho diz a unidade escolhida', cabecalho('chart-bop-tree'));
ok(!rPct.layout.title, 'o grafico nao tem mais title do Plotly (seria o titulo em dobro)');
{
  // % do PIB tem de dividir pelo PIB da MESMA janela: no anual, soma de 12 meses
  // de fluxo / soma de 12 meses de PIB.
  registry['sel-bop-period'].value = 'annual'; registry['sel-bop-period'].change();
  const rA = ultimoReact('chart-bop-tree');
  const cc = rA.traces.find(t => t.name === 'Conta Corrente');
  const ultimoCC = cc.y.filter(v => v != null).slice(-1)[0];
  ok(ultimoCC > -12 && ultimoCC < 12, 'conta corrente anual em % do PIB fica em faixa plausivel',
     ultimoCC && ultimoCC.toFixed(2));
}
registry['sel-bop-period'].value = 'monthly'; registry['sel-bop-period'].change();
registry['sel-bop-mode'].value = 'abs'; registry['sel-bop-mode'].change();

console.log('\n=== 10. Comex: exportacao - importacao = saldo ===============');
[['comex-pais', 'comex_pais', ['china', 'eua', 'argentina', 'alemanha', 'demais'], 'mundo'],
 ['comex-fator', 'comex_fator_agregado', ['basicos', 'semimanufaturados', 'manufaturados', 'demais'], 'total'],
 ['comex-produto', 'comex_produto', ['soja', 'petroleo', 'minerio_ferro', 'carnes', 'cafe', 'demais'], 'mundo'],
].forEach(([pfx, key, itens, totalKey]) => {
  const dd = REPORT_DATA[key];
  let piorSaldo = 0, piorTotal = 0;
  for (let i = 0; i < dd.dates.length; i++) {
    itens.forEach(it => {
      const s = dd['saldo_' + it], x = dd['export_' + it], m = dd['import_' + it];
      if (s[i] != null && x[i] != null && m[i] != null) piorSaldo = Math.max(piorSaldo, Math.abs(s[i] - (x[i] - m[i])));
    });
    const soma = itens.reduce((a, it) => a + (dd['saldo_' + it][i] || 0), 0);
    const tot = dd['saldo_' + totalKey][i];
    if (tot != null) piorTotal = Math.max(piorTotal, Math.abs(tot - soma));
  }
  ok(piorSaldo < 1e-9, `${pfx}: saldo = exportacao - importacao em toda a serie`, piorSaldo);
  ok(piorTotal < 1e-9, `${pfx}: os itens somam o total em toda a serie`, piorTotal);

  const corpoC = registry[pfx.replace('comex-', 'comex-') + '-body'];
  ok(corpoC.children.length > 0, `${pfx}: a tabela renderizou`, corpoC.children.length);
  const rc = ultimoReact('chart-' + pfx);
  ok(rc && rc.traces.length > 0, `${pfx}: o grafico renderizou`, rc && rc.traces.length);
  ok(rc.traces.filter(t => t.type === 'scatter').length === 1,
     `${pfx}: o total marcado e a unica linha; os itens sao barras`,
     rc.traces.map(t => t.type).join('/'));
});

// Expandir um item do Comex tem de revelar Exportacao/Importacao -- o detalhe que
// a fonte tem e o BPM6 nao, e a razao de essas tabelas existirem separadas.
registry['btn-comex-pais-expand'].click();
{
  const corpoC = registry['comex-pais-body'];
  const rotulos = corpoC.children.map(tr => tr.children[1].children.filter(c => c.nodeType === 3).map(c => c.textContent).join(''));
  ok(rotulos.filter(t => t === 'Exportação').length === 5, 'cada um dos 5 parceiros abre em Exportacao',
     rotulos.filter(t => t === 'Exportação').length);
  ok(rotulos.filter(t => t === 'Importação (saída)').length === 5, 'e em Importacao (saida)');
}

console.log('\n=== 10b. a aba Fluxo Cambial ================================');
// A aba foi reconstruida em 2026-08-27 sobre cmb_cambio_contratado. A anterior lia
// cmb_fluxo_cambial, que NAO e fluxo cambial: o "saldo total" de la sobe de 81,0 a
// 82,9 em 307 meses e nunca troca de sinal, enquanto um saldo de fluxo cambial
// oscila em torno de zero. Correlacao entre os dois: 0,05. Estas assercoes existem
// para que ninguem religue a fonte antiga por engano.
ok(htmlBruto.indexOf('REPORT_DATA.fluxo') < 0, 'o relatorio nao le mais REPORT_DATA.fluxo');
['chart-fluxo', 'chart-fluxo-breakdown', 'chart-interbank-vol'].forEach(id => {
  ok(htmlBruto.indexOf('id="' + id + '"') < 0, `o grafico antigo ${id} saiu do HTML`);
});
ok(!!REPORT_DATA.cambio_contratado && REPORT_DATA.cambio_contratado.dates.length > 200,
   'o payload traz cambio_contratado', REPORT_DATA.cambio_contratado &&
   REPORT_DATA.cambio_contratado.dates.length);

// A ordem das abas no nav: Fluxo Cambial em 2o lugar (pedido do usuario), e o painel
// no HTML tem de seguir a mesma ordem da navegacao.
const ordemNav = [...htmlBruto.matchAll(/<button class="tab-btn" data-tab="([\w-]+)">/g)].map(m => m[1]);
ok(ordemNav[0] === 'tab-bop' && ordemNav[1] === 'tab-flow',
   'Fluxo Cambial e a 2a aba do nav', ordemNav.slice(0, 4).join(' > '));
const ordemPaineis = [...htmlBruto.matchAll(/<div class="tab-panel[^"]*" id="([\w-]+)">/g)].map(m => m[1]);
ok(ordemPaineis[0] === 'tab-bop' && ordemPaineis[1] === 'tab-flow',
   'o painel esta na mesma ordem do nav', ordemPaineis.slice(0, 4).join(' > '));

// Seletor e tabela em cada um dos 3 graficos da aba
['cc', 'ccdet', 'ib'].forEach(pfx => {
  ok(!!registry['sel-' + pfx + '-period'], `${pfx}: tem seletor de agregacao`);
  ok(!!registry['sel-' + pfx + '-kind'], `${pfx}: tem seletor de tipo de grafico`);
  ok(!!registry['btn-' + pfx + '-expand'], `${pfx}: tem Expandir Tudo`);
  const corpoF = registry[pfx + '-tree-body'];
  ok(corpoF && corpoF.children.length > 0, `${pfx}: a tabela renderizou`,
     corpoF && corpoF.children.length);
});

// Aditividade da arvore, lida da propria tabela. Na fonte o residuo e 0,000 exato --
// aqui a unica folga e o arredondamento de exibicao (1 casa em USD Bi).
{
  const corpoCC = registry['cc-tree-body'];
  function valoresCC(chave) {
    const linha = corpoCC.children.find(tr => tr.dataset.key === chave);
    if (!linha) return null;
    return linha.children.slice(2).map(td =>
      td.textContent === '—' ? null : parseFloat(td.textContent.replace(',', '.')));
  }
  function somaCC(msg, pai, filhos) {
    const p = valoresCC(pai), fs = filhos.map(valoresCC);
    if (!p || fs.some(f => !f)) { ok(false, msg, 'linha nao encontrada'); return; }
    let pior = 0, n = 0;
    for (let i = 0; i < 12; i++) {
      if (p[i] == null || fs.some(f => f[i] == null)) continue;
      pior = Math.max(pior, Math.abs(p[i] - fs.reduce((a, f) => a + f[i], 0)));
      n++;
    }
    ok(n >= 10 && pior <= 0.05 * (filhos.length + 1) + 1e-9, msg,
       `n=${n} pior=${pior.toFixed(3)}`);
  }
  registry['btn-cc-expand'].click();
  somaCC('Saldo Total = Comercial + Financeiro', 'cc_total', ['cc_comercial', 'cc_financeiro']);
  somaCC('Comercial = Exportacao + Importacao(negada)', 'cc_comercial', ['cc_export', 'cc_import']);
  somaCC('Exportacao = ACC + PA + Demais', 'cc_export',
         ['cc_export_acc', 'cc_export_pa', 'cc_export_outros']);
  somaCC('Financeiro = Compras + Vendas(negadas)', 'cc_financeiro',
         ['cc_fin_compras', 'cc_fin_vendas']);

  // O saldo tem de trocar de sinal -- e o que a serie antiga nao fazia, e o teste
  // mais direto de que a fonte certa esta ligada.
  const saldo = (REPORT_DATA.cambio_contratado.cc_saldo_total || []).filter(v => v != null);
  const trocas = saldo.slice(1).filter((v, i) => (v >= 0) !== (saldo[i] >= 0)).length;
  ok(trocas > 50, 'o saldo contratado troca de sinal ao longo da serie (a antiga nunca trocava)',
     `${trocas} trocas em ${saldo.length} meses`);
  ok(Math.max.apply(null, saldo.map(Math.abs)) > 5,
     'e tem magnitude de USD bilhoes, nao de dezenas de USD milhoes',
     Math.max.apply(null, saldo.map(Math.abs)).toFixed(1));
}

console.log('\n=== 11. a aba Mapa de Calor foi removida ====================');
// Removida a pedido do usuario em 2026-08-27. O que vale testar e a limpeza, nao a
// ausencia do botao: um painel morto que continua sendo plotado nao aparece em lugar
// nenhum da UI e so se descobre pelo custo. As 3 arvores CONTINUAM, porque nunca
// foram do mapa de calor -- sao a declaracao em pedacos de BOP_TREE_FULL.
const aindaPlota = newPlotCalls.concat(reactCalls).filter(c => String(c.div).indexOf('heatmap') >= 0);
ok(aindaPlota.length === 0, 'nenhum painel de mapa de calor e plotado',
   aindaPlota.map(c => c.div).join(', '));
ok(htmlBruto.indexOf('tab-heatmap') < 0 && htmlBruto.indexOf('chart-heatmap') < 0,
   'os ids da aba sairam do HTML');
ok(htmlBruto.indexOf('heatmap-btn') < 0 && htmlBruto.indexOf('heatmap-legend') < 0,
   'e o CSS dos controles dela tambem');
ok(typeof rollingZScore === 'undefined' && typeof renderHeatmapPanel === 'undefined',
   'as funcoes que so ela usava sairam do script');
ok(BOP_TREE_FULL.length === BOP_TREE_CURRENT.length + BOP_TREE_FINANCIAL.length + BOP_TREE_CAPITAL.length,
   'as 3 raizes seguem sendo a arvore do BP, concatenada na ordem do BPM6');

console.log('\n=== 12. cartoes de definicao nas linhas ======================');
// Rotulo curto na linha; nome oficial da fonte, explicacao e unidade no cartao
// (padrao de analytics/brasil/labor_market). O que estas assercoes protegem nao e
// a aparencia -- posicao e hover so sao verificaveis num browser -- e sim as tres
// regras que fazem o padrao valer a pena: cartao so onde ha o que dizer, `full` que
// nunca repete o rotulo de volta, e unidade que acompanha os seletores em vez de
// ser uma string fixa que passa a mentir no primeiro clique.
function celulaRotulo(tr) { return tr.children[1]; }
function botaoInfo(tr) {
  return celulaRotulo(tr).children.find(c => c.classList && c.classList.contains('info-btn')) || null;
}
{
  // 12a. cobertura: linha com entrada tem botao, linha sem entrada nao tem
  registry['btn-bop-expand'].click();
  const linhas = corpo.children;
  const semBotao = linhas.filter(tr => infoOf({ key: tr.dataset.key }) && !botaoInfo(tr));
  ok(semBotao.length === 0, 'toda linha do BP com definicao tem botao "i"',
     semBotao.map(tr => tr.dataset.key).join(', '));
  const botaoAtoa = linhas.filter(tr => !infoOf({ key: tr.dataset.key }) && botaoInfo(tr));
  ok(botaoAtoa.length === 0, 'nenhuma linha sem definicao ganhou botao (o cartao nunca abre vazio)',
     botaoAtoa.map(tr => tr.dataset.key).join(', '));
  ok(linhas.every(tr => botaoInfo(tr)), 'na arvore do BP todas as linhas tem cartao',
     linhas.filter(tr => !botaoInfo(tr)).map(tr => tr.dataset.key).join(', '));

  // 12b. o botao vai DEPOIS do texto -- as duas colunas invisiveis (toggle, cor)
  // continuam sendo os dois primeiros filhos, senao o alinhamento da secao 7d cai
  const ordemOk = linhas.every(tr => {
    const f = celulaRotulo(tr).children;
    const iTexto = f.findIndex(c => c.nodeType === 3);
    const iBtn = f.findIndex(c => c.classList && c.classList.contains('info-btn'));
    return f[0].classList.contains('tree-toggle') && f[1].classList.contains('swatch-dot') &&
           iTexto >= 0 && iBtn > iTexto;
  });
  ok(ordemOk, 'o botao vem depois do rotulo (toggle, cor, texto, "i")');

  // 12c. `full` nunca repete o rotulo exibido
  const todasArvores = [BOP_TREE_FULL, COMEX_PAIS_TREE, COMEX_FATOR_TREE, COMEX_PRODUTO_TREE,
                        CC_TREE, CC_DET_TREE, IB_TREE, RES_TREE, INTERV_TREE, SWAP_TREE,
                        COT_ROWS];
  const nos = [];
  todasArvores.forEach(t => (function walk(l) {
    (l || []).forEach(n => { nos.push(n); walk(n.children); });
  })(t));
  const fullRedundante = nos.filter(n => { const i = infoOf(n); return i && i.full === n.label; });
  ok(fullRedundante.length === 0, 'nenhum `full` repete o rotulo da propria linha',
     fullRedundante.map(n => n.key).join(', '));
  const semNada = nos.filter(n => { const i = infoOf(n); return i && !i.desc; });
  ok(semNada.length === 0, 'todo cartao tem explicacao, nao so o nome oficial',
     semNada.map(n => n.key).join(', '));

  // 12d. nenhuma entrada orfa: renomear uma chave de no tem de quebrar aqui, nao
  // virar um cartao que nunca aparece
  const chavesVivas = new Set(nos.map(n => n.key));
  const orfas = Object.keys(NODE_INFO).filter(k => !chavesVivas.has(k));
  ok(orfas.length === 0, 'nenhuma entrada de NODE_INFO aponta para chave que nao existe mais',
     orfas.join(', '));

  // 12e. o conteudo do cartao: abre com o rotulo, traz full/desc e a unidade
  registry['sel-bop-period'].value = 'monthly'; registry['sel-bop-period'].change();
  registry['sel-bop-mode'].value = 'abs'; registry['sel-bop-mode'].change();
  const trCC = corpo.children.find(tr => tr.dataset.key === 'conta_corrente');
  botaoInfo(trCC).fire('mouseenter');
  const cartao = _infoPop.innerHTML;
  ok(cartao.indexOf('<h4>Conta Corrente</h4>') >= 0, 'o cartao abre com o rotulo da linha');
  ok(cartao.indexOf('Transações correntes — saldo') > 0, 'traz o nome oficial da fonte');
  ok(cartao.indexOf('info-desc') > 0 && cartao.indexOf('sem criar nem quitar dívida') > 0,
     'traz a explicacao');
  ok(/Unidade: fluxo no mês, USD bilhões/.test(cartao), 'traz a unidade corrente', cartao.slice(-90));

  // 12f. a unidade acompanha os seletores -- e a regra que impede o cartao de
  // mentir: o mesmo par (unidade, janela) que o eixo Y e o cabecalho mostram
  registry['sel-bop-mode'].value = 'pct'; registry['sel-bop-mode'].change();
  registry['sel-bop-period'].value = 'annual'; registry['sel-bop-period'].change();
  corpo.children.find(tr => tr.dataset.key === 'conta_corrente').children[1]
       .children.find(c => c.classList && c.classList.contains('info-btn')).fire('mouseenter');
  ok(/Unidade: fluxo no ano, % do PIB/.test(_infoPop.innerHTML),
     'trocar Unidade e Agregacao muda a linha de unidade do cartao',
     _infoPop.innerHTML.slice(-90));
  registry['sel-bop-mode'].value = 'abs'; registry['sel-bop-mode'].change();
  registry['sel-bop-period'].value = 'monthly'; registry['sel-bop-period'].change();

  // 12g. o interbancario e VOLUME, nao fluxo -- chamar de fluxo sugeriria direcao
  // onde nao ha nenhuma (todo negocio interbancario tem comprador e vendedor)
  const trIB = registry['ib-tree-body'].children.find(tr => tr.dataset.key === 'ib_total');
  botaoInfo(trIB).fire('mouseenter');
  ok(/Unidade: volume negociado no mês, USD bilhões/.test(_infoPop.innerHTML),
     'o cartao do interbancario diz volume negociado, nao fluxo', _infoPop.innerHTML.slice(-90));
  ok(_infoPop.innerHTML.indexOf('nunca diz se entrou ou saiu dólar') > 0,
     'e o texto avisa que volume nao e direcao');

  // 12h. um unico .info-pop no documento, por mais botoes que se abra
  const pops = document.body.children.filter(c => c.classList && c.classList.contains('info-pop'));
  ok(pops.length === 1, 'existe um unico cartao no body, reposicionado a cada abertura', pops.length);

  // 12i. Comex: o cartao da raiz avisa que a regua NAO e a do BPM6, que e a
  // pergunta que a aba inteira provoca ao mostrar dois saldos de bens diferentes
  const trComex = registry['comex-pais-body'].children[0];
  botaoInfo(trComex).fire('mouseenter');
  ok(_infoPop.innerHTML.indexOf('NÃO é o do Balanço de Pagamentos') > 0,
     'o cartao do Comex avisa que o criterio difere do BPM6');
  const trImp = registry['comex-pais-body'].children.find(tr => /_m$/.test(tr.dataset.key || ''));
  ok(trImp && botaoInfo(trImp), 'as linhas de importacao do Comex tambem tem cartao');
  botaoInfo(trImp).fire('mouseenter');
  ok(_infoPop.innerHTML.indexOf('NEGADA') > 0,
     'e o cartao explica que a importacao aparece negada para somar ao saldo do pai');

  // 12j. o nome de classe e exclusivo desta metade do relatorio. Este arquivo
  // hospeda dois design systems (a fusao do ex-dashboard PPP em 2026-08), e ja
  // custou uma rodada de depuracao quando `table.data-table` do lado de modelo
  // capturou as celulas da aba BP. Antes de trazer um componente de outro
  // relatorio para ca, grep o nome da classe -- este teste e esse grep.
  {
    const css = htmlBruto.slice(htmlBruto.indexOf('<style>'), htmlBruto.indexOf('</style>'))
                         .replace(/\/\*[\s\S]*?\*\//g, '');
    ['info-btn', 'info-pop'].forEach(cls => {
      const emPppScope = css.split('\n').filter(l => l.indexOf(cls) >= 0 && l.indexOf('.ppp-scope') >= 0);
      ok(emPppScope.length === 0, `.${cls} nao existe tambem do lado de modelo`, emPppScope.join(' | '));
    });
  }

  registry['btn-bop-collapse'].click();
}


console.log('\n=== 13. aba Posicionamento: BCB e mercado ===================');
// A aba ganhou duas arvores em 2026-08-27. A que importa testar e a de RESERVAS,
// porque ela e a primeira do relatorio a agregar ESTOQUE: toda a maquinaria da
// fabrica foi escrita para fluxo, e somar tres meses de reservas devolveria ~1.100
// USD Bi sem lancar excecao nenhuma. As assercoes abaixo afirmam sobre o NUMERO que
// sai do agregador, nao sobre a existencia da opcao no <select>.
{
  const resv = REPORT_DATA.bcb_positioning.reservas_arvore;
  const intv = REPORT_DATA.bcb_positioning.intervencoes;

  // 13a. o payload chegou, e a arvore comeca onde a decomposicao comeca
  ok(resv && resv.dates && resv.dates.length > 250,
     'a arvore de reservas chegou com historia mensal', resv && resv.dates && resv.dates.length);
  ok(resv.dates[0].slice(0, 7) === '2001-01',
     'e comeca em jan/2001, onde a abertura por componente existe', resv.dates[0]);
  ok(intv && intv.dates && intv.dates.length > 300,
     'a serie de intervencoes chegou somada em meses', intv && intv.dates && intv.dates.length);

  // 13b. aditividade do template do FMI, mes a mes. O limite e 0,011 USD Bi: a
  // fonte publica em USD milhoes e o pior residuo medido em 307 meses e 0,010.
  let piorFx = 0, piorOut = 0, piorTot = 0, n = 0;
  for (let i = 0; i < resv.dates.length; i++) {
    const g = (k) => resv[k] == null ? null : resv[k][i];
    const fx = g('reserves_fx_total'), sec = g('reserves_fx_securities'), dep = g('reserves_fx_currency_deposits');
    if (fx != null && sec != null && dep != null) piorFx = Math.max(piorFx, Math.abs(fx - (sec + dep)));
    const ot = g('reserves_other_total'), rr = g('reserves_other_reverse_repo'),
          lo = g('reserves_other_loans'), de = g('reserves_other_derivatives');
    if (ot != null && rr != null && lo != null && de != null) piorOut = Math.max(piorOut, Math.abs(ot - (rr + lo + de)));
    const tt = g('reserves_total_monthly'), sd = g('reserves_sdrs'),
          im = g('reserves_imf_position'), ou = g('reserves_gold_usd');
    if (tt != null && fx != null && ot != null && sd != null && im != null && ou != null) {
      piorTot = Math.max(piorTot, Math.abs(tt - (fx + ou + sd + im + ot)));
      n++;
    }
  }
  ok(n > 250, 'ha meses suficientes com a arvore inteira preenchida', n);
  ok(piorFx < 0.011, 'titulos + moeda e depositos = moeda estrangeira', piorFx.toFixed(4));
  ok(piorOut < 0.011, 'compromissadas + emprestimos + derivativos = outros ativos', piorOut.toFixed(4));
  ok(piorTot < 0.011, 'os 5 componentes somam o total de reservas', piorTot.toFixed(4));

  // 13c. intervencoes: os 4 instrumentos somam o total, em todo mes
  let piorInt = 0;
  for (let i = 0; i < intv.dates.length; i++) {
    const soma = ['bcb_intervention_spot', 'bcb_intervention_forwards',
                  'bcb_intervention_fx_loans_repos', 'bcb_intervention_repo_lines']
                 .reduce((a, k) => a + (intv[k][i] || 0), 0);
    piorInt = Math.max(piorInt, Math.abs(intv.bcb_intervention_total[i] - soma));
  }
  ok(piorInt < 1e-9, 'os 4 instrumentos somam a intervencao liquida total', piorInt);

  // 13d. dia ausente e ZERO, nao lacuna -- e o que faz 2013-2018 aparecer zerado
  // em vez de em branco. Se o payload propagasse null, o grafico abriria um buraco
  // de seis anos e o leitor entenderia "sem dado" onde o certo e "nao interveio".
  const semDado = intv.dates.filter((d, i) => intv.bcb_intervention_total[i] == null);
  ok(semDado.length === 0, 'nenhum mes de intervencao vem nulo', semDado.slice(0, 3).join(', '));
  const janela1418 = intv.dates
    .map((d, i) => ({ d, v: intv.bcb_intervention_spot[i] }))
    .filter(o => o.d >= '2014-01' && o.d < '2018-01');
  ok(janela1418.length === 48 && janela1418.every(o => o.v === 0),
     'o periodo sem intervencao a vista vem zerado, e nao em branco',
     janela1418.filter(o => o.v !== 0).length + ' meses nao-zero de ' + janela1418.length);

  // 13e. ESTOQUE agrega por fim de periodo. O teste que pega o erro que interessa:
  // o valor trimestral tem de ser o do ULTIMO MES do trimestre, e nao a soma dos
  // tres -- que aqui seria ~3x maior e continuaria "plausivel" para quem so olha a
  // ordem de grandeza do grafico.
  const oTotal = (divId) => ultimoReact(divId).traces.find(t => t.name === 'Reservas Internacionais');
  registry['sel-resv-period'].value = 'monthly'; registry['sel-resv-period'].change();
  const mensal = oTotal('chart-resv-tree');
  registry['sel-resv-period'].value = 'quarterly'; registry['sel-resv-period'].change();
  const trim = oTotal('chart-resv-tree');

  const porData = {};
  mensal.x.forEach((d, i) => { porData[String(d).slice(0, 7)] = mensal.y[i]; });
  let batemFim = 0, comoSoma = 0, comparados = 0;
  trim.x.forEach((d, i) => {
    if (trim.y[i] == null) return;
    // bucketStartDate rotula o trimestre pelo mes FINAL (mar/jun/set/dez)
    const ano = String(d).slice(0, 4), mes = Number(String(d).slice(5, 7));
    const fim = ano + '-' + String(mes).padStart(2, '0');
    if (!(fim in porData) || porData[fim] == null) return;
    comparados++;
    if (Math.abs(trim.y[i] - porData[fim]) < 1e-6) batemFim++;
    const soma = [mes - 2, mes - 1, mes]
      .map(m => porData[ano + '-' + String(m).padStart(2, '0')])
      .reduce((a, v) => a + (v || 0), 0);
    if (Math.abs(trim.y[i] - soma) < 1e-6) comoSoma++;
  });
  ok(comparados > 90, 'ha trimestres suficientes para comparar', comparados);
  ok(batemFim === comparados, 'o trimestre de um estoque e o valor do ULTIMO mes dele',
     (comparados - batemFim) + ' de ' + comparados + ' divergem');
  ok(comoSoma === 0, 'e nunca a soma dos tres meses (seria ~3x o estoque real)', comoSoma);

  // 13f. bucket incompleto continua em branco: um ano rotulado "2026" com o valor
  // de julho leria como fim de ano e nao e.
  registry['sel-resv-period'].value = 'annual'; registry['sel-resv-period'].change();
  const anual = oTotal('chart-resv-tree');
  const ultimoAnoComValor = anual.x.filter((d, i) => anual.y[i] != null).slice(-1)[0];
  ok(String(ultimoAnoComValor).slice(0, 4) === '2025',
     'o ano em curso sai em branco porque ainda nao tem fim', String(ultimoAnoComValor));

  // 13g. "% do PIB" de estoque usa o PIB de 12 MESES, nao o do bucket. Dividir
  // reservas pelo PIB de um mes daria ~1.700% e a escala mudaria a cada clique no
  // seletor de agregacao -- o numero certo fica na casa de 15-20% do PIB.
  registry['sel-resv-period'].value = 'monthly'; registry['sel-resv-period'].change();
  registry['sel-resv-mode'].value = 'pct'; registry['sel-resv-mode'].change();
  const pctM = oTotal('chart-resv-tree');
  const ultPctM = pctM.y.filter(v => v != null).slice(-1)[0];
  ok(ultPctM > 8 && ultPctM < 35, 'reservas em % do PIB ficam em faixa plausivel',
     ultPctM && ultPctM.toFixed(2));
  registry['sel-resv-period'].value = 'quarterly'; registry['sel-resv-period'].change();
  const pctT = oTotal('chart-resv-tree');
  const ultPctT = pctT.y.filter(v => v != null).slice(-1)[0];
  ok(Math.abs(ultPctT - ultPctM) < 3,
     'e nao mudam de escala ao trocar a agregacao (o denominador segue sendo 12m)',
     ultPctM.toFixed(2) + ' -> ' + ultPctT.toFixed(2));
  registry['sel-resv-mode'].value = 'abs'; registry['sel-resv-mode'].change();
  registry['sel-resv-period'].value = 'monthly'; registry['sel-resv-period'].change();

  // 13h. a linha de unidade do cartao acompanha o seletor, e diz FIM de periodo
  {
    const corpoResv = registry['resv-tree-body'];
    const trTotal = corpoResv.children.find(tr => tr.dataset.key === 'res_total');
    const btn = trTotal.children[1].children.find(c => c.classList && c.classList.contains('info-btn'));
    btn.fire('mouseenter');
    ok(_infoPop.innerHTML.indexOf('estoque no fim do mês') > 0,
       'o cartao de reserva diz estoque, e no FIM do mes', _infoPop.innerHTML.slice(-140));
    hideInfo();
    registry['sel-resv-period'].value = 'annual'; registry['sel-resv-period'].change();
    corpoResv.children.find(tr => tr.dataset.key === 'res_total')
             .children[1].children.find(c => c.classList && c.classList.contains('info-btn')).fire('mouseenter');
    ok(_infoPop.innerHTML.indexOf('no fim do ano') > 0,
       'e acompanha a agregacao escolhida', _infoPop.innerHTML.slice(-140));
    hideInfo();
    registry['sel-resv-period'].value = 'monthly'; registry['sel-resv-period'].change();
  }

  // 13i. o pedido literal do usuario: barra empilhada no grafico de intervencoes.
  // O total marcado junto com os componentes vira LINHA, senao a pilha seria contada
  // duas vezes -- e a mesma regra das outras arvores, verificada aqui de novo porque
  // esta e a unica arvore em que o total e derivado no Python, nao lido da fonte.
  const rInt = ultimoReact('chart-intv-tree');
  ok(rInt.layout.barmode === 'relative', 'o grafico de intervencoes empilha barras',
     rInt.layout.barmode);
  ok(rInt.traces.filter(t => t.type === 'bar').length === 4,
     'os 4 instrumentos entram como barra', rInt.traces.filter(t => t.type === 'bar').length);
  const totalTrace = rInt.traces.find(t => t.name.indexOf('Total') >= 0);
  ok(totalTrace && totalTrace.type === 'scatter',
     'e o total marcado junto vira linha por cima da pilha', totalTrace && totalTrace.type);

  // 13j. os dois graficos retirados nao voltaram por acidente
  ok(!('chart-bcb-gold' in cardOf) && htmlBruto.indexOf('chart-bcb-gold') < 0,
     'o grafico solto de Reservas em Ouro saiu (virou a linha res_gold da arvore)');
  ok(!('chart-bcb-intervention' in cardOf) && htmlBruto.indexOf('chart-bcb-intervention') < 0,
     'e o de intervencao diaria saiu (virou a arvore mensal)');

  // 13l. a secao de Posicao Cambial ganhou tabela PLANA (2026-08-27, pedido do
  // usuario). O ponto de testar: uma tabela sem hierarquia so vale a pena se
  // entregar o resto do pacote -- celula mes a mes, caixa que plota e cartao de
  // definicao -- sem arrastar junto o que so faz sentido numa arvore.
  const corpoSwap = registry['swap-tree-body'];
  ok(corpoSwap.children.length === 4, 'a tabela de posicao cambial tem as 4 linhas',
     corpoSwap.children.length);
  ok(corpoSwap.children.every(tr => botaoInfo(tr)),
     'e todas as 4 tem cartao de definicao',
     corpoSwap.children.filter(tr => !botaoInfo(tr)).map(tr => tr.dataset.key).join(', '));
  ok(corpoSwap.children.every(tr => celulaRotulo(tr).style.paddingLeft === '14px'),
     'nenhuma linha vem recuada: sem hierarquia nao ha nivel para sinalizar');
  ok(corpoSwap.children.every(tr => celulaRotulo(tr).children[0].classList.contains('is-empty')),
     'e nenhuma linha tem seta de expandir');

  // 13m. abre em LINHAS, e nao ha seletor de tipo -- empilhar as quatro somaria
  // exposicoes de duas entidades diferentes num total que a fonte nao publica.
  const rSwap = ultimoReact('chart-bcb-swap');
  ok(rSwap.traces.length === 4 && rSwap.traces.every(t => t.type === 'scatter'),
     'o grafico de posicao cambial abre com as 4 series em linha',
     rSwap.traces.map(t => t.type).join(', '));
  ok(!('sel-swap-kind' in registry),
     'a secao nao oferece barras empilhadas (seria um agregado inventado)');
  ok(!('btn-swap-expand' in registry) && !('btn-swap-collapse' in registry),
     'nem os botoes de expandir/recolher, que numa tabela plana nao fazem nada');

  // 13n. posicao tambem e estoque: fim de periodo, nao soma
  registry['sel-swap-period'].value = 'monthly'; registry['sel-swap-period'].change();
  const swapM = ultimoReact('chart-bcb-swap').traces.find(t => t.name.indexOf('Swap') >= 0);
  const porMes = {};
  swapM.x.forEach((d, i) => { porMes[String(d).slice(0, 7)] = swapM.y[i]; });
  registry['sel-swap-period'].value = 'quarterly'; registry['sel-swap-period'].change();
  const swapT = ultimoReact('chart-bcb-swap').traces.find(t => t.name.indexOf('Swap') >= 0);
  let batem = 0, comparados2 = 0;
  swapT.x.forEach((d, i) => {
    if (swapT.y[i] == null) return;
    const fim = String(d).slice(0, 7);
    if (!(fim in porMes) || porMes[fim] == null) return;
    comparados2++;
    if (Math.abs(swapT.y[i] - porMes[fim]) < 1e-6) batem++;
  });
  ok(comparados2 > 50 && batem === comparados2,
     'o trimestre da posicao e o valor do ultimo mes, nao a soma dos tres',
     (comparados2 - batem) + ' de ' + comparados2 + ' divergem');
  registry['sel-swap-period'].value = 'monthly'; registry['sel-swap-period'].change();

  // 13o. "% do PIB" continua com denominador de 12 meses (posicao e estoque)
  registry['sel-swap-mode'].value = 'pct'; registry['sel-swap-mode'].change();
  const swapPct = ultimoReact('chart-bcb-swap').traces.find(t => t.name.indexOf('Swap') >= 0);
  const ultSwapPct = swapPct.y.filter(v => v != null).slice(-1)[0];
  ok(ultSwapPct < 0 && ultSwapPct > -15, 'o swap em % do PIB fica em faixa plausivel e negativa',
     ultSwapPct && ultSwapPct.toFixed(2));
  registry['sel-swap-mode'].value = 'abs'; registry['sel-swap-mode'].change();

  // 13p. o cartao diz "posicao", nao "fluxo" -- estas linhas sao saldo em aberto,
  // e chama-las de fluxo sugeriria movimento onde ha estoque.
  botaoInfo(corpoSwap.children.find(tr => tr.dataset.key === 'swp_bancos')).fire('mouseenter');
  ok(_infoPop.innerHTML.indexOf('Unidade: posição no fim do mês') > 0,
     'o cartao da posicao cambial diz posicao, e no fim do mes', _infoPop.innerHTML.slice(-120));
  ok(_infoPop.innerHTML.indexOf('outra ponta') > 0,
     'e explica por que a linha dos bancos mora no mesmo grafico do swap do BCB');
  hideInfo();

  // 13k. a aba e a terceira do nav
  const abas = (htmlBruto.match(/data-tab="tab-[\w-]+"/g) || []).map(m => m.slice(10, -1));
  ok(abas[2] === 'tab-bcb', 'Posicionamento: BCB e mercado e a terceira aba', abas.slice(0, 4).join(', '));
}

console.log('\n=== 14. reorganizacao das abas (2026-09-01) =================');
// A aba Cotacao foi apagada e os seus dois vizinhos redistribuidos, a pedido do
// usuario: o PTAX foi para Valuation (e o nivel contra o qual as outras tres secoes
// da aba sao lidas) e o posicionamento especulativo da CFTC saiu de Valuation para a
// aba do BCB, que passou a se chamar "Posicionamento: BCB e mercado" justamente
// porque agora carrega as duas pontas.
//
// A assercao que importa aqui e a de PERTENCIMENTO. Um grafico que continua
// existindo, continua sendo desenhado e continua passando em todo o resto deste
// arquivo pode ter ficado no painel errado sem levantar erro nenhum -- ele so nunca
// aparece onde o leitor foi procura-lo. E a mesma classe do bug de aba que nenhum
// teste de configuracao pega: o objeto esta certo, o lugar e que nao.
{
  const abas14 = (htmlBruto.match(/data-tab="tab-[\w-]+"/g) || []).map(m => m.slice(10, -1));

  // Fatia o HTML nos limites dos paineis para responder "que aba hospeda este div?".
  const limites = [...htmlBruto.matchAll(/<div class="tab-panel[^"]*" id="([\w-]+)">/g)]
    .map(m => ({ id: m[1], i: m.index }));
  function abaDe(divId) {
    const k = htmlBruto.indexOf('id="' + divId + '"');
    if (k < 0) return null;
    let atual = null;
    limites.forEach(l => { if (l.i < k) atual = l.id; });
    return atual;
  }

  // 14a. a aba Cotacao nao existe mais, em nenhuma das tres formas em que existia
  ok(abas14.indexOf('tab-quotation') < 0, 'a aba Cotacao saiu do nav', abas14.join(', '));
  ok(htmlBruto.indexOf('id="tab-quotation"') < 0, 'e o painel dela saiu do HTML');
  ok(htmlBruto.indexOf('sec-quotation-ptax') < 0, 'e a secao antiga do PTAX nao ficou orfa');

  // 14b. todo botao aponta para um painel que existe, e vice-versa. E o que pega um
  // painel esquecido sem botao (invisivel para sempre) ou um botao sem painel (clique
  // que nao mostra nada) -- os dois modos de falha de mexer no nav.
  const idsPaineis = tabPanels.map(p => p.id);
  const semPainel = abas14.filter(a => idsPaineis.indexOf(a) < 0);
  const semBotao  = idsPaineis.filter(i => abas14.indexOf(i) < 0);
  ok(semPainel.length === 0 && semBotao.length === 0,
     'nenhum botao sem painel e nenhum painel sem botao',
     'sem painel: ' + semPainel.join(', ') + ' / sem botao: ' + semBotao.join(', '));
  ok(abas14.length === 7, 'sobraram 7 abas', abas14.join(', '));

  // 14c. o rotulo da aba anuncia as duas pontas
  ok(htmlBruto.indexOf('data-tab="tab-bcb">Posicionamento: BCB e mercado<') > 0,
     'a aba do BCB se chama "Posicionamento: BCB e mercado"');

  // 14d. onde cada grafico foi parar -- os dois que mudaram...
  ok(abaDe('chart-cot-brl') === 'tab-bcb',
     'o posicionamento especulativo mora na aba do BCB', abaDe('chart-cot-brl'));
  ok(abaDe('chart-ptax') === 'tab-valuation',
     'o PTAX mora na aba Valuation', abaDe('chart-ptax'));
  // ...e os que nao mudaram, para a mudanca nao ter arrastado vizinho junto
  ['chart-reer', 'chart-termos'].forEach(id => {
    ok(abaDe(id) === 'tab-valuation', 'segue em Valuation: ' + id, abaDe(id));
  });
  ['chart-resv-tree', 'chart-bcb-swap', 'chart-intv-tree'].forEach(id => {
    ok(abaDe(id) === 'tab-bcb', 'segue na aba do BCB: ' + id, abaDe(id));
  });

  // 14e. o PTAX ABRE a aba Valuation: e o preco que as outras tres secoes qualificam
  const painelVal = htmlBruto.slice(htmlBruto.indexOf('id="tab-valuation"'));
  ok(painelVal.indexOf('chart-ptax') < painelVal.indexOf('chart-reer') &&
     painelVal.indexOf('chart-reer') < painelVal.indexOf('chart-termos'),
     'a ordem em Valuation e PTAX -> cambio real -> termos de troca');

  // 14f. e o especulativo entra DEPOIS das tres secoes do BCB -- e a ordem que o
  // nome da aba promete ("BCB e mercado", nessa ordem)
  const painelBcb = htmlBruto.slice(htmlBruto.indexOf('id="tab-bcb"'));
  ok(painelBcb.indexOf('chart-intv-tree') < painelBcb.indexOf('chart-cot-brl'),
     'na aba do BCB o mercado vem depois do BCB');

  // 14g. os dois graficos movidos mantiveram o cabecalho. Eles vieram de painel E o
  // bloco de JS que os desenha foi movido junto: e a combinacao em que um
  // finishChart deixado para tras passa despercebido.
  ['chart-ptax', 'chart-cot-brl'].forEach(id => {
    ok(cardOf[id] && cabecalho(id) && cabecalho(id).indexOf('Fonte:') > 0,
       'o grafico movido manteve o cabecalho: ' + id, cabecalho(id));
  });

  // 14h. a nota do especulativo tem de dizer QUAL sinal e qual aposta. A anterior
  // falava de "net comprado em USD (vendido em BRL)" sem dizer o que a barra positiva
  // significa -- lida do lado errado, ela inverte a leitura do grafico inteiro, que e
  // o unico erro possivel aqui que nao tem tell visual.
  const iCot = htmlBruto.indexOf('id="sec-bcb-cot"');
  const secCot = htmlBruto.slice(iCot, htmlBruto.indexOf('</section>', iCot));
  ok(secCot.indexOf('positivo = comprado em real') > 0,
     'a nota diz que positivo = comprado em real');
  ok(/open interest/i.test(secCot),
     'e explica o que o eixo da direita acrescenta');
  ok(secCot.indexOf('exposição do <strong>BCB</strong>') > 0 &&
     secCot.indexOf('do <strong>mercado</strong>') > 0,
     'e diz de quem e a posicao, ja que a aba agora hospeda duas pontas');
}

console.log('\n=== 15. Diferenciais de Juros removidos (2026-09-01) ========');
// Pedido do usuario: apagar os tres graficos da secao (Taxas Basicas, Diferencial
// Nominal, Juros Reais ex-post). Removida a secao inteira, os tres CHART_META, os
// tres IIFEs e a chave `diferenciais` do payload.
//
// Sao tres modos de sobra que nao levantam erro nenhum, e cada um deixa um rastro
// diferente -- e por isso que o teste afirma sobre os quatro artefatos, e nao so
// sobre o div: um CHART_META orfao vive para sempre em silencio, um IIFE orfao faz
// um Plotly.newPlot num id inexistente, e 39 KB de payload morto so aparecem na
// balanca do arquivo.
{
  const IDS = ['chart-nominal-rates', 'chart-diferencial-nominal', 'chart-taxas-reais'];

  // 15a. nem div, nem secao no HTML
  IDS.forEach(id => {
    ok(htmlBruto.indexOf('id="' + id + '"') < 0, 'o div sumiu do HTML: ' + id);
  });
  ok(htmlBruto.indexOf('sec-valuation-juros') < 0, 'e a secao que os abrigava tambem');

  // 15b. nenhum Plotly.newPlot/react apontou para eles -- o rastro de um IIFE que
  // tivesse ficado para tras, desenhando num id que nao existe mais
  const desenhados = newPlotCalls.concat(reactCalls).map(c => c.div);
  IDS.forEach(id => {
    ok(desenhados.indexOf(id) < 0, 'nada tentou desenhar: ' + id);
  });

  // 15c. e nenhum CHART_META orfao ficou. Vale para os tres removidos E para o
  // mapa inteiro: uma entrada sem div e texto que nunca aparece na tela.
  const idsMeta = [...(scripts.join('\n').match(/'(chart-[\w-]+)':\s*\{\s*\n\s*title:/g) || [])]
    .map(m => m.slice(1, m.indexOf("'", 1)));
  const orfaos = idsMeta.filter(id => htmlBruto.indexOf('id="' + id + '"') < 0);
  // 8, e nao 15: as abas de arvore declaram title/source nas opcoes de
  // makeTreeChartTab(), nao aqui -- e la um div que sumisse quebraria a fabrica
  // em voz alta, que e o motivo de nao precisarem deste mapa.
  ok(idsMeta.length >= 7, 'o mapa CHART_META foi encontrado', idsMeta.length + ' entradas');
  ok(orfaos.length === 0, 'nenhuma entrada de CHART_META sem div correspondente',
     orfaos.join(', '));

  // 15d. o payload nao carrega mais `diferenciais` -- eram 39 KB para tres graficos
  // que nao existem mais. O loader continua no generate_report.py de proposito
  // (agent_data.py o importa), so nao entra mais AQUI.
  ok(!REPORT_DATA.diferenciais, 'a chave `diferenciais` saiu do payload',
     REPORT_DATA.diferenciais && Object.keys(REPORT_DATA.diferenciais).join(', '));

  // 15e. Valuation ficou com exatamente os 3 graficos que o usuario listou
  const iVal = htmlBruto.indexOf('id="tab-valuation"');
  const fimVal = htmlBruto.indexOf('<div class="tab-panel', iVal + 10);
  const noVal = chartDivIds.filter(id => {
    const k = htmlBruto.indexOf('id="' + id + '"');
    return k > iVal && k < fimVal;
  });
  ok(noVal.length === 3 && noVal.join(',') === 'chart-ptax,chart-reer,chart-termos',
     'Valuation tem so PTAX, cambio efetivo real e termos de troca', noVal.join(', '));
}

console.log('\n=== 16. posicionamento no futuro de real (CFTC) =============');
// A secao foi reconstruida em 2026-09-01: o grafico unico (uma serie de barras mais
// o open interest numa linha pontilhada de eixo secundario) virou tabela com caixa
// que plota, cinco categorias de participante em vez de uma, e media movel de 12 e
// 24 semanas.
{
  const corpoCot = registry['cot-tree-body'];
  const linhasCot = () => corpoCot.children;
  const caixaDe = (chave) => {
    const tr = linhasCot().find(x => x.dataset.key === chave);
    return tr && tr.children[0].children[0];
  };
  const marcar = (chave, v) => { const cb = caixaDe(chave); cb.checked = v; cb.fire('change'); };
  const D = REPORT_DATA.cot_fx;
  const CATS = ['cot_dealer', 'cot_asset', 'cot_lev', 'cot_other', 'cot_nonrept'];
  const SERIE = { cot_oi: 'open_interest', cot_dealer: 'dealer_net', cot_asset: 'asset_mgr_net',
                  cot_lev: 'lev_net', cot_other: 'other_net', cot_nonrept: 'nonrept_net' };

  // 16a. o payload tem as cinco categorias, e nao so os alavancados
  ok(!!D && !!D.dates, 'o payload do COT chegou');
  const faltando = Object.values(SERIE).filter(k => !Array.isArray(D[k]));
  ok(faltando.length === 0, 'as 5 categorias + o open interest estao no payload', faltando.join(', '));
  ok(D.dates.length > 700, 'a serie semanal veio inteira', D.dates.length + ' semanas');

  // 16b. AS DUAS IDENTIDADES DA FONTE, conferidas no ARQUIVO ENTREGUE e nao so no
  // banco. Sao elas que autorizam as duas leituras do grafico: sem a primeira,
  // empilhar os cinco liquidos seria juntar coisas que nao somam nada; sem a
  // segunda, "participacao no open interest" nao seria participacao em coisa
  // nenhuma. Uma perna trocada de sinal ou uma categoria esquecida no loader passam
  // por qualquer outro teste deste arquivo e morrem aqui.
  const PS = ['dealer', 'asset_mgr', 'lev', 'other', 'nonrept'];
  let piorNet = 0, piorLong = 0, piorShort = 0;
  for (let i = 0; i < D.dates.length; i++) {
    const soma = CATS.reduce((a, k) => a + (D[SERIE[k]][i] || 0), 0);
    piorNet = Math.max(piorNet, Math.abs(soma));
    // spread e comprado E vendido ao mesmo tempo: entra uma vez de cada lado
    const sp = PS.reduce((a, p) => a + ((D[p + '_spread'] || [])[i] || 0), 0);
    piorLong  = Math.max(piorLong,
      Math.abs(PS.reduce((a, p) => a + D[p + '_long'][i], 0)  + sp - D.open_interest[i]));
    piorShort = Math.max(piorShort,
      Math.abs(PS.reduce((a, p) => a + D[p + '_short'][i], 0) + sp - D.open_interest[i]));
  }
  ok(piorNet === 0, 'as 5 posicoes liquidas somam exatamente zero em toda semana', piorNet);
  ok(piorLong === 0 && piorShort === 0,
     'e (comprado + spread) das 5, dos DOIS lados, da o open interest',
     piorLong + ' / ' + piorShort);

  // ...e o open interest NAO e a soma dos liquidos: e o tamanho do mercado. Sao
  // duas quantidades diferentes, que e por que ele nao pode entrar na mesma pilha.
  const ultimo = D.dates.length - 1;
  const somaAbs = CATS.reduce((a, k) => a + Math.abs(D[SERIE[k]][ultimo]), 0);
  ok(D.open_interest[ultimo] > 0 && D.open_interest[ultimo] !== somaAbs,
     'o open interest nao e a soma dos liquidos', D.open_interest[ultimo]);

  // 16b2. os NUMEROS que a nota e os cartoes afirmam. Escrever "os alavancados sao
  // 28% do open interest, o dealer e 36%" e uma afirmacao sobre o dado, e ela
  // envelhece a cada divulgacao -- entao ou o teste a confere ou ela nao devia estar
  // escrita. A participacao inclui o spread, senao as cinco somam 91% e nao 100%.
  function participacao(p) {
    let acc = 0;
    for (let i = 0; i < D.dates.length; i++) {
      const sp = (D[p + '_spread'] || [])[i] || 0;
      acc += ((D[p + '_long'][i] + D[p + '_short'][i]) / 2 + sp) / D.open_interest[i];
    }
    return acc / D.dates.length * 100;
  }
  const share = {}; PS.forEach(p => { share[p] = participacao(p); });
  const somaShare = PS.reduce((a, p) => a + share[p], 0);
  ok(Math.abs(somaShare - 100) < 0.05, 'as 5 participacoes somam 100%', somaShare.toFixed(2));
  ok(Math.abs(share.dealer - 36) < 1, 'o dealer e ~36% do open interest, como a nota diz',
     share.dealer.toFixed(1));
  ok(Math.abs(share.lev - 28) < 1, 'e os alavancados ~28%, como a nota e o cartao dizem',
     share.lev.toFixed(1));
  ok(share.dealer > share.lev,
     'e o dealer e MAIOR que os alavancados -- a frase que motivou o pedido',
     share.dealer.toFixed(1) + ' vs ' + share.lev.toFixed(1));
  const secCotN = htmlBruto.slice(htmlBruto.indexOf('id="sec-bcb-cot"'),
                                  htmlBruto.indexOf('</section>', htmlBruto.indexOf('id="sec-bcb-cot"')));
  ok(secCotN.indexOf('28% do open interest') > 0 && secCotN.indexOf('36%') > 0,
     'e sao esses os numeros escritos na nota');

  // 16c. a tabela tem as 6 linhas, e o default marca as 5 categorias (a pergunta
  // "quem mais esta no mercado" tem de estar respondida ao abrir)
  ok(linhasCot().length === 6, 'a tabela tem 6 linhas', linhasCot().length);
  const marcadasIni = linhasCot().filter(tr => tr.children[0].children[0].checked).map(tr => tr.dataset.key);
  ok(marcadasIni.length === 5 && marcadasIni.indexOf('cot_oi') < 0,
     'abre com as 5 categorias marcadas e o open interest fora', marcadasIni.join(', '));

  // 16d. TODAS as series plotadas sao BARRAS (pedido explicito: o open interest era
  // uma linha pontilhada de eixo secundario e passou a ser barra como as outras)
  let r16 = ultimoReact('chart-cot-brl');
  ok(r16.traces.length === 5 && r16.traces.every(t => t.type === 'bar'),
     'o default plota 5 barras e nenhuma linha',
     r16.traces.map(t => t.type).join(', '));
  ok(!r16.layout.yaxis2, 'nao ha mais eixo Y secundario');
  ok((r16.layout.yaxis.title.text || '').indexOf('contratos') >= 0,
     'o eixo diz a unidade', r16.layout.yaxis.title.text);

  // 16e. marcar o open interest o poe em OUTRA pilha. Este e o unico jeito de ele
  // ser barra sem virar um agregado inventado -- somado a pilha dos liquidos, o topo
  // deixaria de significar coisa alguma.
  marcar('cot_oi', true);
  r16 = ultimoReact('chart-cot-brl');
  ok(r16.traces.length === 6 && r16.traces.every(t => t.type === 'bar'),
     'com o open interest marcado sao 6 barras', r16.traces.length);
  const grpOI = r16.traces.find(t => t.name.indexOf('Open Interest') === 0).offsetgroup;
  const grpsNet = r16.traces.filter(t => t.name.indexOf('Open Interest') !== 0)
                            .map(t => t.offsetgroup);
  ok(grpOI !== grpsNet[0], 'o open interest fica numa offsetgroup propria', grpOI + ' vs ' + grpsNet[0]);
  ok(new Set(grpsNet).size === 1, 'e as 5 categorias dividem a mesma pilha', [...new Set(grpsNet)].join(', '));
  marcar('cot_oi', false);

  // 16f. MEDIA MOVEL: entra como LINHA sobre as barras, uma por serie marcada
  registry['sel-cot-ma'].value = '12'; registry['sel-cot-ma'].change();
  r16 = ultimoReact('chart-cot-brl');
  const barras16 = r16.traces.filter(t => t.type === 'bar');
  const linhas16 = r16.traces.filter(t => t.type === 'scatter');
  ok(barras16.length === 5 && linhas16.length === 5,
     'com MM12 sao 5 barras + 5 linhas', barras16.length + ' / ' + linhas16.length);
  ok(linhas16.every(t => /MM12s$/.test(t.name)), 'as linhas sao as medias moveis',
     linhas16.map(t => t.name).join(', '));
  // as linhas vem DEPOIS das barras no array, senao ficariam por baixo da pilha
  ok(r16.traces.findIndex(t => t.type === 'scatter') > r16.traces.map(t => t.type).lastIndexOf('bar'),
     'as medias moveis sao desenhadas por cima das barras');
  ok((cabecalho('chart-cot-brl') || '').indexOf('12 semanas') > 0,
     'o cabecalho anuncia a media movel', cabecalho('chart-cot-brl'));

  // 16g. O VALOR da media movel, recalculado aqui, e a regra que a torna honesta.
  // "12 semanas" tem de ser 12 SEMANAS, nao 12 observacoes: a serie tem 16 buracos
  // maiores que uma semana ate 2015, um deles de 196 dias. Uma janela de 12 linhas
  // cobrindo oito meses continuaria produzindo um numero, e ele estaria rotulado
  // errado -- entao ela sai em branco.
  const lev = D.lev_net, dts = D.dates.map(x => Date.parse(String(x).replace(' ', 'T') + 'Z'));
  function mmEsperada(k) {
    const out = new Array(lev.length).fill(null);
    const limite = ((k - 1) * 7 + 10) * 86400000;
    for (let i = k - 1; i < lev.length; i++) {
      if (dts[i] - dts[i - k + 1] > limite) continue;
      let soma = 0, furo = false;
      for (let j = i - k + 1; j <= i; j++) {
        if (lev[j] == null || isNaN(lev[j])) { furo = true; break; }
        soma += lev[j];
      }
      if (!furo) out[i] = soma / k;
    }
    return out;
  }
  const esp12 = mmEsperada(12);
  const got12 = linhas16.find(t => t.name.indexOf('Fundos Alavancados') === 0).y;
  let dif = 0, comparados = 0, brancosOk = true;
  for (let i = 0; i < esp12.length; i++) {
    if (esp12[i] === null) { if (got12[i] !== null) brancosOk = false; continue; }
    comparados++;
    dif = Math.max(dif, Math.abs(got12[i] - esp12[i]));
  }
  ok(comparados > 600 && dif < 1e-9, 'a MM12 bate valor a valor com o recalculo',
     comparados + ' pontos, pior diferenca ' + dif);
  ok(brancosOk, 'e o que o guarda de span veta sai em branco, nao com um numero');

  // ...e o guarda tem de MORDER: se nao vetasse nada, ele nao estaria testado
  const vetados = esp12.filter((v, i) => v === null && i >= 11).length;
  ok(vetados > 20, 'o guarda de span veta pontos de verdade (os buracos ate 2015)', vetados);
  // ...mas so la atras: apagar a amostra moderna seria um custo real, e nao ha
  const ultimoVetado = D.dates[esp12.reduce((acc, v, i) => (v === null && i >= 11 ? i : acc), -1)];
  ok(String(ultimoVetado) < '2016', 'e nenhum ponto depois de 2015 e vetado', String(ultimoVetado).slice(0, 10));

  // 16h. MM24 existe e e mais curta que a MM12 (janela maior come mais pontas)
  registry['sel-cot-ma'].value = '24'; registry['sel-cot-ma'].change();
  const got24 = ultimoReact('chart-cot-brl').traces
    .find(t => /MM24s$/.test(t.name || '')).y;
  const n12 = got12.filter(v => v !== null).length, n24 = got24.filter(v => v !== null).length;
  ok(n24 > 500 && n24 < n12, 'a MM24 tem menos pontos validos que a MM12', n24 + ' vs ' + n12);

  // 16i. sem media movel nao sobra nenhuma linha -- o estado default e barras puras
  registry['sel-cot-ma'].value = '0'; registry['sel-cot-ma'].change();
  ok(ultimoReact('chart-cot-brl').traces.every(t => t.type === 'bar'),
     'voltando para "Nenhuma" nao sobra linha nenhuma');

  // 16j. o seletor de tipo troca tudo para linha
  registry['sel-cot-kind'].value = 'lines'; registry['sel-cot-kind'].change();
  ok(ultimoReact('chart-cot-brl').traces.every(t => t.type === 'scatter'),
     'em "Linhas" nao sobra barra');
  registry['sel-cot-kind'].value = 'bars'; registry['sel-cot-kind'].change();

  // 16k. as 6 linhas tem cartao de definicao -- e o cartao e onde a resposta a
  // "quem sao os outros participantes" fica por escrito
  const semCartao = linhasCot().filter(tr => !botaoInfo(tr)).map(tr => tr.dataset.key);
  ok(semCartao.length === 0, 'as 6 linhas tem botao "i"', semCartao.join(', '));
  botaoInfo(linhasCot().find(tr => tr.dataset.key === 'cot_dealer')).fire('mouseenter');
  ok(_infoPop.innerHTML.indexOf('sell side') > 0,
     'o cartao do dealer explica o papel dele, nao so o nome');
  ok(_infoPop.innerHTML.indexOf('Unidade: contratos') > 0,
     'e a unidade do cartao e a do grafico', _infoPop.innerHTML.slice(-120));
  hideInfo();
  botaoInfo(linhasCot().find(tr => tr.dataset.key === 'cot_oi')).fire('mouseenter');
  ok(_infoPop.innerHTML.indexOf('Não é a soma') > 0,
     'e o cartao do open interest avisa que ele nao e a soma dos liquidos');
  hideInfo();

  // 16l. o grafico de manchete das Reservas foi removido (item (i) do pedido)
  ok(htmlBruto.indexOf('chart-bcb-reserves') < 0, 'o grafico de Reservas Internacionais saiu');
  ok(htmlBruto.indexOf('sec-bcb-reserves"') < 0, 'e a secao dele tambem');
  ok(newPlotCalls.concat(reactCalls).every(c => c.div !== 'chart-bcb-reserves'),
     'e nada tentou desenha-lo');
  // a arvore de reservas continua de pe, e a nota dela nao pode mais mandar o leitor
  // olhar "o grafico acima", que nao existe
  ok(htmlBruto.indexOf('chart-resv-tree') > 0, 'a arvore de reservas continua');
  const iArv = htmlBruto.indexOf('id="sec-bcb-reserves-tree"');
  const secArv = htmlBruto.slice(iArv, htmlBruto.indexOf('</section>', iArv));
  ok(secArv.indexOf('gráfico acima') < 0, 'a nota da arvore nao aponta mais para um grafico que nao existe');
}

console.log(`\n${oks} ok, ${falhas} falhou`);
process.exit(falhas ? 1 : 0);
