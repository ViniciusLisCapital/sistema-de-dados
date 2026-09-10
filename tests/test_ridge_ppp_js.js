/*
 * Confere o termo de PPP com coeficiente FIXO EM 1 no arquivo entregue --
 * reports/brasil/FX Report.html, aba Ridge.
 *
 * Por que existe: adicionar o PPP como OFFSET (beta imposto, nao estimado) e
 * uma mudanca que quebra em SILENCIO em tres lugares distintos, e nenhum deles
 * levanta erro.
 *
 *  1. Se alguem tirar o offset da previsao (`fitted_delta`), a ponte de nivel
 *     CONTINUA reconstruindo o PTAX exato -- o residuo absorve a diferenca. O
 *     grafico fica igual e o modelo passa a ser outro.
 *  2. Se o `is_log_return` da serie do PPP mudar, ou se a "level" exposta na
 *     grade de previsao deixar de ser o indice de precos relativos, o
 *     simulador do navegador passa a somar uma quantidade que NAO e o
 *     diferencial de inflacao -- com o mesmo beta 1, sem tell visual.
 *  3. Se o `delta_ppp` entrar na lista de coeficientes ESTIMADOS, o seletor de
 *     coeficiente movel ganha uma linha reta em 1,000 que se le como achado
 *     sobre o dado, e nao como premissa.
 *
 * As assercoes centrais sao identidades, nao numeros de uma amostra: elas
 * continuam valendo quando entrar dado novo.
 *
 * Uso:  node tests/test_ridge_ppp_js.js
 */

const fs = require('fs');
const path = require('path');

// Caminho opcional no argv para o harness de mutantes conseguir apontar para
// uma copia adulterada sem mexer no arquivo entregue.
const HTML = process.argv[2] || path.join(__dirname, '..', 'reports', 'brasil', 'FX Report.html');

let falhas = 0, oks = 0;
function ok(cond, msg, extra) {
  if (cond) { oks++; console.log('  ok      ' + msg); }
  else { falhas++; console.log('  FALHOU  ' + msg + (extra ? '  -> ' + extra : '')); }
}
function sec(t) { console.log('\n' + t); }
function perto(a, b, tol) { return Math.abs(a - b) <= tol; }

const src = fs.readFileSync(HTML, 'utf8');

// ---------------------------------------------------------------------------
// payload
// ---------------------------------------------------------------------------
const m = src.match(/^const RIDGE_DATA = (\{.*\});$/m);
if (!m) { console.log('FALHOU: RIDGE_DATA nao encontrado (build com include_models=False?)'); process.exit(1); }
const D = JSON.parse(m[1]);

const PPP = 'delta_ppp';
const CM = D.contrib_monthly;
const n = D.months.length;

sec('1. o PPP esta no modelo, com o coeficiente IMPOSTO em 1');
ok(D.whole_sample.beta[PPP] === 1, 'beta do PPP no ajuste global e exatamente 1',
   String(D.whole_sample.beta[PPP]));
ok(D.last_window.beta[PPP] === 1, 'e na ultima janela tambem');
ok(D.forecast.beta[PPP] === 1, 'e o simulador recebe o mesmo 1');
const st = D.forecast.channel_stats[PPP];
ok(st && st.mean === 0 && st.std === 1,
   'as estatisticas do PPP sao a identidade (entra cru, nao z-scored)', JSON.stringify(st));
ok(!(PPP in D.rolling.channels),
   'e ele NAO aparece entre os coeficientes moveis (nao e estimado)');
ok(PPP in CM, 'a decomposicao tem uma barra propria para o PPP');
ok(!('delta_ppp' in { ...CM, delta_ppp: undefined }) === false, 'sanidade do harness');

sec('2. a barra do PPP e mesmo o diferencial de inflacao');
// A serie de "nivel" que a grade de previsao expoe tem de reproduzir, ao ser
// diferenciada como log-retorno, exatamente a contribuicao mensal do PPP. E o
// que amarra o simulador do navegador ao ajuste feito no servidor.
const hist = D.forecast.channel_history.ppp;
ok(!!hist, 'a grade de previsao expoe uma serie de nivel para o PPP');
ok(hist && hist.is_log_return === true,
   'marcada como log-retorno -- e o que faz a caixa virar diferencial de inflacao');
// 2026-09-08: a serie passou a vir na historia INTEIRA (ver a secao 14), entao
// a amostra do ajuste e a CAUDA dela. O deslocamento e derivado do proprio mes,
// nunca de um slice(-n) -- se a cauda deixar de bater com D.months, e isso que
// tem de reprovar, e nao uma reconstrucao deslocada que continua fechando.
const offPpp = hist ? hist.months.indexOf(D.months[0]) : -1;
ok(offPpp >= 0 && hist.months.slice(offPpp).join(',') === D.months.join(','),
   'a cauda da serie e exatamente a amostra do ajuste, mes a mes');
const hv = hist ? hist.values.slice(offPpp) : [];
ok(hv.length === n, 'com um ponto por mes da amostra', hv.length + ' vs ' + n);
let piorRecon = 0;
for (let i = 1; i < n; i++) {
  const recalc = 100 * Math.log(hv[i] / hv[i - 1]);
  piorRecon = Math.max(piorRecon, Math.abs(recalc - CM[PPP][i]));
}
ok(piorRecon < 5e-3,
   'diferenciar a serie de nivel reproduz a contribuicao mensal do PPP',
   'pior erro ' + piorRecon.toExponential(2));

// Identidade que nao envelhece: o acumulado da barra e o log-retorno do indice
// entre as duas pontas da amostra.
// Do SEGUNDO mes em diante: a barra do primeiro mes e a diferenca contra o mes
// ANTERIOR a amostra, que a serie de nivel exposta aqui nao carrega.
const acumPPP = CM[PPP].reduce((s, v) => s + v, 0);
const acumPPPdo2 = CM[PPP].slice(1).reduce((s, v) => s + v, 0);
const pontaAponta = 100 * Math.log(hv[n - 1] / hv[0]);
ok(perto(acumPPPdo2, pontaAponta, 0.02),
   'o acumulado da barra do PPP e o movimento ponta a ponta do indice relativo',
   acumPPPdo2.toFixed(3) + ' vs ' + pontaAponta.toFixed(3));

sec('3. o offset esta DENTRO da previsao, nao no residuo');
// Esta e a assercao que pega a regressao silenciosa numero 1. A previsao tem de
// ser a soma de TODAS as barras menos o residuo; se o offset sair do
// fitted_delta, o residuo cresce por exatamente o PPP e a ponte de nivel
// continua fechando.
const buckets = Object.keys(CM).filter(k => k !== 'residual');
let piorFit = 0, piorRes = 0;
for (let i = 0; i < n; i++) {
  const soma = buckets.reduce((s, k) => s + CM[k][i], 0);
  piorFit = Math.max(piorFit, Math.abs(soma - D.fit_delta.fitted[i]));
  piorRes = Math.max(piorRes, Math.abs((D.fit_delta.actual[i] - D.fit_delta.fitted[i]) - CM.residual[i]));
}
ok(piorFit < 5e-3, 'a previsao mensal e a soma das barras (PPP incluido)',
   'pior erro ' + piorFit.toExponential(2));
ok(piorRes < 5e-3, 'e o residuo e o que sobra dela', 'pior erro ' + piorRes.toExponential(2));
// e o residuo NAO pode carregar a tendencia do PPP
const acumRes = CM.residual.reduce((s, v) => s + v, 0);
ok(Math.abs(acumRes) < Math.abs(acumPPP) / 10,
   'o residuo acumulado e pequeno perto da barra do PPP -- a tendencia nao voltou para la',
   'residuo ' + acumRes.toFixed(2) + ' vs ppp ' + acumPPP.toFixed(2));

sec('4. a ponte de nivel continua fechando no PTAX real');
const L = D.level_decomposition;
ok('delta_ppp' in L, 'a ponte tem a camada do PPP');
let piorPonte = 0;
for (let i = 0; i < n; i++) {
  let soma = 0;
  for (const k of Object.keys(L)) if (k !== 'actual') soma += L[k][i];
  piorPonte = Math.max(piorPonte, Math.abs(soma - L.actual[i]));
}
ok(piorPonte < 1e-2, 'somando todas as camadas volta o PTAX observado',
   'pior erro ' + piorPonte.toExponential(2));

sec('5. o alpha deixou de carregar a tendencia');
// Sem numero de amostra: o teste e comparativo e sobrevive a dado novo. O PPP
// tem de ser uma parcela GRANDE do movimento acumulado, e o que sobra para a
// constante nao pode ser o total de antes.
const acumFx = D.fit_delta.actual.reduce((s, v) => s + v, 0);
ok(acumPPP > 0.25 * acumFx,
   'o PPP responde por mais de um quarto do movimento acumulado do cambio',
   (100 * acumPPP / acumFx).toFixed(1) + '%');
const acumBase = CM.baseline.reduce((s, v) => s + v, 0);
ok(acumBase < acumFx,
   'e o balde Baseline (ancora + alpha + AR1) ja nao responde por quase tudo',
   (100 * acumBase / acumFx).toFixed(1) + '%');

// Canais ESTIMADOS do payload: tudo que tem beta menos o offset e o AR(1).
const canais = Object.keys(D.whole_sample.beta)
  .filter(k => k !== PPP && k !== 'delta_fx_lag1')
  .map(k => k.replace(/^delta_/, '')).sort();

sec('6. a banda de erro pertence a ESTE modelo');
const B = D.forecast_error_bands;
// A tag tem de declarar o offset E o conjunto de canais. window/horizon ficam
// identicos quando o modelo muda, entao sem isso o cache antigo seria
// reaproveitado e a banda entregue descreveria um modelo que a pagina nao roda.
ok(B && String(B.spec).startsWith('ppp_offset_b1|'),
   'o cache da banda declara a spec com PPP', B ? String(B.spec) : 'ausente');
ok(B && String(B.spec) === 'ppp_offset_b1|' + canais.join(','),
   'e o conjunto de canais da banda e o MESMO que o ajuste entregue usa',
   B ? String(B.spec) + '  vs  ' + canais.join(',') : 'ausente');
ok(B && B.std_error_pct[0] < B.std_error_pct[B.std_error_pct.length - 1],
   'e a banda continua abrindo com o horizonte');

// ---------------------------------------------------------------------------
// JS da aba
// ---------------------------------------------------------------------------
sec('7. a aba trata o PPP como termo fixo, nao como coeficiente estimado');
const ordem = src.match(/const CHANNEL_ORDER_RIDGE = \[([\s\S]*?)\];/);
ok(!!ordem && /'delta_ppp'/.test(ordem[1]), 'delta_ppp esta na ordem de canais da aba');
ok(!!ordem && ordem[1].trim().startsWith("'delta_ppp'"),
   'e vem primeiro -- e identidade, nao mais um canal estimado');
ok(/const PINNED_PARAMS_RIDGE = \[[^\]]*'delta_ppp'/.test(src),
   'declarado como parametro fixo');
ok(/paramKeys = \['alpha', \.\.\.CHANNEL_ORDER_RIDGE\.filter\(k => !PINNED_PARAMS_RIDGE\.includes\(k\)\)\]/.test(src),
   'o seletor de coeficiente movel filtra os fixos');
ok(/delta_ppp: 'PPP \(β fixed at 1\)'/.test(src) || /delta_ppp: 'PPP \(β fixed at 1\)'/.test(src),
   'o rotulo do parametro diz que o beta e fixo');
ok(/delta_ppp: 'PPP \(BR-US inflation differential\)'/.test(src),
   'e o rotulo da serie nomeia o que ela mede');
ok(/PINNED_PARAMS_RIDGE\.includes\(k\)\)[\s\S]{0,200}sort\(\(a, b\) => Math\.abs\(FC\.beta\[b\]\)/.test(src),
   'e o ranking dos cartoes de previsao tira os fixos da comparacao por |beta|');

sec('8. as cores das series sao distinguiveis (regra do lis-dashboard)');
const mapaCor = src.match(/const CHANNEL_COLORS_RIDGE = \{([\s\S]*?)\n  \};/);
ok(!!mapaCor, 'mapa de cores encontrado');
const cores = {};
if (mapaCor) for (const mm of mapaCor[1].matchAll(/(\w+): '(#[0-9A-Fa-f]{6})'/g)) cores[mm[1]] = mm[2];
ok('delta_ppp' in cores, 'delta_ppp tem cor propria');

function lab(hex) {
  const v = [1, 3, 5].map(i => parseInt(hex.substr(i, 2), 16) / 255)
    .map(c => c <= 0.04045 ? c / 12.92 : Math.pow((c + 0.055) / 1.055, 2.4));
  const X = v[0] * 0.4124564 + v[1] * 0.3575761 + v[2] * 0.1804375;
  const Y = v[0] * 0.2126729 + v[1] * 0.7151522 + v[2] * 0.0721750;
  const Z = v[0] * 0.0193339 + v[1] * 0.1191920 + v[2] * 0.9503041;
  const g = t => t > 216 / 24389 ? Math.cbrt(t) : (841 / 108) * t + 4 / 29;
  const fx = g(X / 0.95047), fy = g(Y), fz = g(Z / 1.08883);
  return [116 * fy - 16, 500 * (fx - fy), 200 * (fy - fz)];
}
function deltaE(h1, h2) {
  const [L1, a1, b1] = lab(h1), [L2, a2, b2] = lab(h2);
  const C1 = Math.hypot(a1, b1), C2 = Math.hypot(a2, b2), Cb = (C1 + C2) / 2;
  const G = 0.5 * (1 - Math.sqrt(Math.pow(Cb, 7) / (Math.pow(Cb, 7) + Math.pow(25, 7))));
  const a1p = (1 + G) * a1, a2p = (1 + G) * a2;
  const C1p = Math.hypot(a1p, b1), C2p = Math.hypot(a2p, b2);
  const h1p = (Math.atan2(b1, a1p) * 180 / Math.PI + 360) % 360;
  const h2p = (Math.atan2(b2, a2p) * 180 / Math.PI + 360) % 360;
  const dLp = L2 - L1, dCp = C2p - C1p;
  let dhp = 0;
  if (C1p * C2p !== 0) {
    dhp = h2p - h1p;
    if (dhp > 180) dhp -= 360; else if (dhp < -180) dhp += 360;
  }
  const dHp = 2 * Math.sqrt(C1p * C2p) * Math.sin(dhp * Math.PI / 360);
  const Lb = (L1 + L2) / 2, Cbp = (C1p + C2p) / 2;
  let hbp;
  if (C1p * C2p === 0) hbp = h1p + h2p;
  else if (Math.abs(h1p - h2p) <= 180) hbp = (h1p + h2p) / 2;
  else hbp = h1p + h2p < 360 ? (h1p + h2p + 360) / 2 : (h1p + h2p - 360) / 2;
  const r = d => d * Math.PI / 180;
  const T = 1 - 0.17 * Math.cos(r(hbp - 30)) + 0.24 * Math.cos(r(2 * hbp))
    + 0.32 * Math.cos(r(3 * hbp + 6)) - 0.20 * Math.cos(r(4 * hbp - 63));
  const dth = 30 * Math.exp(-Math.pow((hbp - 275) / 25, 2));
  const Rc = 2 * Math.sqrt(Math.pow(Cbp, 7) / (Math.pow(Cbp, 7) + Math.pow(25, 7)));
  const Sl = 1 + 0.015 * Math.pow(Lb - 50, 2) / Math.sqrt(20 + Math.pow(Lb - 50, 2));
  const Sc = 1 + 0.045 * Cbp, Sh = 1 + 0.015 * Cbp * T;
  const Rt = -Math.sin(r(2 * dth)) * Rc;
  return Math.sqrt(Math.pow(dLp / Sl, 2) + Math.pow(dCp / Sc, 2) + Math.pow(dHp / Sh, 2)
    + Rt * (dCp / Sc) * (dHp / Sh));
}
let piorPPP = Infinity, viz = '';
for (const [k, v] of Object.entries(cores)) {
  if (k === 'delta_ppp') continue;
  const d = deltaE(cores.delta_ppp, v);
  if (d < piorPPP) { piorPPP = d; viz = k; }
}
ok(piorPPP >= 20,
   'a cor do PPP fica a CIEDE2000 >= 20 da vizinha mais proxima',
   'pior par: ' + viz + ' dE=' + piorPPP.toFixed(1));

sec('9. a prosa explica para quem nunca viu o dashboard');
// Fatiado no painel da aba do modelo. A aba FX Attribution tem uma secao com o
// MESMO titulo e vem ANTES no arquivo -- casar direto pega o painel errado, e
// foi exatamente esse descuido que apagou a aba FX Attribution inteira numa
// edicao de 2026-09-01 (pego por tests/test_fx_report_js.js §14b, que exige um
// painel para cada botao). Ancore sempre no painel.
const painelRidge = (src.match(/id="tab-ridge"([\s\S]*?)<!-- \/tab-ridge -->/) || [, ''])[1];
const intro = (painelRidge.match(/id="ridgeMethodFold"([\s\S]*?)<\/details>/) || [, ''])[1];
ok(intro.length > 500, 'o bloco de introducao da aba Ridge foi localizado',
   intro.length + ' caracteres');
ok(/coefficient fixed at 1, not fitted/.test(intro),
   'a equacao avisa que o coeficiente do PPP e fixo');
ok(/Brazilian prices rise faster than American ones/.test(intro) &&
   /inflation gap/.test(intro),
   'e o paragrafo do PPP diz o que ele mede em linguagem comum');
ok(!/ppp_offset|offset_col|delta_ppp|build_plain_regression_sample|Ridge\(|sklearn/.test(intro),
   'sem nome de variavel, funcao ou biblioteca no texto do leitor');
ok(!/2026-0[0-9]-[0-9]{2}|Desde 2026|direct user request/.test(intro),
   'sem data de decisao nem referencia a pedido do usuario');
// O texto nao pode voltar a afirmar que o PPP esta FORA do modelo. Duas formas
// de dizer isso, ambas do texto anterior a 2026-09-01 e ambas agora falsas.
ok(!/absorbs its average drift/i.test(intro),
   'a prosa nao diz mais que o alfa absorve a deriva do PPP');
ok(!/(PPP|inflation gap)[^.]{0,140}(is|was|it is) excluded/i.test(intro),
   'nem que o PPP foi excluido do modelo');


// ---------------------------------------------------------------------------
// 10. o bloco das abas de MODELO roda de verdade
// ---------------------------------------------------------------------------
// Vale um teste proprio por causa do gotcha registrado no CLAUDE.md desta pasta:
// as tres abas de modelo dividem UM <script>, entao um throw em qualquer uma
// aborta o bloco inteiro e as tres saem em branco -- sem mensagem, sem erro
// visivel na pagina. Uma chave nova nos mapas do Ridge e exatamente o tipo de
// mudanca que pode disparar isso.
//
sec('10. o bloco das abas de modelo continua valido');
// O CLAUDE.md desta pasta registra o gotcha que justifica olhar para isto: as
// tres abas de modelo dividem UM <script>, entao um erro em qualquer uma aborta
// o bloco inteiro e as tres saem em branco, sem mensagem na pagina.
//
// O que esta assercao cobre e SINTAXE, nao execucao. Executar o bloco de verdade
// exige o stub de DOM completo que tests/test_fx_report_js.js mantem para o
// primeiro bloco; um stub generico (Proxy que responde qualquer propriedade) foi
// tentado e produz FALSO NEGATIVO -- a aba PPP quebra no stub, nao no produto.
// Enquanto nao houver esse harness, a renderizacao das abas de modelo segue
// verificada so em browser real, e isto aqui pega o erro mais barato.
const blocos = [...src.matchAll(/<script(?![^>]*\bsrc=)[^>]*>([\s\S]*?)<\/script>/g)].map(x => x[1]);
ok(blocos.length === 2, 'o relatorio tem os dois blocos inline', blocos.length);
let erroSintaxe = null;
try { new (require('vm').Script)(blocos[1], { filename: 'model-tabs.js' }); }
catch (e) { erroSintaxe = e; }
ok(erroSintaxe === null, 'o bloco das tres abas de modelo e sintaticamente valido',
   erroSintaxe && erroSintaxe.message);

sec('11. a caixa do PPP na previsao nao assume inflacao igual a dos EUA');
// "Plano por default" significa "sem mudanca" para um NIVEL (um CDS parado nao
// contribui nada). Para um INDICE de precos, congelar significa Brasil e EUA
// inflacionando no mesmo ritmo por 12 meses -- que nao e neutro, e uma hipotese
// forte, e enviesaria toda previsao intocada.
ok(/const TREND_SEEDED_RG = \['delta_ppp'\]/.test(src),
   'o PPP e semeado por TENDENCIA, nao plano');
ok(/boxSeedRg\[key\] = drift;/.test(src) && /levels\[key\] = futureMonthsForBoxes\.map\(\(m, h\) => \{[\s\S]{0,220}drift === 0 \? lastVal : lastVal \* Math\.exp\(drift \* \(h \+ 1\) \/ 100\)/.test(src),
   'as 12 caixas iniciais seguem a deriva recente');
ok(/const drift = boxSeedRg\[key\] \|\| 0;[\s\S]{0,260}Math\.exp\(drift \* \(h \+ 1\) \/ 100\)/.test(src),
   'e o botao "Reset shocks" devolve a MESMA semente, nao um indice congelado');
// a deriva semeada tem de ser positiva e da ordem do diferencial recente
const v = hist.values, k = Math.min(12, v.length - 1);
const driftSeed = 100 * Math.log(v[v.length - 1] / v[v.length - 1 - k]) / k;
ok(driftSeed > 0.05 && driftSeed < 1.0,
   'a deriva de 12m e positiva e plausivel para um diferencial mensal de inflacao',
   driftSeed.toFixed(3) + ' pp/mes');
ok(Math.abs(12 * driftSeed - 100 * Math.log(v[v.length - 1] / v[v.length - 1 - 12])) < 1e-9,
   'e 12 meses dela reproduzem o diferencial acumulado de 12 meses');

sec('12. o corte para 5 canais esta consistente de ponta a ponta');
// Um descasamento entre a lista do JS e o channel set do payload nao levanta
// erro: uma chave a mais faz o loop da decomposicao ler undefined, uma a menos
// apaga uma barra em silencio. Aqui as duas listas sao comparadas conjunto a
// conjunto, nao por contagem.
ok(canais.length === 5, 'o payload traz exatamente 5 canais estimados',
   canais.length + ': ' + canais.join(', '));
const ordemJs = (src.match(/const CHANNEL_ORDER_RIDGE = \[([\s\S]*?)\];/) || [, ''])[1]
  .match(/'(\w+)'/g) || [];
const chavesJs = ordemJs.map(x => x.replace(/'/g, ''));
ok(chavesJs.length === 7,
   'a ordem do JS tem 7 chaves (PPP + 5 canais + AR1)', chavesJs.join(', '));
const espera = [PPP, ...canais.map(c => 'delta_' + c), 'delta_fx_lag1'].sort().join(',');
ok(chavesJs.slice().sort().join(',') === espera,
   'e o conjunto do JS e IDENTICO ao do payload',
   chavesJs.slice().sort().join(',') + '  vs  ' + espera);
// cada chave do JS tem de existir nos tres mapas: sem isso a barra sai sem nome
// ou sem cor, e o seletor mostra "undefined"
const rotulos = (src.match(/const CHANNEL_LABELS_RIDGE = \{([\s\S]*?)\n  \};/) || [, ''])[1];
const params = (src.match(/const PARAM_LABELS_RIDGE = \{([\s\S]*?)\n  \};/) || [, ''])[1];
const semRotulo = chavesJs.filter(k => !new RegExp(k + ':').test(rotulos));
const semCor = chavesJs.filter(k => !(k in cores));
const semParam = chavesJs.filter(k => k !== PPP && !new RegExp(k + ':').test(params));
ok(semRotulo.length === 0, 'toda chave tem rotulo de serie', semRotulo.join(', '));
ok(semCor.length === 0, 'toda chave tem cor', semCor.join(', '));
ok(semParam.length === 0, 'e todo coeficiente estimado tem rotulo de parametro', semParam.join(', '));
// mapa orfao = texto ou cor que nenhuma barra usa; nao quebra nada e nunca aparece
const orfaosCor = Object.keys(cores).filter(k => !chavesJs.includes(k));
ok(orfaosCor.length === 0, 'nenhuma cor orfa de canal removido', orfaosCor.join(', '));
const chavesRot = (rotulos.match(/(\w+):/g) || []).map(x => x.replace(':', ''));
const orfaosRot = chavesRot.filter(k => !chavesJs.includes(k));
ok(orfaosRot.length === 0, 'nenhum rotulo orfao', orfaosRot.join(', '));
// a paleta INTEIRA passa na regua, nao so a cor nova: separabilidade e uma
// propriedade do conjunto que esta no grafico junto, entao trocar o channel set
// obriga a remedir
let piorPar = Infinity, quem = '';
const todas = { ...cores, baseline: '#1F2853', residual: '#C9CEDB' };
const ks = Object.keys(todas);
for (let i = 0; i < ks.length; i++) for (let j = i + 1; j < ks.length; j++) {
  const d = deltaE(todas[ks[i]], todas[ks[j]]);
  if (d < piorPar) { piorPar = d; quem = ks[i] + ' x ' + ks[j]; }
}
ok(piorPar >= 20, 'TODOS os pares da paleta do Ridge ficam a CIEDE2000 >= 20',
   'pior par: ' + quem + ' dE=' + piorPar.toFixed(1));
// primitivo de canal removido continuaria custando leitura de banco e viajando
// no payload sem nada para desenhar
const prims = Object.keys(D.forecast.primitives || {});
ok(!prims.includes('br_real_10y') && !prims.includes('br_real_2y') && !prims.includes('us_real_10y'),
   'os primitivos dos canais removidos sairam do payload', prims.join(', '));
ok(Object.keys(D.forecast.composite_primitives || {}).join(',') === 'carry_vol',
   'e so carry_vol continua declarado como composto',
   Object.keys(D.forecast.composite_primitives || {}).join(','));

sec('13. os ajustes de 2026-09-01 na aba FX Model');

// (vi) nome da aba
const navBtns = [...src.matchAll(/<button class="tab-btn" data-tab="(tab-[\w-]+)">([^<]*)<\/button>/g)]
  .map(m => ({ id: m[1], rotulo: m[2] }));
const btnModelo = navBtns.find(b => b.id === 'tab-ridge');
ok(!!btnModelo && btnModelo.rotulo === 'FX Model',
   'a aba se chama "FX Model" no nav', btnModelo ? btnModelo.rotulo : 'sem botao');
ok(!navBtns.some(b => b.rotulo === 'Ridge'), 'e nenhum botao ainda se chama "Ridge"');

// (ii) Descriptive stats
ok(!/ridgeStatsRow/.test(src), 'o elemento da faixa "Descriptive stats" nao existe mais');
ok(!/>Descriptive stats</.test(src), 'nem o titulo dela');
ok(/id="ridgeFitLine"/.test(src) && /As fitted today:/.test(src),
   'e os numeros do ajuste viraram uma linha dentro da metodologia');

// (i) metodologia em click-drop, com a equacao em display
ok(/<details class="fold" id="ridgeMethodFold">/.test(src),
   'a metodologia e um <details> (click-drop)');
ok(!/<details class="fold" id="ridgeMethodFold"[^>]*\sopen/.test(src),
   'fechado por default');
const eqRows = (intro.match(/class="eq-row"/g) || []).length;
ok(eqRows === 9, 'a equacao tem uma linha por termo (5 canais + PPP + alfa + AR1 + residuo)', eqRows);
ok(/eq-fixed/.test(intro), 'e o termo de coeficiente fixo esta marcado a parte');
const termosEq = ['fiscal', 'dxy_em', 'carry_vol', 'sp500', 'icbr_usd'];
const faltamEq = termosEq.filter(t => !new RegExp('&Delta;' + t).test(intro));
ok(faltamEq.length === 0, 'os cinco canais aparecem na equacao', faltamEq.join(', '));
ok(!/&Delta;dxy<|curve_steep_real|real_yield_diff/.test(intro),
   'e nenhum canal removido sobrou na equacao');

// (iii) diagnosticos no click-drop do fim
const diag = (painelRidge.match(/id="ridgeDiagFold"([\s\S]*?)<\/details>/) || [, ''])[1];
ok(diag.length > 200, 'existe um click-drop de diagnosticos', diag.length + ' chars');
ok(/<details class="fold" id="ridgeDiagFold">/.test(src),
   'e ele e mesmo um <details>, nao uma div com a mesma classe');
ok(/ridgeParamChart/.test(diag) && /ridgeR2Chart/.test(diag),
   'com os dois graficos (Rolling Coefficient e R2) dentro dele');
ok(painelRidge.indexOf('id="ridgeDiagFold"') > painelRidge.indexOf('ridgeDecompChart') &&
   painelRidge.indexOf('id="ridgeDiagFold"') > painelRidge.indexOf('ridgeForecastChart'),
   'e ele fica DEPOIS da decomposicao e da previsao, no fim da aba');
// um grafico desenhado dentro de um <details> fechado renderiza com largura zero
ok(src.indexOf("['ridgeMethodFold', 'ridgeDiagFold'].forEach") >= 0 &&
   src.indexOf("addEventListener('toggle'") >= 0 &&
   src.indexOf("Plotly.Plots.resize(gd)") >= 0,
   'e abrir o bloco redimensiona os graficos que estavam escondidos');

// (v) tendencia = baseline + PPP, uma barra so
ok(/const TREND_EXTRA_RG = 'delta_ppp';/.test(src), 'o PPP entra no balde de tendencia');
ok(/const DECOMP_BARS_RG = DECOMP_CHANNELS_RG\.filter\(k => k !== TREND_EXTRA_RG\);/.test(src),
   'e sai da lista de barras da decomposicao');
ok(/const levelOrderRg = \['"]baseline\['"], \.\.\.DECOMP_BARS_RG/.test(src.replace(/'/g, '"')) ||
   /levelOrderRg = \['baseline', \.\.\.DECOMP_BARS_RG/.test(src),
   'a ordem das barras usa DECOMP_BARS_RG, nao DECOMP_CHANNELS_RG');
ok(/baseline: 'Trend'/.test(src), 'o balde se chama "Trend" na legenda');
ok(/somaArrRg\(currentArr\('baseline'\), currentArr\(TREND_EXTRA_RG\)\)/.test(src),
   'e o valor plotado e a SOMA das duas series');
ok(/id="ridgeDecompFoot"/.test(src), 'o grafico tem rodape');
ok(/<b>Trend<\/b> is drawn as one bar/.test(src) &&
   /inflation gap/.test(src) && /constant drift/.test(src) && /momentum term/.test(src),
   'e o rodape diz de que a barra e composta');
ok(/compound rather than add/.test(src),
   'avisando que as partes compoem, nao somam -- sao percentuais');
// O SENTIDO de alpha tem de sair do sinal. A frase dizia "real depreciation"
// fixo e ficou errada em 2026-09-08, quando a reestimacao sobre o CDS da
// Bloomberg virou alpha para -0,107 pp/mes: o numero ao lado ja saia com o
// sinal certo, entao nada na tela se contradizia -- a prosa so passou a afirmar
// o contrario do numero que ela mesma imprime. Sem guarda isso volta na proxima
// reestimacao que mude o lado.
ok(/alphaTot >= 0[\s\S]{0,160}real depreciation[\s\S]{0,160}real appreciation/.test(src),
   'e o sentido de alpha e derivado do SINAL, nunca escrito fixo');
ok(!/The second is real depreciation/.test(src),
   'a frase fixa de depreciacao nao voltou');
// a grade de previsao CONTINUA editando o PPP: a fusao e so do grafico
ok(/DECOMP_CHANNELS_RG\.forEach\(key => \{ deltasByChannel\[key\] = channelDeltas/.test(src),
   'a simulacao segue percorrendo DECOMP_CHANNELS_RG (com o PPP dentro)');

// (iv) o input do PPP e inflacao em % a/a
ok(/const YOY_INPUT_RG = \['"]delta_ppp\['"]\]/.test(src.replace(/'/g, '"')) ||
   /const YOY_INPUT_RG = \['delta_ppp'\]/.test(src),
   'o PPP esta declarado como input em % a/a');
ok(/boxMode\[key\] = YOY_INPUT_RG\.includes\(key\) \? 'yoy' : 'level'/.test(src),
   'e a caixa dele nasce nesse modo');
ok(/if \(boxMode\[key\] === 'yoy'\) return levels\[key\]\.map\(\(v, h\) => levelToYoyRg/.test(src),
   'a exibicao converte nivel -> % a/a');
ok(/if \(boxMode\[key\] === 'yoy'\) return yoyToLevelRg\(key, h, displayVal\);/.test(src),
   'e a entrada converte de volta');
ok(/Enter the 12-month inflation gap you expect/.test(src),
   'o cartao diz ao leitor o que digitar');
ok(/Now running at \$\{fmtSignedRg\(levelToYoyRg/.test(src),
   'e "Last observed" mostra a inflacao acumulada, nao o indice');
ok(/value="\$\{Math\.round\(dispVals\[h\] \* 100\) \/ 100\}"/.test(src),
   'as caixas imprimem a unidade de exibicao arredondada, nao o float do indice');

// a conversao tem de fechar contra o proprio payload
const vv = hist.values;
const ref = vv[vv.length - 12];        // referencia da caixa h=0
const yoyAtual = 100 * Math.log(vv[vv.length - 1] / ref);
ok(yoyAtual > -2 && yoyAtual < 15,
   'a inflacao acumulada de 12m implicita no indice e plausivel',
   yoyAtual.toFixed(2) + '%');
// ida e volta exata: nivel -> y/y -> nivel
const nivel = vv[vv.length - 1] * 1.0123;
const volta = ref * Math.exp((100 * Math.log(nivel / ref)) / 100);
ok(Math.abs(volta - nivel) < 1e-9, 'a conversao ida-e-volta e exata',
   Math.abs(volta - nivel).toExponential(2));

// ---------------------------------------------------------------------------
// 14. historico COMPLETO dos regressores (2026-09-08, pedido do usuario)
// ---------------------------------------------------------------------------
// 14. o grafico de cada regressor mostra a HISTORIA INTEIRA (2026-09-08)
// ---------------------------------------------------------------------------
// O `channel_history` saia reindexado em `z.index`, entao o grafico de um canal
// abria na amostra do ajuste: o CDS comeca em 2001-10 e o painel dele comecava
// em 2006-02, sem o pico de 2002 (3790 bps) -- a maior ordem de grandeza que a
// serie tem, e o proposito declarado destes graficos.
//
// A correcao anterior tinha construido uma SEGUNDA secao no fim da aba, o que o
// usuario recusou ("cada regressor tem uma sessao de grafico, por que voce criou
// outra sessao la em baixo?"). Entao o historico foi para dentro do grafico que
// ja existe, e a secao extra saiu.
//
// Quatro coisas quebram em silencio aqui:
//   * estender a serie pelo FIM: os meses depois do corte ja sao desenhados
//     pela linha do nowcast, e a caixa de previsao se ancora em `values[len-1]`
//     -- as duas linhas passariam a repetir os mesmos meses e a ancora mudaria;
//   * o alinhamento da CAUDA com `D.months`: e dele que saem `values[len-1]` e
//     o `values[len-12+h]` da leitura em % a/a do PPP, em todo o template;
//   * `log` escrito a mao em vez de derivado da amplitude medida;
//   * log ligado fora do nivel cru: z-score e variacao a/a tem valores
//     negativos, e log de negativo some do grafico sem levantar nada.
sec('14. o grafico de cada regressor mostra a historia inteira');
const CH = D.forecast.channel_history;
ok(!!CH, 'o payload traz channel_history');
const chaves = Object.keys(CH);
ok(chaves.length === 6, 'os 5 canais mais o PPP', chaves.join(', '));
['fiscal', 'dxy_em', 'carry_vol', 'sp500', 'icbr_usd', 'ppp'].forEach(c =>
  ok(chaves.indexOf(c) >= 0, 'o canal ' + c + ' esta no historico'));

ok(!('channel_history_full' in D),
   'e o bloco duplicado do payload saiu junto com a secao extra');

// A cauda: e o que todo o resto do template le, e o que a extensao para tras
// nao pode ter movido.
chaves.forEach(c => {
  const h = CH[c];
  ok(h.months.length === h.values.length, c + ': meses e valores alinhados',
     h.months.length + ' vs ' + h.values.length);
  ok(h.end === D.sample_range[1],
     c + ': a serie termina no corte do ajuste, nao depois dele',
     h.end + ' vs ' + D.sample_range[1]);
  const off = h.months.indexOf(D.months[0]);
  ok(off >= 0, c + ': a grade do ajuste comeca dentro da serie', String(off));
  ok(off >= 0 && h.months.slice(off).join(',') === D.months.join(','),
     c + ': e a CAUDA e exatamente a amostra do ajuste, mes a mes');
  // Nenhum canal pode carregar mes ALEM do corte -- ali quem desenha e o
  // nowcast, e duas linhas repetiriam os mesmos pontos.
  const nc = D.forecast.nowcast.channels[c];
  if (nc && nc.months.length) {
    ok(nc.months[0] > h.end,
       c + ': o nowcast comeca depois do fim do historico, sem sobreposicao',
       nc.months[0] + ' > ' + h.end);
  }
});

// O ganho: pelo menos um canal comeca ANTES do ajuste. Sem isto a mudanca nao
// acrescentou nada, e e esse o estado em que ela deveria ser revertida.
const antes = chaves.filter(c => CH[c].start < D.sample_range[0]);
ok(antes.length >= 1, 'ao menos um canal comeca antes da amostra do ajuste',
   antes.join(', '));
ok(CH.fiscal.months.length > D.months.length,
   'o CDS tem mais meses que o ajuste -- e o caso que motivou a correcao',
   CH.fiscal.months.length + ' contra ' + D.months.length);
ok(CH.fiscal.start <= '2001-12',
   'e ele carrega o historico de 2001 que a fonte nova trouxe', CH.fiscal.start);
ok(CH.fiscal.values[0] > 500,
   'com o NIVEL de 2001 no primeiro ponto, nao um resto de grade',
   String(CH.fiscal.values[0]));
ok(CH.fiscal.max > 5 * CH.fiscal.values[CH.fiscal.values.length - 1],
   'o pico historico e ordens de grandeza acima do nivel de hoje -- que e o que'
   + ' o grafico existe para mostrar',
   CH.fiscal.max + ' contra ' + CH.fiscal.values[CH.fiscal.values.length - 1]);

// Campos de escala, todos derivados.
const canaisSemPpp = chaves.filter(c => c !== 'ppp');
chaves.forEach(c => {
  const h = CH[c];
  ok(!!h.unit, c + ': declara a unidade nativa, para o eixo poder cita-la');
  const vivos = h.values.filter(v => v !== null);
  ok(vivos.length === h.n, c + ': n bate com os valores nao nulos',
     vivos.length + ' vs ' + h.n);
  ok(perto(h.min, Math.min.apply(null, vivos), 1e-3)
     && perto(h.max, Math.max.apply(null, vivos), 1e-3),
     c + ': min/max declarados batem com a serie');
  ok(h.span === null || perto(h.span, Math.round(100 * h.max / h.min) / 100, 1e-2),
     c + ': span e max/min, medido', String(h.span));
  // `log` DERIVADO da amplitude. Um mutante que ligue log num canal de 1,6x so
  // e pego por isto.
  ok(h.log === (h.span !== null && h.span >= 8),
     c + ': log e derivado de span >= 8', 'span ' + h.span + ' log ' + h.log);
  if (h.log) ok(h.min > 0, c + ': so entra em log porque e estritamente positivo');
  // level_mean/level_std tem de ser da serie DESENHADA, nao da janela do
  // ajuste: padronizar o que se ve por uma media que exclui os anos extremos e
  // o defeito que a versao anterior tinha (o CDS de 2002 a 46 desvios).
  const media = vivos.reduce((s, v) => s + v, 0) / vivos.length;
  ok(perto(h.level_mean, media, Math.max(1e-3, Math.abs(media) * 1e-4)),
     c + ': level_mean e a media da serie inteira', h.level_mean + ' vs ' + media);
});
const mediaAjuste = (function () {
  const off = CH.fiscal.months.indexOf(D.months[0]);
  const v = CH.fiscal.values.slice(off);
  return v.reduce((s, x) => s + x, 0) / v.length;
})();
ok(Math.abs(CH.fiscal.level_mean - mediaAjuste) > 1,
   'e no CDS ela e mesmo diferente da media da janela do ajuste',
   CH.fiscal.level_mean + ' vs ' + mediaAjuste.toFixed(2));

// A escolha de escala tem de ser MISTA, senao a regra nao esta separando nada.
const nLog = chaves.filter(c => CH[c].log).length;
ok(nLog >= 1 && nLog < chaves.length,
   'a regra de log separa de fato: alguns canais em log, outros em linear',
   nLog + ' de ' + chaves.length);

// O canal que amarra o inicio da amostra, derivado dos proprios `start`.
const maisTarde = canaisSemPpp.reduce((a, b) => CH[a].start > CH[b].start ? a : b);
function mesesEntre(a, b) {
  const [ay, am] = a.split('-').map(Number), [by, bm] = b.split('-').map(Number);
  return (by - ay) * 12 + (bm - am);
}
// O ajuste roda na INTERSECCAO, entao o canal de comeco mais tarde manda em
// tudo. Nao e igualdade exata: a regressao e em DIFERENCAS, e a primeira
// observacao de cada serie e consumida pela propria diferenca -- hoje sao
// exatamente esses 1 mes. Mais que isso significa que quem amarra a amostra
// deixou de ser um canal, e e isso que esta assercao existe para pegar.
const folga = mesesEntre(CH[maisTarde].start, D.sample_range[0]);
ok(folga >= 0 && folga <= 2,
   'a amostra do ajuste comeca onde o canal de comeco mais tarde comeca, a menos'
   + ' do mes que a diferenciacao consome',
   maisTarde + ' ' + CH[maisTarde].start + ' -> ' + D.sample_range[0]
   + ' (' + folga + ' mes/meses)');
canaisSemPpp.forEach(c => ok(CH[c].start <= CH[maisTarde].start,
  c + ': nao comeca depois do canal que amarra a amostra'));

// ---- o lado do template ----
// Regex sobre o src, no padrao do resto deste arquivo -- o bloco de <script>
// das abas de modelo nao e executado por harness permanente (ver o CLAUDE.md da
// pasta), entao o que da para afirmar e a forma do codigo entregue.
ok(!/ridgeFullHistChart|renderFullHistChart|channel_history_full/.test(src),
   'a secao separada de historico completo saiu da pagina inteira');
ok(/id="regressor-graph-\$\{key\}"/.test(src),
   'o grafico continua sendo o de dentro do card de cada regressor');
ok(/id="graph-note-\$\{key\}"/.test(src), 'com uma ficha de escala propria');
ok(src.indexOf('id="regressor-graph-${key}"') < src.indexOf('id="graph-note-${key}"'),
   'e a ficha vem DEPOIS do grafico no DOM (regra de 2026-08-27)');
ok(/connectgaps: false/.test(src),
   'connectgaps false -- buraco interno da fonte nao vira reta');
ok(/const usaLog = !!hist\.log && graphMode\[key\] === 'level' && !yoyChart/.test(src),
   'log so no nivel cru, e so quando o payload manda');
ok(/if \(usaLog\) layout\.yaxis\.type = 'log'/.test(src),
   'e e o eixo Y que vira log, nao os dados que sao transformados');
ok(/let yTitle = hist\.unit \? 'Level, ' \+ hist\.unit : 'Level'/.test(src),
   'o eixo Y cita a unidade que vem da serie, nao uma string fixa');
ok(/x1: fitIni/.test(src) && /const fitIni = D\.sample_range\[0\] \+ '-01'/.test(src),
   'a faixa sombreada termina no inicio do ajuste, derivado do payload');
ok(/text: 'before the fit sample'/.test(src),
   'e diz o que ela significa, em vez de ser um cinza sem legenda');
ok(/renderChannelGraphNote\(key, hist, usaLog, preAjuste >= 6\)/.test(src),
   'a ficha e reconstruida a cada render, junto com o grafico');
// A faixa so aparece quando ha o que mostrar, e a MESMA condicao governa o
// desenho e a frase que fala dele -- separadas, a ficha passa a descrever um
// cinza que nao esta na tela. O canal que amarra a amostra comeca um mes antes
// dela, entao sem piso ele ganharia um risco de 1 mes com rotulo por cima.
ok(/const preAjuste = hist\.months\.length \? mesesEntreRg\(hist\.months\[0\], D\.sample_range\[0\]\) : 0;/.test(src)
   && /if \(preAjuste >= 6\) \{/.test(src),
   'a faixa tem piso de 6 meses, medido do proprio inicio da serie');
ok(/function renderChannelGraphNote\(key, hist, usaLog, temFaixa\)/.test(src)
   && /if \(temFaixa\) \{/.test(src),
   'e a frase que a descreve depende da mesma condicao, nao de um teste proprio');
ok(/Math\.round\(hist\.span\)/.test(src) && !/fmtNumRg\(hist\.span/.test(src),
   'a amplitude e arredondada, nao truncada -- fmtNumRg faria 60,97 virar "60x"');
// binding channel derivado no cliente tambem -- nada escrito a mao.
ok(/const bindingChannelRg = \(function \(\)/.test(src)
   && /h\.start > FC\.channel_history\[melhor\]\.start/.test(src),
   'o canal que amarra a amostra e derivado no cliente, nunca escrito');
ok(!/bindingChannelRg = 'dxy_em'|bindingChannelRg = "dxy_em"/.test(src),
   'e nao ha nome de canal cravado nele');

// ---------------------------------------------------------------------------
// 15. a padronizacao ESCALA, nao centra (2026-09-08)
// ---------------------------------------------------------------------------
// O usuario achou o defeito pela leitura obvia do grafico: *"no comeco de 2006
// o CDS era ~120 pontos, atualmente esta proximo disso. Como o CDS pode ter
// contribuido com 48% da desvalorizacao do real no periodo?"*
//
// Nao podia. `_standardize_ext` subtraia a media da janela de referencia, e
// toda coluna que passa por ali e' uma DIFERENCA -- a media de uma diferenca e'
// uma deriva, entao subtrai-la injeta um sinal constante de -mu/sd em todo mes,
// inclusive nos meses em que o canal ficou parado. Com o CDS da Bloomberg a
// referencia comeca em 2001-10 a 1100 bps, mu = -3,28 bps/mes, e a deriva valia
// +52,5 pp dos +49,0 pp que a barra do canal mostrava.
//
// O ajuste nunca dependeu disso (o Ridge do sklearn nao penaliza o intercepto,
// entao a constante ia toda para o alpha), o que torna estas assercoes baratas
// de manter: elas afirmam a ATRIBUICAO, que e' o unico lugar onde a convencao
// aparece.
//
// Quatro regressoes silenciosas que isto pega:
//   * `mean` voltando a ser diferente de zero no payload -- o cliente le so o
//     `std`, entao servidor e navegador passariam a discordar sem sintoma
//     (media -0,185 pp/mes, -2,22 pp em 12 meses, quando foi medido);
//   * o simulador do cliente passando a subtrair o `mean`, o outro lado da
//     mesma moeda;
//   * a contribuicao acumulada de um canal deixando de ser o que o canal fez;
//   * centrar na propria amostra, que zera TODO canal por identidade
//     aritmetica e se le como achado.
sec('15. a padronizacao escala, nao centra');
const CS = D.forecast.channel_stats;
Object.keys(CS).forEach(k => {
  ok(CS[k].mean === 0, k + ': media do transforme e exatamente zero',
     String(CS[k].mean));
  ok(CS[k].std > 0, k + ': e a escala e positiva', String(CS[k].std));
});

// Servidor e cliente aplicam o MESMO transforme. O cliente faz `raw / std`; se
// o payload trouxer media, o vies e sum(beta*mu/sd) por mes -- exatamente a
// quantidade abaixo, que tem de ser zero.
const viesMes = Object.keys(CS)
  .filter(k => CS[k].std > 0 && D.forecast.beta[k] !== undefined)
  .reduce((s, k) => s + D.forecast.beta[k] * CS[k].mean / CS[k].std, 0);
ok(Math.abs(viesMes) < 1e-12,
   'o ajuste do servidor e a simulacao do navegador nao tem vies entre si',
   viesMes.toExponential(2) + ' pp/mes');
ok(/const z = stat\.std > 0 \? raw \/ stat\.std : raw;/.test(src),
   'e o simulador do cliente divide pelo std sem subtrair nada');
ok(!/stat\.mean|channel_stats\[[^\]]*\]\.mean/.test(src),
   'o cliente nunca le o campo mean -- se ler, os dois lados divergem de novo');

// A assercao central, e a unica que nao envelhece: a contribuicao acumulada de
// um canal e o MOVIMENTO DELE, nada mais. beta * (x_fim - x_inicio) / sd, com
// os niveis lidos do channel_history e o log-retorno onde e o caso.
// Sob a convencao antiga isto falhava no fiscal por 52 pp.
const LOGRET = ['sp500', 'icbr_usd'];
canais.map(c => 'delta_' + c).forEach(k => {
  const raw = k.replace(/^delta_/, '');
  const h = D.forecast.channel_history[raw];
  const off = h.months.indexOf(D.months[0]);
  // o primeiro delta da amostra e contra o mes ANTERIOR ao primeiro mes dela
  const x0 = h.values[off - 1], x1 = h.values[h.values.length - 1];
  const dx = LOGRET.indexOf(raw) >= 0 ? 100 * Math.log(x1 / x0) : x1 - x0;
  const esperado = D.whole_sample.beta[k] * dx / CS[k].std;
  const obtido = D.contrib_monthly[k].reduce((s, v) => s + v, 0);
  ok(perto(esperado, obtido, 0.05),
     raw + ': a barra acumulada e o movimento do proprio canal',
     'esperado ' + esperado.toFixed(2) + ', payload ' + obtido.toFixed(2));
});

// E a leitura que motivou tudo: um canal que termina perto de onde comecou nao
// pode carregar uma fatia grande do movimento acumulado.
const hF = D.forecast.channel_history.fiscal;
const offF = hF.months.indexOf(D.months[0]);
const cdsIni = hF.values[offF - 1], cdsFim = hF.values[hF.values.length - 1];
const totalMov = D.fit_delta.actual.reduce((s, v) => s + v, 0);
ok(Math.abs(cdsFim / cdsIni - 1) < 0.5,
   'o CDS termina a amostra na mesma ordem de grandeza em que comecou',
   cdsIni.toFixed(1) + ' -> ' + cdsFim.toFixed(1) + ' bps');
ok(Math.abs(D.contrib_monthly.delta_fiscal.reduce((s, v) => s + v, 0)) < 0.15 * Math.abs(totalMov),
   'entao a barra dele nao pode carregar uma fatia grande do movimento acumulado',
   D.contrib_monthly.delta_fiscal.reduce((s, v) => s + v, 0).toFixed(2)
   + ' pp de ' + totalMov.toFixed(2));

// O lado do servidor: a funcao que faz o transforme nao pode voltar a centrar.
const PY = fs.readFileSync(
  path.join(__dirname, '..', 'analytics', 'brasil', 'exchange_rate', 'models',
            'ridge_deviation_model.py'), 'utf8');
const corpo = PY.slice(PY.indexOf('def _standardize_ext('), PY.indexOf('# Started as ["fiscal"'));
ok(corpo.length > 500, 'o corpo de _standardize_ext foi encontrado', String(corpo.length));
ok(/z\[c\] = sample\[c\] \/ sd/.test(corpo),
   '_standardize_ext divide pelo desvio-padrao da referencia');
ok(/stats\[c\] = \(0\.0, sd\)/.test(corpo),
   'e publica media zero, que e o que o cliente assume');
ok(!/\(sample\[c\] - mu\)|ref_col\.mean\(\)/.test(corpo),
   'e nao subtrai media nenhuma');
// A prosa da aba tem de explicar isso ao leitor, senao o grafico de
// decomposicao afirma algo cuja convencao nao esta em lugar nenhum.
ok(/Nothing is subtracted before the division/.test(src),
   'e a metodologia da aba diz ao leitor que nada e subtraido');

console.log('\n' + oks + ' ok, ' + falhas + ' falhou');
process.exit(falhas ? 1 : 0);
