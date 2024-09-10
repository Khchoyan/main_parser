import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup as bs
import os
import time
import datetime

from date_functions import reformate_date
from help_functions import append_date_rez_file_Y


def pars_year_by_months():
    """
    Функция для получения ссылок на документы по месяцам.
    Для ВВП реализовано возвращение названия последнего доступного месяца в конкретном году
    и ссылки на соответствующий раздел.
    """
    header = {
        'user-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:86.0) Gecko/20100101 Firefox/86.0'
    }
    time.sleep(15)
    url = f'https://www.cbr.ru/statistics/macro_itm/svs/'
    response = requests.get(url, headers=header)
    soup = bs(response.content, "html.parser")
    for i in soup.find_all('a'):
        if i.text.replace('\n', '').strip() == 'Внешняя торговля Российской Федерации товарами (по методологии ' \
                                               'платежного баланса)':
            link_to_download = f'https://www.cbr.ru' + str(i['href'])
            print(link_to_download)
            time.sleep(15)
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
    """
    Функция осуществляет парсинг документа.
    path - путь к документу (обязательно в формате .docx)
    year - текущий год
    """
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
    """
        Функция осуществляет обновление файла со всеми данными rez_file_Y_v2.xlsx
    """
    data_xlsx = pd.read_excel(xlsx_path)
    if data.values[-1][0] not in list(data_xlsx['Целевой показатель']):
        append_date_rez_file_Y()
        data_xlsx = pd.read_excel(xlsx_path)
    for c in data.columns[1:]:
        index = list(data.columns).index(c)
        for j in data.values:
            data_xlsx.loc[data_xlsx['Целевой показатель'] == j[0], c] = float(str(j[index]).replace(',', '.'))

    data_xlsx.to_excel(xlsx_path, index=False)


def Export_import_parser_main():
    """
    Основная функция. Выполняет проверку данных на полноту. Скачивет недостающие
    данные и дополняет ими файл с данными.
    """
    path = pars_year_by_months()
    data = parse_docx_document(path)
    if not data.empty:
        update_rez_file_y(data, xlsx_path='rez_file_Y_v2.xlsx')
