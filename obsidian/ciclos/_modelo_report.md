# Report — <área> · ciclo <AAAA-MM-DD> · rodada <1 | 2 | final>

Dados até: <data de corte> · Horizontes: os seis trimestres do Modelo Estrutural a partir do trimestre em curso (ex.: 4T26 a 1T28), com a variável no fechamento do trimestre

## 1. Tese

| Variável | Trimestre | Central | Base: faixa · P | Cauda worst: limite · P | Cauda best: limite · P | Pbc − Pwc |
|---|---|---|---|---|---|---|
| <ex.: USD/BRL, PTAX de fechamento> | 4T26 | <5,20> | <5,05 a 5,35 · 55%> | <acima de 5,35 · 25%> | <abaixo de 5,05 · 20%> | <−0,05> |
| | 1T27 | | | | | |
| | 2T27 | | | | | |
| | 3T27 | | | | | |
| | 4T27 | | | | | |
| | 1T28 | | | | | |

- Uma linha por trimestre. A variável é medida no fechamento do trimestre (no câmbio, a PTAX do último dia útil), porque é o que se compara com o dado de hoje.
- **A central é a do Modelo Estrutural no cenário base** (seção 3.1), sem ajuste. Faixa, limites das caudas e probabilidades são do agente (seção 3.2).
- As três probabilidades de cada linha somam 100%. Worst e best são as caudas abaixo e acima da faixa base, na direção que vale para a variável (inflação mais alta é worst; no câmbio, depreciação é worst).
- **O que leva a cada cauda**, uma linha para cada, dita nas duas etapas da seção 3: o cenário do modelo e o tempero ("acima de 5,35 se o 2º turno reverter o resultado: CDS a 150 dá 5,30 no modelo, e o efeito do CDS × 1,5 leva a 5,45").
- **A tese em uma frase:** o que se espera, em que trimestres e por qual mecanismo.

## 2. Argumentação

- **As perguntas centrais.** A resposta a cada pergunta central do mapa conceitual da área (no câmbio, Q1–Q4). É o mínimo, não o máximo: insights novos e alertas entram aqui também.
- **Por que a central.** Os caminhos das exógenas no cenário base e o que o modelo faz com eles: quais canais movem a variável, e quanto. A central não leva tempero; uma força qualitativa no cenário base entra na assimetria.
- **Por que a faixa e a probabilidade de cada cauda.** Os riscos que justificam a assimetria: o que levaria a variável para o worst-case e para o best-case, e por que um é mais provável que o outro, com os temperos da seção 3.2.

**Cada dado tem um papel.** Uma afirmação com partes é escrita em partes ("mercado fino" e "demanda fora do mercado à vista"), e cada dado diz a qual parte responde:
- **sustenta:** fica no parágrafo, ligado à afirmação por uma palavra que diga a relação ("o que mostra", "porque");
- **contraria ou enfraquece:** fica no mesmo parágrafo, logo depois, com "mas" ou "apesar de" e o que teria de acontecer para mudar a conclusão;
- **sem sinal neste ciclo:** vai para o bloco abaixo.

Dado sem ligação com uma afirmação é defeito: ou ganha a ligação, ou vai para o bloco.

**Olhado, sem sinal.** No fim da seção, uma linha por dado que o agente olhou e que não diz nada neste ciclo:
- <dado> · <valor (tabela · data)> · <por que não diz nada agora> · <o que o faria dizer algo>
- Ex.: "Estoque de swaps · −US$ 91,6 bi (`cmb_reservas_bc` · ago) · estável no mês · diria algo se o BC ampliasse a oferta acima dos vencimentos."

Todo número vem com valor · tabela · data. No report final, o número vem arredondado ao que a afirmação precisa: "~60 mil contratos (`cmb_cot_fx` · 22/09)". A tabela e a data bastam para conferir o valor exato.

**Notas para o leitor**, como nota de rodapé (`[^1]`), em todo report. O leitor do relatório final não conhece o sistema nem a literatura:
- o que um percentil quer dizer, na primeira aparição ("quanto maior, maior a liquidez em relação ao histórico"), e de novo quando o sentido for menos óbvio;
- o arcabouço citado, em uma ou duas frases ("posicionamento como sinal contrário: quando os fundos já estão muito comprados, sobra pouco comprador novo");
- um conceito pouco conhecido, com um exemplo simples;
- o comentário sobre o próprio processo ("não há dado eleitoral nesta análise"), que sai do texto principal.

## 3. Premissas

Duas etapas, nesta ordem. A etapa 1 dá a central; a etapa 2 dá a distribuição em torno dela. Um evento (eleição, decisão de política, choque) não é premissa: é o motivo de um cenário na etapa 1 ou de um tempero na etapa 2.

### 3.1 Etapa 1 — o modelo

**Cenários.** Uma linha por cenário com a história que o define, em eventos:
- Base: <ex.: o 2º turno confirma a leitura de 05/10; o plano fiscal de 2027 estabiliza a dívida devagar>
- Worst: <ex.: o 2º turno reverte a leitura de 05/10>
- Best: <...>

**Caminhos das exógenas.** Só as exógenas do Modelo Estrutural que a área usa, uma por linha, sem agrupar. As endógenas (hiato, inflação, expectativas, Selic, câmbio) o modelo resolve, e o agente não as fixa. As exógenas que a área não usa ficam no padrão do simulador.

| Exógena | Hoje (valor · tabela · data) | Cenário | 4T26 | 1T27 | 2T27 | 3T27 | 4T27 | 1T28 |
|---|---|---|---|---|---|---|---|---|
| <CDS 5 anos> | <112 · `cmb_risco_pais` · 08/09> | base | | | | | | |
| | | worst | | | | | | |
| | | best | | | | | | |

Um caminho que não seja óbvio pela história do cenário ganha uma linha de motivo abaixo da tabela.

**Acompanhamento das exógenas.**

| Exógena | Tipo · status | Alerta | Checkpoints |
|---|---|---|---|
| <CDS 5 anos> | <exógeno · assumida> | <CDS 5 anos · variação · +25 p.b. · 10 sessões> | <2º turno · 25/10> |

**Saída do modelo.** A variável da área e as endógenas que a argumentação usa, por cenário. A linha base da variável é a central da seção 1.

| Variável | Cenário | 4T26 | 1T27 | 2T27 | 3T27 | 4T27 | 1T28 |
|---|---|---|---|---|---|---|---|
| <PTAX> | base · worst · best | | | | | | |
| <Selic, IPCA 12m> | base · worst · best | | | | | | |

### 3.2 Etapa 2 — o tempero qualitativo

O que o agente acrescenta ao modelo para formar a distribuição. Uma ficha por tempero, de dois tipos. Um canal que está no modelo só entra pelo tipo (i): pelo (ii) ele seria contado duas vezes.

**(i) <Exógena> — efeito mais forte | mais fraco que o estimado** · cenário <base | worst | best>
- Coeficiente: estimado <β>, intervalo de 90% do posterior <a> a <b>. Multiplicador: × <m>, <dentro | fora> do intervalo.
- Efeito: <a variável no cenário, do modelo → com o multiplicador, nos trimestres afetados>.
- Por quê: <X1>; <X2>; … Quanto mais para a cauda da distribuição do coeficiente, melhor tem de ser a justificativa. Fora do intervalo, o agente afirma que o histórico subestima o canal, e diz por que agora é diferente (ex.: o modelo é linear e o estresse não é).
- Onde entra: <limite da cauda | probabilidade | assimetria do cenário base>.
- Alerta: <indicador> · <tipo> · <limiar> · <janela>
- Checkpoints: <evento · data>

**(ii) <Fator fora do modelo> — <indicador>** · cenário <base | worst | best>
- Hoje: <valor> (<tabela>, <data>)
- Por que o modelo não vê: <o fator, e por que ele não está em nenhuma exógena>.
- Efeito: <direção · tamanho · duração> (ex.: "+2% sobre o modelo por um trimestre").
- Onde entra: <limite da cauda | probabilidade | assimetria do cenário base>.
- Alerta: <indicador> · <tipo> · <limiar> · <janela>
- Checkpoints: <evento · data>

Um tempero no cenário base não move a central: entra como assimetria (Pbc − Pwc).

### 3.3 Da etapa 1 à tese

| Trimestre | Central (modelo, base) | Worst: modelo → com tempero | Best: modelo → com tempero |
|---|---|---|---|
| 4T26 | | | |

Abaixo da tabela, em uma ou duas frases: como esses pontos dão a faixa base, os limites das caudas e as probabilidades da seção 1.

### Campos

- **Tipo:** endógeno · endógeno de <agente> · TWA · exógeno.
- **Status:** próprio · aguarda <agente> (qual saída) · assumida (TWA ou exógeno: a premissa é declarada aqui).
- **Alerta**, sempre na mesma forma, para a matriz de acompanhamento conseguir ler. O tipo é um destes três:
  - patamar: "CDS 5 anos · patamar · acima de 150 · —";
  - variação numa janela: "DI 5 anos · variação · +50 p.b. · 10 sessões";
  - conjunto: dois ou mais alertas ligados por "e", quando só juntos indicam mudança ("DI 5 anos · variação · +50 p.b. · 10 sessões **e** PTAX contra os pares · variação · +2% · 10 sessões").

## 4. Para os outros agentes

- **Respostas às entradas fixas** do mapa conceitual (no câmbio, E1–E7 para política monetária): uma linha cada. Quando a condição de alerta do mapa aconteceu, o item vem marcado **em destaque**, com o motivo e o argumento ("E7, em destaque: o BC vendeu US$ 3 bi à vista em setembro").
- **Pedidos:** as saídas fixas do mapa (no câmbio, S1–S4) e os pedidos deste ciclo, com a pergunta exata e a tese que depende dela.

## 5. Placar

Os trimestres que fecharam desde o último ciclo.

| Variável | Trimestre | Central e faixas do último report antes do fechamento | Realizado (fechamento) | Caiu em | Leitura |
|---|---|---|---|---|---|

Em que faixa a variável caiu, e o que isso diz da tese e das premissas: mantidas, revistas ou derrubadas, e por quê.
