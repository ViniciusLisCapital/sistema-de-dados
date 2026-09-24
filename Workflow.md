**PONTO IMPORTANTE:** A esse material não deve ser adicionado ou retirado elementos por meio de agentes/AI. Somente humanos devem adicionar/retirar elementos. Contudo, modelos de AI podem organizar o material, quando pedido. Referencie esse material por meio de títulos e sessões e número da pagina.


# (I) Dashboards

  ## (I.I) Dashboards Brasil: 
  *Dashboards relacionados aos dados do Brasil*
  
  ### (I.I.I) Pendências gerais:
    - i. Dados de inflação do IPA-DI e adjacentes (ver Relatório de Política monetária do BC). O Banco Central (ver RPM 3T/2026) usou os dados para avaliar os impactos pirmarios diretos e indiretos do choque de petróleo sobre a inflação. Na mesma linha, usou um conjunto de dados para avaliar os efeitos de segunda ordem sobre a inflação, como a pesquisa Firmus e acho que no relatório tambem fala sobre dados qualitativos da Confederação da Industria. A ideia é fazer uma mapeamento do que ele usa, se temos API direta/indireta para consumir esses dados. Embora, os dados estejam sendo usados para analisar um processo inflacionario, a pesuqisa pode ser usada em varios dashboards.
    
    - ii. Consumo de dados do QPC (Questionario pre COPOM) - quando eu vi esse relatório, ele tinha bastante informações, não sei se conseguimos construir series e coisas do tipo. A ideia é mapear o que tem e ver como podemos consumir.

  ### (I.I.II) Dashboard de cambio
    - i. Unir dashboard de cambio do Arthur com o nosso. A ideia é colocar o dashboard dele numa unica aba do nosso, pois existem metricas que já estão sendo acompanhadas por lá que não temos no nosso dash.

  ### (I.I.III) Dashboard de política monetária
    - i. Criar os modelos mentais Verde, Kinea e Kapitalo 
    - ii. Criar o Attributor para o agente de política monetária


  ### (I.I.III) Dashboard de Expectativas
    -
 
  ### (I.I.IV) Dashboard de Credito
    -  

  ## (I.B) Dashboards US
  
  ### Dashboard de Inflação
    - i.Indicadores especiais de inflação (supercore, core services, metricas mais qualitativas, Ver relatório do BTG)
    - ii. Aumentar tamanho dos gráficos

  ### Dashboard de Mercado de trabalho




# (II) Sistema de Agentes 
*Contexto: O objetivo final é construir um sistema de agentes, cada um com a sua especialidade e contribuição para o todo. O sistema se alimentará com dados brutos, literatura econômica, literatura de mercado e ferramentas quantitativas e de dados para construção de relatórios e embasamento de decisões.*

## (II.I) Pendencias gerais 
    - i. Como está o ciclo de ingestão de literatura acadêmica e organização no obsidian? Divisão entre raw, clean e sintese, e o mapa conceitual. Eu sinto que esse processo está desorganizado.

    - ii. Como está a ingestão automatica das cartas dos gestores? Onde o processo roda (agente, .py)? Está agendado?

    - iii. Definir instruções de sistema e instruções específicas.

## (II.II) Agente de cambio
    - i. Estabelecimento doa agente de câmbio: O agente de cambio já tem um script inicial em /.claude. Contudo, acho que o modelo não foi setado, e não sei quais instruções o agente recebeu. Além do mais, o agente foi construido num vacuo, sem a consideração dos outros agentes/sistema como um todo, e isso será feito com o tempo. (Ver II.I.iii)

    - ii. Relatório de câmbio já considerando o processo interatico com os outros agentes.

## (II.III) Agente de politica monetaria
    - Organizar a literatura (ver II.I.i)
    - Criar o material de discussão inicial
    - Definir as instruções específicas do agente de política monetária e relação deste com o sistema geral.

## (II.IV) Agente de Juros
 
## (II.V) Agente Fiscal

# (III) Outras Demandas
    - i. Eleição americana e impacto no USD: (1) O que o Trump implementou daquilo que estava expresso no chamado acordo de Mar a Lago - um artigo publicado, se eu não me engano, no final de 2024 pelo Stephen Miran? (2) Considerando o que foi implementado, como a midterms pode afetar o poder do Trump e reverter algumas medidas? Aqui cabe uma analise de cenário, no caso da manutenção das duas casas, e da perda de uma ou das duas. (3) Acompanhar a decomposição do USDBRL (Ver IV.II.ii) diariamente para entender uma mudança de fatores explicativos.

# (IV) Modelo Quantitativo

## (IV. I) Pendencias gerais
    - i. Já temos um modelo de cambio embutido no "reports\brasil\FX Report.html". Para o sistema macroecnomico geral, a ideia é manter um unico modelo estrutural que, a principio, terá equações para inflação, cambio, juros, hiato, expectativas. Ainda preciso definir coisas nesse processo.

## (IV. II) Modelo de cambio
    
    - i. Usar o modelo mensal + variaveis diarias para calcular a decomposição da variação do cambio em frequência diaria. A ideia é decompor usando a estimativa mensal (somente para ter uma ideia)

## (IV.III) Modelo de inflação
    - i. Melhoramentos das equações de inflação (ver analytics\brasil\structural_model\pendencias_philips_eq.md)












