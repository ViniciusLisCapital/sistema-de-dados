# Pendências abertas — US Labor Market, depois da rodada de produtividade

Escrito em **2026-09-03**, ao fim da rodada que trouxe o release *Productivity and Costs*
(`prod2`) para dentro do relatório. O que está aqui é o que **não** ficou resolvido, mais
os erros que apareceram no caminho e que valem como aviso para a próxima sessão.

O que ficou pronto está documentado em [`../CLAUDE.md`](../CLAUDE.md) e no `CLAUDE.md` da
raiz; este arquivo não repete.

---

## 1. Nada foi confirmado num browser real

**É a pendência mais importante e a mais antiga.** Não há browser neste ambiente, então
todo o comportamento de tela foi verificado por harness (jsdom-ish, com `Plotly` e
`document` stubados). O harness afirma sobre `Plotly.react`/`relayout` e sobre a árvore de
elementos — não sobre o que o Chrome desenha.

O que vale abrir e olhar, em ordem de risco:

| o que | por que é o mais provável de estar errado |
|---|---|
| **Aba Productivity, gráfico de ciclos** | É o 2º gráfico da página cujo X **não é tempo** (o 1º é a curva de Beveridge). Ele tem `xaxis: {type: 'category'}` com rótulos longos (`Current cycle (2019 Q4 → 2026 Q2)`) — três categorias com texto grande num eixo estreito é exatamente onde o Plotly quebra ou sobrepõe rótulo |
| **Aba Productivity, tabela com Manufacturing expandido** | 6 linhas em 2 níveis, com o recuo significando **contenção e não soma**. Se o recuo ler como hierarquia aditiva, a nota não resolve |
| **Cabeçalho do gráfico com dois conceitos de produto** | O aviso é uma frase longa no subtítulo (`two output concepts plotted together — value added for…`). Pode estar quebrando o layout de três linhas |
| **Pills desabilitadas** | São 3 na aba nova (barras, "% do total", NSA) mais as 4 medidas da Tabela 6. Contraste do `i` sobre pill navy ativa já era pendência da rodada do JOLTS |
| **Árvore de 839 linhas do payroll**, rolada e expandida | Pendência da rodada anterior, não olhada |
| **Linha de população da CPS** na vista dessazonalizada (travessões) | Idem |

## 2. O especificador `%q` do Plotly não foi verificado, só evitado

O rótulo de trimestre do hover queria `%{x|%Y Q%q}`. O `%q` (trimestre) existe no
`d3-time-format` a partir da v3, mas **não foi encontrado no bundle `plotly-2.35.2.min.js`
por grep** (busquei `"%q"`, `formatQuarter`, `case "q"` e o mapa de especificadores — nada
casou, e o mapa está minificado de forma que não localizei).

Solução adotada: o rótulo é montado em JS por `fmtQuarter()`, a **mesma** função que rotula
a coluna da tabela, e o hover recebe `customdata`. Isso é testável e não depende do bundle.

**O que fica pendente é só a curiosidade:** se um dia houver browser, vale conferir se `%q`
funciona — se funcionar, `opt.fmtHover` pode sair e o `customdata` com ele (é um array de
strings por trace, custa payload). Não é urgente: o caminho atual está correto e coberto.

## 3. Dados carregados que a página não mostra

Três casos, todos **decisão** e não lacuna — mas todos custam confusão para quem abrir o
banco e não achar na tela:

- **A média anual da produtividade** (`periodicidade='anual'`, o `Q05` do BLS): **16.555
  linhas, 1947 → 2025**, só anos completos. A aba lê a grade trimestral. Mostrar exige uma
  pill, não dado novo. As duas leituras de variação **coincidem** nessa grade (é o mesmo
  número), então a pill teria 2 opções, não 3.
- **A razão `UO` do JOLTS** — *unemployed persons per job opening*, a série que o BLS
  publica ele mesmo: **308 linhas, 2000-12 → 2026-07**, SA. Ficou fora na rodada do JOLTS
  porque dependia da pesquisa domiciliar, que ainda não existia. **Agora existe**, e a aba
  Derived até usa a série como gabarito (invertida) da razão vagas/desempregado. Mostrá-la
  como série própria é uma linha de gráfico.
- **`classe` da produtividade** está gravada e não é dimensão: é função do setor (todos os
  trabalhadores nos cinco primeiros, só empregados nas não financeiras). Está no cartão de
  definição do setor, não numa pill — e isso está certo. Só não confundir com um seletor
  que falta.

## 4. O que não foi carregado, e o que cada um custaria

- **Claims semanais** — seria a primeira grade **semanal** do schema. Tudo aqui é mensal, e
  a produtividade acabou de introduzir o trimestral; a semanal quebra a mesma coisa que o
  trimestral quebrou (rótulo de coluna, formato de hover, número de colunas), e a fábrica
  já está parametrizada para isso desde esta rodada. Fonte: `ETA 539` do DOL, não BLS —
  connector novo.
- **ECI** (Employment Cost Index) — trimestral, mesmo release slug family (`eci`), e o
  `connectors/us_agenda.py` já lista o slug. Seria a segunda tabela trimestral, e a mais
  próxima em forma da que acabou de entrar.
- **Produtividade total dos fatores** (survey `mp`, anual, divulgada em março) — **é outro
  release**, não uma extensão deste. 7,4 MB de arquivo. Só vale se a pergunta for
  decomposição de crescimento (capital vs. trabalho vs. TFP).
- **Produtividade por indústria** (survey `ip`, 40 MB) — é onde esta página poderia **cruzar
  produtividade com a árvore de 839 indústrias da CES**, que é o único cruzamento realmente
  novo que sobrou. Provavelmente o item de maior retorno da lista.
- **CES: produção/não-supervisionados** (tabelas B-6 a B-9, ganhos desde **1964** contra 2006
  dos *all employees*), **mulheres** (B-5) e os índices de difusão. É um `datatype` novo em
  `mt_ces._MEDIDAS`, sem encanamento novo.
- **CPS: cruzamentos demográficos** — 43 conceitos carregados de **68.630 séries**. Projeto
  próprio; nada na página consome.
- **Erros-padrão do JOLTS** — publicados separadamente
  (`www.bls.gov/jlt/jolts_median_standard_errors.htm`). Hoje a página diz em prosa que um
  movimento mensal numa indústria pequena está frequentemente dentro deles, sem mostrar o
  número. Carregá-los permitiria acinzentar movimento não significativo na tabela.

## 5. Um problema NOVO, achado ao verificar o calendário — e é de outra área

Ao conferir se algum outro grupo tinha duas entradas para o mesmo `reference_period` (a
forma que o `bls_prod` introduziu), apareceu **`bcb_credit_note`**, e ali a duplicata
parece ser **erro de dado, não a fonte**:

```
- {date: "2026-05-28", reference_period: "2026-04"}
- {date: "2026-07-01", reference_period: "2026-06"}   <-- suspeito
- {date: "2026-07-30", reference_period: "2026-06"}
- {date: "2026-08-28", reference_period: "2026-07"}
```

Não existe **nenhuma** entrada com `reference_period: 2026-05` no grupo, e há um vão em
junho. O padrão mais provável é que a divulgação de fim de junho escorregou para
**01/07**, e a regra `ics: {ref: {unit: month, lag: 1}}` derivou a referência do **mês da
divulgação** (julho − 1 = junho) em vez do mês que ela de fato entregou (maio).

**É a mesma classe de bug que a nota do `bls_jolts` documenta** ("derivar `reference_period`
de 'mês anterior ao da divulgação' erraria todas as entradas"), agora por um caminho
diferente: não uma defasagem estrutural errada, e sim **uma divulgação que atravessa a
fronteira do mês**.

Consequência medida: hoje não há falso alarme, porque a entrada de 30/07 dá a data esperada
certa e o desempate novo (item 7 abaixo) pega a mais recente. Mas **2026-05 nunca aparece
como período esperado**, então se as tabelas de crédito tivessem parado em abril, a checagem
de frescor **não teria acusado** entre 01/07 e 30/07.

**Antes de corrigir**: confirmar contra o feed ICS do BCB qual foi a data real da divulgação
de maio. Se ela existe e está faltando no YAML, é uma entrada a acrescentar; se a de 01/07
*é* ela, é só trocar o `reference_period` para `2026-05`. Não mexi porque é outra área e
exige a fonte ao vivo.

## 6. Três erros meus nesta rodada, e o que cada um ensina

Ficam registrados porque dois deles podem se repetir de novo por descuido.

**(a) Inverti a atribuição da precisão, e escrevi isso em três lugares antes de medir.**
Afirmei que o arquivo do BLS traz o índice com 1 decimal e que por isso recontar a variação
erra. **Está errado**: o arquivo traz o índice com **3 decimais** (exatamente a precisão que
a nota (5) das tabelas diz que o BLS usa) e as variações com 1. Recontar do arquivo concorda
com o publicado em **0,0500 p.p. no máximo, nunca acima** — o resíduo é o arredondamento da
*taxa*, não do índice. Quem erra 1,35 p.p. é recontar do índice **impresso no PDF**.

Corrigido no docstring do ETL, no do `prod_tab.py` e na nota da aba. A lição: a hipótese
plausível ("a fonte publica pouca precisão") era falsa, e custou nada medir —
`value.map(lambda v: len(str(v).split('.')[1]))` responde em uma linha. **Meça antes de
escrever a explicação.**

**(b) Copiei os literais da Tabela 1 na linha da Tabela 2 no teste.** As seis primeiras
colunas coincidem entre *business* e *nonfarm business* na leitura anual, e as duas últimas
não (9,2 e 5,0 contra 8,8 e 4,7). O teste reprovou em 2 de 24 células — o dado estava certo,
o gabarito não. Comentário deixado no ponto, porque é uma armadilha de leitura de PDF: duas
tabelas quase idênticas lado a lado.

**(c) Um script de patch reaplicou 3× e duplicou um bloco do `CLAUDE.md` da raiz.** O texto
de substituição **continha a própria âncora** (eu inseri o bloco novo *antes* do bloco
antigo, mantendo o antigo no `depois`), então cada re-execução do script — e ele rodou 3
vezes por causa de âncoras erradas nas trocas seguintes — inseriu outra cópia. Reparado
apagando as duas primeiras (50 linhas).

**Regra para os próximos patches por script**: se o `depois` contém o `antes`, o patch
**não é idempotente** — ou faça a âncora ser algo que desaparece na troca, ou verifique
antes se a marca do bloco novo já existe e saia sem fazer nada. E rode as trocas todas num
único `write` no fim, não uma por vez, para uma âncora errada no meio não deixar o arquivo
meio-editado.

## 7. Mudanças que fiz fora da área e que valem revisão

Duas, ambas pequenas e ambas em código compartilhado:

- **`connectors/bls.py`**: `Q05` (média anual das pesquisas trimestrais) entrou em
  `_AGGREGATE_PERIODS` e ganhou mapeamento em `_to_date` (→ 1 de janeiro, como `M13`/`A01`).
  Antes, a linha era descartada por `dropna` porque o código era desconhecido — **mesmo
  resultado por acidente**, e `include_aggregates=True` não trazia a média anual de jeito
  nenhum. Nenhum consumidor usava `include_aggregates=True` (conferido por grep), então o
  comportamento default de todos os outros scripts não mudou.
- **`domain/release_calendar/sync.py`**: o desempate de `status()` era `>` estrito no
  `esperado`; passou a desempatar pela **data de divulgação** quando o esperado empata. Sem
  isso, um grupo com duas divulgações do mesmo período (o `bls_prod`, e possivelmente o
  `bcb_credit_note` do item 5) ficava mostrando a divulgação **preliminar** depois de a
  revisada sair — imprimia "28 dias desde a divulgação" no dia da divulgação. O veredito
  nunca mudava, só o metadado exibido.

## 8. Estado do repositório

Nada foi commitado. **19 arquivos** entre modificados e novos nesta rodada:

```
novos       domain/db/us/labor_market/mt_produtividade.py
            analytics/us/labor_market/prod_tab.py
            tests/test_produtividade.py
modificados analytics/us/labor_market/{report.html,generate_report.py,CLAUDE.md}
            tests/test_labor_market_us_js.js
            connectors/bls.py
            domain/db/CLAUDE.md · domain/dashboards/manifest.yaml
            domain/release_calendar/{calendar_2026.yaml,sync.py}
            jobs/update_us.py
            CLAUDE.md · analytics/CLAUDE.md · .claude/rules/lis-dashboards.md
movidos     prod2.pdf e empsit.pdf da raiz -> analytics/us/labor_market/referencia/
```

Suítes na última execução: `test_labor_market_us_js.js` **389/389**,
`test_produtividade.py` **47/47**, `test_jolts.py` **51/51**,
`test_dashboard_status.py`, `test_release_calendar_js.js` e
`test_dashboard_procedimentos.py` todos verdes. **7 mutantes testados, 7 pegos.**

O relatório foi gerado por `status.gerar('us_labor_market')` (**93,7 s**, stamp gravado) e o
calendário regerado depois — 30 grupos, 12 dashboards, 129 dependências.

---

## Ordem sugerida para retomar

1. **Abrir o relatório num browser** e olhar os 6 itens do item 1. É o que nenhum teste
   substitui, e a lista só cresce a cada rodada.
2. **Confirmar a data real da divulgação de maio do crédito** (item 5) e corrigir o YAML.
   É o único problema aqui que pode esconder um dado atrasado.
3. **Mostrar a razão `UO` do JOLTS** (item 3) — o dado já está no banco e a página já a usa
   como gabarito; é a menor entrega com valor da lista.
4. Depois disso, **produtividade por indústria** (`ip`) é o próximo dado com pergunta nova:
   é o que permite cruzar produtividade com a árvore da CES.
