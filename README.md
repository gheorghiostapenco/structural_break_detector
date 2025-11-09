# Structural Break Detector for Financial Time Series

## Description

This is a Python tool designed to detect structural breaks in the **volatility** of financial time series. It identifies significant changes in market regimes by performing a statistical analysis on the mean of the squared log-returns.

The tool is configurable to fetch data from different sources, including cryptocurrency exchanges (via `ccxt`) and traditional markets like Forex or Stocks (via `yfinance`).

The final output is a price chart saved as a `.png` file, with vertical lines annotating the dates of the detected structural breaks.

## Features

* Detects structural breaks in time series volatility using the `ruptures` library.
* Configurable data sources: `ccxt` (Crypto) and `yfinance` (Forex, Stocks).
* Modular source code (`src/`) for easy maintenance and extension.
* Caches downloaded data to a `data/` directory (CSV) for faster re-runs.
* Generates and saves a `.png` visualization of the price history with breaks overlaid.

## How to Run

### 1. Installation

First, create a virtual environment to manage the project's dependencies.

```bash
# Create a virtual environment named 'venv'
python3 -m venv venv

# Activate the virtual environment
source venv/bin/activate

# Install all required packages
pip install -r requirements.txt
```

2. Configuration
All settings are managed in the src/config.py file. Before running, you can adjust the key settings to define your analysis:

DATA_SOURCE: The data provider. Set to 'ccxt' or 'yfinance'.

ASSET: The ticker symbol to analyze.

Examples for ccxt: 'BTC/USDT', 'ETH/USDT'

Examples for yfinance: 'EURUSD=X', 'SPY', 'AAPL'

START_DATE: The start date for fetching data (e.g., '2017-01-01').

N_BREAKS: The fixed number of structural breaks you want the algorithm to find.

3. Execution
Ensure your virtual environment is still active (you should see (venv) in your terminal prompt).

Run the main script from the project's root directory:

```bash
python main.py
```

4. Output
The script will print its progress to the terminal, showing each step:

Loading data (from cache or network)

Processing signal

Detecting breaks

Visualizing results

The final chart (e.g., eur_usd_volatility_breaks.png) will be saved in the output/ directory.