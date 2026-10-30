# Feedback do agente de política monetária sobre o Modelo Estrutural · 2026-10-30

Resposta literal do `politica-monetaria-analyst` (Opus, modo ad hoc) ao questionário da frente C (passo C1b), a partir do report final do ciclo 2026-10-27. Só leitura dos arquivos do ciclo. Custo: 155k tokens.

---

**1. Onde o modelo complicou o trabalho**

O custo principal veio da âncora da (R). A Selic segue `rr_10a` + meta um por um, no mesmo trimestre (G `pm_sensibilidade`: +1 no `rr_10a` dá +1,00 na Selic, com o hiato igual). Por isso a central do ciclo acabou sendo, na prática, o caminho de `rr_10a` do fiscal. As duas revisões dele moveram a central em 0,1 a 0,5 p.p. sem nenhum dado novo de inflação ou atividade (P1 13,34 → P2 13,43 no 4T26). O prêmio eleitoral de 26/10 pôs 0,76 a 1,00 p.p. na Selic de fechamento (G `pm_r2_premio`). O modelo lê esse prêmio como neutro, e a (R) não tem um peso livre na âncora em que eu pudesse aplicar multiplicador. Precisei de um item na moderação (ata_r2, item 5) e de uma justificativa de que os regimes "não seguem o `rr_10a`".

Como a IS mede o aperto contra a mesma âncora, o hiato sai idêntico nos três cenários (diferença máxima de 0,01) e o IPCA quase não muda (5,32 a 5,36 no 4T26). As caudas do modelo viram só deslocamentos de nível da Selic (14,12 contra 12,92), e a política monetária não tem consequência dentro dele. A história do mapa 2.5 que contei em Q4 não é o que o modelo faz.

Fora a âncora, houve quatro custos:
- **A (R) não tem câmbio nem prêmio.** Com a PTAX a 5,50, o regime de alta (32%) e o tempero ii-a (+25 a +50 p.b.) foram montados à mão.
- **Selic de fechamento.** Ela é derivada de médias e é contínua. O 4T26 a 13,43 pede mais de um corte até 09/12 com a curva precificando alta, e o downside de 12,92 pediria −50 e −25. Corrigi pelo tempero ii-b (gradualismo).
- **Ponto de partida.** A média do 4T26 (13,48) ignora que 13,75 vale até 04/11. A Focus do modelo começa 0,11 a 0,30 p.p. abaixo da pesquisa de 23/10 em todos os trimestres, e esse erro entra na (R) pelo termo do desvio, que é por onde a central corta.
- **A faixa do posterior não serviu para a distribuição.** No 4T26 ela vai de 13,12 a 13,75 e não contém nenhuma alta. A distribuição inteira veio da mistura de regimes (`pm_r2_distribuicao`), com a mediana em 13,75 até o 2T27, acima da central.

**2 a 5. Propostas, da mais importante para a menos**

| Proposta | Equação/peça · coeficiente | Teste | Efeito na tese do ciclo |
|---|---|---|---|
| Liberar o coeficiente da âncora, ou trocá-la por um trecho mais curto (NTN-B 5a, termo 2–5a), ou separar o prêmio (CDS, implícita) do neutro | (R), âncora hoje sem peso próprio (passa 1 a 1) | (R) 2006–2026 com coeficiente livre e com as âncoras curtas, `br_interest_rate` e `pm_copom_reuniao`. Coeficiente bem abaixo de 1 (< 0,5) ou ganho fora da amostra com âncora curta muda a especificação | A central cai uma fração dos 0,76–1,00 p.p. que o prêmio pôs nela, proporcional a (1 − coeficiente). Ela se afasta ainda mais da minha mediana, mas por uma razão honesta. A justificativa "regimes não seguem `rr_10a`" sai do texto; a distância vira tempero ii-a declarado |
| A mesma decomposição na IS: o prêmio como custo de capital, não como neutro | (H), termo de aperto contra `rr_10a` + meta | IS 2006–2026 com o aperto medido contra a âncora sem o prêmio explicado pelo CDS. Peso significativo do prêmio no hiato muda a especificação | As caudas fiscais passam a mover hiato e IPCA. O upside de prêmio fica menos inflacionário pela demanda, e as caudas do modelo ganham conteúdo econômico em vez de só nível de Selic |
| Variação da PTAX ou do CDS na regra | (R), regressor novo | (R) 2003–2026 com a ΔPTAX ou a ΔCDS do trimestre. Coeficiente positivo, estável e com ganho fora da amostra entra na regra | Parte do ii-a (+25 a +50 p.b.) vai para a central no 4T26–2T27, e a assimetria (+0,26 no 4T26) cai. Esse é o tempero de maior peso que eu tenho |
| Estimar a regra no fechamento, com passo de 25 p.b., em vez de (média t + média t+1)/2 | Selic de fechamento derivada (erro médio de 0,12, máximo de 0,55) | 2006–2026: erro da derivada contra o de uma regra no fechamento com arredondamento, medido nos trimestres de virada de ciclo. Mudar se ele cair ali | O 4T26 iria para 13,50 ou 13,75 (hoje 13,43). O ii-b sai do tempero para a central e o downside do modelo se aproxima dos 13,50 que dei |
| Condicionar o 1º trimestre projetado ao que já se sabe: a Selic até 04/11 e a média parcial da Focus | Ponto de partida (Selic média e `focus_12m` do 4T26) | Backtest: erro do 1º trimestre com e sem condicionamento, e quanto ele move a Selic projetada nos dois trimestres seguintes | A central sobe no 4T26–1T27, e o item "a expectativa do modelo começa baixa" sai da lista de erros de Q4 |
| Faixa preditiva com o erro das equações, além do posterior dos pesos | Saída do simulador | Cobertura de faixas de 80% e 90% num backtest 2006–2026 | A central não muda. A minha mistura de regimes teria um termo de comparação; hoje não tem nenhum |

**6. Propostas já na mesa que me tocam**

- **g:** apoio. É a primeira linha acima e o maior custo do ciclo. Peço que a decisão sobre a âncora saia junto com a k.
- **h:** apoio, com teste fora da amostra. Se a reação for discreta, só ao balanço de riscos, o coeficiente sai instável e o canal deve ficar no tempero.
- **i:** apoio. Elimina um tempero (ii-b) que hoje corrige o próprio modelo.
- **k:** apoio, se usar a mesma decomposição do prêmio que a g. Com âncoras diferentes na (R) e na IS, a invariância do hiato some sem criar uma inconsistência nova.
- **o:** apoio. A Selic do 4T26 está fixa até 04/11, e a Focus do trimestre já existe.
- **m:** apoio. Os resíduos positivos da (E) chegam à (R) pelo desvio contra a meta, e foi por esse termo que a central cortou.
- **n:** indiferente a contra, como está. A implícita carrega prêmio (7,87% contra Focus de 4,53% em 23/10), e na (E) ela levaria à (R) o mesmo prêmio que a g tenta tirar. Só a apoio em variação e se o teste mostrar que a pesquisa segue o preço.
- **j:** indiferente. O viés da IS chega à regra só pelo hiato; não foi o que pesou neste ciclo.
- **f:** apoio, por tabela. Na rodada 1 a vol segurada no padrão deu PTAX de 5,24 no modelo contra 5,50 no mercado, e isso contaminou o canal câmbio → expectativa da minha central.

Abri: obsidian/ciclos/2026-10-27/politica_monetaria_rf.md (inteiro); log.md (Rodada 1, Rodada 2 e Report final · política monetária; Consolidação P1); ata_r2.md (itens 1, 5 e 8, por grep); PF.md (linhas da Selic, por grep).
