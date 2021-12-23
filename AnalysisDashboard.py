import streamlit as st
import datetime
from technicalIndicators import macdIndicator, obvIndicator, stochRsiIndicator
from dataManager import get_historical_data, get_crypto_symbols, get_crypto_name
from technicalIndicatorUtils import analyse, plot_signals

st.title("Technical Analysis Simulator")
st.sidebar.header("Select Parameters")

def get_simulation_params():
  crypto_symbol = st.sidebar.selectbox("Cryptocurrency Symbol", get_crypto_symbols())
  indicator = st.sidebar.selectbox("Technical Indicator", ('MACD Crossover', "On-Balance Volume", "Stochastic RSI"))
  # default stasrt date 1 year ago
  start_date = st.sidebar.date_input("Start Date", datetime.datetime.now() - datetime.timedelta(days=365))
  end_date = st.sidebar.date_input("End Date")
  return crypto_symbol, indicator, start_date, end_date

def apply_technical_indicator(df, indicator):
  if indicator == "MACD Crossover":
    return macdIndicator.execute_MACD(df)
  elif indicator == "On-Balance Volume":
    return obvIndicator.execute_OBV(df)
  elif indicator == "Stochastic RSI":
    return stochRsiIndicator.execute_stochastic_rsi(df)
  else:
    return df

def display_indicator_info(indicator):
  if indicator == 'MACD Crossover':
    macdIndicator.DESCRIPTION
  elif indicator == 'On-Balance Volume': 
    obvIndicator.DESCRIPTION
  elif indicator == 'Stochastic RSI':
    stochRsiIndicator.DESCRIPTION
  else:
    "wait wot.."
# Receive user inputs
symbol, indicator, start, end = get_simulation_params()

# Perform computations
df = get_historical_data(symbol, start, end)
df = analyse(df)
report = apply_technical_indicator(df, indicator)

# Display
st.header((indicator) + " Analysis on " + get_crypto_name(symbol) + " Price")
display_indicator_info(indicator)

st.pyplot(plot_signals(df, symbol))
st.subheader('Trade Summary')
st.write(f"* Total trades: {report['wins'] + report['loss']} ({report['wins']} wins, {report['loss']} losses)")
st.write(f"* Biggest gain: {report['maxGain']}%")
st.write(f"* Smallest gain : {report['maxLoss']}%")
st.write(f"* Net gains captured: {report['netPercentGains']}%")
st.write(f"* Gains with returns reinvested: {report['cumulativePercentageChange']}%")
st.subheader('Trade History')
st.write(report['tradesPlaced'])
