from .holding import Holding
from pyquery import PyQuery
import requests, json

def scrape_ticker(ticker):
    response = __make_request(ticker, True)
    holdings = []
    if __valid_request(response):
        __scrape_etf(ticker, response, holdings)
    else:
        response = __make_request(ticker, False)
        __scrape_stock(ticker, response, holdings)
    return holdings
    
def __make_request(ticker, etf):
    ticker_type = "etf" if etf else "stock"
    url = 'http://etfdb.com/' + ticker_type + '/' + ticker + '/'
    return requests.get(url, allow_redirects=False)

def __valid_request(response):
    return response.status_code == requests.codes.ok

def __scrape_stock(ticker, response, holdings):
    if not __valid_request(response):
        return None
    page_content = response.content
    title = __get_title(page_content)[10:]
    title = title.split('(')[0]
    holding = Holding(title, ticker)
    holdings.append(holding)

def __scrape_etf(ticker, response, holdings):
    page_content = response.content
    title = __get_title(page_content)
    
    url = __get_holdings_url(page_content)
    holdings_json = requests.get(url).json()

    for entry in holdings_json['rows']:
        holding = __get_etf_holding(entry)
        holdings.append(holding) 

def __get_title(content):
    pq = PyQuery(content)
    return pq("meta[property='og:title']").attr('content')

def __get_holdings_url(content):
    pq = PyQuery(content)
    url = 'http://etfdb.com/'
    sort = '&sort=weight&order=desc&limit=1000'
    url += pq("table[data-hash='etf-holdings']").attr('data-url') + sort
    return url

def __get_etf_holding(entry):
    name = ticker = ''
    data = entry['holding']
    pq = PyQuery(data)
    if pq('a').length:
        name = pq('a').text().split('(')[0]
        ticker = pq('a').attr('href').split('/')[2]
    else:
        name = data
    weight = entry['weight'][:-1]
    return Holding(name, ticker, weight)

