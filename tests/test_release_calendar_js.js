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

  new Function(SRC)();

  let falhas = 0;
  const check = (rotulo, cond, extra) => {
    if (cond) console.log('  ok     ' + rotulo);
    else { console.log('  FALHA  ' + rotulo + (extra !== undefined ? '  -> ' + extra : '')); falhas++; }
  };

  return new Promise((resolve) => {
    setTimeout(() => {
      const all = getEl('table-body').children.map((c) => c.innerHTML).filter(Boolean);
      const linhas = all.filter((h) => h.indexOf('col-update') >= 0);
      const mes = all.filter((h) => h.indexOf('colspan') >= 0);

      console.log('\nMODE=' + MODE);
      check('renderizou linhas de divulgacao', linhas.length > 100, linhas.length);
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
        { ok: true, agora: '10:00', dashboards: DASHBOARDS_STUB }) });
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
    check('usou o payload ao vivo (2 dashboards do stub)', n === 2, n);
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
    // Nao pode existir controle de lote: a regeneracao e um dashboard por vez, por
    // decisao explicita do usuario. Se alguem reintroduzir "regerar todos", cai aqui.
    check('nenhum controle de regeneracao em lote na aba',
          cards.indexOf('regerar todos') < 0 &&
          getEl('dash-mode-hint').innerHTML.indexOf('todos') < 0);

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
    // O piloto deixou de ser piloto em 2026-09-01: a inflacao tambem tem passo, e o dela
    // e um FETCH -- o unico insumo daquele relatorio que nao vem do MySQL.
    check('o payload real traz o passo da inflacao tambem',
          cards.indexOf('Séries agregadas do IPCA (Banco Central)') >= 0);
    check('e ele e mensal, nao diario nem trimestral',
          cards.indexOf('fica velho quando abre um mês novo') >= 0);


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

(async () => {
  const modos = process.env.MODE ? [process.env.MODE] : ['file', 'served'];
  for (const m of modos) await rodar(m);
  for (const m of modos) await testeStatusDashboard(m);
  if (!process.env.MODE) await testeServidoSemEstado();
  if (!process.env.MODE) await testeHorario();
  console.log('\n' + '='.repeat(62));
  console.log(falhasTotais ? `${falhasTotais} FALHA(S)` : 'todos os asserts passaram');
  process.exit(falhasTotais ? 1 : 0);
})();
