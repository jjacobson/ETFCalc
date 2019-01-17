import requests_cache
from .webscraper import scrape_ticker, get_stock_sectors, get_stock_news, get_underlying_data
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
                holding.set_weight(round_weight(weight))
                data[underlying] = holding
            else:
                previous_weight = data[underlying].get_weight()
                data[underlying].set_weight(
                    round_weight(previous_weight + weight))

    handle_stock_data(data)
    return list(data.values())


def handle_stock_data(data):
    stock_data = get_underlying_data(list(data.keys()))
    sectors = get_stock_sectors(stock_data)
    news = get_stock_news(stock_data)
    for ticker, holding in data.items():
        sector = sectors.get(ticker)
        if sector is not None:
            holding.set_sector(sector)
        stock_news = news.get(ticker)
        if stock_news is not None:
            holding.set_news(stock_news)


def round_weight(weight):
    return round(weight, 3)


def _get_total(portfolio):
    total = 0
    for ticker, shares in portfolio.get_holdings().items():
        price = portfolio.get_price(ticker)
        total += shares * price
    return total