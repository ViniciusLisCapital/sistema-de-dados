# -*- coding: utf-8 -*-
"""Testa o F(A) do agente de mercado de trabalho (analytics/agent_system/dados/mercado_trabalho.py).

Roda com:
    uv run python tests/test_dados_mercado_trabalho.py

Script com asserts, nao pytest (mesmo padrao de tests/test_dados_agentes.py). O item 4 le o
banco (so leitura) e grava A e F numa pasta temporaria; nao toca em obsidian/ciclos/. Cada item
erra sem levantar nada se quebrar:

1. a declaracao diverge da lista V.VIII do SISTEMA_AGENTES.md (o agente ganharia ou perderia uma
   tabela calado), ou a secao nao fecha no marcador certo;
2. uma tabela que outro agente tambem declara ganha outra consulta no MESMO arquivo de A (o A do
   ciclo e um so): as sete mt_* contra a politica monetaria, a atividade e a inflacao, a Focus da
   desocupacao contra a atividade, a PTC contra as demais;
3. a PTC volta a dizer "-1 a 1" (a escala e -2 a +2);
4. o F de um ciclo passado nao sai, ou sai sem uma das leituras que o mapa pede (a desocupacao
   aberta em emprego e forca de trabalho; o saldo do CAGED de 12 meses por setor), ou as duas
   tabelas de leitura enxuta saem com a leitura completa;
5. mutantes: tabela a menos na declaracao, tabela a mais, consulta alterada.
"""
from __future__ import annotations

import sys
import tempfile
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from dotenv import load_dotenv  # noqa: E402

load_dotenv(Path(__file__).resolve().parents[1] / ".env")

from analytics.agent_system.dados import __main__ as dados_main  # noqa: E402
from analytics.agent_system.dados import (atividade, fiscal, inflacao, mercado_trabalho,  # noqa: E402
                                          motor)
from analytics.agent_system.dados import politica_monetaria as pm  # noqa: E402

sys.stdout.reconfigure(encoding="utf-8")
falhas = 0
mt = mercado_trabalho


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
grupos = motor.ler_lista(mt.SECAO)
itens = [it for g in grupos for it in g["itens"]]
check("a declaracao bate com a lista V.VIII", not levanta(lambda: motor.conferir(mt.TABELAS, grupos), ""))
check("V.VIII tem 19 tabelas em 6 grupos", (len(itens), len(grupos)) == (19, 6), (len(itens), len(grupos)))
check("a secao nao leva o texto do agente seguinte nem o de antes",
      "cmb_ptax" not in {it["tabela"] for it in itens} and "mt_pnad" in {it["tabela"] for it in itens})
check("so o primeiro grupo e 'Endogeno' (leitura completa)",
      [g["nome"] for g in grupos][0] == "Endógeno" and sum(g["nome"] == "Endógeno" for g in grupos) == 1,
      [g["nome"] for g in grupos])
por_grupo = {g["id"]: [it["tabela"] for it in g["itens"]] for g in grupos}
check("o grupo i tem as sete mt_* e so elas",
      sorted(por_grupo["i"]) == sorted(["mt_pnad", "mt_desocupacao_retro", "mt_caged", "mt_caged_setor",
                                        "mt_pnad_trimestral", "mt_caged_uf", "mt_caged_salario"]), por_grupo["i"])
check("o marcador de fim e um que existe no SISTEMA (a V.IX, do credito)",
      mt.SECAO[1] in motor.SISTEMA.read_text(encoding="utf-8"), mt.SECAO[1])

# 2. consultas: o A do ciclo e um so
corte = pd.Timestamp("2026-10-27")
modulos = {a: __import__(m, fromlist=["TABELAS"]) for a, m in dados_main.AGENTES.items()}
check("conferir_consultas passa sobre os sete e este juntos",
      not levanta(lambda: motor.conferir_consultas({**{a: m.TABELAS for a, m in modulos.items()},
                                                    "mercado_trabalho": mt.TABELAS}), ""))
por_nome = {(t.nome, t.recorte): t for t in mt.TABELAS}
for nome in ("mt_pnad", "mt_desocupacao_retro", "mt_caged", "mt_caged_setor"):
    t_pm = next(t for t in pm.TABELAS if t.nome == nome)
    t_mt = por_nome[(nome, None)]
    check(f"{nome}: mesmo arquivo de A e mesma consulta que a politica monetaria",
          t_mt.arquivo == t_pm.arquivo and motor._sql(t_mt, corte) == motor._sql(t_pm, corte), t_mt.arquivo)
for nome, dono in (("atv_ibcbr", atividade), ("atv_pim", atividade), ("atv_pmc", atividade),
                   ("atv_pms", atividade), ("atv_pib", pm), ("atv_pib_taxas", pm), ("pm_hiato_produto", pm),
                   ("inflc_agregados", inflacao), ("fisc_rtn", fiscal), ("expc_qpc", atividade),
                   ("cred_ptc", pm)):
    t_d = next(t for t in dono.TABELAS if t.nome == nome and t.recorte is None)
    t_m = por_nome[(nome, None)]
    check(f"{nome}: a consulta e a de {dono.__name__.rsplit('.', 1)[1]}",
          t_m.arquivo == t_d.arquivo and motor._sql(t_m, corte) == motor._sql(t_d, corte), t_m.arquivo)
foc = por_nome[("expc_focus_periodo", "desocupação")]
foc_at = next(t for t in atividade.TABELAS if t.nome == "expc_focus_periodo" and t.recorte == "desocupação")
check("a Focus da desocupacao e a mesma consulta e o mesmo arquivo da atividade",
      foc.arquivo == foc_at.arquivo and motor._sql(foc, corte) == motor._sql(foc_at, corte), foc.arquivo)

# 3. a PTC: escala -2 a +2, e so o rotulo mudou
ptc = por_nome[("cred_ptc", None)]
check("a PTC diz -2 a +2, nunca -1 a 1",
      ptc.series and all("−2 a +2" in s.unidade and "−1 a 1" not in s.unidade for s in ptc.series),
      {s.unidade for s in ptc.series})
check("as series da PTC sao as mesmas chaves da politica monetaria (so o rotulo muda)",
      [s.chave for s in ptc.series] == [s.chave for s in next(t for t in pm.TABELAS if t.nome == "cred_ptc").series])

# 4. o F de um ciclo passado, numa pasta temporaria
ciclo = pd.Timestamp("2026-10-27").date()
with tempfile.TemporaryDirectory() as tmp:
    pasta_a = Path(tmp) / "A"
    motor.extrair(mt.TABELAS, pasta_a, pd.Timestamp(ciclo))
    texto = motor.montar_f("mercado_trabalho", ciclo, grupos, mt.TABELAS, mt.COMBINADAS, pasta_a, None, mt.PIB)
check("o F sai e tem o cabecalho do agente", texto.startswith("# F(A) — mercado_trabalho — ciclo 2026-10-27"))
check("o F traz as 19 tabelas",
      all(f"### {t['tabela']}" in texto for t in itens), [t["tabela"] for t in itens if f"### {t['tabela']}" not in texto])
check("o grupo i sai em leitura completa e os de consulta em enxuta",
      "## i. Endógeno (leitura completa)" in texto and "## ii. Endógeno de atividade (leitura enxuta)" in texto)
for chave in ("Taxa de desocupação", "Desalentados", "Subocupação por insuficiência de horas",
              "Desocupação, 18 a 24 anos", "Horas habituais, empregado", "Estoque de emprego formal",
              "Saldo: Comércio", "Saldo: SP", "Saldo: Até 1 SM", "Desocupação dessazonalizada, retropolada",
              "Bolsa Família", "Seguro-desemprego", "Micro, pequenas e médias", "índice, −2 a +2",
              "Valor adicionado", "Serviços subjacentes"):
    check(f"o F traz a serie '{chave}'", chave in texto)
check("a desocupacao aberta em emprego e forca de trabalho sai",
      "### Variação da desocupação: emprego e força de trabalho" in texto and "Efeito do emprego (p.p.)" in texto)
check("o saldo do CAGED de 12 meses por setor sai, com o total",
      "### Saldo do CAGED por setor, 12 meses até" in texto and "**Total**" in texto)
check("nenhuma serie declarada fica 'sem dado no corte'", "Sem dado no corte" not in texto,
      [ln for ln in texto.splitlines() if "Sem dado no corte" in ln])


def bloco(nome):
    i = texto.index(f"### {nome}\n")
    j = texto.find("\n### ", i + 1)
    k = texto.find("\n## ", i + 1)
    fim = min(x for x in (j, k, len(texto)) if x > 0)
    return texto[i:fim]


check("mt_caged_uf e mt_caged_salario saem em leitura enxuta (sem percentil)",
      "Pctl" not in bloco("mt_caged_uf") and "Pctl" not in bloco("mt_caged_salario"))
check("mt_caged_setor e mt_caged saem completas (com percentil)",
      "Pctl" in bloco("mt_caged_setor") and "Pctl" in bloco("mt_caged"))
check("a nota das faixas de salario minimo aparece", "reajustado todo janeiro" in bloco("mt_caged_salario"))

# a decomposicao fecha: efeito do emprego + efeito da forca de trabalho = variacao da taxa
linha = next(ln for ln in texto.split("### Variação da desocupação: emprego e força de trabalho")[1].splitlines()
             if ln.startswith("| 20"))
c = [x.strip() for x in linha.strip("|").split("|")]
check("a decomposicao soma: emprego + forca de trabalho = variacao de 12 meses (arredondamento de 0,01)",
      abs(float(c[3]) + float(c[4]) - float(c[2])) <= 0.011, c)

# 5. mutantes
check("mutante: tabela a menos na declaracao levanta",
      levanta(lambda: motor.conferir([t for t in mt.TABELAS if t.nome != "mt_caged_uf"], grupos), "faltam"))
check("mutante: tabela a mais levanta",
      levanta(lambda: motor.conferir(mt.TABELAS + [motor.Tabela("tabela_nova")], grupos), "sobram"))
check("mutante: mt_pnad com outro filtro conflita com a politica monetaria",
      levanta(lambda: motor.conferir_consultas({"pm": pm.TABELAS, "mt": [
          motor.de(pm, "mt_pnad", filtro="region = 'Norte'")]}), "mt_pnad.csv.gz"))

print("")
print(("%d FALHA(S)" % falhas) if falhas else "todos os asserts passaram")
sys.exit(1 if falhas else 0)
