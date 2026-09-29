# -*- coding: utf-8 -*-
"""Testa o que domain/db/brasil/bcb/cred_fluxo_financeiro.py faz quando uma edicao do RPM sai
SEM o grafico de fluxo financeiro.

Roda com:
    uv run python tests/test_cred_fluxo_financeiro.py      # offline: anexo e banco sao falsos

Script com asserts, nao pytest (mesmo padrao de tests/test_projecao_rpm.py).

Nasceu de 2026-09-29: a edicao 2026-09 saiu sem o grafico, o parse levantou dizendo que o BCB o
tinha RENOMEADO -- nao tinha, tirou do relatorio -- e a linha da pagina de calendario ficou
vermelha. As regras que isto segura:

1. parse() separa AUSENCIA (GraficoAusente) de RENOMEACAO/ERA EM R$ (RuntimeError com os titulos
   achados), e o grafico de debentures sozinho conta como ausencia;
2. na rotina, a ausencia vira aviso e a ULTIMA edicao que publica o grafico e recarregada, com o
   boxe escrito antes dela;
3. a renomeacao continua levantando, sem voltar para uma edicao antiga;
4. nenhum caminho de falha grava nada -- em particular o boxe nunca vai sozinho para o banco, que
   sobrescreveria 2018-2025 com o vintage de 2025-03;
5. o aviso do grafico no relatorio de credito (impulso_tab.aviso_fluxo) so afirma "o RPM saiu
   sem este grafico" com o registro do ETL provando isso -- nunca por deducao do banco.
"""
from __future__ import annotations

import contextlib
import datetime as dt
import io
import sys

from domain.db.brasil.bcb import cred_fluxo_financeiro as m

falhas = 0


def check(nome, cond, detalhe=""):
    global falhas
    if cond:
        print("  ok     " + nome)
    else:
        falhas += 1
        print("  FALHA  " + nome + (("  -- " + str(detalhe)) if detalhe else ""))


# --------------------------------------------------------------- anexo falso

class Aba:
    """O minimo de uma worksheet do openpyxl read-only que o script usa: title e iter_rows."""

    def __init__(self, title, linhas):
        self.title = title
        self._linhas = [tuple(r) for r in linhas]

    def iter_rows(self, min_row=1, max_row=None, max_col=None, values_only=True):
        for r in self._linhas[min_row - 1:max_row]:
            yield r[:max_col] if max_col else r


class Livro:
    def __init__(self, abas):
        self.worksheets = abas
        self.sheetnames = [a.title for a in abas]


def _meses(n, inicio=dt.date(2018, 1, 1)):
    out, d = [], inicio
    for _ in range(n):
        out.append(dt.datetime(d.year, d.month, 1))
        d = dt.date(d.year + d.month // 12, d.month % 12 + 1, 1)
    return out


def aba_grafico(titulo, colunas, valores, nome="Graf 1.2.30", subtitulo=None):
    topo = ["Capítulo 1 – Conjuntura econômica", "1.2 - Conjuntura interna", titulo]
    if subtitulo:
        topo.append(subtitulo)
    topo.append("Fonte: BC")
    linhas = [(t,) + (None,) * len(colunas) for t in topo]
    linhas.append(("Data",) + tuple(colunas))
    linhas += [(d,) + tuple(v(i) for v in valores) for i, d in enumerate(_meses(70))]
    return Aba(nome, linhas)


def recorrente(titulo="Gráfico 1.2.30 – Fluxo financeiro acumulado em 12 meses"):
    return aba_grafico(titulo, ["Pessoas jurídicas", "Pessoas físicas", "Total"],
                       [lambda i: -1.0, lambda i: -0.5 - i / 100, lambda i: -1.5 - i / 100])


def debentures():
    return aba_grafico("Gráfico 1.2.31 – Decomposição do fluxo financeiro de debêntures "
                       "acumulado em 12 meses", ["Emissões", "Total"],
                       [lambda i: 1.0, lambda i: 0.5], nome="Graf 1.2.31")


def outra():
    return aba_grafico("Gráfico 1.2.32 – Inadimplência do crédito no SFN", ["Total"],
                       [lambda i: 3.0], nome="Graf 1.2.32")


def livro_boxe():
    return Livro([
        aba_grafico("Gráfico 2 – Fluxo financeiro", ["R$ bi", "% PIB"],
                    [lambda i: -100.0, lambda i: -1.5], nome="C1 Boxe Graf 2"),
        aba_grafico("Gráfico 3 – Decomposição do fluxo financeiro", ["Livre", "Total"],
                    [lambda i: 0.0, lambda i: -1.0], nome="C1 Boxe Graf 3",
                    subtitulo="Pessoas jurídicas"),
        aba_grafico("Gráfico 4 – Decomposição do fluxo financeiro", ["Livre", "Total"],
                    [lambda i: 0.0, lambda i: -0.5], nome="C1 Boxe Graf 4",
                    subtitulo="Pessoas físicas"),
    ])


class Anexo:
    """Edicoes 2026-03 em diante mais o boxe de 2025-03; `livros[v]` e o anexo de cada uma."""

    def __init__(self, livros):
        self.livros = {m._VINTAGE_BOXE: livro_boxe(), **livros}
        self.abertas = []

    def vintage_mais_recente(self):
        return max(self.livros)

    def url_de(self, v):
        return f"falso/{v:%Y%m}" if v in self.livros else None

    def abrir(self, v):
        self.abertas.append(v)
        return self.livros[v]


def rodar(livros, **kw):
    """(exc, inserts, stdout, anexo) de m.run() contra um anexo falso e um banco falso."""
    anexo = Anexo(livros)
    inserts = []
    orig_anexo, orig_insert = m.AnexoRPM, m.insert_data_into_database
    class Fabrica:  # m.AnexoRPM() devolve o falso; m.AnexoRPM.cabecalho continua o real
        cabecalho = staticmethod(orig_anexo.cabecalho)

        def __new__(cls):
            return anexo

    m.AnexoRPM = Fabrica
    m.insert_data_into_database = lambda db, tb, df: inserts.append(df.copy())
    out, exc = io.StringIO(), None
    try:
        with contextlib.redirect_stdout(out):
            m.run(**kw)
    except Exception as e:  # noqa: BLE001 -- o teste inspeciona o tipo
        exc = e
    finally:
        m.AnexoRPM, m.insert_data_into_database = orig_anexo, orig_insert
    return exc, inserts, out.getvalue(), anexo


V03, V06, V09 = dt.date(2026, 3, 1), dt.date(2026, 6, 1), dt.date(2026, 9, 1)
normal = lambda: Livro([recorrente(), debentures(), outra()])
sem_grafico = lambda: Livro([outra()])
so_debentures = lambda: Livro([debentures(), outra()])
renomeado = lambda: Livro([recorrente("Gráfico 1.2.30 – Fluxo financeiro do crédito em 12 meses"),
                           outra()])


def parse_em(livro, v):
    try:
        return m.parse(Anexo({v: livro}), v), None
    except Exception as e:  # noqa: BLE001
        return None, e


# ------------------------------------------------------------------ 1. parse

print("1. parse() separa ausencia de renomeacao")
s, e = parse_em(normal(), V06)
check("edicao normal le as 3 series", e is None and set(s or {}) == {"fluxo_pj", "fluxo_pf", "fluxo_total"}, e)

_, e = parse_em(sem_grafico(), V09)
check("sem grafico nenhum -> GraficoAusente", isinstance(e, m.GraficoAusente), repr(e))

_, e = parse_em(so_debentures(), V09)
check("so o grafico de debentures -> GraficoAusente (nao e a serie desta tabela)",
      isinstance(e, m.GraficoAusente), repr(e))

_, e = parse_em(renomeado(), V09)
check("renomeado -> RuntimeError que NAO e GraficoAusente",
      isinstance(e, RuntimeError) and not isinstance(e, m.GraficoAusente), repr(e))
check("a mensagem diz que renomeou e mostra o titulo achado",
      e is not None and "renomeou" in str(e) and "do crédito em 12 meses" in str(e), e)

_, e = parse_em(renomeado(), dt.date(2025, 12, 1))
check("antes de 2026-03 a mensagem culpa a era em R$, nao a renomeacao",
      e is not None and "R$" in str(e) and "renomeou" not in str(e), e)

# ------------------------------------------------------------- 2. rotina

print("\n2. rotina com a edicao corrente sem o grafico")
exc, ins, out, anexo = rodar({V03: normal(), V06: normal(), V09: sem_grafico()})
check("nao levanta", exc is None, repr(exc))
check("grava duas vezes: boxe e a ultima edicao valida", len(ins) == 2, len(ins))
if len(ins) == 2:
    check("o boxe vai PRIMEIRO (a edicao corrente vence na sobreposicao)",
          set(ins[0]["vintage"]) == {m._VINTAGE_BOXE} and set(ins[1]["vintage"]) == {V06},
          [sorted(set(d["vintage"])) for d in ins])
check("o aviso nomeia a edicao pulada e a recarregada",
      "AVISO" in out and "2026-09" in out and "2026-06" in out, out)
check("volta so ate a primeira edicao com o grafico (2026-03 nem e aberta)",
      V03 not in anexo.abertas, anexo.abertas)

print("\n   duas edicoes seguidas sem o grafico")
exc, ins, out, _ = rodar({V03: normal(), V06: sem_grafico(), V09: sem_grafico()})
check("recarrega 2026-03 e nomeia as duas puladas",
      exc is None and len(ins) == 2 and set(ins[1]["vintage"]) == {V03}
      and "2026-09, 2026-06" in out, (repr(exc), out))

print("\n   edicao normal: sem aviso")
exc, ins, out, _ = rodar({V03: normal(), V06: normal(), V09: normal()})
check("le 2026-09, sem AVISO", exc is None and len(ins) == 2
      and set(ins[1]["vintage"]) == {V09} and "AVISO" not in out, (repr(exc), out))

# ------------------------------------------------ 3 e 4. falhas nao gravam

print("\n3. falhas levantam e nao gravam nada")
# (livros, kwargs de run, exigencia sobre a excecao) -- o tipo e a mensagem sao afirmados, senao
# um AttributeError qualquer passaria por "levanta".
casos = {
    "renomeado na rotina": (
        {V03: normal(), V06: normal(), V09: renomeado()}, {},
        lambda e: type(e) is RuntimeError and "renomeou" in str(e)),
    "nenhuma edicao desde 2026-03 com o grafico": (
        {V03: sem_grafico(), V06: sem_grafico()}, {},
        lambda e: type(e) is RuntimeError and "nenhuma edicao de 2026-03" in str(e)),
    "vintage explicito sem o grafico": (
        {V03: normal(), V06: normal(), V09: sem_grafico()}, {"vintage": "2026-09"},
        lambda e: isinstance(e, m.GraficoAusente)),
}
for nome, (livros, kw, esperado) in casos.items():
    exc, ins, _, anexo = rodar(livros, **kw)
    check(f"{nome}: levanta o erro certo", exc is not None and esperado(exc), repr(exc))
    check(f"{nome}: zero inserts (o boxe nao vai sozinho)", len(ins) == 0, len(ins))
    check(f"{nome}: o boxe nem e baixado", m._VINTAGE_BOXE not in anexo.abertas, anexo.abertas)

exc, _, _, anexo = rodar({V03: normal(), V06: normal(), V09: renomeado()})
check("renomeado na rotina: nao volta para 2026-06", V06 not in anexo.abertas, anexo.abertas)

# ------------------------------------------- 4. o aviso do relatorio de credito

print("\n4. impulso_tab.aviso_fluxo: so afirma com os fatos do registro do ETL")
from analytics.brasil.credit.impulso_tab import aviso_fluxo  # noqa: E402

RPM = {"ok": True, "max": "2026-09-01", "mudou_em": "2026-09-29T10:16:55",
       "desde": "2026-09-24T11:50:39"}
FLX = {"ok": True, "ok_em": "2026-09-29T10:31:08", "max": "2026-06-01"}
REF = "2026-04-01"

t = aviso_fluxo(FLX, RPM, REF)
check("edicao nova lida + fluxo rodou sem erro depois -> aviso",
      t == "Série interrompida em abr/2026: o último RPM a publicar este gráfico foi o de "
           "jun/2026, e a edição de set/2026 saiu sem ele.", t)
check("fluxo em dia com a edicao -> sem aviso",
      aviso_fluxo({**FLX, "max": "2026-09-01"}, RPM, "2026-07-01") is None)
check("ultima tentativa do fluxo FALHOU (renomeacao) -> sem aviso: o grafico pode existir",
      aviso_fluxo({**FLX, "ok": False}, RPM, REF) is None)
check("fluxo rodou ANTES da edicao nova entrar -> sem aviso: ainda nao olhou",
      aviso_fluxo({**FLX, "ok_em": "2026-09-29T10:00:00"}, RPM, REF) is None)
check("sem mudou_em, o limite e o `desde` da tabela irma",
      aviso_fluxo(FLX, {**RPM, "mudou_em": None}, REF) is not None
      and aviso_fluxo({**FLX, "ok_em": "2026-09-20T00:00:00"}, {**RPM, "mudou_em": None}, REF) is None)
check("sem registro de uma das duas (outra maquina) -> sem aviso",
      aviso_fluxo(None, RPM, REF) is None and aviso_fluxo(FLX, None, REF) is None)
t2 = aviso_fluxo({**FLX, "ok_em": "2026-12-21T09:00:00"},
                 {**RPM, "max": "2026-12-01", "mudou_em": "2026-12-20T09:00:00"}, REF)
check("duas edicoes sem o grafico -> nomeia o intervalo",
      t2 is not None and "as edições de set/2026 a dez/2026 saíram sem ele" in t2, t2)

print(f"\n{'OK' if not falhas else f'{falhas} FALHA(S)'}")
sys.exit(1 if falhas else 0)
