/* Asserções sobre reports/brasil/Structural Model.html — a aba Curva de Phillips.
 *
 * Cada seção existe por um modo de falha que NÃO lança exceção nenhuma:
 *
 *  §1  o bloco de script executa. Um erro de referência na montagem dos cartões
 *      deixa a página em branco e o arquivo continua sendo gerado sem reclamar.
 *  §2  os quatro gráficos plotam, com as séries certas. Uma chave errada no
 *      payload produz um gráfico vazio, não um erro.
 *  §3  a janela da PRIMEIRA pintura é calculada, não `autorange` — senão o eixo
 *      abre com anos vazios depois do último ponto (o padding do próprio Plotly),
 *      e ninguém percebe porque nenhum botão foi clicado.
 *  §4  cada botão da régua manda um [from, to] tirado dos dados reais, inclusive
 *      o "Tudo"; e a régua fica DEPOIS do gráfico dentro do mesmo cartão.
 *  §5  o eixo Y diz o que a série mede, e o subtítulo imprime a MESMA string —
 *      as duas divergirem é o defeito que o cabeçalho existe para impedir.
 *  §6  o período do cabeçalho sai em trimestre, não em mês: um eixo trimestral
 *      rotulado "abr/2026" dá dois nomes para o que a fonte chama 2026T2.
 *  §7  duas séries no mesmo gráfico são distinguíveis por medida (ΔE2000 ≥ 20),
 *      não a olho.
 *  §8  o trimestre em aberto está marcado nos três lugares (faixa, tabela, aviso).
 *      Sem isso o último ponto é lido como fechamento de trimestre e não é.
 *  §9  toda chave do mapa de definições resolve numa série plotada. Uma chave
 *      órfã produz um botão que nunca nasce — sem erro e sem lacuna visível.
 *  §10 a prosa da página não usa o vocabulário do repositório.
 *
 * Roda com: node tests/test_structural_model_js.js
 */
'use strict';
const fs = require('fs');
const path = require('path');
const vm = require('vm');

const HTML = process.env.SM_REPORT ||
  path.join(__dirname, '..', 'reports', 'brasil', 'Structural Model.html');

if (!fs.existsSync(HTML)) {
  console.error('Relatorio nao encontrado: ' + HTML);
  console.error('Gere com: uv run python -c "from analytics.brasil.structural_model.generate_report import run; run()"');
  process.exit(1);
}
const CRU = fs.readFileSync(HTML, 'utf8');

const blocos = CRU.match(/<script>([\s\S]*?)<\/script>/g) || [];
if (!blocos.length) { console.error('Nenhum bloco <script> no HTML'); process.exit(1); }
const SRC = blocos[blocos.length - 1].replace(/^<script>/, '').replace(/<\/script>$/, '');
if (SRC.length < 5000) {
  // O HTML entregue tem CRLF; um terminador de fatia que nao casa devolve string
  // vazia sem erro, e o teste passa a medir nada achando que mede o real.
  console.error('Bloco de script curto demais (' + SRC.length + ' chars) — extracao falhou');
  process.exit(1);
}

// ── Stub de DOM ───────────────────────────────────────────────────────────────
const PORID = {};
const PORCLASSE = {};

function El(tag) {
  this.tagName = (tag || 'div').toUpperCase();
  this._id = '';
  this._class = '';
  this.children = [];
  this.childNodes = [];
  this.parentNode = null;
  this.style = {};
  this._text = '';
  this._html = '';
  this._attrs = {};
  this._lis = {};
  this.offsetWidth = 380;
  this.offsetHeight = 140;
  const self = this;
  this.classList = {
    add(c) { if (!self._cls().includes(c)) self._class = (self._class + ' ' + c).trim(); },
    remove(c) { self._class = self._cls().filter((x) => x !== c).join(' '); },
    contains(c) { return self._cls().includes(c); },
    toggle(c, force) {
      const tem = self._cls().includes(c);
      const quer = (force === undefined) ? !tem : !!force;
      if (quer) this.add(c); else this.remove(c);
      return quer;
    },
  };
}
El.prototype._cls = function () { return String(this._class || '').split(/\s+/).filter(Boolean); };
Object.defineProperty(El.prototype, 'id', {
  get() { return this._id; },
  set(v) { this._id = v; if (v) PORID[v] = this; },
});
Object.defineProperty(El.prototype, 'className', {
  get() { return this._class; },
  set(v) {
    this._class = v;
    this._cls().forEach((c) => { (PORCLASSE[c] = PORCLASSE[c] || []).push(this); });
  },
});
Object.defineProperty(El.prototype, 'textContent', {
  get() { return this._text; },
  set(v) { this._text = String(v); this._html = ''; },
});
Object.defineProperty(El.prototype, 'innerHTML', {
  get() { return this._html; },
  set(v) { this._html = String(v); this.children = []; this.childNodes = []; },
});
El.prototype.appendChild = function (c) {
  c.parentNode = this; this.children.push(c); this.childNodes.push(c); return c;
};
El.prototype.insertBefore = function (n, ref) {
  const i = this.children.indexOf(ref);
  if (i < 0) throw new Error('insertBefore: no ref nao e filho deste no');
  this.children.splice(i, 0, n); this.childNodes.splice(i, 0, n); n.parentNode = this; return n;
};
El.prototype.addEventListener = function (ev, fn) { (this._lis[ev] = this._lis[ev] || []).push(fn); };
El.prototype.dispatch = function (ev, arg) { (this._lis[ev] || []).forEach((f) => f(arg || {})); };
El.prototype.setAttribute = function (k, v) { this._attrs[k] = v; };
El.prototype.getAttribute = function (k) { return this._attrs[k]; };
El.prototype.getBoundingClientRect = function () { return { left: 10, right: 30, top: 10, bottom: 30 }; };
// Devolve SEMPRE vazio, e isso e deliberado: neste stub `innerHTML` nao constroi
// arvore nenhuma, entao nao existe filho para achar. A alternativa -- nao ter o
// metodo -- faria o codigo sob teste estourar com TypeError num caminho que no
// navegador funciona, o que e o stub sendo mais FRACO que o browser no lugar errado.
// O contrario tambem seria pior: devolver algo faria um teste de clique passar sem
// exercitar nada. A fiacao de quem monta a tela por `innerHTML` e coberta em
// `tests/test_structural_model_browser.js`, em Chrome de verdade.
El.prototype.querySelectorAll = function () { return []; };
El.prototype.querySelector = function () { return null; };
El.prototype.matches = function () { return false; };
El.prototype.contains = function (x) {
  if (x === this) return true;
  return this.children.some((c) => c.contains && c.contains(x));
};
El.prototype.closest = function (sel) {
  const c = sel.replace(/^\./, '');
  let n = this;
  while (n) { if (n._cls && n._cls().includes(c)) return n; n = n.parentNode; }
  return null;
};

function mk(tag, cls, id) {
  const e = new El(tag);
  if (cls) e.className = cls;
  if (id) e.id = id;
  return e;
}

const body = mk('body');
const document = {
  body,
  documentElement: { clientWidth: 1600, clientHeight: 900 },
  createElement: (t) => new El(t),
  getElementById: (id) => PORID[id] || null,
  querySelectorAll: (sel) => (PORCLASSE[sel.replace(/^\./, '')] || []),
  addEventListener: () => {},
};

// Elementos estaticos que o script toca, criados a partir dos ids que o HTML declara.
['hdrBadge', 'hdrDate', 'introNota', 'flagAberto', 'chartGrid',
 'tblPainel', 'tblNota', 'foldTabela', 'ftr',
 'subSemDados', 'subConteudo', 'subFicha', 'subFold', 'subFoldHint', 'subEqs',
 'subEqNota', 'tblSaz', 'sazNota', 'tblAcf', 'acfNota', 'tblIA', 'iaNota',
 'pillTri', 'pill12', 'vistaNota',
 'tblIM', 'imNota', 'subStats', 'subGridCheio',
 'subCoefSub', 'tblSubCoef', 'subCoefNota', 'subGrid',
 'subMathFold', 'subMathSimb', 'subMathLeg', 'subMathRestr', 'subMathSaz',
 'subMathFechos', 'subMathNum',
 'expSemDados', 'expConteudo', 'expFicha', 'expMathFold', 'expMathSimb', 'expMathLeg',
 'expMathRestr', 'expMathNota', 'expMathNum', 'expStats', 'expGrid', 'expCoefSub',
 'tblExpCoef', 'expCoefNota', 'expFold',
 'tblExpAcf', 'expAcfNota', 'tblExpBc', 'expBcNota',
 'isSemDados', 'isConteudo', 'isFicha', 'isMathFold', 'isMathSimb', 'isMathLeg',
 'isMathNota', 'isMathRestr', 'isMathNum', 'isStats', 'isGrid', 'isCoefSub',
 'tblIsCoef', 'isCoefNota', 'isFold', 'tblIsRR', 'isRRNota', 'tblIsComp',
 'isCompNota', 'tblIsAcf', 'isAcfNota', 'tblIsBc', 'isBcNota',
 'taySemDados', 'tayConteudo', 'tayFicha', 'tayMathFold', 'tayMathSimb', 'tayMathLeg',
 'tayMathNota', 'tayMathRestr', 'tayMathNum', 'tayStats', 'tayGrid', 'tayCoefSub',
 'tblTayCoef', 'tayCoefNota', 'tayFold', 'tblTayJanela', 'tayJanelaNota', 'tblTayComp',
 'tayCompNota', 'tblTayAcf', 'tayAcfNota', 'tblTayBc', 'tayBcNota',
 'fxSemDados', 'fxConteudo', 'fxFicha', 'fxMathFold', 'fxMathSimb', 'fxMathLeg',
 'fxMathNota', 'fxMathNum', 'fxStats', 'fxGrid', 'fxCoefSub', 'tblFxCoef', 'fxCoefNota',
 'fxFlipCard', 'fxFlipTitulo', 'fxFlipTexto', 'tblFxFlip', 'fxFlipNota', 'fxFold',
 'tblFxComp', 'fxCompNota', 'tblFxMensal', 'fxMensalNota', 'tblFxAcf',
 'fxAcfNota',
 'simSemDados', 'simConteudo', 'simEqTitulo', 'simEqSub',
 'simOpcoes', 'simAviso', 'simGrid',
 'simJanela', 'simInputs'].forEach((id) => {
  if (!CRU.includes('id="' + id + '"')) {
    console.error('id declarado no teste mas ausente do HTML: ' + id); process.exit(1);
  }
  body.appendChild(mk('div', '', id));
});
// as abas, com o data-tab que o markup realmente traz
const TABS = [];
CRU.replace(/class="tab-btn[^"]*"\s+data-tab="([^"]+)"/g, (_, t) => { TABS.push(t); return _; });
TABS.forEach((t) => {
  const b = mk('button', 'tab-btn active'); b.setAttribute('data-tab', t); body.appendChild(b);
  body.appendChild(mk('div', 'tab-panel active', t));
});

// ── Stub de Plotly ────────────────────────────────────────────────────────────
const PLOT = {};
const RELAYOUTS = [];
function thenable(v) {
  const p = { then(f) { const r = f(v); return (r && r.then) ? r : p; }, catch() { return p; } };
  return p;
}
const Plotly = {
  newPlot(divId, traces, layout, config) {
    const gd = (typeof divId === 'string') ? document.getElementById(divId) : divId;
    if (!gd) throw new Error('newPlot num div inexistente: ' + divId);
    gd.on = function (ev, fn) { (gd._lis[ev] = gd._lis[ev] || []).push(fn); };
    gd.data = traces;
    gd.layout = layout;
    gd._fullLayout = JSON.parse(JSON.stringify(layout));
    PLOT[gd.id] = { traces, layout, config };
    return thenable(gd);
  },
  react(d, t, l, c) { return Plotly.newPlot(d, t, l, c); },
  relayout(divId, upd) {
    RELAYOUTS.push({ div: (typeof divId === 'string' ? divId : divId.id), upd });
    const e = PLOT[typeof divId === 'string' ? divId : divId.id];
    if (e && upd['xaxis.range']) e.layout.xaxis.range = upd['xaxis.range'];
    return thenable(null);
  },
  restyle(divId, upd) { (PLOT[divId] || {}).restyled = upd; return thenable(null); },
};

// ── Executa ───────────────────────────────────────────────────────────────────
let falhas = 0, oks = 0;
function secao(t) { console.log('\n' + t); }
function ok(cond, nome, detalhe) {
  if (cond) { oks++; console.log('  ok    ' + nome); }
  else { falhas++; console.log('  FALHA ' + nome + (detalhe ? '  [' + detalhe + ']' : '')); }
}

const ctx = {
  document, Plotly, console,
  window: { scrollX: 0, scrollY: 0 },
  setTimeout: () => 0,
  Set, Map, Math, Date, JSON, Object, Array, String, Number,
  isNaN, parseInt, parseFloat, RegExp, Error,
};
ctx.globalThis = ctx;
vm.createContext(ctx);

secao('1. O bloco de script executa');
let erro = null;
try { vm.runInContext(SRC, ctx, { filename: 'structural_model.js' }); }
catch (e) { erro = e; }
ok(!erro, 'roda sem lancar', erro && (erro.constructor.name + ': ' + erro.message));
if (erro) { console.log('\n' + (erro.stack || '').split('\n').slice(0, 6).join('\n')); process.exit(1); }

const D = ctx.D;
ok(!!D && !!D.s, 'o payload chegou ao contexto (var D, nao const)');

// ── §2 ────────────────────────────────────────────────────────────────────────
secao('2. Os graficos da aba de dados plotam as series certas');
const ESPERADO = {
  'ch-grupos': ['pi_q', 'pi_is_q', 'pi_ia_q', 'pi_ii_q', 'pi_im_q'],
  'ch-exp': ['pi_e'],
  'ch-hiato': ['hiato'],
  // as duas pontas da curva real num cartao, a inclinacao noutro: unidades diferentes
  'ch-real': ['rr_2a', 'rr_10a'],
  'ch-grr': ['g_rr'],
  'ch-cambio': ['de'],
  'ch-comm': ['pi_agr_usd', 'pi_met_usd'],
  // os insumos da regra de juros. A Selic sozinha (escala propria), as duas
  // expectativas de horizonte longo juntas e as duas metas juntas
  'ch-selic': ['selic'],
  'ch-exp-longa': ['pi_e_2a', 'pi_bcb'],
  'ch-metas': ['meta_12m', 'meta_24m'],
};
// derivado de ESPERADO: acrescentar um grafico la nao pode deixar a contagem velha aqui
ok(Object.keys(PLOT).length === Object.keys(ESPERADO).length,
   Object.keys(ESPERADO).length + ' graficos plotados na aba de dados',
   'plotou ' + Object.keys(PLOT).join(','));
Object.keys(ESPERADO).forEach((div) => {
  const e = PLOT[div];
  ok(!!e, div + ': plotou');
  if (!e) return;
  ok(e.traces.length === ESPERADO[div].length,
     div + ': ' + ESPERADO[div].length + ' serie(s)', 'tem ' + e.traces.length);
  e.traces.forEach((t) => {
    const n = t.y.filter((v) => v != null).length;
    ok(n > 50, div + ' / ' + t.name + ': tem dado (' + n + ' pontos)');
    ok(t.x.length === D.x.length, div + ' / ' + t.name + ': x do tamanho do painel');
  });
  const L = e.layout;
  ok(L.dragmode === 'pan', div + ": dragmode 'pan'", L.dragmode);
  ok(!L.xaxis.rangeselector, div + ': sem rangeselector nativo');
  ok(L.xaxis.fixedrange !== true && L.yaxis.fixedrange !== true, div + ': sem fixedrange');
  ok(Array.isArray(L.shapes), div + ': shapes SEMPRE passado (nunca omitido)');
  ok(e.config.scrollZoom === true, div + ': scrollZoom ligado');
});
// A asserção acima passa mesmo que a fábrica perca o default, porque todo chamador de
// hoje passa `shapes` por cima. O que protege o gráfico que AINDA não existe — um que
// chame a fábrica sem passar nada, e com `Plotly.react` herde as formas do desenho
// anterior — é o default da própria fábrica, e é ele que esta linha cobra.
ok(Array.isArray(ctx.mkLayout().shapes) && ctx.mkLayout().shapes.length === 0,
   'mkLayout() sem argumento nenhum ja devolve shapes vazio',
   JSON.stringify(ctx.mkLayout().shapes));

// ── §3 ────────────────────────────────────────────────────────────────────────
secao('3. A primeira pintura aplica uma janela CALCULADA');
const passo = (Date.parse(D.x[D.x.length - 1]) - Date.parse(D.x[D.x.length - 2])) / 2;
Object.keys(ESPERADO).forEach((div) => {
  const r = RELAYOUTS.filter((x) => x.div === div && x.upd['xaxis.range']);
  ok(r.length >= 1, div + ': aplicou xaxis.range na primeira pintura');
  if (!r.length) return;
  const [from, to] = r[0].upd['xaxis.range'];
  const loD = Date.parse(D.x[0]), hiD = Date.parse(D.x[D.x.length - 1]);
  ok(Math.abs(Date.parse(from) - (loD - passo)) <= 864e5,
     div + ': borda esquerda a meio passo do primeiro ponto', from);
  ok(Math.abs(Date.parse(to) - (hiD + passo)) <= 864e5,
     div + ': borda direita a meio passo do ultimo ponto', to);
  ok(!('xaxis.autorange' in r[0].upd), div + ': nao usou autorange');
});

// ── §4 ────────────────────────────────────────────────────────────────────────
secao('4. A regua de tempo');
Object.keys(ESPERADO).forEach((div) => {
  const bar = document.getElementById('rp-' + div);
  ok(!!bar && bar.children.length === 4, div + ': 4 botoes de range',
     bar ? String(bar.children.length) : 'sem barra');
  if (!bar || !bar.children.length) return;
  const ativos = bar.children.filter((b) => b._cls().includes('active'));
  ok(ativos.length === 1 && ativos[0].textContent === 'Tudo',
     div + ': "Tudo" nasce ativo', ativos.map((a) => a.textContent).join(','));

  const antes = RELAYOUTS.length;
  bar.children[0].dispatch('click');
  const dep = RELAYOUTS.slice(antes).filter((x) => x.div === div && x.upd['xaxis.range']);
  ok(dep.length === 1, div + ': clicar em "3a" manda um range');
  if (dep.length) {
    const to = Date.parse(dep[0].upd['xaxis.range'][1]);
    ok(Math.abs(to - (Date.parse(D.x[D.x.length - 1]) + passo)) <= 864e5,
       div + ': o "to" de "3a" sai do ultimo ponto real, nao do eixo atual');
  }
  // o cartao tem o grafico ANTES da regua
  const card = document.getElementById(div).parentNode;
  const iPlot = card.children.indexOf(document.getElementById(div));
  const iBar = card.children.indexOf(bar);
  ok(iPlot >= 0 && iBar > iPlot, div + ': a regua fica ABAIXO do grafico, no mesmo cartao',
     'plot=' + iPlot + ' regua=' + iBar);
});

// ── §5 ────────────────────────────────────────────────────────────────────────
secao('5. Eixo Y e subtitulo dizem a MESMA unidade');
const UNID = {
  'ch-grupos': 'variação do trimestre, %',
  'ch-exp': 'IPCA esperado para os 12 meses seguintes, % ao ano',
  'ch-hiato': 'produto efetivo − potencial, % do potencial',
  'ch-cambio': 'variação da taxa média do trimestre, %',
  'ch-comm': 'variação da média do trimestre, %',
};
Object.keys(UNID).forEach((div) => {
  const L = PLOT[div].layout;
  ok(L.yaxis.title === UNID[div], div + ': o eixo Y define o que a serie mede', String(L.yaxis.title));
  const card = document.getElementById(div).parentNode;
  const frame = card._chFrame;
  ok(!!frame, div + ': o cartao entregou o quadro do cabecalho pronto');
  if (!frame) return;
  ok((frame.sub.textContent || '').indexOf(UNID[div]) >= 0,
     div + ': o subtitulo imprime a mesma string do eixo', frame.sub.textContent);
  ok((frame.title.textContent || '').length > 3, div + ': tem titulo', frame.title.textContent);
  ok((frame.src.textContent || '').indexOf('Fonte:') === 0, div + ': declara a fonte', frame.src.textContent);
});

// ── §6 ────────────────────────────────────────────────────────────────────────
secao('6. O periodo do cabecalho sai em TRIMESTRE');
Object.keys(UNID).forEach((div) => {
  const src = document.getElementById(div).parentNode._chFrame.src.textContent;
  ok(/\d{4}T[1-4] a \d{4}T[1-4]/.test(src), div + ': periodo em "AAAATn a AAAATn"', src);
  ok(!/jan\/|fev\/|mar\/|abr\/|mai\/|jun\/|jul\/|ago\/|set\/|out\/|nov\/|dez\//.test(src),
     div + ': nao rotula o trimestre com nome de mes', src);
});

// ── §7 — CIEDE2000 ────────────────────────────────────────────────────────────
secao('7. Series do mesmo grafico sao distinguiveis (dE2000 >= 20)');
function hex2rgb(h) {
  const n = parseInt(h.replace('#', ''), 16);
  return [(n >> 16) & 255, (n >> 8) & 255, n & 255];
}
function rgb2lab(rgb) {
  let [r, g, b] = rgb.map((v) => {
    v /= 255;
    return v > 0.04045 ? Math.pow((v + 0.055) / 1.055, 2.4) : v / 12.92;
  });
  const x = (r * 0.4124 + g * 0.3576 + b * 0.1805) / 0.95047;
  const y = (r * 0.2126 + g * 0.7152 + b * 0.0722) / 1.00000;
  const z = (r * 0.0193 + g * 0.1192 + b * 0.9505) / 1.08883;
  const f = (t) => t > 0.008856 ? Math.cbrt(t) : (7.787 * t + 16 / 116);
  const [fx, fy, fz] = [f(x), f(y), f(z)];
  return [116 * fy - 16, 500 * (fx - fy), 200 * (fy - fz)];
}
function deltaE(h1, h2) {
  const [L1, a1, b1] = rgb2lab(hex2rgb(h1));
  const [L2, a2, b2] = rgb2lab(hex2rgb(h2));
  const avgL = (L1 + L2) / 2;
  const C1 = Math.hypot(a1, b1), C2 = Math.hypot(a2, b2);
  const avgC = (C1 + C2) / 2;
  const G = 0.5 * (1 - Math.sqrt(Math.pow(avgC, 7) / (Math.pow(avgC, 7) + Math.pow(25, 7))));
  const a1p = a1 * (1 + G), a2p = a2 * (1 + G);
  const C1p = Math.hypot(a1p, b1), C2p = Math.hypot(a2p, b2);
  const avgCp = (C1p + C2p) / 2;
  const deg = (r) => r * 180 / Math.PI;
  const rad = (d) => d * Math.PI / 180;
  let h1p = deg(Math.atan2(b1, a1p)); if (h1p < 0) h1p += 360;
  let h2p = deg(Math.atan2(b2, a2p)); if (h2p < 0) h2p += 360;
  let avgHp;
  if (Math.abs(h1p - h2p) > 180) avgHp = (h1p + h2p + 360) / 2; else avgHp = (h1p + h2p) / 2;
  const T = 1 - 0.17 * Math.cos(rad(avgHp - 30)) + 0.24 * Math.cos(rad(2 * avgHp))
            + 0.32 * Math.cos(rad(3 * avgHp + 6)) - 0.20 * Math.cos(rad(4 * avgHp - 63));
  let dhp = h2p - h1p;
  if (Math.abs(dhp) > 180) dhp += (h2p <= h1p) ? 360 : -360;
  const dLp = L2 - L1, dCp = C2p - C1p;
  const dHp = 2 * Math.sqrt(C1p * C2p) * Math.sin(rad(dhp) / 2);
  const SL = 1 + (0.015 * Math.pow(avgL - 50, 2)) / Math.sqrt(20 + Math.pow(avgL - 50, 2));
  const SC = 1 + 0.045 * avgCp;
  const SH = 1 + 0.015 * avgCp * T;
  const dTheta = 30 * Math.exp(-Math.pow((avgHp - 275) / 25, 2));
  const RC = 2 * Math.sqrt(Math.pow(avgCp, 7) / (Math.pow(avgCp, 7) + Math.pow(25, 7)));
  const RT = -RC * Math.sin(2 * rad(dTheta));
  return Math.sqrt(Math.pow(dLp / SL, 2) + Math.pow(dCp / SC, 2) + Math.pow(dHp / SH, 2)
                   + RT * (dCp / SC) * (dHp / SH));
}
// sanidade do porte: dois pares conhecidos da paleta publicada
ok(deltaE('#1F2853', '#1F2853') < 0.001, 'deltaE de uma cor com ela mesma e zero');
Object.keys(ESPERADO).forEach((div) => {
  const cores = PLOT[div].traces.map((t) => t.line.color);
  if (cores.length < 2) return;
  for (let i = 0; i < cores.length; i++) {
    for (let j = i + 1; j < cores.length; j++) {
      if (PLOT[div].traces[i].line.dash !== PLOT[div].traces[j].line.dash) continue;
      const d = deltaE(cores[i], cores[j]);
      ok(d >= 20, div + ': ' + cores[i] + ' x ' + cores[j] + ' separadas (dE ' + d.toFixed(1) + ')');
    }
  }
});

// ── §8 ────────────────────────────────────────────────────────────────────────
secao('8. O trimestre em aberto esta marcado');
const aberto = D.meta.aberto;
ok(D.completo.length === D.x.length, 'a marca de trimestre fechado cobre o painel inteiro');
ok(D.completo[D.completo.length - 1] === false || aberto === null,
   'a ultima linha so e "fechada" se nao houver trimestre em aberto');
if (aberto) {
  Object.keys(ESPERADO).forEach((div) => {
    const sh = PLOT[div].layout.shapes;
    ok(sh.length === 1 && sh[0].yref === 'paper' && sh[0].layer === 'below',
       div + ': a faixa do trimestre em aberto foi desenhada', JSON.stringify(sh));
    ok(sh.length === 1 && sh[0].x0 === aberto.x0 && sh[0].x1 === aberto.x1,
       div + ': a faixa cobre o trimestre em aberto, nao outro');
  });
  const flag = document.getElementById('flagAberto');
  ok(flag.style.display === '' && flag.textContent.indexOf(aberto.rot) >= 0,
     'o aviso no topo nomeia o trimestre em aberto', flag.textContent);
  ok(flag.textContent.indexOf(D.meta.fim_completo) >= 0,
     'o aviso diz qual foi o ultimo trimestre inteiro');
  const tbl = document.getElementById('tblPainel').innerHTML;
  ok(tbl.indexOf('class="aberto"') >= 0, 'a linha da tabela esta marcada');
  ok(document.getElementById('tblNota').textContent.indexOf(aberto.rot) >= 0,
     'a nota da tabela explica a marca');
}

// ── §9 ────────────────────────────────────────────────────────────────────────
secao('9. Definicoes: nenhuma chave orfa, nenhum `full` redundante');
const PLOTADAS = {};
Object.keys(ESPERADO).forEach((d) => ESPERADO[d].forEach((k) => { PLOTADAS[k] = true; }));
Object.keys(D.info).forEach((k) => {
  ok(!!PLOTADAS[k], 'chave "' + k + '" resolve numa serie plotada');
  const i = D.info[k];
  ok(!!i.nome && !!i.eixo && !!i.fonte, k + ': tem nome, unidade e fonte');
  ok(!i.full || i.full !== i.nome, k + ': `full` so existe quando difere do rotulo');
  ok((i.desc || '').length > 60, k + ': a explicacao tem conteudo', String((i.desc || '').length));
});
Object.keys(PLOTADAS).forEach((k) => ok(!!D.info[k], 'serie "' + k + '" tem entrada de definicao'));
// um botao `i` por serie, dentro das ferramentas do cartao
Object.keys(ESPERADO).forEach((div) => {
  const card = document.getElementById(div).parentNode;
  const tools = card.children.filter((c) => c._cls().includes('card-tools'))[0];
  const bts = tools ? tools.children.filter((c) => c._cls().includes('info-btn')) : [];
  ok(bts.length === ESPERADO[div].length,
     div + ': um botao de definicao por serie', 'tem ' + bts.length);
});

// ── §10 ───────────────────────────────────────────────────────────────────────
secao('10. A prosa e do dominio, nao do repositorio');
const PROIBIDO = ['generate_report', 'manifest.yaml', 'panel.py', 'MySQL', 'YAML', 'registry',
                  'para_q', 'DataFrame', 'payload', 'SGS 13522', 'commit', 'Desde 2026',
                  'inflc_', 'expc_', 'pm_hiato', 'cmb_ptax', 'comm_icbr'];
// Dois grupos, e a distincao importa: os que estao escritos no HTML, e os que so
// existem depois do render. Um bloco vazio no HTML NAO e defeito -- e um dos que o
// JS preenche; defeito e ele continuar vazio depois de a pagina montar, que e o que
// o segundo grupo cobra. Medir so o HTML deixaria o texto derivado sem guarda
// nenhum, que e justamente o que envelhece sozinho.
const noHtml = [];
CRU.replace(/<p class="prose"[^>]*>([\s\S]*?)<\/p>/g, (_, t) => { noHtml.push(t); return _; });
const fixos = noHtml.filter((b) => b.replace(/\s+/g, ' ').trim().length > 0);
// `innerHTML || textContent`: os blocos montados com innerHTML nao populam
// textContent no stub, e ler so um dos dois deixaria metade da prosa derivada
// fora do guarda sem que nada reprovasse.
function _prosa(id) {
  const e = document.getElementById(id);
  return String((e && (e.innerHTML || e.textContent)) || '').replace(/<[^>]*>/g, ' ');
}
const derivados = {
  introNota: _prosa('introNota'),
  tblNota: _prosa('tblNota'),
  flagAberto: _prosa('flagAberto'),
  subFicha: _prosa('subFicha'),
  subEqNota: _prosa('subEqNota'),
  sazNota: _prosa('sazNota'),
  acfNota: _prosa('acfNota'),
  iaNota: _prosa('iaNota'),
  imNota: _prosa('imNota'),
  subCoefSub: _prosa('subCoefSub'),
  subCoefNota: _prosa('subCoefNota'),
  expFicha: _prosa('expFicha'),
  isFicha: _prosa('isFicha'),
  isCoefNota: _prosa('isCoefNota'),
  isRRNota: _prosa('isRRNota'),
  isAcfNota: _prosa('isAcfNota'),
  isBcNota: _prosa('isBcNota'),
  tayFicha: _prosa('tayFicha'),
  tayMathNota: _prosa('tayMathNota'),
  tayCoefSub: _prosa('tayCoefSub'),
  tayCoefNota: _prosa('tayCoefNota'),
  tayJanelaNota: _prosa('tayJanelaNota'),
  tayCompNota: _prosa('tayCompNota'),
  tayAcfNota: _prosa('tayAcfNota'),
  tayBcNota: _prosa('tayBcNota'),
  fxFicha: _prosa('fxFicha'),
  fxMathNota: _prosa('fxMathNota'),
  fxCoefSub: _prosa('fxCoefSub'),
  fxCoefNota: _prosa('fxCoefNota'),
  fxFlipTexto: _prosa('fxFlipTexto'),
  fxFlipNota: _prosa('fxFlipNota'),
  fxCompNota: _prosa('fxCompNota'),
  fxMensalNota: _prosa('fxMensalNota'),
  fxAcfNota: _prosa('fxAcfNota'),
};
ok(noHtml.length >= 3, 'achou os blocos de prosa no HTML', String(noHtml.length));
ok(fixos.length >= 2, 'ha prosa escrita a mao', String(fixos.length));
ok(noHtml.length - fixos.length >= 1, 'ha prosa preenchida no render');

const junta = fixos.concat(Object.keys(derivados).map((k) => derivados[k])).join(' \n ');
PROIBIDO.forEach((t) => ok(junta.indexOf(t) < 0, 'a prosa nao usa "' + t + '"'));
fixos.forEach((b, i) =>
  ok(b.replace(/\s+/g, ' ').trim().length > 80, 'bloco fixo ' + (i + 1) + ' tem conteudo'));
Object.keys(derivados).forEach((k) =>
  ok(derivados[k].replace(/\s+/g, ' ').trim().length > 60,
     'o texto derivado "' + k + '" foi preenchido no render',
     String(derivados[k].length)));
// justificado com hifenizacao, e o <html> com lang (sem ele o browser nao hifeniza)
ok(/\.prose\s*\{[^}]*text-align:\s*justify/.test(CRU), 'a prosa e justificada');
ok(/\.prose\s*\{[^}]*hyphens:\s*auto/.test(CRU), 'com hyphens: auto');
ok(/<html lang="pt-BR">/.test(CRU), 'o <html> declara lang="pt-BR"');

// ── §11 ───────────────────────────────────────────────────────────────────────
secao('11. Tabela e botao "Dados no grafico"');
const linhas = (document.getElementById('tblPainel').innerHTML.match(/<tr/g) || []).length;
ok(linhas === D.x.length + 1, 'a tabela tem uma linha por trimestre mais o cabecalho',
   linhas + ' contra ' + (D.x.length + 1));
Object.keys(ESPERADO).forEach((div) => {
  const card = document.getElementById(div).parentNode;
  const tools = card.children.filter((c) => c._cls().includes('card-tools'))[0];
  const dl = tools.children.filter((c) => c._cls().includes('dl-toggle'))[0];
  ok(!!dl, div + ': tem o botao "Dados no grafico"');
  if (!dl) return;
  dl.dispatch('click');
  ok(dl._cls().includes('on'), div + ': o clique liga o botao');
  ok((PLOT[div].restyled || {}).mode === 'lines+markers+text',
     div + ': o clique mostra os rotulos', JSON.stringify(PLOT[div].restyled));
  dl.dispatch('click');
  ok((PLOT[div].restyled || {}).mode === 'lines+markers', div + ': o segundo clique oculta');
});

// ── §12 ───────────────────────────────────────────────────────────────────────
secao('12. A aba do modelo: pinta so quando aberta, e pinta os cinco graficos');
const S = D.sub;
ok(!!S, 'o payload traz a estimacao por grupo');
ok(CRU.indexOf('data-tab="tab-modelo"') >= 0, 'a aba existe no markup');
ok(CRU.indexOf('data-tab="tab-estim"') < 0, 'a aba da equacao agregada NAO existe mais');
// a lista exata, e nao so a contagem: uma aba que suma ou troque de id reprova
ok(TABS.join(',') === 'tab-dados,tab-modelo,tab-exp,tab-is,tab-tay,tab-fx,tab-sim',
   'as sete abas, nesta ordem', TABS.join(','));
ok(!PLOT['ch-cheio'], 'os graficos da aba NAO sao pintados enquanto ela esta fechada');

ctx.activateTab('tab-modelo');
const DIVS_SUB = ['ch-cheio'].concat(S.ordem.map((k) => 'ch-sub-' + k));
// posicao de cada trimestre dentro da grade trimestral, usada da §21 em diante
const POS12 = {};
S.x.forEach((d, i) => { POS12[d] = i; });
DIVS_SUB.forEach((d) => ok(!!PLOT[d], d + ': pintado ao abrir a aba'));
const nPlots = Object.keys(PLOT).length;
ctx.activateTab('tab-dados');
ctx.activateTab('tab-modelo');
ok(Object.keys(PLOT).length === nPlots, 'reabrir a aba nao duplica cartao');

ok(S.ordem.length === 4, 'quatro grupos', String(S.ordem.length));
S.ordem.forEach((k) => {
  const e = S.eq[k];
  ok(e.obs.length === S.x.length && e.fit.length === S.x.length,
     k + ': realizado e ajustado cobrem a amostra inteira');
  ok(e.coef.filter((c) => c.restrito).length >= 1,
     k + ': ao menos um peso dentro da restricao');
});
ok(S.cheio.obs.length === S.x.length && S.cheio.fit.length === S.x.length,
   'o cheio reconstruido cobre a mesma amostra');

// ── §13 ───────────────────────────────────────────────────────────────────────
secao('13. O cheio na tela E a soma ponderada dos quatro ajustados');
// Refaz a soma AQUI, a partir dos ajustados e dos pesos que viajam no payload, em vez
// de comparar o payload consigo mesmo.
let piorSoma = 0;
for (let i = 0; i < S.x.length; i++) {
  let acc = 0, w = 0;
  S.ordem.forEach((k) => { acc += (S.eq[k].peso[i] / 100) * S.eq[k].fit[i]; w += S.eq[k].peso[i] / 100; });
  piorSoma = Math.max(piorSoma, Math.abs(acc - S.cheio.fit[i]));
  if (i === 0) ok(Math.abs(w - 1) < 0.005, 'os pesos dos quatro somam 1 (' + w.toFixed(4) + ')');
}
ok(piorSoma < 0.02, 'o cheio e a soma ponderada dos quatro (erro max ' + piorSoma.toFixed(4) + ' p.p.)');

// o piso e a MESMA soma sobre os realizados -- refeita aqui tambem
let piorPiso = 0;
for (let i = 0; i < S.x.length; i++) {
  let acc = 0;
  S.ordem.forEach((k) => { acc += (S.eq[k].peso[i] / 100) * S.eq[k].obs[i]; });
  piorPiso = Math.max(piorPiso, Math.abs(acc - S.cheio.piso[i]));
}
ok(piorPiso < 0.02, 'o piso e a soma dos REALIZADOS (erro max ' + piorPiso.toFixed(4) + ')');

S.ordem.forEach((k) => {
  let pior = 0;
  S.eq[k].resid.forEach((r, i) => { pior = Math.max(pior, Math.abs(r - (S.eq[k].obs[i] - S.eq[k].fit[i]))); });
  ok(pior < 0.001, k + ': o residuo e realizado menos ajustado');
});

{
  const m = S.cheio.obs.reduce((a, b) => a + b, 0) / S.cheio.obs.length;
  let sst = 0, ssr = 0, ssrP = 0;
  S.cheio.obs.forEach((y, i) => {
    sst += (y - m) * (y - m);
    ssr += Math.pow(y - S.cheio.fit[i], 2);
    ssrP += Math.pow(y - S.cheio.piso[i], 2);
  });
  ok(Math.abs((1 - ssr / sst) - S.cheio.r2) < 0.002, 'o R2 do cheio fecha');
  ok(Math.abs(Math.sqrt(ssr / S.cheio.obs.length) - S.cheio.rmse) < 0.002, 'o RMSE do cheio fecha');
  ok(Math.abs(Math.sqrt(ssrP / S.cheio.obs.length) - S.cheio.rmse_piso) < 0.002, 'o RMSE do piso fecha');
  ok(S.cheio.rmse_piso < S.cheio.rmse / 5,
     'o piso e uma fracao do erro do modelo -- somar quase nao custa',
     S.cheio.rmse_piso + ' vs ' + S.cheio.rmse);
}

// ── §14 ───────────────────────────────────────────────────────────────────────
secao('14. As duas equacoes reconstrutiveis batem com a conta escrita, na unidade certa');
// IS e IM sao as unicas cujos regressores viajam inteiros no payload (hiato, expectativa
// e o IPCA cheio estao em D.s; IA e II usam commodities que nao viajam).
// Esta secao amarra as tres decisoes da especificacao de uma vez: a expectativa dividida
// por 4, a media movel dentro da restricao, e o ajuste pelo trimestre do rotulo.
const POS2 = {};
D.x.forEach((d, i) => { POS2[d] = i; });
function coefDe(k) {
  const m = {};
  S.eq[k].coef.forEach((c) => { m[c.key] = c.b; });
  return m;
}
function triDe(rot) { return parseInt(rot.split('T')[1], 10); }

{
  const b = coefDe('IS'), e = S.eq.IS;
  let pior = 0, n = 0;
  for (let i = 4; i < S.x.length; i++) {
    const t = POS2[S.x[i]];
    const mm4 = (e.obs[i - 1] + e.obs[i - 2] + e.obs[i - 3] + e.obs[i - 4]) / 4;
    const f = b.is1 * e.obs[i - 1] + b.is1b * mm4
            + (1 - b.is1 - b.is1b) * (D.s.pi_e[t - 1] / 4)
            + b.is2 * D.s.hiato[t] + e.saz[triDe(S.rot[i]) - 1];
    pior = Math.max(pior, Math.abs(f - e.fit[i])); n++;
  }
  ok(n > 80, 'IS: reconstruiu ' + n + ' trimestres');
  ok(pior < 0.02, 'IS: ajustado = is1*IS(-1) + is1b*MM4 + (1-is1-is1b)*E(-1)/4 + is2*H + saz'
     + ' (erro max ' + pior.toFixed(4) + ')');
}
{
  const b = coefDe('IM'), e = S.eq.IM;
  let pior = 0;
  for (let i = 1; i < S.x.length; i++) {
    const t = POS2[S.x[i]];
    const f = b.im1 * e.obs[i - 1] + b.im2 * D.s.pi_q[t - 1]
            + (1 - b.im1 - b.im2) * (D.s.pi_e[t - 1] / 4)
            + e.saz[triDe(S.rot[i]) - 1];
    pior = Math.max(pior, Math.abs(f - e.fit[i]));
  }
  ok(pior < 0.02, 'IM: os TRES pesos somam 1 e o ajustado sai deles (erro max '
     + pior.toFixed(4) + ')');
}
// a expectativa entra em /4 e nao inteira: refazer IS com ela inteira tem de ERRAR
{
  const b = coefDe('IS'), e = S.eq.IS;
  let pior = 0;
  for (let i = 4; i < S.x.length; i++) {
    const t = POS2[S.x[i]];
    const mm4 = (e.obs[i - 1] + e.obs[i - 2] + e.obs[i - 3] + e.obs[i - 4]) / 4;
    const f = b.is1 * e.obs[i - 1] + b.is1b * mm4
            + (1 - b.is1 - b.is1b) * D.s.pi_e[t - 1]
            + b.is2 * D.s.hiato[t] + e.saz[triDe(S.rot[i]) - 1];
    pior = Math.max(pior, Math.abs(f - e.fit[i]));
  }
  ok(pior > 0.5, 'a expectativa entra DIVIDIDA por 4 (sem a divisao o erro vai a '
     + pior.toFixed(2) + ' p.p.)');
}
S.ordem.forEach((k) => {
  const e = S.eq[k];
  let soma = 0;
  e.coef.filter((c) => c.restrito).forEach((c) => { soma += c.b; });
  ok(Math.abs(e.peso_e - (1 - soma)) < 1e-5,
     k + ': o peso da expectativa e o que sobra de 1',
     e.peso_e + ' vs ' + (1 - soma));
  e.coef.filter((c) => c.lp != null).forEach((c) => {
    ok(Math.abs(c.lp - c.b / e.peso_e) < 0.002,
       k + ' / ' + c.key + ': o longo prazo e o peso dividido pelo da expectativa');
  });
  ok(e.coef.filter((c) => c.lp != null).every((c) => !c.restrito),
     k + ': so os empurroes tem efeito de longo prazo, nunca um peso restrito');
});

// ── §15 ───────────────────────────────────────────────────────────────────────
secao('15. Os ajustes de trimestre somam ZERO -- e e isso que preserva a restricao');
S.ordem.forEach((k) => {
  const e = S.eq[k];
  ok(e.saz.length === 4, k + ': quatro ajustes, um por trimestre do ano');
  const soma = e.saz.reduce((a, v) => a + v, 0);
  ok(Math.abs(soma) < 1e-5, k + ': os quatro somam zero (' + soma.toExponential(1) + ')');
  ok(e.rmse_sem_saz > e.rmse,
     k + ': sem eles o erro tipico PIORA (' + e.rmse_sem_saz + ' vs ' + e.rmse + ')');
  ok(e.r2_sem_saz < e.r2, k + ': e o movimento explicado cai');
});
// a restricao so fecha porque eles somam zero: um estado estacionario com os quatro
// trimestres visitados uma vez devolve a expectativa, e nada mais
{
  const e = S.eq.IS, b = coefDe('IS');
  const pi = 1.0;
  let media = 0;
  for (let q = 0; q < 4; q++) {
    media += (b.is1 * pi + b.is1b * pi + (1 - b.is1 - b.is1b) * pi + e.saz[q]) / 4;
  }
  ok(Math.abs(media - pi) < 1e-5,
     'IS: com tudo parado em pi, a media dos quatro trimestres devolve pi', String(media));
}
const tSaz = document.getElementById('tblSaz').innerHTML;
S.ordem.forEach((k) => ok(tSaz.indexOf(S.eq[k].nome) >= 0, 'a tabela tem a linha de ' + S.eq[k].nome));
S.rot_saz.forEach((r) => ok(tSaz.indexOf(r) >= 0, 'a tabela nomeia "' + r + '"'));
ok(document.getElementById('sazNota').textContent.length > 120, 'a nota dos ajustes tem conteudo');

// ── §16 ───────────────────────────────────────────────────────────────────────
secao('16. O diagnostico de residuo, e a prosa que ele manda escrever');
S.ordem.forEach((k) => {
  const e = S.eq[k];
  ok(e.acf.length === 6, k + ': perfil medido com seis defasagens');
  ok(e.lb_p4 >= 0 && e.lb_p4 <= 1, k + ': o resumo e uma probabilidade', String(e.lb_p4));
  ok(e.lb_q4 > 0, k + ': a estatistica do teste e positiva');
});
// a nota NAO pode ser escrita a mao: ela tem de concordar com o que os numeros dizem
{
  const ruins = S.ordem.filter((k) => S.eq[k].lb_p4 < 0.05);
  const nota = document.getElementById('acfNota').textContent;
  if (ruins.length === 0) {
    ok(nota.indexOf('Nenhuma das quatro') >= 0,
       'sem rejeicao: a nota diz que nenhuma rejeita', nota.slice(0, 120));
    ok(nota.indexOf('Ainda rejeita') < 0, 'e nao afirma o contrario');
  } else {
    ruins.forEach((k) => ok(nota.toLowerCase().indexOf(S.eq[k].nome.toLowerCase()) >= 0,
                            'a nota nomeia ' + S.eq[k].nome + ', que rejeita'));
  }
}
const tAcf = document.getElementById('tblAcf').innerHTML;
S.ordem.forEach((k) => ok(tAcf.indexOf(S.eq[k].nome) >= 0, 'o diagnostico tem a linha de ' + S.eq[k].nome));
ok(CRU.indexOf('1 - k/4') < 0 && CRU.indexOf('acf_janela') < 0,
   'o gabarito da janela de 12 meses sumiu do relatorio -- esta metrica nao o produz');

// ── §17 ───────────────────────────────────────────────────────────────────────
secao('17. As variantes de alimentacao: o teste esta registrado na tela');
ok(S.ia_variantes.length === 4, 'quatro formas testadas', String(S.ia_variantes.length));
ok(S.ia_variantes.filter((v) => v.escolhida).length === 1,
   'exatamente UMA esta marcada como em uso');
const maV = S.ia_variantes.filter((v) => v.theta != null);
ok(maV.length === 1, 'exatamente uma variante modela o residuo (MA(1))');
if (maV.length) {
  const base = S.ia_variantes.filter((v) => v.escolhida)[0];
  ok(maV[0].rmse > base.rmse,
     'o MA(1) ajusta PIOR que a forma escolhida', maV[0].rmse + ' vs ' + base.rmse);
  // o argumento MUDOU de metrica: antes era a janela, agora e o proprio diagnostico
  ok(S.eq.IA.lb_p4 >= 0.05,
     'e o diagnostico da forma escolhida ja diz que nao ha padrao a modelar (p '
     + S.eq.IA.lb_p4 + ')');
  ok(document.getElementById('iaNota').textContent.length > 200,
     'a nota explica o resultado do teste');
}
const tIA = document.getElementById('tblIA').innerHTML;
S.ia_variantes.forEach((v) => ok(tIA.indexOf(v.desc.slice(0, 20)) >= 0,
                                 'a tabela lista a forma "' + v.key + '"'));

// ── §18 ───────────────────────────────────────────────────────────────────────
secao('18. As ancoras de monitorados: o defeito esta declarado, nao escondido');
ok(S.im_ancoras.length >= 2, 'ao menos duas ancoras testadas', String(S.im_ancoras.length));
ok(S.im_ancoras.filter((a) => a.escolhida).length === 1, 'exatamente UMA em uso');
ok(S.im_ancoras.every((a) => a.b < 0),
   'todas dao peso NEGATIVO -- e isso que descarta a explicacao do horizonte');
{
  const esc = S.im_ancoras.filter((a) => a.escolhida)[0];
  ok(esc.peso_e <= 1,
     'a ancora em uso e a unica que mantem o peso da expectativa abaixo de 1',
     String(esc.peso_e));
  ok(Math.abs(esc.b - S.eq.IM.coef.filter((c) => c.key === 'im2')[0].b) < 1e-9,
     'a ancora marcada e mesmo a que a equacao publicada usa');
}
const tIM = document.getElementById('tblIM').innerHTML;
S.im_ancoras.forEach((a) => ok(tIM.indexOf(a.desc.slice(0, 18)) >= 0,
                               'a tabela lista a ancora "' + a.key + '"'));
{
  const nota = document.getElementById('imNota').textContent;
  ok(nota.length > 150, 'a nota explica a causa');
  const acima = S.im_ancoras.filter((a) => a.peso_e > 1).length;
  ok(nota.indexOf('em ' + acima + ' das ') >= 0,
     'a nota conta quantas ancoras estouram o peso da expectativa', nota.slice(0, 200));
}

// ── §19 ───────────────────────────────────────────────────────────────────────
secao('19. Os cinco graficos da aba seguem as regras de eixo, cabecalho e regua');
DIVS_SUB.forEach((div) => {
  const L = PLOT[div].layout;
  ok(L.yaxis.title === 'variação do trimestre, %', div + ': eixo Y define o que se mede',
     String(L.yaxis.title));
  ok(L.dragmode === 'pan', div + ": dragmode 'pan'");
  ok(!L.xaxis.rangeselector, div + ': sem rangeselector nativo');
  ok(Array.isArray(L.shapes) && Array.isArray(L.annotations),
     div + ': shapes e annotations SEMPRE passados');
  ok(PLOT[div].config.scrollZoom === true, div + ': scrollZoom ligado');

  const frame = document.getElementById(div).parentNode._chFrame;
  ok(!!frame, div + ': quadro de cabecalho pronto');
  if (frame) {
    ok((frame.sub.textContent || '').indexOf('variação do trimestre, %') >= 0,
       div + ': subtitulo imprime a mesma unidade do eixo', frame.sub.textContent);
    ok(/\d{4}T[1-4] a \d{4}T[1-4]/.test(frame.src.textContent || ''),
       div + ': periodo em trimestre', frame.src.textContent);
  }
  const bar = document.getElementById('rp-' + div);
  ok(!!bar && bar.children.length === 4, div + ': 4 botoes de range');
  const card = document.getElementById(div).parentNode;
  ok(card.children.indexOf(bar) > card.children.indexOf(document.getElementById(div)),
     div + ': a regua fica ABAIXO do grafico');
  const r = RELAYOUTS.filter((x) => x.div === div && x.upd['xaxis.range']);
  ok(r.length >= 1 && !('xaxis.autorange' in r[0].upd),
     div + ': primeira pintura com janela calculada');
});
// o grafico do cheio tem TRES linhas e a do piso e tracejada -- senao duas linhas
// cheias quase iguais viram uma so na tela
{
  const t = PLOT['ch-cheio'].traces;
  ok(t.length === 3, 'ch-cheio: realizado, soma dos ajustados e soma dos realizados',
     String(t.length));
  ok(t[2].line.dash === 'dash', 'ch-cheio: o piso entra tracejado (e referencia)');
  ok(PLOT['ch-cheio'].layout.showlegend === true, 'ch-cheio: com legenda (tem tres linhas)');
  for (let i = 0; i < 3; i++) {
    for (let j = i + 1; j < 3; j++) {
      if (t[i].line.dash !== t[j].line.dash) continue;
      const dd = deltaE(t[i].line.color, t[j].line.color);
      ok(dd >= 20, 'ch-cheio: ' + t[i].line.color + ' x ' + t[j].line.color
         + ' separadas (dE ' + dd.toFixed(1) + ')');
    }
  }
}
S.ordem.forEach((k) => {
  const card = document.getElementById('ch-sub-' + k).parentNode;
  const tools = card.children.filter((c) => c._cls().includes('card-tools'))[0];
  const bts = tools ? tools.children.filter((c) => c._cls().includes('info-btn')) : [];
  ok(bts.length === 1, 'ch-sub-' + k + ': um botao de definicao');
  ok(!!S.eq[k].desc && S.eq[k].desc.length > 60, k + ': a explicacao tem conteudo');
  ok(S.eq[k].full !== S.eq[k].nome, k + ': `full` difere do rotulo curto');
});
ok(document.getElementById('ch-cheio').parentNode.children
     .filter((c) => c._cls().includes('card-tools'))[0]
     .children.filter((c) => c._cls().includes('info-btn')).length === 0,
   'ch-cheio: sem botao de definicao (nao e um grupo)');

// ── §20 ───────────────────────────────────────────────────────────────────────
secao('20. A tabela de pesos imprime o que o payload traz');
{
  const t = document.getElementById('tblSubCoef').innerHTML;
  S.ordem.forEach((k) => {
    ok(t.indexOf(S.eq[k].nome) >= 0, 'a tabela tem a secao de ' + S.eq[k].nome);
    S.eq[k].coef.forEach((c) => {
      ok(t.indexOf(c.rot) >= 0, k + ': a linha "' + c.rot + '" esta impressa');
    });
  });
  ok(t.indexOf('†') >= 0, 'a marca dos pesos restritos existe');
  ok(document.getElementById('subCoefNota').textContent.indexOf('†') === 0,
     'e a nota explica a marca');

  // o peso da expectativa TEM linha propria, e ela se declara conta de sobra.
  // O formatador e local de proposito: usar o da pagina faria os dois lados mutarem
  // juntos e a asserção viraria tautologia.
  const _f = (v, d) => v.toFixed(d).replace('.', ',');
  const LINHAS = t.split('<tr').filter((r) => r.indexOf('Peso da expectativa') >= 0);
  ok(LINHAS.length === S.ordem.length,
     'uma linha de peso da expectativa por grupo', String(LINHAS.length));
  LINHAS.forEach((r) => {
    ok(r.indexOf('‡') >= 0, 'a linha de sobra tem a marca propria');
    ok(r.indexOf('conta de sobra: 1') >= 0, 'e diz que e conta de sobra, com a subtracao');
    ok(r.indexOf('class="sig"') < 0 && r.indexOf('class="insig"') < 0,
       'a linha de sobra NAO recebe leitura de significancia: nao ha t para ela');
    ok(r.indexOf('<td>—</td><td>—</td>') >= 0,
       'e nao inventa margem nem t para um numero que nao foi estimado');
  });
  S.ordem.forEach((k, i) => {
    const e = S.eq[k], r = LINHAS[i];
    ok(r.indexOf(_f(e.peso_e, 4)) >= 0,
       k + ': a linha imprime o peso da expectativa do payload', _f(e.peso_e, 4));
    const rest = e.coef.filter((c) => c.restrito);
    let conta = 1;
    rest.forEach((c) => { conta -= c.b; });
    ok(Math.abs(conta - e.peso_e) < 1e-6, k + ': a subtracao mostrada fecha no peso');
    rest.forEach((c) => {
      ok(r.indexOf(_f(Math.abs(c.b), 4)) >= 0,
         k + ': a parcela ' + c.rot + ' aparece na subtracao');
    });
    // sinal: um peso restrito NEGATIVO entra somando na conta de sobra
    rest.filter((c) => c.b < 0).forEach(() => {
      ok(r.indexOf('1 − ') >= 0 && r.indexOf(' + ') >= 0,
         k + ': o peso negativo entra somando (1 - a - (-b) = 1 - a + b)');
    });
  });
  // e o cabecalho do grupo NAO repete o numero que agora tem linha
  ok(t.indexOf('peso da expectativa ' + _f(S.eq[S.ordem[0]].peso_e, 3)) < 0,
     'o cabecalho do grupo nao diz o peso duas vezes');
  ok(document.getElementById('subCoefNota').textContent.indexOf('‡') > 0,
     'e a nota explica a marca da conta de sobra');
  // nenhum coeficiente de ajuste de trimestre vaza para a tabela de pesos: eles tem a sua
  ok(!S.ordem.some((k) => S.eq[k].coef.some((c) => /^s[123]$/.test(c.key))),
     'os ajustes de trimestre NAO entram na tabela de pesos');
}

// ── §21 ───────────────────────────────────────────────────────────────────────
secao('21. O seletor de leitura: o trimestre e o mesmo numero em doze meses');
ok(!!document.getElementById('pillTri') && !!document.getElementById('pill12'),
   'as duas pills existem');
ok(ctx.VISTA_SUB === 'tri', 'a aba abre no trimestre, que e onde os pesos foram medidos',
   String(ctx.VISTA_SUB));
ok(/id="pillTri"[^>]*>|class="vista-pill active" id="pillTri"/.test(CRU)
   && CRU.indexOf('class="vista-pill active" id="pillTri"') >= 0,
   'e o markup ja entrega a pill do trimestre marcada');
ok(S.janela === 4, 'a janela de leitura e de quatro trimestres', String(S.janela));
ok(S.x12.length === S.x.length - (S.janela - 1),
   'a leitura de 12 meses perde so os ' + (S.janela - 1) + ' primeiros trimestres, '
   + 'que sao os que nao tem janela completa atras',
   S.x12.length + ' contra ' + S.x.length);
// cada janela cobre UM de cada trimestre do ano -- e por isso que o ajuste sazonal,
// que soma zero no ano, nao sobra na leitura de doze meses
{
  let ruim = 0;
  S.x12.forEach((d) => {
    const t = POS12[d], vistos = {};
    for (let h = 0; h < S.janela; h++) vistos[triDe(S.rot[t - h])] = 1;
    if (Object.keys(vistos).length !== 4) ruim++;
  });
  ok(ruim === 0, 'toda janela cobre os quatro trimestres do ano uma vez -- e o que faz '
     + 'a sazonalidade, que soma zero, sair da leitura de 12 meses');
}
ok(S.x12[S.x12.length - 1] === S.x[S.x.length - 1],
   'e termina no mesmo trimestre que a leitura trimestral');

// o realizado em 12 meses, ENCADEADO aqui a partir do trimestral do payload
{
  let pior = 0;
  S.x12.forEach((d, i) => {
    const t = POS12[d];
    let f = 1;
    for (let h = 0; h < S.janela; h++) f *= 1 + S.cheio.obs[t - h] / 100;
    pior = Math.max(pior, Math.abs((f - 1) * 100 - S.cheio.obs12[i]));
  });
  ok(pior < 0.002, 'o realizado em 12 meses e o encadeamento dos quatro trimestres (erro max '
     + pior.toFixed(5) + ')');
  // ENCADEAR, nao somar: a soma dos quatro tem de ficar VISIVELMENTE longe
  let dif = 0;
  S.x12.forEach((d, i) => {
    const t = POS12[d];
    let soma = 0;
    for (let h = 0; h < S.janela; h++) soma += S.cheio.obs[t - h];
    dif = Math.max(dif, Math.abs(soma - S.cheio.obs12[i]));
  });
  ok(dif > 0.3, 'somar os quatro em vez de encadear daria outro numero (ate '
     + dif.toFixed(3) + ' p.p. de diferenca)');
}
// O GABARITO: o nosso encadeamento contra o IPCA de 12 meses PUBLICADO. E a unica
// conferencia da pagina contra um numero que nao saiu daqui.
{
  let pior = 0, n = 0;
  S.cheio.ref12.forEach((v, i) => {
    if (v == null) return;
    pior = Math.max(pior, Math.abs(v - S.cheio.obs12[i])); n++;
  });
  ok(n > 50, 'o gabarito cobre ' + n + ' janelas');
  ok(pior < 0.05, 'o realizado em 12 meses bate com o IPCA 12m publicado (erro max '
     + pior.toFixed(4) + ' p.p.)');
}
// NAO ha previsao aqui: a linha de 12 meses e o MESMO ajuste trimestral do payload,
// encadeado de quatro em quatro. Refeito no teste, para todos os cinco blocos.
{
  let pior = 0, n = 0;
  S.x12.forEach((d, i) => {
    const t = POS12[d];
    let f = 1;
    for (let h = 0; h < S.janela; h++) f *= 1 + S.cheio.fit[t - h] / 100;
    pior = Math.max(pior, Math.abs((f - 1) * 100 - S.cheio.aj12[i])); n++;
  });
  ok(n > 80, 'o cheio em 12 meses foi refeito em ' + n + ' janelas');
  ok(pior < 0.002, 'a linha de 12 meses E o ajuste trimestral encadeado -- nada e '
     + 'simulado e nada realimenta (erro max ' + pior.toFixed(6) + ')');
  // e o mutante que volta a iterar a equacao erra MUITO mais do que essa tolerancia:
  // a soma dos quatro, que e a outra leitura errada possivel, ja difere aqui
  let soma = 0;
  S.x12.forEach((d, i) => {
    const t = POS12[d];
    let acc = 0;
    for (let h = 0; h < S.janela; h++) acc += S.cheio.fit[t - h];
    soma = Math.max(soma, Math.abs(acc - S.cheio.aj12[i]));
  });
  // o limiar e menor que o do realizado (0,86) porque o ajustado e mais liso, e o
  // cruzado da composicao depende da dispersao dentro da janela
  ok(soma > 0.15, 'somar os quatro ajustados em vez de encadear daria outro numero (ate '
     + soma.toFixed(3) + ' p.p., cem vezes a tolerancia da assercao acima)');
}
// A corrente inteira numa assercao so: coeficientes publicados -> ajuste do trimestre
// -> sazonal do trimestre do rotulo -> os quatro encadeados. Se qualquer elo se mover,
// esta conta deixa de fechar.
{
  const b = coefDe('IS'), e = S.eq.IS;
  const aj = [];
  for (let i = 0; i < S.x.length; i++) {
    if (i < 4) { aj.push(null); continue; }
    const t = POS2[S.x[i]];
    const mm4 = (e.obs[i - 1] + e.obs[i - 2] + e.obs[i - 3] + e.obs[i - 4]) / 4;
    aj.push(b.is1 * e.obs[i - 1] + b.is1b * mm4
            + (1 - b.is1 - b.is1b) * (D.s.pi_e[t - 1] / 4)
            + b.is2 * D.s.hiato[t] + e.saz[triDe(S.rot[i]) - 1]);
  }
  let pior = 0, n = 0;
  S.x12.forEach((d, i) => {
    const t = POS12[d];
    if (t < 4 + S.janela - 1) return;
    let f = 1;
    for (let h = 0; h < S.janela; h++) f *= 1 + aj[t - h] / 100;
    pior = Math.max(pior, Math.abs((f - 1) * 100 - e.aj12[i])); n++;
  });
  ok(n > 70, 'IS: a corrente foi refeita dos coeficientes em ' + n + ' janelas');
  ok(pior < 0.05, 'IS: coeficientes -> ajuste do trimestre -> sazonal -> 12 meses, a '
     + 'corrente inteira fecha (erro max ' + pior.toFixed(4) + ' p.p.)');
}
// O ajuste de calendario e GRANDE no trimestre e some na janela de doze meses -- que e
// o que a codificacao soma-zero garante e o que torna a leitura anual comparavel a uma
// serie dessazonalizada, sem nenhum filtro rodando. Medido aqui pelos dois lados.
S.ordem.forEach((k) => {
  const e = S.eq[k];
  const amp = Math.max.apply(null, e.saz) - Math.min.apply(null, e.saz);
  let pior = 0;
  S.x12.forEach((d, i) => {
    const t = POS12[d];
    let f = 1;
    for (let h = 0; h < S.janela; h++) {
      f *= 1 + (e.fit[t - h] - e.saz[triDe(S.rot[t - h]) - 1]) / 100;
    }
    pior = Math.max(pior, Math.abs((f - 1) * 100 - e.aj12[i]));
  });
  ok(amp > 0.5, k + ': o ajuste de calendario move ' + amp.toFixed(2)
     + ' p.p. dentro do trimestre');
  ok(pior < 0.1, k + ': e sobra ' + pior.toFixed(4) + ' p.p. na leitura de 12 meses -- '
     + 'os quatro somam zero, entao a estacao sai sozinha da janela');
  ok(pior < amp / 5, k + ': o que sobra e uma fracao do que o ajuste vale no trimestre');
});
ok(S.cheio.rmse12 > S.cheio.rmse,
   'o erro em 12 meses e maior, porque e a soma de quatro erros trimestrais dentro da '
   + 'janela (' + S.cheio.rmse12 + ' contra ' + S.cheio.rmse + ')');
ok(S.cheio.rmse12 < 4 * S.cheio.rmse,
   'e menor que quatro vezes ele: os erros trimestrais nao andam todos juntos');
S.ordem.forEach((k) => {
  const e = S.eq[k];
  ok(e.obs12.length === S.x12.length && e.aj12.length === S.x12.length,
     k + ': a leitura de 12 meses cobre as mesmas janelas');
  ok(e.rmse12 > e.rmse, k + ': o erro acumulado do ano e maior que o de um trimestre');
});

// ── o clique troca de verdade: series, eixo, titulo, regua e cartoes ─────────
const ANTES = {
  eixo: PLOT['ch-cheio'].layout.yaxis.title,
  titulo: document.getElementById('ch-cheio').parentNode._chFrame.title.textContent,
  y0: PLOT['ch-cheio'].traces[0].y.length,
  stats: document.getElementById('subStats').innerHTML,
  nota: document.getElementById('vistaNota').textContent,
};
document.getElementById('pill12').dispatch('click');
ok(document.getElementById('pill12')._cls().includes('active'), 'a pill de 12 meses ativa');
ok(!document.getElementById('pillTri')._cls().includes('active'), 'e a do trimestre desativa');
DIVS_SUB.forEach((div) => {
  ok(PLOT[div].layout.yaxis.title === 'variação em 12 meses, %',
     div + ': o eixo passa a dizer 12 meses', String(PLOT[div].layout.yaxis.title));
  ok(PLOT[div].traces[0].y.length === S.x12.length,
     div + ': as series sao as da janela de 12 meses');
  // e sao as series CERTAS: a payload estar correta nao garante que o grafico leia dela.
  // O mutante que plota o realizado duas vezes passa por todo o resto desta secao.
  {
    const alvo = div === 'ch-cheio' ? S.cheio : S.eq[div.slice('ch-sub-'.length)];
    const t0 = PLOT[div].traces[0].y, t1 = PLOT[div].traces[1].y;
    const igual = (a, b) => a.every((v, i) => v === b[i]);
    ok(igual(t0, alvo.obs12), div + ': a primeira linha e o realizado em 12 meses');
    ok(igual(t1, alvo.aj12), div + ': a segunda e o ajuste encadeado em 12 meses');
    ok(!igual(t1, alvo.obs12),
       div + ': e as duas NAO sao a mesma serie desenhada duas vezes');
  }
  const fr = document.getElementById(div).parentNode._chFrame;
  ok((fr.sub.textContent || '').indexOf('variação em 12 meses, %') >= 0,
     div + ': o subtitulo acompanha', fr.sub.textContent);
  // a regua tem de ser REFEITA: as duas leituras comecam em trimestres diferentes
  const r = RELAYOUTS.filter((x) => x.div === div && x.upd['xaxis.range']);
  const ult = r[r.length - 1].upd['xaxis.range'];
  ok(Date.parse(ult[0]) >= Date.parse(S.x12[0]) - 200 * 864e5,
     div + ': a janela aplicada comeca dentro da leitura de 12 meses', String(ult[0]));
});
ok(document.getElementById('ch-cheio').parentNode._chFrame.title.textContent !== ANTES.titulo,
   'o titulo do grafico muda -- um clique aqui muda o que ele AFIRMA');
ok(document.getElementById('ch-cheio').parentNode._chFrame.title.textContent
     .indexOf('12 meses') >= 0, 'e o titulo novo nomeia a leitura');
ok(document.getElementById('subStats').innerHTML !== ANTES.stats,
   'os cartoes de resumo trocam');
ok(document.getElementById('subStats').innerHTML.indexOf(String(S.cheio.rmse12).replace('.', ',')
   .slice(0, 4)) >= 0 || document.getElementById('subStats').innerHTML.indexOf('doze meses') >= 0,
   'e passam a falar da leitura de doze meses');
ok(document.getElementById('vistaNota').textContent !== ANTES.nota,
   'a nota do seletor e reescrita');
{
  const nt = document.getElementById('vistaNota').textContent;
  ok(nt.indexOf('Nada \u00e9 projetado') >= 0,
     'e diz, na tela, que nada e projetado -- e a diferenca que a vista inteira depende',
     nt.slice(0, 80));
  ok(nt.indexOf(String(S.janela)) >= 0,
     'e a nota nomeia a janela lendo do payload, em vez de ter o 4 escrito a mao');
  ok(nt.indexOf('previs') < 0 && nt.indexOf('Previs') < 0,
     'e a palavra previsao NAO aparece: esta vista nao preve nada', nt.slice(0, 80));
}
// no cheio a terceira linha vira o gabarito publicado, e segue tracejada
{
  const t = PLOT['ch-cheio'].traces;
  ok(t.length === 3, 'ch-cheio: tres linhas tambem na leitura de 12 meses');
  ok(t[2].line.dash === 'dash', 'ch-cheio: o gabarito publicado entra tracejado');
  ok(t[2].name.indexOf('publicado') >= 0, 'ch-cheio: e ele e nomeado como publicado',
     t[2].name);
}
// e voltar restaura
document.getElementById('pillTri').dispatch('click');
ok(PLOT['ch-cheio'].layout.yaxis.title === ANTES.eixo, 'voltar ao trimestre restaura o eixo');
ok(PLOT['ch-cheio'].traces[0].y.length === ANTES.y0, 'e as series do trimestre');
ok(document.getElementById('ch-cheio').parentNode._chFrame.title.textContent === ANTES.titulo,
   'e o titulo');
// clicar na pill ja ativa nao redesenha
{
  const n = RELAYOUTS.length;
  document.getElementById('pillTri').dispatch('click');
  ok(RELAYOUTS.length === n, 'clicar na pill ja ativa nao faz nada');
}

// ── §22 ───────────────────────────────────────────────────────────────────────
secao('22. O click-drop de notacao: a matematica sai do MESMO payload');
{
  const _f = (v, d) => v.toFixed(d).replace('.', ',');
  // o sinal e o numero ficam separados por uma tag, entao "+ menos" so aparece no
  // TEXTO -- procurar no markup nunca casa, e o mutante passa
  const _txt = (h) => h.replace(/<[^>]*>/g, '');
  const SIMB = document.getElementById('subMathSimb').innerHTML;
  const NUM = document.getElementById('subMathNum').innerHTML;
  const LEG = document.getElementById('subMathLeg').innerHTML;

  ok(/<details[^>]*id="subMathFold"/.test(CRU), 'o bloco e um <details>, ou seja, click-drop');
  ok(CRU.indexOf('nota\u00e7\u00e3o matem\u00e1tica') >= 0, 'e o summary diz o que abre');

  S.ordem.forEach((k) => {
    ok(SIMB.indexOf('(' + k + ')') >= 0, k + ': tem equacao simbolica');
    ok(NUM.indexOf('(' + k + ')') >= 0, k + ': tem equacao com numeros');
  });

  // cada equacao numerica imprime O PESO DO PAYLOAD de cada termo, inclusive a sobra
  const porEq = NUM.split('<span class="tag">').slice(1);
  ok(porEq.length === S.ordem.length, 'uma linha numerica por grupo');
  S.ordem.forEach((k, i) => {
    const e = S.eq[k], linha = porEq[i];
    e.coef.forEach((c) => {
      ok(linha.indexOf(_f(Math.abs(c.b), 4)) >= 0,
         k + ' / ' + c.key + ': o peso esta na equacao numerica');
    });
    ok(linha.indexOf(_f(Math.abs(e.peso_e), 4)) >= 0,
       k + ': o peso da expectativa esta na equacao numerica');
    ok(_txt(linha).indexOf('+ −') < 0 && _txt(linha).indexOf('+ -') < 0,
       k + ': um peso negativo vira subtracao, nunca "+ menos"',
       _txt(linha).slice(0, 90));
    // a expectativa entra DIVIDIDA por 4, como na conta
    ok(linha.indexOf('<sub>t−1</sub>/4') >= 0,
       k + ': a expectativa entra dividida por quatro tambem na notacao');
  });

  // a forma simbolica: a restricao aparece como (1 - os pesos), nao como parametro livre
  const porEqS = SIMB.split('<span class="tag">').slice(1);
  S.ordem.forEach((k, i) => {
    const e = S.eq[k], linha = porEqS[i];
    const nrest = e.coef.filter((c) => c.restrito).length;
    const esperado = '(1 ' + '− '.repeat(nrest).trim();
    ok(linha.indexOf('(1 −') >= 0,
       k + ': o peso da expectativa aparece como 1 menos os outros, e nao como simbolo proprio');
    ok((linha.slice(linha.indexOf('(1 −')).split('−').length - 1) >= nrest,
       k + ': com uma subtracao por peso restrito (' + nrest + ')', esperado);
  });

  // a restricao imposta: a expectativa subtraida dos DOIS lados
  const R = document.getElementById('subMathRestr').innerHTML;
  ok(R.split('<i>E</i><sub>t−1</sub>/4').length - 1 >= 3,
     'a expectativa aparece dos dois lados da forma estimada');
  ok(R.indexOf('= <i>E</i>/4') >= 0, 'e o estado de repouso devolve a expectativa');

  // dois regressores da MESMA equacao nao podem dividir simbolo: a equacao ficaria
  // ambigua e a legenda, que deduplica, perderia uma das duas definicoes
  S.ordem.forEach((k) => {
    const usados = {};
    S.eq[k].coef.forEach((c) => {
      const sim = ctx._mv(c);
      ok(!usados[sim], k + ': ' + c.key + ' tem simbolo proprio, diferente de '
         + (usados[sim] || 'qualquer outro da equacao'), _txt(sim));
      usados[sim] = c.key;
    });
  });

  // a legenda cobre TODO simbolo usado, porque sai do mesmo mapa
  S.ordem.forEach((k) => {
    S.eq[k].coef.forEach((c) => {
      const sim = ctx._mv(c);
      ok(SIMB.indexOf(sim) >= 0, k + ' / ' + c.key + ': o simbolo esta na equacao');
      ok(LEG.indexOf(sim) >= 0, k + ' / ' + c.key + ': e tem definicao na legenda');
    });
  });
  ok(LEG.indexOf('<i>E</i><sub>t−1</sub>/4') >= 0, 'a expectativa tem definicao');
  ok(LEG.indexOf('não anualizada') >= 0, 'a legenda diz a unidade das dependentes');

  // o ajuste de trimestre: nq-1 colunas estimadas, a ultima derivada, soma zero
  const SZ = document.getElementById('subMathSaz').innerHTML;
  const nq = S.rot_saz.length;
  ok(SZ.indexOf('<sup>' + (nq - 1) + '</sup>') >= 0,
     'a soma da forma estimada vai ate ' + (nq - 1) + ', nao ate ' + nq);
  ok(SZ.indexOf('1{q(t) = ' + nq + '}') >= 0, 'a referencia e o ultimo trimestre do ano');
  ok(SZ.indexOf('= 0') >= 0, 'e os quatro somam zero');

  // a volta ao cheio e o encadeamento
  const F = document.getElementById('subMathFechos').innerHTML;
  ok(F.indexOf('= 1') >= 0, 'os pesos dos grupos somam um');
  ok(F.indexOf('<sup>' + (S.janela - 1) + '</sup>') >= 0,
     'o produtorio de doze meses vai de 0 a ' + (S.janela - 1));
  ok(F.indexOf('∏') >= 0 && F.indexOf('/ 100 ) − 1 ] × 100') >= 0,
     'e ele MULTIPLICA os quatro trimestres, nao soma');
  ok(F.indexOf('∑<sub>j') < 0, 'nada de somatorio no encadeamento de doze meses');
}

// ── §23 ───────────────────────────────────────────────────────────────────────
secao('23. A aba de expectativas: a conta (E)');
const E = D.exp;
ok(!!E, 'o payload traz a equacao de expectativas');
ok(CRU.indexOf('data-tab="tab-exp"') >= 0, 'a aba existe no markup');

{
  const _f = (v, d) => v.toFixed(d).replace('.', ',');

  // ── a forma e a do plano da pasta, e NADA alem dela. Esta secao existe tanto
  //    para conferir a conta quanto para impedir que a especificacao cresca sem
  //    que alguem tenha pedido: `E(t) = e1 E(t-1) + e2 I12(t) + (1-e1-e2) Meta(t)`.
  ok(E.coef.length === 2, 'a conta tem exatamente dois pesos estimados',
     String(E.coef.length));
  ok(E.coef.map((c) => c.key).join(',') === 'e1,e2',
     'e eles sao a defasagem da expectativa e a inflacao, nessa ordem',
     E.coef.map((c) => c.key).join(','));
  ok(E.coef.every((c) => c.restrito),
     'os dois dividem a soma-um com a meta: nao ha termo livre');
  ok(E.saz === undefined && E.variantes === undefined,
     'e o payload nao carrega ajuste de trimestre nem escada de leituras');

  let soma = 0;
  E.coef.forEach((c) => { soma += c.b; });
  ok(Math.abs(soma + E.peso_meta - 1) < 1e-6,
     'os pesos estimados e o da meta somam 1', String(soma + E.peso_meta));

  // ── o efeito de longo prazo e do termo de INFLACAO, nao da defasagem
  const cInf = E.coef.filter((c) => c.key === 'e2')[0];
  const cLag = E.coef.filter((c) => c.key === 'e1')[0];
  ok(cInf.lp != null, 'o termo de inflacao tem efeito de longo prazo proprio');
  ok(cLag.lp == null,
     'e a defasagem da expectativa nao: ela PRODUZ o acumulo, nao o sofre');

  // ── o repouso devolve a meta, e o repasse bate com a formula
  ok(E.repouso.devolve_a_meta === true, 'em repouso a conta devolve a meta');
  ok(Math.abs(E.repouso.simulado - E.repouso.formula) < 1e-5,
     'o repasse simulado bate com a formula',
     E.repouso.simulado + ' vs ' + E.repouso.formula);
  ok(Math.abs(E.repasse - cInf.b / (1 - cLag.b)) < 1e-5,
     'o repasse e o peso da inflacao sobre um menos a defasagem',
     E.repasse + ' vs ' + (cInf.b / (1 - cLag.b)));
  ok(Math.abs(E.soma_inercia - cLag.b) < 1e-6, 'a soma das defasagens bate');
  ok(E.repasse > 0 && E.repasse < 1,
     'e ele fica entre zero e um: nem ancora perfeita nem expectativa puramente '
     + 'adaptativa', String(E.repasse));

  // ── a meia-vida: simular o AR restrito tem de reproduzir o numero publicado
  {
    let h = [1, 1];
    const phis = [cLag.b];
    let achou = null;
    for (let t = 0; t < 200 && achou === null; t++) {
      const v = phis.reduce((a, p, i) => a + p * h[h.length - 1 - i], 0);
      h.push(v);
      if (Math.abs(v) <= 0.5) achou = t + 1;
    }
    ok(achou === E.meia_vida, 'a meia-vida publicada e a que o AR restrito produz',
       achou + ' vs ' + E.meia_vida);
  }

  // ── a decomposicao e IDENTIDADE: parcelas + residuo == desvio observado
  {
    let pior = 0;
    for (let i = 0; i < E.x.length; i++) {
      let soma2 = 0;
      Object.keys(E.contrib).forEach((k) => {
        if (E.contrib[k]) soma2 += E.contrib[k][i];
      });
      const desvio = E.obs[i] - E.meta[i];
      pior = Math.max(pior, Math.abs(soma2 + E.resid[i] - desvio));
    }
    // 1e-3 e o arredondamento do payload (4 casas em varias parcelas), nao folga
    ok(pior < 1e-3, 'a decomposicao fecha: as parcelas mais o erro dao a distancia '
       + 'ate a meta (pior ' + pior.toExponential(1) + ')');
    ok(pior > 0, 'e a identidade nao e trivial: as parcelas sao numeros distintos');
  }
  // e o ajustado e mesmo a soma das parcelas com a meta
  {
    let pior = 0;
    for (let i = 0; i < E.x.length; i++) {
      let soma2 = E.meta[i];
      Object.keys(E.contrib).forEach((k) => {
        if (E.contrib[k]) soma2 += E.contrib[k][i];
      });
      pior = Math.max(pior, Math.abs(soma2 - E.fit[i]));
    }
    ok(pior < 1e-3, 'e a conta e a meta mais as parcelas (pior '
       + pior.toExponential(1) + ')');
  }

  // ── a meta e a do HORIZONTE de 12 meses, nao a do ano-calendario.
  // Com a mistura, os quatro trimestres de um ano de transicao de meta tem valores
  // DIFERENTES; com a meta do ano eles seriam iguais, e nada mais na pagina diria.
  {
    const porAno = {};
    E.rot.forEach((r, i) => {
      const ano = r.slice(0, 4);
      (porAno[ano] = porAno[ano] || []).push(E.meta[i]);
    });
    const variam = Object.keys(porAno).filter((a) => {
      const v = porAno[a];
      return v.length > 1 && Math.max.apply(null, v) - Math.min.apply(null, v) > 1e-6;
    });
    ok(variam.length > 0,
       'a meta anda DENTRO do ano nas transicoes de meta, como a pesquisa',
       variam.length + ' anos de ' + Object.keys(porAno).length);
  }

  // ── a amostra e mais LONGA que a da curva de Phillips, e isso e o ponto
  ok(E.n > D.sub.n, 'a amostra de (E) e maior que a da curva de Phillips',
     E.n + ' vs ' + D.sub.n);
  ok(E.x[0] < D.sub.x[0], 'e comeca antes', E.ini + ' vs ' + D.sub.ini);

  // ── os cartoes
  const st = document.getElementById('expStats').innerHTML;
  ok((st.match(/stat-card/g) || []).length === 4, 'quatro cartoes de resumo');
  ok(st.indexOf(_f(E.peso_meta, 3)) >= 0, 'o cartao imprime o peso da meta');
  ok(st.indexOf(_f(E.repasse, 2)) >= 0, 'e o repasse de longo prazo');
  ok(st.indexOf(_f(E.bc.meta.v, 3)) >= 0,
     'e poe o numero do Banco Central ao lado do peso da meta');

  // ── a tabela de pesos, com a linha de sobra da meta
  const tc = document.getElementById('tblExpCoef').innerHTML;
  E.coef.forEach((c) => {
    ok(tc.indexOf(c.rot) >= 0, 'a linha "' + c.rot + '" esta impressa');
  });
  const sobra = tc.split('<tr').filter((r) => r.indexOf('Peso da meta') >= 0);
  ok(sobra.length === 1, 'uma linha de peso da meta, marcada como conta de sobra');
  ok(sobra[0].indexOf('‡') >= 0 && sobra[0].indexOf('conta de sobra: 1') >= 0,
     'com a marca e a subtracao inteira');
  ok(sobra[0].indexOf('<td>—</td><td>—</td>') >= 0,
     'e sem margem nem t inventados');
  E.coef.forEach((c) => {
    ok(sobra[0].indexOf(' − ' + _f(c.b, 4)) >= 0,
       'o peso de ' + c.key + ' entra SUBTRAINDO na conta de sobra',
       sobra[0].replace(/<[^>]*>/g, '').trim().slice(0, 80));
  });
  // Nesta forma os dois pesos sao positivos, entao a regra do sinal so e exercitada
  // injetando um negativo: sem isto, trocar `+` por `−` no gerador passa verde.
  {
    const orig = E.coef[1].b;
    E.coef[1].b = -orig;
    ctx.renderExpCoef();
    const s2 = document.getElementById('tblExpCoef').innerHTML
      .split('<tr').filter((r) => r.indexOf('Peso da meta') >= 0)[0];
    ok(s2.indexOf(' + ' + _f(orig, 4)) >= 0,
       'e um peso NEGATIVO entraria somando, nao subtraindo',
       s2.replace(/<[^>]*>/g, '').trim().slice(0, 80));
    E.coef[1].b = orig;
    ctx.renderExpCoef();
  }
  ok(document.getElementById('expCoefNota').textContent.indexOf('†') === 0,
     'a nota explica as duas marcas');

  // ── a notacao: gerada do payload, e a legenda cobre todo simbolo
  const MS = document.getElementById('expMathSimb').innerHTML;
  const MN = document.getElementById('expMathNum').innerHTML;
  const ML = document.getElementById('expMathLeg').innerHTML;
  ok(/<details[^>]*id="expMathFold"/.test(CRU), 'o bloco de notacao e um click-drop');
  ok(MS.indexOf('(1 −') >= 0,
     'o peso da meta aparece como 1 menos os outros, nao como simbolo proprio');
  ok(MS.indexOf('<sub>q(t)</sub>') < 0,
     'e nao ha ajuste de trimestre na equacao escrita');
  {
    const usados = {};
    E.coef.forEach((c) => {
      const sim = ctx._mvE(c);
      ok(!usados[sim], c.key + ' tem simbolo proprio', sim.replace(/<[^>]*>/g, ''));
      usados[sim] = c.key;
      ok(MS.indexOf(sim) >= 0, c.key + ': o simbolo esta na equacao');
      ok(ML.indexOf(sim) >= 0, c.key + ': e tem definicao na legenda');
      ok(MN.indexOf(_f(Math.abs(c.b), 4)) >= 0,
         c.key + ': o peso esta na equacao numerica');
    });
  }
  ok(MN.indexOf(_f(Math.abs(E.peso_meta), 4)) >= 0,
     'e o peso da meta tambem esta na equacao numerica');
  ok(MN.replace(/<[^>]*>/g, '').indexOf('+ −') < 0,
     'um peso negativo vira subtracao, nunca "+ menos"');
  ok(ML.indexOf('Meta<sub>t</sub>') >= 0, 'a meta tem definicao na legenda');
  const MR = document.getElementById('expMathRestr').innerHTML;
  ok(MR.split('Meta<sub>t</sub>').length - 1 >= 3,
     'a meta aparece dos dois lados da forma estimada');
  ok(MR.indexOf('= Meta') >= 0, 'e o repouso devolve a meta');

  // ── o diagnostico de residuo: o que a pagina DIZ e o que o teste mede tem de ser
  //    a mesma coisa, nos quatro lugares em que ela fala do erro
  {
    const sobraErro = E.lb_p4 < 0.05;
    ok(sobraErro,
       'nesta forma o erro AINDA TEM padrao -- e o fato que as quatro frases abaixo '
       + 'precisam dizer', 'p ' + E.lb_p4);
    const ta = document.getElementById('tblExpAcf').innerHTML;
    ok(ta.indexOf(sobraErro ? 'ainda sobra padrão' : 'nada sobrando') >= 0,
       'a tabela de erro diz o que o teste mediu');
    const na = document.getElementById('expAcfNota').textContent || '';
    ok(na.indexOf(sobraErro ? 'acusam padrão sobrando' : 'Nenhum dos dois testes') >= 0,
       'e a nota ao lado dela diz a mesma coisa');
    ok(st.indexOf(sobraErro ? 'ainda sobra padrão no erro'
                            : 'sem padrão de erro sobrando') >= 0,
       'e o cartao de erro tipico tambem');
    const fi = String(document.getElementById('expFicha').innerHTML)
      .replace(/<[^>]*>/g, '');
    ok((fi.indexOf('ainda tem padrão') >= 0) === sobraErro,
       'e a ficha de abertura nao promete um erro limpo que a conta nao tem');
  }

  // ── a comparacao com o BC, e a ressalva na propria linha
  const tb = document.getElementById('tblExpBc').innerHTML;
  ok(tb.indexOf(_f(E.bc.f1.v, 3)) >= 0 && tb.indexOf(_f(E.bc.meta.v, 3)) >= 0,
     'a tabela do BC imprime os pesos publicados');
  {
    const linhas = tb.split('<tr').filter((r) => r.indexOf('<td>') >= 0);
    const naoComp = linhas.filter((r) => r.indexOf('outro objeto') >= 0);
    ok(naoComp.length === 1,
       'exatamente uma linha marcada como nao comparavel', String(naoComp.length));
    ok(naoComp[0].indexOf(_f(E.bc.f2.v, 3)) >= 0,
       'e ela e a da previsao do proprio modelo');
    const f3 = linhas.filter((r) => r.indexOf(_f(E.bc.f3.v, 3)) >= 0)[0];
    ok(!!f3 && f3.indexOf('<td>—</td>') >= 0,
       'e o termo que a nossa conta NAO tem aparece sem numero nosso');
  }
  {
    const nb = document.getElementById('expBcNota').textContent || '';
    ok(nb.indexOf('previsão que o próprio modelo faz') >= 0,
       'a nota diz O QUE e o termo do BC: a previsao do proprio modelo');
    ok(nb.indexOf('olha para frente') >= 0, 'e que ele olha para frente');
    ok(nb.indexOf('vale a comparação direta') < 0
       && nb.indexOf('são coisas diferentes') >= 0,
       'e nao sugere que a comparacao direta valha');
  }

  // ── a prosa da aba nao vaza vocabulario de dentro do repositorio
  // a prosa pode ter sido escrita por textContent OU por innerHTML; ler so um dos
  // dois deixa metade dos blocos fora do guarda sem que nada falhe
  const _txtOf = (id) => {
    const el = document.getElementById(id);
    return String(el.textContent || '') + ' '
         + String(el.innerHTML || '').replace(/<[^>]*>/g, '');
  };
  ['expFicha', 'expCoefNota', 'expAcfNota', 'expBcNota', 'expMathNota']
    .forEach((id) => {
      ok(_txtOf(id).trim().length > 80, id + ' tem prosa de verdade',
         String(_txtOf(id).trim().length));
      ['panel.csv', 'generate_report', 'HAC', 'Ljung', 'statsmodels', 'DataFrame',
       'expc_focus', 'pi_e', 'meta_12m', 'payload'].forEach((termo) => {
        ok(_txtOf(id).indexOf(termo) < 0, id + ' nao usa "' + termo + '"');
      });
    });
}

// ── §23b ──────────────────────────────────────────────────────────────────────
secao('23b. Nenhum id de gráfico se repete na página');
{
  // Um id repetido NAO levanta nada: `getElementById` devolve o primeiro, entao o
  // grafico da aba nova plota dentro do cartao da aba velha e o cartao dele fica
  // vazio. Foi o que aconteceu ao chamar o grafico desta aba de `ch-exp`, que ja era
  // o da expectativa na aba de dados -- e so o browser real pegou.
  const ids = [];
  ctx.CHARTS.forEach((c) => ids.push(c.div));
  ctx._cfgsSub().forEach((c) => ids.push(c.div));
  ctx._cfgsExp().forEach((c) => ids.push(c.div));
  const rep = ids.filter((x, i) => ids.indexOf(x) !== i);
  ok(rep.length === 0, 'os ' + ids.length + ' graficos da pagina tem ids distintos',
     rep.join(', '));

  // e o mesmo no literal de CHART_META: uma chave repetida num objeto literal e
  // silenciosamente vencida pela ultima, o que troca titulo e fonte de lugar
  const bloco = CRU.slice(CRU.indexOf('var CHART_META = {'));
  const corpo = bloco.slice(0, bloco.indexOf('\n};'));
  const chaves = (corpo.match(/'(ch-[^']+)'\s*:/g) || [])
    .map((m) => m.replace(/['\s:]/g, ''));
  const repM = chaves.filter((x, i) => chaves.indexOf(x) !== i);
  ok(repM.length === 0, 'e CHART_META nao tem chave repetida (' + chaves.length + ')',
     repM.join(', '));
  ids.forEach((d) => {
    ok(chaves.indexOf(d) >= 0, 'o grafico ' + d + ' tem entrada em CHART_META');
  });
}

// ── §24 ───────────────────────────────────────────────────────────────────────
secao('24. Os graficos da aba de expectativas');
ctx.activateTab('tab-exp');
{
  const niv = PLOT['ch-eqexp'], dec = PLOT['ch-eqexp-dec'];
  ok(!!niv && !!dec, 'os dois graficos foram plotados');

  // o de nivel: tres linhas, e cada uma e a serie que diz ser
  ok(niv.traces.length === 3, 'o grafico de nivel tem tres linhas',
     String(niv.traces.length));
  ok(niv.traces[0].y === E.obs, 'a primeira e a expectativa da pesquisa');
  ok(niv.traces[1].y === E.fit, 'a segunda e a conta');
  ok(niv.traces[2].y === E.meta, 'a terceira e a meta');
  ok(niv.traces[1].y !== E.obs, 'e a conta NAO e o realizado plotado de novo');
  ok(niv.traces[2].line.dash === 'dash', 'a meta entra tracejada');
  ok(niv.layout.yaxis.title.indexOf('12 meses') >= 0,
     'o eixo diz que a unidade e a taxa anual de 12 meses', niv.layout.yaxis.title);

  // o da decomposicao: barras empilhadas em `relative`, mais a linha do desvio
  ok(dec.layout.barmode === 'relative',
     'as parcelas empilham em relative, nao em stack: elas trocam de sinal',
     dec.layout.barmode);
  const barras = dec.traces.filter((t) => t.type === 'bar');
  const linhas = dec.traces.filter((t) => t.type === 'scatter');
  const nPar = Object.keys(E.contrib).filter((k) => !!E.contrib[k]).length;
  ok(nPar >= 2, 'o payload traz pelo menos duas parcelas', String(nPar));
  ok(barras.length === nPar, 'ha uma barra por parcela, e so uma',
     barras.length + ' vs ' + nPar);
  ok(linhas.length === 1, 'e uma linha so, a do desvio observado');
  {
    let pior = 0;
    for (let i = 0; i < E.x.length; i++) {
      pior = Math.max(pior, Math.abs(linhas[0].y[i] - (E.obs[i] - E.meta[i])));
    }
    ok(pior < 1e-9, 'e essa linha e mesmo a distancia observada ate a meta');
  }
  {
    // as barras plotadas sao as parcelas do payload, e nenhuma esta plotada duas vezes
    const vistas = {};
    barras.forEach((b) => {
      const k = Object.keys(E.contrib).filter((c) => E.contrib[c] === b.y)[0];
      ok(!!k, 'a barra "' + b.name + '" e uma parcela do payload');
      ok(!vistas[k], 'e nenhuma parcela e plotada duas vezes: ' + k);
      vistas[k] = 1;
    });
    // e o contrario tambem: nenhuma parcela do payload pode ficar de FORA, senao as
    // barras deixam de somar a distancia que a linha desenha e ninguem percebe
    Object.keys(E.contrib).filter((k) => !!E.contrib[k]).forEach((k) => {
      ok(!!vistas[k], 'a parcela "' + k + '" do payload esta plotada');
    });
  }
  ok(dec.layout.yaxis.title.indexOf('p.p.') >= 0,
     'o eixo da decomposicao esta em p.p., nao em %', dec.layout.yaxis.title);

  // cabecalho de tres linhas nos dois
  ['ch-eqexp', 'ch-eqexp-dec'].forEach((id) => {
    const fr = document.getElementById(id).parentNode._chFrame;
    ok(!!fr && fr.title.textContent.length > 8, id + ': tem titulo');
    ok(fr.sub.textContent.length > 8, id + ': tem subtitulo derivado');
    ok(fr.src.textContent.indexOf('Fonte:') === 0, id + ': e linha de fonte');
  });
  // a regua de tempo fica ABAIXO do grafico
  ['ch-eqexp', 'ch-eqexp-dec'].forEach((id) => {
    const card = document.getElementById(id).parentNode;
    const kids = Array.prototype.slice.call(card.children);
    const iPlot = kids.indexOf(document.getElementById(id));
    let iBar = -1;
    kids.forEach((c, j) => { if (c._cls().includes('range-pills')) iBar = j; });
    ok(iBar > iPlot, id + ': a regua de tempo vem depois do grafico');
  });
}

// ── §25 ───────────────────────────────────────────────────────────────────────
secao('25. A aba de Hiato: a curva IS (H)');
const H = D['is'];
ok(!!H, 'o payload traz a curva IS');
ok(CRU.indexOf('data-tab="tab-is"') >= 0, 'a aba existe no markup');

if (H) {
  const _f = (v, d) => v.toFixed(d).replace('.', ',');
  const cLag = H.coef.filter((c) => c.key === 'h1')[0];
  const cApt = H.coef.filter((c) => c.key === 'h2')[0];

  // ── a forma e a do plano, com a inclinacao no lugar do juro contra um neutro.
  //    Esta parte trava a especificacao: dois parametros e duas dummies, nada mais.
  ok(H.coef.length === 4, 'a conta tem dois pesos e duas marcas de crise',
     String(H.coef.length));
  ok(H.coef.map((c) => c.key).join(',') === 'h1,h2,d08,d20',
     'e eles sao o hiato anterior, o aperto, 2008 e 2020, nessa ordem',
     H.coef.map((c) => c.key).join(','));
  ok(H.coef.filter((c) => c.crise).map((c) => c.key).join(',') === 'd08,d20',
     'so as duas crises sao marcadas como crise');
  ok(H.lag_grr === 1, 'o aperto entra defasado UM trimestre', String(H.lag_grr));

  // ── sem intercepto: o payload nao pode carregar um, e o repouso tem de dar zero
  ok(H.coef.every((c) => c.key !== 'const' && c.key !== 'intercepto'),
     'nao ha termo constante na conta');
  ok(H.repouso.volta_a_zero === true,
     'em repouso, com a politica neutra, o hiato volta a ZERO');

  // ── o sinal, que e a validacao do plano contra o BC: h2 < 0
  ok(cApt.b < 0, 'o aperto SEGURA a economia: o peso e negativo', String(cApt.b));
  ok(cLag.b > 0 && cLag.b < 1,
     'e o hiato e persistente mas estavel: o peso da defasagem fica entre 0 e 1',
     String(cLag.b));
  ok(H.estavel === true, 'a equacao e declarada estavel');

  // ── o efeito de longo prazo e do APERTO, nao da defasagem
  ok(cApt.lp != null, 'o aperto tem efeito de longo prazo proprio');
  ok(cLag.lp == null,
     'e a defasagem do hiato nao: ela PRODUZ o acumulo, nao o sofre');
  ok(H.coef.filter((c) => c.crise).every((c) => c.lp == null),
     'as marcas de crise tambem nao tem efeito de longo prazo');
  ok(Math.abs(H.efeito_lp - cApt.b / (1 - cLag.b)) < 1e-5,
     'o efeito de longo prazo e o peso do aperto sobre um menos a defasagem',
     H.efeito_lp + ' vs ' + (cApt.b / (1 - cLag.b)));
  ok(Math.abs(H.repouso.simulado - H.repouso.formula) < 1e-5,
     'e o simulado bate com a formula',
     H.repouso.simulado + ' vs ' + H.repouso.formula);

  // ── a meia-vida: simular o AR tem de reproduzir o numero publicado
  {
    const h = [1];
    let achou = null;
    for (let t = 0; t < 400 && achou === null; t++) {
      const v = cLag.b * h[h.length - 1];
      h.push(v);
      if (Math.abs(v) <= 0.5) achou = t + 1;
    }
    ok(achou === H.meia_vida, 'a meia-vida publicada e a que o AR produz',
       achou + ' vs ' + H.meia_vida);
  }

  // ── a decomposicao e IDENTIDADE: parcelas + residuo == hiato observado
  {
    let pior = 0;
    for (let i = 0; i < H.x.length; i++) {
      let soma = 0;
      Object.keys(H.contrib).forEach((k) => {
        if (H.contrib[k]) soma += H.contrib[k][i];
      });
      pior = Math.max(pior, Math.abs(soma + H.resid[i] - H.obs[i]));
    }
    // 1e-3 e o arredondamento do payload, nao folga escolhida
    ok(pior < 1e-3, 'a decomposicao fecha: as parcelas mais o erro dao o hiato '
       + 'observado (pior ' + pior.toExponential(1) + ')');
    ok(pior > 0, 'e a identidade nao e trivial: as parcelas sao numeros distintos');
  }
  // a parcela de crise e ZERO fora das duas janelas, e nao-zero dentro
  {
    const cr = H.contrib.crise;
    let dentro = 0, fora = 0;
    H.rot.forEach((r, i) => {
      const y = +r.slice(0, 4), q = +r.slice(5);
      const e08 = (y === 2008 && q === 4) || (y === 2009);
      const e20 = (y === 2020);
      if (e08 || e20) { if (cr[i] !== 0) dentro++; } else if (cr[i] !== 0) fora++;
    });
    ok(fora === 0, 'a parcela de crise e exatamente zero fora de 2008-2009 e 2020',
       String(fora));
    ok(dentro > 0, 'e nao-zero dentro delas', String(dentro));
  }

  // ── a tabela de RR*: e o registro do POR QUE a inclinacao foi escolhida
  ok(Array.isArray(H.rr) && H.rr.length >= 4,
     'a tabela de taxas de equilibrio tem as candidatas medidas',
     String((H.rr || []).length));
  ok(H.rr.filter((r) => r.escolhida).length === 1,
     'exatamente uma linha e marcada como a escolhida');
  ok(H.rr.filter((r) => r.escolhida)[0].key === 'incl',
     'e ela e a inclinacao da curva real');
  {
    const n0 = H.rr[0].n;
    ok(H.rr.every((r) => r.n === n0),
       'todas medidas na MESMA janela, senao a tabela nao compara nada',
       H.rr.map((r) => r.n).join(','));
    const fixas = H.rr.filter((r) => r.key === 'const' || r.key === 'bc');
    const nossa = H.rr.filter((r) => r.key === 'incl')[0];
    ok(fixas.length === 2, 'as duas taxas fixas estao na tabela');
    ok(fixas.every((r) => Math.abs(r.t) < 2),
       'e nelas o aperto e indistinguivel de zero -- que e o motivo da escolha',
       fixas.map((r) => _f(r.t, 2)).join(' / '));
    ok(Math.abs(nossa.t) >= 2, 'enquanto a inclinacao mede alguma coisa',
       _f(nossa.t, 2));
    ok(Math.abs(nossa.h2 - cApt.b) < 1e-5,
       'e a linha escolhida traz o MESMO peso que a conta da pagina',
       nossa.h2 + ' vs ' + cApt.b);
  }

  // ── a tabela de formas testadas
  ok(H.comparar.filter((r) => r.escolhida).length === 1,
     'uma unica forma marcada como a da pagina');
  ok(H.comparar.filter((r) => r.escolhida)[0].key === 'base',
     'e ela e a defasada de um trimestre');
  {
    const base = H.comparar.filter((r) => r.key === 'base')[0];
    const cont = H.comparar.filter((r) => r.key === 'cont')[0];
    const sem = H.comparar.filter((r) => r.key === 'sem_cri')[0];
    ok(!!cont && !!sem, 'a contemporanea e a sem-crises estao medidas');
    ok(Math.abs(base.h2) > Math.abs(cont.h2),
       'a defasada mede MAIS aperto que a contemporanea -- o motivo da defasagem',
       base.h2 + ' vs ' + cont.h2);
    ok(Math.abs(sem.t) < Math.abs(base.t),
       'e sem as crises marcadas o aperto fica menos firme',
       sem.t + ' vs ' + base.t);
    const ns = H.comparar.map((r) => r.n === undefined ? null : r.n);
    ok(ns.every((v) => v === null), 'a tabela de formas nao expoe n por linha');
  }

  // ── as quatro frases sobre o residuo tem de concordar com o que o teste MEDE,
  //    nos dois sentidos -- mesma regra da aba de expectativas
  {
    const sobra = H.lb_p4 < 0.05;
    const acf = document.getElementById('tblIsAcf').innerHTML;
    const nota = document.getElementById('isAcfNota').textContent;
    const ficha = document.getElementById('isFicha').innerHTML;
    const stats = document.getElementById('isStats').innerHTML;
    ok(acf.indexOf(sobra ? 'ainda sobra padrão' : 'nada sobrando') >= 0,
       'a tabela de erro diz o que o teste mede');
    ok((nota.indexOf('acusam padrão sobrando') >= 0) === sobra,
       'a nota ao lado dela diz a mesma coisa');
    ok((ficha.indexOf('ainda tem padrão') >= 0) === sobra,
       'a ficha de abertura diz a mesma coisa');
    ok((stats.indexOf('ainda sobra padrão no erro') >= 0) === sobra,
       'e o cartao de erro tipico tambem');
    ok(sobra, 'nesta forma o erro AINDA TEM padrao -- se isso mudar, a prosa acima '
       + 'tem de mudar junto (Ljung-Box p ' + _f(H.lb_p4, 4) + ')');
  }

  // ── a media do hiato: o plano mandava CONFERIR e REPORTAR, e a pagina reporta
  {
    // innerHTML, e nao textContent: renderIsMath escreve innerHTML (ha <b> na frase)
    const mt = document.getElementById('isMathNota').innerHTML;
    ok(mt.indexOf(_f(H.hiato_medio, 2)) >= 0,
       'a prosa imprime a media medida do hiato, que justifica nao ter intercepto',
       _f(H.hiato_medio, 2));
    ok(Math.abs(H.hiato_medio) < 0.5 * H.hiato_sd,
       'e ela e pequena contra o desvio, que e a condicao para isso ser honesto',
       _f(H.hiato_medio, 3) + ' contra ' + _f(H.hiato_sd, 3));
  }

  // ── a tabela de pesos imprime o que o payload traz
  {
    const tb = document.getElementById('tblIsCoef').innerHTML;
    H.coef.forEach((c) => {
      ok(tb.indexOf(_f(c.b, 4)) >= 0, 'a tabela imprime o peso de ' + c.key);
      ok(tb.indexOf(c.rot) >= 0, 'e o nome legivel de ' + c.key);
    });
    ok(tb.indexOf('h1') < 0 && tb.indexOf('h2') < 0,
       'e nenhum nome de variavel do codigo vaza para a tela');
    // -1 pelo split e -1 pelo <tr> do cabecalho
    const linhas = tb.split('<tr').length - 2;
    ok(linhas === H.coef.length,
       'uma linha por coeficiente, sem conta de sobra: (H) nao tem restricao de soma',
       String(linhas));
  }

  // ── um peso NEGATIVO entra subtraindo na equacao numerica. h2 ja e negativo,
  //    entao o guarda e exercitado invertendo h1, que e positivo.
  {
    const orig = cLag.b;
    cLag.b = -orig;
    ctx.renderIsMath();
    // o <span class="tm"> fica ENTRE o sinal e o numero, entao procurar "−0,8864"
    // no markup nunca casa -- a asserção tem de olhar o texto sem as tags
    const txt = document.getElementById('isMathNum').innerHTML
      .replace(/<[^>]*>/g, '').replace(/\s+/g, ' ');
    ok(txt.indexOf('− ' + _f(orig, 4)) >= 0,
       'um peso negativo sai como subtracao, nunca como "+ −"', txt.slice(0, 120));
    ok(txt.indexOf('+ −') < 0, 'e nunca como "+ −" literal');
    cLag.b = orig;
    ctx.renderIsMath();
    const volta = document.getElementById('isMathNum').innerHTML
      .replace(/<[^>]*>/g, '').replace(/\s+/g, ' ');
    ok(volta.indexOf('− ' + _f(orig, 4)) < 0 && volta.indexOf(_f(orig, 4)) >= 0,
       'e o valor volta a entrar somando depois');
  }

  // ── a comparacao com o BC: a linha do aperto TEM de estar marcada como outro objeto
  {
    ok(H.bc.b1.comparavel === true, 'o peso do hiato anterior e comparavel com o do BC');
    ok(H.bc.b2.comparavel === false,
       'e o do aperto NAO e: la o regressor e outro');
    const nb = document.getElementById('isBcNota').textContent;
    ok(nb.indexOf('não') >= 0 && nb.indexOf('unidade do outro') >= 0,
       'e a nota explica por que a comparacao nao vale naquela linha');
    ok(nb.indexOf(_f(H.bc.b2.efeito, 3)) >= 0,
       'imprimindo o efeito que o coeficiente do BC produz, que e o comparavel',
       _f(H.bc.b2.efeito, 3));
  }

  // ── a notacao sai do payload, e cada simbolo tem definicao
  {
    ctx.renderIsMath();
    const leg = document.getElementById('isMathLeg').innerHTML;
    const simb = document.getElementById('isMathSimb').innerHTML;
    ok(simb.indexOf('<i>h</i><sub>t</sub>') >= 0, 'a equacao nomeia o hiato');
    ok(simb.indexOf('<i>g</i><sub>t−1</sub>') >= 0,
       'e o aperto aparece DEFASADO na notacao, como e estimado');
    ok(leg.split('<tr').length - 1 >= H.coef.length + 2,
       'a legenda define todos os simbolos usados, mais o explicado e o erro');
  }
}

// ── §26 ───────────────────────────────────────────────────────────────────────
secao('26. Os graficos da aba de Hiato');
if (H) {
  ctx.activateTab('tab-is');
  ['ch-eqis', 'ch-eqis-dec'].forEach((id) => {
    ok(!!PLOT[id], id + ': plotado ao abrir a aba');
  });
  // a decomposicao empilha em `relative`, porque as parcelas trocam de sinal
  const dec = PLOT['ch-eqis-dec'];
  ok(dec.layout.barmode === 'relative',
     'a decomposicao empilha em relative, nao em stack', dec.layout.barmode);
  const barras = dec.traces.filter((t) => t.type === 'bar');
  const nPar = Object.keys(H.contrib).filter((k) => !!H.contrib[k]).length;
  ok(barras.length === nPar,
     'uma barra por parcela do payload (' + nPar + ')', String(barras.length));
  ok(dec.traces.filter((t) => t.type === 'scatter').length === 1,
     'mais a linha do hiato observado por cima');

  // eixo, cabecalho e regua
  ['ch-eqis', 'ch-eqis-dec'].forEach((id) => {
    const y = PLOT[id].layout.yaxis;
    ok((y.title || '').indexOf('potencial') >= 0,
       id + ': o eixo nomeia a unidade do hiato', y.title);
    const fr = document.getElementById(id).parentNode._chFrame;
    ok(!!fr && fr.title.textContent.length > 8, id + ': tem titulo');
    ok(fr.sub.textContent.length > 8, id + ': tem subtitulo derivado');
    ok(fr.src.textContent.indexOf('Fonte:') === 0, id + ': e linha de fonte');
    const card = document.getElementById(id).parentNode;
    const kids = Array.prototype.slice.call(card.children);
    const iPlot = kids.indexOf(document.getElementById(id));
    let iBar = -1;
    kids.forEach((c, j) => { if (c._cls().includes('range-pills')) iBar = j; });
    ok(iBar > iPlot, id + ': a regua de tempo vem depois do grafico');
  });
  // os titulos dos dois sao DIFERENTES: sao perguntas diferentes
  ok(document.getElementById('ch-eqis').parentNode._chFrame.title.textContent
     !== document.getElementById('ch-eqis-dec').parentNode._chFrame.title.textContent,
     'e os dois graficos nao dividem o mesmo titulo');
}


// ── §27 ───────────────────────────────────────────────────────────────────────
secao('27. A aba de Juros: a regra de juros (R)');
const R = D.tay;
ok(!!R, 'o payload traz a regra de juros');
ok(CRU.indexOf('data-tab="tab-tay"') >= 0, 'a aba existe no markup');

if (R) {
  // ── a forma: duas defasagens, a inflacao e as duas crises, nada mais
  ok(R.coef.map((c) => c.key).join(',') === 'r1,r1b,r2,d08,d20',
     'a conta tem os dois juros passados, a inflacao e as duas crises, nessa ordem',
     R.coef.map((c) => c.key).join(','));
  ok(R.lags === 2, 'duas defasagens, que foi a decisao tomada', String(R.lags));
  ok(R.coef.filter((c) => c.crise).map((c) => c.key).join(',') === 'd08,d20',
     'so as duas crises sao marcadas como crise');
  ok(R.dummies_fora.length === 0,
     'as duas crises tem suporte na amostra -- nenhuma caiu fora',
     R.dummies_fora.join(','));
  ok(R.coef.every((c) => c.key !== 'const' && c.key !== 'intercepto'),
     'nao ha termo constante na conta');

  // ── a restricao: o peso da ancora e 1 menos a soma, e nao um parametro
  const soma = R.coef.filter((c) => c.key === 'r1' || c.key === 'r1b')
                     .reduce((a, c) => a + c.b, 0);
  ok(Math.abs(soma - R.soma) < 1e-6,
     'a soma publicada e a soma dos dois pesos do juro passado',
     soma + ' vs ' + R.soma);
  ok(R.soma < 1, 'e ela fica abaixo de 1 -- sem isso nao ha ancora', String(R.soma));
  ok(R.estavel === true, 'a equacao e declarada estavel');
  ok(R.repouso.volta_a_ancora === true,
     'em repouso, com a inflacao na meta, a Selic volta para a ancora');

  // ── a resposta de longo prazo e uma DIVISAO, e o simulado tem de bater
  const cInf = R.coef.filter((c) => c.key === 'r2')[0];
  ok(cInf.b > 0, 'a Selic sobe quando a inflacao esperada passa da meta',
     String(cInf.b));
  ok(Math.abs(R.efeito_lp - cInf.b / (1 - R.soma)) < 1e-5,
     'a resposta de longo prazo e o peso da inflacao sobre um menos a soma',
     R.efeito_lp + ' vs ' + (cInf.b / (1 - R.soma)));
  ok(Math.abs(R.repouso.simulado - R.repouso.formula) < 1e-5,
     'e o simulado bate com a formula',
     R.repouso.simulado + ' vs ' + R.repouso.formula);
  ok(R.efeito_lp > cInf.b,
     'e ela e MAIOR que a resposta do proprio trimestre -- o comite move devagar');

  // ── as duas identidades que a tela desenha
  let piorNivel = 0;
  R.x.forEach((_, i) => {
    if (R.selic_fit[i] == null || R.ancora[i] == null || R.fit[i] == null) return;
    piorNivel = Math.max(piorNivel, Math.abs(R.selic_fit[i] - (R.ancora[i] + R.fit[i])));
  });
  ok(piorNivel < 5e-4,
     'a Selic da conta e a ancora mais o desvio ajustado', String(piorNivel));
  let piorDec = 0;
  R.x.forEach((_, i) => {
    if (R.obs[i] == null) return;
    const t = (R.contrib.inercia[i] || 0) + (R.contrib.inflacao[i] || 0)
            + (R.contrib.crise[i] || 0) + (R.resid[i] || 0);
    piorDec = Math.max(piorDec, Math.abs(t - R.obs[i]));
  });
  ok(piorDec < 5e-4,
     'as parcelas da decomposicao mais o erro somam a distancia observada',
     String(piorDec));
  // e o observado E a Selic menos a ancora, que e o que a aba diz que ele e
  let piorDesv = 0;
  R.x.forEach((_, i) => {
    if (R.obs[i] == null || R.selic[i] == null || R.ancora[i] == null) return;
    piorDesv = Math.max(piorDesv, Math.abs(R.obs[i] - (R.selic[i] - R.ancora[i])));
  });
  ok(piorDesv < 5e-4, 'e a distancia observada e a Selic menos a ancora',
     String(piorDesv));

  // ── o veredito contra o BC sai do INTERVALO, nao esta escrito
  ['t1', 't2', 't3'].forEach((k) => {
    const b = R.bc[k];
    const v = b.nosso === 'lp' ? R.efeito_lp
                               : R.coef.filter((c) => c.key === b.nosso)[0].b;
    ok(R.dentro[k] === (v >= b.ic[0] && v <= b.ic[1]),
       'o veredito de "' + k + '" sai do intervalo publicado, nao de uma constante',
       v + ' em [' + b.ic[0] + ';' + b.ic[1] + '] -> ' + R.dentro[k]);
  });

  // ── a tabela de janelas: exatamente uma em uso, e e a que o modulo declara
  ok(R.janela.filter((j) => j.escolhida).length === 1,
     'exatamente uma janela marcada como em uso');
  ok(R.janela.filter((j) => j.escolhida)[0].k === R.mm_rr,
     'e ela e a que o modulo declara');
  ok(R.janela.every((j) => j.n === R.janela[0].n),
     'as janelas sao comparadas na MESMA amostra -- senao a comparacao e de recorte');
  ok(R.comparar.filter((c) => c.escolhida).length === 1,
     'exatamente uma forma marcada como a da pagina');

  // ── a prosa derivada diz o que o payload traz
  const ficha = _prosa('tayFicha');
  ok(ficha.indexOf(String(R.n)) >= 0 && ficha.indexOf(R.ini) >= 0
     && ficha.indexOf(R.fim) >= 0,
     'a ficha nomeia a amostra que o payload traz');
  // a nota do residuo NAO pode citar como quem reprova uma conta que passa
  const acfNota = _prosa('tayAcfNota');
  if (D.exp && D.exp.lb_p4 >= 0.05) {
    ok(acfNota.indexOf('expectativas') < 0,
       'a nota do erro nao cita a conta de expectativas quando ela tambem passa');
  }
  if (D['is'] && D['is'].lb_p4 >= 0.05) {
    ok(acfNota.indexOf('hiato') < 0,
       'a nota do erro nao cita a conta do hiato quando ela tambem passa');
  }
  ok(acfNota.indexOf('unica delas') < 0 && acfNota.indexOf('única delas') < 0,
     'e nao afirma ser a unica conta com residuo limpo');
  // o veredito escrito bate com o calculado
  const bcNota = _prosa('tayBcNota');
  const dentroN = ['t1', 't2', 't3'].filter((k) => R.dentro[k]).length;
  ok(bcNota.indexOf(String(dentroN) + ' dos 3') >= 0,
     'a nota conta quantos pesos caem dentro, e a conta bate', bcNota.slice(0, 40));
}

// ── §28 ───────────────────────────────────────────────────────────────────────
secao('28. A aba de Cambio: a equacao (F)');
const F = D.fx;
ok(!!F, 'o payload traz a equacao de cambio');
ok(CRU.indexOf('data-tab="tab-fx"') >= 0, 'a aba existe no markup');

if (F) {
  ok(F.ordem.join(',') === 'd_fiscal,d_dxy_em,d_carry_vol,d_sp500,d_icbr_usd,de_l1',
     'os cinco canais mais a persistencia, nessa ordem', F.ordem.join(','));
  ok(F.coef.length === F.ordem.length, 'uma linha de peso por regressor');

  // ── a identidade que a barra empilhada afirma
  let pior = 0;
  F.x.forEach((_, i) => {
    if (F.obs[i] == null) return;
    let t = (F.contrib.ppp[i] || 0) + (F.contrib.alpha[i] || 0) + (F.resid[i] || 0);
    F.ordem.forEach((k) => { t += (F.contrib[k][i] || 0); });
    pior = Math.max(pior, Math.abs(t - F.obs[i]));
  });
  ok(pior < 5e-3, 'as parcelas mais o erro somam a variacao observada', String(pior));

  // ── e o acumulado de cada termo E a soma da parcela dele
  F.coef.forEach((c) => {
    const soma = (F.contrib[c.key] || []).reduce((a, v) => a + (v || 0), 0);
    ok(Math.abs(soma - c.acum) < 5e-2,
       'o acumulado de "' + c.key + '" e a soma da parcela dele',
       soma + ' vs ' + c.acum);
  });
  const somaPpp = F.contrib.ppp.reduce((a, v) => a + (v || 0), 0);
  ok(Math.abs(somaPpp - F.acum_ppp) < 5e-2,
     'e o do diferencial de inflacao tambem', somaPpp + ' vs ' + F.acum_ppp);
  ok(F.acum_ppp > 0 && F.acum_ppp < F.de_total,
     'o diferencial de inflacao explica PARTE do movimento, nao tudo',
     F.acum_ppp + ' de ' + F.de_total);

  // ── o canal que troca de sinal e DERIVADO, nao escrito
  F.coef.forEach((c) => {
    ok(c.troca_sinal === (c.b * c.corr < 0),
       '"' + c.key + '": a marca de troca de sinal sai do dado',
       'b ' + c.b + ' corr ' + c.corr + ' -> ' + c.troca_sinal);
  });
  ok(F.flip.join(',') === F.coef.filter((c) => c.troca_sinal).map((c) => c.key).join(','),
     'a lista de canais que trocam de sinal e a dos que estao marcados');

  if (F.flip.length) {
    ok(F.anatomia.length >= 3, 'a anatomia tem pelo menos tres degraus');
    ok(F.anatomia[0].n === 0, 'o primeiro degrau e a serie sozinha');
    ok(F.anatomia[F.anatomia.length - 1].todos === true,
       'e o ultimo e a conta inteira');
    ok(F.anatomia[0].b * F.anatomia[F.anatomia.length - 1].b < 0,
       'e o sinal de fato vira entre os dois extremos',
       F.anatomia[0].b + ' -> ' + F.anatomia[F.anatomia.length - 1].b);
    // a leitura economica e a do canal que virou, e nao a de outro
    const nota = _prosa('fxFlipNota');
    if (F.flip[0] === 'd_sp500') {
      ok(nota.indexOf('bolsa') >= 0, 'a leitura escrita e a da bolsa americana');
    } else {
      ok(nota.indexOf('bolsa') < 0,
         'a leitura escrita nao fala de bolsa quando quem virou foi outro canal');
    }
    ok(_prosa('fxFlipTexto').indexOf('condicional') < 0
       || _prosa('fxFlipNota').indexOf('condicional') >= 0,
       'e a palavra condicional aparece onde explica a coluna de acumulado');
  }

  // ── o lambda no piso e o que torna os t legiveis; os dois campos andam juntos
  ok(F.piso === F.t_valem,
     'os t so sao declarados legiveis quando a penalidade esta no piso');
  ok(F.cv.length > 5, 'a curva de validacao tem grade', String(F.cv.length));
  ok(F.cv[0].mse < F.cv[F.cv.length - 1].mse,
     'e a penalidade mais forte erra mais que a mais fraca',
     F.cv[0].mse + ' vs ' + F.cv[F.cv.length - 1].mse);

  // ── o mensal ao lado: mesma unidade, e o corte de cada um e proprio
  ok(F.mensal.n > F.n * 2, 'o modelo mensal tem mais observacoes que o trimestral',
     F.mensal.n + ' vs ' + F.n);
  ok(F.r2 > F.mensal.r2,
     'e o trimestral explica mais do movimento, que e o esperado',
     F.r2 + ' vs ' + F.mensal.r2);
  ok(F.comparar.filter((c) => c.escolhida).length === 1,
     'exatamente uma forma marcada como a da pagina');
  const semPpp = F.comparar.filter((c) => c.key === 'sem_ppp')[0];
  ok(!!semPpp && Math.abs(semPpp.alpha) > Math.abs(F.alpha),
     'sem o diferencial de inflacao o termo constante fica MAIOR -- e o que ele tira',
     (semPpp ? semPpp.alpha : '?') + ' vs ' + F.alpha);

  const fichaF = _prosa('fxFicha');
  ok(fichaF.indexOf(String(F.n)) >= 0 && fichaF.indexOf(F.ini) >= 0,
     'a ficha da aba nomeia a amostra que o payload traz');
}

// ── §29 ───────────────────────────────────────────────────────────────────────
secao('29. Os graficos das abas de Juros e Cambio');
[['tab-tay', ['ch-eqtay', 'ch-eqtay-dec'], R, 'Selic'],
 ['tab-fx', ['ch-eqfx', 'ch-eqfx-dec'], F, 'câmbio']].forEach((caso) => {
  const [aba, ids, S, unidade] = caso;
  if (!S) return;
  ctx.activateTab(aba);
  ids.forEach((id) => ok(!!PLOT[id], id + ': plotado ao abrir a aba'));

  const dec = PLOT[ids[1]];
  ok(dec.layout.barmode === 'relative',
     ids[1] + ': empilha em relative, nao em stack -- as parcelas trocam de sinal',
     dec.layout.barmode);
  ok(dec.traces.filter((t) => t.type === 'scatter').length === 1,
     ids[1] + ': tem a linha do observado por cima das barras');
  ok(dec.traces.filter((t) => t.type === 'bar').length >= 3,
     ids[1] + ': tem uma barra por parcela',
     String(dec.traces.filter((t) => t.type === 'bar').length));

  ids.forEach((id) => {
    const y = PLOT[id].layout.yaxis;
    ok((y.title || '').length > 6, id + ': o eixo nomeia a unidade', y.title);
    const fr = document.getElementById(id).parentNode._chFrame;
    ok(!!fr && fr.title.textContent.length > 8, id + ': tem titulo');
    ok(fr.sub.textContent.length > 8, id + ': tem subtitulo derivado');
    ok(fr.src.textContent.indexOf('Fonte:') === 0, id + ': e linha de fonte');
    const card = document.getElementById(id).parentNode;
    const kids = Array.prototype.slice.call(card.children);
    const iPlot = kids.indexOf(document.getElementById(id));
    let iBar = -1;
    kids.forEach((c, j) => { if (c._cls().includes('range-pills')) iBar = j; });
    ok(iBar > iPlot, id + ': a regua de tempo vem depois do grafico');
  });
  ok(document.getElementById(ids[0]).parentNode._chFrame.title.textContent
     !== document.getElementById(ids[1]).parentNode._chFrame.title.textContent,
     aba + ': os dois graficos nao dividem o mesmo titulo');
  // o subtitulo tem de falar da unidade do eixo, e nao de outra coisa
  const sub = document.getElementById(ids[0]).parentNode._chFrame.sub.textContent;
  ok(sub.indexOf(PLOT[ids[0]].layout.yaxis.title) >= 0,
     ids[0] + ': o subtitulo repete a MESMA unidade do eixo', sub);
});

// ── 8. Simulador ──────────────────────────────────────────────────────────────
// A aba tem dois blocos, e este harness cobre a METADE de baixo do contrato: a
// taxonomia das variaveis, a resolucao de caminho de cada uma, a recursao e o texto
// que os cartoes imprimem. O CLIQUE nao e coberto aqui de proposito: o stub de DOM
// deste arquivo nao constroi arvore a partir de `innerHTML`, entao um teste de clique
// passaria sem exercitar nada -- afirmar sobre a string que o render produz e o que da
// para fazer com honestidade. Quem clica e `tests/test_structural_model_browser.js`,
// em Chrome de verdade.
secao('8. Simulador: taxonomia, caminhos e recursao');
if (!D.sim) {
  ok(false, 'o payload traz o simulador');
} else {
  const EQ = D.sim.eq[D.sim.eq_ordem[0]];
  const SIM = ctx.SIM;

  // ── 8a. o payload ──
  ok(D.sim.eq_ordem.length >= 1, 'ha pelo menos uma equacao', D.sim.eq_ordem.join(','));
  ok(D.sim.var_ordem.length >= 1, 'ha inputs declarados', D.sim.var_ordem.join(','));
  ok(D.sim.h_max === 12, 'o horizonte tem teto de 12 trimestres', String(D.sim.h_max));
  ok(EQ.draws && EQ.draws.t1.length === EQ.n_draws,
     'os desenhos do posterior vieram completos', String(EQ.n_draws));
  ok(EQ.n_draws_total > EQ.n_draws, 'os desenhos sao um afinamento do posterior',
     EQ.n_draws + ' de ' + EQ.n_draws_total);

  // ── 8b. endogena/exogena e propriedade do MODELO, e o payload separa os dois fatos ──
  const VSel = D.sim.var.selic, VDi = D.sim.var.di, VAnc = D.sim.var.ancora;
  ok(VSel.tipo === 'endogena' && VSel.produzida_por === 'R' && VSel.produtor_no_sim,
     'a Selic e endogena: a equacao que a produz esta no simulador');
  ok(VDi.tipo === 'exogena' && VDi.produzida_por === 'E' && !VDi.produtor_no_sim,
     'o desvio da inflacao e exogena HOJE e traz qual equacao o produzira',
     VDi.produzida_por + ' / produtor_no_sim=' + VDi.produtor_no_sim);
  ok(VAnc.tipo === 'exogena' && VAnc.produzida_por === null,
     'a ancora e exogena e NENHUMA equacao do modelo a produz');
  ok(/12 meses/.test(VDi.nota) && /18/.test(VDi.nota),
     'a nota do desvio declara o desencaixe de horizonte com a equacao (E)',
     VDi.nota.slice(0, 80));
  // Uma variavel endogena tem de poder ser estressada; uma exogena nao pode oferecer
  // "a equacao", porque nao ha equacao que a produza.
  ok(VSel.fontes.indexOf('equacao') >= 0 && VSel.fontes.indexOf('digitado') >= 0,
     'a endogena oferece a equacao E o caminho digitado', VSel.fontes.join(','));
  D.sim.var_ordem.filter((k) => D.sim.var[k].tipo === 'exogena').forEach((k) => {
    ok(D.sim.var[k].fontes.indexOf('equacao') < 0,
       k + ': exogena nao oferece "a equacao" como fonte',
       D.sim.var[k].fontes.join(','));
    ok(D.sim.var[k].fontes.indexOf('digitado') >= 0,
       k + ': exogena pode ser estressada');
  });
  // Toda parte declarada tem de existir no dicionario de primitivas -- uma chave
  // errada nao levanta nada, so faz o cartao abrir vazio.
  D.sim.var_ordem.forEach((k) => {
    (D.sim.var[k].partes || []).forEach((p) => {
      ok(!!D.sim.prim[p], k + ': a parte ' + p + ' existe no payload');
    });
  });

  // ── 8c. a aba pinta quando aberta, e abre PROJETANDO ──
  ok(!PLOT['ch-sim'], 'antes de abrir a aba o grafico nao existe');
  ctx.activateTab('tab-sim');
  ok(!!PLOT['ch-sim'], 'ao abrir a aba o grafico e pintado');

  // A janela nao se escolhe: ela comeca no trimestre SEGUINTE ao fim da janela
  // estimada, e so ali -- pedido do usuario em 2026-09-22, *"sempre projeta para
  // frente da janela estimada"*. Antes a aba abria em 2006T3, refazendo 2008.
  ok(D.sim.i0 === EQ.est_i1 + 1,
     'o payload declara a partida como o trimestre seguinte ao fim da estimacao',
     'i0 = ' + D.sim.i0 + ', estimou ate ' + EQ.est_fim + ' (indice ' + EQ.est_i1 + ')');
  ok(SIM.i0 === D.sim.i0, 'e a tela abre exatamente nela', String(SIM.i0));
  ok(!document.getElementById('simJanela').innerHTML.match(/<select/),
     'nao ha seletor de partida: a janela e uma so');
  ok(SIM.h === 12, 'e projeta 12 trimestres', String(SIM.h));
  ok(ctx._simRotIdx(D.sim.x.length) !== D.sim.rot[D.sim.rot.length - 1],
     'o primeiro trimestre projetado e o seguinte ao ultimo observado',
     D.sim.rot[D.sim.rot.length - 1] + ' -> ' + ctx._simRotIdx(D.sim.x.length));
  // O rotulo derivado tem de virar o ano, e nao imprimir T5.
  ok(/^\d{4}T[1-4]$/.test(ctx._simRotIdx(D.sim.x.length + 11)),
     'o rotulo do ultimo trimestre projetado vira o ano corretamente',
     ctx._simRotIdx(D.sim.x.length + 11));
  // E a regua de tempo tem de alcancar o que foi desenhado: com "Tudo" tirado so da
  // serie observada, os 12 trimestres projetados ficam fora da tela -- desenhados e
  // invisiveis, que e o pior dos dois mundos.
  const gProj = SIM._ultimo.g;
  ok(PLOT['ch-sim'].layout.xaxis.range[1] >= gProj.x[gProj.x.length - 1],
     'a janela do eixo alcanca o ultimo trimestre projetado',
     PLOT['ch-sim'].layout.xaxis.range[1] + ' contra ' + gProj.x[gProj.x.length - 1]);
  // Na janela padrao NENHUMA caixa e de trimestre publicado: todas seguram o ultimo
  // valor conhecido, e e isso que a cor dourada diz.
  const htmlProj = document.getElementById('simInputs').innerHTML;
  ok(!/sim-caixa-in obs/.test(htmlProj) && /sim-caixa-in seg/.test(htmlProj),
     'projetando, toda caixa sai em dourado -- nao ha trimestre publicado ali');

  const g0 = { i0: SIM.i0, h: SIM.h, coef: JSON.parse(JSON.stringify(SIM.coef)),
               fonte: JSON.parse(JSON.stringify(SIM.fonte)), faixa: SIM.faixa };
  function restaura() {
    SIM.i0 = g0.i0; SIM.h = g0.h;
    SIM.coef = JSON.parse(JSON.stringify(g0.coef));
    SIM.fonte = JSON.parse(JSON.stringify(g0.fonte));
    SIM.faixa = g0.faixa; SIM.choque = false;
    ctx.simRecarregarCaixas();
    ctx.renderSim();
  }

  // ── 8d. a restricao, conferida no caminho SIMULADO ──
  // Com a inflacao esperada na meta a conta tem de voltar para a ancora e parar ali.
  // Mesma propriedade que `taylor.repouso()` afirma do lado do Python, agora medida no
  // codigo que o navegador roda.
  SIM.i0 = D.sim.rot.length - 1;
  SIM.h = 8;
  SIM.faixa = false;
  SIM.fonte.di = 'digitado';
  SIM.fonte.ancora = 'digitado';
  SIM.cx.di = new Array(8).fill(0);
  SIM.cx.ancora = new Array(8).fill(9);
  ctx.renderSim();
  // 8 trimestres nao bastam para convergir de verdade (meia-vida 3,6), entao a
  // afirmacao e de DIRECAO: cada passo anda para a ancora e o ultimo esta perto.
  let cam = SIM._ultimo.cam;
  ok(Math.abs(cam[cam.length - 1] - 9) < Math.abs(cam[0] - 9),
     'com a inflacao esperada na meta o caminho anda na direcao da ancora',
     cam[0].toFixed(3) + ' -> ' + cam[cam.length - 1].toFixed(3));
  // Com horizonte longo a conta converge exatamente -- rodada aqui pela funcao, sem
  // passar pelo teto de 8 da tela, que e limite de INTERFACE e nao da conta.
  const entLonga = { di: new Array(200).fill(0), ancora: new Array(200).fill(9) };
  EQ.dummies.forEach((c) => { entLonga[c] = new Array(200).fill(0); });
  const longo = ctx._simCaminhoSelic(SIM.coef, SIM.i0, 200, entLonga, null);
  ok(Math.abs(longo[longo.length - 1] - 9) < 1e-6,
     'no longo prazo ela converge exatamente para a ancora',
     longo[longo.length - 1].toFixed(8));
  entLonga.di = new Array(200).fill(1);
  const lp = ctx._simCaminhoSelic(SIM.coef, SIM.i0, 200, entLonga, null);
  ok(Math.abs((lp[lp.length - 1] - 9) - SIM.coef.t3) < 1e-6,
     'um desvio permanente de 1 p.p. leva a Selic a subir t3 no longo prazo',
     (lp[lp.length - 1] - 9).toFixed(6) + ' contra t3 = ' + SIM.coef.t3.toFixed(6));

  // ── 8e. a faixa ──
  SIM.faixa = true;
  ctx.renderSim();
  const fx = SIM._ultimo.faixa;
  ok(!!fx, 'com a faixa ligada o resultado traz lo/hi');
  ok(fx.lo.length === SIM.h && fx.hi.length === SIM.h,
     'a faixa tem um par por trimestre simulado');
  ok(fx.lo.every((v, i) => v <= fx.hi[i]), 'a borda de baixo nunca passa a de cima');
  ok((fx.hi[SIM.h - 1] - fx.lo[SIM.h - 1]) > (fx.hi[0] - fx.lo[0]),
     'a faixa ALARGA com o horizonte -- e incerteza propagada pela dinamica',
     (fx.hi[0] - fx.lo[0]).toFixed(3) + ' -> '
       + (fx.hi[SIM.h - 1] - fx.lo[SIM.h - 1]).toFixed(3));
  const semChoque = fx.hi[SIM.h - 1] - fx.lo[SIM.h - 1];
  SIM.choque = true;
  ctx.renderSim();
  const comChoque = SIM._ultimo.faixa.hi[SIM.h - 1] - SIM._ultimo.faixa.lo[SIM.h - 1];
  ok(comChoque > semChoque, 'somar o erro da equacao alarga a faixa',
     semChoque.toFixed(3) + ' -> ' + comChoque.toFixed(3));
  ctx.renderSim();
  ok(Math.abs(comChoque
       - (SIM._ultimo.faixa.hi[SIM.h - 1] - SIM._ultimo.faixa.lo[SIM.h - 1])) < 1e-12,
     'a faixa de choque nao treme entre dois renders -- a semente e fixa');
  SIM.choque = false;

  // ── 8f. fonte por variavel ──
  restaura();
  const base = SIM._ultimo.cam[SIM._ultimo.cam.length - 1];
  SIM.fonte.di = 'digitado';
  SIM.cx.di = SIM.cx.di.map((v) => v + 1);
  ctx.renderSim();
  const comDi = SIM._ultimo.cam[SIM._ultimo.cam.length - 1];
  ok(comDi > base, 'estressar so a inflacao esperada sobe a Selic simulada',
     base.toFixed(3) + ' -> ' + comDi.toFixed(3));

  // O composto: mexer numa PARTE move o agregado, e so nele.
  restaura();
  const ancAntes = SIM.cx.ancora.slice(0, 3).join(',');
  SIM.fonte.ancora = 'digitado';
  SIM.px.rr_10a = SIM.px.rr_10a.map((v) => v + 2);
  ctx.simAgregarDePartes('ancora');
  ctx.renderSim();
  ok(Math.abs(SIM.cx.ancora[0] - (parseFloat(ancAntes.split(',')[0]) + 2)) < 1e-9,
     'somar 2 ao juro real de equilibrio soma 2 a ancora',
     ancAntes.split(',')[0] + ' -> ' + SIM.cx.ancora[0].toFixed(3));
  ok(Math.abs(SIM._ultimo.ent.di[0] - ctx.simObs('di', SIM.i0, 1)[0]) < 1e-9,
     'e nao mexe no desvio da inflacao, que tem a propria fonte');

  // A Selic imposta desliga a equacao.
  restaura();
  SIM.fonte.selic = 'observado';
  ctx.renderSim();
  ok(SIM._ultimo.faixa === null,
     'com a Selic imposta nao ha faixa: nao ha equacao rodando');
  ok(SIM._ultimo.cam.every((v, i) => Math.abs(v - ctx.simObs('selic', SIM.i0, SIM.h)[i])
       < 1e-9),
     'e o caminho desenhado e exatamente o observado');
  ok(document.getElementById('simAviso').style.display === ''
     && /desligada/.test(document.getElementById('simAviso').innerHTML),
     'a faixa de aviso diz que a regra de juros esta desligada');

  // ── 8g. a corrida solta contra o observado ──
  restaura();
  SIM.i0 = EQ.est_i0;
  SIM.h = D.sim.h_max;
  ctx.renderSim();
  const solta = SIM._ultimo;
  const obsSolta = ctx.simObs('selic', SIM.i0, SIM.h);
  let somaErro = 0;
  for (let i = 0; i < SIM.h; i++) somaErro += Math.abs(solta.cam[i] - obsSolta[i]);
  const erroMed = somaErro / SIM.h;
  ok(erroMed > D.tay.rmse,
     'o erro da corrida solta e maior que o RMSE do ajuste -- e a prova dificil',
     erroMed.toFixed(3) + ' contra ' + D.tay.rmse.toFixed(3));

  // ── 8h. o teto do horizonte ──
  SIM.h = 40;
  ctx.renderSim();
  ok(SIM.h === D.sim.h_max, 'o horizonte e limitado ao teto declarado no payload',
     String(SIM.h));

  // ── 8i. os PESOS nao sao controle: a simulacao vem dos inputs ──
  // Pedido direto do usuario em 2026-09-22. O guarda e sobre a barra RENDERIZADA e
  // nao sobre o markup: a versao anterior montava as tres caixas de peso por
  // `innerHTML`, entao um grep no arquivo entregue nao acharia nada.
  restaura();
  const barra = document.getElementById('simOpcoes').innerHTML;
  ok(!/type="number"/.test(barra),
     'a barra do bloco 1 nao tem caixa de numero -- nenhum peso se digita ali');
  ok(!/simT1|simT2|simT3|simReset/.test(barra),
     'e nao sobrou nenhum controle de peso da versao anterior');
  ok(/pesos fixos no estimado/.test(barra),
     'a barra diz que os pesos estao fixos no estimado');
  ok(/simFaixa/.test(barra) && /simChoque/.test(barra),
     'o que resta sao as duas opcoes de DESENHO: a faixa e o erro da equacao');
  ok(document.getElementById('simAviso').style.display === 'none',
     'com a equacao ligada nao ha aviso');

  // ── 8j. o cartao de input, no desenho do FX Report ──
  // A cobertura e afirmada na FUNCAO e na TELA. So na tela nao bastaria: as duas
  // classes sao string, e um mutante que troque a condicao continua imprimindo
  // alguma classe.
  restaura();
  SIM.i0 = D.sim.rot.length - 2;
  SIM.h = 8;
  ctx.renderSim();
  const cobSel = ctx._simCobertura('selic', SIM.i0, SIM.h);
  ok(cobSel[0] === true && cobSel[SIM.h - 1] === false,
     'a cobertura separa o trimestre publicado do que passou do ultimo dado',
     cobSel.map((b) => (b ? '1' : '0')).join(''));
  const html = document.getElementById('simInputs').innerHTML;
  ok(/sim-caixa-in obs/.test(html) && /✓/.test(html),
     'voltando para dentro da historia, o trimestre publicado sai verde e marcado');
  ok(/sim-caixa-in seg/.test(html) && /~<\/div>/.test(html),
     'o que passou do ultimo dado sai em dourado -- e o ultimo valor repetido');
  ok(/sim-modo-btn on/.test(html),
     'a fonte e um par de pills como no FX Report, com a ativa marcada');
  ok(!/type="radio"/.test(html), 'e nao sobrou radio nenhum');
  ok(/Aplicar choque/.test(html) && /class="sim-link"/.test(html),
     'as acoes sao links no padrao do FX Report');
  D.sim.var_ordem.forEach((k) => {
    ok(html.indexOf(D.sim.var[k].instrucao) >= 0,
       k + ': o cartao imprime a instrucao do que se digita ali');
  });
  // Enquanto a fonte nao for "digitado" a caixa nao se edita -- e o mesmo estado
  // `final` do FX Report, que existe para uma suposicao nao sobrescrever um dado.
  ok((html.match(/disabled/g) || []).length > 0,
     'com a fonte no observado as caixas estao travadas');
  // A trava e por TRIMESTRE e nao por cartao, que e a pratica do FX Report: em Exogeno
  // destravam as caixas SEM dado publicado, e as publicadas continuam travadas -- um
  // palpite nao sobrescreve dado que ja se conhece.
  SIM.fonte.ancora = 'digitado';
  ctx.renderSim();
  const hDig = document.getElementById('simInputs').innerHTML;
  const caixasAnc = hDig.match(/<input[^>]*data-chave="ancora"[^>]*>/g) || [];
  const cobAnc = ctx._simCobertura('ancora', SIM.i0, SIM.h);
  ok(caixasAnc.length === SIM.h, 'ha uma caixa por trimestre da janela',
     caixasAnc.length + ' para h = ' + SIM.h);
  ok(cobAnc.some(Boolean) && cobAnc.some((c) => !c),
     'este cenario tem trimestre publicado E trimestre sem dado -- senao nao separa nada',
     cobAnc.map((c) => (c ? '1' : '0')).join(''));
  ok(caixasAnc.every((cx, i) => /disabled/.test(cx) === cobAnc[i]),
     'em Exogeno, destrava exatamente o que NAO tem dado publicado',
     caixasAnc.map((cx) => (/disabled/.test(cx) ? 'x' : '.')).join(''));
  ok(caixasAnc.filter((cx) => /sim-caixa-in obs/.test(cx)).length
       === cobAnc.filter(Boolean).length,
     'e as publicadas seguem verdes mesmo com a fonte em Exogeno');
  restaura();

  // ── 8j2. a forma do choque, e o choque numa PARTE ──
  // Tres formas pedidas pelo usuario em 2026-09-22. A terceira contem a segunda, e as
  // duas existem separadas porque foram pedidas separadas.
  restaura();
  const perfilRampa = ctx._simPerfilChoque({ tipo: 'rampa', v: 2, n: 4 }, 6);
  ok(perfilRampa.every((x, i) => Math.abs(x - 2 * Math.min(1, (i + 1) / 4)) < 1e-12),
     'rampa: sobe em N trimestres e fica no valor cheio',
     perfilRampa.map((x) => x.toFixed(2)).join(' '));
  const perfilDecai = ctx._simPerfilChoque({ tipo: 'decai', v: 2, rho: 0.8 }, 5);
  ok(Math.abs(perfilDecai[0] - 2) < 1e-12
     && Math.abs(perfilDecai[1] - 1.6) < 1e-12
     && Math.abs(perfilDecai[4] - 2 * Math.pow(0.8, 4)) < 1e-12,
     'temporario: entra cheio e sobra rho a cada trimestre',
     perfilDecai.map((x) => x.toFixed(3)).join(' '));
  const perfilConst = ctx._simPerfilChoque({ tipo: 'const', v: 2, n: 3, rho: 0.8 }, 6);
  ok(perfilConst[0] === 2 && perfilConst[2] === 2
     && Math.abs(perfilConst[3] - 1.6) < 1e-12
     && Math.abs(perfilConst[5] - 2 * Math.pow(0.8, 3)) < 1e-12,
     'constante por N e depois decaindo: os dois trechos batem',
     perfilConst.map((x) => x.toFixed(3)).join(' '));
  // A terceira com N = 1 tem de coincidir com a segunda -- e o que prova que a forma
  // geral e uma so e que a do meio e um caso dela.
  const c1 = ctx._simPerfilChoque({ tipo: 'const', v: 2, n: 1, rho: 0.8 }, 5);
  ok(c1.every((x, i) => Math.abs(x - perfilDecai[i]) < 1e-12),
     'a forma geral com N = 1 e exatamente o choque temporario');
  // rho fora do payload cai em 0,8, que e o numero que o usuario citou.
  const cPad = ctx._simPerfilChoque({ tipo: 'decai', v: 1 }, 2);
  ok(Math.abs(cPad[1] - 0.8) < 1e-12, 'sem rho declarado o padrao e 0,8',
     cPad[1].toFixed(3));

  // O choque numa PARTE move o agregado pela formula e nao toca na irma.
  restaura();
  SIM.fonte.ancora = 'digitado';
  const rrAntes = SIM.px.rr_10a.slice(0, 3);
  const metaAntes = SIM.px.meta_12m.slice(0, 3);
  const ancAntes2 = SIM.cx.ancora.slice(0, 3);
  SIM.chq.rr_10a = { tipo: 'const', v: 1.5, n: 12, rho: 0.8 };
  ctx.simAplicarChoque('rr_10a', 'ancora');
  ok(Math.abs(SIM.px.rr_10a[0] - (rrAntes[0] + 1.5)) < 1e-9,
     'o choque entra na primitiva escolhida',
     rrAntes[0].toFixed(3) + ' -> ' + SIM.px.rr_10a[0].toFixed(3));
  ok(SIM.px.meta_12m.slice(0, 3).every((v, i) => Math.abs(v - metaAntes[i]) < 1e-12),
     'e NAO toca na outra parte -- e isso que faz o cenario ser diferente');
  ok(Math.abs(SIM.cx.ancora[0] - (ancAntes2[0] + 1.5)) < 1e-9,
     'o agregado e recomposto pela formula, nao chutado',
     ancAntes2[0].toFixed(3) + ' -> ' + SIM.cx.ancora[0].toFixed(3));
  ok(SIM.aberto.ancora === true,
     'e o cartao abre nas partes, para o usuario ver onde o choque entrou');
  restaura();

  // O choque pula trimestre ja publicado: X "no primeiro trimestre" quer dizer o
  // primeiro que da para editar, senao ele se perde conforme o dado avanca.
  SIM.i0 = D.sim.rot.length - 2;
  SIM.h = 8;
  SIM.fonte.di = 'digitado';
  ctx.renderSim();
  const cobDi = ctx._simCobertura('di', SIM.i0, D.sim.h_max);
  const nPub = cobDi.filter(Boolean).length;
  ok(nPub > 0, 'este cenario tem trimestre publicado na janela', String(nPub));
  const diAntes = SIM.cx.di.slice();
  SIM.chq.di = { tipo: 'const', v: 1, n: 99, rho: 1 };
  ctx.simAplicarChoque('di', null);
  ok(SIM.cx.di.slice(0, nPub).every((v, i) => Math.abs(v - diAntes[i]) < 1e-12),
     'o trimestre ja publicado nao recebe choque nenhum');
  ok(Math.abs(SIM.cx.di[nPub] - (diAntes[nPub] + 1)) < 1e-9,
     'e o choque comeca inteiro no primeiro trimestre editavel',
     diAntes[nPub].toFixed(3) + ' -> ' + SIM.cx.di[nPub].toFixed(3));
  restaura();

  // ── 8k. a equacao NAO fica no simulador ──
  // Pedido do usuario: "deixa a equacao somente nas abas individuais". A aba de
  // Juros continua com ela, e e para la que o subtitulo do bloco 1 aponta.
  ok(document.getElementById('tayMathSimb').innerHTML.indexOf('∑') >= 0,
     'a equacao de juros continua escrita na aba dela');
  ok(/aba Juros/.test(document.getElementById('simEqSub').innerHTML),
     'e o bloco 1 do simulador manda o leitor para la');

  // ── 8l. o grafico, no contrato da casa ──
  const yt = PLOT['ch-sim'].layout.yaxis.title;
  ok((yt || '').length > 6, 'o eixo do simulador nomeia a unidade', yt);
  const frS = document.getElementById('ch-sim').parentNode._chFrame;
  ok(frS.title.textContent.length > 8, 'ch-sim: tem titulo');
  ok(frS.sub.textContent.length > 8, 'ch-sim: tem subtitulo derivado');
  ok(frS.src.textContent.indexOf('Fonte:') === 0, 'ch-sim: e linha de fonte');
  const kidsS = Array.prototype.slice.call(
    document.getElementById('ch-sim').parentNode.children);
  let iBarS = -1;
  kidsS.forEach((c, j) => { if (c._cls().includes('range-pills')) iBarS = j; });
  ok(iBarS > kidsS.indexOf(document.getElementById('ch-sim')),
     'ch-sim: a regua de tempo vem depois do grafico');
  ok(Array.isArray(PLOT['ch-sim'].layout.shapes),
     'ch-sim: as formas sao passadas SEMPRE, para o react nao herdar as do desenho '
     + 'anterior');
}

// ── Fim ───────────────────────────────────────────────────────────────────────
console.log('\n' + '='.repeat(62));
console.log(oks + ' ok, ' + falhas + ' falharam');
process.exit(falhas ? 1 : 0);
