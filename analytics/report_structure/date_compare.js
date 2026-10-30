// ── Comparação por data ──────────────────────────────────────────────────────
// Um gráfico que põe o que se lê hoje ao lado do que se lia antes escolhe esse "antes" por
// DATA, e uma data por fonte -- nunca por uma defasagem relativa ("1 semana antes", "4
// semanas") que vale para todas as fontes ao mesmo tempo. Pedido do usuário (2026-10-29):
// "eu quero poder comparar por data mesmo e separado entre focus e curva ... às vezes quero
// ver o que mudou de um dia para o outro".
//
// O controle: ‹ (data anterior disponível) · a data · › (seguinte) · × (sem comparação).
// A data digitada ENCAIXA na disponível mais recente até ela -- num fim de semana, feriado ou
// dia sem pesquisa, a anterior -- e a caixa passa a mostrar a que foi usada, com uma nota
// dizendo a troca. Sem isso a caixa diria uma data e o gráfico desenharia outra.
//
// `datas` é sempre um array ISO ('AAAA-MM-DD') em ordem crescente e sem repetição: as datas
// que AQUELA fonte tem. Quem chama decide o que entra nele (a grade semanal, a diária, a união
// das duas); este arquivo só escolhe dentro dele.
//
// Inlinado em cada relatório pelo marcador /*DATE_COMPARE_JS*/ (analytics/report_structure/).

// Índice da última data <= `data`; antes da primeira, 0; sem datas ou sem `data`, -1.
function dcNaData(datas, data) {
  if (!datas || !datas.length || !data) return -1;
  var lo = 0, hi = datas.length - 1, best = -1;
  while (lo <= hi) {
    var mid = (lo + hi) >> 1;
    if (datas[mid] <= data) { best = mid; lo = mid + 1; } else { hi = mid - 1; }
  }
  return best < 0 ? 0 : best;
}
// A data disponível vizinha (passo -1 ou +1) da data usada para `data`; null além das pontas.
function dcVizinha(datas, data, passo) {
  var k = dcNaData(datas, data);
  if (k < 0) return null;
  var n = k + passo;
  return (n >= 0 && n < datas.length) ? datas[n] : null;
}
// O default de "o que mudou": a data imediatamente anterior à mais recente.
function dcPadrao(datas) { return datas && datas.length >= 2 ? datas[datas.length - 2] : null; }
function dcDataBR(iso) { var p = String(iso).split('-'); return p[2] + '/' + p[1] + '/' + p[0]; }

// Monta o controle dentro de `box` (id ou elemento) e devolve {get, set}.
//   o.datas     function() -> array de datas da fonte (lido a cada clique: a fonte pode mudar)
//   o.valor     a data inicial (ISO) ou null
//   o.nome      'a curva', 'a pesquisa' -- entra nos `title` e na nota
//   o.semDado   'pregão', 'pesquisa' -- o que não existe num dia sem dado
//   o.vazio     false tira o "×": quando o gráfico só existe com uma comparação
//   o.notaId    elemento onde a nota de encaixe é escrita (opcional)
//   o.onChange  function(dataUsada) -- chamado a cada mudança, não na montagem
function setupDateCompare(box, o) {
  var el = typeof box === 'string' ? document.getElementById(box) : box;
  var estado = {v: o.valor || null};
  if (!el) return {get: function() { return estado.v; }, set: function() {}};
  el.innerHTML = '';
  el.classList.add('dc-cmp');
  var nome = o.nome || 'a série', datas = function() { return o.datas() || []; };
  var botao = function(txt, title) {
    var b = document.createElement('button');
    b.className = 'dc-btn'; b.type = 'button'; b.textContent = txt; b.title = title;
    el.appendChild(b); return b;
  };
  var ant = botao('‹', 'Comparar com ' + nome + ' da data anterior disponível');
  var inp = document.createElement('input');
  inp.type = 'date'; inp.className = 'date-select';
  inp.title = 'Data com que ' + nome + ' é comparada';
  el.appendChild(inp);
  var seg = botao('›', 'Comparar com ' + nome + ' da data seguinte disponível');
  var sem = o.vazio === false ? null : botao('×', 'Sem comparação para ' + nome);
  var nota = function(txt) {
    if (!o.notaId) return;
    var n = document.getElementById(o.notaId);
    if (!n) return;
    var partes = (n._dcNotas = n._dcNotas || {});
    partes[o.nome || ''] = txt || '';
    n.innerHTML = Object.keys(partes).map(function(k) { return partes[k]; }).filter(Boolean).join(' ');
  };
  var sync = function() {
    var L = datas();
    if (L.length) { inp.min = L[0]; inp.max = L[L.length - 1]; }
    inp.value = estado.v || '';
    ant.disabled = !L.length || (estado.v != null && dcVizinha(L, estado.v, -1) == null);
    seg.disabled = estado.v == null || dcVizinha(L, estado.v, 1) == null;
    if (sem) sem.disabled = estado.v == null;
  };
  // `pedida`: a data que o usuário digitou, quando foi ele -- é o que a nota compara.
  var set = function(data, pedida, silencioso) {
    var L = datas(), k = data ? dcNaData(L, data) : -1;
    if (k < 0 && o.vazio === false && L.length) k = L.length - 1;
    estado.v = k >= 0 ? L[k] : null;
    nota(estado.v && pedida && estado.v !== pedida
      ? 'Sem ' + (o.semDado || 'dado') + ' em ' + dcDataBR(pedida) + ': ' + nome + ' comparada é a de ' +
        dcDataBR(estado.v) + '.'
      : '');
    sync();
    if (!silencioso && o.onChange) o.onChange(estado.v);
  };
  ant.addEventListener('click', function() {
    var L = datas();
    set(estado.v == null ? dcPadrao(L) : dcVizinha(L, estado.v, -1));
  });
  seg.addEventListener('click', function() { if (estado.v != null) set(dcVizinha(datas(), estado.v, 1)); });
  if (sem) sem.addEventListener('click', function() { set(null); });
  inp.addEventListener('change', function() {
    if (!inp.value && o.vazio === false) { sync(); return; }
    set(inp.value || null, inp.value || null);
  });
  set(estado.v, null, true);
  return {get: function() { return estado.v; }, set: function(d) { set(d, null, true); }};
}
