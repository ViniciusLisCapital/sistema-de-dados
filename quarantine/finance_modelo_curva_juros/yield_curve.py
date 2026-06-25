"""
    Set o path para conseguir buscar as bibliotecas que não estão na pasta Termometro.
"""

import sys
sys.path.append(r'C:\Users\LIS CAPITAL\LIS Capital Dropbox\LIS Capital\LIS Value FIA\BD_MACRO\ORACULO')

import pandas as pd
# from statsmodels.tsa.seasonal import STL

from DATABASE.MYSQL_CONECTOR.My_Sql_Conector import MySQLDataRequester
from FUNCTIONS.func_Tratamento import nominal_to_real, marginal_to_index, pivot_table_to_long


# di_curve_requester = MySQLDataRequester(database='br_finance', table = 'curva_di')
# di_curve_requester.connect()


# df_diCurve = di_curve_requester.request_data()
# df_diCurve = di_curve_requester.long_to_wide(df_diCurve)
# print(df_diCurve.columns)

#df_nominal_ample_credit = ample_credit_requester.long_to_wide(df_nominal_ample_credit) 



#! 2.2) importações nativa
from datetime import datetime
from DATABASE.API_CONECTOR.B3.B3_API import verifica_disponibilidade_de_datas, CurveDiPreProcessor

#_ 3.) CONSULTA NOVAS DATAS 
# Ano, mes e dia final
year = (datetime.now().date()).year
month = (datetime.now().date()).month
day = (datetime.now().date()).day


# Ano, mes e dia inicial
data_inicial = datetime(2024, 6, 1)
data_final = datetime(year, month, day)

dts_disponiveis = verifica_disponibilidade_de_datas(data_inicial, data_final)


df_request = CurveDiPreProcessor.get_historico(dts_disponiveis) 

df_request.to_excel('curva_di_recente.xlsx')