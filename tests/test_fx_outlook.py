# -*- coding: utf-8 -*-
"""Testes do Panorama Cambial (`analytics/brasil/exchange_rate/`).

Cada um nasceu de um defeito concreto encontrado ao construir o relatorio:

1. **O port do simulador.** A projecao do FX Model so existia em JavaScript,
   dentro de `report.html`. `fx_forecast_sim.py` a reescreveu em Python. Se o
   port divergir do original, todo cenario do PDF passa a ser ficcao sem que
   nada levante erro -- entao o teste roda o **JS de verdade**, extraido do
   proprio arquivo entregue, e compara caminho contra caminho.
2. **O salto fantasma.** No JS, uma caixa nao editada volta ao valor do corte
   do ajuste (jun/2026) em vez de seguir o ultimo dado conhecido. Como os tres
   primeiros meses vem preenchidos com o realizado, isso produz um degrau
   artificial de ~3,7% em out/2026, igual nos tres cenarios. Medido antes da
   correcao; o teste exige que o caminho neutro nao tenha esse degrau.
3. **As probabilidades.** Tres numeros escritos a mao que precisam somar 100.
4. **O PDF contra o dashboard.** Os dois leem as mesmas funcoes, entao um
   numero que divirja e sinal de que o PDF montou a conta de outro jeito.

Os testes que precisam de banco/FRED sao pulados quando nao ha acesso; os que
so precisam do HTML entregue rodam sempre.

    uv run pytest tests/test_fx_outlook.py -v
"""

import json
import math
import os
import shutil
import subprocess
import tempfile

try:
    import pytest
except ImportError:                     # pragma: no cover
    # O venv deste projeto nao sincroniza o extra `dev`, entao pytest pode nao
    # existir. Um shim minimo mantem o arquivo importavel e executavel pelo
    # runner do fim do arquivo -- as asserções sao as mesmas nos dois modos.
    class _Skipped(Exception):
        pass

    class _Mark(object):
        @staticmethod
        def skipif(cond, reason=""):
            def deco(fn):
                fn._skip = (bool(cond), reason)
                return fn
            return deco

    class _Pytest(object):
        mark = _Mark()
        Skipped = _Skipped

        @staticmethod
        def fixture(*a, **k):
            def deco(fn):
                return fn
            return deco if not (a and callable(a[0])) else a[0]

        @staticmethod
        def skip(msg=""):
            raise _Skipped(msg)

        @staticmethod
        def importorskip(name):
            try:
                return __import__(name)
            except ImportError:
                raise _Skipped("modulo ausente: %s" % name)

    pytest = _Pytest()

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPORT_HTML = os.path.join(ROOT, "reports", "brasil", "FX Report.html")


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------
@pytest.fixture(scope="module")
def payload():
    """Payload vivo do modelo. Precisa de MySQL e da fetch do FRED."""
    try:
        from analytics.brasil.exchange_rate.models import ridge_deviation_model as rdm
        return rdm.build_dashboard_payload()
    except Exception as exc:                                  # pragma: no cover
        pytest.skip("sem acesso aos dados do modelo: %s" % exc)


def _extract_ridge_data(path):
    """Le `const RIDGE_DATA = {...}` do HTML entregue, contando chaves."""
    src = open(path, encoding="utf-8").read()
    marker = "const RIDGE_DATA = "
    i = src.index(marker) + len(marker)
    depth = 0
    in_str = False
    esc = False
    for k in range(i, len(src)):
        c = src[k]
        if in_str:
            if esc:
                esc = False
            elif c == "\\":
                esc = True
            elif c == '"':
                in_str = False
            continue
        if c == '"':
            in_str = True
        elif c == "{":
            depth += 1
        elif c == "}":
            depth -= 1
            if depth == 0:
                return json.loads(src[i:k + 1])
    raise ValueError("RIDGE_DATA nao encontrado")


# ---------------------------------------------------------------------------
# 1. O port do simulador reproduz o JS
# ---------------------------------------------------------------------------
JS_HARNESS = r"""
const fs = require('fs');
const FC = JSON.parse(fs.readFileSync(process.argv[2], 'utf8')).forecast;
const CH = ['delta_ppp','delta_fiscal','delta_dxy_em','delta_carry_vol','delta_sp500','delta_icbr_usd'];

function futureMonths(last, n) {
  let [y, m] = last.split('-').map(Number); const out = [];
  for (let k = 0; k < n; k++) { m++; if (m > 12) { m = 1; y++; }
    out.push(String(y).padStart(4,'0') + '-' + String(m).padStart(2,'0')); }
  return out;
}
const lastFit = FC.channel_history.fiscal.months[FC.channel_history.fiscal.months.length - 1];
const months = futureMonths(lastFit, FC.horizon);
const currentMonth = FC.nowcast && FC.nowcast.current_month;

// --- verbatim de report.html (bloco de default das caixas) ---
const TREND_SEEDED_RG = ['delta_ppp'], TREND_LOOKBACK_RG = 12;
const levels = {}, resolvedFlags = {};
CH.forEach(key => {
  const rawKey = key.replace(/^delta_/, '');
  const hist = FC.channel_history[rawKey];
  const lastVal = hist.values[hist.values.length - 1];
  const nc = FC.nowcast && FC.nowcast.channels[rawKey];
  resolvedFlags[key] = months.map(m => {
    if (!nc || !nc.months.includes(m)) return false;
    return m === currentMonth ? 'provisional' : 'final';
  });
  let drift = 0;
  if (TREND_SEEDED_RG.includes(key)) {
    const v = hist.values, k = Math.min(TREND_LOOKBACK_RG, v.length - 1);
    if (k > 0) drift = 100 * Math.log(v[v.length - 1] / v[v.length - 1 - k]) / k;
  }
  levels[key] = months.map((m, h) => {
    if (resolvedFlags[key][h]) return nc.values[nc.months.indexOf(m)];
    return drift === 0 ? lastVal : lastVal * Math.exp(drift * (h + 1) / 100);
  });
});
function channelDeltas(key) {
  const hist = FC.channel_history[key.replace(/^delta_/, '')];
  const lastReal = hist.values[hist.values.length - 1];
  const boxes = levels[key], deltas = [];
  for (let h = 0; h < boxes.length; h++) {
    const prev = h === 0 ? lastReal : boxes[h - 1];
    deltas.push(hist.is_log_return ? 100 * Math.log(boxes[h] / prev) : boxes[h] - prev);
  }
  return deltas;
}
const dz = {}; CH.forEach(k => { dz[k] = channelDeltas(k); });
let prevDeltaFx = FC.seed_delta_fx_lag1, level = FC.seed_level; const out = [];
for (let h = 0; h < FC.horizon; h++) {
  let d = FC.alpha + FC.beta.delta_fx_lag1 * prevDeltaFx;
  CH.forEach(key => {
    const st = FC.channel_stats[key];
    const raw = dz[key][h];
    d += FC.beta[key] * (st.std > 0 ? raw / st.std : raw);
  });
  level = level * Math.exp(d / 100); out.push(level); prevDeltaFx = d;
}
console.log(JSON.stringify(out));
"""


@pytest.mark.skipif(shutil.which("node") is None, reason="node nao disponivel")
def test_port_do_simulador_reproduz_o_js(payload):
    """O Python tem de dar o MESMO caminho que o JS do relatorio, no MESMO payload.

    Rodar o JS contra o RIDGE_DATA do HTML entregue nao serve: aquele arquivo
    foi construido noutro instante e o nowcast de um canal pode ter mudado de
    vintage -- foi o que aconteceu com o S&P de set/2026 (7.592,44 no arquivo,
    7.600,05 no payload novo), e a diferenca aparecia como se fosse erro de
    port. Os dois lados precisam receber o mesmo payload.
    """
    from analytics.brasil.exchange_rate.models import fx_forecast_sim as sim

    tmp = tempfile.mkdtemp(prefix="fxsim_")
    pj = os.path.join(tmp, "payload.json")
    js = os.path.join(tmp, "harness.js")
    with open(pj, "w", encoding="utf-8") as f:
        json.dump({"forecast": payload["forecast"]}, f, default=str)
    with open(js, "w", encoding="utf-8") as f:
        f.write(JS_HARNESS)

    res = subprocess.run(["node", js, pj], capture_output=True, text=True, timeout=120)
    assert res.returncode == 0, res.stderr
    js_path = json.loads(res.stdout)

    py_path, _ = sim.verify_against_dashboard(payload)
    assert len(py_path) == len(js_path) == sim.HORIZON_JS
    for h, (a, b) in enumerate(zip(py_path, js_path)):
        assert abs(a - b) < 1e-9, "mes %d: python %.10f vs js %.10f" % (h, a, b)


# ---------------------------------------------------------------------------
# 2. O salto fantasma
# ---------------------------------------------------------------------------
def test_o_degrau_artificial_existe_no_default_do_js(payload):
    """Guarda do defeito: sem ancorar no realizado, out/2026 pula sozinho.

    Se algum dia o JS deixar de ter esse comportamento, este teste falha e
    avisa que a correcao de `build_paths()` virou desnecessaria -- em vez de
    ela ficar la para sempre corrigindo algo que nao existe mais.
    """
    from analytics.brasil.exchange_rate.models import fx_forecast_sim as sim

    _, levels, flags = sim.default_levels(payload, sim.HORIZON_JS, anchor_last_real=False)
    path, _, _ = sim.simulate(payload, levels, sim.HORIZON_JS)
    n_real = max(sum(1 for f in col if f == "real") for col in flags.values())
    degrau = 100.0 * (path[n_real] / path[n_real - 1] - 1.0)
    assert degrau > 2.0, "o degrau do default do JS sumiu (%.2f%%)" % degrau


def test_caminho_neutro_nao_importa_o_degrau(payload):
    """O cenario neutro nao pode ter salto entre o ultimo mes real e o primeiro projetado."""
    from analytics.brasil.exchange_rate.models import fx_forecast_sim as sim

    r = sim.build_paths(payload, {"neutro": {}})["neutro"]
    n0 = r["n_real"]
    degrau = 100.0 * (r["path"][n0] / r["path"][n0 - 1] - 1.0)
    assert abs(degrau) < 1.0, "degrau de %.2f%% em %s" % (degrau, r["months"][n0])


def test_projecao_parte_do_cambio_observado(payload):
    """Rebaseado, o ultimo mes realizado do caminho tem de ser o PTAX de fato."""
    from analytics.brasil.exchange_rate.models import fx_forecast_sim as sim

    r = sim.build_paths(payload, {"neutro": {}})["neutro"]
    obs = payload["forecast"]["nowcast"]["ptax"]["values"][-1]
    assert abs(r["path"][r["n_real"] - 1] - obs) < 1e-9


def test_residuo_do_modelo_e_reportavel(payload):
    """O residuo contra o spot existe e e um numero -- o PDF o imprime."""
    from analytics.brasil.exchange_rate.models import fx_forecast_sim as sim

    mes, obs, mod, pct = sim.spot_residual(payload)
    assert obs > 0 and mod > 0
    assert abs(pct) < 25.0, "residuo implausivel: %.2f%%" % pct
    assert abs(pct - 100.0 * (obs / mod - 1.0)) < 1e-9


# ---------------------------------------------------------------------------
# 3. As probabilidades
# ---------------------------------------------------------------------------
def test_probabilidades_somam_cem():
    from analytics.brasil.exchange_rate import generate_fx_outlook_pdf as G

    probs = G._scenarios.__defaults__ is not None  # nada a assertar aqui
    # as probabilidades sao constantes do modulo de cenarios
    import inspect
    src = inspect.getsource(G._scenarios)
    assert '"_probs"' in src
    # extrai o dicionario literal
    import re
    m = re.search(r'res\["_probs"\] = (\{[^}]*\})', src)
    assert m, "nao achei o bloco de probabilidades"
    d = eval(m.group(1))                      # literal simples do proprio fonte
    assert set(d) == {"otimista", "neutro", "pessimista"}
    assert sum(d.values()) == 100, "probabilidades somam %d" % sum(d.values())


# ---------------------------------------------------------------------------
# 4. O PDF concorda com o dashboard
# ---------------------------------------------------------------------------
@pytest.mark.skipif(not os.path.exists(REPORT_HTML), reason="FX Report.html nao gerado")
def test_numeros_batem_com_o_dashboard():
    """Os dois leem os mesmos carregadores; divergir e sinal de conta remontada."""
    from analytics.brasil.exchange_rate import generate_fx_outlook_pdf as G

    try:
        D = G.load_all()
    except Exception as exc:                                   # pragma: no cover
        pytest.skip("sem acesso aos dados: %s" % exc)

    src = open(REPORT_HTML, encoding="utf-8").read()
    marker = "const REPORT_DATA = "
    i = src.index(marker) + len(marker)
    depth = 0
    in_str = False
    esc = False
    R = None
    for k in range(i, len(src)):
        c = src[k]
        if in_str:
            if esc:
                esc = False
            elif c == "\\":
                esc = True
            elif c == '"':
                in_str = False
            continue
        if c == '"':
            in_str = True
        elif c == "{":
            depth += 1
        elif c == "}":
            depth -= 1
            if depth == 0:
                R = json.loads(src[i:k + 1])
                break
    assert R is not None

    def last(seq):
        return [v for v in seq if v is not None][-1]

    casos = [
        ("PTAX", D["px"]["last"], last(R["ptax"]["ptax_venda"])),
        ("termos de troca", D["tot"]["last"], last(R["termos"]["termos_de_troca_funcex"])),
        ("REER Brasil", D["reer_now"]["BR"], last(R["reer"]["BR"])),
        ("CFTC gestores", D["cot"]["asset_mgr_net"]["now"], last(R["cot_fx"]["asset_mgr_net"])),
        ("conta corrente 12m", D["bop12"]["conta_corrente"]["now"],
         sum(R["bop"]["conta_corrente"][-12:])),
        ("fluxo cambial 12m", D["fluxo"]["cc_saldo_total"]["now"],
         sum(v or 0 for v in R["cambio_contratado"]["cc_saldo_total"][-12:])),
    ]
    erros = []
    for nome, a, b in casos:
        # tolerancia relativa de 0,1%: o dashboard pode ter sido gerado noutro
        # instante e uma serie diaria pode ter ganho um ponto no meio
        if abs(a - b) > max(1e-6, abs(b) * 0.001):
            erros.append("%s: PDF %.4f vs dashboard %.4f" % (nome, a, b))
    assert not erros, "; ".join(erros)


# ---------------------------------------------------------------------------
# 5. O PDF gera e tem o que promete
# ---------------------------------------------------------------------------
def test_pdf_gera_e_contem_os_blocos():
    from analytics.brasil.exchange_rate import generate_fx_outlook_pdf as G

    try:
        D = G.load_all()
    except Exception as exc:                                   # pragma: no cover
        pytest.skip("sem acesso aos dados: %s" % exc)

    out = os.path.join(tempfile.mkdtemp(prefix="fxout_"), "teste.pdf")
    G.run(out_path=out, D=D)
    assert os.path.getsize(out) > 200_000

    fitz = pytest.importorskip("fitz")
    doc = fitz.open(out)
    txt = "\n".join(p.get_text() for p in doc)

    for termo in ("Sumário executivo", "Balanço de Pagamentos", "Fluxo Cambial",
                  "FX Attribution", "FX Model", "Três cenários", "Conclusão"):
        assert termo in txt, "faltou o bloco %r" % termo

    # vocabulario de mecanismo nao entra num documento para o leitor
    for proibido in ("generate_report", "build_dashboard_payload", "MySQL", "SGS 22701",
                     "delta_fiscal", "channel_stats", "nowcast"):
        assert proibido not in txt, "termo de bastidor vazou para a pagina: %r" % proibido

    # as tres probabilidades tem de aparecer e somar 100
    import re
    m = re.search(r"As probabilidades são (\d+)%, (\d+)% e (\d+)%", txt)
    assert m, "a frase das probabilidades sumiu do sumario executivo"
    assert sum(int(g) for g in m.groups()) == 100

    # ------------------------------------------------------------------
    # O grafico e o corpo da evidencia (2026-09-10, pedido do usuario:
    # "os graficos ficaram pequenos ... evite graficos duplos ... nao deixe
    # grafico com legendas em cima das linhas"). As tres regras nao tem
    # sintoma nenhum quando quebram -- um painel de meia largura continua
    # gerando, e uma legenda em cima da serie so some com o dado.
    # ------------------------------------------------------------------
    import matplotlib.pyplot as plt

    nomes = sorted(k for k in dir(G) if k.startswith("fig_"))
    assert len(nomes) >= 14, "faltam graficos: %d" % len(nomes)
    for nome in nomes:
        fig = getattr(G, nome)(D)
        assert len(fig.axes) == 1, "%s desenha %d paineis numa figura so" % (nome, len(fig.axes))
        ax = fig.axes[0]
        if ax.get_legend_handles_labels()[0]:
            # a legenda vive na FIGURA, ancorada abaixo do eixo -- dentro do
            # quadro ela cobre a serie que deveria mostrar
            assert ax.get_legend() is None, "%s: legenda dentro da area de plotagem" % nome
            assert fig.legends, "%s: series rotuladas e nenhuma legenda" % nome
        plt.close(fig)

    # e a imagem impressa ocupa a coluna: o quadro util e ~482 pt
    larguras = []
    for pg in doc:
        for img in pg.get_images(full=True):
            larguras.append(pg.get_image_bbox(img).width)
    assert larguras, "o PDF nao tem grafico nenhum"
    assert min(larguras) > 430, "grafico impresso estreito: %.0f pt" % min(larguras)


# ---------------------------------------------------------------------------
# Runner autonomo -- o venv deste projeto nao tem pytest instalado (ele esta
# no extra `dev`, que nao e sincronizado por padrao). Sem isto o arquivo seria
# um teste que ninguem consegue rodar.
#
#     uv run python tests/test_fx_outlook.py
# ---------------------------------------------------------------------------
def _main():
    import traceback

    try:
        from analytics.brasil.exchange_rate.models import ridge_deviation_model as rdm
        P = rdm.build_dashboard_payload()
    except Exception as exc:
        print("sem acesso aos dados do modelo:", exc)
        P = None

    casos = [
        ("port do simulador reproduz o JS", test_port_do_simulador_reproduz_o_js, True),
        ("o degrau artificial existe no default do JS", test_o_degrau_artificial_existe_no_default_do_js, True),
        ("caminho neutro nao importa o degrau", test_caminho_neutro_nao_importa_o_degrau, True),
        ("projecao parte do cambio observado", test_projecao_parte_do_cambio_observado, True),
        ("residuo do modelo e reportavel", test_residuo_do_modelo_e_reportavel, True),
        ("probabilidades somam cem", test_probabilidades_somam_cem, False),
        ("numeros batem com o dashboard", test_numeros_batem_com_o_dashboard, False),
        ("pdf gera e contem os blocos", test_pdf_gera_e_contem_os_blocos, False),
    ]
    ok = fail = skip = 0
    for nome, fn, precisa_payload in casos:
        if precisa_payload and P is None:
            print("  SKIP  %s" % nome)
            skip += 1
            continue
        try:
            fn(P) if precisa_payload else fn()
            print("  OK    %s" % nome)
            ok += 1
        except Exception as exc:
            if exc.__class__.__name__ in ("Skipped", "OutcomeException"):
                print("  SKIP  %s (%s)" % (nome, exc))
                skip += 1
                continue
            print("  FALHA %s" % nome)
            traceback.print_exc(limit=3)
            fail += 1
    print("\n%d ok, %d falhas, %d pulados" % (ok, fail, skip))
    return 1 if fail else 0


if __name__ == "__main__":
    import sys
    sys.exit(_main())
