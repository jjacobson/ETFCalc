import requests_cache
from .webscraper import scrape_ticker, get_stocks_sectors
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
            else:
                previous_weight = data[underlying].get_weight()
                data[underlying].set_weight(
                    _round_weight(previous_weight + weight))
    print('sector list: ', get_stocks_sectors(list(data.keys())))
    return list(data.values())


def _get_total(portfolio):
    total = 0
    for ticker, shares in portfolio.get_holdings().items():
        price = portfolio.get_price(ticker)
        total += shares * price
    return total


def _round_weight(weight):
    return round(weight, 3)



