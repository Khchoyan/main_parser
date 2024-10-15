import datetime
import requests
import time
from bs4 import BeautifulSoup as bs
import os
import pandas as pd
from date_functions import reformate_date


pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)


def pars_year_by_months():
    header = {
        'user-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:86.0) Gecko/20100101 Firefox/86.0'
    }
    time.sleep(3)
    url = f'https://rosstat.gov.ru/statistics/price'
    response = requests.get(url, headers=header)
    soup = bs(response.content, "html.parser")
    for i in soup.find_all("div", {"class": "document-list__item document-list__item--row"}):
        if 'Индексы цен производителей по видам экономической деятельности (с 1998 г.)' in str(i.find_all("div", {"class": "document-list__item-title"})):
            link_to_download = f'https://rosstat.gov.ru' + i.find('a').get('href')
            time.sleep(3)
            dok_name_to_download = 'Manufacture_prices_file_X.xlsx'
            folder = os.getcwd()
            response = requests.get(link_to_download, headers=header)
            folder = os.path.join(folder, 'temp_data_for_X_factors', dok_name_to_download)
            if response.status_code == 200:
                with open(folder, 'wb') as f:
                    f.write(response.content)
                print(f'Manufacturer prices file X was downloaded.')
            else:
                print('FAILED:', link_to_download)
            return 'temp_data_for_X_factors/' + dok_name_to_download


def parse_docx_document(path):
    xlsx = pd.ExcelFile(path)
    sheet_num = list(xlsx.sheet_names)[-4:]
    data_1, data_2, data_3, data_4 = 0, 0, 0, 0
    data = pd.read_excel(xlsx, sheet_name=sheet_num)
    for i in range(len(sheet_num)):
        if 'в % к предыдущему месяцу' in list(data[sheet_num[i]].iloc[0])[0]:
            data_1 = data[sheet_num[i]]
        elif 'в % к декабрю предыдущего года' in list(data[sheet_num[i]].iloc[0])[0]:
            data_2 = data[sheet_num[i]]
        elif 'в % к соответствующему месяцу предыдущего года' in list(data[sheet_num[i]].iloc[0])[0]:
            data_3 = data[sheet_num[i]]
        elif 'в % к соответствующему периоду предыдущего года' in list(data[sheet_num[i]].iloc[0])[0]:
            data_4 = data[sheet_num[i]]
    month_name = ['январь', 'февраль', 'март', 'апрель', 'май', 'июнь', 'июль', 'август', 'сентябрь', 'октябрь', 'ноябрь', 'декабрь']
    year = datetime.datetime.now().year
    column_name_new = [pd.to_datetime(reformate_date(i, year)) for i in data_1.iloc[1].values if i in month_name]

    column_name = [pd.to_datetime(reformate_date(i, year)) if i in month_name else i for i in data_1.iloc[1].values]
    data_1 = data_1.loc[data_1.iloc[:, 0] == 'Собирательная классификационная группировка видов экономической деятельности "Промышленность" на основе ОКВЭД2 (КДЕС Ред. 2)']
    data_1.columns = column_name

    column_name = [pd.to_datetime(reformate_date(i, year)) if i in month_name else i for i in data_2.iloc[1].values]
    data_2 = data_2.loc[data_2.iloc[:,
                        0] == 'Собирательная классификационная группировка видов экономической деятельности "Промышленность" на основе ОКВЭД2 (КДЕС Ред. 2)']
    data_2.columns = column_name

    column_name = [pd.to_datetime(reformate_date(i, year)) if i in month_name else i for i in data_3.iloc[1].values]
    data_3 = data_3.loc[data_3.iloc[:,
                        0] == 'Собирательная классификационная группировка видов экономической деятельности "Промышленность" на основе ОКВЭД2 (КДЕС Ред. 2)']
    data_3.columns = column_name

    column_name = [pd.to_datetime(reformate_date(i, year)) if i in month_name else i for i in data_4.iloc[1].values]
    data_4 = data_4.loc[data_4.iloc[:,
                        0] == 'Собирательная классификационная группировка видов экономической деятельности "Промышленность" на основе ОКВЭД2 (КДЕС Ред. 2)']
    data_4.columns = column_name

    update_rez_file_X(data_1[column_name_new], 'Индекс цен производителей, в % к предыдущему месяцу')
    update_rez_file_X(data_2[column_name_new], 'Индекс цен производителей, в % к декабрю предыдущего года')
    update_rez_file_X(data_3[column_name_new], 'Индекс цен производителей, в % к соответствующему месяцу предыдущего года')
    update_rez_file_X(data_4[column_name_new], 'Индекс цен производителей, в % к соответствующему периоду предыдущего года')

    return 1


def update_rez_file_X(data, column_name, xlsx_path='rez_file_X_v6.xlsx'):
    data_xlsx = pd.read_excel(xlsx_path)

    for j in list(data):
        data_xlsx.loc[data_xlsx['date'] == j, column_name] = float(data[j].iloc[0])

    data_xlsx.to_excel(xlsx_path, index=False)


def manufacturer_prices_parser_main():
    path = pars_year_by_months()
    # path = 'temp_data_for_X_factors/Manufacture_prices_file_X.xlsx'
    flag = parse_docx_document(path)
    if flag:
        print('retail_turnover_file_X was updated')
