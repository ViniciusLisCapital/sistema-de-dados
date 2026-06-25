'''Script Docs:
Nesse codigo, o objetivo é requisitar os dados de variação mensal, peso e variação 12m do IPCA. Com os dados de variação mensal e peso que 
eu construo a contribuição de cada subitem do ipca para a variação mensal do ipca.

Os dados de variação 12m são usados na forma bruta.
'''

'''Ultima atualização:

07/10/2024

'''

'''Melhorias Futuras:
a.) organizar a estrutura dos dados para exportação em formato Long; (ver se é necessário)

b.) Calculo de subindices importantes, como serviços subjacentes;
'''


#_IMPORTAÇÕES
import os
import pandas as pd

# importações nativa
from connectors.ibge import ibge_get, TratarDataIbge

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

#_ FUNÇÕES
def request_ibge_data():
    
    '''Importação dos dados do IBGE'''
    
    # links de importação do IBGE    
    link_var_mensal = "https://servicodados.ibge.gov.br/api/v3/agregados/7060/periodos//variaveis/63?localidades=N1[all]&classificacao=315[7173,7175,7176,47617,12222,47618,7185,7187,7188,7190,7191,7195,107608,47619,7201,7202,7203,7204,7206,7209,7210,7212,7215,7216,7220,7221,12224,107609,7230,107611,7233,47620,7242,7244,7245,7246,7248,7249,7253,7255,7256,7257,7258,7259,7260,7262,7263,7265,7266,7267,7268,7269,7270,7271,7272,7275,7276,7279,7280,7281,7285,7287,7288,7290,7291,7292,7293,7294,7295,7296,12294,7298,7299,7300,7301,101448,7302,47621,7305,7306,7309,7310,7311,7313,107615,107616,7317,7320,7323,12300,12301,101466,12431,12302,41129,7333,47623,8874,31694,47624,7336,12304,7339,7341,12305,7343,12379,7347,107617,107618,7355,12393,7358,7359,107619,12394,47627,7367,7368,7373,7375,7376,7377,7378,7380,7385,7386,12395,7390,47628,12396,7392,7393,107621,7396,7397,7399,47630,47631,107702,7406,7407,107624,107625,7411,7412,107628,107630,7416,109463,7418,12397,7420,7421,7422,7423,7424,7425,7428,7434,7435,107633,7438,7440,7443,47632,7444,47633,7448,7449,7451,7453,7455,7456,12433,7459,12398,47634,107638,107639,107640,107641,107642,107643,12399,7463,7464,7465,7466,7467,7470,7471,47635,47636,7477,47637,7481,7482,7483,7485,7489,7490,7492,12401,7493,47638,7497,7498,12402,12403,107645,7508,47639,7518,7520,7523,12434,7526,7530,7531,7539,7542,7543,47640,47641,12405,107648,12406,7555,47642,47643,7561,7563,47644,7565,107649,7573,7574,7575,7576,7577,7579,47645,12408,7589,7590,7591,47646,107650,12409,7606,7607,7608,107652,47647,7614,47648,7617,7618,7619,7622,7623,7628,7629,7630,7631,7632,7634,7635,7639,47649,47650,7641,7642,7643,107653,7644,7645,12411,7647,7648,7649,107654,7653,107656,7654,7658,7659,107657,7663,7664,7665,7666,12412,7669,7670,7671,47651,7673,7674,107659,7677,47652,7657,47653,7685,7686,12414,12435,12436,7691,7692,12416,7696,7699,12420,101642,101644,107661,7703,7704,7707,7708,7709,7710,7711,7715,12421,7720,47654,7721,7723,7724,7727,7728,47655,7733,7735,47657,7736,107666,7738,47658,107668,7746,47659,47660,47661,47662,7759,7769,47663,107671,107672,107673,107674,47664,47665,7778,107676,47666,47667,7783,7785,107679,107681,107682,107683,12428,7789,47668,47669,47670,107688,7794,47671,47672]"
    link_peso = "https://servicodados.ibge.gov.br/api/v3/agregados/7060/periodos//variaveis/66?localidades=N1[all]&classificacao=315[7173,7175,7176,47617,12222,47618,7185,7187,7188,7190,7191,7195,107608,47619,7201,7202,7203,7204,7206,7209,7210,7212,7215,7216,7220,7221,12224,107609,7230,107611,7233,47620,7242,7244,7245,7246,7248,7249,7253,7255,7256,7257,7258,7259,7260,7262,7263,7265,7266,7267,7268,7269,7270,7271,7272,7275,7276,7279,7280,7281,7285,7287,7288,7290,7291,7292,7293,7294,7295,7296,12294,7298,7299,7300,7301,101448,7302,47621,7305,7306,7309,7310,7311,7313,107615,107616,7317,7320,7323,12300,12301,101466,12431,12302,41129,7333,47623,8874,31694,47624,7336,12304,7339,7341,12305,7343,12379,7347,107617,107618,7355,12393,7358,7359,107619,12394,47627,7367,7368,7373,7375,7376,7377,7378,7380,7385,7386,12395,7390,47628,12396,7392,7393,107621,7396,7397,7399,47630,47631,107702,7406,7407,107624,107625,7411,7412,107628,107630,7416,109463,7418,12397,7420,7421,7422,7423,7424,7425,7428,7434,7435,107633,7438,7440,7443,47632,7444,47633,7448,7449,7451,7453,7455,7456,12433,7459,12398,47634,107638,107639,107640,107641,107642,107643,12399,7463,7464,7465,7466,7467,7470,7471,47635,47636,7477,47637,7481,7482,7483,7485,7489,7490,7492,12401,7493,47638,7497,7498,12402,12403,107645,7508,47639,7518,7520,7523,12434,7526,7530,7531,7539,7542,7543,47640,47641,12405,107648,12406,7555,47642,47643,7561,7563,47644,7565,107649,7573,7574,7575,7576,7577,7579,47645,12408,7589,7590,7591,47646,107650,12409,7606,7607,7608,107652,47647,7614,47648,7617,7618,7619,7622,7623,7628,7629,7630,7631,7632,7634,7635,7639,47649,47650,7641,7642,7643,107653,7644,7645,12411,7647,7648,7649,107654,7653,107656,7654,7658,7659,107657,7663,7664,7665,7666,12412,7669,7670,7671,47651,7673,7674,107659,7677,47652,7657,47653,7685,7686,12414,12435,12436,7691,7692,12416,7696,7699,12420,101642,101644,107661,7703,7704,7707,7708,7709,7710,7711,7715,12421,7720,47654,7721,7723,7724,7727,7728,47655,7733,7735,47657,7736,107666,7738,47658,107668,7746,47659,47660,47661,47662,7759,7769,47663,107671,107672,107673,107674,47664,47665,7778,107676,47666,47667,7783,7785,107679,107681,107682,107683,12428,7789,47668,47669,47670,107688,7794,47671,47672]"
    link_var_12m = "https://servicodados.ibge.gov.br/api/v3/agregados/7060/periodos//variaveis/2265?localidades=N1[all]&classificacao=315[7173,7175,7176,47617,12222,47618,7185,7187,7188,7190,7191,7195,107608,47619,7201,7202,7203,7204,7206,7209,7210,7212,7215,7216,7220,7221,12224,107609,7230,107611,7233,47620,7242,7244,7245,7246,7248,7249,7253,7255,7256,7257,7258,7259,7260,7262,7263,7265,7266,7267,7268,7269,7270,7271,7272,7275,7276,7279,7280,7281,7285,7287,7288,7290,7291,7292,7293,7294,7295,7296,12294,7298,7299,7300,7301,101448,7302,47621,7305,7306,7309,7310,7311,7313,107615,107616,7317,7320,7323,12300,12301,101466,12431,12302,41129,7333,47623,8874,31694,47624,7336,12304,7339,7341,12305,7343,12379,7347,107617,107618,7355,12393,7358,7359,107619,12394,47627,7367,7368,7373,7375,7376,7377,7378,7380,7385,7386,12395,7390,47628,12396,7392,7393,107621,7396,7397,7399,47630,47631,107702,7406,7407,107624,107625,7411,7412,107628,107630,7416,109463,7418,12397,7420,7421,7422,7423,7424,7425,7428,7434,7435,107633,7438,7440,7443,47632,7444,47633,7448,7449,7451,7453,7455,7456,12433,7459,12398,47634,107638,107639,107640,107641,107642,107643,12399,7463,7464,7465,7466,7467,7470,7471,47635,47636,7477,47637,7481,7482,7483,7485,7489,7490,7492,12401,7493,47638,7497,7498,12402,12403,107645,7508,47639,7518,7520,7523,12434,7526,7530,7531,7539,7542,7543,47640,47641,12405,107648,12406,7555,47642,47643,7561,7563,47644,7565,107649,7573,7574,7575,7576,7577,7579,47645,12408,7589,7590,7591,47646,107650,12409,7606,7607,7608,107652,47647,7614,47648,7617,7618,7619,7622,7623,7628,7629,7630,7631,7632,7634,7635,7639,47649,47650,7641,7642,7643,107653,7644,7645,12411,7647,7648,7649,107654,7653,107656,7654,7658,7659,107657,7663,7664,7665,7666,12412,7669,7670,7671,47651,7673,7674,107659,7677,47652,7657,47653,7685,7686,12414,12435,12436,7691,7692,12416,7696,7699,12420,101642,101644,107661,7703,7704,7707,7708,7709,7710,7711,7715,12421,7720,47654,7721,7723,7724,7727,7728,47655,7733,7735,47657,7736,107666,7738,47658,107668,7746,47659,47660,47661,47662,7759,7769,47663,107671,107672,107673,107674,47664,47665,7778,107676,47666,47667,7783,7785,107679,107681,107682,107683,12428,7789,47668,47669,47670,107688,7794,47671,47672]"
    
    # Requisição
    df_response_varmensal = ibge_get(link_var_mensal, 2020, 2026, "M")
    df_response_peso = ibge_get(link_peso, 2020, 2026, "M")
    df_response_var12m = ibge_get(link_var_12m, 2020, 2026, "M")

    return df_response_varmensal, df_response_peso, df_response_var12m

def processar_varmensal(df_varmensal):
    '''Processar dados de variação mensal do IPCA'''
    
    var_mensal = df_varmensal.drop(['variavel', 'localidade'], axis = 1)
    var_mensal = var_mensal.rename({'Class_0': 'Subitem', 'serie':'var_mensal'}, axis = 1)
    var_mensal['dt'] = TratarDataIbge(var_mensal['dt'], 'M')
    var_mensal['var_mensal'] = pd.to_numeric(var_mensal['var_mensal'], errors = 'coerce')
    var_mensal['Subitem'] = var_mensal['Subitem'].str.replace('.', ' ')
    
    return var_mensal

def processar_peso_mensal(df_response_peso):
    '''Processar dados do peso de cada variavel do IPCA'''
  
    peso_mensal = df_response_peso.drop(['variavel', 'localidade'], axis = 1)
    peso_mensal = peso_mensal.rename({'Class_0': 'Subitem', 'serie': 'pesos'}, axis = 1)
    peso_mensal['dt'] = TratarDataIbge(peso_mensal['dt'], 'M')
    peso_mensal['pesos'] = pd.to_numeric(peso_mensal['pesos'], errors = 'coerce')/100
    peso_mensal['Subitem'] = peso_mensal['Subitem'].str.replace('.', ' ')
    
    return peso_mensal

def processar_var12m(df_response_var12m):
    '''Processar dados do peso de cada variavel do IPCA'''
    
    variacao_12m = df_response_var12m.drop(['variavel', 'localidade'], axis = 1)
    variacao_12m = variacao_12m.rename({'Class_0': 'Subitem', 'serie': 'var12m'}, axis = 1)
    variacao_12m['dt'] = TratarDataIbge(variacao_12m['dt'], 'M')
    variacao_12m['var12m'] = pd.to_numeric(variacao_12m['var12m'], errors = 'coerce')
    variacao_12m['Subitem'] = variacao_12m['Subitem'].str.replace('.', ' ')
    
    return variacao_12m

def calculo_contribuicao_varmensal(df_variacao_mensal, df_peso_mensal):
    ''' Unindo os dados de variacao mensal e o peso calculamos a contribuição de cada subitem para aquela variação'''
    
    # merge do frames para facilitar o calculo
    df_merge = pd.merge(df_variacao_mensal, df_peso_mensal, left_on=['Subitem', 'dt'], right_on=['Subitem', 'dt'])
    #df_merge.to_excel('ipca_2020_2024.xlsx')
    
    #calculo da contribuição de cada subitem
    df_merge['contribuição_mensal'] = df_merge['var_mensal'] * (df_merge['pesos'])
    
    return df_merge

def calculo_contribuicao_var_12m(variacao_12m, df_peso_mensal):
    ''' Unindo os dados de variacao 12m e o peso calculamos a contribuição de cada subitem para aquela variação'''
    
        # merge do frames para facilitar o calculo
    df_merge = pd.merge(variacao_12m, df_peso_mensal, left_on=['Subitem', 'dt'], right_on=['Subitem', 'dt'])
    #calculo da contribuição de cada subitem
    df_merge['contribuicao_var12m'] = df_merge['var12m'] * (df_merge['pesos'])
    df_var12m = df_merge.copy()
    
    return df_var12m
    
def exportacao_dados(frame_var12, merged_frame):
    ''' Exportacao dos dados tratados '''

    frame_var12.to_excel(os.path.join(SCRIPT_DIR, 'variacao12m_ipca.xlsx'))
    merged_frame.to_excel(os.path.join(SCRIPT_DIR, 'variacao_peso_contribuicao_ipca.xlsx'))

    print('Exportado!')
    
    
#_EXECUÇÃO DO SCRIPT
#explicacao
'''
Explicação "__name__ == 'main':"
Quando você executa um arquivo Python, algumas variáveis especiais são configuradas automaticamente. Uma dessas variáveis é __name__. 
Seu valor depende de como o arquivo está sendo executado:

Quando você executa um script diretamente (por exemplo, python meu_script.py), a variável __name__ é definida como "__main__".
Quando você importa o script como um módulo em outro script (por exemplo, import meu_script), 
a variável __name__ é definida como o nome do módulo, como meu_script.
O bloco if __name__ == "__main__": verifica se o script está sendo executado diretamente. 
Se isso for verdadeiro, o código dentro desse bloco será executado. Caso contrário, se o script for importado como módulo, esse código será ignorado.

'''


#execução
if __name__ == '__main__':
    
    # requisição dos dados
    var_mensal, peso_mensal, variacao_12m = request_ibge_data()
    
    # processamento dos dados
    var_mensal = processar_varmensal(var_mensal)
    peso_mensal = processar_peso_mensal(peso_mensal)
    var_12m = processar_var12m(variacao_12m)
    
    # frame com varmensal, peso e contribuição
    var_mensal = calculo_contribuicao_varmensal(var_mensal, peso_mensal)
    var_12m = calculo_contribuicao_var_12m(var_12m, peso_mensal)
    
    #exportacao de dados
    exportacao_dados(var_12m, var_mensal)













































# def ipca_antigo():
#     #_ 2.) IMPORTAR BIBLIOTECAS PROPRIAS
#     import sys


#     #! 2.2) importações nativa
#     from DATABASE.DB_Management.API_CONECTOR.IBGE.IBGE_API import ibge_get, TratarDataIbge


#     import pandas as pd


#     link = "https://servicodados.ibge.gov.br/api/v3/agregados/7060/periodos//variaveis/63|66?localidades=N1[all]&classificacao=315[7173,7175,7176,47617,12222,47618,7185,7187,7188,7190,7191,7195,107608,47619,7201,7202,7203,7204,7206,7209,7210,7212,7215,7216,7220,7221,12224,107609,7230,107611,7233,47620,7242,7244,7245,7246,7248,7249,7253,7255,7256,7257,7258,7259,7260,7262,7263,7265,7266,7267,7268,7269,7270,7271,7272,7275,7276,7279,7280,7281,7285,7287,7288,7290,7291,7292,7293,7294,7295,7296,12294,7298,7299,7300,7301,101448,7302,47621,7305,7306,7309,7310,7311,7313,107615,107616,7317,7320,7323,12300,12301,101466,12431,12302,41129,7333,47623,8874,31694,47624,7336,12304,7339,7341,12305,7343,12379,7347,107617,107618,7355,12393,7358,7359,107619,12394,47627,7367,7368,7373,7375,7376,7377,7378,7380,7385,7386,12395,7390,47628,12396,7392,7393,107621,7396,7397,7399,47630,47631,107702,7406,7407,107624,107625,7411,7412,107628,107630,7416,109463,7418,12397,7420,7421,7422,7423,7424,7425,7428,7434,7435,107633,7438,7440,7443,47632,7444,47633,7448,7449,7451,7453,7455,7456,12433,7459,12398,47634,107638,107639,107640,107641,107642,107643,12399,7463,7464,7465,7466,7467,7470,7471,47635,47636,7477,47637,7481,7482,7483,7485,7489,7490,7492,12401,7493,47638,7497,7498,12402,12403,107645,7508,47639,7518,7520,7523,12434,7526,7530,7531,7539,7542,7543,47640,47641,12405,107648,12406,7555,47642,47643,7561,7563,47644,7565,107649,7573,7574,7575,7576,7577,7579,47645,12408,7589,7590,7591,47646,107650,12409,7606,7607,7608,107652,47647,7614,47648,7617,7618,7619,7622,7623,7628,7629,7630,7631,7632,7634,7635,7639,47649,47650,7641,7642,7643,107653,7644,7645,12411,7647,7648,7649,107654,7653,107656,7654,7658,7659,107657,7663,7664,7665,7666,12412,7669,7670,7671,47651,7673,7674,107659,7677,47652,7657,47653,7685,7686,12414,12435,12436,7691,7692,12416,7696,7699,12420,101642,101644,107661,7703,7704,7707,7708,7709,7710,7711,7715,12421,7720,47654,7721,7723,7724,7727,7728,47655,7733,7735,47657,7736,107666,7738,47658,107668,7746,47659,47660,47661,47662,7759,7769,47663,107671,107672,107673,107674,47664,47665,7778,107676,47666,47667,7783,7785,107679,107681,107682,107683,12428,7789,47668,47669,47670,107688,7794,47671,47672]"


#     #! Requisição
#     df_response = ibge_get(link, 2020, 2024, "M")

#     df_variacao_mensal = df_response[df_response['variavel'] == 'IPCA - Variação mensal'] 
#     df_peso_mensal = df_response[df_response['variavel'] == 'IPCA - Peso mensal']


#     #___ajuste do frame de variações mensais
#     df_variacao_mensal = df_variacao_mensal.drop(['variavel', 'localidade'], axis = 1)
#     df_variacao_mensal = df_variacao_mensal.rename({'Class_0': 'subitem', 'serie':'var_mensal'}, axis = 1)




#     #___ajuste do frame de peso mensal
#     df_peso_mensal = df_peso_mensal.drop(['variavel', 'localidade'], axis = 1)
#     df_peso_mensal = df_peso_mensal.rename({'Class_0': 'subitem', 'serie': 'pesos'}, axis = 1)


#     df_merge = pd.merge(df_variacao_mensal, df_peso_mensal, left_on=['subitem', 'dt'], right_on=['subitem', 'dt'])


#     #___dt como index
#     df_merge['dt'] = TratarDataIbge(df_merge['dt'], "M")


#     #__transformando o valores de string para numerico
#     df_merge['var_mensal'] = pd.to_numeric(df_merge['var_mensal'], errors = 'coerce')
#     df_merge['pesos'] = pd.to_numeric(df_merge['pesos'], errors = 'coerce')


#     #__contribuição
#     df_merge['contribuição_mensal'] = df_merge['var_mensal'] * (df_merge['pesos']/100)


#     ww
#     #__export variacao mensal
#     df_variacao_mensal = df_merge.drop(['pesos', 'contribuição_mensal'], axis = 1) 
#     df_variacao_mensal.rename({'var_mensal': 'Values', 'dt':'Date', 'subitem':'Name'}, axis= 1, inplace = True)
#     df_variacao_mensal['Name'] = df_variacao_mensal['Name'].str.replace('.', ' ')
#     df_variacao_mensal.to_excel(
#                                 r"C:\Users\LIS CAPITAL\LIS Capital Dropbox\LIS Capital\LIS Value FIA\BD_MACRO\ORACULO\DASHBOARDS\BRASIL\INFLATION\IPCA\db_br_ipca_decomposition\var_monthly_ipca.xlsx")


#     #__export peso mensal
#     df_peso_mensal = df_merge.drop(['var_mensal', 'contribuição_mensal'], axis = 1) 
#     df_peso_mensal.rename({'pesos': 'Values', 'dt':'Date', 'subitem':'Name'}, axis= 1, inplace = True)
#     df_peso_mensal['Name'] = df_peso_mensal['Name'].str.replace('.', ' ')
#     df_peso_mensal.to_excel(
#                             r"C:\Users\LIS CAPITAL\LIS Capital Dropbox\LIS Capital\LIS Value FIA\BD_MACRO\ORACULO\DASHBOARDS\BRASIL\INFLATION\IPCA\db_br_ipca_decomposition\weight_monthly_ipca.xlsx")


#     #__export contribuição mensal
#     df_contribuicao_mensal = df_merge.drop(['var_mensal', 'pesos'], axis = 1) 
#     df_contribuicao_mensal.rename({'contribuição_mensal': 'Values', 'dt':'Date', 'subitem':'Name'}, axis= 1, inplace = True)
#     df_contribuicao_mensal['Name'] = df_contribuicao_mensal['Name'].str.replace('.', ' ')
#     df_contribuicao_mensal.to_excel(
#                             r"C:\Users\LIS CAPITAL\LIS Capital Dropbox\LIS Capital\LIS Value FIA\BD_MACRO\ORACULO\DASHBOARDS\BRASIL\INFLATION\IPCA\db_br_ipca_decomposition\contribution_monthly_ipca.xlsx")


#     print("IPCA decomposition Update!!")













    def guardar ():
        pass
        # # 2.5) União dos frames
        # df_merge = pd.merge(df_variacao_mensal, df_peso_mensal, left_on=['Subitem', 'dt'], right_on=['Subitem', 'dt'])

        # # 2.6) Tratar datas
        # df_merge['dt'] = TratarDataIbge(df_merge['dt'], "M")

        # # 2.7) transformando o valores: string para numerico
        # df_merge['var_mensal'] = pd.to_numeric(df_merge['var_mensal'], errors = 'coerce')
        # df_merge['pesos'] = pd.to_numeric(df_merge['pesos'], errors = 'coerce')

        # # 2.8) calculo de contribuição
        # df_merge['contribuição_mensal'] = df_merge['var_mensal'] * (df_merge['pesos']/100)
        # df_merge['Subitem'] = df_merge['Subitem'].str.replace('.', ' ')


        # # 3.) IMPORTAÇÃO DE DADOS DE DIMENSÃO
        # ipca_dimension = pd.read_excel(r"C:\Users\LIS CAPITAL\LIS Capital Dropbox\LIS Capital\LIS Value FIA\BD_MACRO\ORACULO\DASHBOARDS\BRASIL\INFLATION\IPCA\db_br_ipca_decomposition\dim_br_inflation_ipca.xlsx", sheet_name = 'dim_bcb_view')


        # # 4.) TRATAMENTO DOS DADOS PARA CRIAR O INDICE DE SERVIÇOS SUBJACENTES
        # #4.1) merge a tabela fatos e a tabela dimensão
        # df_merge = pd.merge(df_merge, ipca_dimension, on  = 'Subitem')

        # # 4.2) filtro dos componentes de Serviços subjacentes
        # df_filtered = df_merge[df_merge['Item'] == 'Serviços Subjacente']

        # # 4.3) Agregação e reponderação
        # df_filtered['peso_ajustado'] = df_filtered.groupby('dt')['pesos'].transform(lambda x: x / x.sum())

        # df_filtered['contribuicao_serv_subjacentes'] = df_filtered['peso_ajustado'] * df_filtered['var_mensal']

        # variacao_subjacente = df_filtered.groupby('dt')['contribuicao_serv_subjacentes'].sum()
