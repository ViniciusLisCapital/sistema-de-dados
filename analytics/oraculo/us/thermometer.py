

#_ 1.) Set Up inicial


import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest

from utils.thermometer import Score
from utils.transforms import pivot_table_to_long as unpivot

#_ 1.) Colocar num lugar diferente
#!sem usar
def criar_banda(input_vector, valor_inicial):
    
    vector_banda = []

    for i in range(len(input_vector)):
        if i == 0:
            vector_banda.append(valor_inicial)
        else:
            diff = input_vector[i] - vector_banda[i - 1]

            if diff < -0.75:
                vector_banda.append(vector_banda[i - 1] - 1)
            
            elif diff > 0.75:
                vector_banda.append(vector_banda[i - 1] + 1)
            
            else:
                vector_banda.append(vector_banda[i - 1])

    return vector_banda

def remove_outliers(df, column_name, kind_interpol = 'linear', contamination = 0.05):
    
  # Organizando o Frame
  array_intermediate = df.loc[ : , column_name]
  df = pd.DataFrame(array_intermediate)

  #SetUp o IsolationForest 
  clf = IsolationForest(contamination = contamination)
  df['Outlier'] = clf.fit_predict(df.values)

  # Substituindo os outliers por 0
  df.loc[df['Outlier'] == -1, column_name] = np.nan

  #Dropando a coluna comm index_Outlier
  df = df.drop(columns=['Outlier'])

  #Processo de substituição do zero por uma interpolação
  df.interpolate(method = kind_interpol, axis = 0, inplace = True)

  return df[column_name]


#_2.) IMPORTAR INFORMAÇÕES FINANCEIRAS
# 2.1) Importação das informações das empresas
# Caminho de importacao 
path_economatica_base = r'C:\Users\LIS CAPITAL\LIS Capital Dropbox\LIS Capital\Macro\Sistema de dados\database\us\finance\base_dados_economatica_us.xlsx'
path_economatica_deactivate = r'C:\Users\LIS CAPITAL\LIS Capital Dropbox\LIS Capital\Macro\Sistema de dados\database\us\finance\base_dados_economatica_us - deactive.xlsx'
path_10yinterest_rate = r'C:\Users\LIS CAPITAL\LIS Capital Dropbox\LIS Capital\Macro\Sistema de dados\database\us\finance\10YReal_rates.xlsx'

# Valor de mercado
df_valor_mercado = pd.read_excel(path_economatica_base, sheet_name = "valor_mercado", index_col="Datas")
df_valor_mercado_deactivate = pd.read_excel(path_economatica_deactivate, sheet_name = "valor_mercado", index_col="Datas")
df_valor_mercado = df_valor_mercado.merge(df_valor_mercado_deactivate, how = 'outer', left_index = True, right_index = True)
#df_valor_mercado.to_excel(r'C:\Users\LIS CAPITAL\LIS Capital Dropbox\LIS Capital\LIS Value FIA\Macro\Sistema de dados\Database\United States\Finance\valor_mercado.xlsx')  

# PRECO/LUCRO
df_preco_lucro = pd.read_excel(path_economatica_base, sheet_name = "preco_lucro", index_col="Datas")
df_preco_lucro_deactivate = pd.read_excel(path_economatica_deactivate, sheet_name = "preco_lucro", index_col="Datas")
df_preco_lucro = df_preco_lucro.merge(df_preco_lucro_deactivate, how = 'outer', left_index = True, right_index = True)

# PRICE TO BOOK
df_price_book = pd.read_excel(path_economatica_base, sheet_name = "price_book", index_col="Datas")
df_price_book_deactivate = pd.read_excel(path_economatica_deactivate, sheet_name = "price_book", index_col="Datas")
df_price_book = df_price_book.merge(df_price_book_deactivate, how = 'outer', left_index = True, right_index = True)

# PATRIMONIO LIQUIDO
df_patrimonio_liquido = df_valor_mercado.div(df_price_book)

# ENTERPRISE VALUE
df_enterprise_value = pd.read_excel(path_economatica_base, sheet_name = "enterprise_value", index_col="Datas")
df_enterprise_value_deactivate = pd.read_excel(path_economatica_deactivate, sheet_name = "enterprise_value", index_col="Datas")
df_enterprise_value = df_enterprise_value.merge(df_enterprise_value_deactivate, how = 'outer', left_index = True, right_index = True)

# LUCRO TRIMESTRAL
df_lucro3m = pd.read_excel(path_economatica_base, sheet_name = "lucro_3m", index_col = "Datas")
df_lucro3m_deactivate = pd.read_excel(path_economatica_deactivate, sheet_name = "lucro_3m", index_col = "Datas")
df_lucro3m = df_lucro3m.merge(df_lucro3m_deactivate, how = 'outer', left_index = True, right_index = True)

# Lucro dos ultimos 12 meses
df_lucro12m = pd.read_excel(path_economatica_base, sheet_name = "lucro_12m", index_col = "Datas")
df_lucro12m_deactivate = pd.read_excel(path_economatica_deactivate, sheet_name = "lucro_12m", index_col = "Datas")
df_lucro12m = df_lucro12m.merge(df_lucro12m_deactivate, how = 'outer', left_index = True, right_index = True)

# EBTIDA
df_ebitda = pd.read_excel(path_economatica_base, sheet_name = "ebitda", index_col = "Datas") 
df_ebitda_deactivate = pd.read_excel(path_economatica_deactivate, sheet_name = "ebitda", index_col = "Datas")
df_ebitda = df_ebitda.merge(df_ebitda_deactivate, how = 'outer', left_index = True, right_index = True)

# -- Importando e organizando Equity Risk Premium

# Importar taxa de juros de 10 anos
interest_rate = pd.read_excel(path_10yinterest_rate, index_col = 'Date') 
# adding equity risk premium de 6%
long_real_rates = interest_rate.loc[: , ['10Y real interest rate']] + 6
# Renomeando colunas
long_real_rates.rename({'10Y real interest rate' : 'ke'}, axis = 1, inplace = True)


# Setando um frame para organixar as notas
Notas_preco = pd.DataFrame()


#_3.) PREÇO / LUCRO
def preco_lucro(df_preco_lucro, df_valor_mercado, df_lucro_12m, ke):

    metricas_preco_lucro = pd.DataFrame()

    #! 1.) Preço/lucro Média Aritimética
    # Ajuste: Retirada de valores negativo e P/L acima de 80
    preco_lucro_adj = df_preco_lucro.map(lambda x: np.nan if x < 0 or x > 80 else x)

    #preco_lucro_adj.to_excel(r'C:\Users\LIS CAPITAL\LIS Capital Dropbox\LIS Capital\LIS Value FIA\Macro\Sistema de dados\Database\United States\prec_lucro.xlsx')
    
    # Calculo da média aritimética
    metricas_preco_lucro['P/L - ma'] = preco_lucro_adj.mean(axis = 1) 

    #! 2.) Preço lucro com soma de preço e soma de lucro
    # Ajuste do df de valor de mercado
    valor_de_mercado_adj = pd.DataFrame(np.where(preco_lucro_adj.isna(), 0, df_valor_mercado), 
                                                 preco_lucro_adj.index, 
                                                 preco_lucro_adj.columns)
    
    # Obtenção o lucro de 12 meses com as informações que temos
    #! df_lucro_12m = valor_de_mercado_adj.div(preco_lucro_adj) 
    
    #df_lucro_12m.to_excel(r'C:\Users\LIS CAPITAL\LIS Capital Dropbox\LIS Capital\LIS Value FIA\Macro\Sistema de dados\Database\United States\df_lucro_12m.xlsx')
    
    # -- Ajuste do df de lucro: Será que precisa dessa parte 
    lucro_adj = pd.DataFrame(np.where(preco_lucro_adj.isna(), 0, df_lucro_12m), 
                             preco_lucro_adj.index, 
                             preco_lucro_adj.columns)

    # Calculo do PL pela soma do valor de mercado
    metricas_preco_lucro['P/L - Soma'] = valor_de_mercado_adj.sum(axis = 1)/lucro_adj.sum(axis = 1)
      
    # PL JUSTO
    metricas_preco_lucro['Preco_lucro - Justo'] = (1 / (ke/100)).astype('Float64')
    
    
    #! 3.) Criação dos Ratios para as notas
    metricas_preco_lucro['Ratio MA'] =  metricas_preco_lucro['P/L - ma'] / metricas_preco_lucro['Preco_lucro - Justo']
    metricas_preco_lucro['Ratio Soma'] = metricas_preco_lucro['P/L - Soma'] / metricas_preco_lucro['Preco_lucro - Justo']

    # Colocando o vetor usado na criação do mutiplo justo no frame final
    metricas_preco_lucro['ke'] = ke.astype('Float64')
    
    return metricas_preco_lucro

metricas_preco_lucro = preco_lucro(df_preco_lucro, df_valor_mercado, df_lucro12m, long_real_rates['ke'])
metricas_preco_lucro.to_excel(r'C:\Users\LIS CAPITAL\LIS Capital Dropbox\LIS Capital\Macro\Sistema de dados\oraculo\us\dados_termometro\Preco lucro (US).xlsx')

#Notas_preco['pl_ma'] = Score(metricas_preco_lucro['Ratio MA'], -1, 'PL - MA', False)
#Notas_preco['pl_soma'] = Score(metricas_preco_lucro['Ratio Soma'], -1,  'PL - Soma', False)


#_4.) PREÇO / LUCRO (Shiller)
def preco_lucro_Shiller(df_lucro_trimestral, df_valor_mercado, ke): 

    metricas_preco_lucro_Shiller = pd.DataFrame()

    # Suavização dos lucro : Média Móvel de 5 anos
    lucro_smooth = (df_lucro_trimestral.rolling(window = 20, min_periods = 8).mean()) * 4 #! deixar com min_periodos parece errado - verificar!

    #! 1.) Preço/lucro Média Aritimética
    df_preco_lucro_shiller =  df_valor_mercado.div(lucro_smooth)

    # Ajuste: Retirada de valores negativo e P/L acima de 80
    preco_lucro_shiller_adj = df_preco_lucro_shiller.map(lambda x: np.nan if x < 0 or x > 80 else x)

    # Calculo da média aritimética
    metricas_preco_lucro_Shiller['P/L - ma (Shiller)'] = preco_lucro_shiller_adj.mean(axis = 1) 

    #! 2.) Preço lucro com soma de preço e soma de lucro 
    # Ajuste do df de valor de mercado
    valor_de_mercado_adj = pd.DataFrame(np.where(preco_lucro_shiller_adj.isna(), 0, df_valor_mercado), 
                                                 preco_lucro_shiller_adj.index, 
                                                 preco_lucro_shiller_adj.columns)

    # Ajuste do df de valor de mercado
    lucro_smooth_Adj = pd.DataFrame(np.where(preco_lucro_shiller_adj.isna(), 0, lucro_smooth), 
                                             preco_lucro_shiller_adj.index, 
                                             preco_lucro_shiller_adj.columns)
    # Calculo do PL pela soma do valor de mercado
    metricas_preco_lucro_Shiller['P/L - Soma (Shiller)'] = valor_de_mercado_adj.sum(axis = 1)/lucro_smooth_Adj.sum(axis = 1)
    # PL JUSTO
    metricas_preco_lucro_Shiller['Preco_lucro - Justo'] = (1 / (ke/100)).astype('Float64')

    #! 3.) Criação dos Ratios para as notas
    metricas_preco_lucro_Shiller['Ratio MA (Shiller)'] =  metricas_preco_lucro_Shiller['P/L - ma (Shiller)'] / metricas_preco_lucro_Shiller['Preco_lucro - Justo']
    metricas_preco_lucro_Shiller['Ratio Soma (Shiller)'] = metricas_preco_lucro_Shiller['P/L - Soma (Shiller)'] / metricas_preco_lucro_Shiller['Preco_lucro - Justo']
    metricas_preco_lucro_Shiller['ke'] = ke.astype('Float64')

    return metricas_preco_lucro_Shiller

metricas_pl_shiller = preco_lucro_Shiller(df_lucro3m, df_valor_mercado, long_real_rates['ke'])
metricas_pl_shiller.to_excel(r'C:\Users\LIS CAPITAL\LIS Capital Dropbox\LIS Capital\Macro\Sistema de dados\oraculo\us\dados_termometro\Preco lucro - shiller (US).xlsx')

# Notas_preco['pl_shiller_ma']= Score(metricas_pl_shiller['Ratio MA (Shiller)'], -1,  'Ratio MA (Shiller)', False)
# Notas_preco['pl_shiller_soma'] = Score(metricas_pl_shiller['Ratio Soma (Shiller)'], -1,  'Ratio Soma (Shiller)', False)


#_4.) PRICE / BOOK 
def price_to_book(df_price_book, df_valor_mercado, df_patrimonio_liquido, df_preco_lucro, ke):
    
    medidas_price_book = pd.DataFrame()

    #! 1.) Price/Book Média Aritimética
    # Ajuste: Retirada de valores negativo e P/L acima de 80
    price_book_adj = df_price_book.map(lambda x: np.nan if x < 0 or x > 10 else x)
    # Calculo da média aritimética
    medidas_price_book['P/B - ma'] = price_book_adj.mean(axis = 1) 


    #! 2.) Preço lucro com soma de preço e soma de Patrimonio liquido
    # Ajuste do df de valor de mercado
    valor_de_mercado_adj = pd.DataFrame(np.where(price_book_adj.isna(), 0, df_valor_mercado), 
                                                 price_book_adj.index, 
                                                 price_book_adj.columns)
    
    # Ajuste do df de valor de mercado
    patrimonio_liq_adj = pd.DataFrame(np.where(price_book_adj.isna(), 0, df_patrimonio_liquido), 
                                               price_book_adj.index, 
                                               price_book_adj.columns)
    
    
    #patrimonio_liq_adj.to_excel(r'C:\Users\LIS CAPITAL\LIS Capital Dropbox\LIS Capital\LIS Value FIA\Macro\Sistema de dados\Database\United States\patrimonio_liq.xlsx')
    
    
    # Calculo do P/B pela soma do valor de mercado
    medidas_price_book['P/B - Soma'] = valor_de_mercado_adj.sum(axis = 1)/patrimonio_liq_adj.sum(axis = 1)
    

    #! 3.) P/B Justo
    # Lucro 12 meses
    lucro_12m = df_valor_mercado.div(df_preco_lucro)

    lucro_12m_adj = pd.DataFrame(np.where(price_book_adj.isna(), 0, lucro_12m), 
                                          price_book_adj.index, 
                                          price_book_adj.columns)

    medidas_price_book['ROE'] = 100 * (lucro_12m_adj.sum(axis = 1) / patrimonio_liq_adj.sum(axis = 1))

    medidas_price_book['ROE'] = remove_outliers(medidas_price_book, 'ROE')

    medidas_price_book['P/B - Justo'] = (medidas_price_book['ROE'] / ke.astype('Float64'))

    #! 3.) Criação dos Ratios para as notas
    medidas_price_book['Ratio MA'] =  medidas_price_book['P/B - ma'] / medidas_price_book['P/B - Justo']
    medidas_price_book['Ratio Soma'] = medidas_price_book['P/B - Soma'] / medidas_price_book['P/B - Justo']
    medidas_price_book['Juros'] = ke.astype('Float64')
    
    return medidas_price_book

metricas_pb = price_to_book(df_price_book, df_valor_mercado, df_patrimonio_liquido, df_preco_lucro, long_real_rates['ke'])
metricas_pb.to_excel(r'C:\Users\LIS CAPITAL\LIS Capital Dropbox\LIS Capital\Macro\Sistema de dados\oraculo\us\dados_termometro\Price to book (US).xlsx')

# Notas_preco['price_book_ma'] = Score(metricas_pb['Ratio MA'],  -1, 'Ratio MA (Shiller)', False)
# Notas_preco['price_book_soma']= Score(metricas_pb['Ratio Soma'], -1,  'Ratio MA (Shiller)', False)


#_4.) EV / EBITDA
def ev_ebitda(df_enterprise_value, df_ebitda, ke):
    
    medidas_ev_ebitda = pd.DataFrame()

    ev_ebitda = df_enterprise_value.div(df_ebitda)

    #df_ebitda.to_excel(r'C:\Users\LIS CAPITAL\LIS Capital Dropbox\LIS Capital\LIS Value FIA\Macro\Sistema de dados\Database\United States\ebitda.xlsx')
    
    #! 1.) Price/Book Média Aritimética
    # Ajuste: Retirada de valores negativo e EV/EBITDA acima de 80
    ev_ebitda_adj = ev_ebitda.map(lambda x: np.nan if x < 0 or x > 80 else x)

    # Calculo da média aritimética
    medidas_ev_ebitda['Ev/Ebitda - ma'] = ev_ebitda_adj.mean(axis = 1) 


    #! 2.) Ev/Ebitda Soma    
    # Ajuste do df de valor de mercado
    enterprise_value_adj = pd.DataFrame(np.where(ev_ebitda_adj.isna(), 0, df_enterprise_value), 
                                                 ev_ebitda_adj.index, 
                                                 ev_ebitda_adj.columns)

    # Ajuste do df de valor de mercado
    ebitda_adj = pd.DataFrame(np.where(ev_ebitda_adj.isna(), 0, df_ebitda), 
                                       ev_ebitda_adj.index, 
                                       ev_ebitda_adj.columns)

    # Calculo do EV_Ebitda pela soma do valor de mercado
    medidas_ev_ebitda['EV/Ebitda - Soma'] = enterprise_value_adj.sum(axis = 1)/ebitda_adj.sum(axis = 1)
    

    #! 3.) EV/Ebitda Justo

    ke = ke.astype('Float64')
    
    #_metricas_wacc
    taxes = 0.21
    cost_debt = ke - 6
    cost_equity = ke
    equity_weight = 0.5
    
    medidas_ev_ebitda['wacc'] = (cost_equity * equity_weight + cost_debt * (1 - equity_weight)*(1 - taxes))
    medidas_ev_ebitda['ev/ebitda - Justo'] = (1 /(medidas_ev_ebitda['wacc']/100))
    

    #! 3.) Criação dos Ratios para as notas
    medidas_ev_ebitda['Ratio MA'] =  medidas_ev_ebitda['Ev/Ebitda - ma'] / medidas_ev_ebitda['ev/ebitda - Justo']
    medidas_ev_ebitda['Ratio Soma'] = medidas_ev_ebitda['EV/Ebitda - Soma'] / medidas_ev_ebitda['ev/ebitda - Justo']
    medidas_ev_ebitda['Juros'] = ke.astype('Float64')
    

    return medidas_ev_ebitda

medidas_ev_ebitda = ev_ebitda(df_enterprise_value, df_ebitda, long_real_rates['ke'])
medidas_ev_ebitda.to_excel(r'C:\Users\LIS CAPITAL\LIS Capital Dropbox\LIS Capital\Macro\Sistema de dados\oraculo\us\dados_termometro\Ev_ebitda (US).xlsx')



print("Feito!")
# Notas_preco['ev_ebitda_ma'] = Score(medidas_ev_ebitda['Ratio MA'],  -1, 'Ratio MA (Shiller)', False)
# Notas_preco['ev_ebitda_soma']= Score(medidas_ev_ebitda['Ratio Soma'], -1,  'Ratio MA (Shiller)', False)


# # #_5.) EXPORTAÇÃO
# # Notas_preco = unpivot(Notas_preco)
# #Notas_preco.to_csv(r'C:\Users\LIS CAPITAL\LIS Capital Dropbox\LIS Capital\LIS Value FIA\BD_MACRO\ORACULO\TERMOMETRO\BRL\BRL_NOTAS_PRECO.csv')


# Notas_preco.to_excel(r'C:\Users\LIS CAPITAL\LIS Capital Dropbox\LIS Capital\LIS Value FIA\Macro\Sistema de dados\BRL_NOTAS_PRECO.xlsx')

