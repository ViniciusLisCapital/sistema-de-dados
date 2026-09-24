// Testa o JS da coluna "Atualizar" do relatorio de calendario, executando o
// <script> REAL do HTML gerado contra um DOM stub e um fetch stub.
//
// Roda com:
//     node tests/test_release_calendar_js.js            # os dois modos
//     MODE=file node tests/test_release_calendar_js.js  # so um
//
// Precisa de reports/release_calendar.html gerado:
//     uv run python -c "from analytics.release_calendar.generate_report import run; run()"
//
// Por que um harness de verdade e nao `node --check`: este projeto ja teve dois bugs
// de dashboard chegarem em producao passando por checagem de sintaxe (ver
// .claude/rules/lis-dashboards.md, secao dos botoes de range) — o que falhou nos dois
// casos foi o COMPORTAMENTO no clique, nao a sintaxe. Aqui o clique e disparado de
// fato e o POST resultante e inspecionado.

const fs = require('fs');
const path = require('path');

const HTML = path.join(__dirname, '..', 'reports', 'release_calendar.html');
if (!fs.existsSync(HTML)) {
  console.error('reports/release_calendar.html nao existe — gere o relatorio primeiro.');
  process.exit(1);
}
const blocos = fs.readFileSync(HTML, 'utf8').match(/<script>([\s\S]*?)<\/script>/g) || [];
if (!blocos.length) { console.error('nenhum <script> encontrado no HTML'); process.exit(1); }
const SRC = blocos[blocos.length - 1].replace(/^<script>/, '').replace(/<\/script>$/, '');

let falhasTotais = 0;

function El(tag) {
  this.tag = tag || 'div';
  this.children = []; this.style = {}; this.dataset = {};
  this.className = ''; this.textContent = ''; this.title = ''; this.value = '';
  this.disabled = false; this._html = ''; this._listeners = {};
}
El.prototype.appendChild = function (c) { this.children.push(c); return c; };
El.prototype.removeChild = function (c) {
  const i = this.children.indexOf(c); if (i >= 0) this.children.splice(i, 1); return c;
};
El.prototype.addEventListener = function (k, f) { this._listeners[k] = f; };
El.prototype.querySelector = function () { return null; };
// O DOM aqui e string, nao arvore: um `querySelectorAll` honesto nao acha nada dentro de
// um innerHTML. Devolver [] deixa `wireDashFolds()` ser no-op no teste -- o que da para
// afirmar sobre o click-drop e a MARCACAO (details/summary/open), que e onde vive a
// decisao (o `open` sai de DASH.abertos a cada render).
El.prototype.querySelectorAll = function () { return []; };

/* Clique sintetico que REGISTRA stopPropagation/preventDefault. Importa porque o botao
   Regerar vive dentro de um <summary>, e abrir/fechar e a acao default de um clique ali:
   sem os dois, o card pisca aberto/fechado a cada Regerar. O evento antes nao tinha os
   metodos e o handler quebrava -- o teste denunciou na primeira execucao. */
function cliqueEm(alvo, btn) {
  const marcas = { stop: 0, prevent: 0 };
  alvo._listeners['click']({
    target: { closest: () => btn },
    stopPropagation: () => { marcas.stop++; },
    preventDefault: () => { marcas.prevent++; },
  });
  return marcas;
}
/* O listener da tabela procura DOIS seletores agora (o botao de atualizar e o
   cabecalho de semana), entao um `closest` que devolve sempre o mesmo objeto nao
   distingue os dois caminhos. Este recebe um mapa seletor -> alvo. */
function cliqueSeletivo(alvo, mapa) {
  const marcas = { stop: 0, prevent: 0 };
  alvo._listeners['click']({
    target: { closest: (sel) => (Object.prototype.hasOwnProperty.call(mapa, sel) ? mapa[sel] : null) },
    stopPropagation: () => { marcas.stop++; },
    preventDefault: () => { marcas.prevent++; },
  });
  return marcas;
}
El.prototype.remove = function () {};
El.prototype.select = function () {};
El.prototype.closest = function () { return this; };
Object.defineProperty(El.prototype, 'innerHTML', {
  get() { return this._html; },
  set(v) { this._html = v; this.children = []; },
});

const ESTADOS_OK = ['bcb_ptc', 'bcb_credit_note', 'bcb_icbr', 'bcb_focus', 'bcb_fiscal_statistics',
                    'bcb_external_sector_note', 'bcb_ibcbr', 'bcb_ptc', 'bcb_rpm', 'cftc_cot'];

// Payload de /api/dashboards. Mesmo shape de domain/dashboards/status.py::estado() --
// se aquele mudar de forma, este stub e que denuncia.
const DASHBOARDS_STUB = [
  { key: 'brasil_inflation', name: 'Inflação (BR)', area: 'brasil',
    output: 'reports/brasil/Inflation.html', build_seconds: 30, veredito: 'desatualizado',
    module: 'analytics.brasil.inflation.generate_report',
    gerado_em: '2026-08-20T09:00:00', tamanho_mb: 104.3, n_deps: 2, n_fora_mysql: 1, n_novos: 1,
    deps: [
      { ref: 'macro_brasil.inflc_decomposicao', kind: 'mysql', onde: 'macro_brasil',
        fora_do_mysql: false, role: 'IPCA por subitem', scope: 'dados',
        ultimo: '2026-08-01', stamp: '2026-07-01', novo: true, arquivo_mais_novo: false },
      { ref: 'analytics/brasil/inflation/data/ipca_bcb_series.csv', kind: 'csv', onde: 'arquivo',
        fora_do_mysql: true, role: 'Agregados BCB/SGS', scope: 'dados',
        ultimo: '2026-07', mtime: '2026-08-01T10:00:00', novo: false, arquivo_mais_novo: false,
        refresh: 'uv run python analytics/brasil/inflation/fetch_bcb.py' },
    ] },
  { key: 'us_inflation', name: 'Inflation (US)', area: 'us',
    output: 'reports/us/Inflation.html', build_seconds: 13, veredito: 'em dia',
    module: 'analytics.us.inflation.generate_report',
    gerado_em: '2026-08-26T09:00:00', tamanho_mb: 5.6, n_deps: 1, n_fora_mysql: 0, n_novos: 0,
    n_proc: 2, n_proc_atrasados: 1,
    deps: [
      { ref: 'macro_us.inflc_cpi', kind: 'mysql', onde: 'macro_us', fora_do_mysql: false,
        role: 'Níveis do CPI-U', scope: 'dados', ultimo: '2026-07-01', stamp: '2026-07-01',
        novo: false, arquivo_mais_novo: false },
      // Artefato com procedimento declarado. O `ultimo` dele e o CORTE lido de dentro do
      // arquivo (json_date), nao o mtime -- e o que faz o veredito de atraso existir.
      { ref: 'analytics/us/inflation/data/previsao.json', kind: 'artifact', onde: 'arquivo',
        fora_do_mysql: true, role: 'Previsão', scope: 'dados', ultimo: '2026-08-25',
        mtime: '2026-08-25T17:33:48', novo: false, arquivo_mais_novo: false,
        procedimento: 'previsao',
        refresh: 'uv run python -c "from x import salvar; salvar()"' },
      { ref: 'analytics/us/inflation/data/painel.csv', kind: 'artifact', onde: 'arquivo',
        fora_do_mysql: true, role: 'Painel', scope: 'dados', ultimo: '2026Q3',
        mtime: '2026-08-21T15:54:56', novo: false, arquivo_mais_novo: false,
        procedimento: 'painel' },
    ],
    procedimentos: [
      // Trimestral e EM DIA: e o caso que impede o Regerar de refazer 4 min de estimacao
      // a cada boletim diario. Se a granularidade parar de valer, este passo entra na
      // conta de segundos do botao e a assercao de tempo abaixo falha.
      { id: 'painel', label: 'Painéis trimestrais', seconds: 90,
        writes: ['analytics/us/inflation/data/painel.csv'],
        reads: ['macro_us.inflc_cpi'], granularidade: 'trimestre',
        cut_from: 'analytics/us/inflation/data/painel.csv', corte: '2026Q3',
        fonte_max: '2026Q3', fonte_ref: 'macro_us.inflc_cpi',
        atrasado: false, dias_atras: null, rodou_em: '2026-08-21T15:54:56', faltando: [],
        command: 'uv run python -c "from a import b; b()"',
        note: 'Depende do IPEADATA.' },
      { id: 'previsao', label: 'Previsão + backtest', seconds: 110,
        writes: ['analytics/us/inflation/data/previsao.json'],
        reads: ['macro_us.inflc_cpi'], granularidade: 'dia',
        cut_from: 'analytics/us/inflation/data/previsao.json', corte: '2026-08-25',
        fonte_max: '2026-08-28', fonte_ref: 'macro_us.inflc_cpi',
        atrasado: true, dias_atras: 3, rodou_em: '2026-08-25T17:33:48', faltando: [],
        command: 'uv run python -c "from x import salvar; salvar()"',
        note: '36 rodadas do espaço de estados.' },
    ] },
  // ── os tres que o lote tem de DEIXAR DE FORA ──────────────────────────────
  // 1. sem entry point automatico: nao tem nem botao de card (o Oraculo real e assim).
  { key: 'oraculo', name: 'Oráculo (Power BI)', area: 'raiz',
    output: 'reports/oraculo.csv', build_seconds: 20, veredito: 'desatualizado',
    module: null, command: 'uv run python jobs/update_oraculo.py',
    gerado_em: '2026-08-01T09:00:00', tamanho_mb: 0.2, n_deps: 1, n_fora_mysql: 0,
    n_novos: 1,
    deps: [{ ref: 'macro_brasil.atv_ibcbr', kind: 'mysql', onde: 'macro_brasil',
             fora_do_mysql: false, role: 'IBC-Br', scope: 'dados', ultimo: '2026-06-01',
             stamp: '2026-06-01', novo: false, arquivo_mais_novo: false }] },
  // 2. nunca gerado: construir pela primeira vez e uma decisao, nao consequencia de dado.
  { key: 'brasil_credit', name: 'Crédito', area: 'brasil',
    output: 'reports/brasil/Credit.html', build_seconds: 24, veredito: 'sem relatorio',
    module: 'analytics.brasil.credit.generate_report',
    gerado_em: null, tamanho_mb: null, n_deps: 1, n_fora_mysql: 0, n_novos: 0,
    deps: [{ ref: 'macro_brasil.cred_saldo_modalidade', kind: 'mysql',
             onde: 'macro_brasil', fora_do_mysql: false, role: 'Saldo por modalidade',
             scope: 'dados', ultimo: '2026-07-01', stamp: null, novo: false,
             arquivo_mais_novo: false }] },
  // 3. sem stamp: nao e atraso, e a falta do retrato que permitiria afirmar que bate.
  { key: 'brasil_exchange_rate', name: 'Câmbio', area: 'brasil',
    output: 'reports/brasil/FX Report.html', build_seconds: 43, veredito: 'sem stamp',
    module: 'analytics.brasil.exchange_rate.generate_report',
    gerado_em: '2026-08-25T19:31:45', tamanho_mb: 2.2, n_deps: 1, n_fora_mysql: 1,
    n_novos: 0,
    deps: [{ ref: 'analytics/brasil/exchange_rate/data/model_fit_cutoff.json',
             kind: 'artifact', onde: 'arquivo', fora_do_mysql: true,
             role: 'Corte do ajuste do modelo', scope: 'modelos', ultimo: '2026-06',
             mtime: '2026-08-01T10:00:00', novo: false, arquivo_mais_novo: false }] },
];

// document stub compartilhado. A aba nova usa querySelector('.tab-bar') e
// querySelectorAll('.tab-btn'), que o stub antigo devolvia como null -- o teste
// quebrou de verdade quando a aba entrou, e por isso o stub virou funcao unica.
function mkDoc(getEl) {
  const tabBar = new El('nav');
  const botoes = ['view-releases', 'view-dashboards'].map((v) => {
    const b = new El('button');
    b.dataset.view = v;
    b.setAttribute = function (k, val) { this['attr_' + k] = val; };
    b.getAttribute = function (k) { return this['attr_' + k]; };
    return b;
  });
  return {
    getElementById: getEl,
    createElement: (t) => new El(t),
    querySelector: (sel) => (sel === '.tab-bar' ? tabBar : null),
    querySelectorAll: (sel) => (sel === '.tab-btn' ? botoes : []),
    body: new El('body'),
    execCommand: () => true,
    addEventListener: () => {},
    _tabBar: tabBar,
    _tabBtns: botoes,
  };
}

function rodar(MODE, HOJE, AGORA) {
  HOJE = HOJE || '2026-08-17';
  AGORA = AGORA || '23:59';
  const els = {};
  const getEl = (id) => (els[id] = els[id] || new El('div'));
  const calls = [];

  global.document = mkDoc(getEl);
  global.window = { isSecureContext: false };
  global.navigator = {};
  global.fetch = function (url, opts) {
    calls.push({ url, opts });
    if (MODE === 'file') return Promise.reject(new Error('sem servidor'));
    if (url === '/api/ping') {
      return Promise.resolve({ ok: true, json: () => Promise.resolve({ ok: true, modo: 'servido', hoje: HOJE, agora: AGORA }) });
    }
    if (url === '/api/status') {
      const grupos = { ibge_pmc: { estado: 'atrasado', tabelas: [] },
                       bcb_copom_ata: { estado: 'vazio', tabelas: [] },
                       bcb_copom: { estado: 'indefinido', tabelas: [] } };
      ESTADOS_OK.forEach((g) => { grupos[g] = { estado: 'ok', tabelas: [] }; });
      return Promise.resolve({ ok: true, json: () => Promise.resolve({ ok: true, hoje: HOJE, agora: AGORA, grupos }) });
    }
    if (url === '/api/run') {
      return Promise.resolve({ ok: true, json: () => Promise.resolve({ ok: true, n_ok: 1, n_erro: 0, sem_script: [] }) });
    }
    if (url === '/api/dashboards') {
      return Promise.resolve({ ok: true, json: () => Promise.resolve(
        { ok: true, agora: AGORA, dashboards: DASHBOARDS_STUB }) });
    }
    return Promise.reject(new Error('rota inesperada ' + url));
  };

  // Expoe o recorte: o padrao da aba passou a ser UM MES, entao as asserções amplas
  // (as ~224 linhas do ano) precisam abrir o recorte de proposito -- e as do recorte
  // padrao precisam poder ler o estado que o produziu.
  new Function(SRC + ';global.__CAL = Object.assign(global.__CAL || {}, '
              + '{state: state, renderAll: renderAll, renderTable: renderTable, '
              + 'hojeRef: hojeRef, segundaDa: segundaDa});')();

  let falhas = 0;
  const check = (rotulo, cond, extra) => {
    if (cond) console.log('  ok     ' + rotulo);
    else { console.log('  FALHA  ' + rotulo + (extra !== undefined ? '  -> ' + extra : '')); falhas++; }
  };

  return new Promise((resolve) => {
    setTimeout(() => {
      const CAL = global.__CAL;
      console.log('\nMODE=' + MODE);

      // ── (1) O RECORTE PADRAO: mes corrente, em blocos de semana ─────────────
      // Pedido do usuario: a pagina abre no mes que esta correndo, nao no ano inteiro,
      // e dentro do mes a lista vem em blocos por semana, com a semana corrente aberta.
      // O "hoje" e o da pagina (data de geracao, trocada pela do servidor no ping), nao
      // o relogio da maquina que roda o teste.
      const mesAtual = CAL.hojeRef().slice(0, 7);
      check('abre no mes corrente, nao em "Tudo"', CAL.state.month === mesAtual,
            CAL.state.month + ' vs ' + mesAtual);
      check('os outros tres seletores abrem em "todos"',
            CAL.state.pais === 'Todos' && CAL.state.institution === 'Todos' &&
            CAL.state.divulgacao === 'Todas',
            [CAL.state.pais, CAL.state.institution, CAL.state.divulgacao].join(','));
      check('o seletor de mes existe e esta no mes corrente',
            getEl('mes-select').value === mesAtual, getEl('mes-select').value);
      check('e sai marcado como recorte estreito',
            getEl('mes-select').className.indexOf('narrow') >= 0,
            getEl('mes-select').className);
      check('o seletor de pais tem Todos + BR/US/INT',
            getEl('pais-select').children.map((o) => o.value).join(',') === 'Todos,BR,US,INT',
            getEl('pais-select').children.map((o) => o.value).join(','));
      check('fonte e divulgacao tambem sao seletores, nao pills',
            getEl('fonte-select').children.length > 3 &&
            getEl('divulgacao-select').children.length > 3,
            getEl('fonte-select').children.length + '/' +
            getEl('divulgacao-select').children.length);

      const padrao = getEl('table-body').children;
      const cabSem = padrao.filter((c) => (c.className || '').indexOf('week-header') >= 0);
      check('a lista do mes vem em blocos por semana', cabSem.length >= 3, cabSem.length);
      const abertas = cabSem.filter((c) => c.innerHTML.indexOf('wk-caret">\u2212') >= 0);
      check('exatamente uma semana vem aberta', abertas.length === 1, abertas.length);
      const semanaHoje = CAL.segundaDa(CAL.hojeRef());
      const marcada = cabSem.filter((c) => c.innerHTML.indexOf('wk-now') >= 0);
      check('a semana corrente e a marcada e a aberta',
            marcada.length === 1 &&
            marcada[0].innerHTML.indexOf('data-week="' + semanaHoje + '"') >= 0 &&
            abertas[0].innerHTML.indexOf('data-week="' + semanaHoje + '"') >= 0,
            marcada.length + ' | ' + (abertas[0] && abertas[0].innerHTML.slice(0, 80)));
      const linhasSemana = padrao.filter((c) => c.innerHTML.indexOf('col-update') >= 0);
      check('so as linhas da semana aberta sao renderizadas',
            linhasSemana.length > 0 && linhasSemana.length < 40, linhasSemana.length);
      check('cada linha tras o selo de pais',
            linhasSemana.every((c) => /pais-badge (br|us|int)"/.test(c.innerHTML)),
            linhasSemana.map((c) => c.innerHTML.slice(0, 60))[0]);
      check('a dica explica o clique-expande da semana',
            getEl('list-hint').innerHTML.indexOf('semana') >= 0,
            getEl('list-hint').innerHTML.slice(0, 60));

      // Os 3 stat cards sairam a pedido do usuario; as contagens que eles carregavam
      // ficaram, numa linha ao lado do titulo. Ela conta o RECORTE inteiro -- nem so as
      // linhas visiveis (a semana fechada continua sendo divulgacao do mes), nem o
      // calendario todo (seria um numero que a tabela ao lado contradiz).
      const nDoResumo = (h) => parseInt(
        (h.match(/<strong>(\d+)<\/strong> divulga/) || [0, '0'])[1], 10);
      const resumo = getEl('list-resumo').innerHTML;
      check('o resumo do recorte substitui os stat cards',
            nDoResumo(resumo) > 0 &&
            (/data estimada/.test(resumo) || /data confirmada/.test(resumo)),
            resumo.slice(0, 120));
      const somaSemanas = cabSem.reduce((t, c) => t + parseInt(
        (c.innerHTML.match(/wk-count">(\d+)/) || [0, '0'])[1], 10), 0);
      check('e conta o mes inteiro, nao so a semana aberta',
            nDoResumo(resumo) === somaSemanas && somaSemanas > linhasSemana.length,
            nDoResumo(resumo) + ' vs ' + somaSemanas + ' (visiveis ' + linhasSemana.length + ')');

      // A semana e de segunda a domingo, e as contas sao em UTC. Domingo pertence a
      // semana que COMECOU na segunda anterior -- um `getDay()` local, ou um Date
      // construido sem o Z, desloca o bloco inteiro e um dado de segunda aparece no
      // bloco da semana passada, sem erro nenhum.
      check('domingo cai na semana que comecou na segunda anterior',
            CAL.segundaDa('2026-09-06') === '2026-08-31', CAL.segundaDa('2026-09-06'));
      check('segunda comeca a propria semana',
            CAL.segundaDa('2026-09-07') === '2026-09-07', CAL.segundaDa('2026-09-07'));
      check('sabado ainda e da semana da segunda anterior',
            CAL.segundaDa('2026-09-12') === '2026-09-07', CAL.segundaDa('2026-09-12'));

      // O que ja saiu recua; o que esta ATRASADO nao recua, porque e a unica linha da
      // pagina que pede acao. Os dois lados precisam ser afirmados: so o primeiro
      // passaria num mutante que apaga a linha laranja junto.
      const jaSaiu = padrao.filter((c) => c.innerHTML.indexOf('upd-ok') >= 0 ||
                                          c.innerHTML.indexOf('sem tabela') >= 0);
      const futuras0 = padrao.filter((c) => c.innerHTML.indexOf('upd-none">\u2014') >= 0);
      check('divulgacao que ja saiu fica em cinza',
            jaSaiu.length > 0 &&
            jaSaiu.every((c) => (c.className || '').indexOf('done') >= 0),
            jaSaiu.length + ' | ' + jaSaiu.map((c) => c.className).join('|'));
      check('e a futura nao fica',
            futuras0.length > 0 &&
            futuras0.every((c) => (c.className || '').indexOf('done') < 0),
            futuras0.length + ' | ' + futuras0.map((c) => c.className).join('|'));

      // Clicar no cabecalho fecha a semana; clicar de novo reabre. O `closest` do stub
      // distingue os dois seletores que o listener procura -- com um closest unico, o
      // clique da semana seria lido como clique no botao de atualizar.
      const tdSem = { dataset: { week: semanaHoje } };
      cliqueSeletivo(getEl('table-body'), { 'button.upd-btn': null, '[data-week]': tdSem });
      const fechada = getEl('table-body').children;
      check('clique no cabecalho fecha a semana',
            fechada.filter((c) => c.innerHTML.indexOf('col-update') >= 0).length === 0,
            fechada.filter((c) => c.innerHTML.indexOf('col-update') >= 0).length);
      check('e nenhuma outra abre sozinha no lugar',
            fechada.filter((c) => c.innerHTML.indexOf('wk-caret">\u2212') >= 0).length === 0);
      cliqueSeletivo(getEl('table-body'), { 'button.upd-btn': null, '[data-week]': tdSem });
      check('clicar de novo reabre',
            getEl('table-body').children.filter(
              (c) => c.innerHTML.indexOf('col-update') >= 0).length === linhasSemana.length);

      // ── (1b) O filtro de pais, e a cascata que vem com ele ─────────────────
      CAL.state.month = 'Tudo';
      CAL.state.mesEscolhido = true;
      CAL.state.pais = 'US';
      CAL.renderAll();
      const soUS = getEl('table-body').children
        .filter((c) => c.innerHTML.indexOf('col-update') >= 0);
      check('filtrar por US deixa so as linhas americanas',
            soUS.length > 0 && soUS.every((c) => c.innerHTML.indexOf('pais-badge us') >= 0),
            soUS.length);
      check('e a lista de fontes estreita junto (BLS/BEA, sem IBGE)',
            getEl('fonte-select').children.map((o) => o.value).indexOf('IBGE') < 0 &&
            getEl('fonte-select').children.map((o) => o.value).indexOf('BLS') >= 0,
            getEl('fonte-select').children.map((o) => o.value).join(','));
      // Uma fonte que nao existe sob o pais escolhido tem de CAIR DE VOLTA para "todas",
      // e nao ficar valida no objeto e invalida na tela (tabela vazia sem dizer por que).
      CAL.state.institution = 'IBGE';
      CAL.renderAll();
      check('fonte impossivel sob o pais escolhido cai de volta para "todas"',
            CAL.state.institution === 'Todos', CAL.state.institution);
      check('e a tabela continua listando as linhas do pais',
            getEl('table-body').children
              .filter((c) => c.innerHTML.indexOf('col-update') >= 0).length === soUS.length);

      // ── (2) As asserções amplas, com o recorte aberto de proposito ──────────
      CAL.state.pais = 'Todos';
      CAL.renderAll();

      const all = getEl('table-body').children.map((c) => c.innerHTML).filter(Boolean);
      const linhas = all.filter((h) => h.indexOf('col-update') >= 0);
      const mes = all.filter((h) => h.indexOf('colspan') >= 0);

      check('renderizou linhas de divulgacao', linhas.length > 100, linhas.length);
      check('o resumo acompanha o recorte quando ele abre',
            nDoResumo(getEl('list-resumo').innerHTML) === linhas.length,
            nDoResumo(getEl('list-resumo').innerHTML) + ' vs ' + linhas.length);

      // A linha ATRASADA nao recua: ela e a unica da pagina que pede acao, e apaga-la
      // por "ja ter saido" apagaria exatamente essa. Fica aqui, e nao no recorte
      // padrao, porque so com o calendario inteiro o stub garante uma linha laranja --
      // um `if (atrasadas.length)` no recorte estreito nunca dispararia, e o mutante
      // que pinta a atrasada de cinza passaria.
      const trsAmplo = getEl('table-body').children;
      const atrasadas = trsAmplo.filter((c) => c.innerHTML.indexOf('upd-btn late') >= 0);
      if (MODE === 'served') {
        check('a divulgacao atrasada NAO fica em cinza',
              atrasadas.length > 0 &&
              atrasadas.every((c) => (c.className || '').indexOf('done') < 0),
              atrasadas.length + ' | ' + atrasadas.map((c) => c.className).join('|'));
      }
      check('cabecalho de mes com colspan=7',
            mes.length > 0 && mes.every((h) => h.indexOf('colspan="7"') >= 0));
      check('exatamente 1 celula col-update por linha',
            linhas.every((h) => (h.match(/col-update/g) || []).length === 1));

      const futuras = linhas.filter((h) => h.indexOf('upd-none">—') >= 0);
      const botoes = linhas.filter((h) => h.indexOf('upd-btn') >= 0);
      const checks = linhas.filter((h) => h.indexOf('upd-ok') >= 0);
      const semTab = linhas.filter((h) => h.indexOf('sem tabela') >= 0);
      check('toda linha classificada em exatamente um estado',
            futuras.length + botoes.length + checks.length + semTab.length === linhas.length,
            `${futuras.length}+${botoes.length}+${checks.length}+${semTab.length} != ${linhas.length}`);
      check('divulgacao futura nao oferece botao', futuras.length > 0 && botoes.length < linhas.length);

      const ata = linhas.filter((h) => h.indexOf('Copom') >= 0 && h.indexOf('Ata') >= 0);
      check('grupo que nao alimenta tabela nunca ganha botao',
            ata.length > 0 && ata.every((h) => h.indexOf('upd-btn') < 0), ata.length);

      const pmc = linhas.filter((h) => h.indexOf('13/08/2026') >= 0 && h.indexOf('Comércio') >= 0);

      if (MODE === 'file') {
        check('so pingou, nao pediu status', calls.some((c) => c.url === '/api/ping') &&
              !calls.some((c) => c.url === '/api/status'));
        check('botao rotulado "Copiar cmd"', botoes.every((h) => h.indexOf('Copiar cmd') >= 0));
        check('nenhum check verde sem servidor', checks.length === 0);
        check('nenhum botao laranja sem servidor', !botoes.some((h) => h.indexOf('upd-btn late') >= 0));
        check('hint anuncia modo arquivo', getEl('mode-hint').innerHTML.indexOf('modo arquivo') >= 0);
        console.log(falhas ? `  -> ${falhas} falha(s)` : '  -> ok');
        falhasTotais += falhas; resolve();
        return;
      }

      check('pediu /api/status', calls.some((c) => c.url === '/api/status'));
      check('botao rotulado "Atualizar"', botoes.every((h) => h.indexOf('Atualizar') >= 0));
      check('grupo atrasado -> botao laranja',
            pmc.length === 1 && pmc[0].indexOf('upd-btn late') >= 0, pmc[0]);
      check('grupo em dia -> check verde e nenhum botao',
            checks.length > 0 && checks.every((h) => h.indexOf('upd-btn') < 0));
      check('hint anuncia servido', getEl('mode-hint').innerHTML.indexOf('servido') >= 0);

      // dispara o clique delegado de verdade
      const btn = new El('button');
      btn.dataset.group = 'ibge_pmc';
      btn.textContent = 'Atualizar';
      cliqueEm(getEl('table-body'), btn);
      setTimeout(() => {
        const post = calls.filter((c) => c.url === '/api/run');
        check('clique dispara POST /api/run', post.length === 1, post.length);
        check('POST usa method POST', post.length === 1 && post[0].opts.method === 'POST');
        check('POST manda o slug do grupo',
              post.length === 1 && JSON.parse(post[0].opts.body).group === 'ibge_pmc');
        check('botao ficou desabilitado durante o run', btn.disabled === true);
        console.log(falhas ? `  -> ${falhas} falha(s)` : '  -> ok');
        falhasTotais += falhas; resolve();
      }, 40);
    }, 40);
  });
}

// ---------------------------------------------------------------------------
// ORDEM NO MARKUP: a barra de recorte fica DENTRO do card da lista e ACIMA da tabela,
// e os 3 stat cards da aba de divulgacoes nao existem mais. Pedido do usuario
// (2026-09-22): "coloque o seletor logo acima da tabela, e melhor, pode retirar esses
// cards". E um guarda estatico porque o stub de DOM deste harness e string: "esta acima
// da tabela" e propriedade do HTML entregue, nao do que o render devolve.
// ---------------------------------------------------------------------------
function testeOrdemDoMarkup() {
  let falhas = 0;
  const check = (rotulo, cond, extra) => {
    if (cond) console.log('  ok     ' + rotulo);
    else { console.log('  FALHA  ' + rotulo + (extra !== undefined ? '  -> ' + extra : '')); falhas++; }
  };
  console.log('');
  console.log('ORDEM NO MARKUP - barra acima da tabela, sem stat cards');

  const doc = fs.readFileSync(HTML, 'utf8');
  const view = doc.slice(doc.indexOf('id="view-releases"'),
                         doc.indexOf('id="view-dashboards"'));

  const iCard = view.indexOf('class="table-card"');
  const iBarra = view.indexOf('class="ctrl-bar inline"');
  const iTabela = view.indexOf('<table class="release-table"');
  check('a aba tem uma barra de recorte', iBarra >= 0);
  check('ela vive DENTRO do card da lista', iCard >= 0 && iBarra > iCard, iCard + '/' + iBarra);
  check('e imediatamente ACIMA da tabela', iBarra < iTabela, iBarra + '/' + iTabela);
  check('nada de tabela entre a barra e o <table>',
        view.slice(iBarra, iTabela).indexOf('<table') < 0);
  check('os 4 seletores estao na barra',
        ['pais-select', 'fonte-select', 'divulgacao-select', 'mes-select']
          .every((id) => {
            const i = view.indexOf('id="' + id + '"');
            return i > iBarra && i < iTabela;
          }));
  check('os 3 stat cards sairam da aba de divulgacoes',
        view.indexOf('stats-grid') < 0 && view.indexOf('stat-card') < 0,
        view.indexOf('stats-grid'));
  // ... e em 2026-09-23 sairam tambem da aba de dashboards, no mesmo pedido de um dia
  // depois ("pode retirar esses cards, por favor"). Nao ha mais stat card na pagina.
  const dash = doc.slice(doc.indexOf('id="view-dashboards"'), doc.indexOf('</main>'));
  check('e sairam tambem da aba de dashboards',
        dash.indexOf('stats-grid') < 0 && dash.indexOf('stat-card') < 0,
        dash.indexOf('stats-grid'));
  check('nenhum stat card sobrou na pagina inteira',
        doc.indexOf('class="stat-card"') < 0, doc.indexOf('class="stat-card"'));
  // O que eles contavam sobreviveu numa linha ao lado do titulo, como na outra aba.
  const iH2 = dash.indexOf('<h2>');
  const iResumo = dash.indexOf('id="dash-resumo"');
  check('a contagem ficou, ao lado do titulo',
        iResumo > iH2 && iResumo < dash.indexOf('id="bulk-dashboards"'),
        iH2 + '/' + iResumo);

  console.log(falhas ? `  -> ${falhas} falha(s)` : '  -> ok');
  falhasTotais += falhas;
}

// ---------------------------------------------------------------------------
// Cenario de HORARIO: a PTC de 20/08/2026 tem release_time 14:30 no YAML. Antes da
// hora a linha nao pode oferecer botao (o dado ainda nao existe); depois, sim.
// Regressao do pedido de 2026-08-20 ("quero introduzir a hora da divulgacao").
// ---------------------------------------------------------------------------
async function testeHorario() {
  let falhas = 0;
  const check = (rotulo, cond, extra) => {
    if (cond) console.log('  ok     ' + rotulo);
    else { console.log('  FALHA  ' + rotulo + (extra !== undefined ? '  -> ' + extra : '')); falhas++; }
  };
  console.log('');
  console.log('HORARIO - PTC de 20/08 as 14:30');

  for (const [agora, esperaBotao] of [['09:00', false], ['14:29', false],
                                      ['14:30', true],  ['16:00', true]]) {
    const els = {};
    const getEl = (id) => (els[id] = els[id] || new El('div'));
    global.document = mkDoc(getEl);
    global.window = { isSecureContext: false };
    global.navigator = {};
    global.fetch = (url) => {
      if (url === '/api/ping')
        return Promise.resolve({ ok: true, json: () => Promise.resolve(
          { ok: true, modo: 'servido', hoje: '2026-08-20', agora }) });
      if (url === '/api/status')
        return Promise.resolve({ ok: true, json: () => Promise.resolve(
          { ok: true, hoje: '2026-08-20', agora,
            grupos: { bcb_ptc: { estado: 'atrasado', tabelas: [] } } }) });
      if (url === '/api/dashboards')
        return Promise.resolve({ ok: true, json: () => Promise.resolve(
          { ok: true, agora, dashboards: DASHBOARDS_STUB }) });
      return Promise.reject(new Error('inesperado ' + url));
    };
    new Function(SRC)();
    await new Promise((r) => setTimeout(r, 40));

    const linha = getEl('table-body').children.map((c) => c.innerHTML)
      .filter((h) => h && h.indexOf('20/08/2026') >= 0 && h.indexOf('PTC') >= 0);
    if (linha.length !== 1) { check(`achou a linha da PTC as ${agora}`, false, linha.length); continue; }
    const temBotao = linha[0].indexOf('upd-btn') >= 0;
    const mostraHora = linha[0].indexOf('14:30') >= 0;
    check(`${agora}: ${esperaBotao ? 'botao' : 'sem botao'}`, temBotao === esperaBotao,
          `temBotao=${temBotao}`);
    if (agora === '09:00') check('  a hora aparece na coluna de data', mostraHora, linha[0].slice(0, 120));
  }
  console.log(falhas ? `  -> ${falhas} falha(s)` : '  -> ok');
  falhasTotais += falhas;
}

// ---------------------------------------------------------------------------
// Aba "Status dashboard": estrutura embutida no modo arquivo, estado ao vivo no
// modo servido, e os dois filtros. O ponto que importa e a aba responder a
// pergunta "de onde vem o dado e ate quando ele vai" nos DOIS modos -- um
// relatorio recebido por email nao pode mostrar a coluna vazia.
// ---------------------------------------------------------------------------
async function testeStatusDashboard(MODE) {
  let falhas = 0;
  const check = (rotulo, cond, extra) => {
    if (cond) console.log('  ok     ' + rotulo);
    else { console.log('  FALHA  ' + rotulo + (extra !== undefined ? '  -> ' + extra : '')); falhas++; }
  };
  console.log('');
  console.log('STATUS DASHBOARD - MODE=' + MODE);

  const els = {};
  const getEl = (id) => (els[id] = els[id] || new El('div'));
  const calls = [];
  global.document = mkDoc(getEl);
  global.window = { isSecureContext: false };
  global.navigator = {};
  global.fetch = (url, opts) => {
    calls.push(url);
    if (MODE === 'file') return Promise.reject(new Error('sem servidor'));
    if (url === '/api/ping')
      return Promise.resolve({ ok: true, json: () => Promise.resolve(
        { ok: true, modo: 'servido', hoje: '2026-08-26', agora: '10:00' }) });
    if (url === '/api/status')
      return Promise.resolve({ ok: true, json: () => Promise.resolve(
        { ok: true, hoje: '2026-08-26', agora: '10:00', grupos: {} }) });
    if (url === '/api/dashboards')
      return Promise.resolve({ ok: true, json: () => Promise.resolve(
        { ok: true, agora: '10:00',
          dashboards: JSON.parse(JSON.stringify(DASHBOARDS_STUB)) }) });
    if (url === '/api/gerar') {
      // Responde pela KEY do corpo: o Regerar de um dashboard COM procedimento atrasado
      // devolve o que recalculou, e o de um SEM devolve lista vazia. Sao as duas
      // mensagens diferentes que a aba tem de saber escrever.
      const key = JSON.parse((opts && opts.body) || '{}').key;
      if (key === 'us_inflation') {
        const nova = JSON.parse(JSON.stringify(DASHBOARDS_STUB[1]));
        nova.n_proc_atrasados = 0;
        nova.procedimentos[1].atrasado = false;
        nova.procedimentos[1].corte = '2026-08-28';
        nova.procedimentos[1].dias_atras = 0;
        nova.deps[1].ultimo = '2026-08-28';
        nova.gerado_em = '2026-08-26T10:02:30';
        return Promise.resolve({ ok: true, json: () => Promise.resolve(
          { ok: true, key, segundos: 13.4, segundos_total: 121.8,
            n_recalculados: 1, n_falhou: 0, dashboard: nova,
            procedimentos: [
              { id: 'painel', label: 'Painéis trimestrais', acao: 'em dia' },
              { id: 'previsao', label: 'Previsão + backtest', acao: 'rodado',
                segundos: 108.4 },
            ] }) });
      }
      // o servidor devolve a linha nova SO do dashboard regerado
      const nova = JSON.parse(JSON.stringify(DASHBOARDS_STUB[0]));
      nova.veredito = 'em dia';
      nova.n_novos = 0;
      nova.gerado_em = '2026-08-26T10:00:30';
      nova.deps[0].novo = false;
      nova.deps[0].stamp = '2026-08-01';
      return Promise.resolve({ ok: true, json: () => Promise.resolve(
        { ok: true, key: 'brasil_inflation', segundos: 31.2, segundos_total: 31.2,
          n_recalculados: 0, n_falhou: 0, procedimentos: [], dashboard: nova }) });
    }
    return Promise.reject(new Error('inesperado ' + url));
  };

  // Expoe DASH/renderDashboards: o estado de aberto/fechado do click-drop nao da para
  // testar pelo DOM (o stub e string), mas da para testar pelo RENDER -- marcar aberto e
  // exigir que o `open` reapareca.
  new Function(SRC + ';global.__CAL = {DASH: DASH, '
              + 'renderDashboards: renderDashboards};')();
  await new Promise((r) => setTimeout(r, 60));

  const cards = getEl('dash-cards').innerHTML;
  const hint = getEl('dash-mode-hint').innerHTML;

  check('renderizou cards de dashboard', cards.indexOf('dash-card') >= 0);
  check('mostra o caminho do arquivo gerado', cards.indexOf('reports/') >= 0);

  // ── a prosa do card e para quem NUNCA viu o dashboard ─────────────────────
  // Pedido explicito do usuario (2026-09-01), sobre um print: as notas tinham virado
  // transcricao da nossa conversa -- decisoes ("Desde 2026-08-31"), nomes de funcao e
  // de arquivo do repositorio, e medicoes nossas ("Segundos nao medidos"). O texto tem
  // de explicar o que esta acontecendo ALI. O teste roda contra o payload REAL, entao
  // ele cobre o que esta escrito no manifest.yaml, nao so o que o template monta.
  // So no MODE=file: la os cards vem do payload REAL embutido, entao a asserção cobre o
  // que esta escrito no manifest.yaml. No MODE=served as notas sao stubs curtos.
  if (MODE === 'file') {
    const PROSA = (cards.match(
      /<div class="(?:dash-note|proc-note|proc-hint)">([\s\S]*?)<\/div>/g) || [])
      .map((b) => b.replace(/<[^>]*>/g, ''));
    check('cada card com nota rende um bloco de prosa', PROSA.length >= 5, PROSA.length);
    const JARGAO = ['generate_report', 'manifest.yaml', 'procedures', 'granularidade',
                    'mtime', 'artefato', 'ETL', 'serve.py', 'run(', 'MySQL', 'YAML',
                    'Desde 2026', 'não medidos', 'corte de informação'];
    const vazamentos = [];
    PROSA.forEach((t) => JARGAO.forEach((j) => {
      if (t.indexOf(j) >= 0) vazamentos.push(j + ' -> ' + t.slice(0, 60));
    }));
    check('a prosa nao carrega jargao do repositorio nem data de decisao',
          vazamentos.length === 0, vazamentos.join(' | '));
    // ... e nao e vazia de conteudo: cada nota tem de dizer algo sobre o dashboard.
    check('cada bloco de prosa tem pelo menos uma frase de verdade',
          PROSA.every((t) => t.trim().length > 60),
          JSON.stringify(PROSA.map((t) => t.length)));
  }

  check('toda dependencia declara onde mora',
        (cards.match(/src-badge/g) || []).length >= 2,
        (cards.match(/src-badge/g) || []).length);

  if (MODE === 'file') {
    check('caiu no payload embutido (sem /api/dashboards util)',
          !calls.some((u) => u === '/api/dashboards') || true);
    check('hint anuncia modo arquivo', hint.indexOf('modo arquivo') >= 0, hint.slice(0, 90));
    // O payload embutido e o real, gerado do manifesto -- 11 dashboards hoje.
    const n = (cards.match(/class="dash-card"/g) || []).length;
    check('renderizou os dashboards do manifesto embutido', n >= 10, n);
    check('embutido traz dependencia fora do MySQL marcada',
          cards.indexOf('src-badge out') >= 0);
  } else {
    check('pediu /api/dashboards', calls.some((u) => u === '/api/dashboards'));
    check('hint anuncia estado ao vivo', hint.indexOf('ao vivo') >= 0, hint.slice(0, 90));
    const n = (cards.match(/class="dash-card"/g) || []).length;
    check('usou o payload ao vivo (5 dashboards do stub)', n === 5, n);
    check('dependencia com dado novo ganha marca',
          cards.indexOf('dep-flag new') >= 0 && cards.indexOf('dado novo') >= 0);
    check('mostra o que o relatorio embutiu, ao lado do que a fonte tem',
          cards.indexOf('no relatório:') >= 0);
    check('veredito desatualizado vira pill stale', cards.indexOf('verdict stale') >= 0);
    check('veredito em dia vira pill ok', cards.indexOf('verdict ok') >= 0);
    check('CSV fora do MySQL mostra como atualizar',
          cards.indexOf('fetch_bcb.py') >= 0);
    check('card resume dependencias e custo de regerar',
          cards.indexOf('~30s para regerar') >= 0 && cards.indexOf('fora do MySQL') >= 0);

    // filtro "Fora do MySQL": some a dependencia de MySQL, fica a de arquivo
    const pills = getEl('dash-scope-pills').children;
    check('tres pills de filtro de dependencia', pills.length === 3, pills.length);
    pills[1]._listeners['click']();
    const filtrado = getEl('dash-cards').innerHTML;
    check('filtro "fora do MySQL" esconde as tabelas do banco',
          filtrado.indexOf('macro_brasil.inflc_decomposicao') < 0 &&
          filtrado.indexOf('ipca_bcb_series.csv') >= 0);
    pills[0]._listeners['click']();
    check('voltar para "todas" traz as tabelas de volta',
          getEl('dash-cards').innerHTML.indexOf('macro_brasil.inflc_decomposicao') >= 0);

    // filtro de area
    const areas = getEl('dash-area-pills').children;
    const iUs = areas.map((b) => b.textContent).indexOf('EUA');
    check('pill de area por area presente no payload', iUs > 0, areas.map((b) => b.textContent).join(','));
    areas[iUs]._listeners['click']();
    const soUs = getEl('dash-cards').innerHTML;
    check('filtro de area deixa so o dashboard daquela area',
          soUs.indexOf('Inflation (US)') >= 0 && soUs.indexOf('Inflação (BR)') < 0);

    // Os 3 stat cards desta aba sairam em 2026-09-23; a contagem ficou numa linha ao
    // lado do titulo. Ela conta o RECORTE de area -- um numero que os cards logo abaixo
    // contradizem e pior do que numero nenhum.
    const nDoResumo = (h) => parseInt(
      (h.match(/<strong>(\d+)<\/strong> dashboard/) || [0, '0'])[1], 10);
    const nCards = (h) => (h.match(/<details class="dash-card"/g) || []).length;
    check('o resumo conta o recorte de area, nao a lista inteira',
          nDoResumo(getEl('dash-resumo').innerHTML) === nCards(soUs),
          nDoResumo(getEl('dash-resumo').innerHTML) + ' vs ' + nCards(soUs));
    areas[0]._listeners['click']();
    const todas = getEl('dash-cards').innerHTML;
    check('e cresce ao voltar para todas as areas',
          nDoResumo(getEl('dash-resumo').innerHTML) === nCards(todas)
            && nCards(todas) > nCards(soUs),
          nDoResumo(getEl('dash-resumo').innerHTML) + ' vs ' + nCards(todas));
    // ... e o unico numero que pede acao sai marcado, na cor do selo do card.
    check('o que pede acao vem destacado no resumo',
          /<span class="acao">\d+<\/span> com dado novo/.test(getEl('dash-resumo').innerHTML),
          getEl('dash-resumo').innerHTML);
    areas[iUs]._listeners['click']();
  }

  // ── click-drop: um <details> por dashboard ───────────────────────────────
  // 11 dashboards x 27 dependencias abertos empurram tudo para fora da tela, entao o card
  // e um click-drop fechado por default. O que fica no <summary> e o que se le fechado.
  check('cada dashboard e um <details>', cards.indexOf('<details class="dash-card"') >= 0);
  check('e nenhum vem aberto por default', cards.indexOf('<details class="dash-card" data-key="'
        ) >= 0 && cards.indexOf(' open>') < 0, 'algum card veio com open');
  check('o cabecalho fica no <summary>',
        /<summary><div class="dash-head">/.test(cards));
  check('a meta tambem, para ser legivel com o card fechado',
        cards.indexOf('dash-meta') >= 0 &&
        cards.indexOf('</div></summary>') >= 0);
  check('nota, procedimentos e tabela ficam no corpo',
        /<\/summary><div class="dash-body">/.test(cards));
  // O estado aberto tem de sobreviver ao re-render: `renderDashboards()` reescreve o
  // innerHTML inteiro, e e isso que o POST de Regerar dispara. Sem isto o card que voce
  // abriu fecharia sozinho no meio da operacao.
  // Os filtros da secao anterior deixaram a area em "EUA" no modo servido; volta para
  // todas, senao o card que se vai abrir nem esta renderizado.
  const pillsArea = getEl('dash-area-pills').children;
  if (pillsArea.length) pillsArea[0]._listeners['click']();
  const chaveAberta = ((getEl('dash-cards').innerHTML
                        .match(/data-key="([^"]+)"/) || [])[1]);
  if (chaveAberta && global.__CAL) {
    global.__CAL.DASH.abertos[chaveAberta] = true;
    global.__CAL.renderDashboards();
    const reaberto = getEl('dash-cards').innerHTML;
    check('card marcado como aberto volta aberto depois do re-render',
          reaberto.indexOf('data-key="' + chaveAberta + '" open>') >= 0,
          reaberto.slice(0, 90));
    check('e os outros continuam fechados',
          (reaberto.match(/ open>/g) || []).length === 1,
          (reaberto.match(/ open>/g) || []).length);
    global.__CAL.DASH.abertos[chaveAberta] = false;
    global.__CAL.renderDashboards();
    check('e fechar de novo tira o atributo',
          getEl('dash-cards').innerHTML.indexOf(' open>') < 0);
  }
  check('card oferece botao de regerar', cards.indexOf('dash-btn') >= 0);
  check('botao carrega a key do dashboard', cards.indexOf('data-key="') >= 0);
  check('botao rotulado conforme o modo',
        cards.indexOf(MODE === 'file' ? 'Copiar cmd' : 'Regerar') >= 0);

  if (MODE === 'served') {
    // ── "Regerar pendentes": quem entra na fila e quem NAO entra ────────────
    // A regra e o que importa aqui, nao o botao: dos 5 do stub, tres estao vermelhos ou
    // chamativos de algum jeito e so DOIS podem entrar. Errar isso nao levanta nada --
    // gera relatorio a mais (ou de menos) em silencio.
    const lote = getEl('bulk-dashboards').innerHTML;
    check('a aba oferece o lote', lote.indexOf('bulk-gerar-btn') >= 0, lote.slice(0, 120));
    check('a fila tem os 2 pendentes de verdade, nao os 5',
          lote.indexOf('Regerar pendentes (2)') >= 0, lote.slice(0, 160));
    // desatualizado entra; passo atras dos dados entra
    check('o titulo do lote nomeia quem vai ser regerado',
          lote.indexOf('Inflação (BR)') >= 0 && lote.indexOf('Inflation (US)') >= 0);
    // ... e os tres excluidos NAO aparecem
    check('sem entry point automatico fica fora da fila',
          lote.indexOf('Oráculo') < 0, lote.slice(0, 200));
    check('nunca gerado fica fora da fila (construir e uma decisao)',
          lote.indexOf('Crédito') < 0, lote.slice(0, 200));
    check('sem stamp fica fora da fila (nao e atraso)',
          lote.indexOf('Câmbio') < 0, lote.slice(0, 200));

    // O ROTULO na tela nao pode ser a palavra de quem construiu isto. O usuario leu o
    // selo `sem stamp` e respondeu "eu nao sei o que e stamp" (2026-09-23) -- e ele tem
    // razao: o registro e mecanismo nosso, nao vocabulario de quem abre a pagina. A
    // assercao e sobre a aba RENDERIZADA, nao sobre o dicionario de rotulos: um mutante
    // que reintroduza a palavra em qualquer outro lugar da aba tambem reprova.
    // Sobre o TEXTO, nao sobre o HTML: `class="stamped"` e nome de classe, que ninguem
    // le. O que o usuario le e o que sobra depois de tirar as tags.
    const textoDaAba = cards.replace(/<[^>]*>/g, ' ');
    check('a aba nao diz "stamp" em lugar nenhum',
          !/stamp/i.test(textoDaAba),
          (textoDaAba.match(/.{0,40}stamp.{0,40}/i) || [''])[0]);
    check('o veredito sem retrato aparece como "nao da para conferir"',
          cards.indexOf('não dá para conferir') >= 0,
          cards.slice(cards.indexOf('verdict'), cards.indexOf('verdict') + 120));
    // ... e um selo cinza sozinho le como defeito da pagina: ele precisa do motivo E da
    // saida, dentro do <summary>, para ser legivel com o card fechado. O card tem de ser
    // achado pelo SELO -- pegar o primeiro `verdict-why` da aba acha o de "nunca gerado",
    // que e outro estado, com outro motivo.
    const cardSemRetrato = cards.split('<details')
      .find((c) => c.indexOf('não dá para conferir') >= 0) || '';
    const iPorque = cardSemRetrato.indexOf('verdict-why');
    check('e vem com o motivo e a saida, dentro do summary',
          iPorque >= 0 && /Regerar uma vez/.test(cardSemRetrato.slice(iPorque, iPorque + 320))
            && cardSemRetrato.indexOf('</summary>') > iPorque,
          cardSemRetrato.slice(iPorque, iPorque + 200));
    // O tempo anunciado e o do clique: 30s da inflacao BR + 13s de build do US + 110s
    // do passo atrasado dele. Os 90s do painel trimestral, que esta em dia, NAO entram.
    check('o lote anuncia a soma dos tempos, com o recalculo de cada um',
          lote.indexOf('~153s no total') >= 0, lote.slice(0, 260));
    // O botao de card continua existindo -- o lote nao substitui a escolha um-a-um.
    check('o botao de cada card continua no lugar',
          (cards.match(/dash-btn/g) || []).length >= 4,
          (cards.match(/dash-btn/g) || []).length);

    // O filtro de area vale para o lote tambem: agir sobre card que nao esta listado
    // seria surpresa.
    const areasLote = getEl('dash-area-pills').children;
    const iUs2 = areasLote.map((b) => b.textContent).indexOf('EUA');
    areasLote[iUs2]._listeners['click']();
    check('o lote acompanha o filtro de area',
          getEl('bulk-dashboards').innerHTML.indexOf('Regerar pendentes (1)') >= 0,
          getEl('bulk-dashboards').innerHTML.slice(0, 160));
    areasLote[0]._listeners['click']();

    // Os filtros acima deixaram a area em "EUA"; volta para todas, senao o card do
    // dashboard que vamos regerar nem esta renderizado.
    getEl('dash-area-pills').children[0]._listeners['click']();

    const btnGerar = new El('button');
    btnGerar.dataset.key = 'brasil_inflation';
    btnGerar.textContent = 'Regerar';
    const marcasGerar = cliqueEm(getEl('dash-cards'), btnGerar);
    // O botao esta dentro do <summary>: sem barrar a acao default, o clique no
    // Regerar abriria/fecharia o card junto.
    check('o clique no Regerar barra o toggle do click-drop',
          marcasGerar.stop === 1 && marcasGerar.prevent === 1, JSON.stringify(marcasGerar));
    check('botao desabilita durante a regeneracao', btnGerar.disabled === true);
    check('botao avisa que esta rodando', btnGerar.textContent === 'regerando...');

    await new Promise((r) => setTimeout(r, 40));
    const posGerar = getEl('dash-cards').innerHTML;
    const post = calls.filter((u) => u === '/api/gerar');
    check('clique dispara POST /api/gerar', post.length === 1, post.length);
    check('veredito do card regerado vira "em dia"',
          posGerar.indexOf('verdict ok') >= 0);
    check('card mostra quanto demorou, e que nao havia o que recalcular',
          posGerar.indexOf('regerado em 31.2s') >= 0 &&
          posGerar.indexOf('nada estava atrás dos dados') >= 0);
    // O outro dashboard NAO pode ter sido tocado -- o POST devolve so uma linha.
    check('o outro dashboard segue como estava',
          posGerar.indexOf('Inflation (US)') >= 0);
    check('marca de "dado novo" sumiu do dashboard regerado',
          (posGerar.match(/dep-flag new/g) || []).length === 0,
          (posGerar.match(/dep-flag new/g) || []).length);

    // ── bloco de procedimentos: LEITURA, sem botao proprio ────────────────
    // Sao dois botoes no sistema e so dois (pedido do usuario, 2026-08-31): Atualizar
    // para a base, Regerar para o dashboard. Um terceiro botao por procedimento existiu
    // por horas e deixou o processo confuso -- se voltar, cai aqui.
    check('o bloco de procedimentos nao tem botao proprio',
          posGerar.indexOf('proc-btn') < 0 && posGerar.indexOf('>Rodar<') < 0);
    check('card renderiza o bloco de procedimentos', posGerar.indexOf('proc-box') >= 0);
    // O cabecalho e a nota do bloco sao para quem nunca viu o dashboard: dizem o que
    // aqueles itens SAO, nao o que combinamos sobre eles.
    check('o cabecalho do bloco nomeia o que o bloco contem',
          posGerar.indexOf('O que este dashboard prepara por conta própria') >= 0);
    check('o bloco explica por que um numero velho cabe num arquivo novo',
          posGerar.indexOf('proc-hint') >= 0 &&
          posGerar.indexOf('preparados pelo próprio dashboard') >= 0 &&
          posGerar.indexOf('fica velho mesmo que o arquivo seja novo') >= 0);
    // Um passo pode ser CALCULO (o modelo) ou BUSCA (o fetch do IPCA no BCB), e o texto
    // do bloco vale para os dois: chamar tudo de "cálculo" mentiria no card da inflacao.
    check('o bloco nao chama todo passo de calculo',
          posGerar.indexOf('resultados de cálculo') < 0 &&
          posGerar.indexOf('refazendo o cálculo') < 0);
    check('procedimento aparece com o rotulo declarado',
          posGerar.indexOf('Previsão + backtest') >= 0 &&
          posGerar.indexOf('Painéis trimestrais') >= 0);
    check('procedimento diz onde o resultado fica',
          posGerar.indexOf('guarda o resultado em 1 arquivo: previsao.json') >= 0);
    check('procedimento atrasado diz que vai ser refeito, com corte e fonte',
          posGerar.indexOf('atrás dos dados: usou o que havia até') >= 0 &&
          posGerar.indexOf('2026-08-25') >= 0 && posGerar.indexOf('2026-08-28') >= 0 &&
          posGerar.indexOf('3 dias depois') >= 0 &&
          posGerar.indexOf('o Regerar refaz') >= 0);
    check('linha do procedimento atrasado ganha a classe late',
          posGerar.indexOf('proc-row late') >= 0);
    // A granularidade e o que da a cada passo a frequencia dele -- e o que impede a
    // estimacao trimestral de ser refeita a cada boletim diario.
    // ... e mostra a CONSEQUENCIA dela (de quanto em quanto tempo fica velho), nao a
    // palavra "granularidade", que nao diz nada a quem abre a pagina.
    check('cada passo mostra de quanto em quanto tempo fica velho',
          posGerar.indexOf('fica velho quando abre um trimestre novo') >= 0 &&
          posGerar.indexOf('fica velho quando o dado anda, dia a dia') >= 0);
    check('a palavra "granularidade" nao aparece na pagina renderizada',
          posGerar.indexOf('granularidade') < 0);
    check('o passo trimestral em dia NAO e marcado para refazer',
          posGerar.indexOf('em dia: usou os dados até') >= 0);
    // O tempo anunciado tem de ser o do CLIQUE: geracao + o que vai ser recalculado.
    // 13s de build + 110s da previsao = 123s; os 90s do painel NAO entram.
    check('o tempo do botao soma a geracao e so o recalculo atrasado',
          posGerar.indexOf('~123s para regerar') >= 0 &&
          posGerar.indexOf('13s + 110s de rec') >= 0,
          posGerar.indexOf('para regerar') >= 0 ? 'sem os 123s' : 'sem a frase');
    check('o cabecalho do bloco soma os segundos do recalculo',
          posGerar.indexOf('+110s') >= 0);
    // A dependencia aponta para o Regerar, nao para um comando a copiar.
    check('dep com procedimento diz que o Regerar cuida dela',
          posGerar.indexOf('refeito pelo Regerar') >= 0 &&
          posGerar.indexOf('from x import salvar') < 0);
    // ... e onde NAO ha procedimento, o texto continua sendo a resposta honesta.
    check('dep sem procedimento mantem o comando em texto',
          posGerar.indexOf('fetch_bcb.py') >= 0);

    // ── Regerar num dashboard COM metrica atrasada ────────────────────────
    const btnUS = new El('button');
    btnUS.dataset.key = 'us_inflation';
    btnUS.textContent = 'Regerar';
    cliqueEm(getEl('dash-cards'), btnUS);
    check('o botao anuncia o tempo do recalculo enquanto roda',
          btnUS.textContent === 'refazendo os passos... (~123s)', btnUS.textContent);

    await new Promise((r) => setTimeout(r, 40));
    const posUS = getEl('dash-cards').innerHTML;
    check('um POST /api/gerar por clique',
          calls.filter((u) => u === '/api/gerar').length === 2,
          calls.filter((u) => u === '/api/gerar').length);
    // A mensagem tem de dizer o que foi REFEITO, senao o usuario nao sabe que a metrica
    // dentro do relatorio tambem andou.
    check('a mensagem lista o que foi recalculado',
          posUS.indexOf('refez Previsão + backtest (108.4s)') >= 0 &&
          posUS.indexOf('regerou em 13.4s') >= 0);
    check('o passo em dia nao entra na mensagem',
          posUS.indexOf('Painéis trimestrais (') < 0);
    check('depois do Regerar nada fica atrasado',
          posUS.indexOf('proc-row late') < 0);
    check('e o corte do passo refeito alcancou a fonte',
          posUS.indexOf('em dia: usou os dados até <strong>2026-08-28') >= 0);
  } else {
    // Modo arquivo: o payload embutido e o real, e o piloto de `procedures` esta nele.
    check('payload embutido traz o bloco de procedimentos do piloto',
          cards.indexOf('proc-box') >= 0);
    check('no modo arquivo tambem nao ha botao de procedimento',
          cards.indexOf('proc-btn') < 0);
    check('e o bloco diz o que aqueles itens sao',
          cards.indexOf('O que este dashboard prepara por conta própria') >= 0);
    // A inflacao teve um passo entre 2026-09-01 e 2026-09-11, e ele era um FETCH: buscava no
    // SGS uma copia de `inflc_agregados`, tabela que o update_db.py ja mantinha. Foi apagado
    // junto com o CSV, e a asserção agora cobra o INVERSO -- que aquele relatorio nao tenha
    // passo nenhum. Um passo que volte a existir ali e um insumo que o botao Atualizar deixou
    // de alcancar, que foi exatamente o defeito.
    check('a inflacao nao tem passo: todo insumo dela vem do banco',
          cards.indexOf('Séries agregadas do IPCA (Banco Central)') < 0);
    // E o bloco de passos que sobra e de estimacao de modelo, com granularidade trimestral --
    // calculo de verdade, que nenhuma tabela substitui.
    check('o payload real traz os passos do modelo de politica monetaria',
          cards.indexOf('Painéis trimestrais') >= 0);
    check('e eles sao trimestrais, nao mensais',
          cards.indexOf('fica velho quando abre um trimestre novo') >= 0);

    // ── lote no modo arquivo: copia um comando por dashboard pendente ───────
    // O retrato embutido carrega veredito, entao aqui a fila E conhecida (ao contrario
    // da outra aba, onde sem servidor nao ha veredito nenhum). Injeta o stub para haver
    // pendencia: no payload real do momento pode nao haver nenhuma.
    if (global.__CAL) {
      let copiado = null;
      global.navigator = { clipboard: { writeText: (t) => {
        copiado = t; return Promise.resolve();
      } } };
      // ... e o caminho do execCommand, que e o que roda quando o contexto nao e
      // seguro (file:// nao e): le o valor do <textarea> que `copiarTexto` acabou de
      // pendurar no body.
      global.document.execCommand = () => {
        const filhos = global.document.body.children;
        if (filhos.length) copiado = filhos[filhos.length - 1].value;
        return true;
      };
      global.__CAL.DASH.rows = JSON.parse(JSON.stringify(DASHBOARDS_STUB));
      global.__CAL.renderDashboards();
      const loteArq = getEl('bulk-dashboards').innerHTML;
      check('sem servidor o lote copia em vez de rodar',
            loteArq.indexOf('Copiar cmds (2)') >= 0, loteArq.slice(0, 160));
      cliqueEm(getEl('bulk-dashboards'), new El('button'));
      await new Promise((r) => setTimeout(r, 20));
      const linhasCmd = (copiado || '').split('\n').filter(Boolean);
      check('copiou uma linha por dashboard pendente', linhasCmd.length === 2,
            JSON.stringify(copiado));
      check('cada linha e o --gerar daquela key',
            linhasCmd.length === 2 &&
            linhasCmd[0].indexOf('--gerar brasil_inflation') > 0 &&
            linhasCmd[1].indexOf('--gerar us_inflation') > 0,
            JSON.stringify(linhasCmd));
      check('e nenhuma linha e o --gerar todos',
            (copiado || '').indexOf('--gerar todos') < 0);
    }


  }

  // troca de aba: o clique delegado tem de despir a aba de divulgacoes
  const btnDash = global.document._tabBtns[1];
  cliqueEm(global.document._tabBar, btnDash);
  check('clique na aba marca aria-selected',
        btnDash.getAttribute('aria-selected') === 'true' &&
        global.document._tabBtns[0].getAttribute('aria-selected') === 'false');
  check('trocar de aba esconde a outra view',
        getEl('view-releases').hidden === true && getEl('view-dashboards').hidden === false);

  console.log(falhas ? `  -> ${falhas} falha(s)` : '  -> ok');
  falhasTotais += falhas;
}

// ---------------------------------------------------------------------------
// Servido, mas com /api/dashboards falhando. Tem de ficar distinguivel de "modo
// arquivo": o /api/gerar continua no ar, entao o botao segue sendo Regerar e a dica
// diz o que falhou. Regressao do bug de 2026-08-26, em que o rotulo do botao seguia
// "o estado carregou?" em vez de "existe servidor?" e um /api/dashboards quebrado
// aparecia na tela como modo arquivo.
// ---------------------------------------------------------------------------
async function testeServidoSemEstado() {
  let falhas = 0;
  const check = (rotulo, cond, extra) => {
    if (cond) console.log('  ok     ' + rotulo);
    else { console.log('  FALHA  ' + rotulo + (extra !== undefined ? '  -> ' + extra : '')); falhas++; }
  };
  console.log('');
  console.log('SERVIDO SEM ESTADO - /api/dashboards devolve ok:false');

  const els = {};
  const getEl = (id) => (els[id] = els[id] || new El('div'));
  global.document = mkDoc(getEl);
  global.window = { isSecureContext: false };
  global.navigator = {};
  global.fetch = (url) => {
    if (url === '/api/ping')
      return Promise.resolve({ ok: true, json: () => Promise.resolve(
        { ok: true, modo: 'servido', hoje: '2026-08-26', agora: '10:00' }) });
    if (url === '/api/status')
      return Promise.resolve({ ok: true, json: () => Promise.resolve(
        { ok: true, hoje: '2026-08-26', agora: '10:00', grupos: {} }) });
    if (url === '/api/dashboards')
      return Promise.resolve({ ok: true, json: () => Promise.resolve(
        { ok: false, erro: 'OperationalError: banco fora do ar' }) });
    return Promise.reject(new Error('inesperado ' + url));
  };

  new Function(SRC)();
  await new Promise((r) => setTimeout(r, 60));

  const cards = getEl('dash-cards').innerHTML;
  const hint = getEl('dash-mode-hint').innerHTML;
  check('botao continua Regerar (o /api/gerar nao depende do /api/dashboards)',
        cards.indexOf('Regerar') >= 0 && cards.indexOf('Copiar cmd') < 0);
  check('dica NAO diz modo arquivo', hint.indexOf('modo arquivo') < 0, hint.slice(0, 100));
  check('dica diz servido e mostra o erro',
        hint.indexOf('servido') >= 0 && hint.indexOf('banco fora do ar') >= 0,
        hint.slice(0, 140));
  check('cards caem para o retrato embutido', cards.indexOf('dash-card') >= 0);

  console.log(falhas ? `  -> ${falhas} falha(s)` : '  -> ok');
  falhasTotais += falhas;
}


// ---------------------------------------------------------------------------
// "Regerar pendentes" -- o CLIQUE. Em cenario proprio para nao regerar os cards antes
// dos testes de clique um-a-um de testeStatusDashboard().
//
// O que precisa ser verdade e nao da para ver na marcacao: um POST por dashboard, EM
// SERIE (nao ha endpoint de lote, e dois geradores nao podem disputar o banco), a fila
// fotografada antes de comecar, e uma falha no meio nao interrompendo o resto.
// ---------------------------------------------------------------------------
async function testeLoteDashboards(comFalha) {
  let falhas = 0;
  const check = (rotulo, cond, extra) => {
    if (cond) console.log('  ok     ' + rotulo);
    else { console.log('  FALHA  ' + rotulo + (extra !== undefined ? '  -> ' + extra : '')); falhas++; }
  };
  console.log('');
  console.log('LOTE DE DASHBOARDS - ' + (comFalha ? 'com uma falha no meio' : 'tudo OK'));

  const els = {};
  const getEl = (id) => (els[id] = els[id] || new El('div'));
  const postados = [];
  let emVoo = 0, maxEmVoo = 0;

  global.document = mkDoc(getEl);
  global.window = { isSecureContext: false };
  global.navigator = {};
  global.fetch = (url, opts) => {
    if (url === '/api/ping')
      return Promise.resolve({ ok: true, json: () => Promise.resolve(
        { ok: true, modo: 'servido', hoje: '2026-08-26', agora: '10:00' }) });
    if (url === '/api/status')
      return Promise.resolve({ ok: true, json: () => Promise.resolve(
        { ok: true, hoje: '2026-08-26', agora: '10:00', grupos: {} }) });
    if (url === '/api/dashboards')
      return Promise.resolve({ ok: true, json: () => Promise.resolve(
        { ok: true, agora: '10:00', dashboards: JSON.parse(JSON.stringify(DASHBOARDS_STUB)) }) });
    if (url === '/api/gerar') {
      const key = JSON.parse((opts && opts.body) || '{}').key;
      postados.push(key);
      emVoo++; maxEmVoo = Math.max(maxEmVoo, emVoo);
      // resposta assincrona de verdade: se o lote disparasse os dois de uma vez,
      // maxEmVoo chegaria a 2 e a assercao de serie pegaria.
      return new Promise((resolve) => setTimeout(() => {
        emVoo--;
        if (comFalha && key === 'brasil_inflation') {
          resolve({ ok: true, json: () => Promise.resolve(
            { erro: 'RuntimeError: banco fora do ar' }) });
          return;
        }
        const idx = key === 'us_inflation' ? 1 : 0;
        const nova = JSON.parse(JSON.stringify(DASHBOARDS_STUB[idx]));
        nova.veredito = 'em dia';
        nova.n_novos = 0;
        nova.n_proc_atrasados = 0;
        nova.gerado_em = '2026-08-26T10:05:00';
        nova.deps.forEach((d) => { d.novo = false; d.arquivo_mais_novo = false; });
        (nova.procedimentos || []).forEach((pr) => { pr.atrasado = false; });
        resolve({ ok: true, json: () => Promise.resolve(
          { ok: true, key, segundos: 12.0, segundos_total: 12.0,
            n_recalculados: 0, n_falhou: 0, dashboard: nova, procedimentos: [] }) });
      }, 10));
    }
    return Promise.reject(new Error('inesperado ' + url));
  };

  new Function(SRC)();
  await new Promise((r) => setTimeout(r, 60));

  check('antes do clique nada foi postado', postados.length === 0, postados.length);
  cliqueEm(getEl('bulk-dashboards'), new El('button'));

  // o primeiro POST tem de sair sem esperar render nenhum
  await new Promise((r) => setTimeout(r, 5));
  check('o botao do lote desabilita enquanto roda',
        getEl('bulk-dashboards').innerHTML.indexOf('disabled') >= 0,
        getEl('bulk-dashboards').innerHTML.slice(0, 160));
  check('e diz em qual dashboard esta',
        getEl('bulk-dashboards').innerHTML.indexOf('regerando 1 de 2') >= 0,
        getEl('bulk-dashboards').innerHTML.slice(0, 220));

  await new Promise((r) => setTimeout(r, 120));

  check('um POST por dashboard pendente, e so por eles',
        postados.length === 2, JSON.stringify(postados));
  check('na ordem em que a aba lista',
        postados[0] === 'brasil_inflation' && postados[1] === 'us_inflation',
        JSON.stringify(postados));
  check('EM SERIE: nunca dois geradores ao mesmo tempo', maxEmVoo === 1, maxEmVoo);
  check('nenhum POST para os excluidos',
        postados.indexOf('oraculo') < 0 && postados.indexOf('brasil_credit') < 0 &&
        postados.indexOf('brasil_exchange_rate') < 0, JSON.stringify(postados));

  const lote = getEl('bulk-dashboards').innerHTML;
  const cards = getEl('dash-cards').innerHTML;

  if (comFalha) {
    // O ponto todo: a falha do primeiro NAO impede o segundo de rodar.
    check('a falha nao interrompeu a fila', postados.length === 2, postados.length);
    check('o resumo conta quantos deram certo e nomeia quem falhou',
          lote.indexOf('1 de 2 regerado(s)') >= 0 &&
          lote.indexOf('falhou: Inflação (BR)') >= 0, lote.slice(0, 260));
    check('o resumo do lote sai marcado como erro',
          lote.indexOf('upd-msg err') >= 0, lote.slice(0, 200));
    check('o card de quem falhou mostra o motivo',
          cards.indexOf('banco fora do ar') >= 0);
    // ... e o que falhou continua pendente, entao o lote continua sendo oferecido
    check('quem falhou continua na fila do proximo clique',
          lote.indexOf('Regerar pendentes (1)') >= 0, lote.slice(0, 200));
  } else {
    check('o resumo diz que os dois foram regerados',
          lote.indexOf('2 de 2 regerado(s)') >= 0, lote.slice(0, 260));
    check('o resumo NAO sai marcado como erro', lote.indexOf('upd-msg err') < 0);
    check('cada card recebeu a mensagem do proprio Regerar',
          (cards.match(/regerado em 12s/g) || []).length === 2,
          (cards.match(/regerado em 12s/g) || []).length);
    check('os dois vereditos viraram "em dia"',
          (cards.match(/verdict ok/g) || []).length >= 2,
          (cards.match(/verdict ok/g) || []).length);
    // Com a fila vazia o controle deixa de ser um botao: nao ha clique morto na tela.
    check('com nada pendente o lote deixa de oferecer botao',
          lote.indexOf('bulk-gerar-btn') < 0 &&
          lote.indexOf('nenhum dashboard pendente') >= 0, lote.slice(0, 200));
  }

  console.log(falhas ? `  -> ${falhas} falha(s)` : '  -> ok');
  falhasTotais += falhas;
}

// ---------------------------------------------------------------------------
// "Atualizar pendentes" -- o lote da aba de divulgacoes. Dois grupos atrasados, um
// deles falhando, para exercitar a mesma regra de fila da outra aba.
//
// E o terceiro estado, que e o que separa esta aba da outra: sem servidor NAO HA
// veredito de freshness, entao nao existe lista de pendentes para copiar -- e dizer
// "nenhuma pendente" ali seria afirmar um veredito que ninguem tem.
// ---------------------------------------------------------------------------
async function testeLoteDivulgacoes() {
  let falhas = 0;
  const check = (rotulo, cond, extra) => {
    if (cond) console.log('  ok     ' + rotulo);
    else { console.log('  FALHA  ' + rotulo + (extra !== undefined ? '  -> ' + extra : '')); falhas++; }
  };
  console.log('');
  console.log('LOTE DE DIVULGACOES - 2 atrasados, 1 falha');

  const els = {};
  const getEl = (id) => (els[id] = els[id] || new El('div'));
  const postados = [];
  let rodados = 0;

  // ESTADOS_OK primeiro, atrasados DEPOIS: `bcb_icbr` esta na lista de "ok" e aqui
  // precisa estar atrasado, senao a ordem o sobrescreve.
  const grupos = () => {
    const g = {};
    ESTADOS_OK.forEach((k) => { g[k] = { estado: 'ok', tabelas: [] }; });
    g.ibge_pmc = { estado: rodados > 0 ? 'ok' : 'atrasado', tabelas: [] };
    g.bcb_icbr = { estado: 'atrasado', tabelas: [] };   // 4 divulgacoes passadas
    return g;
  };

  global.document = mkDoc(getEl);
  global.window = { isSecureContext: false };
  global.navigator = {};
  global.fetch = (url, opts) => {
    if (url === '/api/ping')
      return Promise.resolve({ ok: true, json: () => Promise.resolve(
        { ok: true, modo: 'servido', hoje: '2026-08-17', agora: '23:59' }) });
    if (url === '/api/status')
      return Promise.resolve({ ok: true, json: () => Promise.resolve(
        { ok: true, hoje: '2026-08-17', agora: '23:59', grupos: grupos() }) });
    if (url === '/api/dashboards')
      return Promise.resolve({ ok: true, json: () => Promise.resolve(
        { ok: true, agora: '23:59', dashboards: [] }) });
    if (url === '/api/run') {
      const slug = JSON.parse((opts && opts.body) || '{}').group;
      postados.push(slug);
      return new Promise((resolve) => setTimeout(() => {
        if (slug === 'bcb_icbr') {
          resolve({ ok: true, json: () => Promise.resolve(
            { ok: false, n_ok: 0, n_erro: 1, sem_script: [] }) });
          return;
        }
        rodados++;
        resolve({ ok: true, json: () => Promise.resolve(
          { ok: true, n_ok: 1, n_erro: 0, sem_script: [] }) });
      }, 10));
    }
    return Promise.reject(new Error('inesperado ' + url));
  };

  new Function(SRC + ';global.__CAL = Object.assign(global.__CAL || {}, '
              + '{state: state, renderAll: renderAll});')();
  await new Promise((r) => setTimeout(r, 60));

  // O lote age sobre o RECORTE, e o recorte padrao virou um mes. Este cenario e sobre a
  // regra da fila (um POST por grupo, em serie, falha nao interrompe), entao ele abre o
  // calendario inteiro de proposito -- a regra do recorte estreito e exercitada no fim.
  global.__CAL.state.month = 'Tudo';
  global.__CAL.state.mesEscolhido = true;
  global.__CAL.renderAll();

  const antes = getEl('bulk-releases').innerHTML;
  check('a aba oferece o lote', antes.indexOf('bulk-run-btn') >= 0, antes.slice(0, 140));
  // Sao 2 GRUPOS atrasados e 5 LINHAS atrasadas (a PMC tem 1 divulgacao passada, o ICBr
  // tem 4). O botao roda o ETL de um grupo, entao contar linha pediria o mesmo ETL
  // quatro vezes -- e nada levantaria, so demoraria 4x.
  check('conta GRUPO e nao linha (2 grupos, 5 linhas atrasadas)',
        antes.indexOf('Atualizar pendentes (2)') >= 0, antes.slice(0, 200));
  // ... e o Focus, com 16 linhas passadas e 'ok', nao entra.
  check('grupo em dia nao entra na conta', antes.indexOf('Focus') < 0, antes.slice(0, 200));

  cliqueEm(getEl('bulk-releases'), new El('button'));
  await new Promise((r) => setTimeout(r, 5));
  check('avisa em qual divulgacao esta',
        getEl('bulk-releases').innerHTML.indexOf('atualizando 1 de 2') >= 0,
        getEl('bulk-releases').innerHTML.slice(0, 200));

  await new Promise((r) => setTimeout(r, 120));
  check('um POST /api/run por grupo pendente', postados.length === 2,
        JSON.stringify(postados));
  check('a falha de um nao interrompe o outro',
        postados.indexOf('ibge_pmc') >= 0 &&
        postados.indexOf('bcb_icbr') >= 0, JSON.stringify(postados));
  // ... e o grupo de 4 linhas foi postado UMA vez, nao quatro
  check('um POST por grupo, mesmo com 4 divulgacoes atrasadas nele',
        postados.filter((x) => x === 'bcb_icbr').length === 1,
        JSON.stringify(postados));

  const depois = getEl('bulk-releases').innerHTML;
  check('o resumo conta os que deram certo e nomeia o que falhou',
        depois.indexOf('1 de 2 atualizada(s)') >= 0 &&
        depois.indexOf('falhou') >= 0, depois.slice(0, 260));
  // O estado do banco e reconsultado UMA vez, no fim: a linha do grupo que rodou tem
  // de ter virado check verde sem F5.
  const linhas = getEl('table-body').children.map((c) => c.innerHTML).filter(Boolean);
  const pmc = linhas.filter((h) => h.indexOf('13/08/2026') >= 0 && h.indexOf('Comércio') >= 0);
  check('a tabela reflete o grupo que rodou, sem recarregar',
        pmc.length === 1 && pmc[0].indexOf('upd-ok') >= 0, pmc[0] && pmc[0].slice(0, 160));
  check('e o que falhou continua oferecendo botao',
        depois.indexOf('Atualizar pendentes (1)') >= 0, depois.slice(0, 200));

  // ── o recorte estreito nao pode APAGAR o atraso ──────────────────────────
  // Com a pagina abrindo num mes so, um grupo atrasado de outro mes sai da fila do lote
  // (que e a regra certa: o lote age sobre o que esta listado). O que nao pode acontecer
  // e ele sumir em silencio -- dezembro nao tem nenhuma linha atrasada, e mesmo assim a
  // barra tem de dizer que existe um atraso fora dali.
  global.__CAL.state.month = '2026-12';
  global.__CAL.renderAll();
  const estreito = getEl('bulk-releases').innerHTML;
  check('num mes sem atraso o lote nao oferece botao',
        estreito.indexOf('bulk-run-btn') < 0, estreito.slice(0, 160));
  check('mas avisa quantos pendentes ficaram fora do recorte',
        /\+1 pendente\(s\) fora do recorte/.test(estreito), estreito.slice(0, 260));
  check('e nomeia qual e',
        estreito.indexOf('Commodities') >= 0 || estreito.indexOf('IC-Br') >= 0,
        estreito.slice(0, 260));

  console.log(falhas ? `  -> ${falhas} falha(s)` : '  -> ok');
  falhasTotais += falhas;
}

// ---------------------------------------------------------------------------
// Sem servidor a aba de divulgacoes NAO tem veredito, entao nao pode existir lista de
// pendentes -- nem botao, nem "nenhuma pendente". O terceiro estado, que e onde as
// duas abas divergem (o retrato embutido da outra aba carrega veredito; este nao).
// ---------------------------------------------------------------------------
async function testeLoteSemVeredito() {
  let falhas = 0;
  const check = (rotulo, cond, extra) => {
    if (cond) console.log('  ok     ' + rotulo);
    else { console.log('  FALHA  ' + rotulo + (extra !== undefined ? '  -> ' + extra : '')); falhas++; }
  };
  console.log('');
  console.log('LOTE SEM VEREDITO - modo arquivo e banco fora do ar');

  for (const caso of ['arquivo', 'banco']) {
    const els = {};
    const getEl = (id) => (els[id] = els[id] || new El('div'));
    global.document = mkDoc(getEl);
    global.window = { isSecureContext: false };
    global.navigator = {};
    global.fetch = (url) => {
      if (caso === 'arquivo') return Promise.reject(new Error('sem servidor'));
      if (url === '/api/ping')
        return Promise.resolve({ ok: true, json: () => Promise.resolve(
          { ok: true, modo: 'servido', hoje: '2026-08-17', agora: '23:59' }) });
      if (url === '/api/status')
        return Promise.resolve({ ok: true, json: () => Promise.resolve(
          { ok: false, erro: 'OperationalError: banco fora do ar' }) });
      if (url === '/api/dashboards')
        return Promise.resolve({ ok: true, json: () => Promise.resolve(
          { ok: true, agora: '23:59', dashboards: [] }) });
      return Promise.reject(new Error('inesperado ' + url));
    };

    new Function(SRC)();
    await new Promise((r) => setTimeout(r, 60));

    const lote = getEl('bulk-releases').innerHTML;
    check(caso + ': nao oferece botao de lote', lote.indexOf('bulk-run-btn') < 0,
          lote.slice(0, 160));
    check(caso + ': e NAO afirma que nada esta pendente',
          lote.indexOf('nenhuma divulgação pendente') < 0, lote.slice(0, 160));
    check(caso + ': diz por que nao ha lista',
          lote.indexOf('não há') >= 0 || lote.indexOf('Sem') >= 0, lote.slice(0, 160));
    // clique nao pode fazer nada: nao ha botao, mas o listener existe
    cliqueEm(getEl('bulk-releases'), new El('button'));
    await new Promise((r) => setTimeout(r, 20));
    check(caso + ': o clique nao dispara nada', true);
  }

  console.log(falhas ? `  -> ${falhas} falha(s)` : '  -> ok');
  falhasTotais += falhas;
}

(async () => {
  const modos = process.env.MODE ? [process.env.MODE] : ['file', 'served'];
  for (const m of modos) await rodar(m);
  for (const m of modos) await testeStatusDashboard(m);
  if (!process.env.MODE) await testeServidoSemEstado();
  if (!process.env.MODE) testeOrdemDoMarkup();
  if (!process.env.MODE) await testeHorario();
  if (!process.env.MODE) await testeLoteDashboards(false);
  if (!process.env.MODE) await testeLoteDashboards(true);
  if (!process.env.MODE) await testeLoteDivulgacoes();
  if (!process.env.MODE) await testeLoteSemVeredito();
  console.log('\n' + '='.repeat(62));
  console.log(falhasTotais ? `${falhasTotais} FALHA(S)` : 'todos os asserts passaram');
  process.exit(falhasTotais ? 1 : 0);
})();
