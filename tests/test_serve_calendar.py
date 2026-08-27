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
    # Contado do proprio YAML, nao fixado: um numero literal aqui vira falha de
    # teste toda vez que um grupo entra no calendario (aconteceu ao adicionar
    # bls_cpi e bea_pce, que passaram os grupos de 25 para 27). O que o teste tem
    # a dizer e que o /api/status cobre TODOS os grupos, nao quantos existem.
    from domain.release_calendar.sync import carregar, tabelas_por_grupo
    esperados = set(tabelas_por_grupo(carregar()))
    check("  um estado por grupo do calendario",
          set(g) == esperados, sorted(esperados ^ set(g)))
    check("  todo grupo tem estado valido",
          all(v["estado"] in ("atrasado", "ok", "indefinido", "vazio") for v in g.values()))
    check("  grupo sem tabelas -> vazio", g["bcb_copom_ata"]["estado"] == "vazio",
          g["bcb_copom_ata"])
    print(f"         estados: {sorted({v['estado'] for v in g.values()})}")

print("\n3. dashboards (aba Status dashboard)")
code, body, _ = req("/api/dashboards")
d = json.loads(body)
check("GET /api/dashboards = 200", code == 200, code)
check("  ok=True (banco acessivel)", d.get("ok") is True, d.get("erro"))
if d.get("ok"):
    ds = d["dashboards"]
    from domain.dashboards.status import dashboards as declarados
    check("  uma linha por dashboard do manifesto",
          len(ds) == len(declarados()), f"{len(ds)} != {len(declarados())}")
    check("  todo dashboard tem veredito valido",
          all(x["veredito"] in ("em dia", "desatualizado", "sem stamp", "sem relatorio")
              for x in ds), sorted({x["veredito"] for x in ds}))
    check("  toda dependencia diz onde mora",
          all(dep.get("onde") for x in ds for dep in x["deps"]))
    check("  toda dependencia declara se esta fora do MySQL",
          all(isinstance(dep.get("fora_do_mysql"), bool) for x in ds for dep in x["deps"]))
    # O ponto da aba: tabela de serie temporal tem de responder com data de verdade,
    # senao a coluna "ultimo dado" nasce vazia e o painel nao serve para nada.
    sql = [dep for x in ds for dep in x["deps"] if dep["kind"] == "mysql"]
    com_data = [dep for dep in sql if dep.get("ultimo")]
    check("  tabela do banco responde MAX(date)",
          len(com_data) >= len(sql) - 8, f"{len(com_data)}/{len(sql)}")
    fx = [x for x in ds if x["key"] == "brasil_exchange_rate"][0]
    check("  FRED entra como fonte fora do MySQL, nao consultada por default",
          any(dep["onde"] == "FRED" and dep["fora_do_mysql"] and dep.get("nao_checado")
              for dep in fx["deps"]))
    check("  base_mercado marcada como de outro projeto",
          any(dep["ref"].startswith("base_mercado.") and dep.get("owner")
              for dep in fx["deps"]))
    print(f"         vereditos: {sorted({x['veredito'] for x in ds})}")

print("\n4. guarda de Host (DNS rebinding)")
for rota, metodo, corpo in (("/api/ping", "GET", None),
                            ("/api/run", "POST", {"group": "bcb_icbr"}),
                            ("/api/gerar", "POST", {"key": "release_calendar"})):
    code, _, _ = req(rota, host="evil.example.com", metodo=metodo, corpo=corpo)
    check(f"{metodo} {rota} com Host estranho -> 403", code == 403, code)

print("\n5. allowlist do POST")
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

# Mesma allowlist, agora por `key` -- a pagina manda um id do manifesto, nunca um
# caminho ou nome de modulo.
for corpo, rotulo in (
    ({"key": "nao_existe"}, "key inexistente"),
    ({}, "sem campo key"),
    ({"key": ["brasil_credit"]}, "key nao-string"),
    ({"key": "analytics.brasil.credit.generate_report"}, "nome de modulo como key"),
    ({"key": "oraculo"}, "dashboard sem entry point automatico"),
):
    code, body, _ = req("/api/gerar", metodo="POST", corpo=corpo)
    check(f"/api/gerar: {rotulo} -> 400", code == 400, code)
check("  a recusa do oraculo diz o comando manual",
      b"update_oraculo" in req("/api/gerar", metodo="POST", corpo={"key": "oraculo"})[1])

print("\n6. POST /api/gerar de verdade (release_calendar — barato e sem escrita no banco)")
code, body, _ = req("/api/gerar", metodo="POST", corpo={"key": "release_calendar"})
d = json.loads(body)
check("POST /api/gerar = 200", code == 200, code)
check("  ok=True", d.get("ok") is True, d)
check("  reporta quanto demorou", isinstance(d.get("segundos"), (int, float)), d.get("segundos"))
check("  devolve o estado novo SO desse dashboard",
      (d.get("dashboard") or {}).get("key") == "release_calendar",
      (d.get("dashboard") or {}).get("key"))
# O ponto do stamp: regerar pelo endpoint tem de sair de "sem stamp" para "em dia".
check("  regerar deixa o dashboard em dia",
      (d.get("dashboard") or {}).get("veredito") == "em dia",
      (d.get("dashboard") or {}).get("veredito"))

if RUN_ETL:
    print("\n7. POST /api/run de verdade (bcb_icbr — 2 scripts SGS rapidos)")
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
    print("\n7. POST /api/run real: PULADO (passe --run-etl para incluir)")

_srv.shutdown()
_srv.server_close()
print("\n" + "=" * 62)
if falhas:
    print(f"{len(falhas)} FALHA(S): {falhas}")
    raise SystemExit(1)
print("E2E ok")
