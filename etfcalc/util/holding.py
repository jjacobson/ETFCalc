class Holding(object):

    def __init__(self, name, ticker, weight=100, sector=None, news=None):
        self.name = name
        self.ticker = ticker
        self.weight = weight
        self.sector = sector
        self.news = news

    def get_name(self):
        return self.name

    def get_ticker(self):
        return self.ticker

    def get_weight(self):
        return self.weight

    def set_weight(self, weight):
        self.weight = weight

    def set_sector(self, sector):
        self.sector = sector

    def get_sector(self):
        return self.sector

    def set_news(self, news):
        self.news = news

    def get_news(self):
        return self.news

    def __str__(self):
        return self.name + ' (' + self.ticker + ') ' + str(self.weight)
