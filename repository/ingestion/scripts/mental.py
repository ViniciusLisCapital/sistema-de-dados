"""
repository/ingestion/scripts/mental.py — the mental-model agent's deterministic helper.

    uv run python repository/ingestion/scripts/mental.py --list
    uv run python repository/ingestion/scripts/mental.py begin <manager> <area> [--n N] [letter ...]
    uv run python repository/ingestion/scripts/mental.py check <manager> <area>
    uv run python repository/ingestion/scripts/mental.py packet <manager> <area>
    uv run python repository/ingestion/scripts/mental.py done <manager> <area> [--accept 4.4:C2 ...]
    uv run python repository/ingestion/scripts/mental.py abort <manager> <area>
    uv run python repository/ingestion/scripts/mental.py audit <manager> <area>
    uv run python repository/ingestion/scripts/mental.py seed <manager> <area> <from> <to>

A document is one manager x one area (obsidian/<area>/mental_models/<manager>_<code>_mental_models.md),
built from that manager's letters in repository/mental_model/ (mental_models.yaml says where). It
grows a few letters per run, in date order, and each run is bracketed by this script:

  begin   picks the next letters (date order, inside the document's range, up to a word budget),
          takes a snapshot of the document and prints the files to read. One open run per document.
  check   compares the document with the snapshot. Entries may be REPACKED — rewritten as one
          coherent text that takes in what the new letters add — but nothing they held may go.
          Fails (exit 1) on
            - material lost: an entry or cluster number that disappears (other files cite them
              by number), an existing quote no longer word for word in its block, a dated
              application ("- **Jul/2019** ...") whose date lead is gone, a number gone from its
              block (the About section's counts excepted), a [[wikilink]] gone;
            - an entry rewritten with no new dated application in it: a run repacks only the
              entries its letters add to;
            - a repacked block keeping under 75% of its words (under 90%: a warning to read it);
            - new material not from this run's letters: a quote (a quoted span of 4+ words, or a
              blockquote line) not found word for word in them, a number not in them (dates,
              years and the document's own section numbers are not compared);
            - a new [[wikilink]] that resolves to no file, or to two;
            - a framework entry ("## 2.3 ...") without "What it is" and "How <manager> applied
              it" (or the Portuguese labels), or a document without About and Connections;
            - the writer's claims file (ledger/.<document>.claims.json) missing, or not covering
              exactly the blocks repacked and added: per block, the old text cut into statements
              (C1...) and the new statements (N1...), each tied to a letter of the run.
  packet  what the independent reviewer reads: per block, the old text, the new text and the
          claims; the run's letters; the document's sha. Requires a passing check.
  done    requires a passing check AND the reviewer's verdicts (ledger/.<document>.review.json) on
          the current version of the document (same sha): every old claim kept or sharpened, cited
          word for word in the new text; every new claim supported, with its evidence word for word
          in a letter; nothing in uncovered_old or extra. --accept lets through verdicts the USER
          accepted. Then writes the letters to ledger/<document>.tsv, appends the verdict table to
          ledger/<document>.log.md, and drops the run's files. A letter with nothing for the area
          still goes in the ledger.
  abort   drops the open run's files, the ledger unchanged (the document is not restored).
  audit   the whole document's quotes against the manager's whole corpus. Read-only; it reports
          on documents written before this script, it does not gate anything.
  seed    writes letters dated <from>..<to> (YYYY-MM or YYYY-MM-DD) to the ledger as read
          before the ledger existed. For documents built before this script.

The script sees words, quotes, dates and numbers; meaning ("fortalece" -> "enfraquece") is the
reviewer's, and the log keeps every verdict so the user can audit both.
"""

import argparse
import datetime as dt
import json
import re
import sys
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))
from run import OBSIDIAN, REPOSITORY  # noqa: E402
from vault import LINK, NUM, _forms, index, resolve, source_numbers  # noqa: E402

MM = REPOSITORY / "mental_model"
CONFIG = MM / "mental_models.yaml"
LEDGER = MM / "ledger"

WORD_BUDGET = 18_000        # words of letters per run, so the agent reads every one in full
MAX_LETTERS = 10

ABOUT = re.compile(r"^##\s+(About this document|Sobre este documento)\s*$")
NOTES = re.compile(r"^##\s+(Notes for the next processing pass|Notas para a próxima passada)\s*$", re.I)
CONNECTIONS = re.compile(r"^##\s+Connections\s*$")
ENTRY = re.compile(r"^##\s+(\d+\.\d+)\s")
HEADING_ID = re.compile(r"^#{1,3}\s+(\d+(?:\.\d+)*)[.\s]", re.M)
WHAT = re.compile(r"^\*\*(What it is|O que é):\*\*", re.M)
HOW = re.compile(r"^\*\*(How .+ applied it|Como a? ?.+ aplic(ou|a)):\*\*", re.M)

_MON = (r"(?:jan|fev|feb|mar|abr|apr|mai|may|jun|jul|ago|aug|set|sep|out|oct|nov|dez|dec)"
        r"[a-zç]*\.?")
DATES = re.compile(
    rf"(?i)\b\d{{1,2}}\s+(?:de\s+)?{_MON}(?:\s+(?:de\s+)?\d{{4}})?"     # 31 Jan 2025, 3 de março de 2020
    rf"|\b{_MON}\s*/\s*\d{{2,4}}\b"                                     # Jul/2019, set/20
    rf"|\b{_MON}\s+(?:de\s+)?\d{{4}}"                                   # March 2025, março de 2020
    r"|\b\d{1,2}/\d{1,2}/\d{2,4}\b|\b\d{1,2}/\d{4}\b"                   # 31/08/2026, 07/2019
    r"|\b(?:19|20)\d{2}s?\s*[–-]\s*(?:19|20)?\d{2}\b"                    # 2019–2020, 1997-98
    r"|\b(?:19|20)\d{2}s?\b"                                            # 2008, 1970s
    r"|\b[1-4][TQ]\s?\d{2,4}\b|\bQ[1-4]\b|\bH[12]\b")                   # 1T25, Q1, H2
QUOTED = re.compile(r"“([^”]*)”|\"([^\"]*)\"")      # marks consumed in pairs, so prose between two quotes is never one
ELLIPSIS = re.compile(r"\s*(?:\[\s*(?:\.\.\.|…)\s*\]|\(\s*(?:\.\.\.|…)\s*\)|\.\.\.|…|\[[^\]]*\])\s*")


# ── configuration, corpus, ledger ────────────────────────────────────────────

def config() -> dict:
    return yaml.safe_load(CONFIG.read_text(encoding="utf-8"))


def doc_name(cfg: dict, manager: str, area: str) -> str:
    if manager not in cfg["managers"]:
        sys.exit(f"unknown manager {manager!r}; configured: {', '.join(cfg['managers'])}")
    if area not in cfg["areas"]:
        sys.exit(f"unknown area {area!r}; configured: {', '.join(cfg['areas'])}")
    return f"{manager}_{cfg['areas'][area]}_mental_models"


def doc_path(cfg: dict, manager: str, area: str) -> Path:
    return OBSIDIAN / area / "mental_models" / f"{doc_name(cfg, manager, area)}.md"


def letters(cfg: dict, manager: str) -> tuple[list[dict], list[str]]:
    """Every letter of the manager, in date order: {name, path, date}. And the corpus folders
    that do not exist yet."""
    out, missing = [], []
    for c in cfg["managers"][manager]["corpora"]:
        d = MM / c["path"]
        if not d.is_dir() or not any(d.glob("*.md")):
            missing.append(c["path"])
            continue
        rx = re.compile(c["date"])
        for f in d.glob("*.md"):
            m = rx.search(f.stem)
            if not m:
                continue                          # notes kept next to the letters (CURATION_SCOPE.md)
            g = m.groupdict()
            out.append({"name": f.stem, "path": f,
                        "date": dt.date(int(g["y"]), int(g["m"]), int(g.get("d") or 1))})
    out.sort(key=lambda x: (x["date"], x["name"]))
    return out, missing


def _parse_day(s: str, end: bool = False) -> dt.date:
    p = [int(x) for x in str(s).split("-")]
    if len(p) == 3:
        return dt.date(*p)
    if not end:
        return dt.date(p[0], p[1], 1)
    nxt = dt.date(p[0] + (p[1] == 12), p[1] % 12 + 1, 1)
    return nxt - dt.timedelta(days=1)


def start_of(cfg: dict, name: str) -> dt.date | None:
    s = (cfg.get("documents") or {}).get(name, {}).get("start")
    return _parse_day(s) if s else None


def ledger_path(name: str) -> Path:
    return LEDGER / f"{name}.tsv"


def ledger(name: str) -> dict[str, str]:
    p = ledger_path(name)
    if not p.exists():
        return {}
    out = {}
    for line in p.read_text(encoding="utf-8").splitlines():
        if line and not line.startswith("#"):
            letter, _, when = line.partition("\t")
            out[letter] = when
    return out


def ledger_add(name: str, names: list[str], when: str) -> None:
    p = ledger_path(name)
    LEDGER.mkdir(exist_ok=True)
    head = "" if p.exists() else "# letter\tread on (written by mental.py done; seeded = read before the ledger existed)\n"
    with p.open("a", encoding="utf-8") as fh:
        fh.write(head + "".join(f"{n}\t{when}\n" for n in names))


def run_path(name: str) -> Path:
    return LEDGER / f".{name}.run.json"


def state(cfg: dict, manager: str, area: str) -> dict:
    name = doc_name(cfg, manager, area)
    all_, missing = letters(cfg, manager)
    done = ledger(name)
    start = start_of(cfg, name)
    in_range = [x for x in all_ if start is None or x["date"] >= start]
    return {"name": name, "path": doc_path(cfg, manager, area), "missing": missing, "start": start,
            "all": all_, "done": [x for x in all_ if x["name"] in done],
            "pending": [x for x in in_range if x["name"] not in done],
            "before_start": [x for x in all_ if x not in in_range and x["name"] not in done],
            "unknown_in_ledger": sorted(set(done) - {x["name"] for x in all_})}


# ── text matching ────────────────────────────────────────────────────────────

def norm(s: str) -> str:
    s = s.replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"').replace("«", '"')
    s = s.replace("»", '"').replace("–", "-").replace("—", "-").replace(" ", " ")
    s = re.sub(r"[*_`#>|\"']", " ", s)                      # quote marks too: nested quotes swap ' and "
    s = re.sub(r"(\w)-\s*\n\s*(\w)", r"\1\2", s)              # a word broken over two lines
    return re.sub(r"\s+", " ", s).strip().lower()


def quotes(line: str) -> list[str]:
    """The quotes in one line of the document: quoted spans of 4+ words; on a blockquote line
    with no quote marks, the whole line minus a trailing (date) attribution."""
    if line.lstrip().startswith("#"):
        return []                                          # a heading names a framework, it does not quote
    found = [q for q in (a or b for a, b in QUOTED.findall(line)) if len(q.split()) >= 4]
    if not found and line.lstrip().startswith(">"):
        body = re.sub(r"\s*[—-]?\s*\([^)]*\)\s*$", "", line.lstrip()[1:].strip())
        if len(body.split()) >= 4:
            found = [body]
    return found


def quote_found(q: str, text_n: str) -> bool:
    """Every fragment of 3+ words (split at ellipses and [inserted words]) is in the text."""
    frags = [f for f in (norm(x).strip(" .,;:'\"") for x in ELLIPSIS.split(q)) if len(f.split()) >= 3]
    return bool(frags) and all(f in text_n for f in frags)


def numbers(line: str, own_ids: set[str]) -> list[str]:
    body = LINK.sub(" ", line)
    body = re.sub(r"^\s*(?:#{1,6}\s+)?(?:\d+\.)+\d*\s", " ", body)       # "## 2.3 ", "1. "
    body = DATES.sub(" ", body)
    out = []
    for m in NUM.finditer(body):
        tok = m.group(0).strip(".")
        if tok and tok not in own_ids:
            out.append(tok)
    return out


def structure(text: str) -> list[str]:
    prob = []
    lines = text.splitlines()
    if not lines or not lines[0].startswith("# "):
        prob.append("the first line must be the H1 title")
    if not any(ABOUT.match(ln) for ln in lines):
        prob.append("section missing: ## About this document (or ## Sobre este documento)")
    if not any(CONNECTIONS.match(ln) for ln in lines):
        prob.append("section missing: ## Connections")
    starts = [i for i, ln in enumerate(lines) if ln.startswith("#")]
    for i, ln in enumerate(lines):
        m = ENTRY.match(ln)
        if not m:
            continue
        end = next((j for j in starts if j > i), len(lines))
        block = "\n".join(lines[i:end])
        if not WHAT.search(block) and not HOW.search(block) and re.search(r"\b\d+\.\d+\b", "\n".join(lines[i + 1:end])):
            continue                     # a pointer entry: "Documented in full under 1.4"
        if not WHAT.search(block):
            prob.append(f"entry {m.group(1)} has no **What it is:** / **O que é:**")
        if not HOW.search(block):
            prob.append(f"entry {m.group(1)} has no **How <manager> applied it:** / **Como a <gestora> aplicou:**")
    return prob


# ── commands ─────────────────────────────────────────────────────────────────

def _fmt(x: dict) -> str:
    return f"{x['date']:%Y-%m-%d}  {x['name']}"


def cmd_list(cfg: dict) -> None:
    docs = {(m, a) for m in cfg["managers"] for a in cfg["areas"]
            if doc_path(cfg, m, a).exists() or ledger_path(doc_name(cfg, m, a)).exists()}
    print("Documents")
    for m, a in sorted(docs, key=lambda x: (x[1], x[0])):
        s = state(cfg, m, a)
        done = s["done"]
        span = f"{done[0]['date']:%Y-%m} → {done[-1]['date']:%Y-%m}" if done else "none read"
        line = (f"  {a}/{s['name']}: read {len(done)} ({span}) · pending {len(s['pending'])}"
                + (f" · before start {s['start']:%Y-%m}: {len(s['before_start'])}" if s["before_start"] else "")
                + (" · RUN OPEN" if run_path(s["name"]).exists() else "")
                + ("" if s["path"].exists() else " · document file missing"))
        print(line)
        if s["missing"]:
            print(f"      no text yet: {', '.join(s['missing'])} — run /ingest mental_model/<folder> first")
        if s["unknown_in_ledger"]:
            print(f"      in the ledger but not in the corpus: {', '.join(s['unknown_in_ledger'][:5])}"
                  + (" …" if len(s["unknown_in_ledger"]) > 5 else ""))
        for x in s["pending"][:3]:
            print(f"      next  {_fmt(x)}")
    print("\nCorpora")
    for m, mc in cfg["managers"].items():
        all_, missing = letters(cfg, m)
        span = f"{all_[0]['date']:%Y-%m} → {all_[-1]['date']:%Y-%m}" if all_ else "—"
        print(f"  {m}: {len(all_)} letters ({span})" + (f" · no text: {', '.join(missing)}" if missing else ""))


def cmd_begin(cfg: dict, manager: str, area: str, n: int | None, chosen: list[str]) -> None:
    s = state(cfg, manager, area)
    rp = run_path(s["name"])
    if rp.exists():
        sys.exit(f"a run is already open for {s['name']}: check and done it, or abort it")
    if s["missing"] and not s["all"]:
        sys.exit(f"no text for {manager}: {', '.join(s['missing'])} — run /ingest mental_model/<folder> first")
    if chosen:
        by = {x["name"]: x for x in s["all"]}
        bad = [c for c in chosen if c.removesuffix(".md") not in by]
        if bad:
            sys.exit(f"not in {manager}'s corpus: {', '.join(bad)}")
        batch = [by[c.removesuffix(".md")] for c in chosen]
    else:
        batch, words = [], 0
        for x in s["pending"]:
            w = len(x["path"].read_text(encoding="utf-8").split())
            if batch and (len(batch) >= (n or MAX_LETTERS) or (n is None and words + w > WORD_BUDGET)):
                break
            batch.append(x)
            words += w
    if not batch:
        print(f"{s['name']}: nothing pending")
        return
    snap = s["path"].read_text(encoding="utf-8") if s["path"].exists() else ""
    LEDGER.mkdir(exist_ok=True)
    rp.write_text(json.dumps({"document": str(s["path"].relative_to(OBSIDIAN.parent)),
                              "letters": [str(x["path"].relative_to(OBSIDIAN.parent)) for x in batch],
                              "names": [x["name"] for x in batch], "snapshot": snap,
                              "opened": dt.datetime.now().isoformat(timespec="seconds")},
                             ensure_ascii=False, indent=1), encoding="utf-8")
    root = OBSIDIAN.parent
    print(f"document: {s['path'].relative_to(root)}" + ("" if snap else "   (NEW — create it)"))
    print(f"claims of every block you repack or add go to: {side_path(s['name'], 'claims').relative_to(root)}")
    print(f"letters this run ({len(batch)}, in this order; pending after this run: {len(s['pending']) - len(batch)}):")
    for x in batch:
        w = len(x["path"].read_text(encoding="utf-8").split())
        print(f"  {x['date']:%Y-%m-%d}  {x['path'].relative_to(root)}   ({w:,} words)")


def _open_run(cfg: dict, manager: str, area: str) -> tuple[dict, dict]:
    s = state(cfg, manager, area)
    rp = run_path(s["name"])
    if not rp.exists():
        sys.exit(f"no open run for {s['name']}: start one with begin")
    return s, json.loads(rp.read_text(encoding="utf-8"))


def blocks(text: str) -> dict[str, dict]:
    """The document cut at every # and ## heading. Key: "title" for what precedes the first
    heading after the H1; the entry or cluster number ("2.3", "2") when the heading has one, so a
    retitled entry is still the same entry; otherwise the heading's text ("About this document").
    kind: about · notes · entry · other."""
    out: dict[str, dict] = {}
    key, kind, buf = "title", "title", []

    def flush():
        out[key] = {"kind": kind, "text": "\n".join(buf)}

    for i, ln in enumerate(text.splitlines()):
        if i > 0 and re.match(r"^#{1,2}\s", ln):
            flush()
            num = re.match(r"^#{1,2}\s+(\d+(?:\.\d+)?)[.\s]", ln)
            key = num.group(1) if num else re.sub(r"^#+\s*", "", ln).strip()
            kind = ("about" if ABOUT.match(ln) else "notes" if NOTES.match(ln)
                    else "entry" if ENTRY.match(ln) else "other")
            buf = []
        buf.append(ln)
    flush()
    return out


LEAD = re.compile(r"^\s*-\s+\*\*([^*]+)\*\*", re.M)          # "- **Jul/2019** ...": a dated application


def material(block: str, own_ids: set[str]) -> dict:
    lines = block.splitlines()
    return {"quotes": [q for ln in lines for q in quotes(ln)],
            "leads": {norm(m) for m in LEAD.findall(block)},
            "numbers": [t for ln in lines for t in numbers(ln, own_ids)],
            "links": {m.group(1).strip() for m in LINK.finditer(block)},
            "words": {w for w in re.findall(r"[a-zà-ú]{5,}", norm(block))}}


def check(cfg: dict, manager: str, area: str) -> dict:
    s, run = _open_run(cfg, manager, area)
    root = OBSIDIAN.parent
    res: dict = {"document": run["document"], "letters": run["names"], "problems": [], "warnings": []}
    prob, warn = res["problems"], res["warnings"]
    if not s["path"].exists():
        prob.append("the document does not exist")
        res["ok"] = False
        return res
    new = s["path"].read_text(encoding="utf-8")
    old = run["snapshot"]
    prob += structure(new)
    letters_txt = " ".join((root / p).read_text(encoding="utf-8") for p in run["letters"])
    text_n, have = norm(letters_txt), source_numbers(letters_txt)
    own_ids = set(HEADING_ID.findall(new)) | set(HEADING_ID.findall(old))
    ob, nb = blocks(old) if old else {}, blocks(new)
    old_n, new_n = norm(old), norm(new)
    old_nums = {f for t in numbers(old, own_ids) for f in _forms(t)} if old else set()
    idx = index()
    res.update(quotes_checked=0, numbers_checked=0, repacked=[], changed=[], added=[])

    # 1. nothing that was there is lost: every block, quote, dated application, number and link
    for k, o in ob.items():
        if k not in nb:
            prob.append(f"section {k!r} is gone (entries and clusters keep their number; their content can be repacked, not removed)")
            continue
        n = nb[k]
        om, nm = material(o["text"], own_ids), material(n["text"], own_ids)
        nt = norm(n["text"])
        for q in om["quotes"]:
            if not quote_found(q, nt):
                prob.append(f"{k}: an existing quote is gone or altered: \"{q[:90]}\"")
        for lead in om["leads"] - nm["leads"]:
            prob.append(f"{k}: the dated application **{lead}** is gone (repack its text, keep its date lead)")
        if o["kind"] not in ("about", "title", "notes"):
            nforms = {f for t in nm["numbers"] for f in _forms(t)}
            for t in dict.fromkeys(om["numbers"]):
                if not (_forms(t) & nforms):
                    prob.append(f"{k}: the number {t} is gone")
        if norm(o["text"]) != nt and o["kind"] in ("entry", "other"):
            cover = len(om["words"] & nm["words"]) / max(len(om["words"]), 1)
            res["repacked"].append(f"{k} ({cover:.0%} of its words kept)")
            res["changed"].append(k)
            if o["kind"] == "entry" and not (nm["leads"] - om["leads"]):
                prob.append(f"{k}: rewritten without a new dated application from this run — repack only the entries this run adds to")
            if cover < 0.75:
                prob.append(f"{k}: only {cover:.0%} of its words survive the repack — material looks dropped")
            elif cover < 0.9:
                warn.append(f"{k}: {cover:.0%} of its words survive the repack — read it against the old text")
    old_links = {m.group(1).strip() for m in LINK.finditer(old)}
    new_links = {m.group(1).strip() for m in LINK.finditer(new)}
    for t in sorted(old_links - new_links):
        prob.append(f"the link [[{t}]] is gone")

    # 2. everything new comes from this run's letters
    res["added"] = [k for k in nb if k not in ob and nb[k]["kind"] in ("entry", "other")]
    res["_kinds"] = {k: v["kind"] for k, v in nb.items()}
    for k, n in nb.items():
        for q in material(n["text"], own_ids)["quotes"]:
            if quote_found(q, old_n):
                continue                                   # an existing quote, moved or kept
            res["quotes_checked"] += 1
            if not quote_found(q, text_n):
                prob.append(f"{k}: new quote not in this run's letters: \"{q[:90]}\"")
        if n["kind"] in ("about", "title", "notes"):
            continue
        for t in dict.fromkeys(material(n["text"], own_ids)["numbers"]):
            if _forms(t) & old_nums:
                continue
            res["numbers_checked"] += 1
            if not (_forms(t) & have):
                prob.append(f"{k}: new number {t} not in this run's letters")
    for t in sorted(new_links - old_links):
        st, _ = resolve(t, idx)
        if st != "ok":
            prob.append(f"[[{t}]] {'matches several files' if st == 'ambiguous' else 'resolves to no file'}")
    prob += claims_problems(s["name"], res, run["names"])
    prob[:] = list(dict.fromkeys(prob))
    res["ok"] = not prob
    res.update(_ob=ob, _nb=nb, _text_n=text_n, _new=new)
    return res


# ── the claims (writer) and the review (an independent agent) ────────────────

def side_path(name: str, kind: str) -> Path:
    """kind: claims · review — the run's two hand-offs, next to the snapshot, removed by done/abort."""
    return LEDGER / f".{name}.{kind}.json"


def log_path(name: str) -> Path:
    return LEDGER / f"{name}.log.md"


def _load(p: Path) -> dict | None:
    if not p.exists():
        return None
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        return {"_error": f"{p.name} is not valid JSON: {e}"}


def claims_problems(name: str, res: dict, letters_: list[str]) -> list[str]:
    """Every repacked or new block has its claims: the old text cut into numbered statements
    (C1, C2, ...) and the new statements (N1, ...) each tied to a letter of this run."""
    need = res["changed"] + res["added"]
    if not need:
        return []
    cl = _load(side_path(name, "claims"))
    if cl is None:
        return [f"no claims file for the blocks changed or added ({', '.join(need)}): "
                f"write {side_path(name, 'claims').relative_to(OBSIDIAN.parent)}"]
    if "_error" in cl:
        return [cl["_error"]]
    prob = []
    for k in need:
        c = cl.get(k)
        if not isinstance(c, dict):
            prob.append(f"claims: no entry for block {k}")
            continue
        old, new = c.get("old") or {}, c.get("new") or {}
        if k in res["changed"] and not old:
            prob.append(f"claims {k}: the old text's statements are missing (\"old\": {{\"C1\": \"...\"}})")
        if (k in res["added"] or res["_kinds"].get(k) == "entry") and not new:
            prob.append(f"claims {k}: no new statement (\"new\": {{\"N1\": {{\"claim\": ..., \"letter\": ...}}}})")
        for nid, v in new.items():
            if not isinstance(v, dict) or not v.get("claim") or v.get("letter") not in letters_:
                prob.append(f"claims {k}.{nid}: needs a claim and a letter of this run ({', '.join(letters_)})")
    for k in cl:
        if k not in need:
            prob.append(f"claims: block {k} is listed but was not changed or added in this run")
    return prob


OLD_OK, NEW_OK = {"kept", "sharpened"}, {"supported"}
OLD_ALL, NEW_ALL = OLD_OK | {"weakened", "contradicted", "missing"}, NEW_OK | {"unsupported"}


def doc_sha(text: str) -> str:
    import hashlib
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:16]


def cmd_packet(cfg: dict, manager: str, area: str) -> None:
    """What the reviewer reads: for every changed or added block, the old text, the new text and the
    writer's claims; the letters to check new claims against; where to write the verdicts."""
    res = check(cfg, manager, area)
    if not res["ok"]:
        sys.exit("check fails — the writer has to finish first:\n" + "\n".join(f"- {p}" for p in res["problems"]))
    s, run = _open_run(cfg, manager, area)
    cl = _load(side_path(s["name"], "claims")) or {}
    need = res["changed"] + res["added"]
    print(f"document_sha: {doc_sha(res['_new'])}")
    print(f"write the verdicts to: {side_path(s['name'], 'review').relative_to(OBSIDIAN.parent)}")
    print("letters of this run (read each in full before judging a new claim):")
    for p in run["letters"]:
        print(f"  {p}")
    if not need:
        print('\nnothing repacked or added: write {"document_sha": "<the sha above>", "entries": {}}')
        return
    for k in need:
        print(f"\n{'=' * 100}\nBLOCK {k}  ({'repacked' if k in res['changed'] else 'new'})")
        if k in res["changed"]:
            print(f"\n--- OLD TEXT ---\n{res['_ob'][k]['text'].strip()}")
        print(f"\n--- NEW TEXT ---\n{res['_nb'][k]['text'].strip()}")
        print(f"\n--- WRITER'S CLAIMS ---\n{json.dumps(cl.get(k, {}), ensure_ascii=False, indent=1)}")


def review_problems(name: str, res: dict, accept: set[str]) -> tuple[list[str], list[str]]:
    """(problems, table rows for the log). Every claim judged, every passing verdict anchored in text."""
    need = res["changed"] + res["added"]
    rv = _load(side_path(name, "review"))
    cl = _load(side_path(name, "claims")) or {}
    if rv is None:
        return [f"no review: run the reviewer (it writes {side_path(name, 'review').relative_to(OBSIDIAN.parent)})"], []
    if "_error" in rv:
        return [rv["_error"]], []
    prob, rows = [], []
    if rv.get("document_sha") != doc_sha(res["_new"]):
        prob.append("the review is of another version of the document (it changed after the review) — review again")
    ents = rv.get("entries") or {}
    for k in need:
        e, c = ents.get(k), cl.get(k, {})
        if not isinstance(e, dict):
            prob.append(f"review: block {k} was not reviewed")
            continue
        new_t = norm(res["_nb"][k]["text"])
        # a key variable is a short bullet ("CPI/PCE US"): a whole bullet line is a valid anchor too
        bullets = {norm(re.sub(r"^\s*[-*]\s+", "", ln)).strip(" .,;:")
                   for ln in res["_nb"][k]["text"].splitlines() if re.match(r"^\s*[-*]\s+", ln)}
        for cid, claim in (c.get("old") or {}).items():
            v = (e.get("old") or {}).get(cid) or {}
            verdict, where = v.get("verdict"), norm(v.get("where", "")).strip(" .,;:")
            if verdict not in OLD_ALL:
                prob.append(f"review {k}.{cid}: no verdict (one of {sorted(OLD_ALL)})")
                continue
            rows.append(f"| {k} | {cid} | {str(claim)[:80]} | {verdict} | {v.get('note', '')[:80]} |")
            if verdict in OLD_OK and not ((len(where.split()) >= 3 and where in new_t) or where in bullets):
                prob.append(f"review {k}.{cid}: '{verdict}' must cite, word for word, where the new text says it")
            if verdict not in OLD_OK and f"{k}:{cid}" not in accept:
                prob.append(f"review {k}.{cid} {verdict.upper()}: {str(claim)[:80]} — {v.get('note', '')[:120]}")
        for nid, claim in (c.get("new") or {}).items():
            v = (e.get("new") or {}).get(nid) or {}
            verdict = v.get("verdict")
            if verdict not in NEW_ALL:
                prob.append(f"review {k}.{nid}: no verdict (one of {sorted(NEW_ALL)})")
                continue
            rows.append(f"| {k} | {nid} | {claim.get('claim', '')[:80]} | {verdict} | {v.get('note', '')[:80]} |")
            if verdict in NEW_OK and not quote_found(v.get("evidence", ""), res["_text_n"]):
                prob.append(f"review {k}.{nid}: 'supported' must quote the letter word for word as evidence")
            if verdict not in NEW_OK and f"{k}:{nid}" not in accept:
                prob.append(f"review {k}.{nid} UNSUPPORTED: {claim.get('claim', '')[:80]} — {v.get('note', '')[:120]}")
        for tag, label in (("uncovered_old", "said in the old text but not in the writer's claims"),
                           ("extra", "said in the new text but in neither the old text nor the letters")):
            for item in e.get(tag) or []:
                rows.append(f"| {k} | {tag} | {str(item)[:80]} | flagged | |")
                if f"{k}:{tag}" not in accept:
                    prob.append(f"review {k}: {label}: {str(item)[:140]}")
    return prob, rows


def cmd_done(cfg: dict, manager: str, area: str, accept: list[str]) -> None:
    res = check(cfg, manager, area)
    if not res["ok"]:
        sys.exit("check fails — fix the document first:\n" + "\n".join(f"- {p}" for p in res["problems"]))
    s, run = _open_run(cfg, manager, area)
    prob, rows = review_problems(s["name"], res, set(accept))
    if prob:
        sys.exit("the review blocks the run:\n" + "\n".join(f"- {p}" for p in prob)
                 + "\n\nSend these back to the writer; or, for a verdict the USER accepts, done --accept <block>:<id>")
    today = dt.date.today().isoformat()
    ledger_add(s["name"], run["names"], today)
    lp = log_path(s["name"])
    head = "" if lp.exists() else (f"# {s['name']} — review log\n\nOne section per run: what was repacked or "
                                   "added, and the independent reviewer's verdict on every statement.\n")
    summary = (f"Repacked: {', '.join(res['repacked']) or '—'} · added: {', '.join(res['added']) or '—'}"
               + (f" · accepted by the user: {', '.join(accept)}" if accept else ""))
    table = ("| block | id | statement | verdict | note |\n|---|---|---|---|---|\n" + "\n".join(rows) + "\n"
             if rows else "No block repacked or added.\n")
    with lp.open("a", encoding="utf-8") as fh:
        fh.write(head + f"\n## {today} · {', '.join(run['names'])}\n\n{summary}\n\n{table}")
    for p in (run_path(s["name"]), side_path(s["name"], "claims"), side_path(s["name"], "review")):
        p.unlink(missing_ok=True)
    s = state(cfg, manager, area)
    span = f"{s['done'][0]['date']:%Y-%m} → {s['done'][-1]['date']:%Y-%m}"
    print(f"{s['name']}: +{len(run['names'])} letters · read {len(s['done'])} ({span}) · pending {len(s['pending'])}")


def cmd_audit(cfg: dict, manager: str, area: str) -> None:
    s = state(cfg, manager, area)
    if not s["path"].exists():
        sys.exit(f"no document: {s['path']}")
    text_n = norm(" ".join(x["path"].read_text(encoding="utf-8") for x in s["all"]))
    lines = s["path"].read_text(encoding="utf-8").splitlines()
    total, bad = 0, []
    for n, ln in enumerate(lines, 1):
        for q in quotes(ln):
            total += 1
            if not quote_found(q, text_n):
                bad.append(f"line {n}: \"{q[:100]}\"")
    print(f"{s['name']}: {total - len(bad)}/{total} quotes found word for word in the corpus"
          + (f" (corpus missing: {', '.join(s['missing'])})" if s["missing"] else ""))
    for b in bad:
        print(f"  - {b}")
    for p in structure("\n".join(lines)):
        print(f"  structure: {p}")


def cmd_seed(cfg: dict, manager: str, area: str, a: str, b: str) -> None:
    s = state(cfg, manager, area)
    lo, hi = _parse_day(a), _parse_day(b, end=True)
    done = ledger(s["name"])
    names = [x["name"] for x in s["all"] if lo <= x["date"] <= hi and x["name"] not in done]
    ledger_add(s["name"], names, "seeded")
    print(f"{s['name']}: seeded {len(names)} letters dated {lo} → {hi}")


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--list", action="store_true", help="every document and corpus, with what is pending")
    sub = ap.add_subparsers(dest="cmd")
    for c in ("begin", "check", "packet", "done", "abort", "audit", "seed"):
        p = sub.add_parser(c)
        p.add_argument("manager")
        p.add_argument("area")
        if c == "begin":
            p.add_argument("--n", type=int, help=f"letters this run (default: up to {WORD_BUDGET:,} words, max {MAX_LETTERS})")
            p.add_argument("letters", nargs="*", help="these letters (file names without .md) instead of the next ones")
        if c == "done":
            p.add_argument("--accept", nargs="*", default=[], metavar="BLOCK:ID",
                           help="verdicts the USER accepted (4.4:C2, 4.4:N1, 4.4:extra, 4.4:uncovered_old)")
        if c == "seed":
            p.add_argument("start", help="YYYY-MM or YYYY-MM-DD")
            p.add_argument("end", help="YYYY-MM or YYYY-MM-DD (inclusive)")
    a = ap.parse_args()
    cfg = config()
    if a.list:
        cmd_list(cfg)
    elif a.cmd == "begin":
        cmd_begin(cfg, a.manager, a.area, a.n, a.letters)
    elif a.cmd == "check":
        res = check(cfg, a.manager, a.area)
        print(json.dumps({k: v for k, v in res.items() if k != "problems" and not k.startswith("_")},
                         ensure_ascii=False, indent=1))
        print("\n" + ("PASS" if res["ok"] else "FAIL\n" + "\n".join(f"- {p}" for p in res["problems"])))
        sys.exit(0 if res["ok"] else 1)
    elif a.cmd == "packet":
        cmd_packet(cfg, a.manager, a.area)
    elif a.cmd == "done":
        cmd_done(cfg, a.manager, a.area, a.accept)
    elif a.cmd == "abort":
        s, _ = _open_run(cfg, a.manager, a.area)
        for p in (run_path(s["name"]), side_path(s["name"], "claims"), side_path(s["name"], "review")):
            p.unlink(missing_ok=True)
        print(f"{s['name']}: run dropped, ledger unchanged")
    elif a.cmd == "audit":
        cmd_audit(cfg, a.manager, a.area)
    elif a.cmd == "seed":
        cmd_seed(cfg, a.manager, a.area, a.start, a.end)
    else:
        ap.print_help()


if __name__ == "__main__":
    main()
