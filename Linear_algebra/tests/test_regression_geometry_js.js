/*
 * Harness do dashboard Linear_algebra/regression_geometry.html.
 *
 * Executa o JS DE VERDADE do arquivo entregue -- as fatias LINALG e GEO sao
 * extraidas do HTML e avaliadas -- em vez de uma copia. Uma copia diverge em
 * silencio na primeira edicao, que e o modo de falha que .claude/rules/
 * lis-dashboards.md documenta duas vezes.
 *
 *   node Linear_algebra/tests/test_regression_geometry_js.js
 */
'use strict';
const fs = require('fs');
const path = require('path');
const vm = require('vm');

/* O caminho pode ser passado por argumento para que o runner de mutantes
   rode o MESMO teste contra uma copia modificada do HTML. */
const HTML = process.argv[2] || path.join(__dirname, '..', 'regression_geometry.html');
const src = fs.readFileSync(HTML, 'utf8');

let pass = 0, fail = 0;
function ok(cond, msg) { if (cond) { pass++; } else { fail++; console.log('  FALHOU: ' + msg); } }
function near(a, b, tol, msg) { ok(Math.abs(a - b) <= tol, msg + ' (obtido ' + a + ', esperado ' + b + ')'); }
function sec(t) { console.log('\n' + t); }

/* O HTML entregue pode estar em CRLF; um terminador de fatia com \n literal
   devolveria string vazia SEM erro, e o teste voltaria a medir nada. */
function slice(tag) {
  const re = new RegExp('/\\* =+ ' + tag + '_START =+ \\*/([\\s\\S]*?)/\\* =+ ' + tag + '_END =+ \\*/');
  const m = src.match(re);
  if (!m) { console.log('ERRO: fatia ' + tag + ' nao encontrada no HTML'); process.exit(1); }
  if (m[1].length < 400) { console.log('ERRO: fatia ' + tag + ' curta demais (' + m[1].length + ' chars)'); process.exit(1); }
  return m[1];
}

const ctx = { Math: Math, console: console, isFinite: isFinite };
vm.createContext(ctx);
vm.runInContext(slice('LINALG'), ctx);
vm.runInContext(slice('GEO'), ctx);
const { dot, norm, sub, scale, inv, det, angleDeg, orthoBasis, fitModel, planeQuad, rightAngle } = ctx;

/* ---------------------------------------------------------------- 1. inversa */
sec('1. inv / det');
{
  const A = [[4, 7], [2, 6]];
  const I = inv(A);
  near(I[0][0], 0.6, 1e-12, 'inv 2x2 [0][0]');
  near(I[0][1], -0.7, 1e-12, 'inv 2x2 [0][1]');
  near(det(A), 10, 1e-12, 'det 2x2');
  near(det([[6, 1, 1], [4, -2, 5], [2, 8, 7]]), -306, 1e-10, 'det 3x3');
  ok(inv([[1, 2], [2, 4]]) === null, 'matriz singular devolve null');
  ok(inv([[0, 0], [0, 0]]) === null, 'matriz nula devolve null');

  /* A tolerancia tem de ser RELATIVA: uma absoluta reprova uma matriz bem
     condicionada so por ela estar em unidades pequenas. A escala do exemplo
     tem de ficar ABAIXO de qualquer tolerancia absoluta plausivel, senao o
     mutante que troca a relativa por 1e-8 passa (foi o que aconteceu). */
  const tiny = [[1e-10, 0], [0, 1e-10]];
  ok(inv(tiny) !== null, 'matriz minuscula porem bem condicionada NAO e singular');
  near(inv(tiny)[0][0], 1e10, 1e4, 'inversa da matriz minuscula');
  const huge = [[1e8, 2e8], [2e8, 4e8]];
  ok(inv(huge) === null, 'matriz enorme e exatamente singular continua singular');

  /* Pivoteamento parcial: com o primeiro pivo zero, uma eliminacao ingenua
     declara singular uma matriz perfeitamente invertivel. */
  const troca = inv([[0, 1], [1, 0]]);
  ok(troca !== null, 'primeiro pivo zero nao torna a matriz singular');
  if (troca) {
    near(troca[0][1], 1, 1e-12, 'inv da matriz de troca: [0][1]');
    near(troca[0][0], 0, 1e-12, 'inv da matriz de troca: [0][0]');
  }
  const p3 = inv([[0, 2, 1], [1, 0, 3], [4, 1, 0]]);
  ok(p3 !== null, 'pivo zero no meio de uma 3x3 tambem e resolvido');
  if (p3) {
    /* conferido multiplicando de volta: A * A^-1 = I */
    const A3 = [[0, 2, 1], [1, 0, 3], [4, 1, 0]];
    let pior = 0;
    for (let i = 0; i < 3; i++) for (let j = 0; j < 3; j++) {
      let v = 0; for (let k = 0; k < 3; k++) v += A3[i][k] * p3[k][j];
      pior = Math.max(pior, Math.abs(v - (i === j ? 1 : 0)));
    }
    ok(pior < 1e-12, 'A * inv(A) = I na 3x3 com pivo zero (pior desvio ' + pior + ')');
  }
}

/* ------------------------------------------------- 2. formas fechadas */
sec('2. formas fechadas da regressao simples');
{
  /* sem intercepto: beta = x'y / x'x */
  const y = [3, 1], x = [1, 2];
  const M = fitModel(y, [x], ['x1']);
  near(M.beta[0], dot(x, y) / dot(x, x), 1e-12, 'beta sem intercepto = x\'y/x\'x');
  near(M.beta[0], 1, 1e-12, 'beta conferido a mao: xty/xtx = 5/5');
  near(M.yhat[0], 1, 1e-12, 'yhat[0] conferido a mao');
  near(M.yhat[1], 2, 1e-12, 'yhat[1] conferido a mao');
  near(M.resid[0], 2, 1e-12, 'residuo[0] conferido a mao');
  near(M.resid[1], -1, 1e-12, 'residuo[1] conferido a mao');
  near(M.cos2, 0.5, 1e-12, 'cos2 conferido a mao = 0,5');
  near(M.angle, 45, 1e-9, 'angulo conferido a mao = 45 graus');

  /* com intercepto: beta1 = cov/var, beta0 = ybar - beta1*xbar */
  const yy = [1, 3, 2], xx = [1, 2, 4], n = 3;
  const mx = (1 + 2 + 4) / 3, my = (1 + 3 + 2) / 3;
  let cov = 0, vr = 0;
  for (let i = 0; i < n; i++) { cov += (xx[i] - mx) * (yy[i] - my); vr += (xx[i] - mx) * (xx[i] - mx); }
  const F = fitModel(yy, [[1, 1, 1], xx], ['1', 'x1']);
  near(F.beta[1], cov / vr, 1e-12, 'beta1 com intercepto = cov/var');
  near(F.beta[0], my - (cov / vr) * mx, 1e-12, 'beta0 com intercepto = ybar - b1*xbar');
  near(F.beta[0], 1.5, 1e-12, 'beta0 do padrao 3D conferido a mao');
  near(F.beta[1], 3 / 14, 1e-12, 'beta1 do padrao 3D conferido a mao');
  near(F.det, 14, 1e-12, 'det(XtX) do padrao 3D conferido a mao');
}

/* ------------------------------------------- 3. ortogonalidade e Pitagoras */
sec('3. ortogonalidade, Pitagoras, projetor');
{
  let seed = 7;
  const rnd = () => { seed = (seed * 1103515245 + 12345) % 2147483648; return (seed / 2147483648) * 8 - 4; };
  for (let t = 0; t < 60; t++) {
    const n = 3 + (t % 4);
    const y = Array.from({ length: n }, rnd);
    const p = 1 + (t % 3);
    const cols = [];
    if (t % 2 === 0) cols.push(Array.from({ length: n }, () => 1));
    while (cols.length < p) cols.push(Array.from({ length: n }, rnd));
    const M = fitModel(y, cols, cols.map((_, i) => 'c' + i));
    if (M.singular) continue;
    ok(M.maxOrth < 1e-9, 'caso ' + t + ': X\'e = 0');
    near(M.normY * M.normY, M.normYhat * M.normYhat + M.normE * M.normE, 1e-8, 'caso ' + t + ': Pitagoras');
    /* H simetrica, idempotente, traco = p, e Hy = yhat */
    let tr = 0, badSym = 0, badIdem = 0, badHy = 0;
    for (let i = 0; i < n; i++) {
      tr += M.H[i][i];
      let hy = 0;
      for (let k = 0; k < n; k++) {
        hy += M.H[i][k] * y[k];
        if (Math.abs(M.H[i][k] - M.H[k][i]) > 1e-9) badSym++;
        let h2 = 0;
        for (let q = 0; q < n; q++) h2 += M.H[i][q] * M.H[q][k];
        if (Math.abs(h2 - M.H[i][k]) > 1e-9) badIdem++;
      }
      if (Math.abs(hy - M.yhat[i]) > 1e-9) badHy++;
    }
    ok(badSym === 0, 'caso ' + t + ': H simetrica');
    ok(badIdem === 0, 'caso ' + t + ': H idempotente (H^2 = H)');
    ok(badHy === 0, 'caso ' + t + ': Hy = yhat');
    near(tr, M.p, 1e-8, 'caso ' + t + ': traco(H) = p');
  }
}

/* ------------------------------------------------ 4. o que o dashboard afirma */
sec('4. afirmacoes exibidas na tela');
{
  /* residuos somam zero quando ha intercepto -- e SO quando ha */
  const y = [1, 3, 2];
  const comI = fitModel(y, [[1, 1, 1], [1, 2, 4]], ['1', 'x1']);
  near(comI.resid.reduce((a, b) => a + b, 0), 0, 1e-12, 'com intercepto os residuos somam zero');
  ok(comI.hasConst === true, 'hasConst detecta a coluna de 1s');
  const semI = fitModel(y, [[1, 2, 4]], ['x1']);
  ok(Math.abs(semI.resid.reduce((a, b) => a + b, 0)) > 1e-6, 'sem intercepto os residuos NAO somam zero');
  ok(semI.hasConst === false, 'hasConst falso sem coluna constante');
  ok(semI.r2c === null, 'R2 centrado fica indefinido sem intercepto');

  /* hasConst tem de pegar uma constante que nao seja 1 -- uma coluna (5,5,5)
     gera o mesmo subespaco que (1,1,1) e o R2 centrado continua valendo. */
  const cinco = fitModel(y, [[5, 5, 5], [1, 2, 4]], ['5', 'x1']);
  ok(cinco.hasConst === true, 'hasConst pega uma coluna constante diferente de 1');
  ok(cinco.r2c !== null, 'R2 centrado definido com coluna constante = 5');
  near(cinco.r2c, comI.r2c, 1e-12, 'a constante reescalada da o mesmo R2 centrado');

  /* uma coluna de zeros NAO e constante para este fim: ela nao gera nada */
  const zeros = fitModel(y, [[0, 0, 0], [1, 2, 4]], ['0', 'x1']);
  ok(zeros.hasConst === false, 'coluna de zeros nao conta como intercepto');
  ok(zeros.singular === true, 'coluna de zeros deixa X\'X singular');

  /* R2 centrado = 1 - SQR/SQT */
  const mean = y.reduce((a, b) => a + b, 0) / 3;
  const sst = y.reduce((a, b) => a + (b - mean) * (b - mean), 0);
  near(comI.r2c, 1 - dot(comI.resid, comI.resid) / sst, 1e-12, 'R2 centrado = 1 - SQR/SQT');

  /* cos2 = ||yhat||^2 / ||y||^2, e indefinido quando y = 0 */
  near(comI.cos2, (comI.normYhat ** 2) / (comI.normY ** 2), 1e-12, 'cos2 = razao dos comprimentos ao quadrado');
  const y0 = fitModel([0, 0, 0], [[1, 1, 1], [1, 2, 4]], ['1', 'x1']);
  ok(y0.cos2 === null && y0.angle === null, 'y nulo nao inventa cos2 nem angulo');

  /* p = n: ajuste exato, df = 0, s2 indefinido */
  const sat = fitModel(y, [[1, 1, 1], [1, 2, 4], [2, 1, 1]], ['1', 'x1', 'x2']);
  ok(!sat.singular, 'p = n com colunas independentes nao e singular');
  ok(sat.normE < 1e-9, 'p = n da residuo zero');
  ok(sat.df === 0 && sat.s2 === null, 'df = 0 e s2 indefinido em p = n');
  near(sat.r2c, 1, 1e-9, 'R2 = 1 no ajuste saturado');

  /* s2 = ||e||^2/(n-p) quando ha graus de liberdade */
  near(comI.s2, dot(comI.resid, comI.resid) / (3 - 2), 1e-12, 's2 = ||e||^2/(n-p)');
}

/* ----------------------------------------------- 5. as dicas "o que testar" */
sec('5. as dicas do card "o que testar" sao verdadeiras');
{
  const y = [3, 1], x = [1, 2];
  const A = fitModel(y, [x], ['x1']);
  const B = fitModel(y, [scale(x, 10)], ['x1']);
  near(B.beta[0], A.beta[0] / 10, 1e-12, 'reescalar x por 10 divide beta por 10');
  near(norm(sub(B.yhat, A.yhat)), 0, 1e-12, 'reescalar x nao move yhat');
  near(B.cos2, A.cos2, 1e-12, 'reescalar x nao muda o R2');

  /* ortogonais: tirar x2 nao mexe em beta1. Fora da ortogonalidade, mexe. */
  const yy = [1, 3, 2], o1 = [1, 1, 0], o2 = [1, -1, 0];
  near(dot(o1, o2), 0, 1e-12, 'as colunas do preset "ortogonais" sao de fato ortogonais');
  const dois = fitModel(yy, [o1, o2], ['x1', 'x2']);
  const so1 = fitModel(yy, [o1], ['x1']);
  near(dois.beta[0], so1.beta[0], 1e-12, 'com colunas ortogonais, omitir x2 nao muda beta1');
  const c1 = [1, 2, 4], c2 = [2, 1, 1];
  const amb = fitModel(yy, [c1, c2], ['x1', 'x2']);
  const um = fitModel(yy, [c1], ['x1']);
  ok(Math.abs(amb.beta[0] - um.beta[0]) > 1e-3, 'fora da ortogonalidade, omitir x2 MUDA beta1');

  /* o preset "ortogonais" projeta no plano z=0: yhat = (1,3,0), e = (0,0,2) */
  near(dois.yhat[2], 0, 1e-12, 'projecao no plano z=0 zera a terceira coordenada');
  near(dois.resid[2], 2, 1e-12, 'o residuo do preset ortogonal e (0,0,2)');
}

/* ----------------------------------------------------- 6. colinearidade */
sec('6. colinearidade: yhat estavel, beta instavel');
{
  const x1 = [1, 2, 4], x2 = [1.01, 2.01, 4.03];   // mesmo preset "quase colineares" do HTML
  const y = [1, 3, 2], yp = [1.05, 3, 2];
  const A = fitModel(y, [x1, x2], ['x1', 'x2']);
  const B = fitModel(yp, [x1, x2], ['x1', 'x2']);
  ok(!A.singular, 'quase colineares ainda tem inversa (nao e exatamente singular)');
  const dBeta = norm(sub(B.beta, A.beta));
  const dYhat = norm(sub(B.yhat, A.yhat));
  ok(dBeta > 100 * dYhat, 'beta se move muito mais que yhat sob a mesma perturbacao ' +
    '(dBeta=' + dBeta.toFixed(3) + ' vs dYhat=' + dYhat.toFixed(3) + ')');
  const ang = Math.min(angleDeg(x1, x2), 180 - angleDeg(x1, x2));
  ok(ang < 0.5, 'o angulo entre as colunas quase colineares e menor que meio grau (' + ang.toFixed(3) + ')');
  ok(Math.abs(A.det) < 0.01, 'det(XtX) proximo de zero no caso colinear (' + A.det.toFixed(5) + ')');

  /* o contraste que o card promete: com colunas bem separadas, beta e estavel */
  const W1 = fitModel(y, [[1, 2, 4], [2, 1, 1]], ['x1', 'x2']);
  const W2 = fitModel(yp, [[1, 2, 4], [2, 1, 1]], ['x1', 'x2']);
  const dBetaW = norm(sub(W2.beta, W1.beta));
  ok(dBetaW < dBeta / 50, 'com colunas bem separadas beta se move muito menos (' + dBetaW.toFixed(4) + ')');

  /* exatamente colineares -> singular, e o dashboard tem de dizer o posto */
  const S = fitModel(y, [x1, scale(x1, 3)], ['x1', 'x2']);
  ok(S.singular === true, 'colunas exatamente paralelas sao detectadas');
  ok(S.rank === 1, 'posto 1 para duas colunas paralelas');
  ok(S.beta === undefined, 'nao ha beta quando e singular');
}

/* -------------------------------------------------------- 7. posto / base */
sec('7. orthoBasis e o posto exibido');
{
  ok(orthoBasis([[1, 0, 0], [0, 1, 0]]).length === 2, 'posto 2 de duas colunas independentes');
  ok(orthoBasis([[1, 2, 4], [3, 6, 12]]).length === 1, 'posto 1 de duas colunas paralelas');
  ok(orthoBasis([[0, 0, 0]]).length === 0, 'posto 0 da coluna nula');
  ok(orthoBasis([[1, 1, 1], [1, 2, 4], [2, 1, 1]]).length === 3, 'posto 3 no caso saturado');
  const B = orthoBasis([[1, 2, 4], [2, 1, 1]]);
  near(norm(B[0]), 1, 1e-12, 'base ortonormal: norma 1');
  near(dot(B[0], B[1]), 0, 1e-12, 'base ortonormal: ortogonal');
  /* colunas grandes nao podem virar "posto deficiente" por escala */
  ok(orthoBasis([[1e6, 2e6, 4e6], [2e6, 1e6, 1e6]]).length === 2, 'posto correto com colunas enormes');
  ok(orthoBasis([[1e-6, 2e-6, 4e-6], [2e-6, 1e-6, 1e-6]]).length === 2, 'posto correto com colunas minusculas');
}

/* ----------------------------------------------------------- 8. geometria */
sec('8. helpers de desenho');
{
  const B = orthoBasis([[1, 0, 0], [0, 1, 0]]);
  const q = planeQuad(B, 2);
  ok(q.x.length === 4 && q.i.length === 2, 'planeQuad devolve 4 cantos e 2 triangulos');
  for (let i = 0; i < 4; i++) near(q.z[i], 0, 1e-12, 'canto ' + i + ' do plano fica dentro do span');

  /* a marca de angulo reto tem de ter os dois bracos iguais e perpendiculares,
     senao ela desenha um angulo que nao e o que afirma */
  const foot = [1, 1, 0], inD = [-1, 0, 0], pD = [0, 0, 1];
  const ra = rightAngle(foot, inD, pD, 0.5);
  ok(ra.length === 3, 'a marca tem 3 pontos');
  const l1 = norm(sub(ra[0], foot)), l2 = norm(sub(ra[2], foot));
  near(l1, l2, 1e-12, 'os dois bracos da marca tem o mesmo comprimento');
  near(dot(sub(ra[0], foot), sub(ra[2], foot)), 0, 1e-12, 'os dois bracos da marca sao perpendiculares');

  /* e ela tem de funcionar em 2D com o mesmo codigo */
  const ra2 = rightAngle([2, 2], [-0.7071, -0.7071], [0.7071, -0.7071], 0.3);
  ok(ra2.length === 3 && ra2[0].length === 2, 'a mesma funcao serve o caso 2D');

  near(angleDeg([1, 0], [0, 1]), 90, 1e-9, 'angleDeg de vetores ortogonais');
  /* acos perto de 1 e mal condicionado: o erro aqui e ~1e-6 grau, ruido de
     ponto flutuante e nao defeito -- a tela arredonda a uma decimal. */
  near(angleDeg([1, 1], [2, 2]), 0, 1e-3, 'angleDeg de vetores paralelos');
  ok(angleDeg([0, 0], [1, 1]) === null, 'angleDeg do vetor nulo devolve null');
}

/* --------------------------- 8b. enquadramento: o defeito visual de 2026-09-22 */
sec('8b. enquadramento das figuras');
{
  const { maxCoord, extentAlong } = ctx;
  near(maxCoord([[3, 1], [1, 2]]), 3, 1e-12, 'maxCoord = maior coordenada absoluta');
  near(maxCoord([[-9, 1]]), 9, 1e-12, 'maxCoord respeita o sinal');
  ok(maxCoord([[0, 0]]) === 1, 'maxCoord degenerado devolve 1 em vez de zero');

  /* maxCoord tem de ser MENOR que a maior norma: foi trocar um pelo outro que
     deixou os vetores ocupando um quinto da figura na primeira versao. */
  ok(maxCoord([[3, 4]]) < norm([3, 4]), 'maxCoord < norma (e por isso enquadra mais apertado)');

  /* squareWindow: o enquadramento do grafico 2D */
  const { squareWindow } = ctx;
  const pts2 = [[3, 1], [1, 2], [1, 2]];          // y, x1, yhat do caso padrao
  const W = squareWindow(pts2);
  ok(W.x[0] <= 0 && W.y[0] <= 0, 'a origem esta dentro da janela (e um espaco vetorial)');
  for (const q of pts2) {
    ok(q[0] >= W.x[0] && q[0] <= W.x[1], 'ponto dentro da janela em x');
    ok(q[1] >= W.y[0] && q[1] <= W.y[1], 'ponto dentro da janela em y');
  }
  near(W.x[1] - W.x[0], W.y[1] - W.y[0], 1e-12,
    'os dois eixos tem o MESMO vao -- sem isso a trava 1:1 distorce a folga');
  ok(W.data / W.span > 0.7, 'o dado ocupa mais de 70% do vao (' +
    (100 * W.data / W.span).toFixed(0) + '%)');

  /* centrada na caixa e nao na origem: com dado todo positivo, o limite
     inferior nao pode descer ate -max, que era o defeito */
  ok(W.x[0] > -W.x[1] + 1e-9, 'a janela nao e simetrica na origem quando o dado e todo positivo');
  const sim = squareWindow([[3, 1], [-3, 1]]);
  near(sim.x[0], -sim.x[1], 1e-12, 'com dado simetrico a janela volta a ser simetrica');

  /* degenerado: tudo na origem nao pode produzir vao zero */
  const deg = squareWindow([[0, 0]]);
  ok(deg.span > 0.5, 'janela degenerada ainda tem vao positivo (' + deg.span + ')');

  near(extentAlong([[3, 0, 0], [0, 5, 0]], [1, 0, 0]), 3, 1e-12, 'extentAlong projeta sobre a direcao dada');
  near(extentAlong([[3, 0, 0], [0, 5, 0]], [0, 1, 0]), 5, 1e-12, 'extentAlong na outra direcao');

  /* o plano tem de CONTER as projecoes de tudo o que e plotado, com folga,
     e ser retangular quando as duas direcoes tem extensoes diferentes */
  const B = orthoBasis([[1, 2, 4], [2, 1, 1]]);
  const pontos = [[1, 3, 2], [1, 2, 4], [2, 1, 1]];
  const e1 = extentAlong(pontos, B[0]) * 1.22, e2 = extentAlong(pontos, B[1]) * 1.22;
  const q = planeQuad(B, e1, e2);
  ok(Math.abs(e1 - e2) > 1e-6, 'as duas direcoes tem extensoes diferentes neste caso');
  const lado1 = Math.hypot(q.x[1] - q.x[0], q.y[1] - q.y[0], q.z[1] - q.z[0]);
  const lado2 = Math.hypot(q.x[2] - q.x[1], q.y[2] - q.y[1], q.z[2] - q.z[1]);
  ok(Math.abs(lado1 - lado2) > 1e-6, 'planeQuad com duas meias-arestas produz um retangulo, nao um quadrado');
  near(lado1, 2 * e1, 1e-9, 'lado 1 = 2 x meia-aresta 1');
  near(lado2, 2 * e2, 1e-9, 'lado 2 = 2 x meia-aresta 2');
  for (const p of pontos) {
    ok(Math.abs(dot(p, B[0])) <= e1 + 1e-9, 'ponto contido no plano ao longo de u1');
    ok(Math.abs(dot(p, B[1])) <= e2 + 1e-9, 'ponto contido no plano ao longo de u2');
  }
  /* ... e nao pode ser folgado demais: a folga e 22%, nao 300% */
  ok(e1 / extentAlong(pontos, B[0]) < 1.5 && e2 / extentAlong(pontos, B[1]) < 1.5,
    'a folga do plano fica abaixo de 50%');
  ok(planeQuad(B, 2).x.length === 4, 'planeQuad com um argumento so continua valendo (quadrado)');
}

/* ----------------------- 8c. cubeWindow: a cena 3D nao pode ser sequestrada */
sec('8c. janela cubica da cena 3D');
{
  const { cubeWindow } = ctx;
  const pontos = [[1, 3, 2], [1, 2, 4], [2, 1, 1], [1.42, 1.53, 2.63]];
  const CW = cubeWindow(pontos);
  ok(CW.ranges.length === 3, 'cubeWindow devolve tres intervalos');
  const vaos = CW.ranges.map(r => r[1] - r[0]);
  near(vaos[0], vaos[1], 1e-12, 'vao igual entre x e y (sem isso o angulo reto se deforma)');
  near(vaos[1], vaos[2], 1e-12, 'vao igual entre y e z');
  for (const q of pontos) for (let k = 0; k < 3; k++) {
    ok(q[k] >= CW.ranges[k][0] && q[k] <= CW.ranges[k][1], 'ponto dentro do cubo no eixo ' + k);
  }
  ok(CW.ranges[0][0] <= 0 && CW.ranges[1][0] <= 0 && CW.ranges[2][0] <= 0, 'a origem esta dentro do cubo');
  ok(CW.data / CW.span > 0.7, 'o dado ocupa mais de 70% da aresta (' + (100 * CW.data / CW.span).toFixed(0) + '%)');
  ok(cubeWindow([[0, 0, 0]]).span > 0.5, 'cubo degenerado ainda tem aresta positiva');

  /* O caso que motivou a janela explicita: as parcelas do preset colinear sao
     ~300x o yhat. A janela tem de ignora-las -- e o teste tem de MEDIR isso,
     senao um retorno ao autorange volta sem sintoma. */
  const P3 = vm.runInNewContext('(' + /var P3=(\{[\s\S]*?\});/.exec(src)[1] + ')');
  const c = P3.colin;
  const M = fitModel(c.y, [c.a, c.b], ['x1', 'x2']);
  const parcelas = [scale(c.a, M.beta[0]), scale(c.b, M.beta[1])];
  const maiorParcela = Math.max(...parcelas.map(norm));
  ok(maiorParcela > 100 * M.normYhat / 3, 'as parcelas do caso colinear sao ordens de grandeza acima de yhat (' +
    maiorParcela.toFixed(0) + ' vs ' + M.normYhat.toFixed(2) + ')');
  const semParcelas = cubeWindow([c.y, c.a, c.b, M.yhat]);
  const comParcelas = cubeWindow([c.y, c.a, c.b, M.yhat].concat(parcelas));
  ok(comParcelas.span > 50 * semParcelas.span,
    'incluir as parcelas explodiria a janela (' + comParcelas.span.toFixed(0) + ' contra ' + semParcelas.span.toFixed(2) + ')');
  ok(/cubeWindow\(all\)/.test(src) && !/cubeWindow\([^)]*parcela/.test(src),
    'o render 3D enquadra pelos vetores, nao pelas parcelas da decomposicao');
  ok(/maiorParcela>2\*M\.normYhat/.test(src),
    'e a leitura avisa, com o numero medido, quando as parcelas saem do cubo');
}

/* -------------------------------------------- 9. guardas sobre o HTML */
sec('9. guardas estaticos do HTML entregue');
{
  /* HTMLCollection nao tem .filter/.map/.forEach -- o defeito de chart_head.js.
     Os produtores de colecao viva tem de passar por slice.call/Array.from. */
  const limpo = src.replace(/Array\.prototype\.slice\.call\([^;]*?\)/g, 'SAFE')
                   .replace(/Array\.from\([^;]*?\)/g, 'SAFE');
  const vivos = limpo.match(/(\.children|querySelectorAll\([^)]*\)|getElementsBy\w+\([^)]*\))\s*\.\s*(filter|map|reduce|some|every|sort|forEach)/g) || [];
  const proibidos = vivos.filter(m => !/querySelectorAll\([^)]*\)\s*\.\s*forEach/.test(m));
  ok(proibidos.length === 0, 'nenhum metodo de Array em colecao viva do DOM: ' + JSON.stringify(proibidos));

  /* escala 1:1 -- sem isso o angulo reto nao aparece reto, que e a figura toda */
  ok(/scaleanchor\s*=\s*'x'/.test(src), 'o grafico 2D trava a razao de aspecto (scaleanchor)');
  ok(/scaleratio\s*=\s*1/.test(src), 'a razao de aspecto 2D e 1:1');
  /* Em 3D a garantia de 1:1 e o CUBO com arestas iguais nos tres eixos: um
     aspectmode sozinho nao diz nada se o range vier de autorange sobre um
     trace gigante (as parcelas beta_j*x_j do caso colinear). */
  /* Medido em Chrome: com ranges EXPLICITOS e iguais, 'cube' e 'data' resolvem
     os mesmos vaos (5,12 nos tres eixos) -- a string do aspectmode nao carrega
     a garantia, o range explicito carrega. E o range explicito e o que impede
     o autorange de enquadrar pelas parcelas gigantes da decomposicao. */
  ok(/sceneAxis\('obs 1',CW\.ranges\[0\]\)/.test(src), 'a cena 3D recebe range explicito no eixo x');
  ok(/sceneAxis\('obs 2',CW\.ranges\[1\]\)/.test(src), 'a cena 3D recebe range explicito no eixo y');
  ok(/sceneAxis\('obs 3',CW\.ranges\[2\]\)/.test(src), 'a cena 3D recebe range explicito no eixo z');
  ok(/aspectmode:'(cube|data)'/.test(src), 'a cena 3D declara um aspectmode isotropico');

  /* interacao: a regra do repositorio pede scroll-zoom em todo grafico */
  ok(/scrollZoom:\s*true/.test(src), 'scrollZoom ligado');
  ok(/dragmode:\s*'pan'/.test(src), 'drag = pan nos graficos 2D');

  /* todo id lido por el() existe no markup (um typo produz null silencioso) */
  const ids = new Set();
  let m, reId = /\bid="([^"]+)"/g;
  while ((m = reId.exec(src))) ids.add(m[1]);
  const lidos = new Set();
  let reEl = /\bel\('([^']+)'\)/g;
  while ((m = reEl.exec(src))) lidos.add(m[1]);
  let rePlot = /Plotly\.react\('([^']+)'/g;
  while ((m = rePlot.exec(src))) lidos.add(m[1]);
  const orfaos = [...lidos].filter(i => !ids.has(i));
  ok(orfaos.length === 0, 'nenhum id referenciado sem existir no markup: ' + JSON.stringify(orfaos));

  /* a hifenizacao do texto justificado depende do lang no <html> */
  ok(/<html lang="pt-BR">/.test(src), '<html lang="pt-BR"> presente (justify + hyphens dependem dele)');
  ok(/hyphens:\s*auto/.test(src), 'hyphens:auto junto do text-align:justify');

  /* os presets citados no HTML tem de existir no objeto de presets */
  const btns2 = [...src.matchAll(/data-p="([^"]+)"/g)].map(x => x[1]);
  ok(btns2.length === 10, 'os 10 botoes de preset estao no markup (obtido ' + btns2.length + ')');
  for (const k of ['base', 'orto', 'alin', 'sat', 'sing', 'simples', 'dois', 'colin']) {
    ok(btns2.includes(k), 'botao de preset "' + k + '" presente');
  }
}

/* ------------------------------------ 10. os presets produzem o que prometem */
sec('10. cada preset produz o estado que o rotulo promete');
{
  /* Os presets sao LIDOS do HTML, nao copiados: uma copia aqui passaria a
     testar um dashboard que nao e o entregue na primeira vez que um vetor
     mudasse de lado. */
  const P2 = vm.runInNewContext('(' + /var P2=(\{[\s\S]*?\});/.exec(src)[1] + ')');
  const P3 = vm.runInNewContext('(' + /var P3=(\{[\s\S]*?\});/.exec(src)[1] + ')');
  ok(Object.keys(P2).length === 5 && Object.keys(P3).length === 5, 'os 10 presets foram lidos do HTML');
  const mk2 = p => fitModel(p.y, p.int ? [[1, 1], p.a] : [p.a], p.int ? ['1', 'x1'] : ['x1']);
  ok(mk2(P2.orto).cos2 < 0.05, 'preset "y quase perpendicular" da R2 baixo (' + mk2(P2.orto).cos2.toFixed(4) + ')');
  ok(mk2(P2.alin).cos2 > 0.99, 'preset "y quase sobre x1" da R2 alto (' + mk2(P2.alin).cos2.toFixed(4) + ')');
  ok(mk2(P2.sat).normE < 1e-9 && !mk2(P2.sat).singular, 'preset "p = n" ajusta exato e NAO e singular');
  ok(mk2(P2.sing).singular === true, 'preset "x1 = 0" e singular');
  ok(!mk2(P2.base).singular && mk2(P2.base).normE > 0.1, 'preset "ajuste tipico" tem residuo visivel');

  /* o estado inicial da pagina e o preset base: se divergirem, a dica de
     "ligue o intercepto -> ajuste exato" passa a mentir na primeira tela */
  const iniY = [+/id="i2-y0"[^>]*value="([^"]+)"/.exec(src)[1], +/id="i2-y1"[^>]*value="([^"]+)"/.exec(src)[1]];
  const iniA = [+/id="i2-a0"[^>]*value="([^"]+)"/.exec(src)[1], +/id="i2-a1"[^>]*value="([^"]+)"/.exec(src)[1]];
  ok(iniY[0] === P2.base.y[0] && iniY[1] === P2.base.y[1], 'os inputs iniciais 2D batem com o preset base (y)');
  ok(iniA[0] === P2.base.a[0] && iniA[1] === P2.base.a[1], 'os inputs iniciais 2D batem com o preset base (x1)');
  const comInt = fitModel(iniY, [[1, 1], iniA], ['1', 'x1']);
  ok(!comInt.singular && comInt.normE < 1e-9,
    'ligar o intercepto no estado INICIAL da ajuste exato, como a dica promete');

  const mk3 = p => {
    const cols = [], nm = [];
    if (p.int) { cols.push([1, 1, 1]); nm.push('1'); }
    cols.push(p.a); nm.push('x₁');
    if (p.x2) { cols.push(p.b); nm.push('x₂'); }
    return fitModel(p.y, cols, nm);
  };
  ok(mk3(P3.simples).rank === 2 && mk3(P3.simples).normE > 0.1, 'preset "simples" projeta num plano e sobra residuo');
  ok(mk3(P3.dois).rank === 2 && mk3(P3.dois).normE > 0.01, 'preset "dois regressores" tambem sobra residuo');
  ok(mk3(P3.colin).rank === 2 && !mk3(P3.colin).singular, 'preset "quase colineares" nao e singular');
  ok(Math.max(...mk3(P3.colin).beta.map(Math.abs)) > 50, 'no preset colinear os coeficientes sao grandes (' +
    mk3(P3.colin).beta.map(b => b.toFixed(2)).join(', ') + ')');
  ok(Math.max(...mk3(P3.dois).beta.map(Math.abs)) < 5, 'no preset bem condicionado os coeficientes sao pequenos');
  ok(mk3(P3.orto).rank === 2, 'preset "ortogonais" gera um plano');
  ok(mk3(P3.sat).rank === 3 && mk3(P3.sat).normE < 1e-9, 'preset "p = n" satura o espaco e zera o residuo');

  /* mesmo guarda do estado inicial, do lado 3D */
  ok(P3.colin.b.join(',') === '1.01,2.01,4.03',
    'o preset colinear do HTML e o mesmo vetor contra o qual os limiares da secao 6 foram calibrados');

  const i3y = ['i3-y0', 'i3-y1', 'i3-y2'].map(id => +new RegExp('id="' + id + '"[^>]*value="([^"]+)"').exec(src)[1]);
  const i3a = ['i3-a0', 'i3-a1', 'i3-a2'].map(id => +new RegExp('id="' + id + '"[^>]*value="([^"]+)"').exec(src)[1]);
  ok(JSON.stringify(i3y) === JSON.stringify(P3.simples.y), 'os inputs iniciais 3D batem com o preset simples (y)');
  ok(JSON.stringify(i3a) === JSON.stringify(P3.simples.a), 'os inputs iniciais 3D batem com o preset simples (x1)');
  ok(/id="k3-int"[^>]*checked/.test(src), 'o intercepto ja vem ligado na aba 3D, como o preset simples pressupoe');
}

/* ------------------------------- 11. a caixa de decomposicao */
sec('11. a caixa "mostrar decomposicao" so vale com mais de uma coluna');
{
  ok(/function syncDecomp\(/.test(src), 'syncDecomp existe');
  ok(/chk\.disabled = !podeDecompor/.test(src), 'a caixa e desabilitada em vez de sumir');
  ok(/chk\.parentNode\.title/.test(src), 'o motivo vai para o title');
  ok(/chk\.checked=false; st\.dec=false;/.test(src),
    'ao invalidar, o estado cai de volta explicitamente (marcada-e-inerte e pior que cinza)');
  ok(/label\.chk\.off\s*\{/.test(src), 'existe estilo para a caixa desabilitada');
  ok(/syncDecomp\(el\('k2-dec'\)/.test(src) && /syncDecomp\(el\('k3-dec'\)/.test(src),
    'as duas abas chamam syncDecomp');
  /* Contar ocorrencias e fragil -- quebrou ao nascer a segunda, na leitura. O
     invariante e que TODO uso do flag esteja guardado por p > 1, o que
     continua valendo quando um terceiro uso aparecer. */
  for (const flag of ['S2', 'S3']) {
    const usos = src.match(new RegExp(flag + '\\.dec\\s*&&[^)\\n]*', 'g')) || [];
    ok(usos.length >= 1, 'ha pelo menos um uso de ' + flag + '.dec');
    ok(usos.every(u => /M\.p>1/.test(u)), 'todo uso de ' + flag + '.dec e guardado por p > 1: ' + JSON.stringify(usos));
    ok(!new RegExp('[(\\s]' + flag + '\\.dec\\s*\\)').test(src), 'nao ha uso de ' + flag + '.dec sem guarda');
  }
}

/* --------------- 12. as duas setas do caso padrao sao distinguiveis */
sec('12. no estado inicial x1 e yhat nao se escondem um no outro');
{
  /* Com um regressor so, x1 e yhat sao colineares por definicao -- o que se
     pode exigir e que tenham COMPRIMENTOS diferentes, senao a seta dourada
     fica exatamente debaixo da verde e o rotulo dela desaparece. */
  const P2 = vm.runInNewContext('(' + /var P2=(\{[\s\S]*?\});/.exec(src)[1] + ')');
  const M = fitModel(P2.base.y, [P2.base.a], ['x1']);
  ok(Math.abs(M.beta[0] - 1) > 0.2, 'beta do preset padrao esta longe de 1 (' + M.beta[0].toFixed(3) + ')');
  const razao = M.normYhat / norm(P2.base.a);
  ok(Math.abs(razao - 1) > 0.2, 'as pontas de x1 e yhat ficam separadas (razao ' + razao.toFixed(2) + ')');
  ok(M.normE > 0.3 * M.normY, 'e o residuo continua grande o bastante para ser visto');
}

console.log('\n' + pass + ' asserções passaram, ' + fail + ' falharam.');
process.exit(fail ? 1 : 0);
