# main.py

import sys
import time
from src.data_loader import fetch_and_save_data
from src.signal_processor import prepare_signal
from src.break_detector import find_breakpoints
from src.visualizer import plot_breaks

def main():
    """
    Main function to run the entire analysis pipeline.
    It orchestrates the loading, processing, analysis, and visualization.
    """
    print("Starting the Structural Break Detector...")
    start_time = time.time() # Start timer

    # --- Step 1: Load Data ---
    # Fetch data from the exchange or load from cache
    print("\n[Step 1/4] Loading data...")
    raw_data_df = fetch_and_save_data()

    # Check if data loading was successful
    if raw_data_df.empty:
        print("Error: Failed to load data. Exiting.")
        sys.exit(1) # Exit the script with an error code
    
    print(f"Data loaded successfully. {len(raw_data_df)} rows found.")

    # --- Step 2: Process Signal ---
    # Convert raw price data into the analytical signal (squared log returns)
    print("\n[Step 2/4] Processing signal...")
    analysis_df = prepare_signal(raw_data_df)

    # Check if signal processing was successful
    if analysis_df.empty:
        print("Error: Failed to process signal. Exiting.")
        sys.exit(1)
        
    print("Signal processed successfully.")

    # --- Step 3: Detect Breaks ---
    # Run the 'ruptures' algorithm on our signal
    print("\n[Step 3/4] Detecting breaks...")
    # We pass analysis_df which contains the 'signal' column
    break_dates = find_breakpoints(analysis_df)

    if not break_dates:
        print("Warning: No significant breaks were found with the current settings.")
    else:
        print(f"Successfully found {len(break_dates)} structural breaks.")

    # --- Step 4: Visualize Results ---
    # Plot the original price and overlay the detected break dates
    print("\n[Step 4/4] Visualizing results...")
    # We pass analysis_df again because it contains the 'price' column
    plot_breaks(analysis_df, break_dates)

    # --- Done ---
    end_time = time.time()
    total_time = end_time - start_time
    print(f"\nAnalysis complete in {total_time:.2f} seconds.")
    print("Please check the 'output/' directory for your chart.")

if __name__ == "__main__":
    # This standard Python construct ensures that main() is called
    # only when the script is executed directly (not when imported as a module).
    main()