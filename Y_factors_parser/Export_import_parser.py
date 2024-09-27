import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup as bs
import os
import time
import datetime

from date_functions import reformate_date
from help_functions import append_date_rez_file_Y, append_date_rez_file_X


def pars_year_by_months():
    header = {
        'user-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:86.0) Gecko/20100101 Firefox/86.0'
    }
    time.sleep(3)
    url = f'https://www.cbr.ru/statistics/macro_itm/svs/'
    response = requests.get(url, headers=header)
    soup = bs(response.content, "html.parser")
    for i in soup.find_all('a'):
        if i.text.replace('\n', '').strip() == 'Внешняя торговля Российской Федерации товарами (по методологии ' \
                                               'платежного баланса)':
            link_to_download = f'https://www.cbr.ru' + str(i['href'])
            print(link_to_download)
            time.sleep(5)
            dok_name_to_download = 'export_import.xls'
            folder = os.getcwd()
            response = requests.get(link_to_download, headers=header)
            folder = os.path.join(folder, 'temp_data', dok_name_to_download)
            if response.status_code == 200:
                with open(folder, 'wb') as f:
                    f.write(response.content)
                print(f'Document Export was downloaded.')
            else:
                print('FAILED:', link_to_download)
            return 'temp_data/' + dok_name_to_download


def parse_docx_document(path):
    data_xlsx = pd.read_excel(path)
    data_xlsx = data_xlsx.iloc[:, [1, 2, 3, 8, 9]]
    count = 0
    flag = False
    data = pd.DataFrame()
    data_xlsx.columns = ['Дата', 'Экспорт, млн долл. США', 'Экспорт,  % накопленным итогом год к году', 'Импорт, млн '
                                                                                                        'долл. США',
                         'Импорт,  % накопленным итогом год к году']
    for i in data_xlsx.iloc[::-1, [1]].values:
        if not np.isnan(i[0]):
            if count != 1:
                string = data_xlsx.loc[data_xlsx['Экспорт, млн долл. США'] == i[0]].iloc[0]
                data = data._append(string)
            if flag is False:
                flag = True
        elif flag is True and np.isnan(i[0]):
            flag = False
            count += 1
        if count == 3 and np.isnan(i[0]):
            break
    year = datetime.datetime.now().year
    data = data.iloc[::-1].reset_index(drop=True)
    name_1 = 'Экспорт,  % накопленным итогом год к году'
    name_2 = 'Импорт,  % накопленным итогом год к году'
    data[name_1] = data[name_1].apply(lambda x: x/100)
    data[name_2] = data[name_2].apply(lambda x: x/100)

    for i in range(len(data)):
        if i <= 11:
            data.iloc[i, 0] = reformate_date(data.iloc[i, 0], year - 1)
        else:
            data.iloc[i, 0] = reformate_date(data.iloc[i, 0], year)

    return data


def update_rez_file_y(data, xlsx_path='rez_file_Y_v2.xlsx'):
    data_xlsx = pd.read_excel(xlsx_path)
    if data.values[-1][0] not in list(data_xlsx['Целевой показатель']):
        append_date_rez_file_Y()
        data_xlsx = pd.read_excel(xlsx_path)
    for c in data.columns[1:]:
        print(list(data.columns))
        index = list(data.columns).index(c)
        for j in data.values:
            data_xlsx.loc[data_xlsx['Целевой показатель'] == j[0], c] = float(str(j[index]).replace(',', '.'))

    data_xlsx.to_excel(xlsx_path, index=False)
    print('Document Y export_import was downloaded.')


def update_rez_file_X(data, xlsx_path='rez_file_X_v6.xlsx'):
    data_xlsx = pd.read_excel(xlsx_path)
    if data.values[-1][0] not in list(data_xlsx['date']):
        append_date_rez_file_X()
        data_xlsx = pd.read_excel(xlsx_path)
    for j in data.values:
        data_xlsx.loc[data_xlsx['date'] == j[0], 'Чистый экспорт'] = float(str(j[1]).replace(',', '.')) - float(str(j[3]).replace(',', '.'))

    data_xlsx.to_excel(xlsx_path, index=False)
    print('Document X export_import was downloaded.')


def Export_import_parser_main():
    path = pars_year_by_months()
    data = parse_docx_document(path)
    if not data.empty:
        update_rez_file_y(data, xlsx_path='rez_file_Y_v2.xlsx')
        update_rez_file_X(data, xlsx_path='rez_file_X_v6.xlsx')
