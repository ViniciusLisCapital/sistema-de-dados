"""
Diagrama do sistema de agentes-analistas: de onde vêm dados e conhecimento, as ferramentas,
e como os agentes interagem num ciclo.

O desenho (caixas e setas) é escrito à mão no `report.html`, porque muda pouco. As contagens
que aparecem nele são LIDAS na geração, para não envelhecerem em silêncio: tabelas no
registry, connectors e notas do vault por área.

Desde 2026-10-02 a página tem só a visão geral; as abas de ciclo, ferramentas e dados foram
retiradas a pedido do usuário e voltam quando o fluxo de cada uma estiver definido.

Uso:
    uv run python -m analytics.agent_system.generate_report
"""

from __future__ import annotations

from datetime import datetime
from pathlib import Path

from analytics.report_structure.builder import render_report

_AQUI = Path(__file__).parent
RAIZ = _AQUI.parents[1]
TEMPLATE = _AQUI / "report.html"
SAIDA = RAIZ / "team_materials" / "structure_materials" / "Sistema de Agentes.html"
VAULT = RAIZ / "obsidian"


def registry_info(avisos: list[str]) -> dict:
    try:
        from domain.db import registry
        tabs = registry.tabelas()
    except Exception as exc:  # noqa: BLE001 -- o diagrama sai mesmo sem o registry
        avisos.append(f"Registry de tabelas indisponível ({type(exc).__name__}).")
        return {}
    por_area: dict[str, int] = {}
    for dotted in tabs.values():
        area = dotted.split(".")[2]
        por_area[area] = por_area.get(area, 0) + 1
    return {"total": len(tabs), "por_area": por_area}


def vault_info() -> dict:
    out = {}
    for area in sorted(p for p in VAULT.iterdir() if p.is_dir() and p.name != "ciclos"
                        and not p.name.startswith(".")):
        conta = {sub: (sum(1 for _ in (area / sub).rglob("*.md")) if (area / sub).exists() else 0)
                 for sub in ("clean_md", "synthesis", "concepts", "mental_models")}
        conta["mapa"] = (area / f"{area.name}_conceptual_map.md").exists()
        out[area.name] = conta
    return out


def montar() -> dict:
    avisos: list[str] = []
    return {
        "gerado_em": datetime.now().strftime("%d/%m/%Y %H:%M"),
        "registry": registry_info(avisos),
        "n_connectors": sum(1 for p in (RAIZ / "connectors").glob("*.py") if p.name != "__init__.py"),
        "vault": vault_info(),
        "avisos": avisos,
    }


def run() -> Path:
    data = montar()
    out = render_report(TEMPLATE, data, SAIDA)
    for aviso in data["avisos"]:
        print(f"  [aviso] {aviso}")
    print(f"  {out}")
    return out


if __name__ == "__main__":
    run()
