from dataManager import get_crypto_symbols ,update_price_data
from subscription import simulate_notify

def daily_task():
  for crypto_symbol in get_crypto_symbols():
    try:
      # Update price data
      update_price_data(crypto_symbol)
      # Notify subscribers
      simulate_notify(crypto_symbol)
    except Exception:
      continue
    

if __name__ == '__main__':
  daily_task()