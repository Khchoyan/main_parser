import platform
from calendar import monthrange
from bs4 import BeautifulSoup as bs
import datetime
import pandas as pd
import doc2docx
import requests
import os
import time


def get_os_type():
    os_type = platform.system()
    if os_type == "Windows":
        return "Windows"
    elif os_type == "Darwin" or os_type == "Linux":
        return "Unix"
    else:
        return "Unknown"


def doc_to_docx(path: str):
    """
    Функция конвертирует документ формата .doc в формат .docx
    doc_path - абсолютный путь к документу
    """
    exist_system = get_os_type()
    if exist_system == 'Unix':
        doc2docx.convert(path)

    elif exist_system == 'Windows':
        from win32com import client as wc
        w = wc.Dispatch('Word.Application')

        doc = w.Documents.Open(path)
        doc.SaveAs(path + 'x', 16)
        doc.Close()
        w.Quit()
        print(f'Document {path} was converted to docx-format.')

    return path + 'x'


def create_new_date(last_date_in_file_year, last_date_in_file_month):
    now = datetime.datetime.now()
    lst_date = []
    _, last_day = monthrange(now.year, now.month)
    last_date = datetime.datetime.strptime(f"{now.year}-{now.month}-{last_day}", "%Y-%m-%d").date()
    for i in range((last_date.year - last_date_in_file_year) * 12 + last_date.month - last_date_in_file_month):
        if last_date.month - 1 != 0:
            _, last_day = monthrange(last_date.year, last_date.month - i)
            last_date = datetime.datetime.strptime(f"{last_date.year}-{last_date.month - i}-{last_day}", "%Y-%m-%d").date()
        else:
            _, last_day = monthrange(last_date.year - 1, 12)
            last_date = datetime.datetime.strptime(f"{last_date.year - 1}-{12}-{last_day}", "%Y-%m-%d").date()
        lst_date.append(last_date)
    return sorted(lst_date)


def append_date_rez_file_Y(xlsx_path='rez_file_Y_v2.xlsx'):
    """
        Функция осуществляет дабавление месяцев, если их нет в файле.
    """
    data_xlsx = pd.read_excel(xlsx_path)
    year = pd.to_datetime(data_xlsx['Целевой показатель'].iloc[-1]).year
    month = pd.to_datetime(data_xlsx['Целевой показатель'].iloc[-1]).month
    date_lst = create_new_date(year, month)
    for date in date_lst:
        new_string = {'Целевой показатель': [date]}
        new_string.update({c: [None] for c in data_xlsx.columns[1:]})
        new_string = pd.DataFrame(new_string)
        if not data_xlsx.empty and not new_string.empty:
            data_xlsx = pd.concat([data_xlsx, new_string])
    data_xlsx.to_excel(xlsx_path, index=False)


def append_date_rez_file_X(xlsx_path='rez_file_X_v6.xlsx'):
    """
        Функция осуществляет дабавление месяцев, если их нет в файле.
    """
    data_xlsx = pd.read_excel(xlsx_path)
    year = pd.to_datetime(data_xlsx['date'].iloc[-1]).year
    month = pd.to_datetime(data_xlsx['date'].iloc[-1]).month
    date_lst = create_new_date(year, month)
    for date in date_lst:
        new_string = {'date': [date]}
        new_string.update({c: [None] for c in data_xlsx.columns[1:]})
        new_string = pd.DataFrame(new_string)
        if not data_xlsx.empty and not new_string.empty:
            data_xlsx = pd.concat([data_xlsx, new_string])
    data_xlsx.to_excel(xlsx_path, index=False)


def pars_cbr_date_for_file_X(url, pattern_type, pattern, file_name):
    header = {
        'user-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:86.0) Gecko/20100101 Firefox/86.0'
    }
    response = requests.get(url, headers=header)
    soup = bs(response.content, "html.parser")
    for i in soup.find_all('a'):
        if i.get(pattern_type) == pattern:
            link_to_download = 'https://cbr.ru/' + i.get('href')
            time.sleep(5)
            dok_name_to_download = file_name
            folder = os.getcwd()
            response = requests.get(link_to_download, headers=header)
            folder = os.path.join(folder, 'temp_data_for_X_factors', dok_name_to_download)
            if response.status_code == 200:
                with open(folder, 'wb') as f:
                    f.write(response.content)
                print(f'Document {file_name} was downloaded.')
            else:
                print('FAILED:', link_to_download)
            return 'temp_data_for_X_factors/' + dok_name_to_download

