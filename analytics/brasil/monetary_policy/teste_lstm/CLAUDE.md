# teste_lstm/ — Contexto para o Claude

**Experimento, não produção.** A pergunta é uma só: um LSTM prevendo o IPCA 12 meses à frente bate
os benchmarks? Se não bater, esta pasta é apagada. Enquanto for teste, o `torch` **não entra no
`pyproject.toml`** — roda efêmero.

```powershell
# só os benchmarks (roda no venv do projeto, sem torch)
uv run python -m analytics.brasil.monetary_policy.teste_lstm.run --sem-lstm

# completo — torch efêmero por cima do venv do projeto, sem tocar no pyproject.toml
uv run --with torch python -m analytics.brasil.monetary_policy.teste_lstm.run

# quanto o vazamento do HP bilateral embelezaria (número NÃO reportável)
uv run python -m analytics.brasil.monetary_policy.teste_lstm.run --sem-lstm --hiato-vazado
```

| módulo | o que faz |
|---|---|
| `dados.py` | painel mensal: lê MySQL, defasa por data de publicação, transforma, monta os 12 alvos |
| `avaliacao.py` | o walk-forward **compartilhado** — folds, corte treino/teste, tabela de RMSE |
| `benchmark.py` | 5 competidores (`media12`, `sazonal`, `focus`, `focus_saz`, `ridge`) |
| `modelo.py` | o LSTM (janela → 12 saídas). É o único módulo que importa `torch` |
| `run.py` | entry point; grava RMSE, previsões e veredito em `data/` |

**Nunca passe `--python` aqui.** O `uv run --python 3.12` tenta **recriar o `.venv` do projeto**
naquela versão — só não destruiu porque o Windows tinha o diretório travado (`os error 32`). O venv
do projeto é **Python 3.10.2**, o `torch` tem wheel para ele, e `--with torch` sozinho monta uma
camada efêmera em cima sem escrever no `pyproject.toml`. Também não precisa de `--with-editable .`:
o projeto já está instalado editável no venv, e passar isso junto foi o que puxou a reconstrução.
(O `python` do PATH é 3.14 e não tem relação com o do projeto — foi essa confusão que gerou o
comando errado.)

## O que o painel é

Alvo: variação % mensal do IPCA, **cabeça de 12 saídas** (um mês por saída, não a acumulada), para
comparar mês a mês contra a Focus. A linha `t` contém só o que estava **publicado** no fim do mês
`t`, e o alvo são os 12 IPCA que ainda não saíram — meses `t` a `t+11`. O IPCA de `t` está no alvo,
não nas features, porque só é divulgado em `t+1`.

| bloco | tabela | transformação | defasagem de publicação |
|---|---|---|---|
| IPCA (alvo e inércia) | `inflc_agregados.ipca` | já é taxa %; + lags 2, 3, 12 e o acum. 12m | 1 mês |
| Expectativas | `expc_focus` (`horizonte='12m'`, `suavizada='S'`) | nível % + variação | 0 |
| Hiato | `atv_ibcbr.ibcbr_sa` → HP em tempo real | nível (desvio %) | 2 meses |
| Commodities USD | `comm_icbr_usd` | log-diff × 100 | 1 mês |
| Câmbio | `cmb_ptax.ptax_venda` | log-diff da **média do mês** × 100 | 0 |

**Amostra utilizável: 2008-02 a 2025-08, 211 meses** com features e alvo completos, e o gargalo
não é o IPCA nem a Focus — é o hiato. O IBC-Br começa em 2003-01 e o `HP_MIN_OBS = 60` do HP em
tempo real exige 5 anos de aquecimento, o que come até 2008. Teste: 2015-01 a 2025-08, **128 meses
em 11 folds** anuais.

## Medições desta rodada (2026-09-02)

**O hiato mensal do IBC-Br não é substituto do hiato do BC, e em tempo real ele é quase outra
coisa.** Medido contra `pm_hiato_produto.central`:

| versão do HP | corr em nível | corr em diferença | n |
|---|---|---|---|
| **bilateral** (λ=14.400, amostra toda) | +0,54 | +0,79 | 91 |
| **tempo real** (λ=14.400, o que o código usa) | **+0,21** | +0,76 | 74 |

E o custo do viés de ponta, medido entre as **duas versões da mesma série**: correlação +0,71,
desvio absoluto médio de **1,29 p.p.** e máximo de 3,35 — contra um hiato cujo desvio-padrão é ~2
p.p. Ou seja, mais de meio desvio-padrão de ruído puro de vintage. O ciclo sobrevive (a correlação
em diferença cai só de 0,79 para 0,76), o **nível** não.

Isso é a explicação mais provável de o Ridge não tirar nada do hiato, e é o argumento mais forte da
pendência "testar sem o hiato". Hoje as duas séries discordam até de sinal: nos últimos 4 trimestres
o do IBC-Br está entre −0,85 e −0,07 e o do BC entre +0,82 e +0,36.

Por λ, na versão **bilateral**: +0,42 (1.600), +0,54 (14.400), +0,71 (129.600), +0,88 (1e6). **Não
subir o λ só porque a correlação melhora** — isso é ajustar o proxy ao alvo, e o hiato do BC é ele
mesmo um objeto de modelo.

**A régua** (RMSE em p.p. de IPCA mensal, 128 meses fora da amostra) está na seção de resultado
abaixo. Três leituras dos benchmarks que valem mais que a tabela. **A média sazonal pura empata com a Focus** — o que a
pesquisa acrescenta sobre "cada mês repete a média histórica dele" é ~0 no RMSE mensal, e o
`focus_saz` (nível da Focus + forma sazonal) empata com as duas. **O Ridge, com as 10 features, é
pior que a média sazonal**, e o padrão por horizonte diz por quê: ele ganha em h1-h2 (0,338 contra
0,394) e perde de h3 em diante. Fora de 2 meses, as features não informam. **E `focus` e
`focus_saz` têm `acum12m` idêntico por construção** — o perfil sazonal só redistribui dentro dos 12
meses —, o que serve de checagem de implementação.

## O resultado (2026-09-02)

Duas rodadas no mesmo dia. A primeira sem dummy de calendário, a segunda com — **as 12 dummies de
mês viraram o veredito**, e é o achado principal.

| modelo | médio (s/ dummy) | **médio (c/ dummy)** | acum. 12m |
|---|---|---|---|
| **`lstm`** | 0,3957 (3º) | **0,3817 (1º)** | **2,526** |
| `sazonal` | 0,3869 | 0,3869 | 2,743 |
| `focus_saz` | 0,3870 | 0,3870 | 2,751 |
| `ridge` | 0,4057 | 0,3908 | 2,690 |
| `focus` | 0,3985 | 0,3985 | 2,751 |
| `media12` | 0,4273 | 0,4273 | 3,388 |

O LSTM saiu de +2,3% *atrás* do melhor benchmark para **−1,3% à frente**, um ganho de 3,5% só com
informação de calendário. O Ridge também ganhou (0,4057 → 0,3908), o que era esperado e é o motivo
de as dummies entrarem no conjunto **compartilhado** de features: um ganho que só o LSTM recebesse
não seria comparação.

**Onde o ganho aparece confirma o diagnóstico.** O LSTM era o pior de todos nos horizontes curtos,
onde a sazonalidade explica quase tudo; com as dummies o degrau desaparece:

| horizonte | s/ dummy | c/ dummy |
|---|---|---|
| h1 | 0,405 | **0,387** |
| h2 | 0,410 | **0,390** |
| h3 | 0,409 | **0,384** |
| h11 | 0,386 | 0,371 |

Custo: 6.028 → **7.564 parâmetros** (70 por janela de treino, contra 108 janelas). O early stopping
para mais cedo — 84 épocas contra 114 —, o que é o sinal esperado de a rede não precisar mais gastar
capacidade descobrindo o calendário.

### O que a checagem por ano mostra, e ela muda a leitura

O veredito **sobrevive** ao teste que derrubou o resultado da primeira rodada. Excluindo 2015 — o ano
que sozinho produzia a falsa vitória no acumulado —, a ordem se mantém: LSTM 0,3835, `sazonal`
0,3903, `ridge` 0,3918, `focus_saz` 0,3921.

**Mas não é vitória ano a ano.** O LSTM ganha de `sazonal` em 5 de 11 anos e de `focus_saz` em
apenas **3 de 11**. O agregado vira a favor dele porque ele perde pouco nos anos calmos e ganha
muito nos ruins:

| ano | `focus_saz` | `lstm` | |
|---|---|---|---|
| 2016-2019 | 0,281-0,383 | 0,328-0,450 | Focus ganha, com folga |
| **2020** | 0,563 | **0,423** | LSTM ganha 25% |
| **2021** | 0,635 | **0,582** | LSTM ganha 8% |
| 2023-2025 | 0,201-0,269 | 0,194-0,277 | empate técnico |

Então a afirmação defensável não é "o LSTM prevê melhor o IPCA" — é **"o LSTM degrada menos na
virada de regime"**, e num critério de erro quadrático sobre 11 anos isso basta para ficar em
primeiro. Para quem previsse mês a mês em tempo normal, a Focus com forma sazonal continua melhor.

**E o tamanho da vitória é 1,3%, sem teste de significância.** Com 128 meses e janelas sobrepostas,
isso pode não ser distinguível de zero — ver pendências.

## Decisões que o protocolo fixa

- **O hiato é de tempo real** (`hiato_ibcbr_realtime`): para cada mês, o HP roda só com dado até
  ali e guarda a última observação. O HP é bilateral, então filtrar a amostra toda e depois cortar o
  teste injeta futuro em todo ponto histórico — e o vazamento não levanta exceção, só melhora o
  RMSE. `--hiato-vazado` existe para medir o tamanho disso, não para reportar.
- **Padronização com média/desvio do treino de cada fold.**
- **Avaliar exige alvo completo**, senão cada horizonte sairia medido em meses diferentes e o
  `medio` da tabela misturaria períodos.
- **A validação do early stopping é purgada.** Janelas vizinhas compartilham 23 dos 24 meses *e* os
  alvos se sobrepõem 12 meses, então um hold-out cortado no meio das janelas quase repete o treino.
  A purga (`JANELA + HORIZONTE` = 36 janelas descartadas na fronteira) cobre as duas vias.
- **Um par (média, desvio) para os 12 horizontes**, não um por horizonte: padronizar por horizonte
  faz o modelo minimizar erro relativo e o RMSE deixa de ser comparável com os benchmarks.

## Pendências

- **A decisão de continuar ou não é do usuário.** O veredito de hoje é "não bate", com a estrutura
  pronta para reteste em um comando. Por ordem de retorno, se continuar:
- **Diebold-Mariano, e agora é a pendência que manda.** A vitória é de 1,3% com 128 meses e
  janelas sobrepostas; sem teste de significância com correção para sobreposição (o que o paper do
  HNN faz na Tabela 2), "fica em primeiro" não é "é melhor". É o único item que pode mudar o
  veredito.
- **A outra forma de dar sazonalidade, ainda não testada:** prever o **desvio** contra o perfil
  sazonal em vez do nível. Custa 0 parâmetro (as dummies custaram 1.536) e torna o `focus_saz` o
  baseline explícito, com o LSTM modelando só o resíduo. Vale medir contra a versão com dummy.
- **Testar sem o hiato.** Ganha 2003-2008, ~60 meses (+55% de treino no primeiro fold), e o Ridge
  sugere que o hiato não é o que informa. O gargalo de amostra é ele, não o IPCA nem a Focus.
- **Nenhum teste de significância foi feito.** Com 128 meses e séries sobrepostas, +2,3% pode não
  ser distinguível de zero. Antes de qualquer conclusão mais forte que "não bate", cabe um
  Diebold-Mariano com correção para sobreposição (é o que o paper do HNN faz na Tabela 2).
- **Decidir o hiato** entre o do IBC-Br (mensal, tempo real, o que está no código) e o do BC
  (trimestral, com vintages em `pm_hiato_produto_vintages`, mas exige interpolar). A discordância de
  sinal de hoje torna isso material, não cosmético.
- **`ptax_fim` está carregado e não usado** — o painel usa a média do mês. Trocar é uma linha; qual
  serve melhor não foi medido.

## Referência

`2202.04146v2.pdf` (na raiz do projeto, ainda fora do pipeline de ingestão) — "A Neural Phillips
Curve and a Deep Output Gap", Goulet Coulombe. Trimestral, 1960Q1–2024Q1 = **257 observações** e
**>2 milhões de parâmetros**; o que segura o overfit é a arquitetura restrita, early stopping em
hold-out de 35%, dropout 0,2 e ensemble de 50 divisões. É um **MLP de previsão direta** — não gera
trajetória e não é motor de cenário; o tempo entra pelas features (4 defasagens + médias móveis de
ordem 2, 4 e 8), não pela arquitetura. Os "hemisférios" dele (expectativas, atividade, commodities)
são a origem dos blocos de input daqui.
