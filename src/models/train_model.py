import os
import sys
import numpy as np
import pandas as pd
import pymc as pm
import arviz as az
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Dict, Any

# Ensure the project root is in the system path for module imports.
# This is crucial for the script to find data_loader, preprocessor, and bcp_model.
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(os.path.dirname(current_dir))
sys.path.append(project_root)

# Import the custom modules.
from src.data_ingestion.data_loader import load_data
from src.data_processing.preprocessor import preprocess_data
from src.models.bcp_model import build_bcp_model


def train_and_analyze_bcp_model(prices_path: str, events_path: str):
    """
    Loads, preprocesses, and trains a Bayesian Change Point model.
    It then analyzes and visualizes the results, printing the outputs directly.

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
        # Ensure the model is built with a backend that supports PyMC
        with pm.Model() as bcp_model:
            # Build the model using the provided function
            build_bcp_model(log_returns)

            # Sample from the posterior distribution using MCMC
            # We will use a smaller number of draws for demonstration purposes
            print("Sampling posterior distribution...")
            trace = pm.sample(draws=2000, tune=1000, cores=1, random_seed=42, return_inferencedata=True)

        # Step 3: Analyze and Visualize the Results
        print("\n--- Analyzing and Visualizing Results ---")

        # Get the posterior mean of the change point 'tau'
        tau_samples = trace.posterior['tau'].values.flatten()
        tau_mean = int(np.mean(tau_samples))
        change_point_date = dates[tau_mean]

        # Get the posterior means of the pre- and post-change parameters
        mu_1_post = az.summary(trace, var_names=['mu_1'])['mean'].values[0]
        sigma_1_post = az.summary(trace, var_names=['sigma_1'])['mean'].values[0]
        mu_2_post = az.summary(trace, var_names=['mu_2'])['mean'].values[0]
        sigma_2_post = az.summary(trace, var_names=['sigma_2'])['mean'].values[0]

        # Print a summary of the model parameters
        print(f"Posterior mean for change point (tau): {tau_mean} (Index)")
        print(f"Detected change point date: {change_point_date.strftime('%Y-%m-%d')}")
        print(f"Posterior mean for mu_1 (pre-change mean): {mu_1_post:.4f}")
        print(f"Posterior mean for sigma_1 (pre-change std dev): {sigma_1_post:.4f}")
        print(f"Posterior mean for mu_2 (post-change mean): {mu_2_post:.4f}")
        print(f"Posterior mean for sigma_2 (post-change std dev): {sigma_2_post:.4f}")

        # Visualize the change point and posterior distributions
        # Plot the log returns and the detected change point
        plt.figure(figsize=(15, 6))
        plt.plot(dates, log_returns, label='Log Returns', alpha=0.7)
        plt.axvline(x=change_point_date, color='red', linestyle='--', label=f'Change Point: {change_point_date.strftime("%Y-%m-%d")}')
        plt.title('Log Returns with Detected Change Point')
        plt.xlabel('Date')
        plt.ylabel('Log Returns')
        plt.legend()
        plt.grid(True)
        plt.show()

        # Plot the posterior distribution of the change point 'tau'
        plt.figure(figsize=(10, 6))
        sns.histplot(tau_samples, kde=True, bins=50)
        plt.axvline(x=tau_mean, color='red', linestyle='--', label=f'Mean Tau: {tau_mean}')
        plt.title('Posterior Distribution of the Change Point (tau)')
        plt.xlabel('Change Point Index')
        plt.ylabel('Frequency')
        plt.legend()
        plt.show()
        
        # Step 4: Associate Change Point with External Events
        print("\n--- Associating Change Point with Events ---")
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


def get_analysis_results(prices_path: str, events_path: str) -> Dict[str, Any]:
    """
    Loads, preprocesses, and trains a Bayesian Change Point model.
    It returns the key results in a dictionary instead of printing them.
    This is the "current" method requested by the user.

    Args:
        prices_path (str): The file path to the Brent oil prices CSV.
        events_path (str): The file path to the events CSV.
    
    Returns:
        Dict[str, Any]: A dictionary containing the raw data, preprocessed data,
                        model results, and associated events.
    """
    try:
        # Step 1: Data Ingestion and Preprocessing
        print("--- Loading and Preprocessing Data ---")
        prices_raw, events_raw = load_data(prices_path, events_path)
        preprocessed_df = preprocess_data(prices_raw, events_raw)

        log_returns = preprocessed_df['Log_Returns'].dropna().values
        dates = preprocessed_df['Log_Returns'].dropna().index

        # Step 2: Build and Train the Bayesian Change Point Model
        print("\n--- Building and Training PyMC Model ---")
        with pm.Model() as bcp_model:
            build_bcp_model(log_returns)
            print("Sampling posterior distribution...")
            trace = pm.sample(draws=2000, tune=1000, cores=1, random_seed=42, return_inferencedata=True)

        # Step 3: Analyze and Extract Key Results
        tau_samples = trace.posterior['tau'].values.flatten()
        tau_mean = int(np.mean(tau_samples))
        change_point_date = dates[tau_mean]

        mu_1_post = az.summary(trace, var_names=['mu_1'])['mean'].values[0]
        sigma_1_post = az.summary(trace, var_names=['sigma_1'])['mean'].values[0]
        mu_2_post = az.summary(trace, var_names=['mu_2'])['mean'].values[0]
        sigma_2_post = az.summary(trace, var_names=['sigma_2'])['mean'].values[0]

        # Step 4: Associate Change Point with External Events
        event_date_buffer = pd.Timedelta(days=30)
        relevant_events = events_raw[
            (events_raw['Date'] >= change_point_date - event_date_buffer) &
            (events_raw['Date'] <= change_point_date + event_date_buffer)
        ].sort_values(by='Date')

        # Convert to list of dicts for JSON serialization if needed
        relevant_events_list = relevant_events.to_dict('records')

        # Return a dictionary of all results
        return {
            'prices_raw': prices_raw.to_dict('records'),
            'preprocessed_df': preprocessed_df.reset_index().to_dict('records'),
            'model_results': {
                'trace': trace,  # Return the full trace for further analysis
                'tau_mean': tau_mean,
                'change_point_date': change_point_date.strftime('%Y-%m-%d'),
                'mu_1_post': mu_1_post,
                'sigma_1_post': sigma_1_post,
                'mu_2_post': mu_2_post,
                'sigma_2_post': sigma_2_post,
                'tau_samples': tau_samples.tolist(), # Convert to list for JSON serialization
            },
            'events_raw': events_raw.to_dict('records'),
            'relevant_events': relevant_events_list,
        }

    except FileNotFoundError as e:
        print(f"Error: {e}")
        return {"error": str(e)}
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return {"error": f"An unexpected error occurred: {e}"}


if __name__ == '__main__':
    # Define file paths. Assuming a standard project structure.
    prices_file_path = os.path.join(project_root, 'data', 'raw', 'BrentOilPrices.csv')
    events_file_path = os.path.join(project_root, 'data', 'raw', 'events.csv')
    
    # -------------------------------------------------------------
    # Demonstration of the first method: `train_and_analyze_bcp_model`
    # This method prints and visualizes the results directly.
    # -------------------------------------------------------------
    print("------------------------------------------------------------------------")
    print("--- DEMONSTRATION OF METHOD 1: PRINTING AND VISUALIZING RESULTS ---")
    print("------------------------------------------------------------------------")
    train_and_analyze_bcp_model(prices_file_path, events_file_path)

    print("\n\n")

    # -------------------------------------------------------------
    # Demonstration of the second method: `get_analysis_results`
    # This method returns a dictionary of results, which we can then
    # process or inspect as needed.
    # -------------------------------------------------------------
    print("------------------------------------------------------------------------")
    print("--- DEMONSTRATION OF METHOD 2: RETURNING RESULTS AS A DICTIONARY ---")
    print("------------------------------------------------------------------------")
    results = get_analysis_results(prices_file_path, events_file_path)

    if 'error' not in results:
        print("\nSuccessfully ran the analysis and received the results dictionary.")
        print("Here is a summary of the returned data:")
        
        # Access and print some key results from the dictionary
        model_results = results['model_results']
        print(f"  - Detected Change Point Date: {model_results['change_point_date']}")
        print(f"  - Posterior Mean of Pre-change Mean (mu_1): {model_results['mu_1_post']:.4f}")
        print(f"  - Posterior Mean of Post-change Mean (mu_2): {model_results['mu_2_post']:.4f}")
        
        print("\nPotentially Related Events from the returned dictionary:")
        if results['relevant_events']:
            for event in results['relevant_events']:
                print(f"  - {event['Date']}: {event['Event_Name']}")
        else:
            print("  - No significant events found around the detected change point.")
            
        print("\nFull results dictionary is available for further analysis or serialization.")
    else:
        print(f"An error occurred: {results['error']}")

