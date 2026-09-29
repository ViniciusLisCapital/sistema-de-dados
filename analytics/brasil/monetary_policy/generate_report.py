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
                 contra o que ele faz. Uma linha por reuniao, nao uma grade de calendario.
                 Mais, de projecao_rpm.py, o caminho trimestral inteiro de cada edicao do RPM
                 e o IPCA realizado ao lado (2026-09-25)
  Condicionais   condicionais.py: os condicionantes da projecao do Copom edicao a edicao --
                 o hiato como cada RPM o publicou (pm_hiato_produto_vintages) e o caminho da
                 Selic que a Focus trazia antes de cada reuniao (expc_focus_copom). Nome da
                 aba provisorio (2026-09-24)
  Expectativas   expectativas_juros.py: o caminho da Selic que a Focus espera e o que a curva
  de Juros       DI precifica, reuniao a reuniao, semana a semana (expc_focus_copom e
                 br_di_grade). Veio da aba Curva do Copom do relatorio de Expectativas, que
                 saiu de la no mesmo dia (2026-09-24)

As abas Cenarios, Decomposicao, Taxa Neutra e Hiato do Produto foram REMOVIDAS em
2026-08-25, a aba Modelo BC - Agregado -- o motor portado para JS -- em 2026-09-22 e o
Apendice, que descrevia o modelo agregado, em 2026-09-24: as seis a pedido do usuario,
com os loaders delas. Nada deste relatorio le mais os artefatos `modelo_*` de `data/`;
`modelo_agregado.py` e `modelo_painel.py` continuam no diretorio porque a aba Condicoes e
o Modelo Estrutural importam funcoes deles, e `antecipa_copom.backtest(modelo=True)`
ainda refaz a comparacao que justificou trocar o modelo pelo delta da Focus.

O unico calculo proprio e a previsao da proxima projecao do BC, gravada por
`antecipa_copom.salvar()` e LIDA aqui (o botao Regerar refaz quando esta atras dos dados):

    uv run python -c "from analytics.brasil.monetary_policy.antecipa_copom import salvar; salvar()"
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
    # Os campos do modelo agregado (`delta_modelo`, `nivel_modelo`, `rr`, `h0`...) so existem
    # num JSON gravado com `salvar(modelo=True)`, que e pesquisa e nao producao. A aba nao le
    # nenhum deles, entao nao entram no payload em nenhum dos dois casos.
    for k in ("delta_modelo", "previsto", "previsto_publicado", "nivel_modelo", "rr",
              "h0", "h0_vintage", "piA_4t", "selic_fim", "t0", "parametros",
              "cambio_condicionado", "modelo"):
        prev.pop(k, None)
    ano = int(str(prev["periodo"])[:4])
    mt = meta_ano.get(ano, meta_ano.get(ultimo_ano_meta))
    prev["meta"] = round(mt, 4) if mt is not None else None
    prev["meta_estendida"] = int(ultimo_ano_meta is not None and ano > ultimo_ano_meta)
    # O modelo saiu da aba em 2026-09-24, a pedido do usuario: sobrou o delta da Focus, e o
    # que o modelo produzia (`delta_modelo`, `previsto`, `erro`, `nivel_modelo`, `rr`, `t0`)
    # nao alimenta mais nada na tela. `erro_ingenuo` saiu junto por outro motivo: ele e
    # exatamente `-revisao`, coluna que fica -- carregar as duas era carregar a mesma coisa
    # duas vezes. O CSV segue com todas; quem le e este recorte.
    # `anc_doc` e `anc_dias` nao sao lidos pela tela: existem para o teste poder afirmar que
    # a expansao ancora sempre no relatorio e a revisao no comunicado anterior.
    bt = pd.read_csv(csv)
    cols = ["nro", "reuniao", "alvo", "tipo", "ancora", "anc_doc", "anc_dias", "real",
            "revisao", "delta_focus", "erro_focus"]
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
    # O caminho trimestral inteiro de cada edicao do RPM, para as duas secoes de baixo da aba.
    # try proprio: se falhar, as duas somem e o resto da aba continua de pe.
    try:
        from analytics.brasil.monetary_policy import projecao_rpm
        out["caminhos"] = projecao_rpm.montar()
    except Exception as exc:                                      # noqa: BLE001
        print(f"  projecoes  caminhos do RPM FALHOU -- {type(exc).__name__}: {exc}")
    return out


def _load_condicionais() -> dict:
    """Aba Acompanhamento Condicionais -> `condicionais.hiato()` e `condicionais.selic()`.

    O hiato e uma entrada por edicao do RPM; o caminho da Selic, uma por reuniao do Copom,
    mais o da pesquisa mais recente e a Selic efetiva. As escolhas que decidem cada um (so a
    estimativa central do hiato; a pesquisa da sexta-feira anterior a decisao; a data estimada
    de uma reuniao que o BC ainda nao marcou) estao no docstring do modulo. Nada e calculado
    aqui nem la: leitura em tempo real e revisoes saem no JS, dos mesmos arrays
    que os graficos desenham, para os dois nao poderem divergir.

    Cada condicionante no seu try/except: um que falhe degrada so o grafico dele.
    """
    from analytics.brasil.monetary_policy import condicionais as cn
    out = {}
    for chave, fn in (("hiato", cn.hiato), ("selic", cn.selic)):
        try:
            out[chave] = fn()
        except Exception as exc:                                  # noqa: BLE001
            print(f"  condicionais  {chave} FALHOU -- {type(exc).__name__}: {exc}")
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
        cm = pj.get("caminhos") or {}
        if cm.get("edicoes"):
            E = cm["edicoes"]
            print(f"  projecoes  caminhos do RPM: {len(E)} edicoes ({E[0]['vintage'][:7]} -> "
                  f"{E[-1]['vintage'][:7]}), "
                  + ", ".join(f"{i} em {sum(1 for e in E if i in e['series'])}"
                              for i in cm["indices"])
                  + (f" | sem o cenario de juros esperado: {', '.join(cm['sem_cenario'])}"
                     if cm.get("sem_cenario") else ""))
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
                  f"{pv['tipo']}: ancora {pv['ancora']:.1f} -> "
                  f"{pv['previsto_focus_publicado']}"
                  + (f" | MAE {mae:.3f} em {len(pj['backtest'])} reunioes"
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
        data["condicionais"] = _load_condicionais()
        ed = (data["condicionais"].get("hiato") or {}).get("edicoes") or []
        if ed:
            nb = sum(1 for e in ed if e["regime"] == "banda")
            print(f"  condicionais  hiato: {len(ed)} edicoes ({ed[0]['vintage'][:7]} -> "
                  f"{ed[-1]['vintage'][:7]}), {nb} com um modelo e banda, "
                  f"{len(ed) - nb} com conjunto de modelos")
        sl = data["condicionais"].get("selic") or {}
        cs = sl.get("caminhos") or []
        if cs:
            hj = sl.get("hoje")
            print(f"  condicionais  selic: {len(cs)} caminhos ({cs[0]['reuniao']} -> "
                  f"{cs[-1]['reuniao']})"
                  + (f" + o de hoje, Focus de {hj['pesquisa']} para a {hj['nro']}a"
                     + (" (provisorio)" if hj.get("provisorio") else "") if hj else ""))
            if sl.get("sem_pesquisa"):
                print(f"             AVISO  {len(sl['sem_pesquisa'])} reuniao(oes) sem pesquisa "
                      f"Focus na semana do corte: {sl['sem_pesquisa']}")
    except Exception as exc:
        print(f"  condicionais  FALHOU -- {exc}")
        data["condicionais"] = {}

    try:
        from analytics.brasil.monetary_policy import expectativas_juros as ej
        data["expectativas"] = ej.montar()
        ex = data["expectativas"]
        for nome in ("focus", "di"):
            s = ex.get(nome)
            if s:
                print(f"  expectativas  {nome:5s} {len(s['datas'])} semanas "
                      f"({s['datas'][0]} -> {s['datas'][-1]}), {len(s['por_reuniao'])} reunioes")
    except Exception as exc:
        print(f"  expectativas  FALHOU -- {exc}")
        data["expectativas"] = {}

    out = render_report(_TEMPLATE, data, output)
    print(f"Relatorio salvo: {out}")


if __name__ == "__main__":
    run()
