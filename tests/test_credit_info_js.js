// Testa os CARTOES DE DEFINICAO (botao "i") das 11 tabelas do Panorama de Credito,
// executando o script REAL do HTML gerado contra um DOM stub e um Plotly stub.
//
// Roda com:
//     node tests/test_credit_info_js.js
//
// Precisa de "reports/brasil/Credit.html" gerado:
//     uv run python -c "from analytics.brasil.credit.generate_report import run; run()"
//
// Por que ele existe -- os quatro modos de falha desta feature nao lancam excecao:
//
//   (a) CHAVE ORFA. Um erro de digitacao numa chave do NODE_INFO produz um botao que
//       nunca e criado: sem erro, sem buraco visivel, nada a notar. A secao 2 resolve
//       TODA entrada do mapa contra as arvores reais e exige zero orfas.
//   (b) NAMESPACE ERRADO. `saldo_livre_pj` existe na aba Saldo (estoque) e na aba
//       Impulso (contribuicao ao impulso); `porte__mpme` em tres abas. Um mapa de chave
//       nua faz uma tabela explicar a outra e o cartao abre, com o texto errado. A
//       secao 4 exige que as duas leituras da MESMA chave sejam textos diferentes.
//   (c) UNIDADE PRESA. A linha de unidade do cartao tem de vir da mesma funcao que
//       titula o eixo Y -- se ficar fixa, passa a mentir no primeiro clique do seletor
//       de Nivel/Nominal-Real/%PIB ou de Fluxo/Impulso. A secao 6 troca os seletores e
//       exige que a unidade do cartao acompanhe; a 7 fixa o caso inverso, as linhas com
//       `unit` propria (saldo de maior risco), que precisam IGNORAR a da tabela.
//   (d) ROTULO CONTAMINADO. Depois do botao, o `textContent` da celula inclui o "i".
//       Qualquer codigo que compare rotulos (teste, filtro) passa a comparar errado. A
//       secao 8 le so os nos de texto e exige o rotulo limpo.
//
// O que ele NAO substitui: confirmacao visual num browser real (posicao do cartao,
// hover, pin).

const fs = require('fs');
const path = require('path');

const HTML = path.join(__dirname, '..', 'reports', 'brasil', 'Credit.html');
if (!fs.existsSync(HTML)) {
  console.error('reports/brasil/Credit.html nao existe -- gere o relatorio primeiro:');
  console.error('  uv run python -c "from analytics.brasil.credit.generate_report import run; run()"');
  process.exit(1);
}
const CRU = fs.readFileSync(HTML, 'utf8');
const blocos = CRU.match(/<script>([\s\S]*?)<\/script>/g) || [];
if (!blocos.length) { console.error('nenhum <script> encontrado no HTML'); process.exit(1); }
const SRC = blocos[blocos.length - 1].replace(/^<script>/, '').replace(/<\/script>$/, '');

let falhas = 0;
let asserts = 0;
function ok(cond, nome, detalhe) {
  asserts++;
  if (cond) { console.log('  ok    ' + nome); }
  else { falhas++; console.log('  FALHA ' + nome + (detalhe ? '  -- ' + detalhe : '')); }
}
function secao(t) { console.log('\n' + t); }

// -- DOM stub (mesmo de tests/test_credit_fluxo_js.js) ------------------------
function El(tag) {
  this.tag = tag || 'div';
  this.children = []; this.style = {}; this.dataset = {};
  this._className = ''; this.textContent = ''; this.value = '';
  this._html = ''; this._listeners = {}; this._plotly = {};
  this.parentNode = null;
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
Object.defineProperty(El.prototype, 'className', {
  get() { return this._className; },
  set(v) {
    this._className = v;
    this.classList._set = {};
    String(v).split(/\s+/).filter(Boolean).forEach((c) => { this.classList._set[c] = true; });
  },
});
El.prototype.appendChild = function (c) { c.parentNode = this; this.children.push(c); return c; };
El.prototype.insertBefore = function (n, r) {
  n.parentNode = this;
  const i = this.children.indexOf(r);
  this.children.splice(i < 0 ? this.children.length : i, 0, n);
  return n;
};
El.prototype.removeChild = function (c) {
  const i = this.children.indexOf(c);
  if (i >= 0) this.children.splice(i, 1);
  c.parentNode = null; return c;
};
El.prototype.setAttribute = function (k, v) { (this._attrs = this._attrs || {})[k] = v; };
El.prototype.addEventListener = function (k, f) { (this._listeners[k] = this._listeners[k] || []).push(f); };
El.prototype.fire = function (k, ev) { (this._listeners[k] || []).forEach((f) => f(ev)); };
El.prototype.on = function (k, f) { (this._plotly[k] = this._plotly[k] || []).push(f); };
El.prototype.closest = function () { return this._closest || null; };
El.prototype.contains = function () { return false; };
El.prototype.matches = function () { return false; };
El.prototype.getBoundingClientRect = function () {
  return { left: 10, right: 24, top: 40, bottom: 54, width: 14, height: 14 };
};
El.prototype.querySelector = function (sel) {
  if (typeof sel === 'string' && sel.charAt(0) === '.') {
    const cls = sel.slice(1);
    const pilha = (this.children || []).slice();
    while (pilha.length) {
      const n = pilha.shift();
      if (n.classList && n.classList.contains(cls)) return n;
      pilha.push.apply(pilha, n.children || []);
    }
  }
  return null;
};
El.prototype.querySelectorAll = function () { return []; };
Object.defineProperty(El.prototype, 'innerHTML', {
  get() { return this._html; },
  set(v) {
    this._html = v;
    this.children = [];
    const re = /<(\w+)[^>]*class="([^"]*)"[^>]*>/g;
    let m;
    while ((m = re.exec(String(v))) !== null) {
      const filho = new El(m[1]);
      filho.className = m[2];
      this.appendChild(filho);
    }
  },
});

// Rotulo LIMPO da linha: so os nos de TEXTO. Filtrar por tag vira lista de excecoes que
// envelhece (hoje span.tree-toggle, span.row-n e button.info-btn) -- ver a nota em
// .claude/rules/lis-dashboards.md.
function rotuloLimpo(tdLabel) {
  return tdLabel.children.filter((c) => c.tag === '#text').map((c) => c.textContent).join('').trim();
}
function linhasDaTabela(tbody) {
  return tbody.children.map((tr) => {
    let tdLabel = null;
    tr.children.forEach((td) => { if (td.classList.contains('col-label')) tdLabel = td; });
    const botao = tdLabel ? tdLabel.children.find((c) => c.classList && c.classList.contains('info-btn')) : null;
    return { tr, tdLabel, botao, label: tdLabel ? rotuloLimpo(tdLabel) : '' };
  });
}

const SELECTS = {};
(CRU.match(/<select[^>]*id="([^"]+)"[^>]*>([\s\S]*?)<\/select>/g) || []).forEach((blk) => {
  const id = /id="([^"]+)"/.exec(blk)[1];
  const opts = [];
  const re = /<option([^>]*)>/g;
  let m;
  while ((m = re.exec(blk)) !== null) {
    const attrs = m[1] || '';
    const v = /value="([^"]*)"/.exec(attrs);
    opts.push({ value: v ? v[1] : '', disabled: false, selected: /\sselected/.test(attrs) });
  }
  SELECTS[id] = opts;
});

// Pills: lidas do HTML gerado com TODOS os data-* (freq, variant, metric, basis, source,
// horizonte). Sem isso wirePills()/wireControls() nao acham nada e o teste exercitaria so
// o estado default -- que e justamente o que ele nao precisa testar.
const PILLS = {};
(CRU.match(/<div class="pill-group" id="[^"]+">[\s\S]*?<\/div>/g) || []).forEach((blk) => {
  const id = /id="([^"]+)"/.exec(blk)[1];
  const botoes = [];
  const re = /<button([^>]*)>([\s\S]*?)<\/button>/g;
  let m;
  while ((m = re.exec(blk)) !== null) {
    const attrs = m[1] || '';
    const el = new El('button');
    const cls = /class="([^"]*)"/.exec(attrs);
    el.className = cls ? cls[1] : '';
    const reData = /data-([a-z]+)="([^"]*)"/g;
    let d;
    while ((d = reData.exec(attrs)) !== null) el.dataset[d[1]] = d[2];
    el.textContent = m[2].replace(/<[^>]*>/g, '').trim();
    botoes.push(el);
  }
  PILLS[id] = botoes;
});

const ABAS = ['saldo', 'concessao', 'impulso', 'taxa', 'inadimplencia', 'ptc', 'apendice'];
function makeDom() {
  const els = {};
  const tabBtns = ABAS.map((t) => { const b = new El('button'); b.dataset.tab = t; return b; });
  const tabPanels = ABAS.map((t) => { const p = new El('div'); p.id = 'tab-' + t; return p; });
  return {
    getElementById(id) {
      if (!els[id]) {
        const opts = SELECTS[id];
        const el = new El(opts ? 'select' : 'div');
        el.id = id;
        if (opts) {
          el.options = opts.map((o) => ({ value: o.value, disabled: o.disabled }));
          const sel = opts.find((o) => o.selected) || opts[0];
          el.value = sel ? sel.value : '';
        }
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
    createTextNode(t) { const n = new El('#text'); n.textContent = t; return n; },
    querySelector: () => null,
    querySelectorAll(sel) {
      if (sel === '.tab-btn') return tabBtns;
      if (sel === '.tab-panel') return tabPanels;
      const m = /^#([\w-]+) \.pill$/.exec(String(sel));
      if (m && PILLS[m[1]]) return PILLS[m[1]];
      return [];
    },
    addEventListener() {},
    body: new El('body'),
    documentElement: { clientWidth: 1400, clientHeight: 900 },
    _els: els,
  };
}

function makePlotly(documento, chamadas) {
  function thenable(v) { return { then(f) { f(v); return thenable(v); }, catch() { return thenable(v); } }; }
  return {
    react(divId, traces, layout) {
      chamadas.push({ tipo: 'react', divId, traces, layout });
      const el = documento.getElementById(divId);
      el.data = traces;
      el._fullLayout = JSON.parse(JSON.stringify(layout || {}));
      el._fullLayout.xaxis = el._fullLayout.xaxis || {};
      if (!el._fullLayout.xaxis.type) el._fullLayout.xaxis.type = 'date';
      return thenable(el);
    },
    newPlot(divId, traces, layout) { return this.react(divId, traces, layout); },
    relayout(divId, upd) { chamadas.push({ tipo: 'relayout', divId, upd }); return thenable(documento.getElementById(divId)); },
  };
}

// -- Execucao ------------------------------------------------------------------
const doc = makeDom();
const chamadas = [];
global.document = doc;
global.window = { scrollX: 0, scrollY: 0 };
global.Option = function (label, value) { const o = new El('option'); o.textContent = label; o.value = value; return o; };
global.Plotly = makePlotly(doc, chamadas);

const EXPORTS = [
  'D', 'NODE_INFO', 'infoOf', 'showInfo', 'attachInfo', 'hideInfo',
  'SALDO_TAB', 'CONCESSAO_TAB', 'AMPLO_TAB',
  'IMP_RECURSO_TAB', 'IMP_PORTE_TAB', 'IMP_ATIV_TAB', 'IMP_FLUXO_TAB',
  'taxaState', 'taxaYTitle', 'taxaInfoNs', 'renderTaxaTable',
  'inadState', 'inadInfoUnit', 'renderInadTable',
  'ptcState', 'ptcInfoUnit', 'ptcDesvioInfoUnit', 'renderPtcTable', 'renderPtcDesvioTable',
  'RENDERERS',
];
let R;
try {
  new Function(SRC + ';global.__R = {' + EXPORTS.join(',') + '};')();
  R = global.__R;
} catch (e) {
  console.error('erro ao executar o script do relatorio:', e.message);
  console.error(e.stack);
  process.exit(1);
}

// Renderiza todas as abas (RENDERERS.saldo ja rodou via activateTab('saldo')).
['concessao', 'impulso', 'taxa', 'inadimplencia', 'ptc'].forEach((t) => R.RENDERERS[t]());

// -- Mapa tabela -> {tbody, ns, arvore} ---------------------------------------
function arvoreDe(grupo, treeKey) {
  const g = R.D[grupo];
  return treeKey ? g.trees[treeKey] : (g.tree || g.trees);
}
const TABELAS = [
  { nome: 'Saldo', body: 'saldo-table-body', ns: ['saldo', 'modal'], tree: arvoreDe('saldo') },
  { nome: 'Crédito Ampliado', body: 'amplo-table-body', ns: ['amplo'], tree: arvoreDe('amplo_hier') },
  { nome: 'Concessão', body: 'concessao-table-body', ns: ['concessao', 'modal'], tree: arvoreDe('concessao') },
  { nome: 'Impulso — recurso', body: 'imp-recurso-table-body', ns: ['imp'], tree: arvoreDe('impulso', 'recurso') },
  { nome: 'Impulso — porte', body: 'imp-porte-table-body', ns: ['imp'], tree: arvoreDe('impulso', 'porte') },
  { nome: 'Impulso — atividade', body: 'imp-ativ-table-body', ns: ['imp'], tree: arvoreDe('impulso', 'atividade') },
  { nome: 'Impulso — fluxo', body: 'imp-fluxo-table-body', ns: ['fluxo'], tree: arvoreDe('fluxo') },
  { nome: 'Taxa média', body: 'taxa-table-body', ns: ['taxa', 'modal'], tree: R.D.taxa.taxa_media.tree },
  { nome: 'Spread', body: 'taxa-table-body', ns: ['spread', 'modal'], tree: R.D.taxa.spread.tree },
  { nome: 'Inadimplência', body: 'inad-table-body', ns: ['inad', 'modal'], tree: arvoreDe('inadimplencia') },
  { nome: 'PTC — observada', body: 'ptc-table-body', ns: ['ptc'], tree: R.D.ptc.tree },
  { nome: 'PTC — surpresa', body: 'ptc-desvio-table-body', ns: ['ptcsurp', 'ptc'], tree: R.D.ptc.tree },
];
// Abre toda a arvore: as tabelas nascem colapsadas, entao contar cobertura sobre o que
// esta na tela mediria so os nos de topo. Clica em cada seta ate nao aparecer linha nova.
function expandirTudo(bodyId) {
  for (let i = 0; i < 8; i++) {
    const antes = doc.getElementById(bodyId).children.length;
    linhasDaTabela(doc.getElementById(bodyId)).forEach((l) => {
      const seta = l.tdLabel && l.tdLabel.children.find((c) => c.classList && c.classList.contains('tree-toggle'));
      if (seta && seta.textContent === '▸') seta.fire('click');
    });
    if (doc.getElementById(bodyId).children.length === antes) break;
  }
}
function achatar(tree, out) {
  out = out || [];
  (tree || []).forEach((n) => { out.push(n); if (n.children) achatar(n.children, out); });
  return out;
}

// ── 1. O bloco existe e esta ligado ──────────────────────────────────────────
secao('1. Infraestrutura');
ok(R.NODE_INFO && Object.keys(R.NODE_INFO).length > 100,
   'NODE_INFO existe e tem mais de 100 entradas', 'n=' + Object.keys(R.NODE_INFO || {}).length);
ok(typeof R.infoOf === 'function' && typeof R.attachInfo === 'function',
   'infoOf() e attachInfo() existem');
ok(/\.info-btn\s*\{/.test(CRU) && /\.info-pop\s*\{/.test(CRU),
   'CSS .info-btn e .info-pop presentes no HTML');
ok(/\.info-btn:hover,\s*\.info-btn\.pinned/.test(CRU),
   'CSS tem o estado .pinned (clique fixa o cartao)');

// ── 2. Zero chaves orfas ─────────────────────────────────────────────────────
// Uma chave que nao existe em arvore nenhuma produz um botao que nunca nasce: sem erro,
// sem buraco visivel. Este e o unico jeito de pegar um erro de digitacao no mapa.
secao('2. Chaves orfas no NODE_INFO');
const chavesReais = new Set();
TABELAS.forEach((t) => {
  achatar(t.tree).forEach((n) => {
    t.ns.forEach((ns) => {
      chavesReais.add(ns + ':' + n.key);
      if (String(n.key).indexOf('__') >= 0) chavesReais.add(ns + ':' + String(n.key).split('__').pop());
    });
  });
});
const orfas = Object.keys(R.NODE_INFO).filter((k) => !chavesReais.has(k));
ok(orfas.length === 0, 'toda entrada do mapa resolve numa linha real', orfas.slice(0, 8).join(', '));

// ── 3. Botao existe exatamente onde ha entrada ───────────────────────────────
secao('3. O botao nasce da presenca da entrada, nunca do markup');
let totalLinhas = 0, totalBotoes = 0, divergencias = [];
TABELAS.forEach((t) => {
  // Taxa/Spread e PTC observada/surpresa compartilham corpo com estado diferente:
  // conferidos nas secoes proprias.
  if (t.nome === 'Spread' || t.nome === 'PTC — surpresa') return;
  expandirTudo(t.body);
  const linhas = linhasDaTabela(doc.getElementById(t.body));
  const nos = achatar(t.tree);
  // Casamento por POSICAO, nao por rotulo: "Outros", "Pessoa Juridica" e "Pessoa Fisica"
  // se repetem dezenas de vezes na arvore, e casar por texto conferiria a linha errada --
  // foi assim que a primeira versao deste teste acusou falso positivo. Com tudo
  // expandido, a ordem das linhas e exatamente a do achatamento da arvore.
  if (linhas.length !== nos.length) {
    divergencias.push(t.nome + ': ' + linhas.length + ' linhas para ' + nos.length + ' nos');
    return;
  }
  nos.forEach((no, i) => {
    const l = linhas[i];
    const esperado = !!R.infoOf(t.ns, no.key);
    totalLinhas++;
    if (l.botao) totalBotoes++;
    if (esperado !== !!l.botao) divergencias.push(t.nome + '/' + no.key + ' esperado=' + esperado);
  });
});
ok(divergencias.length === 0, 'botao presente exatamente onde infoOf() resolve',
   divergencias.slice(0, 6).join(' | '));
ok(totalBotoes >= 250, 'cobertura: pelo menos 250 linhas com cartao, com a arvore aberta',
   totalBotoes + ' de ' + totalLinhas + ' linhas');
ok(totalBotoes < totalLinhas, 'nem toda linha tem cartao (o icone precisa ser raro)',
   totalBotoes + '/' + totalLinhas);

// ── 4. Namespace: a mesma chave, duas tabelas, dois textos ───────────────────
// Este e o modo de falha que nada denuncia: com mapa de chave nua o cartao abre, com o
// texto da OUTRA tabela.
secao('4. Namespace da chave');
const parasColididas = [
  ['saldo_livre_pj', ['saldo', 'modal'], ['imp']],
  ['saldo_direcionado_total', ['saldo', 'modal'], ['imp']],
  ['porte__total', ['saldo', 'modal'], ['imp']],
  ['porte__mpme', ['saldo', 'modal'], ['imp']],
  ['ativ__total', ['saldo', 'modal'], ['imp']],
];
parasColididas.forEach(([k, nsA, nsB]) => {
  const a = R.infoOf(nsA, k), b = R.infoOf(nsB, k);
  ok(a && b && a.desc !== b.desc,
     'chave "' + k + '" tem leitura propria em ' + nsA[0] + ' e em ' + nsB[0],
     a && b ? 'descs iguais' : 'faltou entrada em um dos dois');
});
ok(R.infoOf(['imp'], 'saldo_total_total').desc.indexOf('Segunda diferen') >= 0,
   'imp:saldo_total_total fala de impulso, nao de estoque');
ok(R.infoOf(['saldo', 'modal'], 'saldo_total_total').desc.indexOf('Estoque') >= 0,
   'saldo:saldo_total_total fala de estoque, nao de impulso');
// Sufixo: chave cheia vence o sufixo dentro do mesmo namespace.
ok(R.infoOf(['saldo', 'modal'], 'ativ__outros').desc !== R.infoOf(['saldo', 'modal'], 'livre_pj__outros').desc,
   'ativ__outros nao herda o texto de modal:outros (chave cheia vence o sufixo)');
ok(R.infoOf(['saldo', 'modal'], 'livre_pj__cheque_especial') === R.infoOf(['taxa', 'modal'], 'livre_pf__cheque_especial'),
   'o sufixo faz UMA definicao de modalidade servir 4 prefixos e 4 abas');

// ── 5. `full` nunca repete o rotulo ──────────────────────────────────────────
secao('5. `full` so quando acrescenta');
// Comparacao NORMALIZADA (caixa e acento): "Cheque especial" vs "Cheque Especial" e
// repetir a linha de volta, mesmo passando numa igualdade estrita.
const norm = (x) => String(x).normalize('NFD').replace(/[̀-ͯ]/g, '').toLowerCase().replace(/[^a-z0-9]/g, '');
const repetidos = [];
TABELAS.forEach((t) => {
  achatar(t.tree).forEach((n) => {
    const info = R.infoOf(t.ns, n.key);
    if (info && info.full && norm(info.full) === norm(n.label)) repetidos.push(t.nome + '/' + n.key);
  });
});
ok(repetidos.length === 0, '`full` nunca repete o rotulo ja visivel na linha',
   repetidos.slice(0, 6).join(', '));
const semNada = Object.entries(R.NODE_INFO).filter(([, v]) => !v.full && !v.desc);
ok(semNada.length === 0, 'nenhuma entrada vazia (sem full e sem desc)', semNada.map((e) => e[0]).join(', '));

// ── 6. A unidade acompanha o seletor ─────────────────────────────────────────
// Tres tabelas trocam de unidade por seletor. Uma string fixa mentiria no 1o clique.
secao('6. Unidade do cartao segue o seletor');
function unidadeDoCartao(btn, label, info, unitFn) {
  R.showInfo(btn, label, info, unitFn);
  const html = doc.body.children[doc.body.children.length - 1]._html;
  const m = /class="info-unit">Unidade: ([^<]*)</.exec(html);
  return m ? m[1] : null;
}
const btnFake = new El('button');
const infoFluxo = R.infoOf(['fluxo'], 'fluxo_total');
// A tabela de fluxo comeca em "Fluxo" (% do PIB); clicar em "Impulso" leva a p.p. do PIB.
const uFluxoAntes = unidadeDoCartao(btnFake, 'Total', infoFluxo, null);
const pillsMedida = PILLS['imp-fluxo-medida-group'] || [];
const pillImpulso = pillsMedida.find((b) => b.dataset.variant === 'impulso');
ok(!!pillImpulso, 'pill "Impulso" existe no grupo de medida');
if (pillImpulso) pillImpulso.fire('click');
const linhasFluxo = linhasDaTabela(doc.getElementById('imp-fluxo-table-body'));
const botaoFluxo = linhasFluxo.find((l) => l.botao) || {};
if (botaoFluxo.botao) botaoFluxo.botao.fire('mouseenter');
let htmlPop = doc.body.children[doc.body.children.length - 1]._html;
ok(/Unidade: p\.p\. do PIB/.test(htmlPop),
   'na variante Impulso o cartao diz "p.p. do PIB"', htmlPop.slice(0, 160));
const pillFluxo = pillsMedida.find((b) => b.dataset.variant === 'fluxo');
if (pillFluxo) pillFluxo.fire('click');
const linhasFluxo2 = linhasDaTabela(doc.getElementById('imp-fluxo-table-body'));
const botaoFluxo2 = linhasFluxo2.find((l) => l.botao) || {};
if (botaoFluxo2.botao) botaoFluxo2.botao.fire('mouseenter');
htmlPop = doc.body.children[doc.body.children.length - 1]._html;
ok(/Unidade: % do PIB/.test(htmlPop),
   'de volta em Fluxo o cartao diz "% do PIB"', htmlPop.slice(0, 160));

// Saldo: Nominal/Nivel -> "R$ mi"; %PIB -> "% do PIB"
function cartaoDaPrimeiraLinha(bodyId) {
  const l = linhasDaTabela(doc.getElementById(bodyId)).find((x) => x.botao);
  if (!l) return null;
  l.botao.fire('mouseenter');
  return doc.body.children[doc.body.children.length - 1]._html;
}
let h = cartaoDaPrimeiraLinha('saldo-table-body');
ok(h && /Unidade: R\$ mi/.test(h), 'Saldo em Nominal/Nível: cartao diz "R$ mi"', (h || '').slice(0, 160));
const pillPctPib = (PILLS['saldo-basis-group'] || []).find((b) => b.dataset.basis === 'pctpib');
ok(!!pillPctPib, 'pill "% PIB" existe no grupo de base do Saldo');
if (pillPctPib) pillPctPib.fire('click');
h = cartaoDaPrimeiraLinha('saldo-table-body');
ok(h && /Unidade: % do PIB/.test(h), 'Saldo em % PIB: cartao acompanha', (h || '').slice(0, 160));
const pillNominal = (PILLS['saldo-basis-group'] || []).find((b) => b.dataset.basis === 'nominal');
if (pillNominal) pillNominal.fire('click');

// Taxa x Spread: mesma tabela, unidades diferentes -- e a mesma string vai para o eixo Y.
ok(R.taxaYTitle() === '% a.a.', 'taxaYTitle() em Taxa Média = "% a.a."', R.taxaYTitle());
R.taxaState.source = 'spread';
ok(/p\.p\./.test(R.taxaYTitle()), 'taxaYTitle() em Spread muda para p.p.', R.taxaYTitle());
ok(R.taxaInfoNs()[0] === 'spread', 'taxaInfoNs() acompanha a árvore selecionada', R.taxaInfoNs().join(','));
R.taxaState.source = 'taxa_media';
ok(R.taxaInfoNs()[0] === 'taxa', 'taxaInfoNs() volta para taxa', R.taxaInfoNs().join(','));
const usaTaxaYTitle = /renderLineChart\('chart-taxa', specs, taxaYTitle\(\)\)/.test(SRC);
ok(usaTaxaYTitle, 'o eixo Y do grafico de Taxa & Spread usa a MESMA funcao do cartao');

// ── 7. `unit` da linha vence a da tabela ─────────────────────────────────────
// Saldo de maior risco e atraso 15-90d nao sao "% da carteira em atraso > 90 dias".
secao('7. Linha com unidade propria');
[['riscoant__total', '% do saldo PJ'],
 ['riscores4966__mpme', '% do saldo PJ'],
 ['pj__atraso_pj', '% da carteira PJ com atraso de 15 a 90 dias']].forEach(([k, esperada]) => {
  const info = R.infoOf(['inad', 'modal'], k);
  ok(info && info.unit === esperada, 'inad:' + k + ' carrega unidade propria', info ? info.unit : 'sem entrada');
  const got = unidadeDoCartao(btnFake, 'x', info, R.inadInfoUnit);
  ok(got === esperada, 'e ela vence a unidade da tabela no cartao', got);
});
const infoModalInad = R.infoOf(['inad', 'modal'], 'livre_pf__cheque_especial');
ok(unidadeDoCartao(btnFake, 'Cheque Especial', infoModalInad, R.inadInfoUnit) === '% da carteira com atraso > 90 dias',
   'linha sem unidade propria herda a da tabela de inadimplencia');

// ── 8. O rotulo continua legivel depois do botao ─────────────────────────────
secao('8. Rotulo nao contaminado pelo "i"');
const linhasSaldo = linhasDaTabela(doc.getElementById('saldo-table-body'));
const comBotao = linhasSaldo.filter((l) => l.botao);
ok(comBotao.length > 0, 'a tabela Saldo tem linhas com cartao', String(comBotao.length));
const sujos = comBotao.filter((l) => /i$/.test(l.label) && l.label.length > 1 && !/^.*[a-zà-ú]i$/i.test(l.label));
ok(comBotao.every((l) => l.label && l.label === l.label.trim() && l.label.indexOf('▸') < 0),
   'rotulo lido dos nos de texto sai limpo (sem "i", sem seta)');
const cruTextContent = comBotao[0].tdLabel.children.map((c) => c.textContent).join('');
ok(cruTextContent !== comBotao[0].label,
   'e o textContent CRU realmente difere (o "i" esta la) — por isso a leitura filtra',
   JSON.stringify(cruTextContent) + ' vs ' + JSON.stringify(comBotao[0].label));

// ── 9. Conteudo do cartao ────────────────────────────────────────────────────
secao('9. Montagem do cartao');
R.showInfo(btnFake, 'Total', R.infoOf(['fluxo'], 'fluxo_total'), null);
const popHtml = doc.body.children[doc.body.children.length - 1]._html;
ok(/^<h4>Total<\/h4>/.test(popHtml), 'o cartao abre com o rotulo curto em <h4>');
ok(/class="info-full">Fluxo financeiro do crédito bancário/.test(popHtml), '`full` entra como info-full');
ok(/class="info-desc">/.test(popHtml), '`desc` entra como info-desc');
// `full` identico ao rotulo nao deve ser impresso.
R.showInfo(btnFake, 'Cheque Especial', { full: 'Cheque Especial', desc: 'x' }, null);
const popHtml2 = doc.body.children[doc.body.children.length - 1]._html;
ok(popHtml2.indexOf('info-full') < 0, '`full` igual ao rotulo nao e impresso');
ok(doc.body.children.filter((c) => c.classList.contains('info-pop')).length === 1,
   'existe UM unico .info-pop no body, reposicionado — nao um por linha');

// ── 10. Pin / unpin ──────────────────────────────────────────────────────────
secao('10. Clique fixa, segundo clique solta');
const alvo = comBotao[0].botao;
alvo.fire('click', { stopPropagation() {} });
ok(alvo.classList.contains('pinned'), 'primeiro clique fixa (classe .pinned)');
alvo.fire('click', { stopPropagation() {} });
ok(!alvo.classList.contains('pinned'), 'segundo clique solta');

// ── 11. Cobertura por tabela ─────────────────────────────────────────────────
// Piso por tabela: uma regressao que apague um namespace inteiro do mapa nao apareceria
// no total, que e dominado pelas modalidades compartilhadas.
secao('11. Cobertura por tabela (piso)');
const PISO = {
  'saldo': 40, 'amplo': 18, 'concessao': 40, 'fluxo': 3,
  'taxa': 40, 'spread': 7, 'inad': 40, 'ptc': 10, 'ptcsurp': 2, 'modal': 50,
};
const porNs = {};
Object.keys(R.NODE_INFO).forEach((k) => {
  const ns = k.split(':')[0];
  porNs[ns] = (porNs[ns] || 0) + 1;
});
// As 3 arvores de Biggs somam 15 nos no total (7+3+5) e TODOS tem de ter cartao: e o
// namespace onde a leitura muda de significado, entao um buraco ali e o pior caso.
const impCobertos = ['recurso', 'porte', 'atividade']
  .map((tk) => achatar(arvoreDe('impulso', tk)))
  .reduce((a, b) => a.concat(b), []);
ok(impCobertos.every((n) => R.infoOf(['imp'], n.key)) && impCobertos.length === 15,
   'Impulso: TODOS os 15 nos das 3 arvores tem cartao',
   impCobertos.filter((n) => !R.infoOf(['imp'], n.key)).map((n) => n.key).join(', ') || ('n=' + impCobertos.length));
Object.entries(PISO).forEach(([ns, piso]) => {
  if (ns === 'modal') {
    ok((porNs.modal || 0) >= piso, 'namespace "modal" tem pelo menos ' + piso + ' definicoes', String(porNs.modal || 0));
    return;
  }
  const t = TABELAS.find((x) => x.ns[0] === ns);
  const cobertas = achatar(t.tree).filter((n) => R.infoOf(t.ns, n.key)).length;
  ok(cobertas >= piso, t.nome + ': pelo menos ' + piso + ' linhas com cartao', String(cobertas));
});

// ── 12. Regressao: as tabelas continuam funcionando ──────────────────────────
secao('12. Regressao (o botao nao quebrou as tabelas)');
TABELAS.forEach((t) => {
  if (t.nome === 'Spread' || t.nome === 'PTC — surpresa') return;
  const linhas = linhasDaTabela(doc.getElementById(t.body));
  ok(linhas.length > 0, t.nome + ': tabela renderizou linhas', String(linhas.length));
});
const reacts = chamadas.filter((c) => c.tipo === 'react' || c.tipo === 'newPlot');
ok(reacts.length >= 10, 'os graficos das 6 abas seguem sendo plotados', String(reacts.length));

console.log('\n' + (falhas ? falhas + ' FALHA(S) de ' + asserts + ' assercoes' : asserts + ' assercoes -- TODOS OS TESTES PASSARAM'));
process.exit(falhas ? 1 : 0);
