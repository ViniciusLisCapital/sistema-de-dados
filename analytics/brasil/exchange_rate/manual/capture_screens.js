// Screenshots of the delivered FX Report for the reading guide (generate_manual_pdf.py).
//
//   node capture_screens.js "<path to FX Report.html>" "<output dir>"
//
// Drives a real headless Chrome over the DevTools protocol with Node's built-in
// WebSocket (no npm dependency -- same route as the browser checks in this repo).
// Needs network: the report pulls Plotly from a CDN.
//
// For every section it writes <name>.png, cropped from the section's controls bar
// (or its first card) down to the bottom of its chart card, so the prose notes the
// guide already explains are left out of the picture. It also writes anatomy.json:
// the boxes of the controls the guide's first section numbers on the BOP picture,
// in the picture's own pixel coordinates.
const { spawn } = require('child_process');
const fs = require('fs');
const path = require('path');

const file = process.argv[2];
const outDir = process.argv[3];
const DSF = 1.25;
const WIDTH = 1440;
const port = 9400 + Math.floor(Math.random() * 400);
const chrome = spawn('C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe', [
  '--headless=new', `--remote-debugging-port=${port}`, '--hide-scrollbars',
  '--user-data-dir=' + path.join(process.env.TEMP || '.', 'lis_manual_cdp_' + port), 'about:blank',
]);
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

// [output name, tab id, top element selector, bottom element selector, optional setup JS]
const SHOTS = [
  ['bop_tree', 'tab-bop', '#sec-bop-tree .chart-ctrl', '#sec-bop-tree .chart-card'],
  ['comex_pais', 'tab-bop', '#sec-comex-pais .chart-ctrl', '#sec-comex-pais .chart-card'],
  ['comex_fator', 'tab-bop', '#sec-comex-fator .chart-ctrl', '#sec-comex-fator .chart-card'],
  ['comex_produto', 'tab-bop', '#sec-comex-produto .chart-ctrl', '#sec-comex-produto .chart-card'],
  ['flow_contratado', 'tab-flow', '#sec-flow-contratado .chart-ctrl', '#sec-flow-contratado .chart-card'],
  ['flow_detalhe', 'tab-flow', '#sec-flow-detalhe .chart-ctrl', '#sec-flow-detalhe .chart-card'],
  ['flow_interbank', 'tab-flow', '#sec-flow-interbank .chart-ctrl', '#sec-flow-interbank .chart-card'],
  ['bcb_reserves', 'tab-bcb', '#sec-bcb-reserves-tree .chart-ctrl', '#sec-bcb-reserves-tree .chart-card'],
  ['bcb_swap', 'tab-bcb', '#sec-bcb-swap .chart-ctrl', '#sec-bcb-swap .chart-card'],
  ['bcb_intervention', 'tab-bcb', '#sec-bcb-intervention .chart-ctrl', '#sec-bcb-intervention .chart-card'],
  ['bcb_cot', 'tab-bcb', '#sec-bcb-cot .chart-ctrl', '#sec-bcb-cot .chart-card'],
  ['val_ptax', 'tab-valuation', '#sec-valuation-ptax .chart-card', '#sec-valuation-ptax .chart-card'],
  ['val_reer', 'tab-valuation', '#sec-valuation-reer .chart-card', '#sec-valuation-reer .chart-card'],
  ['val_termos', 'tab-valuation', '#sec-valuation-termos .chart-card', '#sec-valuation-termos .chart-card'],
  ['ppp_controls', 'tab-data', '#tab-data .controls', '#statsRow'],
  ['ppp_main', 'tab-data', '.chart-container:has(#mainChart)', '.chart-container:has(#mainChart)'],
  ['ppp_dev', 'tab-data', '.chart-container:has(#devChart)', '.chart-container:has(#devChart)'],
  ['fxattr_top', 'tab-fxattr', '#fxattrManagerSelect', '#fxattrStatsRow',
    "(function(){var s=document.getElementById('fxattrManagerSelect');var o=[...s.options].find(o=>/Verde/.test(o.textContent));if(o){s.value=o.value;s.dispatchEvent(new Event('change'));}})()"],
  ['fxattr_dir', 'tab-fxattr', '.chart-container:has(#fxattrDirChart)', '.chart-container:has(#fxattrDirChart)'],
  ['fxattr_mag', 'tab-fxattr', '.chart-container:has(#fxattrMagChart)', '.chart-container:has(#fxattrMagChart)'],
  ['fxattr_claims', 'tab-fxattr', '#fxattrCategorySelect', '#fxattrClaimsTable tr:nth-child(7)'],
];

(async () => {
  let t;
  for (let i = 0; i < 60; i++) {
    try { t = (await (await fetch(`http://127.0.0.1:${port}/json/list`)).json()).find((x) => x.type === 'page'); if (t) break; } catch (e) {}
    await sleep(200);
  }
  if (!t) throw new Error('Chrome did not start');
  const ws = new WebSocket(t.webSocketDebuggerUrl);
  await new Promise((r) => ws.addEventListener('open', r));
  let id = 0; const pend = {}; const errors = [];
  ws.addEventListener('message', (ev) => {
    const m = JSON.parse(ev.data);
    if (m.id && pend[m.id]) { pend[m.id](m); delete pend[m.id]; }
    if (m.method === 'Runtime.exceptionThrown') errors.push(m.params.exceptionDetails.exception?.description || m.params.exceptionDetails.text);
  });
  const send = (method, params = {}) => new Promise((r) => { const i = ++id; pend[i] = r; ws.send(JSON.stringify({ id: i, method, params })); });
  const ev = async (expr) => {
    const r = await send('Runtime.evaluate', { expression: expr, awaitPromise: true, returnByValue: true });
    if (r.result.exceptionDetails) throw new Error(expr.slice(0, 120) + ' -> ' + JSON.stringify(r.result.exceptionDetails.exception?.description));
    return r.result.result.value;
  };
  await send('Runtime.enable'); await send('Page.enable');
  await send('Emulation.setDeviceMetricsOverride', { width: WIDTH, height: 1000, deviceScaleFactor: DSF, mobile: false });
  await send('Page.navigate', { url: 'file:///' + path.resolve(file).split(path.sep).join('/') });
  await sleep(15000);

  let currentTab = null;
  const boxOf = (sel) => `(function(){var e=document.querySelector(${JSON.stringify(sel)});if(!e)return null;var r=e.getBoundingClientRect();return {x:r.left+scrollX,y:r.top+scrollY,w:r.width,h:r.height};})()`;

  async function shoot(name, tab, topSel, botSel, setup) {
    if (tab !== currentTab) {
      await ev(`document.querySelector('.tab-btn[data-tab="${tab}"]').click()`);
      await sleep(3000);
      currentTab = tab;
    }
    if (setup) { await ev(setup); await sleep(2500); }
    await ev(`document.querySelector(${JSON.stringify(topSel)}).scrollIntoView()`);
    await sleep(700);
    const a = await ev(boxOf(topSel)); const b = await ev(boxOf(botSel));
    if (!a || !b) throw new Error('missing element for ' + name + ': ' + (!a ? topSel : botSel));
    // The range ruler of a data-tab chart is drawn right after its card, not inside it:
    // extend the bottom to any .range-bar that starts within 60px of the card's bottom.
    const bottom = await ev(`(function(){var e=document.querySelector(${JSON.stringify(botSel)});var r=e.getBoundingClientRect();var b=r.bottom;
      document.querySelectorAll('.range-bar').forEach(function(x){var q=x.getBoundingClientRect();if(q.height>0&&q.top>=r.bottom-5&&q.top<=r.bottom+60)b=Math.max(b,q.bottom);});
      return b+scrollY;})()`);
    // the whole content column, not just the element, so every picture has the same width
    const col = await ev(boxOf('#' + tab));
    const pad = 12;
    const clip = { x: col.x - pad, y: a.y - pad, width: col.w + 2 * pad, height: bottom - a.y + 2 * pad, scale: 1 };
    const shot = await send('Page.captureScreenshot', { format: 'png', captureBeyondViewport: true, clip });
    fs.writeFileSync(path.join(outDir, name + '.png'), Buffer.from(shot.result.data, 'base64'));
    return clip;
  }

  const clips = {};
  for (const [name, tab, top, bot, setup] of SHOTS) {
    clips[name] = await shoot(name, tab, top, bot, setup);
    console.log('ok', name);
  }

  // Anatomy of a section: pin the definition card of the first row, then re-shoot the
  // BOP section with it open, and record where each numbered control sits.
  currentTab = null;
  await ev(`document.querySelector('.tab-btn[data-tab="tab-bop"]').click()`); await sleep(2500);
  currentTab = 'tab-bop';
  await ev(`(function(){var b=document.querySelector('#bop-tree-body .info-btn');b.scrollIntoView({block:'center'});b.click();})()`);
  await sleep(800);
  const clip = await shoot('anatomy', 'tab-bop', '#sec-bop-tree .chart-ctrl', '#sec-bop-tree .chart-card');
  const rel = (bx) => bx && { x: (bx.x - clip.x) * DSF, y: (bx.y - clip.y) * DSF, w: bx.w * DSF, h: bx.h * DSF };
  const anatomy = {
    ctrl: rel(await ev(boxOf('#sec-bop-tree .chart-ctrl'))),
    expand: rel(await ev(boxOf('#btn-bop-expand'))),
    checkbox: rel(await ev(boxOf('#bop-tree-body tr:nth-child(2) input[type=checkbox]'))),
    caret: rel(await ev(boxOf('#bop-tree-body tr:nth-child(3) .tree-toggle'))),
    info: rel(await ev(boxOf('#bop-tree-body tr:nth-child(1) .info-btn'))),
    popover: rel(await ev(boxOf('.info-pop'))),
    head: rel(await ev(boxOf('#sec-bop-tree .chart-head'))),
    range: rel(await ev(boxOf('#sec-bop-tree .range-bar'))),
  };
  fs.writeFileSync(path.join(outDir, 'anatomy.json'), JSON.stringify(anatomy, null, 1));
  if (errors.length) console.log('page exceptions:', errors);
  ws.close(); chrome.kill(); process.exit(errors.length ? 1 : 0);
})().catch((e) => { console.error(e); chrome.kill(); process.exit(2); });
