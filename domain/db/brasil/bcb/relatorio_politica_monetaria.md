# Relatório de Política Monetária — o que a fonte permite

Levantado ao vivo em 2026-08-25, baixando e lendo as **109 edições** que a API do BCB devolve
(1999-06 → 2026-06, sem buraco). O relatório se chamava **Relatório de Inflação (RI)** até a edição
de 2024-12 e virou **Relatório de Política Monetária (RPM)** em 2025-03; é o mesmo documento.

Consumidores: [`_rpm_projecoes.py`](_rpm_projecoes.py) (sincronização + parsing),
[`pm_copom_projecoes.py`](pm_copom_projecoes.py) (a tabela, junto com os comunicados),
`connectors/bcb_rpm.py` (listagem de edições + download).

Companheiro deste arquivo: [`copom_comunicados.md`](copom_comunicados.md), a mesma coisa para o
comunicado de decisão.

---

## Por que o relatório e não só o comunicado

| | Comunicado | Relatório |
|---|---|---|
| Quando sai | dia da decisão | 7 a 28 dias depois, última semana de mar/jun/set/dez |
| Frequência | 8 por ano | 4 por ano |
| Projeções que publica | 2 ou 3 períodos escolhidos | o **caminho trimestral contíguo inteiro**, 6 a 15 trimestres |
| Cenários | 1, às vezes 2 | 2, às vezes 3 |
| Desde quando tem número | ~2010 | **1999-06**, a primeira edição |

O ganho não é redundância: é que o relatório publica o caminho contíguo, então o ponto a 6 trimestres
à frente — a aproximação do horizonte relevante — **existe em toda edição desde 1999**, enquanto o
comunicado só o dá de 2020 em diante.

## Listagem de edições: existe, e é uma chamada

`api/servico/sitebcb/rpm/ultimas?quantidade=500&filtro=` devolve as 109 edições com data de
publicação e URL do PDF. A coleção irmã `ri` do mesmo endpoint é **subconjunto** (para em 2024-12) —
não serve. Descoberto por tentativa: `relatorioinflacao`, `relatoriopoliticamonetaria` e variantes
dão 400.

Isso resolve a descoberta do **relatório**, não a do **anexo estatístico xlsx** — a listagem não diz
nada sobre o anexo, e nem toda edição tem (só de 2021-09 em diante). Por isso a enumeração de URLs
do `AnexoRPM` continua existindo.

## Qual reunião condiciona cada edição

A **última reunião anterior ou igual à data de publicação**. Não é heurística de proximidade: o
relatório declara o vínculo no texto — *"a taxa básica de juros permanecerá inalterada em 17,5% a.a.,
valor decidido pelo Copom em sua última reunião, nos dias 19 e 20 de junho"* (RI de jun/2000). Medido
nas 109 edições, a distância é sempre de **7 a 28 dias** e não há um único caso ambíguo.

O número da reunião vem de `bcb_copom.calendario_reunioes()`, que lê a listagem de **atas** — 260
reuniões, da 21ª (1998-01-28) à atual, incluindo as extraordinárias. É a única fonte do projeto para
o número das reuniões de 1998-2000, já que os comunicados só respondem da 48ª em diante.

O RI **tem** numeração própria na capa (`v. 2 n. 2 jun 2000` — volume conta anos desde 1999, número é
o trimestre dentro do ano), mas não serve de chave: é derivável da data de publicação, 1999 é exceção
(começa em n.1 em junho) e a API não devolve.

## Os dois formatos de tabela

**Leque (1999-06 → 2024-12).** Uma linha por trimestre, 7 números: os limites dos intervalos de
50%/30%/10% mais a projeção central. Duas ou três tabelas por edição, uma por cenário.

**Matriz (2025-03 →).** Igual à Tabela 1 do comunicado: linhas = índice (IPCA, livres,
administrados), colunas = trimestres. Não tem leque numérico no PDF — virou gráfico. Só o cenário de
referência.

## Cinco armadilhas, todas silenciosas

Nenhuma destas levanta exceção. Cada uma devolve número errado ou perde tabela sem avisar.

1. **A coluna central muda de lugar.** Até ~2016 são 6 limites e a central no **fim**; de ~2017 em
   diante são 3 limites, a central, e 3 limites — central no **meio**. Ler a posição errada devolve um
   limite do leque como se fosse a projeção: no RI de jun/2019 daria 3,4% e 4,2% onde a prosa da
   própria edição diz 3,0% e 3,6%. `_convencao()` decide por **simetria do leque** em torno do
   candidato, e decide **uma vez por tabela** — por linha as margens são de 0,05 contra 0,15 p.p. e um
   arredondamento inverte a escolha.

2. **O separador ano/trimestre muda sem aviso.** `2000 2` (espaço), `20102` (nada), `2002:3`
   (dois-pontos); e o trimestre é árabe até ~2016 e romano depois (`2019 II`). Um regex que só aceite
   espaço perde edições inteiras.

3. **O layout é de 2 colunas, e as duas extrações possíveis perdem casos diferentes.** Página inteira:
   uma linha de tabela na coluna direita sai com a prosa da esquerda colada na frente, e um regex
   ancorado no início da linha a descarta. Dividida na calha: uma tabela **larga**, que atravessa o
   centro (todas as de 2025-2026), é cortada no meio e perde metade das colunas. O `.md` guarda as
   duas variantes e o parser varre as duas.

4. **O título da tabela às vezes está numa fonte de subconjunto sem cmap legível.** O pdfplumber
   devolve códigos de glifo: `,QIODomR(cid:3)GR(cid:3),3&$` é "Inflação do IPCA" deslocado 29
   posições no ASCII. Em 2000-2002 é um deslocamento fixo, e `_decodificar_cid()` o descobre por
   busca (testa cada deslocamento, aceita o que produz uma palavra reconhecível). Em 2003-09 **não é
   deslocamento linear** — é subconjunto com cmap próprio, e não há caminho para o texto. A prosa da
   mesma página usa fonte normal e sai legível; só os títulos quebram, e o título é justamente onde
   vive a identificação do cenário. Sem tratar isso, ~40% das edições ficam sem cenário identificado.

5. **"Cenário de referência" trocou de significado**, igual nos comunicados: até ~2020 era o de juros
   **constantes**, de 2021 em diante é o com juros da Focus. Por isso a classificação nunca usa a
   palavra "referência" — usa o condicionamento declarado ("juros fixos de 19% a.a.", "expectativas de
   mercado", "taxa Selic da pesquisa Focus"). Quando duas legendas casam no mesmo contexto, vence a
   **mais próxima** da tabela: uma menção solta a "juros constantes" na prosa 14 linhas acima roubava
   a tabela do cenário de mercado.

## Quando a legenda não dá para ler

Fallback por **ordem**: no par de tabelas que cobre a mesma faixa de trimestres — as duas versões da
mesma projeção, uma por cenário —, a de juros constantes vem primeiro no documento. Medido nas 17
edições em que as duas legendas são legíveis: **17 acertos, zero violação**.

As linhas atribuídas assim ficam com `cenario_publicado` **nulo**, para a procedência mostrar que o
rótulo não foi lido, e a atribuição entra em `avisos`.

## Conferência cruzada que a fonte oferece de graça

Da 264ª reunião (2024-07) em diante, comunicado e relatório publicam o **mesmo** número para o
horizonte relevante da mesma reunião — o RPM de jun/2026 diz "no horizonte relevante de política
monetária, atualmente o quarto trimestre de 2027, a inflação projetada é 3,7%", e o comunicado da
279ª reunião diz 3,7% para 2027Q4. Divergência aí acusa parser quebrado, não dado errado.

## Um terceiro cenário

O RI de set/1999 publicou **três** tabelas: juros fixos, expectativas de mercado e "IPCA com juros
decrescentes" — uma trajetória de queda arbitrada pelo BCB, que não é nem constante nem esperada pelo
mercado. Virou o valor `juros_decrescente` da coluna `cenario`. Só essa edição tem.

## O que fica de fora

- **O leque não é gravado**, só a projeção central — decisão explícita do usuário. Os limites de
  50%/30%/10% estão no `.md` de cada edição, se algum dia fizerem falta.
- **As projeções de outros índices** (INPC, IPC-Fipe, IGP-DI, IGP-M) que as edições dos anos 2000
  publicam ao lado do IPCA, por ano civil.
- **O anexo estatístico xlsx** (2021-09 em diante) tem a `Tab 2.2.1` e a `Graf 2.2.9`, esta última com
  o caminho trimestral e os percentis do leque em coluna própria. É fonte melhor que o PDF para as
  edições recentes, e não foi usada aqui porque o PDF cobre a série toda com um parser só.
