class Portfolio(object):

    def __init__(self):
        self.holdings = {}

    def set_amount(self, ticker, amount):
        self.holdings[ticker] = amount

    def get_amount(self, ticker):
        return self.holdings[ticker]

    def remove_holding(self, ticker):
        del self.holdings[holding]

    def clear_holdings(self):
        self.holdings.clear()
    


