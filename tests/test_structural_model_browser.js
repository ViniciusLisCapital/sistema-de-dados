// Confirmacao em browser real do Structural Model, com foco na aba Simulador.
// Chrome headless via CDP, WebSocket global do Node 22+, sem npm.
//
// Este harness cobre o que `tests/test_structural_model_js.js` NAO cobre de proposito:
// a FIACAO. Os controles do simulador nascem de `innerHTML`, e o stub de DOM daquele
// arquivo nao constroi arvore a partir de string -- um teste de clique passaria la sem
// exercitar nada. Aqui os cliques sao cliques.
//
//   node tests/test_structural_model_browser.js "<caminho do HTML gerado>"
const { spawn } = require('child_process');
const path = require('path');
const fs = require('fs');
const os = require('os');

const CHROME = process.env.CHROME_BIN
  || 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe';
const ARQ = process.argv[2] || path.join(
  __dirname, '..', 'reports', 'brasil', 'Structural Model.html');
const PORTA = 9333 + (process.pid % 200);
const PERFIL = fs.mkdtempSync(path.join(os.tmpdir(), 'cdpsim-'));

let oks = 0, falhas = 0;
function ok(cond, nome, det) {
  if (cond) { oks++; console.log('  ok    ' + nome + (det ? '  [' + det + ']' : '')); }
  else { falhas++; console.log('  FALHA ' + nome + (det ? '  [' + det + ']' : '')); }
}

const chrome = spawn(CHROME, [
  '--headless=new', '--disable-gpu', '--no-first-run', '--no-default-browser-check',
  '--remote-debugging-port=' + PORTA, '--user-data-dir=' + PERFIL,
  '--window-size=1600,1200', 'about:blank',
], { stdio: 'ignore' });

const esperar = (ms) => new Promise((r) => setTimeout(r, ms));

async function alvo() {
  for (let i = 0; i < 60; i++) {
    try {
      const r = await fetch('http://127.0.0.1:' + PORTA + '/json/list');
      const pg = (await r.json()).find((t) => t.type === 'page');
      if (pg) return pg.webSocketDebuggerUrl;
    } catch (e) { /* ainda subindo */ }
    await esperar(250);
  }
  throw new Error('Chrome nao abriu a porta de depuracao');
}

function conectar(url) {
  const ws = new WebSocket(url);
  let id = 0;
  const pend = new Map();
  const eventos = [];
  ws.addEventListener('message', (ev) => {
    const m = JSON.parse(ev.data);
    if (m.id && pend.has(m.id)) { pend.get(m.id)(m); pend.delete(m.id); }
    else if (m.method) eventos.push(m);
  });
  const pronto = new Promise((r) => ws.addEventListener('open', r));
  return {
    eventos, pronto,
    envia(method, params) {
      const k = ++id;
      ws.send(JSON.stringify({ id: k, method, params: params || {} }));
      return new Promise((r) => pend.set(k, r));
    },
    fecha() { ws.close(); },
  };
}

(async () => {
  const c = conectar(await alvo());
  await c.pronto;
  await c.envia('Runtime.enable');
  await c.envia('Log.enable');
  await c.envia('Page.enable');

  const url = 'file:///' + ARQ.replace(/\\/g, '/').replace(/ /g, '%20');
  await c.envia('Page.navigate', { url });
  await esperar(4500);

  async function aval(expr) {
    const r = await c.envia('Runtime.evaluate', {
      expression: expr, returnByValue: true, awaitPromise: true,
    });
    if (r.result && r.result.exceptionDetails) {
      throw new Error(JSON.stringify(r.result.exceptionDetails));
    }
    return r.result && r.result.result ? r.result.result.value : undefined;
  }
  // Dispara o evento que o navegador dispararia, e nao so escreve no `.value`:
  // escrever no valor deixa o estado valido no objeto e invalido na tela, que e
  // exatamente o modo de falha que este harness existe para pegar.
  async function mexe(sel, valor, ev) {
    return aval(`(() => {
      const e = document.querySelector(${JSON.stringify(sel)});
      if (!e) return 'sem elemento';
      ${typeof valor === 'boolean' ? 'e.checked = ' + valor + ';'
                                   : 'e.value = ' + JSON.stringify(String(valor)) + ';'}
      e.dispatchEvent(new Event(${JSON.stringify(ev || 'change')}, { bubbles: true }));
      return 'ok';
    })()`);
  }
  async function clica(sel) {
    return aval(`(() => {
      const e = document.querySelector(${JSON.stringify(sel)});
      if (!e) return 'sem elemento';
      e.click();
      return 'ok';
    })()`);
  }
  const fimCam = () => aval('SIM._ultimo.cam[SIM._ultimo.cam.length-1]');

  console.log('\n1. Carregamento');
  const exc = c.eventos.filter((e) => e.method === 'Runtime.exceptionThrown');
  const erros = c.eventos.filter((e) => e.method === 'Log.entryAdded'
    && e.params.entry.level === 'error');
  ok(exc.length === 0, 'zero excecoes no carregamento',
     exc.map((e) => e.params.exceptionDetails.text).join(' | ') || 'nenhuma');
  ok(erros.length === 0, 'zero erros no console',
     erros.map((e) => e.params.entry.text).slice(0, 2).join(' | ') || 'nenhum');
  const dupl = await aval(`(() => {
    const vis = {}, dup = [];
    document.querySelectorAll('[id]').forEach((e) => {
      if (vis[e.id]) dup.push(e.id); vis[e.id] = 1;
    });
    return dup.join(',');
  })()`);
  ok(dupl === '', 'nenhum id repetido na pagina', dupl || 'nenhum');
  const abas = await aval(
    `Array.from(document.querySelectorAll('.tab-btn')).map(b=>b.textContent).join('|')`);
  ok(abas.indexOf('Simulador') >= 0, 'a aba Simulador esta na barra', abas);

  console.log('\n2. A aba abre, pinta, e tem os dois blocos');
  await clica('.tab-btn[data-tab="tab-sim"]');
  await esperar(2500);
  ok(await aval(`document.getElementById('tab-sim').classList.contains('active')`),
     'o painel do simulador fica ativo');
  const blocos = await aval(
    `document.querySelectorAll('#tab-sim .sim-bloco').length`);
  ok(blocos === 2, 'a aba tem exatamente dois blocos', String(blocos));
  const plot = await aval(`(() => {
    const el = document.getElementById('ch-sim');
    if (!el || !el.data) return { n: 0, nomes: '(sem div ou sem data)', pontos: 0 };
    return { n: el.data.length,
             nomes: el.data.map(t => t.name || '(anonimo)').join(', '),
             pontos: el.data.reduce((a, t) => a + ((t.y && t.y.length) || 0), 0) };
  })()`);
  ok(plot.n === 5 && plot.pontos > 100,
     'o Plotly de verdade pintou o grafico: 5 traces com dado',
     plot.n + ' traces, ' + plot.pontos + ' pontos; ' + plot.nomes);
  ok(await aval(`(document.getElementById('ch-sim')._fullLayout.xaxis||{}).type`)
       === 'date',
     'o eixo X resolve para data, nao para linear');
  // A aba abre projetando 12 trimestres para a FRENTE do ultimo dado, entao a janela
  // do eixo tem de alcanca-los: um "Tudo" tirado so da serie observada deixaria a
  // projecao desenhada e fora da tela.
  const proj = await aval(`(() => {
    const g = SIM._ultimo.g;
    const r = document.getElementById('ch-sim')._fullLayout.xaxis.range;
    return { i0: SIM.i0, decl: D.sim.i0, estI1: D.sim.eq.R.est_i1,
             estFim: D.sim.eq.R.est_fim, h: SIM.h,
             ini: g.rot[0], fim: g.rot[g.rot.length - 1],
             sel: document.getElementById('simJanela')
                    .querySelectorAll('select').length,
             cobre: Date.parse(r[1]) >= Date.parse(g.x[g.x.length - 1]) };
  })()`);
  ok(proj.i0 === proj.decl && proj.decl === proj.estI1 + 1,
     'a janela comeca no trimestre seguinte ao fim da janela estimada',
     'i0 = ' + proj.i0 + ', estimou ate ' + proj.estFim);
  ok(proj.sel === 0, 'nao ha seletor de partida na barra', String(proj.sel));
  ok(proj.h === 12, 'e projeta 12 trimestres', proj.ini + ' a ' + proj.fim);
  ok(proj.cobre === true, 'a janela do eixo alcanca o ultimo trimestre projetado');
  const cab = await aval(`(() => {
    const c = document.getElementById('ch-sim').parentNode;
    const t = c.querySelector('.chart-title'), s = c.querySelector('.chart-sub'),
          f = c.querySelector('.chart-src');
    return [t && t.textContent.length, s && s.textContent.length,
            f && f.textContent.slice(0, 6)].join('|');
  })()`);
  ok(/^\d+\|\d+\|Fonte:/.test(cab), 'o cabecalho de tres linhas esta no cartao', cab);
  ok(await aval(`(() => {
    const c = document.getElementById('ch-sim').parentNode;
    const k = Array.from(c.children);
    return k.indexOf(c.querySelector('.range-pills'))
         > k.indexOf(document.getElementById('ch-sim'));
  })()`), 'a regua de tempo esta DEPOIS do grafico');

  console.log('\n3. Bloco 2: um cartao por variavel, no desenho do FX Report');
  const cards = await aval(`(() => {
    const out = [];
    document.querySelectorAll('#simInputs .sim-card').forEach((c) => {
      out.push({ id: c.id, selo: (c.querySelector('.sim-selo') || {}).className || '',
                 texto: (c.querySelector('.sim-selo') || {}).textContent || '',
                 fontes: Array.from(c.querySelectorAll('.sim-modo-btn'))
                   .map(r => r.getAttribute('data-fonte')).join(','),
                 rots: Array.from(c.querySelectorAll('.sim-modo-btn'))
                   .map(r => r.textContent).join('|'),
                 ajuda: (c.querySelector('.sim-modo-btn[data-fonte=observado]') || {})
                   .title || '',
                 ativa: (c.querySelector('.sim-modo-btn.on') || {})
                   .getAttribute ? c.querySelector('.sim-modo-btn.on')
                     .getAttribute('data-fonte') : '',
                 linhas: c.querySelectorAll('.sim-card-lin').length,
                 links: Array.from(c.querySelectorAll('.sim-link'))
                   .map(l => l.textContent).join(' | '),
                 caixas: c.querySelectorAll('.sim-caixa-in').length });
    });
    return out;
  })()`);
  ok(cards.length === 4, 'ha um cartao por input declarado', String(cards.length));
  const cSel = cards.find((c) => c.id === 'simcard-selic');
  const cDi = cards.find((c) => c.id === 'simcard-di');
  ok(!!cSel && /endo/.test(cSel.selo), 'a Selic traz o selo de endogena', cSel && cSel.texto);
  ok(!!cDi && /futura/.test(cDi.selo),
     'o desvio da inflacao traz o selo de "exogena hoje, endogena depois"',
     cDi && cDi.texto);
  // A ordem e a das pills na tela, e os rotulos sao os que o usuario pediu em
  // 2026-09-22: Endogeno, Exogeno, Observado.
  ok(cSel.fontes === 'equacao,digitado,observado',
     'a endogena oferece as tres fontes, nessa ordem', cSel.fontes);
  ok(cDi.fontes === 'digitado,observado',
     'a exogena nao oferece Endogeno -- nao ha equacao que a produza', cDi.fontes);
  ok(cSel.rots === 'Endógeno|Exógeno|Observado',
     'e os rotulos sao Endogeno / Exogeno / Observado', cSel.rots);
  ok(cDi.ativa === 'observado', 'a pill da fonte corrente esta marcada', cDi.ativa);
  ok(/repetido/.test(cDi.ajuda),
     'a pill Observado explica que, sem dado, o ultimo valor e repetido', cDi.ajuda);
  ok(cDi.caixas === 12, 'cada cartao tem 12 caixas, uma por trimestre do teto',
     String(cDi.caixas));
  // As duas linhas do cabecalho do cartao do FX: a leitura de hoje e a instrucao do
  // que se digita ali. Sem a segunda o cartao mostra caixas e nao diz o que vai nelas.
  ok(cards.every((c) => c.linhas === 2),
     'todo cartao traz a leitura de hoje E a instrucao do que se digita',
     cards.map((c) => c.id + ':' + c.linhas).join(' '));
  ok(/Aplicar choque/.test(cDi.links) && /Abrir em partes/.test(cDi.links),
     'as acoes do cartao sao links, como no FX Report', cDi.links);
  const est = await aval(`(() => {
    const cx = Array.from(document.querySelectorAll('#simcard-di .sim-caixa-in'));
    return { desab: cx[0].disabled,
             obs: cx.filter(e => e.className.indexOf('obs') >= 0).length,
             seg: cx.filter(e => e.className.indexOf('seg') >= 0).length };
  })()`);
  ok(est.desab === true, 'as caixas nascem desabilitadas: a fonte e o observado');
  // A aba abre PROJETANDO, entao nenhuma caixa e de trimestre publicado: todas as 12
  // seguram o ultimo valor conhecido, e e isso que o dourado diz.
  ok(est.seg + est.obs === 12,
     'as 12 caixas dizem, cada uma, se aquele trimestre ja saiu ou esta sendo repetido',
     est.obs + ' verdes, ' + est.seg + ' douradas');

  console.log('\n4. Os controles mexem no resultado');
  const base = await fimCam();
  await clica('#simcard-di .sim-modo-btn[data-fonte="digitado"]');
  await esperar(700);
  ok(await aval(`SIM.fonte.di`) === 'digitado',
     'clicar na pill troca a fonte daquela variavel');
  ok(await aval(`document.querySelector('#simcard-di .sim-caixa-in').disabled`) === false,
     'e as caixas ficam editaveis');
  await mexe('#simcard-di .sim-caixa-in', 5);
  await esperar(700);
  const comDi = await fimCam();
  ok(Math.abs(comDi - base) > 1e-6,
     'editar uma caixa do desvio muda o caminho simulado',
     base.toFixed(3) + ' -> ' + comDi.toFixed(3));

  // O composto: abrir em partes e mexer numa delas move o agregado.
  // A ordem importa e ja custou uma falha: o botao e um ALTERNA, e o estado de aberto
  // sobrevive ao re-render. Clicar duas vezes fecha, e ai o seletor da caixa nao acha
  // nada e o teste reprova a pagina certa.
  await clica('#simcard-ancora .sim-modo-btn[data-fonte="digitado"]');
  await esperar(500);
  await clica('#simcard-ancora [data-partes="ancora"]');
  await esperar(600);
  const nPartes = await aval(
    `document.querySelectorAll('#simcard-ancora .sim-parte').length`);
  ok(nPartes === 2, 'abrir a ancora em partes mostra as duas primitivas',
     String(nPartes));
  ok(await aval(
     `document.querySelector('#simcard-ancora .sim-parte .sim-caixa-in').disabled`)
     === false, 'as caixas das partes ficam editaveis junto com as do agregado');
  const ancAntes = await aval(`SIM.cx.ancora[0]`);
  const rrAntes = await aval(`SIM.px.rr_10a[0]`);
  await mexe('#simcard-ancora .sim-parte .sim-caixa-in', rrAntes + 2);
  await esperar(700);
  const ancDepois = await aval(`SIM.cx.ancora[0]`);
  ok(Math.abs((ancDepois - ancAntes) - 2) < 1e-6,
     'somar 2 ao juro real de equilibrio soma 2 a ancora',
     ancAntes.toFixed(3) + ' -> ' + ancDepois.toFixed(3));

  // O choque rapido.
  await clica('#simcard-di [data-reset="di"]');
  await esperar(600);
  const antesChq = await fimCam();
  await clica('#simcard-di [data-choque="di"]');
  await esperar(500);
  ok(await aval(`document.querySelectorAll('#simcard-di .sim-choque').length`) === 1,
     'o painel de choque rapido abre');
  await mexe('#simcard-di [data-chq="v"]', 2);
  await clica('#simcard-di [data-aplica="di"]');
  await esperar(800);
  const depoisChq = await fimCam();
  ok(await aval(`SIM.fonte.di`) === 'digitado',
     'aplicar um choque passa a variavel para o caminho digitado');
  ok(depoisChq > antesChq, 'e o choque de +2 p.p. sobe a Selic simulada',
     antesChq.toFixed(3) + ' -> ' + depoisChq.toFixed(3));

  console.log('\n4b. As premissas movem a Selic, e a parte aceita choque');
  // (i) Mexer numa premissa tem de mover as CAIXAS da Selic, e nao so a linha: em
  // Endogeno a caixa mostra o que a equacao produz. Antes ela mostrava o ultimo
  // observado repetido, que nao se mexia nunca.
  await clica('#simcard-di [data-reset="di"]');
  await esperar(700);
  const selAntes = await aval(
    `Array.from(document.querySelectorAll('#simcard-selic .sim-caixa-in')).map(e=>e.value).join(',')`);
  await clica('#simcard-di .sim-modo-btn[data-fonte="digitado"]');
  await esperar(600);
  await mexe('#simcard-di .sim-caixa-in:not([disabled])', 4);
  await esperar(800);
  const selDepois = await aval(
    `Array.from(document.querySelectorAll('#simcard-selic .sim-caixa-in')).map(e=>e.value).join(',')`);
  ok(selAntes !== selDepois,
     'mexer na premissa move as caixas da Selic, e nao so a linha do grafico',
     selAntes.slice(0, 24) + ' -> ' + selDepois.slice(0, 24));
  ok(await aval(
     `document.querySelector('#simcard-selic .sim-caixa-in').className.indexOf('eqp') >= 0`),
     'as caixas da Selic saem na cor de "vem da equacao"');

  // (ii) O choque numa PARTE.
  await clica('#simcard-di [data-reset="di"]');
  await esperar(600);
  // O botao de abrir em partes e um ALTERNA e o estado sobrevive ao re-render: a secao
  // anterior ja o abriu, entao clicar aqui fecharia. Abre so se estiver fechado.
  if (await aval(`!!SIM.aberto.ancora`) !== true) {
    await clica('#simcard-ancora [data-partes="ancora"]');
    await esperar(600);
  }
  ok(await aval(
     `document.querySelectorAll('#simcard-ancora .sim-parte .sim-link[data-choque]').length`)
     === 2, 'cada parte tem o proprio "Aplicar choque"');
  const antesP = await aval(`SIM.px.rr_10a[0]`);
  const metaP = await aval(`SIM.px.meta_12m[0]`);
  await clica('#simcard-ancora .sim-parte .sim-link[data-choque="rr_10a"]');
  await esperar(600);
  ok(await aval(`document.querySelectorAll('#simcard-ancora .sim-parte .sim-choque').length`)
     === 1, 'o painel de choque da parte abre');
  // A forma: constante por N trimestres e depois decaindo.
  await mexe('#simcard-ancora [data-chq="tipo"][data-chqk="rr_10a"]', 'const');
  await esperar(600);
  await mexe('#simcard-ancora [data-chq="v"][data-chqk="rr_10a"]', 2);
  await esperar(600);
  const campos = await aval(`(() => {
    const p = document.querySelector('#simcard-ancora .sim-parte .sim-choque');
    return { n: p.querySelectorAll('[data-chq=n]').length,
             rho: p.querySelectorAll('[data-chq=rho]').length,
             pre: (p.querySelector('.sim-chq-pre') || {}).textContent || '' };
  })()`);
  ok(campos.n === 1 && campos.rho === 1,
     'a forma "constante e depois decaindo" mostra os dois campos', JSON.stringify(campos));
  ok(/soma/.test(campos.pre) && /\+2,00/.test(campos.pre),
     'e a previa mostra o acrescimo trimestre a trimestre', campos.pre);
  await clica('#simcard-ancora .sim-parte [data-aplica="rr_10a"]');
  await esperar(800);
  const depoisP = await aval(`SIM.px.rr_10a[0]`);
  ok(Math.abs((depoisP - antesP) - 2) < 1e-6,
     'aplicar o choque na parte soma 2 ao juro real de equilibrio',
     antesP.toFixed(3) + ' -> ' + depoisP.toFixed(3));
  ok(Math.abs(await aval(`SIM.px.meta_12m[0]`) - metaP) < 1e-9,
     'e a outra parte fica onde estava');
  ok(await aval(`SIM.fonte.ancora`) === 'digitado',
     'o cartao pai passa para Exogeno, que e a fonte que a conta le');
  await clica('#simcard-ancora [data-reset="ancora"]');
  await esperar(700);

  console.log('\n5. A janela, o aviso, e nenhum peso para digitar');
  await clica('#simcard-di [data-reset="di"]');
  await esperar(600);
  // O pedido do usuario: a simulacao vem dos INPUTS. Nenhum peso da equacao e
  // digitavel, e o guarda vive aqui e nao so no harness de node porque a barra e
  // montada por `innerHTML` -- e no browser que ela existe como elemento.
  const pesos = await aval(`(() => {
    const b = document.getElementById('simOpcoes');
    return { nums: b.querySelectorAll('input[type=number]').length,
             chks: b.querySelectorAll('input[type=checkbox]').length,
             txt: b.textContent.slice(0, 60) };
  })()`);
  ok(pesos.nums === 0, 'o bloco 1 nao tem nenhuma caixa de numero para digitar peso',
     String(pesos.nums));
  ok(pesos.chks === 2, 'so as duas opcoes de desenho: a faixa e o erro da equacao',
     String(pesos.chks));

  const semFaixa = await aval(`(() => {
    const el = document.getElementById('ch-sim');
    return el.data.length;
  })()`);
  await mexe('#simFaixa', false, 'change');
  await esperar(800);
  ok(await aval(`document.getElementById('ch-sim').data.length`) === semFaixa - 2,
     'desligar a faixa tira os dois traces que a desenham',
     semFaixa + ' -> ' + await aval(`document.getElementById('ch-sim').data.length`));
  await mexe('#simFaixa', true, 'change');
  await esperar(800);

  await mexe('#simH', 40);
  await esperar(700);
  ok(await aval('SIM.h') === 12, 'o horizonte e limitado ao teto de 12 trimestres',
     String(await aval('SIM.h')));
  await mexe('#simH', 4);
  await esperar(700);
  ok(await aval(
     `document.querySelectorAll('#simcard-di .sim-caixa-in').length`) === 4,
     'as caixas acompanham o horizonte');
  await mexe('#simH', 12);
  await esperar(700);

  await clica('#simcard-selic .sim-modo-btn[data-fonte="observado"]');
  await esperar(700);
  const av = await aval(`(() => {
    const a = document.getElementById('simAviso');
    return a.style.display + '|' + a.textContent.slice(0, 40);
  })()`);
  ok(av.indexOf('none') !== 0 && /desligada/.test(av),
     'impor a Selic avisa que a regra de juros esta desligada', av);
  await clica('#simcard-selic [data-reset="selic"]');
  await esperar(700);
  ok(await aval(`SIM.fonte.selic`) === 'equacao',
     'e o botao do cartao devolve a Selic para a equacao');

  console.log('\n6. Nada quebrou nas outras abas');
  for (const t of ['tab-dados', 'tab-modelo', 'tab-exp', 'tab-is', 'tab-tay',
                   'tab-fx', 'tab-sim']) {
    await clica('.tab-btn[data-tab="' + t + '"]');
    await esperar(1100);
  }
  const ex2 = c.eventos.filter((e) => e.method === 'Runtime.exceptionThrown');
  ok(ex2.length === 0, 'zero excecoes depois de visitar as sete abas',
     ex2.map((e) => e.params.exceptionDetails.text).slice(0, 2).join(' | ') || 'nenhuma');
  const vazios = await aval(`(() => {
    const ids = ['ch-sim'];
    document.querySelectorAll('.chart-plot').forEach(e => ids.push(e.id));
    return Array.from(new Set(ids)).filter((i) => {
      const e = document.getElementById(i);
      return !e || !e.data || !e.data.length;
    }).join(',');
  })()`);
  ok(vazios === '', 'todo cartao de grafico da pagina tem traces pintados',
     vazios || 'nenhum vazio');

  console.log('\n' + '='.repeat(62));
  console.log(oks + ' ok, ' + falhas + ' falharam');
  c.fecha();
  chrome.kill();
  try { fs.rmSync(PERFIL, { recursive: true, force: true }); } catch (e) { /* ok */ }
  process.exit(falhas ? 1 : 0);
})().catch((e) => {
  console.error('ERRO NO HARNESS:', e);
  chrome.kill();
  process.exit(2);
});
