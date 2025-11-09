# src/visualizer.py

import pandas as pd
import matplotlib.pyplot as plt
import os
from src import config

def plot_breaks(analysis_df: pd.DataFrame, break_dates: list):
    """
    Generates and saves a plot of the price series with vertical lines
    indicating the detected structural breakpoints.

    Args:
        analysis_df (pd.DataFrame): The DataFrame from signal_processor,
                                    which must contain the 'price' column.
        break_dates (list): A list of datetime objects (the breakpoints)
                            from break_detector.
    """
    
    print(f"Plotting {len(break_dates)} breaks...")
    
    # --- 1. Set up the plot ---
    fig, ax = plt.subplots(figsize=(15, 8))

    # --- 2. Plot the Price Data ---
    analysis_df['price'].plot(
        ax=ax, 
        label=f'{config.ASSET} Price', 
        color='blue', 
        alpha=0.8,
        linewidth=1.0
    )

    # --- 3. Add Vertical Lines for Breaks ---
    if break_dates:
        # Plot the first break with a label
        ax.axvline(
            break_dates[0], 
            color='red', 
            linestyle='--', 
            linewidth=1.5, 
            label='Structural Break (Volatility)'
        )
        # Plot the rest without labels
        for date in break_dates[1:]:
            ax.axvline(date, color='red', linestyle='--', linewidth=1.5)
            
    # --- 4. Customize the Chart ---
    ax.set_title(f'Structural Breaks in {config.ASSET} Volatility', fontsize=16)
    ax.set_xlabel('Date', fontsize=12)
    
    # --- START OF FIX ---
    # Use logarithmic scale on Y-axis (good for both crypto and FX)
    ax.set_yscale('log')
    
    # Try to intelligently set the Y-axis label
    try:
        # This works for 'BTC/USDT' -> 'USDT'
        quote_currency = config.ASSET.split('/')[1]
    except IndexError:
        # This is a fallback for tickers like 'EURUSD=X' or 'SPY'
        # It will just use the full ticker name.
        quote_currency = config.ASSET
        
    ax.set_ylabel(f'Price ({quote_currency})', fontsize=12) # <-- FIXED
    # --- END OF FIX ---
    
    ax.legend()
    ax.grid(True, which="both", linestyle='--', linewidth=0.5, alpha=0.5)
    plt.tight_layout() # Adjusts plot to prevent labels from overlapping

    # --- 5. Save the Figure ---
    output_dir = os.path.dirname(config.CHART_FILEPATH)
    os.makedirs(output_dir, exist_ok=True)
    
    try:
        fig.savefig(config.CHART_FILEPATH, dpi=300) # Save high-res image
        print(f"Successfully saved chart to {config.CHART_FILEPATH}")
    except Exception as e:
        print(f"Error saving chart: {e}")

# --- Standalone test ---
if __name__ == '__main__':
    # This block allows us to run this file directly to test it:
    # python src/visualizer.py
    
    print("Running visualizer as a standalone script...")
    
    import numpy as np
    
    dates = pd.date_range('2020-01-01', periods=365)
    price_data = pd.Series(
        np.exp(np.cumsum(np.random.normal(0.001, 0.02, 365))), 
        index=dates,
        name='price'
    )
    dummy_analysis_df = pd.DataFrame(price_data)

    dummy_breaks = [dates[100], dates[250]] # Two breaks
    
    print(f"Dummy data and {len(dummy_breaks)} breaks created.")

    # Override config path for the test
    config.CHART_FILEPATH = 'output/TEST_visualizer_chart.png'
    config.ASSET = 'TEST/ASSET' # Test the 'try' block
    
    plot_breaks(dummy_analysis_df, dummy_breaks)
    
    print(f"Test chart saved. Please check {config.CHART_FILEPATH}")