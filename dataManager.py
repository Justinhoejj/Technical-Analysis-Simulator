import pandas as pd
from dateutil import tz
import requests
from datetime import datetime
from sqlalchemy import create_engine
import os

uri = os.getenv("DATABASE_URL") 
if uri and uri.startswith("postgres://"):
    uri = uri.replace("postgres://", "postgresql://", 1)
engine = create_engine(uri, echo = False)

CRYPTO_SYMBOL_NAMES = {
  'ADA': "Cardano", 
  'AVAX': "Avalanche", 
  'BNB': "Binance Coin", 
  'BTC': "Bitcoin", 
  # 'BUSD': "Binance USD", 
  'CRO': "Crypto.com Coin", 
  'DOGE': "Dogecoin", 
  'DOT': "Polkadot", 
  'ETH': "Ethereum", 
  # 'LINK': "Chainlink", 
  # 'LTC': "Litecoin", 
  'LUNA1': "Terra", 
  'MATIC': "Polygon", 
  'SHIB': "SHIBA INU", 
  # 'SOL1': "Solana", 
  # 'USDC': "USD Coin", 
  # 'USDT': "Tether",
  # 'UNI': "Uniswap",
  # 'WBTC': "Wrapped Bitcoin", 
  'XRP': "XRP"
}


def get_crypto_symbols():
  return CRYPTO_SYMBOL_NAMES.keys()

def get_crypto_name(symbol):
  return CRYPTO_SYMBOL_NAMES[f'{symbol}']

uri = os.getenv("DATABASE_URL") 
if uri and uri.startswith("postgres://"):
    uri = uri.replace("postgres://", "postgresql://", 1)
engine = create_engine(uri, echo = False)

def get_historical_data(symbol, start, end):
  # link to your database
  df = pd.read_sql(f"SELECT * FROM {symbol.lower()}", engine)
  df = df.set_index(pd.DatetimeIndex(df['Date'].values))
  return df.loc[start: end]

def get_crypto_symbols():
  return CRYPTO_SYMBOL_NAMES.keys()

def utc_integer_to_utc_date(utc_integer): 
  utc_zone = tz.gettz('UTC')
  return str(datetime.fromtimestamp(utc_integer).astimezone(utc_zone).date())

# Request data from yahoo finance
def get_latest_data(crypto_symbol):
  url = f'https://yfapi.net/v8/finance/chart/{crypto_symbol}-USD?range=1d&region=US&interval=1d&lang=en'
  API_KEY = os.getenv('YAHOO_FINANCE_API_KEY')
  headers = {
    'accept':'application/json',
    'x-api-key': API_KEY
  }
  response = requests.get(url, headers=headers).json()
  return response

# Save data to data base
def update_dataset(crypto_symbol):
  print(f'fetching{crypto_symbol}...')
  response = get_latest_data(crypto_symbol)
  print(response)
  utc_integer = response['chart']['result'][0]['timestamp'][0]
  priceData = response['chart']['result'][0]['indicators']['quote'][0]
  
  newRow = pd.DataFrame({
    'Date': utc_integer_to_utc_date(utc_integer),
    'Open': priceData['open'], 
    'High': priceData['high'], 
    'Low': priceData['low'],
    'Close': priceData['close'],
    'Volume': priceData['volume'],
  })

  newRow.to_sql(f'{crypto_symbol.lower()}', con = engine, if_exists='append', index=False)
  print(f"saved {crypto_symbol} to db successfully")




if __name__ == '__main__':
  for key in get_crypto_symbols():
    try:
      update_dataset(key)
    except Exception:
      continue