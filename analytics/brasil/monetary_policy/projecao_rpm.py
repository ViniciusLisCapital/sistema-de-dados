"""
A projecao de inflacao do BC edicao a edicao do RPM -- o caminho trimestral INTEIRO, para duas
secoes da aba Projecoes do Copom: o caminho de cada edicao e um trimestre edicao a edicao.

A aba ja tinha um ponto por reuniao (o horizonte relevante). O Relatorio publica o caminho
contiguo, de 6 a 15 trimestres, e o que se acompanha aqui e como cada trimestre -- cada vertice
da tabela 2.2.1 -- foi revisto de uma edicao para a seguinte.

## Fonte: pm_copom_projecoes, e nao uma tabela nova do anexo estatistico

O pedido foi "consumir a tabela 2.2.1 do anexo estatistico do RPM". O mesmo numero ja estava no
banco, lido do TEXTO do relatorio (`documento = 'relatorio'`), e desde 1999 -- o anexo so existe
de set/2021 em diante e, no dia em que saiu o RPM de set/2026, ainda nao tinha a planilha dessa
edicao. Medido em 2026-09-25 nas 20 edicoes que tem os dois: **as 414 celulas de projecao que as
duas fontes tem sao iguais**, e o anexo tem uma a mais, o 2026T1 da edicao de dez/2022. A tabela
de livres e administrados do anexo e ANUAL ate jun/2024 e trimestral so dali em diante, igual ao
texto -- nao acrescenta historia. A conferencia vive em `tests/test_projecao_rpm.py`, e e o que
justifica nao duplicar o dado.

Uma edicao tem dois caminhos com a Selic da Focus: mar/2022, com o Cenario A (petroleo pela curva
futura, "de maior probabilidade" segundo o Comite) e o B (a hipotese usual de petroleo, que o
comunicado da 245a chamou de referencia: 7,1% para 2022). O texto do relatorio -- e portanto esta
serie -- traz o A, que e o do leque e da tabela principal daquela edicao.

## O que entra

- **O cenario de juros esperado** (a Selic da pesquisa Focus). Ate ~2020 o cenario que o BC
  chamava de referencia era o de juros constantes; o esperado e o que ele publica hoje e o unico
  com historia continua. Tres edicoes (mar/2002, dez/2002, mar/2003) publicaram so o constante:
  elas entram com esse cenario, marcadas em `cenario` e listadas em `sem_cenario`, para a pagina
  desenha-las a parte e nao medir revisao atravessando a troca de cenario (pedido de 2026-09-25;
  antes ficavam de fora).
- **So projecao.** A tabela da edicao traz tambem os trimestres ja fechados ("valores em fundo
  branco sao efetivos"); o ETL os descarta (`trimestres_a_frente >= 0`), e o realizado entra aqui
  como serie propria.
- **Livres e administrados trimestrais so existem desde set/2024.** Antes disso, so o IPCA.

## O realizado

IPCA acumulado em quatro trimestres = a variacao em 12 meses no ultimo mes do trimestre. Para o
IPCA, a serie publicada (`ipca_12m`, SGS 13522); para livres e administrados, composta das
variacoes mensais (SGS 11428 e 4449), porque o SGS nao publica o acumulado deles. Conferido contra
os "efetivos" que o anexo imprime (96 celulas, 8 edicoes x 4 trimestres x 3 indices): 95 batem na
primeira casa; administrados de 2026T1 sai 5,44 aqui e 5,5 la -- as variacoes mensais do SGS vem com
duas casas e o BC compoe as dele sem esse arredondamento.

Datas: o 1o mes do trimestre, a mesma convencao de `pm_copom_projecoes.date`.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from analytics.brasil.monetary_policy.dados import q

_DB = "macro_brasil"
INDICES = ("ipca", "ipca_livres", "ipca_administrados")
# nome em inflc_agregados -> indice da projecao; o IPCA vem pelo acumulado publicado
_MENSAL = {"ipca_livres": "ipca_livres", "ipca_administrados": "ipca_administrado"}


def _iso(d) -> str:
    return pd.Timestamp(d).strftime("%Y-%m-%d")


def edicoes() -> tuple[list[dict], list[str]]:
    """Uma entrada por edicao do RPM, em ordem cronologica: o cenario de juros esperado, ou o de
    juros constantes na edicao que so publicou esse.

    Cada uma: `vintage` (publicacao), `nro` (a reuniao que ela condiciona), `cenario`, `hr` (o
    trimestre do horizonte relevante, ou None) e `series` {indice: {dates, values}}, so os indices
    que ela publicou. Devolve tambem as edicoes que nao tem o cenario de juros esperado.
    """
    p = q(_DB, "SELECT vintage, nro_reuniao, indice, cenario, date, value, horizonte_relevante "
               "FROM pm_copom_projecoes WHERE documento = 'relatorio' AND periodo_tipo = 'trimestre'")
    p["vintage"] = pd.to_datetime(p["vintage"])
    p["date"] = pd.to_datetime(p["date"])
    p["value"] = pd.to_numeric(p["value"])
    esp = p[p["cenario"] == "juros_esperado"]
    sem = sorted({_iso(v) for v in p["vintage"]} - {_iso(v) for v in esp["vintage"]})
    # A edicao sem o esperado entra com o de juros constantes, o unico que ela publicou.
    cte = p[(p["cenario"] == "juros_constante") & p["vintage"].map(_iso).isin(sem)]
    faltou = sorted(set(sem) - {_iso(v) for v in cte["vintage"]})
    if faltou:
        raise ValueError(f"edicao sem juros esperado nem constante: {faltou}")

    out = []
    for (vint, nro, cen), g in pd.concat([esp, cte]).groupby(["vintage", "nro_reuniao", "cenario"]):
        series = {}
        for ind in INDICES:
            gi = g[g["indice"] == ind].sort_values("date")
            if len(gi):
                series[ind] = {"dates": [_iso(d) for d in gi["date"]],
                               "values": [round(float(v), 4) for v in gi["value"]]}
        hr = g[(g["horizonte_relevante"] == 1) & (g["indice"] == "ipca")]["date"]
        out.append({"vintage": _iso(vint), "nro": int(nro), "cenario": cen,
                    "hr": _iso(hr.iloc[0]) if len(hr) else None, "series": series})
    out.sort(key=lambda e: e["vintage"])
    return out, sem


def realizado(desde: str) -> dict:
    """{indice: {dates, values}}: o acumulado em quatro trimestres, trimestre a trimestre."""
    d = q(_DB, "SELECT date, name, value FROM inflc_agregados "
               "WHERE name IN ('ipca_12m', 'ipca_livres', 'ipca_administrado') ORDER BY date")
    d["date"] = pd.to_datetime(d["date"])
    d["value"] = pd.to_numeric(d["value"])
    w = d.pivot(index="date", columns="name", values="value").sort_index()
    ac = {"ipca": w["ipca_12m"]}
    for ind, nome in _MENSAL.items():
        m = w[nome]
        # 12 meses COMPLETOS: um mes faltando no meio da janela nao pode virar um acumulado
        # de 11 que parece de 12.
        ac[ind] = (np.exp(np.log1p(m / 100).rolling(12, min_periods=12).sum()) - 1) * 100
    out = {}
    ini = pd.Timestamp(desde)
    for ind, s in ac.items():
        s = s[(s.index.month % 3 == 0)].dropna()
        # o 1o mes do trimestre que termina neste mes
        s.index = s.index - pd.DateOffset(months=2)
        s = s[s.index >= ini]
        out[ind] = {"dates": [_iso(x) for x in s.index],
                    "values": [round(float(v), 4) for v in s.values]}
    return out


def meta() -> tuple[dict, int | None]:
    """{ano: meta} e o ultimo ano publicado. Depois dele vale o ultimo valor: sob a meta
    continua (3%, desde 2025) isso e o desenho da meta, nao extrapolacao."""
    m = q(_DB, "SELECT date, value FROM inflc_meta WHERE name = 'meta_inflacao'")
    anos = {int(pd.Timestamp(r.date).year): round(float(r.value), 4) for r in m.itertuples()}
    return {str(a): v for a, v in sorted(anos.items())}, (max(anos) if anos else None)


def montar() -> dict:
    E, sem = edicoes()
    desde = min(s["dates"][0] for e in E for s in e["series"].values()) if E else "1999-01-01"
    mt, ult = meta()
    return {"indices": list(INDICES), "edicoes": E, "sem_cenario": sem,
            "realizado": realizado(desde), "meta": mt, "ultimo_ano_meta": ult}
