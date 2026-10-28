"""Atividade, rodada 2: contas pequenas citadas no report.

- capital de giro: concessões em 12 meses até ago/26 contra um ano antes (cred_modalidade_livre_pj), e o
  tamanho do Brasil Soberano (R$ 15 bi + R$ 6 bi, notícia r1-25) contra o aumento;
- Selic: a média da distribuição da política monetária para 09/12 (13,83, politica_monetaria_r1) e a manutenção
  em 13,75 contra a Selic do P1 (fechamento e média do 4T26, média do 1T27);
- rr_10a do P1 no 4T26 contra a média do 3T26 (7,84, padrão do simulador);
- o hiato do P1 no 1T28 contra a projeção do RPM de set/26 (−0,4).
"""
import json
from pathlib import Path

CIC = Path(__file__).resolve().parents[2]
P1 = json.loads((CIC / "P1.json").read_text(encoding="utf-8"))
m = P1["modelo"]; tr = m["trimestres"]
sel = m["endogenas"]["selic"]["central"]
fim = m["endogenas"].get("selic_fim", {}).get("central") if "selic_fim" in m["endogenas"] else None

aumento = 534.9 - 335.3
print(f"capital de giro: aumento das concessoes em 12 meses R$ {aumento:.1f} bi; Brasil Soberano 21 / aumento = {21/aumento:.2f}")
print(f"Selic media P1: 4T26 {sel[tr.index('4T26')]:.2f}, 1T27 {sel[tr.index('1T27')]:.2f}")
if fim:
    print(f"Selic fechamento P1 4T26 {fim[tr.index('4T26')]:.2f}; 13,83 - P1 = {13.83 - fim[tr.index('4T26')]:.2f}")
print(f"13,75 - media P1 4T26 = {13.75 - sel[tr.index('4T26')]:.2f}; 13,75 - media P1 1T27 = {13.75 - sel[tr.index('1T27')]:.2f}")
rr = P1["caminhos_usados"]["rr_10a"]
print(f"rr_10a P1 4T26 {rr['4T26']:.2f} - media 3T26 7,84 = {rr['4T26'] - 7.84:+.2f}; 8,05 (26/10) - P1 4T26 = {8.05 - rr['4T26']:+.2f}")
h = m["endogenas"]["hiato"]["central"][tr.index("1T28")]
print(f"hiato P1 1T28 {h:.2f}; contra -0,4 do RPM: {h + 0.4:+.2f}")
