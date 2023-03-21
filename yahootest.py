import yfinance as yf

symbol = 'AAPL'
start_date = '2021-01-01'
end_date = '2021-03-31'

df = yf.download(symbol, start=start_date, end=end_date, adjusted=True)

print(df.head())