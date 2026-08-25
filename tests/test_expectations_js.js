// Testa o esqueleto JS do Panorama de Expectativas (Focus), executando o script REAL do
// HTML gerado contra um DOM stub e um Plotly stub.
//
// Roda com:
//     node tests/test_expectations_js.js
//
// Precisa de "reports/brasil/Expectations.html" gerado:
//     uv run python analytics/brasil/expectations/generate_report.py
//
// Por que um harness e nao `node --check`: este projeto ja teve dois bugs de dashboard
// chegarem em producao passando por checagem de sintaxe (ver .claude/rules/lis-dashboards.md,
// "Quick-range buttons") -- o que falhou nos dois casos foi o COMPORTAMENTO do clique, nao a
// sintaxe.
//
// O que este relatorio tem de proprio, e que concentra os testes:
//   (a) o payload e COMPRIMIDO -- cada serie e {i0, m[], s[], n[]} sobre uma grade semanal
//       global. Se blkSerie/blkAt errarem o offset, todo numero do relatorio sai deslocado no
//       tempo sem nenhum erro aparecer;
//   (b) "ha 4 semanas" anda por DATA, nao por contagem de pontos da grade -- e a diferenca
//       aparece justamente nas semanas de feriado, que sao as que ninguem testa a mao;
//   (c) a ordem cronologica das reunioes do Copom nao e alfabetica ("R10/2027" ordenaria
//       antes de "R2/2027") e nao ha calendario do Copom no payload.
//
// O que ele NAO substitui: confirmacao visual num browser real.

const fs = require('fs');
const path = require('path');

const HTML = path.join(__dirname, '..', 'reports', 'brasil', 'Expectations.html');
if (!fs.existsSync(HTML)) {
  console.error('reports/brasil/Expectations.html nao existe -- gere o relatorio primeiro:');
  console.error('  uv run python analytics/brasil/expectations/generate_report.py');
  process.exit(1);
}
const blocos = fs.readFileSync(HTML, 'utf8').match(/<script>([\s\S]*?)<\/script>/g) || [];
if (!blocos.length) { console.error('nenhum <script> encontrado no HTML'); process.exit(1); }
const SRC = blocos[blocos.length - 1].replace(/^<script>/, '').replace(/<\/script>$/, '');

// Ids duplicados: o stub de DOM nao pega (ele guarda um elemento por id), mas o browser
// devolve o PRIMEIRO do documento. Uma <table id="tab-boletim"> convivendo com o painel
// <div id="tab-boletim"> fez getElementById devolver o painel -- a tabela seria escrita
// por cima da aba inteira. Por isso a checagem e feita no HTML cru, antes de tudo.
const IDS = (fs.readFileSync(HTML, 'utf8').match(/ id="[^"]+"/g) || []).map((s) => s.trim());
const vistos = {}, duplicados = [];
IDS.forEach((id) => { if (vistos[id]) duplicados.push(id); vistos[id] = true; });

let falhas = 0;
function ok(cond, nome, detalhe) {
  if (cond) { console.log('  ok   ' + nome); }
  else { falhas++; console.log('  FALHA ' + nome + (detalhe ? '  -- ' + detalhe : '')); }
}

// ── DOM stub ──────────────────────────────────────────────────────────────────
function El(tag) {
  this.tag = tag || 'div';
  this.children = []; this.style = {}; this.dataset = {};
  this._className = ''; this.textContent = ''; this.value = '';
  this._html = ''; this._listeners = {}; this._plotly = {};
  this._inputs = [];
  this.parentNode = null; this.previousElementSibling = null;
  const self = this;
  this.classList = {
    _set: {},
    add(c) { self.classList._set[c] = true; self._syncClass(); },
    remove(c) { delete self.classList._set[c]; self._syncClass(); },
    contains(c) { return !!self.classList._set[c]; },
    toggle(c, force) {
      const on = force === undefined ? !self.classList._set[c] : !!force;
      if (on) self.classList._set[c] = true; else delete self.classList._set[c];
      self._syncClass();
      return on;
    },
  };
}
El.prototype._syncClass = function () { this._className = Object.keys(this.classList._set).join(' '); };
// className e classList tem que ficar em sincronia nas DUAS direcoes: o script atribui
// `el.className = 'ctrl-bar period-ctrl-bar'` direto e depois consulta
// `el.classList.contains('period-ctrl-bar')`.
Object.defineProperty(El.prototype, 'className', {
  get() { return this._className; },
  set(v) {
    this._className = v;
    this.classList._set = {};
    String(v).split(/\s+/).filter(Boolean).forEach((c) => { this.classList._set[c] = true; });
  },
});
El.prototype.appendChild = function (c) { c.parentNode = this; this.children.push(c); return c; };
El.prototype.insertBefore = function (novo, ref) {
  novo.parentNode = this;
  const i = this.children.indexOf(ref);
  this.children.splice(i < 0 ? this.children.length : i, 0, novo);
  if (ref) ref.previousElementSibling = novo;
  return novo;
};
El.prototype.removeChild = function (c) {
  const i = this.children.indexOf(c);
  if (i >= 0) this.children.splice(i, 1);
  c.parentNode = null;
  return c;
};
El.prototype.addEventListener = function (k, f) { (this._listeners[k] = this._listeners[k] || []).push(f); };
El.prototype.fire = function (k, ev) { (this._listeners[k] || []).forEach((f) => f(ev)); };
El.prototype.on = function (k, f) { (this._plotly[k] = this._plotly[k] || []).push(f); };
El.prototype.emit = function (k, ev) { (this._plotly[k] || []).forEach((f) => f(ev)); };
El.prototype.closest = function () { return this._closest || null; };
El.prototype.contains = function () { return false; };
El.prototype.querySelector = function (sel) {
  const m = /^\[data-role=([a-z]+)\]$/.exec(sel);
  if (m) return this._roles ? this._roles[m[1]] : null;
  return null;
};
El.prototype.querySelectorAll = function (sel) {
  if (sel === '.pill') return this.children.filter((c) => c.classList.contains('pill'));
  // O multiselect e montado por innerHTML e depois lido com querySelectorAll('input:checked');
  // sem parsear os <input> o stub devolveria "nada selecionado" e os renderizadores
  // desenhariam graficos vazios -- que e exatamente o que este harness precisa exercitar.
  if (sel === 'input:checked') return this._inputs.filter((i) => i.checked);
  if (sel === 'input') return this._inputs;
  return [];
};
Object.defineProperty(El.prototype, 'innerHTML', {
  get() { return this._html; },
  set(v) {
    this._html = v; this.children = [];
    this._roles = {};
    if (/data-role="quick"/.test(v))  this._roles.quick = new El('div');
    if (/data-role="from"/.test(v))   this._roles.from = new El('select');
    if (/data-role="to"/.test(v))     this._roles.to = new El('select');
    this._inputs = [];
    const re = /<input type="checkbox" value="([^"]*)"( checked)?>/g;
    let m;
    while ((m = re.exec(v)) !== null) this._inputs.push({ value: m[1], checked: !!m[2] });
  },
});

const ABAS = ['boletim', 'revisao', 'copom', 'movel', 'trajetoria', 'dispersao', 'bases', 'appendix'];
function makeDom() {
  const els = {};
  const tabBtns = ABAS.map((t) => { const b = new El('button'); b.dataset.tab = t; return b; });
  const tabPanels = ABAS.map((t) => { const p = new El('div'); p.id = 'tab-' + t; return p; });
  const doc = {
    getElementById(id) {
      if (!els[id]) {
        const el = new El('div');
        el.id = id;
        // Todo div de grafico precisa da arvore que _ensurePeriodSelector espera:
        // <pai> > .chart-card > #chart-*
        if (/^chart-/.test(id)) {
          const card = new El('div'); card.classList.add('chart-card');
          const pai = new El('div');
          pai.appendChild(card); card.appendChild(el);
          el._closest = card;
        }
        els[id] = el;
      }
      return els[id];
    },
    createElement: (t) => new El(t),
    querySelector(sel) {
      if (sel === 'main') return new El('main');
      const m = /^\.period-ctrl-bar\[data-for="(.+)"\]$/.exec(sel);
      if (m) {
        const chart = els[m[1]];
        if (!chart || !chart._closest || !chart._closest.parentNode) return null;
        return chart._closest.parentNode.children.find((c) => c.classList.contains('period-ctrl-bar')) || null;
      }
      return null;
    },
    querySelectorAll(sel) {
      if (sel === '.tab-btn') return tabBtns;
      if (sel === '.tab-panel') return tabPanels;
      return [];
    },
    addEventListener() {},
    _els: els, _tabBtns: tabBtns, _tabPanels: tabPanels,
  };
  return doc;
}

// ── Plotly stub ───────────────────────────────────────────────────────────────
function makePlotly(doc, chamadas) {
  function thenable(v) { return { then(f) { f(v); return thenable(v); }, catch() { return thenable(v); } }; }
  return {
    react(divId, traces, layout) {
      chamadas.push({ tipo: 'react', divId, traces, layout });
      const el = doc.getElementById(divId);
      el.data = traces;
      // O Plotly resolve o layout em _fullLayout (com xaxis.type detectado); e de la que o
      // y_autofit.js le -- ler de el.layout tem a precedencia invertida e ja foi bug.
      el._fullLayout = JSON.parse(JSON.stringify(layout));
      el._fullLayout.xaxis = el._fullLayout.xaxis || {};
      if (!el._fullLayout.xaxis.type) el._fullLayout.xaxis.type = 'date';
      return thenable(el);
    },
    relayout(divId, upd) {
      chamadas.push({ tipo: 'relayout', divId, upd });
      return thenable(doc.getElementById(divId));
    },
    newPlot() { throw new Error('newPlot nao deve ser chamado -- use _reactPreserveX/_reactPlain'); },
  };
}

// ── Execucao ──────────────────────────────────────────────────────────────────
const doc = makeDom();
const chamadas = [];
global.document = doc;
global.window = {};
global.Option = function (label, value) { const o = new El('option'); o.textContent = label; o.value = value; return o; };
global.Plotly = makePlotly(doc, chamadas);

const EXPORTS = ['D', 'GRADE', 'NG', 'SNAPS', 'RENDERERS', 'activateTab',
                 'fmtBR', 'fmtTrunc', 'fmtSig', 'clsDelta', 'fmtDataBR', 'dlText', 'lineTrace', 'barTrace',
                 'gidxOnOrBefore', 'gidxBackWeeks', 'snapGi', 'blkSerie', 'blkAt', 'pBlk', 'pMeta',
                 'movBlk', 'indsDe', 'difSemanas', '_quickRangeOptions', '_defaultXRange',
                 '_traceAllDates', 'mkTsLayout', 'mkCatLayout', '_reactPreserveX', '_reactPlain',
                 '_resetChartAxis', '_PLOTLY_CONFIG', '_parseReuniao', '_copCurva', '_copMatriz',
                 '_bolLinha', '_traFoto', '_mesesAte', '_movIndicadores', '_disBloco', '_copCategorias', 'vigenteOuFuturo', '_fimPeriodo',
                 'ordemCronologica'];
let R;
try {
  new Function(SRC + ';global.__R = {' + EXPORTS.join(',') + '};')();
  R = global.__R;
} catch (e) {
  console.error('o script do relatorio lancou excecao ao carregar: ' + e.stack);
  process.exit(1);
}

console.log('\n1. Carga, abas e payload');
ok(!!R, 'script executa sem excecao');
ok(duplicados.length === 0, 'nenhum id duplicado no HTML gerado', duplicados.join(', '));
ok(Object.keys(R.RENDERERS).sort().join(',') === ABAS.slice().sort().join(','),
   'RENDERERS tem as 8 abas', JSON.stringify(Object.keys(R.RENDERERS)));
ok(doc._tabPanels[0].classList.contains('active'), 'aba inicial (boletim) ativa no load');
ok(doc._els['generated-at'].textContent !== '', 'generated_at escrito no header');
ok(doc._els['hdr-ultima'].textContent === R.fmtDataBR(R.GRADE[R.NG - 1]),
   'header mostra a ultima data da grade', doc._els['hdr-ultima'].textContent);
// Escopo: so as tres tabelas do Focus. Qualquer grupo novo em D e sinal de que alguem
// trouxe fonte de fora sem atualizar o Apendice.
ok(Object.keys(R.D).sort().join(',') === 'cobertura,copom,generated_at,indice,meta,movel,periodo',
   'payload tem so os grupos do Focus (nada de meta/realizado)', Object.keys(R.D).sort().join(','));
ok(R.NG > 1000 && R.GRADE[0] < R.GRADE[R.NG - 1], 'grade semanal ordenada e longa', R.NG + ' semanas');

console.log('\n2. Grade semanal: busca por data, nao por posicao');
const ultima = R.GRADE[R.NG - 1];
ok(R.gidxOnOrBefore(ultima) === R.NG - 1, 'gidxOnOrBefore acha a ultima data exata');
ok(R.gidxOnOrBefore('1900-01-01') === -1, 'data anterior a toda a grade devolve -1');
ok(R.gidxOnOrBefore('2999-01-01') === R.NG - 1, 'data futura cai na ultima semana');
// A grade e semanal, entao "ha 4 semanas" tem que cair entre 28 e ~42 dias atras -- nunca
// menos que 28, que e o erro que aparece quando se conta posicoes em vez de datas.
[1, 4, 12, 52].forEach((w) => {
  const gi = R.gidxBackWeeks(w);
  const dias = (Date.parse(ultima) - Date.parse(R.GRADE[gi])) / 86400000;
  ok(dias >= w * 7 && dias <= w * 7 + 21,
     `gidxBackWeeks(${w}) cai entre ${w * 7} e ${w * 7 + 21} dias atras`, dias + 'd');
});
ok(R.gidxBackWeeks(0) === R.NG - 1, 'gidxBackWeeks(0) e a semana corrente');
ok(R.SNAPS.length === 7 && R.SNAPS[0].key === 'w0' && R.SNAPS.every((s) => s.gi >= 0),
   'os 7 snapshots resolvidos na grade', JSON.stringify(R.SNAPS.map((s) => s.data)));

console.log('\n3. Blocos comprimidos: offset e alinhamento');
const blkIpca = R.pBlk('anual', 'IPCA|', '2026');
ok(!!blkIpca, 'serie anual IPCA|2026 existe no store');
const sIpca = R.blkSerie(blkIpca, 'm');
ok(sIpca.dates.length === blkIpca.m.length, 'blkSerie devolve um ponto por posicao do bloco');
ok(sIpca.dates[0] === R.GRADE[blkIpca.i0], 'primeira data do bloco = GRADE[i0]', sIpca.dates[0]);
ok(sIpca.dates[sIpca.dates.length - 1] === R.GRADE[blkIpca.i0 + blkIpca.m.length - 1],
   'ultima data do bloco confere com i0 + tamanho');
// blkAt e blkSerie tem que concordar em toda posicao -- e o par que sustenta todo numero
// mostrado no relatorio.
let divergencias = 0;
for (let i = 0; i < sIpca.dates.length; i += 7) {
  const gi = R.gidxOnOrBefore(sIpca.dates[i]);
  if (R.blkAt(blkIpca, 'm', gi) !== sIpca.values[i]) divergencias++;
}
ok(divergencias === 0, 'blkAt(gi) == blkSerie[i] em toda amostra', String(divergencias));
ok(R.blkAt(blkIpca, 'm', blkIpca.i0 - 1) === null, 'antes do inicio do bloco devolve null');
ok(R.blkAt(blkIpca, 'm', R.NG + 500) === null, 'depois do fim do bloco devolve null');
ok(R.blkAt(undefined, 'm', 0) === null, 'bloco inexistente devolve null em vez de estourar');
ok(R.blkAt(blkIpca, 'inexistente', R.NG - 1) === null, 'estatistica inexistente devolve null');
// O IPCA para 2026 ficou ancorado em 3,00% por anos antes de subir: o store tem que
// preservar isso, e nao ser um artefato de arredondamento.
const ipcaHoje = R.blkAt(blkIpca, 'm', R.NG - 1);
ok(ipcaHoje > 2 && ipcaHoje < 12, 'IPCA 2026 hoje em faixa plausivel', String(ipcaHoje));

console.log('\n4. difSemanas: janela alinhada pela grade');
const serieTeste = { dates: R.GRADE.slice(R.NG - 30), values: R.GRADE.slice(R.NG - 30).map((_, i) => i * 1.0) };
const dif = R.difSemanas(serieTeste, 4);
ok(dif.dates.length === serieTeste.dates.length, 'difSemanas preserva o comprimento');
const ultDif = dif.values[dif.values.length - 1];
ok(ultDif === 4 || ultDif === 5, 'variacao de 4 semanas numa serie linear e ~4', String(ultDif));
ok(dif.values[0] === null, 'primeiro ponto nao tem par 4 semanas atras -> null');

console.log('\n5. Copom: ordem cronologica das reunioes');
ok(R._parseReuniao('R6/2026').ord < R._parseReuniao('R1/2027').ord,
   'R6/2026 vem antes de R1/2027 (ano manda)');
// "R10/2027" nao existe hoje, mas ordenar por string quebraria se a numeracao passasse de 9.
ok(R._parseReuniao('R2/2027').ord < R._parseReuniao('R10/2027').ord,
   'R2/2027 vem antes de R10/2027 (numerico, nao alfabetico)');
ok(R._parseReuniao('R6/2026').label === 'R6/26', 'rotulo curto para o eixo', R._parseReuniao('R6/2026').label);
ok(R._parseReuniao('lixo') === null, 'string invalida nao vira reuniao');
const curva = R._copCurva(R.NG - 1, '0');
ok(curva.length >= 8, 'curva de hoje tem pelo menos 8 reunioes cotadas', String(curva.length));
let ordenada = true;
for (let i = 1; i < curva.length; i++) if (curva[i].ord <= curva[i - 1].ord) ordenada = false;
ok(ordenada, 'curva devolvida em ordem cronologica estrita');
ok(curva.every((c) => c.valor > 0 && c.valor < 60), 'Selic esperada em faixa plausivel',
   JSON.stringify([curva[0].valor, curva[curva.length - 1].valor]));
const M0 = R._copMatriz('0');
ok(M0.hz.length === 20 && M0.hz[0].length === R.NG, 'matriz horizonte x grade no tamanho certo');
ok(M0.hz[0][R.NG - 1] === curva[0].valor, '1a linha da matriz = 1a reuniao da curva');
ok(M0.ultima[R.NG - 1] === curva[curva.length - 1].valor, 'linha "ultima cotada" = fim da curva');
ok(M0.cotadas[R.NG - 1] === curva.length, 'contagem de reunioes cotadas bate');
// A aba Dispersao oferece a metrica "amplitude" para a fonte Copom; ela le lo/hi da
// matriz, entao a matriz tem de carregar as duas -- ja faltaram.
ok(M0.lo[0][R.NG - 1] != null && M0.hi[0][R.NG - 1] != null
   && M0.hi[0][R.NG - 1] >= M0.lo[0][R.NG - 1],
   'matriz do Copom carrega minimo e maximo (max >= min)',
   JSON.stringify([M0.lo[0][R.NG - 1], M0.hi[0][R.NG - 1]]));
// A base 1 da Selic so comeca em 2021-03-31 -- e propriedade da fonte, nao falha de carga.
const M1 = R._copMatriz('1');
let primeiraB1 = null;
for (let i = 0; i < R.NG; i++) if (M1.hz[0][i] != null) { primeiraB1 = R.GRADE[i]; break; }
ok(primeiraB1 >= '2021-03-01', 'base 1 do Copom nao inventa historico antes de 2021-03', String(primeiraB1));

console.log('\n6. Boletim: linha da tabela = mediana + variacoes');
const linhaIpca = R._bolLinha({ key: 'IPCA|', label: 'IPCA', familia: 'Inflação', meta: R.pMeta('anual', 'IPCA|') });
ok(!!linhaIpca, '_bolLinha monta a linha do IPCA');
ok(linhaIpca.hoje === R.blkAt(blkIpca, 'm', R.NG - 1), 'coluna "hoje" le a ultima semana da grade');
[1, 4, 12, 52].forEach((w) => {
  const esperado = linhaIpca['v' + w] == null ? null
    : Math.round((linhaIpca.hoje - linhaIpca['v' + w]) * 10000) / 10000;
  ok(linhaIpca['d' + w] === esperado, `delta de ${w} semana(s) = hoje - passado`, String(linhaIpca['d' + w]));
});
ok(linhaIpca.n > 0, 'numero de respondentes vem junto', String(linhaIpca.n));
ok(R.clsDelta(0.5) === 'up' && R.clsDelta(-0.5) === 'down' && R.clsDelta(0) === 'flat'
   && R.clsDelta(null) === 'flat', 'classe de cor por direcao (e neutra para nulo)');
ok(R.fmtSig(0.5, 2) === '+0,50' && R.fmtSig(-0.5, 2) === '-0,50', 'delta assinado em formato BR');

console.log('\n7. Trajetoria: fotografia da curva a frente');
// _traFoto depende do estado global _traPer/_traInd; renderTrajetoria e quem os define.
R.RENDERERS.trajetoria();
const foto = R._traFoto(R.NG - 1);
ok(foto.dates.length > 6, 'fotografia mensal de hoje tem varios meses a frente', String(foto.dates.length));
let crescente = true;
for (let i = 1; i < foto.dates.length; i++) if (foto.dates[i] <= foto.dates[i - 1]) crescente = false;
ok(crescente, 'periodos de referencia em ordem crescente');
ok(foto.dates[0] >= '2015-01-01', 'store mensal comeca no corte declarado', foto.dates[0]);
ok(R._mesesAte('2026-08-21', '2027-08-01') === 11.5,
   'meses ate o periodo desconta meia unidade quando a pesquisa e no fim do mes',
   String(R._mesesAte('2026-08-21', '2027-08-01')));
ok(R._mesesAte('2026-08-07', '2026-08-01') === 0, 'pesquisa dentro do proprio mes de referencia -> 0');

console.log('\n7b. Ordem cronologica dos periodos de referencia');
// data_referencia mensal vem no formato do BCB ("MM/YYYY"): .sort() de string poe
// "01/2027" antes de "12/2026". A ordem correta e a posicao em meta.refs, que o gerador
// ordenou por ref_date. Foi bug real, pego pelo teste de dados antes de chegar na tela.
const metaMensal = R.pMeta('mensal', 'IPCA|');
ok(!!metaMensal, 'indice mensal do IPCA existe');
const refsMensais = metaMensal.refs;
let cronologico = true;
for (let i = 1; i < metaMensal.refDates.length; i++) {
  if (metaMensal.refDates[i] < metaMensal.refDates[i - 1]) cronologico = false;
}
ok(cronologico, 'meta.refs ja vem ordenado por ref_date do gerador');
const embaralhado = [refsMensais[5], refsMensais[0], refsMensais[3]];
ok(JSON.stringify(R.ordemCronologica(metaMensal, embaralhado))
   === JSON.stringify([refsMensais[0], refsMensais[3], refsMensais[5]]),
   'ordemCronologica reordena pela posicao em meta.refs',
   JSON.stringify(R.ordemCronologica(metaMensal, embaralhado)));
// A prova de que .sort() nao serviria: alguma janela de 13 meses tem que discordar.
let discorda = false;
for (let i = 0; i + 13 < refsMensais.length && !discorda; i++) {
  const janela = refsMensais.slice(i, i + 13);
  if (JSON.stringify(janela.slice().sort()) !== JSON.stringify(janela)) discorda = true;
}
ok(discorda, 'sort() de string DIVERGE da ordem cronologica no store mensal');

console.log('\n7c. Correcoes da revisao de 2026-08-24');
// (1) Eixo da curva do Copom. Uma curva antiga cota reunioes que ja passaram; como sao
// categorias novas para o eixo, o Plotly as jogava para o FIM, depois de R5/28. O
// categoryarray tem de ser a uniao ordenada por (ano, numero).
const curvaHoje = R._copCurva(R.NG - 1, '0');
const curva12 = R._copCurva(R.gidxBackWeeks(12), '0');
const cats = R._copCategorias([curvaHoje, curva12]);
ok(cats.length >= curvaHoje.length, 'categoryarray cobre as duas curvas', String(cats.length));
const todas = {};
curvaHoje.concat(curva12).forEach((o) => { todas[o.label] = o.ord; });
let catsOrdenado = true;
for (let i = 1; i < cats.length; i++) if (todas[cats[i]] <= todas[cats[i - 1]]) catsOrdenado = false;
ok(catsOrdenado, 'categoryarray em ordem cronologica estrita', cats.join(' '));
ok(Object.keys(todas).length === cats.length, 'sem categoria repetida no eixo');
// A prova do bug: alguma reuniao da curva antiga tem de vir ANTES da primeira de hoje.
const soAntigas = curva12.filter((o) => !curvaHoje.some((h) => h.label === o.label));
if (soAntigas.length) {
  ok(cats.indexOf(soAntigas[0].label) < cats.indexOf(curvaHoje[0].label),
     'reuniao que so a curva antiga cota fica a ESQUERDA (era o bug: ia para o fim)',
     soAntigas[0].label + ' em ' + cats.indexOf(soAntigas[0].label)
       + ' vs ' + curvaHoje[0].label + ' em ' + cats.indexOf(curvaHoje[0].label));
} else {
  ok(false, 'esperava reunioes so na curva de 12 semanas atras para exercitar o caso');
}

// (2) Periodo "vigente ou futuro" pelo FIM, nao pelo comeco. Em agosto de 2026 o ano
// corrente TEM de contar -- comparar pelo ref_date (01/01) o excluia desde fevereiro.
ok(R.vigenteOuFuturo('anual', '2026-01-01', '2026-08-21') === true,
   'ano corrente conta como vigente em agosto');
ok(R.vigenteOuFuturo('anual', '2025-01-01', '2026-08-21') === false, 'ano passado nao conta');
ok(R.vigenteOuFuturo('mensal', '2026-08-01', '2026-08-21') === true, 'mes corrente conta');
ok(R.vigenteOuFuturo('mensal', '2026-07-01', '2026-08-21') === false, 'mes passado nao conta');
ok(R.vigenteOuFuturo('trimestral', '2026-07-01', '2026-08-21') === true, 'trimestre corrente conta');
ok(R.vigenteOuFuturo('trimestral', '2026-04-01', '2026-08-21') === false, 'trimestre passado nao conta');
ok(R._fimPeriodo('anual', '2026-01-01') === '2027-01-01', 'fim do ano de referencia',
   R._fimPeriodo('anual', '2026-01-01'));
ok(R._fimPeriodo('trimestral', '2026-10-01') === '2027-01-01', 'fim do 4o trimestre vira o ano',
   R._fimPeriodo('trimestral', '2026-10-01'));

console.log('\n8. Renderizadores rodam contra o payload real');
ABAS.forEach((aba) => {
  chamadas.length = 0;
  let erro = null;
  try { R.RENDERERS[aba](); } catch (e) { erro = e; }
  const reacts = chamadas.filter((c) => c.tipo === 'react');
  ok(!erro, 'render de "' + aba + '" nao lanca excecao', erro ? erro.message : '');
  if (aba === 'appendix') {
    ok(doc._els['tbl-cobertura'].innerHTML.indexOf('<tbody>') > 0, 'appendix monta a tabela de cobertura');
  } else {
    ok(reacts.length > 0, 'render de "' + aba + '" desenha pelo menos um grafico', String(reacts.length));
    const comDados = reacts.filter((c) => c.traces.length > 0 && (c.traces[0].y || []).length > 0);
    ok(comDados.length > 0, 'render de "' + aba + '" desenha com dado, nao vazio',
       reacts.map((c) => c.divId + ':' + c.traces.length).join(' '));
  }
});
ok(doc._els['tbl-boletim'].innerHTML.indexOf('fam-row') > 0, 'tabela do Boletim agrupa por familia');
ok(doc._els['bol-lead'].innerHTML.indexOf('indicadores cotam') > 0, 'lead do Boletim preenchido');
ok(doc._els['kpi-cop-prox-v'].textContent !== '—', 'KPI da proxima reuniao preenchido',
   doc._els['kpi-cop-prox-v'].textContent);
ok(doc._els['kpi-mov-12-v'].textContent.indexOf('%') > 0, 'KPI do IPCA 12m preenchido',
   doc._els['kpi-mov-12-v'].textContent);
ok(doc._els['kpi-bas-gap-v'].textContent.indexOf('p.p.') > 0, 'KPI do gap entre bases preenchido',
   doc._els['kpi-bas-gap-v'].textContent);

console.log('\n8b. Efeito das correcoes depois de renderizar');
// (3) O KPI da Revisao descreve o periodo MAIS PROXIMO selecionado -- com a correcao (2),
// o padrao passa a incluir o ano corrente, entao o rotulo tem de citar o ano de hoje.
const anoHoje = R.GRADE[R.NG - 1].slice(0, 4);
ok(doc._els['kpi-rev-hoje-l'].textContent === 'Mediana para ' + anoHoje,
   'KPI da Revisao abre no ano corrente, nao no mais distante',
   doc._els['kpi-rev-hoje-l'].textContent);

// (4) Δ 4 semanas do Copom compara a MESMA reuniao. Recalcula do payload e confere o texto.
const cHoje = R._copCurva(R.NG - 1, '0');
const gi4 = R.gidxBackWeeks(4);
const mesmaProx = R.blkAt(R.D.copom[cHoje[0].reuniao + '|0'], 'm', gi4);
ok(mesmaProx != null, 'a proxima reuniao ja era cotada 4 semanas atras', String(mesmaProx));
const espProx = R.fmtSig(cHoje[0].valor - mesmaProx, 2) + ' p.p. em 4 semanas';
ok(doc._els['kpi-cop-prox-s'].textContent === espProx,
   'sub do KPI da proxima reuniao usa a mesma reuniao, nao o 1o horizonte de entao',
   doc._els['kpi-cop-prox-s'].textContent + '  esperado: ' + espProx);

// (5) O titulo do eixo Y do horizonte movel segue o horizonte escolhido -- clicando na
// pill de verdade, nao inspecionando a definicao dela.
chamadas.length = 0;
const pillsHz = doc._els['pg-mov-hz'].children;
ok(pillsHz.length === 2, 'as duas pills de horizonte existem', String(pillsHz.length));
pillsHz[1].fire('click');
const reactMov = chamadas.filter((c) => c.tipo === 'react' && c.divId === 'chart-mov').pop();
ok(reactMov && reactMov.layout.yaxis.title.text === '% em 24 meses',
   'clicar em "24 meses" muda o titulo do eixo Y',
   reactMov ? reactMov.layout.yaxis.title.text : '-');
pillsHz[0].fire('click');

// (6) A Trajetoria mantem a view inicial justa: passar um xaxis inteiro no `extra`
// apagava o range que mkTsLayout calcula, e o grafico abria com o autopad do Plotly.
chamadas.length = 0;
R.RENDERERS.trajetoria();
const reactTra = chamadas.filter((c) => c.tipo === 'react' && c.divId === 'chart-tra').pop();
ok(reactTra && reactTra.layout.xaxis.autorange === false && !!reactTra.layout.xaxis.range,
   'chart-tra abre com range explicito',
   reactTra ? JSON.stringify(reactTra.layout.xaxis.range) : '-');
ok(reactTra && reactTra.layout.xaxis.title.text === 'Período de referência',
   'e o titulo do eixo X sobrevive ao merge');

// (7) Destaque na fotografia mais recente SELECIONADA, mesmo sem "Hoje" marcado.
const traces0 = reactTra ? reactTra.traces : [];
ok(traces0.length && traces0[0].line.dash === 'solid' && traces0.slice(1).every((t) => t.line.dash === 'dot'),
   'so a primeira fotografia e solida', traces0.map((t) => t.line.dash).join(','));

console.log('\n9. Layout: pan nos dois eixos, view inicial justa');
const S = { dates: ['2024-03-01', '2024-06-01', '2024-09-01', '2024-12-01', '2025-03-01'],
            values: [1.5, 2.25, null, 3.75, 4.0] };
const tr = R.lineTrace(S, 'Serie', '#1F2853', false, 2, '%');
const layout = R.mkTsLayout('%', 520, [tr]);
ok(layout.dragmode === 'pan', 'dragmode pan (arrastar move, nao faz box-zoom)');
ok(R._PLOTLY_CONFIG.scrollZoom === true, 'scrollZoom ligado');
ok(!('fixedrange' in layout.yaxis) && !('fixedrange' in layout.xaxis), 'nenhum eixo com fixedrange');
ok(layout.hovermode === 'x unified' && layout.hoverlabel.bgcolor === '#1F2853', 'tooltip unificado navy');
const xr = layout.xaxis.range;
ok(layout.xaxis.autorange === false && xr[0] < '2024-03-01' && xr[1] > '2025-03-01',
   'range inicial ancorado no dado real', JSON.stringify(xr));
ok((Date.parse(xr[1]) - Date.parse(xr[0])) / 86400000 < 400, 'folga de ~2%, nao o autopad do Plotly');
ok(R.mkCatLayout('%', 520).xaxis.range === undefined, 'mkCatLayout nao inventa range de data');
const comLabel = R.lineTrace(S, 'Serie', '#1F2853', true, 2, '%');
ok(tr.text === undefined && comLabel.mode.indexOf('text') > 0, 'toggle de labels muda o modo do trace');
ok(comLabel.text[2] === '', 'ponto nulo nao recebe label');
ok(tr.connectgaps === false, 'buracos nao sao costurados (serie encerrada nao vira linha reta)');
ok(tr.customdata[1] === '2,25', 'hover em formato BR via customdata', tr.customdata[1]);
ok(R.fmtTrunc(16.951, 1) === '16,9', 'fmtTrunc TRUNCA (nao arredonda)', R.fmtTrunc(16.951, 1));
ok(R.dlText(Array.from({ length: 100 }, (_, i) => i + 0.5), 1, '%').filter((s) => s !== '').length === 21,
   '>60 pontos -> 1 em 5 (+ o ultimo)');

console.log('\n10. Presets de range: ancoragem no ultimo ponto REAL');
const datas = R._traceAllDates([tr]);
const presets = R._quickRangeOptions(datas);
ok(presets.map((p) => p.label).join(',') === '1a,3a,5a,10a,Tudo', 'os 5 presets na ordem');
ok(presets.every((p) => p.to === '2025-03-01'), 'todo preset termina na ULTIMA data real',
   JSON.stringify(presets.map((p) => p.to)));
ok(presets[1].from === '2022-03-01', 'preset 3a comeca exatamente 3 anos antes', presets[1].from);

console.log('\n11. _reactPreserveX: barra de periodo e clique da pill');
const chart = doc.getElementById('chart-teste');
chamadas.length = 0;
R._reactPreserveX('chart-teste', [tr], layout);
const reacts = chamadas.filter((c) => c.tipo === 'react');
ok(reacts.length === 1, 'chama Plotly.react uma vez');
ok(reacts[0].layout.xaxis.autorange === false, 'react recebe range explicito');
ok((chart._plotly['plotly_relayout'] || []).length === 2,
   'dois listeners ligados (tracker de X + y-autofit)',
   String((chart._plotly['plotly_relayout'] || []).length));
const bar = chart._closest.parentNode.children.find((c) => c.classList.contains('period-ctrl-bar'));
ok(!!bar, 'barra de periodo injetada acima do .chart-card');
const pills = bar ? bar._roles.quick.children : [];
ok(pills.length === 5, 'as 5 pills renderizadas como <button> HTML', String(pills.length));
chamadas.length = 0;
if (pills.length) pills[1].fire('click');
const rl = chamadas.filter((c) => c.tipo === 'relayout');
ok(rl.length >= 1 && JSON.stringify(rl[0].upd['xaxis.range']) === JSON.stringify(['2022-03-01', '2025-03-01']),
   'clique na pill "3a" chama relayout com o [from, to] exato',
   rl.length ? JSON.stringify(rl[0].upd) : '-');

console.log('\n12. Eixo que nao e data: sem barra de periodo, e limpeza ao trocar de modo');
const cat = doc.getElementById('chart-cat-teste');
chamadas.length = 0;
R._reactPlain('chart-cat-teste', [{ type: 'scatter', x: ['R6/26', 'R7/26'], y: [13.75, 13.5] }],
              R.mkCatLayout('%', 400));
const barCat = cat._closest.parentNode.children.find((c) => c.classList.contains('period-ctrl-bar'));
ok(!barCat, '_reactPlain NAO injeta barra de periodo (ela fala em mes/ano)');
ok((cat._plotly['plotly_relayout'] || []).length === 1, '_reactPlain liga so o y-autofit');
R._resetChartAxis('chart-teste');
const barDepois = chart._closest.parentNode.children.find((c) => c.classList.contains('period-ctrl-bar'));
ok(!barDepois, '_resetChartAxis remove a barra de periodo ao trocar de eixo');

console.log('\n13. y-autofit: refaz Y quando SO o X muda');
chamadas.length = 0;
R._reactPreserveX('chart-teste', [tr], layout);
chamadas.length = 0;
chart.emit('plotly_relayout', { 'xaxis.range': ['2024-06-01', '2025-03-01'] });
const fit = chamadas.filter((c) => c.tipo === 'relayout' && c.upd['yaxis.range']);
ok(fit.length === 1, 'X sozinho -> Y refeito', String(fit.length));
ok(fit.length && fit[0].upd['yaxis.autorange'] === false, 'Y fixado no range calculado');
if (fit.length) {
  const [lo, hi] = fit[0].upd['yaxis.range'];
  ok(lo < 2.25 && hi > 4.0, 'Y cobre so o visivel (com folga)', JSON.stringify([lo, hi]));
}
chamadas.length = 0;
chart.emit('plotly_relayout', { 'xaxis.range': ['2024-06-01', '2025-03-01'], 'yaxis.range': [0, 9] });
ok(chamadas.filter((c) => c.tipo === 'relayout' && c.upd['yaxis.range']).length === 0,
   'X e Y juntos (drag/scroll) -> autofit sai da frente');

console.log('\n13b. Identidade entre tabelas: Selic anual x ultima reuniao do ano');
// A Selic anual da expc_focus_periodo e FIM DE PERIODO, entao tem de bater com a
// expectativa para a ULTIMA reuniao do Copom daquele ano -- que vem de outro endpoint,
// com outro painel. Nao e identidade exata (paineis e arredondamentos diferentes), mas
// meio ponto de distancia ja seria sinal de que uma das duas leituras esta errada.
// So vale para anos com o calendario inteiro cotado: em 2028 o Focus ainda para na R5.
const cur = R._copCurva(R.NG - 1, '0');
const porAno = {};
cur.forEach((c) => { const a = R._parseReuniao(c.reuniao).ano; porAno[a] = c; });
let conferidos = 0, fora = [];
Object.keys(porAno).forEach((ano) => {
  if (R._parseReuniao(porAno[ano].reuniao).n < 8) return;   // ano incompleto na fila
  const anual = R.blkAt(R.pBlk('anual', 'Selic|', ano), 'm', R.NG - 1);
  if (anual == null) return;
  conferidos++;
  if (Math.abs(anual - porAno[ano].valor) > 0.5) {
    fora.push(ano + ': anual=' + anual + ' vs ' + porAno[ano].reuniao + '=' + porAno[ano].valor);
  }
});
ok(conferidos > 0 && fora.length === 0,
   conferidos + ' ano(s) com calendario completo: Selic anual bate com a ultima reuniao',
   fora.join('; '));

console.log('\n14. Cobertura e consistencia do payload');
const cob = R.D.cobertura || [];
ok(cob.length > 40, 'tabela de cobertura tem uma linha por serie', String(cob.length));
ok(cob.every((r) => r.d0 <= r.d1), 'primeira data nunca depois da ultima');
const tabelas = {};
cob.forEach((r) => { tabelas[r.tabela] = true; });
ok(Object.keys(tabelas).sort().join(',') === 'expc_focus,expc_focus_copom,expc_focus_periodo',
   'cobertura cobre as tres tabelas', Object.keys(tabelas).join(','));
// Componentes do IPCA so existem depois da reformulacao de 2021-09-14.
const comp = cob.filter((r) => r.serie === 'IPCA Serviços' && r.tabela === 'expc_focus_periodo');
ok(comp.length && comp.every((r) => r.d0 >= '2021-09-01'),
   'componentes do IPCA comecam na reformulacao de set/2021', JSON.stringify(comp.map((r) => r.d0)));
// Nenhum indicador pode ter caido em "Outros": se caiu, a pesquisa mudou e o mapa de
// familias em generate_report.py ficou para tras.
const semFamilia = [];
['anual', 'trimestral', 'mensal'].forEach((per) => {
  R.indsDe(per).forEach((i) => { if (i.familia === 'Outros') semFamilia.push(per + ':' + i.label); });
});
ok(semFamilia.length === 0, 'todo indicador tem familia declarada', semFamilia.join(', '));
// A grade tem que terminar na ultima pesquisa que o banco tem.
ok(R.D.meta.expc_focus_periodo.ultima === R.GRADE[R.NG - 1],
   'ultima semana da grade = ultima pesquisa da expc_focus_periodo',
   R.D.meta.expc_focus_periodo.ultima + ' vs ' + R.GRADE[R.NG - 1]);
// Todo bloco tem que caber na grade -- um i0 fora do intervalo desloca a serie inteira.
let forasDeGrade = 0, statsDesalinhados = 0;
['anual', 'trimestral', 'mensal'].forEach((per) => {
  Object.keys(R.D.periodo[per]).forEach((k) => {
    const b = R.D.periodo[per][k];
    if (b.i0 < 0 || b.i0 + b.m.length > R.NG) forasDeGrade++;
    if (b.s.length !== b.m.length || b.n.length !== b.m.length) statsDesalinhados++;
  });
});
Object.keys(R.D.movel).forEach((k) => {
  const b = R.D.movel[k];
  if (b.i0 < 0 || b.i0 + b.m.length > R.NG) forasDeGrade++;
  if (b.lo.length !== b.m.length || b.hi.length !== b.m.length) statsDesalinhados++;
});
ok(forasDeGrade === 0, 'nenhum bloco extrapola a grade', String(forasDeGrade));
ok(statsDesalinhados === 0, 'todas as estatisticas de um bloco tem o mesmo comprimento',
   String(statsDesalinhados));

console.log('\n' + (falhas ? falhas + ' FALHA(S)' : 'todos os testes passaram'));
process.exit(falhas ? 1 : 0);
