"""
Gera `reports/us/Labor Market.html` a partir das tres pesquisas de mercado de trabalho
do BLS que estao no banco: JOLTS (`mt_jolts`), CES (`mt_ces`, o payroll) e CPS
(`mt_cps`, as manchetes domiciliares), mais as quatro derivadas que cruzam as tres.

    uv run python -c "from analytics.us.labor_market.generate_report import run; run()"

**UI em ingles**, como `analytics/us/inflation/` -- e um produto americano lido
contra fontes americanas, e as notas de `us_project/` ja estao em ingles.

--------------------------------------------------------------------------------
O QUE VAI NO PAYLOAD, E O QUE E DERIVADO NO NAVEGADOR
--------------------------------------------------------------------------------
Vai: o **valor mensal publicado** por (corte, categoria, medida, tipo, ajuste), numa
grade de datas unica na raiz, series como arrays nus alinhados a ela. 960 series x
308 meses, 1,86 MB. (960 e nao 961 porque a razao `UO` fica fora da consulta -- ela
esta na tabela e nao nesta pagina; ver o ultimo bloco.)

Nao vai: media de 3 e de 12 meses, acumulado de 12 meses, variacao anual e a
**participacao no total** (o tipo `% of total`, que e o nivel dividido pelo nivel da
raiz da propria arvore). Todas saem do valor mensal em JS, cacheadas por (chave,
transformacao). Embarcar as transformacoes seria varias vezes os numeros por
informacao que o mensal ja implica, e deixaria o gravado e o exibido divergirem --
mesma decisao de `analytics/us/inflation`, que embarca nivel de indice e deriva todas
as variacoes.

A grade e **uma para os tres cortes e os dois ajustes**, e isso e conferido em vez de
suposto (`_grade`): as 913 series do JOLTS comecam todas em 2000-12 e terminam todas
no mesmo mes. Se o BLS passar a publicar um corte com atraso diferente, a montagem
levanta em vez de deslocar uma serie no tempo em silencio -- que e o defeito que o
teste de payload de `analytics/brasil/expectations` existe para pegar.

--------------------------------------------------------------------------------
TRES GRADES DE DATA, E ELAS **NAO** SAO A MESMA
--------------------------------------------------------------------------------
    JOLTS   2000-12 -> o mes corrente, todas as series na mesma janela
    CES     1939-01 -> o mes corrente, **borda direita irregular** por profundidade
    CPS     1948-01 -> o mes corrente, com outubro/2025 ausente (paralisacao)

O `_grade()` do JOLTS levanta se os tres cortes nao compartilharem a janela, e faz
sentido ali. Para a CES a mesma checagem reprovaria um passe correto: a primeira
divulgacao de um mes traz os agregados e o detalhe vem na seguinte, entao no mes mais
recente so 27 das 555 folhas tem dado. Cada fonte carrega a sua grade e a sua regra.

--------------------------------------------------------------------------------
AS QUATRO DERIVADAS SAO AS UNICAS CONTAS QUE NAO SAO DE EXIBICAO
--------------------------------------------------------------------------------
Vagas por desempregado, contratacao liquida, curva de Beveridge e a divergencia
CES x CPS. Elas so passaram a ser possiveis nesta rodada, e o escopo do JOLTS foi
fechado sem elas justamente esperando isto. Ficam em `derivadas_tab.py`, que e onde
esta tambem o gabarito: a razao vagas/desempregado e conferida contra a serie que o
proprio BLS publica -- **o reciproco dela**, ver o docstring de la.
"""

from __future__ import annotations

import datetime as _dt
from pathlib import Path

import pandas as pd

from analytics.report_structure.builder import render_report
from analytics.us.labor_market import ces_tab, cps_tab, derivadas_tab, jolts_tab
from domain.db.us._gravar import ler

_DATABASE = "macro_us"
_AQUI = Path(__file__).parent
_TEMPLATE = _AQUI / "report.html"
_SAIDA = Path(__file__).resolve().parents[3] / "reports" / "us" / "Labor Market.html"

# Ajustes e tipos, com o rotulo que a pill mostra.
_AJUSTES = [("sa", "Seasonally adjusted"), ("nsa", "Not adjusted")]
# `share` NAO e um tipo da tabela: nao existe em `mt_jolts`. E o nivel dividido pelo
# nivel da RAIZ da propria arvore, derivado no navegador -- ver `garantirShare()` no
# report.html. Entra aqui porque a lista alimenta as pills.
_TIPOS = [("nivel", "Level"), ("taxa", "Rate"), ("share", "% of total")]


def _ler_tudo() -> tuple[pd.DataFrame, pd.DataFrame]:
    dim = ler(_DATABASE, "SELECT * FROM mt_jolts_dim ORDER BY corte, ordem")
    dados = ler(
        _DATABASE,
        "SELECT date, corte, categoria, medida, tipo, ajuste, valor, preliminar "
        "FROM mt_jolts WHERE medida <> 'UO' ORDER BY date",
    )
    if dim.empty or dados.empty:
        raise RuntimeError(
            "mt_jolts / mt_jolts_dim vazias -- rode "
            "`from domain.db.us.labor_market import mt_jolts; mt_jolts.run()` primeiro."
        )
    dados["date"] = pd.to_datetime(dados["date"])
    return dim, dados


def _ler_ces() -> tuple[pd.DataFrame, pd.DataFrame]:
    """A arvore e os dados da CES, ja recortados ao que a pagina mostra.

    O recorte de horas/ganhos aos niveis 0-4 e de PAYLOAD, nao de dado: sao 94
    industrias contra 549, a granularidade que as tabelas B-2/B-3/B-4 do release
    publicam, e o banco guarda as 549. Sem ele o arquivo passa de 20 MB.
    """
    dim = ler(_DATABASE, "SELECT * FROM mt_ces_dim ORDER BY ordem")
    if dim.empty:
        raise RuntimeError(
            "mt_ces_dim vazia -- rode `from domain.db.us.labor_market import mt_ces; "
            "mt_ces.run(anos='all')` primeiro."
        )
    niveis_horas = ces_tab.NIVEL_MAX_HORAS
    medidas_horas = "','".join(ces_tab.ORDEM_HORAS)
    dados = ler(
        _DATABASE,
        "SELECT c.date, c.categoria, c.medida, c.ajuste, c.valor "
        "FROM mt_ces c JOIN mt_ces_dim d ON d.categoria = c.categoria "
        "WHERE d.alternativo = 0 AND ("
        "  c.medida = 'emprego'"
        f"  OR (c.medida IN ('{medidas_horas}') AND d.nivel <= {niveis_horas})"
        ") ORDER BY c.date",
    )
    dados["date"] = pd.to_datetime(dados["date"])
    return dim, dados


def _ler_cps() -> pd.DataFrame:
    d = ler(_DATABASE, "SELECT date, categoria, ajuste, valor, grupo, unidade "
                       "FROM mt_cps ORDER BY date")
    if d.empty:
        raise RuntimeError(
            "mt_cps vazia -- rode `from domain.db.us.labor_market import mt_cps; "
            "mt_cps.run()` primeiro."
        )
    d["date"] = pd.to_datetime(d["date"])
    return d


def _grade_simples(dados: pd.DataFrame) -> list[str]:
    """A grade mensal contigua que cobre os dados, SEM exigir janela comum.

    E o oposto do `_grade()` do JOLTS de proposito: na CES a borda direita e irregular
    por construcao, e na CPS falta outubro/2025. Uma grade contigua com None nos vazios
    e o que impede a compressao de deslocar serie no tempo.
    """
    a, b = dados["date"].min(), dados["date"].max()
    return [d.strftime("%Y-%m-%d") for d in pd.date_range(a, b, freq="MS")]


def _series_por(dados: pd.DataFrame, grade: list[str], chaves: list[str],
                dec: int = 4) -> dict:
    """`'<a>|<b>|...' -> {i0, v}`, com `i0` = indice na grade do primeiro valor.

    A compressao e obrigatoria aqui, nao uma otimizacao. A CES vai de 1939 a 2026 e a
    maior parte das 3.496 series comeca em 1990: um array cheio de nulos por serie
    gasta ~600 posicoes so escrevendo a palavra `null`, e o payload sai 26 MB contra 8.
    Mesma tecnica de `analytics/brasil/expectations`.

    O que NAO pode acontecer e cortar buraco INTERNO: `v` e contigua mes a mes a partir
    de `i0`, com None onde falta -- outubro/2025 na CPS, por exemplo. Um `dropna()` ali
    desloca todos os meses seguintes um mes para tras sem lancar excecao (o defeito que
    o teste de payload de `expectations` existe para pegar).
    """
    idx = {d: i for i, d in enumerate(grade)}
    dados = dados.copy()
    dados["i"] = dados["date"].dt.strftime("%Y-%m-%d").map(idx)
    if dados["i"].isna().any():
        raise RuntimeError("ha datas fora da grade -- a grade nao cobre os dados")
    saida = {}
    for chave, sub in dados.groupby(chaves, sort=False):
        pares = [(int(i), v) for i, v in zip(sub["i"], sub["valor"]) if pd.notna(v)]
        if not pares:
            continue
        i0 = min(p[0] for p in pares)
        i1 = max(p[0] for p in pares)
        vetor = [None] * (i1 - i0 + 1)
        for i, v in pares:
            vetor[i - i0] = round(float(v), dec)
        nome = "|".join(chave if isinstance(chave, tuple) else (chave,))
        saida[nome] = {"i0": i0, "v": vetor}
    return saida


def _grade(dados: pd.DataFrame) -> list[str]:
    """A grade mensal comum, conferindo que ela E comum.

    Nao basta tomar `sorted(unique(date))`: isso produziria uma grade valida mesmo se
    um corte estivesse um mes atras, e a serie curta apareceria alinhada a esquerda,
    deslocada no tempo, sem lacuna visivel. A checagem e por (corte, ajuste).
    """
    fins = (dados.dropna(subset=["valor"])
                 .groupby(["corte", "ajuste"])["date"].agg(["min", "max"]))
    if fins["max"].nunique() > 1 or fins["min"].nunique() > 1:
        raise RuntimeError(
            "os cortes do JOLTS deixaram de compartilhar a mesma janela mensal:\n"
            + fins.to_string()
            + "\nUma grade unica alinharia a serie mais curta a esquerda e a deslocaria "
              "no tempo sem lacuna visivel. Trate a janela por corte antes de gerar."
        )
    datas = sorted(dados["date"].unique())
    return [pd.Timestamp(d).strftime("%Y-%m-%d") for d in datas]


def _series(dados: pd.DataFrame, grade: list[str]) -> dict:
    """`'corte|categoria|medida|tipo|ajuste' -> [valores]`, alinhado a `grade`."""
    idx = {d: i for i, d in enumerate(grade)}
    dados = dados.copy()
    dados["i"] = dados["date"].dt.strftime("%Y-%m-%d").map(idx)

    saida = {}
    chaves = ["corte", "categoria", "medida", "tipo", "ajuste"]
    for chave, sub in dados.groupby(chaves, sort=False):
        vetor = [None] * len(grade)
        for i, v in zip(sub["i"], sub["valor"]):
            vetor[int(i)] = None if pd.isna(v) else round(float(v), 4)
        saida["|".join(chave)] = vetor
    return saida


def _preliminares(dados: pd.DataFrame) -> list[str]:
    """Meses marcados como preliminares pelo BLS, para a nota do relatorio."""
    p = dados[dados["preliminar"] == 1]["date"]
    return sorted({pd.Timestamp(d).strftime("%Y-%m-%d") for d in p.unique()})


def construir() -> dict:
    """Monta o payload. Separado de `run()` para o teste poder afirmar sobre ele."""
    dim, dados = _ler_tudo()
    grade = _grade(dados)
    arvs = jolts_tab.arvores(dim)

    orfas = jolts_tab.orfaos_info(arvs)
    if orfas:
        raise RuntimeError(
            f"{len(orfas)} chaves do INFO nao resolvem contra as arvores reais: {orfas}. "
            "Uma chave errada produz um botao que nunca nasce -- sem erro e sem lacuna "
            "visivel."
        )
    redundantes = jolts_tab.full_redundante(arvs)
    if redundantes:
        raise RuntimeError(
            f"{len(redundantes)} entradas do INFO tem `full` igual ao rotulo curto que a "
            f"linha ja mostra: {redundantes}. O cartao abriria para repetir o que o leitor "
            "acabou de ler -- remova o `full`, nao a entrada."
        )

    series = _series(dados, grade)
    prelim = _preliminares(dados)

    # Cobertura por corte: quantas series cada um traz, para a nota da aba dizer isso
    # em vez de o texto afirmar um numero que envelhece.
    cobertura = {}
    for corte in arvs:
        sub = dados[dados["corte"] == corte]
        cobertura[corte] = {
            "nSeries": int(sub.groupby(["categoria", "medida", "tipo", "ajuste"]).ngroups),
            "nObs": int(len(sub)),
        }

    ces = _payload_ces()
    cps = _payload_cps()
    derivadas = _payload_derivadas()

    info = dict(jolts_tab.INFO)
    info.update(ces["info"])
    info.update(cps_tab.INFO)

    return {
        "meta": {
            "gerado": _dt.datetime.now().strftime("%Y-%m-%d %H:%M"),
            "ultimoMes": grade[-1],
            "primeiroMes": grade[0],
            "nMeses": len(grade),
            "nSeries": len(series) + len(ces["series"]) + len(cps["series"]),
            "preliminares": prelim,
            "fonte": "BLS, Job Openings and Labor Turnover Survey (JOLTS)",
            "fonteCes": "BLS, Current Employment Statistics (establishment survey)",
            "fonteCps": "BLS, Current Population Survey (household survey)",
            "cesUltimoMes": ces["dates"][-1],
            "cpsUltimoMes": cps["dates"][-1],
        },
        "dates": grade,
        "medidas": jolts_tab.MEDIDAS,
        "ordemMedidas": jolts_tab.ORDEM_MEDIDAS,
        "tipos": [{"key": k, "label": v} for k, v in _TIPOS],
        "ajustes": [{"key": k, "label": v} for k, v in _AJUSTES],
        "cortes": arvs,
        "cobertura": cobertura,
        "series": series,
        "ces": ces,
        "cps": cps,
        "derivadas": derivadas,
        "info": info,
    }


def _payload_ces() -> dict:
    """As duas abas da CES: emprego (raiz Total nonfarm) e horas/ganhos (Total private).

    As duas arvores tem RAIZES diferentes porque a CES nao publica horas nem ganhos do
    setor publico. Um seletor de medida numa aba unica faria o total mudar de
    significado no clique -- mesma razao pela qual os tres cortes do JOLTS ficam em
    cards separados.
    """
    dim, dados = _ler_ces()
    grade = _grade_simples(dados)
    series = _series_por(dados, grade, ["categoria", "medida", "ajuste"])

    arv_emprego = ces_tab.arvore(dim, raiz="00000000")
    arv_horas = ces_tab.arvore(dim, raiz="05000000",
                               nivel_max=ces_tab.NIVEL_MAX_HORAS, exigir_horas=True)

    # Cobertura por mes: quantas linhas da arvore de emprego ja tem dado. E o que o
    # cabecalho usa para nao desenhar a borda irregular como se fosse queda.
    chaves = achatar_keys(arv_emprego)
    idx = {d: i for i, d in enumerate(grade)}
    presentes = [0] * len(grade)
    sub = dados[(dados["medida"] == "emprego") & (dados["ajuste"] == "sa")
                & dados["categoria"].isin(chaves) & dados["valor"].notna()]
    for d, n in sub.groupby(sub["date"].dt.strftime("%Y-%m-%d")).size().items():
        presentes[idx[d]] = int(n)

    return {
        "dates": grade,
        "series": series,
        "medidas": ces_tab.MEDIDAS,
        "abas": {
            "emprego": {
                "label": "Payroll employment",
                "colLabel": "Industry",
                "raiz": "00000000",
                "raizLabel": arv_emprego[0]["label"],
                "tree": arv_emprego,
                "nLinhas": len(chaves),
                "niveis": 1 + max(n["nivel"] for n in ces_tab.achatar(arv_emprego)),
                "ordemMedidas": ces_tab.ORDEM_EMPREGO,
                "note": (
                    "Every filled job on the payroll of a surveyed establishment, for the "
                    "pay period that includes the 12th of the month. The tree follows the "
                    "BLS's own industry hierarchy, and the branches sum to their parent — "
                    "<b>in the not-adjusted data</b>. Seasonal adjustment is done "
                    "independently for each series, so in the adjusted view the parts do "
                    "not add exactly; the deviation is under a tenth of a percent at the "
                    "supersector level and grows with depth."
                ),
            },
            "horas": {
                "label": "Hours and earnings",
                "colLabel": "Industry",
                "raiz": "05000000",
                "raizLabel": arv_horas[0]["label"],
                "tree": arv_horas,
                "nLinhas": len(achatar_keys(arv_horas)),
                "niveis": 1 + max(n["nivel"] for n in ces_tab.achatar(arv_horas)),
                "ordemMedidas": ces_tab.ORDEM_HORAS,
                "note": (
                    "Hours and earnings of <b>all employees</b>, from the same "
                    "establishment survey. The tree starts at Total private because the "
                    "survey does not collect hours or earnings for government — so this "
                    "total is about 23 million jobs smaller than the payroll total above. "
                    "Shown to the level of detail the release's own tables B-2 to B-4 "
                    "publish; the database holds the finer industries."
                ),
            },
        },
        "info": ces_tab.cartoes(dim, "ces"),
        "coberturaMes": presentes,
        "nLinhasArvore": len(chaves),
    }


def achatar_keys(tree: list[dict]) -> list[str]:
    return [n["key"] for n in ces_tab.achatar(tree)]


def _payload_cps() -> dict:
    dados = _ler_cps()
    grade = _grade_simples(dados)
    series = _series_por(dados, grade, ["categoria", "ajuste"])
    presentes = set(dados["categoria"])

    orf = cps_tab.orfaos(presentes)
    if orf:
        raise RuntimeError(
            f"{len(orf)} categorias da CPS declaradas em cps_tab.LINHAS e ausentes do "
            f"banco (ou o contrario): {orf}. Uma linha declarada e ausente nao aparece "
            "na tabela, sem erro."
        )
    info_orf = cps_tab.info_orfaos()
    if info_orf:
        raise RuntimeError(f"chaves do INFO da CPS que nao resolvem: {info_orf}")
    red = cps_tab.full_redundante()
    if red:
        raise RuntimeError(
            f"{len(red)} cartoes da CPS tem `full` igual ao rotulo curto: {red}")

    blocos = []
    for chave, rotulo, aditivo in cps_tab.BLOCOS:
        if chave == "composicao":
            linhas = cps_tab.linhas_do_bloco("composicao", presentes)
        else:
            linhas = cps_tab.linhas_do_bloco(chave, presentes)
        blocos.append({"key": chave, "label": rotulo, "aditivo": aditivo,
                       "linhas": linhas})
    return {
        "dates": grade,
        "series": series,
        "blocos": blocos,
        "eixos": [{"key": k, "label": v} for k, v in cps_tab.EIXOS_COMPOSICAO],
        "unidades": cps_tab.unidade_por_linha(dados),
        "rotuloUnidade": cps_tab.UNIDADES,
    }


def _payload_derivadas() -> dict:
    jolts = ler(_DATABASE, "SELECT date, medida, tipo, ajuste, valor FROM mt_jolts "
                           "WHERE corte='industria' AND categoria='000000'")
    cps = ler(_DATABASE, "SELECT date, categoria, ajuste, valor FROM mt_cps")
    ces = ler(_DATABASE, "SELECT date, categoria, medida, ajuste, valor FROM mt_ces "
                         "WHERE categoria='00000000' AND medida='emprego'")
    for d in (jolts, cps, ces):
        d["date"] = pd.to_datetime(d["date"])
    return derivadas_tab.construir(jolts, cps, ces)


def run(output: str | Path | None = None) -> Path:
    """Gera o relatorio.

    Args:
        output: caminho de saida. Default `reports/us/Labor Market.html` -- `reports/`
                espelha o layout pais > area de `analytics/`, e sem isso um
                `Labor Market.html` do Brasil colidiria com este. O nome do parametro e
                `output` e nao `saida` porque `domain/dashboards/status.gerar()` chama
                `mod.run(output=...)` para poder gravar o stamp junto; um nome diferente
                faz o botao "Regerar" do calendario estourar com TypeError.

    Returns:
        O caminho gravado.
    """
    dados = construir()
    destino = Path(output) if output else _SAIDA
    caminho = render_report(_TEMPLATE, dados, destino)
    tam = caminho.stat().st_size / 1e6
    m = dados["meta"]
    print(f"{caminho}  ({tam:.2f} MB)")
    print(f"  {m['nSeries']} series x {m['nMeses']} meses, {m['primeiroMes']} -> {m['ultimoMes']}")
    for corte, cfg in dados["cortes"].items():
        cob = dados["cobertura"][corte]
        print(f"  jolts/{corte:8s} {cfg['nLinhas']:3d} linhas, {cfg['niveis']} niveis, "
              f"{cob['nSeries']} series")
    for aba, cfg in dados["ces"]["abas"].items():
        print(f"  ces/{aba:10s} {cfg['nLinhas']:3d} linhas, {cfg['niveis']} niveis")
    print(f"  ces        {len(dados['ces']['series']):,} series, "
          f"{dados['ces']['dates'][0]} -> {dados['ces']['dates'][-1]}")
    print(f"  cps        {len(dados['cps']['series']):,} series, "
          f"{sum(len(b['linhas']) for b in dados['cps']['blocos'])} linhas em "
          f"{len(dados['cps']['blocos'])} blocos")
    af = dados["derivadas"]["vuAferido"]
    print(f"  derivadas  vagas/desempregado conferida contra o BLS em {af['n']} meses "
          f"(erro medio {af['erroMedio']})")
    return caminho


if __name__ == "__main__":
    run()
