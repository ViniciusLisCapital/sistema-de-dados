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

const ESTADOS_OK = ['bcb_credit_note', 'bcb_icbr', 'bcb_focus', 'bcb_fiscal_statistics',
                    'bcb_external_sector_note', 'bcb_ibcbr', 'bcb_ptc', 'bcb_rpm', 'cftc_cot'];

function rodar(MODE) {
  const els = {};
  const getEl = (id) => (els[id] = els[id] || new El('div'));
  const calls = [];

  global.document = {
    getElementById: getEl,
    createElement: (t) => new El(t),
    querySelector: () => null,
    body: new El('body'),
    execCommand: () => true,
    addEventListener: () => {},
  };
  global.window = { isSecureContext: false };
  global.navigator = {};
  global.fetch = function (url, opts) {
    calls.push({ url, opts });
    if (MODE === 'file') return Promise.reject(new Error('sem servidor'));
    if (url === '/api/ping') {
      return Promise.resolve({ ok: true, json: () => Promise.resolve({ ok: true, modo: 'servido', hoje: '2026-08-17' }) });
    }
    if (url === '/api/status') {
      const grupos = { ibge_pmc: { estado: 'atrasado', tabelas: [] },
                       bcb_copom_ata: { estado: 'vazio', tabelas: [] },
                       bcb_copom: { estado: 'indefinido', tabelas: [] } };
      ESTADOS_OK.forEach((g) => { grupos[g] = { estado: 'ok', tabelas: [] }; });
      return Promise.resolve({ ok: true, json: () => Promise.resolve({ ok: true, hoje: '2026-08-17', grupos }) });
    }
    if (url === '/api/run') {
      return Promise.resolve({ ok: true, json: () => Promise.resolve({ ok: true, n_ok: 1, n_erro: 0, sem_script: [] }) });
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

(async () => {
  const modos = process.env.MODE ? [process.env.MODE] : ['file', 'served'];
  for (const m of modos) await rodar(m);
  console.log('\n' + '='.repeat(62));
  console.log(falhasTotais ? `${falhasTotais} FALHA(S)` : 'todos os asserts passaram');
  process.exit(falhasTotais ? 1 : 0);
})();
