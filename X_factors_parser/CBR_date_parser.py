import requests
import time
from bs4 import BeautifulSoup as bs

def pars_year_by_months():
    header = {
            'user-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:86.0) Gecko/20100101 Firefox/86.0'
        }
    time.sleep(5)
    url = f'https://cbr.ru/analytics/dkp/monitoring/0824/'
    response = requests.get(url, headers=header)
    soup = bs(response.content, "html.parser")
    print(soup)
    print(soup.find_all('a'))


print(pars_year_by_months())