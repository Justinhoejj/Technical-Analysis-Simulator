import streamlit as st
import pandas as pd
import datetime
import plotly.graph_objects as go
import matplotlib.pyplot as plt
from technicalIndicatorUtils import analyse, execute_MACD

st.title("Technical Analysis Simulator")
st.sidebar.header("Select Parameters")

def get_input():
  indicator = st.sidebar.selectbox("Technical Indicator", ('MACD',''))
  start_date = st.sidebar.text_input("Start Date", "2020-01-01")
  end_date = st.sidebar.text_input("End Date", "2020-08-01")
  crypto_symbol = st.sidebar.selectbox("Cryptocurrency", ('BTC', 'ETH', 'DOGE'))
  return start_date, end_date, crypto_symbol

def get_crypto_name(symbol):
  symbol = symbol.upper()
  if symbol == "BTC":
    return "Bitcoin"
  elif symbol == "ETH":
    return "Ethereum"
  elif symbol == "DOGE":
    return "Dogecoin"
  else:
    return "NONE"

def get_data(symbol, start, end):
  symbol = symbol.upper()
  if symbol == "BTC":
    df = analyse("/Users/justinhoe/Desktop/Projects/BTC-AlgoTradeAnalysis/testDataset/BTC-USD.csv")
  elif symbol == "ETH":
    df = analyse("/Users/justinhoe/Desktop/Projects/BTC-AlgoTradeAnalysis/testDataset/ETH-USD.csv")
  elif symbol == "DOGE":
    df = analyse("/Users/justinhoe/Desktop/Projects/BTC-AlgoTradeAnalysis/testDataset/DOGE-USD.csv")
  else: 
    df = pd.DataFrame(columns=['Date', 'Close', 'Open','Volume', 'Adj Close'])
  
  start = pd.to_datetime(start)
  end = pd.to_datetime(end)

  execute_MACD(df)
  df = df.set_index(pd.DatetimeIndex(df['Date'].values))

  return df.loc[start: end]


start, end, symbol = get_input()
df = get_data(symbol, start, end)
crypto_name = get_crypto_name(symbol)

st.header(crypto_name + " Close Price")
fig = plt.figure(figsize=(12.2, 4.5))
plt.scatter(df.index, df['MACD_Buy_Price'], color = 'green', label='Buy', marker='^', alpha=1)
plt.scatter(df.index, df['MACD_Sell_Price'], color = 'red', label='Sell', marker='v', alpha=1)
plt.plot(df['Close'], label='Close Price', alpha=0.35)
plt.title('Close Price Buy Sell Signals')
plt.xticks(rotation=45)
plt.xlabel('Date')
plt.ylabel('Close Price USD ($)')
plt.legend(loc='upper left')
st.pyplot(fig)