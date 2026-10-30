"""
A aba Expectativas de Juros: o caminho da Selic que a pesquisa Focus espera e o que a curva
DI precifica, reuniao a reuniao, e como os dois andaram semana a semana.

Duas fontes, lidas como o que sao:

  focus()   PESQUISA (`expc_focus_copom`): a mediana do que as instituicoes respondem que o
            Copom vai decidir em cada reuniao, com a dispersao das respostas e a mediana so
            das respostas dos ultimos 4 dias uteis (`base_calculo = 1`)
  di()      PRECO (`br_di_grade`): a taxa que o mercado aceita hoje para emprestar ate cada
            data. Carrega expectativa e premio de prazo juntos, e nada aqui separa um do
            outro -- a curva nao precisa bater com a pesquisa, e nao e lida como previsao

Nenhuma das duas e pontuada contra a decisao do Copom, em lugar nenhum da aba: nao e o
enquadramento do usuario (2026-09-24). A conferencia de que a leitura da curva esta certa
existe, mas mora no teste (`tests/test_expectativas_juros.py`), nao na tela.

## Da curva ao caminho reuniao a reuniao

O procedimento inteiro, com os numeros que decidiram cada escolha, esta em
`caminho_selic_curva_di.md`, nesta pasta. Em resumo:

A curva DI x pre da B3 e montada dos futuros de DI1, que vencem no primeiro dia util de cada
mes, e e flat-forward entre dois vencimentos. A taxa de cada vencimento e a MEDIA composta
dos overnights de hoje ate ele; a Selic e uma escada que muda no dia util seguinte a cada
reuniao. O caminho e a escada cuja media ate cada vencimento reproduz a taxa dele -- e, entre
as escadas que reproduzem quase igualmente bem, a mais lisa: a conta paga um custo por mudar
de uma reuniao para a seguinte (`SUAVIZACAO`), e aceita errar a taxa de um contrato em cerca
de 1 p.b. para nao transformar esse 1 p.b. num degrau. E o que a tela de CDI implicito da
Bloomberg faz: no pregao de 22/09/2026, em que a curva da B3 e exatamente a da tela dela, o
caminho daqui fica a menos de 2 p.b. do dela em todas as reunioes ate dez/2027 (0,7 em media).

Sem o custo, o caminho repete o ruido dos contratos amplificado: a um ano e meio, 1 p.b. a
mais na taxa de UM contrato move o forward daquele mes em ~13 p.b. (a media de ~270 dias uteis
tem de ser carregada pelos ~20 do ultimo mes), e o caminho saia em zigue-zague -- sobe,
desce, sobe -- de reuniao em reuniao, sem que o mercado precificasse nada disso.

A curva e de CDI, que negocia abaixo da meta (0,10 p.p. hoje). O caminho em meta soma a
diferenca do proprio pregao -- meta vigente menos o CDI do primeiro overnight --, que e a que
o mercado pratica naquele dia.

**Dia util e o da epoca do pregao.** A B3 conta com o calendario de feriados vigente no dia:
o 20 de novembro so e feriado nacional desde a Lei 14.759, de 21/12/2023, e um pregao de 2021
conta nov/2024 com um dia util a mais. Com essa regra o calendario daqui reproduz o `du` de
todos os 60.740 vertices de ate 800 dias uteis de uma amostra de um pregao em cada dez; sem
ela, 1.427 divergem.

## Datas das reunioes

As mesmas da aba Acompanhamento Condicionais (`condicionais.posicoes()` e
`data_da_posicao()`): a real onde o Banco Central ja marcou -- o calendario oficial chega ao
ano seguinte (`pm_copom_calendario`) e sao as mesmas datas da Bloomberg --, e a estimada onde
nao marcou (a mesma reuniao do ano anterior, 52 semanas depois), com `est` dizendo qual. As
duas fontes usam a MESMA lista, entao a reuniao j da pesquisa e a reuniao j da curva sao
sempre a mesma reuniao.
"""

from __future__ import annotations

import datetime as dt
import re

import numpy as np
import pandas as pd

from analytics.brasil.monetary_policy.condicionais import (
    PRIMEIRO_ANO,
    REUNIOES_POR_ANO,
    data_da_posicao,
    posicoes,
)
from analytics.brasil.monetary_policy.dados import q

_DB = "macro_brasil"
# Quantos meses de curva entram na conta: dois anos, o mesmo alcance da pesquisa (16
# reunioes desde 2021). Alem disso a curva continua existindo, mas a pergunta da aba e sobre
# as reunioes que a pesquisa tambem cota.
HORIZONTE_MESES = 24
# Custo de mudar a Selic de uma reuniao para a seguinte, contra o erro na taxa dos
# contratos -- as duas coisas em taxa anual em log, entao o numero nao tem unidade. Um degrau
# de 1 p.b. custa o mesmo que errar em ~0,3 p.b. a taxa de um contrato. Calibrado contra a
# tela de CDI implicito da Bloomberg (22 e 24/09/2026): das cinco formas de custo e onze
# pesos testados, e a que fica mais perto dela nos dois dias. Ver caminho_selic_curva_di.md.
SUAVIZACAO = 0.1
# A serie semanal (a ultima data de cada semana) cobre a historia inteira; nos ultimos
# DIARIO_ANOS a aba guarda tambem TODO dia, para o caminho de hoje poder ser comparado com o de
# qualquer data -- inclusive a de ontem (pedido do usuario, 2026-10-29). Toda a historia em
# diario custaria ~90 s a mais de geracao so na curva.
DIARIO_ANOS = 2
# Lei 14.759: o 20 de novembro vira feriado nacional.
_LEI_20NOV = dt.date(2023, 12, 21)
_ROTULO = re.compile(r"R(\d+)/(\d{4})$")


# ── calendario de dias uteis (ANBIMA, como a B3 conta) ──────────────────────────
def feriados(ano: int, pregao: dt.date) -> list[dt.date]:
    """Feriados nacionais de `ano` no calendario que valia no dia `pregao`."""
    from dateutil.easter import easter

    p = easter(ano)
    fs = [dt.date(ano, 1, 1), p - dt.timedelta(48), p - dt.timedelta(47), p - dt.timedelta(2),
          dt.date(ano, 4, 21), dt.date(ano, 5, 1), p + dt.timedelta(60), dt.date(ano, 9, 7),
          dt.date(ano, 10, 12), dt.date(ano, 11, 2), dt.date(ano, 11, 15), dt.date(ano, 12, 25)]
    if ano >= 2024 and pregao >= _LEI_20NOV:
        fs.append(dt.date(ano, 11, 20))
    return fs


_CAL: dict[bool, np.ndarray] = {}


def _cal(pregao: dt.date) -> np.ndarray:
    k = pregao >= _LEI_20NOV
    if k not in _CAL:
        _CAL[k] = np.array([d for a in range(2000, 2046) for d in feriados(a, pregao)],
                           dtype="datetime64[D]")
    return _CAL[k]


def dias_uteis(a: dt.date, b: dt.date, pregao: dt.date) -> int:
    """Dias uteis em [a, b), no calendario da epoca de `pregao`."""
    return int(np.busday_count(np.datetime64(a), np.datetime64(b), holidays=_cal(pregao)))


def _primeiros_dias_uteis(p: dt.date, meses: int) -> list[dt.date]:
    """Primeiro dia util de cada um dos `meses` meses seguintes a `p` -- os vencimentos de DI1."""
    out, y, m = [], p.year, p.month
    for _ in range(meses):
        m += 1
        if m > 12:
            y, m = y + 1, 1
        d = np.busday_offset(np.datetime64(dt.date(y, m, 1)), 0, roll="forward", holidays=_cal(p))
        out.append(pd.Timestamp(d).date())
    return out


# ── a curva num pregao -> um CDI por reuniao ─────────────────────────────────────
def caminho_di(pregao: dt.date, du: np.ndarray, taxa: np.ndarray, reunioes: list[dt.date],
               suavizacao: float = SUAVIZACAO) -> tuple[float, list[float]]:
    """(CDI do primeiro overnight, [CDI depois de cada reuniao]) em % a.a., base 252.

    `du`/`taxa`: a grade do pregao. `reunioes`: datas de decisao >= `pregao`, em ordem; so
    as que caem dentro de HORIZONTE_MESES (e da grade) recebem valor -- a lista devolvida pode
    ser mais curta que a pedida, nunca desalinhada. `suavizacao=0` devolve a escada que MELHOR
    reproduz os vencimentos, sem custo nenhum por degrau: exata numa curva sintetica, e o que o
    teste usa para conferir a convencao de datas.

    Tudo em taxa anual em log (`y = ln(1 + r)`), onde a taxa de um vencimento e a media, em
    dias uteis, dos overnights ate ele -- o que torna a conta linear. Para cada vencimento T:

        media_T(y) = (n0 * y0 + soma_k n_k * y_k) / T

    com n_k os overnights ate T em que vigora o degrau k e y0 o overnight de hoje. Minimiza-se
    soma_T (media_T(y) - taxa_T)^2 + suavizacao * soma_k (y_k - y_(k-1))^2, e a primeira
    diferenca inclui a passagem do CDI de hoje para o da primeira reuniao, como na Bloomberg.
    """
    xs = np.concatenate([[0.0], du.astype(float)])
    lnF = np.concatenate([[0.0], du / 252.0 * np.log1p(taxa / 100.0)])
    fator = lambda d: np.interp(d, xs, lnF)  # noqa: E731  -- flat-forward entre vertices
    y0 = 252 * float(fator(1))
    # Os vencimentos de DI1 (primeiro dia util de cada mes) que a grade cobre.
    venc = [dias_uteis(pregao, t, pregao) for t in _primeiros_dias_uteis(pregao, HORIZONTE_MESES)]
    venc = np.array([v for v in venc if 0 < v <= xs[-1]], float)
    # O degrau k comeca no overnight do dia util SEGUINTE a decisao: o da propria quarta
    # ainda corre na taxa velha.
    ini = [dias_uteis(pregao, m, pregao) + 1 for m in reunioes]
    ini = [s for s in ini if len(venc) and s < venc[-1]]
    K = len(ini)
    if K == 0:
        return float(np.expm1(y0) * 100), []
    T = venc[:, None]
    lo = np.array([0] + ini, float)[None, :]
    hi = np.array(ini + [np.inf], float)[None, :]
    # Quantos overnights ate cada vencimento (linha) correm em cada degrau (coluna).
    n = np.clip(np.minimum(T, hi) - lo, 0, None)
    A = n[:, 1:] / T
    b = 252 * fator(venc) / venc - n[:, 0] * y0 / venc
    D = np.eye(K) - np.eye(K, k=-1)
    d = np.zeros(K)
    d[0] = y0
    w = np.sqrt(suavizacao)
    y, *_ = np.linalg.lstsq(np.vstack([A, w * D]), np.concatenate([b, w * d]), rcond=None)
    return float(np.expm1(y0) * 100), [float(v) for v in np.expm1(y) * 100]


# ── as reunioes ────────────────────────────────────────────────────────────────
def reunioes(ate_ano: int) -> list[dict]:
    """Toda reuniao de PRIMEIRO_ANO a `ate_ano`, na ordem: data (real ou estimada), se e
    estimada, numero e Selic decidida quando ja houve decisao."""
    from analytics.brasil.monetary_policy.condicoes_copom import todas_reunioes

    reun = todas_reunioes()
    pos = posicoes([r["date"] for r in reun])
    por_data = {r["date"]: r for r in reun}
    out = []
    for ano in range(PRIMEIRO_ANO, ate_ano + 1):
        for k in range(1, REUNIOES_POR_ANO + 1):
            d, est = data_da_posicao(ano, k, pos)
            r = por_data.get(d, {}) if not est else {}
            out.append({"ano": ano, "pos": k, "date": d, "est": est,
                        "nro": r.get("numero"), "selic": r.get("selic")})
    return out


def _vigente(reun: list[dict], d: dt.date) -> float | None:
    """Selic decidida na ultima reuniao ANTES de `d` -- a que vigora no overnight de `d`."""
    ant = [r["selic"] for r in reun if r["date"] < d and r["selic"] is not None]
    return ant[-1] if ant else None


def _semanal(datas: pd.Series) -> list[dt.date]:
    """A ultima data de cada semana ISO."""
    s = pd.Series(pd.to_datetime(sorted(set(datas))))
    iso = s.dt.isocalendar()
    return [d.date() for d in s.groupby([iso["year"], iso["week"]]).max()]


def _bloco(pontos: dict[int, dict], campos: list[str]) -> dict:
    """{indice da semana: {campo: valor}} -> {i0, campo: [...]} contiguo, None nos buracos."""
    i0, i1 = min(pontos), max(pontos)
    out = {"i0": i0}
    for c in campos:
        out[c] = [pontos.get(i, {}).get(c) for i in range(i0, i1 + 1)]
    return out


def _j0(reun: list[dict], datas: list[dt.date]) -> list[int]:
    """Para cada semana, o indice da primeira reuniao com decisao na data ou depois dela."""
    ds = [r["date"] for r in reun]
    out, j = [], 0
    for d in datas:
        while j < len(ds) and ds[j] < d:
            j += 1
        out.append(j)
    return out


# ── pesquisa ───────────────────────────────────────────────────────────────────
def focus(reun: list[dict]) -> dict:
    """A Focus semana a semana: a ultima pesquisa de cada semana, por reuniao."""
    f = q(_DB, "SELECT date, reuniao, base_calculo, mediana, desvio_padrao, minimo, maximo, "
               "numero_respondentes FROM expc_focus_copom WHERE tipo_calculo = 'geral' "
               "AND date >= '%d-01-01'" % PRIMEIRO_ANO)
    f["date"] = pd.to_datetime(f["date"]).dt.date
    for c in ("mediana", "desvio_padrao", "minimo", "maximo", "numero_respondentes"):
        f[c] = pd.to_numeric(f[c])
    idx = {(r["ano"], r["pos"]): j for j, r in enumerate(reun)}
    m = f["reuniao"].astype(str).str.extract(_ROTULO)
    f["j"] = [idx.get((int(a), int(n))) if pd.notna(a) else None for n, a in zip(m[0], m[1])]
    f = f[f["j"].notna()]
    f["j"] = f["j"].astype(int)

    b0 = f[f["base_calculo"] == 0]
    datas = _semanal(b0["date"])
    semana = {d: i for i, d in enumerate(datas)}
    b0 = b0[b0["date"].isin(semana)]
    # Base 1 da mesma semana ISO, na ultima data dela: nem sempre o mesmo dia da base 0.
    b1 = f[f["base_calculo"] == 1].copy()
    if len(b1):
        b1["wk"] = [d.isocalendar()[:2] for d in b1["date"]]
        b1 = b1[b1["date"] == b1["wk"].map(b1.groupby("wk")["date"].max())]
    semana_wk = {d.isocalendar()[:2]: i for i, d in enumerate(datas)}

    por_j: dict[int, dict[int, dict]] = {}
    for r in b0.itertuples():
        # Uma reuniao so e "a frente" ate o dia dela: a pesquisa do proprio dia da decisao
        # ainda a cota, a do dia seguinte ja nao.
        if r.date > reun[r.j]["date"]:
            continue
        por_j.setdefault(r.j, {})[semana[r.date]] = {
            "m": _r(r.mediana), "sd": _r(r.desvio_padrao), "lo": _r(r.minimo),
            "hi": _r(r.maximo),
            "n": None if pd.isna(r.numero_respondentes) else int(r.numero_respondentes)}
    for r in b1.itertuples():
        i = semana_wk.get(r.wk)
        if i is None or r.date > reun[r.j]["date"] or i not in por_j.get(r.j, {}):
            continue
        por_j[r.j][i]["b1"] = _r(r.mediana)

    # Todo dia, so a mediana, na janela recente: e o que a comparacao por data le.
    bd = f[f["base_calculo"] == 0]
    bd = bd[bd["date"] >= _inicio_diario(bd["date"].max())]
    dias = sorted(bd["date"].unique())
    dia = {d: i for i, d in enumerate(dias)}
    por_dia: dict[int, dict[int, dict]] = {}
    for r in bd.itertuples():
        if r.date > reun[r.j]["date"]:
            continue
        por_dia.setdefault(r.j, {})[dia[r.date]] = {"m": _r(r.mediana)}
    return {
        "datas": [d.isoformat() for d in datas],
        "vig": [_vigente(reun, d) for d in datas],
        "j0": _j0(reun, datas),
        "por_reuniao": {str(j): _bloco(p, ["m", "b1", "lo", "hi", "sd", "n"])
                        for j, p in sorted(por_j.items())},
        "diario": _serie_diaria(reun, dias, por_dia, "m"),
    }


def _inicio_diario(ultima: dt.date) -> dt.date:
    return (pd.Timestamp(ultima) - pd.DateOffset(years=DIARIO_ANOS)).date()


def _serie_diaria(reun: list[dict], dias: list[dt.date], por_j: dict, campo: str) -> dict:
    """O mesmo formato da serie semanal (datas, vig, j0, por_reuniao), com um campo so."""
    return {
        "datas": [d.isoformat() for d in dias],
        "vig": [_vigente(reun, d) for d in dias],
        "j0": _j0(reun, dias),
        "por_reuniao": {str(j): _bloco(p, [campo]) for j, p in sorted(por_j.items())},
    }


def _r(v, casas=4):
    return None if v is None or pd.isna(v) else round(float(v), casas)


# ── curva ──────────────────────────────────────────────────────────────────────
def di(reun: list[dict]) -> dict:
    """A curva semana a semana: o ultimo pregao de cada semana, lido como um caminho de meta
    Selic por reuniao."""
    g = q(_DB, "SELECT g.date, g.du, g.value FROM br_di_grade g "
               "JOIN (SELECT MAX(date) d FROM br_di_grade GROUP BY YEARWEEK(date, 3)) w "
               "ON g.date = w.d ORDER BY g.date, g.du")
    datas, por_j, spread = _caminhos_di(g, reun)
    # Todo pregao, na janela recente: e o que a comparacao por data le.
    ult = q(_DB, "SELECT MAX(date) d FROM br_di_grade").iloc[0]["d"]
    gd = q(_DB, "SELECT date, du, value FROM br_di_grade WHERE date >= '%s' "
                "ORDER BY date, du" % _inicio_diario(ult).isoformat())
    dias, por_dia, _ = _caminhos_di(gd, reun)
    return {
        "datas": [d.isoformat() for d in datas],
        "vig": [_vigente(reun, d) for d in datas],
        "spread": spread,
        "j0": _j0(reun, datas),
        "por_reuniao": {str(j): _bloco(p, ["v"]) for j, p in sorted(por_j.items())},
        "diario": _serie_diaria(reun, dias, por_dia, "v"),
    }


def _caminhos_di(g: pd.DataFrame, reun: list[dict]):
    """Uma grade por pregao -> (pregoes, {reuniao: {indice do pregao: {v}}}, spread por pregao)."""
    g["date"] = pd.to_datetime(g["date"]).dt.date
    g["value"] = pd.to_numeric(g["value"])
    datas = sorted(g["date"].unique())
    datas_r = [r["date"] for r in reun]
    por_j: dict[int, dict[int, dict]] = {}
    spread = []
    for i, (p, gg) in enumerate(g.groupby("date", sort=True)):
        vig = _vigente(reun, p)
        js = [j for j, d in enumerate(datas_r) if d >= p]
        cdi0, cam = caminho_di(p, gg["du"].to_numpy(), gg["value"].to_numpy(),
                               [datas_r[j] for j in js])
        s = None if vig is None else vig - cdi0
        spread.append(_r(s, 3))
        if s is None:
            continue
        for j, v in zip(js, cam):
            por_j.setdefault(j, {})[i] = {"v": round(v + s, 3)}
    return datas, por_j, spread


# ── opcoes de Copom ─────────────────────────────────────────────────────────────
# Uma opcao vence no dia util seguinte a reuniao; o casamento vencimento -> reuniao aceita
# ate 6 dias corridos (sexta de Carnaval, feriado na quinta) e nunca o proprio dia.
_OPCAO_FOLGA = 6
_OPCAO_SOMA = (80.0, 120.0)


def _chave(x: float) -> str:
    """A chave da decisao como o JS a escreve com String(): -25, nao -25.0; -12.5 fica."""
    return str(int(x)) if x == int(x) else str(x)


def opcoes(reun: list[dict]) -> dict:
    """As opcoes digitais de Copom pregao a pregao (`pm_copom_opcoes`): a probabilidade de cada
    decisao em cada reuniao cotada, e a Selic esperada que sai delas.

    A probabilidade e o premio da decisao sobre a SOMA dos premios da reuniao naquele pregao --
    o premio e valor presente de 100, e a soma e 100 x o fator de desconto, que assim se cancela
    sem curva nenhuma. A Selic esperada para a reuniao j e a vigente mais a variacao esperada
    (sum p x variacao) de cada reuniao ate j; so existe quando TODAS as reunioes de hoje ate j
    tem opcao naquele pregao, senao faltaria um passo no meio da soma."""
    o = q(_DB, "SELECT date, vencimento, variacao_bps, premio FROM pm_copom_opcoes ORDER BY date")
    if o.empty:
        return None
    o["date"] = pd.to_datetime(o["date"]).dt.date
    o["vencimento"] = pd.to_datetime(o["vencimento"]).dt.date
    o["premio"] = pd.to_numeric(o["premio"])
    o["variacao_bps"] = pd.to_numeric(o["variacao_bps"]).astype(float)
    datas_r = [r["date"] for r in reun]
    venc_j = {}
    for v in sorted(o["vencimento"].unique()):
        js = [j for j, d in enumerate(datas_r) if d < v and (v - d).days <= _OPCAO_FOLGA]
        if js:
            venc_j[v] = js[-1]
    o["j"] = o["vencimento"].map(venc_j)
    sem = sorted(set(o.loc[o["j"].isna(), "vencimento"]))
    if sem:
        print(f"  expectativas   opcoes: {len(sem)} vencimento(s) sem reuniao: {sem[:4]}")
    o = o[o["j"].notna()]
    o["j"] = o["j"].astype(int)
    # Reuniao so e "a frente" ate o dia dela, como na pesquisa: o premio do dia da decisao e o
    # da vespera do anuncio, que sai depois do fechamento.
    o = o[o["date"] <= o["j"].map(lambda j: datas_r[j])]

    # A soma dos premios de uma reuniao fica em geral perto de 100 x o desconto (mediana anual
    # de 97 a 99,7), mas cada premio e formado separadamente. Fora de [80, 120] ela nao e uma
    # distribuicao legivel: abaixo, faltam decisoes listadas (em fev/2021 havia reuniao com UM
    # strike, que normalizado sairia 100%); acima, os precos nao conversam entre si.
    soma = o.groupby(["date", "j"])["premio"].transform("sum")
    fora = ~soma.between(_OPCAO_SOMA[0], _OPCAO_SOMA[1])
    if fora.any():
        n = o.loc[fora, ["date", "j"]].drop_duplicates().shape[0]
        print(f"  expectativas   opcoes: {n} reuniao x pregao fora de {_OPCAO_SOMA} na soma, fora da leitura")
    o, soma = o[~fora].copy(), soma[~fora]
    o["p"] = o["premio"] / soma
    datas = sorted(o["date"].unique())
    idx = {d: i for i, d in enumerate(datas)}
    vig = [_vigente(reun, d) for d in datas]
    j0 = _j0(reun, datas)

    por_j: dict[int, dict] = {}
    esp_delta: dict[tuple[int, int], float] = {}
    for (d, j), g in o.groupby(["date", "j"]):
        i = idx[d]
        b = por_j.setdefault(j, {"dec": set(), "pts": {}})
        b["dec"].update(float(x) for x in g["variacao_bps"])
        b["pts"][i] = {"p": dict(zip(g["variacao_bps"], g["p"])),
                       "soma": float(g["premio"].sum())}
        esp_delta[(i, j)] = float((g["p"] * g["variacao_bps"]).sum())

    out_j = {}
    for j, b in sorted(por_j.items()):
        dec = sorted(b["dec"])
        i0, i1 = min(b["pts"]), max(b["pts"])
        p = {_chave(x): [] for x in dec}
        v, dd, sm = [], [], []
        for i in range(i0, i1 + 1):
            pt = b["pts"].get(i)
            for x in dec:
                p[_chave(x)].append(None if pt is None else round(100 * pt["p"].get(x, 0.0), 2))
            sm.append(None if pt is None else round(pt["soma"], 2))
            dd.append(None if pt is None else round(esp_delta[(i, j)], 2))
            # A Selic esperada: a vigente mais o passo esperado de cada reuniao de hoje ate j.
            passos = [esp_delta.get((i, k)) for k in range(j0[i], j + 1)]
            v.append(None if pt is None or vig[i] is None or any(s is None for s in passos)
                     else round(vig[i] + sum(passos) / 100, 4))
        out_j[str(j)] = {"i0": i0, "dec": [int(x) if x == int(x) else x for x in dec],
                         "p": p, "d": dd, "v": v, "soma": sm}
    return {
        "datas": [d.isoformat() for d in datas],
        "vig": vig,
        "j0": j0,
        "por_reuniao": out_j,
    }


def montar() -> dict:
    """O payload da aba. Cada fonte degrada sozinha."""
    anos = q(_DB, "SELECT MAX(date) d FROM expc_focus_copom").iloc[0]["d"]
    ate = pd.Timestamp(anos).year + 3 if anos is not None else dt.date.today().year + 3
    reun = reunioes(ate)
    out: dict = {"reunioes": [{"d": r["date"].isoformat(), "est": r["est"], "nro": r["nro"],
                               "selic": r["selic"], "rot": "R%d/%d" % (r["pos"], r["ano"])}
                              for r in reun]}
    for nome, fn in (("focus", focus), ("di", di), ("opcoes", opcoes)):
        try:
            out[nome] = fn(reun)
        except Exception as exc:  # noqa: BLE001 -- uma fonte que cai nao derruba a outra
            print(f"  expectativas   {nome} FALHOU -- {exc}")
            out[nome] = None
    # Corta a lista de reunioes onde nenhuma fonte cota mais: 2029 inteiro sem ponto nenhum so
    # alargaria o eixo.
    usadas = [int(j) for s in ("focus", "di", "opcoes") if out.get(s) for j in out[s]["por_reuniao"]]
    if usadas:
        out["reunioes"] = out["reunioes"][:max(usadas) + 1]
    return out
