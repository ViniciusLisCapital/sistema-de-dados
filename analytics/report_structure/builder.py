"""
Shared build-time assembly for analytics/ self-contained HTML reports.

Extracted 2026-08 from analytics/inflation/generate_report.py (the pilot) --
see analytics/report_structure/CLAUDE.md for the convention this establishes
and which reports have been migrated onto it so far.

This module only runs at generation time, inside each report's own
generate_report.py. The assembled output is still one flat, self-contained
HTML file -- report.html templates never import or reference this package at
runtime, so emailability/portability of the generated report is unaffected.
"""

import json
from pathlib import Path

_HERE = Path(__file__).parent
THEME_CSS = (_HERE / "theme.css").read_text(encoding="utf-8")
Y_AUTOFIT_JS = (_HERE / "y_autofit.js").read_text(encoding="utf-8")


def render_report(template_path, data: dict, output_path, extra_markers: dict | None = None) -> Path:
    """Substitutes /*REPORT_DATA*/ (always) and /*THEME_CSS*/ / /*Y_AUTOFIT_JS*/
    (only if the template has those markers) into `template_path`, writes the
    result to `output_path`, and returns the resolved output Path.

    `extra_markers` is for templates carrying additional JSON payload markers
    beyond the single /*REPORT_DATA*/ one -- `{"PPP_DATA": payload_or_None}`
    substitutes `/*PPP_DATA*/` with that payload's JSON, or with the literal
    `null` when the value is None (so the template's JS always has something
    valid to check against, whether or not that section's data was built this
    run). Unlike /*REPORT_DATA*/, the marker is replaced by the bare JSON
    value, not a `const X = ...;` statement -- the template owns the
    declaration. Added 2026-08 for exchange_rate/, whose report.html carries
    /*PPP_DATA*/ + /*FXATTR_DATA*/ + /*RIDGE_DATA*/ alongside /*REPORT_DATA*/
    since the PPP dashboard was fused into it.
    """
    template = Path(template_path).read_text(encoding="utf-8")

    payload = json.dumps(data, ensure_ascii=False, default=str)
    html = template.replace("/*REPORT_DATA*/", f"const REPORT_DATA = {payload};")
    if "/*THEME_CSS*/" in html:
        html = html.replace("/*THEME_CSS*/", THEME_CSS)
    if "/*Y_AUTOFIT_JS*/" in html:
        html = html.replace("/*Y_AUTOFIT_JS*/", Y_AUTOFIT_JS)
    for name, value in (extra_markers or {}).items():
        marker = f"/*{name}*/"
        if marker not in html:
            continue
        rendered = "null" if value is None else json.dumps(value, ensure_ascii=False, default=str)
        html = html.replace(marker, rendered)

    out = Path(output_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html, encoding="utf-8")
    return out.resolve()
