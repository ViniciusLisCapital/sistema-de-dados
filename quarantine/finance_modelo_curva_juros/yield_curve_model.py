
'''Script Docs:

'''

'''Ultima atualização:

02/10/2024

'''

'''Melhorias Futuras:

a.) detalhes de blocos do codigo;

b.) Base sem a coluna indicando se está ajustado ou não

'''



#_ Importações
if "importacoes":
        
    import sys
    sys.path.append(r'C:\Users\LIS CAPITAL\LIS Capital Dropbox\LIS Capital\LIS Value FIA\BD_MACRO\ORACULO')

    import pandas as pd
    from DATABASE.mg_database.Mysql_conector.My_Sql_Conector import MySQLDataRequester

#_ Funções
def request_dados_di_from_db():
    # set up connection MySql
    reqster = MySQLDataRequester(database='br_finance', table = 'brazil_yield_curve_di')
    reqster.connect()
    
    # Request Data
    df_response = reqster.request_data()
    
    # adicionando coluna
    df_response['curve'] = 'nominal'
    
    return df_response    
def request_dados_governamentbonds_from_db():
    # set up connection MySql
    reqster = MySQLDataRequester(database='br_finance', table = 'brazil_real_yield_curve')
    reqster.connect()
    
    # Request Data
    df_response = reqster.request_data()
    
    # adicionando coluna
    df_response['curve'] = 'real'
    
    return df_response    

def export_to_excel(df_to_export, nome_arquivo):
    
    # caminho de exportação
    path = r'C:\Users\LIS CAPITAL\LIS Capital Dropbox\LIS Capital\LIS Value FIA\BD_MACRO\ORACULO\SISTEMA DE ACOMPANHAMENTO\Brasil\Finance\dados'

    # exportação
    df_to_export.to_excel(path + nome_arquivo + '.xlsx')



#_ Execução Scripts
run_as_import = 'yes'

if run_as_import == 'yes':
    
    df_response_di = request_dados_di_from_db()
    df_response_governamentbonds = request_dados_governamentbonds_from_db()
    print(len(df_response_di['name'].unique()))
    
    # export_to_excel(df_response_di, '\yield_curve_di')
    # export_to_excel(df_response_governamentbonds, '\yield_curve_governamentbonds')
  
    