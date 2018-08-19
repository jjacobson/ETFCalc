from flask import Flask, render_template, request
from util.webscraper import WebScraper

app = Flask(__name__)

@app.route('/')
def hello_world():
    scraper = WebScraper()
    data = scraper.scrape_ticker('QQQ')
    return str(data[97])

if __name__ == '__main__':
    app.run()
