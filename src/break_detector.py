# src/break_detector.py

import ruptures as rpt
import pandas as pd
import numpy as np  # <-- Make sure numpy is imported
from src import config # Import our configuration

def find_breakpoints(signal_df: pd.DataFrame) -> list:
    """
    Finds structural break points in the given signal using the Pelt
    algorithm with a BIC-based penalty for automatic detection.

    Args:
        signal_df (pd.DataFrame): The DataFrame containing the 'signal' column
                                  prepared by the signal_processor.

    Returns:
        list: A list of datetime objects representing the detected
              breakpoint dates.
    """
    
    # 1. Extract the signal as a numpy array
    signal_values = signal_df['signal'].values
    n_samples = len(signal_values)
    
    print("Starting structural break detection (Automatic)...")

    # 2. Initialize the algorithm
    # We use 'Pelt' (Pruned Exact Linear Time) algorithm.
    # It is fast, exact, and works with a penalty value.
    algo = rpt.Pelt(model=config.COST_MODEL).fit(signal_values)
    
    # 3. Calculate the penalty value (BIC)
    # A common penalty based on Bayesian Information Criterion (BIC) is:
    # pen = C * log(n) * sigma^2
    # Where:
    #   C     = PENALTY_MULTIPLIER (our tuning constant)
    #   n     = n_samples (number of data points)
    #   sigma = standard deviation of the signal
    
    sigma = signal_values.std()
    
    # Ensure sigma is not zero to avoid log(0) or division by zero errors
    # and to ensure penalty is not zero if signal is flat.
    if sigma < 1e-9:
        print("Warning: Signal standard deviation is near zero. No breaks will be found.")
        return []
        
    penalty = config.PENALTY_MULTIPLIER * np.log(n_samples) * (sigma**2)
    print(f"Calculated Penalty (BIC-based): {penalty:.2f}")

    # 4. Predict the breakpoints using the penalty
    # This will automatically find the *optimal number* of breaks
    try:
        # predict() returns a list of indices *ending* segments, e.g., [120, 350, 700, n_samples]
        result_indices = algo.predict(pen=penalty)
        print(f"Found {len(result_indices) - 1} break(s) automatically.")

        # The result includes the *end* of the array, which is not a "break".
        # We must remove it before converting to dates.
        if result_indices and result_indices[-1] == n_samples:
            result_indices = result_indices[:-1]
            
    except Exception as e:
        print(f"Error during segmentation: {e}")
        return []

    # 5. Convert indices back to dates
    break_dates = []
    for idx in result_indices:
        if idx < n_samples: # Safety check
            break_dates.append(signal_df.index[idx])
        
    print(f"Successfully converted {len(break_dates)} indices to dates.")
    return break_dates

# --- Standalone test ---
if __name__ == '__main__':
    # This block allows us to run this file directly to test it:
    # python src/break_detector.py
    
    print("Running break_detector as a standalone script (Automatic)...")

    # Create a dummy signal:
    # 100 points of low volatility (mean=0.1)
    # 100 points of high volatility (mean=1.0)
    # 100 points of medium volatility (mean=0.5)
    np_signal = pd.concat([
        pd.Series(np.random.normal(0.1, 0.05, 100)),
        pd.Series(np.random.normal(1.0, 0.2, 100)),
        pd.Series(np.random.normal(0.5, 0.1, 100))
    ]).values
    
    dummy_index = pd.date_range('2023-01-01', periods=300)
    dummy_df = pd.DataFrame({'signal': np_signal}, index=dummy_index)

    print(f"Created a dummy signal with 3 segments (expecting 2 breaks).")

    # Override config for this test
    config.COST_MODEL = 'l2'
    config.PENALTY_MULTIPLIER = 2.0 # Use a lower penalty for test data

    dates = find_breakpoints(dummy_df)
    
    if dates:
        print("\n--- Test Results ---")
        print(f"Found {len(dates)} break dates:")
        for d in dates:
            print(d.strftime('%Y-%m-%d'))
            
        idx_locs = [dummy_df.index.get_loc(d) for d in dates]
        print(f"\nCorresponding indices: {idx_locs}")
        print("Test successful if indices are close to 100 and 200.")