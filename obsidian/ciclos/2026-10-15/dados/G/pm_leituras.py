"""G pm: as contas pequenas que o report de política monetária cita (ciclo 2026-10-15).
Lê só A/. Cada bloco imprime o número e de onde ele vem."""
from pathlib import Path
import pandas as pd

A = Path(__file__).resolve().parent.parent / "A"


def ler(arq):
    return pd.read_csv(A / arq, parse_dates=["date"])


# 1. IPCA de setembro contra o QPC (mediana, R281) e contra a projeção do Copom (RPM set/26, Tabela 2.1.2: 0,65)
inf = ler("inflc_agregados.csv.gz").pivot(index="date", columns="name", values="value")
s = inf.loc["2026-09-01"]
nuc = ["ipca_nucleo_ex0", "ipca_nucleo_ex03", "ipca_nucleo_medias_aparadas", "ipca_nucleo_dp", "ipca_nucleo_p55"]
media_nuc = s[nuc].mean()
print(f"1. IPCA set/26 {s['ipca']:.2f}: −QPC 0,56 = {s['ipca'] - 0.56:+.2f} p.p.; −RPM 0,65 = {s['ipca'] - 0.65:+.2f} p.p.")
print(f"   média dos 5 núcleos do BC (EX0, EX3, MS, DP, P55) set/26 = {media_nuc:.3f}; −QPC 0,29 = {media_nuc - 0.29:+.2f} p.p.")
print(f"   EX3 serviços set/26 {s['ipca_nucleo_ex03_servicos']:.2f}; −QPC 0,30 = {s['ipca_nucleo_ex03_servicos'] - 0.30:+.2f} p.p.")
m3 = inf.loc["2026-07-01":"2026-09-01", nuc].mean(axis=1)
print(f"   média dos núcleos por mês jul–set: " + " · ".join(f"{d:%m} {v:.3f}" for d, v in m3.items()))
ac3 = ((1 + m3 / 100).prod() - 1) * 100
print(f"   média dos núcleos, acum. 3m jul–set = {ac3:.2f}%, anualizado {((1 + ac3 / 100) ** 4 - 1) * 100:.2f}% (sem ajuste sazonal)")
print(f"   IPCA 12m: " + " · ".join(f"{d:%Y-%m} {v:.2f}" for d, v in inf['ipca_12m'].loc['2026-03-01':].items())
      + "  (limite superior da meta: 3,00 + 1,50 = 4,50)")

# 2. Juro real e postura
selic, focus12 = 13.75, 4.48
real_exante = ((1 + selic / 100) / (1 + focus12 / 100) - 1) * 100
print(f"2. Selic real ex-ante refeita aqui = {real_exante:.2f}% (o F imprime 8,88, com a Focus sem arredondar)")
F_REAL = 8.88
print(f"   8,88 − neutro do Copom (RPM set/26, 5,00) = {F_REAL - 5.00:+.2f} p.p.; "
      f"8,88 − NTN-B 10a (6,87, âncora do modelo) = {F_REAL - 6.87:+.2f} p.p.")
print(f"   NTN-B 10a 15/10 (6,869) − média 3T26 (7,843) = {6.869 - 7.843:+.2f} p.p.")
print(f"   aperto no modelo (Selic − NTN-B 10a − meta): hoje 13,75 − 6,87 − 3,00 = {13.75 - 6.87 - 3.00:.2f}; "
      f"3T26 (médias) 14,06 − 7,84 − 3,00 = {14.06 - 7.84 - 3.00:.2f}")
print(f"   juro real neutro QPC 2a: R279 6,00 − R275 5,50 = {6.00 - 5.50:+.2f}")

# 3. Inflação implícita (DI × NTN-B, mesmo prazo, Fisher) hoje, 1 mês e 3 meses antes
br = ler("br_interest_rate.csv.gz")
for ten in ["12M", "24M", "60M", "120M"]:
    di = br[(br.curve == "DIPRE") & (br.tenor == ten)].set_index("date")["value"].sort_index()
    nb = br[(br.curve == "NTNBJS") & (br.tenor == ten)].set_index("date")["value"].sort_index()
    j = pd.concat({"di": di, "nb": nb}, axis=1).dropna()
    imp = ((1 + j.di / 100) / (1 + j.nb / 100) - 1) * 100
    out = []
    for d in ["2026-10-15", "2026-09-15", "2026-07-15", "2026-10-02"]:
        v = imp[:d]
        out.append(f"{v.index[-1]:%d/%m} {v.iloc[-1]:.2f}")
    print(f"3. inflação implícita {ten}: " + " · ".join(out))

# 4. Curva DI por reunião: o passo implícito em fração de −25 (se as opções forem só manter ou −25)
for reu, passo in [("04/11", -18), ("09/12", -19), ("27/01", -20), ("17/03", -19)]:
    print(f"4. {reu}: passo implícito {passo} p.b. = {passo / -25:.0%} de um corte de 25")
print(f"   Selic na curva em 08/12/27 (12,13) − vigente 13,75 = {12.13 - 13.75:+.2f} p.p.; "
      f"Focus R8/2027 (12,00) − 13,75 = {12.00 - 13.75:+.2f}")

# 5. Câmbio contra o condicionante do Copom (R$ 5,15 no cenário de referência da 281ª)
print(f"5. PTAX 14/10 5,0441 contra 5,15: {(5.0441 / 5.15 - 1) * 100:+.1f}%")

# 6. Brent contra a premissa do Copom (média de US$ 90 no 3T26, RPM set/26 2.2; ~US$ 84 no 2T27)
br_ = ler("comm_brent.csv.gz").set_index("date")["value"].sort_index()
print(f"6. Brent 06/10 {br_.iloc[-1]:.2f}: contra 90 = {(br_.iloc[-1] / 90 - 1) * 100:+.0f}%; contra 84 = {(br_.iloc[-1] / 84 - 1) * 100:+.0f}%"
      f"; máximo de set–out/26 {br_['2026-09-01':].max():.2f} em {br_['2026-09-01':].idxmax():%d/%m}")

# 7. Projeção do Copom no horizonte relevante contra a meta
print(f"7. IPCA projetado 1T28 3,2 − meta 3,00 = {3.2 - 3.0:+.1f} p.p.")

# 8. Crédito: concessões livres 12m contra 12m um ano antes (nominal)
for n, a, b in [("PF", 4074.7, 3685.6), ("PJ", 3487.1, 3126.1)]:
    print(f"8. concessões livres {n}, soma 12m: {(a / b - 1) * 100:+.1f}% contra um ano antes")

# 9. Focus por trimestre: a Selic de fechamento que a pesquisa e a curva dão (última reunião do trimestre)
print("9. Focus/DI no fechamento: 4T26 13,25/13,38 · 1T27 13,00/12,99 · 2T27 12,62/12,58 · 3T27 12,25/12,25 · 4T27 12,00/12,13 (F, Leituras combinadas)")
for q, foc, di, c in [("4T26", 13.25, 13.38, 12.47), ("1T27", 13.00, 12.99, 12.14), ("2T27", 12.62, 12.58, 11.86),
                      ("3T27", 12.25, 12.25, 11.62), ("4T27", 12.00, 12.13, 11.41)]:
    print(f"   {q}: central do modelo {c:.2f} − Focus = {c - foc:+.2f}; − curva = {c - di:+.2f}")

# 10. Inflação implícita de 10 anos contra a meta, e a variação de um mês
print(f"10. implícita 10a 15/10 5,55 − meta 3,00 = {5.55 - 3.00:+.2f} p.p.; 5,55 − 6,28 (15/09) = {5.55 - 6.28:+.2f} p.p.; "
      f"implícita 1a 6,84 − 6,72 (15/09) = {6.84 - 6.72:+.2f} p.p.; 6,84 − Focus 12m 4,48 = {6.84 - 4.48:+.2f} p.p.")
# 11. O tempero do gradualismo contra a central do modelo (pm_tempero_ii.py)
for q, c, t_ in [("4T26", 12.47, 13.25), ("1T27", 12.14, 12.75), ("2T27", 11.86, 12.25), ("3T27", 11.62, 11.75),
                 ("4T27", 11.41, 11.50), ("1T28", 11.22, 11.25)]:
    print(f"11. {q}: com gradualismo {t_:.2f} − modelo {c:.2f} = {t_ - c:+.2f} p.p.")
# 12. O que o fechamento de 12,47 no 4T26 exige: corte acumulado nas duas reuniões do trimestre
print(f"12. 12,50 (grade mais perto de 12,47) − 13,75 = {12.50 - 13.75:+.2f} p.p. em duas reuniões")
print(f"    a média do 4T26 tem 13,75 de 01/10 a 04/11: dias corridos {(pd.Timestamp('2026-11-04') - pd.Timestamp('2026-10-01')).days} "
      f"de {(pd.Timestamp('2026-12-31') - pd.Timestamp('2026-09-30')).days}")
# 13. Minha média de fechamento (pm_reunioes.py) contra a Focus e a curva
for q, m, foc, di in [("4T26", 13.45, 13.25, 13.38), ("1T27", 13.15, 13.00, 12.99), ("2T27", 12.85, 12.62, 12.58),
                      ("3T27", 12.55, 12.25, 12.25), ("4T27", 12.28, 12.00, 12.13)]:
    print(f"13. {q}: média do agente {m:.2f} − Focus = {m - foc:+.2f}; − curva = {m - di:+.2f}")
# 14. Complementos citados no texto
print(f"14. pausa implícita na curva em 04/11 = 1 − 72% = {1 - 0.72:.0%}; surpresa se mantiver = 18 p.b.; se cortar 25 = {25 - 18} p.b.")
print(f"    NTN-B 1a 5,80 − neutro do Copom 5,00 = {5.80 - 5.00:+.2f} p.p.")
for d in ["2026-10-02", "2026-10-05"]:
    di = br[(br.curve == "DIPRE") & (br.tenor == "120M")].set_index("date")["value"].sort_index()[:d].iloc[-1]
    nb = br[(br.curve == "NTNBJS") & (br.tenor == "120M")].set_index("date")["value"].sort_index()[:d].iloc[-1]
    print(f"    {d}: DI 10a {di:.2f} · NTN-B 10a {nb:.2f} · implícita 10a {((1 + di / 100) / (1 + nb / 100) - 1) * 100:.2f}")
