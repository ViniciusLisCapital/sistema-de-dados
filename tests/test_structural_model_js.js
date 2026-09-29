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
 'simSemDados', 'simConteudo',
 // Um cartao por equacao, sufixado pela chave dela. A lista sai do proprio markup
 // logo abaixo, e nao escrita aqui, para uma equacao nova nao passar em silencio.
 ...[...CRU.matchAll(/id="simGrid-(\w+)"/g)].flatMap((m) => [
   'simEqTitulo-' + m[1], 'simEqSub-' + m[1], 'simAviso-' + m[1], 'simGrid-' + m[1]]),
 'simJanela', 'simInputs',
 'irfSemDados', 'irfConteudo', 'irfIntro', 'irfBar', 'irfAviso', 'irfPillTri', 'irfPill12',
 'irfGrid', 'irfGruposNota', 'irfGridGrupos'].forEach((id) => {
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
  'ch-grr': ['gap_juro', 'g_rr'],
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

// ── §6b ───────────────────────────────────────────────────────────────────────
secao('6b. As taxas de inflacao da aba de dados tambem se leem em 12 meses');
{
  const DV = 'ch-grupos';
  const KS = ESPERADO[DV];
  const dz = D.doze;
  ok(!!dz && KS.every((k) => Array.isArray(dz.s12[k]) && dz.s12[k].length === D.x.length),
     'o payload traz a leitura de 12 meses das cinco taxas, na grade do painel');
  // refeita AQUI, dos trimestres, e nao comparada com o retorno de uma funcao da pagina
  const enc = (v, i) => {
    if (i < 3) return null;
    let f = 1;
    for (let j = i - 3; j <= i; j++) { if (v[j] == null) return null; f *= 1 + v[j] / 100; }
    return (f - 1) * 100;
  };
  let pior = 0, n = 0;
  KS.forEach((k) => D.s[k].forEach((_, i) => {
    const a = enc(D.s[k], i), b = dz.s12[k][i];
    if ((a == null) !== (b == null)) { pior = Infinity; return; }
    if (a != null) { pior = Math.max(pior, Math.abs(a - b)); n++; }
  }));
  ok(pior < 2e-3 && n > 400, 'cada ponto e o encadeamento dos quatro trimestres, nao a soma',
     n + ' pontos, pior ' + pior.toExponential(2));
  let pr = 0, nr = 0;
  dz.s12.pi_q.forEach((v, i) => {
    if (v != null && dz.ref12[i] != null) { pr = Math.max(pr, Math.abs(v - dz.ref12[i])); nr++; }
  });
  ok(pr < 0.01 && nr > 80, 'o IPCA cheio encadeado reproduz o de 12 meses PUBLICADO',
     nr + ' trimestres, pior ' + pr.toFixed(4));
  ok(Math.abs(pr - dz.erro_max) < 1e-3 && nr === dz.n,
     'e o erro que a pagina imprime e o medido', dz.erro_max + ' contra ' + pr.toFixed(4));
  const nota = document.getElementById('introNota').textContent;
  ok(nota.indexOf(dz.erro_max.toFixed(4).replace('.', ',')) >= 0 && nota.indexOf('12 meses') >= 0,
     'a introducao da aba diz que a leitura existe, e o erro contra o publicado', nota);

  const card = document.getElementById(DV).parentNode;
  const bar = document.getElementById('vb-' + DV);
  ok(!!bar && bar.parentNode === card, 'o seletor fica DENTRO do cartao do grafico');
  const pills = bar ? bar.children.filter((c) => c._cls().includes('vista-pill')) : [];
  ok(pills.length === 2 && pills[0].textContent === 'Do trimestre'
     && pills[1].textContent === 'Em 12 meses', 'duas leituras: do trimestre e em 12 meses',
     pills.map((p) => p.textContent).join(','));
  ok(pills.length === 2 && pills[0]._cls().includes('active') && !pills[1]._cls().includes('active'),
     'nasce na leitura do trimestre, que e a que as contas usam');
  const iHead = card.children.indexOf(card._chFrame.head);
  const iBar = card.children.indexOf(bar), iPlot = card.children.indexOf(document.getElementById(DV));
  ok(iHead < iBar && iBar < iPlot, 'entre o cabecalho e o grafico', iHead + ' ' + iBar + ' ' + iPlot);
  // so este cartao tem a segunda leitura: cambio e commodities seguem sem seletor
  ok(!document.getElementById('vb-ch-cambio') && !document.getElementById('vb-ch-comm'),
     'nenhum outro cartao ganhou o seletor');

  const TIT_TRI = card._chFrame.title.textContent;
  const infoBtn = card.children[0].children[0];
  const unidade = () => {
    ctx._pinned = null;
    infoBtn.dispatch('mouseenter');
    const m = /Unidade: ([^<]*)/.exec(ctx._pop ? ctx._pop.innerHTML : '');
    return m ? m[1] : null;
  };
  ok(unidade() === 'variação do trimestre, %', 'o cartao de definicao diz a unidade do trimestre',
     String(unidade()));

  if (pills.length === 2) {
    const antes = RELAYOUTS.length;
    pills[1].dispatch('click');
    const e = PLOT[DV];
    ok(e.traces.length === KS.length && e.traces.every((t, j) => t.y === dz.s12[KS[j]]),
       'em 12 meses as cinco linhas passam a ser as encadeadas');
    ok(e.layout.yaxis.title === 'variação em 12 meses, %', 'e o eixo diz isso',
       String(e.layout.yaxis.title));
    ok(card._chFrame.sub.textContent.indexOf('variação em 12 meses, %') >= 0,
       'o subtitulo imprime a mesma unidade do eixo', card._chFrame.sub.textContent);
    ok(card._chFrame.title.textContent === 'Inflação em 12 meses, cheio e por grupo de preço',
       'o titulo muda junto: o clique muda o que o grafico afirma', card._chFrame.title.textContent);
    ok(unidade() === 'variação em 12 meses, %', 'e o cartao de definicao tambem', String(unidade()));
    ok(pills[1]._cls().includes('active') && !pills[0]._cls().includes('active'),
       'a pill ativa acompanha o clique');
    let iu = -1;
    dz.s12.pi_q.forEach((v, i) => { if (v != null) iu = i; });
    const st = document.getElementById('st-' + DV).innerHTML;
    ok(st.indexOf(ctx.fmt(dz.s12.pi_q[iu])) >= 0 && st.indexOf(D.rot[iu]) >= 0,
       'o ultimo/maxima/minima passa a ler a serie de 12 meses', D.rot[iu] + ' ' + dz.s12.pi_q[iu]);
    // a regua e refeita: a primeira janela de 12 meses fecha tres trimestres depois
    const r = RELAYOUTS.slice(antes).filter((x) => x.div === DV && x.upd['xaxis.range']);
    let i0 = D.x.length;
    KS.forEach((k) => { const j = dz.s12[k].findIndex((v) => v != null); if (j >= 0) i0 = Math.min(i0, j); });
    ok(r.length >= 1 && Math.abs(Date.parse(r[r.length - 1].upd['xaxis.range'][0])
                                 - (Date.parse(D.x[i0]) - passo)) <= 864e5,
       'o "Tudo" de 12 meses comeca na primeira janela, nao na grade', r.length ? r[r.length - 1].upd['xaxis.range'][0] : '-');
    const ativos = document.getElementById('rp-' + DV).children.filter((b) => b._cls().includes('active'));
    ok(ativos.length === 1 && ativos[0].textContent === 'Tudo', 'e a regua volta ao "Tudo"');
    ok(PLOT['ch-cambio'].traces[0].y === D.s.de, 'os outros graficos nao mudam');

    // clicar na leitura ja ativa nao redesenha
    const nPlot = RELAYOUTS.length;
    pills[1].dispatch('click');
    ok(RELAYOUTS.length === nPlot, 'clicar na leitura ja ativa nao faz nada');

    pills[0].dispatch('click');
    const e2 = PLOT[DV];
    ok(e2.traces.every((t, j) => t.y === D.s[KS[j]]) && e2.layout.yaxis.title === 'variação do trimestre, %'
       && card._chFrame.title.textContent === TIT_TRI && unidade() === 'variação do trimestre, %',
       'e volta: series, eixo, titulo e unidade do trimestre');
  }
  // o ajuste de Y e ligado UMA vez por grafico: nem nenhuma (a primeira pintura tratada
  // como redesenho), nem uma a mais a cada troca de leitura
  Object.keys(ESPERADO).forEach((div) => {
    const n = (document.getElementById(div)._lis.plotly_relayout || []).length;
    ok(n === 1, div + ': o ajuste de Y ligado uma vez, mesmo depois das trocas', String(n));
  });
  ctx._pinned = null;
  if (ctx.hideInfo) ctx.hideInfo();
}

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
  // A TABELA de formas da (F) tambem e texto que o leitor le, e a descricao de cada
  // forma vem do payload. Ela ficou de fora da varredura ate 2026-09-25, quando uma
  // delas entrou carregando data de decisao nossa.
  tblFxComp: _prosa('tblFxComp'),
};
ok(noHtml.length >= 3, 'achou os blocos de prosa no HTML', String(noHtml.length));
ok(fixos.length >= 2, 'ha prosa escrita a mao', String(fixos.length));
ok(noHtml.length - fixos.length >= 1, 'ha prosa preenchida no render');

const junta = fixos.concat(Object.keys(derivados).map((k) => derivados[k])).join(' \n ');
PROIBIDO.forEach((t) => ok(junta.indexOf(t) < 0, 'a prosa nao usa "' + t + '"'));
// Data de decisao NOSSA, em qualquer forma. "Desde 2026" pegava uma redacao so; uma
// data ISO solta e sempre nossa -- o leitor nao tem o que fazer com ela, e ela so
// levanta "e antes disso?". Datas de DADO na pagina sao trimestres (2026T2), entao
// esta classe nao tem falso positivo aqui.
const isoData = junta.match(/20\d\d-\d\d-\d\d/g) || [];
ok(isoData.length === 0,
   'a prosa nao carrega data de decisao nossa em forma ISO',
   isoData.join(', ') || '(nenhuma)');
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
ok(TABS.join(',') === 'tab-dados,tab-modelo,tab-exp,tab-is,tab-tay,tab-fx,tab-sim,tab-irf',
   'as oito abas, nesta ordem', TABS.join(','));
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

  // ── a tabela das medidas do aperto: e o registro do POR QUE da escolha. Desde
  //    2026-09-25 a escolhida e a Selic contra a ancora da regra de juros, e a
  //    inclinacao da curva real -- a anterior -- continua na tabela.
  ok(Array.isArray(H.rr) && H.rr.length >= 5,
     'a tabela tem as candidatas medidas, a inclinacao anterior e o gap',
     String((H.rr || []).length));
  ok(H.rr.filter((r) => r.escolhida).length === 1,
     'exatamente uma linha e marcada como a escolhida');
  ok(H.rr.filter((r) => r.escolhida)[0].key === 'gap',
     'e ela e a Selic contra a ancora da regra de juros');
  {
    const n0 = H.rr[0].n;
    ok(H.rr.every((r) => r.n === n0),
       'todas medidas na MESMA janela, senao a tabela nao compara nada',
       H.rr.map((r) => r.n).join(','));
    const fixas = H.rr.filter((r) => r.key === 'const' || r.key === 'bc');
    const nossa = H.rr.filter((r) => r.key === 'gap')[0];
    const inc = H.rr.filter((r) => r.key === 'incl')[0];
    ok(fixas.length === 2, 'as duas taxas fixas estao na tabela');
    ok(fixas.every((r) => Math.abs(r.t) < 2),
       'e nelas o aperto e indistinguivel de zero -- que e o motivo de nao usa-las',
       fixas.map((r) => _f(r.t, 2)).join(' / '));
    ok(Math.abs(nossa.t) >= 2, 'enquanto a Selic contra a ancora mede alguma coisa',
       _f(nossa.t, 2));
    ok(!!inc && Math.abs(inc.t) >= 2, 'e a inclinacao, que continua na tabela, tambem',
       inc ? _f(inc.t, 2) : '-');
    ok(Math.abs(nossa.h2 - cApt.b) < 1e-5,
       'e a linha escolhida traz o MESMO peso que a conta da pagina',
       nossa.h2 + ' vs ' + cApt.b);

    // O PESO POR PONTO NAO SE COMPARA entre medidas de dispersao diferente -- o gap
    // oscila 2,6x o que a inclinacao oscila. A coluna por desvio existe por isso, e as
    // duas asserções abaixo afirmam o fato que ela mostra: por ponto os pesos parecem
    // de ordens diferentes, por desvio eles quase coincidem.
    H.rr.forEach((r) => {
      ok(Math.abs(r.h2_dp - r.h2 * r.sd) < 1e-5,
         r.key + ': o peso por desvio e o peso por ponto vezes o desvio da medida',
         _f(r.h2_dp, 4) + ' vs ' + _f(r.h2 * r.sd, 4));
    });
    const razaoPonto = inc.h2 / nossa.h2, razaoDp = inc.h2_dp / nossa.h2_dp;
    ok(razaoPonto > 2,
       'por ponto, os dois pesos parecem de ordens diferentes',
       _f(razaoPonto, 2) + 'x');
    ok(Math.abs(razaoDp - 1) < 0.25,
       'e por desvio da propria medida eles quase coincidem -- o que a tabela existe '
       + 'para mostrar', _f(razaoDp, 2) + 'x');
    const tr = document.getElementById('tblIsRR').innerHTML;
    ok(tr.indexOf('Peso por desvio da medida') >= 0 && tr.indexOf(_f(nossa.h2_dp, 3)) >= 0,
       'a coluna por desvio esta na tela, com o numero do payload');
    const nr = document.getElementById('isRRNota').textContent;
    ok(nr.indexOf(_f(inc.h2_dp, 3)) >= 0 && nr.indexOf(_f(nossa.h2_dp, 3)) >= 0,
       'e a nota cita os dois pesos por desvio, derivados');
    ok(nr.indexOf('inclinação da curva não tem esse problema') < 0,
       'a frase que defendia a inclinacao como a escolhida saiu da nota');
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
    const incC = H.comparar.filter((r) => r.key === 'incl')[0];
    ok(!!incC, 'e a inclinacao da curva real, no lugar da Selic, tambem');
    ok((document.getElementById('isCompNota').textContent || '')
         .indexOf(_f(incC.h2, 3)) >= 0,
       'a nota da tabela cita o peso da inclinacao, derivado');
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
    // Desde 2026-09-25 o erro NAO tem mais padrao: foi o que a troca da inclinacao
    // pela Selic contra a ancora comprou (Ljung-Box de 0,021 para 0,070). O fio
    // inverteu junto -- se voltar a acusar padrao, a prosa acima muda sozinha, e este
    // teste avisa que o motivo da troca deixou de valer.
    ok(!sobra, 'nesta forma o erro NAO tem mais padrao -- se isso mudar, o argumento da '
       + 'troca de medida enfraquece (Ljung-Box p ' + _f(H.lb_p4, 4) + ')');
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

  // ── a comparacao com o BC: desde 2026-09-25 o aperto E comparavel -- os dois sao
  //    juro real contra um juro de equilibrio, em p.p. -- e a linha do BC mostra o
  //    EFEITO por ponto (-b2/4), que e a unidade do nosso h2
  {
    ok(H.bc.b1.comparavel === true, 'o peso do hiato anterior e comparavel com o do BC');
    ok(H.bc.b2.comparavel === true,
       'e o do aperto tambem: os dois medem juro real contra um equilibrio');
    ok(Math.abs(H.bc.b2.v - (-H.bc.b2.b2_publicado / 4)) < 1e-9,
       'a linha do BC e o efeito por ponto, -b2/4, e nao o b2 publicado',
       _f(H.bc.b2.v, 4) + ' vs b2 ' + _f(H.bc.b2.b2_publicado, 3));
    ok(H.bc.b2.ic[0] < H.bc.b2.ic[1],
       'e a margem foi convertida junto, com as pontas na ordem certa',
       _f(H.bc.b2.ic[0], 4) + ' a ' + _f(H.bc.b2.ic[1], 4));
    const nb = document.getElementById('isBcNota').textContent;
    const dentro2 = cApt.b >= H.bc.b2.ic[0] && cApt.b <= H.bc.b2.ic[1];
    ok(nb.indexOf(_f(H.bc.b2.v, 3)) >= 0 && nb.indexOf(_f(cApt.b, 3)) >= 0,
       'a nota imprime os dois efeitos, o do BC e o nosso');
    ok(nb.indexOf(dentro2 ? 'dentro da margem dele' : 'fora da margem dele') >= 0,
       'e diz se o nosso cai dentro da margem do BC -- o que o numero diz');
    ok(nb.indexOf('unidade do outro') < 0,
       'a frase de que nao eram comparaveis saiu');
    // Fio: hoje o nosso efeito cai DENTRO da margem publicada pelo BC. A prosa acima
    // se ajusta sozinha se isso mudar; este teste existe para alguem olhar.
    ok(dentro2, 'o efeito do aperto cai dentro da margem do BC -- se sair, olhe',
       _f(cApt.b, 4) + ' em [' + _f(H.bc.b2.ic[0], 4) + ', ' + _f(H.bc.b2.ic[1], 4) + ']');
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
  // `D.sim.eq_ordem[0]` era a (R) ate 2026-09-25 e passou a ser a (E): ler a equacao
  // pela POSICAO na ordem de solucao era uma comodidade que virou armadilha silenciosa
  // no minuto em que a ordem ganhou um elemento na frente.
  const EQ = D.sim.eq.R, EQE = D.sim.eq.E;
  const SIM = ctx.SIM;

  // ── 8a. o payload ──
  ok(D.sim.eq_ordem.length >= 1, 'ha pelo menos uma equacao', D.sim.eq_ordem.join(','));
  ok(D.sim.var_ordem.length >= 1, 'ha inputs declarados', D.sim.var_ordem.join(','));
  ok(D.sim.h_max === 12, 'o horizonte tem teto de 12 trimestres', String(D.sim.h_max));
  ok(EQ.draws && EQ.draws.t1.length === EQ.n_draws,
     'os desenhos do posterior vieram completos', String(EQ.n_draws));
  ok(EQ.n_draws_total > EQ.n_draws, 'os desenhos sao um afinamento do posterior',
     EQ.n_draws + ' de ' + EQ.n_draws_total);

  // ── 8a2. as crises entram na conta, mas nao sao input ──
  // Cortadas do bloco 2 em 2026-09-24 (*"pretendo usa-las mais como ajuste do que
  // variaveis exogenas"*). O risco do corte e silencioso: tirar o cartao e tirar os
  // pesos da recursao junto, e o caminho continua saindo plausivel.
  ok(D.sim.var_ordem.indexOf('crise') < 0 && !D.sim.var.crise,
     'nao ha cartao de crise no bloco de inputs', D.sim.var_ordem.join(','));
  ok(!D.sim.prim,
     'e nao ha mais dicionario de primitivas: todo cartao tem serie propria');
  ok(EQ.dummies.length === 2 && EQ.dummies.join(',') === 'd08,d20',
     'mas a equacao continua com as duas marcas', EQ.dummies.join(','));
  EQ.dummies.forEach((c) => {
    ok(Array.isArray(EQ.dummy_obs[c]) && EQ.dummy_obs[c].length === EQ.y.length,
       c + ': a serie viaja na equacao, com uma posicao por trimestre da amostra');
    ok(EQ.dummy_obs[c].some((x) => x === 1), c + ': e ela marca a janela dela');
    ok(EQ.pars.indexOf(c) >= 0 && typeof EQ.mediana[c] === 'number',
       c + ': com o peso estimado no payload', String(EQ.mediana[c]));
  });
  // E o que a recursao recebe na janela projetada e zero -- se o cartao tivesse sido
  // cortado junto com a serie, `ent[c]` viria indefinido e a soma sairia NaN.
  const entCr = ctx.simEntradas();
  EQ.dummies.forEach((c) => {
    ok(Array.isArray(entCr[c]) && entCr[c].every((x) => x === 0),
       c + ': vale zero em todo trimestre projetado', String(entCr[c] && entCr[c][0]));
  });

  // ── 8b. endogena/exogena e propriedade do MODELO, e o payload separa os dois fatos ──
  const VSel = D.sim.var.selic, VPie = D.sim.var.pi_e, VMeta = D.sim.var.meta_12m;
  ok(VSel.tipo === 'endogena' && VSel.produzida_por === 'R' && VSel.produtor_no_sim,
     'a Selic e endogena: a equacao que a produz esta no simulador');
  ok(VPie.tipo === 'endogena' && VPie.produzida_por === 'E' && VPie.produtor_no_sim,
     'e a expectativa tambem, desde que a (E) entrou',
     VPie.produzida_por + ' / produtor_no_sim=' + VPie.produtor_no_sim);
  // "Endogena" e propriedade do MODELO e nao do simulador. A inflacao do trimestre foi
  // o caso vivo disso ate 2026-09-28: a curva de Phillips a produzia e nao estava aqui.
  // Com ela dentro, as cinco variaveis que o modelo produz sao endogenas NESTA rodada.
  const VInf = D.sim.var.infl_br;
  ok(VInf.produzida_por === 'I' && VInf.produtor_no_sim === true
     && VInf.tipo === 'endogena',
     'a inflacao do Brasil e endogena: a curva de Phillips a produz, aqui dentro',
     VInf.produzida_por + ' / produtor_no_sim=' + VInf.produtor_no_sim);
  ok(D.sim.var_ordem.every((k) => !D.sim.var[k].produzida_por
                                  || D.sim.var[k].produtor_no_sim),
     'e nenhuma variavel tem equacao no modelo fora do simulador -- as cinco rodam');
  ok(VMeta.tipo === 'exogena' && VMeta.produzida_por === null,
     'a meta e exogena e NENHUMA equacao do modelo a produz -- ela e decisao do CMN');

  // ── 8b2. nao ha mais premissa com subpremissa ──
  // Pedido do usuario em 2026-09-25: *"nao havera mais premissas com subpremissas.
  // Todas serao separadas em exogenas e endogenas."* O que era peca virou cartao, e a
  // conta mudou de dono -- ela passou a ser declarada pela EQUACAO que a consome.
  ok(!D.sim.prim, 'o dicionario de primitivas saiu do payload');
  ok(D.sim.var_ordem.every((k) => !D.sim.var[k].partes && !D.sim.var[k].formula),
     'e nenhum cartao declara partes ou formula',
     D.sim.var_ordem.filter((k) => D.sim.var[k].partes).join(',') || '(nenhum)');
  ['di', 'ancora', 'ppp', 'crise'].forEach((k) => {
    ok(!D.sim.var[k], 'o cartao composto `' + k + '` deixou de existir');
  });
  ['pi_e', 'meta_12m', 'rr_10a', 'infl_br', 'infl_us'].forEach((k) => {
    ok(!!D.sim.var[k] && D.sim.var_ordem.indexOf(k) >= 0,
       'e `' + k + '`, que era peca, virou cartao proprio');
  });
  // As contas continuam existindo -- so mudaram de dono. Quem as declara e a equacao.
  ok(EQ.deriva.di.de.join(',') === 'pi_e,meta_12m' && EQ.deriva.di.op === '-',
     'o desvio da inflacao e conta da (R): expectativa menos meta',
     EQ.deriva.di.de.join(' ' + EQ.deriva.di.op + ' '));
  ok(EQ.deriva.ancora.de.join(',') === 'rr_10a,meta_12m'
     && EQ.deriva.ancora.op === '+',
     'e o juro nominal de equilibrio tambem: juro real de dez anos mais a meta');
  ok(D.sim.eq.F.deriva.ppp.de.join(',') === 'infl_br,infl_us',
     'o diferencial de inflacao e conta da (F): a inflacao daqui menos a de la');
  ok(EQE.deriva.i12.op === 'acum_log' && EQE.deriva.i12.k === 4
     && EQE.deriva.i12.de.join(',') === 'infl_br',
     'e o IPCA de 12 meses e conta da (E): quatro trimestres compostos',
     EQE.deriva.i12.op + ', k = ' + EQE.deriva.i12.k);
  // Toda peca de uma conta derivada tem de ter cartao -- uma chave errada nao levanta
  // nada, so faz a conta sair indefinida e o caminho inteiro virar NaN.
  D.sim.eq_ordem.forEach((ek) => {
    const dv = D.sim.eq[ek].deriva || {};
    Object.keys(dv).forEach((n) => {
      dv[n].de.forEach((p) => {
        ok(!!D.sim.var[p],
           '(' + ek + ') ' + n + ': a peca ' + p + ' tem cartao no bloco 2');
      });
    });
  });
  // E o que a equacao CONSOME sao cartoes, nunca uma conta derivada: um cartao de
  // `di` deixaria digitar um desvio que contradiz a expectativa da propria rodada.
  D.sim.eq_ordem.forEach((ek) => {
    const e = D.sim.eq[ek];
    e.consome.forEach((c) => {
      ok(!!D.sim.var[c], '(' + ek + ') consome ' + c + ', e ele tem cartao');
      ok(!(e.deriva || {})[c],
         '(' + ek + ') e ' + c + ' nao e ao mesmo tempo conta derivada');
    });
  });

  // ── 8b3. as exogenas se dividem em DOMESTICA e EXTERNA ──
  // Mesmo pedido. `tipo` responde "alguma equacao a produz?" e `regiao` so existe em
  // quem responde nao -- um `regiao` numa endogena seria um grupo que nao se desenha.
  // `tipo` e sobre ESTE simulador, e por isso ele e sempre igual a `produtor_no_sim`.
  // Os dois discordando nao levantaria nada: o cartao so cairia no grupo errado, e o
  // grupo e o que responde "eu digito isto ou nao?".
  D.sim.var_ordem.forEach((k) => {
    const v = D.sim.var[k];
    ok((v.tipo === 'endogena') === !!v.produtor_no_sim,
       k + ': `tipo` e `produtor_no_sim` dizem a mesma coisa',
       v.tipo + ' / ' + v.produtor_no_sim);
  });
  const REG = ['domestica', 'externa'];
  D.sim.var_ordem.forEach((k) => {
    const v = D.sim.var[k];
    if (v.tipo === 'endogena') {
      ok(v.regiao === undefined, k + ': endogena nao declara regiao');
    } else {
      ok(REG.indexOf(v.regiao) >= 0,
         k + ': exogena declara domestica ou externa', String(v.regiao));
    }
  });
  REG.forEach((rg) => {
    const n = D.sim.var_ordem.filter((k) => D.sim.var[k].regiao === rg).length;
    ok(n > 0, 'o recorte ' + rg + ' nao esta vazio -- ele separa de fato', String(n));
    ok(!!(D.sim.regioes || {})[rg] && D.sim.regioes[rg].nome,
       'e ele tem rotulo no payload, nao escrito no relatorio',
       (D.sim.regioes[rg] || {}).nome);
  });
  // Os dois exemplos que o usuario deu ao definir o criterio, e os dois que ele nao
  // deu e sao os ambiguos: o CDS e risco do Brasil, o IC-Br e preco formado fora.
  ok(D.sim.var.ffr.regiao === 'externa', 'o Fed Funds e externo');
  ok(D.sim.var.vol.regiao === 'domestica',
     'e a volatilidade do real e domestica: e o preco de um ativo brasileiro');
  ok(D.sim.var.fiscal.regiao === 'domestica',
     'o CDS soberano e domestico -- e risco de credito do Brasil');
  ok(D.sim.var.icbr_usd.regiao === 'externa',
     'e as commodities em dolar sao externas: a cesta e daqui, o preco nao');

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
  const barraJan = document.getElementById('simJanela').innerHTML;
  ok(!/<select/.test(barraJan), 'nao ha seletor de partida: a janela e uma so');
  // E o horizonte tambem deixou de ser escolha -- pedido do usuario em 2026-09-24,
  // *"deixe sempre 12T"*. A barra DIZ o tamanho, nao pergunta.
  ok(!/<input/.test(barraJan),
     'e nao ha caixa de horizonte: a barra da janela nao tem controle nenhum');
  ok(/12 trimestres/.test(barraJan), 'a barra imprime o tamanho da projecao');
  ok(SIM.h === D.sim.h_padrao && SIM.h === 12, 'e projeta 12 trimestres',
     String(SIM.h));
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
  // Na janela padrao NENHUMA caixa e de trimestre publicado: elas seguram o ultimo
  // valor conhecido, e e isso que a cor dourada diz.
  //
  // Ate 2026-09-25 havia uma excecao, a volatilidade, porque a serie dela vinha
  // defasada um trimestre e a do primeiro trimestre projetado ja estava medida. Com
  // a vol IMPLICITA entrando no proprio trimestre isso deixou de valer: a cotacao de
  // um trimestre que ainda nao aconteceu nao existe. A asserção virou do contrario
  // e ficou mais forte -- um trimestre a mais aqui seria um numero que ninguem
  // observou, impresso em verde e travado, que e a pior forma de estar errado.
  const htmlProj = document.getElementById('simInputs').innerHTML;
  ok(/sim-caixa-in seg/.test(htmlProj),
     'projetando, as caixas saem em dourado -- nao ha trimestre publicado ali');
  const verdes = D.sim.var_ordem.filter((k) =>
    ctx._simCobertura(k, SIM.i0, SIM.h).some(Boolean));
  ok(verdes.length === 0,
     'e NENHUMA premissa tem trimestre publicado adiante da grade',
     verdes.join(',') || '(nenhuma)');
  // E a mesma afirmacao pelo lado da serie: a da volatilidade termina onde terminam
  // as outras premissas da (F), em vez de um trimestre depois.
  const _fim = (k) => {
    const o = D.sim.var[k].obs;
    let i = o.length - 1;
    while (i >= 0 && (o[i] === null || o[i] === undefined)) i -= 1;
    return i;
  };
  ok(_fim('vol') === _fim('fiscal'),
     'a serie da volatilidade termina no mesmo trimestre que a do risco fiscal',
     _fim('vol') + ' contra ' + _fim('fiscal'));
  ok(D.sim.var.vol.obs.length === D.sim.var.fiscal.obs.length,
     'e ela nao carrega mais um trimestre alem da grade',
     D.sim.var.vol.obs.length + ' contra ' + D.sim.var.fiscal.obs.length);

  const g0 = { i0: SIM.i0, h: SIM.h, coef: JSON.parse(JSON.stringify(SIM.coef)),
               fonte: JSON.parse(JSON.stringify(SIM.fonte)) };
  function restaura() {
    SIM.i0 = g0.i0; SIM.h = g0.h;
    SIM.coef = JSON.parse(JSON.stringify(g0.coef));
    SIM.fonte = JSON.parse(JSON.stringify(g0.fonte));
    ctx.simRecarregarCaixas();
    ctx.renderSim();
  }

  // ── 8d. a restricao, conferida no caminho SIMULADO ──
  // Com a inflacao esperada na meta a conta tem de voltar para a ancora e parar ali.
  // Mesma propriedade que `taylor.repouso()` afirma do lado do Python, agora medida no
  // codigo que o navegador roda.
  SIM.i0 = D.sim.rot.length - 1;
  SIM.h = 8;
  // O desvio e a ancora deixaram de ser cartao: para pedir "inflacao esperada na meta
  // e ancora em 9" agora se impoem as TRES pecas. A conta continua a mesma.
  SIM.fonte.pi_e = 'digitado';
  SIM.fonte.meta_12m = 'digitado';
  SIM.fonte.rr_10a = 'digitado';
  SIM.cx.pi_e = new Array(D.sim.h_max).fill(3);
  SIM.cx.meta_12m = new Array(D.sim.h_max).fill(3);
  SIM.cx.rr_10a = new Array(D.sim.h_max).fill(6);
  ctx.renderSim();
  ok(SIM._ultimo.di.every((v) => Math.abs(v) < 1e-12),
     'com a expectativa na meta, o desvio que a equacao multiplica e zero',
     SIM._ultimo.di[0].toFixed(9));
  ok(SIM._ultimo.anc.every((v) => Math.abs(v - 9) < 1e-12),
     'e a ancora que ela soma e 9 -- as duas contas saem das tres pecas');
  // 8 trimestres nao bastam para convergir de verdade (meia-vida 3,6), entao a
  // afirmacao e de DIRECAO: cada passo anda para a ancora e o ultimo esta perto.
  let cam = SIM._ultimo.cam;
  ok(Math.abs(cam[cam.length - 1] - 9) < Math.abs(cam[0] - 9),
     'com a inflacao esperada na meta o caminho anda na direcao da ancora',
     cam[0].toFixed(3) + ' -> ' + cam[cam.length - 1].toFixed(3));
  // Com horizonte longo a conta converge exatamente -- rodada aqui pela funcao, sem
  // passar pelo teto de 8 da tela, que e limite de INTERFACE e nao da conta.
  const entLonga = { pi_e: new Array(200).fill(3),
                     meta_12m: new Array(200).fill(3),
                     rr_10a: new Array(200).fill(6) };
  EQ.dummies.forEach((c) => { entLonga[c] = new Array(200).fill(0); });
  const longo = ctx._simCaminhoSelic(SIM.coef.R, SIM.i0, 200, entLonga);
  ok(Math.abs(longo[longo.length - 1] - 9) < 1e-6,
     'no longo prazo ela converge exatamente para a ancora',
     longo[longo.length - 1].toFixed(8));
  entLonga.pi_e = new Array(200).fill(4);
  const lp = ctx._simCaminhoSelic(SIM.coef.R, SIM.i0, 200, entLonga);
  ok(Math.abs((lp[lp.length - 1] - 9) - SIM.coef.R.t3) < 1e-6,
     'um desvio permanente de 1 p.p. leva a Selic a subir t3 no longo prazo',
     (lp[lp.length - 1] - 9).toFixed(6) + ' contra t3 = ' + SIM.coef.R.t3.toFixed(6));

  // ── 8e0. o juro nominal de equilibrio tambem segue para a frente ──
  // Pedido do usuario em 2026-09-24: *"o juro nominal tambem faz parte do grafico,
  // sendo assim, pode extrapola-lo para frente tambem"*. O que torna isso honesto e a
  // linha projetada ser EXATAMENTE o caminho que a recursao consome -- nao uma
  // extrapolacao propria do desenho, que poderia discordar da conta sem nada avisar.
  restaura();
  const trAnc = ctx._tracesSim(SIM._ultimo).filter(
    (t) => t.line && t.line.dash === 'dot');
  ok(trAnc.length === 2,
     'sao duas linhas pontilhadas: o observado e o trecho projetado',
     String(trAnc.length));
  const projAnc = trAnc[1];
  ok(projAnc.showlegend === false,
     'a projetada nao ganha legenda propria -- e a mesma linha continuando');
  ok(projAnc.y.length === SIM.h + 1,
     'ela cobre os 12 trimestres mais o ponto de onde parte', String(projAnc.y.length));
  // A serie observada da ancora deixou de estar no payload em 2026-09-25: ela e a
  // conta que a equacao faz com o juro real de dez anos e a meta. O teste refaz a
  // MESMA conta, pela mesma declaracao -- uma copia gravada seria uma copia a mais.
  const ancSerie = ctx._simDerivObs('R', 'ancora');
  ok(Math.abs(projAnc.y[0] - ancSerie[SIM.i0 - 1]) < 1e-9,
     'e parte do ultimo valor observado, para nao flutuar solta a direita',
     projAnc.y[0].toFixed(3));
  ok(Math.abs(ancSerie[SIM.i0 - 1]
       - (D.sim.var.rr_10a.obs[SIM.i0 - 1] + D.sim.var.meta_12m.obs[SIM.i0 - 1]))
       < 1e-9,
     'e essa conta e mesmo juro real de dez anos mais a meta');
  ok(projAnc.y.slice(1).every((v, i) => Math.abs(v - SIM._ultimo.anc[i]) < 1e-9),
     'o trecho projetado E o caminho que a conta consome, trimestre a trimestre');
  // E por isso ele acompanha a premissa: digitar outro caminho move a linha. Com a
  // ancora virando conta, digita-se a PECA -- o resultado na tela e o mesmo.
  SIM.fonte.rr_10a = 'digitado';
  SIM.fonte.meta_12m = 'digitado';
  SIM.cx.rr_10a = new Array(D.sim.h_max).fill(4.25);
  SIM.cx.meta_12m = new Array(D.sim.h_max).fill(3);
  ctx.renderSim();
  const projDig = ctx._tracesSim(SIM._ultimo)
    .filter((t) => t.line && t.line.dash === 'dot')[1];
  ok(projDig.y.slice(1).every((v) => Math.abs(v - 7.25) < 1e-9),
     'com a premissa digitada a linha desenha o que foi digitado',
     projDig.y[1].toFixed(3));
  ok(Math.abs(projDig.y[0] - projAnc.y[0]) < 1e-9,
     'e o ponto de partida continua sendo o observado, que ninguem digita');

  // ── 8e. a faixa ──
  // Ela nao e mais opcao: a caixa de marcar saiu em 2026-09-24 e a faixa passou a ser
  // conteudo. Incerteza MEDIDA nao e controle -- quem le nao escolhe nada ali.
  ctx.renderSim();
  ok(SIM.faixa === undefined && SIM.choque === undefined,
     'a faixa e o erro da equacao deixaram de ser estado: nao ha o que desligar');
  const fx = SIM._ultimo.faixa;
  ok(!!fx, 'com a equacao rodando o resultado traz lo/hi, sempre');
  ok(fx.lo.length === SIM.h && fx.hi.length === SIM.h,
     'a faixa tem um par por trimestre simulado');
  ok(fx.lo.every((v, i) => v <= fx.hi[i]), 'a borda de baixo nunca passa a de cima');
  ok((fx.hi[SIM.h - 1] - fx.lo[SIM.h - 1]) > (fx.hi[0] - fx.lo[0]),
     'a faixa ALARGA com o horizonte -- e incerteza propagada pela dinamica',
     (fx.hi[0] - fx.lo[0]).toFixed(3) + ' -> '
       + (fx.hi[SIM.h - 1] - fx.lo[SIM.h - 1]).toFixed(3));
  // Ela e determinista: dois renders seguidos dao o MESMO desenho, senao ela tremeria
  // a cada clique em qualquer outro controle e pareceria que o resultado mudou.
  const larg = fx.hi[SIM.h - 1] - fx.lo[SIM.h - 1];
  ctx.renderSim();
  ok(Math.abs(larg
       - (SIM._ultimo.faixa.hi[SIM.h - 1] - SIM._ultimo.faixa.lo[SIM.h - 1])) < 1e-12,
     'e nao treme entre dois renders');

  // ── 8f. fonte por variavel ──
  restaura();
  const base = SIM._ultimo.cam[SIM._ultimo.cam.length - 1];
  SIM.fonte.pi_e = 'digitado';
  SIM.cx.pi_e = SIM.cx.pi_e.map((v) => v + 1);
  ctx.renderSim();
  const comDi = SIM._ultimo.cam[SIM._ultimo.cam.length - 1];
  ok(comDi > base, 'estressar so a inflacao esperada sobe a Selic simulada',
     base.toFixed(3) + ' -> ' + comDi.toFixed(3));

  // Uma PECA move a conta de que ela faz parte, e so ela. Era o teste do "abrir em
  // partes"; com cada peca virando cartao, a propriedade e a mesma e a mecanica some.
  restaura();
  const ancAntes = SIM._ultimo.anc[0], diAntes0 = SIM._ultimo.di[0];
  SIM.fonte.rr_10a = 'digitado';
  SIM.cx.rr_10a = SIM.cx.rr_10a.map((v) => v + 2);
  ctx.renderSim();
  ok(Math.abs(SIM._ultimo.anc[0] - (ancAntes + 2)) < 1e-9,
     'somar 2 ao juro real de dez anos soma 2 a ancora',
     ancAntes.toFixed(3) + ' -> ' + SIM._ultimo.anc[0].toFixed(3));
  // Com o laco fechado o juro real move a expectativa -- Selic, cambio, alimentacao,
  // IPCA, Focus --, entao o desvio pode andar. O que a conta garante e que ele anda SO
  // pelo que a expectativa andou: o juro real nao e peca dele.
  const peAntes0 = diAntes0 + D.sim.var.meta_12m.obs[D.sim.var.meta_12m.obs.length - 1];
  ok(Math.abs((SIM._ultimo.di[0] - diAntes0)
              - (SIM._ultimo.ent.pi_e[0] - peAntes0)) < 1e-9,
     'e o desvio da inflacao so se move pelo que a expectativa se moveu -- o juro real '
     + 'nao e peca da conta dele',
     'desvio ' + (SIM._ultimo.di[0] - diAntes0).toExponential(2));
  // A meta e a peca que MAIS de uma equacao le, e mexer nela move tudo de uma vez.
  // Com a (E) ligada ela entra por dois caminhos de sinais opostos, e e por isso que
  // o efeito liquido nao e obvio -- a ficha do cartao diz isso ao leitor.
  restaura();
  const anc2 = SIM._ultimo.anc[0], di2 = SIM._ultimo.di[0];
  SIM.fonte.meta_12m = 'digitado';
  SIM.cx.meta_12m = SIM.cx.meta_12m.map((v) => v + 1);
  ctx.renderSim();
  ok(Math.abs(SIM._ultimo.anc[0] - (anc2 + 1)) < 1e-9,
     'subir a meta em 1 sobe a ancora em 1, exatamente',
     anc2.toFixed(3) + ' -> ' + SIM._ultimo.anc[0].toFixed(3));
  const quedaDi = di2 - SIM._ultimo.di[0];
  ok(quedaDi > 0 && quedaDi < 1,
     'e reduz o desvio em MENOS de 1: a expectativa segue a meta em parte, porque a '
     + '(E) tambem le a meta -- com ela desligada a queda seria de 1 exato',
     'caiu ' + quedaDi.toFixed(4) + ' p.p.');
  // Com a (E) desligada a conta vira aritmetica pura, e o teste afirma isso para
  // separar o efeito da equacao do efeito da subtracao.
  SIM.fonte.pi_e = 'observado';
  ctx.renderSim();
  const diSemE = SIM._ultimo.di[0];
  SIM.cx.meta_12m = SIM.cx.meta_12m.map((v) => v + 1);
  ctx.renderSim();
  ok(Math.abs((diSemE - SIM._ultimo.di[0]) - 1) < 1e-9,
     'com a expectativa imposta, subir a meta em 1 reduz o desvio em 1 exato',
     (diSemE - SIM._ultimo.di[0]).toFixed(9));

  // A Selic imposta desliga a equacao.
  restaura();
  SIM.fonte.selic = 'observado';
  ctx.renderSim();
  ok(SIM._ultimo.faixa === null,
     'com a Selic imposta nao ha faixa: nao ha equacao rodando');
  ok(SIM._ultimo.cam.every((v, i) => Math.abs(v - ctx.simObs('selic', SIM.i0, SIM.h)[i])
       < 1e-9),
     'e o caminho desenhado e exatamente o observado');
  ok(document.getElementById('simAviso-R').style.display === ''
     && /desligada/.test(document.getElementById('simAviso-R').innerHTML),
     'a faixa de aviso diz que a regra de juros esta desligada');
  ok(/carry/.test(document.getElementById('simAviso-R').innerHTML),
     'e diz que o cambio continua lendo a Selic imposta -- a (F) esta no simulador');

  // ── 8g. a corrida solta contra o observado ──
  restaura();
  // De onde as CINCO conseguem partir: a (I) precisa de quatro trimestres observados
  // antes, para a media movel de servicos e industriais.
  ok(D.sim.i0_min >= 4, 'o payload declara de onde a conta solta pode partir',
     String(D.sim.i0_min));
  SIM.i0 = Math.max(EQ.est_i0, D.sim.i0_min);
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

  // ── 8i. o bloco 1 nao tem controle NENHUM ──
  // Duas rodadas de corte: os pesos sairam em 2026-09-22 (*"a simulacao vem dos
  // inputs"*) e a barra de desenho em 2026-09-24. O guarda e sobre a tela
  // RENDERIZADA e nao sobre o markup -- os controles nasciam de `innerHTML`, entao
  // um grep no arquivo entregue nao acharia nada.
  restaura();
  ok(!CRU.includes('id="simOpcoes"'),
     'a barra de opcoes do bloco 1 saiu do markup');
  // Pelo ID, e nao pelo nome: `_simFaixa` e a funcao que CALCULA a faixa e continua
  // existindo -- o que tem de sumir e o elemento que a desligava.
  ['simOpcoes', 'simFaixa', 'simChoque', 'simH', 'simI0', 'simT1', 'simT2', 'simT3',
   'simReset'].forEach((id) => {
    ok(!CRU.includes('id="' + id + '"'), 'nao ha elemento #' + id + ' no entregue');
  });
  ok(!/class="sim-chk"|class="sim-num"/.test(CRU),
     'e nem as classes dos controles cortados');
  // O bloco 1 e o que o cartao da equacao imprime: titulo, subtitulo, aviso e os
  // graficos. Nenhum deles pode trazer um campo para digitar.
  const bloco1 = D.sim.eq_ordem.map((k) =>
    document.getElementById('simEqSub-' + k).innerHTML
    + document.getElementById('simAviso-' + k).innerHTML
    + document.getElementById('simGrid-' + k).innerHTML).join('');
  ok(!/<input|<select/.test(bloco1),
     'o bloco 1 nao tem nenhum controle: ele so imprime');
  ok(/aba Juros/.test(document.getElementById('simEqSub-R').innerHTML),
     'e manda para a aba Juros quem quiser os pesos e a equacao');
  ok(/aba Câmbio/.test(document.getElementById('simEqSub-F').innerHTML),
     'e para a aba Cambio quem quiser os da equacao do cambio');
  ok(/aba Expectativas/.test(document.getElementById('simEqSub-E').innerHTML),
     'e para a aba Expectativas quem quiser os da terceira');
  ok(D.sim.eq_ordem.every((k) =>
       document.getElementById('simAviso-' + k).style.display === 'none'),
     'com as equacoes ligadas nao ha aviso nenhum');

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
  SIM.fonte.rr_10a = 'digitado';
  ctx.renderSim();
  const hDig = document.getElementById('simInputs').innerHTML;
  const caixasAnc = hDig.match(/<input[^>]*data-chave="rr_10a"[^>]*>/g) || [];
  const cobAnc = ctx._simCobertura('rr_10a', SIM.i0, SIM.h);
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

  // As tres formas NOMEIAM em vez de descrever -- pedido do usuario em 2026-09-24. A
  // descricao desceu para o `title` da opcao, que e onde a frase inteira cabe sem
  // alargar a caixa fechada do seletor; as duas pontas sao afirmadas porque cortar a
  // frase sem lhe dar outro lugar seria meio corte.
  ok(ctx.SIM_CHQ_TIPOS.map((t) => t.rot).join(' | ')
     === 'Choque permanente | Choque com decaimento | Choque constante + decaimento',
     'as tres formas de choque sao nomes, nao descricoes',
     ctx.SIM_CHQ_TIPOS.map((t) => t.rot).join(' | '));
  ok(ctx.SIM_CHQ_TIPOS.every((t) => t.desc && t.desc.length > 30),
     'e cada uma leva a descricao consigo, para o title da opcao');
  SIM.chqAberto.pi_e = true;
  ctx.renderSim();
  const painel = document.getElementById('simInputs').innerHTML;
  ctx.SIM_CHQ_TIPOS.forEach((t) => {
    ok(painel.indexOf('title="' + t.desc + '">' + t.rot + '</option>') >= 0,
       t.k + ': a opcao imprime o nome e carrega a descricao no title');
  });
  ok(!/, que<\/span>/.test(painel),
     'e a frase do painel nao rege mais o rotulo -- o "que" saiu com a descricao');
  SIM.chqAberto.pi_e = false;

  // O choque numa PECA move a conta de que ela participa e nao toca na irma. Com cada
  // peca virando cartao, o choque deixou de ter um parametro `pai` -- ele soma no
  // caminho daquele cartao e nada precisa ser recomposto.
  restaura();
  const rrAntes = SIM.cx.rr_10a.slice(0, 3);
  const metaAntes = SIM.cx.meta_12m.slice(0, 3);
  const ancAntes2 = SIM._ultimo.anc[0];
  SIM.chq.rr_10a = { tipo: 'const', v: 1.5, n: 12, rho: 0.8 };
  ctx.simAplicarChoque('rr_10a');
  ok(Math.abs(SIM.cx.rr_10a[0] - (rrAntes[0] + 1.5)) < 1e-9,
     'o choque entra no cartao escolhido',
     rrAntes[0].toFixed(3) + ' -> ' + SIM.cx.rr_10a[0].toFixed(3));
  ok(SIM.cx.meta_12m.slice(0, 3).every((v, i) => Math.abs(v - metaAntes[i]) < 1e-12),
     'e NAO toca na outra peca -- e isso que faz o cenario ser diferente');
  ok(Math.abs(SIM._ultimo.anc[0] - (ancAntes2 + 1.5)) < 1e-9,
     'a ancora e recomposta pela formula da equacao, nao chutada',
     ancAntes2.toFixed(3) + ' -> ' + SIM._ultimo.anc[0].toFixed(3));
  ok(SIM.fonte.rr_10a === 'digitado',
     'e a fonte do cartao chocado passa para Exogeno, senao o choque nao valeria');
  restaura();

  // O choque pula trimestre ja publicado: X "no primeiro trimestre" quer dizer o
  // primeiro que da para editar, senao ele se perde conforme o dado avanca.
  SIM.i0 = D.sim.rot.length - 2;
  SIM.h = 8;
  SIM.fonte.pi_e = 'digitado';
  ctx.renderSim();
  const cobDi = ctx._simCobertura('pi_e', SIM.i0, D.sim.h_max);
  const nPub = cobDi.filter(Boolean).length;
  ok(nPub > 0, 'este cenario tem trimestre publicado na janela', String(nPub));
  const diAntes = SIM.cx.pi_e.slice();
  SIM.chq.pi_e = { tipo: 'const', v: 1, n: 99, rho: 1 };
  ctx.simAplicarChoque('pi_e');
  ok(SIM.cx.pi_e.slice(0, nPub).every((v, i) => Math.abs(v - diAntes[i]) < 1e-12),
     'o trimestre ja publicado nao recebe choque nenhum');
  ok(Math.abs(SIM.cx.pi_e[nPub] - (diAntes[nPub] + 1)) < 1e-9,
     'e o choque comeca inteiro no primeiro trimestre editavel',
     diAntes[nPub].toFixed(3) + ' -> ' + SIM.cx.pi_e[nPub].toFixed(3));
  restaura();

  // ── 8k. a equacao NAO fica no simulador ──
  // Pedido do usuario: "deixa a equacao somente nas abas individuais". A aba de
  // Juros continua com ela, e e para la que o subtitulo do bloco 1 aponta.
  ok(document.getElementById('tayMathSimb').innerHTML.indexOf('∑') >= 0,
     'a equacao de juros continua escrita na aba dela');
  ok(/aba Juros/.test(document.getElementById('simEqSub-R').innerHTML),
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

  // ── 8m. a SEGUNDA equacao: o cambio ──
  // Pedido do usuario em 2026-09-24: *"rode os sistema com as duas equacoes: Taylor e
  // Cambio"*. O que este bloco guarda nao e "a (F) existe" -- e que ela esta LIGADA na
  // (R), porque o unico elo entre as duas e um canal fraco e uma ligacao que se
  // desfaz em silencio produz uma tela plausivel e errada.
  secao('8m. O cambio, a segunda equacao do simulador');
  restaura();
  ctx.renderSim();

  ok(D.sim.eq_ordem.join(',') === 'H,I,E,R,F',
     'ha cinco equacoes, e a ORDEM e de solucao dentro do trimestre: a (H) le a Selic '
     + 'do trimestre anterior, a (I) le o hiato, a (E) a inflacao, a (R) a expectativa '
     + 'e a (F) a Selic e a inflacao',
     D.sim.eq_ordem.join(' -> '));
  // Todo item de `eq_ordem` tem de ter cartao no markup. E o que substitui gerar os
  // cartoes em JS: a terceira equacao nao entra em silencio.
  ok(D.sim.eq_ordem.every((k) => CRU.includes('id="simGrid-' + k + '"')),
     'e cada uma tem o seu cartao no markup -- nenhuma equacao sem lugar na tela');

  const EQF = D.sim.eq.F;
  ok(EQF.explica === 'de' && D.sim.var.de.produzida_por === 'F'
     && D.sim.var.de.produtor_no_sim === true,
     'a (F) explica a variacao do cambio, e ela consta como endogena NESTA rodada');
  ok(EQF.consome.indexOf('carry_vol') < 0
     && EQF.consome.indexOf('ffr') >= 0 && EQF.consome.indexOf('vol') >= 0,
     'o carry nao e input: quem tem cartao sao as pecas dele (Fed Funds e vol)',
     EQF.consome.join(','));
  ok(EQF.canais.indexOf('carry_vol') >= 0 && EQF.carry.juro === 'selic',
     'mas ele E canal da equacao, e o juro dele e a Selic do simulador');
  ok(EQF.consome.every((c) => !!D.sim.var[c]),
     'e tudo o que ela consome tem cartao no bloco 2');

  // O elo, medido: 2 p.p. de Selic a mais tem de MOVER o cambio, e para baixo.
  const entF = ctx.simEntradas();
  const selBase = ctx._simCaminhoSelic(SIM.coef.R, SIM.i0, SIM.h, entF);
  const deBase = ctx._simCaminhoDe(SIM.coef.F, SIM.i0, SIM.h, entF, selBase);
  const deAlta = ctx._simCaminhoDe(SIM.coef.F, SIM.i0, SIM.h, entF,
                                   selBase.map((v) => v + 2));
  const somaB = deBase.reduce((a, b) => a + b, 0);
  const somaA = deAlta.reduce((a, b) => a + b, 0);
  ok(Math.abs(somaA - somaB) > 1e-6,
     'a Selic CHEGA ao cambio: subi-la 2 p.p. muda o caminho do cambio',
     (somaA - somaB).toFixed(4) + ' p.p. no acumulado');
  ok(somaA < somaB,
     'e na direcao certa: juro mais alto, real mais forte',
     somaA.toFixed(3) + ' contra ' + somaB.toFixed(3));
  // E a contrapartida da especificacao em DIFERENCA, que precisa estar afirmada
  // porque ela e contraintuitiva: um juro que sobe e depois volta nao deixa efeito.
  const selDeg = selBase.slice();
  selDeg[0] += 2;
  const deDeg = ctx._simCaminhoDe(SIM.coef.F, SIM.i0, SIM.h, entF, selDeg);
  ok(Math.abs(deDeg.reduce((a, b) => a + b, 0) - somaB) < 1e-9,
     'mas um juro que sobe SO num trimestre e volta nao deixa efeito no nivel: '
     + 'o canal le a variacao do carry, nao o nivel dele');
  ok(deDeg[0] < deBase[0],
     'e ainda assim ele move o trimestre em que aconteceu',
     deDeg[0].toFixed(3) + ' contra ' + deBase[0].toFixed(3));

  // A ancora do primeiro trimestre: sem o nivel do trimestre anterior, a primeira
  // variacao de um canal seria o PROPRIO nivel -- num CDS de 125 pontos, um choque
  // de 125 pontos-base saido do nada.
  ok(EQF.canais.every((c) => EQF.nivel[c] && EQF.nivel[c][SIM.i0 - 1] != null),
     'todo canal traz o nivel do trimestre anterior a janela, que e a ancora dele');
  ok(Math.abs(deBase[0]) < 20,
     'e por isso a primeira variacao e de tamanho de variacao, nao de nivel',
     deBase[0].toFixed(3) + ' %');

  // O nivel e a inversa exata da variacao -- as duas sao o MESMO caminho, e e por
  // isso que o grafico pode desenhar uma e as caixas a outra.
  const niv = ctx._simNivelCambio(SIM.i0, deBase);
  const p0 = EQF.ptax[SIM.i0 - 1];
  ok(Math.abs(niv[0] - p0 * Math.exp(deBase[0] / 100)) < 1e-9,
     'o nivel parte do ultimo fechamento observado');
  ok(Math.abs(100 * Math.log(niv[niv.length - 1] / p0) - somaB) < 1e-6,
     'e o acumulado do nivel devolve a soma das variacoes, exatamente');

  // A faixa: ela existe, ela cresce, e ela CONTEM a mediana.
  ok(SIM._ultimo.fx && SIM._ultimo.fx.faixa,
     'a faixa do cambio existe com a equacao ligada');
  const fFx = SIM._ultimo.fx.faixa;
  ok(fFx.hi.every((v, i) => v >= SIM._ultimo.fx.nivel[i] - 1e-6)
     && fFx.lo.every((v, i) => v <= SIM._ultimo.fx.nivel[i] + 1e-6),
     'e ela contem o caminho da mediana em todo trimestre');
  ok((fFx.hi[fFx.hi.length - 1] - fFx.lo[fFx.lo.length - 1])
       > (fFx.hi[0] - fFx.lo[0]),
     'e cresce com o horizonte -- e incerteza passando pela dinamica, nao margem',
     (fFx.hi[0] - fFx.lo[0]).toFixed(3) + ' -> '
       + (fFx.hi[fFx.hi.length - 1] - fFx.lo[fFx.lo.length - 1]).toFixed(3));
  ok(SIM._ultimo.fx.duasFaixas === true && SIM._ultimo.fx.nEq === 5,
     'com as CINCO ligadas a faixa do cambio carrega a incerteza das cinco -- o laco '
     + 'leva a de cada uma a todas', String(SIM._ultimo.fx.nEq));
  // E a legenda CONTA, em vez de repetir um numero escrito a mao: "das duas equacoes"
  // passou a mentir no dia em que a terceira entrou.
  const nomeFx = ctx._tracesSimFx(SIM._ultimo)
    .map((t) => t.name || '').filter((n2) => /^Faixa de/.test(n2))[0];
  ok(/das cinco equações/.test(nomeFx), 'e a legenda diz de quantas ela e', nomeFx);

  // Impor a Selic tira a (R) de dentro da faixa do cambio -- mas a inflacao continua
  // chegando da curva de Phillips, e com ela a (H) e a (E): quatro.
  SIM.fonte.selic = 'digitado';
  SIM.cx.selic = ctx.simObs('selic', SIM.i0, D.sim.h_max).map((v) => v);
  ctx.renderSim();
  ok(SIM._ultimo.fx.faixa && SIM._ultimo.fx.nEq === 4,
     'com a Selic imposta a faixa do cambio perde a (R) e fica com quatro',
     String(SIM._ultimo.fx.nEq));
  // E impondo tambem a inflacao, o que sobra e so a (F): nada mais a alimenta.
  SIM.fonte.infl_br = 'digitado';
  SIM.cx.infl_br = ctx.simObs('infl_br', SIM.i0, D.sim.h_max).map((v) => v);
  ctx.renderSim();
  ok(SIM._ultimo.fx.faixa && SIM._ultimo.fx.duasFaixas === false
     && SIM._ultimo.fx.nEq === 1,
     'com a Selic e a inflacao impostas a faixa do cambio fica, e passa a ser so a da (F)');
  ok(!/equações/.test(ctx._tracesSimFx(SIM._ultimo)
       .map((t) => t.name || '').filter((n2) => /^Faixa de/.test(n2))[0]),
     'e a legenda para de citar mais de uma');

  // Impor o cambio desliga a (F), e o aviso do cartao DELA tem de dizer isso.
  restaura();
  SIM.fonte.de = 'observado';
  ctx.renderSim();
  ok(SIM._ultimo.fx.faixa === null,
     'com o cambio imposto nao ha faixa: nao ha equacao rodando');
  ok(document.getElementById('simAviso-F').style.display === ''
     && /desligada/.test(document.getElementById('simAviso-F').innerHTML),
     'e o aviso aparece no cartao da (F), nao no da (R)');
  ok(document.getElementById('simAviso-R').style.display === 'none',
     'o cartao da (R) segue sem aviso: a equacao dela continua ligada');

  // ── as DUAS PONTAS da mesma recursao ──
  // `simulator._sim_fx` (Python) e `_simCaminhoDe` (JS) sao a mesma conta escrita duas
  // vezes. Duas implementacoes divergem em silencio -- um `sd` trocado, um log
  // esquecido, um sinal invertido continuam produzindo um caminho plausivel --, entao
  // o payload traz o ajuste de UM PASSO calculado do lado do Python e o teste exige
  // que o JS devolva os mesmos numeros. Um passo porque ali todas as defasagens vem
  // do observado, o que torna a comparacao exata em vez de aproximada.
  restaura();
  const canaisF = EQF.canais.filter((c) => c !== EQF.carry.canal);
  let nPar = 0, piorPar = 0;
  EQF.ajuste.forEach((alvo, i) => {
    if (alvo == null || i < 1) return;
    const e1 = { infl_br: ctx.simObs('infl_br', i, 1),
                 infl_us: ctx.simObs('infl_us', i, 1),
                 ffr: ctx.simObs('ffr', i, 1), vol: ctx.simObs('vol', i, 1) };
    canaisF.forEach((c) => { e1[c] = ctx.simObs(c, i, 1); });
    const got = ctx._simCaminhoDe(SIM.coef.F, i, 1, e1, ctx.simObs('selic', i, 1))[0];
    piorPar = Math.max(piorPar, Math.abs(got - alvo));
    nPar += 1;
  });
  ok(nPar > 60, 'ha trimestres bastantes para comparar as duas pontas', String(nPar));
  ok(piorPar < 1e-5,
     'e o JS reproduz o ajuste que o Python calculou, trimestre a trimestre',
     'pior diferenca ' + piorPar.toExponential(2) + ' p.p.');
  // E o gabarito tem de ser um ajuste de VERDADE, senao a asserção acima passaria
  // comparando duas contas erradas iguais.
  const errF = EQF.ajuste
    .map((v, i) => (v == null || EQF.y[i] == null) ? null : v - EQF.y[i])
    .filter((v) => v != null);
  const rmseF = Math.sqrt(errF.reduce((a2, b2) => a2 + b2 * b2, 0) / errF.length);
  ok(rmseF > 0.5 && rmseF < 6,
     'e esse ajuste explica o cambio de verdade -- o erro esta na ordem do estimado',
     'RMSE ' + rmseF.toFixed(3) + ' p.p./tri');

  // ── 8n. o cartao do cambio fala em NIVEL, a equacao em variacao ──
  // Pedido do usuario em 2026-09-24: *"conseguimos trabalhar com ela no simulador (nos
  // boxes) em nivel?"*. A conversao e uma bijecao ancorada no ultimo fechamento
  // observado, entao nada se perde -- mas duas unidades para a mesma serie e
  // exatamente o tipo de coisa que passa a divergir sem nada avisar.
  secao('8n. O cambio: caixa em nivel, equacao em variacao');
  restaura();
  ctx.renderSim();

  const VDE = D.sim.var.de;
  ok(/reais/.test(VDE.unidade) && VDE.em_nivel_de_variacao === true
     && VDE.unidade_eq === '% no trimestre',
     'o cartao declara as DUAS unidades: a da caixa e a da equacao',
     VDE.unidade + ' / ' + VDE.unidade_eq);
  ok(VDE.obs.every((v, i) => v === EQF.ptax[i]),
     'e a serie observada do cartao e o NIVEL, a mesma que o grafico desenha');

  // A bijecao, nos dois sentidos, sobre o caminho que esta na tela.
  const voltou = ctx._simVarDeNivel(SIM.i0, SIM._ultimo.fx.nivel);
  ok(voltou.every((v, i) => Math.abs(v - SIM._ultimo.fx.cam[i]) < 1e-9),
     'nivel -> variacao desfaz variacao -> nivel, exatamente',
     'pior ' + Math.max(...voltou.map((v, i) =>
       Math.abs(v - SIM._ultimo.fx.cam[i]))).toExponential(2));

  // Em Endogeno a caixa mostra o que a equacao produziu, no MESMO numero do grafico.
  ok(SIM._ultimo.produzido.de
     && SIM._ultimo.produzido.de.every((v, i) =>
          Math.abs(v - SIM._ultimo.fx.nivel[i]) < 1e-12),
     'em Endogeno a caixa mostra o nivel que a equacao produziu, nao a variacao');
  const htmlDe = document.getElementById('simInputs').innerHTML;
  ok(/no trimestre"/.test(htmlDe),
     'e o hover da caixa continua trazendo a variacao -- ela nao sumiu com a troca');

  // Digitar em NIVEL move a conta: o caminho digitado vira variacao e volta igual.
  restaura();
  SIM.fonte.de = 'digitado';
  const base0 = ctx.simObs('de', SIM.i0, D.sim.h_max);
  SIM.cx.de = base0.map((v, i) => v + 0.5 * (i + 1) / base0.length);
  ctx.renderSim();
  ok(SIM._ultimo.fx.nivel.every((v, i) => Math.abs(v - SIM.cx.de[i]) < 1e-12),
     'digitando em nivel, o grafico desenha exatamente o que foi digitado');
  const impl = ctx._simVarDeNivel(SIM.i0, SIM.cx.de.slice(0, SIM.h));
  ok(SIM._ultimo.fx.cam.every((v, i) => Math.abs(v - impl[i]) < 1e-9),
     'e a variacao que a conta consome e a implicita naquele caminho');
  ok(SIM._ultimo.fx.faixa === null,
     'e a equacao fica desligada, como em qualquer variavel imposta');

  // "Observado" em nivel quer dizer cambio PARADO depois do ultimo dado -- e nao o
  // nivel derivando na taxa do ultimo trimestre, que e o que segurar a VARIACAO daria.
  restaura();
  SIM.fonte.de = 'observado';
  ctx.renderSim();
  const nObs = SIM._ultimo.fx.nivel;
  ok(nObs.every((v) => Math.abs(v - nObs[nObs.length - 1]) < 1e-9),
     'em Observado, passado o ultimo dado o cambio fica PARADO no ultimo fechamento',
     nObs[0].toFixed(4) + ' .. ' + nObs[nObs.length - 1].toFixed(4));
  ok(SIM._ultimo.fx.cam.every((v) => Math.abs(v) < 1e-9),
     'o que em variacao quer dizer zero -- e nao a taxa do ultimo trimestre repetida');

  // O passo e o choque padrao acompanham a unidade: `1` fixo virava +1 real.
  restaura();
  ok(VDE.passo <= 0.1, 'o passo da caixa e de nivel de cambio, nao de ponto percentual',
     String(VDE.passo));
  ok(SIM.chq.de.v <= 0.5 && SIM.chq.de.v > 0,
     'e o choque padrao escala com ele em vez de ser +1 real (19% de uma vez)',
     String(SIM.chq.de.v));
  ok(SIM.chq.fiscal.v >= 10,
     'a mesma regra faz o choque do CDS nascer em dezenas de pontos-base, nao em 1',
     String(SIM.chq.fiscal.v));

  restaura();
  ctx.renderSim();

  // ── 8o. o que MOVE a projecao, e por que os canais parados nao movem ──
  // O usuario perguntou de onde vinha a desvalorizacao com todas as caixas paradas
  // (2026-09-24). A resposta e forte o bastante para estar na tela: a equacao le a
  // VARIACAO de cada canal, entao canal parado contribui exatamente zero, e o que
  // sobra e o diferencial de inflacao com peso imposto em 1.
  secao('8o. De onde vem a projecao do cambio');
  restaura();
  ctx.renderSim();
  const ac = SIM._ultimo.fx.acum;
  ok(!!ac, 'a rodada recolhe a contribuicao de cada termo');
  const somaAc = Object.keys(ac).reduce((t, k2) => t + ac[k2], 0);
  ok(Math.abs(somaAc - SIM._ultimo.fx.total) < 1e-9,
     'e as partes somam EXATAMENTE o caminho -- e a mesma recursao, nao uma segunda',
     somaAc.toFixed(6) + ' contra ' + SIM._ultimo.fx.total.toFixed(6));

  const naoCarry = EQF.canais.filter((c) => c !== EQF.carry.canal);
  ok(naoCarry.every((c) => Math.abs(ac[c]) < 1e-9),
     'com as premissas paradas, os canais de mercado contribuem exatamente zero',
     naoCarry.map((c) => c + ' ' + ac[c].toFixed(6)).join(' · '));
  ok(Math.abs(ac.carry_vol) > 1e-6,
     'e o carry NAO -- ele se mexe porque a Selic se mexe',
     ac.carry_vol.toFixed(4) + ' p.p.');
  // Com a curva de Phillips ligada o diferencial deixa de ser premissa parada: a inflacao
  // daqui vem da equacao, e a parte dele no caminho e um numero do cenario, que a ficha
  // imprime (hoje 55%). A afirmacao de que ele e QUASE TUDO vale onde ela sempre valeu:
  // com as duas inflacoes seguradas.
  const fracCom = ac[EQF.offset] / SIM._ultimo.fx.total;
  ok(fracCom > 0.2 && fracCom < 1,
     'com a (I) ligada o diferencial continua sendo a maior parte, sem ser tudo',
     Math.round(100 * fracCom) + '%');
  SIM.fonte.infl_br = 'observado';
  ctx.renderSim();
  ok(SIM._ultimo.fx.acum[EQF.offset] / SIM._ultimo.fx.total > 0.8,
     'e com a inflacao segurada a projecao e quase toda o diferencial, com peso imposto '
     + 'em 1', Math.round(100 * SIM._ultimo.fx.acum[EQF.offset] / SIM._ultimo.fx.total) + '%');
  restaura();
  ctx.renderSim();
  ok(SIM._ultimo.fx.parados === naoCarry.length,
     'e a tela conta quantos canais estao parados, em vez de o leitor descobrir',
     String(SIM._ultimo.fx.parados));

  // Mexer num canal parado o faz aparecer -- que e o que a frase da ficha promete.
  SIM.fonte.fiscal = 'digitado';
  SIM.cx.fiscal = ctx.simObs('fiscal', SIM.i0, D.sim.h_max).map((v, i) => v + 20 * (i + 1));
  ctx.renderSim();
  ok(Math.abs(SIM._ultimo.fx.acum.fiscal) > 0.1,
     'mexer no CDS o tira do zero, como a ficha diz que acontece',
     SIM._ultimo.fx.acum.fiscal.toFixed(3) + ' p.p.');
  ok(SIM._ultimo.fx.acum.fiscal > 0,
     'e na direcao certa: risco maior, real mais fraco');
  ok(SIM._ultimo.fx.parados === naoCarry.length - 1,
     'e a contagem de parados cai junto', String(SIM._ultimo.fx.parados));

  // A ficha imprime esses numeros, e e por ali que o leitor os alcanca.
  const fichaF = document.getElementById('simEqSub-F').innerHTML;
  ok(/diferencial de inflação/.test(fichaF) && /exatamente zero/.test(fichaF),
     'e a ficha da equacao diz as duas coisas na tela');
  ok(/\d+% disso/.test(fichaF),
     'com o numero derivado do cenario, nao escrito a mao');

  restaura();
  ctx.renderSim();

  // ── 8p. segurar a MEDIA, e so onde a variavel e taxa de fluxo ──
  // Pedido do usuario em 2026-09-24: *"pode colocar a media dos ultimos 4
  // trimestres"*. A regra da casa (segure o ultimo valor) continua valendo em todo
  // cartao de NIVEL; a excecao e declarada por variavel. Um `segura` que vazasse para
  // um cartao de nivel produziria um CDS projetado na media de quatro trimestres --
  // plausivel, errado, e sem sintoma.
  secao('8p. Segurar a media: so nas taxas de fluxo');
  restaura();
  ctx.renderSim();

  // Com o `ppp` deixando de ser cartao, as taxas de fluxo do painel sao duas -- e as
  // duas continuam sendo as unicas que seguram media.
  const FLUXO = ['infl_br', 'infl_us'];
  FLUXO.forEach((k2) => {
    const alvo = D.sim.var[k2];
    ok(alvo && alvo.segura && alvo.segura.modo === 'media' && alvo.segura.k === 4,
       k2 + ': segura a media de 4 trimestres, porque e taxa de fluxo',
       JSON.stringify(alvo && alvo.segura));
  });
  const nivelSemMedia = D.sim.var_ordem
    .filter((k2) => FLUXO.indexOf(k2) < 0 && D.sim.var[k2].segura);
  ok(nivelSemMedia.length === 0,
     'e NENHUM cartao de nivel segura media -- ali o ultimo valor e a leitura certa',
     nivelSemMedia.join(',') || '(nenhum)');

  // A media morde: ela tem de diferir do ultimo valor, senao a asserção nao separa
  // nada. Medido, a leitura isolada e ~2,5x a media de quatro.
  const serPpp = ctx._simDerivObs('F', 'ppp');
  const obsPpp = serPpp.filter((v) => v != null);
  const ultPpp = obsPpp[obsPpp.length - 1];
  const medPpp = ctx._simMediaFinal(obsPpp, 4);
  ok(Math.abs(ultPpp - medPpp) > 0.1,
     'a media difere da ultima leitura -- a regra esta decidindo alguma coisa',
     'ultimo ' + ultPpp.toFixed(4) + ' contra media ' + medPpp.toFixed(4));
  // O caminho que a (F) consome sai das DUAS metades seguradas, cada uma na media
  // dela. E o que a asserção seguinte mede: a media e linear, entao segurar as duas e
  // subtrair devolve a media da diferenca. Era o teste do "abrir em partes"; com as
  // partes virando cartao, a propriedade continua e a mecanica some.
  const entPpp = ctx.simEntradas();
  const camPpp = ctx._simDerivadas('F', entPpp, SIM.i0, SIM.h).ppp;
  // A tolerancia e 1e-5 e nao zero: as series sao arredondadas a seis casas no
  // payload, cada uma por si. O que se afirma e a linearidade, nao o arredondamento.
  ok(camPpp.every((v) => Math.abs(v - medPpp) < 1e-5),
     'todo trimestre projetado usa a media das duas metades, nao a ultima leitura',
     camPpp[0].toFixed(6) + ' contra ' + medPpp.toFixed(6));

  // Dentro do dado nada muda: a media so vale DEPOIS do ultimo publicado.
  const dentro = ctx.simObs('infl_br', 1, 8);
  ok(dentro.every((v, i) => Math.abs(v - D.sim.var.infl_br.obs[1 + i]) < 1e-12),
     'dentro da amostra a serie continua sendo o dado, e nao a media');

  // O que a caixa dourada DIZ tem de acompanhar a regra, senao ela mente numa das duas.
  const htmlSeg = document.getElementById('simInputs').innerHTML;
  ok(/média dos últimos 4 trimestres publicados/.test(htmlSeg),
     'a caixa da taxa de fluxo diz que o numero e a media');
  ok(/último valor conhecido, repetido/.test(htmlSeg),
     'e a caixa de nivel continua dizendo que e o ultimo valor repetido');
  const subF = document.getElementById('simEqSub-F').innerHTML;
  ok(/segurada na média dos últimos/.test(subF) && !/segurad[oa] em a/.test(subF),
     'e a ficha usa o complemento regido certo, nao "segurado em a media"');
  ok(/vindo da curva de Phillips/.test(subF),
     'e diz que a inflacao daqui nao esta segurada: ela vem da curva de Phillips');

  restaura();
  ctx.renderSim();

  // ── 8q. a TERCEIRA equacao: as expectativas ──
  // Pedido do usuario em 2026-09-25: *"Vamos introduzir a equacao de expectativas"*.
  // Ela e a primeira da ordem de solucao, e o que este bloco guarda nao e "a (E)
  // existe" -- e que ela esta LIGADA na (R), porque uma corrente que se desfaz em
  // silencio produz uma tela plausivel e errada.
  secao('8q. As expectativas, a terceira equacao do simulador');
  restaura();
  ctx.renderSim();

  ok(EQE.explica === 'pi_e' && D.sim.var.pi_e.produtor_no_sim === true,
     'a (E) explica a expectativa, e ela consta como endogena NESTA rodada');
  ok(EQE.consome.join(',') === 'infl_br,meta_12m',
     'ela consome a inflacao do trimestre e a meta -- e so isso tem cartao',
     EQE.consome.join(','));
  ok(EQE.consome.indexOf('i12') < 0 && !D.sim.var.i12,
     'o IPCA de 12 meses NAO e cartao: ele e conta, composta de quatro trimestres');

  // A restricao, conferida no caminho SIMULADO: com a inflacao na meta a expectativa
  // volta para a meta e fica ali. E a propriedade que justifica a soma-um, e num
  // simulador ela vale por conjunto de pesos, nao so na mediana.
  // O cartao de inflacao esta em 100*dlog e NAO em variacao simples: para que o
  // acumulado de doze meses de exatamente a meta, cada trimestre tem de ser
  // `ln(1 + meta/100)/4` e nao `(1+meta/100)^(1/4) - 1`. As duas diferem 0,004 p.p.
  // por trimestre, o que a conta amplifica para 0,006 p.p. na expectativa de repouso
  // -- pequeno, sistematico, e exatamente o tipo de troca que passa despercebida.
  const META_T = 3.5, INF_T = 100 * Math.log(1 + META_T / 100) / 4;
  const entE = { infl_br: new Array(400).fill(INF_T),
                 meta_12m: new Array(400).fill(META_T) };
  const camLongo = ctx._simCaminhoPiE(SIM.coef.E, SIM.i0, 400, entE);
  ok(Math.abs(camLongo[camLongo.length - 1] - META_T) < 1e-6,
     'com a inflacao na meta a expectativa converge EXATAMENTE para a meta',
     camLongo[camLongo.length - 1].toFixed(8) + ' contra ' + META_T);
  // E ela vale desenho a desenho, porque o peso da meta nao e amostrado: ele e
  // `1 - e1 - e2`. Usar o desenho gravado de `peso_meta` pareceria equivalente e nao e.
  let piorRep = 0;
  for (let sdr = 0; sdr < EQE.n_draws; sdr += 97) {
    const cD = { e1: EQE.draws.e1[sdr], e2: EQE.draws.e2[sdr] };
    const cc = ctx._simCaminhoPiE(cD, SIM.i0, 400, entE);
    piorRep = Math.max(piorRep, Math.abs(cc[cc.length - 1] - META_T));
  }
  ok(piorRep < 1e-6,
     'e isso vale em TODO desenho do posterior, nao so na mediana',
     'pior desvio ' + piorRep.toExponential(2) + ' p.p.');
  ok(EQE.draws.peso_meta.every((v, i) =>
       Math.abs(v - (1 - EQE.draws.e1[i] - EQE.draws.e2[i])) < 1e-4),
     'o peso da meta gravado bate com `1 - e1 - e2` em todo desenho');

  // Uma inflacao permanentemente acima da meta e incorporada em parte, e o quanto e o
  // repasse de longo prazo que a aba publica.
  const ACIMA = 1.0;
  const infAlta = 100 * Math.log(1 + (META_T + ACIMA) / 100) / 4;
  const entE2 = { infl_br: new Array(400).fill(infAlta),
                  meta_12m: new Array(400).fill(META_T) };
  const camAlto = ctx._simCaminhoPiE(SIM.coef.E, SIM.i0, 400, entE2);
  const repasse = (camAlto[camAlto.length - 1] - META_T) / ACIMA;
  ok(Math.abs(repasse - D.exp.repasse) < 0.02,
     'e uma inflacao permanente 1 p.p. acima e incorporada no repasse que a aba mede',
     repasse.toFixed(4) + ' contra ' + D.exp.repasse.toFixed(4));
  ok(repasse > 0.05 && repasse < 0.95,
     'nem ancora perfeita (0) nem expectativa puramente adaptativa (1)',
     repasse.toFixed(3));

  // O IPCA de 12 meses e COMPOSTO, e nao a soma das quatro variacoes. A diferenca e
  // pequena e sistematica, entao trocar uma pela outra passa despercebido -- e e por
  // isso que ela e afirmada.
  const q4 = [1.0, 1.2, 0.8, 1.1];
  const comp = ctx._simAcumLog(q4, 3, 4);
  ok(Math.abs(comp - 100 * (Math.exp(4.1 / 100) - 1)) < 1e-12,
     'a composicao e exp(soma dos logs), nao a soma das variacoes',
     comp.toFixed(6) + ' contra soma simples 4,100000');
  // E ela reproduz o IPCA de 12 meses que o painel publica -- o gabarito que impede
  // o painel de precisar de um segundo cartao de IPCA.
  let nI12 = 0, piorI12 = 0;
  EQE.i12_obs.forEach((v, i) => {
    const pub = EQE.i12_pub[i];
    if (v == null || pub == null) return;
    piorI12 = Math.max(piorI12, Math.abs(v - pub));
    nI12 += 1;
  });
  ok(nI12 > 60, 'ha trimestres bastantes para conferir a composicao', String(nI12));
  ok(piorI12 < 0.02,
     'e o composto bate com o IPCA de 12 meses PUBLICADO -- e por isso que o painel '
     + 'tem UM cartao de IPCA e nao dois',
     'pior diferenca ' + piorI12.toFixed(4) + ' p.p. em ' + nI12 + ' trimestres');
  // E a forma errada tem de errar de VERDADE, senao a asserção acima nao separa nada:
  // somar as quatro variacoes em vez de compor erra uma ordem de grandeza a mais.
  let piorSoma = 0;
  EQE.i12_obs.forEach((v, i) => {
    const pub = EQE.i12_pub[i];
    if (v == null || pub == null || i < 3) return;
    const soma = EQE.obs_insumo.infl_br.slice(i - 3, i + 1)
      .reduce((a, b) => (a == null || b == null) ? null : a + b, 0);
    if (soma == null) return;
    piorSoma = Math.max(piorSoma, Math.abs(soma - pub));
  });
  ok(piorSoma > 10 * piorI12,
     'somar as quatro variacoes em vez de compor erra muito mais',
     piorSoma.toFixed(4) + ' contra ' + piorI12.toFixed(4) + ' p.p.');

  // O elo (E) -> (R): mexer na expectativa tem de mover a Selic, e para cima.
  restaura();
  const selBaseE = SIM._ultimo.cam[SIM.h - 1];
  ok(SIM._ultimo.eloE != null,
     'a rodada mede o elo entre a (E) e a (R) em vez de afirma-lo',
     String(SIM._ultimo.eloE));
  SIM.fonte.infl_br = 'digitado';
  SIM.cx.infl_br = ctx.simObs('infl_br', SIM.i0, D.sim.h_max).map((v) => v + 1);
  ctx.renderSim();
  ok(SIM._ultimo.exp.cam[SIM.h - 1] > SIM._ultimo.exp.cam[0],
     'mais inflacao em cada trimestre empurra a expectativa para cima ao longo do '
     + 'horizonte');
  ok(SIM._ultimo.cam[SIM.h - 1] > selBaseE,
     'e a Selic sobe junto -- a corrente (E) -> (R) esta ligada',
     selBaseE.toFixed(3) + ' -> ' + SIM._ultimo.cam[SIM.h - 1].toFixed(3));
  // E o cambio se mexe por tras disso, pelo carry: a corrente tem tres elos.
  restaura();
  const nivBaseE = SIM._ultimo.fx.nivel[SIM.h - 1];
  SIM.fonte.infl_br = 'digitado';
  SIM.cx.infl_br = ctx.simObs('infl_br', SIM.i0, D.sim.h_max).map((v) => v + 1);
  ctx.renderSim();
  ok(Math.abs(SIM._ultimo.fx.nivel[SIM.h - 1] - nivBaseE) > 1e-6,
     'e o cambio muda junto: (E) -> (R) -> (F) fecha a corrente',
     nivBaseE.toFixed(4) + ' -> ' + SIM._ultimo.fx.nivel[SIM.h - 1].toFixed(4));
  restaura();

  // Impor a expectativa desliga a (E), e o aviso tem de aparecer no cartao DELA.
  SIM.fonte.pi_e = 'observado';
  ctx.renderSim();
  ok(SIM._ultimo.exp.faixa === null,
     'com a expectativa imposta nao ha faixa: nao ha equacao rodando');
  ok(document.getElementById('simAviso-E').style.display === ''
     && /desligada/.test(document.getElementById('simAviso-E').innerHTML),
     'e o aviso aparece no cartao da (E)');
  ok(/distância até a meta/.test(document.getElementById('simAviso-E').innerHTML),
     'dizendo que a regra de juros continua lendo a expectativa imposta');
  ok(document.getElementById('simAviso-R').style.display === 'none'
     && document.getElementById('simAviso-F').style.display === 'none',
     'e os cartoes das outras duas seguem sem aviso');
  restaura();

  // A faixa da (R) passa a carregar a incerteza das DUAS quando a (E) esta ligada.
  ctx.renderSim();
  ok(SIM._ultimo.duasFaixasR === true,
     'com a (E) ligada a faixa da Selic carrega a incerteza das duas equacoes');
  // **A comparacao tem de ser com o MESMO caminho central.** Comparar com a rodada em
  // que a expectativa e imposta compara duas coisas ao mesmo tempo -- e medido, la a
  // faixa sai MAIS LARGA (1,77 contra 1,37), porque segurar a Focus no ultimo valor
  // mantem um desvio grande e constante, e e o desvio que a incerteza de `t3`
  // multiplica. O que isola a propagacao e trocar so os desenhos, com o caminho da
  // mediana fixo dos dois lados.
  // Pelo sistema: as mesmas mil rodadas do laco, trocando os desenhos SO da (R) contra
  // trocando os da (R) e da (E). O caminho da mediana e o mesmo nos dois lados.
  const entB = ctx.simEntradas(), ligaB = ctx._simLiga();
  const fSo = ctx._simFaixasSistema(SIM.i0, SIM.h, entB, ligaB, { R: true }).selic;
  const fCom = ctx._simFaixasSistema(SIM.i0, SIM.h, entB, ligaB, { R: true, E: true }).selic;
  const lSo = fSo.hi[SIM.h - 1] - fSo.lo[SIM.h - 1];
  const lCom = fCom.hi[SIM.h - 1] - fCom.lo[SIM.h - 1];
  ok(lCom > lSo,
     'no mesmo cenario, propagar os desenhos da (E) ALARGA a faixa da Selic',
     lSo.toFixed(4) + ' -> ' + lCom.toFixed(4));
  // Trimestre a trimestre ela nao CONTEM a outra, e isso e amostragem e nao defeito:
  // sao 1000 desenhos de cada lado, e onde a contribuicao da (E) ainda e pequena o
  // ruido do quantil inverte a ordem. O que se afirma e a largura, com a folga do
  // proprio ruido medida em vez de escolhida.
  let piorEstreita = 0;
  for (let i = 0; i < SIM.h; i++) {
    piorEstreita = Math.max(piorEstreita,
      (fSo.hi[i] - fSo.lo[i]) - (fCom.hi[i] - fCom.lo[i]));
  }
  ok(piorEstreita < 0.02,
     'e em nenhum trimestre ela fica mais estreita alem do ruido do quantil',
     'pior ' + piorEstreita.toFixed(4) + ' p.p. contra uma largura de '
       + lCom.toFixed(3));
  SIM.fonte.pi_e = 'observado';
  ctx.renderSim();
  ok(SIM._ultimo.duasFaixasR === false,
     'com a expectativa imposta ela volta a ser so a da (R)');
  restaura();

  // ── as DUAS PONTAS da recursao da (E) ──
  // Mesma razao do gabarito da (F): a conta esta escrita duas vezes, e duas
  // implementacoes divergem em silencio. Aqui o risco e maior, porque a composicao de
  // quatro trimestres e nova e um `k` trocado continua produzindo caminho plausivel.
  let nParE = 0, piorParE = 0;
  EQE.ajuste.forEach((alvo, i) => {
    if (alvo == null || i < 1) return;
    const e1 = { infl_br: ctx.simObs('infl_br', i, 1),
                 meta_12m: ctx.simObs('meta_12m', i, 1) };
    const got = ctx._simCaminhoPiE(EQE.mediana, i, 1, e1)[0];
    piorParE = Math.max(piorParE, Math.abs(got - alvo));
    nParE += 1;
  });
  ok(nParE > 60, 'ha trimestres bastantes para comparar as duas pontas da (E)',
     String(nParE));
  ok(piorParE < 1e-5,
     'e o JS reproduz o ajuste que o Python calculou, trimestre a trimestre',
     'pior diferenca ' + piorParE.toExponential(2) + ' p.p.');
  const errE = EQE.ajuste
    .map((v, i) => (v == null || EQE.y[i] == null) ? null : v - EQE.y[i])
    .filter((v) => v != null);
  const rmseE = Math.sqrt(errE.reduce((a2, b2) => a2 + b2 * b2, 0) / errE.length);
  ok(rmseE > 0.1 && rmseE < 2,
     'e esse ajuste explica a expectativa de verdade -- na ordem do estimado',
     'RMSE ' + rmseE.toFixed(3) + ' p.p.');

  // ── e as duas pontas da (R), que ganharam gabarito com as contas derivadas ──
  // A (R) nao tinha gabarito ate 2026-09-25: o desvio e a ancora chegavam prontos no
  // payload. Com as duas virando CONTA refeita nas duas pontas, elas passaram a ser
  // exatamente o tipo de coisa que diverge em silencio.
  let nParR = 0, piorParR = 0;
  EQ.ajuste.forEach((alvo, i) => {
    if (alvo == null || i < 2) return;
    const e1 = { pi_e: ctx.simObs('pi_e', i, 1),
                 meta_12m: ctx.simObs('meta_12m', i, 1),
                 rr_10a: ctx.simObs('rr_10a', i, 1) };
    EQ.dummies.forEach((c) => { e1[c] = [EQ.dummy_obs[c][i] || 0]; });
    const got = ctx._simCaminhoSelic(EQ.mediana, i, 1, e1)[0];
    piorParR = Math.max(piorParR, Math.abs(got - alvo));
    nParR += 1;
  });
  ok(nParR > 60, 'ha trimestres bastantes para comparar as duas pontas da (R)',
     String(nParR));
  ok(piorParR < 1e-5,
     'e o JS reproduz o ajuste da (R) que o Python calculou',
     'pior diferenca ' + piorParR.toExponential(2) + ' p.p.');
  const errR = EQ.ajuste
    .map((v, i) => (v == null || EQ.selic_obs[i] == null) ? null : v - EQ.selic_obs[i])
    .filter((v) => v != null);
  const rmseR = Math.sqrt(errR.reduce((a2, b2) => a2 + b2 * b2, 0) / errR.length);
  ok(rmseR > 0.1 && rmseR < 2,
     'e o ajuste da (R) explica a Selic de verdade', 'RMSE ' + rmseR.toFixed(3));

  // ── o grafico da (E), no contrato da casa ──
  restaura();
  ctx.renderSim();
  ok(!!PLOT['ch-simexp'], 'o grafico da (E) e pintado');
  const ytE = PLOT['ch-simexp'].layout.yaxis.title;
  ok((ytE || '').length > 6 && /12 meses/.test(ytE),
     'o eixo nomeia a unidade e o horizonte', ytE);
  const frE = document.getElementById('ch-simexp').parentNode._chFrame;
  ok(frE.title.textContent.length > 4, 'ch-simexp: tem titulo');
  ok(frE.sub.textContent.length > 8, 'ch-simexp: tem subtitulo derivado');
  ok(frE.src.textContent.indexOf('Fonte:') === 0, 'ch-simexp: e linha de fonte');
  ok(Array.isArray(PLOT['ch-simexp'].layout.shapes),
     'ch-simexp: as formas sao passadas SEMPRE');
  const kidsE = Array.prototype.slice.call(
    document.getElementById('ch-simexp').parentNode.children);
  let iBarE = -1;
  kidsE.forEach((c, j) => { if (c._cls().includes('range-pills')) iBarE = j; });
  ok(iBarE > kidsE.indexOf(document.getElementById('ch-simexp')),
     'ch-simexp: a regua de tempo vem depois do grafico');
  const rEx = RELAYOUTS.filter((x) => x.div === 'ch-simexp' && x.upd['xaxis.range']);
  ok(rEx.length > 0, 'e ele recebeu uma janela calculada, nao autorange');
  // A meta atravessa o corte junto com a expectativa, pela mesma regra da ancora no
  // grafico da (R): ela e premissa que a conta consome nos trimestres projetados.
  const trMeta = ctx._tracesSimExp(SIM._ultimo).filter(
    (t) => t.line && t.line.dash === 'dot');
  ok(trMeta.length === 2, 'sao duas linhas pontilhadas: a meta observada e a projetada',
     String(trMeta.length));
  ok(trMeta[1].showlegend === false,
     'e a projetada nao ganha legenda propria -- e a mesma linha continuando');
  const metaProj = trMeta[1].y.slice(1);
  ok(metaProj.every((v, i) => Math.abs(v - SIM._ultimo.ent.meta_12m[i]) < 1e-12),
     'e ela e EXATAMENTE o caminho que a recursao consome, nao uma extrapolacao',
     metaProj.length + ' trimestres conferidos');

  // O grafico do cambio, no contrato da casa.
  restaura();
  ctx.renderSim();
  const ytF = PLOT['ch-simfx'].layout.yaxis.title;
  ok((ytF || '').length > 6 && /real|dólar|dolar/i.test(ytF),
     'o eixo do cambio nomeia a unidade, e ela e o NIVEL', ytF);
  const frF = document.getElementById('ch-simfx').parentNode._chFrame;
  ok(frF.title.textContent.length > 4, 'ch-simfx: tem titulo');
  ok(frF.sub.textContent.length > 8, 'ch-simfx: tem subtitulo derivado');
  ok(frF.src.textContent.indexOf('Fonte:') === 0, 'ch-simfx: e linha de fonte');
  ok(Array.isArray(PLOT['ch-simfx'].layout.shapes),
     'ch-simfx: as formas sao passadas SEMPRE');
  const kidsF = Array.prototype.slice.call(
    document.getElementById('ch-simfx').parentNode.children);
  let iBarF = -1;
  kidsF.forEach((c, j) => { if (c._cls().includes('range-pills')) iBarF = j; });
  ok(iBarF > kidsF.indexOf(document.getElementById('ch-simfx')),
     'ch-simfx: a regua de tempo vem depois do grafico');
  // A regua e refeita so quando a ponta direita anda, entao aqui ela ja foi aplicada
  // antes -- o que se afirma e a ULTIMA janela que o grafico recebeu, e nao o estado
  // do layout, que nao guarda o que veio por `relayout`.
  const rFx = RELAYOUTS.filter((x) => x.div === 'ch-simfx' && x.upd['xaxis.range']);
  ok(rFx.length > 0, 'o grafico do cambio recebeu uma janela calculada, nao autorange');
  ok(rFx[rFx.length - 1].upd['xaxis.range'][1]
       >= SIM._ultimo.g.x[SIM._ultimo.g.x.length - 1],
     'e ela alcanca o ultimo trimestre projetado',
     rFx[rFx.length - 1].upd['xaxis.range'][1] + ' contra '
       + SIM._ultimo.g.x[SIM._ultimo.g.x.length - 1]);

  // ════ 8r. O hiato, a quarta equacao do simulador ════════════════════════════
  // A (H) le a Selic que a (R) produz, com um trimestre de atraso, e e por ela que o
  // juro chega ao produto. O aperto e CONTA de tres cartoes -- a mesma ancora que a (R)
  // persegue --, e a conta e refeita nas duas pontas: daqui o gabarito de um passo e a
  // exigencia de que a conta dos cartoes devolva a coluna que a estimacao usou.
  secao('8r. O hiato, a quarta equacao do simulador');
  restaura();
  ctx.renderSim();
  const EQH = D.sim.eq.H;
  ok(!!EQH && EQH.explica === 'hiato' && D.sim.var.hiato.produtor_no_sim === true,
     'a (H) explica o hiato, e ele consta como endogena NESTA rodada');
  ok(EQH.consome.join(',') === 'selic,rr_10a,meta_12m',
     'ela consome a Selic, o juro real de 10 anos e a meta -- e so isso tem cartao',
     EQH.consome.join(','));
  const gd = EQH.deriva && EQH.deriva.gap;
  ok(!!gd && gd.op === 'lin' && gd.de.join(',') === 'selic,rr_10a,meta_12m'
       && gd.coef.join(',') === '1,-1,-1',
     'o aperto e CONTA: a Selic menos o juro real de 10 anos menos a meta',
     gd ? gd.op + ' ' + gd.coef.join(',') : '-');
  ok(!D.sim.var.gap, 'e ele nao e cartao -- um cartao deixaria digitar um aperto que '
     + 'contradiz a Selic da rodada');
  ok(['selic', 'rr_10a', 'meta_12m'].every((k) =>
       D.sim.var[k].consumida_por.indexOf('H') >= 0),
     'os tres cartoes que ela le dizem que ela os le');
  ok(D.sim.var.hiato.consumida_por.join(',') === 'H,I',
     'e o hiato e lido pela propria (H), defasado, e pela curva de Phillips, no mesmo '
     + 'trimestre', D.sim.var.hiato.consumida_por.join(','));
  ok(EQH.lag === 1, 'o aperto chega com um trimestre de atraso, e isso esta no payload',
     String(EQH.lag));

  // A conta feita dos CARTOES devolve a coluna do painel que a estimacao usou, na
  // grade inteira. E o que prova que `deriva` e a identidade do painel sao a mesma
  // coisa -- mesmo papel do `i12_pub` da (E).
  {
    const gObs = ctx._simDerivObs('H', 'gap');
    let nG = 0, piorG = 0;
    gObs.forEach((v, i) => {
      if (v == null || EQH.gap_pub[i] == null) return;
      piorG = Math.max(piorG, Math.abs(v - EQH.gap_pub[i]));
      nG += 1;
    });
    ok(nG > 60, 'ha trimestres bastantes para conferir a conta do aperto', String(nG));
    // 1e-5 e o arredondamento do payload (seis casas em quatro series), nao folga
    ok(piorG < 1e-5,
       'a conta dos cartoes devolve a coluna do painel que a estimacao usou',
       'pior ' + piorG.toExponential(2));
    ok(ctx._simDerivObsEm('H', 'gap', 5) === gObs[5],
       'e a leitura de um trimestre so e a mesma conta que a da grade');
  }

  // O gabarito de um passo: as duas recursoes -- Python e navegador -- tem de dar o
  // mesmo numero rodando h = 1 a partir de cada trimestre. O Python le o aperto da
  // coluna do painel; o JS o refaz dos cartoes. Um passo bater prova as duas coisas.
  {
    let nParH = 0, piorParH = 0;
    EQH.ajuste.forEach((alvo, i) => {
      if (alvo == null || i < 1) return;
      const e1 = { selic: ctx.simObs('selic', i, 1),
                   rr_10a: ctx.simObs('rr_10a', i, 1),
                   meta_12m: ctx.simObs('meta_12m', i, 1) };
      EQH.dummies.forEach((c) => { e1[c] = [EQH.dummy_obs[c][i] || 0]; });
      const got = ctx._simCaminhoHiato(EQH.mediana, i, 1, e1)[0];
      piorParH = Math.max(piorParH, Math.abs(got - alvo));
      nParH += 1;
    });
    ok(nParH > 60, 'ha trimestres bastantes para comparar as duas pontas da (H)',
       String(nParH));
    ok(piorParH < 1e-5, 'e o JS reproduz o ajuste da (H) que o Python calculou',
       'pior diferenca ' + piorParH.toExponential(2) + ' p.p.');
    const errH = EQH.ajuste
      .map((v, i) => (v == null || EQH.y[i] == null) ? null : v - EQH.y[i])
      .filter((v) => v != null);
    const rmseH = Math.sqrt(errH.reduce((a2, b2) => a2 + b2 * b2, 0) / errH.length);
    ok(rmseH > 0.3 && rmseH < 1.5,
       'e esse ajuste explica o hiato de verdade -- na ordem do estimado',
       'RMSE ' + rmseH.toFixed(3) + ' p.p.');
  }

  // Sem termo constante: com o aperto em zero e sem crise, o hiato volta a ZERO; com um
  // aperto permanente de 1 p.p., ele para em h2/(1-h1). As duas coisas no caminho
  // SIMULADO, e nao so na algebra.
  {
    const ZH = 400;
    const fill = (v) => new Array(ZH).fill(v);
    const entZ = { selic: fill(10), rr_10a: fill(7), meta_12m: fill(3) };
    EQH.dummies.forEach((c) => { entZ[c] = fill(0); });
    const zc = ctx._simCaminhoHiato(EQH.mediana, SIM.i0, ZH, entZ);
    ok(Math.abs(zc[ZH - 1]) < 1e-6,
       'com o aperto em zero o hiato volta a zero -- a conta nao tem termo constante',
       zc[ZH - 1].toExponential(2));
    const entU = { selic: fill(11), rr_10a: fill(7), meta_12m: fill(3) };
    EQH.dummies.forEach((c) => { entU[c] = fill(0); });
    const uc = ctx._simCaminhoHiato(EQH.mediana, SIM.i0, ZH, entU);
    const lp = EQH.mediana.h2 / (1 - EQH.mediana.h1);
    ok(Math.abs(uc[ZH - 1] - lp) < 1e-6,
       'e com 1 p.p. de aperto para sempre ele para em h2/(1-h1)',
       uc[ZH - 1].toFixed(6) + ' contra ' + lp.toFixed(6));
  }

  // O ELO (R) -> (H), na recursao: a (H) le a Selic que a (R) produziu NESTA rodada, e
  // mais Selic da menos hiato -- com um trimestre de atraso.
  {
    const U = SIM._ultimo;
    ok(U.ent.selic === U.cam,
       'a (H) le a Selic que a (R) produziu nesta rodada, e nao a observada');
    const base = ctx._simCaminhoHiato(SIM.coef.H, SIM.i0, SIM.h, U.ent);
    // 1e-9 e nao zero: o caminho desenhado e o do laco resolvido, que para quando nada
    // muda mais que 1e-10 -- refaze-lo sobre o resultado devolve o mesmo ate ali.
    ok(base.every((v, i) => Math.abs(v - U.is.cam[i]) < 1e-9),
       'e o caminho desenhado e exatamente essa recursao, sobre o laco resolvido');
    const alto = ctx._simCaminhoHiato(SIM.coef.H, SIM.i0, SIM.h,
      ctx._simEntCom(U.ent, 'selic', U.ent.selic.map((v) => v + 2)));
    ok(alto[alto.length - 1] < base[base.length - 1],
       'mais Selic, hiato menor no fim -- o juro chega ao produto',
       base[base.length - 1].toFixed(3) + ' -> ' + alto[alto.length - 1].toFixed(3));
    ok(Math.abs(alto[0] - base[0]) < 1e-12,
       'e o primeiro trimestre nao se mexe: o aperto chega com um trimestre de atraso');
    ok(U.is.sens != null && U.is.sens < 0,
       'a sensibilidade que a ficha imprime e medida, e tem o sinal do aperto',
       String(U.is.sens));
    ok(U.is.eloR != null, 'e o elo (R) -> (H) tambem e medido, no cenario da tela',
       String(U.is.eloR));
  }

  // A faixa: com as cinco ligadas, o laco leva a incerteza de todas ao hiato -- a Selic
  // que ele le vem da expectativa, que vem da inflacao, que vem do proprio hiato.
  {
    const U = SIM._ultimo;
    ok(U.is.nEq === 5, 'a faixa do hiato carrega a incerteza das cinco equacoes',
       String(U.is.nEq));
    ok(!!U.is.faixa && U.is.faixa.lo.every((v, i) => v <= U.is.faixa.hi[i]),
       'e ela existe, com a ponta de baixo abaixo da de cima');
    const trH = PLOT['ch-simis'].traces;
    ok(trH.some((t) => /cinco equações/.test(t.name || '')),
       'a legenda da faixa diz de quantas equacoes ela carrega incerteza');
  }

  // Com a Selic imposta, so a (H) propaga; com o hiato imposto, nao ha faixa e o
  // cartao da equacao diz que ela esta desligada.
  SIM.fonte.selic = 'observado';
  ctx.renderSim();
  ok(SIM._ultimo.is.nEq === 1,
     'com a Selic imposta, a faixa do hiato carrega so a (H)',
     String(SIM._ultimo.is.nEq));
  restaura();
  SIM.fonte.hiato = 'observado';
  ctx.renderSim();
  ok(SIM._ultimo.is.faixa === null, 'com o hiato imposto, nao ha faixa nenhuma');
  {
    const av = document.getElementById('simAviso-H');
    ok(av.style.display !== 'none' && /curva IS está desligada/.test(av.innerHTML),
       'e o cartao da (H) diz que ela esta desligada', av.innerHTML.slice(0, 80));
  }
  restaura();
  ctx.renderSim();

  // A ficha: a conta escrita com o sinal de CADA peca, e os numeros medidos.
  {
    const fH = document.getElementById('simEqSub-H').innerHTML;
    ok(fH.indexOf('Selic menos juro real de 10 anos menos meta de inflação') >= 0,
       'a ficha escreve a conta com o sinal de cada peca', fH.slice(0, 160));
    ok(fH.indexOf(ctx.fmt(Math.abs(EQH.mediana.h2), 3)) >= 0,
       'e imprime o peso do aperto da mediana do posterior');
    // Em modulo, com a direcao por extenso: "leva o hiato a -0,44" se lia como nivel.
    const uIs = SIM._ultimo.is;
    ok(fH.indexOf(ctx.fmt(Math.abs(uIs.sens)) + ' p.p. '
                  + (uIs.sens < 0 ? 'mais baixo' : 'mais alto')) >= 0,
       'e a sensibilidade, com a direcao dita por extenso');
    ok(fH.indexOf(ctx.fmt(Math.abs(uIs.eloR)) + ' p.p. '
                  + (uIs.eloR > 0 ? 'mais alto' : 'mais baixo')) >= 0,
       'e o elo (R) -> (H), tambem com a direcao');
    ok(fH.indexOf('leva o hiato a') < 0,
       'a redacao que se lia como nivel saiu');
    const tH = document.getElementById('simEqTitulo-H').textContent;
    ok(/\(H\)/.test(tH) && /o hiato do produto/.test(tH),
       'o titulo diz de que equacao ele e e o que ela explica', tH);
  }

  // O grafico do hiato, no contrato da casa.
  {
    const ytH = PLOT['ch-simis'].layout.yaxis.title;
    ok(ytH === ctx.EIXO_IS, 'o eixo do hiato e a MESMA string da aba Hiato', ytH);
    ok(PLOT['ch-simis'].layout.yaxis.zeroline === true,
       'e o zero -- o repouso do hiato -- e a referencia do grafico');
    const frH = document.getElementById('ch-simis').parentNode._chFrame;
    ok(frH.title.textContent.length > 4, 'ch-simis: tem titulo');
    ok(frH.sub.textContent.length > 8, 'ch-simis: tem subtitulo derivado');
    ok(frH.src.textContent.indexOf('Fonte:') === 0, 'ch-simis: e linha de fonte');
    ok(Array.isArray(PLOT['ch-simis'].layout.shapes),
       'ch-simis: as formas sao passadas SEMPRE');
    const kidsH = Array.prototype.slice.call(
      document.getElementById('ch-simis').parentNode.children);
    let iBarH = -1;
    kidsH.forEach((c, j) => { if (c._cls().includes('range-pills')) iBarH = j; });
    ok(iBarH > kidsH.indexOf(document.getElementById('ch-simis')),
       'ch-simis: a regua de tempo vem depois do grafico');
    const rIs = RELAYOUTS.filter((x) => x.div === 'ch-simis' && x.upd['xaxis.range']);
    ok(rIs.length > 0, 'o grafico do hiato recebeu uma janela calculada, nao autorange');
  }

  // ════ 8s. A curva de Phillips, a quinta equacao, e o laco ═════════════════════
  // Pedido do usuario em 2026-09-28: *"you can enter this in the simulator"*. A (I) le o
  // hiato, a expectativa e o cambio, e o que ela produz volta para a (E) e para a (F):
  // o simulador deixa de ser uma corrente. Tres coisas precisam de gabarito proprio --
  // cada grupo (um passo, contra as colunas do painel), a conta dentro da janela (varios
  // passos, contra a forma fechada) e o laco (o cenario padrao, contra o Python).
  secao('8s. A curva de Phillips, a quinta equacao, e o laco');
  restaura();
  ctx.renderSim();
  const EQI = D.sim.eq.I;
  ok(!!EQI && EQI.explica === 'infl_br' && EQI.key === 'I',
     'a (I) esta no simulador e explica a inflacao do trimestre');
  ok(EQI.consome.join(',') === 'hiato,pi_e,de,icbr_agr_usd,icbr_met_usd',
     'ela consome o hiato, a expectativa, o cambio e as duas cestas de commodity',
     EQI.consome.join(','));
  ok(['icbr_agr_usd', 'icbr_met_usd'].every((k) => D.sim.var[k]
       && D.sim.var[k].regiao === 'externa' && D.sim.var[k].tipo === 'exogena'
       && D.sim.var[k].consumida_por.join(',') === 'I'),
     'as duas cestas sao cartoes externos, lidos so pela (I)');
  ok(D.sim.var.infl_br.consumida_por.join(',') === 'I,E,F',
     'e a inflacao e lida pela propria (I), defasada, pela (E) e pela (F)',
     D.sim.var.infl_br.consumida_por.join(','));
  ok(D.sim.var.pi_e.consumida_por.indexOf('I') >= 0,
     'a expectativa diz que a (I) a le -- como a ancora do trimestre seguinte');

  // As contas: o cambio MEDIO e as duas commodities, nenhuma com cartao.
  ok(EQI.deriva.de_med.op === 'dlog_medio' && EQI.deriva.de_med.de.join(',') === 'de',
     'o cambio que ela le e conta: a variacao do cambio MEDIO, feita de dois fechamentos');
  ok(EQI.deriva.agr.op === 'dlog' && EQI.deriva.met.op === 'dlog',
     'e as commodities tambem: a variacao do nivel de um trimestre para o outro');
  ok(!D.sim.var.de_med && !D.sim.var.agr && !D.sim.var.met,
     'e nenhuma delas e cartao');
  {
    const dm = ctx._simDerivObs('I', 'de_med'), P = D.sim.var.de.obs;
    let pior = 0, n = 0;
    for (let i = 2; i < P.length; i++) {
      if (dm[i] == null) continue;
      const a = 100 * Math.log(P[i] / P[i - 1]), b = 100 * Math.log(P[i - 1] / P[i - 2]);
      pior = Math.max(pior, Math.abs(dm[i] - 0.5 * (a + b)));
      n += 1;
    }
    ok(n > 60 && pior < 1e-12,
       'o cambio medio e exatamente a media de duas variacoes de fechamento seguidas',
       n + ' trimestres, pior ' + pior.toExponential(2));
  }

  // Todo peso estimado tem lugar na recursao -- conferido no Python ao montar, e aqui do
  // lado que o usa: cada termo de cada grupo tem um peso no payload.
  {
    let faltam = [];
    EQI.ordem_grupos.forEach((g) => {
      const sp = EQI.grupos[g];
      [sp.inercia].concat(sp.restritos.map((x) => x[0]), sp.regs.map((x) => x[0]), sp.saz)
        .forEach((q) => { if (typeof EQI.mediana[g + '.' + q] !== 'number') faltam.push(g + '.' + q); });
    });
    ok(faltam.length === 0, 'todo termo dos quatro grupos tem peso no payload',
       faltam.join(',') || '(nenhum faltando)');
    ok(EQI.pars.every((q) => EQI.draws[q] && EQI.draws[q].length === EQI.n_draws),
       'e os desenhos vieram completos, pareados entre os grupos', String(EQI.n_draws));
    const somaP = EQI.ordem_grupos.reduce((a, g) => a + EQI.pesos_fim[g], 0);
    ok(Math.abs(somaP - 1) < 1e-9, 'os pesos do fim somam 1', somaP.toFixed(12));
  }

  // O gabarito de um passo, grupo a grupo e no cheio. O Python le as colunas do painel
  // (media movel, cheio defasado, variacao das commodities); o JS as refaz dos cartoes.
  {
    const V = D.sim.var;
    const pior = { cheio: 0 };
    EQI.ordem_grupos.forEach((g) => { pior[g] = 0; });
    let n = 0;
    EQI.ajuste.cheio.forEach((alvo, i) => {
      if (alvo == null) return;
      const e1 = { hiato: [V.hiato.obs[i]], pi_e: [V.pi_e.obs[i]], de: [V.de.obs[i]],
                   icbr_agr_usd: [V.icbr_agr_usd.obs[i]],
                   icbr_met_usd: [V.icbr_met_usd.obs[i]] };
      const partes = [];
      const got = ctx._simCaminhoInfl(EQI.mediana, i, 1, e1, partes)[0];
      pior.cheio = Math.max(pior.cheio, Math.abs(got - alvo));
      EQI.ordem_grupos.forEach((g) => {
        pior[g] = Math.max(pior[g], Math.abs(partes[0].grupos[g] - EQI.ajuste[g][i]));
      });
      n += 1;
    });
    ok(n > 60, 'ha trimestres bastantes para comparar as duas pontas da (I)', String(n));
    Object.keys(pior).forEach((k) => {
      ok(pior[k] < 1e-5,
         '(' + k + ') o JS reproduz o ajuste de um passo que o Python fez do painel',
         'pior diferenca ' + pior[k].toExponential(2));
    });
    const err = EQI.ajuste.cheio
      .map((v, i) => (v == null || EQI.y[i] == null) ? null : v - EQI.y[i])
      .filter((v) => v != null);
    const rmse = Math.sqrt(err.reduce((a, b) => a + b * b, 0) / err.length);
    ok(rmse > 0.3 && rmse < 1.2,
       'e esse ajuste explica o IPCA do trimestre de verdade -- na ordem do estimado',
       'RMSE ' + rmse.toFixed(3) + ' p.p.');
    ok(ctx._simPassoTri(3).tri === parseInt(D.sim.rot[3].slice(5), 10)
       && ctx._simPassoTri(D.sim.rot.length + 5).tri >= 1,
       'o trimestre do ano que decide a sazonal sai da contagem, dentro e fora da grade');
  }

  // A conta DENTRO da janela, que o gabarito de um passo nao alcanca: la toda defasagem
  // vem do observado. Tres propriedades em 400 trimestres, cada uma com a forma fechada.
  {
    const ZH = 400, EXP = 4.0, fill = (v) => new Array(ZH).fill(v);
    const V = D.sim.var, i0 = SIM.i0;
    const entR = { hiato: fill(0), pi_e: fill(EXP), de: fill(V.de.obs[i0 - 1]),
                   icbr_agr_usd: fill(V.icbr_agr_usd.obs[i0 - 1]),
                   icbr_met_usd: fill(V.icbr_met_usd.obs[i0 - 1]) };
    const md = EQI.mediana, w = EQI.pesos_fim;
    const base = [];
    ctx._simCaminhoInfl(md, i0, ZH, entR, base);
    const media4 = (ps, f) => ps.slice(-4).reduce((a, p) => a + f(p), 0) / 4;
    // 1. sem choque, a media do ano de cada grupo converge para a expectativa: a
    // restricao soma 1 e as quatro sazonais somam zero
    EQI.ordem_grupos.forEach((g) => {
      const m = media4(base, (p) => p.grupos[g]);
      ok(Math.abs(m - EXP / 4) < 1e-6,
         g + ': sem choque, a media do ano converge para a expectativa do trimestre',
         m.toFixed(8) + ' contra ' + (EXP / 4).toFixed(8));
    });
    const mc = media4(base, (p) => p.cheio);
    ok(Math.abs(mc - EXP / 4) < 1e-6, 'e o cheio tambem', mc.toFixed(8));
    // 2. um hiato de 1 p.p. para sempre soma ao cheio a forma fechada, com a indexacao
    // dos monitorados devolvendo parte dele ao proprio cheio
    const pe = (g) => { const sp = EQI.grupos[g];
      return 1 - md[g + '.' + sp.inercia]
        - sp.restritos.reduce((a, rt) => a + md[g + '.' + rt[0]], 0); };
    const b = (g, fonte) => { const r = EQI.grupos[g].regs.filter((x) => x[1] === fonte)[0];
      return r ? md[g + '.' + r[0]] : 0; };
    const im1 = md['IM.im1'], im2 = md['IM.im2'];
    const mult = (1 - im1) / (1 - im1 - im2 * w.IM);
    const comH = [];
    ctx._simCaminhoInfl(md, i0, ZH, Object.assign({}, entR, { hiato: fill(1) }), comH);
    const lpH = mult * ['IS', 'IA', 'II'].reduce((a, g) => a + w[g] * b(g, 'hiato') / pe(g), 0);
    const efH = media4(comH, (p) => p.cheio) - mc;
    ok(Math.abs(efH - lpH) < 1e-6,
       'um hiato de 1 p.p. para sempre soma ao cheio exatamente a forma fechada',
       efH.toFixed(6) + ' contra ' + lpH.toFixed(6));
    // 3. uma depreciacao de 1%, uma vez so, chega ao nivel do IPCA na forma fechada --
    // o que prova o cambio medio DENTRO da janela: a metade do trimestre do choque e a
    // metade do seguinte, e a defasagem de bens industriais sobre as duas
    const comF = [];
    ctx._simCaminhoInfl(md, i0, ZH, Object.assign({}, entR, {
      de: entR.de.map((v) => v * Math.exp(0.01)) }), comF);
    let acum = 0;
    for (let k = 0; k < ZH; k++) acum += comF[k].cheio - base[k].cheio;
    const lpF = mult * (w.IA * b('IA', 'de_med') / pe('IA')
                        + w.II * b('II', 'de_med_l1') / pe('II'));
    ok(Math.abs(acum - lpF) < 1e-6,
       'e uma depreciacao de 1% chega ao nivel do IPCA exatamente na forma fechada',
       acum.toFixed(6) + '% contra ' + lpF.toFixed(6) + '%');
    ok(comF[0].cheio > base[0].cheio && Math.abs(comF[0].grupos.II - base[0].grupos.II) < 1e-12,
       'e no trimestre do choque so a alimentacao se mexe -- industriais vem depois');
  }

  // O LACO. O cenario padrao resolvido no Python viaja no payload; o navegador tem de
  // resolver o mesmo, porque as duas pontas da conta que junta as cinco sao escritas duas
  // vezes, e nenhum gabarito de equacao alcanca essa conta.
  {
    const sp = D.sim.sistema_padrao;
    ok(!!sp && sp.voltas >= 2 && sp.voltas < 40,
       'o payload traz o cenario padrao resolvido do lado do Python, em poucas voltas',
       String(sp && sp.voltas));
    restaura();
    ctx.renderSim();
    const U = SIM._ultimo;
    let pior = 0;
    D.sim.eq_ordem.forEach((ek) => {
      const v = D.sim.eq[ek].explica;
      sp.caminho[v].forEach((x, i) => { pior = Math.max(pior, Math.abs(x - U.ent[v][i])); });
    });
    ok(pior < 1e-7, 'e o navegador resolve o MESMO laco: os cinco caminhos batem com o Python',
       'pior ' + pior.toExponential(2));
    ok(Math.abs(U.voltas - sp.voltas) <= 1, 'nas mesmas voltas, a menos de uma',
       U.voltas + ' contra ' + sp.voltas);
    D.sim.eq_ordem.forEach((ek) => {
      const v = D.sim.eq[ek].explica;
      const novo = ctx._simRoda(ek, SIM.coef[ek], SIM.i0, SIM.h, U.ent);
      const d = Math.max.apply(null, novo.map((x, i) => Math.abs(x - U.ent[v][i])));
      ok(d < 1e-9, '(' + ek + ') rodada sobre o laco resolvido, devolve o proprio caminho',
         d.toExponential(2));
    });
    // Uma passada so -- a corrente de antes -- deixaria alguem lendo um caminho velho.
    const uma = {};
    Object.keys(U.base).forEach((k) => { uma[k] = U.base[k].slice(); });
    D.sim.eq_ordem.forEach((ek) => {
      uma[D.sim.eq[ek].explica] = ctx._simRoda(ek, SIM.coef[ek], SIM.i0, SIM.h, uma);
    });
    const difUma = Math.max.apply(null, D.sim.eq_ordem.map((ek) => {
      const v = D.sim.eq[ek].explica;
      return Math.max.apply(null, uma[v].map((x, i) => Math.abs(x - U.ent[v][i])));
    }));
    ok(difUma > 1e-3, 'e uma passada so NAO bastaria: ela erra o resolvido de verdade',
       difUma.toFixed(4));
    ok(U.naoConvergiu === 0, 'todos os desenhos da faixa convergiram',
       String(U.naoConvergiu));
    ok(D.sim.eq_ordem.every((ek) => {
      const e = D.sim.eq[ek];
      const n = { E: U.exp, R: { nEq: U.nEqR }, H: U.is, I: U.infl, F: U.fx }[ek].nEq;
      return n === 5;
    }), 'com as cinco ligadas, toda faixa carrega a incerteza das cinco');
  }

  // Os elos que ENTRAM na (I), e o que sai dela. Cada um medido contra a mesma rodada com
  // aquela variavel parada, e com o sinal que a equacao diz.
  {
    const fim12 = () => SIM._ultimo.infl.i12[SIM.h - 1];
    restaura();
    SIM.fonte.hiato = 'observado';
    ctx.renderSim();
    const hObs = fim12();
    SIM.fonte.hiato = 'digitado';
    SIM.cx.hiato = ctx.simObs('hiato', SIM.i0, D.sim.h_max).map((v) => v + 1);
    ctx.renderSim();
    ok(fim12() > hObs, 'mais hiato, mais inflacao: o produto chega aos precos',
       hObs.toFixed(3) + ' -> ' + fim12().toFixed(3));
    restaura();
    SIM.fonte.de = 'observado';
    ctx.renderSim();
    const dObs = fim12();
    SIM.fonte.de = 'digitado';
    SIM.cx.de = ctx.simObs('de', SIM.i0, D.sim.h_max).map((v) => v * 1.1);
    ctx.renderSim();
    ok(fim12() > dObs, 'e um real 10% mais fraco, mais inflacao: o cambio chega aos precos',
       dObs.toFixed(3) + ' -> ' + fim12().toFixed(3));
    // e o que sai da (I) volta: desligar a curva de Phillips muda a Selic
    restaura();
    ctx.renderSim();
    const selCom = SIM._ultimo.cam[SIM.h - 1], expCom = SIM._ultimo.exp.cam[SIM.h - 1];
    SIM.fonte.infl_br = 'observado';
    ctx.renderSim();
    ok(Math.abs(SIM._ultimo.cam[SIM.h - 1] - selCom) > 1e-3
       && Math.abs(SIM._ultimo.exp.cam[SIM.h - 1] - expCom) > 1e-3,
       'e a inflacao volta: com a curva de Phillips desligada a expectativa e a Selic mudam',
       'Selic ' + selCom.toFixed(3) + ' -> ' + SIM._ultimo.cam[SIM.h - 1].toFixed(3));
    ok(SIM._ultimo.infl.faixa === null && SIM._ultimo.exp.nEq === 1,
       'e o laco abre: sem a (I), a faixa da expectativa volta a ser so a dela',
       String(SIM._ultimo.exp.nEq));
    const av = document.getElementById('simAviso-I');
    ok(av.style.display !== 'none' && /curva de Phillips está desligada/.test(av.innerHTML)
       && /laço fica aberto/.test(av.innerHTML),
       'e o cartao da (I) diz que ela esta desligada e que o laco abriu',
       av.innerHTML.slice(0, 90));
    restaura();
  }

  // A ficha e o cartao.
  {
    restaura();
    ctx.renderSim();
    const U = SIM._ultimo;
    const tI = document.getElementById('simEqTitulo-I').textContent;
    ok(/\(I\)/.test(tI) && /a inflação do Brasil no trimestre/.test(tI),
       'o titulo diz de que equacao ele e e o que ela explica', tI);
    const fI = document.getElementById('simEqSub-I').innerHTML;
    ok(/quatro equações por dentro/.test(fI), 'a ficha diz que sao quatro grupos por dentro');
    ok(fI.indexOf(ctx.fmt(EQI.mediana['IS.is2'], 3)) >= 0,
       'e imprime o peso do hiato em servicos, da mediana');
    ok(fI.indexOf(ctx.fmt(Math.abs(U.infl.sens)) + ' p.p. '
                  + (U.infl.sens > 0 ? 'mais alto' : 'mais baixo')) >= 0,
       'e a sensibilidade ao hiato, com a direcao por extenso', String(U.infl.sens));
    ok(U.infl.eloH != null && U.infl.eloF != null
       && fI.indexOf(ctx.fmt(Math.abs(U.infl.eloF))) >= 0,
       'e os dois elos que entram nela, medidos no cenario');
    ok(/serviços <b>/.test(fI) && /monitorados <b>/.test(fI),
       'e o fim do horizonte em doze meses, grupo a grupo, pelo nome que se le numa frase');
    ok(/vira um laço/.test(fI), 'e diz que o modelo deixou de ser uma corrente');
    ok(/variação do câmbio médio do trimestre/.test(fI),
       'e nomeia a conta do cambio que ela faz, em vez de fingir que le o cartao');
    const htmlI = document.getElementById('simInputs').innerHTML;
    const caixasI = htmlI.match(/<input[^>]*data-chave="infl_br"[^>]*>/g) || [];
    ok(caixasI.length === SIM.h && caixasI.every((c) => /sim-caixa-in eqp/.test(c)),
       'em Endogeno as caixas da inflacao mostram o que a equacao produz, em azul');
    ok(/vem da equação \(I\)/.test(htmlI),
       'e o selo do cartao diz que ela vem da (I), nesta rodada');
  }

  // O grafico da (I), no contrato da casa: em DOZE MESES, com a meta ao lado.
  {
    restaura();
    ctx.renderSim();
    const U = SIM._ultimo;
    ok(!!PLOT['ch-simipca'], 'o grafico da (I) e pintado');
    ok(PLOT['ch-simipca'].layout.yaxis.title === ctx.EIXO_SIMIPCA
       && /12 meses/.test(ctx.EIXO_SIMIPCA),
       'o eixo diz que e o IPCA de doze meses', ctx.EIXO_SIMIPCA);
    const trI = PLOT['ch-simipca'].traces;
    const simT = trI.filter((t) => /equação produz, 12 meses/.test(t.name || ''))[0];
    const i12 = ctx._simI12(SIM.i0, SIM.h, U.ent.infl_br);
    ok(!!simT && simT.y.slice(1).every((v, i) => Math.abs(v - i12[i]) < 1e-9),
       'a linha simulada e o caminho do laco composto em doze meses, trimestre a trimestre');
    ok(simT && Math.abs(simT.y[0] - EQI.i12_obs[SIM.i0 - 1]) < 1e-9,
       'e parte do ultimo IPCA de 12 meses observado');
    ok(trI.some((t) => /cinco equações/.test(t.name || '')),
       'a faixa diz que carrega as cinco');
    const f = U.infl.faixa;
    ok(f.lo.every((v, i) => v <= f.hi[i])
       && (f.hi[SIM.h - 1] - f.lo[SIM.h - 1]) > (f.hi[0] - f.lo[0]),
       'e ela alarga com o horizonte');
    ok(trI.filter((t) => t.line && t.line.dash === 'dot').length === 2,
       'a meta e desenhada, observada e projetada');
    const frI = document.getElementById('ch-simipca').parentNode._chFrame;
    ok(frI.title.textContent.length > 4, 'ch-simipca: tem titulo');
    ok(frI.sub.textContent.length > 8, 'ch-simipca: tem subtitulo derivado');
    ok(frI.src.textContent.indexOf('Fonte:') === 0, 'ch-simipca: e linha de fonte');
    ok(Array.isArray(PLOT['ch-simipca'].layout.shapes),
       'ch-simipca: as formas sao passadas SEMPRE');
    const kidsI = Array.prototype.slice.call(
      document.getElementById('ch-simipca').parentNode.children);
    let iBarI = -1;
    kidsI.forEach((c, j) => { if (c._cls().includes('range-pills')) iBarI = j; });
    ok(iBarI > kidsI.indexOf(document.getElementById('ch-simipca')),
       'ch-simipca: a regua de tempo vem depois do grafico');
    const rI = RELAYOUTS.filter((x) => x.div === 'ch-simipca' && x.upd['xaxis.range']);
    ok(rI.length > 0, 'o grafico da (I) recebeu uma janela calculada, nao autorange');
  }

  // A aba se chama Structural Model: ela e o modelo agregado, as cinco juntas.
  ok(/data-tab="tab-sim"[^>]*>Structural Model</.test(CRU),
     'a aba do simulador se chama Structural Model');
  ok(!/data-tab="tab-sim"[^>]*>Simulador</.test(CRU), 'e o nome antigo saiu da barra');
}

// ── §30 ───────────────────────────────────────────────────────────────────────
// A aba Impulso-resposta. Cada asserção existe por um defeito que sai plausível:
//  - o residuo novo e codigo novo nas cinco recursoes do JS, e nenhum gabarito de um
//    passo nem o `sistema_padrao` o alcancam -- dai o gabarito proprio, do Python;
//  - a faixa medida contra o cenario da MEDIANA (e nao o do mesmo desenho) mediria a
//    distancia entre dois cenarios de pesos, e nao o choque;
//  - um eixo de trimestres sem `type` explicito vira milissegundos.
secao('30. Impulso-resposta: um choque, e o caminho dele pelas cinco');
if (!D.irf) {
  ok(false, 'o payload traz o bloco do impulso-resposta');
} else {
  const IR = D.irf, i0 = D.sim.i0, h = IR.h;
  ok(h === 20, 'o horizonte e de 20 trimestres, decisao do usuario', String(h));
  const res = IR.alvos.filter((a) => a.tipo === 'residuo').map((a) => a.key);
  ok(res.join(',') === 'res:H,res:IS,res:IA,res:II,res:IM,res:E,res:R,res:F',
     'os alvos com equacao: um residuo por equacao, quatro na (I), na ordem de solucao',
     res.join(','));
  const exo = D.sim.var_ordem.filter((k) => D.sim.var[k].tipo !== 'endogena');
  const cam = IR.alvos.filter((a) => a.tipo === 'caminho').map((a) => a.key);
  ok(exo.join(',') === cam.join(','), 'e TODA exogena pode receber o choque', cam.join(','));
  ok(IR.alvos.filter((a) => a.modo === 'pct').map((a) => a.var).sort().join(',')
       === 'dxy_em,icbr_agr_usd,icbr_met_usd,icbr_usd,sp500',
     'nos indices o choque e em % do nivel, e so neles');

  // Os mesmos pesos da mediana nas duas pontas.
  const cm = {};
  D.sim.eq_ordem.forEach((ek) => { cm[ek] = ctx._simCoefPadrao(ek); });
  const base = ctx._irfEstado(cm, i0, h, ctx._irfEntradas(i0, h), null);

  // O gabarito: cinco choques resolvidos no Python, cada tipo de alvo e cada forma.
  let pior = 0, onde = '';
  IR.gabarito.forEach((g) => {
    const r = ctx.irfResposta(cm, ctx.irfAlvo(g.alvo), g.choque, i0, h, base);
    const cmp = (a, b, nm) => a.forEach((x, k) => {
      const d = Math.abs(x - b[k]);
      if (!(d <= pior)) { pior = d; onde = g.alvo + ' ' + nm + '[' + k + ']'; }
    });
    ['hiato', 'infl', 'infl12', 'pi_e', 'selic', 'de'].forEach((nm) => cmp(r[nm], g.resp[nm], nm));
    Object.keys(g.resp.grupos).forEach((q) => {
      cmp(r.grupos[q], g.resp.grupos[q], q);
      cmp(r.grupos12[q], g.resp.grupos12[q], q + '12');
    });
  });
  ok(IR.gabarito.length === 5 && pior < 1e-6,
     'as respostas do JS batem com as do Python nos cinco choques do gabarito',
     'pior ' + pior.toExponential(2) + ' em ' + onde);
  ok(IR.gabarito.some((g) => Math.max(...g.resp.selic.map(Math.abs)) > 0.1),
     'e o gabarito nao e de respostas nulas');

  // Choque zero, resposta zero -- em todo alvo.
  let piorZ = 0;
  IR.alvos.forEach((a) => {
    const r = ctx.irfResposta(cm, a, { tipo: 'decai', v: 0, n: 1, rho: 0.5 }, i0, h, base);
    ['hiato', 'infl', 'pi_e', 'selic', 'de'].forEach((nm) => r[nm].forEach((x) => {
      piorZ = Math.max(piorZ, Math.abs(x));
    }));
  });
  ok(piorZ < 1e-8, 'um choque de tamanho zero nao move nada, em nenhum alvo',
     piorZ.toExponential(2));

  // No impacto, um choque no residuo move a variavel pelo tamanho dele -- a menos do
  // que o proprio trimestre devolve pelo laco, que e pequeno.
  const rR = ctx.irfResposta(cm, ctx.irfAlvo('res:R'), { tipo: 'decai', v: 1, rho: 0 }, i0, h, base);
  ok(Math.abs(rR.selic[0] - 1) < 0.05, 'um residuo de 1 p.p. na regra move a Selic ~1 p.p. no impacto',
     ctx.fmt(rR.selic[0], 4));
  ok(rR.selic[1] > 0.5, 'e a suavizacao da regra o carrega para o trimestre seguinte',
     ctx.fmt(rR.selic[1], 4));
  ok(Math.abs(rR.hiato[0]) < 1e-9 && rR.hiato[1] < 0,
     'o hiato nao se move no impacto -- a (H) le a Selic de um trimestre antes -- e cai depois',
     ctx.fmt(rR.hiato[0], 6) + ' / ' + ctx.fmt(rR.hiato[1], 4));
  const rA = ctx.irfResposta(cm, ctx.irfAlvo('res:IA'), { tipo: 'decai', v: 1, rho: 0 }, i0, h, base);
  ok(Math.abs(rA.grupos.IA[0] - 1) < 0.02,
     'um residuo de 1 p.p. em alimentacao move alimentacao ~1 p.p. no impacto',
     ctx.fmt(rA.grupos.IA[0], 4));
  {
    const w = ctx._simPesosEm(i0);
    const soma = Object.keys(rA.grupos).reduce((s, g) => s + w[g] * rA.grupos[g][0], 0);
    ok(Math.abs(soma - rA.infl[0]) < 1e-9,
       'e a resposta do IPCA e a soma ponderada da dos quatro grupos',
       ctx.fmt(soma, 6) + ' contra ' + ctx.fmt(rA.infl[0], 6));
  }
  ok(rA.grupos.IA[1] > 0 && rA.grupos.IA[1] < rA.grupos.IA[0],
     'e a inercia de alimentacao carrega parte dele para o trimestre seguinte');

  // Um residuo permanente acumula pela persistencia da propria equacao: sem as outras
  // equacoes (todas desligadas menos a da Selic), a forma fechada e 1/(1 - t1 - t2).
  {
    const eqR = D.sim.eq.R, md = eqR.mediana, N = 400;
    const ent = ctx._irfEntradas(i0, N), lig = {};
    D.sim.eq_ordem.forEach((ek) => { lig[ek] = ek === 'R'; });
    const perm = ctx._simPerfilChoque({ tipo: 'rampa', v: 1, n: 1 }, N);
    const a = ctx._simResolver(cm, i0, N, ent, lig).ent.selic;
    const b = ctx._simResolver(cm, i0, N, ent, lig, null, { R: perm }).ent.selic;
    const lp = 1 / (1 - md.t1 - md.t2);
    ok(Math.abs((b[N - 1] - a[N - 1]) - lp) < 1e-6,
       'um residuo permanente na regra, sozinha, vale 1/(1 - t1 - t2) no longo prazo',
       ctx.fmt(b[N - 1] - a[N - 1], 4) + ' contra ' + ctx.fmt(lp, 4));
  }

  // Exogena: o choque troca o caminho, e em % do nivel nos indices.
  {
    const ent = ctx._irfEntradas(i0, h);
    const s = ctx._irfAplicar(ctx.irfAlvo('sp500'), { tipo: 'rampa', v: -10, n: 1 }, h, ent);
    ok(s.choque === null && s.ent.sp500.every((x, k) => Math.abs(x - 0.9 * ent.sp500[k]) < 1e-9),
       'um choque de -10% no S&P e o caminho segurado vezes 0,9, sem residuo nenhum');
    const f = ctx._irfAplicar(ctx.irfAlvo('ffr'), { tipo: 'rampa', v: 1, n: 1 }, h, ent);
    ok(f.ent.ffr.every((x, k) => Math.abs(x - ent.ffr[k] - 1) < 1e-12) && ent.ffr !== f.ent.ffr,
       'num juro o choque soma, e o caminho do cenario padrao fica intacto');
  }

  // A tela.
  ok(/data-tab="tab-irf"[^>]*>Impulso-resposta</.test(CRU), 'a aba existe e se chama Impulso-resposta');
  ok(!PLOT['ch-irf-selic'], 'os graficos nao sao pintados enquanto a aba esta fechada');
  const t0 = Date.now();
  ctx.activateTab('tab-irf');
  const ms = Date.now() - t0;
  console.log('        (pintura com a faixa: ' + ms + ' ms)');
  const divs = ['ch-irf-hiato', 'ch-irf-infl', 'ch-irf-pie', 'ch-irf-selic', 'ch-irf-de',
                'ch-irf-g-IS', 'ch-irf-g-IA', 'ch-irf-g-II', 'ch-irf-g-IM'];
  ok(divs.every((d) => PLOT[d]), 'os nove graficos plotam: as cinco endogenas e os quatro grupos',
     divs.filter((d) => !PLOT[d]).join(','));
  ok(ctx.IRF._ult.naoConvergiu === 0, 'todos os conjuntos de pesos convergem no choque padrao',
     String(ctx.IRF._ult.naoConvergiu));
  divs.forEach((d) => {
    const P = PLOT[d];
    if (!P) return;
    const xa = P.layout.xaxis;
    ok(xa.type === 'linear' && xa.range[0] === 0.5 && xa.range[1] === h + 0.5,
       d + ': eixo de trimestres linear, com janela calculada', xa.type + ' ' + xa.range);
    const fr = document.getElementById(d).parentNode._chFrame;
    ok(fr && fr.title.textContent.length > 3 && fr.src.textContent.indexOf('Fonte:') === 0
         && fr.src.textContent.indexOf(D.sim.rot.length ? ctx._simRotIdx(i0) : '') > 0,
       d + ': cabecalho de tres linhas, com a janela do choque');
    ok(fr.sub.textContent.indexOf(P.layout.yaxis.title) >= 0
         && fr.sub.textContent.indexOf('choque em') >= 0,
       d + ': o subtitulo diz o choque e a MESMA unidade do eixo', fr.sub.textContent);
    const med = P.traces[2].y, lo = P.traces[1].y, hi = P.traces[0].y;
    ok(med.length === h && lo.every((x, k) => x <= hi[k] + 1e-12),
       d + ': mediana e faixa com ' + h + ' trimestres, a faixa bem ordenada');
  });
  ok(PLOT['ch-irf-selic'].traces[2].y.every((x, k) =>
       Math.abs(x - ctx.IRF._ult.med.selic[k]) < 1e-12),
     'o grafico da Selic desenha a resposta calculada');
  ok(ctx.IRF.alvo === IR.padrao.alvo && ctx.IRF.chq[IR.padrao.alvo].rho === IR.padrao.rho,
     'a aba abre no choque padrao do payload');

  // A faixa e medida contra o cenario do MESMO desenho: com o choque zero ela fecha em zero.
  {
    ctx.IRF.chq[ctx.IRF.alvo].v = 0;
    const r0 = ctx.irfCalcular();
    const larg = Math.max(...Object.keys(r0.faixa).map((nm) =>
      Math.max(...r0.faixa[nm].hi.map((x, k) => Math.abs(x) + Math.abs(r0.faixa[nm].lo[k])))));
    ok(larg < 1e-6, 'com choque zero a faixa inteira e zero -- base e choque com os mesmos pesos',
       larg.toExponential(2));
    ctx.IRF.chq[ctx.IRF.alvo].v = IR.padrao.v;
    ctx.renderIrf();
  }

  // O seletor de inflacao troca os graficos de inflacao, e so eles.
  const selAntes = PLOT['ch-irf-selic'].traces[2].y.slice();
  document.getElementById('irfPill12').dispatch('click');
  ok(PLOT['ch-irf-infl'].traces[2].y.every((x, k) => Math.abs(x - ctx.IRF._ult.med.infl12[k]) < 1e-12)
       && /12 meses/.test(document.getElementById('ch-irf-infl').parentNode._chFrame.title.textContent),
     'em 12 meses o grafico do IPCA desenha o acumulado, e o titulo diz');
  ok(PLOT['ch-irf-g-IS'].traces[2].y.every((x, k) =>
       Math.abs(x - ctx.IRF._ult.med['g12:IS'][k]) < 1e-12),
     'e os quatro grupos tambem');
  ok(PLOT['ch-irf-selic'].traces[2].y.every((x, k) => x === selAntes[k]),
     'e a Selic nao muda');
  document.getElementById('irfPillTri').dispatch('click');

  // Trocar o alvo pela barra recalcula, e o subtitulo passa a nomear o novo.
  const bar = document.getElementById('irfBar');
  bar.dispatch('change', { target: { getAttribute: () => 'alvo', value: 'ffr' } });
  ok(ctx.IRF.alvo === 'ffr' && ctx.IRF._ult.alvo.key === 'ffr', 'trocar o alvo recalcula');
  ok(document.getElementById('ch-irf-de').parentNode._chFrame.sub.textContent
       .indexOf(D.sim.var.ffr.nome_frase) >= 0,
     'e o subtitulo passa a nomear o choque novo');
  ok(ctx.IRF._ult.med.de[h - 1] > 0,
     'Fed Funds mais alto desvaloriza o real (o carry encolhe)', ctx.fmt(ctx.IRF._ult.med.de[h - 1], 3));

  // O aviso do residuo permanente: so onde ele vale, com o numero derivado.
  bar.dispatch('change', { target: { getAttribute: () => 'alvo', value: 'res:R' } });
  bar.dispatch('change', { target: { getAttribute: () => 'tipo', value: 'rampa' } });
  const av = document.getElementById('irfAviso');
  const mR = 1 / (1 - D.sim.eq.R.mediana.t1 - D.sim.eq.R.mediana.t2);
  ok(av.style.display !== 'none' && av.innerHTML.indexOf(ctx.fmt(mR, 1) + ' vezes') >= 0,
     'um residuo permanente na regra avisa quanto ele acumula, derivado dos pesos', av.innerHTML);
  bar.dispatch('change', { target: { getAttribute: () => 'tipo', value: 'decai' } });
  ok(av.style.display === 'none', 'e o aviso some com o decaimento');
  bar.dispatch('change', { target: { getAttribute: () => 'rho', value: '1,5' } });
  ok(ctx.IRF.chq['res:R'].rho === 1, 'a sobra e limitada a 1, e a virgula e lida');
  bar.dispatch('change', { target: { getAttribute: () => 'rho', value: String(IR.padrao.rho) } });
}

// ── Fim ───────────────────────────────────────────────────────────────────────
console.log('\n' + '='.repeat(62));
console.log(oks + ' ok, ' + falhas + ' falharam');
process.exit(falhas ? 1 : 0);
