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
    if (v.disabled) p.classList.add('disabled');
    p.classList.add('pill');
    return p;
  });
}
definePills('release-view-group', 'view', [{name: 'series', active: true}, {name: 'table1'}]);
definePills('expenditure-view-group', 'view', [{name: 'series', active: true}, {name: 'table1'}]);
definePills('release-metric-group', 'metric', [
  {name: 'level'}, {name: 'yoy', active: true}, {name: 'mom'}, {name: 'ann3m'}, {name: 'contrib'}]);
definePills('release-basis-group', 'basis', [{name: 'NSA'}, {name: 'SA', active: true}]);
definePills('expenditure-metric-group', 'metric', [
  {name: 'level'}, {name: 'yoy', active: true}, {name: 'mom'}, {name: 'ann3m'}, {name: 'contrib'}]);
definePills('expenditure-basis-group', 'basis', [{name: 'NSA'}, {name: 'SA', active: true}]);
// A aba de PCE nao tem pills de View (o toggle Series|Table 1 e coisa do release do
// BLS) e a pill NSA dela nasce desabilitada: o BEA nao publica PCE mensal sem ajuste
// sazonal.
definePills('pce-metric-group', 'metric', [
  {name: 'level'}, {name: 'yoy', active: true}, {name: 'mom'}, {name: 'ann3m'}, {name: 'contrib'}]);
definePills('pce-basis-group', 'basis', [{name: 'NSA', disabled: true}, {name: 'SA', active: true}]);

const tabButtons = ['release', 'expenditure', 'pce', 'appendix'].map(t => {
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

console.log('\n=== 12. a visao Table 1 =====================================');
// As 37 importancias relativas IMPRESSAS na Tabela 1 do release de julho/2026.
// A planilha de pesos so publica dezembro, entao a coluna e RECONSTRUIDA -- este
// bloco e a prova de que a reconstrucao esta certa, contra o numero publicado.
const RI_PUBLICADA = {
  SA0: 100.000, SAF1: 13.522, SAF11: 8.231, SAF111: 1.023, SAF112: 1.959, SEFJ: 0.743,
  SAF113: 1.283, SAF114: 0.981, SAF115: 2.242, SEFV: 5.290, SA0E: 7.432, SACE: 4.132,
  SEHE01: 0.106, SETB: 3.971, SETB01: 3.852, SEHF: 3.300, SEHF01: 2.552, SEHF02: 0.748,
  SA0L1E: 79.047, SACL1E: 18.829, SAA: 2.437, SETA01: 3.751, SETA02: 2.679, SAM1: 1.412,
  SAF116: 0.823, SEGA: 0.445, SASLE: 60.217, SAH1: 35.304, SEHA: 7.716, SEHC: 25.849,
  SAM2: 6.840, SEMC01: 1.660, SEMD01: 2.156, SAS4: 6.352, SETD: 1.048, SETE: 2.570,
  SETG01: 1.091
};
const spec = table1Spec('release');
ok(spec.ref.slice(0, 7) === D.meta.ultimo_mes,
   'o mes de referencia e o ultimo mes da base', spec.ref);
const mesAnterior = (function(ym) {
  const a = parseInt(ym.slice(0, 4), 10), m = parseInt(ym.slice(5, 7), 10) - 1;
  const tot = a * 12 + (m - 1);
  return String(Math.floor(tot / 12)).padStart(4, '0') + '-' + String(tot % 12 + 1).padStart(2, '0');
})(spec.ref.slice(0, 7));
ok(spec.ri.slice(0, 7) === mesAnterior,
   'a importancia relativa e datada um mes atras, como o release a data', spec.ri);

let piorRI = 0, semRI = [], conferidas = 0;
Object.keys(RI_PUBLICADA).forEach(function(code) {
  const v = riAt('release', code, spec.ri);
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

// A linha All items, celula por celula, contra o release impresso.
near(levelAt('release', 'SA0', 'NSA', spec.yrAgo), 323.048, 0.0005, 'indice NSA jul/25 = 323.048');
near(levelAt('release', 'SA0', 'NSA', spec.prev), 333.952, 0.0005, 'indice NSA jun/26 = 333.952');
near(levelAt('release', 'SA0', 'NSA', spec.ref), 333.918, 0.0005, 'indice NSA jul/26 = 333.918');
near(pctBetween('release', 'SA0', 'NSA', spec.ref, spec.yrAgo), 3.4, 0.05, 'NSA 12 meses = 3.4%');
near(pctBetween('release', 'SA0', 'NSA', spec.ref, spec.prev), 0.0, 0.05, 'NSA 1 mes = 0.0%');
const saM = spec.sa;
ok(saM.length === 4, 'a grade SA rende as 3 variacoes mensais do release', saM.length);
near(pctBetween('release', 'SA0', 'SA', saM[1], saM[0]), 0.5, 0.05, 'SA abr->mai = +0.5%');
near(pctBetween('release', 'SA0', 'SA', saM[2], saM[1]), -0.4, 0.05, 'SA mai->jun = -0.4%');
near(pctBetween('release', 'SA0', 'SA', saM[3], saM[2]), 0.1, 0.05, 'SA jun->jul = +0.1%');

// Prova estrutural, independente da Tabela 1 impressa: atualizar cada item
// separadamente nao pode quebrar a soma. Os 8 grupos de nivel 1 da arvore de
// despesa somam 100 antes e depois.
const especExp = table1Spec('expenditure');
const raizExp = D.tabs.expenditure.tree[0];
const somaRI = raizExp.children.reduce(function(a, c) {
  return a + (riAt('expenditure', c.seriesKey, especExp.ri) || 0);
}, 0);
near(somaRI, 100, 0.002, 'a importancia relativa atualizada dos 8 grupos de nivel 1 ainda soma 100');

// Sem peso publicado nao ha importancia relativa a atualizar.
ok(riAt('expenditure', 'SS47014', spec.ri) === null,
   'um item sem peso (gasolina comum) nao inventa importancia relativa');
ok(levelAt('expenditure', 'SS47014', 'NSA', spec.ref) != null,
   'mas o indice dele esta la');

// -0.04 imprime "0.0", nunca "-0.0" -- como o release imprime.
ok(fmtT1(-0.0102, 1) === '0.0', 'fmtT1 nao produz "-0.0"', fmtT1(-0.0102, 1));
ok(fmtT1(null, 3) === '—', 'celula vazia e em-dash');

// E agora o caminho pelo DOM: clicar no pill e conferir a tabela renderizada.
const pillT1 = pills['release-view-group'].find(x => x.dataset.view === 'table1');
pillT1.click();
const cabT1 = el('release-table-head');
ok(cabT1.children.length === 2, 'cabecalho da Table 1 tem duas linhas', cabT1.children.length);
ok(cabT1.children[0].children.length === 6,
   'linha de grupos: check + label + 4 grupos', cabT1.children[0].children.length);
ok(cabT1.children[1].children.length === 9,
   'linha de meses: as 9 colunas do release', cabT1.children[1].children.length);
ok(cabT1.children[0].children.map(x => x.textContent).join('|') ===
   '|Expenditure category|Relative importance|Unadjusted indexes|Unadjusted percent change|' +
   'Seasonally adjusted percent change',
   'os grupos sao os do release', cabT1.children[0].children.map(x => x.textContent).join('|'));

const linhaAll = el('release-table-body').children[0];
ok(linhaAll.children.length === 11, 'linha tem check + label + 9 valores', linhaAll.children.length);
const celulas = linhaAll.children.slice(2).map(td => td.textContent);
ok(celulas.join(' ') === '100.000 323.048 333.952 333.918 3.4 0.0 0.5 -0.4 0.1',
   'a linha All items reproduz a Tabela 1 celula por celula', celulas.join(' '));
ok(linhaAll.children[8].classList.contains('neg') === false &&
   linhaAll.children[9].classList.contains('neg') === true,
   'so a celula negativa de verdade fica vermelha (0.0 nao)');
ok(el('release-t1note').innerHTML.indexOf('Relative importance') === -1 ||
   el('release-t1note').style.display === '',
   'a nota da visao aparece');
ok(el('release-t1note').innerHTML.indexOf('computed') > 0,
   'e diz que a importancia relativa e calculada, nao publicada');

// Uma linha de drill-down vive na outra aba: as colunas de indice tem de resolver.
const linhas = el('release-table-body').children;
ok(linhas.length === 4, 'a Table 1 nao mexeu na arvore, so nas colunas', linhas.length);
ok(levelAt('release', 'SS47014', 'NSA', spec.ref) != null,
   'e um codigo de drill-down resolve na aba de divulgacao (seriesOwner)');

ok(/^\d+$/.test(el('ap-ri-n').textContent),
   'o apendice recebeu a contagem de linhas com importancia relativa', el('ap-ri-n').textContent);
const nRI = parseInt(el('ap-ri-n').textContent, 10);
ok(nRI > 250 && nRI < D.meta.n_expenditure,
   'a contagem e plausivel: menos que os 355 itens, mais que 250', nRI);

// Voltar para Series restaura as 12 colunas de mes.
pills['release-view-group'].find(x => x.dataset.view === 'series').click();
ok(el('release-table-head').children.length === 1 &&
   el('release-table-head').children[0].children.length === 14,
   'voltar para Series traz as 12 colunas de mes de volta');

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
  const linhas = el('release-table-body').children;
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
['release-table-body', 'expenditure-table-body'].forEach(function(id) {
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
ok(D.meta.ultimo_mes_pce !== D.meta.ultimo_mes,
   'e NAO e o mesmo do CPI: o PCE sai semanas depois',
   D.meta.ultimo_mes_pce + ' vs ' + D.meta.ultimo_mes);
function nivelPce(key) {
  const s = metricSeries('pce', key, 'SA', 'level');
  return s.values[s.values.length - 1];
}
near(nivelPce('1'), 131.392, 0.0005, 'PCE headline = 131.392 (= PCEPI no FRED)');
near(nivelPce('374'), 130.266, 0.0005, 'PCE core = 130.266 (= PCEPILFE no FRED)');

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

console.log('\n' + '='.repeat(62));
console.log(`${oks} ok, ${falhas} falharam`);
process.exit(falhas ? 1 : 0);
