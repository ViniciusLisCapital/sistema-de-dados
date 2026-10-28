"""fi: as diferenças e variações pequenas citadas no texto do report, todas a partir dos arquivos A
(janelas de fim de setembro e de outubro, ondas do crédito ao BNDES) e dos caminhos dos cenários."""
from pathlib import Path
import pandas as pd
A = Path(__file__).resolve().parent.parent / "A"
r = lambda f: pd.read_csv(A / f"{f}.csv.gz", parse_dates=["date"])
br = r("br_interest_rate")
nb = br[(br.curve == "NTNBJS") & (br.tenor == "120M")].set_index("date").value
di = br[(br.curve == "DIPRE") & (br.tenor == "120M")].set_index("date").value
c = r("cmb_risco_pais"); cds = c[c.name == "cds_5y_usd"].set_index("date").value
pt = r("cmb_ptax"); pt = pt[pt.name == "ptax_venda"].set_index("date").value
fx = r("cmb_fx_latam"); mx = fx[fx.country_code == "MX"].set_index("date").value
de = r("cmb_dollar_index_em").set_index("date").value
pc = lambda s, a, b: round(100 * (s[b] / s[a] - 1), 2)
print("CDS 17/09 -> 30/09:", round(cds["2026-09-30"] - cds["2026-09-17"], 1), "p.b.")
print("MXN 17/09 -> 30/09:", pc(mx, "2026-09-17", "2026-09-30"), "% · dxy_em:", pc(de, "2026-09-17", "2026-09-30"), "%")
print("21/09 contra 18/09: CDS", round(cds["2026-09-21"] - cds["2026-09-18"], 1), "p.b. · PTAX", pc(pt, "2026-09-18", "2026-09-21"), "% · DI 10a", round(100 * (di["2026-09-21"] - di["2026-09-18"]), 0), "p.b.")
print("MXN 30/09 -> 20/10:", pc(mx, "2026-09-30", "2026-10-20"), "%")
ii = 100 * ((1 + di / 100) / (1 + nb / 100) - 1)
print("Inflação implícita 10a 26/10 contra 30/09:", round(ii["2026-10-26"] - ii["2026-09-30"], 2), "p.p.")
print("CDS 05/10–23/10: mín", cds["2026-10-05":"2026-10-23"].min(), "máx", cds["2026-10-05":"2026-10-23"].max(),
      "· NTN-B 10a: mín", round(nb["2026-10-05":"2026-10-23"].min(), 2), "máx", round(nb["2026-10-05":"2026-10-23"].max(), 2))
dl = r("fisc_dlsp_fatores")
cr = dl[(dl.fator == "estoque") & (dl.item == "interna__gov_federal__creditos_inst_fin_oficiais")].set_index("date").value / 1000
w1 = cr["2025-12-01"] - cr["2025-08-01"]; w2 = cr["2026-08-01"] - cr["2026-04-01"]; tot = cr["2026-08-01"] - cr["2025-08-01"]
print(f"Crédito ao BNDES: set–dez/25 {w1:.1f} · mai–ago/26 {w2:.1f} · 12m {tot:.1f} (R$ bi; negativo = mais crédito) · fração mai–ago/26 {100*w2/tot:.0f}%")
print("Caminhos: base CDS 4T26 − último (140 − 137,43):", round(140 - 137.43, 1), "· upside 2T27 − 3T26 (200 − 131,21):", round(200 - 131.21, 1),
      "· base rr_10a 1T27 − 26/10 (7,80 − 8,05):", round(7.80 - 8.054, 2), "· upside rr_10a 2T27 − 3T26 (9,00 − 7,84):", round(9.00 - 7.843, 2))
print("Selic do modelo 1T27, base − downside (13,21 − 12,31):", round(13.21 - 12.31, 2))
# multiplicador que reproduz +9,19% (interpolação linear entre x5 = 8,01% e x6 = 9,68%, fi_cds_peso_real.py)
print("Multiplicador para +9,19%:", round(5 + (9.19 - 8.01) / (9.68 - 8.01), 1))
# maior alta de um pregão da NTN-B 10a antes de out/26 (sem filtro de um por mês)
d = (nb.sort_index().diff() * 100)
antes = d[d.index < "2026-10-01"]
print("Maiores altas diárias da NTN-B 10a até set/26 (p.b.):", antes.nlargest(5).round(1).to_dict())
print("26/10:", round(d["2026-10-26"], 1))
di1 = br[(br.curve == "DIPRE") & (br.tenor == "12M")].set_index("date").value
print("DI 1a 26/10 − Selic 13,75:", round(100 * (di1["2026-10-26"] - 13.75), 0), "p.b.")
