import datetime
import pandas as pd
from X_factors_parser.RZD_Parser import RZDParser
from help_functions import append_date_rez_file_X


def update_rez_file_X(data, column_name, xlsx_path='rez_file_X_v6.xlsx'):
    """
        Функция осуществляет обновление файла со всеми данными rez_file_X_v6.xlsx
    """
    data_xlsx = pd.read_excel(xlsx_path, skiprows=1)
    if list(data.index)[-1] not in list(data_xlsx['date']):
        append_date_rez_file_X()
        data_xlsx = pd.read_excel(xlsx_path, skiprows=1)

    for j in data.index:
        data_xlsx.loc[data_xlsx['date'] == j, column_name] = float(data.loc[j])

    data_xlsx.to_excel(xlsx_path, index=False, startrow=1)
    print('rez_file_X_v6.xlsx RZD date was updated')


def RZDParser_main():
    parser = RZDParser()
    last_date_in_table = pd.to_datetime(pd.read_excel('rez_file_X_v6.xlsx', skiprows=1).dropna(subset=['Погрузка на сети РЖД']).iloc[
                                                -1]['date']).strftime('%d.%m.%Y')
    start_date = f'{last_date_in_table}'
    end_date = f'{datetime.datetime.now().strftime("%d.%m.%Y")}'

    df = parser.parse_data(date_publication_0=start_date, date_publication_1=end_date)
    update_rez_file_X(df['Погрузка на сети млн тонн'], 'Погрузка на сети РЖД')



# Надо проверить работу append_date_rez_file_X()
# исправить electricity_consumption_parser.py чтобы не все данные с 2014 обновлчлись