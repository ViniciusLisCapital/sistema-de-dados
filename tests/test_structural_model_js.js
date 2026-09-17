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
['hdrBadge', 'hdrDate', 'eqBox', 'introNota', 'flagAberto', 'chartGrid',
 'tblPainel', 'tblNota', 'foldTabela', 'ftr'].forEach((id) => {
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
secao('2. Os quatro graficos plotam as series certas');
const ESPERADO = {
  'ch-infl': ['ipca_12m', 'pi_e'],
  'ch-hiato': ['hiato'],
  'ch-cambio': ['de'],
  'ch-icbr': ['pi_star_usd'],
};
ok(Object.keys(PLOT).length === 4, 'quatro graficos plotados', 'plotou ' + Object.keys(PLOT).join(','));
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
  'ch-infl': 'variação do IPCA em 12 meses, %',
  'ch-hiato': 'produto efetivo − potencial, % do potencial',
  'ch-cambio': 'variação da taxa média do trimestre, %',
  'ch-icbr': 'variação da média do trimestre, %',
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
const derivados = {
  introNota: document.getElementById('introNota').textContent,
  tblNota: document.getElementById('tblNota').textContent,
  flagAberto: document.getElementById('flagAberto').textContent,
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

// ── Fim ───────────────────────────────────────────────────────────────────────
console.log('\n' + '='.repeat(62));
console.log(oks + ' ok, ' + falhas + ' falharam');
process.exit(falhas ? 1 : 0);
