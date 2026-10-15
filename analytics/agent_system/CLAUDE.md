# analytics/agent_system/ — diagrama do sistema de agentes e o F(A)

Gera `team_materials/structure_materials/Sistema de Agentes.html`: um diagrama SVG da visão geral
— processos de entrada, as três fontes do agente (MySQL, ferramentas, conhecimento), cada uma
apontando para cada agente, e o ciclo dos agentes (rodada 1 → P1 → rodada 2 → P2 → report final →
PF*), no desenho do usuário de 2026-10-07. Não está no manifesto de dashboards.

```
uv run python -m analytics.agent_system.generate_report
```

- **À mão, no `report.html`:** caixas, setas e o estado de cada bloco (existe / em construção /
  planejado), em `SPECS.geral` e `rodadasGeral()`; a lista `FERRAMENTAS`; o texto de cada detalhe.
- **Lido na geração:** contagens do registry, dos connectors e das notas do vault por área; a lista
  de dados do câmbio, da seção V.I do `SISTEMA_AGENTES.md` (com a fonte de cada tabela pelo
  registry).

## Guia expansível

O diagrama é um guia expansível (pedido do usuário, 2026-10-07): seta ou caixa com entrada em
`DETALHES` ganha o selo "+" e abre uma caixa (`<dialog>`) com o "under the hood". Para acrescentar
um detalhe: uma entrada em `DETALHES` (chave `<fonte>><agente>` para as setas do leque, ou `det` na
caixa) e a função que monta o HTML. Ir aos poucos, sem encher de conteúdo.

Hoje: **MySQL → Câmbio** (como os dados chegam e as tabelas da lista, lidas da V.I do
`SISTEMA_AGENTES.md`), **Ferramentas** e **Câmbio · report 1** (as perguntas centrais, lidas da Parte 1
do mapa conceitual). O tratamento de cada tabela (as métricas do F) não entra na caixa: é do sistema,
não do usuário (2026-10-07). Tabela da lista fora do registry vira aviso na página.

Conferido em Chrome headless (2026-10-07): zero exceções, as três caixas abrem, sem rolagem
horizontal a 390 px.

## dados/ — o retrato de dados do ciclo (A → F(A))

```
uv run python -m analytics.agent_system.dados cambio [--ciclo AAAA-MM-DD] [--refazer]
```

Grava em `obsidian/ciclos/<data>/dados/`: `A/` (cada tabela da lista do agente, um `.csv.gz`, mais
`_manifesto.json` com a consulta; fora do git), `F_<agente>.md` (o que o agente lê) e `G/` (vazia,
para as funções G do agente). Regras de SISTEMA_AGENTES.md IV.iv.

- `motor.py`: igual para todo agente. Lê a lista da seção V, **levanta se a declaração do agente
  divergir dela**, extrai A uma vez por ciclo (compartilhado entre agentes) e calcula F **a partir
  dos arquivos de A**, nunca do banco. Leituras: `pct`, `dif`, `fluxo`, `media`, `var_mensal`; o
  grupo "Endógeno" ganha a leitura completa (percentis, mín–máx de 10 anos).
- `especiais.py`: F próprio de curva DI (prazos redondos e Selic precificada por reunião, com o
  `caminho_di` do relatório de política monetária), Focus, calendário, decisões e projeções do Copom.
- `cambio.py`: as tabelas do câmbio, as séries e a leitura de cada uma, e as leituras combinadas
  (o real e os pares: variação, volatilidade, carry). Agente novo = um arquivo destes e uma linha em
  `AGENTES` no `__main__.py`.
- O F(A) é fixo no ciclo: rodar de novo para a mesma data para; `--refazer` reextrai.
- `Tabela.fora` tira da conta uma tabela da lista com defeito conhecido (hoje nenhuma; a
  `cmb_fluxo_cambial` saiu da lista em 2026-10-07); `Tabela.nota` imprime um defeito conhecido no F (hoje nenhuma: a
  do PEN da `cmb_fx_latam` saiu em 2026-10-07, quando a tabela trocou o Yahoo pelo BIS).

O diagrama lê a lista pelo mesmo `motor.ler_lista()`.

## modelo.py — o Modelo Estrutural para os G (SISTEMA_AGENTES.md IV.vi)

```
uv run python -m analytics.agent_system.modelo --ciclo AAAA-MM-DD [--refazer]
```

A função fixa que o G do agente chama para rodar o simulador do Modelo Estrutural, sem
reestimar: `carregar(ciclo)`, `listar(sim)`, `rodar(sim, caminhos, mult)`, `texto(res)`. Uso e
regras na docstring do módulo.

- **Retrato por ciclo:** `dados/A/modelo_estrutural.json` (fora do git, ~0,6 MB), o payload de
  `simulator.construir()` com os pesos de hoje. O `dados` o grava junto com o A; o comando acima
  serve para um ciclo que já tem A. Monta do banco na hora em que roda (~40 s), então é para o
  início do ciclo, como o A.
- **A conta é `simulator.resolver()`**, não uma cópia. `carregar()` levanta se o retrato não
  reproduzir o `sistema_padrao` do payload.
- **Faixa:** a de `_simFaixasSistema` da página (desenho s de cada equação junto, quantis de
  caudas iguais a 90%), só incerteza dos pesos. Conferida contra o JS no mesmo payload em
  2026-10-15: 3e-9 no pior quantil. O teste não pega uma troca de `ceil` por `floor` no quantil
  (mutante verificado); só essa paridade pegaria.
- **Multiplicador:** `"<equação>.<coeficiente>"`, aplicado à mediana e a cada desenho. As
  restrições continuam valendo (na (E) o peso da meta é `1 − e1 − e2`, na (R) `1 − t1 − t2`),
  então multiplicar uma inércia move o peso que sobra. `sigma` e as marcas de crise não aceitam.
- **A partida é o último trimestre com dado** (decisão do usuário, 2026-10-15: trimestre que
  já fechou não se projeta). Os 12 trimestres seguintes saem projetados; o último com dado sai
  como "observado". Exógena sem o dado dele fica no último valor e aparece como segurada (hoje
  a vol implícita, que vem de planilha). Retrato gravado antes dessa regra levanta.

Teste: `uv run python tests/test_modelo_agentes.py` (lê o payload do relatório entregue, não o
banco; ~1 min).
