"""Gera reports/brasil/Structural Model.html.

Seis abas: os insumos trimestrais, a curva de Phillips nos quatro grupos de preco do
BC, a equacao de expectativas, a curva IS, a regra de juros e o cambio. O relatorio
monta o painel DIRETO do MySQL a cada geracao -- nao ha artefato intermediario, porque
`panel.construir()` e so um punhado de consultas.

A aba de cambio e a unica que nao sai do painel: ela le o frame MENSAL do FX Report e
trimestraliza por cima (ver `equations/fx.py`), entao acrescenta ~15 consultas e a
serie diaria de PTAX ao custo da geracao.

Uso:
    uv run python -c "from analytics.brasil.structural_model.generate_report import run; run()"
"""
from __future__ import annotations

import datetime as dt
import math
from pathlib import Path

import pandas as pd

from analytics.brasil.monetary_policy import modelo_agregado as _mp_agregado
from analytics.brasil.structural_model import panel, simulator
from analytics.brasil.structural_model.equations import (
    expectations,
    fx,
    is_curve,
    phillips_sub,
    taylor,
)
from analytics.report_structure.builder import render_report

_HERE = Path(__file__).parent
_TEMPLATE = _HERE / "report.html"
_SAIDA = "reports/brasil/Structural Model.html"

_EIXO_INFL = "variação do trimestre, %"

# Uma entrada por insumo. `nome` e o rotulo curto que aparece na tela; `full` so entra
# no cartao de definicao quando acrescenta algo ao nome; `eixo` e a MESMA string que
# titula o eixo Y, para o cartao e o eixo nao divergirem.
INFO = {
    "pi_q": dict(
        nome="IPCA do trimestre",
        full="Índice Nacional de Preços ao Consumidor Amplo, variação no trimestre",
        desc="A inflação dos três meses do trimestre, encadeada. Não é o acumulado de "
             "doze meses: trimestres vizinhos não compartilham nenhum mês, e é isso que "
             "faz o peso da inflação passada medir inércia de preço em vez de medir a "
             "sobreposição de duas janelas. Não é explicada por nenhuma conta desta "
             "página — ela é o alvo que a soma dos quatro grupos tenta reproduzir.",
        eixo=_EIXO_INFL,
        fonte="IBGE, via Banco Central",
    ),
    "pi_is_q": dict(
        nome="Serviços",
        full="IPCA — serviços, preços livres, variação no trimestre",
        desc="Corte de bem mais de um terço do índice e o mais ligado ao mercado de "
             "trabalho: aluguel, alimentação fora de casa, escola, plano de saúde, salão. "
             "Preço de serviço é feito sobretudo de salário, então é aqui que o "
             "aquecimento da economia deveria aparecer primeiro.",
        eixo=_EIXO_INFL,
        fonte="IBGE, via Banco Central",
    ),
    "pi_ia_q": dict(
        nome="Alimentação",
        full="IPCA — alimentação no domicílio, preços livres, variação no trimestre",
        desc="Comida comprada para casa. É o corte mais volátil do índice, porque responde "
             "a safra, clima e ao preço internacional da soja, do café e da carne — coisas "
             "que não têm relação com a demanda interna.",
        eixo=_EIXO_INFL,
        fonte="IBGE, via Banco Central",
    ),
    "pi_ii_q": dict(
        nome="Bens industriais",
        full="IPCA — bens industriais, preços livres, variação no trimestre",
        desc="Produto de fábrica: carro, eletrodoméstico, roupa, remédio. É o corte mais "
             "exposto ao câmbio, porque parte do que se consome é importada e o resto é "
             "feito com insumo importado.",
        eixo=_EIXO_INFL,
        fonte="IBGE, via Banco Central",
    ),
    "pi_im_q": dict(
        nome="Monitorados",
        full="IPCA — preços administrados ou monitorados, variação no trimestre",
        desc="Preços que não saem de negociação livre: energia, combustível, ônibus, plano "
             "de saúde regulado, água, taxas. Seguem contrato, reajuste anual ou decisão de "
             "agência, e por isso costumam perseguir a inflação passada em vez de reagir à "
             "demanda.",
        eixo=_EIXO_INFL,
        fonte="IBGE, via Banco Central",
    ),
    "pi_e": dict(
        nome="Expectativa de inflação",
        full="Mediana das expectativas de mercado para o IPCA dos doze meses seguintes, série suavizada",
        desc="O que o mercado esperava de inflação para o ano seguinte, em média ao longo do "
             "trimestre. É a pesquisa semanal que o Banco Central faz com cerca de cem "
             "instituições. Vem em taxa anual e as contas usam um quarto dela, que é a parte "
             "que cabe num trimestre — sem isso a conta somaria um ano a três meses.",
        eixo="IPCA esperado para os 12 meses seguintes, % ao ano",
        fonte="Banco Central, pesquisa Focus",
    ),
    "hiato": dict(
        nome="Hiato do produto",
        full="Hiato do produto — cenário de referência",
        desc="Quanto a economia está produzindo acima ou abaixo do que consegue sustentar sem "
             "pressionar preços. Positivo é demanda acima da capacidade. Não é medido: é a "
             "estimativa que o próprio Banco Central publica, e ele a reescreve a cada "
             "trimestre — a série aqui é sempre a leitura mais recente, não o que ele dizia "
             "na época.",
        eixo="produto efetivo − potencial, % do potencial",
        fonte="Banco Central, anexo do Relatório de Política Monetária",
    ),
    "de": dict(
        nome="Câmbio",
        full="Variação do real por dólar (PTAX venda) no trimestre",
        desc="Positivo é real mais fraco. A conta usa a taxa média do trimestre, não o "
             "fechamento do último dia: o que pressiona preços é o câmbio que o importador "
             "enfrentou ao longo do trimestre inteiro.",
        eixo="variação da taxa média do trimestre, %",
        fonte="Banco Central, PTAX venda",
    ),
    "pi_agr_usd": dict(
        nome="Commodities agrícolas",
        full="Índice de Commodities Brasil — agropecuária, denominado em dólar",
        desc="O preço internacional, em dólar, da cesta agropecuária que pesa na inflação "
             "brasileira: soja, milho, café, carne, açúcar. Em dólar e não em real de "
             "propósito — a versão em real já embute o câmbio, que entra nas contas pela sua "
             "própria linha, e contá-lo duas vezes inflaria o repasse cambial.",
        eixo="variação da média do trimestre, %",
        fonte="Banco Central (série 29041)",
    ),
    "rr_2a": dict(
        nome="Juro real de 2 anos",
        full="Taxa de juro real de mercado para 2 anos, curva de NTN-B",
        desc="O juro acima da inflação que o mercado negocia hoje para os próximos dois "
             "anos, lido na curva dos títulos indexados ao IPCA. Dois anos é curto o "
             "bastante para o número refletir sobretudo o que se espera do Banco Central — "
             "quando o Copom aperta, é esta ponta que sobe.",
        eixo="taxa real de mercado, % ao ano",
        fonte="B3, curva de NTN-B do arquivo de pregão",
    ),
    "rr_10a": dict(
        nome="Juro real de 10 anos",
        full="Taxa de juro real de mercado para 10 anos, curva de NTN-B",
        desc="O mesmo para dez anos. A essa distância o ciclo de política já passou, então "
             "o número é feito da taxa que a economia sustenta no longo prazo mais o prêmio "
             "que o investidor cobra para carregar um papel tão longo. É por carregar esse "
             "prêmio que ele não serve sozinho como taxa de equilíbrio.",
        eixo="taxa real de mercado, % ao ano",
        fonte="B3, curva de NTN-B do arquivo de pregão",
    ),
    "g_rr": dict(
        nome="Aperto monetário",
        full="Inclinação da curva real: juro real de 2 anos menos o de 10 anos",
        desc="A medida de aperto que a curva IS usa. Positivo é política apertada: o juro "
             "de dois anos acima do de dez significa que o Banco Central está segurando a "
             "economia agora e o mercado espera que solte depois. Ela é a diferença entre "
             "dois preços observados no mesmo dia, então não depende de nenhuma estimativa "
             "de qual seria o juro de equilíbrio — que é justamente a conta que ninguém "
             "sabe fazer sem discordar.",
        eixo="juro real de 2 anos − de 10 anos, p.p.",
        fonte="B3, curva de NTN-B do arquivo de pregão",
    ),
    "pi_met_usd": dict(
        nome="Commodities metálicas",
        full="Índice de Commodities Brasil — metal, denominado em dólar",
        desc="O preço internacional, em dólar, dos metais: minério de ferro, alumínio, "
             "cobre, ouro. É o insumo que aparece do outro lado da cadeia dos bens de "
             "fábrica, e por isso entra na conta de bens industriais e não na de comida.",
        eixo="variação da média do trimestre, %",
        fonte="Banco Central (série 29040)",
    ),
}

INFO.update({
    "selic": dict(
        nome="Selic",
        full="Taxa Selic, meta definida pelo Copom — média do trimestre",
        desc="O juro que o Banco Central define. Entra pela média dos dias do "
             "trimestre, e não pelo valor do último dia, porque é a taxa que vigorou "
             "ao longo do trimestre que afeta a economia dele. A coluna paralela pelo "
             "fechamento existe no painel e não está desenhada aqui.",
        eixo="% ao ano",
        fonte="Banco Central, via BIS",
    ),
    "meta_12m": dict(
        nome="Meta de inflação (12 meses)",
        full="Meta de inflação do CMN no horizonte de doze meses",
        desc="A meta que vale para o horizonte de doze meses à frente, e não a do ano "
             "corrente. Como a meta é anual e o horizonte é móvel, ela é a mistura das "
             "metas de dois anos-calendário, pesada pelos meses que cada uma cobre. "
             "Está em 3,0% de forma contínua desde 2025.",
        eixo="% ao ano",
        fonte="Conselho Monetário Nacional, via Banco Central",
    ),
    "pi_e_2a": dict(
        nome="Expectativa de inflação (18 meses)",
        full="Expectativa de IPCA da pesquisa Focus, horizonte de 18 meses",
        desc="O que o mercado espera de inflação num horizonte mais longo que o de doze "
             "meses. O Banco Central publica esta série com o nome de <i>IPCA 24 meses "
             "à frente</i>: é a inflação acumulada em doze meses terminando daqui a "
             "vinte e quatro, então o centro dela está a dezoito meses — que é o "
             "horizonte de fato. A série publicada só começa em 2021, e a daqui é "
             "reconstruída da pesquisa anual, que vai a 2000.",
        eixo="% ao ano",
        fonte="Pesquisa Focus, Banco Central",
    ),
    "meta_24m": dict(
        nome="Meta de inflação (24 meses)",
        full="Meta de inflação do CMN no horizonte de 24 meses",
        desc="A mesma mistura de metas anuais da linha de doze meses, um ano adiante — "
             "é contra ela que a expectativa de dezoito meses é comparada, para que os "
             "dois lados da conta olhem o mesmo horizonte.",
        eixo="% ao ano",
        fonte="Conselho Monetário Nacional, via Banco Central",
    ),
    "pi_bcb": dict(
        nome="Projeção de IPCA do Copom",
        full="Projeção de IPCA do próprio Copom no horizonte relevante",
        desc="O que o comitê projetava de inflação no horizonte que ele mesmo declarava "
             "relevante, no cenário em que o juro segue o caminho esperado pelo mercado. "
             "É um vintage por reunião: cada ponto é o que ele publicou na época, não "
             "uma revisão posterior. Não entra em nenhuma conta desta página — está "
             "aqui como contraste com a expectativa do mercado.",
        eixo="% ao ano",
        fonte="Relatório de Política Monetária, Banco Central",
    ),
})

_ORDEM = ["pi_q", "pi_is_q", "pi_ia_q", "pi_ii_q", "pi_im_q",
          "pi_e", "hiato", "rr_2a", "rr_10a", "g_rr",
          "de", "pi_agr_usd", "pi_met_usd",
          "selic", "meta_12m", "pi_e_2a", "meta_24m", "pi_bcb"]

# Rotulo e definicao de cada grupo na aba do modelo. Reaproveita o texto do insumo
# correspondente, para os dois nao divergirem.
INFO_SUB = {
    "IS": dict(nome="Serviços", full=INFO["pi_is_q"]["full"], desc=INFO["pi_is_q"]["desc"]),
    "IA": dict(nome="Alimentação", full=INFO["pi_ia_q"]["full"], desc=INFO["pi_ia_q"]["desc"]),
    "II": dict(nome="Bens industriais", full=INFO["pi_ii_q"]["full"], desc=INFO["pi_ii_q"]["desc"]),
    "IM": dict(nome="Monitorados", full=INFO["pi_im_q"]["full"], desc=INFO["pi_im_q"]["desc"]),
}


def _ser(s: pd.Series) -> list:
    """Serie -> lista JSON, com None no lugar de NaN (JSON nao tem NaN)."""
    return [None if (v is None or (isinstance(v, float) and math.isnan(v))) else round(float(v), 4)
            for v in s]


def _iso(p: pd.Period) -> str:
    return p.start_time.strftime("%Y-%m-%d")


def _rot(p: pd.Period) -> str:
    return "%dT%d" % (p.year, p.quarter)


def _coef_lista(r: dict) -> list:
    """Coeficientes de uma equacao, no formato que a tela consome.

    `restrito` marca os pesos que dividem a soma-um com a expectativa -- a tela
    precisa saber quais para escrever de onde sai o peso da expectativa. `saz` marca
    as dummies de trimestre, que vao para a sua propria tabela.
    """
    eq = phillips_sub.EQUACOES[r["chave"]]
    restritos = {eq["inercia"]} | {p for p, _, _ in r["restritos"]}
    out = []
    for par in r["coef"]:
        if par in phillips_sub.SAZ:
            continue
        lp = r["longo_prazo"].get(par)
        out.append({
            "key": par,
            "rot": phillips_sub._rotulo(r["chave"], par),
            "b": round(float(r["coef"][par]), 6),
            "se": round(float(r["se"][par]), 6),
            "t": round(float(r["t"][par]), 2),
            "t_ols": round(float(r["t_ols"][par]), 2),
            "p": round(float(r["p"][par]), 4),
            "lp": round(float(lp), 6) if lp is not None else None,
            "restrito": par in restritos,
        })
    return out


def _load_sub(df: pd.DataFrame) -> dict:
    """As quatro equacoes na amostra comum, com dummies de trimestre e sem crise."""
    d = phillips_sub.montar(df)
    R = phillips_sub.estimar(d)
    S = phillips_sub.sem_sazonais(d)
    P = phillips_sub.leitura_12m(R)
    idx, i12 = R["idx"], P["idx"]

    eqs = {}
    for k in phillips_sub.ORDEM:
        r = R["equacoes"][k]
        eqs[k] = {
            "nome": r["nome"],
            "r2": round(r["r2"], 4),
            "rmse": round(r["rmse"], 4),
            "r2_sem_saz": round(S[k]["r2"], 4),
            "rmse_sem_saz": round(S[k]["rmse"], 4),
            "acf": [round(v, 3) for v in r["acf"]],
            "lb_q4": round(r["lb_q4"], 2), "lb_p4": round(r["lb_p4"], 4),
            "lb_q8": round(r["lb_q8"], 2), "lb_p8": round(r["lb_p8"], 4),
            "saz": [round(v, 6) for v in r["saz"]],
            "peso_e": round(float(r["peso_expectativa"]), 6),
            "coef": _coef_lista(r),
            "obs": _ser(r["obs"].reindex(idx)),
            "fit": _ser(r["fit"].reindex(idx)),
            "resid": _ser(r["resid"].reindex(idx)),
            "peso": _ser(d.loc[idx, panel.PESO_COL[k.lower()]] * 100.0),
            # a leitura de 12 meses: realizado e ajustado, os dois encadeados
            "obs12": _ser(P["eq"][k]["obs12"]),
            "aj12": _ser(P["eq"][k]["aj12"]),
            "rmse12": round(P["eq"][k]["rmse"], 4),
            "erro12": round(P["eq"][k]["erro_medio"], 4),
            "vies12": round(P["eq"][k]["vies"], 4),
            **INFO_SUB[k],
        }

    c, a = R["cheio"], R["erro_agregacao"]

    # As leituras de (IA). E o registro de um teste: a forma contemporanea ficou porque
    # as outras nao melhoram nada, e o Ljung-Box da base nao rejeita -- entao nao ha
    # autocorrelacao a modelar e o MA(1) nao e necessario.
    variantes = []
    for v, r in phillips_sub.comparar_ia(d).items():
        variantes.append({
            "key": v,
            "desc": phillips_sub.VARIANTES_IA[v]["desc"],
            "escolhida": v == R["variante_ia"],
            "r2": round(r["r2"], 4), "rmse": round(r["rmse"], 4),
            "lb_p4": round(r["lb_p4"], 4),
            "estimador": r["estimador"],
            "theta": round(float(r["theta"]), 4) if r["theta"] is not None else None,
            "theta_t": (round(float(r["theta"] / r["theta_se"]), 2)
                        if r["theta"] is not None else None),
            "coef": [x for x in _coef_lista(r) if x["key"] in ("ia2", "ia2b")],
        })

    # As ancoras de (IM). Todas negativas e nenhuma significativa: o registro de que o
    # defeito nao e o horizonte da indexacao.
    ancoras = []
    for a_key, r in phillips_sub.comparar_im(d).items():
        par = phillips_sub.EQUACOES["IM"]["restritos"][0][0]
        ancoras.append({
            "key": a_key,
            "desc": phillips_sub.ANCORAS_IM[a_key]["desc"],
            "escolhida": a_key == R["ancora_im"],
            "b": round(float(r["coef"][par]), 6),
            "t": round(float(r["t"][par]), 2),
            "peso_e": round(float(r["peso_expectativa"]), 6),
            "rmse": round(r["rmse"], 4),
        })

    return {
        "x": [_iso(p) for p in idx],
        "rot": [_rot(p) for p in idx],
        "hac_lags": phillips_sub.HAC_LAGS,
        "n": int(len(idx)),
        "ini": _rot(idx[0]),
        "fim": _rot(idx[-1]),
        "ordem": list(phillips_sub.ORDEM),
        "x12": [_iso(p) for p in i12],
        "rot12": [_rot(p) for p in i12],
        "janela": phillips_sub.JANELA,
        "rot_saz": [phillips_sub.ROT_SAZ["s%d" % i] for i in (1, 2, 3, 4)],
        "eq": eqs,
        "cheio": {
            "obs": _ser(c["obs"]),
            "fit": _ser(c["fit"]),
            "piso": _ser(a["serie"]),
            "r2": round(c["r2"], 4),
            "rmse": round(c["rmse"], 4),
            "erro_medio": round(c["erro_medio"], 4),
            "rmse_piso": round(a["rmse"], 4),
            "r2_piso": round(a["r2"], 4),
            "erro_medio_piso": round(a["erro_medio"], 4),
            "erro_max_piso": round(a["erro_max"], 4),
            "obs12": _ser(P["cheio"]["obs12"]),
            "aj12": _ser(P["cheio"]["aj12"]),
            # o gabarito: a mesma janela lida do IPCA 12m PUBLICADO
            "ref12": _ser(panel.ipca_12m_publicado().reindex(i12)),
            "rmse12": round(P["cheio"]["rmse"], 4),
            "erro12": round(P["cheio"]["erro_medio"], 4),
            "vies12": round(P["cheio"]["vies"], 4),
        },
        "ia_variantes": variantes,
        "im_ancoras": ancoras,
    }


def construir() -> dict:
    """Monta o payload. Separado de `run()` para o teste poder afirmar sobre ele."""
    df = panel.construir()
    idx = df.index

    completo = df["completo"].astype(bool)
    fim_completo = idx[completo][-1] if completo.any() else None

    aberto = None
    if not bool(completo.iloc[-1]):
        p = idx[-1]
        meio = p.start_time
        aberto = {
            "rot": _rot(p),
            "x0": (meio - pd.Timedelta(days=45)).strftime("%Y-%m-%d"),
            "x1": (meio + pd.Timedelta(days=45)).strftime("%Y-%m-%d"),
        }

    # A estimacao no seu try/except: se ela quebrar, a aba dela degrada em vez de
    # derrubar o relatorio inteiro. A aba de dados nao depende dela.
    try:
        sub = _load_sub(df)
    except Exception as exc:  # noqa: BLE001
        print("AVISO: equacoes por grupo nao estimadas (%s: %s)"
              % (type(exc).__name__, exc))
        sub = None

    try:
        exp = _load_exp(df)
    except Exception as exc:  # noqa: BLE001
        print("AVISO: equacao de expectativas nao estimada (%s: %s)"
              % (type(exc).__name__, exc))
        exp = None

    try:
        eqis = _load_is(df)
    except Exception as exc:  # noqa: BLE001
        print("AVISO: curva IS nao estimada (%s: %s)" % (type(exc).__name__, exc))
        eqis = None

    try:
        tay = _load_taylor(df)
    except Exception as exc:  # noqa: BLE001
        print("AVISO: regra de juros nao estimada (%s: %s)" % (type(exc).__name__, exc))
        tay = None

    try:
        cam = _load_fx()
    except Exception as exc:  # noqa: BLE001
        print("AVISO: equacao de cambio nao estimada (%s: %s)" % (type(exc).__name__, exc))
        cam = None

    # O simulador LE os desenhos do posterior de um arquivo; ele nao roda MCMC. Se o
    # arquivo nao existir, a aba degrada com a instrucao de como gera-lo em vez de
    # segurar a geracao do relatorio por tres minutos de amostrador.
    try:
        sim = simulator.construir(df)
    except Exception as exc:  # noqa: BLE001
        print("AVISO: simulador nao montado (%s: %s)" % (type(exc).__name__, exc))
        sim = None

    return {
        "meta": {
            "gerado": dt.datetime.now().strftime("%d/%m/%Y %H:%M"),
            "n": int(len(df)),
            "ini": _rot(idx[0]),
            "fim": _rot(idx[-1]),
            "fim_completo": _rot(fim_completo) if fim_completo is not None else None,
            "aberto": aberto,
        },
        "x": [_iso(p) for p in idx],
        "rot": [_rot(p) for p in idx],
        "completo": [bool(v) for v in completo],
        "s": {c: _ser(df[c]) for c in _ORDEM},
        "info": {c: INFO[c] for c in _ORDEM},
        "ordem": _ORDEM,
        "sub": sub,
        "exp": exp,
        "is": eqis,
        "tay": tay,
        "fx": cam,
        "sim": sim,
    }


# As modas publicadas da eq. (5) do BC (C2 Boxe3, RI jun/2024), para a tabela de
# comparacao. `f2` NAO e o mesmo objeto que o nosso `e2` -- o de la e a previsao do
# proprio modelo quatro trimestres a frente, o daqui e o trimestre que acabou. A tela
# diz isso; guardar o numero sem a ressalva seria pior do que nao guardar.
BC_EQ5 = {
    "f1":   dict(rot="Expectativa do trimestre anterior", v=0.75, ic=(0.68, 0.82),
                 nosso="e1", comparavel=True),
    "f2":   dict(rot="Previsão do próprio modelo, quatro trimestres à frente",
                 v=0.11, ic=(0.06, 0.13), nosso="e2", comparavel=False),
    "f3":   dict(rot="Média de quatro trimestres de IPCA passado", v=0.021,
                 ic=(0.0, 0.049), nosso=None, comparavel=True),
    "meta": dict(rot="Peso da meta", v=0.119, ic=None, nosso="meta", comparavel=True),
}


def _coef_exp(r: dict) -> list:
    """Coeficientes de (E) no formato que a tela consome.

    Os dois dividem a soma-um com a meta, entao `restrito` e verdadeiro nos dois --
    o campo existe porque e ele que diz a tela de onde sai a conta de sobra.
    """
    out = []
    for par, _col in r["termos"]:
        lp = r["longo_prazo"].get(par)
        out.append({
            "key": par,
            "rot": expectations.rotulo(par),
            "b": round(float(r["coef"][par]), 6),
            "se": round(float(r["se"][par]), 6),
            "t": round(float(r["t"][par]), 2),
            "t_ols": round(float(r["t_ols"][par]), 2),
            "p": round(float(r["p"][par]), 4),
            "lp": round(float(lp), 6) if lp is not None else None,
            "restrito": True,
        })
    return out


def _load_exp(df: pd.DataFrame) -> dict:
    """A equacao (E), na especificacao do plano da pasta."""
    d = expectations.montar(df)
    r = expectations.estimar(d)
    idx = r["idx"]
    rep = expectations.repouso(r)

    # A decomposicao do DESVIO contra a meta: quanto de E-Meta vem da inercia e
    # quanto da inflacao. Ela e uma identidade, nao um modelo -- as duas parcelas
    # mais o residuo somam o desvio observado, e ha assercao para isso.
    dd = d.loc[idx]
    mm = r["meta"]
    contrib = {}
    for grupo, par, col in (("inercia", "e1", "pi_e_l1"), ("inflacao", "e2", "i12")):
        contrib[grupo] = _ser(r["coef"][par] * (dd[col] - mm))

    return {
        "x": [_iso(p) for p in idx],
        "rot": [_rot(p) for p in idx],
        "n": r["n"], "ini": _rot(r["ini"]), "fim": _rot(r["fim"]),
        "hac_lags": r["hac_lags"], "estimador": r["estimador"],
        "obs": _ser(r["obs"]), "fit": _ser(r["fit"]),
        "meta": _ser(mm), "resid": _ser(r["resid"]),
        "coef": _coef_exp(r),
        "peso_meta": round(r["peso_meta"], 6),
        "soma_inercia": round(r["soma_inercia"], 6),
        "meia_vida": r["meia_vida"],
        "repasse": round(r["repasse_lp"], 6),
        "r2": round(r["r2"], 4), "rmse": round(r["rmse"], 4),
        "erro_medio": round(r["erro_medio"], 4),
        "acf": [round(v, 3) for v in r["acf"]],
        "lb_q4": round(r["lb_q4"], 2), "lb_p4": round(r["lb_p4"], 4),
        "lb_q8": round(r["lb_q8"], 2), "lb_p8": round(r["lb_p8"], 4),
        "contrib": contrib,
        "repouso": {"devolve_a_meta": bool(rep["devolve_a_meta"]),
                    "simulado": round(rep["repasse_simulado"], 6),
                    "formula": round(rep["repasse_formula"], 6)},
        "bc": {k: dict(v) for k, v in BC_EQ5.items()},
    }


# As modas publicadas da eq. (2) do BC (C2 Boxe3 Tab 1, RI jun/2024), copiadas de
# `monetary_policy.modelo_agregado.BCB`/`BCB_IC` -- importadas de la e nao redigitadas,
# para as duas paginas nao divergirem.
#
# A eq. (2) do BC e  h = b1*h(-1) - b2*r_hat(-1)/4 - b3*rp_hat + b4*h_mundo + s^h,
# entao `b2` entra SUBTRAINDO e o efeito dele e -b2/4 = -0,110 por p.p. de juro real
# acima do neutro. E na mesma direcao que o nosso h2, mas NAO na mesma unidade: o
# regressor de la e o desvio do juro real ex-ante contra o r* do filtro, e o daqui e a
# inclinacao 2a-10a da curva real. A tabela marca a linha e a nota diz por que.
_BCB = _mp_agregado.BCB
_BCB_IC = _mp_agregado.BCB_IC

BC_EQ2 = {
    "b1": dict(rot="Hiato do trimestre anterior", v=_BCB["b1"], ic=_BCB_IC["b1"],
               nosso="h1", comparavel=True),
    "b2": dict(rot="Juro real contra o neutro do filtro, do trimestre anterior",
               v=_BCB["b2"], ic=_BCB_IC["b2"], nosso="h2", comparavel=False,
               efeito=-_BCB["b2"] / 4.0),
    "b3": dict(rot="Condições financeiras (prêmio de risco)", v=_BCB["b3"],
               ic=_BCB_IC["b3"], nosso=None, comparavel=True),
}


def _coef_is(r: dict) -> list:
    """Coeficientes de (H) no formato que a tela consome.

    `crise` separa as duas dummies dos dois parametros da conta: elas nao sao leitura
    economica, sao o que impede 2008 e 2020 de definirem a inclinacao.
    """
    out = []
    for par in [x for x, _ in r["termos"]] + r["dummies"]:
        lp = r["longo_prazo"].get(par)
        out.append({
            "key": par,
            "rot": is_curve.rotulo(par),
            "b": round(float(r["coef"][par]), 6),
            "se": round(float(r["se"][par]), 6),
            "t": round(float(r["t"][par]), 2),
            "t_ols": round(float(r["t_ols"][par]), 2),
            "p": round(float(r["p"][par]), 4),
            "lp": round(float(lp), 6) if lp is not None else None,
            "crise": par in is_curve.CRISES,
        })
    return out


def _load_is(df: pd.DataFrame) -> dict:
    """A equacao (H), a curva IS."""
    d = is_curve.montar(df)
    r = is_curve.estimar(d)
    idx = r["idx"]
    rep = is_curve.repouso(r)
    dd = d.loc[idx]

    # A decomposicao do hiato: quanto vem da inercia, quanto do aperto e quanto das
    # crises. E identidade -- as parcelas mais o residuo somam o hiato observado.
    contrib = {
        "inercia": _ser(r["coef"]["h1"] * dd["hiato_l1"]),
        "aperto": _ser(r["coef"]["h2"] * dd["g_rr_l"]),
        "crise": _ser(sum(r["coef"][k] * dd[k] for k in r["dummies"])),
    }

    comp = []
    for k, rr in is_curve.comparar(df).items():
        comp.append({
            "key": k, "desc": rr["desc"], "escolhida": k == "base",
            "h1": round(float(rr["coef"]["h1"]), 6),
            "h2": round(float(rr["coef"]["h2"]), 6),
            "t": round(float(rr["t"]["h2"]), 2),
            "r2": round(rr["r2"], 4), "rmse": round(rr["rmse"], 4),
            "lb_p4": round(rr["lb_p4"], 4),
        })

    return {
        "x": [_iso(p) for p in idx],
        "rot": [_rot(p) for p in idx],
        "n": r["n"], "ini": _rot(r["ini"]), "fim": _rot(r["fim"]),
        "hac_lags": r["hac_lags"], "estimador": r["estimador"],
        "lag_grr": r["lag_grr"],
        "obs": _ser(r["obs"]), "fit": _ser(r["fit"]), "resid": _ser(r["resid"]),
        "grr": _ser(dd["g_rr_l"]),
        "coef": _coef_is(r),
        "persistencia": round(r["persistencia"], 6),
        "estavel": bool(r["estavel"]),
        "meia_vida": r["meia_vida"],
        "efeito_lp": round(r["efeito_lp"], 6),
        "r2": round(r["r2"], 4), "rmse": round(r["rmse"], 4),
        "erro_medio": round(r["erro_medio"], 4),
        "acf": [round(v, 3) for v in r["acf"]],
        "lb_q4": round(r["lb_q4"], 2), "lb_p4": round(r["lb_p4"], 4),
        "lb_q8": round(r["lb_q8"], 2), "lb_p8": round(r["lb_p8"], 4),
        "hiato_medio": round(r["hiato_medio"], 4),
        "hiato_sd": round(r["hiato_sd"], 4),
        "contrib": contrib,
        "comparar": comp,
        "rr": [{"key": r["key"], "desc": r["desc"], "escolhida": bool(r["escolhida"]),
                "h2": round(r["h2"], 6), "t": round(r["t"], 2),
                "r2": round(r["r2"], 4), "n": int(r["n"])}
               for r in is_curve.comparar_rr(df)],
        "repouso": {"volta_a_zero": bool(rep["volta_a_zero"]),
                    "simulado": round(rep["efeito_simulado"], 6),
                    "formula": round(rep["efeito_formula"], 6)},
        "bc": {k: dict(v) for k, v in BC_EQ2.items()},
    }


# ═══════════ A equacao (R), a regra de juros ═══════════

# Os tres parametros publicados da eq. (3) do BC. `t3` NAO e o nosso `r2`: la o
# multiplicador esta DENTRO do colchete, pesado por (1-t1-t2), entao o objeto
# comparavel e o nosso efeito de longo prazo. A tela diz isso.
BC_EQ3 = {
    "t1": dict(rot="Juros do trimestre anterior", v=taylor.BCB["t1"],
               ic=taylor.BCB_IC["t1"], nosso="r1", comparavel=True),
    "t2": dict(rot="Juros de dois trimestres atrás", v=taylor.BCB["t2"],
               ic=taylor.BCB_IC["t2"], nosso="r1b", comparavel=True),
    "t3": dict(rot="Resposta à inflação esperada acima da meta", v=taylor.BCB["t3"],
               ic=taylor.BCB_IC["t3"], nosso="lp", comparavel=True),
}


def _coef_taylor(r: dict) -> list:
    """Coeficientes de (R). `crise` separa as dummies dos tres pesos da conta."""
    out = []
    for par in r["termos"] + r["dummies"]:
        out.append({
            "key": par,
            "rot": taylor.rotulo(par),
            "b": round(float(r["coef"][par]), 6),
            "se": round(float(r["se"][par]), 6),
            "t": round(float(r["t"][par]), 2),
            "t_ols": round(float(r["t_ols"][par]), 2),
            "p": round(float(r["p"][par]), 4),
            "crise": par in taylor.CRISES,
        })
    return out


def _load_taylor(df: pd.DataFrame) -> dict:
    """A equacao (R), a regra de juros."""
    d = taylor.montar(df)
    r = taylor.estimar(d)
    idx = r["idx"]
    rep = taylor.repouso(r)
    dd = d.loc[idx]

    # A decomposicao e do DESVIO em relacao a ancora, que e o que a conta explica --
    # nao do nivel da Selic. No nivel a ancora responderia por quase tudo e as outras
    # parcelas ficariam ilegiveis; e ela ja esta desenhada como linha no outro grafico.
    contrib = {
        "inercia": _ser(r["coef"]["r1"] * dd["r1"]
                        + (r["coef"].get("r1b", 0.0) * dd["r1b"] if "r1b" in r["coef"]
                           else 0.0)),
        "inflacao": _ser(r["coef"]["r2"] * dd["r2"]),
        "crise": _ser(sum(r["coef"][k] * dd[k] for k in r["dummies"])
                      if r["dummies"] else dd["r2"] * 0.0),
    }

    comp = []
    for k, rr in taylor.comparar(df).items():
        comp.append({
            "key": k, "desc": rr["desc"], "escolhida": k == "base",
            "r1": round(float(rr["coef"]["r1"]), 6),
            "r2": round(float(rr["coef"]["r2"]), 6),
            "soma": round(float(rr["soma"]), 6),
            "efeito_lp": round(float(rr["efeito_lp"]), 6),
            "r2_cent": round(rr["r2_cent"], 4), "rmse": round(rr["rmse"], 4),
            "lb_p4": round(rr["lb_p4"], 4),
        })

    jan = []
    for j in taylor.comparar_janela(df):
        jan.append({
            "k": int(j["k"]), "rot": j["rot"], "escolhida": bool(j["escolhida"]),
            "corr_aperto": round(j["corr_aperto"], 4),
            "nivel_hoje": round(j["nivel_hoje"], 4),
            "r1": round(j["r1"], 6), "r2": round(j["r2"], 6),
            "efeito_lp": round(float(j["efeito_lp"]), 6),
            "r2_cent": round(j["r2_cent"], 4), "lb_p4": round(j["lb_p4"], 4),
            "n": int(j["n"]),
        })

    cf = {c["key"]: c["b"] for c in _coef_taylor(r)}
    dentro = {}
    for k, b in BC_EQ3.items():
        v = r["efeito_lp"] if b["nosso"] == "lp" else cf.get(b["nosso"])
        dentro[k] = None if v is None else bool(b["ic"][0] <= v <= b["ic"][1])

    return {
        "x": [_iso(p) for p in idx],
        "rot": [_rot(p) for p in idx],
        "n": r["n"], "ini": _rot(r["ini"]), "fim": _rot(r["fim"]),
        "hac_lags": r["hac_lags"], "estimador": r["estimador"],
        "lags": r["lags"], "mm_rr": r["mm_rr"],
        "di": taylor.DI[taylor.DI_BASE][2],
        "selic": _ser(dd["selic"]),
        "ancora": _ser(dd["ancora"]),
        "rr_star": _ser(dd["rr_star"]),
        "selic_fit": _ser(dd["ancora"] + r["fit"]),
        "obs": _ser(r["obs"]), "fit": _ser(r["fit"]), "resid": _ser(r["resid"]),
        "di_serie": _ser(dd["r2"]),
        "contrib": contrib,
        "coef": _coef_taylor(r),
        "soma": round(r["soma"], 6), "estavel": bool(r["estavel"]),
        "meia_vida": r["meia_vida"],
        "efeito_lp": round(float(r["efeito_lp"]), 6),
        "r2": round(r["r2_cent"], 4), "rmse": round(r["rmse"], 4),
        "erro_medio": round(r["erro_medio"], 4),
        "acf": [round(v, 3) for v in r["acf"]],
        "lb_q4": round(r["lb_q4"], 2), "lb_p4": round(r["lb_p4"], 4),
        "lb_q8": round(r["lb_q8"], 2), "lb_p8": round(r["lb_p8"], 4),
        "dummies_fora": list(r["dummies_fora"]),
        "repouso": {"volta_a_ancora": bool(rep["volta_a_ancora"]),
                    "simulado": round(rep["efeito_simulado"], 6),
                    "formula": round(rep["efeito_formula"], 6),
                    "dentro_do_ic": bool(rep["dentro_do_ic"])},
        "comparar": comp,
        "janela": jan,
        "bc": {k: dict(v) for k, v in BC_EQ3.items()},
        "dentro": dentro,
        "soma_bc": round(taylor.BCB_SOMA, 4),
    }


# ═══════════ A equacao (F), o cambio ═══════════

def _load_fx() -> dict:
    """A equacao (F). Nao recebe o painel: le o frame mensal do FX Report."""
    z, st, reg = fx.montar()
    r = fx.estimar(z, reg)
    zz = r["z"]
    idx = zz.index
    nat = fx.nativo(r, st)
    corr = fx.correlacoes(zz, reg)

    # a parcela de cada termo em cada trimestre. Soma + residuo = a variacao observada,
    # e o teste afirma isso.
    contrib = {c: _ser(r["beta"][c] * zz[c]) for c in reg}
    contrib["ppp"] = _ser(zz[fx.OFFSET])
    contrib["alpha"] = _ser(pd.Series(r["alpha"], index=idx))

    coef = []
    for c in reg:
        coef.append({
            "key": c, "rot": fx.ROT.get(c, c), "unid": fx.UNID.get(c, ""),
            "b": round(float(r["beta"][c]), 6),
            "t": round(float(r["t"][c]), 2),
            "p": round(float(r["p"][c]), 4),
            "nativo": round(float(nat[c]), 6),
            "acum": round(float(r["contrib"][c]), 4),
            "corr": round(corr[c], 4),
            # DERIVADO: o canal cujo coeficiente tem sinal oposto ao da correlacao
            # bruta. A prosa da pagina le este campo em vez de nomear um canal a mao.
            "troca_sinal": bool(r["beta"][c] * corr[c] < 0),
        })

    comp = []
    for k, rr in fx.comparar().items():
        comp.append({
            "key": k, "desc": rr["desc"], "escolhida": k == "base",
            "r2": round(rr["r2"], 4), "rmse": round(rr["rmse"], 4),
            "sd_y": round(rr["sd_y"], 4),
            "alpha": round(rr["alpha"], 4), "t_alpha": round(rr["t"]["alpha"], 2),
            "lb_p4": round(rr["lb_p4"], 4),
        })

    m = fx.mensal_ao_lado()
    flip = [c["key"] for c in coef if c["troca_sinal"]]
    ana = []
    if flip:
        for a in fx.anatomia(zz, flip[0]):
            ana.append({
                "controles": [fx.ROT.get(c, c) for c in a["controles"]],
                "n": a["n_controles"], "todos": bool(a["todos"]),
                "b": round(a["b"], 6), "t": round(a["t"], 2),
            })

    return {
        "x": [_iso(p) for p in idx],
        "rot": [_rot(p) for p in idx],
        "n": r["n"], "ini": _rot(r["ini"]), "fim": _rot(r["fim"]),
        "corte": fx.corte(), "estimador": r["estimador"],
        "lam": round(r["lam"], 4), "piso": bool(r["piso"]),
        "t_valem": bool(r["t_valem"]),
        "cv": [{"lam": round(float(v["lambda"]), 4), "mse": round(float(v["mse"]), 4)}
               for _, v in r["cv"].sort_values("lambda").iterrows()],
        "obs": _ser(zz["de"]), "fit": _ser(r["fit"]), "resid": _ser(r["resid"]),
        "contrib": contrib,
        "coef": coef, "ordem": list(reg),
        "alpha": round(r["alpha"], 6), "t_alpha": round(r["t"]["alpha"], 2),
        "p_alpha": round(r["p"]["alpha"], 4),
        "acum_alpha": round(r["contrib"]["alpha"], 4),
        "acum_ppp": round(r["contrib"][fx.OFFSET], 4),
        "de_total": round(r["de_total"], 4),
        "r2": round(r["r2"], 4), "rmse": round(r["rmse"], 4),
        "acf1": round(r["acf1"], 3),
        "lb_p4": round(r["lb_p4"], 4), "lb_p8": round(r["lb_p8"], 4),
        "comparar": comp,
        "anatomia": ana, "flip": flip,
        "mensal": {"n": int(m["n"]), "r2": round(m["r2"], 4),
                   "lam": round(m["lam"], 4),
                   "ini": m["ini"].strftime("%m/%Y"), "fim": m["fim"].strftime("%m/%Y"),
                   "alpha": round(m["alpha"], 6),
                   "nativo": {c: round(float(v), 6) for c, v in m["nativo"].items()}},
        "vol_source": fx.VOL_SOURCE, "vol_lag": fx.VOL_LAG_Q,
    }


def run(output: str = _SAIDA) -> None:
    """Gera o HTML.

    O parametro se chama `output` e nao outra coisa porque o botao Regerar do
    calendario chama `mod.run(output=...)` para poder gravar o carimbo junto; um
    nome diferente estoura com TypeError.
    """
    try:
        data = construir()
    except Exception as exc:  # noqa: BLE001
        print("AVISO: painel nao pode ser construido (%s: %s)" % (type(exc).__name__, exc))
        raise

    out = render_report(_TEMPLATE, data, output)
    m = data["meta"]
    print("Relatorio salvo: %s" % out)
    print("  painel %s -> %s (%d trimestres); ultimo trimestre fechado: %s"
          % (m["ini"], m["fim"], m["n"], m["fim_completo"]))
    sb = data.get("sub")
    if sb is None:
        print("  equacoes por grupo: NAO estimadas")
    else:
        c = sb["cheio"]
        print("  por grupo: %d tri (%s a %s); cheio reconstruido RMSE %.3f, piso %.3f"
              % (sb["n"], sb["ini"], sb["fim"], c["rmse"], c["rmse_piso"]))
        for k in sb["ordem"]:
            e = sb["eq"][k]
            print("    (%s) %-17s R2 %.3f  RMSE %.3f  Ljung-Box p %.3f"
                  % (k, e["nome"], e["r2"], e["rmse"], e["lb_p4"]))
    ex = data.get("exp")
    if ex is None:
        print("  expectativas: NAO estimada")
    else:
        print("  (E) expectativas: %d tri (%s a %s); R2 %.3f RMSE %.3f LB p %.3f"
              % (ex["n"], ex["ini"], ex["fim"], ex["r2"], ex["rmse"], ex["lb_p4"]))
        print("      peso da meta %.3f · meia-vida %.0f tri · repasse de longo prazo %.3f"
              % (ex["peso_meta"], ex["meia_vida"], ex["repasse"]))
    hi = data.get("is")
    if hi is None:
        print("  (H) curva IS: NAO estimada")
    else:
        print("  (H) curva IS: %d tri (%s a %s); R2 %.3f RMSE %.3f LB p %.3f"
              % (hi["n"], hi["ini"], hi["fim"], hi["r2"], hi["rmse"], hi["lb_p4"]))
        print("      persistencia %.3f · meia-vida %.0f tri · efeito de longo prazo %.3f"
              % (hi["persistencia"], hi["meia_vida"], hi["efeito_lp"]))
    ty = data.get("tay")
    if ty is None:
        print("  (R) regra de juros: NAO estimada")
    else:
        print("  (R) regra de juros: %d tri (%s a %s); R2 %.3f RMSE %.3f LB p %.3f"
              % (ty["n"], ty["ini"], ty["fim"], ty["r2"], ty["rmse"], ty["lb_p4"]))
        print("      soma das defasagens %.3f · efeito de longo prazo %.2f (BC %.2f [%.2f; %.2f])"
              % (ty["soma"], ty["efeito_lp"], ty["bc"]["t3"]["v"],
                 ty["bc"]["t3"]["ic"][0], ty["bc"]["t3"]["ic"][1]))
    cm = data.get("fx")
    if cm is None:
        print("  (F) cambio: NAO estimada")
    else:
        print("  (F) cambio: %d tri (%s a %s); R2 %.4f RMSE %.2f lambda %.4f"
              % (cm["n"], cm["ini"], cm["fim"], cm["r2"], cm["rmse"], cm["lam"]))
        print("      mensal ao lado: n %d, R2 %.4f · canais que trocam de sinal: %s"
              % (cm["mensal"]["n"], cm["mensal"]["r2"],
                 ", ".join(cm["flip"]) if cm["flip"] else "nenhum"))
    sm = data.get("sim")
    if sm is None:
        print("  simulador: NAO montado")
    else:
        eq = sm["eq"][sm["eq_ordem"][0]]
        print("  simulador: %d equacao(oes) (%s), %d inputs (%s); horizonte ate %d tri"
              % (len(sm["eq_ordem"]), ", ".join(sm["eq_ordem"]),
                 len(sm["var_ordem"]), ", ".join(sm["var_ordem"]), sm["h_max"]))
        print("      %d desenhos de %d, priori '%s'"
              % (eq["n_draws"], eq["n_draws_total"], eq["priori"]))
        for k in sm["var_ordem"]:
            v = sm["var"][k]
            prod = v["produzida_por"]
            quem = ("(%s)%s" % (prod, "" if v["produtor_no_sim"] else ", FORA do sim"))                if prod else "-"
            print("      %-8s %-9s produzida por %-16s partes: %s"
                  % (k, v["tipo"], quem, ", ".join(v["partes"] or []) or "-"))


if __name__ == "__main__":
    run()
