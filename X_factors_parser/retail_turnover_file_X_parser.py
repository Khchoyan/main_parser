import requests
import os
import time
from bs4 import BeautifulSoup as bs
import pandas as pd

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)


def pars_year_by_months():
    header = {
        'user-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:86.0) Gecko/20100101 Firefox/86.0'
    }
    url = f'https://rosstat.gov.ru/leading_indicators'
    response = requests.get(url, headers=header)
    soup = bs(response.content, "html.parser")
    for i in soup.find_all("div", {"class": "document-list__item document-list__item--row"}):
        if 'Розничная торговля' in str(i.find_all("div", {"class": "document-list__item-title"})):
            link_to_download = f'https://rosstat.gov.ru' + i.find('a').get('href')
            time.sleep(3)
            dok_name_to_download = 'retail_turnover_file_X.xls'
            folder = os.getcwd()
            response = requests.get(link_to_download, headers=header)
            folder = os.path.join(folder, 'temp_data_for_X_factors', dok_name_to_download)
            if response.status_code == 200:
                with open(folder, 'wb') as f:
                    f.write(response.content)
                print(f'retail turnover file X was downloaded.')
            else:
                print('FAILED:', link_to_download)
            return 'temp_data_for_X_factors/' + dok_name_to_download


def parse_docx_document(path):
    name_list = ["Индекс предринимательской уверенности 2006-2023гг.\n(в  % )", "Экономическая ситуация 2006-2023гг.\n(Баланс оценок изменения значения показателя) фактические значения", "Экономическая ситуация 2006-2023гг.\n(Баланс оценок изменения значения показателя) перспективы изменения",
                 "Складские запасы 2006-2021гг.\n(Баланс оценок уровня складских запасов )", 'Средняя численность работников 2006-2023гг. (Баланс оценок изменения значения показателя) фактические значения', 'Средняя численность работников 2006-2023гг. (Баланс оценок изменения значения показателя) перспективы изменения',
                 'Оборот розничной торговли 2006-2023гг. (Баланс оценок изменения значения показателя) фактические значения', 'Оборот розничной торговли 2006-2023гг. (Баланс оценок изменения значения показателя) перспективы изменения', "Ассортимент товаров 2006-2023гг.\n(Баланс оценок уровня складских запасов ) фактические значения",
                 "Ассортимент товаров 2006-2023гг.\n(Баланс оценок уровня складских запасов ) перспективы изменения", 'Цены реализации 2006-2023гг. (Баланс оценок изменения значения показателя) фактические значения', 'Цены реализации 2006-2023гг. (Баланс оценок изменения значения показателя) перспективы изменения',
                 'Средний сложившийся уровень торговой наценки 2006-2023гг. (в % к стоимости проданных товаров)', 'Прибыль 2006-2023гг. (Баланс оценок изменения значения показателя) фактические значения', 'Прибыль 2006-2023гг. (Баланс оценок изменения значения показателя) перспективы изменения', "Складские площади 2006-2023гг.\n(Баланс оценок уровня складских запасов ) фактические значения",
                 "Складские площади 2006-2023гг.\n(Баланс оценок уровня складских запасов ) перспективы изменения", 'Обеспеченность собственными финансовыми ресурсами 2006-2023гг. (Баланс оценок изменения значения показателя) фактические значения', 'Обеспеченность собственными финансовыми ресурсами 2006-2023гг. (Баланс оценок изменения значения показателя) перспективы изменения',
                 'Инвестиции на расширение деятельности, ремонт и модернизацию 2006-2023гг. (Баланс оценок изменения значения  показателя) фактические значения', 'Инвестиции на расширение деятельности, ремонт и модернизацию 2006-2023гг. (Баланс оценок изменения значения  показателя) перспективы изменения']
    count = 0
    xlsx_file = pd.ExcelFile(path)
    sheet_names = xlsx_file.sheet_names[1:]
    columns_name = ['Дата', 'I', 'II', 'III', 'IV']
    data_xlsx = pd.read_excel(xlsx_file, sheet_name=sheet_names, skiprows=4)
    for i in list(data_xlsx.keys())[:-1]:
        data = data_xlsx[i]
        data = data.iloc[1:, -5:]
        data.columns = columns_name
        data = data.dropna(subset=['I', 'Дата']).reset_index(drop=True)
        if len(set(data['Дата'])) != len(list(data['Дата'])):
            data_1 = data.iloc[-len(list(data['Дата']))//2:].reset_index(drop=True)
            data_2 = data.iloc[len(list(data['Дата']))//2:].reset_index(drop=True)
            update_rez_file_X(data_1.iloc[-2:], name_list[count])
            update_rez_file_X(data_2.iloc[-2:], name_list[count + 1])
            count += 2
        else:
            update_rez_file_X(data.iloc[-2:], name_list[count])
            count += 1

    count = 0
    name_list = ['13.1. Недостаточный платежеспособный спрос', '13.2. Недостаток финансовых средств', '13.3. Высокий уровень налогов', '13.4. Высокая арендная плата', '13.5. Высокая конкуренция со стороны других организаций розничной торговли', '13.6. Высокие транспортные расходы ']
    data = data_xlsx[list(data_xlsx.keys())[-1]]
    data = data.iloc[1:, -5:]
    data.columns = columns_name
    data = data.dropna(subset=['I', 'Дата']).reset_index(drop=True)
    data_lst = [data.iloc[:len(data)//6], data.iloc[len(data)//6:len(data)//3], data.iloc[len(data)//3:len(data)//2], data.iloc[len(data)//2:len(data)//3 * 2], data.iloc[len(data)//3 * 2:len(data)//6 * 5], data.iloc[len(data)//6 * 5:]]
    for data in data_lst:
        update_rez_file_X(data.iloc[-2:], name_list[count])
        count += 1


def update_rez_file_X(data, column_name, xlsx_path='rez_file_X_v6.xlsx'):
    data_xlsx = pd.read_excel(xlsx_path)

    for j in list(data.values):
        data_xlsx.loc[data_xlsx['date'] == pd.to_datetime(f'{int(j[0])}-3-31'), column_name] = float(j[1])
        data_xlsx.loc[data_xlsx['date'] == pd.to_datetime(f'{int(j[0])}-6-30'), column_name] = float(j[2])
        data_xlsx.loc[data_xlsx['date'] == pd.to_datetime(f'{int(j[0])}-9-30'), column_name] = float(j[3])
        data_xlsx.loc[data_xlsx['date'] == pd.to_datetime(f'{int(j[0])}-12-31'), column_name] = float(j[4])

    data_xlsx.to_excel(xlsx_path, index=False)


def retail_turnover_file_X_parser_main():
    path = pars_year_by_months()
    # path = 'temp_data_for_X_factors/retail_turnover_file_X.xls'
    parse_docx_document(path)
    print('retail_turnover_file_X was updated')
