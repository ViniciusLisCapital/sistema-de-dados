"""fi: os três cenários fiscais no Modelo Estrutural (CDS = `fiscal`, NTN-B 10a = `rr_10a`), mais o padrão
do simulador e dois cenários isolando cada exógena, para contar a história de cada canal."""
import sys
from analytics.agent_system import modelo
sys.stdout.reconfigure(encoding="utf-8")
T = ["4T26", "1T27", "2T27", "3T27", "4T27", "1T28"]
cen = {
    "base":     {"fiscal": [140, 140, 138, 135, 135, 135], "rr_10a": [7.70, 7.80, 7.70, 7.60, 7.55, 7.50]},
    "upside":   {"fiscal": [165, 190, 200, 200, 195, 190], "rr_10a": [8.05, 8.80, 9.00, 9.00, 8.90, 8.80]},
    "downside": {"fiscal": [115, 110, 108, 106, 105, 105], "rr_10a": [7.35, 6.90, 6.80, 6.75, 6.70, 6.70]},
}
sim = modelo.carregar("2026-10-27")
def cm(d):
    return {k: dict(zip(T, v)) for k, v in d.items()}
print("=== PADRÃO DO SIMULADOR ===")
print(modelo.texto(modelo.rodar(sim, faixa=False), T))
for n, d in cen.items():
    print(f"\n=== {n.upper()} ===")
    print(modelo.texto(modelo.rodar(sim, caminhos=cm(d)), T))
print("\n=== SÓ O CDS DO UPSIDE (rr_10a no padrão) ===")
print(modelo.texto(modelo.rodar(sim, caminhos=cm({"fiscal": cen["upside"]["fiscal"]}), faixa=False), T))
print("\n=== SÓ A rr_10a DO UPSIDE (CDS no padrão) ===")
print(modelo.texto(modelo.rodar(sim, caminhos=cm({"rr_10a": cen["upside"]["rr_10a"]}), faixa=False), T))
print("\n=== BASE com F.b_fiscal x 1,2 (argumento ao câmbio) ===")
print(modelo.texto(modelo.rodar(sim, caminhos=cm(cen["base"]), mult={"F.b_fiscal": 1.2}, faixa=False), T))
print("\n=== UPSIDE com F.b_fiscal x 1,5 (argumento ao câmbio) ===")
print(modelo.texto(modelo.rodar(sim, caminhos=cm(cen["upside"]), mult={"F.b_fiscal": 1.5}, faixa=False), T))
