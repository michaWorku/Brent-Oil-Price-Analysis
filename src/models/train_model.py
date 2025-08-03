import os
import sys
import numpy as np
import pandas as pd
import pymc as pm
import arviz as az
import matplotlib.pyplot as plt
import seaborn as sns

# Add the project root to the path for module imports
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(os.path.dirname(current_dir))
sys.path.append(project_root)

from src.data_ingestion.data_loader import load_data
from src.data_processing.preprocessor import preprocess_data
from src.models.bcp_model import build_bcp_model


def train_and_analyze_bcp_model(prices_path: str, events_path: str):
    """
    Loads, preprocesses, and trains a Bayesian Change Point model.
    It then analyzes and visualizes the results.

    Args:
        prices_path (str): The file path to the Brent oil prices CSV.
        events_path (str): The file path to the events CSV.
    """
    try:
        # Step 1: Data Ingestion and Preprocessing
        print("--- Loading and Preprocessing Data ---")
        prices_raw, events_raw = load_data(prices_path, events_path)
        preprocessed_df = preprocess_data(prices_raw, events_raw)

        # Extract log returns, dropping the first NaN value
        log_returns = preprocessed_df['Log_Returns'].dropna().values
        dates = preprocessed_df['Log_Returns'].dropna().index

        # Step 2: Build and Train the Bayesian Change Point Model
        print("\n--- Building and Training PyMC Model ---")
        bcp_model = build_bcp_model(log_returns)
        
        with bcp_model:
            # Run MCMC sampler to find the posterior distributions
            # Explicitly set cores to 4 for more robust computation of convergence diagnostics
            # and to handle potential versioning issues by asking for InferenceData
            idata = pm.sample(2000, tune=1000, cores=4, return_inferencedata=True)

        # Defensive check to ensure the result is an InferenceData object,
        # and convert it if it's not (e.g., if an old MultiTrace object is returned).
        if not isinstance(idata, az.InferenceData):
            print("\nWarning: The sampler did not return an InferenceData object. Attempting to convert...")
            idata = az.from_pymc(idata)

        # Step 3: Analyze and Interpret the Results
        print("\n--- Analyzing Model Results ---")
        print(az.summary(idata, var_names=['tau', 'mu_1', 'mu_2', 'sigma_1', 'sigma_2']))
        
        # Check for convergence with trace plots
        az.plot_trace(idata, var_names=['tau', 'mu_1', 'mu_2', 'sigma_1', 'sigma_2'])
        plt.show()

        # Step 4: Visualize the Change Point
        # The change point is the posterior mean of tau
        tau_post = idata.posterior['tau'].mean().item()
        change_point_date = dates[int(tau_post)]
        print(f"\nMost probable change point date: {change_point_date.strftime('%Y-%m-%d')}")

        # Plot the posterior distribution of the change point
        plt.figure(figsize=(12, 6))
        sns.histplot(dates[idata.posterior['tau'].values.flatten().astype(int)], bins=30, kde=True)
        plt.title('Posterior Distribution of the Change Point (tau)')
        plt.xlabel('Date')
        plt.ylabel('Frequency')
        plt.tight_layout()
        plt.show()

        # Step 5: Quantify the Impact
        mu_1_post = idata.posterior['mu_1'].mean().item()
        mu_2_post = idata.posterior['mu_2'].mean().item()
        print("\nQuantifying the Impact of the Change:")
        print(f"Average log return BEFORE the change: {mu_1_post:.4f}")
        print(f"Average log return AFTER the change: {mu_2_post:.4f}")

        # Step 6: Associate Change Point with External Events
        print("\n--- Associating Change Point with Events ---")
        print("Detected change point date:", change_point_date.strftime('%Y-%m-%d'))
        
        # Filter events close to the detected change point
        event_date_buffer = pd.Timedelta(days=30)
        relevant_events = events_raw[
            (events_raw['Date'] >= change_point_date - event_date_buffer) &
            (events_raw['Date'] <= change_point_date + event_date_buffer)
        ].sort_values(by='Date')

        if not relevant_events.empty:
            print("\nPotentially Related Events:")
            for _, row in relevant_events.iterrows():
                print(f"- {row['Date'].strftime('%Y-%m-%d')}: {row['Event_Name']}")
        else:
            print("No significant events found around the detected change point.")
            
        print("\n--- Change Point Analysis Complete ---")

    except FileNotFoundError as e:
        print(f"Error: {e}")
        print("Please ensure 'BrentOilPrices.csv' and 'events.csv' are in the 'data/raw/' directory.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


if __name__ == '__main__':
    # Define file paths
    prices_file_path = os.path.join(project_root, 'data', 'raw', 'BrentOilPrices.csv')
    events_file_path = os.path.join(project_root, 'data', 'raw', 'events.csv')
    train_and_analyze_bcp_model(prices_file_path, events_file_path)
