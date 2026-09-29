// Confirmacao em browser real do Structural Model, com foco na aba do simulador --
// que desde 2026-09-28 se chama Structural Model, porque e o modelo agregado.
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
  ok(abas.indexOf('Structural Model') >= 0 && abas.indexOf('Simulador') < 0,
     'a aba do simulador esta na barra com o nome novo, Structural Model', abas);

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
  // Seis traces: a Selic observada, o juro nominal de equilibrio observado e o trecho
  // projetado dele (sem legenda propria), as duas bordas da faixa e a Selic produzida.
  ok(plot.n === 6 && plot.pontos > 100,
     'o Plotly de verdade pintou o grafico: 6 traces com dado',
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
  // A organizacao em grupos, pedida em 2026-09-24: (1) Endogenas; (2) Exogenas, em
  // Gerais e Especificas por equacao. Cada grupo e um clique-expande, e o que se afirma
  // aqui e o que so existe no browser: o <details> de verdade, o estado `open`, e que
  // fechar um grupo SOBREVIVE ao re-render que qualquer clique no bloco dispara.
  const grp = await aval(`(() => {
    const ds = Array.from(document.querySelectorAll('#simInputs details.sim-fold'));
    return ds.map(d => ({ id: d.getAttribute('data-grupo'), open: d.open,
                          nome: d.querySelector('.sim-grupo-nome').textContent,
                          cards: d.querySelectorAll('.sim-card').length }));
  })()`);
  ok(grp.length >= 3, 'o bloco 2 esta dividido em grupos de clique-expande',
     grp.map(g => g.id + ':' + g.cards).join(' '));
  ok(grp.every(g => g.open), 'todos abrem por padrao', JSON.stringify(grp.map(g => g.open)));
  // Dois recortes desde 2026-09-25, no lugar de "gerais" e "especificas por equacao":
  // *"As exogenas vamos separar somente em Domestica e Externa."*
  const gEndo = grp.find(g => g.id === 'endo');
  const gDom = grp.find(g => g.id === 'reg-domestica');
  const gExt = grp.find(g => g.id === 'reg-externa');
  const cont = await aval(`(() => {
    const v = D.sim.var, o = D.sim.var_ordem;
    return { endo: o.filter((k) => v[k].tipo === 'endogena').length,
             dom: o.filter((k) => v[k].regiao === 'domestica').length,
             ext: o.filter((k) => v[k].regiao === 'externa').length };
  })()`);
  ok(grp.length === 3,
     'sao exatamente tres grupos: endogenas, domesticas e externas',
     grp.map(g => g.id).join(' '));
  ok(!!gEndo && gEndo.cards === cont.endo,
     'Endogenas traz toda variavel que alguma equacao DO SIMULADOR produz',
     (gEndo && String(gEndo.cards)) + ' de ' + cont.endo);
  ok(cont.endo === 5,
     'e com a (I) no simulador elas sao cinco: hiato, inflacao, expectativa, Selic e '
     + 'cambio', String(cont.endo));
  ok(!!gDom && gDom.cards === cont.dom && gDom.cards > 0,
     'as exogenas domesticas tem cartao', (gDom && String(gDom.cards)));
  ok(!!gExt && gExt.cards === cont.ext && gExt.cards > 0,
     'e as externas tambem -- o recorte separa de fato',
     (gExt && String(gExt.cards)));
  ok(!grp.some(g => /gerais|^esp-/.test(g.id)),
     'e nao sobrou grupo da divisao antiga', grp.map(g => g.id).join(' '));
  // Fechar um grupo e mexer num controle: o grupo tem de continuar fechado.
  await clica('#simInputs details.sim-fold[data-grupo="endo"] summary');
  await esperar(300);
  await clica('#simcard-rr_10a .sim-modo-btn[data-fonte="digitado"]');
  await esperar(700);
  ok(await aval(
     `document.querySelector('#simInputs details[data-grupo="endo"]').open`) === false,
     'o grupo fechado sobrevive ao re-render que outro controle dispara');
  await clica('#simInputs details.sim-fold[data-grupo="endo"] summary');
  await esperar(300);
  await clica('#simcard-rr_10a [data-reset="rr_10a"]');
  await esperar(700);

  // Contado contra o payload, e nao contra um numero escrito aqui: as crises sairam
  // do bloco em 2026-09-24 e um literal teria reprovado uma tela correta.
  const nVar = await aval('D.sim.var_ordem.length');
  ok(cards.length === nVar, 'ha um cartao por input declarado',
     cards.length + ' cartoes para ' + nVar + ' inputs');
  ok(!cards.some((c) => c.id === 'simcard-crise'),
     'e nenhum deles e o das crises, que deixaram de ser input');
  const cSel = cards.find((c) => c.id === 'simcard-selic');
  const cDi = cards.find((c) => c.id === 'simcard-meta_12m');
  const cInf = cards.find((c) => c.id === 'simcard-infl_br');
  ok(!!cSel && /endo/.test(cSel.selo), 'a Selic traz o selo de endogena', cSel && cSel.texto);
  // O selo fala DESTA rodada. A inflacao do trimestre foi ate 2026-09-28 o caso
  // "endogena no modelo, fora do simulador"; com a (I) dentro, o selo diz de onde ela vem.
  ok(!!cInf && /endo/.test(cInf.selo) && /\(I\)/.test(cInf.texto)
     && cInf.fontes === 'equacao,digitado,observado',
     'a inflacao e endogena, vem da (I), e oferece as tres fontes',
     cInf && cInf.texto.slice(0, 80));
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
  ok(/Aplicar choque/.test(cDi.links) && /Ver o gráfico/.test(cDi.links),
     'as acoes do cartao sao links, como no FX Report', cDi.links);
  ok(!/Abrir em partes/.test(cards.map((c) => c.links).join(' ')),
     'e nenhum cartao abre em partes: nao ha mais premissa com subpremissa');
  const est = await aval(`(() => {
    const cx = Array.from(document.querySelectorAll('#simcard-meta_12m .sim-caixa-in'));
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
  await clica('#simcard-meta_12m .sim-modo-btn[data-fonte="digitado"]');
  await esperar(700);
  ok(await aval(`SIM.fonte.meta_12m`) === 'digitado',
     'clicar na pill troca a fonte daquela variavel');
  ok(await aval(`document.querySelector('#simcard-meta_12m .sim-caixa-in').disabled`) === false,
     'e as caixas ficam editaveis');
  await mexe('#simcard-meta_12m .sim-caixa-in', 5);
  await esperar(700);
  const comDi = await fimCam();
  ok(Math.abs(comDi - base) > 1e-6,
     'editar uma caixa da meta muda o caminho simulado',
     base.toFixed(3) + ' -> ' + comDi.toFixed(3));

  // O que era "abrir em partes" virou cartao proprio: mexer no juro real de dez anos
  // move a ANCORA, que e conta da equacao e nao tem caixa nenhuma.
  await clica('#simcard-rr_10a .sim-modo-btn[data-fonte="digitado"]');
  await esperar(500);
  ok(await aval(
     `document.querySelectorAll('#simcard-rr_10a .sim-parte').length`) === 0,
     'o cartao do juro real nao tem partes -- ele E a peca');
  const ancAntes = await aval(`SIM._ultimo.anc[0]`);
  const rrAntes = await aval(`SIM.cx.rr_10a[0]`);
  await mexe('#simcard-rr_10a .sim-caixa-in:not([disabled])', rrAntes + 2);
  await esperar(700);
  const ancDepois = await aval(`SIM._ultimo.anc[0]`);
  ok(Math.abs((ancDepois - ancAntes) - 2) < 1e-6,
     'somar 2 ao juro real de dez anos soma 2 a ancora que a equacao usa',
     ancAntes.toFixed(3) + ' -> ' + ancDepois.toFixed(3));
  await clica('#simcard-rr_10a [data-reset="rr_10a"]');
  await esperar(600);

  // O choque rapido.
  await clica('#simcard-meta_12m [data-reset="meta_12m"]');
  await esperar(600);
  const antesChq = await fimCam();
  await clica('#simcard-meta_12m [data-choque="meta_12m"]');
  await esperar(500);
  ok(await aval(`document.querySelectorAll('#simcard-meta_12m .sim-choque').length`) === 1,
     'o painel de choque rapido abre');
  await mexe('#simcard-meta_12m [data-chq="v"]', 2);
  await clica('#simcard-meta_12m [data-aplica="meta_12m"]');
  await esperar(800);
  const depoisChq = await fimCam();
  ok(await aval(`SIM.fonte.meta_12m`) === 'digitado',
     'aplicar um choque passa a variavel para o caminho digitado');
  // Subir a META em 2 p.p. sobe a Selic: a ancora sobe 2 e o desvio cai menos que 2,
  // porque a expectativa acompanha a meta em parte -- e a (E) que faz isso.
  ok(depoisChq > antesChq, 'e o choque de +2 p.p. na meta sobe a Selic simulada',
     antesChq.toFixed(3) + ' -> ' + depoisChq.toFixed(3));

  console.log('\n4b. As premissas movem a Selic, e a parte aceita choque');
  // (i) Mexer numa premissa tem de mover as CAIXAS da Selic, e nao so a linha: em
  // Endogeno a caixa mostra o que a equacao produz. Antes ela mostrava o ultimo
  // observado repetido, que nao se mexia nunca.
  await clica('#simcard-meta_12m [data-reset="meta_12m"]');
  await esperar(700);
  const selAntes = await aval(
    `Array.from(document.querySelectorAll('#simcard-selic .sim-caixa-in')).map(e=>e.value).join(',')`);
  await clica('#simcard-meta_12m .sim-modo-btn[data-fonte="digitado"]');
  await esperar(600);
  await mexe('#simcard-meta_12m .sim-caixa-in:not([disabled])', 4);
  await esperar(800);
  const selDepois = await aval(
    `Array.from(document.querySelectorAll('#simcard-selic .sim-caixa-in')).map(e=>e.value).join(',')`);
  ok(selAntes !== selDepois,
     'mexer na premissa move as caixas da Selic, e nao so a linha do grafico',
     selAntes.slice(0, 24) + ' -> ' + selDepois.slice(0, 24));
  ok(await aval(
     `document.querySelector('#simcard-selic .sim-caixa-in').className.indexOf('eqp') >= 0`),
     'as caixas da Selic saem na cor de "vem da equacao"');

  // (ii) O choque numa PECA de uma conta derivada, agora que a peca e cartao.
  await clica('#simcard-meta_12m [data-reset="meta_12m"]');
  await esperar(600);
  const antesP = await aval(`SIM.cx.rr_10a[0]`);
  const metaP = await aval(`SIM.cx.meta_12m[0]`);
  await clica('#simcard-rr_10a [data-choque="rr_10a"]');
  await esperar(600);
  ok(await aval(`document.querySelectorAll('#simcard-rr_10a .sim-choque').length`)
     === 1, 'o painel de choque do cartao abre');
  // A forma: constante por N trimestres e depois decaindo.
  await mexe('#simcard-rr_10a [data-chq="tipo"][data-chqk="rr_10a"]', 'const');
  await esperar(600);
  await mexe('#simcard-rr_10a [data-chq="v"][data-chqk="rr_10a"]', 2);
  await esperar(600);
  const campos = await aval(`(() => {
    const p = document.querySelector('#simcard-rr_10a .sim-choque');
    return { n: p.querySelectorAll('[data-chq=n]').length,
             rho: p.querySelectorAll('[data-chq=rho]').length,
             pre: (p.querySelector('.sim-chq-pre') || {}).textContent || '' };
  })()`);
  ok(campos.n === 1 && campos.rho === 1,
     'a forma "constante e depois decaindo" mostra os dois campos', JSON.stringify(campos));
  ok(/soma/.test(campos.pre) && /\+2,00/.test(campos.pre),
     'e a previa mostra o acrescimo trimestre a trimestre', campos.pre);
  await clica('#simcard-rr_10a [data-aplica="rr_10a"]');
  await esperar(800);
  const depoisP = await aval(`SIM.cx.rr_10a[0]`);
  ok(Math.abs((depoisP - antesP) - 2) < 1e-6,
     'aplicar o choque soma 2 ao juro real de dez anos',
     antesP.toFixed(3) + ' -> ' + depoisP.toFixed(3));
  ok(Math.abs(await aval(`SIM.cx.meta_12m[0]`) - metaP) < 1e-9,
     'e a outra peca da mesma conta fica onde estava');
  ok(await aval(`SIM.fonte.rr_10a`) === 'digitado',
     'o cartao chocado passa para Exogeno, que e a fonte que a conta le');
  await clica('#simcard-rr_10a [data-reset="rr_10a"]');
  await esperar(700);

  console.log('\n5. A janela, o aviso, e nenhum controle no bloco 1');
  await clica('#simcard-meta_12m [data-reset="meta_12m"]');
  await esperar(600);
  // Duas rodadas de corte: os pesos (*"a simulacao vem dos inputs"*) e depois a barra
  // de desenho e a caixa de horizonte. O guarda vive aqui e nao so no harness de node
  // porque esses controles nasciam de `innerHTML` -- e no browser que eles existiriam
  // como elemento.
  const ctrl = await aval(`(() => {
    const card = document.querySelector('.sim-eq-card');
    const jan = document.getElementById('simJanela');
    return { eqIn: card.querySelectorAll('input, select').length,
             janIn: jan.querySelectorAll('input, select').length,
             barra: !!document.getElementById('simOpcoes'),
             janTxt: jan.textContent };
  })()`);
  ok(ctrl.eqIn === 0, 'o bloco 1 nao tem nenhum controle: ele so imprime',
     String(ctrl.eqIn));
  ok(!ctrl.barra, 'e a barra "o desenho" nao existe mais na pagina');
  ok(ctrl.janIn === 0, 'a barra da janela tambem nao tem controle', String(ctrl.janIn));
  ok(/12 trimestres/.test(ctrl.janTxt), 'ela diz o tamanho da projecao', ctrl.janTxt);
  ok(await aval('SIM.h') === 12, 'que e sempre 12', String(await aval('SIM.h')));
  ok(await aval(
     `document.querySelectorAll('#simcard-meta_12m .sim-caixa-in').length`) === 12,
     'e as caixas de cada cartao acompanham os 12 trimestres');

  // A faixa deixou de ser opcao: ela e conteudo, e os dois traces que a desenham
  // estao sempre la enquanto a equacao estiver rodando.
  const nTr = await aval(`document.getElementById('ch-sim').data.length`);
  ok(await aval(`(() => {
    const el = document.getElementById('ch-sim');
    return el.data.filter((t) => t.fill === 'tonexty'
                                 && /Faixa de \\d+%/.test(t.name || '')).length;
  })()`) === 1, 'a faixa do posterior esta desenhada, e nao ha como desliga-la',
     String(nTr) + ' traces');

  await clica('#simcard-selic .sim-modo-btn[data-fonte="observado"]');
  await esperar(700);
  const av = await aval(`(() => {
    const a = document.getElementById('simAviso-R'), b = document.getElementById('simAviso-F');
    return a.style.display + '|' + a.textContent.slice(0, 60) + '|F:' + b.style.display;
  })()`);
  ok(av.indexOf('none') !== 0 && /desligada/.test(av),
     'impor a Selic avisa que a regra de juros esta desligada', av);
  ok(/F:none/.test(av),
     'e o aviso e do cartao DELA: a equacao do cambio continua ligada');
  await clica('#simcard-selic [data-reset="selic"]');
  await esperar(700);
  ok(await aval(`SIM.fonte.selic`) === 'equacao',
     'e o botao do cartao devolve a Selic para a equacao');

  console.log('\n5c. As tres equacoes, na tela');
  // Pedido do usuario em 2026-09-24. O guarda vive aqui, e nao so no harness de node,
  // porque o que pode dar errado e de RENDERIZACAO: um segundo grafico que nasce
  // dentro de um cartao com largura zero, ou uma faixa que o Plotly nao pinta.
  const duas = await aval(`(() => {
    function plot(id) {
      const f = document.getElementById(id);
      return { tem: !!f, traces: f ? f.data.length : 0,
               faixa: f ? f.data.filter((t) => t.fill === 'tonexty').length : 0,
               largura: f && f._fullLayout ? f._fullLayout.width : 0,
               eixo: f && f._fullLayout ? (f._fullLayout.yaxis.title.text || '') : '' };
    }
    return {
      cartoes: document.querySelectorAll('#tab-sim .sim-eq-card').length,
      ordem: D.sim.eq_ordem.join(','),
      fx: plot('ch-simfx'), ex: plot('ch-simexp'), is: plot('ch-simis'),
      ip: plot('ch-simipca'),
      titI: document.getElementById('simEqTitulo-I').textContent,
      titE: document.getElementById('simEqTitulo-E').textContent,
      titR: document.getElementById('simEqTitulo-R').textContent,
      titH: document.getElementById('simEqTitulo-H').textContent,
      titF: document.getElementById('simEqTitulo-F').textContent,
      // A ORDEM DOS CARTOES na tela tem de ser a ordem de solucao. Um cartao no lugar
      // errado nao levanta nada e sugere uma causalidade que a conta nao tem.
      ids: Array.from(document.querySelectorAll('#tab-sim .sim-eq-card'))
             .map((c) => c.id).join(','),
    };
  })()`);
  ok(duas.cartoes === 5, 'ha um cartao de equacao para cada uma', String(duas.cartoes));
  ok(duas.ids === 'simEqCard-H,simEqCard-I,simEqCard-E,simEqCard-R,simEqCard-F',
     'e eles aparecem na ORDEM DE SOLUCAO, nao numa ordem qualquer', duas.ids);
  ok(duas.ordem === 'H,I,E,R,F', 'que e a mesma que o payload declara', duas.ordem);
  ok(duas.ip.tem && duas.ip.traces >= 5 && duas.ip.faixa === 1,
     'o grafico da inflacao plotou, com a faixa do posterior',
     duas.ip.traces + ' traces, faixa ' + duas.ip.faixa);
  ok(duas.ip.largura > 100, 'e com largura de verdade', String(duas.ip.largura));
  ok(/12 meses/.test(duas.ip.eixo), 'e o eixo diz que e o IPCA de doze meses',
     duas.ip.eixo);
  ok(/\(I\)/.test(duas.titI) && /inflação do Brasil/.test(duas.titI),
     'e o cartao da (I) diz de que equacao ele e', duas.titI);
  // O laco resolve mil vezes por render, para a faixa. Medido no browser de verdade,
  // porque e o custo que o leitor sente a cada clique.
  const tRender = await aval(`(() => { const t0 = performance.now(); renderSim();
                                        return performance.now() - t0; })()`);
  ok(tRender < 2000, 'um render inteiro, com as mil resolucoes do laco, cabe num clique',
     Math.round(tRender) + ' ms');
  ok(await aval('SIM._ultimo.naoConvergiu') === 0,
     'e todos os desenhos da faixa convergiram');
  ok(duas.is.tem && duas.is.traces >= 3 && duas.is.faixa === 1,
     'o grafico do hiato plotou, com a faixa do posterior',
     duas.is.traces + ' traces, faixa ' + duas.is.faixa);
  ok(duas.is.largura > 100,
     'e com largura de verdade -- nao nasceu dentro de uma caixa de zero',
     String(duas.is.largura));
  ok(/potencial/.test(duas.is.eixo), 'o eixo do hiato nomeia a unidade', duas.is.eixo);
  ok(/\(H\)/.test(duas.titH), 'e o cartao da (H) diz de que equacao ele e', duas.titH);
  ok(duas.fx.tem && duas.fx.traces >= 3,
     'o grafico do cambio plotou', duas.fx.traces + ' traces');
  ok(duas.ex.tem && duas.ex.traces >= 4,
     'e o das expectativas tambem', duas.ex.traces + ' traces');
  ok(duas.fx.faixa === 1 && duas.ex.faixa === 1,
     'os dois com a faixa do posterior',
     duas.fx.faixa + ' / ' + duas.ex.faixa);
  ok(duas.fx.largura > 100 && duas.ex.largura > 100,
     'e com largura de verdade -- nenhum nasceu dentro de uma caixa de zero',
     duas.fx.largura + ' / ' + duas.ex.largura);
  ok(/real|dólar/i.test(duas.fx.eixo), 'o eixo do cambio e o NIVEL em reais',
     duas.fx.eixo);
  ok(/12 meses/.test(duas.ex.eixo),
     'e o das expectativas nomeia o horizonte', duas.ex.eixo);
  ok(/\(E\)/.test(duas.titE) && /\(R\)/.test(duas.titR) && /\(F\)/.test(duas.titF),
     'e cada cartao diz de que equacao ele e',
     duas.titE + ' / ' + duas.titR + ' / ' + duas.titF);

  // A CORRENTE INTEIRA, medida na tela: mexer na inflacao do trimestre tem de mover a
  // expectativa, a Selic, o hiato e o cambio -- de uma vez so. E o que prova que os
  // quatro elos estao ligados; cada um deles se desfaz em silencio. Aplicar o choque
  // IMPOE a inflacao, o que desliga a (I): o que se mede aqui e o que sai dela.
  const antesCad = await aval(`(() => ({
    pie: SIM._ultimo.exp.cam[SIM._ultimo.exp.cam.length - 1],
    selic: SIM._ultimo.cam[SIM._ultimo.cam.length - 1],
    hiato: SIM._ultimo.is.cam[SIM._ultimo.is.cam.length - 1],
    cambio: SIM._ultimo.fx.nivel[SIM._ultimo.fx.nivel.length - 1],
  }))()`);
  await clica('#simcard-infl_br [data-choque="infl_br"]');
  await esperar(500);
  await mexe('#simcard-infl_br [data-chq="v"]', 1);
  await clica('#simcard-infl_br [data-aplica="infl_br"]');
  await esperar(1000);
  const depCad = await aval(`(() => ({
    pie: SIM._ultimo.exp.cam[SIM._ultimo.exp.cam.length - 1],
    selic: SIM._ultimo.cam[SIM._ultimo.cam.length - 1],
    hiato: SIM._ultimo.is.cam[SIM._ultimo.is.cam.length - 1],
    cambio: SIM._ultimo.fx.nivel[SIM._ultimo.fx.nivel.length - 1],
  }))()`);
  ok(depCad.pie > antesCad.pie,
     '(I) -> (E): mais inflacao no trimestre sobe a expectativa',
     antesCad.pie.toFixed(3) + ' -> ' + depCad.pie.toFixed(3));
  ok(depCad.selic > antesCad.selic,
     '(E) -> (R): e a Selic sobe atras dela',
     antesCad.selic.toFixed(3) + ' -> ' + depCad.selic.toFixed(3));
  ok(depCad.hiato < antesCad.hiato,
     '(R) -> (H): e o hiato cai atras da Selic -- o juro chega ao produto',
     antesCad.hiato.toFixed(3) + ' -> ' + depCad.hiato.toFixed(3));
  ok(Math.abs(depCad.cambio - antesCad.cambio) > 1e-6,
     '(R) -> (F): e o cambio se mexe atras da Selic -- a corrente fecha',
     antesCad.cambio.toFixed(4) + ' -> ' + depCad.cambio.toFixed(4));
  await clica('#simcard-infl_br [data-reset="infl_br"]');
  await esperar(700);

  // O ELO (R) -> (F) isolado: subir a Selic pelo juro real tem de mover o cambio.
  const camAntes = await aval(
    `SIM._ultimo.fx.nivel[SIM._ultimo.fx.nivel.length - 1]`);
  // O link de choque e um ALTERNA e o estado sobrevive ao re-render: a secao anterior
  // ja o abriu, entao clicar aqui FECHARIA o painel -- e os seletores seguintes nao
  // achariam nada, reprovando uma pagina correta. Mesma armadilha do "abrir em
  // partes", que custou uma falha em 2026-09-22.
  if (await aval(`!!SIM.chqAberto.rr_10a`) !== true) {
    await clica('#simcard-rr_10a [data-choque="rr_10a"]');
    await esperar(500);
  }
  await mexe('#simcard-rr_10a [data-chq="v"]', 4);
  await clica('#simcard-rr_10a [data-aplica="rr_10a"]');
  await esperar(900);
  const dep = await aval(`(() => ({
    selic: SIM._ultimo.cam[SIM._ultimo.cam.length - 1],
    cambio: SIM._ultimo.fx.nivel[SIM._ultimo.fx.nivel.length - 1],
  }))()`);
  ok(dep.cambio !== camAntes,
     'um choque que sobe a Selic CHEGA ao cambio: as equacoes estao ligadas',
     camAntes.toFixed(4) + ' -> ' + dep.cambio.toFixed(4));
  ok(dep.cambio < camAntes,
     'e na direcao certa -- juro mais alto, real mais forte',
     'R$ ' + dep.cambio.toFixed(4));
  await clica('#simcard-rr_10a [data-reset="rr_10a"]');
  await esperar(700);

  console.log('\n5b. Clique-expande do grafico, SO nesta aba');
  // Pedido em 2026-09-24 e corrigido no mesmo dia em duas frentes: o ESCOPO (a aba do
  // simulador, nao o relatorio inteiro) e a AFORDANCIA (a mesma dos grupos do bloco 2 --
  // um botao de 22px no canto do cartao nao le como clique-expande). O guarda vive aqui
  // e nao no harness de node porque o que pode dar errado e de layout: um plot que volta
  // de `display:none` mede zero.
  const esc = await aval(`(() => {
    const h = document.querySelector('#tab-sim .chart-card .chart-head');
    const o = document.querySelector('#tab-dados .chart-card .chart-head');
    return {
      sim: document.querySelectorAll('#tab-sim .chart-card').length,
      fora: document.querySelectorAll('.chart-card').length
            - document.querySelectorAll('#tab-sim .chart-card').length,
      cursor: getComputedStyle(h).cursor,
      caret: getComputedStyle(h, '::before').content,
      outroCursor: o ? getComputedStyle(o).cursor : 'sem cartao',
      outroCaret: o ? getComputedStyle(o, '::before').content : 'sem cartao',
    };
  })()`);
  ok(esc.sim === (await aval('D.sim.eq_ordem.length')),
     'a aba do simulador tem um cartao de grafico por equacao', String(esc.sim));
  ok(esc.cursor === 'pointer', 'o cabecalho dele e clicavel', esc.cursor);
  ok(esc.caret.indexOf('+') < 0 && esc.caret !== 'none',
     'e traz o caret aberto, como os grupos do bloco 2', esc.caret);
  // O ESCOPO: as outras seis abas nao foram mexidas.
  ok(esc.fora > 0, 'ha cartoes de grafico fora da aba do simulador', String(esc.fora));
  ok(esc.outroCursor !== 'pointer' && esc.outroCaret === 'none',
     'e nenhum deles ganhou caret nem virou clicavel',
     esc.outroCursor + ' / ' + esc.outroCaret);

  const largAntes = await aval(
    `document.getElementById('ch-sim')._fullLayout.width`);
  await clica('#tab-sim .chart-card .chart-head');
  await esperar(500);
  const fech = await aval(`(() => {
    const card = document.querySelector('#tab-sim .chart-card');
    const plot = card.querySelector('.chart-plot');
    const h = card.querySelector('.chart-head');
    return { classe: card.className,
             visivel: plot.offsetParent !== null || plot.offsetHeight > 0,
             cab: !!h.textContent.trim(),
             caret: getComputedStyle(h, '::before').content };
  })()`);
  ok(/recolhido/.test(fech.classe) && !fech.visivel,
     'clicar no cabecalho recolhe o grafico', fech.classe);
  ok(fech.cab === true,
     'e o cabecalho FICA -- um cartao recolhido continua dizendo o que e');
  ok(fech.caret.indexOf('+') >= 0, 'o caret vira +', fech.caret);

  // O estado tem de sobreviver a troca de aba, que e quando `ligarDobraGraficos` roda
  // de novo -- se ele nascesse do DOM, reabriria sozinho.
  await clica('.tab-btn[data-tab="tab-dados"]');
  await esperar(900);
  await clica('.tab-btn[data-tab="tab-sim"]');
  await esperar(1200);
  ok(await aval(
     `document.querySelector('#tab-sim .chart-card').className.indexOf('recolhido') >= 0`),
     'e o recolhido sobrevive a ida e volta de aba');

  await clica('#tab-sim .chart-card .chart-head');
  await esperar(900);
  const largDepois = await aval(
    `document.getElementById('ch-sim')._fullLayout.width`);
  ok(largDepois > 100 && Math.abs(largDepois - largAntes) < 2,
     'ao reabrir, o Plotly remede o grafico em vez de voltar com largura zero',
     largAntes + ' -> ' + largDepois);

  // A aba Impulso-resposta: os controles nascem de `innerHTML`, entao o clique e a troca
  // de alvo so se provam aqui.
  console.log('\n5b. Impulso-resposta');
  const tIrf = Date.now();
  await clica('.tab-btn[data-tab="tab-irf"]');
  await esperar(300);
  const msIrf = Date.now() - tIrf;
  const irfDivs = ['ch-irf-hiato', 'ch-irf-infl', 'ch-irf-pie', 'ch-irf-selic', 'ch-irf-de',
                   'ch-irf-g-IS', 'ch-irf-g-IA', 'ch-irf-g-II', 'ch-irf-g-IM'];
  const irfP = await aval(`(() => ${JSON.stringify(irfDivs)}.map((d) => {
    const e = document.getElementById(d);
    return { d, n: e && e.data ? e.data.length : 0,
             tipo: e && e._fullLayout ? e._fullLayout.xaxis.type : null,
             cab: e ? e.closest('.chart-card').querySelectorAll('.chart-head').length : 0 };
  }))()`);
  ok(irfP.every((x) => x.n === 3), 'os nove graficos pintam: faixa e resposta',
     irfP.filter((x) => x.n !== 3).map((x) => x.d).join(',') || 'todos');
  ok(irfP.every((x) => x.tipo === 'linear'), 'o eixo de trimestres resolve linear, nao data');
  ok(irfP.every((x) => x.cab === 1), 'um cabecalho por cartao');
  ok(msIrf < 8000, 'a primeira pintura, com as faixas, cabe em segundos', msIrf + ' ms');
  const msTroca = await aval(`(() => {
    const e = document.querySelector('#irfBar select[data-irf="alvo"]');
    e.value = 'res:IA';
    const t0 = performance.now();
    e.dispatchEvent(new Event('change', { bubbles: true }));
    return performance.now() - t0;
  })()`);
  ok(await aval(`IRF._ult.alvo.key`) === 'res:IA', 'trocar o alvo no seletor recalcula',
     Math.round(msTroca) + ' ms');
  ok(Math.abs(await aval(`document.getElementById('ch-irf-g-IA').data[2].y[0]`) - 1) < 0.02,
     'e o grafico de alimentacao passa a responder ~1 p.p. no impacto');
  ok(await aval(`document.querySelectorAll('#irfBar input[data-irf="rho"]').length`) === 1,
     'a barra refeita traz os campos da forma do alvo novo');
  await mexe('#irfBar select[data-irf="tipo"]', 'const');
  ok(await aval(`document.querySelectorAll('#irfBar input[data-irf="n"]').length`) === 1
       && await aval(`IRF.chq['res:IA'].tipo`) === 'const',
     'trocar a forma troca os campos');
  await mexe('#irfBar input[data-irf="v"]', '2');
  ok(await aval(`IRF.chq['res:IA'].v`) === 2
       && Math.abs(await aval(`document.getElementById('ch-irf-g-IA').data[2].y[0]`) - 2) < 0.04,
     'e o tamanho novo chega ao grafico');
  await clica('#irfPill12');
  ok(/12 meses/.test(await aval(
       `document.getElementById('ch-irf-infl').closest('.chart-card').querySelector('.chart-title').textContent`)),
     'o seletor de inflacao passa os graficos para 12 meses');
  await clica('#irfPillTri');

  console.log('\n6. Nada quebrou nas outras abas');
  for (const t of ['tab-dados', 'tab-modelo', 'tab-exp', 'tab-is', 'tab-tay',
                   'tab-fx', 'tab-sim', 'tab-irf']) {
    await clica('.tab-btn[data-tab="' + t + '"]');
    await esperar(1100);
  }
  const ex2 = c.eventos.filter((e) => e.method === 'Runtime.exceptionThrown');
  ok(ex2.length === 0, 'zero excecoes depois de visitar as oito abas',
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
