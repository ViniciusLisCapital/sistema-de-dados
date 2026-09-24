/* Cabecalho de 3 linhas de cada grafico -- o helper compartilhado e quem ainda falta.
 *
 * Duas metades, e a segunda existe por causa de um erro de PROCESSO: quando a regra do
 * cabecalho foi promovida (2026-08-27), a lista de "quem falta migrar" foi escrita de
 * memoria e deixou de fora quatro relatorios do Brasil e o de inflacao dos EUA -- todos
 * descobertos meses depois, pelo usuario. Uma varredura no repositorio inteiro nao
 * esquece nenhum, e e o que esta secao 2 faz.
 *
 *   uv run python analytics/<area>/generate_report.py   (gera o que a secao 3 le)
 *   node tests/test_chart_head_js.js
 */
'use strict';
const fs = require('fs');
const path = require('path');

const RAIZ = path.join(__dirname, '..');
let okN = 0, falhas = 0;
function ok(cond, nome, detalhe) {
  if (cond) { okN++; console.log('  ok    ' + nome); }
  else { falhas++; console.log('  FALHA ' + nome + (detalhe !== undefined ? '  --  ' + detalhe : '')); }
}
function secao(t) { console.log('\n' + t); }

// -- 1. O helper compartilhado, executado de verdade --------------------------
secao('1. chart_head.js -- o helper, contra um DOM de mentira');

// O stub de DOM tem de ser FRACO onde o browser e fraco, senao ele mede outra coisa.
// `children` no browser e um HTMLCollection: so `length`, indice, item/namedItem e o
// iterador -- NENHUM metodo de Array. Enquanto o stub devolvia um Array de verdade,
// `card.children.filter(...)` passava aqui e lancava TypeError na pagina, e nenhuma das
// 40 assercoes abaixo tinha como perceber. (NodeList, a irma que sai de querySelectorAll,
// TEM `forEach` e continua sem `filter`/`map` -- o subconjunto quebrado nao e obvio, o
// que e a razao de o guarda ser sobre o stub e nao sobre a memoria de quem edita.)
function Colecao(arr) {
  const c = Object.create(Colecao.prototype);
  for (let i = 0; i < arr.length; i++) c[i] = arr[i];
  Object.defineProperty(c, 'length', {value: arr.length, enumerable: false});
  return c;
}
Colecao.prototype.item = function (i) { return this[i] != null ? this[i] : null; };
Colecao.prototype.namedItem = function () { return null; };
Colecao.prototype[Symbol.iterator] = function* () {
  for (let i = 0; i < this.length; i++) yield this[i];
};
// Quem le os filhos passa por aqui -- no stub e no codigo sob teste, pela mesma razao.
const filhos = (el) => Array.prototype.slice.call((el && el.children) || []);

function El(tag) {
  this.tagName = tag; this._kids = []; this.parentNode = null;
  this.className = ''; this.textContent = '';
}
// A mutacao vive no array interno; `children` e uma VISTA fraca sobre ele.
Object.defineProperty(El.prototype, 'children', {
  get() { return Colecao(this._kids); },
});
El.prototype.appendChild = function (c) { c.parentNode = this; this._kids.push(c); return c; };
El.prototype.insertBefore = function (n, ref) {
  n.parentNode = this;
  const i = this._kids.indexOf(ref);
  this._kids.splice(i < 0 ? this._kids.length : i, 0, n);
  return n;
};
El.prototype.closest = function () { return this._closest || null; };

const cards = {};
const documento = {
  createElement: (t) => new El(t),
  getElementById(id) {
    if (!cards[id]) {
      const div = new El('div'); div.id = id;
      const card = new El('div'); card.className = 'chart-card';
      card.appendChild(div); div._closest = card;
      cards[id] = div;
    }
    return cards[id];
  },
  querySelector: () => null,
};
function frameDe(id) {
  const card = documento.getElementById(id)._closest;
  const head = filhos(card).filter((c) => c.className.indexOf('chart-head') === 0)[0];
  const txt = (cls) => {
    const el = head && filhos(head).filter((c) => c.className === cls)[0];
    return el ? el.textContent : null;
  };
  return {head, titulo: txt('chart-title'), sub: txt('chart-sub'), src: txt('chart-src')};
}

const fonte = fs.readFileSync(path.join(RAIZ, 'analytics/report_structure/chart_head.js'), 'utf8');
// O relatorio declara o proprio CHART_META; o helper so o consulta.
const META = {
  g1: {title: 'Taxa de Desocupação — Brasil', source: 'IBGE, PNAD Contínua'},
  g2: {title: 'Sem Fonte', source: 'BLS'},
};
const escopo = new Function(
  'document', 'CHART_META',
  fonte + '\n; return {describeChart: describeChart, fmtPeriodo: fmtPeriodo, ' +
          '_chTraceXRange: _chTraceXRange};');
const H = escopo(documento, META);

// -- 1a. O STUB e fraco onde o browser e fraco --------------------------------
// Esta assercao nao e sobre o codigo sob teste, e sobre o instrumento. Ela existe porque
// o defeito de 2026-09-17 (TypeError em todo card de 2 relatorios) vivia EXATAMENTE na
// diferenca entre este stub e o browser: com `children` sendo Array, as 40 assercoes
// seguintes passavam verdes com a pagina quebrada. Um mutante que devolva um Array aqui
// tem de reprovar, senao o guarda nao guarda nada.
{
  const c = documento.getElementById('_fid')._closest.children;
  ok(typeof c.length === 'number', 'stub: a colecao tem length', typeof c.length);
  ok(c[0] !== undefined && c[0] === documento.getElementById('_fid'),
     'stub: a colecao tem acesso indexado');
  ok(typeof c.item === 'function' && c.item(0) === c[0], 'stub: a colecao tem item()');
  ok([...c].length === c.length, 'stub: a colecao e iteravel');
  ok(!Array.isArray(c), 'stub: a colecao NAO e um Array');
  ['filter', 'map', 'forEach', 'some', 'every', 'reduce', 'slice', 'indexOf', 'find']
    .forEach((m) => ok(typeof c[m] === 'undefined',
                       'stub: a colecao NAO tem .' + m + ' (HTMLCollection nao tem)', typeof c[m]));
  ok(Array.prototype.slice.call(c).length === c.length,
     'stub: slice.call converte a colecao -- o caminho que o codigo sob teste tem de usar');
}

const serieA = {name: 'Taxa de Desocupação — Brasil', x: ['2012-03-01', '2026-07-01'], y: [7.9, 5.8]};
H.describeChart('g1', [serieA], ['Mensal (trimestre móvel)'], 'desocupados / força de trabalho, %');
let f = frameDe('g1');
ok(f.titulo === 'Taxa de Desocupação — Brasil', 'titulo sai do CHART_META', f.titulo);
ok(f.sub === 'Mensal (trimestre móvel) · desocupados / força de trabalho, %',
   'subtitulo = seletores + unidade, e o nome da serie some por ser o proprio titulo', f.sub);
ok(f.src === 'Fonte: IBGE, PNAD Contínua · mar/2012 a jul/2026',
   'linha de fonte = fonte + a janela REAL das series plotadas', f.src);

// A poda: um pedaco ja contido na unidade nao entra duas vezes. Aqui os DOIS saem --
// "Mensal" e "%" ja estao dentro de "variação mensal, %" --, e e o comportamento certo:
// o subtitulo nao repete o que a propria unidade diz.
H.describeChart('g1', [serieA], ['Mensal', '%'], 'variação mensal, %');
ok(frameDe('g1').sub === 'variação mensal, %',
   'pedaco ja contido na unidade e podado', frameDe('g1').sub);
// E o que NAO esta contido sobrevive, senao a assercao acima passaria por vacuidade.
H.describeChart('g1', [serieA], ['Dessazonalizado', '%'], 'variação mensal, %');
ok(frameDe('g1').sub === 'Dessazonalizado · variação mensal, %',
   'o que a unidade nao diz continua no subtitulo', frameDe('g1').sub);

// Com mais de tres series o subtitulo diz a CONTAGEM -- a legenda ja nomeia cada uma, e
// ela viaja no mesmo print.
const quatro = ['a', 'b', 'c', 'd'].map((n) => ({name: n, x: ['2020-01-01'], y: [1]}));
H.describeChart('g1', quatro, [], 'p.p.');
ok(/^4 séries \(ver legenda\)/.test(frameDe('g1').sub), 'acima de 3 series, a contagem',
   frameDe('g1').sub);

// A janela vem do dado COM VALOR, nao do comprimento do array: numa visao de variacao
// anual o grafico comeca legitimamente depois, e a linha da fonte tem de dizer isso.
H.describeChart('g1', [{name: 'x', x: ['2020-01-01', '2020-02-01', '2020-03-01'], y: [null, 2, null]}],
                [], '%');
ok(/fev\/2020 a fev\/2020/.test(frameDe('g1').src), 'a janela ignora os nulos das pontas',
   frameDe('g1').src);

// Num heatmap o `y` sao os ROTULOS das linhas, nao valores: olhar `y` reportaria as N
// primeiras colunas como a serie inteira (N = numero de linhas).
const hm = {type: 'heatmap', x: ['2020-01-01', '2020-02-01', '2020-03-01'],
            y: ['linha 1', 'linha 2'], z: [[null, 1, 2], [null, 3, 4]]};
const rh = H._chTraceXRange([hm]);
ok(rh.lo === '2020-02-01' && rh.hi === '2020-03-01', 'heatmap: a janela sai do z, nao do y',
   rh.lo + '..' + rh.hi);

// Frequencia: um eixo trimestral rotulado em mes anuncia um mes que o grafico nao mostra.
ok(H.fmtPeriodo('2028-01-01', 'tri') === '2028T1', 'freq tri', H.fmtPeriodo('2028-01-01', 'tri'));
ok(H.fmtPeriodo('2026-12-01', 'ano') === '2026', 'freq ano', H.fmtPeriodo('2026-12-01', 'ano'));
ok(H.fmtPeriodo('2026-09-16', 'dia') === '16/09/2026', 'freq dia', H.fmtPeriodo('2026-09-16', 'dia'));

// Titulo derivado: onde a metrica e um seletor, um titulo fixo mentiria no 1o clique.
H.describeChart('g1', [serieA], [], '%', {titulo: 'Outro Título'});
ok(frameDe('g1').titulo === 'Outro Título', 'opts.titulo vence o CHART_META', frameDe('g1').titulo);

// Grafico cujo X nao e tempo: a janela vem pronta, senao a linha da fonte imprimiria uma
// faixa de VALORES lida como se fosse periodo.
H.describeChart('g1', [{name: 'p', x: [0.12, 8.4], y: [1, 2]}], [], 'eixo X: … · eixo Y: …',
                {periodo: 'leitura de jul/2026'});
ok(/· leitura de jul\/2026$/.test(frameDe('g1').src), 'opts.periodo substitui a derivacao',
   frameDe('g1').src);

// A moldura e construida UMA vez por card: varios renders reescrevem texto, nao empilham.
const antes = documento.getElementById('g1')._closest.children.length;
H.describeChart('g1', [serieA], [], '%');
ok(documento.getElementById('g1')._closest.children.length === antes,
   'a moldura nao e recriada a cada render');

// Uma trace fora da legenda (a ponte tracejada de uma previsao) nao e uma serie.
H.describeChart('g2', [serieA, {name: 'ponte', showlegend: false, x: ['2026-08-01'], y: [1]}], [], '%');
ok(!/ponte/.test(frameDe('g2').sub), 'trace com showlegend:false fica fora do subtitulo',
   frameDe('g2').sub);

// O ramo do card que JA traz o cabecalho pronto no markup (structural_model faz isso, e
// e por isso que ele escapou do TypeError): a varredura que o reaproveita tambem le
// `children`, entao ela precisa da mesma assercao -- e do mesmo slice.
{
  const div = new El('div'); div.id = 'g3';
  const card = new El('div'); card.className = 'chart-card';
  const head = new El('div'); head.className = 'chart-head';
  ['chart-title', 'chart-sub', 'chart-src'].forEach((cls) => {
    const d = new El('div'); d.className = cls; head.appendChild(d);
  });
  card.appendChild(head); card.appendChild(div); div._closest = card;
  cards.g3 = div;
  H.describeChart('g3', [serieA], ['Mensal'], '%', {titulo: 'Reaproveitado', fonte: 'IBGE'});
  ok(filhos(card).filter((c) => c.className.indexOf('chart-head') === 0).length === 1,
     'o cabecalho ja presente no markup e reaproveitado, nao duplicado',
     filhos(card).length);
  ok(frameDe('g3').titulo === 'Reaproveitado', 'e o cabecalho reaproveitado recebe o texto',
     frameDe('g3').titulo);
}

// -- 2. Quem ainda falta -- varredura, nunca de memoria -----------------------
secao('2. Todo relatorio que plota carrega o cabecalho');

const relatorios = [];
(function varre(dir) {
  fs.readdirSync(dir, {withFileTypes: true}).forEach((e) => {
    const full = path.join(dir, e.name);
    if (e.isDirectory()) varre(full);
    else if (e.name === 'report.html') relatorios.push(full);
  });
})(path.join(RAIZ, 'analytics'));

relatorios.forEach((file) => {
  const src = fs.readFileSync(file, 'utf8');
  const rel = path.relative(RAIZ, file).replace(/\\/g, '/');
  if (!/Plotly\.(newPlot|react)\s*\(/.test(src)) return;   // o calendario nao plota nada
  // Dois relatorios tem mecanica PROPRIA, anterior a compartilhada, e cobrem os graficos
  // deles por ela: labor_market monta o card inteiro em JS com o cabecalho dentro, e
  // exchange_rate tem renderChartHead() nas abas de dados e renderModelSrc() nas de
  // modelo (onde titulo e subtitulo ja vivem no markup do proprio card). Sao aceitos aqui
  // pelo nome da funcao, e nao por excecao muda: apagar a funcao reprova.
  const proprio = /function renderChartHead\(/.test(src) && /function renderModelSrc\(/.test(src);
  const emJs = /'<div class="chart-src">'|"<div class=\\"chart-src\\">"|className = 'chart-src'/.test(src)
               || /chart-src">/.test(src);
  const temCabecalho = src.indexOf('/*CHART_HEAD_JS*/') >= 0 || /describeChart\s*\(/.test(src)
                       || proprio || emJs;
  ok(temCabecalho, rel + ': tem cabecalho de grafico');
  if (!temCabecalho) return;
  // Fonte vazia e pior que ausente: a linha sai com a janela e sem de onde veio o dado.
  const metas = [...src.matchAll(/'(chart-[\w-]+)':\s*\{title:[^,]*,\s*source:\s*([A-Za-z_$][\w$]*|'[^']*'|"[^"]*")/g)];
  metas.forEach((m) => {
    ok(m[2] !== "''" && m[2] !== '""', rel + ': ' + m[1] + ' declara uma fonte', m[2]);
  });
});

// -- 3. O que foi GERADO carrega as tres linhas -------------------------------
secao('3. Os relatorios gerados trazem o cabecalho inlinado');

const GERADOS = [
  'reports/brasil/Monetary Policy.html',
  'reports/brasil/Credit.html',
  'reports/brasil/Fiscal Policy.html',
  'reports/brasil/Inflation.html',
  'reports/us/Inflation.html',
  'reports/brasil/Structural Model.html',
];
GERADOS.forEach((r) => {
  const file = path.join(RAIZ, r);
  if (!fs.existsSync(file)) { ok(false, r + ': existe (rode o generate_report da pasta)'); return; }
  const src = fs.readFileSync(file, 'utf8');
  ok(src.indexOf('/*CHART_HEAD_JS*/') < 0 && src.indexOf('/*CHART_HEAD_CSS*/') < 0,
     r + ': os marcadores foram substituidos');
  ok(/function describeChart\(divId, traces, bits, unit, opts\)/.test(src),
     r + ': o helper esta inlinado');
  ok(/\.chart-head \.chart-title/.test(src), r + ': o CSS do cabecalho esta inlinado');
  ok(/var CHART_META = \{/.test(src), r + ': declara o proprio CHART_META');
});

// -- 4. Metodo de Array em colecao viva do DOM -- a CLASSE, nao o caso --------
secao('4. Nenhuma colecao do DOM recebe metodo de Array');

// O defeito de 2026-09-17 era `card.children.filter(...)` em chart_head.js: lancava
// TypeError no PRIMEIRO grafico de cada pagina, e nenhum cabecalho era escrito. A secao
// 1a fecha isso pelo comportamento, mas so alcanca o que algum harness executa de fato;
// esta alcanca o codigo ESCRITO, inclusive o de um relatorio que ninguem exercita.
//
// O subconjunto quebrado nao e obvio, e e por isso que o guarda separa as duas colecoes:
//   HTMLCollection (.children, getElementsBy*)      -> NENHUM metodo de Array, nem forEach
//   NodeList       (querySelectorAll, .childNodes)  -> TEM forEach; nao tem filter/map/...
//
// `.children` de um NO DE ARVORE do payload e um Array de verdade, e ha dezenas desses
// nos relatorios (node.children, raiz.children). Por isso a varredura de `.children` so
// roda em report_structure/, onde todo `.children` e de um Element; nos report.html o
// guarda parte dos PRODUTORES, que nao tem ambiguidade nenhuma.
const ARRAY_METS = ['filter', 'map', 'reduce', 'reduceRight', 'some', 'every', 'find',
                    'findIndex', 'slice', 'sort', 'concat', 'indexOf', 'lastIndexOf',
                    'includes', 'join', 'flat', 'flatMap', 'reverse', 'splice'];
const MET = '(?:' + ARRAY_METS.join('|') + ')';

// Um uso ja embrulhado em Array.from(...) / Array.prototype.slice.call(...) esta CERTO --
// apague o embrulho antes de procurar, senao o guarda acusa o proprio conserto.
function semEmbrulho(src) {
  return src
    .replace(/Array\.prototype\.[A-Za-z]+\.call\(/g, 'JACONVERTIDO(')
    .replace(/Array\.from\(/g, 'JACONVERTIDO(');
}

// Casa `X.children.met(`, `(X.children || []).met(` e `X.querySelectorAll(..).met(`.
function achaUsos(src, produtor, mets) {
  const re = new RegExp(produtor + '\\s*(?:\\|\\|\\s*\\[\\s*\\])?\\s*\\)?\\s*\\.\\s*(' + mets + ')\\s*\\(', 'g');
  const out = [];
  let m;
  while ((m = re.exec(src)) !== null) {
    // `JACONVERTIDO(` abrindo o receptor = ja passou pelo slice/from e esta certo. O
    // que pode haver entre o parentese e o produtor e so o nome do receptor
    // (`slice.call(panel.querySelectorAll(...))`), entao a classe exclui `;`, `,` e
    // parenteses de proposito: um `Array.from(a); b.children.filter(` continua sendo
    // acusado, que e o caso em que o embrulho e de OUTRA expressao.
    const antes = src.slice(Math.max(0, m.index - 40), m.index);
    if (/JACONVERTIDO\(\s*[A-Za-z0-9_$.]*$/.test(antes)) continue;
    out.push({met: m[1], linha: src.slice(0, m.index).split('\n').length});
  }
  return out;
}
const mostra = (u) => u.map((x) => 'linha ' + x.linha + ': .' + x.met + '()').join(' | ');

fs.readdirSync(path.join(RAIZ, 'analytics/report_structure'))
  .filter((f) => f.endsWith('.js'))
  .forEach((f) => {
    const src = semEmbrulho(fs.readFileSync(path.join(RAIZ, 'analytics/report_structure', f), 'utf8'));
    const maus = achaUsos(src, '\\.(?:children|childNodes)', MET + '|forEach');
    ok(maus.length === 0,
       'report_structure/' + f + ': nenhum metodo de Array em .children/.childNodes',
       mostra(maus));
  });

relatorios.forEach((file) => {
  const rel = path.relative(RAIZ, file).replace(/\\/g, '/');
  const src = semEmbrulho(fs.readFileSync(file, 'utf8'));
  // getElementsBy* devolve HTMLCollection: nem forEach vale.
  const hc = achaUsos(src, 'getElementsBy(?:ClassName|TagNameNS|TagName|Name)\\([^()]*\\)',
                      MET + '|forEach');
  ok(hc.length === 0, rel + ': nenhum metodo de Array em getElementsBy* (HTMLCollection)',
     mostra(hc));
  // querySelectorAll e .childNodes devolvem NodeList: forEach vale, o resto nao.
  const nl = achaUsos(src, 'querySelectorAll\\((?:[^()]|\\([^()]*\\))*\\)', MET)
    .concat(achaUsos(src, '\\.childNodes', MET));
  ok(nl.length === 0, rel + ': nenhum metodo de Array (fora forEach) em NodeList', mostra(nl));
});

console.log('\n' + '='.repeat(62));
console.log(okN + ' ok, ' + falhas + ' falharam');
process.exit(falhas ? 1 : 0);
