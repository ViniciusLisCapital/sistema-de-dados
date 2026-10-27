"""G do fiscal, ciclo 2026-10-02: contas pequenas que o report cita.

1. F.b_fiscal por p.b. de variação do CDS (mediana e intervalo de 90%, sobre o desvio de 298,5 p.b.
   que `modelo.listar()` imprime), e o efeito de +10 p.b. e de +60 p.b. no câmbio do trimestre.
2. NTN-B 10a de 02/10/2026 contra o juro real neutro de 5 anos da QPC (mediana, jun/2026).
3. O que o Focus do primário de 2026 pede de set-dez/2026, contra set-dez/2025 (NFSP).
4. Distância entre o primário de 12 meses e o estabilizador da DLSP.
5. EFGG: a Δ da despesa exceto juros sem as transferências entre esferas (soma dos itens que
   chegam à demanda: benefícios, remuneração, bens e serviços, investimento líquido, subsídios).
6. O aperto na convenção da curva IS, hoje: (Selic − meta) − NTN-B 10a.
"""
import pandas as pd

A = "obsidian/ciclos/2026-10-02/dados/A/"
sd = 298.5
for nome, b in [("mediana", 25.111), ("p5", 19.481), ("p95", 30.608), ("x1,2", 25.111 * 1.2)]:
    print(f"F.b_fiscal {nome}: {b / sd:.4f} % por p.b.; +10 p.b. → {10 * b / sd:+.2f}%; +60 p.b. → {60 * b / sd:+.2f}%")

ntnb = pd.read_csv(A + "br_interest_rate.csv.gz", parse_dates=["date"])
ntnb = ntnb[(ntnb.curve == "NTNBJS") & (ntnb.tenor == "120M")].set_index("date")["value"]
q = pd.read_csv(A + "expc_qpc.csv.gz")
neu = q[(q.bloco == "juro_real_neutro") & (q.referencia == "5a") & (q.estatistica == "mediana")].sort_values("date").iloc[-1]
print(f"\nNTN-B 10a {ntnb.loc['2026-10-02']:.2f} − neutro 5a QPC {neu.valor:.2f} ({neu.date}) = {ntnb.loc['2026-10-02'] - neu.valor:.2f} p.p.")
print(f"NTN-B 10a máx 02/07/2026 {ntnb.loc['2026-07-02']:.2f} − neutro = {ntnb.loc['2026-07-02'] - neu.valor:.2f} p.p.")

nf = pd.read_csv(A + "fisc_nfsp.csv.gz", parse_dates=["date"]).pivot(index="date", columns="name", values="value")
pib = pd.read_csv(A + "atv_pib_mensal.csv.gz", parse_dates=["date"]).pivot(index="date", columns="name", values="value")
p12 = pib.loc["2026-09-01", "pib_acum_12m"]
falta = (-0.41 - (-0.62)) / 100 * p12
sd25 = nf.loc["2025-09-01":"2025-12-01", "resultado_primario_fluxo_mensal"].sum()
print(f"\nFocus 2026 −0,41 contra 12m −0,62: faltam {falta / 1e3:.1f} R$ bi (PIB 12m set/2026 R$ {p12 / 1e6:.2f} tri); "
      f"set-dez/2025 deu {sd25 / 1e3:+.1f}; set-dez/2026 teria de dar ~{(sd25 + falta) / 1e3:+.1f} R$ bi")
print(f"\nprimário estabilizador 4,26 − primário 12m (−0,62) = {4.26 - (-0.62):.2f} p.p. do PIB")

ef = pd.read_csv(A + "fisc_efgg.csv.gz", parse_dates=["date"]).pivot(index="date", columns="name", values="value")
pq = pib["pib_mensal"].resample("QS").sum().rolling(4).sum()
itens = ["geral_beneficios_previdenciarios_assistenciais", "geral_remuneracao_empregados", "geral_uso_bens_servicos",
         "geral_investimento_liquido", "geral_subsidios"]
s = ef[itens].sum(axis=1).rolling(4).sum() / pq.reindex(ef.index) * 100
print(f"\nEFGG itens de demanda (4 itens + subsídios), 4 tri: 2T26 {s.loc['2026-04-01']:.2f} vs 2T25 {s.loc['2025-04-01']:.2f}, "
      f"Δ {s.loc['2026-04-01'] - s.loc['2025-04-01']:+.2f} p.p.; 1T26 {s.loc['2026-01-01']:.2f}, 4T25 {s.loc['2025-10-01']:.2f}")

sel = pd.read_csv(A + "br_interest_rate.csv.gz", parse_dates=["date"])
sel = sel[(sel.curve == "POLICY")].set_index("date")["value"]
print(f"\naperto na convenção da (H), hoje: Selic {sel.loc['2026-10-02']:.2f} − meta 3,00 − NTN-B 10a {ntnb.loc['2026-10-02']:.2f} = "
      f"{sel.loc['2026-10-02'] - 3.0 - ntnb.loc['2026-10-02']:.2f} p.p.")

# 7. As faixas históricas do CDS aplicadas ao nível de 02/10/2026 (percentis 25 e 75 da variação
#    % de 1 e 5 trimestres desde 2010, de fi_premio_risco.py) e o tamanho do upside em %.
cds0 = 131.04
print("faixa p25-p75 de 1 trimestre:", round(cds0 * (1 - 0.16)), "a", round(cds0 * 1.07),
      "· de 5 trimestres:", round(cds0 * (1 - 0.24)), "a", round(cds0 * 1.40))
print("upside de +60 p.b. partindo de", cds0, "=", round(60 / cds0 * 100), "%")
