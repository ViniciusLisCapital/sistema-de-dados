"""
Classificacao dos subitens do IPCA por INERCIA, medida como a autocorrelacao de
ordem 12 da variacao acumulada em 12 meses:

    r12(k) = corr( yoy_k(t), yoy_k(t-12) )

Por que o lag 12 sobre o y/y, e nao sobre a variacao mensal (medido 2026-08,
ver `diagnostico()`):

  - Sobre o dado MENSAL BRUTO, o lag 12 e um detector de sazonalidade, nao de
    inercia: os 8 primeiros colocados sao todos ensino (Ensino medio 0,94,
    Ensino fundamental 0,93, Pre-escola 0,87), que reajustam em fevereiro.
    Dessazonalizar destroi o sinal -- a media cai de 0,16 para -0,06 e o maior
    valor cai para 0,29.
  - Sobre o Y/Y, as janelas de t e t-12 sao DISJUNTAS (meses t-11..t contra
    t-23..t-12), entao nao ha sobreposicao mecanica: para uma serie sem
    dependencia temporal a estatistica vale ~0. Confirmado por bootstrap de
    permutacao: media real +0,017 contra -0,137 da serie embaralhada.
    Sazonalidade tambem sai de graca, porque uma janela de 12 meses ja contem
    cada mes-calendario uma vez -- nao ha etapa de STL aqui.

O lag 1 sobre o y/y foi deliberadamente DEIXADO DE FORA (decisao do usuario,
2026-08, apos a medicao): janelas consecutivas de 12 meses compartilham 11
meses, entao a estatistica tem piso mecanico. Medido: media real 0,921 contra
0,895 da serie embaralhada -- ~97% do numero e construcao, e o que sobra ordena
mais por volatilidade do print do que por inercia (o fundo do ranking e pepino,
abobrinha, caranguejo, couve-flor). Se voltar, volta com o piso descontado
subitem a subitem; `diagnostico()` ja calcula o benchmark necessario.

Estimado no IPCA e herdado pelo IPCA-15 por codigo de subitem -- mesmo padrao
das flags nucleo_* da NT-57. O subitem e o mesmo produto nos dois indices, e uma
etiqueta estrutural que mudasse conforme a aba confundiria mais do que informa.

Nada aqui escreve no banco: e calculado em tempo de geracao do relatorio e viaja
no payload como ~380 tuplas [r12, faixa_por_peso, n_pares, faixa_fixa].

Uso:
    from analytics.brasil.inflation.inercia import calcular, diagnostico
"""

from __future__ import annotations

import numpy as np
import pandas as pd

# 120 observacoes de y/y = 10 anos. Exige 131 meses de dado mensal (os 11
# primeiros so formam o primeiro ponto) e rende 108 pares (t, t-12).
_JANELA_YOY = 120
# Minimo de pares (t, t-12) para classificar. 48 = 4 anos de sobreposicao.
#
# O numero nao e arbitrario, e o corte medido: a distribuicao de pares entre os
# 377 subitens vivos e BIMODAL -- 108 pares (a janela inteira) para 315 deles, e
# exatamente 56 para um bloco de 62. Esse bloco e a safra de subitens que entrou
# na estrutura de ponderacao de jan/2020 (Combo de telefonia com 1,43% do
# indice, Cabeleireiro 1,12%, Transporte por aplicativo, TV por assinatura...),
# que so tem 79 meses de historia na janela. Um corte em 60 os excluiria em
# bloco e levaria 6,75% do indice para "nao classificado" -- nao por serem
# atipicos, mas por serem novos. Com 48, os 377 vivos entram e 100% do peso e
# classificado, e a exclusao passa a atingir so o que de fato foi descontinuado.
#
# O custo e assumido, nao escondido: com 56 pares o erro-padrao da correlacao e
# ~0,134 contra ~0,096 de quem tem 108. Por isso `n_pares` viaja POR SUBITEM no
# payload e aparece no hover da linha -- duas estimativas na mesma faixa nao
# merecem a mesma confianca.
_MIN_PARES = 48
_N_FAIXAS = 5
# A classificacao sai do IPCA cheio e e herdada pelo IPCA-15.
_INDICE_BASE = "IPCA"

_ROTULOS = {
    1: "Q1 — Menos inercial",
    2: "Q2",
    3: "Q3",
    4: "Q4",
    5: "Q5 — Mais inercial",
    0: "Não classificado",
}

# Segunda classificacao, de CORTES FIXOS em r (pedido do usuario, 2026-08).
# Convive com a de quintis, nao a substitui: as duas leem o mesmo r12 e so
# discordam em ONDE cortar.
#
# A diferenca de leitura e real. A de quintis reparte o PESO em 5 partes iguais,
# entao cada faixa e sempre ~20% do indice e os limites em r andam quando a
# amostra anda. Esta reparte o EIXO r em intervalos fixos, entao os limites
# nunca andam e o peso e que sai desigual -- medido em 2026-08: 6,1% / 24,6% /
# 66,8% / 2,5%. Dois tercos do indice caem numa faixa so porque a distribuicao
# de r e unimodal em torno de ~+0,02, nao bimodal; cortar em +-0,5 pega so as
# caudas. Isso e propriedade do dado, nao defeito do corte.
#
# O que a comparacao 2006-2016 x 2016-2026 mostra sobre ESTA versao: as pontas
# NAO sobrevivem (13,3% e 4,2% de permanencia), e a faixa que sobrevive e a
# grande (65,4%), o que e persistencia trivial. Agregado kappa +0,11; so o
# sinal, kappa +0,22. A causa e regressao a media -- com EP da ordem de 0,25
# (bootstrap por blocos de 12; o 1/sqrt(n) do hover subestima, ver o CLAUDE.md
# da pasta), quem aparece alem de +-0,5 numa decada e em boa parte quem teve
# cauda de ruido, e volta para o meio na decada seguinte.
_CORTES_FIXOS = (-0.5, 0.0, 0.5)
_ROTULOS_FIXOS = {
    1: "Intensamente reversível · r ≤ −0,5",
    2: "Moderadamente reversível · −0,5 < r ≤ 0",
    3: "Moderadamente não reversível · 0 < r ≤ +0,5",
    4: "Intensamente não reversível · r > +0,5",
}


def _faixa_fixa(r12: float) -> int:
    """Faixa de corte fixo. Os limites sao fechados a direita, como os rotulos
    dizem: r = -0,5 e 'intensamente reversivel', r = 0 e 'moderadamente
    reversivel'."""
    for i, corte in enumerate(_CORTES_FIXOS):
        if r12 <= corte:
            return i + 1
    return len(_CORTES_FIXOS) + 1


def _pivot_mensal(decomposicao: pd.DataFrame, indice: str) -> pd.DataFrame:
    sub = decomposicao[decomposicao["indice"] == indice]
    piv = sub.pivot_table(index="date", columns="subitem_codigo", values="var_mensal")
    # Grade mensal completa: sem ela, um mes ausente faria a janela de 12 do
    # rolling abaixo atravessar o buraco sem reclamar, e o y/y sairia
    # encadeando meses nao contiguos.
    return piv.reindex(pd.date_range(piv.index.min(), piv.index.max(), freq="MS")).sort_index()


def _yoy(mensal: pd.Series) -> pd.Series:
    """Variacao acumulada em 12 meses. NaN onde a janela nao esta completa --
    o rolling propaga o NaN da grade, que e exatamente o que se quer."""
    fator = 1 + mensal / 100
    return (fator.rolling(12).apply(np.prod, raw=True) - 1) * 100


def _autocorr(y: pd.Series, lag: int, min_pares: int = _MIN_PARES) -> tuple[float | None, int]:
    """corr(y_t, y_{t-lag}) e quantos pares a sustentam.

    `shift` e posicional, mas a serie esta numa grade mensal completa, entao
    deslocar 12 posicoes e deslocar 12 meses.
    """
    par = pd.concat([y, y.shift(lag)], axis=1).dropna()
    if len(par) < min_pares:
        return None, len(par)
    a, b = par.iloc[:, 0], par.iloc[:, 1]
    if a.std() == 0 or b.std() == 0:
        return None, len(par)
    return float(a.corr(b)), len(par)


def _faixas_por_peso(ordenado: pd.DataFrame, n_faixas: int = _N_FAIXAS) -> list[int]:
    """Corta `ordenado` (ja em ordem crescente de r12) em faixas de ~1/n do PESO.

    Programacao dinamica exata sobre a soma dos desvios ao quadrado: `dp[j][i]`
    e o custo minimo de repartir os `i` primeiros subitens em `j` faixas, e o
    otimo global sai da reconstrucao. O(n_faixas x n^2) -- com ~380 subitens e 5
    faixas sao ~700 mil operacoes, vetorizadas por faixa, custo irrelevante
    perto do resto da geracao.

    Tres tentativas anteriores erraram, e as duas primeiras "parecem" certas:

      1. `int(peso_acumulado / total * n) + 1` -- empurra todo subitem de
         fronteira para a faixa seguinte. Medido: faixas de 16,5% a 23,4%.
      2. Guloso, cada fronteira indo para o lado que a deixa mais perto do
         proprio alvo. Melhor, mas ainda 21,9% contra 18,0%: o otimo de cada
         corte isolado nao e o otimo do conjunto.
      3. Descida coordenada sobre o MAIOR desvio. Some no caso mais simples que
         existe -- 100 subitens de peso igual devolviam [21, 20, 19, 20, 20] em
         vez de 20 em cada. O motivo e o objetivo minimax: se uma faixa ja esta
         a 0,01 do alvo, mover QUALQUER outro corte sozinho nao baixa o maximo,
         entao nenhuma troca individual melhora e a busca para longe do otimo.
         E exatamente o tipo de erro que so aparece num caso de teste
         construido a mao -- contra o banco real ela devolvia 0,94 p.p., que
         parecia bom o bastante.
    """
    peso = ordenado["peso"].to_numpy(dtype=float)
    n = len(peso)
    if n < n_faixas:
        return [1] * n
    cum = np.concatenate([[0.0], np.cumsum(peso)])
    alvo = cum[-1] / n_faixas

    dp = np.full((n_faixas + 1, n + 1), np.inf)
    veio_de = np.zeros((n_faixas + 1, n + 1), dtype=int)
    dp[0, 0] = 0.0
    for j in range(1, n_faixas + 1):
        # i so pode ir ate onde ainda sobra ao menos 1 subitem para cada faixa
        # restante -- e o que garante que nenhuma faixa saia vazia.
        for i in range(j, n - (n_faixas - j) + 1):
            ms = np.arange(j - 1, i)
            cand = dp[j - 1, ms] + (cum[i] - cum[ms] - alvo) ** 2
            k = int(np.argmin(cand))
            dp[j, i] = cand[k]
            veio_de[j, i] = ms[k]

    cortes = []
    i = n
    for j in range(n_faixas, 1, -1):
        i = int(veio_de[j, i])
        cortes.append(i)
    cortes.reverse()

    bordas = [0, *cortes, n]
    saida = [0] * n
    for f in range(n_faixas):
        for k in range(bordas[f], bordas[f + 1]):
            saida[k] = f + 1
    return saida


def calcular(decomposicao: pd.DataFrame) -> dict:
    """Payload da classificacao. `decomposicao` e o dataframe ja mesclado de
    _load_decomposicao() (inflc_decomposicao + inflc_dim)."""
    piv = _pivot_mensal(decomposicao, _INDICE_BASE)
    fim = piv.index.max()
    ini_yoy = fim - pd.DateOffset(months=_JANELA_YOY - 1)

    base = decomposicao[decomposicao["indice"] == _INDICE_BASE]
    ultimo = base[base["date"] == base["date"].max()]
    peso_ult = ultimo.set_index("subitem_codigo")["pesos"]
    nomes = decomposicao.drop_duplicates("subitem_codigo").set_index("subitem_codigo")["nome"]

    linhas = []
    for codigo in piv.columns:
        y = _yoy(piv[codigo])
        y = y[y.index >= ini_yoy]
        r12, n_pares = _autocorr(y, 12)
        if r12 is None:
            continue
        peso = peso_ult.get(codigo)
        if peso is None or pd.isna(peso) or peso <= 0:
            # Sem peso no mes corrente nao ha como alocar em faixa por peso.
            # Cai em "nao classificado" junto com os sem historia.
            continue
        linhas.append({"codigo": codigo, "r12": r12, "peso": float(peso), "n_pares": n_pares})

    res = pd.DataFrame(linhas).sort_values("r12").reset_index(drop=True)
    res["faixa"] = _faixas_por_peso(res)
    res["faixa_fixa"] = res["r12"].map(_faixa_fixa)

    faixas = []
    for q, g in res.groupby("faixa"):
        faixas.append({
            "q": int(q),
            "rotulo": _ROTULOS[int(q)],
            "n": int(len(g)),
            "peso": round(float(g["peso"].sum()), 8),
            "lo": round(float(g["r12"].min()), 4),
            "hi": round(float(g["r12"].max()), 4),
            "min_pares": int(g["n_pares"].min()),
        })

    # Uma faixa fixa pode sair VAZIA (nenhum subitem alem de +-0,5 numa janela
    # futura), e o front-end tem de receber a linha assim mesmo -- some-la faria
    # a tabela mudar de numero de linhas sem aviso.
    faixas_fixas = []
    for q in range(1, len(_CORTES_FIXOS) + 2):
        g = res[res["faixa_fixa"] == q]
        faixas_fixas.append({
            "q": q,
            "rotulo": _ROTULOS_FIXOS[q],
            "n": int(len(g)),
            "peso": round(float(g["peso"].sum()), 8),
            "lo": None if g.empty else round(float(g["r12"].min()), 4),
            "hi": None if g.empty else round(float(g["r12"].max()), 4),
        })

    todos = set(decomposicao["subitem_codigo"].unique())
    classificados = set(res["codigo"])
    nao = sorted(todos - classificados)

    return {
        "medida": "corr(yoy_t, yoy_t-12)",
        "janela": {
            "inicio": ini_yoy.strftime("%Y-%m"),
            "fim": fim.strftime("%Y-%m"),
            "n_pontos": _JANELA_YOY,
            "indice_base": _INDICE_BASE,
        },
        "min_pares": _MIN_PARES,
        "n_faixas": _N_FAIXAS,
        "rotulos": {str(k): v for k, v in _ROTULOS.items()},
        "faixas": faixas,
        "cortes_fixos": list(_CORTES_FIXOS),
        "rotulos_fixos": {str(k): v for k, v in _ROTULOS_FIXOS.items()},
        "faixas_fixas": faixas_fixas,
        # {codigo: [r12, faixa_por_peso, n_pares, faixa_fixa]} -- um codigo
        # ausente do dict E o descontinuado, e o front-end o trata assim.
        "subitens": {
            r.codigo: [round(r.r12, 4), int(r.faixa), int(r.n_pares), int(r.faixa_fixa)]
            for r in res.itertuples()
        },
        "pares_max": int(res["n_pares"].max()) if len(res) else 0,
        "n_classificados": int(len(res)),
        "nao_classificados": [
            {"codigo": c, "nome": (None if c not in nomes.index or pd.isna(nomes[c]) else str(nomes[c]))}
            for c in nao
        ],
    }


# ── Diagnostico: nao entra no relatorio, e o que o teste usa ──────────────────

def diagnostico(decomposicao: pd.DataFrame, n_permutacoes: int = 3, semente: int = 20260826) -> dict:
    """Mede o que justifica a escolha da medida, para o teste afirmar em cima:

    - `benchmark`: distribuicao de r12 quando a ordem temporal de cada subitem e
      destruida por permutacao. Se a medida fosse artefato de construcao, o real
      e o embaralhado coincidiriam.
    - `estabilidade`: a mesma medida estimada em duas janelas de 10 anos que nao
      se sobrepoem, e quanto a faixa sobrevive de uma para a outra.
    """
    rng = np.random.default_rng(semente)
    piv = _pivot_mensal(decomposicao, _INDICE_BASE)
    fim = piv.index.max()

    def r12_de(janela_piv: pd.DataFrame, ini) -> dict[str, float]:
        out = {}
        for c in janela_piv.columns:
            y = _yoy(janela_piv[c])
            y = y[y.index >= ini]
            v, _ = _autocorr(y, 12)
            if v is not None:
                out[c] = v
        return out

    ini = fim - pd.DateOffset(months=_JANELA_YOY - 1)
    real = r12_de(piv, ini)

    embaralhado = []
    for _ in range(n_permutacoes):
        emb = piv.copy()
        for c in emb.columns:
            vals = emb[c].dropna()
            emb.loc[vals.index, c] = rng.permutation(vals.values)
        embaralhado.extend(r12_de(emb, ini).values())

    # Duas janelas de 10 anos sem sobreposicao.
    fim_ant = fim - pd.DateOffset(months=_JANELA_YOY)
    ini_ant = fim_ant - pd.DateOffset(months=_JANELA_YOY - 1)
    antiga = r12_de(piv[piv.index <= fim_ant], ini_ant)

    comuns = sorted(set(real) & set(antiga))
    base = decomposicao[decomposicao["indice"] == _INDICE_BASE]
    peso_ult = base[base["date"] == base["date"].max()].set_index("subitem_codigo")["pesos"]

    def faixa_de(mapa: dict[str, float]) -> dict[str, int]:
        d = pd.DataFrame({"codigo": comuns, "r12": [mapa[c] for c in comuns]})
        d["peso"] = [float(peso_ult.get(c, 0) or 0) for c in comuns]
        d = d[d["peso"] > 0].sort_values("r12").reset_index(drop=True)
        d["faixa"] = _faixas_por_peso(d)
        return dict(zip(d["codigo"], d["faixa"]))

    fa, fb = faixa_de(antiga), faixa_de(real)
    pares = [(fa[c], fb[c]) for c in fa if c in fb]
    igual = sum(a == b for a, b in pares) / len(pares) if pares else float("nan")
    perto = sum(abs(a - b) <= 1 for a, b in pares) / len(pares) if pares else float("nan")
    q5 = [b for a, b in pares if a == 5]
    q5_fica = (sum(b == 5 for b in q5) / len(q5)) if q5 else float("nan")

    rr = pd.Series({c: real[c] for c in comuns})
    ra = pd.Series({c: antiga[c] for c in comuns})
    return {
        "real": {"n": len(real), "media": float(np.mean(list(real.values()))),
                 "dp": float(np.std(list(real.values()))),
                 "min": float(min(real.values())), "max": float(max(real.values()))},
        "benchmark": {"n": len(embaralhado), "media": float(np.mean(embaralhado)),
                      "dp": float(np.std(embaralhado))},
        "estabilidade": {
            "n": len(pares),
            "janela_antiga": f"{ini_ant:%Y-%m}→{fim_ant:%Y-%m}",
            "janela_nova": f"{ini:%Y-%m}→{fim:%Y-%m}",
            "corr": float(ra.corr(rr)), "spearman": float(ra.corr(rr, method="spearman")),
            "mesma_faixa": igual, "faixa_pm1": perto, "q5_continua_q5": q5_fica,
        },
    }
