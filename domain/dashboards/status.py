"""
Estado de cada dashboard: do que ele depende, o que a fonte tem hoje, e se o arquivo
gerado ja esta atras disso.

Le `manifest.yaml` (a declaracao de quem consome o que) e resolve o estado AO VIVO de
cada dependencia:

    mysql     MAX(<date_col>) da tabela — um UNION ALL so para todas, nao 70 round-trips
    csv       maior valor da coluna de data declarada
    artifact  mtime + ultimo indice do arquivo (os CSVs do modelo sao indexados por
              trimestre, entao a ultima linha ja diz ate quando o modelo foi rodado)
    yaml      mtime
    live      ultima observacao na fonte (hoje so FRED), so quando `live=True`

E compara com o STAMP — o retrato que `stamp()` grava no momento em que o relatorio e
gerado. Sem stamp nao da para afirmar "esta desatualizado": o mtime do HTML diz quando
ele foi gerado, mas nao o que havia dentro. Com stamp a afirmacao vira exata: "o banco
tem IPCA de agosto, o relatorio foi feito com ate julho".

Uso:

    uv run python -m domain.dashboards.status                    # tabela de estado
    uv run python -m domain.dashboards.status --validar          # so a checagem
    uv run python -m domain.dashboards.status --gerar brasil_credit
    uv run python -m domain.dashboards.status --live             # inclui FRED

`gerar(key)` e o ponto de entrada unico: roda o run() do modulo e grava o stamp no
mesmo passo. Gerar um relatorio por fora (chamando o generate_report direto) continua
funcionando, so deixa o stamp para tras — e isso aparece na aba como "gerado fora do
fluxo" em vez de virar um veredito errado.

Por que a consulta de MySQL nao reusa `domain.release_calendar.sync.estado_banco()`:
aquela varre schemas inteiros assumindo a coluna `date` e chaveia por nome de tabela.
Aqui a chave precisa ser `schema.tabela` (o manifesto alcanca `base_mercado`, de outro
projeto) e a coluna de data varia por dependencia (`inflc_cpi_pesos` e anual, por
`reference_period`; as tres tabelas de dimensao nao tem data nenhuma). Sao perguntas
diferentes sobre o mesmo banco.
"""

from __future__ import annotations

import json
import os
from datetime import datetime
from pathlib import Path

import yaml

_RAIZ = Path(__file__).resolve().parents[2]
_MANIFEST = Path(__file__).parent / "manifest.yaml"
_STAMPS = _RAIZ / "reports" / ".build"

# Coluna de data default de uma dependencia mysql. `date_col: null` no manifesto
# desliga a leitura de data (tabela de dimensao) e deixa so a contagem de linhas.
_COL_PADRAO = "date"

_SCHEMAS_PROPRIOS = ("macro_brasil", "macro_international", "macro_us")


# --------------------------------------------------------------------- manifesto


def carregar(path: Path | str = _MANIFEST) -> dict:
    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f)


def dashboards(doc: dict | None = None) -> list[dict]:
    return (doc or carregar())["dashboards"]


def por_chave(doc: dict | None = None) -> dict[str, dict]:
    return {d["key"]: d for d in dashboards(doc)}


def _col(dep: dict) -> str | None:
    """Coluna de data da dependencia. Ausente = default; presente e null = sem data."""
    return dep.get("date_col", _COL_PADRAO) if "date_col" in dep else _COL_PADRAO


def _onde(dep: dict) -> str:
    """Rotulo de ONDE o dado mora — a pergunta "esta no MySQL ou fora dele?"."""
    kind = dep["kind"]
    if kind == "mysql":
        return dep["ref"].split(".", 1)[0]
    if kind == "live":
        return dep["ref"].split(":", 1)[0]
    return "arquivo"


def fora_do_mysql(dep: dict) -> bool:
    """True quando o dado nao vem de um schema alimentado por este projeto.

    `base_mercado` conta como fora: e MySQL, mas quem escreve e o CentralManagement,
    entao rodar qualquer ETL daqui nao a move.
    """
    if dep["kind"] != "mysql":
        return True
    return dep["ref"].split(".", 1)[0] not in _SCHEMAS_PROPRIOS


# ------------------------------------------------------------------------ MySQL


def _conectar():
    import mysql.connector
    from dotenv import load_dotenv

    load_dotenv(_RAIZ / ".env")
    return mysql.connector.connect(
        host=os.environ.get("MYSQL_HOST", "localhost"),
        user=os.environ.get("MYSQL_USER", "root"),
        password=os.environ.get("MYSQL_PASSWORD", ""),
    )


def estado_mysql(refs: dict[str, str | None]) -> dict[str, dict]:
    """{`schema.tabela`: {ultimo, linhas, existe, erro}} para as refs informadas.

    `refs` mapeia ref -> coluna de data (None = tabela sem serie temporal).

    Duas consultas, nao duas por tabela: um UNION ALL para os MAX (0,1s para as ~70
    do manifesto, porque cada MAX usa indice) e o `table_rows` do information_schema
    para a contagem. A contagem sai APROXIMADA de proposito — COUNT(*) exato custa
    varredura completa e levava 7,6s no mesmo conjunto, so para preencher uma coluna
    informativa.
    """
    out = {r: {"ultimo": None, "linhas": None, "existe": False, "erro": None}
           for r in refs}
    try:
        conn = _conectar()
    except Exception as exc:
        for r in out:
            out[r]["erro"] = f"{type(exc).__name__}: {exc}"
        return out

    try:
        cur = conn.cursor()

        cur.execute(
            "SELECT CONCAT(table_schema, '.', table_name), table_rows "
            "FROM information_schema.tables WHERE table_type = 'BASE TABLE'"
        )
        existentes = dict(cur.fetchall())
        for r in out:
            if r in existentes:
                out[r]["existe"] = True
                out[r]["linhas"] = existentes[r]
            else:
                out[r]["erro"] = "tabela nao existe no banco"

        partes = []
        for ref, col in refs.items():
            if not col or not out[ref]["existe"]:
                continue
            schema, tabela = ref.split(".", 1)
            # Nomes vem do manifesto (nosso), nunca da pagina; backticks de todo jeito.
            partes.append(
                f"SELECT '{ref}' AS r, MAX(`{col}`) AS mx "
                f"FROM `{schema}`.`{tabela}`"
            )
        if partes:
            cur.execute(" UNION ALL ".join(partes))
            for ref, mx in cur.fetchall():
                out[ref]["ultimo"] = _iso(mx)

        cur.close()
    except Exception as exc:
        for r in out:
            if out[r]["erro"] is None:
                out[r]["erro"] = f"{type(exc).__name__}: {exc}"
    finally:
        conn.close()

    return out


def _iso(valor) -> str | None:
    if valor is None:
        return None
    if isinstance(valor, datetime):
        return valor.date().isoformat()
    if hasattr(valor, "isoformat"):
        return valor.isoformat()
    return str(valor)


# ---------------------------------------------------------------------- arquivos


def estado_arquivo(dep: dict) -> dict:
    """{ultimo, mtime, existe, erro} para dependencia csv/artifact/yaml.

    `ultimo` e a maior data da coluna declarada (csv) ou o ultimo rotulo de indice
    (artifact CSV — os do modelo sao indexados por trimestre). Para JSON e YAML nao ha
    data interna generica, entao so o mtime responde.
    """
    caminho = _RAIZ / dep["ref"]
    info = {"ultimo": None, "mtime": None, "existe": caminho.exists(), "erro": None}
    if not info["existe"]:
        info["erro"] = "arquivo nao existe"
        return info

    info["mtime"] = datetime.fromtimestamp(caminho.stat().st_mtime).isoformat(
        timespec="seconds")

    try:
        col = dep.get("date_col")
        if col:
            import pandas as pd

            serie = pd.read_csv(caminho, usecols=[col], encoding="utf-8-sig")[col]
            serie = serie.dropna()
            if len(serie):
                info["ultimo"] = str(max(str(v) for v in serie))
        elif caminho.suffix == ".csv":
            info["ultimo"] = _ultimo_indice(caminho)
    except Exception as exc:
        info["erro"] = f"{type(exc).__name__}: {exc}"

    return info


def _ultimo_indice(caminho: Path) -> str | None:
    """Primeiro campo da ultima linha nao vazia — o rotulo do indice num CSV indexado.

    Le so o fim do arquivo: os artefatos do modelo sao pequenos, mas a mesma funcao
    serve para qualquer um deles e nao ha motivo para carregar o arquivo inteiro.
    """
    with open(caminho, "rb") as f:
        f.seek(0, os.SEEK_END)
        tamanho = f.tell()
        bloco = min(8192, tamanho)
        f.seek(tamanho - bloco)
        linhas = [ln for ln in f.read().decode("utf-8", "replace").splitlines()
                  if ln.strip()]
    if len(linhas) < 2:          # so cabecalho (ou nada) nao e indice
        return None
    return linhas[-1].split(",", 1)[0].strip() or None


# -------------------------------------------------------------------------- FRED


def estado_live(ref: str) -> dict:
    """Ultima observacao publicada na fonte externa. Hoje so `FRED:<serie>`.

    Uma chamada de metadado por serie (`get_series_info`), nao o download da serie.
    Falha de rede/chave devolve `erro` — a aba mostra "indisponivel" e segue.
    """
    info = {"ultimo": None, "existe": True, "erro": None}
    fonte, _, serie = ref.partition(":")
    if fonte != "FRED":
        info["erro"] = f"fonte live desconhecida: {fonte}"
        return info
    try:
        from connectors.fred import _fred

        meta = _fred().get_series_info(serie)
        info["ultimo"] = _iso(meta.get("observation_end"))
    except Exception as exc:
        info["erro"] = f"{type(exc).__name__}: {exc}"
    return info


# ------------------------------------------------------------------------ stamps


def caminho_stamp(key: str) -> Path:
    return _STAMPS / f"{key}.json"


def ler_stamp(key: str) -> dict | None:
    p = caminho_stamp(key)
    if not p.exists():
        return None
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None


def stamp(key: str, doc: dict | None = None) -> dict:
    """Grava o retrato das dependencias de `key` — chamado logo apos gerar.

    O que fica registrado e o `ultimo` de cada dependencia NAQUELE momento, que e
    exatamente o que o relatorio acabou de embutir. A comparacao posterior contra o
    estado ao vivo e o que produz o veredito.
    """
    d = por_chave(doc)[key]
    estados = _estados_deps(d["deps"], live=False)
    saida = _RAIZ / d["output"]
    registro = {
        "key": key,
        "gerado_em": datetime.now().isoformat(timespec="seconds"),
        "output_mtime": (datetime.fromtimestamp(saida.stat().st_mtime)
                         .isoformat(timespec="seconds") if saida.exists() else None),
        # Em nanossegundos, e nao a string acima, porque e este campo que decide se o
        # arquivo foi regerado por fora depois do stamp. Com resolucao de segundo,
        # gerar a mao no mesmo segundo do stamp passava por "em dia".
        "output_mtime_ns": saida.stat().st_mtime_ns if saida.exists() else None,
        "deps": {dep["ref"]: estados[dep["ref"]].get("ultimo")
                 for dep in d["deps"]},
    }
    _STAMPS.mkdir(parents=True, exist_ok=True)
    caminho_stamp(key).write_text(
        json.dumps(registro, ensure_ascii=False, indent=2), encoding="utf-8")
    return registro


# ------------------------------------------------------------------------ estado


def _estados_deps(deps: list[dict], live: bool) -> dict[str, dict]:
    """{ref: estado} para uma lista de dependencias, com os MySQL em lote."""
    refs_sql = {d["ref"]: _col(d) for d in deps if d["kind"] == "mysql"}
    sql = estado_mysql(refs_sql) if refs_sql else {}

    out: dict[str, dict] = {}
    for dep in deps:
        if dep["kind"] == "mysql":
            out[dep["ref"]] = sql[dep["ref"]]
        elif dep["kind"] == "live":
            out[dep["ref"]] = (estado_live(dep["ref"]) if live else
                               {"ultimo": None, "existe": True,
                                "erro": None, "nao_checado": True})
        else:
            out[dep["ref"]] = estado_arquivo(dep)
    return out


def estado(doc: dict | None = None, live: bool = False,
           chaves: list[str] | None = None) -> list[dict]:
    """Uma linha por dashboard, pronta para a aba "Status dashboard".

    Todos os MySQL de todos os dashboards saem em UMA consulta (a mesma tabela
    aparece em varios relatorios — `inflc_agregados` em cinco), entao o custo nao
    cresce com o numero de dashboards.
    """
    doc = doc or carregar()
    alvos = [d for d in dashboards(doc)
             if chaves is None or d["key"] in chaves]

    todas = [dep for d in alvos for dep in d["deps"]]
    refs_sql = {dep["ref"]: _col(dep) for dep in todas if dep["kind"] == "mysql"}
    sql = estado_mysql(refs_sql) if refs_sql else {}

    linhas = []
    for d in alvos:
        st = ler_stamp(d["key"])
        saida = _RAIZ / d["output"]
        existe = saida.exists()
        mtime = (datetime.fromtimestamp(saida.stat().st_mtime).isoformat(timespec="seconds")
                 if existe else None)
        mtime_ns = saida.stat().st_mtime_ns if existe else None

        deps_out = []
        for dep in d["deps"]:
            if dep["kind"] == "mysql":
                e = dict(sql[dep["ref"]])
            elif dep["kind"] == "live":
                e = (estado_live(dep["ref"]) if live else
                     {"ultimo": None, "existe": True, "erro": None, "nao_checado": True})
            else:
                e = estado_arquivo(dep)

            stamped = (st or {}).get("deps", {}).get(dep["ref"])
            e.update({
                "ref": dep["ref"],
                "kind": dep["kind"],
                "role": dep.get("role"),
                "scope": dep.get("scope", "dados"),
                "owner": dep.get("owner"),
                "refresh": dep.get("refresh"),
                "note": dep.get("note"),
                "onde": _onde(dep),
                "fora_do_mysql": fora_do_mysql(dep),
                "stamp": stamped,
                "novo": bool(stamped and e.get("ultimo") and
                             str(e["ultimo"]) > str(stamped)),
                # Sinal que funciona mesmo SEM stamp: um artefato reescrito depois do
                # HTML nao esta dentro dele, ponto -- nao depende de retrato nenhum.
                "arquivo_mais_novo": bool(
                    mtime and e.get("mtime") and e["mtime"] > mtime),
            })
            deps_out.append(e)

        novos = [e for e in deps_out if e["novo"] or e["arquivo_mais_novo"]]
        faltando = [e for e in deps_out if e.get("erro")]

        if not existe:
            veredito = "sem relatorio"
        elif novos:
            veredito = "desatualizado"
        elif st is None or (st.get("output_mtime_ns") != mtime_ns):
            # Stamp ausente, ou gerado por fora (o arquivo mudou depois do stamp):
            # da para mostrar o estado das fontes, nao da para afirmar que bate.
            veredito = "sem stamp"
        else:
            veredito = "em dia"

        linhas.append({
            "key": d["key"], "name": d["name"], "area": d.get("area"),
            "output": d["output"], "module": d.get("module"),
            "command": d.get("command"), "build_seconds": d.get("build_seconds"),
            "note": d.get("note"),
            "existe": existe, "gerado_em": mtime,
            "tamanho_mb": round(saida.stat().st_size / 1048576, 1) if existe else None,
            "veredito": veredito,
            "n_deps": len(deps_out),
            "n_fora_mysql": sum(1 for e in deps_out if e["fora_do_mysql"]),
            "n_novos": len(novos),
            "n_erro": len(faltando),
            "stamp_em": (st or {}).get("gerado_em"),
            "deps": deps_out,
        })
    return linhas


# ------------------------------------------------------------------------- gerar


def gerar(key: str, doc: dict | None = None, **kwargs) -> dict:
    """Roda o gerador do dashboard e grava o stamp no mesmo passo.

    E o ponto de entrada que o botao da aba vai chamar. Dashboards sem `module`
    (o Oraculo, cujo entry point e um script solto) levantam aqui em vez de fingir
    sucesso — o comando deles esta no manifesto e continua sendo manual.
    """
    import importlib
    import time

    d = por_chave(doc)[key]
    if not d.get("module"):
        raise ValueError(
            f"{key} nao tem module com run(); rode a mao: {d.get('command')}")

    inicio = time.time()
    mod = importlib.import_module(d["module"])
    mod.run(output=d["output"], **kwargs)
    segundos = round(time.time() - inicio, 1)

    registro = stamp(key, doc)
    return {"key": key, "ok": True, "segundos": segundos,
            "gerado_em": registro["gerado_em"], "output": d["output"]}


# ---------------------------------------------------------------------- validar


def validar(doc: dict | None = None) -> list[str]:
    """Problemas de declaracao. Vazio = manifesto bate com a realidade.

    Cobra o que da para cobrar sem adivinhar consumo: chave duplicada, tabela
    declarada que nao existe no banco, arquivo declarado que nao existe em disco,
    modulo que nao importa. NAO cobra o inverso (tabela lida pelo codigo e nao
    declarada aqui) — isso exigiria derivar consumo, que e justamente o que o
    manifesto existe para substituir.
    """
    doc = doc or carregar()
    problemas: list[str] = []

    vistos = set()
    for d in dashboards(doc):
        if d["key"] in vistos:
            problemas.append(f"chave duplicada: {d['key']}")
        vistos.add(d["key"])
        if not d.get("deps"):
            problemas.append(f"{d['key']}: sem dependencias declaradas")
        for dep in d.get("deps", []):
            if dep["kind"] not in ("mysql", "csv", "artifact", "yaml", "live"):
                problemas.append(f"{d['key']}: kind desconhecido {dep['kind']!r} "
                                 f"em {dep['ref']}")
            if dep["kind"] == "mysql" and "." not in dep["ref"]:
                problemas.append(f"{d['key']}: ref mysql sem schema: {dep['ref']}")
            if dep["kind"] in ("csv", "artifact", "yaml"):
                if not (_RAIZ / dep["ref"]).exists():
                    problemas.append(f"{d['key']}: arquivo declarado nao existe: "
                                     f"{dep['ref']}")

    refs_sql = {dep["ref"]: None
                for d in dashboards(doc) for dep in d["deps"]
                if dep["kind"] == "mysql"}
    if refs_sql:
        for ref, e in estado_mysql(refs_sql).items():
            if e["erro"]:
                problemas.append(f"mysql {ref}: {e['erro']}")

    import importlib.util
    for d in dashboards(doc):
        if d.get("module") and importlib.util.find_spec(d["module"]) is None:
            problemas.append(f"{d['key']}: modulo nao encontrado: {d['module']}")

    return problemas


# --------------------------------------------------------------------------- CLI


def main(argv: list[str] | None = None) -> int:
    import argparse
    import sys

    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    p = argparse.ArgumentParser(description=__doc__.splitlines()[1])
    p.add_argument("--validar", action="store_true",
                   help="so checa o manifesto contra o banco/disco e sai")
    p.add_argument("--live", action="store_true",
                   help="consulta tambem as fontes live (FRED)")
    p.add_argument("--gerar", metavar="KEY",
                   help="gera esse dashboard e grava o stamp ('todos' para todos)")
    p.add_argument("--detalhe", metavar="KEY",
                   help="lista dependencia por dependencia de um dashboard")
    args = p.parse_args(argv)

    doc = carregar()

    if args.validar:
        problemas = validar(doc)
        if not problemas:
            print("manifesto ok: toda tabela e todo arquivo declarado existe")
            return 0
        print(f"{len(problemas)} problema(s):")
        for x in problemas:
            print(f"  - {x}")
        return 1

    if args.gerar:
        chaves = ([d["key"] for d in dashboards(doc) if d.get("module")]
                  if args.gerar == "todos" else [args.gerar])
        falhou = False
        for k in chaves:
            try:
                r = gerar(k, doc)
                print(f"  {k:28s} OK em {r['segundos']}s")
            except Exception as exc:
                falhou = True
                print(f"  {k:28s} FALHOU: {type(exc).__name__}: {exc}")
        return 1 if falhou else 0

    if args.detalhe:
        linha = estado(doc, live=args.live, chaves=[args.detalhe])[0]
        print(f"{linha['name']}  [{linha['veredito']}]")
        print(f"  saida     {linha['output']}")
        print(f"  gerado em {linha['gerado_em'] or '(nunca)'}")
        print()
        for e in linha["deps"]:
            marca = "NOVO" if (e["novo"] or e["arquivo_mais_novo"]) else "    "
            fora = "*" if e["fora_do_mysql"] else " "
            print(f"  {marca} {fora}{e['onde']:20s} {e['ref']:58s} "
                  f"{str(e['ultimo'] or e.get('mtime') or e.get('erro') or '—')}")
        print("\n  * = fora dos schemas alimentados por este projeto")
        return 0

    linhas = estado(doc, live=args.live)
    print(f"{'dashboard':28s} {'veredito':14s} {'gerado em':20s} "
          f"{'deps':>5s} {'fora':>5s} {'novos':>6s}")
    for l in linhas:
        print(f"{l['name']:28s} {l['veredito']:14s} "
              f"{(l['gerado_em'] or '—'):20s} {l['n_deps']:5d} "
              f"{l['n_fora_mysql']:5d} {l['n_novos']:6d}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
