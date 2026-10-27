"""G do fiscal, ciclo 2026-10-02: o primário do governo central sem sentenças judiciais e
precatórios, e o ritmo das discricionárias.

Precatórios = soma dos cinco itens de sentenças judiciais e precatórios do RTN (custeio e
capital; benefícios urbanos e rurais; BPC/LOAS; pessoal). O primário sem eles = primário + eles.
Real: IPCA mês a mês, a preços de set/2026. % do PIB: PIB nominal de 12 meses (`atv_pib_mensal`).
"""
import pandas as pd

A = "obsidian/ciclos/2026-10-02/dados/A/"
r = pd.read_csv(A + "fisc_rtn.csv.gz", parse_dates=["date"]).pivot(index="date", columns="name", values="value")
ipca = pd.read_csv(A + "inflc_indice_geral.csv.gz", parse_dates=["date"])
ipca = ipca[ipca.indice == "IPCA"].set_index("date")["numero_indice"]
pib = pd.read_csv(A + "atv_pib_mensal.csv.gz", parse_dates=["date"]).pivot(index="date", columns="name", values="value")["pib_acum_12m"]
fator = ipca.loc["2026-09-01"] / ipca

prec_cols = ["sentencas_judiciais_e_precatorios_custeio_e_capital",
             "beneficios_previdenciarios_urbano_sentencas_judiciais_e_precatorios",
             "beneficios_previdenciarios_rural_sentencas_judiciais_e_precatorios",
             "beneficios_de_prestacao_continuada_da_loas_rmv_sentencas_judiciais_e_precatorios",
             "pessoal_e_encargos_sociais_sentencas_judiciais_e_precatorios"]
prec = r[prec_cols].sum(axis=1)
print("precatórios, todos os itens (R$ bi): jul/2025", round(prec.loc["2025-07-01"] / 1e3, 1),
      "· mar/2026", round(prec.loc["2026-03-01"] / 1e3, 1))
prim = r["resultado_primario_governo_central"]
p12 = prim.rolling(12).sum() / pib * 100
x12 = (prim + prec).rolling(12).sum() / pib * 100
t = pd.DataFrame({"primário 12m": p12.round(2), "sem precatórios 12m": x12.round(2),
                  "precatórios 12m, % PIB": (prec.rolling(12).sum() / pib * 100).round(2)})
print(t.loc["2024-08-01":"2026-08-01"].to_string())
for a, b in [("2025-08-01", "2026-08-01"), ("2026-05-01", "2026-08-01")]:
    print(f"impulso sem precatórios {a}→{b}: {-(x12.loc[b] - x12.loc[a]):+.2f} p.p.; com: {-(p12.loc[b] - p12.loc[a]):+.2f}")

desp_x = r["despesa_total"] - prec
real = lambda s, m: (s.loc[m] * fator.loc[m]).sum()
m1 = pd.date_range("2025-09-01", "2026-08-01", freq="MS")
m0 = pd.date_range("2024-09-01", "2025-08-01", freq="MS")
print(f"despesa total sem precatórios, real 12m: {(real(desp_x, m1) / real(desp_x, m0) - 1) * 100:+.1f}%")
print(f"receita líquida, real 12m: {(real(r['receita_liquida'], m1) / real(r['receita_liquida'], m0) - 1) * 100:+.1f}%")
ben_x = r["beneficios_previdenciarios"] - r[prec_cols[1]] - r[prec_cols[2]]
print(f"benefícios previdenciários sem precatórios, real 12m: {(real(ben_x, m1) / real(ben_x, m0) - 1) * 100:+.1f}%")

print("\ndiscricionárias do Executivo: crescimento real contra o mesmo trimestre do ano anterior (soma de 3 meses)")
d = r["despesas_discricionarias_do_poder_executivo"] * fator
d3 = d.rolling(3).sum()
yy = (d3 / d3.shift(12) - 1) * 100
print(yy.loc["2025-08-01":"2026-08-01"].iloc[::1].round(1).to_string())
print("discricionárias set/2025-dez/2025 (R$ bi correntes):", round(r.loc["2025-09-01":"2025-12-01", "despesas_discricionarias_do_poder_executivo"].sum() / 1e3, 1),
      "· set/2024-dez/2024:", round(r.loc["2024-09-01":"2024-12-01", "despesas_discricionarias_do_poder_executivo"].sum() / 1e3, 1))
print("primário do governo central set-dez/2025 (R$ bi, + = superávit):",
      round(prim.loc["2025-09-01":"2025-12-01"].sum() / 1e3, 1))
