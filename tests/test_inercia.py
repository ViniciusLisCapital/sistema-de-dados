"""
Testa o CALCULO da classificacao de inercia (analytics/brasil/inflation/inercia.py).

O harness de JS (tests/test_inflation_js.js, secoes 13b/13c) cobre o que o
relatorio faz com o resultado; aqui se testa o resultado em si -- separado
porque o que pode dar errado e diferente. Duas metades:

  1. Unidades, contra series construidas a mao: encadeamento do y/y, exigencia
     de janela contigua, a autocorrelacao em si e o corte em faixas de peso.
     Rodam sem banco.
  2. Contra o banco real: a distribuicao se separa da serie embaralhada (senao
     a medida seria artefato de construcao), as faixas fecham em ~20% do peso,
     e itens indexados conhecidos caem no lado certo. Pula sozinho se nao
     houver banco.

Uso:  uv run python tests/test_inercia.py
      uv run python tests/test_inercia.py --rapido    (so a parte 1)
"""

import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from analytics.brasil.inflation import inercia as I  # noqa: E402

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


def perto(a, b, tol, msg):
    ok(abs(a - b) <= tol, msg, f"esperado ~{b}, veio {a}")


def _serie(valores, inicio="2010-01"):
    idx = pd.date_range(inicio, periods=len(valores), freq="MS")
    return pd.Series(valores, index=idx, dtype=float)


print("=== 1. y/y: encadeamento e contiguidade =====================")
# 12 meses de 1% cada -> (1,01^12 - 1)*100 = 12,6825%
s = _serie([1.0] * 24)
y = I._yoy(s)
ok(y.iloc[:11].isna().all(), "os 11 primeiros meses nao tem janela e saem NaN")
perto(float(y.iloc[11]), (1.01 ** 12 - 1) * 100, 1e-9, "12 meses de +1% encadeiam para +12,6825%")
perto(float(y.iloc[23]), (1.01 ** 12 - 1) * 100, 1e-9, "e segue igual quando a serie e constante")

# Um buraco no meio tem de zerar 12 pontos, nao ser costurado por cima.
com_buraco = _serie([1.0] * 24)
com_buraco.iloc[5] = np.nan
yb = I._yoy(com_buraco)
ok(yb.iloc[11:17].isna().all(), "um mes ausente invalida as 12 janelas que o contem, nao e ignorado")
ok(not np.isnan(yb.iloc[17]), "e o y/y volta assim que a janela limpa passa do buraco")

# _pivot_mensal tem de reindexar para grade completa -- e o que faz o buraco existir.
df = pd.DataFrame({
    "indice": ["IPCA"] * 4,
    "date": pd.to_datetime(["2020-01-01", "2020-02-01", "2020-05-01", "2020-06-01"]),
    "subitem_codigo": ["1101002"] * 4,
    "var_mensal": [1.0, 1.0, 1.0, 1.0],
    "pesos": [0.5] * 4, "contribuicao": [0.005] * 4,
})
piv = I._pivot_mensal(df, "IPCA")
ok(len(piv) == 6, "o pivot reindexa para a grade mensal completa (jan..jun), nao so os meses presentes", len(piv))
ok(piv["1101002"].isna().sum() == 2, "e os meses faltantes ficam NaN de verdade", int(piv["1101002"].isna().sum()))

print("\n=== 2. autocorrelacao ========================================")
# Serie perfeitamente periodica de periodo 12: corr no lag 12 tem de ser 1.
per = _serie([float(i % 12) for i in range(200)])
r, n = I._autocorr(per, 12, min_pares=10)
perto(r, 1.0, 1e-9, "serie de periodo 12 da correlacao 1 no lag 12")
ok(n == 188, "e conta os pares certos (200 - 12)", n)

# Serie constante nao tem variancia -- tem de devolver None, nao NaN nem 0.
r, _ = I._autocorr(_serie([2.0] * 100), 12, min_pares=10)
ok(r is None, "serie sem variancia devolve None, nao um numero", r)

# Abaixo do minimo de pares, nao classifica -- mas informa quantos tinha.
r, n = I._autocorr(_serie([float(i % 7) for i in range(30)]), 12, min_pares=48)
ok(r is None and n == 18, "abaixo do minimo devolve None e o numero de pares disponiveis", (r, n))

# Contra numpy, numa serie qualquer: a implementacao nao pode divergir do padrao.
rng = np.random.default_rng(7)
qualquer = _serie(rng.normal(size=200))
r, _ = I._autocorr(qualquer, 12, min_pares=10)
esperado = np.corrcoef(qualquer.values[12:], qualquer.values[:-12])[0, 1]
perto(r, esperado, 1e-12, "bate com np.corrcoef sobre os mesmos pares")

print("\n=== 3. faixas por peso =======================================")
# 100 subitens de peso igual -> 20 em cada faixa, exatamente.
d = pd.DataFrame({"r12": np.arange(100.0), "peso": [0.01] * 100})
f = I._faixas_por_peso(d)
cont = pd.Series(f).value_counts().sort_index().tolist()
ok(cont == [20] * 5, "pesos iguais dao faixas de 20 subitens cada", cont)
ok(f == sorted(f), "e a faixa nunca anda para tras ao longo da ordem", None)

# Um subitem gigante nao pode engolir uma faixa inteira nem deixar faixa vazia.
d = pd.DataFrame({"r12": np.arange(10.0), "peso": [0.02] * 9 + [0.82]})
f = I._faixas_por_peso(d)
ok(len(set(f)) == 5, "com um subitem de 82% do peso, ainda saem 5 faixas nao vazias", sorted(set(f)))

# O caso que motivou trocar o algoritmo: pesos desiguais em que o corte guloso
# erra. O minimax tem de ficar melhor que o guloso ingenuo.
rng = np.random.default_rng(3)
peso = np.sort(rng.pareto(1.2, 300) + 0.01)
rng.shuffle(peso)
d = pd.DataFrame({"r12": np.arange(300.0), "peso": peso / peso.sum()})
f = I._faixas_por_peso(d)
por_faixa = d.assign(q=f).groupby("q")["peso"].sum()
pior = float((por_faixa - 0.2).abs().max())
ok(len(por_faixa) == 5, "5 faixas", len(por_faixa))
ok(pior < 0.02, "com pesos muito desiguais, nenhuma faixa se afasta 2 p.p. dos 20%",
   f"pior {pior*100:.2f} p.p.")

print("\n=== 3b. faixas de corte fixo =================================")
# Os limites sao fechados a direita -- o rotulo da faixa diz isso, e um subitem
# exatamente em -0,5 ou em 0 nao pode escorregar para a faixa de cima.
ok(I._faixa_fixa(-0.9) == 1 and I._faixa_fixa(-0.5) == 1, "r <= -0,5 e intensamente reversivel")
ok(I._faixa_fixa(-0.4999) == 2 and I._faixa_fixa(0.0) == 2, "-0,5 < r <= 0 e moderadamente reversivel")
ok(I._faixa_fixa(0.0001) == 3 and I._faixa_fixa(0.5) == 3, "0 < r <= +0,5 e moderadamente nao reversivel")
ok(I._faixa_fixa(0.5001) == 4 and I._faixa_fixa(0.99) == 4, "r > +0,5 e intensamente nao reversivel")
ok(len(I._ROTULOS_FIXOS) == len(I._CORTES_FIXOS) + 1,
   "ha um rotulo por faixa -- um corte novo sem rotulo daria KeyError so na geracao",
   (len(I._ROTULOS_FIXOS), len(I._CORTES_FIXOS)))

print("\n=== 4. contra o banco real ===================================")
if "--rapido" in sys.argv:
    print("  PULADO (--rapido) -- nao rodou: distribuicao, faixas reais, sanidade nominal")
else:
    try:
        from analytics.brasil.inflation.generate_report import _load_decomposicao
        dec = _load_decomposicao()
    except Exception as exc:  # noqa: BLE001
        print(f"  PULADO (sem banco: {type(exc).__name__}) -- nao rodou: "
              "distribuicao, faixas reais, sanidade nominal")
        dec = None

    if dec is not None:
        p = I.calcular(dec)
        ok(p["n_classificados"] > 350, "classifica os subitens vivos", p["n_classificados"])
        soma = sum(f["peso"] for f in p["faixas"])
        perto(soma, 1.0, 0.005, "as faixas cobrem ~100% do peso do indice")
        pior = max(abs(f["peso"] / soma - 0.2) for f in p["faixas"]) * 100
        ok(pior <= 1.5, "e cada uma carrega 20% +-1,5 p.p.", f"pior {pior:.2f} p.p.")
        ok(all(p["faixas"][i - 1]["hi"] <= p["faixas"][i]["lo"] for i in range(1, 5)),
           "as faixas nao se sobrepoem em r")

        # O corte de 48 pares e o que inclui a safra de 2020. Se alguem subir
        # para 60 sem perceber, 6,75% do indice sai de fininho.
        pares = [v[2] for v in p["subitens"].values()]
        ok(min(pares) >= I._MIN_PARES, "todo classificado respeita o minimo de pares", min(pares))
        ok(min(pares) < 108, "e a safra de subitens novos (56 pares) esta dentro, nao excluida", min(pares))

        # As duas classificacoes leem o MESMO r12 e so discordam em onde cortar.
        ok(all(len(v) == 4 for v in p["subitens"].values()),
           "cada subitem sai como [r12, faixa_por_peso, n_pares, faixa_fixa]")
        ok(all(v[3] == I._faixa_fixa(v[0]) for v in p["subitens"].values()),
           "e a faixa fixa e deduzivel do proprio r, sem estado paralelo")
        ff = p["faixas_fixas"]
        ok(len(ff) == len(I._CORTES_FIXOS) + 1, "o payload traz as 4 faixas fixas", len(ff))
        ok(sum(f["n"] for f in ff) == p["n_classificados"],
           "que particionam os classificados sem sobra nem repeticao",
           (sum(f["n"] for f in ff), p["n_classificados"]))
        perto(sum(f["peso"] for f in ff), soma, 1e-9, "e cobrem o mesmo peso que as faixas por quintil")
        # O ponto da comparacao: corte fixo NAO equilibra peso, e e assim mesmo.
        # Se um dia equilibrar, a distribuicao de r mudou de forma e a nota da
        # aba precisa ser reescrita.
        maior = max(f["peso"] for f in ff) / soma
        ok(maior > 0.5, "a maior faixa fixa concentra mais de metade do indice (a de r nao e bimodal)",
           f"{maior:.1%}")

        # A justificativa da medida: contra a serie embaralhada.
        dg = I.diagnostico(dec, n_permutacoes=2)
        real, bench = dg["real"], dg["benchmark"]
        print(f"          real media {real['media']:+.4f} dp {real['dp']:.4f} | "
              f"embaralhado {bench['media']:+.4f} dp {bench['dp']:.4f}")
        ok(real["media"] - bench["media"] > 0.10,
           "a distribuicao real se separa da embaralhada (a medida nao e artefato)",
           f"diferenca {real['media'] - bench['media']:+.4f}")
        ok(real["max"] > 0.4 and real["min"] < -0.4,
           "e tem amplitude util nos dois sentidos", f"[{real['min']:.2f}, {real['max']:.2f}]")

        # A instabilidade fora da amostra e o achado mais importante da medida.
        # O teste NAO exige que ela seja alta -- exige que o numero continue
        # sendo medido e reportado, para nao virar promessa esquecida.
        est = dg["estabilidade"]
        print(f"          estabilidade {est['janela_antiga']} vs {est['janela_nova']}: "
              f"corr {est['corr']:+.3f} | mesma faixa {est['mesma_faixa']:.0%} | "
              f"Q5 fica Q5 {est['q5_continua_q5']:.0%}")
        ok(est["n"] > 200, "a comparacao entre janelas tem amostra suficiente", est["n"])
        ok(est["corr"] > 0, "a relacao entre as duas janelas e positiva (ha alguma persistencia)",
           est["corr"])
        ok(est["q5_continua_q5"] < 0.5,
           "e a instabilidade documentada continua real -- se isto passar a falhar, "
           "a nota da aba e o CLAUDE.md precisam ser reescritos, nao o teste",
           f"{est['q5_continua_q5']:.0%}")

        # Sanidade nominal: reajuste anual em cima, commodity/bandeira embaixo.
        nomes = dict(zip(dec["subitem_codigo"], dec["nome"]))
        def faixa_de(parcial):
            for cod, v in p["subitens"].items():
                if parcial.lower() in str(nomes.get(cod, "")).lower():
                    return v[1], v[0]
            return None, None
        for nome, minimo in [("Plano de saúde", 4), ("Empregado doméstico", 4), ("Mão de obra", 4)]:
            q, r = faixa_de(nome)
            ok(q is not None and q >= minimo, f"{nome} cai nas faixas mais inerciais", f"Q{q} r={r}")
        for nome, maximo in [("Gasolina", 2), ("Energia elétrica residencial", 2)]:
            q, r = faixa_de(nome)
            ok(q is not None and q <= maximo, f"{nome} cai nas menos inerciais", f"Q{q} r={r}")

print("\n" + "=" * 62)
print(f"{_oks} ok, {_falhas} falhou")
sys.exit(1 if _falhas else 0)
