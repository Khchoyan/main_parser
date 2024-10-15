import datetime
import requests
import os
import pandas as pd
from help_functions import append_date_rez_file_X
from date_functions import str_digit2month_with_date

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)


def pars_year_by_months(xlsx_path='rez_file_X_v6.xlsx'):
    data_xlsx = pd.read_excel(xlsx_path)
    date1 = pd.to_datetime(data_xlsx.dropna(subset=['Ключевая ставка']).iloc[-1]['date']).strftime('%d.%m.%Y')
    date2 = datetime.datetime.now().strftime('%d.%m.%Y')
    link_to_download = f"https://cbr.ru/Queries/UniDbQuery/DownloadExcel/132934?Posted=True&From={date1}&To={date2}&FromDate={date1.split('.')[1]}%2F{date1.split('.')[0]}%2F{date1.split('.')[2]}&ToDate={date2.split('.')[1]}%2F{date2.split('.')[0]}%2F{date2.split('.')[2]}"
    header = {
        'user-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:86.0) Gecko/20100101 Firefox/86.0'
    }
    dok_name_to_download = 'CBR_key_rate.xlsx'
    folder = os.getcwd()
    folder = os.path.join(folder, 'temp_data_for_X_factors', dok_name_to_download)
    response = requests.get(link_to_download, headers=header)
    if response.status_code == 200:
        with open(folder, 'wb') as f:
            f.write(response.content)
        print(f'Document CBR key rate was downloaded.')
    else:
        print('FAILED: The data on the site has not yet been updated', response.status_code, date1, date2)
    return 'temp_data_for_X_factors/' + dok_name_to_download


def parse_docx_document(path):
    data_xlsx = pd.read_excel(path)
    data_xlsx = data_xlsx[['Дата', 'Ключевая ставка, % годовых']]
    data_xlsx['Дата'] = data_xlsx['Дата'].apply(lambda x: str_digit2month_with_date(str(x).split('.')[0], int(str(x).split('.')[1])))
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


def CBR_key_rate_parser_main():
    path = pars_year_by_months()
    # path = 'temp_data_for_X_factors/CBR_key_rate.xlsx'
    data = parse_docx_document(path)
    print(data)
    if not data.empty:
        update_rez_file_X(data, 'Ключевая ставка')
        print('CBR key rate was updated')


# обновляется в -1 месяц. Если сегодня сентябрь, то должны быть данные за август
