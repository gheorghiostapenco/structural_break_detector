# src/config.py

# --- Data Source Settings ---
# 'ccxt' for Crypto, 'yfinance' for Stocks/FX
DATA_SOURCE = 'yfinance'

# The asset pair we want to analyze
# For yfinance, EUR/USD ticker is 'EURUSD=X'
ASSET = 'EURUSD=X'

# The timeframe (yfinance uses '1d' for daily)
TIMEFRAME = '1d'

# Exchange is only used if DATA_SOURCE is 'ccxt'
EXCHANGE = 'binance' 

# Start date for fetching historical data (YYYY-MM-DD)
START_DATE = '2010-01-01'

# --- File Paths ---
# Where to cache the downloaded data
DATA_FILEPATH = 'data/eur_usd_1d.csv'

# Where to save the final chart
CHART_FILEPATH = 'output/eur_usd_volatility_breaks.png'

# --- Analysis Settings ---
# The cost model to use for change point detection.
# "l2" (Least Squares) is good for detecting shifts in the mean (of variance).
COST_MODEL = 'l2'

# Penalty multiplier for automatic break detection (BIC-based).
# Higher value = fewer breaks (less sensitive).
# Lower value = more breaks (more sensitive).
# A good starting point is between 2.0 and 3.0.
PENALTY_MULTIPLIER = 3.0