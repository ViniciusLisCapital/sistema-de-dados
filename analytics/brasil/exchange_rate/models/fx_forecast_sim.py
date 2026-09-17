"""Simulador em Python da projecao do FX Model.

O ajuste do modelo vive em Python (`ridge_deviation_model.py`), mas a projecao
para frente so existia em JavaScript, dentro do bloco de script de
`report.html` (funcoes `channelDeltas` e `simulateForecast`). Este modulo porta
esse laco para que um relatorio em PDF possa rodar cenarios sem um navegador.

Nada aqui reestima coisa alguma: `alpha`, `beta`, `channel_stats`, `seed_level`
e `seed_delta_fx_lag1` sao lidos do payload de `build_dashboard_payload()`. O
corte do ajuste continua congelado em `model_fit_cutoff.json`.

A recorrencia, identica a do JS:

    delta(h) = alpha + beta_ar * delta(h-1) + sum_c beta_c * (var_c(h) / sd_c)
    nivel(h) = nivel(h-1) * exp(delta(h) / 100)

onde `var_c(h)` e a diferenca de nivel entre a caixa h e a anterior (ou a
variacao em log vezes 100, para os canais com `is_log_return`), e a caixa -1 e
o ultimo valor **do ajuste** (jun/2026), nao o ultimo dado disponivel.

Duas armadilhas do original, ambas silenciosas, tratadas aqui:

1. **O salto fantasma.** No JS, uma caixa nao editada volta ao valor de
   jun/2026 em vez de seguir o ultimo dado conhecido. Como os tres primeiros
   meses vem preenchidos com o realizado (o `nowcast`), a quarta caixa produz
   um degrau artificial -- medido, +3,7% de depreciacao em out/2026, igual em
   qualquer cenario. `build_paths()` ancora as caixas livres no ultimo valor
   realizado justamente para nao importar esse degrau.
2. **O horizonte.** O modelo ancora em jun/2026 e anda 12 meses, terminando em
   jun/2027. Para doze meses a contar do ultimo dado (set/2026) sao precisos 15
   passos: os tres primeiros consomem o realizado e os doze seguintes sao o
   cenario. `HORIZON_DEFAULT` reflete isso.
"""

import math

# Os canais na ordem em que o JS os percorre. `delta_fx_lag1` fica de fora: e
# o termo autorregressivo, alimentado pela propria previsao, nao por uma caixa.
CHANNEL_KEYS = [
    "delta_ppp",
    "delta_fiscal",
    "delta_dxy_em",
    "delta_carry_vol",
    "delta_sp500",
    "delta_icbr_usd",
]

TREND_SEEDED = ["delta_ppp"]   # TREND_SEEDED_RG no JS
TREND_LOOKBACK = 12            # TREND_LOOKBACK_RG no JS

HORIZON_JS = 12                # o que a pagina roda
HORIZON_DEFAULT = 15           # 3 meses realizados + 12 de cenario


def raw_key(key):
    return key[len("delta_"):] if key.startswith("delta_") else key


def future_months(last_month, n):
    """Meses seguintes a `last_month`, no formato YYYY-MM. Espelha futureMonthLabels()."""
    y, m = (int(p) for p in last_month.split("-"))
    out = []
    for _ in range(n):
        m += 1
        if m > 12:
            m = 1
            y += 1
        out.append("%04d-%02d" % (y, m))
    return out


def ppp_drift(payload):
    """Deriva mensal em log do diferencial de inflacao, olhando 12 meses.

    E o unico canal cujas caixas nao sao planas por default no JS -- e a razao
    pela qual o caminho neutro inclina para cima mesmo sem nenhum choque.
    """
    v = payload["forecast"]["channel_history"]["ppp"]["values"]
    k = min(TREND_LOOKBACK, len(v) - 1)
    if k <= 0:
        return 0.0
    return 100.0 * math.log(v[-1] / v[-1 - k]) / k


def default_levels(payload, horizon=HORIZON_JS, anchor_last_real=False):
    """As caixas como a pagina as monta.

    `anchor_last_real=False` reproduz o JS ao pe da letra, degrau incluido --
    e o que a verificacao contra o dashboard exige. `True` ancora cada canal no
    ultimo valor realizado (o `nowcast`, quando existe), que e o ponto de
    partida honesto para um cenario.
    """
    fc = payload["forecast"]
    months = future_months(fc["channel_history"]["fiscal"]["months"][-1], horizon)
    nowcast = (fc.get("nowcast") or {}).get("channels") or {}
    drift_ppp = ppp_drift(payload)

    levels, flags = {}, {}
    for key in CHANNEL_KEYS:
        rk = raw_key(key)
        hist = fc["channel_history"][rk]
        last_fit = hist["values"][-1]
        nc = nowcast.get(rk) or {"months": [], "values": []}
        drift = drift_ppp if key in TREND_SEEDED else 0.0

        base = last_fit
        if anchor_last_real and nc["values"]:
            base = nc["values"][-1]

        col, flg = [], []
        n_real = 0
        for h, m in enumerate(months):
            if m in nc["months"]:
                col.append(nc["values"][nc["months"].index(m)])
                flg.append("real")
                n_real = h + 1
            else:
                # passos a contar do fim do trecho realizado, nao do ajuste
                step = (h - n_real + 1) if anchor_last_real else (h + 1)
                col.append(base if drift == 0 else base * math.exp(drift * step / 100.0))
                flg.append(False)
        levels[key], flags[key] = col, flg
    return months, levels, flags


def channel_deltas(payload, key, boxes):
    """Espelha channelDeltas(): a caixa -1 e o ultimo valor DO AJUSTE."""
    hist = payload["forecast"]["channel_history"][raw_key(key)]
    last_real = hist["values"][-1]
    is_log = bool(hist.get("is_log_return"))
    out = []
    for h, box in enumerate(boxes):
        prev = last_real if h == 0 else boxes[h - 1]
        out.append(100.0 * math.log(box / prev) if is_log else box - prev)
    return out


def simulate(payload, levels, horizon=None):
    """Espelha simulateForecast(). Devolve (niveis, deltas, contribuicoes)."""
    fc = payload["forecast"]
    alpha = fc["alpha"]
    beta = fc["beta"]
    stats = fc["channel_stats"]
    n = horizon or len(levels[CHANNEL_KEYS[0]])

    deltas = {k: channel_deltas(payload, k, levels[k]) for k in CHANNEL_KEYS}

    level = fc["seed_level"]
    prev_delta = fc["seed_delta_fx_lag1"]
    path, dpath, contrib = [], [], []
    for h in range(n):
        parts = {"alpha": alpha, "ar": beta["delta_fx_lag1"] * prev_delta}
        d = parts["alpha"] + parts["ar"]
        for key in CHANNEL_KEYS:
            z = deltas[key][h] / stats[key]["std"]
            parts[key] = beta[key] * z
            d += parts[key]
        level *= math.exp(d / 100.0)
        path.append(level)
        dpath.append(d)
        contrib.append(parts)
        prev_delta = d
    return path, dpath, contrib


def error_band(payload, path, offset=0):
    """Banda de +-1 desvio-padrao, do proprio walk-forward do modelo.

    `offset` e quantos passos do caminho ja sao dado realizado: a banda so
    comeca a contar dali, porque e dali que a projecao de fato comeca.
    """
    se = payload["forecast_error_bands"]["std_error_pct"]
    lo, hi = [], []
    for h, lv in enumerate(path):
        j = h - offset
        if j < 0:
            lo.append(lv)
            hi.append(lv)
            continue
        s = se[min(j, len(se) - 1)]
        lo.append(lv * (1 - s / 100.0))
        hi.append(lv * (1 + s / 100.0))
    return lo, hi


def spot_residual(payload, horizon=HORIZON_DEFAULT):
    """Quanto o cambio observado difere do que os canais explicam, hoje.

    O modelo e uma explicacao do mesmo mes, entao rodar a recorrencia sobre os
    canais JA REALIZADOS produz um nivel que deveria bater com o PTAX do mesmo
    mes. A diferenca e o residuo acumulado desde o corte do ajuste -- e ela
    tem de ser dita, nao absorvida em silencio.

    Devolve (mes, ptax_observado, nivel_do_modelo, residuo_em_%).
    """
    months, base, flags = default_levels(payload, horizon, anchor_last_real=True)
    n_real = max(sum(1 for f in col if f == "real") for col in flags.values())
    path, _, _ = simulate(payload, base, horizon)
    nc_ptax = payload["forecast"]["nowcast"]["ptax"]
    obs = nc_ptax["values"][-1]
    mod = path[n_real - 1]
    return nc_ptax["months"][-1], obs, mod, 100.0 * (obs / mod - 1.0)


def build_paths(payload, scenarios, horizon=HORIZON_DEFAULT, rebase_to_spot=True):
    """Roda varios cenarios sobre a mesma base ancorada no realizado.

    `scenarios` = {nome: {chave_do_canal: [niveis dos meses livres]}}. Uma
    chave ausente mantem o caminho neutro daquele canal.

    `rebase_to_spot` reescala o caminho inteiro para que o ultimo mes realizado
    valha o PTAX efetivamente observado. Sem isso, os tres cenarios partem do
    nivel que o modelo explica (5,02) e nao do que o mercado negocia (5,10), e
    todo endpoint carrega 1,5% de residuo que nao tem nada a ver com o cenario.
    O residuo continua reportavel por `spot_residual()`.
    """
    months, base, flags = default_levels(payload, horizon, anchor_last_real=True)
    # O trecho realizado tem tamanho DIFERENTE por canal (o CDS, o dolar EM e o
    # S&P vao ate set/2026; carry, commodity e PPP so ate jul/2026). O cenario
    # comeca depois do mais longo deles, para que os seis canais compartilhem
    # uma linha do tempo -- os meses que faltam nos canais mais curtos ficam no
    # proprio ultimo valor realizado, que e a continuacao honesta.
    n_real = max(sum(1 for f in col if f == "real") for col in flags.values())

    out = {}
    for name, overrides in scenarios.items():
        levels = {k: list(v) for k, v in base.items()}
        for key, free_path in (overrides or {}).items():
            if key not in levels:
                raise KeyError("canal desconhecido: %s" % key)
            n_free = len(levels[key]) - n_real
            if len(free_path) != n_free:
                raise ValueError(
                    "%s/%s: %d valores para %d meses livres"
                    % (name, key, len(free_path), n_free)
                )
            levels[key][n_real:] = list(free_path)
        path, dpath, contrib = simulate(payload, levels, horizon)
        scale = 1.0
        if rebase_to_spot:
            obs = payload["forecast"]["nowcast"]["ptax"]["values"][-1]
            scale = obs / path[n_real - 1]
            path = [v * scale for v in path]
        lo, hi = error_band(payload, path, offset=n_real)
        out[name] = {
            "rebase_scale": scale,
            "months": months,
            "levels": levels,
            "path": path,
            "deltas": dpath,
            "contrib": contrib,
            "lo": lo,
            "hi": hi,
            "n_real": n_real,
        }
    return out


def verify_against_dashboard(payload, expected=None, tol=1e-3):
    """Refaz o caminho que a pagina produz sem nenhuma caixa editada.

    Se isto nao bater, o port esta errado e nenhum cenario vale. E a checagem
    que a secao de verificacao do plano exige antes de qualquer cenario.
    """
    _, levels, _ = default_levels(payload, HORIZON_JS, anchor_last_real=False)
    path, _, _ = simulate(payload, levels, HORIZON_JS)
    if expected is None:
        return path, None
    diffs = [abs(a - b) for a, b in zip(path, expected)]
    return path, (max(diffs) if diffs else 0.0) <= tol
