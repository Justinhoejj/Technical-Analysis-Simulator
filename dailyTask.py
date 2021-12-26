from dataManager import get_crypto_symbols ,update_price_data
from subscription import simulate_notify

def daily_task():
  # Update price data
  for crypto_symbol in get_crypto_symbols():
    try:
      update_price_data(crypto_symbol)
      simulate_notify(crypto_symbol)
    except Exception:
      continue
  
  # Notify subscribers


if __name__ == '__main__':
  daily_task()