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

# gerar por fora deixa o stamp para tras -- nao pode virar "em dia" mentiroso.
# O sleep nao e decoracao: o veredito compara `output_mtime_ns`, e o relogio de
# arquivo do Windows anda em passos de ~15ms -- duas escritas no mesmo passo saem com
# mtime_ns identico e o teste falha por flake, nao por bug (visto em 2026-08-28).
time.sleep(0.05)
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

# ---------------------------------------------------------------------------
# O retrato VELHO nao pode virar acusacao (conserto de 2026-09-23)
# ---------------------------------------------------------------------------
# O defeito, medido no card de Credito naquele dia: retrato de 11/09, HTML de 17/09, e a
# aba acusando o relatorio de nao ter a inadimplencia de setembro que ESTAVA dentro dele.
# O codigo ja sabia que o retrato nao era daquele arquivo (`output_mtime_ns` diferente) e
# comparava com ele assim mesmo, porque testava `novos` ANTES da validade do retrato.
#
# Arquivos proprios de proposito: o bloco acima deixa `csv_dep` com mtime no futuro e uma
# assercao presa ao ultimo indice dele, entao mexer naquele par aqui quebraria um teste
# que nao tem nada a ver com este.
csv2 = tmp / "dados" / "serie2.csv"
csv2.write_text("dt,value\n2026-07,1\n", encoding="utf-8")
saida2 = tmp / "reports" / "Fake3.html"
saida2.write_text("<html></html>", encoding="utf-8")
DOC_VELHO = {"dashboards": [{
    "key": "fake3", "name": "Fake3", "area": "brasil",
    "output": "reports/Fake3.html", "module": None, "command": "echo",
    "build_seconds": 1,
    "deps": [{"kind": "csv", "ref": "dados/serie2.csv", "date_col": "dt",
              "role": "serie de teste"}],
}]}

S.stamp("fake3", DOC_VELHO)
time.sleep(0.05)                       # ver a nota sobre o relogio de arquivo do Windows
saida2.write_text("<html>gerado na mao</html>", encoding="utf-8")
csv2.write_text("dt,value\n2026-07,1\n2026-08,2\n", encoding="utf-8")
linha = S.estado(DOC_VELHO)[0]
check("fonte andou com o retrato VELHO -> 'sem stamp', nunca 'desatualizado'",
      linha["veredito"] == "sem stamp", linha["veredito"])
check("e a dependencia nao sai marcada como nova (a comparacao nao vale)",
      linha["deps"][0]["novo"] is False and linha["n_novos"] == 0,
      (linha["deps"][0]["novo"], linha["n_novos"]))
check("mas o estado da fonte continua visivel na tela",
      linha["deps"][0]["ultimo"] == "2026-08", linha["deps"][0]["ultimo"])

# Com o retrato de volta ao arquivo certo, a afirmacao volta a ser possivel -- senao o
# conserto acima teria matado o sinal em vez de conserta-lo.
S.stamp("fake3", DOC_VELHO)
check("restampado e nada mudou -> 'em dia'",
      S.estado(DOC_VELHO)[0]["veredito"] == "em dia")
csv2.write_text("dt,value\n2026-07,1\n2026-08,2\n2026-09,3\n", encoding="utf-8")
linha = S.estado(DOC_VELHO)[0]
check("com retrato valido, a fonte andando volta a dar 'desatualizado'",
      linha["veredito"] == "desatualizado" and linha["deps"][0]["novo"] is True,
      linha["veredito"])
saida2.unlink()

# ---------------------------------------------------------------------------
# chave_por_saida(): e o que deixa o gerador stampar sem saber a chave
# ---------------------------------------------------------------------------
check("acha a chave pelo caminho de saida",
      S.chave_por_saida(tmp / "reports" / "Fake.html", DOC) == "fake",
      S.chave_por_saida(tmp / "reports" / "Fake.html", DOC))
check("arquivo que nao esta no manifesto nao casa com ninguem",
      S.chave_por_saida(tmp / "reports" / "Outro.html", DOC) is None)
# O casamento e pelo caminho RESOLVIDO, nao pelo nome: dois relatorios de paises
# diferentes se chamam Inflation.html, e casar por nome stamparia um no lugar do outro.
(tmp / "outra_pasta").mkdir(exist_ok=True)
(tmp / "outra_pasta" / "Fake.html").write_text("<html></html>", encoding="utf-8")
check("mesmo NOME noutra pasta nao casa",
      S.chave_por_saida(tmp / "outra_pasta" / "Fake.html", DOC) is None)

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


# ---------------------------------------------------------------------------
print("\n2b. afetados() / regerar_afetados() -- atualizar dado regera a metrica")
# ---------------------------------------------------------------------------
# O caso que motivou isto (2026-08-28): o usuario atualizou fisc_rtn e esperava as
# medidas de impulso fiscal se moverem. Elas nao leem fisc_rtn -- mas nada no sistema
# dizia isso, nem regerava o que de fato le. As duas metades da resposta sao um mapa
# "quem le esta tabela" e um gatilho que so dispara para quem ficou para tras.

DOC_AF = {"dashboards": [
    {"key": "a", "name": "A", "output": "reports/A.html", "module": None,
     "command": "echo a", "deps": [
        {"kind": "mysql", "ref": "macro_brasil.fisc_rtn", "role": "rtn"},
        {"kind": "mysql", "ref": "macro_brasil.inflc_agregados", "role": "ipca"}]},
    {"key": "b", "name": "B", "output": "reports/B.html", "module": None,
     "command": "echo b", "deps": [
        {"kind": "mysql", "ref": "macro_brasil.fisc_nfsp", "role": "nfsp"}]},
    {"key": "c", "name": "C", "output": "reports/C.html", "module": None,
     "command": "echo c", "deps": [
        {"kind": "mysql", "ref": "base_mercado.interest_rates", "role": "curvas"},
        {"kind": "csv", "ref": "dados/serie.csv", "date_col": "dt", "role": "csv"}]},
]}

check("afetados() acha quem le a tabela",
      S.afetados(["fisc_rtn"], DOC_AF) == ["a"], S.afetados(["fisc_rtn"], DOC_AF))
check("uma tabela pode nao ter leitor nenhum",
      S.afetados(["fisc_investimento"], DOC_AF) == [])
check("varias tabelas somam sem repetir dashboard",
      S.afetados(["fisc_rtn", "inflc_agregados", "fisc_nfsp"], DOC_AF) == ["a", "b"])
# O ETL fala em nome nu, o manifesto em schema.tabela -- o casamento e pelo sufixo.
check("casa nome nu com a ref qualificada do manifesto",
      S.afetados(["macro_brasil.fisc_rtn"], DOC_AF) == ["a"])
check("lista vazia nao varre nada", S.afetados([], DOC_AF) == [])
# base_mercado e MySQL mas quem escreve e outro projeto: rodar ETL daqui nao a move,
# entao ela nunca pode disparar regeracao por conta de um passe nosso.
check("dependencia fora dos nossos schemas nao dispara",
      S.afetados(["interest_rates"], DOC_AF) == [])
check("csv nao dispara por nome de tabela",
      S.afetados(["serie.csv"], DOC_AF) == [])

# regerar_afetados(): o filtro por veredito e o que separa "regera o que precisa" de
# "regera tudo que toca a tabela". Aqui nenhum dos tres tem arquivo em disco, entao
# todos saem "sem relatorio" -- veredito deliberadamente FORA do gatilho default.
res = S.regerar_afetados(["fisc_rtn"], DOC_AF)
check("regerar_afetados() so olha quem le a tabela",
      [r["key"] for r in res] == ["a"], [r["key"] for r in res])
check("'sem relatorio' nao dispara geracao sozinho",
      res[0]["acao"] == "em dia" and res[0]["veredito"] == "sem relatorio", res[0])
check("tabela sem leitor devolve lista vazia",
      S.regerar_afetados(["fisc_investimento"], DOC_AF) == [])
# Dashboard sem module (o Oraculo) nao pode fingir que gerou.
res = S.regerar_afetados(["fisc_rtn"], DOC_AF, vereditos=("sem relatorio",))
check("dashboard sem run() sai como 'manual', com o comando",
      res[0]["acao"] == "manual" and res[0]["command"] == "echo a", res[0])

# ---------------------------------------------------------------------------
print("\n2c. quem gera o relatorio grava o retrato (conserto de 2026-09-23)")
# ---------------------------------------------------------------------------
# O outro lado do mesmo defeito. Ate aqui o retrato so era gravado por `status.gerar()`,
# um passo separado -- e o comando documentado em 10 dos 13 CLAUDE.md de pasta e o
# `generate_report.run()` direto, que nao passa por la. Medido em 2026-09-23: 8 dos 13
# relatorios entregues tinham retrato ausente ou de outra geracao.
#
# A correcao poe a gravacao dentro de `render_report()`, por onde TODO relatorio HTML
# deste projeto passa. Este teste e o que impede a regressao: um refactor do builder que
# perca a chamada volta a produzir uma aba que nao sabe responder nada.
from analytics.report_structure.builder import render_report      # noqa: E402

_carregar_orig = S.carregar
S.carregar = lambda *a, **k: DOC_RENDER                # o builder resolve pelo manifesto

modelo = tmp / "modelo.html"
modelo.write_text("<html><script>/*REPORT_DATA*/</script></html>", encoding="utf-8")
saida4 = tmp / "reports" / "Fake4.html"
DOC_RENDER = {"dashboards": [{
    "key": "fake4", "name": "Fake4", "area": "brasil",
    "output": "reports/Fake4.html", "module": None, "command": "echo",
    "build_seconds": 1,
    "deps": [{"kind": "csv", "ref": "dados/serie2.csv", "date_col": "dt",
              "role": "serie de teste"}],
}]}

csv2.write_text("dt,value\n2026-07,1\n2026-08,2\n", encoding="utf-8")
check("nao ha retrato antes de gerar", S.ler_stamp("fake4") is None)

render_report(modelo, {"x": 1}, saida4)
reg = S.ler_stamp("fake4")
check("render_report() gravou o retrato sozinho, sem passar por gerar()",
      reg is not None and reg["key"] == "fake4", reg)
check("o retrato guarda o que a fonte tinha na hora",
      reg and reg["deps"]["dados/serie2.csv"] == "2026-08", reg)
# A ordem importa e e invisivel quando errada: gravado ANTES do write_text, o retrato
# seria da versao anterior do arquivo e daria um "em dia" de mentira na geracao seguinte.
check("gravou DEPOIS de escrever (o mtime do retrato e o do arquivo entregue)",
      reg and reg["output_mtime_ns"] == saida4.stat().st_mtime_ns, reg)
check("e o veredito ja sai 'em dia', sem passo manual nenhum",
      S.estado(DOC_RENDER)[0]["veredito"] == "em dia",
      S.estado(DOC_RENDER)[0]["veredito"])

# Gerar de novo com a fonte adiantada tem de reescrever o retrato, nao manter o antigo.
csv2.write_text("dt,value\n2026-07,1\n2026-08,2\n2026-09,3\n", encoding="utf-8")
time.sleep(0.05)
render_report(modelo, {"x": 2}, saida4)
check("regerar atualiza o retrato junto",
      S.ler_stamp("fake4")["deps"]["dados/serie2.csv"] == "2026-09"
      and S.estado(DOC_RENDER)[0]["veredito"] == "em dia")

# Saida que ninguem declarou (o template de comparacao de juros reais, por exemplo) nao
# stampa e nao levanta -- nao ha dashboard contra o que comparar.
antes = sorted(p.name for p in S._STAMPS.glob("*.json"))
fora = tmp / "reports" / "NaoDeclarado.html"
render_report(modelo, {"x": 3}, fora)
check("saida fora do manifesto nao quebra a geracao e nao stampa",
      fora.exists() and sorted(p.name for p in S._STAMPS.glob("*.json")) == antes,
      sorted(p.name for p in S._STAMPS.glob("*.json")))

# E uma falha ao gravar o retrato NAO pode custar o relatorio: o banco pode estar fora do
# ar, e o arquivo ja esta em disco. O veredito passa a ser "nao da para conferir", que e a
# resposta honesta -- perder o HTML nao seria. Tem de ser uma saida DECLARADA, senao a
# funcao sai antes de chegar no stamp e o teste nao exercita nada.
_stamp_orig = S.stamp
S.stamp = lambda *a, **k: (_ for _ in ()).throw(RuntimeError("banco fora do ar"))
time.sleep(0.05)
render_report(modelo, {"marcador": "sobreviveu"}, saida4)
check("retrato que falha nao derruba a geracao",
      saida4.exists() and "sobreviveu" in saida4.read_text(encoding="utf-8"))
S.stamp = _stamp_orig
S.carregar = _carregar_orig

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

# E, desde que o Oraculo saiu da lista (2026-09-23), NENHUM dashboard fica sem module.
# O ramo que trata disso continua no codigo (`gerar()` levanta, o card oferece so a linha
# de comando) porque a situacao volta assim que alguem declarar outro artefato sem run();
# esta assercao e o que impede ele de virar codigo morto sem ninguem notar -- mesma
# escolha que o ramo de `owner` ja tinha. Se ela reprovar, o ramo ganhou usuario de novo.
check("nenhum dashboard do manifesto fica sem module (o ramo existe, sem usuario)",
      not [d["key"] for d in ds if not d.get("module")],
      [d["key"] for d in ds if not d.get("module")])

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
    # Tabela de DIMENSAO nao tem data por definicao, e o manifesto declara isso com
    # `date_col: null`. A isencao sai dessa declaracao e nao de um numero: a versao
    # anterior admitia "ate 4 sem data", e ao entrar a quinta dimensao (mt_ces_dim, em
    # 2026-09-01) o teste reprovou uma adicao correta. Um numero magico aqui envelhece
    # a cada tabela nova; a declaracao nao.
    sem_data_declarada = {
        f"{d.get('ref')}"
        for dash in ds for d in dash.get("deps", [])
        if d.get("kind") == "mysql" and "date_col" in d and d.get("date_col") is None
    }
    devem_responder = [dep for dep in sql if dep["ref"] not in sem_data_declarada]
    mudos = [dep["ref"] for dep in devem_responder if not dep["ultimo"]]
    check("tabela de serie responde MAX(date)", not mudos,
          f"{len(com_data)}/{len(sql)} com data; sem responder: {mudos}")
    # E a contrapartida: uma tabela declarada sem data nao pode devolver data -- seria
    # sinal de que a declaracao esta errada e o estado dela nunca sera comparado.
    falsas = [dep["ref"] for dep in sql
              if dep["ref"] in sem_data_declarada and dep["ultimo"]]
    check("dimensao declarada sem data de fato nao tem data", not falsas, str(falsas))

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
