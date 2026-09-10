// CIEDE2000 (dE2000) — distancia perceptual entre duas cores hex.
//
// Primeiro modulo COMPARTILHADO entre os harnesses de JS deste repo, e a razao
// de existir e' que a alternativa e' pior: sao ~45 linhas de codigo numerico que
// dois testes precisam calcular IDENTICAMENTE, senao a mesma paleta passa num e
// reprova no outro e a discussao vira sobre qual implementacao esta certa.
// Portado em 2026-09-01 para tests/test_economic_activity_js.js e extraido para
// ca em 2026-09-08, quando a secao de cenarios do FX Report passou a precisar do
// mesmo criterio para as suas dez cores de episodio.
//
// A regra que ele serve esta em .claude/rules/lis-dashboards.md: duas series que
// podem dividir um grafico precisam de dE2000 >= 20. O limiar foi calibrado
// contra paletas publicadas (pior par do Okabe-Ito 21,7; do Tol bright 20,5),
// nao escolhido.

function _lin(c) { c /= 255; return c <= 0.04045 ? c / 12.92 : Math.pow((c + 0.055) / 1.055, 2.4); }

function lab(hex) {
  const h = hex.replace('#', '');
  const r = _lin(parseInt(h.slice(0, 2), 16)), g = _lin(parseInt(h.slice(2, 4), 16)), b = _lin(parseInt(h.slice(4, 6), 16));
  const x = (r * 0.4124564 + g * 0.3575761 + b * 0.1804375) / 0.95047;
  const y = (r * 0.2126729 + g * 0.7151522 + b * 0.0721750);
  const z = (r * 0.0193339 + g * 0.1191920 + b * 0.9503041) / 1.08883;
  const f = (t) => (t > 216 / 24389 ? Math.cbrt(t) : (841 / 108) * t + 4 / 29);
  const fx = f(x), fy = f(y), fz = f(z);
  return [116 * fy - 16, 500 * (fx - fy), 200 * (fy - fz)];
}

function deltaE(hex1, hex2) {
  const L1 = lab(hex1), L2 = lab(hex2);
  const C1 = Math.hypot(L1[1], L1[2]), C2 = Math.hypot(L2[1], L2[2]), Cb = (C1 + C2) / 2;
  const G = 0.5 * (1 - Math.sqrt(Math.pow(Cb, 7) / (Math.pow(Cb, 7) + Math.pow(25, 7))));
  const a1p = (1 + G) * L1[1], a2p = (1 + G) * L2[1];
  const C1p = Math.hypot(a1p, L1[2]), C2p = Math.hypot(a2p, L2[2]);
  const h1p = (Math.atan2(L1[2], a1p) * 180 / Math.PI + 360) % 360;
  const h2p = (Math.atan2(L2[2], a2p) * 180 / Math.PI + 360) % 360;
  const dLp = L2[0] - L1[0], dCp = C2p - C1p;
  let dhp = 0;
  if (C1p * C2p !== 0) {
    dhp = h2p - h1p;
    if (dhp > 180) dhp -= 360; else if (dhp < -180) dhp += 360;
  }
  const dHp = 2 * Math.sqrt(C1p * C2p) * Math.sin(dhp * Math.PI / 360);
  const Lbp = (L1[0] + L2[0]) / 2, Cbp = (C1p + C2p) / 2;
  let hbp;
  if (C1p * C2p === 0) hbp = h1p + h2p;
  else if (Math.abs(h1p - h2p) <= 180) hbp = (h1p + h2p) / 2;
  else hbp = (h1p + h2p + (h1p + h2p < 360 ? 360 : -360)) / 2;
  const rad = (d) => d * Math.PI / 180;
  const T = 1 - 0.17 * Math.cos(rad(hbp - 30)) + 0.24 * Math.cos(rad(2 * hbp))
            + 0.32 * Math.cos(rad(3 * hbp + 6)) - 0.20 * Math.cos(rad(4 * hbp - 63));
  const dTheta = 30 * Math.exp(-Math.pow((hbp - 275) / 25, 2));
  const Rc = 2 * Math.sqrt(Math.pow(Cbp, 7) / (Math.pow(Cbp, 7) + Math.pow(25, 7)));
  const Sl = 1 + (0.015 * Math.pow(Lbp - 50, 2)) / Math.sqrt(20 + Math.pow(Lbp - 50, 2));
  const Sc = 1 + 0.045 * Cbp, Sh = 1 + 0.015 * Cbp * T;
  const Rt = -Math.sin(rad(2 * dTheta)) * Rc;
  return Math.sqrt(Math.pow(dLp / Sl, 2) + Math.pow(dCp / Sc, 2) + Math.pow(dHp / Sh, 2)
                   + Rt * (dCp / Sc) * (dHp / Sh));
}

// Pior par de uma lista, com o par que o produziu — a forma em que os testes
// realmente usam isto, e que evita cada um reescrever o laco duplo.
function worstPair(cores) {
  let pior = Infinity, par = null;
  for (let i = 0; i < cores.length; i++) {
    for (let j = i + 1; j < cores.length; j++) {
      const d = deltaE(cores[i], cores[j]);
      if (d < pior) { pior = d; par = [cores[i], cores[j]]; }
    }
  }
  return { deltaE: pior, pair: par };
}

module.exports = { deltaE, lab, worstPair };
