import numpy as np
import pandas as pd
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv
from notification import send_mail
from technicalIndicatorUtils import analyse
from technicalIndicators.indicatorManager import get_indicator_names, get_indicator

# Set up connections
load_dotenv()
database_url = os.getenv("DATABASE_URL") 
if database_url and database_url.startswith("postgres://"):
    database_url = database_url.replace("postgres://", "postgresql://", 1)
engine = create_engine(database_url, echo = False)

def send_confirmation_message(crypto_symbol, indicator_name, subscriber_email):
  subject = f'Subscribed to {indicator_name} on {crypto_symbol} '
  message = (f'You have subscribed to alerts from {indicator_name} on {crypto_symbol}. To unsubscribe reply with subject: UNSUB-{crypto_symbol}-{indicator_name}' 
  + '<br/><br/>Disclaimer: This service is in testing phase performance not garuanteed and service provided at best effort. '
  + 'The sigenals provided mrely reflect computations of the various technical indicators and do not garuantee any returns. ' 
  + 'Past performance does not garuantee future performance ensure due dilligence is done before making any cryptocurrency purchases.')
  send_mail(subscriber_email, subject, message)

def add_subscriber(crypto_symbol, indicator_name, subscriber_email):
  subscription = pd.DataFrame({
    'crypto': crypto_symbol,
    'indicator': indicator_name, 
    'email': subscriber_email
    }, index=[0])
  try:
    send_confirmation_message(crypto_symbol, indicator_name, subscriber_email)
    subscription.to_sql('subscription', con = engine, if_exists='append', index=False)  
    print(f'new subscription: {crypto_symbol}, {indicator_name}, {subscriber_email}')
    return True
  except:
    return False


def get_subscribers(crypto_symbol, indicator_name):
    df = pd.read_sql(f"SELECT email FROM subscription WHERE crypto='{crypto_symbol}' AND indicator='{indicator_name}'", engine)
    return df['email'].tolist()

def send_buy_signal(crypto_symbol, indicator_name, message):
    subject = f'Bullish signal for {crypto_symbol} with {indicator_name}'
    subscribers = get_subscribers(crypto_symbol, indicator_name)
    if(len(subscribers) > 0):
      send_mail(subscribers, subject, message)

def send_sell_signal(crypto_symbol, indicator_name, message):
    subject = f'Bearish signal for {crypto_symbol} with {indicator_name}'
    subscribers = get_subscribers(crypto_symbol, indicator_name)
    if(len(subscribers) > 0):
      send_mail(subscribers, subject, message)
    

def simulate_notify(crypto_symbol):
  df = pd.read_sql(f'SELECT * FROM {crypto_symbol.lower()}', engine)
  # Set date as idnex
  df = df.set_index(pd.DatetimeIndex(df['Date'].values))
  df = analyse(df)
  for indicator_name in get_indicator_names():
    indicator = get_indicator(indicator_name)
    indicator.simulate(df)
    lastIndex = len(df) - 1
    buy_price = df['Buy_Price'][lastIndex]
    sell_price = df['Sell_Price'][lastIndex]
    if not np.isnan(buy_price):
        buy_message = indicator.get_buy_message(crypto_symbol, buy_price)
        send_buy_signal(crypto_symbol, indicator_name, buy_message)
    if not np.isnan(sell_price):
        sell_message = indicator.get_sell_message(crypto_symbol, buy_price)
        send_sell_signal(crypto_symbol, indicator_name, sell_message)

