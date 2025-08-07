import yfinance as yf

# Example: Get historical data for Siemens AG (Frankfurt stock exchange ticker: SIE.DE)
#data = yf.download("SIE.DE", start="2024-01-01", end="2024-12-31")
#print(data)

from yahooquery import Ticker
appl = Ticker('aapl')

print(appl.summary_detail)