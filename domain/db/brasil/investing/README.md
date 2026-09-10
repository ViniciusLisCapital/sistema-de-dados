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
