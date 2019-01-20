import requests_cache
from operator import attrgetter
from .webscraper import scrape_ticker, get_company_data, get_stock_news
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

    holdings = list(data.values())
    holdings.sort(key=attrgetter('weight'), reverse=True)
    handle_stock_data(holdings)
    return holdings


def handle_stock_data(holdings):
    tickers = [holding.ticker for holding in holdings]
    company_data = get_company_data(tickers)
    news = get_stock_news(tickers[:50])
    for holding in holdings:
        ticker = holding.get_ticker()
        if ticker in company_data:
            company = company_data[holding.get_ticker()]
        if company is not None:
            # use iex names if available (they look better)
            name = company['name']
            if name is not None:
                holding.set_name(name)
            holding.set_sector(company['sector'])
            holding.set_link(company['link'])
        stock_news = news.get(holding.get_ticker())
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