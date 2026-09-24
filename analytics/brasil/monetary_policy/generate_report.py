"""
Gerador do Panorama de Politica Monetaria em HTML.

Abas de dado, e a fonte de cada uma:

  Condicoes      condicoes_copom.montar(): uma linha por variavel, uma coluna por
                 reuniao -- as 8 ultimas ja decididas mais a proxima --, com o que o
                 Comite tinha na mesa em cada uma, mais a agenda ate a proxima. O
                 corte e um DATETIME (o comunicado sai ~18:30 do dia 2) e a data de
                 divulgacao de cada serie mensal vem do domain/release_calendar/.
                 A primeira linha e a projecao do proprio BC no horizonte relevante,
                 do comunicado -- a mesma fonte da aba Projecoes, so que lida reuniao
                 a reuniao
  Projecoes      pm_copom_projecoes x pm_copom_reuniao: a projecao do BC para o horizonte
                 relevante contra o passo de Selic da MESMA reuniao -- o que o Comite projeta
                 contra o que ele faz. Uma linha por reuniao, nao uma grade de calendario
  Apendice       descricao do modelo (equacoes com os coeficientes estimados) + a tabela
                 de validacao contra a Tabela 1 do boxe

As abas Cenarios, Decomposicao, Taxa Neutra e Hiato do Produto foram REMOVIDAS em
2026-08-25 e a aba Modelo BC - Agregado -- o motor portado para JS -- em 2026-09-22, as
cinco a pedido do usuario, com os loaders delas. Os artefatos continuam sendo gravados
por `modelo_agregado.rodar()` em `data/`, e o Apendice segue lendo os dele: parametros,
validacao contra a Tabela 1 do boxe e o IRF.

Rodar o modelo NAO faz parte da geracao do relatorio de proposito: a estimacao leva
minutos e depende de MySQL, do IPEADATA e do anexo do RPM, enquanto gerar o HTML tem
de ser rapido e reproduzivel. Pipeline completo:

    uv run python analytics/brasil/monetary_policy/modelo_painel.py     # paineis
    uv run python analytics/brasil/monetary_policy/modelo_agregado.py   # estima + grava
    uv run python analytics/brasil/monetary_policy/generate_report.py   # HTML

Mesmo padrao /*REPORT_DATA*/ dos demais relatorios, via
analytics.report_structure.builder.render_report(), que tambem preenche /*THEME_CSS*/
e /*Y_AUTOFIT_JS*/. Output autocontido.

## Como adicionar uma aba

1. Escreva o `_load_<aba>()` aqui devolvendo `{chave: {"dates": [...], "values": [...]}}`
   -- o shape que `ser(grupo, chave)` espera no template. Chaves compostas usam `__`.
2. Ligue em `run()` com try/except PROPRIO: artefato faltando degrada so a aba dele em
   vez de derrubar o relatorio (convencao do projeto).
3. Preencha o `render<Aba>()` em report.html e apague o `.stub-note` do painel.
"""

import json
from datetime import datetime
from pathlib import Path

import pandas as pd

from analytics.report_structure.builder import render_report
from connectors.mysql import MySQLDataRequester

_HERE = Path(__file__).parent
_TEMPLATE = _HERE / "report.html"
_DATA = _HERE / "data"
_DATABASE = "macro_brasil"


# ── utilitarios ──────────────────────────────────────────────────────────────
def _ser(s: pd.Series) -> dict:
    """Serie com PeriodIndex trimestral -> {"dates": ISO, "values": [...]}."""
    s = s.dropna() if s.isna().all() else s
    idx = s.index
    if isinstance(idx, pd.PeriodIndex):
        datas = idx.to_timestamp().strftime("%Y-%m-%d").tolist()
    else:
        datas = pd.to_datetime(idx).strftime("%Y-%m-%d").tolist()
    return {"dates": datas,
            "values": [None if pd.isna(v) else round(float(v), 4) for v in s.values]}


def _csv(nome: str) -> pd.DataFrame:
    df = pd.read_csv(_DATA / nome, index_col=0)
    try:
        df.index = pd.PeriodIndex(df.index, freq="Q")
    except Exception:
        pass
    return df


def _read_table(table: str) -> pd.DataFrame:
    req = MySQLDataRequester(_DATABASE, table)
    req.connect()
    df = req.request_data()
    req.close_connection()
    if "date" in df.columns:
        df["date"] = pd.to_datetime(df["date"])
    if "value" in df.columns:
        df["value"] = pd.to_numeric(df["value"])
    return df


def _raio_eq5() -> float | None:
    """Raio espectral do laco da eq. (5) no cenario default, lido do proprio cenario.

    Nao roda o modelo: `cenarios_padrao()` grava o raio junto com o cenario endogeno.
    """
    p = _DATA / "modelo_eq5_diag.json"
    if not p.exists():
        return None
    return json.loads(p.read_text()).get("raio")


# ── loaders por aba ─────────────────────────────────────────────────────────
def _load_antecipa(meta_ano: dict, ultimo_ano_meta) -> dict:
    """Previsao para a proxima reuniao + backtest, de `data/` (grava `antecipa_copom.salvar()`).

    Le artefato em vez de rodar o modelo: `antecipar()` roda o espaco de estados duas vezes e
    o backtest 34, o que nao cabe num generate_report. Devolve {} se os arquivos nao existirem
    -- a aba entao mostra so o historico publicado, sem a previsao.

    O `meta` do alvo vem do MESMO dicionario que as linhas publicadas usam, de proposito: na
    escala "desvio da meta" o ponto previsto tem de ser medido contra a mesma regua, incluindo
    a extensao da meta continua de 3% para alem do ultimo ano em `inflc_meta`.
    """
    csv = _HERE / "data" / "antecipa_backtest.csv"
    js = _HERE / "data" / "antecipa_previsao.json"
    if not (csv.exists() and js.exists()):
        return {}
    prev = json.loads(js.read_text(encoding="utf-8"))
    # O diagnostico que faltava: o `corte_usado` gravado no artefato contra o que as
    # fontes tem AGORA. Roda na geracao (o unico momento em que ha MySQL do lado) e vai
    # embutido, entao viaja com o arquivo -- quem receber o HTML por email ve o aviso
    # tambem. `salvar()` e o que conserta; regerar o relatorio, nao.
    try:
        from analytics.brasil.monetary_policy.antecipa_copom import frescor
        prev["frescor"] = frescor(prev.get("corte_usado"))
    except Exception as exc:                                     # noqa: BLE001
        prev["frescor"] = {"erro": f"{type(exc).__name__}: {exc}"}
    ano = int(str(prev["periodo"])[:4])
    mt = meta_ano.get(ano, meta_ano.get(ultimo_ano_meta))
    prev["meta"] = round(mt, 4) if mt is not None else None
    prev["meta_estendida"] = int(ultimo_ano_meta is not None and ano > ultimo_ano_meta)
    bt = pd.read_csv(csv)
    cols = ["nro", "reuniao", "alvo", "tipo", "ancora", "anc_doc", "anc_dias", "real",
            "revisao", "delta_modelo", "previsto", "erro", "erro_ingenuo", "delta_focus",
            "erro_focus", "nivel_modelo", "rr", "t0"]
    bt = bt[[c for c in cols if c in bt.columns]]
    return {"previsao": prev,
            "backtest": json.loads(bt.to_json(orient="records"))}


def _load_projecoes() -> dict:
    """Aba Projecoes do Copom: a projecao do horizonte relevante x o passo de Selic.

    Duas tabelas, uma linha por reuniao cada, casadas por `nro_reuniao`:
    `pm_copom_projecoes` (o que o Comite PROJETA) e `pm_copom_reuniao` (o que ele FEZ).

    Nao passa pelo loop de series por dois motivos: o payload e uma tabela de linhas, nao
    {chave: {dates, values}}, e a unidade de tempo e a REUNIAO, nao um periodo de
    calendario -- reuniao nao cai em grade regular (8 por ano, espacadas de ~45 dias).

    ## Tres filtros, e cada um responde a uma armadilha da fonte

    `horizonte_relevante = 1 & indice = 'ipca'` e o recorte obvio. Os outros dois nao:

    - **`documento`**. A mesma reuniao pode ter DUAS projecoes, uma do comunicado e uma
      do relatorio, com numeros diferentes -- o relatorio e vintage 7 a 28 dias posterior
      e, em 2017-2020, o comunicado publicava o cenario hibrido. Sem filtro a serie
      duplica a reuniao. Aqui o comunicado ganha quando existe: sai no DIA da decisao,
      entao e o conjunto de informacao exato; o relatorio completa o resto. Da 264a em
      diante os dois batem exatos (60 de 60), o que torna a preferencia inocua justo onde
      ela seria mais visivel.
    - **`regime`**. A palavra "horizonte relevante" cobre quatro conceitos diferentes na
      fonte, e so um deles e uma distancia fixa. Aqui a serie e sempre `hr_6_trimestres`
      (comunicado, 2024-07 em diante) ou `hr_aproximado` (relatorio, a regra dos seis
      trimestres aplicada ao caminho continuo que ele publica). Os regimes
      `ano_calendario` e `horizonte_suavizado` do comunicado pre-2024 ficam FORA de
      proposito: o ano calendario encurta de 12 para 4 trimestres a frente ao longo do
      proprio ano, o que poe um dente de serra na serie que nao e mudanca de projecao.
      Custa 14 reunioes de 2020-2024; o que se compra e uma unidade so.

    `cenario` classifica pelo CONDICIONAMENTO, nao pelo rotulo publicado -- "cenario de
    referencia" significava o OPOSTO em 2016-2017 (o rotulo original fica em
    `cenario_publicado`). Levantamento das duas fontes em
    domain/db/brasil/bcb/copom_comunicados.md e relatorio_politica_monetaria.md.

    ## A meta

    `inflc_meta` e ANUAL e termina em 2026; os trimestres projetados vao a 2028. A meta do
    ultimo ano publicado e estendida para frente, o que sob o regime de meta CONTINUA
    (3%, desde 2025) nao e extrapolacao -- e o proprio desenho da meta. Os anos estendidos
    vem marcados em `meta_estendida` e a aba os identifica.

    Escala da projecao: IPCA acumulado em 4 trimestres (%). Nao anualizar, nao acumular.
    """
    proj = _read_table("pm_copom_projecoes")
    reun = _read_table("pm_copom_reuniao")
    meta = _read_table("inflc_meta")

    m = proj[(proj["horizonte_relevante"] == 1) & (proj["indice"] == "ipca")
             & (((proj["documento"] == "relatorio") & (proj["regime"] == "hr_aproximado"))
                | ((proj["documento"] == "comunicado") & (proj["regime"] == "hr_6_trimestres")))]

    # meta por ano, estendida para frente com o ultimo valor publicado
    meta_ano = {int(r["date"].year): float(r["value"])
                for _, r in meta[meta["name"] == "meta_inflacao"].iterrows()}
    ultimo_ano_meta = max(meta_ano) if meta_ano else None

    reun = reun.sort_values("nro_reuniao").reset_index(drop=True)
    # `nro_prox` e o numero da reuniao SEGUINTE. Ele nao alimenta nada na tela; existe para
    # o teste poder afirmar que a linha n de fato antecede a n+1 na serie ordenada.
    reun["nro_prox"] = reun["nro_reuniao"].shift(-1)
    por_reuniao = reun.set_index("nro_reuniao")

    # So o cenario de juros esperado desde 2026-09-23, quando o seletor de cenario saiu da
    # aba: o de juros constantes e o mais proximo de uma funcao de reacao e e justamente o
    # que o BC parou de publicar -- a serie dele termina em jul/2024. Carregar dado que
    # nenhum controle le e divida; voltar a carregar e uma palavra nesta tupla.
    cenarios: dict[str, list] = {}
    sem_decisao: list[int] = []
    for cen in ("juros_esperado",):
        linhas = []
        sub = m[m["cenario"] == cen]
        # comunicado ganha do relatorio na mesma reuniao: sai no dia da decisao
        sub = sub.sort_values(["nro_reuniao", "documento"])  # 'comunicado' < 'relatorio'
        for nro, g in sub.groupby("nro_reuniao"):
            r = g.iloc[0]
            if nro not in por_reuniao.index:
                sem_decisao.append(int(nro))
                continue
            d = por_reuniao.loc[nro]
            ano = int(r["date"].year)
            mt = meta_ano.get(ano, meta_ano.get(ultimo_ano_meta))
            linhas.append({
                "nro": int(nro),
                "reuniao": r["vintage"].strftime("%Y-%m-%d") if hasattr(r["vintage"], "strftime")
                           else str(r["vintage"]),
                "decisao_date": pd.Timestamp(d["date"]).strftime("%Y-%m-%d"),
                "periodo": r["date"].strftime("%Y-%m-%d"),
                "qa": int(r["trimestres_a_frente"]),
                "proj": round(float(r["value"]), 4),
                "meta": round(mt, 4) if mt is not None else None,
                "meta_estendida": int(ultimo_ano_meta is not None and ano > ultimo_ano_meta),
                "doc": r["documento"],
                "bps": int(d["variacao_bps"]),
                "nro_prox": None if pd.isna(d["nro_prox"]) else int(d["nro_prox"]),
                "decisao": d["decisao"],
                "selic_ant": round(float(d["selic_anterior"]), 2),
                "selic_dec": round(float(d["selic_decidida"]), 2),
                "fora": int(d["alterada_fora_da_reuniao"]),
            })
        cenarios[cen] = sorted(linhas, key=lambda x: x["nro"])

    out = {"cenarios": cenarios,
           "sem_decisao": sorted(set(sem_decisao)),
           "ultimo_ano_meta": ultimo_ano_meta}
    out.update(_load_antecipa(meta_ano, ultimo_ano_meta))
    return out


def _load_condicoes() -> dict:
    """Aba Condicoes -> `condicoes_copom.montar()`, que le MySQL e o calendario.

    Nao passa pelo loop de series por dois motivos: o payload e uma tabela de linhas, nao
    {chave: {dates, values}}, e o corte de informacao e um DATETIME (o comunicado sai as
    ~18:30 do dia 2), coisa que o shape de serie nao carrega.

    O modulo faz o trabalho todo; aqui so se registra o que ele avisou. Um aviso nao
    derruba a aba: significa que a data de divulgacao ajustada de algum grupo nao bate com
    o que ja esta no banco, e a linha correspondente ja vem marcada como estimada.
    """
    from analytics.brasil.monetary_policy.condicoes_copom import montar
    return montar()


def _load_info() -> dict:
    """Metadados nao-serie: validacao dos parametros, do IRF e os numeros de cabecalho."""
    par = json.loads((_DATA / "modelo_params.json").read_text())
    val = pd.read_csv(_DATA / "modelo_validacao.csv")
    virf = json.loads((_DATA / "modelo_validacao_irf.json").read_text())
    S = _csv("modelo_estados.csv")
    P = _csv("modelo_painel_full.csv")

    hp = _read_table("pm_hiato_produto")
    hp["per"] = pd.PeriodIndex(hp["date"] + pd.DateOffset(months=2), freq="Q")
    cen = hp[hp["variavel"] == "central"].set_index("per")["value"]
    Se = _csv("modelo_estados_est.csv")
    j = pd.DataFrame({"a": Se["h"], "b": cen}).dropna()

    ult = S["h"].dropna().index.max()
    return {
        "params": {k: round(v, 6) for k, v in par.items() if not k.startswith("_")},
        "logL": round(par["_logL"], 3), "logL_bcb": round(par["_logL_bcb"], 3),
        "sigma_rr": round(par["_sigma_rr"], 4),
        "validacao": json.loads(val.to_json(orient="records")),
        "n_dentro": int(val["dentro"].sum()), "n_total": int(len(val)),
        "irf": {k: (round(v, 4) if isinstance(v, float) else v) for k, v in virf.items()},
        "eq5": dict(par.get("_eq5") or {},
                    raio=_raio_eq5(), phi_bcb=dict(f1=0.75, f2=0.11, f3=0.021)),
        "hiato_corr": round(float(j["a"].corr(j["b"])), 4),
        "hiato_n": int(len(j)),
        "ultimo_tri": str(ult),
        "selic_hoje": round(float(P["selic"].dropna().iloc[-1]), 2),
        "h_hoje": round(float(S["h"].dropna().iloc[-1]), 2),
        "r_is_hoje": round(float(S["rr_IS_total"].dropna().iloc[-1]), 2),
        "r_tay_hoje": round(float(S["rr_TAY_total"].dropna().iloc[-1]), 2),
        "r_hat_hoje": round(float(S["r_hat"].dropna().iloc[-1]), 2),
        "neutra_pub_ult": round(float(_csv("modelo_neutra_pub.csv").median(axis=1).dropna().iloc[-1]), 2),
        "neutra_pub_tri": str(_csv("modelo_neutra_pub.csv").median(axis=1).dropna().index.max()),
    }


# ── entry point ──────────────────────────────────────────────────────────────
def run(output: str = "reports/brasil/Monetary Policy.html") -> None:
    print("Carregando dados...")
    data = {"generated_at": datetime.now().strftime("%d/%m/%Y %H:%M")}

    # O payload desta aba e uma tabela de linhas indexada por REUNIAO, nao
    # {chave: {dates, values}} numa grade de calendario -- por isso ela nao passa por _ser().
    try:
        data["projecoes"] = _load_projecoes()
        pj = data["projecoes"]
        for cen, linhas in pj["cenarios"].items():
            if not linhas:
                print(f"  projecoes  {cen}: vazio")
                continue
            docs = {}
            for x in linhas:
                docs[x["doc"]] = docs.get(x["doc"], 0) + 1
            print(f"  projecoes  {cen}: {len(linhas)} reunioes "
                  f"({linhas[0]['decisao_date']} -> {linhas[-1]['decisao_date']}), "
                  + " + ".join(f"{n} do {d}" for d, n in sorted(docs.items())))
        if pj["sem_decisao"]:
            print(f"             AVISO  {len(pj['sem_decisao'])} reuniao(oes) com projecao e sem "
                  f"linha em pm_copom_reuniao: {pj['sem_decisao']}")
        est = sum(x["meta_estendida"] for x in pj["cenarios"]["juros_esperado"])
        if est:
            print(f"             {est} reunioes projetam periodo depois de "
                  f"{pj['ultimo_ano_meta']}, o ultimo ano com meta publicada -- a meta continua "
                  "de 3% e estendida para frente e marcada na aba")
        if pj.get("previsao"):
            pv = pj["previsao"]
            mae = None
            if pj.get("backtest"):
                errs = [abs(r["erro_focus"]) for r in pj["backtest"]
                        if r.get("erro_focus") is not None]
                mae = sum(errs) / len(errs) if errs else None
            print(f"  previsao   {pv['nro']}a ({pv['data_reuniao']}), horizonte {pv['alvo']}, "
                  f"{pv['tipo']}: ancora {pv['ancora']:.1f} -> focus "
                  f"{pv['previsto_focus_publicado']} / modelo {pv['previsto_publicado']}"
                  + (f" | MAE focus {mae:.3f} em {len(pj['backtest'])} reunioes"
                     if mae is not None else ""))
            # O aviso que importa nao e "o corte e anterior a reuniao" (isso e normal e
            # so vai deixar de ser no dia dela), e "o corte e anterior ao que o banco JA
            # tem": ai a previsao embutida esta velha e regerar o relatorio nao conserta,
            # porque o gerador so le o artefato.
            fr = pv.get("frescor") or {}
            if fr.get("atrasado"):
                print(f"             AVISO  previsao calculada com dado ate "
                      f"{fr['corte']}, mas {fr['fonte_ref']} ja tem {fr['fonte_max']} "
                      f"({fr['dias']}d): rode antecipa_copom.salvar() e regere")
            elif pv["corte_usado"] < pv["data_reuniao"]:
                print(f"             corte de informacao {pv['corte_usado']}, em dia com "
                      f"o banco; ate {pv['data_reuniao']} entram mais boletins")
        else:
            print("  previsao   ausente -- rode antecipa_copom.salvar() para gerar "
                  "data/antecipa_{backtest.csv,previsao.json}")
    except Exception as exc:
        print(f"  projecoes  FALHOU -- {exc}")
        data["projecoes"] = {}

    try:
        data["condicoes"] = _load_condicoes()
        c = data["condicoes"]
        if c.get("erro"):
            print(f"  condicoes  {c['erro']}")
        else:
            cols = c["reunioes"]
            linhas = [l for b in c["blocos"] for l in b["linhas"]]
            falhas = [l["key"] for l in linhas if l.get("erro")]
            celulas = [x for l in linhas for x in (l.get("celulas") or [])]
            novas = sum(1 for x in celulas if x["novo"])
            estim = sum(1 for x in celulas if not x["exata"])
            prox = cols[-1]
            print(f"  condicoes  {len(linhas)} variaveis x {len(cols)} reunioes "
                  f"({cols[0]['label']} -> {cols[-1]['label']}) | {novas}/{len(celulas)} "
                  f"celulas com dado novo, {estim} com data estimada | proxima "
                  f"{prox['date']} em {prox['dias']}d | {len(c['agenda'])} divulgacoes ate la")
            if falhas:
                print(f"             AVISO  {len(falhas)} linha(s) sem serie: "
                      + ", ".join(falhas))
            # So os avisos de celula AMBIGUA chegam aqui -- os demais ja viram marca na
            # tela. Imprimir todos afogaria o log num recorte de 9 reunioes.
            for a in c.get("avisos", [])[:8]:
                print(f"             AVISO  {a}")
            if len(c.get("avisos", [])) > 8:
                print(f"             ... e mais {len(c['avisos']) - 8} aviso(s)")
    except Exception as exc:
        print(f"  condicoes  FALHOU -- {exc}")
        data["condicoes"] = {}

    try:
        data["info"] = _load_info()
        i = data["info"]
        print(f"  info       {i['n_dentro']}/{i['n_total']} parametros no IC 90% do BC | "
              f"corr do hiato {i['hiato_corr']} | r* {i['r_is_hoje']}%")
    except Exception as exc:
        print(f"  info       FALHOU -- {exc}")
        data["info"] = {}

    out = render_report(_TEMPLATE, data, output)
    print(f"Relatorio salvo: {out}")


if __name__ == "__main__":
    run()
