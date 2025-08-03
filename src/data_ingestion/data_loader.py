# FILE: src/data_ingestion/data_loader.py

import pandas as pd
import os

def load_data(prices_path: str, events_path: str) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Loads raw Brent oil price data and a compiled events list from CSV files.

    Args:
        prices_path (str): The file path to the Brent oil prices CSV.
        events_path (str): The file path to the events CSV.

    Returns:
        tuple[pd.DataFrame, pd.DataFrame]: A tuple containing the prices DataFrame
                                           and the events DataFrame.
    
    Raises:
        FileNotFoundError: If either of the specified files do not exist.
    """
    # Check if files exist before attempting to load
    if not os.path.exists(prices_path):
        raise FileNotFoundError(f"Price data file not found at: {prices_path}")
    if not os.path.exists(events_path):
        raise FileNotFoundError(f"Events data file not found at: {events_path}")

    print(f"Loading raw data from '{prices_path}' and '{events_path}'...")
    
    # Load the prices data and parse the 'Date' column as datetime objects
    # 'dayfirst=True' is used to correctly interpret the '20-May-87' format
    prices_df = pd.read_csv(
        prices_path,
        parse_dates=['Date'],
        dayfirst=True
    )

    # Load the events data and parse the 'Approximate_Date' column
    events_df = pd.read_csv(
        events_path,
        parse_dates=['Approximate_Date']
    )
    
    # Ensure the prices DataFrame is sorted by date for time series analysis
    prices_df.sort_values('Date', inplace=True)
    prices_df.reset_index(drop=True, inplace=True)

    print("Raw data loaded successfully.")
    return prices_df, events_df

# Example usage when run directly
if __name__ == '__main__':
    # Define file paths (assuming a standard project structure)
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(os.path.dirname(current_dir))
    PRICES_FILE_PATH = os.path.join(project_root, 'data', 'raw', 'BrentOilPrices.csv')
    EVENTS_FILE_PATH = os.path.join(project_root, 'data', 'raw', 'events.csv')
    
    try:
        prices, events = load_data(PRICES_FILE_PATH, EVENTS_FILE_PATH)
        print("\nSuccessfully loaded Brent Oil Prices:")
        print(prices.head())
        print("\nSuccessfully loaded Events Data:")
        print(events.head())
    except FileNotFoundError as e:
        print(f"Error: {e}")
