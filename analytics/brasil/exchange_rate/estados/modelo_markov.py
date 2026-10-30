"""Fase 2 — Markov oculto supervisionado de uma camada para os estados do câmbio USD/BRL.

Uso:  uv run python analytics/brasil/exchange_rate/estados/modelo_markov.py

Classes (5): Q0, Q1, Q2, Q4u (Q4 ↑ dólar), Q4d (Q4 ↓ dólar). As fases do Q1 não viram classe; o Q3 entra
como covariável (dummy de novembro–dezembro).

- Métricas: todas causais (só informação até o dia t): janelas para trás, z-score contra a média/desvio
  dos 252 pregões anteriores (régua de 1 ano) e dos 1260 anteriores (régua de 5 anos), e o nível absoluto.
- Emissão: logit multinomial L2 com pesos de classe balanceados. Com pesos balanceados o logit estima o
  posterior sob prior uniforme, então p(x|y) ∝ p_bal(y|x): esse é o termo de emissão do HMM.
- Transição: contada nos rótulos diários de treino, com pseudo-contagem pequena só nas transições que
  ocorrem nos rótulos; transição que nunca ocorre fica proibida (probabilidade zero).
- Validação: um ano fora por vez (21 dobras), e do treino sai todo trecho rotulado que toca o ano de
  teste (purga), para nenhum episódio ficar dos dois lados.
- Ablação: (a) câmbio + vol implícita + prêmio onshore (+ dólar contra emergentes e a dummy Q3);
  (b) (a) + CDS; (c) (b) + juros (DI 1 ano, inclinação 1–5 anos, NTN-B 10 anos).

Saídas na pasta: prob_estados_diaria.csv e resultado_fase2.xlsx.
"""
from __future__ import annotations

import warnings
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import balanced_accuracy_score, confusion_matrix, log_loss
from sklearn.preprocessing import StandardScaler

warnings.filterwarnings("ignore")
AQUI = Path(__file__).resolve().parent
INICIO, FIM = "2006-01-02", "2026-10-28"
CLASSES = ["Q0", "Q1", "Q2", "Q4u", "Q4d"]
C_REG = 0.1          # regularização do logit (L2), valor padrão
GRADE_C = (0.001, 0.003, 0.01, 0.1)
GRADE_TAU = (0.02, 0.05, 0.1, 0.2, 0.35, 0.5, 1.0)  # têmpera da emissão no filtro: E**tau
PSEUDO = 0.1         # pseudo-contagem da matriz de transição
H_PROJ = (21, 63)
JANELAS_SOBREP = {   # episódios de sobreposição analisados à parte
    "2008 (crise global + Lehman + eleição EUA)": ("2008-08-08", "2009-03-03"),
    "2015 a fev/2016 (fiscal + perda do grau)": ("2015-07-23", "2016-03-02"),
    "2020 (Covid + Moro + fiscal + eleição EUA)": ("2020-01-21", "2020-11-30"),
    "2021 (fiscal + 7/9 + furo do teto)": ("2021-07-29", "2021-12-30"),
    "fim de 2024 (fiscal + pacote + Copom + dezembro)": ("2024-09-01", "2025-01-17"),
}


# ----------------------------------------------------------------------------------------------- dados
def _sql(schema: str, q: str) -> pd.DataFrame:
    from utils import explore as ex

    return pd.read_sql(q, ex._conn(schema))


def carregar() -> dict[str, pd.Series]:
    s = {}
    p = _sql("macro_brasil", "select date, value from cmb_ptax where name='ptax_venda' and date>='2000-01-01'")
    s["ptax"] = p.set_index(pd.to_datetime(p.date)).value.astype(float)
    v = _sql("macro_brasil", "select date, prazo, value from cmb_vol_implicita")
    v = v.pivot(index="date", columns="prazo", values="value")
    v.index = pd.to_datetime(v.index)
    for k in ["1M", "2M", "3M", "6M"]:
        s[f"vol{k}"] = v[k].astype(float)
    br = _sql("macro_brasil", "select date, curve, tenor, value from br_interest_rate where "
              "(curve='CUPOM_LIMPO' and tenor='3M') or (curve='JUROS_USD' and tenor='3M') or "
              "(curve='DIPRE' and tenor in ('12M','60M')) or (curve='NTNBJS' and tenor='120M')")
    br["k"] = br.curve + "_" + br.tenor
    br = br.pivot(index="date", columns="k", values="value").astype(float)
    br.index = pd.to_datetime(br.index)
    s["cupom3m"], s["usd3m"] = br["CUPOM_LIMPO_3M"], br["JUROS_USD_3M"]
    s["di1y"], s["di5y"], s["ntnb10"] = br["DIPRE_12M"], br["DIPRE_60M"], br["NTNBJS_120M"]
    tb = _sql("macro_us", "select date, value from us_interest_rate where curve='US_TREASURY' and tenor='3M' "
              "and date>='2000-01-01'")
    s["tbill3m"] = tb.set_index(pd.to_datetime(tb.date)).value.astype(float)
    cds = _sql("macro_brasil", "select date, value from cmb_risco_pais where name='cds_5y_usd'")
    s["cds"] = cds.set_index(pd.to_datetime(cds.date)).value.astype(float)
    em = _sql("macro_international", "select date, value from cmb_dollar_index_em where name='dxy_em'")
    s["dxy_em"] = em.set_index(pd.to_datetime(em.date)).value.astype(float)
    return s


def _z(x: pd.Series, w: int) -> pd.Series:
    """z-score contra os w pregões ANTERIORES (o próprio dia não entra na régua)."""
    r = x.shift(1).rolling(w, min_periods=min(w, 63))
    return (x - r.mean()) / r.std()


def metricas(s: dict[str, pd.Series]) -> pd.DataFrame:
    grid = s["ptax"].index
    g = {k: v.reindex(grid.union(v.index)).sort_index().ffill().reindex(grid) for k, v in s.items()}
    f = pd.DataFrame(index=grid)
    lp = np.log(g["ptax"])
    ret = lp.diff()
    rv21 = ret.rolling(21).std() * np.sqrt(252) * 100
    vf = g["vol1M"].fillna(g["vol2M"])
    front = (vf + g["vol2M"]) / 2
    v3 = g["vol3M"]
    # --- (a) câmbio
    for k in (1, 5, 21, 63):
        f[f"a_fx_r{k}"] = (lp - lp.shift(k)) / (v3.shift(k) / 100 * np.sqrt(k / 252))
    f["a_fx_ma63"] = lp - lp.rolling(63).mean()
    f["a_fx_ma252"] = lp - lp.rolling(252).mean()
    f["a_fx_ma252_z5"] = _z(f["a_fx_ma252"], 1260)
    f["a_rv21"] = rv21
    # --- (a) vol implícita
    f["a_vol3m"] = v3
    f["a_vol3m_z1"] = _z(v3, 252)
    f["a_vol3m_z5"] = _z(v3, 1260)
    f["a_vol3m_d21"] = v3 - v3.shift(21)
    f["a_vol_termo"] = front - g["vol6M"]
    f["a_vol_termo_z1"] = _z(f["a_vol_termo"], 252)
    f["a_vol_vrp"] = front - rv21
    f["a_vol_evento"] = np.sqrt(np.maximum(g["vol2M"] ** 2 - g["vol6M"] ** 2, 0) * 2 / 12)
    # --- (a) prêmio onshore: cupom limpo 3M − juro em dólar 3M (T-bill 3M antes de 21/02/2008)
    usd = g["usd3m"].where(grid >= "2008-02-21", g["tbill3m"])
    prem = g["cupom3m"] - usd
    dev = prem - prem.shift(1).rolling(252, min_periods=63).median()
    # sazonalidade: média do desvio no mesmo mês-calendário dos anos ANTERIORES
    mes, ano = grid.month, grid.year
    saz = pd.Series(np.nan, index=grid)
    dfm = pd.DataFrame({"dev": dev, "mes": mes, "ano": ano})
    medias = dfm.groupby(["ano", "mes"]).dev.mean().unstack()
    acum = medias.expanding().mean().shift(1)  # só anos anteriores
    for (a, m), val in acum.stack().items():
        saz[(ano == a) & (mes == m)] = val
    f["a_prem"] = prem
    f["a_prem_dev_sa"] = dev - saz.fillna(0)
    f["a_prem_z5"] = _z(prem, 1260)
    # --- (a) dólar contra emergentes
    le = np.log(g["dxy_em"])
    sd_em = le.diff().shift(1).rolling(252, min_periods=63).std()
    for k in (21, 63):
        f[f"a_em_r{k}"] = (le - le.shift(k)) / (sd_em * np.sqrt(k))
    f["a_q3"] = (grid.month >= 11).astype(float)
    # --- (b) CDS
    lc = np.log(g["cds"])
    f["b_cds"] = g["cds"]
    f["b_cds_z1"] = _z(lc, 252)
    f["b_cds_z5"] = _z(lc, 1260)
    f["b_cds_d5"] = lc - lc.shift(5)
    f["b_cds_d21"] = lc - lc.shift(21)
    # --- (c) juros
    incl = g["di5y"] - g["di1y"]
    for nome, x in (("di1y", g["di1y"]), ("incl", incl), ("ntnb10", g["ntnb10"])):
        f[f"c_{nome}"] = x
        f[f"c_{nome}_d21"] = x - x.shift(21)
        f[f"c_{nome}_z1"] = _z(x, 252)
    return f.loc[INICIO:FIM]


BLOCOS = {"a": ("a_",), "b": ("a_", "b_"), "c": ("a_", "b_", "c_")}
NOME_BLOCO = {"a": "(a) câmbio + vol + prêmio onshore", "b": "(b) = (a) + CDS", "c": "(c) = (b) + juros"}


# ----------------------------------------------------------------------------------------------- rótulos
def rotulos() -> pd.DataFrame:
    d = pd.read_csv(AQUI / "rotulos_diarios.csv", keep_default_na=False)
    d["date"] = pd.to_datetime(d["date"])
    d["classe"] = d["estado"]
    q4 = d["estado"] == "Q4"
    d.loc[q4, "classe"] = np.where(d.loc[q4, "direcao"].str.startswith("↑"), "Q4u", "Q4d")
    d["y"] = d["classe"].map({c: i for i, c in enumerate(CLASSES)})
    d["ids"] = d["ids_cobrindo"].map(lambda s: set(s.split(" | ")) if s else set())
    return d.set_index("date")


# ----------------------------------------------------------------------------------------------- HMM
def transicao(y: np.ndarray, consecutivo: np.ndarray, permitido: np.ndarray) -> np.ndarray:
    k = len(CLASSES)
    n = np.zeros((k, k))
    for a, b, ok in zip(y[:-1], y[1:], consecutivo[1:]):
        if ok:
            n[a, b] += 1
    n = (n + PSEUDO) * permitido
    return n / n.sum(1, keepdims=True)


def estacionaria(A: np.ndarray) -> np.ndarray:
    w, v = np.linalg.eig(A.T)
    p = np.real(v[:, np.argmin(np.abs(w - 1))])
    return p / p.sum()


def filtrar_suavizar(E: np.ndarray, A: np.ndarray, p0: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    T, k = E.shape
    al = np.zeros((T, k))
    c = np.zeros(T)
    prev = p0
    for t in range(T):
        a = (prev @ A if t else p0) * E[t]
        c[t] = a.sum()
        al[t] = a / c[t]
        prev = al[t]
    be = np.ones((T, k))
    for t in range(T - 2, -1, -1):
        b = A @ (E[t + 1] * be[t + 1])
        be[t] = b / b.sum()
    sm = al * be
    return al, sm / sm.sum(1, keepdims=True)


def emissao(Xtr, ytr, Xte, c_reg=C_REG):
    sc = StandardScaler().fit(Xtr)
    Ztr = np.nan_to_num(sc.transform(Xtr))
    Zte = np.nan_to_num(sc.transform(Xte))
    m = LogisticRegression(C=c_reg, class_weight="balanced", max_iter=5000).fit(Ztr, ytr)
    pb = np.zeros((len(Zte), len(CLASSES)))
    pb[:, m.classes_] = m.predict_proba(Zte)
    return np.clip(pb, 1e-6, None), m, sc


# ----------------------------------------------------------------------------------------------- validação
def emissoes_oos(X: pd.DataFrame, lab: pd.DataFrame, permitido: np.ndarray, c_reg: float) -> list:
    """Um ano fora por vez, com purga dos trechos que tocam o ano de teste. Devolve, por ano de teste,
    a emissão fora da amostra, a matriz de transição e o prior do treino daquela dobra."""
    y = lab["y"].values
    dobras = []
    for ano in sorted(X.index.year.unique()):
        te = X.index.year == ano
        ids_te = set().union(*lab.loc[te, "ids"])
        purga = lab["ids"].map(lambda s: bool(s & ids_te)).values
        tr = ~te & ~purga
        pb, _, _ = emissao(X.values[tr], y[tr], X.values[te], c_reg)
        prior = np.bincount(y[tr], minlength=len(CLASSES)) / tr.sum()
        A = transicao(np.where(tr, y, -1), np.r_[False, tr[1:] & tr[:-1]], permitido)
        dobras.append((te, pb, A, prior))
    return dobras


def montar(dobras: list, idx: pd.DatetimeIndex, tau: float) -> dict[str, pd.DataFrame]:
    """Probabilidades fora da amostra: só logit, filtrada e suavizada, com a emissão elevada a tau."""
    out = {k: np.zeros((len(idx), len(CLASSES))) for k in ("logit", "filtrada", "suavizada")}
    for te, pb, A, prior in dobras:
        f, s = filtrar_suavizar(pb ** tau, A, estacionaria(A))
        lg = pb * prior
        out["logit"][te] = lg / lg.sum(1, keepdims=True)
        out["filtrada"][te] = f
        out["suavizada"][te] = s
    return {k: pd.DataFrame(v, index=idx, columns=CLASSES) for k, v in out.items()}


def ll_bal(P: np.ndarray, y: np.ndarray) -> float:
    """Log-loss balanceado: média, entre as classes presentes, do log-loss dentro de cada classe.
    É a métrica de escolha porque os pesos de classe tratam as cinco classes como igualmente importantes;
    o log-loss comum premia prever Q0 e Q4 sempre (44% + 34% dos dias) e nunca Q1/Q2."""
    nll = -np.log(np.clip(P[np.arange(len(y)), y], 1e-9, 1))
    return float(np.mean([nll[y == i].mean() for i in np.unique(y)]))


def avaliar(P: pd.DataFrame, y: np.ndarray, mask=None) -> dict:
    if mask is not None:
        P, y = P[mask], y[mask]
    pred = P.values.argmax(1)
    rec = {c: (pred[y == i] == i).mean() if (y == i).any() else np.nan for i, c in enumerate(CLASSES)}
    return {"n": len(y), "acerto": (pred == y).mean(),
            "acerto_balanceado": balanced_accuracy_score(y, pred),
            "log_loss": log_loss(y, np.clip(P.values, 1e-9, 1), labels=range(len(CLASSES))),
            "log_loss_bal": ll_bal(P.values, y),
            **{f"recall_{c}": v for c, v in rec.items()}}


def confusao(P: pd.DataFrame, y: np.ndarray, mask=None) -> pd.DataFrame:
    if mask is not None:
        P, y = P[mask], y[mask]
    cm = confusion_matrix(y, P.values.argmax(1), labels=range(len(CLASSES)))
    return pd.DataFrame(cm, index=[f"rótulo {c}" for c in CLASSES], columns=[f"previsto {c}" for c in CLASSES])


# ----------------------------------------------------------------------------------------------- régua antiga
def regua_antiga(idx: pd.DatetimeIndex) -> pd.Series:
    o = pd.read_csv(AQUI / "classificacao_regra_antiga.csv", encoding="utf-8-sig", keep_default_na=False)
    o["date"] = pd.to_datetime(o["date"])
    m = o["estado"].map(lambda e: "Q0" if e == "calmo" else e[:2])
    m = np.where(m == "Q4", np.where(o["direcao"].str.startswith("↓"), "Q4d", "Q4u"), m)
    return pd.Series(m, index=o["date"]).reindex(idx)


# ----------------------------------------------------------------------------------------------- main
def main() -> None:
    lab = rotulos()
    X_all = metricas(carregar()).reindex(lab.index)
    y = lab["y"].values
    k = len(CLASSES)
    # transições permitidas: as que ocorrem nos rótulos (mais a permanência)
    cont = np.zeros((k, k))
    for a, b in zip(y[:-1], y[1:]):
        cont[a, b] += 1
    permitido = ((cont > 0) | np.eye(k, dtype=bool)).astype(float)

    # grade: regularização do logit x têmpera da emissão (as métricas são janelas sobrepostas, então dias
    # vizinhos não são observações independentes; sem têmpera o filtro conta a mesma evidência 20 vezes)
    grade, dobras = [], {}
    for b, pref in BLOCOS.items():
        cols = [c for c in X_all.columns if c.startswith(pref)]
        for c_reg in GRADE_C:
            dobras[(b, c_reg)] = emissoes_oos(X_all[cols], lab, permitido, c_reg)
            for tau in GRADE_TAU:
                P = montar(dobras[(b, c_reg)], lab.index, tau)
                for tipo in ("filtrada", "suavizada") + (("logit",) if tau == GRADE_TAU[0] else ()):
                    grade.append({"bloco": b, "C": c_reg, "tau": tau if tipo != "logit" else np.nan,
                                  "n_metricas": len(cols), "probabilidade": tipo, **avaliar(P[tipo], y)})
        print(f"bloco {b}: {len(cols)} métricas ok")
    grade = pd.DataFrame(grade)
    # hiperparâmetros comuns aos três blocos (para a ablação ser justa): menor log-loss BALANCEADO médio
    # da filtrada
    gf = grade[grade.probabilidade == "filtrada"].groupby(["C", "tau"]).log_loss_bal.mean()
    c_ok, tau_ok = gf.idxmin()
    abl = grade[((grade.C == c_ok) & ((grade.tau == tau_ok) | grade.tau.isna()))].copy()
    abl["bloco"] = abl["bloco"].map(NOME_BLOCO)
    filt = abl[abl.probabilidade == "filtrada"].set_index("bloco")
    melhor = min(BLOCOS, key=lambda b: filt.loc[NOME_BLOCO[b], "log_loss_bal"])
    oos = {b: montar(dobras[(b, c_ok)], lab.index, tau_ok) for b in BLOCOS}
    P_f, P_s = oos[melhor]["filtrada"], oos[melhor]["suavizada"]
    print(f"escolhidos C={c_ok}, tau={tau_ok}, bloco={melhor}")

    # ablação ano a ano: em quantos dos 21 anos de teste cada bloco melhora o log-loss do anterior
    anos = lab.index.year
    pa = []
    for ano in sorted(anos.unique()):
        msk = anos == ano
        linha = {"ano": ano}
        for b in BLOCOS:
            for tipo in ("logit", "filtrada"):
                P = oos[b][tipo][msk].values
                linha[f"{b}_{tipo}"] = ll_bal(P, y[msk])
        pa.append(linha)
    por_ano = pd.DataFrame(pa)
    resumo_abl = []
    for tipo in ("logit", "filtrada"):
        for x, z in (("a", "b"), ("b", "c"), ("a", "c")):
            dlt = por_ano[f"{z}_{tipo}"] - por_ano[f"{x}_{tipo}"]
            resumo_abl.append({"comparação": f"{z} contra {x}", "probabilidade": tipo,
                               "anos em que melhora (de 21)": int((dlt < 0).sum()),
                               "Δ log-loss balanceado médio por ano": dlt.mean(), "Δ mediano": dlt.median()})
    resumo_abl = pd.DataFrame(resumo_abl)
    print(resumo_abl.round(4).to_string())

    # separação par a par: AUC de p_i/(p_i+p_j) nos dias rotulados i ou j (0,5 = não separa)
    from sklearn.metrics import roc_auc_score
    pares = []
    for tipo in ("logit", "filtrada"):
        P = oos[melhor][tipo].values
        for i in range(k):
            for j in range(i + 1, k):
                m_ = (y == i) | (y == j)
                sc_ = P[m_, i] / (P[m_, i] + P[m_, j])
                pares.append({"probabilidade": tipo, "par": f"{CLASSES[i]} × {CLASSES[j]}",
                              "AUC": roc_auc_score(y[m_] == i, sc_), "n_dias": int(m_.sum())})
    pares = pd.DataFrame(pares)
    # acerto por fase do Q1 (a fase não é classe, mas diz onde o Q1 é visível)
    fases = []
    pred_s = P_s.values.argmax(1)
    for fz in ("antes", "evento", "depois"):
        m_ = (lab["classe"] == "Q1").values & (lab["fase"] == fz).values
        fases.append({"fase do Q1": fz, "n_dias": int(m_.sum()), "acerto (suavizada)": (pred_s[m_] == 1).mean(),
                      "p média de Q1 (suavizada)": P_s.values[m_, 1].mean()})
    fases = pd.DataFrame(fases)
    print(pares.round(3).to_string())
    print(fases.round(3).to_string())

    # sobreposição
    sob = []
    for nome, (a, z) in JANELAS_SOBREP.items():
        msk = (lab.index >= a) & (lab.index <= z)
        for tipo, P in (("filtrada", P_f), ("suavizada", P_s)):
            sob.append({"janela": nome, "probabilidade": tipo, **avaliar(P, y, msk)})
    for v in (0, 1):
        msk = lab["sobreposicao"].values == v
        sob.append({"janela": f"todos os dias com sobreposicao={v}", "probabilidade": "filtrada",
                    **avaliar(P_f, y, msk)})
    sob = pd.DataFrame(sob)
    conf_sob = {nome: confusao(P_f, y, (lab.index >= a) & (lab.index <= z))
                for nome, (a, z) in JANELAS_SOBREP.items()}

    # régua antiga
    ant = regua_antiga(lab.index)
    ya = ant.map({c: i for i, c in enumerate(CLASSES)}).values
    ok = ~np.isnan(ya)
    pa = ya[ok].astype(int)
    regua = pd.DataFrame([
        {"classificação": "régua antiga (regra sobre métricas)", "acerto": (pa == y[ok]).mean(),
         "acerto_balanceado": balanced_accuracy_score(y[ok], pa)},
        {"classificação": f"modelo {melhor}, filtrada, fora da amostra",
         "acerto": (P_f.values.argmax(1) == y).mean(), "acerto_balanceado": balanced_accuracy_score(y, P_f.values.argmax(1))},
        {"classificação": f"modelo {melhor}, suavizada, fora da amostra",
         "acerto": (P_s.values.argmax(1) == y).mean(), "acerto_balanceado": balanced_accuracy_score(y, P_s.values.argmax(1))},
    ])
    for nome, (a, z) in JANELAS_SOBREP.items():
        msk = ok & (lab.index >= a) & (lab.index <= z)
        regua[f"acerto {nome[:4]}"] = [(ya[msk].astype(int) == y[msk]).mean(),
                                      (P_f.values.argmax(1)[msk] == y[msk]).mean(),
                                      (P_s.values.argmax(1)[msk] == y[msk]).mean()]
    conf_antiga = pd.DataFrame(confusion_matrix(y[ok], pa, labels=range(k)),
                               index=[f"rótulo {c}" for c in CLASSES], columns=[f"régua {c}" for c in CLASSES])

    # modelo final: todos os dados, melhor bloco
    cols = [c for c in X_all.columns if c.startswith(BLOCOS[melhor])]
    pb, m, sc = emissao(X_all[cols].values, y, X_all[cols].values, c_ok)
    A = transicao(y, np.ones(len(y), bool), permitido)
    F, S = filtrar_suavizar(pb ** tau_ok, A, estacionaria(A))
    dur = 1 / (1 - np.diag(A))
    trans = pd.DataFrame(A, index=[f"de {c}" for c in CLASSES], columns=[f"para {c}" for c in CLASSES])
    trans["duração típica (pregões)"] = dur
    trans["permanência p_ficar"] = np.diag(A)
    proj = [{"horizonte (pregões)": 0, **dict(zip(CLASSES, F[-1]))}]
    for h in H_PROJ:
        proj.append({"horizonte (pregões)": h, **dict(zip(CLASSES, F[-1] @ np.linalg.matrix_power(A, h)))})
    proj.append({"horizonte (pregões)": "estacionária", **dict(zip(CLASSES, estacionaria(A)))})
    proj = pd.DataFrame(proj)
    coef = pd.DataFrame(m.coef_.T, index=cols, columns=[CLASSES[i] for i in m.classes_])

    # saída diária
    dia = pd.DataFrame({"date": lab.index.strftime("%Y-%m-%d"), "rotulo": lab["classe"].values,
                        "id_episodio": lab["id_episodio"].values}, index=lab.index)
    for nome, M in (("filt", F), ("suav", S)):
        for i, c in enumerate(CLASSES):
            dia[f"{nome}_{c}"] = M[:, i].round(4)
    for nome, P in (("oos_filt", P_f), ("oos_suav", P_s)):
        for c in CLASSES:
            dia[f"{nome}_{c}"] = P[c].values.round(4)
    dia["oos_prev"] = [CLASSES[i] for i in P_s.values.argmax(1)]
    dia["oos_p_rotulo"] = P_s.values[np.arange(len(y)), y].round(4)
    dia["regua_antiga"] = ant.values
    dia.to_csv(AQUI / "prob_estados_diaria.csv", index=False, encoding="utf-8")

    piores = dia.sort_values("oos_p_rotulo").head(20)[
        ["date", "rotulo", "id_episodio", "oos_prev", "oos_p_rotulo"] + [f"oos_suav_{c}" for c in CLASSES]]
    ep = pd.read_csv(AQUI / "rotulos_episodios.csv", keep_default_na=False).set_index("id")
    tr = dia[dia.id_episodio != ""].groupby("id_episodio").agg(
        n_dias=("date", "size"), rotulo=("rotulo", "first"), p_media_rotulo=("oos_p_rotulo", "mean"),
        prev_mais_comum=("oos_prev", lambda s: s.value_counts().index[0]),
        frac_acerto=("oos_prev", "size"))
    tr["frac_acerto"] = dia[dia.id_episodio != ""].assign(ok=lambda d: d.oos_prev == d.rotulo).groupby(
        "id_episodio").ok.mean()
    tr["episodio"] = ep.loc[tr.index, "episodio"].values
    tr["inicio"] = ep.loc[tr.index, "inicio"].values
    tr["confianca"] = ep.loc[tr.index, "confianca"].values
    tr = tr.sort_values("p_media_rotulo")

    with pd.ExcelWriter(AQUI / "resultado_fase2.xlsx", engine="openpyxl") as w:
        pd.DataFrame({"item": [
            "Classes: Q0, Q1, Q2, Q4u (Q4 ↑ dólar), Q4d (Q4 ↓ dólar); Q3 é covariável (nov–dez).",
            f"Melhor bloco fora da amostra (log-loss da filtrada): {NOME_BLOCO[melhor]}.",
            "Validação: um ano fora por vez, purgando do treino os trechos que tocam o ano de teste.",
            f"Emissão: logit multinomial L2 (C={c_ok}) com pesos balanceados; p(x|y) ∝ p_bal(y|x), elevada a tau={tau_ok} "
            "no filtro (as métricas usam janelas sobrepostas; sem têmpera o filtro superconta a evidência). "
            "C e tau escolhidos pelo menor log-loss BALANCEADO médio fora da amostra nos três blocos (aba grade).",
            f"Transição: contagem dos rótulos + {PSEUDO} de pseudo-contagem nas transições observadas.",
            "Probabilidades 'filt'/'suav' = modelo final ajustado em toda a amostra (dentro da amostra); "
            "'oos_*' = fora da amostra.",
            "As métricas de vol, prêmio e CDS usam z-score contra janelas ANTERIORES de 252 e 1260 pregões, "
            "mais o nível absoluto.",
            "CDS de 2026-09-09 a 2026-10-26 veio provisoriamente do investing.com; CDS e T-bill de 27–28/10 "
            "repetem o último valor."]}).to_excel(w, sheet_name="leia_me", index=False)
        dia.to_excel(w, sheet_name="probabilidades", index=False)
        trans.to_excel(w, sheet_name="transicao")
        proj.to_excel(w, sheet_name="projecao", index=False)
        abl.to_excel(w, sheet_name="ablacao", index=False)
        resumo_abl.to_excel(w, sheet_name="ablacao", index=False, startrow=len(abl) + 3)
        por_ano.to_excel(w, sheet_name="ablacao", index=False, startrow=len(abl) + len(resumo_abl) + 6)
        grade.to_excel(w, sheet_name="grade", index=False)
        pares.to_excel(w, sheet_name="separacao_pares", index=False)
        fases.to_excel(w, sheet_name="separacao_pares", index=False, startrow=len(pares) + 3)
        r = 0
        for tipo, P in (("filtrada", P_f), ("suavizada", P_s), ("só logit", oos[melhor]["logit"])):
            pd.DataFrame({f"confusão fora da amostra — {tipo} — bloco {melhor}": []}).to_excel(
                w, sheet_name="confusao", startrow=r, index=False)
            confusao(P, y).to_excel(w, sheet_name="confusao", startrow=r + 1)
            r += 9
        sob.to_excel(w, sheet_name="sobreposicao", index=False)
        r = len(sob) + 3
        for nome, cm in conf_sob.items():
            pd.DataFrame({f"confusão (filtrada) — {nome}": []}).to_excel(w, sheet_name="sobreposicao",
                                                                        startrow=r, index=False)
            cm.to_excel(w, sheet_name="sobreposicao", startrow=r + 1)
            r += 9
        regua.to_excel(w, sheet_name="regua_antiga", index=False)
        conf_antiga.to_excel(w, sheet_name="regua_antiga", startrow=len(regua) + 3)
        piores.to_excel(w, sheet_name="piores_dias", index=False)
        tr.to_excel(w, sheet_name="trechos_suspeitos")
        coef.to_excel(w, sheet_name="coeficientes")

    pd.set_option("display.width", 220)
    print(grade[grade.probabilidade=="filtrada"].pivot_table(index=["C","tau"],columns="bloco",values=["log_loss_bal","log_loss","acerto_balanceado"]).round(3).to_string())
    print(abl.round(3).to_string())
    print("melhor:", melhor)
    print(confusao(P_f, y))
    print(confusao(P_s, y))
    print(sob.round(3).to_string())
    for nome, cm in conf_sob.items():
        print(nome); print(cm)
    print(regua.round(3).to_string())
    print(conf_antiga)
    print(trans.round(3).to_string())
    print(proj.round(3).to_string())
    print(piores.to_string())
    print(tr.head(25).round(3).to_string())


if __name__ == "__main__":
    main()
