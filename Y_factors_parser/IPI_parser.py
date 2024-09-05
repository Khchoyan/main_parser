import pandas as pd
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
    url = f'https://rosstat.gov.ru/enterprise_industrial#'
    response = requests.get(url, headers=header)
    soup = bs(response.content, "html.parser")
    for i in soup.find_all('a', {'class': "btn btn-icon btn-white btn-br btn-sm"}):
        if '/storage/mediabank/ind_sub_2018.xlsx' in str(i.get('href')).lower():
            link_to_download = f'https://rosstat.gov.ru' + str(i.get('href'))
            print(link_to_download)
            time.sleep(15)
            dok_name_to_download = 'IPI.xlsx'
            folder = os.getcwd()
            response = requests.get(link_to_download, headers=header)
            folder = os.path.join(folder, 'temp_data', dok_name_to_download)
            if response.status_code == 200:
                with open(folder, 'wb') as f:
                    f.write(response.content)
                print(f'Document was downloaded.')
            else:
                print('FAILED:', link_to_download)
            return 'temp_data/' + dok_name_to_download


def create_dict(df, year):
    dct = {}
    date = list(df.loc[3])
    value = list(df.loc[4])
    count = 10**6
    for i in range(len(df.iloc[0])):
        if ('январь' in date[i].lower() and i != 0 and 'январь-' not in date[i].lower()) or i >= count:
            dct[reformate_date(date[i], year)] = value[i]
            count = i
        else:
            dct[reformate_date(date[i], year - 1)] = value[i]
    return dct


def update_rez_file_y(data, column_name, xlsx_path='rez_file_Y_v2.xlsx'):
    """
        Функция осуществляет обновление файла со всеми данными rez_file_Y_v2.xlsx
    """
    data_xlsx = pd.read_excel(xlsx_path)
    if list(data.keys())[-1] not in list(data_xlsx['Целевой показатель']):
        append_date_rez_file_Y()
        data_xlsx = pd.read_excel(xlsx_path)

    for j in data:
        data_xlsx.loc[data_xlsx['Целевой показатель'] == j, column_name] = data[j]

    data_xlsx.to_excel(xlsx_path, index=False)


def IPI_parser_main():
    year = datetime.datetime.now().year
    path = pars_year_by_months()
    print(path)

    df_1 = create_dict(pd.read_excel(path, sheet_name='1').loc[[3, 4]].iloc[:, -12:], year)
    df_2 = create_dict(pd.read_excel(path, sheet_name='2').loc[[3, 4]].iloc[:, -12:], year)
    df_3 = create_dict(pd.read_excel(path, sheet_name='3').loc[[3, 4]].iloc[:, -12:], year)

    update_rez_file_y(df_1, 'ИПП в % к соответствующему месяцу предыдущего года')
    update_rez_file_y(df_2, 'ИПП в % к соответствующему периоду предыдущего года')
    update_rez_file_y(df_3, 'ИПП в % к предыдущему месяцу')

