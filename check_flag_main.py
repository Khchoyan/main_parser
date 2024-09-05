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
        (last_month_in_table_invest + 4 < month_now):  # + 4 так как только квартальные данные
    invest_flag = True
if (last_month_in_table_wage + 2 == month_now and update_date_dict_Y['wage'] <= day_now) or \
        (last_month_in_table_wage + 3 < month_now):
    wage_flag = True
if (last_month_in_table_DGP + 4 == month_now and update_date_dict_Y['DGP'] <= day_now) or \
        (last_month_in_table_DGP + 4 < month_now):  # + 4 так как только квартальные данные
    DGP_flag = True
if last_month_in_table_DGP + 4 <= month_now:
    DGP_preliminary_data_flag = True
if (last_month_in_table_unemployment + 2 == month_now and update_date_dict_Y['unemployment'] <= day_now) or \
        (last_month_in_table_unemployment + 2 < month_now):
    unemployment_flag = True
if (last_month_in_table_trade_turnover + 2 == month_now and update_date_dict_Y['trade_turnover'] <= day_now) or \
        (last_month_in_table_trade_turnover + 2 < month_now):
    trade_turnover_flag = True
if (last_month_in_table_Export_import + 2 == month_now and update_date_dict_Y['Export_import'] <= day_now) or \
        (last_month_in_table_Export_import + 3 < month_now):
    Export_import_flag = True
if (last_month_in_table_IPI + 2 == month_now and update_date_dict_Y['IPI'] <= day_now) or \
        (last_month_in_table_IPI + 2 < month_now):
    IPI_flag = True
if (last_month_in_table_inflation + 2 == month_now and update_date_dict_Y['inflation'] <= day_now) or \
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


df_X = pd.read_excel('rez_file_X_v6.xlsx', skiprows=1)
last_date_in_table_RZD = pd.to_datetime(df_X.dropna(subset=['Погрузка на сети РЖД']).iloc[-1]['date']).month

last_date_in_table_Nominal_ruble_exchange_rate_flag = pd.to_datetime(df_X.dropna(subset=['Курс Рубля к доллару США, номинальный']).iloc[-1]['date']).month

RZD_flag = False
electricity_consumption_flag = True
Nominal_ruble_exchange_rate_flag = False

update_date_dict_X = {'RZD': 5}

if (last_date_in_table_RZD + 2 == month_now and update_date_dict_X['RZD'] <= day_now) or \
        (last_date_in_table_RZD + 2 < month_now):
    RZD_flag = True

if last_date_in_table_Nominal_ruble_exchange_rate_flag < month_now:
    Nominal_ruble_exchange_rate_flag = True
