import pandas_datareader.data as web
from datetime import date, timedelta
from .webscraper import scrape_ticker
from .holding import Holding
from .portfolio import Portfolio

def get_holdings(portfolio):
    data = {}
    prices = _get_prices(portfolio)
    total = _get_total(portfolio, prices)
    for ticker, shares in portfolio.get_holdings().items():
        price = prices[ticker]
        ratio = (shares * price) / total
        holdings = scrape_ticker(ticker)
        for holding in holdings:
            underlying = holding.get_ticker()
            weight = float(holding.get_weight()) * ratio
            if not underlying in data:
                holding.set_weight(weight)
                data[underlying] = holding
                continue
            previous_weight = data[underlying].get_weight()
            data[underlying].set_weight(previous_weight + weight)
    return list(data.values())

def _get_total(portfolio, prices):
    total = 0
    for ticker, shares in portfolio.get_holdings().items():
        price = prices[ticker]
        total += shares * price
    return total

def _get_prices(portfolio):
    tickers = portfolio.get_tickers()
    weekday = _last_weekday()
    data = web.get_data_yahoo(tickers, weekday, weekday)
    return data.iloc[0]['Close']

def _last_weekday():
    weekday = date.today() - timedelta(days=1)
    while weekday.weekday():
        weekday -= timedelta(days=1)
    return weekday