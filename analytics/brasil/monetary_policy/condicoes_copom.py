"""
Condicoes economicas entre duas reunioes do Copom: o que o Comite viu na ultima decisao
contra o que ja esta na mesa para a proxima.

A pergunta que a aba responde nao e "onde estamos", e "o que MUDOU desde a ultima
decisao". Entre duas reunioes passam ~45 dias, e nesse intervalo saem 1 ou 2 IPCAs, 1
IPCA-15, 6 Boletins Focus e ~30 pregoes -- e sao esses dados novos, nao o nivel das
variaveis, que podem mover a decisao seguinte.

Nada e reconstruido para tras: a aba compara SEMPRE a ultima reuniao ja realizada com o
conjunto de informacao de hoje, entao ela se renova sozinha quando uma reuniao passa.

## A regra de corte, que e o coracao do modulo

O comunicado sai no FIM DO DIA 2 da reuniao (~18:30 BRT), entao o corte e
`datetime(dia_2, 18:30)` -- tudo divulgado ate ali PODE ter sido usado. Aplicar isso
exige separar dois tipos de serie, porque a data que indexa cada uma significa coisas
diferentes:

- **serie de mercado / Focus** -- o indice E a data em que o dado existiu (pregao,
  pesquisa). Corte direto: ultimo ponto com `data <= corte`. Exato, sem regra nenhuma.
- **serie de referencia mensal** -- o indice e o MES A QUE O DADO SE REFERE, e ele so e
  publicado semanas depois. O IPCA de julho existe no banco com data 2026-07-01 e foi
  divulgado em ~13/08: na reuniao de 05/08 o Copom ainda estava com o de junho. Ler o
  banco por `date <= corte` daria julho e seria um anacronismo silencioso -- o erro que
  este modulo existe para nao cometer.

Para o segundo tipo a data de divulgacao vem de `domain/release_calendar/calendar_2026.yaml`,
que ja e a config de QUANDO cada dado sai. Onde o calendario tem a entrada exata do
periodo (`reference_period`), ela e usada; onde nao tem -- o arquivo comeca em 2026-08-13
e a ultima reuniao foi antes disso --, a data e ESTIMADA pela regra do proprio grupo,
ajustada das entradas que ele tem: mediana do defasamento em meses e mediana do indice
de dia util dentro do mes de divulgacao. Cada linha carrega `exata`, e o relatorio marca
as estimadas, porque medido e estimado nao se misturam em silencio neste projeto.

O horario tambem entra, e nao e detalhe: o IC-Br de julho saiu as 14:30 de 05/08/2026, o
mesmo dia da 280a reuniao -- entrou no conjunto de informacao por quatro horas.

## Teto do banco

Para a coluna "hoje" a referencia e `min(o que o calendario diz que ja saiu, o que existe
no banco)`. O calendario descreve a divulgacao, o banco descreve o que temos: quando os
dois divergem o dado saiu e o ETL ainda nao rodou, e a linha e marcada `pendente` em vez
de fingir um valor que nao esta carregado.

## Cor

`z = sinal x (valor_hoje - valor_na_reuniao) / sigma`, com sigma = escala tipica (10
anos, robusta) da variacao da MESMA serie sobre o MESMO numero de observacoes que
separou as duas leituras. Sem isso 0,2 p.p. no IPCA e 0,2 p.p. no Brent teriam a mesma
cor. Num NIVEL de preco a diferenca em pontos nao e a noticia -- o cambio entra em
variacao PERCENTUAL (`modo='pct'`), porque o repasse e proporcional e 10 centavos a 3,00
nao sao a mesma coisa que 10 centavos a 6,00. `sinal` e +1 quando subir e hawkish, -1 quando subir e dovish (juro real ex-ante
alto ja e politica apertada, logo argumento para cortar) e 0 quando a variavel nao tem
leitura hawk/dove -- as expectativas de Selic da Focus sao REACAO do mercado a decisao,
nao condicao que a antecede, e colori-las de vermelho seria circular.

## Dessazonalizacao

As metricas de margem (nucleos, EX3, desocupacao e saldo do CAGED) sao dessazonalizadas
por STL com FATORES CONGELADOS ate dezembro do ano anterior -- mesma convencao de
`analytics/brasil/inflation/fetch_bcb.py`. Congelar importa aqui mais do que la: com
fatores reestimados a cada rodada o valor "na reuniao passada" mudaria junto com o de
hoje, e a diferenca entre as duas colunas deixaria de ser so dado novo. O IBC-Br e a
excecao: usa a serie que o proprio BCB ja dessazonaliza.
"""

from __future__ import annotations

import datetime as dt
import pathlib

import numpy as np
import pandas as pd
import yaml
from statsmodels.tsa.seasonal import STL

from analytics.brasil.monetary_policy.modelo_painel import (
    focus_selic_12m_diario,
    q,
    serie,
)

_RAIZ = pathlib.Path(__file__).resolve().parents[3]
_CALENDARIO = _RAIZ / "domain" / "release_calendar" / "calendar_2026.yaml"

# Comunicado no fim do dia 2. O calendario documenta ~18:30 BRT na nota do grupo bcb_copom.
HORA_DECISAO = dt.time(18, 30)
# Sem `time` na entrada nem `release_time` no grupo, assume manha -- e o horario de todo
# release macro brasileiro relevante aqui (IBGE 09:00, BCB 08:30/09:00). So muda o
# resultado se a divulgacao cair no proprio dia da reuniao.
HORA_PADRAO = dt.time(9, 0)
ANOS_SIGMA = 10
# Inicio da amostra do ajuste sazonal -- ver `_sa()`. 2000 e o mesmo corte de
# analytics/brasil/inflation/fetch_bcb.py, ja com o regime de metas rodando.
INICIO_SA = "2000-01"

# Os 5 nucleos que o BCB acompanha no RPM. EX3 e o EX03 da tabela; MS e
# `medias_aparadas` (com suavizacao), nao a versao sem.
NUCLEOS = ("ipca_nucleo_ex0", "ipca_nucleo_ex03", "ipca_nucleo_medias_aparadas",
           "ipca_nucleo_dp", "ipca_nucleo_p55")


# ── calendario de divulgacao ─────────────────────────────────────────────────
_CAL: dict | None = None


def calendario() -> dict:
    global _CAL
    if _CAL is None:
        _CAL = yaml.safe_load(_CALENDARIO.read_text(encoding="utf-8"))
    return _CAL


def grupos() -> dict:
    return {g["group"]: g for g in calendario().get("groups", [])}


def _data(v) -> dt.date:
    return v if isinstance(v, dt.date) else dt.date.fromisoformat(str(v))


def _hora(entrada: dict | None, grupo: dict) -> dt.time:
    t = (entrada or {}).get("time") or grupo.get("release_time")
    return dt.time.fromisoformat(str(t)) if t else HORA_PADRAO


def _quando(entrada: dict, grupo: dict) -> dt.datetime:
    return dt.datetime.combine(_data(entrada["date"]), _hora(entrada, grupo))


def _ref(rp) -> pd.Period | None:
    """'2026-08' -> Period. Qualquer outra coisa ('281a reuniao') -> None."""
    if not rp:
        return None
    try:
        return pd.Period(str(rp), freq="M")
    except Exception:
        return None


def _dia_util(d: dt.date) -> int:
    """Indice do dia util de `d` dentro do proprio mes (1 = primeiro dia util)."""
    return int(np.busday_count(d.replace(day=1), d)) + 1


def _data_dia_util(ano: int, mes: int, k: int) -> dt.date:
    """k-esimo dia util do mes. Feriados nacionais nao entram -- ver `regra()`."""
    ini = np.datetime64(dt.date(ano, mes, 1), "D")
    return np.busday_offset(ini, k - 1, roll="forward").astype(dt.date)


def regra(grupo: dict) -> tuple[int, int, int] | None:
    """(defasagem em meses, indice do dia util, erro maximo em dias) do proprio grupo.

    Mediana em vez de media porque uma antecipacao pontual (o IPCA de setembro/2026 sai
    no 7o dia util contra 9 nas outras tres entradas) nao deve deslocar a regra.

    O terceiro elemento e o que impede a regra de se vender como exata: e o maior desvio
    entre o que ela preve e o que o calendario publica, medido nas proprias entradas do
    grupo. Ele nao e uniforme -- o IPCA e o IPCA-15 sao ancorados no mes e fecham em <=4
    dias, enquanto o IC-Br sai numa cadencia de 4-5 semanas ancorada em QUARTA-FEIRA (a
    nota do grupo no calendario diz isso), que nenhuma regra mensal reproduz: ali o erro
    chega a 5 dias. Nao vale caso especial -- o IC-Br tem entrada exata no calendario
    desde 2026-05, entao a estimativa nunca e exercida no recorte da aba -- mas vale
    CARREGAR o erro, para `montar()` poder avisar quando ele for grande o bastante para
    mudar a resposta.

    Feriados nacionais ficam de fora do contador de dia util de proposito: entram
    igualmente no ajuste e na aplicacao, entao se cancelam enquanto nao cair um feriado
    entre o dia ajustado e o dia real -- e quando cai, ja esta contabilizado no erro.
    """
    defas, dias, pares = [], [], []
    for e in grupo.get("entries", []):
        ref = _ref(e.get("reference_period"))
        if ref is None:
            continue
        d = _data(e["date"])
        defas.append((d.year * 12 + d.month) - (ref.year * 12 + ref.month))
        dias.append(_dia_util(d))
        pares.append((ref, d))
    if not defas:
        return None
    md, mdia = int(np.median(defas)), int(round(float(np.median(dias))))
    erro = 0
    for ref, real in pares:
        m = ref + md
        erro = max(erro, abs((_data_dia_util(m.year, m.month, mdia) - real).days))
    return md, mdia, erro


def divulgacao(grupo: dict, ref: pd.Period) -> tuple[dt.datetime | None, bool]:
    """Quando o periodo `ref` foi (ou sera) divulgado. bool = veio do calendario."""
    for e in grupo.get("entries", []):
        if _ref(e.get("reference_period")) == ref:
            return _quando(e, grupo), True
    r = regra(grupo)
    if r is None:
        return None, False
    defas, dia, _ = r
    m = ref + defas
    return dt.datetime.combine(_data_dia_util(m.year, m.month, dia),
                               _hora(None, grupo)), False


def ref_divulgado(grupo: dict, corte: dt.datetime,
                  refs) -> tuple[pd.Period | None, bool]:
    """Ultimo periodo de `refs` ja divulgado em `corte`."""
    for ref in reversed(list(refs)):
        quando, exata = divulgacao(grupo, ref)
        if quando is not None and quando <= corte:
            return ref, exata
    return None, False


# ── reunioes do Copom ────────────────────────────────────────────────────────
def reunioes(agora: dt.datetime | None = None) -> tuple[dict | None, dict | None]:
    """(ultima ja decidida, proxima). `date` no calendario e o DIA 2, o da decisao.

    A separacao e pelo CORTE, nao pela data: no dia 1 -- e no proprio dia 2 antes das
    18:30 -- a decisao ainda nao saiu, e a reuniao em curso e a `proxima`. Comparar por
    data faria a aba comparar a reuniao consigo mesma no dia em que ela acontece.
    """
    agora = agora or dt.datetime.now()
    g = grupos().get("bcb_copom")
    if not g:
        return None, None
    ant = prox = None
    for e in sorted(g.get("entries", []), key=lambda x: _data(x["date"])):
        d = _data(e["date"])
        r = {"date": d,
             "date_start": _data(e["date_start"]) if e.get("date_start") else None,
             "corte": dt.datetime.combine(d, HORA_DECISAO),
             "rotulo": e.get("reference_period")}
        if r["corte"] <= agora:
            ant = r
        elif prox is None:
            prox = r
    return ant, prox


def numero_reuniao(data: dt.date) -> int | None:
    """Numero absoluto da reuniao, de `pm_copom_projecoes` (vintage = dia da decisao).

    So casamento exato: `pm_copom_projecoes` carrega da 206a reuniao em diante e toda
    reuniao recente publica projecao, entao a ultima ja realizada sempre esta la. Contar
    reunioes para preencher um buraco seria adivinhar um numero oficial.
    """
    d = q("macro_brasil", "SELECT DISTINCT vintage, nro_reuniao FROM pm_copom_projecoes "
                          "WHERE vintage = '%s'" % data.isoformat())
    return int(d["nro_reuniao"].iloc[0]) if len(d) else None


def rotulo_focus(hoje_focus: pd.Timestamp) -> str | None:
    """Rotulo da PROXIMA reuniao na convencao do `expc_focus_copom` ('R6/2026').

    Data-driven em vez de contado do calendario: a Focus para de pesquisar uma reuniao no
    dia em que ela acontece, entao a proxima e a menor (ano, R) cuja serie ainda chega a
    ultima data de pesquisa. Nao depende de saber quantas reunioes ja houve no ano.
    """
    d = q("macro_brasil", "SELECT reuniao, MAX(date) mx FROM expc_focus_copom "
                          "WHERE base_calculo=0 GROUP BY reuniao")
    if d.empty:
        return None
    d["mx"] = pd.to_datetime(d["mx"])
    viva = d[d["mx"] >= hoje_focus]
    if viva.empty:
        return None

    def chave(r):
        n, ano = r.split("/")
        return (int(ano), int(n[1:]))

    return sorted(viva["reuniao"], key=chave)[0]


# ── series ───────────────────────────────────────────────────────────────────
def _mensal(nome: str, tabela: str = "inflc_agregados", db: str = "macro_brasil",
            filtro: str | None = None) -> pd.Series:
    """Serie mensal com indice de PERIODO -- e o indice que `divulgacao()` entende.

    `filtro` existe para as tabelas cuja chave tem mais de uma dimensao alem do nome
    (`mt_pnad` e (date, name, region)): sem ele o SELECT traria uma linha por regiao e o
    indice sairia duplicado.
    """
    w = "" if filtro is None else " AND %s" % filtro
    d = q(db, "SELECT date, value FROM %s WHERE name='%s'%s ORDER BY date"
              % (tabela, nome.replace("'", "''"), w))
    d["date"] = pd.to_datetime(d["date"])
    s = d.set_index("date")["value"].astype(float).dropna()
    s.index = pd.PeriodIndex(s.index, freq="M")
    return s.sort_index()


def _sa(r: pd.Series) -> pd.Series:
    """STL aditivo na TAXA mensal, fatores congelados ate dez do ano anterior.

    Dezembro fica fora da amostra ate janeiro seguinte chegar -- mesma regra de
    `_seasonal_cutoff()` em analytics/brasil/inflation/fetch_bcb.py.

    A amostra comeca em `INICIO_SA`, e isso NAO e detalhe: `inflc_agregados` guarda o
    IPCA desde 1980, e ajustar sazonalidade aditiva numa serie que passa de 80% ao mes
    para 0,4% produz fator sazonal de -2,0 p.p. em agosto. Com a serie inteira o
    "dessazonalizado" saia MAIS volatil que o bruto (sd de 1,03 contra 0,39 no IPCA
    cheio, 0,46 contra 0,34 em servicos) -- ou seja, o ajuste estava injetando ruido, e
    esse ruido ia direto para o sigma que define a cor. `fetch_bcb.py` nunca viu o
    problema porque puxa do SGS a partir de 2000.
    """
    r = r.dropna()
    r = r[r.index >= pd.Period(INICIO_SA, freq="M")]
    corte = pd.Period(f"{r.index.max().year - 1}-12", freq="M")
    dentro = r[r.index <= corte]
    if len(dentro) < 24:
        return r
    fit = STL(dentro.values, period=12, robust=True).fit()
    sf = pd.Series(fit.seasonal, index=dentro.index.month).groupby(level=0).mean()
    return r - np.array([sf.get(m, 0.0) for m in r.index.month])


def acum12(nome: str) -> pd.Series:
    return (np.exp(np.log1p(_mensal(nome) / 100.0).rolling(12).sum()) - 1.0) * 100.0


def mm3m_anual(nome: str) -> pd.Series:
    sa = _sa(_mensal(nome))
    return (np.exp(np.log1p(sa / 100.0).rolling(3).sum() * 4.0) - 1.0) * 100.0


def nucleos_mm3m() -> pd.Series:
    X = pd.DataFrame({n: _mensal(n) for n in NUCLEOS}).dropna()
    sa = _sa(X.mean(axis=1))
    return (np.exp(np.log1p(sa / 100.0).rolling(3).sum() * 4.0) - 1.0) * 100.0


def nucleo_ex3_mm3m() -> pd.Series:
    """EX3 -- o nucleo por exclusao que sobra em bens industriais e servicos subjacentes.

    E o mais proximo de uma medida de inflacao subjacente sensivel ao hiato: sai de fora
    exatamente o que o Copom nao controla no curto prazo (alimentacao no domicilio e
    administrados). Entra ao lado da media dos cinco porque a media dilui justamente esse
    recorte -- EX0, DP, MA e P55 mantem administrados.
    """
    return mm3m_anual("ipca_nucleo_ex03")


def desocupacao_sa() -> pd.Series:
    """Taxa de desocupacao da PNAD Continua mensal, dessazonalizada por STL.

    O IBGE nao publica versao dessazonalizada da mensal (so da trimestral movel), entao o
    ajuste e nosso -- mesma convencao de fatores congelados do resto do modulo. O indice e
    o mes final do trimestre movel, que e como a propria divulgacao rotula.
    """
    return _sa(_mensal("taxa_desocupacao", tabela="mt_pnad", filtro="region='Brasil'"))


def caged_saldo_sa() -> pd.Series:
    """Saldo de emprego formal em mil vagas, dessazonalizado, media de 3 meses.

    `mt_caged` guarda o ESTOQUE de vinculos, nao o fluxo -- e a diferenca mensal dele que
    reproduz o saldo do Novo CAGED (conferido ao vivo contra `mt_caged_setor`, ver
    domain/db/CLAUDE.md). A media de 3 meses e o que torna a serie legivel: o saldo de um
    mes isolado oscila mais que o sinal que ele carrega.
    """
    saldo = _mensal("caged_total", tabela="mt_caged").diff().dropna() / 1000.0
    return _sa(saldo).rolling(3).mean()


def ibcbr_3m3m() -> pd.Series:
    """IBC-Br: media movel de 3 meses contra a anterior, anualizada.

    Usa a serie que o proprio BCB dessazonaliza (`ibcbr_sa`) -- nao ha por que rodar STL
    em cima de um ajuste oficial. 3m/3m em vez de m/m porque um mes de IBC-Br revisa muito.
    """
    ma = _mensal("ibcbr_sa", tabela="atv_ibcbr").rolling(3).mean()
    return ((ma / ma.shift(3)) ** 4.0 - 1.0) * 100.0


def focus_anual_serie(indicador: str, ano: int) -> pd.Series:
    """Mediana da Focus para um ano-calendario fixo, por data de pesquisa."""
    d = q("macro_brasil",
          "SELECT date, mediana FROM expc_focus_periodo WHERE periodicidade='anual' "
          "AND base_calculo=0 AND indicador='%s' AND data_referencia='%d' ORDER BY date"
          % (indicador.replace("'", "''"), ano))
    d["date"] = pd.to_datetime(d["date"])
    return d.set_index("date")["mediana"].astype(float).dropna().sort_index()


def focus_reuniao_serie(rotulo: str) -> pd.Series:
    d = q("macro_brasil", "SELECT date, mediana FROM expc_focus_copom WHERE "
                          "base_calculo=0 AND reuniao='%s' ORDER BY date"
                          % rotulo.replace("'", "''"))
    d["date"] = pd.to_datetime(d["date"])
    return d.set_index("date")["mediana"].astype(float).dropna().sort_index()


def focus_ipca_12m_diario() -> pd.Series:
    d = q("macro_brasil", "SELECT date, mediana FROM expc_focus WHERE indicador='IPCA' "
                          "AND horizonte='12m' AND suavizada='S' AND base_calculo=0 "
                          "ORDER BY date")
    d["date"] = pd.to_datetime(d["date"])
    return d.set_index("date")["mediana"].astype(float).dropna().sort_index()


def juro_real_ex_ante() -> pd.Series:
    """i^e - pi^e, diferenca simples, como na eq. (2.1) do boxe.

    Reaproveita `focus_selic_12m_diario()` do modelo_painel de proposito: a leitura de
    i^e como a Selic esperada NO ponto de 12 meses (e nao a media do caminho) e uma
    decisao validada contra a Tabela 1 do boxe da neutra, e duas definicoes de juro real
    no mesmo relatorio seriam bug, nao variacao.
    """
    i = focus_selic_12m_diario()
    p = focus_ipca_12m_diario()
    return (i - p).dropna()


# ── especificacao das variaveis ──────────────────────────────────────────────
# `sinal`: +1 subir e hawkish, -1 subir e dovish, 0 sem leitura hawk/dove.
# `grupo`: grupo do calendario quando a serie e indexada por periodo de REFERENCIA;
#          None quando o indice ja e a data em que o dado existiu (mercado/Focus).
# `grupo_agenda`: so para a agenda -- a serie e lida por data (grupo=None), mas a
#          divulgacao dela ainda e um evento agendado. E o caso da Focus: o indice e a
#          data da pesquisa, e mesmo assim o Boletim tem dia e hora no calendario.
# `modo`: 'pct' quando a variavel e um NIVEL de preco e o que importa e a variacao
#          proporcional (cambio). Muda o delta e o sigma, nao o valor exibido.
SPEC = [
    dict(key="ipca12", bloco="Inflação corrente", label="IPCA — acum. 12m",
         unidade="%", sinal=+1, grupo="ibge_ipca", casas=2,
         fn=lambda ctx: acum12("ipca"),
         nota="Variação acumulada em 12 meses do IPCA cheio."),
    dict(key="nucleos", bloco="Inflação corrente",
         label="Núcleos (média de 5) — mm3m anualizada",
         unidade="% a.a.", sinal=+1, grupo="ibge_ipca", casas=2,
         fn=lambda ctx: nucleos_mm3m(),
         nota="Média simples de EX0, EX3, médias aparadas com suavização, dupla "
              "ponderação e P55 — os cinco que o BCB acompanha no RPM. "
              "Dessazonalizada por STL com fatores congelados."),
    dict(key="ex3", bloco="Inflação corrente", label="Núcleo EX3 — mm3m anualizada",
         unidade="% a.a.", sinal=+1, grupo="ibge_ipca", casas=2,
         fn=lambda ctx: nucleo_ex3_mm3m(),
         nota="Núcleo por exclusão que deixa de fora alimentação no domicílio e "
              "administrados — o que sobra é bens industriais e serviços subjacentes, "
              "a parte da cesta que responde ao hiato. Dessazonalizado por STL com "
              "fatores congelados."),

    dict(key="ibcbr", bloco="Atividade e mercado de trabalho",
         label="IBC-Br — 3m/3m anualizada (dessaz.)",
         unidade="% a.a.", sinal=+1, grupo="bcb_ibcbr", casas=2,
         fn=lambda ctx: ibcbr_3m3m(),
         nota="Proxy mensal do PIB. Média móvel de 3 meses contra a anterior, "
              "anualizada, sobre a série que o próprio BCB dessazonaliza. Atividade "
              "mais forte pressiona o hiato — leitura hawkish."),
    dict(key="desemprego", bloco="Atividade e mercado de trabalho",
         label="Taxa de desocupação (dessaz.)",
         unidade="%", sinal=-1, grupo="ibge_pnad_mensal", casas=2,
         fn=lambda ctx: desocupacao_sa(),
         nota="PNAD Contínua mensal, trimestre móvel, dessazonalizada por STL (o IBGE "
              "só publica ajuste da trimestral). Sinal invertido: desemprego mais alto "
              "é mais folga no mercado de trabalho, logo argumento para cortar."),
    dict(key="caged", bloco="Atividade e mercado de trabalho",
         label="CAGED — saldo formal (dessaz., média 3m)",
         unidade="mil vagas", sinal=+1, grupo="bcb_caged_sgs_mirror", casas=1,
         fn=lambda ctx: caged_saldo_sa(),
         nota="Diferença mensal do estoque de vínculos celetistas do Novo CAGED "
              "espelhado no SGS, em mil vagas, dessazonalizada por STL e suavizada em "
              "3 meses. Geração de emprego mais forte é menos folga — leitura hawkish."),

    dict(key="focus_ipca_a0", bloco="Expectativas (Focus)",
         label=lambda ctx: "IPCA %d (Focus)" % ctx["ano0"],
         unidade="%", sinal=+1, grupo=None, grupo_agenda="bcb_focus", casas=2,
         fn=lambda ctx: focus_anual_serie("IPCA", ctx["ano0"]),
         nota="Mediana para o ano-calendário corrente."),
    dict(key="focus_ipca_a1", bloco="Expectativas (Focus)",
         label=lambda ctx: "IPCA %d (Focus)" % ctx["ano1"],
         unidade="%", sinal=+1, grupo=None, grupo_agenda="bcb_focus", casas=2,
         fn=lambda ctx: focus_anual_serie("IPCA", ctx["ano1"]),
         nota="Ano seguinte — mais próximo do horizonte relevante que o Copom persegue "
              "do que o ano corrente."),
    dict(key="focus_ipca_12m", bloco="Expectativas (Focus)",
         label="IPCA 12m suavizado (Focus)", unidade="%", sinal=+1, grupo=None,
         grupo_agenda="bcb_focus", casas=2,
         fn=lambda ctx: focus_ipca_12m_diario(),
         nota="Horizonte móvel — é o π^e que entra na Curva de Phillips do modelo "
              "agregado (eq. 1)."),
    dict(key="focus_pib_a0", bloco="Expectativas (Focus)",
         label=lambda ctx: "PIB %d (Focus)" % ctx["ano0"],
         unidade="%", sinal=+1, grupo=None, grupo_agenda="bcb_focus", casas=2,
         fn=lambda ctx: focus_anual_serie("PIB Total", ctx["ano0"]),
         nota="Crescimento mais forte pressiona o hiato — leitura hawkish."),
    dict(key="focus_pib_a1", bloco="Expectativas (Focus)",
         label=lambda ctx: "PIB %d (Focus)" % ctx["ano1"],
         unidade="%", sinal=+1, grupo=None, grupo_agenda="bcb_focus", casas=2,
         fn=lambda ctx: focus_anual_serie("PIB Total", ctx["ano1"]),
         nota="Ano seguinte — é o crescimento que cai dentro do horizonte em que a "
              "política monetária de hoje ainda age."),
    dict(key="focus_selic_reuniao", bloco="Expectativas (Focus)",
         label=lambda ctx: "Selic esperada na reunião de %s (Focus)"
                           % ctx["prox"]["date"].strftime("%d/%m"),
         unidade="%", sinal=0, grupo=None, grupo_agenda="bcb_focus", casas=2,
         fn=lambda ctx: (focus_reuniao_serie(ctx["rotulo_focus"])
                         if ctx.get("rotulo_focus") else pd.Series(dtype=float)),
         nota="A MESMA reunião nas duas colunas: o que o mercado esperava dela na "
              "decisão passada contra o que espera hoje. Sem cor — é reação do mercado, "
              "não condição que antecede a decisão."),
    dict(key="focus_selic_a0", bloco="Expectativas (Focus)",
         label=lambda ctx: "Selic fim de %d (Focus)" % ctx["ano0"],
         unidade="%", sinal=0, grupo=None, grupo_agenda="bcb_focus", casas=2,
         fn=lambda ctx: focus_anual_serie("Selic", ctx["ano0"]),
         nota="Idem — reação, não condição."),

    dict(key="juro_real", bloco="Condições financeiras",
         label="Juro real ex-ante (12m)", unidade="%", sinal=-1, grupo=None,
         grupo_agenda="bcb_focus", casas=2,
         fn=lambda ctx: juro_real_ex_ante(),
         nota="Selic esperada no ponto de 12 meses menos IPCA esperado a 12 meses, "
              "diferença simples (eq. 2.1). Sinal invertido: juro real mais alto é "
              "política já mais apertada, logo argumento para cortar."),
    dict(key="ptax", bloco="Condições financeiras", label="Câmbio PTAX (venda)",
         unidade="R$/US$", sinal=+1, grupo=None, casas=4, modo="pct",
         fn=lambda ctx: serie("macro_brasil", "cmb_ptax", "ptax_venda"),
         nota="Fechamento diário. Depreciação é repasse — leitura hawkish. O Δ é "
              "variação percentual, não em centavos: o repasse cambial é proporcional, "
              "e 10 centavos a 3,00 não são a mesma notícia que 10 centavos a 6,00."),
    dict(key="brent", bloco="Condições financeiras", label="Brent (1º futuro)",
         unidade="US$/bbl", sinal=+1, grupo=None, casas=2,
         fn=lambda ctx: serie("macro_international", "comm_brent", "brent_usd"),
         nota="Insumo direto de combustíveis e de administrados."),
    dict(key="icbr", bloco="Condições financeiras", label="IC-Br (índice, R$)",
         unidade="índice", sinal=+1, grupo="bcb_icbr", casas=1,
         fn=lambda ctx: _mensal("icbr_geral", tabela="comm_icbr"),
         nota="Índice de Commodities Brasil, em reais — é a inflação importada π* do "
              "modelo agregado (eq. 1.1). Divulgado mensalmente às 14:30."),
]


# ── montagem ─────────────────────────────────────────────────────────────────
def _valor_em(s: pd.Series, corte, grupo_cal: dict | None, teto=None) -> dict:
    """Leitura da serie `s` no corte, com a divulgacao que a justifica.

    `grupo_cal` None -> a serie e indexada pela data em que o dado existiu; corte direto.
    Caso contrario o indice e periodo de REFERENCIA e a data de divulgacao decide.
    """
    vazio = {"valor": None, "ref": None, "pos": None, "exata": True,
             "pendente": False, "divulgacao": None}
    s = s.dropna()
    if s.empty:
        return vazio

    if grupo_cal is None:
        idx = s.index[s.index <= pd.Timestamp(corte)]
        if not len(idx):
            return vazio
        ref = idx[-1]
        return {"valor": float(s.loc[ref]), "ref": ref, "pos": int(s.index.get_loc(ref)),
                "exata": True, "pendente": False, "divulgacao": None}

    ref, exata = ref_divulgado(grupo_cal, corte, s.index)
    if ref is None:
        return vazio
    # Teto do banco: nao se afirma um valor que o ETL ainda nao carregou.
    pendente = False
    if teto is not None and ref > teto:
        ref, exata = teto, divulgacao(grupo_cal, teto)[1]
        pendente = True
    quando, _ = divulgacao(grupo_cal, ref)
    return {"valor": float(s.loc[ref]), "ref": ref, "pos": int(s.index.get_loc(ref)),
            "exata": exata, "pendente": pendente,
            "divulgacao": quando.strftime("%d/%m/%Y %H:%M") if quando else None}


def _sigma(s: pd.Series, k: int) -> float | None:
    """Escala tipica da variacao sobre k observacoes, nos ultimos ANOS_SIGMA anos.

    Escala ROBUSTA (1,4826 x desvio absoluto mediano), nao desvio-padrao. Dez anos de
    historia contem 2020-2021, e com desvio-padrao aquele episodio vira a regua: a
    inflacao de servicos em mm3m anualizada saia com sigma de 3,06 p.p. para uma variacao
    mensal, o que apagava a cor de praticamente qualquer movimento normal da serie. O
    1,4826 e a constante que faz as duas medidas coincidirem sob normalidade, entao a
    escala continua legivel como "desvio-padrao" -- so nao se deixa sequestrar por uma
    pandemia. Mesmo motivo pelo qual `regra()` usa mediana.
    """
    if k <= 0 or len(s) < k + 8:
        return None
    d = s.diff(k).dropna()
    if isinstance(d.index, pd.PeriodIndex):
        corte = d.index.max() - 12 * ANOS_SIGMA
    else:
        corte = d.index.max() - pd.DateOffset(years=ANOS_SIGMA)
    d = d[d.index >= corte]
    if len(d) < 8:
        return None
    v = 1.4826 * float(np.median(np.abs(d.values - np.median(d.values))))
    if not (np.isfinite(v) and v > 0):        # serie quase constante na janela
        v = float(d.std())
    return v if np.isfinite(v) and v > 0 else None


def _rotulo_ref(ref) -> str:
    if ref is None:
        return "—"
    if isinstance(ref, pd.Period):
        return ref.strftime("%m/%Y")
    return pd.Timestamp(ref).strftime("%d/%m/%Y")


def agenda(prox: dict, hoje: dt.date, rotulos: dict[str, list[str]]) -> list[dict]:
    """Divulgacoes que ainda VAO sair antes do corte e que alimentam a tabela.

    Duas restricoes, as duas a pedido do usuario. Para frente: o que ja saiu desde a
    ultima reuniao esta na propria tabela, linha a linha, e de forma exata. E so o que
    esta em `rotulos` -- o calendario inteiro ja tem relatorio proprio
    (analytics/release_calendar/), e aqui a pergunta e outra: o que ainda pode virar uma
    celula desta tabela antes da decisao.
    """
    saida = []
    for nome, g in grupos().items():
        if nome not in rotulos:
            continue
        for e in g.get("entries", []):
            quando = _quando(e, g)
            if not (dt.datetime.combine(hoje, dt.time.min) <= quando <= prox["corte"]):
                continue
            saida.append({
                "grupo": nome,
                "instituicao": g.get("institution", ""),
                "nome": g.get("name", nome),
                "date": quando.date().isoformat(),
                "hora": quando.strftime("%H:%M"),
                "referencia": str(e.get("reference_period") or ""),
                "confirmado": bool(e.get("confirmed", False)),
                "variaveis": rotulos[nome],
                "tables": g.get("tables", []),
            })
    return sorted(saida, key=lambda r: (r["date"], r["hora"]))


def montar(agora: dt.datetime | None = None) -> dict:
    agora = agora or dt.datetime.now()
    hoje = agora.date()
    ant, prox = reunioes(agora)
    if ant is None or prox is None:
        return {"erro": "calendario sem reuniao anterior ou proxima para %s -- ver "
                        "domain/release_calendar/ROLLOVER.md" % hoje}

    corte_hoje = agora
    gs = grupos()
    ctx = {
        "hoje": hoje, "ant": ant, "prox": prox,
        "ano0": hoje.year, "ano1": hoje.year + 1,
        "rotulo_focus": None,
    }
    try:
        ult_focus = pd.Timestamp(q("macro_brasil",
                                   "SELECT MAX(date) mx FROM expc_focus_copom")["mx"].iloc[0])
        ctx["rotulo_focus"] = rotulo_focus(ult_focus)
    except Exception:
        pass

    linhas, avisos = [], []
    for spec in SPEC:
        label = spec["label"](ctx) if callable(spec["label"]) else spec["label"]
        linha = {"key": spec["key"], "bloco": spec["bloco"], "label": label,
                 "unidade": spec["unidade"], "sinal": spec["sinal"],
                 "casas": spec["casas"], "nota": spec["nota"],
                 "grupo": spec["grupo"]}
        try:
            s = spec["fn"](ctx).dropna()
        except Exception as exc:
            linha["erro"] = str(exc)
            linhas.append(linha)
            avisos.append("%s: %s" % (spec["key"], exc))
            continue
        if s.empty:
            linha["erro"] = "serie vazia"
            linhas.append(linha)
            continue

        s = s[~s.index.duplicated(keep="last")].sort_index()
        g = gs.get(spec["grupo"]) if spec["grupo"] else None
        teto = s.index.max() if g is not None else None
        a = _valor_em(s, ant["corte"], g, teto)
        h = _valor_em(s, corte_hoje, g, teto)

        # A regra ajustada tem de reproduzir o que ja aconteceu: se ela diz que o ultimo
        # ponto do banco so sai depois de hoje, ou ela esta errada ou o dado saiu antes do
        # previsto -- nos dois casos as datas da coluna "na reuniao" ficam suspeitas.
        if g is not None:
            quando_ult, exata_ult = divulgacao(g, s.index.max())
            if quando_ult is not None and not exata_ult and quando_ult > agora:
                avisos.append("%s: a regra ajustada de %s poe a divulgacao de %s em %s, "
                              "depois de agora -- dado no banco antes do previsto"
                              % (spec["key"], spec["grupo"], _rotulo_ref(s.index.max()),
                                 quando_ult.strftime("%d/%m/%Y")))

        # Uma data estimada so e perigosa quando cai perto do corte: se a regra erra ate
        # E dias e a divulgacao estimada esta a mais de E dias da reuniao, a resposta e a
        # mesma com ou sem o erro. Avisar sempre que a data e estimada seria ruido; avisar
        # quando o erro PODE virar a celula e informacao.
        erro_fit = regra(g)[2] if (g is not None and regra(g)) else None
        linha["fit_erro_dias"] = erro_fit
        for col, leitura, corte in (("na reuniao", a, ant["corte"]), ("hoje", h, agora)):
            if leitura["exata"] or leitura["divulgacao"] is None or not erro_fit:
                continue
            quando = dt.datetime.strptime(leitura["divulgacao"], "%d/%m/%Y %H:%M")
            if abs((quando - corte).days) <= erro_fit:
                avisos.append("%s (%s): divulgacao estimada em %s, a menos de %d dias do "
                              "corte %s, e a regra de %s erra ate %d dias -- a celula pode "
                              "estar no periodo errado"
                              % (spec["key"], col, leitura["divulgacao"], erro_fit,
                                 corte.strftime("%d/%m/%Y %H:%M"), spec["grupo"], erro_fit))

        linha.update({
            "ant": None if a["valor"] is None else round(a["valor"], 6),
            "hoje": None if h["valor"] is None else round(h["valor"], 6),
            "ref_ant": _rotulo_ref(a["ref"]), "ref_hoje": _rotulo_ref(h["ref"]),
            "div_ant": a["divulgacao"], "div_hoje": h["divulgacao"],
            "exata": bool(a["exata"] and h["exata"]),
            "pendente": bool(h["pendente"]),
            "ultimo_banco": _rotulo_ref(s.index.max()),
        })
        if a["valor"] is None or h["valor"] is None:
            linhas.append(linha)
            continue

        k = h["pos"] - a["pos"]
        # `pct`: a escala tambem tem de virar log, senao o sigma continua em centavos e o
        # z ficaria com numerador e denominador em unidades diferentes. 100*dlog e a
        # variacao percentual para os movimentos desta ordem de grandeza.
        if spec.get("modo") == "pct" and a["valor"] and bool((s > 0).all()):
            delta = (h["valor"] / a["valor"] - 1.0) * 100.0
            sigma = _sigma(np.log(s) * 100.0, k)
            linha["delta_pct"] = True
        else:
            delta = h["valor"] - a["valor"]
            sigma = _sigma(s, k)
        linha["novos"] = int(k)
        linha["delta"] = round(delta, 6)
        linha["sigma"] = None if sigma is None else round(sigma, 6)
        if k == 0:
            linha["z"] = 0.0
        elif spec["sinal"] == 0 or sigma is None:
            linha["z"] = None
        else:
            linha["z"] = round(float(np.clip(spec["sinal"] * delta / sigma, -3, 3)), 4)
        linhas.append(linha)

    # As quatro categorias particionam as linhas: uma variavel sem dado novo NAO e
    # "neutra" (isso seria dizer que ela nao mexeu), e sim mudez -- ela nao foi
    # perguntada. Contar as duas coisas junto foi bug numa primeira versao.
    com_dado = [l for l in linhas if l.get("novos", 0) > 0 and l.get("z") is not None]
    zs = [l["z"] for l in com_dado]
    resumo = {
        "hawkish": sum(1 for l in com_dado if l["z"] > 0.05),
        "dovish": sum(1 for l in com_dado if l["z"] < -0.05),
        "neutro": sum(1 for l in com_dado if abs(l["z"]) <= 0.05),
        "sem_leitura": sum(1 for l in linhas
                           if l.get("novos", 0) > 0 and l.get("z") is None),
        "sem_dado": sum(1 for l in linhas if l.get("novos") == 0),
        "saldo": round(float(np.mean(zs)), 3) if zs else None,
        "n_saldo": len(zs),
    }

    # Quais grupos do calendario alimentam quais linhas -- e o que a agenda mostra na
    # coluna "Alimenta", e o que decide o que entra nela.
    rotulos: dict[str, list[str]] = {}
    for spec, l in zip(SPEC, linhas):
        for g in (l.get("grupo"), spec.get("grupo_agenda")):
            if g:
                rotulos.setdefault(g, []).append(l["label"])
    n_ant = numero_reuniao(ant["date"])
    return {
        "hoje": hoje.isoformat(),
        "ant": {"date": ant["date"].isoformat(),
                "date_start": ant["date_start"].isoformat() if ant["date_start"] else None,
                "numero": n_ant,
                "corte": ant["corte"].strftime("%d/%m/%Y %H:%M")},
        "prox": {"date": prox["date"].isoformat(),
                 "date_start": prox["date_start"].isoformat() if prox["date_start"] else None,
                 "numero": (n_ant + 1) if n_ant else None,
                 "rotulo": prox["rotulo"],
                 "rotulo_focus": ctx["rotulo_focus"],
                 "dias": (prox["date"] - hoje).days},
        "linhas": linhas,
        "resumo": resumo,
        "agenda": agenda(prox, hoje, rotulos),
        "avisos": avisos,
        "anos_sigma": ANOS_SIGMA,
    }


if __name__ == "__main__":
    import json
    d = montar()
    if "erro" in d:
        raise SystemExit(d["erro"])
    print("%da reuniao (%s)  ->  %da (%s), em %d dias"
          % (d["ant"]["numero"] or 0, d["ant"]["date"], d["prox"]["numero"] or 0,
             d["prox"]["date"], d["prox"]["dias"]))
    print("-" * 108)
    print("%-46s %10s %10s %9s %7s  %s" % ("variavel", "na reuniao", "hoje", "delta", "z", "referencia"))
    for l in d["linhas"]:
        if l.get("erro"):
            print("%-46s  FALHOU: %s" % (l["label"][:46], l["erro"]))
            continue
        f = "%%.%df" % l["casas"]
        print("%-46s %10s %10s %9s %7s  %s -> %s%s%s" % (
            l["label"][:46],
            "—" if l["ant"] is None else f % l["ant"],
            "—" if l["hoje"] is None else f % l["hoje"],
            "—" if l.get("delta") is None else
            ("%+.2f%%" % l["delta"] if l.get("delta_pct") else "%+.2f" % l["delta"]),
            "—" if l.get("z") is None else "%+.2f" % l["z"],
            l["ref_ant"], l["ref_hoje"],
            "" if l["exata"] else " ~", " PENDENTE" if l.get("pendente") else ""))
    print("-" * 108)
    r = d["resumo"]
    print("hawkish %d | dovish %d | neutro %d | sem leitura %d | sem dado novo %d | "
          "saldo %s (%d variaveis)"
          % (r["hawkish"], r["dovish"], r["neutro"], r["sem_leitura"], r["sem_dado"],
             r["saldo"], r["n_saldo"]))
    print("\nDivulgacao que sustenta cada coluna (~ = data estimada, nao do calendario):")
    for l in d["linhas"]:
        if l.get("div_ant") or l.get("div_hoje"):
            print("  %-46s %s  |  %s%s" % (l["label"][:46], l.get("div_ant") or "—",
                                           l.get("div_hoje") or "—",
                                           "" if l["exata"] else "  ~"))
    print("\nAinda sai antes da reuniao (%d eventos):" % len(d["agenda"]))
    for a in d["agenda"]:
        print("  %s %s  %-40s %-9s %s" % (a["date"], a["hora"], a["nome"][:40],
                                          a["referencia"], " | ".join(a["variaveis"])[:60]))
    if d["avisos"]:
        print("\nAVISOS:", *d["avisos"], sep="\n  ")
