from flask import Flask, render_template
import pandas as pd
from pandas_datareader.nasdaq_trader import get_nasdaq_symbols
import pandas_datareader.data as web
from datetime import datetime

from .util import holdings_calculator
from .util.portfolio import Portfolio

app = Flask(__name__)

@app.route('/')
def hello_world():

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


    #data = holdings_calculator.get_holdings(portfolio)
    data = {}
    total = 0
    for ticker, value in data.items():
        total = total + value.get_weight()
        print(str(value))
    print('TOTAL IS ', total)
    
    return render_template('input/input.html')
   #return render_template('output/output.html', data=data)