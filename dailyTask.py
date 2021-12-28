from dataManager import get_crypto_symbols ,update_price_data
from subscription import simulate_notify
from notification import send_mail

def daily_task():
  for crypto_symbol in get_crypto_symbols():
    try:
      # Update price data
      update_price_data(crypto_symbol)
    except Exception as e:
      send_mail('hoejj05@gmail.com', 
      f'Failed to update price for {crypto_symbol}',
      str(e))
      continue
    try:
      # Notify subscribers
      simulate_notify(crypto_symbol)
    except Exception as e:
      send_mail('hoejj05@gmail.com', 
      f'Failed to simulate and notifiy for {crypto_symbol}',
      str(e))
      continue
    

if __name__ == '__main__':
  daily_task()