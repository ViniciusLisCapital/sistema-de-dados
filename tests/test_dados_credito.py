# -*- coding: utf-8 -*-
"""Testa o F(A) do agente de credito (analytics/agent_system/dados/credito.py).

Roda com:
    uv run python tests/test_dados_credito.py

Script com asserts, nao pytest (mesmo padrao de tests/test_dados_agentes.py). O item 5 le o
banco (so leitura) e grava A e F numa pasta temporaria; nao toca em obsidian/ciclos/. Cada item
erra sem levantar nada se quebrar:

1. a declaracao diverge da lista V.IX do SISTEMA_AGENTES.md (o agente ganharia ou perderia uma
   tabela calado), ou a secao nao fecha no marcador certo;
2. uma tabela que outro agente tambem declara ganha outra consulta no MESMO arquivo de A (o A do
   ciclo e um so): as 11 cred_* contra a politica monetaria, a atividade e o fiscal; as tabelas
   de consulta contra o dono; ou ganha uma `variante`, que poria dois agentes no mesmo arquivo;
3. a PTC volta a dizer "-1 a 1" (a escala e -2 a +2);
4. a `cred_credito_resumo` perde series (84) ou as modalidades perdem uma metrica;
5. o F de um ciclo passado nao sai, ou sai sem uma das leituras combinadas, ou as identidades
   deixam de fechar (as quatro contribuicoes somam o saldo total; PF + PJ = impulso total), ou
   a fluxo financeiro parada nao aparece com a data, ou as duas tabelas de leitura enxuta saem
   com a leitura completa;
6. mutantes: tabela a menos na declaracao, tabela a mais, consulta alterada, variante.
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
from analytics.agent_system.dados import (atividade, cambio, credito, expectativas, fiscal,  # noqa: E402
                                          inflacao, mercado_trabalho, motor)
from analytics.agent_system.dados import politica_monetaria as pm  # noqa: E402

sys.stdout.reconfigure(encoding="utf-8")
falhas = 0
cr = credito


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
grupos = motor.ler_lista(cr.SECAO)
itens = [it for g in grupos for it in g["itens"]]
nomes = [it["tabela"] for it in itens]
check("a declaracao bate com a lista V.IX", not levanta(lambda: motor.conferir(cr.TABELAS, grupos), ""))
check("V.IX tem 29 itens (28 tabelas) em 8 grupos",
      (len(itens), len(set(nomes)), len(grupos)) == (29, 28, 8), (len(itens), len(set(nomes)), len(grupos)))
check("a secao nao leva o texto de fora da lista", "mt_caged_setor" not in nomes and "cred_ptc" in nomes)
check("so o primeiro grupo e 'Endogeno' (leitura completa)",
      [g["nome"] for g in grupos][0] == "Endógeno" and sum(g["nome"] == "Endógeno" for g in grupos) == 1,
      [g["nome"] for g in grupos])
por_grupo = {g["id"]: [it["tabela"] for it in g["itens"]] for g in grupos}
check("o grupo i tem as 14 cred_* e so elas",
      len(por_grupo["i"]) == 14 and all(n.startswith("cred_") for n in por_grupo["i"]), por_grupo["i"])
check("a Focus aparece duas vezes na lista, uma por recorte (Selic, IPCA)",
      sorted(it["recorte"] for it in itens if it["tabela"] == "expc_focus_periodo") == ["IPCA", "Selic"])
check("o marcador de fim existe no SISTEMA", cr.SECAO[1] in motor.SISTEMA.read_text(encoding="utf-8"), cr.SECAO[1])

# 2. consultas: o A do ciclo e um so
corte = pd.Timestamp("2026-10-27")
modulos = {a: __import__(m, fromlist=["TABELAS"]) for a, m in dados_main.AGENTES.items()}
todos = {**{a: m.TABELAS for a, m in modulos.items()}, "mercado_trabalho": mercado_trabalho.TABELAS,
         "credito": cr.TABELAS}
check("conferir_consultas passa sobre os agentes registrados, o de mercado de trabalho e este",
      not levanta(lambda: motor.conferir_consultas(todos), ""))
por_nome = {(t.nome, t.recorte): t for t in cr.TABELAS}
check("nenhuma tabela do credito leva `variante` (dois agentes no mesmo arquivo de A)",
      all(t.variante is None for t in cr.TABELAS), [t.arquivo for t in cr.TABELAS if t.variante])


def mesma(t_c, t_d, rotulo):
    check(f"{rotulo}: mesmo arquivo de A e mesma consulta",
          t_c.arquivo == t_d.arquivo and motor._sql(t_c, corte) == motor._sql(t_d, corte), t_c.arquivo)


# as cred_* ja declaradas: mesma consulta que a politica monetaria, a atividade e o fiscal
for nome in (n for n in por_grupo["i"] if n not in ("cred_credito_porte", "cred_credito_atividade_economica",
                                                  "cred_credito_tipo_cliente")):
    for dono in (pm, atividade, fiscal):
        t_d = next((t for t in dono.TABELAS if t.nome == nome), None)
        if t_d is not None:
            mesma(por_nome[(nome, None)], t_d, f"{nome} contra {dono.__name__.rsplit('.', 1)[1]}")
# as tres que ninguem declara
for nome in ("cred_credito_porte", "cred_credito_atividade_economica", "cred_credito_tipo_cliente"):
    check(f"{nome}: nenhum outro agente declara", all(t.nome != nome for m in modulos.values() for t in m.TABELAS))
# as de consulta: a consulta do dono
dono_de = (("pm_copom_reuniao", pm), ("br_interest_rate", pm), ("pm_hiato_produto", pm), ("atv_pib_mensal", pm),
           ("atv_pib", pm), ("atv_pmc", pm), ("atv_pim_uso", pm), ("inflc_agregados", inflacao),
           ("mt_pnad", mercado_trabalho), ("mt_caged", mercado_trabalho), ("fisc_dlsp_fatores", fiscal),
           ("fisc_rtn", fiscal), ("cmb_ptax", cambio))
for nome, dono in dono_de:
    t_d = next(t for t in dono.TABELAS if t.nome == nome and t.recorte is None)
    mesma(por_nome[(nome, None)], t_d, f"{nome} contra {dono.__name__.rsplit('.', 1)[1]}")
mesma(por_nome[("expc_focus_periodo", "Selic")],
      next(t for t in expectativas.TABELAS if t.nome == "expc_focus_periodo" and t.recorte == "Selic"),
      "a Focus da Selic contra a de expectativas")
mesma(por_nome[("expc_focus_periodo", "IPCA")],
      next(t for t in cambio.TABELAS if t.nome == "expc_focus_periodo" and t.recorte == "IPCA"),
      "a Focus do IPCA contra a do cambio")
check("a fisc_rtn e so as equalizacoes e subsidios ao credito (nenhum agregado fiscal)",
      all(se.chave in dict(cr._RTN) for se in por_nome[("fisc_rtn", None)].series)
      and not any(se.chave in ("receita_liquida", "despesa_total") for se in por_nome[("fisc_rtn", None)].series))
check("as series de consulta sao so as que a lista nomeia (mt_pnad: ocupacao, informalidade, rendimento, massa)",
      [s.chave for s in por_nome[("mt_pnad", None)].series]
      == ["ocupado", "taxa_informalidade", "rend_habitual_real_todos_trabalhos", "massa_real_habitual"])

# 3. a PTC: escala -2 a +2, e so o rotulo mudou
ptc = por_nome[("cred_ptc", None)]
check("a PTC diz -2 a +2, nunca -1 a 1",
      ptc.series and all("−2 a +2" in s.unidade and "−1 a 1" not in s.unidade for s in ptc.series),
      {s.unidade for s in ptc.series})
chaves_pm = [s.chave for s in next(t for t in pm.TABELAS if t.nome == "cred_ptc").series]
check("a PTC traz as series da politica monetaria (observada) e mais as esperadas",
      set(chaves_pm) <= {s.chave for s in ptc.series} and len(ptc.series) == 16, len(ptc.series))

# 4. series declaradas
check("a cred_credito_resumo declara as 84 series, sem repeticao",
      len(cr._RESUMO) == 84 and len({s.chave for s in cr._RESUMO}) == 84, len(cr._RESUMO))
check("a cred_credito_atividade_economica declara as 38 series",
      len(por_nome[("cred_credito_atividade_economica", None)].series) == 38)
check("a cred_credito_amplo declara as 17 series", len(por_nome[("cred_credito_amplo", None)].series) == 17)
check("as modalidades pedem saldo, concessao, taxa e inadimplencia (cartao a vista: so saldo e concessao)",
      all({s.chave.split("|")[1] for s in cr._LIVRE_PF if s.chave.startswith(m)} == {"saldo", "concessao"}
          for m in ("cartao_de_credito_a_vista",))
      and {s.chave.split("|")[1] for s in cr._LIVRE_PF if s.chave.startswith("cheque_especial")}
      == {"saldo", "concessao", "taxa_media", "inadimplencia"})
check("a fluxo financeira tem F proprio (para dizer ate quando vai)",
      por_nome[("cred_fluxo_financeiro", None)].especial is cr.fluxo_financeiro)

# 5. o F de um ciclo passado, numa pasta temporaria
ciclo = pd.Timestamp("2026-10-27").date()
with tempfile.TemporaryDirectory() as tmp:
    pasta_a = Path(tmp) / "A"
    motor.extrair(cr.TABELAS, pasta_a, pd.Timestamp(ciclo))
    texto = motor.montar_f("credito", ciclo, grupos, cr.TABELAS, cr.COMBINADAS, pasta_a, None, cr.PIB)
    # os numeros brutos das identidades, lidos de A
    ctx = motor.Ctx(corte=pd.Timestamp(ciclo), anterior=None, pasta_a=pasta_a, tabelas=cr.TABELAS)
    tot = ctx.serie("cred_credito_resumo", "saldo_total_total")
    blocos = [ctx.serie("cred_credito_resumo", k) for k, _ in cr._BLOCOS]
    ult_fluxo = ctx.serie("cred_fluxo_financeiro", "fluxo_total").index[-1]
check("o F sai e tem o cabecalho do agente", texto.startswith("# F(A) — credito — ciclo 2026-10-27"))
check("o F traz as 28 tabelas (a Focus nos dois recortes)",
      all(f"### {it['tabela']}" in texto for it in itens),
      [it["tabela"] for it in itens if f"### {it['tabela']}" not in texto])
check("o F traz expc_focus_periodo (Selic) e (IPCA)",
      "### expc_focus_periodo (Selic)" in texto and "### expc_focus_periodo (IPCA)" in texto)
check("o grupo i sai em leitura completa e os de consulta em enxuta",
      "## i. Endógeno (leitura completa)" in texto and "## ii. Endógeno de política monetária (leitura enxuta)" in texto)
for chave in ("Saldo: livre PF", "Spread: livre, não rotativo PJ", "Custo do crédito (ICC): direcionado PJ",
              "Consignado INSS: saldo", "Cartão rotativo: inadimplência", "Capital de giro: taxa", "ACC: concessões",
              "BNDES, investimento: saldo", "Programas para MPME: saldo", "Saldo: bancos públicos",
              "Provisões: bancos públicos", "Saldo: MPME", "Saldo de maior risco desde 2025-01",
              "Indústria: bens de capital", "Serviços: comércio", "Setor público: estados e municípios",
              "Empresas: dívida externa, mercado externo", "Grandes empresas: oferta, esperada",
              "índice, −2 a +2", "Fluxo financeiro, PF", "Endividamento das famílias",
              "Comprometimento de renda: só juros", "Atraso PJ de 15 a 90 dias", "Selic (variável da política",
              "Selic, meta", "DI × pré", "PTAX venda", "Ocupados", "Estoque de emprego formal", "IPCA",
              "Bens de capital", "Equalização de custeio agropecuário", "Impacto primário do FIES",
              "Créditos do Tesouro às instituições financeiras oficiais"):
    check(f"o F traz '{chave}'", chave in texto)
check("nenhuma serie declarada fica 'sem dado no corte'", "Sem dado no corte" not in texto,
      [ln for ln in texto.splitlines() if "Sem dado no corte" in ln])
for tit in ("### O impulso de crédito pelo estoque", "### O impulso de crédito no conceito do BC",
            "### As concessões em termos reais", "### Quem puxa o crescimento do saldo de crédito",
            "### PTC: o observado contra o esperado"):
    check(f"a leitura combinada '{tit[4:]}' sai", tit in texto)


def bloco(nome):
    i = texto.index(f"### {nome}\n")
    j = texto.find("\n### ", i + 1)
    k = texto.find("\n## ", i + 1)
    fim = min(x for x in (j, k, len(texto)) if x > 0)
    return texto[i:fim]


check("atividade_economica e tipo_cliente saem em leitura enxuta (sem percentil)",
      "Pctl" not in bloco("cred_credito_atividade_economica") and "Pctl" not in bloco("cred_credito_tipo_cliente"))
check("resumo, modalidades e porte saem completas (com percentil)",
      all("Pctl" in bloco(n) for n in ("cred_credito_resumo", "cred_modalidade_livre_pf", "cred_credito_porte")))
check("a nota da quebra do saldo de maior risco aparece", "Res. CMN 4.966" in bloco("cred_credito_porte"))
check("a nota de que a base ampla nao reconcilia aparece", "não reconciliam" in bloco("cred_credito_amplo"))
bl_flux = bloco("cred_fluxo_financeiro")
check("a fluxo financeira parada mostra a data do ultimo dado e diz que parou",
      f"Último dado da série: {ult_fluxo:%Y-%m}" in bl_flux and "Série parada" in bl_flux, ult_fluxo)
check("o impulso do BC diz que a serie esta parada na mesma data",
      f"parada em {ult_fluxo:%Y-%m}" in texto.split("### O impulso de crédito no conceito do BC")[1])


def tabela_de(titulo):
    sec = texto.split(titulo)[1].split("\n### ")[0].split("\n## ")[0]
    return [[x.strip() for x in ln.strip("|").split("|")] for ln in sec.splitlines() if ln.startswith("| 20")]


# identidade 1: as quatro contribuicoes somam o crescimento do saldo total
linhas = tabela_de("### Quem puxa o crescimento do saldo de crédito")
check("a decomposicao tem 6 meses", len(linhas) == 6, len(linhas))
ok = all(abs(sum(float(c) for c in r[2:6]) - float(r[1])) <= 0.025 and abs(float(r[7])) <= 0.025 for r in linhas)
check("as quatro contribuicoes somam o crescimento de 12 meses do saldo total (arredondamento de 0,01)", ok, linhas[:2])
t1 = tot.index[-1]
g = (tot.iloc[-1] / tot[motor.antes(t1, 12)] - 1) * 100
check("o crescimento do total impresso e o do A", abs(float(linhas[0][1]) - g) <= 0.006, (linhas[0][1], g))
check("o saldo total e a soma dos quatro blocos no A (a identidade que a decomposicao usa)",
      abs(float(sum(s.iloc[-1] for s in blocos)) - tot.iloc[-1]) <= 4, (sum(s.iloc[-1] for s in blocos), tot.iloc[-1]))
# identidade 2: PF + PJ = impulso total
linhas = tabela_de("### O impulso de crédito pelo estoque")
check("o impulso pelo estoque tem 6 meses", len(linhas) == 6, len(linhas))
check("PF + PJ = impulso total (arredondamento de 0,01)",
      all(abs(float(r[2]) + float(r[3]) - float(r[1])) <= 0.015 for r in linhas), linhas[:2])
check("o impulso e uma fracao do PIB (|p.p.| < 15), nao uma escala errada",
      all(abs(float(r[1])) < 15 and abs(float(r[4])) < 30 for r in linhas), linhas[:1])
# impulso do BC: fluxo(t) - fluxo(t-12)
linhas = tabela_de("### O impulso de crédito no conceito do BC")
check("o impulso do BC termina na data do ultimo dado da fluxo e tem 6 meses",
      len(linhas) == 6 and linhas[0][0] == f"{ult_fluxo:%Y-%m}", linhas[:1])
# concessoes reais
sec = texto.split("### As concessões em termos reais")[1].split("\n### ")[0].split("\n## ")[0]
check("as concessoes reais trazem os cinco cortes, real e nominal",
      all(f"| {c} |" in sec for c in ("Total", "Livre", "Direcionado", "PF", "PJ")) and "Δ% real" in sec
      and "Δ% nominal" in sec)
linhas = tabela_de("### As concessões em termos reais")
check("a variacao real nao e igual a nominal (o deflator entra)",
      any(abs(float(r[1]) - float(r[2])) > 0.0 for r in linhas if r[1] != "—" and r[2] != "—"), linhas[:2])
check("a surpresa da PTC cobre os 4 segmentos nos dois lados (8 linhas)",
      sum(1 for ln in texto.split("### PTC: o observado contra o esperado")[1].splitlines() if ln.startswith("| ")
          and "Segmento" not in ln) == 8)

# 6. mutantes
check("mutante: tabela a menos na declaracao levanta",
      levanta(lambda: motor.conferir([t for t in cr.TABELAS if t.nome != "cred_credito_porte"], grupos), "faltam"))
check("mutante: a Focus de um recorte a menos levanta",
      levanta(lambda: motor.conferir([t for t in cr.TABELAS if t.recorte != "IPCA"], grupos), "faltam"))
check("mutante: tabela a mais levanta",
      levanta(lambda: motor.conferir(cr.TABELAS + [motor.Tabela("tabela_nova")], grupos), "sobram"))
check("mutante: cred_credito_resumo com outro filtro conflita com a politica monetaria",
      levanta(lambda: motor.conferir_consultas({"pm": pm.TABELAS, "cr": [
          motor.de(pm, "cred_credito_resumo", filtro="name LIKE 'saldo%%'")]}), "cred_credito_resumo.csv.gz"))
check("mutante: cred_ptc com o corte numa coluna de outra data conflita com a atividade",
      levanta(lambda: motor.conferir_consultas({"at": atividade.TABELAS, "cr": [
          motor.de(pm, "cred_ptc", corte=None)]}), "cred_ptc.csv.gz"))
check("mutante: a Focus da Selic com variante vira outro arquivo de A (nao conflita, mas duplicaria o A)",
      motor.de(expectativas, "expc_focus_periodo", recorte="Selic", variante="credito").arquivo
      != por_nome[("expc_focus_periodo", "Selic")].arquivo)
check("mutante: a PTC rotulada -1 a 1 e pega pelo teste da escala",
      not all("−2 a +2" in s.unidade for s in motor.de(pm, "cred_ptc").series))

print("")
print(("%d FALHA(S)" % falhas) if falhas else "todos os asserts passaram")
sys.exit(1 if falhas else 0)
