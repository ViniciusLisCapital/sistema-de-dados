"""G externo: quanto cada exógena do cenário base move a PTAX contra o padrão do simulador (tirando uma
de cada vez do caminho base e rodando de novo). Lê o retrato do modelo e ex_cenarios.py."""
from analytics.agent_system import modelo
import ex_cenarios as C
sim = modelo.carregar("2026-10-27"); base = C.caminhos()
def ptax(cam):
    r = modelo.rodar(sim, caminhos=cam); t = modelo.texto(r, C.TRIS)
    ln = [l for l in t.splitlines() if l.startswith("| PTAX")][0]
    return [c.split(" [")[0].strip() for c in ln.split("|")[3:9]]
pb = ptax(base); pdf = ptax({})
print("padrão:", pdf); print("base  :", pb)
for k in base:
    cam = {kk: vv for kk, vv in base.items() if kk != k}
    print(f"base sem {k:13s}:", ptax(cam))
