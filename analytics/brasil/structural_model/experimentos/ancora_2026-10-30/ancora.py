"""Teste da ancora da (R) e da (H) -- chat C do Plano 2, 2026-10-30.

Decisao do usuario (coordenacao/C_modelo.md, "Decisoes", item 2): testar a ancora
`rr_10a + meta` contra a mesma ancora com o juro real de 10 anos em media movel de 4
e de 8 trimestres, e, como variante extra, a media movel como ancora com o desvio do
10 anos cru contra a propria media como regressor proprio na (H).

Variantes, as duas equacoes trocadas JUNTAS (elas dividem a ancora):

    (0)   ancora = rr_10a + meta                              -- a de hoje
    (1)   ancora = MM4(rr_10a) + meta
    (2)   ancora = MM8(rr_10a) + meta
    (1b)  como (1), e a (H) le tambem dev = rr_10a - MM4(rr_10a), defasado
    (2b)  como (2), com MM8

A variante b ANINHA as outras duas: na (H),
    h2*(Selic - meta - MM) + h3*(rr_10a - MM)
com h3 = -h2 devolve a ancora crua (0) e com h3 = 0 devolve a media (1 ou 2). O que a
regressao diz de h3 e a resposta direta a "o 10 anos cru ou o suavizado?".

O que mede:
    (a) erro fora da amostra, estimacao recursiva a partir de 2016T1, cada equacao
        sozinha com os insumos dela observados, em 1, 4 e 8 trimestres;
    (b) os pesos da (R) contra os intervalos do BC e o h2 da (H);
    (c) quanto 1 p.p. permanente a mais na NTN-B de 10 anos move Selic e hiato do
        sistema (R)+(H), com expectativa e meta paradas.

Rodar:  uv run python -m analytics.brasil.structural_model.experimentos.ancora_2026-10-30.ancora
        (o nome com hifen nao importa como modulo: rodar pelo caminho do arquivo)
"""
from __future__ import annotations

import pickle
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels.api as sm

from analytics.brasil.structural_model import panel
from analytics.brasil.structural_model.equations import taylor

AQUI = Path(__file__).parent
CACHE = AQUI / "data" / "panel_2026-10-30.pkl"

VARIANTES = {
    "0":  dict(k=1, dev=False, rot="10 anos cru (hoje)"),
    "1":  dict(k=4, dev=False, rot="MM 4 trimestres"),
    "2":  dict(k=8, dev=False, rot="MM 8 trimestres"),
    "1b": dict(k=4, dev=True,  rot="MM4 + desvio na IS"),
    "2b": dict(k=8, dev=True,  rot="MM8 + desvio na IS"),
}
CRISES = taylor.CRISES
OOS_INI = pd.Period("2016Q1", "Q")
HS = (1, 4, 8)


def painel() -> pd.DataFrame:
    if CACHE.exists():
        return pickle.loads(CACHE.read_bytes())
    df = panel.construir()
    CACHE.parent.mkdir(exist_ok=True)
    CACHE.write_bytes(pickle.dumps(df))
    return df


def matriz(df: pd.DataFrame, k: int) -> pd.DataFrame:
    """Uma matriz com as colunas das duas equacoes sob a janela `k`."""
    df = df[df["completo"].astype(bool)]
    mm = df["rr_10a"].rolling(k).mean()
    anc = mm + df["meta_12m"]
    d = pd.DataFrame(index=df.index)
    d["selic"] = df["selic"]
    d["anc"] = anc
    d["y"] = df["selic"] - anc                       # (R): desvio da ancora; (H): o aperto
    d["y1"] = d["y"].shift(1)
    d["y2"] = d["y"].shift(2)
    d["dI"] = df["pi_e"] - df["meta_12m"]
    d["hiato"] = df["hiato"]
    d["h_l1"] = df["hiato"].shift(1)
    d["ap_l"] = d["y"].shift(1)
    d["dev_l"] = (df["rr_10a"] - mm).shift(1)
    for c, (a, b) in CRISES.items():
        d[c] = ((d.index >= a) & (d.index <= b)).astype(float)
    return d


def _ols(y, X):
    return sm.OLS(y, X).fit(cov_type="HAC", cov_kwds={"maxlags": 4})


def est_R(d: pd.DataFrame) -> tuple[dict, list[str]]:
    reg = ["y1", "y2", "dI"] + [c for c in CRISES if d[c].sum() > 0]
    r = _ols(d["y"].to_numpy(float), d[reg].to_numpy(float))
    return dict(zip(reg, r.params)), reg, r


def est_H(d: pd.DataFrame, dev: bool):
    reg = ["h_l1", "ap_l"] + (["dev_l"] if dev else []) + [c for c in CRISES if d[c].sum() > 0]
    r = _ols(d["hiato"].to_numpy(float), d[reg].to_numpy(float))
    return dict(zip(reg, r.params)), reg, r


def amostra_comum(df: pd.DataFrame) -> pd.Index:
    ix = None
    for v in VARIANTES.values():
        d = matriz(df, v["k"])
        a = d[["y", "y1", "y2", "dI", "hiato", "h_l1", "ap_l", "dev_l"]].dropna().index
        ix = a if ix is None else ix.intersection(a)
    return ix


# ── (a) fora da amostra ─────────────────────────────────────────────────────
def prever_R(c: dict, d: pd.DataFrame, t0: int, h: int) -> float:
    """Selic em t0+h-1 com a (R) solta a partir de t0, insumos observados."""
    y1, y2 = d["y1"].iloc[t0], d["y2"].iloc[t0]
    for j in range(h):
        t = t0 + j
        v = c["y1"] * y1 + c["y2"] * y2 + c["dI"] * d["dI"].iloc[t]
        v += sum(c.get(cr, 0.0) * d[cr].iloc[t] for cr in CRISES)
        y2, y1 = y1, v
    return float(d["anc"].iloc[t0 + h - 1] + y1)


def prever_H(c: dict, d: pd.DataFrame, t0: int, h: int) -> float:
    """Hiato em t0+h-1 com a (H) solta, a Selic (e o aperto) observados."""
    hl = d["h_l1"].iloc[t0]
    for j in range(h):
        t = t0 + j
        v = c["h_l1"] * hl + c["ap_l"] * d["ap_l"].iloc[t]
        v += c.get("dev_l", 0.0) * d["dev_l"].iloc[t]
        v += sum(c.get(cr, 0.0) * d[cr].iloc[t] for cr in CRISES)
        hl = v
    return float(hl)


def fora_da_amostra(df: pd.DataFrame, comum: pd.Index) -> dict:
    out = {}
    for nome, v in VARIANTES.items():
        d = matriz(df, v["k"]).loc[comum]
        idx = list(d.index)
        erros = {("R", h): [] for h in HS} | {("H", h): [] for h in HS}
        alvos = {("R", h): [] for h in HS} | {("H", h): [] for h in HS}
        for T in [p for p in idx if p >= OOS_INI - 1]:
            pos = idx.index(T)
            tr = d.iloc[: pos + 1]
            cR, _, _ = est_R(tr)
            cH, _, _ = est_H(tr, v["dev"])
            for h in HS:
                t_alvo = pos + h
                if t_alvo >= len(idx):
                    continue
                eR = prever_R(cR, d, pos + 1, h) - d["selic"].iloc[t_alvo]
                eH = prever_H(cH, d, pos + 1, h) - d["hiato"].iloc[t_alvo]
                erros[("R", h)].append(eR)
                erros[("H", h)].append(eH)
                alvos[("R", h)].append(idx[t_alvo])
                alvos[("H", h)].append(idx[t_alvo])
        out[nome] = {kk: pd.Series(e, index=alvos[kk]) for kk, e in erros.items()}
    return out


def fora_da_amostra_segurado(df: pd.DataFrame, comum: pd.Index) -> dict:
    """O sistema (R)+(H) solto, como o simulador o roda por padrao.

    Na origem T, NTN-B de 10 anos, Focus e meta ficam paradas no valor de T (a regra
    "Observado" das caixas do simulador); a Selic sai da (R) e o hiato le essa Selic.
    E o teste que separa uma vantagem que so existe conhecendo o caminho realizado da
    NTN-B -- que o mercado forma olhando a propria Selic -- de uma vantagem utilizavel.
    """
    fechado = df[df["completo"].astype(bool)]
    out = {}
    for nome, v in VARIANTES.items():
        k = v["k"]
        d = matriz(df, k).loc[comum]
        idx = list(d.index)
        er = {("R", h): {} for h in HS} | {("H", h): {} for h in HS}
        for T in [p for p in idx if p >= OOS_INI - 1]:
            pos = idx.index(T)
            if pos + 1 >= len(idx):
                continue
            tr = d.iloc[: pos + 1]
            cR, _, _ = est_R(tr)
            cH, _, _ = est_H(tr, v["dev"])
            rr_hist = list(fechado["rr_10a"].loc[:T].to_numpy(float))
            rr_T, dI_T, meta_T = rr_hist[-1], d["dI"].iloc[pos], fechado["meta_12m"].loc[T]
            y1, y2 = d["y"].iloc[pos], d["y"].iloc[pos - 1]
            ap_prev, dev_prev = d["y"].iloc[pos], float(rr_T - np.mean(rr_hist[-k:]))
            h_prev = d["hiato"].iloc[pos]
            for j in range(max(HS)):
                t = pos + 1 + j
                if t >= len(idx):
                    break
                rr_hist.append(rr_T)
                mm = float(np.mean(rr_hist[-k:]))
                anc = mm + meta_T
                y = cR["y1"] * y1 + cR["y2"] * y2 + cR["dI"] * dI_T
                y += sum(cR.get(c, 0.0) * d[c].iloc[t] for c in CRISES)
                selic = anc + y
                h = cH["h_l1"] * h_prev + cH["ap_l"] * ap_prev + cH.get("dev_l", 0.0) * dev_prev
                h += sum(cH.get(c, 0.0) * d[c].iloc[t] for c in CRISES)
                if j + 1 in HS:
                    er[("R", j + 1)][idx[t]] = selic - d["selic"].iloc[t]
                    er[("H", j + 1)][idx[t]] = h - d["hiato"].iloc[t]
                y2, y1 = y1, y
                ap_prev, dev_prev, h_prev = y, rr_T - mm, h
        out[nome] = {kk: pd.Series(e) for kk, e in er.items()}
    return out


def _rmse(s: pd.Series, sem_covid: bool = False) -> float:
    if sem_covid:
        s = s[(s.index < pd.Period("2020Q1", "Q")) | (s.index > pd.Period("2021Q2", "Q"))]
    return float(np.sqrt((s ** 2).mean()))


# ── (c) 1 p.p. permanente na NTN-B ──────────────────────────────────────────
def choque_ntnb(df: pd.DataFrame, cR: dict, cH: dict, k: int, H: int = 12) -> pd.DataFrame:
    """Diferenca de Selic e hiato entre a NTN-B +1 p.p. e o cenario base.

    Sistema (R)+(H) em diferencas contra o base: expectativa e meta paradas, entao o
    dI nao muda e so a ancora e o desvio carregam o choque. A media movel absorve o
    choque aos poucos: na janela k, j/k dele depois de j trimestres.
    """
    sel, hia = [0.0, 0.0], [0.0]
    dev_path, anc_path, linhas = [], [], []
    for j in range(H):
        frac = min(1.0, (j + 1) / k)
        anc = frac                       # quanto a ancora andou
        dev = 1.0 - frac                 # o cru andou 1, a media `frac`
        y1, y2 = sel[-1] - anc_path[-1] if anc_path else 0.0, \
            (sel[-2] - anc_path[-2]) if len(anc_path) > 1 else 0.0
        y = cR["y1"] * y1 + cR["y2"] * y2
        s = anc + y
        ap_l = (sel[-1] - anc_path[-1]) if anc_path else 0.0
        dv_l = dev_path[-1] if dev_path else 0.0
        h = cH["h_l1"] * hia[-1] + cH["ap_l"] * ap_l + cH.get("dev_l", 0.0) * dv_l
        sel.append(s); hia.append(h); anc_path.append(anc); dev_path.append(dev)
        linhas.append({"j": j + 1, "selic": s, "hiato": h, "ancora": anc})
    return pd.DataFrame(linhas).set_index("j")


def main() -> None:
    df = painel()
    comum = amostra_comum(df)
    print(f"amostra comum: {comum[0]} a {comum[-1]}, {len(comum)} trimestres\n")

    ic = taylor.BCB_IC
    print("(b) pesos na amostra comum")
    print(f"{'var':<5}{'t1':>8}{'t2':>8}{'t3(LP)':>8}{'LB4 R':>7} |{'h1':>7}{'h2':>8}{'t h2':>7}"
          f"{'h3 dev':>8}{'t h3':>7}{'R2 H':>7}{'LB4 H':>7}")
    est = {}
    for nome, v in VARIANTES.items():
        d = matriz(df, v["k"]).loc[comum]
        cR, rR, oR = est_R(d)
        cH, rH, oH = est_H(d, v["dev"])
        est[nome] = (cR, cH)
        lp = cR["dI"] / (1 - cR["y1"] - cR["y2"])
        from statsmodels.stats.diagnostic import acorr_ljungbox
        lbR = acorr_ljungbox(oR.resid, lags=[4], return_df=True)["lb_pvalue"].iloc[0]
        lbH = acorr_ljungbox(oH.resid, lags=[4], return_df=True)["lb_pvalue"].iloc[0]
        tH = dict(zip(rH, oH.tvalues))
        r2H = 1 - (oH.resid ** 2).sum() / ((d["hiato"] - d["hiato"].mean()) ** 2).sum()
        print(f"{nome:<5}{cR['y1']:>8.3f}{cR['y2']:>8.3f}{lp:>8.2f}{lbR:>7.3f} |"
              f"{cH['h_l1']:>7.3f}{cH['ap_l']:>8.4f}{tH['ap_l']:>7.2f}"
              f"{cH.get('dev_l', float('nan')):>8.4f}{tH.get('dev_l', float('nan')):>7.2f}"
              f"{r2H:>7.3f}{lbH:>7.3f}")
    print(f"BC   t1 {ic['t1']}  t2 {ic['t2']}  t3 {ic['t3']}\n")

    print("(a) fora da amostra, RMSE (estimacao recursiva desde 2016T1; entre parenteses sem 2020T1-2021T2)")
    oos = fora_da_amostra(df, comum)
    base = oos["0"]
    for eq, nomeq in (("R", "Selic"), ("H", "hiato")):
        print(f"  {nomeq}")
        for nome in VARIANTES:
            cel = []
            for h in HS:
                e = oos[nome][(eq, h)]
                rel = _rmse(e) / _rmse(base[(eq, h)]) - 1
                cel.append(f"h{h} {_rmse(e):5.3f} ({_rmse(e, True):5.3f}) {rel:+6.1%}")
            print(f"    {nome:<3} " + "   ".join(cel) + f"   n={len(oos[nome][(eq, 1)])}")

    print("\n(a2) o sistema (R)+(H) solto, NTN-B, Focus e meta paradas na origem (como o simulador)")
    oos2 = fora_da_amostra_segurado(df, comum)
    base2 = oos2["0"]
    for eq, nomeq in (("R", "Selic"), ("H", "hiato")):
        print(f"  {nomeq}")
        for nome in VARIANTES:
            cel = []
            for h in HS:
                e = oos2[nome][(eq, h)]
                rel = _rmse(e) / _rmse(base2[(eq, h)]) - 1
                cel.append(f"h{h} {_rmse(e):5.3f} ({_rmse(e, True):5.3f}) {rel:+6.1%}")
            print(f"    {nome:<3} " + "   ".join(cel) + f"   n={len(oos2[nome][(eq, 1)])}")

    print("\n(c) NTN-B de 10 anos +1 p.p. permanente: diferenca contra o base (p.p.)")
    for nome, v in VARIANTES.items():
        cR, cH = est[nome]
        c = choque_ntnb(df, cR, cH, v["k"])
        print(f"  {nome:<3} Selic  " + " ".join(f"{c.loc[j, 'selic']:+.2f}" for j in (1, 2, 4, 8, 12))
              + "   hiato " + " ".join(f"{c.loc[j, 'hiato']:+.3f}" for j in (1, 2, 4, 8, 12)))
    print("       (trimestres 1, 2, 4, 8, 12)")

    ult = matriz(df, 1).dropna(subset=["y"]).index[-1]
    print(f"\nultimo trimestre fechado: {ult}")
    for k in (1, 4, 8):
        d = matriz(df, k)
        print(f"  k={k}: ancora {d['anc'].loc[ult]:.2f}  aperto {d['y'].loc[ult]:+.2f}"
              f"  desvio cru-MM {matriz(df, 1)['anc'].loc[ult] - d['anc'].loc[ult]:+.2f}")


if __name__ == "__main__":
    sys.exit(main())
