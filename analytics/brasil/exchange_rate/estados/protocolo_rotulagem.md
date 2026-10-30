# Protocolo de rotulagem — estados do câmbio USD/BRL

Piloto com **um rótulo por pregão** (Q0 a Q4), de 2006-01-02 a 2026-10-28. O rótulo serve de gabarito
para a fase 2, que vai testar se as métricas de mercado recuperam os estados. Por isso ele foi feito
**a partir de notícias e de narrativa retrospectiva, sem olhar as métricas**. As definições abaixo já
incorporam as decisões do usuário de 2026-10-29.

## O que foi usado e o que não foi

- **Usado:** notícias da época e análises retrospectivas (WebSearch/WebFetch), cada trecho com ao menos
  uma URL; e a PTAX de venda, só para conferir se o dia era pregão e a direção do câmbio.
- **Não usado:** vol implícita, cupom cambial, CDS, juros, `Quadrantes cambio.xlsx` e os arquivos da
  classificação antiga por regra. Se fossem olhados, o modelo da fase 2 só reaprenderia a regra de quem
  rotulou.
- Algumas datas de início ou fim de processos (Q4) foram ancoradas na PTAX quando as notícias davam o
  tema mas não o dia (anotado na `nota` de cada linha: D01, D23, D30 e D28b). Isso é permitido pela regra,
  mas faz desses limites os menos independentes do câmbio.

## Os estados

| estado | data do evento | resultado | rotulado? |
|---|---|---|---|
| Q0 | — | — | sim, por exclusão: todo pregão sem trecho |
| Q1 | conhecida | incerto | sim, em três fases |
| Q2 | desconhecida | desconhecido | sim |
| Q3 | conhecida | conhecido | **não** (ver abaixo) |
| Q4 | desconhecida | esperado | sim, com direção |

- **Q0 — sem estado.** Nada relevante em curso.
- **Q1 — data conhecida, resultado incerto.** Eleição, anúncio fiscal com data, Copom/Fed com aposta
  dividida, tarifa com data marcada, votação com data. Três fases, cada uma numa linha:
  - `antes`: da primeira notícia que liga o evento ao risco de mercado ou de câmbio até o pregão anterior
    ao evento. O padrão é no máximo ~3 meses antes. Numa eleição o `antes` pode ir **até 6 meses** quando
    as notícias mostram o câmbio reagindo às pesquisas;
  - `evento`: os 1–3 pregões em que o resultado fica conhecido; evento em fim de semana ou à noite (Copom,
    FOMC fora do horário da PTAX, apurações) conta a partir do primeiro pregão seguinte;
  - `depois`: a absorção, até as notícias pararem de tratar o assunto como motor (tipicamente até 10
    pregões).
  Um Q1 sem drama pode ter só `evento`, ou só `antes` + `evento`. As fases não são forçadas.
- **Q2 — data e resultado desconhecidos.** A surpresa pura. Do primeiro pregão com a notícia até o fim
  da absorção, **no máximo ~10 pregões**. Um choque que dura mais segue o padrão gatilho → processo: Q2
  nos 10 primeiros pregões e Q4 com a direção do choque no resto (linha com sufixo `p`).
- **Q3 — data e resultado conhecidos.** Calendário de fluxo, como a saída sazonal de fim de ano e os
  vencimentos. **Não é rotulado**: na fase 2 ele entra no modelo como dummy de calendário de
  novembro–dezembro. No rótulo diário ele aparece só como marca de sobreposição, na mesma janela de
  novembro–dezembro.
- **Q4 — data desconhecida, resultado esperado (processo).** Um ajuste que todos esperam, mas sem data.
  Começa quando as notícias estabelecem a direção como consenso ("deterioração fiscal", "rebaixamento é
  questão de tempo", "chance de impeachment subiu"). Termina quando o desfecho acontece e o mercado segue
  em frente, ou quando a direção se inverte. A direção é obrigatória: `↑ dólar` ou `↓ dólar`.

**Direção** de um trecho é a do desfecho que o mercado esperava ou que se materializou: `↑ dólar`,
`↓ dólar` ou `sem direção`. Ela descreve o choque ou o resultado, **não a variação líquida da PTAX no
trecho**. Um Q2 inclui a absorção, que costuma devolver parte do movimento. No desmonte do carry do iene
(D17, ago/2024), por exemplo, o dólar sobe até 05/08 e fecha o trecho em queda. Em 16 dos 193 trechos o
sinal da PTAX no trecho contraria a direção. Quase todos são `depois`, eventos de variação próxima de
zero, ou a cauda `p` de um choque longo em que a absorção já tinha começado (A01p, C23p, D31p).

O `antes` de um Q1 costuma ser `sem direção`. Quando as notícias já davam o resultado como consenso, ele
recebeu a direção esperada. Foi o caso do 2º turno de 2018 (C21a), da cessão onerosa (C27a) e da 2ª
eleição grega (B11a).

## Casos de fronteira — decisões do usuário (2026-10-29)

1. **Tendência de fluxo, carry ou dólar global** é **Q4** quando as notícias tratavam a direção como
   consenso. São A23 (guerra cambial de 2010), B01 (2011), C40 (2021), D01 (2022), D23 (2025) e D30
   (2026), todos Q4↓, e D12 e D32, Q4↑.
2. **Decisão com data marcada que surpreendeu, sem aposta dividida**, é **Q1 `evento`**. Os casos são os
   Copom de 31/08/2011, 29/10/2014, jan/2009, jan/2017 e mai/2020, e o FOMC de 18/09/2013.
3. **Rating esperado sem data** é o **desfecho do Q4 em curso**, sem linha própria. A S&P de 30/04/2008
   (ex-A12) entrou no A05, que foi estendido até 02/05/2008. A S&P de 09/09/2015 (ex-B32) entrou no B28,
   e também a Fitch de 16/12/2015 junto com a saída de Levy (ex-B36). A Moody's de fev/2016 já estava
   dentro do B28.
   - Exceção: a S&P BBB- de 24/03/2014 (ex-B22) não tinha Q4 cobrindo. Com o `antes` da eleição recuado
     para março, ela ficou dentro do B23a.
   - O rebaixamento dos EUA pela S&P em ago/2011 (B04) continua Q2. É choque global, não rating do
     Brasil, e foi tratado como surpresa.
4. **Choque longo:** Q2 nos 10 primeiros pregões; o resto vira **Q4 com a direção do choque**. Q2 de
   11–12 pregões foram mantidos, porque a sobra de 1–2 pregões não forma processo: A04, A07, A11, B18,
   B34, C16, C29 e D16. Quando um Q4 de mesma direção já cobria a cauda, só o Q2 foi encurtado: A14
   (Lehman, dentro de A13) e C02 (China, dentro de B28).
5. **`antes` de eleição** vai até 6 meses quando há evidência de câmbio reagindo às pesquisas.
   - 2014 (B23a) recuou para 17/03/2014. Bloomberg e Reuters ligam o rali de bolsa e real à queda de Dilma
     nas pesquisas desde meados de março. São 6,6 meses antes do 1º turno, seguindo o exemplo do usuário.
   - 2018 (C19a) recuou para 19/07/2018, a primeira notícia que liga o câmbio à corrida (o centrão com
     Alckmin). Fica dentro de 3 meses.
   - 2022 e 2026: as buscas não acharam reação do câmbio a pesquisa antes do que já estava rotulado.
   - 2006 e 2010: sem drama, ficaram como estavam.
6. **Impeachment de 2016:** o Q4↓ (C03) termina no **afastamento, em 12/05/2016**.
   - O julgamento final (C07) e o Brexit (C08) ficaram fora do Q4.
   - O **tapering de 2013** foi partido em dois: B15a vai de 22/05 a 22/08/2013 e B15b de 19/09 a
     20/12/2013.
   - O intervalo em que a direção se inverteu, de 23/08 a 18/09, ficou com o programa de swaps (B18) e com
     o FOMC de setembro (B19a e B19b).
7. **Q3** é marcado em `sobreposicao` em **novembro e dezembro**, alinhado com a dummy da fase 2.
8. **Swaps do BC e IOF** são **Q2 só se foram surpresa**. Se eram esperados, ficam dentro do estado em
   curso.
   - Saíram: o IOF de 4% de out/2010 (ex-A26) e o IOF de derivativos de jul/2011 (ex-B02).
     - O IOF de 4% entrou no A23. Mantega tinha dito em 28/09 que "depois das eleições" todas as
       possibilidades estavam abertas, e a PTAX ficou parada.
     - O IOF de derivativos entrou no B03a. O BBVA escreveu "comes as no surprise".
   - Mantidos como Q2, com o motivo na nota de cada linha:
     - o IOF de 2% de out/2009 (A18), pela reação de bolsa e real;
     - o IOF de 6% de out/2010 (A27), pelo aumento de juros de surpresa da China no mesmo dia;
     - os swaps de 2013 (B18), que a LatinNews chama de "surprise announcement";
     - a sinalização de Tombini sobre reservas (B34);
     - os US$ 20 bi em swaps de 2018 (C17);
     - o decreto do IOF de 2025 (D25);
     - o IOF de mar/2008 (A11), que se sustenta pelo Bear Stearns.

## Regra de prioridade (aplicada por `rotular.py`)

Num pregão coberto por mais de um trecho, **o evento ganha do fundo**:

```
Q2  >  Q1 evento  >  Q1 depois  >  Q1 antes  >  Q4
```

No mesmo nível vence o trecho mais curto, que é o mais específico, e depois o que começou mais tarde.
Pregão sem trecho é Q0. Os Q4 são linhas longas, e os Q1/Q2 ficam dentro deles **sem recortar o Q4**.
Dois Q4 sobrepostos, como a cauda da guerra do Irã (D31p, ↑) dentro da rotação global (D30, ↓), também
se resolvem pelo mais curto.

O Q2 ficou acima do Q1 `evento` por causa de 04/10/2010, quando o IOF de 4% caiu no dia do 1º turno. Com
a decisão 8 esse IOF saiu, e hoje nenhum pregão tem Q2 e Q1 `evento` ao mesmo tempo. A ordem ficou como
regra para casos futuros. Todos os 193 trechos vencem ao menos um pregão.

## Sobreposição

No arquivo diário, `sobreposicao = 1` quando:

- o pregão é coberto por mais de um trecho (um evento sobre um Q4 de fundo, ou dois eventos); ou
- o pregão tem estado diferente de Q0 e cai em **novembro ou dezembro**, o Q3 da saída sazonal.

A coluna extra `ids_cobrindo` lista todos os trechos daquele dia. Com ela a fase 2 consegue separar o que
estava ao fundo. Os casos de sobreposição mais carregados, onde vale verificar se o modelo erra:

- **2008:** o Q4↑ da crise global (A13) traz o Lehman (A14, agora 10 pregões) e a eleição americana
  dentro, e o Q3 de novembro–dezembro por cima.
- **2015 a fev/2016:** o Q4↑ fiscal (B28) traz dentro:
  - o yuan e a China;
  - o orçamento com déficit;
  - o FOMC, Tombini e Cunha;
  - os desfechos da S&P, da Fitch e da Moody's;
  - o Q3 de 2015.
- **2016:** o Q4↓ do impeachment (C03), até 12/05, traz a votação da Câmara, a anulação de Maranhão e o
  afastamento.
- **2020:** os choques da Covid (C30 e a cauda C30p) e de Moro e o Copom de maio; depois o Q4↑ fiscal
  (C33); a eleição americana e a vacina, com o Q3.
- **2021:** o Q4↑ fiscal (C41) traz o 7 de setembro, o furo do teto e o Q3 de novembro–dezembro.
- **2024 a jan/2025:** o Q4↑ fiscal (D13) traz dentro:
  - o PLDO, o Copom 5×4 e os ataques ao BC;
  - o carry do iene, a superquarta e a eleição americana;
  - o pacote fiscal (Q1 nas três fases);
  - o Copom de +100 bps e o recorde de dezembro (Q2);
  - o Q3 de novembro–dezembro.
- **2025:** o Q4↓ do dólar global (D23) traz o Liberation Day, o IOF, a carta da tarifa de 50% e o
  tarifaço.
- **2026:** o Q4↓ da rotação global (D30) traz a guerra do Irã (Q2 e cauda Q4↑). Na eleição, o `depois`
  do 1º turno (D33c) se sobrepõe ao `antes` do 2º (D34a).

## Ressalvas

- **Cobertura das fontes.** As fontes são de sites de notícia abertos, e alguns links de jornal de 2006
  a 2010 são blogs ou agregadores que reproduzem a notícia. Confiança `baixa` quer dizer uma de duas
  coisas: não houve matéria ligando o evento ao câmbio, ou a fonte achada era fraca.
- **Consolidação das eras.** A rotulagem foi feita em quatro blocos (2006–10, 2011–15, 2016–21,
  2022–26) e consolidada.
  - O Q4 fiscal de 2015 foi emendado com a continuação de 2016 até 02/03/2016 (B28).
  - O Q4↑ fiscal de 2021 (C41) termina em 30/12/2021, porque em jan/2022 as notícias invertem a direção
    (D01).
- **Caudas `p` mecânicas.** As linhas Q4 com sufixo `p` herdam as datas e as fontes do choque e não têm
  notícia própria do início do processo. Em B06, a de setembro de 2011, a cauda **não** foi criada: os 5
  pregões restantes, 03–07/10, ficaram Q0, porque as notícias dizem que ali as vendas de swap do BC já
  invertiam a direção.
- **O fim da amostra.** O `depois` do 2º turno de 2026 (D34c) tem só 28/10/2026 porque a série acaba aí.
  Estender quando houver dado.
- **Proporção de estados.** O Q0 ficou com 44% dos pregões, não com os ~85% que a classificação antiga
  sugeria. O motivo é o Q4: os processos são longos por definição, e o usuário manteve as tendências como
  Q4 (decisão 1). Os pesos de classe da fase 2 devem partir desta proporção.
