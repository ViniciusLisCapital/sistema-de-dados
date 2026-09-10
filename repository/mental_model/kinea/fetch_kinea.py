"""Kinea blog post -> markdown, in the shape this folder's *.md already use.

Kinea publishes its two series as blog posts, not PDFs, so unlike Verde
(`../verde_asset/DOWNLOAD_PROCESS.md`) and Kapitalo (`../kapitalo/curate.py`)
there is no PDF step: the post's HTML *is* the source, and this script is both
the fetcher and the curator.

    # what exists on the site that is not here yet
    uv run python repository/mental_model/kinea/fetch_kinea.py --new

    # convert specific posts
    uv run python repository/mental_model/kinea/fetch_kinea.py \
        repository/mental_model/kinea kinea_ https://www.kinea.com.br/blog/<slug>/

Two series, two folders and two prefixes:
  Carta do Gestor  -> repository/mental_model/kinea/          prefix "kinea_"
  Kinea Insights   -> repository/mental_model/kinea_insights/ prefix "kinea_insights_"

Filename stamp is DDMMYYYY of the PUBLICATION date, and so is the `date`
column of `fx_attribution_data/kinea/documents.csv`. Its `month` column is
NOT: since 2026-09-08 a main letter is bucketed by the month it COVERS, so
one published in the first days of a month (kinea_01082026 = the July letter)
belongs to the previous one. `kinea_insights` is bucketed on publication,
because a mid-month deep-dive covers no prior period. Getting this backwards
is what put two letters in Ago/2026 and none in Jul/2026 -- see the "2026H2
refresh" section of `analytics/brasil/exchange_rate/models/fx_attribution_model.md`.

Gotchas, both found the hard way:
  - The WordPress REST API (`/wp-json/wp/v2/posts`) is blocked by the site's
    WAF (403 "automated requests"). The rendered `/blog/` index is not, so
    discovery goes through it.
  - Section headings arrive fully wrapped in <strong> in some letters and bare
    in others; the corpus convention is a bare "### TITLE", hence
    `_plain_heading()`. And the template appends a newsletter call-to-action
    inside the article body, which is boilerplate and is cut.
"""
import argparse
import html as _html
import re
import subprocess
import sys
from pathlib import Path

BLOG_INDEX = "https://www.kinea.com.br/blog/"
CORPUS = Path(__file__).resolve().parent.parent  # repository/mental_model
SERIES = {  # folder -> filename prefix
    CORPUS / "kinea": "kinea_",
    CORPUS / "kinea_insights": "kinea_insights_",
}

MES = {"janeiro": 1, "fevereiro": 2, "março": 3, "marco": 3, "abril": 4, "maio": 5,
       "junho": 6, "julho": 7, "agosto": 8, "setembro": 9, "outubro": 10,
       "novembro": 11, "dezembro": 12}


def fetch(url: str) -> str:
    out = subprocess.run(["curl", "-sL", "--max-time", "60", "-A", "Mozilla/5.0", url],
                         capture_output=True)
    return out.stdout.decode("utf-8", errors="replace")


def _inner(tag_html: str) -> str:
    """One block element's inner HTML -> markdown inline text."""
    s = re.sub(r"<br\s*/?>", "\n", tag_html, flags=re.I)
    s = re.sub(r"<(strong|b)\b[^>]*>(.*?)</\1>", r"**\2**", s, flags=re.I | re.S)
    s = re.sub(r"<(em|i)\b[^>]*>(.*?)</\1>", r"*\2*", s, flags=re.I | re.S)
    s = re.sub(r'<a\b[^>]*href="([^"]+)"[^>]*>(.*?)</a>', r"[\2](\1)", s, flags=re.I | re.S)
    s = re.sub(r"<[^>]+>", "", s)
    return " ".join(_html.unescape(s).split())


def _plain_heading(txt: str) -> str:
    m = re.fullmatch(r"\*\*(.+)\*\*", txt)
    return (m.group(1) if m else txt).strip()


def convert(url: str) -> tuple[str, str, str]:
    """-> (DDMMYYYY stamp, markdown, title)"""
    doc = fetch(url)

    m = re.search(r'<h1 class="singlePost__titulo">(.*?)</h1>', doc, re.S)
    title = _inner(m.group(1)) if m else "(sem titulo)"

    m = re.search(r'<span class="singlePost__autorTexto">.*?&mdash;\s*(\d{1,2})\s+de\s+([a-zç]+),\s*(\d{4})',
                  doc, re.S | re.I)
    if not m:
        raise SystemExit(f"publication date not found in {url}")
    day, mes, year = int(m.group(1)), MES[m.group(2).lower()], int(m.group(3))

    m = re.search(r'<div class="singlePost__textoPost ConteudoPostagem">(.*?)</div>\s*</div>\s*</section>',
                  doc, re.S) or re.search(r'<div class="singlePost__textoPost ConteudoPostagem">(.*)', doc, re.S)
    body = re.sub(r"<(script|style|figcaption)\b.*?</\1>", "", m.group(1), flags=re.I | re.S)
    body = re.split(r"Receba insights da Kinea", body)[0]

    lines = []
    for m2 in re.finditer(r"<(h2|h3|h4|p|li)\b[^>]*>(.*?)</\1>|<img\b([^>]*?)/?>", body, re.S | re.I):
        if m2.group(1):
            tag, txt = m2.group(1).lower(), _inner(m2.group(2))
            if not txt:
                continue
            if tag in ("h2", "h3", "h4"):
                lines.append("#" * int(tag[1]) + " " + _plain_heading(txt))
            elif tag == "li":
                lines.append(f"- {txt}")
            else:
                lines.append(txt)
        else:
            src = re.search(r'src="([^"]+)"', m2.group(3) or "")
            if src and "wp-content" in src.group(1):
                lines.append(f"![]({src.group(1)})")

    md = (f"# {title}\n\n**Data de publicação:** {day:02d}/{mes:02d}/{year}\n"
          f"**Fonte:** {url}\n\n" + "\n\n".join(lines) + "\n")
    return f"{day:02d}{mes:02d}{year}", md, title


def have_urls() -> set[str]:
    """Every source URL already in the corpus, normalized with a trailing slash."""
    urls = set()
    for d in SERIES:
        for p in d.glob("*.md"):
            m = re.search(r"\*\*Fonte:\*\*\s*(\S+)", p.read_text(encoding="utf-8", errors="replace"))
            if m:
                urls.add(m.group(1).rstrip("/") + "/")
    return urls


def list_new() -> list[str]:
    index = fetch(BLOG_INDEX)
    site = sorted(set(re.findall(r'href="(https://www\.kinea\.com\.br/blog/[a-z0-9-]+/)"', index)))
    return [u for u in site if u not in have_urls()]


def write(outdir: Path, prefix: str, urls: list[str]) -> None:
    for url in urls:
        stamp, md, title = convert(url)
        p = outdir / f"{prefix}{stamp}.md"
        p.write_text(md, encoding="utf-8")
        print(f"ok  {p.name}  ({len(md)} chars)  {title}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--new", action="store_true",
                    help="list posts on the blog index that are not in the corpus yet")
    ap.add_argument("args", nargs="*", metavar="OUTDIR PREFIX URL...")
    ns = ap.parse_args()

    if ns.new:
        new = list_new()
        print("\n".join(new) if new else "corpus is up to date with the blog index")
        sys.exit(0)
    if len(ns.args) < 3:
        ap.error("need OUTDIR PREFIX and at least one URL (or --new)")
    write(Path(ns.args[0]), ns.args[1], ns.args[2:])
