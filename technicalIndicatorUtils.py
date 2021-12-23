import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# On balance volume
def analyse_OBV(data):
    OBV = [0]
    for i in range(1, len(data.Close)):
        if data.Close[i] > data.Close[i - 1]:
            OBV.append(OBV[-1] + data.Volume[i])
        elif data.Close[i] < data.Close[i - 1]:
            OBV.append(OBV[-1] - data.Volume[i])
        else:
            OBV.append(OBV[-1])
    return OBV

# Stochastic RSI
def analyse_stochRSI(data, period=14):
    delta = data.Close.diff(1)
    delta = delta.dropna()
    up = delta.copy()
    down = delta.copy()
    up[up < 0] = 0
    down[down > 0] = 0
    avgGain = up.ewm(span=period, adjust=False).mean()
    avgLoss = abs(down.ewm(span=period, adjust=False).mean())
    rs = avgGain/avgLoss
    rsi = 100 - (100 / (1 + rs))
    stochRsi = (rsi - rsi.rolling(period).min()) / (rsi.rolling(period).max() - rsi.rolling(period).min())
    return stochRsi

# Moving Average Convergence Divergence
def analyse_MACD(data, short_span=12, long_span=26):
    shortEma = data.Close.ewm(span=short_span, adjust=False).mean()
    longEma = data.Close.ewm(span=long_span, adjust=False).mean()
    macd = shortEma - longEma
    return macd

# Simple moving average
def sma(data, period=30):
    return data.Close.rolling(period).mean()

# Exponential moving average
def ema(data, period=30):
    return data.Close.ewm(window=period).mean()

# Bollinger Bands
def analyse_upper_lower_bollinger_bands(data, period=20):
    sma = data.Close.rolling(window=period).mean()
    sd = data.Close.rolling(window=period).std()
    upperBand = sma + (sd * 2)
    lowerBand = sma - (sd * 2)
    return (upperBand, lowerBand)

# Average True Range
def analyse_ATR(data, period=20):
    high_low = data['High'] - data['Low']
    high_prevClose = np.abs(data['High'] - data['Close'].shift(1))
    low_prevClose = np.abs(data['Low'] - data['Close'].shift(1))
    tempdf = pd.concat([high_low, high_prevClose, low_prevClose], axis=1)
    tempdf.dropna(subset=[0, 1, 2], inplace=True)
    true_range = tempdf.max(axis=1)
    ATR = true_range.rolling(14).mean()
    return ATR

# Analyse CSV
def analyse(df):
    df = df.set_index(pd.DatetimeIndex(df['Date'].values))
    df['OBV'] = analyse_OBV(df)
    df['Stochastic RSI'] = analyse_stochRSI(df)
    df['MACD'] = analyse_MACD(df)
    df['ATR'] = analyse_ATR(df)
    bollinger_bands = analyse_upper_lower_bollinger_bands(df)
    df['Upper Bollinger Band'] = bollinger_bands[0]
    df['Lower Bollinger Band'] = bollinger_bands[1]
    return df

# Visualise Close price with Buy Sell signals
def plot_signals(df, symbol):
    fig = plt.figure(figsize=(15, 8))
    plt.scatter(df.index, df['Buy_Price'], color = 'green', label='Buy', marker='^', alpha=1)
    plt.scatter(df.index, df['Sell_Price'], color = 'red', label='Sell', marker='v', alpha=1)
    plt.plot(df['Close'], label='Close Price', alpha=0.35)
    plt.title(f'{symbol} Price History', fontsize=18)
    plt.xticks(rotation=45)
    plt.xlabel('Date', fontsize=18)
    plt.ylabel('Close Price in USD($)', fontsize=18)
    plt.legend(loc='upper left')
    return fig  

def buy_report_format(currDate, buyPrice):
  return f'* {currDate}: Buy at {buyPrice}  \n'

def sell_report_format(currDate, sellPrice, percentGain):
  return f'* {currDate}: Sell at {sellPrice}  ({np.round(percentGain,2)}%)  \n'

def execute_buy_hold(df):
    buyAt = df['Close'][0]
    sellAt = df['Close'][len(df.index)-1]
    percentChange = (sellAt - buyAt) * 100 / (buyAt)
    return f'Percent change: {np.round(percentChange, 3)}%'  