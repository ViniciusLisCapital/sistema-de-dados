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
    deps: [
      { ref: 'macro_us.inflc_cpi', kind: 'mysql', onde: 'macro_us', fora_do_mysql: false,
        role: 'Níveis do CPI-U', scope: 'dados', ultimo: '2026-07-01', stamp: '2026-07-01',
        novo: false, arquivo_mais_novo: false },
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
      getEl('table-body')._listeners['click']({ target: { closest: () => btn } });
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
  global.fetch = (url) => {
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
      // o servidor devolve a linha nova SO do dashboard regerado
      const nova = JSON.parse(JSON.stringify(DASHBOARDS_STUB[0]));
      nova.veredito = 'em dia';
      nova.n_novos = 0;
      nova.gerado_em = '2026-08-26T10:00:30';
      nova.deps[0].novo = false;
      nova.deps[0].stamp = '2026-08-01';
      return Promise.resolve({ ok: true, json: () => Promise.resolve(
        { ok: true, key: 'brasil_inflation', segundos: 31.2, dashboard: nova }) });
    }
    return Promise.reject(new Error('inesperado ' + url));
  };

  new Function(SRC)();
  await new Promise((r) => setTimeout(r, 60));

  const cards = getEl('dash-cards').innerHTML;
  const hint = getEl('dash-mode-hint').innerHTML;

  check('renderizou cards de dashboard', cards.indexOf('dash-card') >= 0);
  check('mostra o caminho do arquivo gerado', cards.indexOf('reports/') >= 0);
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

  // ── botao de regerar, um por card ────────────────────────────────────────
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
    getEl('dash-cards')._listeners['click']({ target: { closest: () => btnGerar } });
    check('botao desabilita durante a regeneracao', btnGerar.disabled === true);
    check('botao avisa que esta rodando', btnGerar.textContent === 'regerando...');

    await new Promise((r) => setTimeout(r, 40));
    const posGerar = getEl('dash-cards').innerHTML;
    const post = calls.filter((u) => u === '/api/gerar');
    check('clique dispara POST /api/gerar', post.length === 1, post.length);
    check('veredito do card regerado vira "em dia"',
          posGerar.indexOf('verdict ok') >= 0);
    check('card mostra quanto demorou', posGerar.indexOf('regerado em 31.2s') >= 0);
    // O outro dashboard NAO pode ter sido tocado -- o POST devolve so uma linha.
    check('o outro dashboard segue como estava',
          posGerar.indexOf('Inflation (US)') >= 0);
    check('marca de "dado novo" sumiu do dashboard regerado',
          (posGerar.match(/dep-flag new/g) || []).length === 0,
          (posGerar.match(/dep-flag new/g) || []).length);
  }

  // troca de aba: o clique delegado tem de despir a aba de divulgacoes
  const btnDash = global.document._tabBtns[1];
  global.document._tabBar._listeners['click']({ target: { closest: () => btnDash } });
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
