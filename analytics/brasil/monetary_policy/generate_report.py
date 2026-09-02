"""
Gerador do Panorama de Politica Monetaria em HTML.

Abas de dado, e a fonte de cada uma:

  Motor          modelo agregado rodando NO NAVEGADOR: `_load_motor()` manda o historico
                 e `_motor_cfg()` manda parametros + condicoes iniciais + defaults dos
                 condicionantes, e o JS porta `modelo_agregado.simular()`. E a unica aba
                 em que o usuario move input e ve o modelo responder
  Condicoes      condicoes_copom.montar(): o conjunto de informacao da ultima reuniao
                 contra o de hoje, variavel a variavel, mais a agenda ate a proxima. O
                 corte e um DATETIME (o comunicado sai ~18:30 do dia 2) e a data de
                 divulgacao de cada serie mensal vem do domain/release_calendar/
  Projecoes      pm_copom_projecoes x pm_copom_reuniao: a projecao do BC para o horizonte
                 relevante contra o passo de Selic da MESMA reuniao -- o que o Comite projeta
                 contra o que ele faz. Uma linha por reuniao, nao uma grade de calendario
  Apendice       descricao do modelo (equacoes com os coeficientes estimados) + a tabela
                 de validacao contra a Tabela 1 do boxe

As abas Cenarios, Decomposicao, Taxa Neutra e Hiato do Produto foram REMOVIDAS em
2026-08-25 a pedido do usuario, com os loaders delas. Os artefatos que alimentavam as
quatro continuam sendo gravados por `modelo_agregado.rodar()` em `data/` -- o motor
ainda le `modelo_cenario_focus__eq5.csv` (curva de Selic da Focus) e o teste JS confere
o porte contra os 12 CSVs de cenario.

O que sobrou le os artefatos que `modelo_agregado.rodar()` grava em `data/`.
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
def _load_antecipa(meta_ano: dict, ultimo_ano_meta) -> dict:
    """Previsao para a proxima reuniao + backtest, de `data/` (grava `antecipa_copom.salvar()`).

    Le artefato em vez de rodar o modelo: `antecipar()` roda o espaco de estados duas vezes e
    o backtest 34, o que nao cabe num generate_report. Devolve {} se os arquivos nao existirem
    -- a aba entao mostra so o historico publicado, sem a previsao.

    O `meta` do alvo vem do MESMO dicionario que as linhas publicadas usam, de proposito: na
    escala "desvio da meta" o ponto previsto tem de ser medido contra a mesma regua, incluindo
    a extensao da meta continua de 3% para alem do ultimo ano em `inflc_meta`.
    """
    csv = _HERE / "data" / "antecipa_backtest.csv"
    js = _HERE / "data" / "antecipa_previsao.json"
    if not (csv.exists() and js.exists()):
        return {}
    prev = json.loads(js.read_text(encoding="utf-8"))
    # O diagnostico que faltava: o `corte_usado` gravado no artefato contra o que as
    # fontes tem AGORA. Roda na geracao (o unico momento em que ha MySQL do lado) e vai
    # embutido, entao viaja com o arquivo -- quem receber o HTML por email ve o aviso
    # tambem. `salvar()` e o que conserta; regerar o relatorio, nao.
    try:
        from analytics.brasil.monetary_policy.antecipa_copom import frescor
        prev["frescor"] = frescor(prev.get("corte_usado"))
    except Exception as exc:                                     # noqa: BLE001
        prev["frescor"] = {"erro": f"{type(exc).__name__}: {exc}"}
    ano = int(str(prev["periodo"])[:4])
    mt = meta_ano.get(ano, meta_ano.get(ultimo_ano_meta))
    prev["meta"] = round(mt, 4) if mt is not None else None
    prev["meta_estendida"] = int(ultimo_ano_meta is not None and ano > ultimo_ano_meta)
    bt = pd.read_csv(csv)
    cols = ["nro", "reuniao", "alvo", "tipo", "ancora", "anc_doc", "anc_dias", "real",
            "revisao", "delta_modelo", "previsto", "erro", "erro_ingenuo", "delta_focus",
            "erro_focus", "nivel_modelo", "rr", "t0"]
    bt = bt[[c for c in cols if c in bt.columns]]
    return {"previsao": prev,
            "backtest": json.loads(bt.to_json(orient="records"))}


def _load_projecoes() -> dict:
    """Aba Projecoes do Copom: a projecao do horizonte relevante x o passo de Selic.

    Duas tabelas, uma linha por reuniao cada, casadas por `nro_reuniao`:
    `pm_copom_projecoes` (o que o Comite PROJETA) e `pm_copom_reuniao` (o que ele FEZ).

    Nao passa pelo loop de series por dois motivos: o payload e uma tabela de linhas, nao
    {chave: {dates, values}}, e a unidade de tempo e a REUNIAO, nao um periodo de
    calendario -- reuniao nao cai em grade regular (8 por ano, espacadas de ~45 dias).

    ## Tres filtros, e cada um responde a uma armadilha da fonte

    `horizonte_relevante = 1 & indice = 'ipca'` e o recorte obvio. Os outros dois nao:

    - **`documento`**. A mesma reuniao pode ter DUAS projecoes, uma do comunicado e uma
      do relatorio, com numeros diferentes -- o relatorio e vintage 7 a 28 dias posterior
      e, em 2017-2020, o comunicado publicava o cenario hibrido. Sem filtro a serie
      duplica a reuniao. Aqui o comunicado ganha quando existe: sai no DIA da decisao,
      entao e o conjunto de informacao exato; o relatorio completa o resto. Da 264a em
      diante os dois batem exatos (60 de 60), o que torna a preferencia inocua justo onde
      ela seria mais visivel.
    - **`regime`**. A palavra "horizonte relevante" cobre quatro conceitos diferentes na
      fonte, e so um deles e uma distancia fixa. Aqui a serie e sempre `hr_6_trimestres`
      (comunicado, 2024-07 em diante) ou `hr_aproximado` (relatorio, a regra dos seis
      trimestres aplicada ao caminho continuo que ele publica). Os regimes
      `ano_calendario` e `horizonte_suavizado` do comunicado pre-2024 ficam FORA de
      proposito: o ano calendario encurta de 12 para 4 trimestres a frente ao longo do
      proprio ano, o que poe um dente de serra na serie que nao e mudanca de projecao.
      Custa 14 reunioes de 2020-2024; o que se compra e uma unidade so.

    `cenario` classifica pelo CONDICIONAMENTO, nao pelo rotulo publicado -- "cenario de
    referencia" significava o OPOSTO em 2016-2017 (o rotulo original fica em
    `cenario_publicado`). Levantamento das duas fontes em
    domain/db/brasil/bcb/copom_comunicados.md e relatorio_politica_monetaria.md.

    ## A meta

    `inflc_meta` e ANUAL e termina em 2026; os trimestres projetados vao a 2028. A meta do
    ultimo ano publicado e estendida para frente, o que sob o regime de meta CONTINUA
    (3%, desde 2025) nao e extrapolacao -- e o proprio desenho da meta. Os anos estendidos
    vem marcados em `meta_estendida` e a aba os identifica.

    Escala da projecao: IPCA acumulado em 4 trimestres (%). Nao anualizar, nao acumular.
    """
    proj = _read_table("pm_copom_projecoes")
    reun = _read_table("pm_copom_reuniao")
    meta = _read_table("inflc_meta")

    m = proj[(proj["horizonte_relevante"] == 1) & (proj["indice"] == "ipca")
             & (((proj["documento"] == "relatorio") & (proj["regime"] == "hr_aproximado"))
                | ((proj["documento"] == "comunicado") & (proj["regime"] == "hr_6_trimestres")))]

    # meta por ano, estendida para frente com o ultimo valor publicado
    meta_ano = {int(r["date"].year): float(r["value"])
                for _, r in meta[meta["name"] == "meta_inflacao"].iterrows()}
    ultimo_ano_meta = max(meta_ano) if meta_ano else None

    reun = reun.sort_values("nro_reuniao").reset_index(drop=True)
    # passo da reuniao SEGUINTE, para o seletor de defasagem da aba
    reun["bps_prox"] = reun["variacao_bps"].shift(-1)
    reun["nro_prox"] = reun["nro_reuniao"].shift(-1)
    por_reuniao = reun.set_index("nro_reuniao")

    cenarios: dict[str, list] = {}
    sem_decisao: list[int] = []
    for cen in ("juros_esperado", "juros_constante"):
        linhas = []
        sub = m[m["cenario"] == cen]
        # comunicado ganha do relatorio na mesma reuniao: sai no dia da decisao
        sub = sub.sort_values(["nro_reuniao", "documento"])  # 'comunicado' < 'relatorio'
        for nro, g in sub.groupby("nro_reuniao"):
            r = g.iloc[0]
            if nro not in por_reuniao.index:
                sem_decisao.append(int(nro))
                continue
            d = por_reuniao.loc[nro]
            ano = int(r["date"].year)
            mt = meta_ano.get(ano, meta_ano.get(ultimo_ano_meta))
            linhas.append({
                "nro": int(nro),
                "reuniao": r["vintage"].strftime("%Y-%m-%d") if hasattr(r["vintage"], "strftime")
                           else str(r["vintage"]),
                "decisao_date": pd.Timestamp(d["date"]).strftime("%Y-%m-%d"),
                "periodo": r["date"].strftime("%Y-%m-%d"),
                "qa": int(r["trimestres_a_frente"]),
                "proj": round(float(r["value"]), 4),
                "meta": round(mt, 4) if mt is not None else None,
                "meta_estendida": int(ultimo_ano_meta is not None and ano > ultimo_ano_meta),
                "doc": r["documento"],
                "bps": int(d["variacao_bps"]),
                "bps_prox": None if pd.isna(d["bps_prox"]) else int(d["bps_prox"]),
                "nro_prox": None if pd.isna(d["nro_prox"]) else int(d["nro_prox"]),
                "decisao": d["decisao"],
                "selic_ant": round(float(d["selic_anterior"]), 2),
                "selic_dec": round(float(d["selic_decidida"]), 2),
                "fora": int(d["alterada_fora_da_reuniao"]),
            })
        cenarios[cen] = sorted(linhas, key=lambda x: x["nro"])

    out = {"cenarios": cenarios,
           "sem_decisao": sorted(set(sem_decisao)),
           "ultimo_ano_meta": ultimo_ano_meta}
    out.update(_load_antecipa(meta_ano, ultimo_ano_meta))
    return out


def _load_condicoes() -> dict:
    """Aba Condicoes -> `condicoes_copom.montar()`, que le MySQL e o calendario.

    Nao passa pelo loop de series por dois motivos: o payload e uma tabela de linhas, nao
    {chave: {dates, values}}, e o corte de informacao e um DATETIME (o comunicado sai as
    ~18:30 do dia 2), coisa que o shape de serie nao carrega.

    O modulo faz o trabalho todo; aqui so se registra o que ele avisou. Um aviso nao
    derruba a aba: significa que a data de divulgacao ajustada de algum grupo nao bate com
    o que ja esta no banco, e a linha correspondente ja vem marcada como estimada.
    """
    from analytics.brasil.monetary_policy.condicoes_copom import montar
    return montar()


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
    a = df[(df["documento"] == "comunicado")
           & (df["indice"] == "ipca_administrados")
           & (df["cenario"] == "juros_esperado")
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
    # `documento` no filtro nao e opcional: a mesma reuniao tem projecao do comunicado E do RPM,
    # com numeros que podem diferir, e sem isto a linha escolhida depende da ordem do resultado
    h = df[(df["documento"] == "comunicado")
           & (df["horizonte_relevante"] == 1)
           & (df["cenario"] == "juros_esperado")
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
    }


# ── entry point ──────────────────────────────────────────────────────────────
def run(output: str = "reports/brasil/Monetary Policy.html") -> None:
    print("Carregando dados...")
    data = {"generated_at": datetime.now().strftime("%d/%m/%Y %H:%M")}

    for grupo, loader, label in (
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

    # Fora do loop pelo mesmo motivo do condicoes: o payload e tabela de linhas indexada por
    # REUNIAO, nao {chave: {dates, values}} numa grade de calendario.
    try:
        data["projecoes"] = _load_projecoes()
        pj = data["projecoes"]
        for cen, linhas in pj["cenarios"].items():
            if not linhas:
                print(f"  projecoes  {cen}: vazio")
                continue
            docs = {}
            for x in linhas:
                docs[x["doc"]] = docs.get(x["doc"], 0) + 1
            print(f"  projecoes  {cen}: {len(linhas)} reunioes "
                  f"({linhas[0]['decisao_date']} -> {linhas[-1]['decisao_date']}), "
                  + " + ".join(f"{n} do {d}" for d, n in sorted(docs.items())))
        if pj["sem_decisao"]:
            print(f"             AVISO  {len(pj['sem_decisao'])} reuniao(oes) com projecao e sem "
                  f"linha em pm_copom_reuniao: {pj['sem_decisao']}")
        est = sum(x["meta_estendida"] for x in pj["cenarios"]["juros_esperado"])
        if est:
            print(f"             {est} reunioes projetam periodo depois de "
                  f"{pj['ultimo_ano_meta']}, o ultimo ano com meta publicada -- a meta continua "
                  "de 3% e estendida para frente e marcada na aba")
        if pj.get("previsao"):
            pv = pj["previsao"]
            mae = None
            if pj.get("backtest"):
                errs = [abs(r["erro_focus"]) for r in pj["backtest"]
                        if r.get("erro_focus") is not None]
                mae = sum(errs) / len(errs) if errs else None
            print(f"  previsao   {pv['nro']}a ({pv['data_reuniao']}), horizonte {pv['alvo']}, "
                  f"{pv['tipo']}: ancora {pv['ancora']:.1f} -> focus "
                  f"{pv['previsto_focus_publicado']} / modelo {pv['previsto_publicado']}"
                  + (f" | MAE focus {mae:.3f} em {len(pj['backtest'])} reunioes"
                     if mae is not None else ""))
            # O aviso que importa nao e "o corte e anterior a reuniao" (isso e normal e
            # so vai deixar de ser no dia dela), e "o corte e anterior ao que o banco JA
            # tem": ai a previsao embutida esta velha e regerar o relatorio nao conserta,
            # porque o gerador so le o artefato.
            fr = pv.get("frescor") or {}
            if fr.get("atrasado"):
                print(f"             AVISO  previsao calculada com dado ate "
                      f"{fr['corte']}, mas {fr['fonte_ref']} ja tem {fr['fonte_max']} "
                      f"({fr['dias']}d): rode antecipa_copom.salvar() e regere")
            elif pv["corte_usado"] < pv["data_reuniao"]:
                print(f"             corte de informacao {pv['corte_usado']}, em dia com "
                      f"o banco; ate {pv['data_reuniao']} entram mais boletins")
        else:
            print("  previsao   ausente -- rode antecipa_copom.salvar() para gerar "
                  "data/antecipa_{backtest.csv,previsao.json}")
    except Exception as exc:
        print(f"  projecoes  FALHOU -- {exc}")
        data["projecoes"] = {}

    try:
        data["condicoes"] = _load_condicoes()
        c = data["condicoes"]
        if c.get("erro"):
            print(f"  condicoes  {c['erro']}")
        else:
            r = c["resumo"]
            print(f"  condicoes  {c['ant']['numero']}a ({c['ant']['date']}) -> "
                  f"{c['prox']['numero']}a ({c['prox']['date']}, em {c['prox']['dias']}d) | "
                  f"{r['hawkish']} hawkish / {r['dovish']} dovish / {r['neutro']} neutro / "
                  f"{r['sem_dado']} sem dado novo | saldo {r['saldo']} | "
                  f"{len(c['agenda'])} divulgacoes ate a reuniao")
            for a in c.get("avisos", []):
                print(f"             AVISO  {a}")
    except Exception as exc:
        print(f"  condicoes  FALHOU -- {exc}")
        data["condicoes"] = {}

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
