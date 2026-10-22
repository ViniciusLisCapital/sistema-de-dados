"""
As tabelas do agente de política monetária (SISTEMA_AGENTES.md V.II) e o F de cada uma.

A lista (quais tabelas) é decidida com o usuário e vive no SISTEMA_AGENTES.md; o gerador
levanta se esta declaração divergir dela. O tratamento (quais séries, que leitura) é do
sistema (IV.iv) e se ajusta pela qualidade do report.

Três coisas que valem para o arquivo inteiro:

  - A seção vai até o grupo "xi. Fora da lista": o que está ali é consulta livre, sem uso
    previsto, e não entra no F.
  - Tabela que o câmbio também lê sai da declaração DELE (`de(cambio, ...)` e
    `so(cambio, ...)`, do motor), trocando só as séries. A consulta fica idêntica, e o A
    do ciclo, que é compartilhado, serve aos dois. Onde a consulta tem de ser outra (a curva
    americana inteira, e não só três vértices), ela leva uma `variante` e vai para outro
    arquivo.
  - Profundidade (PRINCIPIOS I.II.vii): só o grupo "Endógeno" ganha a leitura completa;
    "Endógeno de câmbio", TWA e Exógeno, a enxuta. O motor decide pelo nome do grupo.
"""

from __future__ import annotations

from functools import partial

import numpy as np
import pandas as pd

from analytics.agent_system.dados import cambio
from analytics.agent_system.dados import especiais as esp
from analytics.agent_system.dados.motor import (Ctx, Serie, Tabela, antes, de, em, fdata, fmt,
                                                md_tabela, pctl, so)

SECAO = ("## (V.II) Agente de política monetária", "### xi. Fora da lista")
PIB = None   # o balanço de pagamentos em % do PIB é leitura do câmbio; aqui não há PIB em dólar

_BI = 1000.0  # R$ ou US$ milhões -> bilhões


def _s(chave, rotulo, unidade, leitura, **kw) -> Serie:
    return Serie(chave, rotulo, unidade, leitura, **kw)


def _modalidade(itens) -> tuple[Serie, ...]:
    """Séries de uma tabela de crédito por modalidade: (modalidade, métrica, rótulo)."""
    un = {"taxa_media": ("taxa", "% a.a.", "dif"),
          "inadimplencia": ("inadimplência", "% da carteira", "dif"),
          "saldo": ("saldo", "R$ bi", "pct"), "concessao": ("concessões", "R$ bi", "fluxo")}
    out = []
    for mod, met, rot in itens:
        nome, u, leit = un[met]
        out.append(_s(f"{mod}|{met}", f"{rot}: {nome}", u, leit,
                      escala=_BI if u == "R$ bi" else 1.0, casas=0 if met == "saldo" else 2))
    return tuple(out)


# ── F próprio das endógenas (leitura completa) ────────────────────────────────
def copom_decisoes(df: pd.DataFrame, ctx: Ctx) -> list[str]:
    """As últimas oito decisões e o ciclo em curso: desde quando, quantas reuniões, quanto."""
    r = df.sort_values("date").reset_index(drop=True)
    ult = r.tail(8).iloc[::-1]
    linhas = [{"Reunião": int(x.nro_reuniao), "Decisão": fdata(x.date),
               "Selic decidida (% a.a.)": fmt(x.selic_decidida),
               "Passo (p.b.)": f"{int(x.variacao_bps):+d}"} for x in ult.itertuples()]
    mov = r[r["variacao_bps"] != 0]
    out = md_tabela(linhas)
    if mov.empty:
        return out
    sinal = np.sign(mov["variacao_bps"].iloc[-1])
    k = len(mov) - 1
    while k > 0 and np.sign(mov["variacao_bps"].iloc[k - 1]) == sinal:
        k -= 1
    ini = mov.index[k]
    trecho = r.loc[ini:]
    antes_ini = r.loc[ini - 1, "selic_decidida"] if ini > 0 else None
    paradas = 0
    for v in r["variacao_bps"].iloc[::-1]:
        if v != 0:
            break
        paradas += 1
    acum = int(trecho["variacao_bps"].sum())
    txt = (f"Ciclo em curso: {'alta' if sinal > 0 else 'corte'} desde {fdata(r.loc[ini, 'date'])}, "
           f"{len(trecho)} reuniões, {acum:+d} p.b. acumulados (Selic de {fmt(antes_ini)}% "
           f"para {fmt(r['selic_decidida'].iloc[-1])}%).")
    if paradas:
        txt += f" As últimas {paradas} reuniões mantiveram a taxa."
    return out + ["", txt]


def copom_projecoes(df: pd.DataFrame, ctx: Ctx) -> list[str]:
    """O caminho projetado na reunião mais recente (IPCA, livres e administrados) e o
    horizonte relevante nas últimas oito reuniões, ao lado do passo decidido em cada uma."""
    ref = df[df["cenario"] == "juros_esperado"]
    if ref.empty:
        return ["Sem projeção no cenário com juros esperados."]

    def da_reuniao(d, nro):
        sub = d[d["nro_reuniao"] == nro]
        doc = "relatorio" if (sub["documento"] == "relatorio").any() else "comunicado"
        return sub[sub["documento"] == doc], doc

    nros = sorted(ref["nro_reuniao"].unique())
    sub, doc = da_reuniao(ref, nros[-1])
    larga = sub.pivot_table(index="date", columns="indice", values="value", aggfunc="last")
    hr = set(sub.loc[sub["horizonte_relevante"] == 1, "date"])
    tipo = sub.groupby("date")["periodo_tipo"].first()
    nomes = (("ipca", "IPCA"), ("ipca_livres", "Livres"), ("ipca_administrados", "Administrados"))
    linhas = []
    for d in larga.index:
        row = {"Período": esp._periodo(d, tipo[d])}
        for k, rot in nomes:
            row[f"{rot} (%)"] = fmt(larga[k].get(d) if k in larga else None, 1)
        row[""] = "horizonte relevante" if d in hr else ""
        linhas.append(row)
    meta = ctx.ler("inflc_meta").sort_values("date")
    out = [f"Reunião {nros[-1]} (de {fdata(sub['vintage'].iloc[0])}), "
           f"{'Relatório de Política Monetária' if doc == 'relatorio' else 'comunicado'}, "
           "cenário de referência (juros da Focus). Valor = acumulado em quatro trimestres. "
           f"Meta vigente: {fmt(meta['value'].iloc[-1])}%.", ""] + md_tabela(linhas)

    alt = df[(df["nro_reuniao"] == nros[-1]) & (df["cenario"] != "juros_esperado")
             & (df["indice"] == "ipca") & (df["horizonte_relevante"] == 1)]
    for x in alt.drop_duplicates("cenario").itertuples():
        out += ["", f"Cenário alternativo ({x.cenario.replace('_', ' ')}): IPCA de "
                    f"{fmt(x.value, 1)}% no horizonte relevante "
                    f"({esp._periodo(x.date, x.periodo_tipo)})."]

    dec = ctx.ler("pm_copom_reuniao").set_index("nro_reuniao")
    hist = []
    for nro in nros[-8:][::-1]:
        s, dc = da_reuniao(ref[ref["indice"] == "ipca"], nro)
        h = s[s["horizonte_relevante"] == 1]
        if h.empty:
            continue
        x = h.iloc[0]
        passo = dec["variacao_bps"].get(nro)
        hist.append({"Reunião": int(nro), "Documento": dc, "Data": fdata(x["vintage"]),
                     "Horizonte relevante": esp._periodo(x["date"], x["periodo_tipo"]),
                     "IPCA projetado (%)": fmt(x["value"], 1),
                     "Passo decidido (p.b.)": "—" if passo is None or pd.isna(passo)
                     else f"{int(passo):+d}"})
    return out + ["", "O horizonte relevante nas últimas reuniões (cenário de referência):",
                  ""] + md_tabela(hist)


def hiato(df: pd.DataFrame, ctx: Ctx) -> list[str]:
    """O hiato da última edição do RPM, nos últimos oito trimestres, com a dispersão publicada."""
    w = df.pivot_table(index="date", columns="variavel", values="value", aggfunc="last").sort_index()
    if "central" not in w:
        return ["Sem a estimativa central."]
    linhas = []
    for d, x in w.tail(8).iloc[::-1].iterrows():
        linhas.append({"Trimestre": esp._periodo(d, "trimestre"), "Central": fmt(x.get("central")),
                       "p25 a p75": f"{fmt(x.get('p25'))} a {fmt(x.get('p75'))}",
                       "Mín–máx": f"{fmt(x.get('minimo'))} a {fmt(x.get('maximo'))}"})
    c = w["central"].dropna()
    return [f"Edição de {fdata(df['vintage'].max())} do RPM. % do produto potencial; "
            "positivo = economia acima do potencial. A dispersão é a que o BC publica para "
            "o conjunto de estimativas.", ""] + md_tabela(linhas) + [
        "", f"Pctl hist. da central no último trimestre: {fmt(pctl(c, c.iloc[-1]), 0)} "
            f"({len(c)} trimestres, desde {esp._periodo(c.index[0], 'trimestre')})."]


def hiato_vintages(df: pd.DataFrame, ctx: Ctx) -> list[str]:
    """A revisão do hiato: a central de cada trimestre recente em cada uma das últimas edições."""
    c = df[df["variavel"] == "central"]
    w = c.pivot_table(index="date", columns="vintage", values="value", aggfunc="last").sort_index()
    eds = list(w.columns[-4:])
    if not eds:
        return []
    linhas = []
    for d, x in w.tail(6).iloc[::-1].iterrows():
        row = {"Trimestre": esp._periodo(d, "trimestre")}
        for v in eds:
            row[f"Edição {fdata(v)}"] = fmt(x.get(v))
        if len(eds) > 1:
            a, b = x.get(eds[-1]), x.get(eds[-2])
            row["Revisão na última (p.p.)"] = fmt(None if pd.isna(a) or pd.isna(b) else a - b, 2, True)
        linhas.append(row)
    return [f"{w.shape[1]} edições na tabela, desde {fdata(w.columns[0])}. Central, % do potencial.",
            ""] + md_tabela(linhas)


# ── F próprio dos TWA (leitura enxuta) ────────────────────────────────────────
def _texto(s: pd.Series) -> pd.Series:
    """Coluna de rótulo lida do csv: vazio vira "" e número vira "25", não "25.0"."""
    def um(v):
        if pd.isna(v):
            return ""
        try:
            f = float(v)
            return str(int(f)) if f == int(f) else str(f)
        except (TypeError, ValueError):
            return str(v)
    return s.map(um)


def qpc(df: pd.DataFrame, ctx: Ctx) -> list[str]:
    """O Questionário Pré-Copom mais recente: o que o mercado acha que o Copom fará e deveria
    fazer, as projeções e o hiato do mercado, o balanço de riscos e as variáveis estruturais."""
    df = df.copy()
    for c in ("referencia", "categoria", "estatistica", "variavel", "bloco"):
        df[c] = _texto(df[c])
    nros = sorted(df["nro_reuniao"].unique())
    n0 = nros[-1]
    n1 = nros[-2] if len(nros) > 1 else None
    q0 = df[df["nro_reuniao"] == n0]

    def val(q, bloco, var, ref="", est="mediana", cat=""):
        r = q[(q["bloco"] == bloco) & (q["variavel"] == var) & (q["estatistica"] == est)
              & (q["categoria"] == cat) & ((q["referencia"] == ref) if ref is not None else True)]
        return None if r.empty else float(r["valor"].iloc[0])

    def anterior(bloco, var, ref):
        """O valor no QPC mais recente antes deste que fez a mesma pergunta, e de qual reunião."""
        r = df[(df["nro_reuniao"] < n0) & (df["bloco"] == bloco) & (df["variavel"] == var)
               & (df["referencia"] == ref) & (df["estatistica"] == "mediana") & (df["categoria"] == "")]
        if r.empty:
            return "—"
        x = r.sort_values("nro_reuniao").iloc[-1]
        return f"{fmt(x['valor'])} (R{int(x['nro_reuniao'])})"

    out = [f"QPC da reunião {n0} (publicado em {fdata(q0['date'].max())})"
           + (f"; o anterior é o da reunião {n1}." if n1 else "."), ""]

    dec = q0[q0["bloco"] == "copom_decisao"]
    linhas = []
    for ref in sorted(dec["referencia"].unique(), key=lambda x: int(x[1:]) if x[1:].isdigit() else 0):
        row = {"Reunião": ref}
        for var, rot in (("fara", "Fará"), ("deveria", "Deveria")):
            r = dec[(dec["referencia"] == ref) & (dec["variavel"] == var)].copy()
            r["passo"] = pd.to_numeric(r["categoria"], errors="coerce")
            r = r.dropna(subset=["passo"])
            tot = r["valor"].sum()
            if not tot:
                row[rot] = "—"
                continue
            moda = r.loc[r["valor"].idxmax()]
            row[rot] = (f"{int(moda['passo']):+d} p.b. ({moda['valor'] / tot:.0%}); "
                        f"média {(r['passo'] * r['valor']).sum() / tot:+.0f}")
        linhas.append(row)
    out += ["Passo da Selic, em p.b.: a resposta mais frequente (fatia das respostas) e a média.",
            ""] + md_tabela(linhas) + [""]

    linhas = []
    for bloco, var, rot in (("ipca_horizonte_relevante", "ipca_4t", "IPCA no horizonte relevante, 4 trimestres (%)"),
                            ("hiato", "hiato", "Hiato do produto (% do potencial)"),
                            ("pib_trimestral", "qoq_sa", "PIB, trimestre contra o anterior, dessaz. (%)"),
                            ("ipca_curto_prazo", "ipca", "IPCA no mês (%)"),
                            ("ipca_curto_prazo", "media_nucleos", "Média dos núcleos no mês (%)"),
                            ("ipca_curto_prazo", "servicos_subjacentes", "Serviços subjacentes no mês (%)")):
        refs = sorted(q0.loc[(q0["bloco"] == bloco) & (q0["variavel"] == var), "referencia"].unique())
        for ref in refs:
            linhas.append({"Variável": rot, "Referência": ref, "Mediana": fmt(val(q0, bloco, var, ref)),
                           "p25 a p75": f"{fmt(val(q0, bloco, var, ref, 'p25'))} a "
                                        f"{fmt(val(q0, bloco, var, ref, 'p75'))}",
                           "Última vez perguntado": anterior(bloco, var, ref)})
    out += ["Medianas. \"Última vez perguntado\": o QPC anterior mais recente com a mesma pergunta "
            "e a mesma referência.", ""] + md_tabela(linhas) + [""]

    linhas = []
    for bloco, var in (("vies_ipca", "ipca"), ("vies_pib", "pib"),
                       ("ambiente_externo", "ambiente_externo"), ("situacao_fiscal", "situacao_fiscal")):
        r = q0[(q0["bloco"] == bloco) & (q0["estatistica"] == "fracao")]
        for ref, g in r.groupby("referencia"):
            linhas.append({"Pergunta": bloco.replace("_", " ") + (f" {ref}" if ref else ""),
                           "Respostas": "; ".join(f"{c.replace('_', ' ')} {v:.0%}"
                                                  for c, v in zip(g["categoria"], g["valor"]))})
    out += ["Balanço de riscos e avaliação do cenário, fatia das respostas:", ""] + md_tabela(linhas) + [""]

    linhas = []
    for var, rot in (("juro_real_neutro", "Juro real neutro (% a.a.)"),
                     ("pib_potencial", "Crescimento do PIB potencial (%)"),
                     ("nairu", "Taxa de desemprego neutra (%)")):
        r = df[(df["variavel"] == var) & (df["estatistica"] == "mediana")]
        if r.empty:
            continue
        nro = r["nro_reuniao"].max()
        for x in r[r["nro_reuniao"] == nro].itertuples():
            ant = r[(r["nro_reuniao"] < nro) & (r["referencia"] == x.referencia)].sort_values("nro_reuniao")
            linhas.append({"Variável estrutural": rot, "Horizonte": x.referencia.replace("_", " ") or "—",
                           "Mediana": fmt(x.valor), "QPC": f"R{int(nro)} ({fdata(x.date)})",
                           "Na pergunta anterior": "—" if ant.empty else
                           f"{fmt(ant['valor'].iloc[-1])} (R{int(ant['nro_reuniao'].iloc[-1])})"})
    if linhas:
        out += ["Perguntadas só em algumas reuniões; vale a mais recente:", ""] + md_tabela(linhas)
    return out


def _por_classe(dec: pd.DataFrame, dim: pd.DataFrame) -> pd.DataFrame:
    """Variação mensal (%) de cada recorte do BC, ponderada pelos pesos do próprio mês."""
    d = dec.assign(sub=dec["subitem_codigo"].astype(str)).merge(
        dim.assign(sub=dim["subitem_codigo"].astype(str))[["sub", "subgrupo", "subjacente"]],
        on="sub", how="left")
    recortes = {"Alimentação": d["subgrupo"] == "Alimentos",
                "Bens industriais": d["subgrupo"] == "Bens Industriais",
                "Serviços": d["subgrupo"] == "Serviços",
                "Monitorados": d["subgrupo"] == "Monitorados",
                "Serviços subjacentes": d["subjacente"] == "Serviços Subjacente",
                "Industriais subjacentes": d["subjacente"] == "Bens Industriais Subjacente"}
    d = d.assign(pv=d["pesos"] * d["var_mensal"])
    cols = {}
    for nome, m in recortes.items():
        g = d[m].groupby("date")[["pv", "pesos", "contribuicao"]].sum()
        cols[nome] = g["pv"] / g["pesos"]
        cols[nome + "|contrib"] = g["contribuicao"]
    return pd.DataFrame(cols).sort_index()


def _acum(x: pd.Series) -> float | None:
    return None if len(x) == 0 or x.isna().any() else float((np.prod(1 + x / 100) - 1) * 100)


def inflc_decomposicao(df: pd.DataFrame, ctx: Ctx) -> list[str]:
    """O IPCA nos recortes que a ata cita, refeitos dos subitens com a classificação do BC,
    e os subitens que mais pesaram no último mês."""
    dec = df[df["indice"] == "IPCA"]
    dim = ctx.ler("inflc_dim")
    t = _por_classe(dec, dim)
    t0 = t.index[-1]
    linhas = []
    for nome in [c for c in t.columns if "|" not in c]:
        s = t[nome]
        linhas.append({"Recorte do BC": nome, "Mês": f"{t0:%Y-%m}", "Último mês (%)": fmt(s.iloc[-1]),
                       "Acum. 3m": fmt(_acum(s.iloc[-3:])), "Acum. 12m": fmt(_acum(s.iloc[-12:])),
                       "Acum. 12m, 3 meses antes": fmt(_acum(s.iloc[-15:-3]) if len(s) >= 15 else None),
                       "Contribuição no mês (p.p.)": fmt(t[nome + "|contrib"].iloc[-1])})
    ult = dec[dec["date"] == dec["date"].max()].assign(sub=lambda x: x["subitem_codigo"].astype(str))
    nomes = dim.assign(sub=dim["subitem_codigo"].astype(str)).set_index("sub")["nome"]
    ult = ult.assign(nome=ult["sub"].map(nomes)).sort_values("contribuicao")

    def tab(x):
        return md_tabela([{"Subitem": r.nome, "Var. no mês (%)": fmt(r.var_mensal),
                           "Peso (%)": fmt(r.pesos * 100), "Contribuição (p.p.)": fmt(r.contribuicao, 3)}
                          for r in x.itertuples()])
    return (["IPCA. Recortes refeitos dos subitens com a classificação do BC (`inflc_dim`); "
             "variação ponderada pelos pesos do mês. Sem ajuste sazonal.", ""] + md_tabela(linhas)
            + ["", f"Maiores contribuições para cima em {t0:%Y-%m}:", ""] + tab(ult.iloc[::-1].head(5))
            + ["", "Maiores contribuições para baixo:", ""] + tab(ult.head(5)))


def inflc_decomposicao_item(df: pd.DataFrame, ctx: Ctx) -> list[str]:
    """Os itens do IPCA que mais contribuíram no último mês, para cima e para baixo."""
    d = df[df["indice"] == "IPCA"].assign(item=lambda x: x["item_codigo"].astype(str))
    dim = ctx.ler("inflc_dim")
    nomes = (dim.assign(item=dim["subitem_codigo"].astype(str).str[:4])
             .drop_duplicates("item").set_index("item")["ibge_item"])
    larga = d.pivot_table(index="date", columns="item", values="var_mensal", aggfunc="last").sort_index()
    t0 = d["date"].max()
    ult = d[d["date"] == t0].assign(nome=lambda x: x["item"].map(nomes))
    ult = ult.reindex(ult["contribuicao"].abs().sort_values(ascending=False).index).head(8)
    linhas = [{"Item": r.nome if isinstance(r.nome, str) else r.item, "Var. no mês (%)": fmt(r.var_mensal),
               "Acum. 12m (%)": fmt(_acum(larga[r.item].iloc[-12:])),
               "Peso (%)": fmt(r.pesos * 100), "Contribuição (p.p.)": fmt(r.contribuicao, 3)}
              for r in ult.itertuples()]
    return [f"IPCA de {t0:%Y-%m}: os oito itens de maior contribuição, em valor absoluto.", ""] + md_tabela(linhas)


def inflc_dim(df: pd.DataFrame, ctx: Ctx) -> list[str]:
    """A classificação do BC: quantos subitens e quanto peso em cada classe, no último IPCA."""
    dec = ctx.ler("inflc_decomposicao")
    dec = dec[(dec["indice"] == "IPCA") & (dec["date"] == dec["date"].max())]
    pesos = dec.assign(sub=dec["subitem_codigo"].astype(str)).set_index("sub")["pesos"]
    d = df.assign(sub=df["subitem_codigo"].astype(str), item=df["item"].fillna("—"))
    d = d.assign(peso=d["sub"].map(pesos))
    g = d.groupby(["subgrupo", "item"]).agg(n=("sub", "size"), no_mes=("peso", "count"),
                                            peso=("peso", "sum")).reset_index()
    linhas = [{"Grupo do BC": r.subgrupo, "Classe": r.item, "Subitens": int(r.n),
               "No IPCA do mês": int(r.no_mes), "Peso (%)": fmt(r.peso * 100, 1)}
              for r in g.itertuples()]
    return [f"Peso no IPCA de {dec['date'].max():%Y-%m}. A tabela guarda subitens que já saíram "
            "da cesta; só os do mês têm peso.", ""] + md_tabela(linhas)


def _soma4(df: pd.DataFrame, nome: str) -> pd.Series:
    s = df[df["name"] == nome].set_index("date")["value"].sort_index()
    return s.rolling(4).sum()


def pib_correntes(df: pd.DataFrame, ctx: Ctx) -> list[str]:
    """Os pesos de cada componente da demanda no PIB, em quatro trimestres."""
    pib = _soma4(df, "pib_pm").dropna()
    t0 = pib.index[-1]
    linhas = []
    for nome, rot in (("consumo_familias", "Consumo das famílias"), ("consumo_adm_publica", "Consumo do governo"),
                      ("fbcf", "Formação bruta de capital fixo"), ("variacao_estoque", "Variação de estoques"),
                      ("exportacao", "Exportação"), ("importacao", "Importação")):
        s = _soma4(df, nome) / pib * 100
        linhas.append({"Componente": rot, f"% do PIB, 4 tri até {esp._periodo(t0, 'trimestre')}": fmt(em(s, t0), 1),
                       "Um ano antes": fmt(em(s, antes(t0, 12)), 1)})
    return [f"Preços correntes. PIB de 4 trimestres: R$ {pib.iloc[-1] / 1e6:.2f} tri.", ""] + md_tabela(linhas)


def renda_poupanca(df: pd.DataFrame, ctx: Ctx) -> list[str]:
    """Poupança, investimento e capacidade de financiamento em % do PIB, em quatro trimestres."""
    pib = _soma4(df, "pib").dropna()
    t0 = pib.index[-1]
    linhas = []
    for nome, rot in (("poupanca_bruta", "Poupança bruta"), ("formacao_bruta_capital", "Formação bruta de capital"),
                      ("capacidade_liquida_financiamento", "Capacidade (+) ou necessidade (−) de financiamento"),
                      ("rendas_propriedade_exterior", "Rendas de propriedade líquidas com o exterior (− = envio)")):
        s = _soma4(df, nome) / pib * 100
        v0, v1 = em(s, t0), em(s, antes(t0, 12))
        linhas.append({"Conta": rot, f"% do PIB, 4 tri até {esp._periodo(t0, 'trimestre')}": fmt(v0, 1),
                       "Um ano antes": fmt(v1, 1),
                       "Δ (p.p.)": fmt(None if v0 is None or v1 is None else v0 - v1, 1, True)})
    return ["Contas nacionais trimestrais, preços correntes.", ""] + md_tabela(linhas)


def dlsp_fatores(df: pd.DataFrame, ctx: Ctx) -> list[str]:
    """O que moveu a dívida líquida nos últimos 12 meses, fator a fator, em R$ e em % do PIB."""
    tot = df[df["item"] == "total"].pivot_table(index="date", columns="fator", values="value",
                                                aggfunc="last").sort_index()
    if tot.empty:
        return ["Sem o item total."]
    t0 = tot.index[-1]
    pib = ctx.serie("atv_pib_mensal", "pib_acum_12m")
    p = em(pib, t0)
    rot = {"primario": "Resultado primário (+ = déficit)", "juros": "Juros nominais",
           "ajuste_met_externo": "Ajuste cambial da dívida externa",
           "ajuste_met_interno": "Ajuste da dívida interna indexada",
           "ajuste_paridade": "Ajuste de paridade da cesta de moedas",
           "reconhecimento_dividas": "Reconhecimento de dívidas", "privatizacoes": "Privatizações",
           "ajuste_caixa_competencia": "Ajuste caixa-competência"}
    linhas = []
    for f, r in rot.items():
        if f not in tot:
            continue
        s12 = tot[f].iloc[-12:].sum()
        s12a = tot[f].iloc[-24:-12].sum() if len(tot) >= 24 else None
        linhas.append({"Fator": r, "Último mês (R$ bi)": fmt(tot[f].iloc[-1] / _BI, 1),
                       "12m (R$ bi)": fmt(s12 / _BI, 1),
                       "12m % do PIB": fmt(s12 / p * 100 if p else None, 2),
                       "12m, um ano antes (R$ bi)": fmt(None if s12a is None else s12a / _BI, 1)})
    est = tot["estoque"].iloc[-1] if "estoque" in tot else None
    return [f"Setor público consolidado, até {t0:%Y-%m}. Fluxo que AUMENTA a dívida é positivo. "
            f"Estoque da dívida líquida: R$ {fmt(None if est is None else est / 1e6, 2)} tri.", ""] + md_tabela(linhas)


def efgg(df: pd.DataFrame, ctx: Ctx) -> list[str]:
    """O governo geral (classificação do FMI) em quatro trimestres, em % do PIB. O `geral_` da
    tabela é a SOMA de União, estados e municípios, sem consolidar as transferências entre
    eles: receita e despesa saem maiores que as do governo geral consolidado."""
    pib = _soma4(ctx.ler("atv_pib_valores_correntes"), "pib_pm").dropna()
    t0 = df["date"].max()
    p0, p1 = em(pib, t0), em(pib, antes(t0, 12))
    linhas = []
    for nome, rot in (("geral_receita_total", "Receita total"), ("geral_despesa_total", "Despesa total"),
                      ("geral_juros", "Juros"), ("geral_beneficios_previdenciarios_assistenciais",
                                                 "Benefícios previdenciários e assistenciais"),
                      ("geral_remuneracao_empregados", "Remuneração de empregados"),
                      ("geral_investimento_liquido", "Investimento líquido")):
        s = _soma4(df, nome)
        v0 = em(s, t0) / p0 * 100 if p0 and em(s, t0) is not None else None
        v1 = em(s, antes(t0, 12)) / p1 * 100 if p1 and em(s, antes(t0, 12)) is not None else None
        linhas.append({"Conta": rot, f"% do PIB, 4 tri até {esp._periodo(t0, 'trimestre')}": fmt(v0, 1),
                       "Um ano antes": fmt(v1, 1),
                       "Δ (p.p.)": fmt(None if v0 is None or v1 is None else v0 - v1, 1, True)})
    return ["Governo geral (GFSM) = soma de União, estados e municípios, SEM consolidar as "
            "transferências entre esferas: receita e despesa ficam acima das do governo geral "
            "consolidado; leia a variação, não o nível. Soma de quatro trimestres sobre o PIB "
            "nominal dos mesmos quatro.", ""] + md_tabela(linhas)


# ── a declaração ──────────────────────────────────────────────────────────────
TABELAS: list[Tabela] = [
    # ── i. Endógeno ──────────────────────────────────────────────────────────
    de(cambio, "pm_copom_calendario", especial=partial(esp.copom_calendario, proximas=None)),
    de(cambio, "pm_copom_reuniao", especial=copom_decisoes),
    de(cambio, "pm_copom_projecoes", especial=copom_projecoes),
    Tabela("pm_hiato_produto", corte="vintage", especial=hiato),
    Tabela("pm_hiato_produto_vintages", corte="vintage", especial=hiato_vintages),
    Tabela("br_interest_rate", dims=("curve", "tenor"), series=(
        _s("POLICY|1d", "Selic, meta", "% a.a.", "dif"),
        *[_s(f"DIPRE|{t}", f"DI × pré {r}", "% a.a.", "dif")
          for t, r in (("3M", "3 meses"), ("6M", "6 meses"), ("12M", "1 ano"), ("24M", "2 anos"),
                       ("60M", "5 anos"), ("120M", "10 anos"))],
        *[_s(f"NTNBJS|{t}", f"NTN-B {r} (juro real)", "% a.a.", "dif")
          for t, r in (("12M", "1 ano"), ("24M", "2 anos"), ("60M", "5 anos"), ("120M", "10 anos"))],
    )),
    de(cambio, "br_di_grade"),
    de(cambio, "inflc_meta"),
    # ── ii. Endógeno de câmbio ───────────────────────────────────────────────
    so(cambio, "cmb_ptax", ("ptax_venda",)),
    de(cambio, "cmb_fx_latam"),
    so(cambio, "cmb_reer", ("BR|real_broad", "BR|nominal_broad", "MX|real_broad", "CL|real_broad", "CO|real_broad")),
    so(cambio, "cmb_reservas_bc", ("reserves_total_daily", "bcb_swap_cambial_position",
                            "bcb_intervention_spot", "bcb_intervention_repo_lines")),
    so(cambio, "cmb_cambio_contratado", ("cc_saldo_total", "cc_saldo_comercial", "cc_fin_saldo")),
    so(cambio, "cmb_balanco_pagmt", ("conta_corrente", "investimento_direto_liquido", "portfolio_passivos")),
    so(cambio, "cmb_cot_fx", ("BRL|lev_net", "BRL|asset_mgr_net", "BRL|open_interest")),
    de(cambio, "cmb_termos_troca"),
    so(cambio, "cmb_comex_fator_agregado", ("basicos_export", "manufaturados_export")),
    so(cambio, "cmb_comex_pais", ("mundo_export", "mundo_import", "china_export")),
    so(cambio, "cmb_comex_produto", ("petroleo_export", "soja_export", "minerio_ferro_export")),
    so(cambio, "diferenciais_juros", ("selic", "fed_funds", "diferencial_nominal", "diferencial_real")),
    # ── iii. TWA — expectativas ──────────────────────────────────────────────
    de(cambio, "expc_focus_copom"),
    de(cambio, "expc_focus_periodo", recorte="Selic"),
    Tabela("expc_qpc", especial=qpc),
    Tabela("expc_focus", filtro="tipo_calculo = 'geral' AND base_calculo = 0",
           dims=("indicador", "horizonte", "suavizada"), valor="mediana", series=(
        _s("IPCA|12m|S", "IPCA 12 meses à frente (suavizada)", "%", "dif"),
        _s("IPCA|24m|N", "IPCA 24 meses à frente", "%", "dif"),
        _s("IPCA Serviços|12m|S", "IPCA serviços 12 meses à frente (suavizada)", "%", "dif"),
        _s("IPCA Livres|12m|S", "IPCA livres 12 meses à frente (suavizada)", "%", "dif"),
        _s("IPCA Administrados|12m|S", "IPCA administrados 12 meses à frente (suavizada)", "%", "dif"),
    )),
    de(cambio, "expc_focus_periodo", recorte="IPCA"),
    de(cambio, "expc_focus_periodo", recorte="câmbio"),
    # ── iv. TWA — inflação ───────────────────────────────────────────────────
    de(cambio, "inflc_agregados", series=(
        *[_s(k, rot, "%", "var_mensal") for k, rot in (
            ("ipca", "IPCA"), ("ipca15", "IPCA-15"), ("ipca_livres", "Livres"),
            ("ipca_administrado", "Administrados"), ("ipca_alimentacao", "Alimentação"),
            ("ipca_servicos", "Serviços"), ("ipca_industriais", "Industriais"),
            ("ipca_nucleo_ex0", "Núcleo EX0"), ("ipca_nucleo_ex03", "Núcleo EX3"),
            ("ipca_nucleo_medias_aparadas", "Núcleo médias aparadas com suavização"),
            ("ipca_nucleo_p55", "Núcleo P55"), ("ipca_nucleo_dp", "Núcleo dupla ponderação"),
            ("ipca_nucleo_exfe", "Núcleo EXFE"))],
        _s("ipca_indice_difusao", "Índice de difusão", "% dos subitens", "dif", casas=1),
    )),
    Tabela("inflc_decomposicao", especial=inflc_decomposicao),
    Tabela("inflc_decomposicao_item", especial=inflc_decomposicao_item),
    Tabela("inflc_dim", corte=None, especial=inflc_dim),
    # ── v. TWA — atividade ───────────────────────────────────────────────────
    Tabela("atv_pib", dims=("name", "seasonal_adjs"), series=tuple(
        _s(f"{k}|Y", rot, "índice, dessaz.", "pct") for k, rot in (
            ("pib_pm", "PIB"), ("consumo_familias", "Consumo das famílias"),
            ("consumo_adm_publica", "Consumo do governo"), ("fbcf", "FBCF"),
            ("exportacao", "Exportação"), ("importacao", "Importação"),
            ("agropecuaria", "Agropecuária"), ("industria", "Indústria"), ("servicos", "Serviços")))),
    Tabela("atv_pib_taxas", dims=("name", "indicador"), series=(
        _s("pib_pm|qoq", "PIB, contra o trimestre anterior (dessaz.)", "%", "dif", casas=1),
        _s("pib_pm|yoy", "PIB, contra o mesmo trimestre do ano anterior", "%", "dif", casas=1),
        _s("pib_pm|acum_4t", "PIB, acumulado em 4 trimestres", "%", "dif", casas=1),
        _s("consumo_familias|qoq", "Consumo das famílias, contra o trimestre anterior", "%", "dif", casas=1),
        _s("fbcf|qoq", "FBCF, contra o trimestre anterior", "%", "dif", casas=1),
        _s("servicos|qoq", "Serviços, contra o trimestre anterior", "%", "dif", casas=1),
        _s("industria|qoq", "Indústria, contra o trimestre anterior", "%", "dif", casas=1),
    )),
    Tabela("atv_pib_valores_correntes", especial=pib_correntes),
    Tabela("atv_pib_mensal", series=(
        _s("pib_acum_12m", "PIB nominal, 12 meses", "R$ bi", "pct", escala=_BI, casas=0),)),
    Tabela("atv_ibcbr", series=tuple(
        _s(k, rot, "índice, dessaz.", "pct") for k, rot in (
            ("ibcbr_sa", "IBC-Br"), ("ibcbr_ex_agropecuaria_sa", "IBC-Br ex-agropecuária"),
            ("ibcbr_agropecuaria_sa", "Agropecuária"), ("ibcbr_industria_sa", "Indústria"),
            ("ibcbr_servicos_sa", "Serviços")))),
    Tabela("atv_pim", dims=("name", "seasonal_adjs"), series=tuple(
        _s(f"{k}|Y", rot, "índice, dessaz.", "pct") for k, rot in (
            ("industria_geral", "Indústria geral"), ("ind_transformacao", "Transformação"),
            ("ind_extrativas", "Extrativa")))),
    Tabela("atv_pim_uso", dims=("name", "seasonal_adjs"), series=tuple(
        _s(f"{k}|Y", rot, "índice, dessaz.", "pct") for k, rot in (
            ("bens_capital", "Bens de capital"), ("bens_intermediarios", "Bens intermediários"),
            ("bens_consumo_duraveis", "Bens de consumo duráveis"),
            ("bens_consumo_semi_nao_duraveis", "Bens de consumo semi e não duráveis")))),
    Tabela("atv_pmc", dims=("name", "seasonal_adjs"), series=tuple(
        _s(f"{k}|Y", rot, "índice, dessaz.", "pct") for k, rot in (
            ("comercio_restrito_total", "Varejo restrito"), ("comercio_ampliado_total", "Varejo ampliado"),
            ("hipermercados_supermercados", "Super e hipermercados"),
            ("moveis_eletrodomesticos", "Móveis e eletrodomésticos"),
            ("veiculos_motocicletas_pecas", "Veículos, motos e peças")))),
    Tabela("atv_pms", dims=("name", "seasonal_adjs"), series=tuple(
        _s(f"{k}|Y", rot, "índice, dessaz.", "pct") for k, rot in (
            ("servicos_total", "Serviços, total"), ("servicos_familias", "Prestados às famílias"),
            ("informacao_comunicacao", "Informação e comunicação"),
            ("prof_adm_complementares", "Profissionais e administrativos"),
            ("transportes_correio", "Transportes e correio")))),
    Tabela("atv_renda_poupanca", especial=renda_poupanca),
    # ── vi. TWA — mercado de trabalho ────────────────────────────────────────
    Tabela("mt_pnad", filtro="region = 'Brasil'", series=(
        _s("taxa_desocupacao", "Taxa de desocupação", "%", "dif", casas=1),
        _s("taxa_participacao", "Taxa de participação", "%", "dif", casas=1),
        _s("nivel_ocupacao", "Nível de ocupação", "% da PIA", "dif", casas=1),
        _s("taxa_subutil_composta", "Subutilização composta", "%", "dif", casas=1),
        _s("taxa_informalidade", "Informalidade", "% dos ocupados", "dif", casas=1),
        _s("ocupado", "Ocupados", "mil pessoas", "pct", casas=0),
        _s("rend_habitual_real_todos_trabalhos", "Rendimento habitual real", "R$", "pct", casas=0),
        _s("massa_real_habitual", "Massa de rendimento habitual real", "R$ bi", "pct", escala=_BI, casas=1),
    )),
    Tabela("mt_desocupacao_retro", corte="vintage", dims=(), series=(
        _s("value", "Desocupação dessazonalizada, retropolada pelo BC", "%", "dif"),)),
    Tabela("mt_caged", series=tuple(
        _s(k, rot, "mil empregos", "pct", escala=_BI, casas=0) for k, rot in (
            ("caged_total", "Estoque de emprego formal"), ("caged_servicos", "Serviços"),
            ("caged_comercio", "Comércio"), ("caged_ind_transformacao", "Indústria de transformação"),
            ("caged_construcao", "Construção")))),
    Tabela("mt_caged_setor", dims=("categoria", "metrica"), series=tuple(
        _s(f"{k}|saldo", f"Saldo: {rot}", "mil empregos", "fluxo", escala=_BI, casas=1) for k, rot in (
            ("comercio", "comércio"), ("industria_transformacao", "indústria de transformação"),
            ("construcao", "construção"), ("agropecuaria", "agropecuária"),
            ("alojamento_alimentacao", "alojamento e alimentação"),
            ("informacao_comunicacao", "informação e comunicação"),
            ("atividades_administrativas_servicos_complementares", "serviços administrativos"),
            ("saude_servicos_sociais", "saúde"), ("educacao", "educação")))),
    # ── vii. TWA — crédito ───────────────────────────────────────────────────
    Tabela("cred_credito_resumo", series=(
        _s("saldo_total_total", "Saldo total", "R$ bi", "pct", escala=_BI, casas=0),
        _s("saldo_livre_pf", "Saldo livre PF", "R$ bi", "pct", escala=_BI, casas=0),
        _s("saldo_livre_pj", "Saldo livre PJ", "R$ bi", "pct", escala=_BI, casas=0),
        _s("concessao_livre_pf", "Concessões livres PF", "R$ bi", "fluxo", escala=_BI, casas=1),
        _s("concessao_livre_pj", "Concessões livres PJ", "R$ bi", "fluxo", escala=_BI, casas=1),
        _s("taxa_juros_livre_pf", "Taxa de juros, livre PF", "% a.a.", "dif"),
        _s("taxa_juros_livre_pj", "Taxa de juros, livre PJ", "% a.a.", "dif"),
        _s("spread_livre_total", "Spread, livre", "p.p.", "dif"),
        _s("icc_total_total", "Custo do crédito (ICC)", "% a.a.", "dif"),
        _s("inadimplencia_livre_pf", "Inadimplência, livre PF", "% da carteira", "dif"),
        _s("inadimplencia_livre_pj", "Inadimplência, livre PJ", "% da carteira", "dif"),
    )),
    Tabela("cred_fluxo_financeiro", corte="vintage", series=(
        _s("fluxo_total", "Fluxo financeiro, total", "% do PIB, 12m", "dif", casas=1),
        _s("fluxo_pf", "Fluxo financeiro, PF", "% do PIB, 12m", "dif", casas=1),
        _s("fluxo_pj", "Fluxo financeiro, PJ", "% do PIB, 12m", "dif", casas=1),
    )),
    Tabela("cred_ptc", series=tuple(
        _s(f"{seg}_{lado}_observada", f"{rot}: {lado}, observada", "índice, −1 a 1", "dif")
        for seg, rot in (("pfc", "PF consumo"), ("pfh", "PF habitação"), ("ge", "Grandes empresas"),
                         ("mpme", "Micro, pequenas e médias"))
        for lado in ("oferta", "demanda"))),
    Tabela("cred_credito_familias", series=(
        _s("endividamento_renda", "Endividamento das famílias", "% da renda 12m", "dif"),
        _s("endividamento_sem_imob", "Endividamento sem imobiliário", "% da renda 12m", "dif"),
        _s("comp_renda_servico_total", "Comprometimento de renda com o serviço da dívida", "% da renda", "dif"),
        _s("comp_renda_juros", "Comprometimento de renda com juros", "% da renda", "dif"),
    )),
    Tabela("cred_credito_amplo", series=tuple(
        _s(k, rot, "R$ bi", "pct", escala=_BI, casas=0) for k, rot in (
            ("emp_emprestimos_sfn", "Empresas: empréstimos do SFN"),
            ("emp_titulos_divida_privado", "Empresas: títulos de dívida"),
            ("emp_divida_externa_mercado_ext", "Empresas: dívida externa"),
            ("fam_emprestimos_sfn", "Famílias: empréstimos do SFN"),
            ("gov_titulos_publicos", "Governo: títulos públicos")))),
    Tabela("cred_modalidade_livre_pf", dims=("modalidade", "metrica"), series=_modalidade((
        ("credito_pessoal_consignado_total", "taxa_media", "Consignado"),
        ("credito_pessoal_nao_consignado_total", "taxa_media", "Pessoal não consignado"),
        ("aquisicao_de_veiculos", "taxa_media", "Veículos"),
        ("cartao_de_credito_rotativo", "taxa_media", "Cartão rotativo"),
        ("credito_pessoal_nao_consignado_total", "concessao", "Pessoal não consignado"),
        ("aquisicao_de_veiculos", "concessao", "Veículos"),
        ("credito_pessoal_nao_consignado_total", "inadimplencia", "Pessoal não consignado"),
        ("aquisicao_de_veiculos", "inadimplencia", "Veículos")))),
    Tabela("cred_modalidade_livre_pj", dims=("modalidade", "metrica"), series=_modalidade((
        ("capital_de_giro_total", "taxa_media", "Capital de giro"),
        ("desconto_de_duplicatas_e_recebiveis", "taxa_media", "Desconto de duplicatas"),
        ("conta_garantida", "taxa_media", "Conta garantida"),
        ("capital_de_giro_total", "concessao", "Capital de giro"),
        ("capital_de_giro_total", "inadimplencia", "Capital de giro")))),
    Tabela("cred_modalidade_direcionado_pf", dims=("modalidade", "metrica"), series=_modalidade((
        ("financiamentos_imobiliarios_total", "saldo", "Imobiliário"),
        ("credito_rural_total", "saldo", "Rural"),
        ("financiamentos_imobiliarios_total", "taxa_media", "Imobiliário")))),
    Tabela("cred_modalidade_direcionado_pj", dims=("modalidade", "metrica"), series=_modalidade((
        ("credito_com_recursos_do_bndes_total", "saldo", "BNDES"),
        ("credito_rural_total", "saldo", "Rural"),
        ("credito_com_recursos_do_bndes_total", "taxa_media", "BNDES")))),
    Tabela("cred_credito_controle_capital", dims=("controle", "metrica"), series=(
        *[_s(f"{k}|saldo", f"Saldo: {rot}", "R$ bi", "pct", escala=_BI, casas=0) for k, rot in (
            ("publicas", "bancos públicos"), ("privadas_nacionais", "privados nacionais"),
            ("estrangeiras", "estrangeiros"))],
        *[_s(f"{k}|inadimplencia", f"Inadimplência: {rot}", "% da carteira", "dif") for k, rot in (
            ("publicas", "bancos públicos"), ("privadas_nacionais", "privados nacionais"),
            ("estrangeiras", "estrangeiros"))],
    )),
    Tabela("cred_inadimplencia_pj", series=(
        _s("inadimplencia_pj", "Inadimplência PJ (acima de 90 dias)", "% da carteira", "dif"),
        _s("atraso_pj", "Atraso PJ de 15 a 90 dias", "% da carteira", "dif"),
        _s("taxa_juros_pj", "Taxa de juros PJ", "% a.a.", "dif"),
        _s("concessao_credito_pj", "Concessões PJ", "R$ bi", "fluxo", escala=_BI, casas=1),
    )),
    # ── viii. TWA — fiscal ───────────────────────────────────────────────────
    de(cambio, "fisc_nfsp", series=(
        _s("resultado_primario_pct_pib_12m", "Resultado primário, 12m (+ = superávit)", "% do PIB", "dif"),
        _s("resultado_primario_governo_federal_bc_pct_pib_12m",
           "Primário do governo federal e BC, 12m", "% do PIB", "dif"),
        _s("resultado_nominal_pct_pib_12m", "Resultado nominal, 12m", "% do PIB", "dif"),
        _s("juros_nominais_pct_pib_12m", "Juros nominais, 12m", "% do PIB", "dif"),
    )),
    de(cambio, "fisc_divida"),
    Tabela("fisc_dlsp_fatores", especial=dlsp_fatores),
    Tabela("fisc_rtn", series=(
        _s("resultado_primario_governo_central", "Primário do governo central (+ = superávit)",
           "R$ bi", "fluxo", escala=_BI, casas=1),
        _s("receita_liquida", "Receita líquida", "R$ bi", "fluxo", escala=_BI, casas=1),
        _s("despesa_total", "Despesa total", "R$ bi", "fluxo", escala=_BI, casas=1),
    )),
    Tabela("fisc_efgg", especial=efgg),
    # ── ix. TWA — externo ────────────────────────────────────────────────────
    de(cambio, "us_interest_rate", variante="curva",
               filtro="curve = 'POLICY' OR (curve = 'US_TREASURY' AND tenor IN ('3M', '2Y', '5Y', '10Y', '30Y'))",
               series=(_s("POLICY|1d", "Fed Funds, meta (ponto médio)", "% a.a.", "dif"),
                       *[_s(f"US_TREASURY|{t}", f"Treasury {r}", "% a.a.", "dif")
                         for t, r in (("3M", "3 meses"), ("2Y", "2 anos"), ("5Y", "5 anos"),
                                      ("10Y", "10 anos"), ("30Y", "30 anos"))])),
    Tabela("inter_interest_rate", dims=("country_code",), filtro="curve = 'POLICY'", series=tuple(
        _s(p, f"{rot}, juro de política", "% a.a.", "dif") for p, rot in (
            ("MX", "México"), ("CL", "Chile"), ("CO", "Colômbia"), ("PE", "Peru")))),
    de(cambio, "cmb_real_rates"),
    de(cambio, "cmb_dollar_index"),
    de(cambio, "cmb_dollar_index_em"),
    de(cambio, "comm_brent"),
    de(cambio, "comm_icbr_usd"),
    Tabela("comm_icbr", series=tuple(
        _s(k, rot, "índice, em R$", "pct") for k, rot in (
            ("icbr_geral", "IC-Br"), ("icbr_agropecuaria", "IC-Br agropecuária"),
            ("icbr_metal", "IC-Br metal"), ("icbr_energia", "IC-Br energia")))),
    # ── x. Exógeno ───────────────────────────────────────────────────────────
    de(cambio, "cmb_risco_pais"),
]


# ── leituras combinadas ───────────────────────────────────────────────────────
def selic_curva_focus(ctx: Ctx) -> list[str]:
    """A Selic reunião a reunião, na curva DI e na Focus, lado a lado."""
    di = ctx.ler("br_di_grade")
    p0 = di["date"].max()
    curva = esp.selic_na_curva(ctx, p0)
    fc = ctx.ler("expc_focus_copom")
    d0 = fc["date"].max()
    cal = esp._datas_reunioes(ctx)
    foc = {}
    for r in fc[fc["date"] == d0].itertuples():
        m = esp._ROTULO_REUNIAO.match(str(r.reuniao))
        if m and (d := cal.get((int(m.group(1)), int(m.group(2))))) is not None:
            foc[d] = (r.reuniao, float(r.mediana))
    vig, dv = esp._selic_vigente(ctx, ctx.corte + pd.Timedelta(days=1))
    linhas = []
    for d in sorted(set(curva) | {d for d in foc if d >= p0}):
        c, f = curva.get(d), foc.get(d, (None, None))[1]
        linhas.append({"Reunião": fdata(d), "Rótulo Focus": foc.get(d, ("—",))[0],
                       "Focus (mediana)": fmt(f), "Curva DI": fmt(c),
                       "Curva − Focus (p.b.)": fmt(None if c is None or f is None else (c - f) * 100, 0, True)})
    return (["### A Selic por reunião: curva DI e Focus", "",
             f"Selic vigente {fmt(vig)}% (decidida em {fdata(dv)}). Curva do pregão de {fdata(p0)}; "
             f"Focus de {fdata(d0)}. A curva é preço, com prêmio de prazo; a Focus é a mediana da "
             "pesquisa. A diferença mistura prêmio e discordância.", ""] + md_tabela(linhas))


def juro_real(ctx: Ctx) -> list[str]:
    """Quão restritiva está a política: juro real ex-ante, inflação implícita e o neutro do QPC."""
    def ult(nome, chave):
        s = ctx.serie(nome, chave)
        return (None, None) if s.empty else (float(s.iloc[-1]), s.index[-1])

    def real(i, pi):
        return None if i is None or pi is None else ((1 + i / 100) / (1 + pi / 100) - 1) * 100

    pi12, dpi = ult("expc_focus", "IPCA|12m|S")
    vig, dv = esp._selic_vigente(ctx, ctx.corte + pd.Timedelta(days=1))
    rv = real(vig, pi12)
    linhas = [{"Medida": "Selic vigente", "Data": fdata(dv), "Nominal (%)": fmt(vig),
               "Inflação (%)": f"{fmt(pi12)} (Focus 12m)", "Real (%)": fmt(rv)}]
    for t, rot in (("12M", "1 ano"), ("24M", "2 anos"), ("60M", "5 anos"), ("120M", "10 anos")):
        i, di = ult("br_interest_rate", f"DIPRE|{t}")
        r, dr = ult("br_interest_rate", f"NTNBJS|{t}")
        impl = None if i is None or r is None else ((1 + i / 100) / (1 + r / 100) - 1) * 100
        linhas.append({"Medida": f"DI e NTN-B, {rot}", "Data": fdata(dr), "Nominal (%)": fmt(i),
                       "Inflação (%)": f"{fmt(impl)} (implícita)", "Real (%)": fmt(r)})
    out = ["### Juro real e inflação implícita", "",
           f"Focus IPCA 12 meses (suavizada) de {fdata(dpi)}. Real = (1 + nominal)/(1 + inflação) − 1; "
           "nos títulos, o real é a própria NTN-B e a inflação implícita sai do DI contra ela no mesmo "
           "prazo (com prêmio de risco de inflação dentro).", ""] + md_tabela(linhas)
    q = ctx.ler("expc_qpc")
    n = q[(q["variavel"] == "juro_real_neutro") & (q["estatistica"] == "mediana")]
    if not n.empty and rv is not None:
        nro = n["nro_reuniao"].max()
        neutros = n[n["nro_reuniao"] == nro]
        out += ["", f"Juro real neutro no QPC da reunião {int(nro)} ({fdata(neutros['date'].max())}), "
                    "mediana, e a Selic real acima dele: "
                + "; ".join(f"{str(x.referencia).replace('_', ' ')} {fmt(x.valor)}% "
                            f"({fmt(rv - x.valor, 2, True)} p.p.)" for x in neutros.itertuples()) + "."]
    return out


COMBINADAS = [selic_curva_focus, juro_real]
