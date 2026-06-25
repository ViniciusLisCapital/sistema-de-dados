
import json
import requests
import pandas as pd


#_ 2.) IMPORTAR BIBLIOTECAS PROPRIAS


#_FUNCTIONS

def bls_request(series_dict, start_year, end_year):
    """
    Fetch data from BLS API and convert to a long-format DataFrame with inferred dates.

    Args:
        series_dict (dict): A dictionary where keys are series IDs and values are series names.
        start_year (int): The start year for fetching data.
        end_year (int): The end year for fetching data.

    Returns:
        pd.DataFrame: A long-format DataFrame with series IDs, series names, dates, and values.
    """
    BLS_API_KEY = '8c7fe923715143688e37c1c2b069a38d'
    BLS_ENDPOINT = "https://api.bls.gov/publicAPI/v2/timeseries/data/"

    headers = {'Content-type': 'application/json'}
    data = {
        "seriesid": list(series_dict.keys()),
        "startyear": str(start_year),
        "endyear": str(end_year),
        "registrationKey": BLS_API_KEY  # Adiciona a chave da API ao payload
    }
    data = json.dumps(data)

    response = requests.post(BLS_ENDPOINT, data=data, headers=headers)
    response.raise_for_status()  # Levanta uma exceção se a solicitação falhar

    json_data = response.json()

    if json_data['status'] != 'REQUEST_SUCCEEDED':
        raise Exception(json_data['message'][0])

    all_data = []
    for series in json_data['Results']['series']:
        series_id = series['seriesID']
        series_name = series_dict[series_id]
        for item in series['data']:
            year = int(item['year'])
            period = item['period']
            value = item['value']

            # Inferir a data a partir do ano e do período
            if period.startswith('M'):
                month = int(period[1:])
                date = pd.Timestamp(year=year, month=month, day=1)
            elif period.startswith('Q'):
                quarter = int(period[1:])
                month = (quarter - 1) * 3 + 1
                date = pd.Timestamp(year=year, month=month, day=1)
            else:
                continue  # Ignorar outros tipos de períodos

            all_data.append({
                'series_id': series_id,
                'series_name': series_name,
                'date': date,
                'value': float(value)
            })

    df_response = pd.DataFrame(all_data)
    
    return  df_response


# dict_series_to_request = {'CUSR0000SAH1': 'Shelter', 'CUUR0000SAH1': 'Shelter'}

# x = bls_request(dict_series_to_request, 2024, 2024)














# #_ Dimension Table
# # Componentes selecionado do CPI
def CPI_Selection():
    cpi_selection = pd.read_excel(
                            r'C:\Users\LIS CAPITAL\LIS Capital Dropbox\LIS Capital\LIS Value FIA\BD_MACRO\ORACULO\DATABASE\mg_database\Api_conector\BLS\BLS_Codes_dimension.xlsx',
                            sheet_name = "CPI Selection")
    
    return cpi_selection