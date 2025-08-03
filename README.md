# **Brent-Oil-Price-Analysis**

## **Project Description**

### **Business Understanding**

The main goal of this analysis is to study how important events affect Brent oil prices to provide insights to investors, analysts, and policymakers. Birhan Energies, a consultancy firm specializing in the energy sector, aims to deliver data-driven intelligence that supports decision-making processes, risk management, and strategic planning. I am tasked with analyzing how big political and economic events affect Brent oil prices and how they are linked to changes in oil prices.

### **Project Overview**

This project uses change point analysis and statistical modeling to detect significant structural breaks in historical Brent oil price data. I will apply a Bayesian change point detection model using PyMC3 to identify these shifts and then associate them with key geopolitical events, OPEC decisions, and economic shocks. The final deliverable will be a clear report and an interactive dashboard to communicate the findings.

### **Key Features**

- **Change Point Detection:** Identifies statistically significant shifts in Brent oil price behavior.
- **Event Correlation:** Formulates hypotheses about which events caused the detected price shifts.
- **Quantitative Impact Analysis:** Measures and quantifies the impact of key events on oil prices.
- **Interactive Dashboard:** A web-based application (Flask + React) to visualize the analysis results and allow stakeholders to explore the data.

### **Business Objectives**

- Finding key events that have significantly impacted Brent oil prices.
- Measuring the effect of these events on price changes.
- Providing clear, data-driven insights to guide investment strategies, policy development, and operational planning.

## **Project Structure**
```
├── .vscode/                 # VSCode specific settings
├── .github/                 # GitHub specific configurations (e.g., Workflows)
│   └── workflows/
│       └── unittests.yml    # CI/CD workflow for tests and linting
├── .gitignore               # Specifies intentionally untracked files to ignore
├── requirements.txt         # Python dependencies
├── pyproject.toml           # Modern Python packaging configuration (PEP 517/621)
├── README.md                # Project overview, installation, usage
├── Makefile                 # Common development tasks (setup, test, lint, clean)
├── .env                     # Environment variables (e.g., API keys - kept out of Git)
├── src/                          # Core source code for the project
│   ├── data_ingestion/           # Scripts for data acquisition and initial cleaning
│   │   └── load_data.py          # Loads raw data, compiles event data, and performs initial validation
│   ├── data_processing/          # Scripts for data transformation and feature engineering
│   │   └── preprocess_data.py    # Calculates log returns, merges datasets, and prepares data for modeling
│   ├── EDA/                      # Scripts for Exploratory Data Analysis (EDA)
│   │   └── analyze_data.py       # Performs initial analysis, plots trends, and checks for stationarity
│   ├── models/                   # Bayesian change point modeling
│   │   ├── bcp_model.py          # Defines the Bayesian Change Point model using PyMC3
│   │   └── train_model.py        # Script to run the MCMC sampler and save the model output
│   ├── dashboard/                # Code for the interactive dashboard
│   │   ├── backend/              # Flask application to serve model results
│   │   │   └── app.py            # Main Flask application file
│   │   └── frontend/             # React application for the user interface
│   │       ├── public/
│   │       └── src/
│   └── utils/               # Utility functions and helper classes
│       └── helpers.py       # General helper functions
├── tests/                   # Test suite (unit, integration)
│   ├── unit/                # Unit tests for individual components
│   └── integration/         # Integration tests for combined components
├── notebooks/               # Jupyter notebooks for experimentation, EDA, prototyping
    └── eda.ipynb            # Notebook for initial data exploration and visualizations
├── scripts/                 # Standalone utility scripts (e.g., data processing, deployment)
├── docs/                    # Project documentation (e.g., Sphinx docs)
├── data/                    # Data storage (raw, processed)
│   ├── raw/                 # Original, immutable raw data
│   └── processed/           # Transformed, cleaned, or feature-engineered data
├── config/                  # Configuration files
└── examples/                # Example usage of the project components
```


## **Technologies Used**

- **Programming Language:** Python 3.8+
- **Data Analysis:** Pandas, NumPy
- **Statistical Modeling:** PyMC3 (Bayesian inference, MCMC)
- **Frontend:** React
- **Backend:** Flask
- **Visualization:** Matplotlib, Plotly, or a React-based charting library

## **Setup and Installation**

### **Prerequisites**

- Python 3.8+
- Git

### **Steps**

1. **Clone the repository:**
    
    ```
    git clone https://github.com/michaWorku/Brent-Oil-Price-Analysis.git
    cd Brent-Oil-Price-Analysis
    
    ```
    
    *(Update the URL with your repository's URL)*
    
2. **Create and activate a virtual environment:**
    
    ```
    python3 -m venv venv
    source venv/bin/activate  # On Windows: .\venv\Scripts\activate
    
    ```
    
3. **Install dependencies:**
    
    ```
    pip install -r requirements.txt
    
    ```
    

## **Usage**

- Running the Analysis:
    
    The core analysis will be executed through scripts located in src/models/. You can run the main script to perform the change point analysis and save the model results.
    
    ```
    python src/models/run_analysis.py
    
    ```
    
- Launching the Dashboard:
    
    Navigate to the src/dashboard/ directory to run the Flask backend and React frontend.
    
    ```
    # From the project root
    # Start the Flask backend
    python src/dashboard/backend/app.py
    # Then, start the React frontend
    # cd src/dashboard/frontend
    # npm start
    
    ```
    

## **Live Demo**

A link to a live version of the interactive dashboard will be provided upon completion.

## **Development and Evaluation**

The project will be developed in three main tasks: laying the foundation, change point modeling and insight generation, and developing the interactive dashboard. Interim and final submissions will be made on key dates to receive feedback.

## **Contributing**

Guidelines for contributing to the project.

## **License**

This project is licensed under the [MIT License](https://www.google.com/search?q=LICENSE).
