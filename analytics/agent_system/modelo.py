"""
O Modelo Estrutural rodado por um agente: a função fixa que o G chama (SISTEMA_AGENTES.md IV.vi).

    # no início do ciclo, uma vez (o `dados` já faz isto sozinho):
    uv run python -m analytics.agent_system.modelo --ciclo 2026-10-15

    # dentro de um G do agente, em obsidian/ciclos/<ciclo>/dados/G/:
    from analytics.agent_system import modelo
    sim = modelo.carregar("2026-10-15")
    print(modelo.listar(sim))                     # exógenas e coeficientes, com as chaves
    base = modelo.rodar(sim, caminhos={"fiscal": {"4T26": 130, "1T27": 125}})
    worst = modelo.rodar(sim, caminhos={"fiscal": {"4T26": 150}}, mult={"F.b_fiscal": 1.5})
    print(modelo.texto(worst))

O que entra:

  caminhos  {exógena: {trimestre: valor}}, no nível e na unidade do cartão do simulador
            (`listar()` diz a de cada uma). Trimestre como "4T26" ou "2026T4". Antes do
            primeiro trimestre dado, vale o padrão do simulador (o último valor repetido;
            nas duas inflações, a média dos últimos 4 trimestres); a partir dele, o valor
            dado, segurado até o próximo. Endógena não entra: o modelo a resolve.
  mult      {"<equação>.<coeficiente>": m}, o tempero (i): o coeficiente multiplicado por m,
            na mediana e em cada desenho do posterior. m ≥ 0.

O que sai, por trimestre dos 12 seguintes ao último trimestre com dado (o último sai como
"observado", é dali que a conta parte): PTAX de fechamento, Selic média, IPCA do trimestre e
de 12 meses, Focus de 12 meses e hiato, cada um com a central (os pesos da mediana) e a faixa
de 90% do posterior.

Três regras, cada uma contra um defeito silencioso:

  - **Sem reestimar e sem banco.** O retrato do simulador é gravado uma vez por ciclo em
    `dados/A/modelo_estrutural.json`, com os pesos de hoje (`bayes/data/*_draws.json`), e o
    G lê dele. Rodar de novo no meio do ciclo daria outro modelo para o mesmo ciclo.
  - **A conta é a do simulador, não uma cópia.** A recursão e o laço são os de
    `simulator.resolver()`, o mesmo que dá o gabarito da página; sem caminho nenhum e sem
    multiplicador, a central sai igual ao cenário que a aba Structural Model abre, e
    `carregar()` confere isso a cada leitura.
  - **A faixa é incerteza dos PESOS, não do erro das equações.** É a mesma faixa da página
    (`_simFaixasSistema`): o desenho s de cada equação entra junto e o laço é resolvido para
    ele. Ela não é um intervalo de previsão: o erro de um trimestre da equação do câmbio
    sozinho é de ~3,6%. A distribuição em torno da central é do agente (IV.ix).
"""

from __future__ import annotations

import argparse
import bisect
import datetime as dt
import json
import sys
from pathlib import Path

import numpy as np

from analytics.agent_system.dados import motor

ARQUIVO = "modelo_estrutural.json"

# As endógenas que saem, na ordem em que se leem. (chave, nome, unidade, casas)
SAIDAS = (
    ("ptax", "PTAX de venda, fechamento do trimestre", "R$/US$", 3),
    ("selic", "Selic, média do trimestre", "% a.a.", 2),
    ("ipca_12m", "IPCA acumulado em 12 meses, no fim do trimestre", "%", 2),
    ("ipca_tri", "IPCA no trimestre", "%", 2),
    ("focus_12m", "Focus IPCA 12 meses à frente, média do trimestre", "% a.a.", 2),
    ("hiato", "Hiato do produto", "% do potencial", 2),
)

# Coeficiente que não aceita multiplicador: o desvio do erro não entra na conta, e as
# marcas de crise valem zero em todo trimestre projetado.
_SEM_MULT = {"sigma", "d08", "d20"}


# ── o retrato do ciclo ────────────────────────────────────────────────────────
def _pasta_a(ciclo) -> Path:
    return motor.CICLOS / str(ciclo) / "dados" / "A"


def retratar(ciclo, refazer: bool = False) -> Path:
    """Monta o simulador (lê o banco e os desenhos gravados) e grava o retrato do ciclo."""
    from analytics.brasil.structural_model import simulator as sm

    saida = _pasta_a(ciclo) / ARQUIVO
    if saida.exists() and not refazer:
        return saida
    p = sm.construir()
    saida.parent.mkdir(parents=True, exist_ok=True)
    saida.write_text(json.dumps({
        "ciclo": str(ciclo),
        "gerado_em": dt.datetime.now().isoformat(timespec="seconds"),
        "p": p,
    }), encoding="utf-8")
    return saida


def carregar(ciclo) -> dict:
    """Lê o retrato do ciclo e confere que ele reproduz o cenário padrão do simulador."""
    from analytics.brasil.structural_model import simulator as sm

    arq = _pasta_a(ciclo) / ARQUIVO
    if not arq.exists():
        raise FileNotFoundError(
            f"{arq} não existe. Ele é gravado no início do ciclo, com:\n"
            f"    uv run python -m analytics.agent_system.modelo --ciclo {ciclo}")
    sim = json.loads(arq.read_text(encoding="utf-8"))
    p = sim["p"]
    sol, _ = sm.resolver(p, _coefs(p, {}), p["i0"], p["h_padrao"],
                         sm.entradas(p, p["i0"], p["h_padrao"]))
    for var, gab in p["sistema_padrao"]["caminho"].items():
        if max(abs(a - b) for a, b in zip(sol[var], gab)) > 1e-6:
            raise ValueError(f"o retrato não reproduz o cenário padrão do simulador em {var!r}")
    return sim


# ── a partida: o último trimestre com dado ────────────────────────────────────
def _partida(sim: dict) -> dict:
    """Confere que a projeção parte do trimestre seguinte ao último com dado, e o que faltou nele.

    Decisão do usuário em 2026-10-15: trimestre que já tem dado não se projeta. O simulador
    parte daí desde então (`p["i0"]`, o trimestre seguinte ao último completo da grade), com
    os pesos da estimação, que pode ter parado antes: o dado anda, a estimação não.

    Uma exógena sem o dado daquele trimestre (hoje, a vol implícita, que vem de uma planilha)
    fica no último valor conhecido e é listada em `segurados`, para o agente ver. Uma
    endógena sem ele levanta: a conta partiria de um número que ninguém observou.
    """
    if "_pc" in sim:
        return sim["_pc"]
    p = sim["p"]
    u = len(p["rot"]) - 1
    if p["i0"] != u + 1:
        raise ValueError(f"o retrato parte de {p['i0']}, e não do trimestre seguinte ao último "
                         f"com dado ({u + 1}): é de antes de 2026-10-15; refaça com --refazer")
    segurados = []
    for k in _exogenas_keys(p):
        obs = p["var"][k]["obs"]
        if obs[u] is None:
            j = _ultimo(obs)
            segurados.append({"chave": k, "nome": p["var"][k]["nome"], "valor": obs[j],
                              "de": _rot(p["rot"][j]), "em": _rot(p["rot"][u])})
    endo = [k for k in p["var_ordem"] if p["var"][k]["tipo"] == "endogena"]
    falta = [p["var"][k]["nome"] for k in endo if p["var"][k]["obs"][u] is None]
    falta += [f"IPCA {g}" for g in p["eq"]["I"]["ordem_grupos"]
              if p["eq"]["I"]["obs_grupo"][g][u] is None]
    if falta:
        raise ValueError(f"o retrato não tem {_rot(p['rot'][u])} completo: falta {', '.join(falta)}")
    sim["_pc"] = {"p": p, "segurados": segurados}
    return sim["_pc"]


# ── trimestres ────────────────────────────────────────────────────────────────
def _janela(p: dict) -> list[tuple[int, int]]:
    """(ano, trimestre) de cada posição da janela projetada."""
    ult = p["rot"][-1]
    ano, tri = int(ult[:4]), int(ult[5:])
    n0 = ano * 4 + tri - 1 + (p["i0"] - (len(p["rot"]) - 1))
    return [divmod(n0 + k, 4) for k in range(p["h_padrao"])]


def _rotulo(ano: int, tri0: int) -> str:
    return f"{tri0 + 1}T{ano % 100:02d}"


def _rot(r: str) -> str:
    """'2026T3', o rótulo da grade, -> '3T26', o dos reports."""
    return _rotulo(int(r[:4]), int(r[5:]) - 1)


def _ler_tri(s: str) -> tuple[int, int]:
    """'4T26' ou '2026T4' -> (2026, 3), o trimestre contado de zero."""
    a, b = str(s).strip().upper().split("T")
    if len(a) == 4:
        ano, tri = int(a), int(b)
    else:
        ano, tri = 2000 + int(b), int(a)
    if not 1 <= tri <= 4:
        raise ValueError(f"trimestre inválido: {s!r}")
    return ano, tri - 1


def _fechado(ano: int, tri0: int, ciclo: dt.date) -> bool:
    prox = dt.date(ano + (tri0 == 3), (tri0 + 1) % 4 * 3 + 1, 1)
    return ciclo >= prox


# ── coeficientes ──────────────────────────────────────────────────────────────
def _ler_mult(p: dict, mult: dict) -> dict:
    """{"F.b_fiscal": 1.5} -> {"F": {"b_fiscal": 1.5}}, validado."""
    out: dict = {}
    for chave, m in (mult or {}).items():
        ek, _, par = chave.partition(".")
        if ek not in p["eq"] or par not in p["eq"][ek]["pars"]:
            raise KeyError(f"coeficiente desconhecido: {chave!r}. Ver modelo.listar().")
        if par.split(".")[-1] in _SEM_MULT:
            raise ValueError(f"{chave!r} não entra na projeção; não aceita multiplicador.")
        if m is None or float(m) < 0:
            raise ValueError(f"multiplicador de {chave!r} tem de ser ≥ 0, veio {m!r}")
        out.setdefault(ek, {})[par] = float(m)
    return out


def _coefs(p: dict, mult: dict, s: int | None = None) -> dict:
    """Os pesos de cada equação: a mediana (s=None) ou o desenho s, com os multiplicadores."""
    out = {}
    for ek in p["eq_ordem"]:
        e = p["eq"][ek]
        c = (dict(e["mediana"]) if s is None
             else {par: e["draws"][par][s] for par in e["pars"]})
        for par, m in mult.get(ek, {}).items():
            c[par] = c[par] * m
        out[ek] = c
    return out


def _descreve(p: dict, ek: str, par: str) -> tuple[str, str]:
    """(o que o coeficiente é, o que ele lê), em uma linha cada."""
    e, var = p["eq"][ek], p["var"]
    if ek == "F":
        if par == "alpha":
            return "constante da equação do câmbio", "—"
        if par == "phi":
            return "inércia do câmbio (variação do trimestre anterior)", "câmbio"
        c = par[2:]
        # O desvio-padrao e o da janela de REFERENCIA da equacao, nao o da amostra do
        # ajuste: no CDS, 298,5 p.b. (2002 inteiro dentro) contra ~57 de 2006 a 2026. Sem
        # o numero ao lado, "por desvio-padrao" faz o peso parecer outra coisa.
        sd = e["sd"][c]
        un = "% de variação" if c in e["log_ret"] else (
            "" if c == "carry_vol" else var[c]["unidade"])
        por = f"por desvio-padrão da variação ({_f(sd, 3 if sd < 1 else 1)}{' ' + un if un else ''})"
        if c == "carry_vol":
            return (f"efeito no câmbio da variação do carry, {por}",
                    "(Selic − Fed Funds) / vol implícita")
        return (f"efeito no câmbio da variação de {var[c]['nome_frase']}, {por}",
                var[c]["nome"])
    if ek == "R":
        return {"t1": ("suavização da Selic, 1º trimestre anterior", "Selic"),
                "t2": ("suavização da Selic, 2º trimestre anterior", "Selic"),
                "t3": ("reação da Selic ao desvio da expectativa contra a meta",
                       "Focus 12m − meta")}[par]
    if ek == "E":
        return {"e1": ("inércia da expectativa (o peso da meta é 1 − e1 − e2)", "Focus 12m"),
                "e2": ("peso do IPCA de 12 meses na expectativa", "IPCA 12m")}[par]
    if ek == "H":
        lag = int(e["lag"])
        return {"h1": ("inércia do hiato", "hiato"),
                "h2": ("efeito do aperto monetário no hiato, "
                       + ("no trimestre seguinte" if lag == 1 else f"{lag} trimestres depois"),
                       "Selic − juro real de 10 anos − meta")}[par]
    if ek == "I":
        g, q = par.split(".")
        G = e["grupos"][g]
        lido = {"hiato": "do hiato", "de_med": "do câmbio médio do trimestre",
                "de_med_l1": "do câmbio médio do trimestre anterior",
                "agr": "das commodities agrícolas em US$", "met": "dos metais em US$",
                "met_l1": "dos metais em US$ do trimestre anterior",
                "mm4": "da média de 4 trimestres do próprio grupo",
                "cheio_l1": "do IPCA cheio do trimestre anterior"}
        if q == G["inercia"]:
            return f"{G['nome']}: inércia", G["nome"]
        for pq, tipo in list(G["restritos"]) + list(G["regs"]):
            if pq == q:
                de = lido.get(tipo, tipo)
                return f"{G['nome']}: efeito {de}", de.split(" ", 1)[-1]
        return f"{G['nome']}: sazonalidade ({q})", "trimestre do ano"
    return par, "—"


def coeficientes(sim: dict) -> list[dict]:
    """Os coeficientes que aceitam multiplicador, com a mediana e o intervalo de 90%."""
    p = sim["p"]
    out = []
    for ek in p["eq_ordem"]:
        e = p["eq"][ek]
        for par in e["pars"]:
            if par.split(".")[-1] in _SEM_MULT:
                continue
            o_que, le = _descreve(p, ek, par)
            out.append({"chave": f"{ek}.{par}", "equacao": e["nome"], "o_que": o_que,
                        "le": le, "mediana": float(e["mediana"][par]),
                        "intervalo": [float(x) for x in e["hdi"][par]],
                        "prob": float(e["hdi_prob"])})
    return out


def _posicao(p: dict, ek: str, par: str, m: float) -> dict:
    """Onde o coeficiente multiplicado cai no posterior ESTIMADO."""
    e = p["eq"][ek]
    med = float(e["mediana"][par])
    val = med * m
    d = sorted(float(x) for x in e["draws"][par])
    lo, hi = (float(x) for x in e["hdi"][par])
    return {"chave": f"{ek}.{par}", "o_que": _descreve(p, ek, par)[0], "m": m,
            "mediana": med, "multiplicado": val, "intervalo": [lo, hi],
            "prob": float(e["hdi_prob"]),
            "percentil": 100.0 * bisect.bisect_right(d, val) / len(d),
            "dentro": lo <= val <= hi}


# ── exógenas ──────────────────────────────────────────────────────────────────
def _exogenas_keys(p: dict) -> list[str]:
    usadas = {c for ek in p["eq_ordem"] for c in p["eq"][ek]["consome"]}
    return [k for k in p["var_ordem"] if p["var"][k]["tipo"] != "endogena" and k in usadas]


def _ultimo(obs: list) -> int:
    return max((i for i, v in enumerate(obs) if v is not None), default=-1)


def exogenas(sim: dict) -> list[dict]:
    """As exógenas do simulador: chave, nome, unidade, o último dado e o caminho padrão."""
    from analytics.brasil.structural_model import simulator as sm

    p = _partida(sim)["p"]
    jan = [_rotulo(a, t) for a, t in _janela(p)]
    out = []
    for k in _exogenas_keys(p):
        v = p["var"][k]
        u = _ultimo(v["obs"])
        seg = v.get("segura") or {}
        out.append({
            "chave": k, "nome": v["nome"], "unidade": v["unidade"],
            "regiao": v.get("regiao"), "como_digitar": v.get("instrucao"),
            "lida_por": [p["eq"][ek]["nome"] for ek in p["eq_ordem"]
                         if k in p["eq"][ek]["consome"]],
            "ultimo": {"trimestre": _rot(p["rot"][u]), "valor": v["obs"][u]},
            "padrao": dict(zip(jan, sm._observado(p, k, p["i0"], p["h_padrao"]))),
            "regra_padrao": (f"média dos últimos {seg['k']} trimestres"
                             if seg.get("modo") == "media" else "último valor repetido"),
        })
    return out


def _caminhos(p: dict, caminhos: dict) -> tuple[dict, dict]:
    """O `ent` do simulador com os caminhos do cenário, e a fonte de cada valor."""
    from analytics.brasil.structural_model import simulator as sm

    i0, h = p["i0"], p["h_padrao"]
    ent = sm.entradas(p, i0, h)
    pos = {t: k for k, t in enumerate(_janela(p))}
    exo = _exogenas_keys(p)
    fonte = {k: ["padrão"] * h for k in exo}
    for k, valores in (caminhos or {}).items():
        if k not in p["var"]:
            raise KeyError(f"exógena desconhecida: {k!r}. As do simulador: {', '.join(exo)}")
        if p["var"][k]["tipo"] == "endogena":
            raise ValueError(f"{k!r} é endógena: o modelo a resolve, o cenário não a fixa.")
        if k not in exo:
            raise ValueError(f"{k!r} não é lida por nenhuma equação do simulador.")
        dados = {}
        for t, v in valores.items():
            j = pos.get(_ler_tri(t))
            if j is None:
                raise ValueError(f"{k}: {t} fora da janela do simulador "
                                 f"({_rotulo(*_janela(p)[0])} a {_rotulo(*_janela(p)[-1])})")
            dados[j] = float(v)
        cam, atual = list(ent[k]), None
        for j in range(h):
            if j in dados:
                atual = dados[j]
            if atual is not None:
                cam[j] = atual
                fonte[k][j] = "cenário" if j in dados else "cenário, segurado"
        ent[k] = cam
    return ent, fonte


# ── a rodada ──────────────────────────────────────────────────────────────────
def _saidas(p: dict, sol: dict) -> dict:
    from analytics.brasil.structural_model import simulator as sm

    i0, h = p["i0"], p["h_padrao"]
    eqi = p["eq"]["I"]
    pre = list(eqi["pre_insumo"]["infl_br"])
    serie = pre + list(eqi["obs_insumo"]["infl_br"][:i0]) + list(sol["infl_br"])
    return {
        "ptax": list(sol["de"]),
        "selic": list(sol["selic"]),
        "ipca_12m": [sm._i12_de_trimestres(serie, len(pre) + i0 + j) for j in range(h)],
        "ipca_tri": [100.0 * (float(np.exp(x / 100.0)) - 1.0) for x in sol["infl_br"]],
        "focus_12m": list(sol["pi_e"]),
        "hiato": list(sol["hiato"]),
    }


def _observado_em(p: dict, i: int) -> dict:
    """As saídas no trimestre `i` da grade, como foram publicadas: o ponto de partida."""
    v = p["var"]
    return {"ptax": p["eq"]["F"]["ptax"][i], "selic": v["selic"]["obs"][i],
            "ipca_12m": p["eq"]["I"]["i12_obs"][i],
            "ipca_tri": 100.0 * (float(np.exp(v["infl_br"]["obs"][i] / 100.0)) - 1.0),
            "focus_12m": v["pi_e"]["obs"][i], "hiato": v["hiato"]["obs"][i]}


def _quantis(cols: list[list[float]], prob: float) -> tuple[list, list]:
    """Os mesmos índices de `_simQuantis` na página."""
    a, lo, hi = (1 - prob) / 2, [], []
    for col in cols:
        col = sorted(col)
        lo.append(col[int(np.floor(a * (len(col) - 1)))])
        hi.append(col[int(np.ceil((1 - a) * (len(col) - 1)))])
    return lo, hi


def rodar(sim: dict, caminhos: dict | None = None, mult: dict | None = None,
          faixa: bool = True) -> dict:
    """Um cenário: as endógenas por trimestre, com a central e a faixa de 90% do posterior."""
    from analytics.brasil.structural_model import simulator as sm

    part = _partida(sim)
    p = part["p"]
    i0, h = p["i0"], p["h_padrao"]
    mt = _ler_mult(p, mult)
    ent, fonte = _caminhos(p, caminhos)
    try:
        sol, voltas = sm.resolver(p, _coefs(p, mt), i0, h, ent)
    except RuntimeError as err:
        raise RuntimeError(f"o modelo não converge com estes multiplicadores ({err})") from None
    central = _saidas(p, sol)

    ciclo = dt.date.fromisoformat(sim["ciclo"])
    jan = _janela(p)
    res = {
        "ciclo": sim["ciclo"],
        "trimestres": [_rotulo(a, t) for a, t in jan],
        "fechados": [_rotulo(a, t) for a, t in jan if _fechado(a, t, ciclo)],
        "ultimo_dado": _rot(p["rot"][-1]),
        "partida": _observado_em(p, i0 - 1),
        "segurados": part["segurados"],
        "endogenas": {k: {"nome": n, "unidade": u, "casas": c, "central": central[k]}
                      for k, n, u, c in SAIDAS},
        "entradas": {k: {"nome": p["var"][k]["nome"], "unidade": p["var"][k]["unidade"],
                         "caminho": list(ent[k]), "fonte": fonte[k]}
                     for k in _exogenas_keys(p)},
        "mult": [_posicao(p, ek, par, m) for ek, ps in mt.items() for par, m in ps.items()],
        "caminhos": caminhos or {},
        "voltas": voltas,
        "faixa": None,
    }
    if not faixa:
        return res

    n = min(p["eq"][ek]["n_draws"] for ek in p["eq_ordem"])
    prob = float(p["eq"][p["eq_ordem"][0]]["hdi_prob"])
    cols = {k: [[] for _ in range(h)] for k, *_ in SAIDAS}
    falhou = 0
    for s in range(n):
        try:
            sd, _ = sm.resolver(p, _coefs(p, mt, s), i0, h, ent)
        except RuntimeError:
            falhou += 1
            continue
        for k, serie in _saidas(p, sd).items():
            for j in range(h):
                cols[k][j].append(serie[j])
    for k, *_ in SAIDAS:
        res["endogenas"][k]["lo"], res["endogenas"][k]["hi"] = _quantis(cols[k], prob)
    res["faixa"] = {"prob": prob, "desenhos": n - falhou, "nao_convergiu": falhou}
    return res


# ── texto, para o log ─────────────────────────────────────────────────────────
def _f(v, casas: int, sinal: bool = False) -> str:
    if v is None:
        return "—"
    s = f"{v:+,.{casas}f}" if sinal else f"{v:,.{casas}f}"
    return s.replace(",", "§").replace(".", ",").replace("§", ".")


def texto(res: dict, trimestres: list[str] | None = None) -> str:
    """O cenário em tabelas markdown: as endógenas (central e faixa) e o que entrou."""
    tri = res["trimestres"]
    idx = [tri.index(t) for t in (trimestres or tri)]
    cab = "| | " + " | ".join(tri[j] for j in idx) + " |\n|---|" + "---|" * len(idx)
    ud = res["ultimo_dado"]
    out = [f"Modelo Estrutural · ciclo {res['ciclo']} · parte do {ud} observado · "
           f"{res['voltas']} voltas"]
    for sg in res["segurados"]:
        out.append(f"Sem o dado de {sg['em']}: {sg['nome']}, segurada em {_f(sg['valor'], 2)} "
                   f"({sg['de']}).")
    if res["fechados"]:
        out.append("Já fecharam, mas o retrato não tem o dado completo deles: "
                   f"{', '.join(res['fechados'])} (projetados).")
    cab_e = cab.replace("| | ", f"| | {ud} (observado) | ", 1).replace("|---|", "|---|---|", 1)
    out += ["", "**Endógenas** — central" + (" e faixa" if res["faixa"] else ""), "", cab_e]
    for k, e in res["endogenas"].items():
        c = e["casas"]
        cel = [_f(res["partida"][k], c)]
        for j in idx:
            s = _f(e["central"][j], c)
            if res["faixa"]:
                s += f" [{_f(e['lo'][j], c)}; {_f(e['hi'][j], c)}]"
            cel.append(s)
        out.append(f"| {e['nome']} ({e['unidade']}) | " + " | ".join(cel) + " |")
    if res["faixa"]:
        fx = res["faixa"]
        out.append(f"\nFaixa: {fx['prob']:.0%} do posterior dos pesos, {fx['desenhos']} desenhos"
                   + (f", {fx['nao_convergiu']} sem convergir" if fx["nao_convergiu"] else "")
                   + ". Não inclui o erro das equações.")
    mexidas = [k for k, e in res["entradas"].items() if any(f != "padrão" for f in e["fonte"])]
    out += ["", "**Exógenas do cenário** (as outras no padrão do simulador)", ""]
    if mexidas:
        out.append(cab)
        for k in mexidas:
            e = res["entradas"][k]
            out.append(f"| {e['nome']} ({e['unidade']}) | "
                       + " | ".join(_f(e["caminho"][j], 2) for j in idx) + " |")
    else:
        out.append("nenhuma: o cenário padrão do simulador.")
    if res["mult"]:
        out += ["", "**Multiplicadores**", ""]
        for m in res["mult"]:
            lo, hi = m["intervalo"]
            out.append(f"- {m['chave']} ({m['o_que']}): × {_f(m['m'], 2)}, "
                       f"{_f(m['mediana'], 3)} → {_f(m['multiplicado'], 3)}; intervalo de "
                       f"{m['prob']:.0%} {_f(lo, 3)} a {_f(hi, 3)}, "
                       f"{'dentro' if m['dentro'] else 'FORA'}; percentil {_f(m['percentil'], 1)}")
    return "\n".join(out)


def listar(sim: dict) -> str:
    """As chaves que `rodar()` aceita: exógenas (com o padrão) e coeficientes."""
    p = _partida(sim)["p"]
    jan = [_rotulo(a, t) for a, t in _janela(p)]
    out = [f"Janela: {jan[0]} a {jan[-1]} · parte do último trimestre com dado, {_rot(p['rot'][-1])}",
           "", "**Exógenas** (caminhos={chave: {trimestre: valor}})", ""]
    for e in exogenas(sim):
        u = e["ultimo"]
        out.append(f"- `{e['chave']}` · {e['nome']} ({e['unidade']}) · último {u['trimestre']}"
                   f" = {_f(u['valor'], 2)} · padrão: {e['regra_padrao']}, "
                   f"{_f(e['padrao'][jan[0]], 2)} · lida por {', '.join(e['lida_por'])}")
    out += ["", "**Coeficientes** (mult={chave: m})", ""]
    for c in coeficientes(sim):
        lo, hi = c["intervalo"]
        out.append(f"- `{c['chave']}` · {c['o_que']} · mediana {_f(c['mediana'], 3)}, "
                   f"{c['prob']:.0%}: {_f(lo, 3)} a {_f(hi, 3)}")
    return "\n".join(out)


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser(prog="python -m analytics.agent_system.modelo")
    ap.add_argument("--ciclo", type=dt.date.fromisoformat, default=dt.date.today())
    ap.add_argument("--refazer", action="store_true")
    a = ap.parse_args()
    arq = retratar(a.ciclo.isoformat(), a.refazer)
    sim = carregar(a.ciclo.isoformat())
    print(f"  retrato  {arq}\n")
    print(listar(sim))
    print()
    print(texto(rodar(sim)))


if __name__ == "__main__":
    main()
