import datetime
import numpy as np
import requests
from bs4 import BeautifulSoup
import pandas as pd
from help_functions import append_date_rez_file_X


pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)


def update_rez_file_X(data, column_name, xlsx_path='rez_file_X_v6.xlsx'):
    """
        Функция осуществляет обновление файла со всеми данными rez_file_X_v6.xlsx
    """
    data_xlsx = pd.read_excel(xlsx_path)
    if list(data.index)[-1] not in list(data_xlsx['date']):
        append_date_rez_file_X()
        data_xlsx = pd.read_excel(xlsx_path)

    for j in data.index:
        data_xlsx.loc[data_xlsx['date'] == j, column_name] = float(data.loc[j])

    data_xlsx.to_excel(xlsx_path, index=False)


def electricity_consumption_parser_main(xlsx_path='rez_file_X_v6.xlsx'):
    # потребление электроэнергии на РСВ
    data_xlsx = pd.read_excel(xlsx_path)
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

    rsv_df.DAT = rsv_df.DAT.apply(lambda x: pd.to_datetime(x, dayfirst=True))
    rsv_df['CONSUMER_PRICE'] = pd.to_numeric(rsv_df['CONSUMER_PRICE'], errors='coerce')
    rsv_df['CONSUMER_VOLUME'] = pd.to_numeric(rsv_df['CONSUMER_VOLUME'], errors='coerce')
    rsv_df = rsv_df.dropna(subset=['CONSUMER_PRICE', 'CONSUMER_VOLUME'])
    rsv_df_agg = pd.pivot_table(data=rsv_df, index='DAT',
                        values=['CONSUMER_PRICE', 'CONSUMER_VOLUME'],
                        aggfunc={'CONSUMER_PRICE': np.mean, 'CONSUMER_VOLUME': np.sum})

    rsv_df_zone = pd.pivot_table(data=rsv_df, index='DAT', columns=['PRICE_ZONE_CODE'],
                  values=['CONSUMER_PRICE', 'CONSUMER_VOLUME'])
    rsv_df = pd.concat([rsv_df_agg, rsv_df_zone], axis=1).sort_index()
    rsv_df = rsv_df.resample('ME').mean()

    update_rez_file_X(rsv_df['CONSUMER_PRICE'], 'Индекс цен на РСВ')
    update_rez_file_X(rsv_df['CONSUMER_VOLUME'], 'CONSUMER_VOLUME')
    update_rez_file_X(rsv_df[('CONSUMER_PRICE', '1')], '(CONSUMER_PRICE, 1)')
    update_rez_file_X(rsv_df[('CONSUMER_PRICE', '2')], '(CONSUMER_PRICE, 2)')
    update_rez_file_X(rsv_df[('CONSUMER_VOLUME', '1')], '(CONSUMER_VOLUME, 1)')
    update_rez_file_X(rsv_df[('CONSUMER_VOLUME', '2')], '(CONSUMER_VOLUME, 2)')
    print('rez_file_X_v6.xlsx electricity_consumption was updated')
