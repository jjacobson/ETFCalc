import logging
from flask import Flask, render_template, request
from operator import attrgetter
from .util import holdings_calculator
from .util import webscraper
from .util.portfolio import Portfolio

app = Flask(__name__)

@app.route('/')
def main(error=False):
    return render_template('input/input.html', error=error)

@app.route('/output', methods=['POST'])
def output():
    portfolio = Portfolio()

    ticker_list = request.form.getlist('tickers')
    share_list = request.form.getlist('shares')
    price_list = request.form.getlist('prices')

    for ticker, shares, price in zip(ticker_list, share_list, price_list):
        if not (ticker and shares and price):
            continue
        portfolio.set_amount(ticker.upper(), int(shares))
        portfolio.set_price(ticker.upper(), float(price))

    if portfolio.get_holdings():
        try:
            data = holdings_calculator.get_holdings(portfolio)
        except ValueError as e:
            logging.exception('Raised exception while making request')
            return main(True)
        data.sort(key=attrgetter('weight'), reverse=True)
    else:
        data = {}

    return render_template('output/output.html', data=data)

@app.route('/ticker_value', methods=['POST'])
def ticker_value():
    ticker = request.form['ticker']
    ticker = ticker.upper()
    if (webscraper.get_data(ticker) is None):
        logging.info('invalid ticker, ignoring', ticker)
        return 'null'

    price = webscraper.get_price(ticker)
    return str(price)