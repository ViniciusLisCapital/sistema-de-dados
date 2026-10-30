# Feedback do agente fiscal sobre o Modelo Estrutural · 2026-10-30

Resposta literal do `fiscal-analyst` (Opus, modo ad hoc) ao questionário da frente C (passo C1b), a partir do report final do ciclo 2026-10-27. Só leitura dos arquivos do ciclo. Custo: 145k tokens.

---

**1. Onde o modelo complicou o trabalho**

O maior custo veio da âncora da regra. A (R) repassa a `rr_10a` à Selic um a um, e a (H) mede o aperto como `(Selic − meta) − rr_10a`. Com isso, o meu caminho da `rr_10a` virou, na prática, a central da Selic do P, e o hiato saiu idêntico nos três cenários: 0,13 em 4T26 e −0,52 em 1T28 (fiscal_rf, 3.1). O salto de 26/10 foi de +135 p.b. na NTN-B 10a, e só +22 p.b. vieram dos dois primeiros anos da curva real. O modelo leu esse prêmio como neutro. A PM mediu o efeito: o prêmio põe 0,76 a 1,00 p.p. na Selic de fechamento do modelo. Isso não pôde virar tempero, porque a (R) não tem peso livre na âncora. Fiquei com três coisas:
- uma nota de discordância na 3.1;
- dois itens da moderação (1 e 5);
- a escolha do caminho base 7,72 → 7,75 · 7,95 · … · 7,70, negociado com a PM sabendo que cada 0,1 p.p. ali é Selic do P.

No meu downside (consolidação), a Selic do modelo cai cerca de 0,65 p.p. a mais em 1T27 sem afrouxar o hiato. No upside, sobe a 14,33 sem apertar a demanda. Nenhum dos dois conta a história fiscal que escrevi.

O segundo custo é o canal do CDS. Na (F) só conta a variação do CDS. Em 26/10 o real andou 5,9 vezes o que o CDS explica no modelo, e em 05/10, 4,4 vezes. O choque foi precificado na inflação implícita (+0,9 p.p. num pregão) e no juro real, que a (F) não lê. Tive de argumentar ao câmbio um multiplicador × 1,2 em `F.b_fiscal`, só no upside, e retirei o × 1,5 que estava fora do intervalo. Um CDS que fica parado num nível mais alto não faz nada no modelo depois do primeiro trimestre.

O terceiro é a falta de uma variável fiscal no modelo. Afrouxamento ou consolidação só chegam ao modelo pelo CDS e pela `rr_10a`. O resto não entra:
- o impulso (+0,1 a −0,3 p.p. na base, até +0,5 no upside) e o parafiscal (~0,9 p.p. do PIB ao BNDES) viraram premissa ao atividade, que aplica 0,09 p.p. de hiato por ponto de impulso no tempero dele;
- os tributos sobre a gasolina e a subvenção ao diesel viraram premissa à inflação;
- o primário e a dívida não entram. A cauda de dominância (~10%, ou ~15% se o Copom subir em 09/12) não tem como ser simulada: a regra não deixa uma alta de juros depreciar o real.

Por fim, as convenções de medição. O CDS é medido no fechamento do trimestre e a `rr_10a` na média. A média de 4T26 já tinha 17 pregões a 6,99%, antes do 2º turno. Tive de traduzir o nível pós-eleição (8,05%) em média do trimestre, 7,75%, à mão, por G.

**2–5. Propostas, da mais importante para a menos**

| Proposta · equação/peça | Teste que decide | Efeito na tese deste ciclo |
|---|---|---|
| 1. Separar a `rr_10a` em parte de política (curva real de 2 a 5 anos) e prêmio (anos 5 a 10, ou a parte explicada por CDS e implícita), com peso livre na âncora · (R) `RR* + meta` e o neutro da (H) | Estimar a (R) e a (H) com as duas partes, 2006–2026. Mudar a especificação se o peso do prêmio na âncora tiver intervalo de 90% abaixo de 1, ou se o prêmio entrar com sinal negativo na (H) (custo de capital) | O caminho da `rr_10a` não muda. Muda o que ele faz: sai da Selic central até ~0,8–1,0 p.p. em 4T26–1T27 (a medida da PM), que hoje ela só desconta na distribuição. O hiato passa a diferir entre os cenários. A base pós-26/10 fica com Selic menor e hiato menor que hoje. Os −0,65 p.p. de Selic do downside encolhem |
| 2. Impulso fiscal como exógena da (H), principal fiscal (primário 12m sem precatórios mais o parafiscal) · (H) | Incluir o impulso na (H), 2003–2026. Entra se o coeficiente for positivo com intervalo fora de zero, ou se reduzir os 25 resíduos positivos do viés da (H) | O tempero do atividade passa para a central. Com o 0,09 dele, a diferença de hiato entre cenários é de centésimos (ordem de 0,03 a 0,06 p.p.; conta de ordem de grandeza, sem G). O efeito é pequeno, mas os cenários fiscais deixam de ser iguais no hiato |
| 3. Variação da inflação implícita de 10 anos (ou NTN-B 10a − Treasury 10a) na (F), mais a interação ΔCDS × vol implícita ou uma dummy eleitoral · (F), `F.b_fiscal` = 25,1 [19,5; 30,6] por desvio da ΔCDS (298,5 p.b.) | Estimar em 2006–2026 e olhar os trimestres de choque doméstico. Mudar se a implícita tirar poder do resíduo e a interação sair positiva com intervalo fora de zero | O × 1,2 do upside sai do tempero do câmbio e vira especificação. A PTAX do upside em 1T27 fica perto de 5,86 na central do cenário, contra ~5,78 hoje. A base mexe pouco: a ΔCDS dela é pequena. Eu passaria a ser principal da implícita |
| 4. Uma equação para o CDS, em função do Focus de primário e de dívida, mais o componente global | Regressão do ΔCDS em 2010–2026 sobre a revisão do Focus de primário e de DLSP e o componente global. Mudar se a revisão fiscal entrar com sinal e intervalo fora de zero | O CDS deixa de ser tese e vira endógena, e a minha tese passa a ser o caminho do primário. A central do CDS (140 → 125) sairia de uma conta, não de um caminho escrito por mim |

**6. Propostas da mesa que tocam o meu trabalho**

- **b** · apoio. É minha também: decide se o peso do CDS no estresse é tempero ou especificação.
- **c** · apoio. É minha: o choque de 26/10 está na curva local, não no CDS.
- **d** · apoio. O dólar contra emergentes contém o real, e isso inflou o componente "global" do CDS que usei com o externo.
- **f** · apoio. A interação ΔCDS × vol da proposta 3 depende de ter a vol implícita.
- **g** · apoio forte à versão "separar prêmio de neutro", ou ao menos a liberar o coeficiente. Sou contra suavizar a taxa de 10 anos: esconde o prêmio em vez de separá-lo.
- **h** · contra somar o CDS à regra se a proposta g separar o prêmio pelo CDS: o mesmo prêmio seria contado duas vezes. Apoio só como alternativa a g, e o teste da dominância pede o sinal livre.
- **j** · apoio. O impulso fiscal e o parafiscal são candidatos naturais ao viés da (H) (a minha proposta 2).
- **k** · apoio. É a metade (H) da proposta g.
- **o** · apoio. A `rr_10a` de 4T26 já tinha 17 de 60 pregões observados, e condicionar o primeiro trimestre ao dado parcial faz à máquina a conta que fiz à mão.
- **p** · apoio à parte do tributo sobre combustível. A MP 1.395 e a subvenção ao diesel são decisões fiscais que hoje chegam à inflação só como premissa minha.
- **s** · apoio às variáveis próprias para o fiscal e ao modelo de PIB com a demanda do governo (as minhas propostas 2 e 4). Indiferente ao hiato estimado só na parte consolidada.

Abri: `obsidian/ciclos/2026-10-27/fiscal_rf.md` (inteiro); `log.md` (seções "Rodada 1 · fiscal", "Rodada 2 · fiscal", "Report final · fiscal"); `ata_r2.md` (trechos sobre `rr_10a`, âncora e CDS, por grep).
