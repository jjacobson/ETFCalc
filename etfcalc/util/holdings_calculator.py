from .webscraper import scrape_ticker
from .holding import Holding
from .portfolio import Portfolio

def get_holdings(portfolio):
    data = {}
    total = __get_total(portfolio)
    for ticker, value in portfolio.get_holdings().items():
        ratio = value / total
        holdings = scrape_ticker(ticker)
        for holding in holdings:
            underlying = holding.get_ticker()
            weight = float(holding.get_weight())
            if not underlying in data:
                data[underlying] = 0
            data[underlying] += round((ratio * weight), 5)
    return data
        
def __get_total(portfolio):
    total = 0
    for value in portfolio.get_holdings().values():
        total += value
    return total