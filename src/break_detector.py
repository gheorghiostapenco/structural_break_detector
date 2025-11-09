# src/break_detector.py

import ruptures as rpt
import pandas as pd
from src import config # Import our configuration

def find_breakpoints(signal_df: pd.DataFrame) -> list:
    """
    Finds structural break points in the given signal.

    Args:
        signal_df (pd.DataFrame): The DataFrame containing the 'signal' column
                                  prepared by the signal_processor.

    Returns:
        list: A list of datetime objects representing the detected
              breakpoint dates.
    """
    
    # 1. Extract the signal as a numpy array
    # ruptures library expects a numpy array as input
    signal_values = signal_df['signal'].values
    
    print("Starting structural break detection...")

    # 2. Initialize the algorithm
    # We use 'Dynp' (Dynamic Programming) - it is exact and fast enough for
    # a few thousand data points.
    # 'Binseg' (Binary Segmentation) is faster but less accurate.
    # We use the COST_MODEL from our config (e.g., 'l2')
    algo = rpt.Dynp(model=config.COST_MODEL).fit(signal_values)
    
    # 3. Predict the breakpoints
    # We ask it to find N_BREAKS, which we defined in our config.
    # This returns a list of *indices* (integers) where the breaks occur.
    # Note: These indices are +1 relative to the *end* of a segment.
    try:
        result_indices = algo.predict(n_bkps=config.N_BREAKS)
        print(f"Found {len(result_indices)} break indices: {result_indices}")

        # The result includes the *end* of the array, which we don't
        # need as a "break date".
        # e.g., if data has 1000 points, result is [200, 500, 1000]
        # We only care about 200 and 500.
        if result_indices[-1] == len(signal_values):
            result_indices = result_indices[:-1]
            
    except rpt.exceptions.BadSegmentation as e:
        print(f"Error during segmentation: {e}")
        print("This can happen if N_BREAKS is too high for the data.")
        return []

    # 4. Convert indices back to dates
    # The indices from ruptures correspond to locations in our numpy array.
    # We need to map them back to the original dates from the DataFrame's index.
    break_dates = []
    for idx in result_indices:
        # Ensure index is within bounds (it should be)
        if idx < len(signal_df):
            break_dates.append(signal_df.index[idx])
        
    print(f"Successfully converted indices to {len(break_dates)} dates.")
    return break_dates

# --- Standalone test ---
if __name__ == '__main__':
    # This block allows us to run this file directly to test it:
    # python src/break_detector.py
    
    print("Running break_detector as a standalone script...")

    # Create a dummy signal:
    # 100 points of low volatility (mean=0.1)
    # 100 points of high volatility (mean=1.0)
    # 100 points of medium volatility (mean=0.5)
    np_signal = pd.concat([
        pd.Series(np.random.normal(0.1, 0.05, 100)),
        pd.Series(np.random.normal(1.0, 0.2, 100)),
        pd.Series(np.random.normal(0.5, 0.1, 100))
    ]).values
    
    # Create a dummy index
    dummy_index = pd.date_range('2023-01-01', periods=300)
    dummy_df = pd.DataFrame({'signal': np_signal}, index=dummy_index)

    print(f"Created a dummy signal with {len(dummy_df)} points.")
    print("Expecting breaks around index 100 and 200.")

    # Override config for this test
    config.COST_MODEL = 'l2'
    config.N_BREAKS = 2 # We expect 2 breaks

    dates = find_breakpoints(dummy_df)
    
    if dates:
        print("\n--- Test Results ---")
        print(f"Found {len(dates)} break dates:")
        for d in dates:
            print(d.strftime('%Y-%m-%d'))
            
        # We can also check the index location
        idx_locs = [dummy_df.index.get_loc(d) for d in dates]
        print(f"\nCorresponding indices: {idx_locs}")
        print("Test successful if indices are close to 100 and 200.")