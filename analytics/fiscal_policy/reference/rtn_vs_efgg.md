# RTN vs. EFGG — duas métricas de despesa do Tesouro, propósitos diferentes

Diferenciação entre a RTN (já em `fisc_rtn`, ver `domain/db/brasil/tesouro/fisc_rtn.py`) e a EFGG
(Estatísticas Fiscais do Governo Geral, nova fonte identificada em 2026-08 para viabilizar o IEG — ver
`impulso_estrutural_IEG.pdf` nesta mesma pasta e "Pending" em `../CLAUDE.md`). Não são medidas
redundantes — respondem perguntas diferentes, do mesmo jeito que "acima da linha" (STN) e "abaixo da
linha" (BCB) já não reconciliam entre si no restante do relatório (ver Gotchas em `../CLAUDE.md`).

## Diferenças principais

| | RTN (`fisc_rtn`) | EFGG |
|---|---|---|
| Abrangência | Só Governo Central (Tesouro + Previdência + BC) | Governo Geral = Central + Estados + Municípios consolidado |
| Classificação | Rubrica orçamentária/programa (benefícios previdenciários, pessoal, "outras obrigatórias", discricionárias por função — saúde/educação/etc.) | Classificação econômica GFSM 2014 do FMI (remuneração de empregados, uso de bens e serviços, juros, subsídios, transferências, benefícios previdenciários/assistenciais, investimento) |
| Regime contábil | Caixa ("acima da linha" — valor pago/liberado) | Competência modificada (caixa p/ receita, competência p/ despesa) |
| Propósito original | Acompanhamento operacional do caixa do Tesouro | Comparabilidade internacional, harmonizada com o SNA 2008/IBGE — a base que o paper do IEG usa |
| Fonte primária | RTN (Resultado do Tesouro Nacional), Series Temporais API | SIAFI + Estados/Municípios via Siconfi, consolidado pela STN |

Os números de "despesa total" das duas **não batem entre si** — nem deveriam, dado o escopo e o
regime contábil diferentes. Não tentar reconciliar.

## Frequência da EFGG por arquivo/esfera (o ponto que importa para o IEG)

Confirmado ao vivo (2026-08, baixando os 4 xlsx reais da publicação trimestral mais recente —
Estatísticas Fiscais do Governo Geral, 2026 T1, publicada 2026-07-01, dados atualizados 2026-06-30):

| Arquivo | Esfera | Periodicidade | Defasagem | Cobertura confirmada |
|---|---|---|---|---|
| `demonstrativos_governo_central_orcamentario.xlsx` | Governo Central | **Mensal**, trimestral e anual | 1 trimestre p/ dados trim./anuais | 2006-01 → 2026-05 (247 colunas mensais) |
| `demonstrativos_governos_estaduais.xlsx` | Estados | **Trimestral** e anual (sem mensal) | 1 trimestre | 2010-I → 2026-I |
| `demonstrativos_governos_municipais.xlsx` | Municípios | **Trimestral** e anual (sem mensal) | 1 trimestre | 2010-I → 2026-I |
| `demonstrativos_investimento_governo_geral.xlsx` | Governo Geral consolidado (só investimento) | Mensal (Central)/trimestral/anual | 1 trimestre | 2010-I → 2026-I |

**Resposta direta à pergunta de frequência**: nenhuma dessas quatro fontes é anual. A pior
granularidade é trimestral (Estados/Municípios) — dá pra montar Governo Geral trimestral, que é
exatamente o que o paper do IEG usa (2010T1–2023T4, também trimestral). Governo Central sozinho está
disponível mensalmente, mas o agregado de Governo Geral fica limitado à cadência de Estados/
Municípios, ou seja, trimestral.

**Correção (checado via código, `domain/db/brasil/tesouro/fisc_efgg.py`)**: a suspeita inicial de que
Municípios atrasaria ~1 trimestre em relação a Central/Estados estava **errada** — era leitura
equivocada de uma coluna extra vazia ao final da planilha (placeholder do próximo trimestre, ainda não
publicado), não do trimestre corrente faltando. Confirmado extraindo os 16 códigos reais: Municípios
tem 2026-I completo, junto com Central e Estados — as três esferas fecham no mesmo trimestre, sem
defasagem entre si. Não há gargalo de ponta-solta nessa fonte (ao menos não observado nesta consulta).

## Validação de consistência (Central + Estados + Municípios = Governo Geral)

Somei investimento líquido (código GFSM 31) das três esferas para 2025-IV:

```
Central (out+nov+dez/2025, mensal agregado) = -1.107,59
Estados 2025-IV                             = 18.422,95
Municípios 2025-IV                          = 15.629,81
                                               ---------
Soma                                        = 32.945,17

Arquivo consolidado "Governo Geral" 2025-IV = 32.945,18   ✓ bate
```

Confirma que os três arquivos por esfera são somáveis sem nenhum ajuste de consolidação adicional —
dá pra montar o agregado de Governo Geral diretamente somando os três, célula a célula, por código
GFSM.

## Mapeamento IEG (Resende & Pires, Textos para Discussão nº16, FGV/Tesouro 2024) → código GFSM

Extraído direto do texto do paper (`impulso_estrutural_IEG.pdf` nesta pasta), não inferido:

| Categoria IEG | Multiplicador | Definição do paper | Código GFSM na planilha |
|---|---|---|---|
| Folha | 1,32 | "salários e vencimentos" — exclui contribuições sociais | 211 |
| Transferências | 1,46 | "gastos previdenciários e assistenciais" (não é o código 26 de transferências entre entes — esse é excluído para evitar dupla contagem) | 27 |
| Investimentos | 1,66 | "aquisição de ativos não financeiros" (bruto, não o líquido) | 311 |
| Outras despesas | 0,64 | resíduo = despesa primária ajustada − (Folha+Transferências+Investimentos) | 22+25+28 (residual) |

Despesa primária ajustada = gasto total **excluindo** consumo de capital fixo (23), juros (24) e
transferências/doações entre entes (26).

Fórmula: `IEG = 1,32·ΔF + 1,46·ΔT + 1,66·ΔI + 0,64·ΔO`, cada Δ = variação trimestral em % do PIB.

O paper confirma que a fonte usada é literalmente a EFGG: *"As séries de despesas primárias foram
provenientes do Resultado de Estatísticas Fiscais do Governo Geral, disponibilizadas pelo Tesouro
Nacional."*

## Links de download (sem autenticação, HTML puro — corrigido: não é SPA)

Testado com `curl` simples (sem Playwright/headless browser): a página já vem renderizada em HTML
puro pelo servidor (é Plone, não Angular — a suspeita inicial de SPA estava errada). Um conector real
é só `requests.get()` + regex/BeautifulSoup, mesma classe de esforço de `connectors/tesouro.py` ou
`connectors/tesouro_series_temporais.py`.

Padrão dos anexos: `https://thot-arquivos.tesouro.gov.br/publicacao-anexo/{id}` — o `{id}` muda a cada
nova publicação trimestral (não fixar). Página-mãe **é estável**: confirmado que
`tesourotransparente.gov.br/publicacoes/estatisticas-fiscais-do-governo-geral/2021/22` é o link
permanente citado na página-tema (`temas/estatisticas-fiscais-e-planejamento/estatisticas-fiscais-do-governo-geral`)
— mesmo com "2021/22" no path (slug antigo reaproveitado pelo Plone), ela mostra a publicação mais
recente (2026 T1 no momento desta checagem), o mesmo padrão de URL-fixa-conteúdo-sobrescrito das
tabelas especiais do BCB. Fluxo do conector: 1) baixar essa página fixa, 2) extrair os 4 hrefs atuais
via regex, 3) baixar os 4 xlsx, 4) ler pelos códigos GFSM fixos (211, 27, 311 etc. — não por posição de
linha, mesma abordagem já usada em `fisc_rtn.py`).

**Fragilidade real, não bloqueio**: é um link não documentado como API oficial — se a Tesouro
Transparente reorganizar o Plone, essa URL fixa pode mudar sem aviso. Mesma categoria de ressalva já
registrada para a Series Temporais API.

## Peças que faltam para completar o pipeline do IEG

- **Denominador PIB**: já temos `atv_pib_valores_correntes` (PIB nominal trimestral) no MySQL.
- **Deflator IPCA**: já temos via `analytics/inflation/data/ipca_bcb_series.csv` — o paper deflaciona
  as séries pelo IPCA antes de logaritimizar.
- **Dessazonalização**: o paper usa X-13 nas séries de despesa antes de calcular os multiplicadores —
  não precisamos repetir a estimação dos multiplicadores (já são constantes publicadas), só aplicar a
  fórmula do impulso à série observada, então X-13 não é estritamente necessário para replicar o
  indicador (a menos que quisermos re-estimar, o que o paper não recomenda sem ampliar a amostra).
