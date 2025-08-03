import pymc as pm
import numpy as np

def build_bcp_model(data: np.ndarray):
    """
    Builds a Bayesian Change Point model for a given time series using PyMC.

    The model assumes the data's mean and volatility change at an unknown
    point in time. It uses a discrete uniform prior for the change point
    and models the data before and after the change point with two
    separate Normal distributions.

    Args:
        data (np.ndarray): The time series data (e.g., log returns).

    Returns:
        pymc.Model: The defined PyMC model.
    """
    with pm.Model() as bcp_model:
        # Define the prior for the unknown change point 'tau'
        # It's a discrete uniform distribution over the length of the data.
        tau = pm.DiscreteUniform("tau", lower=0, upper=len(data) - 1)

        # Define priors for the mean and standard deviation before the change point
        mu_1 = pm.Normal("mu_1", mu=0.0, sigma=0.1)
        sigma_1 = pm.HalfNormal("sigma_1", sigma=0.1)

        # Define priors for the mean and standard deviation after the change point
        mu_2 = pm.Normal("mu_2", mu=0.0, sigma=0.1)
        sigma_2 = pm.HalfNormal("sigma_2", sigma=0.1)

        # Create an index for the switch function
        idx = np.arange(len(data))
        
        # Combine the "before" and "after" parameters using the switch function
        mu = pm.math.switch(idx < tau, mu_1, mu_2)
        sigma = pm.math.switch(idx < tau, sigma_1, sigma_2)
        
        # Define the likelihood of the observed data
        # We model the data as being normally distributed with the switched mean and std.
        pm.Normal("y", mu=mu, sigma=sigma, observed=data)

    return bcp_model
