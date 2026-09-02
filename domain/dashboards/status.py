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


# ------------------------------------------------------------------ procedimentos


def procedimentos(d: dict) -> list[dict]:
    """Os `procedures` declarados de um dashboard, na ordem de execucao. [] se nao ha.

    Um procedimento e o que ESCREVE artefato: a estimacao de um modelo, um backtest, um
    fetch que nao passa por ETL. Nao e o gerador do relatorio — esse e `module` + run(),
    e continua sendo outra decisao (ver `rodar_procedimento`).
    """
    return d.get("procedures") or []


def por_procedimento(d: dict) -> dict[str, dict]:
    return {p["id"]: p for p in procedimentos(d)}


def proc_por_dep(d: dict) -> dict[str, str]:
    """{ref do artefato: id do procedimento que o grava}, invertido do `writes`.

    A declaracao vive no procedimento (um `writes` com N refs) porque a mesma rodada
    grava varios arquivos — `rodar()` grava sete. A aba precisa da relacao no sentido
    oposto, para marcar cada linha de dependencia com quem a produz.
    """
    out: dict[str, str] = {}
    for p in procedimentos(d):
        for ref in p.get("writes") or []:
            out[ref] = p["id"]
    return out


def comando_procedimento(p: dict) -> str:
    """Comando equivalente, para o modo arquivo copiar — nao e o que o servidor executa.

    O servidor importa `module` e chama `call`; isto e so a versao em texto da mesma
    coisa, para quem abriu o HTML por fora.
    """
    return 'uv run python -c "from %s import %s; %s()"' % (
        p["module"], p["call"], p["call"])


_GRAN_PADRAO = "dia"


def _para_gran(valor, gran: str) -> str | None:
    """Reduz uma data ou um rotulo de trimestre a `gran`, para os dois lados compararem.

    O corte de um procedimento e a fonte dele quase nunca vem na mesma unidade: o painel
    guarda `2026Q3` e a Focus responde `2026-08-28`. Reduzir os dois ao trimestre e o que
    torna a comparacao honesta -- e, mais que isso, e o que da a cada passo a FREQUENCIA
    dele. Um painel trimestral comparado em dia ficaria "atrasado" a cada boletim, e a
    estimacao do modelo seria refeita todo dia mudando os 22 parametros por nada.

    Aceita "YYYY-MM-DD", "YYYY-MM" e "YYYYQn"; devolve None para o que nao for nenhum dos
    tres (ha artefato indexado por numero de reuniao e por nome de parametro).
    """
    if valor is None:
        return None
    s = str(valor).strip()
    ano = s[:4]
    if not (len(ano) == 4 and ano.isdigit()):
        return None
    if gran == "dia":
        return s if len(s) >= 10 else None
    # mes/trimestre: precisa do mes, seja de uma data ou de um rotulo Qn
    if "Q" in s.upper():
        q = s.upper().split("Q", 1)[1][:1]
        if not q.isdigit():
            return None
        mes = (int(q) - 1) * 3 + 1
    elif len(s) >= 7 and s[4] == "-" and s[5:7].isdigit():
        mes = int(s[5:7])
    else:
        return None
    if gran == "mes":
        return "%s-%02d" % (ano, mes)
    return "%sQ%d" % (ano, (mes - 1) // 3 + 1)


def estado_procedimentos(d: dict, estados: dict[str, dict]) -> list[dict]:
    """Uma linha por `procedure`: quando rodou e se o corte dele ficou atras da fonte.

    `atrasado` responde a pergunta que o mtime nao responde. Um artefato tem DUAS datas
    diferentes: quando foi escrito e com que conjunto de informacao. Rodar `salvar()` hoje
    contra o Focus de anteontem produz mtime de hoje e numero de anteontem — e foi
    exatamente isso que passou por "em dia" no caso que motivou esta funcao (2026-08-31:
    relatorio regerado no dia, previsao calculada com Focus de seis dias antes).

    So sai definido onde o procedimento declara `cut_from` (o artefato que grava o proprio
    corte, com `json_date` no dep para o corte ser legivel) e `reads`. Sem os dois,
    `atrasado` fica None e a aba mostra "sem veredito" em vez de inventar um: um CSV
    indexado por trimestre nao tem corte que se compare com o MAX(date) mensal de uma
    tabela, e fingir que tem daria alarme falso todo trimestre.

    NAO entra no `veredito` do dashboard, de proposito. Os vereditos existentes comparam
    o HTML com as fontes dele; isto compara um INSUMO com as fontes. Se virasse
    "desatualizado", `regerar_afetados()` regeraria o relatorio — que nao conserta nada,
    porque o gerador so le o artefato — e continuaria regerando para sempre. Sai como
    sinal proprio (`n_proc_atrasados`) para a aba oferecer a acao certa.
    """
    linhas = []
    for p in procedimentos(d):
        refs_w = p.get("writes") or []
        escritos = [estados[r] for r in refs_w if r in estados]
        mtimes = [e["mtime"] for e in escritos if e.get("mtime")]
        faltando = [r for r in refs_w
                    if r in estados and not estados[r].get("existe")]

        gran = p.get("granularidade") or _GRAN_PADRAO
        cf = p.get("cut_from")
        corte_bruto = estados[cf].get("ultimo") if (cf and cf in estados) else None
        corte = _para_gran(corte_bruto, gran)

        # `reads` aceita tabela E artefato pelo mesmo motivo: a pergunta e "o que eu leio
        # andou depois de mim?", e a resposta nao depende de onde o que eu leio mora. E o
        # que faz a cascata funcionar -- `modelo` le o painel que `painel` grava.
        fontes, fonte_max, fonte_ref = [], None, None
        for r in p.get("reads") or []:
            bruto = estados.get(r, {}).get("ultimo")
            u = _para_gran(bruto, gran)
            fontes.append({"ref": r, "ultimo": bruto, "na_gran": u})
            if u and (fonte_max is None or u > fonte_max):
                fonte_max, fonte_ref = u, r

        atrasado, dias = None, None
        if corte and fonte_max:
            atrasado = corte < fonte_max
            try:
                dias = (datetime.fromisoformat(fonte_max).date()
                        - datetime.fromisoformat(corte).date()).days
            except ValueError:
                dias = None       # trimestre nao tem contagem de dias

        linhas.append({
            "id": p["id"], "label": p.get("label") or p["id"],
            "module": p.get("module"), "call": p.get("call"),
            "seconds": p.get("seconds"), "note": p.get("note"),
            "command": comando_procedimento(p),
            "writes": refs_w, "reads": p.get("reads") or [],
            "cut_from": cf, "corte": corte, "corte_bruto": corte_bruto,
            "granularidade": gran,
            "fontes": fontes, "fonte_max": fonte_max, "fonte_ref": fonte_ref,
            "atrasado": atrasado, "dias_atras": dias,
            "rodou_em": max(mtimes) if mtimes else None,
            "faltando": faltando,
        })
    return linhas


def rodar_procedimento(key: str, proc_id: str, doc: dict | None = None,
                       **kwargs) -> dict:
    """Importa `module` e chama `call` — o irmao de `gerar()` para o lado dos insumos.

    Nao grava stamp e NAO rege o relatorio, de proposito: atualizar o artefato e
    atualizar o HTML sao duas decisoes, e o encadeamento fica visivel em vez de
    automatico — o artefato novo aparece como "dado novo" na linha dele, o dashboard cai
    para "desatualizado", e ai o botao Regerar do card faz sentido. Mesma decisao de
    2026-08-26 que recusou regeracao em lote.

    Sem shell em ponto nenhum, como o `gerar()`: o que chega e um id declarado no
    manifesto, nunca um comando.
    """
    import importlib
    import time

    d = por_chave(doc)[key]
    p = por_procedimento(d).get(proc_id)
    if p is None:
        raise ValueError(f"{key} nao declara procedimento {proc_id!r}")
    if not p.get("module") or not p.get("call"):
        raise ValueError(f"{key}:{proc_id} sem module/call no manifesto")

    mod = importlib.import_module(p["module"])
    fn = getattr(mod, p["call"], None)
    if not callable(fn):
        raise ValueError(f"{p['module']}.{p['call']} nao e chamavel")

    inicio = time.time()
    fn(**kwargs)
    segundos = round(time.time() - inicio, 1)
    return {"key": key, "proc": proc_id, "ok": True, "segundos": segundos,
            "label": p.get("label") or proc_id,
            "rodou_em": datetime.now().isoformat(timespec="seconds")}


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

    `ultimo` e a maior data da coluna declarada (csv), o valor de uma CHAVE declarada
    (`json_date`, para JSON que grava o proprio corte de informacao) ou o ultimo rotulo
    de indice (artifact CSV — os do modelo sao indexados por trimestre). Para os demais
    JSON e para YAML nao ha data interna generica, entao so o mtime responde.

    `json_date` existe porque mtime e a data ERRADA para um artefato calculado: o que
    importa nele nao e quando foi escrito, e com que dado. `antecipa_previsao.json` grava
    `corte_usado`, e le-lo torna o veredito honesto — ver `estado_procedimentos()`.
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
        chave = dep.get("json_date")
        if chave:
            valor = json.loads(caminho.read_text(encoding="utf-8")).get(chave)
            if valor is None:
                info["erro"] = f"json_date {chave!r} ausente no arquivo"
            else:
                info["ultimo"] = str(valor)
        elif col:
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


def _estados_deps(deps: list[dict], live: bool,
                  sql: dict[str, dict] | None = None) -> dict[str, dict]:
    """{ref: estado} para uma lista de dependencias, com os MySQL em lote.

    `sql` pronto salta a consulta: `gerar()` reavalia os procedimentos a cada passo da
    cascata e os artefatos mudam no disco, mas as tabelas nao mudam no meio da rodada.
    """
    if sql is None:
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
        # Indexado por ref porque `estado_procedimentos()` precisa alcancar o estado de
        # uma dependencia a partir do `writes`/`reads`/`cut_from` dela, e nao pela ordem.
        por_ref: dict[str, dict] = {}
        proc_de = proc_por_dep(d)
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
                # Quem GRAVA esta dependencia, quando e um artefato produzido aqui. E o
                # que deixa a linha oferecer a acao certa: rodar o procedimento, nao
                # regerar o relatorio.
                "procedimento": proc_de.get(dep["ref"]),
            })
            deps_out.append(e)
            por_ref[dep["ref"]] = e

        procs = estado_procedimentos(d, por_ref)
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
            # Sinal SEPARADO do veredito, e a separacao e o ponto: veredito compara o
            # HTML com as fontes dele, isto compara um INSUMO com as fontes. Ver a
            # docstring de `estado_procedimentos()`.
            "procedimentos": procs,
            "n_proc": len(procs),
            "n_proc_atrasados": sum(1 for x in procs if x["atrasado"]),
            "stamp_em": (st or {}).get("gerado_em"),
            "deps": deps_out,
        })
    return linhas


# ---------------------------------------------------------------------- afetados


def afetados(tabelas, doc: dict | None = None) -> list[str]:
    """Chaves dos dashboards que LEEM alguma das `tabelas` (nomes sem schema).

    A contrapartida de `domain/db/registry.py`: ele responde "quem ESCREVE esta
    tabela", isto responde "quem LE". E o que fecha o circuito entre atualizar o
    dado e regerar a metrica que sai dele -- sem isso, `update_db.py` termina sem
    saber que o numero que o usuario vai olhar continua sendo o de ontem.

    O manifesto declara a dependencia como `schema.tabela` e o registry/ETL fala em
    nome nu; o casamento e pelo sufixo. Uma colisao de nome entre schemas so causaria
    uma regeracao a mais, nunca a menos -- e quem decide se ela de fato acontece e o
    veredito de `estado()`, nao esta funcao.
    """
    alvo = {str(t).split(".")[-1] for t in tabelas}
    if not alvo:
        return []
    out = []
    for d in dashboards(doc):
        for dep in d["deps"]:
            if dep["kind"] != "mysql" or fora_do_mysql(dep):
                continue
            if dep["ref"].split(".")[-1] in alvo:
                out.append(d["key"])
                break
    return out


def regerar_afetados(tabelas, doc: dict | None = None,
                     vereditos=("desatualizado",)) -> list[dict]:
    """Rege os dashboards que leem `tabelas` E cujo veredito esta em `vereditos`.

    O filtro por veredito e o que separa isto de "regera tudo que toca a tabela":
    depois de um passe de ETL que nao trouxe linha nova, nenhum dashboard fica
    `desatualizado` e nada e regerado. `sem relatorio` fica de fora de proposito --
    construir pela primeira vez um relatorio que nunca existiu e uma decisao, nao
    uma consequencia de atualizar dado.

    Devolve uma linha por dashboard candidato, com `acao` em
    {gerado, falhou, manual, em dia}.
    """
    doc = doc or carregar()
    chaves = afetados(tabelas, doc)
    if not chaves:
        return []

    saida = []
    for l in estado(doc, chaves=chaves):
        if l["veredito"] not in vereditos:
            saida.append({"key": l["key"], "name": l["name"],
                          "acao": "em dia", "veredito": l["veredito"]})
            continue
        if not l.get("module"):
            saida.append({"key": l["key"], "name": l["name"], "acao": "manual",
                          "veredito": l["veredito"], "command": l.get("command")})
            continue
        try:
            r = gerar(l["key"], doc)
            saida.append({"key": l["key"], "name": l["name"], "acao": "gerado",
                          "veredito": l["veredito"], "segundos": r["segundos"],
                          "output": r["output"]})
        except Exception as exc:
            saida.append({"key": l["key"], "name": l["name"], "acao": "falhou",
                          "veredito": l["veredito"],
                          "erro": f"{type(exc).__name__}: {exc}"})
    return saida


# ------------------------------------------------------------------------- gerar


def recalcular_atrasados(key: str, doc: dict | None = None) -> list[dict]:
    """Roda, na ordem declarada, os `procedures` que estiverem atras. Devolve o que fez.

    Reavalia a cada passo em vez de decidir tudo de uma vez, e isso e a CASCATA: se
    `painel` ganhou um trimestre novo, o `modelo` que le o painel passa a estar atras
    dentro da mesma rodada, sem precisar de aresta declarada entre os dois. As tabelas
    sao consultadas uma vez (nao mudam no meio da rodada); os artefatos sao relidos do
    disco a cada passo, porque e justamente o que os passos anteriores mexeram.

    Um passo que falha NAO interrompe: entra como `falhou` e a geracao segue. A estimacao
    depende do IPEADATA e do anexo do RPM, e rede fora do ar nao pode ser motivo para
    ficar sem relatorio nenhum -- o relatorio sai com o artefato antigo, dizendo isso.
    """
    d = por_chave(doc)[key]
    procs = procedimentos(d)
    if not procs:
        return []

    refs_sql = {dep["ref"]: _col(dep) for dep in d["deps"] if dep["kind"] == "mysql"}
    sql = estado_mysql(refs_sql) if refs_sql else {}

    feito = []
    for p in procs:
        estados = _estados_deps(d["deps"], live=False, sql=sql)
        linha = next(x for x in estado_procedimentos(d, estados) if x["id"] == p["id"])
        base = {"id": p["id"], "label": linha["label"], "corte": linha["corte"],
                "fonte_max": linha["fonte_max"], "fonte_ref": linha["fonte_ref"],
                "granularidade": linha["granularidade"]}
        if not linha["atrasado"]:
            # inclui o caso `atrasado is None`: sem veredito nao se roda 4 minutos de
            # estimacao no escuro -- aparece como "sem veredito" e o CLI/`--rodar` cobre.
            feito.append(dict(base, acao="em dia" if linha["atrasado"] is False
                                    else "sem veredito"))
            continue
        try:
            r = rodar_procedimento(key, p["id"], doc)
            feito.append(dict(base, acao="rodado", segundos=r["segundos"]))
        except Exception as exc:                                  # noqa: BLE001
            feito.append(dict(base, acao="falhou",
                              erro=f"{type(exc).__name__}: {exc}"))
    return feito


def gerar(key: str, doc: dict | None = None, recalcular: bool = True,
          **kwargs) -> dict:
    """Recalcula o que esta atras, roda o gerador e grava o stamp — um passo so.

    E o unico botao do lado do consumo, por pedido explicito do usuario (2026-08-31):
    "Atualizar" mexe na base de dados, "Regerar" reconstroi o dashboard, e reconstruir
    inclui refazer as metricas que ficaram atras. Antes disso o recalculo era um terceiro
    botao, e o usuario disse que o processo tinha ficado confuso.

    O que impede isto de virar "roda tudo sempre" e o veredito de cada passo (ver
    `estado_procedimentos`): a granularidade declarada faz o painel trimestral ficar atras
    uma vez por trimestre, nao a cada boletim Focus. Numa rodada tipica de politica
    monetaria isso e ~110s de previsao; quando o trimestre vira, sao ~8 min.

    `recalcular=False` gera sem tocar em artefato — e o que o `--gerar todos` usa, que
    existe para carga inicial de stamp e nao para refazer modelo.

    Dashboards sem `module` (o Oraculo, cujo entry point e um script solto) levantam aqui
    em vez de fingir sucesso — o comando deles esta no manifesto e segue manual.
    """
    import importlib
    import time

    d = por_chave(doc)[key]
    if not d.get("module"):
        raise ValueError(
            f"{key} nao tem module com run(); rode a mao: {d.get('command')}")

    t0 = time.time()
    procs = recalcular_atrasados(key, doc) if recalcular else []

    inicio = time.time()
    mod = importlib.import_module(d["module"])
    mod.run(output=d["output"], **kwargs)
    segundos = round(time.time() - inicio, 1)

    registro = stamp(key, doc)
    return {"key": key, "ok": True, "segundos": segundos,
            "segundos_total": round(time.time() - t0, 1),
            "gerado_em": registro["gerado_em"], "output": d["output"],
            "procedimentos": procs,
            "n_recalculados": sum(1 for x in procs if x["acao"] == "rodado"),
            "n_falhou": sum(1 for x in procs if x["acao"] == "falhou")}


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

    def _existe_modulo(nome: str) -> bool:
        """find_spec() LEVANTA quando o pacote-pai nao existe, em vez de devolver None.

        `find_spec("modulo.que.nao.existe")` faz `__import__("modulo.que")` e propaga
        ModuleNotFoundError -- entao usar o retorno cru aqui derruba `validar()`, que
        existe para RELATAR problemas de declaracao, com um traceback em vez de uma
        linha na lista. Pego pelo teste ao cobrar o caso do modulo inexistente.
        """
        try:
            return importlib.util.find_spec(nome) is not None
        except (ImportError, AttributeError, ValueError):
            return False

    for d in dashboards(doc):
        if d.get("module") and not _existe_modulo(d["module"]):
            problemas.append(f"{d['key']}: modulo nao encontrado: {d['module']}")

    # Procedimentos. O que se cobra aqui e o que envelhece em silencio: um `writes` que
    # aponta para dep que ninguem declarou (o artefato sai da aba e o botao deixa de
    # aparecer), um `call` renomeado (o botao passa a dar 500 no clique) e um `cut_from`
    # cujo dep nao tem `json_date` (o veredito de atraso nunca sai do None, sem erro).
    for d in dashboards(doc):
        procs = procedimentos(d)
        if not procs:
            continue
        # `csv` entra junto de `artifact`: o que separa os dois no manifesto e COMO a data sai
        # do arquivo (coluna declarada vs. rotulo de indice/`json_date`), nao quem o escreve --
        # o `fetch_bcb.py` grava um dep `csv`. Cobrar so `artifact` aqui rejeitaria um `writes`
        # correto.
        refs_art = {dep["ref"] for dep in d["deps"]
                    if dep["kind"] in ("artifact", "csv")}
        refs_sql_d = {dep["ref"] for dep in d["deps"] if dep["kind"] == "mysql"}
        com_json = {dep["ref"] for dep in d["deps"] if dep.get("json_date")}
        vistos_p: set[str] = set()
        for pr in procs:
            pid = pr.get("id")
            if not pid:
                problemas.append(f"{d['key']}: procedimento sem id")
                continue
            if pid in vistos_p:
                problemas.append(f"{d['key']}: id de procedimento duplicado: {pid}")
            vistos_p.add(pid)
            if not pr.get("writes"):
                problemas.append(f"{d['key']}:{pid}: sem `writes` -- nada o liga a uma "
                                 f"dependencia, entao nao aparece na aba")
            for ref in pr.get("writes") or []:
                if ref not in refs_art:
                    problemas.append(f"{d['key']}:{pid}: writes {ref} nao e dep "
                                     f"artifact declarada")
            for ref in pr.get("reads") or []:
                # tabela OU artefato: `modelo` le o painel, nao o banco
                if ref not in refs_sql_d and ref not in refs_art:
                    problemas.append(f"{d['key']}:{pid}: reads {ref} nao e dep declarada "
                                     f"(mysql ou artifact) -- declare para o veredito "
                                     f"de atraso usar o date_col certo")
            gran = pr.get("granularidade", _GRAN_PADRAO)
            if gran not in ("dia", "mes", "trimestre"):
                problemas.append(f"{d['key']}:{pid}: granularidade invalida: {gran!r}")
            cf = pr.get("cut_from")
            if not cf:
                # Sem corte o passo nunca entra no recalculo automatico do Regerar: fica
                # em "sem veredito" para sempre, e nada avisa. E o pior dos silencios.
                problemas.append(f"{d['key']}:{pid}: sem `cut_from` -- o Regerar nunca "
                                 f"vai saber se este passo esta atras")
            else:
                if cf not in (pr.get("writes") or []):
                    problemas.append(f"{d['key']}:{pid}: cut_from {cf} nao esta em writes")
                elif cf.endswith(".json") and cf not in com_json:
                    problemas.append(f"{d['key']}:{pid}: cut_from {cf} e JSON sem "
                                     f"`json_date` no dep -- o corte nunca sera lido")
                if not pr.get("reads"):
                    problemas.append(f"{d['key']}:{pid}: cut_from sem `reads` -- nao ha "
                                     f"contra o que comparar o corte")
                # O corte tem de SER uma data na granularidade declarada. Um CSV longo sem
                # `date_col` devolve o primeiro campo da ultima linha, que pode ser o nome de
                # uma serie ("IPCA_servicos_ma3_sa") -- e ai `atrasado` fica None para sempre,
                # sem erro, exatamente o silencio que esta camada existe para fechar.
                dep_cf = next((x for x in d["deps"] if x["ref"] == cf), None)
                if dep_cf is not None:
                    bruto = estado_arquivo(dep_cf).get("ultimo")
                    if bruto is not None and _para_gran(bruto, gran) is None:
                        problemas.append(
                            f"{d['key']}:{pid}: o corte lido de {cf} nao e data em "
                            f"{gran}: {bruto!r} -- declare `date_col`/`json_date` no dep")

            mod = pr.get("module")
            if not mod or not pr.get("call"):
                problemas.append(f"{d['key']}:{pid}: sem module/call")
            elif not _existe_modulo(mod):
                problemas.append(f"{d['key']}:{pid}: modulo nao encontrado: {mod}")
            else:
                try:
                    import importlib as _il
                    if not callable(getattr(_il.import_module(mod), pr["call"], None)):
                        problemas.append(f"{d['key']}:{pid}: {mod}.{pr['call']} nao e "
                                         f"chamavel")
                except Exception as exc:
                    problemas.append(f"{d['key']}:{pid}: import de {mod} falhou: "
                                     f"{type(exc).__name__}: {exc}")

    return problemas


# --------------------------------------------------------------------------- CLI


def main(argv: list[str] | None = None) -> int:
    import argparse
    import sys

    # Console em UTF-8: o `--gerar` roda geradores que imprimem progresso, e um caractere
    # fora do cp1252 do console do Windows derrubava a geracao pelo print. utils/console.py
    from utils.console import stdout_utf8

    stdout_utf8()

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
    p.add_argument("--rodar", metavar="KEY:PROC",
                   help="roda UM procedimento declarado, sem gerar "
                        "(ex: brasil_monetary_policy:previsao)")
    p.add_argument("--sem-recalcular", action="store_true",
                   help="no --gerar, so gera o HTML: nao refaz metrica atrasada")
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
        todos = args.gerar == "todos"
        chaves = ([d["key"] for d in dashboards(doc) if d.get("module")]
                  if todos else [args.gerar])
        # `--gerar todos` existe para carga inicial de STAMP, nao para refazer modelo:
        # recalcular ali somaria minutos de estimacao a cada um dos onze.
        recalc = not (args.sem_recalcular or todos)
        falhou = False
        for k in chaves:
            try:
                r = gerar(k, doc, recalcular=recalc)
            except Exception as exc:
                falhou = True
                print(f"  {k:28s} FALHOU: {type(exc).__name__}: {exc}")
                continue
            for x in r.get("procedimentos", []):
                if x["acao"] == "rodado":
                    print(f"  {'':28s} recalculou {x['label']} em {x['segundos']}s")
                elif x["acao"] == "falhou":
                    print(f"  {'':28s} AVISO {x['label']} falhou -- {x['erro']}")
                    print(f"  {'':28s}       o relatorio sai com o artefato antigo")
            print(f"  {k:28s} OK em {r['segundos']}s"
                  + (f" (+{r['segundos_total'] - r['segundos']:.0f}s de recalculo)"
                     if r.get("n_recalculados") else ""))
            if r.get("n_falhou"):
                falhou = True
        return 1 if falhou else 0

    if args.rodar:
        chave, _, pid = args.rodar.partition(":")
        if not pid:
            print("use KEY:PROC -- os procedimentos de um dashboard saem no --detalhe")
            return 1
        try:
            r = rodar_procedimento(chave, pid, doc)
        except Exception as exc:
            print(f"  {args.rodar}: FALHOU: {type(exc).__name__}: {exc}")
            return 1
        print(f"  {r['label']}: OK em {r['segundos']}s")
        print("  o artefato mudou; o dashboard passa a aparecer como 'desatualizado' "
              f"-- regere com --gerar {chave}")
        return 0

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
        if linha.get("procedimentos"):
            print("\n  procedimentos (escrevem os artefatos acima):")
            for pr in linha["procedimentos"]:
                if pr["atrasado"] is None:
                    vd = "sem veredito de corte"
                elif pr["atrasado"]:
                    vd = (f"ATRASADO: corte {pr['corte']} < fonte "
                          f"{pr['fonte_max']}"
                          + (f" ({pr['dias_atras']}d)" if pr["dias_atras"]
                             else ""))
                else:
                    vd = f"corte {pr['corte']} em dia com a fonte"
                print(f"    {pr['id']:12s} {pr['label']}  [{pr['granularidade']}]")
                print(f"                 rodou em {pr['rodou_em'] or '-'}"
                      f" | ~{pr['seconds'] or '?'}s | {vd}")
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
