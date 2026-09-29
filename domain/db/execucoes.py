"""
Registro de execucao do ETL: quando cada tabela foi buscada na fonte, se deu certo e se
o dado mudou.

Existe para a aba Divulgacoes do relatorio de calendario parar de DEDUZIR se o banco
esta em dia. A deducao comparava `MAX(date)` contra uma data esperada derivada do
calendario, e cada tabela com data peculiar pedia uma excecao propria (o Focus conta
pela coleta, o Copom pela reuniao, as projecoes pela edicao). Em 2026-09-24 ela errava
para os dois lados ao mesmo tempo: o Copom verde sem a 281a reuniao na vespera, e dois
dos tres grupos laranja do dia eram alarme falso. Ver
`analytics/release_calendar/CLAUDE.md`.

O que substitui a deducao sao tres FATOS, gravados por quem busca o dado:

    ok_em        a ultima vez que o script daquela tabela rodou sem erro
    mudou_em     a ultima execucao sem erro em que o dado MUDOU -- (max, linhas)
                 diferente do registro anterior
    desde        a primeira execucao com medida: antes dela, uma mudanca nao seria
                 percebida
    tentativa_em a ultima vez que alguem tentou, com `ok` e `erro` dela

A pagina compara esses fatos com o momento da divulgacao: saiu as 08:00 e ninguem
buscou depois disso e um fato, nao uma deducao sobre que data a tabela deveria ter.

**Quem grava e o executor, nao o script.** Os tres jobs (`update_db`, `update_us`,
`update_international`) chamam `rodar(mod, kwargs)` em vez de `mod.run(**kwargs)`,
e o botao da pagina passa por `update_db.executar_tabelas()`. Mesma licao do registro
dos dashboards (`domain/dashboards/CLAUDE.md`): um registro paralelo so fica em dia se
for gravado no mesmo ponto por onde o trabalho passa. Um script rodado a mao
(`python -m domain.db...`) nao grava -- a mudanca que ele fez aparece como `mudou_em`
na proxima execucao pelo executor, com o horario dela (ver `_mudou`).

**Falhar ao registrar nunca derruba o ETL.** O dado ja esta no banco; perder o registro
custa uma linha "sem registro" na pagina, e perder a carga custaria o dado.

Um arquivo JSON por tabela em `logs/etl/` (gitignored), gravado de forma atomica. Um
por tabela, e nao um arquivo so, porque a tarefa agendada e o botao podem rodar ao
mesmo tempo -- em tabelas diferentes, quase sempre, e aqui isso basta para nenhum dos
dois sobrescrever o registro do outro.
"""

from __future__ import annotations

import json
import os
import time
from datetime import datetime
from pathlib import Path
from types import ModuleType

_RAIZ = Path(__file__).resolve().parents[2]
_DIR = _RAIZ / "logs" / "etl"
_SCHEMAS = ("macro_brasil", "macro_international", "macro_us")

# Uma tabela com `vintage` guarda EDICOES (o hiato do RPM, as projecoes do Copom): o
# `MAX(date)` dela e o trimestre projetado -- 2029-01-01 nas projecoes, em 2026 --, e
# nao diz nada sobre se a edicao nova chegou. O `MAX(vintage)` diz.
_COLUNAS = ("vintage", "date")


def _agora() -> str:
    return datetime.now().strftime("%Y-%m-%dT%H:%M:%S")


def tabelas_do_modulo(dotted: str) -> list[str]:
    """As tabelas que o registry atribui a este modulo (o inverso de `modulo()`)."""
    from domain.db.registry import tabelas
    return sorted(t for t, m in tabelas().items() if m == dotted)


# ------------------------------------------------------------------------ banco

def medir(tabelas) -> dict[str, dict]:
    """{tabela: {schema, coluna, max, linhas}} lido agora do banco, numa consulta so.

    `coluna` e a que responde "qual o dado mais novo": `vintage` quando a tabela tem,
    senao `date`, senao None (as tabelas de dimensao, que so tem contagem). Tabela que
    nao existe no banco fica de fora do resultado.
    """
    tabelas = sorted({str(t) for t in tabelas})
    if not tabelas:
        return {}

    import mysql.connector
    from dotenv import load_dotenv

    load_dotenv(_RAIZ / ".env")
    conn = mysql.connector.connect(
        host=os.environ.get("MYSQL_HOST", "localhost"),
        user=os.environ.get("MYSQL_USER", "root"),
        password=os.environ.get("MYSQL_PASSWORD", ""),
    )
    try:
        cur = conn.cursor()
        ph_s = ", ".join(["%s"] * len(_SCHEMAS))
        ph_t = ", ".join(["%s"] * len(tabelas))
        cur.execute(
            "SELECT table_schema, table_name FROM information_schema.tables "
            f"WHERE table_schema IN ({ph_s}) AND table_name IN ({ph_t}) "
            "AND table_type = 'BASE TABLE'",
            (*_SCHEMAS, *tabelas),
        )
        schema = {t: s for s, t in cur.fetchall()}
        if not schema:
            return {}

        cur.execute(
            "SELECT table_name, column_name FROM information_schema.columns "
            f"WHERE table_schema IN ({ph_s}) AND table_name IN ({ph_t}) "
            f"AND column_name IN ({', '.join(['%s'] * len(_COLUNAS))})",
            (*_SCHEMAS, *tabelas, *_COLUNAS),
        )
        cols: dict[str, set] = {}
        for t, c in cur.fetchall():
            cols.setdefault(t, set()).add(c)

        out: dict[str, dict] = {}
        partes = []
        for t in sorted(schema):
            coluna = next((c for c in _COLUNAS if c in cols.get(t, ())), None)
            out[t] = {"schema": schema[t], "coluna": coluna, "max": None, "linhas": None}
            mx = f"MAX(`{coluna}`)" if coluna else "NULL"
            partes.append(f"SELECT '{t}' AS t, {mx} AS mx, COUNT(*) AS n "
                          f"FROM `{schema[t]}`.`{t}`")
        cur.execute(" UNION ALL ".join(partes))
        for t, mx, n in cur.fetchall():
            out[t]["max"] = str(mx) if mx is not None else None
            out[t]["linhas"] = int(n) if n is not None else None
        cur.close()
    finally:
        conn.close()
    return out


def _medir_seguro(tabelas) -> dict[str, dict] | None:
    try:
        return medir(tabelas)
    except Exception as exc:
        print(f"  [registro] nao deu para medir {', '.join(tabelas)} "
              f"({type(exc).__name__}: {exc})")
        return None


# ---------------------------------------------------------------------- arquivo

def _caminho(tabela: str) -> Path:
    return _DIR / f"{tabela}.json"


def ler(tabelas=None) -> dict[str, dict]:
    """{tabela: registro}. Sem `tabelas`, tudo o que ja foi registrado."""
    if tabelas is None:
        arquivos = sorted(_DIR.glob("*.json")) if _DIR.exists() else []
    else:
        arquivos = [_caminho(str(t)) for t in tabelas]
    out: dict[str, dict] = {}
    for p in arquivos:
        try:
            out[p.stem] = json.loads(p.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            continue
    return out


def _gravar(tabela: str, registro: dict) -> None:
    """Escrita atomica: um leitor nunca ve um JSON pela metade.

    Tres tentativas porque a pasta vive dentro do Dropbox, que segura um arquivo por
    alguns milissegundos enquanto sincroniza -- e no Windows isso faz o `os.replace`
    falhar com PermissionError.
    """
    _DIR.mkdir(parents=True, exist_ok=True)
    destino = _caminho(tabela)
    tmp = destino.with_suffix(f".{os.getpid()}.tmp")
    tmp.write_text(json.dumps(registro, ensure_ascii=False, indent=1), encoding="utf-8")
    for k in range(3):
        try:
            os.replace(tmp, destino)
            return
        except PermissionError:
            if k == 2:
                tmp.unlink(missing_ok=True)
                raise
            time.sleep(0.2)


def _mudou(antes: dict | None, depois: dict | None, anterior: dict) -> bool | None:
    """O dado desta tabela mudou desde o ultimo registro? None quando nao da para dizer.

    A base da comparacao e o ULTIMO REGISTRO, nao a medida de antes desta execucao --
    senao uma mudanca feita por um script rodado a mao entre duas execucoes registradas
    nunca apareceria: antes e depois desta execucao seriam iguais. Com o registro como
    base, ela aparece com o horario desta execucao, que e mais tarde do que de fato foi
    e continua sendo depois da divulgacao, que e o que a pagina pergunta.

    So no primeiro registro de uma tabela a base e a medida de antes -- e ai o que se
    responde e so "esta execucao mudou alguma coisa?".
    """
    if depois is None:
        return None
    if anterior and "max" in anterior:
        base = anterior
    elif antes is not None:
        base = antes
    else:
        return None
    return (base.get("max"), base.get("linhas")) != (depois.get("max"), depois.get("linhas"))


def registrar(tabelas, *, modulo: str, inicio: str, ok: bool, erro: str | None = None,
              antes: dict | None = None, depois: dict | None = None) -> None:
    """Grava o registro de cada tabela de uma execucao.

    `desde` e a primeira execucao com medida desta tabela -- o momento a partir do qual
    uma mudanca no dado seria percebida. E ele que deixa a pagina distinguir "buscou
    depois da divulgacao e nada mudou" (uma afirmacao) de "buscou depois, mas o dado
    pode ter chegado antes de existir registro" (nao se sabe). Sem ele, no primeiro dia
    toda divulgacao ja no banco apareceria como "sem dado novo", em dourado.
    """
    for t in tabelas:
        anterior = ler([t]).get(t, {})
        reg = dict(anterior)
        reg.update({"tabela": t, "modulo": modulo, "tentativa_em": inicio,
                    "ok": ok, "erro": erro})
        if ok:
            reg["ok_em"] = inicio
            d = (depois or {}).get(t)
            if d is not None:
                mudou = _mudou((antes or {}).get(t) if antes is not None else None,
                               d, anterior)
                reg.update({"coluna": d.get("coluna"), "max": d.get("max"),
                            "linhas": d.get("linhas")})
                if not reg.get("desde"):
                    reg["desde"] = inicio
                if mudou:
                    reg["mudou_em"] = inicio
        reg.setdefault("ok_em", None)
        reg.setdefault("mudou_em", None)
        reg.setdefault("desde", None)
        _gravar(t, reg)


def _registrar_seguro(tabelas, **kw) -> None:
    try:
        registrar(tabelas, **kw)
    except Exception as exc:
        print(f"  [registro] {', '.join(tabelas)}: nao registrado "
              f"({type(exc).__name__}: {exc}) -- a carga seguiu normalmente")


# --------------------------------------------------------------------- executor

def rodar(mod: ModuleType, kwargs: dict | None = None) -> None:
    """`mod.run(**kwargs)`, registrando a execucao de cada tabela do modulo.

    Relanca a excecao do script depois de registrar a falha: quem chama continua
    decidindo o que um erro significa (os jobs seguem para o proximo script).
    """
    tabelas = tabelas_do_modulo(mod.__name__)
    inicio = _agora()
    antes = _medir_seguro(tabelas) if tabelas else None
    try:
        mod.run(**(kwargs or {}))
    except Exception as exc:
        if tabelas:
            _registrar_seguro(tabelas, modulo=mod.__name__, inicio=inicio, ok=False,
                              erro=f"{type(exc).__name__}: {exc}")
        raise
    if tabelas:
        depois = _medir_seguro(tabelas)
        _registrar_seguro(tabelas, modulo=mod.__name__, inicio=inicio, ok=True,
                          antes=antes, depois=depois)
