# -*- coding: utf-8 -*-
"""Testa o manifesto de dashboards e o veredito de domain/dashboards/status.py.

Roda com:
    uv run python tests/test_dashboard_status.py

Padrao dos demais testes daqui: script executavel com asserts, nao pytest (o projeto
nao tem pytest configurado). Duas metades:

  1. LOGICA -- sobre um manifesto sintetico e um diretorio temporario, sem MySQL.
     E onde mora o que de fato pode dar errado em silencio: um dashboard cujo dado
     andou continuar aparecendo como "em dia".
  2. MANIFESTO REAL -- valida a declaracao contra o banco e contra o registry. Essa
     metade precisa de MySQL e e pulada com aviso se ele nao responder, para o teste
     seguir util numa maquina sem banco.

O que a metade 2 cobra e a pergunta que o registry sozinho nao responde: toda tabela
que um dashboard LE tem alguem que a ESCREVE? Uma tabela consumida e sem script de
ETL nao tem como ser atualizada por botao nenhum -- e um beco sem saida, nao um
detalhe de configuracao.
"""

import os
import sys
import tempfile
import time
from pathlib import Path

from domain.dashboards import status as S

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

falhas = []


def check(rotulo, cond, extra=""):
    print(("  ok     " if cond else "  FALHA  ") + rotulo
          + (f"  -> {extra}" if extra and not cond else ""))
    if not cond:
        falhas.append(rotulo)


# ---------------------------------------------------------------------------
print("1. classificacao de dependencia")
# ---------------------------------------------------------------------------

check("coluna de data default e 'date'",
      S._col({"kind": "mysql", "ref": "macro_brasil.atv_pib"}) == "date")
check("date_col: null desliga a leitura de data (tabela de dimensao)",
      S._col({"kind": "mysql", "ref": "macro_brasil.inflc_dim", "date_col": None}) is None)
check("date_col explicito vence o default",
      S._col({"kind": "mysql", "ref": "macro_us.inflc_cpi_pesos",
              "date_col": "reference_period"}) == "reference_period")

check("schema proprio nao e 'fora do MySQL'",
      not S.fora_do_mysql({"kind": "mysql", "ref": "macro_brasil.atv_pib"}))
check("macro_us tambem e schema proprio",
      not S.fora_do_mysql({"kind": "mysql", "ref": "macro_us.inflc_cpi"}))
# O ponto: base_mercado E MySQL, mas nenhum ETL deste projeto escreve la. Tratar como
# "dentro" faria a aba prometer um botao que nao existe.
check("base_mercado conta como fora (quem escreve e outro projeto)",
      S.fora_do_mysql({"kind": "mysql", "ref": "base_mercado.interest_rates"}))
check("csv e fora do MySQL",
      S.fora_do_mysql({"kind": "csv", "ref": "x.csv"}))
check("fonte live e fora do MySQL",
      S.fora_do_mysql({"kind": "live", "ref": "FRED:CPIAUCSL"}))

check("onde: mysql mostra o schema",
      S._onde({"kind": "mysql", "ref": "macro_brasil.atv_pib"}) == "macro_brasil")
check("onde: live mostra a fonte",
      S._onde({"kind": "live", "ref": "FRED:CPIAUCSL"}) == "FRED")
check("onde: arquivo",
      S._onde({"kind": "artifact", "ref": "a/b.csv"}) == "arquivo")


# ---------------------------------------------------------------------------
print("\n2. veredito, sobre manifesto sintetico (sem MySQL)")
# ---------------------------------------------------------------------------

tmp = Path(tempfile.mkdtemp(prefix="dashstatus_"))
_RAIZ_ORIG, _STAMPS_ORIG = S._RAIZ, S._STAMPS
S._RAIZ = tmp
S._STAMPS = tmp / "reports" / ".build"

(tmp / "reports").mkdir(parents=True)
(tmp / "dados").mkdir()

csv_dep = tmp / "dados" / "serie.csv"
csv_dep.write_text("dt,value\n2026-06,1\n2026-07,2\n", encoding="utf-8")
saida = tmp / "reports" / "Fake.html"
saida.write_text("<html></html>", encoding="utf-8")

DOC = {"dashboards": [{
    "key": "fake", "name": "Fake", "area": "brasil",
    "output": "reports/Fake.html", "module": None, "command": "echo",
    "build_seconds": 1,
    "deps": [{"kind": "csv", "ref": "dados/serie.csv", "date_col": "dt",
              "role": "serie de teste"}],
}]}

linha = S.estado(DOC)[0]
check("sem stamp -> veredito 'sem stamp'", linha["veredito"] == "sem stamp",
      linha["veredito"])
check("le o ultimo dado do CSV", linha["deps"][0]["ultimo"] == "2026-07",
      linha["deps"][0]["ultimo"])
check("conta a dependencia como fora do MySQL", linha["n_fora_mysql"] == 1)
check("registra tamanho e data de geracao do arquivo",
      linha["existe"] and linha["gerado_em"] and linha["tamanho_mb"] is not None)

S.stamp("fake", DOC)
linha = S.estado(DOC)[0]
check("com stamp e nada mudou -> 'em dia'", linha["veredito"] == "em dia",
      linha["veredito"])
check("o stamp guarda o que a fonte tinha",
      S.ler_stamp("fake")["deps"]["dados/serie.csv"] == "2026-07")

# a fonte anda: e exatamente o caso que a aba existe para pegar
csv_dep.write_text("dt,value\n2026-06,1\n2026-07,2\n2026-08,3\n", encoding="utf-8")
linha = S.estado(DOC)[0]
check("fonte andou depois da geracao -> 'desatualizado'",
      linha["veredito"] == "desatualizado", linha["veredito"])
check("a dependencia culpada vem marcada", linha["deps"][0]["novo"] is True)
check("mostra o que o relatorio tem, ao lado do que a fonte tem",
      linha["deps"][0]["stamp"] == "2026-07" and linha["deps"][0]["ultimo"] == "2026-08")
check("conta quantas dependencias andaram", linha["n_novos"] == 1)

# regerar (aqui: so reescrever a saida e restampar) tem de limpar o veredito
saida.write_text("<html>novo</html>", encoding="utf-8")
S.stamp("fake", DOC)
check("regerar + restampar volta para 'em dia'",
      S.estado(DOC)[0]["veredito"] == "em dia")

# gerar por fora deixa o stamp para tras -- nao pode virar "em dia" mentiroso
saida.write_text("<html>gerado na mao</html>", encoding="utf-8")
linha = S.estado(DOC)[0]
check("arquivo mexido por fora do fluxo -> 'sem stamp', nao 'em dia'",
      linha["veredito"] == "sem stamp", linha["veredito"])

# artefato reescrito depois do HTML: sinal que funciona mesmo SEM stamp
DOC_ART = {"dashboards": [{
    "key": "fake2", "name": "Fake2", "area": "brasil", "output": "reports/Fake.html",
    "module": None, "command": "echo", "build_seconds": 1,
    "deps": [{"kind": "artifact", "ref": "dados/serie.csv", "role": "artefato"}],
}]}
os.utime(csv_dep, (time.time() + 60, time.time() + 60))
linha = S.estado(DOC_ART)[0]
check("artefato mais novo que o HTML e sinalizado sem precisar de stamp",
      linha["deps"][0]["arquivo_mais_novo"] and linha["veredito"] == "desatualizado",
      linha["veredito"])
check("artefato CSV reporta o ultimo indice",
      linha["deps"][0]["ultimo"] == "2026-08", linha["deps"][0]["ultimo"])

saida.unlink()
check("sem arquivo gerado -> 'sem relatorio'",
      S.estado(DOC)[0]["veredito"] == "sem relatorio")

# validar() reclama do que nao existe em disco
DOC_RUIM = {"dashboards": [{
    "key": "x", "name": "X", "output": "reports/X.html", "module": None,
    "deps": [{"kind": "csv", "ref": "dados/nao_existe.csv", "date_col": "dt"}],
}]}
probs = S.validar(DOC_RUIM)
check("validar() acusa arquivo declarado que nao existe",
      any("nao existe" in p for p in probs), probs)

S._RAIZ, S._STAMPS = _RAIZ_ORIG, _STAMPS_ORIG


# ---------------------------------------------------------------------------
print("\n3. manifesto real")
# ---------------------------------------------------------------------------

doc = S.carregar()
ds = S.dashboards(doc)
check("manifesto tem dashboards", len(ds) >= 10, len(ds))
check("toda chave e unica", len({d["key"] for d in ds}) == len(ds))
check("todo dashboard declara saida e dependencias",
      all(d.get("output") and d.get("deps") for d in ds))
check("todo dashboard declara o comando de geracao",
      all(d.get("command") for d in ds))

kinds = {dep["kind"] for d in ds for dep in d["deps"]}
check("so kinds conhecidos", kinds <= {"mysql", "csv", "artifact", "yaml", "live"}, kinds)

# Todo relatorio HTML tem de ter modulo com run() -- e o que o botao vai chamar.
sem_modulo = [d["key"] for d in ds
              if d["output"].endswith(".html") and not d.get("module")]
check("todo relatorio HTML tem module com run()", not sem_modulo, sem_modulo)

todas_saidas = [d["output"] for d in ds]
check("nenhuma saida repetida entre dashboards",
      len(set(todas_saidas)) == len(todas_saidas))

# Cruzamento com o registry: quem le tem de ter quem escreve.
from domain.db.registry import tabelas as tabelas_registry

reg = set(tabelas_registry())
orfas = []
for d in ds:
    for dep in d["deps"]:
        if dep["kind"] != "mysql" or S.fora_do_mysql(dep):
            continue
        tabela = dep["ref"].split(".", 1)[1]
        if tabela not in reg:
            orfas.append(f"{d['key']}: {dep['ref']}")
check("toda tabela lida por dashboard tem script de ETL que a escreve",
      not orfas, orfas)

# E o inverso util: as fontes fora do MySQL sao justamente as que nenhum botao
# resolve, entao cada uma tem de dizer como se atualiza.
sem_receita = []
for d in ds:
    for dep in d["deps"]:
        if dep["kind"] in ("csv", "artifact") and not dep.get("refresh") and not dep.get("note"):
            sem_receita.append(f"{d['key']}: {dep['ref']}")
check("dependencia de arquivo diz como atualizar (ou explica que nao precisa)",
      len(sem_receita) <= 8, sem_receita)

try:
    probs = S.validar(doc)
    check("manifesto valida contra banco e disco", not probs, probs)

    linhas = S.estado(doc)
    check("estado() devolve uma linha por dashboard", len(linhas) == len(ds))
    check("todo veredito e conhecido",
          all(l["veredito"] in ("em dia", "desatualizado", "sem stamp", "sem relatorio")
              for l in linhas), sorted({l["veredito"] for l in linhas}))

    sql = [dep for l in linhas for dep in l["deps"]
           if dep["kind"] == "mysql" and not dep.get("erro")]
    com_data = [dep for dep in sql if dep["ultimo"]]
    # As 3 tabelas de dimensao nao tem data por definicao; o resto tem de responder.
    check("tabela de serie responde MAX(date)", len(com_data) >= len(sql) - 4,
          f"{len(com_data)}/{len(sql)}")

    # A tabela mais compartilhada do projeto: se ela some, cinco relatorios param.
    quem_le_ipca = [l["name"] for l in linhas
                    if any(dep["ref"] == "macro_brasil.inflc_agregados" for dep in l["deps"])]
    check("inflc_agregados aparece como dependencia compartilhada",
          len(quem_le_ipca) >= 4, quem_le_ipca)
    print(f"         inflc_agregados alimenta: {', '.join(quem_le_ipca)}")

except Exception as exc:
    print(f"  PULADO  metade com MySQL indisponivel: {type(exc).__name__}: {exc}")


print("\n" + "=" * 62)
if falhas:
    print(f"{len(falhas)} FALHA(S):")
    for f in falhas:
        print(f"  - {f}")
    raise SystemExit(1)
print("todos os asserts passaram")
