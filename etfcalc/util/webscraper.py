from .holding import Holding
from pyquery import PyQuery
import requests, json

class WebScraper(object):

    def scrape_ticker(self, ticker):
        response = self.__make_request(ticker, True)
        holdings = []
        if self.__valid_request(response):
            self.__scrape_etf(ticker, response, holdings)
        else:
            response = self.__make_request(ticker, False)
            self.__scrape_stock(ticker, response, holdings)
        return holdings
        
    def __make_request(self, ticker, etf):
        ticker_type = "etf" if etf else "stock"
        url = 'http://etfdb.com/' + ticker_type + '/' + ticker + '/'
        return requests.get(url, allow_redirects=False)

    def __valid_request(self, response):
        return response.status_code == requests.codes.ok

    def __scrape_stock(self, ticker, response, holdings):
        if not self.__valid_request(response):
            return None
        page_content = response.content
        title = self.__get_title(page_content)[10:]
        title = title.split('(')[0]
        holding = Holding(title, ticker)
        holdings.append(holding)

    def __scrape_etf(self, ticker, response, holdings):
        page_content = response.content
        title = self.__get_title(page_content)
        
        url = self.__get_holdings_url(page_content)
        holdings_json = requests.get(url).json()

        for entry in holdings_json['rows']:
            holding = self.__get_etf_holding(entry)
            holdings.append(holding) 

    def __get_title(self, content):
        pq = PyQuery(content)
        return pq("meta[property='og:title']").attr('content')

    def __get_holdings_url(self, content):
        pq = PyQuery(content)
        url = 'http://etfdb.com/'
        sort = '&sort=weight&order=desc&limit=1000'
        url += pq("table[data-hash='etf-holdings']").attr('data-url') + sort
        return url
    
    def __get_etf_holding(self, entry):
        name = ticker = ''
        data = entry['holding']
        pq = PyQuery(data)
        if pq('a').length:
            name = pq('a').text().split('(')[0]
            ticker = pq('a').attr('href').split('/')[2]
        else:
            name = data
        weight = entry['weight'][:-1]
        return Holding(name, ticker, weight)

