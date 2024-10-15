import datetime
import requests
import os
import pandas as pd
from help_functions import append_date_rez_file_X
from dateutil.relativedelta import relativedelta

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)


def pars_year_by_months(flag=False):
    date = datetime.datetime.now()
    date = date.replace(month=date.month - 1 - flag).strftime('%Y-%m')[2:]
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
        print('FAILED: The data on the site has not yet been updated', response.status_code, date)
        if date == datetime.datetime.now().replace(month=datetime.datetime.now().month - 1).strftime('%Y-%m')[2:]:
            pars_year_by_months(flag=True)
        else:
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


def parse_docx_documen_unemploymence(path):
    data_xlsx = pd.read_excel(path, sheet_name='Данные за все годы')
    date_lst = list(data_xlsx.loc[0].values)[-13:]
    date_lst = [(i - relativedelta(months=1, day=31)) for i in date_lst]

    # про безработицу
    ind = data_xlsx.loc[data_xlsx['Данные в таблице приводятся в % от всех опрошенных, если не указано иное.'] == 'Как Вы считаете, что из перечисленного будет происходить в ближайший год в экономике страны по такому показателю, как безработица? Посмотрите на карточку и дайте ответ.'].index
    data_1 = data_xlsx.loc[[i for i in range(ind[0] + 1, ind[0] + 5)]]
    data_1 = data_1.iloc[:, -13:]
    data_1.columns = date_lst


    # Про сбережения
    ind_2 = data_xlsx.loc[data_xlsx['Данные в таблице приводятся в % от всех опрошенных, если не указано иное.'] == 'покупать дорогостоящие товары'].index[0]
    data_2 = data_xlsx.loc[[ind_2 - 3, ind_2 - 1, ind_2, ind_2 + 1]]
    data_2 = data_2.iloc[:, -13:]
    data_2.columns = date_lst


    # про потребительские настроения и ожидания
    ind_3 = data_xlsx.loc[data_xlsx[
                              'Данные в таблице приводятся в % от всех опрошенных, если не указано иное.'] == 'индекс потребительских настроений (в пунктах)'].index[
        0]
    data_3 = data_xlsx.loc[[ind_3, ind_3 + 2, ind_3 + 4, ind_3 + 6, ind_3 + 12, ind_3 + 14]]
    data_3 = data_3.iloc[:, -13:]
    data_3.columns = date_lst
    return data_1, data_2, data_3


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


def CBR_inflation_expectations_parser_main():
    path = pars_year_by_months()
    # path = 'temp_data_for_X_factors/CBR_inflation_expectations.xlsx'
    name_list_data = ['выросли очень сильно', 'выросли умеренно', 'выросли незначительно', 'не изменились', 'снизились', 'затрудняюсь ответить', 'вырастут очень сильно', 'вырастут умеренно', 'вырастут незначительно', 'не изменятся', 'снизятся', 'затрудняюсь ответить.1']
    name_list_data_1 = ['вырастет', 'не изменится', 'снизится', 'затрудняюсь ответить.3']
    name_list_data_2 = ['Сберегательные настроения, баланс ответов ("хорошее" минус "плохое")', 'откладывать, беречь', 'покупать дорогостоящие товары', 'затрудняюсь ответить.2']
    name_list_data_3 = ['индекс потребительских настроений (в пунктах)', 'индекс ожиданий  (в пунктах)', 'индекс текущего состояния  (в пунктах)', 'индекс оценки изменения личного материального положения за последний год (в пунктах)', 'индекс ожидания изменения личного материального положения в ближайший год (в пунктах)', 'индекс крупных покупок (в пунктах)']
    if path == 0:
        return 0
    else:
        data = parse_docx_document(path, name_list_data)
        data_1, data_2, data_3 = parse_docx_documen_unemploymence(path)
        if not data.empty:
            name_list_data[0] = 'Инфляционные ожидания: выросли очень сильно'
            update_rez_file_X(data, name_list_data)
            update_rez_file_X(data_1, name_list_data_1)
            update_rez_file_X(data_2, name_list_data_2)
            update_rez_file_X(data_3, name_list_data_3)

        print('CBR_inflation_expectations was updated')

