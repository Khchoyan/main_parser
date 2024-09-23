import datetime
import pandas as pd

year_now = datetime.datetime.now().year
month_now = datetime.datetime.now().month
day_now = datetime.datetime.now().day

df_Y = pd.read_excel('rez_file_Y_v2.xlsx')

# Получаем месяц последнего обновления каждого фактора
last_month_in_table_invest = pd.to_datetime(df_Y.dropna(subset=['Инвестиции в основной '
                                                                'капитал накопленным '
                                                                'итогом, млрд руб']).iloc[
                                                -1]['Целевой показатель']).month

last_month_in_table_wage = pd.to_datetime(df_Y.dropna(subset=['Реальные располагаемые '
                                                              'денежные доходы']).iloc[-1][
                                              'Целевой показатель']).month

last_month_in_table_DGP = pd.to_datetime(df_Y.dropna(subset=['Реальный ВВП (Темп роста накопленным итогом)']).iloc[
                                             -1]['Целевой показатель']).month

last_month_in_table_unemployment = pd.to_datetime(df_Y.dropna(subset=['Уровень безработицы, % к рабочей силе']).iloc[
                                                      -1]['Целевой показатель']).month

last_month_in_table_trade_turnover = pd.to_datetime(df_Y.dropna(subset=['Розничный товарооборот']).iloc[
                                                        -1]['Целевой показатель']).month

last_month_in_table_Export_import = pd.to_datetime(df_Y.dropna(subset=['Импорт, млн долл. США']).iloc[
                                                       -1]['Целевой показатель']).month

last_month_in_table_IPI = pd.to_datetime(
    df_Y.dropna(subset=['ИПП в % к соответствующему периоду предыдущего года']).iloc[
        -1]['Целевой показатель']).month

last_month_in_table_inflation = pd.to_datetime(df_Y.dropna(subset=['Инфляция, Период с начала года к соответствующему '
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
update_date_dict_Y = {'invest': 10, 'wage': 10,
                      'DGP': 10, 'unemployment': 10,
                      'trade_turnover': 10, 'Export_import': 10,
                      'IPI': 10, 'inflation': 10}

# Проверяем нужно ли обновлять каждый фактор, если да, flag --> True
if (last_month_in_table_invest + 4 == month_now and update_date_dict_Y['invest'] <= day_now) or \
        (last_month_in_table_invest + 4 < month_now):
    invest_flag = True
if (last_month_in_table_wage + 4 == month_now and update_date_dict_Y['wage'] <= day_now) or \
        (last_month_in_table_wage + 3 < month_now):
    wage_flag = True
if (last_month_in_table_DGP + 4 == month_now and update_date_dict_Y['DGP'] <= day_now) or \
        (last_month_in_table_DGP + 4 < month_now):
    DGP_flag = True
if last_month_in_table_DGP + 4 <= month_now:
    DGP_preliminary_data_flag = True
if (last_month_in_table_unemployment + 3 == month_now and update_date_dict_Y['unemployment'] <= day_now) or \
        (last_month_in_table_unemployment + 3 < month_now):
    unemployment_flag = True
if (last_month_in_table_trade_turnover + 3 == month_now and update_date_dict_Y['trade_turnover'] <= day_now) or \
        (last_month_in_table_trade_turnover + 3 < month_now):
    trade_turnover_flag = True
if (last_month_in_table_Export_import + 3 == month_now and update_date_dict_Y['Export_import'] <= day_now) or \
        (last_month_in_table_Export_import + 3 < month_now):
    Export_import_flag = True
if (last_month_in_table_IPI + 3 == month_now and update_date_dict_Y['IPI'] <= day_now) or \
        (last_month_in_table_IPI + 3 < month_now):
    IPI_flag = True
if (last_month_in_table_inflation + 2 == month_now and update_date_dict_Y['inflation'] <= day_now) or \
        (last_month_in_table_inflation + 2 < month_now):
    inflation_flag = True


# Посмотреть сколько времени нужно wage и import на обновление


df_X = pd.read_excel('rez_file_X_v6.xlsx')
last_date_in_table_RZD = pd.to_datetime(df_X.dropna(subset=['Погрузка на сети РЖД']).iloc[-1]['date']).month

last_date_in_table_Nominal_ruble_exchange_rate_flag = pd.to_datetime(df_X.dropna(subset=['Курс Рубля к доллару США, номинальный']).iloc[-1]['date']).month

last_date_in_table_oil_price_flag = pd.to_datetime(df_X.dropna(subset=['Стоимость нефти']).iloc[-1]['date']).month

last_date_in_table_CBR_polls_parser_flag = pd.to_datetime(df_X.dropna(subset=['Мониторинг предприятий ЦБ']).iloc[-1]['date']).month

last_date_in_table_CBR_news_index_parser_flag = pd.to_datetime(df_X.dropna(subset=['Новостной индекс ЦБ']).iloc[-1]['date']).month

last_date_in_table_CBR_invest_parser_flag = pd.to_datetime(df_X.dropna(subset=['Средства клиентов, всего, млн руб.']).iloc[-1]['date']).month

last_date_in_table_CBR_inflation_expectations_parser_flag = pd.to_datetime(df_X.dropna(subset=['Инфляционные ожидания: выросли очень сильно']).iloc[-1]['date']).month

last_date_in_table_retail_turnover_file_X_parser_flag = pd.to_datetime(df_X.dropna(subset=['13.1. Недостаточный платежеспособный спрос']).iloc[-1]['date']).month


RZD_flag = False
electricity_consumption_flag = True
Nominal_ruble_exchange_rate_flag = False
oil_price_flag = False
CBR_polls_parser_flag = False
CBR_news_index_parser_flag = False
CBR_invest_parser_flag = False
zcyc_moex_parser_flag = True
CBR_inflation_expectations_parser_flag = False
retail_turnover_file_X_parser_flag = False


update_date_dict_X = {'RZD': 10}

if (last_date_in_table_RZD + 2 == month_now and update_date_dict_X['RZD'] <= day_now) or \
        (last_date_in_table_RZD + 1 < month_now):
    RZD_flag = True

if last_date_in_table_Nominal_ruble_exchange_rate_flag + 1 < month_now:
    Nominal_ruble_exchange_rate_flag = True

if last_date_in_table_oil_price_flag + 1 < month_now:
    oil_price_flag = True

if CBR_polls_parser_flag + 1 < month_now:
    CBR_polls_parser_flag = True

if last_date_in_table_CBR_news_index_parser_flag + 2 < month_now:
    CBR_news_index_parser_flag = True

if last_date_in_table_CBR_invest_parser_flag + 2 < month_now:
    CBR_invest_parser_flag = True

if last_date_in_table_CBR_inflation_expectations_parser_flag + 2 < month_now:
    CBR_inflation_expectations_parser_flag = True

if last_date_in_table_retail_turnover_file_X_parser_flag + 3 < month_now:
    retail_turnover_file_X_parser_flag = True
