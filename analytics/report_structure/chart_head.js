/* ── Cabeçalho de cada gráfico ────────────────────────────────────────────────
   Três linhas no topo do card, acima do plot: título, subtítulo e "Fonte · período".

   A regra dura: SÓ o título e a fonte são texto fixo; o subtítulo e o período são
   recalculados a cada render, a partir das séries que o gráfico ACABOU de plotar.
   Um subtítulo escrito no HTML passa a mentir no primeiro clique de seletor — e é o
   print tirado depois desse clique que vai circular fora da página.

   Onde a métrica é um seletor, o TÍTULO também é derivado (passe `titulo` em opts):
   a regra de fundo é "nenhum texto que um clique possa contradizer", não "o título
   é sagrado". O que fica fixo é só o que não depende de seletor nenhum — a fonte.

   O relatório declara o seu próprio `CHART_META = {divId: {title, source}}`; este
   arquivo não o declara, para não sobrescrevê-lo qualquer que seja a ordem em que os
   dois são inlinados. */

var CH_CARD_SEL = '.chart-card';   // o relatório sobrescreve se usar outro nome

function _chMeta(divId) {
  return (typeof CHART_META !== 'undefined' && CHART_META[divId]) || {};
}

var _CH_MESES = ['jan', 'fev', 'mar', 'abr', 'mai', 'jun',
                 'jul', 'ago', 'set', 'out', 'nov', 'dez'];
/* freq: 'mes' (default) | 'tri' | 'ano' | 'dia'. Um eixo trimestral rotulado em mês
   diz "jan/2028" para o que a fonte chama 2028T1 — dois nomes para o mesmo ponto. */
function fmtPeriodo(iso, freq) {
  var s = String(iso);
  var p = s.split('-');
  var y = p[0], m = parseInt(p[1], 10);
  if (freq === 'ano' || !m) return y;
  if (freq === 'tri') return y + 'T' + (Math.floor((m - 1) / 3) + 1);
  if (freq === 'dia') return s.slice(0, 10).split('-').reverse().join('/');
  return _CH_MESES[m - 1] + '/' + y;
}

/* Extensão REAL das séries plotadas — nunca uma constante do dataset inteiro, nem o
   range atual do eixo (que carrega o padding do Plotly). Numa visão de variação anual
   o gráfico começa legitimamente um ano depois, e tem que dizer isso.
   Num heatmap o `y` são os RÓTULOS das linhas, não valores: olhe `z` antes de `y`, ou
   a varredura reporta as N primeiras colunas como a série inteira (N = nº de linhas). */
function _chTraceXRange(traces) {
  var lo = null, hi = null;
  (traces || []).forEach(function(t) {
    if (!t || !t.x) return;
    var z = (t.type === 'heatmap') ? (t.z || null) : null;
    if (!z && !t.y) return;
    for (var i = 0; i < t.x.length; i++) {
      var tem = false;
      if (z) {
        for (var r = 0; r < z.length; r++) { if (z[r] && z[r][i] != null) { tem = true; break; } }
      } else {
        tem = (t.y[i] != null && !(typeof t.y[i] === 'number' && isNaN(t.y[i])));
      }
      if (!tem) continue;
      var v = t.x[i];
      if (v == null) continue;
      if (lo == null || v < lo) lo = v;
      if (hi == null || v > hi) hi = v;
    }
  });
  return {lo: lo, hi: hi};
}

/* A moldura é construída uma vez por card e guardada nele; os renders seguintes só
   reescrevem texto. O cabeçalho entra ANTES do div do gráfico — a régua de tempo, que
   cada relatório monta por conta própria, continua indo depois. */
function _ensureChartFrame(divId, compact) {
  var el = document.getElementById(divId);
  if (!el) return null;
  var card = (el.closest ? el.closest(CH_CARD_SEL) : null) || el.parentNode;
  if (!card) return null;
  if (!card._chFrame) {
    // Um card cujo markup JA traz o cabecalho (porque aquele grafico precisa de algo a
    // mais na linha do titulo, um botao de definicao por exemplo) e reaproveitado em vez
    // de ganhar um segundo: dois cabecalhos no mesmo card e o defeito que isso evita.
    var pronto = (card.children || []).filter(function(c) {
      return c.className && String(c.className).indexOf('chart-head') === 0;
    })[0];
    if (pronto) {
      var pega = function(cls) {
        return (pronto.children || []).filter(function(c) { return c.className === cls; })[0];
      };
      card._chFrame = {head: pronto, title: pega('chart-title'),
                       sub: pega('chart-sub'), src: pega('chart-src')};
      return card._chFrame;
    }
    var head = document.createElement('div');
    head.className = 'chart-head' + (compact ? ' compact' : '');
    var h = document.createElement('div'); h.className = 'chart-title';
    var sub = document.createElement('div'); sub.className = 'chart-sub';
    var src = document.createElement('div'); src.className = 'chart-src';
    head.appendChild(h); head.appendChild(sub); head.appendChild(src);
    card.insertBefore(head, el);
    card._chFrame = {head: head, title: h, sub: sub, src: src};
  }
  return card._chFrame;
}

/* describeChart(divId, traces, bits, unit, opts)
     traces : as séries EFETIVAMENTE plotadas (objetos Plotly, com .name/.x/.y)
     bits   : estado dos seletores já como rótulo ('Acum. 12m', '% do PIB', ...)
     unit   : a MESMA string do título do eixo Y — para as duas não divergirem
     opts   : {freq, titulo, fonte, compact, fmt, periodo}

   A poda é a parte que dá trabalho: o mesmo fato chega por três caminhos — o rótulo do
   seletor, o nome da série e o título do eixo — e imprimir os três vira ruído. Duas
   regras resolvem: pedaço já contido na unidade sai fora, e o nome da série some quando
   ele é o próprio título do gráfico. Com mais de três séries o subtítulo diz a CONTAGEM,
   porque a legenda do gráfico já nomeia cada uma e o print carrega a legenda junto. */
function describeChart(divId, traces, bits, unit, opts) {
  opts = opts || {};
  var frame = _ensureChartFrame(divId, opts.compact);
  if (!frame) return;
  var meta = _chMeta(divId);
  var titulo = (opts.titulo != null) ? opts.titulo : (meta.title || '');
  var fonte = (opts.fonte != null) ? opts.fonte : (meta.source || '');
  if (frame.title) frame.title.textContent = titulo;

  var nomes = [];
  (traces || []).forEach(function(t) {
    if (t && t.name && t.showlegend !== false && nomes.indexOf(t.name) < 0) nomes.push(t.name);
  });
  var parts = [];
  if (nomes.length === 1) { if (titulo.indexOf(nomes[0]) !== 0) parts.push(nomes[0]); }
  else if (nomes.length > 1 && nomes.length <= 3) { parts.push(nomes.join(', ')); }
  else if (nomes.length > 3) { parts.push(nomes.length + ' séries (ver legenda)'); }
  (bits || []).forEach(function(b) { if (b) parts.push(b); });
  var lowU = String(unit || '').toLowerCase();
  parts = parts.filter(function(p) {
    return !lowU || lowU.indexOf(String(p).toLowerCase()) < 0;
  });
  if (unit) parts.push(unit);
  if (frame.sub) frame.sub.textContent = parts.join(' · ');

  // Num grafico cujo X NAO e tempo (dispersao de dois valores), derivar a janela das
  // abscissas daria "0,12 a 8,4" na linha da fonte -- uma faixa de valores lida como se
  // fosse periodo. Nesses o chamador passa `periodo` pronto: e uma data so, a leitura em
  // que os pontos foram tirados, e ela nao esta no eixo nenhum.
  var periodo;
  if (opts.periodo != null) {
    periodo = opts.periodo;
  } else {
    var r = _chTraceXRange(traces);
    var f = opts.fmt || fmtPeriodo;
    periodo = (r.lo != null && r.hi != null) ? (f(r.lo, opts.freq) + ' a ' + f(r.hi, opts.freq)) : '';
  }
  if (frame.src) {
    frame.src.textContent = (fonte ? 'Fonte: ' + fonte : '') +
                            (periodo ? ((fonte ? ' · ' : '') + periodo) : '');
  }
}
