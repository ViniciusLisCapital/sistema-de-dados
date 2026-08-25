"""
Gerador do Panorama de Politica Monetaria em HTML.

Abas de dado, e a fonte de cada uma:

  Cenarios       modelo agregado (data/modelo_cenario_*.csv) + IRF validado contra o
                 C2 Boxe3 Graf 4B do anexo do RPM
  Decomposicao   contribuicoes exatas das eqs. (1), (2) e (3) (data/modelo_decomp_*.csv)
  Taxa Neutra    r* latente do modelo vs. as 5 medidas do C2 Boxe2 Graf 1
  Hiato          hiato latente do modelo vs. pm_hiato_produto (+ dispersao)
  Projecoes      pm_copom_projecoes -- AINDA STUB, unica aba nao construida
  Motor          modelo agregado rodando NO NAVEGADOR: `_load_motor()` manda o historico
                 e `_motor_cfg()` manda parametros + condicoes iniciais + defaults dos
                 condicionantes, e o JS porta `modelo_agregado.simular()`. E a unica aba
                 em que o usuario move input e ve o modelo responder
  Apendice       tabela de validacao dos 19 parametros contra a Tabela 1 do boxe

As cinco primeiras leem os artefatos que `modelo_agregado.rodar()` grava em `data/`.
Rodar o modelo NAO faz parte da geracao do relatorio de proposito: a estimacao leva
minutos e depende de MySQL, do IPEADATA e do anexo do RPM, enquanto gerar o HTML tem
de ser rapido e reproduzivel. Pipeline completo:

    uv run python analytics/brasil/monetary_policy/modelo_painel.py     # paineis
    uv run python analytics/brasil/monetary_policy/modelo_agregado.py   # estima + grava
    uv run python analytics/brasil/monetary_policy/generate_report.py   # HTML

Mesmo padrao /*REPORT_DATA*/ dos demais relatorios, via
analytics.report_structure.builder.render_report(), que tambem preenche /*THEME_CSS*/
e /*Y_AUTOFIT_JS*/. Output autocontido.

## Como adicionar uma aba

1. Escreva o `_load_<aba>()` aqui devolvendo `{chave: {"dates": [...], "values": [...]}}`
   -- o shape que `ser(grupo, chave)` espera no template. Chaves compostas usam `__`.
2. Ligue no loop de `run()`. **Cada loader tem o seu try/except**: artefato faltando
   degrada so a aba dele em vez de derrubar o relatorio (convencao do projeto).
3. Preencha o `render<Aba>()` em report.html e apague o `.stub-note` do painel.
"""

import json
from datetime import datetime
from pathlib import Path

import pandas as pd

from analytics.report_structure.builder import render_report
from connectors.mysql import MySQLDataRequester

_HERE = Path(__file__).parent
_TEMPLATE = _HERE / "report.html"
_DATA = _HERE / "data"
_DATABASE = "macro_brasil"


# ── utilitarios ──────────────────────────────────────────────────────────────
def _ser(s: pd.Series) -> dict:
    """Serie com PeriodIndex trimestral -> {"dates": ISO, "values": [...]}."""
    s = s.dropna() if s.isna().all() else s
    idx = s.index
    if isinstance(idx, pd.PeriodIndex):
        datas = idx.to_timestamp().strftime("%Y-%m-%d").tolist()
    else:
        datas = pd.to_datetime(idx).strftime("%Y-%m-%d").tolist()
    return {"dates": datas,
            "values": [None if pd.isna(v) else round(float(v), 4) for v in s.values]}


def _csv(nome: str) -> pd.DataFrame:
    df = pd.read_csv(_DATA / nome, index_col=0)
    try:
        df.index = pd.PeriodIndex(df.index, freq="Q")
    except Exception:
        pass
    return df


def _cols(df: pd.DataFrame, prefixo: str = "") -> dict:
    return {prefixo + c: _ser(df[c]) for c in df.columns if df[c].notna().any()}


def _read_table(table: str) -> pd.DataFrame:
    req = MySQLDataRequester(_DATABASE, table)
    req.connect()
    df = req.request_data()
    req.close_connection()
    if "date" in df.columns:
        df["date"] = pd.to_datetime(df["date"])
    if "value" in df.columns:
        df["value"] = pd.to_numeric(df["value"])
    return df


def _raio_eq5() -> float | None:
    """Raio espectral do laco da eq. (5) no cenario default, lido do proprio cenario.

    Nao roda o modelo: `cenarios_padrao()` grava o raio junto com o cenario endogeno.
    """
    p = _DATA / "modelo_eq5_diag.json"
    if not p.exists():
        return None
    return json.loads(p.read_text()).get("raio")


# ── loaders por aba ─────────────────────────────────────────────────────────
def _load_cenarios() -> dict:
    """Cenarios pre-calculados + historico de contexto + o IRF com o alvo publicado.

    Os cenarios sao pre-calculados em `modelo_agregado.cenarios_padrao()` porque o
    navegador nao roda o modelo: o que a interface faz e escolher entre trajetorias
    ja simuladas. Duas dimensoes de escolha -- caminho de Selic e tratamento da
    expectativa de inflacao. Na segunda o default e ENDOGENO (eq. 5 resolvida); as
    duas premissas fixas ficam como contrafactual, para separar o canal de expectativa
    do de demanda.
    """
    out = {}
    rot = json.loads((_DATA / "modelo_cenarios_rotulos.json").read_text())
    CAMPOS = ("selic", "i_e", "r_hat", "h", "pi_L", "pi_IPCA", "ipca_4t",
              "pi_e", "pi_A", "de", "de_hat")
    for k in rot:
        C = _csv("modelo_cenario_%s.csv" % k)
        for c in CAMPOS:
            if c in C.columns:
                out["%s__%s" % (k, c)] = _ser(C[c])

    # historico: o que o cenario continua
    P = _csv("modelo_painel_full.csv")
    S = _csv("modelo_estados.csv")
    out["hist__selic"] = _ser(P["selic"])
    out["hist__h"] = _ser(S["h"])
    out["hist__r_hat"] = _ser(S["r_hat"])
    out["hist__pi_IPCA"] = _ser(P["pi_IPCA"])
    out["hist__ipca_4t"] = _ser(P["pi_IPCA"].rolling(4).sum())
    out["hist__pi_e"] = _ser(P["pi_e"])
    out["hist__meta"] = _ser(P["meta"])

    # IRF: eixo em datas a partir do primeiro trimestre simulado, para manter o eixo
    # de tempo do framework; o rotulo do grafico diz que o horizonte e em trimestres
    I = _csv("modelo_irf.csv")
    t0 = P[["selic"]].dropna().index.max()
    idx = pd.period_range(t0 + 1, periods=len(I), freq="Q")
    for c in ("selic_choque", "h", "pi_L", "ipca_4t",
              "ipca_4t_so_demanda", "ipca_4t_com_expectativa", "ipca_4t_completo",
              "ipca_4t_motor_bcb", "pi_e_com_expectativa", "de_completo",
              "publicado_so_demanda", "publicado_sem_cambio", "publicado_completo"):
        if c in I.columns:
            out["irf__" + c] = _ser(pd.Series(I[c].values, index=idx))
    return out


def _load_decomp() -> dict:
    """Contribuicoes das eqs. (1), (2) e (3). Cada bloco soma o total exatamente."""
    out = {}
    for bloco in ("phillips", "hiato", "taylor"):
        D = _csv("modelo_decomp_%s.csv" % bloco)
        out.update(_cols(D, bloco + "__"))
    return out


def _load_neutra() -> dict:
    """r* latente do modelo vs. as 5 medidas publicadas no C2 Boxe2 Graf 1.

    A coluna "Modelos BC" e a taxa que o proprio BC obtem endogenamente pela filtragem
    dos semiestruturais (nota 4 da Tabela 1 do boxe) -- e o comparavel direto do nosso.
    As outras quatro sao grupos de metodologia e servem de faixa de referencia.
    """
    S = _csv("modelo_estados.csv")
    P = _csv("modelo_painel_full.csv")
    out = {"r_IS": _ser(S["rr_IS_total"]), "r_TAY": _ser(S["rr_TAY_total"]),
           "tendencia": _ser(P["rr_trend"]), "r_focus": _ser(P["r_focus"]),
           "desvio_IS": _ser(S["rr_IS"]), "r_hat": _ser(S["r_hat"])}
    NB = _csv("modelo_neutra_pub.csv")
    for c in NB.columns:
        chave = "pub_" + str(c).replace(" ", "_").replace(".", "")
        out[chave] = _ser(NB[c])
    return out


def _load_hiato() -> dict:
    """Hiato latente do modelo vs. pm_hiato_produto.

    NAO plotar as duas faixas do publicado como a mesma coisa: `minimo/p25/p75/maximo`
    (regime suite, edicoes >=2024-09) e desacordo ENTRE modelos, e `banda_sup/banda_inf`
    (<=2024-06) e incerteza de UM modelo. A serie comparavel entre edicoes e `central`.
    """
    S = _csv("modelo_estados.csv")
    out = {"nosso": _ser(S["h"]), "choque_persistente": _ser(S["s_h"])}
    df = _read_table("pm_hiato_produto")
    df["date"] = df["date"] + pd.DateOffset(months=2)   # rotulo do BC e inicio do tri
    df["per"] = pd.PeriodIndex(df["date"], freq="Q")
    piv = df.pivot_table(index="per", columns="variavel", values="value", aggfunc="first")
    for c in piv.columns:
        out["pub_" + str(c)] = _ser(piv[c])
    return out


def _load_projecoes() -> dict:
    """Aba Projecoes do Copom -> macro_brasil.pm_copom_projecoes. AINDA STUB.

    Nao passa por um loader flat: a tabela e (nro_reuniao, indice, cenario, date) +
    `vintage`, `horizonte_relevante`, `regime`, entao precisa de filtro antes do
    groupby e a chave natural e composta.

    Leitura principal (uma linha por reuniao, a projecao do horizonte que o Copom diz
    perseguir, no cenario de Selic da Focus):
        horizonte_relevante == 1 & cenario == 'juros_focus'
        & indice == 'ipca' & regime == 'hr_6_trimestres'

    Duas armadilhas, em domain/db/brasil/bcb/copom_comunicados.md: `cenario` classifica
    pelo CONDICIONAMENTO (juros_focus | juros_constante), nao pelo rotulo publicado --
    "cenario de referencia" significava o OPOSTO em 2016-2017 (o rotulo original fica
    em `cenario_publicado`); e sem filtro de `regime` tres conceitos de horizonte
    relevante se misturam na mesma serie.

    Escala: IPCA acumulado em 4 trimestres (%). Duas dimensoes de tempo, e a escolha
    muda o grafico: `date` e o periodo projetado, `vintage` e a reuniao que projetou.
    """
    return {}


# ── aba Modelo BC - Agregado: motor rodando no NAVEGADOR ─────────────────────
# Diferenca de natureza para a aba Cenarios: la o Python pre-simula uma grade e o
# navegador escolhe uma trajetoria pronta; aqui o simulador de `modelo_agregado.simular()`
# esta PORTADO para JS e roda a cada mudanca de input. O que estes loaders enviam nao e
# resultado, e o que o motor precisa para produzir resultado: parametros, condicoes
# iniciais lidas em t0 e os caminhos default de cada condicionante.
#
# Toda constante daqui tem de casar com `simular()` -- e o teste que fecha isso e
# tests/test_monetary_policy_js.js, que roda o motor JS com a configuracao equivalente a
# `cenarios_padrao()` e exige bater com os CSVs que o Python gravou.
_MOTOR_N_OPCOES = [8, 12, 16, 20, 24]
_MOTOR_N = 16
_MOTOR_FOLGA = 40          # = modelo_agregado.FOLGA


def _load_motor() -> dict:
    """Series historicas que os graficos da aba emendam no inicio do cenario."""
    P = _csv("modelo_painel_full.csv")
    S = _csv("modelo_estados.csv")
    out = {
        "selic": _ser(P["selic"]),
        "i_e": _ser(P["i_e"]),
        "pi_IPCA": _ser(P["pi_IPCA"]),
        "ipca_4t": _ser(P["pi_IPCA"].rolling(4).sum()),
        "pi_L": _ser(P["pi_L"]),
        "pi_A": _ser(P["pi_A"]),
        "pi_e": _ser(P["pi_e"]),
        "meta": _ser(P["meta"]),
        "h": _ser(S["h"]),
        "s_h": _ser(S["s_h"]),
        "r_hat": _ser(S["r_hat"]),
        "rr_IS_total": _ser(S["rr_IS_total"]),
        "rr_TAY_total": _ser(S["rr_TAY_total"]),
        # juro real ex-ante como na eq. (2.1): diferenca simples, nao Fisher exato
        "r_real": _ser(P["i_e"] - P["pi_e"]),
        # condicionantes: o grafico por input da aba do motor plota o historico de cada um
        # contra o caminho digitado, entao TODO input do MT_SPEC precisa da serie dele aqui
        "de": _ser(P["de"]),
        # O card de inflacao importada e o IC-Br, nao o pi* cru. pi* = (variacao do
        # IC-Br) - meta/4 por construcao (eq. 1.1: os pesos somam 1), entao somar
        # meta/4 devolve a variacao do indice, exata, sem puxar `comm_icbr` de novo.
        # Os subindices agro/metal/energia so existem para recuperar os pesos que o
        # BC nao publica -- o que o modelo le, e o que o usuario digita, e o agregado.
        "icbr": _ser(P["pi_star"] + P["meta"] / 4.0),
        "pi_star": _ser(P["pi_star"]),
        "rp": _ser(P["rp_hat"]),
        "Zel": _ser(P["Zel"]),
        "Yla": _ser(P["Yla"]),
    }
    return out


def _copom_administrados(P: pd.DataFrame, idx: pd.PeriodIndex, t0: pd.Period) -> dict:
    """Projecao de precos administrados do PROPRIO Copom, trimestralizada.

    O bloco de administrados do BC nao esta implementado aqui, entao pi^A e premissa --
    mas premissa nao precisa ser inventada: o comunicado do Copom publica a projecao de
    administrados por ano-calendario, e `pm_copom_projecoes` ja carrega isso (indice
    `ipca_administrados`). Vira o atalho "Projecao do Copom" no card de pi^A.

    Conversao ano -> trimestre por DIVISAO SIMPLES, nao raiz quarta, porque e assim que o
    modelo acumula: `ipca_4t` e a SOMA de quatro trimestres. No primeiro ano projetado os
    trimestres ja observados sao descontados do total e o residuo e dividido pelos que
    faltam -- se a projecao e para o ano fechado, o que sobra para o 2o semestre nao e
    metade dela.

    Devolve {} se a tabela nao estiver disponivel: o atalho some, o resto da aba fica.
    """
    df = _read_table("pm_copom_projecoes")
    a = df[(df["indice"] == "ipca_administrados")
           & (df["cenario"] == "juros_focus")
           & (df["periodo_tipo"] == "ano")].copy()
    if a.empty:
        return {}
    a["vintage"] = pd.to_datetime(a["vintage"])
    a = a[a["vintage"] == a["vintage"].max()]
    a["ano"] = pd.to_datetime(a["date"]).dt.year
    anos = {int(r.ano): float(r.value) for r in a.itertuples()}
    if not anos:
        return {}

    obs = P["pi_A"][P["pi_A"].index <= t0].dropna()
    caminho, resto = [], {}
    for per in idx:
        ano = per.year
        alvo = anos.get(ano)
        if alvo is None:                      # depois do ultimo ano publicado, segura o ultimo
            ultimo = anos[max(anos)]
            caminho.append(ultimo / 4.0)
            continue
        if ano not in resto:
            ja = float(obs[obs.index.year == ano].sum())
            n_falta = sum(1 for p2 in idx if p2.year == ano)
            resto[ano] = (alvo - ja) / max(n_falta, 1)
        caminho.append(resto[ano])
    return {"caminho": [round(v, 6) for v in caminho],
            "reuniao": int(a["nro_reuniao"].iloc[0]),
            "vintage": str(a["vintage"].iloc[0].date()),
            "anos": {str(k): v for k, v in sorted(anos.items())}}


def _copom_hr() -> dict:
    """O horizonte relevante que o PROPRIO Copom declarou no ultimo comunicado.

    Desde a 264a reuniao o regime e `hr_6_trimestres` (Decreto 12.079/2024): o Copom
    persegue a meta seis trimestres a frente da REUNIAO, nao mais no ano-calendario. E
    dai que sai a regra de fallback do JS: `idx` comeca em t0+1, o trimestre corrente,
    que e onde a reuniao acontece -- entao seis trimestres a frente e `idx[6]`. Mandamos
    a data PUBLICADA e deixamos o JS preferi-la; se as duas divergirem, o painel esta
    atrasado em relacao a ultima reuniao, e o marcador segue a reuniao, nao a regra.

    Sem filtro de `regime` tres conceitos de horizonte relevante se misturam na mesma
    serie (ver a nota em `_load_projecoes()`). Devolve {} se a tabela nao existir: o
    marcador cai na regra dos 6 trimestres e o resto da aba fica de pe.
    """
    df = _read_table("pm_copom_projecoes")
    h = df[(df["horizonte_relevante"] == 1)
           & (df["cenario"] == "juros_focus")
           & (df["indice"] == "ipca")
           & (df["regime"] == "hr_6_trimestres")]
    if h.empty:
        return {}
    r = h[h["nro_reuniao"] == h["nro_reuniao"].max()].iloc[0]
    return {"date": str(pd.to_datetime(r["date"]).date()),
            "reuniao": int(r["nro_reuniao"]),
            "vintage": str(pd.to_datetime(r["vintage"]).date()),
            "trimestres": int(r["trimestres_a_frente"]),
            "ipca": round(float(r["value"]), 4)}


def _motor_cfg() -> dict:
    """Parametros, condicoes iniciais em t0 e defaults dos condicionantes.

    Le tudo EM t0 com a mesma semantica de `modelo_agregado._em()` (valor em t0, ou o
    ultimo valido ate t0) -- `rp_hat`, por exemplo, ja falta em t0 e cai no trimestre
    anterior. Divergir disso aqui faria o motor JS partir de um estado diferente do que
    o Python usa, que e exatamente o que o teste compara.
    """
    par = json.loads((_DATA / "modelo_params.json").read_text())
    P = _csv("modelo_painel_full.csv")
    S = _csv("modelo_estados.csv")
    t0 = P[["pi_L", "selic"]].dropna().index.max()
    nn = max(_MOTOR_N_OPCOES) + _MOTOR_FOLGA
    idx = pd.period_range(t0 + 1, periods=nn, freq="Q")

    def em(s):
        if t0 in s.index and pd.notna(s.loc[t0]):
            return float(s.loc[t0])
        d = s[s.index <= t0].dropna()
        return float(d.iloc[-1]) if len(d) else 0.0

    meta = P["meta"].reindex(idx).ffill()
    meta = meta.fillna(em(P["meta"]))

    # caminho de Selic da Focus: as 16 primeiras vem do cenario que o Python ja simulou
    # (identico a `caminho_selic_focus`), e depois segue plano -- a propria curva Focus
    # para em ~4,5 anos e `caminho_selic_focus` tambem prolonga o ultimo ponto dali.
    foc = list(_csv("modelo_cenario_focus__eq5.csv")["selic"].values)
    foc = [round(float(v), 6) for v in foc]

    ipca_obs = P["pi_IPCA"][P["pi_IPCA"].index <= t0].dropna()
    sel_obs = P["selic"][P["selic"].index <= t0].dropna()

    return {
        "t0": str(t0),
        "n_opcoes": _MOTOR_N_OPCOES,
        "n": _MOTOR_N,
        "folga": _MOTOR_FOLGA,
        "datas": idx.to_timestamp().strftime("%Y-%m-%d").tolist(),
        "par": {k: round(float(v), 10) for k, v in par.items() if not k.startswith("_")},
        "phi": {k: round(float(par[k]), 10) for k in ("f1", "f2", "f3")},
        "w_ipca": [0.7672, 0.2328],
        "pi_ext": 2.0,
        "meta": [round(float(v), 6) for v in meta.values],
        "ini": {
            "h": round(em(S["h"]), 8),
            "s_h": round(em(S["s_h"]), 8),
            "rr_IS": round(em(P["rr_trend"]) + em(S["rr_IS"]), 8),
            "rr_TAY": round(em(P["rr_trend"]) + em(S["rr_TAY"]), 8),
            "r_hat": round(em(S["r_hat"]), 8),
            "pi_L": round(em(P["pi_L"]), 8),
            "pi_e": round(em(P["pi_e"]), 8),
            "de_hat": round(em(P["de_hat"]), 8),
            "ipca4": [round(float(v), 8) for v in ipca_obs.iloc[-4:].values],
            "ipca3": [round(float(v), 8) for v in ipca_obs.iloc[-3:].values],
            "selic": round(float(sel_obs.iloc[-1]), 6),
            "selic_l1": round(float(sel_obs.iloc[-2]), 6),
        },
        "dflt": {
            "selic_focus": foc,
            # Duas ancoras diferentes, e a distincao importa: `ini.selic`/`ini.pi_e` sao
            # lidos EM t0 (t0 = ultimo trimestre com pi_L E selic) porque sao a defasagem
            # que as equacoes usam; estes dois sao o ULTIMO valor publicado, que ja pode
            # estar um trimestre a frente -- e a Selic corrente que "Selic constante"
            # significa, e a leitura mais recente da Focus que "expectativa fixa na Focus"
            # significa. `cenarios_padrao()` usa exatamente estes.
            "selic_ult": round(float(P["selic"].dropna().iloc[-1]), 6),
            "pi_e_focus": round(float(P["pi_e"].dropna().iloc[-1]), 8),
            "rp": round(em(P["rp_hat"]), 8),
            "pi_star": 0.0,
            "Zel": 0.0,
            "Yla": 0.0,
        },
        "copom_adm": _copom_administrados(P, idx, t0),
        "hr": _copom_hr(),
    }


def _load_info() -> dict:
    """Metadados nao-serie: validacao dos parametros, do IRF e os numeros de cabecalho."""
    par = json.loads((_DATA / "modelo_params.json").read_text())
    val = pd.read_csv(_DATA / "modelo_validacao.csv")
    virf = json.loads((_DATA / "modelo_validacao_irf.json").read_text())
    S = _csv("modelo_estados.csv")
    P = _csv("modelo_painel_full.csv")

    hp = _read_table("pm_hiato_produto")
    hp["per"] = pd.PeriodIndex(hp["date"] + pd.DateOffset(months=2), freq="Q")
    cen = hp[hp["variavel"] == "central"].set_index("per")["value"]
    Se = _csv("modelo_estados_est.csv")
    j = pd.DataFrame({"a": Se["h"], "b": cen}).dropna()

    ult = S["h"].dropna().index.max()
    return {
        "params": {k: round(v, 6) for k, v in par.items() if not k.startswith("_")},
        "logL": round(par["_logL"], 3), "logL_bcb": round(par["_logL_bcb"], 3),
        "sigma_rr": round(par["_sigma_rr"], 4),
        "validacao": json.loads(val.to_json(orient="records")),
        "n_dentro": int(val["dentro"].sum()), "n_total": int(len(val)),
        "irf": {k: (round(v, 4) if isinstance(v, float) else v) for k, v in virf.items()},
        "eq5": dict(par.get("_eq5") or {},
                    raio=_raio_eq5(), phi_bcb=dict(f1=0.75, f2=0.11, f3=0.021)),
        "hiato_corr": round(float(j["a"].corr(j["b"])), 4),
        "hiato_n": int(len(j)),
        "ultimo_tri": str(ult),
        "selic_hoje": round(float(P["selic"].dropna().iloc[-1]), 2),
        "h_hoje": round(float(S["h"].dropna().iloc[-1]), 2),
        "r_is_hoje": round(float(S["rr_IS_total"].dropna().iloc[-1]), 2),
        "r_tay_hoje": round(float(S["rr_TAY_total"].dropna().iloc[-1]), 2),
        "r_hat_hoje": round(float(S["r_hat"].dropna().iloc[-1]), 2),
        "neutra_pub_ult": round(float(_csv("modelo_neutra_pub.csv").median(axis=1).dropna().iloc[-1]), 2),
        "neutra_pub_tri": str(_csv("modelo_neutra_pub.csv").median(axis=1).dropna().index.max()),
        "rotulos": json.loads((_DATA / "modelo_cenarios_rotulos.json").read_text()),
    }


# ── entry point ──────────────────────────────────────────────────────────────
def run(output: str = "reports/brasil/Monetary Policy.html") -> None:
    print("Carregando dados...")
    data = {"generated_at": datetime.now().strftime("%d/%m/%Y %H:%M")}

    for grupo, loader, label in (
        ("cenarios",  _load_cenarios,  "Cenarios (modelo agregado + IRF)"),
        ("decomp",    _load_decomp,    "Decomposicao (eqs. 1, 2 e 3)"),
        ("neutra",    _load_neutra,    "Taxa Neutra (r* latente + C2 Boxe2 Graf 1)"),
        ("hiato",     _load_hiato,     "Hiato (r* latente + pm_hiato_produto)"),
        ("projecoes", _load_projecoes, "Projecoes do Copom (pm_copom_projecoes)"),
        ("motor",     _load_motor,     "Modelo BC - Agregado (historico do motor JS)"),
    ):
        try:
            series = loader()
            data[grupo] = series
            if series:
                n = sum(len(v["dates"]) for v in series.values())
                print(f"  {grupo:10s} {label}: {len(series)} series, {n} obs")
            else:
                print(f"  {grupo:10s} {label}: aba ainda nao construida (loader stub)")
        except Exception as exc:
            print(f"  {grupo:10s} {label}: FALHOU -- {exc}")
            data[grupo] = {}

    # Config do motor: nao e serie, entao fica fora do loop -- mesmo tratamento do info.
    try:
        data["motor_cfg"] = _motor_cfg()
        m = data["motor_cfg"]
        hr = m.get("hr") or {}
        print(f"  motor_cfg  t0={m['t0']} | folga={m['folga']} | "
              f"{len(m['par'])} parametros | horizonte ate {max(m['n_opcoes'])}T | "
              f"HR {hr.get('date', 'regra 6T')}"
              + (f" ({hr['reuniao']}a reuniao)" if hr else ""))
        # Divergir aqui e legitimo (painel um trimestre atras da ultima reuniao), mas
        # troca a fonte do marcador em silencio -- entao avisa.
        if hr and hr["date"] != m["datas"][6]:
            print(f"             AVISO  HR publicado ({hr['date']}) != datas[6] "
                  f"({m['datas'][6]}): painel atrasado ante a {hr['reuniao']}a reuniao; "
                  "o marcador segue a reuniao, nao a regra")
    except Exception as exc:
        print(f"  motor_cfg  FALHOU -- {exc}")
        data["motor_cfg"] = {}

    try:
        data["info"] = _load_info()
        i = data["info"]
        print(f"  info       {i['n_dentro']}/{i['n_total']} parametros no IC 90% do BC | "
              f"corr do hiato {i['hiato_corr']} | r* {i['r_is_hoje']}%")
    except Exception as exc:
        print(f"  info       FALHOU -- {exc}")
        data["info"] = {}

    out = render_report(_TEMPLATE, data, output)
    print(f"Relatorio salvo: {out}")


if __name__ == "__main__":
    run()
