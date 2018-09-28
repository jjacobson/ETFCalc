from flask import Flask, render_template, request
from operator import attrgetter
from .util import holdings_calculator
from .util.portfolio import Portfolio

app = Flask(__name__)

@app.route('/')
def main():
    return render_template('input/input.html')

@app.route('/output', methods=['POST'])
def output():
    portfolio = Portfolio()

    ticker_list = request.form.getlist('tickers')
    share_list = request.form.getlist('shares')

    for ticker, shares in zip(ticker_list, share_list):
        if not ticker or not shares:
            continue
        portfolio.set_amount(ticker.upper(), int(shares))

    if portfolio.get_holdings():
        data = holdings_calculator.get_holdings(portfolio)
        data.sort(key=attrgetter('weight'), reverse=True)
    else:
        data = {}

    return render_template('output/output.html', data=data)