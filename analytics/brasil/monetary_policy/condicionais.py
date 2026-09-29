"""
Condicionantes da projecao do Copom, edicao a edicao -- a aba Acompanhamento Condicionais.

Dois hoje:

  hiato()   o hiato do produto como cada edicao do RPM o publicou (pm_hiato_produto_vintages)
  selic()   o caminho da Selic que a pesquisa Focus trazia antes de cada reuniao
            (expc_focus_copom), que e de onde sai a trajetoria de juros do cenario de
            referencia: "a trajetoria para a taxa de juros e extraida da pesquisa Focus",
            diz todo comunicado desde 2020

Nada aqui calcula revisao nem resume nada: o JS deriva isso dos mesmos arrays que desenha.

## O caminho da Selic: tres escolhas, e o que cada uma evita

**Qual pesquisa.** O comunicado nao diz a data. Usamos a ultima pesquisa ate a SEXTA-FEIRA
anterior a decisao, que e o corte que o proprio Copom declara para o cambio do cenario
("cinco dias uteis encerrados na sexta-feira anterior a reuniao", comunicados 214-229) e o
boletim publicado na segunda-feira da semana da reuniao. E convencao nossa, nao dado do BC.
Mediana na janela de 30 dias (`base_calculo = 0`), a do boletim semanal.

**Que data tem cada reuniao futura.** A Focus pergunta pela reuniao pelo numero dela no ano
("R3/2027"), nao pela data. Reunioes passadas e as do calendario que o BC ja publicou entram
na data real -- o calendario oficial vai alem do ano corrente (`pm_copom_calendario`, com as
oito de 2027 desde meados de 2026). As que o BC ainda nao marcou entram ESTIMADAS, com
`estimada` marcado ponto a ponto: a mesma posicao no ultimo ano conhecido, 52 semanas depois
por ano de distancia -- o que a mantem numa quarta-feira. Medido de 2012 a 2027, estimando
cada ano so com os anteriores (128 reunioes): erro mediano de 0 dia, medio de 4,0, mes
errado em 25. A regra anterior, a data TIPICA da posicao (mediana do dia do ano em dez anos),
errava 7,0 dias em media, o mes em 37, e caia em sabado ou domingo. A posicao so e bem
definida com oito reunioes por ano, o regime desde 2006; antes disso eram 12 e a Focus
rotulava diferente (as 13 reunioes de 2004-2005 nao casam), entao a serie comeca em 2006. Um
ano com mais de oito reunioes conhecidas (uma extraordinaria) levanta, porque deslocaria a
posicao de todas as seguintes sem erro nenhum.

**Onde o caminho comeca.** Na Selic VIGENTE na data da pesquisa, e so depois o primeiro passo,
que e a propria reuniao. Sem essa ancora a linha nasce solta no ar, e a distancia entre ela e
a Selic efetiva -- o que o grafico existe para mostrar -- teria de ser adivinhada.

O mapeamento posicao -> reuniao foi conferido contra a decisao: em nenhuma das reunioes desde
2006 a mediana da Focus para a propria reuniao errou por mais de 50 p.b. Um deslocamento de
uma posicao erraria por um ciclo inteiro.
"""

from __future__ import annotations

import bisect
import datetime as dt
import re

import pandas as pd

from analytics.brasil.monetary_policy.dados import q

_DB = "macro_brasil"
# O regime de oito reunioes por ano, e o primeiro em que a numeracao da Focus casa.
PRIMEIRO_ANO = 2006
REUNIOES_POR_ANO = 8
# Pesquisa mais velha que isto em relacao a sexta-feira de corte nao conta como "a pesquisa
# daquela semana" -- o caminho da reuniao fica de fora em vez de herdar um de semanas antes.
FOLGA_PESQUISA_DIAS = 7


# ── hiato ─────────────────────────────────────────────────────────────────────
def hiato() -> dict:
    """Uma entrada por edicao do RPM, so a estimativa `central`.

    Ate a edicao 2024-06 o anexo publica um modelo com banda de +-2 d.p.; de 2024-09 em
    diante, o cenario de referencia com a dispersao de um conjunto de modelos. As faixas
    medem coisas diferentes nos dois regimes e nao sao comparaveis; a central e. E nem ela
    fica dentro da faixa nova: na edicao 2026-06 o central de 2019T1 esta abaixo do p25 dos
    modelos, porque o cenario de referencia nao e a mediana deles.

    `regime` e "esta edicao publica `minimo`?", a mesma regra do docstring do ETL -- nao ha
    coluna para isso no banco.
    """
    df = q(_DB, "SELECT vintage, date, variavel, value FROM pm_hiato_produto_vintages")
    df["vintage"] = pd.to_datetime(df["vintage"])
    df["date"] = pd.to_datetime(df["date"])
    df["value"] = pd.to_numeric(df["value"])
    suite = set(df.loc[df["variavel"] == "minimo", "vintage"])
    cen = df[df["variavel"] == "central"].sort_values(["vintage", "date"])
    edicoes = []
    for vint, g in cen.groupby("vintage"):
        edicoes.append({
            "vintage": vint.strftime("%Y-%m-%d"),
            "regime": "suite" if vint in suite else "banda",
            "dates": g["date"].dt.strftime("%Y-%m-%d").tolist(),
            "values": [round(float(v), 4) for v in g["value"]],
        })
    return {"edicoes": edicoes}


# ── caminho da Selic ─────────────────────────────────────────────────────────
def sexta_anterior(d: dt.date) -> dt.date:
    """A sexta-feira ESTRITAMENTE anterior a `d` (numa sexta, a da semana anterior)."""
    return d - dt.timedelta(days=((d.weekday() - 4) % 7) or 7)


def posicoes(datas: list[dt.date]) -> dict[tuple[int, int], dt.date]:
    """(ano, n) -> data da n-esima reuniao do ano, a partir de PRIMEIRO_ANO.

    Levanta se um ano tiver mais de REUNIOES_POR_ANO: uma reuniao extraordinaria deslocaria
    a posicao de todas as seguintes naquele ano, e o caminho sairia com as datas trocadas
    sem erro nenhum.
    """
    por_ano: dict[int, list[dt.date]] = {}
    for d in sorted(set(datas)):
        if d.year >= PRIMEIRO_ANO:
            por_ano.setdefault(d.year, []).append(d)
    out = {}
    for ano, ds in por_ano.items():
        if len(ds) > REUNIOES_POR_ANO:
            raise ValueError(f"{ano} tem {len(ds)} reunioes conhecidas, mais que "
                             f"{REUNIOES_POR_ANO}: a posicao 'R<n>/{ano}' da Focus deixa de "
                             "identificar a reuniao")
        for i, d in enumerate(ds, 1):
            out[(ano, i)] = d
    return out


def data_da_posicao(ano: int, n: int, pos: dict) -> tuple[dt.date, bool]:
    """Data da reuniao `R<n>/<ano>` e se ela e estimada.

    Estimada: a mesma posicao no ultimo ano em que ela e conhecida, 52 semanas depois por
    ano de distancia (ver o docstring do modulo para a medicao). Sem ano anterior conhecido,
    o seguinte, 52 semanas antes."""
    if (ano, n) in pos:
        return pos[(ano, n)], False
    anos = [a for a, k in pos if k == n]
    antes = [a for a in anos if a < ano]
    a0 = max(antes) if antes else min(anos)
    return pos[(a0, n)] + dt.timedelta(weeks=52 * (ano - a0)), True


_ROTULO = re.compile(r"R(\d+)/(\d{4})$")


def selic(hoje: dt.date | None = None) -> dict:
    """Um caminho por reuniao desde PRIMEIRO_ANO, mais o caminho de HOJE, mais a Selic efetiva.

    Cada caminho: a reuniao que ele condiciona (`nro`, `reuniao`), a data da pesquisa
    (`pesquisa`), a Selic que a reuniao decidiu (`decidida`, nula se ainda nao decidiu) e os
    pontos -- o primeiro e a ancora na Selic vigente na data da pesquisa, os demais uma
    reuniao futura cada, com `rotulos` ("R7/2026") e `estimada` ponto a ponto.

    `hoje` e o caminho da pesquisa mais recente, quando ela e posterior ao corte da ultima
    reuniao ja decidida: e o que esta na mesa para a proxima. `provisorio` diz se o corte
    dela (a sexta-feira anterior) ainda nao chegou -- ate la a pesquisa ainda anda.
    """
    from analytics.brasil.monetary_policy.condicoes_copom import todas_reunioes

    hoje = hoje or dt.date.today()
    reun = todas_reunioes()
    pos = posicoes([r["date"] for r in reun])

    f = q(_DB, "SELECT date, reuniao, mediana FROM expc_focus_copom "
               "WHERE base_calculo = 0 AND tipo_calculo = 'geral' AND date >= '%d-01-01' "
               "ORDER BY date" % (PRIMEIRO_ANO - 1))
    f["date"] = pd.to_datetime(f["date"]).dt.date
    f["mediana"] = pd.to_numeric(f["mediana"])
    por_pesquisa = {d: g for d, g in f.groupby("date")}
    datas_pesquisa = sorted(por_pesquisa)

    decididas = [r for r in reun if r.get("selic") is not None]

    def vigente(d: dt.date) -> float | None:
        """Selic decidida na ultima reuniao ANTES de `d` -- a que vigorava em `d`."""
        ant = [r for r in decididas if r["date"] < d]
        return ant[-1]["selic"] if ant else None

    def caminho(pesquisa: dt.date, reuniao: dict) -> dict | None:
        g = por_pesquisa[pesquisa]
        pts = []
        for rot, v in zip(g["reuniao"], g["mediana"]):
            m = _ROTULO.match(str(rot))
            if not m or pd.isna(v):
                continue
            data, est = data_da_posicao(int(m.group(2)), int(m.group(1)), pos)
            if data < reuniao["date"]:
                continue
            pts.append((data, round(float(v), 4), str(rot), est))
        pts.sort()
        anc = vigente(pesquisa)
        if not pts or anc is None:
            return None
        return {
            "nro": reuniao.get("numero"),
            "reuniao": reuniao["date"].isoformat(),
            "pesquisa": pesquisa.isoformat(),
            "decidida": reuniao.get("selic"),
            "dates": [pesquisa.isoformat()] + [p[0].isoformat() for p in pts],
            "values": [anc] + [p[1] for p in pts],
            "rotulos": [""] + [p[2] for p in pts],
            "estimada": [False] + [p[3] for p in pts],
        }

    caminhos, sem_pesquisa = [], []
    for r in reun:
        if r["date"].year < PRIMEIRO_ANO or r["date"] > hoje:
            continue
        sexta = sexta_anterior(r["date"])
        i = bisect.bisect_right(datas_pesquisa, sexta)
        if not i or (sexta - datas_pesquisa[i - 1]).days > FOLGA_PESQUISA_DIAS:
            sem_pesquisa.append(r.get("numero"))
            continue
        c = caminho(datas_pesquisa[i - 1], r)
        if c:
            caminhos.append(c)

    atual = None
    prox = next((r for r in reun if r["date"] > hoje), None)
    ultima = datas_pesquisa[-1] if datas_pesquisa else None
    if prox and ultima and (not caminhos or ultima > dt.date.fromisoformat(caminhos[-1]["pesquisa"])):
        atual = caminho(ultima, prox)
        if atual:
            atual["provisorio"] = ultima < sexta_anterior(prox["date"])

    # A Selic efetiva comeca na decisao que vigorava no dia da primeira pesquisa -- a ancora
    # do primeiro caminho --, nem antes (seria historia sem caminho nenhum ao lado) nem depois.
    ini = dt.date.fromisoformat(caminhos[0]["pesquisa"]) if caminhos else dt.date(PRIMEIRO_ANO, 1, 1)
    ant = [r["date"] for r in decididas if r["date"] < ini]
    ini = ant[-1] if ant else ini
    ef = [r for r in decididas if ini <= r["date"] <= hoje]
    efetiva = {"dates": [r["date"].isoformat() for r in ef] + [hoje.isoformat()],
               "values": [r["selic"] for r in ef] + [ef[-1]["selic"] if ef else None]}
    return {"caminhos": caminhos, "hoje": atual, "efetiva": efetiva,
            "sem_pesquisa": sem_pesquisa}
