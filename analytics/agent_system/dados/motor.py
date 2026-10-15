"""
O motor de A → F(A), igual para todo agente. Cada agente só declara as tabelas dele (ver
`cambio.py`): o recorte de cada uma, as séries que entram no F e a leitura de cada série.

Três garantias, cada uma contra um defeito silencioso:

  - A declaração bate com a lista do SISTEMA_AGENTES.md (seção V) ou o gerador levanta. A
    lista é decidida com o usuário; o código não pode ganhar nem perder uma tabela calado.
  - F é calculado a partir dos ARQUIVOS de A, nunca do banco. É isso que faz o F(A) e as
    funções G do agente olharem exatamente o mesmo dado.
  - A é extraído uma vez por ciclo e compartilhado entre os agentes. Um segundo agente que
    declare a mesma tabela com o mesmo nome de recorte e outra consulta faz o gerador
    levantar, em vez de reaproveitar um arquivo que não é o que ele pediu.

As leituras de série (o F genérico):

  pct         nível de preço ou índice: variação % em 1, 3 e 12 meses
  dif         taxa, spread, posição, % do PIB: diferença na unidade da série
  fluxo       fluxo mensal (ou diário, somado em meses): último mês, somas de 3 e 12 meses
  media       volume diário: média em 1, 3 e 12 meses
  var_mensal  variação % mensal (inflação): último mês e acumulados compostos

Profundidade (IV.iv): o grupo "Endógeno" da lista recebe a leitura completa (posição no
histórico, mínimo e máximo de 10 anos); os outros grupos, a enxuta.
"""

from __future__ import annotations

import datetime as dt
import gzip
import json
import re
import unicodedata
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable

import numpy as np
import pandas as pd

RAIZ = Path(__file__).resolve().parents[3]
CICLOS = RAIZ / "obsidian" / "ciclos"
SISTEMA = RAIZ / "SISTEMA_AGENTES.md"

_SCHEMA = {"brasil": "macro_brasil", "international": "macro_international", "us": "macro_us"}
_COLS_DATA = ("date", "date_start", "vintage", "ref_date")
_GRUPO_COMPLETO = "Endógeno"
_JANELAS = (("1m", 1), ("3m", 3), ("12m", 12))


# ── declaração ────────────────────────────────────────────────────────────────
@dataclass(frozen=True)
class Serie:
    chave: str                 # valor da(s) coluna(s) de dimensão, unidos por "|"
    rotulo: str
    unidade: str
    leitura: str               # pct | dif | fluxo | media | var_mensal
    escala: float = 1.0        # o valor do banco é dividido por isto
    casas: int = 2
    pib: bool = False          # fluxo em US$ milhões: soma de 12 meses em % do PIB
    eventos: bool = False      # fluxo diário em que dia sem linha é zero (intervenções)


@dataclass
class Tabela:
    nome: str
    recorte: str | None = None           # o rótulo entre parênteses na lista (V)
    filtro: str = ""                     # SQL depois do WHERE, com %(x)s
    params: dict = field(default_factory=dict)
    corte: str | None = "date"           # coluna limitada à data do ciclo; None = sem limite
    dims: tuple[str, ...] = ("name",)
    valor: str = "value"
    series: tuple[Serie, ...] = ()
    especial: Callable | None = None     # F próprio: (df, ctx) -> linhas de markdown
    fora: str | None = None              # está na lista mas não entra: o motivo
    nota: str | None = None              # defeito conhecido do dado, impresso no F

    @property
    def arquivo(self) -> str:
        return self.nome + (f"__{_slug(self.recorte)}" if self.recorte else "") + ".csv.gz"


def _slug(s: str) -> str:
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", "_", s.lower()).strip("_")


# ── a lista do SISTEMA_AGENTES.md ─────────────────────────────────────────────
_RE_GRUPO = re.compile(r"^### ([ivx]+)\. (.+?)\s*$")
_RE_ITEM = re.compile(r"^\s*- `([A-Za-z0-9_]+)`(?: \(([^)]+)\))?: (.+?)\s*$")


def ler_lista(secao: tuple[str, str]) -> list[dict]:
    """Os grupos e itens da lista de um agente: [{id, nome, itens: [{tabela, recorte, papel}]}]."""
    texto = SISTEMA.read_text(encoding="utf-8")
    i = texto.index(secao[0])
    j = texto.index(secao[1], i)
    grupos: list[dict] = []
    for linha in texto[i:j].splitlines():
        if m := _RE_GRUPO.match(linha):
            grupos.append({"id": m.group(1), "nome": m.group(2), "itens": []})
        elif (m := _RE_ITEM.match(linha)) and grupos:
            grupos[-1]["itens"].append({"tabela": m.group(1), "recorte": m.group(2),
                                        "papel": m.group(3)})
    return grupos


def conferir(tabelas: list[Tabela], grupos: list[dict]) -> None:
    lista = {(it["tabela"], it["recorte"]) for g in grupos for it in g["itens"]}
    decl = [(t.nome, t.recorte) for t in tabelas]
    dup = {k for k in decl if decl.count(k) > 1}
    faltam, sobram = lista - set(decl), set(decl) - lista
    if dup or faltam or sobram:
        raise ValueError("A declaração não bate com a lista do SISTEMA_AGENTES.md: "
                         f"faltam {sorted(faltam, key=str)}, sobram {sorted(sobram, key=str)}, "
                         f"repetidas {sorted(dup, key=str)}")


# ── A ─────────────────────────────────────────────────────────────────────────
def _sql(t: Tabela, corte: pd.Timestamp) -> tuple[str, dict]:
    where, params = [], dict(t.params)
    if t.filtro:
        where.append(f"({t.filtro})")
    if t.corte:
        where.append(f"`{t.corte}` <= %(corte)s")
        params["corte"] = corte.date().isoformat()
    sql = f"SELECT * FROM `{t.nome}`" + (" WHERE " + " AND ".join(where) if where else "")
    return sql, params


def extrair(tabelas: list[Tabela], pasta_a: Path, corte: pd.Timestamp,
            refazer: bool = False) -> None:
    """Grava A: um .csv.gz por tabela e recorte, mais o _manifesto.json com a consulta de cada um."""
    from domain.db import registry
    from utils import explore as ex

    pasta_a.mkdir(parents=True, exist_ok=True)
    man_path = pasta_a / "_manifesto.json"
    manifesto = json.loads(man_path.read_text(encoding="utf-8")) if man_path.exists() else {}
    reg = registry.tabelas()
    for t in tabelas:
        if t.fora:
            continue
        if t.nome not in reg:
            raise ValueError(f"`{t.nome}` não está no registry de tabelas")
        schema = _SCHEMA[reg[t.nome].split(".")[2]]
        sql, params = _sql(t, corte)
        anterior = manifesto.get(t.arquivo)
        if anterior and not refazer and (t.arquivo and (pasta_a / t.arquivo).exists()):
            if anterior["sql"] != sql or anterior["params"] != params:
                raise ValueError(f"{t.arquivo} já existe neste ciclo com outra consulta "
                                 f"({anterior['sql']}); dê outro nome ao recorte")
            continue
        df = ex.q(sql, schema=schema, params=params or None)
        df.to_csv(pasta_a / t.arquivo, index=False)
        datas = df[t.corte or "date"] if (t.corte or "date") in df else pd.Series(dtype=object)
        manifesto[t.arquivo] = {
            "tabela": t.nome, "recorte": t.recorte, "schema": schema, "sql": sql,
            "params": params, "linhas": int(len(df)),
            "primeira": None if datas.empty else str(pd.Timestamp(datas.min()).date()),
            "ultima": None if datas.empty else str(pd.Timestamp(datas.max()).date()),
            "extraido_em": dt.datetime.now().isoformat(timespec="seconds"),
        }
        print(f"  A  {t.arquivo:<45} {len(df):>9} linhas")
    man_path.write_text(json.dumps(manifesto, ensure_ascii=False, indent=1), encoding="utf-8")


def ler_a(pasta_a: Path, arquivo: str) -> pd.DataFrame:
    with gzip.open(pasta_a / arquivo, "rt", encoding="utf-8") as fh:
        df = pd.read_csv(fh)
    for c in _COLS_DATA:
        if c in df:
            df[c] = pd.to_datetime(df[c], errors="coerce")
    return df


# ── contexto ──────────────────────────────────────────────────────────────────
@dataclass
class Ctx:
    corte: pd.Timestamp
    anterior: pd.Timestamp | None
    pasta_a: Path
    tabelas: list[Tabela]
    completo: bool = False
    _cache: dict = field(default_factory=dict)

    def ler(self, nome: str, recorte: str | None = None) -> pd.DataFrame:
        t = next(t for t in self.tabelas if t.nome == nome and t.recorte == recorte)
        if t.arquivo not in self._cache:
            self._cache[t.arquivo] = ler_a(self.pasta_a, t.arquivo)
        return self._cache[t.arquivo]

    def serie(self, nome: str, chave: str, recorte: str | None = None) -> pd.Series:
        t = next(t for t in self.tabelas if t.nome == nome and t.recorte == recorte)
        w = largo(self.ler(nome, recorte), t)
        return w[chave].dropna() if chave in w else pd.Series(dtype=float)


def largo(df: pd.DataFrame, t: Tabela) -> pd.DataFrame:
    if df.empty:
        return pd.DataFrame()
    k = df[list(t.dims)].astype(str).agg("|".join, axis=1)
    w = df.assign(_k=k).pivot_table(index="date", columns="_k", values=t.valor, aggfunc="last")
    return w.sort_index()


# ── números ───────────────────────────────────────────────────────────────────
def fmt(v, casas: int = 2, sinal: bool = False) -> str:
    if v is None or (isinstance(v, float) and not np.isfinite(v)):
        return "—"
    return f"{v:+.{casas}f}" if sinal else f"{v:.{casas}f}"


def fdata(d) -> str:
    return "—" if d is None or pd.isna(d) else pd.Timestamp(d).date().isoformat()


def em(s: pd.Series, d) -> float | None:
    """Último valor da série em ou antes de `d`."""
    s2 = s.loc[:d]
    return None if s2.empty else float(s2.iloc[-1])


def antes(t0, meses: int) -> pd.Timestamp:
    return pd.Timestamp(t0) - pd.DateOffset(months=meses)


def pctl(hist: pd.Series, v) -> float | None:
    hist = hist.dropna()
    if v is None or pd.isna(v) or len(hist) < 24:
        return None
    return float((hist <= v).mean() * 100)


def frequencia(s: pd.Series) -> str:
    if len(s) < 3:
        return "mensal"
    dias = float(pd.Series(s.index).diff().dt.days.median())
    return ("diária" if dias <= 4 else "semanal" if dias <= 10 else "mensal" if dias <= 45
            else "trimestral" if dias <= 120 else "anual")


def _ultimo_dia_util(mes: pd.Timestamp) -> pd.Timestamp:
    fim = (mes + pd.offsets.MonthEnd(0)).date()
    return pd.Timestamp(np.busday_offset(np.datetime64(fim), 0, roll="backward"))


def mensal(s: pd.Series, fim: pd.Timestamp | None = None) -> tuple[pd.Series, tuple | None]:
    """Fluxo diário somado em meses: (meses completos, (data, soma) do mês em curso ou None).

    O mês da última observação só conta como completo se ela cai no último dia útil dele
    (sem feriados: um feriado no último pregão descarta um mês completo, o lado seguro). Com
    `fim`, a série é estendida com zeros até ele: dia sem linha é zero (intervenções)."""
    if fim is not None and fim > s.index[-1]:
        s = pd.concat([s, pd.Series([0.0], index=[fim])])
    m = s.resample("MS").sum()
    ult = s.index[-1]
    if ult < _ultimo_dia_util(m.index[-1]):
        return m.iloc[:-1], (ult, float(m.iloc[-1]))
    return m, None


# ── leituras ──────────────────────────────────────────────────────────────────
def _nivel(se: Serie, s: pd.Series, ctx: Ctx, pct: bool) -> dict:
    t0, v = s.index[-1], float(s.iloc[-1])

    def var(ref):
        if ref is None or (pct and ref == 0):
            return None
        return (v / ref - 1) * 100 if pct else v - ref

    cd = 1 if pct else se.casas
    row = {"Série": se.rotulo, "Unidade": se.unidade, "Data": fdata(t0), "Último": fmt(v, se.casas)}
    p = "Δ%" if pct else "Δ"
    for lab, m in _JANELAS:
        row[f"{p} {lab}"] = fmt(var(em(s, antes(t0, m))), cd, True)
    if ctx.anterior is not None:
        row[f"{p} desde o ciclo ant."] = ("sem dado novo" if t0 <= ctx.anterior
                                          else fmt(var(em(s, ctx.anterior)), cd, True))
    if ctx.completo:
        dez = s.loc[antes(t0, 120):]
        row["Pctl 10a"] = fmt(pctl(dez, v), 0)
        row["Pctl hist."] = fmt(pctl(s, v), 0)
        if pct:
            m = s.resample("MS").last().dropna()
            v12 = m.pct_change(12, fill_method=None) * 100
            row["Pctl Δ12m hist."] = fmt(pctl(v12, v12.iloc[-1] if len(v12) else None), 0)
        row["Mín–máx 10a"] = f"{fmt(dez.min(), se.casas)} a {fmt(dez.max(), se.casas)}"
    return row


def _fluxo(se: Serie, s: pd.Series, ctx: Ctx, fim_tabela: pd.Timestamp) -> dict:
    diaria = se.eventos or frequencia(s) == "diária"
    parcial = None
    if diaria:
        m, parcial = mensal(s, fim_tabela if se.eventos else None)
    else:
        m = s.resample("MS").sum()          # mês sem linha é zero (comex, lucros reinvestidos)
    row = {"Série": se.rotulo, "Unidade": se.unidade}
    if m.empty:
        return row | {"Último mês": "—"}
    t0 = m.index[-1]
    s12 = m.rolling(12).sum()
    row["Último mês"] = f"{fmt(m.iloc[-1], se.casas)} ({t0:%Y-%m})"
    row["Soma 3m"] = fmt(m.iloc[-3:].sum() if len(m) >= 3 else None, se.casas)
    row["Soma 12m"] = fmt(s12.iloc[-1], se.casas)
    row["Soma 12m, um ano antes"] = fmt(em(s12, antes(t0, 12)), se.casas)
    if se.pib:
        pib12 = ctx.pib12()
        p = em(pib12, t0) if pib12 is not None else None
        row["12m % PIB"] = fmt(s12.iloc[-1] * se.escala / p * 100 if p else None, 2)
    if diaria:
        row["Mês em curso"] = (f"{fmt(parcial[1], se.casas)} (até {parcial[0]:%d/%m})"
                               if parcial else "—")
        if ctx.anterior is not None:
            row["Soma desde o ciclo ant."] = fmt(s.loc[ctx.anterior + pd.Timedelta(days=1):].sum(),
                                                se.casas)
    if ctx.completo:
        row["Pctl soma 12m hist."] = fmt(pctl(s12, s12.iloc[-1]), 0)
    return row


def _media(se: Serie, s: pd.Series, ctx: Ctx) -> dict:
    t0 = s.index[-1]
    row = {"Série": se.rotulo, "Unidade": se.unidade, "Data": fdata(t0)}
    for lab, m in _JANELAS:
        row[f"Média {lab}"] = fmt(s.loc[antes(t0, m) + pd.Timedelta(days=1):].mean(), se.casas)
    if ctx.completo:
        r = s.rolling("30D").mean()
        row["Pctl média 1m 10a"] = fmt(pctl(r.loc[antes(t0, 120):], r.iloc[-1]), 0)
    return row


def _acum(x: pd.Series) -> float | None:
    return None if x.isna().any() or x.empty else float((np.prod(1 + x / 100) - 1) * 100)


def _var_mensal(se: Serie, s: pd.Series, ctx: Ctx) -> dict:
    t0 = s.index[-1]
    row = {"Série": se.rotulo, "Mês": f"{t0:%Y-%m}", "Último mês": fmt(s.iloc[-1], 2),
           "Acum. 3m": fmt(_acum(s.iloc[-3:]), 2), "Acum. 12m": fmt(_acum(s.iloc[-12:]), 2),
           "Acum. 12m, 3 meses antes": fmt(_acum(s.iloc[-15:-3]) if len(s) >= 15 else None, 2)}
    if ctx.completo:
        a12 = s.rolling(12).apply(lambda x: (np.prod(1 + x / 100) - 1) * 100, raw=True)
        row["Pctl acum. 12m hist."] = fmt(pctl(a12, a12.iloc[-1]), 0)
    return row


_LEITURAS = {
    "pct": lambda se, s, ctx, fim: _nivel(se, s, ctx, True),
    "dif": lambda se, s, ctx, fim: _nivel(se, s, ctx, False),
    "fluxo": _fluxo,
    "media": lambda se, s, ctx, fim: _media(se, s, ctx),
    "var_mensal": lambda se, s, ctx, fim: _var_mensal(se, s, ctx),
}


# ── markdown ──────────────────────────────────────────────────────────────────
def md_tabela(linhas: list[dict]) -> list[str]:
    if not linhas:
        return []
    cab = list(dict.fromkeys(k for r in linhas for k in r))
    out = ["| " + " | ".join(cab) + " |", "|" + "---|" * len(cab)]
    out += ["| " + " | ".join(str(r.get(k, "")) for k in cab) + " |" for r in linhas]
    return out


def bloco_generico(t: Tabela, df: pd.DataFrame, ctx: Ctx) -> list[str]:
    w = largo(df, t)
    fim = w.index.max() if not w.empty else None
    por_leitura: dict[str, list[dict]] = {}
    faltam = []
    for se in t.series:
        s = w[se.chave].dropna() / se.escala if se.chave in w else pd.Series(dtype=float)
        if s.empty:
            faltam.append(se.chave)
            continue
        por_leitura.setdefault(se.leitura, []).append(_LEITURAS[se.leitura](se, s, ctx, fim))
    out: list[str] = []
    for linhas in por_leitura.values():
        out += md_tabela(linhas) + [""]
    if faltam:
        out.append(f"Sem dado no corte: {', '.join(faltam)}.")
    return out


def _cabecalho_tabela(t: Tabela, df: pd.DataFrame, ctx: Ctx) -> str:
    col = t.corte or "date"
    if df.empty or col not in df:
        return f"A: `A/{t.arquivo}` · sem linhas no corte"
    ult = df[col].max()
    dias = (ctx.corte - ult).days
    quando = ("data no futuro" if dias < 0 else "no corte" if dias == 0
              else f"{dias} dia{'s' if dias > 1 else ''} antes do corte")
    return f"Último dado {fdata(ult)} ({quando}) · A: `A/{t.arquivo}`"


# ── F(A) ──────────────────────────────────────────────────────────────────────
_COMO_LER = """\
Como ler:
- **Δ% 1m/3m/12m**: variação contra o último valor de 1, 3 e 12 meses antes da última data da série.
- **Δ**: diferença na unidade da série (p.p. quando a série é %, p.b. quando é p.b.).
- **Pctl**: posição do último valor no histórico, de 0 (o menor já visto) a 100 (o maior). "10a" = últimos 10 anos.
- **Soma 3m/12m**: soma dos últimos 3 e 12 meses completos; o mês em curso aparece à parte e não entra nas somas.
- **Acum.**: variação composta.
"""


def montar_f(agente: str, ciclo: dt.date, grupos: list[dict], tabelas: list[Tabela],
             combinadas: list[Callable], pasta_a: Path, anterior: pd.Timestamp | None,
             pib: tuple[str, str] | None = None) -> str:
    corte = pd.Timestamp(ciclo)
    ctx = Ctx(corte=corte, anterior=anterior, pasta_a=pasta_a, tabelas=tabelas)

    def pib12():
        if pib is None:
            return None
        s = ctx.serie(*pib)
        return s.rolling(12).sum() if not s.empty else None
    ctx.pib12 = pib12  # type: ignore[attr-defined]

    por_chave = {(t.nome, t.recorte): t for t in tabelas}
    linhas = [f"# F(A) — {agente} — ciclo {ciclo.isoformat()}", "",
              f"Gerado em {dt.datetime.now():%Y-%m-%d %H:%M}. Dados do banco até {ciclo.isoformat()}, "
              "fixos durante o ciclo. "
              + (f"Ciclo anterior: {anterior.date().isoformat()}." if anterior is not None
                 else "Sem ciclo anterior."), "",
              "Os dados brutos (A) estão em `A/`, um arquivo por tabela; as funções G leem de lá "
              "e o código delas fica em `G/`. Nada aqui é opinião: é a mesma conta em todo ciclo.",
              "", _COMO_LER.rstrip()]
    if anterior is not None:
        linhas.append(f"- **Desde o ciclo ant.**: contra o valor em {anterior.date().isoformat()}.")
    linhas.append("")
    for g in grupos:
        ctx.completo = g["nome"] == _GRUPO_COMPLETO
        prof = "leitura completa" if ctx.completo else "leitura enxuta"
        linhas += [f"## {g['id']}. {g['nome'].split(' (')[0]} ({prof})", ""]
        for it in g["itens"]:
            t = por_chave[(it["tabela"], it["recorte"])]
            titulo = t.nome + (f" ({t.recorte})" if t.recorte else "")
            if t.fora:
                linhas += [f"### {titulo} — fora do F", "", t.fora, ""]
                continue
            df = ctx.ler(t.nome, t.recorte)
            linhas += [f"### {titulo}", "", _cabecalho_tabela(t, df, ctx), ""]
            if t.nota:
                linhas += [f"**Atenção:** {t.nota}", ""]
            if df.empty:
                continue
            corpo = t.especial(df, ctx) if t.especial else bloco_generico(t, df, ctx)
            linhas += corpo + ([""] if corpo and corpo[-1] != "" else [])
    if combinadas:
        ctx.completo = True
        linhas += ["## Leituras combinadas", ""]
        for f in combinadas:
            linhas += f(ctx) + [""]
    return "\n".join(linhas).rstrip() + "\n"


# ── ciclo ─────────────────────────────────────────────────────────────────────
_RE_CICLO = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def ciclo_anterior(agente: str, ciclo: dt.date) -> pd.Timestamp | None:
    if not CICLOS.exists():
        return None
    datas = [p.name for p in CICLOS.iterdir()
             if p.is_dir() and _RE_CICLO.match(p.name) and p.name < ciclo.isoformat()
             and (p / "dados" / f"F_{agente}.md").exists()]
    return pd.Timestamp(max(datas)) if datas else None
