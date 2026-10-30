# Decisões pendentes do Modelo Estrutural · preparadas em 2026-10-30

Adiadas pelo usuário, para antes do ciclo 2. Nada aqui foi rodado além dos dois testes do PDF
(`experimentos/Testes do Modelo Estrutural - ancora e hiato.pdf`) e do que os `pendencias_*_eq.md` já mediram.

Formato pedido pelo usuário: a pergunta numa frase; o impacto prático de cada opção (Selic, inflação, câmbio do
modelo, trabalho dos agentes, custo); a recomendação em uma linha; um exemplo real.

Duas convenções:
- **"conta"** quer dizer uma aproximação feita a partir de elasticidades já medidas do modelo, sem rodar o modelo. O número sem essa marca foi medido.
- **Custo de pôr no modelo** uma mudança aprovada: reestimar a equação, ajustar o simulador e a ferramenta dos agentes, testes e painel. A estimativa, por precedente, é de **~150–250 mil tokens por equação mexida**. Não há medidor.

Três lotes de até quatro decisões. O lote 1 vem primeiro: A e C mexem nas mesmas duas equações. O item 10 (lote 3) entra na mesma reestimação do câmbio que os itens 5 e 14.

---

## Lote 1 — os dois testes do PDF

### A. Âncora da Selic

**Pergunta.** A Selic de equilíbrio do modelo deve seguir o juro real de 10 anos do trimestre, ou a média do último ano?

- **Média do último ano (recomendada).**
    - Selic: cerca de 0,2 p.p. mais baixa no fim do horizonte, porque a média de hoje está em 10,63 contra 10,84 (conta).
    - Previsão da Selic: 23% menos erro no 1º trimestre e 6% menos em um ano (medido).
    - Salto da NTN-B: entra na Selic aos poucos, um quarto por trimestre.
    - Inflação: não muda.
    - Câmbio: ~+0,1%, pelo juro um pouco menor (conta).
    - Hiato: praticamente igual.
    - Agentes: a revisão que o fiscal fizer no caminho do juro longo passa à Selic em quatro trimestres, e não de uma vez.
    - Custo: duas equações, ~300–500 mil.
- **Manter o juro do trimestre.**
    - Nada muda e não custa nada.
    - Um pregão de estresse continua indo inteiro para a Selic no trimestre.
- **Por que a média:** prevê melhor a Selic, não piora o hiato e tira do modelo a reação a um pregão.
- **Ressalva:** o fiscal é contra suavizar, porque esconde o prêmio de risco em vez de separá-lo. Só o item C separa.
- **Exemplo.** Em 26/10 a NTN-B de 10 anos saltou 135 p.b. e pôs 0,76–1,00 p.p. na Selic de fechamento do modelo, com o hiato igual (ata do ciclo, item 5). Com a média, só cerca de um quarto disso entraria no trimestre.

### B. Hiato de partida

**Pergunta.** Para dizer quanto a economia está aquecida hoje, ficamos com o número do BC (+0,4) ou com o que a capacidade instalada e o desemprego já observados indicam (+1,5)?

- **Refazer o teste com uma taxa de desemprego de equilíbrio que anda no tempo, antes de decidir (recomendada).**
    - Nada muda no modelo até o resultado.
    - Custo: ~100 mil.
    - Se a taxa de equilíbrio caiu, o hiato da regressão se aproxima do BC. Se não caiu, a leitura de economia mais aquecida ganha força.
- **Usar a regressão como cenário de hiato alto para os agentes.**
    - A central não muda. Atividade, inflação e PM ganham um cenário medido, com hiato ~1 p.p. acima.
    - Nesse cenário, o IPCA de 12 meses fica ~+0,2 p.p. no primeiro ano, a Selic menos de +0,2 p.p. e o câmbio ~+0,2% (conta).
    - Custo: ~50–100 mil.
- **Manter o hiato do BC.**
    - Nada muda e não custa nada.
    - Fica o problema conhecido: a primeira publicação erra e é revista depois.
- **Por que refazer:** a diferença de ~1 p.p. vem toda de um desemprego (5,4%) abaixo do menor valor usado na estimação (6,67%). Adotar agora poria no modelo uma premissa não testada.
- **Agentes:** se alguma versão entrar, a tese do mercado de trabalho sobre o desemprego de equilíbrio passa a mover o ponto de partida do hiato.
- **Exemplo.** Do 4T22 ao 3T23, o BC errou o sinal do hiato nas primeiras publicações em 12 de 12 casos; a regressão acertou 8 ou 9. Hoje, no 3T26: BC +0,41, regressão +1,45.

### C. Juro neutro separado do prêmio de risco

**Pergunta.** Construímos agora um juro neutro tirado das expectativas da Focus, separado do prêmio de risco do juro longo, ou depois de fechar A e B?

- **Depois de A e B (recomendada).**
    - Nada muda agora.
    - Custo: ~250 mil para o teste, mais a implementação se ele passar.
- **Agora.** Se o teste passar:
    - Selic: deixa de seguir o juro longo e devolve parte dos 0,76–1,00 p.p. que o prêmio de 26/10 pôs nela.
    - Hiato: um salto do prêmio passa a apertar o hiato, e os cenários fiscais passam a diferir no hiato, não só na Selic.
    - Câmbio: o cenário de risco fiscal deixa de apreciar o real só porque a Selic do modelo subiu.
    - Agentes: alguém passa a escrever o caminho do neutro (perto das expectativas) e alguém o do prêmio (o fiscal). Essa divisão é decisão sua.
    - Custo: ~250 mil de teste, mais ~300–500 mil se entrar.
- **Por que depois:** o neutro muda de novo as duas equações que A mexe.
- **A e C juntos:** se C for feito antes do ciclo 2, implementar A primeiro reestima as mesmas equações duas vezes. Nesse caso A vira só a coluna de comparação.
- **Exemplo.** Em 26/10 só 22 dos 135 p.b. de alta vieram dos dois primeiros anos da curva real. O modelo subiu a Selic e apreciou o real no cenário de risco fiscal, e o câmbio teve de rodar à mão um segundo cenário para representar a dominância fiscal.

---

## Lote 2 — o seguinte do quadro (itens 4 a 7)

### 4. Faixa de incerteza

**Pergunta.** A faixa que o modelo entrega aos agentes deve incluir o erro típico das equações, e não só a incerteza dos pesos?

- **Incluir, numa segunda faixa só para os agentes, com o painel intacto (recomendada).**
    - A central não muda.
    - As faixas ficam mais largas, conferidas num teste de quantas vezes o realizado caiu dentro delas desde 2012.
    - Agentes: as caudas passam a ter uma dispersão medida, em vez de pontos escolhidos à mão.
    - Custo: ~50–100 mil.
- **Manter.**
    - Nada muda.
    - As caudas continuam sendo escolhidas à mão.
- **Por que incluir:** custa pouco, não mexe em nenhuma equação, e a faixa atual não serviu de distribuição a nenhum agente.
- **Exemplo.** No ciclo, a faixa da Selic no 4T26 ia de 13,12 a 13,75 e não continha nenhuma alta, com a curva precificando alta. A do câmbio ia de 5,34 a 5,52, contra um erro típico da equação de ~3,6% por trimestre.

### 5. O real enfraquece no fim do ano?

**Pergunta.** O modelo deve prever que o real costuma enfraquecer no quarto trimestre?

- **Testar, e adotar se passar (recomendada).** Se passar:
    - Câmbio: o dólar central do 4T sobe ~2%, com devolução parcial no 1T se o teste mostrar.
    - Inflação: ~+0,07 p.p. no IPCA (conta).
    - Selic: praticamente nada.
    - Agentes: o câmbio deixa de ajustar o 4T à mão.
    - Custo: ~80 mil, na mesma reestimação do item 14 (o diferencial de inflação com o núcleo americano).
- **Não testar.**
    - Nada muda.
    - O ajuste do fim do ano continua sendo feito à mão.
- **Por que testar:** o padrão é forte e o teste é barato. Mas são só 9 anos, e por isso ele precisa passar fora da amostra.
- **Exemplo.** Desde 2017 o modelo subestimou a alta do dólar no 4T em 8 de 9 anos, em +2,1% em média.

### 6. Fonte da volatilidade do dólar

**Pergunta.** A volatilidade do dólar no modelo deve vir da B3, que já está no banco e se atualiza sozinha, em vez da planilha da Bloomberg, parada em agosto?

- **Trocar para a B3 (recomendada).**
    - Na história, o número quase não muda: diferença média de −0,19 p.p. e correlação 0,978 com a planilha.
    - Na projeção, entra a volatilidade de hoje, e não a do 2T26 repetida.
    - O efeito na central do câmbio depende da volatilidade atual, que não li.
    - Custo: ~50 mil.
- **Manter a planilha.**
    - A volatilidade segue parada em 12,19 até alguém atualizar à mão.
- **Por que trocar:** é o mesmo dado, só que atualizado, e encerra um insumo mantido fora do banco.
- **Exemplo.** Neste ciclo a volatilidade foi o canal que mais moveu o câmbio do 4T26, e entrou parada no valor de abril a junho.

### 7. Âncora da expectativa de inflação

**Pergunta.** A expectativa de inflação do modelo volta para a meta mais depressa do que a Focus tem voltado. Testamos uma âncora mais fraca?

- **Testar três formas de uma vez e adotar a que passar (recomendada).** As formas:
    - peso da meta que muda com o tempo (ou com quebra em 2017);
    - ancorar na Focus de longo prazo, hoje em 3,50, em vez da meta;
    - pesos sem a soma igual a um.

  Se uma passar:
    - Focus: a central sobe +0,16 a +0,33 p.p.
    - Inflação: +0,1 a +0,2 p.p. entre o 3T27 e o 1T28.
    - Selic: +0,3 a +0,7 p.p. no fim do horizonte (conta).
    - Câmbio: efeito pequeno e de sinal incerto, porque o juro mais alto e a inflação mais alta se compensam em parte (não medido).
    - Agentes: as expectativas deixam de multiplicar a inércia por 1,2 à mão. Com a Focus de longo prazo como âncora, passam a escrever o caminho dela a cada ciclo.
    - Custo: ~100 mil de teste, mais ~150–250 mil se entrar.
- **Manter.**
    - Nada muda.
    - O ajuste à mão continua, e com ele a negociação com a PM.
- **Por que testar:** o erro tem um sinal só há dois anos, e o ajuste à mão mexe na peça errada (a inércia, não a âncora).
- **Exemplo.** Desde o 4T24 a expectativa do modelo ficou abaixo da Focus em 7 de 8 trimestres, em +0,35 p.p. em média. No ciclo, o ajuste à mão custou uma negociação com a PM (ata, item 8).

---

## Lote 3 — pedido do usuário depois do adiamento

### 10. O papel da bolsa americana (S&P 500) na equação do câmbio

**Pergunta.** A bolsa americana deve continuar na equação do câmbio como está hoje, em que ela sobe e o real enfraquece quando o resto fica parado?

**O que a equação diz hoje (medido)**
- **Sinal.** Com o risco Brasil e o dólar contra emergentes parados, 1% de alta do S&P no trimestre enfraquece o real em 0,23%. O coeficiente é positivo e firme: t 3,6, com 90% de chance entre 0,98 e 2,79 na escala da equação.
- **O sinal se inverte.** Sozinha, a bolsa subindo vem com o real mais forte (correlação −0,44), porque bolsa em alta é apetite a risco, e apetite a risco derruba o CDS e enfraquece o dólar contra emergentes. Segurados esses dois, o que sobra da bolsa age no sentido oposto. Lê-se como competição por capital, com o dinheiro indo para ativo americano. É o único dos cinco canais em que o sinal se inverte, e o modelo mensal do FX Report tem o mesmo padrão.
- **Tamanho.** É o maior contribuinte isolado da desvalorização desde 2006: +39,9 p.p. de +86,8, ou 46%. Esse número é condicional ao CDS e ao dólar contra emergentes: não é uma causa independente.
- **Estabilidade.** No mensal, quando foi incluída, o coeficiente ficou positivo e estável nas 163 janelas, e a bolsa reduziu o erro de previsão em ~4%. No trimestral nunca foi testada por subperíodo.
- **Risco global ou crescimento americano.** Pela forma, a parte que fica na equação é a de crescimento americano e atração de capital. A de apetite a risco já passa pelo CDS e pelo dólar contra emergentes.
- **Outra medida de apetite a risco.** O VIX e o juro real de 10 anos americano foram testados no mensal, junto com a bolsa, e não melhoraram a previsão. Não estão no banco.

**Correção ao ponto de partida.** A alta do S&P não aprecia o real pela equação: ela o enfraquece. No cenário de apetite a risco, o real só se aprecia se o externo também escrever o dólar mais fraco contra emergentes. O resultado líquido depende dos tamanhos que ele der aos dois caminhos.

**O que os sete disseram**
- **Câmbio.** O S&P "entra com sinal contrário ao mecanismo do mapa": somou +0,12 ao dólar do 1T28. Ele aplicou × 0,55 à mão, e o assunto foi para a moderação. Propõe reestimar sem o dólar contra emergentes, ou com o S&P limpo dos outros dois canais.
- **Externo.** O S&P do cenário base sobe ~11% em seis trimestres, por lucro e não por apetite a risco, e vira o maior canal externo do dólar: +0,13 no 1T28. Diz que foi o maior custo de negociação do ciclo. Propõe o S&P limpo do dólar contra emergentes, ou o S&P só nos trimestres de crise. Apoia o teste.
- **Fiscal.** Apoia o teste, pela parte do dólar contra emergentes, que contém o próprio real e inflou o componente global do CDS que ele usou.
- **PM, inflação, expectativas e atividade** não falaram do S&P.

**Opções**
- **Testar numa reestimação só (recomendada).** Ela mede: o S&P limpo dos outros dois canais; a equação sem o dólar contra emergentes; o dólar contra emergentes sem o real; e o coeficiente em 2006–15 contra 2016–26.
    - Câmbio: se o S&P perder força ou virar, o dólar central do 1T28 cai até ~0,12 (com o S&P parado, 5,41 contra 5,53).
    - Inflação: ~−0,07 p.p. no IPCA em um ano (conta).
    - Selic: praticamente nada.
    - Agentes: o câmbio deixa de cortar o S&P à mão, e o externo passa a ter uma leitura clara do caminho de bolsa que escreve.
    - Custo: ~100 mil de teste, dividido com os itens 5 e 14, que reestimam a mesma equação; mais ~150–250 mil se a forma mudar.
- **Manter e só escrever o aviso.** A equação fica igual. O aviso vai na definição do externo e do câmbio: o S&P em alta, sozinho, enfraquece o real.
    - O corte à mão e a negociação continuam.
    - Custo: quase nada.
- **Tirar o S&P.**
    - Perde-se o ganho medido no mensal e o maior contribuinte do ajuste, sem saber o que entra no lugar.
    - Custo: ~150–250 mil, sem teste. Não recomendo.
- **Por que testar:** é barato, vai junto com os itens 5 e 14, e o sinal foi o maior custo de negociação do ciclo para o câmbio e o externo.
- **Exemplo.** No ciclo de 2026-10-27, o S&P do base subiu 11% por lucro e pôs +0,13 no dólar do 1T28. O câmbio aplicou × 0,55 à mão, e a assimetria do 1T28 ficou negativa por causa disso.
