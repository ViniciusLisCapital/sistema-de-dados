"""G cambio (rodada 2): as contas da tese com as saídas do modelo (cambio_r2_cenarios.py, cambio_vol_r2.py).
Os números de entrada são os que esses G imprimiram; aqui só a aritmética dos temperos e das distâncias."""
T = ["4T26", "1T27", "2T27", "3T27", "4T27", "1T28"]
base = [5.435, 5.503, 5.508, 5.495, 5.526, 5.565]            # P1 (= base_P1)
sp_parado = [5.430, 5.474, 5.456, 5.421, 5.429, 5.445]
sp_meio = [5.428, 5.486, 5.480, 5.457, 5.477, 5.506]          # F.b_sp500 x 0,55
up_m12 = [5.654, 5.848, 5.891, 5.863, 5.859, 5.874]           # upside, F.b_fiscal x 1,2
up_sem = [5.622, 5.791, 5.823, 5.796, 5.796, 5.816]
up_m15 = [5.703, 5.935, 5.993, 5.966, 5.954, 5.962]
dn = [5.256, 5.337, 5.349, 5.350, 5.386, 5.422]
dn_sp = [5.249, 5.319, 5.321, 5.312, 5.339, 5.364]           # downside com F.b_sp500 x 0,55

print("Efeito do caminho do S&P no base (base - S&P parado) e da peso x0,55 (base - x0,55):")
for t, b, s, m in zip(T, base, sp_parado, sp_meio):
    print(f"  {t}: +{b - s:.3f} ({100 * (b / s - 1):.2f}%)   peso x0,55: -{b - m:.3f} ({100 * (m / b - 1):.2f}%)")

print("\nUpside com tempero (ii): 4T26 posição +1% e BC -1,5%; 1T27 BC -1%")
print(f"  4T26: {up_m12[0]:.3f} -> {up_m12[0] * 1.01 * 0.985:.3f}")
print(f"  1T27: {up_m12[1]:.3f} -> {up_m12[1] * 0.99:.3f}")
print("Efeito do x1,2 e do x1,5 sobre o upside sem multiplicador:")
for t, a, b, c in zip(T, up_sem, up_m12, up_m15):
    print(f"  {t}: {a:.3f} -> x1,2 {b:.3f} ({100*(b/a-1):.2f}%) -> x1,5 {c:.3f} ({100*(c/a-1):.2f}%)")

print("\nSazonalidade de dezembro (+2,1%):")
print(f"  4T26: {base[0]:.3f} -> {base[0] * 1.021:.3f}   4T27: {base[4]:.3f} -> {base[4] * 1.021:.3f}")

print("\nContra o condicionante do Copom (R$ 5,15):")
for nome, v in [("central 4T26", base[0]), ("PTAX 26/10", 5.5007), ("PTAX 23/10", 5.0377), ("InfoMoney 27/10 9h52", 5.333)]:
    print(f"  {nome}: {v:.4f} -> {100 * (v / 5.15 - 1):+.2f}%")
print("\nCentral contra a PTAX de 26/10:", f"{100 * (base[0] / 5.5007 - 1):+.2f}%")
print("P1 contra r1 (central):", [f"{b - r:+.3f}" for b, r in zip(base, [5.38, 5.39, 5.37, 5.35, 5.35, 5.38])])
print("Queda de 27/10 até 9h52 (InfoMoney) contra 26/10:", f"{100 * (5.333 / 5.5007 - 1):+.2f}%")

up_rrb = [5.662, 5.872, 5.928, 5.908, 5.904, 5.918]          # upside x1,2 com a NTN-B no base
dn_rrb = [5.243, 5.304, 5.314, 5.317, 5.353, 5.390]          # downside com a NTN-B no base
print("\nEfeito da NTN-B de cauda (via Selic) na PTAX:")
for t, a, b, c, d_ in zip(T, up_m12, up_rrb, dn, dn_rrb):
    print(f"  {t}: upside NTN-B no base - upside = {b - a:+.3f}   downside - downside NTN-B no base = {c - d_:+.3f}")
