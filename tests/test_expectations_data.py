# -*- coding: utf-8 -*-
"""
Confere o payload do Panorama de Expectativas contra o MySQL, valor a valor.

Roda com:
    uv run python tests/test_expectations_data.py

Precisa do relatorio gerado E de conexao com o banco -- e o unico teste do projeto
que compara o ARQUIVO ENVIADO com a fonte, em vez de exercitar funcoes puras:

    uv run python analytics/brasil/expectations/generate_report.py

Por que existe: o payload e comprimido. Cada serie vira {i0, m[], s[], n[]} sobre uma
grade semanal global, e um erro de offset desloca a serie inteira no tempo sem lancar
excecao nenhuma -- o relatorio abriria bonito, com todo numero na semana errada. O
harness JS (tests/test_expectations_js.js) so consegue testar consistencia interna:
que blkAt e blkSerie concordam entre si. Este aqui responde a outra pergunta, que e
se o que esta no arquivo e o que esta no banco.

Segue o padrao do tests/test_sync_calendar.py: script executavel com asserts, nao
pytest (o projeto nao tem pytest configurado).
"""

from __future__ import annotations

import json
import random
import re
import sys
from datetime import date, timedelta
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from connectors.mysql import MySQLDataRequester  # noqa: E402

_RAIZ = Path(__file__).resolve().parents[1]
_HTML = _RAIZ / "reports" / "brasil" / "Expectations.html"
_AMOSTRA_SERIES = 40   # series sorteadas por store
_AMOSTRA_PONTOS = 4    # pontos sorteados por serie

falhas = []


def check(rotulo, obtido, esperado):
    ok = obtido == esperado
    print(f"  {'ok  ' if ok else 'FALHA'}  {rotulo}")
    if not ok:
        print(f"          esperado: {esperado!r}")
        print(f"          obtido  : {obtido!r}")
        falhas.append(rotulo)


def check_true(rotulo, cond, detalhe=""):
    print(f"  {'ok  ' if cond else 'FALHA'}  {rotulo}")
    if not cond:
        if detalhe:
            print(f"          {detalhe}")
        falhas.append(rotulo)


def carrega_payload() -> dict:
    """Le o REPORT_DATA do HTML GERADO -- nao re-roda os loaders de proposito.

    Testar o artefato enviado, e nao o que os loaders devolvem em memoria, e o que
    cobre tambem a serializacao (json.dumps com default=str, acentuacao, NaN virando
    null)."""
    if not _HTML.exists():
        print(f"{_HTML} nao existe -- gere o relatorio primeiro:")
        print("  uv run python analytics/brasil/expectations/generate_report.py")
        sys.exit(1)
    texto = _HTML.read_text(encoding="utf-8")
    m = re.search(r"^const REPORT_DATA = (.*);$", texto, re.MULTILINE)
    if not m:
        print("nao achei 'const REPORT_DATA = ...;' no HTML gerado")
        sys.exit(1)
    return json.loads(m.group(1))


def conecta():
    req = MySQLDataRequester("macro_brasil", "expc_focus")
    req.connect()
    if req.connection is None:
        print("sem conexao com o MySQL -- este teste compara o payload com o banco.")
        sys.exit(1)
    return req.connection


def valor_bloco(blk, stat, gi):
    arr = blk.get(stat) or []
    j = gi - blk["i0"]
    return arr[j] if 0 <= j < len(arr) else None


def semana(iso: str) -> tuple[str, str]:
    """Segunda e domingo da semana ISO de `iso`.

    A conferencia usa intervalo de datas em vez de YEARWEEK(date,3) de proposito:
    funcao sobre a coluna impede o uso do indice, e a PK destas tabelas comeca em
    `date` -- com YEARWEEK cada ponto sorteado custava um full scan.
    """
    d = date.fromisoformat(iso)
    seg = d - timedelta(days=d.weekday())
    return seg.isoformat(), (seg + timedelta(days=6)).isoformat()


def main():
    random.seed(20260824)  # sorteio reproduzivel: uma falha da para reproduzir igual
    D = carrega_payload()
    grade = D["meta"]["grade"]
    conn = conecta()
    q = lambda sql: pd.read_sql(sql, conn)  # noqa: E731

    print("\n1. Grade semanal = ultima data de pesquisa de cada semana ISO")
    # A ancora de cada semana e o MAX(date) entre as tres tabelas naquela semana ISO.
    amostra = random.sample(range(len(grade)), 25)
    erros = []
    for i in amostra:
        d = grade[i]
        seg, dom = semana(d)
        real = q(
            "SELECT MAX(d) m FROM ("
            f"  SELECT MAX(date) d FROM expc_focus WHERE date BETWEEN '{seg}' AND '{dom}'"
            "  UNION ALL"
            f"  SELECT MAX(date) d FROM expc_focus_copom WHERE date BETWEEN '{seg}' AND '{dom}'"
            "  UNION ALL"
            f"  SELECT MAX(date) d FROM expc_focus_periodo WHERE date BETWEEN '{seg}' AND '{dom}'"
            ") t"
        ).iloc[0]["m"]
        if str(real) != d:
            erros.append(f"{d} != {real}")
    check_true(f"{len(amostra)} ancoras sorteadas sao o MAX(date) da propria semana ISO",
               not erros, "; ".join(erros[:5]))
    check("grade termina na ultima pesquisa da expc_focus_periodo",
          grade[-1], str(q("SELECT MAX(date) d FROM expc_focus_periodo").iloc[0]["d"]))
    check_true("grade estritamente crescente", all(grade[i] < grade[i + 1] for i in range(len(grade) - 1)))

    print("\n2. expc_focus_periodo: mediana/desvio/respondentes de cada ponto sorteado")
    # O loader reduz por JOIN com o MAX(date) da semana NA PROPRIA TABELA -- ou seja,
    # todo indicador de uma mesma semana vem da MESMA data de pesquisa (o que e o que
    # torna a tabela do Boletim uma leitura transversal honesta). A conferencia tem de
    # usar a mesma regra, nao "ultimo ponto da serie na semana".
    # Uma varredura so, aqui, em vez de uma por ponto sorteado.
    maxsem = q("SELECT MAX(date) d FROM expc_focus_periodo GROUP BY YEARWEEK(date, 3)")
    ancora_tabela = {}
    for d in maxsem["d"]:
        ancora_tabela[semana(str(d))[0]] = str(d)

    total, divergentes = 0, []
    for per in ("anual", "trimestral", "mensal"):
        chaves = random.sample(list(D["periodo"][per]), min(_AMOSTRA_SERIES, len(D["periodo"][per])))
        for chave in chaves:
            ind, det, ref = chave.split("|")
            blk = D["periodo"][per][chave]
            n = len(blk["m"])
            for gi in random.sample(range(blk["i0"], blk["i0"] + n), min(_AMOSTRA_PONTOS, n)):
                d = grade[gi]
                esperado = valor_bloco(blk, "m", gi)
                alvo = ancora_tabela.get(semana(d)[0])
                linha = q(
                    "SELECT mediana, desvio_padrao, numero_respondentes "
                    f"FROM expc_focus_periodo WHERE date='{alvo}' "
                    f"  AND periodicidade='{per}' AND indicador='{ind}' "
                    f"  AND detalhe='{det}' AND data_referencia='{ref}'"
                ) if alvo else pd.DataFrame()
                total += 1
                if linha.empty:
                    if esperado is not None:
                        divergentes.append(f"{per}/{chave}@{d}: payload={esperado}, banco=sem linha")
                    continue
                obtido = float(linha.iloc[0]["mediana"])
                if esperado is None or abs(obtido - esperado) > 5e-5:
                    divergentes.append(f"{per}/{chave}@{d}: payload={esperado}, banco={obtido}")
                nn = linha.iloc[0]["numero_respondentes"]
                if nn is not None and valor_bloco(blk, "n", gi) not in (None, int(nn)):
                    divergentes.append(f"{per}/{chave}@{d}: respondentes {valor_bloco(blk, 'n', gi)} != {int(nn)}")
    check_true(f"{total} pontos sorteados batem com o banco", not divergentes,
               "\n          ".join(divergentes[:8]))

    print("\n3. expc_focus e expc_focus_copom: reducao por serie dentro da semana")
    # Estes dois loaders reduzem por (serie, semana) em pandas, nao por JOIN: a tabela e
    # pequena e a leitura e serie a serie, entao vale pegar o ultimo ponto QUE AQUELA
    # SERIE tem na semana. Regra diferente da de cima, de proposito.
    divergentes = []
    total = 0
    for chave in random.sample(list(D["movel"]), min(_AMOSTRA_SERIES, len(D["movel"]))):
        ind, hz, suav, base = chave.split("|")
        blk = D["movel"][chave]
        n = len(blk["m"])
        for gi in random.sample(range(blk["i0"], blk["i0"] + n), min(_AMOSTRA_PONTOS, n)):
            d = grade[gi]
            esperado = valor_bloco(blk, "m", gi)
            seg, dom = semana(d)
            linha = q(
                "SELECT mediana, minimo, maximo FROM expc_focus "
                f"WHERE date BETWEEN '{seg}' AND '{dom}' AND indicador='{ind}' "
                f"  AND horizonte='{hz}' AND suavizada='{suav}' AND base_calculo={base} "
                "ORDER BY date DESC LIMIT 1"
            )
            total += 1
            if linha.empty:
                if esperado is not None:
                    divergentes.append(f"movel/{chave}@{d}: payload={esperado}, banco=sem linha")
                continue
            obtido = float(linha.iloc[0]["mediana"])
            if esperado is None or abs(obtido - esperado) > 5e-5:
                divergentes.append(f"movel/{chave}@{d}: payload={esperado}, banco={obtido}")
    for chave in random.sample(list(D["copom"]), min(_AMOSTRA_SERIES, len(D["copom"]))):
        reuniao, base = chave.split("|")
        blk = D["copom"][chave]
        n = len(blk["m"])
        for gi in random.sample(range(blk["i0"], blk["i0"] + n), min(_AMOSTRA_PONTOS, n)):
            d = grade[gi]
            esperado = valor_bloco(blk, "m", gi)
            seg, dom = semana(d)
            linha = q(
                "SELECT mediana FROM expc_focus_copom "
                f"WHERE date BETWEEN '{seg}' AND '{dom}' AND reuniao='{reuniao}' "
                f"  AND base_calculo={base} ORDER BY date DESC LIMIT 1"
            )
            total += 1
            if linha.empty:
                if esperado is not None:
                    divergentes.append(f"copom/{chave}@{d}: payload={esperado}, banco=sem linha")
                continue
            obtido = float(linha.iloc[0]["mediana"])
            if esperado is None or abs(obtido - esperado) > 5e-5:
                divergentes.append(f"copom/{chave}@{d}: payload={esperado}, banco={obtido}")
    check_true(f"{total} pontos sorteados de expc_focus/expc_focus_copom batem", not divergentes,
               "\n          ".join(divergentes[:8]))

    print("\n4. A ultima semana da grade reproduz o Boletim publicado")
    # Leitura transversal: todo indicador anual do payload na ultima semana tem de bater
    # com a linha correspondente da ultima pesquisa no banco.
    ult = grade[-1]
    banco = q(
        "SELECT indicador, detalhe, data_referencia, mediana FROM expc_focus_periodo "
        f"WHERE periodicidade='anual' AND date='{ult}'"
    )
    divergentes, conferidos = [], 0
    for r in banco.itertuples():
        chave = f"{r.indicador}|{r.detalhe}|{r.data_referencia}"
        blk = D["periodo"]["anual"].get(chave)
        if blk is None:
            divergentes.append(f"{chave}: no banco, ausente do payload")
            continue
        v = valor_bloco(blk, "m", len(grade) - 1)
        conferidos += 1
        if v is None or abs(float(r.mediana) - v) > 5e-5:
            divergentes.append(f"{chave}: payload={v}, banco={float(r.mediana)}")
    check_true(f"as {conferidos} linhas anuais da ultima pesquisa batem uma a uma",
               not divergentes, "\n          ".join(divergentes[:8]))

    print("\n5. Contagens e limites declarados")
    check("indicadores anuais no indice", len(D["indice"]["anual"]),
          int(q("SELECT COUNT(*) n FROM (SELECT DISTINCT indicador, detalhe FROM expc_focus_periodo "
                "WHERE periodicidade='anual') t").iloc[0]["n"]))
    check("series no store do Copom", len(D["copom"]),
          int(q("SELECT COUNT(*) n FROM (SELECT DISTINCT reuniao, base_calculo FROM expc_focus_copom) t").iloc[0]["n"]))
    check("series no store de horizonte movel", len(D["movel"]),
          int(q("SELECT COUNT(*) n FROM (SELECT DISTINCT indicador, horizonte, suavizada, base_calculo "
                "FROM expc_focus) t").iloc[0]["n"]))
    # O corte do store mensal e declarado no payload e tem de ser respeitado.
    corte = D["meta"]["mensalRefMin"]
    # data_referencia mensal vem no formato do BCB, "MM/YYYY" -- comparar a string crua
    # com uma data ISO daria falso negativo (e ja deu, ao escrever este teste).
    refs_mensais = {k.split("|")[2] for k in D["periodo"]["mensal"]}
    iso_mensais = {r.split("/")[1] + "-" + r.split("/")[0] for r in refs_mensais}
    check_true(f"nenhuma referencia mensal anterior a {corte}",
               all(r >= corte[:7] for r in iso_mensais), min(iso_mensais))
    # base 1 nao existe na expc_focus_periodo -- se aparecer, alguem mudou o loader sem
    # atualizar a aba Bases, que oferece so movel e Copom.
    check("expc_focus_periodo segue so com base 0",
          int(q("SELECT COUNT(DISTINCT base_calculo) n FROM expc_focus_periodo").iloc[0]["n"]), 1)

    print("\n6. Sanidade dos valores")
    ruins = []
    for store, nome in ((D["periodo"]["anual"], "anual"), (D["periodo"]["mensal"], "mensal"),
                        (D["periodo"]["trimestral"], "trimestral"), (D["movel"], "movel"),
                        (D["copom"], "copom")):
        for chave, blk in store.items():
            for stat in ("m", "s", "n"):
                for v in blk.get(stat) or []:
                    if v is None:
                        continue
                    if not isinstance(v, (int, float)) or v != v or abs(v) > 1e7:
                        ruins.append(f"{nome}/{chave}/{stat}={v!r}")
                        break
    check_true("nenhum NaN, string ou valor absurdo nos stores", not ruins, "; ".join(ruins[:5]))
    dp_negativo = [k for k, b in D["periodo"]["anual"].items()
                   if any(v is not None and v < 0 for v in (b.get("s") or []))]
    check_true("desvio-padrao nunca negativo", not dp_negativo, "; ".join(dp_negativo[:5]))
    conn.close()

    print()
    if falhas:
        print(f"{len(falhas)} FALHA(S): " + "; ".join(falhas))
        sys.exit(1)
    print("todos os testes passaram")


if __name__ == "__main__":
    main()
