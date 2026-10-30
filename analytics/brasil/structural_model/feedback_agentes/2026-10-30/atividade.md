# Feedback do agente de atividade sobre o Modelo Estrutural · 2026-10-30

Resposta literal do `atividade-analyst` (Opus, modo ad hoc) ao questionário da frente C (passo C1b), a partir do report final do ciclo 2026-10-27. Só leitura dos arquivos do ciclo. Custo: 140k tokens.

---

Usei o ciclo 2026-10-27, só leitura, sem gravar nenhum arquivo.

**1. Onde o modelo complicou o trabalho**

A maior parte da minha distribuição foi montada à mão em volta da (H). Quatro casos:

- **O salto de 26/10 não aperta nada no modelo.** Com `rr_10a` em 8,05, a Selic do modelo sobe 0,21 p.p. e o hiato não se move (r1). Isso se repetiu no P2: o caminho do fiscal ficou 0,15 a 0,20 p.p. acima do P1 e o hiato saiu idêntico. A política monetária mediu que o prêmio põe 0,76 a 1,00 p.p. na Selic de fechamento, também com o hiato igual (ata_r2, item 5). Para mim aquilo foi custo de capital, e o fiscal concorda. Por isso criei um tempero de condições financeiras: −0,02 p.p. por trimestre no começo e −0,01 depois, −0,06 acumulado no 1T28. Esse tamanho não é estimado.
- **A (H) erra sempre para o mesmo lado.** O erro de um passo foi positivo em 25 trimestres seguidos, com média de +0,25 nos últimos 8. Rodada sozinha desde o 4T24, a equação daria −0,74 no 3T26 contra os 0,41 publicados. Para acertar, o `H.h2` teria de ser cerca de um sexto do estimado, fora do posterior. Montei um tempero de "resiliência" de +0,05 a +0,10 com uma razão de 0,09 por ponto de impulso fiscal que não é estimada: foi a parte fiscal do meu r1 dividida pelo impulso medido.
- **O ponto de partida não é meu.** O modelo parte dos 0,41 do BC para o 3T26, um nowcast. O IBC-Br de jul–ago implica −0,38, e a Focus implica 0,15. Precisei de uma regressão de revisão contra PIB (inclinação 0,24, 20 edições) para chegar a uma discordância de −0,15, que entra só como assimetria. E a (H) é estimada na edição atual, revista para cima em 20 de 20 trimestres, enquanto o placar usa outra edição.
- **A Selic do modelo é baixa demais para a minha tese.** O hiato herda a Selic da (R): 12,18 no 1T28 no P2, contra média de 12,96 na distribuição da política monetária. Somei um deslocamento de −0,16 no 1T28 fora da central. Como o hiato quase não volta para a Selic (no máximo 0,05 p.p. entre cenários), as duas equações não conversam.
- **A linha do PIB.** A central mecânica (potencial fixo de 2,50 mais a variação do hiato) dá 1,89% no 4T26. O carrego do IBC-Br dá 1,15% e a Focus 1,67%. Tive de deslocar a linha em −0,15 e −0,10 p.p. no 4T26 e no 1T27 e pôr 42% na cauda baixa. Além disso, o potencial implícito oscila (subiu de 2,2 para 2,7, desvio de 0,30) e a linha não separa choque de oferta (extrativa, agro).
- **A faixa do posterior é estreita.** No 1T28 vai de −1,11 a 0,00, sem o erro da equação nem a revisão do hiato. A dispersão da tese tive de montar por fora, com o erro da (H) de 0,34 em um trimestre e 0,62 em seis.

**2–5. Propostas, da mais importante para a menos**

| # | O que é | Equação / peça | Teste que decide | Efeito na tese deste ciclo |
|---|---|---|---|---|
| 1 | Termo de demanda fora do juro: impulso fiscal (na medida do fiscal), impulso de crédito ou fluxo financeiro; intercepto só se nada disso fechar | (H): erro sem intercepto; `H.h1` e `H.h2` reestimados junto | Reestimar em 2006T2–2026T2 com cada termo; Breusch-Godfrey no erro. Muda se o termo for significativo **e** o erro deixar de ter um sinal só | Com o termo fiscal: para cima no começo (+0,05 a +0,10) e perto de zero ou para baixo no 1T28, porque o impulso vira −0,3. Com intercepto puro: para cima e crescente (ordem +0,1 a +0,3 no 1T28, já que o estado de repouso é 8 vezes o intercepto). Nos dois casos a resiliência e a razão de 0,09 saem do tempero |
| 2 | Âncora separada em neutro (QPC + meta) e prêmio (NTN-B 10a − neutro), com o prêmio como regressor próprio | (H) e (R) juntas, porque usam a mesma âncora | (H) com o prêmio à parte, desde que o QPC pergunta o neutro. Muda se o prêmio tiver coeficiente negativo e significativo | Para baixo. Se o coeficiente do prêmio igualar o `H.h2`, o salto de ~0,9 p.p. sobre a média pré-eleição dá ~−0,06 por trimestre; contra a média do 3T26 dá quase zero. O tempero de condições financeiras (−0,06 no 1T28) entra na central. Efeito colateral: a Selic do modelo cai 0,8 a 1,0 p.p. e se afasta da política monetária, o que aumenta o meu deslocamento S-PM1 |
| 3 | Estimar a (H) no hiato do placar | (H), a edição do hiato | 20 trimestres desde 2021 e comparar `H.h1` e `H.h2`. Serve como checagem, não substituição: muda se os coeficientes saírem do intervalo de 90% atual | Central mais baixa, na ordem de 0,1 a 0,3 em 2027, porque o placar fica em média 0,28 abaixo da edição atual. Parte do viés da proposta 1 passaria a ser revisão, e a resiliência encolhe |
| 4 | Potencial móvel na linha do PIB e primeiro trimestre condicionado ao carrego do IBC-Br | Linha companheira e ponto de partida | Backtest da linha mecânica contra a primeira divulgação do IBGE desde 2021: potencial fixo contra média de 8 trimestres, com e sem o carrego (o IBC-Br tem desvio de 0,48 contra o PIB) | PIB do 4T26 de 1,89 para entre 1,15 e 1,67. O deslocamento de −0,15 e −0,10 da linha sai do tempero |
| 5 | Partida ajustada pela revisão esperada | Ponto de partida da projeção | Fora da amostra: revisão (placar − primeiro número) contra o carrego do IBC-Br. Muda se a correlação se mantiver acima de ~0,5. A amostra não tem trimestre negativo, e é isso que o 3T26 testa | Hoje a própria regra dá revisão de −0,02, e a central quase não muda. A discordância de −0,15 continua sendo julgamento, não modelo, até a amostra ter um trimestre de queda |

**6. Propostas da mesa que tocam o meu trabalho**

- **g (âncora da R)** · apoio, desde que andem juntas (g, minha k e a proposta 2 acima). Corrigir só a (R) deixa a (H) lendo o prêmio como neutro.
- **h (regra com câmbio ou CDS)** · indiferente no mérito, mas toca a Selic que entra no aperto. Se o CDS entra na (R) e o prêmio continua na âncora, o prêmio pesa duas vezes na Selic.
- **i (Selic de fechamento)** · indiferente, com uma ressalva: a (H) usa a Selic média, e a conversão fechamento→média precisa ser uma só nas duas equações.
- **j (viés da H)** · apoio; é a minha proposta 1, a que mais custou tempero neste ciclo.
- **k (prêmio como custo de capital)** · apoio; é a proposta 2.
- **l (H no hiato do placar)** · apoio como checagem; a amostra é curta para substituir.
- **m, n (equação de expectativas)** · indiferente. Chegam ao hiato só pela Selic, e essa ligação é fraca.
- **o (primeiro trimestre condicionado ao dado parcial)** · apoio. Resolve metade da proposta 4 e dá à partida uma regra em vez de julgamento.
- **s, modelo de PIB com a demanda do governo e variáveis próprias para o fiscal** · apoio. É o termo fiscal da proposta 1 com um principal, o fiscal, para o caminho do impulso.
- **s, hiato estimado só na parte consolidada do hiato do BC** · apoio; é a l.

Abri: `obsidian/ciclos/2026-10-27/atividade_rf.md` (inteiro); `obsidian/ciclos/2026-10-27/log.md` (entradas da atividade: rodada 1 por busca e o report final inteiro); `obsidian/ciclos/2026-10-27/ata_r2.md` (itens 5 e 7, por busca).
