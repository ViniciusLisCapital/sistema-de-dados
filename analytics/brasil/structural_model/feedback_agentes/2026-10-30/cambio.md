# Feedback do agente de câmbio sobre o Modelo Estrutural · 2026-10-30

Resposta literal do `cambio-analyst` (Opus, modo ad hoc) ao questionário da frente C (passo C1b), a partir do report final do ciclo 2026-10-27. Só leitura dos arquivos do ciclo. Custo: 165k tokens.

---

**1. Onde o modelo complicou o trabalho**

O maior custo veio do ponto de partida. A (F) parte do fechamento do 3T26 (5,181) e não sabe que a PTAX já subiu 6,2% dentro do 4T26. Dos ~9,2% do pregão de 26/10, o CDS explica ~1,6%. Quem fez o papel de alavanca do nível foi o caminho da volatilidade implícita, que eu escrevo sem dado: ela não está no F, e o modelo segura 12,19 no 3T26. No r1 o 4T26 saía assim: 5,21 sem caminho nenhum, 5,275 com o CDS, o dólar contra emergentes e o S&P no nível de hoje, e 5,381 com a vol a 17%. Escolher 17% em vez de 18,5% move a central em ~0,02. Mesmo assim, a central do 4T26 ficou 1,34% abaixo da PTAX de 26/10.

O segundo custo foi a sazonalidade. O resíduo da (F) no 4T foi positivo em 8 dos 9 anos desde 2017, com média de +2,1%. Ela entrou como tempero de +0,11 (5,43 → 5,54 no 4T26 e 5,51 → 5,63 no 4T27), e só por isso a assimetria do 4T26 ficou em +0,09.

O S&P 500 entra com sinal contrário ao mecanismo do mapa: no 1T28 ele soma +0,12 à PTAX. Apliquei × 0,55, perto do piso do posterior, e o item foi para a moderação (item 4). É ele que deixa a assimetria do 1T28 negativa.

O CDS entra de forma linear. Em 26/10 o real andou ~6 vezes o que o CDS explica pelo modelo. Daí o × 1,2 no upside, e uma rodada inteira de discussão com o fiscal sobre o × 1,5 (item 2 da ata).

A Selic sai da âncora `rr_10a` + meta. No upside, a NTN-B a ~9% leva a Selic do modelo a 14,30% no 1T27, e esse carry aprecia o real em 0,01 a 0,04. Para representar a dominância fiscal tive de rodar um segundo upside, com a NTN-B no base. No downside acontece o contrário: o corte da Selic tira de 0,01 a 0,03 da apreciação. No base, a Selic do modelo é de 12,30% no 4T27, contra a mediana da política monetária acima disso e 15,78% na curva para dez/27.

Por fim, a faixa do posterior (5,34 a 5,52 no 4T26) não inclui o erro da equação, de ~3,6% por trimestre. Por isso não serve como distribuição, e montei as faixas a partir dos pontos de cauda.

**2–5. Propostas**

| Proposta (mais importante primeiro) | Equação · peça · coeficiente | Teste | Efeito na tese deste ciclo |
|---|---|---|---|
| Sazonalidade do 4T: dummy pós-2017 ou fluxo financeiro de nov–dez | (F), termo novo | Reestimar com dummies dos quatro trimestres, interagidas com o pós-2017. Adotar se a do 4T tiver intervalo de 90% acima de zero e cair o erro fora da amostra de 2021–2025. Ver se o 1T devolve o efeito | Central do 4T26 e do 4T27 sobe ~+2% (~+0,11). O tempero sai para a central, e a assimetria do 4T26 cai para perto de zero. No 1T27–3T27 o efeito depende de o 1T reverter: se não reverter, o nível fica mais alto |
| Sinal do S&P: (F) sem o dólar EM, com o índice sem o real, ou S&P ortogonalizado | (F), `F.b_sp500` (+1,89; 0,98–2,79) e `F.b_dxy_em` | Reestimar sem o dólar EM e medir a correlação das duas variações. Se o sinal virar ou perder significância, tirar o S&P ou ortogonalizar | Central de 2027–28 cai até ~0,12 no 1T28 (o S&P parado dá 5,41 contra 5,53). O × 0,55 sai do tempero, e a assimetria do 1T28 vai de −0,03 para perto de zero ou positiva |
| Primeiro trimestre condicionado à PTAX diária já observada | Ponto de partida da projeção | Pseudo-tempo-real de 2010–2025: projetar cada trimestre com e sem os dias observados até a data do ciclo. Adotar se o erro do primeiro trimestre cair sem piorar o segundo | 4T26 mais perto do spot. A direção é para cima, mas depende do dia: 5,50 em 26/10, 5,35 no comercial em 27/10. Como a (F) é em variação, o deslocamento persiste no horizonte. O caminho da vol deixa de carregar o choque, e é preciso evitar contá-lo duas vezes |
| Vol implícita no banco; até lá, o trimestre faltante preenchido pela realizada | Convenção da exógena `vol` (carry/vol) | Estimar a (F) com a implícita preenchida pela realizada (erro de 2,1 p.p.) contra a atual. Adotar se o coeficiente de carry/vol ficar no intervalo | Pouco efeito na central, ±0,02 por 1,5 p.p. Muito efeito na confiança: o canal que mais move o 4T26 deixa de ser escrito sem dado |
| Não linearidade do CDS: interação ΔCDS × nível, ou Δlog | (F), `F.b_fiscal` (25,1; 19,5–30,6) | Reestimar trimestral com as duas formas. Adotar se o coeficiente for estável entre 2006–2015 e 2016–2026 e o em p.b. não for, ou se a interação sair do zero | Central quase igual, porque o base só anda 10 a 17 p.b. O × 1,2 do upside vira especificação. O meu dado trimestral (0,57% contra 0,85% por 10 p.b. com o CDS baixo) é contra o log |
| Faixa preditiva com o erro da equação, além do posterior | Faixa impressa | Cobertura da faixa de 90% nos fechamentos de 2016–2025, em pseudo-fora da amostra | Central igual. As faixas e as probabilidades passam a partir de uma dispersão medida, em vez dos pontos de cauda; a faixa sairia bem mais larga que a de hoje |

**6. Propostas na mesa que me tocam**

- **a.** Apoio, porque é a minha primeira linha. Peço as quatro dummies e o teste de reversão no 1T.
- **b.** Apoio o teste, sou cético quanto ao log: no trimestral, a sensibilidade com o CDS baixo é menor, não maior. Prefiro a interação com o nível. Uma dummy eleitoral teria dois ou três eventos na amostra.
- **c.** Contra na forma contemporânea. A implícita de 10 anos responde ao próprio câmbio (repasse), é endógena à (F) e é colinear com o CDS. Só a aceito defasada ou instrumentada.
- **d.** Apoio, porque é a minha segunda linha.
- **e.** Indiferente, inclinado a apoiar. O CPI do base anda pouco, então o efeito na central é pequeno, e liberar um coeficiente imposto é bom.
- **f.** Apoio, porque é a minha quarta linha.
- **g.** Apoio liberar o coeficiente ou separar o prêmio. Hoje a NTN-B de cauda vira carry e aprecia o real justamente no cenário de dominância, e me obriga a rodar dois upsides.
- **h.** Apoio com o teste, mas ele cria o laço câmbio → Selic → carry → câmbio e amortece o upside no modelo. As caudas de dominância continuariam precisando da versão sem reação.
- **i.** Indiferente. A tese é a PTAX; a Selic de fechamento só pesa na leitura de E3 e S1.
- **o.** Apoio, porque é a minha terceira linha.
- **s.** Cautela com tornar o CDS endógeno: o canal das minhas caudas sai do fiscal e entra no laço. Só apoio se o CDS ainda puder ser imposto por cenário.

Abri: obsidian/ciclos/2026-10-27/cambio_rf.md (inteiro); log.md (Rodada 1, Rodada 2 e Report final · câmbio, Consolidação PF*, Divergências abertas); ata_r2.md (pauta e itens 2 e 4, por grep); PF.md (seções 1, 2 e 4); cambio_r1.md e cambio_r2.md (trechos sobre vol, partida e Selic, por grep).
