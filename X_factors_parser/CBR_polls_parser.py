import requests
import time
from bs4 import BeautifulSoup as bs
import os
import pandas as pd
from help_functions import append_date_rez_file_X
from dateutil.relativedelta import relativedelta

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)


def pars_year_by_months():
    header = {
        'user-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:86.0) Gecko/20100101 Firefox/86.0'
    }
    time.sleep(5)
    url = f'https://cbr.ru/analytics/dkp/monitoring/0824/'
    response = requests.get(url, headers=header)
    soup = bs(response.content, "html.parser")
    for i in soup.find_all('a'):
        if i.text == '«Данные опросов»':
            link_to_download = f'https://www.cbr.ru' + i.get('href')
            time.sleep(5)
            dok_name_to_download = 'CBR_polls.xlsx'
            folder = os.getcwd()
            response = requests.get(link_to_download, headers=header)
            folder = os.path.join(folder, 'temp_data_for_X_factors', dok_name_to_download)
            if response.status_code == 200:
                with open(folder, 'wb') as f:
                    f.write(response.content)
                print(f'Document CBR polls was downloaded.')
            else:
                print('FAILED:', link_to_download)
            return 'temp_data_for_X_factors/' + dok_name_to_download


def parse_docx_document(path):
    data_xlsx_1 = pd.read_excel(path, sheet_name='Промышленность', skiprows=2)
    data_xlsx_2 = pd.read_excel(path, sheet_name='Экономика всего', skiprows=2)
    data_xlsx_1 = data_xlsx_1[['Отчетный период', 'Как изменился объем производства, подрядных работ, товарооборота, '
                                              'услуг? баланс ответов',  'Индикатор бизнес-климата Банка России ('
                                                                        'факт)', 'Как изменился спрос на продукцию, '
                                                                                 'товары, услуги? баланс ответов']]
    data_xlsx_2 = data_xlsx_2[['Отчетный период',  'Индикатор бизнес-климата Банка России (факт)', 'Как изменился спрос на продукцию, товары, услуги? баланс ответов']]

    data_xlsx_1 = data_xlsx_1.dropna(subset='Как изменился спрос на продукцию, товары, услуги? баланс ответов')
    data_xlsx_2 = data_xlsx_2.dropna(subset='Индикатор бизнес-климата Банка России (факт)')
    data_xlsx_1 = data_xlsx_1[-12:].reset_index(drop=True)
    data_xlsx_2 = data_xlsx_2[-12:].reset_index(drop=True)
    data_xlsx_1['Отчетный период'] = data_xlsx_1['Отчетный период'].apply(lambda x: x + relativedelta(day=31))
    data_xlsx_2['Отчетный период'] = data_xlsx_2['Отчетный период'].apply(lambda x: x + relativedelta(day=31))
    data_xlsx_1['Отчетный период'] = pd.to_datetime(data_xlsx_1['Отчетный период'])
    data_xlsx_2['Отчетный период'] = pd.to_datetime(data_xlsx_2['Отчетный период'])
    return data_xlsx_1, data_xlsx_2


def update_rez_file_X(data, column_name, xlsx_path='rez_file_X_v6.xlsx'):
    """
        Функция осуществляет обновление файла со всеми данными rez_file_X_v6.xlsx
    """
    data_xlsx = pd.read_excel(xlsx_path)
    if list(data['Отчетный период'])[-1] not in list(data_xlsx['date']):
        append_date_rez_file_X()
        data_xlsx = pd.read_excel(xlsx_path)

    for j in list(data.values):
        data_xlsx.loc[data_xlsx['date'] == j[0], column_name] = float(j[1])

    data_xlsx.to_excel(xlsx_path, index=False)


def CBR_polls_parser_main():
    path_1 = pars_year_by_months()
    # path_1 = 'temp_data_for_X_factors/CBR_polls.xlsx'
    data_1, data_2 = parse_docx_document(path_1)
    if not data_1.empty:
        update_rez_file_X(data_1[['Отчетный период', 'Как изменился спрос на продукцию, товары, услуги? баланс ответов']], 'Мониторинг предприятий ЦБ')
        update_rez_file_X(data_1[['Отчетный период', 'Индикатор бизнес-климата Банка России (факт)']], 'Бизнес климат ЦБ')
        update_rez_file_X(data_1[['Отчетный период', 'Как изменился объем производства, подрядных работ, товарооборота, услуг? баланс ответов']], 'Как изменился объем производства, подрядных работ, товарооборота, услуг? баланс ответов')
    if not data_2.empty:
        update_rez_file_X(data_2[['Отчетный период', 'Как изменился спрос на продукцию, товары, услуги? баланс ответов']], 'ЦБ опрос Как изменился спрос на продукцию, товары, услуги баланс ответов')
        update_rez_file_X(data_2[['Отчетный период', 'Индикатор бизнес-климата Банка России (факт)']], 'Индикатор бизнес-климата Банка России')
