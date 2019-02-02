# ETFCalc

## Objective
An [exchange traded fund (etf)](https://en.wikipedia.org/wiki/Exchange-traded_fund) holds a number of underlying stocks. This tool attempts to simplify viewing the portion of a portfolio that is made up by the underlying stocks of ETFs. The tool allows a user to enter the list of stocks and ETFs held in their portfolio and will then calculate and output the percentage of the portfolio that each underlying stock makes up.

##  Steps Taken
I used this project to familiarize myself with web development and the flask framework. Stock price data is retrieved from yahoo finance through the use of Pandas Datareader or a backup data scraper accessing the site itself. ETF holdings are currently scraped from http://etfdb.com through python requests.

### Pictures
![Input page](https://i.imgur.com/0T4CALr.png)
![Output page](https://i.imgur.com/hXzEMJg.png)
