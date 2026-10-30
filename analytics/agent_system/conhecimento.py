"""
Gera o retrato do conhecimento de um agente para um ciclo (PLANO_AGENTES.md 3C).

    uv run python -m analytics.agent_system.conhecimento cambio
    uv run python -m analytics.agent_system.conhecimento cambio --ciclo 2026-10-22
    uv run python -m analytics.agent_system.conhecimento cambio --refazer
    uv run python -m analytics.agent_system.conhecimento cambio --sem-literatura

Roda no início do ciclo, junto com o `dados` (o F(A)). O agente lê só daqui, nunca do vault direto.

O que entra (SISTEMA_AGENTES I.III.xvii, PRINCIPIOS I.VI): o dono e a camada vêm do tracker
(repository/agent_mapping/data_tracker.xlsx), nunca da pasta. Desde 2026-10-29 cada fonte fica na
pasta do dono (repository/ingestion/scripts/owner.py; o tracker.py avisa quando uma sai do lugar), mas
o retrato acha a nota na pasta da aba em que a linha está, seja qual for o dono.
  1. a camada 1 de que o agente é dono: na literatura, síntese + clean_md de cada fonte (abas
     "Qual", colunas Dono e Camada); os modelos mentais da área dele (aba "Mental Models", Camada);
     no agente de política monetária, os documentos do Copom da camada 1 para a data do ciclo
     (tracker.copom_layer: publicados no mandato do presidente atual e antes do ciclo);
  2. as páginas de conceito que linkam algum item de (1). Uma página que não linka nenhum fica fora;
  3. a camada 1 de OUTROS donos que essas páginas linkam, inclusive de donos que ainda não existem.
     Não é transitivo: os conceitos dessas notas não entram por elas;
  4. o mapa conceitual do agente, inteiro.
Nunca a camada 2 ou 3 de ninguém.

Como entra: com o caminho do vault preservado (obsidian/ciclos/<data>/conhecimento/<agente>/
exchange_rate/synthesis/<nome>.md), para os wikilinks resolverem dentro do retrato. Numa página de
conceito ficam só as linhas sem link, as que linkam uma nota do retrato, e as que só linkam
conceitos do retrato; a tabela que ficar sem linha some com o cabeçalho. Em todo arquivo copiado,
menos o mapa, um link para fora do retrato vira texto simples. Assim nenhum wikilink aponta para
fora. INDICE.md (para o agente) e retrato.json (para quem audita o log) listam cada arquivo com o
dono, a camada e por que entrou. É por eles que se sabe quando o agente leu material de outro dono.

Sem literatura (`--sem-literatura`, o primeiro ciclo conjunto dos sete agentes): só o mapa
conceitual e, no agente de política monetária, os documentos do Copom da camada 1, pela mesma regra
de data. Nenhuma síntese, clean_md, página de conceito ou modelo mental, e o tracker nem é lido. O
mapa é obrigatório: sem ele o retrato ficaria vazio, então o gerador levanta. INDICE.md e
retrato.json dizem que o retrato é sem literatura.

Fixo no ciclo, como o F(A): se o retrato do agente já existe naquele ciclo, o gerador para. Se o
que existe foi feito no outro modo (com ou sem literatura), ele levanta em vez de parar calado.
`--refazer` apaga e refaz; serve para consertar um ciclo que ainda não começou.
"""

from __future__ import annotations

import argparse
import datetime as dt
import importlib.util
import json
import re
import shutil
import sys
from dataclasses import dataclass, field
from functools import lru_cache
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
OBSIDIAN = RAIZ / "obsidian"
CICLOS = OBSIDIAN / "ciclos"
CONCEITOS = OBSIDIAN / "concepts"
SCRIPTS = RAIZ / "repository" / "ingestion" / "scripts"

# agente -> pasta da área no vault (None: agente que ainda não tem pasta). É o OWNERS do tracker.py,
# o mapa que o owner.py usa para mover as fontes; tests/test_conhecimento.py exige os dois iguais
AREA = {"cambio": "exchange_rate", "politica_monetaria": "monetary_policy", "inflacao": "inflation",
        "fiscal": "fiscal_policy", "atividade": "economic_activity", "mercado_trabalho": "labor_market",
        "trader": "trader", "externo": "external", "expectativas": "expectations", "credito": None}
DONO_DA_AREA = {a: d for d, a in AREA.items() if a}
DONO_COPOM = "politica_monetaria"

# [[alvo]], [[alvo|apelido]], [[alvo#seção]]; dentro de tabela o pipe vem escapado como \|
LINK = re.compile(r"\[\[([^\]|#]+?)\\?(#[^\]|]*)?(?:\\?\|([^\]]*))?\]\]")


@lru_cache(maxsize=1)
def tracker():
    """repository/ingestion/scripts/tracker.py, carregado pelo caminho (repository/ não é pacote)."""
    spec = importlib.util.spec_from_file_location("_tracker_ingestao", SCRIPTS / "tracker.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


@dataclass
class Item:
    """Uma unidade de conhecimento: a nota principal e os arquivos que vão junto com ela."""
    chave: str                      # caminho da nota principal a partir de obsidian/, sem .md
    tipo: str                       # literatura · modelo_mental · copom
    dono: str
    camada: int
    arquivos: list[Path] = field(default_factory=list)
    falta: list[str] = field(default_factory=list)   # o que a camada 1 pede e não existe no vault


# ── o que o tracker diz ──────────────────────────────────────────────────────

def _camada(v) -> int | None:
    try:
        c = int(str(v).strip())
    except (TypeError, ValueError):
        return None
    return c if c in (1, 2, 3) else None


def itens(ciclo: dt.date, planilha: Path | None = None) -> tuple[list[Item], list[str]]:
    """Todo item com dono e camada no tracker, mais os do Copom para a data do ciclo. Devolve
    também os avisos (dono ou camada inválidos), que vão para o INDICE."""
    import openpyxl

    tk = tracker()
    wb = openpyxl.load_workbook(planilha or tk.TRACKER, read_only=True)
    topico = {aba: t for t, aba in tk.TAB.items()}
    out, avisos = [], []
    for aba in wb.sheetnames:
        if not aba.startswith("Qual - "):
            continue
        t = topico.get(aba, aba.removeprefix("Qual - ").lower().replace(" ", "_"))
        linhas = wb[aba].iter_rows(values_only=True)
        cab = [str(c or "") for c in next(linhas)]
        if not all(h in cab for h in ("Dono", "Camada", "File")):
            avisos.append(f"{aba}: sem as colunas Dono/Camada/File — rode tracker.py")
            continue
        iD, iC, iF = cab.index("Dono"), cab.index("Camada"), cab.index("File")
        for r in linhas:
            dono, camada, arqs = str(r[iD] or "").strip(), _camada(r[iC]), str(r[iF] or "").splitlines()
            nomes = [a.strip() for a in arqs if a.strip()]
            if r[iC] in (None, ""):
                continue                               # ainda sem camada: fora de todo retrato, sem aviso
            if dono not in AREA or camada is None:
                avisos.append(f"{aba}: {', '.join(nomes) or r[0]} — dono {dono!r} ou camada {r[iC]!r} "
                              "fora do esperado; fora do retrato")
                continue
            for nome in nomes:
                it = Item(f"{t}/synthesis/{nome}", "literatura", dono, camada)
                for p, o_que in ((OBSIDIAN / t / "synthesis" / f"{nome}.md", "síntese"),
                                 (OBSIDIAN / t / "clean_md" / f"{nome}.md", "clean_md")):
                    (it.arquivos.append(p) if p.exists() else it.falta.append(o_que))
                out.append(it)
    if tk.MM_TAB in wb.sheetnames:
        ws = wb[tk.MM_TAB]
        linhas = ws.iter_rows(values_only=True)
        cab = [str(c or "") for c in next(linhas)]
        iDoc, iA, iC = cab.index("Document"), cab.index("Area"), cab.index("Camada")
        for r in linhas:
            if not r or not r[iDoc]:
                break                                  # a linha em branco antes da tabela de cartas
            camada = _camada(r[iC])
            if camada is None:
                continue
            dono = DONO_DA_AREA.get(r[iA])
            p = OBSIDIAN / str(r[iA]) / "mental_models" / f"{r[iDoc]}.md"
            it = Item(f"{r[iA]}/mental_models/{r[iDoc]}", "modelo_mental", dono, camada)
            (it.arquivos.append(p) if p.exists() else it.falta.append("documento"))
            out.append(it)
    wb.close()                                         # read_only segura o arquivo aberto até fechar
    return out + itens_copom(ciclo), avisos


def itens_copom(ciclo: dt.date) -> list[Item]:
    """Os documentos do Copom publicados antes da data do ciclo, com a camada de cada um."""
    tk = tracker()
    docs = tk.copom_docs()
    camadas = tk.copom_layer(docs, ciclo)
    out = []
    for d in docs:
        c = camadas[d["name"]]
        if c is not None:                              # None: publicado na data do ciclo ou depois
            rel = d["path"].relative_to(OBSIDIAN).with_suffix("")
            out.append(Item(rel.as_posix(), "copom", DONO_COPOM, c, [d["path"]]))
    return out


# ── links ────────────────────────────────────────────────────────────────────

def indice_vault() -> dict[str, list[Path]]:
    """nome (minúsculo) -> arquivos com esse nome no vault, FORA de ciclos/ (os retratos são cópias)."""
    out: dict[str, list[Path]] = {}
    for p in OBSIDIAN.rglob("*.md"):
        rel = p.relative_to(OBSIDIAN).parts
        if rel[0] in (".obsidian", "ciclos"):
            continue
        out.setdefault(p.stem.lower(), []).append(p)
    return out


def resolver(alvo: str, idx: dict[str, list[Path]], base: Path = OBSIDIAN) -> Path | None:
    """O arquivo de um wikilink, como o Obsidian: com barra, caminho a partir da raiz; sem barra,
    o nome (sem caixa), desde que seja único."""
    t = alvo.strip().rstrip("\\").strip()
    t = t[:-3] if t.lower().endswith(".md") else t
    if "/" in t:
        p = base / f"{t}.md"
        return p if p.exists() else None
    hits = idx.get(t.lower(), [])
    return hits[0] if len(hits) == 1 else None


def _rel(p: Path) -> str:
    return p.relative_to(OBSIDIAN).with_suffix("").as_posix()


def _texto_link(m: re.Match) -> str:
    """O que um link vira quando sai do retrato: o apelido, ou o nome sem o caminho."""
    return (m.group(3) or m.group(1).strip().rstrip("\\").split("/")[-1]).strip()


def deslinkar(texto: str, dentro: set[str], idx) -> str:
    def troca(m):
        p = resolver(m.group(1), idx)
        return m.group(0) if p is not None and _rel(p) in dentro else _texto_link(m)
    return LINK.sub(troca, texto)


def podar_conceito(texto: str, dentro: set[str], idx) -> str:
    """As linhas de uma página de conceito que ficam no retrato: a linha sem link; a que linka uma
    nota do retrato; a que só linka conceitos, quando algum deles está no retrato. Nas que ficam,
    o link para fora vira texto. Uma tabela que perdeu todas as linhas do corpo some com o
    cabeçalho (None marca a linha cortada dentro de uma tabela)."""
    saida, tabela = [], []
    for ln in texto.splitlines():
        alvos = [resolver(m.group(1), idx) for m in LINK.finditer(ln)]
        if alvos:
            fontes = [p for p in alvos if p is None or p.parent != CONCEITOS]
            conceitos = [p for p in alvos if p is not None and p.parent == CONCEITOS]
            fica = (any(p is not None and _rel(p) in dentro for p in fontes)
                    or (not fontes and any(_rel(p) in dentro for p in conceitos)))
            if not fica:
                if tabela:
                    tabela.append(None)
                continue
            ln = deslinkar(ln, dentro, idx)
        if ln.lstrip().startswith("|"):
            tabela.append(ln)
            continue
        _fecha(tabela, saida)
        saida.append(ln)
    _fecha(tabela, saida)
    return "\n".join(saida) + ("\n" if texto.endswith("\n") else "")


def _fecha(tabela: list, saida: list) -> None:
    vivas = [ln for ln in tabela if ln is not None]
    if vivas[2:] or len(vivas) == len(tabela):      # sobrou corpo, ou nada foi cortado
        saida.extend(vivas)
    tabela.clear()


# ── o alcance ────────────────────────────────────────────────────────────────

def alcance(agente: str, todos: list[Item], idx) -> tuple[dict[str, tuple[Item, str]], dict[str, str]]:
    """(itens que entram: chave -> (item, motivo); conceitos que entram: chave -> motivo)."""
    camada1 = {it.chave: it for it in todos if it.camada == 1 and it.arquivos}
    entra = {k: (it, "camada 1 do agente") for k, it in camada1.items() if it.dono == agente}
    # as chaves que um link pode alcançar: a nota principal e os arquivos que vão com ela
    por_arquivo = {_rel(p): k for k, it in camada1.items() for p in it.arquivos}
    conceitos, links_do_conceito = {}, {}
    for pagina in sorted(CONCEITOS.glob("*.md")):
        alvos = {_rel(p) for m in LINK.finditer(pagina.read_text(encoding="utf-8"))
                 if (p := resolver(m.group(1), idx)) is not None}
        links_do_conceito[_rel(pagina)] = alvos
        proprios = sorted({por_arquivo[a] for a in alvos if a in por_arquivo and por_arquivo[a] in entra})
        if proprios:
            conceitos[_rel(pagina)] = "linka " + ", ".join(proprios[:3]) + (" …" if len(proprios) > 3 else "")
    for c in conceitos:
        for a in sorted(links_do_conceito[c]):
            k = por_arquivo.get(a)
            if k and k not in entra:
                entra[k] = (camada1[k], f"camada 1 de {camada1[k].dono}, pelo conceito {c.split('/')[-1]}")
    return entra, conceitos


# ── o retrato ────────────────────────────────────────────────────────────────

def pasta(agente: str, ciclo: dt.date, destino: Path = CICLOS) -> Path:
    return Path(destino) / ciclo.isoformat() / "conhecimento" / agente


def mapa_de(agente: str) -> Path | None:
    """O mapa conceitual do agente no vault (None: agente sem pasta)."""
    return OBSIDIAN / AREA[agente] / f"{AREA[agente]}_conceptual_map.md" if AREA[agente] else None


def gerar(agente: str, ciclo: dt.date, refazer: bool = False, planilha: Path | None = None,
          destino: Path = CICLOS, sem_literatura: bool = False) -> Path:
    if agente not in AREA:
        raise ValueError(f"agente desconhecido {agente!r}; conhecidos: {', '.join(AREA)}")
    saida = pasta(agente, ciclo, destino)
    if saida.exists() and not refazer:
        feito = saida / "retrato.json"
        modo = json.loads(feito.read_text(encoding="utf-8")).get("sem_literatura", False) if feito.exists() else None
        if modo is not None and modo != sem_literatura:
            raise ValueError(f"{saida} já existe {'sem' if modo else 'com'} literatura, e o pedido é "
                             f"{'sem' if sem_literatura else 'com'}. Use --refazer para refazer.")
        raise FileExistsError(f"{saida} já existe: o retrato é fixo no ciclo. Use --refazer para refazer.")
    mapa = mapa_de(agente)
    if sem_literatura:
        # Só o mapa e, para o dono do Copom, os documentos da camada 1. O tracker nem é lido.
        if mapa is None or not mapa.exists():
            onde = mapa.relative_to(OBSIDIAN).as_posix() if mapa else "o agente não tem pasta no vault"
            raise FileNotFoundError(f"{agente}: falta o mapa conceitual ({onde}); "
                                    "sem ele o retrato sem literatura ficaria vazio")
        todos, avisos = itens_copom(ciclo), []
        idx = indice_vault()
        entra = {it.chave: (it, "camada 1 do agente") for it in todos
                 if it.dono == agente and it.camada == 1 and it.arquivos}
        conceitos: dict[str, str] = {}
    else:
        todos, avisos = itens(ciclo, planilha)
        idx = indice_vault()
        entra, conceitos = alcance(agente, todos, idx)
    dentro = {_rel(p) for it, _ in entra.values() for p in it.arquivos} | set(conceitos)
    if mapa is not None and mapa.exists():
        dentro.add(_rel(mapa))

    if saida.exists():
        shutil.rmtree(saida)
    saida.mkdir(parents=True)
    linhas = []

    def grava(p: Path, texto: str) -> Path:
        alvo = saida / p.relative_to(OBSIDIAN)
        alvo.parent.mkdir(parents=True, exist_ok=True)
        alvo.write_text(texto, encoding="utf-8")
        return alvo

    for k, (it, motivo) in sorted(entra.items(), key=lambda x: (x[1][0].dono != agente, x[1][0].tipo, x[0])):
        for p in it.arquivos:
            texto = p.read_text(encoding="utf-8")
            grava(p, deslinkar(texto, dentro, idx) if "[[" in texto else texto)
            linhas.append({"arquivo": _rel(p) + ".md", "tipo": it.tipo, "dono": it.dono, "camada": it.camada,
                           "outro_dono": it.dono != agente, "motivo": motivo})
    for c, motivo in sorted(conceitos.items()):
        p = OBSIDIAN / f"{c}.md"
        grava(p, podar_conceito(p.read_text(encoding="utf-8"), dentro, idx))
        linhas.append({"arquivo": f"{c}.md", "tipo": "conceito", "dono": None, "camada": None,
                       "outro_dono": False, "motivo": motivo})
    if mapa is not None and mapa.exists():
        grava(mapa, mapa.read_text(encoding="utf-8"))
        linhas.append({"arquivo": _rel(mapa) + ".md", "tipo": "mapa", "dono": agente, "camada": None,
                       "outro_dono": False, "motivo": "mapa conceitual do agente, inteiro"})
    faltando = [f"{it.chave}: falta {', '.join(it.falta)}" for it in todos
                if it.dono == agente and it.camada == 1 and it.falta]

    meta = {"agente": agente, "ciclo": ciclo.isoformat(), "gerado_em": dt.datetime.now().isoformat(timespec="seconds"),
            "sem_literatura": sem_literatura, "arquivos": linhas, "camada1_sem_arquivo": faltando, "avisos": avisos}
    (saida / "retrato.json").write_text(json.dumps(meta, ensure_ascii=False, indent=1), encoding="utf-8")
    (saida / "INDICE.md").write_text(_indice_md(meta), encoding="utf-8")
    return saida


def _indice_md(meta: dict) -> str:
    n_outro = sum(1 for x in meta["arquivos"] if x["outro_dono"])
    out = [f"# Retrato do conhecimento — {meta['agente']} · ciclo {meta['ciclo']}", "",
           "O que este agente pode ler neste ciclo, e só isto. Cada caminho é relativo a esta pasta e repete o "
           "do vault, então os wikilinks resolvem aqui dentro. A coluna **outro dono** marca o material da "
           "biblioteca de outro agente, alcançado por uma página de conceito: ao abrir um desses arquivos, "
           "registre no log.", "",
           f"{len(meta['arquivos'])} arquivos · {n_outro} de outros donos · gerado em {meta['gerado_em']}", ""]
    if meta.get("sem_literatura"):
        out += ["**Retrato sem literatura.** Neste ciclo o agente lê só o mapa conceitual"
                + (" e os documentos do Copom da camada 1" if any(x["tipo"] == "copom" for x in meta["arquivos"]) else "")
                + ": nenhuma síntese, clean_md, página de conceito ou modelo mental. O que o mapa cita e não está "
                "aqui não pode ser lido neste ciclo.", ""]
    out += ["| arquivo | tipo | dono | camada | outro dono | por que entrou |", "|---|---|---|---|---|---|"]
    for x in meta["arquivos"]:
        out.append(f"| {x['arquivo']} | {x['tipo']} | {x['dono'] or '—'} | {x['camada'] or '—'} | "
                   f"{'sim' if x['outro_dono'] else ''} | {x['motivo']} |")
    if meta["camada1_sem_arquivo"]:
        out += ["", "## Camada 1 que não está no vault", "",
                "Itens da camada 1 deste agente que o tracker lista e que ainda não têm o arquivo (síntese ou "
                "clean_md). Se fizer falta na análise, registre em \"faltou\" no log.", ""]
        out += [f"- {x}" for x in meta["camada1_sem_arquivo"]]
    if meta["avisos"]:
        out += ["", "## Avisos do tracker", ""] + [f"- {x}" for x in meta["avisos"]]
    return "\n".join(out) + "\n"


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser(prog="python -m analytics.agent_system.conhecimento")
    ap.add_argument("agente", choices=sorted(AREA))
    ap.add_argument("--ciclo", type=dt.date.fromisoformat, default=dt.date.today())
    ap.add_argument("--refazer", action="store_true")
    ap.add_argument("--sem-literatura", action="store_true",
                    help="só o mapa conceitual (e o Copom da camada 1, na política monetária)")
    a = ap.parse_args()
    try:
        saida = gerar(a.agente, a.ciclo, a.refazer, sem_literatura=a.sem_literatura)
    except (FileExistsError, FileNotFoundError, ValueError) as e:
        sys.exit(str(e))
    meta = json.loads((saida / "retrato.json").read_text(encoding="utf-8"))
    print(f"  retrato  {saida}  ({len(meta['arquivos'])} arquivos, "
          + ("sem literatura, " if meta["sem_literatura"] else "")
          + f"{sum(1 for x in meta['arquivos'] if x['outro_dono'])} de outros donos)")
    for x in meta["camada1_sem_arquivo"] + meta["avisos"]:
        print(f"  aviso    {x}")


if __name__ == "__main__":
    main()
