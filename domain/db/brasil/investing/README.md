# investing.com — fonte aposentada (2026-09-08)

Esta pasta alimentava `macro_brasil.cmb_risco_pais` (CDS Brasil 5Y, USD) a partir
de CSVs exportados à mão do investing.com. O loader foi substituído por
[`domain/db/brasil/bloomberg/cmb_risco_pais.py`](../bloomberg/cmb_risco_pais.py),
que lê um export da Bloomberg (`BRAZIL CDS USD SR 5Y D14`).

Os CSVs em `raw/` **não são lidos por nada** — ficam como registro do que esteve
no banco até 08/09/2026, e porque a comparação entre as duas fontes é o que
justifica a troca:

| | investing.com | Bloomberg |
|---|---|---|
| início | 2007-12-19 | 2001-10-12 |
| cobertura de dia útil | 99,32% | 100% de 2004 em diante |
| maior cotação congelada | **113 pregões** (121,65, abr–set/2008) | 3 pregões |
| dias sem variação, 2011+ | 2,1% | 0,2% |
| dez/2015 | ausente (23 pregões) | presente |

Nos 4.850 dias em que as duas se sobrepõem, apenas **13 valores coincidem**
(diferença mediana 2,14 bps, máxima 126,5). Não é defasagem: a correlação das
variações diárias é máxima em lag 0.

Detalhe completo no docstring do loader novo.

## Exceção provisória: 09/09 a 14/10/2026 (carregado em 2026-10-15)

Com a cota da API da Bloomberg estourada, os **26 pregões de 09/09 a 14/10/2026**
entraram na `cmb_risco_pais` a partir de `raw/cds_5y_brasil_2026_outubro.csv`
(investing.com), acrescentados por insert direto depois do último dia do export
Bloomberg (08/09) — o histórico Bloomberg não foi tocado. Nos 27 dias em que os
dois se sobrepõem (03/08 a 08/09) a diferença média é 1,5 bps e a máxima 5,3; na
emenda, 112,95 contra 112,395.

**Some sozinho no próximo export da Bloomberg**: o loader trunca a tabela antes de
carregar, então rodar `cmb_risco_pais.run()` com um xlsx novo em `bloomberg/raw/`
substitui esses 26 dias sem passo extra. Previsto para novembro/2026.
