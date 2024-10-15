import requests
import time
import pandas as pd
from bs4 import BeautifulSoup as bs
from help_functions import append_date_rez_file_X
from date_functions import reformate_date
import datetime
import os

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)


def pars_year_by_months():
    header = {
        'user-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:86.0) Gecko/20100101 Firefox/86.0'
    }
    url = f'https://rosstat.gov.ru/statistics/price'
    response = requests.get(url, headers=header)
    soup = bs(response.content, "html.parser")
    for i in soup.find_all("div", {"class": "document-list__item document-list__item--row"}):
        if 'Индексы тарифов на грузовые перевозки (с 2010 г.)' in str(i.find_all("div", {"class": "document-list__item-title"})):
            link_to_download = f'https://rosstat.gov.ru' + i.find('a').get('href')
            time.sleep(3)
            dok_name_to_download = 'Freight_tariff_indices_file_X.xlsx'
            folder = os.getcwd()
            response = requests.get(link_to_download, headers=header)
            folder = os.path.join(folder, 'temp_data_for_X_factors', dok_name_to_download)
            if response.status_code == 200:
                with open(folder, 'wb') as f:
                    f.write(response.content)
            else:
                print('FAILED:', link_to_download)
            return 'temp_data_for_X_factors/' + dok_name_to_download


def parse_docx_document(path):
    xlsx = pd.ExcelFile(path)
    dct = {}
    for i in [-2, -4]:
        sheet_num = list(xlsx.sheet_names)[i]
        data = pd.read_excel(xlsx, sheet_name=sheet_num)
        year = datetime.datetime.now().year
        column_name = list(data.iloc[2])
        column_name[0] = 'Название'
        column_name = [reformate_date(i, year) if i != 'Название' else i for i in column_name]
        data = data.iloc[3:]
        data.columns = column_name
        data = data.loc[:10]
        data = data.iloc[:, 1:]
        dct[i] = data

    return dct


def update_rez_file_X(data, column_name, xlsx_path='rez_file_X_v6.xlsx'):
    data_xlsx = pd.read_excel(xlsx_path)
    if list(data.columns)[-1] not in list(data_xlsx['date']):
        append_date_rez_file_X()
        data_xlsx = pd.read_excel(xlsx_path)

    for c in range(8):
        count = 0
        for i in data.iloc[c]:
            data_xlsx.loc[data_xlsx['date'] == list(data.columns)[count], column_name[c]] = float(i)
            count += 1

    data_xlsx.to_excel(xlsx_path, index=False)
    return 'File was download'


def Freight_tariff_indices_parser_main():
    path = pars_year_by_months()
    # path = 'temp_data_for_X_factors/Freight_tariff_indices_file_X.xlsx'
    data = parse_docx_document(path)
    column_name_1 = ['Индексы тарифов на грузовые перевозки Трнаспорт - все виды, в % к предыдущему месяцу',
                   'Индексы тарифов на грузовые перевозки Железнодорожный транспорт, в % к предыдущему месяцу',
                   'Индексы тарифов на грузовые перевозки Трубопроводный транспорт, в % к предыдущему месяцу',
                   'Индексы тарифов на грузовые перевозки Морской транспорт, в % к предыдущему месяцу',
                   'Индексы тарифов на грузовые перевозки Внутренний водный транспорт, в % к предыдущему месяцу',
                   'Индексы тарифов на грузовые перевозки Автомобильный транспорт, в % к предыдущему месяцу',
                   'Индексы тарифов на грузовые перевозки Воздушный транспорт, в % к предыдущему месяцу',
                   'Индексы тарифов на грузовые перевозки Транспорт - итого (без трубопроводного), в % к предыдущему месяцу',
                   ]
    column_name_2 = ['Индексы тарифов на грузовые перевозки Трнаспорт - все виды, в % к соответствующему месяцу предыдущего года',
                     'Индексы тарифов на грузовые перевозки Железнодорожный транспорт, в % к соответствующему месяцу предыдущего года',
                     'Индексы тарифов на грузовые перевозки Трубопроводный транспорт, в % к соответствующему месяцу предыдущего года',
                     'Индексы тарифов на грузовые перевозки Морской транспорт, в % к соответствующему месяцу предыдущего года',
                     'Индексы тарифов на грузовые перевозки Внутренний водный транспорт, в % к соответствующему месяцу предыдущего года',
                     'Индексы тарифов на грузовые перевозки Автомобильный транспорт, в % к соответствующему месяцу предыдущего года',
                     'Индексы тарифов на грузовые перевозки Воздушный транспорт, в % к соответствующему месяцу предыдущего года',
                     'Индексы тарифов на грузовые перевозки Транспорт - итого (без трубопроводного), в % к соответствующему месяцу предыдущего года',
                     ]
    update_rez_file_X(data[-4], column_name_1)
    update_rez_file_X(data[-2], column_name_2)
    print('Freight_tariff_indices was update')
