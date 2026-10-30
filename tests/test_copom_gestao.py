"""
repository/ingestion/scripts/copom_gestao.py: the Copom index page of a presidency and its
managed lines on concept pages. Everything runs in a tmp vault (module paths and the DB read
patched); the real vault is never touched.

    uv run --with pytest python -m pytest tests/test_copom_gestao.py
"""

import sys
from pathlib import Path

import pytest
import yaml

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "repository" / "ingestion" / "scripts"))

import copom_gestao as cg  # noqa: E402
import vault  # noqa: E402

ATA1 = ("Fonte: BCB\nReunião: 1ª reunião do Copom\nData de referência: 2025-02-01\n"
        "Data de publicação: 2025-02-08\n\n---\n\nAs expectativas de inflação\n permanecem acima da meta. "
        "O quadro fiscal exige cautela.\n")
COM1 = "Fonte: BCB\n\n---\n\nO Comitê elevou a taxa Selic em 100 pontos-base.\n"
ATA2 = "Fonte: BCB\nData de publicação: 2025-03-27\n\n---\n\nO mercado de trabalho segue aquecido.\n"

ROWS = [
    {"nro": 1, "date": "2025-02-01", "ant": 12.25, "dec": 13.25, "bps": 100, "decisao": "elevacao"},
    {"nro": 2, "date": "2025-03-19", "ant": 13.25, "dec": 13.25, "bps": 0, "decisao": "manutencao"},
    {"nro": 0, "date": "2024-12-11", "ant": 11.25, "dec": 12.25, "bps": 100, "decisao": "elevacao"},
]


@pytest.fixture
def v(tmp_path, monkeypatch):
    root = tmp_path / "obsidian"
    cb = root / "monetary_policy" / "clean_md" / "central_bank"
    (cb / "atas").mkdir(parents=True)
    (cb / "comunicados").mkdir()
    (cb / "atas" / "copom_1_ata_2025-02-01.md").write_text(ATA1, encoding="utf-8")
    (cb / "comunicados" / "copom_1_comunicado_2025-02-01.md").write_text(COM1, encoding="utf-8")
    (cb / "atas" / "copom_2_ata_2025-03-19.md").write_text(ATA2, encoding="utf-8")
    (root / "concepts").mkdir()
    for slugs in cg.VOCABULARY.values():
        for c in slugs[1]:
            (root / "concepts" / f"{c}.md").write_text(f"# {c}\n\nBody 0.5.\n", encoding="utf-8")
    themes = tmp_path / "themes"
    themes.mkdir()
    for name, val in (("OBSIDIAN", root), ("CONCEPTS", root / "concepts"), ("ATAS_DIR", cb / "atas"),
                      ("COMUNICADOS_DIR", cb / "comunicados"), ("PAGE_DIR", root / "monetary_policy" / "central_bank"),
                      ("THEMES_DIR", themes)):
        monkeypatch.setattr(cg, name, val)
    monkeypatch.setattr(cg, "read_decisions", lambda: [dict(r) for r in ROWS])
    monkeypatch.setitem(cg.GESTOES, "galipolo", {"nome": "Galípolo", "inicio": "2025-01-01"})

    class V:
        pass
    o = V()
    o.root, o.themes, o.cb = root, themes, cb
    o.page = root / "monetary_policy" / "central_bank" / "gestao_galipolo.md"
    o.concept = lambda c: root / "concepts" / f"{c}.md"
    o.write = lambda data: (themes / "gestao_galipolo_temas.yaml").write_text(
        yaml.safe_dump({"gestao": "galipolo", "reunioes": data}, allow_unicode=True), encoding="utf-8")
    o.good = {1: {"temas": [
        {"tema": "expectativas", "evidence": "As expectativas de inflação permanecem acima da meta."},
        {"tema": "fiscal", "evidence": "O quadro fiscal exige cautela."}]},
        2: {"temas": [{"tema": "mercado-de-trabalho", "evidence": "O mercado de trabalho segue aquecido."}]}}
    o.write(o.good)
    return o


def test_build_page_content(v):
    assert cg.build("galipolo") == []
    t = v.page.read_text(encoding="utf-8")
    assert t.startswith("# Copom — gestão Galípolo\n")
    for s in ("## Sobre esta página", "## Vocabulário de temas", "## Reunião 1 — 2025-02-01", "## Reunião 2 — 2025-03-19"):
        assert s in t
    assert "Reunião 0" not in t                          # before the gestão
    s1 = t.split("## Reunião 1 — 2025-02-01")[1].split("## Reunião 2")[0]
    assert "reunião 2025-02-01 · publicação da ata 2025-02-08" in s1
    assert "**Decisão:** Selic 12,25% → 13,25% (+100 bps, elevacao)" in s1
    assert "#gestao/galipolo #copom/reuniao-1 #decisao/elevacao #tema/expectativas #tema/fiscal" in s1
    assert "[[monetary_policy/clean_md/central_bank/atas/copom_1_ata_2025-02-01]]" in s1
    assert "[[monetary_policy/clean_md/central_bank/comunicados/copom_1_comunicado_2025-02-01]]" in s1
    assert "[[fiscal_dominance]], [[fiscal_impulse]]" in s1
    assert '"As expectativas de inflação permanecem acima da meta."' in s1   # whitespace-normalised
    s2 = t.split("## Reunião 2 — 2025-03-19")[1]
    assert "(+0 bps, manutencao)" in s2 and "comunicado [[" not in s2
    assert "| `balanco-de-riscos` |" in t                # vocabulary table
    assert cg.check("galipolo") == []


def test_concept_line_insert_replace_remove(v):
    before = v.concept("fiscal_dominance").read_text(encoding="utf-8")
    cg.build("galipolo")
    after = v.concept("fiscal_dominance").read_text(encoding="utf-8")
    assert after.startswith(before.rstrip("\n"))
    line = after.splitlines()[-1]
    assert line == ("Copom, gestão Galípolo: [[monetary_policy/central_bank/gestao_galipolo#Reunião 1 — 2025-02-01|1]] "
                    "<!-- copom-gestao:galipolo -->")
    assert after.count("copom-gestao:galipolo") == 1
    assert cg.apply_line(after, "galipolo", None) == before            # exact inverse
    # idempotent
    cg.build("galipolo")
    assert v.concept("fiscal_dominance").read_text(encoding="utf-8") == after
    # replace in place, text after the line preserved
    v.concept("fiscal_dominance").write_text(after + "\nTrailing note.\n", encoding="utf-8")
    d = dict(v.good)
    d[2] = {"temas": [{"tema": "fiscal", "evidence": "O mercado de trabalho segue aquecido."}]}
    v.write(d)
    cg.build("galipolo")
    t = v.concept("fiscal_dominance").read_text(encoding="utf-8")
    assert t.count("copom-gestao:galipolo") == 1 and "|1]], [[" in t and "|2]]" in t
    assert t.endswith("Trailing note.\n")
    # remove from pages no longer referenced
    v.write({1: {"temas": []}, 2: {"temas": []}})
    cg.build("galipolo")
    assert "copom-gestao" not in v.concept("fiscal_dominance").read_text(encoding="utf-8")
    assert "copom-gestao" not in v.concept("inflation_expectations_anchoring").read_text(encoding="utf-8")
    assert v.concept("fiscal_dominance").read_text(encoding="utf-8").rstrip("\n") == before.rstrip("\n") + "\n\nTrailing note."


def test_build_refuses_bad_input_and_writes_nothing(v):
    v.write({1: {"temas": [{"tema": "inventado", "evidence": "x"}]}, 2: {"temas": []}})
    assert cg.build("galipolo")
    assert not v.page.exists()


def test_check_theme_not_in_vocabulary(v):
    cg.build("galipolo")
    v.write({1: {"temas": [{"tema": "inventado", "evidence": "x"}]}, 2: {"temas": []}})
    assert any("not in the vocabulary" in p for p in cg.check("galipolo"))


def test_check_evidence_not_found(v):
    cg.build("galipolo")
    d = dict(v.good)
    d[1] = {"temas": [{"tema": "fiscal", "evidence": "O quadro fiscal exige muita cautela."}]}
    v.write(d)
    assert any("evidence of fiscal not found" in p for p in cg.check("galipolo"))


def test_check_evidence_may_come_from_the_comunicado(v):
    d = dict(v.good)
    d[1] = {"temas": [{"tema": "guidance", "evidence": "O Comitê elevou a taxa Selic em 100 pontos-base."}]}
    v.write(d)
    cg.build("galipolo")
    assert cg.check("galipolo") == []


def test_check_broken_link(v):
    cg.build("galipolo")
    (v.cb / "atas" / "copom_1_ata_2025-02-01.md").rename(v.cb / "atas" / "copom_1_ata_2025-02-02.md")
    assert any("link does not resolve" in p or "stale" in p for p in cg.check("galipolo"))
    cg.build("galipolo")                                     # relinked to the renamed file: resolves
    assert cg.check("galipolo") == []
    v.page.write_text(v.page.read_text(encoding="utf-8") + "\n[[monetary_policy/clean_md/nada]]\n", encoding="utf-8")
    assert any("link does not resolve: [[monetary_policy/clean_md/nada]]" in p for p in cg.check("galipolo"))


def test_check_concept_link_missing_page(v):
    cg.build("galipolo")
    v.concept("fiscal_impulse").unlink()
    assert any("fiscal_impulse" in p for p in cg.check("galipolo"))


def test_check_missing_meeting(v, monkeypatch):
    cg.build("galipolo")
    v.write({1: v.good[1]})                                  # themes file lacks meeting 2
    assert any("meeting 2 is missing from the themes file" in p for p in cg.check("galipolo"))
    v.write(v.good)
    t = v.page.read_text(encoding="utf-8")
    v.page.write_text(t.replace("## Reunião 2 — 2025-03-19", "## Outra coisa"), encoding="utf-8")
    assert any("no section for meeting 2" in p for p in cg.check("galipolo"))
    v.page.write_text(t, encoding="utf-8")
    # a meeting with files in the period but no table row
    (v.cb / "atas" / "copom_3_ata_2025-05-07.md").write_text(ATA2, encoding="utf-8")
    assert any("meeting 3" in p and "pm_copom_reuniao" in p for p in cg.check("galipolo"))
    # a meeting in the table, not in the page
    (v.cb / "atas" / "copom_3_ata_2025-05-07.md").unlink()
    monkeypatch.setattr(cg, "read_decisions", lambda: [dict(r) for r in ROWS]
                        + [{"nro": 3, "date": "2025-05-07", "ant": 13.25, "dec": 13.25, "bps": 0, "decisao": "manutencao"}])
    assert cg.check("galipolo")


def test_check_decision_differs_from_table(v, monkeypatch):
    cg.build("galipolo")
    rows = [dict(r) for r in ROWS]
    rows[0]["dec"], rows[0]["bps"] = 13.0, 75
    monkeypatch.setattr(cg, "read_decisions", lambda: rows)
    assert any("decision of meeting 1 differs from the table" in p for p in cg.check("galipolo"))


def test_check_stale_page_and_concept_lines(v):
    cg.build("galipolo")
    assert cg.check("galipolo") == []
    v.page.write_text(v.page.read_text(encoding="utf-8") + "extra\n", encoding="utf-8")
    assert any("index page" in p and "stale" in p for p in cg.check("galipolo"))
    cg.build("galipolo")
    p = v.concept("fiscal_dominance")
    p.write_text(p.read_text(encoding="utf-8").replace("|1]]", "|7]]"), encoding="utf-8")
    assert any("concept fiscal_dominance: managed line is stale" in x for x in cg.check("galipolo"))
    cg.build("galipolo")
    # a page that carries the line but is no longer referenced
    q = v.concept("output_gap")
    q.write_text(q.read_text(encoding="utf-8") + "\nCopom, gestão Galípolo: x " + cg.mark("galipolo") + "\n", encoding="utf-8")
    assert any("output_gap" in x and "to be removed" in x for x in cg.check("galipolo"))
    # a concept page missing the line
    v.concept("fiscal_impulse").write_text("# fiscal_impulse\n", encoding="utf-8")
    assert any("fiscal_impulse" in x for x in cg.check("galipolo"))


def test_vault_concept_check_ignores_the_managed_line(v, monkeypatch):
    clean = v.root / "mp" / "clean_md"
    syn = v.root / "mp" / "synthesis"
    clean.mkdir(parents=True)
    syn.mkdir()
    (clean / "paper (Doe, 2000).md").write_text("a weight of 0.5", encoding="utf-8")
    (syn / "paper (Doe, 2000).md").write_text("x", encoding="utf-8")
    monkeypatch.setattr(vault, "OBSIDIAN", v.root)
    monkeypatch.setattr(vault, "CONCEPTS", v.root / "concepts")
    cg.build("galipolo")
    page = v.concept("fiscal_dominance")
    page.write_text("# F\n\nWeight 0.5 [[mp/synthesis/paper (Doe, 2000)]].\n", encoding="utf-8")
    cg.build("galipolo")
    assert "copom-gestao" in page.read_text(encoding="utf-8")
    r = vault.check_concept("fiscal_dominance")
    assert r["ok"], r["problems"]
    # without the marker the 281-style numbers on that line would be flagged: the marker is what exempts it
    page.write_text(page.read_text(encoding="utf-8").replace("<!-- copom-gestao:galipolo -->", ""), encoding="utf-8")
    assert not vault.check_concept("fiscal_dominance")["ok"]
