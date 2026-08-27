// Testa o esqueleto JS do Panorama de Politica Monetaria, executando o script REAL do
// HTML gerado contra um DOM stub e um Plotly stub.
//
// Roda com:
//     node tests/test_monetary_policy_js.js
//
// Precisa de "reports/brasil/Monetary Policy.html" gerado:
//     uv run python analytics/brasil/monetary_policy/generate_report.py
//
// Por que um harness e nao `node --check`: este projeto ja teve dois bugs de dashboard
// chegarem em producao passando por checagem de sintaxe (ver .claude/rules/lis-dashboards.md,
// secao "Quick-range buttons") -- o que falhou nos dois casos foi o COMPORTAMENTO do clique
// no botao de range, nao a sintaxe. Aqui o clique e disparado de fato e o relayout resultante
// e inspecionado, incluindo a ancoragem no ultimo ponto REAL do dado (a causa raiz das duas
// quebras).
//
// Cobre (a) o FRAMEWORK compartilhado -- layouts, presets de range, preservacao de X,
// y-autofit, formatacao BR/truncada, toggle de labels -- e (b) as abas do modelo agregado:
// que cada renderizador executa contra o payload real, que as series que ele pede existem,
// que as decomposicoes fecham como identidade, e que a eq. (5) chega no payload como
// resposta (pi^e se move) e nao como premissa. O que ele NAO substitui e confirmacao
// visual num browser real.

const fs = require('fs');
const path = require('path');

const HTML = path.join(__dirname, '..', 'reports', 'brasil', 'Monetary Policy.html');
if (!fs.existsSync(HTML)) {
  console.error('reports/brasil/Monetary Policy.html nao existe -- gere o relatorio primeiro:');
  console.error('  uv run python analytics/brasil/monetary_policy/generate_report.py');
  process.exit(1);
}
const blocos = fs.readFileSync(HTML, 'utf8').match(/<script>([\s\S]*?)<\/script>/g) || [];
if (!blocos.length) { console.error('nenhum <script> encontrado no HTML'); process.exit(1); }
const RAW = fs.readFileSync(HTML, 'utf8');
const SRC = blocos[blocos.length - 1].replace(/^<script>/, '').replace(/<\/script>$/, '');

// ── Referencia do Python: os CSVs que modelo_agregado.rodar() gravou ─────────
// Ate 2026-08-25 estas series chegavam pelo payload (D.cenarios), que a aba Cenarios
// consumia. Com a aba removida o payload nao as carrega mais, e a referencia passou a ser
// lida direto do artefato -- que e fonte MELHOR: precisao cheia, sem o arredondamento de
// 4 casas que o _ser() do generate_report aplica antes de escrever no HTML.
const DATA_DIR = path.join(__dirname, '..', 'analytics', 'brasil', 'monetary_policy', 'data');
function lerCSV(nome) {
  const linhas = fs.readFileSync(path.join(DATA_DIR, nome), 'utf8').trim().split(/\r?\n/);
  const cols = linhas[0].split(',').slice(1);
  const out = { _index: [] };
  cols.forEach((c) => { out[c] = []; });
  linhas.slice(1).forEach((l) => {
    const campos = l.split(',');
    out._index.push(campos[0]);
    cols.forEach((c, i) => {
      const v = campos[i + 1];
      out[c].push(v === '' || v === undefined ? null : Number(v));
    });
  });
  return out;
}
const _cenCache = {};
function cenarioPy(jk, ek) {
  const k = jk + '__' + ek;
  if (!_cenCache[k]) _cenCache[k] = lerCSV('modelo_cenario_' + k + '.csv');
  return _cenCache[k];
}

let falhas = 0;
function ok(cond, nome, detalhe) {
  if (cond) { console.log('  ok   ' + nome); }
  else { falhas++; console.log('  FALHA ' + nome + (detalhe ? '  -- ' + detalhe : '')); }
}

// ── DOM stub ──────────────────────────────────────────────────────────────────
// querySelector entende so os seletores que o script realmente usa ([data-role=...],
// .pill, .period-ctrl-bar[data-for=...]) -- um stub que devolve null para tudo (como o de
// tests/test_release_calendar_js.js) nao exercita a barra de periodo, que e justamente onde
// os dois bugs de producao moraram.
function El(tag) {
  this.tag = tag || 'div';
  this.children = []; this.style = {}; this.dataset = {}; this._attrs = {};
  this.id = ''; this.checked = false; this.disabled = false;
  this._className = ''; this.textContent = ''; this.value = '';
  this._html = ''; this._listeners = {}; this._plotly = {};
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
// `el.classList.contains('period-ctrl-bar')`. Um stub que trate os dois como campos
// independentes faz a barra de periodo parecer nunca injetada (era um bug DESTE harness,
// nao do relatorio).
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
El.prototype.addEventListener = function (k, f) { (this._listeners[k] = this._listeners[k] || []).push(f); };
El.prototype.fire = function (k, ev) { (this._listeners[k] || []).forEach((f) => f(ev)); };
// Plotly expoe .on() nos divs de grafico (nao e addEventListener)
El.prototype.on = function (k, f) { (this._plotly[k] = this._plotly[k] || []).push(f); };
El.prototype.emit = function (k, ev) { (this._plotly[k] || []).forEach((f) => f(ev)); };
El.prototype.closest = function () { return this._closest || null; };
El.prototype.querySelectorAll = function (sel) {
  // Combinador descendente: cada parte separada por espaco filtra DENTRO da anterior.
  // Sem isso '.eq .n' exigia as duas classes no mesmo no e devolvia [] em silencio --
  // um seletor que nunca casa faz o teste passar por vacuidade, nao por acerto.
  let atual = [this];
  String(sel).trim().split(/\s+/).forEach((parte) => {
    const prox = [];
    atual.forEach((el) => {
      _descendentes(el, []).forEach((c) => {
        if (_selMatch(c, parte) && prox.indexOf(c) < 0) prox.push(c);
      });
    });
    atual = prox;
  });
  return atual;
};
El.prototype.querySelector = function (sel) {
  const r = this.querySelectorAll(sel);
  return r.length ? r[0] : null;
};
Object.defineProperty(El.prototype, 'innerHTML', {
  get() { return this._html; },
  set(v) {
    this._html = v; this.children = [];
    parseIntoEl(String(v), this);
    // _roles continua existindo para os testes da barra de periodo, mas agora aponta para
    // os nos REAIS da arvore -- se apontasse para copias, os botoes que o script cria com
    // appendChild iriam para um objeto e o teste leria outro.
    this._roles = {quick: this.querySelector('[data-role=quick]'),
                   from: this.querySelector('[data-role=from]'),
                   to: this.querySelector('[data-role=to]')};
  },
});

// ── innerHTML vira ARVORE de verdade ─────────────────────────────────────────
// A versao anterior deste stub so guardava a string e devolvia [] em querySelectorAll, o
// que deixava todo o fiamento por clique sem cobertura -- exatamente a classe de bug que a
// regra .claude/rules/lis-dashboards.md manda nao repetir (markup e seletor combinam? o
// clique faz o que promete?). Aqui o HTML e parseado numa arvore com atributos, classes e
// dataset, e querySelectorAll entende os seletores compostos simples que os relatorios
// realmente usam (tag, .classe, #id, [attr], [attr="v"], e combinacoes deles).
const _VOID_TAGS = {br: 1, hr: 1, img: 1, input: 1, meta: 1, link: 1, source: 1};
function _camel(s) { return s.replace(/-([a-z])/g, (m, c) => c.toUpperCase()); }

function parseIntoEl(html, pai) {
  const tagRe = /<\/?([a-zA-Z][\w-]*)((?:\s+[\w:-]+(?:=(?:"[^"]*"|'[^']*'|[^\s>]+))?)*)\s*(\/?)>/g;
  const pilha = [pai];
  let m;
  while ((m = tagRe.exec(html))) {
    if (m[0].charAt(1) === '/') { if (pilha.length > 1) pilha.pop(); continue; }
    const tag = m[1].toLowerCase();
    const el = new El(tag);
    const attrRe = /([\w:-]+)(?:="([^"]*)")?/g;
    let a;
    while ((a = attrRe.exec(m[2] || ''))) {
      const nome = a[1], val = a[2] == null ? '' : a[2];
      el._attrs[nome] = val;
      if (nome === 'class') el.className = val;
      else if (nome === 'value') el.value = val;
      else if (nome === 'id') el.id = val;
      else if (nome === 'checked') el.checked = true;
      else if (nome === 'disabled') el.disabled = true;
      else if (nome.indexOf('data-') === 0) el.dataset[_camel(nome.slice(5))] = val;
    }
    pilha[pilha.length - 1].appendChild(el);
    if (!_VOID_TAGS[tag] && !m[3]) pilha.push(el);
  }
}

function _selMatch(el, sel) {
  const toks = sel.match(/^[a-zA-Z][\w-]*|\.[\w-]+|#[\w-]+|\[[^\]]+\]|:checked/g) || [];
  return toks.every((t) => {
    if (t.charAt(0) === '.') return el.classList.contains(t.slice(1));
    if (t.charAt(0) === '#') return el.id === t.slice(1);
    if (t === ':checked') return !!el.checked;
    if (t.charAt(0) === '[') {
      const dentro = t.slice(1, -1), eq = dentro.indexOf('=');
      if (eq < 0) return el._attrs[dentro] !== undefined;
      const k = dentro.slice(0, eq);
      const v = dentro.slice(eq + 1).replace(/^["']|["']$/g, '');
      return el._attrs[k] === v;
    }
    return el.tag === t;
  });
}
function _descendentes(el, out) {
  el.children.forEach((c) => { out.push(c); _descendentes(c, out); });
  return out;
}

function makeDom() {
  const els = {};
  const ABAS = ['motor', 'condicoes', 'projecoes', 'appendix'];
  const tabBtns = ABAS.map((t) => {
    const b = new El('button'); b.dataset.tab = t; return b;
  });
  const tabPanels = ABAS.map((t) => {
    const p = new El('div'); p.id = 'tab-' + t; return p;
  });
  const doc = {
    getElementById(id) {
      if (!els[id]) { els[id] = new El('div'); els[id].id = id; }
      return els[id];
    },
    createElement: (t) => new El(t),
    querySelector(sel) {
      if (sel === 'main') return new El('main');
      const m = /^\.period-ctrl-bar\[data-for="(.+)"\]$/.exec(sel);
      if (m) return doc._periodBars[m[1]] || null;
      return null;
    },
    querySelectorAll(sel) {
      if (sel === '.tab-btn') return tabBtns;
      if (sel === '.tab-panel') return tabPanels;
      return [];
    },
    addEventListener() {},
    _periodBars: {},
    _els: els,
    _tabBtns: tabBtns,
    _tabPanels: tabPanels,
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
      el._fullLayout.xaxis.type = 'date';
      return thenable(el);
    },
    relayout(divId, upd) {
      chamadas.push({ tipo: 'relayout', divId, upd });
      return thenable(doc.getElementById(divId));
    },
    newPlot() { throw new Error('newPlot nao deve ser chamado -- use _reactPreserveX'); },
    Plots: { resize(el) { chamadas.push({ tipo: 'resize', el }); } },
  };
}

// ── Execucao ──────────────────────────────────────────────────────────────────
const doc = makeDom();
const chamadas = [];
global.document = doc;
global.window = {};
global.Option = function (label, value) { const o = new El('option'); o.textContent = label; o.value = value; return o; };
global.Plotly = makePlotly(doc, chamadas);
// localStorage de mentira: sem ele mtLer()/mtGravar() caem no catch e a lista de cenarios
// salvos fica sem cobertura nenhuma.
const _store = {};
global.localStorage = {
  getItem(k) { return Object.prototype.hasOwnProperty.call(_store, k) ? _store[k] : null; },
  setItem(k, v) { _store[k] = String(v); },
  removeItem(k) { delete _store[k]; },
};
global.confirm = () => true;
global.alert = () => {};

// Reexporta as funcoes internas: new Function() cria escopo proprio, entao nada e visivel
// de fora sem esta linha.
const EXPORTS = ['fmtBR', 'fmtTrunc', 'fmtDate', 'lastValid', 'growthN', 'dlText', 'lineTrace',
                 '_quickRangeOptions', '_defaultXRange', '_traceAllDates', 'mkTimeseriesLayout',
                 'mkBarLayout', '_reactPreserveX', 'activateTab', 'RENDERERS', 'setKPI', '_PLOTLY_CONFIG',
                 'D', 'dashTrace',
                 'renderCondicoes', 'cdCor', 'cdVeredito', 'cdDataCurta', 'cdAlimenta',
                 'motorSim', 'mtCfgPadrao', 'mtClone', '_mtVals', '_mtSolve', 'MT_SPEC',
                 'mtRenderInputs', 'mtRenderCenarios', '_mtResumo',
                 'mtDefaults', 'mtPathMeta', 'mtAtalho', 'mtChoque', 'mtIgualPadrao',
                 '_mtLinha', '_mtShapes', 'MT_GRUPOS', 'mtToggleGraf',
                 '_mtHR', 'mtNotaHR', 'MT_HR_TRI',
                 'renderProjecoes', 'renderProjecoesSerie', 'renderProjecoesBacktest',
                 'renderProjecoesPrevBox', 'renderProjecoesBtTabela',
                 'pjLinhas', 'pjCorr', 'pjMAE', 'pjBtNivel', 'pjPrevisao', 'pjPrevValor',
                 'pjMet', 'PJ_METODOS', 'PJ'];
let MP;
try {
  new Function(SRC + ';global.__MP = {' + EXPORTS.join(',')
               + ', get MT_CFG(){return MT_CFG;}, get MT_RES(){return MT_RES;}};')();
  MP = global.__MP;
} catch (e) {
  console.error('o script do relatorio lancou excecao ao carregar: ' + e.stack);
  process.exit(1);
}

console.log('\n1. Carga e troca de abas');
ok(!!MP, 'script executa sem excecao');
ok(Object.keys(MP.RENDERERS).sort().join(',') === 'appendix,condicoes,motor,projecoes',
   'RENDERERS tem as 4 abas, todas construidas', JSON.stringify(Object.keys(MP.RENDERERS)));
// A aba Projecoes deixou de ser stub em 2026-08-25 -- cobertura propria na secao 33.
ok('projecoes' in MP.RENDERERS, 'projecoes entra no RENDERERS');
// appendix TEM renderizador: preenche a tabela de validacao dos parametros a partir de D.info.
ok('appendix' in MP.RENDERERS, 'appendix entra no RENDERERS (monta a tabela de validacao)');
ok(doc._tabPanels[0].classList.contains('active'), 'aba inicial (motor) ativa no load');
MP.activateTab('condicoes');
ok(doc._tabPanels[1].classList.contains('active') && !doc._tabPanels[0].classList.contains('active'),
   'activateTab troca o painel ativo');
ok(doc._tabBtns[1].classList.contains('active'), 'activateTab troca o botao ativo');
ok(doc._els['generated-at'].textContent !== '', 'generated_at escrito no header',
   JSON.stringify(doc._els['generated-at'].textContent));

console.log('\n2. Formatacao BR (virgula decimal) e truncamento dos labels');
ok(MP.fmtBR(1.5) === '1,50', 'fmtBR usa virgula decimal', MP.fmtBR(1.5));
// A convencao da skill lis-dashboard e TRUNCAR, nunca arredondar: 16,951 -> "16,9".
ok(MP.fmtTrunc(16.951, 1) === '16,9', 'fmtTrunc TRUNCA (nao arredonda)', MP.fmtTrunc(16.951, 1));
ok(MP.fmtTrunc(-0.28, 1) === '-0,3', 'fmtTrunc de negativo (floor, consistente)', MP.fmtTrunc(-0.28, 1));
ok(MP.fmtBR(null) === '—' && MP.fmtTrunc(null) === '—', 'nulo vira em-dash em vez de NaN');
ok(MP.fmtDate('2026-08-01', 'projecoes') === '2026 T3', 'fmtDate trimestral para grupo de 4/ano',
   MP.fmtDate('2026-08-01', 'projecoes'));
// Todo grupo do relatorio e trimestral agora (o modelo e trimestral). Um grupo nao
// declarado cai no default mensal, que e o caminho que este caso cobre.
ok(MP.fmtDate('2026-08-01', 'motor') === '2026 T3', 'fmtDate trimestral tambem para motor',
   MP.fmtDate('2026-08-01', 'motor'));
ok(MP.fmtDate('2026-08-01', 'grupo_inexistente') === 'Ago/2026',
   'fmtDate cai em mensal quando o grupo nao esta em PERIODS_PER_YEAR',
   MP.fmtDate('2026-08-01', 'grupo_inexistente'));

console.log('\n3. Desbaste dos labels de valor (dlText)');
const cem = Array.from({ length: 100 }, (_, i) => i + 0.5);
const t100 = MP.dlText(cem, 1, '%');
ok(t100.filter((s) => s !== '').length === 21, '>60 pontos -> 1 em 5 (+ o ultimo)',
   String(t100.filter((s) => s !== '').length));
ok(t100[t100.length - 1] !== '', 'ultimo ponto sempre rotulado');
ok(MP.dlText([1.11, 2.22, 3.33], 1, '%').every((s) => s !== ''), '<=30 pontos -> todos rotulados');
ok(MP.dlText([1.96], 1, '%')[0] === '1,9%', 'label trunca e leva o sufixo', MP.dlText([1.96], 1, '%')[0]);

console.log('\n4. lineTrace / toggle "Dados no grafico"');
const S = {
  dates: ['2024-03-01', '2024-06-01', '2024-09-01', '2024-12-01', '2025-03-01'],
  values: [1.5, 2.25, null, 3.75, 4.0],
};
const semLabel = MP.lineTrace(S, 'Serie', '#1F2853', false, 2, '%');
const comLabel = MP.lineTrace(S, 'Serie', '#1F2853', true, 2, '%');
ok(semLabel.text === undefined && semLabel.mode === 'lines+markers', 'toggle OFF: sem text, sem modo text');
ok(Array.isArray(comLabel.text) && comLabel.mode === 'lines+markers+text', 'toggle ON: text + modo text');
ok(comLabel.text[2] === '', 'ponto nulo nao recebe label');
ok(semLabel.hovertemplate.indexOf('%{customdata}') >= 0 && semLabel.customdata[1] === '2,25',
   'hover usa customdata em formato BR (o %{y} nao aceita virgula decimal)', semLabel.customdata[1]);
ok(semLabel.line.shape === 'spline', 'linha spline (padrao visual da skill)');

console.log('\n5. Layout: pan nos dois eixos + view inicial justa');
const traces = [semLabel];
const layout = MP.mkTimeseriesLayout('%', 540, traces);
ok(layout.dragmode === 'pan', 'dragmode pan (arrastar move, nao faz box-zoom)');
ok(MP._PLOTLY_CONFIG.scrollZoom === true, 'scrollZoom ligado (scroll da zoom nos dois eixos)');
ok(!('fixedrange' in layout.yaxis) && !('fixedrange' in layout.xaxis),
   'nenhum eixo com fixedrange (Y tem pan/zoom livre)');
ok(layout.hovermode === 'x unified' && layout.hoverlabel.bgcolor === '#1F2853',
   'tooltip unificado com fundo navy da marca');
// A view inicial usa os limites REAIS do dado (+2%), nao o autopad bem maior do Plotly.
const xr = layout.xaxis.range;
ok(layout.xaxis.autorange === false && xr[0] < '2024-03-01' && xr[1] > '2025-03-01',
   'range inicial ancorado no dado real, autorange desligado', JSON.stringify(xr));
const spanDias = (Date.parse(xr[1]) - Date.parse(xr[0])) / 86400000;
ok(spanDias < 400, 'folga da view inicial e pequena (~2%), nao o autopad do Plotly', spanDias.toFixed(0) + 'd');
ok(MP.mkBarLayout('%', 480, traces).showlegend === false, 'mkBarLayout sem legenda');

console.log('\n6. Presets de range rapido: ancoragem no ultimo ponto REAL');
// Este e o bug que chegou em producao duas vezes. Um botao nativo stepmode:'backward'
// calcularia o "to" a partir do range atual do eixo (auto-paddeado) -- aqui tem que ser
// exatamente a ultima data do dado.
const datas = MP._traceAllDates(traces);
const presets = MP._quickRangeOptions(datas);
ok(presets.map((p) => p.label).join(',') === '1a,3a,5a,10a,Tudo', 'os 5 presets na ordem',
   presets.map((p) => p.label).join(','));
ok(presets.every((p) => p.to === '2025-03-01'), 'todo preset termina na ULTIMA data real do dado',
   JSON.stringify(presets.map((p) => p.to)));
ok(presets[1].from === '2022-03-01', 'preset 3a comeca exatamente 3 anos antes', presets[1].from);
ok(presets[4].from === '2024-03-01', 'preset Tudo comeca na primeira data real', presets[4].from);

console.log('\n7. _reactPreserveX: react + binds + barra de periodo');
// Monta a arvore que o script espera: <div>(pai) > .chart-card > #chart-teste
const chart = doc.getElementById('chart-teste');
const card = new El('div'); card.classList.add('chart-card');
const pai = new El('div');
pai.appendChild(card);
card.appendChild(chart);
chart._closest = card;
chamadas.length = 0;
MP._reactPreserveX('chart-teste', traces, layout);
const reacts = chamadas.filter((c) => c.tipo === 'react');
ok(reacts.length === 1, 'chama Plotly.react uma vez', String(reacts.length));
ok(reacts[0].layout.xaxis.autorange === false, 'react recebe range explicito, nao autorange');
ok((chart._plotly['plotly_relayout'] || []).length === 2,
   'dois listeners de relayout ligados (tracker de X + y-autofit)',
   String((chart._plotly['plotly_relayout'] || []).length));
const bar = pai.children.find((c) => c.classList.contains('period-ctrl-bar'));
ok(!!bar, 'barra de periodo injetada acima do .chart-card');
ok(bar && bar.dataset.for === 'chart-teste', 'barra marcada com o div dono');
const pills = bar ? bar._roles.quick.children : [];
ok(pills.length === 5, 'as 5 pills de range renderizadas como <button> HTML', String(pills.length));
ok(bar && bar._roles.from.children.length === datas.length,
   'dropdown De populado com todas as datas', bar ? String(bar._roles.from.children.length) : '-');

console.log('\n8. Clique numa pill dispara o relayout com o range exato');
// O componente nativo xaxis.rangeselector.buttons falhou aqui duas vezes; o caminho atual e
// Plotly.relayout() direto, e este teste dispara o clique de verdade.
chamadas.length = 0;
pills[1].fire('click');
const rl = chamadas.filter((c) => c.tipo === 'relayout');
ok(rl.length >= 1, 'clique na pill "3a" chama Plotly.relayout', String(rl.length));
ok(rl.length && JSON.stringify(rl[0].upd['xaxis.range']) === JSON.stringify(['2022-03-01', '2025-03-01']),
   'relayout carrega o [from, to] exato do preset', rl.length ? JSON.stringify(rl[0].upd) : '-');

console.log('\n9. y-autofit: refaz Y quando SO o X muda, e sai da frente quando nao');
// Regra do _bindYAutofit (analytics/report_structure/y_autofit.js): reagir a um preset/reset
// (X muda sozinho) e NAO reagir a um drag/scroll (X e Y mudam juntos), senao briga com o gesto.
chamadas.length = 0;
chart.emit('plotly_relayout', { 'xaxis.range': ['2024-06-01', '2025-03-01'] });
const fit = chamadas.filter((c) => c.tipo === 'relayout' && c.upd['yaxis.range']);
ok(fit.length === 1, 'X sozinho -> Y refeito', String(fit.length));
ok(fit.length && fit[0].upd['yaxis.autorange'] === false, 'Y fixado no range calculado');
if (fit.length) {
  const [lo, hi] = fit[0].upd['yaxis.range'];
  // Janela 2024-06 -> 2025-03 contem 2,25 / null / 3,75 / 4,0
  ok(lo < 2.25 && hi > 4.0, 'Y cobre so o visivel (com folga)', JSON.stringify([lo, hi]));
}
chamadas.length = 0;
chart.emit('plotly_relayout', { 'xaxis.range': ['2024-03-01', '2025-03-01'], 'yaxis.range': [0, 5] });
ok(chamadas.filter((c) => c.tipo === 'relayout' && c.upd['yaxis.range']).length === 0,
   'X e Y juntos (drag/scroll) -> y-autofit nao interfere');

console.log('\n10. Preservacao do X entre re-renders');
// Sem isso, todo re-render disparado por um controle reseta o eixo -- le como "o grafico
// fica resetando".
chart.emit('plotly_relayout', { 'xaxis.range': ['2024-09-01', '2025-03-01'] });
chamadas.length = 0;
MP._reactPreserveX('chart-teste', traces, MP.mkTimeseriesLayout('%', 540, traces));
const r2 = chamadas.filter((c) => c.tipo === 'react')[0];
ok(r2 && JSON.stringify(r2.layout.xaxis.range) === JSON.stringify(['2024-09-01', '2025-03-01']),
   're-render mantem a janela de X que o usuario deixou',
   r2 ? JSON.stringify(r2.layout.xaxis.range) : '-');

console.log('\n11. KPI cards');
MP.setKPI('kpi-teste', -1.5, 'sub');
ok(doc._els['kpi-teste-value'].textContent === '-1,50%', 'KPI em formato BR com sufixo',
   doc._els['kpi-teste-value'].textContent);
ok(doc._els['kpi-teste-value'].className.indexOf('neg') >= 0, 'KPI negativo recebe classe neg');
MP.setKPI('kpi-teste', null);
ok(doc._els['kpi-teste-value'].textContent === '—', 'KPI nulo vira em-dash');


console.log('\n12. Abas renderizam sem excecao');
// Renderizar de fato cada aba contra o payload REAL: pega chave de serie errada, campo
// ausente em D.info e trace malformado -- o tipo de erro que `node --check` nao ve.
// Cenarios, Decomposicao, Taxa Neutra e Hiato do Produto foram REMOVIDAS em 2026-08-25;
// a aba do motor tem cobertura propria e muito mais funda nas secoes 19-30.
['appendix', 'condicoes', 'projecoes'].forEach((tab) => {
  let erro = null;
  try { MP.RENDERERS[tab](); } catch (e) { erro = e; }
  ok(!erro, 'render' + tab[0].toUpperCase() + tab.slice(1) + ' executa', erro && String(erro));
});

console.log('\n13. Payload: o que as abas vivas pedem existe, e o das mortas nao sobrou');
const D = MP.D || {};
ok(Object.keys(D.motor || {}).length > 0, 'grupo motor populado');
['selic', 'h', 'ipca_4t', 'pi_e', 'rr_IS_total'].forEach((k) => {
  ok(!!(D.motor && D.motor[k]), 'motor traz o historico de ' + k);
});
// Apagar a aba sem apagar o loader deixaria o payload carregando series que ninguem le.
// Num arquivo autocontido isso e peso morto invisivel -- so aparece no tamanho do .html.
['cenarios', 'decomp', 'neutra', 'hiato'].forEach((g) => {
  ok(!D[g], 'grupo ' + g + ' saiu do payload junto com a aba');
});
// 22 = os 19 do filtro + os 3 phi da eq. (5), que vem de estimador proprio.
ok((D.info || {}).n_total === 22, 'info traz os 22 parametros da Tabela 1 do boxe',
   String((D.info || {}).n_total));
const _val = (D.info || {}).validacao || [];
ok(_val.filter((r) => r.metodo === 'filtro').length === 19,
   '19 parametros marcados como estimados no filtro',
   String(_val.filter((r) => r.metodo === 'filtro').length));
ok(_val.filter((r) => r.metodo === 'dois passos').map((r) => r.param).sort().join(',') === 'f1,f2,f3',
   'os tres phi vem marcados como estimados fora do filtro');

// As secoes 14 (identidade das decomposicoes) e 15 (_emenda/_recorta) sairam em 2026-08-25
// com as abas Decomposicao e Cenarios. A numeracao das seguintes NAO foi corrida de
// proposito: o CLAUDE.md da pasta cita as secoes 19, 22, 25, 28 e 31 pelo numero.

console.log('\n16. Equacao (5): a expectativa endogena e resposta, nao premissa');
// O cenario default e o endogeno. O teste que importa: no cenario 'eq5' pi^e VARIA ao
// longo do horizonte (o modelo a move), enquanto no cenario 'focus' ela e uma constante
// por construcao.
function _spread(vals) {
  const v = (vals || []).filter((x) => x != null);
  return v.length ? Math.max.apply(null, v) - Math.min.apply(null, v) : 0;
}
const _pe5 = cenarioPy('focus', 'eq5').pi_e;
const _pef = cenarioPy('focus', 'focus').pi_e;
ok(_pe5.length > 0, 'existe cenario com expectativa endogena (eq. 5)');
ok(_spread(_pe5) > 0.1, 'pi^e endogena se move ao longo do cenario',
   'amplitude ' + _spread(_pe5).toFixed(4));
ok(_spread(_pef) < 1e-9, 'pi^e da premissa Focus e constante, como anunciado',
   'amplitude ' + _spread(_pef).toFixed(9));
ok(cenarioPy('focus', 'eq5').de.length > 0, 'o cenario traz a variacao cambial da eq. (4)');
const _f2 = ((D.info || {}).params || {}).f2;
ok(_f2 > 0 && _f2 < 1, 'phi2 (peso da previsao do modelo) esta em (0,1)', String(_f2));

console.log('\n17. IRF: a escada de validacao tem os tres pares e o motor com parametros do BC');
const _IRF = lerCSV('modelo_irf.csv');
const _PARES = [['ipca_4t_so_demanda', 'publicado_so_demanda'],
                ['ipca_4t_com_expectativa', 'publicado_sem_cambio'],
                ['ipca_4t_completo', 'publicado_completo']];
_PARES.forEach((par) => {
  ok(!!_IRF[par[0]] && !!_IRF[par[1]], 'par presente: ' + par[0] + ' vs ' + par[1]);
});
ok(!!_IRF.ipca_4t_motor_bcb, 'IRF traz a linha do nosso motor com os parametros publicados');
// Ligar a eq. (5) tem de FORTALECER a transmissao: o pico fica mais negativo. Se um dia
// sair mais fraco, ou o sinal do canal de expectativa inverteu ou o phi degenerou.
function _pico(k) {
  const v = (_IRF[k] || []).filter((x) => x != null);
  return Math.min.apply(null, v);
}
ok(_pico('ipca_4t_com_expectativa') < _pico('ipca_4t_so_demanda') - 0.01,
   'a eq. (5) aprofunda o IRF (canal de expectativa com sinal certo)',
   _pico('ipca_4t_so_demanda').toFixed(3) + ' -> ' + _pico('ipca_4t_com_expectativa').toFixed(3));
ok(_pico('ipca_4t_motor_bcb') < _pico('ipca_4t_com_expectativa'),
   'com os parametros do BC o motor responde mais que com os nossos');
const _vi = (D.info || {}).irf || {};
ok(_vi.motor_bcb && _vi.motor_bcb.erro_abs_medio < 0.06,
   'motor com parametros do BC bate no publicado (erro |medio| < 0,06 p.p.)',
   _vi.motor_bcb && String(_vi.motor_bcb.erro_abs_medio));

console.log('\n18. dashTrace: a linha publicada e tracejada e sem marcador');
const _dt = MP.dashTrace({dates: ['2026-01-01'], values: [1]}, 'x', '#000', false, 2, '%');
ok(_dt.line.dash === 'dash', 'dashTrace marca a linha como tracejada');
ok(_dt.mode === 'lines' && _dt.marker.size === 0, 'dashTrace nao desenha marcador');

console.log('\n19. Motor do modelo agregado: o porte JS reproduz o simulador Python');
// Este e o teste que sustenta a aba inteira. O motor JS refaz as equacoes que
// modelo_agregado.simular() resolve em Python, e o unico jeito de saber se a traducao
// esta certa e rodar as MESMAS 12 configuracoes que cenarios_padrao() pre-simulou e exigir
// que batam serie a serie. A referencia vem dos CSVs de `data/` (precisao cheia); a
// tolerancia segue 3e-4 porque `mtCfgPadrao()` monta o cenario a partir de `dflt`, que
// CHEGA arredondado no payload -- o piso de discrepancia e esse, nao o do CSV.
const _MC = (D.motor_cfg || {});
ok(!!_MC.par && !!_MC.ini && !!_MC.dflt, 'payload do motor chegou (par + ini + dflt)');
ok(typeof MP.motorSim === 'function', 'motorSim existe');

// Config = um vetor por input, como no `levels[]` do FX Report. Estes tres helpers montam
// as variacoes que os testes precisam sem depender do DOM.
function _cfg(n) { return MP.mtCfgPadrao(n || 16); }
function _manual(base, key, vals) {
  const c = MP.mtClone(base);
  c[key] = { modo: 'manual', vals: vals };
  return c;
}
function _const(base, key, v) {
  const c = MP.mtClone(base);
  c[key] = { modo: 'manual', vals: c[key].vals.map(() => v) };
  return c;
}
function _endog(base, key, on) {
  const c = MP.mtClone(base);
  c[key] = Object.assign({}, c[key], { modo: on ? 'endog' : 'manual' });
  return c;
}

if (_MC.par && MP.motorSim) {
  const _i0 = _MC.dflt.selic_ult;
  const _n = 16;
  const _choque = [];
  for (let k = 0; k < _n; k++) _choque.push(k < 4 ? 1 : Math.pow(0.8, k - 3));
  const _base16 = _cfg(_n);
  const _selCfg = (base, nome) => {
    if (nome === 'focus') return base;                       // o default JA e a curva Focus
    if (nome === 'constante') return _const(base, 'selic', _i0);
    const sg = nome === 'alta100' ? 1 : -1;
    return _manual(base, 'selic', _choque.map((c) => _i0 + sg * c));
  };
  const _pieCfg = (base, nome) => {
    if (nome === 'eq5') return base;                          // default endogeno
    if (nome === 'focus') return _const(base, 'pi_e', _MC.dflt.pi_e_focus);
    return _manual(base, 'pi_e', MP.mtPathMeta(_n));
  };
  const _CAMPOS = ['selic', 'i_e', 'r_hat', 'h', 'pi_L', 'pi_IPCA', 'ipca_4t', 'pi_e', 'de', 'de_hat'];
  const _TOL = 3e-4;
  let _pior = 0, _piorNome = '', _conferidos = 0;

  ['focus', 'constante', 'alta100', 'baixa100'].forEach((jk) => {
    ['eq5', 'focus', 'meta'].forEach((ek) => {
      const cfg = _pieCfg(_selCfg(_base16, jk), ek);
      const r = MP.motorSim(cfg);
      if (!r || r.erro) { ok(false, jk + '__' + ek + ' simula', r && r.erro); return; }
      let maxd = 0, campo = '';
      _CAMPOS.forEach((c) => {
        const py = cenarioPy(jk, ek)[c];
        if (!py || !py.length) return;
        _conferidos++;
        for (let i = 0; i < Math.min(py.length, r.n); i++) {
          const d = Math.abs(py[i] - r[c][i]);
          if (d > maxd) { maxd = d; campo = c + '[' + i + ']'; }
        }
      });
      if (maxd > _pior) { _pior = maxd; _piorNome = jk + '__' + ek + ' ' + campo; }
      ok(maxd < _TOL, 'motor JS == Python em ' + jk + '__' + ek,
         'max |dif| ' + maxd.toExponential(2) + ' em ' + campo);
    });
  });
  ok(_conferidos >= 100, 'as 12 configuracoes cobriram >=100 series', String(_conferidos));
  console.log('       maior discrepancia: ' + _pior.toExponential(2) + ' (' + _piorNome + ')');
  // O default da interface TEM de ser exatamente o focus__eq5 do Python: e o que garante que
  // quem abre a aba ve o mesmo cenario que a aba Cenarios chama de referencia. Guardar os
  // vetores ja arredondados para exibicao quebraria isto -- por isso `vals` guarda numeros.
  const _def = MP.motorSim(_cfg());
  const _pyDef = cenarioPy('focus', 'eq5').ipca_4t;
  let _dd = 0;
  for (let i = 0; i < _def.n; i++) _dd = Math.max(_dd, Math.abs(_pyDef[i] - _def.ipca_4t[i]));
  ok(_dd < _TOL, 'o cfg default da interface e o focus__eq5 do Python', _dd.toExponential(2));

  console.log('\n20. Motor: a eq. (5) fecha e o teste de folga passa');
  const _b = _def;
  ok(_b && !_b.erro, 'cenario default simula');
  ok(_b.diag.eq5 && _b.diag.taylor === false && _b.diag.uip === true,
     'default = Selic da Focus, expectativa endogena, cambio pela UIP');
  // A eq. (5) e resolvida como sistema afim, nao iterada: o residuo tem de ser ruido de
  // ponto flutuante, nao tolerancia de convergencia.
  ok(_b.diag.resid < 1e-8, 'residuo da eq. (5) e numerico', _b.diag.resid.toExponential(2));
  // Dobrar o buffer nao pode mover o trecho reportado. Se mover, a condicao terminal e que
  // esta determinando a resposta -- foi este teste que calibrou FOLGA=40 no Python.
  ok(_b.diag.folga < 1e-4, 'teste de folga: dobrar o buffer nao move o reportado',
     _b.diag.folga.toExponential(2));
  const _prem = MP.motorSim(_endog(_base16, 'pi_e', false));
  ok(_prem.diag.eq5 === false && _prem.diag.resid === undefined,
     'com expectativa de premissa o motor nao monta ponto fixo');

  console.log('\n21. Motor: Selic endogena pela regra de Taylor (eq. 3)');
  // A eq. (3) nao esta no simulador Python -- e a extensao que esta aba trouxe, para o juro
  // poder ser resposta e nao so premissa. Nao ha alvo publicado para comparar, entao o que
  // se testa e o comportamento que a regra TEM de ter.
  const _tay = MP.motorSim(_endog(_base16, 'selic', true));
  ok(_tay && !_tay.erro && _tay.diag.taylor === true, 'cenario com Taylor simula');
  ok(Math.abs(_MC.par.t1 + _MC.par.t2) < 1, 'a regra e estavel (|t1+t2| < 1)',
     (_MC.par.t1 + _MC.par.t2).toFixed(3));
  // Convergencia: com expectativa na meta a regra tem de levar o juro a rr_TAY + meta.
  const _alvo = _MC.ini.rr_TAY + _MC.meta[0];
  const _longo = MP.motorSim(_const(_endog(_cfg(24), 'selic', true), 'pi_e', _MC.meta[0]));
  ok(Math.abs(_longo.selic[23] - _alvo) < 0.25,
     'com pi^e na meta a Taylor converge para r*_TAY + meta',
     _longo.selic[23].toFixed(2) + ' vs alvo ' + _alvo.toFixed(2));
  // Sinal: expectativa acima da meta tem de puxar o juro PARA CIMA (t3 > 1, Taylor forte).
  const _tayNaMeta = _const(_endog(_base16, 'selic', true), 'pi_e', _MC.meta[0]);
  const _acima = MP.motorSim(_const(_endog(_base16, 'selic', true), 'pi_e', _MC.meta[0] + 2));
  const _naMeta = MP.motorSim(_tayNaMeta);
  ok(_acima.selic[8] > _naMeta.selic[8] + 1,
     'pi^e 2 p.p. acima da meta sobe a Selic mais de 1 p.p.',
     (_acima.selic[8] - _naMeta.selic[8]).toFixed(2));

  console.log('\n22. Motor: cada input move o modelo na direcao certa');
  // Taxa neutra: r* menor => o mesmo juro nominal vira mais aperto => hiato e IPCA caem.
  // E o input que a aba marca como o que mais move o resultado, entao o sinal dele e o
  // primeiro que tem de estar certo.
  const _r5 = MP.motorSim(_const(_base16, 'rr_IS', 5));
  ok(_r5.r_hat[15] > _b.r_hat[15] && _r5.h[15] < _b.h[15] && _r5.ipca_4t[15] < _b.ipca_4t[15],
     'r* menor => mais aperto, menos hiato, menos inflacao',
     'r_hat ' + _b.r_hat[15].toFixed(2) + '->' + _r5.r_hat[15].toFixed(2)
     + ' | ipca4t ' + _b.ipca_4t[15].toFixed(2) + '->' + _r5.ipca_4t[15].toFixed(2));
  // Resultado primario entra na IS com sinal negativo (beta3): primario maior contrai.
  const _rpMais = MP.motorSim(_const(_base16, 'rp', _MC.dflt.rp + 2));
  ok(_rpMais.h[15] < _b.h[15], 'primario maior contrai o hiato (beta3 > 0)',
     _b.h[15].toFixed(3) + ' -> ' + _rpMais.h[15].toFixed(3));
  // Administrados sao premissa pura: sem a eq. (5) nao ha canal de volta para o hiato.
  const _semExp = _endog(_base16, 'pi_e', false);
  const _pa = MP.motorSim(_const(_semExp, 'pi_A', 2));
  const _pa0 = MP.motorSim(_semExp);
  ok(Math.abs(_pa.h[15] - _pa0.h[15]) < 1e-9,
     'sem eq. (5), administrados nao voltam para o hiato (premissa pura)');
  ok(_pa.pi_IPCA[15] > _pa0.pi_IPCA[15], 'administrados maiores elevam o IPCA');
  // ...e com a eq. (5) ligada eles VOLTAM, via expectativa -- mas o sinal do retorno depende
  // de quem escolhe o juro, e este par e a razao de a aba deixar o Taylor disponivel.
  // Com a Selic NOMINAL dada por fora, expectativa maior derruba o juro REAL ex-ante
  // (r_hat = i^e - pi^e - r*), entao um choque de administrados e EXPANSIONISTA: o hiato
  // abre. Nao e bug -- e o que a eq. (2.1) diz quando o BC nao reage.
  const _paE = MP.motorSim(_const(_base16, 'pi_A', 2));
  ok(_paE.pi_e[15] > _b.pi_e[15], 'com eq. (5), administrados contaminam a expectativa',
     _b.pi_e[15].toFixed(2) + ' -> ' + _paE.pi_e[15].toFixed(2));
  ok(_paE.r_hat[15] < _b.r_hat[15] && _paE.h[15] > _b.h[15],
     'com Selic exogena o choque de administrados afrouxa o juro real e abre o hiato',
     'r_hat ' + _b.r_hat[15].toFixed(2) + ' -> ' + _paE.r_hat[15].toFixed(2));
  // Com o Taylor ligado o BC reage e o sinal inverte: e o teste que separa "o modelo esta
  // errado" de "faltava fechar a regra de politica".
  const _tBase = MP.motorSim(_endog(_base16, 'selic', true));
  const _tPaE = MP.motorSim(_const(_endog(_base16, 'selic', true), 'pi_A', 2));
  ok(_tPaE.selic[15] > _tBase.selic[15] && _tPaE.r_hat[15] > _tBase.r_hat[15]
     && _tPaE.h[15] < _tBase.h[15],
     'com Taylor o mesmo choque sobe a Selic, aperta o juro real e fecha o hiato',
     'selic ' + _tBase.selic[15].toFixed(2) + ' -> ' + _tPaE.selic[15].toFixed(2)
     + ' | h ' + _tBase.h[15].toFixed(2) + ' -> ' + _tPaE.h[15].toFixed(2));
  const _cl = MP.motorSim(_const(_base16, 'Zel', 100));
  ok(_cl.pi_L[15] > _b.pi_L[15], 'anomalia de El Nino eleva a inflacao de livres');
  // Condicoes iniciais: h0 com beta1 ~ 0,74 ainda pesa depois de 4 trimestres.
  const _h2cfg = MP.mtClone(_base16); _h2cfg.h0 = { v: _MC.ini.h + 2 };
  const _h2 = MP.motorSim(_h2cfg);
  ok(_h2.h[3] > _b.h[3] + 0.4, 'h0 +2 p.p. ainda aparece no 4o trimestre',
     (_h2.h[3] - _b.h[3]).toFixed(3));
  // s^h e o CAMINHO do choque da IS (eq. 2.2), nao mais so a condicao inicial. Default = o
  // decaimento que o filtro implica; digitar por cima e impor um choque de demanda.
  ok(Math.abs(_b.s_h[0] - _MC.par.b5 * _MC.ini.s_h) < 1e-12,
     'o default de s^h e o decaimento do filtro (b5 . s^h_t0)', _b.s_h[0].toFixed(6));
  ok(Math.abs(_b.s_h[4] - Math.pow(_MC.par.b5, 5) * _MC.ini.s_h) < 1e-12,
     'e segue decaindo por b5 ao longo do horizonte');
  const _sh = MP.motorSim(_manual(_base16, 's_h', _b.s_h.map((v) => v + 1)));
  ok(Math.abs((_sh.h[0] - _b.h[0]) - 1) < 1e-9,
     'choque de +1 p.p. em s^h entra aditivamente no hiato do 1o trimestre',
     (_sh.h[0] - _b.h[0]).toFixed(6));
  // ...e a persistencia da IS (beta1) faz ele durar mais que o proprio choque.
  ok(_sh.h[4] - _b.h[4] > 1.2, 'e beta1 acumula o choque nos trimestres seguintes',
     (_sh.h[4] - _b.h[4]).toFixed(3));
  // Caixa vazia significa "usa o default", nunca NaN -- e o que faz um cenario salvo
  // continuar valendo depois de um update do painel.
  const _vazio = MP.motorSim(_manual(_base16, 'rp', new Array(16).fill('')));
  ok(Math.abs(_vazio.h[15] - _b.h[15]) < 1e-12, 'caixa vazia cai no default do input');
  const _virg = MP.motorSim(_manual(_base16, 'rr_IS', new Array(16).fill('5,0')));
  ok(Math.abs(_virg.h[15] - _r5.h[15]) < 1e-12, 'virgula decimal e aceita nas caixas');

  console.log('\n23. Motor: horizonte e atalhos de preenchimento');
  // O buffer da eq. (5) e medido a partir de n (nn = n + folga), nao de uma data fixa, entao
  // com os MESMOS condicionantes os trimestres em comum tem de bater exatamente. Testado com
  // Selic constante justamente para isolar o buffer da questao seguinte.
  const _f8 = MP.motorSim(_const(_cfg(8), 'selic', _i0));
  const _f24 = MP.motorSim(_const(_cfg(24), 'selic', _i0));
  let _dmax = 0;
  for (let i = 0; i < 8; i++) _dmax = Math.max(_dmax, Math.abs(_f8.ipca_4t[i] - _f24.ipca_4t[i]));
  ok(_dmax < 1e-9, 'com o mesmo condicionante, o horizonte nao move os trimestres em comum',
     _dmax.toExponential(2));
  // Mas o horizonte NAO e so uma janela de exibicao: depois dele o ultimo trimestre digitado
  // se repete para sempre (o `vec()` do Python faz o mesmo). Com a curva da Focus, escolher 8
  // trimestres e dizer "a Selic para no 8o valor da Focus", nao "mostre so 8" -- por isso o
  // cenario muda de verdade. Se um dia isto passar a bater, o prolongamento quebrou.
  const _n8 = MP.motorSim(_cfg(8)), _n24 = MP.motorSim(_cfg(24));
  let _dfoc = 0;
  for (let i = 0; i < 8; i++) _dfoc = Math.max(_dfoc, Math.abs(_n8.ipca_4t[i] - _n24.ipca_4t[i]));
  ok(_dfoc > 1e-3, 'com a curva da Focus, encurtar o horizonte muda o cenario (path holding)',
     _dfoc.toExponential(2) + ' p.p.');
  ok(_n24.datas.length === 24 && _n8.datas.length === 8, 'o horizonte escolhido chega no output');
  ok(_n24.diag.resid < 1e-8, 'eq. (5) fecha tambem em 24 trimestres', _n24.diag.resid.toExponential(2));
  // Os atalhos PREENCHEM as caixas -- nao sao um modo paralelo que o motor precise conhecer.
  MP.MT_CFG.n = 16;
  MP.MT_SPEC.filter((x) => !x.escalar).map((x) => x.key)
    .forEach((k) => { MP.MT_CFG[k] = { modo: MP.MT_CFG[k].modo, vals: _cfg(16)[k].vals.slice() }; });
  MP.mtAtalho('rr_IS', 'bcb');
  ok(MP.MT_CFG.rr_IS.vals.every((v) => v === 4.8), 'atalho "mediana do BC" preenche 4,8 em todas as caixas');
  MP.mtAtalho('rr_IS', 'padrao');
  ok(Math.abs(MP.MT_CFG.rr_IS.vals[0] - _MC.ini.rr_IS) < 1e-12, 'atalho "padrao" repoe o filtrado');
  // Choque: soma X por T trimestres e depois segura ou dissipa a 0,8 -- a mesma forma do
  // choque do C2 Boxe3 Graf 4A que a aba de IRF replica.
  MP.mtAtalho('rp', 'padrao');
  const _rp0 = MP.MT_CFG.rp.vals[0];
  MP.mtChoque('rp', 1, 4, false);
  ok(Math.abs(MP.MT_CFG.rp.vals[0] - (_rp0 + 1)) < 1e-12
     && Math.abs(MP.MT_CFG.rp.vals[15] - (_rp0 + 1)) < 1e-12,
     'choque permanente soma X em todos os trimestres');
  MP.mtAtalho('rp', 'padrao');
  MP.mtChoque('rp', 1, 4, true);
  ok(Math.abs(MP.MT_CFG.rp.vals[3] - (_rp0 + 1)) < 1e-12
     && Math.abs(MP.MT_CFG.rp.vals[4] - (_rp0 + 0.8)) < 1e-12
     && Math.abs(MP.MT_CFG.rp.vals[5] - (_rp0 + 0.64)) < 1e-12,
     'choque que dissipa segue 0,8^k depois dos T trimestres',
     MP.MT_CFG.rp.vals.slice(3, 6).map((v) => (v - _rp0).toFixed(3)).join(' / '));
  MP.mtAtalho('rp', 'padrao');

  console.log('\n24. Motor: contrafactual de expectativa e de cambio');
  // A distancia entre expectativa endogena e premissa E o canal de expectativa. Se um dia
  // as duas coincidirem, ou phi degenerou ou a eq. (5) parou de entrar no caminho.
  const _semExp2 = MP.motorSim(_endog(_base16, 'pi_e', false));
  ok(Math.abs(_semExp2.ipca_4t[15] - _b.ipca_4t[15]) > 0.05,
     'ligar a eq. (5) muda o IPCA de forma visivel (canal de expectativa vivo)',
     _semExp2.ipca_4t[15].toFixed(3) + ' vs ' + _b.ipca_4t[15].toFixed(3));
  // Com o cambio pela UIP, um corte de juros deprecia (delta > 0) e o desvio Deltae^ sobe.
  const _cortes = MP.motorSim(_const(_base16, 'selic', _MC.dflt.selic_ult - 3));
  ok(_cortes.de_hat[0] > 0, 'corte de juros deprecia o cambio pela eq. (4)', _cortes.de_hat[0].toFixed(3));
  // Com o cambio manual na PPC o desvio e exatamente zero, por definicao.
  const _ppc = MP.motorSim(_endog(_base16, 'de', false));
  ok(Math.max.apply(null, _ppc.de_hat.map(Math.abs)) < 1e-12,
     'com o cambio manual no default (PPC) o desvio e identicamente zero');
}

console.log('\n25. Aba do motor: a markup gerada casa com os seletores que a fiam');
// Os cards de input sao montados por innerHTML e so DEPOIS fiados por querySelectorAll. E o
// tipo de falha que passa por `node --check` e por qualquer teste que olhe so o resultado da
// simulacao: o modelo continua certo, e a interface para de responder. Aqui a markup gerada
// e conferida contra os mesmos seletores que mtWireInputs() usa.
if (MP.MT_SPEC && MP.mtRenderInputs) {
  const _chaves = MP.MT_SPEC.map((x) => x.key);
  const _vet = MP.MT_SPEC.filter((x) => !x.escalar).map((x) => x.key);
  const _padrao = MP.mtCfgPadrao();
  // Um input no MT_SPEC sem entrada no cfg default e um input que o motor nunca le; um no
  // cfg sem card e um input que o motor le e ninguem consegue mexer.
  ok(_vet.every((k) => _padrao[k] && Array.isArray(_padrao[k].vals)),
     'todo input de caminho tem vetor no cfg padrao',
     _vet.filter((k) => !(_padrao[k] && _padrao[k].vals)).join(','));
  ok(MP.MT_SPEC.filter((x) => x.escalar).every((x) => _padrao[x.key] && 'v' in _padrao[x.key]),
     'todo input escalar tem campo v no cfg padrao');
  const _extras = Object.keys(_padrao).filter((k) => k !== 'n' && _chaves.indexOf(k) < 0);
  ok(_extras.length === 0, 'todo input do cfg padrao tem card', _extras.join(','));
  // Um key fora do MT_GRUPOS simplesmente nao e renderizado -- o card some sem erro nenhum.
  const _agrupados = MP.MT_GRUPOS.reduce((a, g) => a.concat(g.keys), []);
  ok(_chaves.every((k) => _agrupados.indexOf(k) >= 0), 'todo input do MT_SPEC esta em algum grupo',
     _chaves.filter((k) => _agrupados.indexOf(k) < 0).join(','));
  ok(_agrupados.every((k) => _chaves.indexOf(k) >= 0), 'nenhum grupo cita input inexistente',
     _agrupados.filter((k) => _chaves.indexOf(k) < 0).join(','));
  // A ordem pedida: juros, hiato, expectativas, cambio, importada, resto.
  ok(_agrupados.slice(0, 6).join(',') === 'selic,rr_IS,rr_TAY,h0,s_h,pi_e',
     'a ordem comeca por juros (Selic + as duas neutras) e depois hiato', _agrupados.slice(0, 6).join(','));
  // Todo card precisa da serie historica dele, senao "Ver grafico" abre vazio.
  const _semHist = MP.MT_SPEC.filter((x) => !(D.motor || {})[x.hist]);
  ok(_semHist.length === 0, 'todo card tem historico no payload para o grafico proprio',
     _semHist.map((x) => x.key + '->' + x.hist).join(','));
  ok(_vet.every((k) => _padrao[k].vals.length === _padrao.n),
     'os vetores nascem com uma posicao por trimestre');
  ok(MP.MT_SPEC.every((x) => !x.modoPadrao || x.modoPadrao === 'endog' || x.modoPadrao === 'manual'),
     'modoPadrao so assume endogeno ou manual');
  ok(MP.MT_SPEC.filter((x) => x.endogeno).length === 3,
     'exatamente 3 inputs tem caminho endogeno (eqs. 3, 4 e 5)');

  const _box = doc.getElementById('mt-inputs');
  MP.mtRenderInputs();
  const _html = _box.innerHTML || '';
  const _cards = (_html.match(/class="mt-card[ "]/g) || []).length;
  ok(_cards === _chaves.length, 'sai um card por input', String(_cards));
  ok((_html.match(/class="mt-grupo"/g) || []).length === MP.MT_GRUPOS.length,
     'e um cabecalho por grupo');
  // Todos nascem FECHADOS: sao treze, e a barra e o unico jeito de abrir.
  ok((_html.match(/mt-card open/g) || []).length === 0, 'os cards nascem fechados');
  ok(_chaves.every((k) => _html.indexOf('data-card="' + k + '"') >= 0),
     'toda barra de card traz o data-card que abre/fecha');
  // `data-k` + `data-h` sao literalmente os seletores do wiring das caixas de caminho.
  const _semCaixa = _vet.filter((k) =>
    (_html.match(new RegExp('data-k="' + k + '" data-h=', 'g')) || []).length !== _padrao.n);
  ok(_semCaixa.length === 0, 'todo card de caminho traz n caixas com data-k/data-h', _semCaixa.join(','));
  ok(_html.indexOf('data-k="selic" data-h="0"') >= 0
     && _html.indexOf('data-k="selic" data-h="' + (_padrao.n - 1) + '"') >= 0,
     'as caixas vao de 0 ate n-1');
  ok(_html.indexOf('data-est="h0"') >= 0, 'o input escalar do hiato inicial usa data-est');
  // Toggle Endogeno|Manual so nos 3 que tem endogeno de verdade.
  ok((_html.match(/class="mt-mode-toggle"/g) || []).length === 3,
     'o toggle Endogeno|Manual aparece so nos 3 inputs endogenos');
  // Caixa travada = input endogeno. No default, pi^e e o cambio estao endogenos.
  ok((_html.match(/mt-box-input endog/g) || []).length === 2 * _padrao.n,
     'no default as caixas de pi^e e do cambio nascem travadas',
     String((_html.match(/mt-box-input endog/g) || []).length));
  // Atalhos, painel de choque e painel de grafico, com os data-attrs do wiring.
  ok(_vet.every((k) => _html.indexOf('data-k="' + k + '" data-atalho=') >= 0),
     'todo card de caminho traz pelo menos um atalho de preenchimento');
  ok(_chaves.every((k) => _html.indexOf('data-k="' + k + '" data-painel="grafico"') >= 0),
     'todo card traz o link do grafico proprio');
  ok(_html.indexOf('data-aplica="rp"') >= 0 && _html.indexOf('data-ch="rp" data-f="x"') >= 0
     && _html.indexOf('data-ch="rp" data-f="t"') >= 0 && _html.indexOf('data-ch="rp" data-f="d"') >= 0,
     'o painel de choque traz os tres campos que o Aplicar le');
  // O atalho da projecao do Copom so faz sentido se o payload trouxer o caminho.
  ok(_html.indexOf('data-k="pi_A" data-atalho="copom"') >= 0,
     'o card de administrados traz o atalho da projecao do Copom');
  ok(((D.motor_cfg || {}).copom_adm || {}).caminho,
     'e o payload traz o caminho do Copom para ele preencher');

  // Um input endogeno nao pode aparecer com caixa editavel depois de trocar de modo.
  const _antes = MP.MT_CFG.pi_e.modo;
  MP.MT_CFG.pi_e = { modo: 'manual', vals: MP.mtCfgPadrao().pi_e.vals.slice() };
  MP.mtRenderInputs();
  const _h2 = _box.innerHTML || '';
  ok((_h2.match(/mt-box-input endog/g) || []).length === _padrao.n,
     'passar pi^e para manual destrava as caixas dele');
  MP.MT_CFG.pi_e = { modo: _antes, vals: MP.mtCfgPadrao().pi_e.vals.slice() };
  MP.mtRenderInputs();

  console.log('\n26. Cenarios salvos: lista, resumo e a referencia condicional');
  const _lista = doc.getElementById('mt-sc-list');
  MP.mtRenderCenarios();
  const _hs = _lista.innerHTML || '';
  // Sem localStorage no harness a lista vem vazia -- e a mensagem tem de dizer isso em vez
  // de renderizar um bloco em branco.
  ok(_hs.indexOf('sc-vazio') >= 0, 'sem cenarios salvos, a lista explica que esta vazia');
  // O resumo e o que distingue um cenario salvo do outro na lista.
  ok(/tudo no default/.test(MP._mtResumo(MP.mtCfgPadrao())), 'resumo do default diz "tudo no default"',
     MP._mtResumo(MP.mtCfgPadrao()));
  const _cfgTay = _endog(MP.mtCfgPadrao(), 'selic', true);
  ok(/Selic.*endógeno/.test(MP._mtResumo(_cfgTay)), 'resumo cita a troca de modo', MP._mtResumo(_cfgTay));
  const _cfgR5 = _const(MP.mtCfgPadrao(), 'rr_IS', 5);
  ok(/16T editado/.test(MP._mtResumo(_cfgR5)), 'resumo conta quantos trimestres foram editados',
     MP._mtResumo(_cfgR5));
  // A referencia endogena so entra no grafico quando o cenario ativo difere dela -- foi por
  // nao ter esta checagem que a primeira versao desenhou uma tracejada em cima da linha cheia.
  ok(MP.mtIgualPadrao(MP.mtCfgPadrao()) === true, 'o cfg default e reconhecido como igual ao padrao');
  ok(MP.mtIgualPadrao(_cfgR5) === false, 'um cfg com r* editado NAO e igual ao padrao');
  ok(MP.mtIgualPadrao(_cfgTay) === false, 'um cfg com Selic endogena NAO e igual ao padrao');
  const _cfgH0 = MP.mtClone(MP.mtCfgPadrao()); _cfgH0.h0 = { v: 2 };
  ok(MP.mtIgualPadrao(_cfgH0) === false, 'mexer na condicao inicial tambem conta como diferente');

  console.log('\n27. Graficos: historico e cenario na MESMA linha');
  // A primeira versao colava so o ULTIMO ponto observado -- desenhado num
  // eixo de 2018 a 2030 isso deixava os quatro graficos sem historico nenhum. A linha tem de
  // vir com os dois trechos, cortada em t0.
  const _res = MP.motorSim(MP.mtCfgPadrao());
  const _lin = MP._mtLinha('ipca_4t', 'ipca_4t', _res);
  ok(_lin.dates.length > _res.n + 12, 'a linha traz historico ALEM do trecho simulado',
     _lin.dates.length + ' pontos para ' + _res.n + ' trimestres de cenario');
  ok(_lin.values.every((v) => v != null), 'a linha nao carrega nulos (cauda de NaN do painel filtrada)');
  ok(_lin.dates[_lin.dates.length - 1] === _res.datas[_res.n - 1], 'a linha termina no fim do horizonte');
  // Nenhuma data pode aparecer duas vezes: historico e cenario nao podem se sobrepor em t0.
  const _vistas = {};
  const _dup = _lin.dates.filter((d) => (_vistas[d] = (_vistas[d] || 0) + 1) > 1);
  ok(_dup.length === 0, 'historico e cenario nao se sobrepoem', _dup.join(','));
  // Ordem crescente -- um x fora de ordem faz o Plotly desenhar a linha voltando.
  let _cresc = true;
  for (let i = 1; i < _lin.dates.length; i++) if (_lin.dates[i] <= _lin.dates[i - 1]) _cresc = false;
  ok(_cresc, 'as datas da linha sao estritamente crescentes');
  // O corte visual da projecao tem de cair no primeiro trimestre simulado.
  const _sh2 = MP._mtShapes(_res);
  ok(_sh2.shapes[0].x0 === _res.datas[0] && _sh2.annotations[0].x === _res.datas[0],
     'a marca de "projecao" fica no primeiro trimestre simulado');
}

console.log('\n28. Aba do motor: os cliques fazem o que prometem (fiamento de verdade)');
// As secoes acima conferem o MODELO e a MARKUP. Esta dispara os eventos de fato contra a
// arvore parseada e olha o que mudou em MT_CFG / MT_RES / nos traces do Plotly -- a mesma
// exigencia que .claude/rules/lis-dashboards.md faz depois dos dois bugs de botao de range
// que passaram por checagem de sintaxe.
if (MP.MT_SPEC && doc._els['mt-inputs']) {
  const _box = doc.getElementById('mt-inputs');
  const _q = (sel) => _box.querySelectorAll(sel);
  const _um = (sel) => { const r = _q(sel); return r.length ? r[0] : null; };
  const _traces = (div) => {
    const c = chamadas.filter((x) => x.tipo === 'react' && x.divId === div).pop();
    return c ? c.traces : [];
  };

  // Ponto de partida limpo -- e ja testa o botao Restaurar padrao.
  doc.getElementById('mt-reset').fire('click');
  ok(MP.mtIgualPadrao(MP.MT_CFG), 'Restaurar padrao devolve a config ao default');

  // ── toggle Endogeno|Manual ──
  const _pieBtns = _q('.mt-mode-btn').filter((b) => b.parentNode.dataset.k === 'pi_e');
  ok(_pieBtns.length === 2, 'pi^e tem os dois botoes de modo');
  const _manualBtn = _pieBtns.filter((b) => b.dataset.modo === 'manual')[0];
  const _pieEndog = MP.MT_RES.pi_e.slice();
  _manualBtn.fire('click');
  ok(MP.MT_CFG.pi_e.modo === 'manual', 'clicar em Manual troca o modo na config');
  ok(MP.MT_RES.diag.eq5 === false, 'e o motor passa a tratar pi^e como premissa');
  // Sair do endogeno tem de herdar o caminho resolvido -- editar parte de onde o modelo
  // esta, nao do zero (mesmo principio do "pre-preenchido" do FX Report).
  ok(Math.abs(MP.MT_CFG.pi_e.vals[0] - _pieEndog[0]) < 1e-9
     && Math.abs(MP.MT_CFG.pi_e.vals[15] - _pieEndog[15]) < 1e-9,
     'as caixas herdam o caminho que o modelo tinha resolvido',
     MP.MT_CFG.pi_e.vals[15] + ' vs ' + _pieEndog[15]);
  // ...e por herdarem, o resultado nao pode dar um salto so por trocar o modo.
  ok(Math.abs(MP.MT_RES.ipca_4t[15] - 3.6166) < 0.02,
     'trocar para manual herdando o caminho nao muda o cenario',
     MP.MT_RES.ipca_4t[15].toFixed(4));
  ok(_q('.mt-box-input[data-k="pi_e"]').every((i) => !i.disabled),
     'as caixas de pi^e ficam editaveis no modo manual');
  _q('.mt-mode-btn').filter((b) => b.parentNode.dataset.k === 'pi_e' && b.dataset.modo === 'endog')[0].fire('click');
  ok(MP.MT_CFG.pi_e.modo === 'endog' && MP.MT_RES.diag.eq5 === true, 'e volta para endogeno');
  ok(_q('.mt-box-input[data-k="pi_e"]').every((i) => i.disabled),
     'no modo endogeno as caixas voltam travadas');

  // ── atalho preenche as caixas ──
  const _bcb = _q('.mt-link[data-atalho]').filter((l) => l.dataset.k === 'rr_IS' && l.dataset.atalho === 'bcb')[0];
  ok(!!_bcb, 'o atalho da mediana do BC existe no card de r*');
  const _ipcaAntes = MP.MT_RES.ipca_4t[15];
  _bcb.fire('click');
  ok(MP.MT_CFG.rr_IS.vals.every((v) => v === 4.8), 'o atalho escreve 4,8 em todas as caixas de r*');
  ok(Math.abs(MP.MT_RES.rr_IS[0] - 4.8) < 1e-12, 'e o motor le o valor novo');
  ok(MP.MT_RES.ipca_4t[15] < _ipcaAntes - 0.5, 'r* menor derruba a inflacao do cenario',
     _ipcaAntes.toFixed(2) + ' -> ' + MP.MT_RES.ipca_4t[15].toFixed(2));
  ok(_um('.mt-box-input[data-k="rr_IS"]').value === '4,80',
     'a caixa mostra o valor com virgula decimal', _um('.mt-box-input[data-k="rr_IS"]').value);

  // ── digitar numa caixa ──
  const _cx = _q('.mt-box-input[data-k="rr_IS"]')[3];
  _cx.value = '6,5';
  _cx.fire('change');
  ok(MP.MT_CFG.rr_IS.vals[3] === '6,5', 'o change da caixa grava o que foi digitado');
  ok(Math.abs(MP.MT_RES.rr_IS[3] - 6.5) < 1e-12, 'e o motor re-simula com ele',
     String(MP.MT_RES.rr_IS[3]));

  // ── painel de choque ──
  _q('.mt-link[data-painel]').filter((l) => l.dataset.k === 'rp' && l.dataset.painel === 'choque')[0].fire('click');
  ok(_um('[data-painel-de="rp|choque"]').classList.contains('open'), 'o link abre o painel de choque');
  const _rpAntes = MP.MT_CFG.rp.vals[0];
  _um('[data-ch="rp"][data-f="x"]').value = '2';
  _um('[data-ch="rp"][data-f="t"]').value = '4';
  _um('[data-ch="rp"][data-f="d"]').value = '1';
  _um('.mt-link[data-aplica="rp"]').fire('click');
  ok(Math.abs(MP.MT_CFG.rp.vals[0] - (_rpAntes + 2)) < 1e-9, 'Aplicar soma o choque nas caixas',
     String(MP.MT_CFG.rp.vals[0]));
  ok(Math.abs(MP.MT_CFG.rp.vals[4] - (_rpAntes + 1.6)) < 1e-9,
     'e a dissipacao 0,8/tri comeca depois dos T trimestres', String(MP.MT_CFG.rp.vals[4]));

  // ── condicoes iniciais ──
  const _h0 = _um('.mt-box-input[data-est="h0"]');
  _h0.value = '2';
  _h0.fire('change');
  ok(MP.MT_CFG.h0.v === '2' && Math.abs(MP.MT_RES.h0 - 2) < 1e-12,
     'a caixa do hiato inicial chega no motor');
  // Limpar a caixa e o jeito de voltar ao filtrado: vazio significa "usa o default".
  _h0.value = '';
  _h0.fire('change');
  ok(Math.abs(MP.MT_RES.h0 - D.motor_cfg.ini.h) < 1e-12,
     'esvaziar a caixa devolve o estado do filtro');
  // s^h agora e caminho, entao tem grade e atalhos como os demais.
  ok(_q('.mt-box-input[data-k="s_h"]').length === MP.MT_CFG.n,
     'o choque no hiato tem uma caixa por trimestre');
  _q('.mt-link[data-atalho]').filter((l) => l.dataset.k === 's_h' && l.dataset.atalho === 'zero')[0].fire('click');
  ok(MP.MT_CFG.s_h.vals.every((v) => v === 0) && Math.abs(MP.MT_RES.s_h[0]) < 1e-12,
     'zerar o choque no hiato chega no motor');
  _q('.mt-link[data-atalho]').filter((l) => l.dataset.k === 's_h' && l.dataset.atalho === 'padrao')[0].fire('click');
  // A projecao de administrados do Copom: o atalho preenche as caixas com o caminho do payload.
  const _cop = (D.motor_cfg.copom_adm || {}).caminho;
  _q('.mt-link[data-atalho]').filter((l) => l.dataset.k === 'pi_A' && l.dataset.atalho === 'copom')[0].fire('click');
  ok(Math.abs(MP.MT_CFG.pi_A.vals[0] - _cop[0]) < 1e-9
     && Math.abs(MP.MT_RES.pi_A[0] - _cop[0]) < 1e-9,
     'o atalho da projecao do Copom preenche administrados', String(MP.MT_CFG.pi_A.vals[0]));
  _q('.mt-link[data-atalho]').filter((l) => l.dataset.k === 'pi_A' && l.dataset.atalho === 'padrao')[0].fire('click');

  // ── horizonte ──
  const _sel = doc.getElementById('mt-horizonte');
  _sel.value = '24';
  _sel.fire('change');
  ok(MP.MT_CFG.n === 24 && MP.MT_RES.n === 24, 'trocar o horizonte re-simula com o novo n');
  ok(MP.MT_CFG.rr_IS.vals.length === 24, 'os vetores sao redimensionados, nao descartados');
  ok(MP.MT_CFG.rr_IS.vals[3] === '6,5', 'e o que ja tinha sido digitado sobrevive');
  ok(_q('.mt-box-input[data-k="rr_IS"]').length === 24, 'a grade passa a ter 24 caixas');
  _sel.value = '16'; _sel.fire('change');

  // ── cenarios salvos: salvar, plotar, editar, excluir ──
  const _tracesAntes = _traces('chart-mt-infl').length;
  doc.getElementById('mt-sc-novo').fire('click');
  doc.getElementById('mt-sc-nome').value = 'r* na mediana do BC';
  doc.getElementById('mt-sc-racional').value = 'Testa se a Selic de hoje aperta com r* em 4,8%.';
  doc.getElementById('mt-sc-salvar').fire('click');
  const _lista = doc.getElementById('mt-sc-list');
  ok(_lista.querySelectorAll('.sc-card').length === 1, 'salvar cria um card na lista');
  ok(_lista.innerHTML.indexOf('r* na mediana do BC') >= 0, 'com o nome que foi digitado');
  ok(_lista.innerHTML.indexOf('Testa se a Selic') >= 0, 'e com o racional');
  // Salvar ja marca o cenario para plotar, entao o grafico ganha uma linha.
  ok(_traces('chart-mt-infl').length === _tracesAntes + 1,
     'o cenario salvo entra como uma linha a mais no grafico',
     _tracesAntes + ' -> ' + _traces('chart-mt-infl').length);
  const _cb = _lista.querySelector('input[data-plot]');
  _cb.checked = false;
  _cb.fire('change');
  ok(_traces('chart-mt-infl').length === _tracesAntes,
     'desmarcar Plotar tira a linha sem mexer nas caixas');
  ok(MP.MT_CFG.rr_IS.vals[3] === '6,5', 'e as caixas continuam como estavam');

  // Carregar traz as premissas de volta; primeiro sujamos a config para haver o que voltar.
  doc.getElementById('mt-reset').fire('click');
  ok(MP.mtIgualPadrao(MP.MT_CFG), 'reset antes do carregar');
  _lista.querySelectorAll('.sc-btn').filter((b) => b.dataset.acao === 'load')[0].fire('click');
  ok(MP.MT_CFG.rr_IS.vals[3] === '6,5' && MP.MT_CFG.rr_IS.vals[0] === 4.8,
     'Carregar devolve as premissas gravadas para as caixas');

  // Editar carrega e troca o botao para Atualizar; salvar de novo NAO cria um segundo card.
  _lista.querySelectorAll('.sc-btn').filter((b) => b.dataset.acao === 'edit')[0].fire('click');
  ok(doc.getElementById('mt-sc-salvar').textContent === 'Atualizar',
     'Editar troca o botao do formulario para Atualizar');
  doc.getElementById('mt-sc-nome').value = 'r* na mediana do BC (v2)';
  doc.getElementById('mt-sc-salvar').fire('click');
  ok(_lista.querySelectorAll('.sc-card').length === 1, 'Atualizar regrava no MESMO cenario');
  ok(_lista.innerHTML.indexOf('(v2)') >= 0, 'com o nome novo');
  ok(_lista.innerHTML.indexOf('editado') >= 0, 'e marcando que foi editado');
  ok(doc.getElementById('mt-sc-salvar').textContent === 'Salvar', 'e o botao volta a Salvar');

  _lista.querySelectorAll('.sc-btn').filter((b) => b.dataset.acao === 'del')[0].fire('click');
  ok(_lista.querySelectorAll('.sc-card').length === 0, 'Excluir remove o card');
  ok(_lista.innerHTML.indexOf('sc-vazio') >= 0, 'e a lista volta a dizer que esta vazia');

  // ── a referencia so aparece quando ha diferenca ──
  doc.getElementById('mt-reset').fire('click');
  const _nRef = _traces('chart-mt-infl').filter((t) => /Referência/.test(t.name)).length;
  ok(_nRef === 0, 'no default a referencia endogena nao e desenhada (seria uma linha em cima da outra)');
  _q('.mt-link[data-atalho]').filter((l) => l.dataset.k === 'rr_IS' && l.dataset.atalho === 'bcb')[0].fire('click');
  ok(_traces('chart-mt-infl').filter((t) => /Referência/.test(t.name)).length === 1,
     'e passa a ser desenhada assim que o cenario difere');
  doc.getElementById('mt-reset').fire('click');
}

console.log('\n29. Abre/fecha, faixa de projecao e a inflacao importada como IC-Br');
if (MP.MT_SPEC && doc._els['mt-inputs']) {
  const _box2 = doc.getElementById('mt-inputs');
  // ── cards abrem e fecham pela barra ──
  const _bar = _box2.querySelectorAll('.mt-card-bar').filter((b) => b.dataset.card === 'selic')[0];
  const _card = doc.getElementById('mt-card-selic');
  ok(!_card.classList.contains('open'), 'o card nasce fechado');
  _bar.fire('click');
  ok(_card.classList.contains('open'), 'clicar na barra abre o card');
  _bar.fire('click');
  ok(!_card.classList.contains('open'), 'e clicar de novo fecha');
  // "Abrir/fechar todos" opera os treze de uma vez.
  doc.getElementById('mt-abrir-tudo').fire('click');
  ok(MP.MT_SPEC.every((sp) => (_box2.innerHTML || '').indexOf('mt-card is-endog open') >= 0
       || (_box2.innerHTML || '').indexOf('mt-card open') >= 0),
     'Abrir/fechar todos abre os cards');
  ok((_box2.innerHTML.match(/mt-card[^"]* open/g) || []).length === MP.MT_SPEC.length,
     'todos os cards abrem juntos',
     String((_box2.innerHTML.match(/mt-card[^"]* open/g) || []).length));
  doc.getElementById('mt-abrir-tudo').fire('click');
  ok((_box2.innerHTML.match(/mt-card[^"]* open/g) || []).length === 0, 'e fecham juntos');

  // ── graficos abrem e fecham; so o titulo e clicavel ──
  const _slot = doc.getElementById('slot-chart-mt-hiato');
  const _hit = doc.getElementById('hit-chart-mt-hiato');
  ok(!!_hit, 'o titulo do grafico e a area clicavel');
  ok(!_slot.classList.contains('open'), 'os graficos alem do primeiro nascem fechados');
  ok(doc.getElementById('slot-chart-mt-infl').classList.contains('open'),
     'o primeiro grafico nasce aberto');
  _hit.fire('click');
  ok(_slot.classList.contains('open'), 'clicar no titulo abre o grafico');
  // Um Plotly desenhado escondido sai com largura zero: abrir tem de forcar o resize.
  const _antesResize = chamadas.filter((c) => c.tipo === 'resize').length;
  _hit.fire('click'); _hit.fire('click');
  ok(chamadas.filter((c) => c.tipo === 'resize').length > _antesResize,
     'abrir um grafico dispara o resize do Plotly');

  // ── faixa cinza sobre a projecao ──
  const _res2 = MP.motorSim(MP.mtCfgPadrao());
  const _sh3 = MP._mtShapes(_res2);
  const _rects = _sh3.shapes.filter((x) => x.type === 'rect');
  ok(_rects.length === 2, 'a faixa de projecao vem em duas partes (dentro/fora do HR)');
  ok(_rects[0].x0 === _res2.datas[0] && _rects[1].x1 === _res2.datas[_res2.n - 1],
     'e juntas cobrem exatamente o trecho simulado');
  ok(_rects[0].x1 === _rects[1].x0, 'as duas se encontram sem buraco no meio');
  ok(_rects.every((r) => r.layer === 'below'),
     'e ficam ATRAS das series (senao lavam a cor das linhas)');
  ok(_sh3.shapes.filter((x) => x.type === 'line').length === 2,
     'duas linhas verticais: o corte em t0 e o horizonte relevante');

  // ── o choque persistente saiu do grafico do hiato ──
  const _tH = (chamadas.filter((c) => c.tipo === 'react' && c.divId === 'chart-mt-hiato').pop() || {}).traces || [];
  ok(_tH.length >= 1 && _tH.every((t) => !/s\^h|persistente/i.test(t.name)),
     'o grafico do hiato nao carrega mais o choque persistente',
     _tH.map((t) => t.name).join(' | '));

  // ── inflacao importada = IC-Br, e o default e meta/4 (nao zero) ──
  const _b2 = MP.motorSim(MP.mtCfgPadrao());
  const _meta4 = D.motor_cfg.meta[0] / 4;
  ok(Math.abs(_b2.icbr[0] - _meta4) < 1e-12,
     'o default do IC-Br e a meta/4 (variacao consistente com pi* = 0)', String(_b2.icbr[0]));
  ok(Math.abs(_b2.pi_star[0]) < 1e-12, 'que e exatamente pi* = 0 na Phillips');
  // Digitar 0 no indice JA e choque desinflacionario -- e a armadilha que o card avisa.
  const _icbr0 = MP.motorSim(_const(MP.mtCfgPadrao(), 'icbr', 0));
  ok(Math.abs(_icbr0.pi_star[0] + _meta4) < 1e-12, 'indice parado significa pi* = -meta/4');
  ok(_icbr0.pi_L[15] < _b2.pi_L[15], 'e derruba a inflacao de livres');
  // O historico do card e a variacao do indice, nao o pi* cru: diferem pela meta/4.
  const _hIc = (D.motor || {}).icbr || {values: []};
  const _hPi = (D.motor || {}).pi_star || {values: []};
  let _k = _hIc.values.length - 1;
  while (_k > 0 && (_hIc.values[_k] == null || _hPi.values[_k] == null)) _k--;
  ok(Math.abs((_hIc.values[_k] - _hPi.values[_k]) - _meta4) < 1e-3,
     'o historico do IC-Br e o pi* do painel mais a meta/4',
     (_hIc.values[_k] - _hPi.values[_k]).toFixed(4));
}

console.log('\n30. Marcacao do horizonte relevante');
if (MP._mtHR && MP.mtNotaHR) {
  const _r = MP.motorSim(MP.mtCfgPadrao());
  const _pubOrig = (D.motor_cfg || {}).hr;

  ok(MP.MT_HR_TRI === 6, 'a regra de fallback e de 6 trimestres (Decreto 12.079/2024)');
  // ── a fonte publicada ganha quando cai dentro da janela ──
  if (_pubOrig && _pubOrig.date) {
    ok(_pubOrig.trimestres === 6,
       'o HR que veio no payload e mesmo o regime de 6 trimestres', String(_pubOrig.trimestres));
    ok(_pubOrig.reuniao > 0, 'e diz qual reuniao o declarou', String(_pubOrig.reuniao));
    const _hr = MP._mtHR(_r);
    ok(_hr.date === _pubOrig.date, 'o marcador usa a data que o Copom publicou', _hr.date);
    ok(_hr.reuniao === _pubOrig.reuniao, 'e guarda de qual reuniao ela veio', String(_hr.reuniao));
    ok(_r.datas.indexOf(_hr.date) === _hr.i, 'o indice devolvido aponta para a mesma data');
    ok(_hr.i >= 0 && _hr.i < _r.n, 'e cai DENTRO da janela simulada', _hr.i + '/' + _r.n);
  }

  // ── sem payload, vale a regra dos 6 trimestres ──
  D.motor_cfg.hr = {};
  const _reg = MP._mtHR(_r);
  ok(_reg.i === 6 && _reg.date === _r.datas[6],
     'sem data publicada o marcador cai em datas[6]', _reg.date);
  ok(_reg.reuniao === null, 'e nao inventa reuniao nenhuma');
  // Uma data publicada VELHA (fora da janela) tambem cai na regra: nao pode virar um
  // marcador plantado no historico.
  D.motor_cfg.hr = {date: '1999-01-01', reuniao: 42, trimestres: 6};
  const _velho = MP._mtHR(_r);
  ok(_velho.date === _r.datas[6] && _velho.reuniao === null,
     'data publicada fora da janela e descartada em favor da regra', _velho.date);
  // Horizonte curto: a regra nunca pode apontar para fora do vetor.
  D.motor_cfg.hr = {};
  const _cfgC = MP.mtCfgPadrao(); _cfgC.n = 8;
  const _curto = MP.motorSim(_cfgC);
  const _hrC = MP._mtHR(_curto);
  ok(_hrC.i < _curto.n && _hrC.date === _curto.datas[_hrC.i],
     'com horizonte de 8T o marcador continua dentro do vetor', _hrC.i + '/' + _curto.n);
  D.motor_cfg.hr = _pubOrig;

  // ── a faixa escurece DENTRO do horizonte e clareia depois ──
  const _sh = MP._mtShapes(_r), _hr2 = MP._mtHR(_r);
  const _rs = _sh.shapes.filter((x) => x.type === 'rect');
  ok(_rs[0].x1 === _hr2.date && _rs[1].x0 === _hr2.date, 'a faixa e cortada no HR');
  const _alfa = (r) => parseFloat(String(r.fillcolor).split(',').pop());
  ok(_alfa(_rs[0]) > _alfa(_rs[1]),
     'e o trecho de dentro do HR e o mais escuro dos dois',
     _alfa(_rs[0]) + ' vs ' + _alfa(_rs[1]));
  const _ln = _sh.shapes.filter((x) => x.type === 'line');
  ok(_ln.some((l) => l.x0 === _hr2.date && l.x1 === _hr2.date && l.line.dash === 'dash'),
     'ha uma vertical tracejada em cima do HR');
  ok(_ln.some((l) => l.x0 === _r.datas[0] && l.line.dash === 'dot'),
     'e a pontilhada de t0 continua, com tracejado diferente para nao confundir');
  const _anHR = _sh.annotations.filter((a) => /horizonte relevante/.test(a.text))[0];
  ok(!!_anHR && _anHR.x === _hr2.date, 'o rotulo do HR fica na propria linha');
  ok(_anHR.xanchor === 'left', 'e aponta para a direita quando ha espaco sobrando');
  // Perto da borda direita o rotulo tem de virar, senao o texto sai do quadro.
  const _perto = MP._mtShapes(Object.assign({}, _r, {n: _hr2.i + 2}));
  const _anP = _perto.annotations.filter((a) => /horizonte relevante/.test(a.text))[0];
  ok(_anP.xanchor === 'right', 'com o HR colado na borda o rotulo vira para a esquerda');

  // ── a nota embaixo dos graficos ──
  const _nota = doc.getElementById('mt-hr-nota');
  ok(!!_nota, 'a nota do HR tem lugar no HTML');
  if (_nota) {
    MP.mtNotaHR(_r);
    const _t = _nota.innerHTML || '';
    ok(/Decreto 12\.079/.test(_t), 'a nota cita o decreto que fixou o regime', _t.slice(0, 80));
    if (_pubOrig && _pubOrig.reuniao) {
      ok(_t.indexOf(String(_pubOrig.reuniao)) >= 0,
         'e diz qual reuniao marcou o horizonte', _t.slice(0, 110));
    }
    // Sem payload a nota tem de MUDAR de texto, nao repetir a versao publicada.
    D.motor_cfg.hr = {};
    MP.mtNotaHR(_r);
    ok((_nota.innerHTML || '') !== _t, 'sem data publicada a nota troca de texto');
    ok(/regra/.test(_nota.innerHTML || ''), 'avisando que vale a regra, com todas as letras');
    D.motor_cfg.hr = _pubOrig;
    MP.mtNotaHR(_r);
  }
}

console.log('\n31. Apendice: a descricao do modelo sai do payload, nao de texto fixo');
// A secao "O modelo, equacao por equacao" escreve cada equacao com o COEFICIENTE
// ESTIMADO no lugar do simbolo. O modo de falhar dela e silencioso: reestimar o modelo e
// a prosa continuar mostrando o numero velho porque alguem digitou o valor no HTML. O que
// os testes abaixo cobram e justamente que os numeros na tela venham de D.info.params.
MP.RENDERERS.appendix();
const _mod = doc._els['modelo-desc'];
const _modHtml = (_mod && _mod.innerHTML) || '';
ok(_modHtml.length > 3000, 'renderModelo preenche #modelo-desc', String(_modHtml.length));

const _itens = _mod.querySelectorAll('details.appendix-item');
ok(_itens.length === 10, 'os 10 blocos click-drop sao montados', String(_itens.length));
ok(_itens.every((d) => d.querySelector('summary') && d.querySelector('.appendix-body')),
   'cada bloco tem titulo clicavel e corpo');
const _eqs = _mod.querySelectorAll('.eq');
ok(_eqs.length >= 14, 'as equacoes (1) a (9) e as auxiliares aparecem como bloco proprio',
   String(_eqs.length));
ok(_mod.querySelectorAll('.eq .n').length === _eqs.length, 'toda equacao vem numerada');

// Os coeficientes: cada um tem de aparecer NA TELA com o valor do payload.
const _P = ((MP.D || {}).info || {}).params || {};
const _fb = MP.fmtBR;
[['a1L', 3], ['a1I', 3], ['a2', 3], ['a3', 4], ['a4', 3], ['b1', 3], ['b2', 3],
 ['b5', 3], ['t1', 3], ['t3', 3], ['delta', 2], ['gn', 2], ['ge', 2], ['gc', 2],
 ['f1', 3], ['f2', 3], ['f3', 3]].forEach(([k, d]) => {
  ok(_modHtml.indexOf('<b>' + _fb(_P[k], d) + '</b>') >= 0,
     'o coeficiente ' + k + ' aparece com o valor estimado (' + _fb(_P[k], d) + ')');
});
// Os pesos implicitos: nao estao em params, tem de ser CALCULADOS na tela.
ok(_modHtml.indexOf('<b>' + _fb(1 - _P.a1L - _P.a1I, 3) + '</b>') >= 0,
   'o peso da expectativa na Phillips sai de 1-a1L-a1I');
ok(_modHtml.indexOf('<b>' + _fb(1 - _P.t1 - _P.t2, 3) + '</b>') >= 0,
   'o peso do bloco de longo prazo na Taylor sai de 1-t1-t2');

// Estado latente marcado: e o que separa "o filtro recupera" de "e dado observado".
ok(_mod.querySelectorAll('.eq .lat').length >= 8,
   'os estados latentes vem destacados dentro das equacoes',
   String(_mod.querySelectorAll('.eq .lat').length));

// A tabela de choques: sao os parametros que a Tabela 1 do BC nao publica, entao nao
// aparecem em lugar nenhum alem daqui.
const _tabc = _mod.querySelectorAll('.par-table tbody tr');
ok(_tabc.length === 8, 'a tabela de choques e ruidos tem as 8 linhas', String(_tabc.length));
[['s_h', 4], ['k08', 2], ['k20', 2], ['s_pi', 4], ['k_pi', 2], ['s_i', 4], ['s_e', 3]]
  .forEach(([k, d]) => {
    ok(_modHtml.indexOf('>' + _fb(_P[k], d) + '<') >= 0,
       'a variancia ' + k + ' aparece na tabela (' + _fb(_P[k], d) + ')');
  });
ok(_modHtml.indexOf('>' + _fb(((MP.D || {}).info || {}).sigma_rr, 4) + '<') >= 0,
   'e o sigma(eps_r*) calibrado tambem');

// Os numeros de diagnostico que a secao cita.
const _I = ((MP.D || {}).info || {});
ok(_modHtml.indexOf(_fb(_I.hiato_corr, 3)) >= 0, 'a correlacao do hiato vem do payload');
ok(_modHtml.indexOf(_fb(_I.r_is_hoje, 2)) >= 0, 'o r* corrente da IS vem do payload');
ok(_modHtml.indexOf(_fb((_I.eq5 || {}).raio, 2)) >= 0,
   'o raio espectral da eq. (5) vem do payload');
ok((doc._els['mod-lead'].innerHTML || '').indexOf(_I.ultimo_tri.replace('Q', 'T')) >= 0,
   'a chamada da secao diz ate quando os estados foram estendidos');

// A nota antiga afirmava que a eq. (5) estava FORA do modelo e que Fair-Taylor divergira
// por instabilidade genuina -- as duas deixaram de valer. Um apendice que se contradiz e
// pior que um incompleto, entao o texto antigo nao pode ter sobrado.
const _raw = fs.readFileSync(HTML, 'utf8');
ok(_raw.indexOf('Por que a equação (5) está fora') < 0,
   'a nota desatualizada da eq. (5) saiu do apendice');
ok(_raw.indexOf('o que mudou desde a réplica anterior') >= 0,
   'e foi trocada pela nota de historico, que reconcilia a afirmacao antiga');

console.log('\n32. Aba Condicoes: o anacronismo e a cor');
// A afirmacao que a aba inteira faz e uma so: a coluna "na reuniao" so contem dado que ja
// tinha sido DIVULGADO quando o Copom decidiu. E ela e verificavel do proprio payload,
// porque `div_ant`/`div_hoje` carregam a data de divulgacao que justifica cada celula --
// e por isso que elas estao la, e nao so para o tooltip.
{
  const Q = MP.D.condicoes || {};
  ok(!!Q.linhas && Q.linhas.length > 0, 'payload de condicoes populado',
     JSON.stringify(Object.keys(Q)));

  // "05/08/2026 18:30" -> Date. Formato BR, montado no Python.
  function brDate(s) {
    if (!s) return null;
    const m = /^(\d{2})\/(\d{2})\/(\d{4})(?:\s+(\d{2}):(\d{2}))?$/.exec(String(s));
    if (!m) return null;
    return new Date(+m[3], +m[2] - 1, +m[1], m[4] ? +m[4] : 0, m[5] ? +m[5] : 0);
  }
  const corteAnt = brDate(Q.ant.corte);
  ok(!!corteAnt, 'corte da reuniao anterior chega como datetime', String(Q.ant.corte));

  const comDiv = Q.linhas.filter((l) => l.div_ant);
  ok(comDiv.length > 0, 'ha linhas indexadas por periodo de referencia no payload');
  comDiv.forEach((l) => {
    ok(brDate(l.div_ant) <= corteAnt,
       '"' + l.label + '" na reuniao: divulgado ' + l.div_ant + ' <= corte ' + Q.ant.corte);
  });
  // E a coluna de hoje nao pode usar dado que ainda nao saiu.
  const agora = new Date();
  comDiv.forEach((l) => {
    if (l.div_hoje) ok(brDate(l.div_hoje) <= agora,
      '"' + l.label + '" hoje: divulgado ' + l.div_hoje + ', ja no passado');
  });

  // A proxima reuniao tem que estar a frente da anterior, e o rotulo da Focus so pode
  // apontar para ela -- foi assim que se descobriu que "Selic da proxima reuniao" comparava
  // DUAS reunioes diferentes se o rotulo fosse recalculado em cada corte.
  ok(new Date(Q.prox.date) > new Date(Q.ant.date), 'proxima reuniao e depois da anterior');
  ok(Q.prox.numero == null || Q.prox.numero === Q.ant.numero + 1,
     'numeracao das reunioes e consecutiva', Q.ant.numero + ' -> ' + Q.prox.numero);

  // As 4 categorias do resumo particionam as linhas com dado: contar "sem dado novo"
  // junto com "neutro" foi bug numa primeira versao -- mudez nao e ausencia de movimento.
  const R = Q.resumo;
  ok(R.hawkish + R.dovish + R.neutro + R.sem_leitura + R.sem_dado === Q.linhas.length,
     'resumo particiona as linhas',
     [R.hawkish, R.dovish, R.neutro, R.sem_leitura, R.sem_dado, Q.linhas.length].join('/'));
  const semDado = Q.linhas.filter((l) => l.novos === 0);
  semDado.forEach((l) => {
    ok(l.ref_ant === l.ref_hoje,
       '"' + l.label + '" sem dado novo tem a MESMA referencia nas duas colunas',
       l.ref_ant + ' vs ' + l.ref_hoje);
    ok(l.delta === 0, '"' + l.label + '" sem dado novo tem delta zero');
  });
  // Sinal 0 = sem leitura hawk/dove. Nunca pode sair com z, ou a Selic esperada da Focus
  // seria colorida pela propria reacao a decisao passada -- circular.
  Q.linhas.filter((l) => l.sinal === 0).forEach((l) => {
    ok(l.z == null, '"' + l.label + '" (sinal 0) nao recebe z', String(l.z));
  });
  // E toda linha com sinal e dado novo TEM que ter z: sem ele a celula sai branca e se
  // confunde com "nada mudou".
  Q.linhas.filter((l) => l.sinal !== 0 && l.novos > 0 && !l.erro).forEach((l) => {
    ok(typeof l.z === 'number', '"' + l.label + '" com dado novo recebe z', String(l.z));
    ok(Math.abs(l.z) <= 3.0001, '"' + l.label + '" tem z limitado a +-3', String(l.z));
  });

  // Nivel de preco entra em variacao PERCENTUAL: se o delta viesse em pontos, a celula
  // diria "+0,04" ao lado de uma PTAX de 5,15 e seria lida como quatro centavos -- e o z
  // estaria dividindo centavos por um sigma medido em log. Os dois tem de mudar juntos.
  Q.linhas.filter((l) => l.delta_pct && l.novos > 0).forEach((l) => {
    const esperado = (l.hoje / l.ant - 1) * 100;
    ok(Math.abs(l.delta - esperado) < 1e-6,
       '"' + l.label + '" tem delta em %, nao em pontos',
       l.delta + ' vs ' + esperado.toFixed(6));
    ok(Math.abs(l.delta) < Math.abs(l.hoje - l.ant) * 100,
       '"' + l.label + '" nao esta com o delta em nivel disfarcado de %');
  });
  const _pct = Q.linhas.filter((l) => l.delta_pct).map((l) => l.key);
  ok(_pct.length > 0 && _pct.indexOf('ptax') >= 0,
     'o cambio e a linha em variacao percentual', JSON.stringify(_pct));

  // cdCor: vermelho = hawkish, azul = dovish, nada = sem leitura.
  ok(MP.cdCor(2).indexOf('234,82,58') === 0 || MP.cdCor(2).indexOf('rgba(234,82,58') === 0,
     'z positivo pinta de laranja/vermelho', MP.cdCor(2));
  ok(MP.cdCor(-2).indexOf('rgba(2,115,155') === 0, 'z negativo pinta de azul', MP.cdCor(-2));
  ok(MP.cdCor(null) === 'transparent', 'z nulo nao pinta');
  const _a3 = parseFloat(MP.cdCor(3).split(',')[3]);
  const _a1 = parseFloat(MP.cdCor(1).split(',')[3]);
  ok(_a3 > _a1, 'saturacao cresce com |z|', _a1 + ' -> ' + _a3);

  // cdVeredito: a ordem dos testes e o ponto. Sem dado novo tem z=0 por construcao, e sem
  // o teste vir antes a linha sairia rotulada "em linha" -- afirmando que ela nao mexeu.
  ok(MP.cdVeredito({novos: 0, z: 0}).txt === 'sem dado novo',
     'sem dado novo vence o z=0', MP.cdVeredito({novos: 0, z: 0}).txt);
  ok(MP.cdVeredito({novos: 3, z: 0}).txt === 'em linha', 'z zero COM dado novo e "em linha"');
  ok(MP.cdVeredito({novos: 3, z: 1}).cls === 'cd-hawk', 'z positivo e hawkish');
  ok(MP.cdVeredito({novos: 3, z: -1}).cls === 'cd-dove', 'z negativo e dovish');
  ok(MP.cdVeredito({novos: 3, z: null}).txt === 'reação de mercado', 'sinal 0 vira reacao');

  // Markup: uma linha por variavel + um cabecalho por bloco, e a celula de hoje pintada.
  MP.RENDERERS.condicoes();
  const _tab = doc.getElementById('cd-tabela');
  const _trs = _tab.querySelectorAll('tr');
  const _blocos = _trs.filter((t) => t.classList.contains('cd-bloco'));
  const _nBlocos = new Set(Q.linhas.map((l) => l.bloco)).size;
  ok(_blocos.length === _nBlocos, 'um cabecalho por bloco',
     _blocos.length + ' vs ' + _nBlocos);
  ok(_trs.length === Q.linhas.length + _nBlocos + 1,
     'uma linha por variavel (+ blocos + cabecalho)',
     _trs.length + ' vs ' + (Q.linhas.length + _nBlocos + 1));
  const _pintadas = _tab.querySelectorAll('td').filter(
    (td) => (td._attrs.style || '').indexOf('rgba(') >= 0);
  const _esperadas = Q.linhas.filter((l) => l.z != null && Math.abs(l.z) > 0.0001).length;
  ok(_pintadas.length === _esperadas, 'so as celulas com z != 0 saem pintadas',
     _pintadas.length + ' vs ' + _esperadas);
  ok(doc.getElementById('cd-kpis').querySelectorAll('.kpi-card').length === 4,
     'quatro KPI cards');

  // Agenda: so o que ainda vai sair, e ordenado.
  const _ag = Q.agenda || [];
  ok(_ag.every((a) => new Date(a.date + 'T00:00:00') <= new Date(Q.prox.date + 'T23:59:59')),
     'agenda nao passa da data da reuniao');
  ok(_ag.every((a) => a.date >= Q.hoje), 'agenda nao contem evento passado');
  ok(_ag.every((a, i) => i === 0 || _ag[i - 1].date <= a.date), 'agenda ordenada por data');
  ok(!_ag.some((a) => a.grupo === 'bcb_copom'), 'a propria reuniao nao entra na agenda');
  // A agenda e filtrada ao que alimenta a tabela (pedido explicito): todo evento tem de
  // apontar para pelo menos uma variavel, e o rotulo apontado tem de existir de fato --
  // um rotulo orfao aqui seria a agenda prometendo dado novo para uma linha inexistente.
  const _labels = new Set(Q.linhas.map((l) => l.label));
  ok(_ag.every((a) => (a.variaveis || []).length > 0),
     'todo evento da agenda alimenta alguma variavel da tabela');
  ok(_ag.every((a) => (a.variaveis || []).every((v) => _labels.has(v))),
     'os rotulos da agenda existem na tabela');
  // E o inverso: nenhum grupo do calendario fora dos que a tabela usa.
  const _grupos = new Set(Q.linhas.map((l) => l.grupo).filter(Boolean));
  ok(_ag.every((a) => _grupos.has(a.grupo) || (a.variaveis || []).length > 0),
     'agenda restrita aos grupos que alimentam a tabela',
     JSON.stringify([...new Set(_ag.map((a) => a.grupo))]));
  const _agTab = doc.getElementById('cd-agenda').querySelectorAll('tr');
  ok(_agTab.length === _ag.length + 1, 'tabela da agenda tem uma linha por evento',
     _agTab.length + ' vs ' + (_ag.length + 1));
  // cdAlimenta: 6 linhas da Focus numa celula so estouram a largura.
  ok(MP.cdAlimenta(['a', 'b']) === 'a · b', 'ate dois rotulos saem inteiros');
  ok(MP.cdAlimenta(['a', 'b', 'c', 'd']).indexOf('e mais 2') > 0,
     'acima de dois, conta o resto', MP.cdAlimenta(['a', 'b', 'c', 'd']));
  ok(MP.cdAlimenta([]).indexOf('—') >= 0, 'lista vazia nao inventa rotulo');
}


console.log('\n33. Aba Projecoes do Copom: projecao do HR x passo de Selic');
{
  const P = MP.D.projecoes || {};
  const E = (P.cenarios || {}).juros_esperado || [];
  const K = (P.cenarios || {}).juros_constante || [];
  ok(E.length > 90, 'cenario juros_esperado tem a serie longa', String(E.length));
  ok(K.length > 0, 'cenario juros_constante existe', String(K.length));

  // O ponto de partida da aba: a serie e HOMOGENEA. Sem isto o eixo mistura um "horizonte
  // relevante" que e o ano civil (distancia encurtando de 12 para 4 trimestres ao longo do
  // proprio ano) com um que e distancia fixa, e o dente de serra resultante nao e mudanca de
  // projecao nenhuma. Nao levanta excecao: so desenha errado.
  ok(E.every((r) => r.qa === 6), 'toda projecao esta a exatamente 6 trimestres da reuniao',
     JSON.stringify([...new Set(E.map((r) => r.qa))]));
  ok(K.every((r) => r.qa === 6), 'idem no cenario de juros constante');

  // Sem filtro de `documento` a mesma reuniao entra duas vezes, com numeros diferentes
  // (o relatorio e vintage 7-28 dias posterior). Duplicata aqui e o sintoma.
  ok(new Set(E.map((r) => r.nro)).size === E.length, 'uma linha por reuniao, sem duplicata');
  ok(E.every((r, i) => i === 0 || E[i - 1].nro < r.nro), 'ordenada por numero de reuniao');
  ok(E.every((r, i) => i === 0 || E[i - 1].decisao_date < r.decisao_date),
     'e a data da decisao cresce junto');

  // A DEFINICAO do passo: variacao decidida NESTA reuniao, nao acumulado do ciclo. Os dois
  // niveis viajam no payload justamente para esta conferencia ser possivel aqui.
  ok(E.every((r) => r.bps === Math.round((r.selic_dec - r.selic_ant) * 100)),
     'bps e (selic decidida - selic anterior), reuniao por reuniao');
  ok(E.every((r) => (r.bps > 0 ? r.decisao === 'elevacao'
                   : r.bps < 0 ? r.decisao === 'reducao' : r.decisao === 'manutencao')),
     'o rotulo da decisao segue o sinal do passo');
  // Um ciclo de alta com passos iguais provaria pouco; este cobre o caso que distingue as
  // duas leituras -- passos DIFERENTES em reunioes consecutivas.
  const _seq = E.filter((r) => r.nro >= 265 && r.nro <= 269).map((r) => r.bps);
  ok(_seq.length > 1 && _seq.every((b) => b > 0) && new Set(_seq).size > 1,
     'no ciclo de alta de 2024-2025 os passos variam entre reunioes (nao e acumulado)',
     JSON.stringify(_seq));

  ok(E.every((r) => r.meta != null && r.meta > 0), 'toda reuniao tem meta para o periodo projetado');
  ok(E.every((r) => (r.meta_estendida === 1) === (Number(r.periodo.slice(0, 4)) > P.ultimo_ano_meta)),
     'meta_estendida marca exatamente os periodos depois do ultimo ano publicado');
  ok(!(P.sem_decisao || []).length, 'nenhuma reuniao com projecao ficou sem decisao de Selic',
     JSON.stringify(P.sem_decisao));

  // Correlacao: contra calculo independente feito aqui.
  const _xs = E.map((r) => r.proj - r.meta), _ys = E.map((r) => r.bps);
  const _mx = _xs.reduce((a, b) => a + b, 0) / _xs.length;
  const _my = _ys.reduce((a, b) => a + b, 0) / _ys.length;
  let _cov = 0, _vx = 0, _vy = 0;
  for (let i = 0; i < _xs.length; i++) {
    _cov += (_xs[i] - _mx) * (_ys[i] - _my);
    _vx += (_xs[i] - _mx) ** 2; _vy += (_ys[i] - _my) ** 2;
  }
  const _ref = _cov / Math.sqrt(_vx * _vy);
  ok(Math.abs(MP.pjCorr(_xs, _ys) - _ref) < 1e-12, 'pjCorr bate com Pearson calculado a parte',
     MP.pjCorr(_xs, _ys) + ' vs ' + _ref);
  ok(MP.pjCorr([1, 2], [1, 2]) === null, 'pjCorr recusa menos de 3 pares');
  ok(MP.pjCorr([1, 1, 1], [1, 2, 3]) === null, 'pjCorr recusa variancia nula');

  // Render de verdade contra o payload real.
  let _erro = null;
  try { MP.RENDERERS.projecoes(); } catch (e) { _erro = e; }
  ok(!_erro, 'renderProjecoes executa', _erro && String(_erro));

  function ultimoReact(divId) {
    const c = chamadas.filter((x) => x.tipo === 'react' && x.divId === divId);
    return c.length ? c[c.length - 1] : null;
  }
  const _s = ultimoReact('chart-pj-serie');
  ok(!!_s, 'o grafico principal foi plotado');
  // 5 e nao 3: a previsao acrescenta a ponte tracejada e o ponto previsto.
  ok(_s && _s.traces.length === (P.previsao ? 5 : 3),
     'traces: barra do passo, meta, projecao e (com previsao) a ponte e o ponto previsto',
     _s && String(_s.traces.length));
  const _bar = _s && _s.traces.find((t) => t.type === 'bar');
  ok(!!_bar && _bar.yaxis === 'y2', 'na escala de Nivel o passo vai no eixo da direita');
  ok(!!_s && !!_s.layout.yaxis2, 'e o layout declara o segundo eixo');
  // barmode:'relative' com UMA barra so nao empilha nada -- e o que faz o _bindYAutofit dobrar
  // o zero dentro do range do eixo das barras. Sem isso, numa janela de ciclo de alta o autofit
  // devolveria [20, 105] e as barras sairiam desenhadas do fundo do eixo, como se +25 pb fosse
  // quase nada. E um erro puramente visual: nenhuma excecao, nenhum numero errado.
  ok(_s && _s.layout.barmode === 'relative',
     "barmode 'relative' presente, para o autofit de Y dobrar o zero no eixo do passo",
     _s && String(_s.layout.barmode));
  ok(_bar && _bar.y.length === E.length, 'uma barra por reuniao', _bar && String(_bar.y.length));

  // ── O ponto previsto no grafico principal ──
  // Ele e o unico numero da aba que ninguem publicou, e a asercao que importa e que ele NAO
  // se confunda com dado: trace separada, x na data da proxima reuniao, e some quando o
  // cenario ou a defasagem tiram o sentido dele.
  const PV = P.previsao;
  ok(!!PV, 'o payload traz a previsao da proxima reuniao');
  if (PV) {
    const _pt = _s.traces[4];
    ok(_pt.x.length === 1 && _pt.x[0] === PV.data_reuniao,
       'o ponto previsto esta na data da proxima reuniao, um ponto so',
       JSON.stringify(_pt.x));
    ok(Math.abs(_pt.y[0] - PV.previsto_focus) < 1e-12,
       'e o valor e o do metodo default (delta da Focus)', _pt.y[0] + ' vs ' + PV.previsto_focus);
    // O que distingue previsao de publicado e a COR e o tracejado, nao a forma: o losango
    // vazado que estava aqui antes lia como sujeira no grafico. Bolinha da mesma medida da
    // serie -- e a asercao le o tamanho da propria serie, para nao virar constante solta.
    ok(_pt.marker.symbol === 'circle' && _pt.marker.size === _s.traces[2].marker.size,
       'o ponto previsto e bolinha do mesmo tamanho dos marcadores da serie publicada',
       _pt.marker.symbol + '/' + _pt.marker.size + ' vs ' + _s.traces[2].marker.size);
    ok(_pt.marker.color === '#418791' && _pt.marker.color !== _s.traces[2].line.color,
       'e a cor e outra -- verde da marca, nunca o dourado da serie', _pt.marker.color);
    // A ponte tracejada nao pode virar dado: sem legenda e sem hover.
    ok(_s.traces[3].showlegend === false && _s.traces[3].hoverinfo === 'skip',
       'a ponte tracejada fica fora da legenda e do hover');
    ok(_s.traces[3].x.length === 2 &&
       _s.traces[3].x[0] === E[E.length - 1].decisao_date &&
       _s.traces[3].x[1] === PV.data_reuniao,
       'e ela liga exatamente o ultimo publicado ao previsto');
    ok(_s.traces[1].y.length === E.length + 1 &&
       _s.traces[1].y[E.length] === PV.meta,
       'a linha da meta se estende ao ponto previsto',
       _s.traces[1].y.length + ' vs ' + (E.length + 1));
    ok(PV.meta === 3.0 && PV.meta_estendida === 1,
       'e a meta dele vem do MESMO dicionario das linhas publicadas, com a extensao marcada',
       PV.meta + '/' + PV.meta_estendida);

    // Trocar de metodo troca o ponto. Os tres partem da mesma ancora, entao o que muda e o
    // delta -- e o ingenuo tem de dar a ancora crua.
    const _porMetodo = {};
    ['focus', 'modelo', 'ingenuo'].forEach((k) => {
      MP.PJ.metodo = k;
      MP.renderProjecoesSerie();
      _porMetodo[k] = ultimoReact('chart-pj-serie').traces[4].y[0];
    });
    ok(_porMetodo.ingenuo === PV.ancora, 'o metodo ingenuo poe o ponto na propria ancora',
       _porMetodo.ingenuo + ' vs ' + PV.ancora);
    ok(Math.abs(_porMetodo.modelo - (PV.ancora + PV.delta_modelo)) < 1e-9,
       'o modelo poe ancora + delta do modelo');
    ok(Math.abs(_porMetodo.focus - (PV.ancora + PV.delta_focus)) < 1e-9,
       'e a Focus poe ancora + delta da Focus');
    MP.PJ.metodo = 'focus';

    // Escala desvio: o ponto tem de ser medido contra a mesma regua que a serie publicada.
    MP.PJ.escala = 'desvio';
    MP.renderProjecoesSerie();
    ok(Math.abs(ultimoReact('chart-pj-serie').traces[4].y[0] -
                (PV.previsto_focus - PV.meta)) < 1e-12,
       'no modo Desvio o ponto previsto tambem vira previsto menos meta');
    MP.PJ.escala = 'nivel';
    MP.renderProjecoesSerie();

    // A caixa verde: sem ela o ponto no grafico e um numero sem procedencia.
    MP.renderProjecoesPrevBox();
    ok(doc._els['pj-prev-box'].style.display !== 'none', 'a caixa da previsao aparece');
    ok(doc._els['pj-prev-num'].textContent === '3,2%',
       'e mostra UMA casa decimal, que e como o BC publica',
       doc._els['pj-prev-num'].textContent);
    ok(doc._els['pj-prev-sub'].innerHTML.indexOf(PV.ancora_doc) >= 0 &&
       doc._els['pj-prev-sub'].innerHTML.indexOf('Corte de informa') >= 0,
       'e diz de qual documento veio a ancora e qual corte de informacao usou');
    // O corte e a data da GERACAO, nao a da reuniao: se o relatorio for gerado semanas antes,
    // falta IPCA e faltam boletins Focus, e quem le tem de ser avisado.
    ok(PV.corte_usado >= PV.data_reuniao ||
       doc._els['pj-prev-sub'].innerHTML.indexOf('anterior à reunião') >= 0,
       'com corte anterior a reuniao, a caixa avisa em vez de deixar passar');
  }

  // ── Backtest: o que estimamos contra o que o BC publicou ──
  const BT = P.backtest || [];
  ok(BT.length === 17, '17 reunioes no backtest -- a era em que o Copom declara o horizonte',
     String(BT.length));
  const _bt = ultimoReact('chart-pj-bt');
  ok(!!_bt, 'o grafico do backtest foi plotado');
  ok(_bt && _bt.traces.length === 4,
     'quatro traces: o publicado e os tres metodos', _bt && String(_bt.traces.length));
  ok(_bt && BT.every((r, i) => _bt.traces[0].y[i] === r.real),
     'a linha grossa e o numero que o BC publicou');
  // A proxima reuniao entra como ponto extra dos TRES metodos, e e o que o grafico existe para
  // mostrar. O publicado nao ganha o ponto: o null e o que faz a linha dourada parar antes da
  // vertical, e essa parada e o sinal de que ali nao ha contrapartida do BC.
  if (PV) {
    ok(_bt.traces[0].x.length === BT.length + 1 &&
       _bt.traces[0].x[BT.length] === PV.data_reuniao,
       'o eixo do backtest se estende a proxima reuniao', String(_bt.traces[0].x.length));
    ok(_bt.traces[0].y[BT.length] === null,
       'e o publicado fica null nela -- a linha dourada para antes');
    MP.PJ_METODOS.forEach((m, i) => {
      const _y = _bt.traces[i + 1].y;
      const _esp = m.key === 'modelo' ? PV.previsto
                 : (m.key === 'ingenuo' ? PV.ancora : PV.previsto_focus);
      ok(_y.length === BT.length + 1 && Math.abs(_y[BT.length] - _esp) < 1e-12,
         'e ' + m.label + ' aponta ' + _esp + ' para ela', String(_y[BT.length]));
    });
    // O ponto extra do backtest e o MESMO numero do ponto do grafico 1 e da caixa verde: tres
    // consumidores do mesmo valor, e dois divergirem daria dois numeros na mesma tela.
    ok(Math.abs(_bt.traces[1].y[BT.length] - _s.traces[4].y[0]) < 1e-12,
       'e ele bate com o ponto previsto do grafico principal');
    ok((_bt.layout.shapes || []).length === 1 &&
       _bt.layout.shapes[0].x0 === PV.data_reuniao,
       'uma vertical pontilhada separa o conferivel do nao conferivel');
  }
  // O metodo selecionado e o unico continuo -- a distincao visual e o ponto do grafico.
  const _solidos = _bt.traces.slice(1).filter((t) => t.line.dash === 'solid');
  ok(_solidos.length === 1, 'so o metodo selecionado vem continuo',
     String(_solidos.length));
  ok(_solidos[0].name === MP.pjMet('focus').label,
     'e ele e o que os pills dizem', _solidos[0].name);
  // Cada metodo parte da MESMA ancora: e a estrutura comum aos tres, e se ela se rompesse os
  // MAEs deixariam de ser comparaveis sem lancar excecao nenhuma.
  ok(BT.every((r) => Math.abs(MP.pjBtNivel(r, 'ingenuo') - r.ancora) < 1e-12),
     'o nivel do ingenuo e a propria ancora');
  ok(BT.every((r) => Math.abs(MP.pjBtNivel(r, 'modelo') - (r.ancora + r.delta_modelo)) < 1e-9),
     'o do modelo e ancora + delta do modelo');
  ok(BT.every((r) => r.delta_focus == null ||
       Math.abs(MP.pjBtNivel(r, 'focus') - (r.ancora + r.delta_focus)) < 1e-9),
     'e o da Focus e ancora + delta da Focus');
  // O erro de cada metodo tem de ser o nivel dele menos o publicado -- se o CSV trouxesse a
  // coluna de erro dessincronizada do delta, o grafico e a tabela discordariam em silencio.
  ok(BT.every((r) => Math.abs(r.erro_ingenuo - (r.ancora - r.real)) < 1e-9),
     'erro_ingenuo e ancora menos publicado');
  ok(BT.every((r) => Math.abs(r.erro - (r.previsto - r.real)) < 1e-9),
     'erro do modelo e previsto menos publicado');
  ok(BT.every((r) => r.erro_focus == null ||
       Math.abs(r.erro_focus - (r.ancora + r.delta_focus - r.real)) < 1e-9),
     'e erro_focus e ancora + delta menos publicado');
  ok(BT.every((r) => Math.abs(r.revisao - (r.real - r.ancora)) < 1e-9),
     'e a revisao, que os tres tentam prever, e publicado menos ancora');

  // MAE: contra media calculada aqui. E o numero que decide entre metodos, entao nao pode vir
  // de uma funcao que ignora null de um jeito e da tabela de outro.
  function _maeRef(campo) {
    const vs = BT.map((r) => r[campo]).filter((v) => v != null && !isNaN(v));
    return vs.reduce((a, b) => a + Math.abs(b), 0) / vs.length;
  }
  ['erro', 'erro_ingenuo', 'erro_focus'].forEach((campo) => {
    ok(Math.abs(MP.pjMAE(BT, campo) - _maeRef(campo)) < 1e-12,
       'pjMAE bate com a media calculada a parte em ' + campo);
  });
  ok(MP.pjMAE([], 'erro') === null, 'pjMAE devolve null sem linha nenhuma');
  ok(MP.pjMAE([{erro: null}], 'erro') === null, 'e null quando toda linha esta vazia');
  // O resultado que a aba existe para mostrar: a Focus ganha do ingenuo, e o modelo perde.
  ok(MP.pjMAE(BT, 'erro_focus') < MP.pjMAE(BT, 'erro_ingenuo'),
     'MAE da Focus < ingenuo (e o achado da aba)',
     MP.pjMAE(BT, 'erro_focus').toFixed(4) + ' vs ' + MP.pjMAE(BT, 'erro_ingenuo').toFixed(4));
  ok(MP.pjMAE(BT, 'erro') > MP.pjMAE(BT, 'erro_ingenuo'),
     'e MAE do modelo > ingenuo -- o resultado negativo tambem esta medido',
     MP.pjMAE(BT, 'erro').toFixed(4));

  // Revisao x expansao de horizonte: os dois casos existem e alternam.
  const _exp = BT.filter((r) => r.tipo === 'expansao');
  const _rev = BT.filter((r) => r.tipo === 'revisao');
  ok(_exp.length === 9 && _rev.length === 8, '9 expansoes e 8 revisoes',
     _exp.length + '/' + _rev.length);
  ok(BT.every((r, i) => i === 0 || r.tipo !== BT[i - 1].tipo),
     'e elas alternam sem excecao -- 2 reunioes por trimestre, 1 RPM por trimestre');
  ok(_exp.every((r) => r.anc_doc === 'relatorio'),
     'na expansao a ancora vem SEMPRE do relatorio, que publica o caminho contiguo');
  ok(_rev.every((r) => r.anc_doc === 'comunicado'),
     'e na revisao vem do comunicado anterior');

  // Eixo Erro: a trace 0 passa a ser a constante zero, nao o publicado.
  MP.PJ.btEixo = 'erro';
  MP.renderProjecoesBacktest();
  const _btE = ultimoReact('chart-pj-bt');
  ok(_btE.traces[0].y.every((v) => v === 0), 'no eixo Erro a referencia e a constante zero');
  // E o eixo Erro NAO se estende: nao ha numero publicado para subtrair na proxima reuniao,
  // entao um ponto ali seria erro contra nada.
  ok(_btE.traces[0].x.length === BT.length,
     'e ele nao se estende a proxima reuniao -- nao ha erro a plotar sem publicado',
     String(_btE.traces[0].x.length));
  ok(!(_btE.layout.shapes || []).length, 'nem a vertical da previsao aparece nele');
  ok(_btE.traces.slice(1).every((t, i) =>
       t.y.every((v, j) => v == null || Math.abs(v - BT[j][MP.PJ_METODOS[i].campo]) < 1e-12)),
     'e cada metodo plota a coluna de erro dele');
  MP.PJ.btEixo = 'nivel';
  MP.renderProjecoesBacktest();

  // O backtest E serie temporal em X (a data da reuniao), entao passa pelo _reactPreserveX --
  // ao contrario da dispersao que ele substituiu, cujos dois eixos nao eram tempo. O efeito
  // colateral que distingue os dois caminhos: _reactPreserveX liga DOIS listeners de
  // plotly_relayout (tracker de X + y-autofit), Plotly.react cru nao liga nenhum.
  ok((doc.getElementById('chart-pj-serie')._plotly['plotly_relayout'] || []).length === 2,
     'a serie principal ganha o tracker de X e o y-autofit',
     String((doc.getElementById('chart-pj-serie')._plotly['plotly_relayout'] || []).length));
  ok((doc.getElementById('chart-pj-bt')._plotly['plotly_relayout'] || []).length === 2,
     'e o backtest tambem, porque o X dele tambem e tempo',
     String((doc.getElementById('chart-pj-bt')._plotly['plotly_relayout'] || []).length));

  const _btTab = doc.getElementById('pj-bt-tabela');
  ok(_btTab.querySelectorAll('tr').length === BT.length + 2,
     'tabela do backtest: uma linha por reuniao + cabecalho + linha de MAE',
     _btTab.querySelectorAll('tr').length + ' vs ' + (BT.length + 2));
  ok(_btTab.innerHTML.indexOf('MAE') >= 0, 'e a linha de MAE esta la');
  // As duas tabelas viraram click-drop (<details>). Fechadas por default, entao o <summary> tem
  // de dizer o que ha dentro -- um "+" sozinho nao diz. O JS escreve a contagem la.
  ok(doc._els['pj-bt-sum'].textContent.indexOf(String(BT.length)) === 0,
     'o summary do backtest anuncia a contagem de reunioes',
     doc._els['pj-bt-sum'].textContent);
  ok(RAW.indexOf('<details class="tbl-fold"') >= 0 &&
     RAW.split('class="tbl-fold"').length - 1 === 2,
     'as duas tabelas da aba estao dentro de um details.tbl-fold',
     String(RAW.split('class="tbl-fold"').length - 1));

  const _tab = doc.getElementById('pj-tabela');
  ok(_tab.querySelectorAll('tr').length === E.length + 1,
     'tabela com uma linha por reuniao (+ cabecalho)',
     _tab.querySelectorAll('tr').length + ' vs ' + (E.length + 1));
  ok(doc._els['kpi-pj-proj-value'].textContent !== '—' &&
     doc._els['kpi-pj-passo-value'].textContent !== '—' &&
     doc._els['kpi-pj-corr-value'].textContent !== '—' &&
     doc._els['kpi-pj-n-value'].textContent !== '—', 'os quatro KPI cards preenchidos');
  ok(doc._els['kpi-pj-n-value'].textContent === String(E.length),
     'o card de cobertura conta as reunioes da serie',
     doc._els['kpi-pj-n-value'].textContent);
  ok(doc._els['pj-sum'].textContent.indexOf(String(E.length)) === 0,
     'e o summary da tabela grande tambem, com o cenario ao lado',
     doc._els['pj-sum'].textContent);

  // Escala: no modo desvio a linha de referencia e a constante zero; no modo nivel e a meta.
  MP.PJ.escala = 'nivel';
  MP.renderProjecoesSerie();
  const _ref1 = ultimoReact('chart-pj-serie').traces[1];
  // A linha da meta tem UM ponto a mais que a serie publicada quando ha previsao: ela se
  // estende ao ponto previsto, senao o unico ponto sem referencia seria justo esse.
  ok(E.every((r, i) => _ref1.y[i] === r.meta), 'no modo Nivel a referencia e a meta');
  ok(_ref1.y.length === E.length + (P.previsao ? 1 : 0),
     'e ela cobre a serie publicada mais o ponto previsto',
     _ref1.y.length + ' vs ' + (E.length + (P.previsao ? 1 : 0)));
  ok(ultimoReact('chart-pj-serie').traces[2].y.every((v, i) => v === E[i].proj),
     'e a linha dourada e a projecao');
  MP.PJ.escala = 'desvio';
  MP.renderProjecoesSerie();
  ok(ultimoReact('chart-pj-serie').traces[1].y.every((v) => v === 0),
     'no modo Desvio a referencia e a constante zero');
  ok(ultimoReact('chart-pj-serie').traces[2].y.every(
       (v, i) => Math.abs(v - (E[i].proj - E[i].meta)) < 1e-12),
     'e a linha dourada e projecao menos meta');
  // UM eixo so no modo Desvio, e a razao e unidade: desvio e passo estao ambos em pontos
  // percentuais, entao dividir regua e o que torna "o desvio era +1,0 e o Comite mexeu +1,0"
  // uma frase legivel do grafico. Duas coisas tem de acontecer juntas -- as barras mudarem de
  // eixo E o yaxis2 sair do layout: um eixo sobreposto sem trace nenhuma ainda desenha titulo
  // e ticks na direita, e o leitor le duas escalas onde ha uma.
  const _sd = ultimoReact('chart-pj-serie');
  const _barD = _sd.traces.find((tr) => tr.type === 'bar');
  ok(_barD.yaxis === 'y', 'no modo Desvio o passo vem para o eixo da esquerda', _barD.yaxis);
  ok(_sd.layout.yaxis2 === undefined,
     'e o segundo eixo sai do layout, senao sobrariam ticks de uma escala vazia');
  ok(_barD.y.every((v, i) => Math.abs(v - E[i].bps / 100) < 1e-12),
     'e o passo passa a pontos percentuais (100 pb = 1,00 p.p.), a mesma unidade do desvio');
  ok(_barD.hovertemplate.indexOf('p.p.') >= 0,
     'com o hover na unidade nova', _barD.hovertemplate);
  // O rotulo em cima da barra segue em pb, de proposito: passo de Selic se fala em pb.
  MP.PJ.dlSerie = true;
  MP.renderProjecoesSerie();
  const _txt = ultimoReact('chart-pj-serie').traces.find((tr) => tr.type === 'bar').text;
  ok(_txt.some((s) => s === '+50' || s === '+25' || s === '-50'),
     'mas o rotulo no grafico continua em pontos-base', JSON.stringify(_txt.slice(0, 4)));
  MP.PJ.dlSerie = false;
  // E barmode 'relative' tem de sobreviver: com desvio e passo no MESMO eixo, e ele que
  // garante que o zero fique no range -- e zero e a linha da meta.
  ok(_sd.layout.barmode === 'relative', "barmode 'relative' segue no modo Desvio");
  MP.PJ.escala = 'nivel';
  MP.renderProjecoesSerie();
  ok(ultimoReact('chart-pj-serie').traces.find((tr) => tr.type === 'bar').yaxis === 'y2' &&
     !!ultimoReact('chart-pj-serie').layout.yaxis2,
     'e voltar para Nivel devolve o eixo duplo -- o estado nao vaza entre as escalas');

  // Defasagem: o par passa a ser a projecao de hoje contra o passo da reuniao SEGUINTE, e a
  // ultima reuniao sai da amostra porque ainda nao existe passo seguinte.
  MP.PJ.defasagem = true;
  const _def = MP.pjLinhas();
  ok(_def.length === E.length - 1, 'a defasagem tira exatamente a ultima reuniao',
     _def.length + ' vs ' + (E.length - 1));
  // O ponto que isto fixa: a serie desenhada e trimestral (o relatorio sai 4x/ano) e salta 2-3
  // reunioes por ponto, entao "proxima reuniao" NAO e o proximo ponto do grafico. bps_prox vem
  // de pm_copom_reuniao, que tem as 247, e nro_prox prova de qual reuniao ele e.
  ok(_def.every((r) => r.nro_prox === r.nro + 1),
     'o passo defasado e o da reuniao imediatamente seguinte no calendario');
  const _saltos = _def.filter((r, i) => i + 1 < _def.length && _def[i + 1].nro !== r.nro + 1);
  ok(_saltos.length > 50,
     'e a serie de fato salta reunioes, senao a asercao acima seria vacua',
     String(_saltos.length));
  MP.renderProjecoesSerie();
  ok(ultimoReact('chart-pj-serie').traces[0].y.every((v, i) => v === _def[i].bps_prox),
     'e e ele que vai para as barras');
  // Com defasagem a previsao SAI do grafico, e essa e a decisao que a asercao fixa: a serie
  // desenhada para na penultima reuniao, entao o tracejado saltaria por cima de uma reuniao ja
  // publicada -- daria a entender que ela tambem e previsao.
  ok(ultimoReact('chart-pj-serie').traces.length === 3,
     'e com defasagem o ponto previsto sai do grafico',
     String(ultimoReact('chart-pj-serie').traces.length));
  MP.PJ.defasagem = false;

  // O stub de DOM CRIA elemento para qualquer id (getElementById nunca devolve null), entao um
  // id que o JS busca e o markup nao tem passaria por todos os testes acima e renderizaria uma
  // aba vazia no browser -- a classe de bug que este harness estruturalmente nao pega. Checagem
  // estatica: todo getElementById('pj-*'|'kpi-pj-*'|'chart-pj-*'|'dl-chart-pj-*') e todo
  // setupPillGroup/wireDlToggle desta aba tem de casar com um id="..." no HTML.
  const _idsJs = new Set();
  const _reId = /(?:getElementById|setupPillGroup|wireDlToggle)\(\s*'((?:pj-|kpi-pj-|chart-pj-|dl-chart-pj-)[\w-]+)'/g;
  let _m;
  while ((_m = _reId.exec(SRC))) _idsJs.add(_m[1]);
  // os prefixos de setKPI/pjKPI viram -value e -sub no DOM
  const _rePref = /pjKPI\(\s*'(kpi-pj-[\w-]+)'/g;
  while ((_m = _rePref.exec(SRC))) { _idsJs.add(_m[1] + '-value'); _idsJs.add(_m[1] + '-sub'); }
  ok(_idsJs.size >= 12, 'a checagem de ids achou os alvos da aba no script', String(_idsJs.size));
  const _faltando = [...(_idsJs)].filter((id) => RAW.indexOf('id="' + id + '"') < 0);
  ok(!_faltando.length, 'todo id que o JS da aba busca existe no markup', JSON.stringify(_faltando));

  // Trocar de cenario nao pode deixar estado do anterior atras.
  MP.PJ.cenario = 'juros_constante';
  MP.renderProjecoesSerie();
  ok(ultimoReact('chart-pj-serie').traces[0].y.length === K.length,
     'trocar para juros constante replota com a amostra dele',
     ultimoReact('chart-pj-serie').traces[0].y.length + ' vs ' + K.length);
  // A previsao e condicionada na curva de Selic da Focus, que E o condicionamento do cenario
  // de juros esperado. No de juros constante ela nao tem leitura, e desenha-la ali seria pior
  // que nao desenhar: o ponto pareceria comparavel a uma serie que ele nao continua.
  ok(MP.pjPrevisao() === null, 'e no cenario de juros constante a previsao nao existe');
  ok(ultimoReact('chart-pj-serie').traces.length === 3,
     'entao o grafico volta a tres traces', String(ultimoReact('chart-pj-serie').traces.length));
  MP.PJ.cenario = 'juros_esperado';
}

console.log('\n' + (falhas ? falhas + ' FALHA(S)' : 'todos os testes passaram'));
process.exit(falhas ? 1 : 0);
