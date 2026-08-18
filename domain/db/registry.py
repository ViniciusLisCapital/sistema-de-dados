"""
Mapa tabela -> script de ETL que escreve nela.

Existe para responder "quero atualizar SO estas tabelas, quais scripts rodar?" —
pergunta que `jobs/update_db.py` nao sabia responder (ele so tem a lista completa,
na ordem curada) e que aparece em dois lugares novos: o `--group` do proprio job e
o botao de atualizar do relatorio de calendario.

**Descoberto por convencao, nao mantido a mao.** Todo script em `domain/db/` declara
`_TABLE = "<nome>"` (ou `TABLE`) e vive num arquivo com exatamente esse nome — 60 de
60 seguem isso, verificado. Entao o mapa e derivado varrendo os arquivos, e
`validar()` levanta se algum quebrar a convencao. Uma lista escrita a mao envelheceria
em silencio a cada tabela nova; esta nao envelhece, ela reclama.

A varredura le os arquivos com regex, sem importar nada — importar `domain.db.*`
inteiro puxaria pandas/mysql/requests de 60 modulos so para montar um dicionario.
O import acontece so em `carregar()`, no modulo que vai de fato rodar.

Uso:

    from domain.db.registry import scripts_para_tabelas

    plano, sem_script = scripts_para_tabelas(["cred_credito_resumo", "cred_ptc"])
    for dotted, tabelas in plano:
        carregar(dotted).run()
"""

from __future__ import annotations

import importlib
import re
from pathlib import Path
from types import ModuleType

_RAIZ = Path(__file__).parent          # domain/db/
_PKG = "domain.db"

_RE_TABLE = re.compile(r'^_?TABLE\w*\s*=\s*"([^"]+)"', re.M)

# Tabela -> modulo, quando o modulo NAO se chama igual a tabela.
#
# So o Novo CAGED: as 3 tabelas de corte tem modulo proprio com run() que funciona,
# mas o ponto de entrada certo e o orquestrador `mt_caged_novo`, que baixa cada
# release do FTP UMA vez e alimenta as 3 no mesmo passe. Rodar os 3 separados
# baixaria ~50MB/mes tres vezes. Como os tres apontam para o mesmo modulo,
# scripts_para_tabelas() naturalmente colapsa num unico script.
_OVERRIDES = {
    "mt_caged_setor": f"{_PKG}.brasil.mte.mt_caged_novo",
    "mt_caged_uf": f"{_PKG}.brasil.mte.mt_caged_novo",
    "mt_caged_salario": f"{_PKG}.brasil.mte.mt_caged_novo",
}

# Modulos que declaram _TABLE mas nao devem ser oferecidos como script de tabela
# (sao alimentados por um orquestrador; ver _OVERRIDES acima).
_NAO_DIRETOS = {"mt_caged_setor", "mt_caged_uf", "mt_caged_salario"}


def _varrer() -> tuple[dict[str, str], list[str]]:
    """Devolve ({tabela: modulo}, [avisos de convencao quebrada])."""
    mapa: dict[str, str] = {}
    problemas: list[str] = []

    for py in sorted(_RAIZ.rglob("*.py")):
        nome = py.stem
        if nome.startswith("_") or nome == "registry":
            continue
        try:
            texto = py.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError) as exc:  # pragma: no cover
            problemas.append(f"{py}: nao deu para ler ({exc})")
            continue

        achados = _RE_TABLE.findall(texto)
        if not achados:
            continue

        dotted = _PKG + "." + ".".join(py.relative_to(_RAIZ).with_suffix("").parts)

        for tabela in set(achados):
            if tabela != nome:
                problemas.append(
                    f"{py.relative_to(_RAIZ)}: declara _TABLE={tabela!r} mas o arquivo "
                    f"se chama {nome!r} — convencao do registry quebrada"
                )
                continue
            if nome in _NAO_DIRETOS:
                continue
            mapa[tabela] = dotted

    mapa.update(_OVERRIDES)
    return mapa, problemas


_MAPA, _PROBLEMAS = _varrer()


def tabelas() -> dict[str, str]:
    """{tabela: caminho pontilhado do modulo} — copia, nao o dict interno."""
    return dict(_MAPA)


def modulo(tabela: str) -> str | None:
    return _MAPA.get(tabela)


def carregar(dotted: str) -> ModuleType:
    return importlib.import_module(dotted)


def scripts_para_tabelas(alvos) -> tuple[list[tuple[str, list[str]]], list[str]]:
    """Menor conjunto de scripts que cobre `alvos`.

    Devolve ([(modulo, [tabelas que ele alimenta]), ...], [tabelas sem script]).
    Deduplica: 3 tabelas do Novo CAGED viram um script so. Ordem estavel (alfabetica
    por modulo) para o log ficar comparavel entre execucoes.

    As tabelas sem script sao DEVOLVIDAS, nao ignoradas — quem chama precisa poder
    dizer "nao sei atualizar isto" em vez de reportar sucesso silencioso.
    """
    por_modulo: dict[str, list[str]] = {}
    sem_script: list[str] = []

    for t in alvos:
        t = str(t)
        dotted = _MAPA.get(t)
        if dotted is None:
            sem_script.append(t)
        else:
            por_modulo.setdefault(dotted, []).append(t)

    plano = [(m, sorted(ts)) for m, ts in sorted(por_modulo.items())]
    return plano, sorted(set(sem_script))


def validar() -> list[str]:
    """Problemas de convencao encontrados na varredura. Vazio = tudo certo."""
    return list(_PROBLEMAS)


if __name__ == "__main__":
    import sys

    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    print(f"{len(_MAPA)} tabelas mapeadas:\n")
    for tabela, dotted in sorted(_MAPA.items()):
        print(f"  {tabela:34s} {dotted}")

    if _PROBLEMAS:
        print(f"\n{len(_PROBLEMAS)} problema(s) de convencao:")
        for p in _PROBLEMAS:
            print(f"  - {p}")
        sys.exit(1)
    print("\nconvencao ok: todo _TABLE casa com o nome do arquivo")
