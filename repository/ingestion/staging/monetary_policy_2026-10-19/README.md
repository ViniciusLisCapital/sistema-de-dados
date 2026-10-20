# Diagnostic extraction of the monetary-policy PDFs — 2026-10-19

Not the ingestion. A read-only run of the pipeline as it stood on 2026-10-19 (`extract.py` with
pdfplumber's default `x_tolerance=3`, then `clean_code.py`) over the 46 PDFs in
`repository/monetary_policy/raw_pdf/theorical_literature/`, kept so the run is not lost.

**Do not copy these into `raw_md/` or `obsidian/.../clean_md/`.** They carry the defects the run
was made to find:

- words run together in ~20 files (`x_tolerance=3`; 1.5 fixes all of them, no regressions);
- the References cut deletes what follows it when the next heading is not ALL CAPS — Campbell et
  al. (2012) loses the whole "Comments and Discussion" (~1,150 lines);
- math symbols as `(cid:N)` in 22 files;
- Clarida–Galí–Gertler 1999/2000 shifted by 3 characters, Orphanides 2001 letter-spaced,
  Bernanke–Gertler–Gilchrist 1999 and Walsh 1995 empty (scanned).

Files: `<paper>.raw.md` and `<paper>.clean.md` per PDF, `_diag.json` with the metrics per file,
and the four `diag_*.py` scripts that produced them (run from the project root). Delete this
folder once the fixed pipeline has written the real raw_md/clean_md.
