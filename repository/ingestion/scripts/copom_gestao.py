"""
repository/ingestion/scripts/copom_gestao.py — index page of the Copom documents of one BCB
presidency ("gestão"), published in the vault. Deterministic: no AI, same inputs, same bytes.

    uv run python repository/ingestion/scripts/copom_gestao.py build --gestao galipolo
    uv run python repository/ingestion/scripts/copom_gestao.py check --gestao galipolo

The Copom ETL writes the minutes and statements (obsidian/monetary_policy/clean_md/central_bank/
atas|comunicados) and mirrors them byte for byte on every run, so they are never edited: tags
and links live outside them, here.

Inputs
  A. repository/central_bank/gestao_<gestao>_temas.yaml — per meeting, the themes and for each
     one an `evidence` sentence copied word for word from the ata or the comunicado.
  B. VOCABULARY below — the closed list of theme slugs and the concept pages each points to.
  C. MySQL macro_brasil.pm_copom_reuniao — the decision (Selic before/after, bps, decisao).

Outputs
  obsidian/monetary_policy/central_bank/gestao_<gestao>.md — the index page, one section per meeting.
  In every concept page that a theme points to, ONE managed line (marker MARK_PREFIX + gestao,
  at the end of the line): created if absent, replaced if present, removed from pages no
  longer referenced. Nothing else on a concept page is touched.

check fails (exit 1) when a theme is outside the vocabulary, an evidence sentence is not in the
meeting's ata/comunicado, a link does not resolve, a meeting of the gestão is missing (table,
files, themes file or page), the decision on the page differs from the table, or the index page
or a managed concept line differs from what build would write.
"""

import argparse
import datetime as dt
import re
import sys
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))
from run import OBSIDIAN  # noqa: E402

ROOT = Path(__file__).resolve().parents[3]
CONCEPTS = OBSIDIAN / "concepts"
CB_CLEAN = OBSIDIAN / "monetary_policy" / "clean_md" / "central_bank"
ATAS_DIR = CB_CLEAN / "atas"
COMUNICADOS_DIR = CB_CLEAN / "comunicados"
PAGE_DIR = OBSIDIAN / "monetary_policy" / "central_bank"
THEMES_DIR = ROOT / "repository" / "central_bank"

GESTOES = {"galipolo": {"nome": "Galípolo", "inicio": "2025-01-01"}}

# theme slug -> (what it covers, concept pages). A theme with no page has no link.
VOCABULARY = {
    "expectativas": ("Inflation expectations and their anchoring to the target", ["inflation_expectations_anchoring"]),
    "fiscal": ("Fiscal policy and its effect on inflation and the neutral rate", ["fiscal_dominance", "fiscal_impulse"]),
    "cambio": ("Exchange rate and its pass-through to prices", ["exchange_rate_pass_through"]),
    "mercado-de-trabalho": ("Labour market, slack and wages", ["natural_rate_of_unemployment"]),
    "hiato": ("Output gap and the pace of activity", ["output_gap"]),
    "credito": ("Credit conditions and the transmission channel", ["credit_channel"]),
    "externo": ("External environment, global financial conditions", ["global_financial_cycle"]),
    "commodities": ("Commodity price shocks", ["commodity_shocks"]),
    "guidance": ("The Copom's communication and forward guidance", ["central_bank_communication", "forward_guidance"]),
    "balanco-de-riscos": ("The balance of risks around the inflation outlook", []),
    "inercia": ("Inflation persistence and indexation", ["inflation_persistence"]),
}

MARK_PREFIX = "<!-- copom-gestao:"


def mark(gestao: str) -> str:
    return f"{MARK_PREFIX}{gestao} -->"


def page_name(gestao: str) -> str:
    return f"gestao_{gestao}"


def _norm(s: str) -> str:
    return re.sub(r"\s+", " ", s).strip()


def _brl(x) -> str:
    return f"{float(x):.2f}".replace(".", ",")


# ── inputs ────────────────────────────────────────────────────────────────────

def read_decisions() -> list[dict]:
    """pm_copom_reuniao rows: nro_reuniao, date (ISO string), selic_anterior, selic_decidida,
    variacao_bps, decisao. Read-only."""
    from connectors.mysql import MySQLDataRequester
    r = MySQLDataRequester("macro_brasil", "pm_copom_reuniao")
    r.connect()
    try:
        cur = r.connection.cursor()
        cur.execute("SELECT nro_reuniao, date, selic_anterior, selic_decidida, variacao_bps, decisao "
                    "FROM pm_copom_reuniao ORDER BY date")
        return [{"nro": int(a), "date": str(b), "ant": c, "dec": d, "bps": int(e), "decisao": f}
                for a, b, c, d, e, f in cur.fetchall()]
    finally:
        r.close_connection()


def _doc(dirpath: Path, kind: str, nro: int) -> Path | None:
    hits = sorted(dirpath.glob(f"copom_{nro}_{kind}_*.md")) if dirpath.is_dir() else []
    return hits[0] if hits else None


def load_themes(gestao: str) -> dict:
    p = THEMES_DIR / f"gestao_{gestao}_temas.yaml"
    data = yaml.safe_load(p.read_text(encoding="utf-8")) or {}
    return {int(k): (v or {}).get("temas") or [] for k, v in (data.get("reunioes") or {}).items()}


def meetings(gestao: str) -> list[dict]:
    """The meetings of the gestão (date >= its start) in the table, with their documents; plus
    any meeting that has a document file in the period but no table row (flagged by the check)."""
    start = GESTOES[gestao]["inicio"]
    out = {}
    for r in read_decisions():
        if r["date"] >= start:
            out[r["nro"]] = dict(r, in_table=True)
    for kind, d in (("ata", ATAS_DIR), ("comunicado", COMUNICADOS_DIR)):
        for f in d.glob(f"copom_*_{kind}_*.md") if d.is_dir() else []:
            m = re.fullmatch(rf"copom_(\d+)_{kind}_(\d{{4}}-\d{{2}}-\d{{2}})\.md", f.name)
            if m and m.group(2) >= start and int(m.group(1)) not in out:
                out[int(m.group(1))] = {"nro": int(m.group(1)), "date": m.group(2), "in_table": False}
    for n, m in out.items():
        m["ata"] = _doc(ATAS_DIR, "ata", n)
        m["com"] = _doc(COMUNICADOS_DIR, "comunicado", n)
    return [out[n] for n in sorted(out)]


def _publication(ata: Path | None) -> str | None:
    if ata is None:
        return None
    m = re.search(r"^Data de publicação:\s*(\S+)", ata.read_text(encoding="utf-8"), re.M)
    return m.group(1) if m else None


# ── render ────────────────────────────────────────────────────────────────────

def _vault_link(p: Path) -> str:
    return f"[[{p.relative_to(OBSIDIAN).with_suffix('').as_posix()}]]"


def _heading(m: dict) -> str:
    return f"Reunião {m['nro']} — {m['date']}"


def decision_line(m: dict) -> str:
    return (f"**Decisão:** Selic {_brl(m['ant'])}% → {_brl(m['dec'])}% "
            f"({m['bps']:+d} bps, {m['decisao']})")


def render_page(gestao: str, ms: list[dict], themes: dict) -> str:
    g = GESTOES[gestao]
    L = [f"# Copom — gestão {g['nome']}", "", "## Sobre esta página", "",
         f"Índice das atas e dos comunicados do Copom da gestão {g['nome']}, a partir de {g['inicio']}. "
         "Os documentos são ligados como foram publicados, sem alteração: etiquetas e links vivem aqui, "
         "nunca neles. A decisão vem da tabela do Banco Central (pm_copom_reuniao). Os temas são "
         "escolhidos de um vocabulário fechado, cada um com uma frase do documento que o sustenta. "
         "Gerada por `copom_gestao.py build`; não editar à mão.", "",
         "## Vocabulário de temas", "", "| Tema | O que cobre | Conceitos |", "|---|---|---|"]
    for slug, (desc, cons) in VOCABULARY.items():
        L.append(f"| `{slug}` | {desc} | {', '.join(f'[[{c}]]' for c in cons) or '—'} |")
    for m in ms:
        ts = themes.get(m["nro"], [])
        tags = [f"#gestao/{gestao}", f"#copom/reuniao-{m['nro']}"]
        if m.get("decisao"):
            tags.append(f"#decisao/{m['decisao']}")
        tags += [f"#tema/{t['tema']}" for t in ts]
        pub = _publication(m["ata"])
        L += ["", f"## {_heading(m)}", "",
              f"- **Datas:** reunião {m['date']}" + (f" · publicação da ata {pub}" if pub else ""),
              f"- {decision_line(m)}", f"- **Tags:** {' '.join(tags)}"]
        docs = [f"ata {_vault_link(m['ata'])}"] if m["ata"] else []
        docs += [f"comunicado {_vault_link(m['com'])}"] if m["com"] else []
        L.append(f"- **Documentos:** {' · '.join(docs) or '—'}")
        if ts:
            L.append("- **Temas:**")
            for t in ts:
                cons = VOCABULARY[t["tema"]][1]
                L.append(f"  - `{t['tema']}` — \"{_norm(t['evidence'])}\""
                         + (f" — {', '.join(f'[[{c}]]' for c in cons)}" if cons else ""))
    return "\n".join(L) + "\n"


def concept_lines(gestao: str, ms: list[dict], themes: dict) -> dict[str, str]:
    """concept slug -> the managed line, for every concept some meeting's theme points to."""
    by: dict[str, list[dict]] = {}
    for m in ms:
        seen = set()
        for t in themes.get(m["nro"], []):
            for c in VOCABULARY[t["tema"]][1]:
                if c not in seen:
                    seen.add(c)
                    by.setdefault(c, []).append(m)
    nome = GESTOES[gestao]["nome"]
    return {c: f"Copom, gestão {nome}: " + ", ".join(
        f"[[monetary_policy/central_bank/{page_name(gestao)}#{_heading(m)}|{m['nro']}]]" for m in lst)
        + f" {mark(gestao)}" for c, lst in by.items()}


def apply_line(text: str, gestao: str, line: str | None) -> str:
    """The concept page text with the managed line created, replaced (in place) or removed
    (line=None). Everything else is returned byte for byte."""
    mk = mark(gestao)
    lines = text.split("\n")
    idx = [i for i, l in enumerate(lines) if l.rstrip().endswith(mk)]
    if line is None:
        if not idx:
            return text
        last = max(i for i, l in enumerate(lines) if l.strip()) == idx[-1]
        for i in reversed(idx):
            del lines[i]
        out = "\n".join(lines)
        return out.rstrip("\n") + "\n" if last else out
    if idx:
        lines[idx[0]] = line
        for i in reversed(idx[1:]):
            del lines[i]
        return "\n".join(lines)
    return text.rstrip("\n") + "\n\n" + line + "\n"


# ── check ─────────────────────────────────────────────────────────────────────

def input_problems(gestao: str, ms: list[dict], themes: dict) -> list[str]:
    prob = []
    for slug, (_, cons) in VOCABULARY.items():
        for c in cons:
            if not (CONCEPTS / f"{c}.md").exists():
                prob.append(f"vocabulary: {slug} → concept page {c} does not exist")
    nros = {m["nro"] for m in ms}
    for m in ms:
        if not m["in_table"]:
            prob.append(f"meeting {m['nro']} ({m['date']}) has documents but no row in pm_copom_reuniao")
        if m["nro"] not in themes:
            prob.append(f"meeting {m['nro']} is missing from the themes file")
    for n in themes:
        if n not in nros:
            prob.append(f"themes file: meeting {n} is not a meeting of the gestão")
    for m in ms:
        text = " ".join(_norm(p.read_text(encoding="utf-8")) for p in (m["ata"], m["com"]) if p)
        seen = set()
        for t in themes.get(m["nro"], []):
            slug, ev = t.get("tema"), t.get("evidence")
            if slug not in VOCABULARY:
                prob.append(f"meeting {m['nro']}: theme {slug!r} is not in the vocabulary")
                continue
            if slug in seen:
                prob.append(f"meeting {m['nro']}: theme {slug} repeated")
            seen.add(slug)
            if not ev or not _norm(str(ev)):
                prob.append(f"meeting {m['nro']}: theme {slug} has no evidence")
            elif _norm(str(ev)) not in text:
                prob.append(f"meeting {m['nro']}: evidence of {slug} not found in the ata or comunicado: "
                            f"{_norm(str(ev))[:80]}")
    return prob


LINK = re.compile(r"\[\[([^\]|#]+?)(?:#[^\]|]*)?(?:\|[^\]]*)?\]\]")


def _resolves(target: str) -> bool:
    t = target.strip()
    return ((OBSIDIAN / f"{t}.md").exists() if "/" in t else (CONCEPTS / f"{t}.md").exists())


def check(gestao: str) -> list[str]:
    ms, themes = meetings(gestao), load_themes(gestao)
    prob = input_problems(gestao, ms, themes)
    if any(not m["in_table"] or m["nro"] not in themes for m in ms) or any(
            t.get("tema") not in VOCABULARY for ts in themes.values() for t in ts):
        return prob                        # cannot render what the inputs do not define
    page = PAGE_DIR / f"{page_name(gestao)}.md"
    if not page.exists():
        return prob + [f"index page missing: {page.name} (run build)"]
    have = page.read_text(encoding="utf-8")
    for m in ms:
        sec = re.search(rf"^## {re.escape(_heading(m))}$(.*?)(?=^## |\Z)", have, re.M | re.S)
        if not sec:
            prob.append(f"page: no section for meeting {m['nro']}")
        elif decision_line(m) not in sec.group(1):
            got = re.search(r"\*\*Decisão:\*\*.*", sec.group(1))
            prob.append(f"page: decision of meeting {m['nro']} differs from the table "
                        f"(page: {got.group(0) if got else 'none'}; table: {decision_line(m)})")
    cl = concept_lines(gestao, ms, themes)
    texts = [have] + [l for l in cl.values()]
    for t in texts:
        for target in LINK.findall(t):
            if not _resolves(target):
                prob.append(f"link does not resolve: [[{target}]]")
    if have != render_page(gestao, ms, themes):
        prob.append(f"index page {page.name} differs from what build would write (stale)")
    for c, p in _concept_state(gestao, cl):
        if p.exists() and p.read_text(encoding="utf-8") != apply_line(p.read_text(encoding="utf-8"), gestao, cl.get(c)):
            prob.append(f"concept {c}: managed line is stale ({'expected' if c in cl else 'to be removed'})")
        elif not p.exists():
            prob.append(f"concept page {c} does not exist")
    return list(dict.fromkeys(prob))


def _concept_state(gestao: str, cl: dict) -> list[tuple[str, Path]]:
    """Every concept page that has, or should have, the managed line."""
    names = set(cl)
    mk = mark(gestao)
    for p in CONCEPTS.glob("*.md"):
        if mk in p.read_text(encoding="utf-8"):
            names.add(p.stem)
    return [(c, CONCEPTS / f"{c}.md") for c in sorted(names)]


# ── build ─────────────────────────────────────────────────────────────────────

def build(gestao: str) -> list[str]:
    """Writes the page and the concept lines; returns the problems that stopped it (nothing is
    written then)."""
    ms, themes = meetings(gestao), load_themes(gestao)
    prob = input_problems(gestao, ms, themes)
    if prob:
        return prob
    PAGE_DIR.mkdir(parents=True, exist_ok=True)
    (PAGE_DIR / f"{page_name(gestao)}.md").write_text(render_page(gestao, ms, themes), encoding="utf-8", newline="\n")
    cl = concept_lines(gestao, ms, themes)
    for c, p in _concept_state(gestao, cl):
        old = p.read_text(encoding="utf-8")
        new = apply_line(old, gestao, cl.get(c))
        if new != old:
            p.write_text(new, encoding="utf-8", newline="\n")
    return []


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    for n in ("build", "check"):
        s = sub.add_parser(n)
        s.add_argument("--gestao", required=True, choices=sorted(GESTOES))
    a = ap.parse_args()
    prob = build(a.gestao) if a.cmd == "build" else check(a.gestao)
    if prob:
        print("FAIL\n" + "\n".join(f"- {p}" for p in prob))
        sys.exit(1)
    print("built" if a.cmd == "build" else "PASS")


if __name__ == "__main__":
    main()
