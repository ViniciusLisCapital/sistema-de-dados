# Quadro de propostas para o Modelo Estrutural · 2026-10-30

Passo C1a da frente C (Plano 2). Junta três fontes:

- a seção 6 ("Sobre o modelo") dos 21 reports do ciclo 2026-10-27;
- as respostas dos sete agentes ao questionário de C1b (os outros arquivos desta pasta);
- os pedidos do usuário que já estavam no brief da frente C.

Cada linha foi cruzada com o que os `pendencias_*_eq.md` desta pasta já mediram. Várias propostas já têm meio teste feito.

**Como ler.**
- **Apoio:** quem pediu e quem apoiou na pergunta 6 do questionário. **Contra** aparece só quando alguém foi contra.
- **Custo:**
    - baixo: um termo numa equação e a reestimação;
    - médio: reestimar mais de uma equação, ou mexer no simulador e no `modelo.py`;
    - alto: um modelo novo (decomposição da curva, equação nova), ou uma exógena nova com principal na aba Exógenas.
- Toda mudança de especificação que passar custa, além do teste, a mesma lista fixa de trabalho:
    - MCMC da equação;
    - paridade Python/JS do simulador;
    - `modelo.py` e `CONVENCAO`;
    - os testes;
    - regerar o painel;
    - a lista de impacto para o chat E.
- **Impacto:** o que sai do tempero de cada agente e entra na central, ou o contrário.

## Resumo, na ordem em que as decisões vão ao usuário

| # | Proposta | Peça | Apoio (de 7) | Contra | Custo | Recomendação |
|---|---|---|---|---|---|---|
| 1 | Partir do dado já observado dentro do trimestre corrente | partida | 7 | — | médio | fazer |
| 2 | Separar prêmio de neutro na âncora `rr_10a` + meta | (R) e (H) | 6 | fiscal contra só a versão "suavizar" | alto | fazer, com o coeficiente livre como coluna de comparação |
| 3 | Termo de demanda fora do juro na IS (fiscal, crédito, intercepto) | (H) | 3 + usuário | — | médio | testar; entra o que passar |
| 3b | Desemprego no hiato | (H) | 0 | — | alto | fora do ciclo 2 |
| 4 | Faixa de previsão com o erro das equações | saída | 4 | — | baixo | fazer, no `modelo.py` |
| 5 | Sazonalidade do 4º trimestre no câmbio | (F) | 1 + usuário | — | baixo | testar |
| 6 | Vol implícita da tabela da B3 no lugar do CSV | (F) | 3 | — | baixo | fazer |
| 7 | Âncora da (E): quebra no peso da meta, Focus longa, ou soma-um livre | (E) | 3 | — | médio | testar |
| 8 | Monitorados: Brent em reais, indexação ao IPCA livre | (I) | 3 (+ PM no 2º teste solo) | — | médio | testar |
| 9 | Não linearidade do CDS | (F) | 4 + usuário | câmbio contra o log | baixo | testar a interação, não o log |
| 10 | S&P 500 e o dólar EM que contém o real | (F) | 3 | — | baixo | testar |
| 11 | Selic de fechamento por regra no fechamento, passo de 25 p.b. | saída / (R) | 1 + usuário | — | médio | arredondar a derivada; não reestimar |
| 12 | Regra de juros com câmbio ou CDS | (R) | 2 + usuário | expectativas e atividade, se vier sem a 2 | baixo | testar depois da 2 |
| 13 | Inflação implícita na (E) (2 anos) e na (F) (10 anos) | (E), (F) | 2 | câmbio (na F), PM (na E) | médio | não neste plano |
| 14 | PPC com o núcleo do CPI e coeficiente livre | (F) | 1 | — | baixo | testar junto com a 5 |
| 15 | Equação do CDS / componente global do CDS | novo | 2 | câmbio, se o CDS não puder mais ser imposto | alto | não neste plano |
| 16 | (H) no hiato do placar | (H) | 2 | — | médio | só checagem |
| 17 | Alimentação: in natura ou clima | (I) | 1 | — | médio | não neste plano |
| 18 | Âncora por componente na (I) | (I) | 2 | — | médio | não (20 trimestres de amostra) |
| 19 | Repasse cambial não linear | (I) | 1 | — | baixo | não neste plano |
| 20 | Linha do PIB com potencial móvel; modelo de PIB com demanda do governo | atividade | 2 | — | médio | linha móvel sim; modelo de PIB não |
| 21 | Satélites do bloco externo; hiato só na parte consolidada | novo | 1–2 | — | alto | não neste plano |

As quatro primeiras são as de maior convergência. Juntas, respondem pela maior parte do tempero que os agentes montaram à mão neste ciclo.


## 1. Partir do dado já observado dentro do trimestre corrente

- **O que é.** O modelo projeta o trimestre em curso a partir do último trimestre fechado e ignora o que já saiu dentro dele. A proposta: o 1º trimestre projetado usa a fração já observada.
    - Expectativas: as pesquisas Focus do trimestre.
    - PM: a Selic já decidida até a próxima reunião (proposta 2 de III.III.vi).
    - Câmbio: a PTAX diária.
    - Inflação: o IPCA mensal e o IPCA-15.
    - Fiscal: os pregões da `rr_10a` (média do trimestre).
- **Apoio.** Os sete. Expectativas e inflação pediram; PM, câmbio, atividade, fiscal e externo apoiaram.
- **Evidência no ciclo.**
    - A Focus do modelo no 4T26 é 4,17. As 16 pesquisas já feitas no trimestre têm média de 4,52. Para fechar em 4,17, o resto do trimestre teria de cair a 4,05, o que aconteceu em 3,1% dos dias desde 2001. O erro passa à (R) pelo desvio e, pela âncora, à inflação de 2027.
    - A Selic média do 4T26 é 13,48, mas 13,75 vale até 04/11.
    - A PTAX já subiu 6,2% dentro do 4T26, e a (F) parte do fechamento do 3T26.
    - A `rr_10a` do 4T26 tinha 17 de 60 pregões a 6,99% antes do 2º turno. O fiscal fez à mão a conta da média.
- **Já medido.** Nada.
- **Teste.** Pseudo-tempo-real de 2010 a 2026. Para cada trimestre, projetar com e sem a fração observada até o dia equivalente do ciclo. Adotar se o erro do 1º trimestre cair sem piorar o 2º.
- **Custo.** Médio. Não reestima nada: é uma regra de partida no `modelo.py`.
    - Endógenas com média do trimestre (Focus, Selic): a média ponderada entre os dias observados e o que o modelo dá para o resto. É mecânico.
    - Câmbio de fechamento: trocar o ponto de partida por um nível conhecido no dia exige decidir a convenção, porque a (F) é em variação.
    - Exógenas em média do trimestre (`rr_10a`, vol): o `modelo.py` passa a fornecer a média parcial, para o agente não refazer a conta.
    - Depende do F(A) carregar o dado diário do trimestre aberto (chat E).
- **Risco.** O câmbio avisa que o caminho da vol que ele escreveu já carregava o choque de 26/10. Com a partida condicionada, o choque não pode entrar duas vezes. A regra de escrita dos caminhos muda junto.
- **Impacto.**
    - Focus do 4T26 de 4,17 para ~4,45; a inércia leva parte disso ao 1T27.
    - Selic do 4T26 para cima.
    - PTAX do 4T26 mais perto do spot.
    - IPCA do 4T26 de 5,34 para ~5,2. A inflação lia a conta com o IPCA-15 e a Focus.
    - Sai do tempero: a evidência 1 das expectativas, o "a (E) começa baixa" da PM e o deslocamento de partida da atividade.

## 2. A âncora `rr_10a` + meta

- **O que é.** A (R) põe a Selic de equilíbrio em `rr_10a + meta`, de um para um. Desde 2026-09-25 a (H) mede o aperto contra a mesma âncora. Com isso, um prêmio de risco no juro longo vira juro neutro: sobe a Selic e não aperta a economia.
- **Apoio.**
    - É o maior custo do ciclo para o fiscal e a PM, e o segundo para a atividade.
    - Câmbio e expectativas apoiam: ele inverte o sinal econômico das caudas de dominância deles.
    - O externo apoia separar o prêmio.
    - A inflação é indiferente: no horizonte, a âncora move a Selic e não o IPCA.
    - Pedido do usuário: refazer a taxa neutra (propostas 1 e 3 de III.III.vi).
    - O fiscal é **contra** a versão "suavizar a taxa de 10 anos", porque ela esconde o prêmio em vez de separá-lo.
    - PM e atividade pedem que (R) e (H) mudem juntas.
- **Evidência no ciclo.**
    - O salto de 26/10 foi de +135 p.b. na NTN-B de 10 anos, e só +22 p.b. vieram dos dois primeiros anos da curva real. O prêmio põe 0,76 a 1,00 p.p. na Selic de fechamento do modelo, com o hiato igual (ata, item 5).
    - O hiato saiu idêntico nos três cenários da PM e nos do fiscal (diferença máxima de 0,01). As caudas fiscais viraram só nível de Selic.
    - As duas revisões do caminho de `rr_10a` do fiscal moveram a central da Selic em 0,1 a 0,5 p.p., sem dado novo de inflação ou atividade.
    - No upside fiscal o modelo sobe a Selic e aprecia o real. O câmbio teve de rodar um segundo upside para representar a dominância.
- **Já medido** (`pendencias_taylor_eq.md` R2, R11 e R12; `pendencias_is_eq.md` H6, H9 e H10).
    - A `rr_10a` crua correlaciona +0,80 com o próprio aperto.
    - Cortar a curva não resolve: todo vértice e toda taxa a termo correlaciona ≥ 0,88 com a NTN-B de 2 anos, porque a curva se move em bloco. A termo de 5a→10a ainda tem +0,70.
    - Separar prêmio de expectativa exige modelo. Duas rotas, estimadas antes de escrever: strip pela Focus (até 5 anos sem hipótese, ~150 linhas) ou estrutura a termo afim tipo ACM (~250 linhas).
    - O prêmio de maturidade é de 0,9 a 1,1 p.p. em 3–4 anos. Descontado, o neutro de hoje fica em ~6,45%, a Focus de 4 anos.
    - Suavizar (média de 7 anos) leva a âncora de 7,67% a 5,46% e o efeito de longo prazo de 2,83 a 3,09. A janela de 5 anos custa 19 trimestres de amostra.
    - Na (H), o gap contra a âncora perde força em 2016–2026 (t −0,44). Uma das hipóteses é o prêmio variando dentro do neutro.
- **Opções.**
    - (a) **Separar.** Neutro de mercado pelo strip da Focus (ou o neutro do QPC, onde houver) mais a meta, como âncora da (R) e neutro da (H). O prêmio (`rr_10a` − neutro) entra na (H) como regressor próprio, de custo de capital.
    - (b) **Só liberar o coeficiente da âncora**, na (R) e na (H). É barato, mas perde o estado de repouso em `RR* + meta` e pede intercepto (R3).
    - (c) **Âncora mais curta** (5 anos, ou o termo 2–5a). Já medido que quase não descontamina.
    - (d) **Suavizar a `rr_10a`.**
- **Teste.** Estimar a (R) e a (H) de 2006 a 2026 com (a), (b) e (d) lado a lado, e comparar o erro fora da amostra.
    - Muda a especificação se o peso do prêmio na âncora tiver intervalo abaixo de 1, ou se o prêmio sair negativo e significativo na (H).
    - Rodar a (b) junto custa uma coluna e responde à pergunta da PM.
- **Custo.** Alto na (a): o strip, duas equações reestimadas por MCMC, simulador e `modelo.py`. E uma pergunta de governança: quem escreve o caminho do neutro e quem escreve o do prêmio. Hoje a `rr_10a` é exógena do fiscal. Com (a), o neutro de pesquisa fica perto do agente de expectativas, e o prêmio, do fiscal. A aba Exógenas é do usuário.
- **Impacto.**
    - A central da Selic deixa de ser o caminho de `rr_10a`: cai uma fração dos 0,76–1,00 p.p. do prêmio de 26/10.
    - O hiato passa a diferir entre cenários fiscais.
    - Saem do tempero: o "regimes não seguem `rr_10a`" da PM, o tempero de condições financeiras da atividade (−0,06 no 1T28) e o segundo upside do câmbio.
    - Efeito colateral, dito pela atividade: a Selic do modelo se afasta ainda mais da mediana da PM. É uma distância honesta, mas maior.

## 3. Termo de demanda fora do juro na (H), e a pergunta do chat B

- **O que é.** A (H) só tem o hiato defasado, o aperto e as duas dummies de crise. O erro dela tem um sinal só. A proposta: um termo de demanda fora do juro.
    - Candidatos: impulso fiscal (na medida do fiscal, com parafiscal), impulso de crédito ou fluxo financeiro, o prêmio de risco do próprio BC (`rp_hat`, H5) e, se nada fechar, intercepto.
- **Apoio.** Atividade (é a proposta 1 dela), fiscal (o impulso como exógena dele), inflação (é o teste da IN-E5 dela) e o usuário (crédito na IS). A PM e as expectativas são indiferentes.
- **Evidência no ciclo.**
    - O erro de um passo foi positivo em 25 trimestres seguidos, com média de +0,25 nos últimos oito.
    - Rodada sozinha desde o 4T24, a (H) daria −0,74 no 3T26, contra 0,41 publicado.
    - A atividade montou um tempero de resiliência de +0,05 a +0,10 com uma razão de 0,09 p.p. de hiato por ponto de impulso que não é estimada.
- **Já medido.**
    - O `rp_hat` do BC já é construído em `modelo_agregado/modelo_painel.py` e é importável (H5). No BC, `b3` = 0,030, bem identificado.
    - Com a medida antiga do aperto o intercepto quase não mudava nada. Com o gap atual não foi medido.
- **Dados.**
    - `cred_fluxo_financeiro` está parado em 2026-04 (aviso do chat B). É um teste possível, mas um insumo que para o caminho no meio do horizonte.
    - `fisc_efgg` vai até o 2T26.
- **Teste.** Reestimar em 2006T2–2026T2 com cada candidato, e Breusch-Godfrey no erro. Entra o termo significativo que deixar o erro sem sinal único. Intercepto só se nenhum fechar.
- **Custo.** Médio. Cada termo que entrar é uma exógena nova com principal: o fiscal para o impulso fiscal, o agente de crédito para o impulso de crédito.
- **Impacto.**
    - Com o termo fiscal: o hiato sobe +0,05 a +0,10 no começo e fica perto de zero no 1T28, porque o impulso do fiscal vira −0,3.
    - Com intercepto puro: sobe de forma crescente, +0,1 a +0,3 no 1T28.
    - Nos dois casos a resiliência sai do tempero.

**3b. Desemprego no hiato.** Nenhum dos sete pediu. Pô-lo no hiato não é um termo na (H): a variável da (H) é o hiato do BC, lido pronto. O desemprego só entraria com um modelo do hiato próprio (item 21), que está fora deste plano.

**Posição para o chat B** (depende da decisão do usuário sobre o item 3):
- O crédito entra no teste do item 3 como candidato. Se passar, o agente de crédito é principal da exógena de impulso de crédito na (H). Se não passar, ele segue a regra de fiscal e externo: a tese é o caminho das exógenas de que tem tutela. Hoje não tem nenhuma; a tese dele fica fora do modelo.
- O mercado de trabalho não ganha variável no ciclo 2. A tese dele fica fora do modelo, como a linha companheira do PIB da atividade.

## 4. Faixa de previsão com o erro das equações

- **O que é.** A faixa que o modelo imprime é só a incerteza dos pesos. Ela não serviu de distribuição a nenhum agente. Exemplos:
    - PM: no 4T26 a faixa vai de 13,12 a 13,75 e não contém nenhuma alta.
    - Câmbio: 5,34 a 5,52, contra um erro da equação de ~3,6% por trimestre.
    - Atividade: no 1T28, de −1,11 a 0,00.
- **Apoio.** Câmbio, PM, inflação e atividade pediram; o externo se queixou da mesma coisa.
- **Já existe.** O posterior de cada equação tem `sigma`. O simulador já somou o erro da equação e o usuário cortou o controle em 2026-09-24, como opção de tela. A proposta aqui é outra: uma segunda faixa na saída do `modelo.py`, para os agentes, sem tocar no painel.
- **Teste.** Cobertura das faixas de 80% e 90% num backtest recursivo de 2012 a 2026, por horizonte.
- **Custo.** Baixo.
- **Impacto.** A central não muda. As caudas dos agentes passam a ter uma dispersão medida para comparar, em vez de pontos de cauda escolhidos à mão.

## 5. Sazonalidade do 4º trimestre no câmbio

- **Apoio.** Pedido do usuário; é a proposta 1 do câmbio.
- **Evidência.** O resíduo da (F) no 4T foi positivo em 8 de 9 anos desde 2017, com média de +2,1%. Entrou como tempero de +0,11 na PTAX do 4T26 e do 4T27.
- **Teste.** Quatro dummies de trimestre (soma-zero, como na (I)), interagidas com o pós-2017, e fluxo financeiro de nov–dez como alternativa. Adotar se a do 4T tiver intervalo de 90% acima de zero e o erro fora da amostra de 2021–2025 cair. Ver se o 1T devolve o efeito.
- **Custo.** Baixo.
- **Impacto.** A PTAX central do 4T sobe ~+2% e o tempero sai.

## 6. Vol implícita da tabela da B3

- **Apoio.** O câmbio pediu (proposta 4 dele); a PM e o fiscal apoiaram.
- **Evidência.** O modelo segurou a vol em 12,19 (2T26), porque o CSV da Bloomberg para em 2026-08-04. A vol é o canal que mais move a central do 4T26, e foi escrita sem dado.
- **Já feito.** `macro_brasil.cmb_vol_implicita` existe desde 2026-10-28, pela B3 (F4).
    - Contra o CSV no 3M, em 5.098 pregões: diferença média −0,19 p.p. e correlação de fim de mês 0,978.
    - Os desvios grandes ficam em estresse agudo e em evento dentro do prazo fixo.
    - A troca de fonte é decisão do usuário, ainda não tomada.
- **Teste.** Reestimar a (F) com a série da B3. Adotar se o coeficiente do carry/vol ficar no intervalo atual.
- **Custo.** Baixo. Fecha também uma dívida de encanamento (insumo fora do banco).

## 7. Âncora da equação de expectativas

- **Apoio.** Expectativas (proposta 1), inflação (apoio forte: é a maior fonte de assimetria dela) e PM.
- **Evidência.** 7 de 8 resíduos positivos desde 4T24, com média de +0,35. Zerar o viés pediria peso da meta de ~0,03, fora do posterior. O tempero usado (`E.e1` × 1,2 no base) mexe na inércia, que não é o defeito, e custou uma negociação com a PM (ata, item 8).
- **Opções.**
    - (a) Quebra em 2017 ou peso da meta variável no tempo.
    - (b) Âncora na Focus longa (t+3, hoje 3,50) no lugar da meta. Vira exógena com caminho; o principal seria o agente de expectativas.
    - (c) Pesos sem impor a soma um, o que dá um multiplicador direto no peso da meta.
- **Já medido.** O resíduo da (E) rejeita Ljung-Box (autocorrelação de 0,393, E1). O câmbio na (E) dá `e3` = 0,018 (t 2,11), fora da forma (E4).
- **Teste.** O erro de um passo fora da amostra em 4T24–3T26. Mudar se cair mais de um terço e o viés sumir.
- **Custo.** Médio.
- **Impacto.** A Focus central sobe +0,16 a +0,33 p.p. sobre o P2. A inflação sobe +0,1 a +0,2 em 3T27–1T28.

## 8. Monitorados: Brent em reais e a indexação ao IPCA livre

- **Apoio.** Inflação (proposta 1) e externo (o Brent como exógena dele). A PM também pediu, no 2º teste solo (III.III.vi, proposta 4). O fiscal apoia a parte do tributo sobre combustível.
- **Evidência.**
    - O Brent subiu ~90% em 12 meses. Para o modelo, uma PTAX 4–7% mais fraca dá no máximo +0,01 p.p. a monitorados.
    - Toda a história de combustíveis ficou no tempero da inflação: +0,14 a +0,27 p.p. no upside.
- **Já medido.** A indexação ao IPCA cheio tem sinal negativo (−0,225, t −0,40; o posterior dá −0,21). Ela devolve parte de qualquer choque ao próprio IPCA com o sinal trocado. O conserto proposto, indexar à parte livre, não precisa de dado novo (P3). O Brent em bens industriais é o P1, com aviso de colinearidade com os metais.
- **Teste.** Monitorados de 2003 a 2026, com e sem Δlog(Brent × PTAX) em t−1 e com o livre em t−1. Muda se o petróleo entrar positivo com intervalo fora de zero e a indexação ficar positiva.
- **Custo.** Médio. Uma exógena nova, o Brent, com o externo de principal. O tributo sobre combustível não tem série: fica de fora.
- **Impacto.** A central da inflação sobe 0,1–0,3 p.p. em 1T27–3T27 e devolve parte em 4T27–1T28. O tempero de combustíveis sai.

## 9 a 21, mais curtos

- **9. Não linearidade do CDS na (F).**
    - Apoio: pedido do usuário; câmbio, fiscal, externo e inflação.
    - O real andou 4,4× (05/10) e 5,9× (26/10) o que o CDS explica pelo modelo.
    - O dado trimestral do câmbio vai contra o CDS em log: com o CDS baixo a sensibilidade é menor, não maior. O fiscal concluiu o mesmo na moderação.
    - A dummy eleitoral teria 2–3 eventos na amostra.
    - Testar ΔCDS × nível e ΔCDS × vol. Custo baixo.
    - Efeito: o × 1,2 do upside vira especificação; a central quase não muda.
- **10. S&P 500 e o dólar EM.**
    - Apoio: câmbio, externo e fiscal.
    - O S&P tem sinal oposto ao da correlação bruta: colinearidade com o CDS e o dólar EM, medida em F1.
    - O dólar EM contém o real (peso ~0,07).
    - Testar a (F) sem o dólar EM, com o S&P ortogonalizado e com o índice sem o real. Os pesos da cesta não estão no banco; a alternativa é o resíduo da regressão diária.
    - Efeito: a PTAX do 1T28 cai até ~0,12, e o × 0,55 sai do tempero.
- **11. Selic de fechamento.**
    - Apoio: pedido do usuário; PM.
    - A derivada é contínua: o 4T26 a 13,43 pede mais de um corte com a curva precificando alta. A PM corrigiu pelo tempero.
    - Já medido no `modelo.py`: a derivada erra 0,12 p.p. em média. Degraus nas reuniões, encadeados por 12 trimestres, chegam a 41,8 p.p. de erro.
    - Opções: (a) arredondar a derivada a 25 p.b., com passo máximo por reunião, que é barato e mecânico; (b) reestimar a (R) no fechamento.
    - A (b) mexe na convenção da (H), que usa a média. A (F) foi estimada com o fechamento (F2).
    - Recomendação: (a).
- **12. Câmbio ou CDS na regra de juros.**
    - Apoio: pedido do usuário; PM e externo. O câmbio apoia com ressalva.
    - Expectativas e atividade são contra se vier sem o item 2: o prêmio pesaria duas vezes na Selic.
    - Cria o laço câmbio → Selic → carry → câmbio.
    - Testar depois do item 2, com teste fora da amostra.
- **13. Inflação implícita como regressor.**
    - 2 anos na (E), proposta das expectativas; 10 anos na (F), proposta do fiscal.
    - O câmbio é contra na (F) contemporânea: é endógena e colinear com o CDS.
    - A PM é contra na (E): carrega o mesmo prêmio que o item 2 quer tirar.
    - As expectativas pedem que, se entrar, as duas tenham um principal só.
    - Custo médio, com exógena nova. Não neste plano.
- **14. PPC com o núcleo do CPI e o coeficiente livre.**
    - Pedido do externo; o câmbio está inclinado a apoiar.
    - No cenário de Fed mais alto o modelo aprecia o real: o CPI entra com peso 1.
    - Já medido (F §2): sem o offset, o α vira deriva de ~2,7 p.p. ao ano. Liberar o coeficiente pede cuidado com o α.
    - Custo baixo. Testar junto com o item 5, na mesma reestimação da (F).
- **15. Equação do CDS** (fiscal: em função das revisões da Focus de primário e de dívida) **ou componente global do CDS** (externo: em função do dólar EM e do S&P).
    - O câmbio só aceita se o CDS ainda puder ser imposto por cenário.
    - Custo alto. Não neste plano.
- **16. (H) no hiato do placar.**
    - Pedido da atividade, como checagem. A inflação pede a (I) no mesmo hiato.
    - Só 20 trimestres de amostra, e o usuário deixou as edições do hiato de lado em 2026-09-21 (H1).
    - Custo médio. Só checagem.
- **17. Alimentação: in natura ou clima.**
    - Pedido da inflação.
    - O `clima_oni` para em 2026-04 e está fora das listas.
    - Não neste plano.
- **18. Âncora por componente na (I).**
    - Inflação; expectativas com condição.
    - Bloqueado por amostra: a Focus por componente só existe desde set/2021 (P6).
- **19. Repasse não linear.**
    - Inflação.
    - Pequeno: +0,05 p.p. Não neste plano.
- **20. A linha do PIB.**
    - A atividade pede um potencial móvel e uma partida pelo carrego do IBC-Br. A central mecânica dá 1,89% no 4T26, contra 1,15% do carrego e 1,67% da Focus.
    - É uma conta derivada, não equação. Custo baixo, e entra com o item 1.
    - O modelo de PIB com demanda do governo (usuário e fiscal) fica fora deste plano.
- **21. Satélites do bloco externo** (`infl_us`, agro em função do Brent) e **hiato só na parte consolidada** (usuário).
    - Disciplina, sem número do ciclo por trás.
    - Fora deste plano.

## O que fica de fora por princípio

O Modelo Estrutural é o filtro de saída da análise (I.III.xv): o que entra nele tem de ter dono do caminho e ser medido.

Duas propostas trocam um tempero por uma exógena sem dado no banco: o tributo sobre combustível e o impulso de crédito com a série parada. Elas só entram quando o dado existir.
