# -*- coding: utf-8 -*-
"""Testa o retrato do conhecimento por ciclo (analytics/agent_system/conhecimento.py, PLANO_AGENTES 3C).

Roda com:
    uv run python tests/test_conhecimento.py

Script com asserts, não pytest (mesmo padrão de tests/test_dados_agentes.py). Não escreve no vault
nem na planilha real: o tracker é uma cópia com uma camada 1 FICTÍCIA, e o retrato vai para uma
pasta temporária. Cada item erra sem levantar nada se quebrar:

1. entra no retrato algo que não é camada 1 do dono (camada 2 do agente, ou de outro dono);
2. um wikilink de um arquivo copiado aponta para fora do retrato (salvo os do mapa) — o agente
   seguiria o link de volta ao vault inteiro;
3. a camada 1 de outro dono, alcançada por um conceito, não entra, ou entra sem a marca de
   "outro dono" que o log usa;
4. um documento do Copom publicado na data do ciclo ou depois entra no retrato (a ata sai ~6 dias
   depois da reunião);
5. rodar de novo sem --refazer refaz o retrato no meio do ciclo;
6. o retrato sem literatura leva algo além do mapa (e do Copom da camada 1, na PM), não diz que é
   sem literatura, sai vazio quando falta o mapa, ou um retrato do outro modo passa por "já existe".
"""
from __future__ import annotations

import datetime as dt
import json
import shutil
import sys
import tempfile
from pathlib import Path

import openpyxl

from analytics.agent_system import conhecimento as k

sys.stdout.reconfigure(encoding="utf-8")
falhas = 0


def confere(cond, msg):
    global falhas
    if not cond:
        falhas += 1
        print(f"FALHA  {msg}")
    else:
        print(f"ok     {msg}")


# A camada 1 fictícia (as colunas reais são do usuário e mudam): três fontes e um modelo mental do
# câmbio; uma fonte fiscal que um conceito do câmbio linka (uip, fiscal_dominance); e duas camadas 2
# que esses mesmos conceitos linkam — uma do câmbio, uma de outro dono — e que não podem entrar.
FICTICIA = {
    "expectations_and_exchange_rate_dynamics (Dornbusch, 1976)": ("cambio", 1),
    "capital_mobility_exchange_rates_regimes (Mundell, 1963)": ("cambio", 1),
    "primer_gsdeer_gsfeer (Goldman, 2025)": ("cambio", 1),
    "fiscal_dominance (itau, 2025)": ("fiscal", 1),
    "exchange_rate_foreign_exchange_market (Krugman, 2023)": ("cambio", 2),
    "fiscal_dominance_it_brazil (Blanchard, 2004)": ("politica_monetaria", 2),
}
MM_FICTICIO = {"verde_fx_mental_models": 1, "kinea_fx_mental_models": 2}


def planilha_ficticia(destino: Path) -> Path:
    tk = k.tracker()
    p = destino / "data_tracker.xlsx"
    shutil.copy(tk.TRACKER, p)
    wb = openpyxl.load_workbook(p)
    for aba in wb.sheetnames:
        ws = wb[aba]
        if aba.startswith("Qual - "):
            cab = {ws.cell(1, c).value: c for c in range(1, ws.max_column + 1)}
            for r in range(2, ws.max_row + 1):
                for h in ("Dono", "Camada", "Fila"):
                    ws.cell(r, cab[h]).value = None
                for nome in str(ws.cell(r, cab["File"]).value or "").splitlines():
                    if nome.strip() in FICTICIA:
                        ws.cell(r, cab["Dono"]).value, ws.cell(r, cab["Camada"]).value = FICTICIA[nome.strip()]
        elif aba == tk.MM_TAB:
            cab = {ws.cell(1, c).value: c for c in range(1, ws.max_column + 1)}
            for r in range(2, ws.max_row + 1):
                if not ws.cell(r, 1).value:
                    break
                ws.cell(r, cab["Camada"]).value = MM_FICTICIO.get(ws.cell(r, 1).value)
    wb.save(p)
    return p


def links_para_fora(raiz: Path) -> list[str]:
    """Todo wikilink de um arquivo do retrato (menos o mapa e o INDICE) que não resolve lá dentro."""
    idx = {}
    for p in raiz.rglob("*.md"):
        idx.setdefault(p.stem.lower(), []).append(p)
    fora = []
    for p in raiz.rglob("*.md"):
        if p.name == "INDICE.md" or p.name.endswith("_conceptual_map.md"):
            continue
        for m in k.LINK.finditer(p.read_text(encoding="utf-8")):
            if k.resolver(m.group(1), idx, base=raiz) is None:
                fora.append(f"{p.relative_to(raiz)} -> {m.group(1)}")
    return fora


with tempfile.TemporaryDirectory() as tmp:
    tmp = Path(tmp)
    planilha = planilha_ficticia(tmp)
    ciclo = dt.date(2026, 9, 20)

    # ── câmbio ──────────────────────────────────────────────────────────────
    raiz = k.gerar("cambio", ciclo, planilha=planilha, destino=tmp / "ciclos")
    meta = json.loads((raiz / "retrato.json").read_text(encoding="utf-8"))
    arqs = {x["arquivo"]: x for x in meta["arquivos"]}
    print(f"\nretrato do câmbio: {len(arqs)} arquivos")

    nao_conceito = [x for x in meta["arquivos"] if x["tipo"] in ("literatura", "modelo_mental", "copom")]
    confere(nao_conceito and all(x["camada"] == 1 for x in nao_conceito), "1. só camada 1 no retrato")
    confere(not any("Krugman, 2023" in a or "Blanchard, 2004" in a for a in arqs),
            "1. a camada 2 linkada pelos mesmos conceitos fica fora (do câmbio e de outro dono)")
    confere("exchange_rate/mental_models/kinea_fx_mental_models.md" not in arqs, "1. modelo mental de camada 2 fica fora")
    # o caminho é o da pasta em que a nota está: Mundell (1963) está em monetary_policy/ e aqui o dono
    # fictício é o câmbio — o dono vem do tracker, e o retrato o acha na pasta em que estiver
    confere(all(any(a.endswith(f"/synthesis/{n}.md") and (k.OBSIDIAN / a).exists() for a in arqs)
                for n, (d, c) in FICTICIA.items() if d == "cambio" and c == 1),
            "a camada 1 do câmbio entra, com o caminho do vault")
    confere(k.AREA == k.tracker().OWNERS, "o AREA do retrato é o OWNERS do tracker (dono -> pasta)")
    confere("exchange_rate/mental_models/verde_fx_mental_models.md" in arqs, "o modelo mental de camada 1 entra")
    confere("exchange_rate/exchange_rate_conceptual_map.md" in arqs, "o mapa conceitual entra")

    fora = links_para_fora(raiz)
    confere(not fora, f"2. nenhum wikilink aponta para fora do retrato ({len(fora)}: {fora[:3]})")

    outro = arqs.get("fiscal_policy/synthesis/fiscal_dominance (itau, 2025).md")
    confere(outro is not None and outro["outro_dono"] and outro["dono"] == "fiscal" and "pelo conceito" in outro["motivo"],
            "3. a camada 1 de outro dono entra pelo conceito, marcada como outro dono")
    confere(not any(x["outro_dono"] and x["tipo"] == "conceito" for x in meta["arquivos"]),
            "3. não é transitivo: conceito só entra por nota do próprio agente")
    indice = (raiz / "INDICE.md").read_text(encoding="utf-8")
    confere("| sim |" in indice and "outro dono" in indice, "3. o INDICE marca o material de outro dono")

    uip = (raiz / "concepts/uip.md").read_text(encoding="utf-8")
    original = (k.CONCEITOS / "uip.md").read_text(encoding="utf-8")
    confere("[[exchange_rate/synthesis/expectations_and_exchange_rate_dynamics (Dornbusch, 1976)]]" in uip
            and "Krugman, 2023)]]" not in uip and "Krugman, 2023)]]" in original,
            "conceito: fica a linha da nota do retrato, sai a da camada 2")
    confere("[[fiscal_policy/synthesis/fiscal_dominance (itau, 2025)]]" in uip, "conceito: fica a linha da nota de outro dono que entrou")
    confere("## Statement" in uip, "conceito: as linhas sem link (a definição) ficam")
    confere(not any(m.group(1).startswith("monetary_policy/clean_md/central_bank") for m in k.LINK.finditer(uip)),
            "câmbio: sem Copom (é de politica_monetaria e nenhum conceito o linka)")

    # ── refazer ─────────────────────────────────────────────────────────────
    antes = (raiz / "retrato.json").stat().st_mtime_ns
    try:
        k.gerar("cambio", ciclo, planilha=planilha, destino=tmp / "ciclos")
        confere(False, "5. rodar de novo sem --refazer para")
    except FileExistsError:
        confere((raiz / "retrato.json").stat().st_mtime_ns == antes, "5. rodar de novo sem --refazer para e não toca no retrato")
    (raiz / "lixo.md").write_text("x", encoding="utf-8")
    k.gerar("cambio", ciclo, refazer=True, planilha=planilha, destino=tmp / "ciclos")
    confere(not (raiz / "lixo.md").exists(), "5. --refazer refaz do zero")

    # ── política monetária: o Copom pela data do ciclo ──────────────────────
    raiz_pm = k.gerar("politica_monetaria", ciclo, planilha=planilha, destino=tmp / "ciclos")
    meta = json.loads((raiz_pm / "retrato.json").read_text(encoding="utf-8"))
    copom = [x["arquivo"] for x in meta["arquivos"] if x["tipo"] == "copom"]
    docs = {d["name"]: d for d in k.tracker().copom_docs()}
    pub = [docs[Path(a).stem]["published"] for a in copom]
    confere(copom and all(p < ciclo for p in pub), f"4. nenhum documento do Copom publicado em {ciclo} ou depois ({len(copom)} no retrato)")
    confere(not any("copom_281_ata" in a for a in copom) and any("copom_281_comunicado" in a for a in copom),
            "4. a ata da 281ª (publicada 22/09) fica fora; o comunicado (16/09) entra")
    confere(sum("comunicado" in a for a in copom) == 14 and sum("/rpm/" in a for a in copom) == 6,
            "4. camada 1 do Copom: 14 comunicados do mandato, RPMs de 202503 a 202606")
    fora = links_para_fora(raiz_pm)
    confere(not fora, f"2. PM: nenhum wikilink para fora ({len(fora)}: {fora[:3]})")
    copom_com = sorted(copom)

    # ── sem literatura ──────────────────────────────────────────────────────
    sem = tmp / "sem"
    raiz = k.gerar("cambio", ciclo, planilha=planilha, destino=sem, sem_literatura=True)
    meta = json.loads((raiz / "retrato.json").read_text(encoding="utf-8"))
    confere([x["arquivo"] for x in meta["arquivos"]] == ["exchange_rate/exchange_rate_conceptual_map.md"],
            f"6. câmbio sem literatura: só o mapa ({[x['arquivo'] for x in meta['arquivos']]})")
    no_disco = sorted(p.relative_to(raiz).as_posix() for p in raiz.rglob("*") if p.is_file())
    confere(no_disco == ["INDICE.md", "exchange_rate/exchange_rate_conceptual_map.md", "retrato.json"],
            f"6. e no disco também ({no_disco})")
    confere(meta["sem_literatura"] is True and "sem literatura" in (raiz / "INDICE.md").read_text(encoding="utf-8"),
            "6. retrato.json e INDICE dizem que é sem literatura")

    raiz_pm = k.gerar("politica_monetaria", ciclo, planilha=planilha, destino=sem, sem_literatura=True)
    meta = json.loads((raiz_pm / "retrato.json").read_text(encoding="utf-8"))
    tipos = {x["tipo"] for x in meta["arquivos"]}
    copom = sorted(x["arquivo"] for x in meta["arquivos"] if x["tipo"] == "copom")
    confere(tipos == {"mapa", "copom"}, f"6. PM sem literatura: só o mapa e o Copom ({tipos})")
    confere(copom == copom_com, f"6. PM sem literatura: os mesmos {len(copom_com)} documentos do Copom da camada 1")
    confere(all(docs[Path(a).stem]["published"] < ciclo for a in copom),
            f"4. sem literatura: nenhum documento do Copom publicado em {ciclo} ou depois")
    confere(not any("/synthesis/" in x["arquivo"] or "/clean_md/" in x["arquivo"] and x["tipo"] != "copom"
                    or x["arquivo"].startswith("concepts/") or "/mental_models/" in x["arquivo"]
                    for x in meta["arquivos"]),
            "6. PM sem literatura: nenhuma síntese, clean_md, conceito ou modelo mental")
    fora = links_para_fora(raiz_pm)
    confere(not fora, f"2. PM sem literatura: nenhum wikilink para fora ({len(fora)}: {fora[:3]})")
    confere("Copom" in (raiz_pm / "INDICE.md").read_text(encoding="utf-8").split("| arquivo |")[0],
            "6. o INDICE da PM diz que entram os documentos do Copom")

    # o modo do retrato que já existe tem de bater com o pedido
    try:
        k.gerar("cambio", ciclo, planilha=planilha, destino=sem)
        confere(False, "6. retrato sem literatura que já existe, pedido com: levanta")
    except ValueError as e:
        confere("sem literatura" in str(e), "6. retrato sem literatura que já existe, pedido com: levanta")
    except FileExistsError:
        confere(False, "6. retrato sem literatura que já existe, pedido com: levanta (não só 'já existe')")
    try:
        k.gerar("cambio", ciclo, planilha=planilha, destino=sem, sem_literatura=True)
        confere(False, "6. mesmo modo: para com 'já existe'")
    except FileExistsError:
        confere(True, "6. mesmo modo: para com 'já existe'")

    # sem mapa, o retrato sem literatura ficaria vazio: levanta
    k.AREA["_teste_sem_mapa"] = "_pasta_que_nao_existe"
    try:
        for ag, trecho in (("credito", "não tem pasta"), ("_teste_sem_mapa", "_pasta_que_nao_existe_conceptual_map")):
            try:
                k.gerar(ag, ciclo, planilha=planilha, destino=sem, sem_literatura=True)
                confere(False, f"6. {ag} sem mapa: levanta")
            except FileNotFoundError as e:
                confere(trecho in str(e) and not k.pasta(ag, ciclo, sem).exists(),
                        f"6. {ag} sem mapa: levanta com o caminho, sem criar a pasta")
    finally:
        del k.AREA["_teste_sem_mapa"]

    confere(k.AREA["externo"] == "external" and k.AREA["expectativas"] == "expectations"
            and k.DONO_DA_AREA["expectations"] == "expectativas" and "expectativas" in k.tracker().OWNERS,
            "externo e expectativas reconhecidos (vault e tracker)")

print(f"\n{'tudo ok' if not falhas else f'{falhas} falha(s)'}")
sys.exit(1 if falhas else 0)
