# -*- coding: utf-8 -*-
"""
Confere as duas portas do BEA para a mesma tabela: API x xlsx, valor a valor.

Roda com:
    uv run python tests/test_bea_api.py          # historia inteira, ~150 MB
    uv run python tests/test_bea_api.py --rapido  # ultimos 3 anos, ~7 MB

Precisa de `BEA_API_KEY` no `.env` (registro gratuito em
https://apps.bea.gov/API/signup/) e de rede. Sem a chave o teste NAO passa em
silencio -- imprime SKIP dizendo o que deixou de ser conferido.

--------------------------------------------------------------------------------
POR QUE ESTE TESTE EXISTE
--------------------------------------------------------------------------------
O ramo de PCE le por DUAS portas, e nenhuma das duas cobre o que a outra faz:

  `inflc_pce`      valores -> **API** (dataset NIUnderlyingDetail)
  `inflc_pce_dim`  arvore  -> **xlsx** de release da Secao 2

A arvore ficou no xlsx porque a API nao publica hierarquia nenhuma -- a secao 3 checa
isso ao vivo, e o proprio servico responde que existem so quatro metodos
(GetDatasetList, GetParameterList, GetParameterValues, GetData). Por isso
`inflc_pce_dim` exige `fonte == "xlsx"`, o que a secao 5 exercita.

E o xlsx continua sendo lido porque o parser dele depende de convencoes de
APRESENTACAO: "Line" na celula A8, 2 espacos por nivel na coluna B, `.....` como
ausente, `ZZZZZZ` como "nao ha serie", nota de rodape identificada por "a coluna A
nao e numero". Um reformat cosmetico do BEA quebra qualquer uma dessas suposicoes --
e como a arvore SO pode vir dali, o risco nao desaparece por a carga ter migrado.

O que este teste faz e transformar as duas portas numa conferencia: elas leem a MESMA
publicacao por caminhos independentes (JSON tipado de um lado, planilha do outro),
entao onde concordam nao ha erro de leitura em nenhuma das duas -- e onde discordam,
uma delas esta errada. Mesma ideia da conferencia que `connectors/bls.py` faz entre a
API do BLS e o arquivo bruto. A versao por carga dessa mesma checagem vive em
`inflc_pce._conferir` (secao 6), que roda de graca sempre que o xlsx do dia ja esta em
cache.

Segue o padrao dos outros testes do projeto: script executavel com asserts, nao
pytest (o projeto nao tem pytest configurado).
"""

from __future__ import annotations

import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from dotenv import load_dotenv  # noqa: E402

load_dotenv(Path(__file__).resolve().parents[1] / ".env")

import os  # noqa: E402

import pandas as pd  # noqa: E402

from connectors import bea  # noqa: E402

_RAPIDO = "--rapido" in sys.argv
# Janela como tupla de anos: `bea.anos_param` converte para o parametro Year da API, e
# `bea.indexar_obs` usa a mesma tupla para recortar o lado do xlsx. Uma unica
# definicao de janela para os dois lados, senao a comparacao acha "sobras" que sao so
# recorte diferente.
_JANELA = (2024, 2026) if _RAPIDO else None
_ANOS = bea.anos_param(*(_JANELA or (None, None)))

_falhas: list[str] = []


def ok(cond: bool, rotulo: str, detalhe: str = "") -> None:
    print(f"  {'OK  ' if cond else 'FALHA'} {rotulo}" + (f"  [{detalhe}]" if detalhe else ""))
    if not cond:
        _falhas.append(rotulo)


def main() -> int:
    if not os.environ.get("BEA_API_KEY", "").strip():
        print("=" * 78)
        print("SKIP -- BEA_API_KEY nao esta no .env.")
        print("Nao foi conferido: se a API e o xlsx concordam valor a valor, se a API")
        print("segue sem campo de hierarquia, e se os rotulos e os codigos casam.")
        print("ATENCAO: sem chave a CARGA de inflc_pce tambem nao roda -- ela le da")
        print("API desde 2026-08-26. Ha saida de emergencia (`fonte=\"xlsx\"`), que")
        print("dispensa chave e da o mesmo numero, mas nao e o caminho default.")
        print("Registro gratuito: https://apps.bea.gov/API/signup/")
        print("=" * 78)
        return 0

    print(f"\nBEA: API x xlsx  ({'ultimos 3 anos' if _RAPIDO else 'historia inteira, 1959->hoje'})")

    # -----------------------------------------------------------------------
    # 1) a chave funciona, e as tabelas 2.4.xU estao no dataset
    # -----------------------------------------------------------------------
    print("\n1) dataset e catalogo")
    api = bea._get_api(method="GetParameterValues", datasetname="NIUnderlyingDetail",
                       ParameterName="TableName")
    nomes = {v.get("TableName") or v.get("Key")
             for v in api["Results"]["ParamValue"]}
    for t in (bea.TABELA_PCE_INDICE, bea.TABELA_PCE_NOMINAL):
        ok(t in nomes, f"{t} existe em NIUnderlyingDetail")

    # -----------------------------------------------------------------------
    # 2) a conferencia que da nome ao arquivo: valor a valor
    # -----------------------------------------------------------------------
    # Roda a funcao DE VERDADE, `conferir_api_xlsx` -- e nao uma copia da comparacao
    # aqui dentro. Uma copia deixaria a funcao exposta pelo connector sem exercicio, e
    # e ela que `inflc_pce` usa (via `comparar_obs`) para decidir se grava.
    print("\n2) valores")
    for aba in (bea.ABA_PCE_INDICE, bea.ABA_PCE_NOMINAL):
        t0 = time.time()
        r = bea.conferir_api_xlsx(aba, anos=_JANELA)
        print(f"  {aba} ({r['tabela_api']})  {r['n_comum']:,} obs em comum, "
              f"{time.time()-t0:.0f}s")
        ok(r["n_comum"] > (5_000 if _RAPIDO else 300_000),
           f"{aba}: as duas portas trazem o mesmo volume", f"{r['n_comum']:,} obs")
        ok(not r["n_so_a"], f"{aba}: nada existe so na API", f"{r['n_so_a']} sobras")
        ok(not r["n_so_b"], f"{aba}: nada existe so no xlsx", f"{r['n_so_b']} sobras")
        ok(r["n_diferentes"] == 0, f"{aba}: todo valor bate exatamente",
           f"{r['n_diferentes']} difs, max {r['dif_max']:.10g}"
           + (f" em {r['onde_dif']}" if r["dif_max"] else ""))
        if r["dif_max"] > 0:
            print(f"      publicado: api={r['publicado_api']!r} "
                  f"xlsx={r['publicado_xlsx']!r}")
            print("      (se as datas diferem, uma das portas esta num vintage"
                  " diferente -- o BEA revisa meses anteriores em cada divulgacao,"
                  " e nao e necessariamente bug do parser)")

        # rotulos e codigos: o mesmo texto sai das duas depois da MESMA limpeza. A API
        # traz a referencia cruzada "(55)" no rotulo igual ao xlsx, entao
        # _limpar_rotulo() e necessario dos dois lados -- a API nao vem mais limpa.
        ok(not r["n_rotulos_diferentes"], f"{aba}: rotulos identicos apos _limpar_rotulo()",
           f"{r['n_rotulos_diferentes']} de {r['n_linhas_api']}")
        ok(not r["n_codigos_diferentes"], f"{aba}: SeriesCode identicos",
           f"{r['n_codigos_diferentes']} de {r['n_linhas_api']}")

    # -----------------------------------------------------------------------
    # 3) a API continua sem hierarquia
    # -----------------------------------------------------------------------
    # Se isto falhar um dia, e boa noticia: o BEA passou a publicar parentesco e o
    # xlsx deixa de ser necessario para a arvore. A mensagem tem de dizer isso, senao
    # a falha vai parecer um defeito e alguem vai relaxar o teste.
    print("\n3) hierarquia (ou a falta dela)")
    api = bea._get_api(method="GetData", datasetname="NIUnderlyingDetail",
                       TableName=bea.TABELA_PCE_INDICE, Frequency="M", Year="2026")
    dados = api["Results"]["Data"]
    campos = set()
    for r in dados:
        campos |= set(r.keys())
    suspeitos = sorted(c for c in campos
                       if any(w in c.lower()
                              for w in ("parent", "level", "indent", "hier", "depth")))
    ok(not suspeitos,
       "GetData nao tem campo de pai/nivel/indentacao "
       "(se falhar, o BEA passou a publicar hierarquia -- boa noticia, revisar a dim)",
       f"campos: {sorted(campos)}")
    ok("METRIC_NAME" in campos,
       "o campo e METRIC_NAME em maiusculas (o guia oficial escreve Metric_Name)")
    ok("NoteRef" in campos, "ha um 10o campo, NoteRef, que o guia nao lista")
    indentados = [r for r in dados if r["LineDescription"] != r["LineDescription"].lstrip()]
    ok(not indentados,
       "LineDescription vem sem os espacos de indentacao que o xlsx tem na coluna B",
       f"{len(indentados)} indentados")
    lns = sorted({int(r["LineNumber"]) for r in dados})
    ok(lns[0] == 1, "LineNumber comeca em 1 (e ordem na tabela, nao profundidade)",
       f"{len(lns)} linhas, {lns[0]}..{lns[-1]}")

    # -----------------------------------------------------------------------
    # 4) erro vem com HTTP 200 -- e nao vaza a chave
    # -----------------------------------------------------------------------
    print("\n4) tratamento de erro")
    chave = os.environ["BEA_API_KEY"].strip()
    for rotulo, kw in (("tabela inexistente (erro em BEAAPI.Error)",
                        dict(TableName="U99999", Frequency="M", Year="2026")),
                       ("ano fora do range", dict(TableName=bea.TABELA_PCE_INDICE,
                                                  Frequency="M", Year="1800"))):
        try:
            bea._get_api(method="GetData", datasetname="NIUnderlyingDetail", **kw)
            ok(False, f"{rotulo}: levanta RuntimeError", "nao levantou")
        except RuntimeError as e:
            ok(True, f"{rotulo}: levanta RuntimeError", str(e)[:70])
            ok(chave not in str(e), f"{rotulo}: a mensagem nao vaza a chave")

    # chave invalida cai no OUTRO no (BEAAPI.Results.Error) -- olhar so um dos dois
    # deixaria isto passar como resposta valida e vazia
    guardada = os.environ["BEA_API_KEY"]
    os.environ["BEA_API_KEY"] = "NAO-EXISTE"
    try:
        bea._get_api(method="GetData", datasetname="NIUnderlyingDetail",
                     TableName=bea.TABELA_PCE_INDICE, Frequency="M", Year="2026")
        ok(False, "chave invalida: levanta (erro em BEAAPI.Results.Error)", "nao levantou")
    except RuntimeError as e:
        ok("UserId" in str(e) or "1" in str(e),
           "chave invalida: levanta (erro em BEAAPI.Results.Error)", str(e)[:70])
    finally:
        os.environ["BEA_API_KEY"] = guardada

    os.environ["BEA_API_KEY"] = ""
    try:
        bea.ler_tabela_api(bea.TABELA_PCE_INDICE, anos="2026")
        ok(False, "sem chave: levanta com mensagem acionavel", "nao levantou")
    except RuntimeError as e:
        ok("apps.bea.gov/API/signup" in str(e) and "xlsx" in str(e),
           "sem chave: levanta dizendo que o caminho de xlsx dispensa chave")
    finally:
        os.environ["BEA_API_KEY"] = guardada

    # -----------------------------------------------------------------------
    # 5) a fonte fica marcada, e a dim recusa a API
    # -----------------------------------------------------------------------
    print("\n5) marca de fonte")
    a = bea.ler_tabela_api(bea.TABELA_PCE_INDICE, anos="2026")
    x = bea.ler_tabela(bea.ABA_PCE_INDICE)
    ok(a.fonte == "api" and x.fonte == "xlsx", "cada porta se identifica em `fonte`")
    ok(a.estrutura["indentacao"].isna().all(),
       "a estrutura da API vem sem indentacao (nao ha de onde tirar)")
    ok(x.estrutura["indentacao"].notna().all(), "a do xlsx vem com indentacao")
    ok(a.publicado_em and x.publicado_em,
       "as duas portas trazem data de publicacao",
       f"api={a.publicado_em!r} xlsx={x.publicado_em!r}")
    ok(a.titulo == x.titulo, "titulo identico nas duas", a.titulo[:56])
    ok(a.unidade == x.unidade, "unidade identica nas duas")
    ok(a.sazonalidade == x.sazonalidade == "SA", "as duas se declaram SA")

    from domain.db.us.inflation import inflc_pce_dim
    src = Path(inflc_pce_dim.__file__).read_text(encoding="utf-8")
    ok('fonte != "xlsx"' in src,
       "inflc_pce_dim recusa fonte que nao seja xlsx (a arvore precisa da indentacao)")

    # -----------------------------------------------------------------------
    # 6) o caminho de CARGA: inflc_pce le da API
    # -----------------------------------------------------------------------
    # Nada aqui grava no banco -- `gravar` e substituido. O que interessa e o que o
    # script monta e o que ele recusa a gravar.
    print("\n6) carga (inflc_pce, fonte=api)")

    ok(bea.anos_param(2024, 2026) == "2024,2025,2026",
       "anos_param monta a lista de anos do pedido")
    ok(bea.anos_param() == "X", "anos_param() sem janela = serie inteira")
    for rot, arg in (("so um ano", (2024, None)), ("janela invertida", (2026, 2024))):
        try:
            bea.anos_param(*arg)
            ok(False, f"anos_param recusa {rot}", "nao levantou")
        except ValueError:
            ok(True, f"anos_param recusa {rot}")

    from domain.db.us.inflation import inflc_pce

    gravado = {}
    real_gravar = inflc_pce.gravar
    inflc_pce.gravar = lambda db, t, df, **kw: gravado.update(n=len(df), df=df)
    real_ler = inflc_pce.ler_tabela
    real_cache = inflc_pce.caminho_cache_hoje
    try:
        inflc_pce.run(start_year=2026, medidas=("indice",))
        ok(gravado.get("n", 0) > 2_000, "a carga de 2026 monta as linhas",
           f"{gravado.get('n', 0):,} linhas")
        ok(set(gravado["df"].columns) == {"date", "linha", "medida", "value", "code"},
           "com as colunas da tabela")
        ok(gravado["df"]["code"].notna().all(), "e com o SeriesCode preenchido")

        # sem xlsx em cache a conferencia e PULADA, nao forcada -- baixar 12 MB so
        # para conferir custaria mais que a propria carga
        gravado.clear()
        inflc_pce.caminho_cache_hoje = lambda: None
        inflc_pce.run(start_year=2026, medidas=("indice",))
        ok(gravado.get("n", 0) > 2_000, "sem xlsx em cache a carga segue (conferencia pulada)")

        # e se as duas portas divergirem, nao grava
        class _Mexida:
            def __init__(s, t):
                s.t = t

            def __getattr__(s, k):
                return getattr(s.t, k)

            @property
            def observacoes(s):
                o = s.t.observacoes.copy()
                # dentro da janela conferida, senao o filtro de ano descarta a linha
                alvo = o[[d.year == 2026 for d in o["date"]]].index[0]
                o.loc[alvo, "value"] = o.loc[alvo, "value"] + 0.1
                return o

        gravado.clear()
        inflc_pce.caminho_cache_hoje = lambda: Path("existe.xlsx")
        inflc_pce.ler_tabela = lambda aba, caminho=None: _Mexida(real_ler(aba))
        try:
            inflc_pce.run(start_year=2026, medidas=("indice",))
            ok(False, "divergencia entre as portas levanta antes de gravar", "gravou")
        except RuntimeError as e:
            ok("discordam" in str(e), "divergencia entre as portas levanta antes de gravar")
        ok(not gravado, "e nada foi gravado")
    finally:
        inflc_pce.gravar = real_gravar
        inflc_pce.ler_tabela = real_ler
        inflc_pce.caminho_cache_hoje = real_cache

    # -----------------------------------------------------------------------
    # 7) uma TERCEIRA fonte: as linhas 1 e 374 contra o FRED
    # -----------------------------------------------------------------------
    # As secoes 2 e 6 conferem as duas portas do BEA uma contra a outra, o que pega
    # erro de leitura mas nao pega erro de IDENTIFICACAO: se a linha 374 nao fosse o
    # core, as duas portas concordariam do mesmo jeito. O FRED serve `PCEPI` e
    # `PCEPILFE` (o proprio BEA, redistribuido) e e por isso a checagem que sobra.
    #
    # Nao ha valor esperado escrito aqui de proposito: o BEA revisa os meses
    # anteriores em cada divulgacao (junho/2026 saiu de 131.392 para 131.454 em
    # 26/08/2026), entao qualquer numero fixo envelhece. A assercao e que as duas
    # fontes concordam AGORA, seja qual for o vintage.
    print("\n7) contra o FRED (PCEPI / PCEPILFE)")
    fred_key = os.environ.get("FRED_API_KEY", "").strip()
    if not fred_key:
        print("  SKIP -- FRED_API_KEY nao esta no .env; a identificacao das linhas 1 e")
        print("          374 (headline e core) fica sem conferencia independente.")
    else:
        import json
        import urllib.parse
        import urllib.request

        a_idx = bea.ler_tabela_api(bea.TABELA_PCE_INDICE, anos=bea.anos_param(2025, 2026))
        nosso = {}
        for r in a_idx.observacoes.itertuples():
            if int(r.linha) in (1, 374):
                nosso[(int(r.linha), r.date.isoformat()[:7])] = r.value

        for linha, sid, rotulo in ((1, "PCEPI", "headline"), (374, "PCEPILFE", "core")):
            q = {"series_id": sid, "api_key": fred_key, "file_type": "json",
                 "observation_start": "2025-01-01"}
            url = ("https://api.stlouisfed.org/fred/series/observations?"
                   + urllib.parse.urlencode(q))
            with urllib.request.urlopen(url, timeout=60) as r:
                obs = json.loads(r.read())["observations"]
            pares = [(o["date"][:7], float(o["value"]), nosso[(linha, o["date"][:7])])
                     for o in obs
                     if o["value"] not in (".", "") and (linha, o["date"][:7]) in nosso]
            piores = sorted(((abs(f - n), m, f, n) for m, f, n in pares), reverse=True)
            d, m, f, n = piores[0] if piores else (0.0, "-", 0, 0)
            ok(len(pares) >= 12, f"linha {linha} ({rotulo}): meses comparaveis com {sid}",
               f"{len(pares)} meses")
            ok(d <= 0.0005, f"linha {linha} ({rotulo}) = {sid} do FRED",
               f"pior {m}: BEA {n} vs FRED {f} (dif {d:.4g})")

    # -----------------------------------------------------------------------
    # 8) a arvore vem do MySQL, e a API prova que ela continua valida
    # -----------------------------------------------------------------------
    # O xlsx e o unico lugar com a hierarquia, mas ela nao muda de mes para mes --
    # entao e gravada e reaproveitada, e o arquivo virou caminho de reparo. O que
    # sustenta isso sao DUAS checagens complementares, e esta secao exercita as duas
    # mais a igualdade do resultado.
    print("\n8) arvore reaproveitada (inflc_pce_dim, fonte=auto)")
    from domain.db.us.inflation import inflc_pce_dim as dim

    gravada = dim._estrutura_gravada()
    if gravada is None:
        print("  SKIP -- nada gravado em inflc_pce_dim (ou banco fora); o caminho")
        print("          auto nao tem o que reaproveitar.")
    else:
        capturado = {}
        real_gravar = dim.gravar
        dim.gravar = lambda db, t, df, **kw: capturado.__setitem__(t, df.copy())
        try:
            dim.run()                      # auto: API + estrutura gravada
            auto = capturado.pop("inflc_pce_dim")
            dim.run(fonte="xlsx")          # reconstrucao completa do arquivo
            xlsx = capturado.pop("inflc_pce_dim")
        finally:
            dim.gravar = real_gravar

        a = auto.set_index("linha").sort_index()
        x = xlsx.set_index("linha").sort_index()
        ok(len(a) == len(x) == 402, "as duas rotas gravam as mesmas 402 linhas",
           f"auto={len(a)} xlsx={len(x)}")
        difs = []
        for c in x.columns:
            neq = ~((a[c] == x[c]) | (a[c].isna() & x[c].isna()))
            if neq.any():
                difs.append(f"{c}({int(neq.sum())})")
        ok(not difs, "e a tabela e IDENTICA coluna a coluna",
           ", ".join(difs) or f"{len(x.columns)} colunas + a chave `linha`")

        # --- metade 1 do guarda: o conjunto de linhas ---
        # A API devolve registro so onde ha dado, entao ausencia NAO e remocao: as 2
        # linhas ZZZZZZ nao tem indice de preco em nenhuma janela, e 157/158 foram
        # descontinuadas em 2001-12. Um falso positivo aqui mandaria baixar 12 MB
        # todo mes -- foi exatamente o bug da primeira versao.
        est = gravada[["linha", "rotulo", "code"]].copy()
        ok(dim._conjunto_mudou(gravada, est, "idx", "2025-01",
                               ("rotulo", "code")) is None,
           "conjunto igual a si mesmo nao acusa mudanca")

        sem_descontinuadas = est[~est["linha"].isin([145, 157, 158, 333])]
        ok(dim._conjunto_mudou(gravada, sem_descontinuadas, "idx", "2025-01",
                               ("rotulo", "code")) is None,
           "as 2 linhas ZZZZZZ e as descontinuadas em 2001 podem faltar sem alarme")

        viva = int(gravada.loc[gravada["idx_end"] == gravada["idx_end"].dropna().max(),
                               "linha"].iloc[0])
        r = dim._conjunto_mudou(gravada, est[est["linha"] != viva], "idx", "2025-01",
                                ("rotulo", "code"))
        ok(r is not None and "pararam de vir" in r,
           f"mas uma linha que publicava ate agora (#{viva}) desaparecer, sim", str(r)[:60])

        renomeada = est.copy()
        renomeada.loc[renomeada["linha"] == 1, "rotulo"] = "Outra coisa"
        r = dim._conjunto_mudou(gravada, renomeada, "idx", "2025-01", ("rotulo", "code"))
        ok(r is not None and "rotulo" in r, "rotulo diferente acusa", str(r)[:60])

        nova = pd.concat([est, pd.DataFrame([{"linha": 9999, "rotulo": "Nova",
                                              "code": "XX"}])], ignore_index=True)
        r = dim._conjunto_mudou(gravada, nova, "idx", "2025-01", ("rotulo", "code"))
        ok(r is not None and "novas" in r, "linha nova acusa", str(r)[:60])

        recodificada = est.copy()
        recodificada.loc[recodificada["linha"] == 1, "code"] = "ZZZZZZ"
        r = dim._conjunto_mudou(gravada, recodificada, "idx", "2025-01",
                                ("rotulo", "code"))
        ok(r is not None and "code" in r, "codigo diferente acusa (na tabela de indice)",
           str(r)[:60])

        # --- metade 2 do guarda: re-indentacao, que a metade 1 nao ve ---
        # Se o BEA mover uma linha para outro pai sem mudar numero, rotulo nem
        # codigo, o conjunto bate. O que pega e a aditividade rodada com os valores
        # da API sobre a arvore GRAVADA: um pai trocado de lugar move bilhoes.
        nom = bea.ler_tabela_api(bea.TABELA_PCE_NOMINAL, anos=bea.anos_param(2025, 2026))
        obs = nom.observacoes.copy()
        obs["date"] = pd.to_datetime(obs["date"])
        dim._validar_aditividade(gravada, obs)   # a arvore de verdade fecha
        ok(True, "a arvore gravada fecha em nominal contra os valores da API")

        trocada = gravada.copy()
        alvo = trocada[(trocada["nivel"] == 3) & (trocada["bloco"] == "principal")].iloc[0]
        outro = trocada[(trocada["nivel"] == 2) & (trocada["bloco"] == "principal")
                        & (trocada["linha"] != alvo["parent_linha"])].iloc[0]
        trocada.loc[trocada["linha"] == alvo["linha"], "parent_linha"] = outro["linha"]
        try:
            dim._validar_aditividade(trocada, obs)
            ok(False, "re-indentacao (linha trocada de pai) e detectada", "nao levantou")
        except ValueError as e:
            ok("nao fecham" in str(e),
               f"re-indentacao e detectada (linha {int(alvo['linha'])} movida para "
               f"{int(outro['linha'])})", str(e)[:58])

        # --- cobertura: o fim anda, o comeco nao ---
        atualizada = dim._atualizar_cobertura(gravada, obs.assign(value=1.0), obs)
        ok((atualizada["nom_begin"] == gravada["nom_begin"]).all(),
           "atualizar cobertura preserva o comeco de cada serie")
        vivas = gravada["nom_end"] >= "2025-01"
        ok((atualizada.loc[vivas, "nom_end"] >= gravada.loc[vivas, "nom_end"]).all(),
           "e nunca faz o fim retroceder nas series vivas")
        desc = gravada["nom_end"] < "2025-01"
        if desc.any():
            ok((atualizada.loc[desc, "nom_end"] == gravada.loc[desc, "nom_end"]).all(),
               "series descontinuadas conservam o fim gravado",
               f"{int(desc.sum())} linhas")

    print()
    if _falhas:
        print(f"FALHOU: {len(_falhas)} de {len(_falhas)} + OKs")
        for f in _falhas:
            print(f"  - {f}")
        return 1
    print("todas as assercoes passaram")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
