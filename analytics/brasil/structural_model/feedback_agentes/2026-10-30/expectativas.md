# Feedback do agente de expectativas sobre o Modelo Estrutural · 2026-10-30

Resposta literal do `expectativas-analyst` (Opus, modo ad hoc) ao questionário da frente C (passo C1b), a partir do report final do ciclo 2026-10-27. Só leitura dos arquivos do ciclo. Custo: 143k tokens.

---

**1. Onde o modelo complicou o trabalho**

A central do P2 ficou abaixo da aritmética da própria pesquisa, e eu tive de desenhar a distribuição em volta dela.

No 4T26 a (E) dá 4,17. As 16 pesquisas já feitas no trimestre têm média de 4,52. Para fechar em 4,17, as 46 a 49 restantes teriam de marcar 4,05, uma queda que aconteceu em 3,1% dos dias desde 2001. A faixa base tinha de conter a central, então virou 4,05 a 4,45, com só 14% de probabilidade, e P(up) ficou em 85%. A tese passou a dizer que a central é improvável.

A trajetória sem revisão da Focus de 23/10 fica 0,11 a 0,30 p.p. acima do P2 em todos os trimestres. Para ler upside como "a pesquisa revisar para cima a partir dela mesma", tive de usar essa trajetória como limite de cima da faixa. Ela saiu de um G próprio (xp_trajetoria_pesquisa), porque o modelo não liga a variável dele às medianas da pesquisa por período.

O viés da (E) (7 de 8 resíduos positivos desde 4T24, média +0,35) entrou como tempero permanente: E.e1 × 1,2 no cenário base, nos seis trimestres. Isso tem dois custos:
- **Ferramenta errada para o defeito.** O defeito é o nível da âncora (os longos da pesquisa estão em 3,50, não em 3,00), mas a única alavanca é a inércia e o peso da inflação. Zerar o viés pede um peso da meta de ~0,03, fora do posterior.
- **Uma rodada de negociação.** O e1 maior leva a Selic do 1T28 de 12,18% para 12,71%, e o pedido sobre `R.t3` só se fechou na moderação (item 8), como contagem dupla.

A etapa 1 quase não serviu para a minha variável. Com CDS a 205–210 no upside, a PTAX do modelo sobe R$ 0,21 a 0,36, mas a Focus só +0,00 a +0,06. A distância entre os cenários veio toda dos temperos. Pior: o prêmio fiscal entra na regra de juros pela `rr_10a`, a Selic vai a 14,33% no 1T27, e isso amortece a inflação e a Focus. No modelo, um choque fiscal acaba sendo quase neutro para a expectativa. Na pesquisa, choques assim a fizeram subir.

O salto da implícita (+1,25 p.p. em 5 dias úteis, o maior desde 2006) não tem termo na (E). Medi os oito episódios num G (xp_r2_episodios) e usei a metade da mediana como tempero.

**2–5. Propostas**

| # | O que é | Equação · peça · coeficiente | Teste que decide | Efeito na tese deste ciclo |
|---|---|---|---|---|
| 1 | Âncora livre: quebra no peso da meta, ou âncora na Focus de t+3 em vez de `meta_12m` (item m) | (E), o termo (1 − e1 − e2)·Meta | Reestimar em 2002–2016 e 2017–2026, e com peso da meta variável no tempo. Comparar o erro de um passo fora da amostra em 4T24–3T26: mudar se cair mais de um terço e o viés de +0,35 sumir | Central para cima em todos os trimestres. A melhor referência que tenho é a rodada com E.e1 × 1,2 (viés para +0,19): 4,33 a 3,88, ou +0,16 a +0,33 sobre o P2. O tempero (i) do base passaria para a central, e a assimetria de 4T27 e 1T28 cairia de ~+0,35 para perto de zero |
| 2 | Partir do trimestre corrente com a média parcial já observada das pesquisas (item o) | Ponto de partida da projeção de `focus_12m` | Backtest 2002–2026 com o corte no mesmo ponto do trimestre: erro do 1º trimestre projetado e de h = 2 a 4, com e sem a média parcial. Mudar se o erro cair em h = 1 sem piorar em h ≥ 2 | 4T26 de 4,17 para perto da trajetória sem revisão (~4,45–4,47, +0,3 p.p.). Pela inércia (e1 0,58), uma parte passa a 1T27 e se dissipa até 2T27–3T27 (o tamanho exato ainda precisa ser medido). A evidência 1 de Q4 deixa de ser tempero, e P(up) do 4T26 sai de 85% para algo perto de equilibrado |
| 3 | Variação trimestral da implícita de 2 anos (ou o desvio dela contra a Focus 24m) como regressor (item n) | (E), termo novo | 2006–2026. Mudar se o coeficiente for positivo com o intervalo fora de zero e os resíduos de 4T21 e 1T25 caírem | 4T26 a 2T27 para cima, na ordem dos episódios (Focus 12m com mediana de +0,28 em 45 dias úteis), ou seja +0,1 a +0,3. Os temperos (ii) 1 e 2 passariam em grande parte para a central. Custo: a implícita vira exógena e precisa de um principal com caminho |
| 4 | Multiplicador direto no peso da meta (e3), sem mexer na inércia | (E), parametrização e ferramenta de tempero | Estimar e1, e2 e e3 sem impor soma 1. Se a soma ficar dentro do intervalo, a restrição pode ficar, e o tempero de "âncora fraca" passa a atuar só no e3 | Central igual. O tempero fica limpo: o upside sai de uma âncora mais fraca, e não de e1 × 1,2 com e2 × 1,3, que também alongam a persistência |

**6. Propostas na mesa que me afetam**

- **b (F), não linearidade do CDS:** indiferente. Mesmo um choque de câmbio grande chega à minha variável só pelo e2 de 0,16. No upside, PTAX +0,36 deu Focus +0,06.
- **c (F), implícita de 10 anos:** apoio, com uma condição: que seja coordenada com a proposta n. Uma curva de implícita com dois vértices no modelo (10 anos na F, 2 anos na E) precisa de caminhos coerentes e de um principal só.
- **g (R), âncora `rr_10a` + meta:** apoio separar o prêmio do neutro. Hoje o prêmio fiscal sobe a Selic 1 a 1, e o upside fiscal sai quase sem efeito na expectativa (Selic a 14,33% no 1T27, Focus +0,06). Isso vai contra o que a pesquisa fez depois dos saltos de preço.
- **h (R), regra com câmbio ou CDS:** contra se entrar sem g. Seria mais um canal que faz o choque fiscal desinflacionar no modelo; com g, indiferente.
- **m, n, o:** são minhas. Apoio, na ordem da tabela (1, 3, 2).
- **r (I), âncora por componente:** apoio com uma condição: as expectativas por grupo precisam estar amarradas à (E) do cheio. Duas medidas de expectativa livres podem se contradizer sem nada avisar. A vantagem é que o sinal de serviços longos (2028 +0,15, 2029 +0,10, com o cheio parado) entraria no modelo em vez de ficar como tempero.

Abri: obsidian/ciclos/2026-10-27/expectativas_rf.md; log.md (Rodada 1, Rodada 2 e Report final · expectativas); ata_r2.md (trechos dos itens 5 e 8, por busca); PF.md (seção de expectativas).
