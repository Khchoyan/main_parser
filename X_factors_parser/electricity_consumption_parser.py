import datetime

import requests
from bs4 import BeautifulSoup
import pandas as pd
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
    print('rez_file_X_v6.xlsx electricity_consumption was updated')


def electricity_consumption_parser_main(xlsx_path='rez_file_X_v6.xlsx'):
    # потребление электроэнергии на РСВ
    data_xlsx = pd.read_excel(xlsx_path, skiprows=1)
    date1 = pd.to_datetime(data_xlsx.dropna(subset=['Индекс цен на РСВ']).iloc[-1]['date']).strftime('%Y%m%d')
    date2 = datetime.datetime.now().strftime('%Y%m%d')
    flag = int(date2[-3]) - int(date1[-3]) != 1 and int(date2[-3]) != int(date1[-3])
    if flag:
        url = f'https://www.atsenergo.ru/market/stats.xml?date1={date1}&date2={date2}&period=3'
    else:
        if int(date2[-3]) == int(date1[-3]) and int(date2[-5]) == int(date1[-5]):
            date1 = list(date1)
            date1[-3] = str(int(date1[-3]) - 1)
            date1 = ''.join(date1)
        url = f'https://www.atsenergo.ru/market/stats.xml?date1={date1}&date2={date2}&period=1'

    response = requests.get(url,  verify=False)
    soup = BeautifulSoup(response.content, 'xml')
    soup = BeautifulSoup(str(soup).replace('</col>', ';</col>'), 'xml')
    rsv_df = pd.DataFrame([i.text.split(";")[:-1] for i in soup.find_all('row')],
                          columns=[i.text for i in soup.find_all('name')])

    rsv_df = pd.pivot(data=rsv_df, index='DAT', columns=['PRICE_ZONE_CODE'],
                      values=['CONSUMER_PRICE', 'CONSUMER_VOLUME'])
    rsv_df.columns = ['CONSUMER_PRICE_1', 'CONSUMER_PRICE_2', 'CONSUMER_VOLUME_1', 'CONSUMER_VOLUME_2']
    rsv_df.index = [pd.to_datetime(i, dayfirst=True) + pd.offsets.MonthEnd() for i in rsv_df.index]
    rsv_df = rsv_df.sort_index()
    rsv_df = rsv_df.astype(float)
    rsv_df = rsv_df['CONSUMER_PRICE_1']
    if not flag:
        lst = list(rsv_df.iloc[:-1].values)
        value = sum(lst)/len(lst)
        rsv_df = pd.DataFrame({'ind': [rsv_df.index[0]], 'value': [value]})
        rsv_df.set_index('ind', inplace=True)

    update_rez_file_X(rsv_df, 'Индекс цен на РСВ')

