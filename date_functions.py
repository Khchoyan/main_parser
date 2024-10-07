import re

import pandas as pd


def str_digit2month(month):
    """
    Функция переводит название месяца в его номер.
    """
    month = month.strip().lower()
    if month == '01':
        return 'Январь'
    elif month == '02':
        return 'Январь-февраль'
    elif month == '03':
        return 'Январь-март'
    elif month == '04':
        return 'Январь-апрель'
    elif month == '05':
        return 'Январь-май'
    elif month == '06':
        return 'Январь-июнь'
    elif month == '07':
        return 'Январь-июль'
    elif month == '08':
        return 'Январь-август'
    elif month == '09':
        return 'Январь-сентябрь'
    elif month == '10':
        return 'Январь-октябрь'
    elif month == '11':
        return 'Январь-ноябрь'
    elif month == '12':
        return 'Январь-декабрь'
    else:
        return 'unknown'


def str_digit2month_with_date(month, year):
    month = month.strip().lower()
    flag = True if ((year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)) else False
    if month == '01' or month == '1':
        month = '31 january'
    elif (month == '02' and flag) or (month == '2' and flag):
        month = '29 february'
    elif month == '02' or month == '2':
        month = '28 february'
    elif month == '03' or month == '3':
        month = '31 march'
    elif month == '04' or month == '4':
        month = '30 April'
    elif month == '05' or month == '5':
        month = '31 may'
    elif month == '06' or month == '6':
        month = '30 june'
    elif month == '07' or month == '7':
        month = '31 july'
    elif month == '08' or month == '8':
        month = '31 august'
    elif month == '09' or month == '9':
        month = '30 september'
    elif month == '10':
        month = '31 october'
    elif month == '11':
        month = '30 november'
    elif month == '12':
        month = '31 december'
    return pd.to_datetime(month + str(year))


def str_month2digit_month(month):
    """
    Функция переводит название месяца в его номер.
    """
    month = month.strip().lower()
    if month == 'январь':
        return '01'
    elif month == 'январь-февраль' or month == 'февраль':
        return '02'
    elif month == 'январь-март' or month == 'март':
        return '03'
    elif month == 'январь-апрель' or month == 'апрель':
        return '04'
    elif month == 'январь-май' or month == 'май':
        return '05'
    elif month == 'январь-июнь' or month == 'июнь':
        return '06'
    elif month == 'январь-июль' or month == 'июль':
        return '07'
    elif month == 'январь-август' or month == 'август':
        return '08'
    elif month == 'январь-сентябрь' or month == 'сентябрь':
        return '09'
    elif month == 'январь-октябрь' or month == 'октябрь':
        return '10'
    elif month == 'январь-ноябрь' or month == 'ноябрь':
        return '11'
    elif month == 'январь-декабрь' or month == 'декабрь':
        return '12'
    else:
        return 'unknown'


def reformate_date(date, year):
    date = re.sub('[0-9]', '', date).strip().lower()
    date = date.replace(')', '')
    flag = True if ((year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)) else False
    if date == 'январь':
        date = '31 january'
    elif (date == 'февраль' or date == 'январь-февраль') and flag:
        date = '29 february'
    elif date == 'февраль' or date == 'январь-февраль':
        date = '28 february'
    elif date == 'март' or date == 'январь-март' or date == 'i квартал':
        date = '31 march'
    elif date == 'апрель' or date == 'январь-апрель':
        date = '30 April'
    elif date == 'май' or date == 'январь-май':
        date = '31 may'
    elif date == 'июнь' or date == 'январь-июнь' or date == 'i полугодие' or date == 'ii квартал':
        date = '30 june'
    elif date == 'июль' or date == 'январь-июль':
        date = '31 july'
    elif date == 'август' or date == 'январь-август':
        date = '31 august'
    elif date == 'сентябрь' or date == 'январь-сентябрь' or date == 'iii квартал':
        date = '30 september'
    elif date == 'октябрь' or date == 'январь-октябрь':
        date = '31 october'
    elif date == 'ноябрь' or date == 'январь-ноябрь':
        date = '30 november'
    elif date == 'декабрь' or date == 'январь-декабрь' or date == 'год' or date == 'год)' or date == 'iv квартал':
        date = '31 december'
    return pd.to_datetime(date + str(year))


def reformate_quarterly_date(date):
    if date == 'Январь-март':
        date = 'I квартал'
    elif date == 'Январь-июнь':
        date = 'I полугодие'
    elif date == 'Январь-декабрь':
        date = 'Год'
    return date
