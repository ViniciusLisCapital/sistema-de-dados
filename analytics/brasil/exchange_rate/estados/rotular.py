"""Rótulo diário de estado do câmbio USD/BRL (Q0..Q4) a partir dos trechos de rotulos_episodios.csv.

Uso:  uv run python analytics/brasil/exchange_rate/estados/rotular.py

Lê os trechos rotulados por notícia (protocolo_rotulagem.md), valida, e escreve rotulos_diarios.csv com
um rótulo por dia de PTAX de 2006-01-02 a 2026-10-28. A PTAX entra só como grade de pregões.

Regra de prioridade quando mais de um trecho cobre o mesmo pregão:
    Q2  >  Q1 evento  >  Q1 depois  >  Q1 antes  >  Q4      (o evento ganha do fundo)
e, no mesmo nível, vence o trecho mais curto (o mais específico) e depois o que começou mais tarde.
Dia sem trecho nenhum é Q0.

`sobreposicao` = 1 quando o pregão é coberto por mais de um trecho OU quando tem estado diferente de Q0
em novembro ou dezembro (o Q3 não é rotulado, mas está lá; a janela é a mesma da dummy de calendário da
fase 2 — decisão de 2026-10-29). `ids_cobrindo` lista todos
os trechos que cobrem o dia, para a fase 2 poder separar o que estava ao fundo.
"""
from __future__ import annotations

import warnings
from pathlib import Path

import pandas as pd

AQUI = Path(__file__).resolve().parent
EPISODIOS = AQUI / "rotulos_episodios.csv"
SAIDA = AQUI / "rotulos_diarios.csv"
INICIO, FIM = "2006-01-02", "2026-10-28"

COLUNAS = ["id", "episodio", "estado", "fase", "direcao", "inicio", "fim", "gatilho", "fontes",
           "confianca", "sobreposicao", "nota"]
ESTADOS = {"Q1", "Q2", "Q4"}
FASES = {"antes", "evento", "depois"}
DIRECOES = {"↑ dólar", "↓ dólar", "sem direção"}
CONFIANCAS = {"alta", "media", "baixa"}
MESES_Q3 = (11, 12)  # Q3: saída sazonal de fim de ano, mesma janela da dummy da fase 2
RANK = {("Q2", ""): 4, ("Q1", "evento"): 3, ("Q1", "depois"): 2, ("Q1", "antes"): 1, ("Q4", ""): 0}


def pregoes() -> pd.DatetimeIndex:
    from utils import explore as ex

    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        c = ex._conn("macro_brasil")
        df = pd.read_sql(
            "select distinct date from cmb_ptax where name='ptax_venda' "
            f"and date between '{INICIO}' and '{FIM}' order by date", c)
    return pd.DatetimeIndex(pd.to_datetime(df["date"]))


def carregar(dias: pd.DatetimeIndex) -> pd.DataFrame:
    ep = pd.read_csv(EPISODIOS, dtype=str, keep_default_na=False)
    erros = []
    if list(ep.columns) != COLUNAS:
        erros.append(f"colunas {list(ep.columns)} != {COLUNAS}")
    if ep["id"].duplicated().any():
        erros.append(f"id duplicado: {ep.loc[ep['id'].duplicated(), 'id'].tolist()}")
    ep["inicio_d"] = pd.to_datetime(ep["inicio"])
    ep["fim_d"] = pd.to_datetime(ep["fim"])
    for _, r in ep.iterrows():
        p = f"{r['id']}:"
        if r["estado"] not in ESTADOS:
            erros.append(f"{p} estado {r['estado']!r}")
        if (r["estado"] == "Q1") != (r["fase"] in FASES):
            erros.append(f"{p} fase {r['fase']!r} incompatível com {r['estado']}")
        if r["direcao"] not in DIRECOES:
            erros.append(f"{p} direção {r['direcao']!r}")
        if r["estado"] == "Q4" and r["direcao"] == "sem direção":
            erros.append(f"{p} Q4 precisa de direção")
        if r["confianca"] not in CONFIANCAS:
            erros.append(f"{p} confiança {r['confianca']!r}")
        if "http" not in r["fontes"]:
            erros.append(f"{p} sem URL")
        if r["inicio_d"] > r["fim_d"]:
            erros.append(f"{p} início depois do fim")
        for col in ("inicio_d", "fim_d"):
            if r[col] not in dias:
                erros.append(f"{p} {col[:-2]} {r[col].date()} não é pregão da PTAX")
    if erros:
        raise ValueError("rotulos_episodios.csv inválido:\n  " + "\n  ".join(erros))
    ep["n_pregoes"] = [((dias >= a) & (dias <= b)).sum() for a, b in zip(ep["inicio_d"], ep["fim_d"])]
    ep["rank"] = [RANK[(e, f)] for e, f in zip(ep["estado"], ep["fase"])]
    return ep


def rotular(dias: pd.DatetimeIndex, ep: pd.DataFrame) -> pd.DataFrame:
    # ordem de preferência: maior rank, trecho mais curto, início mais tarde
    ep = ep.sort_values(["rank", "n_pregoes", "inicio_d"], ascending=[False, True, False])
    linhas = []
    for d in dias:
        cob = ep[(ep["inicio_d"] <= d) & (ep["fim_d"] >= d)]
        if cob.empty:
            linhas.append((d, "Q0", "", "", "", 0, ""))
            continue
        w = cob.iloc[0]
        sob = int(len(cob) > 1 or d.month in MESES_Q3)
        ids = " | ".join(sorted(cob["id"]))
        linhas.append((d, w["estado"], w["fase"], w["direcao"], w["id"], sob, ids))
    out = pd.DataFrame(linhas, columns=["date", "estado", "fase", "direcao", "id_episodio",
                                        "sobreposicao", "ids_cobrindo"])
    out["date"] = out["date"].dt.strftime("%Y-%m-%d")
    return out


def main() -> None:
    dias = pregoes()
    ep = carregar(dias)
    out = rotular(dias, ep)
    out.to_csv(SAIDA, index=False, encoding="utf-8")
    print(f"{len(ep)} trechos -> {len(out)} pregões em {SAIDA.name}")
    print(out["estado"].value_counts().sort_index().to_string())
    print(f"dias com sobreposição: {out['sobreposicao'].sum()}")


if __name__ == "__main__":
    main()
