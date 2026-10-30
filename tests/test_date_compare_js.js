// Testa analytics/report_structure/date_compare.js (a comparação por data compartilhada) e
// varre os relatórios atrás do padrão que ela substituiu.
//
// Roda com:
//     node tests/test_date_compare_js.js
//
// Por que existe (2026-10-30): o usuário pediu que a comparação "1 semana antes" virasse
// comparação por DATA "em todos os gráficos com esse padrão". O levantamento achou quatro
// gráficos em dois relatórios; §2 mantém isso verdadeiro sem depender de varredura manual --
// é a lição da regra do cabeçalho de gráfico, cuja lista de quem faltava foi escrita de
// memória e errou duas vezes (.claude/rules/lis-dashboards.md).

const fs = require('fs');
const path = require('path');

const RAIZ = path.join(__dirname, '..');
let falhas = 0;
function ok(cond, nome, detalhe) {
  if (cond) console.log('  ok   ' + nome);
  else { falhas++; console.log('  FALHA ' + nome + (detalhe ? '  -- ' + detalhe : '')); }
}

// ── DOM mínimo: o que setupDateCompare usa ────────────────────────────────────
function El(tag) {
  this.tag = tag; this.children = []; this._l = {}; this.value = ''; this.disabled = false;
  this.className = ''; this.textContent = ''; this.title = ''; this._html = '';
  const self = this;
  this.classList = { add(c) { self.className = (self.className + ' ' + c).trim(); } };
}
El.prototype.appendChild = function (c) { this.children.push(c); return c; };
El.prototype.addEventListener = function (k, f) { (this._l[k] = this._l[k] || []).push(f); };
El.prototype.fire = function (k) { (this._l[k] || []).forEach((f) => f({})); };
Object.defineProperty(El.prototype, 'innerHTML', {
  get() { return this._html; },
  set(v) { this._html = v; if (v === '') this.children = []; },
});
const els = {};
global.document = {
  getElementById: (id) => els[id] || (els[id] = new El('div')),
  createElement: (t) => new El(t),
};

const SRC = fs.readFileSync(path.join(RAIZ, 'analytics', 'report_structure', 'date_compare.js'), 'utf8');
new Function(SRC + ';global.__DC = {dcNaData, dcVizinha, dcPadrao, dcDataBR, setupDateCompare};')();
const DC = global.__DC;

console.log('\n1. date_compare.js');
const L = ['2026-10-19', '2026-10-20', '2026-10-21', '2026-10-23', '2026-10-26'];
ok(DC.dcNaData(L, '2026-10-22') === 2 && DC.dcNaData(L, '2026-10-25') === 3 && DC.dcNaData(L, '2026-10-26') === 4,
   'encaixa na data disponivel mais recente ate a pedida');
ok(DC.dcNaData(L, '2020-01-01') === 0 && DC.dcNaData(L, '2030-01-01') === 4, 'antes do comeco, a primeira; depois do fim, a ultima');
ok(DC.dcNaData([], '2026-10-22') === -1 && DC.dcNaData(L, null) === -1, 'sem datas ou sem data, -1');
ok(DC.dcVizinha(L, '2026-10-23', -1) === '2026-10-21' && DC.dcVizinha(L, '2026-10-24', 1) === '2026-10-26' &&
   DC.dcVizinha(L, '2026-10-26', 1) === null && DC.dcVizinha(L, '2026-10-19', -1) === null,
   'vizinha: uma data DISPONIVEL de cada lado, a partir da usada, e null nas pontas');
ok(DC.dcPadrao(L) === '2026-10-23' && DC.dcPadrao(['2026-10-26']) === null, 'default: a data anterior a mais recente');

let mudou = [];
const box = document.getElementById('cmp');
const c = DC.setupDateCompare('cmp', {
  datas: () => L, valor: '2026-10-23', nome: 'a curva', semDado: 'pregão', notaId: 'nota',
  onChange: (d) => mudou.push(d),
});
const b = (t) => box.children.find((x) => x.tag === 'button' && x.textContent === t);
const inp = box.children.find((x) => x.tag === 'input');
ok(box.children.length === 4 && inp.type === 'date' && inp.value === '2026-10-23' &&
   inp.min === L[0] && inp.max === L[L.length - 1], 'monta ‹ data › ×, com a data e os limites da lista');
ok(mudou.length === 0, 'montar nao dispara onChange');
b('‹').fire('click');
ok(c.get() === '2026-10-21' && mudou.pop() === '2026-10-21', '"‹" recua uma data disponivel e avisa');
inp.value = '2026-10-25'; inp.fire('change');
ok(c.get() === '2026-10-23' && inp.value === '2026-10-23', 'data sem pregao encaixa na anterior, e a caixa mostra a usada');
ok(els.nota.innerHTML === 'Sem pregão em 25/10/2026: a curva comparada é a de 23/10/2026.', 'a nota diz a troca', els.nota.innerHTML);
b('›').fire('click');
ok(c.get() === '2026-10-26' && b('›').disabled && els.nota.innerHTML === '', '"›" ate a ultima, desligado ali, e a nota some');
b('×').fire('click');
ok(c.get() === null && mudou.pop() === null && inp.value === '' && b('×').disabled && b('›').disabled,
   '"×" tira a comparacao');
b('‹').fire('click');
ok(c.get() === '2026-10-23', '"‹" sem comparacao volta ao default');

const box2 = document.getElementById('cmp2');
const c2 = DC.setupDateCompare('cmp2', {datas: () => L, valor: null, nome: 'a pesquisa', vazio: false, onChange: () => {}});
ok(!box2.children.some((x) => x.textContent === '×') && c2.get() === L[L.length - 1],
   'vazio:false: sem "×", e sem data cai na mais recente');
const inp2 = box2.children.find((x) => x.tag === 'input');
inp2.value = ''; inp2.fire('change');
ok(c2.get() === L[L.length - 1] && inp2.value === L[L.length - 1], 'vazio:false: apagar a caixa nao tira a comparacao');

console.log('\n2. Varredura: nenhum relatorio compara por defasagem relativa');
// O padrao substituido tinha duas assinaturas: o rotulo de pill montado com " antes"
// (ejSemanas(n) + ' antes') e a lista de defasagens como pill ("1 sem", "4 semanas").
function relatorios(dir) {
  let out = [];
  for (const e of fs.readdirSync(dir, { withFileTypes: true })) {
    const p = path.join(dir, e.name);
    if (e.isDirectory()) out = out.concat(relatorios(p));
    else if (e.name === 'report.html') out.push(p);
  }
  return out;
}
const PADROES = [
  // O espaco antes da palavra e o que separa "+ ' antes'" (sufixo de rotulo) de 'ago' (agosto)
  // e de legendgroup: 'antes'. "12 meses" fica de fora: na Focus e horizonte, nao defasagem.
  [/['"]\s+(antes|atrás|ago)\s*['"]/, 'rotulo de pill terminado em " antes"/" atras"/" ago"'],
  [/label:\s*['"]\d+\s*(sem|semanas?|weeks?)['"]/, 'pill de defasagem ("4 sem", "12 semanas")'],
  [/semanas:\s*\d+\s*,\s*label:/, 'lista de fotografias por semanas atras'],
];
const achados = [];
for (const f of relatorios(path.join(RAIZ, 'analytics'))) {
  const txt = fs.readFileSync(f, 'utf8');
  txt.split(/\r?\n/).forEach((linha, k) => {
    PADROES.forEach(([re, nome]) => {
      if (re.test(linha)) achados.push(path.relative(RAIZ, f) + ':' + (k + 1) + ' -- ' + nome);
    });
  });
}
ok(achados.length === 0, 'nenhuma comparacao por "N semanas antes" nos relatorios', achados.join('\n        '));
// E quem compara usa o compartilhado.
['brasil/monetary_policy', 'brasil/expectations'].forEach((r) => {
  const txt = fs.readFileSync(path.join(RAIZ, 'analytics', r, 'report.html'), 'utf8');
  ok(txt.indexOf('/*DATE_COMPARE_JS*/') >= 0 && txt.indexOf('/*DATE_COMPARE_CSS*/') >= 0,
     r + ': inlina date_compare.{js,css}');
});

console.log(falhas ? '\n' + falhas + ' FALHA(S)' : '\ntodos os testes passaram');
process.exit(falhas ? 1 : 0);
