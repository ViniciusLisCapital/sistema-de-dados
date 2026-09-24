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
// y-autofit, formatacao BR/truncada, toggle de labels -- e (b) as tres abas vivas: que cada
// renderizador executa contra o payload real, que as series que ele pede existem, que o
// Apendice escreve os coeficientes que vieram de D.info (e nao numero digitado no HTML), e
// que a eq. (5) chega nos artefatos como resposta (pi^e se move) e nao como premissa. O que
// ele NAO substitui e confirmacao visual num browser real.

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
// lida direto do artefato. Desde 2026-09-22, com a aba do motor tambem removida, e a UNICA
// forma de checar o modelo: as secoes 16 e 17 conferem a eq. (5) e o IRF contra os CSVs que
// `modelo_agregado.rodar()` grava, nao contra nada que o HTML carregue.
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
// setAttribute/getAttribute existem porque a pagina os usa (aria-label no botao de
// definicao). Um stub sem eles derruba o carregamento inteiro -- foi exatamente o modo
// de falha que .claude/rules/lis-dashboards.md registra no port de credito.
El.prototype.setAttribute = function (k, v) {
  this._attrs[k] = String(v);
  if (k === 'class') this.className = String(v);
  else if (k === 'id') this.id = String(v);
  else if (k.indexOf('data-') === 0) this.dataset[_camel(k.slice(5))] = String(v);
};
El.prototype.getAttribute = function (k) {
  return Object.prototype.hasOwnProperty.call(this._attrs, k) ? this._attrs[k] : null;
};
El.prototype.removeAttribute = function (k) { delete this._attrs[k]; };
// O card de definicao mede o botao para nao vazar da viewport. Zeros bastam: o que o teste
// cobra e que ele ABRA e leve o texto certo, nao onde ele cai na tela -- isso o browser
// confirma.
El.prototype.getBoundingClientRect = function () {
  return {left: 0, top: 0, right: 0, bottom: 0, width: 0, height: 0};
};
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
  const ABAS = ['condicoes', 'projecoes', 'appendix'];
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
  // `body` existe porque o card de definicao anexa UM no ao documento e o reposiciona a
  // cada abertura. Sem ele o render inteiro lanca na primeira linha com nota.
  doc.body = new El('body');
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
global.window = {innerWidth: 1280, innerHeight: 900};
global.Option = function (label, value) { const o = new El('option'); o.textContent = label; o.value = value; return o; };
global.Plotly = makePlotly(doc, chamadas);

// Reexporta as funcoes internas: new Function() cria escopo proprio, entao nada e visivel
// de fora sem esta linha.
const EXPORTS = ['fmtBR', 'fmtTrunc', 'fmtDate', 'lastValid', 'growthN', 'dlText', 'lineTrace',
                 '_quickRangeOptions', '_defaultXRange', '_traceAllDates', 'mkTimeseriesLayout',
                 'mkBarLayout', '_reactPreserveX', 'activateTab', 'RENDERERS', 'setKPI', '_PLOTLY_CONFIG',
                 'D', 'dashTrace',
                 'renderCondicoes', 'cdCor', 'cdDataCurta', 'cdDataBR', 'cdAlimenta',
                 'mxRenderTabela', 'mxDecisao', 'attachInfo', 'MX',
                 'renderProjecoes', 'renderProjecoesSerie', 'renderProjecoesBacktest',
                 'renderProjecoesLead',
                 'renderProjecoesBtTabela',
                 'pjLinhas', 'pjMAE', 'pjBtNivel', 'pjPrevisao', 'pjPrevValor',
                 'pjMet', 'PJ_METODOS', 'PJ'];
let MP;
try {
  new Function(SRC + ';global.__MP = {' + EXPORTS.join(',') + '};')();
  MP = global.__MP;
} catch (e) {
  console.error('o script do relatorio lancou excecao ao carregar: ' + e.stack);
  process.exit(1);
}

console.log('\n1. Carga e troca de abas');
ok(!!MP, 'script executa sem excecao');
ok(Object.keys(MP.RENDERERS).sort().join(',') === 'appendix,condicoes,projecoes',
   'RENDERERS tem as 3 abas, todas construidas', JSON.stringify(Object.keys(MP.RENDERERS)));
// A aba Projecoes deixou de ser stub em 2026-08-25 -- cobertura propria na secao 33.
ok('projecoes' in MP.RENDERERS, 'projecoes entra no RENDERERS');
// appendix TEM renderizador: preenche a tabela de validacao dos parametros a partir de D.info.
ok('appendix' in MP.RENDERERS, 'appendix entra no RENDERERS (monta a tabela de validacao)');
// A aba Modelo BC - Agregado saiu em 2026-09-22: o motor portado para JS foi junto, entao
// RENDERERS nao pode ter sobrado com uma chave que nenhum botao aciona.
ok(!('motor' in MP.RENDERERS), 'motor saiu do RENDERERS junto com a aba');
ok(doc._tabPanels[0].classList.contains('active'), 'aba inicial (condicoes) ativa no load');
MP.activateTab('projecoes');
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
// Um grupo nao declarado em PERIODS_PER_YEAR cai no default mensal -- e o caminho do caso
// abaixo. `motor` virou um deles em 2026-09-22, junto com a aba.
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

console.log('\n7b. Grafico com barra de controles propria: a regua cede o lugar');
// Quando o grafico tem controles que mudam O QUE ele desenha, eles ficam colados nele e a
// regua de periodo -- que so move a janela de tempo -- entra ACIMA deles. Sem isto a regua
// se insere entre o controle e o grafico, que e exatamente o afastamento que o pedido de
// 2026-09-23 corrigiu. O cenario de cima (sem barra propria) continua valendo e e o default.
{
  const chart2 = doc.getElementById('chart-teste2');
  const card2 = new El('div'); card2.classList.add('chart-card');
  const ctrl = new El('div'); ctrl.className = 'ctrl-bar chart-ctrl-bar';
  const pai2 = new El('div');
  pai2.appendChild(ctrl);
  pai2.appendChild(card2);
  card2.previousElementSibling = ctrl;   // o stub so mantem isso via insertBefore
  card2.appendChild(chart2);
  chart2._closest = card2;
  chamadas.length = 0;
  MP._reactPreserveX('chart-teste2', traces, layout);
  const iRegua = pai2.children.findIndex((c) => c.classList.contains('period-ctrl-bar'));
  const iCtrl = pai2.children.indexOf(ctrl);
  const iCard = pai2.children.indexOf(card2);
  ok(iRegua >= 0, 'a regua de periodo foi injetada tambem neste caso', String(iRegua));
  ok(iRegua < iCtrl && iCtrl < iCard,
     'e ela entra ACIMA da barra de controles, que fica colada no grafico',
     [iRegua, iCtrl, iCard].join(' < '));
  // Idempotencia: uma segunda pintura nao pode empilhar uma regua nova a cada render.
  MP._reactPreserveX('chart-teste2', traces, layout);
  ok(pai2.children.filter((c) => c.classList.contains('period-ctrl-bar')).length === 1,
     'e repintar reaproveita a mesma regua, em vez de empilhar outra',
     String(pai2.children.filter((c) => c.classList.contains('period-ctrl-bar')).length));
}

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
// Cenarios, Decomposicao, Taxa Neutra e Hiato do Produto foram REMOVIDAS em 2026-08-25, e
// Modelo BC - Agregado em 2026-09-22: sobraram estas tres.
['appendix', 'condicoes', 'projecoes'].forEach((tab) => {
  let erro = null;
  try { MP.RENDERERS[tab](); } catch (e) { erro = e; }
  ok(!erro, 'render' + tab[0].toUpperCase() + tab.slice(1) + ' executa', erro && String(erro));
});

console.log('\n13. Payload: o que as abas vivas pedem existe, e o das mortas nao sobrou');
const D = MP.D || {};
// Apagar a aba sem apagar o loader deixaria o payload carregando series que ninguem le.
// Num arquivo autocontido isso e peso morto invisivel -- so aparece no tamanho do .html.
// `motor` e `motor_cfg` entraram nesta lista em 2026-09-22: o segundo era o maior bloco do
// payload (parametros, condicoes iniciais e um caminho default por condicionante).
['cenarios', 'decomp', 'neutra', 'hiato', 'motor', 'motor_cfg'].forEach((g) => {
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
// com as abas Decomposicao e Cenarios; as 19 a 30, que cobriam o motor portado para JS,
// sairam em 2026-09-22 com a aba Modelo BC - Agregado. A numeracao das que ficaram NAO foi
// corrida de proposito: o CLAUDE.md da pasta cita as secoes 31, 32 e 33 pelo numero.

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

console.log('\n32. Aba Condicoes: a matriz reuniao a reuniao');
// A afirmacao que a aba inteira faz e uma so, e agora ela vale em NOVE colunas: a celula
// de uma reuniao so contem dado que ja tinha sido DIVULGADO quando aquele Copom decidiu.
// E verificavel do proprio payload, porque cada celula carrega a data de divulgacao que a
// justifica -- e por isso que ela esta la, e nao so para o tooltip.
{
  const Q = MP.D.condicoes || {};
  const COLS = Q.reunioes || [];
  const LINHAS = (Q.blocos || []).reduce((a, b) => a.concat(b.linhas || []), []);

  ok(COLS.length > 1, 'payload traz a janela de reunioes', String(COLS.length));
  ok(LINHAS.length > 0, 'payload traz as variaveis', String(LINHAS.length));
  ok(COLS.length === (Q.n_passadas || 8) + 1,
     'a janela e N passadas + 1 a frente', COLS.length + ' vs ' + ((Q.n_passadas || 8) + 1));

  // "05/08/2026 18:30" -> Date. Formato BR, montado no Python.
  function brDate(s) {
    if (!s) return null;
    const m = /^(\d{2})\/(\d{2})\/(\d{4})(?:\s+(\d{2}):(\d{2}))?$/.exec(String(s));
    if (!m) return null;
    return new Date(+m[3], +m[2] - 1, +m[1], m[4] ? +m[4] : 0, m[5] ? +m[5] : 0);
  }

  // ── A fronteira, coluna a coluna ──
  // Sem isto a matriz seria uma grade de calendario com cara de conjunto de informacao.
  let checadas = 0;
  const agora = new Date();
  LINHAS.forEach((l) => {
    (l.celulas || []).forEach((c, i) => {
      if (!c.div) return;
      const corte = brDate(COLS[i].corte);
      ok(brDate(c.div) <= corte,
         '"' + l.label + '" em ' + COLS[i].label + ': divulgado ' + c.div +
         ' <= corte ' + COLS[i].corte);
      checadas++;
    });
  });
  ok(checadas > 0, 'ha celulas indexadas por periodo de referencia para checar',
     String(checadas));

  // A coluna da PROXIMA reuniao e a unica cortada em AGORA e nao no fechamento dela --
  // afirmar o corte futuro seria ler dado que ainda nao existe.
  const fut = COLS.filter((r) => r.futura);
  ok(fut.length === 1, 'exatamente uma coluna futura, a ultima', String(fut.length));
  ok(COLS[COLS.length - 1].futura, 'e ela e a ultima da janela');
  ok(brDate(COLS[COLS.length - 1].corte) <= agora,
     'o corte da coluna futura e agora, nao a data da reuniao',
     COLS[COLS.length - 1].corte);
  LINHAS.forEach((l) => {
    const c = (l.celulas || [])[COLS.length - 1];
    if (c && c.div) ok(brDate(c.div) <= agora,
      '"' + l.label + '" na coluna futura: divulgado ' + c.div + ', ja no passado');
  });

  // Ordem e numeracao
  ok(COLS.every((r, i) => i === 0 || COLS[i - 1].date < r.date),
     'as reunioes vem em ordem crescente de data');
  const numeradas = COLS.filter((r) => r.numero != null);
  ok(numeradas.every((r, i) => i === 0 || numeradas[i - 1].numero < r.numero),
     'e a numeracao das que tem numero cresce junto');

  // ── `novo` e o que decide a cor, e ele tem de ser o que diz ──
  // Uma serie trimestral repete o ultimo numero entre divulgacoes. Colorir a repeticao
  // seria afirmar noticia onde houve silencio -- e o defeito nao levanta nada, porque o
  // numero repetido e plausivel.
  let repetidas = 0, novasSemZ = 0;
  LINHAS.forEach((l) => {
    const cs = l.celulas || [];
    cs.forEach((c, i) => {
      if (i === 0) return;               // a coluna 0 se compara com a reuniao que nao e exibida
      const ant = cs[i - 1];
      if (c.v == null || ant.v == null) return;
      // `ref_alvo` marca a linha cujo rotulo impresso e o periodo PROJETADO e nao o
      // que identifica a observacao -- la duas reunioes seguidas publicam numeros
      // diferentes para o mesmo trimestre, entao a equivalencia abaixo e falsa por
      // construcao. O bloco proprio dessa linha, mais abaixo, cobra o que vale nela.
      if (!l.ref_alvo) ok(c.novo === (c.ref !== ant.ref),
         '"' + l.label + '" em ' + COLS[i].label + ': `novo` bate com a troca de referencia',
         c.novo + ' / ' + ant.ref + ' -> ' + c.ref);
      if (!c.novo) {
        repetidas++;
        ok(c.z == null, '"' + l.label + '" repetida nao recebe z', String(c.z));
        ok(c.delta == null, 'e nem delta');
      } else if (c.z == null) {
        novasSemZ++;
      }
    });
  });
  ok(repetidas > 0, 'ha celulas repetidas na matriz (o caso trimestral existe)',
     String(repetidas));
  ok(novasSemZ === 0, 'toda celula com dado novo recebe z -- sem ele sairia branca e se '
     + 'confundiria com a repeticao', String(novasSemZ));

  // Pelo menos uma linha TRIMESTRAL, senao a asercao acima nao separa nada
  // Sem excluir `ref_alvo` a asercao passaria a ser satisfeita pela linha de projecao,
  // cujo rotulo tambem e um trimestre -- e a serie trimestral de verdade (o PIB, que e
  // o caso que a repeticao existe para tratar) poderia sumir sem ninguem notar.
  const tri = LINHAS.filter((l) => !l.ref_alvo
                                   && (l.celulas || []).some((c) => /^\dT\d{4}$/.test(c.ref)));
  ok(tri.length > 0, 'ha linha com referencia trimestral', String(tri.length));
  tri.forEach((l) => {
    ok((l.celulas || []).some((c) => !c.novo),
       '"' + l.label + '" (trimestral) repete em alguma reuniao');
  });

  // -- A projecao do proprio BC para o horizonte relevante --
  // Pedida acima do IPCA em 2026-09-22. Ela e a unica linha cujo indice E uma data de
  // publicacao (o comunicado sai no fechamento da reuniao), e e isso que a faz
  // verificavel pela mesma fronteira das demais: sem `div` a celula sai do laco la em
  // cima sem levantar nada, e a linha passaria a ser a unica sem guarda de
  // anacronismo.
  {
    const alvo = LINHAS.filter((l) => l.ref_alvo);
    ok(alvo.length === 1, 'uma unica linha com rotulo de periodo projetado',
       JSON.stringify(alvo.map((l) => l.key)));
    const bc = alvo[0];
    ok(bc.key === 'bc_hr', 'e ela e a projecao do BC', bc.key);
    const prim = ((Q.blocos || [])[0] || {}).linhas || [];
    ok(prim[0] && prim[0].key === 'bc_hr',
       'a projecao do BC e a primeira linha do primeiro bloco -- acima do IPCA 12m',
       (prim[0] || {}).key + ' / ' + (prim[1] || {}).key);
    ok(prim[1] && prim[1].key === 'ipca12', 'e o IPCA 12m vem logo depois',
       (prim[1] || {}).key);
    const cbc = bc.celulas || [];
    ok(cbc.length === COLS.length && cbc.every((c) => c.v != null),
       'a projecao tem valor em todas as colunas da janela',
       JSON.stringify(cbc.map((c) => c.v)));
    ok(cbc.every((c) => !!c.div),
       'toda celula dela carrega a data de publicacao -- sem isso a fronteira nao a le',
       String(cbc.filter((c) => !c.div).length));
    ok(cbc.every((c) => /^\dT\d{4}$/.test(c.ref)),
       'o rotulo embaixo do valor e o trimestre projetado, nao a data do comunicado',
       JSON.stringify(cbc.map((c) => c.ref)));
    // O horizonte relevante rola para frente com a reuniao; ele nunca anda para tras.
    const ord = cbc.map((c) => c.ref.slice(2) + c.ref.slice(0, 1));
    ok(ord.every((v, i) => i === 0 || ord[i - 1] <= v),
       'e ele nunca recua de uma reuniao para a seguinte', JSON.stringify(ord));
    // A ultima coluna e a proxima reuniao: o comunicado dela ainda nao existe, entao a
    // celula repete a anterior -- cinza, sem cor, que e a resposta honesta ate o BC
    // publicar.
    const ult = cbc[cbc.length - 1];
    ok(ult.novo === false, 'na coluna da proxima reuniao a projecao repete a ultima '
       + 'publicada', String(ult.novo));
    ok(ult.z == null && ult.delta == null, 'e por isso nao recebe cor');
    ok(ult.div === cbc[cbc.length - 2].div,
       'porque e literalmente o mesmo comunicado da coluna anterior',
       ult.div + ' vs ' + cbc[cbc.length - 2].div);
  }

  // z limitado, e sinal 0 nao existe mais nesta especificacao
  LINHAS.forEach((l) => {
    (l.celulas || []).forEach((c) => {
      if (c.z != null) ok(Math.abs(c.z) <= 3.0001,
        '"' + l.label + '" tem z limitado a +-3', String(c.z));
    });
  });

  // Nivel de preco entra em variacao PERCENTUAL: se o delta viesse em pontos, a celula
  // diria "+0,04" ao lado de uma PTAX de 5,15 e seria lida como quatro centavos -- e o z
  // estaria dividindo centavos por um sigma medido em log. Os dois tem de mudar juntos.
  const pct = LINHAS.filter((l) => l.pct);
  ok(pct.length > 0 && pct.some((l) => l.key === 'ptax'),
     'o cambio e uma das linhas em variacao percentual',
     JSON.stringify(pct.map((l) => l.key)));
  pct.forEach((l) => {
    const cs = l.celulas || [];
    cs.forEach((c, i) => {
      if (i === 0 || !c.novo || c.delta == null) return;
      const ant = cs[i - 1];
      if (ant.v == null || !ant.v) return;
      const esperado = (c.v / ant.v - 1) * 100;
      ok(Math.abs(c.delta - esperado) < 1e-6,
         '"' + l.label + '" em ' + COLS[i].label + ': delta em %, nao em pontos',
         c.delta + ' vs ' + esperado.toFixed(6));
    });
  });

  // cdCor: vermelho = hawkish, azul = dovish, nada = sem leitura.
  ok(MP.cdCor(2).indexOf('rgba(234,82,58') === 0, 'z positivo pinta de laranja/vermelho',
     MP.cdCor(2));
  ok(MP.cdCor(-2).indexOf('rgba(2,115,155') === 0, 'z negativo pinta de azul', MP.cdCor(-2));
  ok(MP.cdCor(null) === 'transparent', 'z nulo nao pinta');
  const _a3 = parseFloat(MP.cdCor(3).split(',')[3]);
  const _a1 = parseFloat(MP.cdCor(1).split(',')[3]);
  ok(_a3 > _a1, 'saturacao cresce com |z|', _a1 + ' -> ' + _a3);

  // ── Markup ──
  MP.RENDERERS.condicoes();
  const tab = doc.getElementById('mx-tabela');
  const heads = tab.querySelectorAll('thead tr');
  ok(heads.length === 2, 'duas linhas de cabecalho: reuniao e decisao', String(heads.length));
  ok(heads[0].children.length === COLS.length + 1,
     'uma coluna por reuniao, mais a do rotulo',
     heads[0].children.length + ' vs ' + (COLS.length + 1));
  const corpo = tab.querySelectorAll('tbody tr');
  const blocos = corpo.filter((t) => t.classList.contains('mx-bloco'));
  ok(blocos.length === (Q.blocos || []).length, 'um cabecalho por bloco',
     blocos.length + ' vs ' + (Q.blocos || []).length);
  ok(corpo.length === LINHAS.length + blocos.length,
     'uma linha por variavel, mais os cabecalhos de bloco',
     corpo.length + ' vs ' + (LINHAS.length + blocos.length));

  const cels = tab.querySelectorAll('td.mx-cel');
  ok(cels.length === LINHAS.length * COLS.length, 'uma celula por (variavel, reuniao)',
     cels.length + ' vs ' + (LINHAS.length * COLS.length));
  ok(tab.querySelectorAll('span.mx-ref').length === cels.length,
     'toda celula imprime o periodo de referencia embaixo do valor');

  const pintadas = cels.filter((td) => (td._attrs.style || '').indexOf('rgba(') >= 0);
  const esperadas = LINHAS.reduce((n, l) => n + (l.celulas || []).filter(
    (c) => c.novo && c.z != null && Math.abs(c.z) > 0.0001).length, 0);
  ok(pintadas.length === esperadas, 'so pinta celula com dado novo e z != 0',
     pintadas.length + ' vs ' + esperadas);

  // "Sem dado novo" e "dado novo que nao mudou nada" tem as duas fundo neutro, e o unico
  // jeito de distingui-las e a celula repetida NAO trazer style inline -- ela deixa a
  // lavagem cinza do CSS valer. Um `background:transparent` inline venceria o CSS e as
  // duas voltariam a ser indistinguiveis, sem erro nenhum.
  const repetidasDom = cels.filter((td) => td.classList.contains('mx-repete'));
  ok(repetidasDom.length === LINHAS.reduce(
       (n, l) => n + (l.celulas || []).filter((c) => !c.novo).length, 0),
     'uma celula .mx-repete por celula sem dado novo', String(repetidasDom.length));
  ok(repetidasDom.every((td) => !(td._attrs.style || '').length),
     'celula repetida nao leva style inline -- senao venceria a lavagem do CSS');

  // ── O seletor de decisao ──
  const pills = doc.getElementById('mx-pills').querySelectorAll('.pill');
  ok(pills.length === COLS.length, 'uma pill por reuniao', String(pills.length));
  ok(pills[pills.length - 1].classList.contains('active'),
     'o default e a proxima reuniao -- com ela nada fica esmaecido');
  // O passo de Selic saiu da pill em 2026-09-22 a pedido do usuario: ele ja esta na
  // linha "Decisao" do cabecalho, embaixo da propria coluna.
  ok(pills.every((b) => b.textContent.indexOf('bps') < 0),
     'a pill traz so o rotulo da reuniao, sem o passo de Selic',
     JSON.stringify(pills.map((b) => b.textContent)));
  ok(pills.every((b, i) => b.textContent === COLS[i].label),
     'e o rotulo dela e exatamente o da coluna');
  // A linha Decisao continua imprimindo o passo -- tirar da pill nao e tirar da tela.
  const _dec = tab.querySelectorAll('th.mx-dec');
  ok(_dec.length === COLS.length, 'uma celula de decisao por reuniao', String(_dec.length));
  const _comPasso = COLS.filter((r) => r.bps != null).length;
  ok(_comPasso > 0, 'ha reuniao com passo decidido na janela', String(_comPasso));
  ok((tab.innerHTML.match(/bps/g) || []).length === _comPasso,
     'e o passo continua impresso na linha Decisao, uma vez por reuniao decidida',
     (tab.innerHTML.match(/bps/g) || []).length + ' vs ' + _comPasso);
  ok(tab.querySelectorAll('.mx-depois').length === 0,
     'e no default nenhuma coluna esta esmaecida');

  // Clicar numa pill do meio: a moldura anda e SO as posteriores esmaecem.
  const alvo = Math.max(0, COLS.length - 4);
  pills[alvo].fire('click');
  const tab2 = doc.getElementById('mx-tabela');
  const depois = tab2.querySelectorAll('.mx-depois');
  const linhasTotais = 2 + LINHAS.length;          // 2 de cabecalho + uma por variavel
  ok(depois.length === (COLS.length - 1 - alvo) * linhasTotais,
     'esmaecidas = colunas posteriores x linhas',
     depois.length + ' vs ' + ((COLS.length - 1 - alvo) * linhasTotais));
  ok(tab2.querySelectorAll('.mx-sel').length === linhasTotais,
     'e a coluna escolhida esta emoldurada em toda a altura',
     String(tab2.querySelectorAll('.mx-sel').length));
  // As cores NAO mudam com a selecao: cada coluna mede a novidade contra a anterior a
  // ela, que e propriedade da coluna e nao do que se esta olhando.
  const pintadas2 = tab2.querySelectorAll('td.mx-cel').filter(
    (td) => (td._attrs.style || '').indexOf('rgba(') >= 0);
  ok(pintadas2.length === pintadas.length,
     'trocar a decisao em foco nao muda quais celulas tem cor',
     pintadas2.length + ' vs ' + pintadas.length);
  pills[pills.length - 1].fire('click');           // devolve ao default

  // ── Card de definicao ──
  const botoes = tab2.querySelectorAll('button.info-btn');
  const comNota = LINHAS.filter((l) => l.nota);
  ok(botoes.length === comNota.length, 'um botao de definicao por linha com nota',
     botoes.length + ' vs ' + comNota.length);
  ok(comNota.length === LINHAS.length, 'toda variavel tem nota escrita',
     comNota.length + ' vs ' + LINHAS.length);
  ok(LINHAS.every((l) => (l.nota || '').length >= 60),
     'e nenhuma nota e curta demais para explicar a linha',
     JSON.stringify(LINHAS.filter((l) => (l.nota || '').length < 60).map((l) => l.key)));
  // A nota e escrita para quem abre a pagina, nao para quem construiu a aba: vocabulario
  // de mecanismo aqui e o mesmo defeito que o calendario ja documentou.
  const PROIBIDO = ['_spec(', 'condicoes_copom', 'SPEC', 'sigma', 'payload', 'MySQL',
                    'ETL', 'grupo_cal', 'DataFrame'];
  LINHAS.forEach((l) => {
    PROIBIDO.forEach((t) => {
      ok((l.nota || '').indexOf(t) < 0,
         '"' + l.label + '" nao usa vocabulario de mecanismo ("' + t + '")');
    });
  });

  // ── Agenda ──
  const _ag = Q.agenda || [];
  const prox = COLS[COLS.length - 1];
  ok(_ag.every((a) => new Date(a.date + 'T00:00:00') <= new Date(prox.date + 'T23:59:59')),
     'agenda nao passa da data da proxima reuniao');
  ok(_ag.every((a) => a.date >= Q.hoje), 'agenda nao contem evento passado');
  ok(_ag.every((a, i) => i === 0 || _ag[i - 1].date <= a.date), 'agenda ordenada por data');
  ok(!_ag.some((a) => a.grupo === 'bcb_copom'), 'a propria reuniao nao entra na agenda');
  // A agenda so existe se a coluna futura guardar o corte REAL da reuniao: cortada em
  // agora, a janela [hoje, corte] tem ~zero dia e a agenda sai vazia sem erro nenhum.
  ok(_ag.length > 0, 'a agenda nao saiu vazia -- a coluna futura guarda o corte da reuniao',
     String(_ag.length));
  const _labels = new Set(LINHAS.map((l) => l.label));
  ok(_ag.every((a) => (a.variaveis || []).length > 0),
     'todo evento da agenda alimenta alguma variavel da tabela');
  ok(_ag.every((a) => (a.variaveis || []).every((v) => _labels.has(v))),
     'os rotulos da agenda existem na tabela');
  const _agTab = doc.getElementById('cd-agenda').querySelectorAll('tr');
  ok(_agTab.length === _ag.length + 1, 'tabela da agenda tem uma linha por evento',
     _agTab.length + ' vs ' + (_ag.length + 1));
  // cdAlimenta: 6 linhas da Focus numa celula so estouram a largura.
  ok(MP.cdAlimenta(['a', 'b']) === 'a · b', 'ate dois rotulos saem inteiros');
  ok(MP.cdAlimenta(['a', 'b', 'c', 'd']).indexOf('e mais 2') > 0,
     'acima de dois, conta o resto', MP.cdAlimenta(['a', 'b', 'c', 'd']));
  ok(MP.cdAlimenta([]).indexOf('—') >= 0, 'lista vazia nao inventa rotulo');

  // ── O que saiu da aba ──
  // KPI cards e a regua de saldo foram removidos a pedido do usuario em 2026-09-22. Um
  // resto de markup deles aqui nao quebraria nada -- so ficaria orfao, sem renderizador.
  ok(!RAW.match(/id="cd-kpis"/), 'o bloco de KPI saiu do markup');
  ok(!RAW.match(/id="cd-regua-barra"/), 'a regua hawkish/dovish tambem');
}


console.log('\n33. Aba Projecoes do Copom: projecao do HR x passo de Selic');
{
  const P = MP.D.projecoes || {};
  const E = (P.cenarios || {}).juros_esperado || [];
  ok(E.length > 90, 'cenario juros_esperado tem a serie longa', String(E.length));
  // O seletor de cenario saiu em 2026-09-23 e o payload deixou de carregar o outro. A
  // asserção e sobre o PAYLOAD e nao sobre a tela porque o custo de voltar a carrega-lo e
  // invisivel: 79 linhas que ninguem le, numa aba que ja tem 107 na que se le.
  ok(Object.keys(P.cenarios || {}).length === 1,
     'e e o unico cenario no payload -- juros constante saiu junto com o seletor',
     JSON.stringify(Object.keys(P.cenarios || {})));

  // O ponto de partida da aba: a serie e HOMOGENEA. Sem isto o eixo mistura um "horizonte
  // relevante" que e o ano civil (distancia encurtando de 12 para 4 trimestres ao longo do
  // proprio ano) com um que e distancia fixa, e o dente de serra resultante nao e mudanca de
  // projecao nenhuma. Nao levanta excecao: so desenha errado.
  ok(E.every((r) => r.qa === 6), 'toda projecao esta a exatamente 6 trimestres da reuniao',
     JSON.stringify([...new Set(E.map((r) => r.qa))]));

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

  // Render de verdade contra o payload real.
  let _erro = null;
  try { MP.RENDERERS.projecoes(); } catch (e) { _erro = e; }
  ok(!_erro, 'renderProjecoes executa', _erro && String(_erro));

  // Os 4 KPI cards sairam em 2026-09-23 a pedido do usuario. O guarda tem de ser sobre o
  // MARKUP da aba, nao sobre o stub: `doc._els[...]` cria elemento para qualquer id, entao
  // uma assercao de "o cartao sumiu" via getElementById passaria com ele de volta na tela.
  // Tres dos quatro repetiam numero que a legenda ou a tabela ja traz -- e sao esses que o
  // teste exige que continuem ditos em algum lugar, senao remover o cartao vira perda de dado.
  const _pjRaw = RAW.slice(RAW.indexOf('id="tab-projecoes"'), RAW.indexOf('id="tab-appendix"'));
  ok(_pjRaw.length > 2000, 'a fatia da aba Projecoes foi extraida', String(_pjRaw.length));
  ok(_pjRaw.indexOf('kpi-card') < 0 && _pjRaw.indexOf('kpi-grid') < 0,
     'a aba Projecoes nao tem mais grid de KPI');
  ok(!/kpi-pj-|pjKPI\(|renderProjecoesKPIs|pjCorr/.test(SRC),
     'e o JS que os alimentava saiu junto, sem funcao orfa');
  // A caixa verde da previsao saiu na mesma rodada. O que NAO saiu e a previsao: o
  // ponto verde continua no grafico, entao o guarda cobra as duas metades -- a caixa
  // fora do markup, e o corte de informacao, que so existia dentro dela, dito agora na
  // legenda. Sem a segunda metade, remover a caixa apaga a procedencia do ponto.
  ok(_pjRaw.indexOf('pj-prev') < 0, 'a caixa verde da previsao saiu do markup');
  ok(!/renderProjecoesPrevBox|renderProjecoesFrescor|_pjDia|\.pj-prev/.test(RAW),
     'e o JS e o CSS dela saíram junto');

  // ── Os dois seletores que sairam, e a posicao do que ficou ──
  // Cenario e defasagem sairam em 2026-09-23. O guarda e sobre o markup da aba porque o
  // stub inventa elemento para qualquer id: um `setupPillGroup('pj-cenario', ...)` de volta
  // no JS passaria por qualquer asserção feita via getElementById.
  ok(_pjRaw.indexOf('pj-cenario') < 0 && _pjRaw.indexOf('pj-defasagem') < 0,
     'os seletores de cenario e de defasagem sairam do markup');
  ok(!/PJ\.cenario|PJ\.defasagem|PJ_CENARIOS|bps_prox/.test(SRC),
     'e o estado e as leituras que dependiam deles sairam do JS');

  // O seletor de Projecao comanda ESTE grafico, entao ele fica encostado nele: a barra que
  // o contem tem de ser o ultimo elemento antes do card do grafico. A asserção e sobre a
  // ORDEM no markup, nao sobre CSS -- e a mesma escolha da regra de rodape da casa.
  const _iEscala = _pjRaw.indexOf('id="pj-escala"');
  const _iToggle = _pjRaw.indexOf('id="dl-chart-pj-serie"');
  const _iCard = _pjRaw.indexOf('<div class="chart-card"><div id="chart-pj-serie">');
  const _iMetodo = _pjRaw.indexOf('id="pj-metodo"');
  ok(_iEscala > 0 && _iToggle > 0 && _iCard > 0 && _iMetodo > 0,
     'os quatro alvos do layout existem no markup da aba',
     [_iEscala, _iToggle, _iCard, _iMetodo].join(','));
  ok(_iEscala < _iCard && _iToggle < _iCard,
     'Projecao e o toggle de dados ficam ACIMA do grafico');
  // E nada de outra barra entre eles: o trecho entre o seletor e o card nao pode abrir um
  // <div class="ctrl-bar"> novo, senao o controle deixou de estar encostado no grafico.
  ok(_pjRaw.slice(_iEscala, _iCard).indexOf('class="ctrl-bar') < 0,
     'e nenhuma barra de controle se mete entre o seletor de Projecao e o grafico',
     _pjRaw.slice(_iEscala, _iCard).replace(/\s+/g, ' ').slice(0, 120));
  // A Previsao governa DOIS graficos, entao ela e a excecao que fica no alto da aba.
  ok(_iMetodo < _iEscala,
     'a Previsao, que governa os dois graficos da aba, fica acima da Projecao');
  // A regua de periodo e criada em runtime e se insere ACIMA da barra do grafico. O browser
  // confirma a posicao; aqui ficam os dois elos que a garantem no codigo.
  ok(SRC.indexOf('ancora.parentNode.insertBefore(bar, ancora)') >= 0,
     'e a regua de periodo cede o lugar, ancorando na barra em vez do card');
  // O segundo elo, e o que a ordem estatica NAO pega: a barra que contem o seletor tem de
  // ser a que carrega `chart-ctrl-bar`. Sem a classe o markup fica identico e a regua volta
  // a se inserir entre o controle e o grafico -- nada na ordem denuncia.
  const _abre = _pjRaw.lastIndexOf('<div class="ctrl-bar', _iEscala);
  const _tag = _pjRaw.slice(_abre, _pjRaw.indexOf('>', _abre) + 1);
  ok(_abre >= 0 && _tag.indexOf('chart-ctrl-bar') >= 0,
     'e a barra que contem o seletor de Projecao e a que a regua reconhece', _tag);
  if (P.previsao) {
    const _capPv = doc._els['pj-cap-serie'].textContent;
    // O ponto so e desenhado quando o metodo default tem valor (`yPrev == null` zera o
    // `pv` da serie), entao a legenda tem DUAS obrigacoes e o teste cobra as duas: com
    // ponto, dizer de que reuniao ele e e com que corte; sem ponto, nao prometer um.
    if (P.previsao.previsto_focus != null) {
      ok(_capPv.indexOf(String(P.previsao.nro)) >= 0 &&
         _capPv.indexOf(P.previsao.corte_usado.split('-').reverse().join('/')) >= 0,
         'e a legenda nomeia a reuniao prevista e o corte de informacao dela',
         _capPv.slice(-130));
    } else {
      ok(_capPv.indexOf('Ponto verde') < 0,
         'sem valor no metodo default nao ha ponto, e a legenda nao promete um',
         _capPv.slice(-130));
    }
    // A CHAMADA tem de dizer a mesma coisa que o grafico faz. Ela testava
    // `P.previsao` -- existe previsao no payload? -- e o grafico testa se o metodo
    // selecionado tem valor; hoje as duas divergem, e a frase anunciava um ponto verde
    // que nao estava la. Nada na tela contradizia.
    // Duas defesas, e as duas sao necessarias. `getElementById` em vez de
    // `doc._els[id]`, porque o stub so registra o id que ALGUEM pediu: um mutante que nunca
    // chama a funcao deixa a chave inexistente e a leitura estoura. E `String(x || '')` para
    // o elemento que existe e nunca foi escrito. Sem as duas o mutante derruba o harness em
    // vez de reprovar a regra que ele quebrou -- crash tambem e deteccao, mas nao diz qual
    // regra caiu.
    const _lead = () => String((doc.getElementById('pj-lead') || {}).innerHTML || '');
    const _promete = (t) => t.indexOf('ponto verde ligado por') >= 0;
    const _temPontoAgora = MP.pjPrevValor(P.previsao) != null;
    ok(_promete(_lead()) === _temPontoAgora,
       'a chamada so promete o ponto previsto quando ele e desenhado',
       'promete=' + _promete(_lead()) + ' desenha=' + _temPontoAgora);
    ok(_temPontoAgora || _lead().indexOf('sem ponto previsto</b>') >= 0,
       'e quando nao ha, ela DIZ que nao ha e aponta o seletor', _lead().slice(-200));
    // E ela e reescrita no clique, nao so na primeira pintura: o metodo e um pill, entao
    // a resposta muda sem recarregar a pagina. Escrever `PJ.metodo` e chamar a funcao a
    // mao passaria num mutante que tira a chamada do redraw -- tem de ser o clique.
    const _pillsMet = doc._els['pj-metodo'];
    let _iModelo = -1;
    for (let i = 0; i < _pillsMet.children.length; i++) {
      if (_pillsMet.children[i].textContent.indexOf('Modelo') >= 0) _iModelo = i;
    }
    ok(_iModelo >= 0, 'o pill de Modelo existe', String(_iModelo));
    _pillsMet.children[_iModelo].fire('click');
    ok(_promete(_lead()) === (MP.pjPrevValor(P.previsao, 'modelo') != null),
       'clicar noutro metodo reescreve a chamada junto com o grafico',
       'promete=' + _promete(_lead()));
    let _iFocus = -1;
    for (let i = 0; i < _pillsMet.children.length; i++) {
      if (_pillsMet.children[i].textContent.indexOf('Focus') >= 0) _iFocus = i;
    }
    _pillsMet.children[_iFocus].fire('click');

    // ── A legenda com ponto, exercitada SINTETICAMENTE ──
    // O corte de informacao so aparece na legenda quando ha ponto desenhado, e no payload
    // de hoje nao ha (`previsto_focus` nulo, porque a Focus ainda nao abriu o trimestre
    // alvo). Sem forcar o estado, a asserção que cobra a procedencia do ponto nunca roda --
    // e o corte foi justamente o que sobrou da caixa verde removida. Mesmo instinto do
    // teste da faixa laranja: o estado que o leitor precisa ver nao e o do arquivo recem
    // gerado.
    const _pvOrig = P.previsao.previsto_focus;
    P.previsao.previsto_focus = 3.3;
    MP.renderProjecoesSerie();
    const _capCom = doc._els['pj-cap-serie'].textContent;
    ok(_capCom.indexOf('Ponto verde') >= 0, 'com valor, a legenda nomeia o ponto previsto',
       _capCom.slice(-150));
    ok(_capCom.indexOf(String(P.previsao.nro)) >= 0,
       'e diz de que reuniao ele e', _capCom.slice(-150));
    ok(_capCom.indexOf(P.previsao.corte_usado.split('-').reverse().join('/')) >= 0,
       'e com que corte de informacao foi calculado -- a procedencia que vivia na caixa',
       _capCom.slice(-150));
    MP.renderProjecoesLead();
    ok(_lead().indexOf('ponto verde ligado por') >= 0,
       'e a chamada volta a prometer o ponto quando ele passa a existir',
       _lead().slice(-160));
    P.previsao.previsto_focus = _pvOrig;
    MP.renderProjecoesSerie();
    MP.renderProjecoesLead();
  }
  ok(doc._els['pj-cap-serie'].textContent.indexOf(String(E.length) + ' reuniões') >= 0,
     'a contagem de reunioes continua dita na legenda do grafico',
     doc._els['pj-cap-serie'].textContent.slice(-140));

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

  // O passo plotado e sempre o da PROPRIA reuniao desde 2026-09-23. A serie salta 2-3
  // reunioes por ponto (o relatorio sai 4x/ano), entao a alternativa que existia aqui --
  // emparelhar com o passo da reuniao seguinte -- nunca foi "o proximo ponto do grafico";
  // era o passo da reuniao n+1 do calendario, que na maioria dos pontos nem esta desenhada.
  MP.renderProjecoesSerie();
  ok(ultimoReact('chart-pj-serie').traces[0].y.every((v, i) => v === E[i].bps),
     'as barras sao o passo da propria reuniao, uma por ponto da serie');
  ok(E.every((r) => r.bps_prox === undefined),
     'e o payload nao carrega mais o passo da reuniao seguinte');

  // O stub de DOM CRIA elemento para qualquer id (getElementById nunca devolve null), entao um
  // id que o JS busca e o markup nao tem passaria por todos os testes acima e renderizaria uma
  // aba vazia no browser -- a classe de bug que este harness estruturalmente nao pega. Checagem
  // estatica: todo getElementById('pj-*'|'kpi-pj-*'|'chart-pj-*'|'dl-chart-pj-*') e todo
  // setupPillGroup/wireDlToggle desta aba tem de casar com um id="..." no HTML.
  const _idsJs = new Set();
  const _reId = /(?:getElementById|setupPillGroup|wireDlToggle)\(\s*'((?:pj-|kpi-pj-|chart-pj-|dl-chart-pj-)[\w-]+)'/g;
  let _m;
  while ((_m = _reId.exec(SRC))) _idsJs.add(_m[1]);
  ok(_idsJs.size >= 12, 'a checagem de ids achou os alvos da aba no script', String(_idsJs.size));
  const _faltando = [...(_idsJs)].filter((id) => RAW.indexOf('id="' + id + '"') < 0);
  ok(!_faltando.length, 'todo id que o JS da aba busca existe no markup', JSON.stringify(_faltando));

}

console.log('\n' + (falhas ? falhas + ' FALHA(S)' : 'todos os testes passaram'));
process.exit(falhas ? 1 : 0);
