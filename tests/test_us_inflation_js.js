/*
 * Executa o JavaScript REAL embutido em reports/us/Inflation.html contra um
 * document/Plotly stubados, e confere o comportamento -- nao a forma dos objetos
 * de configuracao.
 *
 * Existe por causa da licao registrada em .claude/rules/lis-dashboards.md: duas
 * rodadas de bug de interacao passaram batido em analytics/brasil/economic_activity
 * porque os testes afirmavam sobre a DEFINICAO dos botoes e nunca sobre o que
 * acontecia ao clicar. Aqui o script inteiro do relatorio e avaliado de verdade,
 * o factory da tabela hierarquica e inicializado, e as assercoes sao sobre as
 * linhas/celulas que ele produziu e sobre os numeros que ele calculou.
 *
 * Sem browser neste ambiente, entao renderizacao visual continua nao verificada --
 * o que este teste cobre e a camada de dados/DOM, que e onde os erros silenciosos
 * de calculo aparecem.
 *
 * Uso:  node tests/test_us_inflation_js.js
 */

const fs = require('fs');
const path = require('path');

const HTML = path.join(__dirname, '..', 'reports', 'us', 'Inflation.html');

let falhas = 0, oks = 0;
function ok(cond, msg, extra) {
  if (cond) { oks++; console.log('  ok      ' + msg); }
  else { falhas++; console.log('  FALHOU  ' + msg + (extra !== undefined ? '  -> ' + extra : '')); }
}
function near(a, b, tol, msg) {
  const d = Math.abs(a - b);
  ok(d <= tol, msg, `esperado ~${b}, veio ${a} (diff ${d.toFixed(4)})`);
}

// ── DOM stub -------------------------------------------------------------------
function makeEl(tag) {
  const e = {
    tagName: (tag || '').toUpperCase(),
    children: [], className: '', textContent: '', title: '',
    style: {}, dataset: {}, type: '', checked: false,
    classList: {
      _s: new Set(),
      add(c) { this._s.add(c); }, remove(c) { this._s.delete(c); },
      contains(c) { return this._s.has(c); },
      toggle(c, on) { if (on === undefined) { this._s.has(c) ? this._s.delete(c) : this._s.add(c); } else { on ? this._s.add(c) : this._s.delete(c); } }
    },
    _listeners: {},
    appendChild(c) { this.children.push(c); return c; },
    addEventListener(ev, fn) { (this._listeners[ev] = this._listeners[ev] || []).push(fn); },
    click() { (this._listeners['click'] || []).forEach(f => f.call(this, {})); },
    // _bindYAutofit (de analytics/report_structure/y_autofit.js) usa a API de
    // eventos do Plotly, el.on(...), e nao addEventListener.
    on(ev, fn) { (this._listeners[ev] = this._listeners[ev] || []).push(fn); },
    fire(ev) { (this._listeners[ev] || []).forEach(f => f.call(this, {})); },
    createTextNode: null
  };
  // innerHTML tem de ser acessor, nao campo: o codigo do relatorio limpa a tabela
  // com `tbody.innerHTML = ''` antes de cada render. Com innerHTML como campo
  // simples o array `children` do stub nunca esvaziava, e as assercoes liam a
  // linha da renderizacao ANTERIOR -- um falso negativo que parecia bug do produto.
  let _html = '';
  Object.defineProperty(e, 'innerHTML', {
    get() { return _html; },
    set(v) { _html = v; if (v === '') e.children.length = 0; }
  });
  // Batizar um elemento tem de torna-lo achavel por getElementById, como no
  // browser. Sem isto, um <button> que o proprio script cria e batiza (o toggle de
  // valores) existia em duas copias: o produto mexia na que criou, o teste lia uma
  // vazia que o registry inventava na hora.
  let _id = '';
  Object.defineProperty(e, 'id', {
    get() { return _id; },
    set(v) { _id = v; if (v) registry[v] = e; }
  });
  return e;
}

const registry = {};
function el(id) {
  if (!registry[id]) { registry[id] = makeEl('div'); registry[id].id = id; }
  return registry[id];
}

// pills que o template declara em HTML -- o script os procura por querySelectorAll
const pills = {};
function definePills(groupId, attr, values) {
  pills[groupId] = values.map((v, i) => {
    const p = makeEl('button');
    p.dataset[attr] = v.name;
    if (v.active) p.classList.add('active');
    if (v.disabled) p.classList.add('disabled');
    p.classList.add('pill');
    return p;
  });
}
// Uma aba de CPI so, com as duas arvores num seletor (2026-08-26). Nao ha mais
// pills de View: a visao Table 1 saiu, e as duas arvores deixaram de ser duas abas.
definePills('cpi-tree-group', 'tree', [{name: 'release', active: true}, {name: 'expenditure'}]);
definePills('cpi-metric-group', 'metric', [
  {name: 'yoy', active: true}, {name: 'mom'}, {name: 'ann3m'},
  {name: 'contrib'}, {name: 'contribm'}]);
definePills('cpi-basis-group', 'basis', [{name: 'NSA'}, {name: 'SA', active: true}]);
definePills('cpi-window-group', 'win', [
  {name: '1'}, {name: '3'}, {name: '6'}, {name: '12', active: true}]);
// A pill NSA do PCE nasce desabilitada: o BEA nao publica PCE mensal sem ajuste
// sazonal.
definePills('pce-metric-group', 'metric', [
  {name: 'yoy', active: true}, {name: 'mom'}, {name: 'ann3m'},
  {name: 'contrib'}, {name: 'contribm'}]);
definePills('pce-basis-group', 'basis', [{name: 'NSA', disabled: true}, {name: 'SA', active: true}]);

const tabButtons = ['cpi', 'pce', 'appendix'].map(t => {
  const b = makeEl('button'); b.dataset.tab = t; return b;
});

const relayoutCalls = [];
const reactCalls = [];
const restyleCalls = [];

// As gavetas do apendice sao lidas do PROPRIO html, nao listadas aqui: renomear
// uma secao no template tem de quebrar o teste, e nao virar um stub vazio que
// passa sem testar nada.
const htmlBruto = fs.readFileSync(HTML, 'utf8');
const drawerIds = [...htmlBruto.matchAll(/<details class="acc" id="([\w-]+)"/g)].map(m => m[1]);
drawerIds.forEach(id => { el(id).open = htmlBruto.indexOf('id="' + id + '" open') >= 0; });
const panelIds = ['panel-cpi', 'panel-pce', 'panel-appendix'];

global.document = {
  getElementById: (id) => el(id),
  createElement: (t) => makeEl(t),
  createTextNode: (txt) => ({ nodeType: 3, textContent: txt }),
  addEventListener: () => {},
  querySelectorAll: (sel) => {
    const m = sel.match(/^#([\w-]+) \.pill$/);
    if (m) return pills[m[1]] || [];
    if (sel === 'nav.tabs button') return tabButtons;
    if (sel === '.panel') return panelIds.map(el);
    if (sel === '#panel-appendix details.acc') return drawerIds.map(el);
    return [];
  }
};
global.Plotly = {
  react: (div, traces, layout, config) => { reactCalls.push({div, traces, layout, config}); },
  newPlot: () => {},
  relayout: (div, upd) => { relayoutCalls.push({div, upd}); return Promise.resolve(); },
  restyle: (div, upd, idx) => { restyleCalls.push({div, upd, idx}); return Promise.resolve(); },
  Plots: { resize: () => {} }
};
global.window = global;

// ── run the report's real script ----------------------------------------------
const html = htmlBruto;
const scripts = [...html.matchAll(/<script(?![^>]*\bsrc=)[^>]*>([\s\S]*?)<\/script>/g)].map(m => m[1]);
if (!scripts.length) { console.log('FALHOU: nenhum <script> inline encontrado'); process.exit(1); }
const code = scripts[scripts.length - 1];
console.log(`script inline: ${code.length.toLocaleString()} chars`);

eval(code);

console.log('\n=== 1. payload =============================================');
ok(typeof D === 'object' && D.tabs, 'REPORT_DATA parseou e tem .tabs');
ok(D.meta.n_release === 37, 'release tree tem 37 linhas', D.meta.n_release);
ok(D.meta.n_expenditure === 355, 'expenditure tree tem 355 itens', D.meta.n_expenditure);
ok(D.meta.n_expenditure_sem_peso === 83, '83 itens enxertados, sem peso publicado', D.meta.n_expenditure_sem_peso);
ok(Object.keys(D.weights).length > 250, 'pesos presentes', Object.keys(D.weights).length);

console.log('\n=== 2. metricSeries reproduz os numeros publicados ==========');
// Tabela 1 de jul/2026: headline y/y 3.4, core y/y 2.5, energy y/y 14.7, food y/y 3.0,
// headline m/m SA 0.1. O banco ja foi conferido contra isso; aqui o teste e do JS.
function ultimo(tab, code, basis, metric) {
  const s = metricSeries(tab, code, basis, metric);
  for (let i = s.values.length - 1; i >= 0; i--) if (s.values[i] != null) return s.values[i];
  return null;
}
near(ultimo('release', 'SA0', 'NSA', 'yoy'), 3.4, 0.05, 'headline y/y NSA ~ 3.4');
near(ultimo('release', 'SA0L1E', 'NSA', 'yoy'), 2.5, 0.05, 'core y/y NSA ~ 2.5');
near(ultimo('release', 'SA0E', 'NSA', 'yoy'), 14.7, 0.05, 'energy y/y NSA ~ 14.7');
near(ultimo('release', 'SAF1', 'NSA', 'yoy'), 3.0, 0.05, 'food y/y NSA ~ 3.0');
near(ultimo('release', 'SA0', 'SA', 'mom'), 0.1, 0.05, 'headline m/m SA ~ 0.1');

console.log('\n=== 3. metricas derivadas sao coerentes =====================');
const lvl = metricSeries('release', 'SA0', 'SA', 'level').values;
const mom = metricSeries('release', 'SA0', 'SA', 'mom').values;
const i = lvl.length - 1;
near(mom[i], (lvl[i] / lvl[i - 1] - 1) * 100, 1e-9, 'm/m == variacao do nivel');
const a3 = metricSeries('release', 'SA0', 'SA', 'ann3m').values;
near(a3[i], (Math.pow(lvl[i] / lvl[i - 3], 4) - 1) * 100, 1e-9, '3M ann. == (L/L-3)^4-1');
ok(mom[0] === null && metricSeries('release','SA0','SA','yoy').values[5] === null,
   'as primeiras posicoes ficam null (sem lag disponivel)');

console.log('\n=== 4. contribuicao: soma dos 3 nos de nivel 1 ~ headline ====');
const cF = ultimo('release', 'SAF1', 'NSA', 'contrib');
const cE = ultimo('release', 'SA0E', 'NSA', 'contrib');
const cC = ultimo('release', 'SA0L1E', 'NSA', 'contrib');
const soma = cF + cE + cC;
const head = ultimo('release', 'SA0', 'NSA', 'yoy');
console.log(`          food ${cF.toFixed(3)} + energy ${cE.toFixed(3)} + core ${cC.toFixed(3)} = ${soma.toFixed(3)} vs headline ${head.toFixed(3)}`);
near(soma, head, 0.15, 'contribuicoes de nivel 1 reconstroem o headline (aprox., ver Apendice)');

console.log('\n=== 5. weightFor usa o snapshot de dezembro do ano anterior ==');
const anos = Object.keys(D.weights['SA0E']).map(Number).sort((a,b)=>a-b);
console.log('          snapshots de SA0E: ' + JSON.stringify(D.weights['SA0E']));
ok(weightFor('SA0E', '2026-07-01') === D.weights['SA0E']['2025'],
   'mes de 2026 usa o snapshot de 2025', weightFor('SA0E', '2026-07-01'));
ok(weightFor('SA0E', '2023-04-01') === D.weights['SA0E']['2022'],
   'mes de 2023 usa o snapshot de 2022', weightFor('SA0E', '2023-04-01'));
ok(weightFor('SA0E', '1995-04-01') === D.weights['SA0E'][String(anos[0])],
   'mes antes do primeiro snapshot cai no mais antigo', weightFor('SA0E', '1995-04-01'));
ok(weightFor('NAO_EXISTE', '2026-01-01') === null, 'item sem peso devolve null');

console.log('\n=== 6. a arvore e o achatamento =============================');
const relTree = D.tabs.release.tree;
ok(relTree.length === 1 && relTree[0].key === 'SA0', 'release tem uma raiz, SA0');
const todosRel = (function cnt(ns) { return ns.reduce((a, n) => a + 1 + (n.children ? cnt(n.children) : 0), 0); })(relTree);
const relPub = (function cnt(ns) {
  return ns.reduce((a, n) => a + (n.detail ? 0 : 1) + (n.children ? cnt(n.children) : 0), 0);
})(relTree);
const relDet = todosRel - relPub;
ok(relPub === 37, 'a arvore de divulgacao mantem as 37 linhas publicadas', relPub);
ok(relDet === 163, 'mais 163 linhas de drill-down da arvore de despesa', relDet);
ok(relDet === D.meta.n_release_drill, 'o meta bate com a arvore', D.meta.n_release_drill);

// O drill-down entra SO abaixo de folha do release: nenhum no publicado pode ter
// ganhado irmao novo, senao a decomposicao parcial da Tabela 1 passaria a mentir.
let misturados = [];
(function walk(ns) {
  ns.forEach(n => {
    if (n.children && !n.detail) {
      const kinds = n.children.map(c => !!c.detail);
      if (kinds.some(k => k) && kinds.some(k => !k)) misturados.push(n.key);
    }
    if (n.children) walk(n.children);
  });
})(relTree);
ok(misturados.length === 0, 'nenhum pai publicado mistura filho publicado com drill-down',
   misturados.join(','));
// Motor fuel continua parcial: Other motor fuels e IRMAO de Gasoline (all types),
// nao um nivel mais fundo, entao o drill-down nao o traz.
const relPorCode = {};
(function walk(ns) { ns.forEach(n => { relPorCode[n.key] = n; if (n.children) walk(n.children); }); })(relTree);
ok(relPorCode['SETB'] && relPorCode['SETB'].decomp === 'partial',
   'Motor fuel segue "partial" na aba de divulgacao');
ok(relPorCode['SETB01'] && relPorCode['SETB01'].children &&
   relPorCode['SETB01'].children.length === 3,
   'e Gasoline (all types) abre nos 3 tipos ali mesmo');
ok(['SS47014','SS47015','SS47016'].every(c => relPorCode[c] && relPorCode[c].detail === 1),
   'os 3 tipos vem marcados detail na aba de divulgacao');

// A serie de um no de drill-down vive na OUTRA aba: seriesSource tem de achar.
const drill = metricSeries('release', 'SS47014', 'NSA', 'yoy');
ok(drill.values.some(v => v !== null && !isNaN(v)),
   'Y/Y de um no de drill-down resolve na aba de divulgacao (seriesSource)');
ok(drill.dates.length > 0 && drill.dates.length === D.tabs.expenditure.dates.NSA.length,
   'e usa a grade de datas da aba que tem a serie', drill.dates.length);
// A tabela monta as colunas com os 12 ultimos meses da grade DA ABA. Se as duas
// grades nao terminarem no mesmo mes, toda linha de drill-down apareceria como "—".
['NSA', 'SA'].forEach(function(b) {
  const r12 = D.tabs.release.dates[b].slice(-12).join(',');
  const e12 = D.tabs.expenditure.dates[b].slice(-12).join(',');
  ok(r12 === e12, 'as duas grades terminam nos mesmos 12 meses (' + b + ')');
});
const expTree = D.tabs.expenditure.tree;
const todosExp = (function cnt(ns) { return ns.reduce((a, n) => a + 1 + (n.children ? cnt(n.children) : 0), 0); })(expTree);
ok(todosExp === 355, 'expenditure tem 355 nos', todosExp);
const prof = (function d(ns, k) { return ns.reduce((m, n) => Math.max(m, n.children ? d(n.children, k + 1) : k), k); })(expTree, 0);
ok(prof === 9, 'expenditure tem 10 niveis (profundidade maxima 9)', prof);

const soRaiz = flattenHierRows(relTree, {}, 0);
ok(soRaiz.length === 1, 'sem nada expandido, achata para 1 linha', soRaiz.length);
const comRaiz = flattenHierRows(relTree, {SA0: true}, 0);
ok(comRaiz.length === 4, 'expandindo SA0 mostra 1 + 3 filhos', comRaiz.length);

console.log('\n=== 6b. o enxerto: os itens abaixo da planilha de pesos ======');
const porCode = {};
(function walk(ns) { ns.forEach(n => { porCode[n.key] = n; if (n.children) walk(n.children); }); })(expTree);

// Gasoline (all types) deixou de ser folha: os 3 tipos estao abaixo dele.
const gas = porCode['SETB01'];
ok(!!gas && !!gas.children, 'Gasoline (all types) tem filhos agora');
ok(gas && gas.children && gas.children.length === 3,
   'os 3 tipos de gasolina (regular/midgrade/premium)', gas && gas.children && gas.children.length);
ok(['SS47014', 'SS47015', 'SS47016'].every(c => !!porCode[c]), 'os 3 codigos SS estao na arvore');
ok(!!porCode['SS17031'] && !!porCode['SS17032'], 'roasted e instant coffee estao na arvore');
ok(!!porCode['SSEE041'], 'Smartphones esta na arvore');

const semPeso = Object.keys(porCode).map(k => porCode[k]).filter(n => n.noWeight);
ok(semPeso.length === 83, '83 nos marcados noWeight', semPeso.length);
ok(semPeso.every(n => !n.children || n.children.every(c => c.noWeight)),
   'nenhum item COM peso publicado esta pendurado abaixo de um sem peso');

// Contribuicao de um item sem peso tem de ser vazia -- nao 0, nao NaN.
const contribSemPeso = metricSeries('expenditure', 'SS47014', 'NSA', 'contrib');
ok(contribSemPeso.values.every(v => v === null),
   'contribuicao de um item sem peso e toda nula (nao 0, nao NaN)');
const yoySemPeso = metricSeries('expenditure', 'SS47014', 'NSA', 'yoy');
ok(yoySemPeso.values.some(v => v !== null && !isNaN(v)),
   'mas Y/Y do mesmo item tem valores -- so a contribuicao depende do peso');

// Os 5 itens que o casamento por nome perdia: entraram COM peso.
const alias = ['SEHB01', 'SEAA02', 'SEAC04', 'SEMD03', 'SEEB04'];
ok(alias.every(c => !!porCode[c]), 'os 5 itens de _ALIAS estao na arvore');
ok(alias.every(c => !porCode[c].noWeight), 'e todos os 5 tem peso publicado (nao sao enxerto)');
ok(alias.every(c => metricSeries('expenditure', c, 'NSA', 'contrib').values.some(v => v !== null)),
   'contribuicao dos 5 e calculavel -- era exatamente isso que se perdia');

// Series encerradas ficam marcadas, com o mes final.
const encerradas = Object.keys(porCode).map(k => porCode[k]).filter(n => n.stale);
ok(encerradas.length === 19, '19 series sem observacao recente, marcadas', encerradas.length);
ok(encerradas.every(n => /^[0-9]{4}-[0-9]{2}$/.test(n.stale)),
   'toda marca "last" traz o mes final');
// 1 mes de atraso e lag de divulgacao, nao serie morta -- a folga de 3 meses e o que
// impede o relatorio de declarar encerrada uma serie que so nao imprimiu ainda.
ok(!porCode['SEMC04'] || !porCode['SEMC04'].stale,
   'um item 1 mes atrasado NAO e marcado (Services by other medical professionals)');

console.log('\n=== 7. a decomposicao parcial carrega a massa faltante =======');
let partials = [];
(function walk(ns) { ns.forEach(n => { if (n.decomp === 'partial') partials.push(n); if (n.children) walk(n.children); }); })(relTree);
ok(partials.length === 7, '7 pais parciais na arvore de divulgacao', partials.length);
const massa = partials.reduce((a, n) => a + n.unshown, 0);
near(massa, 25.583, 0.01, 'massa nao exibida soma 25.583 pontos');
ok(partials.every(n => typeof n.unshown === 'number' && n.unshown > 0),
   'todo no parcial tem unshown numerico positivo');

console.log('\n=== 8. o factory renderizou tabela e grafico de verdade ======');
const corpo = el('cpi-table-body');
ok(corpo.children.length === 4, 'tbody da release tem 4 linhas no estado inicial (raiz expandida)', corpo.children.length);
const cab = el('cpi-table-head');
ok(cab.children.length === 1 && cab.children[0].children.length === 14,
   'cabecalho tem check + label + 12 meses', cab.children[0] && cab.children[0].children.length);
const primeira = corpo.children[0];
ok(primeira.children.length === 14, 'linha de dados tem 14 celulas', primeira.children.length);
const valores = primeira.children.slice(2).map(td => td.textContent);
ok(valores.every(v => v === '—' || /^[+-]\d+\.\d{2}$/.test(v)),
   'celulas formatadas como +/-N.NN ou em-dash', JSON.stringify(valores.slice(0, 4)));

ok(reactCalls.length >= 2, 'Plotly.react chamado para os dois graficos', reactCalls.length);
const rel = reactCalls.find(c => c.div === 'chart-cpi');
ok(!!rel, 'chart-release foi plotado');
ok(rel.traces.length === 3, 'plota os 3 nos marcados por default', rel.traces.length);
ok(rel.layout.dragmode === 'pan', 'dragmode = pan');
ok(rel.config.scrollZoom === true, 'scrollZoom ligado');
ok(rel.layout.yaxis.title.text === '%', 'titulo do Y para y/y e "%"', rel.layout.yaxis.title.text);
ok(rel.traces.every(t => t.x.length === t.y.length && t.x.length > 100),
   'traces tem x e y do mesmo tamanho e historico longo');

console.log('\n=== 9. clicar nos pills muda tabela e grafico ================');
// A pill "Index" saiu a pedido do usuario. O NIVEL continua sendo o que viaja no
// payload e do que toda metrica deriva -- so deixou de ser escolhivel.
ok(!pills['cpi-metric-group'].some(p => p.dataset.metric === 'level'),
   'a metrica Index nao e mais oferecida');
ok(html.indexOf('data-metric="level"') === -1,
   'e nao sobrou nenhum data-metric="level" no HTML gerado');
ok(metricSeries('release', 'SA0', 'SA', 'level').values.some(v => v != null),
   'mas o caminho do nivel continua vivo por dentro -- e a base de todo o resto');

const nAntes9 = reactCalls.length;
pills['cpi-metric-group'].find(p => p.dataset.metric === 'mom').click();
ok(reactCalls.length > nAntes9, 'clicar em "M/M %" re-renderizou o grafico');
ok(reactCalls[reactCalls.length - 1].traces.every(x => x.type === 'scatter'),
   'metrica de variacao continua desenhada como linha');

// --- contribuicao: barra empilhada + o total em linha ------------------------
// O que este bloco protege e a LEITURA do grafico, nao a forma do objeto: que a
// pilha e mesmo uma pilha, que o total e uma linha e nao mais uma barra, e que as
// barras somam a linha quando os marcados particionam o indice.
const rotuloHeadRel = D.tabs.release.tree[0].label;
pills['cpi-metric-group'].find(p => p.dataset.metric === 'contrib').click();
const cY = reactCalls[reactCalls.length - 1];
ok(cY.layout.yaxis.title.text === 'p.p. of headline Y/Y',
   'titulo do Y para contribuicao e em p.p.', cY.layout.yaxis.title.text);
ok(cY.layout.barmode === 'relative',
   'empilha em barmode "relative" -- contribuicao negativa desce abaixo do zero em vez ' +
   'de sumir dentro da pilha positiva', cY.layout.barmode);
const barrasY = cY.traces.filter(x => x.type === 'bar');
const totaisY = cY.traces.filter(x => x.type === 'scatter');
ok(barrasY.length === 3 && totaisY.length === 1,
   '3 barras (os nos marcados) + 1 linha (o total)',
   `${barrasY.length} barras, ${totaisY.length} linhas`);
ok(totaisY[0].name.indexOf(rotuloHeadRel) === 0 && totaisY[0].name.indexOf('Y/Y') > 0,
   'a linha e o headline, rotulada com o horizonte', totaisY[0].name);
ok(totaisY[0].line.width > barrasY.length * 0 + 2 && totaisY[0].line.color === '#111111',
   'a linha do total e preta e mais grossa -- nao le como mais um componente',
   totaisY[0].line.color);

function ultimoIndiceCheio(bars, tot) {
  for (let i = tot.y.length - 1; i >= 0; i--) {
    if (tot.y[i] != null && bars.every(b => b.y[i] != null)) return i;
  }
  return -1;
}
const ixY = ultimoIndiceCheio(barrasY, totaisY[0]);
ok(ixY >= 0, 'ha um mes com contribuicao em todos os tres nos e no total');
const somaY = barrasY.reduce((s, b) => s + b.y[ixY], 0);
console.log(`          [medido] Y/Y ${totaisY[0].x[ixY].slice(0, 7)}: barras ` +
            `${somaY.toFixed(3)} vs linha ${totaisY[0].y[ixY].toFixed(3)}`);
near(somaY, totaisY[0].y[ixY], 0.15,
     'as barras empilhadas reconstroem a linha do total (nivel 1 particiona o indice)');
ok(el('cpi-t1note').innerHTML.indexOf('decomposition') > 0 &&
   el('cpi-t1note').innerHTML.indexOf('partition') > 0,
   'a nota diz que a pilha so alcanca a linha quando os marcados particionam o indice');

// --- a metrica nova: contribuicao para o M/M ---------------------------------
pills['cpi-metric-group'].find(p => p.dataset.metric === 'contribm').click();
const cM = reactCalls[reactCalls.length - 1];
ok(cM.layout.yaxis.title.text === 'p.p. of headline M/M',
   'contribuicao M/M tem titulo de Y proprio', cM.layout.yaxis.title.text);
ok(cM.layout.barmode === 'relative', 'e tambem empilha');
const barrasM = cM.traces.filter(x => x.type === 'bar');
const totaisM = cM.traces.filter(x => x.type === 'scatter');
ok(barrasM.length === 3 && totaisM.length === 1, '3 barras + 1 linha tambem no M/M');
ok(totaisM[0].name.indexOf('M/M') > 0, 'a linha do total agora diz M/M', totaisM[0].name);
const ixM = ultimoIndiceCheio(barrasM, totaisM[0]);
const somaM = barrasM.reduce((s, b) => s + b.y[ixM], 0);
console.log(`          [medido] M/M ${totaisM[0].x[ixM].slice(0, 7)}: barras ` +
            `${somaM.toFixed(4)} vs linha ${totaisM[0].y[ixM].toFixed(4)}`);
near(somaM, totaisM[0].y[ixM], 0.06,
     'as contribuicoes de nivel 1 reconstroem tambem a variacao MENSAL do headline');

// A contribuicao mensal e uma ordem de grandeza menor que a anual: com 2 casas a
// coluna vira uma parede de "+0.00". Por isso 3 casas, e so nela.
const celulaM = el('cpi-table-body').children[0].children[2].textContent;
ok(celulaM === '—' || /^[+-]\d+\.\d{3}$/.test(celulaM),
   'celula de contribuicao M/M sai com 3 casas decimais', celulaM);
pills['cpi-metric-group'].find(p => p.dataset.metric === 'contrib').click();
const celulaY = el('cpi-table-body').children[0].children[2].textContent;
ok(celulaY === '—' || /^[+-]\d+\.\d{2}$/.test(celulaY),
   'e a de Y/Y continua com 2', celulaY);

// --- o caso que o desenho existe para tratar: o total marcado ---------------
// A aba de PCE nasce com a linha 1 (o proprio total) marcada. Empilhada junto com
// os componentes ela dobraria o grafico -- entao ela vira a linha.
ok(D.tabs.pce.defaultChecked.indexOf(D.tabs.pce.anchor) >= 0,
   'a aba PCE nasce com o proprio total marcado');
pills['pce-metric-group'].find(p => p.dataset.metric === 'contrib').click();
const cP = reactCalls[reactCalls.length - 1];
ok(cP.div === 'chart-pce', 'o grafico redesenhado e o do PCE', cP.div);
const barrasP = cP.traces.filter(x => x.type === 'bar');
const totaisP = cP.traces.filter(x => x.type === 'scatter');
const rotuloHeadPce = D.tabs.pce.tree[0].label;
ok(barrasP.length === 3 && totaisP.length === 1,
   'o total marcado vira a LINHA, nao uma 4a barra empilhada sobre os proprios componentes',
   `${barrasP.length} barras, ${totaisP.length} linhas`);
ok(!barrasP.some(x => x.name === rotuloHeadPce),
   'e nenhuma barra leva o rotulo do total', barrasP.map(x => x.name).join(' | '));
ok(totaisP[0].name.indexOf(rotuloHeadPce) === 0,
   'a linha, sim', totaisP[0].name);
pills['pce-metric-group'].find(p => p.dataset.metric === 'yoy').click();
ok(reactCalls[reactCalls.length - 1].traces.every(x => x.type === 'scatter'),
   'e voltar para Y/Y no PCE traz o total de volta como linha entre linhas');

const pillNSA = pills['cpi-basis-group'].find(p => p.dataset.basis === 'NSA');
const nAntes = reactCalls.length;
pillNSA.click();
ok(reactCalls.length > nAntes, 'trocar SA->NSA re-renderizou');

console.log('\n=== 10. botoes de range chamam Plotly.relayout ===============');
const barra = el('cpi-range');
const botoes = barra.children.filter(c => c.className === 'rb');
ok(botoes.length === 6, '6 botoes de range (1y/3y/5y/10y/20y/All)', botoes.length);
ok(botoes.map(b => b.textContent).join('/') === '1y/3y/5y/10y/20y/All',
   'nessa ordem', botoes.map(b => b.textContent).join('/'));
relayoutCalls.length = 0;
botoes[1].click();
ok(relayoutCalls.length === 1, 'clicar em "3y" chamou relayout uma vez', relayoutCalls.length);
const r = relayoutCalls[0].upd['xaxis.range'];
ok(Array.isArray(r) && r.length === 2, 'relayout passou um par [de, ate]', JSON.stringify(r));
const anosJan = (new Date(r[1]) - new Date(r[0])) / (365.25 * 24 * 3600 * 1000);
near(anosJan, 3, 0.15, 'a janela de "3y" cobre ~3 anos');
ok(r[1] === D.tabs.release.dates.NSA[D.tabs.release.dates.NSA.length - 1],
   'o fim da janela e o ultimo ponto REAL da serie, nao a data de hoje', r[1]);
relayoutCalls.length = 0;
botoes[0].click();
const r1 = relayoutCalls[0].upd['xaxis.range'];
near((new Date(r1[1]) - new Date(r1[0])) / (365.25 * 24 * 3600 * 1000), 1, 0.1,
     'e a de "1y" cobre ~1 ano');
// "All" manda as duas pontas REAIS, nao `xaxis.autorange`: o autorange devolve o
// range com o padding do proprio Plotly, que numa serie que comeca em 1913 e uma
// faixa vazia visivel depois do ultimo ponto.
relayoutCalls.length = 0;
botoes[5].click();
const rAll = relayoutCalls[0].upd['xaxis.range'];
ok(relayoutCalls[0].upd['xaxis.autorange'] === undefined,
   '"All" nao usa autorange');
const gradeNSA = D.tabs.release.dates.NSA;
ok(Array.isArray(rAll) && rAll[0] === gradeNSA[0] && rAll[1] === gradeNSA[gradeNSA.length - 1],
   'manda as duas pontas reais da grade', JSON.stringify(rAll));

console.log('\n=== 11. KPIs ================================================');
const kpis = el('kpis');
ok(kpis.children.length === 6, '6 cards de KPI', kpis.children.length);
ok(kpis.children.every(c => c.innerHTML.indexOf('—') === -1),
   'nenhum KPI ficou sem valor');

console.log('\n=== 12. o peso reconstruido (a visao Table 1 saiu) ==========');
// As 37 importancias relativas IMPRESSAS na Tabela 1 do release de julho/2026.
// A planilha de pesos so publica dezembro, entao o numero e RECONSTRUIDO -- este
// bloco e a prova de que a reconstrucao esta certa, contra o numero publicado.
//
// A VISAO de nove colunas que imprimia isso na cara da aba saiu em 2026-08-26 a
// pedido do usuario. A aritmetica dela NAO saiu junto: riAt alimenta a coluna
// Weight da tabela de contribuicoes e levelAt/pctBetween alimentam a coluna Change,
// entao esta conferencia sobreviveu a visao que a motivou -- que e a razao de nao
// apagar o bloco com ela.
const RI_PUBLICADA = {
  SA0: 100.000, SAF1: 13.522, SAF11: 8.231, SAF111: 1.023, SAF112: 1.959, SEFJ: 0.743,
  SAF113: 1.283, SAF114: 0.981, SAF115: 2.242, SEFV: 5.290, SA0E: 7.432, SACE: 4.132,
  SEHE01: 0.106, SETB: 3.971, SETB01: 3.852, SEHF: 3.300, SEHF01: 2.552, SEHF02: 0.748,
  SA0L1E: 79.047, SACL1E: 18.829, SAA: 2.437, SETA01: 3.751, SETA02: 2.679, SAM1: 1.412,
  SAF116: 0.823, SEGA: 0.445, SASLE: 60.217, SAH1: 35.304, SEHA: 7.716, SEHC: 25.849,
  SAM2: 6.840, SEMC01: 1.660, SEMD01: 2.156, SAS4: 6.352, SETD: 1.048, SETE: 2.570,
  SETG01: 1.091
};

ok(!pills['cpi-view-group'] && !pills['expenditure-view-group'],
   'nao ha mais grupo de pills de View em aba nenhuma');
ok(html.indexOf('data-view="table1"') === -1,
   'e nenhum data-view="table1" sobrou no HTML gerado');
ok(typeof table1Cols === 'undefined' && typeof fmtT1 === 'undefined',
   'as funcoes que so serviam aquela visao sumiram do script -- nao viraram codigo morto');
ok(typeof pctBetween === 'function' && typeof riAt === 'function',
   'mas as que tem consumidor novo continuam');

const nsaRel = D.tabs.release.dates.NSA, saRel = D.tabs.release.dates.SA;
const mRef = nsaRel[nsaRel.length - 1];
const mPrev = nsaRel[nsaRel.length - 2];
const mYr = nsaRel[nsaRel.length - 13];
ok(mRef.slice(0, 7) === D.meta.ultimo_mes, 'o mes de referencia e o ultimo mes da base', mRef);
const mesAnterior = (function(ym) {
  const a = parseInt(ym.slice(0, 4), 10), m = parseInt(ym.slice(5, 7), 10) - 1;
  const tot = a * 12 + (m - 1);
  return String(Math.floor(tot / 12)).padStart(4, '0') + '-' + String(tot % 12 + 1).padStart(2, '0');
})(mRef.slice(0, 7));
ok(riMonth('release').slice(0, 7) === mesAnterior,
   'a importancia relativa e datada um mes atras, como o release a data', riMonth('release'));

let piorRI = 0, semRI = [], conferidas = 0;
Object.keys(RI_PUBLICADA).forEach(function(code) {
  const v = riAt('release', code, mPrev);
  if (v == null) { semRI.push(code); return; }
  conferidas++;
  piorRI = Math.max(piorRI, Math.abs(v - RI_PUBLICADA[code]));
});
ok(semRI.length === 0, 'as 37 linhas publicadas todas produzem uma importancia relativa',
   semRI.join(','));
// A contagem entra na assercao de proposito: sem ela, um riAt() que devolve null
// para tudo deixa piorRI em 0 e o teste passa sem ter conferido nada -- foi
// exatamente o que aconteceu na primeira rodada.
ok(conferidas === 37 && piorRI <= 0.0015,
   'e as 37 batem com o numero impresso na Tabela 1 (erro <= 0.001)',
   conferidas + ' conferidas, erro ' + piorRI.toFixed(4));
console.log('          erro maximo contra a Tabela 1 impressa: ' + piorRI.toFixed(4));

// A linha All items, celula por celula, contra o release impresso. Continua sendo
// exatamente o caminho que a coluna Change da tabela de contribuicoes percorre.
near(levelAt('release', 'SA0', 'NSA', mYr), 323.048, 0.0005, 'indice NSA jul/25 = 323.048');
near(levelAt('release', 'SA0', 'NSA', mPrev), 333.952, 0.0005, 'indice NSA jun/26 = 333.952');
near(levelAt('release', 'SA0', 'NSA', mRef), 333.918, 0.0005, 'indice NSA jul/26 = 333.918');
near(pctBetween('release', 'SA0', 'NSA', mRef, mYr), 3.4, 0.05, 'NSA 12 meses = 3.4%');
near(pctBetween('release', 'SA0', 'NSA', mRef, mPrev), 0.0, 0.05, 'NSA 1 mes = 0.0%');
const saM = saRel.slice(-4);
ok(saM.length === 4, 'a grade SA rende as 3 variacoes mensais do release', saM.length);
near(pctBetween('release', 'SA0', 'SA', saM[1], saM[0]), 0.5, 0.05, 'SA abr->mai = +0.5%');
near(pctBetween('release', 'SA0', 'SA', saM[2], saM[1]), -0.4, 0.05, 'SA mai->jun = -0.4%');
near(pctBetween('release', 'SA0', 'SA', saM[3], saM[2]), 0.1, 0.05, 'SA jun->jul = +0.1%');

// Prova estrutural, independente da Tabela 1 impressa: atualizar cada item
// separadamente nao pode quebrar a soma. Os 8 grupos de nivel 1 da arvore de
// despesa somam 100 antes e depois.
const somaRI = D.tabs.expenditure.tree[0].children.reduce(function(a, c) {
  return a + (riAt('expenditure', c.seriesKey, riMonth('expenditure')) || 0);
}, 0);
near(somaRI, 100, 0.002, 'a importancia relativa atualizada dos 8 grupos de nivel 1 ainda soma 100');

// Sem peso publicado nao ha importancia relativa a atualizar.
ok(riAt('expenditure', 'SS47014', mPrev) === null,
   'um item sem peso (gasolina comum) nao inventa importancia relativa');
ok(levelAt('expenditure', 'SS47014', 'NSA', mRef) != null,
   'mas o indice dele esta la');
// Uma linha de drill-down vive na outra arvore: o codigo tem de resolver pela de
// divulgacao tambem (seriesOwner).
ok(levelAt('release', 'SS47014', 'NSA', mRef) != null,
   'e resolve tambem pela arvore de divulgacao, onde ela e linha enxertada');

// A tabela nao tem mais visao que troque o conjunto de colunas.
ok(el('cpi-table-head').children.length === 1 &&
   el('cpi-table-head').children[0].children.length === 14,
   'o cabecalho e sempre uma linha de check + label + 12 meses',
   el('cpi-table-head').children.length);

ok(/^\d+$/.test(el('ap-ri-n').textContent),
   'o apendice recebeu a contagem de linhas com importancia relativa', el('ap-ri-n').textContent);
const nRI = parseInt(el('ap-ri-n').textContent, 10);
ok(nRI > 250 && nRI < D.meta.n_expenditure,
   'a contagem e plausivel: menos que os 355 itens, mais que 250', nRI);

console.log('\n=== 13. as linhas nao levam rotulo visivel ==================');
// Os badges (agg / detail / no weight / last YYYY-MM / -X.XXX pp) foram removidos
// a pedido do usuario. O que eles diziam foi para o title da celula do rotulo --
// entao o teste confere as duas coisas: que nao ha rotulo, e que o fato nao sumiu.
ok(html.indexOf('badge') === -1,
   'a palavra "badge" nao aparece em lugar nenhum do HTML gerado (CSS incluido)');

function textoLinha(tr) {
  return (tr.children[1].children || [])
    .map(c => c.textContent || '').join('').replace(/^[▾▸]\s*/, '').trim();
}
function acharLinha(rotulo) {
  const linhas = el('cpi-table-body').children;
  for (let i = 0; i < linhas.length; i++) if (textoLinha(linhas[i]) === rotulo) return linhas[i];
  return null;
}
function abrir(rotulo) {
  const linha = acharLinha(rotulo);
  if (!linha) return false;
  const tog = linha.children[1].children[0];
  if (!tog || tog.className !== 'tree-toggle') return false;
  tog.click();
  return true;
}
['Energy', 'Energy commodities', 'Motor fuel', 'Gasoline (all types)'].forEach(function(r) {
  ok(abrir(r), 'abriu ' + r);
});

const lMotor = acharLinha('Motor fuel');
ok(!!lMotor, 'Motor fuel esta na arvore');
ok(lMotor.children[1].children.filter(c => (c.className || '').indexOf('badge') >= 0).length === 0,
   'Motor fuel nao renderiza nenhum span de rotulo');
ok((lMotor.children[1].title || '').indexOf('0.119') > 0,
   'mas o hover ainda diz quanto peso nao tem linha ali', lMotor.children[1].title);

const lGas = acharLinha('Gasoline, unleaded regular');
ok(!!lGas, 'a gasolina comum continua na arvore (drill-down)');
ok(lGas.children[1].children.every(c => c.nodeType === 3),
   'a celula dela tem so texto, nenhum elemento');
ok((lGas.children[1].title || '').indexOf('no relative importance') > 0 &&
   (lGas.children[1].title || '').indexOf('Table 1') > 0,
   'e o hover diz que ela nao tem peso e nao e linha da Tabela 1', lGas.children[1].title);

const lAll = acharLinha('All items');
ok(!!lAll && !lAll.children[1].title,
   'uma linha sem ressalva nenhuma nao ganha hover', lAll && lAll.children[1].title);

let comRotulo = 0;
['cpi-table-body', 'pce-table-body'].forEach(function(id) {
  el(id).children.forEach(function(tr) {
    (tr.children[1].children || []).forEach(function(c) {
      if ((c.className || '').indexOf('badge') >= 0) comRotulo++;
    });
  });
});
ok(comRotulo === 0, 'nenhuma linha renderizada nas duas abas tem rotulo', comRotulo);

console.log('\n=== 14. a aba de PCE =======================================');
{
ok(D.tabs.pce && D.tabs.pce.tree, 'o payload tem a aba pce');
ok(D.meta.n_pce === 368, 'a arvore do PCE tem 368 linhas', D.meta.n_pce);
ok(D.meta.n_pce_addenda === 34, 'mais 34 agregados de addenda', D.meta.n_pce_addenda);
ok(D.meta.niveis_pce === 9, '9 niveis', D.meta.niveis_pce);
ok(Object.keys(D.tabs.pce.dates).join(',') === 'SA',
   'a grade do PCE so tem SA -- o BEA nao publica NSA mensal', Object.keys(D.tabs.pce.dates).join(','));
ok(!!D.tabs.pce.weights, 'a aba carrega pesos alinhados a grade (convencao mensal)');
ok(!D.tabs.release.weights && !D.tabs.expenditure.weights,
   'e nenhuma aba de CPI carrega -- e assim que weightAt separa as duas convencoes');

// O nivel publicado, contra o que a serie do FRED devolve (conferido ao vivo).
const mesPce = D.tabs.pce.dates.SA[D.tabs.pce.dates.SA.length - 1];
ok(mesPce.slice(0, 7) === D.meta.ultimo_mes_pce,
   'o ultimo mes da grade do PCE e o do meta', mesPce);
// O PCE do mes M sai ~2 semanas depois do CPI do mes M, entao durante parte do mes
// ele esta um mes atras -- mas no fim do mes ALCANCA. Uma versao anterior deste
// teste exigia que os dois nunca coincidissem, o que era um estado transitorio
// escrito como invariante e quebrou sozinho em 2026-08-26. O invariante real e que
// o PCE nunca esta a FRENTE do CPI.
ok(D.meta.ultimo_mes_pce <= D.meta.ultimo_mes,
   'e nunca esta a frente do CPI (sai depois, do mesmo mes de referencia)',
   D.meta.ultimo_mes_pce + ' vs ' + D.meta.ultimo_mes);
// Mes FIXO, nao "o ultimo" -- pinar no ultimo mes fez este teste quebrar sozinho
// quando o dado avancou. Mas mes fixo NAO significa valor imutavel: o BEA revisa os
// meses anteriores em cada divulgacao mensal, e junho de 2026 saiu de 131.392 para
// 131.454 entre 20 e 26/08/2026 (conferido no FRED: ele mostra 131.454 tambem, ou
// seja a revisao e do BEA, nao erro nosso).
//
// Entao o que esta assercao protege e o CAMINHO -- payload -> metricSeries -> nivel
// exibido --, nao a veracidade do numero contra o mundo. Essa segunda pergunta mudou
// de lugar: `tests/test_bea_api.py` secao 7 confere as linhas 1 e 374 contra PCEPI e
// PCEPILFE do FRED ao vivo, que e onde da para ter rede. Se ESTA assercao falhar,
// rode aquela antes de suspeitar do relatorio: se a de la passar, foi revisao e o
// numero abaixo e que esta velho.
const MES_ANCORA = '2026-06-01';
function nivelPceEm(key, mes) {
  const s = metricSeries('pce', key, 'SA', 'level');
  const i = s.dates.indexOf(mes);
  if (i < 0) throw new Error('mes ' + mes + ' nao esta na grade do PCE');
  return s.values[i];
}
near(nivelPceEm('1', MES_ANCORA), 131.454, 0.0005,
     'PCE headline em 2026-06 = 131.454 (vintage de 26/08/2026)');
near(nivelPceEm('374', MES_ANCORA), 130.338, 0.0005,
     'PCE core em 2026-06 = 130.338 (vintage de 26/08/2026)');

// M/M e a razao dos niveis, sem atalho.
const lvlPce = metricSeries('pce', '1', 'SA', 'level').values;
const momPce = metricSeries('pce', '1', 'SA', 'mom').values;
const n = lvlPce.length - 1;
near(momPce[n], (lvlPce[n] / lvlPce[n - 1] - 1) * 100, 1e-9,
     'M/M do PCE e exatamente a razao dos niveis');

// O TESTE QUE IMPORTA: as contribuicoes do nivel 1 somam a variacao do headline.
// Exercita weightAt (peso mensal, defasado pelo lag) e o sinal acumulado de uma vez.
const raizPce = D.tabs.pce.tree[0];
ok(raizPce.key === '1' && raizPce.children.length === 2,
   'a raiz do PCE tem 2 filhos (Goods, Services)',
   raizPce.children.map(c => c.label).join(' | '));
const yoyHead = metricSeries('pce', '1', 'SA', 'yoy').values;
const contribN1 = raizPce.children.map(c => metricSeries('pce', c.seriesKey, 'SA', 'contrib').values);
let piorSoma = 0, mesesSoma = 0;
for (let i = lvlPce.length - 60; i < lvlPce.length; i++) {
  if (yoyHead[i] == null) continue;
  let s = 0, falta = false;
  contribN1.forEach(v => { if (v[i] == null) falta = true; else s += v[i]; });
  if (falta) continue;
  mesesSoma++;
  piorSoma = Math.max(piorSoma, Math.abs(s - yoyHead[i]));
}
ok(mesesSoma === 60, 'os 60 ultimos meses todos tem contribuicao nos dois filhos', mesesSoma);
ok(piorSoma <= 0.12,
   'e Goods + Services reconstroem o Y/Y do headline (erro <= 0.12 pp)', piorSoma.toFixed(4));
console.log('          pior erro da soma nivel 1: ' + piorSoma.toFixed(4) + ' pp');

// A contrapartida MENSAL, que so passou a ser observavel quando a metrica existiu.
// Aqui o peso mensal do BEA aparece pelo que ele vale: a contribuicao para o M/M usa
// a participacao do mes ANTERIOR, nao um snapshot de dezembro carregado o ano todo,
// e a reconstrucao fica uma ordem de grandeza melhor que a do CPI. Comparar esta
// linha de log com a do CPI na secao 9 e o ponto -- e por isso que a decomposicao
// mensal e confiavel nesta aba e so indicativa nas outras duas.
const contribMN1 = raizPce.children.map(c => metricSeries('pce', c.seriesKey, 'SA', 'contribm').values);
let piorSomaM = 0, mesesSomaM = 0;
for (let i = lvlPce.length - 60; i < lvlPce.length; i++) {
  if (momPce[i] == null) continue;
  let s = 0, falta = false;
  contribMN1.forEach(v => { if (v[i] == null) falta = true; else s += v[i]; });
  if (falta) continue;
  mesesSomaM++;
  piorSomaM = Math.max(piorSomaM, Math.abs(s - momPce[i]));
}
ok(mesesSomaM === 60, 'os mesmos 60 meses tem contribuicao M/M nos dois filhos', mesesSomaM);
ok(piorSomaM <= 0.01,
   'e Goods + Services reconstroem o M/M do headline (erro <= 0.01 pp)', piorSomaM.toFixed(4));
console.log('          pior erro da soma M/M nivel 1: ' + piorSomaM.toFixed(4) + ' pp');

// Os pesos do nivel 1 somam 100% -- com o sinal ja embutido.
const iUlt = D.tabs.pce.dates.SA.length - 1;
const somaW = raizPce.children.reduce((a, c) => a + D.tabs.pce.weights[c.seriesKey][iUlt], 0);
near(somaW, 100, 0.02, 'os pesos de Goods + Services somam 100% do PCE');

// As 19 linhas que subtraem: peso negativo, e o flag no no.
function acharNo(tree, key) {
  for (const nd of tree || []) {
    if (nd.key === key) return nd;
    const f = acharNo(nd.children, key);
    if (f) return f;
  }
  return null;
}

// 19 linhas SUBTRAEM (sinal acumulado -1) mas 20 pesos saem negativos: a linha 16,
// `Employee reimbursement`, tem despesa nominal negativa por conta propria (-1.735
// US$ mi), com sinal +1. Peso negativo nao e sinonimo de linha "Less:".
const negativos = Object.keys(D.tabs.pce.weights).filter(k => D.tabs.pce.weights[k][iUlt] < 0);
ok(negativos.length === 20, '20 pesos saem negativos no ultimo mes', negativos.length);
function contaNegativos(tree) {
  return (tree || []).reduce((a, nd) =>
    a + (nd.negativo ? 1 : 0) + contaNegativos(nd.children), 0);
}
ok(contaNegativos(D.tabs.pce.tree) === 19,
   'mas so 19 nos estao marcados como negativos por SINAL', contaNegativos(D.tabs.pce.tree));
ok(acharNo(D.tabs.pce.tree, '16') && !acharNo(D.tabs.pce.tree, '16').negativo,
   'e a 20a (Employee reimbursement) nao esta: o negativo dela e a despesa, nao o sinal');
const noLess = acharNo(D.tabs.pce.tree, '356');  // Less: Receipts from sales... (NPISH)
ok(noLess && noLess.negativo === 1, 'a linha 356 (Less: Receipts...) esta marcada negativa');
const noHerdado = acharNo(D.tabs.pce.tree, '357');  // filho dela, sem "Less:" no rotulo
ok(noHerdado && noHerdado.negativo === 1 && noHerdado.label.indexOf('Less:') === -1,
   'e um filho dela herda o sinal sem dizer "Less:" no rotulo', noHerdado && noHerdado.label);
ok(D.tabs.pce.weights['357'][iUlt] < 0,
   'o peso desse filho vem negativo no payload', D.tabs.pce.weights['357'][iUlt]);

// As 2 linhas de net: tem peso, nao tem indice.
const noNet = acharNo(D.tabs.pce.tree, '145');
ok(noNet && noNet.noIndex === 1, 'a linha 145 (Net expenditures abroad) esta marcada sem indice');
ok(metricSeries('pce', '145', 'SA', 'level').values.every(v => v == null),
   'e nenhum mes dela tem indice');
ok(D.tabs.pce.weights['145'][iUlt] != null, 'mas ela tem peso (o BEA publica a despesa)');

// O bloco de addenda: achatado, sem serie propria no cabecalho.
const grupoAdd = D.tabs.pce.tree[D.tabs.pce.tree.length - 1];
ok(grupoAdd.key === 'ADDENDA' && grupoAdd.noSeries === 1,
   'o ultimo no raiz e o cabecalho sintetico de addenda, sem serie');
ok(grupoAdd.children.length === 34, 'com os 34 agregados dentro', grupoAdd.children.length);
ok(grupoAdd.children.every(c => !c.children),
   'nenhum deles ganhou filho -- o bloco e achatado de proposito');
ok(grupoAdd.children.every(c => c.special === 1), 'e todos vem marcados como agregado');

// A tabela renderizada.
const linhasPce = el('pce-table-body').children;
ok(linhasPce.length === 4,
   'a tabela do PCE abre com 4 linhas: o bloco de addenda vem colapsado', linhasPce.length);
const trRaiz = linhasPce[0];
ok(trRaiz.children.length === 14, 'linha = check + label + 12 meses', trRaiz.children.length);
const cabPce = el('pce-table-head').children[0];
ok(cabPce.children[1].textContent === 'Type of product',
   'o cabecalho da coluna de rotulo e o do PCE', cabPce.children[1].textContent);
const trAdd = linhasPce[linhasPce.length - 1];
ok(trAdd.children[0].children.length === 0,
   'o cabecalho de addenda nao renderiza checkbox');
ok(trRaiz.children[0].children.length === 1,
   'mas uma linha de serie renderiza');
ok((trAdd.children[1].title || '').indexOf('heading') > 0,
   'e o hover dele diz que e cabecalho', trAdd.children[1].title);
// Expandir mostra os 34, e ai sim eles tem checkbox.
trAdd.children[1].children[0].click();
ok(el('pce-table-body').children.length === 38,
   'expandir addenda traz os 34 para a tabela', el('pce-table-body').children.length);
const trAgg = el('pce-table-body').children[37];
ok(trAgg.children[0].children.length === 1, 'e cada agregado tem checkbox proprio');
ok((trAgg.children[1].title || '').indexOf('never be summed together') > 0,
   'e o hover deles avisa que se sobrepoem', trAgg.children[1].title);
el('pce-table-body').children[3].children[1].children[0].click();  // recolhe

// A pill NSA e desabilitada e clicar nela nao muda nada.
const pillNSA = pills['pce-basis-group'].find(x => x.dataset.basis === 'NSA');
ok(pillNSA.classList.contains('disabled'), 'a pill NSA do PCE nasce desabilitada');
const antes = el('pce-table-body').children[0].children[13].textContent;
pillNSA.click();
ok(pillNSA.classList.contains('active') === false,
   'clicar nela nao a ativa');
ok(el('pce-table-body').children[0].children[13].textContent === antes,
   'e a tabela nao muda', el('pce-table-body').children[0].children[13].textContent);

// Trocar de metrica na aba de PCE re-renderiza.
pills['pce-metric-group'].find(x => x.dataset.metric === 'contrib').click();
ok(reactCalls[reactCalls.length - 1].div === 'chart-pce',
   'trocar para contribuicao redesenhou o grafico do PCE',
   reactCalls[reactCalls.length - 1].div);
ok(reactCalls[reactCalls.length - 1].layout.yaxis.title.text === 'p.p. of headline Y/Y',
   'com o titulo de eixo da contribuicao',
   reactCalls[reactCalls.length - 1].layout.yaxis.title.text);
pills['pce-metric-group'].find(x => x.dataset.metric === 'yoy').click();

// O apendice recebeu os dois numeros do PCE.
ok(String(el('ap-pce-folhas').textContent) === String(D.meta.n_pce_folhas),
   'o apendice recebeu a contagem de folhas do PCE', el('ap-pce-folhas').textContent);
ok(el('ap-pce-mes').textContent === D.meta.ultimo_mes_pce,
   'e o ultimo mes do PCE', el('ap-pce-mes').textContent);
}


console.log('\n=== 15. as duas arvores num seletor =========================');
{
// (ii) do pedido: a arvore de despesa deixou de ser uma ABA e virou uma VISAO da
// mesma tabela. O que este bloco protege e o que a fusao pode quebrar em silencio:
// o cabecalho tem de andar com o seletor, e as marcas tem de ser POR ARVORE -- as
// duas chamam All items de SA0, entao um mapa `checked` compartilhado carregaria
// uma selecao para dentro de uma arvore onde ela significa outra coisa.
ok(html.indexOf('data-tab="expenditure"') === -1, 'a aba Expenditure Tree nao existe mais');
ok(html.indexOf('id="panel-expenditure"') === -1, 'nem o painel dela');
ok(html.indexOf('data-tab="cpi"') > 0, 'e ha uma aba CPI no lugar das duas');
ok(pills['cpi-tree-group'].length === 2, 'o seletor de arvore tem as duas', pills['cpi-tree-group'].length);

// Trocar de arvore redesenha a tabela E avisa as duas secoes abaixo, entao a ULTIMA
// chamada do Plotly e a do drill-down, nao a da tabela. Ler reactCalls[last] aqui
// mediria o grafico errado -- foi o que aconteceu na primeira rodada.
function ultimoCpi() {
  const cs = reactCalls.filter(c => c.div === 'chart-cpi');
  return cs[cs.length - 1];
}

pills['cpi-metric-group'].find(p => p.dataset.metric === 'yoy').click();
ok(el('cpi-h2').textContent.indexOf('Release tree') === 0,
   'o cabecalho comeca na arvore de divulgacao', el('cpi-h2').textContent);
ok(el('cpi-note').innerHTML.indexOf(String(D.meta.n_release_drill)) > 0,
   'e a nota dele traz o numero de linhas de drill-down');
ok(el('cpi-table-head').children[0].children[1].textContent === 'Expenditure category',
   'o rotulo da coluna de nome e o da arvore ativa',
   el('cpi-table-head').children[0].children[1].textContent);

// Marca uma linha a mais na arvore de divulgacao -- uma acao do usuario, nao o
// default -- para depois provar que ela sobreviveu a ida e volta.
function marcarLinha(bodyId, i, on) {
  const cb = el(bodyId).children[i].children[0].children[0];
  cb.checked = on;
  cb.fire('change');
}
marcarLinha('cpi-table-body', 0, true);   // All items
const nRel = ultimoCpi().traces.length;
ok(nRel === 4, 'com All items marcado a mais, a arvore de divulgacao plota 4', nRel);

pills['cpi-tree-group'].find(p => p.dataset.tree === 'expenditure').click();
ok(el('cpi-h2').textContent.indexOf('Expenditure tree') === 0,
   'trocar de arvore trocou o cabecalho', el('cpi-h2').textContent);
ok(el('cpi-note').innerHTML.indexOf(String(D.meta.n_expenditure)) > 0,
   'e a nota', el('cpi-note').innerHTML.slice(0, 60));
ok(el('cpi-table-head').children[0].children[1].textContent === 'Item',
   'e o rotulo da coluna', el('cpi-table-head').children[0].children[1].textContent);
const grafExp = ultimoCpi();
ok(reactCalls[reactCalls.length - 1].div === 'chart-cpi-drill',
   'trocar de arvore redesenha tambem o drill-down -- ele segue o seletor',
   reactCalls[reactCalls.length - 1].div);
ok(grafExp.traces.length === 4,
   'e plota as 4 marcas proprias da arvore de despesa, nao as 4 da outra',
   grafExp.traces.map(x => x.name).join(' | '));
ok(el('cpi-table-body').children.length === 9,
   'a raiz da arvore de despesa abre nos 8 grupos de nivel 1', el('cpi-table-body').children.length);

pills['cpi-tree-group'].find(p => p.dataset.tree === 'release').click();
ok(ultimoCpi().traces.length === 4,
   'voltar devolve a selecao da arvore de divulgacao intacta -- as marcas sao por arvore',
   ultimoCpi().traces.length);
marcarLinha('cpi-table-body', 0, false);  // desmarca All items de volta
ok(ultimoCpi().traces.length === 3, 'e desmarcar volta a 3');
}

console.log('\n=== 16. tabela de maiores contribuicoes =====================');
{
// O fato que decidiu a formula da coluna Contribution, e que vale ficar preso num
// teste: OUTUBRO DE 2025 NAO FOI DIVULGADO (paralisacao do governo americano). E o
// unico buraco da base, e apaga DOIS passos mensais -- o proprio e o de novembro --,
// entao somar contribuicoes mes a mes numa janela de 12 deixaria a coluna inteira em
// branco. A janela e razao dos extremos por causa disto.
const iOut = D.tabs.release.dates.NSA.indexOf('2025-10-01');
ok(iOut > 0, 'outubro de 2025 esta na grade', iOut);
const nivelRel = metricSeries('release', 'SA0', 'NSA', 'level').values;
ok(nivelRel[iOut] == null, 'mas o headline nao tem indice nesse mes -- o CPI nao saiu');
ok(nivelRel[iOut - 1] != null && nivelRel[iOut + 1] != null,
   'e os vizinhos tem: e um mes so, nao o fim da serie');
const momRel = metricSeries('release', 'SA0', 'NSA', 'mom').values;
ok(momRel[iOut] == null && momRel[iOut + 1] == null,
   'um indice faltando apaga dois M/M -- o do mes e o do seguinte');
ok(metricSeries('release', 'SA0', 'NSA', 'yoy').values[iOut + 1] != null,
   'mas o Y/Y de novembro sobrevive: ele so precisa das duas pontas');

// (iii) do pedido: o equivalente do "Maiores Contribuições no Período" do Brasil.
// A ancora fica em NSA e 12 meses, que e o corte publicado -- assim o numero do
// rodape tem contra o que ser conferido.
pills['cpi-basis-group'].find(p => p.dataset.basis === 'NSA').click();
pills['cpi-window-group'].find(p => p.dataset.win === '12').click();

const cab = el('cpi-rank-head').children[0];
ok(cab.children.length === 7, '7 colunas', cab.children.length);
ok(cab.children.map(x => x.textContent).join('|') ===
   '#|Level 1|Parent|Item|Weight|Change 12M (%)|Contribution (p.p.)',
   'com os rotulos do ranking', cab.children.map(x => x.textContent).join('|'));
ok(el('cpi-rank-body').children.length === 20, 'mostra 20 linhas', el('cpi-rank-body').children.length);

function col(tr, i) { return parseFloat(tr.children[i].textContent); }
const contribs = el('cpi-rank-body').children.map(tr => col(tr, 6)).filter(v => !isNaN(v));
ok(contribs.length === 20 && contribs.every((v, i) => i === 0 || contribs[i - 1] >= v - 1e-9),
   'ordenadas por contribuicao decrescente', contribs.slice(0, 3).join(' '));

// Cobertura: nas folhas ela NAO chega a 100, e e por isso que a linha existe.
const coberturaFolhas = el('cpi-rank-cover').innerHTML;
ok(coberturaFolhas.indexOf('of the index') > 0 && coberturaFolhas.indexOf('coverage, not error') > 0,
   'o rodape declara a cobertura e avisa que a diferenca nao e erro');
const pesoFolhas = parseFloat((coberturaFolhas.match(/<b>([\d.]+)<\/b> of the index/) || [])[1]);
ok(pesoFolhas > 0 && pesoFolhas < 99,
   'e nas folhas da arvore de divulgacao ela fica claramente abaixo de 100', pesoFolhas);
console.log('          [medido] cobertura das folhas: ' + pesoFolhas.toFixed(1) + ' de 100');

// "Show all" abre a lista inteira e volta.
const btn = el('cpi-rank-toggle');
btn.click();
const todas = el('cpi-rank-body').children.length;
ok(todas > 20, 'Show all abre a lista inteira', todas);
ok(btn.textContent.indexOf('Show top') === 0, 'e o botao passa a oferecer a volta', btn.textContent);
btn.click();
ok(el('cpi-rank-body').children.length === 20, 'e volta para 20');

// A janela muda o cabecalho e os numeros.
pills['cpi-window-group'].find(p => p.dataset.win === '1').click();
ok(el('cpi-rank-head').children[0].children[5].textContent === 'Change 1M (%)',
   'trocar a janela renomeia a coluna de variacao',
   el('cpi-rank-head').children[0].children[5].textContent);
ok(el('cpi-rank-h2').textContent.indexOf('over 1M') > 0,
   'e o titulo da secao', el('cpi-rank-h2').textContent);
pills['cpi-window-group'].find(p => p.dataset.win === '12').click();

// O TESTE QUE IMPORTA: no nivel 1 a arvore particiona, entao peso e contribuicao
// tem contra o que fechar. A contribuicao no periodo e a SOMA das 12 contribuicoes
// mensais -- nao peso x variacao acumulada --, e o que se confere aqui e que essa
// soma reconstroi a variacao de 12 meses do headline.
const pillL1 = el('cpi-rank-level-group').children.filter(b => b.textContent === 'Level 1')[0];
ok(!!pillL1, 'ha uma pill de Level 1');
pillL1.click();
const linhas = el('cpi-rank-body').children;
ok(linhas.length === 3,
   'o nivel 1 da arvore de divulgacao tem 3 linhas (food, energy, core)', linhas.length);
const somaPeso = linhas.reduce((a, tr) => a + col(tr, 4), 0);
near(somaPeso, 100, 0.01, 'os pesos das 3 somam 100 -- o nivel 1 particiona o indice');
const somaContrib = linhas.reduce((a, tr) => a + col(tr, 6), 0);
const headline12 = pctBetween('release', 'SA0', 'NSA', mRef, mYr);
console.log(`          [medido] soma das contribuicoes de nivel 1: ${somaContrib.toFixed(3)} vs ` +
            `headline ${headline12.toFixed(3)}%`);
// A tolerancia e o erro de reconciliacao ja documentado da convencao de peso do CPI
// (a importancia relativa e snapshot de dezembro de um numero que o BLS atualiza a
// preco continuamente), nao folga: ~0.012 p.p. em media, 0.036 medido aqui. Apertar
// mais faria o teste quebrar sozinho a cada mes novo; afrouxar deixaria passar um
// peso trocado.
near(somaContrib, headline12, 0.10,
     'e as contribuicoes de nivel 1 reconstroem a variacao de 12 meses do headline');
const cobertura1 = parseFloat((el('cpi-rank-cover').innerHTML.match(/<b>([\d.]+)<\/b> of the index/) || [])[1]);
near(cobertura1, 100, 0.01, 'e a linha de cobertura diz 100 quando a cobertura e mesmo 100');

// Ordenar: primeiro clique numa coluna de texto sobe, numa de numero desce.
cab.children[3].click();  // Item
const nomes = el('cpi-rank-body').children.map(tr => tr.children[3].textContent);
ok(nomes.every((v, i) => i === 0 || nomes[i - 1] <= v),
   'clicar em Item ordena A-Z', nomes.join(' | '));
cab.children[3].click();
const nomes2 = el('cpi-rank-body').children.map(tr => tr.children[3].textContent);
ok(nomes2.every((v, i) => i === 0 || nomes2[i - 1] >= v), 'e o segundo clique inverte');
cab.children[6].click();  // Contribution, volta ao default
const c2 = el('cpi-rank-body').children.map(tr => col(tr, 6));
ok(c2.every((v, i) => i === 0 || c2[i - 1] >= v - 1e-9), 'e a coluna numerica volta a descer');

// Trocar de arvore refaz a secao (o CPI_TAB avisa).
pills['cpi-tree-group'].find(p => p.dataset.tree === 'expenditure').click();
const l1exp = el('cpi-rank-level-group').children.filter(b => b.textContent === 'Level 1')[0];
l1exp.click();
ok(el('cpi-rank-body').children.length === 8,
   'na arvore de despesa o nivel 1 tem os 8 grupos -- a secao seguiu o seletor',
   el('cpi-rank-body').children.length);
const somaPesoExp = el('cpi-rank-body').children.reduce((a, tr) => a + col(tr, 4), 0);
near(somaPesoExp, 100, 0.01, 'e os 8 pesos tambem somam 100');
pills['cpi-tree-group'].find(p => p.dataset.tree === 'release').click();
}

console.log('\n=== 17. drill-down de 12 meses =============================');
{
// (iv) do pedido: a replica do "Variação 12M — Drilldown de Componentes". A
// diferenca que importa esta na ultima assercao -- no Brasil o agregado de um nivel
// e RECONSTRUIDO (media ponderada encadeada), aqui e o indice publicado do proprio
// no, entao o valor plotado tem de bater EXATO com metricSeries, sem tolerancia.
const pillsNivel = el('cpi-drill-level-group').children;
ok(pillsNivel.length >= 3 && pillsNivel[0].textContent === 'Level 1',
   'pills de nivel, comecando no 1', pillsNivel.map(b => b.textContent).join(','));
ok(pillsNivel[0].classList.contains('active'), 'e o nivel 1 nasce ativo');

function ultimoDrill() {
  const cs = reactCalls.filter(c => c.div === 'chart-cpi-drill');
  return cs[cs.length - 1];
}
const g = ultimoDrill();
ok(!!g, 'o grafico do drill-down foi plotado');
ok(g.traces.length === 3, 'nasce com 3 componentes marcados', g.traces.length);
ok(g.layout.yaxis.title.text.indexOf('% Y/Y') === 0,
   'o eixo Y diz Y/Y e o ajuste', g.layout.yaxis.title.text);
ok(g.layout.dragmode === 'pan' && g.config.scrollZoom === true,
   'e o grafico segue o modelo de interacao da pagina');

const nivel1 = D.tabs.release.tree[0].children;
ok(g.traces.map(x => x.name).join('|') === nivel1.slice(0, 3).map(n => n.label).join('|'),
   'os 3 sao os primeiros componentes do nivel -- food / energy / core',
   g.traces.map(x => x.name).join('|'));

// O valor plotado E o do indice publicado, nao uma reconstrucao.
const pub = metricSeries('release', nivel1[0].seriesKey, 'NSA', 'yoy');
const iPub = pub.values.length - 1;
ok(g.traces[0].y[iPub] === pub.values[iPub] && g.traces[0].x[iPub] === pub.dates[iPub],
   'e e exatamente o Y/Y do indice publicado do no, sem reconstrucao',
   g.traces[0].y[iPub] + ' vs ' + pub.values[iPub]);

// Uma serie so sai preenchida; varias, nao.
const caixas = el('cpi-drill-panel').children.map(lab => lab.children[0]);
ok(caixas.length === nivel1.length, 'o painel lista todos os componentes do nivel', caixas.length);
caixas[1].checked = false; caixas[1].fire('change');
caixas[2].checked = false; caixas[2].fire('change');
const g1 = ultimoDrill();
ok(g1.traces.length === 1, 'desmarcar deixa uma serie', g1.traces.length);
ok(g1.traces[0].fill === 'tozeroy', 'e uma serie sozinha sai preenchida ate o zero', g1.traces[0].fill);
ok(el('cpi-drill-btn').textContent === nivel1[0].label,
   'o botao do multiselect passa a mostrar o nome dela', el('cpi-drill-btn').textContent);
caixas[1].checked = true; caixas[1].fire('change');
ok(!ultimoDrill().traces.some(x => x.fill), 'com duas, nenhuma e preenchida');
ok(el('cpi-drill-btn').textContent.indexOf('2 of ') === 0,
   'e o botao passa a contar', el('cpi-drill-btn').textContent);

// Trocar de nivel repovoa a lista.
const pillN2 = pillsNivel.filter(b => b.textContent === 'Level 2')[0];
pillN2.click();
ok(el('cpi-drill-panel').children.length === nodesAtDepth(D.tabs.release.tree, 2).length,
   'trocar de nivel repovoa o painel com os componentes daquele nivel',
   el('cpi-drill-panel').children.length);
ok(ultimoDrill().traces.length === 3, 'e volta a marcar 3', ultimoDrill().traces.length);

// Clear esvazia sem quebrar.
el('cpi-drill-clear').click();
ok(ultimoDrill().traces.length === 0, 'Clear tira todas as series', ultimoDrill().traces.length);
ok(el('cpi-drill-btn').textContent === 'Select…', 'e o botao volta ao placeholder',
   el('cpi-drill-btn').textContent);

// A barra de range do drill-down e propria.
relayoutCalls.length = 0;
const rbDrill = el('cpi-drill-range').children.filter(c => c.className === 'rb');
ok(rbDrill.length === 6, 'o drill-down tem a sua propria barra de range', rbDrill.length);
rbDrill[0].click();
ok(relayoutCalls.length === 1 && relayoutCalls[0].div === 'chart-cpi-drill',
   'e ela mexe no grafico dele, nao no de cima', relayoutCalls[0] && relayoutCalls[0].div);
}

// ── faixa de agenda de divulgacao ────────────────────────────────────────────
// O que esta secao protege: a faixa mistura dado do payload (data, hora nos dois
// fusos, periodo) com uma conta feita no NAVEGADOR (o "in N days"), e as duas
// falham de jeitos diferentes. Um payload sem `releases` tem de sumir com a faixa
// em vez de renderizar uma caixa vazia; e a contagem tem de ser contra o relogio
// de quem abre, senao um arquivo enviado por email mente com confianca.
console.log('\n-- agenda de divulgacao ------------------------------------');
{
const faixa = el('releases').innerHTML;

ok(D.releases && D.releases.inflc_cpi && D.releases.inflc_pce,
   'o payload traz a agenda das duas series', Object.keys(D.releases || {}));

const cpi = D.releases.inflc_cpi;
ok(cpi.institution === 'BLS' && cpi.grupo === 'bls_cpi',
   'o CPI vem do grupo bls_cpi do calendario', cpi.institution + '/' + cpi.grupo);
ok(D.releases.inflc_pce.institution === 'BEA' && D.releases.inflc_pce.grupo === 'bea_pce',
   'e o PCE do grupo bea_pce', D.releases.inflc_pce.grupo);

ok(faixa.indexOf('CPI · ') >= 0 && faixa.indexOf('PCE · ') >= 0,
   'a faixa renderizou os dois cartoes');
ok((faixa.match(/class="rel-row/g) || []).length === 4,
   'com ultima e proxima em cada um', (faixa.match(/class="rel-row/g) || []).length);

// A hora sai nos DOIS fusos. E o ponto todo de guardar release_time_tz em vez de
// um valor ja convertido: as 08:30 de Nova York nao sao a mesma hora de Brasilia o
// ano inteiro.
ok(faixa.indexOf(cpi.proxima.time_fonte + ' ET') >= 0,
   'a hora da fonte aparece marcada como ET', cpi.proxima.time_fonte);
ok(faixa.indexOf(cpi.proxima.time_local + ' BRT') >= 0,
   'e a convertida como BRT', cpi.proxima.time_local);
ok(cpi.proxima.tz_fonte === 'America/New_York',
   'o fuso guardado e o da fonte, nao o local', cpi.proxima.tz_fonte);

// A conversao tem de mudar com o horario de verao americano. Verificado sobre o
// proprio payload: se as duas divulgacoes caem em regimes diferentes de DST, a
// diferenca fonte->local nao pode ser a mesma nas duas.
function difMin(e) {
  const f = e.time_fonte.split(':'), l = e.time_local.split(':');
  return (+l[0] * 60 + +l[1]) - (+f[0] * 60 + +f[1]);
}
ok(difMin(cpi.proxima) === 60 || difMin(cpi.proxima) === 120,
   'a diferenca ET->BRT e de 1h (EDT) ou 2h (EST), nunca zero', difMin(cpi.proxima));

// Periodo de referencia: e o mes do DADO, nao o da divulgacao. E a distincao que
// separa "o CPI de agosto" de "o CPI que sai em setembro".
ok(cpi.proxima.reference_period < cpi.proxima.date.slice(0, 7),
   'o periodo de referencia antecede o mes da divulgacao',
   cpi.proxima.reference_period + ' vs ' + cpi.proxima.date.slice(0, 7));
ok(faixa.indexOf('ref. ') >= 0, 'e a faixa mostra o periodo, nao so a data');

// A conta de dias e contra o relogio de quem abre o arquivo.
const hoje = new Date();
const hojeISO = hoje.getFullYear() + '-' +
  String(hoje.getMonth() + 1).padStart(2, '0') + '-' +
  String(hoje.getDate()).padStart(2, '0');
const esperado = cpi.proxima.date < hojeISO ? 'past due' :
                 cpi.proxima.date === hojeISO ? 'today' : 'in ';
ok(faixa.indexOf(esperado) >= 0,
   'o badge da proxima reflete o relogio de agora (' + esperado.trim() + ')');
ok(faixa.indexOf('rel-row next') >= 0, 'e a linha da proxima esta marcada como tal');

// Payload sem agenda: a faixa some, nao renderiza caixa vazia.
const guardado = D.releases;
D.releases = {};
el('releases').innerHTML = '';
el('releases').style.display = '';
(function() {
  var alvo = el('releases');
  var R = D.releases || {};
  var ordem = [['inflc_cpi', 'CPI'], ['inflc_pce', 'PCE']];
  var html = '';
  ordem.forEach(function(par) { if (R[par[0]]) html += 'x'; });
  alvo.innerHTML = html;
  if (!html) alvo.style.display = 'none';
})();
ok(el('releases').style.display === 'none',
   'sem agenda no payload a faixa e escondida');
D.releases = guardado;
}

console.log('\n=== 18. o apendice em gavetas ==============================');
{
// O apendice era oito <h3> empilhados: ~2.700 palavras sem estado fechado nenhum.
// Agora cada secao e um <details>, e o resumo ao lado do titulo e o que faz o
// fechado valer -- as oito juntas viram um indice do que esta documentado.
ok(drawerIds.length === 8, 'o apendice tem 8 gavetas', drawerIds.length);
const esperados = ['ap-sources', 'ap-calendar', 'ap-trees', 'ap-numbers',
                   'ap-weights', 'ap-readings', 'ap-pce', 'ap-limits'];
ok(esperados.every(id => drawerIds.indexOf(id) >= 0),
   'com os ids que os links do relatorio usam', drawerIds.join(','));

const i0 = html.indexOf('<section class="panel" id="panel-appendix">');
const apx = html.slice(i0, html.indexOf('</section>', i0));
ok(apx.indexOf('<h3>') < 0, 'nenhum <h3> sobrou solto la dentro');
ok((apx.match(/<summary>/g) || []).length === 8, 'cada gaveta tem um summary');
ok((apx.match(/class="acc-t"/g) || []).length === 8, 'com titulo');
ok((apx.match(/class="acc-s"/g) || []).length === 8,
   'e o resumo de uma linha, que e o que o leitor le antes de decidir abrir');
ok((apx.match(/<details class="acc" id="[\w-]+" open>/g) || []).length === 1,
   'so a primeira nasce aberta -- as outras sete sao indice');
ok(html.indexOf('.appx h3 {') < 0, 'e a regra de CSS do <h3> saiu junto, sem seletor morto');

// Os tres numeros que o script escreve no apendice continuam la, agora dentro de
// gavetas -- um <span> perdido na reorganizacao ficaria vazio em silencio.
['ap-ri-n', 'ap-pce-folhas', 'ap-pce-mes'].forEach(id => {
  ok(apx.indexOf('id="' + id + '"') >= 0, 'o span ' + id + ' segue no apendice');
});
ok(String(el('ap-ri-n').textContent).length > 0,
   'e o script continua preenchendo ap-ri-n', el('ap-ri-n').textContent);
ok(String(el('ap-pce-folhas').textContent).length > 0,
   'e ap-pce-folhas', el('ap-pce-folhas').textContent);

// Todo link do relatorio aponta para uma gaveta que existe. Sem isto, renomear
// uma secao deixaria um link mudo -- clica e nao acontece nada.
// Dois formatos, de proposito: os links escritos no HTML chamam goAppendix
// direto, e os que nascem dentro de string JS passam por axLink. O teste varre
// os dois -- varrer so um deixaria metade das referencias sem cobertura.
const alvos = [
  ...html.matchAll(/goAppendix\((?:&#39;|')([\w-]+)(?:&#39;|')\)/g),
  ...html.matchAll(/axLink\('([\w-]+)'/g),
].map(m => m[1]);
ok(alvos.length >= 6, 'ha links para o apendice espalhados pelo relatorio', alvos.length);
const orfaos = alvos.filter(a => drawerIds.indexOf(a) < 0);
ok(orfaos.length === 0, 'e nenhum aponta para gaveta inexistente', orfaos.join(','));
const cobertos = new Set(alvos);
['ap-trees', 'ap-numbers', 'ap-weights', 'ap-readings', 'ap-pce', 'ap-calendar'].forEach(id => {
  ok(cobertos.has(id), 'a secao ' + id + ' e alcancavel por link');
});
// As duas que sobram sao de proposito: 'onde vem o dado' e 'limites' nao respondem
// a nenhuma afirmacao especifica da pagina, entao nenhum ponto do relatorio tem um
// lugar natural para apontar. Fixado aqui para nao parecer descuido depois.
const semLink = drawerIds.filter(id => !cobertos.has(id));
ok(semLink.length === 2 && semLink.indexOf('ap-sources') >= 0 && semLink.indexOf('ap-limits') >= 0,
   'e so ap-sources e ap-limits ficam sem link de entrada, por nao terem referente',
   semLink.join(','));

// O destino de 'so os niveis 0-2 particionam o indice' e a gaveta que documenta a
// afirmacao (ap-numbers, onde vive o aviso), nao a que explica como a arvore e
// montada -- a primeira versao apontava para a errada.
ok(html.indexOf("axLink('ap-numbers', 'why that matters')") >= 0,
   'a nota da arvore de divulgacao aponta a particao para ap-numbers');

// axLink e o unico gerador desses links no JS, e escapa a aspa com entidade
// porque o onclick vive dentro de uma string JS ja delimitada por aspas simples.
const marcado = axLink('ap-limits', 'Appendix');
ok(marcado.indexOf('goAppendix(&#39;ap-limits&#39;)') >= 0,
   'axLink escapa a aspa com &#39;, para caber dentro do atributo onclick', marcado);
ok(marcado.indexOf('class="axlink"') >= 0, 'e marca o link com a classe que o CSS estiliza');

// goAppendix faz as duas coisas de uma vez: troca de aba E abre a gaveta.
el('ap-limits').open = false;
tabButtons.forEach(b => b.classList.remove('active'));
panelIds.forEach(id => el(id).classList.remove('active'));
const devolveu = goAppendix('ap-limits');
ok(devolveu === false, 'goAppendix devolve false, para o clique nao navegar');
ok(el('ap-limits').open === true, 'a gaveta alvo abre');
ok(el('ap-limits').classList.contains('flash'),
   'e pisca -- cair numa gaveta ja aberta seria indistinguivel de nada ter acontecido');
ok(tabButtons.find(b => b.dataset.tab === 'appendix').classList.contains('active'),
   'a aba do apendice fica ativa');
ok(el('panel-appendix').classList.contains('active'), 'com o painel dela ligado');
ok(!el('panel-cpi').classList.contains('active'), 'e o painel de CPI desligado');

// Um id que nao existe nao pode derrubar a pagina: o link ainda troca de aba.
tabButtons.forEach(b => b.classList.remove('active'));
ok(goAppendix('ap-nao-existe') === false, 'um id inexistente nao lanca excecao');
ok(tabButtons.find(b => b.dataset.tab === 'appendix').classList.contains('active'),
   'e a troca de aba acontece assim mesmo');

// Expand all / Collapse all, que e o que fazer antes de imprimir.
el('appx-collapse').click();
ok(drawerIds.every(id => el(id).open === false), 'Collapse all fecha as oito');
el('appx-expand').click();
ok(drawerIds.every(id => el(id).open === true), 'Expand all abre as oito');

// mostrarAba foi extraida do handler de clique; o clique tem de continuar usando-a.
tabButtons.find(b => b.dataset.tab === 'pce').click();
ok(el('panel-pce').classList.contains('active'),
   'clicar na aba de PCE continua ligando o painel dela');
ok(!el('panel-appendix').classList.contains('active'), 'e desligando o do apendice');
tabButtons.find(b => b.dataset.tab === 'cpi').click();
ok(el('panel-cpi').classList.contains('active'), 'e voltar para CPI religa o de cima');
}

console.log('\n=== 19. conformidade com o design system da skill ===========');
{
// .claude/skills/lis-dashboard/references/design-system.md. So as regras que valem
// para um relatorio analitico multi-serie -- as do genero "dashboard de NAV de um
// ativo so" (3 stat cards min/max, spline navy unica com fill, virgula decimal BR)
// nao se aplicam e estao registradas no CLAUDE.md da pasta.
ok(html.indexOf('cdn.plot.ly/plotly-2.35.2.min.js') >= 0,
   'Plotly 2.35.2, a versao que os outros oito relatorios usam');
['chart.js', 'chartjs-plugin', 'hammer.min.js'].forEach(lib => {
  ok(html.toLowerCase().indexOf(lib) < 0, 'sem ' + lib + ' -- so Plotly');
});
ok(html.indexOf('<canvas') < 0, 'nenhum <canvas>: todo grafico e um <div> vazio');
['Barlow', 'Barlow+Condensed', 'JetBrains+Mono'].forEach(f => {
  ok(html.indexOf(f) >= 0, 'a fonte ' + f.replace('+', ' ') + ' esta no link do Google Fonts');
});

// Config unico, nao copiado por grafico.
ok(PLOTLY_CONFIG.scrollZoom === true, 'scrollZoom ligado no config compartilhado');
ok(PLOTLY_CONFIG.displayModeBar === 'hover',
   'a modebar aparece no hover, para nao competir com os botoes de janela',
   PLOTLY_CONFIG.displayModeBar);
ok(PLOTLY_CONFIG.displaylogo === false, 'sem logo do Plotly');
ok(['lasso2d', 'select2d', 'autoScale2d'].every(b => PLOTLY_CONFIG.modeBarButtonsToRemove.indexOf(b) >= 0),
   'lasso/select/autoScale removidos da modebar');
const cfgs = new Set(reactCalls.map(c => c.config));
ok(cfgs.size === 1 && cfgs.has(PLOTLY_CONFIG),
   'e os tres graficos passam O MESMO objeto -- um config so, nao um por renderizador',
   cfgs.size);

// Layout: a fabrica unica cobre gesto, hover, eixos e fundo.
const L = mkLayout();
ok(L.dragmode === 'pan', 'dragmode pan (drag = pan nos dois eixos, sem box-zoom)');
ok(L.hovermode === 'x unified', 'hovermode x unified');
ok(L.hoverlabel.bgcolor === '#1F2853' && L.hoverlabel.font.family === 'Barlow'
   && L.hoverlabel.font.size === 12, 'tooltip navy em Barlow 12');
ok(L.xaxis.showgrid === false && L.xaxis.showline === true
   && L.xaxis.linecolor === 'rgba(31,40,83,0.1)',
   'eixo X sem grid, so linha de base');
ok(L.xaxis.tickfont.family === 'JetBrains Mono' && L.xaxis.tickfont.size === 10
   && L.xaxis.tickfont.color === '#7A88A8', 'ticks do X em JetBrains Mono 10');
ok(L.yaxis.gridcolor === 'rgba(31,40,83,0.06)' && L.yaxis.tickfont.family === 'JetBrains Mono',
   'grid do Y na cor da referencia e ticks em mono');
ok(L.xaxis.fixedrange === undefined && L.yaxis.fixedrange === undefined,
   'sem fixedrange em eixo nenhum -- o Y tem de ficar livre junto com o X');
ok(L.xaxis.rangeselector === undefined,
   'sem xaxis.rangeselector -- os botoes de janela vivem fora do Plotly, ver a ' +
   'caixa de atencao do design system');
ok(L.paper_bgcolor === 'rgba(0,0,0,0)' && L.plot_bgcolor === 'rgba(0,0,0,0)',
   'fundo transparente, o card por baixo e que pinta');
ok(L.font.family.indexOf('Barlow') === 0 && L.font.size === 12, 'fonte base Barlow 12');
// O merge de `extra` nao pode apagar o resto do eixo.
const L2 = mkLayout({yaxis: {title: {text: 'x'}}, barmode: 'relative'});
ok(L2.yaxis.title.text === 'x' && L2.yaxis.gridcolor === 'rgba(31,40,83,0.06)',
   'passar um extra de yaxis funde, nao substitui o eixo inteiro');
ok(L2.barmode === 'relative', 'e chaves de topo passam direto');

// "Values on chart" -- o "Dados no grafico" obrigatorio do design system.
const dl = document.getElementById('chart-cpi-dl');
ok(!!dl && dl.className === 'dl-toggle', 'o toggle existe na barra do grafico');
ok(!dl.classList.contains('on'), 'e comeca DESLIGADO, como manda a referencia');
const marcaTexto = reactCalls.filter(c => c.div === 'chart-cpi').pop();
ok(marcaTexto.traces[0].mode === 'lines', 'entao as traces nascem em mode "lines"');
ok(Array.isArray(marcaTexto.traces[0].text), 'mas ja carregam o array de texto');
ok(marcaTexto.traces[0].textfont.family === 'JetBrains Mono'
   && marcaTexto.traces[0].textfont.size === 9, 'rotulos em JetBrains Mono 9');
// O passo da referencia: >60 pontos a cada 5, >30 a cada 3, senao todos.
ok(passoDeRotulo(1363) === 5 && passoDeRotulo(45) === 3 && passoDeRotulo(20) === 1,
   'o passo de rotulos segue a regra da skill');
const naoVazios = marcaTexto.traces[0].text.filter(x => x !== '').length;
const preenchidos = marcaTexto.traces[0].y.filter(v => v != null && !isNaN(v)).length;
ok(naoVazios < preenchidos / 3,
   'e o passo realmente rareia os rotulos -- ' + naoVazios + ' de ' + preenchidos,
   naoVazios + '/' + preenchidos);
restyleCalls.length = 0;
dl.click();
ok(restyleCalls.length === 1 && restyleCalls[0].upd.mode === 'lines+text',
   'clicar liga os valores por Plotly.restyle, sem re-renderizar o grafico',
   JSON.stringify(restyleCalls[0] && restyleCalls[0].upd));
ok(dl.classList.contains('on'), 'e o botao fica marcado');
dl.click();
ok(restyleCalls[1].upd.mode === 'lines' && !dl.classList.contains('on'),
   'clicar de novo desliga');

// No grafico de contribuicao o toggle e desabilitado de proposito: sao ate 14
// series de barra empilhada, e um numero por segmento nao produz nada legivel.
pills['cpi-metric-group'].find(p => p.dataset.metric === 'contrib').click();
ok(dl.classList.contains('disabled'), 'em modo contribuicao o toggle fica desabilitado');
restyleCalls.length = 0;
dl.click();
ok(restyleCalls.length === 0, 'e clicar nele nao faz nada');
pills['cpi-metric-group'].find(p => p.dataset.metric === 'yoy').click();
ok(!dl.classList.contains('disabled'), 'voltar para uma metrica de linha reabilita');

// Marca e rodape, como nos outros relatorios de analytics/.
ok(html.indexOf('LIS <em>CAPITAL</em>') >= 0, 'o cabecalho traz a marca LIS CAPITAL');
ok(html.indexOf('<footer>') >= 0 && html.indexOf('LIS Capital \u2014 Internal use') >= 0,
   'e ha rodape com as fontes e a marca');
ok(html.indexOf('BLS \u2014 Consumer Price Index') >= 0 && html.indexOf('BEA \u2014 NIPA Section 2') >= 0,
   'o rodape nomeia as duas fontes');
}

console.log('\n' + '='.repeat(62));
console.log(`${oks} ok, ${falhas} falharam`);
process.exit(falhas ? 1 : 0);
