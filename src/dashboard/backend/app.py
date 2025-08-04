# app.py
# This script combines all backend logic into a single, clear file.
# It runs the Bayesian Change Point analysis once on startup and serves
# the results via a single, comprehensive API endpoint.

import os
import sys
import pandas as pd
import numpy as np
import pymc as pm
import arviz as az
from flask import Flask, jsonify
from flask_cors import CORS
from typing import Dict, Any, List

# --- Path Configuration ---
# Dynamically add the project root directory to the Python path.
# This ensures that imports work correctly regardless of where the script is run from.
current_dir = os.path.dirname(os.path.abspath(__file__))
# Assumes a project structure like: /project-root/src/api/app.py
project_root = os.path.abspath(os.path.join(current_dir, '..', '..', '..'))
sys.path.append(project_root)

# Import your custom modules.
from src.data_ingestion.data_loader import load_data
from src.data_processing.preprocessor import preprocess_data
from src.models.bcp_model import build_bcp_model
from src.models.train_model import get_analysis_results

# --- Flask App Initialization ---
app = Flask(__name__)
# Enable CORS for all routes, allowing the React frontend to make requests.
CORS(app)

# Define file paths relative to the project root.
PRICES_FILE_PATH = os.path.join(project_root, 'data', 'raw', 'BrentOilPrices.csv')
EVENTS_FILE_PATH = os.path.join(project_root, 'data', 'raw', 'events.csv')

# --- Global variable to store pre-computed analysis results ---
# This dictionary will hold all the data needed by the frontend.
analysis_data: Dict[str, Any] = {}

def run_full_analysis_and_serialize() -> Dict[str, Any]:
    """
    Runs the entire Bayesian Change Point analysis pipeline, from data
    ingestion to model training, and serializes the results into a
    JSON-friendly dictionary.

    Returns:
        Dict[str, Any]: A dictionary containing all analysis results, or
                        an error message if the analysis fails.
    """
    print("Starting full analysis pipeline...")
    try:
        # Step 1: Data Ingestion and Preprocessing
        print("--- Loading and Preprocessing Data ---")
        prices_raw_df, events_raw_df = load_data(PRICES_FILE_PATH, EVENTS_FILE_PATH)
        preprocessed_df = preprocess_data(prices_raw_df, events_raw_df)

        # Extract log returns for the model, dropping the initial NaN.
        log_returns = preprocessed_df['Log_Returns'].dropna().values
        dates = preprocessed_df['Log_Returns'].dropna().index

        # Step 2: Build and Train the Bayesian Change Point Model
        print("\n--- Building and Training PyMC Model ---")
        with pm.Model() as bcp_model:
            build_bcp_model(log_returns)
            print("Sampling posterior distribution...")
            # Use a smaller number of draws for faster execution in a web context.
            trace = pm.sample(draws=2000, tune=1000, cores=1, random_seed=42, return_inferencedata=True)
        
        # Step 3: Analyze and Extract Results for the Dashboard
        print("\n--- Analyzing Results and Preparing for Serialization ---")
        
        # Get the posterior mean of the change point index.
        tau_post_mean_idx = int(np.round(trace.posterior['tau'].mean().item()))
        
        # Map the index back to the actual date from the time series.
        change_point_date = str(dates[tau_post_mean_idx].strftime('%Y-%m-%d'))
        
        # Extract the posterior means of the model parameters.
        mu_1_post = trace.posterior['mu_1'].mean().item()
        mu_2_post = trace.posterior['mu_2'].mean().item()
        sigma_1_post = trace.posterior['sigma_1'].mean().item()
        sigma_2_post = trace.posterior['sigma_2'].mean().item()
        
        # Find events near the detected change point date (e.g., within a 30-day window).
        change_point_dt = pd.to_datetime(change_point_date)
        window = pd.Timedelta(days=30)
        
        relevant_events_list = [
            event for _, event in events_raw_df.iterrows()
            if change_point_dt - window <= pd.to_datetime(event['Date']) <= change_point_dt + window
        ]
        
        # Step 4: Convert all data to JSON-friendly formats
        # Convert prices_raw DataFrame to a list of dictionaries.
        prices_raw_list = prices_raw_df.reset_index().rename(columns={'index': 'Date'}).to_dict('records')
        
        # Convert preprocessed_df DataFrame to a list of dictionaries.
        preprocessed_df_list = preprocessed_df.reset_index().rename(columns={'index': 'Date'}).dropna().to_dict('records')

        # Convert event dates to string format for JSON serialization.
        formatted_events = [
            {**event, 'Date': pd.to_datetime(event['Date']).strftime('%Y-%m-%d')}
            for event in relevant_events_list
        ]
        
        # Assemble the final results dictionary.
        results = {
            'prices_raw': prices_raw_list,
            'preprocessed_data': preprocessed_df_list,
            'model_results': {
                'change_point_date': change_point_date,
                'mu_1_post': mu_1_post,
                'mu_2_post': mu_2_post,
                'sigma_1_post': sigma_1_post,
                'sigma_2_post': sigma_2_post
            },
            'relevant_events': formatted_events
        }
        
        print("Analysis successfully completed and results are ready for the API.")
        return results

    except Exception as e:
        print(f"An error occurred during analysis on startup: {e}")
        return {"error": f"Failed to run analysis: {str(e)}"}

# --- Data Loading and Analysis on Application Startup ---
# This is an efficient approach: the heavy analysis is run once when the server
# starts, and the results are stored in memory. Subsequent API calls will be
# fast as they just retrieve the pre-computed data.
try:
    analysis_data = run_full_analysis_and_serialize()
    if 'error' in analysis_data:
        raise Exception(analysis_data['error'])
    print("\nAPI is ready to serve data.")
except Exception as e:
    print(f"Error during app startup: {e}")
    analysis_data = {"error": f"Failed to initialize analysis on startup: {str(e)}"}


# --- API Endpoint to get all data ---
@app.route('/api/all_data', methods=['GET'])
def get_all_data():
    """
    A comprehensive endpoint to get all analysis data in a single request.
    This includes raw prices, preprocessed data, model results, and related events.
    """
    if 'error' in analysis_data:
        return jsonify(analysis_data), 500
    
    return jsonify(analysis_data)


# --- Run the Flask App ---
if __name__ == '__main__':
    # When running locally, use this to start the development server.
    app.run(debug=True, port=5000)

