import requests
import time
from bs4 import BeautifulSoup as bs
import os
import pandas as pd
from help_functions import append_date_rez_file_X
from dateutil.relativedelta import relativedelta


def pars_year_by_months():
    header = {
        'user-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:86.0) Gecko/20100101 Firefox/86.0'
    }
    time.sleep(5)
    url = f'https://cbr.ru/ec_research/mb/'
    response = requests.get(url, headers=header)
    soup = bs(response.content, "html.parser")
    for i in soup.find_all('a'):
        if i.get('id') == 'a_108631file':
            link_to_download = 'https://cbr.ru/' + i.get('href')
            time.sleep(5)
            dok_name_to_download = 'CBR_news_index.xlsx'
            folder = os.getcwd()
            response = requests.get(link_to_download, headers=header)
            folder = os.path.join(folder, 'temp_data_for_X_factors', dok_name_to_download)
            if response.status_code == 200:
                with open(folder, 'wb') as f:
                    f.write(response.content)
                print(f'Document CBR news index was downloaded.')
            else:
                print('FAILED:', link_to_download)
            return 'temp_data_for_X_factors/' + dok_name_to_download


def parse_docx_document(path):
    data_xlsx = pd.read_excel(path)
    data_xlsx = data_xlsx[['Unnamed: 0', 'Новостной индекс']]
    data_xlsx.columns = ['Дата', 'Новостной индекс']
    data_xlsx = data_xlsx[-12:].reset_index(drop=True)
    data_xlsx['Дата'] = data_xlsx['Дата'].apply(lambda x: x - relativedelta(months=1, day=31))
    data_xlsx['Дата'] = pd.to_datetime(data_xlsx['Дата'])
    return data_xlsx


def update_rez_file_X(data, column_name, xlsx_path='rez_file_X_v6.xlsx'):
    """
        Функция осуществляет обновление файла со всеми данными rez_file_X_v6.xlsx
    """
    data_xlsx = pd.read_excel(xlsx_path)
    if list(data['Дата'])[-1] not in list(data_xlsx['date']):
        append_date_rez_file_X()
        data_xlsx = pd.read_excel(xlsx_path)

    for j in list(data.values):
        data_xlsx.loc[data_xlsx['date'] == j[0], column_name] = float(j[1])

    data_xlsx.to_excel(xlsx_path, index=False)
    print('CBR_news_index was updated')


def CBR_news_index_parser_main():
    path = pars_year_by_months()
    # path = 'temp_data_for_X_factors/CBR_news_index.xlsx'
    data = parse_docx_document(path)
    if not data.empty:
        update_rez_file_X(data, 'Новостной индекс ЦБ')

