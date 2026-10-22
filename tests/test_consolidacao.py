# -*- coding: utf-8 -*-
"""Testa a consolidacao de uma rodada do ciclo conjunto (analytics/agent_system/consolidacao.py).

Roda com:
    uv run python tests/test_consolidacao.py

Script com asserts, nao pytest (mesmo padrao de tests/test_modelo_agentes.py). Nao toca no banco
nem na planilha real nem na pasta real do ciclo: o tracker e uma COPIA com a aba "Exogenas"
preenchida por uma tutela FICTICIA, e os JSON dos agentes e o P vao para uma pasta temporaria.
O modelo e o retrato de 2026-10-22 (obsidian/ciclos/2026-10-22/dados/A/modelo_estrutural.json),
so lido. Cada item erra sem levantar nada se quebrar:

1. o P usa o caminho de quem nao tem a tutela, ou de um nivel pior;
2. dois agentes no mesmo nivel nao viram media trimestre a trimestre, ou a media conta quem
   ainda nao tem valor naquele trimestre;
3. um caminho diferente de quem nao tem tutela some calado em vez de virar divergencia;
4. exogena sem caminho de quem tem tutela nao fica no padrao do simulador, ou nao e avisada;
5. o P nao e o modelo.rodar com os mesmos caminhos (central e faixa);
6. um JSON com chave, trimestre ou probabilidade errados passa;
7. a aba sem nenhum nivel passa, e a consolidacao inventa dono.
"""
from __future__ import annotations

import json
import shutil
import sys
import tempfile
from pathlib import Path

import openpyxl

from analytics.agent_system import consolidacao as cs
from analytics.agent_system import modelo

sys.stdout.reconfigure(encoding="utf-8")
falhas = 0
CICLO = "2026-10-22"


def check(nome, cond, extra=""):
    global falhas
    print(("ok    " if cond else "FALHA ") + nome + (f"  [{extra}]" if not cond and extra != "" else ""))
    falhas += 0 if cond else 1


def levanta(fn, *trechos, tipo=Exception):
    try:
        fn()
    except tipo as exc:
        return all(t in str(exc) for t in trechos) or str(exc)
    return False


def perto(a, b, tol=1e-9):
    if a is None or b is None:
        return a is None and b is None
    return abs(a - b) <= tol * max(1.0, abs(b))


# ── a tutela ficticia ─────────────────────────────────────────────────────────
TUTELA = {
    "fiscal": {"fiscal": 1, "politica_monetaria": 3},        # PM escreve diferente: diverge
    "rr_10a": {"fiscal": 1, "politica_monetaria": 1},        # os dois escrevem: media
    "vol": {"cambio": 1},
    "meta_12m": {"politica_monetaria": 1},                   # PM nao escreve: padrao + aviso
    "dxy_em": {"externo": 1},                                # cambio escreve sem tutela: diverge
    "ffr": {"externo": 1},
    "infl_us": {"externo": 1},
    "sp500": {"externo": 1},
    "icbr_usd": {"externo": 1},
    # icbr_agr_usd: ninguem; a inflacao escreve assim mesmo -> padrao, aviso e divergencia
    "icbr_met_usd": {"inflacao": 1, "externo": 2},           # a inflacao nao escreve: vale o 2
}


def planilha(destino: Path, tutela: dict | None) -> Path:
    """Copia do tracker com as colunas dos agentes da aba "Exogenas" apagadas e, se `tutela`,
    preenchidas com ela."""
    p = destino / "data_tracker.xlsx"
    shutil.copy(cs.TRACKER, p)
    wb = openpyxl.load_workbook(p)
    ws = wb[cs.ABA]
    cab_r = next(r for r in range(1, ws.max_row + 1) if cs._norm(ws.cell(r, 1).value) == "chave")
    cab = {cs._norm(ws.cell(cab_r, c).value): c for c in range(1, ws.max_column + 1)}
    cols = {a: cab[cs._norm(n)] for a, n in cs.AGENTES.items()}
    for r in range(cab_r + 1, ws.max_row + 1):
        k = ws.cell(r, 1).value
        for a, c in cols.items():
            ws.cell(r, c).value = (tutela or {}).get(k, {}).get(a)
    wb.save(p)
    return p


def tese(var, worst, tris, base=None, larg=0.1):
    """Uma tese simples: central = base[t] (ou 1.0), faixa +- larg, 50/30/20."""
    return {var: {"worst": worst, "trimestres": {
        t: {"central": (base or {}).get(t, 1.0), "faixa": [(base or {}).get(t, 1.0) - larg,
                                                            (base or {}).get(t, 1.0) + larg],
            "p_faixa": 50, "p_worst": 30, "p_best": 20} for t in tris}}}


def grava(raiz: Path, agente: str, rodada: str, caminhos: dict, ts: dict, **extra):
    arq = cs.arquivo_caminhos(CICLO, agente, rodada, raiz)
    arq.parent.mkdir(parents=True, exist_ok=True)
    d = {"agente": agente, "rodada": rodada, "ciclo": CICLO, "caminhos": caminhos, "tese": ts}
    d.update(extra)
    arq.write_text(json.dumps(d, ensure_ascii=False), encoding="utf-8")
    return arq


SIM = modelo.carregar(CICLO)
CTX = cs.contexto(SIM)
JAN = CTX["janela"]
H6 = JAN[:6]
PAD = CTX["padrao"]

# 0. juntar sozinho, com dados sinteticos (rapido, sem o modelo)
jj = ["4T26", "1T27", "2T27"]
u, o, dv = cs.juntar({"x": {"cambio": 1, "fiscal": 1, "externo": 2}},
                     {"cambio": {"x": {"4T26": 10.0}}, "fiscal": {"x": {"1T27": 20.0}},
                      "externo": {"x": {"4T26": 99.0}}},
                     jj, {"x": [5.0, 5.0, 5.0]})
check("juntar: no mesmo nivel, media so de quem tem valor no trimestre (10; (10+20)/2; segurado)",
      u["x"] == {"4T26": 10.0, "1T27": 15.0, "2T27": 15.0}, u)
check("juntar: o nivel 2 nao entra e diverge do usado", dv == [{
    "agente": "externo", "exogena": "x", "nivel": 2, "trimestre": "4T26", "valor": 99.0,
    "usado": 10.0, "diferenca": 89.0, "usado_de": "cambio, fiscal (nível 1, média)"}], dv)
u, o, dv = cs.juntar({"x": {}}, {"cambio": {"x": {"1T27": 7.0}}}, jj, {"x": [5.0, 6.0, 6.0]})
check("juntar: sem tutela, fica no padrao e quem escreveu diverge contra o padrao",
      "x" not in u and o["x"]["tipo"] == "padrão"
      and [(d["trimestre"], d["usado"]) for d in dv] == [("1T27", 6.0)], (u, dv))
u, o, dv = cs.juntar({"x": {"cambio": 2}}, {"cambio": {"x": {"4T26": 5.0}}, "fiscal": {"x": {"4T26": 5.0}}},
                     jj, {"x": [1.0, 1.0, 1.0]})
check("juntar: valor igual ao usado nao e divergencia", dv == [] and u["x"]["4T26"] == 5.0, dv)

with tempfile.TemporaryDirectory() as tmp:
    tmp = Path(tmp)
    raiz = tmp / "ciclos"
    tk = planilha(tmp, TUTELA)

    # 1. a tutela lida da aba, pelos nomes das colunas
    t = cs.ler_tutela(tk)
    check("ler_tutela le os niveis da copia, coluna achada pelo nome",
          t["niveis"]["rr_10a"] == {"politica_monetaria": 1, "fiscal": 1}
          and t["niveis"]["icbr_agr_usd"] == {}, t["niveis"])
    check("a aba tem as 11 exogenas do modelo", set(t["chaves"]) == set(CTX["exogenas"]), t["chaves"])

    # 2. os caminhos de cada agente na rodada 1
    fis = {"4T26": 140.0, "1T27": 135.0, "2T27": 130.0}
    rr_f = {"4T26": 7.5, "1T27": 7.2, "2T27": 7.0}
    rr_pm = {"1T27": 7.6, "2T27": 7.4}                       # comeca um trimestre depois
    grava(raiz, "fiscal", "r1", {"fiscal": fis, "rr_10a": rr_f},
          tese("fiscal", "acima", H6, base=dict(zip(H6, cs.expandir(fis, H6))), larg=15))
    grava(raiz, "politica_monetaria", "r1", {"rr_10a": rr_pm, "fiscal": {"4T26": 160.0, "1T27": 135.0}},
          tese("selic_fim", "acima", H6, base={t: 13.0 for t in H6}, larg=1.0))
    grava(raiz, "cambio", "r1", {"vol": {"4T26": 14.0}, "dxy_em": {"2026T4": 131.0}},
          tese("ptax", "acima", H6, base={t: 5.2 for t in H6}, larg=0.15))
    grava(raiz, "externo", "r1", {"dxy_em": {"4T26": 129.0, "1T27": 128.0}, "ffr": {"4T26": 3.6},
                                  "icbr_met_usd": {"4T26": 335.0}},
          tese("dxy_em", "acima", H6[:2], base={"4T26": 129.0, "1T27": 128.0}, larg=3))
    grava(raiz, "inflacao", "r1", {"icbr_agr_usd": {"4T26": 210.0}},
          tese("ipca_12m", "acima", H6, base={t: 4.5 for t in H6}, larg=0.4))

    r = cs.consolidar(CICLO, "r1", raiz=raiz, tracker=tk, sim=SIM, faixa=True)
    us = r["caminhos_usados"]

    # 3. tutela e nivel
    check("fiscal: usado o caminho do agente fiscal (nivel 1), nao o da PM (nivel 3)",
          us["fiscal"] == {t: v for t, v in zip(JAN, cs.expandir(fis, JAN)) if v is not None}
          and r["origem"]["fiscal"]["agentes"] == ["fiscal"], us["fiscal"])
    check("vol: usado o do cambio, segurado depois do ultimo trimestre escrito",
          all(us["vol"][t] == 14.0 for t in JAN), us.get("vol"))
    check("icbr_met_usd: a inflacao (nivel 1) nao escreveu, vale o externo (nivel 2)",
          r["origem"]["icbr_met_usd"]["nivel"] == 2 and us["icbr_met_usd"]["4T26"] == 335.0,
          r["origem"]["icbr_met_usd"])

    # 4. media no mesmo nivel
    esp = {"4T26": 7.5, "1T27": (7.2 + 7.6) / 2, "2T27": (7.0 + 7.4) / 2, "3T27": (7.0 + 7.4) / 2}
    check("rr_10a: dois agentes no nivel 1 -> media trimestre a trimestre, so de quem tem valor",
          all(perto(us["rr_10a"][t], v) for t, v in esp.items()), {t: us["rr_10a"][t] for t in esp})
    check("e a origem diz media de quem",
          r["origem"]["rr_10a"]["agentes"] == ["politica_monetaria", "fiscal"]
          and r["origem"]["rr_10a"]["por_trimestre"][0] == ["fiscal"], r["origem"]["rr_10a"])

    # 5. divergencias
    dv = {(d["agente"], d["exogena"], d["trimestre"]): d for d in r["divergencias"]}
    check("a PM (nivel 3) escreveu outro CDS em 4T26 -> divergencia, com os dois valores",
          ("politica_monetaria", "fiscal", "4T26") in dv
          and dv[("politica_monetaria", "fiscal", "4T26")]["usado"] == 140.0
          and dv[("politica_monetaria", "fiscal", "4T26")]["diferenca"] == 20.0
          and dv[("politica_monetaria", "fiscal", "4T26")]["nivel"] == 3, list(dv))
    check("e o 1T27 igual ao usado nao diverge", ("politica_monetaria", "fiscal", "1T27") not in dv)
    check("o cambio escreveu dxy_em sem tutela -> divergencia, nao usado",
          ("cambio", "dxy_em", "4T26") in dv and dv[("cambio", "dxy_em", "4T26")]["nivel"] is None
          and us["dxy_em"]["4T26"] == 129.0, us.get("dxy_em"))
    check("a inflacao escreveu icbr_agr_usd sem tutela de ninguem -> divergencia contra o padrao",
          ("inflacao", "icbr_agr_usd", "4T26") in dv
          and perto(dv[("inflacao", "icbr_agr_usd", "4T26")]["usado"], PAD["icbr_agr_usd"][0]))
    check("so essas tres divergencias (o externo no icbr_met_usd e o usado)", len(r["divergencias"]) == 3, list(dv))

    # 6. padrao e avisos
    check("meta_12m e icbr_agr_usd ficam no padrao (fora dos caminhos usados)",
          "meta_12m" not in us and "icbr_agr_usd" not in us, sorted(us))
    av = "\n".join(r["avisos"])
    check("aviso: exogena sem tutela", "`icbr_agr_usd`: sem tutela" in av, av)
    check("aviso: tutela que nao escreveu (meta_12m)",
          "`meta_12m`: nenhum agente com tutela escreveu" in av, av)
    check("aviso: o nivel 1 nao escreveu e valeu o 2 (icbr_met_usd)",
          "`icbr_met_usd`: inflacao (nível 1) não escreveu" in av, av)
    check("aviso: o padrao antes do primeiro valor de quem tem a tutela? (nenhum aqui: todos comecam em 4T26)",
          "no padrão do simulador; o caminho de quem tem a tutela começa depois" not in av, av)
    check("aviso: agentes sem JSON", "atividade_r1.json" in av and "expectativas_r1.json" in av,
          r["agentes_faltando"])

    # 7. o P e o modelo.rodar com os mesmos caminhos
    direto = modelo.rodar(SIM, caminhos=us, mult={}, faixa=True)
    iguais = all(
        all(perto(a, b) for a, b in zip(r["modelo"]["endogenas"][k][c], direto["endogenas"][k][c]))
        for k in direto["endogenas"] for c in ("central", "lo", "hi"))
    check("o P reproduz modelo.rodar com os caminhos juntados (central e faixa)", iguais)
    check("e o P mexeu de fato no modelo (nao e o cenario padrao)",
          r["modelo"]["endogenas"]["ptax"]["central"][0]
          != modelo.rodar(SIM, faixa=False)["endogenas"]["ptax"]["central"][0])
    check("sem multiplicadores", r["modelo"]["mult"] == [])

    # 8. as teses ao lado do P
    tp = {(x["agente"], x["variavel"], x["trimestre"]): x for x in r["teses"]}
    x = tp[("cambio", "ptax", "4T26")]
    check("a tese do cambio leva a central do P ao lado",
          perto(x["central_p"], r["modelo"]["endogenas"]["ptax"]["central"][0])
          and perto(x["diferenca"], x["central_p"] - 5.2), x)
    x = tp[("externo", "dxy_em", "1T27")]
    check("a tese de quem nao tem variavel no modelo (externo) le o caminho usado",
          x["central_p"] == us["dxy_em"]["1T27"] and x["lo_p"] is None, x)
    check("assimetria = (Pbest - Pworst)/100", perto(x["assimetria"], -0.10), x["assimetria"])

    # 9. os arquivos
    md = (raiz / CICLO / "P1.md").read_text(encoding="utf-8")
    js = json.loads((raiz / CICLO / "P1.json").read_text(encoding="utf-8"))
    check("P1.md e P1.json gravados na pasta do ciclo (temporaria)",
          md.startswith("# P1 — consolidação da rodada 1") and js["p"] == "P1")
    check("o P1.md traz as quatro secoes",
          all(s in md for s in ("## Avisos", "## 1. Exógenas usadas", "## 2. Saída do modelo",
                                "## 3. Divergências", "## 4. As teses")))
    check("a linha do rr_10a diz a media e de quem",
          "média de politica_monetaria e fiscal (nível 1)" in md, md[:2000])
    check("a tabela de divergencias tem a linha da PM no CDS",
          "| Política monetária | `fiscal` | 3 | 4T26 | 160,00 | 140,00 | +20,00 |" in md)
    check("a saida do modelo vem com a faixa e sem a lista repetida de exogenas",
          "**Endógenas** — central e faixa" in md and "**Exógenas do cenário**" not in md)
    check("o JSON do P le de volta com os caminhos usados", js["caminhos_usados"]["fiscal"]["4T26"] == 140.0)

    # 10. o PF*: os mesmos arquivos como report final
    for a in ("fiscal", "politica_monetaria", "cambio", "externo", "inflacao"):
        d = json.loads(cs.arquivo_caminhos(CICLO, a, "r1", raiz).read_text(encoding="utf-8"))
        d["rodada"] = "rf"
        cs.arquivo_caminhos(CICLO, a, "rf", raiz).write_text(json.dumps(d), encoding="utf-8")
    rf = cs.consolidar(CICLO, "rf", raiz=raiz, tracker=tk, sim=SIM, faixa=False)
    md = (raiz / CICLO / "PF.md").read_text(encoding="utf-8")
    check("PF.md: cabecalho do PF* e a distribuicao de cada agente ao lado da central conjunta",
          md.startswith("# PF* — consolidação do report final")
          and "A central conjunta e a distribuição de cada agente" in md
          and "| Trimestre | Central do agente | Central do PF* |" in md, md[:300])
    check("e marca quando a central conjunta cai fora da faixa do agente",
          "**fora da faixa**" in md
          and any(x["fora_da_faixa"] for x in rf["teses"]) and not all(x["fora_da_faixa"] for x in rf["teses"]))

    # 11. o contrato rejeita o que esta errado
    def com(**mudar):
        base = {"agente": "cambio", "rodada": "r1", "ciclo": CICLO, "caminhos": {"vol": {"4T26": 13.0}},
                "tese": tese("ptax", "acima", ["4T26"], base={"4T26": 5.2})}
        base.update(mudar)
        return lambda: cs.validar(base, CTX, "teste")

    check("chave de exogena desconhecida levanta",
          levanta(com(caminhos={"cds": {"4T26": 1}}), "'cds'", "não é exógena") is True)
    check("endogena em caminhos levanta, dizendo que o modelo a resolve",
          levanta(com(caminhos={"ptax": {"4T26": 5}}), "'ptax'", "endógena") is True)
    check("trimestre fora da janela levanta",
          levanta(com(caminhos={"vol": {"4T30": 13}}), "fora da janela") is True)
    check("trimestre mal escrito levanta", levanta(com(caminhos={"vol": {"5T26": 13}}), "inválido") is True)
    ruim = tese("ptax", "acima", ["4T26"], base={"4T26": 5.2})
    ruim["ptax"]["trimestres"]["4T26"]["p_best"] = 19
    check("probabilidades que nao somam 100 levantam", levanta(com(tese=ruim), "não 100") is True)
    ruim = tese("ptax", "acima", ["4T26"], base={"4T26": 5.2})
    ruim["ptax"]["trimestres"]["4T26"]["faixa"] = [5.3, 5.4]
    check("faixa que nao contem a central levanta", levanta(com(tese=ruim), "não contém a central") is True)
    ruim = tese("ptax", "acima", ["4T26"], base={"4T26": 5.2})
    ruim["ptax"]["trimestres"]["4T26"]["p_worts"] = 1
    check("campo desconhecido (erro de digitacao) levanta", levanta(com(tese=ruim), "p_worts") is True)
    check("worst fora de acima/abaixo levanta",
          levanta(com(tese={"ptax": {**tese("ptax", "x", ["4T26"], {"4T26": 5.2})["ptax"]}}), "worst") is True)
    check("tese sobre a variavel do modelo de outro agente levanta",
          levanta(com(tese=tese("hiato", "abaixo", ["4T26"])), "atividade") is True)
    check("tese sobre exogena com central diferente do proprio caminho levanta",
          levanta(com(tese=tese("vol", "acima", ["4T26"], base={"4T26": 12.0})),
                  "diferente do próprio caminho") is True)
    check("varios erros saem juntos numa mensagem so",
          levanta(com(caminhos={"cds": {"4T26": 1}, "vol": {"4T30": 1}}), "'cds'", "4T30") is True)
    arq = grava(raiz, "atividade", "r2", {}, tese("hiato", "abaixo", ["4T26"]))
    d = json.loads(arq.read_text(encoding="utf-8"))
    d["rodada"] = "r1"
    arq.write_text(json.dumps(d), encoding="utf-8")
    check("arquivo cuja rodada nao bate com o nome levanta",
          levanta(lambda: cs.ler_caminhos(CICLO, "r2", CTX, raiz), "o nome e a pasta dizem") is True)
    arq.unlink()
    grava(raiz, "cambioo", "r2", {}, {})
    check("arquivo da rodada com agente desconhecido no nome levanta",
          levanta(lambda: cs.ler_caminhos(CICLO, "r2", CTX, raiz), "agente desconhecido") is True)

    # 12. a aba vazia
    (tmp / "vazia").mkdir()
    vazia = planilha(tmp / "vazia", None)
    check("aba Exogenas sem nenhum nivel levanta, dizendo que o usuario preenche",
          levanta(lambda: cs.ler_tutela(vazia), "Exógenas", "Quem preenche é o", "usuário") is True)
    check("e a consolidacao tambem",
          levanta(lambda: cs.consolidar(CICLO, "r1", raiz=raiz, tracker=vazia, sim=SIM, faixa=False),
                  "sem nenhum nível") is True)
    wb = openpyxl.load_workbook(vazia)
    ws = wb[cs.ABA]
    ws.cell(3, 8).value = 7
    wb.save(vazia)
    check("nivel fora de 1 a 5 levanta", levanta(lambda: cs.ler_tutela(vazia), "nível 7") is True)

    # 13. a pasta real do ciclo nao foi tocada
    real = cs.pasta(CICLO)
    check("nada gravado em obsidian/ciclos/2026-10-22/",
          not (real / "P1.md").exists() and not (real / "caminhos").exists())

print()
print("tudo ok" if falhas == 0 else f"{falhas} falha(s)")
sys.exit(1 if falhas else 0)
