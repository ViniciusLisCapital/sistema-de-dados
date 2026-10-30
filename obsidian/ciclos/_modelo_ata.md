# Ata da conversa · ciclo <AAAA-MM-DD>

Escrita pelo moderador (`.claude/agents/moderador.md`), em `obsidian/ciclos/<ciclo>/ata.md`. A conversa vem depois dos R1 finais e do P da abertura (`P1.md`), e termina quando todos os assuntos estão fechados; então o modelo roda com os caminhos fechados (`PF.md`) e cada agente atualiza o R1 (SISTEMA III.III.ii).

**O papel do moderador.** É o provocador e a central da lógica: questiona premissas, estressa cenários, leva as coisas ao limite para mapear os riscos, confronta cenários de áreas diferentes que não batem, e devolve todo argumento sem premissa sustentada. Pode recomendar o lado com mais fundamento, inclusive o do subordinado contra o principal. **Não decide:** a palavra final é do dono da premissa (o principal da exógena, o dono da equação no tempero, o dono da variável), em até duas voltas por assunto. **Não muda número:** quem muda é o dono, no próprio R1 e no arquivo de caminhos. Tudo fica aqui, literal, para que o moderador e os agentes possam ser avaliados.

## D1 e perguntas entre agentes

Antes da conversa, quando todos os R1 estão escritos, o moderador junta os pedidos ao agente web numa demanda (D1) e as perguntas entre agentes por destinatário. A sessão despacha o web e entrega a cada agente as notícias e as perguntas dirigidas a ele, que ele responde no R1 final.

| Pedido ao web | Agente(s) | Tese que depende dele |
|---|---|---|

| Para | Pergunta | De |
|---|---|---|

## Pauta

| # | Assunto | Tipo | Dono (decide) | Lados | Testemunhas | Pergunta que decide |
|---|---|---|---|---|---|---|
| 1 | <ex.: juro real de 10 anos no 1T27> | <divergência · cenários que não batem · stress do moderador · o que derrubaria a tese · pergunta sem resposta> | <fiscal (principal)> | <fiscal; PM> | <atividade: o hiato sente o juro?> | <o fiscal mantém o caminho diante do argumento da PM?> |

- **Tipo.** *Divergência*: dois agentes escreveram coisas diferentes sobre a mesma premissa. *Cenários que não batem*: ninguém declarou divergência, mas os cenários de duas áreas se contradizem (ex.: a fuga de risco do externo apreciando o real porque o CDS do fiscal ficava parado nela). *Stress do moderador*: um cenário que nenhum agente discutiu. *O que derrubaria a tese*: o teste dos itens da seção 2 de um R1 ("isso derrubaria mesmo?"). *Pergunta sem resposta*: uma pergunta do R1 que o R1 final não respondeu.
- **Testemunha** é outra área chamada para trazer evidência da própria área a favor ou contra um argumento ("os dados de atividade mostram que o que é sensível ao juro está sofrendo"). Não dá opinião sobre a premissa em discussão.
- **Fora da pauta**, com o motivo: o que o moderador olhou e não levou (ex.: diferença abaixo do que muda uma faixa).

**Revisão da pauta pelo usuário** (só no ciclo 2): <o que o usuário acrescentou ou cortou, literal | sem mudança>.

## Regras dadas a todos os agentes

Repetidas no começo de cada mensagem do moderador:

> Conversa do ciclo <AAAA-MM-DD>. Responda só aos assuntos abaixo. Não releia reports inteiros: abra só o trecho de que precisar, e pode rodar um G curto, inclusive o modelo. Cada resposta é premissa → conclusão: o dado ou a notícia que sustenta, e o que o mudaria. Se mudar um número de que é dono, atualize `caminhos/<seu_agente>_r1.json` e o seu R1 (a seção afetada e uma linha na seção 7, etapa "conversa") e diga o antes → depois. Formato: por assunto, "mantenho" ou "mudo", o porquê em até cinco linhas e o número novo, se houver; se precisar de notícia, "Pedido ao web:" e o que falta. No fim, uma linha "Abri:" com os arquivos que abriu.

## Volta <n>

<Uma frase: quais assuntos vão, a quem, e por quê nesta ordem. As mensagens de uma volta são independentes e vão juntas.>

### Mensagens do moderador

**Moderador → <agente>:**

> <mensagem literal: o assunto, o argumento do outro lado citado com a fonte (R1, seção), a provocação ou o stress, e a pergunta que decide>

### Rodadas do modelo pelo moderador

<Quando o moderador estressa um cenário com o modelo: o G (`dados/G/mod_<n>.py`), os caminhos que mudou, o resultado. É provocação, não premissa: entra na mensagem e só vira caminho se o dono adotar.>

### Respostas

**<agente> → moderador:**

> <resposta literal>

### Argumentos devolvidos

<Os argumentos que o moderador devolveu por falta de premissa sustentada ("porque sim"), com o trecho e o que faltava. "Nenhum" é resposta válida.>

## Pausa para o agente web · D<n>

<Os pedidos que os agentes fizeram nesta volta, juntos numa demanda: o pedido, o agente, o assunto da pauta que depende dele. A conversa para, o web roda (`noticias/demanda_d<n>.md`), e a volta seguinte começa com as notícias entregues a quem pediu.>

## Encerramento

| # | Assunto | Como fechou | Quem decidiu | O que muda nos caminhos |
|---|---|---|---|---|
| 1 | | **Resolvido.** <a posição final e o porquê, em duas linhas> \| **Divergência registrada.** <cada posição com o seu número, e o fato, número ou data que decidiria> | <o dono> | <`caminhos/fiscal_r1.json`: `rr_10a` antes → depois \| nada> |

Caminhos alterados pela conversa: <arquivos e exógenas>. Depois daqui, os caminhos não mudam mais neste ciclo; o PF\* roda com eles.

## Para o usuário

O que só o usuário resolve, sem parar a conversa: uma premissa sem dono, um dado que o sistema não tem, uma regra do sistema que a conversa pôs à prova. Uma linha por item, com o assunto da pauta. "Nada" é resposta válida.

## Custo

| Quem | Voltas | Contador antes → depois | Custo |
|---|---|---|---|
| moderador | | | |
| <agente> | | | |
| agente web (D<n>) | | | |
| **total** | | | |
