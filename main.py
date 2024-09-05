import requests
from bs4 import BeautifulSoup as bs
import datetime
import time
import pandas as pd

from Y_factors_parser.invest_parser import run_invest_main
from Y_factors_parser.wage_parser import wage_parser_main
from Y_factors_parser.DGP_parser import DGP_parser_main
from Y_factors_parser.DGP_preliminary_data_parser import DGP_preliminary_data_parser_main
from Y_factors_parser.unemployment_parser import unemployment_parser_main
from Y_factors_parser.trade_turnover_parser import trade_turnover_parser_main
from Y_factors_parser.Export_import_parser import Export_import_parser_main
from Y_factors_parser.IPI_parser import IPI_parser_main
from Y_factors_parser.inflation_parser import inflation_parser_main
from check_flag_main import invest_flag, wage_flag, DGP_flag, DGP_preliminary_data_flag, unemployment_flag,\
    trade_turnover_flag, Export_import_flag, IPI_flag, inflation_flag

from X_factors_parser.RZD_date_parser import RZDParser_main
from X_factors_parser.electricity_consumption_parser import electricity_consumption_parser_main
from X_factors_parser.Nominal_ruble_exchange_rate_parser import Nominal_ruble_exchange_rate_parser_main
from check_flag_main import RZD_flag, electricity_consumption_flag, Nominal_ruble_exchange_rate_flag


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
            time.sleep(15)

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

    # X - факторы
    if RZD_flag:
        RZDParser_main()
        # Погрузка на сети РЖД

    if electricity_consumption_flag:
        electricity_consumption_parser_main()
        # Индекс цен на РСВ

    if Nominal_ruble_exchange_rate_flag:
        Nominal_ruble_exchange_rate_parser_main()
        # Курс Рубля к доллару США, номинальный


if __name__ == '__main__':
    main_start_parsers()

