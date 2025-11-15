# Install yfinance library
!pip install yfinance --quiet

import yfinance as yf
import pandas as pd

# Define the tickers and date range
tickers = "BBRI.JK"
start_date = "2020-10-07"
end_date = "2025-10-07"
# Loop through tickers and download data
print(f"\n==============================")
print(f"📥 Downloading data {tickers}")
print(f"==============================")
try:
  # Download data
  data = yf.download(tickers, start=start_date, end=end_date)

  # Save to CSV
  data.to_csv(f'{tickers}_OHLC_Data_5y.csv')

  print(f"📊 Preview Data {ticker}:")
  print(data)
  print(f"📊 Summary Data {ticker}:")
  print(data.info())
  print(f"✅ Successfully downloaded {ticker}")

except Exception as e:
  print(f"❌ Failed to download {ticker}: {e}")
