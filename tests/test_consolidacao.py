# -*- coding: utf-8 -*-
"""Testa a consolidacao de uma rodada do ciclo conjunto (analytics/agent_system/consolidacao.py).

Roda com:
    uv run python tests/test_consolidacao.py

Script com asserts, nao pytest (mesmo padrao de tests/test_modelo_agentes.py). Nao toca no banco
nem na planilha real nem na pasta real do ciclo: o tracker e uma COPIA com a aba "Exogenas"
preenchida por uma tutela FICTICIA, e os JSON dos agentes e o P vao para uma pasta temporaria.
O modelo e o retrato de 2026-10-22 (obsidian/ciclos/2026-10-22/dados/A/modelo_estrutural.json),
so lido. Cada item erra sem levantar nada se quebrar:

1. o P usa o caminho de quem nao e o principal da exogena, ou faz media de caminhos;
2. o principal escreve e o P nao usa exatamente o dele (nem segurado depois do ultimo dado);
3. um caminho diferente de subordinado ou de quem nao tem papel some calado em vez de virar
   divergencia (com o papel dele);
4. exogena cujo principal nao escreveu nao fica no padrao do simulador, ou nao e avisada;
5. o P nao e o modelo.rodar com os mesmos caminhos (central e faixa);
6. um JSON com chave, trimestre ou probabilidade errados passa;
7. a aba com zero ou mais de um Principal numa linha, ou com valor desconhecido, passa.
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
P, S = "Principal", "Subordinado"
TUTELA = {
    "fiscal": {"fiscal": P, "politica_monetaria": S},         # PM escreve diferente: diverge
    "rr_10a": {"fiscal": P, "politica_monetaria": S},         # os dois escrevem: vale so o principal
    "vol": {"cambio": P},
    "meta_12m": {"politica_monetaria": P, "fiscal": S},       # o principal nao escreve: padrao + aviso
    "dxy_em": {"externo": P},                                 # cambio escreve sem papel: diverge
    "ffr": {"externo": P},
    "infl_us": {"externo": P},
    "sp500": {"externo": P},
    "icbr_usd": {"externo": P},
    # icbr_agr_usd: o externo e o principal e nao escreve; a inflacao escreve sem papel -> padrao,
    # aviso e divergencia contra o padrao
    "icbr_agr_usd": {"externo": P},
    "icbr_met_usd": {"externo": P, "inflacao": S},           # o subordinado nao escreve: sem divergencia
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


def tese(var, tris, base=None, larg=0.1):
    """Uma tese simples: central = base[t] (ou 1.0), faixa +- larg, 50 na faixa, 30 upside, 20
    downside."""
    return {var: {"trimestres": {
        t: {"central": (base or {}).get(t, 1.0), "faixa": [(base or {}).get(t, 1.0) - larg,
                                                            (base or {}).get(t, 1.0) + larg],
            "p_faixa": 50, "p_upside": 30, "p_downside": 20} for t in tris}}}


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
u, o, dv = cs.juntar({"x": {"cambio": "principal", "fiscal": "subordinado"}},
                     {"cambio": {"x": {"4T26": 10.0}}, "fiscal": {"x": {"1T27": 20.0, "2T27": 10.0}},
                      "externo": {"x": {"4T26": 99.0}}},
                     jj, {"x": [5.0, 5.0, 5.0]})
check("juntar: o principal escreve -> vale so o dele, segurado depois do ultimo dado (sem media)",
      u["x"] == {"4T26": 10.0, "1T27": 10.0, "2T27": 10.0} and o["x"]["tipo"] == "principal"
      and o["x"]["principal"] == "cambio", u)
check("juntar: o subordinado diverge (papel 'subordinado') e quem nao tem papel diverge ('sem papel'); "
      "valor igual ao usado nao diverge", dv == [
    {"agente": "fiscal", "exogena": "x", "papel": "subordinado", "trimestre": "1T27", "valor": 20.0,
     "usado": 10.0, "diferenca": 10.0, "usado_de": "cambio (principal)"},
    {"agente": "externo", "exogena": "x", "papel": "sem papel", "trimestre": "4T26", "valor": 99.0,
     "usado": 10.0, "diferenca": 89.0, "usado_de": "cambio (principal)"}], dv)
u, o, dv = cs.juntar({"x": {"cambio": "principal", "fiscal": "subordinado"}},
                     {"fiscal": {"x": {"1T27": 7.0}}}, jj, {"x": [5.0, 6.0, 6.0]})
check("juntar: o principal nao escreveu -> padrao do simulador, e o subordinado que escreveu "
      "diverge contra o padrao (o caminho dele NAO e usado)",
      "x" not in u and o["x"]["tipo"] == "padrão" and o["x"]["principal"] == "cambio"
      and [(d["trimestre"], d["usado"], d["papel"], d["usado_de"]) for d in dv]
      == [("1T27", 6.0, "subordinado", "padrão do simulador")], (u, dv))
u, o, dv = cs.juntar({"x": {"cambio": "principal"}}, {"cambio": {"x": {"1T27": 3.0}}, "fiscal": {"x": {"1T27": 3.0}}},
                     jj, {"x": [1.0, 1.0, 1.0]})
check("juntar: o principal comeca depois -> antes dele vale o padrao; valor igual ao usado nao e divergencia",
      u["x"] == {"1T27": 3.0, "2T27": 3.0} and dv == [], (u, dv))
u, o, dv = cs.juntar({}, {"cambio": {"x": {"1T27": 7.0}}}, jj, {"x": [5.0, 6.0, 6.0]})
check("juntar: exogena fora da aba fica no padrao e quem escreveu diverge ('sem papel')",
      "x" not in u and [(d["papel"], d["usado"]) for d in dv] == [("sem papel", 6.0)], (u, dv))

with tempfile.TemporaryDirectory() as tmp:
    tmp = Path(tmp)
    raiz = tmp / "ciclos"
    tk = planilha(tmp, TUTELA)

    # 1. a tutela lida da aba, pelos nomes das colunas
    t = cs.ler_tutela(tk)
    check("ler_tutela le os papeis da copia, coluna achada pelo nome",
          t["papeis"]["rr_10a"] == {"politica_monetaria": "subordinado", "fiscal": "principal"}
          and t["papeis"]["icbr_agr_usd"] == {"externo": "principal"}, t["papeis"])
    check("a aba tem as 11 exogenas do modelo", set(t["chaves"]) == set(CTX["exogenas"]), t["chaves"])

    # 2. os caminhos de cada agente na rodada 1
    fis = {"4T26": 140.0, "1T27": 135.0, "2T27": 130.0}
    rr_f = {"4T26": 7.5, "1T27": 7.2, "2T27": 7.0}
    rr_pm = {"1T27": 7.6, "2T27": 7.4}                       # comeca um trimestre depois
    grava(raiz, "fiscal", "r1", {"fiscal": fis, "rr_10a": rr_f},
          tese("fiscal", H6, base=dict(zip(H6, cs.expandir(fis, H6))), larg=15))
    grava(raiz, "politica_monetaria", "r1", {"rr_10a": rr_pm, "fiscal": {"4T26": 160.0, "1T27": 135.0}},
          tese("selic_fim", H6, base={t: 13.0 for t in H6}, larg=1.0))
    grava(raiz, "cambio", "r1", {"vol": {"4T26": 14.0}, "dxy_em": {"2026T4": 131.0}},
          tese("ptax", H6, base={t: 5.2 for t in H6}, larg=0.15))
    grava(raiz, "externo", "r1", {"dxy_em": {"4T26": 129.0, "1T27": 128.0}, "ffr": {"4T26": 3.6},
                                  "icbr_met_usd": {"4T26": 335.0}},
          tese("dxy_em", H6[:2], base={"4T26": 129.0, "1T27": 128.0}, larg=3))
    grava(raiz, "inflacao", "r1", {"icbr_agr_usd": {"4T26": 210.0}},
          tese("ipca_12m", H6, base={t: 4.5 for t in H6}, larg=0.4))

    r = cs.consolidar(CICLO, "r1", raiz=raiz, tracker=tk, sim=SIM, faixa=True)
    us = r["caminhos_usados"]

    # 3. so o principal
    check("fiscal: usado o caminho do agente fiscal (principal), nao o da PM (subordinada)",
          us["fiscal"] == {t: v for t, v in zip(JAN, cs.expandir(fis, JAN)) if v is not None}
          and r["origem"]["fiscal"]["principal"] == "fiscal", us["fiscal"])
    check("vol: usado o do cambio, segurado depois do ultimo trimestre escrito",
          all(us["vol"][t] == 14.0 for t in JAN), us.get("vol"))
    check("icbr_met_usd: o externo e o principal e escreveu; a inflacao subordinada nao escreveu",
          r["origem"]["icbr_met_usd"]["principal"] == "externo" and us["icbr_met_usd"]["4T26"] == 335.0,
          r["origem"]["icbr_met_usd"])

    # 4. sem media
    check("rr_10a: vale so o caminho do principal (fiscal), sem media com o da PM",
          all(perto(us["rr_10a"][t], v) for t, v in
              {"4T26": 7.5, "1T27": 7.2, "2T27": 7.0, "3T27": 7.0}.items()),
          {t: us["rr_10a"][t] for t in ("4T26", "1T27", "2T27", "3T27")})
    check("e a origem diz de quem",
          r["origem"]["rr_10a"]["principal"] == "fiscal"
          and r["origem"]["rr_10a"]["por_trimestre"][0] == ["fiscal"]
          and list(r["origem"]["rr_10a"]["valores"]) == ["fiscal"], r["origem"]["rr_10a"])

    # 5. divergencias
    dv = {(d["agente"], d["exogena"], d["trimestre"]): d for d in r["divergencias"]}
    check("a PM (subordinada) escreveu outro CDS em 4T26 -> divergencia, com os dois valores",
          ("politica_monetaria", "fiscal", "4T26") in dv
          and dv[("politica_monetaria", "fiscal", "4T26")]["usado"] == 140.0
          and dv[("politica_monetaria", "fiscal", "4T26")]["diferenca"] == 20.0
          and dv[("politica_monetaria", "fiscal", "4T26")]["papel"] == "subordinado", list(dv))
    check("a PM (subordinada) escreveu outro juro real -> divergencia nos dois trimestres em que escreveu",
          ("politica_monetaria", "rr_10a", "1T27") in dv and ("politica_monetaria", "rr_10a", "2T27") in dv
          and perto(dv[("politica_monetaria", "rr_10a", "1T27")]["diferenca"], 0.4), list(dv))
    check("e o 1T27 igual ao usado nao diverge", ("politica_monetaria", "fiscal", "1T27") not in dv)
    check("o cambio escreveu dxy_em sem papel -> divergencia, nao usado",
          ("cambio", "dxy_em", "4T26") in dv and dv[("cambio", "dxy_em", "4T26")]["papel"] == "sem papel"
          and us["dxy_em"]["4T26"] == 129.0, us.get("dxy_em"))
    check("a inflacao escreveu icbr_agr_usd sem papel (o principal, o externo, nao escreveu) -> divergencia contra o padrao",
          ("inflacao", "icbr_agr_usd", "4T26") in dv
          and perto(dv[("inflacao", "icbr_agr_usd", "4T26")]["usado"], PAD["icbr_agr_usd"][0]))
    check("so essas cinco divergencias (CDS da PM, 2 do juro real da PM, dxy do cambio, icbr_agr da inflacao)",
          len(r["divergencias"]) == 5, list(dv))

    # 6. padrao e avisos
    check("meta_12m e icbr_agr_usd ficam no padrao (fora dos caminhos usados)",
          "meta_12m" not in us and "icbr_agr_usd" not in us, sorted(us))
    av = "\n".join(r["avisos"])
    check("aviso: o principal do icbr_agr_usd nao escreveu",
          "`icbr_agr_usd`: o principal (externo) não escreveu o caminho" in av, av)
    check("aviso: o principal nao escreveu (meta_12m), com o subordinado nomeado",
          "`meta_12m`: o principal (politica_monetaria) não escreveu o caminho "
          "(subordinados: fiscal); ficou no padrão do simulador" in av, av)
    check("aviso: sem o antigo texto de nivel", "nível" not in av, av)
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
    check("assimetria = (P(upside) - P(downside))/100", perto(x["assimetria"], 0.10), x["assimetria"])

    # 9. os arquivos
    md = (raiz / CICLO / "P1.md").read_text(encoding="utf-8")
    js = json.loads((raiz / CICLO / "P1.json").read_text(encoding="utf-8"))
    check("P1.md e P1.json gravados na pasta do ciclo (temporaria)",
          md.startswith("# P1 — consolidação da rodada 1") and js["p"] == "P1")
    check("o P1.md traz as quatro secoes",
          all(s in md for s in ("## Avisos", "## 1. Exógenas usadas", "## 2. Saída do modelo",
                                "## 3. Divergências", "## 4. As teses")))
    check("a linha do rr_10a diz de quem (o principal)",
          "| fiscal (principal) |" in md and "média de " not in md and "(nível" not in md, md[:2000])
    check("a tabela de divergencias tem a linha da PM no CDS, com o papel",
          "| Política monetária | `fiscal` | subordinado | 4T26 | 160,00 | 140,00 | +20,00 |" in md)
    check("e a do cambio sem papel",
          "| Câmbio | `dxy_em` | sem papel | 4T26 | 131,00 |" in md)
    check("a saida do modelo vem com a faixa e sem a lista repetida de exogenas",
          "**Endógenas** — central e faixa" in md and "**Exógenas do cenário**" not in md)
    check("e com os quatro grupos do IPCA (contribuicao para o de 12 meses) e o residuo",
          all(f"| {n} ({u}) |" in md for k, n, u, _c in modelo.SAIDAS if k.startswith("ipca_12m_")))
    lo_, hi_ = 5.2 - 0.15, 5.2 + 0.15
    check("as caudas da tese saem por posicao: downside abaixo da faixa, upside acima",
          "| Downside · P | Upside · P | P(up) − P(down) |" in md
          and f"abaixo de {cs._f(lo_, 3)} · 20% | acima de {cs._f(hi_, 3)} · 30% | +0,10 |" in md
          and "worst" not in md.lower() and "best" not in md.lower(), md[md.find("### Câmbio"):][:600])
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
                "tese": tese("ptax", ["4T26"], base={"4T26": 5.2})}
        base.update(mudar)
        return lambda: cs.validar(base, CTX, "teste")

    check("chave de exogena desconhecida levanta",
          levanta(com(caminhos={"cds": {"4T26": 1}}), "'cds'", "não é exógena") is True)
    check("endogena em caminhos levanta, dizendo que o modelo a resolve",
          levanta(com(caminhos={"ptax": {"4T26": 5}}), "'ptax'", "endógena") is True)
    check("trimestre fora da janela levanta",
          levanta(com(caminhos={"vol": {"4T30": 13}}), "fora da janela") is True)
    check("trimestre mal escrito levanta", levanta(com(caminhos={"vol": {"5T26": 13}}), "inválido") is True)
    ruim = tese("ptax", ["4T26"], base={"4T26": 5.2})
    ruim["ptax"]["trimestres"]["4T26"]["p_downside"] = 19
    check("probabilidades que nao somam 100 levantam", levanta(com(tese=ruim), "não 100") is True)
    ruim = tese("ptax", ["4T26"], base={"4T26": 5.2})
    ruim["ptax"]["trimestres"]["4T26"]["faixa"] = [5.3, 5.4]
    check("faixa que nao contem a central levanta", levanta(com(tese=ruim), "não contém a central") is True)
    ruim = tese("ptax", ["4T26"], base={"4T26": 5.2})
    ruim["ptax"]["trimestres"]["4T26"]["p_upsdie"] = 1
    check("campo desconhecido (erro de digitacao) levanta", levanta(com(tese=ruim), "p_upsdie") is True)
    # As caudas sao de posicao desde 2026-10-22: o contrato antigo (worst/best) nao passa calado.
    ruim = tese("ptax", ["4T26"], base={"4T26": 5.2})
    ruim["ptax"]["worst"] = "acima"
    check("o campo 'worst' antigo levanta como desconhecido", levanta(com(tese=ruim), "'worst'") is True)
    ruim = tese("ptax", ["4T26"], base={"4T26": 5.2})
    q = ruim["ptax"]["trimestres"]["4T26"]
    q["p_worst"], q["p_best"] = q.pop("p_upside"), q.pop("p_downside")
    check("p_worst/p_best antigos levantam, e a mensagem pede p_upside e p_downside",
          levanta(com(tese=ruim), "'p_worst'", "'p_best'", "falta 'p_upside'", "falta 'p_downside'") is True)
    check("a inflacao escreve tese sobre a contribuicao de um grupo do IPCA",
          cs.validar({"agente": "inflacao", "rodada": "r1", "ciclo": CICLO, "caminhos": {},
                      "tese": tese("ipca_12m_servicos", ["4T26"], base={"4T26": 2.0})}, CTX, "teste")
          ["tese"]["ipca_12m_servicos"]["tipo"] == "modelo")
    check("tese sobre a variavel do modelo de outro agente levanta",
          levanta(com(tese=tese("hiato", ["4T26"])), "atividade") is True)
    check("tese sobre exogena com central diferente do proprio caminho levanta",
          levanta(com(tese=tese("vol", ["4T26"], base={"4T26": 12.0})),
                  "diferente do próprio caminho") is True)
    check("varios erros saem juntos numa mensagem so",
          levanta(com(caminhos={"cds": {"4T26": 1}, "vol": {"4T30": 1}}), "'cds'", "4T30") is True)
    arq = grava(raiz, "atividade", "r2", {}, tese("hiato", ["4T26"]))
    d = json.loads(arq.read_text(encoding="utf-8"))
    d["rodada"] = "r1"
    arq.write_text(json.dumps(d), encoding="utf-8")
    check("arquivo cuja rodada nao bate com o nome levanta",
          levanta(lambda: cs.ler_caminhos(CICLO, "r2", CTX, raiz), "o nome e a pasta dizem") is True)
    arq.unlink()
    grava(raiz, "cambioo", "r2", {}, {})
    check("arquivo da rodada com agente desconhecido no nome levanta",
          levanta(lambda: cs.ler_caminhos(CICLO, "r2", CTX, raiz), "agente desconhecido") is True)

    # 12. a aba mal preenchida
    (tmp / "vazia").mkdir()
    vazia = planilha(tmp / "vazia", None)
    check("aba Exogenas sem nenhum Principal levanta, nomeando a linha e dizendo que e um por exogena",
          levanta(lambda: cs.ler_tutela(vazia), "Exógenas", "linha 3 (meta_12m)", "0 agentes Principal",
                  "exatamente um") is True)
    check("e a consolidacao tambem",
          levanta(lambda: cs.consolidar(CICLO, "r1", raiz=raiz, tracker=vazia, sim=SIM, faixa=False),
                  "0 agentes Principal") is True)
    (tmp / "dois").mkdir()
    dois = planilha(tmp / "dois", TUTELA)
    wb = openpyxl.load_workbook(dois)
    ws = wb[cs.ABA]
    ws.cell(3, 8).value = "Principal"          # meta_12m ja tem a PM como Principal (coluna I)
    wb.save(dois)
    check("dois Principais na mesma linha levantam, nomeando os dois",
          levanta(lambda: cs.ler_tutela(dois), "linha 3 (meta_12m)", "2 agentes Principal", "cambio",
                  "politica_monetaria") is True)
    wb = openpyxl.load_workbook(tk)
    ws = wb[cs.ABA]
    ws.cell(3, 8).value = 7
    wb.save(vazia)
    check("valor desconhecido (7) levanta, dizendo o que vale",
          levanta(lambda: cs.ler_tutela(vazia), "valor 7", "'Principal', 'Subordinado'") is True)
    wb = openpyxl.load_workbook(tk)
    ws = wb[cs.ABA]
    ws.cell(3, 8).value = "Nivel 2"
    wb.save(vazia)
    check("o antigo nivel (texto) tambem levanta",
          levanta(lambda: cs.ler_tutela(vazia), "valor 'Nivel 2'") is True)
    wb = openpyxl.load_workbook(tk)
    ws = wb[cs.ABA]
    ws.cell(3, 9).value = " principal "         # caixa e espacos nao importam
    ws.cell(3, 12).value = "SUBORDINADO"
    wb.save(vazia)
    check("caixa e espacos nao importam",
          cs.ler_tutela(vazia)["papeis"]["meta_12m"] == {"politica_monetaria": "principal",
                                                         "fiscal": "subordinado"})

    # 13. a pasta real do ciclo nao foi tocada
    real = cs.pasta(CICLO)
    check("nada gravado em obsidian/ciclos/2026-10-22/",
          not (real / "P1.md").exists() and not (real / "caminhos").exists())

print()
print("tudo ok" if falhas == 0 else f"{falhas} falha(s)")
sys.exit(1 if falhas else 0)
