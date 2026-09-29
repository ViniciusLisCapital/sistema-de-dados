"""
Antecipar a projecao do BC para o horizonte relevante da PROXIMA reuniao do Copom.

Nao e "qual vai ser a inflacao": e "que numero o Copom vai publicar". Sao alvos
diferentes, e o que funciona para o segundo e a **revisao da propria Focus** para o mesmo
trimestre-alvo (correlacao de 0,70 contra a revisao do BC): a revisao do BC entre duas
reunioes vem sobretudo do IPCA mensal novo, que a pesquisa semanal incorpora.

## O resultado

Nas 18 reunioes da era em que o Copom declara o horizonte (2026-09-24): MAE de **0,079** p.p.
pelo delta da Focus contra **0,100** do ingenuo ("nao vai revisar"), direcao da revisao
certa em 9 de 12.

A comparacao com o modelo agregado do BC -- que erra MAIS que o ingenuo, e e o que justifica
ter escolhido a Focus -- saiu deste modulo em 2026-09-24, junto com o modelo: vive em
`analytics/brasil/structural_model/modelo_agregado/antecipa_modelo.py`, que parte das
linhas do `backtest()` daqui e acrescenta as colunas do modelo. Esta pasta guarda so o
relatorio de Politica Monetaria, e o que ele usa depende de tres tabelas
(`expc_focus_periodo`, `pm_copom_projecoes`, `pm_copom_reuniao`) e do calendario.

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

## Rodar

    uv run python analytics/brasil/monetary_policy/antecipa_copom.py

Imprime o backtest e a previsao para a proxima reuniao, e grava os dois artefatos que a aba
Projecoes do Copom le (`data/antecipa_backtest.csv` e `data/antecipa_previsao.json`, via
`salvar()`). Rodar longe da reuniao usa o conjunto de informacao de HOJE, nao o dela -- a
funcao avisa, a caixa da aba avisa, e a previsao precisa ser refeita perto da data. O
relatorio NAO roda nada disso: se os artefatos nao existirem, a aba mostra so o historico
publicado.
"""

from __future__ import annotations

import datetime as dt
import json
import pathlib

import numpy as np
import pandas as pd

from analytics.brasil.monetary_policy.dados import q

_HERE = pathlib.Path(__file__).parent
_DATA = _HERE / "data"

# Dias corridos depois do fim do trimestre para considerar o trimestre FECHADO no conjunto
# de informacao. O IPCA do ultimo mes sai ~dia 10 do mes seguinte; 15 dias cobre com folga
# e nao alcanca o trimestre seguinte.
_DIAS_FECHA_TRI = 15


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


# ── delta da Focus: o metodo que de fato funciona ────────────────────────────
def focus_4t(corte: pd.Timestamp, alvo: pd.Period) -> float | None:
    """IPCA acumulado nos 4 trimestres que terminam em `alvo`, pela Focus <= corte.

    Mesma escala da projecao do BC: variacao acumulada em 4 trimestres, %, COMPOSTA a
    partir das quatro medianas trimestrais da pesquisa. Ate 2026-09-24 era a SOMA delas,
    o que punha o nivel ~0,06 abaixo (3,89 contra 3,95 para 2028T2 na pesquisa de
    18/09/2026). No delta a diferenca e de milesimos -- refeito o backtest nas 18 reunioes,
    MAE 0,0782 somando e 0,0786 compondo, direcao 9/12 nas duas --, entao a troca e pela
    conta certa, nao por ganho. A serie trimestral da Focus comeca na reformulacao de
    2021-09, o que cobre toda a era hr_6_trimestres.
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
    v = d["mediana"].astype(float)
    return float(((1 + v / 100).prod() - 1) * 100)


def delta_focus(corte: pd.Timestamp, corte_ancora: pd.Timestamp,
                alvo: pd.Period) -> float | None:
    """Quanto a Focus mudou de ideia sobre `alvo` entre as duas datas.

    O NIVEL da Focus nao serve de projecao do BC -- ela roda sistematicamente acima (3,95
    contra 3,1 para 2028T2 na pesquisa de 18/09/2026). O DELTA serve, e e o mesmo argumento
    que justifica ancorar em vez de prever nivel: o vies constante cancela na diferenca.
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


def backtest(verbose: bool = True) -> pd.DataFrame:
    """Delta da Focus contra o ingenuo ("nao vai revisar") nas reunioes da era hr_6_trimestres.

    A comparacao com o modelo agregado -- que e o que justifica ter escolhido a Focus -- vive
    em `analytics/brasil/structural_model/modelo_agregado/antecipa_modelo.py`, que parte
    destas mesmas linhas e acrescenta as colunas do modelo.
    """
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
        dfoc = delta_focus(corte, anc["vintage"], alvo)
        linhas.append({
            "nro": nro, "reuniao": corte.date().isoformat(), "alvo": str(alvo),
            "tipo": tipo_horizonte(alvo, corte, proj),
            "t0": str(t0_de(corte)), "ancora": anc["valor"],
            "anc_doc": anc["documento"], "anc_dias": anc["defasagem_dias"],
            "real": real, "revisao": round(real - anc["valor"], 4),
            "erro_ingenuo": round(anc["valor"] - real, 4),
            "delta_focus": (None if dfoc is None else round(dfoc, 4)),
            "erro_focus": (None if dfoc is None
                           else round(anc["valor"] + dfoc - real, 4)),
        })
    D = pd.DataFrame(linhas)
    if verbose and len(D):
        _imprimir(D)
    return D


def _imprimir(D: pd.DataFrame) -> None:
    """O delta da Focus contra o ingenuo, nas reunioes do backtest."""
    if "erro_focus" in D and D["erro_focus"].notna().any():
        F = D[D["erro_focus"].notna()]
        ef = F["erro_focus"].abs()
        print("  --  n = %d" % len(D))
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


def antecipar(nro: int | None = None, corte=None, verbose: bool = True) -> dict:
    """Previsao para a proxima reuniao: ancora publicada + delta da Focus."""
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
           "ancora_dias": anc["defasagem_dias"], "t0": str(t0_de(corte))}
    if verbose:
        print("\n=== %da reuniao, %s -- horizonte relevante %s ==="
              % (nro, out["data_reuniao"], alvo))
        print("  ancora      %.1f  (%s de %s, %dd antes)"
              % (anc["valor"], anc["documento"], out["ancora_vintage"],
                 anc["defasagem_dias"]))
        if dfoc is not None:
            print("  delta FOCUS    %+.3f p.p.  ->  %.3f (publicado %.1f)"
                  % (dfoc, out["previsto_focus"], out["previsto_focus_publicado"]))
        else:
            print("  sem previsao: a Focus nao tem o alvo numa das duas datas do delta")
        if corte.date() < data_reuniao.date():
            print("  AVISO  o corte usado e HOJE, nao a data da reuniao: o conjunto de "
                  "informacao\n         da reuniao ainda nao existe. Rodar de novo perto "
                  "de %s." % out["data_reuniao"])
    return out


# -- artefatos para a aba Projecoes do Copom ---------------------------------
# ── frescor: o corte gravado no artefato contra o que as fontes ja tem ───────
# As tabelas que `antecipar()` consulta sem o modelo, com a coluna que responde "ate quando esta fonte
# foi publicada". `pm_copom_projecoes` vai por VINTAGE: o `date` dela e o periodo projetado
# (vai a 2029), que nao e leitura de frescor nenhuma.
#
# Esta lista e a mesma do `reads:` do procedimento `previsao` em
# domain/dashboards/manifest.yaml. A duplicacao e consciente: aqui ela existe para o
# proprio relatorio se autodiagnosticar quando aberto por fora, sem manifesto nem
# servidor; la, para a aba de status oferecer o botao. Mexeu numa, mexa na outra.
# Cada fonte tem a coluna de data e um NOME que se possa imprimir no relatorio. O nome
# existe porque quem abre a aba nao sabe o que e `expc_focus_periodo`: dizer "a pesquisa
# Focus ja tinha dado de 31/08" e a mesma informacao numa forma que se le.
# So as tres que a previsao SEM o modelo le (2026-09-24). A curva de Selic da Focus, a PTAX
# e o hiato publicado entravam como condicionantes do modelo e sairam com ele.
_FONTES_FRESCOR = {
    "expc_focus_periodo": ("date", "a pesquisa Focus"),
    "pm_copom_projecoes": ("vintage", "as projeções publicadas pelo Copom"),
    "pm_copom_reuniao": ("date", "o histórico de decisões do Copom"),
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



def salvar(corte=None) -> dict:
    """Grava o backtest e a previsao em `data/`, que e o que `generate_report.py` le.

    Dois arquivos, e a separacao e proposital: `antecipa_backtest.csv` e o historico que
    justifica o numero, `antecipa_previsao.json` e o numero. A aba mostra os dois juntos --
    previsao sozinha no grafico parece mais confiavel do que o backtest diz que ela e.

    `corte` fica no JSON de proposito. A previsao usa o conjunto de informacao da data em
    que o relatorio foi gerado, nao o da reuniao -- quem le precisa ver isso.
    """
    D = backtest(verbose=False)
    prev = antecipar(corte=corte, verbose=False)
    _DATA.mkdir(parents=True, exist_ok=True)
    D.to_csv(_DATA / "antecipa_backtest.csv", index=False, encoding="utf-8")
    (_DATA / "antecipa_previsao.json").write_text(
        json.dumps(prev, ensure_ascii=False, indent=2), encoding="utf-8")
    print("  data/antecipa_backtest.csv   %d reunioes" % len(D))
    # So o delta da Focus: desde 2026-09-24 e o unico metodo na aba. Antes esta linha caia no
    # numero do MODELO quando a Focus nao tinha valor, e imprimia "282a -> 3.5" num dia em que a
    # aba mostrava, corretamente, que nao havia ponto previsto.
    pf = prev["previsto_focus_publicado"]
    print("  data/antecipa_previsao.json  %da -> %s (alvo %s, %s)"
          % (prev["nro"], "%.1f" % pf if pf is not None else
             "sem previsao: a Focus nao tem o alvo numa das duas datas do delta",
             prev["alvo"], prev["tipo"]))
    return {"backtest": D, "previsao": prev}


if __name__ == "__main__":
    backtest()
    antecipar()
    salvar()
