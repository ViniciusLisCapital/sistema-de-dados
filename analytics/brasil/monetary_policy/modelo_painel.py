"""Painel trimestral de insumos do modelo agregado semiestrutural do BC.

Fonte da especificacao: boxe "Atualizacao dos modelos semiestruturais de pequeno
porte", Relatorio de Inflacao de junho/2024 (referencia/atualizacao_modelos.pdf,
pp. 97-105). As equacoes estao transcritas na docstring de `modelo_agregado.py`.

Escreve DOIS paineis, que diferem apenas na janela dos filtros HP:

  data/modelo_painel_est.csv   HP ate 2023T4 -- para ESTIMAR. Fiel ao conjunto de
                               informacao que o BC tinha no boxe de jun/2024, e o
                               unico em que a comparacao de parametros e legitima.
  data/modelo_painel_full.csv  HP ate o ultimo trimestre disponivel -- para estender
                               os estados ate hoje e partir dai nos cenarios.

Tres decisoes de construcao foram VALIDADAS contra numero publicado, nao escolhidas
por gosto (ver `referencia/` e o CLAUDE.md da pasta):

  1. i^e e a Selic esperada NO horizonte de 12 meses (ponto), nao a media do caminho.
     Contra a Tabela 1 do boxe da neutra ("esperado 1 ano a frente, filtro HP" =
     5,2% em 2023T2 e 5,7% em 2024T2), o ponto erra +0,14 e a media +0,82.
  2. O HP roda com CAUDA de projecao Focus. Sem ela a tendencia de r* em 2023T4 sai
     7,15% contra 4,82% da mediana publicada; com ela, 5,01%. O BC faz o mesmo -- o
     titulo do C2 Boxe1 Graf 1B do anexo diz "dados completados com projecoes Focus".
  3. O juro real e diferenca simples i^e - pi^e, como na eq. (2.1). Fisher exato
     descola ~0,2 p.p. da serie em amostra.

Uso:
    uv run python analytics/brasil/monetary_policy/modelo_painel.py
    python -c "from analytics.brasil.monetary_policy.modelo_painel import construir_tudo; construir_tudo()"

A primeira execucao baixa o anexo do RPM (xlsx de ~12 MB, duas edicoes) e a Nuci do
IPEADATA; tudo fica em cache em data/, entao as seguintes sao rapidas.
"""
from __future__ import annotations

import datetime as dt
import warnings
from pathlib import Path

import numpy as np
import pandas as pd
from statsmodels.tsa.filters.hp_filter import hpfilter
from statsmodels.tsa.x13 import x13_arima_analysis

from connectors.mysql import MySQLDataRequester

warnings.filterwarnings("ignore")

_HERE = Path(__file__).parent
DATA = _HERE / "data"

PI_EXT = 2.0                        # inflacao de equilibrio externa (nota 5 do boxe)
LAMB = 1600                         # HP trimestral
PRE_COVID = "2019Q4"                # media de referencia de Nuci e desocupacao
SEMIEL_FISCAL = 0.30                # semi-elasticidade do primario ao hiato (% do PIB/p.p.)
FIM_EST = pd.Period("2023Q4", "Q")  # fim da amostra de estimacao do boxe
INICIO = "2001Q4"                   # folga para as defasagens (MA4 do IPCA, 5 de clima)
ESCALA_CLIMA = 10.0                 # ONI em decimos de grau -- ver `_brutos()`

_COLS = ["pi_L", "pi_IPCA", "pi_A", "pi_e", "i_e", "meta", "pi_star", "de_hat", "Zel",
         "Yla", "selic", "i_dif", "de", "r_focus", "rr_trend", "hp_ciclo", "rp_hat",
         "fpib", "fnuci", "femp", "fcaged"]


# ── acesso a dados ───────────────────────────────────────────────────────────
def q(db: str, sql: str) -> pd.DataFrame:
    req = MySQLDataRequester(db, "x")
    req.connect()
    try:
        df = pd.read_sql(sql, req.connection)
        df.columns = [str(c).lower() for c in df.columns]
        return df
    finally:
        req.close_connection()


def serie(db: str, tab: str, name: str | None = None) -> pd.Series:
    w = "" if name is None else " WHERE name='%s'" % name
    d = q(db, "SELECT date, value FROM %s%s ORDER BY date" % (tab, w))
    d["date"] = pd.to_datetime(d["date"])
    return d.set_index("date")["value"].astype(float).sort_index()


def _cache(nome: str, fn):
    """Cache em disco de um pull lento (anexo do RPM, IPEADATA)."""
    p = DATA / nome
    if p.exists():
        s = pd.read_csv(p, index_col=0)
        s.index = pd.to_datetime(s.index)
        return s.iloc[:, 0]
    DATA.mkdir(parents=True, exist_ok=True)
    s = fn()
    s.to_frame("value").to_csv(p)
    return s


def para_q(s: pd.Series, como: str = "media", completos: bool = True) -> pd.Series:
    """Mensal -> trimestral. `completos` descarta o trimestre parcial da ponta.

    Sem isso o ultimo trimestre entra calculado com 1 ou 2 meses: numa serie de fluxo
    isso subestima a taxa trimestral, e numa de nivel desalinha a media.
    """
    g = s.sort_index().groupby(pd.PeriodIndex(s.index, freq="Q"))
    out = g.mean() if como == "media" else g.last()
    if completos and len(out) > 4:
        # regra unica para diaria, semanal e mensal: corta a ponta se ela tem menos
        # observacoes que a metade da mediana dos trimestres cheios
        n = g.size()
        lim = 0.5 * float(n.iloc[:-1].median())
        while len(out) and n.loc[out.index[-1]] < lim:
            out = out.iloc[:-1]
    return out


# ── filtros ──────────────────────────────────────────────────────────────────
def hp(s: pd.Series, comp: str, fim: pd.Period, cauda: pd.Series | None = None) -> pd.Series:
    """HP(1600) de dois lados ate `fim`, com cauda opcional de projecao.

    A cauda entra no filtro e sai do resultado: e o que remove o vies de ponta sem
    contaminar a serie devolvida com valores projetados.
    """
    x = s.dropna()
    x = x[x.index <= fim]
    z = x if cauda is None or not len(cauda) else pd.concat([x, cauda[cauda.index > fim]]).sort_index()
    ciclo, tend = hpfilter(z.values, lamb=LAMB)
    return pd.Series(ciclo if comp == "ciclo" else tend, index=z.index).reindex(x.index)


def _infl_q_sa(nome: str) -> pd.Series:
    """% mensal -> indice -> X-13ARIMA-SEATS -> inflacao trimestral dessazonalizada."""
    r = serie("macro_brasil", "inflc_agregados", nome)
    r = r[r.index >= "1996-01-01"].dropna()          # pos-Real: antes disso o ARIMA nao converge
    idx = pd.Series(100 * np.cumprod(1 + r.values / 100.0), index=r.index)
    idx.index = pd.DatetimeIndex(idx.index).to_period("M").to_timestamp()
    sa = pd.Series(np.asarray(x13_arima_analysis(idx, freq="M", outlier=True).seasadj, float),
                   index=idx.index)
    g = sa.groupby(pd.PeriodIndex(sa.index, freq="Q"))
    ult = g.last()[g.size() == 3]          # so trimestres com os 3 meses
    return (ult / ult.shift(1) - 1.0) * 100.0


def _nivel_sa(s: pd.Series) -> pd.Series:
    """Dessazonaliza uma serie de NIVEL mensal (Nuci) por X-13."""
    x = s.dropna()
    x.index = pd.DatetimeIndex(x.index).to_period("M").to_timestamp()
    x = x.asfreq("MS").interpolate()
    return pd.Series(np.asarray(x13_arima_analysis(x, freq="M", outlier=True).seasadj, float),
                     index=x.index)


# ── Focus ────────────────────────────────────────────────────────────────────
_FA: pd.DataFrame | None = None


def focus_anual() -> pd.DataFrame:
    """Painel anual do Focus (Selic, IPCA, PIB Total) com o horizonte em anos.

    Selic e fim de periodo -> horizonte (ref+1-ano); IPCA e PIB sao acumulados no ano
    -> horizonte (ref+0,5-ano).
    """
    global _FA
    if _FA is None:
        d = q("macro_brasil", "SELECT date, indicador, data_referencia, mediana "
                              "FROM expc_focus_periodo WHERE indicador IN "
                              "('Selic','IPCA','PIB Total') AND periodicidade='anual' "
                              "AND base_calculo=0 ORDER BY date")
        d["date"] = pd.to_datetime(d["date"])
        d["ref"] = d["data_referencia"].astype(int)
        d["mediana"] = d["mediana"].astype(float)
        ano = d["date"].dt.year + (d["date"].dt.dayofyear - 1) / 365.25
        d["h"] = np.where(d["indicador"] == "Selic", d["ref"] + 1.0, d["ref"] + 0.5) - ano
        _FA = d
    return _FA


def focus_ipca_12m() -> pd.Series:
    d = q("macro_brasil", "SELECT date, mediana FROM expc_focus WHERE indicador='IPCA' "
                          "AND horizonte='12m' AND suavizada='S' AND base_calculo=0 ORDER BY date")
    d["date"] = pd.to_datetime(d["date"])
    return para_q(d.set_index("date")["mediana"].astype(float))


def focus_selic_12m() -> pd.Series:
    """Selic esperada NO horizonte de 12 meses (ponto) -- ver decisao 1 na docstring."""
    return para_q(focus_selic_12m_diario())


def focus_selic_12m_diario() -> pd.Series:
    """A mesma coisa antes de virar trimestre, uma observacao por data de pesquisa.

    Separada de `focus_selic_12m()` em 2026-08 para `condicoes_copom.py`, que precisa do
    valor numa data especifica (o dia da reuniao do Copom) e nao numa media trimestral.
    A definicao tem de continuar sendo uma so: duas leituras de juro real ex-ante no
    mesmo relatorio seriam bug, nao variacao.
    """
    d = focus_anual()
    d = d[d["indicador"] == "Selic"].copy()
    sel = serie("macro_international", "diferenciais_juros", "selic")
    sel_m = sel.reindex(pd.date_range(sel.index.min(), "2030-12-01", freq="MS")).ffill()
    mes = d["date"].values.astype("datetime64[M]").astype("datetime64[ns]")
    d["i0"] = sel_m.reindex(pd.DatetimeIndex(mes)).values
    out = {}
    for data, g in d.groupby("date"):
        g = g[g["h"] > 0].sort_values("h")
        if g.empty or not np.isfinite(g["i0"].iloc[0]) or g["h"].max() < 1.0:
            continue
        out[data] = float(np.interp(1.0, np.r_[0.0, g["h"].values],
                                    np.r_[g["i0"].iloc[0], g["mediana"].values]))
    return pd.Series(out).sort_index()


def _ultima_curva(fim: pd.Period) -> pd.DataFrame:
    d = focus_anual()
    sub = d[d["date"] <= fim.to_timestamp("Q") + pd.offsets.QuarterEnd(0)]
    return sub[sub["date"] == sub["date"].max()] if len(sub) else sub


def cauda_juro_real(fim: pd.Period, ate: float = 4.5) -> pd.Series:
    """Juro real Focus projetado por horizonte, da ultima pesquisa <= fim."""
    g = _ultima_curva(fim)
    S = g[g["indicador"] == "Selic"].sort_values("h")
    I = g[g["indicador"] == "IPCA"].sort_values("h")
    if S.empty or I.empty:
        return pd.Series(dtype=float)
    hs = np.arange(1.25, ate + 0.01, 0.25)
    hs = hs[(hs <= S["h"].max()) & (hs <= I["h"].max())]
    if not len(hs):
        return pd.Series(dtype=float)
    r = np.interp(hs, S["h"], S["mediana"]) - np.interp(hs, I["h"], I["mediana"])
    out = pd.Series(r, index=pd.PeriodIndex([fim + int(round(h * 4)) - 4 for h in hs], freq="Q"))
    return out[~out.index.duplicated()].sort_index()


def cauda_pib(nivel: pd.Series, fim: pd.Period, ate: int = 5) -> pd.Series:
    """Nivel do PIB projetado com o crescimento anual esperado no Focus."""
    g = _ultima_curva(fim)
    G = g[g["indicador"] == "PIB Total"].sort_values("h")
    if G.empty or fim not in nivel.index:
        return pd.Series(dtype=float)
    base, idx, vals = float(nivel[fim]), [], []
    for k in range(1, ate * 4 + 1):
        pr = fim + k
        h = (pr.end_time - fim.end_time).days / 365.25
        if h > G["h"].max():
            break
        base *= (1 + float(np.interp(h, G["h"], G["mediana"])) / 100.0) ** 0.25
        idx.append(pr)
        vals.append(base)
    return pd.Series(vals, index=pd.PeriodIndex(idx, freq="Q"))


# ── anexo estatistico do RPM e IPEADATA ──────────────────────────────────────
def desocupacao_retropolada() -> pd.Series:
    """Graf 1.2.11 do anexo de jun/2026: taxa retropolada do BC, mensal a.s. desde 2004-04.

    E a serie que o proprio BC usa na equacao (8) -- retropolada por Alves e Fasolo,
    BCB Working Paper 400 (2015). As tabelas de PNAD do projeto so comecam em 2012, o
    que nao cobre a amostra de estimacao.
    """
    from connectors.bcb_rpm import AnexoRPM
    a = AnexoRPM()
    g = a.grade(a.abrir(dt.date(2026, 6, 1))["Graf 1.2.11"]).iloc[:, :2].dropna()
    g = g[g[0].apply(lambda v: isinstance(v, (dt.date, dt.datetime, pd.Timestamp)))]
    return pd.Series(g[1].astype(float).values, index=pd.to_datetime(g[0].values)).sort_index()


def nuci_fgv() -> pd.Series:
    """Nuci da FGV via IPEADATA (CE12_CUTIND12), mensal desde 1970 (trimestral pre-2005)."""
    from connectors.ipeadata import IPEA
    d = IPEA().get_series("CE12_CUTIND12").dropna()
    d["date"] = pd.to_datetime(d["date"])
    return d.set_index("date")["value"].astype(float).sort_index()


def neutra_publicada() -> pd.DataFrame:
    """C2 Boxe2 Graf 1 do anexo de jun/2024: 5 grupos de medidas de taxa neutra.

    A coluna "Modelos BC" e, pela nota 4 da Tabela 1 do mesmo boxe, a taxa obtida
    endogenamente pela filtragem dos modelos semiestruturais -- o r* do proprio modelo
    que estamos replicando, e portanto o alvo de validacao.
    """
    p = DATA / "modelo_neutra_pub.csv"
    if p.exists():
        out = pd.read_csv(p, index_col=0)
        out.index = pd.PeriodIndex(out.index, freq="Q")
        return out
    from connectors.bcb_rpm import AnexoRPM
    a = AnexoRPM()
    g = a.grade(a.abrir(dt.date(2024, 6, 1))["C2 Boxe2 Graf 1"])
    lab = [str(v) for v in g.iloc[8, 1:6].tolist()]
    lin = g[g[0].astype(str).str.match(r"^\d{4}:\d$", na=False)]
    idx = pd.PeriodIndex([str(v).replace(":", "Q") for v in lin[0]], freq="Q")
    out = pd.DataFrame(lin.iloc[:, 1:6].values, index=idx, columns=lab).apply(
        pd.to_numeric, errors="coerce")
    DATA.mkdir(parents=True, exist_ok=True)
    out.to_csv(p)
    return out


def irf_publicada() -> pd.DataFrame:
    """C2 Boxe3 Graf 4A e 4B do anexo de jun/2024: o experimento de canais.

    Graf 4A e a trajetoria EXOGENA da Selic (+1 p.p. por 4 trimestres, depois decaindo
    a fator fixo de 0,8), escolhida pelo BC justamente para silenciar a resposta
    endogena da regra de Taylor e tornar os cenarios comparaveis.

    Graf 4B da a resposta do IPCA acumulado em 4 trimestres em tres configuracoes. A
    terceira, "Expectativa IPCA e cambio fixos", desliga os canais de expectativa e de
    cambio e deixa so o de demanda -- que e exatamente a configuracao do nosso
    simulador enquanto a equacao (5) nao existe. E o alvo de validacao correto; o
    Graf 1B (modelo cheio) nao e comparavel.

    Devolve colunas: selic, canal_completo, sem_cambio, so_demanda.
    """
    p = DATA / "modelo_irf_pub.csv"
    if p.exists():
        return pd.read_csv(p, index_col=0)
    from connectors.bcb_rpm import AnexoRPM
    a = AnexoRPM()
    wb = a.abrir(dt.date(2024, 6, 1))

    def _num(aba, ncols):
        g = a.grade(wb[aba])
        lin = g[g[0].astype(str).str.match(r"^\d+(\.0)?$", na=False)]
        out = lin.iloc[:, :1 + ncols].apply(pd.to_numeric, errors="coerce").dropna()
        return out.set_index(out.columns[0])

    sel = _num("C2 Boxe3 Graf 4A", 1)
    resp = _num("C2 Boxe3 Graf 4B", 3)
    out = pd.concat([sel, resp], axis=1)
    out.columns = ["selic", "canal_completo", "sem_cambio", "so_demanda"]
    out.index.name = "trimestre"
    out.index = out.index.astype(int)
    DATA.mkdir(parents=True, exist_ok=True)
    out.to_csv(p)
    return out


# ── montagem ─────────────────────────────────────────────────────────────────
def _brutos() -> dict:
    """Tudo o que nao depende da janela do HP (o caro: X-13 e os pulls externos)."""
    b = {}
    b["pi_L"] = _infl_q_sa("ipca_livres")
    b["pi_IPCA"] = _infl_q_sa("ipca")
    b["pi_A"] = _infl_q_sa("ipca_administrado")
    b["pi_e"] = focus_ipca_12m()
    b["i_e"] = focus_selic_12m()

    meta_a = serie("macro_brasil", "inflc_meta", "meta_inflacao")
    mq = meta_a.reindex(pd.date_range("1999-01-01", "2030-10-01", freq="QS")).ffill()
    b["meta"] = pd.Series(mq.values, index=pd.PeriodIndex(mq.index, freq="Q"))

    icbr = {k: para_q(serie("macro_brasil", "comm_icbr", "icbr_" + k))
            for k in ("geral", "agropecuaria", "metal", "energia")}
    dic = {k: (v / v.shift(1) - 1.0) * 100.0 for k, v in icbr.items()}
    sub = ("agropecuaria", "metal", "energia")
    X = pd.DataFrame({k: dic[k] for k in sub}).dropna()
    y = dic["geral"].reindex(X.index)
    ok = y.notna()
    W, *_ = np.linalg.lstsq(X[ok].values, y[ok].values, rcond=None)
    r2 = 1 - ((y[ok].values - X[ok].values @ W) ** 2).sum() / ((y[ok].values - y[ok].mean()) ** 2).sum()
    b["_w_icbr"], b["_r2_icbr"] = W / W.sum(), r2
    b["_dic"] = dic

    ptax = para_q(serie("macro_brasil", "cmb_ptax", "ptax_venda"))
    b["de"] = np.log(ptax).diff() * 100.0

    # O ONI entra em DECIMOS DE GRAU, nao em graus. O boxe (nota 6) nomeia a serie
    # -- ONI do CPC/NOAA, a mesma daqui -- mas nao as unidades, e a diferenca e 100x
    # em Clima^2. Tres coisas medidas apontam para decimos: (i) com a5/a6 livres a
    # verossimilhanca pede 0,1287 e 0,1643, ou seja 107x e 235x as modas publicadas, e
    # o k = sqrt(a5/0,0012) implicito fica entre 10,2 e 10,6 em TODOS os ajustes
    # deixa-um-episodio-ENSO-de-fora (nao e um El Nino carregando a estimativa);
    # (ii) reescalado, a5 = 0,0013 cai praticamente na moda publicada (0,0012) e a6 =
    # 0,0016 dentro do IC de [0; 0,0021]; (iii) o suporte da priori, [0; 0,01], que o
    # BC descreve como "pouco informativa", limitaria a contribuicao do clima a 0,05 p.p.
    # se Clima fosse em graus -- em decimos o teto e 4,6 p.p., que e de fato solto.
    # Em graus o termo contribui 0,006 p.p. na moda deles: decoracao, nao variavel.
    oni = serie("macro_international", "clima_oni") * ESCALA_CLIMA
    oni.index = pd.PeriodIndex(oni.index, freq="Q")
    oni = oni.groupby(level=0).mean()
    # dummies em ZERO, nao no +-0,5 da definicao de episodio do NOAA: o boxe diz
    # "dummy que assume valor 1 quando a anomalia climatica e positiva (eventos El Nino)".
    z = pd.Series(np.where(oni > 0, oni ** 2, 0.0), index=oni.index)
    yy = pd.Series(np.where(oni < 0, oni ** 2, 0.0), index=oni.index)
    mm = lambda s: s.rolling(3).mean() - s.shift(3).rolling(3).mean()
    b["Zel"], b["Yla"] = mm(z), mm(yy)

    b["selic"] = para_q(serie("macro_international", "diferenciais_juros", "selic"))
    ff = para_q(serie("macro_international", "diferenciais_juros", "fed_funds"))
    cds = para_q(serie("macro_brasil", "cmb_risco_pais", "cds_5y_usd")) / 100.0
    cds = cds[cds.index >= pd.Period("2008Q1", "Q")]     # 2007T4 e trimestre parcial
    b["i_dif"] = b["selic"] - (ff + cds)

    d = q("macro_brasil", "SELECT date, value FROM atv_pib WHERE name='pib_pm' "
                          "AND seasonal_adjs='Y' ORDER BY date")
    d["date"] = pd.to_datetime(d["date"])
    b["pib"] = pd.Series(d["value"].astype(float).values,
                         index=pd.PeriodIndex(d["date"], freq="Q")).dropna()

    # Nuci DESSAZONALIZADA. A serie bruta tem sazonalidade de 25% do proprio
    # desvio-padrao (jan -1,8 / out +1,7); deixa-la crua contra uma desocupacao que
    # ja vem a.s. do anexo infla o ruido de medicao dela e empurra gamma_nuci.
    b["nuci"] = para_q(_nivel_sa(_cache("modelo_nuci_fgv.csv", nuci_fgv)))
    b["desoc"] = para_q(_cache("modelo_desoc_retro.csv", desocupacao_retropolada))
    b["caged"] = para_q(serie("macro_brasil", "mt_caged", "caged_total"))

    rtn12 = serie("macro_brasil", "fisc_rtn", "resultado_primario_governo_central").rolling(12).sum()
    d = q("macro_brasil", "SELECT date, name, value FROM atv_pib_valores_correntes ORDER BY date")
    d["date"] = pd.to_datetime(d["date"])
    alvo = [n for n in d["name"].unique() if "pib" in n.lower()][0]
    pn = d[d["name"] == alvo].set_index("date")["value"].astype(float)
    pibn12 = pd.Series(pn.values, index=pd.PeriodIndex(pn.index, freq="Q")).rolling(4).sum()
    b["rp_bruto"] = (para_q(rtn12, "ultimo") / pibn12) * 100.0

    # pesos livres/administrados no IPCA, recuperados por regressao (o BC nao publica
    # os pesos do modelo). Fecham o IPCA no cenario sem exigir um bloco de administrados.
    Xa = pd.DataFrame({"L": b["pi_L"], "A": b["pi_A"]}).dropna()
    ya = b["pi_IPCA"].reindex(Xa.index)
    m = ya.notna()
    Wa, *_ = np.linalg.lstsq(Xa[m].values, ya[m].values, rcond=None)
    r2a = 1 - ((ya[m].values - Xa[m].values @ Wa) ** 2).sum() / ((ya[m].values - ya[m].mean()) ** 2).sum()
    b["_w_ipca"], b["_r2_ipca"] = Wa / Wa.sum(), r2a
    return b


def construir(fim_hp: pd.Period, b: dict | None = None) -> tuple[pd.DataFrame, dict]:
    """Painel com todos os filtros HP fechados em `fim_hp`."""
    b = _brutos() if b is None else b
    W, dic, meta = b["_w_icbr"], b["_dic"], b["meta"]

    pi_star = sum(w * (dic[k] - meta / 4.0)
                  for w, k in zip(W, ("agropecuaria", "metal", "energia")))
    de_hat = b["de"] - (meta - PI_EXT) / 4.0

    r_focus = b["i_e"] - b["pi_e"]
    rr_trend = hp(r_focus, "tend", fim_hp, cauda_juro_real(fim_hp)).reindex(r_focus.index)
    hp_ciclo = r_focus - rr_trend

    fpib = hp(np.log(b["pib"]) * 100, "ciclo", fim_hp,
              cauda=np.log(cauda_pib(b["pib"], fim_hp)) * 100)
    fcaged = hp(np.log(b["caged"].dropna()) * 100, "ciclo", fim_hp)
    fnuci = b["nuci"] - b["nuci"][b["nuci"].index <= PRE_COVID].mean()
    # sinal invertido: a desocupacao e contraciclica e gamma_emp > 0 na eq. (8)
    femp = -(b["desoc"] - b["desoc"][b["desoc"].index <= PRE_COVID].mean())

    lo, hi = b["rp_bruto"].quantile([0.01, 0.99])
    rp_ca = b["rp_bruto"].clip(lo, hi) - SEMIEL_FISCAL * fpib.reindex(b["rp_bruto"].index)
    rp_hat = hp(rp_ca, "ciclo", fim_hp)

    P = pd.DataFrame({
        "pi_L": b["pi_L"], "pi_IPCA": b["pi_IPCA"], "pi_A": b["pi_A"], "pi_e": b["pi_e"],
        "i_e": b["i_e"], "meta": meta, "pi_star": pi_star, "de_hat": de_hat,
        "Zel": b["Zel"], "Yla": b["Yla"], "selic": b["selic"], "i_dif": b["i_dif"],
        "de": b["de"], "r_focus": r_focus, "rr_trend": rr_trend, "hp_ciclo": hp_ciclo,
        "rp_hat": rp_hat, "fpib": fpib, "fnuci": fnuci, "femp": femp, "fcaged": fcaged,
    })[_COLS].loc[INICIO:]
    # a meta se estende anos a frente; o painel para no ultimo trimestre com dado real
    nucleo = P[["pi_L", "pi_IPCA", "selic", "pi_e"]].notna().any(axis=1)
    P = P.loc[:nucleo[nucleo].index.max()]
    meta_info = dict(fim_hp=str(fim_hp), w_icbr=list(map(float, W)),
                     r2_icbr=float(b["_r2_icbr"]),
                     w_ipca=list(map(float, b["_w_ipca"])), r2_ipca=float(b["_r2_ipca"]))
    return P, meta_info


def construir_tudo(verbose: bool = True) -> dict:
    """Gera os dois paineis e o sigma calibrado de r*. Devolve os metadados."""
    DATA.mkdir(parents=True, exist_ok=True)
    b = _brutos()
    ult = min(b["pi_L"].dropna().index.max(), b["selic"].dropna().index.max(),
              b["pi_e"].dropna().index.max())

    info = {}
    for rot, fim in (("est", FIM_EST), ("full", ult)):
        P, mi = construir(fim, b)
        P.to_csv(DATA / ("modelo_painel_%s.csv" % rot))
        info[rot] = mi
        if verbose:
            print("  painel_%-5s HP ate %s | %d trimestres (%s -> %s)"
                  % (rot, fim, len(P), P.index.min(), P.index.max()))

    # sigma(eps_rr): calibrado para casar a variancia de delta r* com a das medidas
    # publicadas -- e o que o boxe diz fazer, e nao e estimado.
    NB = neutra_publicada()
    Pe = pd.read_csv(DATA / "modelo_painel_est.csv", index_col=0)
    Pe.index = pd.PeriodIndex(Pe.index, freq="Q")
    med = NB.median(axis=1).dropna()
    dm = med.diff().dropna()
    dt_ = Pe["rr_trend"].reindex(med.index).dropna().diff().dropna()
    ci = dm.index.intersection(dt_.index)
    v_pub, v_tr = float(dm[ci].var()), float(dt_[ci].var())
    sig = float(np.sqrt(max(v_pub - v_tr, 1e-8)))
    (DATA / "modelo_sigma_rr.txt").write_text("%.6f" % sig)
    info["sigma_rr"] = sig
    info["neutra_pub_fim"] = str(med.index.max())
    if verbose:
        print("  sigma(eps_rr) calibrado = %.4f  (var delta pub %.4f - var delta tend %.4f)"
              % (sig, v_pub, v_tr))
        print("  pesos IC-Br: agro %.4f metal %.4f energia %.4f (R2 %.5f)"
              % (*info["est"]["w_icbr"], info["est"]["r2_icbr"]))
        print("  pesos IPCA: livres %.4f administrados %.4f (R2 %.5f)"
              % (*info["est"]["w_ipca"], info["est"]["r2_ipca"]))
    return info


def carregar(rot: str = "est") -> pd.DataFrame:
    P = pd.read_csv(DATA / ("modelo_painel_%s.csv" % rot), index_col=0)
    P.index = pd.PeriodIndex(P.index, freq="Q")
    return P


if __name__ == "__main__":
    print("Construindo paineis do modelo agregado...")
    construir_tudo()
