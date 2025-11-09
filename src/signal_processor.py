# src/signal_processor.py

import pandas as pd
import numpy as np

def prepare_signal(df: pd.DataFrame, target_column: str = 'close') -> pd.DataFrame:
    """
    Prepares the analytical signal from the raw OHLCV data.

    The signal we want to analyze is the *change in variance (volatility)*.
    A common proxy for daily variance is the **squared log return**.
    
    This function calculates:
    1. Log returns: ln(P_t / P_{t-1})
    2. Squared log returns: [ln(P_t / P_{t-1})]^2
    
    It also retains the original price data for later visualization.

    Args:
        df (pd.DataFrame): The input DataFrame from data_loader (must have a 'close' column).
        target_column (str): The column to use for calculations (default is 'close').

    Returns:
        pd.DataFrame: A new DataFrame containing the original close price,
                      log returns, and the signal (squared log returns).
    """
    
    if target_column not in df.columns:
        print(f"Error: Target column '{target_column}' not found in DataFrame.")
        return pd.DataFrame()

    # Create a new DataFrame to avoid modifying the original one in place
    analysis_df = pd.DataFrame(index=df.index)

    # 1. Keep the original price for plotting
    analysis_df['price'] = df[target_column]

    # 2. Calculate Log Returns
    # ln(P_t / P_{t-1}) is a good approximation for percentage change 
    # and has better statistical properties.
    analysis_df['log_return'] = np.log(analysis_df['price'] / analysis_df['price'].shift(1))

    # 3. Calculate Squared Log Returns (Our Signal)
    # This serves as our proxy for daily variance.
    # We will look for structural breaks in the *mean* of this series.
    analysis_df['signal'] = analysis_df['log_return']**2
    
    # The first row will be NaN due to shift(1). We must drop it.
    analysis_df = analysis_df.dropna()

    if analysis_df.empty:
        print("Error: DataFrame is empty after processing. Check input data.")
        return pd.DataFrame()

    print("Signal processing complete.")
    return analysis_df

# --- Standalone test ---
if __name__ == '__main__':
    # This block allows us to run this file directly to test it:
    # python src/signal_processor.py
    
    # We need a dummy DataFrame to test this, let's simulate one
    print("Running signal_processor as a standalone script...")
    
    # Create a simple dummy DataFrame
    dummy_prices = pd.Series([100, 101, 102, 100, 105, 110], 
                             index=pd.date_range('2023-01-01', periods=6))
    dummy_df = pd.DataFrame({'close': dummy_prices})
    
    print("\n--- Input Data (Dummy) ---")
    print(dummy_df)
    
    processed_data = prepare_signal(dummy_df, target_column='close')
    
    if not processed_data.empty:
        print("\n--- Processed Data ---")
        print(processed_data)
        
        # Check calculations
        # log(101/100) = 0.00995...
        # (0.00995)^2 = 0.000099...
        print("\n--- Verification (Row 1) ---")
        print(f"Expected log_return ~0.00995, Got: {processed_data['log_return'].iloc[0]:.6f}")
        print(f"Expected signal ~0.000099, Got: {processed_data['signal'].iloc[0]:.8f}")