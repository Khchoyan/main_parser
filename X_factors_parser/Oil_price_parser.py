from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from datetime import datetime
from bs4 import BeautifulSoup
import pandas as pd
from help_functions import append_date_rez_file_X


def date_to_timestamp(date_str):
    date_time = datetime.strptime(date_str, '%d.%m.%Y')
    return int(date_time.timestamp())


def my_pars(x):
    try:
        return datetime.strptime(x, "%B %d, %Y")
    except:
        return datetime.strptime(x, "%b %d, %Y")


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
    print('rez_file_X_v6.xlsx oil_price was updated')


def oil_price_parser_main():
    start_date_dt = pd.to_datetime(pd.read_excel('rez_file_X_v6.xlsx', skiprows=1).dropna(subset=['Стоимость нефти']).iloc[
                                                -1]['date']).strftime('%d.%m.%Y')
    start_date = date_to_timestamp(start_date_dt)
    end_date = int(datetime.now().timestamp())

    driver_path = ''
    url = f'https://finance.yahoo.com/quote/BZ%3DF/history?guccounter=1&period1={start_date}&period2={end_date}&frequency=1wk'

    # Запускаем веб-драйвер
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # запускаем браузер в фоновом режиме

    service = Service(driver_path)
    driver = webdriver.Chrome(service=service, options=options)
    driver.get(url)

    ps = driver.page_source
    soup = BeautifulSoup(ps, 'html.parser')

    df = pd.read_html(soup.find('table').prettify())
    mdf = df[0]

    mdf['Date'] = mdf['Date'].apply(lambda x: my_pars(x))
    mdf = mdf.set_index('Date')

    df = mdf.sort_index().Open.resample('ME').mean()
    if not df.empty:
        update_rez_file_X(df, 'Стоимость нефти')
