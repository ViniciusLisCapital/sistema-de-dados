# Feedback do agente externo sobre o Modelo Estrutural · 2026-10-30

Resposta literal do `externo-analyst` (Opus, modo ad hoc) ao questionário da frente C (passo C1b), a partir do report final do ciclo 2026-10-27. Só leitura dos arquivos do ciclo. Custo: 159k tokens.

---

**1. Onde o modelo complicou o meu trabalho**

O maior custo veio do sinal que a (F) dá aos meus canais. O que eu escrevo como cenário sai do modelo com o sinal trocado em três casos:

- **Desconto de PPC.** O cenário de Fed mais alto aprecia o real (PTAX 5,41 contra 5,43 no 4T26), porque o CPI cheio entra com peso 1 e pesa mais que o carry. Pelo mesmo canal, o meu `infl_us` base (~0,6 por trimestre), abaixo do padrão do simulador (0,91), põe +0,08 na PTAX do 1T28. Não pude temperar isso, porque a equação é do câmbio. Fiquei com uma nota de rodapé e uma leitura "contraintuitiva" na saída do modelo.
- **S&P 500.** O S&P do base sobe ~11% em seis trimestres, por lucro e não por apetite a risco, e vira o maior canal externo da PTAX: +0,13 no 1T28. Isso custou um tempero argumentado ao câmbio (`F.b_sp500`, intervalo de 90% de 0,98 a 2,79), um item da moderação e uma resposta sem dado, porque o banco não tem lucro nem valuation. O câmbio aplicou × 0,55.
- **Risk-off sem o CDS.** Com o CDS parado, o risk-off aprecia o real: 5,49 contra 5,52 no 1T27. Para o cenário fazer sentido, medi o componente global do CDS (12,4 p.b. por 1% de dólar EM) e negociei com o fiscal em duas rodadas e na moderação, até ele pôr o risk-off na cauda de alta (5,79 no 1T27).

O dólar EM contém o real, e o real saltou 8,8% em 26/10 por motivo doméstico. Tive de:

- escrever o caminho sem o salto;
- estimar o peso do real no índice (~0,07);
- mexer na probabilidade da cauda de alta (26/19);
- avisar que o placar do 4T26 tem de ler o índice descontado do real.

As convenções custaram G caro. O `infl_us` saiu de caminhos mensais do núcleo, dos alimentos e do Brent, por regressão. O `icbr_usd` é o último mês do trimestre e os grupos são a média, e os pesos dos grupos não estão no banco, então estimei a combinação.

O petróleo, o maior choque do ciclo (Brent +90% em 12 meses), não tem entrada no modelo: o caminho do Brent ficou fora dele, como tempero da inflação.

**O que me faltou por não ter variável da área.** Nada amarra os meus sete caminhos entre si:

- o `ffr` não responde ao `infl_us`;
- o `dxy_em` não responde ao Fed nem ao S&P;
- o agro não responde ao Brent.

Mantive a coerência dentro de cada cenário à mão, com regressões ad hoc. Faixa, centro e probabilidades são todos juízo meu, e o modelo não confere nada na minha tese. A faixa do posterior também não me serve: é incerteza dos pesos, não intervalo de previsão.

**2–5. Propostas**

| # | O que é | Equação/peça · coeficiente | Teste | Efeito na tese deste ciclo |
|---|---|---|---|---|
| 1 | Desconto de PPC com o núcleo do CPI e coeficiente livre | (F), termo de PPC (peso fixo em 1) | Reestimar a (F) de 2006 a 2026 com o núcleo no lugar do cheio e o peso livre; trocar se o peso livre ficar abaixo de 0,5 ou se o núcleo ajustar melhor fora da amostra | O cenário de Fed mais alto deixa de apreciar o real e o carry passa a dominar. Os +0,08 do `infl_us` no 1T28 encolhem. A nota sai; nada sai do tempero, porque eu não temperei esse canal |
| 2 | Dólar EM sem o real | (F), `F.b_dxy_em` (2,26; intervalo de 90% de 1,14 a 3,32) | Montar o índice sem o real (pesos da cesta ou resíduo da regressão diária) e reestimar; trocar se o coeficiente cair abaixo de 1,14 | O caminho e o placar passam a ler o mesmo objeto, e o ajuste de 26/19 na cauda some. O tempero de "coeficiente como teto" sai. Os +0,04 no 4T26 provavelmente caem |
| 3 | S&P ortogonalizado ao dólar EM, ou interação S&P × ΔCDS | (F), `F.b_sp500` (1,89) | Reestimar; se o efeito condicional sumir fora dos trimestres de crise, restringir | Os +0,13 na PTAX do 1T28 vão a ~0 ou a uma fração. O × 0,55 do câmbio sai do tempero e o que sobra entra na central. A PTAX base do 1T28 cairia algo como 0,06 a 0,13 |
| 4 | Brent como exógena minha, entrando nos monitorados (em reais, com defasagem) | (I) monitorados; nova chave `brent` | Δlog do Brent em reais, corrente e defasado, nos monitorados de 2006 a 2026; entra se for significativo e estável | O meu caminho (114 → 91) passa a mover o IPCA: mais alto no 4T26–1T27, depois devolvendo. A parte do petróleo no tempero da inflação vai para a central |
| 5 | Componente global do CDS como satélite: ΔCDS em função do dólar EM e do S&P | Nova peça ao lado da chave `fiscal` (o fiscal segue principal do doméstico) | Estabilidade de 2016–2026 contra 2006–2015; manter se o coeficiente do dólar EM for estável e o R² ficar acima de 0,5 (hoje 0,56) | O risk-off deprecia o real sem negociação (5,79 no 1T27 em vez de 5,49). O que hoje é cauda do fiscal vira o cenário em si |

Uma sexta peça vale menos: satélites do bloco externo (`infl_us` em função do núcleo e do Brent; agro em função do Brent e do dólar EM), que tornariam os meus caminhos reproduzíveis. Esse ganho é de disciplina; não muda número nenhum deste ciclo.

**6. Propostas já na mesa que me tocam**

- **b (não linearidade do CDS):** apoio a interação ΔCDS × nível. A PTAX do meu risk-off depende inteira de quanto o CDS anda; a dummy eleitoral não me toca.
- **c (implícita de 10 anos, ou NTN-B − Treasury):** apoio só a versão com o Treasury, que traz a ponta longa americana ao modelo e transforma o meu caminho do Treasury (hoje só um insumo ao fiscal) em exógena.
- **d (sinal do S&P e dólar EM sem o real):** apoio. É o maior canal externo da PTAX e o maior custo de negociação do ciclo.
- **e (PPC com o núcleo):** apoio. É a minha primeira proposta.
- **g (âncora `rr_10a` + meta):** apoio separar prêmio de neutro; o componente global do prêmio é insumo meu. Sobre o elo com o juro americano, sou indiferente: medi R² de 0,04.
- **h (regra de juros com câmbio ou CDS):** apoio com o CDS. Hoje os meus cenários quase não mexem na Selic (12,05 a 12,29 no 1T28), e um risk-off deveria chegar a ela.
- **o (primeiro trimestre condicionado ao dado parcial):** apoio. Os meus caminhos do 4T26 já usam outubro (Brent, T-bills); o modelo partir do mesmo dado parcial tira a incoerência.
- **p (monitorados com Brent):** apoio forte. É o maior choque externo do ciclo, e hoje ele chega ao IPCA só por tempero.
- **q (clima na alimentação):** indiferente. O El Niño ficou fora do meu agro por falta de dado; o termo seria da inflação.
- **s (variáveis próprias para o externo):** apoio, se forem satélites (Brent, componente global do CDS). Não apoio uma função de reação do Fed endógena: sem futuros nem calendário do FOMC no banco, ela seria estimada às cegas.

Abri: `obsidian/ciclos/2026-10-27/externo_rf.md` (inteiro); `log.md` (Rodada 1 · externo e Report final · externo); `ata_r2.md` (trechos dos itens 3 e 4 por busca); `PF.md` (linhas das minhas exógenas, por busca).
