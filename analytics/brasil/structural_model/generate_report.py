"""Gera reports/brasil/Structural Model.html.

Primeira aba: o painel de dados da equacao (I), a curva de Phillips. O relatorio
monta o painel DIRETO do MySQL a cada geracao -- nao ha artefato intermediario,
porque `panel.construir()` e so um punhado de consultas e nada nele e caro.
Um insumo que so a geracao alcanca e um insumo que a atualizacao do banco nao
alcanca; enquanto nao houver estimacao de modelo (que e cara de verdade), nao ha
passo de recalculo a declarar.

Uso:
    uv run python -c "from analytics.brasil.structural_model.generate_report import run; run()"
"""
from __future__ import annotations

import datetime as dt
import math
from pathlib import Path

import pandas as pd

from analytics.brasil.structural_model import panel
from analytics.report_structure.builder import render_report

_HERE = Path(__file__).parent
_TEMPLATE = _HERE / "report.html"
_SAIDA = "reports/brasil/Structural Model.html"

# Uma entrada por variavel da equacao (I). `nome` e o rotulo curto que aparece na
# tela; `full` so entra no cartao de definicao quando acrescenta algo ao nome; `eixo`
# e a MESMA string que titula o eixo Y, para o cartao e o eixo nao divergirem.
INFO = {
    "ipca_12m": dict(
        nome="IPCA em 12 meses",
        full="Índice Nacional de Preços ao Consumidor Amplo, variação acumulada em doze meses",
        desc="A inflação que a equação explica. É a leitura do último mês de cada trimestre — "
             "a média dos três meses seria a média de três janelas de doze meses sobrepostas, "
             "que não corresponde a acumulado nenhum.",
        eixo="variação do IPCA em 12 meses, %",
        fonte="IBGE, via Banco Central",
    ),
    "pi_e": dict(
        nome="Expectativa de inflação",
        full="Mediana das expectativas de mercado para o IPCA dos doze meses seguintes, série suavizada",
        desc="O que o mercado esperava de inflação para o ano seguinte, em média ao longo do "
             "trimestre. É a pesquisa semanal que o Banco Central faz com cerca de cem instituições; "
             "a versão suavizada interpola as projeções de ano fechado para produzir uma janela "
             "móvel de doze meses.",
        eixo="IPCA esperado para os 12 meses seguintes, %",
        fonte="Banco Central, pesquisa Focus",
    ),
    "hiato": dict(
        nome="Hiato do produto",
        full="Hiato do produto — cenário de referência",
        desc="Quanto a economia está produzindo acima ou abaixo do que consegue sustentar sem "
             "pressionar preços. Positivo é demanda acima da capacidade. Não é medido: é a "
             "estimativa que o próprio Banco Central publica, e ele a reescreve a cada trimestre — "
             "a série aqui é sempre a leitura mais recente, não o que ele dizia na época.",
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
    "pi_star_usd": dict(
        nome="IC-Br em dólar",
        full="Índice de Commodities Brasil, denominado em dólar",
        desc="O preço, em dólar, da cesta de commodities que pesa na inflação brasileira — "
             "agropecuária, metal e energia. Em dólar e não em real de propósito: a versão em "
             "real já embute o câmbio, que entra na equação pela sua própria linha, e contá-lo "
             "duas vezes inflaria o repasse cambial.",
        eixo="variação da média do trimestre, %",
        fonte="Banco Central (série 29042)",
    ),
}

_ORDEM = ["ipca_12m", "pi_e", "hiato", "de", "pi_star_usd"]


def _ser(s: pd.Series) -> list:
    """Serie -> lista JSON, com None no lugar de NaN (JSON nao tem NaN)."""
    return [None if (v is None or (isinstance(v, float) and math.isnan(v))) else round(float(v), 4)
            for v in s]


def _iso(p: pd.Period) -> str:
    return p.start_time.strftime("%Y-%m-%d")


def _rot(p: pd.Period) -> str:
    return "%dT%d" % (p.year, p.quarter)


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


if __name__ == "__main__":
    run()
