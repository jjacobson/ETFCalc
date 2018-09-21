from flask import Flask
import pandas as pd
from pandas_datareader.nasdaq_trader import get_nasdaq_symbols
import pandas_datareader.data as web
from datetime import datetime

from util import holdings_calculator
from util.portfolio import Portfolio

app = Flask(__name__)

@app.route('/')
def hello_world():
    """
    symbols = get_nasdaq_symbols()

    portfolio = Portfolio()
    portfolio.set_amount('V', 4)
    portfolio.set_amount('MSFT', 7)
    portfolio.set_amount('XLF', 17)
    portfolio.set_amount('INTC', 5)
    portfolio.set_amount('XAR', 5)
    portfolio.set_amount('XLY', 5)
    portfolio.set_amount('XPO', 6)
    portfolio.set_amount('WM', 7)
    portfolio.set_amount('DIS', 5)
    holdings_calculator._get_prices(portfolio)

 

    symbols = ['SPY', 'QQQ', 'MSFT', 'V', 'PYPL', 'IBM', 'AAPL', 'MU', 'XLF', 'XAR', 'XPO', 'O', 'COWB', 'VXX', 'TTWO']
    data = []
    f = web.get_data_yahoo(symbols, start="2018-09-19", end="2018-09-19")
    print(f['Close']['QQQ']["2018-09-19"])
    
    data = "none"
    try:
        data = symbols.ix['SSW']
    except KeyError:
        print("oops")
    print(data)
    """


    portfolio = Portfolio()
    portfolio.set_amount('V', 4)
    portfolio.set_amount('MSFT', 7)
    portfolio.set_amount('XLF', 17)
    portfolio.set_amount('INTC', 5)
    portfolio.set_amount('XAR', 5)

    data = holdings_calculator.get_holdings(portfolio)
    for ticker, value in data.items():
        print(str(value))



    
    return str('data[97]')

if __name__ == '__main__':
    app.run()
