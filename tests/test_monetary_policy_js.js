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
// renderizador executa contra o payload real e que as series que ele pede existem. O modelo
// agregado nao e mais coberto aqui desde que o Apendice saiu (2026-09-24): nada deste
// relatorio o le, e o que sobra dele e testado em tests/test_eq5_expectativas.py. O que
// este harness NAO substitui e confirmacao visual num browser real.

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
  const ABAS = ['condicoes', 'projecoes', 'condicionais', 'expectativas'];
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
                 'renderProjecoesApendice',
                 'pjLinhas', 'pjMAE', 'pjBtNivel', 'pjPrevisao', 'pjPrevValor',
                 'pjPrevBruto', 'pjAssoc', 'PJ',
                 'renderPjCaminhos', 'renderPjCaminhosTextos', 'renderPjCaminhosTabela',
                 'renderPjVertice', 'renderPjVerticeTextos', 'pjVtSetupTri', 'pjCmSetupEd', 'PJ_CTE_COR', 'PJ_SEL_CORES',
                 'renderCondicionais', 'renderCnHiato', 'cnEdicoes', 'cnTempoReal', 'cnCor',
                 'cnDistTri', 'cnRevisoes', 'CN', '_chartXRange', '_PERIOD_LABEL',
                 '_ensurePeriodSelector', 'renderCnTextos', 'renderCnSelic',
                 'renderCnSelicTextos',
                 'renderExpectativas', 'renderEjHoje', 'renderEjHojeTextos', 'renderEjReuniao',
                 'renderEjReuniaoTextos', 'renderEjHz', 'renderEjHzTextos', 'EJ',
                 'ejSemanaAtras', 'ejSegunda', 'ejGap'];
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
// A terceira aba, Acompanhamento Condicionais, entrou em 2026-09-24 (secao 34), e a quarta,
// Expectativas de Juros, no mesmo dia (secao 36).
ok(Object.keys(MP.RENDERERS).sort().join(',') === 'condicionais,condicoes,expectativas,projecoes',
   'RENDERERS tem as 4 abas, todas construidas', JSON.stringify(Object.keys(MP.RENDERERS)));
// A aba Projecoes deixou de ser stub em 2026-08-25 -- cobertura propria na secao 33.
ok('projecoes' in MP.RENDERERS, 'projecoes entra no RENDERERS');
// O Apendice (a descricao do modelo agregado) saiu em 2026-09-24, a pedido do usuario: era o
// unico lugar do relatorio que ainda lia o modelo. Nem renderizador nem botao podem sobrar.
ok(!('appendix' in MP.RENDERERS), 'appendix saiu do RENDERERS junto com a aba');
ok(RAW.indexOf('data-tab="appendix"') < 0 && RAW.indexOf('id="tab-appendix"') < 0,
   'e o botao e o painel da aba sairam do HTML');
// A aba Modelo BC - Agregado saiu em 2026-09-22: o motor portado para JS foi junto, entao
// RENDERERS nao pode ter sobrado com uma chave que nenhum botao aciona.
ok(!('motor' in MP.RENDERERS), 'motor saiu do RENDERERS junto com a aba');
ok(doc._tabPanels[0].classList.contains('active'), 'aba inicial (condicoes) ativa no load');
// O rotulo da primeira aba e "Acompanhamento Copom" desde 2026-09-24, a pedido do usuario; o
// identificador interno continua `condicoes`. "FOMC" chegou a ser pedido e foi corrigido na
// hora: as colunas sao reunioes do Copom, e o nome do comite do Fed ali seria erro de fato.
ok(RAW.indexOf('data-tab="condicoes">Acompanhamento Copom</button>') >= 0,
   'a primeira aba se chama Acompanhamento Copom');
ok(!/>Condições<\/button>|FOMC<\/button>/.test(RAW), 'e nenhum botao ficou com o nome antigo');
// Nome provisorio, pedido em 2026-09-24 ("Por hora, coloque o nome de ...").
ok(RAW.indexOf('data-tab="condicionais">Acompanhamento Condicionais</button>') >= 0,
   'a terceira aba se chama Acompanhamento Condicionais');
ok(RAW.indexOf('data-tab="expectativas">Expectativas de Juros</button>') >= 0,
   'a quarta aba se chama Expectativas de Juros');
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
// ausente no payload e trace malformado -- o tipo de erro que `node --check` nao ve.
// Cenarios, Decomposicao, Taxa Neutra e Hiato do Produto foram REMOVIDAS em 2026-08-25, e
// Modelo BC - Agregado em 2026-09-22 e o Apendice em 2026-09-24: sobraram estas duas.
['condicoes', 'projecoes', 'condicionais', 'expectativas'].forEach((tab) => {
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
// `info` (parametros, validacao e IRF do modelo, que o Apendice lia) entrou em 2026-09-24.
['cenarios', 'decomp', 'neutra', 'hiato', 'motor', 'motor_cfg', 'info'].forEach((g) => {
  ok(!D[g], 'grupo ' + g + ' saiu do payload junto com a aba');
});
// As secoes 14 (identidade das decomposicoes) e 15 (_emenda/_recorta) sairam em 2026-08-25
// com as abas Decomposicao e Cenarios; as 19 a 30, que cobriam o motor portado para JS,
// sairam em 2026-09-22 com a aba Modelo BC - Agregado; a 16 (eq. 5), a 17 (IRF) e a 31
// (descricao do modelo) sairam em 2026-09-24 com o Apendice. A numeracao das que ficaram NAO
// foi corrida de proposito: o CLAUDE.md da pasta cita as secoes 32 e 33 pelo numero.

console.log('\n18. dashTrace: a linha publicada e tracejada e sem marcador');
const _dt = MP.dashTrace({dates: ['2026-01-01'], values: [1]}, 'x', '#000', false, 2, '%');
ok(_dt.line.dash === 'dash', 'dashTrace marca a linha como tracejada');
ok(_dt.mode === 'lines' && _dt.marker.size === 0, 'dashTrace nao desenha marcador');

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
  // "Ha previsao no payload" e "ha ponto desenhado" sao coisas diferentes, e e a segunda que
  // governa o grafico: o delta da Focus fica indefinido enquanto a pesquisa nao tiver o
  // trimestre-alvo numa das duas datas que ele compara -- estado de hoje, e legitimo.
  const _pontoPv = !!(P.previsao && P.previsao.previsto_focus != null);
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
  const _pjRaw = RAW.slice(RAW.indexOf('id="tab-projecoes"'), RAW.indexOf('</main>'));
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
  ok(_iEscala > 0 && _iToggle > 0 && _iCard > 0,
     'os tres alvos do layout existem no markup da aba',
     [_iEscala, _iToggle, _iCard].join(','));
  ok(_iEscala < _iCard && _iToggle < _iCard,
     'Projecao e o toggle de dados ficam ACIMA do grafico');
  // E nada de outra barra entre eles: o trecho entre o seletor e o card nao pode abrir um
  // <div class="ctrl-bar"> novo, senao o controle deixou de estar encostado no grafico.
  ok(_pjRaw.slice(_iEscala, _iCard).indexOf('class="ctrl-bar') < 0,
     'e nenhuma barra de controle se mete entre o seletor de Projecao e o grafico',
     _pjRaw.slice(_iEscala, _iCard).replace(/\s+/g, ' ').slice(0, 120));
  // O seletor de PREVISAO saiu em 2026-09-24: com um metodo so ele escolhia entre uma opcao.
  // Guarda sobre o MARKUP e sobre o JS, porque o stub inventa elemento para qualquer id --
  // um setupPillGroup('pj-metodo', ...) de volta passaria por getElementById sem reprovar.
  ok(_pjRaw.indexOf('pj-metodo') < 0, 'o seletor de previsao saiu do markup');
  ok(!/PJ_METODOS|PJ\.metodo|pjMet\(/.test(SRC),
     'e a lista de metodos, o estado e o leitor dela sairam do JS');
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
    // Sem o pill de metodo, o que segura `renderProjecoesLead` dentro do redraw e a chamada
    // ter conteudo depois de `RENDERERS.projecoes()`: tirada de la, o paragrafo fica com o
    // travessao do markup. `String(... || '')` porque o stub so registra o id que alguem pediu.
    ok(_lead().length > 120 && _lead().indexOf('Copom') >= 0,
       'a chamada e escrita pelo redraw, nao ficou no travessao do markup',
       _lead().slice(0, 80));

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
  ok(_s && _s.traces.length === (_pontoPv ? 5 : 3),
     'traces: barra do passo, meta, projecao e (com ponto previsto) a ponte e o ponto',
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
  // O payload pode trazer a previsao SEM valor: o delta da Focus fica indefinido enquanto a
  // pesquisa nao tiver o trimestre-alvo numa das duas datas que ele compara. E o estado de
  // hoje, e o harness tem de reprovar regra em vez de estourar em `traces[4]` inexistente --
  // crash tambem e deteccao, mas nao diz qual regra caiu.
  const _temPt = _pontoPv;
  if (PV) {
    ok(PV.previsto_focus == null ||
       Math.abs(PV.previsto_focus - (PV.ancora + PV.delta_focus)) < 1e-9,
       'a previsao gravada e ancora + delta da Focus, a mesma identidade do backtest',
       PV.ancora + ' + ' + PV.delta_focus + ' vs ' + PV.previsto_focus);
    ok((PV.delta_focus == null) === (PV.previsto_focus == null),
       'e sem delta nao ha previsto -- os dois nulos andam juntos');
  }
  if (_temPt) {
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

    ok(Math.abs(MP.pjPrevBruto(PV) - (PV.ancora + PV.delta_focus)) < 1e-9,
       'o ponto do grafico e ancora + delta da Focus');

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
  // A contagem cresce a cada reuniao nova, entao a asserção e sobre a JANELA e a integridade,
  // nao sobre um numero escrito a mao que envelhece: a era comeca em julho de 2024 e nao ha
  // reuniao repetida nem fora de ordem.
  ok(BT.length >= 17 && BT[0].reuniao.slice(0, 7) === '2024-07',
     'o backtest comeca em jul/2024, quando o Copom passou a declarar o horizonte',
     BT.length + ' reunioes desde ' + BT[0].reuniao);
  ok(new Set(BT.map((r) => r.nro)).size === BT.length &&
     BT.every((r, i) => i === 0 || BT[i - 1].nro < r.nro),
     'uma linha por reuniao, em ordem');
  // O payload deixou de carregar o que o modelo produzia e o erro do ingenuo. Sobre o
  // PAYLOAD porque o custo de voltar a carregar e invisivel na tela: colunas que ninguem le.
  ok(BT.every((r) => !('delta_modelo' in r) && !('erro' in r) && !('erro_ingenuo' in r)),
     'e ele nao carrega mais as colunas do modelo nem a do ingenuo',
     JSON.stringify(Object.keys(BT[0])));
  const _bt = ultimoReact('chart-pj-bt');
  ok(!!_bt, 'o grafico do backtest foi plotado');
  // Sem valor previsto, o backtest nao pode prometer o ponto: nem estender o eixo, nem desenhar a
  // vertical, nem falar dele na legenda. O caso E o de hoje, e o Chrome mostrou duas frases
  // prometendo um ponto ausente antes de haver asserção para isso. O subtitulo sai da mesma
  // variavel `estende`, mas o stub nao monta o cabecalho (o div do grafico nao tem card) --
  // ele fica coberto pelo Chrome, e o eixo e a legenda seguram a condicao aqui.
  if (!_pontoPv) {
    const _capBt = String((doc.getElementById('pj-cap-bt') || {}).textContent || '');
    ok(_bt.traces[0].x.length === (P.backtest || []).length,
       'sem valor previsto o eixo do backtest nao se estende a proxima reuniao',
       String(_bt.traces[0].x.length));
    ok(!(_bt.layout.shapes || []).length, 'nem desenha a vertical da previsao');
    ok(_capBt.indexOf('vertical pontilhada') < 0,
       'e a legenda nao fala de um ponto que nao esta la', _capBt.slice(-150));
  }
  ok(_bt && _bt.traces.length === 2,
     'duas traces: o publicado e a previsao', _bt && String(_bt.traces.length));
  ok(_bt && BT.every((r, i) => _bt.traces[0].y[i] === r.real),
     'a linha grossa e o numero que o BC publicou');
  // A proxima reuniao entra como ponto extra dos TRES metodos, e e o que o grafico existe para
  // mostrar. O publicado nao ganha o ponto: o null e o que faz a linha dourada parar antes da
  // vertical, e essa parada e o sinal de que ali nao ha contrapartida do BC.
  if (_temPt) {
    ok(_bt.traces[0].x.length === BT.length + 1 &&
       _bt.traces[0].x[BT.length] === PV.data_reuniao,
       'o eixo do backtest se estende a proxima reuniao', String(_bt.traces[0].x.length));
    ok(_bt.traces[0].y[BT.length] === null,
       'e o publicado fica null nela -- a linha dourada para antes');
    const _y = _bt.traces[1].y;
    ok(_y.length === BT.length + 1 && Math.abs(_y[BT.length] - PV.previsto_focus) < 1e-12,
       'e a previsao aponta ' + PV.previsto_focus + ' para ela', String(_y[BT.length]));
    // O ponto extra do backtest e o MESMO numero do ponto do grafico 1: dois consumidores do
    // mesmo valor, e divergirem daria dois numeros diferentes na mesma tela.
    ok(Math.abs(_bt.traces[1].y[BT.length] - _s.traces[4].y[0]) < 1e-12,
       'e ele bate com o ponto previsto do grafico principal');
    ok((_bt.layout.shapes || []).length === 1 &&
       _bt.layout.shapes[0].x0 === PV.data_reuniao,
       'uma vertical pontilhada separa o conferivel do nao conferivel');
  }
  // A previsao e a linha verde, nao o dourado do publicado: a distincao entre o que o BC
  // escreveu e o que nos calculamos e a cor, aqui como no grafico de cima.
  ok(_bt.traces[1].line.color === '#418791' &&
     _bt.traces[1].line.color !== _bt.traces[0].line.color,
     'a previsao vem no verde da marca, o publicado no dourado',
     _bt.traces[1].line.color + ' vs ' + _bt.traces[0].line.color);
  ok(BT.every((r) => r.delta_focus == null ||
       Math.abs(MP.pjBtNivel(r) - (r.ancora + r.delta_focus)) < 1e-9),
     'o nivel previsto e ancora + delta da Focus');
  // Se o CSV trouxesse a coluna de erro dessincronizada do delta, o grafico e a tabela
  // discordariam em silencio.
  ok(BT.every((r) => r.erro_focus == null ||
       Math.abs(r.erro_focus - (r.ancora + r.delta_focus - r.real)) < 1e-9),
     'e erro_focus e ancora + delta menos publicado');
  ok(BT.every((r) => Math.abs(r.revisao - (r.real - r.ancora)) < 1e-9),
     'e a revisao, que a previsao tenta acertar, e publicado menos ancora');

  // MAE: contra media calculada aqui. E o numero que decide entre metodos, entao nao pode vir
  // de uma funcao que ignora null de um jeito e da tabela de outro.
  function _maeRef(campo) {
    const vs = BT.map((r) => r[campo]).filter((v) => v != null && !isNaN(v));
    return vs.reduce((a, b) => a + Math.abs(b), 0) / vs.length;
  }
  ['revisao', 'erro_focus'].forEach((campo) => {
    ok(Math.abs(MP.pjMAE(BT, campo) - _maeRef(campo)) < 1e-12,
       'pjMAE bate com a media calculada a parte em ' + campo);
  });
  ok(MP.pjMAE([], 'erro_focus') === null, 'pjMAE devolve null sem linha nenhuma');
  ok(MP.pjMAE([{erro_focus: null}], 'erro_focus') === null,
     'e null quando toda linha esta vazia');
  // A regua do ingenuo saiu do payload e passou a ser lida da coluna de REVISAO: o erro dele
  // e `ancora - publicado`, que e a revisao com o sinal trocado. A identidade tem de valer,
  // senao a barra a bater impressa na chamada deixa de ser a do ingenuo sem nada denunciar.
  ok(BT.every((r) => Math.abs(Math.abs(r.revisao) - Math.abs(r.ancora - r.real)) < 1e-9),
     'o erro do ingenuo e a revisao com o sinal trocado -- por isso ele saiu do payload');
  // O resultado que a aba existe para mostrar.
  ok(MP.pjMAE(BT, 'erro_focus') < MP.pjMAE(BT, 'revisao'),
     'MAE da previsao < o de nao prever nada (e o achado da aba)',
     MP.pjMAE(BT, 'erro_focus').toFixed(4) + ' vs ' + MP.pjMAE(BT, 'revisao').toFixed(4));
  // A chamada do backtest afirma DOIS numeros -- o nosso e a regua -- e e ela que o leitor le
  // primeiro. Sem esta asserção, trocar a coluna de que a regua sai (ou escreve-la a mao)
  // passa em silencio: o texto continua plausivel e o grafico nao o contradiz.
  {
    const _lb = String((doc.getElementById('pj-lead-bt') || {}).innerHTML || '');
    ok(_lb.indexOf(MP.fmtBR(MP.pjMAE(BT, 'erro_focus'), 3)) >= 0,
       'a chamada do backtest imprime o MAE derivado da previsao', _lb.slice(-170));
    ok(_lb.indexOf(MP.fmtBR(MP.pjMAE(BT, 'revisao'), 3)) >= 0,
       'e o da regua -- o erro de nao prever nada, lido da coluna de revisao',
       _lb.slice(-170));
  }

  // Revisao x expansao de horizonte: os dois casos existem e alternam.
  const _exp = BT.filter((r) => r.tipo === 'expansao');
  const _rev = BT.filter((r) => r.tipo === 'revisao');
  // Alternando sem excecao, as duas contagens nao podem diferir de mais de uma -- e essa e a
  // afirmação que sobrevive a cada reuniao nova, ao contrario de um 9/8 escrito a mao.
  ok(_exp.length + _rev.length === BT.length && Math.abs(_exp.length - _rev.length) <= 1,
     'expansoes e revisoes cobrem o backtest e se alternam quase meio a meio',
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
  ok(_btE.traces[1].y.every((v, j) => v == null ||
       Math.abs(v - BT[j].erro_focus) < 1e-12),
     'e a previsao plota a coluna de erro dela');
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
  // A tabela passou a por o delta previsto ao lado da revisao que aconteceu: e a conta
  // inteira, linha a linha. E o MAE do ingenuo entra sob Revisao, que e de onde ele sai.
  ok(_btTab.innerHTML.indexOf('>Previu<') >= 0 && _btTab.innerHTML.indexOf('>Erro<') >= 0,
     'a tabela traz o que a previsao disse e o erro dela, lado a lado com a revisao');
  {
    // As celulas saem do HTML e nao de `textContent`: o stub nao materializa o texto das
    // celulas montadas por innerHTML, entao ler por ali devolve nove strings vazias e as
    // asserções passam a nao afirmar nada -- foi o que aconteceu na primeira execucao.
    const _linhasHtml = _btTab.innerHTML.split('<tr');
    const _mae = _linhasHtml[_linhasHtml.length - 1];
    const _cels = _mae.split('<td').slice(1)
      .map((t) => t.slice(t.indexOf('>') + 1).replace(/<[^>]*>/g, '').trim());
    ok(_cels.length === 9, 'a linha de MAE tem uma celula por coluna',
       _cels.length + ': ' + JSON.stringify(_cels));
    ok(_cels[0] === 'MAE', 'e ela e mesmo a linha de MAE', _cels[0]);
    ok(_cels[6] === MP.fmtBR(MP.pjMAE(BT, 'revisao'), 3),
       'o MAE do ingenuo esta sob Revisao, a coluna de que ele sai', _cels[6]);
    ok(_cels[8] === MP.fmtBR(MP.pjMAE(BT, 'erro_focus'), 3),
       'e o da previsao sob Erro', _cels[8]);
  }
  // O apendice deixou de escrever os numeros a mao: eles saem do MESMO backtest, entao nao ha
  // como o texto contradizer a chamada logo acima dele -- que foi o defeito que motivou isto.
  ok(doc.getElementById('pj-ap-n').textContent === String(BT.length) &&
     doc.getElementById('pj-ap-n2').textContent === String(BT.length),
     'o apendice conta as reunioes do payload, nao um numero escrito a mao',
     doc.getElementById('pj-ap-n').textContent);
  ok(doc.getElementById('pj-ap-mae').textContent === MP.fmtBR(MP.pjMAE(BT, 'erro_focus'), 3) &&
     doc.getElementById('pj-ap-mae-ing').textContent === MP.fmtBR(MP.pjMAE(BT, 'revisao'), 3),
     'e os dois MAEs dele sao os mesmos da chamada',
     doc.getElementById('pj-ap-mae').textContent + ' / ' +
     doc.getElementById('pj-ap-mae-ing').textContent);
  {
    // "Direcao certa" so conta onde houve revisao: sem isso o denominador inclui reunioes em
    // que nao havia direcao a acertar, e a medida infla sozinha.
    const _nn = BT.filter((r) => r.revisao !== 0 && r.delta_focus != null);
    const _ok = _nn.filter((r) => r.delta_focus * r.revisao > 0);
    ok(doc.getElementById('pj-ap-dir').textContent === _ok.length + ' das ' + _nn.length,
       'e a direcao certa conta so as revisoes nao nulas',
       doc.getElementById('pj-ap-dir').textContent);
  }

  // ── Revisao dos apendices (2026-09-24) ──
  // Os textos de "Como isto e montado" e "Como ler esta tabela" tinham numeros medidos uma vez
  // (17 reunioes, 9/8, 107, 0,27/0,28, 152 mudancas), uma conclusao que se INVERTEU ("a
  // expansao e o caso mais facil" -- com 18 a previsao erra menos na revisao), uma afirmacao
  // falsa ("a vantagem e consistente" -- ela ganha em metade e perde na outra) e historia de
  // construcao escrita para o leitor ("a pedido do usuario", "ate setembro de 2026"). O guarda
  // proibe cada frase aposentada por nome, e confere os numeros novos contra conta refeita aqui.
  {
    const _norm = (t) => t.replace(/\s+/g, ' ');
    const _cdRaw = _norm(RAW.slice(RAW.indexOf('id="tab-condicoes"'), RAW.indexOf('id="tab-projecoes"')));
    const _pjTxt = _norm(_pjRaw);
    const _velhas = ['a pedido do usuário', 'até setembro de 2026', 'Havia outros dois métodos',
                     'desta pasta', 'Das 17 reuniões', '9 expansões e 8 revisões', 'caso <b>mais fácil</b>',
                     'consistente, mas não é significante', 'Medido nas 107 reuniões',
                     'das 152 mudanças', 'nas 63 reuniões', '60 células de 60', '0,037 p.p.',
                     'Custa 14 reuniões', 'sai 7 a 28 dias', 'O ramo "nenhum documento',
                     'data em que o relatório foi gerado'];
    const _achadas = _velhas.filter((f) => _pjTxt.indexOf(f) >= 0);
    ok(!_achadas.length, 'nenhuma frase aposentada volta aos apendices da aba Projecoes',
       JSON.stringify(_achadas));
    // Vocabulario de quem constroi, nao de quem le: nome de arquivo e de funcao do codigo.
    const _dev = ['_spec()', 'calendar_2026.yaml', 'condicoes_copom.py', 'carregada em <code>'];
    const _achDev = _dev.filter((f) => _cdRaw.indexOf(f) >= 0);
    ok(!_achDev.length, 'e a aba Condicoes nao ensina o leitor a mexer no codigo',
       JSON.stringify(_achDev));

    // A correlacao desvio x passo sai da mesma serie que o grafico desenha.
    const _cor = MP.pjAssoc(E.map((r) => r.proj - r.meta), E.map((r) => r.bps));
    let _ref = null;
    {
      const n = E.length, xs = E.map((r) => r.proj - r.meta), ys = E.map((r) => r.bps);
      const mx = xs.reduce((a, b) => a + b, 0) / n, my = ys.reduce((a, b) => a + b, 0) / n;
      let sxy = 0, sxx = 0, syy = 0;
      for (let k = 0; k < n; k++) {
        sxy += (xs[k] - mx) * (ys[k] - my); sxx += (xs[k] - mx) ** 2; syy += (ys[k] - my) ** 2;
      }
      _ref = sxy / Math.sqrt(sxx * syy);
    }
    ok(_cor != null && Math.abs(_cor - _ref) < 1e-12, 'pjAssoc bate com a correlacao refeita aqui',
       _cor + ' vs ' + _ref);
    ok(doc.getElementById('pj-ap-corr').textContent === MP.fmtBR(_ref, 2) &&
       doc.getElementById('pj-ap-ncorr').textContent === String(E.length),
       'e o apendice imprime essa correlacao e o n da serie',
       doc.getElementById('pj-ap-corr').textContent + ' em ' +
       doc.getElementById('pj-ap-ncorr').textContent);

    // Expansao x revisao: contagens e a frase sobre qual dos dois a previsao ganha mais.
    const _ex = BT.filter((r) => r.tipo === 'expansao'), _rv = BT.filter((r) => r.tipo === 'revisao');
    ok(doc.getElementById('pj-ap-nexp').textContent === String(_ex.length) &&
       doc.getElementById('pj-ap-nrev').textContent === String(_rv.length),
       'as contagens de expansao e revisao saem do backtest',
       doc.getElementById('pj-ap-nexp').textContent + '/' + doc.getElementById('pj-ap-nrev').textContent);
    const _tp = String((doc.getElementById('pj-ap-tipos') || {}).innerHTML || '');
    const _gR = MP.pjMAE(_rv, 'revisao') - MP.pjMAE(_rv, 'erro_focus');
    const _gE = MP.pjMAE(_ex, 'revisao') - MP.pjMAE(_ex, 'erro_focus');
    ok(_tp.indexOf('ganha mais nas <b>' + (_gR >= _gE ? 'revisões' : 'expansões') + '</b>') >= 0,
       'e a frase diz o tipo em que a previsao de fato ganha mais -- a conclusao que tinha se invertido',
       _tp.slice(-170));
    ok(_tp.indexOf(MP.fmtBR(MP.pjMAE(_rv, 'erro_focus'), 3)) >= 0 &&
       _tp.indexOf(MP.fmtBR(MP.pjMAE(_ex, 'erro_focus'), 3)) >= 0,
       'com os dois MAEs da previsao derivados', _tp.slice(-170));

    // "Nao e uniforme": melhor/pior e o t, refeitos aqui.
    const _d = BT.map((r) => Math.abs(r.revisao) - Math.abs(r.erro_focus));
    const _mel = _d.filter((x) => x > 1e-9).length, _pio = _d.filter((x) => x < -1e-9).length;
    const _md = _d.reduce((a, b) => a + b, 0) / _d.length;
    const _sd = Math.sqrt(_d.reduce((a, b) => a + (b - _md) ** 2, 0) / (_d.length - 1));
    const _t = _md / (_sd / Math.sqrt(_d.length));
    const _sg = String((doc.getElementById('pj-ap-sig') || {}).innerHTML || '');
    ok(_sg.indexOf('erra menos em ' + _mel + ' reuniões e mais em ' + _pio) >= 0,
       'o apendice diz em quantas reunioes a previsao erra menos e em quantas erra mais',
       _sg.slice(0, 160));
    ok(_sg.indexOf('t de ' + MP.fmtBR(_t, 2)) >= 0 &&
       (Math.abs(_t) < 2) === (_sg.indexOf('ainda não é') >= 0),
       'e so afirma significancia se o t a sustentar', _sg.slice(-160));

    // SINTETICO. No backtest de hoje a previsao erra menos em 9 e mais em 9, e o t esta abaixo
    // de 2: trocar melhor por pior, ou afirmar significancia sempre, nao muda uma letra do
    // texto. Um mutante de cada passou verde antes deste bloco. Aqui os numeros diferem --
    // 5 contra 1, t acima de 2, e faixas de dias que nao se sobrepoem entre os tipos.
    const _sin = [
      {tipo: 'expansao', revisao: 0.3, erro_focus: -0.05, delta_focus: 0.25, anc_dias: 30, reuniao: '2030-01-01'},
      {tipo: 'revisao', revisao: 0.2, erro_focus: 0.02, delta_focus: 0.22, anc_dias: 50, reuniao: '2030-02-01'},
      {tipo: 'expansao', revisao: -0.2, erro_focus: 0.03, delta_focus: -0.17, anc_dias: 31, reuniao: '2030-03-01'},
      {tipo: 'revisao', revisao: 0.4, erro_focus: -0.05, delta_focus: 0.35, anc_dias: 52, reuniao: '2030-04-01'},
      {tipo: 'expansao', revisao: 0.1, erro_focus: 0.0, delta_focus: 0.1, anc_dias: 30, reuniao: '2030-05-01'},
      {tipo: 'revisao', revisao: 0.0, erro_focus: 0.05, delta_focus: 0.05, anc_dias: 51, reuniao: '2030-06-01'},
    ];
    MP.renderProjecoesApendice(_sin, MP.pjMAE(_sin, 'erro_focus'), MP.pjMAE(_sin, 'revisao'));
    const _sgS = String(doc.getElementById('pj-ap-sig').innerHTML || '');
    ok(_sgS.indexOf('erra menos em 5 reuniões e mais em 1') >= 0,
       'sintetico: melhor e pior na ordem certa quando eles diferem', _sgS.slice(0, 150));
    ok(_sgS.indexOf('já é') >= 0 && _sgS.indexOf('ainda não é') < 0,
       'sintetico: com t acima de 2 o texto passa a afirmar significancia', _sgS.slice(-120));
    const _tpS = String(doc.getElementById('pj-ap-tipos').innerHTML || '');
    ok(_tpS.indexOf('revisão está a 50–52 dias') >= 0 && _tpS.indexOf('expansão a 30–31') >= 0,
       'sintetico: cada faixa de dias da ancora vai com o seu tipo', _tpS.slice(0, 200));
    MP.renderProjecoesBacktest();                  // devolve o apendice ao backtest real
  }
  // As duas tabelas viraram click-drop (<details>). Fechadas por default, entao o <summary> tem
  // de dizer o que ha dentro -- um "+" sozinho nao diz. O JS escreve a contagem la.
  ok(doc._els['pj-bt-sum'].textContent.indexOf(String(BT.length)) === 0,
     'o summary do backtest anuncia a contagem de reunioes',
     doc._els['pj-bt-sum'].textContent);
  // Tres desde 2026-09-25: a das ultimas edicoes do RPM (secao 37) entrou fechada tambem.
  ok(RAW.indexOf('<details class="tbl-fold"') >= 0 &&
     RAW.split('class="tbl-fold"').length - 1 === 3,
     'as tres tabelas da aba estao dentro de um details.tbl-fold',
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
  ok(_ref1.y.length === E.length + (_pontoPv ? 1 : 0),
     'e ela cobre a serie publicada mais o ponto previsto, quando ha um',
     _ref1.y.length + ' vs ' + (E.length + (_pontoPv ? 1 : 0)));
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

console.log('\n34. Aba Acompanhamento Condicionais: o hiato em cada edicao do RPM');
// Pedida em 2026-09-24: "um grafico para o acompanhamento das vintages do hiato do produto
// divulgado pelo BCB no RPM". Tres coisas que nenhuma excecao denunciaria se quebrassem: o
// traco que separa as duas metodologias, a leitura em tempo real (que so e "tempo real" se o
// ultimo ponto de cada edicao for o trimestre em que ela saiu), e os numeros da prosa, que
// sao TODOS derivados -- entao cada um e refeito aqui, a partir do payload, e nao lido de
// volta da propria funcao que o escreveu.
{
  const E = MP.cnEdicoes();
  ok(E.length >= 2, 'o payload traz as edicoes do hiato', String(E.length));
  ok(E.every((e) => e.dates.every((d) => [1, 4, 7, 10].indexOf(parseInt(d.slice(5, 7), 10)) >= 0)),
     'toda data de toda edicao e o primeiro mes de um trimestre');
  ok(E.every((e) => [3, 6, 9, 12].indexOf(parseInt(e.vintage.slice(5, 7), 10)) >= 0),
     'toda edicao e de mar/jun/set/dez');
  ok(E.every((e, i) => i === 0 || E[i - 1].vintage < e.vintage), 'edicoes em ordem cronologica');
  ok(E.every((e) => e.values.every((v) => v == null || typeof v === 'number')),
     'valores numericos ou nulos');

  const triDe = (iso) => parseInt(iso.slice(0, 4), 10) * 4 + Math.floor((parseInt(iso.slice(5, 7), 10) - 1) / 3);
  const val = (e, d) => { const i = e.dates.indexOf(d); return (i >= 0 && e.values[i] != null) ? e.values[i] : null; };
  // Refeito aqui, sem cnTempoReal: o ultimo ponto nao nulo de cada edicao.
  const indep = E.map((e) => {
    for (let i = e.values.length - 1; i >= 0; i--) if (e.values[i] != null) return [e.dates[i], e.values[i]];
    return null;
  });
  // A nota diz que o ultimo ponto de cada edicao e o trimestre em que ela saiu, cujo PIB
  // ainda nao existia. Uma edicao que terminasse um trimestre antes tornaria "tempo real" falso.
  ok(indep.every((x, i) => x && triDe(x[0]) === triDe(E[i].vintage)),
     'o ultimo ponto de cada edicao e o trimestre em que ela foi publicada',
     JSON.stringify(E.filter((e, i) => !indep[i] || triDe(indep[i][0]) !== triDe(e.vintage)).map((e) => e.vintage)));
  ok(MP.cnDistTri('2025-10-01', '2026-04-01') === 2 && MP.cnDistTri('2026-04-01', '2026-04-01') === 0,
     'cnDistTri conta trimestres ate o fim da edicao');

  // O traco separa as duas metodologias, e so diz algo se elas nao se intercalam. A nota
  // escreve os meses da troca por extenso ("a edicao de junho de 2024 trouxe o boxe"), entao
  // o teste amarra os dois.
  const reg = E.map((e) => e.regime);
  ok(reg.every((r) => r === 'banda' || r === 'suite'), 'regime e banda ou suite',
     JSON.stringify([...new Set(reg)]));
  const ib = reg.indexOf('suite');
  ok(ib > 0 && reg.slice(0, ib).every((r) => r === 'banda') && reg.slice(ib).every((r) => r === 'suite'),
     'as edicoes de um modelo vem todas antes das do conjunto de modelos -- uma troca so');
  ok(ib > 0 && E[ib - 1].vintage === '2024-06-01' && E[ib].vintage === '2024-09-01',
     'e a troca e entre jun/2024 e set/2024, que e o que a nota escreve',
     ib > 0 ? E[ib - 1].vintage + ' -> ' + E[ib].vintage : '-');

  // A janela inicial: o [from] do botao 5a, calculado do dado, e meio trimestre de folga a
  // direita. Registrada antes do primeiro render, que a secao 12 ja fez.
  const W = MP._chartXRange['chart-cn-hiato'];
  const datas = [...new Set([].concat(...E.map((e) => e.dates)))].sort();
  const ultD = datas[datas.length - 1];
  const d5 = new Date(Date.parse(ultD)); d5.setUTCFullYear(d5.getUTCFullYear() - 5);
  ok(!!W && W[0] === d5.toISOString().slice(0, 10),
     'a janela abre cinco anos antes do ultimo trimestre, o mesmo inicio do botao 5a', JSON.stringify(W));
  const folga = W ? (Date.parse(W[1]) - Date.parse(ultD)) / 86400000 : NaN;
  ok(folga > 30 && folga < 60,
     'e a borda direita passa do ultimo trimestre por meio trimestre, nao pelo autopad do Plotly',
     folga.toFixed(0) + 'd');

  // Render com um card de verdade em volta, para a regua de periodo ser injetada.
  const chCn = doc.getElementById('chart-cn-hiato');
  const cardCn = new El('div'); cardCn.classList.add('chart-card');
  const paiCn = new El('div'); paiCn.appendChild(cardCn); cardCn.appendChild(chCn);
  chCn._closest = cardCn;
  chamadas.length = 0;
  let _erro = null;
  try { MP.renderCnHiato(); } catch (e) { _erro = e; }
  ok(!_erro, 'renderCnHiato executa', _erro && String(_erro.stack || _erro));
  const reacts = chamadas.filter((c) => c.tipo === 'react' && c.divId === 'chart-cn-hiato');
  const r = reacts[reacts.length - 1];
  ok(!!r, 'o grafico foi plotado');
  if (r) {
    ok(r.traces.length === E.length + 1, 'uma linha por edicao mais a leitura em tempo real',
       r.traces.length + ' vs ' + (E.length + 1));
    ok(E.every((e, k) => JSON.stringify(r.traces[k].x) === JSON.stringify(e.dates)
                         && JSON.stringify(r.traces[k].y) === JSON.stringify(e.values)),
       'cada linha e a edicao do payload, sem transformacao');
    ok(E.every((e, k) => (r.traces[k].line.dash === 'dash') === (e.regime === 'banda')),
       'tracejada exatamente nas edicoes de um modelo so');
    const tr = r.traces[E.length];
    ok(tr.x.every((x, i) => x === indep[i][0]) && tr.y.every((y, i) => y === indep[i][1]),
       'a leitura em tempo real e o ultimo ponto de cada edicao, refeito aqui');
    ok(tr.mode.indexOf('markers') >= 0 && tr.line.color === '#BB9B1D',
       'e sai em pontos dourados');
    ok(tr.customdata[0].indexOf('na edição mais recente') >= 0,
       'o hover do ponto poe a primeira leitura ao lado da de hoje', tr.customdata[0]);
    ok(tr.customdata[tr.customdata.length - 1].indexOf('mais recente') < 0,
       'e o da propria edicao mais recente nao se compara com ela mesma');
    ok(r.layout.hovermode === 'closest', "hovermode 'closest' -- vinte edicoes numa caixa unificada nao se leem");
    ok(W && r.layout.xaxis.range[0] === W[0] && r.layout.xaxis.range[1] === W[1],
       'o render aplica a janela inicial', JSON.stringify(r.layout.xaxis.range));
    ok(chamadas.some((c) => c.tipo === 'relayout' && c.divId === 'chart-cn-hiato'
                            && JSON.stringify(c.upd['xaxis.range']) === JSON.stringify(W)),
       'com um relayout de X logo depois, que e o que faz o Y se ajustar a janela');
    // A rampa: a ordem das edicoes e informacao, entao a cor escurece com a data.
    const lum = (c) => { const m = /rgb\((\d+),(\d+),(\d+)\)/.exec(c); return m ? (+m[1] + +m[2] + +m[3]) : null; };
    const Ls = r.traces.slice(0, E.length - 1).map((t) => lum(t.line.color));
    ok(Ls.every((v, i) => v != null && (i === 0 || v < Ls[i - 1])),
       'as edicoes anteriores escurecem estritamente com a data', JSON.stringify(Ls.slice(0, 4)));
    const tU = r.traces[E.length - 1];
    ok(tU.line.color === '#1F2853' && tU.line.width > r.traces[0].line.width,
       'a mais recente sai da rampa, em azul e mais grossa');
    ok(r.layout.legend.traceorder === 'reversed', 'legenda da edicao mais recente para a mais antiga');
    ok(r.layout.yaxis.title.text.indexOf('potencial') >= 0,
       'o eixo diz o que o numero mede', r.layout.yaxis.title.text);
  }
  // A regua de periodo fala em trimestre, como o cabecalho e o hover.
  const barCn = paiCn.children.find((c) => c.classList.contains('period-ctrl-bar'));
  ok(!!barCn, 'a regua de periodo foi injetada');
  if (barCn) {
    const opts = barCn._roles.from.children;
    ok(opts.length && opts.every((o) => /^\d{4}T[1-4]$/.test(o.textContent)),
       'os dropdowns da regua rotulam em trimestre (2026T2), nao em mes',
       opts.length ? opts[0].textContent : '-');
    ok(W && datas[parseInt(barCn._roles.from.value, 10)] === W[0],
       'e o De ja abre no inicio da janela inicial', barCn._roles.from.value);
  }
  ok(!MP._PERIOD_LABEL['chart-pj-serie'], 'e os graficos das outras abas seguem em mes/ano');

  // "Dados no grafico": rotula so a mais recente e os pontos dourados -- vinte linhas
  // rotuladas seriam ilegiveis.
  MP.CN.dl = true;
  MP.renderCnHiato();
  const rDl = chamadas.filter((c) => c.tipo === 'react' && c.divId === 'chart-cn-hiato').pop();
  ok(rDl && Array.isArray(rDl.traces[E.length].text) && Array.isArray(rDl.traces[E.length - 1].text),
     'toggle ligado: rotula a edicao mais recente e a leitura em tempo real');
  ok(rDl && rDl.traces.slice(0, E.length - 1).every((t) => t.text === undefined),
     'e nenhuma das anteriores');
  MP.CN.dl = false;
  MP.renderCnHiato();

  // ── A prosa: cada numero refeito aqui ──
  MP.renderCnTextos(E);
  const ult = E[E.length - 1];
  const pares = indep.slice(0, -1).map((x) => ({v: x[1], h: val(ult, x[0])})).filter((p) => p.h != null);
  const media = pares.reduce((s, p) => s + (p.h - p.v), 0) / pares.length;
  const flips = pares.filter((p) => p.v * p.h < 0);
  const sgn = (v, d) => (v > 0 ? '+' : '') + MP.fmtBR(v, d);
  const lead = doc._els['cn-lead'].innerHTML;
  ok(lead.indexOf(E.length + ' edições') >= 0, 'a chamada conta as edicoes', lead.slice(0, 120));
  ok(lead.indexOf('<b>' + pares.length + '</b> leituras em tempo real') >= 0,
     'e as leituras ja revisadas', String(pares.length));
  ok(lead.indexOf(sgn(media, 2) + ' p.p.') >= 0,
     'e a revisao media da primeira leitura para a de hoje', sgn(media, 2));
  ok(pares.every((p) => p.h > p.v) === (lead.indexOf('<b>todas</b> foram revisadas para cima') >= 0),
     'a chamada so diz "todas para cima" quando todas subiram');
  ok(flips.length ? lead.indexOf('<b>' + flips.length + '</b> trocar') >= 0 : lead.indexOf('nenhuma trocou') >= 0,
     'e conta as que trocaram de sinal', String(flips.length));

  const cap = doc._els['cn-cap-hiato'].innerHTML;
  ok(cap.indexOf('tracejadas as ' + ib + ' até jun/2024') >= 0
     && cap.indexOf('contínuas as ' + (E.length - ib) + ' desde set/2024') >= 0,
     'a legenda conta as edicoes de cada metodologia', cap.slice(0, 200));

  // A revisao mora na ponta: e o que a primeira nota afirma, e o teste exige que continue
  // verdade -- se um dia deixar de ser, a frase "por isso a revisao se concentra na ponta"
  // passa a mentir.
  const ponta = [], fundo = [];
  for (let k = 1; k < E.length; k++) {
    const a = E[k - 1], b = E[k], fimA = triDe(indep[k - 1][0]);
    a.dates.forEach((d, i) => {
      const vb = val(b, d);
      if (a.values[i] == null || vb == null) return;
      (fimA - triDe(d) < 8 ? ponta : fundo).push(Math.abs(vb - a.values[i]));
    });
  }
  const mP = ponta.reduce((s, x) => s + x, 0) / ponta.length;
  const mF = fundo.reduce((s, x) => s + x, 0) / fundo.length;
  ok(doc._els['cn-ap-ponta'].innerHTML === MP.fmtBR(mP, 2) && doc._els['cn-ap-fundo'].innerHTML === MP.fmtBR(mF, 2),
     'a nota da ponta imprime as duas medias refeitas aqui',
     doc._els['cn-ap-ponta'].innerHTML + ' / ' + doc._els['cn-ap-fundo'].innerHTML);
  ok(mP > 2 * mF, 'e a ponta revisa bem mais que o meio da historia, que e o que a nota afirma',
     mP.toFixed(3) + ' vs ' + mF.toFixed(3));

  // A troca de metodologia: as duas passagens em volta dela, contra a mediana das demais.
  const mediaPar = (k) => {
    const a = E[k], b = E[k + 1], xs = [];
    a.dates.forEach((d, i) => { const vb = val(b, d); if (a.values[i] != null && vb != null) xs.push(vb - a.values[i]); });
    return xs.reduce((s, x) => s + x, 0) / xs.length;
  };
  const todasM = E.slice(1).map((_, k) => mediaPar(k));
  const volta = [todasM[ib - 2], todasM[ib - 1]];
  const outras = todasM.filter((_, k) => k !== ib - 2 && k !== ib - 1).sort((x, y) => x - y);
  const med = outras.length % 2 ? outras[(outras.length - 1) / 2]
            : (outras[outras.length / 2 - 1] + outras[outras.length / 2]) / 2;
  ok(doc._els['cn-ap-quebra'].innerHTML === sgn(volta[0], 2) + ' e ' + sgn(volta[1], 2),
     'a nota da troca imprime as duas passagens em volta dela', doc._els['cn-ap-quebra'].innerHTML);
  ok(doc._els['cn-ap-n-outras'].innerHTML === String(outras.length)
     && doc._els['cn-ap-mediana'].innerHTML === sgn(med, 2),
     'e a mediana das outras', doc._els['cn-ap-n-outras'].innerHTML + ' / ' + doc._els['cn-ap-mediana'].innerHTML);
  ok(volta.every((v) => v > med),
     'e as duas passagens revisam mais que a mediana -- senao "nao e leitura de conjuntura" nao se sustenta');
  ok(doc._els['cn-ap-ult-banda'].innerHTML === 'jun/2024' && doc._els['cn-ap-pri-suite'].innerHTML === 'set/2024',
     'a nota nomeia as duas edicoes da troca');

  // Um payload SINTETICO exercita o que o dado de hoje nao exercita: hoje toda leitura foi
  // revisada para cima, entao a frase mista e o "trocou" no singular nunca rodam. Revisoes
  // +0,70 e -0,20; uma leitura negativa que hoje e positiva.
  const Dreal = MP.D.condicionais;
  const SINT = [
    {vintage: '2024-06-01', regime: 'banda', dates: ['2024-01-01', '2024-04-01'], values: [-1, -0.5]},
    {vintage: '2024-09-01', regime: 'banda', dates: ['2024-01-01', '2024-04-01', '2024-07-01'], values: [-0.8, 0.2, 0.3]},
    {vintage: '2024-12-01', regime: 'suite', dates: ['2024-01-01', '2024-04-01', '2024-07-01', '2024-10-01'], values: [-0.9, 0.2, 0.1, 0.5]},
  ];
  MP.D.condicionais = {hiato: {edicoes: SINT}};
  MP.renderCnTextos(SINT);
  const leadS = doc._els['cn-lead'].innerHTML;
  ok(leadS.indexOf('1 foram revisadas para cima e 1 para baixo') >= 0,
     'sintetico: revisao mista vira contagem nos dois sentidos', leadS);
  ok(leadS.indexOf('<b>1</b> trocou de sinal — saiu negativa e hoje é positiva') >= 0,
     'sintetico: uma troca de sinal, no singular e com o sentido');
  ok(leadS.indexOf('+0,25 p.p.') >= 0, 'sintetico: media (+0,70 - 0,20) / 2');
  ok(doc._els['cn-ap-quebra'].innerHTML === '+0,45 e -0,10',
     'sintetico: as duas passagens em volta da troca', doc._els['cn-ap-quebra'].innerHTML);
  MP.D.condicionais = Dreal;
  MP.renderCnTextos(E);

  // A prosa desta aba e para quem abre a pagina: sem vocabulario de mecanismo. Sobre o TEXTO
  // da aba -- sem comentarios HTML e sem tags, senao um id como `cn-ap-pri-suite` reprova --,
  // mais o que o JS escreve.
  const iA = RAW.indexOf('id="tab-condicionais"'), iB = RAW.indexOf('</main>');
  const fatia = ((iA >= 0 && iB > iA ? RAW.slice(iA, iB) : '')
    + doc._els['cn-lead'].innerHTML + doc._els['cn-cap-hiato'].innerHTML)
    .replace(/<!--[\s\S]*?-->/g, '').replace(/<[^>]*>/g, ' ');
  ok(fatia.length > 2000, 'a fatia da aba foi achada', String(fatia.length));
  ['payload', 'MySQL', 'pm_hiato', 'vintages', 'ETL', 'regime', 'suite', 'central_'].forEach((t) => {
    ok(fatia.indexOf(t) < 0, 'a prosa da aba nao usa "' + t + '"');
  });

  // O stub cria elemento para qualquer id, entao um id que o JS busca e o markup nao tem
  // passaria por tudo acima e deixaria um buraco no browser. Checagem estatica.
  const _ids = new Set();
  const _re = /(?:getElementById|put|wireDlToggle)\(\s*'((?:cn-|chart-cn-|dl-chart-cn-)[\w-]+)'/g;
  let _m;
  while ((_m = _re.exec(SRC))) _ids.add(_m[1]);
  ok(_ids.size >= 10, 'a checagem de ids achou os alvos da aba no script', String(_ids.size));
  const _falta = [..._ids].filter((id) => RAW.indexOf('id="' + id + '"') < 0);
  ok(!_falta.length, 'todo id que o JS da aba busca existe no markup', JSON.stringify(_falta));
}

console.log('\n35. Aba Acompanhamento Condicionais: o caminho da Selic antes de cada reuniao');
// Pedido de 2026-09-24, logo depois do hiato ("Just the Selic Path"). O que nenhuma excecao
// denunciaria: a pesquisa de um dia errado (lookahead se for depois da sexta de corte), um
// caminho deslocado de uma reuniao (a posicao "R<n>/<ano>" da Focus nao e data), a ancora
// fora da Selic vigente, e as frases -- todas derivadas, entao refeitas aqui.
{
  const S = (MP.D.condicionais || {}).selic || {};
  const CS = S.caminhos || [];
  const H = S.hoje || null;
  const EF = S.efetiva || {dates: [], values: []};
  ok(CS.length > 100, 'o payload traz os caminhos desde 2006', String(CS.length));
  ok(CS[0] && CS[0].reuniao.slice(0, 4) === '2006', 'e o primeiro e de 2006, o primeiro ano de oito reunioes',
     CS[0] && CS[0].reuniao);
  ok(CS.every((c, i) => i === 0 || CS[i - 1].reuniao < c.reuniao), 'um caminho por reuniao, em ordem');

  // A sexta-feira ESTRITAMENTE anterior a decisao, refeita aqui.
  const sexta = (iso) => {
    const d = new Date(Date.parse(iso + 'T00:00:00Z'));
    const recua = ((d.getUTCDay() - 5 + 7) % 7) || 7;
    return new Date(d.getTime() - recua * 86400000).toISOString().slice(0, 10);
  };
  const dias = (a, b) => (Date.parse(b) - Date.parse(a)) / 86400000;
  ok(CS.every((c) => c.pesquisa <= sexta(c.reuniao)),
     'nenhuma pesquisa depois da sexta-feira anterior a decisao -- sem olhar o futuro',
     JSON.stringify(CS.filter((c) => c.pesquisa > sexta(c.reuniao)).map((c) => c.nro)));
  ok(CS.every((c) => dias(c.pesquisa, sexta(c.reuniao)) <= 7),
     'e nenhuma mais velha que uma semana antes dela');
  ok(CS.every((c) => c.dates[0] === c.pesquisa), 'todo caminho comeca no dia da pesquisa');
  ok(CS.every((c) => c.dates.every((d, i) => i === 0 || c.dates[i - 1] < d)),
     'datas estritamente crescentes dentro de cada caminho');
  // O primeiro degrau e a propria reuniao: um caminho deslocado de uma posicao comecaria na
  // reuniao seguinte (ou na anterior, que ja passou).
  ok(CS.every((c) => c.dates[1] === c.reuniao && /^R[1-8]\/\d{4}$/.test(c.rotulos[1])),
     'o primeiro degrau de todo caminho e a propria reuniao que ele antecede',
     JSON.stringify(CS.filter((c) => c.dates[1] !== c.reuniao).map((c) => c.nro).slice(0, 5)));
  // E a mediana para a propria reuniao nunca errou a decisao por um ciclo inteiro: e o que
  // confere o mapeamento posicao -> reuniao contra um dado independente.
  const comDec = CS.filter((c) => c.decidida != null);
  const piorSurpresa = Math.max(...comDec.map((c) => Math.abs(c.decidida - c.values[1])));
  ok(piorSurpresa <= 0.5, 'a Focus nunca errou a decisao da propria reuniao por mais de 50 p.b.',
     piorSurpresa.toFixed(3));
  // A ancora e a Selic vigente: a decisao mais recente ANTES do dia da pesquisa.
  const vig = (iso) => { let v = null; EF.dates.forEach((d, i) => { if (d < iso) v = EF.values[i]; }); return v; };
  ok(CS.every((c) => c.values[0] === vig(c.pesquisa)),
     'a ancora de cada caminho e a Selic vigente no dia da pesquisa, refeita da Selic efetiva',
     JSON.stringify(CS.filter((c) => c.values[0] !== vig(c.pesquisa)).map((c) => c.nro).slice(0, 5)));
  ok(CS.every((c) => c.estimada[0] === false && c.rotulos[0] === ''), 'a ancora nao e reuniao');
  // Reuniao passada tem data real, sempre: so o futuro sem calendario e estimado.
  const ultReu = CS[CS.length - 1].reuniao;
  ok(CS.concat(H ? [H] : []).every((c) => c.dates.every((d, i) => !c.estimada[i] || d > ultReu)),
     'nenhuma data estimada cai antes da ultima reuniao decidida');
  ok(EF.dates.every((d, i) => i === 0 || EF.dates[i - 1] < d) && EF.values.every((v) => v > 0 && v < 30),
     'a Selic efetiva e uma serie ordenada e plausivel');
  ok(EF.dates[0] <= CS[0].pesquisa && EF.dates[1] > CS[0].pesquisa,
     'e ela comeca na decisao que vigorava na primeira pesquisa, nem antes nem depois',
     EF.dates.slice(0, 2).join(' , '));

  if (H) {
    ok(H.pesquisa > CS[CS.length - 1].pesquisa, 'o caminho de hoje e posterior ao corte da ultima reuniao');
    ok(H.dates[1] === H.reuniao && H.reuniao > ultReu, 'e comeca na proxima reuniao', H.reuniao);
    ok(H.provisorio === (H.pesquisa < sexta(H.reuniao)),
       'provisorio exatamente enquanto a sexta-feira de corte nao chegou');
  }

  // ── Render ──
  const chS = doc.getElementById('chart-cn-selic');
  const cardS = new El('div'); cardS.classList.add('chart-card');
  const paiS = new El('div'); paiS.appendChild(cardS); cardS.appendChild(chS);
  chS._closest = cardS;
  chamadas.length = 0;
  let _e = null;
  try { MP.renderCnSelic(); } catch (e) { _e = e; }
  ok(!_e, 'renderCnSelic executa', _e && String(_e.stack || _e));
  const r = chamadas.filter((c) => c.tipo === 'react' && c.divId === 'chart-cn-selic').pop();
  ok(!!r, 'o grafico foi plotado');
  if (r) {
    const T = r.traces, n = CS.length;
    ok(T.length === n + (H ? 1 : 0) + 1, 'um trace por caminho, mais o de hoje, mais a Selic efetiva',
       T.length + ' vs ' + (n + (H ? 1 : 0) + 1));
    ok(CS.every((c, k) => JSON.stringify(T[k].x) === JSON.stringify(c.dates)
                         && JSON.stringify(T[k].y) === JSON.stringify(c.values)),
       'cada caminho e o do payload, sem transformacao');
    ok(T.every((t) => t.line.shape === 'hv'), "todos em degrau ('hv'): a Selic anda na reuniao, nao entre elas");
    const grupo = T.slice(0, n - 1);
    ok(grupo.every((t) => t.legendgroup === 'antes') && grupo.filter((t) => t.showlegend).length === 1,
       'os caminhos anteriores dividem UMA entrada de legenda');
    const lum = (c) => { const m = /rgb\((\d+),(\d+),(\d+)\)/.exec(c); return m ? (+m[1] + +m[2] + +m[3]) : null; };
    const Ls = grupo.map((t) => lum(t.line.color));
    ok(Ls.every((v, i) => v != null && (i === 0 || v <= Ls[i - 1])) && Ls[0] > Ls[Ls.length - 1],
       'e escurecem com a data');
    ok(T[n - 1].line.color === '#02739B', 'o da ultima reuniao decidida em azul-claro');
    if (H) ok(T[n].line.color === '#1F2853' && T[n].line.width === 3, 'o de hoje em azul, mais grosso');
    const tEf = T[T.length - 1];
    ok(tEf.line.color === '#BB9B1D' && JSON.stringify(tEf.y) === JSON.stringify(EF.values),
       'e a Selic efetiva em dourado, por ultimo, por cima de tudo');
    ok(r.layout.hovermode === 'closest', "hovermode 'closest'");
    ok(T[0].customdata[0].indexOf('Selic vigente em') === 0, 'o hover da ancora diz que ela e a Selic vigente');
    const kEst = H ? H.estimada.indexOf(true) : -1;
    if (kEst > 0) {
      ok(T[n].customdata[kEst].indexOf('(data estimada)') >= 0,
         'e o de uma reuniao sem calendario diz que a data e estimada', T[n].customdata[kEst]);
    }
    const W = MP._chartXRange['chart-cn-selic'];
    const todas = [...new Set([].concat(...T.map((t) => t.x)))].sort();
    const d5 = new Date(Date.parse(todas[todas.length - 1])); d5.setUTCFullYear(d5.getUTCFullYear() - 5);
    const de = todas.find((d) => d >= d5.toISOString().slice(0, 10));
    ok(W && W[0] === de, 'a janela abre na primeira data real dos ultimos cinco anos ate o fim do caminho',
       JSON.stringify(W) + ' vs ' + de);
    ok(W && W[1] > todas[todas.length - 1], 'com folga a direita do ultimo degrau');
    const barS = paiS.children.find((c) => c.classList.contains('period-ctrl-bar'));
    ok(barS && barS._roles.from.children.every((o) => /^\d{2}\/\d{2}\/\d{4}$/.test(o.textContent)),
       'a regua rotula por dia: sexta de corte e quarta da decisao caem no mesmo mes',
       barS ? barS._roles.from.children[0].textContent : '-');
    ok(barS && todas[parseInt(barS._roles.from.value, 10)] === W[0], 'e o De abre no inicio da janela');
  }
  MP.CN.dlSel = true;
  MP.renderCnSelic();
  const rD = chamadas.filter((c) => c.tipo === 'react' && c.divId === 'chart-cn-selic').pop();
  const kD = CS.length - 1 + (H ? 1 : 0);
  ok(rD && Array.isArray(rD.traces[kD].text) && rD.traces[kD].text[0] === '',
     'toggle ligado: rotula o caminho em destaque, menos a ancora');
  ok(rD && rD.traces.filter((t) => Array.isArray(t.text)).length === 1, 'e so ele');
  MP.CN.dlSel = false;
  MP.renderCnSelic();

  // ── A prosa, refeita aqui ──
  MP.renderCnSelicTextos();
  const lead = doc._els['cn-lead-selic'].innerHTML;
  ok(lead.indexOf('São ' + CS.length + ' reuniões') >= 0, 'a chamada conta os caminhos');
  const ultC = CS[CS.length - 1];
  if (H) {
    const mapa = {}; ultC.rotulos.forEach((rt, i) => { if (i) mapa[rt] = ultC.values[i]; });
    const com = H.rotulos.map((rt, i) => (i && mapa[rt] != null) ? H.values[i] - mapa[rt] : null).filter((x) => x != null);
    const mud = com.filter((x) => Math.abs(x) > 1e-9);
    ok(mud.length ? lead.indexOf('mudou em <b>' + mud.length + '</b> das ' + com.length) >= 0
                  : lead.indexOf('não mudou em nenhuma das ' + com.length) >= 0,
       'e conta quantas reunioes o caminho de hoje mudou contra o da ultima decidida', mud.length + '/' + com.length);
    ok(lead.indexOf('de 11,00% para 11,00%') < 0 && !/de ([\d,]+)% para \1%/.test(lead),
       'e nunca descreve uma "mudanca" de um numero para ele mesmo');
  }
  // Nenhuma nota pontua a pesquisa contra a decisao (decisao do usuario, 2026-09-24): a
  // Focus e a curva sao lidas como expectativa e preco, nao como previsao.
  ok(['cn-ap-sel-n', 'cn-ap-sel-acerto', 'cn-ap-sel-erro'].every((id) => !RAW.includes('id="' + id + '"')),
     'a aba nao conta quantas decisoes bateram com a mediana');
  if (H) {
    const nE = H.estimada.filter(Boolean).length;
    ok(doc._els['cn-ap-sel-est'].innerHTML === nE + ' das ' + (H.estimada.length - 1) + ' reuniões',
       'a nota das datas conta as estimadas no caminho de hoje', doc._els['cn-ap-sel-est'].innerHTML);
    ok(doc._els['cn-ap-sel-prov'].innerHTML.indexOf(sexta(H.reuniao).split('-').reverse().join('/')) >= 0,
       'e a nota do corte nomeia a sexta-feira certa');
  }

  // Sintetico: exercita os ramos que o dado de hoje nao exercita -- mudanca nos dois sentidos
  // e a pagina sem caminho de hoje.
  const Dsel = MP.D.condicionais.selic;
  const mk = (nro, reu, pq, dec, pares) => ({
    nro, reuniao: reu, pesquisa: pq, decidida: dec,
    dates: [pq].concat(pares.map((p) => p[0])), values: [14].concat(pares.map((p) => p[1])),
    rotulos: [''].concat(pares.map((p) => p[2])), estimada: [false].concat(pares.map(() => false)),
  });
  MP.D.condicionais.selic = {
    caminhos: [
      mk(1, '2027-01-27', '2027-01-22', 14.25, [['2027-01-27', 14, 'R1/2027'], ['2027-03-17', 13.75, 'R2/2027'], ['2027-05-05', 13.5, 'R3/2027']]),
      mk(2, '2027-03-17', '2027-03-12', 13.5, [['2027-03-17', 13.75, 'R2/2027'], ['2027-05-05', 13.5, 'R3/2027'], ['2027-06-16', 13.25, 'R4/2027']]),
    ],
    hoje: Object.assign(mk(3, '2027-05-05', '2027-03-26', null,
      [['2027-05-05', 13.25, 'R3/2027'], ['2027-06-16', 13.5, 'R4/2027']]), {provisorio: true}),
    efetiva: {dates: ['2026-12-09', '2027-01-27', '2027-03-17'], values: [14, 14.25, 13.5]},
  };
  MP.renderCnSelicTextos();
  const lS = doc._els['cn-lead-selic'].innerHTML;
  ok(lS.indexOf('mudou em <b>2</b> das 2 reuniões que os dois cotam, entre −25 e +25 p.b.') >= 0,
     'sintetico: mudanca nos dois sentidos vira faixa', lS);
  ok(lS.indexOf('na mais distante das que mudaram, a 4ª reunião de 2027, de 13,25% para 13,50%') >= 0,
     'sintetico: e a mais distante e a das que MUDARAM');
  MP.D.condicionais.selic = Object.assign({}, MP.D.condicionais.selic, {hoje: null});
  MP.renderCnSelicTextos();
  ok(doc._els['cn-lead-selic'].innerHTML.indexOf('linha azul') < 0
     && doc._els['cn-cap-selic'].innerHTML.indexOf('Azul: o de hoje') < 0,
     'sintetico: sem caminho de hoje, nenhuma frase fala da linha azul');
  MP.D.condicionais.selic = Dsel;
  MP.renderCnSelicTextos();
}

{
  // Vocabulario de mecanismo tambem fora do texto que o JS escreve para a Selic.
  const txt = (doc._els['cn-lead-selic'].innerHTML + doc._els['cn-cap-selic'].innerHTML)
    .replace(/<[^>]*>/g, ' ');
  ['payload', 'MySQL', 'expc_focus', 'base_calculo', 'rotulos', 'provisorio'].forEach((t) => {
    ok(txt.indexOf(t) < 0, 'a prosa da Selic nao usa "' + t + '"');
  });
}


console.log('\n36. Aba Expectativas de Juros: a pesquisa e a curva, reuniao a reuniao');
// Pedida em 2026-09-24: levar para ca o que o relatorio de Expectativas dizia de politica
// monetaria (a aba Curva do Copom) e ler "o que a curva de juros esta precificando". Com uma
// condicao do usuario: nada de RMSE, erro medio ou contagem de acerto -- a pesquisa e a curva
// sao lidas como expectativa e preco, nao como previsao. A conferencia de que a leitura da
// curva esta certa existe, mas mora em tests/test_expectativas_juros.py, nao na tela. O que
// este bloco cobra, e nada disso levantaria excecao se quebrasse: nenhuma semana cotando
// reuniao que ja passou, a fila de "reuniao a frente" contada a partir da data certa, os
// caminhos ancorados na Selic vigente, a distancia curva-pesquisa so entre a MESMA reuniao,
// a janela que acompanha a comparacao escolhida, e cada numero da prosa refeito aqui.
{
  const X = MP.D.expectativas || {};
  ok(X.focus && X.di && X.reunioes && X.reunioes.length > 100, 'o payload traz as duas fontes e a lista de reunioes');
  const R = X.reunioes;
  ok(R.every((r, i) => i === 0 || R[i - 1].d < r.d), 'reunioes em ordem estrita de data');
  ok(R.every((r) => /^R[1-8]\/\d{4}$/.test(r.rot)), 'toda reuniao tem a posicao no ano (R<n>/<ano>)');
  const decididas = R.filter((r) => r.selic != null);
  const ultDec = decididas[decididas.length - 1].d;
  ok(R.every((r) => !r.est || r.d > ultDec), 'data estimada so depois da ultima reuniao decidida');
  const vigDe = (d) => { let v = null; R.forEach((r) => { if (r.d < d && r.selic != null) v = r.selic; }); return v; };
  ['focus', 'di'].forEach((f) => {
    const S = X[f], campo = f === 'di' ? 'v' : 'm';
    ok(S.datas.every((d, i) => i === 0 || MP.ejSegunda(S.datas[i - 1]) < MP.ejSegunda(d)),
       f + ': uma data por semana, em ordem, nunca duas na mesma semana');
    ok(S.datas.every((d, i) => { const j = S.j0[i]; return (j >= R.length || R[j].d >= d) && (j === 0 || R[j - 1].d < d); }),
       f + ': a fila de cada semana comeca na primeira reuniao ainda por acontecer');
    let passou = 0;
    Object.keys(S.por_reuniao).forEach((k) => {
      const b = S.por_reuniao[k];
      b[campo].forEach((v, t) => { if (v != null && S.datas[b.i0 + t] > R[+k].d) passou++; });
    });
    ok(passou === 0, f + ': nenhuma semana cota uma reuniao que ja passou', String(passou));
    ok(S.datas.every((d, i) => S.vig[i] === vigDe(d)), f + ': a Selic vigente de cada semana, refeita das decisoes');
  });
  // A diferenca meta - CDI do primeiro overnight: 0,10 p.p. na maior parte do tempo, e os
  // extremos medidos sao episodios reais (nov/2008, CDI bem abaixo da meta na crise; fim de
  // 2012) -- a faixa pega uma troca de sinal ou de unidade, nao um dia atipico.
  ok(X.di.spread.every((s) => s == null || (s > -0.1 && s < 0.8)), 'di: meta menos CDI do overnight entre -0,1 e 0,8 p.p.');
  let fora = 0;
  Object.values(X.focus.por_reuniao).forEach((b) => b.m.forEach((m, t) => {
    if (m != null && b.lo[t] != null && b.hi[t] != null && (m < b.lo[t] - 1e-9 || m > b.hi[t] + 1e-9)) fora++;
  }));
  ok(fora === 0, 'focus: a mediana sempre dentro da faixa das respostas', String(fora));
  const b1ini = Object.values(X.focus.por_reuniao).reduce((a, b) => {
    const t = b.b1.findIndex((v) => v != null);
    return t < 0 ? a : (a == null || X.focus.datas[b.i0 + t] < a ? X.focus.datas[b.i0 + t] : a);
  }, null);
  ok(b1ini >= '2021-03-01', 'as respostas de 4 dias uteis nao inventam historia antes de 2021', b1ini);

  // ── Render ──
  const cards = {};
  ['chart-ej-hoje', 'chart-ej-reuniao', 'chart-ej-hz', 'chart-ej-gap'].forEach((id) => {
    const ch = doc.getElementById(id);
    const card = new El('div'); card.classList.add('chart-card');
    const pai = new El('div'); pai.appendChild(card); card.appendChild(ch);
    ch._closest = card; cards[id] = pai;
  });
  chamadas.length = 0;
  let _e = null;
  try { MP.renderExpectativas(); } catch (e) { _e = e; }
  ok(!_e, 'renderExpectativas executa', _e && String(_e.stack || _e));
  const ult = (id) => chamadas.filter((c) => c.tipo === 'react' && c.divId === id).pop();

  // 1. O caminho de hoje, refeito do payload.
  const cam = (f, i) => {
    const S = X[f], campo = f === 'di' ? 'v' : 'm', pts = [];
    for (let j = S.j0[i]; j < R.length; j++) {
      const b = S.por_reuniao[String(j)];
      const v = b ? b[campo][i - b.i0] : null;
      if (v != null) pts.push([R[j].d, v]);
    }
    return {x: [S.datas[i]].concat(pts.map((p) => p[0])), y: [S.vig[i]].concat(pts.map((p) => p[1]))};
  };
  const rH = ult('chart-ej-hoje');
  ok(!!rH, 'o caminho de hoje foi plotado');
  if (rH) {
    const T = rH.traces;
    ok(T.length === 4, 'com a comparacao default: as duas de hoje e as duas de 4 semanas antes', String(T.length));
    const tF = T[T.length - 2], tD = T[T.length - 1];
    const cF = cam('focus', X.focus.datas.length - 1), cD = cam('di', X.di.datas.length - 1);
    ok(JSON.stringify(tF.x) === JSON.stringify(cF.x) && JSON.stringify(tF.y) === JSON.stringify(cF.y),
       'a pesquisa de hoje e a do payload, ancorada na Selic vigente e com um degrau por reuniao');
    ok(JSON.stringify(tD.x) === JSON.stringify(cD.x) && JSON.stringify(tD.y) === JSON.stringify(cD.y),
       'e a curva de hoje tambem');
    ok(tF.line.color === '#1F2853' && tD.line.color === '#BB9B1D' && tF.line.width === 3,
       'pesquisa em azul, curva em dourado, as duas grossas');
    ok(T.every((t) => t.line.shape === 'hv'), "tudo em degrau ('hv')");
    ok(T.slice(0, 2).every((t) => t.line.dash === 'dash'), 'as de 4 semanas antes tracejadas');
    ok(tF.customdata[0].indexOf('Selic vigente em') === 0, 'o hover da ancora diz que ela e a Selic vigente');
    const kE = tF.x.findIndex((d, k) => k > 0 && R.find((r) => r.d === d).est);
    if (kE > 0) ok(tF.customdata[kE].indexOf('(data estimada)') >= 0, 'e o de uma reuniao sem data marcada diz isso');
    ok(rH.layout.hovermode === 'x unified', "hover 'x unified': as duas fontes lado a lado em cada reuniao");
  }
  // O toggle rotula so as duas de hoje, e nunca a ancora.
  MP.EJ.dlHoje = true; MP.renderEjHoje();
  const rHd = ult('chart-ej-hoje');
  ok(rHd && rHd.traces.filter((t) => Array.isArray(t.text)).length === 2 &&
     rHd.traces.slice(-2).every((t) => t.text[0] === ''), 'toggle ligado: rotula as duas de hoje, menos a ancora');
  MP.EJ.dlHoje = false;
  // A comparacao muda ate onde o grafico vai para tras, e a janela tem de ir junto -- senao o
  // caminho de 52 semanas antes aparece cortado ao meio.
  const pg = doc.getElementById('pg-ej-comp');
  const pill = (txt) => pg.children.find((b) => b.textContent.indexOf(txt) === 0);
  pill('52 semanas').fire('click');
  const i52 = MP.ejSemanaAtras('focus', 52);
  ok(MP._chartXRange['chart-ej-hoje'][0] <= X.focus.datas[i52],
     'escolher 52 semanas alarga a janela ate o caminho de um ano atras', JSON.stringify(MP._chartXRange['chart-ej-hoje']));
  ok(Date.parse(X.focus.datas[X.focus.datas.length - 1]) - Date.parse(X.focus.datas[i52]) >= 52 * 7 * 86400000,
     'e "52 semanas antes" e por data, nao por posicao');
  pill('Nenhuma').fire('click');
  ok(ult('chart-ej-hoje').traces.length === 2, '"Nenhuma" deixa so as duas de hoje');
  pill('4 semanas').fire('click');

  // 2. Uma reuniao: a proxima por default, e uma decidida pelo seletor.
  const rR = ult('chart-ej-reuniao');
  const jProx = X.focus.j0[X.focus.j0.length - 1];
  ok(MP.EJ.reuniao === jProx, 'a segunda secao abre na proxima reuniao', MP.EJ.reuniao + ' vs ' + jProx);
  const tit = cards['chart-ej-reuniao'].children.find((c) => c.classList.contains('chart-card')).children.find((c) => c.className.indexOf('chart-head') === 0);
  ok(tit && tit.children[0].textContent.indexOf(R[jProx].nro + 'ª') >= 0, 'e o titulo nomeia a reuniao',
     tit && tit.children[0].textContent);
  if (rR) {
    const T = rR.traces;
    const bF = X.focus.por_reuniao[String(jProx)];
    const med = T.find((t) => t.name === 'Pesquisa Focus, mediana');
    ok(med && JSON.stringify(med.y) === JSON.stringify(bF.m.filter((v) => v != null)),
       'a mediana e a do payload, semana a semana');
    ok(med && med.x.every((d) => d <= R[jProx].d), 'e nenhuma semana depois da reuniao');
    const faixa = T.findIndex((t) => t.fill === 'tonexty');
    ok(faixa > 0 && T[faixa - 1].hoverinfo === 'skip', 'a faixa e o par piso/teto, com o piso fora do hover');
    ok(!T.some((t) => t.name === 'Decidida na reuniao' || t.name === 'Decidida na reunião'),
       'reuniao ainda nao decidida: sem marca de decisao');
  }
  const sel = doc.getElementById('sel-ej-reuniao');
  const jDec = R.findIndex((r) => r.d === ultDec);
  sel.value = String(jDec); sel.fire('change');
  const rR2 = ult('chart-ej-reuniao');
  const mk = rR2 && rR2.traces.find((t) => t.name === 'Decidida na reunião');
  ok(mk && mk.y[0] === R[jDec].selic && mk.x[0] === R[jDec].d, 'o seletor troca a reuniao, e a decidida ganha a marca da decisao');
  ok(doc._els['ej-lead-reu'].innerHTML.indexOf('O Copom decidiu <b>') >= 0, 'e a chamada diz o que foi decidido');
  sel.value = String(jProx); sel.fire('change');

  // 3. A n-esima reuniao a frente e a distancia, refeitas.
  const hz = (f, n) => {
    const S = X[f], campo = f === 'di' ? 'v' : 'm', o = {};
    S.datas.forEach((d, i) => {
      const j = S.j0[i] + n - 1, b = S.por_reuniao[String(j)];
      const v = b ? b[campo][i - b.i0] : null;
      if (v != null) o[d] = [j, v];
    });
    return o;
  };
  const rZ = ult('chart-ej-hz'), rG = ult('chart-ej-gap');
  if (rZ) {
    const H4 = hz('focus', 4);
    const tF = rZ.traces.find((t) => t.name === 'Pesquisa Focus, mediana');
    ok(tF && tF.x.length === Object.keys(H4).length && tF.x.every((d, k) => H4[d] && H4[d][1] === tF.y[k]),
       'a 4a reuniao a frente, semana a semana, refeita da fila');
  }
  if (rG) {
    const F4 = hz('focus', 4), D4 = hz('di', 4), porSem = {};
    Object.keys(D4).forEach((d) => { porSem[MP.ejSegunda(d)] = D4[d]; });
    const esp = Object.keys(F4).filter((d) => porSem[MP.ejSegunda(d)] && porSem[MP.ejSegunda(d)][0] === F4[d][0]);
    const g = rG.traces[0];
    ok(g.x.length === esp.length && g.x.every((d, k) => Math.abs(g.y[k] - (porSem[MP.ejSegunda(d)][1] - F4[d][1]) * 100) < 0.051),
       'a distancia curva - pesquisa, em p.b., so nas semanas em que as duas cotam a MESMA reuniao', g.x.length + ' vs ' + esp.length);
    ok(g.marker.color.every((c, k) => c === (g.y[k] >= 0 ? '#BB9B1D' : '#1F2853')), 'dourado acima, azul abaixo');
  }
  doc.getElementById('pg-ej-hz').children.find((b) => b.textContent === '8ª').fire('click');
  ok(MP.EJ.hz === 8 && ult('chart-ej-hz') !== rZ, 'a pill de posicao redesenha a secao');
  const tit8 = cards['chart-ej-hz'].children.find((c) => c.classList.contains('chart-card')).children.find((c) => c.className.indexOf('chart-head') === 0);
  ok(tit8 && tit8.children[0].textContent.indexOf('8ª') >= 0, 'e o titulo acompanha a posicao');
  doc.getElementById('pg-ej-hz').children.find((b) => b.textContent === '4ª').fire('click');

  // ── A prosa, refeita aqui ──
  const brl = (v, d) => v.toFixed(d).replace('.', ',');
  const sel3 = (v) => brl(v, Math.round(v * 1000) % 10 !== 0 ? 3 : 2);
  const lead = doc._els['ej-lead'].innerHTML;
  const cF = cam('focus', X.focus.datas.length - 1), cD = cam('di', X.di.datas.length - 1);
  ok(lead.indexOf(R[jProx].nro + 'ª reunião</b>, a próxima') >= 0, 'a chamada nomeia a proxima reuniao', lead.slice(0, 400));
  ok(lead.indexOf('espera <b>' + sel3(cF.y[1]) + '%</b>') >= 0 && lead.indexOf('precifica <b>' + brl(cD.y[1], 2) + '%</b>') >= 0,
     'e poe o numero das duas para ela');
  ok(lead.indexOf('reunião reunião') < 0 && !/\([^()]*\([^()]*\)[^()]*\)/.test(lead.replace(/<[^>]*>/g, '')),
     'sem "reuniao reuniao" nem parentese dentro de parentese');
  const anoQV = String(parseInt(cF.x[0].slice(0, 4), 10) + 1);
  const comuns = cF.x.filter((d, k) => k > 0 && d.slice(0, 4) === anoQV && cD.x.indexOf(d) > 0);
  if (comuns.length) {
    const dU = comuns[comuns.length - 1];
    const gap = Math.round((cD.y[cD.x.indexOf(dU)] - cF.y[cF.x.indexOf(dU)]) * 100);
    ok(lead.indexOf(Math.abs(gap) + ' p.b. ' + (gap > 0 ? 'acima' : 'abaixo')) >= 0,
       'e a distancia na ultima reuniao do ano que vem, refeita', String(gap));
  }
  const lz = doc._els['ej-lead-hz'].innerHTML;
  const F4 = hz('focus', 4), D4 = hz('di', 4), porSem = {};
  Object.keys(D4).forEach((d) => { porSem[MP.ejSegunda(d)] = D4[d]; });
  const com4 = Object.keys(F4).filter((d) => porSem[MP.ejSegunda(d)] && porSem[MP.ejSegunda(d)][0] === F4[d][0]).sort();
  const dUlt = com4[com4.length - 1];
  const gUlt = Math.round((porSem[MP.ejSegunda(dUlt)][1] - F4[dUlt][1]) * 1000) / 10;
  ok(lz.indexOf('Na semana de ' + dUlt.split('-').reverse().join('/')) >= 0 &&
     lz.indexOf(brl(Math.abs(gUlt), 0) + ' p.b. ' + (gUlt > 0 ? 'acima' : 'abaixo')) >= 0,
     'a chamada da fila da a distancia da semana mais recente com as duas', gUlt + ' em ' + dUlt);
  const ano = Date.parse(dUlt) - 365 * 86400000;
  const doze = com4.filter((d) => Date.parse(d) > ano).map((d) => Math.round((porSem[MP.ejSegunda(d)][1] - F4[d][1]) * 1000) / 10);
  const sgn = (x) => (x > 0 ? '+' : x < 0 ? '−' : '') + brl(Math.abs(x), 0);
  ok(lz.indexOf('entre ' + sgn(Math.min(...doze)) + ' e ' + sgn(Math.max(...doze)) + ' p.b.') >= 0,
     'e a faixa dos doze meses ate ali', sgn(Math.min(...doze)) + ' / ' + sgn(Math.max(...doze)));
  ok(lz.indexOf('por a ') < 0, 'e nao escreve "por a pesquisa"');
  let kS = X.di.spread.length - 1; while (X.di.spread[kS] == null) kS--;
  ok(doc._els['ej-ap-spread'].innerHTML === brl(X.di.spread[kS], 2), 'a nota da diferenca CDI-meta usa a do pregao mais recente');
  const nEst = cF.x.filter((d, k) => k > 0 && R.find((r) => r.d === d).est).length;
  ok(doc._els['ej-ap-est'].innerHTML === nEst + ' das ' + (cF.x.length - 1) + ' reuniões', 'a nota das datas conta as estimadas');

  // Nenhuma estatistica de acerto, e nenhum vocabulario de mecanismo, nem no que o JS
  // escreve nem no que a markup da aba traz pronto.
  const ini = RAW.indexOf('id="tab-expectativas"'), fim = RAW.indexOf('</main>', ini);
  const estatico = RAW.slice(ini, fim).replace(/<!--[\s\S]*?-->/g, ' ').replace(/<[^>]*>/g, ' ');
  const escrito = ['ej-lead', 'ej-cap-hoje', 'ej-lead-reu', 'ej-cap-reu', 'ej-lead-hz', 'ej-cap-hz']
    .map((id) => doc._els[id].innerHTML).join(' ').replace(/<[^>]*>/g, ' ');
  const tudo = estatico + ' ' + escrito;
  ['RMSE', 'erro médio', 'acerto', 'acertou', 'acurácia', 'previsão', 'prevê', 'backtest',
   'mínimos quadrados', 'payload', 'br_di_grade', 'expc_focus', 'base_calculo', 'j0', 'lstsq'].forEach((t) => {
    ok(tudo.indexOf(t) < 0, 'a aba nao usa "' + t + '"');
  });

  // Sintetico: os dois ramos que o dado de hoje nao exercita. (a) Uma semana em que a
  // pesquisa saiu na terca, ANTES da reuniao de quarta, e o pregao na sexta, DEPOIS dela: para
  // a pesquisa a 1a a frente ainda e a de quarta, para a curva ja e a seguinte, e medir a
  // distancia ali compararia duas reunioes diferentes. (b) Uma semana sem pesquisa no meio:
  // "3 semanas antes" e por data, e contar posicoes cairia uma semana antes.
  const Xreal = MP.D.expectativas;
  const bl = (m) => ({i0: 0, m: m, b1: m.map(() => null), lo: m, hi: m, sd: m.map(() => 0), n: m.map(() => 1)});
  MP.D.expectativas = {
    reunioes: [{d: '2027-01-20', est: false, nro: 1, selic: null, rot: 'R1/2027'},
               {d: '2027-03-17', est: false, nro: 2, selic: null, rot: 'R2/2027'}],
    focus: {datas: ['2027-01-12', '2027-01-19'], vig: [14, 14], j0: [0, 0],
            por_reuniao: {'0': bl([13.75, 13.75]), '1': bl([13.5, 13.5])}},
    di: {datas: ['2027-01-15', '2027-01-22'], vig: [14, 13.75], spread: [0.1, 0.1], j0: [0, 1],
         por_reuniao: {'0': {i0: 0, v: [13.7]}, '1': {i0: 0, v: [13.55, 13.52]}}},
  };
  const Gs = MP.ejGap(1);
  ok(Gs.dates.length === 1 && Gs.dates[0] === '2027-01-12',
     'sintetico: a semana em que as duas ja olham reunioes diferentes fica fora da distancia', JSON.stringify(Gs.dates));
  MP.D.expectativas = {reunioes: [], di: null,
    focus: {datas: ['2027-01-01', '2027-01-08', '2027-01-22', '2027-01-29'], vig: [14, 14, 14, 14], j0: [0, 0, 0, 0], por_reuniao: {}}};
  ok(MP.ejSemanaAtras('focus', 3) === 1, 'sintetico: com uma semana faltando, "3 semanas antes" cai na data certa, nao 3 posicoes atras',
     String(MP.ejSemanaAtras('focus', 3)));
  MP.D.expectativas = Xreal;

  // Sintetico: cada fonte degrada sozinha.
  const Xsalvo = MP.D.expectativas;
  MP.D.expectativas = Object.assign({}, Xsalvo, {di: null});
  let _e2 = null;
  try { MP.renderEjHoje(); MP.renderEjHojeTextos(); MP.renderEjHz(); MP.renderEjHzTextos(); } catch (e) { _e2 = e; }
  ok(!_e2, 'sintetico: sem a curva, a aba ainda desenha', _e2 && String(_e2));
  ok(doc._els['ej-lead'].innerHTML.indexOf('precifica') < 0 && doc._els['ej-lead'].innerHTML.indexOf('espera <b>') >= 0,
     'sintetico: e a chamada fala so da pesquisa');
  MP.D.expectativas = Object.assign({}, Xsalvo, {focus: null, di: null});
  MP.renderEjHojeTextos();
  ok(doc._els['ej-lead'].innerHTML.indexOf('Sem dado') === 0, 'sintetico: sem as duas, diz que nao ha dado');
  MP.D.expectativas = Xsalvo;
  MP.renderEjHoje(); MP.renderEjHojeTextos(); MP.renderEjHz(); MP.renderEjHzTextos();
}

console.log('\n37. Aba Projecoes: o caminho que cada Relatorio projetou, e um trimestre edicao a edicao');
// Pedido de 2026-09-25: acompanhar a tabela 2.2.1 do RPM -- a projecao de cada trimestre -- de
// uma edicao para a seguinte. O que nenhuma excecao denunciaria: uma edicao comparada com a
// errada (a revisao da tabela e contra a IMEDIATAMENTE anterior), o realizado desenhado como se
// fosse projecao, o horizonte relevante no trimestre errado, e as frases, todas derivadas --
// entao cada numero delas e refeito aqui, do payload.
{
  const CM = (MP.D.projecoes || {}).caminhos || {};
  const E = (CM.edicoes || []).filter((e) => e.series.ipca);
  const triDe = (iso) => parseInt(iso.slice(0, 4), 10) * 4 + Math.floor((parseInt(iso.slice(5, 7), 10) - 1) / 3);
  const edLbl = (v) => ['jan', 'fev', 'mar', 'abr', 'mai', 'jun', 'jul', 'ago', 'set', 'out', 'nov', 'dez'][parseInt(v.slice(5, 7), 10) - 1] + '/' + v.slice(0, 4);
  const tri = (iso) => iso.slice(0, 4) + 'T' + (Math.floor((parseInt(iso.slice(5, 7), 10) - 1) / 3) + 1);
  const val = (e, ind, d) => { const s = e.series[ind]; if (!s) return null; const i = s.dates.indexOf(d); return i >= 0 ? s.values[i] : null; };
  const pct = (v) => MP.fmtBR(v, Math.abs(v * 10 - Math.round(v * 10)) > 1e-6 ? 2 : 1);

  ok(E.length > 90, 'o payload traz o caminho de toda edicao desde 1999', String(E.length));
  ok(E.every((e, i) => i === 0 || E[i - 1].vintage < e.vintage), 'edicoes em ordem cronologica');
  ok(E.every((e) => [3, 6, 9, 12].indexOf(parseInt(e.vintage.slice(5, 7), 10)) >= 0), 'toda edicao e de mar/jun/set/dez');
  // Contiguo e comecando no trimestre da propria edicao (ou no seguinte, a de set/1999): o
  // realizado nao pode estar dentro do caminho, que e o que a nota diz.
  ok(E.every((e) => Object.values(e.series).every((s) =>
       s.dates.every((d, i) => i === 0 || triDe(d) - triDe(s.dates[i - 1]) === 1))),
     'todo caminho e contiguo, trimestre a trimestre');
  ok(E.every((e) => Object.values(e.series).every((s) => {
       const d0 = triDe(s.dates[0]) - triDe(e.vintage); return d0 >= 0 && d0 <= 1; })),
     'e comeca no trimestre em que a edicao saiu -- sem trimestre ja fechado dentro');
  // O horizonte relevante e seis trimestres a frente do trimestre da reuniao, que e o da edicao.
  const comHr = E.filter((e) => e.hr);
  ok(comHr.length > 80 && comHr.every((e) => triDe(e.hr) - triDe(e.vintage) === 6 && e.series.ipca.dates.indexOf(e.hr) >= 0),
     'o horizonte relevante de cada edicao esta seis trimestres a frente e dentro do caminho', String(comHr.length));
  const L = E.filter((e) => e.series.ipca_livres), A = E.filter((e) => e.series.ipca_administrados);
  const iLiv = E.indexOf(L[0]);
  ok(L.length && L.length === E.length - iLiv && A.length === L.length && L[0].vintage === '2024-09-26',
     'livres e administrados trimestrais desde set/2024, em toda edicao dali em diante',
     L.length ? L[0].vintage + ' / ' + L.length : '-');
  // Pedido de 2026-09-25 (segunda rodada): as tres edicoes que so publicaram juros constantes
  // entram com esse cenario, em cor propria, em vez de ficar de fora.
  const CTE = E.filter((e) => e.cenario === 'juros_constante');
  ok((CM.sem_cenario || []).length === 3 && JSON.stringify(CTE.map((e) => e.vintage)) === JSON.stringify(CM.sem_cenario)
     && E.every((e) => e.cenario === 'juros_constante' || e.cenario === 'juros_esperado'),
     'as edicoes so com juros constantes entram, marcadas, e sao as listadas', JSON.stringify(CM.sem_cenario));
  const R = (CM.realizado || {}).ipca || {dates: [], values: []};
  ok(R.dates.length > 100 && R.dates.every((d, i) => i === 0 || triDe(d) - triDe(R.dates[i - 1]) === 1),
     'o realizado e trimestral e sem buraco', String(R.dates.length));

  // ── O grafico do caminho ──
  const chCm = doc.getElementById('chart-pj-cm');
  const cardCm = new El('div'); cardCm.classList.add('chart-card');
  const paiCm = new El('div'); paiCm.appendChild(cardCm); cardCm.appendChild(chCm); chCm._closest = cardCm;
  chamadas.length = 0;
  MP.PJ.cmIndice = 'ipca';
  let _e = null;
  try { MP.renderPjCaminhos(); } catch (e) { _e = e; }
  ok(!_e, 'renderPjCaminhos executa', _e && String(_e.stack || _e));
  const rc = chamadas.filter((c) => c.tipo === 'react' && c.divId === 'chart-pj-cm').pop();
  ok(!!rc, 'o grafico do caminho foi plotado');
  const n = E.length, ult = E[n - 1], ant = E[n - 2];
  if (rc) {
    ok(rc.traces.length === n + 2, 'uma linha por edicao, mais o realizado e a meta', rc.traces.length + ' vs ' + (n + 2));
    ok(E.every((e, k) => JSON.stringify(rc.traces[k].x) === JSON.stringify(e.series.ipca.dates)
                       && JSON.stringify(rc.traces[k].y) === JSON.stringify(e.series.ipca.values)),
       'cada linha e o caminho da edicao, sem transformacao');
    ok(rc.traces[n - 1].line.color === '#1F2853' && rc.traces[n - 2].line.color === '#02739B'
       && rc.traces[n - 1].line.width > rc.traces[n - 2].line.width && rc.traces[n - 2].line.width > rc.traces[0].line.width,
       'a mais recente em azul e grossa, a anterior em azul-claro, o resto na rampa');
    const antes = rc.traces.slice(0, n - 2).filter((t, k) => E[k].cenario !== 'juros_constante');
    ok(antes.length === n - 2 - CTE.length && antes.every((t) => t.legendgroup === 'antes') && antes.filter((t) => t.showlegend).length === 1,
       'as anteriores num grupo de legenda so, com uma entrada');
    // As de juros constantes: outro grupo, outra cor (fora da rampa), uma entrada que diz quais sao.
    const tc = CTE.map((e) => rc.traces[E.indexOf(e)]);
    ok(tc.every((t) => t.legendgroup === 'cte' && t.line.color === MP.PJ_CTE_COR) && tc.filter((t) => t.showlegend).length === 1
       && tc.find((t) => t.showlegend).name.indexOf('mar/2002, dez/2002 e mar/2003') >= 0,
       'as de juros constantes num grupo proprio, em verde, com a legenda nomeando as tres',
       tc.map((t) => t.legendgroup + '/' + t.line.color).join());
    ok(rc.traces.filter((t, k) => k < n && E[k].cenario !== 'juros_constante').every((t) => t.line.color !== MP.PJ_CTE_COR),
       'e nenhuma outra edicao usa essa cor');
    // Nenhuma revisao atravessa a troca de cenario: a edicao de jun/2002 vem logo depois da de
    // mar/2002, que e de juros constantes.
    const kJun02 = E.findIndex((e) => e.vintage.slice(0, 7) === '2002-06');
    const cJun02 = rc.traces[kJun02].customdata;
    ok(E[kJun02 - 1].cenario === 'juros_constante' && cJun02.every((c) => c.indexOf('revisão desde') < 0 && c.indexOf('outro cenário de juros') >= 0),
       'a edicao seguinte a uma de juros constantes nao mede revisao contra ela, e diz por que', cJun02[0]);
    const kDez02 = E.findIndex((e) => e.vintage.slice(0, 7) === '2002-12'), kMar03 = kDez02 + 1;
    ok(rc.traces[kMar03].customdata.some((c) => c.indexOf('revisão desde dez/2002') >= 0),
       'mas duas de juros constantes seguidas medem revisao entre si');
    const iHr = ult.series.ipca.dates.indexOf(ult.hr);
    ok(Array.isArray(rc.traces[n - 1].marker.size) && rc.traces[n - 1].marker.size[iHr] > 0
       && rc.traces[n - 1].marker.size.filter((s) => s > 0).length === 1,
       'o losango cai so no horizonte relevante da mais recente', ult.hr);
    // A revisao do hover e contra a edicao IMEDIATAMENTE anterior, que e a regra da tabela do RPM.
    const comum = ult.series.ipca.dates.find((d) => val(ant, 'ipca', d) != null);
    const iC = ult.series.ipca.dates.indexOf(comum);
    const esperado = 'revisão desde ' + edLbl(ant.vintage) + ': ';
    ok(rc.traces[n - 1].customdata[iC].indexOf(esperado) >= 0,
       'o hover do trimestre comum diz a revisao desde a edicao anterior', rc.traces[n - 1].customdata[iC]);
    const novo = ult.series.ipca.dates[ult.series.ipca.dates.length - 1];
    ok(val(ant, 'ipca', novo) == null && rc.traces[n - 1].customdata[ult.series.ipca.dates.length - 1].indexOf('não projetava') >= 0,
       'e o trimestre novo diz que a anterior nao o projetava, em vez de revisao zero');
    const tr = rc.traces[n], tm = rc.traces[n + 1];
    ok(tr.line.color === '#BB9B1D' && tr.x.every((d) => R.dates.indexOf(d) >= 0),
       'o realizado sai em dourado, com os trimestres do payload');
    ok(tm.line.dash === 'dash' && tm.line.shape === 'hv' && tm.y.every((v) => v > 0), 'a meta tracejada, em degrau por ano');
    ok(rc.layout.hovermode === 'closest', "hovermode 'closest'");
    const W = MP._chartXRange['chart-pj-cm'];
    const datas = [...new Set([].concat(...rc.traces.map((t) => t.x)))].sort();
    const d5 = new Date(Date.parse(datas[datas.length - 1])); d5.setUTCFullYear(d5.getUTCFullYear() - 5);
    ok(!!W && W[0] >= d5.toISOString().slice(0, 10) && W[0] < datas[datas.length - 1],
       'a janela abre nos ultimos cinco anos', JSON.stringify(W));
  }
  const barCm = paiCm.children.find((c) => c.classList.contains('period-ctrl-bar'));
  ok(barCm && barCm._roles.from.children.every((o) => /^\d{4}T[1-4]$/.test(o.textContent)),
     'a regua rotula em trimestre');

  // ── A prosa do caminho: cada numero refeito aqui ──
  MP.renderPjCaminhosTextos();
  const revs = ult.series.ipca.dates.filter((d) => val(ant, 'ipca', d) != null)
    .map((d) => ({d, de: val(ant, 'ipca', d), para: val(ult, 'ipca', d), r: Math.round((val(ult, 'ipca', d) - val(ant, 'ipca', d)) * 1e6) / 1e6}));
  const sobe = revs.filter((x) => x.r > 0).length, desce = revs.filter((x) => x.r < 0).length;
  const maior = revs.reduce((m, x) => (!m || Math.abs(x.r) > Math.abs(m.r)) ? x : m, null);
  const lead = doc._els['pj-cm-lead'].innerHTML;
  ok(lead.indexOf('<b>' + n + '</b> edições, de ' + edLbl(E[0].vintage) + ' a ' + edLbl(ult.vintage)) >= 0,
     'a chamada conta as edicoes e diz de quando a quando', lead.slice(0, 260));
  ok(lead.indexOf('dos <b>' + revs.length + '</b> trimestres que as duas projetam') >= 0,
     'e quantos trimestres as duas ultimas tem em comum', String(revs.length));
  ok((!sobe || lead.indexOf(sobe === 1 ? '1 subiu' : sobe + ' subiram') >= 0)
     && (!desce || lead.indexOf(desce === 1 ? '1 caiu' : desce + ' caíram') >= 0),
     'e quantos subiram e cairam', sobe + '/' + desce);
  ok(!maior.r || lead.indexOf('a maior revisão foi em ' + tri(maior.d) + ', de ' + pct(maior.de) + '% para ' + pct(maior.para) + '%') >= 0,
     'e a maior revisao, refeita aqui', maior && tri(maior.d));
  ok(lead.indexOf(tri(ult.hr) + ', a projeção é <b>' + pct(val(ult, 'ipca', ult.hr)) + '%</b>') >= 0,
     'e a projecao do horizonte relevante da mais recente');
  ok(doc._els['pj-ap-cm-liv'].innerHTML === 'set/2024', 'a nota diz onde comeca o caminho de livres e administrados');
  const tams = E.map((e) => e.series.ipca.dates.length);
  ok(doc._els['pj-ap-cm-ntri'].innerHTML === Math.min(...tams) + ' a ' + Math.max(...tams),
     'e quantos trimestres cada edicao publica, medido', doc._els['pj-ap-cm-ntri'].innerHTML);
  ok(doc._els['pj-ap-cm-sem'].innerHTML.indexOf('mar/2002, dez/2002 e mar/2003') >= 0,
     'e nomeia as edicoes que ficaram de fora', doc._els['pj-ap-cm-sem'].innerHTML);

  // ── A tabela recolhivel ──
  MP.renderPjCaminhosTabela();
  const tab = doc.getElementById('pj-cm-tabela');
  const trs = tab.querySelectorAll('tbody tr');
  const nTab = Math.min(8, n);
  ok(trs.length === nTab + 1, 'uma linha por edicao das ultimas oito, mais o realizado', String(trs.length));
  // O stub nao guarda texto de no, entao o conteudo das celulas e lido do HTML que o JS escreveu
  // -- lido dos nos, toda celula sairia vazia e a conferencia de cor passaria por vacuidade.
  const htmlTab = tab.innerHTML;
  const linhas = htmlTab.split('<tr').slice(2);            // [0] vazio, [1] cabecalho
  const celulas = (l) => [...l.matchAll(/<td class="([^"]*)"[^>]*>([^<]*)<\/td>/g)].map((x) => ({cls: x[1], txt: x[2]}));
  ok(celulas(linhas[0])[0].txt === edLbl(ult.vintage) && /^ class="pj-cm-real"/.test(linhas[linhas.length - 1]),
     'da mais recente para a mais antiga, e o realizado por ultimo', celulas(linhas[0])[0].txt);
  const cab = [...htmlTab.split('</thead>')[0].matchAll(/<th>(\d{4}T[1-4])<\/th>/g)].map((x) => x[1]);
  ok(cab.length >= 11, 'o cabecalho lista os trimestres', String(cab.length));
  // Cor contra a edicao de baixo, conferida celula a celula na primeira linha.
  const tds = celulas(linhas[0]).slice(1);
  let conferidas = 0;
  const corOk = tds.length === cab.length && tds.every((td, j) => {
    const d = cab[j].slice(0, 4) + '-' + String((parseInt(cab[j].slice(5), 10) - 1) * 3 + 1).padStart(2, '0') + '-01';
    const v = val(ult, 'ipca', d), va = val(ant, 'ipca', d);
    if (v == null) return td.txt === '';
    conferidas++;
    const up = td.cls.indexOf('pj-cm-up') >= 0, dn = td.cls.indexOf('pj-cm-dn') >= 0;
    if (td.txt !== pct(v)) return false;
    if (va == null || Math.abs(v - va) < 1e-9) return !up && !dn;
    return v > va ? up && !dn : dn && !up;
  });
  ok(corOk && conferidas === ult.series.ipca.dates.length,
     'o numero e a cor de cada celula seguem a edicao e o sinal da revisao contra a de baixo', String(conferidas));
  ok(tds.filter((td) => td.cls.indexOf('pj-cm-hr') >= 0).length === 1, 'e o horizonte relevante vem marcado uma vez na linha');
  // A classe so pinta se a regra vencer `.hier-table td.col-value`, que tem a mesma especificidade
  // e vem depois no CSS -- o Chrome mostrou a tabela inteira preta com a regra sem `col-value`.
  ok(/\.hier-table td\.col-value\.pj-cm-up\s*\{/.test(RAW) && /\.hier-table td\.col-value\.pj-cm-dn\s*\{/.test(RAW),
     'e a regra de cor e especifica o bastante para vencer a cor padrao da celula');
  ok(doc._els['pj-cm-sum'].textContent === nTab + ' de ' + n + ' edições · IPCA', 'o summary diz o que ha dentro',
     doc._els['pj-cm-sum'].textContent);

  // ── Trocar o indice ──
  const pillCm = (t) => doc.getElementById('pj-cm-indice').children.find((b) => b.textContent === t);
  ok(['IPCA', 'IPCA livres', 'IPCA administrados'].every((t) => !!pillCm(t)), 'as tres pills de indice');
  pillCm('IPCA livres').fire('click');
  const rL = chamadas.filter((c) => c.tipo === 'react' && c.divId === 'chart-pj-cm').pop();
  ok(rL && rL.traces.length === L.length + 2 && rL.traces[L.length - 1].y.join() === L[L.length - 1].series.ipca_livres.values.join(),
     'livres: uma linha por edicao que publica livres, com os numeros de livres');
  ok(doc._els['pj-cm-lead'].innerHTML.indexOf('caminho trimestral dos preços livres desde a edição de set/2024') >= 0,
     'e a chamada diz desde quando existe', doc._els['pj-cm-lead'].innerHTML.slice(-160));
  // O realizado de livres existe desde 1999, e o caminho so desde 2024: sem o recorte, a regua
  // "Tudo" abriria 25 anos de linha dourada sozinha antes da primeira projecao.
  const rLx = rL ? rL.traces[L.length].x : [];
  ok(rLx.length && triDe(rLx[0]) === triDe(L[0].series.ipca_livres.dates[0]) - 8,
     'e o realizado de livres comeca dois anos antes da primeira projecao, nao em 1999', rLx[0]);
  pillCm('IPCA').fire('click');

  // ── O seletor de edicoes (caixas de marcar, pedido de 2026-09-25) ──
  MP.PJ.cmEds = []; MP.PJ.cmSlot = {}; MP.pjCmSetupEd();
  const panEd = doc.getElementById('pj-cm-ed-panel'), btnEd = doc.getElementById('pj-cm-ed-btn');
  const itens = panEd.children.filter((c) => c.tag === 'label');
  const caixa = (v) => itens.find((l) => l.children[0].value === v);
  const cbDe = (v) => caixa(v).children[0];
  const rotDe = (v) => caixa(v).children[2].textContent;
  ok(itens.length === n + 1 && itens[0].children[0].value === 'todas' && /^Todas as edições/.test(rotDe('todas'))
     && itens[1].children[0].value === ult.vintage && itens[n].children[0].value === E[0].vintage
     && itens.every((l) => l.children[0].type === 'checkbox'),
     'a lista tem "Todas as edicoes" e uma caixa por edicao, da mais recente para tras', String(itens.length));
  ok(itens.filter((l) => /só juros constantes/.test(l.children[2].textContent)).length === CTE.length,
     'e marca as de juros constantes');
  ok(cbDe('todas').checked && cbDe(ult.vintage).checked && cbDe(ult.vintage).disabled
     && itens.slice(2).every((l) => !l.children[0].checked && !l.children[0].disabled)
     && btnEd.textContent === 'Todas as edições · ' + n,
     'no comeco: "Todas" marcada, a mais recente marcada e travada, nenhuma outra', btnEd.textContent);
  const ultCm = () => chamadas.filter((c) => c.tipo === 'react' && c.divId === 'chart-pj-cm').pop();
  const marcar = (v, on) => { const cb = cbDe(v); cb.checked = on; cb.fire('change'); return ultCm(); };
  const headCm = () => cardCm.children.find((c) => c.className.indexOf('chart-head') === 0);
  const e10 = E.find((e) => e.vintage.slice(0, 7) === '2010-06');
  const e15 = E.find((e) => e.vintage.slice(0, 7) === '2015-06');
  const e20 = E.find((e) => e.vintage.slice(0, 7) === '2020-06');
  const rs = marcar(e10.vintage, true);
  ok(rs && rs.traces.length === 4, 'uma edicao marcada: ela, a mais recente, o realizado e a meta', rs && rs.traces.length);
  if (rs) {
    ok(rs.traces[0].y.join() === e10.series.ipca.values.join() && rs.traces[0].line.color === MP.PJ_SEL_CORES[0]
       && rs.traces[1].y.join() === ult.series.ipca.values.join() && rs.traces[1].line.color === '#1F2853'
       && rs.traces[1].line.width > rs.traces[0].line.width,
       'a marcada na primeira cor e a mais recente segue em azul forte e mais grossa');
    const iH = e10.series.ipca.dates.indexOf(e10.hr);
    ok(rs.traces[0].marker && rs.traces[0].marker.size[iH] > 0, 'e a marcada ganha o losango no horizonte relevante dela', e10.hr);
    const W = MP._chartXRange['chart-pj-cm'];
    ok(W && W[0] <= e10.series.ipca.dates[0] && W[1] > ult.series.ipca.dates[ult.series.ipca.dates.length - 1],
       'e a janela abre cobrindo a marcada e a mais recente inteiras', JSON.stringify(W));
    ok(triDe(rs.traces[2].x[0]) === triDe(e10.series.ipca.dates[0]) - 8, 'e o realizado comeca dois anos antes da marcada', rs.traces[2].x[0]);
    const vr = R.values[R.dates.indexOf(e10.hr)];
    const ld = doc._els['pj-cm-lead'].innerHTML;
    ok(ld.indexOf('Selecionada, a edição de jun/2010 projetou de ' + tri(e10.series.ipca.dates[0])) >= 0
       && ld.indexOf('No horizonte relevante dela, ' + tri(e10.hr) + ', a projeção era <b>' + pct(val(e10, 'ipca', e10.hr)) + '%</b>; o realizado foi <b>' + MP.fmtBR(vr, 2) + '%</b>') >= 0,
       'e a chamada diz o que ela projetou para o horizonte relevante e o que aconteceu, refeito aqui', ld.slice(-260));
    ok(doc._els['pj-cm-cap'].innerHTML.indexOf('Azul-claro: a edição selecionada, de jun/2010') >= 0, 'e a legenda escrita acompanha');
    const hd = headCm();
    ok(hd && hd.children[0].textContent.indexOf('o Caminho da Edição de jun/2010 do RPM') >= 0, 'e o titulo nomeia a edicao',
       hd && hd.children[0].textContent);
    ok(!cbDe('todas').checked && cbDe(e10.vintage).checked && btnEd.textContent === 'jun/2010'
       && caixa(e10.vintage).children[1].style.background === MP.PJ_SEL_CORES[0],
       'a lista desmarca "Todas", marca a edicao com a cor dela, e o botao a nomeia', btnEd.textContent);
  }
  // Mais duas: cada uma com a sua cor, na ordem em que foram marcadas.
  marcar(e20.vintage, true);
  const r3 = marcar(e15.vintage, true);
  ok(r3 && r3.traces.length === 6 && [e10, e15, e20, ult].every((e, i) => r3.traces[i].y.join() === e.series.ipca.values.join()),
     'tres marcadas: elas em ordem cronologica, a mais recente, o realizado e a meta', r3 && r3.traces.length);
  if (r3) {
    ok(r3.traces[0].line.color === MP.PJ_SEL_CORES[0] && r3.traces[1].line.color === MP.PJ_SEL_CORES[2]
       && r3.traces[2].line.color === MP.PJ_SEL_CORES[1],
       'a cor e a da ordem em que foram marcadas, nao a da posicao no grafico',
       r3.traces.slice(0, 3).map((t) => t.line.color).join());
    ok([0, 1, 2].every((i) => r3.traces[i].showlegend !== false && !r3.traces[i].legendgroup),
       'e cada uma com a sua entrada na legenda');
    const ld3 = doc._els['pj-cm-lead'].innerHTML;
    ok(ld3.indexOf('Das 3 selecionadas') >= 0 && [e10, e15, e20].every((e) => {
         const a = e.hr && e.series.ipca.dates.indexOf(e.hr) >= 0 ? e.hr : e.series.ipca.dates[e.series.ipca.dates.length - 1];
         const v = R.values[R.dates.indexOf(a)];
         return ld3.indexOf('a de ' + edLbl(e.vintage) + ' projetou <b>' + pct(val(e, 'ipca', a)) + '%</b> para ' + tri(a)) >= 0
           && ld3.indexOf(', e o realizado foi <b>' + MP.fmtBR(v, 2) + '%</b>') >= 0;
       }),
       'e a chamada da, para cada uma, a projecao do horizonte relevante e o realizado, refeitos aqui', ld3.slice(-420));
    ok(doc._els['pj-cm-cap'].innerHTML.indexOf('Coloridas: as 3 edições selecionadas') >= 0, 'e a legenda escrita fala das tres');
    ok(ld3.indexOf('em verde') < 0 && ld3.indexOf('mar/2003 só publicaram o cenário de juros constantes') >= 0,
       'e a chamada nao promete o verde, que e so da vista com todas');
    const hd3 = headCm();
    ok(hd3 && hd3.children[0].textContent.indexOf('o Caminho de 3 Edições do RPM') >= 0
       && hd3.children[1].textContent.indexOf('edições de jun/2010, jun/2015 e jun/2020') >= 0,
       'e titulo e subtitulo acompanham', hd3 && (hd3.children[0].textContent + ' | ' + hd3.children[1].textContent));
    ok(btnEd.textContent === '3 edições marcadas', 'e o botao conta', btnEd.textContent);
  }
  // Desmarcar a primeira nao troca a cor das outras; a proxima marcada fica com a cor livre.
  const rD = marcar(e10.vintage, false);
  ok(rD && rD.traces[0].line.color === MP.PJ_SEL_CORES[2] && rD.traces[1].line.color === MP.PJ_SEL_CORES[1],
     'desmarcar uma nao troca a cor das que ficam', rD && rD.traces.slice(0, 2).map((t) => t.line.color).join());
  const rD2 = marcar(e10.vintage, true);
  ok(rD2 && rD2.traces[0].line.color === MP.PJ_SEL_CORES[0], 'e a proxima marcada fica com a cor que vagou');
  // Uma de juros constantes marcada: pontilhada, e o nome diz o cenario.
  const eCte = CTE[1];
  const rsc = marcar(eCte.vintage, true);
  const tc1 = rsc && rsc.traces.find((t) => t.y.join() === eCte.series.ipca.values.join());
  ok(tc1 && tc1.line.dash === 'dot' && /juros constantes/.test(tc1.name) && rsc.traces.filter((t) => t.line && t.line.dash === 'dot').length === 1,
     'uma de juros constantes marcada sai pontilhada, e o nome diz o cenario', tc1 && tc1.name);
  ok(doc._els['pj-cm-cap'].innerHTML.indexOf('pontilhada, a de juros constantes') >= 0, 'e a legenda escrita diz o que e o pontilhado');
  // O teto: as cores disponiveis. Cheio, as caixas que sobram travam, com o motivo.
  const livres = E.slice(0, n - 1).filter((e) => MP.PJ.cmEds.indexOf(e.vintage) < 0);
  livres.slice(0, MP.PJ_SEL_CORES.length - MP.PJ.cmEds.length).forEach((e) => marcar(e.vintage, true));
  const sobra = livres[livres.length - 1];
  ok(MP.PJ.cmEds.length === MP.PJ_SEL_CORES.length && cbDe(sobra.vintage).disabled && /Cabem até 9/.test(caixa(sobra.vintage).title),
     'com ' + MP.PJ_SEL_CORES.length + ' marcadas as outras caixas travam, com o motivo', caixa(sobra.vintage).title);
  const antesTeto = chamadas.length;
  marcar(sobra.vintage, true);
  ok(MP.PJ.cmEds.length === MP.PJ_SEL_CORES.length && !cbDe(sobra.vintage).checked && chamadas.length === antesTeto,
     'e forcar uma a mais nao muda nada');
  ok(new Set(Object.values(MP.PJ.cmSlot)).size === MP.PJ_SEL_CORES.length, 'e as ' + MP.PJ_SEL_CORES.length + ' tem cores diferentes');
  // "Todas as edicoes" desmarca tudo e volta ao conjunto, na janela de cinco anos.
  const rt = marcar('todas', true);
  const Wt = MP._chartXRange['chart-pj-cm'];
  const dt = [...new Set([].concat(...rt.traces.map((t) => t.x)))].sort();
  const d5t = new Date(Date.parse(dt[dt.length - 1])); d5t.setUTCFullYear(d5t.getUTCFullYear() - 5);
  ok(rt.traces.length === n + 2 && Wt && Wt[0] >= d5t.toISOString().slice(0, 10) && MP.PJ.cmEds.length === 0
     && itens.slice(2).every((l) => !l.children[0].checked && !l.children[0].disabled),
     '"Todas" volta as n edicoes, na janela de cinco anos, e destrava as caixas', JSON.stringify(Wt));
  const antesTodas = chamadas.length;
  marcar('todas', false);
  ok(cbDe('todas').checked && chamadas.length === antesTodas, 'desmarcar "Todas" sozinha nao faz nada');
  // Livres nao tem as edicoes de 2010 e 2015: saem da marcacao; a de 2024 em diante fica.
  const eLiv = L[L.length - 2];
  marcar(e10.vintage, true); marcar(eLiv.vintage, true);
  pillCm('IPCA livres').fire('click');
  const rLv = ultCm();
  ok(JSON.stringify(MP.PJ.cmEds) === JSON.stringify([eLiv.vintage]) && panEd.children.filter((c) => c.tag === 'label').length === L.length + 1
     && rLv.traces[0].y.join() === eLiv.series.ipca_livres.values.join(),
     'trocar para um indice sem uma das marcadas tira so ela, e a outra segue no grafico', JSON.stringify(MP.PJ.cmEds));
  pillCm('IPCA').fire('click');
  marcar('todas', true);
  ok(MP.PJ.cmEds.length === 0, 'e o seletor volta a "Todas" para o resto do teste');

  // ── Um trimestre, edicao a edicao ──
  const chVt = doc.getElementById('chart-pj-vt');
  const cardVt = new El('div'); cardVt.classList.add('chart-card');
  const paiVt = new El('div'); paiVt.appendChild(cardVt); cardVt.appendChild(chVt); chVt._closest = cardVt;
  MP.PJ.vtIndice = 'ipca';
  MP.PJ.vtTri = null;
  MP.pjVtSetupTri();
  ok(MP.PJ.vtTri === ult.hr, 'o seletor de trimestre abre no horizonte relevante da mais recente', MP.PJ.vtTri);
  const sel = doc.getElementById('pj-vt-tri');
  const tris = [...new Set([].concat(...E.map((e) => e.series.ipca.dates)))].sort().reverse();
  ok(sel.children.length === tris.length && sel.children[0].value === tris[0],
     'e lista todo trimestre que alguma edicao projetou, do mais distante para tras', String(sel.children.length));
  const pontos = (d) => E.filter((e) => val(e, 'ipca', d) != null);
  const conferir = (d, rotulo) => {
    chamadas.length = 0;
    MP.renderPjVertice(); MP.renderPjVerticeTextos();
    const r = chamadas.filter((c) => c.tipo === 'react' && c.divId === 'chart-pj-vt').pop();
    const P_ = pontos(d);
    const Pe = P_.filter((e) => e.cenario !== 'juros_constante'), Pc = P_.filter((e) => e.cenario === 'juros_constante');
    ok(r && JSON.stringify(r.traces[0].x) === JSON.stringify(Pe.map((e) => e.vintage))
       && JSON.stringify(r.traces[0].y) === JSON.stringify(Pe.map((e) => val(e, 'ipca', d))),
       rotulo + ': um ponto por edicao que projetou o trimestre, na data da edicao');
    const tCte = r && r.traces.find((t) => t.name === 'Só juros constantes publicados');
    ok(Pc.length ? (tCte && tCte.mode.indexOf('lines') < 0 && JSON.stringify(tCte.x) === JSON.stringify(Pc.map((e) => e.vintage))
                    && JSON.stringify(tCte.y) === JSON.stringify(Pc.map((e) => val(e, 'ipca', d))))
                 : !tCte,
       rotulo + ': as de juros constantes sao pontos soltos, fora da linha (e so quando existem)', String(Pc.length));
    const real = R.dates.indexOf(d) >= 0 ? R.values[R.dates.indexOf(d)] : null;
    // O eixo X rotula as edicoes pelo nome que o BC usa (e nao o mes em ingles do Plotly), e o Y
    // abre com a folga minima de meio ponto do ajuste de Y -- senao 0,1 de revisao le como salto.
    ok(r && JSON.stringify(r.layout.xaxis.ticktext) === JSON.stringify(P_.map((e) => edLbl(e.vintage))),
       rotulo + ': o eixo X rotula cada edicao pelo nome dela', r && JSON.stringify(r.layout.xaxis.ticktext).slice(0, 80));
    const ys = P_.map((e) => val(e, 'ipca', d)).concat(real != null ? [real] : []);
    ok(r && r.layout.yaxis.autorange === false && r.layout.yaxis.range[0] <= Math.min(...ys) - 0.5 + 1e-9
       && r.layout.yaxis.range[1] >= Math.max(...ys) + 0.5 - 1e-9,
       rotulo + ': o Y abre com meio ponto de folga dos dois lados', r && JSON.stringify(r.layout.yaxis.range));
    const temReal = r && r.traces.some((t) => /^Realizado/.test(t.name || ''));
    ok(temReal === (real != null), rotulo + ': a regua do realizado existe se e so se o trimestre fechou');
    const lv = doc._els['pj-vt-lead'].innerHTML;
    const a0 = Pe[0], z = Pe[Pe.length - 1];
    ok(lv.indexOf('<b>' + tri(d) + '</b>') >= 0 && lv.indexOf('a de ' + edLbl(a0.vintage) + ', ') >= 0
       && lv.indexOf('<b>' + pct(val(z, 'ipca', d)) + '%</b>') >= 0,
       rotulo + ': a chamada diz a primeira edicao e o ultimo numero', lv.slice(0, 300));
    let passos = 0, muda = 0;
    for (let i = 1; i < Pe.length; i++) {
      const k = E.indexOf(Pe[i]);
      const va = val(E[k - 1], 'ipca', d);
      if (va == null || E[k - 1].cenario !== Pe[i].cenario) continue;
      passos++; if (Math.abs(val(Pe[i], 'ipca', d) - va) > 1e-9) muda++;
    }
    ok(lv.indexOf('Das ' + passos + ' passagens') >= 0 && (muda ? lv.indexOf(muda + (muda === 1 ? ' mexeu' : ' mexeram')) >= 0 : lv.indexOf('nenhuma mexeu') >= 0),
       rotulo + ': e quantas passagens mudaram o numero', passos + '/' + muda);
    ok((real != null) === (lv.indexOf('O realizado foi <b>' + (real != null ? MP.fmtBR(real, 2) : '') + '%</b>') >= 0),
       rotulo + ': o realizado so e dito quando existe');
    ok(Pc.length ? lv.indexOf(Pc.map((e) => edLbl(e.vintage)).join(', ').replace(/, ([^,]*)$/, ' e $1')) >= 0 && lv.indexOf('fora dessa conta') >= 0
                 : lv.indexOf('juros constantes') < 0,
       rotulo + ': as de juros constantes sao nomeadas a parte, e so quando existem');
    return r;
  };
  conferir(ult.hr, 'horizonte relevante');
  // Um trimestre ja fechado e muito revisto: o de dois anos atras.
  const fechado = R.dates[R.dates.length - 9];
  sel.value = fechado; sel.fire('change');
  ok(MP.PJ.vtTri === fechado, 'o seletor troca o trimestre', MP.PJ.vtTri);
  ok(!MP._chartXRange['chart-pj-vt'] || MP._chartXRange['chart-pj-vt'][0] <= pontos(fechado)[0].vintage,
     'e a janela recomeca na extensao do trimestre novo');
  conferir(fechado, 'trimestre fechado');
  // Um trimestre que edicoes de juros constantes tambem projetaram: 2003T4.
  sel.value = '2003-10-01'; sel.fire('change');
  const r03 = conferir('2003-10-01', 'trimestre com juros constantes');
  ok(r03 && r03.traces[1] && r03.traces[1].name === 'Só juros constantes publicados'
     && r03.layout.xaxis.tickvals.length === pontos('2003-10-01').length,
     'e o eixo X rotula as edicoes dos dois cenarios');
  // Livres nao tem esse trimestre: cai de volta no padrao em vez de desenhar nada.
  const velho = '2010-01-01';
  sel.value = velho; sel.fire('change');
  doc.getElementById('pj-vt-indice').children.find((b) => b.textContent === 'IPCA livres').fire('click');
  ok(MP.PJ.vtTri === ult.hr, 'um trimestre que o indice novo nao tem cai no horizonte relevante', MP.PJ.vtTri);
  doc.getElementById('pj-vt-indice').children.find((b) => b.textContent === 'IPCA').fire('click');

  // ── Sintetico: os ramos que o dado de hoje nao exercita ──
  const salvo = MP.D.projecoes.caminhos;
  const ed = (vintage, dates, values, hr) => ({vintage, nro: 1, hr: hr || null, series: {ipca: {dates, values}}});
  MP.D.projecoes.caminhos = {
    indices: ['ipca'], sem_cenario: [], meta: {'2026': 3}, ultimo_ano_meta: 2026,
    realizado: {ipca: {dates: ['2026-01-01'], values: [4.1]}},
    edicoes: [ed('2026-03-26', ['2026-01-01', '2026-04-01', '2026-07-01'], [4.0, 3.8, 3.5]),
              ed('2026-06-25', ['2026-04-01', '2026-07-01', '2026-10-01'], [3.8, 3.5, 3.2], '2027-10-01')],
  };
  MP.PJ.cmIndice = 'ipca';
  MP.renderPjCaminhosTextos();
  ok(doc._els['pj-cm-lead'].innerHTML.indexOf('dos <b>2</b> trimestres que as duas projetam, nenhum mudou.') >= 0,
     'sintetico: nada revisto vira "nenhum mudou"', doc._els['pj-cm-lead'].innerHTML);
  MP.D.projecoes.caminhos.edicoes[1].series.ipca.values = [3.9, 3.5, 3.2];
  MP.renderPjCaminhosTextos();
  ok(doc._els['pj-cm-lead'].innerHTML.indexOf('1 subiu e 1 ficou igual — a maior revisão foi em 2026T2, de 3,8% para 3,9%') >= 0,
     'sintetico: singular nos dois, e a maior revisao', doc._els['pj-cm-lead'].innerHTML);
  MP.PJ.vtTri = '2026-10-01';
  MP.renderPjVerticeTextos();
  ok(doc._els['pj-vt-lead'].innerHTML.indexOf('Só a edição de jun/2026 o projetou até agora, 2 trimestres à frente, com <b>3,2%</b>') >= 0
     && doc._els['pj-vt-lead'].innerHTML.indexOf('ainda não fechou') >= 0,
     'sintetico: um trimestre projetado por uma edicao so', doc._els['pj-vt-lead'].innerHTML);
  MP.D.projecoes.caminhos = salvo;
  MP.PJ.vtTri = null; MP.pjVtSetupTri();
  MP.renderPjCaminhos(); MP.renderPjCaminhosTextos(); MP.renderPjCaminhosTabela();
  MP.renderPjVertice(); MP.renderPjVerticeTextos();

  // ── A prosa e para quem abre a pagina ──
  const iA = RAW.indexOf('O caminho que cada Relatório projetou'), iB = RAW.indexOf('Como isto é montado', iA);
  const txt = ((iA >= 0 && iB > iA ? RAW.slice(iA, iB) : '') +
    ['pj-cm-lead', 'pj-cm-cap', 'pj-cm-nota', 'pj-vt-lead', 'pj-vt-cap', 'pj-ap-cm-sem'].map((id) => doc._els[id].innerHTML).join(' '))
    .replace(/<!--[\s\S]*?-->/g, '').replace(/<[^>]*>/g, ' ');
  ok(txt.length > 1500, 'a fatia das duas secoes foi achada', String(txt.length));
  ['payload', 'MySQL', 'pm_copom', 'juros_esperado', 'ETL', 'vintage', 'ipca_livres', 'anexo'].forEach((t) => {
    ok(txt.indexOf(t) < 0, 'a prosa das duas secoes nao usa "' + t + '"');
  });
  // Um id que o JS busca e o markup nao tem passaria por tudo acima (o stub cria qualquer id).
  const ids = new Set();
  const re = /(?:getElementById|put|wireDlToggle|setupPillGroup)\(\s*'((?:pj-cm-|pj-vt-|chart-pj-cm|chart-pj-vt|dl-chart-pj-cm|dl-chart-pj-vt|pj-ap-cm-)[\w-]*)'/g;
  let m;
  while ((m = re.exec(SRC))) ids.add(m[1]);
  ok(ids.size >= 12, 'a checagem de ids achou os alvos das duas secoes', String(ids.size));
  const falta = [...ids].filter((id) => RAW.indexOf('id="' + id + '"') < 0);
  ok(!falta.length, 'todo id que o JS das duas secoes busca existe no markup', JSON.stringify(falta));
}

console.log('\n' + (falhas ? falhas + ' FALHA(S)' : 'todos os testes passaram'));
process.exit(falhas ? 1 : 0);
