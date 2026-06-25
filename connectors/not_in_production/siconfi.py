

from siconfipy import get_fiscal, get_budget, br_cods, get_info


#- Relatório de Gestão Fiscal

df = get_fiscal(year = 2022, period=1, cod = 1, power = 'E')


print(df)

# print(df['anexo'].unique())

# def FiltFrame(df, column, FilterVariable):
    
#     Filtro = df[column] == FilterVariable
    
#     OutFrame = df[Filtro]

#     return OutFrame



# print(df)

# #-Primeiro Filtro

# df1 = FiltFrame(df, 'anexo', 'RGF-Anexo 02')

# print(df1['anexo'].unique())


# print(df1.columns)

# -

# df = get_budget(year = 2021, period = 6, cod = 1,)


# print(df['anexo'].unique())


# df1 = FiltFrame(df, 'anexo', 'RREO-Anexo 06')

# df2 = FiltFrame(df1, 'conta', 'RECEITAS PRIMÁRIAS CORRENTES (I)')


#- ANOTAÇÕES PARA PROXIMOS PASSOS:


# - (I) Bater os numeros encontrados nos demonstrativos com os dados encontrados nas tabelas;
#-  (II) Entender a conexão dos dados com aqueles divulgados pelo BC, assim como a questão do resultado primario e nominal;
#- (III) Não tenho certeza, mas acredito que terei que expandir o tratamento da API, ou seja, ampliar a busca por mais informações,
# - como prazo da dívida, emissão e resgate da dívida;


#- RECURSOS:

# - A estrutura e diferença entre Bugdet e Fiscal assim como os anexos abarcados, encontram-se na imagem na pasta SICONFI.
# - O manual de demonstrativos financeiros tambem se encontra na pasta;