# src/data_loader.py

import ccxt
import pandas as pd
import yfinance as yf  # <-- Import yfinance
import os
from datetime import datetime
from src import config # Import our configuration

def _fetch_ccxt_data():
    """Fetches data using ccxt (for Crypto)."""
    print(f"Fetching from {config.EXCHANGE} via ccxt...")
    exchange_class = getattr(ccxt, config.EXCHANGE)
    exchange = exchange_class({'enableRateLimit': True})
    
    start_dt = datetime.strptime(config.START_DATE, '%Y-%m-%d')
    start_timestamp = int(start_dt.timestamp() * 1000)
    
    ohlcv = exchange.fetch_ohlcv(config.ASSET, config.TIMEFRAME, since=start_timestamp, limit=5000)
    
    if not ohlcv:
        raise ValueError("Error: No data returned from ccxt exchange.")
        
    df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    df.set_index('timestamp', inplace=True)
    df = df.apply(pd.to_numeric)
    return df

def _fetch_yfinance_data():
    """Fetches data using yfinance (for Stocks/FX)."""
    print(f"Fetching {config.ASSET} from Yahoo Finance...")
    
    df = yf.download(
        config.ASSET,
        start=config.START_DATE,
        interval=config.TIMEFRAME
    )
    
    if df.empty:
        raise ValueError("Error: No data returned from yfinance.")
    
    # Standardize column names (yfinance uses 'Close', we need 'close')
    df.rename(columns={
        'Open': 'open',
        'High': 'high',
        'Low': 'low',
        'Close': 'close',
        'Volume': 'volume'
    }, inplace=True)
    
    # Standardize index name
    df.index.name = 'timestamp'
    return df

def fetch_and_save_data():
    """
    Fetches historical OHLCV data from the source specified in config
    and saves it to a CSV file.
    
    Returns:
        pd.DataFrame: A pandas DataFrame with the OHLCV data.
    """
    
    # --- 1. Check if cached data exists ---
    if os.path.exists(config.DATA_FILEPATH):
        print(f"Data file found. Loading from {config.DATA_FILEPATH}...")
        try:
            df = pd.read_csv(config.DATA_FILEPATH, index_col='timestamp', parse_dates=True)
            print("Data loaded successfully from cache.")
            return df
        except Exception as e:
            print(f"Error loading data from cache: {e}. Re-fetching.")

    # --- 2. If no cache, fetch from the configured source ---
    print(f"No cached data found. Fetching from source: {config.DATA_SOURCE}")
    
    try:
        if config.DATA_SOURCE == 'ccxt':
            df = _fetch_ccxt_data()
        elif config.DATA_SOURCE == 'yfinance':
            df = _fetch_yfinance_data()
        else:
            raise ValueError(f"Unknown DATA_SOURCE: {config.DATA_SOURCE}")

        # --- 3. Create directory and save to cache ---
        os.makedirs(os.path.dirname(config.DATA_FILEPATH), exist_ok=True)
        df.to_csv(config.DATA_FILEPATH)
        print(f"Data fetched and saved to {config.DATA_FILEPATH}")

        return df

    except Exception as e:
        print(f"An error occurred during data fetching: {e}")
        return pd.DataFrame()

# --- Standalone test ---
if __name__ == '__main__':
    # This block allows us to run this file directly to test it
    print("Running data_loader as a standalone script...")
    
    # Temporarily override config for testing
    config.DATA_SOURCE = 'yfinance'
    config.ASSET = 'EURUSD=X'
    config.DATA_FILEPATH = 'data/TEST_eurusd_1d.csv'
    
    data = fetch_and_save_data()
    
    if not data.empty:
        print("\n--- Data Head (EUR/USD) ---")
        print(data.head())
        print("\n--- Data Tail (EUR/USD) ---")
        print(data.tail())