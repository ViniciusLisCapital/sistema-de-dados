# analytics/agent_system/ — diagrama do sistema de agentes

Gera `team_materials/structure_materials/Sistema de Agentes.html`: um diagrama SVG da visão geral
— processos de entrada, os três blocos que o agente recebe (dados, ferramentas, conhecimento) e o
ciclo dos agentes (rodada 1 → P1 → rodada 2 → P2 → memo final → PF*), no desenho do usuário de
2026-10-02. Não lê o banco e não está no manifesto de dashboards.

```
uv run python -m analytics.agent_system.generate_report
```

- **À mão, no `report.html`:** caixas, setas e o estado de cada bloco (existe / em construção /
  planejado), em `SPECS.geral` e `rodadasGeral()`; a lista `FERRAMENTAS`.
- **Lido na geração:** contagens do registry, dos connectors e das notas do vault por área.

As abas Ciclo, Ferramentas e Dados (e o painel de detalhe ao clicar) saíram em 2026-10-02, a pedido
do usuário; voltam quando o fluxo de cada uma estiver definido. A interação detalhada entre agentes
vai ganhar aba própria.

Conferido em Chrome headless (2026-10-02): zero exceções e sem rolagem horizontal a 390 px.
