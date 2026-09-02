"""
Testa a classificacao de ciclo de politica monetaria que pinta o fundo dos 3 graficos
da aba Impulso (analytics/brasil/credit/impulso_tab.py :: build_ciclos).

A conta e simples; o que pode dar errado nao e. Tres coisas:

  1. A REGRA. Um bloco de manutencoes cercado por movimentos da mesma direcao tem de
     sair CINZA, e nao absorvido pelo ciclo que o cerca -- e a decisao de metodo da
     rodada, e o caso que a motivou (Selic em 6,50% de mai/2018 a jul/2019) so aparece
     no dado real.
  2. O RECORTE. As faixas sao `shapes` com `xref: 'x'`, que entram no autorange do
     Plotly: uma faixa de 1999 que escape do recorte estica o eixo X de um grafico que
     comeca em 2007 sem plotar nada la, e o sintoma no browser e "o grafico abriu
     vazio", nao um erro.
  3. A COBERTURA. As faixas tem de ser contiguas e nao se sobrepor -- um buraco pinta
     de branco um mes que teve regime, e uma sobreposicao soma dois alfas e cria uma
     quarta cor que nao esta na legenda.

Uso:  uv run python tests/test_credit_ciclos.py
      uv run python tests/test_credit_ciclos.py --rapido    (so a parte sem banco)
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from analytics.brasil.credit import impulso_tab as IT  # noqa: E402

_falhas = 0
_oks = 0


def ok(cond, msg, extra=None):
    global _falhas, _oks
    if cond:
        _oks += 1
        print(f"  ok      {msg}")
    else:
        _falhas += 1
        print(f"  FALHOU  {msg}" + (f"  -> {extra}" if extra is not None else ""))


def tipos(faixas):
    return [f["tipo"] for f in faixas]


print("=== 1. Fusao de decisoes iguais consecutivas ==================")
r = [("2020-01-01", "elevacao"), ("2020-02-01", "elevacao"), ("2020-03-01", "reducao")]
f = IT.build_ciclos(r, fim="2020-04-01")
ok(tipos(f) == ["alta", "queda"], "3 reunioes / 2 direcoes viram 2 faixas", tipos(f))
ok(f[0]["de"] == "2020-01-01" and f[0]["ate"] == "2020-03-01",
   "a faixa vai da 1a reuniao do bloco ate a reuniao que muda o regime", f[0])
ok(f[-1]["ate"] == "2020-04-01", "a ultima faixa fecha no `fim` pedido, nao na reuniao", f[-1])

print("\n=== 2. Um bloco de manutencao NAO e absorvido =================")
# alta, [manutencao x3], alta -- a suavizacao "de mercado" faria disso uma faixa
# vermelha so. Aqui tem de sair alta / cinza / alta.
r = ([("2020-01-01", "elevacao")]
     + [(f"2020-0{m}-01", "manutencao") for m in (2, 3, 4)]
     + [("2020-05-01", "elevacao")])
f = IT.build_ciclos(r, fim="2020-06-01")
ok(tipos(f) == ["alta", "manutencao", "alta"],
   "manutencao entre duas altas continua sendo manutencao", tipos(f))
ok(f[1]["de"] == "2020-02-01" and f[1]["ate"] == "2020-05-01",
   "e o bloco cinza cobre da 1a manutencao ate a reuniao que retoma o ciclo", f[1])

print("\n=== 3. Recorte a janela plotada ===============================")
r = [("1999-04-14", "reducao"), ("2010-01-01", "elevacao"), ("2020-01-01", "reducao")]
f = IT.build_ciclos(r, inicio="2015-01-01", fim="2026-01-01")
ok(all(x["de"] >= "2015-01-01" for x in f), "nenhuma faixa comeca antes do `inicio`", f)
ok(all(x["ate"] <= "2026-01-01" for x in f), "nenhuma faixa termina depois do `fim`", f)
ok(f[0]["de"] == "2015-01-01" and f[0]["tipo"] == "alta",
   "a faixa que cruza o `inicio` e cortada nele, nao descartada", f[0])
f_antes = IT.build_ciclos(r, inicio="1990-01-01", fim="1995-01-01")
ok(f_antes == [], "janela inteiramente ANTES da 1a reuniao nao pinta nada", f_antes)
# Depois da ultima reuniao e o caso oposto, e de proposito: o regime decidido na
# ultima reuniao continua valendo ate o fim do dado plotado. E o caso normal, alias --
# o relatorio quase sempre e gerado entre duas reunioes.
f_depois = IT.build_ciclos(r, inicio="2030-01-01", fim="2031-01-01")
ok(len(f_depois) == 1 and f_depois[0]["tipo"] == "queda"
   and (f_depois[0]["de"], f_depois[0]["ate"]) == ("2030-01-01", "2031-01-01"),
   "o ultimo regime segue em vigor depois da ultima reuniao, ate o fim da janela", f_depois)

print("\n=== 4. Decisao desconhecida e ignorada ========================")
r = [("2020-01-01", "elevacao"), ("2020-02-01", "vies_de_baixa"), ("2020-03-01", "reducao")]
f = IT.build_ciclos(r, fim="2020-04-01")
ok(tipos(f) == ["alta", "queda"], "rotulo fora do mapa nao vira faixa nem quebra o bloco", tipos(f))

# ── Parte 2: contra o banco real ────────────────────────────────────────────────
if "--rapido" in sys.argv:
    print(f"\n{_oks} ok, {_falhas} falhas (parte 2 pulada por --rapido)")
    sys.exit(1 if _falhas else 0)

print("\n=== 5. Contra pm_copom_reuniao (banco real) ===================")
try:
    from analytics.brasil.credit.generate_report import _load_copom_reunioes
    reunioes = _load_copom_reunioes()
except Exception as exc:  # noqa: BLE001
    print(f"  (pulado -- sem banco: {exc})")
    reunioes = None

if reunioes:
    ok(len(reunioes) > 200, f"{len(reunioes)} reunioes carregadas")
    f = IT.build_ciclos(reunioes, inicio="2007-03-01", fim="2026-07-16")

    # 3a: contiguidade e ausencia de sobreposicao
    gaps = [(f[i]["ate"], f[i + 1]["de"]) for i in range(len(f) - 1) if f[i]["ate"] != f[i + 1]["de"]]
    ok(not gaps, "as faixas sao contiguas -- sem buraco e sem sobreposicao", gaps[:3])
    ok(all(x["de"] < x["ate"] for x in f), "nenhuma faixa tem largura zero ou negativa")
    ok(all(tipos(f)[i] != tipos(f)[i + 1] for i in range(len(f) - 1)),
       "nenhuma faixa vizinha repete o tipo (a fusao rodou)")

    # O caso que decidiu a regra: Selic parada em 6,50% entre mai/2018 e jul/2019,
    # cercada por cortes dos dois lados.
    plato = [x for x in f if x["de"] <= "2019-01-01" <= x["ate"]]
    ok(len(plato) == 1 and plato[0]["tipo"] == "manutencao",
       "jan/2019 (plato de 6,50%) e MANUTENCAO, nao continuacao do ciclo de queda", plato)
    ok(plato and plato[0]["de"] == "2018-05-16" and plato[0]["ate"] == "2019-07-31",
       "e o plato cobre mai/2018 -> jul/2019 inteiro", plato)

    # Duas leituras de manchete que qualquer um confere de cabeca.
    atual = f[-1]
    ok(atual["tipo"] == "queda" and atual["de"] == "2026-03-18",
       "a faixa corrente e o ciclo de queda iniciado em 2026-03-18", atual)
    aperto = [x for x in f if x["de"] == "2021-03-17"]
    ok(len(aperto) == 1 and aperto[0]["tipo"] == "alta" and aperto[0]["ate"] == "2022-09-21",
       "o ciclo de alta de 2021-2022 vai de 2021-03-17 a 2022-09-21", aperto)

    # O recorte tem de morder: a 1a reuniao e de 1999 e o grafico comeca em 2007.
    ok(f[0]["de"] == "2007-03-01", "a 1a faixa foi cortada no inicio da janela", f[0]["de"])
    ok(f[-1]["ate"] == "2026-07-16", "a ultima faixa foi cortada no fim da janela", f[-1]["ate"])

print(f"\n{_oks} ok, {_falhas} falhas")
sys.exit(1 if _falhas else 0)
