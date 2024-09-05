import pandas as pd
import os
import time
import datetime

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

from help_functions import append_date_rez_file_Y
from date_functions import reformate_date


pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)


def reformat_date(date: str, year):
    """
    Функция переформатирует даты
    """
    date = date.strip()
    flag = True if ((year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)) else False
    if date == 'январь':
        date = '31 january'
    elif date == 'февраль' and flag:
        date = '29 february'
    elif date == 'февраль':
        date = '28 february'
    elif date == 'март':
        date = '31 march'
    elif date == 'апрель':
        date = '30 April'
    elif date == 'май':
        date = '31 may'
    elif date == 'июнь':
        date = '30 june'
    elif date == 'июль':
        date = '31 july'
    elif date == 'август':
        date = '31 august'
    elif date == 'сентябрь':
        date = '30 september'
    elif date == 'октябрь':
        date = '31 october'
    elif date == 'ноябрь':
        date = '30 november'
    elif date == 'декабрь':
        date = '31 december'
    return date + str(year)


def get_data():
    # Ссылка на сайт, который парсим
    url = 'https://fedstat.ru/indicator/31074'

    # Укажите путь к ChromeDriver
    driver_path = './chromedriver'  # Замените на свой путь к драйверу

    # Путь к папке для загрузки
    download_dir = "./temp_data"

    # Проверяем, существует ли папка, если нет – создаем её
    if not os.path.exists(download_dir):
        os.makedirs(download_dir)

    # Настройки для скачивания файлов
    chrome_options = webdriver.ChromeOptions()
    prefs = {
        "download.default_directory": os.path.abspath(download_dir),  # Путь к папке для загрузки
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True
    }

    chrome_options.add_experimental_option("prefs", prefs)

    # Создаем экземпляр Service для запуска WebDriver
    service = Service(driver_path)

    # Создаем экземпляр веб-драйвера
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        driver.get(url=url)
        wait_10 = WebDriverWait(driver, 15)

        # Нажимаем на кнопку
        button = wait_10.until(EC.element_to_be_clickable((By.ID, 'setting_tab')))
        button.click()
        time.sleep(3)

        action_chain = ActionChains(driver)

        elements_to_drag = [
            ('//p[@data-field="3"]',
             '//p[text()="Классификатор объектов административно-территориального деления (ОКАТО)"]'),
            ('//p[@data-field="33560"]',
             '//p[text()="Классификатор объектов административно-территориального деления (ОКАТО)"]')
        ]

        for source_xpath, target_xpath in elements_to_drag:
            source_element = wait_10.until(EC.visibility_of_element_located((By.XPATH, source_xpath)))
            target_element = wait_10.until(EC.visibility_of_element_located((By.XPATH, target_xpath)))

            # Используем click_and_hold для перетаскивания
            action_chain.click_and_hold(source_element).move_to_element(target_element).release().perform()
            time.sleep(1)  # Небольшая пауза между перетаскиванием элементов

        # Обновляем
        refresh_button = wait_10.until(
            EC.element_to_be_clickable((By.XPATH, '//button[contains(@class, "agrid-action-preview-refresh")]')))
        refresh_button.click()
        time.sleep(20)  # Ждем, пока таблица загрузится

        # Фильтр таблицы по наименованию региона (Берем только РФ)
        find_btn = wait_10.until(EC.element_to_be_clickable(
            (By.XPATH, '//a[contains(@class, "k-grid-filter") and contains(@class, "k-state-active")]')))
        find_btn.click()
        time.sleep(1)

        clear_button = wait_10.until(
            EC.element_to_be_clickable((By.XPATH, '//button[contains(@class, "k-button") and text()="Очистить"]')))
        clear_button.click()
        time.sleep(1)

        # тыкаем галачку
        item = wait_10.until(
            EC.visibility_of_element_located((By.XPATH, "//label[contains(text(), 'Российская Федерация')]"))
        )

        # Найдите чекбокс внутри этого элемента
        checkbox = item.find_element(By.XPATH, './/input[@type="checkbox"]')

        # Прокрутите к чекбоксу (если требуется)
        driver.execute_script("arguments[0].scrollIntoView(true);", checkbox)

        # Используем JavaScript для установки галочки, так как чекбокс скрыт
        if not checkbox.is_selected():  # Проверяем, установлен ли чекбокс
            driver.execute_script("arguments[0].click();", checkbox)
        time.sleep(1)

        filter_button = wait_10.until(EC.element_to_be_clickable((By.XPATH,
                                                                  '//button[@type="submit" and contains(@class, '
                                                                  '"k-button") and contains(@class, "k-primary") and '
                                                                  'contains(@class, "k-filter-load") and text('
                                                                  ')="Фильтровать"]')))

        filter_button.click()
        time.sleep(12)  # ждем пока таблица загрузиться

        # Фильтр таблицы товарам (Выбираем одну строку товары и услуги)
        filter_button_product = wait_10.until(
            EC.element_to_be_clickable(
                (By.XPATH, '//th[contains(@data-field, "58273")]//a[contains(@class, "k-grid-filter")]')))

        filter_button_product.click()
        time.sleep(1)

        clear_button_product = wait_10.until(
            EC.element_to_be_clickable((By.XPATH, '//button[contains(@class, "k-button") and text()="Очистить"]')))
        clear_button_product.click()
        time.sleep(1)

        item = wait_10.until(
            EC.visibility_of_element_located((By.XPATH, '//label[contains(text(), "Все товары и услуги")]')))

        # Найдите чекбокс внутри этого элемента
        checkbox_product = item.find_element(By.XPATH, './/input[@type="checkbox"]')

        # Прокрутите к чекбоксу, если требуется
        driver.execute_script("arguments[0].scrollIntoView(true);", checkbox_product)

        # Убедитесь, что чекбокс не отмечен, и используйте JavaScript для установки галочки
        if not checkbox_product.is_selected():  # Проверяем, установлен ли чекбокс
            driver.execute_script("arguments[0].click();", checkbox_product)

        filter_button = wait_10.until(EC.element_to_be_clickable((By.XPATH,
                                                                  '//button[@type="submit" and contains(@class, '
                                                                  '"k-button") and contains(@class, '
                                                                  '"k-primary") and contains(@class, "k-filter-load") '
                                                                  'and text()="Фильтровать"]')))

        filter_button.click()
        time.sleep(20)  # ждем пока таблица загрузиться

        # Фильтр таблицы по месецам (Выбираем 12 пунктов)

        filter_button_product = wait_10.until(
            EC.element_to_be_clickable(
                (By.XPATH, '//th[contains(@data-field, "33560")]//a[contains(@class, "k-grid-filter")]')))
        filter_button_product.click()
        time.sleep(1)

        clear_button_product = wait_10.until(
            EC.element_to_be_clickable((By.XPATH, '//button[contains(@class, "k-button") and text()="Очистить"]')))
        clear_button_product.click()
        time.sleep(1)

        # Список элементов чекбоксов, которые нужно выбрать
        checkbox_texts = [
            "январь", "февраль",
            "март", "апрель",
            "май", "июнь",
            "июль", "август",
            "сентябрь", "октябрь",
            "ноябрь", "декабрь"
        ]

        for text in checkbox_texts:

            checkbox_label = wait_10.until(
                EC.visibility_of_element_located((By.XPATH, f'//label[contains(text(), "{text}")]'))
            )

            checkbox = checkbox_label.find_element(By.XPATH, './/input[@type="checkbox"]')

            # Прокрутите к чекбоксу, если требуется
            driver.execute_script("arguments[0].scrollIntoView(true);", checkbox)

            # Убедитесь, что чекбокс не отмечен, и используйте JavaScript для установки галочки
            if not checkbox.is_selected():  # Проверяем, установлен ли чекбокс
                driver.execute_script("arguments[0].click();", checkbox)

        filter_button = wait_10.until(EC.element_to_be_clickable((By.XPATH,
                                                                  '//button[@type="submit" and contains(@class, '
                                                                  '"k-button") and contains(@class, '
                                                                  '"k-primary") and contains(@class, "k-filter-load") '
                                                                  'and text()="Фильтровать"]')))

        filter_button.click()
        time.sleep(12)  # ждем пока таблица загрузиться

        # Фильтр таблицы по нужным данным (Выбираем 4 пункта)
        # К декабрю предыдущего года
        # К предыдущему месяцу
        # К соответствующему периоду предыдущего года
        # Период с начала года к соответствующему периоду предыдущего года

        button_product = wait_10.until(
            EC.element_to_be_clickable(
                (By.XPATH, '//th[contains(@data-field, "57937")]//a[contains(@class, "k-grid-filter")]')))
        button_product.click()
        time.sleep(1)

        clear_button_product = wait_10.until(
            EC.element_to_be_clickable((By.XPATH, '//button[contains(@class, "k-button") and text()="Очистить"]')))
        clear_button_product.click()
        time.sleep(1)

        # Список элементов чекбоксов, которые нужно выбрать
        checkbox_texts = [
            "К декабрю предыдущего года",
            "К предыдущему месяцу",
            "К соответствующему периоду предыдущего года",
            "Период с начала года к соответствующему периоду"
        ]

        for text in checkbox_texts:

            checkbox_label = wait_10.until(
                EC.visibility_of_element_located((By.XPATH, f'//label[contains(text(), "{text}")]'))
            )

            checkbox = checkbox_label.find_element(By.XPATH, './/input[@type="checkbox"]')

            # Прокрутите к чекбоксу, если требуется
            driver.execute_script("arguments[0].scrollIntoView(true);", checkbox)

            # Убедитесь, что чекбокс не отмечен, и используйте JavaScript для установки галочки
            if not checkbox.is_selected():  # Проверяем, установлен ли чекбокс
                driver.execute_script("arguments[0].click();", checkbox)

        filter_button = wait_10.until(EC.element_to_be_clickable((By.XPATH,
                                                                  '//button[@type="submit" and contains(@class, '
                                                                  '"k-button") and contains(@class, '
                                                                  '"k-primary") and contains(@class, "k-filter-load") '
                                                                  'and text()="Фильтровать"]')))

        filter_button.click()
        time.sleep(12)  # ждем пока таблица загрузиться

        download_button = wait_10.until(EC.element_to_be_clickable(
            (By.XPATH, "//button[contains(@class, 'dropdown_trigger') and contains(text(), 'Скачать')]")))

        # Нажимаем кнопку "Скачать"
        download_button.click()
        time.sleep(3)

        # Ждем появления кнопки "Выбранные данные"
        selected_data_button = wait_10.until(EC.element_to_be_clickable((By.ID, "download_excel_file")))

        # Нажимаем кнопку "Выбранные данные"
        selected_data_button.click()

        time.sleep(15)  # Ждем завершения скачивания
        print(f'Document was downloaded.')

    finally:
        driver.quit()


def update_rez_file_y(data, xlsx_path='rez_file_Y_v2.xlsx'):
    """
        Функция осуществляет обновление файла со всеми данными rez_file_Y_v2.xlsx
    """
    data_xlsx = pd.read_excel(xlsx_path)
    if data.values[-1][0] not in list(data_xlsx['Целевой показатель']):
        append_date_rez_file_Y()
        data_xlsx = pd.read_excel(xlsx_path)

    my_dct = {'К декабрю предыдущего года':
              'К декабрю предыдущего года (в терминологии минэк на конец года в % к декабрю )',
              'К предыдущему месяцу': 'К предыдущему месяцу',
              'К соответствующему периоду предыдущего года': 'К соответствующему периоду предыдущего года',
              'Период с начала года к соответствующему периоду предыдущего года': 'Инфляция, Период с начала года к '
                                                                                  'соответствующему периоду '
                                                                                  'предыдущего года (в среднем за '
                                                                                  'год, в терминологии Минэк)'}
    for c in data.columns[4:]:
        for j in data[c]:
            index = list(data[c]).index(j)
            data_xlsx.loc[data_xlsx['Целевой показатель'] == data.loc[index]['month'], my_dct[c]] = j

    data_xlsx.to_excel(xlsx_path, index=False)


def inflation_parser_main():
    get_data()

    old_file_path = 'temp_data/data.xls'
    new_file_path = 'temp_data/inflation.xls'

    # Переименовываем файл
    try:
        os.rename(old_file_path, new_file_path)
        print(f'Файл успешно переименован в {new_file_path}')

    except FileNotFoundError:
        print(f'Файл {old_file_path} не найден')

    except Exception as e:
        print(f'Произошла ошибка: {e}')

    year = datetime.datetime.now().year
    data = pd.read_excel(new_file_path).loc[1:]
    lst_name = list(data.loc[1])[4:]
    data.columns = ['region_name', 'product_name', 'year', 'month'] + [i for i in lst_name]
    data = data[1:].reset_index()
    del data['index']
    data['month'] = data['month'].apply(lambda x: reformate_date(x, year))
    update_rez_file_y(data)
    print(f'File update_rez_file_y was updated')
