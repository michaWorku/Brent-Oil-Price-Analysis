import pandas as pd
import numpy as np
import os

def preprocess_data(prices_df: pd.DataFrame, events_df: pd.DataFrame) -> pd.DataFrame:
    """
    Performs data preprocessing on the raw prices and events data.
    
    The key preprocessing steps include:
    1. Setting the date as the index.
    2. Calculating log returns to achieve a stationary series.
    3. Merging the events data to the prices data for later analysis.

    Args:
        prices_df (pd.DataFrame): The raw Brent oil prices DataFrame.
        events_df (pd.DataFrame): The raw events DataFrame.

    Returns:
        pd.DataFrame: A preprocessed DataFrame ready for modeling.
    """
    print("Starting data preprocessing...")
    
    # Set the 'Date' column as the index for time series operations.
    prices_df.set_index('Date', inplace=True)
    
    # Calculate log returns. This is a crucial step for generating a stationary series,
    # which is required for the change point model.
    prices_df['Log_Returns'] = np.log(prices_df['Price'] / prices_df['Price'].shift(1))
    
    # Drop the first row, which will have a NaN value after the shift operation.
    prices_df.dropna(inplace=True)
    
    # Perform a left merge to associate events with the price data.
    # This aligns events from the events_df with the corresponding dates in the prices_df.
    # The column to merge on is renamed to ensure a clear join.
    events_df.rename(columns={'Approximate_Date': 'Date'}, inplace=True)
    prices_df = prices_df.merge(events_df, how='left', left_index=True, right_on='Date')
    
    # Fill NaN values in the newly merged columns with 'No Event'.
    # This prevents issues with the data during later analysis or visualization.
    prices_df[['Event_Name', 'Description']] = prices_df[['Event_Name', 'Description']].fillna('No Event')
    
    # Set the date back as the index for the final preprocessed DataFrame.
    prices_df.set_index('Date', inplace=True)
    prices_df.sort_index(inplace=True)

    print("Data preprocessing completed. Data is ready for modeling.")
    return prices_df

def save_preprocessed_data(df: pd.DataFrame, output_path: str, filename: str = 'preprocessed_data.csv'):
    """
    Saves the preprocessed DataFrame to a specified output directory.

    Args:
        df (pd.DataFrame): The DataFrame to save.
        output_path (str): The directory where the file will be saved.
        filename (str): The name of the output CSV file.
    """
    # Ensure the output directory exists
    os.makedirs(output_path, exist_ok=True)
    
    full_path = os.path.join(output_path, filename)
    print(f"\nSaving preprocessed data to '{full_path}'...")
    df.to_csv(full_path, index=True)
    print("Data saved successfully.")

# Example usage when run directly
if __name__ == '__main__':
    # Demonstration of the `preprocess_data` and `save_preprocessed_data` functions.
    print("Demonstration of the preprocessor.py script.")
    
    # Simulate loading data.
    prices_data = {
        'Date': pd.to_datetime(['1990-01-01', '1990-01-02', '1990-01-03']),
        'Price': [20.0, 20.5, 21.0]
    }
    events_data = {
        'Date': pd.to_datetime(['1990-01-02']),
        'Event_Name': ['Sample Event'],
        'Description': ['A test event']
    }
    
    prices_df_raw = pd.DataFrame(prices_data)
    events_df_raw = pd.DataFrame(events_data)
    
    # Call the preprocessing function.
    preprocessed_df = preprocess_data(prices_df_raw, events_df_raw)
    
    print("\nFinal preprocessed DataFrame ready for modeling:")
    print(preprocessed_df)

    # Save the preprocessed data to the 'data/processed' directory.
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(os.path.dirname(current_dir))
    output_dir = os.path.join(project_root, 'data', 'processed')
    save_preprocessed_data(preprocessed_df, output_dir)
