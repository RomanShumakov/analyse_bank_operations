import yfinance as yf

dat = yf.Ticker("AAPL")

print(dat.analyst_price_targets)