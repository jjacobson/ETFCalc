import requests
import json
import requests_cache
import time
import logging
from datetime import date, timedelta, datetime
from pyquery import PyQuery
from pandas_datareader.nasdaq_trader import get_nasdaq_symbols
from .holding import Holding

symbols = get_nasdaq_symbols()
expire_after = timedelta(days=5)
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

# Get latest price for a given ticker
def get_price(ticker):
    with requests_cache.disabled():
        quote = _get_iex_data([ticker], ['price'])
    return _round_price(quote[ticker]['price'])


def get_company_data(tickers):
    company_data = {}
    data = _get_iex_data(tickers, ['company'])
    for ticker, stock in data.items():
        quote = stock['company']
        if quote is None:
            continue
        company_data[ticker] = {'name' : quote['companyName'], 'sector' : quote['sector'], 'link' : quote['website']}
    return company_data


def get_stock_news(tickers):
    stock_news = {}
    with requests_cache.disabled():
        data = _get_iex_data(tickers, ['news'], ['last=5'])
    for ticker, stock in data.items():
        news = stock['news']
        if news is None:
            continue
        news_items = []
        for news_item in news:
            news_items.append({'title' : news_item['headline'], 'description' : news_item['summary'], 
                'image_url' : _get_ticker_image(ticker), 'datetime' : _convert_time(news_item['datetime']),
                'url' : news_item['url'], 'source' : news_item['source']})
        stock_news[ticker] = news_items
    return stock_news


def get_holding_data(ticker):
    holding_data = {}
    with requests_cache.disabled():
        data = _get_iex_data([ticker], ['quote', 'chart'], ['displayPercent=true', 'range=1y'])
    return data


def _round_price(price):
    return format(price, '.2f')


def _is_etf(data):
    return data.loc['ETF']


def _convert_time(timestamp):
    timestamp = timestamp.replace('T', ' ')
    return datetime.fromisoformat(timestamp)


def _get_etf_data(ticker, data, holdings):
    response = _get_etf_page(ticker)
    if not _valid_request(response):
        logging.warning('Failed to get holdings for ticker',
                        ticker, response.status_code)
        return

    page_content = response.content
    pq = PyQuery(page_content)
    table = pq.find('#etfs-that-own')

    # use secondary data source if none available
    if not table:
        _get_etf_data_backup(ticker, data, holdings)
        return

    for row in table('tbody tr').items():
        columns = list(row('td').items())
        ticker = columns[0].children("a").text()
        holding_data = get_data(ticker)
        if holding_data is None:
            # fall back to getting name from scraped data
            name = columns[1].children("a").text()
        else:
            # make use of official nasdaq data if available
            name = holding_data.loc['Security Name']

        weight = columns[2].text()
        weight = weight[:-1]
        holdings.append(Holding(name, ticker, weight))


def _get_etf_data_backup(ticker, data, holdings):
    response = _get_etf_page_backup(ticker)
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
        holdings_json = _make_request(url + str(i + 15), throttle=0.7).json()


def _get_stock_data(ticker, data, holdings):
    title = data.loc['Security Name']
    holding = Holding(title, ticker)
    holdings.append(holding)


def _get_etf_page(ticker):
    url = 'https://etfdailynews.com/etf/{0}/'.format(ticker)
    return _make_request(url, redirects=False)


def _get_etf_page_backup(ticker):
    url = 'https://etfdb.com/etf/{0}/'.format(ticker)
    return _make_request(url, redirects=False)


def _get_ticker_image(ticker):
    return 'https://storage.googleapis.com/iex/api/logos/{0}.png'.format(ticker)


def _get_iex_data(tickers, options, settings=None):
    data = {}
    options = ",".join(options)
    if settings:
        options = options + ("&" + "&".join(settings))
    for i in range(0, len(tickers), 100):
        subset = ",".join(tickers[i:i+100])
        url = 'https://api.iextrading.com/1.0/stock/market/batch?symbols={0}&types={1}'.format(subset, options)
        data.update(_make_request(url, redirects=False).json())
    return data


def _make_request(url, redirects=True, throttle=0.0):
    response = None
    try:
        response = requests.get(url, hooks={'response': _throttle_hook(
            throttle)}, allow_redirects=redirects, timeout=3)
    except requests.exceptions.RequestException as e:
        raise ValueError('Request exception') from e
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
    url = 'https://etfdb.com/'
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
