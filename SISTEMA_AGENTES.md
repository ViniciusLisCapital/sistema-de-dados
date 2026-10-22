**Sobre este arquivo:** organização do sistema de agentes-analistas. Mantido pelo Claude a pedido do usuário: marca o que foi feito e acrescenta o que a conversa decidir. Uma decisão só entra aqui depois que o usuário a tomou. Detalhe técnico vai para o `CLAUDE.md` da pasta, não para cá. Os princípios gerais, que valem para todo agente, ficam no `PRINCIPIOS_AGENTES.md`. A ordem do trabalho até o agente de política monetária finalizado (fases, estimativas, o que roda em paralelo) fica no [`PLANO_AGENTES.md`](PLANO_AGENTES.md).


# (I) O sistema

## (I.I) Objetivo
    - i. Relatório macroeconômico único: contexto atual e tese de cenário, construído a partir da opinião de agentes especialistas.
    - ii. Cada agente usa dados, referencial teórico (literatura) e prático (modelos mentais) e ferramentas.
    - iii. Relatório claro e sem verbosidade; teses falseáveis, com premissas, signposts e checkpoints ("se X continuar em Y, a tese muda").
    - iv. Nenhuma informação inverídica ou misleading: todo número rastreável até a fonte.

## (I.II) Agentes
    - i. Câmbio e política monetária primeiro. Testar bem os dois antes de acrescentar outro.
        - Revisto em 2026-10-22: com só dois agentes, cada um escrevia exógenas que não lhe competem (a NTN-B de 10 anos decidiu a central da Selic sem dono). Os agentes que o Modelo Estrutural precisa entram de uma vez, na forma mínima e sem teste solo: inflação, atividade, fiscal, externo e expectativas, com câmbio e PM, formam o primeiro batch de sete. O primeiro teste é o ciclo conjunto, sem literatura (`PLANO_AGENTES.md`, Fases 7–10).
    - ii. Depois, um a um: crédito, mercado de trabalho e os demais.
    - iii. Os agentes rodam no Claude Code, sob demanda, nesta fase.
    - iv. O modelo quantitativo (Modelo Estrutural, FX Model) fica fora dos agentes por enquanto. Primeiro, azeitar o processo analítico e o fluxo de informação. Quando o Modelo Estrutural entrar, entra como saída dos agentes, não como ferramenta (I.III.xv).
    - v. Agente escrivão (2026-10-02): organiza o relatório final a partir dos reports finais (RF) e do cenário final (PF*). O objetivo é um relatório em ótimo português, de clareza e objetividade excepcionais. Garante a validade lógica e a coesão dos argumentos dos reports, e pode cobrar de um agente mais clareza numa explicação. Regras em IV.vii. Manual de escrita: `obsidian/escrivao/manual_do_escrivao.md` (feito 2026-10-07).
    - vi. Agente administrador (intenção do usuário, 2026-10-02): administra o sistema e cuida da manutenção dele. Primeira tarefa prevista: decidir quais funções G criadas pelos agentes são promovidas ao F (IV.iv). Detalhes a definir (IV.viii).
    - vii. Agente trader (decidido 2026-10-20): a literatura de trading (`repository/trader/`, 26 capítulos de dois livros de Willer et al.) é a bibliografia de um agente novo, e não de um pilar temático. Ingerida em `obsidian/trader/clean_md/` no mesmo dia; papel e desenho do agente a definir.

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
        - Decidido (2026-10-22): expectativas têm agente próprio (`expectativas`), dono da variável de expectativas do Modelo Estrutural.
    - xiii. Dados por agente: ver (V).
    - xiv. Ferramenta = um processamento específico e pré-definido de dados ou de informação qualitativa que gera um output que o agente usa direto, sem processar o bruto ele mesmo. Ex.: o FX attributor processa as cartas das gestoras sobre o câmbio e responde se elas veem o câmbio subindo ou caindo, e com que grau. (decidido 2026-10-02)
    - xv. O Modelo Estrutural não é ferramenta: é o filtro de saída da análise. Na discussão das variáveis e dos cenários, o cenário dos agentes também é expresso por meio do modelo estrutural. É output dos agentes, não input para eles. (decidido 2026-10-02)
    - xvi. Crescer por camadas (decidido 2026-10-21). Ingerir e sintetizar toda a literatura de câmbio e de PM antes de ter o agente foi um erro estratégico: só rodando se vê quanto o agente busca na literatura e como a usa. Daqui em diante: começar pequeno, testar e, se estiver certo, ampliar.
        - O material de cada agente (literatura, modelos mentais, documentos do Copom) tem três camadas; o agente roda só com a camada 1, por um retrato do conhecimento por ciclo. Os dados ficam como estão (V).
        - Nada do que foi feito é apagado: o que está fora da camada 1 é estoque, e entra por promoção (fila de prioridade do agente, lote a lote, ou demanda do ciclo, que fura a fila).
        - Agente novo ingere e sintetiza só a camada 1.
        - Regras em `PRINCIPIOS_AGENTES.md` (I.VI); fases em `PLANO_AGENTES.md`.
    - xvii. Dono da literatura (decidido 2026-10-21). Cada fonte de literatura tem um agente dono, e cada agente tem a sua biblioteca.
        - O dono é decidido pela pergunta que a fonte pretende responder: o agente responsável pela variável que ela explica. Ex.: repasse cambial é do agente de inflação, porque o paper não investiga por que o câmbio se deprecia, e sim como a depreciação afeta a inflação; Blanchard (2004) é da PM, porque discute a eficácia da política monetária supondo dominância fiscal (se investigasse a dominância fiscal em si, como acontece e o que é, seria do fiscal). Caso ambíguo vai para o usuário.
        - A camada (I.III.xvi) é a da biblioteca do dono.
        - Os outros agentes chegam à literatura de um dono pelos conceitos: o retrato do ciclo de um agente leva a camada 1 dele, os conceitos ligados a ela e, por esses conceitos, a camada 1 dos outros donos; nunca a camada 2 ou 3 de ninguém. O log registra quando um agente leu material de outro.
        - Literatura cujo dono ainda não existe (ex.: inflação, fiscal, externo) fica numa camada 1 provisória desse dono futuro, alcançável pelos conceitos como se ele já existisse. Mesma lógica do dado TWA.
        - Conceito não tem dono: a pasta `obsidian/concepts/` é única e qualquer agente lê.
        - O dono fica registrado no tracker agora. Mover os arquivos para a pasta do dono fica para depois, de uma vez, quando o primeiro agente novo for criado (`PLANO_AGENTES.md`, Fase 9).
        - O agente que vê algo relevante para a literatura de outro dono avisa pelo mecanismo de saídas do mapa. Ex.: o câmbio, ao ver risco relevante de depreciação, avisa o agente de inflação.


# (II) Base de conhecimento

## (II.I) Organização
    - i. Separar bruto (repository) e o que o agente lê (obsidian). (feito 2026-09-30)
    - ii. Ingestão grava o clean_md direto no vault. (feito 2026-09-30)
    - iii. O `clean_md` é o `raw_md` menos três coisas: a lista de referências, o apêndice de disclosures de relatório de banco e linhas de boilerplate conhecido (aviso do JSTOR, marca d'água, carimbo de diagramação). Nenhuma regra julga a linha pelo formato: número de página, cabeçalho corrido, número de eixo de gráfico, URL e contato ficam. As regras de formato eram 2,1% do que se removia e todas as perdas silenciosas de conteúdo achadas em três auditorias (células de tabela, frases com URL, linha de total de tabela). A releitura dos 123 arquivos devolveu 15.521 linhas. (decidido 2026-10-20)
    - iv. A ingestão é um processo mecânico do sistema, não tarefa de agente de área. (decidido 2026-10-19)
        - O PDF vai direto para `repository/<área>/raw_pdf/`, e não sai mais de lá. O usuário põe o PDF lá; o Claude também, quando busca literatura na web. (revisto no mesmo dia: substitui a caixa de entrada única)
        - `/ingest` (todas as áreas) ou `/ingest <área>` chama o agente de ingestão. Ele varre o `raw_pdf/` atrás do PDF sem `raw_md` (o pendente), extrai com as ferramentas determinísticas, confere o resultado contra as páginas do PDF e grava `repository/<área>/raw_md/` e `obsidian/<área>/clean_md/`.
        - O controle da literatura é o `repository/agent_mapping/data_tracker.xlsx`, uma aba "Qual" por área: a cada ingestão o sistema atualiza o status de cada fonte (ingerida, pendente, precisa de atenção, em espera) a partir do que está nas pastas.
        - O agente escolhe como extrair e confere; o texto é sempre das ferramentas, nunca escrito por ele. Arquivo que as ferramentas não recuperam (PDF escaneado) volta para o usuário.
        - Volume: intenso no começo do sistema; depois, só material marginal.
    - v. Depois da ingestão, um agente do vault faz a síntese, extrai os conceitos e faz os links. (construído 2026-10-19: `.claude/agents/vault.md`, opus; piloto em 3 papers de política monetária, aguardando revisão do usuário)
        - `/vault` (todas as áreas) ou `/vault <área> [arquivo ...]`. O pendente é o `clean_md` sem nota de síntese. No máximo 5 por rodada, um de cada vez: lê o `clean_md` inteiro, escreve a síntese, atualiza ou cria os conceitos, roda o `vault.py check` e o `tracker.py`.
        - A nota de síntese tem o nome do `clean_md`. As 19 notas antigas foram renomeadas no mesmo dia e os links ajustados. Fleming 1962 fica como está, porque não tem `clean_md`.
        - Uma pasta só de conceitos para todas as áreas: `obsidian/concepts/`. Página existente só recebe patch: a linha na tabela e o link.
        - Todo número da síntese tem de estar no `clean_md`; o `vault.py check` confere. Texto danificado vai para as limitações, não é reconstruído.
        - A literatura é lida pelo raciocínio, não pelos números: mecanismo, premissas, quando vale e quando falha. O resultado entra como teste do argumento (o sinal, o canal que domina, a robustez), e um número só onde ele decide o argumento, sempre com a amostra, o país e o período. Tabela não é transcrita. A estimativa de um paper nunca vira valor atual: o dado atual vem do banco. Vale para as notas de síntese e para as páginas de conceito (`vault.md`). As notas já escritas seguem o modelo anterior. (decidido 2026-10-20)
        - A síntese é sobre o material, não sobre as perguntas da área: resume o que a fonte diz, sem filtro pelo que o agente-analista precisa responder. Se as perguntas mudarem, nada precisa ser ressintetizado, e nada se perde por não ter sido perguntado. Síntese e mapa conceitual são processos independentes: o agente do vault não lê o mapa nem os clusters e notas do tracker, e não propõe acréscimos ao mapa. (decidido 2026-10-20)
        - A linha Source pode tirar título, autor e data do tracker quando o `clean_md` não tem página de rosto (capítulo de livro). Só essa linha. (decidido 2026-10-20)
        - Os números das páginas de conceito também são conferidos (`vault.py concept`), contra o `clean_md` das notas que a página linka. (feito 2026-10-20)
        - Fora do agente: os documentos do Copom em `clean_md/central_bank/` (precisam de desenho próprio, ver II.III.ix); e as 19 notas antigas, que não passam no check (4 sem as seções do modelo, 12 com número que não está no `clean_md`). O usuário vai repassar esse material pela ingestão; conferir de novo depois. (decidido 2026-10-20)
    - vi. As listas de literatura e de dados vivem só no `repository/agent_mapping/data_tracker.xlsx`, sem .md, salvo o muito necessário (decidido 2026-10-19). A justificativa de cada fonte ou série fica em Comments; a de cada cluster ou seção (escopo, lacunas, ordem de aquisição), na aba Notes. Os .md de `recommended_bibliography/` e `recommended_data/` foram apagados (estão no histórico do git).
    - vii. Um agente de modelos mentais lê as cartas das gestoras e faz crescer o documento de cada gestora × área. (construído 2026-10-20: `.claude/agents/mental-model.md`, opus; processo em `repository/mental_model/MENTAL_MODELS.md`)
        - `/mental <gestora> <área>`. Algumas cartas por rodada, em ordem de data, cada uma lida inteira; o `ledger/` guarda quais cartas cada documento já leu.
        - A extração das cartas é da ingestão (`/ingest mental_model/<gestora>`), não do agente de modelos mentais. (decidido 2026-10-20)
        - Reempacotar, nunca excluir: a entrada que as cartas novas acrescentam é reescrita como um texto coerente que incorpora a nuance, sem perder nada do que tinha (citações, aplicações datadas, números, links). Só as entradas que a rodada toca; a numeração das entradas não muda. O `mental.py check` confere contra a versão anterior. (decidido 2026-10-20)
        - O sentido é conferido por um segundo agente, independente (`mental-model-reviewer`): o escritor lista as afirmações do texto antigo e as novas, e o revisor, sem ver o raciocínio do escritor, julga cada uma contra o texto antigo, o novo e as cartas. A rodada só é registrada se nada foi perdido, distorcido ou inventado, ou se o usuário aceitar. Os vereditos ficam no `ledger/<documento>.log.md`. (decidido 2026-10-20)
        - Citação literal e número da carta; o `mental.py check` confere as duas coisas.

## (II.II) Câmbio
    - i. Mapa conceitual no formato novo. (feito 2026-09-30, aguardando revisão do usuário)
    - ii. Extrair os 12 PDFs de câmbio ainda sem raw_md. (feito 2026-10-20: 35 PDFs, 35 raw_md; 17 com síntese, as outras só se promovidas, I.III.xvi)
    - iii. Terminar o modelo mental do Goldman Sachs (25 de ~80 edições feitas). (estoque: só se promovido, I.III.xvi)
    - iv. Camada 1 e fila de prioridade do câmbio (I.III.xvi). (aprovado 2026-10-21; vai para as colunas Dono/Camada/Fila do tracker quando a planilha migrar)
        - Donos das 35 fontes da pasta de câmbio (I.III.xvii): inflação (provisório): Cortapasso 2023, Goldfajn & Werlang 2000, Belaisch 2003. Externo (provisório): FMI 2010, FMI 2012, Krugman 2023 (renda nacional e balanço de pagamentos), Eichengreen & Hausmann 1999, Eichengreen & Kawai 2014, Garcia & Valpassos 1998. PM: Mundell 1963, Fleming 1962. Câmbio: as outras 23, mais o BIS 2026 (que está na pasta de PM).
        - Camada 1 do câmbio: Froot & Thaler 1990 (2.1), Paiva 2006 (2.4 e 2.8), Chamon & Garcia 2016 (2.5), BIS 2026 (2.6), BCB 2020 posição de câmbio (2.7), Obstfeld 1994 (2.9) e o modelo mental da Verde. O 2.2 chega pelo conceito de dominância fiscal à camada 1 da PM. O 2.3 ficou sem literatura numa decisão tomada com a informação errada de que o acervo não tinha fonte; há duas na pasta de PM (Kalemli-Ozcan 2019 e Obstfeld 2015), e o dono e a camada delas se decidem na Fase 2 (decidido 2026-10-21).
        - Camada 1 provisória de outros donos, alcançada pelos conceitos: Cortapasso 2023 (inflação) e FMI 2010 (externo).
        - Fila do câmbio (camada 2, em ordem): Krugman 2023 cap. 14, Goldman Sachs 2025 (GSDEER/GSFEER), Fama 1984, modelo mental da Kapitalo, Dornbusch 1976, modelo mental da Kinea, Flood 1983. O resto é camada 3, inclusive Krugman 2000 (texto extraído ilegível) e o modelo mental do Goldman Sachs.
        - Re-teste da rodada 1 só com a camada 1 (Fase 4, 2026-10-21, ciclo 2026-10-15): report completo; o agente abriu o mapa, a Verde, 6 conceitos e 2 sínteses, nenhum clean_md. Promovido pelo "faltou" (decisão do usuário): o modelo mental da Kapitalo sobe para a camada 1. A síntese do Cortapasso 2023 foi escrita sobre uma extração incompleta e o clean_md hoje está inteiro: a síntese sai e é refeita pelo `/vault`. O resto do "faltou" (Kinea, GS, repasse com coeficientes, estudo de evento de eleições, desmonte de carry em emergentes, cupom cambial, vol implícita) espera o ciclo conjunto. O câmbio não lê os documentos do Copom: o que o Copom disse do câmbio e o condicionante chegam pela S3; nos testes solo o agente declara a lacuna em vez de escrever de memória (`cambio-analyst.md`).

## (II.III) Política monetária
    - i. Comunicados do Copom no vault, atualizados junto com o ETL. (feito 2026-09-30, 234 comunicados)
    - ii. Atas do Copom, todas, no vault, atualizadas junto com o ETL. (feito 2026-09-30, 261 atas, 1998–2026)
    - iii. RPM integral dos últimos 3 anos no vault. (feito 2026-09-30, 12 relatórios, dez/2023–set/2026)
    - iv. RPM integral do histórico. (estoque: só se promovido, I.III.xvi)
    - v. Ingerir os 46 PDFs de `repository/monetary_policy/raw_pdf/` (eram 35; 10 papers de prioridade alta entraram em 2026-10-07), pelo `/ingest monetary_policy` (II.I.iv). Lista e o que falta: a aba Qual - Monetary Policy de `repository/agent_mapping/data_tracker.xlsx`. (feito 2026-10-20: 64 fontes ingeridas, 53 com síntese; as 11 restantes só se caírem na camada 1 ou forem promovidas, I.III.xvi)
    - vi. Construir o mapa conceitual de política monetária, fechando as saídas e entradas com o de câmbio. Junto, a camada 1 e a fila de prioridade de PM. (pendente, `PLANO_AGENTES.md` Fase 2)
        - Donos das fontes da pasta de PM (decidido 2026-10-21, I.III.xvii): todas da PM, salvo Kohlscheen 2014, Tambakis & Tarashev 2012 e Kalemli-Ozcan 2019 (câmbio), Miranda-Agrippino & Rey 2020 (externo) e Calvo 1983 (inflação); BIS 2026 já era do câmbio. Ostry, Ghosh & Chamon 2012 e Rey 2013 ficam com a PM: a pergunta deles é a condução e a autonomia da política monetária.
        - Kalemli-Ozcan 2019 entra na camada 1 do câmbio e cobre o canal 2.3 (dólar global e Fed). Kohlscheen 2014 e Tambakis & Tarashev 2012 entram no fim da fila do câmbio (8 e 9).
        - Mapa: rascunho em `obsidian/monetary_policy/monetary_policy_conceptual_map.md` (2026-10-21). Partes 1 a 4 aprovadas no mesmo dia: perguntas Q1–Q4 (refeitas depois do primeiro teste), horizonte (III.III.i), saídas S1–S7 e entradas E1–E4. Ajustes do espelho com o câmbio: E3 (repasse) provisória no câmbio, a transferir para o agente de inflação quando ele existir (Fase 9); E7 mantém o cupom cambial, que entra nos dados com a API da Bloomberg (prevista para 01/11/2026); S4 engatilhada: enquanto o BC intervém só contra disfunção, a intervenção é do câmbio, que julga a disfunção; se a postura do BC passar a ser de defesa do câmbio, a função de reação, intervenção incluída, vira pergunta dos dois agentes, com foco na PM; S1 no formato de horizonte aprovado.
        - Camada 1 de PM (aprovada 2026-10-21), uma fonte por canal, todas com síntese: Svensson 1997 (2.1), Minella et al. 2002 (2.2), Minella et al. 2003 (2.3), Orphanides 2001 (2.4), Perrelli & Roache 2014 (2.5), Blanchard 2004 (2.6), Bogdanski, Tombini & Werlang 2000 (2.7), Obstfeld 2015 (2.8), Gürkaynak, Sack & Swanson 2005 (2.9), Bernanke & Gertler 1995 (2.10); o modelo mental da Verde de PM; os documentos do Copom pela regra de II.III.ix. Fila (camada 2, em ordem): Segura-Ubiergo 2012, Favero & Giavazzi 2004, Arida, Bacha & Lara-Resende 2005, Nakamura & Steinsson 2018, Taylor 1993, Holston, Laubach & Williams 2017, Havranek & Rusnak 2013, Mishkin 2000, Adrian, Crump & Moench 2013, Rey 2013, e depois os modelos mentais de PM da Kapitalo e da Kinea e outras janelas da Verde. O resto é camada 3, inclusive as 11 fontes sem síntese e o histórico do Copom. Marcado no tracker.
        - Primeiro teste solo do agente de PM (Fase 6, 2026-10-21, ciclo 2026-10-15, `politica_monetaria_r1.md`): report completo; abriu o mapa, comunicado, ata e RPM de set/26, a Verde, 4 conceitos e 1 síntese. Promovidos pelo "faltou" (decisão do usuário): Segura-Ubiergo 2012 (crédito direcionado, neutro) e Adrian, Crump & Moench 2013 (prêmio a termo) sobem para a camada 1. O resto do "faltou" (repasse do petróleo aos monitorados, dado eleitoral, calendário do Copom de 2028, expectativas Firmus/FGV) espera o ciclo conjunto.
    - vii. Modelos mentais de política monetária das gestoras (Verde, Kinea, Kapitalo), a partir das mesmas cartas.
        - Decidido (2026-10-21): por enquanto só a Verde, com as cartas do ciclo de aperto de 2021 e 2022 (~24 cartas), para ver que modelo ela aplicou naquele ciclo. Kinea, Kapitalo e outras janelas vão para a fila de PM.
        - Feito (2026-10-21): `verde_mp_mental_models.md`, 24 cartas em 3 rodadas, todas aprovadas pelo revisor (commits 50c1a1f, ce5d7e6, 14d91ac). A estrutura (4 blocos, 14 seções) ainda não foi revista pelo usuário.
    - viii. Modelos mentais do BC: uma linha histórica (o que não muda com o presidente) e uma da gestão atual. (a discutir; estoque até ser promovido, I.III.xvi)
    - ix. Síntese trimestral de comunicado + ata + RPM. (a discutir; o usuário marcou como discussão importante, adiada em 2026-10-20. Hoje 261 atas, 234 comunicados e 12 RPMs ficam fora do agente do vault. Na camada 1 do agente de PM (I.III.xvi): todos os comunicados, atas e RPMs publicados desde o início do mandato do Galípolo (2025-01-01) e antes da data do ciclo; hoje 14 comunicados e 14 atas (reuniões 268 a 281) e 7 RPMs (mar/2025 a set/2026). Decidido 2026-10-21; a data de início muda quando mudar o presidente do BC.)


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
        - Decidido (2026-10-22), substitui worst/best nos três itens acima, para todos os agentes: as caudas são **upside** (acima da central) e **downside** (abaixo), só posição, sem julgar se é bom ou ruim; a assimetria é P(upside) − P(downside). O report diz em texto se uma cauda é boa ou ruim para o Brasil quando isso importar. Motivo: a direção de "worst" era ambígua em vários casos (commodities, atividade com sinal oposto ao da inflação, expectativa desancorando para baixo, corte de imposto).
        - Riscos não são seção própria: entram na argumentação, justificando a probabilidade de cada cauda.
        - Central (2026-10-15): a do Modelo Estrutural no cenário base; a distribuição em torno dela é do agente (IV.ix).
        - Horizontes (2026-10-15, substitui curto, médio e longo prazo por agente): os trimestres do Modelo Estrutural, seis a partir do trimestre em curso (no ciclo de 07/10/2026, do 4T26 ao 1T28). A variável é medida no fechamento do trimestre (no câmbio, a PTAX do último dia útil), que é o que se compara com o dado de hoje.
            - A tese vira um caminho por trimestre. O dado que vai saindo é conferido contra a faixa de cada trimestre: um movimento que cai fora da faixa base mostra uma cauda se materializando naquele trimestre. Um movimento não mapeado é informação nova e dispara um ciclo.
            - Exceções são possíveis. Ex.: política monetária, cuja taxa no fim do trimestre sai das reuniões do Copom e do FOMC dentro dele.
            - Política monetária (decidido 2026-10-21): a variável é a meta Selic no fechamento de cada um dos seis trimestres (a decisão da última reunião dentro dele). Os dois primeiros trimestres saem também reunião a reunião, com a probabilidade de cada passo (manter, −25, −50 pb…); os seguintes no formato padrão. A central do modelo vem como Selic média do trimestre; o fechamento sai de uma conta fixa no `modelo.py`, a média deste trimestre e a do seguinte (erro médio de 0,12 p.p. contra a Selic real, 2006–2026), mecânica e não tempero. O caminho reunião a reunião dos dois primeiros trimestres é julgamento do agente, com a curva DI e a Focus, e forma a distribuição em volta da central. **A central é a do modelo em todos os trimestres.** Depois do primeiro teste solo chegou a valer uma exceção nos dois primeiros trimestres, desfeita no mesmo dia: ela partia de um passo máximo de 25 p.b. por reunião que o agente afirmou de memória e o ciclo de 2021–2022 desmente; e o corte do modelo tem leitura econômica (a NTN-B de 10 anos cai com o prêmio fiscal, o que precifica consolidação e menos demanda, mapa 2.5). **A revisar quando o plano terminar** (decisão do usuário, 2026-10-21): reestimar a regra de juros no fechamento seria o mais correto. Placar por trimestre e por reunião. Worst = Selic acima da central. O Fed Funds não é variável de tese: entra como caminho exógeno. Perguntas centrais (mapa de PM, Parte 1), refeitas no mesmo dia depois da revisão do primeiro report: o agente não descreve o Copom, confronta o que o Copom vai fazer (Q1), o que deveria fazer pelos dados (Q2) e o que o mercado precifica, com a sinalização do Copom como evidência (Q3); Q4 é a tese, e a distância entre Q1 e Q2 é risco.
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
    - v. Primeiro teste completo com câmbio + política monetária. É o ponto final do `PLANO_AGENTES.md` (Fase 8), rodado só com a camada 1 (I.III.xvi).
    - vi. Propostas sobre o modelo (decidido 2026-10-21, vale para todos os agentes): cada report tem a seção 6, "Sobre o modelo": o que a literatura lida sugere da especificação do Modelo Estrutural e o teste empírico que decidiria. O escrivão não a leva ao relatório; a sessão que conduz o ciclo junta as propostas aqui, e o usuário decide o que testar.
        - Do segundo teste solo de PM (ciclo 2026-10-15, `politica_monetaria_r1.md` §6), a decidir:
            - 1. Regra de juros (R) suavizando o **nível** da Selic em vez da distância Selic − âncora (Clarida-Galí-Gertler; Minella 2002): hoje a âncora `rr_10a` passa 1 para 1 no mesmo trimestre. Teste: estimar as duas formas de 2006 a 2026 e comparar erro fora da amostra e o impacto de `rr_10a`.
            - 2. Restringir a Selic média do trimestre de partida aos dias já decididos até a próxima reunião (no 4T26, 35 de 92 dias a 13,75%). Teste: erro do fechamento derivado, 2006–2026, com e sem a restrição.
            - 3. Âncora só com a parte da NTN-B explicada por fundamentos (CDS, juro real americano de 10 anos), separando prêmio a termo (Perrelli & Roache; Adrian, Crump & Moench). Teste: regredir `rr_10a` nesses fundamentos e reestimar (R) com ajustado e resíduo separados.
            - 4. Brent em reais (ou IC-Br energia) como regressor da equação de monitorados, com uma defasagem, e testar em bens industriais (RPM set/26, boxe do petróleo).
    - vii. Primeiro batch de sete agentes (decidido 2026-10-22, nas janelas de aprovação dos mapas):
        - Fronteiras:
            - o hiato do BC (`pm_hiato_produto` e as vintages) passa da PM para a atividade; na PM fica como o Copom lê o hiato e reage;
            - a atividade absorve o mercado de trabalho provisoriamente (`mt_pnad`, `mt_desocupacao_retro`, `mt_caged`, `mt_caged_setor`), até existir o agente dele;
            - as tabelas da Focus e do QPC são de expectativas, e os outros consultam; a PM continua concluindo sobre o caminho da Selic precificado (Q3 dela); a inflação esperada dos EUA (`expc_inflacao`) é do externo; a conclusão sobre a inflação implícita na curva é de expectativas, com a curva seguindo dado da PM;
            - commodities: Brent e IC-Br em dólar são do externo; o IC-Br em reais é da inflação;
            - o `clima_oni` fica fora das listas até algum job atualizá-lo.
        - O multiplicador de um coeficiente (tempero tipo (i)) é de quem é dono da equação: quem tem a tutela da exógena argumenta pela saída e o dono da equação aplica (ex.: o fiscal argumenta, o câmbio aplica no peso do CDS na (F)).
        - Inflação: a tese é o IPCA 12 meses no fechamento do trimestre; os quatro grupos aparecem só como decomposição da central, sem faixa própria (revisar depois do 1º ciclo). O `modelo.py` passa a devolver os quatro grupos.
        - Atividade: a tese é o hiato do BC por trimestre, com uma linha companheira de PIB interanual derivada mecanicamente (hiato do modelo + potencial implícito no hiato do BC). O placar do hiato é o primeiro RPM depois do PIB do IBGE daquele trimestre (a edição do fechamento do trimestre seguinte; decidido no mesmo dia, depois de a edição do próprio fechamento ter sido escolhida e o viés de revisão aparecer). Ideia do usuário para depois: um modelo que regride só a parte consolidada do hiato do BC (até dois ou três anos atrás, a de menor revisão esperada) contra PIB, desemprego, indústria e outros, e usa esses coeficientes para a frente. Ideia do usuário para depois: decompor o hiato em componentes (PIB, desemprego e outros), e então o hiato passaria a ser de mais de um agente.
        - Fiscal: a política fiscal tem duas discussões, (i) contábil (tamanho e composição da dívida, estrutura do orçamento, propostas do governo, medidas, resultados primário e nominal) e (ii) o impacto das medidas fiscais sobre a atividade e a inflação (crescimento das despesas, impulso, demanda do governo no PIB, a postura da política fiscal). As duas ficam registradas no mapa; o interesse agora é a (ii). As metas da regra fiscal não estão no banco: no 1º ciclo o agente declara a lacuna e compara com a Focus; depois, uma tabela declarativa no molde da `inflc_meta`.
        - Externo: um agente só, com três blocos obrigatórios em todo report, cada um com seção própria (política dos EUA, risco e dólar, commodities). A separação em dois agentes (EUA/condições globais × commodities) se decide pelo log do 1º ciclo. Cada exógena é medida na convenção em que o modelo a usa (`modelo.CONVENCAO`), e as teses vêm em três blocos de cenário.
        - Expectativas: a tese é a Focus IPCA 12 meses, medida pela média do trimestre (convenção do modelo). Q1 compara o nível de desancoragem com o histórico; Q2 lê as aberturas das expectativas de inflação e de PIB. O usuário registrou que ainda tem dúvidas sobre este agente.


# (IV) Decisões pendentes
    - i. Repasse cambial: câmbio ou inflação? Por ora o câmbio reporta (E1, E3 do mapa de câmbio).
        - Decidido (2026-10-21): a literatura de repasse é do agente de inflação (I.III.xvii). O câmbio a alcança pelo conceito de repasse e avisa a inflação quando vê risco relevante de depreciação. Até o agente de inflação existir, a literatura fica na camada 1 provisória dele, e o câmbio continua informando a PM pelas entradas E1 e E3.
    - ii. Como se forma a visão consolidada sobre um dado exógeno ou TWA: discussão entre os agentes ou um "economista-chefe" que calibra. E o que o agente faz com esse dado enquanto isso não estiver definido. (a discutir; para as exógenas, a intenção é distribuí-las a um ou dois agentes, I.III.ix)
        - A discutir na Fase 7 (usuário, 2026-10-21): quem escreve o caminho da NTN-B de 10 anos (`rr_10a`). É exógena no Modelo Estrutural e decide sozinha a central da Selic; a curva B3 é dado endógeno da PM, e o prêmio fiscal que a move não tem agente.
        - Decidido (2026-10-22), para as exógenas do Modelo Estrutural: a tutela de cada uma fica na aba "Exógenas" do `data_tracker.xlsx`, uma exógena por linha e os sete agentes nas colunas, com nível de 1 (decide) a 5; em branco, o agente não escreve o caminho. **Quem preenche é o usuário**, inclusive a `rr_10a`; a coluna "Proposta" é só sugestão. Agentes no mesmo nível têm o mesmo peso. A consolidação lê a aba (não há dono escrito em código).
        - Decidido (2026-10-22): as endógenas do modelo seguem a área: hiato → atividade, IPCA → inflação, expectativas → expectativas, Selic → PM, câmbio → câmbio.
        - Decidido (2026-10-22): quando um agente escreve para uma exógena um caminho diferente do de quem tem a tutela, o P usa o caminho de quem tem a tutela; a divergência vai para o log e é respondida na rodada seguinte. Se o argumento for bom, quem tem a tutela muda o caminho.
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
        - A função fixa que esse G chama (feito 2026-10-15: `analytics/agent_system/modelo.py`): recebe os caminhos das exógenas e os multiplicadores, devolve as endógenas por trimestre e a faixa do posterior. O retrato do simulador é gravado uma vez por ciclo, junto com o A.
        - Decidido (2026-10-22), a consolidação:
            - O P é uma rodada do modelo com o caminho base de cada exógena, vindo de quem tem a tutela dela (IV.ii; no empate, a média), sem multiplicadores: o multiplicador fica no tempero de cada agente.
            - Da rodada 2 em diante, a central de quem tem variável no modelo vem do P.
            - O PF* é a central conjunta mais a distribuição de cada agente.
            - Cada agente grava os caminhos base num JSON padrão, com as chaves do `modelo.CONVENCAO`.
            - Fiscal e externo, sem variável endógena no modelo: a tese é o caminho base das exógenas de que têm tutela, por trimestre, e a distribuição em volta também é deles. No futuro devem ganhar variáveis da área (usuário, 2026-10-22).
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
        - Estrutura do relatório (decidido 2026-10-22): por tema, com um apêndice por área. O cenário em uma página; o que move o cenário, em ordem causal; riscos (upside e downside); onde os analistas discordam; o que acompanhar; apêndice com uma tabela por variável. Detalhe no manual, seção 13.
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
*Grupos refeitos em 2026-10-22, com o primeiro batch de sete agentes (III.III.vii): o que era TWA e o CDS, que era exógeno, viraram endógeno do agente dono. As tabelas são as mesmas.*

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

### iii. Endógeno de expectativas (consulta; a posição vem pela saída S10 do mapa de câmbio)
    - `expc_focus_periodo` (câmbio): mediana da Focus para o câmbio no fim de cada ano. Mostra o que o consenso já espera, para separar surpresa de convergência.

    - `expc_focus_copom`: mediana da Focus para a Selic em cada reunião. É o carry futuro esperado pelo consenso, para comparar com a curva.

    - `expc_focus_periodo` (Selic): mediana da Focus para a Selic no fim de cada ano. Nível do carry esperado num horizonte mais longo que o das reuniões.

    - `expc_focus_periodo` (IPCA): mediana da Focus para o IPCA no fim de cada ano. É a inflação doméstica esperada que entra na paridade de poder de compra prospectiva, ao lado da meta.

### iv. Endógeno de externo (consulta; a posição vem pelas saídas S8–S9 do mapa de câmbio; o caminho das exógenas do bloco global vem de quem tem a tutela na aba Exógenas)
    - `cmb_dollar_index`: DXY, dólar contra moedas desenvolvidas, diário. Separa o ciclo global do dólar do que é do real (canal 2.3).

    - `cmb_dollar_index_em`: dólar contra moedas emergentes (FRED), diário desde 2006. Comparação mais próxima do real que o DXY, porque tira o efeito do euro e do iene.

    - `cmb_equity_us`: S&P 500, diário. Proxy do apetite a risco global, que move o real junto com os outros emergentes (canal 2.2).

    - `us_interest_rate`: só o Fed Funds e os Treasuries de 2 e 10 anos (2026-10-07). É a perna externa do carry; o de 10 anos move o ciclo global do dólar.

    - `cmb_real_rates`: juro real ex-post de BR, MX, CL, CO e PE. Compara o carry real do Brasil com o dos pares.

    - `comm_brent`: Brent em dólar, diário. O Brasil exporta petróleo, então o preço entra nos termos de troca e no saldo (canal 2.4).

    - `comm_icbr_usd`: IC-Br em dólar. Preço das commodities relevantes para o Brasil sem a variação cambial embutida: o insumo certo para explicar o real.

### v. Endógeno de inflação (consulta; a posição vem pela saída S5 do mapa de câmbio)
    - `inflc_agregados`: IPCA e seus componentes. Entra na inflação relativa da paridade de poder de compra e no câmbio real; o agente usa o número sem opinar sobre a inflação.

### vi. Endógeno de fiscal (consulta; a posição vem pelas saídas S6–S7 do mapa de câmbio; o multiplicador do peso do CDS na (F) é do câmbio, que é o dono da equação, III.III.vii)
    - `fisc_nfsp`: resultado primário e nominal do setor público em % do PIB, 12 meses. Esforço fiscal fraco eleva o prêmio de risco do real (canal 2.2).

    - `fisc_divida`: dívida bruta e líquida em % do PIB. A trajetória da dívida é o fundamento do prêmio de risco (canal 2.2).

    - `cmb_risco_pais`: CDS de 5 anos do Brasil. É o preço do risco soberano, par do real no canal de prêmio de risco (2.2), e a exógena `fiscal` da (F), cujo caminho vem de quem tem a tutela; a carga é por export manual da Bloomberg, então conferir a data do último dado antes de usar.

### vii. Endógeno de atividade (consulta; sem saída fixa: o câmbio só usa o número como denominador)
    - `atv_pib_usd`: PIB mensal em dólar. É o denominador do balanço de pagamentos em % do PIB.

## (V.II) Agente de política monetária
*Lista aprovada pelo usuário em 2026-10-21, com as 68 tabelas abaixo (I.III.xvi: os dados ficam fora das camadas por ora; reavaliar depois do teste solo). Grupos refeitos em 2026-10-22, com o primeiro batch de sete agentes (III.III.vii): o hiato do BC passou para a atividade, o que era TWA virou endógeno do agente dono (salvo o crédito, que ainda não tem agente) e o CDS, que era exógeno, foi para o fiscal. As tabelas são as mesmas.*

### i. Endógeno
    - `pm_copom_calendario`: calendário oficial das reuniões, inclusive as do ano seguinte. Situa cada leitura no ciclo e permite ler Focus e curva reunião a reunião.

    - `pm_copom_reuniao`: Selic decidida e passo, por reunião. É o histórico de decisões que, junto com as projeções, revela a função de reação.

    - `pm_copom_projecoes`: projeções de inflação do Copom (referência e alternativas), dos comunicados e do RPM. É a variável que o Copom persegue; o desvio dela para a meta no horizonte relevante explica a decisão.

    - `br_interest_rate`: curva de juros da B3 nos vértices padrão, com a Selic. Mostra o juro nominal e real que o mercado precifica; o juro real é a medida de quão restritiva está a política.

    - `br_di_grade`: curva DI com todos os vértices. Dá a Selic implícita reunião a reunião, para comparar com a Focus e com a sinalização do Copom.

    - `inflc_meta`: meta de inflação do CMN. É a âncora contra a qual projeções e expectativas são medidas; dado institucional, não leitura de inflação.

### ii. Endógeno de câmbio (consulta; a posição vem pelas entradas E1, E2 e E4–E7 do mapa de câmbio; a E3, repasse, passou para a inflação)
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

### iii. Endógeno de expectativas (consulta; a posição vem pela saída S9 do mapa de PM; a conclusão sobre o caminho da Selic que a curva precifica continua da PM, Q3)
    - `expc_focus_copom`: mediana da Focus para a Selic em cada reunião. É o caminho esperado pelo consenso; a diferença para a curva é prêmio, a diferença para a comunicação é espaço de surpresa.

    - `expc_focus_periodo` (Selic): mediana da Focus para a Selic no fim de cada ano. Nível do juro esperado num horizonte mais longo que o das reuniões.

    - `expc_qpc`: Questionário Pré-Copom: o que o mercado acha que o Copom fará e deveria fazer, o balanço de riscos, o hiato do mercado e as projeções de IPCA (curto prazo e horizonte relevante, em percentis). Mostra o consenso às vésperas da reunião e onde ele discorda do BC, inclusive sobre a inflação no horizonte relevante.

    - `expc_focus`: expectativa de inflação 12 e 24 meses à frente. É a expectativa que o Copom cita em todo comunicado.

    - `expc_focus_periodo` (IPCA): expectativa de IPCA por ano-calendário. Mostra o que o mercado espera para a inflação em cada ano do horizonte relevante.

    - `expc_focus_periodo` (câmbio): câmbio esperado pelo consenso. A distância para a premissa do Copom é um dos riscos do cenário de referência; a leitura do câmbio continua vindo do agente de câmbio (E4).

### iv. Endógeno de inflação (consulta; a posição vem pelas saídas S3 e S8 do mapa de PM)
    - `inflc_agregados`: IPCA e IPCA-15 com componentes, difusão e núcleos. É a inflação corrente que o Copom lê, em especial serviços subjacentes e núcleos, que mostram a persistência.

    - `inflc_decomposicao`: IPCA por subitem, com peso e contribuição. Separa choque pontual (alimentos, energia) de pressão disseminada, a distinção que decide se o Copom reage.

    - `inflc_decomposicao_item`: a mesma decomposição por item. Mostra se o movimento de um grupo vem de um item ou de vários.

    - `inflc_dim`: classificação analítica do BC para cada subitem. Permite reconstruir os mesmos recortes que a ata cita (serviços subjacentes, industriais, alimentação no domicílio).

    - `comm_icbr`: IC-Br em reais e sub-índices. Pressão das commodities sobre alimentos e energia já com o câmbio embutido, que é a forma em que ela chega ao IPCA.

### v. Endógeno de atividade (consulta; a posição vem pela saída S10 do mapa de PM; inclui o hiato do BC e, provisoriamente, o mercado de trabalho, III.III.vii)
    - `pm_hiato_produto`: hiato do produto do BCB na última edição do RPM. É a ociosidade que entra na projeção do BC; a diferença para o hiato do mercado (QPC) é fonte de divergência sobre o juro. O caminho do hiato é da atividade; na PM fica como o Copom lê o hiato e reage.

    - `pm_hiato_produto_vintages`: todas as estimativas de hiato já publicadas. Revisão do hiato muda a projeção sem que o dado do mês mude, e por isso explica mudanças de postura que os dados correntes não explicam.

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

    - `mt_pnad`: desocupação, ocupação, rendimento e massa salarial. Mede a folga do mercado de trabalho e o crescimento da renda, que alimenta a inflação de serviços.

    - `mt_desocupacao_retro`: desocupação dessazonalizada retropolada pelo BCB, desde 2004. É a série que o BC usa, longa o bastante para comparar o nível atual com o histórico.

    - `mt_caged`: estoque de emprego formal. Sinal mensal do ciclo, mais rápido que a PNAD.

    - `mt_caged_setor`: saldo de empregos por setor. Mostra se o emprego cresce em serviços, onde a pressão salarial chega mais direto à inflação.

### vi. TWA — crédito
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

### vii. Endógeno de fiscal (consulta; a posição vem pelas saídas S11–S12 do mapa de PM; inclui o CDS)
    - `fisc_nfsp`: resultado primário, nominal e juros em % do PIB, 12 meses. Política fiscal expansionista estimula a demanda e exige juro mais alto para o mesmo resultado de inflação.

    - `fisc_divida`: dívida bruta e líquida em % do PIB. A trajetória da dívida afeta o prêmio de risco e as expectativas, e por aí o juro neutro.

    - `fisc_dlsp_fatores`: o que explica cada variação da dívida líquida. Mostra quanto do crescimento da dívida é o custo da própria Selic.

    - `fisc_rtn`: resultado do governo central, mensal. Mostra o cumprimento do arcabouço, a base da "política fiscal crível" que o Copom menciona.

    - `fisc_efgg`: estatísticas fiscais do governo geral pela classificação do FMI, trimestral. É a base para medir o impulso fiscal, o estímulo à demanda que o Copom pondera.

    - `cmb_risco_pais`: CDS de 5 anos do Brasil. Termômetro da percepção de risco que o Copom cita e que chega ao juro longo e ao câmbio; o caminho vem de quem tem a tutela da exógena `fiscal` na aba Exógenas. Conferir a data do último dado, a carga é manual.

### viii. Endógeno de externo (consulta; a posição vem pela saída S13 do mapa de PM; o caminho do Fed Funds e das outras exógenas do bloco global vem de quem tem a tutela na aba Exógenas)
    - `us_interest_rate`: curva do Treasury e meta do Fed. O juro americano condiciona o espaço para o diferencial de juros e o apetite por emergentes.

    - `inter_interest_rate`: taxa de política dos pares latinos. Mostra o ciclo dos outros BCs, referência para quanto o Copom pode se afastar.

    - `cmb_real_rates`: juro real ex-post dos pares. Compara o grau de restrição da política brasileira com o dos pares.

    - `cmb_dollar_index`: DXY. Condição financeira global, que o Copom descreve como cenário externo.

    - `cmb_dollar_index_em`: dólar contra emergentes. Mostra se a pressão sobre moedas emergentes é generalizada.

    - `comm_brent`: Brent em dólar. Choque de oferta que chega aos combustíveis e aos preços administrados; o Copom olha os efeitos secundários, não o choque.

    - `comm_icbr_usd`: IC-Br em dólar e sub-índices (acrescentado 2026-10-21). Os índices agro e metal em dólar são exógenas do Modelo Estrutural, na curva de Phillips; o caminho deles vem de quem tem a tutela na aba Exógenas.

### ix. Fora da lista (consulta livre, sem uso previsto)
    - `mt_pnad_trimestral`, `mt_caged_uf`, `mt_caged_salario`, `cred_credito_porte`, `cred_credito_atividade_economica`, `cred_credito_tipo_cliente`, `fisc_investimento`: cortes estruturais, regionais ou de detalhe que não mudam a leitura do juro.

## (V.III) Agente de inflação
*Lista aprovada pelo usuário em 2026-10-22 (janela de aprovação do mapa). Escrita pelo subagente do agente.*

### i. Endógeno
    - `inflc_agregados`: IPCA e IPCA-15, os quatro grupos do BC, livres, comercializáveis e não comercializáveis, núcleos, difusão e o IPCA de 12 meses (SGS). É a inflação que o agente explica: o cheio contra os núcleos e a difusão separa choque de tendência (canal 2.1); a série longa sustenta a leitura de inércia (2.2).

    - `inflc_indice_geral`: o IPCA e o IPCA-15 como o IBGE publica (número-índice, mês, ano, 12 meses). Dá o acumulado exato de qualquer janela e chega antes do SGS no dia da divulgação; é a fonte do placar (12 meses do último mês do trimestre).

    - `inflc_decomposicao`: IPCA e IPCA-15 por subitem, com variação, peso e contribuição. Mostra se a pressão vem de poucos itens ou de muitos (2.1) e acompanha os administrados um a um: gasolina, diesel, gás, energia, plano de saúde, remédios, transporte (2.7).

    - `inflc_decomposicao_item`: a mesma decomposição por item. Base dos núcleos de médias aparadas e dupla ponderação, e leitura de qual item move um grupo.

    - `inflc_dim`: a classificação do BC de cada subitem (monitorado ou livre; alimentação, industriais, serviços; serviços subjacentes; comercializável; marcas de núcleo). Reconstrói os mesmos quatro grupos do Modelo Estrutural e os recortes que a ata cita.

    - `comm_icbr`: IC-Br em reais e os subíndices agropecuária, metal e energia. É a forma em que commodities e câmbio chegam juntos ao IPCA: alimentos, industriais e combustíveis (2.5, 2.6, 2.7).

### ii. Endógeno de câmbio (consulta; a posição vem pelas saídas IN-S1–IN-S2 do mapa de inflação)
    - `cmb_ptax`: câmbio diário. É o insumo do repasse a alimentos e industriais (2.5); se o movimento é persistente e qual o caminho vêm do agente de câmbio.

### iii. Endógeno de política monetária (consulta; a posição vem pelas saídas IN-S3–IN-S4)
    - `inflc_meta`: meta de inflação do CMN. É a âncora contra a qual a tese e as expectativas são lidas (2.3).

    - `pm_copom_projecoes`: projeções de IPCA, livres e administrados do Copom (referência e alternativas), por trimestre. É o termo de comparação da Q4; os condicionantes por trás delas chegam pela IN-S4.

### iv. Endógeno de atividade (consulta; a posição vem pela saída IN-S5)
    - `pm_hiato_produto`: hiato do produto do BCB. É o canal de demanda de serviços e industriais (2.4); o caminho vem do agente de atividade.

    - `atv_pms`: volume de serviços. Mostra se a demanda em serviços acompanha o hiato, o grupo mais persistente (2.4).

    - `mt_pnad`: desocupação, rendimento real habitual e massa salarial. Salário acima da produtividade pressiona serviços (2.4); entra só pelo que o hiato não carrega.

    - `mt_desocupacao_retro`: desocupação dessazonalizada do BCB desde 2004. Folga do mercado de trabalho contra o histórico (2.4).

    - `mt_caged`: emprego formal mensal. Sinal mais rápido do ciclo de serviços (2.4).

### v. Endógeno de expectativas (consulta; a posição vem pelas saídas IN-S9–IN-S10)
    - `expc_focus`: Focus do IPCA 12 e 24 meses à frente, os cinco componentes (livres, administrados, serviços, bens industrializados, alimentação no domicílio) e o IGP-M. A expectativa do cheio é a âncora dos quatro grupos no modelo (2.3); os componentes mostram onde o mercado espera mudança de preço relativo.

    - `expc_focus_periodo` (IPCA): Focus do IPCA por ano-calendário. Termo de comparação da Q4 ano a ano.

    - `expc_focus_periodo` (componentes): Focus por ano-calendário dos cinco componentes do IPCA e do IGP-M. Onde o mercado põe a inflação de cada grupo no horizonte; o IGP-M esperado indica a pressão sobre aluguéis e contratos indexados (2.2, 2.3).

    - `expc_qpc`: projeções de IPCA do mercado antes de cada Copom (curto prazo, núcleos, serviços subjacentes, horizonte relevante, balanço de riscos). Comparação com a tese no curto prazo e no horizonte relevante.

### vi. Endógeno de externo (consulta; a posição vem pelas saídas IN-S7–IN-S8)
    - `comm_icbr_usd`: IC-Br em dólar e subíndices agro, metal e energia. Agro e metal são exógenas da curva de Phillips (alimentação e industriais, 2.6); o caminho vem de quem tem a tutela na aba Exógenas.

    - `comm_brent`: Brent em dólar, diário. Fora do modelo; chega aos combustíveis e aos administrados, tempero (ii) (2.7).

## (V.IV) Agente de atividade
*Lista aprovada pelo usuário em 2026-10-22 (janela de aprovação do mapa). Escrita pelo subagente do agente.*

### i. Endógeno
    - `atv_pib`: PIB trimestral em índice de volume dessazonalizado, oferta e demanda. É a medida do nível de atividade e da composição que o agente explica (Q1, Q2).

    - `atv_pib_taxas`: taxas oficiais do PIB e dos componentes (contra o trimestre anterior, interanual, em quatro trimestres). A interanual é a linha companheira da tese e o número conferido no placar.

    - `atv_pib_valores_correntes`: PIB a preços correntes por componente. Dá o peso de cada componente da demanda, para a contribuição ao crescimento.

    - `atv_pib_mensal`: PIB nominal mensal e de 12 meses. Denominador das razões em % do PIB (crédito, impulso fiscal).

    - `atv_ibcbr`: IBC-Br, total, ex-agropecuária e por setor. Leitura mensal do ciclo entre dois PIBs; o ex-agro separa o ciclo do choque de safra (2.7).

    - `atv_pim`: produção industrial por seção. Ciclo do setor mais sensível ao juro e ao câmbio; a extrativa separa choque de oferta (2.1, 2.7).

    - `atv_pim_uso`: produção industrial por categoria de uso. Bens de capital antecipam o investimento (2.6); duráveis respondem primeiro ao aperto (2.1).

    - `atv_pmc`: volume do varejo restrito e ampliado, por segmento. Consumo de bens; veículos e móveis e eletrodomésticos são onde o crédito e a Selic aparecem primeiro (2.1, 2.2).

    - `atv_pms`: volume de serviços por segmento. O maior setor da economia e o elo da atividade com a inflação de serviços.

    - `atv_renda_poupanca`: renda nacional, poupança e capacidade de financiamento. Separa renda de produto (termos de troca, 2.5) e mede poupança e formação de capital (2.6, 2.8).

    - `pm_hiato_produto`: hiato do produto do BC na edição corrente do RPM, central e dispersão entre modelos. É a variável da tese, o ponto de partida do modelo e a série em que a (H) foi estimada (2.8).

    - `pm_hiato_produto_vintages`: todas as edições do hiato. Mostra a revisão que move o ponto de partida sem dado novo e é a base do placar (a edição do fechamento de cada trimestre); só a central é comparável entre as edições de 2024-06 e 2024-09.

    - `mt_pnad`: desocupação, participação, rendimento real e massa salarial, Brasil (provisório, até existir o agente de mercado de trabalho). A massa salarial real move o consumo (2.4), e a desocupação é a checagem observada da folga (2.8).

    - `mt_desocupacao_retro`: desocupação dessazonalizada retropolada pelo BC, desde 2004 (provisório). Série longa para comparar a folga de hoje com o histórico e com a NAIRU do mercado.

    - `mt_caged`: estoque de emprego formal, total e por setor (provisório). Sinal mensal do ciclo, mais rápido que a PNAD.

    - `mt_caged_setor`: saldo de empregos por seção CNAE (provisório). Mostra onde o emprego cresce ou para.

### ii. Endógeno de política monetária (consulta; a posição vem pelas saídas S-PM1–S-PM3 do mapa)
    - `br_interest_rate`: Selic e NTN-B de 2 e 10 anos. A NTN-B de 10 anos é a âncora do aperto da (H) e, fora do modelo, o custo de capital do investimento (2.1, 2.6).

    - `pm_copom_reuniao`: Selic decidida e passo, por reunião. É a Selic que vira o aperto do trimestre seguinte na (H).

    - `inflc_meta`: meta de inflação do CMN. Terceira peça do aperto da (H).

### iii. Endógeno de câmbio (consulta; S-CB1–S-CB2)
    - `cmb_ptax`: câmbio diário. O câmbio real muda a competitividade dos comercializáveis e a renda real (2.5).

    - `cmb_termos_troca`: termos de troca da Funcex. Ganho de renda além do produto (2.5).

    - `cmb_comex_produto`: exportação das principais commodities. Separa preço de volume, e safra de ciclo (2.5, 2.7).

    - `cmb_comex_pais`: exportação e importação por parceiro. Por onde chega o choque de demanda externa (2.5).

### iv. Endógeno de inflação (consulta; S-IN1–S-IN2)
    - `inflc_agregados`: IPCA, livres, serviços e alimentação. Deflator da renda real (2.4), e serviços como o sinal do hiato nos preços (2.8).

    - `comm_icbr`: IC-Br em reais e subíndices. A renda agrícola e mineral em reais, que é a que o produtor recebe (2.5, 2.7).

### v. Endógeno de fiscal (consulta; S-FI1–S-FI2)
    - `fisc_efgg`: governo geral pela classificação do FMI, trimestral. Base do impulso fiscal, a demanda do governo (2.3).

    - `fisc_rtn`: resultado do governo central, mensal. Despesa e transferências que viram renda das famílias (2.3, 2.4).

    - `fisc_nfsp`: resultado primário e nominal em % do PIB, 12 meses. A direção da política fiscal (2.3).

    - `cmb_risco_pais`: CDS de 5 anos do Brasil. Prêmio de risco e condições financeiras; o efeito que passa pelo juro de 10 anos já está no modelo e não entra de novo (2.2, 2.3).

### vi. Endógeno de externo (consulta; S-EXT1–S-EXT3)
    - `comm_icbr_usd`: IC-Br em dólar e subíndices. Renda das commodities e investimento extrativo, que chegam à atividade fora do modelo (2.5).

### vii. Endógeno de expectativas (consulta; S-EXP1–S-EXP2)
    - `expc_focus_periodo` (PIB): mediana da Focus para o PIB, trimestral e anual, com os componentes. O consenso, para separar surpresa de convergência (Q1, Q4).

    - `expc_focus_periodo` (desocupação): mediana da Focus para a taxa de desocupação. O consenso para a folga do mercado de trabalho (Q3).

    - `expc_qpc`: Questionário Pré-Copom: PIB trimestral, hiato, balanço de riscos do PIB, PIB potencial e NAIRU. O hiato do mercado contra o do BC, e o potencial e a NAIRU para medir a folga (Q3, 2.8).

### viii. TWA — crédito
    - `cred_credito_resumo`: concessões, taxas, spread e inadimplência, por recurso e segmento. A transmissão pelo preço do crédito (2.2).

    - `cred_fluxo_financeiro`: impulso de crédito no conceito do RPM. O mesmo número que o BC usa ao falar de condições financeiras (2.2).

    - `cred_ptc`: oferta e demanda de crédito na leitura dos bancos. Antecede o que os saldos só mostram depois (2.2).

    - `cred_credito_familias`: endividamento e comprometimento de renda das famílias. Quanto o consumo aguenta (2.4).

    - `cred_credito_amplo`: crédito ao setor não financeiro, com títulos e dívida externa. Financiamento do investimento fora dos bancos (2.6).

    - `cred_modalidade_livre_pf`: crédito livre à pessoa física por modalidade. Onde o aperto aparece primeiro no consumo (2.2).

    - `cred_modalidade_livre_pj`: crédito livre à pessoa jurídica por modalidade. Capital de giro (2.2).

    - `cred_modalidade_direcionado_pj`: crédito direcionado à pessoa jurídica, inclusive BNDES. Investimento pouco sensível à Selic (2.2, 2.6).

*Fora da lista (consulta livre, sem uso previsto): atv_pib_usd (denominador do balanço de pagamentos, lido pelo câmbio), mt_pnad_trimestral, mt_caged_uf, mt_caged_salario, os outros cortes de crédito, fisc_divida, fisc_investimento, comm_brent. O clima_oni fica fora até algum job atualizá-lo.*

## (V.V) Agente fiscal
*Lista aprovada pelo usuário em 2026-10-22 (janela de aprovação do mapa). Escrita pelo subagente do agente.*

### i. Endógeno
    - `fisc_rtn`: resultado do governo central por rubrica, mensal, acima da linha. Receita e despesa por grupo (benefícios, pessoal, discricionárias, subsídios), a base do crescimento real das despesas e do impulso (2.1, 2.2) e o objeto da regra fiscal (2.7).

    - `fisc_efgg`: governo geral pela classificação do FMI, trimestral, por esfera. O gasto por natureza econômica que chega à demanda (benefícios, remuneração, uso de bens e serviços, investimento): base do impulso medido pela despesa (2.1, 2.2, 2.3).

    - `fisc_investimento`: investimento do governo federal por GND, função e natureza, mensal. A parte do gasto que entra na demanda e no potencial e que costuma ser a primeira a ser cortada (2.1).

    - `fisc_nfsp`: resultado primário, juros nominais e resultado nominal do setor público em % do PIB em 12 meses, por esfera, e o fluxo mensal do primário. A variação do primário é o impulso medido abaixo da linha (2.2); o nível é o esforço fiscal (2.7). Negativo é déficit.

    - `fisc_dlsp_fatores`: o que explica cada variação da dívida líquida, por item. Separa r − g do primário e dos ajustes (2.8) e traz o crédito do Tesouro às instituições financeiras oficiais, o canal parafiscal (2.5). Sinal oposto ao da NFSP: fluxo positivo aumenta a dívida.

    - `fisc_divida`: dívida bruta e líquida em % do PIB, total e por esfera. A trajetória que o prêmio de risco precifica (2.8, 2.9).

    - `cmb_risco_pais`: CDS de 5 anos do Brasil, diário. É a exógena `fiscal` do Modelo Estrutural e a variável da tese, conforme a tutela na aba Exógenas (2.9); carga manual, conferir a data do último dado.

### ii. Endógeno de atividade (consulta; FS-AT1–FS-AT2)
    - `pm_hiato_produto`: hiato do produto do BC na edição corrente do RPM. Corrige o primário pelo ciclo para medir o impulso, e é onde o impulso chega (2.2, 2.4).

    - `atv_pib`: PIB trimestral em volume dessazonalizado, com consumo do governo e FBCF. A demanda do governo no PIB, a checagem do impulso pelas contas nacionais (2.3).

    - `atv_pib_taxas`: crescimento real do PIB e dos componentes. O padrão contra o qual se mede o crescimento real das despesas e o g de r − g (2.1, 2.8).

    - `atv_pib_valores_correntes`: PIB trimestral a preços correntes por componente. O peso do governo no PIB e o denominador da EFGG (2.3).

    - `atv_pib_mensal`: PIB nominal mensal e em 12 meses. Denominador de todo % do PIB (2.2, 2.8).

### iii. Endógeno de inflação (consulta; FS-IN1–FS-IN2)
    - `inflc_agregados`: IPCA e monitorados. Deflaciona a despesa (2.1); os monitorados mostram decisões de governo que chegam direto aos preços (2.4); indexa receita, despesa e dívida (2.8).

### iv. Endógeno de política monetária (consulta; FS-PM1–FS-PM4)
    - `pm_copom_reuniao`: Selic decidida por reunião. A metade monetária do policy mix e o custo da dívida pós-fixada (2.6, 2.8).

    - `br_interest_rate`: Selic, curva DI e curva real das NTN-B. O juro real de 10 anos carrega o prêmio fiscal e é a `rr_10a` do modelo (2.9, 2.10); a inflação implícita, por um G, é sinal de dominância fiscal (2.12).

### v. Endógeno de câmbio (consulta; FS-CB1–FS-CB2)
    - `cmb_ptax`: câmbio diário. Move a dívida líquida pelo ajuste de paridade (2.8); se o real precifica estresse fiscal é leitura do câmbio (2.9).

    - `cmb_reservas_bc`: reservas e swaps do BC. As reservas separam a dívida líquida da bruta; o resultado dos swaps passa pelo resultado nominal (2.8).

    - `cmb_fx_latam`: moedas dos pares latinos. Sem CDS dos pares na base, o real contra os pares separa o prêmio fiscal do movimento global (2.9).

### vi. Endógeno de expectativas (consulta; FS-EP1–FS-EP2)
    - `expc_focus_periodo` (fiscal): mediana da Focus para o resultado primário, o resultado nominal, as dívidas líquida e bruta e o consumo do governo, por ano. O consenso fiscal, para separar surpresa de convergência e comparar o primário na falta das metas da regra (2.4, 2.7, 2.8).

    - `expc_focus_periodo` (IPCA): mediana da Focus para o IPCA por ano. A expectativa longa que desancora com notícia fiscal é sinal de dominância (2.12).

    - `expc_qpc`: Questionário Pré-Copom. A percepção do mercado sobre a situação fiscal desde o último Copom (2.7).

### vii. Endógeno de externo (consulta; FS-EX1–FS-EX3)
    - `us_interest_rate`: Fed Funds e Treasuries de 2 e 10 anos. O componente global do juro real longo (2.10).

    - `cmb_equity_us`: S&P 500. Proxy do apetite a risco global, o componente global do CDS (2.9).

    - `cmb_dollar_index_em`: dólar contra emergentes. Mostra se a pressão sobre os emergentes é generalizada (2.9).

    - `comm_brent`: Brent em dólar. Royalties e dividendos de estatais na receita (2.7).

### viii. TWA — crédito
    - `cred_credito_controle_capital`: crédito por controle do banco (público, privado, estrangeiro). A expansão dos bancos públicos é estímulo parafiscal (2.5).

    - `cred_modalidade_direcionado_pj`: crédito direcionado à pessoa jurídica, inclusive BNDES. Mesma leitura (2.5).

    - `cred_modalidade_direcionado_pf`: crédito direcionado à pessoa física (imobiliário, rural). Mesma leitura (2.5).

    - `cred_credito_resumo`: saldo, concessões, taxas e inadimplência, livre e direcionado. A fatia do crédito fora da taxa de mercado (2.5).

*Fora da lista (consulta livre, sem uso previsto): os outros cortes de crédito, `pm_hiato_produto_vintages`, `atv_renda_poupanca`. As metas da regra fiscal não estão no banco: no 1º ciclo o agente declara a lacuna e compara com a Focus.*

## (V.VI) Agente externo
*Lista aprovada pelo usuário em 2026-10-22 (janela de aprovação do mapa). Escrita pelo subagente do agente.*

### i. Endógeno
    - `us_interest_rate`: meta do Fed (ponto médio) e os 11 vértices do Treasury, na variante "curva completa". A ponta curta é o caminho do Fed que o mercado precifica (Q1); a longa é o juro de desconto global e o prêmio a termo (canal 2.2).

    - `diferenciais_juros` (EUA): só as séries americanas: Fed Funds efetivo, CPI 12 meses e juro real ex-post dos EUA. O Fed Funds efetivo daqui é o `ffr` do modelo, na convenção do último mês do trimestre; o diferencial continua sendo do câmbio.

    - `inflc_cpi`: CPI-U dos EUA (cheio, núcleo, bens, serviços, habitação, alimentação, energia). É a fonte do `infl_us` do modelo e a leitura da persistência da inflação americana (canal 2.3).

    - `inflc_pce`: PCE e núcleo, a medida que o Fed persegue. Diz como o Fed lê a inflação (canal 2.1).

    - `expc_inflacao`: estrutura a termo da inflação esperada dos EUA (Cleveland Fed), de 1 a 30 anos. Mede a ancoragem do objetivo do Fed e, por G, o juro real ex-ante (canais 2.1 e 2.2).

    - `mt_ces`: payroll (emprego total e privado, salário por hora). Mede a folga do mercado de trabalho e os salários, insumos da função de reação do Fed (canais 2.1 e 2.3).

    - `mt_cps`: pesquisa domiciliar (desemprego, U-6, participação). A taxa de desemprego é o outro mandato do Fed.

    - `mt_jolts`: vagas, contratações e pedidos de demissão. Mede o aperto do mercado de trabalho e antecede os salários.

    - `cmb_dollar_index`: DXY. Separa o ciclo do dólar contra desenvolvidos (euro e iene) do ciclo contra emergentes (canal 2.4).

    - `cmb_dollar_index_em`: dólar contra emergentes (FRED). É o `dxy_em` do modelo, em fechamento (canal 2.4).

    - `cmb_equity_us`: S&P 500. É o `sp500` do modelo e a proxy do apetite a risco global (canal 2.5).

    - `comm_icbr_usd`: IC-Br em dólar, total, agropecuária, metal e energia. São o `icbr_usd`, o `icbr_agr_usd` e o `icbr_met_usd` do modelo; a energia ajuda a montar o total (canal 2.6).

    - `comm_brent`: Brent em dólar, diário. Caminho da energia, que fica fora do modelo e chega à inflação (combustíveis, monitorados); dado por este agente para o ciclo não ter dois caminhos de petróleo.

    - `inter_interest_rate`: juro de política de México, Chile, Colômbia e Peru. Mostra o ciclo dos pares e se o movimento do Brasil é comum ou próprio (canal 2.7).

    - `cmb_real_rates`: juro de política, inflação 12 meses e juro real ex-post de BR, MX, CL, CO e PE, num método só. Compara o grau de restrição dos pares e o do Brasil (canal 2.7).

### ii. Endógeno de câmbio (consulta; a posição vem pelas saídas XS1–XS2 do mapa externo)
    - `cmb_fx_latam`: moedas dos pares latinos. Grupo de comparação do global × idiossincrático, que é do câmbio (XS1).

    - `cmb_cot_fx`: posição em futuros de BRL e MXN. Evidência de que o apetite a risco chega ao Brasil por dinheiro, não só por preço (XS2).

    - `cmb_termos_troca`: termos de troca da Funcex. A consequência, no Brasil, do caminho das commodities (canal 2.6).

    - `cmb_comex_pais`: exportação por parceiro (China, EUA). A única janela para a demanda chinesa, que não tem dado no banco (canal 2.6).

### iii. Endógeno de fiscal (consulta; a posição vem pela saída XS5; o externo tem a palavra sobre o componente global, I.III.ix)
    - `cmb_risco_pais`: CDS de 5 anos do Brasil. É onde o risco global e o fiscal se encontram; o caminho é do fiscal, e o externo diz quanto do movimento é global. Conferir a data do último dado, a carga é manual.

### iv. Endógeno de expectativas (consulta; a posição vem pela saída XS8)
    - `expc_qpc`: o bloco de ambiente externo do Questionário Pré-Copom. É o consenso contra o qual o cenário externo é visão ou surpresa.

*Sem TWA (crédito e mercado de trabalho do Brasil não mudam a leitura externa) e sem exógeno (o CDS é do fiscal). Fora da lista (consulta livre, sem uso previsto): `inflc_cpi_dim`, `inflc_cpi_pesos`, `inflc_pce_dim`, `mt_ces_dim`, `mt_jolts_dim` (hierarquias e pesos, que o F usa e o agente não lê), `mt_produtividade` (produtividade e custo unitário do trabalho, profundidade que a forma mínima dispensa) e `cmb_reer` (do câmbio). `comm_icbr` (em reais) é da inflação e `clima_oni` fica fora de todas as listas.*

## (V.VII) Agente de expectativas
*Lista aprovada pelo usuário em 2026-10-22 (janela de aprovação do mapa). Escrita pelo subagente do agente.*

### i. Endógeno
    - `expc_focus` (inflação): expectativa de horizonte móvel do IPCA e dos cinco componentes (livres, administrados, serviços, bens industrializados, alimentação no domicílio), a 12 e 24 meses, suavizada e não suavizada, nas bases de 30 dias e de 4 dias úteis, com mediana, média, desvio-padrão, mínimo, máximo e respondentes. A IPCA 12 meses suavizada, base de 30 dias, é a variável da tese e a `pi_e` do Modelo Estrutural; a 24 meses e os componentes mostram em que horizonte e em que preços a expectativa anda; a base de 4 dias úteis adianta a revisão que a de 30 dias ainda não mostra (canais 2.1, 2.4, 2.5, 2.7, 2.9).

    - `expc_focus_periodo` (inflação): IPCA e os cinco componentes por período fixo (mês, trimestre e ano-calendário, até o último ano perguntado), com as cinco estatísticas e os respondentes. Os anos longos são onde se julga a ancoragem e a posição dela no histórico (Q1); a história da revisão de um período fixo mostra quanto e em que componente a pesquisa revisou (canais 2.2, 2.5, 2.7, 2.9).

    - `expc_focus_periodo` (PIB): PIB total, por setor (agropecuária, indústria, serviços) e por componente da demanda (consumo das famílias e do governo, investimento, exportação, importação), anual e trimestral. A abertura da atividade esperada pela pesquisa, para ver se a inflação esperada é coerente com o crescimento esperado e de onde ele vem (Q2, canal 2.9); a leitura da atividade em si é do agente de atividade.

    - `expc_focus_periodo` (Selic): Selic esperada no fim de cada ano. Com o IPCA esperado do mesmo ano dá o juro real esperado e o teste de coerência da pesquisa (Q3, canal 2.8).

    - `expc_focus_periodo` (câmbio): câmbio esperado no fim de cada ano. Só como o câmbio que a pesquisa supõe ao formar a inflação esperada; a leitura do câmbio é do agente de câmbio (canal 2.4).

    - `expc_focus_copom`: Selic esperada em cada reunião do Copom. O caminho de juros que o consenso espera, para o teste de credibilidade (Q3, canal 2.8); o caminho que a curva precifica é conclusão da política monetária.

    - `expc_qpc`: Questionário Pré-Copom: balanço de riscos do IPCA, projeção no horizonte relevante com a probabilidade de desvio, IPCA de curto prazo, o que o Copom fará e deveria fazer, juro neutro. O consenso às vésperas da reunião e onde ele discorda do Copom (Q3, canais 2.2, 2.8); os blocos de hiato, PIB, potencial e NAIRU são consulta da atividade.

### ii. Endógeno de política monetária (consulta; a posição vem pelas saídas XS1–XS4 do mapa de expectativas)
    - `inflc_meta`: meta de inflação do CMN. É o termo de âncora da (E) e a régua da desancoragem em todos os horizontes (canais 2.1, 2.2).

    - `pm_copom_projecoes`: projeção de inflação do Copom, de referência, até o horizonte relevante. A distância para a Focus e para o QPC é parte do teste de credibilidade (Q3).

    - `pm_copom_reuniao`: Selic decidida e passo, por reunião. Situa a reação das expectativas a cada decisão (canal 2.2).

    - `pm_copom_calendario`: datas das reuniões do Copom. Ordena a Focus por reunião e situa as revisões em torno de cada decisão (canais 2.2, 2.8).

    - `br_interest_rate`: curvas DI × pré e NTN-B (juro real) nos mesmos vértices. A razão entre as duas dá a inflação implícita na curva, a medida de mercado ao lado da pesquisa; a conclusão sobre ela é deste agente, a curva continua sendo dado da política monetária (canal 2.6).

### iii. Endógeno de inflação (consulta; a posição vem pelas saídas XS5–XS6 do mapa de expectativas)
    - `inflc_agregados`: IPCA mensal e 12 meses, grupos, núcleos e difusão. O IPCA 12 meses é o regressor da (E); a composição separa choque pontual de pressão persistente, e a surpresa contra a Focus mensal é o que faz a pesquisa revisar (canais 2.1, 2.4).

### iv. Endógeno de câmbio (consulta; a posição vem pela saída XS7 do mapa de expectativas)
    - `cmb_ptax`: câmbio diário. Para ver se a pesquisa reagiu a um movimento do câmbio (canal 2.4).

### v. Endógeno de fiscal (consulta; a posição vem pela saída XS8 do mapa de expectativas)
    - `cmb_risco_pais`: CDS de 5 anos do Brasil. O prêmio de risco soberano, termômetro da dúvida fiscal que chega primeiro aos horizontes longos (canal 2.3); a carga é manual, conferir a data do último dado.

*Fim das listas por agente.*
