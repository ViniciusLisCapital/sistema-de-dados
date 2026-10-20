"""
repository/ingestion/scripts/vault.py — the vault agent's deterministic helper, the vault's
equivalent of qc.py check. Reads the vault, writes nothing.

    uv run python repository/ingestion/scripts/vault.py --list [topic]
    uv run python repository/ingestion/scripts/vault.py check <topic> "<name>"
    uv run python repository/ingestion/scripts/vault.py concept [<slug> ...]    # concept pages (all if none)
    uv run python repository/ingestion/scripts/vault.py biblio <topic> "<name>"  # the tracker's bibliographic fields

The step after ingestion (SISTEMA_AGENTES.md II.I.v):

    obsidian/<topic>/clean_md/<name>.md               (written by /ingest)
      └─ /vault [topic] [file ...]  (vault agent)
           ├─ obsidian/<topic>/synthesis/<name>.md     (same name as its clean_md)
           ├─ obsidian/concepts/<slug>.md              (one folder for every area)
           └─ vault.py check → tracker.py

--list: a clean_md file at the top level of clean_md/ with no synthesis/<name>.md is pending.
  Skipped: clean_md/central_bank/ (the Copom ETL's documents, not a synthesis per file) and
  topics on hold in repository/ingestion/settings.yaml.

check: one synthesis note against its clean_md and the vault. Fails (exit 1) on
  - a template section or header field missing;
  - "Source file" not a link to obsidian/<topic>/clean_md/<name>.md;
  - a number not found in the clean_md text (see _numbers for what is compared); on the
    **Source:** line a number may also come from the tracker row's bibliographic fields (biblio);
  - a [[wikilink]] that resolves to no file (unless marked "(proposed)" right after it), or to
    two files with the same name (a synthesis note and its clean_md share a name, so links to
    either are written with the path from the vault root: [[<topic>/synthesis/<name>]]);
  - a concept the note links whose page does not link back to the note;
  - a number on a concept page's line that links the note (the patch) not in the note's clean_md.

concept: a concept page's numbers against the sources it links. A line that links synthesis
  notes is checked against their clean_md; a line that links none (Definition, Formal statement)
  against the clean_md of every note the page links. A mental model linked on the line stands for
  itself (its section numbers), and so does a note with no clean_md (Fleming 1962).
A pass is necessary, not sufficient: a small integer that appears anywhere in the text passes
whatever it means in the note. The judgment stays with the agent and the user.
"""

import argparse
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from run import OBSIDIAN  # noqa: E402
from settings import topics_on_hold  # noqa: E402

CONCEPTS = OBSIDIAN / "concepts"
NOT_TOPICS = {"concepts", "ciclos", "escrivao"}
SKIP_CLEAN = {"central_bank"}          # subfolders of clean_md/ that are not synthesized per file

FIELDS = ["Type", "Tags", "Source", "Language", "Source file"]
SECTIONS = ["Context and motivation", "Core argument / thesis", "Key mechanisms / model",
            "Main results / findings", "Limitations and caveats", "Connections"]

# [[target]], [[target|alias]], [[target#heading]]; inside a table the pipe is escaped as \|.
LINK = re.compile(r"\[\[([^\]|#]+?)\\?(?:#[^\]|]*)?(?:\\?\|[^\]]*)?\]\]")
PROPOSED = re.compile(r"\s*\(proposed\)", re.I)
SLUG = re.compile(r"^[a-z0-9]+(?:_[a-z0-9]+)*$")
NUM = re.compile(r"(?<![\d.,])\.?\d+(?:[.,]\d+)*")
YEAR_IN_STEM = re.compile(r"\d{4}")
# Section numbers of another vault file (a mental model's "sections 1.1–1.11", "§3.5"): they
# point into that file, not into the source.
SECTION_REF = re.compile(r"(?i)(?:\bsec(?:tions?|ção|ções|\.)|§)\s*\d+(?:\.\d+)*"
                         r"(?:\s*(?:[–,-]|and|to|e)\s*\d+(?:\.\d+)*)*")


# ── the vault ────────────────────────────────────────────────────────────────

def topics() -> list[str]:
    return sorted(d.name for d in OBSIDIAN.iterdir()
                  if d.is_dir() and (d / "clean_md").is_dir() and d.name not in NOT_TOPICS)


def scan(topic: str) -> list[dict]:
    """Every clean_md file at the top level, with state: done · pending · on_hold."""
    hold = topics_on_hold().get(topic)
    out = []
    for f in sorted((OBSIDIAN / topic / "clean_md").glob("*.md")):
        done = (OBSIDIAN / topic / "synthesis" / f.name).exists()
        state = "done" if done else ("on_hold" if hold else "pending")
        out.append({"topic": topic, "name": f.stem, "state": state})
    return out


def orphans(topic: str) -> list[str]:
    """Synthesis notes with no clean_md of the same name (written before the convention, or from
    a source that was never ingested)."""
    d = OBSIDIAN / topic / "synthesis"
    return sorted(n.stem for n in d.glob("*.md") if not (OBSIDIAN / topic / "clean_md" / n.name).exists()) \
        if d.is_dir() else []


def index() -> dict[str, list[Path]]:
    """note name (lower case) -> every .md file with that name, anywhere in the vault."""
    out: dict[str, list[Path]] = {}
    for p in OBSIDIAN.rglob("*.md"):
        if ".obsidian" not in p.parts:
            out.setdefault(p.stem.lower(), []).append(p)
    return out


def resolve(target: str, idx: dict[str, list[Path]]) -> tuple[str, Path | None]:
    """('ok', path) · ('missing', None) · ('ambiguous', None). Obsidian matches names without
    case; a target with a slash is a path from the vault root."""
    t = target.strip().rstrip("\\").strip()
    if t.lower().endswith(".md"):
        t = t[:-3]
    if "/" in t:
        p = OBSIDIAN / f"{t}.md"
        return ("ok", p) if p.exists() else ("missing", None)
    hits = idx.get(t.lower(), [])
    return ("ok", hits[0]) if len(hits) == 1 else ("ambiguous" if hits else "missing", None)


def links(text: str) -> list[tuple[int, str, bool]]:
    """(line number, target, marked proposed) for every wikilink."""
    out = []
    for n, line in enumerate(text.splitlines(), 1):
        for m in LINK.finditer(line):
            out.append((n, m.group(1), bool(PROPOSED.match(line, m.end()))))
    return out


# ── numbers ──────────────────────────────────────────────────────────────────

def _forms(tok: str) -> set[str]:
    """The ways one number can be written: 1,000 = 1000; 0,5 = 0.5 (Portuguese); .73 = 0.73;
    0.70 = 0.7. The sign is ignored (OCR and fonts lose or change the minus)."""
    out = {tok, "0" + tok if tok.startswith(".") else tok}
    if "," in tok and "." not in tok:
        out |= {tok.replace(",", ""), tok.replace(",", ".")}
    elif "," in tok:
        out |= {tok.replace(",", ""), tok.replace(".", "").replace(",", ".")}
    elif re.fullmatch(r"\d{1,3}(\.\d{3})+", tok):
        out.add(tok.replace(".", ""))
    for f in list(out):
        if "." in f:
            g = f.rstrip("0").rstrip(".")
            out.add(g)
            if f.startswith("0."):
                out.add(f[1:])
    return out


def source_numbers(text: str) -> set[str]:
    out: set[str] = set()
    for tok in NUM.findall(text):
        out |= _forms(tok)
    return out


def _numbers(note: str, name: str, years: set[str] = frozenset()) -> list[tuple[int, str, str]]:
    """Numbers of the note to look for in the clean_md: (line, number, line text).
    Not compared: the frontmatter, the H1 title, wikilink targets (file names carry years),
    list and heading numbering (1., 2.), the year in the source's own file name, and the year
    of a source linked on the same line ("Itaú (2025) restates it" next to its link)."""
    own_years = set(YEAR_IN_STEM.findall(name)) | set(years)
    out = []
    in_front = False
    for n, line in enumerate(note.splitlines(), 1):
        if n == 1 and line.strip() == "---":
            in_front = True
            continue
        if in_front:
            in_front = line.strip() != "---"
            continue
        if line.startswith("# "):
            continue
        linked_years = {y for m in LINK.finditer(line) for y in YEAR_IN_STEM.findall(m.group(1))}
        body = LINK.sub(" ", line)
        body = re.sub(r"^\s*(?:#{1,6}\s+)?(?:\d+\.)+\s", " ", body)       # "1. ", "## 2.3 "
        body = SECTION_REF.sub(" ", body)                                   # "Verde sections 1.1–1.11"
        for m in NUM.finditer(body):
            tok = m.group(0)
            if tok.strip(".") in own_years | linked_years:
                continue                 # a year that dates this source, or a source linked on the line
            if len(tok) == 2 and re.search(r"\d{4}\s?[–-]\s?$", body[:m.start()]):
                continue                 # "1997–98": the short end of a year range
            out.append((n, tok, line.strip()))
    return out


# ── check ────────────────────────────────────────────────────────────────────

def check(topic: str, name: str, meta: dict | None = None) -> dict:
    """meta: the tracker's bibliographic fields for the file (biblio); read from the workbook
    when not given."""
    name = name[:-3] if name.endswith(".md") else name
    note_p = OBSIDIAN / topic / "synthesis" / f"{name}.md"
    clean_p = OBSIDIAN / topic / "clean_md" / f"{name}.md"
    res: dict = {"topic": topic, "name": name, "problems": []}
    prob = res["problems"]
    if not note_p.exists():
        prob.append(f"no synthesis note: {note_p.relative_to(OBSIDIAN.parent)}")
        res["ok"] = False
        return res
    if not clean_p.exists():
        prob.append(f"no clean_md of the same name: {clean_p.relative_to(OBSIDIAN.parent)}")
    note = note_p.read_text(encoding="utf-8")
    idx = index()

    # template
    heads = {h.strip() for h in re.findall(r"^##\s+(.+?)\s*$", note, re.M)}
    res["missing_sections"] = [s for s in SECTIONS if s not in heads]
    res["missing_fields"] = [f for f in FIELDS if not re.search(rf"^\*\*{re.escape(f)}:\*\*", note, re.M)]
    prob += [f"section missing: ## {s}" for s in res["missing_sections"]]
    prob += [f"field missing: **{f}:**" for f in res["missing_fields"]]

    # Source file
    sf = re.search(r"^\*\*Source file:\*\*(.*)$", note, re.M)
    if sf:
        targets = [m.group(1) for m in LINK.finditer(sf.group(1))]
        state, p = resolve(targets[0], idx) if len(targets) == 1 else ("", None)
        if p is None or p.resolve() != clean_p.resolve():
            prob.append(f"Source file must be [[{topic}/clean_md/{name}]], found: {sf.group(1).strip() or 'nothing'}")

    # numbers
    if clean_p.exists():
        have = source_numbers(clean_p.read_text(encoding="utf-8"))
        if meta is None:
            meta = biblio(topic, name)
        have_biblio = have | source_numbers(" ".join(str(v) for v in meta.values()))
        res["numbers_checked"] = 0
        res["numbers_not_in_source"] = []
        for n, tok, line in _numbers(note, name):
            res["numbers_checked"] += 1
            if not (_forms(tok) & (have_biblio if line.startswith("**Source:**") else have)):
                res["numbers_not_in_source"].append(f"line {n}: {tok}  | {line[:110]}")
        prob += [f"number not in the clean_md, {x}" for x in res["numbers_not_in_source"]]

    # links
    res["links"] = 0
    res["proposed"] = []
    concepts = []
    for n, target, proposed in links(note):
        res["links"] += 1
        state, p = resolve(target, idx)
        if state == "ok":
            if p.parent == CONCEPTS:
                concepts.append((n, target, p))
        elif state == "ambiguous":
            prob.append(f"line {n}: [[{target}]] matches several files — write the path from the vault root")
        elif proposed:
            res["proposed"].append(target.strip())
            if not SLUG.match(target.strip()):
                prob.append(f"line {n}: proposed concept [[{target}]] is not a snake_case slug")
        else:
            prob.append(f"line {n}: [[{target}]] resolves to no file (create it, or mark it (proposed))")

    # concepts link back
    res["concepts"] = sorted({p.stem for _, _, p in concepts})
    for n, target, p in concepts:
        if not SLUG.match(p.stem):
            prob.append(f"line {n}: concept page {p.name} is not a snake_case slug")
        back = [resolve(t, idx)[1] for _, t, _ in links(p.read_text(encoding="utf-8"))]
        if not any(b is not None and b.resolve() == note_p.resolve() for b in back):
            prob.append(f"concepts/{p.name} does not link back to [[{topic}/synthesis/{name}]]")
        for x in concept_numbers(p, idx, only=note_p):
            prob.append(f"number in concepts/{p.name} not in the clean_md, {x}")
    prob[:] = list(dict.fromkeys(prob))
    res["ok"] = not prob
    return res


# ── concept pages ──────────────────────────────────────────────────────────────

def _source_of(note_p: Path) -> Path:
    """Where the numbers of a file a concept page links come from: a synthesis note's clean_md,
    or the file itself — a mental model (its section numbers, "3.2–3.4") or a note with no
    clean_md (Fleming 1962, written before ingestion)."""
    clean = note_p.parent.parent / "clean_md" / note_p.name
    return clean if note_p.parent.name == "synthesis" and clean.exists() else note_p


def concept_numbers(page: Path, idx: dict[str, list[Path]], only: Path | None = None) -> list[str]:
    """Numbers of a concept page not found in the sources it links: 'line n: number | text'.
    only: check just the lines that link that synthesis note (the patch a vault run adds)."""
    text = page.read_text(encoding="utf-8")
    per_line: dict[int, list[Path]] = {}
    for n, target, _ in links(text):
        _, p = resolve(target, idx)
        if p is not None and p.parent.name in ("synthesis", "mental_models"):
            per_line.setdefault(n, []).append(p.resolve())
    notes = {p for ps in per_line.values() for p in ps}
    cache: dict[Path, set[str]] = {}

    def have(ps) -> set[str]:
        out: set[str] = set()
        for p in ps:
            if p not in cache:
                cache[p] = source_numbers(_source_of(p).read_text(encoding="utf-8"))
            out |= cache[p]
        return out

    years = {y for p in notes for y in YEAR_IN_STEM.findall(p.stem)}
    bad = []
    for n, tok, line in _numbers(text, "", years):
        linked = per_line.get(n, [])
        if only is not None and only.resolve() not in linked:
            continue
        if not (_forms(tok) & have(linked or notes)):
            bad.append(f"line {n}: {tok}  | {line[:110]}")
    return bad


def check_concept(slug: str) -> dict:
    p = CONCEPTS / f"{slug.removesuffix('.md')}.md"
    if not p.exists():
        return {"slug": slug, "ok": False, "problems": [f"no concept page: concepts/{p.name}"]}
    bad = concept_numbers(p, index())
    return {"slug": p.stem, "ok": not bad, "problems": [f"number not in the linked sources, {x}" for x in bad]}


# ── bibliographic fields from the tracker ────────────────────────────────────

BIBLIO = ("Name", "Autor/Company", "Date", "Type")


def biblio(topic: str, name: str) -> dict:
    """The file's bibliographic fields in the area's Qual tab: title, author, date, type. The
    Source line may take them when the clean_md lacks them (a book chapter with no title page).
    Nothing else of the tracker reaches the vault agent: a synthesis is about the material, not
    about the questions an area wants answered (decided 2026-10-20). {} when the workbook or
    the row is missing. Read-only."""
    try:
        import openpyxl
        from tracker import TAB, TRACKER
        wb = openpyxl.load_workbook(TRACKER, read_only=True)
    except Exception:
        return {}
    tab = TAB.get(topic, f"Qual - {topic.replace('_', ' ').title()}")
    if tab not in wb.sheetnames:
        return {}
    head = None
    for r in wb[tab].iter_rows(values_only=True):
        if head is None:
            head = [str(c or "") for c in r]
            continue
        files = str(r[head.index("File")] or "").splitlines() if "File" in head else []
        if name in (f.strip() for f in files):
            return {k: r[head.index(k)] for k in BIBLIO if k in head and r[head.index(k)] not in (None, "")}
    return {}


# ── command line ─────────────────────────────────────────────────────────────

def cmd_list(only: str | None) -> None:
    for t in ([only] if only else topics()):
        rows = scan(t)
        count = {s: sum(1 for r in rows if r["state"] == s) for s in ("done", "pending", "on_hold")}
        print(f"{t}: {len(rows)} clean_md · " + " · ".join(f"{k.replace('_', ' ')} {v}" for k, v in count.items() if v)
              + ("" if not (OBSIDIAN / t / "clean_md" / "central_bank").is_dir() else " · skipped: clean_md/central_bank/"))
        if t in topics_on_hold():
            print(f"   on hold: {topics_on_hold()[t]}")
        for r in rows:
            if r["state"] == "pending":
                print(f"   pending          {r['name']}")
        for o in orphans(t):
            print(f"   no clean_md      synthesis/{o}.md")


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8")       # the Windows console codepage loses "–", "ç"
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--list", nargs="?", const="", metavar="topic", help="clean_md files with no synthesis note")
    sub = ap.add_subparsers(dest="cmd")
    c = sub.add_parser("check", help="check one synthesis note")
    c.add_argument("topic")
    c.add_argument("name", help="file name without .md (the same for the clean_md and the note)")
    k = sub.add_parser("concept", help="check concept pages' numbers against the sources they link")
    k.add_argument("slugs", nargs="*", help="concept slugs; none = every page")
    x = sub.add_parser("biblio", help="the tracker's bibliographic fields for one file (read-only)")
    x.add_argument("topic")
    x.add_argument("name")
    a = ap.parse_args()
    if a.list is not None:
        if a.list and a.list not in topics():
            sys.exit(f"unknown topic {a.list!r}; existing: {', '.join(topics())}")
        cmd_list(a.list or None)
        return
    if a.cmd == "check":
        res = check(a.topic, a.name)
        print(json.dumps({k: v for k, v in res.items() if k != "problems"}, ensure_ascii=False, indent=1))
        print("\n" + ("PASS" if res["ok"] else "FAIL\n" + "\n".join(f"- {p}" for p in res["problems"])))
        sys.exit(0 if res["ok"] else 1)
    if a.cmd == "concept":
        slugs = a.slugs or sorted(p.stem for p in CONCEPTS.glob("*.md"))
        failed = 0
        for slug in slugs:
            r = check_concept(slug)
            failed += not r["ok"]
            print(f"{'PASS' if r['ok'] else 'FAIL'}  {r['slug']}" + "".join(f"\n   - {x}" for x in r["problems"]))
        print(f"\n{len(slugs) - failed}/{len(slugs)} pass")
        sys.exit(1 if failed else 0)
    if a.cmd == "biblio":
        print(json.dumps(biblio(a.topic, a.name[:-3] if a.name.endswith(".md") else a.name),
                         ensure_ascii=False, indent=1, default=str))
        return
    ap.print_help()


if __name__ == "__main__":
    main()
