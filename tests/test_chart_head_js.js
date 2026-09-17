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

function El(tag) {
  this.tagName = tag; this.children = []; this.parentNode = null;
  this.className = ''; this.textContent = '';
}
El.prototype.appendChild = function (c) { c.parentNode = this; this.children.push(c); return c; };
El.prototype.insertBefore = function (n, ref) {
  n.parentNode = this;
  const i = this.children.indexOf(ref);
  this.children.splice(i < 0 ? this.children.length : i, 0, n);
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
  const head = card.children.filter((c) => c.className.indexOf('chart-head') === 0)[0];
  const txt = (cls) => {
    const el = head && head.children.filter((c) => c.className === cls)[0];
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

console.log('\n' + '='.repeat(62));
console.log(okN + ' ok, ' + falhas + ' falharam');
process.exit(falhas ? 1 : 0);
