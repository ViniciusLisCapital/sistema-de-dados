# Log — ciclo <AAAA-MM-DD>

Escrito pela sessão que conduz o ciclo. Os reports de cada rodada e as consolidações (P1, P2) ficam vivos durante o ciclo; quando ele acaba, ficam o report final (RF) de cada agente e este log, que guarda o processo: o que cada um leu, o que mudou entre as rodadas e por quê.

## Informação nova desde o ciclo anterior

O que disparou o ciclo. Sem informação nova o cenário não muda, então toda mudança registrada abaixo aponta para um item desta lista ou para a leitura de outro agente neste ciclo.

| # | Informação (dado, divulgação, evento) | Data | Fonte · tabela |
|---|---|---|---|

## Agente web

Uma linha por execução do agente web (`.claude/agents/web.md`): antes da rodada 1, uma por agente atendido (`modo=pauta`); entre rodadas, uma por agente com pedidos (`modo=demanda`). Rodam uma de cada vez, porque todas escrevem o `noticias/INDICE.md`.

| Agente atendido | Modo · rodada | Arquivo | Notícias (A · B · C · desmentidas) | Itens sem notícia | Buscas (extended) |
|---|---|---|---|---|---|

## Rodadas

Rodada 1 → P1 → rodada 2 → P2 → report final → PF*. Dentro de uma rodada todos os agentes escrevem, sem ordem entre eles.

### Rodada <n> · <agente>

- **Leu:** <na rodada 1: dados, ferramentas, partes do mapa, as notícias; nenhum report nem JSON dos outros agentes> · <a partir da rodada 2: também os reports de todos da rodada anterior, o P<n−1> e as notícias dos pedidos>
- **Conhecimento aberto:** os arquivos do retrato (`conhecimento/<agente>/`) que o agente abriu nesta rodada — vão para a tabela "Conhecimento" abaixo
- **Notícias usadas:** vão para a tabela "Notícias usadas" abaixo
- **Faltou:** <tema> | nada — vai para a tabela "Faltou" abaixo; o que uma notícia responderia (marcado "(web)") vira pedido ao agente web antes da rodada seguinte
- **Escreveu:** report <n> | report final
- **Blocos** (só o externo): o que cada um dos três blocos (política dos EUA · risco e dólar · commodities) custou e achou nesta rodada. É o insumo para decidir se o externo vira dois agentes (SISTEMA_AGENTES.md III.III.vii)
- **Mudanças** (a partir da rodada 2):

| O que | Antes | Depois | Motivo | Provocado por |
|---|---|---|---|---|
| <premissa n · probabilidade · central · faixa> | | | | <item da informação nova · report de <agente> · P<n−1>> |

### Consolidação P<n>

- **Reports e caminhos usados:** <report e `caminhos/<agente>_<rodada>.json` de cada agente na rodada n; JSON que faltou>
- **Principal e subordinados:** <a aba "Exógenas" no dia; exógena cujo principal não escreveu caminho, que ficou no padrão do simulador>
- **O que o Modelo Estrutural devolveu:** <variáveis e trajetória> (`P<n>.md`)
- **Caminhos divergentes** (seção 3 do P): quem escreveu um caminho que não é o do principal (subordinado, com o caminho de referência, ou agente sem papel na exógena), em que exógena e quanto; na rodada seguinte, a resposta do principal a cada argumento (manteve · mudou, e por quê)
- **Central do modelo contra a faixa dos agentes:** <variável, agente, quando a central conjunta caiu fora da faixa do agente>

## Conhecimento

O que cada agente abriu do seu retrato do conhecimento (`conhecimento/<agente>/`, gerado no início do ciclo com o F(A)). É o que responde quanto da literatura uma análise de fato usa. **Outro dono** = o arquivo é da biblioteca de outro agente e entrou no retrato por uma página de conceito; o `INDICE.md` do retrato diz qual.

| Agente · rodada | Arquivo (caminho no retrato) | Tipo | Dono | Outro dono |
|---|---|---|---|---|

## Notícias usadas

O que cada agente usou das notícias do ciclo (`noticias/`). É o que responde quanto o agente web acrescenta, e quanto pesa cada nível.

| Agente · rodada | Id | Veículo · data | Nível | Onde entrou (afirmação, cenário, tempero, cauda, insumo ao principal) |
|---|---|---|---|---|

## Faltou

O que a análise precisou e o retrato não tinha. Cada linha fura a fila de promoção: o item vai para o topo do próximo lote do agente (PLANO_AGENTES.md I).

| Agente · rodada | Tema | Por que fez falta | O que resolveria (se o agente souber) |
|---|---|---|---|

## Funções G

Conta que o F(A) não faz. O código fica em `dados/G/`, lê os arquivos de `dados/A/` e nunca escreve no banco; o report e o relatório não citam o G, o rastro fica aqui. No fim do ciclo cada G fica como registro ou é promovido ao F.

| Agente · rodada | Arquivo | O que calcula | Resultado usado | Destino (registro · promover ao F) |
|---|---|---|---|---|

## Divergências abertas

Podem envolver mais de dois agentes: uma linha por agente com posição própria.

| Tema | Agente | Posição | Por que não se resolveu |
|---|---|---|---|

## Relatório

<data> · `relatorio.md` · números conferidos contra os RF e o PF\* (escrivão): sim | não · contra a fonte, no banco (sessão que conduz o ciclo, III.III.iii): sim | não
