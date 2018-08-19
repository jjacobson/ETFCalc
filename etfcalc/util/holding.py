class Holding(object):

    def __init__(self, name, ticker, weight=1):
        self.name = name
        self.ticker = ticker
        self.weight = weight

    def get_name(self):
        return self.name

    def get_ticker(self):
        return self.ticker

    def get_weight(self):
        return self.weight

    def __str__(self):
        return self.name + ' (' + self.ticker + ') ' + str(self.weight)
