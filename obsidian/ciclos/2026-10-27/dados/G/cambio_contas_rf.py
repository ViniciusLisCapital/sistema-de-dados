"""G cambio (report final): aritmética da tese com as saídas de cambio_rf_cenarios.py (números copiados de lá)."""
T = ["4T26", "1T27", "2T27", "3T27", "4T27", "1T28"]
base = [5.427, 5.515, 5.517, 5.501, 5.511, 5.528]
sp_parado = [5.421, 5.486, 5.464, 5.427, 5.414, 5.409]
sp_055 = [5.420, 5.497, 5.488, 5.463, 5.462, 5.470]
up_sem = [5.636, 5.869, 5.880, 5.831, 5.824, 5.831]
up_12 = [5.673, 5.942, 5.958, 5.904, 5.890, 5.889]
up_rrb = [5.682, 5.966, 5.992, 5.945, 5.932, 5.930]
dn = [5.279, 5.350, 5.363, 5.369, 5.403, 5.433]
dn_sp = [5.272, 5.333, 5.336, 5.332, 5.355, 5.376]
dn_rrb = [5.266, 5.326, 5.334, 5.340, 5.374, 5.404]
r2 = [5.435, 5.503, 5.508, 5.495, 5.526, 5.565]
for i, t in enumerate(T):
    print(f"{t}: S&P +{base[i]-sp_parado[i]:.3f} ({100*(base[i]/sp_parado[i]-1):.2f}%) | x0,55 {sp_055[i]-base[i]:+.3f} "
          f"| x1,2 {100*(up_12[i]/up_sem[i]-1):+.2f}% | NTN-B up {up_rrb[i]-up_12[i]:+.3f} dn {dn[i]-dn_rrb[i]:+.3f} "
          f"| P2-r2 {base[i]-r2[i]:+.3f}")
print(f"upside 4T26 com posição +1% e BC -1,5%: {up_12[0]*1.01*0.985:.3f};  1T27 com BC -1%: {up_12[1]*0.99:.3f}")
print(f"sazonal: 4T26 {base[0]*1.021:.3f}  4T27 {base[4]*1.021:.3f}")
print(f"central 4T26 contra PTAX 26/10: {100*(base[0]/5.5007-1):+.2f}%")

# cobrança C1: central do PF* no 4T26
pf = 5.42582
print(f"PF 4T26 {pf:.3f}: contra PTAX 26/10 {100*(pf/5.5007-1):+.2f}%  sazonal {pf*1.021:.3f}")
