import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import sys
import numpy as np

# Add the project root to the path for module imports
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(os.path.dirname(current_dir))
sys.path.append(project_root)

# Import our custom modules
from src.data_ingestion.data_loader import load_data
from src.data_processing.preprocessor import preprocess_data


def basic_data_inspection(df: pd.DataFrame):
    """
    Prints basic information and summary statistics of the DataFrame.
    """
    print("--- Basic Data Inspection ---")
    print("\nData Information:")
    df.info()
    print("\nSummary Statistics:")
    print(df.describe())
    print("-" * 30)

def missing_values_analysis(df: pd.DataFrame):
    """
    Identifies and visualizes missing values in the DataFrame.
    """
    print("\n--- Missing Values Analysis ---")
    missing_values = df.isnull().sum()
    missing_values = missing_values[missing_values > 0]
    
    if not missing_values.empty:
        print("\nMissing Values Count by Column:")
        print(missing_values)
        
        # Visualize missing values
        plt.figure(figsize=(15, 7))
        sns.heatmap(df.isnull(), cbar=False, cmap='viridis')
        plt.title("Missing Values Heatmap")
        plt.tight_layout()
        plt.show()
    else:
        print("No missing values found.")
    print("-" * 30)

def univariate_analysis(df: pd.DataFrame, feature: str):
    """
    Performs and visualizes a univariate analysis on a specific feature.
    """
    print(f"\n--- Univariate Analysis of '{feature}' ---")
    plt.figure(figsize=(12, 6))
    sns.histplot(df[feature].dropna(), bins=100, kde=True)
    plt.title(f'Distribution of {feature}', fontsize=16)
    plt.xlabel(feature)
    plt.ylabel('Frequency')
    plt.tight_layout()
    plt.show()
    print("-" * 30)

def temporal_analysis(df: pd.DataFrame, time_column: str, metrics: list):
    """
    Performs and visualizes a temporal analysis of specified metrics over time.
    """
    print("\n--- Temporal Analysis ---")
    for metric in metrics:
        if metric in df.columns:
            plt.figure(figsize=(15, 7))
            sns.lineplot(data=df, x=time_column, y=metric)
            plt.title(f'Trend of {metric} Over Time', fontsize=16)
            plt.xlabel('Date')
            plt.ylabel(metric)
            plt.grid(True)
            plt.tight_layout()
            plt.show()
        else:
            print(f"Warning: Metric '{metric}' not found in DataFrame. Skipping plot.")
    print("-" * 30)

def analyze_data(prices_path: str, events_path: str):
    """
    Main function to orchestrate the entire data analysis process.
    It loads, preprocesses, and performs comprehensive EDA on the data.
    """
    try:
        # Step 1: Data Ingestion
        prices_raw, events_raw = load_data(prices_path, events_path)
        
        # Step 2: Data Preprocessing
        preprocessed_df = preprocess_data(prices_raw, events_raw)
        
        # Reset index to make 'Date' a column for plotting
        preprocessed_df.reset_index(inplace=True)

        print("--- Starting Comprehensive Data Analysis ---")
        
        # Step 3: Perform EDA using the consolidated functions
        basic_data_inspection(preprocessed_df)
        missing_values_analysis(preprocessed_df)
        
        # Perform univariate analysis for key features
        univariate_analysis(preprocessed_df, 'Price')
        univariate_analysis(preprocessed_df, 'Log_Returns')
        
        # Perform temporal analysis for key features
        temporal_analysis(preprocessed_df, 'Date', ['Price', 'Log_Returns'])
        
        print("--- Comprehensive Data Analysis Complete ---")

    except FileNotFoundError as e:
        print(f"Error: {e}")
        print("Please ensure 'BrentOilPrices.csv' and 'events.csv' are in the 'data/raw/' directory.")

if __name__ == '__main__':
    # Define file paths (assuming a standard project structure)
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(os.path.dirname(current_dir))
    PRICES_FILE_PATH = os.path.join(project_root, 'data', 'raw', 'BrentOilPrices.csv')
    EVENTS_FILE_PATH = os.path.join(project_root, 'data', 'raw', 'events.csv')

    analyze_data(PRICES_FILE_PATH, EVENTS_FILE_PATH)
