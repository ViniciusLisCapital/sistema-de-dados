"""
Gerador do Panorama de Expectativas (Focus) em HTML.

Le APENAS as tres tabelas do Focus de macro_brasil -- expc_focus,
expc_focus_copom e expc_focus_periodo -- e nada mais. Escopo "so Focus" e
decisao explicita do usuario (2026-08-24): sem meta de inflacao, sem realizado,
sem projecao do Copom. O que o relatorio mostra e o que o MERCADO espera, e
qualquer linha de referencia externa teria de vir com a sua propria fonte.

Abas, e de qual tabela cada uma vive:

  Boletim      expc_focus_periodo (anual) -- o Boletim Focus propriamente dito:
               mediana de hoje contra 1/4/12/52 semanas atras, por indicador e
               ano de referencia
  Revisao      expc_focus_periodo (3 periodicidades) -- fixa o periodo previsto e
               varre as datas de pesquisa. E a leitura que so esta tabela permite
  Copom        expc_focus_copom -- curva de Selic por reuniao, evolucao por
               horizonte e mapa de calor
  Horizonte    expc_focus -- IPCA/IGP-M e componentes a 12m e 24m, com os toggles
               de suavizada e base de calculo
  Trajetoria   expc_focus_periodo -- a curva a frente inteira numa data de
               pesquisa (25 meses / 8 trimestres / 5+ anos), com datas anteriores
               sobrepostas
  Dispersao    as tres -- desvio-padrao, coeficiente de variacao, respondentes
  Bases        expc_focus + expc_focus_copom -- base 0 (30 dias) vs base 1 (4 dias
               uteis). expc_focus_periodo NAO entra: so a base 0 esta carregada la
  Apendice     cobertura medida no proprio banco + as 4 reformulacoes da pesquisa

## Grade semanal

Tudo que e serie temporal e reduzido a UMA observacao por semana ISO (a ultima
data de pesquisa da semana), e os tres stores compartilham uma unica grade
global de datas -- `meta.grade`. Cada serie e gravada como {i0, m, s, n} onde
`i0` e o indice da primeira semana na grade e os arrays sao contiguos a partir
dali. Duas razoes: 1,28 M de linhas nao cabem num arquivo enviavel por email, e
o Focus e publicado semanalmente de qualquer forma (a pesquisa e diaria, o
Boletim e de segunda com dado ate sexta). O custo e que "ha 4 semanas" no
relatorio significa "4 pontos da grade atras" -- praticamente sempre 28 dias,
mas um feriado pode fazer 35.

`minimo`/`maximo` so entram nos stores de `expc_focus` e `expc_focus_copom`
(tabelas pequenas). Para o `periodo` guardamos mediana, desvio-padrao e numero
de respondentes -- as cinco estatisticas em 268 mil linhas semanais dobrariam o
arquivo por uma leitura secundaria.

Uso:
    uv run python analytics/brasil/expectations/generate_report.py
    uv run python -c "from analytics.brasil.expectations.generate_report import run; run()"
"""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

import pandas as pd

from analytics.report_structure.builder import render_report
from connectors.mysql import MySQLDataRequester

_HERE = Path(__file__).parent
_TEMPLATE = _HERE / "report.html"
_DATABASE = "macro_brasil"

# Corte do store mensal. O endpoint mensal cota 25 meses a frente desde 2000, mas
# a historia de revisao de um mes de 2003 nao tem leitor -- o valor da tabela
# mensal esta no periodo proximo. Anual e trimestral entram inteiros.
_MENSAL_REF_MIN = "2015-01-01"

# Familia de cada indicador, para agrupar os seletores e as linhas do Boletim.
# Todo indicador que a carga trouxer e que nao estiver aqui cai em "Outros" e
# aparece no log -- e sinal de que a pesquisa mudou, nao de bug do relatorio.
_FAMILIAS = {
    "IPCA": "Inflação",
    "IPCA Livres": "Inflação",
    "IPCA Administrados": "Inflação",
    "IPCA Serviços": "Inflação",
    "IPCA Bens industrializados": "Inflação",
    "IPCA Alimentação no domicílio": "Inflação",
    "IGP-M": "Inflação",
    "Selic": "Juros e câmbio",
    "Câmbio": "Juros e câmbio",
    "PIB Total": "Atividade",
    "PIB Agropecuária": "Atividade",
    "PIB Indústria": "Atividade",
    "PIB Serviços": "Atividade",
    "PIB Despesa de consumo das famílias": "Atividade",
    "PIB Despesa de consumo da administração pública": "Atividade",
    "PIB Formação Bruta de Capital Fixo": "Atividade",
    "PIB Exportação de bens e serviços": "Atividade",
    "PIB Importação de bens e serviços": "Atividade",
    "Taxa de desocupação": "Atividade",
    "Resultado primário": "Fiscal",
    "Resultado nominal": "Fiscal",
    "Dívida líquida do setor público": "Fiscal",
    "Dívida bruta do governo geral": "Fiscal",
    "Conta corrente": "Externo",
    "Balança comercial": "Externo",
    "Investimento direto no país": "Externo",
}
_ORDEM_FAMILIA = ["Inflação", "Juros e câmbio", "Atividade", "Fiscal", "Externo", "Outros"]

# Casas decimais por unidade, so para o front-end formatar. '%' cobre variacao
# (IPCA) e nivel (Selic, desocupacao) -- a unidade sozinha nao distingue, e o
# relatorio nao precisa distinguir para formatar.
_DECIMAIS = {"%": 2, "R$/US$": 4, "US$ bi": 1, "% do PIB": 2}


# ── conexao ──────────────────────────────────────────────────────────────────
def _conn():
    req = MySQLDataRequester(_DATABASE, "expc_focus")
    req.connect()
    if req.connection is None:
        raise RuntimeError(
            "sem conexao com o MySQL. Este relatorio le macro_brasil direto do "
            "banco -- nao ha CSV local de fallback. Confira o .env."
        )
    return req.connection


# ── grade semanal ────────────────────────────────────────────────────────────
def _semana(s: pd.Series) -> pd.Series:
    """Chave de semana ISO ('2026-W34') a partir de uma coluna de datas."""
    iso = s.dt.isocalendar()
    return iso["year"].astype(str) + "-W" + iso["week"].astype(int).astype(str).str.zfill(2)


def _monta_grade(conn) -> tuple[list[str], dict[str, int]]:
    """Grade global: uma data-ancora por semana ISO, a ULTIMA data de pesquisa
    daquela semana entre as tres tabelas. Devolve (lista ISO, semana -> indice)."""
    datas = pd.concat([
        pd.read_sql(f"SELECT DISTINCT date FROM {t}", conn)
        for t in ("expc_focus", "expc_focus_copom", "expc_focus_periodo")
    ])
    datas["date"] = pd.to_datetime(datas["date"])
    datas = datas.drop_duplicates().sort_values("date")
    datas["wk"] = _semana(datas["date"])
    ancoras = datas.groupby("wk")["date"].max().sort_values()
    grade = ancoras.dt.strftime("%Y-%m-%d").tolist()
    idx = {wk: i for i, wk in enumerate(ancoras.index)}
    return grade, idx


def _comprime(df: pd.DataFrame, chave: list[str], stats: dict[str, str],
              wk_idx: dict[str, int]) -> dict:
    """DataFrame semanal -> {chave: {i0, <stat>: [...]}}.

    `df` precisa ter as colunas de `chave`, uma coluna `wk` (semana ISO) e as
    colunas-fonte de `stats` ({nome_no_json: coluna_do_df}). Cada serie vira um
    bloco contiguo de indices da grade a partir de `i0`, com None nas semanas
    sem pesquisa dentro do intervalo -- o que economiza reescrever 268 mil datas
    ISO no arquivo final.
    """
    out = {}
    df = df.copy()
    df["_i"] = df["wk"].map(wk_idx)
    df = df[df["_i"].notna()]
    df["_i"] = df["_i"].astype(int)
    for chaves, grp in df.groupby(chave, sort=False):
        if not isinstance(chaves, tuple):
            chaves = (chaves,)
        grp = grp.sort_values("_i")
        i0, i1 = int(grp["_i"].iloc[0]), int(grp["_i"].iloc[-1])
        n = i1 - i0 + 1
        bloco = {"i0": i0}
        pos = (grp["_i"] - i0).to_numpy()
        for nome, col in stats.items():
            arr: list = [None] * n
            vals = grp[col].to_numpy()
            for p, v in zip(pos, vals):
                arr[int(p)] = None if pd.isna(v) else (
                    int(v) if nome == "n" else round(float(v), 4)
                )
            bloco[nome] = arr
        out["|".join(str(k) for k in chaves)] = bloco
    return out


# ── loaders ──────────────────────────────────────────────────────────────────
def _load_periodo(conn, wk_idx: dict[str, int]) -> tuple[dict, dict]:
    """expc_focus_periodo -> ({periodicidade: {serie: bloco}}, indice de rotulos).

    O JOIN reduz a leitura a uma data de pesquisa por semana ISO ANTES de sair
    do banco: sem isso sao 1,28 M de linhas na rede para descartar 80%.
    """
    stores, indice = {}, {}
    for per in ("anual", "trimestral", "mensal"):
        filtro = f" AND p.ref_date >= '{_MENSAL_REF_MIN}'" if per == "mensal" else ""
        df = pd.read_sql(
            "SELECT p.date, p.indicador, p.detalhe, p.data_referencia, p.ref_date, "
            "       p.unidade, p.mediana, p.desvio_padrao, p.numero_respondentes "
            "FROM expc_focus_periodo p "
            "JOIN (SELECT MAX(date) AS d FROM expc_focus_periodo "
            "      GROUP BY YEARWEEK(date, 3)) w ON p.date = w.d "
            f"WHERE p.periodicidade = '{per}'{filtro}",
            conn,
        )
        df["date"] = pd.to_datetime(df["date"])
        df["wk"] = _semana(df["date"])
        df["serie"] = df["indicador"] + "|" + df["detalhe"] + "|" + df["data_referencia"]

        stores[per] = _comprime(
            df, ["serie"],
            {"m": "mediana", "s": "desvio_padrao", "n": "numero_respondentes"},
            wk_idx,
        )
        # Indice de rotulos: o front-end monta os seletores a partir daqui em vez
        # de varrer 3.800 chaves de serie.
        ind = {}
        chaves = df[["indicador", "detalhe", "data_referencia", "ref_date", "unidade"]].drop_duplicates()
        for (indicador, detalhe), grp in chaves.groupby(["indicador", "detalhe"], sort=False):
            key = indicador + ("|" + detalhe if detalhe else "|")
            refs = grp.sort_values("ref_date")
            ind[key] = {
                "label": indicador + (f" — {detalhe}" if detalhe else ""),
                "indicador": indicador,
                "detalhe": detalhe,
                "familia": _FAMILIAS.get(indicador, "Outros"),
                "unidade": grp["unidade"].iloc[0],
                "dec": _DECIMAIS.get(grp["unidade"].iloc[0], 2),
                "refs": refs["data_referencia"].tolist(),
                "refDates": refs["ref_date"].astype(str).tolist(),
            }
        indice[per] = ind
        print(f"  periodo/{per:11s} {len(stores[per]):5d} series, "
              f"{sum(len(b['m']) for b in stores[per].values()):7d} pontos semanais, "
              f"{len(ind)} indicadores")
    return stores, indice


def _load_movel(conn, wk_idx: dict[str, int]) -> dict:
    """expc_focus (horizonte movel 12m/24m) -> {indicador|horizonte|suav|base: bloco}."""
    df = pd.read_sql(
        "SELECT date, indicador, horizonte, suavizada, base_calculo, mediana, "
        "       desvio_padrao, minimo, maximo, numero_respondentes FROM expc_focus",
        conn,
    )
    df["date"] = pd.to_datetime(df["date"])
    df["wk"] = _semana(df["date"])
    df = df.sort_values("date").groupby(
        ["indicador", "horizonte", "suavizada", "base_calculo", "wk"], as_index=False
    ).tail(1)
    df["serie"] = (df["indicador"] + "|" + df["horizonte"] + "|" + df["suavizada"]
                   + "|" + df["base_calculo"].astype(str))
    store = _comprime(
        df, ["serie"],
        {"m": "mediana", "s": "desvio_padrao", "lo": "minimo", "hi": "maximo",
         "n": "numero_respondentes"},
        wk_idx,
    )
    print(f"  movel          {len(store):5d} series, "
          f"{sum(len(b['m']) for b in store.values()):7d} pontos semanais")
    return store


def _load_copom(conn, wk_idx: dict[str, int]) -> dict:
    """expc_focus_copom -> {reuniao|base: bloco}.

    A ORDEM cronologica das reunioes nao e alfabetica nem derivavel da data da
    pesquisa; o front-end reordena por (ano, numero) extraidos de "R<n>/<ano>".
    Nada aqui presume calendario do Copom -- so a numeracao publicada.
    """
    df = pd.read_sql(
        "SELECT date, reuniao, base_calculo, mediana, desvio_padrao, minimo, "
        "       maximo, numero_respondentes FROM expc_focus_copom",
        conn,
    )
    df["date"] = pd.to_datetime(df["date"])
    df["wk"] = _semana(df["date"])
    df = df.sort_values("date").groupby(
        ["reuniao", "base_calculo", "wk"], as_index=False
    ).tail(1)
    df["serie"] = df["reuniao"] + "|" + df["base_calculo"].astype(str)
    store = _comprime(
        df, ["serie"],
        {"m": "mediana", "s": "desvio_padrao", "lo": "minimo", "hi": "maximo",
         "n": "numero_respondentes"},
        wk_idx,
    )
    print(f"  copom          {len(store):5d} series, "
          f"{sum(len(b['m']) for b in store.values()):7d} pontos semanais")
    return store


def _load_cobertura(conn) -> list[dict]:
    """Tabela do Apendice: primeira/ultima data e volume de cada serie, medidos
    no banco na hora da geracao -- nao copiados de documentacao, que envelhece."""
    linhas = []
    per = pd.read_sql(
        "SELECT periodicidade, indicador, detalhe, MIN(date) d0, MAX(date) d1, "
        "       COUNT(*) n, COUNT(DISTINCT data_referencia) nref "
        "FROM expc_focus_periodo GROUP BY 1, 2, 3", conn)
    for r in per.itertuples():
        linhas.append({
            "tabela": "expc_focus_periodo", "recorte": r.periodicidade,
            "serie": r.indicador + (f" — {r.detalhe}" if r.detalhe else ""),
            "d0": str(r.d0), "d1": str(r.d1), "n": int(r.n), "nref": int(r.nref),
        })
    mov = pd.read_sql(
        "SELECT indicador, horizonte, MIN(date) d0, MAX(date) d1, COUNT(*) n "
        "FROM expc_focus GROUP BY 1, 2", conn)
    for r in mov.itertuples():
        linhas.append({
            "tabela": "expc_focus", "recorte": r.horizonte, "serie": r.indicador,
            "d0": str(r.d0), "d1": str(r.d1), "n": int(r.n), "nref": None,
        })
    cop = pd.read_sql(
        "SELECT base_calculo, MIN(date) d0, MAX(date) d1, COUNT(*) n, "
        "       COUNT(DISTINCT reuniao) nref FROM expc_focus_copom GROUP BY 1", conn)
    for r in cop.itertuples():
        linhas.append({
            "tabela": "expc_focus_copom", "recorte": f"base {r.base_calculo}",
            "serie": "Selic por reunião", "d0": str(r.d0), "d1": str(r.d1),
            "n": int(r.n), "nref": int(r.nref),
        })
    return linhas


def _load_meta(conn, grade: list[str]) -> dict:
    """Cabecalho: ultima data de pesquisa de cada tabela e volume total."""
    m = {}
    for t in ("expc_focus", "expc_focus_copom", "expc_focus_periodo"):
        r = pd.read_sql(f"SELECT MAX(date) d, COUNT(*) n FROM {t}", conn).iloc[0]
        m[t] = {"ultima": str(r.d), "linhas": int(r.n)}
    m["grade"] = grade
    m["ordemFamilia"] = _ORDEM_FAMILIA
    m["mensalRefMin"] = _MENSAL_REF_MIN
    return m


# ── entry point ──────────────────────────────────────────────────────────────
def run(output: str = "reports/brasil/Expectations.html") -> None:
    conn = _conn()
    data: dict = {"generated_at": datetime.now().strftime("%d/%m/%Y %H:%M")}
    try:
        grade, wk_idx = _monta_grade(conn)
        print(f"  grade          {len(grade)} semanas, {grade[0]} -> {grade[-1]}")

        try:
            stores, indice = _load_periodo(conn, wk_idx)
            data["periodo"], data["indice"] = stores, indice
        except Exception as exc:
            print(f"  periodo        FALHOU -- {exc}")
            data["periodo"], data["indice"] = {}, {}

        for grupo, loader in (("movel", _load_movel), ("copom", _load_copom)):
            try:
                data[grupo] = loader(conn, wk_idx)
            except Exception as exc:
                print(f"  {grupo:14s} FALHOU -- {exc}")
                data[grupo] = {}

        try:
            data["cobertura"] = _load_cobertura(conn)
            print(f"  cobertura      {len(data['cobertura'])} linhas")
        except Exception as exc:
            print(f"  cobertura      FALHOU -- {exc}")
            data["cobertura"] = []

        data["meta"] = _load_meta(conn, grade)
    finally:
        conn.close()

    tam = len(json.dumps(data, ensure_ascii=False, default=str))
    print(f"  payload        {tam / 1e6:.1f} MB de JSON")
    out = render_report(_TEMPLATE, data, output)
    print(f"Relatorio salvo: {out}")


if __name__ == "__main__":
    run()
