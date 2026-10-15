# Log — ciclo <AAAA-MM-DD>

Escrito pela sessão que conduz o ciclo. Os reports de cada rodada e as consolidações (P1, P2) ficam vivos durante o ciclo; quando ele acaba, ficam o report final (RF) de cada agente e este log, que guarda o processo: o que cada um leu, o que mudou entre as rodadas e por quê.

## Informação nova desde o ciclo anterior

O que disparou o ciclo. Sem informação nova o cenário não muda, então toda mudança registrada abaixo aponta para um item desta lista ou para a leitura de outro agente neste ciclo.

| # | Informação (dado, divulgação, evento) | Data | Fonte · tabela |
|---|---|---|---|

## Rodadas

Rodada 1 → P1 → rodada 2 → P2 → report final → PF*. Dentro de uma rodada todos os agentes escrevem, sem ordem entre eles.

### Rodada <n> · <agente>

- **Leu:** <na rodada 1: dados, ferramentas, vault> · <a partir da rodada 2: os reports de todos da rodada anterior e o P<n−1>>
- **Escreveu:** report <n> | report final
- **Mudanças** (a partir da rodada 2):

| O que | Antes | Depois | Motivo | Provocado por |
|---|---|---|---|---|
| <premissa n · probabilidade · central · faixa> | | | | <item da informação nova · report de <agente> · P<n−1>> |

### Consolidação P<n>

- **Reports usados:** <report de cada agente na rodada n>
- **O que o Modelo Estrutural devolveu:** <variáveis e trajetória>
- **Onde divergiu dos agentes:** <variável, agente, tamanho da diferença>

## Funções G

Conta que o F(A) não faz. O código fica em `dados/G/`, lê os arquivos de `dados/A/` e nunca escreve no banco; o report e o relatório não citam o G, o rastro fica aqui. No fim do ciclo cada G fica como registro ou é promovido ao F.

| Agente · rodada | Arquivo | O que calcula | Resultado usado | Destino (registro · promover ao F) |
|---|---|---|---|---|

## Divergências abertas

| Tema | Posição de <agente A> | Posição de <agente B> | Por que não se resolveu |
|---|---|---|---|

## Relatório

<data> · `relatorio.md` · números conferidos contra a fonte: sim | não
