import urllib
import requests
import pandas as pd
from datetime import datetime
from help_functions import append_date_rez_file_X


def update_rez_file_X(data, column_name, xlsx_path='rez_file_X_v6.xlsx'):
    """
        Функция осуществляет обновление файла со всеми данными rez_file_X_v6.xlsx
    """
    data_xlsx = pd.read_excel(xlsx_path, skiprows=1)
    if list(data.index)[-1] not in list(data_xlsx['date']):
        append_date_rez_file_X()
        data_xlsx = pd.read_excel(xlsx_path, skiprows=1)

    for j in list(data.index):
        data_xlsx.loc[data_xlsx['date'] == j, column_name] = float(data.loc[j])

    data_xlsx.to_excel(xlsx_path, index=False, startrow=1)
    print('rez_file_X_v6.xlsx Nominal_ruble_exchange_rate was updated')


def Nominal_ruble_exchange_rate_parser_main():
    # Номинальный курс рубля
    now = datetime.now()
    c_y, c_m, c_d = now.strftime("%Y"), now.strftime("%m"), now.strftime("%d")
    last_date = pd.to_datetime(
        pd.read_excel('rez_file_X_v6.xlsx', skiprows=1).dropna(subset=['Курс Рубля к доллару США, номинальный']).iloc[
            -1]['date'])
    l_y, l_m, l_d = last_date.strftime("%Y"), last_date.strftime("%m"), last_date.strftime("%d")

    usa_url = f'https://cbr.ru/Queries/UniDbQuery/DownloadExcel/98956?Posted=True&so=1&mode=1&VAL_NM_RQ=R01235&From={l_d}.{l_m}.{l_y}&To={c_d}.{c_m}.{c_y}&FromDate={l_m}%2F{l_d}%2F{l_y}&ToDate={c_m}%2F{c_d}%2F{c_y}'

    urllib.request.urlretrieve(usa_url, f'temp_data_for_X_factors/usa_{c_y}{c_m}{c_d}.xlsx')

    update_usd = pd.read_excel(f'temp_data_for_X_factors/usa_{c_y}{c_m}{c_d}.xlsx', parse_dates=['data'], index_col='data')
    if not update_usd.empty:
        usd_exc_month = update_usd['curs'].resample('ME').mean()
        update_rez_file_X(usd_exc_month, 'Курс Рубля к доллару США, номинальный')
