"""
Diagrama do sistema de agentes-analistas: de onde vêm dados e conhecimento, as ferramentas,
e como os agentes interagem num ciclo.

O desenho (caixas e setas) é escrito à mão no `report.html`, porque muda pouco. As contagens
que aparecem nele são LIDAS na geração, para não envelhecerem em silêncio: tabelas no
registry, connectors e notas do vault por área.

O diagrama é um guia expansível: clicar numa seta ou caixa marcada abre o detalhe dela. A
primeira é MySQL → Câmbio, cuja lista de tabelas é lida da seção V.I do SISTEMA_AGENTES.md.

Uso:
    uv run python -m analytics.agent_system.generate_report
"""

from __future__ import annotations

import re
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


def dados_agente(agente: str, nome: str, avisos: list[str]) -> dict:
    """A lista de dados de um agente, lida da seção V do SISTEMA_AGENTES.md (V.I câmbio, V.II PM).

    É lida, e não copiada para cá, para que o diagrama e a lista decidida não divirjam. O
    leitor é o mesmo do gerador do F(A) (`dados/motor.py`)."""
    import importlib
    from analytics.agent_system.dados.motor import ler_lista
    SECAO = importlib.import_module(f"analytics.agent_system.dados.{agente}").SECAO

    try:
        grupos = ler_lista(SECAO)
    except (OSError, ValueError) as exc:
        avisos.append(f"Lista de dados de {nome} (SISTEMA_AGENTES.md V) não encontrada ({type(exc).__name__}).")
        return {"grupos": []}
    try:
        from domain.db import registry
        reg = registry.tabelas()
    except Exception:  # noqa: BLE001 -- o aviso do registry já sai em registry_info()
        reg = {}
    for g in grupos:
        for it in g["itens"]:
            dotted = reg.get(it["tabela"])
            if reg and not dotted:
                avisos.append(f"`{it['tabela']}` está na lista de {nome} mas não no registry de tabelas.")
            it["fonte"] = dotted.split(".")[3] if dotted else None
    return {"grupos": grupos}


_RE_PERGUNTA = re.compile(r"^\| (Q\d) \| ([^|]+?) \|")


def perguntas(area: str, nome: str, avisos: list[str]) -> list[dict]:
    """As perguntas centrais de uma área, lidas da Parte 1 do mapa conceitual (não copiadas)."""
    mapa = VAULT / area / f"{area}_conceptual_map.md"
    try:
        linhas = mapa.read_text(encoding="utf-8").splitlines()
    except OSError:
        avisos.append(f"Mapa conceitual de {nome} não encontrado: sem as perguntas centrais.")
        return []
    out = [{"id": m.group(1), "texto": m.group(2)} for l in linhas if (m := _RE_PERGUNTA.match(l))]
    if not out:
        avisos.append(f"Perguntas centrais não encontradas no mapa conceitual de {nome}.")
    return out


def montar() -> dict:
    avisos: list[str] = []
    return {
        "gerado_em": datetime.now().strftime("%d/%m/%Y %H:%M"),
        "registry": registry_info(avisos),
        "dados_cambio": dados_agente("cambio", "câmbio", avisos),
        "perguntas_cambio": perguntas("exchange_rate", "câmbio", avisos),
        "dados_pm": dados_agente("politica_monetaria", "política monetária", avisos),
        "perguntas_pm": perguntas("monetary_policy", "política monetária", avisos),
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
