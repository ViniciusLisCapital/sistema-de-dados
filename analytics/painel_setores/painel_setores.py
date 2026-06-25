import pandas as pd
import numpy as np
from datetime import datetime, timedelta


#_ 2.) IMPORTAR BIBLIOTECAS PROPRIAS

#! 2.2) importações nativa
from connectors.bcb import BCB_MultFrame
from connectors.ibge import ibge_get, TratarDataIbge
from utils.transforms import marginal_change_to_index, pivot_table_to_long


#! 2.3) parâmetros de data para requisição da API
dt_final = datetime.now().date()
dt_inicial = "01/01/2000"  

dt_inicial_str = dt_inicial
dt_final_str = dt_final.strftime('%d/%m/%Y')


def Request_data_bcb():

    #! BCB: MENSAL
    dict_data_bcb_mensal = {"INCC" : 192, "INCC - Mao de obra": 7461, "INCC - Materias e Serviços" : 7462, 
                            "Prod. Total Veiculos" : 1373, "Prod. de automoveis e comer. leves" : 1374, "Prod. Caminhoes" : 1375,
                            "Vendas de veiculos - Automoveis": 7384, "Vendas de veiculos - Comerciais Leves" : 7385, "Vendas de veiculos - Caminhoes": 7386,
                            "SINAPI":7495 , "Concessão de credito - Total": 20631, "Concessão de credito - PJ": 20632, "Concessão de credito - PF":20633,
                            "Tx media - Total" : 20714, "Tx media - PJ":20715, "Tx media - PF" : 20716, 
                            "Perc. Carteira de Cred. Atraso (15 - 90 dias) - Total" : 21003, "Perc. Carteira de Cred. Atraso (15 - 90 dias) - PJ" : 21004, 
                            "Perc. Carteira de Cred. Atraso (15 - 90 dias) - PF" : 21005, "Inadimplencia - Total":21082, "Inadimplencia - PJ":21083, "Inadimplencia - PF":21084,
                            "Ind. Commodities - Metal": 27576, "Ind. Commodities - Energia" : 27577,  
                            "Volume de Vendas Varejo - Total": 28473, "Volume de Vendas Varejo - Tecido, Vestuario, Calçados": 28477, "Volume de Vendas Varejo - Farmaceuticos": 28480, 
                            "Volume de Vendas Varejo - Materiais Construção":20105,
                            "Comprometimento Renda - Juros" : 29033, "Comprometimento Renda - Serviço" : 29034, "Endividamento das familias" : 29037}
    
    df_bcb_mensal = BCB_MultFrame(dict_data_bcb_mensal, dt_inicial_str, dt_final_str, Long = False)

  
    # Modeling Data
    list_transform_in_index = ['INCC', 'INCC - Mao de obra', 'INCC - Materias e Serviços', 'SINAPI']

    # Transforming from marginal to index
    for column_name in list_transform_in_index:
        df_bcb_mensal[column_name] = marginal_change_to_index(df_bcb_mensal[column_name])

    # Reframe the frame to long table (Columns --> Values, Names, Date)
    df_bcb_mensal = pivot_table_to_long(df_bcb_mensal)


    #! BCB: TRIMESTRE
    dict_data_bcb_trimestre = {"PTCC - Grandes Empresas - Aprov. Observadas" : 21397, "PTCC - Micro, Pequenas e Medias empresas - Aprov. Observadas":21399, 
                               "PTCC - Consumo - Aprov. Observadas":21401, "PTCC - Habitacional - Aprov. Observadas": 21403}
    df_bcb_trimestral = BCB_MultFrame(dict_data_bcb_trimestre, dt_inicial_str, dt_final_str)
    df_bcb_trimestral = pivot_table_to_long(df_bcb_trimestral)
    


    #_Construção Lista
    List_frames_bcb = [df_bcb_mensal, df_bcb_trimestral]

    #_Concatenar
    df_bcb = pd.concat(List_frames_bcb)


    return df_bcb
       
def request_data_ibge():
    
    #! IBGE
    pms_transporte_cargas = "https://servicodados.ibge.gov.br/api/v3/agregados/8695/periodos//variaveis/7168?localidades=N1[all]&classificacao=11046[56726]|12355[56724]"
    pim_celulose = "https://servicodados.ibge.gov.br/api/v3/agregados/8888/periodos//variaveis/12606?localidades=N1[all]&classificacao=544[129324]"
    capacidade_util_armazenagem = "https://servicodados.ibge.gov.br/api/v3/agregados/5459/periodos//variaveis/153?localidades=N1[all]&classificacao=166[114630]|11278[39324]"
    estoque_soja_milho = "https://servicodados.ibge.gov.br/api/v3/agregados/254/periodos//variaveis/150?localidades=N1[all]&classificacao=162[3045,3047]|161[0]|163[0]"
    area_plantada_rendimento_medio = "https://servicodados.ibge.gov.br/api/v3/agregados/6588/periodos//variaveis/109|36?localidades=N1[all]&classificacao=48[39441,39442,39443]"
    vacas_novilhas_abatidas_perc = 'https://servicodados.ibge.gov.br/api/v3/agregados/1092/periodos//variaveis/1000284?localidades=N1[all]&classificacao=12716[115236]|18[56,111735]|12529[118225]'
    Peso_total_carcaca_abatido = 'https://servicodados.ibge.gov.br/api/v3/agregados/1092/periodos//variaveis/285?localidades=N1[all]&classificacao=12716[115236]|18[992]|12529[118225]'
    rendimento_medio_real = "https://servicodados.ibge.gov.br/api/v3/agregados/6387/periodos//variaveis/5935?localidades=N1[all]"
    SINAPI_sp = "https://servicodados.ibge.gov.br/api/v3/agregados/647/periodos//variaveis/51?localidades=N3[35]&classificacao=314[7116]|41[786]"


    #! Requisição
    #_Transporte de cargas
    df_transporte_cargas = ibge_get(pms_transporte_cargas, 2000, 2024, "M")
    df_transporte_cargas['dt'] =  TratarDataIbge(df_transporte_cargas['dt'], "M")
    df_transporte_cargas = df_transporte_cargas.loc[:, ['Class_1','serie', 'dt']]
    df_transporte_cargas.rename({'Class_1':"Name", "serie" : "Values"}, axis = 1,  inplace=True)
    # df_transporte_cargas.rename_axis({"dt":"Date"})

    #_Prod de celulose
    df_prod_celulose = ibge_get(pim_celulose, 2000, 2024, "M")
    df_prod_celulose['dt'] =  TratarDataIbge(df_prod_celulose['dt'], "M")
    df_prod_celulose = df_prod_celulose.loc[:, ['Class_0','serie', 'dt']]
    df_prod_celulose.rename({'Class_0':"Name", 'serie': "Values"}, axis = 1, inplace=True)
    
    #_Rendimento medio real
    df_rendimento_medio_real = ibge_get(rendimento_medio_real, 2000, 2024, "M")
    df_rendimento_medio_real['dt'] =  TratarDataIbge(df_rendimento_medio_real['dt'], "M")
    df_rendimento_medio_real = df_rendimento_medio_real.loc[:, ['variavel','serie', 'dt']]
    df_rendimento_medio_real.rename({'variavel':"Name", 'serie': "Values"}, axis = 1, inplace=True)

    #_SINAPI
    df_SINAPI = ibge_get(SINAPI_sp, 2000, 2024, "M")
    df_SINAPI['dt'] =  TratarDataIbge(df_SINAPI['dt'], "M")
    df_SINAPI = df_SINAPI.loc[:, ['variavel','serie', 'dt']]
    df_SINAPI.rename({'variavel':"Name", 'serie': "Values"}, axis = 1, inplace=True)

    #_Area plantada e rendimento medio
    df_area_plantada_rendimento_medio = ibge_get(area_plantada_rendimento_medio, 2000, 2024, "M")
    df_area_plantada_rendimento_medio['variavel'] = df_area_plantada_rendimento_medio['Class_0'] + '_' + df_area_plantada_rendimento_medio['variavel']
    df_area_plantada_rendimento_medio['dt'] =  TratarDataIbge(df_area_plantada_rendimento_medio['dt'], "M")
    df_area_plantada_rendimento_medio = df_area_plantada_rendimento_medio.loc[:, ['variavel','serie', 'dt']]
    df_area_plantada_rendimento_medio.rename({'variavel':"Name", 'serie': "Values"}, axis = 1, inplace=True)


    #_vacaas_novilhas_abatidas_perc
    df_vacas_novilhas_abatidas_perc = ibge_get(vacas_novilhas_abatidas_perc, 2000, 2024, "T")
    df_vacas_novilhas_abatidas_perc['dt'] =  TratarDataIbge(df_vacas_novilhas_abatidas_perc['dt'], "T")
    df_vacas_novilhas_abatidas_perc = df_vacas_novilhas_abatidas_perc.loc[:, ['Class_1','serie', 'dt']]
    df_vacas_novilhas_abatidas_perc.rename({'Class_1':"Name", 'serie': "Values"}, axis = 1, inplace=True)
    

    #_peso_carcacas_abatidas
    df_peso_carcacas_abatidas = ibge_get(Peso_total_carcaca_abatido, 2000, 2024, "T")
    df_peso_carcacas_abatidas['dt'] =  TratarDataIbge(df_peso_carcacas_abatidas['dt'], "T")
    df_peso_carcacas_abatidas = df_peso_carcacas_abatidas.loc[:, ['variavel','serie', 'dt']]
    df_peso_carcacas_abatidas.rename({'variavel':"Name", 'serie': "Values"}, axis = 1, inplace=True)
    
    #_capacidade util
    df_capacidade_util = ibge_get(capacidade_util_armazenagem, 2000, 2024, "S")
    df_capacidade_util['dt'] =  TratarDataIbge(df_capacidade_util['dt'], "S")
    df_capacidade_util = df_capacidade_util.loc[:, ['variavel','serie', 'dt']]
    df_capacidade_util.rename({'variavel':"Name", 'serie': "Values"}, axis = 1, inplace=True)
    
    
    #_Quantidade Estoque
    df_estoque_soja_milho = ibge_get(estoque_soja_milho, 2000, 2024, "S")
    df_estoque_soja_milho['variavel'] = df_estoque_soja_milho['Class_0'] + '_' + df_estoque_soja_milho['variavel']
    df_estoque_soja_milho['dt'] =  TratarDataIbge(df_estoque_soja_milho['dt'], "S")
    df_estoque_soja_milho = df_estoque_soja_milho.loc[:, ['variavel','serie', 'dt']]
    df_estoque_soja_milho.rename({'variavel':"Name", 'serie': "Values"}, axis = 1,  inplace=True)

    #_Construção Lista
    Lista_Frames_ibge = [df_transporte_cargas, df_prod_celulose,df_rendimento_medio_real, df_SINAPI, df_area_plantada_rendimento_medio, 
                   df_area_plantada_rendimento_medio, df_vacas_novilhas_abatidas_perc, df_peso_carcacas_abatidas, df_capacidade_util,
                   df_estoque_soja_milho]
    

    #_Concatenar
    df_ibge = pd.concat(Lista_Frames_ibge)
    df_ibge.rename({"dt" : "Date"},axis = 1, inplace = True)
    

    return df_ibge
    

df_bcb = Request_data_bcb()
df_ibge =  request_data_ibge()


df = pd.concat([df_bcb, df_ibge])


df.to_csv(
    r"C:\Users\LIS CAPITAL\LIS Capital Dropbox\LIS Capital\LIS Value FIA\macro\sistema de dados\Painel de Setores\PAINEL_SETORES_BASE\base_painel_setores.csv")



