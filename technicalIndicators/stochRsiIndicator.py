import pandas as pd
import numpy as np
from technicalIndicatorUtils import buy_report_format, sell_report_format

class StochRsiIndicator:
  DESCRIPTION = (">Stochastic Relative Strength Index (StochRSI) is a technical analysis indicator that range from 0 to 1. "
                + "A StochRSI above 0.8 is considered overbought while a reading below 0.2 is is considered oversold. "
                + "The calculation for RSI considers the maximum and minimum RSI value over a 14 day time period. "
                + "A buy signal is produced when the StochRSI exits the oversold region and a sell signal is produced when the StochRSI exits the overbought region "
                + "([read more](https://www.investopedia.com/terms/s/stochrsi.asp)).")
  
  def get_buy_message(self, crypto_symbol, price):
    return f'{crypto_symbol} Buy signal: The Stochastic RSI for {crypto_symbol} exited the over-sold region at {price} USD'
  
  def get_sell_message(self, crypto_symbol, price):
    return f'{crypto_symbol} Sell signal: The Stochastic RSI for {crypto_symbol} exited the over-bought region at {price} USD'

  def simulate(self, data):
      buySignal = []
      sellSignal = []

      isCurrentlyOverSold = False
      isCurrentlyOverBought = False
      cumulativeCapital = 100
      holdQty = 0
      prevBuyPrice = 0
      isHolding = False

      # return values
      wins = 0
      loss = 0
      netPercentGains = 0
      percentGain = 0
      maxLoss = np.Inf
      maxGain = np.NINF
      tradesPlaced = ""
      
      for i in range(len(data)):
          currDate = data.Date[i]
          currPrice = data.Close[i]
          stochRsi = data['Stochastic RSI'][i] 
          if(stochRsi > 0.2 and isCurrentlyOverSold and not isHolding):
              # RSI exits oversold region buillish sign to buy
              isCurrentlyOverSold = False
              buySignal.append(currPrice)
              sellSignal.append(np.nan)
              holdQty = cumulativeCapital / currPrice
              prevBuyPrice = currPrice
              isHolding = True
              tradesPlaced += buy_report_format(currDate, currPrice)
          elif(isHolding and stochRsi < 0.8 and isCurrentlyOverBought):
            # RSI exits overbought region bearish sign to sell
              isCurrentlyOverBought = False
              buySignal.append(np.nan)
              sellSignal.append(currPrice)
              cumulativeCapital = holdQty * currPrice
              percentGain = 100 * (currPrice - prevBuyPrice) / prevBuyPrice
              netPercentGains = netPercentGains + percentGain
              maxLoss = min(maxLoss, percentGain)
              maxGain = max(maxGain, percentGain)
              tradesPlaced += sell_report_format(currDate, currPrice, percentGain)
              if(percentGain > 0):
                  wins += 1
              else:
                  loss += 1
              isHolding = False
          elif(stochRsi < 0.2 ):
              # RSI enters oversold region
              isCurrentlyOverSold = True
              buySignal.append(np.nan)
              sellSignal.append(np.nan)
          elif(stochRsi > 0.8):
              # RSI enters overbought region
              isCurrentlyOverBought = True
              buySignal.append(np.nan)
              sellSignal.append(np.nan)
          else:
              buySignal.append(np.nan)
              sellSignal.append(np.nan)
      
      # Append data for plot
      data['Buy_Price'] = buySignal
      data['Sell_Price'] = sellSignal

      cumulativePercentageChange = np.round(cumulativeCapital - 100, 3)
      netPercentGains = np.round(netPercentGains, 3)
      maxLoss = np.round(maxLoss, 3)
      maxGain = np.round(maxGain, 3)
      
      report = {'wins': wins, 'maxGain': maxGain, 'loss': loss, 'maxLoss': maxLoss, 'cumulativePercentageChange': cumulativePercentageChange, 'netPercentGains': netPercentGains, 'tradesPlaced': tradesPlaced} 
      return report
