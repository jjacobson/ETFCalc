from flask import Flask, render_template, request
from util import holdings_calculator
from util.portfolio import Portfolio

app = Flask(__name__)

@app.route('/')
def hello_world():

    portfolio = Portfolio()
    portfolio.set_amount('QQQ', 6)
    portfolio.set_amount('AAPL', 4)

    data = holdings_calculator.get_holdings(portfolio)
    for ticker, value in data.items():
        print(value)
    return str('data[97]')

if __name__ == '__main__':
    app.run()
