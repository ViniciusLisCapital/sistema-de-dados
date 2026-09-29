"""
O modelo agregado do BC tentando antecipar a projecao do Copom -- a comparacao que mostrou
que ele NAO serve para isso, e por que o relatorio de Politica Monetaria usa o delta da Focus.

Saiu de `analytics/brasil/monetary_policy/antecipa_copom.py` em 2026-09-24, quando a pasta de
Politica Monetaria passou a guardar so o relatorio. O metodo que o relatorio usa (ancora + delta
da Focus) continua la; este modulo parte das mesmas linhas de backtest (`ac.backtest()`) e
acrescenta as colunas do modelo.

## O resultado

Nas 18 reunioes da era em que o Copom declara o horizonte (2026-09-24):

| metodo | MAE | direcao da revisao |
|---|---|---|
| ingenuo ("nao vai revisar") | 0,100 p.p. | -- |
| modelo agregado, nossos parametros | 0,138 | 7/12 |
| modelo agregado, modas publicadas do BC | 0,208 | 6/12 |
| **delta da Focus** | **0,079** | **9/12** |

Com as modas do BC o modelo fica PIOR, entao nao e a nossa estimacao -- e a estrutura. A
revisao do BC entre duas reunioes vem sobretudo do IPCA mensal novo e da inercia de curto
prazo, que a pesquisa semanal incorpora e um modelo trimestral nao ve -- aqui t0 fica ate 4,5
meses atras da reuniao, porque um trimestre so fecha quando sai o IPCA do ultimo mes dele.

Duas coisas foram testadas e nao salvaram o modelo, e as duas estao implementadas e medidas
(`backtest(parametros=..., cambio=...)`):

- **Condicionar o cambio** (observado ate o corte, PPC depois) muda o MAE de 0,1452 para
  0,1453. O canal e mudo porque `a3` estimado aqui e 0,0024 contra 0,011 do BC, e porque o
  bloco de administrados -- onde o repasse cambial do BC e 1,65 p.p. por 10% de
  depreciacao, mais que o dobro do de livres -- nao existe no nosso.
- **Usar as modas do BC** piora, como a tabela mostra.

## Os insumos do cenario, todos cortados na data da decisao

| insumo | fonte | armadilha |
|---|---|---|
| r* real | anunciado no RPM (`R_NEUTRA_BC`) | muda 2x na amostra, e o BC AVISA quando muda |
| Selic | `expc_focus_copom` | realizado ate o corte, esperado depois -- ver `curva_selic` |
| pi^A | `expc_focus_periodo`, administrados trimestral | horizonte trimestral vai a 2028T2 |
| cambio | `cmb_ptax` | observado ate o corte, PPC depois; canal quase mudo |
| hiato inicial | `pm_hiato_produto_vintages` | o que o BC publicou, nao o nosso latente |

O painel (`P`) e os estados (`S`) entram na versao corrente, e isso e deliberado: as series
que `simular()` le em t0 -- IPCA, Selic, Focus, cambio, premio -- ou nao sofrem revisao ou
sao indexadas pela data em que o dado existiu. O unico insumo genuinamente revisado e o
hiato, e e justo o que vem do vintage publicado.

## Rodar

    uv run python -m analytics.brasil.structural_model.modelo_agregado.antecipa_modelo

Le os artefatos `modelo_*` de `data/` (gravados por `modelo_agregado.rodar()`) e imprime as
quatro variantes do backtest e a previsao da proxima reuniao com o modelo ao lado da Focus.
Nao grava nada: o artefato que o relatorio le e o `salvar()` de `antecipa_copom`.
"""

from __future__ import annotations

import datetime as dt
import json

import numpy as np
import pandas as pd

from analytics.brasil.monetary_policy import antecipa_copom as ac
from analytics.brasil.structural_model.modelo_agregado import modelo_agregado as ma
from analytics.brasil.structural_model.modelo_agregado.modelo_painel import DATA, q

# Taxa de juros real neutra que o BC declara usar nas projecoes do cenario de referencia,
# pela reuniao em que passou a valer. Extraido da frase do RPM (o `raw_md` guarda so as
# paginas com tabela de projecao, entao a frase esta no PDF):
#   RPM 2024-06-27 p.74  "o Copom decidiu elevar a taxa de juros real neutra utilizada nas
#                         projecoes de 4,5% para 4,75% a.a."   -> decidido na 263a
#   RPM 2024-12-19 p.59  "... de 4,75% para 5,00% a.a."        -> decidido na 267a
#   RPM 2026-06-25 p.66  "A taxa de juros real neutra considerada para as projecoes do
#                         cenario de referencia e 5,00%."      -> reafirma
# As seis edicoes intermediarias nao repetem o numero, o que e o comportamento esperado:
# o BC fixa a neutra e anuncia quando muda.
#
# NAO confundir com a mediana das MEDIDAS de r* do boxe de jun/2024 (4,8% para 2024T2, que
# a p.95 daquela edicao diz ter subido para 5,0%). Aquilo e estimativa da neutra; isto e o
# valor plugado no cenario.
R_NEUTRA_BC = {1: 4.50, 263: 4.75, 267: 5.00}

def r_neutra(nro_reuniao: int) -> float:
    """r* real (% a.a.) que o BC declarava usar na reuniao `nro_reuniao`."""
    validos = [k for k in R_NEUTRA_BC if k <= nro_reuniao]
    return R_NEUTRA_BC[max(validos)]


def _dia_do_ano_tipico() -> dict[int, int]:
    """Dia do ano mediano da k-esima reuniao, medido no historico.

    Serve para datar reunioes que a Focus projeta e o calendario nao cobre (2027, 2028).
    Medido, nao inventado -- o padrao de 8 reunioes por ano e estavel desde 2006.
    """
    d = ac.calendario_reunioes_ordinal()
    rec = d[d["ano"] >= 2006]
    return rec.assign(doy=rec["date"].dt.dayofyear).groupby("k")["doy"].median().astype(int).to_dict()


def _data_do_rotulo(rotulo: str) -> pd.Timestamp | None:
    """'R3/2027' -> data da reuniao (real se conhecida, tipica se nao)."""
    try:
        k, ano = rotulo.upper().lstrip("R").split("/")
        k, ano = int(k), int(ano)
    except (ValueError, AttributeError):
        return None
    d = ac.calendario_reunioes_ordinal()
    hit = d[(d["ano"] == ano) & (d["k"] == k)]
    if len(hit):
        return pd.Timestamp(hit["date"].iloc[0])
    doy = _dia_do_ano_tipico().get(k)
    if doy is None:
        return None
    return pd.Timestamp(dt.date(ano, 1, 1)) + pd.Timedelta(days=int(doy) - 1)


# ── curvas vintage ───────────────────────────────────────────────────────────
def curva_selic(corte: pd.Timestamp, t0: pd.Period, n: int) -> np.ndarray:
    """Caminho TRIMESTRAL de Selic: realizado ate o corte, esperado pela Focus depois.

    A Focus **descarta da curva as reunioes que ja aconteceram** -- na pesquisa de
    21/08/2026 o primeiro rotulo e R6/2026, a 281a; a 280a, de 05/08, sumiu. Como t0 fica
    ate 4,5 meses atras do corte, a janela de projecao COMECA no passado e contem decisoes
    ja tomadas que a curva nao cobre. Entao a escada tem duas metades:

      - reunioes com data ANTES do corte -> `selic_decidida` de `pm_copom_reuniao`, o que
        de fato aconteceu;
      - reunioes com data >= corte -> mediana da Focus na ultima pesquisa <= corte.

    A reuniao que se quer prever cai na segunda metade (a decisao dela e no proprio corte),
    e e isso que se quer: o cenario de referencia do BC condiciona na trajetoria da Focus,
    que ja precifica a decisao do dia.

    O `selic` do painel e a MEDIA trimestral da meta (`para_q(..., 'media')`), entao a
    escada e agregada por media ponderada por dias -- nao pelo valor de fim de trimestre.
    Num trimestre com duas reunioes a diferenca entre as duas convencoes chega a ~10 pb.
    """
    foco = q("macro_brasil", f"""
        SELECT reuniao, mediana FROM expc_focus_copom
        WHERE base_calculo=0 AND tipo_calculo='geral'
          AND date=(SELECT MAX(date) FROM expc_focus_copom
                    WHERE base_calculo=0 AND tipo_calculo='geral'
                      AND date <= '{corte:%Y-%m-%d}')""")
    if foco.empty:
        raise RuntimeError(f"sem curva Focus por reuniao antes de {corte:%Y-%m-%d}")

    reun = q("macro_brasil", """
        SELECT date, selic_anterior, selic_decidida FROM pm_copom_reuniao ORDER BY date""")
    reun["date"] = pd.to_datetime(reun["date"])

    inicio = t0.to_timestamp("Q") + pd.Timedelta(days=1)
    # nivel vigente no primeiro dia da janela: o decidido na ultima reuniao antes dele
    ant = reun[reun["date"] < inicio]
    if ant.empty:
        raise RuntimeError(f"sem decisao de Selic antes de {inicio:%Y-%m-%d}")
    nivel0 = float(ant["selic_decidida"].iloc[-1])

    passos: list[tuple[pd.Timestamp, float]] = []
    # realizado: reunioes na janela que ja ocorreram antes do corte
    for _, r in reun[(reun["date"] >= inicio) & (reun["date"] < corte)].iterrows():
        passos.append((pd.Timestamp(r["date"]), float(r["selic_decidida"])))
    # esperado: rotulos da Focus cuja reuniao cai no corte ou depois
    for _, r in foco.iterrows():
        data = _data_do_rotulo(str(r["reuniao"]))
        if data is not None and data >= corte.normalize():
            passos.append((data, float(r["mediana"])))
    passos.sort()

    idx = pd.period_range(t0 + 1, periods=n, freq="Q")
    dias = pd.date_range(inicio, idx[-1].to_timestamp("Q"), freq="D")
    escada = pd.Series(np.nan, index=dias, dtype=float)
    escada.iloc[0] = nivel0
    for data, v in passos:
        alvo = data + pd.Timedelta(days=1)   # a meta nova vale do dia seguinte
        if alvo in escada.index:
            escada.loc[alvo] = v
    escada = escada.ffill()
    med = escada.groupby(pd.PeriodIndex(escada.index, freq="Q")).mean()
    return med.reindex(idx).ffill().bfill().values


def curva_administrados(corte: pd.Timestamp, t0: pd.Period, n: int) -> np.ndarray:
    """pi^A trimestral (% no trimestre) da Focus, pesquisa <= corte.

    A Focus publica IPCA Administrados em periodicidade trimestral, com `data_referencia`
    no formato 'T/AAAA'. Onde o horizonte trimestral nao alcanca, cai para a mediana ANUAL
    dividida por 4 -- divisao simples, que e a mesma convencao do atalho "Projecao do
    Copom" da aba do motor (o `ipca_4t` acumula somando os quatro trimestres).
    """
    tri = q("macro_brasil", f"""
        SELECT data_referencia, mediana FROM expc_focus_periodo
        WHERE indicador='IPCA Administrados' AND periodicidade='trimestral'
          AND base_calculo=0
          AND date=(SELECT MAX(date) FROM expc_focus_periodo
                    WHERE indicador='IPCA Administrados' AND periodicidade='trimestral'
                      AND base_calculo=0 AND date <= '{corte:%Y-%m-%d}')""")
    por_tri: dict[pd.Period, float] = {}
    for _, r in tri.iterrows():
        s = str(r["data_referencia"]).strip()
        if "/" not in s:
            continue
        k, ano = s.split("/")
        try:
            por_tri[pd.Period(f"{int(ano)}Q{int(k)}", "Q")] = float(r["mediana"])
        except ValueError:
            continue

    anual = q("macro_brasil", f"""
        SELECT data_referencia, mediana FROM expc_focus_periodo
        WHERE indicador='IPCA Administrados' AND periodicidade='anual' AND base_calculo=0
          AND date=(SELECT MAX(date) FROM expc_focus_periodo
                    WHERE indicador='IPCA Administrados' AND periodicidade='anual'
                      AND base_calculo=0 AND date <= '{corte:%Y-%m-%d}')""")
    por_ano = {int(r["data_referencia"]): float(r["mediana"]) / 4.0
               for _, r in anual.iterrows() if str(r["data_referencia"]).isdigit()}

    idx = pd.period_range(t0 + 1, periods=n, freq="Q")
    out, ult = [], None
    for p in idx:
        v = por_tri.get(p, por_ano.get(p.year))
        if v is None:
            v = ult
        out.append(v)
        ult = v
    if out[0] is None:
        raise RuntimeError(f"sem administrados da Focus antes de {corte:%Y-%m-%d}")
    return np.array([x if x is not None else out[0] for x in out], float)


def curva_cambio(corte: pd.Timestamp, t0: pd.Period, n: int,
                 meta: float = 3.0) -> np.ndarray:
    """Variacao trimestral do cambio: observada ate o corte, PPC depois.

    Mesma estrutura da curva de Selic, e pela mesma razao: t0 fica ate 4,5 meses atras do
    corte, entao a janela de projecao COMECA no passado e os primeiros trimestres dela ja
    aconteceram. O cenario de referencia do BC parte do cambio corrente e o faz seguir a
    paridade do poder de compra dai em diante -- e o `de_ppc = (meta - PI_EXT)/4` do
    proprio simulador.

    Sem isto o cenario roda com cambio neutro desde t0, o que apaga o canal que mais move
    a projecao entre duas reunioes. Medido: o backtest sem cambio perde do ingenuo com MAE
    de 0,145 (contra 0,106), e o pior erro isolado e a 267a reuniao (dez/2024), justamente
    a da depreciacao do real -- o modelo baixava a projecao porque a Focus subira a curva
    de Selic, enquanto o BC a subia 0,4 p.p.

    O trimestre que contem o corte entra PARCIAL, com a media dos dias disponiveis. E o
    que existe no conjunto de informacao, e e assim que o BC monta a hipotese cambial.
    """
    d = q("macro_brasil", f"""
        SELECT date, value FROM cmb_ptax
        WHERE name='ptax_venda' AND date <= '{corte:%Y-%m-%d}' ORDER BY date""")
    if d.empty:
        raise RuntimeError(f"sem PTAX antes de {corte:%Y-%m-%d}")
    s = pd.Series(d["value"].astype(float).values,
                  index=pd.to_datetime(d["date"]))
    # media por trimestre, INCLUINDO o parcial da ponta (`para_q` o descartaria)
    med = s.groupby(pd.PeriodIndex(s.index, freq="Q")).mean()
    de_obs = np.log(med).diff() * 100.0

    de_ppc = (float(meta) - ma.PI_EXT) / 4.0
    idx = pd.period_range(t0 + 1, periods=n, freq="Q")
    tri_corte = pd.Period(corte, "Q")
    out = []
    for p in idx:
        if p <= tri_corte and p in de_obs.index and np.isfinite(de_obs.loc[p]):
            out.append(float(de_obs.loc[p]))
        else:
            out.append(de_ppc)
    return np.array(out, float)


def hiato_vintage(corte: pd.Timestamp, t0: pd.Period) -> tuple[float, pd.Timestamp] | None:
    """Hiato do produto em t0 como o BC publicou na ultima edicao antes do corte."""
    d = q("macro_brasil", f"""
        SELECT vintage, value FROM pm_hiato_produto_vintages
        WHERE variavel='central' AND date='{t0.to_timestamp():%Y-%m-%d}'
          AND vintage <= '{corte:%Y-%m-%d}' ORDER BY vintage DESC LIMIT 1""")
    if d.empty:
        return None
    return float(d["value"].iloc[0]), pd.Timestamp(d["vintage"].iloc[0])


# ── motor ────────────────────────────────────────────────────────────────────
def params_bcb() -> tuple[dict, dict]:
    """Modas publicadas pelo BC na Tabela 1 do boxe, do `modelo_validacao.csv`.

    Existe para separar duas perguntas que o backtest confunde: "o modelo nao consegue
    antecipar a revisao" e "a NOSSA estimativa dos parametros nao consegue". Para prever o
    numero do BC, usar os parametros publicados por ele nao e trapaca -- e replicacao, e e
    o unico jeito de saber se o que falha e a estrutura ou o ajuste.

    O motor rodado com estas modas reproduz o IRF publicado do BC com erro absoluto medio
    de 0,030 p.p., picando no mesmo trimestre (ver `validar_irf`), entao a transmissao aqui
    e a deles, nao a nossa.
    """
    V = pd.read_csv(DATA / "modelo_validacao.csv").set_index("param")["bcb"]
    par = {k: float(V[k]) for k in
           ("a1L", "a1I", "a2", "a3", "a4", "a5", "a6", "b1", "b2", "b3", "b5", "delta")}
    phi = {k: float(V[k]) for k in ("f1", "f2", "f3")}
    return par, phi


def _carregar():
    P = pd.read_csv(DATA / "modelo_painel_full.csv", index_col=0)
    S = pd.read_csv(DATA / "modelo_estados.csv", index_col=0)
    P.index = pd.PeriodIndex(P.index, freq="Q")
    S.index = pd.PeriodIndex(S.index, freq="Q")
    par = json.loads((DATA / "modelo_params.json").read_text())
    par = par.get("par", par)
    return P, S, par


def rodar_cenario(nro: int, corte: pd.Timestamp, alvo: pd.Period,
                  P=None, S=None, par=None, *, usar_hiato_bc: bool = True,
                  cambio: bool = True, phi=None) -> dict:
    """Reproduz o cenario de referencia do BC como ele estava no corte, e le o alvo."""
    if P is None:
        P, S, par = _carregar()
    t0 = ac.t0_de(corte)
    n = (alvo - t0).n
    if n < 1:
        raise ValueError(f"alvo {alvo} nao esta a frente de t0 {t0}")
    rr = r_neutra(nro)
    selic = curva_selic(corte, t0, n)
    piA = curva_administrados(corte, t0, n)
    meta_alvo = float(P["meta"].dropna().iloc[-1])
    de = curva_cambio(corte, t0, n, meta_alvo) if cambio else None
    h_bc = hiato_vintage(corte, t0) if usar_hiato_bc else None
    C = ma.simular(P, par, S, n=n, selic=selic, pi_A=piA, de=de, expectativa="eq5",
                   t0=t0, rr=rr, h0=(h_bc[0] if h_bc else None), phi=phi)
    return {
        "nro": nro, "corte": corte, "t0": t0, "alvo": alvo, "n": n,
        "rr": rr, "selic_1t": float(selic[0]), "selic_fim": float(selic[-1]),
        "piA_4t": float(piA[-4:].sum()) if n >= 4 else float(piA.sum()),
        "de_1t": (float(de[0]) if de is not None else None),
        "de_obs": (float(de[:max(1, (pd.Period(corte, "Q") - t0).n)].sum())
                   if de is not None else None),
        "h0": (h_bc[0] if h_bc else float(S["h"].loc[t0])),
        "h0_vintage": (h_bc[1].date().isoformat() if h_bc else "nosso filtro"),
        "ipca_4t": float(C["ipca_4t"].iloc[-1]),
        "h_alvo": float(C["h"].iloc[-1]),
    }


# ── backtest e previsao com o modelo ao lado ────────────────────────────────
def backtest(verbose: bool = True, parametros: str = "nossos",
             cambio: bool = True) -> pd.DataFrame:
    """As linhas do backtest da Focus (`ac.backtest()`) com as colunas do modelo acrescentadas.

    `parametros`: "nossos" (estimados aqui) ou "bcb" (modas publicadas na Tabela 1).
    `cambio`: liga/desliga o condicionamento cambial, para medir o que ele acrescenta.
    """
    P, S, par = _carregar()
    phi = None
    if parametros == "bcb":
        par, phi = params_bcb()
    elif parametros != "nossos":
        raise ValueError("parametros: 'nossos' ou 'bcb'")
    proj = ac.projecoes_bc()
    linhas = []
    for r in ac.backtest(verbose=False).to_dict("records"):
        nro, corte, alvo = int(r["nro"]), pd.Timestamp(r["reuniao"]), pd.Period(r["alvo"], "Q")
        anc = ac._ancora(alvo, corte, proj)
        # a reuniao a que a ancora pertence define o r* que valia quando ela foi feita
        nro_anc = ac._nro_da_ancora(proj, anc)
        try:
            agora = rodar_cenario(nro, corte, alvo, P, S, par, cambio=cambio, phi=phi)
            antes = rodar_cenario(nro_anc, anc["vintage"], alvo, P, S, par,
                                  cambio=cambio, phi=phi)
        except Exception as exc:            # noqa: BLE001
            if verbose:
                print("  %da: cenario falhou -- %s" % (nro, exc))
            continue
        delta = agora["ipca_4t"] - antes["ipca_4t"]
        r.update({
            "delta_modelo": round(delta, 4),
            "previsto": round(r["ancora"] + delta, 4),
            "erro": round(r["ancora"] + delta - r["real"], 4),
            "rr": agora["rr"], "rr_antes": antes["rr"],
            "nivel_modelo": round(agora["ipca_4t"], 4),
            "h0": round(agora["h0"], 4), "h0_vintage": agora["h0_vintage"],
            "piA_4t": round(agora["piA_4t"], 3),
            "selic_fim": round(agora["selic_fim"], 2),
        })
        linhas.append(r)
    D = pd.DataFrame(linhas)
    if verbose and len(D):
        _imprimir(D)
    return D


def _imprimir(D: pd.DataFrame) -> None:
    cab = ("%5s %7s %5s %5s %6s %6s %5s %6s %6s %5s %6s"
           % ("reun", "alvo", "anc", "real", "revis", "delta", "prev", "erro",
              "ing", "r*", "nivel"))
    print("\n" + cab)
    for _, r in D.iterrows():
        print("%5d %7s %5.1f %5.1f %+6.1f %+6.2f %5.2f %+6.2f %+6.2f %5.2f %6.2f"
              % (r["nro"], r["alvo"], r["ancora"], r["real"], r["revisao"],
                 r["delta_modelo"], r["previsto"], r["erro"], r["erro_ingenuo"],
                 r["rr"], r["nivel_modelo"]))
    e, i = D["erro"].abs(), D["erro_ingenuo"].abs()
    print("\n  n = %d" % len(D))
    print("  MAE   modelo %.4f  |  ingenuo %.4f  -> %s (%+.1f%%)"
          % (e.mean(), i.mean(),
             "MODELO GANHA" if e.mean() < i.mean() else "INGENUO GANHA",
             100 * (1 - e.mean() / i.mean())))
    print("  RMSE  modelo %.4f  |  ingenuo %.4f"
          % ((D["erro"] ** 2).mean() ** 0.5, (D["erro_ingenuo"] ** 2).mean() ** 0.5))
    print("  vies  modelo %+.4f  |  ingenuo %+.4f"
          % (D["erro"].mean(), D["erro_ingenuo"].mean()))
    nz = D[D["revisao"].abs() > 1e-9]
    if len(nz):
        acerto = int((np.sign(nz["delta_modelo"]) == np.sign(nz["revisao"])).sum())
        print("  direcao da revisao (excluindo as %d revisoes nulas): %d/%d = %.0f%%"
              % (len(D) - len(nz), acerto, len(nz), 100 * acerto / len(nz)))
    dn = D["nivel_modelo"] - D["real"]
    print("  nivel do modelo vs publicado: vies %+.3f p.p., |medio| %.3f"
          % (dn.mean(), dn.abs().mean()))
    if "tipo" in D:
        for tp, g in D.groupby("tipo"):
            print("  %-9s n=%-3d MAE modelo %.4f | ingenuo %.4f%s"
                  % (tp, len(g), g["erro"].abs().mean(), g["erro_ingenuo"].abs().mean(),
                     ("" if g["erro_focus"].isna().all()
                      else " | focus %.4f" % g["erro_focus"].abs().mean())))
    ac._imprimir(D)


def antecipar(nro: int | None = None, corte=None, verbose: bool = True,
              parametros: str = "nossos", cambio: bool = True) -> dict:
    """A previsao da Focus (`ac.antecipar()`) com o delta do modelo ao lado, para comparar."""
    out = ac.antecipar(nro=nro, corte=corte, verbose=verbose)
    P, S, par = _carregar()
    phi = None
    if parametros == "bcb":
        par, phi = params_bcb()
    proj = ac.projecoes_bc()
    alvo, corte = pd.Period(out["alvo"], "Q"), pd.Timestamp(out["corte_usado"])
    anc = {"vintage": pd.Timestamp(out["ancora_vintage"]), "documento": out["ancora_doc"]}
    nro_anc = ac._nro_da_ancora(proj, anc)
    agora = rodar_cenario(out["nro"], corte, alvo, P, S, par, cambio=cambio, phi=phi)
    antes = rodar_cenario(nro_anc, anc["vintage"], alvo, P, S, par, cambio=cambio, phi=phi)
    delta = agora["ipca_4t"] - antes["ipca_4t"]
    prev = out["ancora"] + delta
    out.update({"delta_modelo": round(delta, 4), "previsto": round(prev, 4),
                "previsto_publicado": round(round(prev, 1), 1),
                "rr": agora["rr"], "nivel_modelo": round(agora["ipca_4t"], 4),
                "h0": round(agora["h0"], 4), "h0_vintage": agora["h0_vintage"],
                "piA_4t": round(agora["piA_4t"], 3),
                "selic_fim": round(agora["selic_fim"], 2)})
    if verbose:
        print("  delta modelo   %+.3f p.p.  ->  %.3f (publicado %.1f)"
              % (delta, prev, out["previsto_publicado"]))
        print("  (corte %s, t0 %s, r* %.2f%%, Selic no alvo %.2f%%, piA 4T %.2f%%, "
              "hiato inicial %+.2f de %s)"
              % (out["corte_usado"], out["t0"], out["rr"], out["selic_fim"],
                 out["piA_4t"], out["h0"], out["h0_vintage"]))
    return out


if __name__ == "__main__":
    for pa in ("nossos", "bcb"):
        for cb in (False, True):
            print("\n" + "=" * 78)
            print("PARAMETROS: %s   |   CAMBIO CONDICIONADO: %s"
                  % (pa.upper(), "sim" if cb else "nao"))
            backtest(parametros=pa, cambio=cb)
    print("\n" + "=" * 78)
    print("PREVISAO DA PROXIMA REUNIAO, COM O MODELO AO LADO DA FOCUS")
    antecipar()
