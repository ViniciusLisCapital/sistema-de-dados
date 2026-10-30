# Log — ciclo <AAAA-MM-DD>

Escrito pela sessão que conduz o ciclo. Ficam no fim do ciclo o R1 de cada agente (na versão atualizada), a ata da conversa, o P da abertura, o PF\*, o relatório e este log, que guarda o processo: o que cada um leu, o que mudou em cada etapa e por quê, e quanto custou.

O fluxo (SISTEMA III.III.ii, decidido em 2026-10-30):

1. R1 de cada agente, a partir do relatório e do próprio R1 do ciclo anterior, com o D1 (pedidos ao agente web) e as perguntas aos outros agentes.
2. O moderador junta os pedidos ao agente web numa demanda (D1) e as perguntas entre agentes por destinatário (`ata.md`); o agente web responde à D1.
3. R1 final: cada agente recebe as notícias e as perguntas que lhe fizeram, e responde.
4. P da abertura (`P1`): o modelo com os caminhos base do R1 final.
5. Conversa moderada (`ata.md`), com pausas para o agente web (D2, D3…).
6. PF\*: o modelo com os caminhos que a conversa fechou.
7. Atualização do R1 depois da conversa.
8. Relatório do escrivão.

## Informação nova desde o ciclo anterior

O que disparou o ciclo. Sem informação nova o cenário não muda, então toda mudança registrada abaixo aponta para um item desta lista, para uma notícia ou para um assunto da ata.

| # | Informação (dado, divulgação, evento) | Data | Fonte · tabela |
|---|---|---|---|

## Agente web

Uma linha por demanda: D1 depois dos R1, e uma por pausa da conversa. Rodam uma de cada vez, porque todas escrevem o `noticias/INDICE.md`.

| Demanda | Etapa | Arquivo | Pedidos (agentes · itens) | Notícias (A · B · C · desmentidas) | Itens sem notícia | Buscas (extended) | Custo |
|---|---|---|---|---|---|---|---|

## R1

### R1 · <agente>

- **Tipo:** atualização | completo (primeiro R1 do agente)
- **Papel:** principal de <exógenas>; subordinado de <exógenas>
- **Leu:** o relatório e o próprio R1 do ciclo <AAAA-MM-DD>; os dados, partes do mapa, o retrato do conhecimento
- **Conhecimento aberto:** vai para a tabela "Conhecimento" abaixo
- **Faltou:** <tema> | nada — vai para a tabela "Faltou"; o que uma notícia responderia virou pedido do D1
- **Escreveu:** `<agente>_r1.md`, `caminhos/<agente>_r1.json` · custo <tokens>
- **Blocos** (só o externo): o que cada um dos três blocos (política dos EUA · risco e dólar · commodities) custou e achou. É o insumo para decidir se o externo vira dois agentes (SISTEMA III.III.vii)

### Ruído (só no ciclo 2: câmbio e política monetária, R1 rodado duas vezes)

O segundo R1 de cada um, escrito por um agente novo com as mesmas entradas, fica em `<agente>_r1b.md` e não entra no fluxo. A comparação:

| Agente | Variável · trimestre | R1: central · faixa · P(up/base/down) | R1b: central · faixa · P(up/base/down) | Caminhos que diferem | Leitura |
|---|---|---|---|---|---|

## R1 final

Por agente, o que as notícias e as perguntas dos outros mudaram (a tabela da seção 7 do R1, etapa "R1 final"). "Nada mudou" é registro válido.

| Agente | O que | Antes | Depois | Motivo | Provocado por |
|---|---|---|---|---|---|

Custo por agente: <agente · tokens>.

## P da abertura

- **Caminhos usados:** <`caminhos/<agente>_r1.json` de cada agente no R1 final; JSON que faltou>
- **Principal e subordinados:** <a aba "Exógenas" no dia; exógena cujo principal não escreveu caminho, que ficou no padrão do simulador>
- **O que o Modelo Estrutural devolveu:** <variáveis e trajetória> (`P1.md`)
- **Caminhos divergentes** (seção 3 do P): quem escreveu um caminho que não é o do principal, em que exógena e quanto
- **Central do modelo contra a faixa dos agentes:** <variável, agente, quando a central caiu fora da faixa do agente>

## Conversa

- **Pauta:** <n assuntos por tipo: divergências · cenários que não batem · stress · o que derrubaria a tese · perguntas sem resposta>; revisão do usuário: <o que mudou | sem mudança | não houve (só no ciclo 2)>
- **Voltas:** <n>; pausas para o web: <D2… | nenhuma>
- **Como fechou:** <n resolvidos · n divergências registradas · n argumentos devolvidos>; detalhe e mensagens literais em `ata.md`
- **Caminhos alterados:** <arquivo · exógena · antes → depois | nenhum>
- **Rodadas do modelo:** do moderador, <n> (`dados/G/mod_*.py`); dos agentes, na tabela "Funções G"
- **Para o usuário:** <n itens | nada>
- **Custo:** moderador <tokens>; agentes <tokens> (soma das réplicas); web <tokens>

## PF\*

- **Caminhos usados:** os que a conversa fechou
- **O que o Modelo Estrutural devolveu:** <variáveis e trajetória> (`PF.md`); contra o P da abertura: <o que mudou e por qual assunto da ata>

## Atualização depois da conversa

Por agente, o que a conversa mudou (a tabela da seção 7 do R1, etapa "conversa"). Caminhos não mudam aqui.

| Agente | O que | Antes | Depois | Assunto da ata |
|---|---|---|---|---|

Custo por agente: <agente · tokens>.

## Conhecimento

O que cada agente abriu do seu retrato do conhecimento (`conhecimento/<agente>/`, gerado no início do ciclo com o F(A)). É o que responde quanto da literatura uma análise de fato usa. **Outro dono** = o arquivo é da biblioteca de outro agente e entrou no retrato por uma página de conceito; o `INDICE.md` do retrato diz qual.

| Agente · etapa | Arquivo (caminho no retrato) | Tipo | Dono | Outro dono |
|---|---|---|---|---|

## Notícias usadas

O que cada agente usou das notícias do ciclo (`noticias/`). É o que responde quanto o agente web acrescenta, e quanto pesa cada nível.

| Agente · etapa | Id | Veículo · data | Nível | Onde entrou (afirmação, cenário, tempero, cauda, insumo ao principal, assunto da ata) |
|---|---|---|---|---|

## Faltou

O que a análise precisou e o retrato não tinha. Cada linha fura a fila de promoção: o item vai para o topo do próximo lote do agente (PLANO_AGENTES.md I).

| Agente · etapa | Tema | Por que fez falta | O que resolveria (se o agente souber) |
|---|---|---|---|

## Funções G

Conta que o F(A) não faz. O código fica em `dados/G/`, lê os arquivos de `dados/A/` e nunca escreve no banco; o R1 e o relatório não citam o G, o rastro fica aqui. Inclui as rodadas do modelo dos agentes e do moderador durante a conversa. No fim do ciclo cada G fica como registro ou é promovido ao F.

| Agente · etapa | Arquivo | O que calcula | Resultado usado | Destino (registro · promover ao F) |
|---|---|---|---|---|

## Divergências registradas

As que a conversa não resolveu (seção "Encerramento" da ata). Uma linha por agente com posição própria.

| Tema | Agente | Posição | O que decidiria |
|---|---|---|---|

## Custo do ciclo

Teto do ciclo 2: 10M. Ao chegar a ele, a sessão para e pergunta ao usuário.

| Etapa | Tokens |
|---|---|
| R1 (nove agentes) | |
| Ruído (R1b, ciclo 2) | |
| Agente web (todas as demandas) | |
| R1 final | |
| Conversa (moderador e agentes) | |
| Atualização | |
| Escrivão | |
| **Total** | |

## Relatório

<data> · `relatorio.md` · números conferidos contra os R1 e o PF\* (escrivão): sim | não · contra a fonte, no banco (sessão que conduz o ciclo, III.III.iii): sim | não
