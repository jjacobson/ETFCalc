from flask import Flask, render_template, request
from util import webscraper

app = Flask(__name__)

@app.route('/')
def hello_world():
    data = webscraper.scrape_ticker('QQQ')
    return str(data[97])

if __name__ == '__main__':
    app.run()
