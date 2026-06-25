'''Script Docs:
Nesse codigo, o objetivo é requisitar e armazenar na base de dados, os dados de subcomponentes do ipca e ioca 15.

'''

'''Ultima atualização:
Criado: 07/11/2024
Versão: v1 (07/11/2024)

'''

'''Melhorias Futuras:
'''


#_IMPORTAÇÕES
import pandas as pd


# importações nativa
from connectors.ibge import ibge_get, TratarDataIbge



#_ FUNÇÕES AUXILIARES

def variacao_para_indice(df, colunas_variacao, indice_inicial=100):

    '''
    Converte colunas de variação mensal para um índice acumulativo.

    Parâmetros:
        - df: DataFrame com as colunas de variação mensal.
        - colunas_variacao: Lista das colunas que contêm a variação mensal.
        - indice_inicial: Valor inicial para o índice (default=100).

    Retorna:
    - DataFrame com as colunas de índice acumulativo.

    '''

    df_resultado = df.copy()  # Copia o DataFrame original para preservar os dados

    for coluna in colunas_variacao:
        # Inicializa a coluna de índice acumulativo com o valor inicial
        df_resultado[f'indice_{coluna}'] = indice_inicial * (1 + df_resultado[coluna].fillna(0)).cumprod()
    return df_resultado


#_ FUNÇÕES
def rq_dados_variacaomensal():

    '''Importação dos dados do IBGE'''

    # links de importação do IBGE
    link_request_variacaomensal = "https://servicodados.ibge.gov.br/api/v3/agregados/7060/periodos//variaveis/63?localidades=N1[all]&classificacao=315[7173,7175,7176,47617,12222,47618,7185,7187,7188,7190,7191,7195,107608,47619,7201,7202,7203,7204,7206,7209,7210,7212,7215,7216,7220,7221,12224,107609,7230,107611,7233,47620,7242,7244,7245,7246,7248,7249,7253,7255,7256,7257,7258,7259,7260,7262,7263,7265,7266,7267,7268,7269,7270,7271,7272,7275,7276,7279,7280,7281,7285,7287,7288,7290,7291,7292,7293,7294,7295,7296,12294,7298,7299,7300,7301,101448,7302,47621,7305,7306,7309,7310,7311,7313,107615,107616,7317,7320,7323,12300,12301,101466,12431,12302,41129,7333,47623,8874,31694,47624,7336,12304,7339,7341,12305,7343,12379,7347,107617,107618,7355,12393,7358,7359,107619,12394,47627,7367,7368,7373,7375,7376,7377,7378,7380,7385,7386,12395,7390,47628,12396,7392,7393,107621,7396,7397,7399,47630,47631,107702,7406,7407,107624,107625,7411,7412,107628,107630,7416,109463,7418,12397,7420,7421,7422,7423,7424,7425,7428,7434,7435,107633,7438,7440,7443,47632,7444,47633,7448,7449,7451,7453,7455,7456,12433,7459,12398,47634,107638,107639,107640,107641,107642,107643,12399,7463,7464,7465,7466,7467,7470,7471,47635,47636,7477,47637,7481,7482,7483,7485,7489,7490,7492,12401,7493,47638,7497,7498,12402,12403,107645,7508,47639,7518,7520,7523,12434,7526,7530,7531,7539,7542,7543,47640,47641,12405,107648,12406,7555,47642,47643,7561,7563,47644,7565,107649,7573,7574,7575,7576,7577,7579,47645,12408,7589,7590,7591,47646,107650,12409,7606,7607,7608,107652,47647,7614,47648,7617,7618,7619,7622,7623,7628,7629,7630,7631,7632,7634,7635,7639,47649,47650,7641,7642,7643,107653,7644,7645,12411,7647,7648,7649,107654,7653,107656,7654,7658,7659,107657,7663,7664,7665,7666,12412,7669,7670,7671,47651,7673,7674,107659,7677,47652,7657,47653,7685,7686,12414,12435,12436,7691,7692,12416,7696,7699,12420,101642,101644,107661,7703,7704,7707,7708,7709,7710,7711,7715,12421,7720,47654,7721,7723,7724,7727,7728,47655,7733,7735,47657,7736,107666,7738,47658,107668,7746,47659,47660,47661,47662,7759,7769,47663,107671,107672,107673,107674,47664,47665,7778,107676,47666,47667,7783,7785,107679,107681,107682,107683,12428,7789,47668,47669,47670,107688,7794,47671,47672]"
    # link_request_peso = "https://servicodados.ibge.gov.br/api/v3/agregados/7060/periodos//variaveis/66?localidades=N1[all]&classificacao=315[...]"

    # # link de peso e variação com ajuste sazonal
    # link_varmensal_peso_as = "https://servicodados.ibge.gov.br/api/v3/agregados/7061/periodos//variaveis/306|309?localidades=N1[all]&classificacao=315[...]"

    # Requisição
    df_response_varmensal = ibge_get(link_request_variacaomensal, 2021, 2024, "M")
    # df_response_peso = ibge_get(link_peso, 2020, 2024, "M")

    # # ipca com ajuste sazonal
    # df_response_varmensal_peso = ibge_get(link_varmensal_peso_as, 2020, 2024, "M")

    return df_response_varmensal
