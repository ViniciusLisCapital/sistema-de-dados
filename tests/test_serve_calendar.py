# -*- coding: utf-8 -*-
"""
E2E do analytics/release_calendar/serve.py — sobe o servidor numa thread e bate
nos endpoints de verdade (inclusive as guardas de seguranca).

Roda com:
    uv run python tests/test_serve_calendar.py             # sem tocar no banco de escrita
    uv run python tests/test_serve_calendar.py --run-etl   # inclui um POST /api/run real

O `--run-etl` fica de fora por default de proposito: ele executa ETL e ESCREVE no
MySQL. O resto do teste so le (o /api/status faz SELECT MAX(date)), entao pode rodar
a vontade. Precisa do MySQL acessivel de qualquer forma.

Mesmo estilo de script executavel do tests/test_ibge2.py (o projeto nao tem pytest).
"""

import json
import socket
import sys
import threading
import urllib.error
import urllib.request

from analytics.release_calendar.serve import Handler, Server

RUN_ETL = "--run-etl" in sys.argv
falhas = []


def check(rotulo, cond, extra=""):
    print(("  ok     " if cond else "  FALHA  ") + rotulo
          + (f"  -> {extra}" if extra and not cond else ""))
    if not cond:
        falhas.append(rotulo)


def _porta_livre():
    s = socket.socket()
    s.bind(("127.0.0.1", 0))
    p = s.getsockname()[1]
    s.close()
    return p


PORT = _porta_livre()
_srv = Server(("127.0.0.1", PORT), Handler)
threading.Thread(target=_srv.serve_forever, daemon=True).start()
BASE = f"http://127.0.0.1:{PORT}"
print(f"servidor de teste em {BASE}\n")


def req(rota, host=None, metodo="GET", corpo=None, timeout=900):
    r = urllib.request.Request(BASE + rota, method=metodo)
    if host:
        r.add_header("Host", host)
    if corpo is not None:
        r.add_header("Content-Type", "application/json")
        r.data = json.dumps(corpo).encode()
    try:
        with urllib.request.urlopen(r, timeout=timeout) as resp:
            return resp.status, resp.read(), resp.headers.get("Content-Type", "")
    except urllib.error.HTTPError as e:
        return e.code, e.read(), e.headers.get("Content-Type", "")


print("1. ping e pagina")
code, body, ctype = req("/api/ping")
d = json.loads(body)
check("GET /api/ping = 200", code == 200, code)
check("  ok=True, modo=servido", d.get("ok") and d.get("modo") == "servido", d)
check("  content-type json", "application/json" in ctype, ctype)

code, body, ctype = req("/")
check("GET / serve o HTML", code == 200 and b"<!DOCTYPE html>" in body, code)
check("  com a coluna Atualizar", b"col-update" in body)
check("  content-type text/html", "text/html" in ctype, ctype)

print("\n2. status")
code, body, _ = req("/api/status")
d = json.loads(body)
check("GET /api/status = 200", code == 200, code)
check("  ok=True (banco acessivel)", d.get("ok") is True, d.get("erro"))
if d.get("ok"):
    g = d["grupos"]
    check("  um estado por grupo do calendario", len(g) == 25, len(g))
    check("  todo grupo tem estado valido",
          all(v["estado"] in ("atrasado", "ok", "indefinido", "vazio") for v in g.values()))
    check("  grupo sem tabelas -> vazio", g["bcb_copom_ata"]["estado"] == "vazio",
          g["bcb_copom_ata"])
    print(f"         estados: {sorted({v['estado'] for v in g.values()})}")

print("\n3. guarda de Host (DNS rebinding)")
for metodo, corpo in (("GET", None), ("POST", {"group": "bcb_icbr"})):
    rota = "/api/ping" if metodo == "GET" else "/api/run"
    code, _, _ = req(rota, host="evil.example.com", metodo=metodo, corpo=corpo)
    check(f"{metodo} {rota} com Host estranho -> 403", code == 403, code)

print("\n4. allowlist do POST")
for corpo, rotulo in (
    ({"group": "nao_existe"}, "slug inexistente"),
    ({"group": "bcb_copom_ata"}, "grupo sem tabelas"),
    ({}, "sem campo group"),
    ({"group": "domain.db.brasil.bcb.cred_credito_amplo"}, "nome de modulo como slug"),
    ({"group": ["bcb_icbr"]}, "group nao-string"),
):
    code, _, _ = req("/api/run", metodo="POST", corpo=corpo)
    check(f"{rotulo} -> 400", code == 400, code)

code, _, _ = req("/api/nada")
check("rota desconhecida -> 404", code == 404, code)

if RUN_ETL:
    print("\n5. POST /api/run de verdade (bcb_icbr — 2 scripts SGS rapidos)")
    code, body, _ = req("/api/run", metodo="POST", corpo={"group": "bcb_icbr"})
    d = json.loads(body)
    check("POST /api/run = 200", code == 200, code)
    check("  ok=True", d.get("ok") is True, d)
    check("  2 scripts OK", d.get("n_ok") == 2, d.get("n_ok"))
    check("  0 erros", d.get("n_erro") == 0, d.get("n_erro"))
    check("  nenhuma tabela sem script", d.get("sem_script") == [], d.get("sem_script"))
    check("  devolve o status novo do grupo",
          (d.get("status") or {}).get("estado") == "ok", d.get("status"))
    check("  lista as tabelas alimentadas",
          sorted(d.get("tabelas") or []) == ["comm_icbr", "comm_icbr_usd"], d.get("tabelas"))
else:
    print("\n5. POST /api/run real: PULADO (passe --run-etl para incluir)")

_srv.shutdown()
_srv.server_close()
print("\n" + "=" * 62)
if falhas:
    print(f"{len(falhas)} FALHA(S): {falhas}")
    raise SystemExit(1)
print("E2E ok")
