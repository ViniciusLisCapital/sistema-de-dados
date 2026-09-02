"""
Antecipar a projecao do BC para o horizonte relevante da PROXIMA reuniao do Copom.

Nao e "qual vai ser a inflacao": e "que numero o Copom vai publicar". Sao alvos
diferentes, e o segundo se persegue reproduzindo o CENARIO DE REFERENCIA deles -- Selic da
Focus, administrados por fora, e a taxa neutra que eles mesmos anunciam.

## O resultado, antes do metodo

**O modelo agregado nao serve para isto, e o backtest mede quanto.** Nas 17 reunioes da era
em que o Copom declara o horizonte:

| metodo | MAE | direcao da revisao |
|---|---|---|
| ingenuo ("nao vai revisar") | 0,106 p.p. | -- |
| modelo agregado, nossos parametros | 0,145 | 7/12 |
| modelo agregado, modas publicadas do BC | 0,208 | 6/12 |
| **delta da Focus** | **0,082** | **9/12** |

Com as modas do BC o modelo fica PIOR, entao nao e a nossa estimacao -- e a estrutura. O
que funciona e a **revisao da propria Focus** para o mesmo trimestre-alvo, com correlacao
de 0,70 contra a revisao do BC. Faz sentido economico: a revisao do BC entre duas reunioes
vem sobretudo do IPCA mensal novo e da inercia de curto prazo, que a pesquisa semanal
incorpora e um modelo trimestral nao ve -- aqui t0 fica ate 4,5 meses atras da reuniao,
porque um trimestre so fecha quando sai o IPCA do ultimo mes dele.

Duas coisas foram testadas e nao salvaram o modelo, e as duas estao implementadas e
medidas (`backtest(parametros=..., cambio=...)`):

- **Condicionar o cambio** (observado ate o corte, PPC depois) muda o MAE de 0,1452 para
  0,1453. O canal e mudo porque `a3` estimado aqui e 0,0024 contra 0,011 do BC, e porque o
  bloco de administrados -- onde o repasse cambial do BC e 1,65 p.p. por 10% de
  depreciacao, mais que o dobro do de livres -- nao existe no nosso. Com a3 tao pequeno,
  2 p.p. de depreciacao extra valem 0,005 p.p. de inflacao.
- **Usar as modas do BC** piora, como a tabela mostra.

O modelo continua no modulo, com todos os interruptores, porque a comparacao E o resultado:
sem ela, "use a Focus" seria palpite.

## O metodo: ancora + delta, nao nivel

O horizonte relevante e sempre 6 trimestres a frente do TRIMESTRE da reuniao (17/17 na era
em que o Copom o declara), e ha duas reunioes por trimestre. Entao duas reunioes
consecutivas costumam ter o MESMO trimestre-alvo, e o BC ja publicou um numero para ele:

    projecao(281a) = projecao publicada para 2028T1  +  delta

Ancorar existe porque o vies de NIVEL de qualquer previsor aqui e grande e o de DERIVADA
nao. O modelo poe 2028T1 em 3,45 com a nossa r* de 7,81% e em 3,07 com a de 5,00% que o BC
anuncia, contra 3,2 publicado; a Focus poe em 4,02. Nenhum dos tres serve como nivel, e os
tres deltas sao utilizaveis -- o vies constante cancela na diferenca.

## Revisao x expansao de horizonte: os dois casos, e os dois funcionam

Ha duas reunioes por trimestre e o horizonte e 6 trimestres a frente do TRIMESTRE da
reuniao, entao a primeira reuniao de cada trimestre ESTREIA um alvo (expansao) e a segunda
REVISA o dela. Nas 17: **9 expansoes e 8 revisoes, perfeitamente alternadas**, sem uma
excecao.

A expansao nao exige extrapolar nada, e e isto que faz o metodo valer nos dois casos: o
RELATORIO publica o caminho trimestral CONTIGUO, nao so o ponto do horizonte relevante,
entao o trimestre que o comunicado esta estreando ja tem numero publicado la. Nas 9
expansoes a ancora e o relatorio, em todas; nas 8 revisoes e o comunicado anterior. O ramo
"nenhum documento cobre o alvo" -- o unico que precisaria estender uma projecao -- nunca
disparou, e por construcao da fonte nao deve disparar.

E a expansao e o caso MAIS FACIL: MAE de 0,080 pela Focus contra 0,089 do ingenuo, contra
0,084 e 0,125 nas revisoes. O motivo e o intervalo -- a ancora do RPM esta a 34-41 dias da
reuniao e a do comunicado anterior a 35-49, e revisao maior e o que se espera de mais tempo
de noticia acumulada.

O benchmark e severo e e por isso que ele e reportado sempre: as revisoes tem |media| de
0,106 p.p. e 13 das 17 caem dentro de um tique de arredondamento (o BC publica com uma
casa). Um metodo que nao ganhe do ingenuo nao acrescenta nada.

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
hiato, e e justo o que vem do vintage publicado. Isso dispensa reconstruir o painel 17
vezes e dispensa re-rodar o filtro com HP encurtado, que introduziria um erro que nao e do
exercicio.

## Rodar

    uv run python analytics/brasil/monetary_policy/antecipa_copom.py

Imprime as quatro variantes do backtest, o delta da Focus em cada uma, a previsao para a
proxima reuniao, e grava os dois artefatos que a aba Projecoes do Copom le
(`data/antecipa_backtest.csv` e `data/antecipa_previsao.json`, via `salvar()`). Rodar longe
da reuniao usa o conjunto de informacao de HOJE, nao o dela -- a funcao avisa, a caixa da
aba avisa, e a previsao precisa ser refeita perto da data. O relatorio NAO roda o modelo: se
os artefatos nao existirem, a aba mostra so o historico publicado.
"""

from __future__ import annotations

import datetime as dt
import json
import pathlib

import numpy as np
import pandas as pd

from analytics.brasil.monetary_policy import modelo_agregado as ma
from analytics.brasil.monetary_policy.modelo_painel import q

_HERE = pathlib.Path(__file__).parent
_DATA = _HERE / "data"

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

# Dias corridos depois do fim do trimestre para considerar o trimestre FECHADO no conjunto
# de informacao. O IPCA do ultimo mes sai ~dia 10 do mes seguinte; 15 dias cobre com folga
# e nao alcanca o trimestre seguinte.
_DIAS_FECHA_TRI = 15


def r_neutra(nro_reuniao: int) -> float:
    """r* real (% a.a.) que o BC declarava usar na reuniao `nro_reuniao`."""
    validos = [k for k in R_NEUTRA_BC if k <= nro_reuniao]
    return R_NEUTRA_BC[max(validos)]


def t0_de(corte: pd.Timestamp) -> pd.Period:
    """Ultimo trimestre FECHADO no conjunto de informacao de `corte`."""
    tri = pd.Period(corte, "Q")
    while (tri.to_timestamp("Q") + pd.Timedelta(days=_DIAS_FECHA_TRI)) > corte:
        tri -= 1
    return tri


# ── calendario: rotulo Rk/AAAA -> data ───────────────────────────────────────
_CAL: pd.DataFrame | None = None


def calendario_reunioes_ordinal() -> pd.DataFrame:
    """Reunioes com o ordinal DENTRO do ano, que e como a Focus as rotula (R1..R8).

    A Focus nao usa o numero global da reuniao; usa a ordem no ano civil. Junta as
    realizadas (`pm_copom_reuniao`) com as futuras ja agendadas
    (`domain/release_calendar/calendar_2026.yaml`), porque a curva da Focus se estende
    para alem da ultima reuniao realizada.
    """
    global _CAL
    if _CAL is not None:
        return _CAL
    d = q("macro_brasil", "SELECT nro_reuniao, date FROM pm_copom_reuniao ORDER BY date")
    d["date"] = pd.to_datetime(d["date"])
    futuras = _reunioes_agendadas()
    if futuras:
        d = pd.concat([d, pd.DataFrame({"nro_reuniao": [n for n, _ in futuras],
                                        "date": [pd.Timestamp(x) for _, x in futuras]})],
                      ignore_index=True)
    d = d.drop_duplicates("nro_reuniao").sort_values("date").reset_index(drop=True)
    d["ano"] = d["date"].dt.year
    d["k"] = d.groupby("ano").cumcount() + 1
    _CAL = d
    return d


def _reunioes_agendadas() -> list[tuple[int, str]]:
    """Reunioes futuras do `calendar_2026.yaml` (grupo bcb_copom), com o numero do rotulo."""
    import re

    import yaml
    p = _HERE.parents[2] / "domain" / "release_calendar" / "calendar_2026.yaml"
    if not p.exists():
        return []
    cal = yaml.safe_load(p.read_text(encoding="utf-8"))
    g = next((x for x in cal.get("groups", []) if x.get("group") == "bcb_copom"), None)
    out = []
    for e in (g or {}).get("entries", []):
        m = re.match(r"\s*(\d+)", str(e.get("reference_period") or ""))
        if m:
            out.append((int(m.group(1)), str(e["date"])))
    return out


def _dia_do_ano_tipico() -> dict[int, int]:
    """Dia do ano mediano da k-esima reuniao, medido no historico.

    Serve para datar reunioes que a Focus projeta e o calendario nao cobre (2027, 2028).
    Medido, nao inventado -- o padrao de 8 reunioes por ano e estavel desde 2006.
    """
    d = calendario_reunioes_ordinal()
    rec = d[d["ano"] >= 2006]
    return rec.assign(doy=rec["date"].dt.dayofyear).groupby("k")["doy"].median().astype(int).to_dict()


def _data_do_rotulo(rotulo: str) -> pd.Timestamp | None:
    """'R3/2027' -> data da reuniao (real se conhecida, tipica se nao)."""
    try:
        k, ano = rotulo.upper().lstrip("R").split("/")
        k, ano = int(k), int(ano)
    except (ValueError, AttributeError):
        return None
    d = calendario_reunioes_ordinal()
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


# ── ancora ───────────────────────────────────────────────────────────────────
def _ancora(alvo: pd.Period, corte: pd.Timestamp, proj: pd.DataFrame) -> dict | None:
    """Ultima projecao do BC para o MESMO trimestre-alvo, publicada antes do corte.

    Sem filtro de `periodo_tipo` de proposito: a linha de ANO CIVIL e normalizada para o
    4o trimestre daquele ano, e o IPCA acumulado nos 4 trimestres ate o T4 E o ano civil --
    o mesmo objeto economico. Filtrar por 'trimestre' descartaria o comunicado da 270a e
    pegaria um relatorio dois meses mais velho, sem ganho nenhum.
    """
    d = proj[(proj["date"] == alvo.to_timestamp()) & (proj["vintage"] < corte)]
    if d.empty:
        return None
    r = d.sort_values("vintage").iloc[-1]
    return {"valor": float(r["value"]), "documento": r["documento"],
            "vintage": pd.Timestamp(r["vintage"]),
            "periodo_tipo": r["periodo_tipo"],
            "defasagem_dias": int((corte - pd.Timestamp(r["vintage"])).days)}


def projecoes_bc() -> pd.DataFrame:
    """Todas as projecoes de IPCA do BC no cenario de juros esperado, para ancorar."""
    d = q("macro_brasil", """
        SELECT nro_reuniao, documento, vintage, date, value, periodo_tipo,
               horizonte_relevante, regime
        FROM pm_copom_projecoes
        WHERE indice='ipca' AND cenario='juros_esperado'""")
    for c in ("vintage", "date"):
        d[c] = pd.to_datetime(d[c])
    return d


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
    V = pd.read_csv(_DATA / "modelo_validacao.csv").set_index("param")["bcb"]
    par = {k: float(V[k]) for k in
           ("a1L", "a1I", "a2", "a3", "a4", "a5", "a6", "b1", "b2", "b3", "b5", "delta")}
    phi = {k: float(V[k]) for k in ("f1", "f2", "f3")}
    return par, phi


def _carregar():
    P = pd.read_csv(_DATA / "modelo_painel_full.csv", index_col=0)
    S = pd.read_csv(_DATA / "modelo_estados.csv", index_col=0)
    P.index = pd.PeriodIndex(P.index, freq="Q")
    S.index = pd.PeriodIndex(S.index, freq="Q")
    par = json.loads((_DATA / "modelo_params.json").read_text())
    par = par.get("par", par)
    return P, S, par


def rodar_cenario(nro: int, corte: pd.Timestamp, alvo: pd.Period,
                  P=None, S=None, par=None, *, usar_hiato_bc: bool = True,
                  cambio: bool = True, phi=None) -> dict:
    """Reproduz o cenario de referencia do BC como ele estava no corte, e le o alvo."""
    if P is None:
        P, S, par = _carregar()
    t0 = t0_de(corte)
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


# ── delta da Focus: o metodo que de fato funciona ────────────────────────────
def focus_4t(corte: pd.Timestamp, alvo: pd.Period) -> float | None:
    """IPCA acumulado nos 4 trimestres que terminam em `alvo`, pela Focus <= corte.

    Mesma escala da projecao do BC (variacao acumulada em 4 trimestres, %), montada
    somando os quatro trimestres da pesquisa. A serie trimestral da Focus comeca na
    reformulacao de 2021-09, o que cobre toda a era hr_6_trimestres.
    """
    rots = ["%d/%d" % ((alvo - k).quarter, (alvo - k).year) for k in range(4)]
    lista = "','".join(rots)
    d = q("macro_brasil", f"""
        SELECT data_referencia, mediana FROM expc_focus_periodo
        WHERE indicador='IPCA' AND periodicidade='trimestral' AND base_calculo=0
          AND data_referencia IN ('{lista}')
          AND date=(SELECT MAX(date) FROM expc_focus_periodo
                    WHERE indicador='IPCA' AND periodicidade='trimestral'
                      AND base_calculo=0 AND date <= '{corte:%Y-%m-%d}')""")
    if len(d) < 4:
        return None
    return float(d["mediana"].astype(float).sum())


def delta_focus(corte: pd.Timestamp, corte_ancora: pd.Timestamp,
                alvo: pd.Period) -> float | None:
    """Quanto a Focus mudou de ideia sobre `alvo` entre as duas datas.

    O NIVEL da Focus nao serve de projecao do BC -- ela roda sistematicamente acima (4,02
    contra 3,2 para 2028T1 na ultima leitura). O DELTA serve, e e o mesmo argumento que
    justifica ancorar em vez de prever nivel: o vies constante cancela na diferenca.
    """
    a, b = focus_4t(corte, alvo), focus_4t(corte_ancora, alvo)
    return None if (a is None or b is None) else a - b


# ── backtest ─────────────────────────────────────────────────────────────────
def tipo_horizonte(alvo: pd.Period, corte: pd.Timestamp, proj: pd.DataFrame) -> str:
    """"revisao" se o COMUNICADO ja publicou este trimestre-alvo antes do corte, senao "expansao".

    A distincao importa porque os dois casos tem ancora de qualidade diferente, e o padrao e
    perfeitamente alternado: ha duas reunioes por trimestre e o RPM sai uma vez por trimestre,
    entao a primeira reuniao de cada trimestre estreia um alvo (expansao) e a segunda revisa o
    dela (revisao). Nas 17 da amostra: 9 expansoes, 8 revisoes.

    A expansao NAO exige extrapolar nada: o RPM publica o caminho trimestral CONTIGUO, entao o
    trimestre que o comunicado esta estreando ja tem numero publicado la -- e e de onde a ancora
    vem em todas as 9. O ramo "nenhum documento cobre o alvo" nunca dispara na amostra.
    """
    com = proj[(proj["documento"] == "comunicado") & (proj["horizonte_relevante"] == 1)]
    ja = com[(com["date"] == alvo.to_timestamp()) & (com["vintage"] < corte)]
    return "revisao" if len(ja) else "expansao"


def reunioes_hr() -> pd.DataFrame:
    """As reunioes em que o Copom DECLARA o horizonte relevante e ele e uma distancia fixa.

    `regime='hr_6_trimestres'` da 264a (2024-07) em diante. Antes disso a palavra cobre
    outros tres conceitos, e o de ano civil encurta de 12 para 4 trimestres a frente ao
    longo do proprio ano -- misturar poe na serie um degrau que nao e revisao de projecao.
    """
    d = q("macro_brasil", """
        SELECT nro_reuniao, vintage, date, value FROM pm_copom_projecoes
        WHERE documento='comunicado' AND regime='hr_6_trimestres'
          AND horizonte_relevante=1 AND indice='ipca' AND cenario='juros_esperado'
        ORDER BY nro_reuniao""")
    for c in ("vintage", "date"):
        d[c] = pd.to_datetime(d[c])
    return d


def _nro_da_ancora(proj: pd.DataFrame, anc: dict) -> int:
    m = proj[(proj["vintage"] == anc["vintage"]) & (proj["documento"] == anc["documento"])]
    return int(m["nro_reuniao"].iloc[0])


def backtest(verbose: bool = True, parametros: str = "nossos",
             cambio: bool = True) -> pd.DataFrame:
    """Modelo contra o ingenuo ("nao vai revisar") nas reunioes da era hr_6_trimestres.

    `parametros`: "nossos" (estimados aqui) ou "bcb" (modas publicadas na Tabela 1).
    `cambio`: liga/desliga o condicionamento cambial, para medir o que ele acrescenta.
    """
    P, S, par = _carregar()
    phi = None
    if parametros == "bcb":
        par, phi = params_bcb()
    elif parametros != "nossos":
        raise ValueError("parametros: 'nossos' ou 'bcb'")
    proj = projecoes_bc()
    hr = reunioes_hr()

    linhas = []
    for _, r in hr.iterrows():
        nro = int(r["nro_reuniao"])
        corte = pd.Timestamp(r["vintage"])
        alvo = pd.Period(r["date"], "Q")
        real = float(r["value"])
        anc = _ancora(alvo, corte, proj)
        if anc is None:
            if verbose:
                print("  %da: sem ancora para %s -- fora do backtest" % (nro, alvo))
            continue
        # a reuniao a que a ancora pertence define o r* que valia quando ela foi feita
        nro_anc = _nro_da_ancora(proj, anc)
        try:
            agora = rodar_cenario(nro, corte, alvo, P, S, par, cambio=cambio, phi=phi)
            antes = rodar_cenario(nro_anc, anc["vintage"], alvo, P, S, par,
                                  cambio=cambio, phi=phi)
        except Exception as exc:            # noqa: BLE001
            if verbose:
                print("  %da: cenario falhou -- %s" % (nro, exc))
            continue
        delta = agora["ipca_4t"] - antes["ipca_4t"]
        dfoc = delta_focus(corte, anc["vintage"], alvo)
        linhas.append({
            "nro": nro, "reuniao": corte.date().isoformat(), "alvo": str(alvo),
            "tipo": tipo_horizonte(alvo, corte, proj),
            "t0": str(agora["t0"]), "ancora": anc["valor"],
            "anc_doc": anc["documento"], "anc_dias": anc["defasagem_dias"],
            "real": real, "revisao": round(real - anc["valor"], 4),
            "delta_modelo": round(delta, 4),
            "previsto": round(anc["valor"] + delta, 4),
            "erro": round(anc["valor"] + delta - real, 4),
            "erro_ingenuo": round(anc["valor"] - real, 4),
            "delta_focus": (None if dfoc is None else round(dfoc, 4)),
            "erro_focus": (None if dfoc is None
                           else round(anc["valor"] + dfoc - real, 4)),
            "rr": agora["rr"], "rr_antes": antes["rr"],
            "nivel_modelo": round(agora["ipca_4t"], 4),
            "h0": round(agora["h0"], 4), "h0_vintage": agora["h0_vintage"],
            "piA_4t": round(agora["piA_4t"], 3),
            "selic_fim": round(agora["selic_fim"], 2),
        })
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
    if "erro_focus" in D and D["erro_focus"].notna().any():
        F = D[D["erro_focus"].notna()]
        ef = F["erro_focus"].abs()
        print("  --")
        print("  MAE   delta da FOCUS %.4f  (n=%d)  ->  %s o ingenuo (%+.1f%%)"
              % (ef.mean(), len(F),
                 "GANHA de" if ef.mean() < F["erro_ingenuo"].abs().mean() else "PERDE para",
                 100 * (1 - ef.mean() / F["erro_ingenuo"].abs().mean())))
        nzf = F[F["revisao"].abs() > 1e-9]
        if len(nzf):
            ok = int((np.sign(nzf["delta_focus"]) == np.sign(nzf["revisao"])).sum())
            print("  direcao pela Focus: %d/%d = %.0f%%  |  corr(delta, revisao) = %.3f"
                  % (ok, len(nzf), 100 * ok / len(nzf),
                     F["delta_focus"].corr(F["revisao"])))


def antecipar(nro: int | None = None, corte=None, verbose: bool = True,
              parametros: str = "nossos", cambio: bool = True) -> dict:
    """Previsao para a proxima reuniao: ancora publicada + delta do modelo."""
    P, S, par = _carregar()
    phi = None
    if parametros == "bcb":
        par, phi = params_bcb()
    proj = projecoes_bc()
    cal = calendario_reunioes_ordinal()
    hr = reunioes_hr()
    ult = int(hr["nro_reuniao"].iloc[-1])
    nro = (ult + 1) if nro is None else int(nro)
    linha = cal[cal["nro_reuniao"] == nro]
    if linha.empty:
        raise RuntimeError("reuniao %d nao esta no calendario" % nro)
    data_reuniao = pd.Timestamp(linha["date"].iloc[0])
    # 6 trimestres a frente do TRIMESTRE da reuniao -- a regra vale 17/17 na era declarada
    alvo = pd.Period(data_reuniao, "Q") + 6
    corte = pd.Timestamp(dt.date.today()) if corte is None else pd.Timestamp(corte)

    anc = _ancora(alvo, corte, proj)
    if anc is None:
        raise RuntimeError("sem ancora publicada para %s" % alvo)
    nro_anc = _nro_da_ancora(proj, anc)

    agora = rodar_cenario(nro, corte, alvo, P, S, par, cambio=cambio, phi=phi)
    antes = rodar_cenario(nro_anc, anc["vintage"], alvo, P, S, par,
                          cambio=cambio, phi=phi)
    delta = agora["ipca_4t"] - antes["ipca_4t"]
    prev = anc["valor"] + delta
    dfoc = delta_focus(corte, anc["vintage"], alvo)
    out = {"nro": nro, "data_reuniao": data_reuniao.date().isoformat(), "alvo": str(alvo),
           "periodo": alvo.to_timestamp().date().isoformat(),
           "tipo": tipo_horizonte(alvo, corte, proj),
           "delta_focus": (None if dfoc is None else round(dfoc, 4)),
           "previsto_focus": (None if dfoc is None else round(anc["valor"] + dfoc, 4)),
           "previsto_focus_publicado": (None if dfoc is None
                                        else round(round(anc["valor"] + dfoc, 1), 1)),
           "corte_usado": corte.date().isoformat(), "ancora": anc["valor"],
           "ancora_doc": anc["documento"], "ancora_vintage": anc["vintage"].date().isoformat(),
           "ancora_dias": anc["defasagem_dias"],
           "delta_modelo": round(delta, 4), "previsto": round(prev, 4),
           "previsto_publicado": round(round(prev, 1), 1),
           "rr": agora["rr"], "nivel_modelo": round(agora["ipca_4t"], 4),
           "h0": round(agora["h0"], 4), "h0_vintage": agora["h0_vintage"],
           "piA_4t": round(agora["piA_4t"], 3),
           "selic_fim": round(agora["selic_fim"], 2), "t0": str(agora["t0"])}
    if verbose:
        print("\n=== %da reuniao, %s -- horizonte relevante %s ==="
              % (nro, out["data_reuniao"], alvo))
        print("  ancora      %.1f  (%s de %s, %dd antes)"
              % (anc["valor"], anc["documento"], out["ancora_vintage"],
                 anc["defasagem_dias"]))
        print("  delta modelo   %+.3f p.p.  ->  %.3f (publicado %.1f)"
              % (delta, prev, out["previsto_publicado"]))
        if dfoc is not None:
            print("  delta FOCUS    %+.3f p.p.  ->  %.3f (publicado %.1f)   <-- metodo "
                  "com MAE de 0,082 no backtest, contra 0,106 do ingenuo e 0,145 do modelo"
                  % (dfoc, out["previsto_focus"], out["previsto_focus_publicado"]))
        print("  (corte %s, t0 %s, r* %.2f%%, Selic no alvo %.2f%%, piA 4T %.2f%%, "
              "hiato inicial %+.2f de %s)"
              % (out["corte_usado"], out["t0"], out["rr"], out["selic_fim"],
                 out["piA_4t"], out["h0"], out["h0_vintage"]))
        if corte.date() < data_reuniao.date():
            print("  AVISO  o corte usado e HOJE, nao a data da reuniao: o conjunto de "
                  "informacao\n         da reuniao ainda nao existe. Rodar de novo perto "
                  "de %s." % out["data_reuniao"])
    return out


# -- artefatos para a aba Projecoes do Copom ---------------------------------
# ── frescor: o corte gravado no artefato contra o que as fontes ja tem ───────
# As tabelas que `antecipar()` consulta, com a coluna que responde "ate quando esta fonte
# foi publicada". `pm_copom_projecoes` e `pm_hiato_produto_vintages` vao por VINTAGE: o
# `date` das duas e o periodo projetado (vai a 2028), que nao e leitura de frescor nenhuma.
#
# Esta lista e a mesma do `reads:` do procedimento `previsao` em
# domain/dashboards/manifest.yaml. A duplicacao e consciente: aqui ela existe para o
# proprio relatorio se autodiagnosticar quando aberto por fora, sem manifesto nem
# servidor; la, para a aba de status oferecer o botao. Mexeu numa, mexa na outra.
# Cada fonte tem a coluna de data e um NOME que se possa imprimir no relatorio. O nome
# existe porque quem abre a aba nao sabe o que e `expc_focus_periodo`: dizer "a pesquisa
# Focus ja tinha dado de 31/08" e a mesma informacao numa forma que se le.
_FONTES_FRESCOR = {
    "expc_focus_periodo": ("date", "a pesquisa Focus"),
    "expc_focus_copom": ("date", "a pesquisa Focus (curva do Copom)"),
    "pm_copom_projecoes": ("vintage", "as projeções publicadas pelo Copom"),
    "pm_copom_reuniao": ("date", "o histórico de decisões do Copom"),
    "pm_hiato_produto_vintages": ("vintage", "o hiato do produto publicado pelo BC"),
    "cmb_ptax": ("date", "a taxa de câmbio PTAX"),
}


def frescor(corte_usado: str | None) -> dict:
    """O corte gravado no artefato contra o MAX de cada fonte HOJE.

    Existe porque um artefato calculado tem DUAS datas e so uma delas e visivel: quando
    foi ESCRITO (mtime — que `salvar()` move e regerar o relatorio nao) e com que
    CONJUNTO DE INFORMACAO (o `corte_usado`, que so ele grava). Sem comparar a segunda
    com o banco, o relatorio sai novo com previsao velha e a unica pista e esse campo no
    meio da prosa da caixa. Foi o que aconteceu em 2026-08-31.

    Devolve `{}` sem corte, e cada fonte que falhar entra com `ultimo: None`: isto e um
    aviso sobre a geracao, nao pode derrubar a geracao.
    """
    if not corte_usado:
        return {}
    fontes, mx, mx_ref, mx_nome = [], None, None, None
    for tab, (col, nome) in _FONTES_FRESCOR.items():
        try:
            v = q("macro_brasil", f"SELECT MAX({col}) AS mx FROM {tab}").iloc[0, 0]
            u = None if v is None else str(pd.Timestamp(v).date())
        except Exception:                                        # noqa: BLE001
            u = None
        fontes.append({"tabela": tab, "coluna": col, "nome": nome, "ultimo": u})
        if u and (mx is None or u > mx):
            mx, mx_ref, mx_nome = u, tab, nome

    corte = str(corte_usado)
    if mx is None:
        return {"corte": corte, "fontes": fontes, "atrasado": None}
    return {"corte": corte, "fontes": fontes, "fonte_max": mx, "fonte_ref": mx_ref,
            "fonte_nome": mx_nome, "atrasado": corte < mx,
            "dias": int((pd.Timestamp(mx) - pd.Timestamp(corte)).days)}



def salvar(corte=None, parametros: str = "nossos", cambio: bool = True) -> dict:
    """Grava o backtest e a previsao em `data/`, que e o que `generate_report.py` le.

    Dois arquivos, e a separacao e proposital: `antecipa_backtest.csv` e o historico que
    justifica o numero, `antecipa_previsao.json` e o numero. A aba mostra os dois juntos --
    previsao sozinha no grafico parece mais confiavel do que o backtest diz que ela e.

    A variante gravada e a que ganha no backtest (parametros nossos, cambio ligado). As
    outras tres continuam acessiveis por `backtest(parametros=, cambio=)` e nao entram no
    relatorio: elas existem para separar "a estrutura falha" de "o ajuste falha", que e
    argumento de modulo, nao de aba.

    `corte` fica no JSON de proposito. A previsao usa o conjunto de informacao da data em
    que o relatorio foi gerado, nao o da reuniao -- quem le precisa ver isso.
    """
    D = backtest(verbose=False, parametros=parametros, cambio=cambio)
    prev = antecipar(corte=corte, verbose=False, parametros=parametros, cambio=cambio)
    _DATA.mkdir(parents=True, exist_ok=True)
    D.to_csv(_DATA / "antecipa_backtest.csv", index=False, encoding="utf-8")
    prev["parametros"] = parametros
    prev["cambio_condicionado"] = int(bool(cambio))
    (_DATA / "antecipa_previsao.json").write_text(
        json.dumps(prev, ensure_ascii=False, indent=2), encoding="utf-8")
    print("  data/antecipa_backtest.csv   %d reunioes" % len(D))
    print("  data/antecipa_previsao.json  %da -> %.1f (alvo %s, %s)"
          % (prev["nro"], prev["previsto_focus_publicado"] or prev["previsto_publicado"],
             prev["alvo"], prev["tipo"]))
    return {"backtest": D, "previsao": prev}


if __name__ == "__main__":
    for pa in ("nossos", "bcb"):
        for cb in (False, True):
            print("\n" + "=" * 78)
            print("PARAMETROS: %s   |   CAMBIO CONDICIONADO: %s"
                  % (pa.upper(), "sim" if cb else "nao"))
            backtest(parametros=pa, cambio=cb)
    print("\n" + "=" * 78)
    print("PREVISAO E ARTEFATOS (variante que ganha: parametros nossos, cambio ligado)")
    antecipar()
    salvar()
