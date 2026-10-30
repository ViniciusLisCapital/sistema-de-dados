# Chat B — Agentes de mercado de trabalho e crédito

**Objetivo.** Criar os agentes `mercado_trabalho` e `credito` para que rodem no ciclo 2 junto com os sete. Cada um precisa de mapa conceitual aprovado, lista de dados, módulo de dados e definição, e os sete precisam ser ajustados. A camada 1 de literatura e de modelos mentais deles é feita pelo chat D, a partir dos mapas aprovados aqui.

**Ler primeiro:**
- `README.md` desta pasta.
- `PRINCIPIOS_AGENTES.md` inteiro: os princípios de todo agente, aplicados sem perguntar.
- `SISTEMA_AGENTES.md`:
    - I.II.ii e I.III.vi (o mapa conceitual é o contrato da área: perguntas, esqueleto causal, saídas, entradas, conceitos);
    - I.III.ix–xii (endógeno, exógeno, TWA, endógeno de outro agente);
    - **III.III.vii** (as fronteiras do primeiro batch; a atividade absorveu o mercado de trabalho "provisoriamente, até existir o agente dele");
    - V.IV.i (as tabelas `mt_*` hoje na atividade), V.II.vi, V.IV.viii e V.V.viii (crédito, TWA na PM, na atividade e no fiscal).
- Um agente novo do primeiro batch como molde, por exemplo o fiscal: o mapa `obsidian/fiscal_policy/fiscal_policy_conceptual_map.md`, o módulo `analytics/agent_system/dados/fiscal.py` e a definição `.claude/agents/fiscal-analyst.md`.
- O que o banco tem: `analytics/brasil/credit/CLAUDE.md`, `analytics/brasil/labor_market/CLAUDE.md` e `domain/db/CLAUDE.md` (tabelas `cred_*` e `mt_*`).
- O tracker: a aba "Qual - Labor Market" tem 25 candidatas; não há aba de crédito.


## O que precisa do usuário, em ordem

O processo é o da Fase 8 do Plano 1: um subagente Opus rascunha o mapa (Partes 1–4) e a lista de dados, e cada parte é aprovada numa janela, um agente de cada vez.

1. **As fronteiras.**
    - Mercado de trabalho: o que sai da atividade (`mt_pnad`, `mt_desocupacao_retro`, `mt_caged`, `mt_caged_setor`) e o que fica (o hiato fica com a atividade).
    - Crédito: o que é dele e não da PM (o canal de crédito), do fiscal (o crédito parafiscal e o BNDES, canal 2.5 do fiscal) ou da atividade (o impulso de crédito).
2. **As perguntas centrais** de cada um.
3. **A variável, o horizonte e o upside/downside.** Hoje nenhum dos dois tem variável no Modelo Estrutural. A decidir com o chat C (frente do modelo): se o crédito entra na curva IS e se o desemprego entra no hiato. Até lá vale a regra do fiscal e do externo: a tese é o caminho base das exógenas que tutelam, e a distribuição em volta é deles.
4. **A lista de dados.** As lacunas de tempestividade já conhecidas: `cred_fluxo_financeiro` parado em abr/26 e `mt_pnad` fora do job de rotina (achados da Fase 10; confirmar se continuam).
5. **As saídas e as entradas**, espelhadas nos mapas dos sete.
6. **A tutela de exógenas**, se houver alguma para os dois. Quem preenche a aba "Exógenas" é o usuário.


## Passos

- **B1.** Os dois mapas, Partes 1–4, aprovados parte a parte, mais a lista de dados (para o SISTEMA, pelo principal, como V.VIII e V.IX). Ao fim, avisar o chat D, pelo principal, que os mapas estão prontos (D2 começa daí).
- **B2.** Os módulos `dados/mercado_trabalho.py` e `dados/credito.py`, com teste (Sonnet), e as definições `.claude/agents/mercado-trabalho-analyst.md` e `credito-analyst.md` (Opus), derivadas das que existem.
- **B3.** O ajuste dos sete, numa janela que o principal libera:
    - as linhas de saída e entrada com os dois novos nos mapas dos sete;
    - o que era TWA vira "endógeno de <agente> (consulta)" nos módulos de dados dos sete;
    - a lista do que muda nas definições dos sete vai para o chat E.
- **B4.** Pedir ao chat E o registro dos dois novos: a linha em `AGENTES`, a pasta `credit` no `OWNERS` do tracker e no `AREA` do retrato, a checagem de consulta entre todos os pares, e as colunas na aba Exógenas.

**Escreve:** este arquivo, `obsidian/labor_market/` e `obsidian/credit/` (os mapas), as duas definições novas, os dois módulos novos e os testes deles; na janela B3, as linhas dos mapas dos sete e o reagrupamento nos módulos dos sete. **Não escreve:** as definições dos sete, o motor, o `__main__` e o retrato (chat E), a Parte 5 dos mapas e a literatura (chat D), o modelo (chat C).

**Pronto quando:** os dois mapas passam no `vault.py map`, `dados <agente> --ciclo <data>` roda para os dois e o `motor.conferir` bate, as definições estão aprovadas e os sete foram ajustados.


## Estado

- 2026-10-30 — leitura feita (README, PRINCIPIOS, SISTEMA I.III, III.III.vii, V.II.v–vi, V.IV, V.V.viii, o mapa fiscal como molde, os canais de crédito e de trabalho nos mapas de atividade, PM e inflação, o tracker, o banco). Nada escrito fora deste arquivo. Aguardando a liberação do principal para o B1.
- **Achados do banco (30/10):** `mt_pnad` vai até 2026-09 (em dia; não está no `--continuous`, mas nenhuma tabela de divulgação está: entra pelo passe completo ou pelo botão). `cred_fluxo_financeiro` continua parado em 2026-04 (a edição de set/26 do RPM saiu sem o gráfico). Os outros: `mt_caged` e `mt_caged_setor` 2026-08, `mt_desocupacao_retro` 2026-07, `mt_pnad_trimestral` 2026-04 (2T), `cred_ptc` 2026-04 (trimestral), `cred_credito_familias` 2026-08, demais `cred_*` 2026-09. Nenhuma exógena do modelo é de crédito ou de trabalho (aba Exógenas).
- **Plano do B1**, um agente de cada vez, mercado de trabalho primeiro (fronteira mais simples):
    1. Janela de fronteiras (usuário), os dois de uma vez. Proposta: MT leva da atividade `mt_pnad`, `mt_desocupacao_retro`, `mt_caged`, `mt_caged_setor` (e decide se `mt_pnad_trimestral`, `mt_caged_uf`, `mt_caged_salario` entram); o hiato fica com a atividade, e a folga do trabalho (desocupação contra a NAIRU) vira saída do MT para atividade, inflação e PM; o mercado de trabalho dos EUA (`mt_jolts`, `mt_ces`, `mt_cps`) fica com o externo. Crédito leva todas as `cred_*` (as 11 hoje TWA mais porte, atividade econômica e tipo de cliente); a PM conclui sobre a transmissão e a postura, lendo a condição de crédito que o crédito dá; o parafiscal fica com o fiscal (a decisão de governo, `fisc_dlsp_fatores`), e o crédito diz quanto direcionado e bancos públicos crescem; o impulso de crédito (`cred_fluxo_financeiro`) passa ao crédito, e a atividade conclui o efeito no hiato.
    2. Janela das perguntas centrais de cada um.
    3. Janela da variável da tese, horizonte e upside/downside: proposta provisória (desocupação dessazonalizada no fechamento do trimestre; para crédito, a decidir entre impulso e crescimento real das concessões), com a pergunta ao chat C pelo principal sobre crédito na IS e desemprego no hiato.
    4. Um subagente Opus por agente rascunha as Partes 1–4 do mapa e a lista de dados, no molde do fiscal, com as decisões das janelas 1–3; eu confiro com o `vault.py map`.
    5. Janelas de aprovação parte a parte (2, 3, 4) e a lista de dados numerada, de uma vez.
    6. As decisões e a lista vão para "Decisões" deste arquivo (para o principal levar a V.VIII e V.IX); pedido ao principal de avisar o D.
- **Arquivos que o B1 toca:** este arquivo; `obsidian/labor_market/labor_market_conceptual_map.md` (novo; a pasta já existe, com clean_md e synthesis do D, que não toco); `obsidian/credit/credit_conceptual_map.md` (pasta nova, só o mapa). Nada nos mapas nem nos módulos dos sete (B3).
- 2026-10-30 — a pedido do principal, as decisões do usuário passam por ele: as janelas 1 (fronteiras, 4 perguntas: 1a trabalho × atividade, 1b crédito × PM, 1c crédito × fiscal, 1d crédito × atividade) e 2 (perguntas centrais: T1–T4 e C1–C5) foram enviadas ao principal por SendMessage. A janela 3 espera a posição do C. Nenhum subagente até a liberação.
- 2026-10-30 — janela 1 decidida (ver Decisões); a janela 2 vem pelo principal. **Posição do C para a janela 3:** o usuário mandou testar um hiato estimado a partir de PIB, CAGED, desocupação e NUCI (teste A, rodando). Se passar, desocupação e CAGED movem o ponto de partida do hiato, e num passo seguinte o MT pode virar dono desses dois caminhos (seria a variável da tese dele). Crédito na IS fica parado até o resultado do hiato. A janela 3 espera o teste A.
- 2026-10-30 — janela 2 decidida (ver Decisões: MT com cinco perguntas, crédito com seis). **Resultado do teste A do C:** a desocupação é o que mais move o hiato estimado (0,8 de 1,0 p.p. da diferença contra o BC hoje); CAGED e PIB não pesam. A pergunta da NAIRU é do MT, entre ou não algo no modelo. O usuário ainda decide se o teste segue (NAIRU variável no tempo). A janela 3 sai quando o C fechar.
- 2026-10-30 — o usuário adiou as decisões do Modelo Estrutural para antes do ciclo 2; o principal liberou os subagentes dos mapas, com a variável da tese marcada "provisória, decide com o modelo" (MT: desocupação, se entrar no modelo, ou o caminho do que tutela; crédito: impulso ou crescimento real das concessões). Subagente Opus do mapa do MT lançado (Partes 1–4 + lista de dados); o do crédito vem depois dele.
- **Formato das janelas daqui em diante** (pedido do usuário, pelo principal, 30/10): cada decisão com (1) a pergunta numa frase simples, sem código interno; (2) por opção, o impacto prático (o que muda no agente, no relatório ou no ciclo, custo, o que destrava ou trava); (3) a recomendação e o porquê numa linha; (4) um exemplo real curto quando ajudar. Decisão técnica que não é dele, o B decide e só menciona.
- 2026-10-30 — **mapa do MT rascunhado**: `obsidian/labor_market/labor_market_conceptual_map.md` (437 linhas, Partes 1–4, Parte 5 é do D), `vault.py map labor_market` PASS. Lista de dados (23 tabelas: 7 endógenas, 16 de consulta, nenhuma TWA/exógena) no scratchpad, a entrar em Decisões depois de aprovada. Janelas A (tese: direção do cenário ruim, caminho próprio fora do modelo), B (dez canais), C (saídas e entradas) e D (lista) enviadas ao principal. Decidido pelo B: prefixo das entradas ME; crédito já como consulta ao agente de crédito. O que muda nos sete na B3 está anotado no relatório do subagente (atividade 2.4/2.8/Q3/E1, PM 2.4/S10, inflação 2.4, expectativas XS9, fiscal, SISTEMA V.II.v, V.III.iv, V.IV.i). Custo real: subagente ~310 mil tokens. Subagente Opus do mapa de crédito lançado em seguida.
- 2026-10-30 — **mapa do MT aprovado** e ajustado às respostas (canal de juros e crédito retirado, nove canais; MT-PM1 e MT-CR2 saíram, MT-CR1 estreitada; lista com 19 tabelas), `vault.py map` PASS. Decisões e lista gravadas; pedido ao principal de levar a lista ao SISTEMA (V.VIII) e avisar o D. O subagente do crédito foi avisado da retirada, para o espelho.
- 2026-10-30 — **mapa de crédito rascunhado**: `obsidian/credit/credit_conceptual_map.md` (510 linhas, dez canais, saídas CR, entradas CE), `vault.py map credit` PASS; lista com 28 tabelas (14 endógenas, 14 de consulta) no scratchpad. Janelas B (canais), C (trocas) e D (lista: as três tabelas novas; as consultas) enviadas ao principal; tese provisória com as duas candidatas, caudas pelo III.III.i e projeção própria por analogia ao MT. Custo real: subagente ~360 mil tokens. Achados do subagente: o rótulo da PTC em `politica_monetaria.py` diz −1 a 1, a escala é −2 a +2; o empurrão parafiscal arrisca ser contado duas vezes (fiscal 2.2 e crédito 2.7); frases "crédito não tem agente" em PM, atividade, fiscal, câmbio e expectativas (B3).
- 2026-10-30 — **plano do B2 do MT enviado ao principal, aguardando liberação**: Sonnet faz `dados/mercado_trabalho.py` + `tests/test_dados_mercado_trabalho.py`; Opus faz `.claude/agents/mercado-trabalho-analyst.md`; ~0,6–0,9M. Bloqueios: o V.VIII do SISTEMA está em itens numerados, que o `motor.ler_lista` não lê (precisa "- `tabela` (recorte): papel"); corrigido, ele cai dentro da faixa do `expectativas.SECAO` (que vai até "*Fim das listas por agente.*"), e o fim da seção de expectativas tem de passar a "## (V.VIII)" no mesmo momento. E o registro do MT no `AGENTES` do `__main__` (E) é preciso para rodar o gerador.
- 2026-10-30 — **mapa de crédito aprovado** (as quatro recomendadas; ver Decisões); status do mapa atualizado, `vault.py map credit` PASS. Texto do V.IX no formato do leitor enviado ao principal (conferido com as expressões do `motor.ler_lista`: 8 grupos, 29 itens). O principal corrigiu o V.VIII (formato do leitor) e o fim da seção de expectativas (`## (V.VIII)`); `test_dados_agentes.py` passa.
- 2026-10-30 — **B2 do MT lançado** (liberado pelo principal): Sonnet faz `dados/mercado_trabalho.py` + `tests/test_dados_mercado_trabalho.py`; Opus faz `.claude/agents/mercado-trabalho-analyst.md`. Plano do B2 do crédito (~0,7–1,0M) enviado ao principal, a lançar quando o do MT voltar. Pendente com o E: registro do MT (e depois do crédito) no `AGENTES`.
- 2026-10-30 — o V.IX entrou no SISTEMA (29 itens; `test_dados_agentes.py` passa). B2 do crédito liberado pelo principal, a lançar quando o B2 do MT voltar; o registro do crédito no `AGENTES` vai ao E pelo principal quando o módulo existir.
- 2026-10-30 — o E já registrou o MT no retrato, no tracker e numa coluna nova (em branco) da aba Exógenas. Faltam as duas linhas da lista de agentes (`dados/__main__.AGENTES` e `consolidacao.AGENTES`), que dependem do módulo e da definição. Combinado com o principal: quando o B2 do MT entregar, o B avisa o chat E direto (SendMessage "Chat E") e registra aqui; se o gerador precisar rodar antes da definição, pede só a linha dos dados. O mesmo para o crédito.
- 2026-10-30 — **módulo de dados do MT pronto** (Sonnet, ~235 mil tokens): `analytics/agent_system/dados/mercado_trabalho.py` e `tests/test_dados_mercado_trabalho.py` (64 checks, inclusive a geração real do F do ciclo 2026-10-27 em pasta temporária; três mutantes). `test_dados_agentes.py` continua passando. As quatro `mt_*` da PM vêm por `de(pm, ...)` com séries a mais (mesma consulta e mesmo arquivo de A); as três novas são declaradas aqui; consultas por `de` ao dono. Duas leituras derivadas no F: a variação da desocupação aberta em ocupação e força de trabalho, e o saldo do CAGED de 12 meses por setor contra os 12 anteriores. Rótulo da PTC corrigido no módulo (−2 a +2). O B fixou o fim da seção em `## (V.IX)` (o subagente escolhia na importação). Pedida ao E a linha de `dados/__main__.AGENTES`, com o aviso da Focus de desocupação: herdada da atividade com `variante="atividade"`, ela faria dois agentes dividirem um arquivo; a solução limpa é expectativas ser dona do recorte (módulos dos sete: E agora ou B na B3).
- 2026-10-30 — **B2 do crédito lançado** (liberado pelo principal): Sonnet faz `dados/credito.py` + `tests/test_dados_credito.py` (no molde do módulo do MT, com o aviso da variante); Opus faz `.claude/agents/credito-analyst.md`. A definição do MT ainda está rodando.
- 2026-10-30 — **definição do MT pronta** (Opus, ~270 mil tokens): `.claude/agents/mercado-trabalho-analyst.md` (548 linhas), passa nas dez checagens de forma de `test_definicoes_agentes.py` aplicadas à parte (o teste só a pega depois do registro). Avisado o chat E direto (as duas linhas de `AGENTES`); janela de aprovação da definição enviada ao principal. A lista do que muda nas definições dos sete por causa do MT está pronta para a B3 (scratchpad `b3_mudancas_mt.md`). Custo real do B2 do MT: ~505 mil tokens (estimado 0,6–0,9M).
- 2026-10-30 — **definição do crédito pronta** (Opus, ~270 mil tokens + a correção de literatura): `.claude/agents/credito-analyst.md` (648 linhas), checagens de forma 10/10. Janela enviada ao principal: F1 (a variável da tese até o modelo decidir: impulso recomendado, concessões reais, ou as duas) e F2 (aprovar o modo de trabalho). A lista da B3 por causa do crédito está no fim deste arquivo. Módulo de dados do crédito ainda rodando.
- 2026-10-30 — F1 "Impulso de crédito" e F2 "Aprovar" gravados em Decisões; o mapa de crédito registra a escolha na Parte 1 (`vault.py map credit` PASS). **O E registrou o MT** em `dados/__main__.AGENTES` e `consolidacao.AGENTES` (B4 do MT, ~70 mil tokens do E); `test_dados_agentes`, `test_dados_mercado_trabalho`, `test_consolidacao`, `test_definicoes_agentes` (agora oito) e `test_conhecimento` passam. A Focus de desocupação dividida entre atividade e MT ficou como exceção explícita (`DIVIDIDAS`) no `test_dados_agentes.py`, a sair na B3 (pede o recorte "desocupação" na lista V.VII, do principal, e expectativas como dona). **Gerador do MT rodado de ponta a ponta** (`dados.__main__.gerar("mercado_trabalho", 2026-10-30)` numa pasta temporária, extração e F reais, só os retratos do modelo e do conhecimento em stub para não gravar no vault): 19 tabelas extraídas, F de 457 linhas, nenhuma "Sem dado no corte", as duas leituras combinadas presentes. Script: scratchpad `gerar_mt_tmp.py`.
- 2026-10-30 — **módulo de dados do crédito pronto** (Sonnet, ~263 mil tokens): `analytics/agent_system/dados/credito.py` e `tests/test_dados_credito.py` (127 checks, F real do ciclo 2026-10-27 sem "Sem dado no corte"; cinco leituras combinadas: impulso pelo saldo, impulso pelo fluxo com o aviso de série parada, concessões reais, contribuição de livre/direcionado × PF/PJ ao crescimento do saldo, surpresa da PTC). `test_dados_agentes` e `test_dados_mercado_trabalho` continuam passando. Registro pedido ao E. **Custo real do B2:** MT ~505 mil, crédito ~540 mil.
- 2026-10-30 — o principal segurou a B3: o usuário avalia tirar o agente de expectativas. Lista da B3 montada nos dois cenários (fim deste arquivo) e enviada ao principal. Nada escrito nos arquivos dos sete.
- **Custo estimado do B1:** ~2–3M (cada subagente Opus lê os sete mapas e o SISTEMA, ~0,6–1M por mapa; as janelas e a conferência nesta sessão, ~0,5M). Estimativa, não medida.

## Decisões

- **2026-10-30 — Janela 1, fronteiras** (o usuário escolheu as quatro recomendadas, pelo principal):
    - **1a. Trabalho × atividade — "Tabelas + folga".** O mercado de trabalho passa a ser dono de `mt_pnad`, `mt_desocupacao_retro`, `mt_caged` e `mt_caged_setor`, que saem da atividade. O hiato continua com a atividade. A folga do trabalho (desocupação contra a NAIRU, salário contra produtividade) é saída do MT para atividade, inflação e PM. O mercado de trabalho dos EUA (`mt_jolts`, `mt_ces`, `mt_cps`) fica com o externo.
    - **1b. Crédito × PM — "Crédito: condições; PM: postura".** O crédito conclui sobre as condições de crédito e quanto a Selic chega a elas. A PM conclui sobre a postura, lendo a condição de crédito que o crédito entrega.
    - **1c. Crédito × fiscal — "Fiscal decide, crédito mede".** A decisão de governo e o tamanho do estímulo parafiscal (`fisc_dlsp_fatores`, canal 2.5 do fiscal) ficam com o fiscal. O crédito mede quanto o direcionado e os bancos públicos crescem.
    - **1d. Crédito × atividade — "Crédito é dono" do impulso.** O impulso de crédito (`cred_fluxo_financeiro`) passa ao crédito. A atividade conclui o efeito dele sobre o hiato.
- **2026-10-30 — Janela 2, perguntas centrais** (pelo principal; resposta literal do usuário entre aspas):
    - **Mercado de trabalho** — *"As quatro que voce falou, mas eu quero um analisa da dinamica entre os setores (mais sensiveis ao ciclo economico) e coisas do tipo".* A dinâmica setorial vira pergunta própria (decisão do B: como parte da T2 ela seria o primeiro corte quando o report apertar, e o pedido foi explícito). Ficam cinco:
        - **T1.** Quanta folga há no mercado de trabalho (desocupação contra a NAIRU, e as outras medidas de ociosidade).
        - **T2.** O que move emprego e renda agora (ocupação, formal × informal, rendimento real, massa salarial).
        - **T3.** Que setores lideram e quais viram primeiro: a dinâmica entre os setores mais sensíveis ao ciclo (CAGED e PNAD por setor) e o que a composição diz sobre a fase do ciclo; inclui cortes do tipo formal × informal e por região quando dizem algo do ciclo.
        - **T4.** Os salários crescem acima da produtividade, e o que isso pede da inflação de serviços.
        - **T5.** O cenário nos seis trimestres.
    - **Crédito** — *"A cincos recomendadas, mas eu tambem quero uma quebra analitica dos subcomponentes do saldo total."* A decomposição vira pergunta própria (pelo mesmo motivo; e ela responde outra coisa que a C1: a C1 é o sinal, a C2 é de onde ele vem). Ficam seis:
        - **C1.** O crédito está apertando ou afrouxando, e por oferta ou por demanda.
        - **C2.** De que é feito o saldo e quem puxa o crescimento: livre × direcionado, PF × PJ, modalidades, e o que cada corte diz (mercado contra política, consumo contra investimento e capital de giro).
        - **C3.** A Selic está chegando ao crédito, e com que defasagem.
        - **C4.** O impulso de crédito e de onde ele vem.
        - **C5.** Endividamento, comprometimento de renda e inadimplência como limite.
        - **C6.** O cenário nos seis trimestres.

- **2026-10-30 — Mapa do mercado de trabalho, Partes 1–4 e lista de dados** (pelo principal; `obsidian/labor_market/labor_market_conceptual_map.md`, `vault.py map` PASS):
    - **Tese (A1).** Caudas upside e downside só como posição, como já decide o SISTEMA III.III.i (o principal não levou ao usuário). Upside = desocupação acima da faixa base (mais folga); o texto diz quando é bom ou ruim.
    - **Tese (A2) — "Sim, projeção própria".** Se a desocupação não entrar no Modelo Estrutural, o agente escreve mesmo assim o caminho dela por trimestre, com faixa e caudas, fora do modelo e do P, e é cobrado no placar. A variável continua "provisória, decide com o modelo".
    - **Esqueleto (B1), literal:** *"Aprovo, só tem duvida quanto ao juros e credito. Acredito que o desemprego é função do PIB (3). Opto por tirar a idea do juros e do credito, a não ser que voce tenha algum estudo ou literatura nesse sentido. Veja, não é que o juros e credito não afetar o desemprego, é que ele passa primero pelo crescimento."* Aplicado: o canal "juros e crédito chegam ao emprego" saiu; o 2.3 (emprego contra PIB) diz que juro e crédito chegam ao emprego pelo crescimento; a evidência no nível da firma (pequenas empresas cujo banco cortou crédito demitiram mais, crise de 2008–09) virou uma nota no canal setorial 2.6, como efeito de composição. O antigo 2.10 (política e instituições) virou 2.9. Ficam nove canais.
    - **Trocas (C1) — "Aprovar".** Ajustes que a saída do canal 9 obrigou (o principal pediu; aplicados pelo B): sai a MT-PM1 (caminho da Selic; a antiga MT-PM2, leitura do Copom sobre o trabalho, vira MT-PM1); sai a MT-CR2 (crédito às famílias); a MT-CR1 fica estreitada à oferta de crédito a pequenas e médias empresas, para a nota do 2.6. A ME-CR1 (o crédito pede emprego formal e renda ao MT) fica.
    - **Lista (D1) — "As três":** entram a PNAD trimestral, o CAGED por estado e o CAGED por faixa salarial. **D2** (as tabelas de consulta) foi aprovada com o C1 ("trocas e consultas: Aprovar"); pela decisão do B1 saem quatro consultas que só serviam ao canal retirado: `pm_copom_reuniao`, `cred_modalidade_livre_pj`, `cred_modalidade_livre_pf`, `cred_credito_familias`. Ficam 19 tabelas. A lista, para o principal levar ao SISTEMA como V.VIII:

        ###### (V.VIII) Agente de mercado de trabalho — aprovada em 2026-10-30
        *Aprovada pelo usuário em 2026-10-30 (`coordenacao/B_novos_agentes.md`, Decisões), a partir da proposta do mapa (`obsidian/labor_market/labor_market_conceptual_map.md`, Partes 1–4). Fronteiras decididas pelo usuário em 2026-10-30 (III.III.ix): as quatro `mt_*` saem da atividade; o hiato fica com a atividade; o trabalho dos EUA fica com o externo; o crédito é do agente de crédito, que ainda não existe. Os números entre parênteses ao fim de cada item são os canais do mapa. Nenhuma tabela TWA nem exógena.*

        ##### i. Endógeno
            1. `mt_pnad`: PNAD Contínua mensal (trimestre móvel), Brasil: desocupação, participação, nível de ocupação, subutilização (composta, por horas, força potencial, desalentados), informalidade, ocupação e rendimento por posição (com e sem carteira, conta própria com e sem CNPJ, setor público) e por atividade, rendimento habitual e efetivo, massa real. É a base da folga (T1), do emprego e da renda (T2) e do corte setorial (T3) (2.1, 2.2, 2.4, 2.5, 2.6). Sai da atividade.

            2. `mt_desocupacao_retro`: desocupação dessazonalizada (MM3M) do BC, retropolada desde 2004, do anexo do RPM. É a série que o modelo agregado do BC usa e a candidata da variável da tese na alternativa (a); anda só a cada RPM (2.1, tese). Sai da atividade.

            3. `mt_caged`: estoque de emprego formal celetista do BC, total e 13 setores, desde 1992. O sinal mensal do ciclo e a série longa para medir com um G quais setores viram primeiro; o BC reancora o nível para trás e o último mês pode ser provisório (coluna `fonte`) (2.3, 2.4, 2.6). Sai da atividade.

            4. `mt_caged_setor`: admissões, desligamentos e saldo do Novo CAGED por seção CNAE (22), desde 2020. Admissões contra desligamentos por setor é a leitura da fase do ciclo (T3) (2.6). Sai da atividade.

            5. `mt_pnad_trimestral` (aprovada pelo usuário, 30/10): PNAD trimestral, Brasil: horas habituais e efetivas por posição, rendimento por grupo de ocupação e por atividade, desocupação e subutilização por idade, instrução, sexo e cor. É a única série de horas trabalhadas, sem a qual não há produtividade por hora (T4, 2.7); a desocupação dos jovens é o corte mais cíclico (2.2, 2.6). Trimestral e com um trimestre a mais de atraso que a mensal.

            6. `mt_caged_uf` (aprovada pelo usuário, 30/10; leitura enxuta): saldo, admissões e desligamentos do Novo CAGED por UF, desde 2020. É o único corte regional do banco (não há PNAD por UF): diz se uma desaceleração está concentrada em estados agrícolas ou industriais (T3, 2.6).

            7. `mt_caged_salario` (aprovada pelo usuário, 30/10; leitura enxuta): admissões, desligamentos e saldo do Novo CAGED por faixa de salário em múltiplos do salário mínimo, desde 2020. Mostra se a contratação está na base da distribuição, onde o salário mínimo morde (T4, 2.6, 2.9). Não traz salário médio; as faixas saltam a cada janeiro com o reajuste do mínimo.

        ##### ii. Endógeno de atividade (consulta; a posição vem pelas saídas MT-AT1–MT-AT2)
            8. `pm_hiato_produto`: hiato do produto do BC na edição corrente do RPM. A outra leitura da mesma folga: hiato e desocupação que discordam dizem que uma das duas está errada (T1, 2.1, 2.3, 2.8).

            9. `atv_pib`: PIB trimestral em volume, com o valor adicionado por setor (agropecuária, indústria de transformação, construção, comércio, transporte, serviços de informação, financeiros, administração pública…). Numerador da produtividade, total e por setor, contra a ocupação da PNAD (T4, 2.7) e o produto de cada setor contra o emprego dele (T3, 2.6).

            10. `atv_pib_taxas`: crescimento oficial do PIB. A regra de Okun e o crescimento da produtividade (2.3, 2.7).

            11. `atv_ibcbr`: IBC-Br, total e por setor. O ciclo mensal contra o emprego mensal (2.3, 2.6).

            12. `atv_pim`: produção industrial por seção. A produção da indústria contra o emprego na indústria (2.6).

            13. `atv_pmc`: volume do varejo por segmento. O comércio, setor sensível ao crédito, contra o emprego no comércio (2.6).

            14. `atv_pms`: volume de serviços por segmento. O maior empregador, contra o emprego em serviços (2.6, 2.8).

        ##### iii. Endógeno de inflação (consulta; MT-IN1–MT-IN2)
            15. `inflc_agregados`: IPCA, serviços e serviços subjacentes. Deflator do rendimento e da massa (2.5) e o lado dos preços da T4: se a pressão salarial aparece em serviços (2.7, 2.8).

        ##### iv. Endógeno de expectativas (consulta; MT-EP1)
            16. `expc_focus_periodo` (desocupação): mediana da Focus para a taxa de desocupação, anual e trimestral. O consenso, para separar surpresa de convergência (T5, 2.1).

            17. `expc_qpc`: Questionário Pré-Copom, blocos NAIRU e hiato. A NAIRU do mercado é a referência da T1, já que o banco não tem NAIRU (2.1).

        ##### v. Endógeno de fiscal (consulta; MT-FS1–MT-FS2)
            18. `fisc_rtn`: resultado do governo central por rubrica. Bolsa Família, BPC, seguro-desemprego, abono e pessoal: transferências que mudam renda e participação fora do mercado de trabalho, e a folha pública (2.2, 2.9).

        ##### vi. Endógeno de crédito (consulta; MT-CR1; o agente de crédito ainda não existe, e até lá o agente declara as premissas)
            19. `cred_ptc`: oferta e demanda de crédito na leitura dos bancos, por segmento (inclusive micro, pequenas e médias). A oferta às pequenas empresas: quando ela trava, as demissões caem primeiro nos setores de muitas pequenas empresas, comércio e serviços (nota do 2.6; juro e crédito chegam ao emprego agregado pelo crescimento, 2.3, decisão do usuário 30/10).

        *Fora da lista (consulta livre, sem uso previsto): `pm_hiato_produto_vintages` e `atv_pib_valores_correntes` (do placar e da composição da atividade), `atv_pim_uso`, `atv_renda_poupanca`, os outros cortes de crédito, `pm_copom_reuniao`, `br_interest_rate` (juro e crédito chegam ao emprego pelo crescimento, que vem da atividade; decisão do usuário, 30/10). `mt_jolts`, `mt_ces`, `mt_cps` e `mt_produtividade` (EUA) ficam com o externo.*

        *Não está no banco (lacunas do tracker, aba Quant - Labor Market, mais as achadas no mapa): NAIRU calculada; salário mínimo; vagas (curva de Beveridge); PNAD por UF; produtividade e custo unitário do trabalho (viram G sobre `atv_pib` e a PNAD); INPC (o índice do reajuste do mínimo); taxa de sindicalização. O agente declara a lacuna, nunca escreve o valor de memória. A linha do tracker que diz que `mt_pnad` só cobre 2024 em diante está velha: a tabela vai de 2012-03 a 2026-09.*

- **2026-10-30 — Mapa de crédito, Partes 1–4 e lista de dados** (pelo principal; o usuário aprovou as quatro recomendadas; `obsidian/credit/credit_conceptual_map.md`, `vault.py map credit` PASS):
    - **Esqueleto (B1):** os dez canais, inclusive o argumento sobre a transmissão (tempero do tipo (i) sobre o peso do aperto na curva IS, levado à atividade, dona da equação) e o aviso de não contar duas vezes o empurrão parafiscal.
    - **Trocas (C1):** saídas CR (à PM, atividade, fiscal, mercado de trabalho, inflação, expectativas, câmbio) e entradas CE (da PM, atividade, fiscal, mercado de trabalho); o externo sem linha fixa.
    - **Lista (D1, D2):** entram as três tabelas novas (porte, setor da empresa e tipo de cliente, as duas últimas com leitura enxuta) e as 14 consultas. Ficam 28 tabelas; a Focus entra em dois recortes (Selic e IPCA).
    - **Ficam, aplicadas pelo B sem perguntar:** caudas só como posição (SISTEMA III.III.i) e projeção própria fora do modelo (pela resposta do MT). A variável da tese (impulso de crédito ou crescimento real das concessões) espera as decisões do Modelo Estrutural.
    - A lista, para o principal levar ao SISTEMA como V.IX, já no formato do leitor (`motor.ler_lista` conferido: 8 grupos, 29 itens):

        ###### (V.IX) Agente de crédito
        *Aprovada pelo usuário em 2026-10-30 (`coordenacao/B_novos_agentes.md`, Decisões), a partir da proposta do mapa (`obsidian/credit/credit_conceptual_map.md`, Partes 1–4). Fronteiras decididas pelo usuário em 2026-10-30 (III.III.ix): o crédito fica com todas as `cred_*` (as 11 que eram TWA na PM, na atividade e no fiscal, mais porte, atividade econômica e tipo de cliente); conclui sobre as condições e quanto da Selic chega a elas (a PM, sobre a postura); mede o direcionado e os bancos públicos (o fiscal decide o parafiscal); é dono do impulso de crédito (a atividade conclui o efeito no hiato); consulta o mercado de trabalho sem concluir. Os números entre parênteses ao fim de cada item são os canais do mapa. Nenhuma tabela TWA nem exógena.*

        ##### i. Endógeno
            - `cred_credito_resumo`: saldo, concessões (com e sem ajuste sazonal), taxa de juros, spread, ICC, inadimplência e % do PIB, por recurso (total, livre, direcionado) × segmento (total, PF, PJ), mais o corte não rotativo; 84 séries, a maioria desde 2011-03, até 2026-09. É a tabela central: condições (preço contra quantidade, 2.1), a decomposição livre × direcionado e PF × PJ (2.2), o repasse (2.5), a fatia que a Selic não alcança (2.6), o impulso pelo estoque (2.7), a inadimplência (2.9) e a candidata (b) da tese (concessões reais). Sai de TWA na PM, na atividade e no fiscal.

            - `cred_modalidade_livre_pf`: crédito livre à PF por modalidade (consignado por origem, pessoal não consignado, veículos, cartão à vista, parcelado e rotativo, cheque especial, composição de dívidas), saldo, concessão, taxa e inadimplência, desde 1994 (saldo) e 2011 (demais), até 2026-09. O que o crédito às famílias financia e onde aparece o aperto (rotativo e cheque especial como sinal de estresse) (2.3, 2.5, 2.8, 2.9). Sai de TWA na PM e na atividade.

            - `cred_modalidade_livre_pj`: crédito livre à PJ por modalidade (capital de giro por prazo, desconto de duplicatas e recebíveis, conta garantida, ACC, financiamento de exportação e importação, cartão, cheque especial), mesmas métricas e cobertura. Capital de giro e comércio exterior: produção, liquidez das empresas e a parte do saldo atrelada ao dólar (2.3, 2.5, 2.9). Sai de TWA na PM e na atividade.

            - `cred_modalidade_direcionado_pf`: direcionado à PF (imobiliário e rural, a taxas de mercado e reguladas; BNDES; microcrédito), mesmas métricas, desde 2007-03. A metade da política no lado das famílias (2.2, 2.6). Sai de TWA na PM e no fiscal.

            - `cred_modalidade_direcionado_pj`: direcionado à PJ (BNDES por finalidade — capital de giro, investimento, agroindustrial —, rural e imobiliário a taxas de mercado e reguladas, programas para MPME), mesmas métricas, desde 2007-03. O financiamento do investimento e o parafiscal medido pelo lado do empréstimo (2.2, 2.3, 2.6). Sai de TWA na PM, na atividade e no fiscal.

            - `cred_credito_controle_capital`: saldo, inadimplência e provisões por controle do banco (públicos, privados nacionais, estrangeiros), desde 1988. Mercado contra política pelo lado de quem empresta; a série longa para medir com um G se os bancos públicos emprestam contra o ciclo (2.2, 2.6, 2.9). Sai de TWA na PM e no fiscal; as provisões, que nenhuma lista usava, entram.

            - `cred_credito_porte`: saldo, inadimplência e saldo de maior risco das empresas por porte (MPME e grandes), desde 2012. A pequena empresa sente o aperto de oferta primeiro e não tem o mercado de capitais como saída; responde à MT-CR1 do mercado de trabalho. Quebra metodológica no saldo de maior risco (até 2024-12 e desde 2025-01, sem sobreposição) (2.3, 2.7, 2.9).

            - `cred_credito_atividade_economica`: saldo das empresas por atividade (agropecuária, ~17 subsetores da indústria, ~15 de serviços), 38 séries, desde 2012. Que setores tomam crédito e a decomposição do impulso por atividade (2.3, 2.7). Leitura enxuta.

            - `cred_credito_tipo_cliente`: saldo por tipo de cliente (setor privado PF e PJ, setor público federal e estadual-municipal), desde 1988. A fatia do saldo bancário que não é família nem empresa, crédito a governos subnacionais incluído (2.3). Leitura enxuta.

            - `cred_credito_amplo`: crédito ao setor não financeiro (governo, empresas, famílias) por instrumento: SFN, outras instituições, fundos públicos, títulos domésticos e securitização, dívida externa nos mercados interno e externo; 17 séries desde 2013. Separa substituição (empresa grande indo ao mercado) de aperto, e traz a dívida externa que anda com o câmbio (2.4). Universo diferente do crédito do SFN: não reconcilia. Sai de TWA na PM e na atividade.

            - `cred_ptc`: Pesquisa Trimestral de Condições de Crédito, oferta e demanda observadas e esperadas, em grandes empresas, MPME, PF consumo e PF habitacional, desde 2011-T2, até 2026-04 (trimestral). A leitura dos próprios bancos de oferta contra demanda e a surpresa contra o que eles esperavam (2.1). Escala de −2 a +2 (média não ponderada das respostas); painéis pequenos e de tamanhos diferentes. Sai de TWA na PM e na atividade.

            - `cred_fluxo_financeiro`: fluxo financeiro do crédito bancário (concessões − pagamentos), acumulado em 12 meses, % do PIB, total, PF e PJ, do anexo do RPM (não é SGS), desde 2015-01. É a fonte do impulso no conceito do BC, `fluxo(t) − fluxo(t−12)`, e a candidata (a) da tese (2.7). **Parada em 2026-04**: o RPM de set/2026 saiu sem o gráfico, e a carga recarrega a última edição que o publicou (jun/2026); conferir a data a cada ciclo e, enquanto parada, usar o impulso pelo estoque (item 1) e dizer isso. Sai de TWA na PM e na atividade.

            - `cred_credito_familias`: endividamento das famílias (sobre a renda de 12 meses, com e sem imobiliário) e comprometimento de renda (serviço total, sem imobiliário, só juros), desde 2005, até 2026-08 (um mês atrás das outras). O limite das famílias (C5, 2.8). Sai de TWA na PM e na atividade.

            - `cred_inadimplencia_pj`: inadimplência das empresas acima de 90 dias, atraso de 15 a 90 dias, taxa de juros e concessões PJ, com a Selic ao lado, desde 2011 (Selic desde 1986). O ciclo de inadimplência das empresas e o candidato a sinal antecedente, a medir com um G (2.5, 2.9). A Selic que vem nesta tabela é variável da PM: só leitura. Sai de TWA na PM.

        ##### ii. Endógeno de política monetária (consulta; a posição vem pelas saídas CR-PM1–CR-PM2)
            - `pm_copom_reuniao`: Selic decidida por reunião. O referencial do repasse ao crédito pós-fixado e do custo do estoque (2.5, 2.8).

            - `br_interest_rate`: curva DI (pré) nos vértices de 1 e 2 anos e a Selic. O custo de captação contra o qual o crédito prefixado é precificado: o repasse se lê contra a curva no prazo do empréstimo, não só contra a Selic (2.1, 2.5).

        ##### iii. Endógeno de atividade (consulta; CR-AT1–CR-AT2)
            - `pm_hiato_produto`: hiato do BC na edição corrente do RPM. A demanda por crédito e a inadimplência seguem o ciclo (2.7, 2.9).

            - `atv_pib_mensal`: PIB nominal mensal e de 12 meses. Denominador do impulso pelo estoque e de todo % do PIB; o impulso só vai até onde ele vai (2.7).

            - `atv_pib`: PIB trimestral, consumo das famílias e FBCF. O que o crédito financia, para conferir a composição (C2) e se o impulso chega ao gasto (2.3, 2.7).

            - `atv_pmc`: volume do varejo, veículos e móveis e eletrodomésticos. O consumo financiado a crédito (2.3).

            - `atv_pim_uso`: produção industrial por categoria de uso, duráveis e bens de capital. Os bens que o crédito às famílias e o crédito ao investimento financiam (2.3).

        ##### iv. Endógeno de inflação (consulta; CR-IN1)
            - `inflc_agregados`: IPCA. Deflator das concessões e do saldo (tese (b)) e do juro real do crédito (2.1, 2.5, 2.8).

        ##### v. Endógeno de mercado de trabalho (consulta; CR-MT1)
            - `mt_pnad`: ocupação, informalidade, rendimento real habitual e massa salarial real. A renda que sustenta o serviço da dívida e o consignado (2.8, 2.9).

            - `mt_caged`: estoque de emprego formal. O emprego formal, ao qual o consignado privado está atado, e o sinal mensal da inadimplência das famílias (2.8, 2.9).

        ##### vi. Endógeno de fiscal (consulta; CR-FS1–CR-FS2)
            - `fisc_dlsp_fatores`: créditos do Tesouro às instituições financeiras oficiais (BNDES e outras). A decisão parafiscal, do fiscal, contra a qual o crescimento do direcionado é lido (2.2, 2.6).

            - `fisc_rtn`: só as equalizações e subsídios ao crédito (custeio e investimento rural, Pronaf, Proex, fundos regionais, FIES, habitação de interesse social). O custo fiscal dos programas de crédito direcionado (2.6). Leitura enxuta.

        ##### vii. Endógeno de expectativas (consulta; CR-EP1)
            - `expc_focus_periodo` (Selic): mediana da Focus para a Selic por ano. O juro esperado que precifica o crédito prefixado (2.5).

            - `expc_focus_periodo` (IPCA): mediana da Focus para o IPCA por ano. O juro real ex-ante do crédito (2.5).

        ##### viii. Endógeno de câmbio (consulta; CR-CB1)
            - `cmb_ptax`: câmbio diário. Reavalia em reais o crédito atrelado ao dólar (ACC, repasse externo) e a dívida externa das empresas, o que o impulso pelo estoque conta como crédito (2.3, 2.4, 2.7).

        *Fora da lista (consulta livre, sem uso previsto): `br_di_grade` (a curva completa; os vértices de 1 e 2 anos bastam), `pm_copom_projecoes`, `expc_qpc` (não pergunta de crédito), `atv_ibcbr`, `atv_pms`, `mt_caged_setor`, `fisc_nfsp`, `cmb_risco_pais`, as tabelas do externo (as condições globais chegam ao crédito pela curva, pelo câmbio e pela dívida externa da `cred_credito_amplo`).*

        *Não está no banco (lacunas; não há aba de crédito no tracker): o impulso de crédito publicado como série (o BC o publicou em boxe duas vezes); o fluxo financeiro desde set/2026; a decomposição do spread (custo de captação, inadimplência esperada, compulsório e impostos, margem), que o BC publica no Relatório de Economia Bancária; o Relatório de Estabilidade Financeira (capital e testes de estresse dos bancos); as regras e os tetos (consignado, rotativo), os programas e o compulsório, com datas; o saldo de crédito por vintage de concessão; a captação da poupança. O agente declara a lacuna, nunca escreve o valor de memória.*

- **2026-10-30 — Definição do mercado de trabalho** (pelo principal), literal: *"Eu projeção de taxa de desemprego e de CAGED. E a ideia dele é dar mais insumos para a atividade e para o hiato."* Aplicado:
    - **Tese com duas variáveis**, as duas projeção própria com central, faixa e caudas, fora do modelo: a desocupação dessazonalizada no fechamento do trimestre, e o **CAGED**, medido como o **saldo do Novo CAGED em 12 meses no fechamento do trimestre** (mil empregos; igual à variação anual do estoque formal). Escolha do B: 12 meses e não o saldo do trimestre, porque o saldo mensal tem sazonalidade forte (dezembro negativo); a soma de 12 meses dispensa ajuste, é a forma em que o CAGED é citado e a que a atividade compara com o PIB. Placar: a primeira divulgação do último mês do trimestre (revisões por declaração fora do prazo não repontuam). No JSON, chaves `desocupacao` e `caged_12m`.
    - **Papel:** o agente existe para ser insumo da atividade e do hiato; o que ele diz à atividade (ME-AT1, ME-AT2: folga, os dois caminhos, emprego por setor, onde a leitura de desemprego põe o hiato contra o do BC) é o produto principal, à frente de inflação e PM.
    - **Literatura** (correção do principal): a camada 1 do D entra antes do ciclo 2, e a definição lê a literatura pelo retrato do conhecimento, como os outros; sai o "sem literatura no primeiro ciclo" (definição e mapa). A mesma correção foi passada ao subagente da definição do crédito.
    - Ajustados: a definição (introdução, o que lê, tese, placar, passo 1, JSON, seção 5) e o mapa (o que é o arquivo, o papel, a Parte 1, MT-AT1 e ME-AT1). Checagens de forma: tudo ok; `vault.py map labor_market` PASS.

- **2026-10-30 — Definição do crédito** (pelo principal): **F1 "Impulso de crédito"**: até o Modelo Estrutural decidir, a tese do crédito é o impulso de crédito no conceito do BC (fluxo(t) − fluxo(t−12), p.p. do PIB); os trimestres que o fluxo não cobre (parado em abr/26) saem pelo impulso medido no saldo, com o viés dito, e o placar usa a mesma conta sobre as primeiras divulgações. É o default `tese=impulso` da definição. **F2 "Aprovar"**: `.claude/agents/credito-analyst.md` aprovada.

## Pedidos

- **2026-10-30 — ao principal:** levar a lista do MT (acima) ao SISTEMA como V.VIII, e avisar o chat D que o mapa do mercado de trabalho está aprovado (Partes 1–4), para a Parte 5 e a camada 1 dele. Observação ao D: a fonte de camada 1 do canal 2.4 da atividade, Borges (2022), é paper de NAIRU e provavelmente passa ao MT (`owner.py`); e a aba "Quant - Labor Market" do tracker diz que `mt_pnad` só cobre 2024 em diante, mas a tabela vai de 2012-03 a 2026-09.

## Para a B3 (anotado no B1/B2; não aplicado)

### Por causa do mercado de trabalho

- Atividade: regra de dados, canais 2.4 e 2.8, Q3 — as mt_* viram endógeno de MT (consulta); E1 (espelho de PM S10) perde a parte de trabalho; novas linhas S-MT espelhando ME-AT1 e ME-AT2; a fonte de camada 1 Borges (2022) do canal 2.4 é paper de NAIRU e provavelmente vai para o MT (questão do D / owner.py).
- PM: regra de dados e 2.4 dizem "provisoriamente, o mercado de trabalho"; S10 se divide, com nova linha ao MT espelhando ME-PM1.
- Inflação: dados do 2.4 dizem "que a atividade tem provisoriamente"; nova linha ao MT espelhando ME-IN1, e linha de entrada para MT-IN1 e MT-IN2.
- Expectativas: a frase "o mercado de trabalho é lido pela atividade… pela XS9" muda; nova linha XE para MT-EP1; o corte de desocupação da Focus e o bloco NAIRU do QPC não estão na lista do EP.
- Fiscal: linhas FE para MT-FS1 e MT-FS2.
- Externo: sem mudança.
- SISTEMA V.II.v, V.III.iv, V.IV.i: os títulos de grupo das mt_* e os rótulos "provisório" (é do principal).
- Módulos de dados: politica_monetaria.py declara as mt_* hoje (~578–671); atividade.py (~249–300) e inflacao.py (~227–230) consultam com de(pm, ...); passam a consultar de mercado_trabalho.

#### Depois da aprovação (30/10)
- O canal 9 (juros e crédito) saiu: MT-PM1 agora é a leitura do Copom sobre o trabalho (a antiga MT-PM2); não há mais pedido do caminho da Selic. MT-CR2 saiu; MT-CR1 só oferta a pequenas e médias empresas.
- No mapa da PM: a nova linha de entrada espelha só a leitura do Copom (MT-PM1), e a saída ao MT espelha ME-PM1.
- Nos módulos: o MT consulta só cred_ptc do crédito; não consulta pm_copom_reuniao.

#### Definições dos sete (para o chat E), do relatório do subagente da definição do MT
- atividade-analyst.md: descrição (l.3) "provisionally, the labour market" e "labour market's slack"; tipos de dado (l.121–122) com as quatro mt_* como próprias → consulta ao MT (mais as três novas); Q3 (l.284) lê desocupação × NAIRU por conta própria → recebe do MT (ME-AT1); seção 5: perguntas ao MT e respostas a MT-AT1/AT2; listas "other six" (l.11, 75).
- inflacao-analyst.md l.143: "atividade — … provisionally, the labour market (IN-S5)" → MT; o tempero "salário além do hiato" vem do MT (ME-IN1); responde MT-IN1/IN2.
- politica-monetaria-analyst.md l.156: "provisionally, the labour market (S10)" → MT (ME-PM1); responde MT-PM1 (leitura do Copom).
- fiscal-analyst.md: responde MT-FS1 (mínimo, transferências) e MT-FS2 (contratação e salário públicos).
- expectativas-analyst.md: responde MT-EP1 (Focus de desocupação, NAIRU e hiato do QPC).
- externo-analyst.md: linha de fronteira (trabalho do Brasil é do MT; o dos EUA fica com ele).
- cambio-analyst.md: só a contagem de agentes.
- Todos: "seven agents" / "other six" / "when the seven maps are approved" (atividade l.11/75/354, inflação l.10/83, PM l.10, expectativas l.15/17/81–82, fiscal l.14/79–80, câmbio l.10, externo l.11/87–88/392).
- Fora dos sete: moderador e escrivão talvez precisem de uma linha sobre tese fora do modelo sem central no PF*.

### Por causa do crédito (do relatório do subagente do mapa e da definição, 30/10)
- Mapas: PM 2.10 (consulta ao crédito; PM conclui postura e eficácia pela leitura do crédito), 2.5 (direcionado vem do crédito), tirar "Credit has no agent yet" e a regra "TWA: credit only", linhas de saída espelhando CE-PM1/CE-PM2 e de entrada CR-PM1/CR-PM2; atividade 2.2 (consulta, impulso é do crédito), 2.4 e 2.6 (`cred_credito_familias`, `cred_credito_amplo`, BNDES vêm do crédito), saídas espelhando CE-AT1/CE-AT2, entradas CR-AT1/CR-AT2, nota da dupla contagem do parafiscal; fiscal 2.5 (consulta, armadilha muda), saída espelhando CE-FS1, entradas FE para CR-FS1/CR-FS2, nota no 2.2 sobre a medida parafiscal dele contra o impulso de crédito; inflação (entrada CR-IN1); expectativas (entrada CR-EP1; tirar "Credit has no agent", l.338); câmbio (entrada CR-CB1; tirar l.218); mapa do MT (entrada espelhando CR-MT1; a 3.6 deixa de ser "pending").
- SISTEMA (principal): V.II.vi, V.IV.viii e V.V.viii passam de "TWA — crédito" a "Endógeno de crédito (consulta)"; as linhas "fora da lista" de V.II.ix e V.IV ainda citam porte, atividade econômica e tipo de cliente.
- Módulos: `politica_monetaria.py`, `atividade.py` e `fiscal.py` passam as `cred_*` a `de(credito, ...)`; rótulo da PTC (−2 a +2) em PM e atividade; o MT passa `cred_ptc` a `de(credito, ...)`.
- Definições (para o E): PM — intro "seven agents", tipos de dado "TWA (credit) … assumida" → consulta ao crédito (CE-PM1, CE-PM2), tempero (ii) "directed credit" (a medida vem do crédito), listas de perguntas; atividade — "other six" → oito, "TWA (credit)" → consulta (CE-AT1, CE-AT2), tempero: o tipo (i) sobre `H.h2` pode vir do crédito e a atividade aplica, o tipo (ii) chega do crédito dizendo o tipo; fiscal — contagem, "TWA (credit)" → consulta (CE-FS1), tempero (ii) com o empurrão contado uma vez, seção 5 responde CR-FS1/CR-FS2, descrição "parafiscal credit"; câmbio, inflação e expectativas — contagem e responder CR-CB1, CR-IN1, CR-EP1; externo — contagem; `web.md` — "Seven analyst agents" → nove.
- Registro (E): `consolidacao.AGENTES["credito"]`, `dados/__main__.AGENTES`, `conhecimento.AREA["credito"] = "credit"`, coluna na aba Exógenas.

### Plano da B3, nos dois cenários (montado em 30/10; não aplicado)

**Decisão técnica do B (vale nos dois):** as declarações físicas das `mt_*` e `cred_*` ficam onde estão (`politica_monetaria.py`, `atividade.py`), e a posse é dada pela lista do SISTEMA, não por quem declara. Mover as declarações para `mercado_trabalho.py` e `credito.py` criaria import circular (os dois importam `politica_monetaria` e `atividade`, e estes passariam a importar os dois); a consulta já é idêntica nos dois lados e o `conferir_consultas` garante isso.

**Comum aos dois cenários — do B:**
- Mapas dos sete: as linhas e frases listadas acima ("Por causa do mercado de trabalho" e "Por causa do crédito"), e nos dois mapas novos as entradas espelhadas (MT: CR-MT1; crédito: as CE deixam de ser "proposed").
- Módulos dos sete: rótulo da PTC (−2 a +2) em `politica_monetaria.py` e `atividade.py`; comentários que dizem "TWA"/"provisoriamente" passam a "consulta ao crédito"/"ao mercado de trabalho".
**Comum — do E:** as definições dos sete (as duas listas acima); `web.md` (nove analistas); retirar a exceção `DIVIDIDAS` quando a Focus de desocupação tiver dono único.
**Comum — do principal:** SISTEMA V.II.v–vi, V.III.iv, V.IV.i, V.IV.viii, V.V.viii (títulos de grupo: TWA/provisório → endógeno de crédito/de mercado de trabalho, consulta) e as linhas "fora da lista" que citam porte, setor e tipo de cliente.

**Cenário 1 — expectativas continua:**
- Principal: o recorte "desocupação" (e "IPCA", hoje lido de `cambio`) na lista V.VII.
- B: `expectativas.py` declara a Focus de desocupação (e de IPCA) como dona, sem variante; `atividade.py` e `mercado_trabalho.py` (e `credito.py`, para IPCA) passam a `de(expectativas, ...)`. Mapa de expectativas: entradas MT-EP1 e CR-EP1.
- E: definição de expectativas responde MT-EP1 e CR-EP1; `DIVIDIDAS` vazio.

**Cenário 2 — expectativas sai** (Focus de IPCA, ancoragem e inflação implícita → PM; Focus de PIB e desocupação → atividade e MT; câmbio e Selic → câmbio e PM; QPC → PM):
- Principal: V.VIII ganha a Focus de desocupação como endógena do MT e passa o QPC a "endógeno de PM (consulta)"; V.IX passa a Focus de Selic e IPCA a "endógeno de PM (consulta)".
- B: mapa do MT — a Focus de desocupação vira dado próprio (canal 2.1 e T5, o consenso contra a projeção própria); MT-EP1 sai e a NAIRU e o hiato do QPC passam a um pedido à PM (MT-PM2); mapa de crédito — CR-EP1 sai e a Focus de Selic e IPCA vira pedido à PM (CR-PM3 ou dentro da CR-PM1). Módulos: a Focus de desocupação perde a variante (fica declarada em `atividade.py`, o MT consulta por `de(atividade, ...)`; sem variante não há arquivo dividido); `credito.py` lê Selic e IPCA da Focus de onde a PM declarar.
- E: definições do MT e do crédito (fontes da Focus e do QPC; tirar expectativas das listas de quem responde); `DIVIDIDAS` vazio; o resto da retirada de expectativas não é da B3.
