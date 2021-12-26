import pandas as pd
import numpy as np
from technicalIndicatorUtils import buy_report_format, sell_report_format

class MacdIndicator:
  DESCRIPTION = (
                ">Moving average convergence divergence (MACD) is a trend-following momentum indicator. "
                + "The MACD is calculated by subtracting the 26-period exponential moving average (EMA) from the 12-period EMA. "
                + "A 9 day EMA of MACD aka signal line is then plotted on top of the MACD line. "
                + "A buy signal is produced when the MACD line crosses above the signal line and a sell signal produced when the MACD line crosses below the signal line ([Read more](https://www.investopedia.com/terms/m/macd.asp))."
              )

  def get_buy_message(self, crypto_symbol, price):
    return f'{crypto_symbol} Buy signal: The MACD line for {crypto_symbol} has crossed above the 9 day EMA of MACD at {price} USD'
  
  def get_buy_message(self, crypto_symbol, price):
    return f'{crypto_symbol} Sell signal: The MACD line for {crypto_symbol} has crossed below the 9 day EMA of MACD at {price} USD'

  # MACD crossover strategy
  def simulate(self, data):
      data['MACD_EMA'] = data.MACD.ewm(span=9, adjust=False).mean()
      data['Trend'] = np.where(data.MACD > data.MACD_EMA,1 , 0)
      data['Signal'] = data['Trend'].diff()
      data['Buy_Price'] = np.where(data['Signal'] == 1, data['Close'], np.nan)
      data['Sell_Price'] = np.where(data['Signal'] == -1, data['Close'], np.nan)
      data.drop('Trend', axis=1, inplace=True)
      data.drop('Signal', axis=1, inplace=True)

      cumulativeCapital = 100
      holdQty = 0
      prevBuyPrice = 0

      # return values
      wins = 0
      loss = 0
      isHolding = False
      netPercentGains = 0
      percentGain = 0
      maxLoss = np.Inf
      maxGain = np.NINF
      tradesPlaced = ""

      for i in range(len(data)):
          buyPrice = data.Buy_Price[i]
          sellPrice = data.Sell_Price[i]
          currDate = data.Date[i]
          if(not isHolding and not np.isnan(buyPrice)):
              holdQty = cumulativeCapital / buyPrice
              prevBuyPrice = buyPrice
              isHolding = True
              tradesPlaced += buy_report_format(currDate, buyPrice)
          elif(isHolding and not np.isnan(sellPrice)):
              cumulativeCapital = holdQty * sellPrice
              percentGain = 100 * (sellPrice - prevBuyPrice) / prevBuyPrice
              netPercentGains = netPercentGains + percentGain
              maxLoss = min(maxLoss, percentGain)
              maxGain = max(maxGain, percentGain)
              tradesPlaced += sell_report_format(currDate, sellPrice, percentGain)

              if(percentGain > 0):
                  wins += 1
              else:
                  loss += 1
              isHolding = False
          else:
              continue
          
      cumulativePercentageChange = np.round(cumulativeCapital - 100, 3)
      netPercentGains = np.round(netPercentGains, 3)
      maxLoss = np.round(maxLoss, 3)
      maxGain = np.round(maxGain, 3)
      report = {'wins': wins, 'maxGain': maxGain, 'loss': loss, 'maxLoss': maxLoss, 'cumulativePercentageChange': cumulativePercentageChange, 'netPercentGains': netPercentGains, 'tradesPlaced': tradesPlaced} 
      return report