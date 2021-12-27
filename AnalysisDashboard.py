import datetime
import streamlit as st
from dataManager import get_historical_data, get_crypto_symbols, get_crypto_name
from subscription import add_subscriber
from technicalIndicators.indicatorManager import  get_indicator, get_indicator_names
from technicalIndicatorUtils import analyse, plot_signals, execute_buy_hold

st.title("Technical Analysis Simulator")
st.sidebar.header("Select Parameters")

def get_simulation_params():
  crypto_symbol = st.sidebar.selectbox("Cryptocurrency Symbol", get_crypto_symbols())
  indicator_name = st.sidebar.selectbox("Technical Indicator", get_indicator_names())
  # default stasrt date 1 year ago
  start_date = st.sidebar.date_input("Start Date", datetime.datetime.now() - datetime.timedelta(days=365))
  end_date = st.sidebar.date_input("End Date")
  
  return crypto_symbol, indicator_name, start_date, end_date

def get_subscriber_email(crypto_symbol, indicator_name):
  st.sidebar.write(f'### Get {indicator_name} alerts for {crypto_symbol}')
  form = st.sidebar.form('subscriber email', clear_on_submit=True)
  subscriber_email = form.text_input(label='Email')
  submit_button = form.form_submit_button(label='Subscribe')
  if submit_button:
    add_subscriber(crypto_symbol, indicator_name, subscriber_email)

# Receive user inputs
symbol, indicator_name, start, end = get_simulation_params()
st.sidebar.write("##")
get_subscriber_email(symbol, indicator_name)

# Perform computations
indicator = get_indicator(indicator_name)
df = get_historical_data(symbol, start, end)
df = analyse(df)
report = indicator.simulate(df)
gains_from_buy_and_hold = execute_buy_hold(df)

# Display
st.header((indicator_name) + " Analysis on " + get_crypto_name(symbol) + " Price")
st.write(indicator.DESCRIPTION)

st.pyplot(plot_signals(df, symbol))
st.subheader('Trade Summary')
st.write(f"* Total trades: {report['wins'] + report['loss']} ({report['wins']} wins, {report['loss']} losses)")
st.write(f"* Biggest gain: {report['maxGain']}%")
st.write(f"* Smallest gain : {report['maxLoss']}%")
st.write(f"* Net gains captured: {report['netPercentGains']}%")
st.write(f"* Gains with returns reinvested: {report['cumulativePercentageChange']}%")
st.write(f"* Gains with buy and hold strategy: {gains_from_buy_and_hold}%")
st.subheader('Trade History')
st.write(report['tradesPlaced'])
