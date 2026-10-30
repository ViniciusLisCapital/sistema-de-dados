# -*- coding: utf-8 -*-
"""Testa a forma das definicoes dos agentes-analistas (.claude/agents/<area>-analyst.md) e do web.

Roda com:
    uv run python tests/test_definicoes_agentes.py

Script com checks, nao pytest (mesmo padrao de tests/test_consolidacao.py). So le texto: nao toca no
banco nem em nada do ciclo. As definicoes foram reescritas em 2026-10-30 para o ciclo sem rodadas
(SISTEMA_AGENTES.md III.III.viii; coordenacao/A_ciclo.md, "A3 -> E"). O teste existe para que uma
definicao nao volte calada ao fluxo antigo e para que os agentes novos sigam o mesmo esqueleto.
Cada item acusa:

1. um agente de consolidacao.AGENTES sem arquivo, ou com `name:` diferente do nome do arquivo;
2. a `description` do frontmatter falando em "rodada" ou "report final";
3. um titulo obrigatorio faltando (casado pelo prefixo, porque alguns levam parenteses);
4. um dos quatro modos (r1, r1-final, conversa, atualizacao) faltando;
5. o arquivo de caminhos sem o proprio caminhos/<agente>_r1.json, sem "caudas" ou sem "rodada": "r1";
6. marcador do modelo novo faltando (O que derrubaria a tese, secao 7 Mudancas, Como subordinado /
   principal, Pedido ao web: / Abri:, demanda_d, relatorio.md do ciclo anterior);
7. padrao do fluxo antigo (rodada=, rodada 1/2, r2, rf.json, P2, demanda_r, pedidos_r, report final),
   com a linha do achado. A unica frase com "rodada 2"/"report final" e "There is no rodada 2 and no
   report final."; <agente>_rf.md e permitido (ciclo anterior a 2026-10-30 le-se assim);
8. a rodada de ruido (saida=r1b) fora de cambio e politica monetaria, ou faltando neles;
9. o bloco "The Selic: the model's, the curve's and the Focus's" fora do cambio, ou faltando nele;
10. o web.md sem modo=demanda d=<n>, pedidos_d<n>.md, demanda_d<n>.md, ou com rodada=/demanda_r/pedidos_r;
11. a skill .claude/skills/ciclo/SKILL.md (se existir) com a lista de agentes escrita a mao em vez
    de lida de AGENTES, sem um modo, comando ou o teto, com o fluxo antigo, ou citando definicao
    que nao existe.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

from analytics.agent_system.consolidacao import AGENTES

sys.stdout.reconfigure(encoding="utf-8")
falhas = 0
RAIZ = Path(__file__).resolve().parent.parent
DEFS = RAIZ / ".claude" / "agents"


def check(nome, cond, extra=""):
    global falhas
    print(("ok    " if cond else "FALHA ") + nome + (f"  [{extra}]" if not cond and extra != "" else ""))
    falhas += 0 if cond else 1


def arquivo(chave):
    return DEFS / (chave.replace("_", "-") + "-analyst.md")


def frontmatter(texto):
    m = re.match(r"---\r?\n(.*?)\r?\n---", texto, re.S)
    return m.group(1) if m else ""


def campo(fm, nome):
    m = re.search(rf"^{nome}:\s*(.*)$", fm, re.M)
    return m.group(1).strip() if m else ""


FRASE_OK = "There is no rodada 2 and no report final."
CABECALHOS = ["## The cycle", "## Arguments", "## What you read", "## Exogenous variables", "## News",
              "## The report", "## The four steps", "## What you return to the caller", "## Never"]
MODOS = ["modo=r1 ", "modo=r1-final", "modo=conversa", "modo=atualizacao"]
PROIBIDOS = [r"rodada=", r"rodada 1", r"from rodada 2", r"rodada 2 on", r"<r1\\?\|r2\\?\|rf>",
             r"_r2\.", r"_rf\.json", r"\bP2\b", r"demanda_r", r"pedidos_r", r"report final", r"rodada 2"]
SELIC = "The Selic: the model's, the curve's and the Focus's"
COM_RUIDO = {"cambio", "politica_monetaria"}

textos = {}
for chave in AGENTES:
    f = arquivo(chave)
    if f.exists():
        textos[chave] = f.read_text(encoding="utf-8")

# 1. quais agentes
for chave in AGENTES:
    f = arquivo(chave)
    check(f"[{chave}] tem arquivo {f.name}", chave in textos)
    if chave in textos:
        nome = campo(frontmatter(textos[chave]), "name")
        check(f"[{chave}] name: do frontmatter == nome do arquivo", nome == f.stem, nome)

for chave, t in textos.items():
    # 2. description
    desc = campo(frontmatter(t), "description").lower()
    check(f"[{chave}] description sem 'rodada' nem 'report final'",
          "rodada" not in desc and "report final" not in desc)

    # 3. titulos
    linhas = t.splitlines()
    faltam = [h for h in CABECALHOS if not any(l.startswith(h) for l in linhas)]
    check(f"[{chave}] titulos obrigatorios", not faltam, "faltam: " + "; ".join(faltam))

    # 4. modos
    faltam = [m for m in MODOS if m not in t]
    check(f"[{chave}] os quatro modos", not faltam, "faltam: " + "; ".join(faltam))

    # 5. arquivo de caminhos
    faltam = [x for x in (f"caminhos/{chave}_r1.json", '"caudas"', '"rodada": "r1"') if x not in t]
    check(f"[{chave}] arquivo de caminhos", not faltam, "faltam: " + "; ".join(faltam))

    # 6. marcadores do modelo novo
    faltam = []
    for rotulo, ok in [
        ("O que derrubaria a tese", "O que derrubaria a tese" in t),
        ("Section 7 + Mudancas", ("Section 7" in t or "section 7" in t) and "Mudanças" in t),
        ("Como subordinado", "Como subordinado" in t),
        ("Como principal", "Como principal" in t),
        ("Pedido ao web:", "Pedido ao web:" in t),
        ("Abri:", "Abri:" in t),
        ("demanda_d", "demanda_d" in t),
        ("relatorio.md", "relatorio.md" in t),
    ]:
        if not ok:
            faltam.append(rotulo)
    check(f"[{chave}] marcadores do modelo novo", not faltam, "faltam: " + "; ".join(faltam))

    # 7. padroes do fluxo antigo
    achados = []
    for i, l in enumerate(linhas, 1):
        limpa = l.replace(FRASE_OK, "")
        hit = [p for p in PROIBIDOS if re.search(p, limpa, re.I)]
        if hit:
            achados.append(f"l.{i} " + ",".join(hit[:2]))
    check(f"[{chave}] sem padrao do fluxo antigo", not achados, "; ".join(achados))

    # 8. rodada de ruido
    tem = "saida=r1b" in t
    check(f"[{chave}] saida=r1b " + ("presente" if chave in COM_RUIDO else "ausente"),
          tem == (chave in COM_RUIDO))

    # 9. bloco da Selic
    tem = SELIC in t
    check(f"[{chave}] bloco da Selic " + ("presente" if chave == "cambio" else "ausente"),
          tem == (chave == "cambio"))

# 10. o web
web = DEFS / "web.md"
check("web.md existe", web.exists())
if web.exists():
    t = web.read_text(encoding="utf-8")
    faltam = [x for x in ("modo=demanda d=<n>", "pedidos_d<n>.md", "demanda_d<n>.md") if x not in t]
    check("[web] modo=demanda, pedidos_d<n>.md, demanda_d<n>.md", not faltam, "faltam: " + "; ".join(faltam))
    achados = [x for x in ("rodada=", "demanda_r", "pedidos_r") if re.search(re.escape(x), t, re.I)]
    check("[web] sem rodada=, demanda_r, pedidos_r", not achados, "; ".join(achados))

# 11. a skill do ciclo
skill = RAIZ / ".claude" / "skills" / "ciclo" / "SKILL.md"
if skill.exists():
    t = skill.read_text(encoding="utf-8")
    # a lista de agentes vem do registro, nunca escrita na skill (cresce com os agentes novos)
    check("[skill ciclo] le os agentes de AGENTES em dados/__main__.py",
          "dados/__main__.py" in t and "AGENTES" in t)
    # os argumentos que a sessao passa a cada agente e os comandos da consolidacao
    chaves = ["modo=r1 ", "modo=r1-final", "modo=conversa", "modo=atualizacao", "saida=r1b",
              "d1", "pauta", "volta", "VOLTA", "PAUSA WEB", "ENCERRADA",
              "modo=demanda d=", "pedidos_d", "demanda_d", "--etapa p1", "--etapa pf",
              "retomada", "10M"]
    faltam = [x for x in chaves if x not in t]
    check("[skill ciclo] modos, comandos e o teto", not faltam, "faltam: " + "; ".join(faltam))
    achados = [x for x in (r"rodada=", r"--rodada", r"\bP2\b", r"demanda_r", r"pedidos_r") if re.search(x, t)]
    check("[skill ciclo] sem o fluxo antigo", not achados, "; ".join(achados))
    # toda definicao citada existe
    citadas = sorted(set(re.findall(r"\.claude/agents/([a-z-]+)\.md", t)))
    sem = [c for c in citadas if not (RAIZ / ".claude" / "agents" / f"{c}.md").exists()]
    check("[skill ciclo] as definicoes citadas existem", citadas and not sem, "; ".join(sem))
else:
    print("pulado  skill ciclo (.claude/skills/ciclo/SKILL.md ainda nao existe)")

print()
print("tudo ok" if falhas == 0 else f"{falhas} falha(s)")
sys.exit(1 if falhas else 0)
