
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
import requests as rq
import pandas as pd
import re



def verifica_disponibilidade_de_datas(data_inicial, data_final):
   
   
    """
    Verifica a disponibilidade de dados em datas dentro de um intervalo.

    Parâmetros:
    data_inicial (datetime): A data de início.
    data_final (datetime): A data final.

    Retorna:
    list: Uma lista de datas disponíveis no formato 'dd/mm/yyyy'.
    """

    datas_disponiveis = []

    data = data_inicial

    while data <= data_final:
        # Verifique se a data é sábado ou domingo
        if data.weekday() == 5 or data.weekday() == 6:
            # Pule os fins de semana
            data += timedelta(days=1)
            continue

        url = f"https://www2.bmf.com.br/pages/portal/bmfbovespa/boletim1/TxRef1.asp?Data={data.strftime('%d/%m/%Y')}&Data1=20231026&slcTaxa=PRE"
        page = rq.get(url)

        soup = BeautifulSoup(page.content, 'html.parser')

        # Encontre todas as tags <td> com classe "tabelaConteudo2"
        tabela_conteudo_2 = soup.find_all('td', class_='tabelaConteudo2')

        valores_tabela_conteudo_2 = [td.get_text(strip=True) for td in tabela_conteudo_2]
        
        
                                           
        if valores_tabela_conteudo_2 != ['Năo há dados para a data fornecida!']:
            datas_disponiveis.append(data.strftime('%d/%m/%Y'))
    

        data += timedelta(days=1)

    return datas_disponiveis


class CurveDiPreProcessor:
    def __init__(self):
        pass

    @staticmethod
    def get_curve_di_pre(ref_data):
        """
        Obtém as taxas da curva DI pré-fixada para uma data de referência.

        Parameters:
            ref_data (str): Data de referência no formato 'dd/mm/yyyy'.

        Returns:
            pd.DataFrame: Um DataFrame contendo as taxas da curva DI pré-fixada.
        """
        url = f"https://www2.bmf.com.br/pages/portal/bmfbovespa/boletim1/TxRef1.asp?Data={ref_data}&Data1=20240420&slcTaxa=PRE"
        print(ref_data)
        print(url)
        page = rq.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
        
        # Encontre todas as tags <td> com classe "tabelaConteudo1" e "tabelaConteudo2"
        tabela_conteudo_1 = soup.find_all('td', class_='tabelaConteudo1')
        tabela_conteudo_2 = soup.find_all('td', class_='tabelaConteudo2')

        # Extrair os valores das tabelas
        valores_tabela_conteudo_1 = [td.get_text(strip=True) for td in tabela_conteudo_1]
        valores_tabela_conteudo_2 = [td.get_text(strip=True) for td in tabela_conteudo_2]

        # Inicialize um dicionário vazio
        dados_dict = {'diascorridos': [], 'tx_252': [], 'tx_360': []}


        def _parse_rate(x):
            if x is None:
                return None
            s = str(x).strip()
            if s == '' or 'Năo há dados' in s or 'Não há dados' in s or s in ['-', '—']:
                return None
            # Remove milhares (.) e transformar vírgula em ponto decimal
            s = s.replace('.', '').replace(',', '.').replace('%', '')
            try:
                return float(s)
            except Exception:
                return None

        def _parse_day(x):
            m = re.search(r'\d+', str(x))
            if not m:
                return None
            try:
                return int(m.group())
            except Exception:
                return None

        # Percorre as duas listas de valores e extrai em blocos de 3 (dia, taxa1, taxa2)
        for tabela_info in [valores_tabela_conteudo_1, valores_tabela_conteudo_2]:
            if not tabela_info:
                continue
            for i in range(0, len(tabela_info), 3):
                # Pega elementos com verificação de índice para não estourar
                dia = tabela_info[i] if i < len(tabela_info) else None
                taxa1 = tabela_info[i + 1] if i + 1 < len(tabela_info) else None
                taxa2 = tabela_info[i + 2] if i + 2 < len(tabela_info) else None

                d = _parse_day(dia)
                if d is None:
                    # ignora entradas sem dia válido e segue em frente
                    continue

                dados_dict['diascorridos'].append(d)
                dados_dict['tx_252'].append(_parse_rate(taxa1))
                dados_dict['tx_360'].append(_parse_rate(taxa2))

        # Gera o data_frame (garante existência mesmo que vazio)
        df = pd.DataFrame(dados_dict)

        # Se houver ao menos uma linha válida, garante tipos corretos e remove linhas inválidas
        if not df.empty:
            # converte para numérico, mantendo NaN quando não for possível
            df['diascorridos'] = pd.to_numeric(df['diascorridos'], errors='coerce').astype('Int64')
            df['tx_252'] = pd.to_numeric(df['tx_252'], errors='coerce')
            df['tx_360'] = pd.to_numeric(df['tx_360'], errors='coerce')

            # remove linhas sem dia válido
            df = df[df['diascorridos'].notna()].copy()

            # converte diascorridos para int padrão (se ainda houver linhas)
            if not df.empty:
                df['diascorridos'] = df['diascorridos'].astype(int)
        else:
            # mantém DataFrame com colunas corretas caso não haja dados
            df = pd.DataFrame(columns=['diascorridos', 'tx_252', 'tx_360'])

        return df

    @staticmethod
    def padronizar_taxas(df):
        """
        Padroniza as taxas de acordo com uma lista de dias padrão.

        Parameters:
            df (pd.DataFrame): O DataFrame contendo as taxas a serem padronizadas.
            dias_padrao (list): Uma lista de dias padrão.

        Returns:
            pd.DataFrame: Um DataFrame com as taxas padronizadas.
        """

        dias_padrao = [30, 60, 90, 180, 270, 360, 450, 540, 630, 720, 810, 900, 990, 1080, 1170, 1260, 1350, 1440, 1530, 1620,
                        1710, 1800, 1980, 2160, 2340, 2520, 2700, 2880, 3060, 3240, 3420, 3600]

        # Ordenar o DataFrame pelos dias corridos
        df = df.sort_values(by='diascorridos')

        # Criar um novo DataFrame para as taxas padronizadas
        df_padronizado = pd.DataFrame({'dias_padronizados': dias_padrao})

        # Inicializar as colunas de taxas como NaN
        for col in df.columns[1:]:
            df_padronizado[col] = None

        # Para cada dia padronizado, encontrar a taxa mais próxima no DataFrame original
        for i, dia_padronizado in enumerate(dias_padrao):
            # Encontrar o índice da linha com o dia mais próximo no DataFrame original
            index = (df['diascorridos'] - dia_padronizado).abs().idxmin()

            # Copiar as taxas correspondentes para o DataFrame padronizado
            for col in df.columns[1:]:
                df_padronizado.at[i, col] = df.at[index, col]

        df_padronizado['meses_padrao'] = df_padronizado['dias_padronizados'] / 30

        df_padronizado.drop(axis=1, columns=['dias_padronizados'], inplace=True)

        return df_padronizado

    @classmethod
    def get_historico(cls, list_dates):
        """
        Obtém o histórico de taxas padronizadas da curva DI pré-fixada para uma lista de datas.

        Parameters:
            list_dates (list): Uma lista de datas de referência no formato 'dd/mm/yyyy'.

        Returns:
            pd.DataFrame: Um DataFrame contendo o histórico de taxas padronizadas para as datas fornecidas.
        """
        Out_frame = pd.DataFrame()

        for index, date in enumerate(list_dates):
            # Requisita e padroniza os dados para a data
            df = cls.get_curve_di_pre(date)
            df = cls.padronizar_taxas(df)

            if Out_frame.empty:
                # Se Out_frame estiver vazio, ajusta as colunas e índice
                Out_frame = df.drop(columns=['tx_360'])
                Out_frame.set_index('meses_padrao', inplace=True)
            else:
                # Ajusta as colunas e índice do DataFrame atual
                df = df.drop(columns=['tx_360'])
                df.set_index('meses_padrao', inplace=True)

                # Realiza a mesclagem dos DataFrames com base no índice
                Out_frame = Out_frame.merge(df, how='inner', right_index=True, left_index=True)

            # Define os nomes das colunas como as datas de referência
            Out_frame.columns = list_dates[0:index + 1]
        """ Ler comentario 1 para entender desativação"""
        # Convertendo os meses padrão em "Juros X anos" ou "Juros Y meses"
        # Out_frame.reset_index(inplace=True)
        # Out_frame['meses_padrao'] = Out_frame['meses_padrao'].apply(lambda x: f"Juros {x / 12:.1f} anos" if x >= 12 else f"Juros {int(x)} meses")

        return Out_frame

    @staticmethod
    def transformar_para_formato_long(df, list_dates, adicionar_database_id=False):
        """
        Transforma o DataFrame no formato wide para long.

        Parameters:
            df (pd.DataFrame): O DataFrame no formato wide.
            list_dates (list): Lista de datas de referência.
            adicionar_database_id (bool): Se True, adiciona uma coluna 'database_id' que une 'meses_padronizados' e 'date'.

        Returns:
            pd.DataFrame: Um DataFrame no formato long.
        """
        # Redefine o índice
        df_reset = df.reset_index()

        # Usa o melt para transformar o DataFrame para o formato long
        df_long = df_reset.melt(id_vars=['meses_padrao'], value_vars=list_dates, 
                                var_name='date', value_name='value')

        # Renomeia a coluna 'meses_padrao' para 'name'
        df_long.rename(columns={'meses_padrao': 'name'}, inplace=True)

        # Adiciona a coluna 'database_id' se solicitado
        if adicionar_database_id:
            
            df_long['database_id'] =  df_long['name'].astype(int).astype(str) + \
                                      df_long['date'].astype(str).str.replace('/', '')
            
            """ comentario 1: desativação 02/10/2024
                Desativei essa parte em 02/10/2024, pois a maturidade dos títulos ficava string, e dificultava o processo
                de analise da curva de juros, pois a maturidade não ficava ordenada (principalmente no power BI). Deixando em
                meses novamente eu terei que mudar o id da base de dados
            """
            #df_long.apply(lambda row: f"{int(float(row['name'].split()[1]) * 1):02d}M{row['date'].replace('/', '')}" if 'meses' in row['name'] else f"{int(float(row['name'].split()[1]))}A{row['date'].replace('/', '')}", axis=1)

        return df_long

class CurveDiPreProcessor_v0:
    def __init__(self):
        pass

    @staticmethod
    def get_curve_di_pre(ref_data):
        """
        Obtém as taxas da curva DI pré-fixada para uma data de referência.

        Parameters:
            ref_data (str): Data de referência no formato 'dd/mm/yyyy'.

        Returns:
            pd.DataFrame: Um DataFrame contendo as taxas da curva DI pré-fixada.
        """
        url = f"https://www2.bmf.com.br/pages/portal/bmfbovespa/boletim1/TxRef1.asp?Data={ref_data}&Data1=20231026&slcTaxa=PRE"
        page = rq.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
        
        # Encontre todas as tags <td> com classe "tabelaConteudo1" e "tabelaConteudo2"
        tabela_conteudo_1 = soup.find_all('td', class_='tabelaConteudo1')
        tabela_conteudo_2 = soup.find_all('td', class_='tabelaConteudo2')

        # Extrair os valores das tabelas
        valores_tabela_conteudo_1 = [td.get_text(strip=True) for td in tabela_conteudo_1]
        valores_tabela_conteudo_2 = [td.get_text(strip=True) for td in tabela_conteudo_2]
        for tabela_info in [valores_tabela_conteudo_1, valores_tabela_conteudo_2]:
            # Use um loop para iterar sobre a lista de valores da tabela1
            for i in range(0, len(tabela_info), 3):
                try:
                    dia = tabela_info[i]
                    taxa1 = tabela_info[i + 1]
                    taxa2 = tabela_info[i + 2]
                except IndexError:
                    print(f"Could not get to this date - continue (missing data at index {i})")
                    continue

                dados_dict['diascorridos'].append(dia)
                dados_dict['tx_252'].append(taxa1)
                dados_dict['tx_360'].append(taxa2)

                dados_dict['diascorridos'].append(dia)
                dados_dict['tx_252'].append(taxa1)
                dados_dict['tx_360'].append(taxa2)

        # Gera o data_frame
        df = pd.DataFrame(dados_dict)

        # Altera o tipo dos dados
        df['diascorridos'] = df['diascorridos'].astype(int)
        df['tx_252'] = df['tx_252'].str.replace(',', '.', regex=True).astype(float)
        df['tx_360'] = df['tx_360'].str.replace(',', '.', regex=True).astype(float)

        return df

    @staticmethod
    def padronizar_taxas(df):
        """
        Padroniza as taxas de acordo com uma lista de dias padrão.

        Parameters:
            df (pd.DataFrame): O DataFrame contendo as taxas a serem padronizadas.
            dias_padrao (list): Uma lista de dias padrão.

        Returns:
            pd.DataFrame: Um DataFrame com as taxas padronizadas.
        """

        dias_padrao = [30, 60, 90, 180, 270, 360, 450, 540, 630, 720, 810, 900, 990, 1080, 1170, 1260, 1350, 1440, 1530, 1620,
                        1710, 1800, 1980, 2160, 2340, 2520, 2700, 2880, 3060, 3240, 3420, 3600]


        # Ordenar o DataFrame pelos dias corridos
        df = df.sort_values(by='diascorridos')

        # Criar um novo DataFrame para as taxas padronizadas
        df_padronizado = pd.DataFrame({'dias_padronizados': dias_padrao})

        # Inicializar as colunas de taxas como NaN
        for col in df.columns[1:]:
            df_padronizado[col] = None

        # Para cada dia padronizado, encontrar a taxa mais próxima no DataFrame original
        for i, dia_padronizado in enumerate(dias_padrao):
            # Encontrar o índice da linha com o dia mais próximo no DataFrame original
            index = (df['diascorridos'] - dia_padronizado).abs().idxmin()

            # Copiar as taxas correspondentes para o DataFrame padronizado
            for col in df.columns[1:]:
                df_padronizado.at[i, col] = df.at[index, col]

        df_padronizado['meses_padrao'] = df_padronizado['dias_padronizados'] / 30

        df_padronizado.drop(axis=1, columns=['dias_padronizados'], inplace=True)

        return df_padronizado

    @classmethod
    def get_historico(cls, list_dates):
        """
        Obtém o histórico de taxas padronizadas da curva DI pré-fixada para uma lista de datas.

        Parameters:
            list_dates (list): Uma lista de datas de referência no formato 'dd/mm/yyyy'.

        Returns:
            pd.DataFrame: Um DataFrame contendo o histórico de taxas padronizadas para as datas fornecidas.
        """
        Out_frame = pd.DataFrame()

        for index, date in enumerate(list_dates):
            # Requisita e padroniza os dados para a data
            df = cls.get_curve_di_pre(date)
            df = cls.padronizar_taxas(df)

            if Out_frame.empty:
                # Se Out_frame estiver vazio, ajusta as colunas e índice
                Out_frame = df.drop(columns=['tx_360'])
                Out_frame.set_index('meses_padrao', inplace=True)
            else:
                # Ajusta as colunas e índice do DataFrame atual
                df = df.drop(columns=['tx_360'])
                df.set_index('meses_padrao', inplace=True)

                # Realiza a mesclagem dos DataFrames com base no índice
                Out_frame = Out_frame.merge(df, how='inner', right_index=True, left_index=True)

            # Define os nomes das colunas como as datas de referência
            Out_frame.columns = list_dates[0:index + 1]

        return Out_frame
    
