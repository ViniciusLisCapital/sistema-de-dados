/*
 * Confere a secao "Base scenarios for the exogenous channels" no arquivo
 * entregue -- reports/brasil/FX Report.html, aba FX Model, o click-drop que
 * fica acima de "Fit diagnostics".
 *
 * Por que existe: a secao afirma NUMEROS EM PROSA ("uma crise multiplica por
 * 2,7x-3,3x", "o spread caiu entre os dois turnos em todas as eleicoes") e
 * oferece um botao que reescreve as 12 caixas de previsao. Cada uma dessas
 * coisas quebra em silencio:
 *
 *  1. A manchete e DERIVADA dos episodios. Se um episodio entrar com base
 *     errada, a frase continua sendo montada, com um numero novo, e ninguem
 *     tem contra o que conferir. As assercoes daqui refazem a conta.
 *  2. O caminho aplicado e MULTIPLICATIVO por medicao, nao por convencao. Um
 *     mutante que troque para aditivo produz numeros parecidos hoje -- o nivel
 *     de hoje (123) esta perto das bases historicas (105-174) -- e muito
 *     diferentes no dia em que o CDS estiver em 300.
 *  3. Um episodio EM ANDAMENTO tem cauda nula (a eleicao de 2026 ainda nao
 *     aconteceu). Aplicado sem tratamento, as caixas finais voltariam ao nivel
 *     de hoje e desenhariam um degrau que nunca existiu.
 *  4. `_last_at()` devolve a ultima cotacao ANTES de uma data. Para uma
 *     eleicao futura isso e a cotacao de hoje, que apareceria na tabela como
 *     "o nivel no dia do primeiro turno". Nao levanta nada.
 *  5. A prosa e o unico conteudo da secao que nenhuma outra assercao olha, e
 *     este repositorio ja escreveu texto de dashboard no vocabulario de quem
 *     construiu o mecanismo (ver .claude/rules/lis-dashboards.md). Ha uma
 *     lista de termos proibidos no fim.
 *
 * O harness EXECUTA o codigo da secao, fatiado do proprio arquivo entregue,
 * contra um stub de DOM/Plotly -- nao so confere sintaxe. E o que pega chave
 * errada de payload, id orfao e botao que nao escreve nada.
 *
 * Uso:  node tests/test_exog_scenarios_js.js [caminho/para/FX Report.html]
 */

const fs = require('fs');
const path = require('path');
const { worstPair } = require('./_deltae');

const HTML = process.argv[2] || path.join(__dirname, '..', 'reports', 'brasil', 'FX Report.html');

let falhas = 0, oks = 0;
function ok(cond, msg, extra) {
  if (cond) { oks++; console.log('  ok      ' + msg); }
  else { falhas++; console.log('  FALHOU  ' + msg + (extra ? '  -> ' + extra : '')); }
}
function sec(t) { console.log('\n' + t); }
function perto(a, b, tol) { return Math.abs(a - b) <= tol; }
// A pagina imprime o valor arredondado; o teste tem de procurar a mesma
// string, nao o float do payload.
function scenNum(v) { return Number(v).toFixed(0); }

const src = fs.readFileSync(HTML, 'utf8');

// ---------------------------------------------------------------------------
// payload
// ---------------------------------------------------------------------------
const m = src.match(/^const RIDGE_DATA = (\{.*\});$/m);
if (!m) { console.log('FALHOU: RIDGE_DATA nao encontrado (build com include_models=False?)'); process.exit(1); }
const D = JSON.parse(m[1]);
const SCEN = D.exog_scenarios;

sec('1. o payload existe e cobre os cinco canais do modelo');
ok(!!SCEN, 'RIDGE_DATA.exog_scenarios presente');
if (!SCEN) { console.log('\nsem payload, abortando'); process.exit(1); }
ok(SCEN.horizon === 12, 'horizonte 12, igual ao da grade de caixas', String(SCEN.horizon));
ok(SCEN.horizon === D.forecast.horizon,
   'e igual ao horizonte que o simulador de fato roda -- se divergirem, o caminho aplicado nao cobre as caixas');
const modelChannels = Object.keys(D.forecast.beta)
  .filter(k => k !== 'delta_ppp' && k !== 'delta_fx_lag1')
  .map(k => k.replace(/^delta_/, ''))
  .sort();
const scenChannels = (SCEN.order || []).slice().sort();
ok(JSON.stringify(modelChannels) === JSON.stringify(scenChannels),
   'a lista de canais bate EXATAMENTE com os regressores estimados do modelo',
   'modelo=' + modelChannels + ' cenarios=' + scenChannels);
// Um canal sem cenario tem de aparecer como pendente, nao desaparecer: a
// ausencia leria como "este canal nao tem cenario", que e outra afirmacao.
SCEN.order.forEach(k => {
  const ch = SCEN.channels[k];
  ok(!!ch, 'canal ' + k + ' presente no mapa');
  if (!ch) return;
  const measured = !ch.pending && ch.episodes && ch.episodes.length;
  ok(measured || ch.pending === true,
     'canal ' + k + ' e medido ou declarado pendente (nunca vazio em silencio)');
});
const fiscal = SCEN.channels.fiscal;
ok(fiscal && !fiscal.pending && fiscal.episodes.length > 0,
   'o canal fiscal (CDS) esta medido -- e o pedido desta rodada');

// ---------------------------------------------------------------------------
// 2. identidades de medicao, por episodio
// ---------------------------------------------------------------------------
sec('2. cada episodio fecha nas proprias contas');
const EP = fiscal.episodes;
ok(EP.length === 10, '10 episodios: 3 crises + 7 anos de eleicao', String(EP.length));

EP.forEach(ep => {
  const tag = ep.id;
  ok(ep.path.length === 13 && ep.levels.length === 13,
     tag + ': 13 pontos (mes 0 = base, mais 12)');
  ok(ep.path[0] === 1, tag + ': path[0] e exatamente 1', String(ep.path[0]));
  ok(perto(ep.levels[0], ep.base, 0.005), tag + ': levels[0] e a base');

  // path = levels / base, ponto a ponto -- e o que faz o caminho aplicavel.
  let razaoOk = true;
  for (let i = 0; i < 13; i++) {
    if (ep.path[i] === null) { razaoOk = razaoOk && ep.levels[i] === null; continue; }
    if (!perto(ep.path[i], ep.levels[i] / ep.base, 0.0002)) razaoOk = false;
  }
  ok(razaoOk, tag + ': cada razao e o nivel dividido pela base (e nulo casa com nulo)');

  // Cauda nula, nunca buraco interior: um nulo no meio faria o caminho
  // aplicado saltar para tras sem sintoma.
  const primNulo = ep.path.indexOf(null);
  ok(primNulo === -1 || ep.path.slice(primNulo).every(v => v === null),
     tag + ': se ha nulo, ele e cauda -- nao ha buraco no meio');

  const naoNulos = ep.levels.filter(v => v !== null);
  ok(perto(ep.peak, Math.max.apply(null, naoNulos), 0.005),
     tag + ': peak e o MAIOR fechamento mensal da janela', ep.peak + ' vs ' + Math.max.apply(null, naoNulos));
  ok(perto(ep.peak_x, ep.peak / ep.base, 0.002),
     tag + ': peak_x = peak / base', ep.peak_x + ' vs ' + (ep.peak / ep.base));
  ok(ep.peak_x >= 1, tag + ': peak_x nunca menor que 1 (a base esta na janela)');

  const [by, bm] = ep.base_month.split('-').map(Number);
  const [py, pm] = ep.peak_month.split('-').map(Number);
  ok(ep.months_to_peak === (py - by) * 12 + (pm - bm),
     tag + ': months_to_peak bate com as duas datas');
  ok(ep.months_to_peak >= 0 && ep.months_to_peak <= 12,
     tag + ': o pico cai dentro da janela de 12 meses');
  ok(ep.complete === (ep.months_observed === 12),
     tag + ': `complete` e exatamente "12 meses observados"');

  // O pico e do fechamento MENSAL; o spike diario e outra coisa e nunca pode
  // ser menor. Confundir os dois e o erro que prometeria as caixas um nivel
  // que uma serie mensal nao consegue representar.
  if (ep.spike) {
    ok(ep.spike.value >= ep.peak - 0.005,
       tag + ': o spike diario e >= o pico mensal (sao grandezas diferentes)',
       ep.spike.value + ' vs ' + ep.peak);
  }
  // A leitura "foi o Brasil ou o mundo" tem de cobrir a SUBIDA, nao a ida e
  // volta: medida ate o fim da janela, a COVID sai com o dolar em -0,3%.
  if (ep.concurrent) {
    ok(ep.concurrent_window === ep.base_month + ' to ' + ep.peak_month,
       tag + ': a janela do comparativo vai da base ao PICO', ep.concurrent_window);
  }
});

// ---------------------------------------------------------------------------
// 3. a manchete de ordem de magnitude
// ---------------------------------------------------------------------------
sec('3. crise e eleicao sao ordens de magnitude distintas');
const crises = EP.filter(e => e.kind === 'crisis');
const eleicoes = EP.filter(e => e.kind === 'election');
ok(crises.length === 3, '3 crises (2008, 2015-16, 2020)', String(crises.length));
ok(eleicoes.length === 7, '7 anos de eleicao (2002-2026)', String(eleicoes.length));

// A afirmacao central INVERTEU em 2026-09-08, quando a serie de CDS trocou de
// fonte e ganhou 2001-2007. Ate entao a maior corrida eleitoral (2018, 1,76x)
// era menor que a mais branda das crises, e o teste afirmava isso. Com 2002 na
// amostra a maior eleicao supera as tres crises, e a leitura util deixou de ser
// uma faixa por tipo de episodio: as eleicoes sao BIMODAIS. Seis ficam num
// regime brando e uma, a de 2002, esta sozinha no topo da biblioteca inteira.
// Afirmar as duas metades separadamente e o que impede a secao de voltar a
// dizer "eleicao e o evento menor" -- que era verdade e nao e mais.
const eleicoesCompletas = eleicoes.filter(e => e.complete);
const piorEleicao = Math.max.apply(null, eleicoesCompletas.map(e => e.peak_x));
const menorCrise = Math.min.apply(null, crises.map(e => e.peak_x));
const maiorCrise = Math.max.apply(null, crises.map(e => e.peak_x));
ok(piorEleicao > maiorCrise,
   'a MAIOR corrida eleitoral supera as TRES crises -- e a afirmacao central da secao',
   'eleicao ' + piorEleicao.toFixed(2) + 'x vs crise ' + maiorCrise.toFixed(2) + 'x');
ok(eleicoes.some(e => e.id === 'election_2002' && e.peak_x === piorEleicao),
   'e a eleicao que faz isso e a de 2002, nao outra');
const brandas = eleicoesCompletas.filter(e => e.peak_x < 2).map(e => e.peak_x);
ok(brandas.length === eleicoesCompletas.length - 1,
   'as OUTRAS eleicoes completas ficam todas abaixo de 2x -- a distribuicao e bimodal',
   brandas.length + ' de ' + eleicoesCompletas.length);
ok(Math.max.apply(null, brandas) <= 1.8,
   'e o teto desse grupo brando segue em ~1,8x', Math.max.apply(null, brandas).toFixed(2));
ok(menorCrise >= 2.5 && maiorCrise <= 3.2,
   'as tres crises ficam na faixa de ~2,7x a ~3,1x que a manchete anuncia',
   crises.map(e => e.peak_x.toFixed(2)).join(' / '));
// O que separa as crises e velocidade, nao tamanho: 3, 6 e 12 meses ate o pico
// com multiplos quase iguais. Se essa relacao inverter, a prosa fica errada.
const mesesCrise = crises.map(e => e.months_to_peak).sort((a, b) => a - b);
ok(mesesCrise[0] <= 3 && mesesCrise[2] >= 12,
   'e as tres diferem em VELOCIDADE, de ~3 a 12 meses ate o pico', mesesCrise.join('/'));

// ---------------------------------------------------------------------------
// 4. primeiro turno vs segundo turno
// ---------------------------------------------------------------------------
sec('4. os dois turnos compartilham a janela mensal, e a diferenca e diaria');
eleicoes.forEach(ep => {
  const [ey, em] = ep.event_month.split('-').map(Number);
  const [by, bm] = ep.base_month.split('-').map(Number);
  ok((ey - by) * 12 + (em - bm) === 12,
     ep.id + ': a base e exatamente 12 meses antes do mes da eleicao');
  // A razao de existir UMA linha por eleicao em vez de duas: os dois turnos
  // caem no mesmo mes, logo T-12 -> 1o turno e T-12 -> 2o turno sao a mesma
  // janela mensal. Se um pais mudar o calendario, esta assercao avisa.
  ok(ep.round1.slice(0, 7) === ep.event_month && ep.round2.slice(0, 7) === ep.event_month,
     ep.id + ': os dois turnos caem no MESMO mes (e o que torna as janelas identicas)',
     ep.round1 + ' / ' + ep.round2);
});

const completas = eleicoes.filter(e => e.inter_round && e.inter_round.at_r2 !== null);
// 6 desde 2026-09-08 (eram 4). 2002 e 2006 entraram com a troca de fonte do
// CDS, e sao o primeiro teste FORA da amostra em que a queda entre turnos foi
// encontrada: as duas cairam tambem, o que e' o que o loop abaixo afirma uma a
// uma. Se uma eleicao futura subir entre os turnos, e aqui que se descobre.
ok(completas.length === 6, '6 eleicoes com os dois turnos ja realizados', String(completas.length));
completas.forEach(ep => {
  const ir = ep.inter_round;
  ok(ir.bps < 0 && ir.pct < 0,
     ep.id + ': o CDS CAIU entre os dois turnos -- a frase da secao afirma isso',
     ir.bps + ' bps / ' + ir.pct + '%');
  ok(Math.sign(ir.bps) === Math.sign(ir.pct),
     ep.id + ': bps e % tem o mesmo sinal');
  ok(perto(ir.bps, ir.at_r2 - ir.at_r1, 0.15),
     ep.id + ': bps = nivel no 2o turno menos nivel no 1o');
});
// O que vem DEPOIS da eleicao nao repete, e a prosa diz isso -- se algum dia
// os quatro concordarem, a frase passa a ser mais fraca do que o dado permite.
const posSinais = eleicoes.filter(e => e.post).map(e => Math.sign(e.post.bps));
ok(new Set(posSinais).size > 1,
   'os 3 meses seguintes ao 2o turno NAO tem sinal consistente (a secao afirma isso)',
   posSinais.join(','));

// A eleicao futura nao pode ter leitura "no dia do turno": seria a cotacao de
// hoje carimbada com a data da eleicao.
const emCurso = eleicoes.filter(e => !e.complete);
ok(emCurso.length >= 1, 'ha ao menos uma eleicao em andamento (a do ano corrente)');
emCurso.forEach(ep => {
  ok(!ep.inter_round || ep.inter_round.at_r2 === null,
     ep.id + ': sem nivel de 2o turno enquanto o 2o turno nao aconteceu');
  ok(!ep.post, ep.id + ': sem leitura pos-eleicao enquanto nao ha eleicao');
  ok(!!ep.note && /progress/i.test(ep.note), ep.id + ': a linha se anuncia como em andamento');
});

// ---------------------------------------------------------------------------
// 5. distribuicao de referencia
// ---------------------------------------------------------------------------
sec('5. a distribuicao de referencia e monotona e proporcional');
const dist = fiscal.distribution;
ok(!!dist, 'distribuicao presente');
['1m', '3m', '6m', '12m'].forEach(k => {
  const r = dist[k];
  ok(!!r, k + ': presente');
  if (!r) return;
  ok(r.p5 < r.p50 && r.p50 < r.p90 && r.p90 <= r.p95 && r.p95 <= r.p99 && r.p99 <= r.max,
     k + ': percentis em ordem', JSON.stringify(r));
  ok(r.n > 100, k + ': amostra de mais de 100 janelas', String(r.n));
});
// Horizonte maior, cauda maior -- se o 12m for mais estreito que o 1m, a
// tabela deixa de servir para localizar um caminho digitado.
ok(dist['12m'].sd > dist['1m'].sd, 'o desvio cresce com o horizonte');
// A prosa afirma que a distribuicao e "quase simetrica", o que e o contrapeso
// de uma tabela cujos episodios sao todos de abertura.
ok(Math.abs(dist['12m'].p5) > 40 && dist['12m'].p90 > 40,
   'as duas caudas de 12 meses sao da mesma ordem (a secao chama de quase simetrica)',
   dist['12m'].p5 + ' / ' + dist['12m'].p90);

// ---------------------------------------------------------------------------
// 6. o click-drop fica ACIMA de Fit diagnostics, e dentro da aba FX Model
// ---------------------------------------------------------------------------
sec('6. lugar na pagina');
const iScen = src.indexOf('id="ridgeScenFold"');
const iDiag = src.indexOf('id="ridgeDiagFold"');
const iFc = src.indexOf('id="ridgeForecastShocks"');
ok(iScen > 0, 'o fold de cenarios existe');
ok(iDiag > 0, 'o fold de diagnosticos existe');
ok(iScen < iDiag, 'cenarios vem ANTES de Fit diagnostics -- foi o pedido explicito',
   'scen@' + iScen + ' diag@' + iDiag);
ok(iFc > 0 && iFc < iScen,
   'e DEPOIS da grade de caixas que ele alimenta (a ordem de leitura: digite, depois compare)');
// Pertencimento: o painel, nao o titulo. Ver a licao do §14 de
// tests/test_fx_report_js.js -- um bloco no painel errado passa todo teste que
// nao fatie pelos limites do painel.
const iPanel = src.indexOf('<div class="tab-panel ppp-scope" id="tab-ridge">');
const iPanelEnd = src.indexOf('<!-- /tab-ridge -->', iPanel);
ok(iPanel > 0 && iScen > iPanel && iScen < iPanelEnd,
   'o fold mora dentro do painel tab-ridge, nao numa aba vizinha');
ok(src.indexOf('id="scenChannels"') > iScen && src.indexOf('id="scenChannels"') < iDiag,
   'o host #scenChannels esta dentro do corpo do fold de cenarios');

// ---------------------------------------------------------------------------
// 7. EXECUCAO -- o codigo da secao, fatiado do arquivo entregue
// ---------------------------------------------------------------------------
sec('7. o codigo da secao roda e produz o que a pagina mostra');

const CORTE_INI = '    // ---- Base scenarios for the exogenous channels';
const CORTE_FIM = '    })();';
const ini = src.indexOf(CORTE_INI);
const fim = src.indexOf(CORTE_FIM, ini);
ok(ini > 0 && fim > ini, 'a secao foi localizada no arquivo para ser executada');
const codigo = src.slice(ini, fim + CORTE_FIM.length);

// --- stub de DOM: pequeno de proposito. Ele precisa de exatamente tres coisas
// --- reais -- getElementById, um querySelectorAll que enxergue os botoes que
// --- a secao acabou de escrever em innerHTML, e addEventListener -- porque e
// --- justamente o par "escrevi HTML / religo os handlers nele" que quebra em
// --- silencio quando um data-attribute e renomeado.
const registro = {};
function mkEl(id) {
  const e = {
    id: id || '', innerHTML: '', textContent: '', dataset: {},
    classList: { _s: new Set(), add(c) { this._s.add(c); }, remove(c) { this._s.delete(c); },
                 contains(c) { return this._s.has(c); }, toggle(c, on) { on ? this.add(c) : this.remove(c); } },
    _handlers: {},
    addEventListener(ev, fn) { (this._handlers[ev] = this._handlers[ev] || []).push(fn); },
    dispatch(ev) { (this._handlers[ev] || []).forEach(fn => fn.call(this, {})); },
    scrollIntoView() { this._scrolled = true; },
    // O _bindPlotlyYAutofit REAL (embutido abaixo) chama el.on(...) -- sem isto
    // o caminho de layout real nao roda e o teste volta a medir um stub.
    on(ev, fn) { (this._handlers[ev] = this._handlers[ev] || []).push(fn); },
    // Cache por seletor enquanto o innerHTML nao muda: num DOM real duas
    // consultas devolvem os MESMOS nos, e e disso que depende despachar um
    // clique num no consultado depois do render e cair no handler que o render
    // ligou. Sem o cache o stub deixa de exercitar o par "escrevi HTML /
    // religo os handlers nele", que e a razao de ele existir.
    querySelectorAll(sel) {
      this._qsa = this._qsa || {};
      const hit = this._qsa[sel];
      if (hit && hit._html === this.innerHTML) return hit;
      const out = parseFromHtml(this.innerHTML, sel);
      out._html = this.innerHTML;
      this._qsa[sel] = out;
      return out;
    },
  };
  if (id) registro[id] = e;
  return e;
}
// Le os elementos que a secao acabou de escrever. Nao e um parser de HTML: e o
// minimo para que os handlers religados apontem para os MESMOS data-attributes
// que o markup gerou -- que e o unico modo de falha que este trecho tem.
function parseFromHtml(html, sel) {
  const out = [];
  if (sel === '.scen-kind-pill') {
    // Os data-attributes do markup gerado, lidos de volta: e o par
    // "escrevi HTML / religo os handlers nele" que quebra em silencio quando
    // um atributo e renomeado, e desde 2026-09-09 e esta pill que troca a
    // vista do grafico.
    const re = /<span class="scen-kind-pill([^"]*)" data-scen-ch="([^"]+)" data-scen-kind="([^"]+)"/g;
    let mm;
    while ((mm = re.exec(html))) {
      const e = mkEl('');
      (mm[1] || '').trim().split(/\s+/).filter(Boolean).forEach(c => e.classList.add(c));
      e.dataset.scenCh = mm[2];
      e.dataset.scenKind = mm[3];
      out.push(e);
    }
  } else if (sel === 'details.scen-ch') {
    const re = /<details class="scen-ch" id="([^"]+)"( open)?>/g;
    let mm;
    while ((mm = re.exec(html))) {
      const e = mkEl(mm[1]); e.open = !!mm[2];
      e.querySelectorAll = () => [];
      out.push(e);
    }
  } else if (sel === '.chart-wrap > div') {
    return [];
  }
  return out;
}
const scenHost = mkEl('scenChannels');
mkEl('ridgeScenFold').querySelectorAll = () => [];
SCEN.order.forEach(k => {
  mkEl('scen-chart-' + k); mkEl('scen-cap-' + k); mkEl('graph-panel-delta_' + k);
});
const plots = [];
const globalDoc = {
  getElementById: id => registro[id] || null,
  querySelector: () => null,
};
const PlotlyStub = { react: (div, traces, layout) => { plots.push({ div, traces, layout }); return { then: f => (f && f(), { catch: () => {} }) }; },
                     Plots: { resize: () => {} } };

// ---------------------------------------------------------------------------
// A fabrica de layout REAL, extraida do arquivo entregue.
//
// Isto e o que faltava quando esta secao travou a aba em 2026-09-08. O harness
// passava um `plotlyRenderAndBind` de mentira, entao capturava o `layoutExtra`
// que a secao PEDE e nunca o layout que a pagina RESOLVE -- e o defeito estava
// exatamente na diferenca: `plotlyBaseLayout()` funde por chave, um `xaxis`
// parcial herda `type: 'date'`, e um eixo de 0..12 passa a ser lido como
// milissegundos desde 1970. Medido com Plotly real: 107 s para pintar, 1.001
// rotulos de data em precisao de milissegundo, contra 0,3 s com o eixo certo.
// Nenhuma assercao sobre o `layoutExtra` pedido consegue ver isso.
// O arquivo entregue tem CRLF, entao um terminador de quebra-mais-fecha-chaves
// NUNCA casa: o arquivo traz CR antes de cada LF. Isso fez a extracao devolver
// string vazia SEM ERRO e o harness rodar contra um stub achando que rodava
// contra o real -- o mesmo tipo de degradacao silenciosa que este teste existe
// para pegar. Dai o guarda de tamanho minimo em cada fatia, abaixo.
const srcLF = src.split(String.fromCharCode(13)).join('');
function fatia(ini, fim) {
  const a = srcLF.indexOf(ini);
  if (a < 0) throw new Error('marcador nao encontrado no HTML: ' + ini);
  const b = srcLF.indexOf(fim, a);
  if (b < 0) throw new Error('fim nao encontrado para: ' + ini);
  const out = srcLF.slice(a, b + fim.length);
  if (out.length < 40) throw new Error('fatia curta/vazia para: ' + ini);
  return out;
}
const NL = String.fromCharCode(10);
const CLOSE = NL + '}' + NL;
let LAYOUT_API = null, layoutErr = null;
try {
  LAYOUT_API = new Function('Plotly', 'document', [
    fatia('const PLOTLY_RANGE_SELECTOR = {', NL + '};'),
    fatia('const PLOTLY_CONFIG = {', NL + '};'),
    fatia('function _bindPlotlyYAutofit(divId) {', CLOSE),
    fatia('function plotlyBaseLayout(extra) {', CLOSE),
    fatia('function plotlyRenderAndBind(divId, traces, layoutExtra) {', CLOSE),
    'return { plotlyBaseLayout: plotlyBaseLayout, plotlyRenderAndBind: plotlyRenderAndBind };',
  ].join(NL))(PlotlyStub, globalDoc);
} catch (e) { layoutErr = e; }

// A secao NAO le mais o estado da grade de previsao. Ela era gravadora ate
// 2026-09-09 -- uma fileira de tags que reescrevia as doze caixas do canal em
// um clique -- e virou somente leitura, entao o que ela precisa do escopo de
// renderRidgeTab() sao os formatadores, os rotulos de canal e a fabrica de
// layout REAL. Passar `levels`/`resolvedFlags` aqui manteria viva no harness
// uma dependencia que a pagina nao tem mais.
const MES_ABBR = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                  'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
// O MESMO formatador de mes da pagina, nao a identidade. Com `s => s`,
// scenMonth() -- que monta `m + '-01'` antes de formatar -- devolvia
// "2008-08-01" no HTML do teste enquanto a pagina imprime "Aug/2008", e
// qualquer assercao sobre uma celula de mes mediria o stub. Mesmo furo do
// plotlyRenderAndBind de mentira que a 7c-bis registra, num campo de texto.
function mesLeg(m) {
  const [y, mo] = String(m).split('-');
  return MES_ABBR[parseInt(mo, 10) - 1] + '/' + y;
}

function rodar() {
  const api = new Function(
    'D', 'plotlyRenderAndBind', 'CHANNEL_LABELS_RIDGE', 'fmtNumRg', 'fmtSignedRg',
    'monthLabelRg', 'document', 'Plotly',
    codigo + '\n return { scenChannelBody, scenRenderChart, scenSharedTicks, scenElectionTicks, scenElectionPath, scenWorstWindow,'
           + ' scenWhereX, scenXCell, scenAddMonths, SCEN_EP_COLORS, SCEN_VIEW, SCEN };'
  );
  return api(
    D,
    // O de verdade, nao o stub: e o unico jeito de o teste ver o layout que a
    // pagina RESOLVE em vez do que ela pede.
    LAYOUT_API.plotlyRenderAndBind,
    { delta_fiscal: 'Fiscal risk (CDS)', delta_dxy_em: 'EM dollar index', delta_carry_vol: 'Carry / FX vol',
      delta_sp500: 'S&P 500', delta_icbr_usd: 'Commodity index' },
    (v, d) => Number(v).toFixed(d === undefined ? 0 : d),
    (v, d) => (v >= 0 ? '+' : '') + Number(v).toFixed(d === undefined ? 0 : d),
    mesLeg,
    globalDoc, PlotlyStub
  );
}
if (!LAYOUT_API) {
  console.log('  FALHOU  nao foi possivel extrair a fabrica de layout do HTML  -> '
    + (layoutErr && layoutErr.message));
  console.log('');
  console.log('sem a fabrica real o teste mediria um stub, que foi exatamente o furo');
  console.log('que deixou a aba travar. Abortando.');
  process.exit(1);
}
let API = null;
let erro = null;
try { API = rodar(); } catch (e) { erro = e; }
ok(!erro, 'a secao executa sem lancar', erro && (erro.message + '\n' + String(erro.stack).split('\n')[1]));
if (!API) { console.log('\nnao executou, abortando'); process.exit(1); }

sec('7a. o que foi renderizado');
const html = scenHost.innerHTML;
ok(html.length > 2000, 'o host recebeu HTML', String(html.length));
const folds = (html.match(/<details class="scen-ch"/g) || []).length;
ok(folds === SCEN.order.length,
   'um click-drop por variavel exogena, ' + SCEN.order.length + ' no total -- foi o pedido explicito',
   String(folds));
const abertos = (html.match(/<details class="scen-ch" id="[^"]+" open>/g) || []).length;
ok(abertos === 1, 'apenas o canal medido abre por default (cinco abertos seriam a parede que o fold evita)',
   String(abertos));
SCEN.order.forEach(k => {
  ok(html.indexOf('id="scen-ch-' + k + '"') >= 0, 'fold do canal ' + k + ' presente');
});
// Ordem: a mesma do payload, que e a ordem do modelo. Se o fiscal nao vier
// primeiro, o unico canal medido fica escondido embaixo de quatro pendentes.
const posicoes = SCEN.order.map(k => html.indexOf('id="scen-ch-' + k + '"'));
ok(posicoes.every((p, i) => i === 0 || p > posicoes[i - 1]),
   'os folds saem na ordem do payload');
const pend = (html.match(/class="scen-pending"/g) || []).length;
ok(pend === SCEN.order.filter(k => SCEN.channels[k].pending).length,
   'cada canal pendente diz que nao foi medido, em vez de sair vazio', String(pend));

sec('7b. a manchete e DERIVADA, nao escrita');
const faixaCrise = crises.map(e => e.peak_x);
const esperadoCrise = Math.min.apply(null, faixaCrise).toFixed(1) + 'x&ndash;'
  + Math.max.apply(null, faixaCrise).toFixed(1) + 'x';
ok(html.indexOf(esperadoCrise) >= 0,
   'a faixa de crise impressa e a calculada dos episodios (' + esperadoCrise + ')');
const faixaElec = eleicoes.filter(e => e.complete).map(e => e.peak_x);
const esperadoElec = Math.min.apply(null, faixaElec).toFixed(1) + 'x&ndash;'
  + Math.max.apply(null, faixaElec).toFixed(1) + 'x';
ok(html.indexOf(esperadoElec) >= 0,
   'e a faixa de eleicao tambem (' + esperadoElec + ')');
crises.forEach(e => {
  ok(html.indexOf(e.months_to_peak + ' month') >= 0,
     'a manchete cita os ' + e.months_to_peak + ' meses de ' + e.id);
});

sec('7c. a tabela de episodios e a de turnos');
// O spike diario estava no payload e nao era desenhado por ninguem na
// primeira versao desta secao -- serie morta no payload mais uma promessa
// solta na prosa ("where a spike is worth knowing, it is reported
// separately"). E o modo de falha que o CLAUDE.md deste relatorio ja
// registrou duas vezes: um payload carrega serie que nenhum grafico usa e
// nada acusa.
EP.filter(e => e.spike).forEach(e => {
  ok(html.indexOf(scenNum(e.spike.value)) >= 0,
     'o pior dia de ' + e.id + ' (' + e.spike.value.toFixed(0) + ') aparece na tabela');
});
ok(/Worst day/.test(html), 'a coluna do pior dia tem cabecalho');
ok(/cannot represent/.test(html),
   'e a nota explica por que um caminho mensal nao carrega o pico do dia');
ok((html.match(/<table class="scen-table">/g) || []).length === 3,
   '3 tabelas: episodios, turnos e distribuicao',
   String((html.match(/<table class="scen-table">/g) || []).length));
EP.forEach(ep => ok(html.indexOf('>' + ep.label) >= 0 || html.indexOf(ep.label) >= 0,
                    'episodio ' + ep.id + ' aparece na tabela'));
ok((html.match(/class="scen-partial"/g) || []).length >= 1,
   'o episodio em andamento sai marcado como parcial');
ok(html.indexOf('in progress') >= 0, 'e diz "in progress" no rotulo da linha');
// O caveat mora ao lado do episodio que ele qualifica -- e o botao que carrega
// a crise de 2008 fica na mesma tela que o aviso de que a base e cotacao
// congelada.
// Desde 2026-09-08 NENHUM episodio tem ressalva: as duas que existiam eram
// defeitos da fonte antiga do CDS (cotacao congelada em 2008, dez/2015 ausente)
// e sumiram com a troca para a Bloomberg. Isso deixa o caminho de renderizacao
// sem exercicio pelo dado real, que e' precisamente o estado em que ninguem
// percebe que ele quebrou -- entao ele passa a ser exercitado SINTETICAMENTE,
// injetando uma ressalva num episodio e re-renderizando. Mesmo instinto da
// faixa de frescor do relatorio de politica monetaria.
const comCaveat = EP.filter(e => e.caveat);
ok(comCaveat.length === 0,
   'nenhum episodio tem ressalva hoje -- as duas antigas eram da fonte aposentada',
   String(comCaveat.length));
comCaveat.forEach(e => ok(html.indexOf('read the base with care') >= 0 && html.indexOf(e.caveat.slice(0, 40)) >= 0,
                          'a ressalva de ' + e.id + ' e impressa'));
{
  const FAKE = 'Base month is a stale print and the multiple is measured off it.';
  const clone = JSON.parse(JSON.stringify(SCEN));
  clone.channels.fiscal.episodes[0].caveat = FAKE;
  const htmlFake = API.scenChannelBody('fiscal', clone.channels.fiscal);
  ok(htmlFake.indexOf(FAKE.slice(0, 40)) >= 0,
     'e uma ressalva injetada AINDA e impressa -- o caminho nao apodreceu sem uso');
  ok(htmlFake.indexOf('read the base with care') >= 0,
     'com o aviso que a introduz');
}

sec('7c-bis. O EIXO QUE A PAGINA RESOLVE (o defeito que travou a aba)');
ok(!layoutErr, 'plotlyBaseLayout/plotlyRenderAndBind foram extraidos do HTML',
   layoutErr && layoutErr.message);
const plotScen = plots.filter(p => p.div === 'scen-chart-fiscal')[0];
ok(!!plotScen, 'o grafico de cenarios chegou ao Plotly com um layout resolvido');
if (plotScen) {
  const ax = plotScen.layout.xaxis || {};
  // O x deste grafico e CONTAGEM DE MESES desde a base (0..12), nao data.
  const xs = (plotScen.traces || []).map(t => t.x && t.x[0]).filter(v => v !== undefined);
  ok(xs.length > 0 && xs.every(v => typeof v === 'number'),
     'as abscissas sao numeros (contagem de meses), nao string de data');
  ok(ax.type === 'linear',
     'e o eixo X RESOLVIDO e linear -- em `date` os 13 inteiros viram milissegundos desde 1970',
     'type=' + ax.type);
  ok(ax.type !== 'date',
     'nunca `date`: foi o que fez a aba levar 107 s para pintar em vez de 0,3 s');
  // `dtick: 1` significa 1 unidade num eixo linear e 1 MILISSEGUNDO num eixo de
  // data. E a mesma linha de codigo com dois significados a tres ordens de
  // grandeza de distancia, e so o `type` resolvido distingue.
  ok(ax.dtick === 1 && ax.type === 'linear',
     'dtick=1 vale 1 mes porque o eixo e linear (num eixo de data valeria 1 ms)');
  // Os dois componentes que so existem para eixo de data nao podem sobreviver.
  ok(!ax.rangeselector || ax.rangeselector.visible === false,
     'o rangeselector de passos ANUAIS nao sobrevive num eixo de meses');
  ok(!ax.rangeslider || ax.rangeslider.visible === false,
     'nem o rangeslider');
}
// A regra generica, valendo para qualquer grafico que esta secao venha a
// desenhar: abscissa numerica nunca resolve para eixo de data.
plots.forEach(pl => {
  const ax = (pl.layout && pl.layout.xaxis) || {};
  const x0 = (pl.traces || []).map(t => t.x && t.x[0]).filter(v => v !== undefined)[0];
  if (typeof x0 === 'number') {
    ok(ax.type && ax.type !== 'date',
       pl.div + ': abscissa numerica -> eixo nao pode ser `date`', 'type=' + ax.type);
  }
});

sec('7d. o grafico abre na vista ELEITORAL, com MES DE CALENDARIO no eixo');
// A vista eleitoral e o default porque a aba e lida em ano de eleicao, e e a
// unica das duas cujo eixo pode nomear meses -- o que so vale porque as sete
// eleicoes partem do mesmo mes do calendario (a base e o mes do voto menos
// doze, e todo primeiro turno cai em outubro). Se um dia isso deixar de valer,
// e o guarda logo abaixo que avisa, e o grafico volta a contar meses.
function nomesDe(pl) { return (pl.traces || []).map(t => t.name); }
const chart = plots.filter(p => p.div === 'scen-chart-fiscal').slice(-1)[0];
ok(!!chart, 'o grafico do canal fiscal foi plotado');
if (chart) {
  ok(chart.traces.length === eleicoes.length + 1,
     eleicoes.length + ' eleicoes + a linha da base', String(chart.traces.length));
  ok(eleicoes.every(e => nomesDe(chart).indexOf(e.label) >= 0),
     'todas as eleicoes estao no grafico');
  ok(crises.every(e => nomesDe(chart).indexOf(e.label) < 0),
     'e NENHUMA crise -- as duas vistas nao se misturam, porque os dois eixos X nao sao o mesmo eixo');
  const base = chart.traces[chart.traces.length - 1];
  ok(base.y.every(v => v === 1) && base.showlegend === false,
     'a linha de referencia e constante em 1,0x e fica fora da legenda');
  // 14 posicoes desde 2026-09-09: doze fechamentos mensais e os DOIS TURNOS.
  // Outubro era um ponto so, e era o fechamento do mes -- que cai depois do 2o
  // turno e esconde a unica parte da corrida que acontece em dias.
  const tt = chart.layout.xaxis.ticktext;
  const tv = chart.layout.xaxis.tickvals;
  const NPTS = SCEN.horizon + 2;
  ok(Array.isArray(tt) && tt.length === NPTS,
     NPTS + ' rotulos no eixo X: ' + SCEN.horizon + ' meses + os dois turnos', tt && String(tt.length));
  ok(Array.isArray(tv) && tv.length === NPTS && tv[0] === 0 && tv[NPTS - 1] === NPTS - 1,
     'e um tickval por posicao, sobre os mesmos inteiros 0..' + (NPTS - 1));
  // Os rotulos de mes sao DERIVADOS do mes-base dos episodios, nao escritos:
  // escrever "Oct" a mao passaria a mentir no dia em que a data do primeiro
  // turno mudasse, sem levantar nada.
  const mesBase = parseInt(String(eleicoes[0].base_month).slice(5, 7), 10);
  ok(tt && tt[0].indexOf(MES_ABBR[mesBase - 1]) === 0,
     'o primeiro rotulo e o mes-base dos episodios (' + MES_ABBR[mesBase - 1] + ')', tt && tt[0]);
  ok(tt && /base/.test(tt[0]), 'e se anuncia como a base');
  ok(tt && tt[SCEN.horizon - 1].indexOf(MES_ABBR[(mesBase - 2 + SCEN.horizon) % 12]) === 0,
     'o ultimo rotulo MENSAL e o mes anterior ao voto ('
       + MES_ABBR[(mesBase - 2 + SCEN.horizon) % 12] + ')', tt && tt[SCEN.horizon - 1]);
  ok(tt && tt[SCEN.horizon] === '1st round' && tt[SCEN.horizon + 1] === 'Runoff',
     'e as duas ultimas posicoes sao os turnos, nomeados',
     tt && (tt[SCEN.horizon] + ' / ' + tt[SCEN.horizon + 1]));
  ok(tt && tt.every(v => !/vote/.test(v)),
     'nao ha mais um "Oct (vote)": outubro deixou de ser um ponto so');
  ok(!/Months from/.test(chart.layout.xaxis.title),
     'o titulo do eixo nomeia o mes em vez de contar meses', chart.layout.xaxis.title);
  ok(/rounds/.test(chart.layout.xaxis.title),
     'e diz que os dois ultimos pontos sao os turnos', chart.layout.xaxis.title);
  ok(chart.layout.yaxis.ticksuffix === 'x',
     'o eixo Y diz que a unidade e MULTIPLO da base, nao bps');
  // O rotulo do eixo e um nome de mes compartilhado por sete anos diferentes,
  // entao o mes de verdade tem de estar no hover -- em nenhuma das duas vistas
  // o eixo sozinho diz de que ano e o ponto.
  const cd = chart.traces[0].customdata;
  ok(Array.isArray(cd) && /\w{3}\/\d{4}/.test(cd[0]),
     'o hover carrega o mes REAL do ponto (o eixo nao diz o ano)', cd && cd[0]);
  // Os dois ultimos rotulos sao os mesmos nas sete eleicoes, entao a data do
  // turno so existe no hover.
  const epHover = eleicoes.filter(e => e.label === chart.traces[0].name)[0];
  ok(!!epHover && cd[SCEN.horizon].indexOf(epHover.round1) >= 0,
     'e o hover do 1o turno traz a DATA daquele turno (' + (epHover && epHover.round1) + ')',
     cd[SCEN.horizon]);
  ok(!!epHover && cd[SCEN.horizon + 1].indexOf(epHover.round2) >= 0,
     'e o do 2o turno idem (' + (epHover && epHover.round2) + ')', cd[SCEN.horizon + 1]);
  // Os dois pontos novos sao NIVEL DIARIO no dia de cada turno, dividido pela
  // mesma base -- nao mais um fechamento mensal. Refeito aqui a partir do
  // payload, e nao lido da funcao da pagina.
  eleicoes.forEach(ep => {
    const tr = chart.traces.filter(t => t.name === ep.label)[0];
    if (!tr) { ok(false, ep.id + ': traco ausente'); return; }
    ok(tr.y.length === NPTS, ep.id + ': ' + NPTS + ' pontos', String(tr.y.length));
    ok(tr.y.slice(0, SCEN.horizon).every((v, h) => v === ep.path[h]),
       ep.id + ': os ' + SCEN.horizon + ' primeiros continuam sendo os fechamentos mensais');
    const ir = ep.inter_round;
    if (ir && ir.at_r1 !== null && ir.at_r1 !== undefined) {
      ok(perto(tr.y[SCEN.horizon], ir.at_r1 / ep.base, 1e-9),
         ep.id + ': o penultimo ponto e o nivel do 1o turno / base',
         tr.y[SCEN.horizon] + ' vs ' + (ir.at_r1 / ep.base));
      ok(tr.y[SCEN.horizon] !== ep.path[SCEN.horizon],
         ep.id + ': e NAO e o fechamento de outubro, que era o ponto antigo');
    } else {
      ok(tr.y[SCEN.horizon] === null,
         ep.id + ': eleicao sem 1o turno realizado nao inventa ponto');
    }
    if (ir && ir.at_r2 !== null && ir.at_r2 !== undefined) {
      ok(perto(tr.y[SCEN.horizon + 1], ir.at_r2 / ep.base, 1e-9),
         ep.id + ': o ultimo ponto e o nivel do 2o turno / base');
    } else {
      ok(tr.y[SCEN.horizon + 1] === null,
         ep.id + ': sem 2o turno realizado, sem ponto');
    }
  });
  // A faixa cinza nao e decoracao: ali a base de medicao troca de fechamento
  // MENSAL para leitura DIARIA, e sem marcacao os dois ultimos pontos leriam
  // como mais dois meses.
  const faixa = (chart.layout.shapes || [])[0];
  ok(!!faixa, 'a vista eleitoral desenha a faixa dos turnos');
  if (faixa) {
    ok(faixa.x0 === SCEN.horizon - 0.5 && faixa.x1 === SCEN.horizon + 1.5,
       'e ela cobre exatamente as duas posicoes dos turnos',
       '[' + faixa.x0 + ', ' + faixa.x1 + ']');
    ok(faixa.yref === 'paper' && faixa.layer === 'below',
       'de cima a baixo e por tras das linhas');
  }
  const pontilhadas = chart.traces.filter(t => t.line && t.line.dash === 'dot').length;
  ok(pontilhadas === eleicoes.filter(e => !e.complete).length,
     'a eleicao em andamento sai pontilhada, e so ela', String(pontilhadas));
  ok(chart.traces.slice(0, eleicoes.length).every(t => t.connectgaps === false),
     'connectgaps=false -- a cauda nula NAO e ligada por uma reta que inventaria dado');
  // Cores proprias: reusar a paleta dos canais faria "eleicao de 2018" ler como
  // o mesmo objeto que um regressor do resto da aba. E DISTINTA nao basta --
  // .claude/rules/lis-dashboards.md exige dE2000 >= 20 entre quaisquer duas
  // series que possam dividir um grafico, e estas sete dividem.
  const cores = Array.from(new Set(chart.traces.slice(0, eleicoes.length).map(t => t.line.color)));
  ok(cores.length === eleicoes.length, 'uma cor distinta por eleicao', String(cores.length));
  const pior = worstPair(cores);
  ok(pior.deltaE >= 20, 'e o pior par da vista eleitoral fica em dE2000 >= 20',
     pior.deltaE.toFixed(1) + '  (' + pior.pair.join(' x ') + ')');
  // A cor vem da posicao no ACERVO, nao na vista, para um episodio nao trocar
  // de cor quando a vista troca. So esta vista distingue as duas regras: as
  // crises sao os tres primeiros do acervo, entao la os dois indices coincidem
  // e a assercao nao segura nada.
  const paletaAcervo = API.SCEN_EP_COLORS;
  ok(chart.traces.slice(0, eleicoes.length).every(function (t) {
       const idx = EP.map(e => e.label).indexOf(t.name);
       return t.line.color === paletaAcervo[idx % paletaAcervo.length];
     }),
     'e cada eleicao usa a cor do seu indice no acervo (indices 3..9, nao 0..6)');
}
// O guarda dos rotulos, exercitado nos dois sentidos: eleicoes compartilham o
// mes-base, crises nao, e uma base divergente derruba os rotulos em vez de
// rotular sete anos com o mes de um deles.
ok(API.scenSharedTicks(eleicoes, SCEN.horizon) !== null,
   'as eleicoes compartilham o mes-base, que e o que autoriza o eixo de calendario');
ok(API.scenSharedTicks(crises, SCEN.horizon) === null,
   'as crises NAO compartilham, e e por isso que a vista de crise conta meses');
{
  const misturado = [eleicoes[0], Object.assign({}, eleicoes[1], { base_month: '2013-03' })];
  ok(API.scenSharedTicks(misturado, SCEN.horizon) === null,
     'e um mes-base divergente devolve null em vez de rotular com o mes de um deles');
  // O fallback nao pode perder os turnos: sem mes compartilhado o eixo volta a
  // contar, mas as duas ultimas posicoes continuam sendo o 1o e o 2o turno.
  const tks = API.scenElectionTicks(misturado);
  ok(tks.length === SCEN.horizon + 2 && tks[0] === '0'
     && tks[SCEN.horizon] === '1st round' && tks[SCEN.horizon + 1] === 'Runoff',
     'e o fallback conta meses SEM perder os dois turnos', tks.slice(0, 2).concat(tks.slice(-2)).join(' | '));
}
// O cabecalho do grafico e derivado: com uma pill escolhendo o que e plotado,
// texto fixo ali seria contradito por um clique.
{
  const cap = registro['scen-cap-fiscal'].innerHTML;
  ok(/Election years/.test(cap), 'o cabecalho do grafico nomeia a vista eleitoral', cap.slice(0, 70));
  ok(cap.indexOf(eleicoes.length + ' episodes') >= 0,
     'e conta os episodios da vista, nao os do acervo', cap.slice(0, 160));
  ok(cap.indexOf(mesLeg(eleicoes[0].base_month)) >= 0,
     'com a janela coberta pela vista');
}

sec('7e. as duas pills, e o clique que troca a vista');
const pills = scenHost.querySelectorAll('.scen-kind-pill');
// Um canal pendente nao chega a ter pill (o corpo dele e a nota de pendencia),
// entao as duas sao as do canal medido.
ok(pills.length === 2, 'duas pills -- uma por tipo de janela do canal medido', String(pills.length));
const pillDe = k => pills.filter(p => p.dataset.scenKind === k)[0];
ok(!!pillDe('election') && !!pillDe('crisis'), 'uma eleitoral e uma de crise');
// Ordem no DOM: pills, depois o cabecalho derivado, depois o grafico. O
// cabecalho tem de ficar DENTRO do card e ACIMA do plot (um print da regiao do
// grafico nao inclui o titulo da secao), e a regua de controle acima dele. Este
// relatorio ja teve pill posicionada do lado errado do grafico noutra aba.
const iPill = html.indexOf('scen-kind-row');
const iCap = html.indexOf('id="scen-cap-fiscal"');
const iPlot = html.indexOf('id="scen-chart-fiscal"');
ok(iPill > 0 && iCap > iPill && iPlot > iCap,
   'no DOM: pills -> cabecalho derivado -> grafico',
   'pill@' + iPill + ' cap@' + iCap + ' plot@' + iPlot);
ok(pills.filter(p => p.classList.contains('is-on')).length === 1,
   'exatamente uma ativa (a pill nao pode discordar do grafico que ja foi plotado)');
ok(pillDe('election').classList.contains('is-on'),
   'e a ativa e a ELEITORAL, que e o default do ano em curso');

const antesDoClique = plots.length;
pillDe('crisis').dispatch('click');
ok(plots.length === antesDoClique + 1, 'clicar em Crises redesenha o grafico',
   antesDoClique + ' -> ' + plots.length);
const chartCrise = plots[plots.length - 1];
ok(chartCrise.div === 'scen-chart-fiscal', 'no mesmo div, nao num segundo grafico');
ok(chartCrise.traces.length === crises.length + 1,
   crises.length + ' crises + a linha da base', String(chartCrise.traces.length));
ok(crises.every(e => nomesDe(chartCrise).indexOf(e.label) >= 0)
   && eleicoes.every(e => nomesDe(chartCrise).indexOf(e.label) < 0),
   'e a vista de crise traz SO crises');
// O eixo tem de voltar a contar meses: as tres crises partem de meses
// diferentes, e um rotulo de calendario ali estaria certo para uma delas e
// errado para as outras duas, sem nenhum sintoma.
ok(!chartCrise.layout.xaxis.ticktext,
   'o eixo volta a CONTAR meses, sem rotulo de calendario');
ok(chartCrise.traces[0].y.length === SCEN.horizon + 1,
   'e a crise volta a ter ' + (SCEN.horizon + 1) + ' pontos: ela nao tem turnos',
   String(chartCrise.traces[0].y.length));
// A faixa TEM de ser passada vazia, nao omitida: com Plotly.react um layout
// sem a chave herda a forma do desenho anterior, e a vista de crise ficaria
// com a marca dos turnos por cima de dois meses quaisquer.
ok(Array.isArray(chartCrise.layout.shapes) && chartCrise.layout.shapes.length === 0,
   'e a faixa dos turnos e limpa explicitamente ao trocar de vista',
   JSON.stringify(chartCrise.layout.shapes));
ok(/Months from the base/.test(chartCrise.layout.xaxis.title),
   'e o titulo do eixo diz isso', chartCrise.layout.xaxis.title);
ok(chartCrise.layout.xaxis.type === 'linear',
   'e o eixo RESOLVIDO segue linear nas duas vistas -- em `date` a aba trava (ver 7c-bis)',
   'type=' + chartCrise.layout.xaxis.type);
ok(pillDe('crisis').classList.contains('is-on') && !pillDe('election').classList.contains('is-on'),
   'a pill ativa acompanha o clique (estado valido no objeto e velho na tela e o modo de falha)');
// A cor vem da posicao no ACERVO, nao na vista: um episodio nao pode trocar de
// cor quando a vista troca, senao a memoria visual entre as duas se perde.
const paleta = API.SCEN_EP_COLORS;
ok(Array.isArray(paleta) && paleta.length >= EP.length, 'a paleta cobre o acervo inteiro');
const coresOk = chartCrise.traces.slice(0, crises.length).every(function (t) {
  const idx = EP.map(e => e.label).indexOf(t.name);
  return t.line.color === paleta[idx % paleta.length];
});
ok(coresOk, 'e cada crise usa a cor do seu indice no acervo, nao do indice na vista');

const antesDeVoltar = plots.length;
pillDe('election').dispatch('click');
ok(plots.length === antesDeVoltar + 1, 'voltar para Election years redesenha de novo');
ok(Array.isArray(plots[plots.length - 1].layout.xaxis.ticktext),
   'e os rotulos de calendario voltam');
ok((plots[plots.length - 1].layout.shapes || []).length === 1,
   'com a faixa dos turnos junto');
ok(/Crises/.test(registro['scen-cap-fiscal'].innerHTML) === false,
   'o cabecalho do grafico volta com a vista');
const antesDeRepetir = plots.length;
pillDe('election').dispatch('click');
ok(plots.length === antesDeRepetir,
   'e clicar na pill JA ativa nao redesenha nada');

// Um canal com um tipo so ainda mostra as duas pills, a inaplicavel desligada
// com o motivo -- pill ausente nao responde "onde estao as crises deste
// canal?". Exercitado sinteticamente porque o unico canal medido tem os dois
// tipos, que e' exatamente o estado em que ninguem percebe que o caminho
// quebrou.
{
  const soCrise = JSON.parse(JSON.stringify(fiscal));
  soCrise.episodes = soCrise.episodes.filter(e => e.kind === 'crisis');
  const h2 = API.scenChannelBody('fiscal', soCrise);
  ok(/scen-kind-pill[^"]*is-off[^"]*" data-scen-ch="fiscal" data-scen-kind="election"/.test(h2),
     'a pill eleitoral de um canal sem eleicao sai desligada, nao ausente');
  ok(/No episodes of this kind/.test(h2), 'com o motivo no title');
  ok(/data-scen-kind="crisis"/.test(h2) && !/is-off[^"]*" data-scen-ch="fiscal" data-scen-kind="crisis"/.test(h2),
     'e a de crise segue clicavel');
}

sec('7f. a distribuicao sai em MULTIPLOS, a unidade do resto da secao');
// O defeito que motivou a reescrita: a distribuicao e medida como variacao em
// LOG por cento, e a secao inteira fala em multiplos. A tabela imprimia os
// numeros de log sob um cabecalho de "%", ao lado de uma tabela de multiplos --
// e a prosa lia "+50%" como um em dez anos quando o percentil 90 de doze meses
// e 1,79x, ou seja +79%. As duas unidades se parecem e nao sao a mesma, e nada
// na pagina podia contradizer a leitura errada.
const iDistHdr = html.indexOf('Calmest 1 in 20');
ok(iDistHdr > 0, 'a tabela de distribuicao tem cabecalho legivel em frequencia');
const tblDist = html.slice(html.lastIndexOf('<table', iDistHdr), html.indexOf('</table>', iDistHdr));
ok(tblDist.indexOf('%') < 0,
   'nenhuma celula dela sai em % -- era o que a tornava incomparavel com o resto da secao');
const tdDist = (tblDist.match(/<td>[^<]*<\/td>/g) || []);
ok(tdDist.length === 4 * 7, '4 horizontes x (6 percentis + n) celulas', String(tdDist.length));
ok(tdDist.filter(c => /x<\/td>$/.test(c)).length === 4 * 6,
   'e 24 delas sao multiplos', String(tdDist.filter(c => /x<\/td>$/.test(c)).length));
// A conversao e EXATA e nao aproximada: um quantil sobrevive a qualquer
// transformacao crescente, entao exp() do percentil 90 do log E o percentil 90
// da razao. (O desvio-padrao nao sobreviveria, e por isso nao e impresso.)
ok(API.scenXCell(0) === '1.00x', 'log 0 e exatamente 1,00x', API.scenXCell(0));
['p5', 'p50', 'p90', 'p95', 'p99', 'max'].forEach(k => {
  const esperado = Number(Math.exp(dist['12m'][k] / 100)).toFixed(2) + 'x';
  ok(tblDist.indexOf('>' + esperado + '<') >= 0,
     'o ' + k + ' de 12 meses sai como ' + esperado + ' (log ' + dist['12m'][k] + ')');
});
ok(tblDist.indexOf('12 months') >= 0 && tblDist.indexOf('1 month') >= 0,
   'e o horizonte esta em palavras, nao em "12m"');
ok(tblDist.indexOf(String(dist['12m'].n)) >= 0,
   'a contagem de janelas e impressa (elas se sobrepoem, e a nota diz isso)');
ok(/overlap/.test(html), 'e a nota avisa que as janelas se sobrepoem');
// A frase que localiza os episodios nomeados na distribuicao e derivada dos
// MESMOS percentis, entao nao pode divergir da linha acima dela.
const piorCriseX = Math.max.apply(null, crises.map(e => e.peak_x));
const faixaPior = API.scenWhereX(dist['12m'], piorCriseX);
// A conta refeita AQUI, e nao a funcao da pagina, e o gabarito: comparar o
// texto impresso com o retorno da propria funcao passa junto com ela se ela
// esquecer o exp() -- as duas pontas mutariam ao mesmo tempo e a assercao
// viraria tautologia.
const faixaEsperada = (function () {
  const r = dist['12m'], x = piorCriseX, mx = v => Math.exp(v / 100);
  if (x > mx(r.max)) return 'beyond anything in the record';
  if (x >= mx(r.p99)) return 'worse than 99 in every 100';
  if (x >= mx(r.p95)) return 'inside the worst 1 in 20';
  if (x >= mx(r.p90)) return 'inside the worst 1 in 10';
  if (x >= mx(r.p50)) return 'in the upper half';
  return 'in the calmer half';
})();
ok(html.indexOf(faixaEsperada) >= 0,
   'a faixa impressa para a pior crise e a que os percentis pedem ("' + faixaEsperada + '")');
ok(faixaPior === faixaEsperada,
   'e a funcao da pagina concorda com a conta refeita no teste', faixaPior);
// E o achado que justifica a tabela existir: a pior janela de doze meses do
// historico nao e nenhum dos episodios nomeados. Um episodio e ancorado no
// ultimo fechamento calmo antes da corrida, e os doze piores meses de uma
// crise nao precisam comecar ali.
const w12 = API.scenWorstWindow(fiscal, SCEN.horizon);
ok(!!w12 && w12.x > Math.max.apply(null, EP.map(e => e.peak_x)),
   'a pior janela de 12 meses supera TODO episodio nomeado',
   w12 && (w12.x.toFixed(2) + 'x em ' + w12.from + '..' + w12.to));
ok(w12 && html.indexOf(Number(w12.x).toFixed(2) + 'x') >= 0, 'e ela e impressa');
ok(w12 && html.indexOf(mesLeg(w12.from)) >= 0 && html.indexOf(mesLeg(w12.to)) >= 0,
   'com os dois meses em que foi', w12 && (mesLeg(w12.from) + ' a ' + mesLeg(w12.to)));

sec('7g. a secao diz COMO cada janela foi escolhida');
// A pergunta que a secao deixava para o codigo-fonte responder: o inicio de
// uma crise e julgamento e o fim nao e, e ler uma janela de doze meses como
// "quanto tempo a crise durou" erra as duas metades.
ok(/Where each window starts and stops/.test(html), 'o bloco existe');
crises.forEach(e => {
  ok(html.indexOf(mesLeg(e.base_month)) >= 0,
     'o mes-base declarado de ' + e.id + ' e impresso (' + mesLeg(e.base_month) + ')');
});
ok(/not a peak-finder/.test(html),
   'e diz por que a data nao vem de um detector de picos rodado na propria serie');
ok(html.indexOf('exactly ' + SCEN.horizon + ' months from its base') >= 0,
   'e que o FIM e aritmetico: ' + SCEN.horizon + ' meses, o horizonte das caixas');
// `ep.note` existia no dado e nenhum desenho o usava -- campo morto no payload
// mais o leitor sem a unica frase que diz por que estas datas e nao outras. E
// o mesmo modo de falha do `spike` na primeira versao desta secao.
const comNota = EP.filter(e => e.note);
ok(comNota.length >= crises.length, 'as crises trazem nota, e a eleicao em curso tambem',
   String(comNota.length));
comNota.forEach(e => {
  ok(html.indexOf(e.note.slice(0, 45)) >= 0,
     'a nota de ' + e.id + ' e desenhada (era campo morto no dado)');
});
ok(/scen-ep-notes/.test(html), 'num bloco proprio ao lado do criterio de janela');
// O pior dia tambem passou a ser derivado, no mesmo dia e pelo mesmo motivo: a
// frase anterior citava 606 bps, "cinco vezes a base" e um fechamento de 335,
// tres numeros da fonte antiga do CDS que a troca de fonte deixou errados.
const spikeEp = EP.filter(e => e.spike).slice().sort((a, b) => b.spike.x - a.spike.x)[0];
ok(!!spikeEp, 'ha episodio com pico diario');
if (spikeEp) {
  // Fatiado: os mesmos numeros aparecem na coluna "Worst day" da tabela, entao
  // procurar no html inteiro passaria com o rodape inteiramente escrito a mao.
  const iFoot = html.indexOf('<b>Worst day</b> is the highest single print');
  const foot = iFoot >= 0 ? html.slice(iFoot, html.indexOf('</p>', iFoot)) : '';
  ok(foot.length > 200, 'o rodape do pior dia existe', String(foot.length));
  ok(foot.indexOf(spikeEp.spike.date) >= 0,
     'e cita a data do payload (' + spikeEp.spike.date + ')');
  ok(foot.indexOf(Number(spikeEp.spike.x).toFixed(2) + 'x') >= 0,
     'o multiplo do dia, ' + spikeEp.spike.x.toFixed(2) + 'x');
  ok(foot.indexOf(scenNum(spikeEp.spike.value)) >= 0,
     'o nivel do dia, ' + scenNum(spikeEp.spike.value));
  const iM = fiscal.history.months.indexOf(spikeEp.spike.date.slice(0, 7));
  const fech = fiscal.history.values[iM];
  ok(iM >= 0 && foot.indexOf(Number(fech / spikeEp.base).toFixed(2) + 'x') >= 0,
     'e o FECHAMENTO daquele mes, ' + (fech / spikeEp.base).toFixed(2) + 'x -- o numero que um caminho mensal pode carregar');
  ok(iM >= 0 && foot.indexOf(scenNum(fech)) >= 0, 'em nivel tambem');
}

sec('7h. a secao nao escreve mais nas caixas de previsao');
// Era gravadora ate 2026-09-09. Duas afirmacoes, porque as tags saiam do HTML
// e o codigo poderia continuar la (ou voltar num merge) sem sintoma visivel.
ok(!/scen-apply/.test(html) && !/scen-msg/.test(html),
   'nenhuma tag de carregar episodio, nem a caixa de mensagem dela, no HTML gerado');
ok(codigo.indexOf('scenApplyEpisode') < 0 && codigo.indexOf('resolvedFlags') < 0,
   'e nada no codigo da secao toca no estado da grade de previsao');
ok(Object.keys(API).indexOf('scenApplyEpisode') < 0,
   'a secao nao expoe mais uma funcao de aplicar');
// O que SOBREVIVEU da versao gravadora e a medicao de que ela dependia: a
// regra multiplicativa, agora dita ao leitor em vez de executada. E ela e
// DERIVADA do flag por canal, para o proximo canal nao herdar a resposta do
// CDS por acidente.
ok(fiscal.is_multiplicative === true, 'o canal fiscal esta medido como multiplicativo');
ok(/<b>multiply<\/b>/.test(html), 'e a instrucao na tela e multiplicar');
{
  const aditivo = JSON.parse(JSON.stringify(fiscal));
  aditivo.is_multiplicative = false;
  const h3 = API.scenChannelBody('fiscal', aditivo);
  ok(/<b>add<\/b>/.test(h3) && !/<b>multiply<\/b>/.test(h3),
     'um canal medido como aditivo recebe a instrucao contraria, nao a mesma');
}

// ---------------------------------------------------------------------------
// 8. a prosa e escrita para quem abre a pagina
// ---------------------------------------------------------------------------
// Guarda do mesmo tipo do de tests/test_release_calendar_js.js: a prosa e o
// unico conteudo que nenhuma outra assercao olha, e o modo de falha conhecido
// deste repositorio e herdar o vocabulario da sessao em que o mecanismo foi
// construido.
sec('8. a prosa nao fala do mecanismo');
const iBody = src.indexOf('<div class="fold-body">', iScen);
const proseHtml = src.slice(iBody, src.indexOf('</details>', iBody)) + html;
const PROIBIDOS = [
  'exog_scenarios', 'build_payload', 'ridge_deviation_model', 'refreshBoxDisplay',
  'is_multiplicative', 'resolvedFlags', 'levels[', 'payload', 'RIDGE_DATA',
  'cmb_risco_pais', 'MySQL', 'ETL', 'generate_report', 'run(',
  'monthly close basis', 'ratio path',
  // Referencia a NOSSA conversa em vez de ao leitor. A primeira versao do
  // texto de canal pendente dizia "done first at the user's request", que e
  // exatamente o defeito que .claude/rules/lis-dashboards.md registra: quem
  // abre a pagina nao sabe que houve pedido nem de quem.
  'the user', 'at our request', 'we decided', 'this round', 'this session',
  // ASCII no lugar da entidade: sai literal na tela.
  ' -- ',
];
PROIBIDOS.forEach(t => {
  ok(proseHtml.indexOf(t) < 0, 'a prosa nao usa "' + t + '"');
});

// A lista acima tinha '2026-09-08' como termo literal, para pegar a data de
// CONSTRUCAO vazando no texto -- o defeito "Desde 2026-08-31" que
// .claude/rules/lis-dashboards.md registra. Ela saiu porque no mesmo dia essa
// data virou o ULTIMO DIA DO DADO, que o rodape imprime como procedencia e que
// e' exatamente o comportamento certo (derivado do payload, nao escrito na
// prosa). Um literal nao distingue as duas, entao a assercao passou a ser sobre
// a FORMA: uma data so e' aceitavel na prosa se vier de um campo do payload.
// TEXTO VISIVEL, nao o HTML bruto: o recorte do fold arrasta um <script> com
// series diarias serializadas, e uma varredura por data casaria com milhares de
// rotulos de eixo. Os termos proibidos acima toleram isso por serem palavras
// distintivas; uma data nao e. Tirar script/style e as tags e' o que faz a
// assercao falar do que o leitor ve.
const textoVisivel = proseHtml
  .replace(/<script[\s\S]*?<\/script>/gi, ' ')
  .replace(/<style[\s\S]*?<\/style>/gi, ' ')
  .replace(/<[^>]+>/g, ' ');
const datasNaProsa = (textoVisivel.match(/\d{4}-\d{2}-\d{2}/g) || []);
const datasDoPayload = new Set();
Object.keys(SCEN.channels || {}).forEach(k => {
  const ch = SCEN.channels[k];
  if (!ch || typeof ch !== 'object') return;
  if (ch.last_daily_date) datasDoPayload.add(ch.last_daily_date);
  (ch.episodes || []).forEach(e => {
    if (e.spike && e.spike.date) datasDoPayload.add(e.spike.date);
    if (e.round1) datasDoPayload.add(e.round1);
    if (e.round2) datasDoPayload.add(e.round2);
  });
});
const orfas = datasNaProsa.filter(d => !datasDoPayload.has(d));
ok(orfas.length === 0,
   'toda data na prosa vem de um campo do payload -- nenhuma data de construcao',
   orfas.slice(0, 3).join(', '));
ok(datasDoPayload.size > 0 && datasNaProsa.length > 0,
   'e a assercao acima tem o que checar (ha data impressa e ha data no payload)',
   datasNaProsa.length + ' na prosa / ' + datasDoPayload.size + ' no payload');
// E diz as tres coisas que o leitor precisa: o que e a base, por que o pico e
// mensal, e que os outros canais nao se movem sozinhos.
ok(/highest <i>monthly close<\/i>/.test(proseHtml) || /highest .{0,20}monthly close/.test(proseHtml),
   'explica que o pico e de fechamento mensal');
ok(/three-day spike|cannot represent|single day/.test(proseHtml),
   'e por que nao e o pico do dia');
ok(/separate channel in the same regression/.test(proseHtml),
   'avisa que o indice de dolar EM e outro canal do mesmo modelo');
ok(/stay where you left them/.test(proseHtml),
   'e que carregar um episodio nao move os outros quatro canais');
// As duas metades do aviso: a primeira diz o QUE acontece, a segunda diz que
// deixar os outros parados e ELE MESMO uma hipotese. Um mutante que troque
// so a segunda por "and that is fine" passa por cima do sentido inteiro e
// mantem a primeira intacta -- dai as duas assercoes.
ok(/a choice you are making, not a neutral default/.test(proseHtml),
   'e que deixar os outros parados e uma escolha, nao um default neutro');

// ---------------------------------------------------------------------------
// 8b. e nao contradiz os numeros impressos ao lado dela
// ---------------------------------------------------------------------------
sec('8b. a prosa nao promete controle que saiu nem afirma o que os numeros negam');
['Load one into', 'the buttons below', 'Each button', 'Reset shocks', 'straight into the boxes']
  .forEach(t => {
    ok(proseHtml.indexOf(t) < 0, 'nada promete um controle que a secao nao tem: "' + t + '"');
  });
// A manchete AFIRMAVA "a maior corrida eleitoral e menor que a mais branda das
// crises". Era verdade da serie que comecava em 2007-12 e falsa desde que o CDS
// trocou de fonte e trouxe 2001-2007 -- e a frase ficou hard-coded ao lado de
// duas faixas DERIVADAS que a contradiziam, porque nenhuma assercao olhava para
// ela. Este bloco e o guarda que faltava.
['smaller than the mildest', 'run-up on record is smaller'].forEach(t => {
  ok(proseHtml.indexOf(t) < 0, 'a manchete aposentada nao voltou: "' + t + '"');
});
const topEleicao = eleicoesCompletas.filter(e => e.peak_x === piorEleicao)[0];
ok(/bimodal/.test(proseHtml), 'e a leitura atual, bimodal, esta na tela');
ok(proseHtml.indexOf(topEleicao.label + '</b> &mdash; stands alone at') >= 0,
   'nomeando o episodio que a torna bimodal (' + topEleicao.label + ')');
ok(proseHtml.indexOf('above all ' + crises.length + ' crises') >= 0,
   'e dizendo que ele supera as crises, com a contagem derivada');

// As duas frases que DESCREVIAM a tabela em vez de a lerem. A da coluna de
// dolar EM nasceu com quatro eleicoes com leitura ("as duas que subiram, as
// duas quietas") e sobreviveu a chegada de tres eleicoes e de duas celulas
// vazias; a do pos-eleicao dizia "algumas" onde o dado conta. As duas passaram
// a ser derivadas, e estas assercoes refazem as contas por fora.
const elecConc = eleicoes.filter(e => e.concurrent && e.concurrent.dxy_em !== undefined);
const elecSemConc = eleicoes.filter(e => !(e.concurrent && e.concurrent.dxy_em !== undefined));
const dolarNegativo = elecConc.filter(e => e.concurrent.dxy_em < 0);
const maisCalmasCds = elecConc.slice().sort((a, b) => a.peak_x - b.peak_x).slice(0, dolarNegativo.length);
ok(dolarNegativo.length > 0 && dolarNegativo.every(e => maisCalmasCds.indexOf(e) >= 0),
   'as eleicoes com perna de dolar NEGATIVA sao exatamente as mais calmas em CDS -- e a leitura da coluna',
   dolarNegativo.map(e => e.label).join(', '));
ok(proseHtml.indexOf('of the ' + elecConc.length + ' elections the index reaches') >= 0,
   'e a prosa conta quantas eleicoes o indice alcanca (' + elecConc.length + '), nao um numero de outra epoca');
ok(elecSemConc.length === 0
   || proseHtml.indexOf('the ' + elecSemConc.length + ' earliest elections') >= 0,
   'e explica a celula vazia em vez de deixar um travessao sem motivo');
const elecPost = eleicoes.filter(e => e.post);
const elecAbriu = elecPost.filter(e => e.post.bps > 0);
ok(proseHtml.indexOf('wider after ' + elecAbriu.length + '</b> of the ' + elecPost.length) >= 0,
   'e o pos-eleicao sai contado (' + elecAbriu.length + ' de ' + elecPost.length + '), nao como "algumas"');

// ---------------------------------------------------------------------------
console.log('\n' + '='.repeat(70));
console.log(`${oks} ok, ${falhas} falharam`);
process.exit(falhas ? 1 : 0);
