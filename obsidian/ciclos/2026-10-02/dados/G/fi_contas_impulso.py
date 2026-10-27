"""G do fiscal, ciclo 2026-10-02: as contas e o impulso.

1. Primário do governo central (RTN, acima da linha, + = superávit) em 12 meses, % do PIB de 12
   meses, mês a mês de ago/2025 a ago/2026; e o que moveu os 12 meses entre mai/2026 e ago/2026
   (a troca de jun-ago/2025 por jun-ago/2026, em R$ bi e em % do PIB de 12 meses de ago/2026).
2. Jun-ago/2026 contra jun-ago/2025, por grupo, R$ bi e crescimento real (IPCA mês a mês).
3. Primário do setor público consolidado (NFSP) em 12 meses, mês a mês.
4. Dívida: taxa implícita da DLSP (juros 12m / estoque médio de 12 meses), crescimento nominal do
   PIB 12m, IPCA 12m, e o primário que estabiliza a DLSP: d·(i − g)/(1 + g).
5. Parafiscal: estoque de créditos do Tesouro a instituições financeiras oficiais, mês a mês, e a
   parte BNDES e instrumentos híbridos.
6. Governo geral (EFGG, soma não consolidada): despesa exceto juros em 4 trimestres, % do PIB,
   trimestre a trimestre (impulso pela despesa).
7. QPC: o juro real neutro (mediana) nas últimas reuniões (consulta, endógeno de expectativas).
"""
import pandas as pd

A = "obsidian/ciclos/2026-10-02/dados/A/"
rtn = pd.read_csv(A + "fisc_rtn.csv.gz", parse_dates=["date"]).pivot(index="date", columns="name", values="value")
ipca = pd.read_csv(A + "inflc_indice_geral.csv.gz", parse_dates=["date"])
ipca = ipca[ipca.indice == "IPCA"].set_index("date")["numero_indice"]
pib = pd.read_csv(A + "atv_pib_mensal.csv.gz", parse_dates=["date"]).pivot(index="date", columns="name", values="value")

print("## 1. Primário do governo central, 12 meses (RTN, + = superávit)")
prim = rtn["resultado_primario_governo_central"]
p12 = prim.rolling(12).sum()
pct = p12 / pib["pib_acum_12m"] * 100
print(pd.DataFrame({"R$ bi 12m": (p12 / 1000).round(1), "% PIB": pct.round(2)}).loc["2025-08-01":"2026-08-01"].to_string())

grupos = {
    "Receita líquida": "receita_liquida",
    "  receita administrada RFB": "receita_administrada_rfb",
    "  arrecadação RGPS": "arrecadacao_liquida_rgps",
    "  não administradas RFB": "receitas_nao_administradas_rfb",
    "    dividendos": "dividendos_e_participacoes",
    "    recursos naturais": "receitas_de_exploracao_de_recursos_naturais",
    "    concessões": "concessoes_e_permissoes",
    "  transferências por repartição": "transferencias_reparticao_receita",
    "Despesa total": "despesa_total",
    "  benefícios previdenciários": "beneficios_previdenciarios",
    "  pessoal": "pessoal_encargos_sociais",
    "  BPC/LOAS": "beneficios_de_prestacao_continuada_da_loas_rmv",
    "  abono e seguro": "abono_e_seguro_desemprego",
    "  obrig. c/ controle de fluxo": "obrigatorias_com_controle_de_fluxo",
    "    Bolsa Família": "obrigatorias_com_controle_de_fluxo_bolsa_familia",
    "  sentenças e precatórios (custeio e capital)": "sentencas_judiciais_e_precatorios_custeio_e_capital",
    "  créditos extraordinários": "creditos_extraordinarios_exceto_pac",
    "  discricionárias do Executivo": "despesas_discricionarias_do_poder_executivo",
    "  subsídios, subvenções e Proagro": "subsidios_subvencoes_e_proagro",
    "Primário governo central": "resultado_primario_governo_central",
}
meses_n = pd.date_range("2026-06-01", "2026-08-01", freq="MS")
meses_a = pd.date_range("2025-06-01", "2025-08-01", freq="MS")
fator = ipca.loc["2026-09-01"] / ipca  # leva a reais de set/2026
pib12 = pib.loc["2026-08-01", "pib_acum_12m"]
print("\n## 1b/2. Jun-ago/2026 contra jun-ago/2025 (R$ bi correntes; real a preços de set/2026)")
linhas = []
for rot, col in grupos.items():
    s = rtn[col]
    n, a = s.loc[meses_n].sum(), s.loc[meses_a].sum()
    nr, ar = (s.loc[meses_n] * fator.loc[meses_n]).sum(), (s.loc[meses_a] * fator.loc[meses_a]).sum()
    cresc = (nr / ar - 1) * 100 if abs(ar) > 1 and col != "resultado_primario_governo_central" else float("nan")
    linhas.append([rot, round(n / 1000, 1), round(a / 1000, 1), round((n - a) / 1000, 1),
                   round((n - a) / pib12 * 100, 2), round(cresc, 1)])
print(pd.DataFrame(linhas, columns=["grupo", "jun-ago/26", "jun-ago/25", "Δ R$ bi", "Δ % PIB 12m", "real %"]).to_string(index=False))

print("\n## 1c. 12 meses até ago/2026 contra 12 meses até ago/2025 (real a preços de set/2026), itens extras")
for rot, col in [("créditos extraordinários", "creditos_extraordinarios_exceto_pac"),
                 ("sentenças e precatórios (custeio e capital)", "sentencas_judiciais_e_precatorios_custeio_e_capital"),
                 ("dividendos", "dividendos_e_participacoes"),
                 ("recursos naturais", "receitas_de_exploracao_de_recursos_naturais"),
                 ("concessões", "concessoes_e_permissoes"),
                 ("receita administrada RFB", "receita_administrada_rfb"),
                 ("financiamento de campanha eleitoral", "financiamento_de_campanha_eleitoral")]:
    s = rtn[col]
    m1 = pd.date_range("2025-09-01", "2026-08-01", freq="MS")
    m0 = pd.date_range("2024-09-01", "2025-08-01", freq="MS")
    n, a = s.loc[m1].sum(), s.loc[m0].sum()
    nr, ar = (s.loc[m1] * fator.loc[m1]).sum(), (s.loc[m0] * fator.loc[m0]).sum()
    print(f"{rot}: {n/1000:.1f} vs {a/1000:.1f} R$ bi; real {((nr/ar-1)*100 if ar else float('nan')):+.1f}%")

print("\n## 3. Primário do setor público consolidado, 12m (NFSP, % do PIB, + = superávit)")
nf = pd.read_csv(A + "fisc_nfsp.csv.gz", parse_dates=["date"]).pivot(index="date", columns="name", values="value")
print(nf.loc["2025-08-01":"2026-08-01", ["resultado_primario_pct_pib_12m", "resultado_primario_governo_federal_bc_pct_pib_12m",
                                         "juros_nominais_pct_pib_12m", "resultado_nominal_pct_pib_12m"]].to_string())
fl = nf["resultado_primario_fluxo_mensal"]
print("fluxo mensal do primário consolidado (R$ bi, + = superávit), set-dez/2025:",
      (fl.loc["2025-09-01":"2025-12-01"] / 1000).round(1).tolist())
print("soma set-dez/2025 (R$ bi):", round(fl.loc["2025-09-01":"2025-12-01"].sum() / 1000, 1))

print("\n## 4. Dívida líquida: taxa implícita e primário estabilizador")
fat = pd.read_csv(A + "fisc_dlsp_fatores.csv.gz", parse_dates=["date"])
est = fat[(fat.fator == "estoque") & (fat["item"] == "total")].set_index("date")["value"].sort_index()
jur = fat[(fat.fator == "juros") & (fat["item"] == "total")].set_index("date")["value"].sort_index()
for d in ["2025-08-01", "2026-08-01"]:
    j12 = jur.loc[:d].iloc[-12:].sum()
    e_med = est.loc[:d].iloc[-13:].mean()
    i = j12 / e_med
    g = pib.loc[d, "pib_acum_12m"] / pib["pib_acum_12m"].shift(12).loc[d] - 1
    pi = ipca.loc[d] / ipca.shift(12).loc[d] - 1
    dl = pd.read_csv(A + "fisc_divida.csv.gz", parse_dates=["date"])
    dl = dl[dl.name == "dlsp_pct_pib"].set_index("date")["value"].loc[d] / 100
    estab = dl * (i - g) / (1 + g) * 100
    rreal = ((1 + i) / (1 + pi) - 1) * 100
    print(f"{d}: juros 12m R$ {j12/1e3:.0f} bi; estoque médio R$ {e_med/1e6:.2f} tri; taxa implícita {i*100:.1f}%; "
          f"PIB nominal 12m {g*100:.1f}%; IPCA 12m {pi*100:.2f}%; real implícita {rreal:.1f}%; "
          f"DLSP {dl*100:.1f}% do PIB; primário estabilizador {estab:.2f}% do PIB")
print("estoque DLSP (R$ tri), últimos meses:", (est.loc["2026-03-01":] / 1e6).round(2).tolist())

print("\n## 5. Parafiscal: créditos do Tesouro a instituições financeiras oficiais (estoque, R$ bi, − = ativo)")
pf = fat[fat.fator == "estoque"].pivot(index="date", columns="item", values="value")
cols = ["interna__gov_federal__creditos_inst_fin_oficiais",
        "interna__gov_federal__creditos_inst_fin_oficiais__creditos_bndes",
        "interna__gov_federal__creditos_inst_fin_oficiais__instrumentos_hibridos"]
t = (pf.loc["2025-06-01":"2026-08-01", cols] / 1000).round(1)
t.columns = ["total", "BNDES", "híbridos"]
t["% PIB"] = (pf.loc["2025-06-01":"2026-08-01", cols[0]] / pib.loc["2025-06-01":"2026-08-01", "pib_acum_12m"] * 100).round(2)
print(t.to_string())

print("\n## 6. Governo geral (EFGG, soma não consolidada): despesa exceto juros, 4 tri, % do PIB")
ef = pd.read_csv(A + "fisc_efgg.csv.gz", parse_dates=["date"]).pivot(index="date", columns="name", values="value")
pq = pib["pib_mensal"].resample("QS").sum()
dx = (ef["geral_despesa_total"] - ef["geral_juros"]).rolling(4).sum()
r = (dx / pq.rolling(4).sum().reindex(dx.index) * 100)
out = pd.DataFrame({"% PIB 4t": r.round(2), "Δ 4t (p.p.)": r.diff(4).round(2), "Δ 1t (p.p.)": r.diff(1).round(2)})
print(out.loc["2024-01-01":].to_string())
for comp in ["geral_beneficios_previdenciarios_assistenciais", "geral_remuneracao_empregados",
             "geral_uso_bens_servicos", "geral_investimento_liquido", "geral_subsidios", "geral_outros_gastos",
             "geral_transferencias_doacoes", "geral_aquisicao_ativos_nao_financeiros"]:
    c4 = ef[comp].rolling(4).sum() / pq.rolling(4).sum().reindex(ef.index) * 100
    print(f"{comp}: {c4.loc['2026-04-01']:.2f} vs {c4.loc['2025-04-01']:.2f} (Δ {c4.loc['2026-04-01']-c4.loc['2025-04-01']:+.2f})")

print("\n## 7. QPC: juro real neutro (consulta)")
q = pd.read_csv(A + "expc_qpc.csv.gz")
q = q[(q.bloco == "juro_real_neutro") & (q.estatistica.isin(["mediana", "p25", "p75"]))]
print(q.pivot_table(index=["nro_reuniao", "date", "referencia"], columns="estatistica", values="valor").tail(12).to_string())
