# Cobranças · relatório do ciclo 2026-10-27

Cada cobrança reabre o report final do agente só no trecho citado: ele responde à pergunta e reescreve aquele trecho; o resto do report fica como está.

## C1 · respondida
- Para: cambio (`cambio_rf.md`, seção 1)
- Trecho: "| USD/BRL, PTAX de fechamento | 4T26 | 5,427 | 5,30 a 5,60 · 47% | acima de 5,60 · 31% | abaixo de 5,30 · 22% | +0,09 |" e "A central é a PTAX do P2, sem ajuste"
- Defeito: central conjunta diferente da central do RF nas casas do agente. O PF* dá 5,426 no 4T26 (`PF.json`, `central_p` 5,42582) contra 5,427 do RF; o PF* usou o `rr_10a` do 4T26 do report final do fiscal (7,75), e não o do P2 (7,72).
- Falta: em torno da central de 5,426, a faixa de 5,30 a 5,60 e as probabilidades de 47%, 31% e 22% do 4T26 continuam as mesmas? E as frases da seção 2 que dependem da central do 4T26 continuam valendo?
- Por que o leitor precisa: a tabela da seção 1 e o apêndice publicam 5,426 ao lado da faixa e das probabilidades escritas em torno de 5,427.
- No relatório: seção 1 e apêndice com a central 5,426; texto mantido como no RF.
- Resposta: `cambio_rf.md`, seção 2, Q4, "A distribuição": a frase passou a "cerca de 1,35% abaixo da PTAX de 26/10", em torno da central nova; 5,54 com a sazonalidade, a faixa e as probabilidades do 4T26 ficaram como estavam. Nada no relatório muda.

## C2 · respondida
- Para: politica_monetaria (`politica_monetaria_rf.md`, seções 1 e 2)
- Trecho: "*O modelo corta antes do que o Copom costuma.* Fechar o 4T26 em 13,43 pede mais de um corte de 25 p.b. até 09/12 (0,32 p.p. abaixo de 13,75), com a curva precificando alta"
- Defeito: central conjunta diferente da central do RF nas casas do agente. O PF* dá 13,44 no fechamento do 4T26 (`PF.json`, `central_p` 13,4429) contra 13,43 do RF.
- Falta: com a central de 13,44 no 4T26, a frase acima continua valendo, com que distância até 13,75? E a faixa de 13,30 a 13,80 com 62%, 32% e 6% continua a mesma?
- Por que o leitor precisa: a seção 2.8 lista "o modelo corta antes do que o Copom costuma" como um dos quatro erros do modelo, e a única evidência numérica dela citava a central antiga.
- No relatório: seção 2.8, placeholder preenchido; seção 1 e apêndice com a central 13,44.
- Resposta: `politica_monetaria_rf.md`, seção 2, Q4, "Onde acho que o modelo erra", terceiro item: 13,44 também pede mais de um corte de 25 p.b. até 09/12, 0,31 p.p. abaixo de 13,75; faixa e probabilidades sem mudança.

## C3 · respondida
- Para: inflacao (`inflacao_rf.md`, seção 2, Q1)
- Trecho: "Se o IPCA de outubro vier acima de 0,46, a leitura de "tendência estável" enfraquece."
- Defeito: 6, número sem referência clara (índice cheio ou serviços subjacentes).
- Falta: o limiar de 0,46% vale para o IPCA cheio de outubro ou para os serviços subjacentes do IPCA de outubro?
- Por que o leitor precisa: a seção 5 lista o IPCA de outubro como sinal a acompanhar, com dois limiares lado a lado.
- No relatório: seção 5, linha do IPCA de outubro, placeholder preenchido ("serviços subjacentes acima de 0,46%").
- Resposta: `inflacao_rf.md`, seção 2, Q1, parágrafo do IPCA-15: o limiar vale para os serviços subjacentes do IPCA de outubro, não para o índice cheio.

## C4 · respondida
- Para: fiscal (`fiscal_rf.md`, seção 4, Divergências)
- Trecho: "**Com a inflação, sobre a subvenção:** aberta e da decisão dela: a minha base fiscal supõe a subvenção em 2027 (custo no primário); a central dela não, só o tempero. Não muda nenhum caminho do P."
- Defeito: divergência aberta sem o que decidiria entre as posições; e 8.8.
- Falta: em que ponto exatamente a sua posição e a da inflação divergem, e que fato, número ou data decidiria entre elas?
- Por que o leitor precisa: a seção 4 mostra a divergência e precisa dizer o que a resolve.
- No relatório: seção 4, "A subvenção aos combustíveis em 2027", placeholder preenchido; seção 5 ganhou a linha "até 31/12/2026".
- Resposta: `fiscal_rf.md`, seção 4, Divergências, item "Com a inflação, sobre a subvenção": a divergência é sobre a decisão, não sobre o preço; decide um ato legal que estenda a subvenção a 2027, com valor, antes de 31/12/2026; primeiro sinal, a MP 1.395; condição, o Brent alto. A resposta abriu C6.

## C5 · respondida
- Para: inflacao (`inflacao_rf.md`, seção 4, IN-E7)
- Trecho: "A sua base supõe a subvenção mantida em 2027 (nível B), e é coerente com a minha leitura: ..."
- Defeito: 8.8, contradição entre agentes sobre haver ou não divergência.
- Falta: há uma divergência entre a sua leitura e a base do fiscal sobre a subvenção de 2027? Se há, o que a decidiria?
- Por que o leitor precisa: a seção 4 apresenta as duas posições e o que decide entre elas.
- No relatório: seção 4, mesmo parágrafo de C4, preenchido.
- Resposta: `inflacao_rf.md`, seção 4, IN-E7: na direção não divergem; a diferença é onde a decisão mora (premissa da base no fiscal, fora da central e sem tamanho na inflação); decide a renovação em lei ou MP, com valor, até dezembro. É o mesmo fato que o fiscal aponta.

## C6 · respondida
- Para: fiscal (`fiscal_rf.md`, seção 4, Divergências, item "Com a inflação, sobre a subvenção")
- Trecho: "Se 2026 terminar sem ele, o degrau de janeiro passa à base da inflação e a minha base tira o custo."
- Defeito: 8.8, contradição entre agentes: premissa sobre a área da inflação diferente do que a inflação escreveu. No IN-E7 reescrito, a inflação diz: "se não vier, o fim em janeiro entra como alta no 1T27, dentro dos +5% de combustíveis do upside", isto é, na cauda e não na base.
- Falta: sem o ato legal até 31/12/2026, em que parte da distribuição da inflação o degrau de janeiro entra, segundo o report da inflação, e o que isso muda na sua frase?
- Por que o leitor precisa: a seção 4 diz o que acontece com cada posição se o ato não sair.
- No relatório: texto mantido como no RF da inflação, dona da área (seção 4 e linha "até 31/12/2026" da seção 5 dizem "cauda de alta da inflação"); sem placeholder.
- Resposta: `fiscal_rf.md`, seção 4, Divergências, item "Com a inflação, sobre a subvenção", sub-item "O fato": sem o ato legal até 31/12/2026, o degrau de janeiro não passa à base da inflação; fica na cauda de alta dela, como alta no 1T27 dentro dos +5% de combustíveis do upside (IN-E7), porque a central não vê combustíveis. Do lado fiscal muda só a base, que tira o custo do primário de 2027. Nenhum caminho, faixa ou probabilidade muda; o relatório já dizia "cauda de alta da inflação" e fica como está. (2026-10-30, agente fiscal novo, sem o contexto da rodada, só com os três trechos; ~105k)
