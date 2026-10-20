**Sobre este arquivo:** os princípios gerais de um agente-analista, tirados das decisões tomadas no agente de câmbio. Servem para construir os próximos agentes mais rápido: o que está aqui o Claude aplica sem perguntar, e o usuário aprova só os pontos da seção (III). Cada princípio aponta a decisão de origem no `SISTEMA_AGENTES.md`. Um princípio só entra aqui depois que o usuário decidiu; quando o caso de um agente novo contrariar um princípio, pergunta-se.


# (I) Princípios

## (I.I) Conhecimento
    - i. O agente lê só o `obsidian/`. O bruto fica no `repository/` e nenhum agente lê dele. (I.III.i)
    - ii. Pasta da área no vault: `clean_md/`, `synthesis/`, `mental_models/` e o mapa conceitual. Os conceitos de todas as áreas ficam numa pasta só, `obsidian/concepts/`. (I.III.ii; pasta única decidida em 2026-10-19, II.I.v)
    - iii. Modelos mentais por área × gestora. São arcabouço, não opinião atual. (I.III.iii)
    - iv. O mapa conceitual é o contrato da área, em cinco partes: perguntas centrais, esqueleto causal, saídas, entradas, índice de conceitos. (I.III.vi)
    - v. As perguntas centrais são o mínimo do report, não o máximo: insights novos e alertas também entram. (I.III.vi)
    - vi. Saídas e entradas são recíprocas entre os mapas e dão ênfase, não limite. Têm uma camada fixa (mapa) e uma dinâmica (reports). (I.III.vii, viii)
    - vii. Da literatura o agente usa o raciocínio (mecanismo, premissas, quando vale e quando falha), não os números. A estimativa de um paper pertence à amostra dele e nunca entra como valor atual; o dado atual vem do banco. (II.I.v)

## (I.II) Dados
    - i. Toda tabela da lista do agente tem um tipo: endógeno (dele), endógeno de outro agente (consulta sem concluir), TWA (área ainda sem agente) ou exógeno (sem agente). (I.III.ix, x)
    - ii. A lista fica no `SISTEMA_AGENTES.md` (V), uma tabela por linha, dizendo para que serve e por qual canal do mapa entra.
    - iii. Dado bruto A → F(A): F são as transformações fixas de cada tabela. O agente lê F(A), não A. (IV.iv)
    - iv. F(A) é gerado no início do ciclo e não muda até o fim dele. (IV.iv)
    - v. As métricas do F são do sistema: o agente as define sob supervisão do administrador, e o usuário julga pela qualidade do report. Com o usuário se discute QUAIS dados o agente recebe, não o tratamento. (IV.iv)
    - vi. Conta que o F não faz: o agente escreve uma função G e usa G(A). G só lê, usa o mesmo A do ciclo, e o código e o resultado vão para o log, nunca para o report nem para o relatório. No fim do ciclo, G fica como registro ou é promovido ao F. Todo tratamento do dado passa por G; o dado usado como está na base não precisa. (IV.iv)
    - vii. Profundidade: endógeno com leitura completa; TWA e exógeno com leitura enxuta. (IV.iv, provisório até a distribuição das exógenas)
    - viii. Todo número rastreável até a fonte: valor, tabela e data. (I.I.iv)

## (I.III) Report e ciclo
    - i. Report em três blocos (tese, argumentação, premissas), mais saídas e pedidos aos outros agentes e o placar. Modelo único para todos: `obsidian/ciclos/_modelo_report.md`. (III.III.i)
    - ii. Tese por variável: medida central, faixa base com probabilidade, caudas worst e best com probabilidade, assimetria Pbc − Pwc. Riscos entram na argumentação. (III.III.i)
    - iii. Horizontes: os seis trimestres do Modelo Estrutural a partir do trimestre em curso, com a variável no fechamento do trimestre; exceção só quando a variável pede (ex.: política monetária, por reunião). (III.III.i)
    - iv. Ciclo: rodada 1, P1, rodada 2, P2, report final, PF*. Todos escrevem em paralelo dentro da rodada. Do ciclo ficam o report final, o log e o relatório. (III.III.ii)
    - v. Report e relatório em português; termo técnico consagrado em inglês é permitido. (III.III.i)
    - vi. Premissas em duas etapas. Etapa 1: o caminho de cada exógena do modelo por cenário; o modelo resolve as endógenas e dá a central (cenário base, sem ajuste). Etapa 2: o tempero qualitativo forma a distribuição em torno da central, por (i) efeito de um input mais forte ou mais fraco que o estimado, com justificativa tanto mais forte quanto mais longe na distribuição do coeficiente, ou (ii) fator fora das variáveis do modelo. Canal que está no modelo só entra pelo tipo (i). (IV.ix)

## (I.IV) Ferramentas e modelo
    - i. Ferramenta = processamento pré-definido que entrega ao agente uma saída pronta. Fica fora dos agentes nesta fase. (I.III.xiv, I.II.iv)
    - ii. O Modelo Estrutural não é ferramenta: é a saída comum da análise dos agentes. (I.III.xv)

## (I.V) Apresentação
    - i. Diagrama do sistema: guia expansível; cada seta ou caixa abre o detalhe ao clicar. O conteúdo de cada caixa é curto e combinado com o usuário antes de entrar.
    - ii. Títulos se distinguem pela cor, não pelo tamanho da letra.


# (II) O que o Claude faz sem perguntar num agente novo
    - i. Montar a pasta da área no vault e o mapa conceitual no formato das cinco partes.
    - ii. Classificar as tabelas da lista nos quatro tipos e aplicar a profundidade correspondente.
    - iii. Gerar o F(A) com o mesmo código do câmbio, só declarando as tabelas.
    - iv. Usar o modelo de report e o de log sem alterar a estrutura.
    - v. Acrescentar a seta do agente no diagrama, no padrão das que já existem.


# (III) O que vai para aprovação do usuário em cada agente novo
    - i. As perguntas centrais da área.
    - ii. A direção de worst e best de cada variável, e qualquer exceção aos horizontes do modelo.
    - iii. A lista de dados e o tipo de cada tabela, apresentada de uma vez e numerada, para aprovar, cortar ou questionar.
    - iv. As saídas e entradas com os agentes que já existem.
    - v. Qualquer exceção a um princípio deste arquivo.


# (IV) Ainda em definição no câmbio (viram princípio quando decididos)
    - (nada no momento)
