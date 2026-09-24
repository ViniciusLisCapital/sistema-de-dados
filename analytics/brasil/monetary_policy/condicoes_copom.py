"""
Condicoes economicas reuniao a reuniao do Copom: o que o Comite tinha na mesa em cada
uma das ultimas oito decisoes, e o que ja tem para a proxima.

A pergunta que a aba responde nao e "onde estamos", e "o que MUDOU de uma reuniao para a
seguinte". Entre duas reunioes passam ~45 dias, e nesse intervalo saem 1 ou 2 IPCAs, 1
IPCA-15, 6 Boletins Focus e ~30 pregoes -- e sao esses dados novos, nao o nivel das
variaveis, que podem mover a decisao seguinte.

Nada e reconstruido para tras: a janela e sempre relativa a AGORA (as N ultimas ja
decididas mais a proxima), entao ela anda sozinha quando uma reuniao passa.

## A matriz, e o que uma celula significa

Uma linha por variavel, uma coluna por reuniao. A celula e o valor que a variavel tinha
**no corte daquela reuniao** -- nao o valor do mes da reuniao. Sao coisas diferentes
sempre que a divulgacao de um mes cai depois da decisao: na reuniao de 05/08/2026 o IPCA
disponivel era o de JUNHO, porque o de julho so saiu em 13/08.

So recebe COR a celula que trouxe informacao nova desde a coluna anterior. Uma serie
trimestral repete o ultimo numero nas reunioes em que nao houve divulgacao, e essas
celulas ficam sem cor de proposito: repetir nao e noticia. E por isso que a janela
interna tem N+1 reunioes e a exibida tem N -- a coluna mais antiga precisa de uma
anterior para ter delta, e sem ela a primeira coluna nunca receberia cor, o que seria
propriedade da janela e nao do dado.

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
`analytics/brasil/inflation/generate_report.py`. Congelar importa aqui mais do que la: com
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
    focus_anual,
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
# Reunioes passadas na matriz; a proxima entra sempre, entao a tabela tem N+1 colunas.
N_PASSADAS = 8
# Horizonte relevante em trimestres a frente da reuniao -- Decreto 12.079/2024, o mesmo
# `hr_6_trimestres` que a aba Projecoes filtra.
HR_TRIMESTRES = 6
# Inicio da amostra do ajuste sazonal -- ver `_sa()`. 2000 e o mesmo corte de
# analytics/brasil/inflation/generate_report.py, ja com o regime de metas rodando.
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
    """'2026-08' -> Period mensal, '2026-Q2' -> Period trimestral.

    A frequencia e INFERIDA em vez de fixada em mes: o grupo do PIB rotula por trimestre
    (`2026-Q2`) e forcar `freq="M"` ali devolveria o mes de fechamento do trimestre, o
    que casaria com um indice mensal que nao existe e faria a serie nunca resolver.
    Qualquer outra coisa ('281a reuniao') -> None, que e o que tira o grupo bcb_copom da
    conta da regra.
    """
    if not rp:
        return None
    try:
        return pd.Period(str(rp))
    except Exception:
        return None


def _mes_fim(ref: pd.Period) -> tuple[int, int]:
    """(ano, mes) em que o periodo de referencia TERMINA.

    E a ancora da defasagem, e ela tem de ser o fim e nao o inicio: o PIB do 2o trimestre
    sai ~3 meses depois de junho, nao de abril. Num periodo mensal o fim e o proprio mes,
    entao a conta e identica a que havia antes.
    """
    t = ref.end_time
    return int(t.year), int(t.month)


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
    # Uma entrada por periodo de REFERENCIA, a mais tarde -- a mesma desempate de
    # `divulgacao()`. Sem isto o rotulo errado do ICS entra no ajuste: no `bcb_credit_note`
    # de 2026 ele leva o erro maximo da regra de 2 para 27 dias, e 27 dias marca como
    # ambigua toda celula de credito da matriz.
    ultima: dict[pd.Period, dt.date] = {}
    for e in grupo.get("entries", []):
        ref = _ref(e.get("reference_period"))
        if ref is None:
            continue
        d = _data(e["date"])
        if ref not in ultima or d > ultima[ref]:
            ultima[ref] = d

    defas, dias, pares = [], [], []
    for ref, d in sorted(ultima.items()):
        ry, rm = _mes_fim(ref)
        defas.append((d.year * 12 + d.month) - (ry * 12 + rm))
        dias.append(_dia_util(d))
        pares.append((ref, d))
    if not defas:
        return None
    md, mdia = int(np.median(defas)), int(round(float(np.median(dias))))
    erro = 0
    for ref, real in pares:
        ry, rm = _mes_fim(ref)
        alvo = pd.Timestamp(year=ry, month=rm, day=1) + pd.DateOffset(months=md)
        erro = max(erro, abs((_data_dia_util(alvo.year, alvo.month, mdia) - real).days))
    return md, mdia, erro


def divulgacao(grupo: dict, ref: pd.Period) -> tuple[dt.datetime | None, bool]:
    """Quando o periodo `ref` foi (ou sera) divulgado. bool = veio do calendario.

    Havendo mais de uma entrada para o mesmo `reference_period`, vale a MAIS TARDE. Isso
    nao e hipotetico: o grupo `bcb_credit_note` do calendario de 2026 carimba `2026-06` em
    01/07 e de novo em 30/07, e a cadencia do proprio grupo (abril->28/05, junho->30/07,
    julho->28/08) mostra que a primeira e um rotulo errado do ICS. Pegar a primeira faria
    o dado de junho aparecer disponivel um mes antes de existir, que e exatamente o
    anacronismo que este modulo existe para nao cometer.
    """
    candidatas = [_quando(e, grupo) for e in grupo.get("entries", [])
                  if _ref(e.get("reference_period")) == ref]
    if candidatas:
        return max(candidatas), True
    r = regra(grupo)
    if r is None:
        return None, False
    defas, dia, _ = r
    ry, rm = _mes_fim(ref)
    alvo = pd.Timestamp(year=ry, month=rm, day=1) + pd.DateOffset(months=defas)
    return dt.datetime.combine(_data_dia_util(alvo.year, alvo.month, dia),
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


_MES_PT = ["jan", "fev", "mar", "abr", "mai", "jun",
           "jul", "ago", "set", "out", "nov", "dez"]


def _reuniao_label(d: dt.date) -> str:
    return "%s/%02d" % (_MES_PT[d.month - 1], d.year % 100)


def todas_reunioes() -> list[dict]:
    """Toda reuniao conhecida, do banco e do calendario, deduplicada pela DATA.

    As duas fontes sao necessarias e nenhuma basta. `pm_copom_reuniao` tem a historia
    inteira com o passo de Selic decidido, mas so entra depois que o ETL roda -- a 281a
    (16/09/2026) ja aconteceu e ainda nao esta la. O calendario tem as datas futuras e as
    do ano corrente, e nenhum passo. A uniao da a janela; o passo fica `None` onde so o
    calendario alcanca, que e uma coluna sem decisao na tela e nao um zero inventado.
    """
    por_data: dict[dt.date, dict] = {}
    try:
        d = q("macro_brasil", "SELECT nro_reuniao, date, variacao_bps, decisao, "
                              "selic_decidida FROM pm_copom_reuniao ORDER BY date")
        for r in d.itertuples():
            data = pd.Timestamp(r.date).date()
            por_data[data] = {
                "date": data, "date_start": None,
                "numero": int(r.nro_reuniao),
                "bps": None if pd.isna(r.variacao_bps) else int(r.variacao_bps),
                "decisao": r.decisao,
                "selic": None if pd.isna(r.selic_decidida) else float(r.selic_decidida),
            }
    except Exception:
        pass

    g = grupos().get("bcb_copom") or {}
    for e in g.get("entries", []):
        data = _data(e["date"])
        r = por_data.setdefault(data, {"date": data, "numero": None, "bps": None,
                                       "decisao": None, "selic": None})
        r["date_start"] = _data(e["date_start"]) if e.get("date_start") else None
        if r.get("numero") is None:
            # '281a reuniao' -> 281. O rotulo e do calendario e nem toda entrada tem.
            txt = str(e.get("reference_period") or "")
            digitos = "".join(c for c in txt if c.isdigit())
            if digitos:
                r["numero"] = int(digitos)

    saida = []
    for data in sorted(por_data):
        r = dict(por_data[data])
        r.setdefault("date_start", None)
        r["corte"] = dt.datetime.combine(data, HORA_DECISAO)
        r["label"] = _reuniao_label(data)
        saida.append(r)
    return saida


def janela_reunioes(agora: dt.datetime | None = None,
                    n_passadas: int = N_PASSADAS) -> list[dict]:
    """As `n_passadas` ultimas reunioes ja decididas, mais a proxima.

    A separacao e pelo CORTE e nao pela data, pela mesma razao de `reunioes()`: no dia 1
    -- e no proprio dia 2 antes das 18:30 -- a decisao ainda nao saiu, e a reuniao em
    curso e a proxima.

    A coluna da reuniao FUTURA e cortada em `agora`, nao no corte dela: e o conjunto de
    informacao que ja esta na mesa, e afirmar o corte futuro seria ler dado que ainda nao
    existe.
    """
    agora = agora or dt.datetime.now()
    todas = todas_reunioes()
    passadas = [r for r in todas if r["corte"] <= agora]
    futuras = [r for r in todas if r["corte"] > agora]
    janela = passadas[-n_passadas:] if n_passadas > 0 else []
    for r in janela:
        r["futura"] = False
    if futuras:
        prox = dict(futuras[0])
        prox["futura"] = True
        # A leitura e cortada em AGORA -- afirmar o corte futuro seria ler dado que ainda
        # nao existe. O corte da reuniao continua guardado porque a agenda pergunta outra
        # coisa: o que ainda VAI sair antes dela.
        prox["corte_reuniao"] = prox["corte"]
        prox["corte"] = agora
        janela = janela + [prox]
    return janela




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
    `_seasonal_cutoff()` em analytics/brasil/inflation/generate_report.py.

    A amostra comeca em `INICIO_SA`, e isso NAO e detalhe: `inflc_agregados` guarda o
    IPCA desde 1980, e ajustar sazonalidade aditiva numa serie que passa de 80% ao mes
    para 0,4% produz fator sazonal de -2,0 p.p. em agosto. Com a serie inteira o
    "dessazonalizado" saia MAIS volatil que o bruto (sd de 1,03 contra 0,39 no IPCA
    cheio, 0,46 contra 0,34 em servicos) -- ou seja, o ajuste estava injetando ruido, e
    esse ruido ia direto para o sigma que define a cor. O gerador da inflacao nunca viu o
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



def nucleos_mm3m() -> pd.Series:
    X = pd.DataFrame({n: _mensal(n) for n in NUCLEOS}).dropna()
    sa = _sa(X.mean(axis=1))
    return (np.exp(np.log1p(sa / 100.0).rolling(3).sum() * 4.0) - 1.0) * 100.0






def focus_anual_serie(indicador: str, ano: int) -> pd.Series:
    """Mediana da Focus para um ano-calendario fixo, por data de pesquisa."""
    d = q("macro_brasil",
          "SELECT date, mediana FROM expc_focus_periodo WHERE periodicidade='anual' "
          "AND base_calculo=0 AND indicador='%s' AND data_referencia='%d' ORDER BY date"
          % (indicador.replace("'", "''"), ano))
    d["date"] = pd.to_datetime(d["date"])
    return d.set_index("date")["mediana"].astype(float).dropna().sort_index()




# ── series novas da matriz ───────────────────────────────────────────────────
def ibcbr_12m() -> pd.Series:
    """IBC-Br: crescimento acumulado em 12 meses contra os 12 anteriores.

    Serie NSA de proposito. O acumulado de 12 meses ja e sazonalmente neutro por
    construcao -- cada mes do calendario entra uma vez no numerador e uma no
    denominador --, entao aplicar ajuste em cima seria dessazonalizar duas vezes.
    A 3m/3m anualizada, que a versao anterior desta aba usava, precisava do ajuste;
    esta nao.
    """
    ix = _mensal("ibcbr_nsa", tabela="atv_ibcbr")
    return (ix.rolling(12).sum() / ix.rolling(12).sum().shift(12) - 1.0) * 100.0


def pib_acum_4t(categoria: str) -> pd.Series:
    """Taxa acumulada em 4 trimestres que o PROPRIO IBGE publica (SIDRA 5932).

    Nao e recalculada do indice de volume: a fonte publica a taxa, e a regra deste
    projeto e que numero publicado e gabarito. Indice TRIMESTRAL -- a serie fica
    parada entre divulgacoes, e e por isso que a matriz repete o valor nas reunioes
    sem dado novo em vez de deixar a celula vazia.
    """
    d = q("macro_brasil",
          "SELECT date, value FROM atv_pib_taxas WHERE indicador='acum_4t' "
          "AND name='%s' ORDER BY date" % categoria.replace("'", "''"))
    d["date"] = pd.to_datetime(d["date"])
    s = d.set_index("date")["value"].astype(float).dropna()
    s.index = pd.PeriodIndex(s.index, freq="Q")
    return s.sort_index()


def credito_real_12m(recurso: str) -> pd.Series:
    """Saldo de credito, crescimento real em 12 meses -- nominal deflacionado pelo IPCA.

    `recurso` e 'livre' ou 'direcionado'. O deflator e o IPCA acumulado em 12 meses do
    MESMO mes de referencia, e nao o do mes de divulgacao: as duas series sao indexadas
    pelo mes a que se referem, e cruzar por mes de divulgacao misturaria dois calendarios
    para produzir um numero que nao e de nenhum dos dois.

    Consequencia que o consumidor precisa saber: a linha so tem valor nos meses em que as
    DUAS existem. Como o IPCA sai antes da nota de credito do mes correspondente, quem
    limita e sempre o credito -- entao o `grupo` desta linha e o da nota de credito, e a
    data de divulgacao que a matriz usa e a dela.
    """
    nom = _mensal("saldo_%s_total" % recurso, tabela="cred_credito_resumo")
    nom12 = (nom / nom.shift(12) - 1.0) * 100.0
    ipca12 = acum12("ipca")
    j = pd.DataFrame({"n": nom12, "p": ipca12}).dropna()
    return ((1.0 + j["n"] / 100.0) / (1.0 + j["p"] / 100.0) - 1.0) * 100.0


def curva_br(curve: str, tenor: str) -> pd.Series:
    """Um vertice de `br_interest_rate`, por pregao."""
    d = q("macro_brasil",
          "SELECT date, value FROM br_interest_rate WHERE curve='%s' AND tenor='%s' "
          "ORDER BY date" % (curve, tenor))
    d["date"] = pd.to_datetime(d["date"])
    return d.set_index("date")["value"].astype(float).dropna().sort_index()


def implicita(tenor: str) -> pd.Series:
    """Inflacao implicita: (1+nominal)/(1+real) - 1, nao a subtracao das duas.

    A diferenca simples e a aproximacao usual e erra onde os niveis sao altos, que e
    exatamente a faixa brasileira: com DI a 14% e NTN-B a 7,5%, a subtracao da 6,50 e a
    forma correta da 6,05 -- 0,45 p.p. de diferenca, maior que o movimento tipico de um
    mes. Mesma licao da identidade produto/horas do relatorio de produtividade: a forma
    errada funciona na faixa em que se costuma olhar e quebra onde ninguem confere.
    """
    nom = curva_br("DIPRE", tenor)
    real = curva_br("NTNBJS", tenor)
    j = pd.DataFrame({"n": nom, "r": real}).dropna()
    return ((1.0 + j["n"] / 100.0) / (1.0 + j["r"] / 100.0) - 1.0) * 100.0


def us_juro_real(anos: int) -> pd.Series:
    """Juro real ex-ante americano: Treasury constant maturity - inflacao esperada.

    O Treasury NAO publica TIPS de 2 anos (medido: `DFII2` nao existe no FRED, a curva
    comeca em `DFII5`), entao o vertice de 2 anos so existe deflacionando o nominal. Os
    DOIS vertices usam o mesmo metodo de proposito -- ver a docstring de
    `domain/db/us/inflation/expc_inflacao.py` para os numeros que decidiram isso.

    A expectativa e MENSAL e a nominal e diaria. O deslocamento de 1 mes e conservador:
    o Cleveland carimba a estimativa no dia 1 do mes de referencia e a publica ao longo
    daquele mes, entao ler o valor de setembro so a partir de outubro garante que nunca
    se usa um numero antes de ele existir.
    """
    nom = q("macro_us", "SELECT date, value FROM us_interest_rate "
                        "WHERE curve='US_TREASURY' AND tenor='%dY' ORDER BY date" % anos)
    nom["date"] = pd.to_datetime(nom["date"])
    n = nom.set_index("date")["value"].astype(float).dropna().sort_index()

    exp = q("macro_us", "SELECT date, value FROM expc_inflacao WHERE tenor='%dY' "
                        "ORDER BY date" % anos)
    exp["date"] = pd.to_datetime(exp["date"])
    e = exp.set_index("date")["value"].astype(float).dropna().sort_index()
    e.index = e.index + pd.DateOffset(months=1)

    # reindex/ffill: a expectativa vale do mes em que passou a ser publicavel ate a
    # proxima. `n.index` e o calendario de pregao, que e o que decide a data da celula.
    ea = e.reindex(n.index.union(e.index)).ffill().reindex(n.index)
    return (n - ea).dropna()


def icbr_mm() -> pd.Series:
    """IC-Br em variacao percentual mensal.

    A versao anterior desta aba levava o IC-Br em NIVEL de indice, o que obrigava a
    tratar o delta como variacao percentual (`modo='pct'`). Aqui a propria linha ja e a
    variacao, entao o delta e em p.p. e a serie fala a mesma lingua do resto do bloco.
    """
    return _mensal("icbr_geral", tabela="comm_icbr").pct_change() * 100.0


def _focus_tri_ipca() -> pd.DataFrame:
    """IPCA trimestral da Focus: (data da pesquisa, trimestre de referencia, mediana)."""
    d = q("macro_brasil",
          "SELECT date, ref_date, mediana FROM expc_focus_periodo "
          "WHERE periodicidade='trimestral' AND base_calculo=0 AND indicador='IPCA' "
          "ORDER BY date, ref_date")
    d["date"] = pd.to_datetime(d["date"])
    d["tri"] = pd.PeriodIndex(pd.to_datetime(d["ref_date"]), freq="Q")
    d["mediana"] = d["mediana"].astype(float)
    return d.dropna(subset=["mediana"])


def focus_ipca_hr(trimestres: int = HR_TRIMESTRES) -> pd.Series:
    """IPCA esperado no HORIZONTE RELEVANTE, acumulado em 4 trimestres.

    Desde a 264a reuniao (Decreto 12.079/2024) o Copom persegue a meta seis trimestres a
    frente da REUNIAO, e nao mais no ano-calendario. O alvo e portanto a inflacao
    acumulada nos quatro trimestres que TERMINAM naquele ponto -- nao a taxa do trimestre
    isolado, que e o que a Focus publica.

    O horizonte e derivado da data da PESQUISA (trimestre dela + 6), nao da reuniao, e
    isso e o que faz a serie ser uma so em vez de uma por reuniao. As duas coincidem onde
    importa: a pesquisa que a matriz le numa reuniao cai no mesmo trimestre dela. Em
    troca, a janela e ROLANTE -- sempre seis trimestres a frente --, sem o dente de serra
    do horizonte de ano-calendario, que encurta de 12 para 4 trimestres ao longo do ano
    (a mesma razao pela qual a aba Projecoes filtra `regime='hr_6_trimestres'`).

    Acumula em composicao, nao em soma: sao taxas trimestrais, e somar quatro taxas de
    ~1% erra ~0,06 p.p. -- pequeno, mas gratuito de evitar.
    """
    d = _focus_tri_ipca()
    out = {}
    for data, g in d.groupby("date"):
        alvo = pd.Period(data, freq="Q") + trimestres
        janela = [alvo - k for k in range(3, -1, -1)]
        m = g.set_index("tri")["mediana"]
        if not all(t in m.index for t in janela):
            continue
        out[data] = (float(np.prod([1.0 + m.loc[t] / 100.0 for t in janela])) - 1.0) * 100.0
    return pd.Series(out).sort_index()


_PROJ_BC: pd.DataFrame | None = None


def _proj_bc() -> pd.DataFrame:
    """Projecao do BC para o horizonte relevante, UMA linha por reuniao.

    A mesma serie da aba Projecoes, com um filtro a mais: so o `comunicado`
    (`hr_6_trimestres`), nunca o `relatorio` (`hr_aproximado`). Duas razoes, as duas
    medidas antes de escolher:

    - **O comunicado sai no fechamento da reuniao; o relatorio sai 7 a 28 dias
      depois.** A coluna de uma reuniao pergunta o que o Comite publicou NAQUELE
      dia, e um numero de vintage posterior nao estava la.
    - **Espacamento.** Ate 2024-06 o horizonte relevante so existia no relatorio,
      que e trimestral: incluir aquele trecho poe no mesmo indice pontos separados
      por ~45 dias e por ~90, e o passo de uma coluna para a seguinte deixa de
      significar a mesma coisa nas duas metades. Medido: mediana de espacamento de
      84 dias com o trecho antigo dentro contra 45 sem ele, e a escala tipica de uma
      variacao de uma observacao dobra (0,297 p.p. contra 0,148), o que apagaria
      pela metade a cor de todo movimento da linha. De 2024-07 em diante o
      comunicado tem projecao em TODAS as reunioes, entao o que se perde e historia
      velha e o que se ganha e um indice em que uma posicao e uma reuniao.

    `cenario` e o de referencia -- condicionado ao caminho de juros da Focus --, que
    e o numero que o comunicado destaca. O detalhe dos outros filtros (documento,
    regime, cenario) esta na docstring de `_load_projecoes`, em `generate_report.py`.
    """
    global _PROJ_BC
    if _PROJ_BC is None:
        d = q("macro_brasil",
              "SELECT vintage, date, value FROM pm_copom_projecoes "
              "WHERE horizonte_relevante=1 AND indice='ipca' "
              "AND cenario='juros_esperado' AND documento='comunicado' "
              "AND regime='hr_6_trimestres' ORDER BY vintage")
        d["vintage"] = pd.to_datetime(d["vintage"])
        d["date"] = pd.to_datetime(d["date"])
        _PROJ_BC = (d.drop_duplicates("vintage", keep="last")
                     .set_index("vintage").sort_index())
    return _PROJ_BC


def proj_bc_hr() -> pd.Series:
    """Indexada pela data do COMUNICADO, que e quando o numero passou a existir."""
    return _proj_bc()["value"].astype(float)


def proj_bc_hr_alvo() -> dict:
    """{data do comunicado: trimestre projetado} -- o rotulo que vai embaixo do valor.

    O indice da serie e quando o numero saiu; o periodo que ele descreve e outro, e
    e esse que responde "sobre o que e este 3,2". Por isso esta linha e a unica em
    que o rotulo de referencia NAO identifica a observacao: duas reunioes seguidas
    projetam o mesmo trimestre com numeros diferentes.
    """
    return {i: _rotulo_ref(pd.Period(v, freq="Q"))
            for i, v in _proj_bc()["date"].items()}


def focus_selic_ponto(h: float) -> pd.Series:
    """Selic esperada interpolada no horizonte `h` ANOS, por data de pesquisa.

    Mesma mecanica de `focus_selic_12m_diario()` do modelo_painel -- inclusive a ancora em
    h=0 na Selic corrente, que aqui nao e detalhe: a curva anual do Focus comeca no ano
    corrente, e no fim de setembro isso ja e h=0,29. Sem a ancora, qualquer ponto pedido
    abaixo disso devolve vazio, e a media de 0,25 a 2,00 anos nao existiria.
    """
    d = focus_anual()
    d = d[d["indicador"] == "Selic"].copy()
    sel = serie("macro_international", "diferenciais_juros", "selic")
    sel_m = sel.reindex(pd.date_range(sel.index.min(), "2035-12-01", freq="MS")).ffill()
    mes = d["date"].values.astype("datetime64[M]").astype("datetime64[ns]")
    d["i0"] = sel_m.reindex(pd.DatetimeIndex(mes)).values
    out = {}
    for data, g in d.groupby("date"):
        g = g[g["h"] > 0].sort_values("h")
        if g.empty or not np.isfinite(g["i0"].iloc[0]) or g["h"].max() < h:
            continue
        out[data] = float(np.interp(h, np.r_[0.0, g["h"].values],
                                    np.r_[g["i0"].iloc[0], g["mediana"].values]))
    return pd.Series(out).sort_index()


def juro_real_focus_2a() -> pd.Series:
    """Juro real de 2 anos implicito na Focus, para ficar ao lado da NTN-B de 2 anos.

    A NTN-B de 24M e uma taxa MEDIA sobre dois anos, entao a contraparte da Focus tem de
    ser media tambem -- e nao o juro real a termo em h=2, que e o que sairia de repetir a
    receita de 12 meses da versao anterior desta aba com outro horizonte. As duas leituras sao
    legitimas e nao sao a mesma: por isso esta linha e media e o cartao de definicao diz.

    Selic media esperada: a curva anual do Focus lida em 0,25/0,50/.../2,00 ano e mediada
    -- a discretizacao da propria interpolacao, nao uma escolha nova. IPCA acumulado em 2
    anos: oito trimestres da Focus trimestral, compostos e anualizados. Real por Fisher
    exato, nao subtracao (ver `implicita()` para a razao).
    """
    hs = np.arange(0.25, 2.001, 0.25)
    sel = pd.DataFrame({h: focus_selic_ponto(h) for h in hs}).dropna().mean(axis=1)

    d = _focus_tri_ipca()
    ipca = {}
    for data, g in d.groupby("date"):
        # Oito trimestres a partir do TRIMESTRE DA PESQUISA, ele incluido: e ate onde o
        # painel trimestral da Focus alcanca (medido -- a pesquisa de set/2026 publica
        # 3/2026 a 2/2028) e e a janela honesta de "os proximos dois anos" para quem esta
        # dentro do trimestre corrente.
        base = pd.Period(data, freq="Q")
        janela = [base + k for k in range(0, 8)]
        m = g.set_index("tri")["mediana"]
        if not all(t in m.index for t in janela):
            continue
        acum = float(np.prod([1.0 + m.loc[t] / 100.0 for t in janela]))
        ipca[data] = (acum ** 0.5 - 1.0) * 100.0
    pi = pd.Series(ipca).sort_index()

    j = pd.DataFrame({"i": sel, "p": pi}).dropna()
    return ((1.0 + j["i"] / 100.0) / (1.0 + j["p"] / 100.0) - 1.0) * 100.0


# ── especificacao das variaveis ──────────────────────────────────────────────
# `sinal`: +1 subir e hawkish, -1 subir e dovish, 0 sem leitura hawk/dove.
# `grupo`: grupo do calendario quando a serie e indexada por periodo de REFERENCIA;
#          None quando o indice ja e a data em que o dado existiu (mercado/Focus).
# `grupo_agenda`: so para a agenda -- a serie e lida por data (grupo=None), mas a
#          divulgacao dela ainda e um evento agendado. E o caso da Focus: o indice e a
#          data da pesquisa, e mesmo assim o Boletim tem dia e hora no calendario.
# `modo`: 'pct' quando a variavel e um NIVEL de preco e o que importa e a variacao
#          proporcional (cambio). Muda o delta e o sigma, nao o valor exibido.
def _spec(ctx):
    a0, a1, a2 = ctx["ano0"], ctx["ano0"] + 1, ctx["ano0"] + 2
    return [
        # ── Inflação ─────────────────────────────────────────────────────────
        dict(key="bc_hr", bloco="Inflação",
             label="Projeção BC — Horizonte Relevante",
             unidade="%", sinal=+1, grupo=None, casas=1,
             fn=proj_bc_hr, ref_map=proj_bc_hr_alvo, div_hora=HORA_DECISAO,
             nota="A inflação que o próprio Banco Central projeta para o horizonte "
                  "relevante — os quatro trimestres que terminam seis trimestres à "
                  "frente —, no cenário condicionado ao caminho de juros da Focus. "
                  "Sai no comunicado, no fim do segundo dia da reunião, então cada "
                  "coluna traz o número daquela decisão e o trimestre projetado "
                  "aparece embaixo. A coluna da próxima reunião repete o último "
                  "publicado: a projeção seguinte só passa a existir com o "
                  "comunicado dela."),
        dict(key="ipca12", bloco="Inflação", label="IPCA Acumulado 12m",
             unidade="%", sinal=+1, grupo="ibge_ipca", casas=2,
             fn=lambda: acum12("ipca"),
             nota="Variação acumulada em 12 meses do IPCA cheio, o índice sobre o qual a "
                  "meta é definida."),
        dict(key="nucleos", bloco="Inflação",
             label="Núcleos (média de 5) — mm3m anualizada",
             unidade="% a.a.", sinal=+1, grupo="ibge_ipca", casas=2,
             fn=nucleos_mm3m,
             nota="Média simples de EX0, EX3, médias aparadas com suavização, dupla "
                  "ponderação e P55 — os cinco que o Banco Central acompanha no Relatório "
                  "de Política Monetária. Média de três meses anualizada, sobre a série "
                  "dessazonalizada por STL com fatores congelados: é a leitura de margem, "
                  "que responde antes do acumulado em 12 meses."),
        dict(key="focus_ipca_t", bloco="Inflação", label="E - Inflação Ano (T)",
             unidade="%", sinal=+1, grupo=None, grupo_agenda="bcb_focus", casas=2,
             fn=lambda: focus_anual_serie("IPCA", a0),
             nota="Mediana do Boletim Focus para o IPCA do ano-calendário corrente (%d)."
                  % a0),
        dict(key="focus_ipca_t1", bloco="Inflação", label="E - Inflação Ano (T+1)",
             unidade="%", sinal=+1, grupo=None, grupo_agenda="bcb_focus", casas=2,
             fn=lambda: focus_anual_serie("IPCA", a1),
             nota="Mediana do Focus para %d. Mais perto do horizonte em que a política "
                  "monetária de hoje ainda age do que o ano corrente." % a1),
        dict(key="focus_ipca_t2", bloco="Inflação", label="E - Inflação Ano (T+2)",
             unidade="%", sinal=+1, grupo=None, grupo_agenda="bcb_focus", casas=2,
             fn=lambda: focus_anual_serie("IPCA", a2),
             nota="Mediana do Focus para %d. É a leitura mais próxima de expectativa "
                  "ancorada: o que o mercado projeta quando nenhum choque corrente "
                  "alcança mais o período." % a2),
        dict(key="focus_ipca_hr", bloco="Inflação",
             label="E - Inflação Horizonte Relevante",
             unidade="%", sinal=+1, grupo=None, grupo_agenda="bcb_focus", casas=2,
             fn=focus_ipca_hr,
             nota="Inflação acumulada nos quatro trimestres que terminam seis trimestres "
                  "à frente — o horizonte que o Comitê persegue desde o Decreto "
                  "12.079/2024, e por isso a linha mais comparável à própria projeção do "
                  "Banco Central. Montada dos trimestres do Focus, compostos; a janela é "
                  "rolante, então não encurta ao longo do ano como a do ano-calendário."),
        dict(key="bei2", bloco="Inflação", label="Inflação Implícita 02Y",
             unidade="%", sinal=+1, grupo=None, casas=2,
             fn=lambda: implicita("24M"),
             nota="O que o mercado precifica de inflação para os próximos dois anos: o "
                  "juro nominal da curva de DI dividido pelo juro real da NTN-B no mesmo "
                  "vértice. Diferente da Focus, que é pesquisa — aqui alguém tem dinheiro "
                  "no preço."),
        dict(key="bei10", bloco="Inflação", label="Inflação Implícita 10Y",
             unidade="%", sinal=+1, grupo=None, casas=2,
             fn=lambda: implicita("120M"),
             nota="Mesma conta no vértice de dez anos. Nesse prazo quase nada do ciclo "
                  "corrente sobrevive, então o que se lê é o quanto o mercado acredita no "
                  "regime de metas."),

        # ── Atividade ────────────────────────────────────────────────────────
        dict(key="ibcbr12", bloco="Atividade", label="IBC-BR (Crescimento 12m)",
             unidade="%", sinal=+1, grupo="bcb_ibcbr", casas=2,
             fn=ibcbr_12m,
             nota="Índice de atividade do Banco Central, proxy mensal do PIB, acumulado "
                  "em 12 meses contra os 12 anteriores. Atividade mais forte fecha o "
                  "hiato e pressiona a inflação — leitura hawkish."),
        dict(key="focus_pib_t", bloco="Atividade", label="E - PIB Ano (T)",
             unidade="%", sinal=+1, grupo=None, grupo_agenda="bcb_focus", casas=2,
             fn=lambda: focus_anual_serie("PIB Total", a0),
             nota="Mediana do Focus para o crescimento do PIB em %d. O ano corrente ja "
                  "esta quase todo determinado quando a decisao e tomada: o que esta "
                  "linha move e menos a politica de hoje e mais o diagnostico de quanto "
                  "de folga existe." % a0),
        dict(key="focus_pib_t1", bloco="Atividade", label="E - PIB Ano (T + 1)",
             unidade="%", sinal=+1, grupo=None, grupo_agenda="bcb_focus", casas=2,
             fn=lambda: focus_anual_serie("PIB Total", a1),
             nota="Mediana do Focus para %d — o crescimento que cai dentro do horizonte "
                  "em que a decisão de hoje ainda faz efeito." % a1),
        dict(key="pib_4t", bloco="Atividade", label="PIB (Crescimento 4T/4T)",
             unidade="%", sinal=+1, grupo="ibge_pib_trimestral", casas=2,
             fn=lambda: pib_acum_4t("pib_pm"),
             nota="Taxa acumulada em quatro trimestres publicada pelo próprio IBGE. Dado "
                  "trimestral: entre uma divulgação e a seguinte a linha repete o último "
                  "número, e as reuniões sem dado novo ficam sem cor."),
        dict(key="pib_consumo", bloco="Atividade", label="PIB - Consumo (Crescimento 4T/4T)",
             unidade="%", sinal=+1, grupo="ibge_pib_trimestral", casas=2,
             fn=lambda: pib_acum_4t("consumo_familias"),
             nota="Consumo das famílias, acumulado em quatro trimestres. É o componente "
                  "de demanda mais sensível a crédito e renda, e o que o juro alcança "
                  "primeiro."),
        dict(key="pib_fbcf", bloco="Atividade",
             label="PIB - Investimentos (Crescimento 4T/4T)",
             unidade="%", sinal=+1, grupo="ibge_pib_trimestral", casas=2,
             fn=lambda: pib_acum_4t("fbcf"),
             nota="Formação bruta de capital fixo, acumulada em quatro trimestres. É o "
                  "componente mais volátil da demanda e o mais sensível ao custo do "
                  "capital."),

        # ── Condições Financeiras ────────────────────────────────────────────
        dict(key="ptax", bloco="Condições Financeiras", label="PTAX",
             unidade="R$/US$", sinal=+1, grupo=None, casas=4, modo="pct",
             fn=lambda: serie("macro_brasil", "cmb_ptax", "ptax_venda"),
             nota="Fechamento diário do dólar. Depreciação é repasse para preços — "
                  "leitura hawkish. A variação é percentual e não em centavos: o repasse "
                  "é proporcional, e 10 centavos a 3,00 não são a mesma notícia que 10 "
                  "centavos a 6,00."),
        dict(key="juro_real_2a", bloco="Condições Financeiras",
             label="Juro Real 02Y - Ex ante", unidade="%", sinal=-1, grupo=None, casas=2,
             fn=lambda: curva_br("NTNBJS", "24M"),
             nota="Taxa da NTN-B de dois anos — juro real negociado em mercado, já "
                  "líquido da inflação que o preço embute. Sinal invertido: juro real "
                  "mais alto é política já mais apertada, logo argumento para cortar."),
        dict(key="juro_real_10a", bloco="Condições Financeiras",
             label="Juro Real 10Y - Ex ante", unidade="%", sinal=-1, grupo=None, casas=2,
             fn=lambda: curva_br("NTNBJS", "120M"),
             nota="Mesma taxa no vértice de dez anos. A ponta longa responde menos ao "
                  "ciclo e mais à percepção de solvência — quando ela sobe com a curta "
                  "parada, o que mudou não foi a política monetária."),
        dict(key="juro_real_focus_2a", bloco="Condições Financeiras",
             label="Juro Real 02Y (Focus)", unidade="%", sinal=-1, grupo=None,
             grupo_agenda="bcb_focus", casas=2,
             fn=juro_real_focus_2a,
             nota="O mesmo juro real de dois anos, mas pela pesquisa em vez do preço: "
                  "Selic média esperada nos próximos dois anos sobre o IPCA esperado no "
                  "mesmo prazo. A distância entre esta linha e a NTN-B é o prêmio que o "
                  "mercado cobra para carregar o risco — não é erro de uma das duas."),
        dict(key="cred_livre", bloco="Condições Financeiras",
             label="Credito Livre (%, 12m Real)", unidade="%", sinal=+1,
             grupo="bcb_credit_note", casas=2,
             fn=lambda: credito_real_12m("livre"),
             nota="Saldo de crédito com recursos livres, crescimento em 12 meses "
                  "descontada a inflação. É a parte da carteira cujo preço o juro básico "
                  "move — crédito acelerando é estímulo, leitura hawkish."),
        dict(key="cred_direcionado", bloco="Condições Financeiras",
             label="Credito Direcionado (%, 12m Real)", unidade="%", sinal=+1,
             grupo="bcb_credit_note", casas=2,
             fn=lambda: credito_real_12m("direcionado"),
             nota="Idem para o crédito direcionado, cuja taxa é fixada por regra e não "
                  "pelo mercado. Ele acelerando enquanto o livre desacelera é sinal de "
                  "que parte da carteira não está respondendo à política monetária."),

        # ── Condições Externas ───────────────────────────────────────────────
        dict(key="us_real_2a", bloco="Condições Externas",
             label="US - Juros Real 02Y - Ex ante", unidade="%", sinal=+1, grupo=None,
             casas=2, fn=lambda: us_juro_real(2),
             nota="Treasury de dois anos menos a inflação esperada para o mesmo prazo "
                  "(modelo do Fed de Cleveland). Juro real americano mais alto encarece o "
                  "capital para emergentes e pressiona o câmbio — leitura hawkish aqui. O "
                  "Tesouro americano não emite título indexado de dois anos, então este "
                  "vértice não tem taxa real negociada em mercado; ambos os vértices "
                  "desta seção usam o mesmo método para que a comparação entre eles seja "
                  "de prazo, não de metodologia."),
        dict(key="us_real_10a", bloco="Condições Externas",
             label="US - Juros Real 10Y - Ex ante", unidade="%", sinal=+1, grupo=None,
             casas=2, fn=lambda: us_juro_real(10),
             nota="Mesma conta no vértice de dez anos. Existe TIPS de dez anos e ele "
                  "daria outra leitura: contra o título negociado, esta construção erra "
                  "0,26 p.p. em média e 1,37 p.p. no pior mês (nov/2008, quando a "
                  "liquidez dos TIPS colapsou). O que se ganha em troca é as duas linhas "
                  "desta seção dizerem a mesma coisa."),
        dict(key="icbr", bloco="Condições Externas", label="IC-BR (%, m/m)",
             unidade="%", sinal=+1, grupo="bcb_icbr", casas=2,
             fn=icbr_mm,
             nota="Índice de Commodities Brasil, variação no mês. Em reais — então ele "
                  "carrega câmbio junto com o preço da commodity, que é exatamente o "
                  "canal pelo qual entra na inflação daqui."),
        dict(key="brent", bloco="Condições Externas", label="Brent",
             unidade="US$/bbl", sinal=+1, grupo=None, casas=2, modo="pct",
             fn=lambda: serie("macro_international", "comm_brent", "brent_usd"),
             nota="Primeiro futuro do Brent, fechamento diário. Insumo direto de "
                  "combustíveis e, por eles, dos preços administrados. Nível de preço: a "
                  "variação lida é percentual, pela mesma razão do câmbio."),
    ]


# ── montagem da matriz ───────────────────────────────────────────────────────
def _valor_em(s: pd.Series, corte, grupo_cal: dict | None, teto=None,
              div_hora: dt.time | None = None) -> dict:
    """Leitura da serie `s` no corte, com a divulgacao que a justifica.

    `grupo_cal` None -> a serie e indexada pela data em que o dado existiu; corte direto.
    Caso contrario o indice e periodo de REFERENCIA e a data de divulgacao decide.

    `div_hora` so se aplica ao primeiro caso, e diz que aquele indice nao e so a
    data em que o dado existiu: e a data em que ele foi PUBLICADO, aquela hora. Vale
    para o comunicado do Copom e nao vale para a Focus, cujo indice e a data de
    referencia da pesquisa e cujo boletim sai na segunda seguinte -- afirmar
    publicacao ali seria inventar uma data.
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
        quando = (dt.datetime.combine(pd.Timestamp(ref).date(), div_hora)
                  if div_hora is not None else None)
        return {"valor": float(s.loc[ref]), "ref": ref, "pos": int(s.index.get_loc(ref)),
                "exata": True, "pendente": False,
                "divulgacao": quando.strftime("%d/%m/%Y %H:%M") if quando else None}

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


def _por_ano(idx) -> int:
    """Observacoes por ano do indice -- 12 num PeriodIndex mensal, 4 num trimestral."""
    f = str(getattr(idx, "freqstr", "") or "")
    return 4 if f.startswith("Q") else 12


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
        corte = d.index.max() - _por_ano(d.index) * ANOS_SIGMA
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
    """Rotulo curto do periodo de REFERENCIA, o que aparece embaixo do valor."""
    if ref is None:
        return "—"
    if isinstance(ref, pd.Period):
        if str(ref.freqstr).startswith("Q"):
            return "%dT%d" % (ref.quarter, ref.year)
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


def montar(agora: dt.datetime | None = None, n_passadas: int = N_PASSADAS) -> dict:
    """A matriz: uma linha por variavel, uma coluna por reuniao."""
    agora = agora or dt.datetime.now()
    hoje = agora.date()

    # n_passadas + 1: a coluna mais antiga EXIBIDA precisa de uma anterior para ter
    # delta. Sem ela a primeira coluna nunca receberia cor, o que nao e uma propriedade
    # do dado -- e so o fim da janela.
    janela = janela_reunioes(agora, n_passadas + 1)
    if len(janela) < 2:
        return {"erro": "calendario/banco sem reunioes suficientes para a janela -- ver "
                        "domain/release_calendar/ROLLOVER.md"}
    prox = janela[-1] if janela[-1]["futura"] else None
    if prox is None:
        return {"erro": "nenhuma reuniao futura no calendario -- ver "
                        "domain/release_calendar/ROLLOVER.md"}

    ctx = {"hoje": hoje, "ano0": hoje.year}
    gs = grupos()
    especificacao = _spec(ctx)

    blocos: dict[str, list] = {}
    ordem_blocos: list[str] = []
    avisos: list[str] = []
    rotulos: dict[str, list[str]] = {}

    for spec in especificacao:
        linha = {"key": spec["key"], "bloco": spec["bloco"], "label": spec["label"],
                 "unidade": spec["unidade"], "sinal": spec["sinal"],
                 "casas": spec["casas"], "nota": spec["nota"],
                 "grupo": spec["grupo"], "pct": spec.get("modo") == "pct"}
        if spec["bloco"] not in blocos:
            blocos[spec["bloco"]] = []
            ordem_blocos.append(spec["bloco"])
        blocos[spec["bloco"]].append(linha)

        for g in (spec["grupo"], spec.get("grupo_agenda")):
            if g:
                rotulos.setdefault(g, []).append(spec["label"])

        try:
            s = spec["fn"]().dropna()
        except Exception as exc:
            linha["erro"] = str(exc)
            avisos.append("%s: %s" % (spec["key"], exc))
            continue
        if s.empty:
            linha["erro"] = "serie vazia"
            continue
        s = s[~s.index.duplicated(keep="last")].sort_index()

        g = gs.get(spec["grupo"]) if spec["grupo"] else None
        teto = s.index.max() if g is not None else None
        leituras = [_valor_em(s, r["corte"], g, teto, spec.get("div_hora"))
                    for r in janela]

        # `ref_map` troca o rotulo impresso embaixo do valor: onde ele existe, o
        # indice da serie e a data de PUBLICACAO e o periodo descrito e outro.
        # Marcar a linha importa porque isso quebra a equivalencia que vale em todas
        # as outras -- la `novo` e a troca do rotulo de referencia sao a mesma coisa,
        # e aqui nao sao: duas reunioes seguidas projetam o mesmo trimestre.
        alvos = spec.get("ref_map")
        alvos = alvos() if callable(alvos) else alvos
        if alvos:
            linha["ref_alvo"] = True

        erro_fit = regra(g)[2] if (g is not None and regra(g)) else None
        linha["fit_erro_dias"] = erro_fit

        celulas = []
        for i in range(1, len(janela)):
            ant, cur, reuniao = leituras[i - 1], leituras[i], janela[i]
            cel = {
                "v": None if cur["valor"] is None else round(cur["valor"], 6),
                "ref": (alvos or {}).get(cur["ref"]) or _rotulo_ref(cur["ref"]),
                "div": cur["divulgacao"],
                "exata": bool(cur["exata"]),
                "pendente": bool(cur["pendente"]),
                "novo": False, "z": None, "delta": None, "k": 0,
            }
            if cur["valor"] is not None and ant["valor"] is not None:
                k = cur["pos"] - ant["pos"]
                cel["k"] = int(k)
                cel["novo"] = bool(k > 0)
                if k > 0:
                    if spec.get("modo") == "pct" and ant["valor"] and bool((s > 0).all()):
                        delta = (cur["valor"] / ant["valor"] - 1.0) * 100.0
                        sigma = _sigma(np.log(s) * 100.0, k)
                    else:
                        delta = cur["valor"] - ant["valor"]
                        sigma = _sigma(s, k)
                    cel["delta"] = round(delta, 6)
                    cel["sigma"] = None if sigma is None else round(sigma, 6)
                    if spec["sinal"] and sigma:
                        cel["z"] = round(float(np.clip(spec["sinal"] * delta / sigma,
                                                       -3, 3)), 4)
            # Uma data ESTIMADA so e perigosa quando cai perto do corte: se a regra erra
            # ate E dias e a divulgacao estimada esta a mais de E dias da reuniao, a
            # resposta e a mesma com ou sem o erro. Marcar sempre seria ruido; marcar
            # quando o erro pode virar a celula e informacao.
            if (not cur["exata"]) and cur["divulgacao"] and erro_fit:
                quando = dt.datetime.strptime(cur["divulgacao"], "%d/%m/%Y %H:%M")
                if abs((quando - reuniao["corte"]).days) <= erro_fit:
                    cel["ambigua"] = True
                    avisos.append(
                        "%s (%s): divulgacao estimada em %s, a menos de %d dias do corte "
                        "%s, e a regra de %s erra ate %d dias -- a celula pode estar no "
                        "periodo errado"
                        % (spec["key"], reuniao["label"], cur["divulgacao"], erro_fit,
                           reuniao["corte"].strftime("%d/%m/%Y %H:%M"), spec["grupo"],
                           erro_fit))
            celulas.append(cel)
        linha["celulas"] = celulas
        linha["ultimo_banco"] = ((alvos or {}).get(s.index.max())
                                 or _rotulo_ref(s.index.max()))

    return {
        "hoje": hoje.isoformat(),
        "reunioes": [
            {"date": r["date"].isoformat(),
             "date_start": r["date_start"].isoformat() if r["date_start"] else None,
             "numero": r["numero"], "label": r["label"],
             "bps": r["bps"], "decisao": r["decisao"], "selic": r["selic"],
             "futura": r["futura"],
             "corte": r["corte"].strftime("%d/%m/%Y %H:%M"),
             "dias": (r["date"] - hoje).days if r["futura"] else None}
            for r in janela[1:]
        ],
        "blocos": [{"nome": b, "linhas": blocos[b]} for b in ordem_blocos],
        "agenda": agenda({"corte": prox.get("corte_reuniao", prox["corte"])},
                         hoje, rotulos),
        "avisos": avisos,
        "anos_sigma": ANOS_SIGMA,
        "n_passadas": n_passadas,
    }


if __name__ == "__main__":
    d = montar()
    if "erro" in d:
        raise SystemExit(d["erro"])
    cols = d["reunioes"]
    larg = 9
    cab = "%-42s" % "variavel"
    for r in cols:
        cab += ("%*s" % (larg, r["label"]))
    print(cab)
    print("%-42s" % "" + "".join("%*s" % (larg, ("—" if r["bps"] is None
                                                 else "%+dbp" % r["bps"]))
                                 for r in cols))
    print("-" * len(cab))
    for b in d["blocos"]:
        print("\n== %s" % b["nome"])
        for l in b["linhas"]:
            if l.get("erro"):
                print("%-42s  FALHOU: %s" % (l["label"][:42], l["erro"]))
                continue
            f = "%%.%df" % l["casas"]
            linha = "%-42s" % l["label"][:42]
            for c in l["celulas"]:
                txt = "—" if c["v"] is None else f % c["v"]
                if c["novo"] and c["z"] is not None:
                    txt += "*" if abs(c["z"]) > 0.5 else "."
                linha += "%*s" % (larg, txt)
            print(linha)
    print("\n%d divulgacoes ate a proxima reuniao" % len(d["agenda"]))
    if d["avisos"]:
        print("%d aviso(s):" % len(d["avisos"]))
        for a in d["avisos"][:6]:
            print("  - %s" % a)
