# analytics/brasil/monetary_policy/ — Contexto para o Claude

O relatório **Política Monetária** (abas Condições, Projeções do Copom, Acompanhamento
Condicionais e Expectativas de Juros), e só ele.

**Desde 2026-09-24 esta pasta guarda só o relatório**, a pedido do usuário (*"se tem coisa aqui que
é usado no modelo agregado, tem de ser levado para lá"*). O que morava aqui e o relatório não usa
saiu para o Modelo Estrutural, que é quem ainda usa o modelo:

- a réplica do **modelo agregado do BC** (`modelo_painel.py`, `modelo_agregado.py`, os artefatos
  `modelo_*`, os PDFs do boxe e a comparação do modelo com a Focus na antecipação da projeção) →
  [`../structural_model/modelo_agregado/`](../structural_model/modelo_agregado/CLAUDE.md);
- a **Curva de Phillips em planilha**, o **teste do LSTM**, o **teste TVP** e o legado
  **`curva_juros`** → [`../structural_model/experimentos/`](../structural_model/experimentos/CLAUDE.md).

Três funções de leitura que a aba Condições usava do `modelo_painel.py` (`q`, `serie`,
`focus_anual`) foram **copiadas** para `dados.py`, e não importadas de lá: importar faria o
relatório voltar a depender do modelo.

Histórico rodada-a-rodada de como cada peça chegou ao estado atual vive no git log, não aqui.

## Como rodar

O relatório (o que o botão Regerar faz — a previsão só é refeita quando está atrás dos dados):

```powershell
uv run python -c "from analytics.brasil.monetary_policy.antecipa_copom import salvar; salvar()"   # previsão + backtest, ~15s
uv run python analytics/brasil/monetary_policy/generate_report.py   # HTML
node tests/test_monetary_policy_js.js                               # asserções do relatório
uv run python tests/test_antecipa_copom.py                          # previsão e backtest
```

| Módulo | O que faz |
|---|---|
| `dados.py` | `q`, `serie` e `focus_anual`: consulta SQL, série `date, value` e o painel anual da Focus. Cópia das do `modelo_painel.py`, de propósito (ver acima). |
| `condicoes_copom.py` | O conjunto de informação da última reunião contra o de hoje. Lê MySQL e o `domain/release_calendar/` na hora, não usa `data/`. |
| `antecipa_copom.py` | Antecipa a projeção do BC para o horizonte relevante da próxima reunião pelo delta da Focus. `salvar()` lê três tabelas e o calendário e grava `data/antecipa_*`. A comparação com o modelo agregado está em `../structural_model/modelo_agregado/antecipa_modelo.py`. |
| `condicionais.py` | `hiato()` e `selic()`: os condicionantes da projeção edição a edição, para a aba Acompanhamento Condicionais. Lê MySQL e, para as datas das reuniões, `condicoes_copom.todas_reunioes()`. |
| `projecao_rpm.py` | `montar()`: o caminho trimestral inteiro que cada edição do RPM projetou (IPCA desde 1999, livres e administrados desde set/2024) e o realizado ao lado, para as duas seções de baixo da aba Projeções. Lê `pm_copom_projecoes` (relatório, juros esperado), `inflc_agregados` e `inflc_meta`. |
| `expectativas_juros.py` | `montar()`: a pesquisa Focus e a curva DI semana a semana, reunião a reunião, para a aba Expectativas de Juros. `caminho_di()` lê o caminho de meta Selic de uma grade da curva, com a suavização da Bloomberg (`SUAVIZACAO`); `dias_uteis()` conta dia útil com o calendário da época do pregão. **O procedimento inteiro, com os números, está em [`caminho_selic_curva_di.md`](caminho_selic_curva_di.md)** — é para quem lê o método, não para o Claude. |
| `generate_report.py` | Lê `condicoes_copom.montar()`, as tabelas de projeção, `condicionais` e `data/antecipa_*`, e injeta em `report.html`. |

O teste de `condicoes_copom.py` roda junto: `uv run python tests/test_condicoes_copom.py`
(não toca no banco — varre o calendário e séries sintéticas). O de `condicionais.py` também:
`uv run python tests/test_condicionais.py`. E o de `expectativas_juros.py`:
`uv run python tests/test_expectativas_juros.py` (as duas últimas seções leem o banco). E o de
`projecao_rpm.py`: `uv run python tests/test_projecao_rpm.py` (~2 min, baixa o anexo de cada
edição; `--sem-rede` pula essa parte).

## Relatório HTML

`generate_report.py` + `report.html` → `reports/brasil/Monetary Policy.html`. Construído sobre
`analytics/report_structure/`. **`_reactPreserveX()` é o ponto de entrada de todo gráfico — não
chamar `Plotly.newPlot`/`react` direto.**

| Aba | Fonte | Estado |
|---|---|---|
| **Condições** | `condicoes_copom.py` — MySQL + `domain/release_calendar/`. Matriz 25 variáveis × 9 reuniões (aba default) | pronta |
| Projeções do Copom | `pm_copom_projecoes` × `pm_copom_reuniao` + `data/antecipa_*`; o caminho de cada edição do RPM por `projecao_rpm.py` | pronta |
| Acompanhamento Condicionais | `condicionais.py` — o hiato em cada edição do RPM (`pm_hiato_produto_vintages`) e o caminho da Selic da Focus antes de cada reunião (`expc_focus_copom`) | nome provisório |
| Expectativas de Juros | `expectativas_juros.py` — a Selic que a Focus espera (`expc_focus_copom`) e a que a curva DI precifica (`br_di_grade`), reunião a reunião | pronta |

**Seis abas foram removidas a pedido do usuário**, todas com os `_load_*` delas, para o payload
não carregar série que ninguém lê (a seção 13 do teste cobra isso nos dois sentidos): Cenários,
Decomposição, Taxa Neutra e Hiato do Produto em **2026-08-25**, Modelo BC — Agregado em
**2026-09-22** e o Apêndice em **2026-09-24** (ver abaixo). Os artefatos do modelo
moram hoje em `../structural_model/modelo_agregado/data/`, e **nada do relatório nem do teste JS os lê**.


### O Apêndice saiu em 2026-09-24

Pedido do usuário, ao ver na aba de status do calendário a lista de arquivos `modelo_*` que o
relatório declarava (*"Tudo isso aqui do Política Monetária ainda tem razão de ser?"*). Não tinha:
desde que o modelo saiu da previsão, o Apêndice era **documentação de um modelo que não alimentava
número nenhum na tela** — e era o único motivo de 9 artefatos, 2 tabelas (`pm_hiato_produto`,
`mt_caged`) e 2 dos 3 passos do Regerar (painel ~90 s, estimação ~240 s) continuarem declarados.

Saíram juntos: a aba (botão, painel, ~400 linhas de JS com `MODELO_ITENS()`/`renderModelo()`/
`renderAppendix()`, o CSS das equações), o `_load_info()` e o `_raio_eq5()` do gerador, as seções
16, 17 e 31 do teste JS, e do manifesto os 9 artefatos, as 5 tabelas que só o modelo lia
(`pm_hiato_produto`, `pm_hiato_produto_vintages`, `mt_caged`, `expc_focus`, `expc_focus_copom`) e os
passos `painel` e `modelo`. Entrou `diferenciais_juros`, que a aba Condições sempre leu e ninguém
tinha declarado. O card foi de 31 para 18 dependências.

**E o modelo ainda rodava escondido dentro da previsão.** `salvar()` chamava `backtest()` e
`antecipar()`, que simulavam o cenário de referência duas vezes por reunião, e o gerador descartava
o resultado (`delta_modelo`, `nivel_modelo`...). Agora `antecipa_copom` não toca no modelo, e o
passo `previsao` caiu de 55 s para **15 s** medidos, lendo só `expc_focus_periodo`,
`pm_copom_projecoes` e `pm_copom_reuniao`. A comparação que justificou o delta da Focus continua
reproduzível em `../structural_model/modelo_agregado/antecipa_modelo.py` — apagá-la apagaria a
medição.

No mesmo dia o próprio modelo saiu da pasta (ver o topo deste arquivo). As notas metodológicas das
duas abas restantes ficaram: usam a mesma classe `appendix-item`, mas não são o Apêndice.

As duas seções abaixo são história do Apêndice enquanto ele existiu.

### A seção "O modelo, equação por equação" (2026-08-25)

Primeiro bloco do Apêndice: dez notas expansíveis com as equações (1) a (9), mais como o **hiato** e
a **taxa neutra** são recuperados, e uma tabela dos parâmetros de variância que a Tabela 1 do boxe
não publica (`s_h`, `k₀₈`, `k₂₀`, `s_pi`, `k_pi`, `s_i`, `s_e` e o `σ(εʳ*)` calibrado).

**A prosa vive no script, não no HTML**, e é a única coisa aqui que não é preferência: cada equação
é escrita com o **coeficiente estimado no lugar do símbolo**, lido de `D.info.params` — reestimar o
modelo reescreve a descrição em vez de deixá-la envelhecer ao lado de números novos. Uma nota nova é
um objeto `{t, c}` novo em `MODELO_ITENS()`; o `<details>` em volta é montado por `renderModelo()`.
Dourado = coeficiente nosso, azul = estado latente. A seção 31 do teste cobra cada coeficiente na
tela contra o payload, inclusive os pesos implícitos (`1−α₁ᴸ−α₁ᴵ`, `1−θ₁−θ₂`), que não estão em
`params` e têm de ser calculados.

A nota antiga "Por que a equação (5) está fora, e o que isso custa" **saiu**: afirmava que a (5)
estava fora do modelo e que Fair-Taylor divergira por instabilidade genuína, e as duas deixaram de
valer. No lugar ficou uma nota de histórico que reconcilia a afirmação — um apêndice que se
contradiz é pior que um incompleto.

### A aba Modelo BC — Agregado saiu em 2026-09-22

Era a única aba do projeto em que **o modelo rodava no navegador**: `simular()` estava portado para
JS e re-resolvia as equações — inclusive o ponto fixo da eq. (5) — a cada mudança de input, com um
card por condicionante, horizonte selecionável e cenários guardados no `localStorage`. Saiu inteira,
a pedido do usuário: ~1.200 linhas de JS, ~165 de CSS, o painel HTML, os loaders `_load_motor()` e
`_motor_cfg()` (com `_copom_administrados()` e `_copom_hr()`) e as seções 19 a 30 do teste.

O que sobrou dela, e não é pouco: **o modelo continua estimado e continua no Apêndice**. As equações
saem escritas com o coeficiente estimado, a tabela de validação segue conferindo os 22 parâmetros
contra a Tabela 1 do boxe, e o IRF contra o publicado. O que deixou de existir é a interface de
cenário — não o modelo.

Se um dia voltar, três coisas valem uma releitura antes (as três foram bug uma vez, nenhuma tem
sintoma): `vals` guardava número exato e nunca a string arredondada de exibição, senão o cenário
default deixava de reproduzir o Python bit a bit; o choque `s^h` decaía por β₅ no buffer além do
horizonte, ao contrário de todos os outros inputs, que seguravam o último valor; e
`ini.selic`/`ini.pi_e` eram lidos **em t₀** (a defasagem que as equações usam) enquanto
`dflt.selic_ult`/`dflt.pi_e_focus` eram o **último valor publicado**, que já pode estar um trimestre
à frente — confundir os dois acusava em 11 dos 12 cenários. O código está no git, no commit da
remoção.

### A aba Condições: a matriz reunião a reunião (2026-09-22)

**Uma linha por variável, uma coluna por reunião** — as 8 últimas já decididas mais a
próxima. A célula é o valor que a variável tinha **no fechamento daquela reunião**, com o
período de referência impresso embaixo, e recebe cor só quando trouxe informação **nova**
desde a coluna anterior. Mais a agenda de divulgações até o corte, **filtrada ao que
alimenta uma das linhas** — o calendário inteiro tem relatório próprio.

A versão anterior (2026-08-25) era duas colunas: a última reunião contra hoje, com KPIs e
uma régua de saldo hawkish/dovish. As três coisas saíram a pedido do usuário; a mecânica de
corte, σ e cor **não mudou** — ela já era genérica, e passar de 2 para 9 cortes foi
generalizar `_valor_em()`, não reescrevê-lo.

**25 variáveis em quatro blocos**, com a especificação em `_spec()`:

| bloco | linhas |
|---|---|
| Inflação | **projeção do próprio BC no horizonte relevante**, IPCA 12m, núcleos (média de 5) mm3m anualizada, Focus para T/T+1/T+2, Focus no horizonte relevante, implícita de 2 e 10 anos |
| Atividade | IBC-Br 12m, Focus PIB T/T+1, PIB/consumo/FBCF em 4T/4T |
| Condições Financeiras | PTAX, juro real ex-ante de 2 e 10 anos (NTN-B), juro real de 2 anos pela Focus, crédito livre e direcionado (real, 12m) |
| Condições Externas | juro real americano de 2 e 10 anos, IC-Br Y/Y (era m/m até 2026-09-24), Brent |

**O ponto todo continua sendo a regra de corte, e ela não é sobre a reunião — é sobre a
natureza do índice de cada série.** Uma série de mercado ou da Focus é indexada pela data em
que o dado existiu: corte direto, e é por isso que essas linhas mudam em toda coluna (numa
reunião de meio de mês vale o pregão daquele dia, não o fechamento do mês). Uma série mensal
ou trimestral é indexada pelo **período de referência** e só é publicada semanas depois — o
IPCA de julho está no banco com data 01/07 e saiu em ~13/08, de modo que na reunião de 05/08
o Comitê ainda estava com o de junho. Ler o banco por `date <= reunião` daria julho, e **não
levantaria exceção nenhuma**: devolveria um número plausível do período errado. Medido no
mutante que faz isso: **65 asserções** caem.

O corte é `datetime(dia 2, 18:30)`, não a data. Três consequências que já custariam bug: o
horário decide o IC-Br (o de julho saiu às 14:30 de 05/08, o dia da 280ª — entrou por quatro
horas); no dia 2 antes das 18:30 a reunião em curso ainda é a *próxima*; e a coluna da
próxima reunião é cortada em **agora**, não no fechamento dela — afirmar o corte futuro seria
ler dado que ainda não existe.

O que a generalização exigiu, e cada item é a origem de um defeito silencioso:

- **A janela interna tem N+1 reuniões e a tabela mostra N.** A coluna mais antiga precisa de
  uma anterior para ter delta; sem ela a primeira coluna nunca receberia cor, o que seria
  propriedade da janela e não do dado.
- **Cor só onde `novo`.** Uma série trimestral repete o último número entre divulgações, e
  colorir a repetição afirmaria notícia onde houve silêncio — sem sintoma, porque o número
  repetido é plausível. `novo` é `pos` andar entre duas colunas, e o teste cobra que ele bata
  com a troca do período de referência.
- **"Sem dado novo" e "dado novo que não mudou nada" têm as duas fundo neutro** e precisam se
  distinguir: a célula repetida ganha lavagem cinza do CSS, e por isso ela **não** leva
  `style` inline — um `background:transparent` inline venceria o CSS e as duas voltariam a ser
  indistinguíveis. Há mutante para isso.
- **A lista de reuniões vem de DUAS fontes.** `pm_copom_reuniao` tem a história e o passo de
  Selic, mas só depois que o ETL roda — a 281ª (16/09/2026) já aconteceu e ainda não está lá.
  O calendário tem as datas e nenhum passo. A união dá a janela; o passo fica vazio onde só o
  calendário alcança, em vez de virar um zero inventado (parado é uma decisão).
- **Referência trimestral.** `_ref()` infere a frequência em vez de fixar mês: `2026-Q2`
  forçado a mensal devolveria um mês que não existe no índice trimestral e a linha sumiria. E
  a defasagem conta do **fim** do trimestre — o PIB do 2º tri sai ~3 meses depois de junho,
  não de abril.
- **Duas entradas para o mesmo período: vale a mais tarde.** Não é hipotético — o
  `bcb_credit_note` de 2026 carimba `2026-06` em 01/07 e de novo em 30/07, e a cadência do
  grupo mostra que a primeira é rótulo errado do ICS. Pegar a primeira poria o dado de junho
  disponível um mês antes de existir. O mesmo desempate entra no **ajuste da regra**: com a
  duplicata dentro, o erro máximo do grupo ia a **27 dias** e marcava como ambígua toda célula
  de crédito da matriz; sem ela, 2 dias.
- **O seletor traz só o rótulo da reunião.** O passo de Selic saiu dele em 2026-09-22, a
  pedido do usuário: ele já está na linha **Decisão** do cabeçalho, embaixo da própria
  coluna, e repetido na pill só alongava um rótulo que precisa caber nove vezes na mesma
  barra. O teste cobra as duas metades — fora da pill, e ainda na linha Decisão.
- **A agenda depende do corte REAL da próxima reunião**, não do corte da coluna. Como a coluna
  futura é cortada em agora, usar o mesmo campo deixaria a janela `[hoje, corte]` com ~zero
  dia e a agenda sairia **vazia sem erro nenhum**.

Decisões de série que vieram com as linhas novas:

- **A projeção do BC entra pelo COMUNICADO, nunca pelo relatório** (pedida em
  2026-09-22, acima do IPCA). O mesmo número da aba Projeções, com um filtro a mais, e as
  duas razões são independentes: o comunicado sai **no fechamento da reunião** e o
  relatório 7 a 28 dias depois, então só o primeiro estava na mesa daquele dia; e até
  2024-06 o horizonte relevante só existia no relatório, que é trimestral — misturar os
  dois põe no mesmo índice pontos separados por ~45 e por ~90 dias, e `_sigma` mede a
  variação por POSIÇÃO. Medido: mediana de espaçamento de **84 dias** com o trecho antigo
  dentro contra **45** sem ele, e a escala típica de uma variação dobra (**0,297 p.p.**
  contra **0,148**), o que apagaria pela metade a cor de toda a linha. De 2024-07 em
  diante o comunicado tem projeção em todas as reuniões, então o que se perde é história
  velha e o que se ganha é um índice em que uma posição é uma reunião.
- **E ela é a única linha cujo rótulo de referência NÃO identifica a observação.** O
  índice da série é a data do comunicado; o rótulo impresso embaixo do valor é o trimestre
  PROJETADO, que é o que responde "sobre o que é este 3,2". Como o horizonte só anda a
  cada dois meses, **duas reuniões seguidas projetam o mesmo trimestre com números
  diferentes** — e a equivalência "trocou de referência ⇔ tem dado novo", que vale em
  todas as outras linhas e é cobrada no teste, fica falsa aqui. Daí `ref_map` (o rótulo) e
  `ref_alvo` (a marca que tira a linha daquela regra). E daí também `div_hora`: dizer que
  aquele índice é uma data de PUBLICAÇÃO é o que põe a linha debaixo da mesma fronteira de
  anacronismo das demais — sem isso a célula sai sem data de divulgação e o teste deixa de
  checar justo a linha que não tem outra guarda. Não vale para a Focus, cujo índice é a
  data de referência da pesquisa e cujo boletim sai na segunda seguinte.
- **Na coluna da próxima reunião a projeção repete a última publicada**, cinza e sem cor — a
  seguinte só passa a existir com o comunicado dela. O usuário pediu assim por ora; a
  ideia é pôr ali uma PREVISÃO do que o BC vai projetar, depois de rever a aba Projeções.
  A caixa de previsão daquela aba já calcula um candidato
  (`antecipa_copom.py`) — quando entrar, a célula deixa de ser repetição e precisa dizer na
  tela que é estimativa, não publicação.
- **Inflação implícita é razão, não diferença.** A 14% de DI e 7,5% de NTN-B a subtração dá
  6,50 e a forma correta 6,05 — 0,45 p.p., maior que o movimento típico de um mês. A forma
  errada funciona na faixa em que se costuma olhar, como na identidade produto/horas do
  relatório de produtividade.
- **O horizonte relevante é acumulado de 4 trimestres, 6 à frente**, composto e não somado, e
  derivado do trimestre da **pesquisa** — o que faz a série ser uma só em vez de uma por
  reunião, e a janela ser rolante em vez de ter o dente de serra do ano-calendário.
- **O juro real de 2 anos da Focus é MÉDIA, não taxa a termo**, porque a NTN-B de 24M ao lado
  dele é média. Selic da curva anual da Focus lida em 0,25/0,50/…/2,00 e mediada (com âncora
  em h=0 na Selic corrente, sem a qual a curva não cobre 0,25 no fim do ano) sobre o IPCA
  acumulado em 8 trimestres, por Fisher.
- **Os dois juros reais americanos usam o mesmo método** — nominal menos inflação esperada do
  Fed de Cleveland — porque o Treasury **não publica TIPS de 2 anos** e as duas linhas ficam
  lado a lado. Os números que decidiram isso estão na docstring de
  `domain/db/us/inflation/expc_inflacao.py`.
- **IBC-Br em 12m entra pela série NSA**: o acumulado de 12 meses já é sazonalmente neutro por
  construção, e ajustar em cima seria dessazonalizar duas vezes.
- **O crédito real cruza nominal e IPCA pelo MÊS DE REFERÊNCIA**, não pelo de divulgação —
  cruzar por divulgação misturaria dois calendários para produzir um número que não é de
  nenhum dos dois.

O que continua valendo da versão anterior, e não foi tocado: `_sa()` começa em 2000 (com a
série inteira o "dessazonalizado" saía **mais volátil que o bruto**, sd 1,03 contra 0,39, e
esse ruído ia direto para o σ); σ é escala **robusta** (1,4826 × MAD), porque dez anos de
história contêm 2020-2021 e com desvio-padrão aquele episódio vira a régua; fatores sazonais
**congelados** até dezembro do ano anterior; nível de preço em variação percentual
(`modo='pct'` — hoje câmbio e Brent, com σ medido em 100×Δlog); e a marca `pendente` quando o
calendário diz que saiu dado que o ETL não carregou.

**O que saiu com o recorte novo:** as linhas de desocupação da PNAD, saldo do CAGED, núcleo
EX3 e as três da Focus de Selic — e com elas os helpers que só as serviam
(`desocupacao_sa`, `caged_saldo_sa`, `nucleo_ex3_mm3m`, `mm3m_anual`, `ibcbr_3m3m`,
`focus_reuniao_serie`, `rotulo_focus`, `numero_reuniao`, `juro_real_ex_ante`,
`focus_ipca_12m_diario`). Com elas foi embora o caso `sinal = 0`, que existia só para a Selic
esperada da Focus (reação do mercado à decisão, não condição que a antecede). `mt_pnad` saiu
das dependências do dashboard; `mt_caged` ficou, porque o painel do modelo a lê como
observável do hiato.

Cobertura: seção 32 de `tests/test_monetary_policy_js.js` (o payload pronto e a markup — a
fronteira de divulgação em cada uma das 9 colunas, `novo` contra a troca de referência, a
pill que esmaece só as posteriores e não traz o passo de Selic, o card de definição, e a
nota de cada linha contra uma lista de vocabulário de mecanismo) e seções 10-15 de
`tests/test_condicoes_copom.py` (a mecânica que produz aquelas datas, mais o espaçamento
da série de projeção e o efeito dele no σ). Verificado contra **13 mutantes**, todos pegos,
e confirmado em Chrome real: 225 células, 184 pintadas, 25 cards, zero exceções.

### A aba Projeções do Copom (2026-08-25)

A projeção do BC para o horizonte relevante contra o **passo de Selic da mesma reunião** — o que o
Comitê projetava contra o que ele fez —, mais a **previsão da próxima**. Três seções: a série
temporal (barras de pontos-base no eixo da direita, projeção no da esquerda, e o ponto previsto
em bolinha verde ligada por tracejado), o **backtest** do que estimamos contra o que o BC publicou, e a
tabela reunião a reunião. Desde 2026-09-24 sobrou **um** seletor — **projeção**
(nível | desvio da meta) —, colado no gráfico de cima, que é o único que ele muda.

**O seletor de previsão saiu com os dois métodos que ele escolhia** (2026-09-24, a pedido do
usuário: *"vamos usar somente o delta focus, pode retirar o ingênuo e o 'modelo'"*). Ficou o
**delta da Focus**, e com um método só o seletor escolhia entre uma opção. Duas consequências que
não são perda:

- **O ingênuo não sumiu, virou régua.** O erro dele é `âncora − publicado`, que é a coluna
  **Revisão** da tabela com o sinal trocado — então o MAE dele se lê de uma coluna que já estava
  lá, sem o payload carregar `erro_ingenuo`. Ele é impresso na chamada do backtest (*"contra
  0,100 de supor que o BC não revisa nada"*) e na linha de MAE, **sob Revisão**, que é de onde
  ele sai. Sem esse número o MAE da previsão não diz nada: 0,079 é bom ou ruim contra o quê?
- **A tabela ganhou a coluna "Previu".** Com uma previsão só, cabe pôr o delta ao lado da revisão
  que de fato aconteceu — a conta inteira, linha a linha, sem o leitor ir ao apêndice.

E o modelo saiu de onde ainda estava escondido: era ele o segundo método, rodado duas vezes por
reunião. **O que sobrou do modelo no relatório é a aba Apêndice**, que continua descrevendo as
equações com os coeficientes estimados — documentação de um modelo que hoje não alimenta número
nenhum na tela. O usuário levantou a incoerência (*"ainda não entendi esse modelo escondido, pois
já tiramos o modelo do BC do dashboard"*): a pergunta seguinte era se o Apêndice ficava — e ele
saiu no mesmo dia (ver "O Apêndice saiu em 2026-09-24").

Saíram na mesma rodada, a pedido do usuário, os de **cenário** e de **defasagem**. O de cenário
alternava entre juros esperado e juros constantes: o segundo é a leitura mais próxima de uma
função de reação e é justamente o que o BC parou de publicar — a série termina em **jul/2024** —,
então o seletor convidava a comparar uma janela corrente com uma parada há dois anos sem dizer
que eram diferentes. O de defasagem escolhia entre o passo da própria reunião e o da seguinte, e
as duas leituras dão **0,27 e 0,28** de associação: o clique custava uma escolha e não mudava
resposta nenhuma. O payload deixou de carregar `juros_constante` e `bps_prox` junto — voltar a
carregar o cenário é uma palavra na tupla de `_projecoes()`.

**A régua de período cede o lugar.** `_ensurePeriodSelector()` se insere acima da barra que tiver
`chart-ctrl-bar`, e não imediatamente antes do `.chart-card`: quem comanda *o que* o gráfico
desenha fica colado nele, e quem só move a janela de tempo fica acima. Sem a classe o markup
fica idêntico e a régua volta a se meter no meio — nada na ordem denuncia, e foi o mutante que
escapou na primeira rodada.

O **grid de quatro KPIs saiu em 2026-09-23**, a pedido do usuário. Três dos quatro repetiam
número que a página já dava — a projeção e o passo da última reunião estão no último ponto do
gráfico e na última linha da tabela, e a contagem de reuniões por documento está na legenda do
gráfico, palavra por palavra. O quarto era a **correlação**, e esse número deixou de existir na
tela: ele continua medido aqui embaixo, e se voltar o lugar dele é uma oração da legenda, não um
cartão. `pjKPI()` e `pjCorr()` saíram junto — função que só alimentava markup removido é órfã.

A **dispersão desvio × passo foi retirada em 2026-08-25** a pedido do usuário e o backtest ficou no
lugar dela. Com isso a aba deixou de ter gráfico que não é série temporal em X, e a exceção ao
`_reactPreserveX` que ela documentava desapareceu junto: os dois gráficos de hoje passam por ele.

O lado da decisão veio de tabela nova, `macro_brasil.pm_copom_reuniao` — 247 reuniões da 34ª
(1999-04) à 280ª, derivadas da **SGS 432** cruzada com o calendário de reuniões. Não é o texto do
comunicado: aquele só é parseado da 206ª em diante, e o passo precisa cobrir a série toda. O texto
entra como **conferência independente**, e nas 63 reuniões em que ele escreve a decisão em prosa as
duas fontes concordam em todas.

**O passo é o da reunião, não o acumulado do ciclo** (decisão explícita do usuário): parado, parado,
+25, +50 aparece como 0, 0, +25, +50. É a variável de decisão, e é comparável entre ciclos porque
não depende de quantas reuniões o ciclo já teve.

Quatro coisas que decidiram o resultado:

- **A janela de cinco dias**, e ela é medida, não escolhida. A meta nova vale do dia útil seguinte,
  mas feriado emendado empurra isso: das 152 mudanças de nível desde 1999, 147 entram 1 dia depois
  da reunião, 4 em 2 (reunião de quarta com feriado na quinta — Corpus Christi de 2003/2007/2009 e
  o 7 de setembro de 2017) e 1 em 5 (20/04/2011, Tiradentes na quinta e Sexta-feira Santa no dia
  seguinte). Os **8 movimentos por viés** estão todos a 7 dias ou mais. Uma primeira versão pegava
  o *último* ponto de uma janela de 12 dias e com isso atribuía à 45ª reunião um corte por viés
  ocorrido 7 dias depois dela; pegar o *primeiro* ponto quebrava o caso contrário, a 209ª, cujo
  corte só entrou 2 dias depois por causa do feriado. Cinco dias separa as duas coisas exatamente,
  e foi a conferência contra o comunicado que apontou o erro.
- **Uma unidade de horizonte só.** A série é sempre o ponto a **seis trimestres** da reunião. Os
  regimes `ano_calendario` e `horizonte_suavizado` do comunicado pré-2024 ficam fora: um horizonte
  relevante que é o ano civil encurta de 12 para 4 trimestres à frente ao longo do próprio ano, e
  isso põe na série um dente de serra que não é mudança de projeção nenhuma. Custa 14 reuniões de
  2020-2024 e sobram 107.
- **Comunicado ganha do relatório na mesma reunião**, porque sai no dia da decisão. Sem filtro de
  `documento` a reunião entra duas vezes com números diferentes. Da 264ª em diante os dois publicam
  o mesmo número, então a preferência é inócua justo onde seria mais visível.
- **Um eixo Y na escala "desvio da meta", dois na de nível** (2026-08-25, a pedido do usuário), e a
  razão é unidade. Desvio e passo estão ambos em pontos percentuais — 100 pb de Selic é 1,00 p.p. de
  desvio —, então dividir régua é o que torna "o desvio era +1,0 e o Comitê mexeu +1,0" uma frase
  legível do gráfico. Na escala de nível não existe essa leitura (3,5% de IPCA projetado e +50 pb não
  dividem régua nenhuma) e ali o eixo duplo é o certo. Duas coisas têm de acontecer juntas: as barras
  mudarem para `y` **e** o `yaxis2` sair do layout — um eixo sobreposto sem trace nenhuma ainda
  desenha título e ticks à direita, e o leitor lê duas escalas onde há uma. O rótulo em cima da barra
  segue em **pb** mesmo com o eixo em p.p., porque passo de Selic se fala em pb.
- **`barmode: 'relative'` com uma barra só** não empilha nada — é o que faz o `_bindYAutofit` dobrar
  o zero dentro do range do eixo das barras. Sem isso, numa janela de ciclo de alta o autofit
  devolveria `[20, 105]` e as barras sairiam desenhadas do fundo do eixo, como se +25 pb fosse quase
  nada. Erro puramente visual: nenhuma exceção, nenhum número errado.

**A previsão dentro da aba** (2026-08-25). O ponto previsto entra no gráfico principal como duas
traces separadas — uma ponte tracejada sem legenda e sem hover, e uma bolinha verde — e nunca
como mais um ponto da série dourada: é o único número da aba que ninguém publicou.

**A caixa verde que ficava acima do gráfico saiu em 2026-09-23**, a pedido do usuário, na mesma
rodada do grid de KPIs — ela trazia âncora, documento, delta, MAE do método, corte de informação e
a faixa de frescor, seis linhas de texto sobre um número só. O que saiu com ela e **não podia**
sumir é o **corte de informação**, que era a única procedência do ponto na tela: ele passou para a
legenda do gráfico, na mesma oração que já nomeava a reunião prevista e o método. A faixa de
frescor deixou de existir na página; o aviso equivalente continua no console da geração
(`generate_report` imprime `AVISO previsao calculada com dado ate …`), que é onde ele é acionável —
mas quem só abre o HTML não é mais avisado de artefato velho. Vale como pendência se o caso
voltar a acontecer.

Três decisões que a seção 33 do teste fixa, porque nenhuma delas lança exceção se quebrar:

- **A previsão é condicionada na curva de Selic da Focus**, que *é* o condicionamento do cenário
  que a aba lê. Era por isso que ela desaparecia no cenário de juros constante, enquanto esse
  seletor existiu: desenhá-la ali faria o ponto parecer continuar uma série que ele não continua.
- **A linha da meta se estende ao ponto previsto**, senão o único ponto do gráfico sem referência
  seria justo o que mais precisa dela. E a meta dele vem do mesmo dicionário das linhas publicadas,
  com `meta_estendida` marcado — na escala "desvio" a régua tem de ser a mesma.
- **Bolinha, não losango.** O marcador é círculo do mesmo tamanho dos da série publicada, só em
  verde: o losango vazado da primeira versão foi rejeitado pelo usuário — lia como sujeira, não
  como ponto. O que distingue previsão de dado publicado é a cor e o tracejado que leva até ela.
  A prosa da aba ainda dizia "losango vazado" em dois lugares até 2026-09-23: **o marcador mudou e
  as duas frases que o descreviam não**, e nada na página as contradizia.
- **A chamada da aba só promete o ponto quando ele é desenhado.** Ela testava `P.previsao` — existe
  previsão no payload? — e o gráfico testa `pjPrevValor(pv) != null`, que é outra pergunta: o método
  tem valor? As duas divergem hoje mesmo, com `previsto_focus` nulo, e a frase anunciava
  um ponto verde que não estava lá. Corrigido em 2026-09-23: a chamada usa a mesma condição e diz
  explicitamente quando não há ponto. **A distinção sobreviveu ao seletor sair** (2026-09-24) e
  passou a valer também no harness: `P.previsao` existir e o ponto ser desenhado são perguntas
  diferentes, e o teste carrega um `_pontoPv` único em vez de repetir `P.previsao ? …` — com o
  `previsto_focus` nulo de hoje, as asserções escritas sobre a primeira pergunta **estouravam** em
  `traces[4]` inexistente em vez de reprovar regra nenhuma.
  **O backtest tinha o mesmo defeito e só o Chrome o mostrou** (2026-09-24): `estende` testava
  `!!pv`, então sem valor previsto o eixo ganhava a data da 282ª, a vertical pontilhada e duas
  frases — *"com o ponto apontado para a 282ª"* no subtítulo e *"À direita da vertical
  pontilhada…"* na legenda — sobre um ponto que não estava lá. Com três métodos o defeito ficava
  mascarado, porque o modelo tinha valor e desenhava algo ali. Agora `estende` exige
  `pjPrevBruto(pv) != null`; o harness cobra eixo, vertical e legenda, e o subtítulo, que o stub
  não monta (o div do gráfico não tem card no stub), fica coberto pelo browser.

**O backtest também aponta para a frente** (2026-08-25, ainda a pedido do usuário): no eixo Nível
a linha da previsão ganha um ponto extra na próxima reunião, com uma vertical pontilhada
separando o que já pode ser conferido do que não pode, e a linha do publicado recebe `null` ali — é
essa parada que sinaliza a ausência de contrapartida do BC. No eixo **Erro** não estende, porque não
há número publicado para subtrair. O valor do ponto extra é lido pelo mesmo `pjPrevBruto()` que
alimenta o gráfico principal, e o teste cobra que os dois batam: são dois consumidores do
mesmo número na mesma tela.

**Os apêndices das abas Condições e Projeções foram revisados em 2026-09-24**, a pedido do
usuário (*"veja se tem coisa boiando ou antiga"*), e o que saiu vale como padrão do que procurar:

- **Número medido uma vez**, que envelhece a cada reunião: 17 reuniões, 9/8, 107, 152 mudanças de
  nível, 63 comunicados conferidos. Ou passou a ser derivado na página, ou foi reescrito numa forma
  que não envelhece ("todas menos cinco", "em todas as reuniões").
- **Uma conclusão que se inverteu**: *"a expansão é o caso mais fácil"* valia com 17 reuniões; com
  18 a previsão erra **menos** na revisão (0,076 contra 0,081). Agora a frase escolhe o tipo pela conta.
- **Uma afirmação falsa**: *"a vantagem sobre não prever nada é consistente"*. Ela ganha em 9 reuniões
  e perde em 9, com t de 0,82. O texto diz isso, e só afirma significância se o t passar de 2.
- **Três números que não se reproduziam** no item de comunicado × relatório (60 de 60, 0,037, 14
  reuniões de 2020-2024) foram trocados pelo que se mede hoje: o mesmo número em todas as reuniões
  desde a 264ª e em 10 de 11 antes; 36 reuniões fora da série, 29 delas entre 2017 e 2024.
- **História de construção escrita para o leitor**: "a pedido do usuário", "até setembro de 2026",
  "modelo desta pasta", e a nota de como acrescentar uma variável em `_spec()`. É o defeito de
  audiência de `.claude/rules/lis-dashboards.md`, cometido nas rodadas desta mesma semana.

O guarda proíbe cada frase aposentada por nome e confere os números novos contra conta refeita no
teste; os que coincidem no dado de hoje (9 contra 9, t abaixo de 2) são exercitados com um backtest
**sintético**, porque trocá-los não mudava uma letra e três mutantes passavam verdes por isso.

**As duas tabelas da aba são click-drop** (`<details class="tbl-fold">`, mesma mecânica do
apêndice), fechadas por default — 17 e 107 linhas abertas empurravam tudo que vem depois para fora
da tela. O `<summary>` recebe a contagem pelo JS, senão a tabela fechada não diz o que tem dentro.

O relatório **não roda o modelo**: `antecipa_copom.salvar()` grava `data/antecipa_backtest.csv` e
`data/antecipa_previsao.json`, e `_load_antecipa()` só os lê. Sem os arquivos a aba mostra o
histórico publicado e nada mais — `antecipar()` roda o espaço de estados duas vezes e o backtest 34,
o que não cabe num `generate_report`. O contrapeso é que os artefatos envelhecem em silêncio: o
`corte_usado` fica no JSON, a legenda do gráfico o imprime e a geração avisa no console quando ele
ficou atrás do que o banco já tem.

A meta vem de `inflc_meta`, anual e terminando em 2026; os trimestres projetados vão a 2028. A meta
do último ano publicado é estendida para frente, o que sob o regime de **meta contínua** (3%, desde
janeiro de 2025) não é extrapolação — é o próprio desenho da meta. As reuniões afetadas vêm marcadas
com `meta_estendida` e o `generate_report.py` imprime a contagem.

Correlação desvio × passo: **0,27** contemporânea e **0,28** contra o passo seguinte, em 107
reuniões — medidas aqui, e desde 2026-09-23 não calculadas na página (era o quarto KPI). As duas
sobrevivem como **texto do apêndice**, que é onde elas explicam por que não há mais um seletor de
defasagem. O sinal é o esperado e a magnitude modesta também: se o Copom já reagiu, a projeção
condicionada aos juros esperados volta para perto da meta, e o desvio pequeno é *resultado* da
política. O cenário de **juros constantes** seria a leitura mais informativa dos dois — e é justo o
que o BC parou de publicar em 2024. Nenhuma das duas é estimativa de função de reação: falta o
juro real contra a neutra, que a eq. (3) deste modelo usa e que separa duas reuniões com o mesmo
desvio e Selic em 8% ou em 15%.

Cobertura: seção 33 de `tests/test_monetary_policy_js.js` (homogeneidade do horizonte, ausência de
duplicata por reunião, `bps` conferido contra os dois níveis que viajam no payload, o que cada pill
faz com os traces, e o guarda de que o grid de KPI não volta — sobre a **fatia do markup** da aba,
nunca sobre `getElementById`, que no stub cria elemento para qualquer id).

**A seção 33 aborta no meio hoje**, por duas pendências de dado listadas abaixo: a 281ª não tem
linha em `pm_copom_reuniao` e `delta_focus` está nulo, então o gráfico sai com 3 traces e a
asserção seguinte lê `traces[4]` de `undefined`. Tudo que estiver escrito depois desse ponto **não
roda** — foi por isso que o guarda do grid de KPI foi posto logo após o render, e não junto das
asserções de tabela. Verificado contra 3 mutantes (um cartão de volta no markup, a contagem de
reuniões saindo da legenda, e um controle inócuo que tem de passar).

### O caminho de cada Relatório, na aba Projeções (2026-09-25)

Pedido do usuário, com a Tabela 2.2.1 do RPM de set/2026 como exemplo: *"Vamos consumir a tabela
de expectativas de inflação do BC do anexo estatístico do RPM ... A ideia é acompanhar como as
expectativas para cada vértice mudam ao longo do tempo."* Duas seções no fim da aba, antes das
notas: **o caminho que cada Relatório projetou** (uma linha por edição, X = trimestre projetado, a
mais recente com losango no horizonte relevante, a anterior em azul-claro, o realizado em dourado,
e uma tabela recolhível das últimas 8 edições — a 2.2.1 com a linha "Diferença Rel. anterior"
virada cor), e **um trimestre, edição a edição** (seletor de trimestre, default o horizonte
relevante da mais recente). As duas com pill de índice: IPCA, livres, administrados.

**Não entrou tabela nova, e o motivo é medido.** O mesmo número já estava em
`pm_copom_projecoes` (`documento = 'relatorio'`), lido do texto do relatório **desde 1999**; o
anexo só existe de set/2021 em diante e ainda não tinha a planilha de set/2026 no dia em que o
relatório saiu. Nas 20 edições que têm as duas fontes, **as 414 células de projeção comuns são
iguais**, e o anexo tem uma a mais (2026T1 da edição de dez/2022). Livres e administrados no anexo
são anuais até jun/2024 — não acrescentam história. `tests/test_projecao_rpm.py` §3 refaz a
conferência a cada execução: é o guarda do parser de PDF, que tem cinco armadilhas silenciosas.
Se um dia o anexo tiver de ser fonte, ele é um `documento` a mais na mesma tabela, não uma tabela.

Decisões, cada uma com o erro que evita:

- **O cenário de juros esperado, e o constante onde ele é o único.** Três edições (mar/2002,
  dez/2002, mar/2003) publicaram só o constante; ficavam de fora e, a pedido do usuário no mesmo
  dia, entram com ele (`cenario` em cada edição do payload), numa cor própria (`PJ_CTE_COR`, verde
  suave fora da rampa cinza) e com a legenda nomeando as três. **Nenhuma revisão atravessa a troca
  de cenário** — a diferença mediria a hipótese de juros, não a projeção —, então a edição de
  jun/2002 não tem revisão contra a de mar/2002 e o hover diz por quê; duas de juros constantes
  seguidas (dez/2002 → mar/2003) medem entre si. No gráfico de um trimestre elas são pontos soltos,
  fora da linha e da conta da chamada. **Mar/2022 tem dois cenários com a Selic da
  Focus**: o A (petróleo pela curva futura, "de maior probabilidade") e o B (a hipótese usual, que
  o comunicado da 245ª chamou de referência). A série traz o A, que é o do leque do relatório.
- **Seletor de edições, com caixa de marcar** ("Todas as edições" + cada uma; era um `<select>` de
  uma edição só até o fim do mesmo dia). As marcadas — **até 9** — entram ao lado da mais recente,
  que fica sempre, marcada e travada, em azul forte. Cada uma ganha uma cor de `PJ_SEL_CORES`, todas
  a ΔE2000 ≥ 20 entre si e ≥ 21 do azul, do dourado e do cinza do gráfico — **nove é o teto de cores
  separáveis, e por isso é o teto de marcadas**; cheio, as outras caixas travam com o motivo no
  `title`. **A cor é fixada quando a edição é marcada** (`PJ.cmSlot`, a primeira livre), não pela
  posição no gráfico: marcar uma edição mais antiga não repinta as outras, e desmarcar uma libera a
  cor dela. A de juros constantes marcada sai **pontilhada** (o verde é só da vista com todas, e a
  chamada deixa de prometê-lo). O realizado recorta a dois anos antes da mais antiga desenhada e a
  janela recomeça no "Tudo" do desenhado. Trocar o índice desmarca só as edições que ele não tem.
  A chamada diz, para cada marcada, a projeção do horizonte relevante contra o realizado; título,
  subtítulo e botão nomeiam até duas ou três e contam daí em diante. **A lista não é refeita a cada
  clique** (`pjCmSyncEd()` só acerta caixas e cores), senão a rolagem de ~110 itens voltaria ao
  topo. A tabela recolhível não muda (as últimas 8).
- **A revisão é contra a edição IMEDIATAMENTE anterior**, a regra da própria tabela do BC; um
  trimestre que ela não projetava é "novo", nunca revisão zero. Há mutante para isso.
- **O realizado é série própria, não coluna do caminho**: o ETL já descarta os "efetivos" da tabela
  matriz. IPCA pela `ipca_12m`; livres e administrados compostos das variações mensais. Bate com os
  efetivos do anexo em 95 de 96 células na primeira casa — administrados de 2026T1 sai 5,44 aqui e
  5,5 lá, arredondamento das variações mensais do SGS. **O teste arredonda meio para cima**: o
  `round()` do Python faz 5,35 → 5,3 e reprovava quatro células certas.
- **O Y do gráfico de um trimestre abre com a folga do ajuste de Y** (meio ponto, a mesma de
  `y_autofit.js`): com o autorange do Plotly, 3,0–3,2 ocupava a altura inteira e uma revisão de 0,1
  lia como salto — e o primeiro clique na régua mudava a escala sozinho. O X rotula cada edição
  (`set/2026`): o eixo de data escreveria "Jul 2022" em inglês.
- **A cor da tabela só apareceu no Chrome**: `.hier-table td.col-value` tem a mesma especificidade
  e vem depois no CSS, então a regra nova sem `col-value` era apagada. O stub não calcula estilo; o
  teste cobra a regra no CSS.

Coberto por `tests/test_monetary_policy_js.js` §37 (payload, render, prosa refeita, tabela célula a
célula, troca de índice e de trimestre, sintéticos, vocabulário, ids), verificado contra **7
mutantes** e um controle, e por `tests/test_projecao_rpm.py` contra 4. Confirmado em Chrome headless:
108 traces no caminho, zero exceções, e a tabela reproduz a 2.2.1 de set/2026 célula a célula. O
cenário constante e o seletor de edição têm mais 7 mutantes, todos pegos, e foram conferidos no
Chrome (zoom em 2002, jun/2010 e dez/2002 escolhidas, 2003T4 no segundo gráfico; zero exceções). As caixas de marcar têm mais 9 mutantes (cor pela contagem, sem teto, "Todas" que não limpa,
juros constantes sem pontilhado, índice que não desmarca, chamada sem as várias, janela sem reset,
lista sem sincronizar, só a primeira desenhada), todos pegos, e foram conferidas no Chrome (lista
aberta com 110 itens, continua aberta ao marcar, fecha no clique fora; três marcadas; zero exceções).
**Os mutantes têm de ser aplicados ao `reports/brasil/Monetary Policy.html`**, que é o que o
harness lê: aplicados ao `report.html` de origem, todos "escapam".

### A aba Acompanhamento Condicionais (2026-09-24)

Pedido do usuário: *"Vamos criar uma nova aba ... Por hora, coloque o nome de 'Acompanhamento
Condicionais'. Quer criar um grafico para o acompanhamento das vintages do hiato do produto
divulgado pelo BCB no RPM."* O nome aponta para os condicionantes da projeção do Copom; o hiato é
o primeiro. `_load_condicionais()` entrega `D.condicionais.hiato.edicoes` — uma entrada por
edição, só a estimativa `central` — e o resto é JS.

O gráfico é uma linha por edição (X = trimestre de referência) mais a **leitura em tempo real**: o
último ponto de cada edição, que é o trimestre em que ela saiu e cujo PIB ainda não existia. O que
a leitura mostra hoje, e a chamada da aba deriva: as 19 leituras já revisadas foram **todas para
cima** (+1,10 p.p. em média) e 9 saíram negativas e hoje são positivas.

Decisões, cada uma com o motivo de não ser a outra:

- **Só `central`, e o traço marca a metodologia.** Até a edição 2024-06 o anexo publica um modelo
  com banda de ±2 d.p.; de 2024-09 em diante, o cenário de referência com a dispersão de um
  conjunto de modelos. As faixas medem coisas diferentes e ficam fora; tracejado = um modelo,
  contínuo = conjunto. As duas passagens em volta da troca revisam +0,10 e +0,09 p.p. contra
  mediana de +0,01 nas outras 17, e a nota diz isso ao leitor. Nem a central fica dentro da faixa
  nova (2019T1 da edição 2026-06 está abaixo do p25), porque o cenário de referência não é a
  mediana dos modelos — razão a mais para não desenhar a faixa em volta dela.
- **Cor em rampa, não paleta categórica.** A ordem das edições é a informação; vinte cores
  distintas não se leriam e a regra de ΔE ≥ 20 entre séries não se aplica a uma sequência. A mais
  recente sai da rampa (azul, grossa); a leitura em tempo real é dourada.
- **`hovermode: 'closest'`**: vinte edições num `x unified` dariam uma caixa de vinte linhas com
  cabeçalho em data do Plotly, não em trimestre. O hover do ponto dourado põe a primeira leitura
  ao lado da de hoje.
- **A janela abre nos últimos 5 anos**, o mesmo `from` do botão 5a, com meio trimestre de folga à
  direita. Ela é gravada em `_chartXRange` **antes** do primeiro render, e é isso que faz o
  `_reactPreserveX` tratá-la como escolhida: aplica, dispara o relayout que refaz o Y pela janela
  (sem isso o Y abriria dimensionado pela recessão de 2020, que está fora da janela) e acerta
  os dropdowns da régua.
- **`_PERIOD_LABEL[divId]`** troca o rótulo dos dropdowns da régua para trimestre (`2026T2`). Default
  continua mês/ano para os outros gráficos.

**O caminho da Selic** (mesmo dia, segundo gráfico da aba): um caminho por reunião desde 2006 — a
mediana da Focus por reunião na última pesquisa até a **sexta-feira anterior à decisão** —, mais o
da pesquisa mais recente (o que está na mesa para a próxima) e a Selic efetiva. É o gráfico de
"fios de cabelo" clássico: 166 caminhos, em degrau (`shape: 'hv'`).

- **A sexta de corte é convenção nossa.** O comunicado diz só "extraída da pesquisa Focus"; a
  sexta é o corte que o Copom declara para o câmbio do cenário (comunicados 214-229) e o boletim
  da segunda-feira da semana da reunião. A nota diz isso ao leitor.
- **A Focus pergunta pela POSIÇÃO da reunião no ano (`R4/2028`), não pela data.** Reunião
  passada ou do calendário publicado entra na data real; a que o BC ainda não marcou, na mesma
  posição do ano anterior + 52 semanas, marcada `estimada` ponto a ponto. Até 2026-09-24 era a data
  típica da posição (mediana de 10 anos), que errava 7,0 dias em média contra 4,0 da regra nova
  (128 reuniões de 2012 a 2027, cada ano estimado só com os anteriores) e caía em fim de semana. Só existe posição bem definida com 8 reuniões por ano — daí 2006 —, e um
  ano com 9 conhecidas levanta. **O mapeamento foi conferido contra a decisão**: a mediana para a
  própria reunião nunca errou por mais de 50 p.b. desde 2006 (um deslocamento de uma posição
  erraria por um ciclo), e o teste cobra isso.
- **Cada caminho começa na Selic vigente** no dia da pesquisa, e o primeiro degrau é a própria
  reunião — é o que prende o fio à linha dourada. A nota que contava quantas das últimas 16
  decisões bateram com a mediana saiu no mesmo dia, a pedido do usuário (ver a aba seguinte): a
  pesquisa não é lida aqui como previsão a pontuar.
- **Legenda em grupo.** Os 165 anteriores são uma entrada só (`legendgroup`); a última reunião
  decidida sai em azul-claro, o caminho de hoje em azul grosso, a Selic efetiva em dourado.
- **A régua rotula por dia** (`_PERIOD_LABEL`): a sexta de corte e a quarta da decisão caem no
  mesmo mês. E a janela inicial (`_janelaInicial`, agora comum aos dois gráficos) começa na
  primeira data REAL dos últimos cinco anos, senão o dropdown De cairia em 2006.

Toda frase com número é derivada (chamada, legenda e as notas), e as seções 34 e 35 de
`tests/test_monetary_policy_js.js` refazem cada conta a partir do payload — mais payloads
sintéticos para os ramos que o dado de hoje não exercita (revisão mista, troca de sinal no
singular, mudança de caminho nos dois sentidos, sem caminho de hoje). A seção 35 foi conferida
contra um mutante que corta a pesquisa no dia da decisão em vez da sexta anterior: 4 asserções
caem, a primeira delas a de lookahead. Confirmado em Chrome headless: 21 e 168 traces, zero
exceções.

### A aba Expectativas de Juros (2026-09-24)

Dois pedidos do usuário no mesmo dia: trazer para cá o que o relatório de Expectativas dizia de
política monetária (*"a minha ideia com o dash de expectations é esvaziá-lo com o tempo e as
expectativas irem migrando para os seus dash tema"*) e ver *"o que a curva de juros está
precificando"*. A aba Curva do Copom de lá saiu inteira, e o que ela mostrava entrou aqui ao lado
da curva DI. `expectativas_juros.montar()` entrega `D.expectativas`: a lista de reuniões e, por
fonte, a última data de cada semana ISO, a Selic vigente nela, o índice da primeira reunião ainda
por acontecer (`j0`) e um bloco `{i0, ...}` por reunião. Três seções: o caminho de hoje das duas
fontes com a comparação de 1/4/12/52 semanas antes; a formação da expectativa para uma reunião
(seletor, default a próxima), com a faixa das respostas e as respostas de 4 dias úteis; e a
n-ésima reunião à frente ao longo do tempo, com a distância curva − pesquisa em p.b. embaixo.

**O enquadramento é do usuário e é regra da aba**: *"I'm not using the Focus or DI Curve to predict
the BCB movement. The DI curve gives a price, it never price 100% correct because of market
stuff ... I don't wanna RMSE, mean error and stats like that in the dash."* Nenhuma estatística de
acerto na tela, e o guarda de vocabulário da seção 36 proíbe o vocabulário dela. Pelo mesmo motivo
saiu da aba Acompanhamento Condicionais a nota que contava quantas decisões bateram com a mediana.
A conferência de que a leitura da curva está certa **existe, e mora no teste**
(`tests/test_expectativas_juros.py` §4): no pregão do dia de cada decisão desde 2006, a taxa que a
curva precifica para aquela reunião fica a menos de 50 p.b. do decidido (pior: 45, 10/06/2009).

Como a curva vira um caminho, e por que cada escolha:

- **A grade inteira, não os 9 vértices.** `br_interest_rate` tem 1M, 3M, 6M, 9M, 12M… — cinco
  pontos no primeiro ano para oito reuniões. A grade que a B3 publica (~280 vértices, tabela
  `br_di_grade`, criada para isto) é flat-forward entre vencimentos de DI1 e é **o mesmo insumo da
  Bloomberg** (22/09/2026: os 17 vencimentos da tela dela a 0,001 p.p.).
- **A conta é a da Bloomberg desde 2026-09-25**, a pedido do usuário depois de comparar as duas
  telas (*"vamos usar as datas e a suavização da bloomberg"*). Mínimos quadrados sobre a taxa de
  cada vencimento (média composta dos overnights até ele) **mais um custo por mudar de uma reunião
  para a seguinte**, λ = 0,1. A versão de 2026-09-24 ajustava os forwards mês a mês sem custo
  nenhum e saía em zigue-zague: 1 p.b. num contrato a um ano e meio move o forward do mês ~13 p.b.,
  e a Bloomberg aceita errar os contratos em ~1 p.b. para não transformar isso em degrau. Medido
  (22/09, mesma curva e mesmas datas): 0,7 p.b. de diferença média para a Bloomberg até dez/2027
  contra 4,0 sem o custo. O que a suavização custa — pausa e ritmo constante não se distinguem a
  um ano, movimento grande muda até ~15 p.b. — está no `.md`. **`suavizacao=0` continua existindo**
  e é o que o teste usa para exigir a escada sintética de volta exata (e uma deslocada de um dia
  não): a convenção de datas só é testável sem o custo.
- **Mais à frente a curva só informa trimestre.** Medido na grade de 23/09/2026: depois de ~16
  meses os forwards vêm em blocos de três meses iguais (vencimentos trimestrais). Com a suavização
  o caminho passa de um trimestre para o outro em rampa, e a nota diz ao leitor que aquilo não é
  passo precificado.
- **CDI → meta pela diferença do próprio pregão** (meta vigente − CDI do primeiro overnight;
  0,10 p.p. hoje, entre −0,04 e 0,67 na história — nov/2008 e fim de 2012 são os extremos, e são
  episódios reais).
- **Dia útil da época.** O `du` da B3 usa o calendário vigente no pregão, e o 20 de novembro só é
  feriado nacional desde 21/12/2023. Com essa regra o calendário daqui reproduz o `du` publicado em
  todos os vértices conferidos; sem ela, 1.427 de 60.740 divergem.
- **As datas das reuniões são as da aba Condicionais** (`condicionais.posicoes()`), então a reunião
  `j` da pesquisa e a da curva são sempre a mesma. Desde 2026-09-25 as de 2027 são **oficiais**,
  de `pm_copom_calendario` (o feed de reuniões do BCB, que o calendário anual do sistema não
  recebe), e iguais às da Bloomberg. As que o BC ainda não marcou entram na mesma reunião do ano
  anterior + 52 semanas — numa quarta; a regra anterior (dia do ano típico) caía em fim de semana.
  Para 2028 a Bloomberg estima outra coisa (19/01, 01/03, 19/04 contra 26/01, 15/03, 26/04 daqui);
  nenhuma é oficial, e ali a diferença move o caminho ~2 p.b.
- **A distância curva − pesquisa só entre a MESMA reunião.** Pesquisa e pregão da mesma semana
  podem cair dos dois lados de uma decisão; a seção 36 tem o caso sintético.
- **Ficou de fora, de propósito:** o mapa de calor horizonte × semana e os 4 cartões da aba antiga
  — o mapa mostrava a mesma série da terceira seção, e cartão ao lado da lista que ele resume é a
  regra que o usuário já pediu para tirar duas vezes.

Coberto por `tests/test_monetary_policy_js.js` §36 (invariantes do payload, render, prosa refeita,
casos sintéticos, vocabulário) e `tests/test_expectativas_juros.py`; verificado contra 6 mutantes
(fila deslocada, âncora fora da Selic vigente, "semanas antes" por posição, distância sem conferir
a reunião, janela sem reset na comparação, degrau no dia da decisão) e em Chrome headless: 4
gráficos, zero exceções. Geração: ~20 s a mais (o `montar()`).

A suavização e as datas oficiais (2026-09-25) têm gabarito externo no teste: **a tela de CDI
implícito da Bloomberg de 22 e 24/09/2026, transcrita no próprio teste** (§5 e §6) — o caminho
tem de ficar a menos de 2,5 p.b. do dela com os contratos dela, e a menos de 2 p.b. com a curva da
B3 no dia em que as duas coincidem. Quatro mutantes pegos: sem suavização, suavização 3×, datas
estimadas com 365 dias em vez de 52 semanas (sai de quarta), calendário oficial fora.

## Antecipar a projeção do BC (`antecipa_copom.py`, 2026-08-25)

Prever **que número o Copom vai publicar** para o horizonte relevante na próxima reunião — não
qual vai ser a inflação. O horizonte é sempre 6 trimestres à frente do *trimestre* da reunião
(17/17 na era em que o Copom o declara) e há duas reuniões por trimestre, então reuniões
consecutivas costumam ter o mesmo trimestre-alvo e o BC já publicou um número para ele. O método é
**âncora + delta**, nunca nível: `projeção(281ª) = 3,2 publicado para 2028T1 + delta`.

### O resultado, medido nas 18 reuniões da era declarada

Números de 2026-09-24, com a 281ª já no backtest. **Derivados na página** desde essa data — a
chamada, a tabela e o apêndice leem o mesmo `antecipa_backtest.csv`, em vez de o apêndice repetir
à mão os de 17 reuniões enquanto a chamada logo acima imprimia os de 18.

| método | MAE | direção da revisão |
|---|---|---|
| ingênuo ("não vai revisar") | 0,100 p.p. | — |
| modelo agregado, nossos parâmetros | 0,138 | 7/12 |
| modelo agregado, **modas publicadas do BC** | 0,208 | 6/12 |
| **delta da Focus** | **0,079** | **9/12** |

Por tipo de horizonte: expansão 0,082 (Focus) contra 0,089 (ingênuo), revisão 0,076 contra 0,111.
Dos três, só o delta da Focus segue na tela.

**O acumulado da Focus é composto desde 2026-09-24**, e era somado antes. `focus_4t()` pega as
quatro medianas trimestrais até o alvo, e a projeção do BC é a variação acumulada em quatro
trimestres — composta. Somar punha o nível ~0,06 abaixo (3,89 contra 3,95 para 2028T2 na
pesquisa de 18/09/2026) enquanto o docstring dizia "mesma escala da projeção do BC". **No delta a
diferença é de milésimos**, e foi medida antes de trocar: MAE 0,0782 somando e 0,0786 compondo,
direção 9/12 e o decimal publicado 6/18 nas duas, maior diferença de delta 0,009 (267ª). Compor
deixa o delta ~3% maior, o que ajuda onde a Focus subestimava a revisão e atrapalha onde
superestimava — no saldo, empata. Trocado a pedido do usuário por ser a conta certa, não por
ganho; o teste refaz a composição a partir das quatro medianas cruas, e um mutante que volta a
somar reprova em duas asserções.

A comparação com o modelo — por que ele erra mais que o ingênuo, as duas coisas testadas que não
o salvaram, a taxa neutra que o BC anuncia e os insumos do cenário — mudou-se com ele para
[`../structural_model/modelo_agregado/CLAUDE.md`](../structural_model/modelo_agregado/CLAUDE.md),
"A antecipação da projeção com o modelo". Em uma frase: a revisão do BC entre duas reuniões vem
sobretudo do IPCA mensal novo, que a pesquisa semanal incorpora e um modelo trimestral não vê.

`date = 2026-10-01` é **ambíguo** e isso decidiu a busca da âncora: significa o trimestre 2026T4 ou
o ano civil 2026, que a tabela normaliza para o T4. Como o IPCA acumulado nos 4 trimestres até o T4
*é* o ano civil, os dois são o mesmo objeto econômico — filtrar `periodo_tipo='trimestre'`
descartava o comunicado da 270ª e pegava um relatório dois meses mais velho.

O benchmark é severo e por isso é reportado sempre: as revisões têm |média| de 0,106 p.p. e **13 das
17** caem dentro de um tique de arredondamento (o BC publica com uma casa). Só 4 excedem um tique.

Cobertura: `tests/test_antecipa_copom.py` (cada seção nasceu de um erro que devolvia número
plausível e errado sem levantar exceção: `t0` no trimestre não fechado e a âncora filtrada por
`periodo_tipo`, entre outros). As seções de r\*, curva de Selic e câmbio foram com o modelo para
`tests/test_antecipa_modelo.py`.

## Projeções do próprio BC: comunicados + RPM

O texto das duas publicações de política monetária virou dado estruturado **fora desta pasta**, porque
é ETL. As duas alimentam a mesma tabela, `pm_copom_projecoes`, separadas pela coluna `documento`:

- **comunicado**: `connectors/bcb_copom.py` → `_copom_texto.py`. 233 reuniões versionadas em
  `raw_md/central_bank/comunicados/`; carga da 206ª (2017-04) em diante, **396 linhas**.
- **relatório** (RPM, chamado RI até 2024-12): `connectors/bcb_rpm.py` → `_rpm_projecoes.py`.
  **109 edições** de 1999-06 a 2026-06 em `raw_md/central_bank/rpm_paginas_projecao/`; **1.967 linhas**
  de 108 delas.

O relatório não é redundante: o comunicado publica 2 ou 3 períodos escolhidos, o relatório publica o
caminho trimestral **contíguo**. Por isso o ponto a 6 trimestres à frente existe em toda edição desde
1999, e a série de horizonte relevante passou de 52 pontos (2020→) para **150 (1999-09 → 2026-08)**.
Onde os dois cobrem a mesma célula, batem **exatamente da 264ª reunião em diante** (60 de 60); antes
divergem 0,037 p.p. em média, porque o relatório é vintage posterior (7 a 28 dias) e porque em
2017-2020 o comunicado publicava o cenário **híbrido** (juros Focus com câmbio constante) enquanto o
relatório publica os puros.

**Para o uso aqui como alvo de validação, isso importa**: a projeção da mesma reunião pode existir
duas vezes com números diferentes. Filtrar `documento` é obrigatório — e o relatório é o que dá o
caminho inteiro, não só o HR.

Desde 2026-08-25 há uma terceira tabela no par, `pm_copom_reuniao`: uma linha por reunião com o
**passo de Selic** decidido, das 247 reuniões desde 1999. Não vem de texto — vem da SGS 432 cruzada
com o calendário de reuniões, e é o que fecha o par projeta/faz que a aba Projeções usa.

Levantamento das duas fontes:
[`copom_comunicados.md`](../../../domain/db/brasil/bcb/copom_comunicados.md) (5 regimes de
comunicação, a armadilha do nome do cenário) e
[`relatorio_politica_monetaria.md`](../../../domain/db/brasil/bcb/relatorio_politica_monetaria.md)
(3 formatos de tabela, 5 armadilhas silenciosas do PDF, a grade 2×2 de cenários de 2016-2020).

## Cabecalho de cada grafico (2026-09-14)

Todo grafico desta pasta carrega, dentro do proprio card e acima do plot, as tres linhas do
padrao: titulo, subtitulo derivado e `Fonte: … · <periodo>`. So o titulo e a fonte sao texto
fixo (`CHART_META` no `report.html`); subtitulo e periodo sao reescritos a cada render. A
mecanica e compartilhada -- `/*CHART_HEAD_CSS*/` e `/*CHART_HEAD_JS*/`, de
`analytics/report_structure/chart_head.{css,js}` --, entao o que mora aqui e so o
`CHART_META` e a chamada de `describeChart()`.

**Desde 2026-09-24 sao tres**: o `chart-cn-hiato` da aba Acompanhamento Condicionais, com
titulo fixo, mais os dois abaixo. **De 2026-09-22 a 2026-09-24 eram dois**, os dois da aba Projecoes (`chart-pj-serie` e
`chart-pj-bt`): os 4 da aba do motor e os paineis por input sairam com ela, e com eles o
unico uso da variante `compact`. A aba Condicoes nao tem grafico nenhum de proposito -- ela
e uma matriz de 225 celulas, e o cabecalho de tres linhas existe para um grafico que sai da
pagina como print; o equivalente dela e a legenda de cores mais o card por linha. Nos dois que ficaram uma pill troca o que a linha E --
escala na serie, eixo no backtest --, entao o **titulo tambem e derivado**: ali o unico
texto fixo e a fonte.

Coberto por `tests/test_chart_head_js.js`; o porque e o levantamento de quem faltava
estao em `.claude/rules/lis-dashboards.md`, secao "Every chart carries its own header".

## Pending
- **Aba Acompanhamento Condicionais — os outros condicionantes.** Hoje hiato e Selic. Os
  candidatos naturais são os outros insumos do cenário de referência (taxa neutra, câmbio
  inicial, petróleo). Nenhum tem vintage no banco hoje; o câmbio inicial o parser do comunicado
  já lê e não grava (ver o item "Comunicados" abaixo). Levantar a fonte antes de prometer a linha.
- ~~**As reuniões de 2027-2028 entram em data estimada.**~~ As de 2027 são oficiais desde
  2026-09-25 (`pm_copom_calendario`, atualizada todo dia pelo `--continuous`); as de 2028 viram
  oficiais sozinhas quando o BC publicar, e até lá são estimadas (ver a aba Expectativas de Juros).
- **Aba Condições — `condicoes_copom.montar()` levou 74 s em 2026-09-25**, quase todo em
  `juro_real_focus_2a()` → `focus_selic_ponto()`, que filtra um DataFrame da Focus 53 mil vezes
  (medido com cProfile; a função sozinha, 53 s). A geração inteira foi de 73 a 111 s no mesmo dia.
  Não vem das mudanças daquele dia (`todas_reunioes()` leva 0,4 s); vale vetorizar se a geração
  passar a incomodar.
- **Aba Expectativas de Juros — o resto do relatório de Expectativas que é política monetária.**
  Candidatos: a ancoragem das expectativas de inflação (Focus para o ano seguinte e o outro contra
  a meta, a leitura "t+1 rolando" que está pendente lá) e o juro real ex-ante em série (hoje só
  uma linha da matriz de Condições). A Selic de fim de ano ficou lá, nas abas genéricas.
- **Aba Acompanhamento Condicionais — a edição de set/2026 do RPM saiu em 2026-09-24 e o anexo
  estatístico dela ainda não respondia no mesmo dia** (`AnexoRPM().vintages_disponiveis()` só
  achou até 2026-06). O ETL diário a pega quando a URL existir; não há nada a fazer na aba.
- ~~**A aba Apêndice documenta um modelo que não alimenta mais nada na tela.**~~ Resolvido
  removendo a aba (2026-09-24, ver "O Apêndice saiu").
- **Aba Projeções — o aviso de previsão velha não aparece mais na página.** Ele morava na
  faixa dentro da caixa verde, que saiu em 2026-09-23. `previsao.frescor` continua no payload e o
  `generate_report` continua imprimindo `AVISO previsao calculada com dado ate …` no console, então
  quem regera é avisado — quem só abre o HTML, não. Se a previsão voltar a envelhecer em silêncio, o
  lugar dela é uma oração na legenda do gráfico, do lado do corte de informação que já está lá, e
  não uma caixa nova.
- **Aba Projeções — a previsão pelo delta da Focus fica indefinida ~8 dias por trimestre.**
  Medido em 2026-09-23: o alvo da 282ª é 2028T2, a Focus só abriu esse trimestre em
  **10/07/2026** e a âncora disponível é o RPM de **25/06/2026** — 15 dias antes —, então o delta
  não tem "antes" para diferenciar e `previsto_focus` sai nulo. Não é acaso: o RPM sai ~8 dias
  depois da segunda reunião do trimestre (273ª→25/09, 275ª→18/12, 277ª→26/03, 279ª→25/06) e a
  Focus abre o trimestre-alvo no dia ~10 do trimestre seguinte, então a janela entre os dois
  produz o buraco **todo trimestre**, justo na semana seguinte a uma decisão. O backtest nunca o vê
  porque corta na data de cada reunião, onde o RPM já saiu — daí `anc_dias` ser 34–49 nas 18 e 91
  aqui. Enquanto não houver decisão sobre isso, a aba fica sem ponto previsto nesses dias e diz
  isso na chamada. **Com o seletor de previsão fora (2026-09-24) não há mais para onde cair**: o
  ponto some da tela nesses dias, em vez de trocar de método.

  E há uma segunda metade, medida em 2026-09-24: o RPM da 281ª foi publicado **nesse mesmo dia**,
  com 2028T2 = 3,1, e `_ancora()` filtra por `vintage < corte`. Com o corte no dia da geração, a
  âncora fresca fica de fora por um dia e a rodada volta a usar o RPM de 25/06. O `<` é
  **necessário no backtest** — ali o corte é a data da reunião, e o comunicado sai naquele dia, de
  modo que `<=` seria lookahead — e é **errado no caminho ao vivo**, onde um documento publicado
  mais cedo no mesmo dia já está no conjunto de informação. Separar os dois é uma linha; enquanto
  não for separado, basta rodar `antecipa_copom.salvar()` no dia seguinte a um RPM.
- **Antecipar a projeção — o que falta testar.** O delta da Focus ganha do ingênuo (MAE 0,079 contra
  0,100 em 18 reuniões) com repasse 1:1 e sem ajuste nenhum. Três coisas por ordem de retorno: (a) a Focus de
  **administrados** e de **livres** separadas, já que é o bloco de administrados que o modelo não tem;
  (b) o delta do **IPCA de curto prazo** (a Focus mensal dos próximos 3 meses), que é o canal pelo
  qual a notícia entra; (c) um coeficiente estimado no lugar do 1:1 — com n=17 isso é pescaria, então
  só vale quando a amostra crescer. Não tentar melhorar o modelo agregado para esta finalidade: o
  backtest mostra que o problema é o conjunto de informação trimestral, não o ajuste. Medido por
  tipo de horizonte as duas ficaram parecidas nas 18 (expansão 0,082 contra 0,089 do ingênuo,
  revisão 0,076 contra 0,111) — a vantagem da previsão é maior na revisão, onde o ingênuo piora.
  O intervalo entre âncora e reunião segue sendo a variável a explorar antes de qualquer coisa nova.
  **O modelo saiu da tela em 2026-09-24** e o backtest dele continua no script, com interruptor:
  ele é a evidência de que o caminho estrutural não paga, e apagá-lo apagaria a medição.
- **Os artefatos da previsão entraram no botão Regerar** (2026-08-31, depois de o usuário regerar o
  relatório e a previsão continuar a de seis dias antes). `generate_report.py` continua só lendo
  `data/` — de propósito: encadear `salvar()` dentro do `run()` custaria 36 rodadas do espaço de
  estados a cada geração. O que mudou é uma camada acima: `domain/dashboards/manifest.yaml` declara o
  passo de recálculo deste relatório em `procedures:` (`previsao`; até 2026-09-24 havia também
  `painel` e `modelo`), e `status.gerar()` — que é o que o botão **Regerar** da aba "Status
  dashboard" chama — o refaz antes quando está atrás. Medido: `salvar()` em 50,5s em 2026-08-31, com o
  modelo dentro; **15 s** em 2026-09-24, sem ele. A previsão é diária.
  Em paralelo, `antecipa_copom.frescor()` compara o `corte_usado` gravado no artefato com o `MAX` das
  três tabelas que `antecipar()` lê (seis até 2026-09-24) e `_load_antecipa()` embute isso em `previsao.frescor`. Até
  2026-09-23 a caixa da previsão imprimia isso como faixa — laranja se o HTML foi feito com artefato
  velho, verde se em dia —, e **com a caixa removida a faixa não tem mais onde aparecer**: o campo
  continua no payload e o aviso continua no console da geração, mas a página não o mostra.
  **O texto da faixa foi reescrito em 2026-09-01** (correção do usuário: a prosa dos dashboards
  não pode ser a nossa conversa sobre eles). Ela não imprime mais nome de tabela nem comando de
  terminal: `_FONTES_FRESCOR` passou a guardar `(coluna, nome)` — "a pesquisa Focus", "as
  projeções publicadas pelo Copom" — e `frescor()` devolve `fonte_nome` junto do `fonte_ref`, que
  segue existindo para o aviso de console da geração. O teste passou a exercitar a faixa laranja
  **sinteticamente**: ela não aparece no payload de um relatório recém-regerado, que é justamente
  o estado em que ninguém percebe que o texto dela envelheceu.
  **Segue pendente** o agendamento (junto do `bcb_copom`), que é o que tiraria a dependência de
  alguém clicar. Ver `domain/dashboards/CLAUDE.md`.

- **Aba Condições — a célula da próxima reunião na linha de projeção do BC é repetição, e
  deveria virar previsão.** O usuário pediu o observado por ora e disse que define o número
  depois de rever a aba Projeções. Quando entrar, a célula precisa dizer na tela que é
  estimativa — hoje ela é indistinguível de qualquer outra repetição cinza.
- **Aba Condições — ampliar o recorte.** As 25 variáveis de hoje cobrem inflação, atividade,
  condições financeiras e externas. Fora, por falta de dado e não de método: PIM/PMC/PMS, o
  hiato do BCB e o CDS de 5 anos (`cmb_risco_pais` é xlsx exportado à mão e costuma estar
  semanas atrás). Acrescentar qualquer um é uma entrada nova em `_spec()` — a mecânica de
  corte, σ e cor já é genérica, e desde 2026-09-22 vale para série diária, mensal **e
  trimestral**. **Antes de acrescentar, conferir que o grupo do `calendar_2026.yaml` tem
  `reference_period` nas entradas**: sem ele `regra()` devolve `None` e a série não tem como
  ser cortada por divulgação. O `bcb_focus` é a exceção que já existe — não tem
  `reference_period` (cada boletim é o estado corrente, não um período fechado), e por isso
  entra como `grupo_agenda`, que só alimenta a agenda e não corta série.
- **Aba Condições — o calendário de 2026 tem um rótulo errado, e ele está contornado, não
  corrigido.** `bcb_credit_note` carimba `2026-06` em 01/07 **e** em 30/07; pela cadência do
  grupo (abril→28/05, junho→30/07, julho→28/08) a primeira deveria ser `2026-05`. O módulo
  desempata pela data mais tarde e o ajuste da regra usa uma entrada por referência, então
  nenhuma célula fica errada — mas a entrada do YAML segue errada e o mês de maio do crédito
  cai na regra estimada em vez da data exata. Corrigir no `calendar_2026.yaml` é de uma linha.
- **Aba Condições — 55 das 225 células têm data de divulgação estimada**, porque
  `calendar_2026.yaml` só cobre 2026 e a janela de 8 reuniões chega a nov/2025. Em 6 delas a
  estimativa cai perto demais do fechamento para o erro da regra ser inofensivo, e a página
  marca. O corretivo definitivo é um calendário com as entradas de 2025; enquanto não houver,
  a marca é a resposta honesta.
- **Aba Condições — virada de ano.** `condicoes_copom.py` lê `calendar_2026.yaml` por nome
  fixo. Quando o calendário virar, ver `domain/release_calendar/ROLLOVER.md`; sem reunião
  futura no arquivo a aba degrada com mensagem em vez de quebrar, mas para de servir.
- ~~**Aba Projeções — comparar trajetória contra trajetória.**~~ O caminho de cada edição entrou em
  2026-09-25 (ver "O caminho de cada Relatório"). A metade que comparava com um caminho do modelo
  agregado foi com o modelo para `../structural_model/modelo_agregado/`.
- **Aba Projeções — livres e administrados antes de set/2024 existem só por ano.** O caminho
  trimestral deles começa em set/2024, quando o Relatório passou a publicá-lo. De set/2021 a jun/2024
  o anexo traz os dois **por ano civil** (Tab 2.2.4, depois 2.2.2); entrar com eles pede outro eixo
  (ano, não trimestre) e não foi pedido.
- **Aba Projeções — a variável que falta para virar função de reação.** A correlação de 0,27 entre
  desvio e passo é o que se mede hoje, e ela é fraca por construção: o desvio pequeno é resultado da
  política, não ausência de reação. O passo seguinte é acrescentar o juro real contra a neutra (que a
  eq. (3) já estima nesta pasta) — sem ele, duas reuniões com o mesmo desvio e Selic em 8% ou em 15%
  entram na mesma nuvem.
- **RPM: 43 tabelas lidas e não gravadas, todas por motivo registrado em `avisos`.** 32 são cenários
  **mistos** da grade 2×2 de 2016-2020 (juros de um tipo, câmbio de outro), que não cabem numa coluna
  `cenario` que classifica só o juro — precisariam de uma dimensão de câmbio. 4 são o par
  Básico/Alternativo com o mesmo juro (RI de dez/2002 e mar/2003), 4 ficaram sem cenário identificado
  (título em fonte de subconjunto sem cmap legível) e 7 foram classificadas por **ordem** das tabelas
  na página, e por isso têm `cenario_publicado` nulo. O **leque** de confiança (limites de 50/30/10%)
  está no `.md` de cada edição e não foi gravado, por decisão explícita de escopo. O RI de 1999-06
  não entra: publica o leque só como gráfico.
- **Confirmação em browser real** — feita em Chrome headless aba a aba (ver a seção de cada
  uma); a de Expectativas de Juros em 2026-09-24. Falta um olho humano no hover das duas abas
  novas, que o headless não exercita.
- **Comunicados: o que o parser lê mas não grava** — câmbio inicial do cenário e bandeira tarifária.
  São atributos de reunião, e a tabela irmã onde eles cabem já existe: `pm_copom_reuniao`, criada em
  2026-08-25 com a decisão de Selic. O câmbio inicial explica boa parte das revisões de projeção
  entre reuniões, e acrescentá-lo é uma coluna nova ali, sem migração. A decisão/direção saiu desta
  lista: está gravada, e de fonte melhor que o parser (SGS 432 cobre desde 1999, o texto só da 206ª).
- **Atas não estão no pipeline** — só o comunicado. A ata sai ~1 semana depois, em PDF.
