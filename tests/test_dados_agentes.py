# -*- coding: utf-8 -*-
"""Testa o gerador do F(A) dos agentes (analytics/agent_system/dados/).

Roda com:
    uv run python tests/test_dados_agentes.py

Script com asserts, nao pytest (mesmo padrao de tests/test_condicionais.py). Nao toca no banco.
Cada item erra sem levantar nada se quebrar:

1. a declaracao do agente diverge da lista decidida no SISTEMA_AGENTES.md (V) -- o agente
   ganharia ou perderia uma tabela sem o usuario saber;
2. o mes em curso entra numa soma como se estivesse completo;
3. uma serie de eventos (intervencoes) trata mes sem linha como ausencia, nao como zero;
4. a variacao e o percentil saem da janela errada;
5. a curva DI lida nos prazos redondos nao reproduz os vertices publicados;
6. a declaracao de politica monetaria diverge da V.II, ou um item de varias tabelas numa
   linha so ("`a`, `b`, `c`: papel") some da leitura da lista;
7. uma tabela que o cambio tambem le ganha outra consulta no MESMO arquivo de A, que e
   compartilhado no ciclo;
8. uma serie trimestral sai com Δ 1m e Δ 3m iguais (os dois contra o trimestre anterior);
9. uma tabela sem coluna de dimensao (dims=()) quebra o pivot;
10. o recorte do BC refeito dos subitens nao e a media ponderada pelo peso do mes;
11. o ciclo de juros em curso comeca no lugar errado;
12. de()/so() copiam outra coisa que a declaracao do outro agente, ou nao levantam quando
    ela nao existe;
13. dois agentes quaisquer de AGENTES declaram a mesma tabela, no mesmo arquivo de A, com
    consultas diferentes -- um leria o arquivo que o outro pediu;
14. gerar() extrai antes de conferir o conflito, ou deixa o F gravado quando o retrato do
    conhecimento levanta (a rodada seguinte pararia com "ja existe").
15. algum dos sete agentes diverge da propria lista, ha conflito de consulta entre eles, ou sobra
    uma `variante` fora das conhecidas (ou redundante: a mesma consulta em dois arquivos de A).
"""
from __future__ import annotations

import sys

import numpy as np
import pandas as pd

from analytics.agent_system.dados import cambio, motor
from analytics.agent_system.dados import politica_monetaria as pm
from analytics.agent_system.dados.especiais import _taxa

sys.stdout.reconfigure(encoding="utf-8")
falhas = 0


def check(nome, cond, extra=""):
    global falhas
    print(("ok    " if cond else "FALHA ") + nome + (f"  [{extra}]" if not cond and extra != "" else ""))
    falhas += 0 if cond else 1


def levanta(fn, trecho):
    try:
        fn()
    except ValueError as exc:
        return trecho in str(exc)
    return False


# 1. declaracao x lista
grupos = motor.ler_lista(cambio.SECAO)
check("a declaracao do cambio bate com a lista V.I",
      not levanta(lambda: motor.conferir(cambio.TABELAS, grupos), ""))
check("tabela da lista sem declaracao levanta",
      levanta(lambda: motor.conferir([t for t in cambio.TABELAS if t.nome != "cmb_ptax"], grupos), "faltam"))
check("tabela declarada fora da lista levanta",
      levanta(lambda: motor.conferir(cambio.TABELAS + [motor.Tabela("tabela_nova")], grupos), "sobram"))

# 2. mes em curso
s = pd.Series(1.0, index=pd.bdate_range("2026-08-01", "2026-09-25"))
meses, parcial = motor.mensal(s)
check("setembro, que acaba em 25/09, fica fora das somas", meses.index[-1] == pd.Timestamp("2026-08-01"),
      meses.index[-1])
check("e aparece como parcial ate 25/09", parcial is not None and parcial[0] == pd.Timestamp("2026-09-25"))
check("agosto soma os dias uteis dele", meses.iloc[-1] == len(pd.bdate_range("2026-08-01", "2026-08-31")))

# 3. eventos
s = pd.Series([-1.0], index=[pd.Timestamp("2026-08-14")])
meses, parcial = motor.mensal(s, fim=pd.Timestamp("2026-09-30"))
check("mes sem intervencao e zero, ate o fim da tabela", list(meses) == [-1.0, 0.0], list(meses))

# 4. variacao e percentil
idx = pd.date_range("2010-01-01", periods=200, freq="MS")
s = pd.Series(np.arange(1, 201, dtype=float), index=idx)
ctx = motor.Ctx(corte=idx[-1], anterior=None, pasta_a=None, tabelas=[], completo=True)
r = motor._nivel(motor.Serie("x", "x", "u", "pct"), s, ctx, pct=True)
check("Δ% 12m contra o valor de 12 meses antes", r["Δ% 12m"] == f"{(200 / 188 - 1) * 100:+.1f}", r["Δ% 12m"])
check("o maior valor da historia tem percentil 100", r["Pctl hist."] == "100", r["Pctl hist."])
r = motor._nivel(motor.Serie("x", "x", "u", "dif"), s, ctx, pct=False)
check("Δ 3m em unidade da serie", r["Δ 3m"] == "+3.00", r["Δ 3m"])

# 5. curva
du, tx = np.array([21.0, 252.0, 504.0]), np.array([13.0, 12.5, 12.0])
check("a curva reproduz os vertices", all(abs(_taxa(du, tx, int(d)) - t) < 1e-9 for d, t in zip(du, tx)))
check("prazo alem do ultimo vertice nao e extrapolado", _taxa(du, tx, 600) is None)

# 6. politica monetaria: a declaracao bate com a V.II
grupos = motor.ler_lista(pm.SECAO)
itens = [it for g in grupos for it in g["itens"]]
check("a declaracao de PM bate com a lista V.II", not levanta(lambda: motor.conferir(pm.TABELAS, grupos), ""))
check("V.II tem 69 entradas em 8 grupos", (len(itens), len(grupos)) == (69, 8), (len(itens), len(grupos)))
# 2026-10-22 (SISTEMA III.III.vii): o hiato passou para a atividade, o TWA virou endogeno do dono
# (fica so o credito) e o CDS saiu de "Exogeno". As tabelas sao as mesmas.
nomes = [g["nome"] for g in grupos]
check("V.II: sem grupo 'Exogeno' e so o credito como TWA",
      not any(n.startswith("Exógeno") for n in nomes)
      and [n for n in nomes if n.startswith("TWA")] == ["TWA — crédito"], nomes)
por_tabela = {it["tabela"]: g["nome"] for g in grupos for it in g["itens"]}
check("V.II: o hiato e o CDS sao consulta (atividade e fiscal)",
      por_tabela["pm_hiato_produto"].startswith("Endógeno de atividade")
      and por_tabela["cmb_risco_pais"].startswith("Endógeno de fiscal"),
      (por_tabela["pm_hiato_produto"], por_tabela["cmb_risco_pais"]))
nomes_fx = [g["nome"] for g in motor.ler_lista(cambio.SECAO)]
check("V.I: sem TWA nem 'Exogeno'",
      not any(n.startswith(("TWA", "Exógeno")) for n in nomes_fx), nomes_fx)
check("o grupo 'Fora da lista' nao entra na secao", not any("Fora" in g["nome"] for g in grupos))
comex = [it for it in itens if it["tabela"].startswith("cmb_comex")]
check("item com tres tabelas numa linha vira tres itens com o mesmo papel",
      len(comex) == 3 and len({it["papel"] for it in comex}) == 1, [it["tabela"] for it in comex])
check("so o grupo 'Endogeno' ganha a leitura completa",
      [g["nome"] for g in grupos if g["nome"] == "Endógeno"] == ["Endógeno"]
      and any(g["nome"].startswith("Endógeno de câmbio") for g in grupos))

# 7. A compartilhado: tabela que os dois leem tem a mesma consulta, ou outro arquivo
corte = pd.Timestamp("2026-10-15")
fx = {t.arquivo: motor._sql(t, corte) for t in cambio.TABELAS}
divergem = [t.arquivo for t in pm.TABELAS if t.arquivo in fx and motor._sql(t, corte) != fx[t.arquivo]]
check("mesma tabela e mesmo arquivo de A => mesma consulta do cambio", not divergem, divergem)
us = next(t for t in pm.TABELAS if t.nome == "us_interest_rate")
check("a curva americana inteira vai para outro arquivo (variante)",
      us.arquivo == "us_interest_rate__curva.csv.gz" and us.arquivo not in fx, us.arquivo)

# 8. serie trimestral: 1t e 4t, nao 1m/3m (que dariam o mesmo trimestre anterior)
idx = pd.date_range("2020-01-01", periods=12, freq="QS")
s = pd.Series(np.arange(100, 112, dtype=float), index=idx)
ctx = motor.Ctx(corte=idx[-1], anterior=None, pasta_a=None, tabelas=[], completo=False)
r = motor._nivel(motor.Serie("x", "x", "u", "dif"), s, ctx, pct=False)
check("trimestral: Δ 1t contra o trimestre anterior", r.get("Δ 1t") == "+1.00", r)
check("trimestral: Δ 4t contra 4 trimestres antes", r.get("Δ 4t") == "+4.00", r)
check("trimestral: sem colunas 1m/3m", "Δ 1m" not in r and "Δ 3m" not in r, list(r))

# 9. tabela sem coluna de dimensao (dims=()) vira uma serie so
t = motor.Tabela("x", dims=())
df = pd.DataFrame({"date": pd.to_datetime(["2026-01-01", "2026-02-01"]), "value": [5.0, 5.2]})
w = motor.largo(df, t)
check("dims=() da uma coluna, com o nome da coluna de valor", list(w.columns) == ["value"], list(w.columns))

# 10. recortes do BC refeitos dos subitens: media ponderada pelo peso do mes
dec = pd.DataFrame({"date": pd.to_datetime(["2026-09-01"] * 3), "subitem_codigo": [1, 2, 3],
                    "var_mensal": [1.0, 3.0, 10.0], "pesos": [0.3, 0.1, 0.6],
                    "contribuicao": [0.003, 0.003, 0.06]})
dim = pd.DataFrame({"subitem_codigo": [1, 2, 3], "subgrupo": ["Serviços", "Serviços", "Monitorados"],
                    "subjacente": ["Serviços Subjacente", None, None]})
cl = pm._por_classe(dec, dim)
check("servicos = (0,3·1 + 0,1·3)/0,4", abs(cl["Serviços"].iloc[-1] - 1.5) < 1e-12, cl["Serviços"].iloc[-1])
check("servicos subjacentes so com o subitem marcado", abs(cl["Serviços subjacentes"].iloc[-1] - 1.0) < 1e-12)

# 11. o ciclo de juros em curso
r = pd.DataFrame({"nro_reuniao": range(1, 8), "date": pd.date_range("2025-01-01", periods=7, freq="45D"),
                  "selic_decidida": [10.0, 10.5, 10.5, 10.25, 10.0, 10.0, 10.0],
                  "variacao_bps": [50, 50, 0, -25, -25, 0, 0]})
txt = pm.copom_decisoes(r, None)[-1]
check("ciclo de corte comeca no primeiro corte depois da ultima alta",
      "corte desde" in txt and "4 reuniões" in txt and "-50 p.b." in txt and "de 10.50%" in txt, txt)
check("e conta as manutencoes no fim", "últimas 2 reuniões mantiveram" in txt, txt)

# 12. de()/so(): a declaracao de outro agente, copiada
t = motor.de(cambio, "cmb_ptax")
check("de() copia a declaracao do outro agente", t == next(x for x in cambio.TABELAS if x.nome == "cmb_ptax"))
t = motor.de(cambio, "expc_focus_periodo", recorte="IPCA", nota="x")
check("de() acha pelo recorte e troca so o pedido",
      t.recorte == "IPCA" and t.nota == "x" and motor._sql(t, corte) == fx[t.arquivo])
t = motor.so(cambio, "cmb_reer", ("MX|real_broad", "BR|real_broad"))
check("so() fica so com as series pedidas, na ordem pedida",
      [s.chave for s in t.series] == ["MX|real_broad", "BR|real_broad"] and motor._sql(t, corte) == fx[t.arquivo])
check("de() de tabela que o outro nao declara levanta",
      levanta(lambda: motor.de(cambio, "tabela_que_nao_existe"), "não declara"))
check("de() com recorte que o outro nao declara levanta",
      levanta(lambda: motor.de(cambio, "expc_focus_periodo", recorte="PIB"), "não declara"))
check("so() com serie que o outro nao declara levanta (em vez de KeyError)",
      levanta(lambda: motor.so(cambio, "cmb_ptax", ("nao_existe",)), "não declara as séries"))

# 13. conflito de consulta entre TODOS os pares de agentes de AGENTES
from analytics.agent_system.dados import __main__ as dados_main  # noqa: E402

check("os agentes registrados nao tem conflito de consulta",
      not levanta(dados_main.conferir_consultas, ""))
a1 = motor.Tabela("tab_x", filtro="name = 'a'")
check("mutante: mesma tabela, mesmo arquivo, outra consulta => levanta",
      levanta(lambda: motor.conferir_consultas({"ag1": [a1], "ag2": [motor.Tabela("tab_x", filtro="name = 'b'")]}),
              "tab_x.csv.gz"))
check("mutante: o conflito aparece mesmo entre o 2o e o 3o agente",
      levanta(lambda: motor.conferir_consultas({"ag1": [motor.Tabela("outra")], "ag2": [a1],
                                                "ag3": [motor.Tabela("tab_x", corte=None)]}), "ag2"))
check("mesma consulta no mesmo arquivo passa",
      not levanta(lambda: motor.conferir_consultas({"ag1": [a1], "ag2": [motor.Tabela("tab_x", filtro="name = 'a'",
                                                                                     series=(motor.Serie("k", "k", "u", "dif"),))]}), ""))
check("outra consulta com `variante` passa (vai para outro arquivo)",
      not levanta(lambda: motor.conferir_consultas({"ag1": [a1], "ag2": [motor.Tabela("tab_x", filtro="name = 'b'",
                                                                                     variante="b")]}), ""))
check("outra consulta em outro recorte passa",
      not levanta(lambda: motor.conferir_consultas({"ag1": [a1], "ag2": [motor.Tabela("tab_x", recorte="r",
                                                                                     filtro="name = 'b'")]}), ""))
check("params diferentes tambem sao outra consulta",
      levanta(lambda: motor.conferir_consultas({"ag1": [motor.Tabela("tab_x", filtro="x = %(v)s", params={"v": 1})],
                                                "ag2": [motor.Tabela("tab_x", filtro="x = %(v)s", params={"v": 2})]}),
              "tab_x"))

# 14. gerar(): o conflito para antes de extrair; o F so e gravado depois do retrato do conhecimento
import datetime as dt  # noqa: E402
import tempfile  # noqa: E402
import types  # noqa: E402
from pathlib import Path  # noqa: E402

from analytics.agent_system import conhecimento, modelo  # noqa: E402

originais = {"CICLOS": motor.CICLOS, "extrair": motor.extrair, "montar_f": motor.montar_f,
             "retratar": modelo.retratar, "gerar": conhecimento.gerar}
extraiu = []
motor.extrair = lambda tabelas, pasta_a, *a, **k: (pasta_a.mkdir(parents=True, exist_ok=True),
                                                   extraiu.append(pasta_a))
motor.montar_f = lambda *a, **k: "# F de teste\n"
modelo.retratar = lambda *a, **k: "(modelo de teste)"
conhecimento.gerar = lambda *a, **k: "(retrato de teste)"   # nunca o de verdade: ele grava no vault
ciclo = dt.date(2026, 9, 20)
try:
    with tempfile.TemporaryDirectory() as tmp:
        motor.CICLOS = Path(tmp)
        f_pm = Path(tmp) / ciclo.isoformat() / "dados" / "F_politica_monetaria.md"

        # um agente falso que le a mesma tabela do cambio com outra consulta, sem variante
        falso = types.ModuleType("_agente_falso_teste")
        falso.TABELAS = [motor.de(cambio, "cmb_ptax", filtro="name = 'ptax_venda'")]
        sys.modules[falso.__name__] = falso
        dados_main.AGENTES["_falso"] = falso.__name__
        try:
            levantou = levanta(lambda: dados_main.gerar("politica_monetaria", ciclo), "cmb_ptax")
        finally:
            del dados_main.AGENTES["_falso"], sys.modules[falso.__name__]
        check("gerar() levanta no conflito com um terceiro agente, antes de extrair",
              levantou and not extraiu and not f_pm.exists())

        def quebra(*a, **k):
            raise RuntimeError("retrato quebrado")
        conhecimento.gerar = quebra
        try:
            dados_main.gerar("politica_monetaria", ciclo)
            quebrou = False
        except RuntimeError:
            quebrou = True
        check("retrato do conhecimento que levanta: o erro sobe e o F nao fica no disco",
              quebrou and extraiu and not f_pm.exists())

        pedidos = []
        conhecimento.gerar = lambda *a, **k: pedidos.append(k) or "(retrato de teste)"
        dados_main.gerar("politica_monetaria", ciclo, sem_literatura=True)
        check("rodar de novo funciona (sem 'ja existe') e grava o F",
              f_pm.exists() and f_pm.read_text(encoding="utf-8") == "# F de teste\n")
        check("--sem-literatura chega ao retrato do conhecimento", pedidos == [{"sem_literatura": True}], pedidos)

        def ja_existe(*a, **k):
            raise FileExistsError("ja existe")
        conhecimento.gerar = ja_existe
        f_pm.unlink()
        dados_main.gerar("politica_monetaria", ciclo)
        check("retrato que ja existe nao impede o F", f_pm.exists())

        conhecimento.gerar = quebra
        try:
            dados_main.gerar("politica_monetaria", ciclo, refazer=True)
        except RuntimeError:
            pass
        check("--refazer que quebra no retrato nao deixa o F antigo, que descrevia o A trocado", not f_pm.exists())
finally:
    for nome in ("CICLOS", "extrair", "montar_f"):
        setattr(motor, nome, originais[nome])
    modelo.retratar, conhecimento.gerar = originais["retratar"], originais["gerar"]

# 15. os sete agentes: cada declaracao bate com a propria lista, nao ha conflito de consulta, e
#     as `variante` que sobraram sao as conhecidas (uma nova obriga a atualizar este teste)
import importlib  # noqa: E402

check("AGENTES tem os sete agentes",
      sorted(dados_main.AGENTES) == sorted(["cambio", "politica_monetaria", "inflacao", "atividade",
                                            "fiscal", "externo", "expectativas"]), sorted(dados_main.AGENTES))
modulos = {a: importlib.import_module(m) for a, m in dados_main.AGENTES.items()}
for agente, mod in modulos.items():
    check(f"{agente}: a declaracao bate com a lista do SISTEMA_AGENTES.md",
          not levanta(lambda mod=mod: motor.conferir(mod.TABELAS, motor.ler_lista(mod.SECAO)), ""))
check("conferir_consultas passa sobre os sete juntos",
      not levanta(lambda: motor.conferir_consultas({a: m.TABELAS for a, m in modulos.items()}), ""))

declaradas = [(a, t) for a, m in modulos.items() for t in m.TABELAS if not t.fora]
com_variante = sorted((a, t.nome, t.recorte, t.variante) for a, t in declaradas if t.variante)
check("variantes que restam: so as sem dono declarando (Focus de componentes, desocupacao e fiscal) "
      "e as duas curvas americanas",
      com_variante == [("atividade", "expc_focus_periodo", "desocupação", "atividade"),
                       ("externo", "us_interest_rate", None, "curva completa"),
                       ("fiscal", "expc_focus_periodo", "fiscal", "fiscal"),
                       ("inflacao", "expc_focus_periodo", "componentes", "inflacao"),
                       ("politica_monetaria", "us_interest_rate", None, "curva")], com_variante)
arquivos = {}
for a, t in declaradas:
    arquivos.setdefault(t.arquivo, set()).add(a)
check("cada variante e de um agente so (dois agentes com a mesma variante dividiriam o arquivo)",
      all(len(arquivos[t.arquivo]) == 1 for _, t in declaradas if t.variante),
      [t.arquivo for _, t in declaradas if t.variante and len(arquivos[t.arquivo]) > 1])
# Variante duplicada: a mesma consulta (nome, recorte, SQL e params) em dois arquivos de A.
por_consulta = {}
for a, t in declaradas:
    por_consulta.setdefault((t.nome, t.recorte, motor._sql(t, corte)[0],
                             tuple(sorted(motor._sql(t, corte)[1].items()))), set()).add(t.arquivo)
check("nenhuma consulta esta em dois arquivos de A (variante redundante)",
      all(len(v) == 1 for v in por_consulta.values()),
      [k[:2] for k, v in por_consulta.items() if len(v) > 1])
# A Focus do PIB e de expectativas (dono): a atividade a le do mesmo arquivo, sem variante.
pib_at = next(t for t in modulos["atividade"].TABELAS if t.nome == "expc_focus_periodo" and t.recorte == "PIB")
pib_ex = next(t for t in modulos["expectativas"].TABELAS if t.nome == "expc_focus_periodo" and t.recorte == "PIB")
check("a Focus do PIB da atividade vem de expectativas: mesmo arquivo de A e mesma consulta",
      pib_at.variante is None and pib_at.arquivo == pib_ex.arquivo == "expc_focus_periodo__pib.csv.gz"
      and motor._sql(pib_at, corte) == motor._sql(pib_ex, corte), pib_at.arquivo)
check("e so o F muda (a funcao de leitura e a da atividade)",
      pib_at.especial is modulos["atividade"].focus_pib and pib_at.especial is not pib_ex.especial)
check("mutante: a mesma Focus do PIB com a consulta da atividade volta a conflitar sem variante",
      levanta(lambda: motor.conferir_consultas({"ex": [pib_ex], "at": [motor.de(modulos["expectativas"],
              "expc_focus_periodo", "PIB", filtro="indicador = 'PIB Total'")]}), "expc_focus_periodo__pib"))

print("")
print(("%d FALHA(S)" % falhas) if falhas else "todos os asserts passaram")
sys.exit(1 if falhas else 0)
