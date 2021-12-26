from technicalIndicators.macdIndicator import MacdIndicator
from technicalIndicators.obvIndicator import ObvIndicator
from technicalIndicators.stochRsiIndicator import  StochRsiIndicator

def get_indicator_names():
  return ("MACD Crossover", "On-Balance Volume", "Stochastic RSI")

def get_indicator(indicator_name):
  if indicator_name == 'MACD Crossover':
    return MacdIndicator()
  elif indicator_name == 'On-Balance Volume': 
    return ObvIndicator()
  elif indicator_name == 'Stochastic RSI':
    return StochRsiIndicator()
  else:
    return None