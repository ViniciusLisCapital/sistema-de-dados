# -*- coding: utf-8 -*-
"""Testa o caminho trimestral de cada edicao do RPM (analytics/brasil/monetary_policy/projecao_rpm.py).

Roda com:
    uv run python tests/test_projecao_rpm.py              # ~2 min: baixa o anexo de cada edicao
    uv run python tests/test_projecao_rpm.py --sem-rede   # so as secoes 1 e 2, contra o banco

Script com asserts, nao pytest (mesmo padrao de tests/test_condicionais.py). Le o banco. O que o
grafico e a prosa fazem com o payload e a secao 37 de tests/test_monetary_policy_js.js.

Nasceu de uma decisao, nao de um bug: o pedido foi consumir a tabela 2.2.1 do ANEXO ESTATISTICO
do RPM, e o mesmo numero ja estava no banco, lido do texto do relatorio desde 1999. A secao 3 e o
que sustenta nao duplicar o dado -- ela compara, celula a celula, as duas fontes nas edicoes que
tem as duas. Um parser de PDF tem cinco armadilhas silenciosas documentadas
(domain/db/brasil/bcb/relatorio_politica_monetaria.md), e a planilha e a conferencia independente
que a propria fonte oferece.

1. o payload: edicoes contiguas, comecando no trimestre em que sairam, o horizonte relevante seis
   trimestres a frente, livres e administrados so desde set/2024, as tres edicoes so com juros constantes;
2. o realizado e o que o SGS publica -- o IPCA pela serie acumulada, livres e administrados
   compostos das variacoes mensais com 12 meses completos;
3. contra o anexo: toda celula de projecao que as duas fontes tem e IGUAL, e o realizado bate com
   os "efetivos" que o anexo imprime na primeira casa.
"""
from __future__ import annotations

import sys
import warnings

import numpy as np
import pandas as pd

from analytics.brasil.monetary_policy import projecao_rpm as pr
from analytics.brasil.monetary_policy.dados import q

warnings.filterwarnings("ignore")
falhas = 0


def check(nome, cond, detalhe=""):
    global falhas
    if cond:
        print("  ok     " + nome)
    else:
        falhas += 1
        print("  FALHA  " + nome + (("  -- " + str(detalhe)) if detalhe else ""))


def tri(iso) -> int:
    t = pd.Timestamp(iso)
    return t.year * 4 + (t.month - 1) // 3


M = pr.montar()
E = M["edicoes"]

print("1. o payload")
check("uma edicao por trimestre de publicacao desde 1999", len(E) > 100 and E[0]["vintage"] < "2000-01-01",
      f"{len(E)} desde {E[0]['vintage'] if E else '-'}")
check("em ordem e sem duas edicoes da mesma reuniao",
      all(E[i - 1]["vintage"] < E[i]["vintage"] for i in range(1, len(E)))
      and len({e["nro"] for e in E}) == len(E))
contig = all(all(tri(s["dates"][i]) - tri(s["dates"][i - 1]) == 1 for i in range(1, len(s["dates"])))
             for e in E for s in e["series"].values())
check("todo caminho e contiguo", contig)
inicio = [tri(s["dates"][0]) - tri(e["vintage"]) for e in E for s in e["series"].values()]
check("e comeca no trimestre da edicao (so a de set/1999 comeca no seguinte)",
      all(x in (0, 1) for x in inicio) and inicio.count(1) == 1, sorted(set(inicio)))
hr = [e for e in E if e["hr"]]
check("o horizonte relevante e seis trimestres a frente da edicao",
      len(hr) > 80 and all(tri(e["hr"]) - tri(e["vintage"]) == 6 for e in hr), len(hr))
liv = [e for e in E if "ipca_livres" in e["series"]]
check("livres e administrados trimestrais desde set/2024, e em toda edicao dali em diante",
      liv and liv[0]["vintage"] == "2024-09-26" and len(liv) == len(E) - E.index(liv[0])
      and all("ipca_administrados" in e["series"] for e in liv), liv[0]["vintage"] if liv else "-")
cte = [e["vintage"] for e in E if e["cenario"] == "juros_constante"]
check("as tres edicoes que so publicaram juros constantes entram com ele, marcadas e listadas",
      M["sem_cenario"] == ["2002-03-28", "2002-12-30", "2003-03-31"] == cte
      and all(e["cenario"] == "juros_esperado" for e in E if e["vintage"] not in cte), (M["sem_cenario"], cte))

print("2. o realizado")
bruto = q("macro_brasil", "SELECT date, name, value FROM inflc_agregados "
                          "WHERE name IN ('ipca_12m', 'ipca_livres', 'ipca_administrado')")
bruto["date"] = pd.to_datetime(bruto["date"])
bruto["value"] = pd.to_numeric(bruto["value"])
w = bruto.pivot(index="date", columns="name", values="value").sort_index()
R = M["realizado"]
# O trimestre datado no 1o mes e o acumulado em 12 meses do ULTIMO mes dele.
dif = max(abs(v - w.loc[pd.Timestamp(d) + pd.DateOffset(months=2), "ipca_12m"])
          for d, v in zip(R["ipca"]["dates"], R["ipca"]["values"]))
check("o IPCA realizado e a serie acumulada publicada, no ultimo mes do trimestre", dif < 1e-3, dif)
d0 = R["ipca_livres"]["dates"][-1]
fim = pd.Timestamp(d0) + pd.DateOffset(months=2)
janela = w.loc[fim - pd.DateOffset(months=11):fim, "ipca_livres"]
manual = (np.prod(1 + janela.values / 100) - 1) * 100
check("livres: composto dos 12 meses ate o fim do trimestre", len(janela) == 12
      and abs(manual - R["ipca_livres"]["values"][-1]) < 1e-3, (manual, R["ipca_livres"]["values"][-1]))
check("o realizado comeca no primeiro trimestre projetado e nao tem buraco",
      all(R[i]["dates"][0] == min(s["dates"][0] for e in E for s in e["series"].values()) for i in R)
      and all(tri(R["ipca"]["dates"][k]) - tri(R["ipca"]["dates"][k - 1]) == 1 for k in range(1, len(R["ipca"]["dates"]))))

if "--sem-rede" in sys.argv:
    print("\n3. contra o anexo estatistico -- pulada (--sem-rede)")
else:
    from connectors.bcb_rpm import AnexoRPM, normalizar

    print("3. contra o anexo estatistico")
    ROM = {"I": 1, "II": 2, "III": 3, "IV": 4}
    IDX = {"ipca": "ipca", "ipca livres": "ipca_livres", "ipca administrados": "ipca_administrados"}

    def ler(grade) -> list[tuple[str, int, int, float]]:
        """(indice, ano, trimestre, valor) da Tab 2.2.1, nos dois formatos que ela ja teve."""
        g, out = grade, []
        for i in range(len(g)):
            # Ate jun/2024: linhas Ano | Trim. | Meta | RI anterior | RI da edicao | Diferenca. A
            # coluna da edicao e a ULTIMA "RI de"/"RPM de". Em mar/2022 ha dois cenarios com a
            # Selic da Focus (Cen. A e Cen. B, uma linha de subtitulo abaixo); a coluna "RI de
            # marco" e o A, que e o que o texto do relatorio usa -- ver o docstring de projecao_rpm.
            if str(g.iat[i, 0]).strip() == "Ano" and str(g.iat[i, 1]).strip().startswith("Trim"):
                cab = [str(c).strip() if c is not None else "" for c in g.iloc[i]]
                col = max(j for j, c in enumerate(cab) if c.startswith(("RI de", "RPM de")))
                for k in range(i + 1, len(g)):
                    a, t = g.iat[k, 0], g.iat[k, 1]
                    if a is None and k == i + 1:
                        continue                       # a linha "Cen. A | Cen. B"
                    try:
                        ano = int(float(a))
                    except (TypeError, ValueError):
                        break
                    v = g.iat[k, col]
                    if v not in (None, ""):
                        out.append(("ipca", ano, ROM[str(t).strip()], float(v)))
                return out
            # De set/2024: linha de anos, linha de trimestres romanos, uma linha por indice.
            if str(g.iat[i, 0]).strip().startswith("Índice de preços"):
                ano, cols = None, []
                for j in range(1, g.shape[1]):
                    a = g.iat[i - 1, j]
                    if a is not None and str(a).strip().isdigit():
                        ano = int(a)
                    t = g.iat[i, j]
                    if t is not None and str(t).strip() in ROM:
                        cols.append((j, ano, ROM[str(t).strip()]))
                for k in range(i + 1, len(g)):
                    nome = normalizar(g.iat[k, 0] or "")
                    if nome in IDX:
                        for j, a, t in cols:
                            v = g.iat[k, j]
                            if v is not None and str(v).strip() not in ("", "-"):
                                out.append((IDX[nome], a, t, float(v)))
                return out
        raise RuntimeError("Tab 2.2.1 num formato que este teste nao conhece")

    anexo = AnexoRPM()
    ed_por_mes = {e["vintage"][:7]: e for e in E}
    comuns = iguais = so_anexo = 0
    difs, efet, efet_ok, sem_ed = [], 0, 0, []
    for v in anexo.vintages_disponiveis():
        ws, _ = anexo.localizar_aba(anexo.abrir(v), r"^tabela 2\.2\.1 .*projecoes de inflacao")
        e = ed_por_mes.get(f"{v:%Y-%m}")
        if e is None:
            sem_ed.append(f"{v:%Y-%m}")
            continue
        for ind, ano, t, val in ler(anexo.grade(ws)):
            d = f"{ano}-{3 * (t - 1) + 1:02d}-01"
            if tri(d) < tri(e["vintage"]):
                # Trimestre ja fechado: o "efetivo" da tabela contra o realizado daqui.
                r = R[ind]["dates"].index(d) if d in R[ind]["dates"] else None
                if r is not None:
                    efet += 1
                    # Meio para cima, como o BC arredonda: o round() do Python e para o par e
                    # ainda erra pela representacao binaria (5,35 -> 5,3), e isso reprovava os
                    # quatro 2025T2 do IPCA, que a tabela imprime 5,4.
                    bate = abs(np.floor(R[ind]["values"][r] * 10 + 0.5 + 1e-9) / 10 - val) < 1e-9
                    efet_ok += bate
                    if not bate and "-v" in sys.argv:
                        print("       efetivo", f"{v:%Y-%m}", ind, d, val, R[ind]["values"][r])
                continue
            s = e["series"].get(ind)
            if s is None or d not in s["dates"]:
                so_anexo += 1
                continue
            comuns += 1
            x = s["values"][s["dates"].index(d)]
            if abs(x - val) < 1e-9:
                iguais += 1
            else:
                difs.append((f"{v:%Y-%m}", ind, d, val, x))
    print(f"         {comuns} celulas de projecao nas duas fontes, {so_anexo} so no anexo, "
          f"{efet} efetivos conferidos")
    check("toda edicao do anexo tem a mesma edicao no banco", not sem_ed, sem_ed)
    check("as celulas de projecao que as duas fontes tem sao IGUAIS", comuns > 350 and iguais == comuns,
          f"{iguais}/{comuns}; {difs[:4]}")
    # Medido em 2026-09-25: 1, o 2026T1 da edicao de dez/2022, que o texto nao traz.
    check("e o anexo tem no maximo um punhado de celulas que o texto nao tem", so_anexo <= 2, so_anexo)
    # 95 de 96 em 2026-09-25: administrados de 2026T1 sai 5,44 aqui e 5,5 la, porque as variacoes
    # mensais do SGS vem com duas casas e o BC compoe as dele sem esse arredondamento.
    check("o realizado bate com os efetivos que o anexo imprime, na primeira casa",
          efet >= 90 and efet - efet_ok <= 2, f"{efet_ok}/{efet}")

print("")
print(("%d FALHA(S)" % falhas) if falhas else "todos os asserts passaram")
sys.exit(1 if falhas else 0)
