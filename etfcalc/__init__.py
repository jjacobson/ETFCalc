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

    tickers = request.form.getlist('tickers')
    shares = request.form.getlist('shares')

    for ticker, shares in zip(tickers, shares):
        portfolio.set_amount(ticker, int(shares))

    data = holdings_calculator.get_holdings(portfolio)
    data.sort(key=attrgetter('weight'), reverse=True)

    return render_template('output/output.html', data=data)