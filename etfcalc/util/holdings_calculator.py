import pandas_datareader.data as web
from datetime import date
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
    return data

def _get_total(portfolio, prices):
    total = 0
    for ticker, shares in portfolio.get_holdings().items():
        price = prices[ticker]
        total += shares * price
    return total

def _get_prices(portfolio):
    tickers = portfolio.get_tickers()
    today = "2018-09-20"
    data = web.get_data_yahoo(tickers, today, today)
    return data.iloc[0]['Close']