/*
 * Executa o JavaScript REAL embutido em reports/brasil/Inflation.html contra um
 * document/Plotly stubados e confere o COMPORTAMENTO -- nao a forma dos objetos
 * de configuracao.
 *
 * Existe por causa da licao registrada em .claude/rules/lis-dashboards.md: duas
 * rodadas de bug de interacao passaram batido em analytics/brasil/economic_activity
 * porque os testes afirmavam sobre a DEFINICAO dos botoes e nunca sobre o que
 * acontecia ao clicar. Aqui o script inteiro do relatorio e avaliado de verdade,
 * os pills sao clicados, e as assercoes sao sobre as linhas/celulas que a tabela
 * hierarquica produziu e sobre as traces que o grafico recebeu.
 *
 * Nasceu em 2026-08 com a tabela-arvore que substituiu o waterfall "Decomposicao
 * por Periodo". O foco e o que a arvore pode errar em silencio: um nivel que nao
 * soma o pai, um subitem pendurado no ramo errado, uma metrica que devolve
 * numero onde deveria devolver branco, e o corte Top-N do grafico de evolucao
 * (que so e honesto se "Outros" fechar a conta).
 *
 * Sem browser neste ambiente: renderizacao visual continua NAO verificada.
 *
 * Uso:  node --max-old-space-size=8192 tests/test_inflation_js.js
 */

const fs = require('fs');
const path = require('path');

const HTML = path.join(__dirname, '..', 'reports', 'brasil', 'Inflation.html');

let falhas = 0, oks = 0;
function ok(cond, msg, extra) {
  if (cond) { oks++; console.log('  ok      ' + msg); }
  else { falhas++; console.log('  FALHOU  ' + msg + (extra !== undefined ? '  -> ' + extra : '')); }
}
function near(a, b, tol, msg) {
  const d = Math.abs(a - b);
  ok(d <= tol, msg, `esperado ~${b}, veio ${a} (diff ${Number.isFinite(d) ? d.toFixed(5) : d})`);
}

// ── DOM stub ------------------------------------------------------------------
function makeEl(tag) {
  const e = {
    tagName: (tag || '').toUpperCase(),
    children: [], className: '', textContent: '', title: '', value: '',
    style: {}, dataset: {}, type: '', checked: false, disabled: false,
    options: [{ textContent: 'Todos' }], selectedIndex: 0,
    classList: {
      _s: new Set(),
      add(c) { this._s.add(c); }, remove(c) { this._s.delete(c); },
      contains(c) { return this._s.has(c); },
      toggle(c, on) { if (on === undefined) { this._s.has(c) ? this._s.delete(c) : this._s.add(c); } else { on ? this._s.add(c) : this._s.delete(c); } }
    },
    _listeners: {},
    appendChild(c) { this.children.push(c); return c; },
    prepend() {},
    setAttribute(k, v) { this[k] = v; },
    getAttribute(k) { return this[k] === undefined ? null : this[k]; },
    querySelectorAll() { return []; },
    contains() { return false; },
    addEventListener(ev, fn) { (this._listeners[ev] = this._listeners[ev] || []).push(fn); },
    click() { (this._listeners['click'] || []).forEach(f => f.call(this, { stopPropagation() {} })); },
    // _bindYAutofit (analytics/report_structure/y_autofit.js) usa a API de eventos
    // do Plotly -- el.on(...) --, nao addEventListener.
    on(ev, fn) { (this._listeners[ev] = this._listeners[ev] || []).push(fn); },
    fire(ev, arg) { (this._listeners[ev] || []).forEach(f => f.call(this, arg || {})); },
  };
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

const pills = {};
function definePills(groupId, attr, values) {
  pills[groupId] = values.map(v => {
    const p = makeEl('button');
    p.dataset[attr] = v.name;
    p.classList.add('pill');
    if (v.active) p.classList.add('active');
    return p;
  });
}
definePills('tree-source-group', 'tree', [{ name: 'ibge', active: true }, { name: 'bcb' }]);
definePills('tree-metric-group', 'metric', [
  { name: 'var', active: true }, { name: 'contrib' }, { name: 'yoy' }, { name: 'peso' }]);
definePills('evo-level-group', 'evo', [
  { name: '1', active: true }, { name: '2' }, { name: '3' }, { name: '4' }]);
// Aba Inercia: a instancia propria de makeTreeTab() e o seletor de metrica do
// grafico de faixas.
definePills('iner-metric-group', 'metric', [
  { name: 'var', active: true }, { name: 'contrib' }, { name: 'yoy' }, { name: 'peso' }]);
definePills('iner-faixas-metric-group', 'metric', [
  { name: 'yoy', active: true }, { name: 'var' }, { name: 'contrib' }]);
// Segunda tabela da mesma aba, a de cortes fixos em r.
definePills('inerfix-metric-group', 'metric', [
  { name: 'var', active: true }, { name: 'contrib' }, { name: 'yoy' }, { name: 'peso' }]);

const indexPills = ['ipca', 'ipca15'].map((v, i) => {
  const b = makeEl('button'); b.dataset.index = v; if (!i) b.classList.add('active'); return b;
});
const rangePills = ['ytd', '3m', '6m', '12m', 'all', 'custom'].map((v, i) => {
  const b = makeEl('button'); b.dataset.range = v; if (!i) b.classList.add('active'); return b;
});
const tabButtons = ['decomp', 'nucleos', 'inercia', 'heatmap'].map(t => {
  const b = makeEl('button'); b.dataset.tab = t; return b;
});

const react = [];   // {div, traces, layout}
const purged = [];
global.document = {
  getElementById: (id) => el(id),
  createElement: (t) => makeEl(t),
  createTextNode: (txt) => ({ nodeType: 3, textContent: txt }),
  addEventListener: () => {},
  querySelector: () => makeEl('main'),
  querySelectorAll: (sel) => {
    const m = sel.match(/^#([\w-]+) \.pill$/);
    if (m) return pills[m[1]] || [];
    if (sel === '[data-index]') return indexPills;
    if (sel === '[data-range]') return rangePills;
    if (sel === '.tab-btn') return tabButtons;
    return [];
  }
};
global.Plotly = {
  react: (div, traces, layout) => { react.push({ div, traces, layout }); },
  newPlot: (div, traces, layout) => { react.push({ div, traces, layout }); },
  purge: (div) => { purged.push(div); },
  relayout: () => Promise.resolve(),
  Plots: { resize: () => {} }
};
global.window = global;

// ── roda o script real do relatorio -------------------------------------------
const html = fs.readFileSync(HTML, 'utf8');
const scripts = [...html.matchAll(/<script(?![^>]*\bsrc=)[^>]*>([\s\S]*?)<\/script>/g)].map(m => m[1]);
if (!scripts.length) { console.log('FALHOU: nenhum <script> inline encontrado'); process.exit(1); }
const code = scripts[scripts.length - 1];
console.log(`script inline: ${code.length.toLocaleString()} chars`);
eval(code);

// helpers de leitura do HTML que a tabela produziu -----------------------------
function linhasTabela(bodyId) {
  const body = el(bodyId || 'tree-table-body').innerHTML;
  // `([^>]*)` e obrigatorio: a linha carrega data-depth depois da classe, e uma
  // regex que exigisse `>` colado ao class="" so casaria o cabecalho de Nucleos.
  return [...body.matchAll(/<tr class="([^"]*)"([^>]*)>([\s\S]*?)<\/tr>/g)].map(m => {
    const cls = m[1], attrs = m[2], inner = m[3];
    const label = (inner.match(/<td class="col-label"[^>]*>(?:<span[^>]*>[^<]*<\/span>\s*)?([\s\S]*?)<\/td>/) || [, ''])[1].trim();
    const valores = [...inner.matchAll(/<td class="col-value[^"]*">([^<]*)<\/td>/g)].map(v => v[1]);
    const check = (inner.match(/data-check="([^"]*)"/) || [, null])[1];
    const depth = (attrs.match(/data-depth="(\d+)"/) || [, null])[1];
    const cores = [...inner.matchAll(/<td class="col-value([^"]*)">/g)].map(v => v[1].trim());
    return { cls, label, valores, check, depth: depth === null ? null : +depth,
             cores, marcado: /checked/.test(inner) };
  });
}
function ultimoNaoNulo(s) {
  if (!s) return null;
  for (let i = s.values.length - 1; i >= 0; i--) if (s.values[i] != null) return s.values[i];
  return null;
}
function tracesDe(div) {
  for (let i = react.length - 1; i >= 0; i--) if (react[i].div === div) return react[i].traces;
  return null;
}

console.log('\n=== 1. payload ==============================================');
ok(typeof D === 'object' && D.records.length > 0, 'REPORT_DATA parseou', D.records.length);
ok(typeof D.ibge_nomes === 'object', 'D.ibge_nomes existe');
const porNivel = {};
Object.keys(D.ibge_nomes).forEach(k => { porNivel[k.length] = (porNivel[k.length] || 0) + 1; });
ok(porNivel[1] === 9, '9 grupos IBGE', porNivel[1]);
ok(porNivel[2] === 19, '19 subgrupos IBGE', porNivel[2]);
ok(porNivel[4] === 53, '53 itens IBGE', porNivel[4]);
ok(D.ibge_nomes['1'] && /Alimenta/.test(D.ibge_nomes['1']), 'grupo 1 e Alimentacao e bebidas', D.ibge_nomes['1']);
ok(D.ibge_nomes['1101'] === 'Cereais, leguminosas e oleaginosas', 'item 1101 nomeado', D.ibge_nomes['1101']);
// O parentesco NAO viaja por registro -- e o que segura o tamanho do arquivo.
ok(D.records[0].ibge_grupo === undefined, 'nenhum campo ibge_* nos registros (parentesco vem do prefixo do codigo)');

console.log('\n=== 2. a arvore IBGE tem a forma publicada ===================');
let T = DECOMP_TREE.index();
ok(T.root.children.length === 9, 'raiz -> 9 grupos', T.root.children.length);
ok(nodesAtDepth(T, 2).length === 19, 'nivel 2 -> 19 subgrupos', nodesAtDepth(T, 2).length);
ok(nodesAtDepth(T, 3).length === 53, 'nivel 3 -> 53 itens', nodesAtDepth(T, 3).length);
const nSub = nodesAtDepth(T, 4).length;
ok(nSub > 370 && nSub <= 614, 'nivel 4 -> subitens de todas as vigencias', nSub);
// Ordem: peso decrescente no mes de referencia.
const pesos1 = T.root.children.map(n => T.agg[n.key][T.last][1]);
ok(pesos1.every((v, i) => i === 0 || pesos1[i - 1] >= v), 'grupos ordenados por peso decrescente',
   T.root.children.map(n => n.label + '=' + (T.agg[n.key][T.last][1] * 100).toFixed(1)).join(' | '));

console.log('\n=== 3. a arvore SOMA (o unico invariante que importa) ========');
// Cada pai tem de ser exatamente a soma dos filhos em contribuicao E em peso,
// em TODOS os meses -- um subitem pendurado no ramo errado, ou contado duas
// vezes, aparece aqui e em nenhum outro lugar.
function checaSoma(rotulo) {
  const Ti = DECOMP_TREE.index();
  let pior = 0, piorNo = '', piorPeso = 0, nos = 0;
  (function walk(n) {
    if (n.children.length) {
      nos++;
      const a = Ti.agg[n.key] || {};
      Object.keys(a).forEach(dt => {
        let c = 0, p = 0;
        n.children.forEach(k => { const b = Ti.agg[k.key]; if (b && b[dt]) { c += b[dt][0]; p += b[dt][1]; } });
        const dc = Math.abs(c - a[dt][0]), dp = Math.abs(p - a[dt][1]);
        if (dc > pior) { pior = dc; piorNo = n.label + ' @ ' + dt; }
        if (dp > piorPeso) piorPeso = dp;
      });
      n.children.forEach(walk);
    }
  })(Ti.root);
  ok(pior < 1e-9, `${rotulo}: filhos somam o pai em contribuicao (${nos} pais x todos os meses)`, `pior ${pior} em ${piorNo}`);
  ok(piorPeso < 1e-9, `${rotulo}: filhos somam o pai em peso`, 'pior ' + piorPeso);
}
checaSoma('IBGE');

console.log('\n=== 4. a raiz reproduz o headline publicado ==================');
// A raiz e sum(contribuicao)/sum(pesos) dos subitens. O IPCA impresso pelo IBGE
// vem em D.bcb.IPCA (SGS 433). Bate a menos do arredondamento de 2 casas que o
// IBGE aplica em CADA subitem antes de nos os recombinarmos (~0,005 p.p./mes,
// limite de publicacao, ver CLAUDE.md da pasta).
// Medido 2026-08: media 0,00696 p.p. em 319 meses, pior 0,0719 em mai/2000, e
// abaixo de 0,006 desde 2021. O IPCA-15 da os mesmos numeros (0,0059 / 0,0674,
// tambem em mai/2000) -- que sao exatamente os que _splice_headline_15() ja
// registrava em generate_report.py, de uma medicao independente. O erro se
// concentra em 1999-2003 porque a inflacao mensal era maior: o arredondamento
// e absoluto (2 casas por subitem), a taxa nao. Tres limites em vez de um so:
// um teto frouxo sozinho passaria a mao numa degradacao recente.
function erroHeadline(serie, oficialNome, desde) {
  let soma = 0, n = 0, pior = 0, piorRecente = 0, piorDt = '';
  serie.dates.forEach((dt, i) => {
    const of = bcbValue(oficialNome, dt);
    if (of == null || serie.values[i] == null || dt < desde) return;
    const d = Math.abs(serie.values[i] - of);
    n++; soma += d;
    if (d > pior) { pior = d; piorDt = dt; }
    if (dt >= '2021-01' && d > piorRecente) piorRecente = d;
  });
  return { n, media: soma / n, pior, piorRecente, piorDt };
}
const raizVar = _seriesFromAgg(T.agg.root, 'var');
const eh = erroHeadline(raizVar, 'IPCA', '2000-01');
console.log(`          ${eh.n} meses | media ${eh.media.toFixed(5)} | pior ${eh.pior.toFixed(4)} em ${eh.piorDt} | pior desde 2021 ${eh.piorRecente.toFixed(4)}`);
ok(eh.n > 300, 'meses comparados contra a serie oficial', eh.n);
ok(eh.media < 0.01, 'erro medio da reconstrucao fica na casa do milesimo de p.p.', eh.media.toFixed(5));
ok(eh.piorRecente < 0.01, 'e desde 2021 nem o pior mes passa de 0,01 p.p.', eh.piorRecente.toFixed(4));
ok(eh.pior < 0.10, 'o pior de toda a historia (mai/2000, inflacao alta) fica abaixo de 0,10 p.p.',
   eh.pior.toFixed(4) + ' em ' + eh.piorDt);
// Peso total do indice = 100%.
near(_seriesFromAgg(T.agg.root, 'peso').values.slice(-1)[0], 100, 0.001, 'peso da raiz = 100%');

console.log('\n=== 5. metricas do no ========================================');
const alim = T.root.children.find(n => /Alimenta/.test(n.label));
const sv = _seriesFromAgg(T.agg[alim.key], 'var');
const sc = _seriesFromAgg(T.agg[alim.key], 'contrib');
const sp = _seriesFromAgg(T.agg[alim.key], 'peso');
const j = sv.dates.length - 1;
near(sc.values[j] / (sp.values[j] / 100), sv.values[j], 1e-3,
     'var. mensal == contribuicao / peso, no mesmo mes');
// Y/Y encadeia a razao NAO arredondada -- e exige 12 meses contiguos.
const sy = _seriesFromAgg(T.agg[alim.key], 'yoy');
let prod = 1;
for (let k = j - 11; k <= j; k++) prod *= (1 + sv.values[k] / 100);
near(sy.values[sy.dates.length - 1], (prod - 1) * 100, 0.02, 'Y/Y == encadeamento dos 12 meses');
ok(sy.dates.length === sv.dates.length - 11, 'Y/Y comeca 11 meses depois da serie mensal',
   `${sy.dates.length} vs ${sv.dates.length}`);
// A guarda de contiguidade: uma serie com buraco nao pode inventar um 12M.
const comBuraco = _seriesFromAgg({ '2020-01': [1, 1], '2020-02': [1, 1], '2020-03': [1, 1], '2020-04': [1, 1],
  '2020-05': [1, 1], '2020-06': [1, 1], '2020-07': [1, 1], '2020-08': [1, 1], '2020-09': [1, 1],
  '2020-10': [1, 1], '2020-11': [1, 1], '2024-01': [1, 1] }, 'yoy');
ok(comBuraco.values[0] === null, 'janela de 12 meses nao contigua devolve null, nao um numero falso',
   comBuraco.values[0]);

console.log('\n=== 6. a tabela renderizada ==================================');
let linhas = linhasTabela();
ok(linhas.length === 11, 'estado inicial: raiz + 9 grupos + cabecalho de Nucleos', linhas.length);
ok(/is-root/.test(linhas[0].cls) && linhas[0].label === 'IPCA', 'primeira linha e a raiz IPCA', linhas[0].label);
ok(linhas[0].valores.length === 12, '12 colunas de mes', linhas[0].valores.length);
ok(linhas[0].marcado, 'a raiz nasce marcada');
const cab = linhas[linhas.length - 1];
ok(/is-header/.test(cab.cls) && cab.label === 'Núcleos', 'ultima linha e o cabecalho de Nucleos', cab.label);
ok(el('tree-h2').textContent === 'Árvore do IPCA — Estrutura IBGE', 'titulo da secao', el('tree-h2').textContent);
// O valor exibido tem de ser o valor calculado, formatado -- nao um placeholder.
const ultimoMesRaiz = raizVar.values[raizVar.values.length - 1];
const esperado = (ultimoMesRaiz > 0 ? '+' : '') + ultimoMesRaiz.toFixed(2).replace('.', ',') + '%';
ok(linhas[0].valores[11] === esperado, 'ultima celula da raiz = var. mensal do ultimo mes',
   `${linhas[0].valores[11]} vs ${esperado}`);

console.log('\n=== 7. expandir/recolher =====================================');
el('tree-table-body').fire('click', { target: { getAttribute: (k) => k === 'data-toggle' ? 'root' : null } });
ok(linhasTabela().length === 2, 'recolher a raiz deixa raiz + cabecalho de Nucleos', linhasTabela().length);
el('tree-table-body').fire('click', { target: { getAttribute: (k) => k === 'data-toggle' ? 'root' : null } });
ok(linhasTabela().length === 11, 'reabrir devolve as 11 linhas', linhasTabela().length);
el('tree-expand-toggle').click();
linhas = linhasTabela();
ok(linhas.length === 1 + 9 + 19 + 53 + nSub + 1 + activeNucleoList().length - 1,
   'Expandir tudo abre a arvore inteira + os nucleos', linhas.length);
ok(el('tree-expand-toggle').textContent === 'Recolher tudo', 'o botao vira Recolher tudo',
   el('tree-expand-toggle').textContent);
// Indentacao cresce com a profundidade -- e o unico sinal visual de nivel.
const body = el('tree-table-body').innerHTML;
const pads = [...body.matchAll(/padding-left:(\d+)px/g)].map(m => +m[1]);
ok(new Set(pads).size >= 5, 'ha pelo menos 5 recuos distintos (raiz + 4 niveis)', [...new Set(pads)].sort((a, b) => a - b).join(','));
el('tree-expand-toggle').click();
// "Recolher tudo" volta ao estado inicial (raiz aberta nos grupos), nao a 2
// linhas: uma tabela de decomposicao sem nenhum nivel visivel nao serve para nada.
ok(linhasTabela().length === 11, 'Recolher tudo volta ao estado inicial, com os grupos a vista', linhasTabela().length);
ok(el('tree-expand-toggle').textContent === 'Expandir tudo', 'e o botao volta a dizer Expandir tudo',
   el('tree-expand-toggle').textContent);

console.log('\n=== 8. clicar num pill de metrica muda a tabela DE VERDADE ====');
const antes = linhasTabela()[0].valores.slice();
pills['tree-metric-group'][1].click();   // Contribuicao (p.p.)
ok(DECOMP_TREE.estado.metric === 'contrib', 'estado mudou para contrib', DECOMP_TREE.estado.metric);
const depois = linhasTabela()[0].valores.slice();
ok(antes.join('|') !== depois.join('|'), 'as celulas mudaram de valor');
const contribRaiz = _seriesFromAgg(T.agg.root, 'contrib');
const cEsp = (contribRaiz.values.slice(-1)[0] > 0 ? '+' : '') + contribRaiz.values.slice(-1)[0].toFixed(2).replace('.', ',');
ok(depois[11] === cEsp, 'a celula mostra a contribuicao, sem %', `${depois[11]} vs ${cEsp}`);
pills['tree-metric-group'][3].click();   // Peso (%)
ok(/^\d+,\d{2}%$/.test(linhasTabela()[0].valores[11]), 'Peso sai sem sinal e com %', linhasTabela()[0].valores[11]);

// Duas casas em TODAS as metricas (pedido do usuario, 2026-08) -- e nao so na
// raiz: contribuicao e peso vivem numa escala menor, entao um subitem e onde um
// `dec` esquecido apareceria.
DECOMP_TREE.estado.expanded = {}; DECOMP_TREE.grupos(DECOMP_TREE.index()).forEach(n => { DECOMP_TREE.estado.expanded[n.key] = true; });
['var', 'contrib', 'yoy', 'peso'].forEach((met, k) => {
  pills['tree-metric-group'][k].click();
  const fora = [];
  linhasTabela().forEach(l => l.valores.forEach(v => {
    if (v !== '—' && !/^[+-]?\d+,\d{2}%?$/.test(v)) fora.push(v);
  }));
  ok(fora.length === 0, `${met}: toda celula sai com 2 casas decimais`, fora.slice(0, 5).join(' '));
});
// O custo disso e medido, nao teorico: com 2 casas a contribuicao de subitem
// colapsa em "0,00" na maioria das celulas. O hover do grafico e o que salva a
// precisao, entao decHover NAO pode cair junto com dec.
ok(TREE_METRICS.contrib.decHover === 3 && TREE_METRICS.peso.decHover === 3,
   'contribuicao e peso mantem 3 casas no hover do grafico',
   `${TREE_METRICS.contrib.decHover}/${TREE_METRICS.peso.decHover}`);
pills['tree-metric-group'][1].click();
DECOMP_TREE.renderChart();
const hov = (tracesDe('chart-tree-sel') || [])[0];
ok(hov && /%\{y:\.3f\} p\.p\./.test(hov.hovertemplate),
   'e a trace de contribuicao pede 3 casas ao Plotly', hov && hov.hovertemplate);
DECOMP_TREE.estado.expanded = {root: true, nucleos: true};
pills['tree-metric-group'][0].click();   // volta para Var. mensal

console.log('\n=== 8b. cor por sinal e degrade de profundidade ==============');
// Verde >0 / vermelho <0 (v-up/v-dn), e SO nas metricas em que o sinal e a
// leitura. Classes proprias, nao as `pos`/`neg` do ranking desta mesma aba, que
// carregam a convencao inversa (laranja = positivo, "inflacao subindo").
pills['tree-metric-group'][0].click();   // Var. mensal (%)
let comCor = linhasTabela().filter(l => l.cores.some(c => c));
ok(comCor.length > 0, 'Var. mensal pinta celulas', comCor.length);
let erradas = 0, conferidas = 0;
linhasTabela().forEach(l => l.valores.forEach((v, k) => {
  if (v === '—') { if (l.cores[k]) erradas++; return; }
  conferidas++;
  const negativo = v.charAt(0) === '-';
  const esperado = v.replace(/[^0-9]/g, '').replace(/0/g, '') === '' && !negativo ? '' : (negativo ? 'v-dn' : 'v-up');
  if (l.cores[k] !== esperado) erradas++;
}));
ok(erradas === 0, `cada celula pintada bate com o sinal do numero (${conferidas} celulas)`, erradas + ' erradas');
ok(!/class="col-value pos"|class="col-value neg"/.test(el('tree-table-body').innerHTML),
   'nao reusa as classes pos/neg do ranking (convencao oposta)');

pills['tree-metric-group'][1].click();   // Contribuicao (p.p.) -- tambem pinta
ok(linhasTabela().some(l => l.cores.indexOf('v-dn') >= 0), 'Contribuicao pinta negativo de vermelho');
ok(linhasTabela().some(l => l.cores.indexOf('v-up') >= 0), 'e positivo de verde');

pills['tree-metric-group'][2].click();   // Var. 12M (%) -- sem cor
ok(linhasTabela().every(l => l.cores.every(c => c === '')), 'Var. 12M sai sem cor nenhuma',
   linhasTabela().flatMap(l => l.cores).filter(c => c).slice(0, 5).join(','));
ok(linhasTabela()[0].valores.some(v => v !== '—'), 'e ainda assim com numero (nao e tabela vazia)');
pills['tree-metric-group'][3].click();   // Peso (%) -- tambem sem cor
ok(linhasTabela().every(l => l.cores.every(c => c === '')), 'Peso tambem sai sem cor');
pills['tree-metric-group'][0].click();

// data-depth e o que o CSS usa para o degrade pai->filho. Tem de sair do proprio
// no: um segundo lugar guardando profundidade sairia de sincronia com a arvore.
DECOMP_TREE.estado.expanded = {}; DECOMP_TREE.grupos(DECOMP_TREE.index()).forEach(n => { DECOMP_TREE.estado.expanded[n.key] = true; });
DECOMP_TREE.renderTable();
linhas = linhasTabela();
const porProf = {};
linhas.forEach(l => { porProf[l.depth] = (porProf[l.depth] || 0) + 1; });
// Os nucleos tambem sao nivel 1 (sao filhos do cabecalho de Nucleos, que fica
// fora do degrade), entao o nivel 1 e 9 grupos + 12 nucleos.
const nNuc = activeNucleoList().length - 1;
ok(porProf[0] === 1 && porProf[1] === 9 + nNuc && porProf[2] === 19 && porProf[3] === 53,
   `data-depth 0/1/2/3 = raiz / ${9 + nNuc} (9 grupos + ${nNuc} nucleos) / subgrupos / itens`,
   JSON.stringify(porProf));
ok(porProf[4] === nSub, 'e data-depth 4 sao os subitens', porProf[4]);
// A profundidade tem de acompanhar o recuo, senao cor e indentacao contam
// historias diferentes sobre a mesma linha.
const descasado = linhas.filter(l => l.depth !== null &&
  +(el('tree-table-body').innerHTML.match(new RegExp('data-depth="' + l.depth + '"[^>]*>[\\s\\S]*?padding-left:(\\d+)px')) || [, -1])[1] !== 14 + l.depth * 18);
ok(descasado.length === 0, 'o recuo bate com o data-depth em todos os niveis', descasado.length);
// O cabecalho de Nucleos fica fora do degrade -- tem estilo proprio.
const cabNuc = linhas.find(l => /is-header/.test(l.cls));
ok(cabNuc.depth === null, 'o cabecalho de Nucleos nao leva data-depth (senao seria pintado como a raiz)');
const nucFilho = linhas.find(l => l.check && l.check.indexOf('nuc|') === 0);
ok(nucFilho.depth === 1, 'mas os nucleos em si entram como nivel 1', nucFilho.depth);
DECOMP_TREE.estado.expanded = {root: true, nucleos: true};
DECOMP_TREE.renderTable();

console.log('\n=== 9. o bloco de nucleos ====================================');
linhas = linhasTabela();
const nucLinhas = linhas.filter(l => l.check && l.check.indexOf('nuc|') === 0);
ok(nucLinhas.length === activeNucleoList().length - 1,
   'todos os nucleos menos o headline (que ja e a raiz)', nucLinhas.length);
const T2 = DECOMP_TREE.index();
const ex0 = T2.nucHeader.children.find(n => n.label === 'EX-0');
const p55 = T2.nucHeader.children.find(n => n.label === 'P55');
ok(ex0.flag === 'nucleo_ex0', 'EX-0 tem a coluna de pertencimento da NT-57', ex0.flag);
ok(p55.flag === null, 'P55 nao tem flag (e percentil, nao recorte de subitens)', p55.flag);
// A variacao mensal do nucleo e a serie do BCB, nao uma reconstrucao nossa.
const ex0Serie = treeSeriesDe(T2, ex0, 'var');
ok(ex0Serie.values === D.bcb['IPCA_nucleo_EX0'].values,
   'EX-0 le a serie oficial do BCB, sem recomputar');
ok(treeSeriesDe(T2, ex0, 'contrib') === null, 'nucleo nao tem contribuicao (nao e parcela aditiva)');
ok(treeSeriesDe(T2, p55, 'peso') === null, 'P55 nao tem peso');
const ex0Peso = ultimoNaoNulo(treeSeriesDe(T2, ex0, 'peso'));
ok(ex0Peso > 50 && ex0Peso < 100, 'EX-0 cobre a maior parte do indice, mas nao tudo', ex0Peso);
// E a celula em branco tem de sair em branco, nao em zero.
pills['tree-metric-group'][1].click();   // Contribuicao
const linhaEx0 = linhasTabela().find(l => l.label === 'EX-0');
ok(linhaEx0.valores.every(v => v === '—'), 'a linha do nucleo fica em branco na contribuicao',
   linhaEx0.valores.slice(0, 3).join(','));
ok(linhaEx0.cores.every(c => c === ''), 'e em branco nao ganha cor de sinal');
ok(/title="[^"]*não é parcela aditiva/.test(el('tree-table-body').innerHTML),
   'o motivo do branco esta no hover da linha');
pills['tree-metric-group'][0].click();

console.log('\n=== 10. checkbox -> grafico ==================================');
react.length = 0;
el('tree-table-body').fire('change', { target: { checked: true, getAttribute: (k) => k === 'data-check' ? ex0.key : null } });
let tr = tracesDe('chart-tree-sel');
ok(tr && tr.length === 2, 'raiz + EX-0 plotados', tr && tr.length);
ok(tr.some(t => t.name === 'EX-0'), 'a trace do EX-0 esta la', tr.map(t => t.name).join(','));
ok(tr.find(t => t.name === 'EX-0').line.dash === 'dot', 'nucleo entra tracejado, para nao se confundir com um ramo');
ok(tr.find(t => t.name === 'IPCA').y.length === raizVar.values.length,
   'a trace da raiz tem o historico completo, nao so os 12 meses da tabela');
el('tree-table-body').fire('change', { target: { checked: false, getAttribute: (k) => k === 'data-check' ? 'root' : null } });
tr = tracesDe('chart-tree-sel');
ok(tr.length === 1 && tr[0].name === 'EX-0', 'desmarcar a raiz tira a trace dela', tr.map(t => t.name).join(','));
purged.length = 0;
el('tree-clear-checks').click();
ok(purged.indexOf('chart-tree-sel') >= 0, 'limpar a selecao esvazia o grafico');
ok(/Nenhuma linha marcada/.test(el('tree-subtitle').textContent), 'e a legenda diz isso',
   el('tree-subtitle').textContent);
el('tree-table-body').fire('change', { target: { checked: true, getAttribute: (k) => k === 'data-check' ? 'root' : null } });

console.log('\n=== 11. os pills de profundidade (o que o waterfall fazia) ====');
function evoTraces() { return tracesDe('chart-timeseries'); }
react.length = 0;
pills['evo-level-group'][0].click();   // Grupo
let ev = evoTraces();
ok(ev.length === 9 + 1, 'profundidade Grupo: 9 barras + a linha Total', ev.length);
ok(ev[ev.length - 1].name === 'Total' && ev[ev.length - 1].type === 'scatter', 'a ultima trace e a linha Total');
pills['evo-level-group'][2].click();   // Item
ev = evoTraces();
ok(ev.length === EVO_TOP_N + 2, 'profundidade Item: Top-14 + Outros + Total', ev.length);
ok(/^Outros \(\d+\)$/.test(ev[EVO_TOP_N].name), 'a trace de resto se chama Outros(n)', ev[EVO_TOP_N].name);
pills['evo-level-group'][3].click();   // Subitem
ev = evoTraces();
ok(ev.length === EVO_TOP_N + 2, 'profundidade Subitem tambem fica em 16 traces (senao seriam ~600)', ev.length);
// O ponto do corte Top-N: a pilha continua sendo a particao completa do mes.
// Sem isso "Outros" seria decoracao e a linha Total nao bateria com as barras.
const iUlt = ev[0].x.length - 1;
let somaBarras = 0;
for (let k = 0; k < ev.length - 1; k++) somaBarras += ev[k].y[iUlt];
near(somaBarras, ev[ev.length - 1].y[iUlt], 5e-4, 'barras (Top-N + Outros) somam a linha Total no ultimo mes');
let piorMes = 0;
for (let m = 0; m < ev[0].x.length; m++) {
  let s = 0;
  for (let k = 0; k < ev.length - 1; k++) s += ev[k].y[m];
  piorMes = Math.max(piorMes, Math.abs(s - ev[ev.length - 1].y[m]));
}
ok(piorMes < 5e-4, 'e fecham em TODOS os meses, nao so no ultimo', piorMes);
ok(/Subitem/.test(el('evo-subtitle').textContent) && /Outros/.test(el('evo-subtitle').textContent),
   'a legenda diz a profundidade e avisa do corte', el('evo-subtitle').textContent);
pills['evo-level-group'][0].click();

console.log('\n=== 11b. legenda embaixo, e a altura CSS batendo com a do Plotly ====');
function layoutDe(div) {
  for (let i = react.length - 1; i >= 0; i--) if (react[i].div === div) return react[i].layout;
  return null;
}
// A secao 11 zera `react` para contar as traces por profundidade, entao o
// ultimo layout de chart-tree-sel se perde -- redesenha antes de ler.
DECOMP_TREE.renderChart();
// A legenda saiu da lateral por pedido do usuario: a coluna da direita comia
// ~190px de largura util e truncava o proprio rotulo.
[['chart-tree-sel', 600], ['chart-timeseries', 680]].forEach(([div, alturaCss]) => {
  const L = layoutDe(div);
  ok(L.legend.orientation === 'h', `${div}: legenda horizontal`, L.legend.orientation);
  ok(L.legend.y < 0 && L.legend.yanchor === 'top', `${div}: e ancorada abaixo da area do grafico`,
     `y=${L.legend.y} yanchor=${L.legend.yanchor}`);
  ok(L.margin.r <= 40, `${div}: a margem direita voltou para o grafico`, L.margin.r);
  ok(L.margin.b >= 140, `${div}: a margem inferior comporta pills + legenda`, L.margin.b);
  // A legenda tem de caber ABAIXO das pills de periodo, nao em cima delas.
  ok(L.legend.y < L.xaxis.rangeselector.y, `${div}: a legenda fica abaixo das pills de periodo`,
     `legenda ${L.legend.y} vs pills ${L.xaxis.rangeselector.y}`);
  // Este par ja transbordou um card neste relatorio uma vez (ver o gotcha do
  // chart-scatter-momentum no CLAUDE.md da pasta): a altura do layout do Plotly
  // foi ajustada e a do CSS ficou para tras, e o grafico vazou para a secao
  // seguinte em silencio. Agora as duas sao lidas do arquivo e comparadas.
  const cssAltura = +(html.match(new RegExp('#' + div + '\\s*\\{[^}]*height:\\s*(\\d+)px')) || [, -1])[1];
  ok(cssAltura === alturaCss && L.height === alturaCss,
     `${div}: altura do CSS e a do layout do Plotly sao a mesma`, `css ${cssAltura} vs layout ${L.height}`);
});
// Rotulo longo vira MUITAS LINHAS numa legenda horizontal (na vertical virava
// texto cortado), entao o truncamento tem de continuar valendo.
const longos = (tracesDe('chart-timeseries') || []).filter(t => t.name.length > 27);
ok(longos.length === 0, 'nenhum rotulo de legenda passa de 27 caracteres', longos.map(t => t.name).join(' | '));

console.log('\n=== 12. trocar de arvore =====================================');
react.length = 0;
pills['tree-source-group'][1].click();   // Classificacao BCB
ok(DECOMP_TREE.estado.src === 'bcb', 'estado mudou', DECOMP_TREE.estado.src);
T = DECOMP_TREE.index();
ok(T.root.children.length === 2, 'raiz BCB -> Livres e Monitorados', T.root.children.map(n => n.label).join(','));
ok(nodesAtDepth(T, 2).length === 4, 'nivel 2 -> Alimentos/Servicos/Bens Industriais/Monitorados',
   nodesAtDepth(T, 2).map(n => n.label).join(','));
ok(el('tree-h2').textContent === 'Árvore do IPCA — Classificação BCB', 'o titulo acompanha', el('tree-h2').textContent);
checaSoma('BCB');
// As chaves sao namespaced por nivel de proposito: "Monitorados" e Grupo,
// Subgrupo E Item ao mesmo tempo, e uma chave so pelo rotulo colapsaria os tres.
const monG = T.root.children.find(n => n.label === 'Monitorados');
const monS = nodesAtDepth(T, 2).find(n => n.label === 'Monitorados');
const monI = nodesAtDepth(T, 3).find(n => n.label === 'Monitorados');
ok(monG.key !== monS.key && monS.key !== monI.key, 'Monitorados tem chave propria em cada nivel',
   [monG.key, monS.key, monI.key].join(' '));
near(T.agg[monG.key][T.last][1], T.agg[monI.key][T.last][1], 1e-12,
     'e os tres carregam o mesmo peso (sao o mesmo conjunto de subitens, em 3 niveis)');
// 'root' e a unica chave comum as duas arvores (e o mesmo total do indice);
// tudo abaixo dela e namespaced, entao a selecao volta ao estado inicial.
const marcadasBcb = linhasTabela().filter(l => l.marcado);
ok(marcadasBcb.length === 1 && marcadasBcb[0].check === 'root',
   'trocar de arvore zera a selecao de volta so a raiz (as demais chaves nao sobrevivem)',
   marcadasBcb.map(l => l.check).join(','));
// O grafico de evolucao segue a arvore ativa.
ok(evoTraces().length === 2 + 1, 'a evolucao passa a ter 2 barras + Total', evoTraces().length);
pills['tree-source-group'][0].click();

console.log('\n=== 13. trocar de indice =====================================');
indexPills[1].click();   // IPCA-15
ok(currentIndex === 'ipca15', 'estado mudou', currentIndex);
T = DECOMP_TREE.index();
ok(T.root.label === 'IPCA-15', 'a raiz da arvore muda de rotulo', T.root.label);
ok(el('tree-h2').textContent === 'Árvore do IPCA-15 — Estrutura IBGE', 'e o titulo tambem', el('tree-h2').textContent);
checaSoma('IPCA-15');
// Os nucleos do IPCA-15 sao calculados em casa (o BCB nao publica) -- a tabela
// tem de estar lendo essas series, nao as do IPCA cheio.
const ex0_15 = T.nucHeader.children.find(n => n.label === 'EX-0');
ok(ex0_15.serie === 'IPCA15_nucleo_EX0', 'EX-0 aponta para a serie de IPCA-15', ex0_15.serie);
ok(treeSeriesDe(T, ex0_15, 'var').values === D.bcb['IPCA15_nucleo_EX0'].values, 'e le ela');
const raiz15 = _seriesFromAgg(T.agg.root, 'var');
let pior15 = 0, n15 = 0;
raiz15.dates.forEach((dt, i) => {
  const of = bcbValue('IPCA15', dt);
  if (of == null || raiz15.values[i] == null || dt < '2000-06') return;
  n15++; pior15 = Math.max(pior15, Math.abs(raiz15.values[i] - of));
});
ok(n15 > 290 && pior15 < 0.08, 'a raiz reproduz o IPCA-15 publicado dentro do arredondamento do IBGE',
   `${n15} meses, pior ${pior15.toFixed(4)} p.p.`);
indexPills[0].click();

console.log('\n=== 13b. aba Inercia: a classificacao ========================');
ok(D.inercia && D.inercia.subitens, 'payload de inercia presente');
const IN = D.inercia;
ok(IN.medida === 'corr(yoy_t, yoy_t-12)', 'a medida declarada e o lag 12 do y/y', IN.medida);
ok(IN.janela.n_pontos === 120, 'janela de 120 observacoes y/y (10 anos)', IN.janela.n_pontos);
ok(IN.janela.indice_base === 'IPCA', 'estimada no IPCA cheio', IN.janela.indice_base);
ok(IN.faixas.length === 5, '5 faixas', IN.faixas.length);
ok(Object.keys(IN.subitens).length === IN.n_classificados, 'o dict bate com a contagem', IN.n_classificados);

// Faixas por PESO: cada uma ~20% do indice. O corte guloso de duas versoes
// anteriores dava 16,5%-23,4% e depois 18,0%-21,9%; a otimizacao minimax que
// ficou fecha em <=1,5 p.p. -- o piso e a granularidade (um unico subitem chega
// a 5% do indice, entao nao da para cortar mais fino que isso).
const somaPeso = IN.faixas.reduce((a, f) => a + f.peso, 0);
const desvios = IN.faixas.map(f => Math.abs(f.peso / somaPeso - 0.2) * 100);
ok(Math.max(...desvios) <= 1.5, 'toda faixa carrega 20% +-1,5 p.p. do peso classificado',
   IN.faixas.map((f, i) => `Q${f.q}=${(f.peso / somaPeso * 100).toFixed(2)}%`).join(' '));
// Ordem: as faixas tem de ser monotonicas em r, senao o rotulo "mais inercial" mente.
ok(IN.faixas.every((f, i) => i === 0 || IN.faixas[i - 1].hi <= f.lo),
   'as faixas nao se sobrepoem e sobem em r',
   IN.faixas.map(f => `[${f.lo},${f.hi}]`).join(''));
ok(IN.faixas[4].lo > IN.faixas[0].hi, 'Q5 esta inteiramente acima do Q1');

// Sanidade nominal: o que a teoria diz que e indexado tem de cair no topo, e o
// que oscila com commodity/bandeira tarifaria no fundo. E o unico teste que
// pegaria uma inversao de sinal na correlacao.
function faixaDe(nomeParcial) {
  const T = INERCIA_TREE.index();
  for (const cod of Object.keys(IN.subitens)) {
    const no = T.nodes['i1|' + cod];
    if (no && no.label.toLowerCase().indexOf(nomeParcial.toLowerCase()) >= 0) {
      return {cod, r: IN.subitens[cod][0], q: IN.subitens[cod][1], label: no.label};
    }
  }
  return null;
}
[['Plano de saúde', 4], ['Empregado doméstico', 4], ['Mão de obra', 4]].forEach(([n, minQ]) => {
  const f = faixaDe(n);
  ok(f && f.q >= minQ, `${n} cai nas faixas mais inerciais`, f ? `Q${f.q} r=${f.r}` : 'nao achado');
});
[['Gasolina', 2], ['Energia elétrica', 2]].forEach(([n, maxQ]) => {
  const f = faixaDe(n);
  ok(f && f.q <= maxQ, `${n} cai nas menos inerciais (reverte a media)`, f ? `Q${f.q} r=${f.r}` : 'nao achado');
});

console.log('\n=== 13c. aba Inercia: agregados e render =====================');
tabButtons.find(b => b.dataset.tab === 'inercia').click();
ok(tabRendered.inercia, 'a aba renderiza no primeiro switch');
const TI = INERCIA_TREE.index();
ok(TI.root.children.length === 5,
   'a arvore da aba e Faixa -> Subitem, com as 5 faixas e SO elas',
   TI.root.children.map(n => n.label).join(' | '));
// Ordem explicita: Q1..Q5 -- NAO por peso, que e o default das outras arvores.
// E o unico lugar em que `ord` e usado.
ok(TI.root.children[0].label.indexOf('Q1') === 0 && TI.root.children[4].label.indexOf('Q5') === 0,
   'as faixas saem em ordem Q1..Q5, nao por peso',
   TI.root.children.map(n => n.label.slice(0, 2)).join(','));
ok(!TI.root.children.some(n => /classificado/i.test(n.label)),
   'e o ramo "Nao classificado" NAO existe -- eram 237 descontinuados so com travessao');

// O invariante que importa: as faixas + os descontinuados reconstroem o indice,
// em contribuicao E em peso, em TODOS os meses. Sem isso um subitem poderia
// estar em duas faixas, ou em nenhuma, sem levantar excecao. Os descontinuados
// saem da arvore mas NAO da raiz, entao a diferenca tem de ser exatamente eles.
const descont = {};
IN.nao_classificados.forEach(x => { descont[x.codigo] = true; });
const resid = {};
D.records.forEach(r => {
  if (!descont[(r.subitem || '').slice(0, 7)]) return;
  const v = resid[r.dt] || (resid[r.dt] = [0, 0]);
  v[0] += r.contribuicao || 0; v[1] += r.pesos || 0;
});
let piorC = 0, piorP = 0;
Object.keys(TI.agg.root).forEach(dt => {
  let c = (resid[dt] || [0, 0])[0], pp = (resid[dt] || [0, 0])[1];
  TI.root.children.forEach(n => { const a = TI.agg[n.key]; if (a && a[dt]) { c += a[dt][0]; pp += a[dt][1]; } });
  piorC = Math.max(piorC, Math.abs(c - TI.agg.root[dt][0]));
  piorP = Math.max(piorP, Math.abs(pp - TI.agg.root[dt][1]));
});
ok(piorC < 1e-9 && piorP < 1e-9,
   'faixas + descontinuados reconstroem o indice em todos os meses',
   `contrib ${piorC} peso ${piorP}`);
// E a raiz continua sendo o INDICE, nao o subconjunto classificado -- e ela que
// vira a linha de referencia pontilhada do grafico das faixas.
const somaFaixasUlt = TI.root.children.reduce((s, n) => s + ((TI.agg[n.key] || {})[TI.last] || [0, 0])[1], 0);
ok(Math.abs(somaFaixasUlt - TI.agg.root[TI.last][1]) < 1e-9,
   'no ultimo mes os descontinuados pesam zero, entao faixas === raiz',
   `${somaFaixasUlt} vs ${TI.agg.root[TI.last][1]}`);

// A serie agregada de uma faixa e a media ponderada dos subitens dela -- e
// aqui checada contra uma reconstrucao independente a partir de D.records.
const q5 = Object.keys(IN.subitens).filter(k => IN.subitens[k][1] === 5);
const alvo = TI.last;
let somaC = 0, somaP = 0;
D.records.forEach(r => {
  if (r.dt !== alvo) return;
  if (q5.indexOf((r.subitem || '').slice(0, 7)) >= 0) { somaC += r.contribuicao || 0; somaP += r.pesos || 0; }
});
const serieQ5 = inerFaixaSerie(5, 'var');
near(serieQ5.values[serieQ5.dates.indexOf(alvo)], somaC / somaP, 1e-3,
     'a serie do Q5 bate com a media ponderada recalculada dos registros');

// Cartoes, grafico e dispersao renderizaram de fato.
const cards = el('iner-cards').innerHTML;
ok((cards.match(/iner-card/g) || []).length === 5, '5 cartoes de faixa',
   (cards.match(/iner-card/g) || []).length);
ok(/12 meses/.test(cards) && /% do índice/.test(cards), 'os cartoes trazem 12m e peso');
const trF = tracesDe('chart-iner-faixas');
ok(trF && trF.length === 6, '5 faixas + o headline de referencia no grafico', trF && trF.length);
ok(trF[5].line.dash === 'dot' && trF[5].name === 'IPCA', 'o headline entra pontilhado', trF[5].name);
const trD = tracesDe('chart-iner-disp');
ok(trD && trD[0].x.length === IN.n_classificados, 'a dispersao tem um ponto por subitem classificado',
   trD && trD[0].x.length);
ok(layoutDe('chart-iner-disp').yaxis.type === 'log', 'o eixo de peso e log (pesos vao de 0,001% a 5%)');
ok(layoutDe('chart-iner-disp').shapes.length === 4, '4 linhas de fronteira entre as 5 faixas',
   layoutDe('chart-iner-disp').shapes.length);

// A tabela da aba usa a MESMA fabrica -- 12 colunas, checkbox, expansivel.
const linhasIner = linhasTabela('iner-table-body');
ok(linhasIner.length === 6, 'a tabela renderiza raiz + as 5 faixas, e nada mais', linhasIner.length);
// Sem bloco de nucleos nesta aba: eles nao particionam o indice e nao dizem
// nada sobre inercia. A aba Decomposicao continua com eles.
ok(!/Núcleos/.test(el('iner-table-body').innerHTML), 'e SEM o bloco de nucleos');
ok(/Núcleos/.test(el('tree-table-body').innerHTML), 'que segue existindo na aba Decomposicao');
ok(linhasIner[0].valores.length === 12, 'as mesmas 12 colunas de mes', linhasIner[0].valores.length);
// O r de cada subitem aparece no rotulo, e o hover diz em quantos pares.
INERCIA_TREE.estado.expanded['i0|q5'] = true;
INERCIA_TREE.renderTable();
const linhaSub = linhasTabela('iner-table-body').find(l => l.depth === 2);
ok(/r [+-]\d,\d{2}$/.test(linhaSub.label), 'o subitem mostra o proprio r no rotulo', linhaSub.label);
ok(/pares/.test(el('iner-table-body').innerHTML), 'e o hover traz o numero de pares');
ok(/erro-padrão/i.test(el('iner-table-body').innerHTML), 'e o erro-padrao da estimativa');
// Os pills da aba sao independentes dos da Decomposicao.
pills['iner-metric-group'][3].click();
ok(INERCIA_TREE.estado.metric === 'peso' && DECOMP_TREE.estado.metric === 'var',
   'trocar a metrica na aba Inercia nao mexe na aba Decomposicao',
   `${INERCIA_TREE.estado.metric} / ${DECOMP_TREE.estado.metric}`);
pills['iner-metric-group'][0].click();

// A nota tem de dizer o que a medida NAO sustenta -- e o achado mais importante
// e o mais facil de sumir numa reescrita.
const nota = el('iner-nota-panel').innerHTML;
ok(/24%/.test(nota) && /acaso/.test(nota), 'a nota reporta a instabilidade fora da amostra (Q5 fica Q5 em 24%)');
ok(/0,895/.test(nota), 'e explica por que o lag 1 ficou de fora');
ok(/etiqueta de janela/.test(nota), 'e diz que o quintil e uma etiqueta de janela, nao do produto');

tabButtons.find(b => b.dataset.tab === 'decomp').click();

console.log('\n=== 13d. aba Inercia: a tabela de cortes fixos ===============');
ok(IN.faixas_fixas && IN.faixas_fixas.length === 4, 'o payload traz as 4 faixas de corte fixo',
   IN.faixas_fixas && IN.faixas_fixas.length);
ok(Object.keys(IN.subitens).every(k => IN.subitens[k].length === 4),
   'e cada subitem carrega [r, faixa_por_peso, n_pares, faixa_fixa]');
// O corte e FIXO: a faixa tem de ser deduzivel do proprio r, senao as duas
// classificacoes poderiam divergir sem que nada reclamasse.
const cortes = IN.cortes_fixos;
ok(cortes.length === 3 && cortes[0] === -0.5 && cortes[1] === 0 && cortes[2] === 0.5,
   'os limites sao -0,5 / 0 / +0,5', cortes.join(','));
const banda = r => r <= -0.5 ? 1 : r <= 0 ? 2 : r <= 0.5 ? 3 : 4;
ok(Object.keys(IN.subitens).every(k => IN.subitens[k][3] === banda(IN.subitens[k][0])),
   'e a faixa de cada subitem sai exatamente desses limites');
// Cada faixa fixa fecha com o que o Python declarou -- n e peso.
const TF = INERCIA_FIX_TREE.index();
ok(TF.root.children.length === IN.faixas_fixas.filter(f => f.n > 0).length,
   'a arvore tem um ramo por faixa fixa NAO vazia',
   `${TF.root.children.length} vs ${IN.faixas_fixas.filter(f => f.n > 0).length}`);
ok(TF.root.children[0].label.indexOf('Intensamente reversível') === 0,
   'em ordem, do mais reversivel para o menos', TF.root.children.map(n => n.label.slice(0, 14)).join(' | '));
let piorPF = 0;
IN.faixas_fixas.filter(f => f.n > 0).forEach(f => {
  // A chave do no vem de src.charAt(0) + nivel: 'inerciaFix' tambem comeca com
  // 'i', mas o sufixo f/q separa as duas arvores -- e cada indice e construido
  // para um src so, entao elas nunca convivem no mesmo `nodes`.
  const a = TF.agg['i0|f' + f.q];
  const nFilhos = TF.nodes['i0|f' + f.q].children.length;
  ok(nFilhos === f.n, `a faixa fixa ${f.q} tem os ${f.n} subitens que o Python contou`, nFilhos);
  piorPF = Math.max(piorPF, Math.abs(a[TF.last][1] - f.peso));
});
ok(piorPF < 1e-6, 'e o peso de cada faixa bate com o do payload no ultimo mes', piorPF);
// O mesmo invariante da tabela de quintis: faixas + descontinuados = indice.
let piorCF = 0;
Object.keys(TF.agg.root).forEach(dt => {
  let c = (resid[dt] || [0, 0])[0];
  TF.root.children.forEach(n => { const a = TF.agg[n.key]; if (a && a[dt]) c += a[dt][0]; });
  piorCF = Math.max(piorCF, Math.abs(c - TF.agg.root[dt][0]));
});
ok(piorCF < 1e-9, 'faixas fixas + descontinuados reconstroem o indice', piorCF);
// A tabela renderiza, tambem sem nucleos, e com estado independente da de cima.
const linhasFix = linhasTabela('inerfix-table-body');
ok(linhasFix.length === 1 + TF.root.children.length, 'raiz + as faixas, sem nucleos', linhasFix.length);
ok(!/Núcleos/.test(el('inerfix-table-body').innerHTML), 'e sem o bloco de nucleos');
pills['inerfix-metric-group'][3].click();
ok(INERCIA_FIX_TREE.estado.metric === 'peso' && INERCIA_TREE.estado.metric === 'var',
   'os pills das duas tabelas da aba sao independentes',
   `${INERCIA_FIX_TREE.estado.metric} / ${INERCIA_TREE.estado.metric}`);
pills['inerfix-metric-group'][0].click();
// A legenda tem de dizer que ESTA classificacao nao e estavel -- e o unico
// aviso que sobra depois que a nota da aba fala dos quintis.
const capFix = el('inerfix-cap').innerHTML;
ok(/13%/.test(capFix) && /4%/.test(capFix), 'a legenda reporta a retencao das duas pontas');
ok(/0,11|0,22/.test(capFix), 'e o kappa medido');

console.log('\n=== 14. o que o waterfall levou embora nao ficou pendurado ====');
ok(typeof renderWaterfall === 'undefined', 'renderWaterfall foi removida, nao deixada morta');
ok(typeof renderBreadcrumb === 'undefined', 'renderBreadcrumb tambem');
ok(typeof drillPath === 'undefined', 'e o estado drillPath junto');
ok(!/chart-waterfall/.test(html), 'nenhuma referencia a #chart-waterfall sobrou no HTML');
ok(!/id="breadcrumb"/.test(html), 'nem ao breadcrumb');
// O ranking abaixo dependia de applyDrillFilter e continua funcionando sozinho.
ok(el('table-body').innerHTML.length > 0, 'a tabela de ranking continua renderizando');

// Sem browser neste ambiente: DUMP=1 imprime as tabelas renderizadas como
// texto, que e o mais perto de conferir o que a pagina mostra. Nao e assercao.
if (process.env.DUMP) {
  const dump = (bodyId, titulo) => {
    console.log(`\n----- ${titulo} -----`);
    linhasTabela(bodyId).forEach(l =>
      console.log('  ' + '  '.repeat(l.depth) + l.label.padEnd(52).slice(0, 52)
                  + l.valores.slice(-4).map(v => String(v).padStart(9)).join('')));
  };
  tabButtons.find(b => b.dataset.tab === 'inercia').click();
  INERCIA_TREE.estado.expanded['i0|q5'] = true; INERCIA_TREE.renderTable();
  dump('iner-table-body', 'Inercia por quintil de peso (Q5 aberto)');
  INERCIA_FIX_TREE.estado.expanded['i0|f1'] = true;
  INERCIA_FIX_TREE.estado.expanded['i0|f4'] = true;
  INERCIA_FIX_TREE.renderTable();
  dump('inerfix-table-body', 'Reversibilidade por corte fixo (pontas abertas)');
  console.log('\nlegenda: ' + el('inerfix-cap').innerHTML.replace(/<[^>]+>/g, ''));
}

console.log('\n===============================================================');
console.log(`${oks} ok, ${falhas} falhou`);
process.exit(falhas ? 1 : 0);
