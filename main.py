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
from X_factors_parser.Oil_price_parser import oil_price_parser_main
from X_factors_parser.CBR_polls_parser import CBR_polls_parser_main
from X_factors_parser.CBR_news_index_parser import CBR_news_index_parser_main
from X_factors_parser.CBR_invest_parser import CBR_invest_parser_main
from X_factors_parser.zcyc_moex_parser import zcyc_moex_parser_main
from X_factors_parser.CBR_inflation_expectations_parser import CBR_inflation_expectations_parser_main
from X_factors_parser.retail_turnover_file_X_parser import retail_turnover_file_X_parser_main

from check_flag_main import RZD_flag, electricity_consumption_flag, Nominal_ruble_exchange_rate_flag, oil_price_flag, \
    CBR_polls_parser_flag, CBR_news_index_parser_flag, CBR_invest_parser_flag, zcyc_moex_parser_flag, \
    CBR_inflation_expectations_parser_flag, retail_turnover_file_X_parser_flag


def main_start_parsers():
    # link_dict = {}
    # year = datetime.datetime.now().year
    # if trade_turnover_flag + unemployment_flag + DGP_flag + wage_flag + invest_flag + DGP_preliminary_data_flag:
    #     header = {'user-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:86.0) Gecko/20100101 Firefox/86.0'}
    #     for j in [year - 1, year]:
    #         url = f'https://rosstat.gov.ru/storage/mediabank/Doklad_{j}.htm'
    #         response = requests.get(url, headers=header)
    #         soup = bs(response.content, "html.parser")
    #         links_1 = pd.DataFrame()
    #         for i in range(0, len(soup.find('table').find_all('tr')[1].find_all('tr')), 2):
    #             month_name = soup.find('table').find_all('tr')[1].find_all('tr')[i].find_all('td')[0].text
    #             month_name = month_name.replace('\n', '')
    #             if month_name.split()[-1].lower() == 'год':
    #                 month_name = 'Январь-декабрь'
    #             dok_link = soup.find('table').find_all('tr')[1].find_all('tr')[i].find_all('td')[1].find_all('a')[0].get(
    #                 'href')
    #             if dok_link[:4] != 'http':
    #                 dok_link = 'https://rosstat.gov.ru' + dok_link
    #             pril_link = soup.find('table').find_all('tr')[1].find_all('tr')[i + 1].find_all('td')[0].find_all('a')[
    #                 0].get(
    #                 'href')
    #             if pril_link[:4] != 'http':
    #                 pril_link = 'https://rosstat.gov.ru' + pril_link
    #             links_1 = links_1._append([[month_name, dok_link, pril_link]])
    #         link_dict[j] = links_1
    #         time.sleep(15)
    #
    # if invest_flag:
    #     time.sleep(5)
    #     run_invest_main(link_dict)
    #     # invest_parser - Инвестиции в основной капитал накопленным итогом, млрд руб,
    #     # Инвестиции, % накопленным итогом год к году
    #
    # if wage_flag:
    #     time.sleep(5)
    #     wage_parser_main(link_dict)
    #     # Wage_parser - Реальные располагаемые денежные доходы,
    #     # Среднемесячная номинальная начисленная заработная плата, рублей,
    #     # Реальная заработная плата
    #
    # if DGP_flag:
    #     time.sleep(15)
    #     DGP_parser_main(link_dict)
    #     # DGP_parser - Реальный ВВП (Темп роста, квартал к кварталу прошлого года)
    #     # Реальный ВВП (Темп роста накопленным итогом)
    #
    # if DGP_preliminary_data_flag:  # убрать принт данных
    #     time.sleep(5)
    #     DGP_preliminary_data_parser_main(link_dict)
    #     # DGP_parser - Реальный ВВП (Темп роста, квартал к кварталу прошлого года) предворительные данные
    #
    # if unemployment_flag:
    #     time.sleep(5)
    #     unemployment_parser_main(link_dict)
    #     # unemployment_parser - Уровень безработицы, % к рабочей силе
    #
    # if trade_turnover_flag:
    #     time.sleep(15)
    #     trade_turnover_parser_main(link_dict)
    #     # trade_turnover_parser - Розничный товарооборот   - переделать
    #     # Розничный товарооборот, темп роста, % г/г
    #
    # if Export_import_flag:
    #     time.sleep(5)
    #     Export_import_parser_main()
    #     # Export_import_parser - Импорт, млн долл. США
    #     # Импорт,  % накопленным итогом год к году
    #     # Экспорт, млн долл. США
    #     # Экспорт,  % накопленным итогом год к году
    #
    # if inflation_flag:
    #     inflation_parser_main()
    #     # inflation_parser - Инфляция, Период с начала года к соответствующему периоду предыдущего года (в среднем за
    #     # год, в терминологии Минэк)
    #     # К декабрю предыдущего года (в терминологии минэк на конец года в % к декабрю )
    #     # К предыдущему месяцу
    #     # К соответствующему периоду предыдущего года
    #
    # if IPI_flag:
    #     time.sleep(15)  # Здесь нас банит ростат с кучей запросов
    #     IPI_parser_main()
    #     # IPI_parser - ИПП в % к соответствующему периоду предыдущего года
    #     # ИПП в % к соответствующему месяцу предыдущего года
    #     # ИПП в % к предыдущему месяцу
    #
    # # X - факторы
    # if RZD_flag:
    #     RZDParser_main()  # запускаем каждый раз так как данные обновляются езедневно
    #     # Погрузка на сети РЖД
    #
    # if electricity_consumption_flag:
    #     electricity_consumption_parser_main()
    #     # Цены РСВ
    #     # Объемы РСВ
    #     # Цены РСВ ЦЗ 1
    #     # Объемы РСВ ЦЗ 1
    #     # Цены РСВ ЦЗ 2
    #     # Объемы РСВ ЦЗ 2
    #
    # if Nominal_ruble_exchange_rate_flag:
    #     Nominal_ruble_exchange_rate_parser_main()
    #     # Курс Рубля к доллару США, номинальный
    #
    # if oil_price_flag:
    #     oil_price_parser_main()
    #     # Стоимость нефти
    #
    # if CBR_polls_parser_flag:
    #     CBR_polls_parser_main()
    #     # Мониторинг предприятий ЦБ
    #     # Бизнес климат ЦБ
    #     # Как изменился объем производства, подрядных работ, товарооборота, услуг? баланс ответов
    #     # ЦБ опрос Как изменился спрос на продукцию, товары, услуги баланс ответов
    #     # Индикатор бизнес-климата Банка России
    #
    # if CBR_news_index_parser_flag:
    #     CBR_news_index_parser_main()
    #     # Новостной индекс ЦБ
    #
    # if CBR_invest_parser_flag:
    #     CBR_invest_parser_main()
    #     # Средства клиентов, всего, млн руб.
    #     #     средства на счетах организаций, млн руб.
    #     #     депозиты юридических лиц*, млн руб.
    #     #     вклады (депозиты) и другие привлеченные средства физических лиц (с учето
    #     #     средства индивидуальных предпринимателей, млн руб.
    #
    # if zcyc_moex_parser_flag:
    #     zcyc_moex_parser_main()
    #     # Кривая доходности ОФЗ period_0.25
    #     # period_0.5
    #     # period_0.75
    #     # period_1.0
    #     # period_2.0
    #     # period_3.0
    #     # period_5.0
    #     # period_7.0
    #     # period_10.0
    #     # period_15.0
    #     # period_20.0
    #     # period_30.0

    if CBR_inflation_expectations_parser_flag:
        CBR_inflation_expectations_parser_main()
        # Инфляционные ожидания: выросли очень сильно
        # выросли умеренно
        # выросли незначительно
        # не изменились
        # снизились
        # затрудняюсь ответить
        # вырастут очень сильно
        # вырастут умеренно
        # вырастут незначительно
        # не изменятся
        # снизятся
        # затрудняюсь ответить.1

    if retail_turnover_file_X_parser_flag:
        retail_turnover_file_X_parser_main()
        # "Индекс предринимательской уверенности 2006-2023гг.\n(в  % )"
        # Экономическая ситуация 2006-2023гг.\n(Баланс оценок изменения значения показателя) фактические значения
        # Экономическая ситуация 2006-2023гг.\n(Баланс оценок изменения значения показателя) перспективы изменения
        # Складские запасы 2006-2021гг.\n(Баланс оценок уровня складских запасов )
        # Средняя численность работников 2006-2023гг. (Баланс оценок изменения значения показателя) фактические значения
        # Средняя численность работников 2006-2023гг. (Баланс оценок изменения значения показателя) перспективы изменения
        # Оборот розничной торговли 2006-2023гг. (Баланс оценок изменения значения показателя) фактические значения
        # Оборот розничной торговли 2006-2023гг. (Баланс оценок изменения значения показателя) перспективы изменения
        # Ассортимент товаров 2006-2023гг.\n(Баланс оценок уровня складских запасов ) фактические значения
        # Ассортимент товаров 2006-2023гг.\n(Баланс оценок уровня складских запасов ) перспективы изменения
        # Цены реализации 2006-2023гг. (Баланс оценок изменения значения показателя) фактические значения
        # Цены реализации 2006-2023гг. (Баланс оценок изменения значения показателя) перспективы изменения
        # Средний сложившийся уровень торговой наценки 2006-2023гг. (в % к стоимости проданных товаров)
        # Прибыль 2006-2023гг. (Баланс оценок изменения значения показателя) фактические значения
        # Прибыль 2006-2023гг. (Баланс оценок изменения значения показателя) перспективы изменения
        # Складские площади 2006-2023гг.\n(Баланс оценок уровня складских запасов ) фактические значения
        # Складские площади 2006-2023гг.\n(Баланс оценок уровня складских запасов ) перспективы изменения
        # Обеспеченность собственными финансовыми ресурсами 2006-2023гг. (Баланс оценок изменения значения показателя) фактические значения
        # Обеспеченность собственными финансовыми ресурсами 2006-2023гг. (Баланс оценок изменения значения показателя) перспективы изменения
        # Инвестиции на расширение деятельности, ремонт и модернизацию 2006-2023гг. (Баланс оценок изменения значения  показателя) фактические значения
        # Инвестиции на расширение деятельности, ремонт и модернизацию 2006-2023гг. (Баланс оценок изменения значения  показателя) перспективы изменения
        # 13.1. Недостаточный платежеспособный спрос
        # 13.2. Недостаток финансовых средств
        # 13.3. Высокий уровень налогов
        # 13.4. Высокая арендная плата
        # 13.5. Высокая конкуренция со стороны других организаций розничной торговли
        # 13.6. Высокие транспортные расходы


if __name__ == '__main__':
    main_start_parsers()

