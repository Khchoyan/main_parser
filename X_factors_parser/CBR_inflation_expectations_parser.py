import datetime
import requests
import os
import pandas as pd
from help_functions import append_date_rez_file_X
from dateutil.relativedelta import relativedelta

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)


def pars_year_by_months():
    date = datetime.datetime.now()
    date = date.replace(month=date.month - 1).strftime('%Y-%m')[2:]
    link_to_download = f"https://cbr.ru/Collection/Collection/File/50568/stat_Infl_exp_{date}.xlsx"
    header = {
        'user-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:86.0) Gecko/20100101 Firefox/86.0'
    }
    dok_name_to_download = 'CBR_inflation_expectations.xlsx'
    folder = os.getcwd()
    folder = os.path.join(folder, 'temp_data_for_X_factors', dok_name_to_download)
    response = requests.get(link_to_download, headers=header)
    if response.status_code == 200:
        with open(folder, 'wb') as f:
            f.write(response.content)
        print(f'Document CBR inflation expectations was downloaded.')
    else:
        print('FAILED: The data on the site has not yet been updated', response.status_code)
        return 0
    return 'temp_data_for_X_factors/' + dok_name_to_download


def parse_docx_document(path, name_list):
    data_xlsx = pd.read_excel(path, sheet_name='Данные за все годы')
    date_lst = list(data_xlsx.loc[0].values)[-13:]
    date_lst = [(i - relativedelta(months=1, day=31)) for i in date_lst]
    data_xlsx = data_xlsx.loc[data_xlsx['Данные в таблице приводятся в % от всех опрошенных, если не указано иное.'].isin(name_list)][:12].reset_index(drop=True)
    data_xlsx = data_xlsx.iloc[:, -13:]
    data_xlsx.columns = date_lst
    return data_xlsx


def update_rez_file_X(data, name_list, xlsx_path='rez_file_X_v6.xlsx'):
    data_xlsx = pd.read_excel(xlsx_path)
    if list(data.columns)[-1] not in list(data_xlsx['date']):
        append_date_rez_file_X()
        data_xlsx = pd.read_excel(xlsx_path)
    for column_name in name_list:
        index = name_list.index(column_name)
        for j in list(data.columns):
            data_xlsx.loc[data_xlsx['date'] == j, column_name] = float(data[j].iloc[index])
    data_xlsx.to_excel(xlsx_path, index=False)
    print('CBR_inflation_expectations was updated')


def CBR_inflation_expectations_parser_main():
    path = pars_year_by_months()
    # path = 'temp_data_for_X_factors/CBR_inflation_expectations.xlsx'
    name_list = ['выросли очень сильно', 'выросли умеренно', 'выросли незначительно', 'не изменились', 'снизились', 'затрудняюсь ответить', 'вырастут очень сильно', 'вырастут умеренно', 'вырастут незначительно', 'не изменятся', 'снизятся', 'затрудняюсь ответить.1']
    if path == 0:
        return 0
    else:
        data = parse_docx_document(path, name_list)
        if not data.empty:
            name_list[0] = 'Инфляционные ожидания: выросли очень сильно'
            update_rez_file_X(data, name_list)
