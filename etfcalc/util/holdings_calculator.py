from .webscraper import scrape_ticker
from .holding import Holding
from .portfolio import Portfolio

def get_holdings(portfolio):
    data = {}
    total = __get_total(portfolio)
    for ticker, amount in portfolio.get_holdings().items():
        ratio = amount / total
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
        
def __get_total(portfolio):
    total = 0
    for value in portfolio.get_holdings().values():
        total += value
    return total