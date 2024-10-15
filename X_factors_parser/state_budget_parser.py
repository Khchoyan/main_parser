import pandas as pd
import os
import time

from dateutil.relativedelta import relativedelta
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from date_functions import reformate_date
from help_functions import append_date_rez_file_X

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)


def pars_year_by_months():
    url = f'https://minfin.gov.ru/ru/statistics/fedbud/execute?id_57=80042-kratkaya_ezhemesyachnaya_informatsiya_ob_ispolnenii_federalnogo_byudzheta_mlrd._rub._nakopleno_s_nachala_goda'

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
    # chrome_options.add_argument('--headless')  # запускаем браузер в фоновом режиме

    # Создаем экземпляр Service для запуска WebDriver
    service = Service(driver_path)
    # Создаем экземпляр веб-драйвера
    driver = webdriver.Chrome(service=service, options=chrome_options)
    wait = WebDriverWait(driver, 10)

    try:
        driver.get(url=url)
        download_button = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//a[contains(text(), 'скачать (XLSX,  0.19 MB)')]")))
        download_button.click()
        time.sleep(5)

    except Exception as e:
        print(f"Ошибка: {e}")

    finally:
        driver.quit()


def parse_docx_document(path):
    data = pd.read_excel(path)
    data = data.iloc[1:18]
    data = data.drop(index=[2, 16])
    data.iloc[0] = data.iloc[0].apply(lambda x: x if type(x) == str else x - relativedelta(day=31))
    data.iloc[0] = data.iloc[0].apply(lambda x: reformate_date(x.split('.')[0], str('20' + x.split('.')[1])) if type(x) == str and '*' in x else x)
    data = data.drop(data.columns[[0, 1]], axis=1)
    column_name = list(data.iloc[0])
    data = data.iloc[1:]
    data.columns = column_name
    data = data.reset_index(drop=True)
    data = data.iloc[:, -12:]
    return data


def update_rez_file_X(data, column_name, xlsx_path='rez_file_X_v6.xlsx'):
    data_xlsx = pd.read_excel(xlsx_path)
    if list(data.columns)[-1] not in list(data_xlsx['date']):
        append_date_rez_file_X()
        data_xlsx = pd.read_excel(xlsx_path)

    for c in range(14):
        count = 0
        for i in data.iloc[c]:
            data_xlsx.loc[data_xlsx['date'] == list(data.columns)[count], column_name[c]] = float(i)
            count += 1

    data_xlsx.to_excel(xlsx_path, index=False)
    return 'File was download'


def state_budget_parser_main():
    pars_year_by_months()
    old_file_path = 'temp_data_for_X_factors/Prilozhenie_3_dannye_109-111_—_mes.xlsx'
    new_file_path = 'temp_data_for_X_factors/state_budget.xlsx'

    # Переименовываем файл
    try:
        os.rename(old_file_path, new_file_path)
        print(f'Файл успешно переименован в {new_file_path}')

    except FileNotFoundError:
        print(f'Файл {old_file_path} не найден')

    except Exception as e:
        print(f'Произошла ошибка: {e}')

    data = parse_docx_document(new_file_path)
    name_list = ['Доходы, всего', 'Нефтегазовые доходы', 'Ненефтегазовые доходы', 'Доходы, связанные с внутренним производством',
                 'Доходы от НДС (внутренний)', 'Доходы от акцизов', 'Доходы от налогов на прибыль',
                 'Доходы от налог на доходы физических лиц', 'Доходы связанные с импортом', 'Доходы от НДС на ввозимые товары',
                 'Доходы от акцизов на ввозимые товары', 'Доходы от ввозные пошлин', 'Прочие Доходы', 'Расходы всего']
    if not data.empty:
        print(update_rez_file_X(data, name_list))
        print('file state_budget was update')

