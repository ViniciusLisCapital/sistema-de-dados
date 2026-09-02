"""
As metricas derivadas -- as unicas contas deste relatorio que nao sao transformacao
de exibicao.

Elas so existem nesta rodada porque as tres pesquisas passaram a estar na base ao
mesmo tempo. O escopo do JOLTS (2026-09-01) foi fechado sem derivadas exatamente para
esperar isto: *"vamos pegar os outros dados de emprego e ai construimos metricas
derivadas"*.

--------------------------------------------------------------------------------
AS QUATRO, E DE QUE PESQUISA VEM CADA PERNA
--------------------------------------------------------------------------------
| metrica                  | numerador          | denominador        |
|--------------------------|--------------------|--------------------|
| vagas por desempregado   | JOLTS job openings | CPS unemployment   |
| contratacao liquida      | JOLTS hires        | JOLTS separations  |
| curva de Beveridge       | JOLTS openings rate| CPS unemp. rate    |
| divergencia CES x CPS    | CES employment     | CPS employment     |

**Cruzar pesquisas e a parte que pode dar errado em silencio**, e cada uma das quatro
tem uma armadilha propria:

1. **Vagas por desempregado tem gabarito, e ele esta DE CABECA PARA BAIXO.** O BLS
   publica a razao ele mesmo, na serie `UO` do JOLTS -- mas o que ele publica e
   *"unemployed persons per job opening"*, o **reciproco** do que se cita normalmente.
   Em jul/2009 a serie do BLS marca 6,50 e a razao vagas/desempregado do mesmo mes e
   0,153: sao 1/6,50. O guarda desta funcao pegou a inversao na primeira execucao,
   com erro medio de 1,58 -- e e exatamente o tipo de troca que passa despercebida
   quando a razao esta perto de 1, como esta hoje (1,05 contra 0,95).
   O relatorio mostra **vagas por desempregado**, que e a convencao citada, e a
   validacao compara contra `1/UO`.
2. **Contratacao liquida NAO e a variacao do emprego.** Contratacoes menos
   desligamentos do JOLTS nao reproduz a variacao do payroll da CES: as duas pesquisas
   tem amostra, universo e imputacao diferentes, e o proprio BLS publica uma nota
   sobre a diferenca. A serie e informativa como fluxo bruto, e o relatorio diz que a
   comparacao com o payroll e aproximada.
3. **A curva de Beveridge usa a taxa de vagas, nao o nivel.** As duas pernas precisam
   ser razoes para a curva ter significado; e a taxa de vagas do JOLTS tem denominador
   proprio (emprego + vagas), que nao e o da taxa de desemprego (forca de trabalho).
   Sao dois eixos de unidade igual e base diferente, e a nota da aba diz isso.
4. **A divergencia CES x CPS e por construcao, nao um erro de ninguem.** A CES conta
   VAGAS PREENCHIDAS em estabelecimentos (quem tem dois empregos conta duas vezes,
   autonomo nao conta); a CPS conta PESSOAS ocupadas em domicilios (autonomo conta,
   quem tem dois empregos conta uma vez). Elas nunca vao reconciliar, e a distancia
   entre as duas e ela mesma o dado.

--------------------------------------------------------------------------------
UM BURACO QUE ATRAVESSA TUDO: OUTUBRO DE 2025
--------------------------------------------------------------------------------
A paralisacao do governo federal cancelou a coleta da CPS de outubro de 2025 -- o
proprio release traz a nota. O JOLTS continuou. Entao qualquer metrica com perna
domiciliar tem um mes faltando que a perna do JOLTS nao tem, e propagar nulo (em vez
de interpolar) e o que impede a serie de inventar um ponto.
"""

from __future__ import annotations

import pandas as pd

_MES_SEM_CPS = pd.Timestamp("2025-10-01")


def _serie(df: pd.DataFrame, **filtros) -> pd.Series:
    m = pd.Series(True, index=df.index)
    for k, v in filtros.items():
        m &= df[k] == v
    s = df.loc[m].set_index("date")["valor"].sort_index()
    if s.empty:
        raise RuntimeError(f"nenhuma linha para {filtros}")
    if s.index.duplicated().any():
        raise RuntimeError(f"datas repetidas em {filtros}")
    return s


def _mensal(s: pd.Series) -> pd.Series:
    """Reindexa numa grade mensal CONTIGUA, com None nos meses ausentes.

    Obrigatorio antes de qualquer `.diff()` sobre a CPS. A pesquisa domiciliar nao tem
    linha nenhuma em outubro de 2025 (a paralisacao cancelou a coleta), e `.diff()`
    numa serie com o mes ausente calcula **novembro menos setembro** e rotula o
    resultado como variacao mensal: 104 mil onde a variacao de um mes nao existe.
    Nenhuma excecao, e o numero e plausivel.
    """
    if s.empty:
        return s
    return s.reindex(pd.date_range(s.index[0], s.index[-1], freq="MS"))


def _razao(num: pd.Series, den: pd.Series) -> pd.Series:
    j = pd.concat([num.rename("n"), den.rename("d")], axis=1)
    return (j["n"] / j["d"].where(j["d"] != 0)).dropna()


def conferir_uo(nossa: pd.Series, uo_publicada: pd.Series) -> dict:
    """A nossa razao vagas/desempregado contra o RECIPROCO da serie UO do BLS.

    E o unico gabarito externo das quatro derivadas. O BLS publica *desempregados por
    vaga*, entao a comparacao e contra `1/UO` -- ver o item 1 do docstring do modulo,
    que existe porque esta funcao pegou a inversao.

    A comparacao e feita **na direcao do BLS** (`1/nossa` contra `UO`), nao na nossa.
    O motivo e a tolerancia: o BLS publica `UO` com UMA decimal, entao ali o limite e
    0,05 -- metade do ultimo digito -- e nao um numero escolhido. Invertendo para o
    nosso lado o mesmo arredondamento vira um erro que depende do nivel da razao (1/1,0
    contra 1/1,05 sao 0,05 de diferenca, mas 1/0,2 contra 1/0,25 sao 1,0), e o teste
    passaria a reprovar meses corretos de 2009.
    """
    nossa_uo = (1.0 / nossa.where(nossa != 0)).dropna()
    j = pd.concat([nossa_uo.rename("nossa"), uo_publicada.rename("bls")], axis=1).dropna()
    if j.empty:
        raise RuntimeError("nenhum mes em comum entre a nossa razao e a serie UO do BLS")
    erro = (j["nossa"] - j["bls"]).abs()
    if erro.mean() > 0.05:
        pior = erro.idxmax()
        raise RuntimeError(
            f"a razao vagas/desempregado nao reproduz a serie UO publicada: erro medio "
            f"{erro.mean():.4f} em {len(j)} meses, pior {pior.date()} "
            f"({j.loc[pior, 'nossa']:.3f} contra {j.loc[pior, 'bls']:.3f}). "
            "Dois candidatos, nesta ordem: a serie do BLS e o RECIPROCO (desempregados "
            "por vaga), e este calculo ja inverte -- inverter duas vezes volta ao erro; "
            "ou o denominador esta errado, e a razao e sobre DESEMPREGADOS, nao sobre a "
            "forca de trabalho."
        )
    return {"n": int(len(j)), "erroMedio": round(float(erro.mean()), 4),
            "erroMax": round(float(erro.max()), 4),
            "nota": "comparado como desempregados por vaga, a forma em que o BLS "
                    "publica, com uma decimal"}


def construir(jolts: pd.DataFrame, cps: pd.DataFrame, ces: pd.DataFrame) -> dict:
    """As quatro derivadas, na grade mensal comum.

    Args:
        jolts: `mt_jolts` do corte industria/000000 (inclui a medida UO).
        cps:   `mt_cps`, ajuste sa.
        ces:   `mt_ces` de 00000000, medida emprego, ajuste sa.
    """
    vagas = _serie(jolts, medida="JO", tipo="nivel", ajuste="sa")
    vagas_taxa = _serie(jolts, medida="JO", tipo="taxa", ajuste="sa")
    contrat = _serie(jolts, medida="HI", tipo="nivel", ajuste="sa")
    deslig = _serie(jolts, medida="TS", tipo="nivel", ajuste="sa")
    uo_bls = _serie(jolts, medida="UO", tipo="razao", ajuste="sa")

    desocup = _serie(cps, categoria="desocupados", ajuste="sa")
    taxa_desemp = _serie(cps, categoria="taxa_desemprego", ajuste="sa")
    cps_ocup = _serie(cps, categoria="ocupados", ajuste="sa")
    ces_emp = _serie(ces, categoria="00000000", medida="emprego", ajuste="sa")

    vu = _razao(vagas, desocup)
    aferido = conferir_uo(vu, uo_bls)

    liquida = (contrat - deslig).dropna()

    # A divergencia so faz sentido na variacao: os NIVEIS medem universos diferentes
    # (161 milhoes contra 158), entao a diferenca de nivel nao e informacao nova.
    # Reindexar ANTES de diferenciar: ver `_mensal`. Sem isso a variacao de novembro de
    # 2025 sai como a diferenca contra setembro, com cara de variacao mensal.
    ces_mm = _mensal(ces_emp).diff()
    cps_mm = _mensal(cps_ocup).diff()

    def emitir(s: pd.Series, dec: int = 3) -> dict:
        """`{i0, v[]}`: v e uma sequencia MENSAL CONTIGUA a partir de i0.

        Nao use dropna() aqui. Um `.dropna()` global remove o buraco INTERNO (outubro
        de 2025 na perna domiciliar) e todos os meses seguintes andam um mes para tras,
        sem lancar excecao nenhuma -- e o defeito que o teste de payload de
        `analytics/brasil/expectations` existe para pegar. So as pontas sao cortadas; o
        interior e reindexado numa grade mensal cheia, com None onde nao ha dado.
        """
        viva = s.dropna()
        if viva.empty:
            return {"i0": None, "v": []}
        cheia = s.reindex(pd.date_range(viva.index[0], viva.index[-1], freq="MS"))
        return {"i0": cheia.index[0].strftime("%Y-%m-%d"),
                "v": [None if pd.isna(x) else round(float(x), dec) for x in cheia]}

    grade = sorted(set(vu.index) | set(liquida.index) | set(ces_mm.dropna().index))
    return {
        "grade": [d.strftime("%Y-%m-%d") for d in grade],
        "vu": emitir(vu),
        # O reciproco, para o grafico poder desenhar a serie do BLS na mesma escala da
        # nossa em vez de num eixo espelhado.
        "uoBls": emitir((1.0 / uo_bls.where(uo_bls != 0)).dropna()),
        "vuAferido": aferido,
        "liquida": emitir(liquida, 0),
        "contratacoes": emitir(contrat, 0),
        "desligamentos": emitir(deslig, 0),
        "cesMm": emitir(ces_mm, 0),
        "cpsMm": emitir(cps_mm, 0),
        "beveridge": {
            "x": emitir(taxa_desemp, 1),
            "y": emitir(vagas_taxa, 1),
        },
        "mesSemCps": _MES_SEM_CPS.strftime("%Y-%m-%d"),
    }
