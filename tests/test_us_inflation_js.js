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
    p.classList.add('pill');
    return p;
  });
}
definePills('release-metric-group', 'metric', [
  {name: 'level'}, {name: 'yoy', active: true}, {name: 'mom'}, {name: 'ann3m'}, {name: 'contrib'}]);
definePills('release-basis-group', 'basis', [{name: 'NSA'}, {name: 'SA', active: true}]);
definePills('expenditure-metric-group', 'metric', [
  {name: 'level'}, {name: 'yoy', active: true}, {name: 'mom'}, {name: 'ann3m'}, {name: 'contrib'}]);
definePills('expenditure-basis-group', 'basis', [{name: 'NSA'}, {name: 'SA', active: true}]);

const tabButtons = ['release', 'expenditure', 'appendix'].map(t => {
  const b = makeEl('button'); b.dataset.tab = t; return b;
});

const relayoutCalls = [];
const reactCalls = [];

global.document = {
  getElementById: (id) => el(id),
  createElement: (t) => makeEl(t),
  createTextNode: (txt) => ({ nodeType: 3, textContent: txt }),
  addEventListener: () => {},
  querySelectorAll: (sel) => {
    const m = sel.match(/^#([\w-]+) \.pill$/);
    if (m) return pills[m[1]] || [];
    if (sel === 'nav.tabs button') return tabButtons;
    if (sel === '.panel') return [];
    return [];
  }
};
global.Plotly = {
  react: (div, traces, layout, config) => { reactCalls.push({div, traces, layout, config}); },
  newPlot: () => {},
  relayout: (div, upd) => { relayoutCalls.push({div, upd}); return Promise.resolve(); },
  Plots: { resize: () => {} }
};
global.window = global;

// ── run the report's real script ----------------------------------------------
const html = fs.readFileSync(HTML, 'utf8');
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
// ganhado irmao novo, senao os badges "partial" da Tabela 1 passariam a mentir.
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

console.log('\n=== 7. os badges de "partial" carregam a massa faltante ======');
let partials = [];
(function walk(ns) { ns.forEach(n => { if (n.decomp === 'partial') partials.push(n); if (n.children) walk(n.children); }); })(relTree);
ok(partials.length === 7, '7 pais parciais na arvore de divulgacao', partials.length);
const massa = partials.reduce((a, n) => a + n.unshown, 0);
near(massa, 25.583, 0.01, 'massa nao exibida soma 25.583 pontos');
ok(partials.every(n => typeof n.unshown === 'number' && n.unshown > 0),
   'todo no parcial tem unshown numerico positivo');

console.log('\n=== 8. o factory renderizou tabela e grafico de verdade ======');
const corpo = el('release-table-body');
ok(corpo.children.length === 4, 'tbody da release tem 4 linhas no estado inicial (raiz expandida)', corpo.children.length);
const cab = el('release-table-head');
ok(cab.children.length === 1 && cab.children[0].children.length === 14,
   'cabecalho tem check + label + 12 meses', cab.children[0] && cab.children[0].children.length);
const primeira = corpo.children[0];
ok(primeira.children.length === 14, 'linha de dados tem 14 celulas', primeira.children.length);
const valores = primeira.children.slice(2).map(td => td.textContent);
ok(valores.every(v => v === '—' || /^[+-]\d+\.\d{2}$/.test(v)),
   'celulas formatadas como +/-N.NN ou em-dash', JSON.stringify(valores.slice(0, 4)));

ok(reactCalls.length >= 2, 'Plotly.react chamado para os dois graficos', reactCalls.length);
const rel = reactCalls.find(c => c.div === 'chart-release');
ok(!!rel, 'chart-release foi plotado');
ok(rel.traces.length === 3, 'plota os 3 nos marcados por default', rel.traces.length);
ok(rel.layout.dragmode === 'pan', 'dragmode = pan');
ok(rel.config.scrollZoom === true, 'scrollZoom ligado');
ok(rel.layout.yaxis.title.text === '%', 'titulo do Y para y/y e "%"', rel.layout.yaxis.title.text);
ok(rel.traces.every(t => t.x.length === t.y.length && t.x.length > 100),
   'traces tem x e y do mesmo tamanho e historico longo');

console.log('\n=== 9. clicar nos pills muda tabela e grafico ================');
const antes = reactCalls.length;
const pillLevel = pills['release-metric-group'].find(p => p.dataset.metric === 'level');
pillLevel.click();
ok(reactCalls.length > antes, 'clicar em "Index" re-renderizou o grafico');
const depois = reactCalls[reactCalls.length - 1];
ok(depois.layout.yaxis.title.text.indexOf('Index') === 0,
   'titulo do Y virou "Index ..."', depois.layout.yaxis.title.text);
const celulaNivel = el('release-table-body').children[0].children[2].textContent;
ok(/^\d+\.\d{2}$/.test(celulaNivel) || celulaNivel === '—',
   'celula em modo Index nao leva sinal', celulaNivel);

const pillContrib = pills['release-metric-group'].find(p => p.dataset.metric === 'contrib');
pillContrib.click();
ok(reactCalls[reactCalls.length - 1].layout.yaxis.title.text.indexOf('p.p.') === 0,
   'titulo do Y para contribuicao e em p.p.', reactCalls[reactCalls.length - 1].layout.yaxis.title.text);

const pillNSA = pills['release-basis-group'].find(p => p.dataset.basis === 'NSA');
const nAntes = reactCalls.length;
pillNSA.click();
ok(reactCalls.length > nAntes, 'trocar SA->NSA re-renderizou');

console.log('\n=== 10. botoes de range chamam Plotly.relayout ===============');
const barra = el('release-range');
const botoes = barra.children.filter(c => c.className === 'rb');
ok(botoes.length === 5, '5 botoes de range (3y/5y/10y/20y/All)', botoes.length);
relayoutCalls.length = 0;
botoes[0].click();
ok(relayoutCalls.length === 1, 'clicar em "3y" chamou relayout uma vez', relayoutCalls.length);
const r = relayoutCalls[0].upd['xaxis.range'];
ok(Array.isArray(r) && r.length === 2, 'relayout passou um par [de, ate]', JSON.stringify(r));
const anosJan = (new Date(r[1]) - new Date(r[0])) / (365.25 * 24 * 3600 * 1000);
near(anosJan, 3, 0.15, 'a janela de "3y" cobre ~3 anos');
ok(r[1] === D.tabs.release.dates.NSA[D.tabs.release.dates.NSA.length - 1],
   'o fim da janela e o ultimo ponto REAL da serie, nao a data de hoje', r[1]);
relayoutCalls.length = 0;
botoes[4].click();
ok(relayoutCalls[0].upd['xaxis.autorange'] === true, '"All" volta para autorange');

console.log('\n=== 11. KPIs ================================================');
const kpis = el('kpis');
ok(kpis.children.length === 6, '6 cards de KPI', kpis.children.length);
ok(kpis.children.every(c => c.innerHTML.indexOf('—') === -1),
   'nenhum KPI ficou sem valor');

console.log('\n' + '='.repeat(62));
console.log(`${oks} ok, ${falhas} falharam`);
process.exit(falhas ? 1 : 0);
