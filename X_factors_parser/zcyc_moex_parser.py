import pandas as pd
import os
import time
import datetime

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from help_functions import append_date_rez_file_X

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)


def pars_year_by_months():
    now = datetime.datetime.now()
    url = f'https://www.moex.com/ru/marketdata/indices/state/g-curve/archive/'

    # Путь к ChromeDriver
    driver_path = './chromedriver'

    # Путь к папке для загрузки
    download_dir = "./temp_data_for_X_factors"

    # Проверяем, существует ли папка, если нет – создаем её
    if not os.path.exists(download_dir):
        os.makedirs(download_dir)

    # Настройки для скачивания файлов
    chrome_options = webdriver.ChromeOptions()
    # chrome_options.add_argument('--headless')  # запускаем браузер в фоновом режиме
    prefs = {
        "download.default_directory": os.path.abspath(download_dir),  # Путь к папке для загрузки
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True
    }

    chrome_options.add_experimental_option("prefs", prefs)
    chrome_options.add_argument('--headless')  # запускаем браузер в фоновом режиме

    # Создаем экземпляр Service для запуска WebDriver
    service = Service(driver_path)

    # Создаем экземпляр веб-драйвера
    driver = webdriver.Chrome(service=service, options=chrome_options)
    wait = WebDriverWait(driver, 10)

    try:
        driver.get(url=url)
        input_field = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'ui-input__field')))
        input_field.send_keys('0.25,0.5,0.75,1,2,3,5,7,10,15,20,30')
        time.sleep(2)

        date_input = wait.until(EC.visibility_of_element_located(
            (By.XPATH, "//div[contains(text(), 'Начальная дата')]/following-sibling::input")))
        date_input.clear()  # Очищаем поле, если нужно
        date_input.send_keys(f"{now.replace(month=now.month - 3).strftime('%d.%m.%Y')}")  # Вводим нужную дату
        date_input.send_keys(Keys.RETURN)
        time.sleep(3)

        download_button = wait.until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, "button.ui-button.-primary.CurveArchiveExport_whitespace_2hkWi")))
        download_button.click()
        time.sleep(5)

    except Exception as e:
        print(f"Ошибка: {e}")

    finally:
        driver.quit()


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


def zcyc_moex_parser_main():
    pars_year_by_months()
    old_file_path = 'temp_data_for_X_factors/zcyc_range_calculator.csv'
    new_file_path = 'temp_data_for_X_factors/zcyc_data.csv'

    # Переименовываем файл
    try:
        os.rename(old_file_path, new_file_path)
    except FileNotFoundError:
        print(f'Файл {old_file_path} не найден')
    except Exception as e:
        print(f'Произошла ошибка: {e}')

    column_names = [
        'tradedate', 'tradetime', 'period_0.25', 'period_0.5',
        'period_0.75', 'period_1.0', 'period_2.0', 'period_3.0',
        'period_5.0', 'period_7.0', 'period_10.0', 'period_15.0', 'period_20.0', 'period_30.0'
    ]
    df = pd.read_csv('temp_data_for_X_factors/zcyc_data.csv', encoding='utf-8', sep=';', names=column_names, header=0)[1:]

    # Преобразуем столбец 'tradedate' в datetime
    df['tradedate'] = pd.to_datetime(df['tradedate'], dayfirst=True)
    # Установим столбец 'tradedate' как индекс
    df.set_index('tradedate', inplace=True)

    # Удаляем ненужный столбец 'tradetime'
    df.drop(['tradetime'], axis=1, inplace=True)

    for col in df.columns:
        df[col] = df[col].str.replace(',', '.').astype(float)

    # Если вы хотите также знать количество рабочих дней в месяце, добавим новый столбец
    monthly_days_count = df.resample('ME').count()

    # Теперь получим месячные значения и усредним по количеству рабочих дней
    monthly_avg_weighted = df.resample('ME').sum() / monthly_days_count

    update_rez_file_X(monthly_avg_weighted['period_0.25'], 'Кривая доходности ОФЗ period_0.25')

    for i in list(monthly_avg_weighted.columns[1:]):
        update_rez_file_X(monthly_avg_weighted[i], i)

    print('file zcyc moex data was update')

