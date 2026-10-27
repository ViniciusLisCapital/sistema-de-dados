"""
A consolidação de uma rodada do ciclo conjunto: os caminhos dos agentes viram P1, P2 ou PF*
(SISTEMA_AGENTES.md III.III.ii, IV.ii e IV.vi, decisões de 2026-10-22; PLANO_AGENTES.md Fase 9).

    uv run python -m analytics.agent_system.consolidacao --ciclo 2026-10-22 --rodada r1
    uv run python -m analytics.agent_system.consolidacao --ciclo 2026-10-22 --rodada rf --sem-faixa

Lê `obsidian/ciclos/<ciclo>/caminhos/<agente>_<rodada>.json` (um por agente, gravado por ele) e
a tutela de cada exógena da aba "Exógenas" do `repository/agent_mapping/data_tracker.xlsx`;
roda o Modelo Estrutural uma vez (`modelo.rodar`, sem multiplicadores) e grava
`obsidian/ciclos/<ciclo>/P1.md` (r1), `P2.md` (r2) ou `PF.md` (rf), com um `.json` ao lado.

O CONTRATO — o JSON que cada agente grava em cada rodada
---------------------------------------------------------

    {
      "agente": "cambio",                       # um de AGENTES
      "rodada": "r1",                           # r1 | r2 | rf; igual ao nome do arquivo
      "ciclo": "2026-10-22",                    # igual à pasta do ciclo
      "caminhos": {                             # só o cenário BASE, só as exógenas que o agente
        "vol": {"4T26": 13.5, "1T27": 13.0}     # quer escrever; chaves de modelo.exogenas(sim),
      },                                        # na convenção de modelo.CONVENCAO; trimestre
                                                # "4T26" ou "2026T4", dentro da janela do modelo;
                                                # depois do último dado, o valor é segurado
      "tese": {                                 # a distribuição, por variável e trimestre
        "ptax": {                               # variável do modelo que é do agente (ENDOGENA_DONO),
          "trimestres": {                       # uma exógena (fiscal e externo) ou uma variável
            "4T26": {"central": 5.21,           # própria da área (então com "nome" e "unidade")
                     "faixa": [5.10, 5.32],
                     "p_faixa": 55, "p_upside": 25, "p_downside": 20}
          }
        }
      },
      "nota": "opcional, texto livre"
    }

  - As caudas são de POSIÇÃO (SISTEMA III.III.i, decidido 2026-10-22):
    `p_upside` é a probabilidade de a variável fechar ACIMA da faixa (> faixa[1]), `p_downside`
    a de fechar ABAIXO dela (< faixa[0]). Nenhuma das duas é "a ruim": se uma cauda é boa ou
    ruim para o Brasil, o report diz em texto. Assimetria = (p_upside − p_downside) / 100.
  - Em cada trimestre: faixa[0] ≤ central ≤ faixa[1]; cada probabilidade entre 0 e 100, e as
    três (p_faixa, p_upside, p_downside) somam 100.
  - Quem tem variável no modelo escreve como central a do modelo (na rodada 1, a do G dele; da
    rodada 2 em diante, a do P anterior). Quem não tem (fiscal, externo) escreve a tese sobre a
    exógena de que é o principal, e a central é o próprio caminho base: o validador confere que é.
  - Chave, trimestre ou campo desconhecido levanta, com a lista de tudo o que está errado.

A CONTA
-------

  - Tutela (decisão de 2026-10-27, SISTEMA IV.ii): a aba "Exógenas", uma exógena por linha e os
    sete agentes nas colunas (achadas pelo nome, não pela letra). Cada exógena tem EXATAMENTE UM
    "Principal" (o responsável oficial pelo caminho) e zero ou mais "Subordinado" (dão insumos e
    argumentam; a decisão é do principal); em branco, o agente não tem papel na exógena. Zero ou
    mais de um Principal numa linha, ou qualquer outro valor, levanta. Nenhum dono em código.
  - Para cada exógena vale só o caminho do principal (o dele segurado depois do último dado).
    Antes do primeiro valor dele, e se o principal não escreveu caminho, vale o padrão do
    simulador, e o P avisa.
  - Divergência: todo agente que escreveu um caminho para uma exógena e cujo valor difere do
    usado num trimestre que ele escreveu entra na lista (agente, papel, exógena, trimestre, o
    valor dele, o usado, a diferença). O papel é "subordinado" ou "sem papel" (quem não tem papel
    na exógena). O P não o usa; a divergência é respondida na rodada seguinte (SISTEMA IV.ii).
  - Sem multiplicadores: o multiplicador fica no tempero de cada agente.
  - PF*: a central da rodada conjunta (dos caminhos dos reports finais) ao lado da distribuição de
    cada agente, como ele a escreveu. A faixa NÃO é deslocada para a central conjunta: a tabela
    mostra a diferença e marca quando a central conjunta cai fora da faixa do agente.

O vínculo agente ↔ variável é dado, em dois lugares só: a aba "Exógenas" (as exógenas) e
`ENDOGENA_DONO` abaixo (as endógenas, SISTEMA IV.ii, 2026-10-22).
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import math
import sys
import unicodedata
from pathlib import Path

from analytics.agent_system import modelo
from analytics.agent_system.dados import motor

# Os sete agentes do primeiro batch e o cabeçalho da coluna de cada um na aba "Exógenas".
AGENTES = {
    "cambio": "Câmbio",
    "politica_monetaria": "Política monetária",
    "inflacao": "Inflação",
    "atividade": "Atividade",
    "fiscal": "Fiscal",
    "externo": "Externo",
    "expectativas": "Expectativas",
}

# Endógena do modelo (a chave de modelo.SAIDAS) -> o agente da área (SISTEMA IV.ii, 2026-10-22).
# Fiscal e externo não têm: a tese deles é o caminho das exógenas de que são o principal.
ENDOGENA_DONO = {
    "ptax": "cambio",
    "selic": "politica_monetaria",
    "selic_fim": "politica_monetaria",
    "ipca_12m": "inflacao",
    # os quatro grupos do IPCA, como contribuição para o de 12 meses, e o resíduo dos trimestres
    # observados: decomposição da central da inflação (SISTEMA III.III.vii), sem faixa exigida
    "ipca_12m_servicos": "inflacao",
    "ipca_12m_alimentacao": "inflacao",
    "ipca_12m_industriais": "inflacao",
    "ipca_12m_monitorados": "inflacao",
    "ipca_12m_residuo": "inflacao",
    "ipca_tri": "inflacao",
    "focus_12m": "expectativas",
    "hiato": "atividade",
}

RODADAS = {"r1": ("P1", "da rodada 1"), "r2": ("P2", "da rodada 2"), "rf": ("PF", "do report final")}
TRACKER = motor.RAIZ / "repository" / "agent_mapping" / "data_tracker.xlsx"
ABA = "Exógenas"
HORIZONTE = 6            # os seis trimestres da tese, a partir do primeiro projetado
_TOL = 1e-6              # valores iguais até aqui não divergem
_CAMPOS = {"agente", "rodada", "ciclo", "caminhos", "tese", "nota"}
_CAMPOS_VAR = {"trimestres", "nome", "unidade", "nota"}
_CAMPOS_TRI = {"central", "faixa", "p_faixa", "p_upside", "p_downside"}


def _norm(s) -> str:
    s = unicodedata.normalize("NFKD", str(s or "")).encode("ascii", "ignore").decode()
    return " ".join(s.lower().split())


def _f(v, casas: int = 2, sinal: bool = False) -> str:
    return modelo._f(v, casas, sinal)


# ── a tutela, da aba "Exógenas" ───────────────────────────────────────────────
PRINCIPAL, SUBORDINADO = "principal", "subordinado"


def ler_tutela(path: Path | str = TRACKER) -> dict:
    """{"arquivo", "papeis": {exógena: {agente: "principal" | "subordinado"}}, "chaves": [...]}.

    Cada linha (exógena) tem exatamente um Principal e zero ou mais Subordinados; em branco, o
    agente não tem papel. Levanta se a aba não existir, se faltar a coluna de algum agente, se um
    valor não for Principal/Subordinado, e se alguma linha tiver zero ou mais de um Principal
    (quem preenche a aba é o usuário). Maiúsculas e acentos não importam."""
    import openpyxl

    path = Path(path)
    wb = openpyxl.load_workbook(path, read_only=True, data_only=True)
    try:
        if ABA not in wb.sheetnames:
            raise ValueError(f"{path.name} não tem a aba {ABA!r}.")
        linhas = list(wb[ABA].iter_rows(values_only=True))
    finally:
        wb.close()

    cab_i = next((i for i, r in enumerate(linhas) if r and _norm(r[0]) == "chave"), None)
    if cab_i is None:
        raise ValueError(f"aba {ABA!r}: não achei a linha de cabeçalho (primeira célula 'Chave').")
    cab = [_norm(c) for c in linhas[cab_i]]
    col = {}
    for ag, nome in AGENTES.items():
        if _norm(nome) not in cab:
            raise ValueError(f"aba {ABA!r}: falta a coluna {nome!r} (agente {ag}).")
        col[ag] = cab.index(_norm(nome))

    papeis: dict = {}
    chaves: list[str] = []
    erros = []
    for i, r in enumerate(linhas[cab_i + 1:], start=cab_i + 2):
        k = str(r[0]).strip() if r and r[0] is not None else ""
        if not k:
            continue
        if k in papeis:
            erros.append(f"linha {i}: exógena {k!r} repetida")
            continue
        chaves.append(k)
        papeis[k] = {}
        valor_ruim = False
        for ag, c in col.items():
            v = r[c] if c < len(r) else None
            if v is None or str(v).strip() == "":
                continue
            p = _norm(v)
            if p not in (PRINCIPAL, SUBORDINADO):
                erros.append(f"linha {i} ({k}), coluna {AGENTES[ag]!r}: valor {v!r}; vale "
                             "'Principal', 'Subordinado' ou em branco")
                valor_ruim = True
                continue
            papeis[k][ag] = p
        princ = [a for a, p in papeis[k].items() if p == PRINCIPAL]
        if len(princ) != 1 and not valor_ruim:
            erros.append(f"linha {i} ({k}): {len(princ)} agentes Principal"
                         + (f" ({', '.join(princ)})" if princ else "")
                         + "; cada exógena tem exatamente um")
    if erros:
        raise ValueError(f"aba {ABA!r} de {path.name}:\n  - " + "\n  - ".join(erros))
    if not papeis:
        raise ValueError(
            f"a aba {ABA!r} de {path} não tem nenhuma exógena. Quem preenche é o usuário: uma "
            "linha por exógena, com um 'Principal' e zero ou mais 'Subordinado' nas colunas dos "
            "agentes. A coluna 'Proposta' é só sugestão.")
    return {"arquivo": str(path), "papeis": papeis, "chaves": chaves}


# ── o modelo do ciclo: janela, exógenas e o padrão ────────────────────────────
def contexto(sim: dict) -> dict:
    """A janela do modelo, as exógenas (nome, unidade) e o caminho padrão de cada uma."""
    faltam = set(k for k, *_ in modelo.SAIDAS) ^ set(ENDOGENA_DONO)
    if faltam:
        raise ValueError(f"ENDOGENA_DONO não bate com modelo.SAIDAS em {sorted(faltam)}: uma saída "
                         "do modelo entrou ou saiu sem a declaração do dono acompanhar.")
    exo = modelo.exogenas(sim)
    janela = list(exo[0]["padrao"])
    return {"janela": janela,
            "exogenas": {e["chave"]: {"nome": e["nome"], "unidade": e["unidade"]} for e in exo},
            "padrao": {e["chave"]: [e["padrao"][t] for t in janela] for e in exo},
            "saidas": {k: {"nome": n, "unidade": u, "casas": c} for k, n, u, c in modelo.SAIDAS}}


def _tri(t, janela: list[str]) -> str:
    """'4T26' ou '2026T4' -> '4T26', dentro da janela; senão ValueError."""
    try:
        r = modelo._rotulo(*modelo._ler_tri(t))
    except (ValueError, AttributeError):
        raise ValueError(f"trimestre {t!r} inválido; escreva '4T26' ou '2026T4'") from None
    if r not in janela:
        raise ValueError(f"trimestre {t!r} fora da janela do modelo ({janela[0]} a {janela[-1]})")
    return r


def _num(v) -> bool:
    return isinstance(v, (int, float)) and not isinstance(v, bool) and math.isfinite(v)


def expandir(valores: dict, janela: list[str]) -> list[float | None]:
    """{trimestre: valor} -> um valor por trimestre da janela: None antes do primeiro dado,
    o último segurado depois (a mesma regra de `modelo.rodar`)."""
    out, atual = [], None
    for t in janela:
        if t in valores:
            atual = valores[t]
        out.append(atual)
    return out


# ── o contrato ────────────────────────────────────────────────────────────────
def validar(dados, ctx: dict, onde: str = "") -> dict:
    """O JSON de um agente, conferido e normalizado (trimestres como '4T26', números como float).
    Junta TODOS os erros numa mensagem só."""
    jan, erros = ctx["janela"], []
    e = erros.append
    if not isinstance(dados, dict):
        raise ValueError(f"{onde}: o arquivo tem de ser um objeto JSON")
    for c in sorted(set(dados) - _CAMPOS):
        e(f"campo desconhecido {c!r} (valem: {', '.join(sorted(_CAMPOS))})")
    ag = dados.get("agente")
    if ag not in AGENTES:
        e(f"agente {ag!r} desconhecido (valem: {', '.join(AGENTES)})")
    if dados.get("rodada") not in RODADAS:
        e(f"rodada {dados.get('rodada')!r} desconhecida (valem: {', '.join(RODADAS)})")

    caminhos: dict = {}
    cam = dados.get("caminhos")
    if not isinstance(cam, dict):
        e("'caminhos' tem de ser {exógena: {trimestre: valor}} (pode ser {})")
        cam = {}
    for k, vals in cam.items():
        if k not in ctx["exogenas"]:
            dica = (" é endógena: o modelo a resolve, o agente não a fixa" if k in ENDOGENA_DONO
                    else " não é exógena do modelo")
            e(f"caminhos: {k!r}{dica} (as exógenas: {', '.join(ctx['exogenas'])})")
            continue
        if not isinstance(vals, dict) or not vals:
            e(f"caminhos.{k}: tem de ser {{trimestre: valor}}, não vazio")
            continue
        caminhos[k] = {}
        for t, v in vals.items():
            try:
                tn = _tri(t, jan)
            except ValueError as err:
                e(f"caminhos.{k}: {err}")
                continue
            if not _num(v):
                e(f"caminhos.{k}.{t}: valor {v!r} não é número")
                continue
            if tn in caminhos[k]:
                e(f"caminhos.{k}: {tn} aparece duas vezes")
            caminhos[k][tn] = float(v)
        caminhos[k] = {t: caminhos[k][t] for t in jan if t in caminhos[k]}

    tese: dict = {}
    ts = dados.get("tese")
    if not isinstance(ts, dict) or not ts:
        e("'tese' tem de ser {variável: {trimestres}}, com ao menos uma variável")
        ts = {}
    for var, d in ts.items():
        if not isinstance(d, dict):
            e(f"tese.{var}: tem de ser um objeto")
            continue
        for c in sorted(set(d) - _CAMPOS_VAR):
            e(f"tese.{var}: campo desconhecido {c!r} (valem: {', '.join(sorted(_CAMPOS_VAR))})")
        if var in ENDOGENA_DONO:
            tipo = "modelo"
            if ag in AGENTES and ENDOGENA_DONO[var] != ag:
                e(f"tese.{var}: é a variável do modelo do agente {ENDOGENA_DONO[var]}, não de {ag}")
            nome, un = ctx["saidas"][var]["nome"], ctx["saidas"][var]["unidade"]
        elif var in ctx["exogenas"]:
            tipo = "exogena"
            nome, un = ctx["exogenas"][var]["nome"], ctx["exogenas"][var]["unidade"]
            if var not in caminhos:
                e(f"tese.{var}: tese sobre uma exógena exige o caminho base dela em 'caminhos' "
                  "(a central é o próprio caminho)")
        else:
            tipo = "propria"
            nome, un = d.get("nome"), d.get("unidade")
            if not nome or not un:
                e(f"tese.{var}: não é variável do modelo nem exógena; como variável própria da "
                  "área, precisa de 'nome' e 'unidade'")
        tris = d.get("trimestres")
        if not isinstance(tris, dict) or not tris:
            e(f"tese.{var}.trimestres: tem de ser {{trimestre: {{central, faixa, p_faixa, "
              "p_upside, p_downside}}}, não vazio")
            continue
        proprio = expandir(caminhos.get(var, {}), jan) if tipo == "exogena" else None
        out = {}
        for t, q in tris.items():
            w = f"tese.{var}.{t}"
            try:
                tn = _tri(t, jan)
            except ValueError as err:
                e(f"tese.{var}: {err}")
                continue
            if not isinstance(q, dict):
                e(f"{w}: tem de ser um objeto")
                continue
            for c in sorted(set(q) - _CAMPOS_TRI):
                e(f"{w}: campo desconhecido {c!r} (valem: {', '.join(sorted(_CAMPOS_TRI))})")
            for c in sorted(_CAMPOS_TRI - set(q)):
                e(f"{w}: falta {c!r}")
            if not _CAMPOS_TRI <= set(q):
                continue
            fx = q["faixa"]
            if not (isinstance(fx, list) and len(fx) == 2 and all(_num(x) for x in fx)):
                e(f"{w}.faixa: tem de ser [baixo, alto], dois números")
                continue
            ps = [q["p_faixa"], q["p_upside"], q["p_downside"]]
            if not _num(q["central"]) or not all(_num(p) for p in ps):
                e(f"{w}: central e probabilidades têm de ser números")
                continue
            lo, hi, c = float(fx[0]), float(fx[1]), float(q["central"])
            if not lo <= c <= hi:
                e(f"{w}: a faixa [{lo}; {hi}] não contém a central {c} (vale baixo ≤ central ≤ alto)")
            if any(not 0 <= p <= 100 for p in ps):
                e(f"{w}: probabilidade fora de 0 a 100: {ps}")
            if abs(sum(ps) - 100) > 0.01:
                e(f"{w}: p_faixa + p_upside + p_downside = {sum(ps):g}, não 100")
            if proprio is not None:
                j = jan.index(tn)
                if proprio[j] is None:
                    e(f"{w}: a central de uma exógena é o próprio caminho, e o caminho de {var} "
                      f"só começa depois de {tn}")
                elif abs(proprio[j] - c) > _TOL * max(1.0, abs(c)):
                    e(f"{w}: central {c} diferente do próprio caminho base ({proprio[j]}); numa "
                      "tese sobre exógena a central é o caminho")
            out[tn] = {"central": c, "faixa": [lo, hi], "p_faixa": float(ps[0]),
                       "p_upside": float(ps[1]), "p_downside": float(ps[2])}
        tese[var] = {"tipo": tipo, "nome": nome, "unidade": un,
                     "trimestres": {t: out[t] for t in jan if t in out}}
        if d.get("nota"):
            tese[var]["nota"] = d["nota"]

    if erros:
        raise ValueError(f"{onde}: contrato inválido:\n  - " + "\n  - ".join(erros))
    return {"agente": ag, "rodada": dados["rodada"], "ciclo": str(dados.get("ciclo")),
            "caminhos": caminhos, "tese": tese, "nota": dados.get("nota")}


def pasta(ciclo, raiz: Path | None = None) -> Path:
    return Path(raiz or motor.CICLOS) / str(ciclo)


def arquivo_caminhos(ciclo, agente: str, rodada: str, raiz: Path | None = None) -> Path:
    return pasta(ciclo, raiz) / "caminhos" / f"{agente}_{rodada}.json"


def ler_caminhos(ciclo, rodada: str, ctx: dict, raiz: Path | None = None) -> tuple[dict, list]:
    """({agente: JSON validado}, [agentes sem arquivo]). Levanta num arquivo da rodada com nome
    de agente desconhecido, ou cujo agente, rodada ou ciclo não batam com o nome e a pasta."""
    if rodada not in RODADAS:
        raise ValueError(f"rodada {rodada!r} desconhecida (valem: {', '.join(RODADAS)})")
    d = pasta(ciclo, raiz) / "caminhos"
    for arq in sorted(d.glob(f"*_{rodada}.json")) if d.exists() else []:
        if arq.stem[: -len(rodada) - 1] not in AGENTES:
            raise ValueError(f"{arq}: agente desconhecido no nome do arquivo (valem: "
                             f"{', '.join(AGENTES)})")
    lidos, faltam = {}, []
    for ag in AGENTES:
        arq = arquivo_caminhos(ciclo, ag, rodada, raiz)
        if not arq.exists():
            faltam.append(ag)
            continue
        try:
            bruto = json.loads(arq.read_text(encoding="utf-8"))
        except json.JSONDecodeError as err:
            raise ValueError(f"{arq}: não é JSON válido ({err})") from None
        v = validar(bruto, ctx, onde=str(arq))
        if (v["agente"], v["rodada"], v["ciclo"]) != (ag, rodada, str(ciclo)):
            raise ValueError(f"{arq}: o arquivo diz agente={v['agente']!r}, rodada={v['rodada']!r}, "
                             f"ciclo={v['ciclo']!r}; o nome e a pasta dizem {ag!r}, {rodada!r}, "
                             f"{str(ciclo)!r}")
        lidos[ag] = v
    return lidos, faltam


# ── a junção ──────────────────────────────────────────────────────────────────
def juntar(papeis: dict, caminhos: dict, janela: list[str], padrao: dict) -> tuple[dict, dict, list]:
    """Os caminhos que o P usa, de onde veio cada um e as divergências.

      papeis    {exógena: {agente: "principal" | "subordinado"}}, da aba "Exógenas"
      caminhos  {agente: {exógena: {trimestre: valor}}}, trimestres já normalizados
      padrao    {exógena: [valor por trimestre da janela]}, o padrão do simulador

    Devolve:
      usados       {exógena: {trimestre: valor}}, só as exógenas em que o principal escreveu
                   caminho, a partir do primeiro trimestre dele (antes vale o padrão do
                   simulador, que `modelo.rodar` aplica sozinho)
      origem       {exógena: {"tipo": "principal" | "padrão", "principal",
                   "por_trimestre": [[agentes] por trimestre], "valores": {agente: [...]}}}
      divergencias [{agente, exogena, papel, trimestre, valor, usado, diferenca, usado_de}]
    """
    usados, origem, div = {}, {}, []
    for k, pad in padrao.items():
        tut = papeis.get(k, {})
        princ = next((a for a, p in tut.items() if p == PRINCIPAL), None)
        escreveram = {a: c[k] for a, c in caminhos.items() if c.get(k)}
        if princ in escreveram:
            vals = {princ: expandir(escreveram[princ], janela)}
            por_tri, cam = [], {}
            for j, t in enumerate(janela):
                tem = vals[princ][j] is not None
                por_tri.append([princ] if tem else [])
                if tem:
                    cam[t] = vals[princ][j]
            usados[k] = cam
            origem[k] = {"tipo": "principal", "principal": princ,
                         "por_trimestre": por_tri, "valores": vals}
        else:
            origem[k] = {"tipo": "padrão", "principal": princ,
                         "por_trimestre": [[] for _ in janela], "valores": {}}
        de = f"{princ} (principal)" if k in usados else "padrão do simulador"
        for a in AGENTES:
            if a not in escreveram or (a == princ and k in usados):
                continue
            for t, v in escreveram[a].items():
                j = janela.index(t)
                u = usados.get(k, {}).get(t, pad[j])
                if abs(v - u) > _TOL * max(1.0, abs(u)):
                    div.append({"agente": a, "exogena": k, "papel": tut.get(a, "sem papel"),
                                "trimestre": t, "valor": v, "usado": u, "diferenca": v - u,
                                "usado_de": de if k in usados and origem[k]["por_trimestre"][j]
                                else "padrão do simulador"})
    return usados, origem, div


def _avisos(papeis: dict, lidos: dict, origem: dict, janela: list[str], ctx: dict,
            faltam: list, rodada: str, chaves_aba: list) -> list[str]:
    av = []
    for a in faltam:
        av.append(f"Sem `caminhos/{a}_{rodada}.json`: o agente {AGENTES[a]} não entrou nesta "
                  "consolidação (nem caminho, nem tese).")
    for k in ctx["exogenas"]:
        if k not in chaves_aba:
            av.append(f"`{k}` não está na aba {ABA!r}: tratada como sem tutela.")
    for k in chaves_aba:
        if k not in ctx["exogenas"]:
            av.append(f"`{k}` está na aba {ABA!r} mas não é exógena do modelo deste ciclo: ignorada.")
    for k in ctx["exogenas"]:
        tut, o = papeis.get(k, {}), origem[k]
        if not tut:
            av.append(f"`{k}`: sem tutela na aba {ABA!r}; ficou no padrão do simulador.")
            continue
        if o["tipo"] == "padrão":
            subs = [a for a, p in tut.items() if p == SUBORDINADO]
            av.append(f"`{k}`: o principal ({o['principal']}) não escreveu o caminho"
                      + (f" (subordinados: {', '.join(subs)})" if subs else "")
                      + "; ficou no padrão do simulador.")
            continue
        vazios = [janela[j] for j, q in enumerate(o["por_trimestre"]) if not q]
        if vazios:
            av.append(f"`{k}`: de {vazios[0]} a {vazios[-1]} no padrão do simulador; o caminho do "
                      "principal começa depois.")
    for a, c in lidos.items():
        for var, t in c["tese"].items():
            if t["tipo"] == "exogena" and a not in papeis.get(var, {}):
                av.append(f"{AGENTES[a]} escreveu tese sobre `{var}`, em que não tem papel.")
    return av


# ── o P ───────────────────────────────────────────────────────────────────────
def _central_p(var: str, tipo: str, res: dict, ctx: dict, usados: dict, j: int):
    """(central, baixo, alto) do P para a variável da tese no trimestre j."""
    if tipo == "modelo":
        e = res["endogenas"][var]
        return e["central"][j], (e.get("lo") or [None] * 99)[j], (e.get("hi") or [None] * 99)[j]
    if tipo == "exogena":
        t = ctx["janela"][j]
        return usados.get(var, {}).get(t, ctx["padrao"][var][j]), None, None
    return None, None, None


def _teses(lidos: dict, res: dict, ctx: dict, usados: dict) -> list[dict]:
    linhas = []
    for a, c in lidos.items():
        for var, t in c["tese"].items():
            for tri, q in t["trimestres"].items():
                j = ctx["janela"].index(tri)
                pc, plo, phi = _central_p(var, t["tipo"], res, ctx, usados, j)
                lo, hi = q["faixa"]
                linhas.append({
                    "agente": a, "variavel": var, "tipo": t["tipo"], "trimestre": tri,
                    **q, "assimetria": (q["p_upside"] - q["p_downside"]) / 100,
                    "central_p": pc, "lo_p": plo, "hi_p": phi,
                    "diferenca": None if pc is None else pc - q["central"],
                    "fora_da_faixa": pc is not None and not lo - _TOL <= pc <= hi + _TOL})
    return linhas


def _md(r: dict, ctx: dict, res: dict, lidos: dict) -> str:
    P, nome_rod = RODADAS[r["rodada"]]
    pf = r["rodada"] == "rf"
    rot = "PF*" if pf else P
    jan = ctx["janela"]
    hz = jan[:HORIZONTE]
    out = [f"# {rot} — consolidação {nome_rod} · ciclo {r['ciclo']}", ""]
    out.append(
        "Uma rodada do Modelo Estrutural com o caminho base de cada exógena vindo do agente "
        f"principal dela (aba {ABA!r} do `data_tracker.xlsx`; os subordinados dão insumos e "
        "argumentam, a decisão é do principal), sem "
        "multiplicadores: o multiplicador fica no tempero de cada agente."
        + (" Da rodada seguinte em diante, a central de quem tem variável no modelo é a deste "
           "arquivo." if not pf else
           " A central do PF* é a desta rodada conjunta, feita dos caminhos dos reports finais; a "
           "distribuição em volta dela é a de cada agente (seção 4)."))
    out += ["", f"Lidos: {', '.join(AGENTES[a] for a in lidos) or 'nenhum'}"
            + (f" · sem arquivo: {', '.join(AGENTES[a] for a in r['agentes_faltando'])}"
               if r["agentes_faltando"] else "")
            + f" · horizonte: {hz[0]} a {hz[-1]} (a janela inteira, até {jan[-1]}, está em "
            f"`{P}.json`) · gerado em {r['gerado_em']}"]

    out += ["", "## Avisos", ""]
    out += [f"- {a}" for a in r["avisos"]] or ["Nenhum."]

    out += ["", "## 1. Exógenas usadas", "",
            "| Exógena | De onde | " + " | ".join(hz) + " |",
            "|---|---|" + "---|" * len(hz)]
    for k, info in ctx["exogenas"].items():
        o = r["origem"][k]
        if o["tipo"] == "principal":
            de = f"{o['principal']} (principal)"
            vaz = [t for t, q in zip(jan, o["por_trimestre"]) if not q]
            if vaz:
                de += f"; padrão até {vaz[-1]}"
        else:
            de = "padrão do simulador"
        vals = [r["caminhos_usados"].get(k, {}).get(t, ctx["padrao"][k][j])
                for j, t in enumerate(hz)]
        out.append(f"| {info['nome']} ({info['unidade']}) `{k}` | {de} | "
                   + " | ".join(_f(v, 2) for v in vals) + " |")

    out += ["", "## 2. Saída do modelo", ""]
    txt = modelo.texto(res, hz)
    out.append(txt.split("\n\n**Exógenas do cenário**")[0])

    out += ["", "## 3. Divergências", "",
            "Quem escreveu, para uma exógena, um caminho diferente do usado (o do principal): um "
            "subordinado, ou um agente sem papel nela. O P usa o do principal; a divergência é "
            "respondida na rodada seguinte: o principal mantém ou muda o caminho, e diz por quê.", ""]
    if r["divergencias"]:
        out += ["| Agente | Exógena | Papel do agente | Trimestre | Valor do agente | Usado | "
                "Diferença | Usado de |", "|---|---|---|---|---|---|---|---|"]
        for d in r["divergencias"]:
            out.append(f"| {AGENTES[d['agente']]} | `{d['exogena']}` | "
                       f"{d['papel']} | {d['trimestre']} | "
                       f"{_f(d['valor'], 2)} | {_f(d['usado'], 2)} | {_f(d['diferenca'], 2, True)} | "
                       f"{d['usado_de']} |")
    else:
        out.append("Nenhuma.")

    out += ["", "## 4. " + ("A central conjunta e a distribuição de cada agente" if pf
                             else "As teses da rodada ao lado do P"), ""]
    if pf:
        out.append("A faixa e as probabilidades são as do report final de cada agente, escritas "
                   "em volta da central que ele tinha. Elas não foram deslocadas para a central "
                   "conjunta: a coluna da diferença diz quanto as duas se separam, e a marca "
                   "**fora da faixa** diz quando a central conjunta saiu da faixa do agente.")
    else:
        out.append("A central do report de cada agente ao lado da do P. Para quem tem variável no "
                   "modelo, a central da próxima rodada é a do P; a distância entre as duas mostra "
                   "o quanto os caminhos dos outros agentes moveram a variável.")
    cp = "Central do PF*" if pf else f"Central do {P}"
    por_var: dict = {}
    for ln in r["teses"]:
        por_var.setdefault((ln["agente"], ln["variavel"]), []).append(ln)
    for (a, var), lns in por_var.items():
        t = lidos[a]["tese"][var]
        casas = ctx["saidas"][var]["casas"] if t["tipo"] == "modelo" else 2
        out += ["", f"### {AGENTES[a]} — {t['nome']} ({t['unidade']})", "",
                f"| Trimestre | Central do agente | {cp} | Diferença | Faixa base · P | "
                "Downside · P | Upside · P | P(up) − P(down) |",
                "|---|---|---|---|---|---|---|---|"]
        for ln in lns:
            lo, hi = ln["faixa"]
            c_p = _f(ln["central_p"], casas)
            if ln["lo_p"] is not None:
                c_p += f" [{_f(ln['lo_p'], casas)}; {_f(ln['hi_p'], casas)}]"
            if ln["fora_da_faixa"]:
                c_p += " · **fora da faixa**"
            out.append(f"| {ln['trimestre']} | {_f(ln['central'], casas)} | {c_p} | "
                       f"{_f(ln['diferenca'], casas, True)} | {_f(lo, casas)} a {_f(hi, casas)} · "
                       f"{_f(ln['p_faixa'], 0)}% | abaixo de {_f(lo, casas)} · "
                       f"{_f(ln['p_downside'], 0)}% | acima de {_f(hi, casas)} · "
                       f"{_f(ln['p_upside'], 0)}% | {_f(ln['assimetria'], 2, True)} |")
        if t["tipo"] == "propria":
            out.append("\nVariável própria da área, fora do modelo: o P não tem central para ela.")
    return "\n".join(out) + "\n"


def consolidar(ciclo, rodada: str, raiz: Path | None = None, tracker: Path | str = TRACKER,
               sim: dict | None = None, faixa: bool = True, gravar: bool = True) -> dict:
    """Lê os caminhos da rodada e a tutela, roda o modelo e grava <P>.md e <P>.json na pasta do
    ciclo. Devolve o conteúdo do JSON, com "modelo" (o resultado de `modelo.rodar`) e "arquivos".

    `raiz` troca a pasta dos ciclos (testes); `sim` dá o retrato do simulador já carregado (por
    padrão, `modelo.carregar(ciclo)`, que lê de obsidian/ciclos/<ciclo>/dados/A/)."""
    if rodada not in RODADAS:
        raise ValueError(f"rodada {rodada!r} desconhecida (valem: {', '.join(RODADAS)})")
    ciclo = str(ciclo)
    tut = ler_tutela(tracker)            # antes do modelo: a aba vazia é o erro mais provável
    sim = sim if sim is not None else modelo.carregar(ciclo)
    if str(sim["ciclo"]) != ciclo:
        raise ValueError(f"o retrato do simulador é do ciclo {sim['ciclo']}, não de {ciclo}")
    ctx = contexto(sim)
    lidos, faltam = ler_caminhos(ciclo, rodada, ctx, raiz)
    if not lidos:
        raise FileNotFoundError(f"nenhum caminho {RODADAS[rodada][1]} em "
                                f"{pasta(ciclo, raiz) / 'caminhos'} (<agente>_{rodada}.json)")
    cams = {a: c["caminhos"] for a, c in lidos.items()}
    papeis = {k: v for k, v in tut["papeis"].items() if k in ctx["exogenas"]}
    usados, origem, div = juntar(papeis, cams, ctx["janela"], ctx["padrao"])
    res = modelo.rodar(sim, caminhos=usados, mult={}, faixa=faixa)
    P = RODADAS[rodada][0]
    r = {
        "ciclo": ciclo, "rodada": rodada, "p": P,
        "gerado_em": dt.datetime.now().isoformat(timespec="seconds"),
        "tracker": tut["arquivo"], "tutela": papeis,
        "agentes_lidos": list(lidos), "agentes_faltando": faltam,
        "caminhos_usados": usados, "origem": origem, "divergencias": div,
        "avisos": _avisos(papeis, lidos, origem, ctx["janela"], ctx, faltam, rodada, tut["chaves"]),
        "teses": _teses(lidos, res, ctx, usados),
        "contratos": lidos,
        "modelo": res,
    }
    if gravar:
        d = pasta(ciclo, raiz)
        d.mkdir(parents=True, exist_ok=True)
        md, js = d / f"{P}.md", d / f"{P}.json"
        md.write_text(_md(r, ctx, res, lidos), encoding="utf-8")
        js.write_text(json.dumps(r, ensure_ascii=False, indent=1, default=float), encoding="utf-8")
        r["arquivos"] = [str(md), str(js)]
    return r


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser(
        prog="python -m analytics.agent_system.consolidacao",
        description="Consolida uma rodada do ciclo (P1, P2 ou PF*). O caminho de cada exógena é o do "
                    "agente Principal dela na aba Exógenas do data_tracker.xlsx; subordinados dão "
                    "insumos e, se escreverem caminho diferente, viram divergência.")
    ap.add_argument("--ciclo", required=True, type=dt.date.fromisoformat)
    ap.add_argument("--rodada", required=True, choices=list(RODADAS))
    ap.add_argument("--tracker", type=Path, default=TRACKER)
    ap.add_argument("--sem-faixa", action="store_true", help="sem a faixa de 90%% (mais rápido)")
    a = ap.parse_args()
    try:
        r = consolidar(a.ciclo.isoformat(), a.rodada, tracker=a.tracker, faixa=not a.sem_faixa)
    except (ValueError, FileNotFoundError) as err:
        print(f"  erro: {err}")
        sys.exit(2)
    for arq in r["arquivos"]:
        print(f"  gravado  {arq}")
    print(f"  lidos {', '.join(r['agentes_lidos'])}"
          + (f" · sem arquivo: {', '.join(r['agentes_faltando'])}" if r["agentes_faltando"] else ""))
    print(f"  {len(r['divergencias'])} divergência(s) · {len(r['avisos'])} aviso(s)")
    for av in r["avisos"]:
        print(f"    - {av}")


if __name__ == "__main__":
    main()
