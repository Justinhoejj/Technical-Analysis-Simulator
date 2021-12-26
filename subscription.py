import pandas as pd
from dateutil import tz
import requests
from datetime import datetime
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv

# Set up connections
load_dotenv()
database_url = os.getenv("DATABASE_URL") 
if database_url and database_url.startswith("postgres://"):
    database_url = database_url.replace("postgres://", "postgresql://", 1)
engine = create_engine(database_url, echo = False)

# def simulate_notify(crypto_symbol):
#     df = pd.read_sql(f"SELECT * FROM {symbol.lower()}", engine)
