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
5. o trimestre que ja fechou nao e marcado;
6. a Selic de fechamento (derivada) nao segue (media de q + media de q+1)/2 na central ou num
   desenho, o ultimo trimestre nao fica em branco, ou o de partida nao e o observado;
7. as contribuicoes dos quatro grupos do IPCA (mais o residuo) nao somam o IPCA de 12 meses, um
   grupo sai com o rotulo de outro, ou o residuo dos trimestres observados some ou vaza para a
   janela toda projetada.

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
    """Maior diferenca; o trimestre em branco (None) tem de estar em branco nos dois."""
    if any((x is None) != (y is None) for x, y in zip(a, b)):
        return float("inf")
    return max(abs(x - y) for x, y in zip(a, b) if x is not None)


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

# 5b. toda exogena diz a convencao do trimestre e de onde vem o valor (pedido do teste solo de PM)
exo = modelo._exogenas_keys(p)
check("toda exogena do simulador tem a convencao declarada em modelo.CONVENCAO",
      set(exo) <= set(modelo.CONVENCAO), sorted(set(exo) - set(modelo.CONVENCAO)))
check("e nenhuma declaracao sobra (exogena que saiu do simulador)",
      set(modelo.CONVENCAO) <= set(exo), sorted(set(modelo.CONVENCAO) - set(exo)))
ls = modelo.listar(SIM)
check("o listar imprime a convencao de cada exogena", ls.count("trimestre: **") == len(exo))
check("o Fed Funds e o efetivo do ultimo mes, nao o ponto medio",
      modelo.CONVENCAO["ffr"][0] == "último mês do trimestre" and "EFETIVO" in modelo.CONVENCAO["ffr"][1])

# 6. a Selic de fechamento, derivada das medias (decisao do usuario em 2026-10-21, a revisar)
med, fim = r0["endogenas"]["selic"]["central"], r0["endogenas"]["selic_fim"]["central"]
check("central: fechamento de q = (media de q + media de q+1) / 2",
      all(abs(fim[j] - (med[j] + med[j + 1]) / 2) < 1e-12 for j in range(len(med) - 1)))
check("o ultimo trimestre projetado fica em branco", fim[-1] is None and len(fim) == len(med), fim[-1])
# Num desenho: a mesma regra sobre as medias DAQUELE desenho, nao sobre as da central.
from analytics.brasil.structural_model import simulator as sm  # noqa: E402

i0, h = p["i0"], p["h_padrao"]
sd, _ = sm.resolver(p, modelo._coefs(p, {}, 7), i0, h, sm.entradas(p, i0, h))
s7 = modelo._saidas(p, sd, modelo._coefs(p, {}, 7)["I"])
check("num desenho: o fechamento e o das medias do desenho",
      all(abs(s7["selic_fim"][j] - (sd["selic"][j] + sd["selic"][j + 1]) / 2) < 1e-12 for j in range(h - 1))
      and s7["selic_fim"][-1] is None and dif(s7["selic"], med) > 1e-6)
ef = fa["endogenas"]["selic_fim"]
check("a faixa do fechamento existe nos 11 primeiros e fica em branco no ultimo",
      all(lo is not None and lo <= c <= hi for lo, c, hi in zip(ef["lo"][:-1], ef["central"][:-1], ef["hi"][:-1]))
      and ef["lo"][-1] is None and ef["hi"][-1] is None)
check("e o texto diz que ela e derivada", "DERIVADA" in modelo.texto(fa) and "(derivada)" in ef["nome"])

# O de partida e o OBSERVADO: do A do ciclo se a tabela estiver la, senao do retrato.
import gzip  # noqa: E402
import tempfile  # noqa: E402

rot = p["rot"][-1]
fim_tri = modelo._fim_tri(rot)
with tempfile.TemporaryDirectory() as tmp:
    pasta = Path(tmp)
    original = modelo._pasta_a
    modelo._pasta_a = lambda ciclo: pasta
    try:
        retrato = {"rot": rot, "valor": 99.0, "data": str(fim_tri), "fonte": "banco, no retrato"}
        r_ret = modelo.rodar({"ciclo": "2026-10-15", "p": p, "selic_fim": retrato}, faixa=False)
        check("sem a tabela no A, o fechamento de partida vem do retrato",
              r_ret["partida"]["selic_fim"] == 99.0, r_ret["partida"]["selic_fim"])
        linhas = ["date,curve,tenor,tenor_years,value",
                  f"{fim_tri.replace(day=1)},POLICY,1d,0.003968,14.00",
                  f"{fim_tri},POLICY,1d,0.003968,13.75",
                  f"{fim_tri + __import__('datetime').timedelta(days=1)},POLICY,1d,0.003968,13.50",
                  f"{fim_tri},DIPRE,12M,1.0,12.00"]
        with gzip.open(pasta / "br_interest_rate.csv.gz", "wt", encoding="utf-8") as fh:
            fh.write("\n".join(linhas) + "\n")
        r_a = modelo.rodar({"ciclo": "2026-10-15", "p": p, "selic_fim": retrato}, faixa=False)
        check("com a tabela no A, ela ganha do retrato: a POLICY do ultimo dia do trimestre",
              r_a["partida"]["selic_fim"] == 13.75, r_a["partida"]["selic_fim"])
        r_n = modelo.rodar({"ciclo": "2026-10-15", "p": p, "selic_fim": dict(retrato, rot="1999T1")}, faixa=False)
        check("retrato de outro trimestre nao vale (e o A ainda vale)", r_n["partida"]["selic_fim"] == 13.75)
    finally:
        modelo._pasta_a = original

# 7. os quatro grupos do IPCA, como contribuicao para o de 12 meses (decisao de 2026-10-22)
GR = [f"ipca_12m_{s}" for s in modelo.GRUPOS.values()] + ["ipca_12m_residuo"]
check("as quatro contribuicoes e o residuo estao em SAIDAS e no resultado, em p.p.",
      all(k in fa["endogenas"] and fa["endogenas"][k]["unidade"] == "p.p." for k in GR)
      and {k for k, *_ in modelo.SAIDAS} >= set(GR))
check("os grupos de modelo.GRUPOS sao os da (I)", set(modelo.GRUPOS) == set(p["eq"]["I"]["ordem_grupos"]))
i12 = fa["endogenas"]["ipca_12m"]["central"]
soma = [sum(fa["endogenas"][k]["central"][j] for k in GR) for j in range(h)]
check("grupos + residuo somam o IPCA de 12 meses em todo trimestre projetado",
      dif(soma, i12) < 1e-8, dif(soma, i12))
# Num desenho tambem: a decomposicao e refeita com os pesos daquele desenho.
check("e num desenho", dif([sum(s7[k][j] for k in GR) for j in range(h)], s7["ipca_12m"]) < 1e-8)
pa = fa["partida"]
check("e no trimestre de partida, contra o IPCA 12m publicado (6 casas no payload)",
      abs(sum(pa[k] for k in GR) - pa["ipca_12m"]) < 1e-5, sum(pa[k] for k in GR) - pa["ipca_12m"])
res_ = fa["endogenas"]["ipca_12m_residuo"]["central"]
check("o residuo e zero com a janela toda projetada (do 4o trimestre em diante)",
      all(x == 0.0 for x in res_[3:]), res_[3:])
check("e nao e zero enquanto a janela tem trimestre observado (o IPCA publicado != soma dos grupos)",
      any(abs(x) > 1e-4 for x in res_[:3]) and abs(pa["ipca_12m_residuo"]) > 1e-4, (res_[:3], pa["ipca_12m_residuo"]))
check("o residuo nao tem faixa (so depende do observado)",
      fa["endogenas"]["ipca_12m_residuo"]["lo"] == fa["endogenas"]["ipca_12m_residuo"]["hi"] == res_)
check("a faixa de cada grupo contem a central",
      all(e["lo"][j] <= e["central"][j] <= e["hi"][j] and e["lo"][j] < e["hi"][j]
          for k in GR[:-1] for e in [fa["endogenas"][k]] for j in range(h)))
# O rotulo: contra uma conta independente, sem encadear. O encadeamento so multiplica cada
# trimestre pelo cheio dos anteriores, entao a diferenca fica entre 0 e aprox x IPCA12m/100 (com
# as parcelas positivas). Medido: ate 0,03 p.p.; trocar dois rotulos sai alem disso.
I = p["eq"]["I"]


def no_limite(v, aprox, i12_):
    return -1e-9 <= v - aprox <= abs(aprox) * i12_ / 100 + 1e-9


# A chave de cada grupo sai do NOME que a saida imprime contra o nome do grupo no payload, e nao de
# modelo.GRUPOS: um GRUPOS com dois rotulos trocados passaria num teste que lesse o mesmo GRUPOS
# (mutante verificado).
nomes = {k: n for k, n, *_ in modelo.SAIDAS}
chave = {}
for g, G in I["grupos"].items():
    ks = [k for k in GR if nomes[k].endswith("contribuição de " + G["nome_frase"])]
    check(f"uma saida, e so uma, se chama contribuicao de {G['nome_frase']}", len(ks) == 1, ks)
    chave[g] = ks[0] if ks else None
for g, k in chave.items():
    aprox = sum(I["pesos_obs"][g][i] * I["obs_grupo"][g][i] for i in range(u - 3, u + 1))
    check(f"partida: {k} e o grupo {g} (peso x variacao somado na janela, mais o encadeamento)",
          k is not None and no_limite(pa[k], aprox, pa["ipca_12m"]), (k and pa[k], aprox))
partes = []
sm._sim_infl(p, modelo._coefs(p, {})["I"], i0, h, sm.resolver(p, modelo._coefs(p, {}), i0, h,
                                                             sm.entradas(p, i0, h))[0], partes=partes)
for g, k in chave.items():
    aprox = sum(pt["pesos"][g] * pt["grupos"][g] for pt in partes[-4:])
    check(f"ultimo trimestre projetado: {k} e o grupo {g}",
          k is not None and no_limite(fa["endogenas"][k]["central"][-1], aprox, i12[-1]),
          (k and fa["endogenas"][k]["central"][-1], aprox))
tx = modelo.texto(fa)
check("o texto imprime as quatro contribuicoes e diz a unidade e o residuo",
      all(fa["endogenas"][k]["nome"] in tx for k in GR) and "em p.p." in tx and "as faixas não somam" in tx)

print(f"\n{'FALHAS: ' + str(falhas) if falhas else 'tudo ok'}")
sys.exit(1 if falhas else 0)
