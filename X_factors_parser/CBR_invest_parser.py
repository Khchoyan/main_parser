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
    url = f'https://cbr.ru/statistics/bank_sector/sors/'
    response = requests.get(url, headers=header)
    soup = bs(response.content, "html.parser")
    for i in soup.find_all('a'):
        if i.get('id') == 'a_63101':
            link_to_download = 'https://cbr.ru/' + i.get('href')
            time.sleep(5)
            dok_name_to_download = 'CBR_invest.xlsx'
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
    data = pd.read_excel(path, sheet_name='итого', skiprows=1)
    data = data.iloc[[0, 1, 2, 3, 6], [0, -4, -3, -2, -1]]
    return data


def update_rez_file_X(data, column_name, xlsx_path='rez_file_X_v6.xlsx'):
    data_xlsx = pd.read_excel(xlsx_path)
    if list(data.index)[-1] not in list(data_xlsx['date']):
        append_date_rez_file_X()
        data_xlsx = pd.read_excel(xlsx_path)

    for j in data.index[1:]:
        data_xlsx.loc[data_xlsx['date'] == j - relativedelta(months=1, day=31), column_name] = float(data.loc[j])

    data_xlsx.to_excel(xlsx_path, index=False)


def CBR_invest_parser_main():
    path = pars_year_by_months()
    # path = 'temp_data_for_X_factors/CBR_invest.xlsx'
    data = parse_docx_document(path)
    if not data.empty:
        update_rez_file_X(data.iloc[0], 'Средства клиентов, всего, млн руб.')
        update_rez_file_X(data.iloc[1], '    средства на счетах организаций, млн руб.')
        update_rez_file_X(data.iloc[2], '    депозиты юридических лиц*, млн руб.')
        update_rez_file_X(data.iloc[3], '    вклады (депозиты) и другие привлеченные средства физических лиц (с учето')
        update_rez_file_X(data.iloc[4], '    средства индивидуальных предпринимателей, млн руб.')
        print('rez_file_X_v6.xlsx CBR_invest date was updated')
