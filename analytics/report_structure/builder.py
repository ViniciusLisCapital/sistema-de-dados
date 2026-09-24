"""
Shared build-time assembly for analytics/ self-contained HTML reports.

Extracted 2026-08 from analytics/brasil/inflation/generate_report.py (the pilot) --
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
CHART_HEAD_CSS = (_HERE / "chart_head.css").read_text(encoding="utf-8")
CHART_HEAD_JS = (_HERE / "chart_head.js").read_text(encoding="utf-8")


def render_report(template_path, data: dict, output_path, extra_markers: dict | None = None) -> Path:
    """Substitutes /*REPORT_DATA*/ (always) and /*THEME_CSS*/ /
    /*Y_AUTOFIT_JS*/ / /*CHART_HEAD_CSS*/ / /*CHART_HEAD_JS*/ (only if the
    template has those markers) into `template_path`, writes the result to
    `output_path`, and returns the resolved output Path.

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
    if "/*CHART_HEAD_CSS*/" in html:
        html = html.replace("/*CHART_HEAD_CSS*/", CHART_HEAD_CSS)
    if "/*CHART_HEAD_JS*/" in html:
        html = html.replace("/*CHART_HEAD_JS*/", CHART_HEAD_JS)
    for name, value in (extra_markers or {}).items():
        marker = f"/*{name}*/"
        if marker not in html:
            continue
        rendered = "null" if value is None else json.dumps(value, ensure_ascii=False, default=str)
        html = html.replace(marker, rendered)

    out = Path(output_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html, encoding="utf-8")
    _registrar_procedencia(out)
    return out.resolve()


def _registrar_procedencia(out: Path) -> None:
    """Grava o retrato das fontes deste relatorio, no mesmo passo que o escreveu.

    O QUE E: um registro de com que dado o arquivo foi montado -- "quando gerei o
    Credito, o banco tinha inadimplencia ate agosto". A data do arquivo diz quando ele
    foi salvo, nao o que havia dentro; sem o retrato, "este relatorio ficou para tras"
    nao tem como ser afirmado. Quem compara e `domain.dashboards.status`.

    POR QUE AQUI. Ate 2026-09-23 o retrato era gravado por `status.gerar()`, um passo
    separado que so acontecia se o relatorio fosse gerado POR AQUELE caminho -- e o
    comando documentado em 10 dos 13 `CLAUDE.md` de pasta e `generate_report.run()`,
    que nao passa por la. Resultado medido naquele dia: 8 dos 13 relatorios entregues
    tinham retrato ausente ou de outra geracao, e a aba de status nao conseguia dizer
    nada sobre quase metade deles. Um mecanismo que depende de ninguem usar o caminho
    normal nao fica em dia.

    Esta funcao fecha isso por construcao: todos os 12 relatorios HTML do projeto
    passam por `render_report()`, entao gerar de qualquer jeito -- `run()` na mao,
    `status.gerar()`, notebook -- deixa o retrato em dia. Nao ha mais como esquecer.

    TRES CUIDADOS, cada um a origem de um defeito possivel:

    - **Depois de escrever, nunca antes.** O retrato guarda o mtime do arquivo em
      nanossegundos, e e ele que responde "este retrato e deste arquivo?". Gravado
      antes do `write_text`, o retrato seria da versao anterior e daria um "em dia" de
      mentira.
    - **Falhar aqui nao pode derrubar a geracao.** O retrato consulta o banco; banco
      fora do ar nao pode virar "sem relatorio". A falha e avisada e o arquivo, que ja
      esta em disco, fica valendo -- e o veredito passa a ser "nao da para conferir",
      que e a resposta honesta.
    - **Arquivo que nao esta no manifesto nao stampa** (o template de comparacao de
      juros reais, por exemplo). `chave_por_saida()` devolve None e a funcao sai calada:
      nao ha o que comparar contra um dashboard que ninguem declarou.

    O import e local de proposito: `analytics/` nao passa a exigir que `domain/` esteja
    importavel so para montar um HTML, e `status.gerar()` importa `generate_report` (que
    importa este modulo) -- fechar esse ciclo no topo do arquivo seria pedir problema.
    """
    try:
        from domain.dashboards import status
    except Exception as exc:  # noqa: BLE001 -- ver "nao pode derrubar a geracao"
        print(f"  [procedencia] nao registrada ({type(exc).__name__}: {exc})")
        return

    try:
        key = status.chave_por_saida(out)
        if key is None:
            return
        status.stamp(key)
    except Exception as exc:  # noqa: BLE001
        print(f"  [procedencia] {out.name}: nao registrada "
              f"({type(exc).__name__}: {exc}) -- o relatorio foi salvo mesmo assim")
