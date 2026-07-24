
import os
import mysql.connector
import pandas as pd
from dotenv import load_dotenv

load_dotenv()



class MySQLDataRequester:
    def __init__(self, database, table):
        """
        Inicializa a classe com as informações do banco de dados e da tabela.
        
        Args:
            database (str): Nome do schema do MySQL.
            table (str): Nome da tabela a ser consultada.
        """
        self.database = database
        self.table = table
        self.host = os.environ.get("MYSQL_HOST", "localhost")
        self.user = os.environ.get("MYSQL_USER", "root")
        self.password = os.environ.get("MYSQL_PASSWORD", "")
        self.connection = None

    def connect(self):
        """
        Conecta ao banco de dados MySQL.
        """
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
        except mysql.connector.Error as err:
            print(f"MySQL connection error: {err}")
            self.connection = None

    def request_data(self):
        """
        Recupera os dados da tabela especificada e retorna como um DataFrame.
        
        Returns:
            pd.DataFrame: DataFrame contendo os dados da tabela.
        """
        if self.connection is None:
            print("Não conectado ao banco de dados.")
            return None
        
        cursor = self.connection.cursor()
        
        query = f'SELECT * FROM {self.table}'
        
        try:
            cursor.execute(query)
            results = cursor.fetchall()
            df_requested = pd.DataFrame(data=results, columns=list(cursor.column_names))
        except mysql.connector.Error as err:
            print(f"Erro ao executar a consulta: {err}")
            df_requested = None
        finally:
            cursor.close()
        
        return df_requested

    def close_connection(self):
        """
        Fecha a conexão com o banco de dados MySQL.
        """
        if self.connection:
            self.connection.close()
            self.connection = None
    
    @staticmethod
    def explore_data(df):
        """
        Explora os dados do DataFrame fornecido e retorna informações sobre as colunas.
        
        Args:
            df (pd.DataFrame): DataFrame contendo os dados a serem explorados.
        
        Returns:
            pd.DataFrame: DataFrame com informações das colunas, incluindo nome, data inicial, data final e tipo de dado.
        """
        if df is None or df.empty:
            print("DataFrame vazio ou inválido.")
            return None
        
        exploration = (
            df.groupby('name')['date']
            .agg(data_inicial='min', data_final='max')
            .reset_index()
        )
        exploration['tipo_dado'] = df['value'].dtype

        return exploration
    
    @staticmethod
    def long_to_wide(df):
        """
        Transforma o DataFrame do formato 'long' para o formato 'wide'.
        
        Args:
            df (pd.DataFrame): DataFrame no formato 'long'.
        
        Returns:
            pd.DataFrame: DataFrame no formato 'wide' com 'name' como colunas, 'date' como índice e 'value' como células.
        """
        if df is None or df.empty:
            print("DataFrame vazio ou inválido.")
            return None
        
        df_wide = df.pivot(index='date', columns='name', values='value')
        return df_wide


class DataTransformer:
    def __init__(self, df, actual_format):
        """
        Inicializa a classe DataTransformer com um DataFrame e o formato atual dos dados.

        Args:
            df (pd.DataFrame): DataFrame contendo os dados a serem transformados.
            actual_format (str): Formato atual dos dados ('MoM', 'YoY', 'Index').
        """
        self.df = df
        self.actual_format = actual_format

    def transform_to_index(self, exclude_columns=None):
        """
        Transforma o DataFrame no formato MoM ou YoY para um formato de índice.

        Args:
            exclude_columns (list): Lista de nomes de colunas que não devem ser transformadas, mas devem permanecer no DataFrame final.

        Returns:
            pd.DataFrame: DataFrame transformado no formato de índice.
        """
        if self.actual_format == 'MoM':
            return self._transform_mom_to_index(exclude_columns)
        else:
            print(f"Não é possível transformar do formato {self.actual_format} para Index.")
            return None

    def transform_to_mom(self, exclude_columns=None):
        """
        Transforma o DataFrame no formato de índice para MoM.

        Args:
            exclude_columns (list): Lista de nomes de colunas que não devem ser transformadas, mas devem permanecer no DataFrame final.

        Returns:
            pd.DataFrame: DataFrame transformado no formato MoM.
        """
        if self.actual_format == 'Index':
            return self._transform_index_to_mom(exclude_columns)
        else:
            print(f"Não é possível transformar do formato {self.actual_format} para MoM.")
            return None

    def transform_to_yoy(self, exclude_columns=None):
        """
        Transforma o DataFrame no formato MoM para YoY.

        Args:
            exclude_columns (list): Lista de nomes de colunas que não devem ser transformadas, mas devem permanecer no DataFrame final.

        Returns:
            pd.DataFrame: DataFrame transformado no formato YoY.
        """
        if self.actual_format == 'Index':
            return self._transform_index_to_yoy(exclude_columns)
        else:
            print(f"Não é possível transformar do formato {self.actual_format} para YoY.")
            return None

    def _transform_mom_to_index(self, exclude_columns=None):
        """
        Transforma o DataFrame do formato MoM para um formato de índice.

        Args:
            exclude_columns (list): Lista de nomes de colunas que não devem ser transformadas, mas devem permanecer no DataFrame final.

        Returns:
            pd.DataFrame: DataFrame transformado no formato de índice.
        """
        df_transformed = self.df.copy()
        
        df_transformed = (df_transformed / 100 + 1).cumprod() * 100

        if exclude_columns:
            df_transformed[exclude_columns] = self.df[exclude_columns]
        
        
        return df_transformed

    def _transform_index_to_mom(self, exclude_columns=None):
        """
        Transforma o DataFrame do formato de índice para MoM.

        Args:
            exclude_columns (list): Lista de nomes de colunas que não devem ser transformadas, mas devem permanecer no DataFrame final.

        Returns:
            pd.DataFrame: DataFrame transformado no formato MoM.
        """
        df_transformed = self.df.copy()
        
        df_transformed = df_transformed.pct_change(1) * 100
        
        if exclude_columns:
            df_transformed[exclude_columns] = self.df[exclude_columns]
        
        return df_transformed
    
    def _transform_index_to_yoy(self, exclude_columns=None):
        """
        Transforma o DataFrame do formato de índice para YoY.

        Args:
            exclude_columns (list): Lista de nomes de colunas que não devem ser transformadas, mas devem permanecer no DataFrame final.

        Returns:
            pd.DataFrame: DataFrame transformado no formato YoY.
        """
        df_transformed = self.df.copy()
        
        if exclude_columns:
            df_transformed[exclude_columns] = self.df[exclude_columns]
        
        df_transformed = df_transformed.pct_change(periods=12) * 100
        
        return df_transformed













#________________________________

def insert_data_into_database(database, table, df_to_insert, batch_size=1000):
    """
    Insert data from a DataFrame into a MySQL table.

    This function connects to a MySQL database and inserts data from a DataFrame
    into a specified table. It supports converting NaN values to None for proper
    handling of NULL values in the database.

    Args:
        database (str): The name of the schema in MySql.
        table (str): The name of the table to insert data into.
        df_to_insert (pd.DataFrame): The DataFrame containing the data to be inserted.
        batch_size (int): The number of rows to insert per batch.

    Returns:
        None

    Raises:
        mysql.connector.Error: If there is an error while connecting to or interacting
                               with the MySQL database.
    """


    try:
        # Connect to the MySQL database
        connection = mysql.connector.connect(
            host=os.environ.get("MYSQL_HOST", "localhost"),
            user=os.environ.get("MYSQL_USER", "root"),
            password=os.environ.get("MYSQL_PASSWORD", ""),
            database=database,
        )
        
    except mysql.connector.Error as err:
        print(f"MySQL connection error: {err}")
        return

    cursor = connection.cursor()

    try:
        # Get the list of columns from the table
        cursor.execute(f"SHOW COLUMNS FROM {table}")
        columns = [column[0] for column in cursor.fetchall()]

        # Reorder DataFrame columns to match table columns
        df_to_insert = df_to_insert[columns]

        # Prepare the SQL query with ON DUPLICATE KEY UPDATE
        query = f"INSERT INTO {table} ({', '.join(columns)}) VALUES ({', '.join(['%s'] * len(columns))}) " \
                f"ON DUPLICATE KEY UPDATE " \
                f"{', '.join([f'{col} = VALUES({col})' for col in columns if col not in ['database_id']])}"

        # Convert NaN/NaT to None (NULL no MySQL).
        # .where() em colunas float64 nao substitui NaN por None — float nao suporta None.
        # Converter para object primeiro garante que None fica como None no tolist().
        rows = df_to_insert.astype(object).where(pd.notna(df_to_insert), None).values.tolist()
        for i in range(0, len(rows), batch_size):
            batch = rows[i:i + batch_size]
            cursor.executemany(query, batch)
            connection.commit()

        print("Data inserted successfully.")

    except mysql.connector.Error as err:
        print(f"MySQL query error: {err}")
    finally:
        cursor.close()
        connection.close()
