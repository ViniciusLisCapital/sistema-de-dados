"""
`mt_produtividade` contra o release "Productivity and Costs" de 2026-09-03 (`prod2.pdf`).

    uv run python tests/test_produtividade.py

Precisa do banco. Nasceu com a carga (2026-09-03) e afirma tres coisas que a carga
sozinha nao afirma, porque exigem os numeros IMPRESSOS no PDF:

1. **As 60 celulas da Tabela A1 e as 24 da Tabela 1/2** saem exatas do banco. E o que
   distingue "os slugs estao mapeados certo" de "carregou sem excecao": um `measure_code`
   trocado entre duas medidas plausiveis passa por toda validacao interna -- as
   identidades continuam fechando, so entre as series erradas.
2. **A subtracao que o texto do release usa erra ate 15,9 p.p.**, e a forma
   multiplicativa fecha. A asserção e sobre as DUAS: se um dia alguem "simplificar" o
   codigo de contribuicao para a subtracao, o numero de 2020T3 vira 54,2% em vez de 39,5%
   e nada levanta.
3. **As 12 taxas de ciclo do texto** (graficos 3 e 4) saem do indice entre as pontas.

Mais os invariantes estruturais que dependem do banco e nao do arquivo: a media anual so
existe em ano completo, `MAX(date)` e o ultimo trimestre, e o conceito de produto e unico
por setor.
"""

from __future__ import annotations

import sys

import pandas as pd

from analytics.us.labor_market import prod_tab
from domain.db.us._gravar import ler

_DATABASE = "macro_us"

_falhas = 0
_total = 0


def ok(cond: bool, msg: str, detalhe: object = "") -> None:
    global _falhas, _total
    _total += 1
    if cond:
        print(f"  ok    {msg}")
    else:
        _falhas += 1
        print(f"  FALHA {msg}" + (f"  -- {detalhe}" if detalhe != "" else ""))


def secao(t: str) -> None:
    print(f"\n{t}")


# ── dado ────────────────────────────────────────────────────────────────────
D = ler(_DATABASE, "SELECT date, setor, medida, duracao, periodicidade, valor, "
                   "classe, conceito_produto FROM mt_produtividade")
if D.empty:
    print("mt_produtividade vazia -- rode a carga antes")
    sys.exit(1)
D["date"] = pd.to_datetime(D["date"])
D["valor"] = pd.to_numeric(D["valor"], errors="coerce")

TRI = D[D["periodicidade"] == "trimestral"].copy()
TRI["q"] = pd.PeriodIndex(TRI["date"], freq="Q")
ANO = D[D["periodicidade"] == "anual"].copy()

_IDX = {(r.setor, r.medida, r.duracao, r.q): r.valor for r in TRI.itertuples()}


def v(setor: str, medida: str, duracao: str, q: str) -> float | None:
    x = _IDX.get((setor, medida, duracao, pd.Period(q, "Q")))
    return None if x is None or pd.isna(x) else round(float(x), 1)


def serie(setor: str, medida: str, duracao: str) -> pd.Series:
    s = (TRI[(TRI.setor == setor) & (TRI.medida == medida) & (TRI.duracao == duracao)]
         .set_index("q")["valor"].sort_index())
    return s[~s.index.duplicated()]


# ── 1. Tabela A1: as 5 secoes x 6 medidas x 2 duracoes ─────────────────────
secao("1. Tabela A1 do release (60 celulas)")

# (setor, [prev qtr], [year ago]) nas colunas
# produtividade | produto | horas | remun/hora | remun/hora real | custo unitario
_A1 = {
    "nonfarm_business":         ([1.4, 1.7, 0.3, 2.6, -3.3, 1.2], [2.2, 2.5, 0.2, 3.7, -0.1, 1.4]),
    "business":                 ([1.2, 1.6, 0.4, 2.4, -3.4, 1.2], [2.1, 2.5, 0.4, 3.5, -0.3, 1.4]),
    "manufacturing":            ([2.4, 5.4, 2.9, 2.1, -3.7, -0.3], [1.1, 1.6, 0.5, 4.5, 0.7, 3.4]),
    "manufacturing_durable":    ([3.6, 8.9, 5.1, 1.4, -4.4, -2.2], [2.5, 3.6, 1.0, 5.6, 1.7, 3.0]),
    "manufacturing_nondurable": ([2.1, 1.4, -0.6, 2.9, -3.0, 0.8], [-0.2, -0.6, -0.4, 2.2, -1.6, 2.4]),
}
_COLS = ["produtividade", "produto_real", "horas_trabalhadas", "remuneracao_hora",
         "remuneracao_hora_real", "custo_unitario_trabalho"]
_erros = []
_n = 0
for setor, (prev, ano) in _A1.items():
    for duracao, esperado in (("tri_anual", prev), ("ano_a_ano", ano)):
        for medida, pub in zip(_COLS, esperado):
            got = v(setor, medida, duracao, "2026Q2")
            _n += 1
            if got != pub:
                _erros.append(f"{setor}/{medida}/{duracao}: {got} != {pub}")
ok(not _erros, f"as {_n} celulas da Tabela A1 saem exatas do banco",
   "; ".join(_erros[:4]))

# ── 2. Tabela 1 e Tabela 2: as 8 colunas nas 3 duracoes ────────────────────
secao("2. Tabelas 1 e 2 (business e nonfarm business, 24 celulas cada)")
_T8 = ["produtividade", "produto_real", "horas_trabalhadas", "remuneracao_hora",
       "remuneracao_hora_real", "custo_unitario_trabalho",
       "pagamento_unitario_nao_trabalho", "deflator_produto"]
_TAB = {
    "business": {
        "tri_anual": [1.2, 1.6, 0.4, 2.4, -3.4, 1.2, 14.8, 7.4],
        "ano_a_ano": [2.1, 2.5, 0.4, 3.5, -0.3, 1.4, 8.8, 4.7],
        "indice":    [120.2, 127.0, 105.6, 149.1, 109.5, 124.0, 143.5, 132.5],
    },
    "nonfarm_business": {
        "tri_anual": [1.4, 1.7, 0.3, 2.6, -3.3, 1.2, 14.8, 7.4],
        # 9.2 e 5.0, nao 8.8 e 4.7: as duas ultimas colunas DIFEREM entre a Tabela 1
        # (business) e a Tabela 2 (nonfarm business), enquanto as seis primeiras
        # coincidem nesta leitura. Copiar a linha de uma na outra passa em 22 das 24
        # celulas.
        "ano_a_ano": [2.2, 2.5, 0.2, 3.7, -0.1, 1.4, 9.2, 5.0],
        "indice":    [120.0, 127.1, 105.9, 148.8, 109.2, 124.0, 144.0, 132.7],
    },
}
for setor, por_dur in _TAB.items():
    _erros = []
    for duracao, esperado in por_dur.items():
        for medida, pub in zip(_T8, esperado):
            got = v(setor, medida, duracao, "2026Q2")
            if got != pub:
                _erros.append(f"{medida}/{duracao}: {got} != {pub}")
    ok(not _erros, f"{setor}: as 24 celulas de 2026 Q2 conferem", "; ".join(_erros[:4]))

# ── 3. Tabela 6: as corporacoes nao financeiras ────────────────────────────
secao("3. Tabela 6 (corporacoes nao financeiras)")
for medida, dur, pub in (("produtividade", "tri_anual", 2.2),
                         ("produto_real", "tri_anual", 3.9),
                         ("horas_trabalhadas", "tri_anual", 1.7),
                         ("lucro_unitario", "tri_anual", 43.0),
                         ("produtividade", "ano_a_ano", 3.1),
                         ("lucro_unitario", "ano_a_ano", 17.8)):
    got = v("nonfinancial_corp", medida, dur, "2026Q2")
    ok(got == pub, f"{medida}/{dur} = {pub}% (texto do release)", got)
# A classe da nao financeira e "empregados": ela nao tem conta propria, por definicao.
classes = D.groupby("setor")["classe"].unique()
ok(list(classes["nonfinancial_corp"]) == ["empregados"],
   "a nao financeira e medida so para empregados (nao tem conta propria)",
   classes["nonfinancial_corp"])
ok(all(list(classes[s]) == ["todos"] for s in classes.index if s != "nonfinancial_corp"),
   "e os outros cinco setores, para todos os trabalhadores")

# ── 4. as duas identidades, nas duas formas ───────────────────────────────
secao("4. As identidades, e por que a subtracao do texto nao serve")
_piores = {}
for duracao in ("tri_anual", "ano_a_ano"):
    sub_max = mul_max = 0.0
    pior_onde = None
    for setor in _A1:
        prod = serie(setor, "produtividade", duracao)
        out = serie(setor, "produto_real", duracao)
        hrs = serie(setor, "horas_trabalhadas", duracao)
        ulc = serie(setor, "custo_unitario_trabalho", duracao)
        comp = serie(setor, "remuneracao_hora", duracao)
        for a, b, c in ((prod, out, hrs), (ulc, comp, prod)):
            e_sub = (a - (b - c)).abs().dropna()
            e_mul = (a - ((1 + b / 100) / (1 + c / 100) - 1) * 100).abs().dropna()
            if len(e_sub) and float(e_sub.max()) > sub_max:
                sub_max = float(e_sub.max())
                pior_onde = f"{setor} em {e_sub.idxmax()}"
            if len(e_mul):
                mul_max = max(mul_max, float(e_mul.max()))
    _piores[duracao] = (sub_max, mul_max, pior_onde)
    ok(mul_max < 0.30,
       f"{duracao}: a forma multiplicativa fecha (residuo maximo {mul_max:.3f} p.p., "
       f"o arredondamento de 3 series de 1 decimal)", mul_max)
    ok(sub_max > 1.0,
       f"{duracao}: e a SUBTRACAO erra {sub_max:.1f} p.p. no pior caso ({pior_onde}) "
       "-- por isso nao pode virar a forma do codigo", sub_max)
# O caso concreto que o apendice cita.
o = v("manufacturing_durable", "produto_real", "tri_anual", "2020Q3")
h = v("manufacturing_durable", "horas_trabalhadas", "tri_anual", "2020Q3")
pr = v("manufacturing_durable", "produtividade", "tri_anual", "2020Q3")
ok(o == 91.3 and h == 37.1 and pr == 39.5,
   f"2020T3 no durable: produto {o}, horas {h}, produtividade publicada {pr}",
   f"{o} / {h} / {pr}")
ok(abs((o - h) - 54.2) < 0.05,
   "a subtracao daria 54,2% -- plausivel, e errado por 14,7 p.p.", o - h)

# No indice as duas identidades sao razoes exatas.
idx_max = 0.0
for setor in list(_A1) + ["nonfinancial_corp"]:
    prod = serie(setor, "produtividade", "indice")
    out = serie(setor, "produto_real", "indice")
    hrs = serie(setor, "horas_trabalhadas", "indice")
    e = (prod - out / hrs * 100).abs().dropna()
    if len(e):
        idx_max = max(idx_max, float(e.max()))
ok(idx_max < 0.005,
   f"no indice a identidade e exata (residuo maximo {idx_max:.4f})", idx_max)

# ── 5. as duas precisoes publicadas ───────────────────────────────────────
secao("5. Tres decimais no indice, um nas variacoes")


def ndec(x: float) -> int:
    t = f"{x:.10f}".rstrip("0")
    return len(t.split(".")[1]) if "." in t else 0


tres = TRI[TRI.duracao == "indice"]["valor"].dropna().map(ndec)
uma = TRI[TRI.duracao != "indice"]["valor"].dropna().map(ndec)
ok(int((tres == 3).sum()) > len(tres) * 0.9,
   f"o indice chega com 3 decimais em {int((tres == 3).sum()):,} de {len(tres):,} celulas",
   dict(tres.value_counts()))
ok(int((uma <= 1).sum()) == len(uma),
   "e as variacoes com no maximo 1 decimal, como o BLS as publica",
   dict(uma.value_counts()))
# O contrafactual: com o indice arredondado a 1 casa, a reconta erra >1 p.p.
s = serie("nonfarm_business", "produtividade", "indice")
pub = serie("nonfarm_business", "produtividade", "tri_anual")
calc3 = ((s / s.shift(1)) ** 4 - 1) * 100
calc1 = ((s.round(1) / s.round(1).shift(1)) ** 4 - 1) * 100
e3 = (pub - calc3).abs().dropna()
e1 = (pub - calc1).abs().dropna()
ok(float(e3.max()) <= 0.0501,
   f"reconta do indice de 3 decimais: erro maximo {float(e3.max()):.4f} p.p. "
   "(metade do digito publicado)", float(e3.max()))
ok(float(e1.max()) > 1.0,
   f"reconta do indice IMPRESSO no release (1 decimal): erro maximo "
   f"{float(e1.max()):.2f} p.p. -- e o aviso reutilizavel", float(e1.max()))

# ── 6. as taxas de ciclo dos graficos 3 e 4 ───────────────────────────────
secao("6. Os graficos 3 e 4 (ciclos economicos)")
_fim = str(TRI["q"].max())


def cagr(s: pd.Series, de: str, ate: str) -> float | None:
    a, b = pd.Period(de, "Q"), pd.Period(ate, "Q")
    if a not in s.index or b not in s.index:
        return None
    return round(((s[b] / s[a]) ** (4 / (b - a).n) - 1) * 100, 1)


_CICLO = {
    "nonfarm_business": {"inicio": "1947Q1",
                         "atual": {"produtividade": 2.1, "produto_real": 2.5,
                                   "horas_trabalhadas": 0.4},
                         "anterior": {"produtividade": 1.5},
                         "longo": {"produtividade": 2.1}},
    "manufacturing": {"inicio": "1987Q1",
                      "atual": {"produtividade": 0.5, "produto_real": 0.2,
                                "horas_trabalhadas": -0.3},
                      "anterior": {"produtividade": 0.1},
                      "longo": {"produtividade": 2.1}},
}
for setor, cfg in _CICLO.items():
    janelas = {"atual": ("2019Q4", _fim),
               "anterior": ("2007Q4", "2019Q4"),
               "longo": (cfg["inicio"], _fim)}
    for ciclo, esperado in cfg.items():
        if ciclo == "inicio":
            continue
        de, ate = janelas[ciclo]
        for medida, pub in esperado.items():
            got = cagr(serie(setor, medida, "indice"), de, ate)
            ok(got == pub, f"{setor}/{ciclo}/{medida} = {pub}% ({de} a {ate})", got)
    s = serie(setor, "produtividade", "indice")
    ok(str(s.index.min()) == cfg["inicio"],
       f"{setor}: a serie comeca em {cfg['inicio']} -- e o que define a janela longa",
       str(s.index.min()))
# A media das trimestrais NAO e a taxa entre as pontas.
s = serie("nonfarm_business", "produtividade", "tri_anual")
m = s[s.index >= pd.Period("2020Q1", "Q")].mean()
ok(abs(m - 2.1) > 0.03,
   f"a media das taxas trimestrais desde 2020 e {m:.2f}%, nao os 2,1% do release "
   "-- as duas contas nao coincidem", round(float(m), 3))

# ── 7. estrutura: media anual, chave e conceito ───────────────────────────
secao("7. Invariantes estruturais")
ok(int(ANO["date"].dt.year.max()) < int(TRI["date"].dt.year.max())
   or int(TRI["q"].max().quarter) == 4,
   "a media anual nao existe para o ano corrente incompleto",
   f"anual ate {int(ANO['date'].dt.year.max())}, trimestral ate {TRI['q'].max()}")
ok(D["date"].max() == TRI["date"].max(),
   "MAX(date) da tabela e o ultimo trimestre -- e o que a checagem de frescor le",
   f"{D['date'].max().date()} vs {TRI['date'].max().date()}")
# No Q05 as duas duracoes de variacao coincidem.
piv = ANO.pivot_table(index=["date", "setor", "medida"], columns="duracao",
                      values="valor", aggfunc="first")
par = piv[["tri_anual", "ano_a_ano"]].dropna()
ok(float((par["tri_anual"] - par["ano_a_ano"]).abs().max()) < 1e-9,
   f"na media anual as duas variacoes coincidem em {len(par):,} celulas",
   float((par["tri_anual"] - par["ano_a_ano"]).abs().max()))
conc = D.groupby("setor")["conceito_produto"].nunique()
ok(int(conc.max()) == 1, "cada setor tem UM conceito de produto", dict(conc))
ok(set(D.loc[D.setor.str.startswith("manufacturing"), "conceito_produto"]) == {"setorial"},
   "os tres de transformacao usam produto setorial")
ok(set(D.loc[~D.setor.str.startswith("manufacturing"), "conceito_produto"])
   == {"valor_adicionado"},
   "e os outros tres, valor adicionado")

# As 4 medidas da Tabela 6 existem so na nao financeira.
so_nfc = [k for k, m in prod_tab.MEDIDAS.items() if m.get("so_nfc")]
ok(len(so_nfc) == 4, "quatro medidas marcadas como exclusivas da nao financeira", so_nfc)
for medida in so_nfc:
    setores = set(D.loc[D.medida == medida, "setor"])
    ok(setores == {"nonfinancial_corp"}, f"{medida} existe so em nonfinancial_corp",
       sorted(setores))

# Nada e aditivo: dois indices de base 100 somam ~200.
du = serie("manufacturing_durable", "produtividade", "indice")
nd = serie("manufacturing_nondurable", "produtividade", "indice")
mf = serie("manufacturing", "produtividade", "indice")
r = ((du + nd) / mf).dropna()
ok(1.9 < float(r.mean()) < 2.15,
   f"durable + nondurable da {float(r.mean()):.3f}x manufacturing no indice "
   "(nunca somam)", float(r.mean()))

print("\n" + "=" * 66)
print(f"{_total - _falhas}/{_total} assercoes ok"
      + (f", {_falhas} FALHAS" if _falhas else ""))
sys.exit(1 if _falhas else 0)
