import pandas as pd
import numpy as np

def get_historical_data(symbol, start, end):
  df = pd.read_csv(f'dataset/{symbol}-USD.csv')
  df = df.set_index(pd.DatetimeIndex(df['Date'].values))
  return df.loc[start: end]

def get_crypto_symbols():
  return ('BTC', 'DOGE', 'EOS', 'ETH', 'LINK', 'LTC', 'XRP' )

def get_crypto_name(symbol):
  symbol = symbol.upper()
  if symbol == "BTC":
    return "Bitcoin"
  elif symbol == "DOGE":
    return "Dogecoin"
  elif symbol == "EOS":
    return "EOS"
  elif symbol == "ETH":
    return "Ethereum"
  elif symbol == "LINK":
    return "Chainlink"
  elif symbol == "LTC":
    return "Litecoin"
  elif symbol == "XRP":
    return "Ripple"
  else:
    return "NONE"