# -*- coding: utf-8 -*-
"""Testa os `procedures` do manifesto: o veredito de atraso e o recalculo do Regerar.

Roda com:
    uv run python tests/test_dashboard_procedimentos.py

Nasceu de um bug concreto (2026-08-31): o relatorio de politica monetaria foi regerado
no dia, mas a previsao dentro dele tinha sido calculada seis dias antes -- e o sistema
dizia "em dia". A causa e que um artefato CALCULADO tem duas datas, e so uma era
observavel: quando ele foi escrito (mtime) e com que dado (o corte de informacao).

O desenho final e de DOIS botoes, por pedido explicito do usuario no mesmo dia:
"Atualizar" mexe na base de dados e "Regerar" reconstroi o dashboard -- e reconstruir
inclui refazer as metricas que ficaram atras. O que este teste cobra:

  1. `_para_gran()` -- a granularidade, que da a cada passo a FREQUENCIA dele. Sem ela a
     estimacao trimestral do modelo seria refeita a cada boletim Focus diario.
  2. `json_date` -- o corte lido de dentro do artefato, nao o mtime.
  3. `estado_procedimentos()` -- corte x fonte, na granularidade declarada.
  4. `recalcular_atrasados()` / `gerar()` -- roda so o que esta atras, na ordem, em
     CASCATA, e um passo que falha nao impede o relatorio de sair.
  5. `validar()` -- o que envelhece em silencio numa declaracao errada.
  6. O manifesto real.

Duas afirmacoes negativas que valem por si: um procedimento atrasado NAO e veredito
"desatualizado" do dashboard (senao `regerar_afetados()` regeraria num laco que nunca
conserta), e um passo SEM veredito de corte nao roda no escuro.
"""

import json
import sys
import tempfile
import time
import types
from pathlib import Path

from domain.dashboards import status as S

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

falhas = []


def check(rotulo, cond, extra=""):
    print(("  ok     " if cond else "  FALHA  ") + rotulo
          + (f"  -> {extra}" if extra and not cond else ""))
    if not cond:
        falhas.append(rotulo)


# ---------------------------------------------------------------------------
print("1. declaracao: procedimento -> artefatos, e a inversao que a aba usa")
# ---------------------------------------------------------------------------

D_SINT = {
    "key": "fake", "name": "Fake", "output": "reports/fake.html",
    "procedures": [
        {"id": "p1", "label": "Um", "module": "json", "call": "dumps",
         "writes": ["a/x.csv", "a/y.csv"]},
        {"id": "p2", "label": "Dois", "module": "json", "call": "loads",
         "writes": ["a/z.json"], "cut_from": "a/z.json", "granularidade": "dia",
         "reads": ["macro_brasil.t1", "macro_brasil.t2"]},
    ],
    "deps": [
        {"kind": "artifact", "ref": "a/x.csv"},
        {"kind": "artifact", "ref": "a/y.csv"},
        {"kind": "artifact", "ref": "a/z.json", "json_date": "corte_usado"},
        {"kind": "mysql", "ref": "macro_brasil.t1"},
        {"kind": "mysql", "ref": "macro_brasil.t2"},
    ],
}

check("procedimentos() devolve na ordem declarada",
      [p["id"] for p in S.procedimentos(D_SINT)] == ["p1", "p2"])
check("dashboard sem `procedures` devolve lista vazia",
      S.procedimentos({"key": "x"}) == [])

inv = S.proc_por_dep(D_SINT)
# O ponto da inversao: 2 artefatos de p1 apontam para o MESMO procedimento, que e o que
# evita a mesma rodada aparecer duas vezes na aba.
check("writes invertido: cada artefato aponta para quem o grava",
      inv == {"a/x.csv": "p1", "a/y.csv": "p1", "a/z.json": "p2"}, inv)
check("por_procedimento() indexa por id",
      sorted(S.por_procedimento(D_SINT)) == ["p1", "p2"])
check("comando_procedimento monta o equivalente em texto",
      S.comando_procedimento(D_SINT["procedures"][1])
      == 'uv run python -c "from json import loads; loads()"',
      S.comando_procedimento(D_SINT["procedures"][1]))


# ---------------------------------------------------------------------------
print("")
print("2. granularidade: o que da a cada passo a frequencia dele")
# ---------------------------------------------------------------------------
# Sem isto, um painel trimestral comparado contra a Focus diaria ficaria "atrasado" todo
# dia, e o Regerar refaria 4 minutos de estimacao a cada boletim, mudando os 22
# parametros do modelo por nada.

g = S._para_gran
check("data em dia continua data", g("2026-08-28", "dia") == "2026-08-28")
check("data reduzida a trimestre", g("2026-08-28", "trimestre") == "2026Q3")
check("rotulo de trimestre em trimestre e ele mesmo", g("2026Q3", "trimestre") == "2026Q3")
check("data reduzida a mes", g("2026-08-28", "mes") == "2026-08")
check("YYYY-MM (CSV do IPCA) tambem reduz a trimestre",
      g("2026-07", "trimestre") == "2026Q3")
# Um trimestre NAO da uma data: pedir granularidade fina de um dado grosso e a unica
# forma de gerar comparacao falsa, entao devolve None e o veredito fica indefinido.
check("trimestre nao vira dia (nao se inventa precisao)", g("2026Q3", "dia") is None)
check("indice que nao e data devolve None (artefato indexado por reuniao)",
      g("280", "trimestre") is None and g("f3", "trimestre") is None)
check("None entra e None sai", g(None, "dia") is None)
check("virada de trimestre: outubro e Q4", g("2026-10-01", "trimestre") == "2026Q4")


# ---------------------------------------------------------------------------
print("")
print("3. json_date: o corte vem de DENTRO do arquivo, nao do mtime")
# ---------------------------------------------------------------------------

with tempfile.TemporaryDirectory() as tmp:
    raiz = Path(tmp)
    orig = S._RAIZ
    S._RAIZ = raiz
    try:
        (raiz / "a").mkdir()
        alvo = raiz / "a" / "z.json"
        alvo.write_text(json.dumps({"corte_usado": "2026-08-25", "previsto": 3.19}),
                        encoding="utf-8")

        e = S.estado_arquivo({"kind": "artifact", "ref": "a/z.json",
                              "json_date": "corte_usado"})
        check("json_date le a chave declarada como `ultimo`",
              e["ultimo"] == "2026-08-25", e)
        check("mtime continua sendo reportado ao lado", bool(e["mtime"]))
        # Sem json_date o mesmo arquivo nao tem data interna nenhuma -- e era exatamente
        # esse o estado anterior: so mtime, que `salvar()` move e regerar o HTML nao, mas
        # que nada dizia sobre o DADO usado.
        e2 = S.estado_arquivo({"kind": "artifact", "ref": "a/z.json"})
        check("sem json_date o JSON nao tem `ultimo`", e2["ultimo"] is None, e2)

        alvo.write_text(json.dumps({"outra": 1}), encoding="utf-8")
        e3 = S.estado_arquivo({"kind": "artifact", "ref": "a/z.json",
                               "json_date": "corte_usado"})
        check("chave ausente vira erro explicito, nao None silencioso",
              e3["ultimo"] is None and "corte_usado" in (e3["erro"] or ""), e3)
    finally:
        S._RAIZ = orig


# ---------------------------------------------------------------------------
print("")
print("4. estado_procedimentos: corte contra fonte, na granularidade declarada")
# ---------------------------------------------------------------------------


def est(corte, t1, t2, existe=True, mtime="2026-08-25T17:33:48"):
    return {
        "a/x.csv": {"ultimo": "2026Q3", "mtime": mtime, "existe": True},
        "a/y.csv": {"ultimo": "2024Q2", "mtime": mtime, "existe": True},
        "a/z.json": {"ultimo": corte, "mtime": mtime, "existe": existe},
        "macro_brasil.t1": {"ultimo": t1}, "macro_brasil.t2": {"ultimo": t2},
    }


p1, p2 = S.estado_procedimentos(D_SINT, est("2026-08-25", "2026-08-28", "2026-08-24"))

check("procedimento sem cut_from fica SEM veredito, nao 'em dia'",
      p1["atrasado"] is None, p1["atrasado"])
check("procedimento sem cut_from ainda reporta quando rodou",
      p1["rodou_em"] == "2026-08-25T17:33:48")
check("atrasado quando o corte e anterior a fonte mais nova", p2["atrasado"] is True)
check("a fonte apontada e a MAIS NOVA das declaradas",
      p2["fonte_max"] == "2026-08-28" and p2["fonte_ref"] == "macro_brasil.t1",
      p2["fonte_ref"])
check("dias de atraso contados do corte a fonte", p2["dias_atras"] == 3, p2["dias_atras"])
check("a granularidade sai na linha", p2["granularidade"] == "dia")

_, ok = S.estado_procedimentos(D_SINT, est("2026-08-28", "2026-08-28", "2026-08-24"))
check("corte igual a fonte nao e atraso", ok["atrasado"] is False)
check("dias = 0 quando alcancou", ok["dias_atras"] == 0)

_, adiante = S.estado_procedimentos(D_SINT, est("2026-08-31", "2026-08-28", "2026-08-24"))
check("corte a frente da fonte nao e atraso", adiante["atrasado"] is False)

_, sem_fonte = S.estado_procedimentos(D_SINT, est("2026-08-25", None, None))
check("fonte toda indisponivel nao inventa veredito",
      sem_fonte["atrasado"] is None, sem_fonte["atrasado"])

_, sem_corte = S.estado_procedimentos(D_SINT, est(None, "2026-08-28", "2026-08-24"))
check("artefato sem corte legivel nao inventa veredito",
      sem_corte["atrasado"] is None, sem_corte["atrasado"])

_, falta = S.estado_procedimentos(D_SINT,
                                  est("2026-08-25", "2026-08-28", None, existe=False))
check("artefato inexistente aparece em `faltando`",
      falta["faltando"] == ["a/z.json"], falta["faltando"])

# O caso que a granularidade existe para resolver: MESMO corte, MESMA fonte, vereditos
# opostos porque a unidade de comparacao e outra. Em dia, a Focus de 28/08 poe o passo
# atrasado; em trimestre, 2026Q3 == 2026Q3 e nao ha nada a refazer.
D_TRI = dict(D_SINT, procedures=[
    dict(D_SINT["procedures"][1], granularidade="trimestre",
         cut_from="a/x.csv", writes=["a/x.csv"])])
(tri,) = S.estado_procedimentos(D_TRI, est("2026-08-25", "2026-08-28", "2026-08-24"))
check("o MESMO par corte/fonte, em trimestre, fica em dia",
      tri["atrasado"] is False and tri["corte"] == "2026Q3"
      and tri["fonte_max"] == "2026Q3",
      f"{tri['corte']} vs {tri['fonte_max']} -> {tri['atrasado']}")
(tri4,) = S.estado_procedimentos(D_TRI, est("2026-08-25", "2026-10-05", "2026-08-24"))
check("e vira atraso quando o trimestre NOVO abre",
      tri4["atrasado"] is True and tri4["fonte_max"] == "2026Q4",
      f"{tri4['corte']} vs {tri4['fonte_max']} -> {tri4['atrasado']}")
check("em trimestre nao se conta dias de atraso", tri4["dias_atras"] is None)


# ---------------------------------------------------------------------------
print("")
print("5. recalcular_atrasados / gerar: um botao, e a cascata")
# ---------------------------------------------------------------------------
# O Regerar refaz o que esta atras, na ordem declarada, reavaliando a cada passo. Um
# modulo falso registra o que foi chamado; nenhum MySQL entra (as fontes sao artefatos,
# que e justamente o que faz a cascata existir).

CHAMADAS = []

with tempfile.TemporaryDirectory() as tmp:
    raiz = Path(tmp)
    orig_raiz, orig_stamps = S._RAIZ, S._STAMPS
    S._RAIZ, S._STAMPS = raiz, raiz / "reports" / ".build"
    try:
        (raiz / "a").mkdir()
        (raiz / "reports").mkdir()

        def tri(q):
            return "i,v" + chr(10) + q + ",1" + chr(10)

        (raiz / "a" / "fonte.csv").write_text(tri("2026Q4"), encoding="utf-8")
        (raiz / "a" / "painel.csv").write_text(tri("2026Q3"), encoding="utf-8")
        (raiz / "a" / "estados.csv").write_text(tri("2026Q3"), encoding="utf-8")
        (raiz / "reports" / "fake.html").write_text("<html></html>", encoding="utf-8")

        fake = types.ModuleType("_fakeproc")

        def _ultimo(nome):
            linhas = [x for x in (raiz / "a" / nome).read_text(
                encoding="utf-8").splitlines() if x.strip()]
            return linhas[-1].split(",")[0]

        # Os dois PROPAGAM o trimestre da propria fonte, como o pipeline real: o painel
        # absorve o trimestre novo do banco, e e isso que poe o modelo atras.
        def _painel():
            CHAMADAS.append("painel")
            (raiz / "a" / "painel.csv").write_text(tri(_ultimo("fonte.csv")),
                                                   encoding="utf-8")

        def _modelo():
            CHAMADAS.append("modelo")
            (raiz / "a" / "estados.csv").write_text(tri(_ultimo("painel.csv")),
                                                    encoding="utf-8")

        def _quebra():
            CHAMADAS.append("quebra")
            raise RuntimeError("IPEADATA fora do ar")

        def _run(output=None, **kw):
            CHAMADAS.append("run:" + str(output))
            (raiz / "reports" / "fake.html").write_text("<html>novo</html>",
                                                        encoding="utf-8")

        fake.painel = _painel
        fake.modelo = _modelo
        fake.quebra = _quebra
        fake.run = _run
        sys.modules["_fakeproc"] = fake

        DOC = {"dashboards": [{
            "key": "fake", "name": "Fake", "output": "reports/fake.html",
            "module": "_fakeproc", "build_seconds": 1,
            "procedures": [
                {"id": "painel", "label": "Painel", "module": "_fakeproc",
                 "call": "painel", "seconds": 5, "granularidade": "trimestre",
                 "writes": ["a/painel.csv"], "cut_from": "a/painel.csv",
                 "reads": ["a/fonte.csv"]},
                {"id": "modelo", "label": "Modelo", "module": "_fakeproc",
                 "call": "modelo", "seconds": 9, "granularidade": "trimestre",
                 "writes": ["a/estados.csv"], "cut_from": "a/estados.csv",
                 "reads": ["a/painel.csv"]},
            ],
            "deps": [
                {"kind": "artifact", "ref": "a/fonte.csv"},
                {"kind": "artifact", "ref": "a/painel.csv"},
                {"kind": "artifact", "ref": "a/estados.csv"},
            ]}]}

        # Antes de rodar: painel atrasado (2026Q3 < 2026Q4), modelo em dia (Q3 == Q3).
        linhas = S.estado_procedimentos(
            DOC["dashboards"][0],
            S._estados_deps(DOC["dashboards"][0]["deps"], live=False))
        check("painel comeca atrasado e modelo em dia",
              linhas[0]["atrasado"] is True and linhas[1]["atrasado"] is False,
              [x["atrasado"] for x in linhas])

        CHAMADAS.clear()
        feito = S.recalcular_atrasados("fake", DOC)
        # A CASCATA: o modelo estava em dia na foto inicial e ficou atras porque o painel
        # rodou. Sem reavaliar a cada passo, o modelo nao rodaria nesta rodada.
        check("a cascata roda os dois, na ordem declarada",
              CHAMADAS == ["painel", "modelo"], CHAMADAS)
        check("e reporta os dois como rodados",
              [x["acao"] for x in feito] == ["rodado", "rodado"],
              [x["acao"] for x in feito])
        check("cada passo devolve quanto levou",
              all("segundos" in x for x in feito), feito)

        # Segunda rodada: nada mais atras, nada roda.
        CHAMADAS.clear()
        feito2 = S.recalcular_atrasados("fake", DOC)
        check("na segunda rodada nada esta atras e nada roda", CHAMADAS == [], CHAMADAS)
        check("e os dois passos aparecem como 'em dia'",
              [x["acao"] for x in feito2] == ["em dia", "em dia"],
              [x["acao"] for x in feito2])

        # gerar(): recalcula, gera e stampa num passo so.
        (raiz / "a" / "fonte.csv").write_text(tri("2027Q1"), encoding="utf-8")
        CHAMADAS.clear()
        r = S.gerar("fake", DOC)
        check("gerar() recalcula ANTES de gerar",
              CHAMADAS == ["painel", "modelo", "run:reports/fake.html"], CHAMADAS)
        check("gerar() conta o que recalculou", r["n_recalculados"] == 2, r)
        check("e separa o tempo de geracao do tempo total",
              r["segundos_total"] >= r["segundos"], (r["segundos_total"], r["segundos"]))
        check("gerar() gravou o stamp", S.ler_stamp("fake") is not None)

        # recalcular=False: gera sem tocar em artefato. E o que o `--gerar todos` usa.
        (raiz / "a" / "fonte.csv").write_text(tri("2027Q2"), encoding="utf-8")
        CHAMADAS.clear()
        r2 = S.gerar("fake", DOC, recalcular=False)
        check("recalcular=False gera sem refazer nada",
              CHAMADAS == ["run:reports/fake.html"], CHAMADAS)
        check("e reporta zero recalculos", r2["n_recalculados"] == 0)

        # Um passo que FALHA nao pode impedir o relatorio de sair: a estimacao depende do
        # IPEADATA e do anexo do RPM, e rede fora do ar nao e motivo para ficar sem nada.
        DOC_Q = json.loads(json.dumps(DOC))
        DOC_Q["dashboards"][0]["procedures"][0]["call"] = "quebra"
        (raiz / "a" / "fonte.csv").write_text(tri("2027Q3"), encoding="utf-8")
        # `estados` volta atras por conta propria, para o segundo passo estar atrasado
        # INDEPENDENTE do primeiro -- e o que a assercao abaixo mede.
        (raiz / "a" / "estados.csv").write_text(tri("2026Q1"), encoding="utf-8")
        CHAMADAS.clear()
        r3 = S.gerar("fake", DOC_Q)
        check("passo que falha nao interrompe a geracao",
              "run:reports/fake.html" in CHAMADAS and r3["ok"], CHAMADAS)
        check("a falha e reportada, com a mensagem original",
              r3["n_falhou"] == 1 and "IPEADATA" in r3["procedimentos"][0]["erro"],
              r3["procedimentos"][0])
        check("e o passo seguinte ainda tenta rodar", "modelo" in CHAMADAS, CHAMADAS)

        # Um passo SEM veredito de corte nao roda no escuro.
        DOC_S = json.loads(json.dumps(DOC))
        del DOC_S["dashboards"][0]["procedures"][0]["cut_from"]
        (raiz / "a" / "fonte.csv").write_text(tri("2027Q4"), encoding="utf-8")
        CHAMADAS.clear()
        r4 = S.gerar("fake", DOC_S)
        check("passo sem cut_from nao roda automaticamente",
              "painel" not in CHAMADAS, CHAMADAS)
        check("e aparece como 'sem veredito', nao como 'em dia'",
              r4["procedimentos"][0]["acao"] == "sem veredito",
              r4["procedimentos"][0]["acao"])
    finally:
        S._RAIZ, S._STAMPS = orig_raiz, orig_stamps
        sys.modules.pop("_fakeproc", None)


# ---------------------------------------------------------------------------
print("")
print("6. a separacao: procedimento atrasado NAO e dashboard desatualizado")
# ---------------------------------------------------------------------------
# Se `atrasado` entrasse no veredito, `regerar_afetados()` regeraria o relatorio num laco
# que nunca conserta -- o gerador le o artefato, nao o recalcula por conta propria. O
# recalculo entra por `gerar()`, uma vez, e nao por um veredito que nunca se apaga.

with tempfile.TemporaryDirectory() as tmp:
    raiz = Path(tmp)
    orig_raiz, orig_stamps = S._RAIZ, S._STAMPS
    S._RAIZ, S._STAMPS = raiz, raiz / "reports" / ".build"
    try:
        (raiz / "a").mkdir()
        (raiz / "reports").mkdir()
        (raiz / "a" / "z.json").write_text(
            json.dumps({"corte_usado": "2026-08-25"}), encoding="utf-8")
        (raiz / "a" / "x.csv").write_text("i,v" + chr(10) + "2026Q3,1" + chr(10),
                                          encoding="utf-8")
        (raiz / "a" / "y.csv").write_text("i,v" + chr(10) + "2024Q2,1" + chr(10),
                                          encoding="utf-8")
        time.sleep(0.05)
        (raiz / "reports" / "fake.html").write_text("<html></html>", encoding="utf-8")

        somente_art = [d for d in D_SINT["deps"] if d["kind"] == "artifact"]
        doc = {"dashboards": [dict(D_SINT, deps=somente_art)]}
        S.stamp("fake", doc)
        linha = S.estado(doc)[0]
        check("dashboard fica 'em dia' com o stamp gravado",
              linha["veredito"] == "em dia", linha["veredito"])
        check("a linha carrega `procedimentos` e `n_proc_atrasados`",
              "procedimentos" in linha and "n_proc_atrasados" in linha)
        check("veredito continua no vocabulario antigo",
              linha["veredito"] in ("em dia", "desatualizado", "sem stamp",
                                    "sem relatorio"), linha["veredito"])
        check("cada dep artifact sabe quem a grava",
              all(d.get("procedimento") for d in linha["deps"]),
              [(d["ref"], d.get("procedimento")) for d in linha["deps"]])
        z = [d for d in linha["deps"] if d["ref"] == "a/z.json"][0]
        check("o corte virou o `ultimo` do artefato", z["ultimo"] == "2026-08-25", z)
    finally:
        S._RAIZ, S._STAMPS = orig_raiz, orig_stamps


# ---------------------------------------------------------------------------
print("")
print("7. validar(): o que envelhece em silencio")
# ---------------------------------------------------------------------------
# Cada caso abaixo e um erro que NAO da excecao nem gap visivel: o passo simplesmente
# nunca entra no recalculo, ou entra e explode no clique.


def problemas(procs, deps=None):
    d = dict(D_SINT, procedures=procs,
             deps=deps if deps is not None else D_SINT["deps"])
    return S.validar({"dashboards": [d]})


def pega(procs, trecho, deps=None):
    return any(trecho in x for x in problemas(procs, deps))


base = {"id": "p", "module": "json", "call": "dumps", "writes": ["a/z.json"],
        "cut_from": "a/z.json", "granularidade": "dia",
        "reads": ["macro_brasil.t1"]}

check("writes que nao e dep declarada e pego",
      pega([dict(base, writes=["a/inexistente.csv"], cut_from="a/inexistente.csv")],
           "nao e dep artifact"))
check("reads que nao e dep declarada e pego",
      pega([dict(base, reads=["macro_brasil.t9"])], "nao e dep declarada"))
# `reads` aceita artefato: e o que liga `modelo` ao painel que `painel` grava, e o que
# faz a cascata existir sem uma aresta declarada entre os dois passos.
check("reads aceita ARTEFATO, nao so tabela",
      not pega([dict(base, reads=["a/x.csv"])], "nao e dep declarada"))
check("procedimento sem writes e pego (nao apareceria na aba)",
      pega([{"id": "p", "module": "json", "call": "dumps"}], "sem `writes`"))
# O pior dos silencios: sem cut_from o passo nunca entra no recalculo do Regerar, fica
# em "sem veredito" para sempre e nada avisa. E a forma exata do bug de 2026-08-31.
check("procedimento sem cut_from e pego",
      pega([{"id": "p", "module": "json", "call": "dumps",
             "writes": ["a/z.json"]}], "sem `cut_from`"))
check("cut_from fora do writes e pego",
      pega([dict(base, cut_from="a/y.csv")], "nao esta em writes"))
check("cut_from JSON sem json_date no dep e pego",
      pega([dict(base, writes=["a/w.json"], cut_from="a/w.json")],
           "sem `json_date`",
           D_SINT["deps"] + [{"kind": "artifact", "ref": "a/w.json"}]))
check("cut_from sem reads e pego",
      pega([{"id": "p", "module": "json", "call": "dumps",
             "writes": ["a/z.json"], "cut_from": "a/z.json"}], "sem `reads`"))
check("granularidade invalida e pega",
      pega([dict(base, granularidade="semana")], "granularidade invalida"))
check("call inexistente e pego", pega([dict(base, call="naoexiste")], "nao e chamavel"))
check("modulo inexistente e pego",
      pega([dict(base, module="modulo.que.nao.existe")], "modulo nao encontrado"))
check("id duplicado e pego", pega([base, dict(base)], "duplicado"))

# "fake:p: ..." e problema do procedimento; "fake: ..." e do dashboard (arquivo ou tabela
# sintetica que nao existe). O prefixo com o id separa os dois.
so_proc = [x for x in problemas([base]) if x.startswith("fake:p:")]
check("declaracao correta nao gera problema de procedimento", so_proc == [], so_proc)


# ---------------------------------------------------------------------------
print("")
print("8. rodar_procedimento: guardas")
# ---------------------------------------------------------------------------

doc_f = {"dashboards": [D_SINT]}
try:
    S.rodar_procedimento("fake", "naoexiste", doc_f)
    check("procedimento desconhecido levanta", False, "nao levantou")
except ValueError as exc:
    check("procedimento desconhecido levanta ValueError", "naoexiste" in str(exc))

r = S.rodar_procedimento("fake", "p1", doc_f, obj={"a": 1})
check("procedimento declarado e chamado de verdade", r["ok"] and r["proc"] == "p1", r)
check("devolve quanto levou e o rotulo", r["label"] == "Um" and r["segundos"] >= 0, r)


# ---------------------------------------------------------------------------
print("")
print("9. manifesto real")
# ---------------------------------------------------------------------------

doc = S.carregar()
por = S.por_chave(doc)
mp = por["brasil_monetary_policy"]
procs = S.procedimentos(mp)

# TODO dashboard com procedimento passa pelas mesmas exigencias -- a lista cresce sem que
# este teste precise ser reescrito. Em 2026-09-01 sao dois: politica monetaria (3 passos,
# calculo) e inflacao (1 passo, um FETCH -- o unico insumo dela que nao vem do MySQL).
com_proc = [d for d in S.dashboards(doc) if S.procedimentos(d)]
print("         " + str(len(com_proc)) + " dashboard(s) com procedimento: "
      + ", ".join(d["key"] + "(" + str(len(S.procedimentos(d))) + ")" for d in com_proc))
check("mais de um dashboard declara procedimento (o piloto deixou de ser piloto)",
      len(com_proc) >= 2, [d["key"] for d in com_proc])
for d in com_proc:
    refs_f = {x["ref"] for x in d["deps"] if x["kind"] in ("artifact", "csv")}
    for p in S.procedimentos(d):
        pid = d["key"] + ":" + p["id"]
        check("  " + pid + ": writes sao deps de arquivo declaradas",
              set(p["writes"]) <= refs_f, sorted(set(p["writes"]) - refs_f))
        check("  " + pid + ": cut_from esta em writes",
              p.get("cut_from") in (p.get("writes") or []), p.get("cut_from"))
        # O corte tem de sair como DATA na granularidade declarada. Um CSV longo sem
        # `date_col` devolve o primeiro campo da ultima linha -- que pode ser o nome de
        # uma serie, e ai o veredito fica None para sempre, sem erro nenhum.
        dep_cf = next((x for x in d["deps"] if x["ref"] == p.get("cut_from")), None)
        bruto = S.estado_arquivo(dep_cf).get("ultimo") if dep_cf else None
        gran = p.get("granularidade") or "dia"
        check("  " + pid + ": o corte lido do arquivo e data em " + gran,
              bruto is not None and S._para_gran(bruto, gran) is not None,
              "leu " + repr(bruto))

check("politica monetaria declara os 3 procedimentos, na ordem de execucao",
      [p["id"] for p in procs] == ["painel", "modelo", "previsao"],
      [p["id"] for p in procs])

refs_art = {d["ref"] for d in mp["deps"] if d["kind"] == "artifact"}
todos_writes = [r for p in procs for r in p["writes"]]
check("todo `writes` e dep artifact declarada",
      set(todos_writes) <= refs_art, sorted(set(todos_writes) - refs_art))
# O sigma de r* e escrito pelo painel e LIDO pela estimacao: fora do `writes` ele
# desaparece da aba, e a unica pista de que falta e a estimacao estourando.
check("o painel declara o sigma de r* entre o que grava",
      any(r.endswith("modelo_sigma_rr.txt") for r in todos_writes), todos_writes)
check("nenhum artefato e gravado por dois procedimentos",
      len(todos_writes) == len(set(todos_writes)),
      [r for r in set(todos_writes) if todos_writes.count(r) > 1])
# Todo passo tem de ter corte, senao nunca entra no Regerar.
check("os 3 passos declaram cut_from e reads",
      all(p.get("cut_from") and p.get("reads") for p in procs),
      [(p["id"], bool(p.get("cut_from")), len(p.get("reads") or [])) for p in procs])
check("painel e modelo sao trimestrais, previsao e diaria",
      [p.get("granularidade") for p in procs] == ["trimestre", "trimestre", "dia"],
      [p.get("granularidade") for p in procs])
# A cascata do real: `modelo` le o painel que `painel` grava.
modelo = next(p for p in procs if p["id"] == "modelo")
painel = next(p for p in procs if p["id"] == "painel")
check("o modelo le o artefato que o painel grava (a cascata declarada)",
      set(modelo["reads"]) <= set(painel["writes"]), modelo["reads"])

prev = next(p for p in procs if p["id"] == "previsao")
dep_cut = [d for d in mp["deps"] if d["ref"] == prev["cut_from"]][0]
check("o dep do cut_from da previsao tem json_date: corte_usado",
      dep_cut.get("json_date") == "corte_usado", dep_cut)

# A lista de fontes do manifesto tem de bater com a que o proprio modulo consulta -- a
# duplicacao e consciente (o relatorio se autodiagnostica sem manifesto nem servidor), e
# este assert e o que impede as duas de divergirem em silencio.
try:
    from analytics.brasil.monetary_policy.antecipa_copom import _FONTES_FRESCOR
    do_manifesto = {r.split(".", 1)[1] for r in prev["reads"]}
    check("reads do manifesto == fontes de antecipa_copom.frescor",
          do_manifesto == set(_FONTES_FRESCOR),
          do_manifesto.symmetric_difference(set(_FONTES_FRESCOR)))
except ImportError as exc:
    print(f"  PULADO  import de antecipa_copom: {exc}")

check("validar() nao reclama do manifesto real", S.validar(doc) == [], S.validar(doc))

# ---------------------------------------------------------------------------
print("")
print("10. o corte que nao e data, e o stdout que derruba o botao")
# ---------------------------------------------------------------------------

# (a) Um CSV longo (coluna de rotulo na frente) como cut_from sem `date_col`: o corte sai
#     como nome de serie, `atrasado` fica None e NADA avisa. Foi o que quase entrou no
#     passo do fetch do IPCA -- por sorte a primeira coluna daquele arquivo e a data.
tmp = Path(tempfile.mkdtemp())
longo = tmp / "longo.csv"
longo.write_text("name,dt,value\nIPCA,2026-07,0.1\nIPCA_servicos,2026-07,0.3\n",
                 encoding="utf-8")
dep_longo = {"kind": "csv", "ref": str(longo), "role": "x"}
bruto_l = S.estado_arquivo(dep_longo)["ultimo"]
check("sem date_col, o corte de um CSV longo sai como rotulo, nao como data",
      bruto_l == "IPCA_servicos" and S._para_gran(bruto_l, "mes") is None, bruto_l)
dep_longo["date_col"] = "dt"
check("com date_col, sai o MAX da coluna de data",
      S.estado_arquivo(dep_longo)["ultimo"] == "2026-07",
      S.estado_arquivo(dep_longo))

# ... e `validar()` tem de DIZER isso, em vez de deixar o passo em silencio para sempre.
D_LONGO = {
    "key": "fakelongo", "name": "F", "area": "brasil", "output": str(tmp / "o.html"),
    "module": None, "command": "x", "build_seconds": 1,
    "deps": [{"kind": "csv", "ref": str(longo), "role": "x"},
             {"kind": "mysql", "ref": "macro_brasil.inflc_decomposicao", "role": "y"}],
    "procedures": [{"id": "p", "label": "P", "module": "json", "call": "dumps",
                    "seconds": 1, "writes": [str(longo)], "cut_from": str(longo),
                    "granularidade": "mes",
                    "reads": ["macro_brasil.inflc_decomposicao"]}],
}
probs_l = [x for x in S.validar({"dashboards": [D_LONGO]})
           if x.startswith("fakelongo:p:")]
check("validar() reclama do corte que nao e data",
      any("nao e data em mes" in x for x in probs_l), probs_l)
D_LONGO["deps"][0]["date_col"] = "dt"
probs_l2 = [x for x in S.validar({"dashboards": [D_LONGO]})
            if x.startswith("fakelongo:p:")]
check("com date_col declarado, o reclamo desaparece", probs_l2 == [], probs_l2)

# (b) O stdout do servidor. O console do Windows abre em cp1252, e um print com seta
#     dentro do gerador levanta UnicodeEncodeError -- o clique volta erro e o dashboard
#     NAO e regerado, por causa da mensagem de progresso e nao do dado. Medido em
#     2026-09-01 com o relatorio de inflacao, cujo resumo imprime "->" em U+2192.
try:
    from analytics.release_calendar import serve as SV

    class _Fluxo:
        def __init__(self):
            self.args = None

        def reconfigure(self, **kw):
            self.args = kw

    reais = (sys.stdout, sys.stderr)
    f1, f2 = _Fluxo(), _Fluxo()
    sys.stdout, sys.stderr = f1, f2
    try:
        SV.stdout_utf8()
    finally:
        sys.stdout, sys.stderr = reais
    check("serve.stdout_utf8() poe os dois fluxos em utf-8",
          f1.args == {"encoding": "utf-8", "errors": "replace"} and f1.args == f2.args,
          (f1.args, f2.args))

    class _Sem:
        pass

    sys.stdout, sys.stderr = _Sem(), _Sem()
    try:
        SV.stdout_utf8()
        ok_sem = True
    except Exception as exc:                                      # noqa: BLE001
        ok_sem = type(exc).__name__ + ": " + str(exc)
    finally:
        sys.stdout, sys.stderr = reais
    check("e um fluxo sem reconfigure nao derruba o servidor", ok_sem is True, ok_sem)
    # Os TRES entry points que rodam gerador ou ETL, nao so o servidor: o
    # `jobs/update_db.py` regera dashboards desde 2026-08-28, e o `--gerar` do status.py
    # tambem -- os dois morriam no mesmo print.
    for _arq in ("analytics/release_calendar/serve.py", "jobs/update_db.py",
                 "domain/dashboards/status.py"):
        _fonte = Path(_arq).read_text(encoding="utf-8")
        _depois_main = _fonte.split("def main(")[1][:600]
        check("  " + _arq + ": main() poe o console em utf-8 antes de rodar",
              "stdout_utf8()" in _depois_main, _depois_main[:60])
except ImportError as exc:
    print("  PULADO  import de serve: " + str(exc))


try:
    linha = S.estado(doc, chaves=["brasil_monetary_policy"])[0]
    check("estado() do real traz os 3 procedimentos",
          linha["n_proc"] == 3, linha["n_proc"])
    for pr in linha["procedimentos"]:
        check(f"  {pr['id']}: veredito de corte definido",
              pr["atrasado"] in (True, False), pr["atrasado"])
        print(f"         {pr['id']:9s} [{pr['granularidade']}] corte {pr['corte']} | "
              f"fonte {pr['fonte_max']} | atrasado={pr['atrasado']}")
    # O que o Regerar custaria agora, que e o numero que a aba anuncia antes do clique.
    extra = sum(pr["seconds"] or 0 for pr in linha["procedimentos"] if pr["atrasado"])
    print(f"         Regerar agora: ~{(mp.get('build_seconds') or 0) + extra}s "
          f"({mp.get('build_seconds')}s de geracao + {extra}s de recalculo)")
except Exception as exc:
    print(f"  PULADO  metade com MySQL indisponivel: {type(exc).__name__}: {exc}")


print("")
print("=" * 62)
if falhas:
    print(f"{len(falhas)} FALHA(S):")
    for f in falhas:
        print(f"  - {f}")
    raise SystemExit(1)
print("todos os asserts passaram")
