# Feedback do agente de inflação sobre o Modelo Estrutural · 2026-10-30

Resposta literal do `inflacao-analyst` (Opus, modo ad hoc) ao questionário da frente C (passo C1b), a partir do report final do ciclo 2026-10-27. Só leitura dos arquivos do ciclo. Custo: 153k tokens.

---

Respondo do ciclo 2026-10-27, sem dado novo e sem G. Os números vêm do `inflacao_rf.md`, do `log.md` e do `PF.md`.

**1. Onde o modelo complicou**

O maior custo veio de **monitorados**. O modelo põe o grupo em 1,37 p.p. no 4T26 e em ~1,0 p.p. (~3,8%) depois. A equação não lê petróleo, câmbio nem tributo, e a indexação tem o sinal trocado. Por isso não li essa central como informação. Toda a história de combustíveis ficou no tempero:
- +0,14 a +0,27 p.p. no upside;
- −0,16 no downside;
- −0,10 da desoneração, com um tamanho que é hipótese minha;
- ±0,10 da bandeira.

A IN-E1 saiu de fora do modelo. Para ele, uma PTAX 4–7% mais fraca dá no máximo +0,01 p.p. a monitorados. O repasse real passa pela paridade da Petrobras, e eu estimei 5% na bomba = +0,27 p.p. Também tive de explicar à mão a comparação com os administrados do Copom.

O segundo custo foi o **ponto de partida**. O modelo projeta o 4T26 do 3T26 fechado e ignora o que já saiu:
- O IPCA-15 de outubro (0,32%), com a energia do mês quase toda dentro, não entra.
- No r1, a Focus e a QPC implicavam 1,19–1,21% no trimestre (~5,21% em dezembro). O P2 põe 1,33% e 5,34%.
- A (E) põe a Focus do 4T26 em 4,17, contra 4,52 de média nas 16 pesquisas já feitas.

Estreitei a faixa do 4T26 à mão, mas não pude mexer na central.

O terceiro custo é a **âncora**. Pela minha medida, o `E.e1` × 1,2 do agente de expectativas soma +0,10 p.p. no 3T27 e +0,19 no 1T28. Eu acredito nisso para o cenário base, mas o multiplicador não é meu e a regra manda a força para a assimetria. A tese de 4,14% no 1T28 está baixa e eu sei disso, com assimetria de +0,15 a +0,17.

Há ainda três custos menores:
- **Alimentação:** o modelo trata os in natura (+13,0% em 12 meses) como inércia e câmbio. Como subordinado do IC-Br agro, pouco do que eu levo chega ao que move o grupo, porque a cesta não tem hortaliças.
- **Faixa do posterior:** ela mede só a incerteza dos pesos (5,15–5,53 no 4T26). Não há erro de previsão medido, então faixas e probabilidades foram inteiramente julgamento meu.
- **Repasse:** é linear, e um salto de 9,2% num pregão me levou ao × 1,5 em `ia3`/`ii4`, com o de bens industriais perto da borda do intervalo.

**2–5. Propostas, da mais importante para a menos**

Os efeitos na tese são ordem de grandeza: estimei por raciocínio, sem rodar o modelo.

| # | O que é | Equação/peça · coeficiente | Teste que decide | Efeito na tese deste ciclo |
|---|---|---|---|---|
| 1 | Brent em reais defasado um trimestre; tributo e subvenção sobre combustível como exógena com principal (fiscal); IPCA livre na indexação | (I) monitorados · `I.IM.im2` mais um coeficiente novo de petróleo | Monitorados trimestral, 2003–2026, com e sem Δlog(Brent×PTAX) em t−1 e o livre em t−1. Muda se o coeficiente do petróleo for >0 com o intervalo de 90% fora de zero, a indexação ficar positiva e o erro fora da amostra cair | A central sobe ~0,1–0,3 p.p. no 1T27–3T27 (Brent a 114) e devolve parte em 4T27–1T28 (Brent a 91). Uma parte dos +0,27 de combustíveis e dos −0,16 sai do tempero para a central. A desoneração ganha dono e tamanho (resolve o item 6 da ata). |
| 2 | Primeiro trimestre condicionado ao dado parcial: IPCA mensal já publicado, IPCA-15 e Focus semanais | Ponto de partida; (I) e (E) no trimestre corrente | Projeções pseudo fora da amostra, 2015–2026: erro do 1º trimestre com e sem o dado parcial. Muda se o erro cair de forma clara | 4T26 de 5,34 para ~5,2. A Focus do 4T26 sobe de 4,17 para ~4,5, o que soma ~+0,1–0,2 p.p. em 3T27–1T28 pela âncora. Parte da assimetria de expectativas vira central. |
| 3 | Erro de previsão por horizonte impresso junto da faixa do posterior | Saída do simulador (`ipca_12m`) | Erro de previsão do IPCA 12m em h = 1 a 6 trimestres, projeção recursiva 2012–2026 | A central não muda. Faixas e probabilidades passam a ser medidas contra um erro conhecido, e não só julgadas. |
| 4 | Âncora por componente | (I), as quatro âncoras | (I) com a Focus de cada grupo convertida para 12 meses à frente, 2021–2026 (amostra curta). Muda se melhorar o ajuste de serviços e alimentação | Serviços sobem (Focus de 2028 em 4,65) e alimentação cai (4,00). Saldo provavelmente pequeno e para cima, ~+0,1 no 1T28, com sinal incerto. |
| 5 | In natura separado, ou um termo de clima | (I) alimentação · `I.IA.ia2` | Alimentação 2006–2026 dividida em in natura e resto. Muda se o ajuste do resto melhorar e `ia2` subir. O clima pede série fora do F | O 4T26 fica parecido; 2T27–3T27 caem (reversão). Parte do downside de −0,12/−0,24 entra na central. |
| 6 | Repasse não linear | (I) · `I.IA.ia3`, `I.II.ii4` | Interação de ΔlogPTAX com (Focus − meta) ou com uma dummy de salto grande, 2003–2026 | Parte do × 1,5 (+0,03 a +0,18) passa à central em 2T27–4T27, ~+0,05 p.p. |

**6. Propostas da lista que me tocam**

- **b (CDS não linear):** apoio. A cauda de câmbio que uso viria do modelo, e não só do meu multiplicador de repasse.
- **g (âncora da Selic):** indiferente. Medi a NTN-B mais alta: ela move a Selic e não o IPCA dentro do horizonte.
- **j (viés da H):** apoio. É o teste da minha IN-E5: serviços acima do que o hiato explica, ou hiato medido baixo demais. Hoje a divergência com a atividade fica só como leitura.
- **l (hiato do placar):** apoio, desde que a (I) seja reestimada no mesmo hiato. Se não for, `I.IS.is2` lê outro objeto.
- **m (quebra na E):** apoio forte. É a minha maior fonte de assimetria; moveria ~+0,1 a +0,2 de 3T27–1T28 para a central.
- **n (implícita de 2 anos na E):** apoio. Sem ele, o salto de 26/10 não chega à pesquisa no modelo. Sobrepõe-se a m e a o; escolheria um dos dois pela evidência.
- **o (trimestre corrente):** apoio. É a minha proposta 2.
- **p, q, r:** apoio. São as minhas propostas 1, 5 e 4, nessa ordem de prioridade.
- **s (variáveis próprias para o fiscal):** apoio na parte que me toca, se tributo e subvenção sobre preços virarem uma exógena do fiscal. É a metade de governança da minha proposta 1.

Abri:
- obsidian/ciclos/2026-10-27/inflacao_rf.md (inteiro)
- obsidian/ciclos/2026-10-27/log.md (Rodada 1, Rodada 2 e Report final da inflação)
- obsidian/ciclos/2026-10-27/ata_r2.md (busca por inflação e IPCA)
- obsidian/ciclos/2026-10-27/PF.md (busca por IPCA e grupos)
