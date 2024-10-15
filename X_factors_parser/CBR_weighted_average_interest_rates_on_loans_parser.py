import pandas as pd
from help_functions import append_date_rez_file_X, pars_cbr_date_for_file_X
from date_functions import reformate_date


pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)


def parse_docx_document(path):
    data_xlsx = pd.read_excel(path, sheet_name='ставки_руб', skiprows=3)
    data_xlsx = data_xlsx[['Unnamed: 0', 'Unnamed: 6', 'Unnamed: 8']][-13:-1].reset_index(drop=True)
    data_xlsx.columns = ['date', 'от 1 года до 3 лет', 'свыше 1 года']
    data_xlsx['date'] = data_xlsx['date'].apply(lambda x: reformate_date(x.split(' ')[0], int(x.split(' ')[1])))
    return data_xlsx


def update_rez_file_X(data, column_name, xlsx_path='rez_file_X_v6.xlsx'):
    """
        Функция осуществляет обновление файла со всеми данными rez_file_X_v6.xlsx
    """
    data_xlsx = pd.read_excel(xlsx_path)
    if list(data['date'])[-1] not in list(data_xlsx['date']):
        append_date_rez_file_X()
        data_xlsx = pd.read_excel(xlsx_path)

    for j in list(data.values):
        data_xlsx.loc[data_xlsx['date'] == j[0], column_name] = float(j[1])

    data_xlsx.to_excel(xlsx_path, index=False)


def CBR_weighted_average_interest_rates_on_loans_parser_main():
    path = pars_cbr_date_for_file_X(url='https://cbr.ru/statistics/bank_sector/int_rat/', pattern_type='id', pattern='a_87346', file_name='CBR_interest_rate.xlsx')
    # path = 'temp_data_for_X_factors/CBR_interest_rate.xlsx'
    data = parse_docx_document(path)
    if not data.empty:
        update_rez_file_X(data[['date', 'от 1 года до 3 лет']], 'Средневзвешенные процентные ставки по кредитам, предоставленным кредитными организациями нефинансовым организациям в рубляхот 1 года до 3 лет')
        update_rez_file_X(data[['date', 'свыше 1 года']], 'Средневзвешенные процентные ставки по кредитам, предоставленным кредитными организациями нефинансовым организациям в рублях свыше 1 года')
        print('CBR_interest_rate was updated')


# обновляется в -2 месяц. Если сегодня сентябрь, то должны быть данные за июль
