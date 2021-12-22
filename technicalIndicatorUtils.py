import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
plt.style.use('fivethirtyeight')

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
    avgLoss = down.ewm(span=period, adjust=False).mean()
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
def analyse(filePath):
    df = pd.read_csv(f'{filePath}')
    df = df.set_index(pd.DatetimeIndex(df['Date'].values))
    df['OBV'] = analyse_OBV(df)
    df['RSI'] = analyse_stochRSI(df)
    df['MACD'] = analyse_MACD(df)
    df['ATR'] = analyse_ATR(df)
    bollinger_bands = analyse_upper_lower_bollinger_bands(df)
    df['Upper Bollinger Band'] = bollinger_bands[0]
    df['Lower Bollinger Band'] = bollinger_bands[1]
    return df

# On Balance Volume EMA strategy
def execute_OBV_EMA(data, use_stop_loss=False):
    data['OBV_EMA'] = data['OBV'].ewm(span=20).mean()
    data['Trend'] = np.where(data.OBV > data.OBV_EMA,1 , 0)
    data['Signal'] = data['Trend'].diff()
    data['OBV_Buy_Price'] = np.where(data['Signal'] == 1, data['Close'], np.nan)
    data['OBV_Sell_Price'] = np.where(data['Signal'] == -1, data['Close'], np.nan)
    data.drop('Trend', axis=1, inplace=True)
    data.drop('Signal', axis=1, inplace=True)

    cumulativeCapital = 100
    holdQty = 0
    stopLoss = 0
    prevBuyPrice = 0
    isHolding = False
    wins = 0
    loss = 0
    netPercentGains = 0
    percentGain = 0
    maxLoss = np.Inf
    maxGain = np.NINF
    
    for i in range(len(data)):
        dayClose = data.Close[i]
        buyPrice = data.OBV_Buy_Price[i]
        sellPrice = data.OBV_Sell_Price[i]
        if(not isHolding and not np.isnan(buyPrice)):
            holdQty = cumulativeCapital / buyPrice
            prevBuyPrice = buyPrice
            isHolding = True
        elif(isHolding and not np.isnan(sellPrice)):
            cumulativeCapital = holdQty * sellPrice
            percentGain = 100 * (sellPrice - prevBuyPrice) / prevBuyPrice
            netPercentGains = netPercentGains + percentGain
            maxLoss = min(maxLoss, percentGain)
            maxGain = max(maxGain, percentGain)
            if(percentGain > 0):
                wins += 1
            else:
                loss += 1
            isHolding = False
        elif(use_stop_loss and dayClose < stopLoss):
            cumulativeCapital = holdQty * dayClose
            percentGain = 100 * (dayClose - prevBuyPrice) / prevBuyPrice
            netPercentGains = netPercentGains + percentGain
            maxLoss = min(maxLoss, percentGain)
            maxGain = max(maxGain, percentGain)
            if(percentGain > 0):
                wins += 1
            else:
                loss += 1
            isHolding = False
        else:
            continue
        stopLoss = dayClose - 2 * data.ATR[i]
    
    cumulativePercentageChange = np.round(cumulativeCapital - 100, 3)
    netPercentGains = np.round(netPercentGains, 3)
    maxLoss = np.round(maxLoss, 3)
    maxGain = np.round(maxGain, 3)
    
    return f'Wins:{wins}, max gain:{maxGain}% \nLosses:{loss}, max loss: {maxLoss}%\nCompounded Percentage Gains: {cumulativePercentageChange}% \nCumulative percentage gains: {netPercentGains}%'

# MACD crossover strategy
def execute_MACD(data, use_stop_loss=False):
    data['MACD_EMA'] = data.MACD.ewm(span=9, adjust=False).mean()
    data['Trend'] = np.where(data.MACD > data.MACD_EMA,1 , 0)
    data['Signal'] = data['Trend'].diff()
    data['MACD_Buy_Price'] = np.where(data['Signal'] == 1, data['Close'], np.nan)
    data['MACD_Sell_Price'] = np.where(data['Signal'] == -1, data['Close'], np.nan)
    data.drop('Trend', axis=1, inplace=True)
    data.drop('Signal', axis=1, inplace=True)

    cumulativeCapital = 100
    holdQty = 0
    stopLoss = 0
    prevBuyPrice = 0
    wins = 0
    loss = 0
    isHolding = False
    netPercentGains = 0
    percentGain = 0
    maxLoss = np.Inf
    maxGain = np.NINF
    
    for i in range(len(data)):
        buyPrice = data.MACD_Buy_Price[i]
        sellPrice = data.MACD_Sell_Price[i]
        dayClose = data.Close[i]
        if(not isHolding and not np.isnan(buyPrice)):
            holdQty = cumulativeCapital / buyPrice
            prevBuyPrice = buyPrice
            isHolding = True
        elif(isHolding and not np.isnan(sellPrice)):
            cumulativeCapital = holdQty * sellPrice
            percentGain = 100 * (sellPrice - prevBuyPrice) / prevBuyPrice
            netPercentGains = netPercentGains + percentGain
            maxLoss = min(maxLoss, percentGain)
            maxGain = max(maxGain, percentGain)
            if(percentGain > 0):
                wins += 1
            else:
                loss += 1
            isHolding = False
        elif(use_stop_loss and isHolding and dayClose < stopLoss):
            cumulativeCapital = holdQty * dayClose
            percentGain = 100 * (dayClose - prevBuyPrice) / prevBuyPrice
            netPercentGains = netPercentGains + percentGain
            maxLoss = min(maxLoss, percentGain)
            maxGain = max(maxGain, percentGain)
            if(percentGain > 0):
                wins += 1
            else:
                loss += 1
            isHolding = False
        else:
            continue
        stopLoss = dayClose - data.ATR[i]
        
    cumulativePercentageChange = np.round(cumulativeCapital - 100, 3)
    netPercentGains = np.round(netPercentGains, 3)
    maxLoss = np.round(maxLoss, 3)
    maxGain = np.round(maxGain, 3)
    
    return f'Wins:{wins}, max gain:{maxGain}% \nLosses:{loss}, max loss: {maxLoss}%\nCompounded Percentage Gains: {cumulativePercentageChange}% \nCumulative percentage gains: {netPercentGains}%'

# OBV and MACD strategy combined
def execute_MACD_OBV(data, use_stop_loss=False):
    cumulativeCapital = 100
    holdQty = 0
    stopLoss = 0
    prevBuyPrice = 0
    wins = 0
    loss = 0
    isHolding = False
    netPercentGains = 0
    percentGain = 0
    maxLoss = np.Inf
    maxGain = np.NINF
    
    for i in range(len(data)):
        buyPrice = data.OBV_Buy_Price[i]
        sellPrice = data.MACD_Sell_Price[i]
        dayClose = data.Close[i]
        if(not isHolding and not np.isnan(buyPrice)):
            holdQty = cumulativeCapital / buyPrice
            prevBuyPrice = buyPrice
            isHolding = True
        elif(isHolding and not np.isnan(sellPrice)):
            cumulativeCapital = holdQty * sellPrice
            percentGain = 100 * (sellPrice - prevBuyPrice) / prevBuyPrice
            netPercentGains = netPercentGains + percentGain
            maxLoss = min(maxLoss, percentGain)
            maxGain = max(maxGain, percentGain)
            if(percentGain > 0):
                wins += 1
            else:
                loss += 1
            isHolding = False
        elif(use_stop_loss and isHolding and dayClose < stopLoss):
            cumulativeCapital = holdQty * dayClose
            percentGain = 100 * (dayClose - prevBuyPrice) / prevBuyPrice
            netPercentGains = netPercentGains + percentGain
            maxLoss = min(maxLoss, percentGain)
            maxGain = max(maxGain, percentGain)
            if(percentGain > 0):
                wins += 1
            else:
                loss += 1
            isHolding = False
        else:
            continue
        stopLoss = dayClose - data.ATR[i]
            
    cumulativePercentageChange = np.round(cumulativeCapital - 100, 3)
    netPercentGains = np.round(netPercentGains, 3)
    maxLoss = np.round(maxLoss, 3)
    maxGain = np.round(maxGain, 3)
    
    return f'Wins:{wins}, max gain:{maxGain}% \nLosses:{loss}, max loss: {maxLoss}%\nCompounded Percentage Gains: {cumulativePercentageChange}% \nCumulative percentage gains: {netPercentGains}%'
    
def plot_close_price(df):
    # View closing price
    plt.figure(figsize=(15, 8))
    plt.title('Price History', fontsize=18)
    plt.plot(df['Close'])
    plt.xlabel('Date', fontsize=18)
    plt.ylabel('Close Price in USD', fontsize=18)
    plt.show()

def execute_buy_hold(df):
    buyAt = df['Close'][0]
    sellAt = df['Close'][len(df.index)-1]
    percentChange = (sellAt - buyAt) * 100 / (buyAt)
    return f'Percent change: {np.round(percentChange, 3)}%'
    