# -*- coding: utf-8 -*-
"""Impulso-resposta: um choque numa variavel, e o que ele faz com as endogenas.

A aba **Impulso-resposta** do relatorio, pedida pelo usuario em 2026-09-28: *"Escolhemos a
variavel de choque (que recebera o choque) e como isso impacta cada variavel endogena.
Sendo que as variaveis exogenas tambem podem ser escolhidas para receber o choque. Os
choques podem ser modelados como temos na aba 'Structural Model' (...) o mesmo
esquema."* E, no meio do trabalho: *"eu quero poder ver e 'chocar' os subindices"*.

## O que e a resposta

A diferenca entre duas solucoes do mesmo sistema, com os mesmos pesos: a do cenario que a
aba Structural Model abre (tudo nas premissas padrao, as cinco equacoes ligadas) e a mesma
com o choque. Como o modelo nao e linear em tudo -- o cambio e nivel em log, o carry e uma
razao, o IPCA de 12 meses e composto --, a resposta depende um pouco do cenario de
partida, e e por isso que ela e medida contra ele e nao calculada em forma fechada.

## Onde o choque entra, decisao do usuario em 2026-09-28

- **Numa ENDOGENA, no residuo da equacao dela.** O perfil soma ao erro da equacao, antes
  de o valor virar defasagem, entao a propria dinamica o propaga: um choque de 1 p.p. em
  alimentacao com inercia 0,25 rende mais de 1 p.p. acumulado, e a regra de juros reage a
  inflacao resultante. E o impulso-resposta estrutural padrao. A curva de Phillips nao tem
  UM residuo, tem quatro -- os alvos sao os quatro grupos, que e o pedido dos subindices.
  O cheio responde como a soma ponderada dos quatro.
- **Numa EXOGENA, no caminho dela.** Nao ha equacao, entao o perfil soma ao caminho que o
  cenario padrao segura. Nas quatro que sao indice (dolar contra emergentes, S&P, as tres
  cestas de commodities) o perfil e em % do nivel, e nao em pontos: "+40 pontos de S&P" nao
  e uma pergunta que alguem faz.

A ressalva que a primeira opcao carrega, e que a tela diz: um choque PERMANENTE no residuo
da regra de juros vira ~7 p.p. de Selic no longo prazo, porque a suavizacao (t1 + t2 =
0,86) acumula o residuo. E o que um residuo permanente quer dizer; a forma natural ali e o
decaimento.

## Horizonte

**20 trimestres**, decisao do usuario no mesmo dia. O hiato tem meia-vida de 6 trimestres e
a Selic de uns 5: em 12 a maioria das respostas ainda nao voltou, e um impulso-resposta que
nao mostra a volta nao diz se ela acontece.

## O que roda onde

A conta roda no NAVEGADOR -- o usuario escolhe o alvo e a forma --, e aqui e a mesma conta,
para o teste conferir as duas pontas. `construir()` grava no payload os alvos, as respostas
e um GABARITO: cinco choques resolvidos aqui com os pesos da mediana, que o teste exige
iguais no JS. O gabarito de um passo de cada equacao nao alcanca o residuo novo, e o
`sistema_padrao` nao alcanca choque nenhum.

Uso:
    uv run python -m analytics.brasil.structural_model.irf
"""
from __future__ import annotations

import numpy as np

from analytics.brasil.structural_model import simulator as sm

H_IRF = 20

# Os tres perfis de choque, os MESMOS da aba Structural Model (`_simPerfilChoque`).
TIPOS = ("rampa", "decai", "const")

# O que a tela desenha, na ordem de solucao. `cheio` e o IPCA; os quatro grupos vem em
# seguida, num bloco proprio.
RESPOSTAS = (
    ("hiato", "Hiato do produto", "p.p. do produto potencial"),
    ("infl", "IPCA", "p.p."),
    ("pi_e", "Inflação esperada (Focus, 12 meses)", "p.p."),
    ("selic", "Selic", "p.p."),
    ("de", "Câmbio", "% do nível"),
)

# Os alvos de RESIDUO, um por equacao -- e quatro na (I), um por grupo. `v` e o tamanho
# padrao do choque, na unidade da equacao.
_RESIDUOS = (
    ("H", None, "Hiato do produto", "o hiato do produto", "p.p. do produto potencial", 1.0),
    ("I", "IS", "Serviços", "a inflação de serviços", "p.p. no trimestre", 1.0),
    ("I", "IA", "Alimentação", "a inflação de alimentação", "p.p. no trimestre", 1.0),
    ("I", "II", "Bens industriais", "a inflação de bens industriais", "p.p. no trimestre",
     1.0),
    ("I", "IM", "Monitorados", "a inflação de monitorados", "p.p. no trimestre", 1.0),
    ("E", None, "Inflação esperada (Focus, 12 meses)", "a inflação esperada",
     "p.p.", 1.0),
    ("R", None, "Selic", "a Selic", "p.p.", 1.0),
    ("F", None, "Câmbio", "o câmbio", "% de variação no trimestre", 5.0),
)

# O choque padrao ao abrir a aba: a regra de juros, 1 p.p. no residuo, passando a metade a
# cada trimestre. Ver `main()` para o que ele produz.
PADRAO = {"alvo": "res:R", "tipo": "decai", "v": 1.0, "n": 4, "rho": 0.5}


def perfil(c: dict, n: int) -> list:
    """O acrescimo trimestre a trimestre -- a MESMA conta de `_simPerfilChoque`."""
    rho = 0.8 if c.get("rho") is None else float(c["rho"])
    nn = max(1, int(c.get("n") or 1))
    v = float(c["v"])
    out = []
    for i in range(n):
        if c["tipo"] == "decai":
            out.append(v * rho ** i)
        elif c["tipo"] == "const":
            out.append(v if i < nn else v * rho ** (i - nn + 1))
        else:
            out.append(v * min(1.0, (i + 1) / nn))
    return out


def alvos(p: dict) -> list:
    """Os alvos possiveis: um residuo por equacao (quatro na (I)) e toda exogena."""
    out = []
    for ek, g, nome, frase, unid, v in _RESIDUOS:
        eq = p["eq"][ek]
        out.append({
            "key": "res:" + (g or ek), "tipo": "residuo", "eq": ek, "grupo": g,
            "nome": nome, "nome_frase": frase, "unidade": unid, "v": v,
            "regiao": None, "eq_nome": eq["nome"],
        })
    for k in p["var_ordem"]:
        var = p["var"][k]
        if var["tipo"] == "endogena":
            continue
        pct = var["unidade"] == "pontos do índice"
        out.append({
            "key": k, "tipo": "caminho", "var": k, "modo": "pct" if pct else "soma",
            "nome": var["nome"], "nome_frase": var["nome_frase"],
            "unidade": "% do nível" if pct else var["unidade"],
            "v": 10.0 if pct else round(4 * float(var["passo"]), 2),
            "regiao": var.get("regiao"), "eq_nome": None,
        })
    return out


def _estado(p: dict, coefs: dict, i0: int, h: int, ent: dict,
            choque: dict | None) -> dict:
    """O sistema resolvido, com o IPCA e os quatro grupos em variacao SIMPLES.

    Os grupos nao sao cartao, entao `resolver()` nao os devolve: a (I) roda uma vez mais
    sobre o sistema ja resolvido, com o mesmo choque, e isso nao muda nada -- o sistema e o
    ponto fixo dela.
    """
    sol, _ = sm.resolver(p, coefs, i0, h, ent, choque=choque)
    partes: list = []
    sm._sim_infl(p, coefs["I"], i0, h, sol, partes, eps=(choque or {}).get("I"))
    return {
        "hiato": list(sol["hiato"]), "pi_e": list(sol["pi_e"]),
        "selic": list(sol["selic"]), "ptax": list(sol["de"]),
        "infl": [pt["cheio"] for pt in partes],
        "grupos": {g: [pt["grupos"][g] for pt in partes]
                   for g in p["eq"]["I"]["ordem_grupos"]},
    }


def _doze(hist: list, cam: list, i0: int) -> list:
    """Doze meses compostos de quatro trimestres em variacao simples."""
    serie = list(hist[:i0]) + list(cam)
    out = []
    for j in range(len(cam)):
        acc = 1.0
        for t in range(i0 + j - 3, i0 + j + 1):
            acc *= 1.0 + serie[t] / 100.0
        out.append(100.0 * (acc - 1.0))
    return out


def _hist_cheio(p: dict, i0: int) -> list:
    return [None if v is None else 100.0 * (float(np.exp(v / 100.0)) - 1.0)
            for v in p["var"]["infl_br"]["obs"][:i0]]


def resposta(p: dict, coefs: dict, alvo: dict, c: dict, i0: int | None = None,
             h: int = H_IRF, base: dict | None = None) -> dict:
    """A resposta das endogenas a um choque, contra o cenario padrao."""
    i0 = p["i0"] if i0 is None else i0
    ent = sm.entradas(p, i0, h)
    if base is None:
        base = _estado(p, coefs, i0, h, ent, None)
    prof = perfil(c, h)
    choque = None
    if alvo["tipo"] == "residuo":
        choque = {alvo["eq"]: ({alvo["grupo"]: prof} if alvo["grupo"] else prof)}
    else:
        ent = dict(ent)
        cam = ent[alvo["var"]]
        ent[alvo["var"]] = ([x * (1.0 + s / 100.0) for x, s in zip(cam, prof)]
                            if alvo["modo"] == "pct"
                            else [x + s for x, s in zip(cam, prof)])
    cho = _estado(p, coefs, i0, h, ent, choque)

    eqi = p["eq"]["I"]
    hc = _hist_cheio(p, i0)
    out = {k: [a - b for a, b in zip(cho[k], base[k])] for k in ("hiato", "pi_e", "selic")}
    out["infl"] = [a - b for a, b in zip(cho["infl"], base["infl"])]
    out["infl12"] = [a - b for a, b in zip(_doze(hc, cho["infl"], i0),
                                           _doze(hc, base["infl"], i0))]
    out["de"] = [100.0 * (a / b - 1.0) for a, b in zip(cho["ptax"], base["ptax"])]
    out["grupos"], out["grupos12"] = {}, {}
    for g in eqi["ordem_grupos"]:
        hg = eqi["obs_grupo"][g]
        out["grupos"][g] = [a - b for a, b in zip(cho["grupos"][g], base["grupos"][g])]
        out["grupos12"][g] = [a - b for a, b in zip(_doze(hg, cho["grupos"][g], i0),
                                                    _doze(hg, base["grupos"][g], i0))]
    out["perfil"] = prof
    return out


# O gabarito: um choque de cada tipo de alvo e de cada forma, com os pesos da mediana.
_GABARITO = (
    ("res:R", {"tipo": "decai", "v": 1.0, "n": 4, "rho": 0.5}),
    ("res:IA", {"tipo": "const", "v": 1.0, "n": 4, "rho": 0.8}),
    ("res:F", {"tipo": "decai", "v": 5.0, "n": 4, "rho": 0.0}),
    ("ffr", {"tipo": "rampa", "v": 1.0, "n": 4, "rho": 0.8}),
    ("sp500", {"tipo": "decai", "v": -10.0, "n": 4, "rho": 0.8}),
)


def _r9(xs):
    return [round(float(x), 9) for x in xs]


def construir(p: dict) -> dict:
    """O bloco do payload: alvos, respostas, o choque padrao e o gabarito."""
    coefs = {k: dict(p["eq"][k]["mediana"]) for k in p["eq_ordem"]}
    al = alvos(p)
    por = {a["key"]: a for a in al}
    i0 = p["i0"]
    base = _estado(p, coefs, i0, H_IRF, sm.entradas(p, i0, H_IRF), None)
    gab = []
    for k, c in _GABARITO:
        r = resposta(p, coefs, por[k], c, i0, H_IRF, base)
        gab.append({
            "alvo": k, "choque": c,
            "resp": {**{n: _r9(r[n]) for n in ("hiato", "infl", "infl12", "pi_e",
                                               "selic", "de")},
                     "grupos": {g: _r9(v) for g, v in r["grupos"].items()},
                     "grupos12": {g: _r9(v) for g, v in r["grupos12"].items()}},
        })
    return {
        "h": H_IRF, "alvos": al, "padrao": dict(PADRAO), "tipos": list(TIPOS),
        "resp": [{"key": k, "nome": n, "unidade": u} for k, n, u in RESPOSTAS],
        "grupos": [{"key": g, "nome": p["eq"]["I"]["grupos"][g]["nome"]}
                   for g in p["eq"]["I"]["ordem_grupos"]],
        "gabarito": gab,
    }


def main() -> None:
    p = sm.construir()
    blk = construir(p)
    coefs = {k: dict(p["eq"][k]["mediana"]) for k in p["eq_ordem"]}
    por = {a["key"]: a for a in blk["alvos"]}
    print("IMPULSO-RESPOSTA, %d trimestres a partir de %s, pesos da mediana"
          % (H_IRF, sm._tri(p, p["i0"])))
    casos = [(k, c) for k, c in _GABARITO] + [
        ("res:R", {"tipo": "rampa", "v": 1.0, "n": 1}),
        ("res:IS", {"tipo": "decai", "v": 1.0, "rho": 0.0}),
        ("res:E", {"tipo": "decai", "v": 1.0, "rho": 0.5}),
        ("res:H", {"tipo": "decai", "v": 1.0, "rho": 0.5}),
    ]
    for k, c in casos:
        r = resposta(p, coefs, por[k], c)
        print("\n  %s  %s v=%s n=%s rho=%s" % (k, c["tipo"], c["v"], c.get("n"), c.get("rho")))
        for n in ("hiato", "infl", "infl12", "pi_e", "selic", "de"):
            s = np.array(r[n])
            j = int(np.argmax(np.abs(s)))
            print("    %-7s pico %+8.3f no tri %2d   tri 4 %+8.3f   tri 12 %+8.3f   tri 20 %+8.3f"
                  % (n, s[j], j + 1, s[3], s[11], s[19]))
        print("    grupos pico: " + "  ".join(
            "%s %+.3f" % (g, max(v, key=abs)) for g, v in r["grupos"].items()))


if __name__ == "__main__":
    main()
