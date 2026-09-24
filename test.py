import numpy as np
import matplotlib.pyplot as plt

# ============================================================
# 1) Caso 2D: projetar y sobre a reta gerada por um vetor x
# ============================================================
x = np.array([4.0, 1.0])      # direção da reta (o "espaço coluna" com 1 coluna)
y = np.array([2.0, 3.0])      # vetor a ser projetado

beta = (x @ y) / (x @ x)      # mesma fórmula de (X^T X)^(-1) X^T y, com 1 coluna
y_hat = beta * x              # a "sombra"
e = y - y_hat                 # resíduo

print("2D -> beta:", beta, "| x·e =", round(x @ e, 10))

fig, ax = plt.subplots(figsize=(6, 5))
t = np.linspace(-0.3, 1.3, 2)
ax.plot(t * x[0], t * x[1], color="lightgray", lw=6, label="reta gerada por x")
ax.quiver(0, 0, *y, angles="xy", scale_units="xy", scale=1, color="teal", label="y")
ax.quiver(0, 0, *y_hat, angles="xy", scale_units="xy", scale=1, color="purple", label="ŷ (projeção)")
ax.plot([y_hat[0], y[0]], [y_hat[1], y[1]], "--", color="coral", lw=2, label="e = y − ŷ")
ax.set_aspect("equal")
ax.set_xlim(-0.5, 5); ax.set_ylim(-0.5, 4)
ax.grid(alpha=0.3); ax.legend(loc="upper right")
ax.set_title("Projeção ortogonal em 2D")
plt.savefig("projecao_2d.png", dpi=120, bbox_inches="tight")

# ============================================================
# 2) Caso 3D: o exemplo da regressão (3 pontos, 2 coeficientes)
# ============================================================
X = np.array([[1, 1],
              [1, 2],
              [1, 3]], dtype=float)
y = np.array([1, 2, 2], dtype=float)

beta = np.linalg.solve(X.T @ X, X.T @ y)   # equações normais
y_hat = X @ beta
e = y - y_hat

print("3D -> beta:", beta, "| X^T e =", np.round(X.T @ e, 10))

# direção da câmera que deixa ŷ e e "de frente" (perpendicular aos dois)
n = np.cross(X[:, 0], X[:, 1])            # normal do plano
d = np.cross(n, y_hat); d /= np.linalg.norm(d)
elev_lado = np.degrees(np.arcsin(d[2]))
azim_lado = np.degrees(np.arctan2(d[1], d[0]))

fig = plt.figure(figsize=(13, 6))
vistas = [("Visão geral", 20, -60, 3),
          ("Visão de lado: o ângulo reto aparece", elev_lado, azim_lado, 2.5)]

for i, (titulo, elev, azim, lim) in enumerate(vistas, start=1):
    ax = fig.add_subplot(1, 2, i, projection="3d", proj_type="ortho")

    # plano = todas as combinações a*col1 + b*col2
    a, b = np.meshgrid(np.linspace(-1, 2, 10), np.linspace(-0.5, 1.2, 10))
    P = a[..., None] * X[:, 0] + b[..., None] * X[:, 1]
    ax.plot_surface(P[..., 0], P[..., 1], P[..., 2], alpha=0.2, color="purple")

    def seta(v, cor, rotulo):
        ax.quiver(0, 0, 0, *v, color=cor, arrow_length_ratio=0.08, lw=2, label=rotulo)

    seta(X[:, 0], "gray", "coluna 1 = (1,1,1)")
    seta(X[:, 1], "black", "coluna 2 = (1,2,3)")
    seta(y, "teal", "y")
    seta(y_hat, "purple", "ŷ = Xβ̂")
    ax.plot(*zip(y_hat, y), "-", color="orangered", lw=3, label="e = y − ŷ")

    ax.set_xlim(0, lim); ax.set_ylim(0, lim); ax.set_zlim(0, lim)
    ax.set_box_aspect((1, 1, 1))              # escalas iguais: ângulos não distorcem
    ax.set_xlabel("obs 1"); ax.set_ylabel("obs 2"); ax.set_zlabel("obs 3")
    ax.view_init(elev=elev, azim=azim)        # mude para girar a câmera
    ax.set_title(titulo)
    if i == 1:
        ax.legend(loc="upper left")

plt.savefig("projecao_3d.png", dpi=120, bbox_inches="tight")

plt.show()   # no seu computador, a janela 3D pode ser girada com o mouse