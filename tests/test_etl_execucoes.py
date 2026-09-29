# -*- coding: utf-8 -*-
"""
Testa domain/db/execucoes.py -- o registro de quando cada tabela foi buscada e se o
dado mudou, que a aba Divulgacoes do calendario le desde 2026-09-24.

Sem banco: `medir()` e trocado por uma sequencia de medidas fabricadas, e o diretorio
de registro por uma pasta temporaria. O que se afirma e a regra de cada campo, que e
onde um erro nao levantaria nada -- so poria a palavra errada ao lado de um botao.

Roda com:
    uv run python tests/test_etl_execucoes.py
"""

import json
import pathlib
import re
import sys
import tempfile
import types

from domain.db import execucoes as E

falhas = []


def check(rotulo, cond, extra=""):
    print(("  ok     " if cond else "  FALHA  ") + rotulo
          + (f"  -> {extra}" if extra != "" and not cond else ""))
    if not cond:
        falhas.append(rotulo)


TMP = pathlib.Path(tempfile.mkdtemp(prefix="etl_exec_"))
E._DIR = TMP
E.tabelas_do_modulo = lambda dotted: ["t_a", "t_b"] if dotted == "fake.mod" else []

_fila = []


def _medir_fake(tabelas):
    """Devolve a proxima medida da fila; um item Exception simula o banco fora."""
    item = _fila.pop(0)
    if isinstance(item, Exception):
        raise item
    return {t: dict(item[t], schema="macro_brasil", coluna="date") for t in tabelas if t in item}


E.medir = _medir_fake

_relogio = iter(f"2026-09-24T10:{m:02d}:00" for m in range(60))
E._agora = lambda: next(_relogio)


def mod(run):
    m = types.ModuleType("fake.mod")
    m.run = run
    return m


def med(ma, la, mb, lb):
    return {"t_a": {"max": ma, "linhas": la}, "t_b": {"max": mb, "linhas": lb}}


def reg(t):
    return json.loads((TMP / f"{t}.json").read_text(encoding="utf-8"))


print("1. primeira execucao, o dado muda nela")
_fila[:] = [med("2026-07-01", 10, "2026-07-01", 5), med("2026-08-01", 11, "2026-07-01", 5)]
E.rodar(mod(lambda: None))
a, b = reg("t_a"), reg("t_b")
check("grava um arquivo por tabela do modulo", a["tabela"] == "t_a" and b["tabela"] == "t_b")
check("ok_em e o INICIO da execucao", a["ok_em"] == "2026-09-24T10:00:00", a["ok_em"])
check("a tabela que mudou ganha mudou_em", a["mudou_em"] == "2026-09-24T10:00:00", a)
check("a que nao mudou fica sem mudou_em", b["mudou_em"] is None, b)
check("guarda o que o banco tem depois", a["max"] == "2026-08-01" and a["linhas"] == 11, a)
check("desde = a primeira execucao com medida", a["desde"] == "2026-09-24T10:00:00", a)

print("\n2. segunda execucao sem mudanca: mudou_em e desde NAO andam")
_fila[:] = [med("2026-08-01", 11, "2026-07-01", 5), med("2026-08-01", 11, "2026-07-01", 5)]
E.rodar(mod(lambda: None))
a = reg("t_a")
check("ok_em anda", a["ok_em"] == "2026-09-24T10:01:00", a["ok_em"])
check("mudou_em fica na execucao que mudou", a["mudou_em"] == "2026-09-24T10:00:00", a["mudou_em"])
check("desde fica no primeiro registro", a["desde"] == "2026-09-24T10:00:00", a["desde"])

print("\n3. mudanca feita FORA do executor (script rodado a mao) entre duas execucoes")
# O banco ja tem o dado novo antes desta execucao comecar; antes == depois nela. So
# comparando com o REGISTRO anterior a mudanca aparece -- com a medida de antes, nunca.
_fila[:] = [med("2026-09-01", 12, "2026-07-01", 5), med("2026-09-01", 12, "2026-07-01", 5)]
E.rodar(mod(lambda: None))
a = reg("t_a")
check("a mudanca aparece, com o horario desta execucao",
      a["mudou_em"] == "2026-09-24T10:02:00", a["mudou_em"])

print("\n4. o script falha")


def _quebra():
    raise RuntimeError("HTTPError: 503")


_fila[:] = [med("2026-09-01", 12, "2026-07-01", 5)]
try:
    E.rodar(mod(_quebra))
    relancou = False
except RuntimeError:
    relancou = True
a = reg("t_a")
check("a excecao do script chega a quem chamou", relancou)
check("ok=False e o erro gravado", a["ok"] is False and "503" in (a["erro"] or ""), a)
check("tentativa_em anda", a["tentativa_em"] == "2026-09-24T10:03:00", a["tentativa_em"])
check("ok_em fica na ultima execucao BOA", a["ok_em"] == "2026-09-24T10:02:00", a["ok_em"])
check("mudou_em nao anda numa falha", a["mudou_em"] == "2026-09-24T10:02:00", a["mudou_em"])

print("\n5. sucesso depois da falha limpa o erro")
_fila[:] = [med("2026-09-01", 12, "2026-07-01", 5), med("2026-09-01", 12, "2026-07-01", 5)]
E.rodar(mod(lambda: None))
a = reg("t_a")
check("ok volta a True e erro a None", a["ok"] is True and a["erro"] is None, a)

print("\n6. banco fora na hora de medir: o ETL segue e o registro nao inventa mudanca")
_fila[:] = [OSError("banco fora"), OSError("banco fora")]
roda = []
E.rodar(mod(lambda: roda.append(1)))
a = reg("t_a")
check("o script rodou mesmo sem medida", roda == [1])
check("ok_em anda", a["ok_em"] == "2026-09-24T10:05:00", a["ok_em"])
check("mudou_em nao anda (nao ha medida para comparar)",
      a["mudou_em"] == "2026-09-24T10:02:00", a["mudou_em"])
check("e o max guardado fica o da ultima medida", a["max"] == "2026-09-01", a["max"])

print("\n7. gravar falha: o ETL nao cai")
_orig_gravar = E._gravar


def _gravar_quebrado(t, r):
    raise PermissionError("Dropbox segurando o arquivo")


E._gravar = _gravar_quebrado
_fila[:] = [med("2026-09-01", 12, "2026-07-01", 5), med("2026-09-01", 12, "2026-07-01", 5)]
try:
    E.rodar(mod(lambda: None))
    caiu = False
except Exception:
    caiu = True
E._gravar = _orig_gravar
check("uma falha ao registrar nao vira falha da carga", caiu is False)

print("\n8. primeira tentativa de uma tabela FALHA: desde so nasce com a primeira medida")
E.tabelas_do_modulo = lambda dotted: ["t_c"] if dotted == "fake.mod" else []
_fila[:] = [{"t_c": {"max": "2026-01-01", "linhas": 1}}]
try:
    E.rodar(mod(_quebra))
except RuntimeError:
    pass
c = reg("t_c")
check("falha sem registro anterior: desde e ok_em vazios",
      c["desde"] is None and c["ok_em"] is None, c)
_fila[:] = [{"t_c": {"max": "2026-01-01", "linhas": 1}}, {"t_c": {"max": "2026-02-01", "linhas": 2}}]
E.rodar(mod(lambda: None))
c = reg("t_c")
check("e nasce na primeira execucao boa, mesmo com o campo ja existindo como null",
      c["desde"] == "2026-09-24T10:08:00", c)
check("ler() devolve todos os registros", set(E.ler()) == {"t_a", "t_b", "t_c"}, sorted(E.ler()))

print("\n9. os tres executores passam por execucoes.rodar()")
# Um executor que chame `mod.run()` direto deixa de registrar, e nada levanta: a pagina
# so passa a dizer "sem registro" para as tabelas dele.
raiz = pathlib.Path(__file__).resolve().parents[1]
for job in ("update_db.py", "update_us.py", "update_international.py"):
    src = (raiz / "jobs" / job).read_text(encoding="utf-8")
    check(f"jobs/{job} chama execucoes.rodar", "execucoes.rodar(mod, kwargs)" in src)
    check(f"jobs/{job} nao chama mod.run direto",
          re.search(r"^\s*mod\.run\(", src, re.M) is None)

print("\n10. o botao da pagina tambem: update_db._executar registra")
from jobs import update_db  # noqa: E402

chamados = []
_orig_rodar = E.rodar
E.rodar = lambda m, kw=None: chamados.append(m.__name__)
res = update_db._executar([("fake", mod(lambda: None), {})])
E.rodar = _orig_rodar
check("_executar() -- o que o /api/run usa -- passa por rodar()",
      chamados == ["fake.mod"] and res[0]["ok"] is True, (chamados, res))

print("\n11. registry: execucoes.py nao e confundido com um script de tabela")
from domain.db import registry  # noqa: E402

check("nenhuma tabela mapeada para domain.db.execucoes",
      all(m != "domain.db.execucoes" for m in registry.tabelas().values()))
check("e a convencao do registry segue valida", registry.validar() == [], registry.validar())

print("\n" + "=" * 62)
if falhas:
    print(f"{len(falhas)} FALHA(S): {falhas}")
    sys.exit(1)
print("todos os asserts passaram")
