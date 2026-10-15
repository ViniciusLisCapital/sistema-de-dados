**Sobre este arquivo:** organização do sistema de agentes-analistas. Mantido pelo Claude a pedido do usuário: marca o que foi feito e acrescenta o que a conversa decidir. Uma decisão só entra aqui depois que o usuário a tomou. Detalhe técnico vai para o `CLAUDE.md` da pasta, não para cá. Os princípios gerais, que valem para todo agente, ficam no `PRINCIPIOS_AGENTES.md`.


# (I) O sistema

## (I.I) Objetivo
    - i. Relatório macroeconômico único: contexto atual e tese de cenário, construído a partir da opinião de agentes especialistas.
    - ii. Cada agente usa dados, referencial teórico (literatura) e prático (modelos mentais) e ferramentas.
    - iii. Relatório claro e sem verbosidade; teses falseáveis, com premissas, signposts e checkpoints ("se X continuar em Y, a tese muda").
    - iv. Nenhuma informação inverídica ou misleading: todo número rastreável até a fonte.

## (I.II) Agentes
    - i. Câmbio e política monetária primeiro. Testar bem os dois antes de acrescentar outro.
    - ii. Depois, um a um: inflação, fiscal, atividade, crédito, mercado de trabalho, externo.
    - iii. Os agentes rodam no Claude Code, sob demanda, nesta fase.
    - iv. O modelo quantitativo (Modelo Estrutural, FX Model) fica fora dos agentes por enquanto. Primeiro, azeitar o processo analítico e o fluxo de informação. Quando o Modelo Estrutural entrar, entra como saída dos agentes, não como ferramenta (I.III.xv).
    - v. Agente escrivão (2026-10-02): organiza o relatório final a partir dos reports finais (RF) e do cenário final (PF*). O objetivo é um relatório em ótimo português, de clareza e objetividade excepcionais. Garante a validade lógica e a coesão dos argumentos dos reports, e pode cobrar de um agente mais clareza numa explicação. Regras em IV.vii. Manual de escrita: `obsidian/escrivao/manual_do_escrivao.md` (feito 2026-10-07).
    - vi. Agente administrador (intenção do usuário, 2026-10-02): administra o sistema e cuida da manutenção dele. Primeira tarefa prevista: decidir quais funções G criadas pelos agentes são promovidas ao F (IV.iv). Detalhes a definir (IV.viii).

## (I.III) Regras decididas
    - i. Base de conhecimento: `repository/` guarda o bruto (raw_pdf, raw_md, cartas das gestoras, acompanhamento de aquisição). `obsidian/` é a única camada que os agentes leem.
    - ii. Pasta de cada área no vault: `clean_md/`, `synthesis/`, `concepts/`, `mental_models/` e o mapa conceitual.
    - iii. Modelos mentais por área × gestora (ex.: `verde_fx_mental_models.md`). São arcabouço, não opinião atual.
    - iv. A bibliografia consolidada é acompanhamento do que foi ingerido: fica no `repository/`.
    - v. Documentos do BC (comunicados, atas, RPM) são bibliografia do agente de política monetária, em `clean_md/central_bank/`.
    - vi. Mapa conceitual = contrato da área: (1) perguntas centrais, (2) esqueleto causal, (3) saídas, (4) entradas, (5) índice de conceitos.
        - Perguntas centrais (2026-10-02): o que o agente responde em todo report. São o mínimo, não o máximo: o agente não fica limitado a elas, e insights novos e alertas também entram. No câmbio: (a) quais as condições subjacentes do mercado de câmbio brasileiro; (b) como estão os fundamentos macroeconômicos para o câmbio; (c) o que explica a dinâmica recente do câmbio ("recente" é decisão do agente: como referência, 1 a 3 meses, considerando também o que aconteceu desde o último ciclo, sobretudo se faz mais de um mês, sem ficar restrito a isso; 2026-10-07); (d) qual o cenário prospectivo para o câmbio, via modelo estrutural.
        - Global × idiossincrático entra na explicação do modelo (FX Model ou Estrutural), dentro da pergunta (c). A discussão marginal × nível fica de fora por ora.
    - vii. Saída de A para B = o que é importante PARA A vindo de B. Entrada de A vinda de B = o que B disse que é importante para B vindo de A. Dá ênfase, não limita a análise.
    - viii. Entradas e saídas têm uma camada fixa (no mapa) e uma dinâmica (nos reports, conforme as teses do ciclo).
    - ix. Três tipos de dado (decidido 2026-10-01):
        - Endógeno: dado da área do próprio agente; ele é o responsável por analisá-lo.
        - Exógeno: dado sem agente, que todos os agentes podem consumir. Ex.: o CDS.
            - Intenção do usuário (2026-10-02): distribuir cada exógena a um ou dois agentes, que terão a palavra para discuti-la. Ex.: o CDS reflete risco fiscal e risk-off global, então os agentes fiscal e externo discutem o CDS.
        - TWA (temporarily without agent): dado de uma área que ainda não tem agente. Funciona como exógeno até o agente existir, quando vira endógeno dele. Ex.: inflação, fiscal, atividade, crédito, mercado de trabalho, expectativas (Focus, QPC) e o dado global, até existir o agente Externo.
    - x. Endógeno de outro agente: qualquer agente consulta, mas não tira conclusão sobre ele; a posição vem do agente responsável. Ex.: o agente de câmbio não conclui sobre o caminho da Selic sem a leitura do agente de política monetária.
    - xi. Exógeno e TWA: a forma de análise ainda será definida, a partir da interação entre os agentes. O mesmo dado pode ser consumido por mais de um agente, então é preciso uma visão consolidada sobre ele (ver IV.ii). Até lá, o agente usa o dado declarando no report as premissas que assumiu. (provisório, 2026-10-01)
    - xii. Expectativas não são da política monetária: são TWA, e pode haver um agente de expectativas no futuro.
    - xiii. Dados por agente: ver (V).
    - xiv. Ferramenta = um processamento específico e pré-definido de dados ou de informação qualitativa que gera um output que o agente usa direto, sem processar o bruto ele mesmo. Ex.: o FX attributor processa as cartas das gestoras sobre o câmbio e responde se elas veem o câmbio subindo ou caindo, e com que grau. (decidido 2026-10-02)
    - xv. O Modelo Estrutural não é ferramenta: é o filtro de saída da análise. Na discussão das variáveis e dos cenários, o cenário dos agentes também é expresso por meio do modelo estrutural. É output dos agentes, não input para eles. (decidido 2026-10-02)


# (II) Base de conhecimento

## (II.I) Organização
    - i. Separar bruto (repository) e o que o agente lê (obsidian). (feito 2026-09-30)
    - ii. Ingestão grava o clean_md direto no vault. (feito 2026-09-30)
    - iii. Definir o que é `clean_md`: texto bruto sem lixo, ou versão reorganizada sem perda de conteúdo. (pendente, sem decisão)

## (II.II) Câmbio
    - i. Mapa conceitual no formato novo. (feito 2026-09-30, aguardando revisão do usuário)
    - ii. Extrair os 12 PDFs de câmbio ainda sem raw_md.
    - iii. Terminar o modelo mental do Goldman Sachs (25 de ~80 edições feitas).

## (II.III) Política monetária
    - i. Comunicados do Copom no vault, atualizados junto com o ETL. (feito 2026-09-30, 234 comunicados)
    - ii. Atas do Copom, todas, no vault, atualizadas junto com o ETL. (feito 2026-09-30, 261 atas, 1998–2026)
    - iii. RPM integral dos últimos 3 anos no vault. (feito 2026-09-30, 12 relatórios, dez/2023–set/2026)
    - iv. RPM integral do histórico. (pendente)
    - v. Ingerir os 45 PDFs de `raw_pdf/theorical_literature/` (eram 35; 10 papers de prioridade alta entraram em 2026-10-07). Lista e o que falta: `repository/agent_mapping/recommended_bibliography/monetary_policy_bibliography.md`.
    - vi. Construir o mapa conceitual de política monetária, fechando as saídas e entradas com o de câmbio.
    - vii. Modelos mentais de política monetária das gestoras (Verde, Kinea, Kapitalo), a partir das mesmas cartas.
    - viii. Modelos mentais do BC: uma linha histórica (o que não muda com o presidente) e uma da gestão atual. (a discutir)
    - ix. Síntese trimestral de comunicado + ata + RPM. (a discutir)


# (III) Agentes

## (III.I) Agente de câmbio
    - i. Reconstruir o agente a partir do mapa conceitual. (feito 2026-10-07: `.claude/agents/cambio-analyst.md`)
    - ii. Corrigir a contradição sobre a PTAX nas instruções atuais. (feito 2026-10-07: a PTAX está no F(A))
    - iii. Dar ao agente acesso aos dados da lista (V.I). A forma é F(A) mais as funções G do agente (IV.iv). Feito o F(A) (2026-10-07): `uv run python -m analytics.agent_system.dados cambio` grava A e o F(A) em `obsidian/ciclos/<data>/dados/`. O agente lê o F(A) desde a reconstrução (item i).
    - iv. Saída em report estruturado: tese, premissas com dado, signposts, riscos, saídas para os outros agentes. (feito 2026-10-07: modelo `_modelo_report.md`)
    - v. Buscar um índice de commodities diário para complementar o Brent. (anotado 2026-10-07, ver depois)
    - vi. Teste solo da rodada 1 (só o câmbio), para avaliar o report e calibrar o F. (feito 2026-10-07: `obsidian/ciclos/2026-10-07/`; os comentários do usuário estão em IV.iv, IV.vii e IV.ix)
    - vii. Dados que o primeiro teste mostrou faltar (anotado 2026-10-15; o usuário decide depois, primeiro testa o formato do agente): fora da lista, o cupom cambial, a volatilidade implícita do real (é a que o Modelo Estrutural usa) e dado político e eleitoral; na base, o CDS parado em 08/09 e os termos de troca da Funcex em jul/2026.
        - Decidido (2026-10-15): dado eleitoral não entra enquanto o sistema está em teste. A volatilidade implícita não temos; o agente a trata como premissa declarada. O CDS parado em 08/09 se resolveu (a base tem 14/10).

## (III.II) Agente de política monetária
    - i. Construir o agente a partir do mapa conceitual de política monetária.
    - ii. Inflação é TWA (I.III.ix, xi). Quando o agente de inflação existir, vira endógeno dele e o agente de política monetária passa a receber a posição dele.

## (III.III) Interação e relatório
    - i. Definir o formato do report de cada agente. Decidido 2026-10-01:
        - Três blocos: tese, argumentação, premissas. Mais as saídas e pedidos aos outros agentes e o placar dos horizontes vencidos. Modelo: `obsidian/ciclos/_modelo_report.md`.
        - Tese por variável: medida central, faixa do cenário base com probabilidade, e worst-case e best-case como as caudas abaixo e acima da faixa, cada uma com probabilidade (soma 100%). Ex.: PIB 2027, central 1,2%; 50% entre 1,0 e 1,4; 40% abaixo de 1,0; 10% acima de 1,4.
        - A direção de worst e best é de cada variável: inflação mais alta é worst, crescimento menor é worst. No câmbio, por ora, depreciação é worst.
        - Assimetria: Pbc − Pwc, de −1 a +1; zero é simétrico e o sinal diz para que lado a distribuição pende (no exemplo, 0,10 − 0,40 = −0,30). Substituiu Pbc/Pwc, que não existe com Pwc = 0 e tem escala torta.
        - Riscos não são seção própria: entram na argumentação, justificando a probabilidade de cada cauda.
        - Central (2026-10-15): a do Modelo Estrutural no cenário base; a distribuição em torno dela é do agente (IV.ix).
        - Horizontes (2026-10-15, substitui curto, médio e longo prazo por agente): os trimestres do Modelo Estrutural, seis a partir do trimestre em curso (no ciclo de 07/10/2026, do 4T26 ao 1T28). A variável é medida no fechamento do trimestre (no câmbio, a PTAX do último dia útil), que é o que se compara com o dado de hoje.
            - A tese vira um caminho por trimestre. O dado que vai saindo é conferido contra a faixa de cada trimestre: um movimento que cai fora da faixa base mostra uma cauda se materializando naquele trimestre. Um movimento não mapeado é informação nova e dispara um ciclo.
            - Exceções são possíveis. Ex.: política monetária, cuja taxa no fim do trimestre sai das reuniões do Copom e do FOMC dentro dele.
        - Placar: para cada trimestre que fechou desde o último ciclo, o agente diz em que faixa a variável caiu.
        - Report e relatório em português; termos técnicos consagrados em inglês são permitidos (forward guidance, carry etc.).
    - ii. Fluxo e registro da interação:
        - Fluxo (desenho do usuário, 2026-10-02; substitui o esboço de 2026-10-01, em que um agente escrevia depois do outro):
            - Rodada 1: cada agente escreve o seu report. O Modelo Estrutural consolida os reports da rodada em P1.
            - Rodada 2: cada agente lê os reports de todos e o P1 e escreve de novo. O modelo consolida em P2.
            - Report final (RF): cada agente lê os reports de todos e o P2 e escreve o RF. Dos RF sai o cenário final (PF*), que vai para o relatório.
        - Registro (decidido 2026-10-01, revisto 2026-10-02): uma pasta por ciclo, `obsidian/ciclos/<data>/`. Os reports de cada rodada e as consolidações (P1, P2) ficam vivos durante o ciclo; quando o ciclo acaba, ficam o report final (RF) de cada agente e o log, além do relatório. O log registra o processo interno: quem leu o quê, cada mudança de premissa ou probabilidade entre rodadas (antes → depois, motivo, o que a provocou) e as divergências que ficaram abertas. Modelo: `obsidian/ciclos/_modelo_log.md`.
        - Ordem: dentro de uma rodada todos os agentes escrevem, sem ordem entre eles (2026-10-02, substitui câmbio → política monetária). Hoje: duas rodadas e o report final. Revisar quando entrar um agente novo (ver IV.iii).
        - Ciclo = um processo de atualização do cenário, disparado por informação nova (quantitativa ou qualitativa). Sem informação nova, o cenário não muda. Um único dado novo basta para rodar um ciclo, embora na prática o usuário prefira juntar mais dados antes.
    - iii. Checagem de todo número do relatório contra a fonte antes de publicar.
    - iv. Relatório final em markdown enquanto calibramos; PDF depois.
    - v. Primeiro teste completo com câmbio + política monetária.


# (IV) Decisões pendentes
    - i. Repasse cambial: câmbio ou inflação? Por ora o câmbio reporta (E1, E3 do mapa de câmbio).
    - ii. Como se forma a visão consolidada sobre um dado exógeno ou TWA: discussão entre os agentes ou um "economista-chefe" que calibra. E o que o agente faz com esse dado enquanto isso não estiver definido. (a discutir; para as exógenas, a intenção é distribuí-las a um ou dois agentes, I.III.ix)
    - iii. Número de rodadas por ciclo: reabrir sempre que entrar um agente novo. Hoje: duas rodadas e o report final.
    - iv. Como o agente analisa os dados quantitativos. (decidido 2026-10-02)
        - Decidido (2026-10-02, reescrito 2026-10-07): o dado bruto A passa por F, as transformações fixas, iguais em todo ciclo. O agente lê F(A), não A. Quando precisa de uma conta que o F não faz, escreve uma função G e usa G(A). Não há catálogo de funções à parte (2026-10-07).
        - As métricas do F (o tratamento de cada tabela) não são definidas pelo usuário: ficam no sistema, sob supervisão do próprio agente e do agente administrador. O usuário avalia pela qualidade do report e ajusta as métricas a partir daí. (2026-10-07)
        - Profundidade (2026-10-02, provisório até a distribuição das exógenas, IV.ii): endógenas com leitura completa (nível, variações, posição no histórico, pares); TWA e exógenas com leitura enxuta (último valor e variação).
        - Retrato fixo por ciclo: F(A) é gerado uma vez, no início do ciclo, e as duas rodadas e o report final leem o mesmo F(A). Dado que chega no meio do ciclo espera o próximo.
        - Sem exploração livre do banco. O G segue quatro regras: só lê, nunca escreve no banco; lê o mesmo A do ciclo; o código fica salvo com o ciclo; o G e o resultado entram no log. O report e o relatório final não citam o G; o rastro fica só no log.
        - Todo tratamento do dado passa por um G: variação, média, soma, diferença, forward, qualquer conta, por menor que seja. O dado usado como está na base ("a PTAX era 4,9698 em 06/10") não precisa de G, porque já é rastreável na própria base. (2026-10-07)
        - No fim do ciclo, o G fica só como registro ou é promovido ao F. Quem decide: o agente administrador (I.II.vi), quando existir.
    - v. Ferramentas (I.III.xiv): quais são (hoje candidatas: FX attributor e FX Model; dashboards não são ferramenta) e quando e como entram nos agentes. Por ora fora (I.II.iv).
    - vi. Como os reports viram P1, P2 e PF* no Modelo Estrutural (I.III.xv): com quais variáveis, quem faz a conta e o que acontece quando o modelo e os agentes divergem. (anotado 2026-10-02, a definir)
        - Decidido (2026-10-15, adianta a parte que o câmbio precisa): como a central vem do modelo (IV.ix), o agente roda o simulador do Modelo Estrutural por um G, com os caminhos das exógenas de cada cenário e, no tempero (i), o multiplicador do coeficiente. Sem reestimar: os coeficientes são os de hoje. As exógenas que a área não usa ficam no padrão do simulador (último valor repetido) até terem dono (IV.ii).
        - A função fixa que esse G chama (feito 2026-10-15: `analytics/agent_system/modelo.py`): recebe os caminhos das exógenas e os multiplicadores, devolve as endógenas por trimestre e a faixa do posterior. O retrato do simulador é gravado uma vez por ciclo, junto com o A. Consolidação de P1, P2 e PF* segue a definir.
    - vii. Agente escrivão (I.II.v):
        - Decidido (2026-10-07): a forma é do escrivão, o conteúdo é do agente. O escrivão reordena, corta, reescreve e padroniza; não muda número, faixa, probabilidade ou premissa, não acrescenta argumento nem dado e não resolve divergência escolhendo um lado. Se precisa de algo que o report não diz, cobra o agente. (manual, 1.1)
        - Decidido (2026-10-07): a cobrança reabre o report final só no trecho cobrado.
        - Decidido (2026-10-07, do primeiro teste), para o relatório final. Os reports intermediários seguem como estão, porque outros agentes os reprocessam:
            - sem nome de tabela (já estava no manual, 1.2);
            - comentário sobre o próprio processo ("o F não traz dado eleitoral", "a decomposição pelo modelo não está disponível") vai para nota de rodapé;
            - número arredondado ao que a afirmação precisa ("~60 mil contratos", não 59.481); o report guarda o valor exato e o escrivão questiona o arredondamento;
            - percentil ganha nota de rodapé na primeira aparição, dizendo o que "maior" significa, e nota própria quando o sentido for menos óbvio;
            - arcabouço de gestora ou conceito pouco conhecido ganha nota de rodapé que o explica de forma simples, com exemplo quando ajuda;
            - muitos números que se comparam vão em tabela.
        - Decidido (2026-10-15): o arredondamento e as notas explicativas vêm do agente. O agente arredonda no report final (a tabela e a data bastam para conferir o valor exato na fonte) e escreve as notas no próprio report. O escrivão leva as notas para o rodapé e pode pedir mais explicação, ou o arredondamento de um número que o agente deixou passar.
        - Decidido (2026-10-15, do primeiro teste), em todo report: cada dado da argumentação tem um de três papéis, e o papel decide onde ele fica:
            - sustenta: no parágrafo, ligado à afirmação por uma palavra que diga a relação ("o que mostra", "porque");
            - contraria ou enfraquece: no mesmo parágrafo, logo depois, com "mas" ou "apesar de" e o que teria de acontecer para mudar a conclusão. Não vai para apêndice, senão o argumento só mostra os dados a favor;
            - sem sinal neste ciclo: no bloco "Olhado, sem sinal", no fim da seção 2, uma linha por dado (dado · valor · por que não diz nada agora · o que o faria dizer algo). Mostra o que o agente olhou e descartou, para o usuário poder cobrar o descarte.
            - Afirmação com partes (ex.: "mercado fino" e "demanda fora do mercado à vista") é escrita em partes, e cada dado diz a qual delas responde.
            - Dado sem ligação com uma afirmação é defeito: ou o agente escreve a ligação, ou o dado vai para o bloco "Olhado, sem sinal". Exemplo do teste: o estoque de swaps citado como nível (−US$ 91,6 bi) não diz nada sobre o mês; a variação diria, a favor ou contra a tese.
        - Estrutura do relatório: a definir mais tarde.
        - Formato (intenção do usuário, 2026-10-15, a resolver depois): relatório final em HTML, numa aba de Report de um dashboard, para poder se ligar a ferramentas interativas de acompanhamento do cenário (ex.: a matriz de premissas, IV.ix). A aba teria um botão que gera o PDF.
        - Decidido (2026-10-15): o dashboard de Report é o mesmo do Modelo Estrutural, porque o modelo só funciona dentro da discussão dos agentes. O dash ganha nome novo e as abas são reorganizadas depois, pelo usuário. O acompanhamento das exógenas (IV.ix) mora nele.
    - viii. Agente administrador (I.II.vi): o que mais administra além da promoção de G ao F, com que critério promove e quem decide até ele existir. (anotado 2026-10-02, a definir)
    - ix. Formato das premissas e dos signposts (anotado 2026-10-15, do primeiro teste, a definir):
        - O formato da tabela de premissas ainda não convence o usuário.
        - Signpost como patamar ("PTAX acima de 5,15 por 3 sessões") diz pouco. Melhor descrever uma dinâmica, e talvez um conjunto de signposts lido junto (ex.: prêmio de risco subindo e real se depreciando nas sessões antes do 2º turno).
        - Ideia do usuário (2026-10-15): premissas numa matriz atualizável, cada uma com seu limiar e uma cor que muda conforme o dado se aproxima dele (ex.: limiar de 13% com o dado em 12,63%; a cor vai ao vermelho conforme a taxa sobe para 13%, porque indica depreciação).
        - Para depois: alarme de signpost enviado por e-mail.
        - Decidido (2026-10-15): por enquanto, sem alertas. O agente não escreve a linha de alerta nas fichas nem na tabela de acompanhamento; o acompanhamento das exógenas vai para o dashboard de Report (IV.vii).
        - Decidido (2026-10-15): o que pode ser expresso pelas variáveis do Modelo Estrutural, é; o agente complementa a estimativa quantitativa com um ajuste qualitativo. Toda premissa se materializa num de dois blocos:
            - canais do modelo quantitativo: entradas do modelo (ex.: o CDS para o risco fiscal). A premissa é o caminho da entrada por trimestre, no cenário base e em cada cauda. Um evento (ex.: o 2º turno) não tem lugar próprio: é o motivo de um caminho, e pode mover mais de uma entrada;
            - canais qualitativos: o que o modelo não tem (ex.: balanço de pagamentos, posicionamento). Cada um é acompanhado por um indicador (ex.: a posição especulativa no COT) e entra como desvio da variável projetada pelo modelo, com direção, tamanho e duração.
        - Decidido (2026-10-15): cada cauda da tese diz o que leva até ela, nos canais (ex.: "acima de 5,20 se o 2º turno reverter o resultado e o CDS for a 150").
        - Decidido (2026-10-15, revisão no mesmo dia; substitui os "dois blocos" acima, porque o teste v2 os misturou): as premissas se fazem em duas etapas.
            - Etapa 1, modelo. O agente escreve o caminho por trimestre de cada exógena do modelo que a área usa, no cenário base e em cada cauda, uma exógena por linha. O evento (2º turno, plano fiscal) é o motivo do cenário, não premissa. O modelo resolve as endógenas (hiato, inflação, expectativas, Selic, câmbio); o agente não as fixa. **A central da tese é a do modelo no cenário base, sem ajuste.**
            - Etapa 2, tempero qualitativo. O agente forma a distribuição em torno da central (limites das caudas e probabilidades), com dois tipos de justificativa:
                - (i) efeito de um input mais forte ou mais fraco que o estimado, escrito como multiplicador do coeficiente num cenário (ex.: na reversão, o modelo dá 5% de depreciação; por X1…Xn o efeito do CDS no câmbio é × 1,5). Quanto mais para a cauda da distribuição do coeficiente (o posterior do modelo), melhor tem de ser a justificativa; fora do intervalo de 90%, o agente afirma que o histórico subestima o canal, e diz por quê.
                - (ii) fator que não se expressa nas variáveis do modelo (ex.: desalavancagem de hedge funds, acompanhada pela posição no COT), com indicador, direção, tamanho e duração.
            - Canal que está no modelo só entra pelo tipo (i), nunca pelo (ii). É o que impede a contagem dupla (na v2, o estresse de regime somava +5% sobre o CDS a 150).
            - O caminho do input e a força do efeito ficam separados: "o CDS vai a 150 na reversão" é etapa 1; "cada ponto de CDS pesa mais que o estimado" é etapa 2 (i).
            - Quando o agente acha que o próprio cenário base deveria desviar do modelo, a central não se move: o tempero entra como assimetria (Pbc − Pwc). Assim o placar separa o erro do modelo do valor do tempero.
            - Vale para todo agente (na política monetária, (i) seria a regra de juros reagindo à inflação mais forte do que o estimado).
            - O que isso corrige na v2: a central justificada por forças qualitativas que as fichas diziam não usar (posicionamento, dezembro); caudas que somavam input e desvio na mesma frase; fichas que agrupavam vários inputs; Selic e IPCA fixados pelo câmbio, sendo endógenas do modelo; dado de evidência na linha "Hoje".
        - Formato no `_modelo_report.md` (2026-10-15): seção 3 em três partes: etapa 1 (cenários com a história de cada um, tabela de caminhos das exógenas, saída do modelo), etapa 2 (uma ficha por tempero) e a ponte até a tese. O alerta tem forma fixa (indicador · tipo · limiar · janela), para a matriz conseguir ler.


# (V) Dados por agente
*Cada agente tem a sua lista, e a mesma tabela aparece em mais de uma, com o motivo daquele agente. Os grupos seguem os tipos de (I.III.ix): endógeno (da área), endógeno de outro agente (consulta; a posição vem daquele agente), TWA e exógeno.*

## (V.I) Agente de câmbio

### i. Endógeno
    - `cmb_ptax`: PTAX de venda diária do BCB (desde jul/1994) e volume do interbancário. É a variável que o agente explica; o volume diz se o movimento veio com mercado fundo ou raso.

    - `cmb_cambio_contratado`: câmbio contratado diário desde set/2008, separado em exportação, importação e financeiro. É o fluxo em alta frequência, para ler o movimento dentro do mês antes do dado mensal.

    - `cmb_balanco_pagmt`: balanço de pagamentos mensal (BPM6), com conta corrente e conta financeira abertas. Dá a oferta estrutural de dólares e a qualidade do financiamento do déficit: investimento direto é estável, carteira é volátil (canal 2.5).

    - `cmb_comex_fator_agregado`: balança comercial do MDIC por fator agregado (básicos, semimanufaturados, manufaturados). Mostra que tipo de produto gera o saldo e, portanto, a que preço ele está exposto; não fecha linha a linha com o balanço de pagamentos.

    - `cmb_comex_pais`: balança comercial por parceiro (China, EUA, Argentina, Alemanha). Mostra por onde um choque de demanda externa chega ao saldo e ao real.

    - `cmb_comex_produto`: exportação e importação de petróleo, soja, minério de ferro, carnes e café. Separa preço de volume no saldo e liga o real a cada commodity (canal 2.4).

    - `cmb_reservas_bc`: reservas internacionais e intervenções do BCB (swaps, leilões à vista e de linha). Mede o colchão contra crise (canal 2.9) e o que o BC está fazendo no mercado (canal 2.7).

    - `cmb_cot_fx`: posição em futuros de BRL e MXN na CFTC (CLP e COP não têm contrato no relatório), semanal, por tipo de participante. Posição especulativa extrema é sinal contrário e amplifica o movimento quando é desmontada (canal 2.6).

    - `cmb_reer`: câmbio efetivo real e nominal do BIS para BR, MX, CL e CO. É a medida de nível: quão caro ou barato o real está contra os parceiros, já corrigido por inflação (canal 2.8).

    - `cmb_termos_troca`: termos de troca da Funcex, mensal desde 1978. Termos de troca melhores aumentam o saldo comercial e sustentam o real (canal 2.4).

    - `cmb_fx_latam`: MXN, CLP, COP e PEN contra o dólar, diário. É o grupo de comparação que separa o movimento global, compartilhado com os pares, do que é só do real.

    - `diferenciais_juros`: Selic menos Fed Funds, nominal e real ex-post, mensal. O carry é leitura do câmbio (canal 2.1); o caminho da Selic por trás dele vem do agente de política monetária (S1).

### ii. Endógeno de política monetária (consulta; a posição vem pelas saídas S1–S4 do mapa de câmbio)
    - `pm_copom_calendario`: datas das reuniões do Copom. São os eventos que concentram a volatilidade do carry e da curva.

    - `pm_copom_reuniao`: Selic decidida e passo, por reunião. É a perna doméstica do carry já realizado; para onde ela vai é S1.

    - `pm_copom_projecoes`: projeções de inflação do Copom, de referência e alternativas. Mostram quanto da inflação projetada o Copom atribui ao câmbio e sustentam a leitura da função de reação (S4); o câmbio de partida do cenário está no texto do comunicado, no vault.

    - `br_di_grade`: curva DI com todos os vértices da B3. Dá a Selic implícita reunião a reunião, ou seja, o carry futuro precificado (S1), e o nível da curva. É a única curva doméstica que o câmbio recebe (2026-10-07).

    - `inflc_meta`: meta de inflação do CMN. É a inflação doméstica de longo prazo que entra na paridade de poder de compra prospectiva.

### iii. TWA — expectativas
    - `expc_focus_periodo` (câmbio): mediana da Focus para o câmbio no fim de cada ano. Mostra o que o consenso já espera, para separar surpresa de convergência.

    - `expc_focus_copom`: mediana da Focus para a Selic em cada reunião. É o carry futuro esperado pelo consenso, para comparar com a curva.

    - `expc_focus_periodo` (Selic): mediana da Focus para a Selic no fim de cada ano. Nível do carry esperado num horizonte mais longo que o das reuniões.

    - `expc_focus_periodo` (IPCA): mediana da Focus para o IPCA no fim de cada ano. É a inflação doméstica esperada que entra na paridade de poder de compra prospectiva, ao lado da meta.

### iv. TWA — externo
    - `cmb_dollar_index`: DXY, dólar contra moedas desenvolvidas, diário. Separa o ciclo global do dólar do que é do real (canal 2.3).

    - `cmb_dollar_index_em`: dólar contra moedas emergentes (FRED), diário desde 2006. Comparação mais próxima do real que o DXY, porque tira o efeito do euro e do iene.

    - `cmb_equity_us`: S&P 500, diário. Proxy do apetite a risco global, que move o real junto com os outros emergentes (canal 2.2).

    - `us_interest_rate`: só o Fed Funds e os Treasuries de 2 e 10 anos (2026-10-07). É a perna externa do carry; o de 10 anos move o ciclo global do dólar.

    - `cmb_real_rates`: juro real ex-post de BR, MX, CL, CO e PE. Compara o carry real do Brasil com o dos pares.

    - `comm_brent`: Brent em dólar, diário. O Brasil exporta petróleo, então o preço entra nos termos de troca e no saldo (canal 2.4).

    - `comm_icbr_usd`: IC-Br em dólar. Preço das commodities relevantes para o Brasil sem a variação cambial embutida: o insumo certo para explicar o real.

### v. TWA — doméstico
    - `inflc_agregados`: IPCA e seus componentes. Entra na inflação relativa da paridade de poder de compra e no câmbio real; o agente usa o número sem opinar sobre a inflação.

    - `fisc_nfsp`: resultado primário e nominal do setor público em % do PIB, 12 meses. Esforço fiscal fraco eleva o prêmio de risco do real (canal 2.2).

    - `fisc_divida`: dívida bruta e líquida em % do PIB. A trajetória da dívida é o fundamento do prêmio de risco (canal 2.2).

    - `atv_pib_usd`: PIB mensal em dólar. É o denominador do balanço de pagamentos em % do PIB.

### vi. Exógeno
    - `cmb_risco_pais`: CDS de 5 anos do Brasil. É o preço do risco soberano, par do real no canal de prêmio de risco (2.2); a carga é por export manual da Bloomberg, então conferir a data do último dado antes de usar.

## (V.II) Agente de política monetária

### i. Endógeno
    - `pm_copom_calendario`: calendário oficial das reuniões, inclusive as do ano seguinte. Situa cada leitura no ciclo e permite ler Focus e curva reunião a reunião.

    - `pm_copom_reuniao`: Selic decidida e passo, por reunião. É o histórico de decisões que, junto com as projeções, revela a função de reação.

    - `pm_copom_projecoes`: projeções de inflação do Copom (referência e alternativas), dos comunicados e do RPM. É a variável que o Copom persegue; o desvio dela para a meta no horizonte relevante explica a decisão.

    - `pm_hiato_produto`: hiato do produto do BCB na última edição do RPM. É a ociosidade que entra na projeção do BC; a diferença para o hiato do mercado (QPC) é fonte de divergência sobre o juro.

    - `pm_hiato_produto_vintages`: todas as estimativas de hiato já publicadas. Revisão do hiato muda a projeção sem que o dado do mês mude, e por isso explica mudanças de postura que os dados correntes não explicam.

    - `br_interest_rate`: curva de juros da B3 nos vértices padrão, com a Selic. Mostra o juro nominal e real que o mercado precifica; o juro real é a medida de quão restritiva está a política.

    - `br_di_grade`: curva DI com todos os vértices. Dá a Selic implícita reunião a reunião, para comparar com a Focus e com a sinalização do Copom.

    - `inflc_meta`: meta de inflação do CMN. É a âncora contra a qual projeções e expectativas são medidas; dado institucional, não leitura de inflação.

### ii. Endógeno de câmbio (consulta; a posição vem pelas entradas E1–E7 do mapa de câmbio)
    - `cmb_ptax`: câmbio diário. Entra na projeção de inflação do Copom; se o movimento é persistente ou transitório (E1) e global ou idiossincrático (E2) vem do agente de câmbio.

    - `cmb_fx_latam`: moedas dos pares latinos. Base da separação global × idiossincrático (E2): depreciação só do real costuma vir com prêmio de risco, que também afeta expectativas.

    - `cmb_reer`: câmbio real efetivo. Diz se o real está caro ou barato, o ponto de partida para a distância entre o câmbio de mercado e a premissa do Copom (E4).

    - `cmb_reservas_bc`: reservas e intervenções. Mostra se o BC está usando instrumento cambial em vez do juro (E7).

    - `cmb_cambio_contratado`: fluxo cambial diário, somado no mês. Pressão de liquidez que pode levar à intervenção (E7) e fundamento para a persistência do movimento (E1).

    - `cmb_balanco_pagmt`: balanço de pagamentos. Déficit externo mal financiado aumenta a vulnerabilidade e o prêmio de risco (E5).

    - `cmb_cot_fx`: posição especulativa em BRL. Posição grande sustentada pelo carry é risco de reversão do câmbio quando o juro cair (E6).

    - `cmb_termos_troca`: termos de troca. Choque de termos de troca muda o câmbio de forma persistente (E1) e, por ele, a projeção de inflação.

    - `cmb_comex_fator_agregado`, `cmb_comex_pais`, `cmb_comex_produto`: composição do saldo comercial. Contexto para a persistência do movimento (E1); raramente lidas diretamente pelo agente de política monetária.

    - `diferenciais_juros`: Selic menos Fed Funds. Mede quanto do carry sustenta o real (E6): se o carry deixa de funcionar, enfraquece o canal pelo qual a Selic chega à inflação via câmbio.

### iii. TWA — expectativas
    - `expc_focus_copom`: mediana da Focus para a Selic em cada reunião. É o caminho esperado pelo consenso; a diferença para a curva é prêmio, a diferença para a comunicação é espaço de surpresa.

    - `expc_focus_periodo` (Selic): mediana da Focus para a Selic no fim de cada ano. Nível do juro esperado num horizonte mais longo que o das reuniões.

    - `expc_qpc`: Questionário Pré-Copom: o que o mercado acha que o Copom fará e deveria fazer, o balanço de riscos, o hiato do mercado e as projeções de IPCA (curto prazo e horizonte relevante, em percentis). Mostra o consenso às vésperas da reunião e onde ele discorda do BC, inclusive sobre a inflação no horizonte relevante.

    - `expc_focus`: expectativa de inflação 12 e 24 meses à frente. É a expectativa que o Copom cita em todo comunicado.

    - `expc_focus_periodo` (IPCA): expectativa de IPCA por ano-calendário. Mostra o que o mercado espera para a inflação em cada ano do horizonte relevante.

    - `expc_focus_periodo` (câmbio): câmbio esperado pelo consenso. A distância para a premissa do Copom é um dos riscos do cenário de referência; a leitura do câmbio continua vindo do agente de câmbio (E4).

### iv. TWA — inflação (vira endógeno do agente de inflação quando ele existir)
    - `inflc_agregados`: IPCA e IPCA-15 com componentes, difusão e núcleos. É a inflação corrente que o Copom lê, em especial serviços subjacentes e núcleos, que mostram a persistência.

    - `inflc_decomposicao`: IPCA por subitem, com peso e contribuição. Separa choque pontual (alimentos, energia) de pressão disseminada, a distinção que decide se o Copom reage.

    - `inflc_decomposicao_item`: a mesma decomposição por item. Mostra se o movimento de um grupo vem de um item ou de vários.

    - `inflc_dim`: classificação analítica do BC para cada subitem. Permite reconstruir os mesmos recortes que a ata cita (serviços subjacentes, industriais, alimentação no domicílio).

### v. TWA — atividade
    - `atv_pib`: PIB trimestral pela oferta e pela demanda. Crescimento da demanda doméstica acima do potencial fecha o hiato e pressiona a inflação.

    - `atv_pib_taxas`: taxas oficiais de variação do PIB. Permitem citar os mesmos números que o comunicado e a ata citam.

    - `atv_pib_valores_correntes`: PIB a preços correntes por componente. Dá os pesos para medir a contribuição de cada componente ao crescimento.

    - `atv_pib_mensal`: PIB mensal em reais, 12 meses. É o denominador das razões de crédito e fiscal em % do PIB.

    - `atv_ibcbr`: IBC-Br, total e por setor. Leitura mensal do ciclo entre dois PIBs, a mesma que o BC acompanha.

    - `atv_pim`: produção industrial por atividade. Ciclo do setor mais sensível ao juro e ao câmbio.

    - `atv_pim_uso`: produção industrial por categoria de uso. Bens de capital antecipam o investimento; bens de consumo duráveis respondem ao crédito.

    - `atv_pmc`: volume do varejo. Consumo de bens, o componente mais sensível ao crédito e à Selic.

    - `atv_pms`: volume de serviços. Liga a atividade à inflação de serviços, a parte que o Copom trata como mais persistente.

    - `atv_renda_poupanca`: renda nacional, poupança e capacidade de financiamento. Poupança e investimento são determinantes do juro neutro.

### vi. TWA — mercado de trabalho
    - `mt_pnad`: desocupação, ocupação, rendimento e massa salarial. Mede a folga do mercado de trabalho e o crescimento da renda, que alimenta a inflação de serviços.

    - `mt_desocupacao_retro`: desocupação dessazonalizada retropolada pelo BCB, desde 2004. É a série que o BC usa, longa o bastante para comparar o nível atual com o histórico.

    - `mt_caged`: estoque de emprego formal. Sinal mensal do ciclo, mais rápido que a PNAD.

    - `mt_caged_setor`: saldo de empregos por setor. Mostra se o emprego cresce em serviços, onde a pressão salarial chega mais direto à inflação.

### vii. TWA — crédito
    - `cred_credito_resumo`: saldo, concessões, juros, spread e inadimplência, por recurso e segmento. É a leitura principal da transmissão: se concessões e taxas respondem à Selic, a política está funcionando.

    - `cred_fluxo_financeiro`: impulso de crédito no conceito do RPM. É o mesmo número que o BC usa ao falar de condições financeiras.

    - `cred_ptc`: percepção dos bancos sobre oferta e demanda de crédito. Antecede a transmissão que os saldos só mostram depois.

    - `cred_credito_familias`: endividamento e comprometimento de renda das famílias. Canal de renda: juro mais alto pesa no serviço da dívida e no consumo.

    - `cred_credito_amplo`: crédito ao setor não financeiro, incluindo títulos e dívida externa. Mostra a transmissão pelo mercado de capitais, que o crédito bancário não capta.

    - `cred_modalidade_livre_pf`: crédito livre à pessoa física por modalidade. É o crédito mais sensível à Selic, onde a transmissão aparece primeiro.

    - `cred_modalidade_livre_pj`: crédito livre à pessoa jurídica por modalidade. Mesma leitura, lado corporativo.

    - `cred_modalidade_direcionado_pf`: crédito direcionado à pessoa física (imobiliário, rural). Pouco sensível à Selic: quanto maior a fatia dele, menor a potência da política.

    - `cred_modalidade_direcionado_pj`: crédito direcionado à pessoa jurídica (BNDES). Mesma leitura, lado corporativo.

    - `cred_credito_controle_capital`: crédito por controle do banco (público, privado, estrangeiro). Expansão dos bancos públicos pode compensar o aperto monetário.

    - `cred_inadimplencia_pj`: inadimplência e atraso de 15 a 90 dias das empresas. Mede o custo do aperto e o risco para a estabilidade financeira.

### viii. TWA — fiscal
    - `fisc_nfsp`: resultado primário, nominal e juros em % do PIB, 12 meses. Política fiscal expansionista estimula a demanda e exige juro mais alto para o mesmo resultado de inflação.

    - `fisc_divida`: dívida bruta e líquida em % do PIB. A trajetória da dívida afeta o prêmio de risco e as expectativas, e por aí o juro neutro.

    - `fisc_dlsp_fatores`: o que explica cada variação da dívida líquida. Mostra quanto do crescimento da dívida é o custo da própria Selic.

    - `fisc_rtn`: resultado do governo central, mensal. Mostra o cumprimento do arcabouço, a base da "política fiscal crível" que o Copom menciona.

    - `fisc_efgg`: estatísticas fiscais do governo geral pela classificação do FMI, trimestral. É a base para medir o impulso fiscal, o estímulo à demanda que o Copom pondera.

### ix. TWA — externo
    - `us_interest_rate`: curva do Treasury e meta do Fed. O juro americano condiciona o espaço para o diferencial de juros e o apetite por emergentes.

    - `inter_interest_rate`: taxa de política dos pares latinos. Mostra o ciclo dos outros BCs, referência para quanto o Copom pode se afastar.

    - `cmb_real_rates`: juro real ex-post dos pares. Compara o grau de restrição da política brasileira com o dos pares.

    - `cmb_dollar_index`: DXY. Condição financeira global, que o Copom descreve como cenário externo.

    - `cmb_dollar_index_em`: dólar contra emergentes. Mostra se a pressão sobre moedas emergentes é generalizada.

    - `comm_brent`: Brent em dólar. Choque de oferta que chega aos combustíveis e aos preços administrados; o Copom olha os efeitos secundários, não o choque.

    - `comm_icbr`: IC-Br em reais e sub-índices. Pressão das commodities sobre alimentos e energia já com o câmbio embutido, que é a forma em que ela chega ao IPCA.

### x. Exógeno
    - `cmb_risco_pais`: CDS de 5 anos do Brasil. Termômetro da percepção de risco que o Copom cita e que chega ao juro longo e ao câmbio; conferir a data do último dado, a carga é manual.

### xi. Fora da lista (consulta livre, sem uso previsto)
    - `mt_pnad_trimestral`, `mt_caged_uf`, `mt_caged_salario`, `cred_credito_porte`, `cred_credito_atividade_economica`, `cred_credito_tipo_cliente`, `fisc_investimento`: cortes estruturais, regionais ou de detalhe que não mudam a leitura do juro.
