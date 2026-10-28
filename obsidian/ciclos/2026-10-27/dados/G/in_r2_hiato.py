"""in_r2_hiato: tamanho, no IPCA, de 0,15 p.p. de hiato a menos em serviços (moderação, item 7).
Direto pelo coeficiente: I.IS.is2 (mediana 0,0922) x 0,15 x peso de serviços (36,24%, set/26),
por trimestre; e o mesmo com is2 x 1,5 (o tempero do downside)."""
is2, w = 0.09217197, 0.3624
for m in (1.0, 1.5):
    q = is2 * m * 0.15 * w
    print(f"is2 x {m}: {q:.4f} p.p. no trimestre; ~{4*q:.3f} p.p. em 12 meses se durar 4 trimestres")
