# -*- coding: utf-8 -*-
"""O simulador: roda as equacoes para a frente, em vez de so estima-las.

Hoje **as cinco equacoes do modelo**, na ordem de solucao dentro do trimestre:

    (H) curva IS         -> hiato do produto         `bayes/is_bayes.py`
    (I) curva de Phillips -> IPCA do trimestre       `bayes/phillips_bayes.py`
    (E) expectativas     -> Focus de 12 meses        `bayes/expectations_bayes.py`
    (R) regra de juros   -> Selic                    `bayes/taylor_bayes.py`
    (F) cambio           -> variacao do cambio       `bayes/fx_bayes.py`

Todas entram pela versao BAYESIANA da mesma equacao que a aba dela estima, porque o
simulador precisa de uma faixa e estimativa pontual nao tem uma para dar. A regra e do
usuario, em 2026-09-25: *"no sistema vamos sempre usar o bayes para todas as equacoes"*.
Na pagina a aba se chama **Structural Model** desde 2026-09-28, a pedido dele: e o modelo
agregado, as cinco juntas.

## Os elos, e desde 2026-09-28 um LACO

    (R) -> (H)   a Selic, pela distancia ate a ancora rr_10a + meta  um trimestre depois
    (H) -> (I)   o hiato, em servicos, alimentacao e industriais      mesmo trimestre
    (F) -> (I)   o cambio MEDIO: alimentacao agora, industriais depois
    (E) -> (I)   a expectativa, como a ancora de cada grupo           um trimestre depois
    (I) -> (E)   a inflacao, composta em doze meses                   mesmo trimestre
    (E) -> (R)   a expectativa, pela distancia ate a meta             mesmo trimestre
    (R) -> (F)   a Selic, pelo carry sobre a vol implicita            mesmo trimestre
    (I) -> (F)   a inflacao, pelo diferencial contra a americana      mesmo trimestre

Ate a (I) entrar era uma corrente `E -> R -> H -> F`, e cada equacao rodava uma vez so. Com
ela a inflacao volta para a expectativa e para o cambio, e o hiato e o cambio voltam para a
inflacao: `resolver()` da voltas ate nenhum caminho mudar mais (10 no cenario padrao). O
unico elo no sentido contrario da ordem DENTRO do trimestre e a alimentacao lendo o cambio
do proprio trimestre; o ganho dele e 0,007, e e por isso que as voltas sao poucas.

Medidos no cenario que a aba abre, no fim dos 12 trimestres, com a curva de Phillips ligada
contra desligada (a inflacao segurada na media dos ultimos quatro trimestres): Focus 3,20
contra 3,64, Selic 11,28 contra 11,91, hiato -0,60 contra -0,72, cambio R$ 5,29 contra
5,38. O IPCA de doze meses vai de 4,64 a 3,36, passando por 5,45 no fim de 2026 -- o
2025T4 de 0,60% sai da janela e o 2026T4 que entra carrega a sazonalidade do quarto
trimestre.

O carry era o elo fraco e ficou mensuravel em 2026-09-25, quando o denominador passou da
volatilidade REALIZADA defasada para a IMPLICITA de 3 meses das opcoes de dolar, medida no
proprio trimestre (o argumento esta em `equations/fx.py`, `vol_trimestral`): mediana -0,58
com 85% da massa abaixo de zero virou **-1,35 com 99,7%**. O que entra na conta e a
VARIACAO do canal -- 2 p.p. de Selic so no primeiro trimestre, voltando depois, nao deixam
efeito nenhum no nivel ao fim, so no trimestre em que aconteceram. E propriedade da
especificacao em diferenca, contraintuitiva o bastante para estar afirmada no teste.

O plano do usuario, em 2026-09-22, foi acrescentar uma de cada vez: *"vamos ajeita-la e
depois vamos adicionar outra equacao."*

## Dois blocos, e a razao de serem dois

Desenho pedido pelo usuario em 2026-09-22, depois de olhar o bloco de stress test do
`FX Report`:

- **As equacoes** -- uma por conta, com o que ela produz desenhado contra o observado.
  Os pesos sao os estimados e **nao sao controle**: o usuario decidiu isso em
  2026-09-22, *"a simulacao vem dos inputs"*. A equacao escrita, os pesos e a estimacao
  vivem na aba daquela equacao, e nao aqui.
- **Os inputs** -- uma por variavel que alimenta alguma conta, com o CAMINHO dela como
  controle. E aqui que o cenario se monta.

A separacao continua nao sendo cosmetica, so que o corte mudou de lugar: o bloco 1 e o
que o modelo AFIRMA e o bloco 2 e o que o usuario SUPOE. Um painel so -- que e o que o
simulador do `monetary_policy` faz -- nao distingue os dois.

## Endogena e exogena sao propriedades DO MODELO, e mudam

Uma variavel e endogena quando alguma equacao DO SIMULADOR a produz. Como as equacoes
entram uma de cada vez, a mesma variavel muda de lado ao longo do tempo -- e o payload
carrega os dois fatos separados, porque eles respondem perguntas diferentes:

    produzida_por     qual equacao do MODELO a produz, exista ela no simulador ou nao
    produtor_no_sim   se essa equacao ja esta no simulador

Desde 2026-09-28 as cinco variaveis que o modelo produz sao endogenas aqui: a `infl_br`
foi a ultima a fazer o caminho, quando a curva de Phillips entrou. Os dois campos continuam
separados porque o caso volta no dia em que o modelo ganhar uma equacao antes de ela
entrar no simulador -- e o selo do cartao e que diz isso ao leitor.

## As tres fontes de caminho de uma variavel

    equacao     ENDOGENO   -- o caminho sai de uma equacao DO SIMULADOR
    digitado    EXOGENO    -- o caminho e imposto, valor a valor
    observado   OBSERVADO  -- o que foi publicado e, passado o ultimo dado, o ultimo
                              valor repetido para a frente

Os rotulos na tela sao os tres em maiusculo inicial, a pedido do usuario em 2026-09-22.
As chaves continuam as antigas porque sao contrato entre o payload e o navegador -- o
nome que se le mora ao lado, no mapa `SIM_FONTE_ROT` do relatorio.

**"Endogeno" e propriedade DESTA RODADA, e o selo do cartao e propriedade do MODELO.**
Os dois podem discordar de proposito: a Selic e endogena na taxonomia e pode ser rodada
como exogena, que e o que desliga a regra de juros. Uma variavel que nenhuma equacao do
simulador produz nao recebe a pill "Endogeno" -- nao ha de onde.

## Conta nao e premissa, e desde 2026-09-25 a conta mora na EQUACAO

Nove numeros que as equacoes usam nao tem cartao, de proposito:

    di      = pi_e    - meta_12m           expectativa de 12 meses contra a meta     (R)
    ancora  = rr_10a  + meta_12m           juro real de equilibrio mais a meta       (R)
    gap     = selic - rr_10a - meta_12m    a Selic contra essa mesma ancora          (H)
    de_med  = 50*ln(P_t / P_t-2)           a variacao do cambio MEDIO do trimestre   (I)
    agr     = 100*dlog(IC-Br agro)         a variacao das commodities agricolas      (I)
    met     = 100*dlog(IC-Br metal)        a variacao dos metais                     (I)
    i12     = 4 trimestres de infl_br      o IPCA de 12 meses, composto              (E)
    ppp     = infl_br - infl_us            inflacao do trimestre aqui menos a de la  (F)
    carry   = (selic - ffr) / vol          o premio de juro sobre a vol esperada     (F)

Cada um deles se calcula de cartoes que existem, e dar cartao a qualquer um deixaria
digitar um numero que contradiz as proprias pecas -- que e exatamente o que a regra da
caixa ("ela mostra o numero que aquele trimestre vai usar") proibe.

Os tres primeiros eram cartoes compostos, com as pecas atras de um "abrir em partes",
ate o setimo round. Hoje sao declaracoes `deriva` na equacao que os CONSOME, com a
operacao e as pecas nomeadas; a conta nao existe sem consumidor, e a ficha da equacao
imprime as duas listas -- o que ela consome e o que ela forma com isso. O `carry_vol`
nunca teve cartao, pela mesma razao, e foi ele que deu o precedente.

## Horizonte

**Maximo de 12 trimestres**, decisao do usuario em 2026-09-22. Isso fixa o numero de
caixas por variavel em 12 e dispensa a logica de "o que acontece depois da ultima caixa",
que e onde o FX Report precisa de uma regra ("segue no ultimo valor").

**As duas marcas de crise nao sao input.** Elas entram na conta com o peso que a
estimacao mediu e valem 0 em todo trimestre projetado. Tiveram cartao ate 2026-09-24,
quando o usuario as cortou: *"pretendo usa-las mais como ajuste do que variaveis
exogenas"*. Ligar uma no futuro era simular "um choque do tamanho daquela crise", que
e uma pergunta legitima e nao e a que esta tela responde -- o choque em qualquer
tamanho ja se aplica pelos cartoes que sobraram.

**E a janela e FIXA: os `H_PADRAO` trimestres seguintes ao fim da janela estimada.**
Nao ha "comecar em" -- decisao do usuario em 2026-09-22, *"sempre projeta para frente da
janela estimada"*. Estimando ate 2026T2, a projecao e 2026T3..2029T2.

O que isso compra e a **pratica do FX Report**: a janela nao se mexe quando o dado anda,
entao o trimestre que sai passa a cair DENTRO dela. Um periodo da janela que ja tem dado
publicado aparece travado e verde -- o `final` do `FC.nowcast` de la, cuja razao esta
escrita no CSS daquele arquivo: *"so a guess never overrides data that's already known"*.
A tela se atualiza sozinha conforme o dado sai, sem reestimar e sem ninguem mexer num
seletor; reestimar move o corte e a janela anda junto.

**O preco, declarado:** nao da mais para rodar a conta sobre a historia pela tela. A
funcao continua aceitando qualquer `i0` -- e como `main()` e o teste a chamam -- mas a
pagina so oferece a janela a frente.

## O que roda onde

Nao ha MCMC na geracao do relatorio. Este modulo le os cinco `bayes/data/*_draws.json`,
gravados pelo `salvar_desenhos()` de cada modulo bayesiano. A recursao roda no NAVEGADOR,
porque o usuario mexe nos controles; `_sim_is()`, `_sim_infl()`, `_sim_exp()`, `_sim()`,
`_sim_fx()` e `resolver()` aqui sao a mesma conta, e servem para o teste conferir as duas
pontas contra o mesmo caso -- cada equacao leva um gabarito de um passo no payload, e o
laco leva o dele: `sistema_padrao`, o cenario que a aba abre resolvido do lado do Python.

Uso:
    uv run python -m analytics.brasil.structural_model.simulator
"""
from __future__ import annotations

import json
import pathlib

import numpy as np
import pandas as pd

from analytics.brasil.structural_model import panel
from analytics.brasil.structural_model.equations import (expectations, fx, is_curve,
                                                         taylor)
from analytics.brasil.structural_model.equations import phillips_sub as ph
from analytics.brasil.structural_model.modelo_agregado.modelo_painel import (para_q,
                                                                             serie)

_BAYES = pathlib.Path(__file__).resolve().parent / "bayes" / "data"
DESENHOS = _BAYES / "taylor_draws.json"
DESENHOS_FX = _BAYES / "fx_draws.json"
DESENHOS_EXP = _BAYES / "exp_draws.json"
DESENHOS_IS = _BAYES / "is_draws.json"
DESENHOS_PH = _BAYES / "phillips_draws.json"

# Horizonte, em trimestres. Comecou em 8 e foi a 12 no mesmo dia, a pedido do usuario
# -- tres anos. E o ponto de partida padrao e o PRIMEIRO TRIMESTRE APOS o ultimo dado:
# a aba abre projetando para a frente, e rodar sobre a historia e um backtest que se
# pede trocando o "Comecar em".
H_MAX = 12
H_PADRAO = 12

# Quantos trimestres a media de "segurar" usa, nas variaveis que sao TAXA DE FLUXO.
#
# A regra da casa e uma so -- passado o ultimo dado, segure o ultimo valor -- e ela e
# certa para NIVEL: o CDS de hoje e a melhor leitura do CDS de amanha. Numa taxa de
# fluxo ela nao e: o diferencial de inflacao de UM trimestre tem desvio-padrao de 0,94
# p.p., maior que a propria media, e ele carrega quase toda a projecao do cambio por
# entrar com peso imposto em 1. Segurar a leitura de 2026T2 (+0,72) dava +2,91% ao ano;
# a media de quatro trimestres (+0,28) da +1,14%. Sao 5,6 p.p. de cambio em tres anos
# escolhidos por uma premissa.
#
# A escolha e do usuario, em 2026-09-24 (*"pode colocar a media dos ultimos 4
# trimestres"*), e ela e DECLARADA POR VARIAVEL e nao imposta ao painel: `ppp`,
# `infl_br` e `infl_us` sao as unicas taxas de fluxo aqui; todo o resto e nivel.
SEGURA_MEDIA_K = 4
_SEGURA_MEDIA = {"modo": "media", "k": SEGURA_MEDIA_K}

_COMO_GERAR = "uv run python -m analytics.brasil.structural_model.bayes.taylor_bayes"
_COMO_GERAR_FX = "uv run python -m analytics.brasil.structural_model.bayes.fx_bayes"
_COMO_GERAR_EXP = ("uv run python -m "
                   "analytics.brasil.structural_model.bayes.expectations_bayes")
_COMO_GERAR_IS = "uv run python -m analytics.brasil.structural_model.bayes.is_bayes"
_COMO_GERAR_PH = ("uv run python -m "
                  "analytics.brasil.structural_model.bayes.phillips_bayes")

# Os dois recortes em que as exogenas se dividem, a pedido do usuario em 2026-09-25.
# O criterio e DE QUEM e a variavel, e nao onde ela e negociada: a volatilidade
# implicita do dolar e domestica por ser o preco do risco de um ativo brasileiro,
# embora as opcoes sejam negociadas la fora; as commodities em dolar sao externas
# porque quem forma o preco esta fora, mesmo que a cesta seja a da pauta de
# exportacao brasileira. O segundo exemplo e o que mostra que o criterio nao e
# 'onde negocia' -- os dois seriam externos por essa regua, e so um e.
REGIOES = {
    "domestica": ("Doméstica", "decididas ou formadas no Brasil"),
    "externa": ("Externa", "formadas fora, e o Brasil as recebe"),
}


def _ser(s: pd.Series) -> list:
    """Serie -> lista com None no lugar de NaN, que e o que o JSON aceita."""
    return [None if pd.isna(v) else round(float(v), 6) for v in s]


def carregar_desenhos(caminho: pathlib.Path | None = None) -> dict:
    """Le os desenhos gravados pela estimacao bayesiana."""
    caminho = caminho or DESENHOS
    if not caminho.exists():
        raise FileNotFoundError(
            "%s nao existe. O simulador nao roda MCMC durante a geracao do relatorio; "
            "gere os desenhos antes com:\n    %s" % (caminho, _COMO_GERAR))
    return json.loads(caminho.read_text(encoding="utf-8"))


def carregar_desenhos_fx(caminho: pathlib.Path | None = None) -> dict:
    """Idem, para a equacao (F)."""
    caminho = caminho or DESENHOS_FX
    if not caminho.exists():
        raise FileNotFoundError(
            "%s nao existe. Gere os desenhos da equacao do cambio antes com:\n    %s"
            % (caminho, _COMO_GERAR_FX))
    return json.loads(caminho.read_text(encoding="utf-8"))


def carregar_desenhos_exp(caminho: pathlib.Path | None = None) -> dict:
    """Idem, para a equacao (E)."""
    caminho = caminho or DESENHOS_EXP
    if not caminho.exists():
        raise FileNotFoundError(
            "%s nao existe. Gere os desenhos da equacao de expectativas antes "
            "com:\n    %s" % (caminho, _COMO_GERAR_EXP))
    return json.loads(caminho.read_text(encoding="utf-8"))


def carregar_desenhos_is(caminho: pathlib.Path | None = None) -> dict:
    """Idem, para a equacao (H)."""
    caminho = caminho or DESENHOS_IS
    if not caminho.exists():
        raise FileNotFoundError(
            "%s nao existe. Gere os desenhos da curva IS antes com:\n    %s"
            % (caminho, _COMO_GERAR_IS))
    return json.loads(caminho.read_text(encoding="utf-8"))


def carregar_desenhos_ph(caminho: pathlib.Path | None = None) -> dict:
    """Idem, para a equacao (I) -- os quatro grupos, com os desenhos JA PAREADOS."""
    caminho = caminho or DESENHOS_PH
    if not caminho.exists():
        raise FileNotFoundError(
            "%s nao existe. Gere os desenhos da curva de Phillips antes com:\n    %s"
            % (caminho, _COMO_GERAR_PH))
    return json.loads(caminho.read_text(encoding="utf-8"))


# ─────────────────────────────────────────────────────────────────────────────
# as variaveis
# ─────────────────────────────────────────────────────────────────────────────
# As cinco equacoes do MODELO, e nao so as que ja estao no simulador. A organizacao do
# bloco 2 e sobre o MODELO: uma exogena e GERAL quando mais de uma equacao a le, tenha
# ou nao essa equacao entrado no simulador ainda. Fosse contado so sobre o que roda, a
# mesma variavel trocaria de grupo a cada equacao nova -- e o mapa deixaria de ser um
# mapa do modelo para ser um retrato do estado da obra.
EQS_MODELO = {
    "I": "Curva de Phillips",
    "E": "Expectativas",
    "H": "Curva IS",
    "R": "Regra de juros",
    "F": "Câmbio",
}


def _insumos_fx(df: pd.DataFrame, am_idx) -> dict:
    """Os niveis trimestrais que a equacao (F) consome, na grade do simulador.

    ## O `carry_vol` e RECONSTRUIDO, e da Selic que a (R) produz

    O canal e `(Selic - Fed Funds) / volatilidade`. Na estimacao a Selic entra pelo
    FECHAMENTO do trimestre; a (R) produz a MEDIA. Um simulador que ligue as duas tem
    de usar uma no lugar da outra, e a escolha aqui e a media -- porque e a que a
    equacao do simulador produz, e porque a alternativa (ancorar no fechamento e
    projetar com a media) poria um degrau de convencao exatamente no primeiro trimestre
    projetado, que e o que ninguem ve.

    **Medido**, 2006T2 a 2026T2: media e fechamento diferem 0,384 p.p. em media e
    1,565 p.p. no pior trimestre (2021T4, no meio do ciclo de alta). Na VARIACAO do
    canal -- que e o que o coeficiente multiplica -- isso vale 0,0217 em media e 0,0701
    no maximo, ou **0,049 p.p. de cambio em media e 0,16 p.p. no pior trimestre**,
    contra um RMSE de 3,59 p.p. por trimestre da propria equacao. E a pendencia F2
    (convencoes de trimestralizacao) ganhando um consumidor e um numero.

    O Fed Funds nao e consultado de novo: ele sai por identidade do que ja esta
    carregado, `ffr = selic_fim - carry`. Reconstruido assim, `(selic_fim - ffr)/vol`
    devolve o `carry_vol` da estimacao com erro maximo de 0,000000 -- o que e a prova
    de que a identidade fecha e de que o resto da diferenca e so convencao de Selic.

    ## A volatilidade entra no PROPRIO trimestre desde 2026-09-25

    O denominador passou a ser a vol implicita de 3 meses das opcoes de dolar, medida no
    fechamento do trimestre -- uma cotacao, como o CDS, e nao uma medicao do passado
    (o argumento inteiro esta em `fx.vol_trimestral`). A consequencia aqui e concreta:
    a serie NAO vai mais um trimestre alem da grade. Com a vol realizada defasada, a do
    primeiro trimestre projetado ja era conhecida e a caixa nascia travada e verde; com
    a implicita contemporanea ela e premissa que se digita, como as outras quatro desta
    equacao. Manter o trimestre a mais aqui imprimiria como observado um numero que
    ninguem observou.
    """
    if fx.VOL_SOURCE != "implicita":
        raise ValueError(
            "o cartao da volatilidade deste simulador esta escrito para a vol IMPLICITA "
            "(nome, instrucao e nota dizem 'implicita de %s das opcoes de dolar'), e "
            "fx.VOL_SOURCE e %r. Trocar a fonte sem trocar o texto poe na tela o nome de "
            "uma serie e na conta outra. Ajuste os dois juntos." % (fx.VOL_PRAZO,
                                                                   fx.VOL_SOURCE))

    n = fx.niveis()
    m = fx._mensal()
    carry_q = fx._para_q(m["carry"], como="last")
    ffr = df["selic_fim"] - carry_q
    vol = fx.vol_trimestral()

    return {
        "niveis": n,
        "ffr": ffr,
        "vol": vol,
        "de": 100 * np.log(n["ptax"]).diff(),
        "ptax": n["ptax"],
        "infl_br": 100 * np.log(n["ipca_index"]).diff(),
        "infl_us": 100 * np.log(n["cpi_index"]).diff(),
        "carry_vol": (df["selic"] - ffr) / vol,
    }


# As duas cestas de commodity que a (I) le, em NIVEL. O painel guarda so a variacao
# (`pi_agr_usd`, `pi_met_usd`), e a variacao nao serve de cartao: segurar o ultimo valor
# de uma VARIACAO projetaria a alta do ultimo trimestre por tres anos, enquanto segurar o
# ultimo NIVEL projeta commodity parada -- a leitura neutra, a mesma dos canais da (F). A
# variacao volta a ser conta, `100*dlog`, declarada no `deriva` da (I).
_ICBR_I = {
    "icbr_agr_usd": ("icbr_agropecuaria_usd", "pi_agr_usd"),
    "icbr_met_usd": ("icbr_metal_usd", "pi_met_usd"),
}


def _insumos_inflacao(df: pd.DataFrame) -> dict:
    """Os niveis trimestrais das duas cestas de commodity que a (I) le.

    Media do trimestre, que e a convencao do painel para commodity (`panel.py`, "tres
    convencoes"): o que o produtor enfrentou foi o preco medio, nao o do ultimo dia.

    **Levanta** se `100*dlog` do nivel nao devolver a coluna do painel que a estimacao
    usou. A conta que a equacao faz com o cartao tem de ser a identidade do painel, e
    medido ela e -- 3,6e-15 no pior trimestre.
    """
    out = {}
    for k, (col_db, col_painel) in _ICBR_I.items():
        nivel = para_q(serie("macro_brasil", "comm_icbr_usd", col_db))
        var = 100 * np.log(nivel).diff()
        dif = (var - df[col_painel]).dropna().abs()
        if len(dif) == 0 or float(dif.max()) > 1e-9:
            raise ValueError(
                "o nivel de %s nao reproduz a coluna %s do painel (pior %.2e): o cartao "
                "e a estimacao estariam lendo series diferentes"
                % (col_db, col_painel, float(dif.max()) if len(dif) else float("nan")))
        out[k] = nivel
    return out


# Os quatro canais da (F) que sao premissa DIRETA -- o quinto, `carry_vol`, e conta e
# nao premissa, entao quem tem cartao sao as duas pecas dele que o leitor escolhe
# (Fed Funds e volatilidade). A Selic, a terceira peca, ja tem cartao proprio.
_FX_CANAIS_CARTAO = {
    "fiscal": ("Risco fiscal (CDS de 5 anos)", "pontos-base",
               "Bloomberg, CDS soberano de 5 anos",
               "risco fiscal (CDS de 5 anos)",
               "O prêmio que o mercado cobra para carregar risco de crédito do "
               "Brasil por cinco anos. É o canal mais forte da equação: um susto "
               "fiscal aparece aqui antes de aparecer em qualquer outro lugar."),
    "dxy_em": ("Dólar contra emergentes", "pontos do índice",
               "Bloomberg, índice de dólar contra moedas emergentes",
               "dólar contra emergentes",
               "A força do dólar contra as moedas emergentes em geral. Separa o que "
               "é movimento do dólar no mundo do que é movimento do real."),
    "sp500": ("Bolsa americana (S&P 500)", "pontos do índice",
              "Yahoo Finance, S&P 500",
              "bolsa americana (S&P 500)",
              "O apetite por risco lá fora. Sozinha, bolsa subindo vem com real mais "
              "forte; segurados o CDS e o dólar contra emergentes, o sinal se inverte "
              "— o coeficiente desta equação é condicional a eles."),
    "icbr_usd": ("Commodities em dólar (IC-Br)", "pontos do índice",
                 "Banco Central, Índice de Commodities Brasil em dólar",
                 "commodities em dólar (IC-Br)",
                 "O preço em dólar da cesta de commodities que o Brasil exporta. "
                 "Commodity mais cara é termo de troca melhor, e real mais forte."),
}



# A regra e a mesma nos quatro -- a equacao le a VARIACAO do canal e nao o nivel --, e
# por isso a primeira versao repetia a MESMA frase nos quatro cartoes, um atras do
# outro. Quatro paragrafos identicos em sequencia nao se leem: o olho pula o segundo.
# Cada cartao diz a consequencia DELE, que e a mesma regra no vocabulario daquele canal.
_FX_CANAIS_NOTA = {
    "fiscal":
        "A equação não lê o patamar do CDS: lê o quanto ele **anda** de um trimestre para o outro, dividido pelo desvio-padrão histórico dessa variação. Um CDS parado em 300 pontos não desvaloriza nada — o que desvaloriza é ele ir de 120 para 300.",
    "dxy_em":
        "Como nos outros canais, o que entra na conta é a **variação** e não o nível. Um dólar forte e estável contra os emergentes não move o real por aqui; o que move é ele ficar mais forte.",
    "sp500":
        "O que entra é a **variação** do índice, em log-retorno — o patamar do S&P não diz nada à equação, só o quanto ele subiu ou caiu no trimestre. E lembre que o sinal positivo é condicional ao CDS e ao dólar emergente estarem na conta.",
    "icbr_usd":
        "Também entra pela **variação**, em log-retorno: commodity cara e parada não valoriza o real, commodity subindo valoriza.",
}

# Domestica ou externa, pelo criterio de `REGIOES`: de quem e a variavel, e nao onde
# ela e negociada. O CDS soberano e risco de credito do Brasil; o IC-Br em dolar e
# preco de commodity formado fora, ainda que a cesta seja a da pauta brasileira -- o
# que o Brasil traz para ele e o peso de cada produto, nao o preco.
_FX_CANAIS_REGIAO = {
    "fiscal": "domestica",
    "dxy_em": "externa",
    "sp500": "externa",
    "icbr_usd": "externa",
}

def _variaveis(df: pd.DataFrame, d: pd.DataFrame, am_idx,
               ins: dict, ins_i: dict) -> tuple[dict, list]:
    """As entradas do modelo, uma por cartao, com a classificacao de cada uma.

    ## Nao ha mais premissa com subpremissa

    Ate 2026-09-24 tres cartoes eram CONTAS de outros dois (`di = pi_e - meta`,
    `ancora = rr_10a + meta`, `ppp = infl_br - infl_us`), com as pecas escondidas atras
    de um "abrir em partes". O usuario cortou o mecanismo em 2026-09-25: *"não haverá
    mais premissas com subpremissas. Todas serão separadas em exógenas e endógenas."*

    O que era peca virou cartao, e a conta mudou de dono -- ela passou a ser declarada
    pela EQUACAO que a consome, no campo `deriva`. Isso nao e so arrumacao: um cartao de
    `di` deixava digitar um desvio que contradiz a expectativa da propria rodada, e com
    a (E) entrando no simulador a expectativa passou a ser produzida. A mesma regra que
    ja impedia o `carry_vol` de ter cartao ("ele e conta, nao premissa") agora vale para
    as tres.

    ## E as exogenas se dividem em DOMESTICA e EXTERNA

    Mesmo pedido. O criterio esta em `REGIOES`, e `regiao` so existe em quem e exogena.

    ## E `tipo` responde sobre ESTE SIMULADOR, nao sobre o modelo

    `tipo == "endogena"` quer dizer *uma equacao que roda aqui produz esta variavel* --
    ou seja, e sempre igual a `produtor_no_sim`, e o `_variaveis` levanta se os dois
    discordarem. O fato do MODELO continua declarado ao lado, em `produzida_por`, e e o
    selo do cartao que o imprime.

    A distincao foi obrigatoria ate 2026-09-28 por causa da `infl_br`: a curva de
    Phillips a produzia no modelo e ainda nao estava no simulador, entao ela era premissa
    que se digita. Desde entao as cinco equacoes do modelo rodam aqui e os dois campos
    coincidem em todo cartao -- a guarda fica, porque o caso volta no dia em que o modelo
    ganhar uma sexta equacao antes de ela entrar no simulador.
    """
    sub = df.reindex(am_idx)

    # As duas marcas de crise NAO tem cartao desde 2026-09-24 (*"pretendo usa-las mais
    # como ajuste do que variaveis exogenas"*). A serie delas viaja dentro da equacao
    # que as le.
    #
    # A ordem e a de leitura: primeiro as cinco endogenas, na ordem de solucao
    # (H -> I -> E -> R -> F), depois as exogenas domesticas e por fim as externas.
    ordem = ["hiato", "infl_br", "pi_e", "selic", "de",
             "meta_12m", "rr_10a", "fiscal", "vol",
             "infl_us", "ffr", "dxy_em", "sp500", "icbr_usd",
             "icbr_agr_usd", "icbr_met_usd"]
    v = {
        "pi_e": {
            "key": "pi_e", "nome_frase": "inflação esperada",
            "nome": "Inflação esperada (Focus, 12 meses)", "unidade": "% ao ano",
            "tipo": "endogena", "produzida_por": "E", "produtor_no_sim": True,
            # A propria (E) a le defasada; a (R) a le no desvio contra a meta; e a (I) a
            # le defasada, dividida por quatro, como a ancora da inflacao do trimestre.
            "consumida_por": ["E", "R", "I"],
            "obs": _ser(sub["pi_e"]),
            "fontes": ["equacao", "digitado", "observado"], "fonte_padrao": "equacao",
            "passo": 0.1,
            "instrucao": "Digite a inflação esperada para os doze meses à frente em "
                         "cada trimestre, em % ao ano.",
            "desc": "A mediana do Focus para o IPCA acumulado nos doze meses à "
                    "frente, suavizada. É o que a equação de expectativas produz, e é "
                    "de onde sai o desvio contra a meta que tira a Selic do repouso.",
            "nota": "Escolher Exógeno ou Observado **desliga a equação de "
                    "expectativas**. Ela não fica solta: **duas equações a leem**. A "
                    "regra de juros, pela distância entre ela e a meta; e a curva de "
                    "Phillips, no trimestre seguinte, como o ponto para onde a inflação "
                    "de cada grupo converge. Impor a expectativa move, portanto, a "
                    "Selic e a inflação que saem daqui — e, por elas, o hiato e o "
                    "câmbio. O caminho contrário também vale: a inflação que a curva de "
                    "Phillips produz move esta expectativa sem que ninguém toque neste "
                    "cartão.",
        },
        "selic": {
            "key": "selic", "nome_frase": "Selic", "nome": "Selic", "unidade": "% ao ano",
            "tipo": "endogena", "produzida_por": "R", "produtor_no_sim": True,
            # A propria (R) a le defasada, a (F) a le no carry, e a (H) a le defasada
            # na distancia ate a ancora.
            "consumida_por": ["R", "H", "F"],
            "obs": _ser(d["selic"].reindex(am_idx)),
            # A ordem e a das pills na tela: Endogeno, Exogeno, Observado.
            "fontes": ["equacao", "digitado", "observado"], "fonte_padrao": "equacao",
            "passo": 0.25,
            "instrucao": "Digite a Selic média que você espera em cada trimestre, "
                         "em % ao ano.",
            "desc": "A taxa básica média do trimestre. É o que a regra de juros produz.",
            "nota": "Escolher Exógeno ou Observado **desliga a regra de juros**: a "
                    "Selic passa a ser imposta em vez de calculada. Ela não fica "
                    "solta — **duas equações a leem**: a curva IS, pela distância até "
                    "o juro nominal de equilíbrio no trimestre anterior, e a do câmbio, "
                    "pelo carry sobre a volatilidade. Impor a Selic move o hiato e o "
                    "câmbio que saem daqui, e por eles a inflação. "
                    "Uma ressalva de medida: a regra de juros produz a Selic MÉDIA do "
                    "trimestre e o carry foi estimado com a do fechamento; as duas "
                    "diferem 0,38 p.p. em média, o que vale no máximo 0,16 p.p. de "
                    "câmbio por trimestre contra um erro típico de 3,6 p.p.",
        },
        "hiato": {
            "key": "hiato", "nome_frase": "hiato do produto",
            "nome": "Hiato do produto", "unidade": "% do potencial",
            "tipo": "endogena", "produzida_por": "H", "produtor_no_sim": True,
            # A propria (H) o le defasado; a curva de Phillips o le no trimestre.
            "consumida_por": ["H", "I"],
            "obs": _ser(sub["hiato"]),
            "fontes": ["equacao", "digitado", "observado"], "fonte_padrao": "equacao",
            "passo": 0.25,
            "instrucao": "Digite o hiato do produto em cada trimestre, em % do produto "
                         "potencial — positivo é a economia acima do que consegue "
                         "sustentar.",
            "desc": "Quanto a economia está produzindo acima (positivo) ou abaixo "
                    "(negativo) do que consegue sustentar sem acelerar a inflação, na "
                    "estimativa do Banco Central. É o que a curva IS produz.",
            "nota": "É por aqui que **a Selic deste simulador chega ao produto**: a "
                    "curva IS lê a distância entre a Selic e o juro nominal de "
                    "equilíbrio no trimestre anterior. E é por aqui que **o produto "
                    "chega aos preços**: a curva de Phillips lê o hiato no mesmo "
                    "trimestre, em serviços, em alimentação e em bens industriais. "
                    "Escolher Exógeno ou Observado **desliga a curva IS**, e a curva de "
                    "Phillips passa a ler o caminho que você impôs.",
        },
        "meta_12m": {
            "key": "meta_12m", "nome_frase": "meta de inflação",
            "nome": "Meta de inflação (12 meses)", "unidade": "% ao ano",
            "tipo": "exogena", "produzida_por": None, "produtor_no_sim": False,
            "regiao": "domestica",
            "consumida_por": ["E", "R", "H"],
            "obs": _ser(sub["meta_12m"]),
            "fontes": ["digitado", "observado"], "fonte_padrao": "observado",
            "passo": 0.25,
            "instrucao": "Digite a meta vigente no horizonte de doze meses em cada "
                         "trimestre, em % ao ano.",
            "desc": "A meta perseguida pelo Banco Central no horizonte de doze meses. "
                    "É decisão do CMN, e por isso exógena por natureza: nenhuma "
                    "equação do modelo a produz.",
            "nota": "**Três equações leem esta variável**, cada uma por um caminho. "
                    "Na equação de expectativas ela é o ponto para onde a expectativa "
                    "converge quando nada a empurra — mexer nela reancora o modelo "
                    "inteiro. Na regra de juros ela entra duas vezes: no desvio da "
                    "inflação esperada e no juro nominal de equilíbrio. E na curva IS "
                    "ela está dentro do juro de equilíbrio contra o qual o aperto é "
                    "medido. Subir a meta em 1 p.p. sobe a âncora em 1 p.p. e, ao mesmo "
                    "tempo, reduz o desvio — os dois efeitos têm sinais contrários e o "
                    "líquido está no gráfico da regra de juros.",
        },
        "rr_10a": {
            "key": "rr_10a", "nome_frase": "juro real de 10 anos",
            "nome": "Juro real de 10 anos (NTN-B)", "unidade": "% ao ano",
            "tipo": "exogena", "produzida_por": None, "produtor_no_sim": False,
            "regiao": "domestica",
            "consumida_por": ["R", "H"],
            "obs": _ser(sub["rr_10a"]),
            "fontes": ["digitado", "observado"], "fonte_padrao": "observado",
            "passo": 0.25,
            "instrucao": "Digite o juro real de dez anos em cada trimestre, "
                         "em % ao ano.",
            "desc": "O juro real de dez anos negociado no mercado. É o que faz as "
                    "vezes de juro de equilíbrio nesta conta — preço observado todo "
                    "dia, e não estimativa.",
            "nota": "Somado à meta, ele forma **o juro nominal de equilíbrio**: onde "
                    "a Selic pararia se a inflação esperada estivesse na meta. **Duas "
                    "equações o usam, e para a mesma coisa**: a regra de juros persegue "
                    "esse ponto, e a curva IS mede o aperto como a distância da Selic "
                    "até ele. Subir este cartão, portanto, sobe a Selic que a regra "
                    "produz e, ao mesmo tempo, reduz o aperto que a curva IS lê. A soma "
                    "não é cartão — é conta das duas equações. Nenhuma equação deste "
                    "modelo produz o juro real de equilíbrio; estimá-lo em vez de ler um "
                    "preço é pendência declarada (R12/H9).",
        },
        "infl_br": {
            "key": "infl_br", "nome_frase": "inflação do Brasil no trimestre",
            "nome": "Inflação do Brasil no trimestre", "unidade": "% no trimestre",
            "tipo": "endogena", "produzida_por": "I", "produtor_no_sim": True,
            # A (E) a compoe em doze meses, a (F) a compara com a americana, e a propria
            # (I) a le defasada: os monitorados se indexam ao IPCA cheio do trimestre
            # anterior.
            "consumida_por": ["I", "E", "F"],
            "obs": _ser(ins["infl_br"].reindex(am_idx)),
            "fontes": ["equacao", "digitado", "observado"], "fonte_padrao": "equacao",
            "passo": 0.1,
            "segura": dict(_SEGURA_MEDIA),
            "instrucao": "Digite a variação do IPCA dentro de cada trimestre, em "
                         "por cento — não acumulada em doze meses e não anualizada.",
            "desc": "A variação do IPCA dentro do trimestre. É o que a curva de "
                    "Phillips produz, somando os quatro grupos — serviços, alimentação, "
                    "bens industriais e monitorados — com o peso de cada um no índice. "
                    "Duas outras equações a leem, por contas diferentes: a de "
                    "expectativas compõe quatro trimestres dela no IPCA de doze meses, e "
                    "a do câmbio a compara com a inflação americana.",
            "nota": "**Este é o cartão que fecha o laço do modelo.** A inflação que "
                    "sai daqui move a expectativa, a expectativa move a Selic, a Selic "
                    "move o hiato e o câmbio — e os dois voltam para cá. Por fora disso "
                    "ela ainda move o câmbio direto, pelo diferencial de inflação, com "
                    "peso imposto em 1. Escolher Exógeno ou Observado **desliga a curva "
                    "de Phillips** e abre o laço: a expectativa e o câmbio passam a ler "
                    "o caminho que você impôs.\n\n"
                    "**Em Observado, passado o último dado este cartão segura a MÉDIA "
                    "dos últimos %d trimestres, e não a última leitura.** Ele e a "
                    "inflação americana são os dois únicos do painel que fazem isso, e "
                    "a razão é que são os dois que medem um *fluxo*: um trimestre de "
                    "inflação tem desvio-padrão da ordem da própria média, e segurar "
                    "uma leitura isolada projetaria ruído por três anos. Nos cartões "
                    "de nível a regra continua sendo repetir o último valor, que ali é "
                    "a leitura certa." % SEGURA_MEDIA_K,
        },
        "infl_us": {
            "key": "infl_us", "nome_frase": "inflação dos Estados Unidos no trimestre",
            "nome": "Inflação dos Estados Unidos no trimestre",
            "unidade": "% no trimestre",
            "tipo": "exogena", "produzida_por": None, "produtor_no_sim": False,
            "regiao": "externa",
            "consumida_por": ["F"],
            "obs": _ser(ins["infl_us"].reindex(am_idx)),
            "fontes": ["digitado", "observado"], "fonte_padrao": "observado",
            "passo": 0.1,
            "segura": dict(_SEGURA_MEDIA),
            "instrucao": "Digite a variação do CPI americano dentro de cada "
                         "trimestre, em por cento.",
            "desc": "A variação do CPI americano dentro do trimestre. Subtraída da "
                    "brasileira, forma o diferencial de inflação que a equação do "
                    "câmbio lê com peso imposto em 1.",
            "nota": "Quando a inflação de lá sobe tanto quanto a daqui, **o "
                    "diferencial some e o câmbio não tem por que se mexer por este "
                    "canal** — é o lado da conta que costuma ser esquecido quando se "
                    "pensa em inflação brasileira e câmbio. Ela também segura a média "
                    "dos últimos %d trimestres passado o último dado, pela mesma razão "
                    "da inflação brasileira." % SEGURA_MEDIA_K,
        },
        "de": {
            "key": "de", "nome_frase": "câmbio", "nome": "Câmbio",
            # "Hoje em 5,18 reais por dolar", e nao "5,18 R$ por US$": a unidade e
            # impressa DEPOIS do numero, entao ela tem de se ler como substantivo e
            # nao como simbolo de moeda.
            "unidade": "reais por dólar",
            # A CAIXA MOSTRA O NIVEL, e a equacao trabalha na variacao. Pedido do
            # usuario em 2026-09-24: *"conseguimos trabalhar com ela no simulador (nos
            # boxes) em nivel?"* -- e sim, porque a conversao e exata nos dois sentidos
            # (`de = 100*ln(P_t / P_{t-1})`, ancorada no ultimo fechamento observado) e
            # porque o grafico ja desenhava o nivel: ate aqui o cartao e o grafico
            # falavam unidades diferentes da mesma coisa.
            #
            # `unidade_eq` continua declarando em que unidade a EQUACAO trabalha, para
            # a tela poder dizer as duas sem que uma tenha de sumir.
            "unidade_eq": "% no trimestre",
            "em_nivel_de_variacao": True,
            "tipo": "endogena", "produzida_por": "F", "produtor_no_sim": True,
            # A propria (F) a le defasada; a curva de Phillips a le pelo cambio MEDIO do
            # trimestre -- alimentacao no mesmo, bens industriais no seguinte.
            "consumida_por": ["F", "I"],
            "obs": _ser(ins["ptax"].reindex(am_idx)),
            "fontes": ["equacao", "digitado", "observado"], "fonte_padrao": "equacao",
            "passo": 0.05,
            "instrucao": "Digite o câmbio de fechamento de cada trimestre, em reais "
                         "por dólar.",
            "desc": "O dólar em reais, no fechamento do trimestre. A equação trabalha "
                    "na variação de um trimestre para o outro, e não no nível — a "
                    "caixa mostra o nível porque é nele que um cenário se pensa, e a "
                    "variação implícita de cada trimestre aparece ao passar o mouse "
                    "sobre a caixa, e no hover do gráfico. As duas são o mesmo "
                    "caminho.",
            "nota": "Escolher Exógeno ou Observado **desliga a equação do câmbio**, e "
                    "a curva de Phillips passa a ler o caminho que você impôs: é por "
                    "aqui que **o câmbio chega aos preços**, em alimentação no mesmo "
                    "trimestre e em bens industriais no seguinte. Ela lê o câmbio MÉDIO "
                    "do trimestre, e não o de fechamento que esta caixa mostra — o "
                    "médio sai de dois fechamentos seguidos, pela metade do caminho "
                    "entre eles. Uma consequência de digitar em nível: um choque que "
                    "**sobe e depois volta** devolve o câmbio ao ponto de partida, "
                    "enquanto o mesmo choque na variação deslocaria o nível para "
                    "sempre. São dois cenários diferentes, e aqui você pede o primeiro.",
        },
        "ffr": {
            "key": "ffr", "nome_frase": "juro dos Fed Funds", "nome": "Juro dos Fed Funds", "unidade": "% ao ano",
            "tipo": "exogena", "produzida_por": None, "produtor_no_sim": False,
            "regiao": "externa",
            "consumida_por": ["F"],
            "obs": _ser(ins["ffr"].reindex(am_idx)),
            "fontes": ["digitado", "observado"], "fonte_padrao": "observado",
            "passo": 0.25,
            "instrucao": "Digite o juro básico americano que você espera em cada "
                         "trimestre, em % ao ano.",
            "desc": "O juro básico dos Estados Unidos. Ele não entra sozinho: entra "
                    "subtraído da Selic, formando o carry — o que se ganha por "
                    "carregar real em vez de dólar.",
            "nota": "É por aqui que **a Selic deste simulador chega ao câmbio**: o "
                    "canal é `(Selic − Fed Funds) ÷ volatilidade`. Mexer na Selic "
                    "move o câmbio sem que ninguém precise mexer neste cartão — e "
                    "mexer aqui move o câmbio sem mexer na Selic.",
        },
        "vol": {
            "key": "vol", "nome_frase": "volatilidade implícita do dólar",
            "nome": "Volatilidade implícita do dólar", "unidade": "% ao ano",
            "tipo": "exogena", "produzida_por": None, "produtor_no_sim": False,
            "regiao": "domestica",
            "consumida_por": ["F"],
            "obs": _ser(ins["vol"].reindex(am_idx)),
            "fontes": ["digitado", "observado"], "fonte_padrao": "observado",
            "passo": 0.5,
            "instrucao": "Digite a volatilidade implícita de 3 meses das opções de "
                         "dólar em cada trimestre, em % ao ano.",
            "desc": "O quanto o mercado de opções está cobrando para proteger contra "
                    "oscilação do dólar nos três meses seguintes, anualizado. Ela é o "
                    "denominador do carry: o mesmo juro atrai menos quando o mercado "
                    "espera que a moeda balance mais.",
            "nota": "O ganho de carregar real é o juro a mais **menos** a "
                    "desvalorização, e o risco desse negócio é a oscilação que se "
                    "espera daqui para a frente — por isso o denominador é um preço "
                    "de opção e não uma medida do que já aconteceu. Ela entra pelo "
                    "fechamento do trimestre, como o risco fiscal e os outros preços "
                    "desta equação.",
        },
    }

    for k, (nome, unid, fonte, frase, desc) in _FX_CANAIS_CARTAO.items():
        v[k] = {
            "key": k, "nome": nome, "nome_frase": frase, "unidade": unid,
            "tipo": "exogena", "produzida_por": None, "produtor_no_sim": False,
            "regiao": _FX_CANAIS_REGIAO[k],
            "consumida_por": ["F"],
            "obs": _ser(ins["niveis"][k].reindex(am_idx)),
            "fontes": ["digitado", "observado"], "fonte_padrao": "observado",
            "passo": 10.0 if k in ("fiscal", "sp500") else 1.0,
            "instrucao": "Digite o NÍVEL de %s em cada trimestre, em %s — a equação "
                         "usa a variação de um trimestre para o outro."
                         % (nome.split(" (")[0].lower(), unid),
            "desc": desc,
            "nota": _FX_CANAIS_NOTA[k],
        }

    # As duas cestas de commodity da (I). Externas pelo mesmo criterio do IC-Br geral: o
    # preco e formado fora, ainda que a cesta seja a da pauta daqui.
    for k, (nome, frase, grupo, desc, nota) in {
        "icbr_agr_usd": (
            "Commodities agrícolas em dólar (IC-Br agropecuária)",
            "commodities agrícolas em dólar (IC-Br agropecuária)", "alimentação",
            "O preço em dólar da parte agropecuária da cesta de commodities que o "
            "Brasil produz, na média do trimestre. É o custo de matéria-prima da "
            "comida, antes do câmbio.",
            "A curva de Phillips lê a **variação** deste índice, no mesmo trimestre, "
            "na inflação de alimentação. Um índice parado em patamar alto não pressiona "
            "nada; o que pressiona é ele subir."),
        "icbr_met_usd": (
            "Metais em dólar (IC-Br metal)", "metais em dólar (IC-Br metal)",
            "bens industriais",
            "O preço em dólar da parte metálica da mesma cesta, na média do trimestre. "
            "É insumo da indústria — aço, alumínio, cobre.",
            "A curva de Phillips lê a **variação** deste índice na inflação de bens "
            "industriais, no mesmo trimestre e no seguinte: o metal leva algum tempo "
            "para chegar à prateleira."),
    }.items():
        v[k] = {
            "key": k, "nome": nome, "nome_frase": frase, "unidade": "pontos do índice",
            "tipo": "exogena", "produzida_por": None, "produtor_no_sim": False,
            "regiao": "externa",
            "consumida_por": ["I"],
            "obs": _ser(ins_i[k].reindex(am_idx)),
            "fontes": ["digitado", "observado"], "fonte_padrao": "observado",
            "passo": 2.0,
            "instrucao": "Digite o NÍVEL do índice em cada trimestre, em pontos — a "
                         "equação usa a variação de um trimestre para o outro, na "
                         "inflação de %s." % grupo,
            "desc": desc,
            "nota": nota,
        }

    # Guardas de contrato. As duas sao baratas e as duas pegam um erro que a tela nao
    # denunciaria: um cartao fora da ordem simplesmente nao aparece, e uma exogena sem
    # regiao cairia num grupo qualquer.
    if sorted(ordem) != sorted(v):
        raise ValueError("a ordem dos cartoes nao cobre exatamente os cartoes: %s"
                         % sorted(set(ordem) ^ set(v)))
    for k, vv in v.items():
        endo = vv["tipo"] == "endogena"
        if endo != bool(vv["produtor_no_sim"]):
            raise ValueError(
                "%r diz tipo=%r e produtor_no_sim=%r: `tipo` e sobre ESTE simulador, "
                "entao os dois nao podem discordar" % (k, vv["tipo"],
                                                       vv["produtor_no_sim"]))
        if endo and "regiao" in vv:
            raise ValueError("%r e endogena e declara regiao" % k)
        if not endo and vv.get("regiao") not in REGIOES:
            raise ValueError("%r e exogena e nao declara regiao valida" % k)
    return v, ordem


def _ajuste_taylor(d: pd.DataFrame, am_idx, des: dict, dummies: list) -> list:
    """O ajuste de UM PASSO da (R) na grade, com os pesos da mediana do posterior.

    Existe pela mesma razao que o da (F): a recursao esta escrita duas vezes, aqui e
    no navegador, e duas implementacoes divergem em silencio. Ganhou peso em
    2026-09-25, quando `di` e `ancora` deixaram de ser caminhos prontos no payload e
    passaram a ser CONTAS que as duas pontas refazem -- e uma conta refeita em dois
    lugares e exatamente o que este gabarito existe para prender.
    """
    md = des["mediana"]
    peso = 1.0 - md["t1"] - md["t2"]
    y = d["y"].reindex(am_idx)
    di = d["r2"].reindex(am_idx)
    anc = d["ancora"].reindex(am_idx)
    dum = {c: d[c].reindex(am_idx) for c in dummies}
    out = []
    for i in range(len(am_idx)):
        if i < 2 or pd.isna(y.iloc[i - 1]) or pd.isna(y.iloc[i - 2]) \
                or pd.isna(di.iloc[i]) or pd.isna(anc.iloc[i]):
            out.append(None)
            continue
        val = (md["t1"] * float(y.iloc[i - 1]) + md["t2"] * float(y.iloc[i - 2])
               + peso * md["t3"] * float(di.iloc[i]))
        for c in dummies:
            dv = float(dum[c].iloc[i])
            if dv:
                val += md.get(c, 0.0) * dv
        out.append(round(val + float(anc.iloc[i]), 6))
    return out


def _eq_juros(d: pd.DataFrame, am_idx, des: dict, est_idx) -> dict:
    """A equacao (R) como um item do bloco de equacoes."""
    dummies = [c for c in taylor.CRISES if c in des["pars"]]
    return {
        "key": "R",
        "nome": "Regra de juros",
        "explica": "selic",
        "unidade": "% ao ano",
        # O que o leitor ESCOLHE -- cartoes do bloco 2, e nao os termos da equacao. As
        # marcas de crise nao entram aqui: elas fazem parte da equacao ajustada e nao
        # sao input de ninguem.
        "consome": ["pi_e", "meta_12m", "rr_10a"],
        # As duas CONTAS que a equacao faz com o que consome. Ate 2026-09-24 elas eram
        # cartoes proprios, com as pecas escondidas atras de "abrir em partes"; o
        # usuario cortou o mecanismo e a conta mudou de dono. Declarada em dados, e nao
        # em codigo, para a mesma conta valer no Python e no navegador.
        "deriva": {
            # `nome` rotula e `nome_frase` e o mesmo nome como ele se LE dentro de
            # uma frase. Sao dois campos e nao um com `.toLowerCase()`, que come a
            # sigla -- e a quarta vez que este defeito aparece nesta pagina.
            "di": {"op": "-", "de": ["pi_e", "meta_12m"],
                   "nome": "Desvio da inflação esperada",
                   "nome_frase": "o desvio da inflação esperada contra a meta",
                   "unidade": "p.p."},
            "ancora": {"op": "+", "de": ["rr_10a", "meta_12m"],
                       "nome": "Juro nominal de equilíbrio",
                       "nome_frase": "o juro nominal de equilíbrio",
                       "unidade": "% ao ano"},
        },
        "multiplica": "di",
        "soma": "ancora",
        "lags": ["t1", "t2"],
        "mult": "t3",
        "dummies": dummies,
        # A serie de cada marca, que o simulador le direto: 1 dentro da janela dela e
        # 0 no resto -- e 0 em todo trimestre projetado, que e o ponto.
        "dummy_obs": {c: _ser(d[c].reindex(am_idx)) for c in dummies},
        "y": _ser(d["y"].reindex(am_idx)),
        "selic_obs": _ser(d["selic"].reindex(am_idx)),
        "ajuste": _ajuste_taylor(d, am_idx, des, dummies),
        "est_ini": "%dT%d" % (est_idx[0].year, est_idx[0].quarter),
        "est_fim": "%dT%d" % (est_idx[-1].year, est_idx[-1].quarter),
        "est_i0": int(am_idx.get_loc(est_idx[0])),
        "est_i1": int(am_idx.get_loc(est_idx[-1])),
        "caixa": des.get("caixa", {}),
        "mediana": des["mediana"],
        "hdi": des["hdi"],
        "hdi_prob": des["hdi_prob"],
        "pars": des["pars"],
        "draws": des["draws"],
        "n_draws": des["n_gravado"],
        "n_draws_total": des["n_total"],
        "priori": des["priori"],
        "amostra": des["gerado_de"],
    }



# Quantos trimestres de inflacao trimestral compoem o acumulado em doze meses.
ACUM_I12 = 4


def _pos_na_grade(am_idx, per: pd.Period, padrao: int) -> int:
    """A posicao de um trimestre na grade, ou `padrao` se ele cair fora dela."""
    return int(am_idx.get_loc(per)) if per in am_idx else int(padrao)


def _i12_de_trimestres(infl: list, i: int, k: int = ACUM_I12) -> float | None:
    """O IPCA acumulado em 12 meses composto de `k` variacoes trimestrais em log.

    `100*(exp(soma/100) - 1)`, que e a composicao exata e nao a soma das variacoes.

    **Isto NAO e uma aproximacao do `ipca_12m` publicado: e o mesmo numero.** Medido
    contra a serie do SGS 13522 em 99 trimestres, o erro medio e 0,0024 p.p. e o maximo
    0,0056 -- meio centesimo, que e o arredondamento da propria serie publicada (duas
    casas). E por isso que o painel tem UM cartao de IPCA e nao dois: manter um cartao
    em % no trimestre e outro em doze meses seria deixar duas premissas digitaveis da
    mesma serie, livres para se contradizer sem que nada na tela avisasse.
    """
    if i - k + 1 < 0:
        return None
    soma = 0.0
    for j in range(i - k + 1, i + 1):
        v = infl[j] if j < len(infl) else None
        if v is None:
            return None
        soma += float(v)
    return 100.0 * (float(np.exp(soma / 100.0)) - 1.0)


def _pre_grade(s: pd.Series, am_idx, n: int) -> list:
    """Os `n` valores de `s` nos trimestres IMEDIATAMENTE ANTES da grade.

    A grade do simulador comeca onde a (R) consegue ser calculada -- ela depende do
    juro real de dez anos, que e a serie mais curta. A inflacao trimestral existe muito
    antes disso, e o acumulado de doze meses do PRIMEIRO trimestre da grade precisa dos
    tres anteriores. Sem eles a composicao devolveria nulo bem no comeco, e uma corrida
    solta partindo dali (que e o que o `main()` e o teste fazem) nao teria expectativa.

    Mesmo instinto do trimestre a mais da volatilidade, no sentido contrario do tempo.
    """
    ini = am_idx[0]
    idx = pd.PeriodIndex([ini - (n - j) for j in range(n)], freq=am_idx.freq)
    return _ser(s.reindex(idx))


def _ajuste_exp(sub: pd.DataFrame, pre: list, infl: list, am_idx, des: dict) -> list:
    """O ajuste de um passo da (E) na grade, com os pesos da mediana do posterior.

    Um passo quer dizer que a defasagem da expectativa vem do OBSERVADO, e por isso ele
    e o gabarito exato: o navegador rodando `h = 1` a partir de cada trimestre tem de
    devolver estes mesmos numeros. O `i12` e composto aqui pelo MESMO caminho que a
    recursao usa -- se fosse lido de `ipca_12m` o gabarito deixaria de prender a
    composicao, que e justamente a parte nova.
    """
    md = des["mediana"]
    peso = 1.0 - md["e1"] - md["e2"]
    pie = sub["pi_e"]
    meta = sub["meta_12m"]
    serie = list(pre) + list(infl)
    base = len(pre)
    out = []
    for i in range(len(am_idx)):
        i12 = _i12_de_trimestres(serie, base + i)
        if i == 0 or i12 is None or pd.isna(pie.iloc[i - 1]) or pd.isna(meta.iloc[i]):
            out.append(None)
            continue
        val = (md["e1"] * float(pie.iloc[i - 1]) + md["e2"] * i12
               + peso * float(meta.iloc[i]))
        out.append(round(val, 6))
    return out


def _eq_expectativas(sub: pd.DataFrame, infl_s: pd.Series, am_idx, des: dict) -> dict:
    """A equacao (E) como um item do bloco de equacoes.

    Ela produz a expectativa que a (R) le no desvio contra a meta e que a (I) le como a
    ancora de cada grupo no trimestre seguinte. E ela le a inflacao do trimestre, que
    desde 2026-09-28 vem da curva de Phillips -- e e por aqui que o laco fecha.
    """
    g = des["gerado_de"]
    ini, fim = pd.Period(g["ini"], "Q"), pd.Period(g["fim"], "Q")
    infl = _ser(infl_s.reindex(am_idx))
    pre = _pre_grade(infl_s, am_idx, ACUM_I12 - 1)
    serie = list(pre) + list(infl)
    i12 = [_i12_de_trimestres(serie, len(pre) + i) for i in range(len(am_idx))]
    return {
        "key": "E",
        "nome": "Expectativas",
        "explica": "pi_e",
        "unidade": "% ao ano",
        "consome": ["infl_br", "meta_12m"],
        # O IPCA em doze meses NAO e cartao: ele e conta, composto de quatro trimestres
        # do cartao de inflacao. Dar cartao a ele poria duas premissas digitaveis da
        # mesma serie, livres para se contradizer -- a mesma regra que ja impedia o
        # `carry_vol` da (F) de ter um.
        "deriva": {
            "i12": {"op": "acum_log", "de": ["infl_br"], "k": ACUM_I12,
                    "nome": "IPCA acumulado em 12 meses",
                    "nome_frase": "o IPCA acumulado em 12 meses",
                    "unidade": "% ao ano"},
        },
        "meta": "meta_12m",
        "lags": ["pi_e_l1"],
        # A serie observada da inflacao trimestral, de onde saem as defasagens que o
        # primeiro trimestre projetado precisa para fechar os quatro do acumulado, mais
        # os tres trimestres ANTERIORES a grade (ver `_pre_grade`).
        "obs_insumo": {"infl_br": list(infl)},
        "pre_insumo": {"infl_br": list(pre)},
        "i12_obs": [None if x is None else round(float(x), 6) for x in i12],
        # O IPCA de 12 meses PUBLICADO (SGS 13522), na mesma grade. Ele nao e desenhado
        # e nao entra em conta nenhuma: existe para o teste poder exigir que a
        # composicao de quatro trimestres devolva a serie da fonte. E o gabarito que
        # justifica o painel ter UM cartao de IPCA e nao dois -- sem ele, "as duas
        # formas sao a mesma serie" seria afirmacao em vez de medicao.
        "i12_pub": _ser(sub["ipca_12m"]),
        "y": _ser(sub["pi_e"]),
        "meta_obs": _ser(sub["meta_12m"]),
        "ajuste": _ajuste_exp(sub, pre, infl, am_idx, des),
        "est_ini": "%dT%d" % (ini.year, ini.quarter),
        "est_fim": "%dT%d" % (fim.year, fim.quarter),
        # A (E) e a unica das quatro estimada ANTES do comeco da grade do simulador: ela
        # so precisa da Focus, do IPCA e da meta, enquanto a grade e definida pela
        # (R), que precisa do juro real de dez anos. Por isso a posicao e recortada e
        # o payload diz que ela foi -- um `est_i0` negativo pintaria a faixa da amostra
        # no lugar errado, e um `get_loc` cru estouraria.
        "est_i0": _pos_na_grade(am_idx, ini, 0),
        "est_i1": _pos_na_grade(am_idx, fim, len(am_idx) - 1),
        "est_antes_da_grade": bool(ini < am_idx[0]),
        "mediana": des["mediana"],
        "hdi": des["hdi"],
        "hdi_prob": des["hdi_prob"],
        "pars": des["pars"],
        "draws": des["draws"],
        "n_draws": des["n_gravado"],
        "n_draws_total": des["n_total"],
        "priori": des["variante"],
        "meia_vida": des["meia_vida"],
        "amostra": g,
    }


def _ajuste_is(dis: pd.DataFrame, sub: pd.DataFrame, am_idx, des: dict,
               dummies: list) -> list:
    """O ajuste de um passo da (H) na grade, com os pesos da mediana do posterior.

    O aperto sai aqui da coluna `gap_juro` do PAINEL, e o navegador o refaz dos tres
    cartoes (`Selic - juro real de 10 anos - meta`). Um passo das duas pontas bater e,
    portanto, a prova de duas coisas ao mesmo tempo: que a recursao e a mesma, e que a
    conta declarada em `deriva` reproduz a identidade do painel.
    """
    md = des["mediana"]
    lag = is_curve.LAG_GRR
    hi = sub["hiato"]
    gap = sub[is_curve.COL_APERTO]
    dum = {c: dis[c].reindex(am_idx) for c in dummies}
    out = []
    for i in range(len(am_idx)):
        if i < lag or pd.isna(hi.iloc[i - 1]) or pd.isna(gap.iloc[i - lag]):
            out.append(None)
            continue
        val = md["h1"] * float(hi.iloc[i - 1]) + md["h2"] * float(gap.iloc[i - lag])
        for c in dummies:
            dv = dum[c].iloc[i]
            if not pd.isna(dv) and float(dv):
                val += md.get(c, 0.0) * float(dv)
        out.append(round(val, 6))
    return out


def _eq_hiato(df: pd.DataFrame, am_idx, des: dict) -> dict:
    """A equacao (H) como um item do bloco de equacoes.

    Ela le a Selic que a (R) produz com um trimestre de defasagem, entao, dentro do
    trimestre, ela e a primeira a ser conhecida. O hiato que ela produz vai para a curva
    de Phillips no mesmo trimestre: a (H) e o caminho do juro ate o produto, e a (I) o do
    produto ate os precos.
    """
    dis = is_curve.montar(df)
    sub = df.reindex(am_idx)
    dummies = [c for c in is_curve.CRISES if c in des["pars"]]
    g = des["gerado_de"]
    ini, fim = pd.Period(g["ini"], "Q"), pd.Period(g["fim"], "Q")
    return {
        "key": "H",
        "nome": "Curva IS",
        "explica": "hiato",
        "unidade": "% do potencial",
        "consome": ["selic", "rr_10a", "meta_12m"],
        # O aperto NAO e cartao: ele e conta dos tres, a mesma ancora que a (R)
        # persegue. `lin` e uma combinacao linear com os pesos declarados, porque a
        # conta tem tres pecas e os `-`/`+` das outras equacoes tem duas.
        "deriva": {
            "gap": {"op": "lin", "de": ["selic", "rr_10a", "meta_12m"],
                    "coef": [1.0, -1.0, -1.0],
                    "nome": "Aperto monetário",
                    "nome_frase": "o aperto monetário",
                    "unidade": "p.p."},
        },
        # Quantos trimestres o aperto demora a chegar ao produto. As `lag` defasagens
        # anteriores a janela vem do OBSERVADO; dali em diante, do caminho da rodada.
        "lag": int(is_curve.LAG_GRR),
        "lags": ["h1"],
        "dummies": dummies,
        "dummy_obs": {c: _ser(dis[c].reindex(am_idx)) for c in dummies},
        "y": _ser(sub["hiato"]),
        # O aperto do PAINEL na mesma grade. Nao entra em conta nenhuma: existe para o
        # teste exigir que a conta de `deriva`, feita dos cartoes, devolva a coluna que
        # a estimacao usou -- mesmo papel do `i12_pub` da (E).
        "gap_pub": _ser(sub[is_curve.COL_APERTO]),
        "ajuste": _ajuste_is(dis, sub, am_idx, des, dummies),
        "est_ini": "%dT%d" % (ini.year, ini.quarter),
        "est_fim": "%dT%d" % (fim.year, fim.quarter),
        "est_i0": _pos_na_grade(am_idx, ini, 0),
        "est_i1": _pos_na_grade(am_idx, fim, len(am_idx) - 1),
        "mediana": des["mediana"],
        "hdi": des["hdi"],
        "hdi_prob": des["hdi_prob"],
        "pars": des["pars"],
        "draws": des["draws"],
        "n_draws": des["n_gravado"],
        "n_draws_total": des["n_total"],
        "priori": des["variante"],
        "meia_vida": des["meia_vida"],
        # Dois numeros do posterior que a ficha imprime: quanto da massa diz que o
        # aperto ESFRIA o produto, e quanto e explosiva. Os dois sao medicao.
        "h2_negativo": des["h2_negativo"],
        "fora_estavel": des["fora_estavel"],
        "amostra": g,
    }


# De cada regressor da estimacao da (I) para o que a recursao do simulador tem na mao. A
# chave e a COLUNA de `phillips_sub.EQUACOES`; o valor, o nome da fonte que a recursao
# le. Uma coluna nova numa das quatro equacoes cai no `KeyError` do construtor, em vez de
# virar zero na conta -- que e o jeito silencioso de uma equacao perder um termo.
_I_FONTE = {
    "hiato": "hiato",              # o hiato do mesmo trimestre
    "de": "de_med",                # o cambio MEDIO do trimestre -- ver `deriva.de_med`
    "de_l1": "de_med_l1",
    "pi_agr_usd": "agr",
    "pi_met_usd": "met",
    "pi_met_usd_l1": "met_l1",
    "mm4_is": "mm4",               # a media dos quatro trimestres anteriores do grupo
    "mm4_ii": "mm4",
    "pi_q_l1": "cheio_l1",         # o IPCA cheio do trimestre anterior
}


_I_NOME_FRASE = {"IS": "serviços", "IA": "alimentação", "II": "bens industriais",
                 "IM": "monitorados"}


def _saz(q: int, j: int) -> float:
    """A coluna soma-zero `1{Q=j} - 1{Q=4}` da estimacao, para o trimestre `q`."""
    return (1.0 if q == j else 0.0) - (1.0 if q == 4 else 0.0)


def _ajuste_infl(df: pd.DataFrame, ins: dict, am_idx, grupos: dict, md: dict,
                 pesos: dict) -> dict:
    """O ajuste de um passo da (I) na grade, grupo a grupo e no cheio.

    Feito das COLUNAS do painel que a estimacao usou (`phillips_sub.montar`), e nao da
    recursao deste modulo: a recursao do navegador refaz cada uma delas dos cartoes --
    a media movel das inflacoes observadas, a variacao das commodities do nivel, o cheio
    defasado do log --, e um passo das duas pontas bater prova as duas coisas ao mesmo
    tempo, como o aperto da (H).

    **A unica coluna que NAO vem do painel e o cambio.** A estimacao le a variacao do
    cambio MEDIO do trimestre; o simulador so tem o de fechamento, que e o que a (F)
    produz. O que entra aqui e a mesma ponte que a recursao usa, a media de duas
    variacoes de fechamento seguidas -- ver `deriva.de_med` em `_eq_inflacao`.
    """
    d = ph.montar(df).reindex(am_idx)
    dfim = ins["de"].reindex(am_idx)
    de_med = 0.5 * (dfim + dfim.shift(1))
    fonte = {"hiato": d["hiato"], "de_med": de_med, "de_med_l1": de_med.shift(1),
             "agr": d["pi_agr_usd"], "met": d["pi_met_usd"],
             "met_l1": d["pi_met_usd_l1"], "cheio_l1": d["pi_q_l1"]}
    qq = am_idx.quarter
    out = {k: [] for k in list(grupos) + ["cheio"]}
    for i in range(len(am_idx)):
        tot, falta = 0.0, i < ACUM_I12
        vals = {}
        for k, g in grupos.items():
            dep = ph.EQUACOES[k]["dep"]
            c = lambda n: md[k + "." + n]  # noqa: E731
            e4 = d["E4_l1"].iloc[i]
            x = [d[dep + "_l1"].iloc[i], e4]
            val = c(g["inercia"]) * float(d[dep + "_l1"].iloc[i])
            peso = 1.0 - c(g["inercia"])
            for par, tipo in g["restritos"]:
                col = {"mm4": "mm4_" + k.lower(), "cheio_l1": "pi_q_l1"}[tipo]
                xv = d[col].iloc[i]
                x.append(xv)
                val += c(par) * float(xv) if not pd.isna(xv) else 0.0
                peso -= c(par)
            val += peso * float(e4) if not pd.isna(e4) else 0.0
            for par, tipo in g["regs"]:
                xv = fonte[tipo].iloc[i]
                x.append(xv)
                val += c(par) * float(xv) if not pd.isna(xv) else 0.0
            for j, s in enumerate(g["saz"], start=1):
                val += c(s) * _saz(int(qq[i]), j)
            if any(pd.isna(v) for v in x):
                falta = True
            vals[k] = val
            tot += float(pesos[k][i]) * val if pesos[k][i] is not None else float("nan")
        for k in grupos:
            out[k].append(None if falta else round(vals[k], 6))
        out["cheio"].append(None if (falta or not np.isfinite(tot))
                            else round(100.0 * float(np.log1p(tot / 100.0)), 6))
    return out


def _eq_inflacao(df: pd.DataFrame, ins: dict, am_idx, des: dict) -> dict:
    """A equacao (I), a curva de Phillips desagregada, como um item do bloco de equacoes.

    Ela e a que FECHA O LACO: le o hiato que a (H) produz, a expectativa que a (E)
    produz e o cambio que a (F) produz, e a inflacao que sai dela volta para a (E) e
    para a (F). Com ela o modelo deixa de ser uma corrente -- ver `resolver()`.

    Quatro equacoes por dentro, uma por grupo do IPCA, e UM cartao por fora: o IPCA
    cheio, que e a soma dos quatro com o peso de cada um no indice. Os pesos sao os
    publicados em cada trimestre da grade e, passado o ultimo dado, os do ultimo
    trimestre -- os pesos do IBGE andam com os precos relativos, e tres anos disso
    movem cada um em centesimos.
    """
    g_ = des["gerado_de"]
    ini, fim = pd.Period(g_["ini"], "Q"), pd.Period(g_["fim"], "Q")
    sub = df.reindex(am_idx)

    grupos = {}
    for k in ph.ORDEM:
        e = ph.EQUACOES[k]
        grupos[k] = {
            # o nome como ele se LE dentro de uma frase -- campo, e nao `.lower()`
            "nome": e["nome"], "nome_frase": _I_NOME_FRASE[k],
            "inercia": e["inercia"],
            "restritos": [[p, _I_FONTE[c]] for p, c, _r in e["restritos"]],
            "regs": [[p, _I_FONTE[c]] for p, c, _r in e["regs"]],
            "saz": list(ph.SAZ),
        }
        # Todo peso estimado tem lugar na recursao, e nenhum lugar fica sem peso. Um
        # termo sem par aqui somaria zero em silencio.
        esperado = ({e["inercia"]} | {p for p, _c, _r in e["restritos"]}
                    | {p for p, _c, _r in e["regs"]} | set(ph.SAZ))
        gravado = set(des["equacoes"][k]["pars"]) - {"sigma"}
        if esperado != gravado:
            raise ValueError("(I) %s: os pesos gravados %s nao sao os da equacao %s"
                             % (k, sorted(gravado), sorted(esperado)))

    pars = [k + "." + p for k in ph.ORDEM for p in des["equacoes"][k]["pars"]
            if p != "sigma"]
    med = {k + "." + p: float(des["equacoes"][k]["mediana"][p])
           for k in ph.ORDEM for p in des["equacoes"][k]["pars"] if p != "sigma"}
    draws = {k + "." + p: des["equacoes"][k]["draws"][p]
             for k in ph.ORDEM for p in des["equacoes"][k]["pars"] if p != "sigma"}
    hdi = {k + "." + p: des["equacoes"][k]["hdi"][p]
           for k in ph.ORDEM for p in des["equacoes"][k]["pars"] if p != "sigma"}

    pesos = {k: _ser(sub[panel.PESO_COL[k.lower()]]) for k in ph.ORDEM}
    ult = max(i for i in range(len(am_idx))
              if all(pesos[k][i] is not None for k in ph.ORDEM))
    tot = sum(pesos[k][ult] for k in ph.ORDEM)
    pesos_fim = {k: float(pesos[k][ult]) / tot for k in ph.ORDEM}

    infl = _ser(ins["infl_br"].reindex(am_idx))
    pre = _pre_grade(ins["infl_br"], am_idx, ACUM_I12 - 1)
    serie_i = list(pre) + list(infl)
    i12 = [_i12_de_trimestres(serie_i, len(pre) + i) for i in range(len(am_idx))]
    sis = des.get("sistema") or {}

    return {
        "key": "I",
        "nome": "Curva de Phillips",
        "explica": "infl_br",
        "unidade": "% no trimestre",
        "consome": ["hiato", "pi_e", "de", "icbr_agr_usd", "icbr_met_usd"],
        # As tres CONTAS que ela faz com os cartoes. O cambio e a unica que nao e so
        # uma variacao: a estimacao le o cambio MEDIO do trimestre e o cartao guarda o
        # de FECHAMENTO, que e o que a (F) produz. A ponte e a media de duas variacoes
        # de fechamento seguidas -- o que supoe o cambio andando em linha reta dentro do
        # trimestre. Medido na amostra: contra o medio de verdade ela correlaciona 0,91
        # (o fechamento sozinho, 0,64), e o erro da equacao de alimentacao passa de
        # 1,927 para 1,949 p.p.; o de bens industriais cai de 0,614 para 0,608.
        "deriva": {
            "de_med": {"op": "dlog_medio", "de": ["de"],
                       "nome": "Variação do câmbio médio do trimestre",
                       "nome_frase": "a variação do câmbio médio do trimestre",
                       "unidade": "% no trimestre"},
            "agr": {"op": "dlog", "de": ["icbr_agr_usd"],
                    "nome": "Variação das commodities agrícolas",
                    "nome_frase": "a variação das commodities agrícolas",
                    "unidade": "% no trimestre"},
            "met": {"op": "dlog", "de": ["icbr_met_usd"],
                    "nome": "Variação dos metais",
                    "nome_frase": "a variação dos metais",
                    "unidade": "% no trimestre"},
        },
        "grupos": grupos,
        "ordem_grupos": list(ph.ORDEM),
        # A primeira posicao da grade de onde ela consegue partir: a media movel de
        # servicos e de industriais precisa de quatro trimestres observados antes.
        "i0_min": ACUM_I12,
        # As quatro inflacoes observadas na grade: sao as defasagens e a media movel do
        # primeiro trimestre projetado.
        "obs_grupo": {k: _ser(sub[panel.SUB_COL[k.lower()]]) for k in ph.ORDEM},
        "pesos_obs": pesos,
        "pesos_fim": pesos_fim,
        "pesos_fim_em": "%dT%d" % (am_idx[ult].year, am_idx[ult].quarter),
        # O IPCA de 12 meses: o observado composto, e o que a recursao precisa para
        # compor o simulado nos tres primeiros trimestres da janela.
        "obs_insumo": {"infl_br": list(infl)},
        "pre_insumo": {"infl_br": list(pre)},
        "i12_obs": [None if x is None else round(float(x), 6) for x in i12],
        "y": list(infl),
        "ajuste": _ajuste_infl(df, ins, am_idx, grupos, med, pesos),
        "est_ini": "%dT%d" % (ini.year, ini.quarter),
        "est_fim": "%dT%d" % (fim.year, fim.quarter),
        "est_i0": _pos_na_grade(am_idx, ini, 0),
        "est_i1": _pos_na_grade(am_idx, fim, len(am_idx) - 1),
        "est_antes_da_grade": bool(ini < am_idx[0]),
        "mediana": med,
        "hdi": hdi,
        "hdi_prob": des["hdi_prob"],
        "pars": pars,
        "draws": draws,
        "n_draws": des["n_gravado"],
        "n_draws_total": des["n_total"],
        "priori": des["variante"],
        # Tres numeros do posterior que a ficha imprime, todos com a expectativa parada:
        # o repasse de um ano, o efeito de um ano de hiato, e quanto da massa e
        # explosiva. Medicao, nao afirmacao.
        "post": {
            "repasse_4t": (sis.get("repasse_4t") or {}).get("mediana"),
            "hiato_4t": (sis.get("hiato_4t") or {}).get("mediana"),
            "frac_explosivos": sis.get("frac_explosivos"),
        },
        "amostra": g_,
    }


def _ajuste_fx(ins: dict, am_idx, canais: list, des: dict, nivel: dict) -> list:
    """O ajuste de um passo da (F) na grade, com os pesos da mediana do posterior.

    Um passo quer dizer que TODAS as defasagens vem do observado -- e por isso ele e o
    gabarito exato: o navegador rodando `h = 1` a partir de cada trimestre tem de
    devolver estes mesmos numeros, digito a digito. Nulo onde alguma peca falta.
    """
    md = des["mediana"]
    sd = {c: float(des["sd_canal"]["d_" + c]) for c in canais}
    logret = set(des["log_ret"])
    ppp = (ins["infl_br"] - ins["infl_us"]).reindex(am_idx)
    de = ins["de"].reindex(am_idx)
    out = []
    for i in range(len(am_idx)):
        if i == 0 or pd.isna(ppp.iloc[i]) or pd.isna(de.iloc[i - 1]):
            out.append(None)
            continue
        val = float(ppp.iloc[i]) + md["alpha"] + md["phi"] * float(de.iloc[i - 1])
        falta = False
        for c in canais:
            cur, ant = nivel[c][i], nivel[c][i - 1]
            if cur is None or ant is None:
                falta = True
                break
            dz = (100.0 * (np.log(cur) - np.log(ant)) if c in logret else cur - ant)
            val += md["b_" + c] * (dz / sd[c])
        out.append(None if falta else round(float(val), 6))
    return out


def _eq_cambio(ins: dict, am_idx, des: dict) -> dict:
    """A equacao (F) como um item do bloco de equacoes.

    O que ela leva alem dos pesos: o `sd` de cada canal e a regra de variacao de cada
    um (nivel ou log-retorno). Sem os dois o navegador nao consegue transformar o NIVEL
    que o leitor digita na coluna padronizada que o coeficiente multiplica -- a conta
    sairia em outra unidade e nada na tela avisaria.
    """
    g = des["gerado_de"]
    # O arquivo de desenhos fala em NOME DE COLUNA (`d_fiscal`), porque e o vocabulario
    # da matriz de regressao; o payload fala em nome de canal (`fiscal`), porque e o
    # vocabulario das variaveis de input. A traducao vive aqui, num lugar so.
    canais = [c[2:] if c.startswith("d_") else c for c in g["canais"]]
    ini, fim = pd.Period(g["ini"], "Q"), pd.Period(g["fim"], "Q")
    nivel = {}
    for c in canais:
        s = ins["carry_vol"] if c == "carry_vol" else ins["niveis"][c]
        nivel[c] = _ser(s.reindex(am_idx))

    return {
        "key": "F",
        "nome": "Câmbio",
        "explica": "de",
        "unidade": "% no trimestre",
        # O que o leitor ESCOLHE. Nem `carry_vol` nem `ppp` estao aqui porque os dois
        # sao CONTA e nao premissa: quem tem cartao sao as pecas que o leitor escolhe
        # -- a Selic (que a (R) produz), o Fed Funds, a volatilidade e as duas
        # inflacoes.
        "consome": ["infl_br", "infl_us", "fiscal", "dxy_em", "sp500", "icbr_usd",
                    "ffr", "vol"],
        # O diferencial de inflacao foi cartao ate 2026-09-24, com as duas metades
        # atras de "abrir em partes". Virou conta da equacao pelo mesmo corte que levou
        # `di` e `ancora`.
        "deriva": {
            "ppp": {"op": "-", "de": ["infl_br", "infl_us"],
                    "nome": "Diferencial de inflação BR−US",
                    "nome_frase": "o diferencial de inflação entre Brasil e "
                                  "Estados Unidos",
                    "unidade": "p.p. no trimestre"},
        },
        "canais": canais,
        "lags": ["de_l1"],
        "offset": "ppp",
        # `(selic - ffr) / vol`, reconstruido a cada trimestre da rodada. Declarado em
        # dados e nao em codigo para a mesma conta valer no Python e no navegador.
        "carry": {"canal": "carry_vol", "juro": "selic", "menos": "ffr",
                  "sobre": "vol"},
        # A equacao produz a VARIACAO e o cartao dela mostra o NIVEL. A conversao e
        # declarada em dados, e nao implicita no JS: `de = 100*ln(P_t / P_{t-1})`,
        # ancorada em `ptax[i0-1]`. Os dois sentidos sao exatos.
        "explica_em": "nivel_log",
        "sd": {c: float(des["sd_canal"]["d_" + c]) for c in canais},
        "log_ret": [c for c in canais if c in des["log_ret"]],
        # O NIVEL observado de cada canal: e dele que sai a defasagem do primeiro
        # trimestre projetado, sem a qual a variacao daquele trimestre nao existe.
        "nivel": nivel,
        "y": _ser(ins["de"].reindex(am_idx)),
        "ptax": _ser(ins["ptax"].reindex(am_idx)),
        # O ajuste de UM PASSO, trimestre a trimestre, com os pesos da mediana. Ele nao
        # e desenhado: existe para o teste poder exigir que a recursao do NAVEGADOR
        # devolva exatamente estes numeros. As duas pontas sao a mesma conta escrita
        # duas vezes -- em Python aqui e em JS no relatorio --, e duas implementacoes
        # da mesma recursao divergem em silencio: um `sd` trocado, um log esquecido, um
        # sinal invertido continuam produzindo um caminho plausivel.
        "ajuste": _ajuste_fx(ins, am_idx, canais, des, nivel),
        "est_ini": "%dT%d" % (ini.year, ini.quarter),
        "est_fim": "%dT%d" % (fim.year, fim.quarter),
        "est_i0": int(am_idx.get_loc(ini)),
        "est_i1": int(am_idx.get_loc(fim)),
        "mediana": des["mediana"],
        "hdi": des["hdi"],
        "hdi_prob": des["hdi_prob"],
        "pars": des["pars"],
        "draws": des["draws"],
        "n_draws": des["n_gravado"],
        "n_draws_total": des["n_total"],
        "priori": des["variante"],
        "amostra": g,
    }


def construir(df: pd.DataFrame | None = None) -> dict:
    """Monta o payload do simulador: um bloco de equacoes e um de inputs."""
    if df is None:
        df = panel.construir()
    des = carregar_desenhos()
    des_fx = carregar_desenhos_fx()
    des_exp = carregar_desenhos_exp()
    des_is = carregar_desenhos_is()
    des_ph = carregar_desenhos_ph()

    d = taylor.montar(df)
    # O simulador precisa de toda linha em que a Selic e a ancora existam -- inclusive
    # as duas anteriores ao inicio da amostra de estimacao, que sao as condicoes
    # iniciais de qualquer partida naquele ponto.
    am = d[d["y"].notna()]
    est = d[["y", "r1", "r1b", "r2", "d08", "d20"]].dropna()

    ins = _insumos_fx(df, am.index)
    ins_i = _insumos_inflacao(df)
    v, ordem_v = _variaveis(df, d, am.index, ins, ins_i)
    eq = _eq_juros(d, am.index, des, est.index)
    eqf = _eq_cambio(ins, am.index, des_fx)
    eqe = _eq_expectativas(df.reindex(am.index), ins["infl_br"], am.index, des_exp)
    eqh = _eq_hiato(df, am.index, des_is)
    eqi = _eq_inflacao(df, ins, am.index, des_ph)

    # As equacoes tem de terminar no MESMO trimestre, senao a janela projetada de uma
    # comeca dentro da amostra da outra e a tela nao teria como dizer isso.
    fins = {e["key"]: e["est_fim"] for e in (eqh, eqi, eqe, eq, eqf)}
    if len(set(fins.values())) > 1:
        raise ValueError(
            "as equacoes foram estimadas ate trimestres diferentes (%s). Reestime "
            "todas antes de montar o simulador."
            % ", ".join("(%s) ate %s" % kv for kv in sorted(fins.items())))

    # Uma marca de crise declarada por DUAS equacoes tem de ser a mesma serie nas duas.
    # `entradas()` resolve cada marca uma vez so, pela primeira equacao que a declara
    # -- se as janelas divergissem, a segunda rodaria com a marca da primeira, sem erro
    # e com um resultado plausivel.
    vistas = {}
    for e in (eqh, eqi, eqe, eq, eqf):
        for c, s_ in (e.get("dummy_obs") or {}).items():
            if c in vistas and vistas[c][1] != s_:
                raise ValueError("a marca %r difere entre (%s) e (%s)"
                                 % (c, vistas[c][0], e["key"]))
            vistas.setdefault(c, (e["key"], s_))

    p = {
        "h_padrao": H_PADRAO, "h_max": H_MAX,
        # O ponto de partida NAO e escolha de quem le: e o trimestre seguinte ao fim da
        # janela estimada, e so ele. Ver o bloco "Horizonte" no topo deste arquivo.
        "i0": int(am.index.get_loc(est.index[-1])) + 1,
        # A primeira posicao da grade de onde as CINCO conseguem partir juntas -- a tela
        # so parte de `i0`, mas `main()` e o teste rodam a conta solta sobre a historia,
        # e ali a (I) e a que mais precisa de passado: quatro trimestres.
        "i0_min": max([2] + [int(e.get("i0_min") or 1) for e in (eqh, eqi, eqe, eq, eqf)]),
        "x": [p.start_time.strftime("%Y-%m-%d") for p in am.index],
        "rot": ["%dT%d" % (p.year, p.quarter) for p in am.index],
        # A ORDEM DE SOLUCAO dentro do trimestre, a do plano da pasta: a (H) le a Selic
        # do trimestre ANTERIOR, entao ela e conhecida primeiro; a (I) le o hiato; a (E)
        # le a inflacao; a (R) le a expectativa; a (F) le a Selic e a inflacao. Sobra um
        # elo no sentido contrario -- a alimentacao le o cambio do proprio trimestre --, e
        # e por ele e pelos lacos defasados que `resolver()` da voltas em vez de uma
        # passada so.
        "eq_ordem": [eqh["key"], eqi["key"], eqe["key"], eq["key"], eqf["key"]],
        "eq": {e["key"]: e for e in (eqh, eqi, eqe, eq, eqf)},
        # O nome de cada equacao do MODELO, para os grupos de exogenas especificas
        # poderem se chamar pelo nome mesmo quando a equacao ainda nao rodar aqui.
        "eq_nomes": dict(EQS_MODELO),
        # Os dois recortes das exogenas, com o rotulo e a explicacao de cada um. No
        # payload e nao no relatorio para os dois nao divergirem.
        "regioes": {k: {"nome": n, "sub": s} for k, (n, s) in REGIOES.items()},
        "var_ordem": ordem_v,
        "var": v,
    }
    # O GABARITO DO SISTEMA: o cenario que a aba abre, resolvido aqui com os pesos da
    # mediana. Os gabaritos de um passo de cada equacao provam cada recursao; nenhum
    # deles prova a conta que as junta, que e onde `resolver()` e `_simResolver()` podem
    # divergir -- uma volta a menos, uma equacao lendo o caminho da volta errada. Com o
    # laco fechado, e isso que precisa de gabarito proprio.
    i0, h = p["i0"], p["h_padrao"]
    coefs = {k: dict(p["eq"][k]["mediana"]) for k in p["eq_ordem"]}
    sol, voltas = resolver(p, coefs, i0, h, entradas(p, i0, h))
    p["sistema_padrao"] = {
        "voltas": voltas,
        "caminho": {p["eq"][k]["explica"]: [round(float(x), 9)
                                            for x in sol[p["eq"][k]["explica"]]]
                    for k in p["eq_ordem"]},
    }
    return p


# ─────────────────────────────────────────────────────────────────────────────
# a recursao, que e a MESMA que o navegador roda
# ─────────────────────────────────────────────────────────────────────────────
def derivadas(p: dict, ek: str, ent: dict, i0: int, h: int) -> dict:
    """As CONTAS que a equacao `ek` faz com o que ela consome.

    Ate 2026-09-24 estas contas viviam no payload como cartoes compostos, com as pecas
    atras de "abrir em partes". Com o corte pedido pelo usuario elas mudaram de dono:
    a equacao declara em `deriva` o que compoe, e as duas pontas -- este modulo e o
    navegador -- refazem a conta. E por refaze-la em dois lugares que a (R) ganhou
    gabarito de um passo junto com esta mudanca.

    `ent` ja traz o caminho resolvido de cada entrada, inclusive o da variavel que uma
    equacao anterior produziu nesta rodada (a expectativa, para a (R)).
    """
    eq = p["eq"][ek]
    out = {}
    for nome, spec in (eq.get("deriva") or {}).items():
        op, de = spec["op"], spec["de"]
        if op in ("-", "+"):
            a, b = ent[de[0]], ent[de[1]]
            out[nome] = [x - b[j] if op == "-" else x + b[j]
                         for j, x in enumerate(a)]
        elif op == "acum_log":
            # As defasagens anteriores a janela vem do OBSERVADO; dali em diante, do
            # caminho desta rodada. Sem isso o primeiro trimestre projetado nao teria
            # os quatro trimestres que o acumulado de doze meses precisa.
            pre = (eq.get("pre_insumo") or {}).get(de[0]) or []
            obs = eq["obs_insumo"][de[0]]
            serie = list(pre) + list(obs[:i0]) + list(ent[de[0]][:h])
            base = len(pre) + i0
            k = int(spec.get("k") or ACUM_I12)
            out[nome] = [_i12_de_trimestres(serie, base + j, k) for j in range(h)]
        elif op == "lin":
            # Combinacao linear das pecas com os pesos declarados. Existe porque o
            # aperto da (H) tem TRES pecas -- Selic, juro real de 10 anos e meta -- e os
            # `-`/`+` das outras equacoes tem duas.
            cs = [float(c) for c in spec["coef"]]
            out[nome] = [sum(cs[j] * ent[de[j]][k] for j in range(len(de)))
                         for k in range(h)]
        elif op in ("dlog", "dlog_medio"):
            # A variacao de um NIVEL. `dlog` e `100*ln(x_t/x_{t-1})`; `dlog_medio` e a
            # variacao do cambio MEDIO do trimestre, feita de dois fechamentos: a media
            # de duas variacoes seguidas, `50*ln(P_t/P_{t-2})`. Os niveis anteriores a
            # janela vem do OBSERVADO do cartao; dali em diante, do caminho da rodada.
            passo, fat = _DLOG[op]
            s = list(p["var"][de[0]]["obs"][:i0]) + list(ent[de[0]][:h])
            out[nome] = [None if (i0 + j - passo < 0 or s[i0 + j - passo] is None)
                         else fat * float(np.log(s[i0 + j] / s[i0 + j - passo]))
                         for j in range(h)]
        else:
            raise ValueError("operacao derivada desconhecida: %r" % op)
    return out


# (quantos trimestres atras, fator) de cada variacao de nivel.
_DLOG = {"dlog": (1, 100.0), "dlog_medio": (2, 50.0)}


def _deriv_obs_em(p: dict, ek: str, nome: str, i: int) -> float | None:
    """A conta `nome` da equacao `ek` sobre o OBSERVADO do trimestre `i` da grade.

    E de onde sai o valor das defasagens ANTERIORES a janela: o primeiro trimestre
    projetado da (H) le o aperto do trimestre que ja aconteceu, e o da (I) le o cambio e
    os metais do trimestre anterior. Feita dos cartoes, pela mesma declaracao, em vez de
    lida de uma copia gravada -- uma copia seria mais uma serie para discordar da conta.
    """
    sp = p["eq"][ek]["deriva"][nome]

    def ob(c, j):
        obs = p["var"][c]["obs"]
        return obs[j] if 0 <= j < len(obs) else None

    if sp["op"] == "lin":
        tot = 0.0
        for c, w in zip(sp["de"], sp["coef"]):
            v = ob(c, i)
            if v is None:
                return None
            tot += float(w) * float(v)
        return tot
    if sp["op"] in _DLOG:
        passo, fat = _DLOG[sp["op"]]
        a, b = ob(sp["de"][0], i), ob(sp["de"][0], i - passo)
        if a is None or b is None:
            return None
        return fat * float(np.log(a / b))
    raise ValueError("a operacao %r nao tem leitura pontual" % sp["op"])


def _sim_exp(p: dict, coef: dict, i0: int, h: int, ent: dict,
             eps: list | None = None) -> list:
    """Roda a equacao de expectativas solta e devolve a Focus de 12 meses simulada.

    **O peso da meta NAO vem do desenho: ele e `1 - e1 - e2`.** Os tres desenhos de
    `peso_meta` estao gravados, e usa-los aqui pareceria equivalente -- nao e, quando o
    coeficiente em uso e a MEDIANA de cada parametro: mediana nao e linear, entao as
    tres medianas nao somam 1 e a equacao deixaria de devolver a meta em repouso por
    alguns milesimos. Refazer a subtracao e o que mantem a restricao valendo com
    qualquer conjunto de pesos.
    """
    eq = p["eq"]["E"]
    der = derivadas(p, "E", ent, i0, h)
    peso = 1.0 - coef["e1"] - coef["e2"]
    ant = eq["y"][i0 - 1]
    out = []
    for k in range(h):
        val = coef["e1"] * ant + coef["e2"] * der["i12"][k] + peso * ent[eq["meta"]][k]
        if eps is not None:
            val += eps[k]
        ant = val
        out.append(val)
    return out


def _sim(p: dict, coef: dict, i0: int, h: int, ent: dict,
         eps: list | None = None) -> list:
    """Roda a regra de juros solta e devolve a Selic simulada.

    `ent` traz o caminho JA RESOLVIDO de cada entrada, com `h` valores -- inclusive o
    da expectativa que a (E) acabou de produzir, quando ela esta ligada. O desvio
    contra a meta e a ancora sao CONTAS feitas aqui, por `derivadas()`; ate 2026-09-24
    elas chegavam prontas, como cartoes proprios.

    **As dummies de crise entram.** Deixa-las de fora nao levanta nada e custa caro: a
    primeira versao deste modulo as esquecia e a corrida solta acusava o maior desvio em
    2020T4, exatamente dentro da janela da `d20`.
    """
    eq = p["eq"]["R"]
    der = derivadas(p, "R", ent, i0, h)
    t1, t2, t3 = coef["t1"], coef["t2"], coef["t3"]
    y = [eq["y"][i0 - 2], eq["y"][i0 - 1]]
    peso = 1.0 - t1 - t2
    out = []
    for k in range(h):
        val = t1 * y[-1] + t2 * y[-2] + peso * t3 * der["di"][k]
        for c in eq["dummies"]:
            dv = ent[c][k]
            if dv:
                val += coef.get(c, 0.0) * dv
        if eps is not None:
            val += eps[k]
        y.append(val)
        out.append(val + der["ancora"][k])
    return out


def _sim_is(p: dict, coef: dict, i0: int, h: int, ent: dict,
            eps: list | None = None) -> list:
    """Roda a curva IS solta e devolve o hiato simulado, em % do produto potencial.

    `ent["selic"]` tem de ser o caminho JA RESOLVIDO da Selic desta rodada -- o que a
    (R) produziu, quando ela esta ligada. Resolver isso e trabalho de quem chama, como
    a expectativa dentro da (R).

    **O aperto chega com `lag` trimestres de atraso**, entao o primeiro trimestre
    projetado le o aperto de um trimestre que ja aconteceu: ele vem do OBSERVADO, feito
    dos cartoes pela mesma conta. Dali em diante, do caminho da rodada.

    **As marcas de crise entram**, com o peso estimado, e valem zero em todo trimestre
    projetado -- mesma regra da (R), pelo mesmo motivo.
    """
    eq = p["eq"]["H"]
    der = derivadas(p, "H", ent, i0, h)
    lag = int(eq["lag"])
    cam_gap = ([_deriv_obs_em(p, "H", "gap", i0 - lag + j) for j in range(lag)]
               + list(der["gap"]))
    h_ant = eq["y"][i0 - 1]
    out = []
    for k in range(h):
        val = coef["h1"] * h_ant + coef["h2"] * cam_gap[k]
        for c in eq["dummies"]:
            dv = ent[c][k]
            if dv:
                val += coef.get(c, 0.0) * dv
        if eps is not None:
            val += eps[k]
        out.append(val)
        h_ant = val
    return out


def _tri(p: dict, i: int) -> int:
    """O trimestre do ano (1 a 4) da posicao `i` da grade, inclusive alem dela.

    Contado a partir do ultimo rotulo, e nao de uma data: e a mesma conta de
    `_simPassoTri` no navegador, e as duas tem de concordar porque o trimestre decide a
    dummy sazonal de cada passo da (I).
    """
    ult = p["rot"][-1]
    n = int(ult[5:]) + (i - (len(p["rot"]) - 1))
    return ((n - 1) % 4) + 1


def _pesos_em(eq: dict, i: int) -> dict:
    """Os pesos dos quatro grupos no trimestre `i`: o publicado, se houver; se nao, o
    do ultimo trimestre publicado."""
    po = eq["pesos_obs"]
    if all(0 <= i < len(po[k]) and po[k][i] is not None for k in eq["ordem_grupos"]):
        return {k: po[k][i] for k in eq["ordem_grupos"]}
    return dict(eq["pesos_fim"])


def _sim_infl(p: dict, coef: dict, i0: int, h: int, ent: dict,
              partes: list | None = None, eps: dict | None = None) -> list:
    """Roda a curva de Phillips solta e devolve o IPCA cheio do trimestre, em 100*dlog.

    Quatro recursoes por dentro, uma por grupo, cada uma a MESMA de
    `phillips_sub.estimar_uma`: a inercia e os termos restritos dividem com a expectativa
    um peso que soma 1, e o da expectativa e o que sobra -- refeito aqui a cada conjunto
    de pesos, e nao lido do desenho gravado, pela mesma razao da (E).

    O que cada uma le, e de onde:

        propria inflacao defasada e media de 4    observado ate i0-1, depois o caminho
        expectativa do trimestre anterior / 4     `ent["pi_e"]`, defasado
        hiato do mesmo trimestre                  `ent["hiato"]`
        cambio medio, commodities                 contas de `deriva` sobre os cartoes
        IPCA cheio defasado (monitorados)         observado, depois o caminho

    O cheio e a soma dos quatro com os pesos de `_pesos_em`, em variacao simples, e sai
    em `100*ln(1 + x/100)`, que e a unidade do cartao: as duas formas do IPCA do
    trimestre sao a mesma serie (medido: 0 de diferenca em 99 trimestres).
    """
    eq = p["eq"]["I"]
    if i0 < int(eq["i0_min"]):
        # Levanta em vez de seguir: o fatiamento do Python devolveria uma media movel de
        # menos de quatro trimestres sem reclamar, e o caminho sairia plausivel.
        raise ValueError("a (I) precisa de %d trimestres observados antes da partida; "
                         "i0 = %d" % (eq["i0_min"], i0))
    der = derivadas(p, "I", ent, i0, h)
    G, ordem = eq["grupos"], eq["ordem_grupos"]
    hist = {k: list(eq["obs_grupo"][k][:i0]) for k in ordem}
    cheio = [None if v is None else 100.0 * (float(np.exp(v / 100.0)) - 1.0)
             for v in p["var"]["infl_br"]["obs"][:i0]]
    pie_obs = p["var"]["pi_e"]["obs"]

    def defas(nome, k):
        return der[nome][k - 1] if k >= 1 else _deriv_obs_em(p, "I", nome, i0 - 1)

    out = []
    for k in range(h):
        q = _tri(p, i0 + k)
        e4 = (ent["pi_e"][k - 1] if k >= 1 else pie_obs[i0 - 1]) / 4.0
        fonte = {"hiato": ent["hiato"][k], "de_med": der["de_med"][k],
                 "de_med_l1": defas("de_med", k), "agr": der["agr"][k],
                 "met": der["met"][k], "met_l1": defas("met", k)}
        w = _pesos_em(eq, i0 + k)
        grp, tot = {}, 0.0
        for g in ordem:
            spec = G[g]

            def c(n, g=g):
                return coef[g + "." + n]

            val = c(spec["inercia"]) * hist[g][-1]
            peso = 1.0 - c(spec["inercia"])
            for par, tipo in spec["restritos"]:
                x = (sum(hist[g][-ACUM_I12:]) / ACUM_I12 if tipo == "mm4"
                     else cheio[-1])
                val += c(par) * x
                peso -= c(par)
            val += peso * e4
            for par, tipo in spec["regs"]:
                val += c(par) * fonte[tipo]
            for j, s in enumerate(spec["saz"], start=1):
                val += c(s) * _saz(q, j)
            if eps and g in eps:
                val += eps[g][k]
            grp[g] = val
            tot += w[g] * val
        for g in ordem:
            hist[g].append(grp[g])
        cheio.append(tot)
        out.append(100.0 * float(np.log1p(tot / 100.0)))
        if partes is not None:
            partes.append({"grupos": grp, "cheio": tot, "pesos": w})
    return out


def _roda(p: dict, ek: str, coef: dict, i0: int, h: int, ent: dict,
          eps=None) -> list:
    """O caminho que a equacao `ek` produz, na unidade do CARTAO que ela explica.

    So a (F) converte: ela produz a variacao do cambio e o cartao dela mostra o nivel.

    `eps` e um choque no RESIDUO daquela equacao, trimestre a trimestre, na unidade da
    propria equacao -- e o que a aba Impulso-resposta usa. Ele entra ANTES de o valor
    virar defasagem, entao a dinamica da propria equacao o propaga. Na (I) ele e um
    dicionario por grupo, porque o residuo e de cada um dos quatro.
    """
    if ek == "E":
        return _sim_exp(p, coef, i0, h, ent, eps)
    if ek == "R":
        return _sim(p, coef, i0, h, ent, eps)
    if ek == "H":
        return _sim_is(p, coef, i0, h, ent, eps)
    if ek == "I":
        return _sim_infl(p, coef, i0, h, ent, eps=eps)
    if ek == "F":
        return _nivel_cambio(p, i0, _sim_fx(p, coef, i0, h, ent, ent["selic"], eps))
    raise ValueError("equacao desconhecida: %r" % ek)


# Quando parar de dar voltas. As variaveis vivem entre 0 e 20, entao 1e-10 e muito abaixo
# de qualquer casa que a tela imprime; e o teto so existe para um defeito de verdade
# aparecer como erro e nao como uma tela que nunca termina de desenhar.
TOL_LACO = 1e-10
MAX_VOLTAS = 100


def resolver(p: dict, coefs: dict, i0: int, h: int, ent: dict,
             liga: dict | None = None, choque: dict | None = None) -> tuple[dict, int]:
    """Resolve as equacoes LIGADAS juntas e devolve (`ent` resolvido, voltas).

    ## Por que a ordem de solucao deixou de bastar

    Ate 2026-09-28 o simulador era uma corrente, `E -> R -> H -> F`, e cada equacao
    rodava uma vez so, lendo o que as anteriores tinham acabado de produzir. A (I) fecha
    o laco: ela le o hiato, a expectativa e o cambio, e a inflacao que ela produz volta
    para a (E) e para a (F). Uma passada so deixaria alguem lendo um caminho velho.

    A conta e a de Gauss-Seidel sobre o CAMINHO: cada volta roda as equacoes na ordem de
    solucao, cada uma lendo o que ja saiu nesta volta e, do resto, o da volta anterior,
    ate nenhum caminho mudar mais que `TOL_LACO`. A solucao e a mesma de resolver
    trimestre a trimestre -- ela e o ponto fixo das cinco equacoes juntas.

    ## E por que converge depressa

    Dentro do trimestre ha um elo so no sentido contrario da ordem: a alimentacao le o
    cambio do proprio trimestre, e o cambio le a inflacao do proprio trimestre. O ganho
    desse laco e o peso da alimentacao vezes o repasse dela vezes metade (a outra metade
    do cambio medio e do trimestre anterior): 0,157 x 0,085 x 0,5 = 0,007. Os lacos que
    passam por defasagem -- inflacao, expectativa, Selic, hiato, inflacao -- tem ganho da
    mesma ordem. Medido no cenario padrao: poucas voltas.

    `liga` diz quais equacoes rodam (as outras mantem o caminho que ja esta em `ent`,
    imposto ou observado); o default e todas. `choque` leva, por equacao, um choque no
    residuo dela (ver `_roda`); o default e nenhum.
    """
    ent = {k: list(v) for k, v in ent.items()}
    liga = liga or {k: True for k in p["eq_ordem"]}
    for volta in range(1, MAX_VOLTAS + 1):
        dif = 0.0
        for ek in p["eq_ordem"]:
            if not liga.get(ek):
                continue
            var = p["eq"][ek]["explica"]
            novo = _roda(p, ek, coefs[ek], i0, h, ent, (choque or {}).get(ek))
            dif = max(dif, max(abs(a - b) for a, b in zip(novo, ent[var])))
            ent[var] = novo
        if dif < TOL_LACO:
            return ent, volta
    raise RuntimeError("as equacoes nao convergiram em %d voltas (ultima diferenca %.2e)"
                       % (MAX_VOLTAS, dif))


def _sim_fx(p: dict, coef: dict, i0: int, h: int, ent: dict, selic: list,
            eps: list | None = None) -> list:
    """Roda a equacao do cambio solta e devolve a variacao simulada, em % do trimestre.

    `selic` e o caminho que a (R) acabou de produzir -- e por ele que as duas equacoes
    se ligam. Rodar a (F) com a Selic observada e um cenario diferente e legitimo, e e
    o que sai quando a Selic esta em Exogeno ou Observado; quem resolve isso e quem
    chama, como faz com qualquer outra entrada.

    **O nivel anterior de cada canal vem do OBSERVADO**, e nao de zero: a equacao le a
    variacao de um trimestre para o outro, entao o primeiro trimestre projetado precisa
    do trimestre que veio antes dele. Sem essa ancora a primeira variacao seria o
    proprio nivel, o que num CDS de 125 pontos daria um choque de 125 pontos-base.
    """
    eq = p["eq"]["F"]
    der = derivadas(p, "F", ent, i0, h)
    logret = set(eq["log_ret"])
    prev = {c: eq["nivel"][c][i0 - 1] for c in eq["canais"]}
    de_ant = eq["y"][i0 - 1]
    out = []
    for k in range(h):
        val = der[eq["offset"]][k] + coef["alpha"] + coef["phi"] * de_ant
        for c in eq["canais"]:
            if c == "carry_vol":
                cur = (selic[k] - ent["ffr"][k]) / ent["vol"][k]
            else:
                cur = ent[c][k]
            dz = (100.0 * (np.log(cur) - np.log(prev[c])) if c in logret
                  else cur - prev[c])
            val += coef["b_" + c] * (dz / eq["sd"][c])
            prev[c] = cur
        if eps is not None:
            val += eps[k]
        de_ant = val
        out.append(val)
    return out


def _nivel_cambio(p: dict, i0: int, de: list) -> list:
    """A sequencia de variacoes virando nivel em R$/US$, a partir do ultimo observado.

    A leitura de um cenario cambial e o NIVEL, e nao a variacao que o produz -- por
    isso o grafico desenha isto e as caixas mostram aquilo. As duas sao o mesmo
    caminho: `ptax(t) = ptax(t-1) * exp(de(t)/100)`, que e a inversa exata de
    `de = 100*dlog(ptax)`, a forma em que a equacao foi estimada.
    """
    p0 = p["eq"]["F"]["ptax"][i0 - 1]
    out = []
    for v in de:
        p0 = p0 * float(np.exp(v / 100.0))
        out.append(p0)
    return out


def _media_final(serie: list, k: int) -> float | None:
    """A media dos ultimos `k` valores publicados. `None` se nao houver nenhum."""
    vals = [v for v in serie if v is not None]
    if not vals:
        return None
    vals = vals[-max(1, k):]
    return float(sum(vals)) / len(vals)


def _obs_lista(serie: list, i0: int, h: int, segura: dict | None = None) -> list:
    """O caminho observado, com a regra de SEGURAR declarada pela variavel.

    Default: segure o ultimo valor publicado. Com `segura={"modo":"media","k":n}`,
    segure a media dos `n` ultimos publicados -- o que vale para taxa de fluxo, onde um
    trimestre e ruido, e nao vale para nivel. Ver `SEGURA_MEDIA_K`.

    **A media so vale DEPOIS do ultimo dado.** Um buraco no meio da serie continua
    segurando o ultimo valor conhecido: ali o que falta e uma observacao, nao o futuro.
    """
    ultimo = -1
    for j, v in enumerate(serie):
        if v is not None:
            ultimo = j
    media = None
    if segura and segura.get("modo") == "media" and ultimo >= 0:
        media = _media_final(serie, int(segura.get("k") or 1))

    out, ult = [], 0.0
    for i in range(0, i0 + h):
        if i < len(serie) and serie[i] is not None:
            ult = serie[i]
        val = media if (media is not None and i > ultimo) else ult
        if i >= i0:
            out.append(val)
    return out


def _observado(p: dict, key: str, i0: int, h: int) -> list:
    """O caminho observado de uma entrada, segurando o ultimo valor quando falta.

    As marcas de crise NAO tem cartao desde 2026-09-24 -- elas viajam dentro da propria
    equacao que as le. Procura-las aqui estourava `KeyError`, e o `main()` deste modulo
    foi o unico consumidor a notar, tarde.
    """
    v = p["var"].get(key)
    if v is not None and v["obs"] is not None:
        return _obs_lista(v["obs"], i0, h, v.get("segura"))
    for e in p["eq"].values():
        if key in (e.get("dummy_obs") or {}):
            return _obs_lista(e["dummy_obs"][key], i0, h)
    raise KeyError("nao ha serie observada para %r" % key)


def entradas(p: dict, i0: int, h: int) -> dict:
    """O caminho observado de tudo o que ALGUMA equacao consome, mais as dummies.

    Derivado do `consome` de cada equacao e nao escrito a mao: uma equacao nova que
    leia uma variavel nova passa a ter o caminho dela aqui sem ninguem lembrar de vir
    aqui. E o espelho de `simEntradas()` no navegador.
    """
    ent = {}
    for ek in p["eq_ordem"]:
        e = p["eq"][ek]
        for c in e["consome"]:
            if c not in ent:
                ent[c] = _observado(p, c, i0, h)
        for c in e.get("dummies") or []:
            ent[c] = _observado(p, c, i0, h)
    return ent


def main() -> dict:
    p = construir()
    eq = p["eq"]["R"]
    n = len(p["x"])
    print("SIMULADOR")
    print("  grade      %s a %s, %d trimestres" % (p["rot"][0], p["rot"][-1], n))
    print("  horizonte  ate %d trimestres (default %d)" % (p["h_max"], p["h_padrao"]))

    print("\n  EQUACOES (%d), na ordem de solucao dentro do trimestre"
          % len(p["eq_ordem"]))
    for k in p["eq_ordem"]:
        e = p["eq"][k]
        md = e["mediana"]
        print("    (%s) %-16s explica %-7s consome %s"
              % (k, e["nome"], e["explica"], ", ".join(e["consome"])))
        print("         amostra %s a %s | %d desenhos, priori '%s'"
              % (e["est_ini"], e["est_fim"], e["n_draws"], e["priori"]))
        der = e.get("deriva") or {}
        if der:
            def _fmt_der(sp):
                if sp["op"] in ("+", "-"):
                    return (" %s " % sp["op"]).join(sp["de"])
                if sp["op"] == "lin":
                    partes = []
                    for j, (c, w) in enumerate(zip(sp["de"], sp["coef"])):
                        if j == 0:
                            partes.append(c if w > 0 else "-" + c)
                        else:
                            partes.append(("+ " if w > 0 else "- ") + c)
                    return " ".join(partes)
                if sp["op"] in _DLOG:
                    passo, fat = _DLOG[sp["op"]]
                    return "%g*ln(%s_t / %s_t-%d)" % (fat, sp["de"][0], sp["de"][0], passo)
                return "%s(%s, %d tri)" % (sp["op"], sp["de"][0], sp["k"])
            print("         deriva  %s"
                  % "  ".join("%s = %s" % (n, _fmt_der(sp)) for n, sp in der.items()))
        if k == "R":
            print("         t1 %+.3f  t2 %+.3f  t3 %+.3f"
                  % (md["t1"], md["t2"], md["t3"]))
        elif k == "E":
            print("         e1 %+.3f  e2 %+.3f  meta %+.3f"
                  % (md["e1"], md["e2"], 1.0 - md["e1"] - md["e2"]))
        elif k == "H":
            print("         h1 %+.3f  h2 %+.4f  d08 %+.3f  d20 %+.3f | aperto defasado %d "
                  "tri | %.1f%% da massa com h2 < 0, %.2f%% explosiva"
                  % (md["h1"], md["h2"], md["d08"], md["d20"], e["lag"],
                     100 * e["h2_negativo"], 100 * e["fora_estavel"]))
        elif k == "I":
            for g in e["ordem_grupos"]:
                gg = e["grupos"][g]
                termos = [gg["inercia"]] + [q for q, _t in gg["restritos"]] \
                    + [q for q, _t in gg["regs"]]
                print("         %-3s %-17s %s" % (g, gg["nome"], "  ".join(
                    "%s %+.3f" % (q, md[g + "." + q]) for q in termos)))
            print("         pesos no fim: %s (%s)" % ("  ".join(
                "%s %.3f" % kv for kv in e["pesos_fim"].items()), e["pesos_fim_em"]))
        else:
            print("         alpha %+.3f  phi %+.3f  %s"
                  % (md["alpha"], md["phi"],
                     "  ".join("%s %+.2f" % (c, md["b_" + c]) for c in e["canais"])))

    print("\n  INPUTS (%d)" % len(p["var_ordem"]))
    print("    %-9s %-10s %-10s %-26s %s"
          % ("chave", "tipo", "regiao", "produzida por", "lida por"))
    for k in p["var_ordem"]:
        v = p["var"][k]
        prod = v["produzida_por"]
        quem = ("(%s), %s" % (prod, "no simulador" if v["produtor_no_sim"]
                              else "AINDA FORA do simulador")) if prod else "nenhuma"
        print("    %-9s %-10s %-10s %-26s %s"
              % (k, v["tipo"], v.get("regiao") or "-", quem,
                 ", ".join(v["consumida_por"])))

    # Uma corrida solta com tudo no observado, para o modulo nao afirmar sem medir.
    # "Solta" quer dizer que so as defasagens iniciais vem do dado: dali em diante cada
    # equacao se alimenta do que as cinco produziram -- que e uma prova bem mais dura do
    # que o ajuste de cada uma.
    i0, h = max(eq["est_i0"], p["i0_min"]), p["h_padrao"]
    coefs = {k: dict(p["eq"][k]["mediana"]) for k in p["eq_ordem"]}
    sol, voltas = resolver(p, coefs, i0, h, entradas(p, i0, h))
    print("\n  corrida solta de %s, %d trimestres, as cinco ligadas (%d voltas):"
          % (p["rot"][i0], h, voltas))
    for k in p["eq_ordem"]:
        var = p["eq"][k]["explica"]
        obs = np.array(p["var"][var]["obs"][i0:i0 + h], dtype=float)
        e = np.array(sol[var]) - obs
        print("    (%s) %-9s erro medio absoluto %.3f   RMSE %.3f   (%s)"
              % (k, var, np.abs(e).mean(), float(np.sqrt((e ** 2).mean())),
                 p["var"][var]["unidade"]))
    # e em doze meses, que e como inflacao se le
    eqi = p["eq"]["I"]
    serie = list(eqi["pre_insumo"]["infl_br"]) + list(eqi["obs_insumo"]["infl_br"][:i0]) \
        + list(sol["infl_br"])
    base = len(eqi["pre_insumo"]["infl_br"]) + i0
    i12s = np.array([_i12_de_trimestres(serie, base + j) for j in range(h)])
    i12o = np.array(eqi["i12_obs"][i0:i0 + h], dtype=float)
    print("        IPCA de 12 meses: erro medio %.3f   RMSE %.3f p.p."
          % (np.abs(i12s - i12o).mean(), float(np.sqrt(((i12s - i12o) ** 2).mean()))))

    # O cenario que a aba abre, e o que a curva de Phillips muda nele: a mesma conta com
    # ela desligada, a inflacao no observado (a media dos ultimos quatro trimestres).
    sp = p["sistema_padrao"]
    i0, h = p["i0"], p["h_padrao"]
    ent0 = entradas(p, i0, h)
    liga = {k: True for k in p["eq_ordem"]}
    liga["I"] = False
    sem, v2 = resolver(p, coefs, i0, h, ent0, liga)
    print("\n  cenario padrao, %s a %s, %d voltas; e sem a curva de Phillips (%d):"
          % (p["rot"][-1], "+%d tri" % h, sp["voltas"], v2))
    for k in p["eq_ordem"]:
        var = p["eq"][k]["explica"]
        a, b = sp["caminho"][var][-1], sem[var][-1]
        print("    %-9s no fim %9.3f   sem a (I) %9.3f   diferenca %+.3f"
              % (var, a, b, a - b))
    return p

if __name__ == "__main__":
    main()
