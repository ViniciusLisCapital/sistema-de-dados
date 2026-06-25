

#_ 2.) IMPORTAR BIBLIOTECAS PROPRIAS




import pandas as pd
import numpy as np
from scipy.interpolate import interp1d



#_ 1.) FUNÇÕES DE REQUISIÇÃO E ORGANIZAÇÃO


def get_gov_bonds_base():

    url = "https://www.tesourotransparente.gov.br/ckan/dataset/df56aa42-484a-4a59-8184-7676580c81e3/resource/796d2059-14e9-44e3-80c9-2d9e30b405c1/download/PrecoTaxaTesouroDireto.csv"
    df = pd.read_csv(url, sep = ';', decimal = ',')

    return df

def interpolate_yields(input_df, maturidades_estilizadas):
    
    df = input_df.copy()

    # Converter as colunas de datas para o formato datetime
    df['Data Vencimento'] = pd.to_datetime(df['Data Vencimento'], dayfirst=True)
    df['Data Base'] = pd.to_datetime(df['Data Base'], dayfirst=True)

    # Calcular a diferença em dias para obter a maturidade em meses
    df['Maturidade (dias)'] = (df['Data Vencimento'] - df['Data Base']).dt.days
    df['Maturidade (dias)'] = df['Maturidade (dias)'].round(2)  # Arredondar as maturidades

    result_list = []

    for date, sub_df in df.groupby('Data Base'):

        df_organize = sub_df.groupby(['Maturidade (dias)']).mean(numeric_only = True)

        interp_func = interp1d(df_organize.index, df_organize['Yield'], kind='slinear', fill_value="extrapolate")

        for target_maturity in maturidades_estilizadas:
            interpolated_yield = interp_func(target_maturity)
            result_list.append({'Data Base': date, 'Maturidade (dias)': target_maturity, 'Yield': interpolated_yield})

    result = pd.DataFrame(result_list)
    return result


#_ 2.) REQUISIÇÃO DOS DADOS

class YieldProcessor:
    def __init__(self):
        pass

    @staticmethod
    def get_yields(titulos, 
                   dias_padrao = [30, 60, 90, 180, 270, 360, 450, 540, 630, 720, 810, 900, 990, 1080, 1170, 1260, 1350, 1440, 1530, 1620, 1710, 1800, 1980, 2160, 2340, 2520, 2700, 2880, 3060, 3240, 3420, 3600]):

        """
        Calcula os yields para títulos específicos e organiza-os em um DataFrame pivotado.

        Args:
        - titulos (list): Lista de títulos específicos a serem filtrados.
        - dias_padrao (list): Lista de dias padrão para interpolação de yields.

        Returns:
        - pivot_df (DataFrame): DataFrame pivotado com os yields calculados.

        """

        # Carregar os dados dos titulos publicos
        df = get_gov_bonds_base()

        # Filtrar os títulos específicos
        df_filtrado = df[df['Tipo Titulo'].isin(titulos)].copy()

        # Calcular a média das taxas de compra e venda
        df_filtrado['Yield'] = df_filtrado[['Taxa Compra Manha', 'Taxa Venda Manha']].mean(axis=1)

        # Interpolar os yields com base nos dias padrão
        df_filtrado = interpolate_yields(df_filtrado, dias_padrao)

        # Arredondar os valores de Yield para 3 casas decimais
        df_filtrado['Yield'] = df_filtrado['Yield'].astype(float)
        df_filtrado['Maturidade (dias)'] = df_filtrado['Maturidade (dias)'] / 30

        # Criar um DataFrame pivotado
        pivot_df = df_filtrado.pivot_table(index='Data Base', 
                                           columns='Maturidade (dias)', 
                                           values='Yield', aggfunc='first')

        return pivot_df

    @staticmethod
    def transformar_para_formato_long(df, adicionar_database_id=False):
        """
        Transforma o DataFrame no formato wide para long.

        Parameters:
            df (pd.DataFrame): O DataFrame no formato wide.
            adicionar_database_id (bool): Se True, adiciona uma coluna 'database_id' que une 'maturidade' e 'date'.

        Returns:
            pd.DataFrame: Um DataFrame no formato long.
        """
        # Redefine o índice
        df_reset = df.reset_index()

        # Usa o melt para transformar o DataFrame para o formato long
        df_long = df_reset.melt(id_vars=['Data Base'], var_name='maturidade', value_name='value')

        # Renomeia as colunas para 'date', 'name', e 'value'
        df_long.rename(columns={'Data Base': 'date', 'maturidade': 'name'}, inplace=True)
        df_long['name'] = df_long['name'].astype(int)

        # Adiciona a coluna 'database_id' se solicitado
        if adicionar_database_id:
            df_long['database_id'] = df_long.apply(lambda row: f"{int(float(row['name']))}M{row['date'].date().strftime('%Y-%m-%d')}" if float(row['name']) < 12
                                                else f"{int(float(row['name']) / 12)}A{row['date'].date().strftime('%Y-%m-%d')}", axis=1)

        return df_long









class YieldProcessor_v0:
    def __init__(self):
        pass

    @staticmethod
    def get_yields(titulos, 
                   dias_padrao = [30, 60, 90, 180, 270, 360, 450, 540, 630, 720, 810, 900, 990, 1080, 1170, 1260, 1350, 1440, 1530, 1620, 1710, 1800, 1980, 2160, 2340, 2520, 2700, 2880, 3060, 3240, 3420, 3600]):

        """
        Calcula os yields para títulos específicos e organiza-os em um DataFrame pivotado.

        Args:
        - titulos (list): Lista de títulos específicos a serem filtrados.
        - dias_padrao (list): Lista de dias padrão para interpolação de yields.

        Returns:
        - pivot_df (DataFrame): DataFrame pivotado com os yields calculados.

        """

        # Carregar os dados dos titulos publicos
        df = get_gov_bonds_base()

        # Filtrar os títulos específicos
        df_filtrado = df[df['Tipo Titulo'].isin(titulos)].copy()

        # Calcular a média das taxas de compra e venda
        df_filtrado['Yield'] = df_filtrado[['Taxa Compra Manha', 'Taxa Venda Manha']].mean(axis=1)

        # Interpolar os yields com base nos dias padrão
        df_filtrado = interpolate_yields(df_filtrado, dias_padrao)

        # Arredondar os valores de Yield para 3 casas decimais
        df_filtrado['Yield'] = df_filtrado['Yield'].astype(float)
        df_filtrado['Maturidade (dias)'] = df_filtrado['Maturidade (dias)'] / 30

        # Criar um DataFrame pivotado
        pivot_df = df_filtrado.pivot_table(index='Data Base', 
                                           columns='Maturidade (dias)', 
                                           values='Yield', aggfunc='first')

        return pivot_df

    @staticmethod
    def transformar_para_formato_long(df, adicionar_database_id=False):
        """
        Transforma o DataFrame no formato wide para long.

        Parameters:
            df (pd.DataFrame): O DataFrame no formato wide.
            adicionar_database_id (bool): Se True, adiciona uma coluna 'database_id' que une 'maturidade' e 'date'.

        Returns:
            pd.DataFrame: Um DataFrame no formato long.
        """
        # Redefine o índice
        df_reset = df.reset_index()

        # Usa o melt para transformar o DataFrame para o formato long
        df_long = df_reset.melt(id_vars=['Data Base'], var_name='maturidade', value_name='value')

        # Renomeia as colunas para 'date', 'name', e 'value'
        df_long.rename(columns={'Data Base': 'date', 'maturidade': 'name'}, inplace=True)

        # Adiciona a coluna 'database_id' se solicitado
        if adicionar_database_id:
            df_long['database_id'] = df_long.apply(
                lambda row: f"{int(float(row['name']))}M{row['date'].replace('/', '')}" if float(row['name']) < 12
                else f"{int(float(row['name']) / 12)}A{row['date'].replace('/', '')}", axis=1)

        return df_long

















# def get_yields(titulos, 
#                dias_padrao = [30, 60, 90, 180, 270, 360, 450, 540, 630, 720, 810, 900, 990, 1080, 1170, 1260, 1350, 1440, 1530, 1620, 1710, 1800, 1980, 2160, 2340, 2520, 2700, 2880, 3060, 3240, 3420, 3600]):

#     """
#     Calcula os yields para títulos específicos e organiza-os em um DataFrame pivotado.

#     Args:
#     - titulos (list): Lista de títulos específicos a serem filtrados.
#     - dias_padrao (list): Lista de dias padrão para interpolação de yields.

#     Returns:
#     - pivot_df (DataFrame): DataFrame pivotado com os yields calculados.

#     """

#     # Carregar os dados dos titulos publicos
#     df = get_gov_bonds_base()

#     # Filtrar os títulos específicos
#     df_filtrado = df[df['Tipo Titulo'].isin(titulos)]

#     # Calcular a média das taxas de compra e venda
#     mean_yield = df_filtrado[['Taxa Compra Manha' , 'Taxa Venda Manha']].mean(axis=1)

#     # -- Essa parte está gerando um aviso, já fiz de tudo mais ainda está gerando
#     # -- Desativando o warning 
#     # pd.options.mode.chained_assignment = None
    
#     # Inputando o Yield
#     df_filtrado.loc[:, 'Yield'] = mean_yield 
    
#     # Interpolar os yields com base nos dias padrão
#     df_filtrado = interpolate_yields(df_filtrado, dias_padrao)

#     # Arredondar os valores de Yield para 3 casas decimais
#     df_filtrado['Yield'] = df_filtrado['Yield'].astype(float)    
#     df_filtrado['Maturidade (dias)'] = df_filtrado['Maturidade (dias)'] /  30

#     # Criar um DataFrame pivotado
#     pivot_df = df_filtrado.pivot_table(index='Data Base', 
#                                        columns='Maturidade (dias)', 
#                                        values='Yield', aggfunc='first')

#     return pivot_df