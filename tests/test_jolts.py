"""
Testa o ramo JOLTS de `macro_us` contra o release publicado e contra si mesmo.

    uv run python tests/test_jolts.py

Precisa de banco ao vivo (`macro_us.mt_jolts` + `mt_jolts_dim` carregadas).

Cada secao existe por um modo de falha que **nao lanca excecao**:

  1. TABELA A / TABELA 7. O jeito de saber que o series_id de 21 caracteres foi montado
     certo e reproduzir o PDF. A primeira tentativa usou 19 caracteres e devolveu
     `None` nas 168 celulas -- nao um erro, so ausencia. Aqui as 210 celulas do release
     de julho/2026 sao literais no teste.
  2. ADITIVIDADE. Um pai trocado de lugar continua plotando. A tolerancia vem do
     arredondamento ao milhar do BLS, `0,5*(k+1)`, nao de um epsilon a dedo.
  3. DENOMINADOR DAS TAXAS. A afirmacao que o relatorio imprime no eixo Y e no apendice
     ("openings / (employment + openings)") e testada, nao parafraseada da
     documentacao -- via o emprego implicito nas contratacoes.
  4. AS TRES ARVORES. Uma raiz a mais ou a menos, ou um no orfao, faz a linha
     desaparecer da tabela em silencio.
  5. RAIZ COMPARTILHADA. `industria|100000` e `tamanho|00` sao a MESMA serie do BLS. Se
     o mapa de destinos voltar a ser 1-para-1, um dos dois cortes perde a raiz sem
     erro -- foi o que aconteceu na primeira carga.
  6. BURACOS. O unico valor ausente e a razao UO em 2025-10. Qualquer outro nulo e
     defeito de carga, nao da fonte.
  7. CARTOES. Chave orfa produz botao que nunca nasce; `full` redundante faz o cartao
     abrir para repetir o rotulo.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from analytics.us.labor_market import jolts_tab                       # noqa: E402
from domain.db.us._gravar import ler                                  # noqa: E402
from domain.db.us.labor_market.mt_jolts_dim import MEDIDAS, series_id  # noqa: E402

_falhas = 0
_asserts = 0


def ok(cond, nome, detalhe=""):
    global _falhas, _asserts
    _asserts += 1
    if cond:
        print(f"  ok    {nome}")
    else:
        _falhas += 1
        print(f"  FALHA {nome}" + (f"  -- {detalhe}" if detalhe else ""))


def secao(t):
    print(f"\n{t}")


# ---------------------------------------------------------------- dados
dim = ler("macro_us", "SELECT * FROM mt_jolts_dim ORDER BY corte, ordem")
dados = ler("macro_us", "SELECT date, corte, categoria, medida, tipo, ajuste, valor, "
                        "natureza, series_id FROM mt_jolts")
dados["date"] = pd.to_datetime(dados["date"])
REF = pd.Timestamp("2026-07-01")   # mes de referencia do PDF em jolts.pdf

# ---------------------------------------------------------------- 1. release
secao("1. O release publicado, celula a celula (BLS, JOLTS, julho/2026)")

mes = dados[dados["date"] == REF]
val = {(r.corte, r.categoria, r.medida, r.tipo, r.ajuste): r.valor for r in mes.itertuples()}

# Tabela A: (industry_code, JO L, HI L, TS L, JO R, HI R, TS R), SA, julho/2026p.
TABELA_A = [
    ("000000", 7271, 5054, 5072, 4.4, 3.2, 3.2),
    ("100000", 6461, 4758, 4731, 4.5, 3.5, 3.5),
    ("110099", 22, 24, 25, 3.5, 4.0, 4.1),
    ("230000", 326, 366, 324, 3.8, 4.4, 3.9),
    ("300000", 580, 288, 286, 4.4, 2.3, 2.3),
    ("320000", 429, 177, 162, 5.2, 2.2, 2.1),
    ("340000", 151, 111, 124, 3.1, 2.3, 2.6),
    ("400000", 1271, 1059, 1104, 4.2, 3.7, 3.8),
    ("420000", 224, 156, 168, 3.6, 2.6, 2.8),
    ("440000", 731, 625, 658, 4.5, 4.0, 4.3),
    ("480099", 316, 277, 277, 4.2, 3.9, 3.8),
    ("510000", 96, 68, 70, 3.3, 2.4, 2.5),
    ("510099", 401, 149, 167, 4.2, 1.6, 1.8),
    ("520000", 285, 92, 106, 4.1, 1.4, 1.6),
    ("530000", 116, 57, 61, 4.6, 2.3, 2.5),
    ("540099", 1138, 900, 901, 4.8, 4.0, 4.0),
    ("600000", 1553, 777, 752, 5.3, 2.8, 2.7),
    ("610000", 116, 101, 95, 2.8, 2.5, 2.3),
    ("620000", 1438, 676, 657, 5.7, 2.8, 2.7),
    ("700000", 783, 885, 896, 4.4, 5.2, 5.3),
    ("710000", 110, 149, 154, 4.0, 5.6, 5.8),
    ("720000", 673, 736, 742, 4.5, 5.2, 5.2),
    ("810000", 291, 242, 207, 4.6, 4.0, 3.4),
    ("900000", 810, 296, 341, 3.4, 1.3, 1.5),
    ("910000", 108, 26, 31, 3.9, 1.0, 1.1),
    ("920000", 702, 270, 311, 3.3, 1.3, 1.5),
    ("923000", 251, 130, 156, 2.3, 1.2, 1.4),
    ("929000", 451, 140, 155, 4.4, 1.4, 1.6),
]
_COLS_A = [("JO", "nivel"), ("HI", "nivel"), ("TS", "nivel"),
           ("JO", "taxa"), ("HI", "taxa"), ("TS", "taxa")]
divergentes = []
for linha in TABELA_A:
    for k, (medida, tipo) in enumerate(_COLS_A):
        got = val.get(("industria", linha[0], medida, tipo, "sa"))
        esperado = linha[1 + k]
        if got is None or abs(got - esperado) > 1e-9:
            divergentes.append(f"{linha[0]}/{medida}/{tipo}: PDF {esperado} x banco {got}")
ok(not divergentes,
   f"Tabela A: 168 celulas conferem exatamente ({len(TABELA_A)} industrias x 6)",
   "; ".join(divergentes[:4]))

# Tabela 7: niveis por classe de tamanho, SA, julho/2026p. Raiz = Total private.
TABELA_7 = {
    "JO": [6461, 1430, 1968, 1602, 729, 491, 241],
    "HI": [4758, 700, 1631, 1559, 540, 248, 80],
    "TS": [4731, 563, 1504, 1727, 609, 255, 73],
    "QU": [2866, 286, 938, 1099, 368, 131, 44],
    "LD": [1582, 192, 470, 577, 214, 110, 20],
    "OS": [283, 85, 97, 51, 27, 15, 8],
}
_CLASSES = ["00", "01", "02", "03", "04", "05", "06"]
divergentes = []
for medida, esperados in TABELA_7.items():
    for cat, esperado in zip(_CLASSES, esperados):
        got = val.get(("tamanho", cat, medida, "nivel", "sa"))
        if got is None or abs(got - esperado) > 1e-9:
            divergentes.append(f"{cat}/{medida}: PDF {esperado} x banco {got}")
ok(not divergentes, "Tabela 7: 42 celulas de nivel conferem exatamente",
   "; ".join(divergentes[:4]))

# A raiz do corte de tamanho NAO e a do corte de industria -- e o erro que a nota da
# aba existe para prevenir, e ele e verificavel: sao 810 mil vagas de governo.
jo_industria = val[("industria", "000000", "JO", "nivel", "sa")]
jo_tamanho = val[("tamanho", "00", "JO", "nivel", "sa")]
ok(abs((jo_industria - jo_tamanho) - 810) < 1e-9,
   "a raiz do corte de tamanho e 810 mil vagas menor que a do corte de industria",
   f"{jo_industria} - {jo_tamanho} = {jo_industria - jo_tamanho}")

# ---------------------------------------------------------------- 2. aditividade
secao("2. Aditividade dos niveis, historia inteira, 3 cortes x 6 medidas x 2 ajustes")

largo = dados[dados["tipo"] == "nivel"].pivot_table(
    index="date", columns=["corte", "categoria", "medida", "ajuste"], values="valor")
total, pior, pior_ctx, estouros = 0, 0.0, None, []
for corte, sub in dim.groupby("corte", sort=False):
    por_cat = sub.set_index("categoria")
    for ajuste in ("sa", "nsa"):
        for medida in MEDIDAS:
            for cat in por_cat.index:
                filhos = [c for c in por_cat.index[por_cat["pai"] == cat]]
                cols_f = [(corte, c, medida, ajuste) for c in filhos]
                col_p = (corte, cat, medida, ajuste)
                cols_f = [c for c in cols_f if c in largo.columns]
                if not cols_f or col_p not in largo.columns:
                    continue
                soma = largo[cols_f].sum(axis=1, min_count=len(cols_f))
                resid = (soma - largo[col_p]).abs().dropna()
                if resid.empty:
                    continue
                limite = 0.5 * (len(cols_f) + 1)
                total += len(resid)
                if resid.max() > limite:
                    estouros.append(f"{corte}/{cat} {medida} {ajuste}: {resid.max():.3f} > {limite}")
                if resid.max() > pior:
                    pior, pior_ctx = resid.max(), f"{corte}/{cat} {medida} {ajuste}"
ok(not estouros, f"{total:,} checagens, nenhuma acima do limite de arredondamento",
   "; ".join(estouros[:3]))
ok(pior <= 3.0, f"pior residuo {pior:.3f} mil ({pior_ctx}) — dentro de 3 mil",
   f"pior={pior}")
ok(total > 40000, f"cobertura: {total:,} checagens (esperado ~40 mil)")

# E a contraprova: as TAXAS nao somam, e e por isso que a validacao nao as inclui.
tx = dados[(dados["tipo"] == "taxa") & (dados["corte"] == "industria")
           & (dados["ajuste"] == "sa") & (dados["medida"] == "JO")]
tx = tx.pivot_table(index="date", columns="categoria", values="valor")
setores = dim[(dim["corte"] == "industria") & (dim["pai"] == "100000")]["categoria"].tolist()
soma_tx = tx[[c for c in setores if c in tx.columns]].sum(axis=1, min_count=len(setores))
gap = (soma_tx - tx["100000"]).abs().dropna()
razao = (soma_tx / tx["100000"]).dropna()
ok(razao.min() > 5,
   f"as taxas dos 10 setores NAO somam a de Total private: a soma delas e {razao.min():.1f}x "
   f"a taxa do pai no melhor caso, {razao.max():.1f}x no pior (gap minimo {gap.min():.1f} p.p.)",
   f"razao min {razao.min()}")

# ---------------------------------------------------------------- 3. denominadores
secao("3. Os denominadores das taxas, reconstruidos do proprio dado")

p = dados[(dados["corte"] == "industria") & (dados["ajuste"] == "sa")].pivot_table(
    index=["date", "categoria"], columns=["medida", "tipo"], values="valor")
emprego = p[("HI", "nivel")] / (p[("HI", "taxa")] / 100)

jo_hat = p[("JO", "nivel")] / (emprego + p[("JO", "nivel")]) * 100
err_certo = (jo_hat - p[("JO", "taxa")]).abs().dropna()
jo_alt = p[("JO", "nivel")] / emprego * 100
err_errado = (jo_alt - p[("JO", "taxa")]).abs().dropna()
ok(err_certo.mean() < 0.06,
   f"taxa de vagas = vagas/(emprego+vagas): erro medio {err_certo.mean():.4f} p.p. "
   f"em {len(err_certo):,} celulas")
ok(err_errado.mean() > 3 * err_certo.mean(),
   f"a hipotese errada (vagas/emprego) erra {err_errado.mean() / err_certo.mean():.1f}x mais "
   f"({err_errado.mean():.4f} p.p.)")
for medida in ("TS", "QU", "LD", "OS"):
    hat = p[(medida, "nivel")] / emprego * 100
    e = (hat - p[(medida, "taxa")]).abs().dropna()
    ok(e.mean() < 0.06,
       f"taxa de {medida} = {medida}/emprego: erro medio {e.mean():.4f} p.p.",
       f"media {e.mean()}")

# ---------------------------------------------------------------- 4. arvores
secao("4. As 3 arvores")

arvs = jolts_tab.arvores(dim)
ok(set(arvs) == {"industria", "tamanho", "regiao"}, "3 cortes montados")
esperado_forma = {"industria": (28, 4, "000000"), "tamanho": (7, 2, "00"), "regiao": (5, 2, "00")}
for corte, (n, niveis, raiz) in esperado_forma.items():
    cfg = arvs[corte]
    ok(cfg["nLinhas"] == n and cfg["niveis"] == niveis and cfg["anchor"] == raiz,
       f"{corte}: {n} linhas, {niveis} niveis, raiz {raiz}",
       f"veio {cfg['nLinhas']}/{cfg['niveis']}/{cfg['anchor']}")
    ok(len(cfg["tree"]) == 1, f"{corte}: exatamente 1 raiz")

# Todo no da dim aparece na arvore montada -- um pai errado tira o no e a subarvore
# dele da tabela, sem erro nenhum.
for corte, cfg in arvs.items():
    achatado = []

    def walk(ns):
        for n in ns:
            achatado.append(n["key"])
            walk(n.get("children") or [])
    walk(cfg["tree"])
    na_dim = set(dim[dim["corte"] == corte]["categoria"])
    ok(set(achatado) == na_dim and len(achatado) == len(na_dim),
       f"{corte}: todos os {len(na_dim)} nos da dim estao na arvore, sem duplicata",
       f"arvore {len(achatado)} x dim {len(na_dim)}")

# ---------------------------------------------------------------- 5. raiz compartilhada
secao("5. As raizes compartilhadas sao a MESMA serie do BLS")

pares = [
    (("industria", "100000"), ("tamanho", "00")),
    (("industria", "000000"), ("regiao", "00")),
]
for (c1, k1), (c2, k2) in pares:
    a = dados[(dados["corte"] == c1) & (dados["categoria"] == k1)]
    b = dados[(dados["corte"] == c2) & (dados["categoria"] == k2)]
    idx = ["date", "medida", "tipo", "ajuste"]
    ja = a.set_index(idx)["valor"].sort_index()
    jb = b.set_index(idx)["valor"].sort_index()
    comum = ja.index.intersection(jb.index)
    dif = (ja.loc[comum] - jb.loc[comum]).abs()
    ok(len(comum) > 5000 and (dif.fillna(0) < 1e-9).all(),
       f"{c1}/{k1} == {c2}/{k2} em {len(comum):,} observacoes",
       f"n={len(comum)}, pior dif {dif.max()}")
    ids_a = set(a["series_id"].unique())
    ids_b = set(b["series_id"].unique())
    so_em_a = {i for i in ids_a - ids_b}
    # A unica serie que pode sobrar em `industria/000000` e a razao UO (vagas por
    # desempregado): o BLS a publica so no total nonfarm nacional, entao nem o corte
    # de tamanho nem o de regiao a reivindicam.
    ok(ids_b <= ids_a and all(i.endswith("UOR") for i in so_em_a),
       f"  e vem literalmente do mesmo series_id ({len(ids_b)} compartilhados"
       + (f", + {len(so_em_a)} de UO so na raiz de industria)" if so_em_a else ")"),
       f"so em A e nao e UO: {sorted(i for i in so_em_a if not i.endswith('UOR'))[:3]}")

# ---------------------------------------------------------------- 6. buracos
secao("6. Buracos")

proprias = dados[dados["medida"] != "UO"]
nulos = proprias[proprias["valor"].isna()]
ok(len(nulos) == 0,
   f"nenhum valor ausente nas 6 medidas do JOLTS ({len(proprias):,} observacoes) — "
   "inclusive em 2025-10, quando a CPS parou e o JOLTS nao",
   f"{len(nulos)} nulos: {nulos[['date', 'corte', 'medida']].head(3).to_dict('records')}")

uo = ler("macro_us", "SELECT date, valor FROM mt_jolts WHERE medida='UO' ORDER BY date")
uo_nulos = uo[uo["valor"].isna()]
ok(len(uo_nulos) == 1 and str(pd.Timestamp(uo_nulos["date"].iloc[0]).date()) == "2025-10-01",
   "a razao UO tem exatamente 1 buraco, em 2025-10 (lapse in appropriations)",
   f"{len(uo_nulos)} nulos em {list(uo_nulos['date'])}")

# ---------------------------------------------------------------- 7. cartoes
secao("7. Cartoes de definicao")

orfas = jolts_tab.orfaos_info(arvs)
ok(not orfas, f"zero chaves orfas no INFO ({len(jolts_tab.INFO)} entradas)", str(orfas[:5]))
redundantes = jolts_tab.full_redundante(arvs)
ok(not redundantes, "nenhum `full` repete o rotulo curto da propria linha",
   str(redundantes[:5]))

# O namespace nao e enfeite: as duas leituras de '00' tem de ser textos DIFERENTES.
t00 = jolts_tab.INFO.get("tamanho:00", {})
r00 = jolts_tab.INFO.get("regiao:00", {})
ok(t00.get("desc") and r00.get("desc") and t00["desc"] != r00["desc"],
   "tamanho:00 e regiao:00 sao entradas distintas (a mesma categoria, dois significados)")
ok("private" in (t00.get("full", "") + t00.get("desc", "")).lower(),
   "  e a de tamanho diz que a raiz e o setor privado")

# Toda medida tem cartao, e toda medida de fluxo tem titulo de eixo para o acumulado.
for m in jolts_tab.ORDEM_MEDIDAS:
    ok(f"medida:{m}" in jolts_tab.INFO, f"medida {m} tem cartao")
for m, cfg in jolts_tab.MEDIDAS.items():
    esperado = cfg["natureza"] == "fluxo"
    ok(bool(cfg["y_acum"]) == esperado,
       f"{m}: y_acum {'presente' if esperado else 'ausente'} (natureza {cfg['natureza']})")
    # `y_share` e obrigatorio nas seis: sem ele o `.replace('{raiz}', ...)` do relatorio
    # estoura e o grafico sai em branco. E o `{raiz}` tem de estar la, ou o eixo deixa de
    # nomear o denominador -- que e o unico jeito de o leitor saber se a participacao e
    # de Total nonfarm, de Total private ou de Total US.
    ok("{raiz}" in (cfg.get("y_share") or ""),
       f"{m}: y_share existe e carrega o placeholder {{raiz}}", repr(cfg.get("y_share")))

# ---------------------------------------------------------------- resumo
print(f"\n{'=' * 66}")
print(f"{_asserts - _falhas}/{_asserts} assercoes ok" + (f", {_falhas} FALHAS" if _falhas else ""))
sys.exit(1 if _falhas else 0)
