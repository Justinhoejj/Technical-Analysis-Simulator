import pandas as pd
import numpy as np

DESCRIPTION = (
               ">On-balance volume (OBV) is a technical trading momentum indicator that uses volume flow to predict price changes. "
              + "The OBV is calculated with the following rules. "
              + "If current day close price is higher than previous day, *add* the current day volume to previous day OBV. "
              + "If current day close price is lower than previous day close price, *subtract* the current day volume from the pervious day OBV. " 
              + "A 20 day EMA of OBV aka signal line is then plotted on top of the OBV line. "
              + "A buy signal is produced when the OBV line crosses the signal line and a sell signal produced when the OBV line crosses below the signal line " 
              + "([Read more](https://www.investopedia.com/terms/o/onbalancevolume.asp))."
              )

# On Balance Volume EMA strategy
def execute_OBV(data):
    data['OBV_EMA'] = data['OBV'].ewm(span=20).mean()
    data['Trend'] = np.where(data.OBV > data.OBV_EMA,1 , 0)
    data['Signal'] = data['Trend'].diff()
    data['Buy_Price'] = np.where(data['Signal'] == 1, data['Close'], np.nan)
    data['Sell_Price'] = np.where(data['Signal'] == -1, data['Close'], np.nan)
    data.drop('Trend', axis=1, inplace=True)
    data.drop('Signal', axis=1, inplace=True)

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
        buyPrice = data.Buy_Price[i]
        sellPrice = data.Sell_Price[i]
        currDate = data.Date[i]
        if(not isHolding and not np.isnan(buyPrice)):
            holdQty = cumulativeCapital / buyPrice
            prevBuyPrice = buyPrice
            isHolding = True
            tradesPlaced += f'* {currDate}: Buy at {buyPrice}  \n'
        elif(isHolding and not np.isnan(sellPrice)):
            cumulativeCapital = holdQty * sellPrice
            percentGain = 100 * (sellPrice - prevBuyPrice) / prevBuyPrice
            netPercentGains = netPercentGains + percentGain
            maxLoss = min(maxLoss, percentGain)
            maxGain = max(maxGain, percentGain)
            tradesPlaced += f'* {currDate}: Sell at {sellPrice}  ({np.round(percentGain,2)}%)  \n'
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