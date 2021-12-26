import pandas as pd
import numpy as np
import requests
from datetime import datetime
from dateutil import tz
from sqlalchemy import create_engine
import psycopg2
import os

# con = psycopg2.connect(dburl)
# con.cursor()
#   API_KEY = os.getenv('YAHOO_FINANCE_API_KEY')

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
  'SOL1': "Solana", 
  # 'USDC': "USD Coin", 
  # 'USDT': "Tether",
  # 'UNI': "Uniswap",
  # 'WBTC': "Wrapped Bitcoin", 
  'XRP': "XRP"
}

def get_historical_data(symbol, start, end):
  # df = pd.read_csv(f'dataset/{symbol}-USD.csv')
  # link to your database
  df = pd.read_sql(f"SELECT * FROM {symbol.lower()}", engine)
  df = df.set_index(pd.DatetimeIndex(df['Date'].values))
  return df.loc[start: end]

def get_crypto_symbols():
  return CRYPTO_SYMBOL_NAMES.keys()

def get_crypto_name(symbol):
  return CRYPTO_SYMBOL_NAMES[f'{symbol}']

def utc_integer_to_utc_date(utc_integer): 
  utc_zone = tz.gettz('UTC')
  return str(datetime.fromtimestamp(utc_integer).astimezone(utc_zone).date())

# # Request data from yahoo finance
# def get_latest_data(crypto_symbol):
#   url = f'https://yfapi.net/v8/finance/chart/{crypto_symbol}-USD?range=1d&region=US&interval=1d&lang=en'
#   API_KEY = os.getenv('YAHOO_FINANCE_API_KEY')
#   headers = {
#     'accept':'application/json',
#     'x-api-key': API_KEY
#   }
#   response = requests.get(url, headers=headers).json()
#   return response

# def update_dataset():
  # crypto_symbol = 'BTC'
  # response = get_latest_data(crypto_symbol)
  # filename = response['chart']['result'][0]['meta']['symbol']
  # utc_integer = response['chart']['result'][0]['timestamp'][0]
  # priceData = response['chart']['result'][0]['indicators']['quote'][0]
  
  # newRow = pd.DataFrame({
  #   'Date': utc_integer_to_utc_date(utc_integer),
  #   'Open': priceData['open'], 
  #   'High': priceData['high'], 
  #   'Low': priceData['low'],
  #   'Close': priceData['close'],
  #   'Volume': priceData['volume'],
  # })

  # df = pd.read_csv(f'dataset/{filename}.csv')
  # newdf = df.append(newRow)
  # newdf.to_csv(f'dataset/{filename}.csv', index=False)