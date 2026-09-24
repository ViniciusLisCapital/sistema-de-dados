# -*- coding: utf-8 -*-
"""O simulador: roda as equacoes para a frente, em vez de so estima-las.

Hoje **uma equacao so**, a regra de juros (R), na versao bayesiana de
`bayes/taylor_bayes.py`. O plano do usuario, em 2026-09-22, e acrescentar uma de cada
vez: *"vamos ajeita-la e depois vamos adicionar outra equacao."*

## Dois blocos, e a razao de serem dois

Desenho pedido pelo usuario em 2026-09-22, depois de olhar o bloco de stress test do
`FX Report`:

- **As equacoes** -- uma por conta, com o que ela produz desenhado contra o observado.
  Os pesos sao os estimados e **nao sao controle**: o usuario decidiu isso em
  2026-09-22, *"a simulacao vem dos inputs"*. A equacao escrita, os pesos e a estimacao
  vivem na aba daquela equacao, e nao aqui.
- **Os inputs** -- uma por variavel que alimenta alguma conta, com o CAMINHO dela como
  controle. E aqui que o cenario se monta.

A separacao continua nao sendo cosmetica, so que o corte mudou de lugar: o bloco 1 e o
que o modelo AFIRMA e o bloco 2 e o que o usuario SUPOE. Um painel so -- que e o que o
simulador do `monetary_policy` faz -- nao distingue os dois.

## Endogena e exogena sao propriedades DO MODELO, e mudam

Uma variavel e endogena quando alguma equacao DO SIMULADOR a produz. Como as equacoes
entram uma de cada vez, a mesma variavel muda de lado ao longo do tempo -- e o payload
carrega os dois fatos separados, porque eles respondem perguntas diferentes:

    produzida_por     qual equacao do MODELO a produz, exista ela no simulador ou nao
    produtor_no_sim   se essa equacao ja esta no simulador

Hoje `di` (o desvio da inflacao esperada) tem `produzida_por="E"` e
`produtor_no_sim=False`: **ela e exogena hoje e endogena quando (E) entrar**. Escrever so
"exogena" no cartao mentiria por omissao -- e o dia em que (E) entrar e exatamente o dia
em que F2, F4, E6 e P13 voltam a ser decisao.

**E a ressalva que ja da para ver:** a equacao (E) explica a Focus de **12 meses**, e a
regra de juros consome a de **18 meses** (pendencia E6). Quando (E) entrar, ela nao
produz o objeto que (R) consome. Por isso `produzida_por` e uma afirmacao sobre qual
equacao e a candidata, e nao uma promessa de que o encaixe esta resolvido; `nota` diz
isso no cartao.

## As tres fontes de caminho de uma variavel

    equacao     ENDOGENO   -- o caminho sai de uma equacao DO SIMULADOR
    digitado    EXOGENO    -- o caminho e imposto, valor a valor
    observado   OBSERVADO  -- o que foi publicado e, passado o ultimo dado, o ultimo
                              valor repetido para a frente

Os rotulos na tela sao os tres em maiusculo inicial, a pedido do usuario em 2026-09-22.
As chaves continuam as antigas porque sao contrato entre o payload e o navegador -- o
nome que se le mora ao lado, no mapa `SIM_FONTE_ROT` do relatorio.

**"Endogeno" e propriedade DESTA RODADA, e o selo do cartao e propriedade do MODELO.**
Os dois podem discordar de proposito: a Selic e endogena na taxonomia e pode ser rodada
como exogena, que e o que desliga a regra de juros. Uma variavel que nenhuma equacao do
simulador produz nao recebe a pill "Endogeno" -- nao ha de onde.

## Composta: a mesma ideia do `carry_vol` do FX Report

Duas das entradas sao contas de outras duas:

    di      = pi_e_2a - meta_24m     expectativa de 18 meses contra a meta do horizonte
    ancora  = rr_10a  + meta_12m     juro real de equilibrio mais a meta

Estressar `rr*` sem mexer na meta e um cenario legitimo e diferente de estressar a soma,
entao as primitivas sao editaveis por baixo, como o "break down into parts" de la. A
formula vive no payload e a aritmetica no navegador -- sao duas contas de uma linha e
ida-e-volta de string de formula nao se paga.

## Horizonte

**Maximo de 12 trimestres**, decisao do usuario em 2026-09-22. Isso fixa o numero de
caixas por variavel em 12 e dispensa a logica de "o que acontece depois da ultima caixa",
que e onde o FX Report precisa de uma regra ("segue no ultimo valor").

**E a janela e FIXA: os `H_PADRAO` trimestres seguintes ao fim da janela estimada.**
Nao ha "comecar em" -- decisao do usuario em 2026-09-22, *"sempre projeta para frente da
janela estimada"*. Estimando ate 2026T2, a projecao e 2026T3..2029T2.

O que isso compra e a **pratica do FX Report**: a janela nao se mexe quando o dado anda,
entao o trimestre que sai passa a cair DENTRO dela. Um periodo da janela que ja tem dado
publicado aparece travado e verde -- o `final` do `FC.nowcast` de la, cuja razao esta
escrita no CSS daquele arquivo: *"so a guess never overrides data that's already known"*.
A tela se atualiza sozinha conforme o dado sai, sem reestimar e sem ninguem mexer num
seletor; reestimar move o corte e a janela anda junto.

**O preco, declarado:** nao da mais para rodar a conta sobre a historia pela tela. A
funcao continua aceitando qualquer `i0` -- e como `main()` e o teste a chamam -- mas a
pagina so oferece a janela a frente.

## O que roda onde

Nao ha MCMC na geracao do relatorio. Este modulo le `bayes/data/taylor_draws.json`,
gravado por `taylor_bayes.salvar_desenhos()`. A recursao roda no NAVEGADOR, porque o
usuario mexe nos controles; `_sim()` aqui e a mesma conta, e serve para o teste poder
conferir as duas pontas contra o mesmo caso.

Uso:
    uv run python -m analytics.brasil.structural_model.simulator
"""
from __future__ import annotations

import json
import pathlib

import numpy as np
import pandas as pd

from analytics.brasil.structural_model import panel
from analytics.brasil.structural_model.equations import taylor

DESENHOS = (pathlib.Path(__file__).resolve().parent / "bayes" / "data"
            / "taylor_draws.json")

# Horizonte, em trimestres. Comecou em 8 e foi a 12 no mesmo dia, a pedido do usuario
# -- tres anos. E o ponto de partida padrao e o PRIMEIRO TRIMESTRE APOS o ultimo dado:
# a aba abre projetando para a frente, e rodar sobre a historia e um backtest que se
# pede trocando o "Comecar em".
H_MAX = 12
H_PADRAO = 12

_COMO_GERAR = "uv run python -m analytics.brasil.structural_model.bayes.taylor_bayes"


def _ser(s: pd.Series) -> list:
    """Serie -> lista com None no lugar de NaN, que e o que o JSON aceita."""
    return [None if pd.isna(v) else round(float(v), 6) for v in s]


def carregar_desenhos(caminho: pathlib.Path | None = None) -> dict:
    """Le os desenhos gravados pela estimacao bayesiana."""
    caminho = caminho or DESENHOS
    if not caminho.exists():
        raise FileNotFoundError(
            "%s nao existe. O simulador nao roda MCMC durante a geracao do relatorio; "
            "gere os desenhos antes com:\n    %s" % (caminho, _COMO_GERAR))
    return json.loads(caminho.read_text(encoding="utf-8"))


# ─────────────────────────────────────────────────────────────────────────────
# as variaveis
# ─────────────────────────────────────────────────────────────────────────────
def _primitiva(key: str, nome: str, unidade: str, serie: pd.Series,
               fonte: str, desc: str) -> dict:
    return {"key": key, "nome": nome, "unidade": unidade, "fonte_dado": fonte,
            "desc": desc, "obs": _ser(serie)}


def _variaveis(df: pd.DataFrame, d: pd.DataFrame, am_idx) -> tuple[dict, list, dict]:
    """As entradas do modelo, com a classificacao e as primitivas de cada uma."""
    sub = df.reindex(am_idx)

    prim = {
        "pi_e_2a": _primitiva(
            "pi_e_2a", "Inflação esperada, Focus de 18 meses", "% a.a.",
            sub["pi_e_2a"], "Banco Central, pesquisa Focus",
            "A mediana do Focus para o IPCA acumulado em doze meses terminando daqui a "
            "vinte e quatro — o centro dessa janela está a dezoito meses, que é o "
            "horizonte efetivo."),
        "meta_24m": _primitiva(
            "meta_24m", "Meta de inflação no horizonte de 18 meses", "% a.a.",
            sub["meta_24m"], "CMN, via Banco Central",
            "A meta vigente no horizonte em que a expectativa é medida."),
        "rr_10a": _primitiva(
            "rr_10a", "Juro real de 10 anos (NTN-B)", "% a.a.",
            sub["rr_10a"], "B3, curva de NTN-B do arquivo de pregão",
            "O juro real de dez anos negociado no mercado. É o que faz as vezes de juro "
            "de equilíbrio — preço observado todo dia, não estimativa."),
        "meta_12m": _primitiva(
            "meta_12m", "Meta de inflação em 12 meses", "% a.a.",
            sub["meta_12m"], "CMN, via Banco Central",
            "A meta vigente no horizonte de doze meses, que entra na âncora."),
    }

    crises = {k: ["%dT%d" % (a.year, a.quarter), "%dT%d" % (b.year, b.quarter)]
              for k, (a, b) in taylor.CRISES.items()}
    for k, rot in (("d08", "Crise financeira de 2008"), ("d20", "Pandemia de 2020")):
        prim[k] = _primitiva(
            k, rot, "0 ou 1", d[k].reindex(am_idx),
            "Calendário — janela fixada na estimação",
            "Vale 1 nos trimestres de %s a %s e 0 no resto. Ligá-la num trimestre "
            "futuro é simular um choque daquele tamanho."
            % (crises[k][0], crises[k][1]))

    ordem = ["selic", "di", "ancora", "crise"]
    v = {
        "selic": {
            "key": "selic", "nome": "Selic", "unidade": "% ao ano",
            "tipo": "endogena", "produzida_por": "R", "produtor_no_sim": True,
            "obs": _ser(d["selic"].reindex(am_idx)),
            # A ordem e a das pills na tela: Endogeno, Exogeno, Observado.
            "fontes": ["equacao", "digitado", "observado"], "fonte_padrao": "equacao",
            "partes": None, "formula": None, "op": None, "passo": 0.25,
            "instrucao": "Digite a Selic média que você espera em cada trimestre, "
                         "em % ao ano.",
            "desc": "A taxa básica média do trimestre. É o que a regra de juros produz.",
            "nota": "Escolher Exógeno ou Observado **desliga a regra de "
                    "juros**: a Selic passa a ser imposta em vez de calculada. Com uma "
                    "equação só no simulador nada consome a Selic, então isso apenas "
                    "desenha o que você impôs. Passa a valer quando entrar uma equação "
                    "que leia a Selic — a curva IS é a candidata.",
        },
        "di": {
            "key": "di", "nome": "Inflação esperada menos a meta", "unidade": "p.p.",
            "tipo": "exogena", "produzida_por": "E", "produtor_no_sim": False,
            "obs": _ser(d["r2"].reindex(am_idx)),
            "fontes": ["digitado", "observado"], "fonte_padrao": "observado",
            "partes": ["pi_e_2a", "meta_24m"], "formula": "pi_e_2a - meta_24m",
            "op": "-",
            "passo": 0.1,
            "instrucao": "Digite quanto a inflação esperada fica acima (ou abaixo) da "
                         "meta em cada trimestre, em pontos percentuais.",
            "desc": "A distância entre a inflação que o mercado espera e a meta, no "
                    "mesmo horizonte. É o que tira a Selic do repouso.",
            "nota": "**Exógena hoje, endógena quando a equação de expectativas entrar "
                    "no simulador.** E há um encaixe a resolver antes disso: aquela "
                    "equação explica a Focus de 12 meses, e esta conta consome a de 18. "
                    "Ela não produz, hoje, o objeto que esta consome.",
        },
        "ancora": {
            "key": "ancora", "nome": "Âncora: juro real de equilíbrio mais a meta",
            "unidade": "% ao ano",
            "tipo": "exogena", "produzida_por": None, "produtor_no_sim": False,
            "obs": _ser(d["ancora"].reindex(am_idx)),
            "fontes": ["digitado", "observado"], "fonte_padrao": "observado",
            "partes": ["rr_10a", "meta_12m"], "formula": "rr_10a + meta_12m",
            "op": "+",
            "passo": 0.25,
            "instrucao": "Digite onde a Selic pararia se a inflação esperada estivesse "
                         "na meta, em % ao ano.",
            "desc": "Onde a Selic pararia se a inflação esperada estivesse na meta. "
                    "Não é estimada: é somada de duas séries observadas.",
            "nota": "Nenhuma equação deste modelo produz o juro real de equilíbrio — "
                    "ele é lido no preço da NTN-B de dez anos. Estimá-lo em vez de "
                    "escolher um proxy é pendência declarada (R12/H9). A meta é decisão "
                    "do CMN e é exógena por natureza.",
        },
        "crise": {
            "key": "crise", "nome": "Choques de crise", "unidade": "0 ou 1",
            "tipo": "exogena", "produzida_por": None, "produtor_no_sim": False,
            "obs": None,
            "fontes": ["digitado", "observado"], "fonte_padrao": "observado",
            "partes": ["d08", "d20"], "formula": None, "op": None, "passo": 1,
            "instrucao": "Marque 1 no trimestre em que quiser ligar aquela crise e 0 "
                         "no resto.",
            "desc": "As duas janelas de crise que a conta marca, cada uma com o próprio "
                    "peso estimado.",
            "nota": "Cada uma é 1 nos trimestres da sua janela e 0 no resto. Ligar uma "
                    "num trimestre futuro simula um choque **daquele tamanho** — o peso "
                    "não é escolhido, é o que a estimação mediu para aquela crise.",
        },
    }
    return v, ordem, prim


def _eq_juros(d: pd.DataFrame, am_idx, des: dict, est_idx) -> dict:
    """A equacao (R) como um item do bloco de equacoes."""
    return {
        "key": "R",
        "nome": "Regra de juros",
        "explica": "selic",
        "unidade": "% ao ano",
        "consome": ["di", "ancora", "crise"],
        "lags": ["t1", "t2"],
        "mult": "t3",
        "dummies": [c for c in taylor.CRISES if c in des["pars"]],
        "y": _ser(d["y"].reindex(am_idx)),
        "est_ini": "%dT%d" % (est_idx[0].year, est_idx[0].quarter),
        "est_fim": "%dT%d" % (est_idx[-1].year, est_idx[-1].quarter),
        "est_i0": int(am_idx.get_loc(est_idx[0])),
        "est_i1": int(am_idx.get_loc(est_idx[-1])),
        "caixa": des.get("caixa", {}),
        "mediana": des["mediana"],
        "hdi": des["hdi"],
        "hdi_prob": des["hdi_prob"],
        "pars": des["pars"],
        "draws": des["draws"],
        "n_draws": des["n_gravado"],
        "n_draws_total": des["n_total"],
        "priori": des["priori"],
        "amostra": des["gerado_de"],
    }


def construir(df: pd.DataFrame | None = None) -> dict:
    """Monta o payload do simulador: um bloco de equacoes e um de inputs."""
    if df is None:
        df = panel.construir()
    des = carregar_desenhos()

    d = taylor.montar(df)
    # O simulador precisa de toda linha em que a Selic e a ancora existam -- inclusive
    # as duas anteriores ao inicio da amostra de estimacao, que sao as condicoes
    # iniciais de qualquer partida naquele ponto.
    am = d[d["y"].notna()]
    est = d[["y", "r1", "r1b", "r2", "d08", "d20"]].dropna()

    v, ordem_v, prim = _variaveis(df, d, am.index)
    eq = _eq_juros(d, am.index, des, est.index)

    return {
        "h_padrao": H_PADRAO, "h_max": H_MAX,
        # O ponto de partida NAO e escolha de quem le: e o trimestre seguinte ao fim da
        # janela estimada, e so ele. Ver o bloco "Horizonte" no topo deste arquivo.
        "i0": int(am.index.get_loc(est.index[-1])) + 1,
        "x": [p.start_time.strftime("%Y-%m-%d") for p in am.index],
        "rot": ["%dT%d" % (p.year, p.quarter) for p in am.index],
        "eq_ordem": [eq["key"]],
        "eq": {eq["key"]: eq},
        "var_ordem": ordem_v,
        "var": v,
        "prim": prim,
    }


# ─────────────────────────────────────────────────────────────────────────────
# a recursao, que e a MESMA que o navegador roda
# ─────────────────────────────────────────────────────────────────────────────
def _sim(p: dict, coef: dict, i0: int, h: int, ent: dict) -> list:
    """Roda a regra de juros solta e devolve a Selic simulada.

    `ent` traz o caminho JA RESOLVIDO de cada entrada, com `h` valores: `di`, `ancora`
    e um por dummy. Resolver a fonte de cada variavel e trabalho de quem chama -- aqui
    so a conta.

    **As dummies de crise entram.** Deixa-las de fora nao levanta nada e custa caro: a
    primeira versao deste modulo as esquecia e a corrida solta acusava o maior desvio em
    2020T4, exatamente dentro da janela da `d20`.
    """
    eq = p["eq"]["R"]
    t1, t2, t3 = coef["t1"], coef["t2"], coef["t3"]
    y = [eq["y"][i0 - 2], eq["y"][i0 - 1]]
    peso = 1.0 - t1 - t2
    out = []
    for k in range(h):
        val = t1 * y[-1] + t2 * y[-2] + peso * t3 * ent["di"][k]
        for c in eq["dummies"]:
            dv = ent[c][k]
            if dv:
                val += coef.get(c, 0.0) * dv
        y.append(val)
        out.append(val + ent["ancora"][k])
    return out


def _observado(p: dict, key: str, i0: int, h: int) -> list:
    """O caminho observado de uma entrada, segurando o ultimo valor quando falta."""
    v = p["var"].get(key)
    serie = v["obs"] if v and v["obs"] is not None else p["prim"][key]["obs"]
    out, ult = [], 0.0
    for i in range(0, i0 + h):
        if i < len(serie) and serie[i] is not None:
            ult = serie[i]
        if i >= i0:
            out.append(ult)
    return out


def main() -> dict:
    p = construir()
    eq = p["eq"]["R"]
    n = len(p["x"])
    print("SIMULADOR")
    print("  grade      %s a %s, %d trimestres" % (p["rot"][0], p["rot"][-1], n))
    print("  horizonte  ate %d trimestres (default %d)" % (p["h_max"], p["h_padrao"]))

    print("\n  EQUACOES (%d)" % len(p["eq_ordem"]))
    for k in p["eq_ordem"]:
        e = p["eq"][k]
        md = e["mediana"]
        print("    (%s) %-16s explica %-7s consome %s"
              % (k, e["nome"], e["explica"], ", ".join(e["consome"])))
        print("         amostra %s a %s | %d desenhos, priori '%s'"
              % (e["est_ini"], e["est_fim"], e["n_draws"], e["priori"]))
        print("         t1 %+.3f  t2 %+.3f  t3 %+.3f" % (md["t1"], md["t2"], md["t3"]))

    print("\n  INPUTS (%d)" % len(p["var_ordem"]))
    print("    %-9s %-10s %-26s %s" % ("chave", "tipo", "produzida por", "partes"))
    for k in p["var_ordem"]:
        v = p["var"][k]
        prod = v["produzida_por"]
        quem = ("(%s), %s" % (prod, "no simulador" if v["produtor_no_sim"]
                              else "AINDA FORA do simulador")) if prod else "nenhuma"
        print("    %-9s %-10s %-26s %s"
              % (k, v["tipo"], quem, ", ".join(v["partes"] or []) or "-"))

    # Uma corrida solta com tudo no observado, para o modulo nao afirmar sem medir.
    i0, h = eq["est_i0"], p["h_padrao"]
    ent = {"di": _observado(p, "di", i0, h), "ancora": _observado(p, "ancora", i0, h)}
    for c in eq["dummies"]:
        ent[c] = _observado(p, c, i0, h)
    sim = _sim(p, eq["mediana"], i0, h, ent)
    obs = np.array(p["var"]["selic"]["obs"][i0:i0 + h], dtype=float)
    e = np.array(sim) - obs
    print("\n  corrida solta de %s, %d trimestres, tudo no observado:"
          % (p["rot"][i0], h))
    print("    erro medio absoluto %.3f p.p.   RMSE %.3f"
          % (np.abs(e).mean(), float(np.sqrt((e ** 2).mean()))))
    return p


if __name__ == "__main__":
    main()
