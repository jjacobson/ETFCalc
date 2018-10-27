import requests, json, requests_cache, time, logging
from datetime import timedelta
from pyquery import PyQuery
from pandas_datareader.nasdaq_trader import get_nasdaq_symbols
from .holding import Holding

symbols = get_nasdaq_symbols()
expire_after = timedelta(days=7)
requests_cache.install_cache('cache_data', expire_after=expire_after)

# Scrape name and holdings if any for a given ticker
def scrape_ticker(ticker):
    holdings = []
    data = get_data(ticker)

    # invalid ticker
    if data is None:
        return holdings

    if _is_etf(data):
        _get_etf_data(ticker, data, holdings)
    else:
        _get_stock_data(ticker, data, holdings)
    return holdings

# Get the nasdaq data for a given ticker
def get_data(ticker):
    data = None
    try:
        data = symbols.loc[ticker]
    except KeyError:
        logging.info('Failed to get data for ticker ', ticker)
    return data

def _is_etf(data):
    return data.loc['ETF']

def _get_etf_data(ticker, data, holdings):
    response = _get_etf_page(ticker)
    if not _valid_request(response):
        logging.warning('Failed to get holdings for ticker ', ticker)
        return

    page_content = response.content
    title = data.loc['Security Name']

    url = _get_holdings_url(page_content)
    holdings_json = _make_request(url + str(0)).json()
    rows = holdings_json['total']
    # etfdb limits us to 15 tickers per page
    for i in range(0, rows, 15):
        for entry in holdings_json['rows']:
            holding = _get_etf_holding(entry)
            holdings.append(holding)
        holdings_json = _make_request(url + str(i + 15)).json()

def _get_stock_data(ticker, data, holdings):
    title = data.loc['Security Name']
    holding = Holding(title, ticker)
    holdings.append(holding)

def _get_etf_page(ticker):
    url = 'https://etfdb.com/etf/' + ticker + '/'
    return _make_request(url, False)

def _make_request(url, redirects = True):
    response = None
    try:
        response = requests.get(url, hooks={'response': _throttle_hook(0.5)}, allow_redirects=redirects, timeout=1)
    except requests.exceptions.RequestException as e:
        raise ValueError('ETF scraping exception') from e

    return response

# returns response hook function which sleeps for
# timeout if the response is not yet cached
def _throttle_hook(timeout):
    def hook(response, *args, **kwargs):
        if not getattr(response, 'from_cache', False):
            time.sleep(timeout)
        return response
    return hook


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
        holding_data = get_data(ticker)
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