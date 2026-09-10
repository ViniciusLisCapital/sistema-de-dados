"""
ETL da estrutura a termo de juros do Brasil -> macro_brasil.br_interest_rate.

Fonte: TaxaSwap.txt do arquivo de pregao da B3, via connectors/b3_curvas.py --
que e onde vivem o formato, a URL e o racional da troca de fonte. Tres curvas:
DIPRE (DI x pre), PREJS (NTN-F) e NTNBJS (NTN-B).

Historia curta: ate 2026-09-03 esta serie era escrita pelo projeto
CentralManagement em base_mercado.interest_rates, interpolando sobre os titulos
ofertados no Tesouro Direto com extrapolacao livre. As 106.308 linhas herdadas
foram DESCARTADAS e nao migradas -- o defeito nao era pontual, era a fonte
(ver connectors/b3_curvas.py). A tabela antiga continua existindo e o dado
antigo e recuperavel de la, se alguem precisar comparar.

## O guarda roda na carga, nao depois

`problemas_do_pregao()` afirma seis coisas sobre cada pregao antes de gravar.
Todos os limiares foram medidos nos 5.115 pregoes reconstruidos, com o extremo
observado ao lado de cada constante -- nenhum e escolhido a olho. A ordem das
checagens e proposital: a de grade vem primeiro porque e a unica que e
invariante em vez de limiar, e e a que pega a causa raiz dos dois defeitos
historicos.

Um pregao com problema NAO bloqueia a carga: ele e gravado e reportado. A
razao e que dois dos flags conhecidos sao ausencia legitima da fonte
(2020-05-07 sem curva de titulo; 2009-05-27 com a NTN-B em 43 vertices em vez
de ~114), e abortar por causa deles pararia um passe correto. Quem decide e
quem le o log.

Testes em tests/test_curvas_juros_b3.py, incluindo os dois defeitos reais como
controle positivo e a serie inteira como controle negativo.

## Por que o nome tem prefixo de PAIS e nao de tema

Contraria a convencao de prefixo tematico do resto do banco (`cmb_`, `inflc_`,
`atv_`...), e e deliberado: as tres tabelas de estrutura a termo se chamavam
`interest_rate` nos tres schemas, e o registry mapeia **tabela -> modulo sem o
schema**. Com o nome repetido, o dia em que a segunda ganhasse loader as duas
disputariam a mesma chave do registry -- em silencio, porque `_varrer()` faz
`mapa[tabela] = dotted` e a ultima varrida ganha. Renomeadas em 2026-09-03 para
`br_interest_rate` / `us_interest_rate` / `inter_interest_rate` por decisao do
usuario, o que resolve a colisao na raiz em vez de contorna-la com _OVERRIDES.

Banco: macro_brasil.br_interest_rate -- PRIMARY KEY (date, curve, tenor)
"""

from __future__ import annotations

import logging

import pandas as pd

from connectors.b3_curvas import (
    CODIGOS,
    DIAS_POR_MES,
    VERTICES,
    baixar_muitos,
    grades,
    nos_vertices,
)
from connectors.bis import BIS
from connectors.mysql import insert_data_into_database

logger = logging.getLogger(__name__)

_DATABASE = "macro_brasil"
_TABLE = "br_interest_rate"

# Primeiro pregao da serie. A B3 publica desde 2004, mas 2006-01-02 e onde a
# serie antiga comecava e foi mantido para as duas serem comparaveis.
_INICIO = "2006-01-02"

# Janela do passe de rotina. 10 dias uteis cobre feriado longo com folga; o
# upsert (ON DUPLICATE KEY UPDATE) torna reescrever os dias ja gravados
# inofensivo, e e o que permite pegar uma revisao da fonte sem passe cheio.
_DIAS_ROTINA = 10


# ---------------------------------------------------------------------------
# Limiares do guarda -- todos medidos nos 5.115 pregoes reconstruidos
# ---------------------------------------------------------------------------

# Piso/teto do valor. As curvas nominais nunca chegaram perto de 1% (minimos
# observados: DIPRE 1,866 e PREJS 1,950, ambos em 2020-2021 com Selic a 2,00%).
# A curva REAL vai a negativo de verdade -- minimo observado -5,423 no 3M em
# marco/2021 -- entao ela tem piso proprio: um piso positivo aqui reprovaria
# dado correto.
_PISO_NOMINAL = 1.0      # obs. 1,866
_PISO_REAL = -9.0        # obs. -5,423
_TETO = 30.0             # obs. 21,079

# Banda do breakeven implicito, (1+DIPRE)/(1+NTNBJS)-1 no mesmo vertice. Folga
# de ~3 p.p. sobre o extremo observado em 20 anos. A ponta curta e larga porque
# breakeven curto negativo EXISTE -- em maio/2020 o 9M deu -1,00% com dado bom,
# e o IPCA de fato deflacionou naquele trimestre.
_BANDA_BREAKEVEN = {         # tenor: (piso, teto)   # (min, max) observados
    "3M": (-9.0, 16.0),     # (-6,12 / +12,81)
    "6M": (-6.0, 15.0),     # (-2,61 / +11,34)
    "9M": (-4.0, 14.0),     # (-1,00 / +10,29)
    "12M": (-2.0, 13.0),    # (+0,73 /  +9,40)
    "24M": (0.0, 13.0),     # (+1,78 /  +9,86)
    "60M": (1.0, 12.0),     # (+3,38 /  +9,16)
    "120M": (1.0, 12.0),    # (+3,55 /  +8,74)
    "240M": (1.0, 12.0),    # (+3,63 /  +8,58)
}

# Salto entre pregoes CONSECUTIVOS (ate 4 dias corridos, para nao acusar
# feriado longo), so nos vertices de 24M ou mais -- o curto e volatil por
# natureza: o 3M da NTN-B carrega a defasagem do IPCA e tem p999 de 2,7 p.p.
# com dado bom, entao um limiar la acusaria movimento legitimo.
_SALTO_MAX = {"DIPRE": 2.5, "PREJS": 2.5, "NTNBJS": 2.0}   # obs. 1,822/1,770/1,208

# Piso de vertices no arquivo da fonte. Pega quebra de formato ou resposta
# throttled que parseia parcialmente. Minimos observados: DIPRE 65, NTNBJS 101,
# PREJS 11 -- os pisos abaixo tem folga grande de proposito, porque a fonte
# genuinamente afina em 2009 (a NTN-B saiu com 43 vertices em 2009-05-27).
_PISO_VERTICES = {"DIPRE": 40, "PREJS": 6, "NTNBJS": 40}


def problemas_do_pregao(grade, publicado, anterior=None, dias_desde_anterior=1):
    """Lista os problemas de um pregao. Vazio = passou.

    Args:
        grade: {curva: [(dias_corridos, taxa), ...]} -- a grade CRUA da fonte,
            por curva ja mapeada para o nome do nosso schema. E o insumo que
            permite a checagem que importa: se o alvo cai dentro dela ou nao.
        publicado: {(curva, tenor): valor} -- o que a extracao vai gravar.
        anterior: {(curva, tenor): valor} do pregao anterior, ou None.
        dias_desde_anterior: dias corridos ate o pregao anterior. Acima de 4 a
            checagem de salto e omitida -- feriado longo nao e distorcao.
    """
    p = []
    meses = {f"{m}M": m for v in VERTICES.values() for m in v}

    # (1) INVARIANTE: o alvo tem de cair dentro da grade publicada pela fonte.
    #     Sem isto, vertice sem titulo que o sustente vira reta esticada. E a
    #     causa raiz dos dois defeitos, de 2010 e de 2026.
    for (curva, tenor), _valor in sorted(publicado.items()):
        g = grade.get(curva)
        if not g or len(g) < 2:
            p.append(f"{curva}: grade ausente ou com menos de 2 vertices")
            continue
        alvo = meses[tenor] * DIAS_POR_MES
        lo, hi = min(d for d, _ in g), max(d for d, _ in g)
        if alvo < lo or alvo > hi:
            p.append(f"{curva}@{tenor}: alvo {alvo:.0f}d fora da grade da fonte "
                     f"[{lo}, {hi}] -- seria extrapolacao nossa")

    # (2) Numero de vertices na fonte, contra quebra de formato / parse parcial.
    for curva, g in grade.items():
        piso = _PISO_VERTICES.get(curva)
        if piso is not None and len(g) < piso:
            p.append(f"{curva}: {len(g)} vertices na fonte, piso {piso}")

    # (3) Valor implausivel. Pega cotacao placeholder da fonte -- o caso de 2010
    #     entrou como Taxa Compra 0,00 / Venda 0,06, media 0,03.
    for (curva, tenor), v in sorted(publicado.items()):
        piso = _PISO_REAL if curva == "NTNBJS" else _PISO_NOMINAL
        if v < piso or v > _TETO:
            p.append(f"{curva}@{tenor}: valor {v:.3f} fora de [{piso}, {_TETO}]")

    # (4) Grade degenerada: os vertices curtos nao podem sair todos iguais.
    #     Em 17/08/2026 a NTN-B saiu com 8,200 em 3M, 6M, 9M, 12M, 24M e 60M.
    curtos = ["3M", "6M", "9M", "12M", "24M", "60M"]
    for curva in CODIGOS.values():
        vals = [round(publicado[(curva, t)], 3) for t in curtos
                if (curva, t) in publicado]
        if len(vals) >= 3 and len(set(vals)) == 1:
            p.append(f"{curva}: {len(vals)} vertices curtos com valor identico "
                     f"({vals[0]:.3f}) -- grade degenerada")

    # (5) Breakeven implicito entre a curva nominal de DI e a real.
    for tenor, (lo, hi) in _BANDA_BREAKEVEN.items():
        kn, kr = ("DIPRE", tenor), ("NTNBJS", tenor)
        if kn in publicado and kr in publicado:
            be = ((1 + publicado[kn] / 100) / (1 + publicado[kr] / 100) - 1) * 100
            if be < lo or be > hi:
                p.append(f"breakeven@{tenor}: {be:+.2f}% fora de [{lo}, {hi}]")

    # (6) Salto contra o pregao anterior, so nos vertices longos.
    if anterior and dias_desde_anterior <= 4:
        for (curva, tenor), v in sorted(publicado.items()):
            if meses[tenor] < 24:
                continue
            if (curva, tenor) in anterior:
                d = abs(v - anterior[(curva, tenor)])
                lim = _SALTO_MAX[curva]
                if d > lim:
                    p.append(f"{curva}@{tenor}: salto de {d:.3f} p.p. contra o "
                             f"pregao anterior (limite {lim})")

    return p


# ---------------------------------------------------------------------------
# Carga
# ---------------------------------------------------------------------------

def _datas(full: bool, dias: int) -> list[pd.Timestamp]:
    fim = pd.Timestamp.today().normalize()
    if full:
        return list(pd.bdate_range(_INICIO, fim))
    return list(pd.bdate_range(end=fim, periods=dias))


def coletar(full: bool = False, dias: int = _DIAS_ROTINA):
    """Devolve (DataFrame pronto para a tabela, {data: [problemas]}).

    Separado de run() para o teste poder exercitar a coleta e o guarda sem
    tocar no banco.
    """
    datas = _datas(full, dias)
    baixar_muitos(datas)

    linhas, avisos, sem_arquivo = [], {}, []
    anterior, data_anterior = None, None
    for d in datas:
        D = grades(d)
        if D is None:
            sem_arquivo.append(d.date())
            continue
        rows = nos_vertices(D, d)
        if not rows:
            sem_arquivo.append(d.date())
            continue

        grade = {curva: list(zip(D[D.cod == cod].dc, D[D.cod == cod].taxa))
                 for cod, curva in CODIGOS.items()}
        publicado = {(r[1], r[2]): r[4] for r in rows}
        dd = (d - data_anterior).days if data_anterior is not None else 99
        probs = problemas_do_pregao(grade, publicado, anterior, dd)
        if probs:
            avisos[d.date()] = probs

        linhas.extend(rows)
        anterior, data_anterior = publicado, d

    df = pd.DataFrame(linhas, columns=["date", "curve", "tenor", "tenor_years", "value"])
    if sem_arquivo:
        # Tres causas, todas legitimas e nenhuma erro nosso: feriado estadual de
        # SP (B3 fechada, 43 casos no historico), pregao sem curva de titulo
        # (2020-05-07), e o dia corrente antes de a B3 publicar -- ela solta o
        # arquivo depois do fechamento, entao um passe de manha sempre lista hoje.
        hoje = pd.Timestamp.today().normalize().date()
        pendentes = [d for d in sem_arquivo if d == hoje]
        outros = [d for d in sem_arquivo if d != hoje]
        if pendentes:
            logger.info("br_interest_rate: %s ainda nao publicado pela B3 (sai apos "
                        "o fechamento)", hoje)
        if outros:
            logger.info("br_interest_rate: %d pregoes sem arquivo na B3 (feriado "
                        "estadual de SP, ou pregao sem curva de titulo): %s%s",
                        len(outros), outros[:5], " ..." if len(outros) > 5 else "")
    return df, avisos


# ---------------------------------------------------------------------------
# A curva POLICY -- a taxa que o BC define, na mesma tabela que a curva
# ---------------------------------------------------------------------------
# Decisao explicita do usuario (2026-09-03): *"na tabela de interest rate
# coloque tambem a policy_rate descrita como tal. Assim centralizamos os dados
# de juros na mesma tabela, independente se ele e o dado da curva, ou dado
# definido pelo BC"*.
#
# A FONTE e o **BIS** (WS_CBPOL, via connectors/bis.py) e nao a SGS 432, e a
# escolha foi medida. As duas concordam em **10.027 dos 10.029 dias** que
# compartilham (99,98%); as 2 divergencias sao dias de reuniao do Copom
# (2001-07-18 e 2006-04-19), em que uma fonte lanca a taxa nova no dia da
# decisao e a outra no dia seguinte. Pesou a favor do BIS:
#
#   - e a MESMA definicao usada nas outras cinco economias, entao a curva
#     `POLICY` significa uma coisa so nos tres schemas;
#   - a SGS 432 devolve HTTP 406 acima de ~10 anos por requisicao, entao usa-la
#     exigiria maquinaria de blocos que o BIS nao precisa.
#
# Este script busca do BIS DIRETO desde 2026-09-03 (2a rodada do mesmo dia).
# Antes ele lia `macro_international.cmb_policy_rates`, o ETL do BIS -- e as
# duas tabelas passaram a guardar o mesmo numero. Medido: as 53.663 linhas de
# `cmb_policy_rates` eram reproduzidas **exatamente** (dif maxima 0,0, zero
# orfas dos dois lados) por esta curva mais a POLICY de
# `macro_international.inter_interest_rate`. O usuario pediu para eliminar a
# duplicacao, `cmb_policy_rates` foi removida, e o fetch veio para ca. A
# chamada ao connector aparece em dois scripts, mas com listas de paises
# DISJUNTAS (BR aqui, os outros cinco no international) -- codigo
# compartilhado, nao numero gravado duas vezes.
#
# Duas ressalvas que ficam registradas em vez de escondidas: o BIS comeca em
# **1994-07** e a meta Selic so existe desde **1999-03** (antes o instrumento
# eram a TBC e a TBAN), entao o trecho 1994-1999 desta curva e "taxa de
# politica" no conceito do BIS, nao meta Selic; e para precisao de dia de
# decisao a autoridade continua sendo `pm_copom_reuniao`, que cruza a SGS 432
# com o calendario de reunioes.
_POLICY_TENOR = "1d"
# 1 dia util em anos. Zero seria errado: `tenor_years` existe para interpolar e
# ordenar, e um vertice em zero quebra qualquer interpolacao ancorada no curto.
_POLICY_TENOR_YEARS = round(1 / 252, 6)
# Medido na serie inteira: 2,00 (2020-2021) a **173,23** (jul/1995, os primeiros
# meses do Real). O teto tem de cobrir isso -- um teto "razoavel" de 60 reprova
# os 145 dias anteriores a ago/1995, que sao dado correto. Desde o inicio da
# meta Selic em 1999-03 o maximo e 45,00.
_POLICY_PISO, _POLICY_TETO = 0.0, 250.0   # obs. 2,00 a 173,23
# Plano Real. O BIS cobre desde 1986-06 e o trecho anterior chega a
# ~790.799% a.a. -- truncar aqui e decisao explicita do usuario.
_POLICY_INICIO = "1994-07-01"

_bis = BIS()


def coletar_policy(full: bool = False, dias: int = _DIAS_ROTINA) -> pd.DataFrame:
    """A meta de politica monetaria como curva `POLICY`, vertice de 1 dia util.

    Busca do BIS (WS_CBPOL, diaria) -- ver o comentario acima para por que essa
    e a fonte e nao a SGS 432. Calendario proprio: a meta vigora todo dia
    corrido, inclusive fim de semana, enquanto as curvas da B3 so existem em
    pregao. Nao truncamos para o calendario da B3 (seria descartar informacao),
    o que significa que um `WHERE date = <sabado>` devolve so a POLICY.

    A janela de rotina e em dias CORRIDOS e o `dias` que chega e em dias uteis
    (a unidade do passe da B3), dai o fator. Generosa de proposito: o BIS
    republica em lote, com lag medido de 8 dias e ate 12 no pior caso, entao
    uma janela curta perderia revisao -- e como a insercao e upsert, reescrever
    dia que nao mudou nao custa nada.
    """
    start = None
    if not full:
        corte = (pd.Timestamp.today().normalize()
                 - pd.Timedelta(days=max(dias, 1) * 3 + 30))
        start = max(corte, pd.Timestamp(_POLICY_INICIO)).strftime("%Y-%m-%d")

    pr = _bis.get_policy_rates(countries=["BR"], freq="D", start=start)

    pr = pr.copy()
    pr["date"] = pd.to_datetime(pr["date"])
    pr["value"] = pr["value"].astype(float)
    # Truncagem no Plano Real, decisao explicita do usuario: o BIS cobre desde
    # 1986-06, mas ~790.799% a.a. em 1990 nao e comparavel com nada.
    pr = pr[pr["date"] >= _POLICY_INICIO]
    pr = pr.dropna(subset=["value"]).sort_values("date")

    fora = pr[(pr.value < _POLICY_PISO) | (pr.value > _POLICY_TETO)]
    if len(fora):
        raise ValueError(f"POLICY: {len(fora)} valores fora de "
                         f"[{_POLICY_PISO}, {_POLICY_TETO}]:\n{fora.head().to_string()}")

    return pd.DataFrame({
        "date": pr["date"].dt.date,
        "curve": "POLICY",
        "tenor": _POLICY_TENOR,
        "tenor_years": _POLICY_TENOR_YEARS,
        "value": pr["value"].round(8),
    })


def run(full: bool = False, dias: int = _DIAS_ROTINA) -> None:
    """Atualiza macro_brasil.br_interest_rate.

    Args:
        full: True recarrega de 2006-01-02 (~5.100 pregoes). O cache local em
              domain/db/brasil/b3/cache/ evita rebaixar; num cache vazio isto
              leva ~1h com os 2 workers que a B3 tolera.
        dias: dias uteis para tras no passe de rotina. Default 10.
    """
    df, avisos = coletar(full=full, dias=dias)

    # A POLICY entra DEPOIS do guarda de propósito: `problemas_do_pregao`
    # afirma sobre a interpolacao de uma grade, e a meta nao e interpolada de
    # nada -- passa-la pelo guarda faria a checagem de grade procurar um
    # vertice "1d" em VERTICES e levantar KeyError.
    policy = coletar_policy(full=full, dias=dias)
    if not policy.empty:
        df = pd.concat([df, policy], ignore_index=True)

    if df.empty:
        logger.warning("br_interest_rate: nada a inserir")
        return

    logger.info("br_interest_rate: %d linhas, %s -> %s (%d datas)",
                len(df), df["date"].min(), df["date"].max(), df["date"].nunique())
    for curva, g in df.groupby("curve"):
        logger.info("  %-7s %6d linhas, %d vertices, %s -> %s", curva, len(g),
                    g["tenor"].nunique(), g["date"].min(), g["date"].max())

    if avisos:
        logger.warning("br_interest_rate: %d pregoes com aviso do guarda de qualidade "
                       "(gravados de todo jeito -- ver o docstring do modulo)", len(avisos))
        for data, probs in sorted(avisos.items()):
            for msg in probs:
                logger.warning("  %s  %s", data, msg)

    insert_data_into_database(_DATABASE, _TABLE, df)
