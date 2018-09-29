from pandas_datareader.data import get_data_yahoo
from datetime import date, timedelta
from .webscraper import scrape_ticker
from .holding import Holding
from .portfolio import Portfolio

def get_holdings(portfolio):
    data = {}
    total = _get_total(portfolio)
    for ticker, shares in portfolio.get_holdings().items():
        price = portfolio.get_price(ticker)
        ratio = (shares * price) / total
        holdings = scrape_ticker(ticker)
        for holding in holdings:
            underlying = holding.get_ticker()
            weight = float(holding.get_weight()) * ratio
            if not underlying in data:
                holding.set_weight(_round_weight(weight))
                data[underlying] = holding
                continue
            previous_weight = data[underlying].get_weight()
            data[underlying].set_weight(_round_weight(previous_weight + weight))
    return list(data.values())

def get_price(ticker):
    weekday = _last_weekday()
    data = get_data_yahoo(ticker, weekday, weekday)
    return _round_price(data.iloc[0]['Close'])

def _get_total(portfolio):
    total = 0
    for ticker, shares in portfolio.get_holdings().items():
        price = portfolio.get_price(ticker)
        total += shares * price
    return total

def _get_prices(portfolio):
    tickers = portfolio.get_tickers()
    weekday = _last_weekday()
    data = get_data_yahoo(tickers, weekday, weekday)
    return data.iloc[0]['Close']

def _last_weekday():
    weekday = date.today() - timedelta(days=1)
    while weekday.weekday():
        weekday -= timedelta(days=1)
    return weekday

def _round_weight(weight):
    return round(weight, 3)

def _round_price(price):
    return round(price, 2)
