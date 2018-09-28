import requests, json, requests_cache
from pyquery import PyQuery
from pandas_datareader.nasdaq_trader import get_nasdaq_symbols
from .holding import Holding

symbols = get_nasdaq_symbols()
requests_cache.install_cache('cache_data')

# Scrape name and holdings if any for a given ticker
def scrape_ticker(ticker):
    holdings = []
    data = _get_data(ticker)

    # invalid ticker
    if data is None:
        return holdings
    
    if _is_etf(data):
        _get_etf_data(ticker, data, holdings)
    else:
        _get_stock_data(ticker, data, holdings)
    return holdings

# Get the nasdaq data for a given ticker
def _get_data(ticker):
    data = None
    try:
        data = symbols.loc[ticker]
    except KeyError:
        print('Failed to get data for ticker ', ticker)
    return data
 
def _is_etf(data):
    return data.loc['ETF']

def _get_etf_data(ticker, data, holdings):
    response = _make_request(ticker)
    if not _valid_request(response):
        print('Failed to get holdings for ticker ', ticker)
        return

    page_content = response.content
    title = data.loc['Security Name']
    
    url = _get_holdings_url(page_content)
    holdings_json = requests.get(url + str(0)).json()
    rows = holdings_json['total']
    # etfdb limits us to 15 tickers per page
    for i in range(0, rows, 15):
        for entry in holdings_json['rows']:
            holding = _get_etf_holding(entry)
            holdings.append(holding)
        holdings_json = requests.get(url + str(i + 15)).json()

def _get_stock_data(ticker, data, holdings):
    title = data.loc['Security Name']
    holding = Holding(title, ticker)
    holdings.append(holding)

def _make_request(ticker):
    url = 'http://etfdb.com/etf/' + ticker + '/'
    return requests.get(url, allow_redirects=False)

def _valid_request(response):
    return response.status_code == requests.codes.ok

def _get_holdings_url(content):
    pq = PyQuery(content)
    url = 'http://etfdb.com/'
    sort = '&sort=weight&order=desc&limit=15&offset='
    url += pq("table[data-hash='etf-holdings']").attr('data-url') + sort
    return url

def _get_etf_holding(entry):
    name = ticker = ''
    data = entry['holding']
    pq = PyQuery(data)

    # handle normal cases of actual stocks
    if pq('a').length:
        ticker = pq('a').attr('href').split('/')[2].split(':')[0]
        holding_data = _get_data(ticker)
        if holding_data is None:
            # fall back to getting name from scraped data
            name = pq('a').text().split('(')[0]
        else:
            # make use of official nasdaq data if available
            name = holding_data.loc['Security Name']
    # handle special underlyings e.g. VIX futures
    elif pq('span').eq(2).length:
        name = data
        ticker = pq('span').eq(2).text()
    # handle further special cases e.g. Cash components, Hogs, Cattle
    else:
        name = data
        ticker = data
    weight = entry['weight'][:-1]
    return Holding(name, ticker, weight)