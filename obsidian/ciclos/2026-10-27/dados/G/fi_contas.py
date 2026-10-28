"""fi: contas do governo central e do setor público — crescimento real por trimestre (RTN, deflator IPCA),
decomposição das discricionárias e da receita, o primário 12m mês a mês (NFSP), o fechamento anual,
o crédito do Tesouro às instituições oficiais mês a mês, e a dinâmica da dívida (juro implícito, primário
que estabiliza a DLSP)."""
from pathlib import Path
import numpy as np
import pandas as pd
A = Path(__file__).resolve().parent.parent / "A"
r = lambda f: pd.read_csv(A / f"{f}.csv.gz", parse_dates=["date"])
pd.set_option("display.width", 220)

ip = r("inflc_agregados"); ip = ip[ip.name == "ipca"].set_index("date").value
idx = (1 + ip / 100).cumprod()
rtn = r("fisc_rtn").pivot_table(index="date", columns="name", values="value")
rtn = rtn[rtn.index >= "2022-01-01"]
defl = idx.reindex(rtn.index)
real = rtn.div(defl, axis=0) * defl.iloc[-1]  # R$ milhões de ago/2026 (último mês do RTN)
print("RTN último mês:", rtn.index.max().date(), "· IPCA até", idx.index.max().date())

itens = ["receita_liquida", "despesa_total", "beneficios_previdenciarios", "pessoal_encargos_sociais",
         "beneficios_de_prestacao_continuada_da_loas_rmv", "obrigatorias_com_controle_de_fluxo_bolsa_familia",
         "despesas_discricionarias_do_poder_executivo", "creditos_extraordinarios_exceto_pac",
         "sentencas_judiciais_e_precatorios_custeio_e_capital"]
q = real[itens].copy(); q["tri"] = q.index.to_period("Q")
# 3T26 tem só jul-ago: compara com jul-ago de 2025
cnt = q.groupby("tri").size()
qs = q.groupby("tri").sum()
print("\nCrescimento real contra o mesmo trimestre do ano anterior (%), RTN, deflator IPCA:")
out = {}
for t in qs.index:
    if t.year < 2025: continue
    prev = t - 4
    if cnt[t] < 3:  # trimestre parcial
        meses = q[q.tri == t].index.month
        cur = q[q.tri == t][itens].sum()
        pv = q[(q.tri == prev) & q.index.month.isin(meses)][itens].sum()
    else:
        cur, pv = qs.loc[t, itens], qs.loc[prev, itens]
    out[f"{t}{'*' if cnt[t] < 3 else ''}"] = (100 * (cur / pv - 1)).round(1)
print(pd.DataFrame(out).to_string())

# discricionárias por função e receita por item, 12m até ago/26 contra 12m até ago/25 (real)
def g12(cols):
    a = real[cols].iloc[-12:].sum(); b = real[cols].iloc[-24:-12].sum()
    return pd.DataFrame({"12m (R$ bi de ago/26)": (a / 1000).round(1), "12m antes": (b / 1000).round(1),
                         "Δ (R$ bi)": ((a - b) / 1000).round(1), "real %": (100 * (a / b - 1)).round(1)})
disc = [c for c in real.columns if c.startswith("discricionarias_")]
print("\nDiscricionárias por função, 12m:\n", g12(disc + ["despesas_discricionarias_do_poder_executivo"]).to_string())
rec = ["receita_total", "receita_administrada_rfb", "arrecadacao_liquida_rgps", "receitas_nao_administradas_rfb",
       "receitas_de_exploracao_de_recursos_naturais", "dividendos_e_participacoes", "dividendos_e_participacoes_petrobras",
       "dividendos_e_participacoes_bndes", "concessoes_e_permissoes", "transferencias_reparticao_receita", "receita_liquida",
       "imposto_de_renda", "iof", "imposto_de_importacao", "ipi", "cofins", "pis_pasep", "csll", "receita_da_cide_combustiveis"]
print("\nReceita, 12m:\n", g12(rec).to_string())
outros = ["subsidios_subvencoes_e_proagro", "auxilio_cde", "obrigatorias_com_controle_de_fluxo",
          "obrigatorias_com_controle_de_fluxo_saude", "obrigatorias_com_controle_de_fluxo_educacao",
          "fundeb_complem_uniao", "apoio_fin_municipios_estados", "outras_despesas_obrigatorias", "demais_despesas_obrigatorias",
          "creditos_extraordinarios_exceto_pac", "seguro_desemprego", "abono", "financiamento_de_campanha_eleitoral"]
print("\nOutras despesas, 12m:\n", g12([c for c in outros if c in real.columns]).to_string())

# primário do governo central mês a mês, nominal, e o mesmo mês do ano anterior
pc = rtn["resultado_primario_governo_central"]
print("\nPrimário do governo central, R$ bi (+ = superávit), mês e mesmo mês do ano anterior:")
print(pd.DataFrame({"mês": (pc / 1000).round(1), "ano antes": (pc.shift(12) / 1000).round(1)}).iloc[-14:].to_string())

nf = r("fisc_nfsp").pivot_table(index="date", columns="name", values="value")
cols = ["resultado_primario_pct_pib_12m", "resultado_primario_governo_federal_bc_pct_pib_12m",
        "resultado_primario_estados_municipios_pct_pib_12m", "juros_nominais_pct_pib_12m", "resultado_nominal_pct_pib_12m"]
print("\nNFSP 12m (% do PIB, + = superávit), mês a mês:\n", nf[cols].iloc[-20:].to_string())
print("\nNFSP 12m em dezembro de cada ano:\n", nf[nf.index.month == 12][cols].iloc[-6:].to_string())
print("\nFluxo mensal do primário consolidado (R$ mi, convenção da fonte):\n", nf["resultado_primario_fluxo_mensal"].iloc[-14:].to_string())

dl = r("fisc_dlsp_fatores")
cr = dl[(dl.fator == "estoque") & dl.item.str.startswith("interna__gov_federal__creditos_inst_fin_oficiais")]
cr = cr.pivot_table(index="date", columns="item", values="value") / 1000
print("\nCréditos do Tesouro a instituições oficiais (estoque, R$ bi; negativo = ativo do governo):\n", cr.iloc[-16:].round(1).to_string())

est = dl[(dl.fator == "estoque") & (dl.item == "total")].set_index("date").value
ju = dl[(dl.fator == "juros") & (dl.item == "total")].set_index("date").value
pr = dl[(dl.fator == "primario") & (dl.item == "total")].set_index("date").value
print("\nDLSP estoque total, últimos 3 (R$ bi):", (est.iloc[-3:] / 1000).round(1).to_dict())
ju12 = ju.rolling(12).sum()
est_med = est.rolling(13).mean()  # média dos 13 estoques (dez a dez) aproxima o saldo médio dos 12 meses
i_impl = 100 * ju12 / est.shift(12)
i_impl_med = 100 * ju12 / est_med
print("Juro implícito nominal da DLSP, 12m até", est.index[-1].date(), ": sobre o estoque inicial", round(i_impl.iloc[-1], 2),
      "% · sobre o estoque médio", round(i_impl_med.iloc[-1], 2), "% · um ano antes (médio)", round(i_impl_med.iloc[-13], 2))
pm = r("atv_pib_mensal"); pm = pm[pm.name == "pib_mensal"].set_index("date").value
print("PIB mensal: nome pib_mensal, último", pm.index[-1].date(), pm.iloc[-1])
pib12 = pm.rolling(12).sum()
g_nom = 100 * (pib12 / pib12.shift(12) - 1)
gdate = est.index[-1]
gn = g_nom.loc[gdate]
ipc12 = 100 * (idx.loc[gdate] / idx.loc[gdate - pd.DateOffset(months=12)] - 1)
d = r("fisc_divida"); d = d[d.name == "dlsp_pct_pib"].set_index("date").value
dd = d.loc[gdate] / 100
i = i_impl_med.loc[gdate] / 100
print(f"Crescimento nominal do PIB 12m até {gdate.date()}: {gn:.2f}% · IPCA 12m {ipc12:.2f}% · DLSP {dd*100:.1f}%")
pe = 100 * dd * (i - gn / 100) / (1 + gn / 100)
print(f"Primário que estabiliza a DLSP com i={i*100:.2f}% e g nominal={gn:.2f}%: {pe:.2f}% do PIB")
for ii in [i - 0.01, i + 0.01]:
    print(f"   com i={ii*100:.2f}%: {100*dd*(ii-gn/100)/(1+gn/100):.2f}% do PIB")
for gg in [gn / 100 - 0.01, gn / 100 + 0.01]:
    print(f"   com g={gg*100:.2f}%: {100*dd*(i-gg)/(1+gg):.2f}% do PIB")
r_real = 100 * ((1 + i) / (1 + ipc12 / 100) - 1)
print(f"Juro real implícito (deflator IPCA 12m): {r_real:.2f}%")
