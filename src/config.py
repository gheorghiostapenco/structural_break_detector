# src/config.py

# --- Data Source Settings ---
# 'ccxt' for Crypto, 'yfinance' for Stocks/FX
DATA_SOURCE = 'yfinance'  # <-- NEW SETTING

# The asset pair we want to analyze
# For yfinance, EUR/USD ticker is 'EURUSD=X'
ASSET = 'EURUSD=X'  # <-- CHANGED

# The timeframe (yfinance uses '1d' for daily)
TIMEFRAME = '1d'

# Exchange is only used if DATA_SOURCE is 'ccxt'
EXCHANGE = 'binance' 

# Start date for fetching historical data (YYYY-MM-DD)
START_DATE = '2010-01-01' # <-- CHANGED (Let's take more history for FX)

# --- File Paths ---
# Where to cache the downloaded data
DATA_FILEPATH = 'data/eur_usd_1d.csv'  # <-- CHANGED

# Where to save the final chart
CHART_FILEPATH = 'output/eur_usd_volatility_breaks.png'  # <-- CHANGED

# --- Analysis Settings ---
# 'l2' (Least Squares) is good for detecting shifts in the mean (of variance)
COST_MODEL = 'l2'

# The number of structural breaks to find
N_BREAKS = 10