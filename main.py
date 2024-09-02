import requests
from bs4 import BeautifulSoup as bs
import datetime
import time
import pandas as pd

from factor_parsers.invest_parser import run_invest_main
from factor_parsers.wage_parser import wage_parser_main
from factor_parsers.DGP_parser import DGP_parser_main
from factor_parsers.DGP_preliminary_data_parser import DGP_preliminary_data_parser_main
from factor_parsers.unemployment_parser import unemployment_parser_main
from factor_parsers.trade_turnover_parser import trade_turnover_parser_main
from factor_parsers.Export_import_parser import Export_import_parser_main
from factor_parsers.IPI_parser import IPI_parser_main
from factor_parsers.inflation_parser import inflation_parser_main


year_now = datetime.datetime.now().year
month_now = datetime.datetime.now().month
day_now = datetime.datetime.now().day

df = pd.read_excel('rez_file_Y_v2.xlsx')

# Получаем месяц последнего обновления каждого фактора
last_month_in_table_invest = pd.to_datetime(df.dropna(subset=['Инвестиции в основной '
                                                              'капитал накопленным '
                                                              'итогом, млрд руб']).iloc[
                                                -1]['Целевой показатель']).month

last_month_in_table_wage = pd.to_datetime(df.dropna(subset=['Реальные располагаемые '
                                                            'денежные доходы']).iloc[-1][
                                              'Целевой показатель']).month

last_month_in_table_DGP = pd.to_datetime(df.dropna(subset=['Реальный ВВП (Темп роста накопленным итогом)']).iloc[
                                             -1]['Целевой показатель']).month

last_month_in_table_unemployment = pd.to_datetime(df.dropna(subset=['Уровень безработицы, % к рабочей силе']).iloc[
                                                      -1]['Целевой показатель']).month

last_month_in_table_trade_turnover = pd.to_datetime(df.dropna(subset=['Розничный товарооборот']).iloc[
                                                        -1]['Целевой показатель']).month

last_month_in_table_Export_import = pd.to_datetime(df.dropna(subset=['Импорт, млн долл. США']).iloc[
                                                       -1]['Целевой показатель']).month

last_month_in_table_IPI = pd.to_datetime(df.dropna(subset=['ИПП в % к соответствующему периоду предыдущего года']).iloc[
                                             -1]['Целевой показатель']).month

last_month_in_table_inflation = pd.to_datetime(df.dropna(subset=['Инфляция, Период с начала года к соответствующему '
                                                                 'периоду предыдущего года (в среднем за год, '
                                                                 'в терминологии Минэк)']).iloc[
                                                   -1]['Целевой показатель']).month

# Условие на месяц и на дату
invest_flag = False
wage_flag = False
DGP_flag = False
DGP_preliminary_data_flag = False
unemployment_flag = False
trade_turnover_flag = False
Export_import_flag = False
IPI_flag = False
inflation_flag = False

# Здесь долежен быть день обновления каждого показателя
update_date_dict = {'invest': 10, 'wage': 10,
                    'DGP': 10, 'unemployment': 10,
                    'trade_turnover': 10, 'Export_import': 10,
                    'IPI': 10, 'inflation': 10}

# Проверяем нужно ли обновлять каждый фактор, если да, flag --> True
if (last_month_in_table_invest + 4 == month_now and update_date_dict['invest'] <= day_now) or \
        (last_month_in_table_invest + 4 < month_now):  # + 4 так как только квартальные данные
    invest_flag = True
if (last_month_in_table_wage + 2 == month_now and update_date_dict['wage'] <= day_now) or \
        (last_month_in_table_wage + 2 < month_now):
    wage_flag = True
if (last_month_in_table_DGP + 4 == month_now and update_date_dict['DGP'] <= day_now) or \
        (last_month_in_table_DGP + 4 < month_now):  # + 4 так как только квартальные данные
    DGP_flag = True
if last_month_in_table_DGP + 4 <= month_now:
    DGP_preliminary_data_flag = True
if (last_month_in_table_unemployment + 2 == month_now and update_date_dict['unemployment'] <= day_now) or \
        (last_month_in_table_unemployment + 2 < month_now):
    unemployment_flag = True
if (last_month_in_table_trade_turnover + 2 == month_now and update_date_dict['trade_turnover'] <= day_now) or \
        (last_month_in_table_trade_turnover + 2 < month_now):
    trade_turnover_flag = True
if (last_month_in_table_Export_import + 2 == month_now and update_date_dict['Export_import'] <= day_now) or \
        (last_month_in_table_Export_import + 2 < month_now):
    Export_import_flag = True
if (last_month_in_table_IPI + 2 == month_now and update_date_dict['IPI'] <= day_now) or \
        (last_month_in_table_IPI + 2 < month_now):
    IPI_flag = True
if (last_month_in_table_inflation + 2 == month_now and update_date_dict['inflation'] <= day_now) or \
        (last_month_in_table_inflation + 2 < month_now):
    inflation_flag = True


# print('inv', last_month_in_table_invest + 4 == month_now, update_date_dict['invest'] <= day_now, last_month_in_table_invest + 4 < month_now, invest_flag)
# print('wage', last_month_in_table_wage + 2 == month_now, update_date_dict['wage'] <= day_now, (
#             last_month_in_table_wage + 2 < month_now), wage_flag)
# print('ввп', last_month_in_table_DGP + 4 == month_now, update_date_dict['DGP'] <= day_now,
#       (last_month_in_table_DGP + 4 < month_now), DGP_flag)
# print(last_month_in_table_DGP + 3 <= month_now, DGP_preliminary_data_flag)
# print('безраб', last_month_in_table_unemployment + 2 == month_now, update_date_dict['unemployment'] <= day_now,
#       (last_month_in_table_unemployment + 2 < month_now), unemployment_flag)
# print('товарооборот', last_month_in_table_trade_turnover + 2 == month_now, update_date_dict['trade_turnover'] <= day_now,
#       last_month_in_table_trade_turnover + 2 < month_now, trade_turnover_flag)
# print('импорт', last_month_in_table_Export_import + 2 == month_now, update_date_dict['Export_import'] <= day_now,
#       last_month_in_table_Export_import + 2 < month_now, Export_import_flag)
# print('IPI', last_month_in_table_IPI + 2 == month_now, update_date_dict['IPI'] <= day_now,
#       last_month_in_table_IPI + 2 < month_now, IPI_flag)
# print('инф', last_month_in_table_inflation + 2 == month_now, update_date_dict['inflation'] <= day_now,
#       last_month_in_table_inflation + 2 < month_now)

# Посмотреть сколько времени нужно wage и import на обновление


def main_start_parsers():
    link_dict = {}
    year = datetime.datetime.now().year
    if trade_turnover_flag + unemployment_flag + DGP_flag + wage_flag + invest_flag + DGP_preliminary_data_flag:
        header = {'user-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:86.0) Gecko/20100101 Firefox/86.0'}
        for j in [year - 1, year]:
            url = f'https://rosstat.gov.ru/storage/mediabank/Doklad_{j}.htm'
            response = requests.get(url, headers=header)
            soup = bs(response.content, "html.parser")
            links_1 = pd.DataFrame()
            for i in range(0, len(soup.find('table').find_all('tr')[1].find_all('tr')), 2):
                month_name = soup.find('table').find_all('tr')[1].find_all('tr')[i].find_all('td')[0].text
                month_name = month_name.replace('\n', '')
                if month_name.split()[-1].lower() == 'год':
                    month_name = 'Январь-декабрь'
                dok_link = soup.find('table').find_all('tr')[1].find_all('tr')[i].find_all('td')[1].find_all('a')[0].get(
                    'href')
                if dok_link[:4] != 'http':
                    dok_link = 'https://rosstat.gov.ru' + dok_link
                pril_link = soup.find('table').find_all('tr')[1].find_all('tr')[i + 1].find_all('td')[0].find_all('a')[
                    0].get(
                    'href')
                if pril_link[:4] != 'http':
                    pril_link = 'https://rosstat.gov.ru' + pril_link
                links_1 = links_1._append([[month_name, dok_link, pril_link]])
            link_dict[j] = links_1
            time.sleep(20)

    if invest_flag:
        run_invest_main(link_dict)
        # invest_parser - Инвестиции в основной капитал накопленным итогом, млрд руб,
        # Инвестиции, % накопленным итогом год к году

    if wage_flag:
        wage_parser_main(link_dict)
        # Wage_parser - Реальные располагаемые денежные доходы,
        # Среднемесячная номинальная начисленная заработная плата, рублей,
        # Реальная заработная плата

    if DGP_flag:
        DGP_parser_main(link_dict)
        # DGP_parser - Реальный ВВП (Темп роста, квартал к кварталу прошлого года)
        # Реальный ВВП (Темп роста накопленным итогом)

    if DGP_preliminary_data_flag:
        DGP_preliminary_data_parser_main(link_dict)
        # DGP_parser - Реальный ВВП (Темп роста, квартал к кварталу прошлого года) предворительные данные

    if unemployment_flag:
        unemployment_parser_main(link_dict)
        # unemployment_parser - Уровень безработицы, % к рабочей силе

    if trade_turnover_flag:
        trade_turnover_parser_main(link_dict)
        # trade_turnover_parser - Розничный товарооборот   - переделать
        # Розничный товарооборот, темп роста, % г/г

    if Export_import_flag:
        Export_import_parser_main()
        # Export_import_parser - Импорт, млн долл. США
        # Импорт,  % накопленным итогом год к году
        # Экспорт, млн долл. США
        # Экспорт,  % накопленным итогом год к году

    if IPI_flag:
        IPI_parser_main()
        # IPI_parser - ИПП в % к соответствующему периоду предыдущего года
        # ИПП в % к соответствующему месяцу предыдущего года
        # ИПП в % к предыдущему месяцу

    if inflation_flag:
        inflation_parser_main()
        # inflation_parser - Инфляция, Период с начала года к соответствующему периоду предыдущего года (в среднем за
        # год, в терминологии Минэк)
        # К декабрю предыдущего года (в терминологии минэк на конец года в % к декабрю )
        # К предыдущему месяцу
        # К соответствующему периоду предыдущего года


if __name__ == '__main__':
    main_start_parsers()

