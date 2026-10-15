# -*- coding: utf-8 -*-
"""Testa a funcao fixa que o G do agente chama para rodar o simulador (analytics/agent_system/modelo.py).

Roda com:
    uv run python tests/test_modelo_agentes.py

Script com asserts, nao pytest (mesmo padrao de tests/test_dados_agentes.py). Nao toca no banco:
le o payload do simulador do relatorio entregue, `reports/brasil/Structural Model.html`.
Cada item erra sem levantar nada se quebrar:

1. sem caminho e sem multiplicador, a central nao e o cenario que a pagina abre;
2. o caminho de uma exogena entra no trimestre errado, ou nao e segurado depois do ultimo dado;
3. o multiplicador nao chega a conta (x1 tem de ser identidade, x0 tem de desligar o canal);
4. uma chave invalida (endogena, sigma, multiplicador negativo, trimestre fora) passa calada;
5. o trimestre que ja fechou nao e marcado.

A faixa foi conferida uma vez contra `_simFaixasSistema` da pagina, no mesmo payload: 3e-9 no
pior quantil (2026-10-15). Aqui so se afirma que x1 nao a muda.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

from analytics.agent_system import modelo

sys.stdout.reconfigure(encoding="utf-8")
falhas = 0

HTML = Path(__file__).resolve().parents[1] / "reports" / "brasil" / "Structural Model.html"
cru = HTML.read_text(encoding="utf-8")
D, _ = json.JSONDecoder().raw_decode(cru, cru.index("REPORT_DATA = ") + len("REPORT_DATA = "))
SIM = {"ciclo": "2026-10-15", "p": D["sim"]}
p = SIM["p"]


def check(nome, cond, extra=""):
    global falhas
    print(("ok    " if cond else "FALHA ") + nome + (f"  [{extra}]" if not cond and extra != "" else ""))
    falhas += 0 if cond else 1


def levanta(fn, trecho, tipo=Exception):
    try:
        fn()
    except tipo as exc:
        return trecho in str(exc)
    return False


def dif(a, b):
    return max(abs(x - y) for x, y in zip(a, b))


# 1. o cenario padrao
r0 = modelo.rodar(SIM, faixa=False)
gab = p["sistema_padrao"]["caminho"]
for k, var in (("ptax", "de"), ("selic", "selic"), ("focus_12m", "pi_e"), ("hiato", "hiato")):
    check(f"sem cenario, {k} e o cenario padrao da pagina",
          dif(r0["endogenas"][k]["central"], gab[var]) < 1e-8)
check("e o IPCA do trimestre tambem, convertido de 100*dlog",
      dif([100 * __import__("math").log1p(x / 100) for x in r0["endogenas"]["ipca_tri"]["central"]],
          gab["infl_br"]) < 1e-8)
jan = r0["trimestres"]
check("a janela tem os 12 trimestres do simulador", len(jan) == p["h_padrao"], len(jan))

# 1b. a partida e o ultimo trimestre com dado (decisao do usuario em 2026-10-15)
u = len(p["rot"]) - 1
check("a projecao comeca no trimestre seguinte ao ultimo com dado", p["i0"] == u + 1, p["i0"])
check("e a coluna 'observado' e o dado publicado daquele trimestre, nao uma projecao",
      r0["partida"]["ptax"] == p["eq"]["F"]["ptax"][u]
      and r0["partida"]["selic"] == p["var"]["selic"]["obs"][u], r0["partida"])
sem = [k for k in modelo._exogenas_keys(p) if p["var"][k]["obs"][u] is None]
check("toda exogena sem o dado daquele trimestre aparece como segurada",
      sorted(sg["chave"] for sg in r0["segurados"]) == sorted(sem), r0["segurados"])
velho = {"ciclo": "2026-10-15", "p": dict(p, i0=u)}
check("um retrato que ainda projeta um trimestre com dado levanta",
      levanta(lambda: modelo.rodar(velho, faixa=False), "--refazer"))

# 2. o caminho de uma exogena
t1, t3 = jan[1], jan[3]
r1 = modelo.rodar(SIM, caminhos={"fiscal": {t1: 200.0, t3: 180.0}}, faixa=False)
cam, fon = r1["entradas"]["fiscal"]["caminho"], r1["entradas"]["fiscal"]["fonte"]
padrao = r0["entradas"]["fiscal"]["caminho"]
check("antes do primeiro trimestre dado vale o padrao", cam[0] == padrao[0] and fon[0] == "padrão")
check("no trimestre dado entra o valor dado", cam[1] == 200.0 and fon[1] == "cenário")
check("entre dois trimestres dados, segura o anterior", cam[2] == 200.0 and fon[2] == "cenário, segurado")
check("depois do ultimo, segura o ultimo", all(v == 180.0 for v in cam[3:]), cam[3:])
check("'2026T4' e '4T26' sao o mesmo trimestre", modelo._ler_tri("2026T4") == modelo._ler_tri("4T26"))
pt0, pt1 = r0["endogenas"]["ptax"]["central"], r1["endogenas"]["ptax"]["central"]
check("o primeiro trimestre nao se mexe (o CDS so muda depois)", abs(pt1[0] - pt0[0]) < 1e-12)
# A equacao le a VARIACAO do CDS sobre o desvio-padrao dela: +X p.b. -> b*X/sd % no trimestre.
F = p["eq"]["F"]
esperado = F["mediana"]["b_fiscal"] * (200.0 - padrao[0]) / F["sd"]["fiscal"]
obtido = 100 * __import__("math").log((pt1[1] / pt1[0]) / (pt0[1] / pt0[0]))
check("o salto do CDS sai do tamanho que o coeficiente diz (laco incluso, 2%)",
      abs(obtido - esperado) < 0.02 * abs(esperado), f"{obtido:.3f} contra {esperado:.3f}")

# 3. o multiplicador
r2 = modelo.rodar(SIM, caminhos={"fiscal": {t1: 200.0}}, mult={"F.b_fiscal": 0.0}, faixa=False)
check("x0 no CDS desliga o canal: o CDS sobe e a PTAX fica no padrao",
      dif(r2["endogenas"]["ptax"]["central"], pt0) < 1e-12)
r3 = modelo.rodar(SIM, caminhos={"fiscal": {t1: 200.0}}, mult={"F.b_fiscal": 2.0}, faixa=False)
s1 = r1["endogenas"]["ptax"]["central"][1] / pt0[1] - 1
s3 = r3["endogenas"]["ptax"]["central"][1] / pt0[1] - 1
check("x2 no CDS quase dobra o efeito no trimestre do choque", 1.9 < s3 / s1 < 2.1, s3 / s1)
m = r3["mult"][0]
check("e diz onde o coeficiente cai no posterior",
      m["chave"] == "F.b_fiscal" and m["multiplicado"] == 2 * m["mediana"] and not m["dentro"]
      and m["percentil"] == 100.0, m)
fa = modelo.rodar(SIM)
fb = modelo.rodar(SIM, mult={"F.b_fiscal": 1.0, "R.t3": 1.0})
check("x1 nao muda nem a central nem a faixa",
      all(dif(fa["endogenas"][k][q], fb["endogenas"][k][q]) == 0
          for k in fa["endogenas"] for q in ("central", "lo", "hi")))
# O multiplicador vale em cada DESENHO, nao so na mediana: todo desenho de b_fiscal e positivo,
# entao com o CDS subindo a faixa inteira do trimestre do choque sobe com x2.
fc = modelo.rodar(SIM, caminhos={"fiscal": {t1: 200.0}})
fd = modelo.rodar(SIM, caminhos={"fiscal": {t1: 200.0}}, mult={"F.b_fiscal": 2.0})
check("x2 desloca a faixa, nao so a central",
      fd["endogenas"]["ptax"]["lo"][1] > fc["endogenas"]["ptax"]["hi"][1],
      (fd["endogenas"]["ptax"]["lo"][1], fc["endogenas"]["ptax"]["hi"][1]))
check("a faixa usa todos os desenhos", fa["faixa"]["desenhos"] == min(
    p["eq"][k]["n_draws"] for k in p["eq_ordem"]) and fa["faixa"]["nao_convergiu"] == 0, fa["faixa"])

# 4. o que tem de levantar
check("endogena no cenario levanta",
      levanta(lambda: modelo.rodar(SIM, caminhos={"selic": {t1: 10}}, faixa=False), "endógena"))
check("exogena desconhecida levanta",
      levanta(lambda: modelo.rodar(SIM, caminhos={"cds": {t1: 10}}, faixa=False), "desconhecida"))
check("trimestre fora da janela levanta",
      levanta(lambda: modelo.rodar(SIM, caminhos={"fiscal": {"1T20": 10}}, faixa=False), "fora da janela"))
check("multiplicador em sigma levanta",
      levanta(lambda: modelo.rodar(SIM, mult={"F.sigma": 2}, faixa=False), "não aceita"))
check("multiplicador negativo levanta",
      levanta(lambda: modelo.rodar(SIM, mult={"F.b_fiscal": -1}, faixa=False), "≥ 0"))
check("coeficiente desconhecido levanta",
      levanta(lambda: modelo.rodar(SIM, mult={"F.b_cds": 2}, faixa=False), "desconhecido"))
check("todo coeficiente listado e aceito",
      all(modelo._ler_mult(p, {c["chave"]: 1.0}) for c in modelo.coeficientes(SIM)))

# 5. o trimestre que ja fechou
import datetime as dt  # noqa: E402

ano, tri0 = modelo._ler_tri(jan[0])
vira = dt.date(ano + (tri0 == 3), (tri0 + 1) % 4 * 3 + 1, 1)
fe = modelo.rodar({"ciclo": vira.isoformat(), "p": p}, faixa=False)["fechados"]
check(f"no primeiro dia depois de {jan[0]}, ele ja fechou", fe == [jan[0]], fe)
fe = modelo.rodar({"ciclo": (vira - dt.timedelta(days=1)).isoformat(), "p": p}, faixa=False)["fechados"]
check("na vespera, nenhum", fe == [], fe)

print(f"\n{'FALHAS: ' + str(falhas) if falhas else 'tudo ok'}")
sys.exit(1 if falhas else 0)
